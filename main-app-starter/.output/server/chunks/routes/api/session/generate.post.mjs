globalThis.__timing__.logStart('Load chunks/routes/api/session/generate.post');import { c as defineEventHandler, r as readBody, f as setResponseStatus } from '../../../_/nitro.mjs';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:path';
import 'node:crypto';
import 'node:url';

const generate_post = defineEventHandler(async (event) => {
  var _a, _b, _c;
  const body = await readBody(event);
  const plannerConfig = (body == null ? void 0 : body.planner_config) || (body == null ? void 0 : body.plannerConfig) || null;
  const dialSelection = (body == null ? void 0 : body.dial_selection) || (body == null ? void 0 : body.dialSelection) || null;
  const themeSelection = (body == null ? void 0 : body.theme_selection) || (body == null ? void 0 : body.themeSelection) || null;
  const templateId = (body == null ? void 0 : body.template_id) || (body == null ? void 0 : body.blueprint_id) || null;
  const durationMinutes = (_c = (_b = (_a = body == null ? void 0 : body.duration_minutes) != null ? _a : body == null ? void 0 : body.duration_override_min) != null ? _b : plannerConfig == null ? void 0 : plannerConfig.duration_minutes) != null ? _c : null;
  setResponseStatus(event, 501);
  return {
    session_run_id: null,
    session_output_id: null,
    output_data: {
      template_id: templateId,
      duration_minutes: durationMinutes,
      phases: [],
      dial_selection: dialSelection,
      theme_selection: themeSelection,
      dial_context: {},
      theme_context: {},
      safety: {
        rules_applied: [],
        warnings: []
      }
    },
    narration_text: "",
    using_service_role: false,
    persisted: false,
    ok: false,
    code: "NOT_IMPLEMENTED",
    message: "Session generate contract is available, but persistence/planning logic is not implemented here yet.",
    route: "/api/session/generate",
    received_keys: body && typeof body === "object" ? Object.keys(body) : [],
    next_doc: "docs/TASK_MANAGER_CURSORBRIDGE_ALIGNMENT.md"
  };
});

export { generate_post as default };;globalThis.__timing__.logEnd('Load chunks/routes/api/session/generate.post');
//# sourceMappingURL=generate.post.mjs.map
