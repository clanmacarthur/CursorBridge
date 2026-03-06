globalThis.__timing__.logStart('Load chunks/routes/api/session/themes.get');import { h as setCookie, u as useRuntimeConfig, i as getHeader, c as defineEventHandler, f as setResponseStatus } from '../../../_/nitro.mjs';
import { createServerClient, parseCookieHeader } from '@supabase/ssr';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:path';
import 'node:crypto';
import 'node:url';

async function fetchWithRetry(req, init) {
  const retries = 3;
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      return await fetch(req, init);
    } catch (error) {
      if (init?.signal?.aborted) {
        throw error;
      }
      if (attempt === retries) {
        console.error(`Error fetching request ${req}`, error, init);
        throw error;
      }
      console.warn(`Retrying fetch attempt ${attempt + 1} for request: ${req}`);
    }
  }
  throw new Error("Unreachable code");
}

function setCookies(event, cookies) {
  const response = event.node.res;
  const headersWritable = () => !response.headersSent && !response.writableEnded;
  if (!headersWritable()) {
    return;
  }
  for (const { name, value, options } of cookies) {
    if (!headersWritable()) {
      break;
    }
    setCookie(event, name, value, options);
  }
}

const serverSupabaseClient = async (event) => {
  if (!event.context._supabaseClient) {
    const { url, key, cookiePrefix, cookieOptions, clientOptions: { auth = {}, global = {} } } = useRuntimeConfig(event).public.supabase;
    event.context._supabaseClient = createServerClient(url, key, {
      auth,
      cookies: {
        getAll: () => parseCookieHeader(getHeader(event, "Cookie") ?? ""),
        setAll: (cookies) => setCookies(event, cookies)
      },
      cookieOptions: {
        ...cookieOptions,
        name: cookiePrefix
      },
      global: {
        fetch: fetchWithRetry,
        ...global
      }
    });
  }
  return event.context._supabaseClient;
};

