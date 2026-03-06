begin;

-- P3: symbolic and deep-reference tables.
select public.cb_migrate_stage_table('mythological_beings_stage');
select public.cb_migrate_stage_table('sacred_animals_stage');
select public.cb_migrate_stage_table('stones_minerals_stage');

commit;
