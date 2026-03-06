globalThis.__timing__.logStart('Load chunks/routes/api/session/composer-payload.get');import { c as defineEventHandler, f as setResponseStatus } from '../../../_/nitro.mjs';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:crypto';
import 'node:url';

const payloadPathCandidates = () => {
  const cwd = process.cwd();
  return [
    resolve(cwd, "docs", "SESSIONS_UI_PAYLOAD_2026-03-05.json"),
    resolve(cwd, "..", "docs", "SESSIONS_UI_PAYLOAD_2026-03-05.json")
  ];
};
const loadPayloadFile = async () => {
  const candidates = payloadPathCandidates();
  let lastError = null;
  for (const filePath of candidates) {
    try {
      const raw = await readFile(filePath, "utf-8");
      return { payload: JSON.parse(raw), filePath };
    } catch (error) {
      lastError = error;
    }
  }
  throw lastError || new Error("payload file not found");
};
const composerPayload_get = defineEventHandler(async (event) => {
  try {
    const { payload, filePath } = await loadPayloadFile();
    return {
      ok: true,
      route: "/api/session/composer-payload",
      source_file: filePath,
      payload
    };
  } catch (error) {
    setResponseStatus(event, 500);
    return {
      ok: false,
      route: "/api/session/composer-payload",
      code: "COMPOSER_PAYLOAD_LOAD_FAILED",
      message: (error == null ? void 0 : error.message) || "failed to load payload"
    };
  }
});

export { composerPayload_get as default };;globalThis.__timing__.logEnd('Load chunks/routes/api/session/composer-payload.get');
//# sourceMappingURL=composer-payload.get.mjs.map
