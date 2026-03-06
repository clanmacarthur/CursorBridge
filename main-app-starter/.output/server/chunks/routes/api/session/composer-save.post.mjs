globalThis.__timing__.logStart('Load chunks/routes/api/session/composer-save.post');import { c as defineEventHandler, r as readBody, f as setResponseStatus } from '../../../_/nitro.mjs';
import { readFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import 'node:http';
import 'node:https';
import 'node:events';
import 'node:buffer';
import 'node:fs';
import 'node:crypto';
import 'node:url';

const TASK_MANAGER_ENV = resolve("C:\\code\\task-manager\\.env");
const loadEnvFile = async (filePath) => {
  const text = await readFile(filePath, "utf-8");
  const out = {};
  for (const raw of text.split(/\r?\n/g)) {
    const line = raw.trim();
    if (!line || line.startsWith("#") || !line.includes("=")) continue;
    const [key, ...rest] = line.split("=");
    out[key.trim().replace(/^\uFEFF/, "")] = rest.join("=").trim().replace(/^['"]|['"]$/g, "");
  }
  return out;
};
const getSupabaseCreds = async () => {
  const env = await loadEnvFile(TASK_MANAGER_ENV);
  const url = (env.SUPABASE_URL || "").trim().replace(/\/$/, "");
  const key = (env.SUPABASE_KEY || env.SUPABASE_ANON_KEY || "").trim();
  if (!url || !key) {
    throw new Error("Supabase credentials missing in task-manager .env");
  }
  return { url, key };
};
const signupTempUser = async (url, anonKey) => {
  var _a;
  const email = `composer_proto_${Date.now()}_${Math.random().toString(16).slice(2, 8)}@example.com`;
  const password = `Composer!${Math.random().toString(36).slice(2, 12)}A1`;
  const response = await fetch(`${url}/auth/v1/signup`, {
    method: "POST",
    headers: {
      apikey: anonKey,
      Authorization: `Bearer ${anonKey}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ email, password })
  });
  if (!response.ok) {
    throw new Error(`Auth signup failed (${response.status})`);
  }
  const data = await response.json();
  const accessToken = data == null ? void 0 : data.access_token;
  const userId = (_a = data == null ? void 0 : data.user) == null ? void 0 : _a.id;
  if (!accessToken || !userId) {
    throw new Error("Auth signup did not return access token and user id");
  }
  return { accessToken, userId, email };
};
const insertRow = async (url, anonKey, authToken, table, payload) => {
  const response = await fetch(`${url}/rest/v1/${table}`, {
    method: "POST",
    headers: {
      apikey: anonKey,
      Authorization: `Bearer ${authToken}`,
      "Content-Type": "application/json",
      Prefer: "return=representation"
    },
    body: JSON.stringify(payload)
  });
  const bodyText = await response.text();
  let bodyJson = null;
  try {
    bodyJson = JSON.parse(bodyText);
  } catch {
    bodyJson = bodyText;
  }
  return {
    ok: response.ok,
    status: response.status,
    data: bodyJson
  };
};
const composerSave_post = defineEventHandler(async (event) => {
  var _a;
  const body = await readBody(event);
  const stack = Array.isArray(body == null ? void 0 : body.stack) ? body.stack : [];
  if (!(body == null ? void 0 : body.subject) || !stack.length) {
    setResponseStatus(event, 400);
    return {
      ok: false,
      route: "/api/session/composer-save",
      code: "INVALID_INPUT",
      message: "subject and non-empty stack are required"
    };
  }
  try {
    const { url, key } = await getSupabaseCreds();
    const auth = await signupTempUser(url, key);
    const warningText = Array.isArray(body.warnings) ? body.warnings.filter(Boolean) : [];
    const durationMinutes = Number.isFinite(Number(body.duration_minutes)) ? Math.max(5, Number(body.duration_minutes)) : Math.max(10, stack.length * 5);
    const runInsert = await insertRow(url, key, auth.accessToken, "session_runs", {
      user_id: auth.userId,
      session_template_id: "sessions-composer-prototype",
      duration_minutes: durationMinutes,
      strictness: "standard",
      persona_id: body.subject,
      safety_rules_applied: warningText.slice(0, 12),
      safety_warnings: warningText.slice(0, 12),
      status: "draft"
    });
    if (!runInsert.ok || !Array.isArray(runInsert.data) || !((_a = runInsert.data[0]) == null ? void 0 : _a.id)) {
      setResponseStatus(event, 500);
      return {
        ok: false,
        route: "/api/session/composer-save",
        code: "SESSION_RUN_INSERT_FAILED",
        message: "failed to insert session_runs row",
        debug: runInsert
      };
    }
    const sessionRunId = runInsert.data[0].id;
    const outputInsert = await insertRow(url, key, auth.accessToken, "session_outputs", {
      session_run_id: sessionRunId,
      output_type: "composer_preview",
      output_data: {
        subject: body.subject,
        stack,
        preview: body.preview || {},
        generated_at: (/* @__PURE__ */ new Date()).toISOString()
      },
      version: 1
    });
    const outputIds = outputInsert.ok && Array.isArray(outputInsert.data) ? outputInsert.data.map((row) => row == null ? void 0 : row.id).filter(Boolean) : [];
    const outputsBlocked = !outputInsert.ok;
    const blocker = outputsBlocked ? {
      table: "session_outputs",
      issue: `insert blocked by policy (${outputInsert.status})`,
      smallest_fix: "Add INSERT policy for authenticated users where session_outputs.session_run_id belongs to a session_runs row with user_id = auth.uid().",
      raw_error: outputInsert.data
    } : null;
    if (outputsBlocked) {
      setResponseStatus(event, 409);
    }
    return {
      ok: !outputsBlocked,
      route: "/api/session/composer-save",
      session_run_id: sessionRunId,
      session_output_ids: outputIds,
      save_status: {
        session_runs: "saved",
        session_outputs: outputsBlocked ? "blocked" : "saved"
      },
      blocker,
      temp_user_id: auth.userId,
      temp_user_email: auth.email
    };
  } catch (error) {
    setResponseStatus(event, 500);
    return {
      ok: false,
      route: "/api/session/composer-save",
      code: "UNHANDLED_ERROR",
      message: (error == null ? void 0 : error.message) || "unexpected error"
    };
  }
});

export { composerSave_post as default };;globalThis.__timing__.logEnd('Load chunks/routes/api/session/composer-save.post');
//# sourceMappingURL=composer-save.post.mjs.map