const THEME_DOMAIN_ORDER = [
  "lens",
  "colour",
  "chakra",
  "meridian",
  "organ",
  "emotion",
  "element",
  "stone",
  "deity",
  "symbol",
  "sacred_geometry",
  "sound",
  "practice_modality",
  "nutrition",
  "knowledge_pack"
];
const THEME_LABELS = {
  lens: "Lens",
  colour: "Colour",
  chakra: "Chakra",
  meridian: "Meridian",
  organ: "Organ",
  emotion: "Emotion",
  element: "Element",
  stone: "Stone",
  deity: "Deity Archetype",
  symbol: "Symbol",
  sacred_geometry: "Sacred Geometry",
  sound: "Sound",
  practice_modality: "Practice Modality",
  nutrition: "Nutrition",
  knowledge_pack: "Knowledge Pack"
};
const toText = (value, fallback = "") => {
  if (typeof value === "string" && value.trim()) return value.trim();
  if (typeof value === "number" && Number.isFinite(value)) return String(value);
  if (typeof value === "bigint") return String(value);
  return fallback;
};
const toNumber = (value) => {
  const parsed = Number(value);
  if (!Number.isFinite(parsed)) return null;
  return parsed;
};
const slugify = (value) => value.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
const splitTextValues = (value) => {
  if (Array.isArray(value)) {
    return value.map((item) => toText(item, "")).filter(Boolean);
  }
  if (typeof value === "string") {
    return value.split(/[,;|/]+/g).map((item) => item.trim()).filter(Boolean);
  }
  return [];
};
const uniqueStrings = (values) => Array.from(new Set(values.filter(Boolean)));
const normalizeColourValue = (value) => {
  const raw = toText(value, "");
  if (!raw) return void 0;
  return raw;
};
const clampStrength = (value) => {
  if (!Number.isFinite(value)) return 0.5;
  return Math.max(0, Math.min(1, value));
};
const parseStrength = (value) => {
  if (typeof value === "number") {
    if (value > 1 && value <= 100) return clampStrength(value / 100);
    return clampStrength(value);
  }
  if (typeof value === "string") {
    const trimmed = value.trim();
    if (!trimmed) return 0.5;
    if (trimmed.endsWith("%")) {
      const percentage = Number(trimmed.slice(0, -1));
      if (Number.isFinite(percentage)) return clampStrength(percentage / 100);
      return 0.5;
    }
    const numeric = Number(trimmed);
    if (Number.isFinite(numeric)) {
      if (numeric > 1 && numeric <= 100) return clampStrength(numeric / 100);
      return clampStrength(numeric);
    }
  }
  return 0.5;
};
const sortThemeOptions = (options) => {
  return [...options].sort((a, b) => {
    const weightA = typeof a.weight === "number" ? a.weight : 0;
    const weightB = typeof b.weight === "number" ? b.weight : 0;
    if (weightB !== weightA) return weightB - weightA;
    return a.label.localeCompare(b.label);
  });
};
const toTitleCase = (value) => value.split(/[\s_-]+/g).filter(Boolean).map((part) => part.charAt(0).toUpperCase() + part.slice(1).toLowerCase()).join(" ");
const shortText = (value, max = 64) => {
  const text = toText(value, "");
  if (!text) return "";
  if (text.length <= max) return text;
  return `${text.slice(0, Math.max(1, max - 3)).trim()}...`;
};
const elementAliasMap = {
  wood: "wood",
  tree: "wood",
  fire: "fire",
  earth: "earth",
  metal: "metal",
  water: "water",
  air: "air",
  wind: "air",
  ether: "ether",
  aether: "ether",
  space: "ether"
};
const normalizeElementKey = (value) => {
  const slug = slugify(toText(value, ""));
  if (!slug) return "";
  return elementAliasMap[slug] || slug;
};
const labelForElementKey = (key, fallback) => {
  if (!key) return toText(fallback, "");
  return toTitleCase(elementAliasMap[key] || key);
};
const normalizeModalityName = (value) => {
  const raw = toText(value, "").toLowerCase();
  const slug = slugify(raw);
  if (!slug) return "";
  if (raw.includes("breath")) return "breathwork";
  if (raw.includes("movement") || raw.includes("mobility") || raw.includes("qigong")) return "movement";
  if (raw.includes("nsdr") || raw.includes("nidra")) return "nsdr";
  if (raw.includes("visual")) return "visualization";
  if (raw.includes("self inquiry") || raw.includes("self-inquiry") || raw.includes("reflect")) {
    return "self-inquiry";
  }
  if (raw.includes("meditat") || raw.includes("mindful")) return "meditation";
  return slug;
};
const domainFromReference = (value) => {
  const normalized = toText(value, "").toLowerCase();
  if (!normalized) return null;
  if (normalized.includes("lens")) return "lens";
  if (normalized.includes("light_colour") || normalized.includes("light-colour")) return "colour";
  if (normalized.includes("light colour")) return "colour";
  if (normalized.includes("colour") || normalized.includes("color")) return "colour";
  if (normalized.includes("chakra")) return "chakra";
  if (normalized.includes("meridian")) return "meridian";
  if (normalized.includes("organ")) return "organ";
  if (normalized.includes("emotion") || normalized.includes("emotional") || normalized.includes("feeling")) {
    return "emotion";
  }
  if (normalized.includes("element")) return "element";
  if (normalized.includes("stone")) return "stone";
  if (normalized.includes("sacred_geometry") || normalized.includes("sacred geometry")) {
    return "sacred_geometry";
  }
  if (normalized.includes("sound") || normalized.includes("vibration")) return "sound";
  if (normalized.includes("practice_modality") || normalized.includes("practice modality") || normalized.includes("technique")) {
    return "practice_modality";
  }
  if (normalized.includes("nutrition") || normalized.includes("diet") || normalized.includes("food")) {
    return "nutrition";
  }
  if (normalized.includes("deit") || normalized.includes("archetype")) return "deity";
  if (normalized.includes("symbol")) return "symbol";
  if (normalized.includes("knowledge") || normalized.includes("kb_") || normalized.includes("kb")) {
    return "knowledge_pack";
  }
  return null;
};
const parseMappingPair = (value) => {
  const raw = toText(value, "");
  if (!raw) return null;
  const arrowSplit = raw.split(/->|=>|→/g);
  if (arrowSplit.length >= 2) {
    return [arrowSplit[0].trim(), arrowSplit[1].trim()];
  }
  return null;
};
const resolveLookupCandidates = (value) => {
  const raw = toText(value, "");
  const parts = splitTextValues(value);
  const values = [...parts, raw];
  const candidates = /* @__PURE__ */ new Set();
  for (const item of values) {
    const normalized = item.trim().toLowerCase();
    if (!normalized) continue;
    candidates.add(normalized);
    candidates.add(slugify(normalized));
    if (normalized.includes(":")) {
      const tail = normalized.split(":").pop() || "";
      if (tail) {
        candidates.add(tail);
        candidates.add(slugify(tail));
      }
    }
    const bare = normalized.replace(/^\w+\s*=\s*/, "");
    if (bare && bare !== normalized) {
      candidates.add(bare);
      candidates.add(slugify(bare));
    }
  }
  return Array.from(candidates);
};
const createWheelMap = () => {
  const wheels = {
    lens: { domain: "lens", label: THEME_LABELS.lens, options: [] },
    colour: { domain: "colour", label: THEME_LABELS.colour, options: [] },
    chakra: { domain: "chakra", label: THEME_LABELS.chakra, options: [] },
    meridian: { domain: "meridian", label: THEME_LABELS.meridian, options: [] },
    organ: { domain: "organ", label: THEME_LABELS.organ, options: [] },
    emotion: { domain: "emotion", label: THEME_LABELS.emotion, options: [] },
    element: { domain: "element", label: THEME_LABELS.element, options: [] },
    stone: { domain: "stone", label: THEME_LABELS.stone, options: [] },
    deity: { domain: "deity", label: THEME_LABELS.deity, options: [] },
    symbol: { domain: "symbol", label: THEME_LABELS.symbol, options: [] },
    sacred_geometry: {
      domain: "sacred_geometry",
      label: THEME_LABELS.sacred_geometry,
      options: []
    },
    sound: { domain: "sound", label: THEME_LABELS.sound, options: [] },
    practice_modality: {
      domain: "practice_modality",
      label: THEME_LABELS.practice_modality,
      options: []
    },
    nutrition: { domain: "nutrition", label: THEME_LABELS.nutrition, options: [] },
    knowledge_pack: {
      domain: "knowledge_pack",
      label: THEME_LABELS.knowledge_pack,
      options: []
    }
  };
  return wheels;
};
const buildOptionLookup = (wheels) => {
  const lookup = {
    lens: /* @__PURE__ */ new Map(),
    colour: /* @__PURE__ */ new Map(),
    chakra: /* @__PURE__ */ new Map(),
    meridian: /* @__PURE__ */ new Map(),
    organ: /* @__PURE__ */ new Map(),
    emotion: /* @__PURE__ */ new Map(),
    element: /* @__PURE__ */ new Map(),
    stone: /* @__PURE__ */ new Map(),
    deity: /* @__PURE__ */ new Map(),
    symbol: /* @__PURE__ */ new Map(),
    sacred_geometry: /* @__PURE__ */ new Map(),
    sound: /* @__PURE__ */ new Map(),
    practice_modality: /* @__PURE__ */ new Map(),
    nutrition: /* @__PURE__ */ new Map(),
    knowledge_pack: /* @__PURE__ */ new Map()
  };
  for (const domain of THEME_DOMAIN_ORDER) {
    for (const option of wheels[domain].options) {
      const keys = uniqueStrings([
        option.id.toLowerCase(),
        slugify(option.id),
        option.label.toLowerCase(),
        slugify(option.label),
        toText(option.secondaryLabel, "").toLowerCase(),
        slugify(toText(option.secondaryLabel, ""))
      ]);
      for (const key of keys) {
        lookup[domain].set(key, option.id);
      }
    }
  }
  return lookup;
};
const resolveOptionId = (lookup, domain, rawValue) => {
  const candidates = resolveLookupCandidates(rawValue);
  for (const candidate of candidates) {
    const resolved = lookup[domain].get(candidate);
    if (resolved) return resolved;
  }
  return null;
};
const optionExists = (wheels, domain, id) => {
  return wheels[domain].options.some((option) => option.id === id);
};
const addEdge = (edgeMap, wheels, edge) => {
  if (!optionExists(wheels, edge.fromDomain, edge.fromId)) return;
  if (!optionExists(wheels, edge.toDomain, edge.toId)) return;
  const normalizedEdge = {
    ...edge,
    strength: clampStrength(edge.strength)
  };
  const key = `${normalizedEdge.fromDomain}:${normalizedEdge.fromId}->${normalizedEdge.toDomain}:${normalizedEdge.toId}`;
  const existing = edgeMap.get(key);
  if (!existing || normalizedEdge.strength > existing.strength) {
    edgeMap.set(key, normalizedEdge);
  }
};
const symmetriseEdges = (wheels, edgeMap) => {
  const result = new Map(edgeMap);
  for (const edge of edgeMap.values()) {
    if (edge.fromDomain === edge.toDomain && edge.fromId === edge.toId) {
      continue;
    }
    const reverse = {
      fromDomain: edge.toDomain,
      fromId: edge.toId,
      toDomain: edge.fromDomain,
      toId: edge.fromId,
      strength: edge.strength,
      rationale: edge.rationale || "reverse-mapping"
    };
    addEdge(result, wheels, reverse);
  }
  return result;
};
const loadRows = async (client, table, columns, extra) => {
  try {
    let query = client.from(table).select(columns);
    if (extra) ;
    const { data, error } = await query;
    if (error) return [];
    return data || [];
  } catch {
    return [];
  }
};
const loadRowsWithFallback = async (client, table, preferredColumns, fallbackColumns = "*", extra) => {
  const preferred = await loadRows(client, table, preferredColumns, extra);
  if (preferred.length) return preferred;
  if (preferredColumns === fallbackColumns) return preferred;
  return loadRows(client, table, fallbackColumns, extra);
};
const addTextRelationEdges = (edgeMap, wheels, lookup, {
  fromDomain,
  fromValue,
  toDomain,
  toValue,
  strength,
  rationale
}) => {
  const fromId = resolveOptionId(lookup, fromDomain, fromValue);
  if (!fromId) return;
  const targets = splitTextValues(toValue);
  for (const target of targets) {
    const toId = resolveOptionId(lookup, toDomain, target);
    if (!toId) continue;
    addEdge(edgeMap, wheels, {
      fromDomain,
      fromId,
      toDomain,
      toId,
      strength: typeof strength === "number" ? strength : 0.5,
      rationale
    });
  }
};
async function buildThemeGraphFromSupabase(client) {
  const [
    lensRows,
    colourRows,
    chakraRows,
    meridianRows,
    organRows,
    deityRows,
    symbolRows,
    sacredGeometryRows,
    soundRows,
    elementalRows,
    nutritionProtocolRows,
    nutritionFoodRows,
    techniqueRows,
    knowledgeRows,
    programmeKnowledgeRows,
    mappingsRows,
    crossDomainRows
  ] = await Promise.all([
    loadRows(
      client,
      "lens_definitions",
      "id, lens_slug, lens_name, lens_description, paradigm_family, language_style, color, icon, sort_order, is_active, notes"
    ),
    loadRowsWithFallback(
      client,
      "light_colour",
      "id, light_colour, colour_family, primary_effect, psychological_theme, circadian_influence, wavelength_nm, wavelength__nm_, chakra_affinity, elemental_bias, notes"
    ),
    loadRows(
      client,
      "chakra_systems",
      "id, chakra, sanskrit_name, symbol, organ_emotion, primary_element, notes"
    ),
    loadRows(
      client,
      "meridian_system",
      "id, meridian, associated_organ, primary_emotion, five_element_phase, sound___vibration_system__db_, notes"
    ),
    loadRowsWithFallback(
      client,
      "organ_emotion_system",
      "id, organ___system, primary_emotion, secondary_emotion, primary_element, secondary_element, nervous_system_bias, stress_expression, symbol, chakra_systems__db_, chakra_systems__db__1, meridian_system__db_, sound___vibration_system__db_, notes"
    ),
    loadRows(
      client,
      "deities_archetypes",
      "id, name, type, primary_domain, associated_colours, key_symbols, notes"
    ),
    loadRows(
      client,
      "symbols_index",
      "id, symbol, stones, meaning_domain, symbol_class, sacred_geometry, primary_element, secondary_element, emotional_tone, chakra_systems__db_, notes"
    ),
    loadRows(
      client,
      "sacred_geometry",
      "id, geometry, geometry_class, symbols_index__db_, primary_element, secondary_element, psychophysiological_effect, notes"
    ),
    loadRows(
      client,
      "sound_vibration",
      "id, sound_type, sound___frequency, frequency__hz_, primary_effect, elemental_bias, chakra_affinity, primary_organ, notes"
    ),
    loadRows(
      client,
      "elemental_framework",
      "id, element, emotional_tone, core_qualities, typical_functions, notes"
    ),
    loadRows(
      client,
      "nutrition_protocols",
      "id, nutrition_protocol, primary_nutrition_goal, primary_attribute_focus, secondary_attribute_focus, strictness_level, notes"
    ),
    loadRowsWithFallback(
      client,
      "nutrition_and_food",
      "id, food_type, primary_nutrition_domain, secondary_nutrition_domains, associated_diets___protocols, feeds_intake_items, notes"
    ),
    loadRows(
      client,
      "techniques",
      "id, technique, technique_category, primary_intent, secondary_intents, objective, session_compatibility, notes"
    ),
    loadRows(
      client,
      "knowledge_bases",
      "id, kb_slug, kb_name, kb_description, primary_topics, is_active, sort_order"
    ),
    loadRows(client, "programme_knowledge_map", "kb_id, weight"),
    loadRows(
      client,
      "mappings",
      "id, from_db, to_db, from_value, to_value, from_field, to_field, mapping_type, mapping, notes"
    ),
    loadRows(
      client,
      "cross_domain_mappings",
      "id, source_domain, target_domain, technique_pattern, confidence, translation_notes, evidence_sources"
    )
  ]);
  const wheels = createWheelMap();
  const chakraSummaryByKey = /* @__PURE__ */ new Map();
  const addChakraSummary = (value, summary) => {
    const values = uniqueStrings([
      ...splitTextValues(value),
      toText(value, "")
    ]);
    for (const raw of values) {
      const normalized = raw.toLowerCase();
      const slug = slugify(raw);
      if (normalized && !chakraSummaryByKey.has(normalized)) {
        chakraSummaryByKey.set(normalized, summary);
      }
      if (slug && !chakraSummaryByKey.has(slug)) {
        chakraSummaryByKey.set(slug, summary);
      }
    }
  };
  for (const row of organRows || []) {
    const organLabel = toText(row == null ? void 0 : row.organ___system, "");
    const emotionLabel = splitTextValues(row == null ? void 0 : row.primary_emotion)[0] || "";
    const summary = shortText(
      [organLabel, emotionLabel].filter(Boolean).join(" \xB7 ") || toText(row == null ? void 0 : row.notes, ""),
      44
    );
    if (!summary) continue;
    addChakraSummary(row == null ? void 0 : row.chakra_systems__db_, summary);
    addChakraSummary(row == null ? void 0 : row.chakra_systems__db__1, summary);
  }
  const lensOptions = (lensRows || []).filter((row) => (row == null ? void 0 : row.is_active) !== false).map((row) => ({
    id: String(row.id),
    domain: "lens",
    label: toText(row.lens_name, toText(row.lens_slug, `Lens ${row.id}`)),
    secondaryLabel: shortText(row.paradigm_family, 38) || shortText(row.language_style, 38) || void 0,
    description: toText(row.lens_description, toText(row.notes, "")),
    colourHex: normalizeColourValue(row.color),
    glyph: toText(row.icon, ""),
    weight: toNumber(row.sort_order) || void 0
  }));
  const colourAttributeCandidates = [
    "wavelength_nm",
    "wavelength__nm_",
    "circadian_influence",
    "psychological_theme",
    "primary_effect",
    "colour_family",
    "chakra_affinity",
    "elemental_bias"
  ];
  const colourOptions = (colourRows || []).map((row) => {
    const colourValue = toText(row.light_colour, toText(row.light___colour, ""));
    const innerAttributes = colourAttributeCandidates.map((column) => {
      if (!(column in row)) return null;
      const raw = row[column];
      const value = raw === null || raw === void 0 ? "" : String(raw).trim();
      if (!value) return null;
      return {
        key: column,
        label: column,
        value
      };
    }).filter(Boolean);
    return {
      id: String(row.id),
      domain: "colour",
      label: toText(
        colourValue,
        toText(row.colour_family, toText(row.psychological_theme, `Colour ${row.id}`))
      ),
      secondaryLabel: shortText(row.psychological_theme, 38) || shortText(row.primary_effect, 38) || void 0,
      description: toText(row.primary_effect, toText(row.notes, "")),
      colourHex: normalizeColourValue(colourValue),
      innerAttributes: innerAttributes.length ? innerAttributes : void 0
    };
  });
  const chakraOptions = (chakraRows || []).map((row) => {
    const chakraId = String(row.id);
    const chakraName = toText(row.chakra, "");
    const sanskritName = toText(row.sanskrit_name, "");
    const fallbackSecondary = uniqueStrings([
      chakraSummaryByKey.get(chakraId.toLowerCase()) || "",
      chakraSummaryByKey.get(slugify(chakraId)) || "",
      chakraSummaryByKey.get(chakraName.toLowerCase()) || "",
      chakraSummaryByKey.get(slugify(chakraName)) || "",
      chakraSummaryByKey.get(sanskritName.toLowerCase()) || "",
      chakraSummaryByKey.get(slugify(sanskritName)) || "",
      shortText(row.organ_emotion, 44)
    ])[0];
    return {
      id: chakraId,
      domain: "chakra",
      label: toText(row.chakra, toText(row.sanskrit_name, `Chakra ${row.id}`)),
      secondaryLabel: shortText(row.primary_element, 38) || fallbackSecondary || void 0,
      description: toText(row.notes, ""),
      glyph: toText(row.symbol, "")
    };
  });
  const meridianOptions = (meridianRows || []).map((row) => ({
    id: String(row.id),
    domain: "meridian",
    label: toText(row.meridian, `Meridian ${row.id}`),
    secondaryLabel: shortText(row.five_element_phase, 32) || void 0,
    description: toText(row.primary_emotion, toText(row.notes, ""))
  }));
  const organAttributeCandidates = [
    "secondary_emotion",
    "primary_element",
    "secondary_element",
    "nervous_system_bias",
    "stress_expression"
  ];
  const organOptions = (organRows || []).map((row) => {
    const innerAttributes = organAttributeCandidates.map((column) => {
      if (!(column in row)) return null;
      const raw = row[column];
      if (raw === null || raw === void 0) return null;
      const value = String(raw).trim();
      if (!value) return null;
      return {
        key: column,
        label: column,
        value
      };
    }).filter(Boolean);
    return {
      id: String(row.id),
      domain: "organ",
      label: toText(row.organ___system, `Organ ${row.id}`),
      secondaryLabel: toText(row.primary_emotion, ""),
      description: toText(row.notes, ""),
      glyph: toText(row.symbol, ""),
      innerAttributes: innerAttributes.length ? innerAttributes : void 0
    };
  });
  const emotionCounts = /* @__PURE__ */ new Map();
  for (const row of organRows || []) {
    for (const emotion of splitTextValues(row == null ? void 0 : row.primary_emotion)) {
      const key = slugify(emotion);
      if (!key) continue;
      const existing = emotionCounts.get(key) || {
        label: emotion,
        fromOrgans: 0,
        fromMeridians: 0,
        description: toText(row == null ? void 0 : row.notes, "")
      };
      existing.fromOrgans += 1;
      if (!existing.description) existing.description = toText(row == null ? void 0 : row.notes, "");
      emotionCounts.set(key, existing);
    }
  }
  for (const row of meridianRows || []) {
    for (const emotion of splitTextValues(row == null ? void 0 : row.primary_emotion)) {
      const key = slugify(emotion);
      if (!key) continue;
      const existing = emotionCounts.get(key) || {
        label: emotion,
        fromOrgans: 0,
        fromMeridians: 0,
        description: toText(row == null ? void 0 : row.notes, "")
      };
      existing.fromMeridians += 1;
      if (!existing.description) existing.description = toText(row == null ? void 0 : row.notes, "");
      emotionCounts.set(key, existing);
    }
  }
  const emotionOptions = Array.from(emotionCounts.entries()).map(([id, item]) => ({
    id,
    domain: "emotion",
    label: item.label,
    secondaryLabel: `Organs ${item.fromOrgans} \xB7 Meridians ${item.fromMeridians}`,
    description: item.description,
    weight: item.fromOrgans + item.fromMeridians
  }));
  const elementIndex = /* @__PURE__ */ new Map();
  const touchElement = (rawElement, sourceType, sourceLabel, description) => {
    for (const elementValue of splitTextValues(rawElement)) {
      const key = normalizeElementKey(elementValue);
      if (!key) continue;
      const existing = elementIndex.get(key) || {
        label: labelForElementKey(key, elementValue),
        meridianCount: 0,
        organCount: 0,
        samples: [],
        description: ""
      };
      if (sourceType === "meridian") existing.meridianCount += 1;
      if (sourceType === "organ") existing.organCount += 1;
      if (sourceLabel && existing.samples.length < 2 && !existing.samples.includes(sourceLabel)) {
        existing.samples.push(sourceLabel);
      }
      if (!existing.description) {
        existing.description = shortText(description, 72);
      }
      elementIndex.set(key, existing);
    }
  };
  for (const row of elementalRows || []) {
    touchElement(
      row == null ? void 0 : row.element,
      "framework",
      "",
      toText(row == null ? void 0 : row.emotional_tone, toText(row == null ? void 0 : row.typical_functions, toText(row == null ? void 0 : row.core_qualities, row == null ? void 0 : row.notes)))
    );
  }
  for (const row of meridianRows || []) {
    touchElement(
      row == null ? void 0 : row.five_element_phase,
      "meridian",
      toText(row == null ? void 0 : row.meridian, ""),
      toText(row == null ? void 0 : row.notes, "")
    );
  }
  for (const row of organRows || []) {
    const label = toText(row == null ? void 0 : row.organ___system, "");
    touchElement(
      row == null ? void 0 : row.primary_element,
      "organ",
      label,
      toText(row == null ? void 0 : row.primary_emotion, toText(row == null ? void 0 : row.notes, ""))
    );
    touchElement(
      row == null ? void 0 : row.secondary_element,
      "organ",
      label,
      toText(row == null ? void 0 : row.secondary_emotion, toText(row == null ? void 0 : row.notes, ""))
    );
  }
  const elementOptions = Array.from(elementIndex.entries()).map(([id, item]) => ({
    id,
    domain: "element",
    label: item.label,
    secondaryLabel: item.samples.join(" / ") || void 0,
    description: item.description,
    weight: item.meridianCount + item.organCount || 1
  }));
  const symbolOptions = (symbolRows || []).map((row) => ({
    id: String(row.id),
    domain: "symbol",
    label: toText(row.symbol, toText(row.stones, `Symbol ${row.id}`)),
    secondaryLabel: shortText(row.symbol_class, 38) || void 0,
    description: toText(row.meaning_domain, toText(row.notes, ""))
  }));
  const stoneCounts = /* @__PURE__ */ new Map();
  for (const row of symbolRows || []) {
    for (const stone of splitTextValues(row == null ? void 0 : row.stones)) {
      const key = slugify(stone);
      if (!key) continue;
      const existing = stoneCounts.get(key);
      if (existing) {
        existing.count += 1;
        if (!existing.secondaryLabel) {
          existing.secondaryLabel = shortText(row == null ? void 0 : row.symbol_class, 34) || shortText(row == null ? void 0 : row.meaning_domain, 34);
        }
        stoneCounts.set(key, existing);
        continue;
      }
      stoneCounts.set(key, {
        label: stone,
        count: 1,
        secondaryLabel: shortText(row == null ? void 0 : row.symbol_class, 34) || shortText(row == null ? void 0 : row.meaning_domain, 34) || void 0,
        description: toText(row == null ? void 0 : row.meaning_domain, toText(row == null ? void 0 : row.notes, ""))
      });
    }
  }
  const stoneOptions = Array.from(stoneCounts.entries()).map(([key, item]) => ({
    id: key,
    domain: "stone",
    label: item.label,
    secondaryLabel: item.secondaryLabel,
    description: item.description,
    weight: item.count
  }));
  const deityOptions = (deityRows || []).map((row) => ({
    id: String(row.id),
    domain: "deity",
    label: toText(row.name, `Deity ${row.id}`),
    secondaryLabel: shortText(row.primary_domain, 38) || shortText(row.type, 38) || void 0,
    description: toText(row.notes, toText(row.type, "")),
    glyph: splitTextValues(row.key_symbols)[0] || void 0
  }));
  const sacredGeometryById = /* @__PURE__ */ new Map();
  const upsertSacredGeometry = (option) => {
    if (!option.id) return;
    if (!sacredGeometryById.has(option.id)) {
      sacredGeometryById.set(option.id, option);
      return;
    }
    const existing = sacredGeometryById.get(option.id);
    sacredGeometryById.set(option.id, {
      ...existing,
      secondaryLabel: existing.secondaryLabel || option.secondaryLabel,
      description: existing.description || option.description,
      weight: Math.max(existing.weight || 0, option.weight || 0)
    });
  };
  for (const row of sacredGeometryRows || []) {
    const label = toText(row == null ? void 0 : row.geometry, toText(row == null ? void 0 : row.untitled_database, ""));
    const id = slugify(label);
    if (!id) continue;
    upsertSacredGeometry({
      id,
      domain: "sacred_geometry",
      label,
      secondaryLabel: shortText(row == null ? void 0 : row.geometry_class, 40) || shortText(row == null ? void 0 : row.primary_element, 40) || shortText(row == null ? void 0 : row.secondary_element, 40) || void 0,
      description: toText(row == null ? void 0 : row.psychophysiological_effect, toText(row == null ? void 0 : row.notes, "")),
      weight: 1
    });
  }
  for (const row of symbolRows || []) {
    const tags = [
      toText(row == null ? void 0 : row.symbol_class, ""),
      toText(row == null ? void 0 : row.meaning_domain, ""),
      toText(row == null ? void 0 : row.sacred_geometry, "")
    ].join(" ").toLowerCase();
    if (!tags.includes("sacred geometry")) continue;
    const label = toText(row == null ? void 0 : row.symbol, "");
    const id = slugify(label);
    if (!id) continue;
    upsertSacredGeometry({
      id,
      domain: "sacred_geometry",
      label,
      secondaryLabel: shortText(row == null ? void 0 : row.symbol_class, 40) || shortText(row == null ? void 0 : row.sacred_geometry, 40) || shortText(row == null ? void 0 : row.meaning_domain, 40) || void 0,
      description: toText(row == null ? void 0 : row.notes, toText(row == null ? void 0 : row.meaning_domain, "")),
      weight: 1
    });
  }
  const sacredGeometryOptions = Array.from(sacredGeometryById.values());
  const programmeWeightByKnowledgeId = /* @__PURE__ */ new Map();
  for (const row of programmeKnowledgeRows || []) {
    const kbId = toText(row == null ? void 0 : row.kb_id, "");
    if (!kbId) continue;
    const weight = toNumber(row == null ? void 0 : row.weight) || 0;
    const existing = programmeWeightByKnowledgeId.get(kbId) || 0;
    programmeWeightByKnowledgeId.set(kbId, Math.max(existing, weight));
  }
  const knowledgeOptions = (knowledgeRows || []).filter((row) => (row == null ? void 0 : row.is_active) !== false).map((row) => ({
    id: String(row.id),
    domain: "knowledge_pack",
    label: toText(row.kb_name, toText(row.kb_slug, `Knowledge ${row.id}`)),
    secondaryLabel: shortText(row.primary_topics, 44) || void 0,
    description: toText(row.kb_description, toText(row.primary_topics, "")),
    weight: programmeWeightByKnowledgeId.get(String(row.id))
  }));
  const soundKeywords = ["sound", "mantra", "binaural", "nsdr", "frequency", "vibration"];
  const soundFamilyMap = /* @__PURE__ */ new Map();
  for (const row of soundRows || []) {
    const family = toText(row == null ? void 0 : row.sound_type, toText(row == null ? void 0 : row.sound___frequency, toText(row == null ? void 0 : row.frequency__hz_, "")));
    const id = slugify(family);
    if (!id) continue;
    const existing = soundFamilyMap.get(id);
    const next = {
      id,
      domain: "sound",
      label: family,
      secondaryLabel: shortText(row == null ? void 0 : row.frequency__hz_, 34) || shortText(row == null ? void 0 : row.sound___frequency, 34) || shortText(row == null ? void 0 : row.primary_effect, 34) || void 0,
      description: toText(row == null ? void 0 : row.primary_effect, toText(row == null ? void 0 : row.notes, "")),
      weight: ((existing == null ? void 0 : existing.weight) || 0) + 1
    };
    soundFamilyMap.set(id, existing ? { ...existing, ...next } : next);
  }
  if (!soundFamilyMap.size) {
    for (const row of knowledgeRows || []) {
      const topics = toText(row == null ? void 0 : row.primary_topics, "").toLowerCase();
      const name = toText(row == null ? void 0 : row.kb_name, "").toLowerCase();
      if (!soundKeywords.some((keyword) => topics.includes(keyword) || name.includes(keyword))) continue;
      const id = `kb-${row.id}`;
      soundFamilyMap.set(id, {
        id,
        domain: "sound",
        label: toText(row == null ? void 0 : row.kb_name, toText(row == null ? void 0 : row.kb_slug, `Sound ${row == null ? void 0 : row.id}`)),
        secondaryLabel: shortText(row == null ? void 0 : row.primary_topics, 34) || void 0,
        description: toText(row == null ? void 0 : row.kb_description, toText(row == null ? void 0 : row.notes, "")),
        weight: programmeWeightByKnowledgeId.get(String(row == null ? void 0 : row.id)) || 1
      });
    }
  }
  const soundOptions = Array.from(soundFamilyMap.values());
  const modalityMap = /* @__PURE__ */ new Map();
  for (const row of techniqueRows || []) {
    const rawModality = toText(
      row == null ? void 0 : row.technique_category,
      toText(row == null ? void 0 : row.primary_intent, toText(row == null ? void 0 : row.session_compatibility, ""))
    );
    const normalized = normalizeModalityName(rawModality);
    if (!normalized) continue;
    const label = toTitleCase(normalized.replace(/-/g, " "));
    const existing = modalityMap.get(normalized);
    modalityMap.set(normalized, {
      id: normalized,
      domain: "practice_modality",
      label,
      secondaryLabel: shortText(row == null ? void 0 : row.primary_intent, 34) || shortText(row == null ? void 0 : row.session_compatibility, 34) || (existing == null ? void 0 : existing.secondaryLabel),
      description: toText(row == null ? void 0 : row.objective, toText(row == null ? void 0 : row.notes, "")) || (existing == null ? void 0 : existing.description),
      weight: ((existing == null ? void 0 : existing.weight) || 0) + 1
    });
  }
  const practiceModalityOptions = Array.from(modalityMap.values());
  const nutritionOptions = [];
  for (const row of nutritionProtocolRows || []) {
    nutritionOptions.push({
      id: `protocol:${row.id}`,
      domain: "nutrition",
      label: toText(row.nutrition_protocol, `Protocol ${row.id}`),
      secondaryLabel: toText(row.primary_nutrition_goal, ""),
      description: toText(row.primary_attribute_focus, toText(row.secondary_attribute_focus, "")),
      innerAttributes: void 0
    });
  }
  const nutritionFoodAttributeCandidates = [
    "feeds_intake_items",
    "associated_diets___protocols",
    "secondary_nutrition_domains"
  ];
  for (const row of nutritionFoodRows || []) {
    const innerAttributes = nutritionFoodAttributeCandidates.map((column) => {
      if (!(column in row)) return null;
      const raw = row[column];
      if (raw === null || raw === void 0) return null;
      const value = String(raw).trim();
      if (!value) return null;
      return {
        key: column,
        label: column,
        value
      };
    }).filter(Boolean);
    nutritionOptions.push({
      id: `food:${row.id}`,
      domain: "nutrition",
      label: toText(row.food_type, toText(row.primary_nutrition_domain, `Food ${row.id}`)),
      secondaryLabel: toText(row.primary_nutrition_domain, ""),
      description: toText(row.notes, ""),
      innerAttributes: innerAttributes.length ? innerAttributes : void 0
    });
  }
  wheels.lens.options = sortThemeOptions(lensOptions);
  wheels.colour.options = sortThemeOptions(colourOptions);
  wheels.chakra.options = sortThemeOptions(chakraOptions);
  wheels.meridian.options = sortThemeOptions(meridianOptions);
  wheels.organ.options = sortThemeOptions(organOptions);
  wheels.emotion.options = sortThemeOptions(emotionOptions);
  wheels.element.options = sortThemeOptions(elementOptions);
  wheels.stone.options = sortThemeOptions(stoneOptions);
  wheels.deity.options = sortThemeOptions(deityOptions);
  wheels.symbol.options = sortThemeOptions(symbolOptions);
  wheels.sacred_geometry.options = sortThemeOptions(sacredGeometryOptions);
  wheels.sound.options = sortThemeOptions(soundOptions);
  wheels.practice_modality.options = sortThemeOptions(practiceModalityOptions);
  wheels.nutrition.options = sortThemeOptions(nutritionOptions);
  wheels.knowledge_pack.options = sortThemeOptions(knowledgeOptions);
  const lookup = buildOptionLookup(wheels);
  const edgeMap = /* @__PURE__ */ new Map();
  for (const row of chakraRows || []) {
    const rationale = toText(row == null ? void 0 : row.notes, "") || "chakra_systems relation";
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "chakra",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "organ",
      toValue: row == null ? void 0 : row.organ_emotion,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "chakra",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "symbol",
      toValue: row == null ? void 0 : row.symbol,
      rationale
    });
  }
  for (const row of meridianRows || []) {
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "meridian",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "organ",
      toValue: row == null ? void 0 : row.associated_organ,
      rationale: toText(row == null ? void 0 : row.notes, "") || "meridian_system relation"
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "meridian",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "element",
      toValue: row == null ? void 0 : row.five_element_phase,
      rationale: toText(row == null ? void 0 : row.notes, "") || "meridian_system.five_element_phase"
    });
  }
  for (const row of organRows || []) {
    const rationale = toText(row == null ? void 0 : row.notes, "") || "organ_emotion_system relation";
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "organ",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "chakra",
      toValue: row == null ? void 0 : row.chakra_systems__db_,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "organ",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "chakra",
      toValue: row == null ? void 0 : row.chakra_systems__db__1,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "organ",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "meridian",
      toValue: row == null ? void 0 : row.meridian_system__db_,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "organ",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "symbol",
      toValue: row == null ? void 0 : row.symbol,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "organ",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "element",
      toValue: row == null ? void 0 : row.primary_element,
      rationale: toText(row == null ? void 0 : row.notes, "") || "organ_emotion_system.primary_element"
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "organ",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "element",
      toValue: row == null ? void 0 : row.secondary_element,
      rationale: toText(row == null ? void 0 : row.notes, "") || "organ_emotion_system.secondary_element"
    });
  }
  for (const row of organRows || []) {
    const rationale = toText(row == null ? void 0 : row.notes, "") || "organ_emotion_system.primary_emotion";
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "organ",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "emotion",
      toValue: row == null ? void 0 : row.primary_emotion,
      rationale
    });
  }
  for (const row of meridianRows || []) {
    const rationale = toText(row == null ? void 0 : row.notes, "") || "meridian_system.primary_emotion";
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "meridian",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "emotion",
      toValue: row == null ? void 0 : row.primary_emotion,
      rationale
    });
  }
  for (const row of colourRows || []) {
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "colour",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "chakra",
      toValue: row == null ? void 0 : row.chakra_affinity,
      rationale: toText(row == null ? void 0 : row.notes, "") || "light_colour relation"
    });
    const rationale = toText(row == null ? void 0 : row.notes, "") || "light_colour.emotion_theme";
    const emotionSource = (row == null ? void 0 : row.psychological_theme) || (row == null ? void 0 : row.primary_effect);
    if (!emotionSource) continue;
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "colour",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "emotion",
      toValue: emotionSource,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "colour",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "element",
      toValue: row == null ? void 0 : row.elemental_bias,
      rationale: toText(row == null ? void 0 : row.notes, "") || "light_colour.elemental_bias"
    });
  }
  for (const row of symbolRows || []) {
    const rationale = toText(row == null ? void 0 : row.notes, "") || "symbols_index relation";
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "symbol",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "chakra",
      toValue: row == null ? void 0 : row.chakra_systems__db_,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "symbol",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "stone",
      toValue: row == null ? void 0 : row.stones,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "symbol",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "element",
      toValue: row == null ? void 0 : row.primary_element,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "symbol",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "element",
      toValue: row == null ? void 0 : row.secondary_element,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "symbol",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "sacred_geometry",
      toValue: row == null ? void 0 : row.sacred_geometry,
      rationale
    });
  }
  for (const row of sacredGeometryRows || []) {
    const rationale = toText(row == null ? void 0 : row.notes, "") || "sacred_geometry.symbols_index__db_";
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "sacred_geometry",
      fromValue: row == null ? void 0 : row.geometry,
      toDomain: "symbol",
      toValue: row == null ? void 0 : row.symbols_index__db_,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "sacred_geometry",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "symbol",
      toValue: row == null ? void 0 : row.symbols_index__db_,
      rationale
    });
  }
  for (const row of nutritionProtocolRows || []) {
    const rationale = toText(row == null ? void 0 : row.notes, "") || "nutrition_protocols relation";
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "nutrition",
      fromValue: row == null ? void 0 : row.nutrition_protocol,
      toDomain: "element",
      toValue: row == null ? void 0 : row.primary_attribute_focus,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "nutrition",
      fromValue: row == null ? void 0 : row.nutrition_protocol,
      toDomain: "emotion",
      toValue: row == null ? void 0 : row.secondary_attribute_focus,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "nutrition",
      fromValue: row == null ? void 0 : row.nutrition_protocol,
      toDomain: "organ",
      toValue: row == null ? void 0 : row.primary_attribute_focus,
      rationale
    });
  }
  for (const row of deityRows || []) {
    const rationale = toText(row == null ? void 0 : row.notes, "") || "deities_archetypes relation";
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "deity",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "colour",
      toValue: row == null ? void 0 : row.associated_colours,
      rationale
    });
    addTextRelationEdges(edgeMap, wheels, lookup, {
      fromDomain: "deity",
      fromValue: row == null ? void 0 : row.id,
      toDomain: "symbol",
      toValue: row == null ? void 0 : row.key_symbols,
      rationale
    });
  }
  for (const row of mappingsRows || []) {
    const fromDomain = domainFromReference(row == null ? void 0 : row.from_db) || domainFromReference(row == null ? void 0 : row.from_field) || domainFromReference(row == null ? void 0 : row.mapping_type);
    const toDomain = domainFromReference(row == null ? void 0 : row.to_db) || domainFromReference(row == null ? void 0 : row.to_field) || domainFromReference(row == null ? void 0 : row.mapping_type);
    if (!fromDomain || !toDomain) continue;
    const parsedPair = parseMappingPair(row == null ? void 0 : row.mapping);
    const fromRaw = toText(row == null ? void 0 : row.from_value, "") || (parsedPair == null ? void 0 : parsedPair[0]) || "";
    const toRaw = toText(row == null ? void 0 : row.to_value, "") || (parsedPair == null ? void 0 : parsedPair[1]) || "";
    const fromId = resolveOptionId(lookup, fromDomain, fromRaw);
    const toId = resolveOptionId(lookup, toDomain, toRaw);
    if (!fromId || !toId) continue;
    addEdge(edgeMap, wheels, {
      fromDomain,
      fromId,
      toDomain,
      toId,
      strength: 0.5,
      rationale: toText(row == null ? void 0 : row.notes, toText(row == null ? void 0 : row.mapping, "mappings relation"))
    });
  }
  for (const row of crossDomainRows || []) {
    const fromDomain = domainFromReference(row == null ? void 0 : row.source_domain);
    const toDomain = domainFromReference(row == null ? void 0 : row.target_domain);
    if (!fromDomain || !toDomain) continue;
    const pair = parseMappingPair(row == null ? void 0 : row.technique_pattern);
    if (!pair) continue;
    const fromId = resolveOptionId(lookup, fromDomain, pair[0]);
    const toId = resolveOptionId(lookup, toDomain, pair[1]);
    if (!fromId || !toId) continue;
    addEdge(edgeMap, wheels, {
      fromDomain,
      fromId,
      toDomain,
      toId,
      strength: parseStrength(row == null ? void 0 : row.confidence),
      rationale: toText(row == null ? void 0 : row.translation_notes, "") || toText(row == null ? void 0 : row.evidence_sources, "") || "cross_domain_mappings relation"
    });
  }
  const symmetrisedEdgeMap = symmetriseEdges(wheels, edgeMap);
  const edges = Array.from(symmetrisedEdgeMap.values()).sort((a, b) => {
    if (a.fromDomain !== b.fromDomain) return a.fromDomain.localeCompare(b.fromDomain);
    if (a.fromId !== b.fromId) return a.fromId.localeCompare(b.fromId);
    if (a.toDomain !== b.toDomain) return a.toDomain.localeCompare(b.toDomain);
    return a.toId.localeCompare(b.toId);
  });
  const graph = {
    wheels: THEME_DOMAIN_ORDER.map((domain) => ({
      domain,
      label: wheels[domain].label,
      options: wheels[domain].options
    })),
    edges
  };
  return graph;
}

const themes_get = defineEventHandler(async (event) => {
  try {
    const client = await serverSupabaseClient(event);
    const graph = await buildThemeGraphFromSupabase(client);
    return { graph };
  } catch (error) {
    setResponseStatus(event, 503);
    return {
      graph: {
        wheels: [],
        edges: []
      },
      ok: false,
      code: "THEME_GRAPH_UNAVAILABLE",
      message: "Theme graph endpoint is wired, but data load failed in this environment.",
      route: "/api/session/themes",
      error: (error == null ? void 0 : error.message) || "unknown error",
      next_doc: "docs/TASK_MANAGER_CURSORBRIDGE_ALIGNMENT.md"
    };
  }
});

export { themes_get as default };;globalThis.__timing__.logEnd('Load chunks/routes/api/session/themes.get');
//# sourceMappingURL=themes.get.mjs.map
