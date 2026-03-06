-- Verification: stage vs canonical row counts.
-- Run after P1/P2/P3.

create or replace function public.cb_safe_count(table_name text)
returns bigint
language plpgsql
as $$
declare
  c bigint;
begin
  if to_regclass(format('public.%I', table_name)) is null then
    return -1;
  end if;

  execute format('select count(*) from public.%I', table_name) into c;
  return c;
end;
$$;

with pairs(stage_table, canonical_table) as (
  values
    ('during_session_stop_triggers_stage', 'during_session_stop_triggers'),
    ('contraindications_mandatory_disclosure_stage', 'contraindications_mandatory_disclosure'),
    ('breathwork_master_taxonomy_stage', 'breathwork_master_taxonomy'),
    ('daily_regulation_sliders_stage', 'daily_regulation_sliders'),
    ('controls_library_design_stage', 'controls_library_design'),
    ('nadi_system_stage', 'nadi_system'),
    ('astrology_calendrical_systems_stage', 'astrology_calendrical_systems'),
    ('emotion_brain_body_energy_mapping_stage', 'emotion_brain_body_energy_mapping'),
    ('full_brain_neural_systems_table_stage', 'full_brain_neural_systems_table'),
    ('mythological_beings_stage', 'mythological_beings'),
    ('sacred_animals_stage', 'sacred_animals'),
    ('stones_minerals_stage', 'stones_minerals')
)
select
  stage_table,
  public.cb_safe_count(stage_table) as stage_rows,
  canonical_table,
  public.cb_safe_count(canonical_table) as canonical_rows,
  case
    when public.cb_safe_count(canonical_table) = -1 then 'missing_canonical_table'
    when public.cb_safe_count(canonical_table) < public.cb_safe_count(stage_table) then 'canonical_has_fewer_rows'
    else 'ok_or_superset'
  end as status
from pairs
order by stage_table;

-- Optional cleanup after verification:
-- drop function if exists public.cb_safe_count(text);
