# AGENTS.md

Read NORTH_STAR.md first. Do not infer intent from code.

Authority on conflict: NORTH_STAR > architecture > PROGRESS > AGENTS.
CLAUDE.md and README hold no authority of their own.

Route by task:
- Intent, scope, boundaries      → NORTH_STAR.md
- Architectural decision         → architecture.md, docs/decisions/
- Implement, fix, resume work    → PROGRESS.md (phase + safe-to-touch)
- Long procedure                 → docs/workflows/
- Historical context             → docs/history/
- Write or review docs           → invoke the project-docs skill
- Ending substantial work        → update PROGRESS.md (state, active, blockers, next)

If a task crosses a goal, anti-goal, pillar, or invariant: stop and surface it.

Commands: install `…` · test `…` · lint `…` · branch from main, PR to main
