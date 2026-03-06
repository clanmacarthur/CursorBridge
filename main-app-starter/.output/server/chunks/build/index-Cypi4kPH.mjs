globalThis.__timing__.logStart('Load chunks/build/index-Cypi4kPH');import { _ as __nuxt_component_0 } from './nuxt-link-CdwPPLpY.mjs';
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
  _push(`<div${ssrRenderAttrs(mergeProps({ class: "landing" }, _attrs))} data-v-0b3d9a3d><div class="hero" data-v-0b3d9a3d><h1 data-v-0b3d9a3d>Your Personal<br data-v-0b3d9a3d><span class="accent" data-v-0b3d9a3d>Wellness Dashboard</span></h1><p class="subtitle" data-v-0b3d9a3d> Track your daily habits, generate guided sessions, and unlock insights about your wellbeing with our adaptive wellness engine. </p><div class="cta-buttons" data-v-0b3d9a3d>`);
  _push(ssrRenderComponent(_component_NuxtLink, {
    to: "/dashboard",
    class: "btn-primary btn-large"
  }, {
    default: withCtx((_, _push2, _parent2, _scopeId) => {
      if (_push2) {
        _push2(` Get Started `);
      } else {
        return [
          createTextVNode(" Get Started ")
        ];
      }
    }),
    _: 1
  }, _parent));
  _push(ssrRenderComponent(_component_NuxtLink, {
    to: "/session",
    class: "btn-secondary btn-large"
  }, {
    default: withCtx((_, _push2, _parent2, _scopeId) => {
      if (_push2) {
        _push2(` Try a Session `);
      } else {
        return [
          createTextVNode(" Try a Session ")
        ];
      }
    }),
    _: 1
  }, _parent));
  _push(`</div></div><div class="features" data-v-0b3d9a3d><div class="feature-card" data-v-0b3d9a3d><div class="feature-icon" data-v-0b3d9a3d>\u{1F39B}\uFE0F</div><h3 data-v-0b3d9a3d>Adaptive Controls</h3><p data-v-0b3d9a3d>Personalized sliders and check-ins that learn from your patterns</p></div><div class="feature-card" data-v-0b3d9a3d><div class="feature-icon" data-v-0b3d9a3d>\u{1F9D8}</div><h3 data-v-0b3d9a3d>Guided Sessions</h3><p data-v-0b3d9a3d>AI-generated breathwork, movement, and meditation sessions</p></div><div class="feature-card" data-v-0b3d9a3d><div class="feature-icon" data-v-0b3d9a3d>\u{1F4CA}</div><h3 data-v-0b3d9a3d>Smart Insights</h3><p data-v-0b3d9a3d>See how your habits influence each other with coupling rules</p></div></div></div>`);
}
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/index.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const index = /* @__PURE__ */ _export_sfc(_sfc_main, [["ssrRender", _sfc_ssrRender], ["__scopeId", "data-v-0b3d9a3d"]]);

export { index as default };;globalThis.__timing__.logEnd('Load chunks/build/index-Cypi4kPH');
//# sourceMappingURL=index-Cypi4kPH.mjs.map
