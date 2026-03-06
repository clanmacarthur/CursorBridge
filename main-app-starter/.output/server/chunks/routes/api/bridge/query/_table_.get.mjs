globalThis.__timing__.logStart('Load chunks/routes/api/bridge/query/_table_.get');import { c as defineEventHandler, u as useRuntimeConfig, g as getRouterParam, e as getQuery } from '../../../../_/nitro.mjs';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:path';
import 'node:crypto';
import 'node:url';

const _table__get = defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const table = getRouterParam(event, "table");
  const query = getQuery(event);
  const url = new URL(`/api/query/${table}`, config.cursorBridgeApi);
  if (query.limit) {
    url.searchParams.set("limit", String(query.limit));
  }
  return await $fetch(url.toString());
});

export { _table__get as default };;globalThis.__timing__.logEnd('Load chunks/routes/api/bridge/query/_table_.get');
//# sourceMappingURL=_table_.get.mjs.map
