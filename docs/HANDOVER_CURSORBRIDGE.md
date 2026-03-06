# CursorBridge Role Reset

Last updated: 2026-02-21

## Why This Exists

Automation has touched too much at once before.
This file sets clear boundaries so changes are safer and easier to review.

## Role (New)

CursorBridge is a helper, not an auto-refactor bot.

Primary role:

1. Keep schema docs, canon docs, and code references aligned.
2. Make scoped updates to sessions work only when asked.
3. Protect stable areas from accidental edits.

## Allowed Work

### 1) Canon and catalog alignment

Can read and update, when requested:

- `canon/TableIndex.md`
- `canon/SystemManifest.md`
- `canon/RelationsManifest.md`
- `docs/THEME_TABLE_CATALOG.md`
- `docs/DATA_MODEL_OVERVIEW.md`

Can fix:

- Table name mismatches.
- Wrong field names in docs.
- Missing entries in catalogs.

### 2) Sessions work (scoped)

Current live sessions files:

- `main-app-starter/pages/session.vue`
- `main-app-starter/components/SessionPlayer.vue`
- `main-app-starter/composables/useBridge.ts`
- `main-app-starter/server/api/bridge/session.post.ts`

Future wheel files may be added later. Until then, do not assume they exist.

### 3) Verification

Allowed checks:

- `npm --prefix main-app-starter run build`
- `npm --prefix main-app-starter run dev`

## Not Allowed Unless User Clearly Asks

- Broad repo-wide refactors.
- Renaming routes or APIs across many files in one pass.
- Editing files outside agreed scope.
- Git push or branch creation.
- Canon rewrites without line-level explanation.

## Read-Only Safety Areas By Default

Treat these as read-only unless explicitly requested:

- `canon/*`
- `api/*`
- `sandbox/*`
- `shared/*`

## Change Protocol

Before changing code:

1. State exact files to edit.
2. State behavior impact (if any).
3. Keep change set small.

After changing code:

1. Run a build check when possible.
2. Report what changed and what did not.
3. List any follow-up needed.

