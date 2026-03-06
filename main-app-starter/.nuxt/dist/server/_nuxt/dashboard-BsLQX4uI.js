import { defineComponent, mergeProps, useSSRContext, ref, computed, unref } from "vue";
import { ssrRenderAttrs, ssrInterpolate, ssrRenderAttr, ssrRenderList, ssrRenderComponent, ssrIncludeBooleanAttr } from "vue/server-renderer";
import { _ as _export_sfc, u as useSupabaseUser } from "../server.mjs";
import "C:/code/CursorBridge/main-app-starter/node_modules/hookable/dist/index.mjs";
import "C:/code/CursorBridge/main-app-starter/node_modules/ofetch/dist/node.mjs";
import "#internal/nuxt/paths";
import "C:/code/CursorBridge/main-app-starter/node_modules/unctx/dist/index.mjs";
import "C:/code/CursorBridge/main-app-starter/node_modules/h3/dist/index.mjs";
import "vue-router";
import "C:/code/CursorBridge/main-app-starter/node_modules/defu/dist/defu.mjs";
import "C:/code/CursorBridge/main-app-starter/node_modules/ufo/dist/index.mjs";
import "@supabase/ssr";
import "C:/code/CursorBridge/main-app-starter/node_modules/cookie-es/dist/index.mjs";
import "C:/code/CursorBridge/main-app-starter/node_modules/destr/dist/index.mjs";
import "C:/code/CursorBridge/main-app-starter/node_modules/nuxt/node_modules/ohash/dist/index.mjs";
import "C:/code/CursorBridge/main-app-starter/node_modules/klona/dist/index.mjs";
const _sfc_main$2 = /* @__PURE__ */ defineComponent({
  __name: "BlockSlider",
  __ssrInlineRender: true,
  props: {
    control: {},
    modelValue: {}
  },
  emits: ["update:modelValue"],
  setup(__props) {
    return (_ctx, _push, _parent, _attrs) => {
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "block-slider" }, _attrs))} data-v-fbb566ff><div class="slider-header" data-v-fbb566ff><label data-v-fbb566ff>${ssrInterpolate(__props.control.control_name)}</label><span class="value" data-v-fbb566ff>${ssrInterpolate(__props.modelValue)} ${ssrInterpolate(__props.control.unit)}</span></div><input type="range"${ssrRenderAttr("min", __props.control.range_min || 0)}${ssrRenderAttr("max", __props.control.range_max || 10)}${ssrRenderAttr("step", __props.control.range_step || 1)}${ssrRenderAttr("value", __props.modelValue)} data-v-fbb566ff><div class="range-labels" data-v-fbb566ff><span data-v-fbb566ff>${ssrInterpolate(__props.control.range_min || 0)}</span><span data-v-fbb566ff>${ssrInterpolate(__props.control.range_max || 10)}</span></div></div>`);
    };
  }
});
const _sfc_setup$2 = _sfc_main$2.setup;
_sfc_main$2.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("components/BlockSlider.vue");
  return _sfc_setup$2 ? _sfc_setup$2(props, ctx) : void 0;
};
const __nuxt_component_0 = /* @__PURE__ */ _export_sfc(_sfc_main$2, [["__scopeId", "data-v-fbb566ff"]]);
const _sfc_main$1 = /* @__PURE__ */ defineComponent({
  __name: "BlockCheckbox",
  __ssrInlineRender: true,
  props: {
    control: {},
    modelValue: { type: Boolean }
  },
  emits: ["update:modelValue"],
  setup(__props, { emit: __emit }) {
    return (_ctx, _push, _parent, _attrs) => {
      _push(`<div${ssrRenderAttrs(mergeProps({
        class: ["block-checkbox", { checked: __props.modelValue }]
      }, _attrs))} data-v-63f7659d><div class="checkbox-icon" data-v-63f7659d>`);
      if (__props.modelValue) {
        _push(`<span data-v-63f7659d>✓</span>`);
      } else {
        _push(`<!---->`);
      }
      _push(`</div><div class="checkbox-content" data-v-63f7659d><label data-v-63f7659d>${ssrInterpolate(__props.control.control_name)}</label>`);
      if (__props.control.description) {
        _push(`<p data-v-63f7659d>${ssrInterpolate(__props.control.description)}</p>`);
      } else {
        _push(`<!---->`);
      }
      _push(`</div></div>`);
    };
  }
});
const _sfc_setup$1 = _sfc_main$1.setup;
_sfc_main$1.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("components/BlockCheckbox.vue");
  return _sfc_setup$1 ? _sfc_setup$1(props, ctx) : void 0;
};
const __nuxt_component_1 = /* @__PURE__ */ _export_sfc(_sfc_main$1, [["__scopeId", "data-v-63f7659d"]]);
const _sfc_main = /* @__PURE__ */ defineComponent({
  __name: "dashboard",
  __ssrInlineRender: true,
  setup(__props) {
    const user = useSupabaseUser();
    const showTemplates = ref(false);
    const saving = ref(false);
    const checkinValues = ref({});
    const defaultControls = ref([]);
    const templates = ref([]);
    const userName = computed(() => user.value?.email?.split("@")[0] || "Friend");
    const greeting = computed(() => {
      const hour = (/* @__PURE__ */ new Date()).getHours();
      if (hour < 12) return "morning";
      if (hour < 17) return "afternoon";
      return "evening";
    });
    const formattedDate = computed(() => {
      return (/* @__PURE__ */ new Date()).toLocaleDateString("en-US", {
        weekday: "long",
        month: "long",
        day: "numeric"
      });
    });
    return (_ctx, _push, _parent, _attrs) => {
      const _component_BlockSlider = __nuxt_component_0;
      const _component_BlockCheckbox = __nuxt_component_1;
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "dashboard" }, _attrs))} data-v-cb074126><header class="dashboard-header" data-v-cb074126><div data-v-cb074126><h1 data-v-cb074126>Good ${ssrInterpolate(unref(greeting))}, ${ssrInterpolate(unref(userName))}</h1><p class="date" data-v-cb074126>${ssrInterpolate(unref(formattedDate))}</p></div><button class="btn-primary" data-v-cb074126> + Add Block </button></header><section class="checkin-section" data-v-cb074126><h2 data-v-cb074126>Daily Check-in</h2><div class="controls-grid" data-v-cb074126><!--[-->`);
      ssrRenderList(unref(defaultControls), (control) => {
        _push(`<div class="control-card" data-v-cb074126>`);
        if (control.control_type === "slider") {
          _push(ssrRenderComponent(_component_BlockSlider, {
            control,
            modelValue: unref(checkinValues)[control.id],
            "onUpdate:modelValue": ($event) => unref(checkinValues)[control.id] = $event
          }, null, _parent));
        } else if (control.control_type === "checkbox") {
          _push(ssrRenderComponent(_component_BlockCheckbox, {
            control,
            modelValue: unref(checkinValues)[control.id],
            "onUpdate:modelValue": ($event) => unref(checkinValues)[control.id] = $event
          }, null, _parent));
        } else {
          _push(`<!---->`);
        }
        _push(`</div>`);
      });
      _push(`<!--]--></div><button class="btn-primary"${ssrIncludeBooleanAttr(unref(saving)) ? " disabled" : ""} data-v-cb074126>${ssrInterpolate(unref(saving) ? "Saving..." : "Save Check-in")}</button></section>`);
      if (unref(showTemplates)) {
        _push(`<div class="modal-overlay" data-v-cb074126><div class="modal" data-v-cb074126><h2 data-v-cb074126>Add Dashboard Block</h2><div class="templates-grid" data-v-cb074126><!--[-->`);
        ssrRenderList(unref(templates), (template) => {
          _push(`<div class="template-card" data-v-cb074126><span class="template-icon" data-v-cb074126>${ssrInterpolate(template.icon)}</span><h3 data-v-cb074126>${ssrInterpolate(template.name)}</h3><p data-v-cb074126>${ssrInterpolate(template.description)}</p></div>`);
        });
        _push(`<!--]--></div><button class="btn-secondary" data-v-cb074126>Cancel</button></div></div>`);
      } else {
        _push(`<!---->`);
      }
      _push(`</div>`);
    };
  }
});
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/dashboard.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const dashboard = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-cb074126"]]);
export {
  dashboard as default
};
//# sourceMappingURL=dashboard-BsLQX4uI.js.map
