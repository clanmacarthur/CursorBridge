-- Read-only preflight for stage -> canonical migration.
-- This does NOT change data.
-- Use this to decide if we should STOP before any write batch.

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
),
scan as (
  select
    stage_table,
    public.cb_safe_count(stage_table) as stage_rows,
    canonical_table,
    public.cb_safe_count(canonical_table) as canonical_rows
  from pairs
)
select
  stage_table,
  stage_rows,
  canonical_table,
  canonical_rows,
  case
    when canonical_rows = -1 then 'STOP_MAJOR_CHANGE_CANONICAL_MISSING'
    when canonical_rows < stage_rows then 'STOP_REVIEW_BEFORE_WRITE'
    else 'OK_FOR_CONTROLLED_WRITE'
  end as stop_condition
from scan
order by stage_table;

-- Global stop summary:
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
),
scan as (
  select
    stage_table,
    public.cb_safe_count(stage_table) as stage_rows,
    canonical_table,
    public.cb_safe_count(canonical_table) as canonical_rows
  from pairs
)
select
  case
    when exists (
      select 1 from scan
      where canonical_rows = -1
         or canonical_rows < stage_rows
    )
    then 'STOP_WRITE_BATCHES_FOR_NOW'
    else 'PRECHECK_OK_FOR_WRITE_BATCHES'
  end as global_decision;
