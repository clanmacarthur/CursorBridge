import { serverSupabaseClient } from '#supabase/server'
import { buildThemeGraphFromSupabase } from '~/domain/engine/themes'

export default defineEventHandler(async (event) => {
  try {
    const client = await serverSupabaseClient(event)
    const graph = await buildThemeGraphFromSupabase(client)

    return { graph }
  } catch (error: any) {
    setResponseStatus(event, 503)

    return {
      graph: {
        wheels: [],
        edges: [],
      },
      ok: false,
      code: 'THEME_GRAPH_UNAVAILABLE',
      message: 'Theme graph endpoint is wired, but data load failed in this environment.',
      route: '/api/session/themes',
      error: error?.message || 'unknown error',
      next_doc: 'docs/TASK_MANAGER_CURSORBRIDGE_ALIGNMENT.md',
    }
  }
})
