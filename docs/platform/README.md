# Platform Planning Router

This directory contains planning material for extending frozenSkillz beyond its
current marketplace/intake boundary. It does not change current repository authority,
activate content, install skills, or claim that a control plane exists.

## Start here (2026-07-21)

**Proposed critical path:** [REFINED-V1.md](REFINED-V1.md) — challenge of the July 16
pack, thin v1 for persisting/managing agent configuration, and explicit non-goals.

**Operator workflow (proposed):** [../workflows/project-agent-config.md](../workflows/project-agent-config.md)

**Already authoritative for skill sync:** [../workflows/skill-authority-and-frozen-sync.md](../workflows/skill-authority-and-frozen-sync.md)

The July 16 three phase plans and `evidence/` pack remain as **appendix / backlog**.
They are not the implementation sequence for v1.

## How the documents hang together

```text
                    REFINED-V1 (proposed critical path)
                              |
          +-------------------+-------------------+
          |                                       |
          v                                       v
 project-agent-config.md              skill-authority-and-frozen-sync.md
 (commit native files per project)    (reviewed skills -> ~/.agents/skills)
          |
          v
 evidence/ + plans/01-03   (July 16 pack: traceability + deferred backlog)
          |
 explicit user approval of REFINED-V1 decisions RV1-01..07
          |
          v
 tracker / manifests / sync script / further implementation PRs
```

The `evidence/` documents are appendices joined by stable decision, requirement,
acceptance, failure, gap, and phase IDs. They remain non-authoritative even though
they live in the repository. Start with
[the evidence-pack index](evidence/README.md) only when auditing the July 16 source.

The `plans/` directory is the **deferred** full control-plane sequence (kept for
history and later backlog), not the v1 critical path:

1. [Plan 1: design closure, authority, and distribution](plans/01-design-closure-authority-and-distribution.md) — superseded for v1 by REFINED-V1
2. [Plan 2: local control plane and client runtime](plans/02-local-control-plane-and-client-runtime.md) — backlog
3. [Plan 3: conformance, integrations, and pilot](plans/03-conformance-integrations-and-pilot.md) — deferred

## Relationship to current repository authority

Until REFINED-V1 (or a successor) is explicitly approved and its changes are
implemented, the existing authority order remains unchanged:

1. `docs/skill-review/tracker.md` governs active, gated, scout, and promotion status.
2. `docs/workflows/external-skill-intake.md` governs external evaluation.
3. Active files under `plugins/frozen-skills/skills/` define installable behavior.
4. `docs/workflows/skill-authority-and-frozen-sync.md` describes the current
   personal-live-to-reviewed-frozen relationship and the sync script contract.
5. Current plugin manifests and marketplace catalogs define repository metadata and
   publication claims; verified install/discovery support remains a separate matrix.

The planning evidence pack may identify a needed authority transition, but it cannot
perform one. An approved transition must update the router, tracker, external-intake
and sync workflows, affected active skill files, all four plugin manifests, all four
marketplace catalogs, public documentation, installation mechanics, and migration
evidence together.

## Document roles

| Surface | Role | Authority |
|---|---|---|
| [REFINED-V1.md](REFINED-V1.md) | Proposed v1 direction + challenge of July 16 overbuild | Draft until approved |
| [../workflows/project-agent-config.md](../workflows/project-agent-config.md) | How to persist config per project | Draft until approved |
| `evidence/source-ledger.md` and `evidence/decision-register.md` | Preserve what was said, by whom with what confidence, and what remains open | Evidence only |
| Other `evidence/*.md` files | Requirements, lifecycle analysis, interfaces, conformance, faults, donors, verification queue | Evidence / candidate only |
| `plans/01-*` … `plans/03-*` | Full control-plane sequence (backlog; not v1 critical path) | Draft / deferred |
| Existing tracker/workflows/manifests | Actual current marketplace and skill lifecycle | Authoritative now |
