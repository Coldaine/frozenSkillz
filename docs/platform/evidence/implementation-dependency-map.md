# Platform Implementation Dependency Map (Working Draft)

> **Non-authoritative planning scratchpad.** This document orders planning, contract, implementation, conformance, integration, and pilot work. It does not approve the transcript's proposed architecture, command names, schemas, integrations, or claimed implementation state.

## Sequencing invariant

The pilot is downstream of the approved system contract and a completed conformance harness. It must not be used to decide the contract by trial and error. This preserves the correction at `pasted-text.txt:L952-955` and the conformance-first sequence at `pasted-text.txt:L1041-1132`.

```text
recovered evidence
    -> current-repository verification
    -> approved decisions
    -> normative architecture and interfaces
    -> deterministic local implementation
    -> client/runtime implementation
    -> automated conformance and failure injection
    -> optional central integrations and update automation
    -> pilot against the committed contract
```

## Phase map

| Phase ID | Purpose and outputs | Entry gate | Exit gate | Must not happen in this phase |
|---|---|---|---|---|
| `PHASE-0-EVIDENCE` | Build the source ledger, classify corrections/superseded proposals, inspect current frozenSkillz lifecycle/authority, verify current repository state, re-verify dynamic client/Docker/Obot claims, and recover or reject the SHA-identified claimed foundation. | Recovered transcript available and treated as untrusted evidence. | Every transcript claim has a status and destination; current authority sources are identified; `REQ-022` is verified or recorded unrecovered. | No transcript proposal is promoted to architecture merely because it is detailed or repeated. |
| `PHASE-1-DECISIONS` | Close authority/lifecycle, install surfaces, project-vs-global precedence, manifest/lock names, CLI surface, rule-template policy, supported-client matrix, versioning, security, and non-goal decisions. | `PHASE-0-EVIDENCE` complete. | `DEC-GAP-001` through `DEC-GAP-006` and `GAP-001` through `GAP-005`, `GAP-008` through `GAP-011` have explicit approved outcomes or explicit deferrals with no dependent v1 work. | No schema or CLI is declared stable while its naming, ownership, or compatibility decision remains open. |
| `PHASE-2-CONTRACTS` | Publish normative architecture, lifecycle state machine, project/lock/catalog/machine/render-state/observation schemas, CLI I/O and error contracts, sync transaction model, structural-merge ownership, secret/redaction model, and conformance evidence format. | `PHASE-1-DECISIONS` complete for all v1 capabilities. | Every approved requirement maps to an interface owner, acceptance ID, failure ID, and implementation phase; all schemas and examples validate; no unresolved decision is hidden in prose. | No pilot fixtures substitute for missing interface definitions. |
| `PHASE-3-LOCAL-CORE` | Implement deterministic local installation/vendoring/sync, validation, host-MCP execution/root resolution, normalized local scan, provenance, pins, and transaction recovery using fixtures only. | Governing `PHASE-2-CONTRACTS` artifacts approved. | Repository/sync, merge, pin, local scan, launcher, path, and secret tests pass; repeated operations are idempotent; approved failure cases pass locally. | No Obot dependency, cross-repository PR automation, or pilot deployment. |
| `PHASE-4-CLIENT-RUNTIME` | Implement machine-global and project-local discovery adapters, supported native MCP renderers, trust/approval observation, namespace/collision analysis, gateway wrapper, tool filtering, and Windows/Linux launcher fixtures. | `PHASE-3-LOCAL-CORE` APIs stable enough for adapters. | All declared client/version fixtures pass behavior tests; portable/host/project-process MCP categories pass roots, pins, availability, health, and concurrency tests on deterministic environments. | No claim of Cursor, Antigravity, or other client parity without a passing exact-version fixture (`pasted-text.txt:L643-666`). |
| `PHASE-5-CONFORMANCE` | Automate the complete acceptance catalog, approved transcript-proposed failure injections, promoted derived safety cases, golden inventory comparison, evidence capture, and pass/fail aggregation. | `PHASE-4-CLIENT-RUNTIME` complete for the declared v1 matrix. | Every approved requirement has executable coverage; all required deterministic cases pass; the evidence bundle can be independently reproduced; blocked cases are reported as not runnable rather than pass. | No pilot execution and no effectiveness claim without quantitative criteria. |
| `PHASE-6-INTEGRATIONS` | Add central observation submission/indexing and cross-repository update PR automation only if retained in v1. | Local observation schema stable; local sync/update safety and conformance pass. | Sink auth/retry/idempotency/privacy tests and update consumer-selection/partial-failure/reversibility tests pass. | Obot is not treated as the scanner; automation does not redefine local ownership semantics (`pasted-text.txt:L795-841`, `pasted-text.txt:L1123-1130`). |
| `PHASE-7-PILOT` | Deploy the approved system to the declared two-repository, Windows/Linux, five-client matrix and run the committed conformance suite as an operational proof. | `PHASE-5-CONFORMANCE` complete and `PHASE-6-INTEGRATIONS` complete for any integration included in pilot scope. | All required operational cases pass with retained evidence; failures map to requirement/interface defects or implementation defects; gateway connection alone is never sufficient. | No architecture invention, implicit waiver, or expansion beyond the approved pilot matrix. |

