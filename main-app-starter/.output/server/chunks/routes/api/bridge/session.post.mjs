globalThis.__timing__.logStart('Load chunks/routes/api/bridge/session.post');import { c as defineEventHandler, u as useRuntimeConfig, r as readBody } from '../../../_/nitro.mjs';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:path';
import 'node:crypto';
import 'node:url';

const session_post = defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const body = await readBody(event);
  return await $fetch(`${config.cursorBridgeSandbox}/sandbox/generate-session`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body
  });
});

export { session_post as default };;globalThis.__timing__.logEnd('Load chunks/routes/api/bridge/session.post');
//# sourceMappingURL=session.post.mjs.map
