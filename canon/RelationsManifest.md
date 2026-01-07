# Relations Manifest

Generated: 2026-01-04T23:38:46Z
Source: Supabase PostgREST OpenAPI (introspected)

Format: from_table.from_col -> to_table.to_col | cardinality | direction | join_table

- control_pack_items.control_id -> control_definitions.id | many-to-one | one-way | -
- control_pack_items.pack_id -> control_packs.id | many-to-one | one-way | -
- coupling_rules.from_control_id -> control_definitions.id | many-to-one | one-way | -
- coupling_rules.to_control_id -> control_definitions.id | many-to-one | one-way | -
- persona_kb_compatibility.kb_id -> knowledge_bases.id | many-to-one | one-way | -
- persona_lens_compatibility.lens_id -> lens_definitions.id | many-to-one | one-way | -
- profile_pack_map.pack_id -> control_packs.id | many-to-one | one-way | -
- programme_knowledge_map.kb_id -> knowledge_bases.id | many-to-one | one-way | -
- questionnaire_questions.questionnaire_id -> questionnaires.id | many-to-one | one-way | -
- questionnaire_responses.questionnaire_id -> questionnaires.id | many-to-one | one-way | -
- session_outputs.session_run_id -> session_runs.id | many-to-one | one-way | -
- technique_lens_explanations.lens_id -> lens_definitions.id | many-to-one | one-way | -
- technique_lens_explanations.technique_id -> techniques.id | many-to-one | one-way | -
- user_knowledge_access.kb_id -> knowledge_bases.id | many-to-one | one-way | -
- user_lens_preferences.lens_id -> lens_definitions.id | many-to-one | one-way | -

## Derived many-to-many (via join tables)
- control_definitions.id -> control_packs.id | many-to-many | two-way | control_pack_items
