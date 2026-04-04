# CANON_AGENT_SYSTEM_ADDITIONS.md

## ACTIVATION PREFIX
Use this short prefix to activate strict patcher mode in chat:

`DELTA ONLY. File: [file name]. Frozen: [what must not change]. Change: [exact thing to edit].`

Meaning:
- `File` = where to work
- `Frozen` = what must not change
- `Change` = the only allowed edit

## DRIFT-CHECK PROTOCOL
Before any UI or structured artifact edit:
1. identify approved baseline
2. identify allowed edit region
3. identify frozen regions
4. apply smallest valid change
5. check rendered or resulting output
6. reject output if drift appears

Drift includes:
- changed frozen regions
- increased empty space without purpose
- widened tabs or inflated spacing
- hero / title drift
- replacing instead of editing
- converting interactive logic into a generic static format

## README POINTER SNIPPET
Use this exact block in README.md:

```md
## Agent control files

For active build/edit behavior, use these files as source of truth:

- `CANON_AGENT_SYSTEM.md`
- `CANON_AGENT_SYSTEM_ADDITIONS.md`
- `AGENTS.md`
- `CURSORBRIDGE_CHAT_AGENT.md`
- `CURSORBRIDGE_LAYOUT_FREEZE.md`
- `CURSORBRIDGE_CHANGE_REQUEST_TEMPLATE.md`
- `CURSORBRIDGE_CURRENT_TASK.md`

Do not rely on README for active edit rules. README is only the pointer.
```
