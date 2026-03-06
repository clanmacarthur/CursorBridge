# Main App Starter (Nuxt 3)

This is the example Nuxt app inside this repo.

## Current Routes

- `/` home page
- `/login` login page
- `/dashboard` dashboard page
- `/session` session generator + player
- `/sessions` planned wheel builder placeholder (contract stub)

Note:

- `/sessions` (plural) is a placeholder route in this code.
- The real, live generation flow is still `/session` until wheel logic is implemented.

## Run Locally

From repo root:

```bash
npm --prefix main-app-starter install
npm --prefix main-app-starter run dev
```

Nuxt runs on port `8080` by default (see `main-app-starter/package.json`).

## Build Check

```bash
npm --prefix main-app-starter run build
```

## Bridge Proxy Endpoints In This App

- `main-app-starter/server/api/bridge/templates.get.ts`
- `main-app-starter/server/api/bridge/templates/[id].get.ts`
- `main-app-starter/server/api/bridge/query/[table].get.ts`
- `main-app-starter/server/api/bridge/session.post.ts`

## Planned Session Contract Stubs

- `main-app-starter/server/api/session/themes.get.ts`
- `main-app-starter/server/api/session/preview.post.ts`
- `main-app-starter/server/api/session/generate.post.ts`

## Related Docs

- `../docs/HANDOVER_SESSIONS.md`
- `../docs/HANDOVER_CURSORBRIDGE.md`
- `../docs/DATA_MODEL_OVERVIEW.md`
- `../docs/THEME_TABLE_CATALOG.md`
