---
name: project-docs
description: >
  Create, review, reconcile, and migrate the project authority documents
  (NORTH_STAR.md, architecture.md, PROGRESS.md, AGENTS.md) and the
  overflow subdirectories that support them (docs/decisions, docs/components,
  docs/workflows, docs/history). Use whenever a repo needs its documentation
  pattern established, audited, reconciled, or repaired. This skill is the
  authoring-time enforcer for the project authority stack; the future
  Guardian runtime is downstream and out of scope here. Trigger when the
  user mentions any of these documents by name, asks to bootstrap a repo's
  docs, asks to review or audit existing docs, asks to migrate an existing
  CLAUDE.md / instructions file to AGENTS.md, or asks how to keep the docs
  consistent with each other.
---

# Project Docs Authoring

<context>
A repo's documentation pattern has an authority hierarchy:
NORTH_STAR (intent) → architecture (technical strategy and shape) →
PROGRESS (current handoff) → AGENTS (agent operating contract).
This skill creates, reviews, reconciles, and migrates those documents.
It produces drafts, edit plans, review findings, and authority-flow
notes. It does not block PRs, run CI, assign severity, or enforce
policy; that belongs to the future Guardian runtime.

Authority flows one direction. When a downstream doc disagrees with
an upstream doc, the downstream doc is always the wrong one.

AGENTS.md is a pure router, not a container. It states the authority
order, routes each task category to the doc that owns it, lists the
commands, and stops there. The project's identity is eager-loaded from
NORTH_STAR; everything else is reached through lazy bare-path routes the
agent follows only when a task needs them. Inlining content into
AGENTS.md instead of routing to it is the pattern's most common failure;
the default is to inline nothing and route everything, and any AGENTS.md
that holds doctrine of its own is a finding.
</context>

<task_router>

Identify the task and load the appropriate references.

| User wants to... | Load these files |
|---|---|
| Create a new authority doc that does not exist | `references/write-workflow.md` + the relevant doc guide below |
| Review or critique an existing authority doc | `references/review-checklist.md` + the relevant doc guide below |
| Reconcile multiple docs against each other | `references/authority-flow.md` |
| Migrate a repo's existing instructions into the AGENTS.md pattern | `references/agents-md-guide.md` + `references/write-workflow.md` |
| Understand the relationship to the future Guardian | `references/guardian-relationship.md` |

Per-document guides (load when working on that specific doc):

| Doc | Guide |
|---|---|
| NORTH_STAR.md | `references/north-star-guide.md` |
| architecture.md | `references/architecture-md-guide.md` |
| PROGRESS.md | `references/progress-md-guide.md` |
| AGENTS.md | `references/agents-md-guide.md` |

Exemplars (open when drafting a new doc to see what "good" looks like):
`examples/NORTH_STAR.md`, `examples/architecture.md`, `examples/PROGRESS.md`,
`examples/AGENTS.md`, `examples/CLAUDE.md`.

For an infrastructure / GitOps repo (manifests are the implementation, and
status means applied-not-authored), see the parallel set under `examples/infra/`:
`examples/infra/NORTH_STAR.md`, `examples/infra/architecture.md`,
`examples/infra/PROGRESS.md`, `examples/infra/AGENTS.md`, `examples/infra/CLAUDE.md`.

</task_router>

<scope>

The skill covers four primary documents and four overflow destinations.

Primary documents:
- `NORTH_STAR.md` — project intent, goals, anti-goals, pillars
- `architecture.md` — technical strategy, system shape, invariants
- `PROGRESS.md` — current handoff state, blockers, next-session focus
- `AGENTS.md` — agent entrypoint and operating contract

Overflow destinations (legal homes for content expelled from the four primaries):
- `docs/decisions/` — ADRs (durable decisions with rationale)
- `docs/components/` — deep subsystem documentation
- `docs/workflows/` — long procedures and agent workflows
- `docs/history/` — archived progress, completed milestones

Documentation lives only in the authority docs and these overflow homes.
Implementation directories hold implementation, not prose docs: a stray
README or design note in a source or manifest directory is content without a
legal home, and it belongs in one of the doc destinations above. A one-line
pointer file that routes to the real doc is the only exception.

The skill does NOT create or rewrite docs unless the user asks. It surfaces
findings, drafts, and suggested edits. Neighboring docs are never silently
rewritten as a side effect of working on one doc.

</scope>

<minimum_viable_stack>

Do not create all four primary documents merely to satisfy the pattern.

- `AGENTS.md` is always recommended.
- `NORTH_STAR.md` is needed when project intent is non-obvious or drift-prone.
- `PROGRESS.md` is needed when work spans sessions.
- `architecture.md` is needed when technical structure or intended direction is complex enough to go stale or be misunderstood.

A new repo can start with `AGENTS.md` alone and accrete the others as need
becomes evident. The skill should not push for completeness.

</minimum_viable_stack>

<output_types>

The skill returns one of:

- a proposed document draft
- a patch-style edit plan
- a review report
- an authority-flow summary
- a migration recommendation

Findings cite the relevant doc section. Suggested edits are concrete.

</output_types>

<vocabulary>

Use skill vocabulary, not Guardian vocabulary. The Guardian runtime is
a separate, downstream system.

| Skill (authoring time) | Guardian (PR / runtime) |
|---|---|
| finding | violation |
| review note | severity |
| conflict | blocker |
| alignment issue | policy violation |
| authority-flow check | enforcement |
| suggested edit | CI failure / PR gate |

See `references/guardian-relationship.md` for the boundary.

</vocabulary>

## Learnings

### 2026-06-29

#### What Worked
- When PROGRESS reflects **verified live cluster state** (kubectl + helmfile diff) and parallel workstreams, keep it — it earns its place as handoff.
- When PROGRESS drifts into changelog + second roadmap contradicting the active plan (`docs/plans/*.md`), **gut the diary**, add a Status block to the plan, and shrink PROGRESS to pointers — don't delete handoff entirely.
- Template/advice questions: score options against **accepted ADRs and live artifacts** (Phase 0 history, capability registry), not generic homelab comparison tables.

#### What Failed
- Recommending "delete PROGRESS" while the doc had just been reconciled to live secrets/cluster state — created conflicting advice in the same session.
- Stating cluster blockers (e.g. "KubeBlocks degraded") from PROGRESS alone without `kubectl` on the session machine — user pushback ("how do you know?") was correct.

#### Configuration Notes
- Pre-implementation with one active plan: plan Status block may suffice; post–wave-A/B with secrets cutover and open PRs: PROGRESS + `docs/components/*.md` live inventory are worth maintaining.
- Durable outcomes belong in ADRs + component docs; PROGRESS "Recently Changed" should roll off after merge, not accumulate.
