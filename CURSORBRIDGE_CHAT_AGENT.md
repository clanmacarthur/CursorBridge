# CURSORBRIDGE_CHAT_AGENT.md

Purpose:
Rules specifically for chat-based editing passes.

Core rule:
Use strict delta-only editing.
Preserve approved baseline.
Do not redesign unchanged areas.

Required workflow:
1. Identify approved baseline
2. Identify allowed edit region
3. Identify frozen regions
4. Apply smallest valid change
5. Verify no drift

Frozen by default:
- header
- tabs
- spacing rhythm
- shell
- approved proportions
- approved row structure

Forbidden without explicit permission:
- hero blocks
- enlarged cards
- new rows
- global re-spacing
- filler text
- replacing instead of editing
