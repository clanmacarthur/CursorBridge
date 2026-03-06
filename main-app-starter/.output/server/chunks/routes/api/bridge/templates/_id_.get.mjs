globalThis.__timing__.logStart('Load chunks/routes/api/bridge/templates/_id_.get');import { c as defineEventHandler, u as useRuntimeConfig, g as getRouterParam } from '../../../../_/nitro.mjs';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:path';
import 'node:crypto';
import 'node:url';

const _id__get = defineEventHandler(async (event) => {
  const config = useRuntimeConfig();
  const id = getRouterParam(event, "id");
  return await $fetch(`${config.cursorBridgeApi}/api/templates/${id}`);
});

export { _id__get as default };;globalThis.__timing__.logEnd('Load chunks/routes/api/bridge/templates/_id_.get');
//# sourceMappingURL=_id_.get.mjs.map
