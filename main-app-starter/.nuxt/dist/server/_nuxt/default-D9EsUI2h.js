import { _ as __nuxt_component_0 } from "./nuxt-link-CdwPPLpY.js";
import { defineComponent, mergeProps, withCtx, createTextVNode, unref, useSSRContext } from "vue";
import { ssrRenderAttrs, ssrRenderComponent, ssrRenderSlot } from "vue/server-renderer";
import { u as useSupabaseUser, _ as _export_sfc } from "../server.mjs";
import { u as useSupabaseClient } from "./useSupabaseClient-H06rCZGb.js";
import "C:/code/CursorBridge/main-app-starter/node_modules/hookable/dist/index.mjs";
import "C:/code/CursorBridge/main-app-starter/node_modules/ufo/dist/index.mjs";
import "C:/code/CursorBridge/main-app-starter/node_modules/ofetch/dist/node.mjs";
import "#internal/nuxt/paths";
import "C:/code/CursorBridge/main-app-starter/node_modules/unctx/dist/index.mjs";
import "C:/code/CursorBridge/main-app-starter/node_modules/h3/dist/index.mjs";
import "vue-router";
import "C:/code/CursorBridge/main-app-starter/node_modules/defu/dist/defu.mjs";
import "@supabase/ssr";
import "C:/code/CursorBridge/main-app-starter/node_modules/cookie-es/dist/index.mjs";
import "C:/code/CursorBridge/main-app-starter/node_modules/destr/dist/index.mjs";
import "C:/code/CursorBridge/main-app-starter/node_modules/nuxt/node_modules/ohash/dist/index.mjs";
import "C:/code/CursorBridge/main-app-starter/node_modules/klona/dist/index.mjs";
const _sfc_main = /* @__PURE__ */ defineComponent({
  __name: "default",
  __ssrInlineRender: true,
  setup(__props) {
    const user = useSupabaseUser();
    useSupabaseClient();
    return (_ctx, _push, _parent, _attrs) => {
      const _component_NuxtLink = __nuxt_component_0;
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "app-layout" }, _attrs))} data-v-331eaddd><header class="app-header" data-v-331eaddd><div class="header-content" data-v-331eaddd>`);
      _push(ssrRenderComponent(_component_NuxtLink, {
        to: "/",
        class: "logo"
      }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`Wellness`);
          } else {
            return [
              createTextVNode("Wellness")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(`<nav class="nav-links" data-v-331eaddd>`);
      _push(ssrRenderComponent(_component_NuxtLink, { to: "/dashboard" }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`Dashboard`);
          } else {
            return [
              createTextVNode("Dashboard")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(ssrRenderComponent(_component_NuxtLink, { to: "/session" }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`Session`);
          } else {
            return [
              createTextVNode("Session")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(ssrRenderComponent(_component_NuxtLink, { to: "/sessions" }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`Sessions (Planned)`);
          } else {
            return [
              createTextVNode("Sessions (Planned)")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(`</nav><div class="user-menu" data-v-331eaddd>`);
      if (unref(user)) {
        _push(`<button class="btn-secondary" data-v-331eaddd> Sign Out </button>`);
      } else {
        _push(ssrRenderComponent(_component_NuxtLink, {
          to: "/login",
          class: "btn-primary"
        }, {
          default: withCtx((_, _push2, _parent2, _scopeId) => {
            if (_push2) {
              _push2(` Sign In `);
            } else {
              return [
                createTextVNode(" Sign In ")
              ];
            }
          }),
          _: 1
        }, _parent));
      }
      _push(`</div></div></header><main class="app-main" data-v-331eaddd>`);
      ssrRenderSlot(_ctx.$slots, "default", {}, null, _push, _parent);
      _push(`</main></div>`);
    };
  }
});
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("layouts/default.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const _default = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-331eaddd"]]);
export {
  _default as default
};
//# sourceMappingURL=default-D9EsUI2h.js.map
