# Platform Planning Router

This directory contains planning material for extending frozenSkillz beyond its
current marketplace/intake boundary. It does not change current repository authority,
activate content, install skills, or claim that a control plane exists.

## How the documents hang together

```text
supplied transcript + current repository authority + live verification
                              |
                              v
evidence/ (planning evidence pack: source, decisions, requirements, tests, gaps)
                              |
                              v
plans/    (three coherent phase plans synthesized from that evidence)
                              |
                    explicit user approval
                              |
                              v
AGENTS.md / tracker / workflows / manifests / implementation
```

The `evidence/` documents are appendices joined by stable decision, requirement,
acceptance, failure, gap, and phase IDs. They remain non-authoritative even though
they live in the repository. Start with
[the evidence-pack index](evidence/README.md).

The `plans/` directory is the readable execution sequence:

1. [Plan 1: design closure, authority, and distribution](plans/01-design-closure-authority-and-distribution.md)
2. [Plan 2: local control plane and client runtime](plans/02-local-control-plane-and-client-runtime.md)
3. [Plan 3: conformance, integrations, and pilot](plans/03-conformance-integrations-and-pilot.md)

## Relationship to current repository authority

Until a plan is explicitly approved and its changes are implemented, the existing
authority order remains unchanged:

1. `docs/skill-review/tracker.md` governs active, gated, scout, and promotion status.
2. `docs/workflows/external-skill-intake.md` governs external evaluation.
3. Active files under `plugins/frozen-skills/skills/` define installable behavior.
4. `docs/workflows/skill-authority-and-frozen-sync.md` describes the current
   personal-live-to-reviewed-frozen relationship.
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
| `evidence/source-ledger.md` and `evidence/decision-register.md` | Preserve what was said, by whom with what confidence, and what remains open | Evidence only |
| Other `evidence/*.md` files | Requirements, current-lifecycle analysis, interface inventory, conformance, faults, donors, and verification queue | Evidence and candidate contracts only |
| `plans/01-*` | Close authority and system-contract decisions | Draft until approved |
| `plans/02-*` | Implement the approved local/distribution/runtime contract | Blocked until Plan 1 approval |
| `plans/03-*` | Prove conformance, add retained integrations, and run the pilot | Blocked until Plan 2 and deterministic conformance complete |
| Existing tracker/workflows/manifests | Actual current marketplace and skill lifecycle | Authoritative now |
