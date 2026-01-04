/**
 * Proxy to CursorBridge: GET /api/query/{table}
 */
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const table = getRouterParam(event, 'table')
  const query = getQuery(event)
  
  const url = new URL(`/api/query/${table}`, config.cursorBridgeApi)
  if (query.limit) {
    url.searchParams.set('limit', String(query.limit))
  }
  
  return await $fetch(url.toString())
})




