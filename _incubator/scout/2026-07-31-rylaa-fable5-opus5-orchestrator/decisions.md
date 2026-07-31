# Decision Log: fable5-opus5-orchestrator

## Decision

- Date: 2026-07-31
- Reviewer: intake agent
- Artifact paths:
  - Keep as concept: `source/skills/playbook/SKILL.md`, `source/instructions/dynamic-workflow-fable.md` (Rule 1), the `LEDGER.md` checkbox grammar
  - Defer: `source/scripts/ledger_guard_spawn.py`
  - Discard: `source/scripts/inject_instructions.py`, `source/scripts/cleanup_session_cache.py`, reaping half of `source/scripts/ledger_guard_stop.py`, all model-tier routing
- Outcome: **adapt concept only** (Component A) + **discard** (Component C) + **incubate for later** (Component B)
- Affected frozenSkillz paths: none yet — no promotion is authorized until a live eval exists

## Evidence

- Inventory summary: `inventory.md`
- Rubric score summary: `analysis.md` — Component A 4.4, Component B 4.3, Component C 2.3
- Eval run paths: **none** — no live eval has been run; this blocks promotion
- Safety notes: no network, no `shell=True`, no `eval`/`exec`/`pickle`; hooks fail open. `tmux kill-server` scoped to `claude-swarm-*` sockets only; `kill-pane` requires `--agent-id` plus exact `--parent-session-id` match. Destructive surface is real but narrow and defensively written.
- Maintenance notes: MIT, single author, 32 commits, active as of 2026-07-25. Component C couples to undocumented host internals (`--agent-id`, `--parent-session-id`, `claude-swarm-*` socket names, `@session-` pane tags, `settings.json` model field) that have already changed once upstream, forcing version-proofing code.

## Rationale

Whole import was ruled out on three independent grounds, any one sufficient:

1. **It cannot execute in this environment.** `hooks/hooks.json` hardcodes `python3`, which is not on this machine's PATH (only `python`). Upstream declares macOS/Linux only. Windows probe: 118 passed / 34 failed, with 21 of 34 failures tracing to `os.getuid`.
2. **Its most complex half is its most fragile half.** Component C holds all the destructive behavior *and* all the undocumented-internals coupling, and has already required rework from upstream drift. Adopting it would import a maintenance liability that breaks on someone else's release schedule.
3. **Its central claim is unevidenced.** No model evals ship with the plugin, and the author concedes the hooks verify "existence and checkbox state, not fidelity" — a shallow ledger passes.

The concepts, however, are cleanly separable from the code that fails, platform-independent, and directly relevant to how this repo already works. Component A scored 4.4 on the shared rubric with its only weak dimension being the same missing-eval gap noted above.

Component B (`ledger_guard_spawn.py`) is deliberately parked rather than discarded: it is pure Python, couples only to the *public* hook contract, passes 40/42 tests on Windows already, and degrades on purpose for non-POSIX (`except ImportError: fcntl = None`). It is a credible future port if repeated manual pain ever justifies one. The intake workflow forbids adding it now — "Do not add scripts for intake v1 unless repeated manual pain has been observed and documented."

## Follow-Up

- Owner: unassigned
- Due date or trigger: before any Component A pattern is written into `plugins/` or `docs/`
- Required validation: a persisted live eval under `evals/runs/` comparing baseline / candidate-inspired / frozenSkillz-adapted output, per `docs/workflows/external-skill-intake.md`. Until then this candidate stays in `_incubator/` and no tracker row claims it as active.
