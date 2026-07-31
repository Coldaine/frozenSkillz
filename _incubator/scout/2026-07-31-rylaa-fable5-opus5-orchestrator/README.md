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

Scored and decided: **adapt concept only**. See `analysis.md` for per-component rubric scores (A 4.4 / B 4.3 / C 2.3) and `decisions.md` for the decision.

Not adoptable as a plugin here — it hardcodes `python3` (absent from this machine's PATH) and is POSIX/tmux-bound. Its ledger and progressive-disclosure patterns are worth adapting; its tmux teammate-reaping layer is discarded.

No promotion is authorized yet: no live eval has been run, and `docs/workflows/external-skill-intake.md` requires one before any pattern from this candidate lands in `plugins/` or `docs/`.

The one empirical check run at import time was a portability probe (see `inventory.md` → Windows portability probe), because the upstream README declares the plugin macOS/Linux-only and this repo's operator is on Windows. That probe is a platform-fitness fact, not a quality eval — it does not satisfy the live-eval requirement in `docs/workflows/external-skill-intake.md`.
