/**
 * Planned contract endpoint.
 * Current implementation is a placeholder so clients can integrate safely.
 */
export default defineEventHandler(async (event) => {
  const body = await readBody(event)
  const plannerConfig = body?.planner_config || body?.plannerConfig || null
  const dialSelection = body?.dial_selection || body?.dialSelection || null
  const themeSelection = body?.theme_selection || body?.themeSelection || null
  const templateId = body?.template_id || body?.blueprint_id || null
  const durationMinutes =
    body?.duration_minutes ??
    body?.duration_override_min ??
    plannerConfig?.duration_minutes ??
    null

  setResponseStatus(event, 501)

  return {
    session_run_id: null,
    session_output_id: null,
    output_data: {
      template_id: templateId,
      duration_minutes: durationMinutes,
      phases: [],
      dial_selection: dialSelection,
      theme_selection: themeSelection,
      dial_context: {},
      theme_context: {},
      safety: {
        rules_applied: [],
        warnings: [],
      },
    },
    narration_text: '',
    using_service_role: false,
    persisted: false,
    ok: false,
    code: 'NOT_IMPLEMENTED',
    message: 'Session generate contract is available, but persistence/planning logic is not implemented here yet.',
    route: '/api/session/generate',
    received_keys: body && typeof body === 'object' ? Object.keys(body) : [],
    next_doc: 'docs/TASK_MANAGER_CURSORBRIDGE_ALIGNMENT.md',
  }
})
