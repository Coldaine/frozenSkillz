# Platform Planning Evidence Pack

> **Status:** non-authoritative planning evidence. The design is not approved, the
> claimed implementation is not verified, and no pilot is authorized by these files.

This directory externalizes the large source discussion so that later reasoning does
not depend on one chat context window. It is intentionally separate from the current
authority documents and active plugin content.

## Evidence base

| Source | Coverage | Evidence status |
|---|---:|---|
| `C:\Users\pmacl\.codex\attachments\678c4dad-dc18-43cb-b6cc-427ed13b86d7\pasted-text.txt` | 1,132 of 1,132 lines; 35,989 bytes; SHA-256 `113FCF645F52D9D8EB56EFCB39040C744C146E7FF41B46FF717A8EC91B9CF237` | Source-recovered, but flattened and missing speaker labels. Most text is assistant-authored proposal, not an approved user decision. |
| `C:\Users\pmacl\.codex\attachments\e02c11ce-7010-490a-8d14-ea3bace784df\pasted-text.txt` | 17 physically collapsed lines; 8,176 bytes; SHA-256 `D7C20EDDB06DF94914686B64CFFD161E5BFE78140B1E2AE0E894C1CAB827358B` | User-supplied secondary architecture reference. Its self-description as canonical is not accepted; useful deltas are classified in `supplemental-control-plane-review.md`. |
| Three independent transcript passes | Decision extraction, architecture/adversarial critique, and requirements/conformance capture | Complete for the supplied file; reconciled findings still need user review. |
| Three independent supplemental passes | Full-source delta/coverage audit, MCP/security audit, and cross-plan fit/consistency audit | Complete for the second attachment; post-edit reviews corrected updater, tool-policy, session/OAuth, root-lifecycle, status, conditionality, and traceability wording. |
| Directives in the current Codex task | User corrections about frozenSkillz's existing lifecycle, real discovery-directory materialization, durable scratchpads, multi-agent review, and consolidation into two or three plans | Direct user evidence; recorded separately in the decision register because it is outside the flattened attachment. |
| `AGENTS.md` | Current repository router and authority order | Current documented authority. |
| `docs/skill-review/tracker.md` | Active, gated, scout, and promotion status | Highest current lifecycle/status authority. |
| `docs/workflows/skill-authority-and-frozen-sync.md` | Current personal-live-to-frozen sync model | Current documented model; may be superseded only by an explicit decision and migration. |
| `docs/workflows/external-skill-intake.md` | External evidence, evaluation, packaging, and promotion path | Current required external-intake workflow. |

The supplied transcript begins mid-conversation. It contains only two clearly
recoverable user interventions, at lines 479 and 952, plus assistant acknowledgements
of omitted user corrections. The source ledger therefore records speaker confidence
and never treats an assistant proposal as user approval.

## Classification axes

Do not use one status word to imply both evidence quality and design approval.

| Axis | Values | Meaning |
|---|---|---|
| Evidence origin | `current-authority`, `direct-user`, `indirect-missing-context`, `assistant-proposal`, `inference`, `unverified-claim` | Who or what supports the statement |
| Design disposition | `candidate`, `open`, `superseded`, `rejected`, `approved` | What the design does with it |
| Work state | `not-started`, `in-progress`, `complete`, `blocked` | Progress on the resulting task |

`approved` is reserved for explicit user approval of a design choice. No platform
design item in this pack is currently approved merely because it is detailed,
repeated, current-documented, or directly requested as a planning action.

## Evidence-pack documents

| File | Purpose |
|---|---|
| [source-ledger.md](source-ledger.md) | Line-level source recovery, speaker confidence, contradictions, corrections, and destination routing. |
| [decision-register.md](decision-register.md) | Direct-user/current, candidate, open, superseded, and unverified records without flattening their evidence or approval status. |
| [authority-lifecycle-and-installation.md](authority-lifecycle-and-installation.md) | Current frozenSkillz lifecycle plus the unresolved publication-to-real-discovery-directory transition. |
| [requirements-matrix.md](requirements-matrix.md) | Stable requirement IDs mapped to source evidence, design surfaces, and acceptance coverage. |
| [traceability-matrix.md](traceability-matrix.md) | Crosswalk from every requirement to decision/current-authority, interface, acceptance, failure, verification/gap, and implementation IDs; missing edges remain explicit `TBD`s. |
| [interfaces-and-schemas.md](interfaces-and-schemas.md) | Inventory of public contracts that must be specified before implementation. |
| [conformance-catalog.md](conformance-catalog.md) | Required repository, client, cross-platform, update, inventory, and agent-effectiveness checks. |
| [failure-injection-catalog.md](failure-injection-catalog.md) | Faults, expected outcomes, invariants, rollback checks, and evidence requirements. |
| [donor-verification-ledger.md](donor-verification-ledger.md) | Candidate code/evidence sources and their port/adapt/fixture/defer/reject status. |
| [non-goals-and-boundaries.md](non-goals-and-boundaries.md) | Explicit scope exclusions and ownership boundaries. |
| [open-verification-queue.md](open-verification-queue.md) | Factual research tasks kept separate from unresolved product decisions. |
| [implementation-dependency-map.md](implementation-dependency-map.md) | Ordered phases and gates; the pilot remains after contract and implementation completion. |
| [plan-to-finish-the-plan.md](plan-to-finish-the-plan.md) | The meta-plan, review passes, stop conditions, and approval path for completing the design. |
| [supplemental-control-plane-review.md](supplemental-control-plane-review.md) | Differential review of the second architecture note, including retained, adapted, deferred, rejected, and decision-needed material. |

## Definition of a decision-complete design

The planning phase is complete only when all of the following are true:

1. Every material segment of the 1,132-line source is routed as retained,
   superseded, rejected, open, or verification-needed.
2. Current frozenSkillz intake, gating, promotion, active publication, and metadata
   surfaces are separated from proposed plugin/personal installation, project
   vendoring, update, drift, deprecation, rollback, and removal stages that do not yet
   exist as one documented lifecycle.
3. The authority transition is explicitly decided; it is not inferred from where a
   copy happens to exist.
4. Global/plugin installation and project-local materialization identify the actual
   client discovery surfaces and their precedence.
5. Manifest, lock, provenance, catalog, machine registry, render state, adapter,
   observation, CLI, and update contracts are internally consistent and versioned.
6. Each normative requirement maps to one or more objective acceptance cases, and
   each fault has an expected result.
7. Time-sensitive client, Docker, Obot, and runtime claims have current evidence or
   are explicitly outside the supported boundary.
8. The unattached SHA-identified "foundation" is recovered and verified, or formally
   classified as unavailable and excluded from implementation status.
9. The user approves the design section by section.
10. Only then is a concrete implementation plan written and reviewed.

## Promotion ladder

```text
planning evidence (this directory)
  -> reconciled candidate design
  -> user-approved normative design
  -> implementation plan
  -> implementation and automated conformance
  -> pilot conformance run
```

Nothing in this directory changes current skill authority, activates a skill, updates
a manifest, installs a client artifact, or proves runtime behavior.
