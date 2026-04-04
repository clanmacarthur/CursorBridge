# CANON_AGENT_SYSTEM.md

## PURPOSE
Universal operating rules across repos.
Use this as the shared funnel for all future project-specific agent files.

## CORE MODE
- delta-first editing
- preserve approved baseline
- do not redesign unchanged areas
- verify before finalizing

## INSTRUCTION HIERARCHY
When instructions conflict, use this order:
1. current explicit user instruction in the active thread
2. current task file for the repo
3. layout freeze / change request files for the repo
4. repo chat-agent file
5. repo AGENTS.md
6. this canon file

## UNIVERSAL EDIT RULE
For UI or structured artifact work:
- identify approved baseline
- identify allowed edit region
- identify frozen regions
- apply smallest valid change
- reject drift

## UNIVERSAL DRIFT CHECK
Reject output if it:
- changes frozen regions
- increases empty space without purpose
- widens tabs or inflates spacing
- reintroduces hero / title drift
- replaces instead of editing
- converts interactive logic into a generic static format

## PATCHER MODE
When the user is iterating on an existing screen or file:
- behave as a strict patcher, not a re-designer
- preserve shell by default
- change only the requested region
- do not add new structure unless explicitly requested

## BUILDER MODE
When the user explicitly asks for net-new structure:
- still preserve any frozen baseline already approved
- separate new build areas from locked existing areas
- do not retroactively redesign approved regions

## WHEN USER IS FRUSTRATED OR SAYS STOP
- stop expanding scope immediately
- do not add theory unless directly asked
- answer the exact question or do the exact requested edit
- do not repeat back large summaries of the user's own point

## FILE DISCIPLINE
For each repo, prefer this stack:
- AGENTS.md
- project chat-agent file
- project layout freeze file
- project change request template
- current task file

## FUTURE MULTI-REPO MODEL
This canon file stays stable.
Each repo may override with project-specific files, but should still route through this funnel.
