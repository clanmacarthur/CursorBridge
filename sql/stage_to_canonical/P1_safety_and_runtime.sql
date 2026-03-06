begin;

-- P1: safety-critical and session runtime support tables.
select public.cb_migrate_stage_table('during_session_stop_triggers_stage');
select public.cb_migrate_stage_table('contraindications_mandatory_disclosure_stage');
select public.cb_migrate_stage_table('breathwork_master_taxonomy_stage');
select public.cb_migrate_stage_table('daily_regulation_sliders_stage');
select public.cb_migrate_stage_table('controls_library_design_stage');

commit;
