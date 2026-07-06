# architecture.md

## Architecture Thesis

This project is built as a local-first documentation-governance system for agentic coding workflows.

The core architectural bet is that project drift is best controlled by keeping a small set of authority documents in the repo, while allowing a future Guardian runtime to mirror and evaluate those documents outside the repo.

## Status Legend

- **Current** — implemented or directly reflected in the repo.
- **Planned** — decided direction, not fully implemented.
- **Candidate** — plausible option, not decided.
- **Deferred** — intentionally not being built now.

## System Shape

| Area | Status | Approach |
|---|---|---|
| Documentation skill | Current | A skill guides agents through creating, reviewing, and reconciling project docs. |
| Authority docs | Planned | The repo uses `NORTH_STAR.md`, `architecture.md`, `PROGRESS.md`, and `AGENTS.md`. |
| Claude compatibility | Planned | `CLAUDE.md` should import `AGENTS.md` and not contain unique doctrine. |
| Guardian runtime | Deferred | A later runtime may inspect PRs or repo changes for drift against the authority docs. |
| Off-repo governance store | Candidate | A mirrored North Star / history store may live outside the repo to reduce self-modification risk. |

## Key Technical Differentiator

The differentiator is not “more documentation.”

The differentiator is **structured authority**:

- `NORTH_STAR.md` owns intent.
- `architecture.md` owns technical strategy and system shape.
- `PROGRESS.md` owns handoff state.
- `AGENTS.md` owns agent operating instructions.
- ADRs own durable decisions.

Agents are not asked to read everything. They are routed to the right authority for the kind of question they are answering.

## Target Architecture

```text
                 AGENTS.md
          agent entrypoint / rules
                    │
                    ▼
 ┌─────────────────────────────────────┐
 │       Project Authority Docs         │
 │                                     │
 │  NORTH_STAR.md  →  architecture.md  │
 │         │                │           │
 │         ▼                ▼           │
 │    PROGRESS.md      docs/decisions/  │
 └─────────────────────────────────────┘
                    │
                    ▼
          future Guardian runtime
       drift review / PR review / memory
```

## Current Architecture

The current implementation is a documentation-pattern skill, not the Guardian runtime.

The skill performs:

1. document inventory
2. task classification
3. per-document generation or review workflow
4. authority-flow check
5. suggested edits or review findings

## Major Components

| Component | Status | Responsibility | Detail |
|---|---|---|---|
| `project-docs/SKILL.md` | Planned | Top-level workflow router for documentation tasks | `docs/workflows/project-docs-skill.md` |
| `references/north-star.md` | Current | North Star writing/review rules | `docs/components/north-star-branch.md` |
| `references/agents.md` | Planned | AGENTS.md guidelines and anti-patterns | `docs/components/agents-branch.md` |
| `references/architecture.md` | Planned | Architecture.md writing/review rules | `docs/components/architecture-branch.md` |
| `references/progress.md` | Planned | Progress handoff rules | `docs/components/progress-branch.md` |
| Guardian runtime | Deferred | Future repo/PR drift detection system | `docs/components/guardian-runtime.md` |

## Architectural Invariants

- `AGENTS.md` must remain a router and operating contract, not a giant documentation index.
- `architecture.md` may include target architecture, but forward-looking claims must be labeled.
- `PROGRESS.md` must remain a handoff window, not a permanent project diary.
- Durable architecture decisions belong in ADRs, not buried in progress notes.
- The skill must not pretend to be the Guardian runtime.

## ADR Index

| ADR | Status | Summary |
|---|---|---|
| `docs/decisions/0001-use-agents-md.md` | accepted | Use `AGENTS.md` as the cross-tool agent entrypoint. |
| `docs/decisions/0002-claude-md-shim.md` | proposed | Reduce `CLAUDE.md` to the two-line eager-load stub: `@AGENTS.md` + `@NORTH_STAR.md`. |
| `docs/decisions/0003-skill-vs-guardian.md` | proposed | Keep the documentation skill separate from the future Guardian runtime. |

## Open Architecture Questions

- Should the Guardian mirror authority docs into an orphan branch, a separate repo, or an external store?
- Does the future Guardian run as a CLI, GitHub Action, local hook, or all three?
- Should doc review findings be advisory only, or can they become blocking in PR contexts?

## Links

- `NORTH_STAR.md` — project intent
- `PROGRESS.md` — current status
- `AGENTS.md` — agent entrypoint
- `docs/decisions/` — architectural decisions
- `docs/components/` — subsystem documentation
- `docs/workflows/` — longer operating procedures
