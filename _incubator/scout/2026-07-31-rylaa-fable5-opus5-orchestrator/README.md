# Scout: fable5-opus5-orchestrator

Token-frugal multi-agent orchestration plugin for Claude Code. A Fable 5 "chair" plans and decides; Sonnet 5 carries bulk work; Opus 5 takes hard slices and escalations. Discipline is enforced mechanically by a Requirements Ledger file plus four guard hooks.

Imported as an intake candidate at operator request ("good skill for intake"). No promotion decision has been made.

## Provenance

| Field | Value |
|---|---|
| Source URL | https://github.com/Rylaa/fable5-opus5-orchestrator |
| Commit | `828974b4998a6f24b0a56c635e3e090309a417a7` |
| Commit date | 2026-07-25T16:43:13+03:00 |
| Commit subject | `feat!: v0.15.0 — progressive disclosure: slim cores + playbook skill; token diet` |
| Plugin version | 0.15.0 |
| Import date | 2026-07-31 |
| License | MIT (Copyright (c) 2026 Yusuf Demirkoparan) |
| Author | Yusuf Demirkoparan (@Rylaa) |
| Repo stats at import | 28 stars, 9 forks, 32 commits, 0 open issues |
| Reviewer | intake agent |
| Scout path | `_incubator/scout/2026-07-31-rylaa-fable5-opus5-orchestrator/` |

Clone was `--depth 1`; `.git` was removed after recording the commit SHA above, so `source/` is a flat read-only snapshot.

## Snapshot layout

```text
source/                       # read-only evidence, 22 files, 252K
  .claude-plugin/             # plugin.json + marketplace.json
  .github/workflows/ci.yml
  hooks/hooks.json            # 4 hook registrations
  instructions/               # 2 core profiles + 2 switch deltas
  scripts/                    # 5 python hook scripts (~1790 LOC)
  skills/playbook/SKILL.md    # the delegation contract
  tests/                      # pytest suite (~2160 LOC)
  LICENSE, README.md
```

`source/` is read-only after import. Do not edit it to "improve" the candidate.

## Status

Scored and decided: **adapt concept only**. See `analysis.md` for per-component rubric scores (A 4.4 / B 4.4 / C 2.3) and `decisions.md` for the decision.

Not adoptable as a plugin here — it hardcodes `python3` (absent from this machine's PATH) and is POSIX/tmux-bound. Its ledger and progressive-disclosure patterns are worth adapting; its tmux teammate-reaping layer is discarded.

No promotion is authorized. One live eval has now been run and persisted at
`evals/runs/2026-07-31-spawn-prompt-richness.md`, and its result reinforces the no-promotion
decision rather than lifting it. It establishes two things — default spawn prompts (1298–1378
chars) sit *below* the guard's 1500-char gate, so the hook is near-inert as shipped; and the guard
is portable to Windows with a one-line `python3` → `py -3` fix. It does **not** establish any
comparative improvement: the candidate arm was measured with an instrument blind below the
threshold, so that question is unresolved. See that file's "Status against the intake evaluation
protocol" section for what it can and cannot be cited for.

The one empirical check run at import time was a portability probe (see `inventory.md` → Windows portability probe), because the upstream README declares the plugin macOS/Linux-only and this repo's operator is on Windows. That probe is a platform-fitness fact, not a quality eval — it does not satisfy the live-eval requirement in `docs/workflows/external-skill-intake.md`.

## What was done

1. **Snapshot + provenance.** Cloned at `828974b`, `.git` stripped, `source/` read-only throughout.
2. **Safety audit** of all five scripts. No network calls, no `shell=True`, no `eval`/`exec`/`pickle`. `tmux kill-server` scoped to `claude-swarm-*` sockets only; `kill-pane` requires `--agent-id` plus an exact `--parent-session-id` match. Hooks fail open on malformed input (verified by piping garbage: exit 0).
3. **Windows portability probe.** Full pytest suite: 118 passed / 34 failed; 21 of 34 from `os.getuid` in the reaping layer.
4. **Rubric scoring** as three components, because their value diverges too far to average into one number.
5. **Sandbox install.** Project-scoped hooks driven through a real headless Claude Code 2.1.220 session on Windows, with `python3` → `py -3`.
6. **Live eval** — `evals/runs/2026-07-31-spawn-prompt-richness.md`, control instrument at `evals/cases/probe.py`.
7. **Eval self-correction.** Review found the candidate arm was instrumented with the guard's own `_metric()`, which is left-censored at the threshold. The comparative result was withdrawn. See that file.
8. **Adapted the identified gap** into `extracted-patterns/delegation-handoff-contract.md` — not promoted, not active.

## What changed during the work

Findings that reversed, recorded because the reversals are the useful part:

- **"It cannot run on Windows" was too broad.** True of the plugin; false of the spawn guard, which needed one interpreter name changed. Component B portability 3 → 4, on observation rather than inference.
- **The `python3` diagnosis was misstated.** This machine has Python 3.13.14 — it has no binary *named* `python3`, which is a Unix convention Windows never adopted. The failure generalizes to every stock Windows box rather than being local. See `inventory.md`.
- **A claimed comparative result was withdrawn.** An earlier draft reported prompts growing ~47% under the guard and treated that as refuting the predicted perverse incentive. The instrument could not observe sub-threshold prompts, so it could not have detected the predicted effect in the first place. That question is **unresolved, not answered.**
- **The surviving results are narrower and hold up:** default spawn prompts (1298–1378) sit below the 1500 gate, so the hook is near-inert as shipped; and it is Windows-portable with a one-line fix. The no-promotion recommendation rests only on these.
