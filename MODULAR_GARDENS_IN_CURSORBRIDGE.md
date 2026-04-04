# MODULAR_GARDENS_IN_CURSORBRIDGE.md

## PURPOSE
Hold the Modular Gardens workstream inside CursorBridge until a dedicated repo exists.

## WHAT BELONGS HERE NOW
- interactive flow mapping
- click-tree logic
- mock UI control rules
- handover packaging
- architecture notes that affect flow and shell behavior
- freeze-state references for approved mock screens

## WHAT DOES NOT BELONG HERE
- uncontrolled redesign of approved mock screens
- conversion into generic investor-deck structure when the task is mock-interactive
- replacing the explicit user tree with invented flow logic

## SOURCE OF TRUTH FOR FLOW
Use the user-provided explicit click tree as the logic source of truth.
Do not flatten it into generic feature groups.

## SOURCE OF TRUTH FOR LOOK / SHELL
Use:
- `CURSORBRIDGE_LAYOUT_FREEZE.md`
- approved screenshots / approved current file state

## FUTURE REPO TRANSFER RULE
When a dedicated Modular Gardens repo exists:
- copy this file into that repo
- keep `CANON_AGENT_SYSTEM.md` as the shared backbone
- create Modular-Gardens-specific AGENTS / freeze / change-request files there
- do not silently reinterpret the workstream during transfer
