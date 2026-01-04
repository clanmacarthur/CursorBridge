/**
 * Proxy to CursorBridge: GET /api/templates/{id}
 */
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const id = getRouterParam(event, 'id')
  
  return await $fetch(`${config.cursorBridgeApi}/api/templates/${id}`)
})






