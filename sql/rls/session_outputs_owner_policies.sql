-- Sessions Composer RLS patch (smallest safe change)
-- Scope: public.session_outputs only
-- Goal: allow authenticated users to INSERT/SELECT only their own output rows.

-- 1) Inspect current policies (read-only)
select
  schemaname,
  tablename,
  policyname,
  permissive,
  roles,
  cmd,
  qual,
  with_check
from pg_policies
where schemaname = 'public'
  and tablename in ('session_runs', 'session_outputs')
order by tablename, policyname;

-- 2) Confirm ownership column exists on session_runs (read-only)
select
  table_schema,
  table_name,
  column_name,
  data_type
from information_schema.columns
where table_schema = 'public'
  and table_name = 'session_runs'
  and column_name = 'user_id';

-- 3) Apply smallest safe policy patch for session_outputs
alter table public.session_outputs enable row level security;

drop policy if exists session_outputs_insert_own_run on public.session_outputs;
create policy session_outputs_insert_own_run
on public.session_outputs
for insert
to authenticated
with check (
  exists (
    select 1
    from public.session_runs sr
    where sr.id = session_outputs.session_run_id
      and sr.user_id = auth.uid()
  )
);

drop policy if exists session_outputs_select_own_run on public.session_outputs;
create policy session_outputs_select_own_run
on public.session_outputs
for select
to authenticated
using (
  exists (
    select 1
    from public.session_runs sr
    where sr.id = session_outputs.session_run_id
      and sr.user_id = auth.uid()
  )
);

-- 4) Verify updated policies (read-only)
select
  schemaname,
  tablename,
  policyname,
  cmd,
  qual,
  with_check
from pg_policies
where schemaname = 'public'
  and tablename = 'session_outputs'
order by policyname;