## Decision and gap gates

| Gate ID | Must be closed before | Decision evidence required |
|---|---|---|
| `GATE-AUTHORITY-LIFECYCLE` | `PHASE-2-CONTRACTS` | Current frozenSkillz promotion/publication lifecycle; authoritative source for reviewed, gated, and installed content; exact machine-global install/update/remove behavior; project-vendor/plugin/adapter precedence. Traces to `REQ-003` through `REQ-005`, `GAP-001`, `GAP-002`, `GAP-004`. |
| `GATE-PUBLIC-INTERFACES` | `PHASE-2-CONTRACTS` | Approved manifest/lock names, CLI executable and commands, schema versions, migration rules, exit codes, JSON output, dry-run, conflict resolution. Traces to `REQ-006`, `REQ-007`, `REQ-017`, `GAP-003`, `GAP-005`. |
| `GATE-SYNC-SAFETY` | `PHASE-3-LOCAL-CORE` | Transaction boundaries, rollback, concurrent modification, dirty worktree, structural merge, delete/rename/deprecate, path security, and provenance integrity. Traces to `REQ-008`, `REQ-009`, `GAP-006` through `GAP-008`. |
| `GATE-CLIENT-MATRIX` | `PHASE-4-CLIENT-RUNTIME` | Exact client versions, skill/rule/MCP discovery paths, precedence, supported format capabilities, trust detection, root behavior, and unsupported-version handling. Traces to `REQ-001`, `REQ-005`, `REQ-011`, `REQ-013`, `REQ-014`, `GAP-010`, `GAP-011`. |
| `GATE-SECURITY` | `PHASE-3-LOCAL-CORE` | Secret references/redaction, allowed committed/machine-local paths, source integrity, diagnostics/log rules, fixture corpus. Traces to `REQ-019`, `GAP-008`, `GAP-009`. |
| `GATE-INVENTORY` | `PHASE-5-CONFORMANCE` | Repository/worktree identity, duplicate clones, discovery boundaries, staleness, golden ownership, gateway downstream identity, observation schema. Traces to `REQ-015`, `GAP-012`. |
| `GATE-EFFECTIVENESS` | Any effectiveness claim in `PHASE-5-CONFORMANCE` or `PHASE-7-PILOT` | Benchmark corpus, baseline, model/version controls, repetitions, metric, threshold, context cost, and latency budget. Traces to `AC-EFF-*`, `GAP-015`. |
| `GATE-PILOT-EVIDENCE` | `PHASE-7-PILOT` | Evidence bundle, environment snapshot, operator procedure, aggregation, waiver policy, retention, and declared fixture commits/versions. Traces to `REQ-020`, `REQ-021`, `GAP-016`. |

## Backlog dependency groups

