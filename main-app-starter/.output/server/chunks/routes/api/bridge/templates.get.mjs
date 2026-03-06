globalThis.__timing__.logStart('Load chunks/routes/api/bridge/templates.get');import { c as defineEventHandler, u as useRuntimeConfig, e as getQuery } from '../../../_/nitro.mjs';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:path';
import 'node:crypto';
import 'node:url';

const templates_get = defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const query = getQuery(event);
  const url = new URL("/api/templates", config.cursorBridgeApi);
  if (query.category) {
    url.searchParams.set("category", String(query.category));
  }
  return await $fetch(url.toString());
});

export { templates_get as default };;globalThis.__timing__.logEnd('Load chunks/routes/api/bridge/templates.get');
//# sourceMappingURL=templates.get.mjs.map
