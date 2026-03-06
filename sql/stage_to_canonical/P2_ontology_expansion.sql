begin;

-- P2: ontology expansion tables.
select public.cb_migrate_stage_table('nadi_system_stage');
select public.cb_migrate_stage_table('astrology_calendrical_systems_stage');
select public.cb_migrate_stage_table('emotion_brain_body_energy_mapping_stage');
select public.cb_migrate_stage_table('full_brain_neural_systems_table_stage');

commit;
