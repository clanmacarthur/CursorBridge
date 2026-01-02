/**
 * Proxy to CursorBridge Sandbox: POST /sandbox/generate-session
 */
export default defineEventHandler(async (event) => {
  const config = useRuntimeConfig()
  const body = await readBody(event)
  
  return await $fetch(`${config.cursorBridgeSandbox}/sandbox/generate-session`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body
  })
})

