# Forensic Evaluation: Dispatching Parallel Agents Against Real-Agent Evidence

## Claim

- Claim being evaluated: Superpowers `dispatching-parallel-agents` reliably turns independent work
  into safe, portable, genuinely concurrent agent execution and integration.
- Candidate artifact: `source/skills/dispatching-parallel-agents/`
- Decision this finding informs: whether to adopt, adapt, defer, or discard the skill.

## Evidence Set

| Source | Type | Captured | Version or revision | Harness, model, and OS | Status | Result |
|---|---|---|---|---|---|---|
| [Pinned v6.1.1 skill](../../source/skills/dispatching-parallel-agents/SKILL.md) | direct source | 2026-07-23 | Superpowers 6.1.1; commit `d884ae0` | harness-neutral prose; model and OS not applicable | current | Strong independence, prompt-scope, and integration gates; contradictory 2+/3+ trigger; no lifecycle or isolation mechanism |
| [PR #948](https://github.com/obra/superpowers/pull/948) | source audit + proposed fix | 2026-07-23 | Superpowers v5-v6 source; PR head `bdf41c9` | Claude Code 1.0.33; Claude Opus 4.6; OS unknown | unresolved | Confirms the frontmatter says 2+ while the body says 3+; the one-line fix remains open |
| [PR #1470](https://github.com/obra/superpowers/pull/1470) and commit [`f0e5117`](https://github.com/obra/superpowers/commit/f0e5117fa6bdd2645485d2a8df8d7a107c4bf2af) | real-session report + code history | 2026-07-23 | pre-v5.1 report; instruction present by `f0e5117` and v6.1.1 | Claude API and Claude Code; model and OS unknown | fixed | A controller launched two agents in separate turns but called them parallel; the missing same-response instruction is fixed, but no post-change compliance run is persisted |
| Commits [`9ccce3b`](https://github.com/obra/superpowers/commit/9ccce3bf07a40e45259004a330409ba00970eff7) and [`1c53f5d`](https://github.com/obra/superpowers/commit/1c53f5deb62efeadaf1e9c924662b8f01c342692), plus [issue #350](https://github.com/obra/superpowers/issues/350) | code history + real-agent report | 2026-07-23 | Superpowers v5 context-isolation/SUBAGENT-STOP changes | Codex 0.89 report; model and OS unknown | fixed | Added the isolated-context principle and SUBAGENT-STOP behavior to address skill leakage; no transcript was preserved for the Codex report |
| [Pinned Codex adapter](../../source/skills/using-superpowers/references/codex-tools.md) | direct source + current tool-contract inspection | 2026-07-23 | Superpowers 6.1.1; commit `d884ae0` | Codex CLI 0.145.0; model identifier unknown; Windows | current | Adapter enables agent tools but contains no history/fork control that enforces the skill's “never inherit” guarantee |
| [Issue #1633](https://github.com/obra/superpowers/issues/1633) and [PR #1662](https://github.com/obra/superpowers/pull/1662) | conflicting investigation + direct Codex session | 2026-07-23 | Superpowers 5.1.0-v6.1.1; PR head `85e3215` | Codex CLI 0.133.0 on macOS and Codex Desktop 0.115.0-era surface; GPT-5.5; Desktop OS unknown | unresolved | One report was closed as a runtime ambiguity; the open PR records deferred tool discovery after an initial false “unavailable” conclusion |
| [Issue #1927](https://github.com/obra/superpowers/issues/1927) and [PR #1982](https://github.com/obra/superpowers/pull/1982) | source-backed lifecycle report + proposed fix | 2026-07-23 | Superpowers 5.1.3-v6.1.1; PR head `35769a1` | Codex CLI 0.142.5 with GPT-5.5 on Linux; Codex v2 source has no model or OS context | unresolved | Codex v1 retained finished workers until close; v2 may expose no close operation; the skill has no neutral release step |
| [Issue #597](https://github.com/obra/superpowers/issues/597) | real-user environment report + maintainer triage | 2026-07-23 | Superpowers version unknown | parallel worktrees; harness, model, and OS unknown | current | Parallel sessions can collide on shared ports and databases; maintainer assigns the isolation recipe to project instructions rather than core |
| [Issue #473](https://github.com/obra/superpowers/issues/473) | paired real-agent report | 2026-07-23 | Superpowers version unknown | Claude Code; harness version, model, and OS unknown | unclear | A verification worker proceeded while a development worker paused for permission; maintainer classified autonomy as platform behavior and no transcript is linked |
| [PR #1934](https://github.com/obra/superpowers/pull/1934) | source critique + merged deletion on `dev` | 2026-07-23 | Superpowers 6.1.1/current `main`; merged `dev` head `67714e0` | source-only critique; harness, model, and OS not applicable | current | Removes the “time of one,” benefits recap, and dated success story as social proof on `dev`; v6.1.1 and current `main` still share the old blob and retain the unaudited claims |
| [Issue #429](https://github.com/obra/superpowers/issues/429) | feature request + maintainer/community discussion | 2026-07-23 | Superpowers version unknown | Claude Code Agent Teams; models and OS unknown | current | Confirms coordinated teams are a separate, unresolved workflow; this does not invalidate the skill's narrower independent fan-out scope |

## Assessment

- Status: unresolved. The core independence pattern is current and useful, but activation,
  portability, context isolation, resource isolation, and worker lifecycle remain inconsistent or
  harness-dependent.
- Corroborating evidence: pinned source, code history, open fixes, Codex tool-contract observations,
  real-agent issue reports, and maintainer triage.
- Contradicting evidence: the skill's dated success story and users reporting useful parallel work
  show the pattern can succeed, but no persisted run supports the claimed speed or failure rate.
- Confidence: moderate.
- Supports: C+ editorial grade, adapting the independence/prompt/integration gates, continued review.
- Does not support: a measured speedup, universal context isolation, a current failure rate, or
  wholesale rejection of parallel agents.

## Reviewer Notes

Current source defects receive more weight than closed platform reports. Agent Teams are treated as
a different coordination model, not a missing requirement for independent fan-out. The local Codex
setting enables multi-agent support today, but actual tool discovery and lifecycle semantics remain
version-sensitive and must be inspected rather than inferred from configuration alone.
