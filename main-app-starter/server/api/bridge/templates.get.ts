/**
 * Proxy to CursorBridge: GET /api/templates
 */
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const query = getQuery(event)
  
  const url = new URL('/api/templates', config.cursorBridgeApi)
  if (query.category) {
    url.searchParams.set('category', String(query.category))
  }
  
  return await $fetch(url.toString())
})

