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
    persisted: false,
    using_service_role: false,
    ruleset_id: 'cursorbridge-main-app-stub',
    ruleset_version: 'v0',
    ok: false,
    code: 'NOT_IMPLEMENTED',
    message: 'Session preview contract is available, but generation logic is not implemented here yet.',
    route: '/api/session/preview',
    received_keys: body && typeof body === 'object' ? Object.keys(body) : [],
    next_doc: 'docs/TASK_MANAGER_CURSORBRIDGE_ALIGNMENT.md',
  }
})
