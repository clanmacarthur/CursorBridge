import { defineComponent, createElementBlock, shallowRef, getCurrentInstance, provide, cloneVNode, h, computed, toValue, onServerPrefetch, ref, nextTick, unref, toRef, reactive, watch, withAsyncContext, mergeProps, useSSRContext } from "vue";
import { ssrRenderAttrs, ssrRenderList, ssrRenderClass, ssrInterpolate, ssrRenderAttr, ssrIncludeBooleanAttr, ssrLooseContain, ssrLooseEqual } from "vue/server-renderer";
import { hash } from "C:/code/CursorBridge/main-app-starter/node_modules/nuxt/node_modules/ohash/dist/index.mjs";
import { isPlainObject } from "@vue/shared";
import { a as useNuxtApp, b as asyncDataDefaults, c as createError, f as fetchDefaults, d as useRequestFetch, e as useRoute, _ as _export_sfc } from "../server.mjs";
import { debounce } from "C:/code/CursorBridge/main-app-starter/node_modules/nuxt/node_modules/perfect-debounce/dist/index.mjs";
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
import "C:/code/CursorBridge/main-app-starter/node_modules/klona/dist/index.mjs";
defineComponent({
  name: "ServerPlaceholder",
  render() {
    return createElementBlock("div");
  }
});
const clientOnlySymbol = /* @__PURE__ */ Symbol.for("nuxt:client-only");
defineComponent({
  name: "ClientOnly",
  inheritAttrs: false,
  props: ["fallback", "placeholder", "placeholderTag", "fallbackTag"],
  ...false,
  setup(props, { slots, attrs }) {
    const mounted = shallowRef(false);
    const vm = getCurrentInstance();
    if (vm) {
      vm._nuxtClientOnly = true;
    }
    provide(clientOnlySymbol, true);
    return () => {
      if (mounted.value) {
        const vnodes = slots.default?.();
        if (vnodes && vnodes.length === 1) {
          return [cloneVNode(vnodes[0], attrs)];
        }
        return vnodes;
      }
      const slot = slots.fallback || slots.placeholder;
      if (slot) {
        return h(slot);
      }
      const fallbackStr = props.fallback || props.placeholder || "";
      const fallbackTag = props.fallbackTag || props.placeholderTag || "span";
      return createElementBlock(fallbackTag, attrs, fallbackStr);
    };
  }
});
const isDefer = (dedupe) => dedupe === "defer" || dedupe === false;
function useAsyncData(...args) {
  const autoKey = typeof args[args.length - 1] === "string" ? args.pop() : void 0;
  if (_isAutoKeyNeeded(args[0], args[1])) {
    args.unshift(autoKey);
  }
  let [_key, _handler, options = {}] = args;
  const key = computed(() => toValue(_key));
  if (typeof key.value !== "string") {
    throw new TypeError("[nuxt] [useAsyncData] key must be a string.");
  }
  if (typeof _handler !== "function") {
    throw new TypeError("[nuxt] [useAsyncData] handler must be a function.");
  }
  const nuxtApp = useNuxtApp();
  options.server ??= true;
  options.default ??= getDefault;
  options.getCachedData ??= getDefaultCachedData;
  options.lazy ??= false;
  options.immediate ??= true;
  options.deep ??= asyncDataDefaults.deep;
  options.dedupe ??= "cancel";
  options._functionName || "useAsyncData";
  nuxtApp._asyncData[key.value];
  function createInitialFetch() {
    const initialFetchOptions = { cause: "initial", dedupe: options.dedupe };
    if (!nuxtApp._asyncData[key.value]?._init) {
      initialFetchOptions.cachedData = options.getCachedData(key.value, nuxtApp, { cause: "initial" });
      nuxtApp._asyncData[key.value] = createAsyncData(nuxtApp, key.value, _handler, options, initialFetchOptions.cachedData);
    }
    return () => nuxtApp._asyncData[key.value].execute(initialFetchOptions);
  }
  const initialFetch = createInitialFetch();
  const asyncData = nuxtApp._asyncData[key.value];
  asyncData._deps++;
  const fetchOnServer = options.server !== false && nuxtApp.payload.serverRendered;
  if (fetchOnServer && options.immediate) {
    const promise = initialFetch();
    if (getCurrentInstance()) {
      onServerPrefetch(() => promise);
    } else {
      nuxtApp.hook("app:created", async () => {
        await promise;
      });
    }
  }
  const asyncReturn = {
    data: writableComputedRef(() => nuxtApp._asyncData[key.value]?.data),
    pending: writableComputedRef(() => nuxtApp._asyncData[key.value]?.pending),
    status: writableComputedRef(() => nuxtApp._asyncData[key.value]?.status),
    error: writableComputedRef(() => nuxtApp._asyncData[key.value]?.error),
    refresh: (...args2) => {
      if (!nuxtApp._asyncData[key.value]?._init) {
        const initialFetch2 = createInitialFetch();
        return initialFetch2();
      }
      return nuxtApp._asyncData[key.value].execute(...args2);
    },
    execute: (...args2) => asyncReturn.refresh(...args2),
    clear: () => {
      const entry = nuxtApp._asyncData[key.value];
      if (entry?._abortController) {
        try {
          entry._abortController.abort(new DOMException("AsyncData aborted by user.", "AbortError"));
        } finally {
          entry._abortController = void 0;
        }
      }
      clearNuxtDataByKey(nuxtApp, key.value);
    }
  };
  const asyncDataPromise = Promise.resolve(nuxtApp._asyncDataPromises[key.value]).then(() => asyncReturn);
  Object.assign(asyncDataPromise, asyncReturn);
  return asyncDataPromise;
}
function writableComputedRef(getter) {
  return computed({
    get() {
      return getter()?.value;
    },
    set(value) {
      const ref2 = getter();
      if (ref2) {
        ref2.value = value;
      }
    }
  });
}
function _isAutoKeyNeeded(keyOrFetcher, fetcher) {
  if (typeof keyOrFetcher === "string") {
    return false;
  }
  if (typeof keyOrFetcher === "object" && keyOrFetcher !== null) {
    return false;
  }
  if (typeof keyOrFetcher === "function" && typeof fetcher === "function") {
    return false;
  }
  return true;
}
function clearNuxtDataByKey(nuxtApp, key) {
  if (key in nuxtApp.payload.data) {
    nuxtApp.payload.data[key] = void 0;
  }
  if (key in nuxtApp.payload._errors) {
    nuxtApp.payload._errors[key] = asyncDataDefaults.errorValue;
  }
  if (nuxtApp._asyncData[key]) {
    nuxtApp._asyncData[key].data.value = void 0;
    nuxtApp._asyncData[key].error.value = asyncDataDefaults.errorValue;
    {
      nuxtApp._asyncData[key].pending.value = false;
    }
    nuxtApp._asyncData[key].status.value = "idle";
  }
  if (key in nuxtApp._asyncDataPromises) {
    nuxtApp._asyncDataPromises[key] = void 0;
  }
}
function pick(obj, keys) {
  const newObj = {};
  for (const key of keys) {
    newObj[key] = obj[key];
  }
  return newObj;
}
function createAsyncData(nuxtApp, key, _handler, options, initialCachedData) {
  nuxtApp.payload._errors[key] ??= asyncDataDefaults.errorValue;
  const hasCustomGetCachedData = options.getCachedData !== getDefaultCachedData;
  const handler = !import.meta.prerender || !nuxtApp.ssrContext?.["~sharedPrerenderCache"] ? _handler : (nuxtApp2, options2) => {
    const value = nuxtApp2.ssrContext["~sharedPrerenderCache"].get(key);
    if (value) {
      return value;
    }
    const promise = Promise.resolve().then(() => nuxtApp2.runWithContext(() => _handler(nuxtApp2, options2)));
    nuxtApp2.ssrContext["~sharedPrerenderCache"].set(key, promise);
    return promise;
  };
  const _ref = options.deep ? ref : shallowRef;
  const hasCachedData = initialCachedData != null;
  const unsubRefreshAsyncData = nuxtApp.hook("app:data:refresh", async (keys) => {
    if (!keys || keys.includes(key)) {
      await asyncData.execute({ cause: "refresh:hook" });
    }
  });
  const asyncData = {
    data: _ref(hasCachedData ? initialCachedData : options.default()),
    pending: shallowRef(!hasCachedData),
    error: toRef(nuxtApp.payload._errors, key),
    status: shallowRef("idle"),
    execute: (...args) => {
      const [_opts, newValue = void 0] = args;
      const opts = _opts && newValue === void 0 && typeof _opts === "object" ? _opts : {};
      if (nuxtApp._asyncDataPromises[key]) {
        if (isDefer(opts.dedupe ?? options.dedupe)) {
          return nuxtApp._asyncDataPromises[key];
        }
      }
      if (opts.cause === "initial" || nuxtApp.isHydrating) {
        const cachedData = "cachedData" in opts ? opts.cachedData : options.getCachedData(key, nuxtApp, { cause: opts.cause ?? "refresh:manual" });
        if (cachedData != null) {
          nuxtApp.payload.data[key] = asyncData.data.value = cachedData;
          asyncData.error.value = asyncDataDefaults.errorValue;
          asyncData.status.value = "success";
          return Promise.resolve(cachedData);
        }
      }
      {
        asyncData.pending.value = true;
      }
      if (asyncData._abortController) {
        asyncData._abortController.abort(new DOMException("AsyncData request cancelled by deduplication", "AbortError"));
      }
      asyncData._abortController = new AbortController();
      asyncData.status.value = "pending";
      const cleanupController = new AbortController();
      const promise = new Promise(
        (resolve, reject) => {
          try {
            const timeout = opts.timeout ?? options.timeout;
            const mergedSignal = mergeAbortSignals([asyncData._abortController?.signal, opts?.signal], cleanupController.signal, timeout);
            if (mergedSignal.aborted) {
              const reason = mergedSignal.reason;
              reject(reason instanceof Error ? reason : new DOMException(String(reason ?? "Aborted"), "AbortError"));
              return;
            }
            mergedSignal.addEventListener("abort", () => {
              const reason = mergedSignal.reason;
              reject(reason instanceof Error ? reason : new DOMException(String(reason ?? "Aborted"), "AbortError"));
            }, { once: true, signal: cleanupController.signal });
            return Promise.resolve(handler(nuxtApp, { signal: mergedSignal })).then(resolve, reject);
          } catch (err) {
            reject(err);
          }
        }
      ).then(async (_result) => {
        let result = _result;
        if (options.transform) {
          result = await options.transform(_result);
        }
        if (options.pick) {
          result = pick(result, options.pick);
        }
        nuxtApp.payload.data[key] = result;
        asyncData.data.value = result;
        asyncData.error.value = asyncDataDefaults.errorValue;
        asyncData.status.value = "success";
      }).catch((error) => {
        if (nuxtApp._asyncDataPromises[key] && nuxtApp._asyncDataPromises[key] !== promise) {
          return nuxtApp._asyncDataPromises[key];
        }
        if (asyncData._abortController?.signal.aborted) {
          return nuxtApp._asyncDataPromises[key];
        }
        if (typeof DOMException !== "undefined" && error instanceof DOMException && error.name === "AbortError") {
          asyncData.status.value = "idle";
          return nuxtApp._asyncDataPromises[key];
        }
        asyncData.error.value = createError(error);
        asyncData.data.value = unref(options.default());
        asyncData.status.value = "error";
      }).finally(() => {
        {
          asyncData.pending.value = false;
        }
        cleanupController.abort();
        delete nuxtApp._asyncDataPromises[key];
      });
      nuxtApp._asyncDataPromises[key] = promise;
      return nuxtApp._asyncDataPromises[key];
    },
    _execute: debounce((...args) => asyncData.execute(...args), 0, { leading: true }),
    _default: options.default,
    _deps: 0,
    _init: true,
    _hash: void 0,
    _off: () => {
      unsubRefreshAsyncData();
      if (nuxtApp._asyncData[key]?._init) {
        nuxtApp._asyncData[key]._init = false;
      }
      if (!hasCustomGetCachedData) {
        nextTick(() => {
          if (!nuxtApp._asyncData[key]?._init) {
            clearNuxtDataByKey(nuxtApp, key);
            asyncData.execute = () => Promise.resolve();
            asyncData.data.value = asyncDataDefaults.value;
          }
        });
      }
    }
  };
  return asyncData;
}
const getDefault = () => asyncDataDefaults.value;
const getDefaultCachedData = (key, nuxtApp, ctx) => {
  if (nuxtApp.isHydrating) {
    return nuxtApp.payload.data[key];
  }
  if (ctx.cause !== "refresh:manual" && ctx.cause !== "refresh:hook") {
    return nuxtApp.static.data[key];
  }
};
function mergeAbortSignals(signals, cleanupSignal, timeout) {
  const list = signals.filter((s) => !!s);
  if (typeof timeout === "number" && timeout >= 0) {
    const timeoutSignal = AbortSignal.timeout?.(timeout);
    if (timeoutSignal) {
      list.push(timeoutSignal);
    }
  }
  if (AbortSignal.any) {
    return AbortSignal.any(list);
  }
  const controller = new AbortController();
  for (const sig of list) {
    if (sig.aborted) {
      const reason = sig.reason ?? new DOMException("Aborted", "AbortError");
      try {
        controller.abort(reason);
      } catch {
        controller.abort();
      }
      return controller.signal;
    }
  }
  const onAbort = () => {
    const abortedSignal = list.find((s) => s.aborted);
    const reason = abortedSignal?.reason ?? new DOMException("Aborted", "AbortError");
    try {
      controller.abort(reason);
    } catch {
      controller.abort();
    }
  };
  for (const sig of list) {
    sig.addEventListener?.("abort", onAbort, { once: true, signal: cleanupSignal });
  }
  return controller.signal;
}
function useFetch(request, arg1, arg2) {
  const [opts = {}, autoKey] = [{}, arg1];
  const _request = computed(() => toValue(request));
  const key = computed(() => toValue(opts.key) || "$f" + hash([autoKey, typeof _request.value === "string" ? _request.value : "", ...generateOptionSegments(opts)]));
  if (!opts.baseURL && typeof _request.value === "string" && (_request.value[0] === "/" && _request.value[1] === "/")) {
    throw new Error('[nuxt] [useFetch] the request URL must not start with "//".');
  }
  const {
    server,
    lazy,
    default: defaultFn,
    transform,
    pick: pick2,
    watch: watchSources,
    immediate,
    getCachedData,
    deep,
    dedupe,
    timeout,
    ...fetchOptions
  } = opts;
  const _fetchOptions = reactive({
    ...fetchDefaults,
    ...fetchOptions,
    cache: typeof opts.cache === "boolean" ? void 0 : opts.cache
  });
  const _asyncDataOptions = {
    server,
    lazy,
    default: defaultFn,
    transform,
    pick: pick2,
    immediate,
    getCachedData,
    deep,
    dedupe,
    timeout,
    watch: watchSources === false ? [] : [...watchSources || [], _fetchOptions]
  };
  if (!immediate) {
    let setImmediate = function() {
      _asyncDataOptions.immediate = true;
    };
    watch(key, setImmediate, { flush: "sync", once: true });
    watch([...watchSources || [], _fetchOptions], setImmediate, { flush: "sync", once: true });
  }
  const asyncData = useAsyncData(watchSources === false ? key.value : key, (_, { signal }) => {
    let _$fetch = opts.$fetch || globalThis.$fetch;
    if (!opts.$fetch) {
      const isLocalFetch = typeof _request.value === "string" && _request.value[0] === "/" && (!toValue(opts.baseURL) || toValue(opts.baseURL)[0] === "/");
      if (isLocalFetch) {
        _$fetch = useRequestFetch();
      }
    }
    return _$fetch(_request.value, { signal, ..._fetchOptions });
  }, _asyncDataOptions);
  return asyncData;
}
function generateOptionSegments(opts) {
  const segments = [
    toValue(opts.method)?.toUpperCase() || "GET",
    toValue(opts.baseURL)
  ];
  for (const _obj of [opts.query || opts.params]) {
    const obj = toValue(_obj);
    if (!obj) {
      continue;
    }
    const unwrapped = {};
    for (const [key, value] of Object.entries(obj)) {
      unwrapped[toValue(key)] = toValue(value);
    }
    segments.push(unwrapped);
  }
  if (opts.body) {
    const value = toValue(opts.body);
    if (!value) {
      segments.push(hash(value));
    } else if (value instanceof ArrayBuffer) {
      segments.push(hash(Object.fromEntries([...new Uint8Array(value).entries()].map(([k, v]) => [k, v.toString()]))));
    } else if (value instanceof FormData) {
      const obj = {};
      for (const entry of value.entries()) {
        const [key, val] = entry;
        obj[key] = val instanceof File ? val.name : val;
      }
      segments.push(hash(obj));
    } else if (isPlainObject(value)) {
      segments.push(hash(reactive(value)));
    } else {
      try {
        segments.push(hash(value));
      } catch {
        console.warn("[useFetch] Failed to hash body", value);
      }
    }
  }
  return segments;
}
const saveRoute = "/sessions-composer-prototype";
const _sfc_main = /* @__PURE__ */ defineComponent({
  __name: "sessions-composer-prototype",
  __ssrInlineRender: true,
  async setup(__props) {
    let __temp, __restore;
    const { data, pending } = ([__temp, __restore] = withAsyncContext(() => useFetch(
      "/api/session/composer-payload",
      "$2KGjUDS2r3"
      /* nuxt-injected */
    )), __temp = await __temp, __restore(), __temp);
    const route = useRoute();
    const loadError = computed(() => data.value?.ok ? "" : data.value?.message || "unknown error");
    const payload = computed(() => data.value?.payload || null);
    const subjects = computed(() => payload.value?.top_level_subjects || []);
    const domains = computed(() => payload.value?.domains || []);
    const selectedSubject = ref("");
    const selectedDomainTable = ref("");
    const drawerOpen = ref(true);
    const searchTerm = ref("");
    const activeFilters = ref({});
    const selectedRowId = ref("");
    const stack = ref([]);
    const saving = ref(false);
    const saveResult = ref(null);
    watch(
      subjects,
      (list) => {
        if (!selectedSubject.value && list.length) {
          selectedSubject.value = list[0];
        }
      },
      { immediate: true }
    );
    watch(
      domains,
      (list) => {
        if (!selectedDomainTable.value && list.length) {
          selectedDomainTable.value = list[0].table;
          drawerOpen.value = true;
        }
      },
      { immediate: true }
    );
    const currentDomain = computed(() => domains.value.find((d) => d.table === selectedDomainTable.value) || null);
    watch(currentDomain, (domain) => {
      searchTerm.value = "";
      selectedRowId.value = "";
      const nextFilters = {};
      if (domain) {
        for (const col of domain.visible_filter_columns) {
          nextFilters[col] = "";
        }
      }
      activeFilters.value = nextFilters;
    });
    const displayValue = (value) => {
      if (value === null || value === void 0) return "";
      if (typeof value === "string") return value;
      if (typeof value === "number" || typeof value === "boolean") return String(value);
      return JSON.stringify(value);
    };
    const normalize = (value) => displayValue(value).toLowerCase().trim();
    const rowKey = (row, index) => `${row.notion_page_id || row.id || row[currentDomain.value?.label_column || ""] || "row"}-${index}`;
    const makeStackItem = (domain, row) => {
      if (!domain || !row) return null;
      const label = displayValue(row[domain.label_column]);
      if (!label) return null;
      return {
        id: `${Date.now()}-${Math.random().toString(16).slice(2, 10)}`,
        domain_table: domain.table,
        domain_label: domain.domain_label,
        label,
        notion_page_id: row.notion_page_id,
        row
      };
    };
    const firstRowForDomain = (table) => {
      const domain = domains.value.find((d) => d.table === table) || null;
      if (!domain || !domain.rows?.length) return null;
      const labelledRow = domain.rows.find((row) => Boolean(displayValue(row[domain.label_column])));
      if (!labelledRow) return null;
      return {
        domain,
        row: labelledRow
      };
    };
    const applyPresetFlow = (flowRaw) => {
      const flow = String(flowRaw || "").trim().toLowerCase();
      if (!flow) return;
      const next = [];
      const pushFirst = (table) => {
        const picked = firstRowForDomain(table);
        const item = makeStackItem(picked?.domain || null, picked?.row || null);
        if (item) next.push(item);
      };
      if (flow === "breath-only" || flow === "breath_only") {
        pushFirst("breath_library");
      }
      if (flow === "breath-movement" || flow === "breath_movement") {
        pushFirst("breath_library");
        pushFirst("movements_system");
      }
      if (flow === "breath-colour-sound-movement-nutrition" || flow === "breath_colour_sound_movement_nutrition") {
        pushFirst("breath_library");
        if (firstRowForDomain("light_colour")) {
          pushFirst("light_colour");
        } else {
          pushFirst("sound_vibration");
        }
        pushFirst("movements_system");
        if (firstRowForDomain("nutrition_and_food")) {
          pushFirst("nutrition_and_food");
        } else {
          pushFirst("nutrition_protocols");
        }
      }
      if (next.length) {
        stack.value = next;
      }
    };
    const filteredRows = computed(() => {
      const domain = currentDomain.value;
      if (!domain) return [];
      let rows = [...domain.rows];
      const term = searchTerm.value.trim().toLowerCase();
      if (term) {
        rows = rows.filter(
          (row) => domain.search_columns.some((col) => normalize(row[col]).includes(term))
        );
      }
      for (const col of domain.visible_filter_columns) {
        const selected = activeFilters.value[col];
        if (!selected) continue;
        rows = rows.filter((row) => displayValue(row[col]) === selected);
      }
      return rows;
    });
    const selectedRow = computed(() => {
      if (!selectedRowId.value) return null;
      return filteredRows.value.find((row, index) => rowKey(row, index) === selectedRowId.value) || null;
    });
    const previewWarnings = computed(() => {
      const safetyRules = payload.value?.support_tables?.safety_rules || [];
      return safetyRules.slice(0, 6).map((rule) => {
        const severity = displayValue(rule.severity || "Info");
        const name = displayValue(rule.rule_name || "");
        const description = displayValue(rule.description || "");
        return `${severity}: ${name}${description ? ` - ${description}` : ""}`;
      });
    });
    const combinedOutput = computed(() => {
      const mappings = payload.value?.support_tables?.mappings || [];
      const crossDomain = payload.value?.support_tables?.cross_domain_mappings || [];
      return {
        subject: selectedSubject.value,
        stack_order: stack.value.map((item, index) => ({
          order: index + 1,
          domain_table: item.domain_table,
          domain_label: item.domain_label,
          label: item.label,
          notion_page_id: item.notion_page_id || null
        })),
        warnings: previewWarnings.value,
        structure: {
          total_items: stack.value.length,
          domains_selected: Array.from(new Set(stack.value.map((s) => s.domain_table))),
          mapping_rows_available: mappings.length,
          cross_domain_rows_available: crossDomain.length
        }
      };
    });
    watch(
      [domains, () => route.query.flow],
      ([list, flow]) => {
        if (!list.length) return;
        const flowValue = String(flow || "").trim();
        if (!flowValue) return;
        applyPresetFlow(flowValue);
      },
      { immediate: true }
    );
    const colors = [
      "#2563eb",
      "#0ea5e9",
      "#0891b2",
      "#0d9488",
      "#16a34a",
      "#65a30d",
      "#ca8a04",
      "#ea580c",
      "#dc2626",
      "#9333ea",
      "#7c3aed",
      "#0369a1"
    ];
    const polarToCartesian = (cx, cy, r, angleDeg) => {
      const angle = (angleDeg - 90) * Math.PI / 180;
      return {
        x: cx + r * Math.cos(angle),
        y: cy + r * Math.sin(angle)
      };
    };
    const donutSlicePath = (cx, cy, outerR, innerR, startAngle, endAngle) => {
      const startOuter = polarToCartesian(cx, cy, outerR, endAngle);
      const endOuter = polarToCartesian(cx, cy, outerR, startAngle);
      const startInner = polarToCartesian(cx, cy, innerR, endAngle);
      const endInner = polarToCartesian(cx, cy, innerR, startAngle);
      const largeArcFlag = endAngle - startAngle <= 180 ? 0 : 1;
      return [
        `M ${startOuter.x} ${startOuter.y}`,
        `A ${outerR} ${outerR} 0 ${largeArcFlag} 0 ${endOuter.x} ${endOuter.y}`,
        `L ${endInner.x} ${endInner.y}`,
        `A ${innerR} ${innerR} 0 ${largeArcFlag} 1 ${startInner.x} ${startInner.y}`,
        "Z"
      ].join(" ");
    };
    const wheelSegments = computed(() => {
      const list = domains.value;
      if (!list.length) return [];
      const step = 360 / list.length;
      const cx = 310;
      const cy = 310;
      const outerR = 282;
      const innerR = 158;
      const labelR = 222;
      return list.map((domain, i) => {
        const start = i * step;
        const end = start + step;
        const mid = start + step / 2;
        const labelPoint = polarToCartesian(cx, cy, labelR, mid);
        return {
          table: domain.table,
          label: domain.domain_label,
          path: donutSlicePath(cx, cy, outerR, innerR, start, end),
          fill: colors[i % colors.length],
          labelX: labelPoint.x,
          labelY: labelPoint.y
        };
      });
    });
    return (_ctx, _push, _parent, _attrs) => {
      _push(`<div${ssrRenderAttrs(mergeProps({ class: "composer-page" }, _attrs))} data-v-379dbdfe><header class="top-subjects" data-v-379dbdfe><h1 data-v-379dbdfe>Sessions Composer Prototype</h1><div class="subject-row" data-v-379dbdfe><!--[-->`);
      ssrRenderList(unref(subjects), (subject) => {
        _push(`<button class="${ssrRenderClass({ active: unref(selectedSubject) === subject })}" data-v-379dbdfe>${ssrInterpolate(subject)}</button>`);
      });
      _push(`<!--]--></div><p class="source-note" data-v-379dbdfe> Source: <code data-v-379dbdfe>docs/SESSIONS_UI_PAYLOAD_2026-03-05.json</code></p></header><main class="composer-grid" data-v-379dbdfe><section class="wheel-pane" data-v-379dbdfe>`);
      if (unref(pending)) {
        _push(`<div class="status" data-v-379dbdfe>Loading composer payload...</div>`);
      } else if (unref(loadError)) {
        _push(`<div class="status error" data-v-379dbdfe> Failed to load payload: ${ssrInterpolate(unref(loadError))}</div>`);
      } else {
        _push(`<div class="wheel-wrap" data-v-379dbdfe><svg class="wheel" viewBox="0 0 620 620" role="img" aria-label="Domain wheel" data-v-379dbdfe><circle cx="310" cy="310" r="288" fill="#111827" data-v-379dbdfe></circle><!--[-->`);
        ssrRenderList(unref(wheelSegments), (segment) => {
          _push(`<path${ssrRenderAttr("d", segment.path)}${ssrRenderAttr("fill", segment.fill)}${ssrRenderAttr("stroke", segment.table === unref(selectedDomainTable) ? "#f59e0b" : "#0f172a")}${ssrRenderAttr("stroke-width", segment.table === unref(selectedDomainTable) ? 4 : 1.4)} class="segment" data-v-379dbdfe></path>`);
        });
        _push(`<!--]--><circle cx="310" cy="310" r="145" fill="#0b1220" data-v-379dbdfe></circle><text x="310" y="296" text-anchor="middle" fill="#e5e7eb" font-size="20" font-weight="700" data-v-379dbdfe> Domains </text><text x="310" y="324" text-anchor="middle" fill="#93a0b5" font-size="12" data-v-379dbdfe> Click a segment to open drawer </text><!--[-->`);
        ssrRenderList(unref(wheelSegments), (segment) => {
          _push(`<text${ssrRenderAttr("x", segment.labelX)}${ssrRenderAttr("y", segment.labelY)} text-anchor="middle" dominant-baseline="middle" fill="#f8fafc" font-size="11" class="wheel-label" data-v-379dbdfe>${ssrInterpolate(segment.label)}</text>`);
        });
        _push(`<!--]--></svg></div>`);
      }
      _push(`</section><aside class="${ssrRenderClass([{ open: unref(drawerOpen) }, "drawer"])}" data-v-379dbdfe><div class="drawer-header" data-v-379dbdfe><h2 data-v-379dbdfe>${ssrInterpolate(unref(currentDomain)?.domain_label || "Domain")}</h2><button class="close-btn" data-v-379dbdfe>Close</button></div>`);
      if (!unref(currentDomain)) {
        _push(`<div class="drawer-empty" data-v-379dbdfe>Select a domain on the wheel.</div>`);
      } else {
        _push(`<div class="drawer-content" data-v-379dbdfe><div class="search-row" data-v-379dbdfe><label data-v-379dbdfe>Search</label><input${ssrRenderAttr("value", unref(searchTerm))} type="text" placeholder="Search live rows..." data-v-379dbdfe></div><div class="filters" data-v-379dbdfe><!--[-->`);
        ssrRenderList(unref(currentDomain).visible_filter_columns, (column) => {
          _push(`<div class="filter" data-v-379dbdfe><label data-v-379dbdfe>${ssrInterpolate(column)}</label><select data-v-379dbdfe><option value="" data-v-379dbdfe${ssrIncludeBooleanAttr(Array.isArray(unref(activeFilters)[column]) ? ssrLooseContain(unref(activeFilters)[column], "") : ssrLooseEqual(unref(activeFilters)[column], "")) ? " selected" : ""}>All</option><!--[-->`);
          ssrRenderList(unref(currentDomain).visible_filter_values[column] || [], (value) => {
            _push(`<option${ssrRenderAttr("value", value)} data-v-379dbdfe${ssrIncludeBooleanAttr(Array.isArray(unref(activeFilters)[column]) ? ssrLooseContain(unref(activeFilters)[column], value) : ssrLooseEqual(unref(activeFilters)[column], value)) ? " selected" : ""}>${ssrInterpolate(value)}</option>`);
          });
          _push(`<!--]--></select></div>`);
        });
        _push(`<!--]--></div><div class="row-list" data-v-379dbdfe><h3 data-v-379dbdfe>Rows (${ssrInterpolate(unref(filteredRows).length)})</h3><ul data-v-379dbdfe><!--[-->`);
        ssrRenderList(unref(filteredRows), (row, rowIndex) => {
          _push(`<li class="${ssrRenderClass({ selected: rowKey(row, rowIndex) === unref(selectedRowId) })}" data-v-379dbdfe><div class="row-title" data-v-379dbdfe>${ssrInterpolate(displayValue(row[unref(currentDomain).label_column]))}</div><div class="row-sub" data-v-379dbdfe>${ssrInterpolate(displayValue(row[unref(currentDomain).subject_grouping_column]))}</div></li>`);
        });
        _push(`<!--]--></ul></div>`);
        if (unref(selectedRow)) {
          _push(`<div class="detail" data-v-379dbdfe><h3 data-v-379dbdfe>Detail</h3><dl data-v-379dbdfe><!--[-->`);
          ssrRenderList(unref(currentDomain).detail_fields, (field) => {
            _push(`<!--[--><dt data-v-379dbdfe>${ssrInterpolate(field)}</dt><dd data-v-379dbdfe>${ssrInterpolate(displayValue(unref(selectedRow)[field]))}</dd><!--]-->`);
          });
          _push(`<!--]--></dl><button class="add-btn" data-v-379dbdfe>Add To Session Stack</button></div>`);
        } else {
          _push(`<!---->`);
        }
        _push(`</div>`);
      }
      _push(`</aside></main><section class="stack-preview" data-v-379dbdfe><div class="stack" data-v-379dbdfe><h2 data-v-379dbdfe>Session Stack</h2><p class="hint" data-v-379dbdfe>Ordered selections to be used for generation and save.</p>`);
      if (unref(stack).length) {
        _push(`<ul data-v-379dbdfe><!--[-->`);
        ssrRenderList(unref(stack), (item, index) => {
          _push(`<li data-v-379dbdfe><span class="order" data-v-379dbdfe>${ssrInterpolate(index + 1)}</span><span class="label" data-v-379dbdfe>${ssrInterpolate(item.domain_label)}: ${ssrInterpolate(item.label)}</span><span class="actions" data-v-379dbdfe><button${ssrIncludeBooleanAttr(index === 0) ? " disabled" : ""} data-v-379dbdfe>Up</button><button${ssrIncludeBooleanAttr(index === unref(stack).length - 1) ? " disabled" : ""} data-v-379dbdfe>Down</button><button data-v-379dbdfe>Remove</button></span></li>`);
        });
        _push(`<!--]--></ul>`);
      } else {
        _push(`<p class="hint" data-v-379dbdfe>No items added yet.</p>`);
      }
      _push(`</div><div class="preview" data-v-379dbdfe><h2 data-v-379dbdfe>Preview</h2><div class="preview-block" data-v-379dbdfe><h3 data-v-379dbdfe>Warnings</h3><ul data-v-379dbdfe><!--[-->`);
      ssrRenderList(unref(previewWarnings), (warning, idx) => {
        _push(`<li data-v-379dbdfe>${ssrInterpolate(warning)}</li>`);
      });
      _push(`<!--]--></ul></div><div class="preview-block" data-v-379dbdfe><h3 data-v-379dbdfe>Combined Output Structure</h3><pre data-v-379dbdfe>${ssrInterpolate(JSON.stringify(unref(combinedOutput), null, 2))}</pre></div><button class="save-btn"${ssrIncludeBooleanAttr(!unref(stack).length || unref(saving)) ? " disabled" : ""} data-v-379dbdfe>${ssrInterpolate(unref(saving) ? "Saving..." : "Save Composer Session")}</button>`);
      if (unref(saveResult)) {
        _push(`<div class="save-result" data-v-379dbdfe><p data-v-379dbdfe><strong data-v-379dbdfe>Route:</strong> ${ssrInterpolate(saveRoute)}</p><p data-v-379dbdfe><strong data-v-379dbdfe>session_runs id:</strong> ${ssrInterpolate(unref(saveResult).session_run_id || "(none)")}</p><p data-v-379dbdfe><strong data-v-379dbdfe>session_outputs id(s):</strong> ${ssrInterpolate((unref(saveResult).session_output_ids || []).length ? unref(saveResult).session_output_ids.join(", ") : "(none)")}</p>`);
        if (unref(saveResult).blocker) {
          _push(`<p data-v-379dbdfe><strong data-v-379dbdfe>Blocker:</strong> ${ssrInterpolate(unref(saveResult).blocker.table)} - ${ssrInterpolate(unref(saveResult).blocker.issue)}</p>`);
        } else {
          _push(`<!---->`);
        }
        _push(`</div>`);
      } else {
        _push(`<!---->`);
      }
      _push(`</div></section></div>`);
    };
  }
});
const _sfc_setup = _sfc_main.setup;
_sfc_main.setup = (props, ctx) => {
  const ssrContext = useSSRContext();
  (ssrContext.modules || (ssrContext.modules = /* @__PURE__ */ new Set())).add("pages/sessions-composer-prototype.vue");
  return _sfc_setup ? _sfc_setup(props, ctx) : void 0;
};
const sessionsComposerPrototype = /* @__PURE__ */ _export_sfc(_sfc_main, [["__scopeId", "data-v-379dbdfe"]]);
export {
  sessionsComposerPrototype as default
};
//# sourceMappingURL=sessions-composer-prototype-D7CAlWye.js.map
