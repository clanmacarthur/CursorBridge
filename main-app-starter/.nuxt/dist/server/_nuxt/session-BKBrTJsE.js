import { defineComponent, ref, computed, mergeProps, unref, useSSRContext } from "vue";
import { ssrRenderAttrs, ssrInterpolate, ssrRenderStyle, ssrRenderClass, ssrRenderList, ssrRenderAttr, ssrIncludeBooleanAttr, ssrLooseContain, ssrLooseEqual, ssrRenderComponent } from "vue/server-renderer";
import "C:/code/CursorBridge/main-app-starter/node_modules/hookable/dist/index.mjs";
import { _ as _export_sfc, u as useSupabaseUser } from "../server.mjs";
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
const _sfc_main$1 = /* @__PURE__ */ defineComponent({
  __name: "SessionPlayer",
  __ssrInlineRender: true,
  props: {
    session: {}
  },
  emits: ["complete"],
  setup(__props) {
    const props = __props;
    const isPlaying = ref(false);
    const elapsedSeconds = ref(0);
    const currentSectionIndex = ref(0);
    const totalSeconds = computed(() => props.session.duration_minutes * 60);
    const progressPercent = computed(
      () => elapsedSeconds.value / totalSeconds.value * 100
    );
    const currentSection = computed(
      () => props.session.sections[currentSectionIndex.value]
    );
    function getSectionEndTime(index) {
      let time = 0;
      for (let i = 0; i <= index; i++) {
        time += props.session.sections[i].duration_minutes * 60;
      }
      return time;
    }
    function formatTime(seconds) {
      const m = Math.floor(seconds / 60);
      const s = seconds % 60;
      return `${m}:${s.toString().padStart(2, "0")}`;
    }
    function isCueActive(cue) {
      const match = cue.match(/^(\d+):(\d+)/);
      if (!match) return false;
      const cueMinutes = parseInt(match[1]);
      const cueSeconds = parseInt(match[2]);
      const cueTime = cueMinutes * 60 + cueSeconds;
      const sectionStart = currentSectionIndex.value > 0 ? getSectionEndTime(currentSectionIndex.value - 1) : 0;
      const sectionElapsed = elapsedSeconds.value - sectionStart;
      return sectionElapsed >= cueTime;
    }
    return (_ctx, _push, _parent, _attrs) => {
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "session-player" }, _attrs))} data-v-45f1cbac><div class="player-header" data-v-45f1cbac><h1 data-v-45f1cbac>${ssrInterpolate(__props.session.name)}</h1><p class="persona" data-v-45f1cbac>${ssrInterpolate(__props.session.persona_style)}</p></div><div class="progress-bar" data-v-45f1cbac><div class="progress-fill" style="${ssrRenderStyle({ width: unref(progressPercent) + "%" })}" data-v-45f1cbac></div></div><div class="time-display" data-v-45f1cbac><span data-v-45f1cbac>${ssrInterpolate(formatTime(unref(elapsedSeconds)))}</span><span data-v-45f1cbac>${ssrInterpolate(formatTime(unref(totalSeconds)))}</span></div><div class="current-section" data-v-45f1cbac><div class="${ssrRenderClass([unref(currentSection)?.type, "section-type"])}" data-v-45f1cbac>${ssrInterpolate(unref(currentSection)?.type)}</div><h2 data-v-45f1cbac>${ssrInterpolate(unref(currentSection)?.name)}</h2><p class="instructions" data-v-45f1cbac>${ssrInterpolate(unref(currentSection)?.instructions)}</p>`);
      if (unref(currentSection)?.cues) {
        _push(`<div class="cues" data-v-45f1cbac><!--[-->`);
        ssrRenderList(unref(currentSection).cues, (cue, i) => {
          _push(`<div class="${ssrRenderClass([{ active: isCueActive(cue) }, "cue"])}" data-v-45f1cbac>${ssrInterpolate(cue)}</div>`);
        });
        _push(`<!--]--></div>`);
      } else {
        _push(`<!---->`);
      }
      _push(`</div><div class="player-controls" data-v-45f1cbac><button class="play-button" data-v-45f1cbac>${ssrInterpolate(unref(isPlaying) ? "⏸" : "▶")}</button><button class="skip-button" data-v-45f1cbac> Skip → </button></div>`);
      if (__props.session.safety_warnings?.length) {
        _push(`<div class="safety-warnings" data-v-45f1cbac><h3 data-v-45f1cbac>Safety Notes</h3><ul data-v-45f1cbac><!--[-->`);
        ssrRenderList(__props.session.safety_warnings, (warning, i) => {
          _push(`<li data-v-45f1cbac>${ssrInterpolate(warning)}</li>`);
        });
        _push(`<!--]--></ul></div>`);
      } else {
        _push(`<!---->`);
      }
      _push(`<button class="btn-secondary close-button" data-v-45f1cbac> End Session </button></div>`);
    };
  }
});
const _sfc_setup$1 = _sfc_main$1.setup;
_sfc_main$1.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("components/SessionPlayer.vue");
  return _sfc_setup$1 ? _sfc_setup$1(props, ctx) : void 0;
};
const __nuxt_component_0 = /* @__PURE__ */ _export_sfc(_sfc_main$1, [["__scopeId", "data-v-45f1cbac"]]);
const _sfc_main = /* @__PURE__ */ defineComponent({
  __name: "session",
  __ssrInlineRender: true,
  setup(__props) {
    useSupabaseUser();
    const session2 = ref(null);
    const generating = ref(false);
    const duration = ref(15);
    const selectedProfile = ref("");
    const profiles = ref([]);
    return (_ctx, _push, _parent, _attrs) => {
      const _component_SessionPlayer = __nuxt_component_0;
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "session-page" }, _attrs))} data-v-2f180b6c>`);
      if (!unref(session2)) {
        _push(`<div class="session-setup" data-v-2f180b6c><h1 data-v-2f180b6c>Generate a Session</h1><p class="subtitle" data-v-2f180b6c>Choose your preferences and we&#39;ll create a personalized guided session.</p><div class="setup-form" data-v-2f180b6c><div class="form-group" data-v-2f180b6c><label data-v-2f180b6c>Duration</label><div class="duration-options" data-v-2f180b6c><!--[-->`);
        ssrRenderList([10, 15, 20, 30], (d) => {
          _push(`<button class="${ssrRenderClass({ active: unref(duration) === d })}" data-v-2f180b6c>${ssrInterpolate(d)} min </button>`);
        });
        _push(`<!--]--></div></div><div class="form-group" data-v-2f180b6c><label data-v-2f180b6c>Profile</label><select data-v-2f180b6c><!--[-->`);
        ssrRenderList(unref(profiles), (p) => {
          _push(`<option${ssrRenderAttr("value", p.id)} data-v-2f180b6c${ssrIncludeBooleanAttr(Array.isArray(unref(selectedProfile)) ? ssrLooseContain(unref(selectedProfile), p.id) : ssrLooseEqual(unref(selectedProfile), p.id)) ? " selected" : ""}>${ssrInterpolate(p.programme_profile___title)}</option>`);
        });
        _push(`<!--]--></select></div><button class="btn-primary btn-large"${ssrIncludeBooleanAttr(unref(generating)) ? " disabled" : ""} data-v-2f180b6c>${ssrInterpolate(unref(generating) ? "Generating..." : "Generate Session")}</button></div></div>`);
      } else {
        _push(`<div class="session-player" data-v-2f180b6c>`);
        _push(ssrRenderComponent(_component_SessionPlayer, {
          session: unref(session2),
          onComplete: ($event) => session2.value = null
        }, null, _parent));
        _push(`</div>`);
      }
      _push(`</div>`);
    };
  }
});
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/session.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const session = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-2f180b6c"]]);
export {
  session as default
};
//# sourceMappingURL=session-BKBrTJsE.js.map
