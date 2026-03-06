globalThis.__timing__.logStart('Load chunks/build/sessions-DVIe3zP1');import { _ as __nuxt_component_0 } from './nuxt-link-CdwPPLpY.mjs';
import { mergeProps, withCtx, createTextVNode, useSSRContext } from 'vue';
import { ssrRenderAttrs, ssrRenderComponent } from 'vue/server-renderer';
import { _ as _export_sfc } from './server.mjs';
import '../_/nitro.mjs';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:path';
import 'node:crypto';
import 'node:url';
import '../routes/renderer.mjs';
import 'vue-bundle-renderer/runtime';
import 'unhead/server';
import 'devalue';
import 'unhead/utils';
import 'unhead/plugins';
import 'vue-router';
import '@supabase/ssr';

const _sfc_main = {};
function _sfc_ssrRender(_ctx, _push, _parent, _attrs) {
  const _component_NuxtLink = __nuxt_component_0;
  _push(`<div${ssrRenderAttrs(mergeProps({ class: "sessions-page" }, _attrs))} data-v-b1af8304><div class="card" data-v-b1af8304><h1 data-v-b1af8304>Sessions Builder (Planned)</h1><p data-v-b1af8304> This page is the planned home for the wheel-based builder. </p><p data-v-b1af8304> The live generation flow is still on <code data-v-b1af8304>/session</code>. </p><h2 data-v-b1af8304>Planned API Contract</h2><ul data-v-b1af8304><li data-v-b1af8304><code data-v-b1af8304>GET /api/session/themes</code></li><li data-v-b1af8304><code data-v-b1af8304>POST /api/session/preview</code></li><li data-v-b1af8304><code data-v-b1af8304>POST /api/session/generate</code></li></ul><p data-v-b1af8304> See <code data-v-b1af8304>docs/HANDOVER_SESSIONS.md</code> for current-vs-target details. </p>`);
  _push(ssrRenderComponent(_component_NuxtLink, {
    to: "/session",
    class: "go-live"
  }, {
    default: withCtx((_, _push2, _parent2, _scopeId) => {
      if (_push2) {
        _push2(`Go to live session page`);
      } else {
        return [
          createTextVNode("Go to live session page")
        ];
      }
    }),
    _: 1
  }, _parent));
  _push(`</div></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/sessions.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const sessions = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender], ["__scopeId", "data-v-b1af8304"]]);

export { sessions as default };;globalThis.__timing__.logEnd('Load chunks/build/sessions-DVIe3zP1');
//# sourceMappingURL=sessions-DVIe3zP1.mjs.map
