# Sessions Handover

Last updated: 2026-02-21
Master doc: `docs/SESSIONS_MASTER.md`

## Purpose

This file is a short operational handover.
For full merged detail, use `docs/SESSIONS_MASTER.md`.

## Current State In This Repo

Today, the live Nuxt page is:

- Route: `/session`
- File: `main-app-starter/pages/session.vue`

Today, session generation goes through a proxy:

- `main-app-starter/server/api/bridge/session.post.ts` -> `POST /sandbox/generate-session`

Today, there is no checked-in wheel UI in `main-app-starter`.
ThemeGraph server loading has started in this repo.

There is now a planned-route placeholder page and session API path:

- `main-app-starter/pages/sessions.vue`
- `main-app-starter/server/api/session/themes.get.ts`
- `main-app-starter/server/api/session/preview.post.ts`
- `main-app-starter/server/api/session/generate.post.ts`

Current endpoint status:

- `GET /api/session/themes`: wired to Supabase theme graph loading.
- `POST /api/session/preview`: stub, but contract keys aligned.
- `POST /api/session/generate`: stub, but contract keys aligned.

## Target State We Are Planning

We are planning a richer session builder where users can:

- Pick a template.
- Pick linked themes across domains.
- See linked circular controls ("wheels") and optional inner rings for extra attributes.
- Preview and generate a session with theme context.

Planned route and APIs:

- Route: `/sessions` (future)
- `GET /api/session/themes` (phase 1 started)
- `POST /api/session/preview` (future logic)
- `POST /api/session/generate` (future logic)

## Naming Rules (Important)

Use these words consistently:

- "Session page" = the current page at `/session`.
- "Sessions builder" = the planned wheel page at `/sessions`.
- "Wheel UI" = visual selectors only.
- "Theme graph" = data model that links one domain to another.
- "Lens and meta-lens" = explanation style layer, not timeline timing.

Do not call the current `/session` page a wheel page.
Do not assume wheel code exists unless files are added.

## Invariants (Must Not Break)

- Keep core generation flow working through sandbox while migration is in progress.
- Do not break current Nuxt app routes.
- Do not treat draft docs as implemented code.
- Keep canon manifests as source references until code is updated.

## Parked Features (Still Planned)

- Multi-ring inner attributes per domain.
- Smart ring sizing and label handling.
- Curved/splayed label rendering.
- Supabase-first complete table coverage, then Convex migration.

## Immediate Build Order

1. Keep current `/session` working.
2. Lock schema for `controls_library` and `user_profiles` first.
3. Finish table catalog and data model mapping docs.
4. Add ThemeGraph server layer in code.
5. Add `/sessions` UI on top of that server layer.
6. Add Convex adapter only after Supabase coverage is complete.

## Programmes Note

Programmes (scheduled tasks over days to months) are intentionally parked for later.
They should be added on top of stable single-session runtime logic.
