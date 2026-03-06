import { readFile } from 'node:fs/promises'
import { resolve } from 'node:path'

const payloadPathCandidates = () => {
  const cwd = process.cwd()
  return [
    resolve(cwd, 'docs', 'SESSIONS_UI_PAYLOAD_2026-03-05.json'),
    resolve(cwd, '..', 'docs', 'SESSIONS_UI_PAYLOAD_2026-03-05.json'),
  ]
}

const loadPayloadFile = async () => {
  const candidates = payloadPathCandidates()
  let lastError: unknown = null

  for (const filePath of candidates) {
    try {
      const raw = await readFile(filePath, 'utf-8')
      return { payload: JSON.parse(raw), filePath }
    } catch (error) {
      lastError = error
    }
  }

  throw lastError || new Error('payload file not found')
}

export default defineEventHandler(async (event) => {
  try {
    const { payload, filePath } = await loadPayloadFile()
    return {
      ok: true,
      route: '/api/session/composer-payload',
      source_file: filePath,
      payload,
    }
  } catch (error: any) {
    setResponseStatus(event, 500)
    return {
      ok: false,
      route: '/api/session/composer-payload',
      code: 'COMPOSER_PAYLOAD_LOAD_FAILED',
      message: error?.message || 'failed to load payload',
    }
  }
})
