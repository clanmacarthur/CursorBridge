import { _ as __nuxt_component_0 } from "./nuxt-link-CdwPPLpY.js";
import { defineComponent, ref, mergeProps, unref, withCtx, createTextVNode, useSSRContext } from "vue";
import { ssrRenderAttrs, ssrRenderAttr, ssrIncludeBooleanAttr, ssrInterpolate, ssrRenderComponent } from "vue/server-renderer";
import { u as useSupabaseClient } from "./useSupabaseClient-H06rCZGb.js";
import "C:/code/CursorBridge/main-app-starter/node_modules/hookable/dist/index.mjs";
import { _ as _export_sfc } from "../server.mjs";
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
  __name: "login",
  __ssrInlineRender: true,
  setup(__props) {
    useSupabaseClient();
    const email = ref("");
    const password = ref("");
    const loading = ref(false);
    const error = ref("");
    return (_ctx, _push, _parent, _attrs) => {
      const _component_NuxtLink = __nuxt_component_0;
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "login-page" }, _attrs))} data-v-90138887><div class="login-card" data-v-90138887><h1 data-v-90138887>Welcome Back</h1><p class="subtitle" data-v-90138887>Sign in to your wellness dashboard</p><form class="login-form" data-v-90138887><div class="form-group" data-v-90138887><label for="email" data-v-90138887>Email</label><input id="email"${ssrRenderAttr("value", unref(email))} type="email" placeholder="you@example.com" required data-v-90138887></div><div class="form-group" data-v-90138887><label for="password" data-v-90138887>Password</label><input id="password"${ssrRenderAttr("value", unref(password))} type="password" placeholder="••••••••" required data-v-90138887></div><button type="submit" class="btn-primary btn-full"${ssrIncludeBooleanAttr(unref(loading)) ? " disabled" : ""} data-v-90138887>${ssrInterpolate(unref(loading) ? "Signing in..." : "Sign In")}</button>`);
      if (unref(error)) {
        _push(`<p class="error" data-v-90138887>${ssrInterpolate(unref(error))}</p>`);
      } else {
        _push(`<!---->`);
      }
      _push(`</form><div class="divider" data-v-90138887><span data-v-90138887>or continue with</span></div><button class="btn-social" data-v-90138887><span data-v-90138887>🔵</span> Google </button><p class="signup-link" data-v-90138887> Don&#39;t have an account? `);
      _push(ssrRenderComponent(_component_NuxtLink, { to: "/register" }, {
        default: withCtx((_, _push2, _parent2, _scopeId) => {
          if (_push2) {
            _push2(`Sign up`);
          } else {
            return [
              createTextVNode("Sign up")
            ];
          }
        }),
        _: 1
      }, _parent));
      _push(`</p></div></div>`);
    };
  }
});
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/login.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const login = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-90138887"]]);
export {
  login as default
};
//# sourceMappingURL=login-D-uqV1t7.js.map