| Backlog group | Source | Depends on | Earliest phase |
|---|---|---|---|
| `BL-001` Reconcile real reusable packs and current plugin/install lifecycle. | `pasted-text.txt:L29-85`, `pasted-text.txt:L1002-1012`, `pasted-text.txt:L1123-1126` | `PHASE-0-EVIDENCE`, `GATE-AUTHORITY-LIFECYCLE` | `PHASE-1-DECISIONS` for decisions; `PHASE-3-LOCAL-CORE` for implementation |
| `BL-002` Define project declaration, lock/pins, provenance, ownership modes, and render state. | `pasted-text.txt:L235-315`, `pasted-text.txt:L565-607`, `pasted-text.txt:L668-695`, `pasted-text.txt:L843-863` | `GATE-PUBLIC-INTERFACES`, `GATE-SYNC-SAFETY` | `PHASE-2-CONTRACTS` |
| `BL-003` Implement safe synchronization/installation and validation. | `pasted-text.txt:L895-906`, `pasted-text.txt:L1045-1052` | `BL-002`, `GATE-SECURITY` | `PHASE-3-LOCAL-CORE` |
| `BL-004` Implement machine launcher resolution and root handling. | `pasted-text.txt:L501-563`, `pasted-text.txt:L907-911` | Machine/CLI schemas, `GATE-CLIENT-MATRIX` | Begins in `PHASE-3-LOCAL-CORE`; completed in `PHASE-4-CLIENT-RUNTIME` |
| `BL-005` Implement client-specific skill/rule/MCP adapters and safe mixed-file merge. | `pasted-text.txt:L609-666`, `pasted-text.txt:L865-894`, `pasted-text.txt:L1125-1128` | `BL-003`, `GATE-CLIENT-MATRIX`, `GATE-SYNC-SAFETY` | `PHASE-4-CLIENT-RUNTIME` |
| `BL-006` Implement gateway wrapper, tool filtering, and runtime observation. | `pasted-text.txt:L739-841` | `BL-004`, approved runtime/observation contracts | `PHASE-4-CLIENT-RUNTIME` |
| `BL-007` Build golden inventory, five-client conformance fixtures, and failure harness. | `pasted-text.txt:L944-950`, `pasted-text.txt:L1041-1119`, `pasted-text.txt:L1125-1129` | `BL-003` through `BL-006`, `GATE-INVENTORY` | `PHASE-5-CONFORMANCE` |
| `BL-008` Add central observation submission/indexing. | `pasted-text.txt:L795-841`, `pasted-text.txt:L1027-1039`, `pasted-text.txt:L1128-1130` | Stable local scan schema and passing `BL-007` inventory cases | `PHASE-6-INTEGRATIONS` |
| `BL-009` Add cross-repository update automation. | `pasted-text.txt:L394-418`, `pasted-text.txt:L1073-1082`, `pasted-text.txt:L1129-1130` | Proven local sync, consumer index, partial-failure/retry contract | `PHASE-6-INTEGRATIONS` |
| `BL-010` Run the conformance pilot. | `pasted-text.txt:L944-955`, `pasted-text.txt:L1041-1132` | `BL-007`, plus `BL-008`/`BL-009` only if included in declared pilot scope | `PHASE-7-PILOT` |
| `BL-011` Implement machine-global selection, reconcile, discovery proof, drift/update/rollback, deprecation, and removal. | Current-task `CTD-002`; transcript omission at `pasted-text.txt:L89-105`, `pasted-text.txt:L297-315`, `pasted-text.txt:L643-666` | `GATE-AUTHORITY-LIFECYCLE`, `GATE-PUBLIC-INTERFACES`, `GATE-SYNC-SAFETY`, `GATE-CLIENT-MATRIX` | Begins in `PHASE-3-LOCAL-CORE`; completed in `PHASE-4-CLIENT-RUNTIME` |
| `BL-012` Implement normalized local repository/client/artifact scanner independently of any sink. | `pasted-text.txt:L795-841`, `pasted-text.txt:L1027-1039` | Stable observation schema, `GATE-INVENTORY`, `GATE-SECURITY` | `PHASE-3-LOCAL-CORE`; full golden coverage in `PHASE-5-CONFORMANCE` |

## Pilot sequencing checks

Before scheduling `BL-010`, the plan must answer yes with evidence to all of the following:

- Are current frozenSkillz lifecycle and real agent discovery/install surfaces documented and approved?
- Are all public file, schema, CLI, ownership, version, error, security, and observation contracts approved?
- Does every approved requirement map to at least one automated acceptance and plausible failure case?
- Do deterministic fixtures pass before deployment to user machines?
- Are exact repository commits, machine states, operating systems, client versions, portable MCP, and host-bound MCP declared?
- Is the evidence bundle reproducible and its pass/fail aggregation fixed before the run?

If any answer is no, the next task remains in the earlier phase. The pilot does not close planning gaps.
