-- Helper for stage -> canonical migration.
-- Safe to re-run.

create or replace function public.cb_migrate_stage_table(
  source_table text,
  target_table text default null
)
returns void
language plpgsql
as $$
declare
  src text;
  tgt text;
  src_exists regclass;
  source_has_notion_page_id boolean;
  target_has_notion_page_id boolean;
  has_notion_page_id boolean;
  insert_cols text;
  update_set text;
  updated_rows bigint := 0;
  inserted_rows bigint := 0;
  skipped_null_notion_rows bigint := 0;
begin
  src := lower(trim(coalesce(source_table, '')));
  tgt := lower(trim(coalesce(target_table, '')));

  if src = '' then
    raise exception 'source_table is required';
  end if;

  if tgt = '' then
    if right(src, 6) = '_stage' then
      tgt := left(src, length(src) - 6);
    else
      tgt := src;
    end if;
  end if;

  select to_regclass(format('public.%I', src)) into src_exists;
  if src_exists is null then
    raise exception 'Source table public.% does not exist', src;
  end if;

  -- Create canonical table from stage structure when missing.
  execute format(
    'create table if not exists public.%I (like public.%I including all)',
    tgt,
    src
  );

  select exists (
    select 1
    from information_schema.columns
    where table_schema = 'public'
      and table_name = src
      and column_name = 'notion_page_id'
  ) into source_has_notion_page_id;

  select exists (
    select 1
    from information_schema.columns
    where table_schema = 'public'
      and table_name = tgt
      and column_name = 'notion_page_id'
  ) into target_has_notion_page_id;

  has_notion_page_id := source_has_notion_page_id and target_has_notion_page_id;

  -- Use column intersection so this still works if canonical table already diverged.
  select string_agg(format('%I', s.column_name), ', ' order by s.ordinal_position)
  into insert_cols
  from information_schema.columns s
  join information_schema.columns t
    on t.table_schema = 'public'
   and t.table_name = tgt
   and t.column_name = s.column_name
  where s.table_schema = 'public'
    and s.table_name = src
    and s.column_name <> 'id';

  if insert_cols is null then
    raise exception 'No shared insert columns found between public.% and public.%', src, tgt;
  end if;

  if has_notion_page_id then
    select string_agg(format('%1$I = s.%1$I', s.column_name), ', ' order by s.ordinal_position)
    into update_set
    from information_schema.columns s
    join information_schema.columns t
      on t.table_schema = 'public'
     and t.table_name = tgt
     and t.column_name = s.column_name
    where s.table_schema = 'public'
      and s.table_name = src
      and s.column_name not in ('id', 'notion_page_id');

    -- Update existing canonical rows using notion_page_id.
    if update_set is not null and update_set <> '' then
      execute format(
        'update public.%I as t
           set %s
          from public.%I as s
         where s.notion_page_id is not null
           and t.notion_page_id = s.notion_page_id',
        tgt,
        update_set,
        src
      );
      get diagnostics updated_rows = row_count;
    end if;

    -- Insert only rows that do not exist in canonical table yet.
    execute format(
      'insert into public.%I (%s)
       select %s
         from public.%I as s
        where s.notion_page_id is not null
          and not exists (
            select 1
              from public.%I as t
             where t.notion_page_id = s.notion_page_id
          )',
      tgt,
      insert_cols,
      insert_cols,
      src,
      tgt
    );
    get diagnostics inserted_rows = row_count;

    execute format(
      'select count(*) from public.%I where notion_page_id is null',
      src
    ) into skipped_null_notion_rows;
  else
    -- Fallback for tables without notion_page_id.
    execute format(
      'insert into public.%I (%s)
       select %s from public.%I',
      tgt,
      insert_cols,
      insert_cols,
      src
    );
    get diagnostics inserted_rows = row_count;
  end if;

  raise notice 'Migrated % -> % | updated: %, inserted: %, skipped_null_notion_page_id: %',
    src,
    tgt,
    updated_rows,
    inserted_rows,
    skipped_null_notion_rows;
end;
$$;
