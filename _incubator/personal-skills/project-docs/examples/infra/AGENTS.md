# AGENTS.md

Read NORTH_STAR.md first. Do not infer intent from code or manifests.

Authority order: NORTH_STAR > architecture.md > PROGRESS.md > AGENTS.md. Downstream never overrides upstream.

## Route by task

- Understand intent, scope, boundaries → NORTH_STAR.md
- Make a technical or architectural decision → NORTH_STAR.md (goals, anti-goals), architecture.md, docs/decisions/ (add an ADR if durable)
- Change the VM substrate → tofu/, docs/components/substrate.md
- Change the cluster (nodes, bootstrap) → talos/, docs/components/talos.md
- Change shared services (ingress, secrets, storage, db) → platform/, docs/components/platform.md
- Add or change a workload → apps/, docs/components/apps.md
- Pick up active work, blockers → PROGRESS.md
- Run a long procedure (bootstrap, disaster recovery) → docs/workflows/
- Look up completed or abandoned work → docs/history/
- Write or review documentation → invoke the project-docs skill
- Anything crossing a goal, anti-goal, pillar, or invariant → Stop. Surface the conflict. Discuss with the operator.

## Commands

- Provision substrate: `tofu -chdir=tofu apply`
- Bootstrap cluster: `talosctl apply-config ...` then `talosctl bootstrap`
- Check reconcile status: `kubectl get -A <reconciler resources>`
- Diff repo vs cluster: `<reconciler> diff`

## Working rules

- No hand-edited live state. Changes land as commits and reconcile; `kubectl edit` on live objects is reverted.
- Manifests only in tofu/, talos/, platform/, apps/. No prose docs there; docs live in the doc homes. A one-line pointer is the only exception.
- No undocumented architectural decisions. A change that picks storage, database, ingress, or secrets strategy needs an ADR.
- Status means applied, not authored. Do not mark a manifest Current in architecture.md until it reconciles.
- Branch from main; PR to main; the reconciler tracks main.

## Handoff

Before ending substantial work, update PROGRESS.md (current state, active work, blockers, next focus, links to new ADRs). Roll completed items into docs/history/.

## Compatibility

CLAUDE.md contains only `@AGENTS.md` and `@NORTH_STAR.md`. No prose, no header.
