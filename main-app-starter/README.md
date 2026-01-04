# Main App Starter (EXAMPLE ONLY)

**This is just example code. Main App connects DIRECTLY to Supabase.**

CursorBridge does NOT need to be running for Main App to work.

---

## The Architecture

```
Main App  ──────────────►  Supabase (direct connection)

CursorBridge = separate admin tool (optional, for content authoring)
```

---

## What Main App Needs

1. Supabase URL + Anon Key
2. `@supabase/supabase-js` package
3. A composable like `useSupabase.ts`

See `MAIN_APP_INTEGRATION_PACKAGE.md` in the parent folder for complete code.

---

## This Folder

This folder contains EXAMPLE components you can reference:

- `composables/useBridge.ts` - Example API patterns (adapt for direct Supabase)
- `components/SessionPlayer.vue` - Example session player UI
- `types/index.ts` - TypeScript interfaces

**Copy what's useful, ignore the rest.**

---

## CursorBridge Role

CursorBridge is a standalone admin tool for:
- Syncing Notion ↔ Supabase
- Creating database schemas
- Running Excel automation
- Seeding content

**It does NOT need to run for Main App to function.**
