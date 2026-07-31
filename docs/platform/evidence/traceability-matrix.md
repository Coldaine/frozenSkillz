# Platform Requirement Traceability Matrix

> **Status:** non-authoritative planning index. This matrix records links that exist
> in the planning evidence pack; it does not approve a candidate decision, requirement,
> interface, acceptance case, failure case, or implementation phase.

## Reading the matrix

- A listed `DR-*` or `CTD-*` retains the status assigned in
  `decision-register.md`. Presence here is not approval.
- A listed `AC-*` or `FI-*` remains a candidate contract until the governing
  requirement and decisions are approved.
- `TBD` means the current evidence pack has no exact artifact for that traceability
  edge. A nearby or partial mapping is labeled `partial`; it is not treated as closure.
- Current-authority references establish current repository behavior only. They do
  not approve a proposed platform extension.

Current-authority sources used below are the repository
[router](../../../AGENTS.md), [skill review tracker](../../skill-review/tracker.md),
[skill authority and frozen sync workflow](../../workflows/skill-authority-and-frozen-sync.md),
and [external intake workflow](../../workflows/external-skill-intake.md). The current
publication manifests are
[Claude](../../../plugins/frozen-skills/.claude-plugin/plugin.json),
[Codex](../../../plugins/frozen-skills/.codex-plugin/plugin.json),
[Cursor](../../../plugins/frozen-skills/.cursor-plugin/plugin.json), and
[Gemini](../../../plugins/frozen-skills/gemini-extension.json).

## Requirement crosswalk

| Requirement | Decision, directive, or current-authority basis | Interface owner(s) | Acceptance coverage | Failure coverage | Open verification and decision gaps | Implementation phase and backlog |
|---|---|---|---|---|---|---|
| `REQ-001` | `DR-003`, `DR-010` (both candidate); **TBD:** no separate current-task directive ID for the user's project-rule correction | `IF-02`, `IF-06` | `AC-REP-003`, `AC-CLIENT-001`, `AC-PLAT-001` | `FI-GAP-012` (partial: unsupported client/format) | `DEC-GAP-003`, `GAP-010`; `VQ-03`, `VQ-04` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-4-CLIENT-RUNTIME`, `PHASE-5-CONFORMANCE`; `BL-005` |
| `REQ-002` | Current repository scope: [router](../../../AGENTS.md); **TBD:** no exact `DR-*` or `CTD-*` | Not applicable: scope boundary | Not applicable | Not applicable | User confirmation of the indirect missing-context boundary | `PHASE-1-DECISIONS`; intentionally no implementation backlog |
| `REQ-003` | `DR-004`, `DR-005`, `CTD-001`; current [router](../../../AGENTS.md), [tracker](../../skill-review/tracker.md), and [external intake workflow](../../workflows/external-skill-intake.md) | `IF-01` | `AC-PUB-001`, `AC-PUB-002` | `FI-GAP-023` | `GAP-001`, `GAP-004`, `GAP-020`; `VQ-03`, `VQ-04` | `PHASE-0-EVIDENCE`, `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`; `BL-001` |
| `REQ-004` | `DR-006`, `CTD-001`, `CTD-002`; current [router](../../../AGENTS.md), [tracker](../../skill-review/tracker.md), and [sync workflow](../../workflows/skill-authority-and-frozen-sync.md) | `IF-01`, `IF-04`, `IF-09` | `AC-PLAT-001` (partial: logical cross-platform inventory) | `FI-GAP-019` | `GAP-001`, `GAP-002`, `GAP-004`, `GAP-019`, `GAP-020`; `VQ-02`, `VQ-04` | `PHASE-0-EVIDENCE`, `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`; `BL-001`, `BL-002` |
| `REQ-005` | `DR-007`, `DR-013`, `DR-014`, `DR-016`, `CTD-002`; current [sync workflow](../../workflows/skill-authority-and-frozen-sync.md) | `IF-03`, `IF-04`, `IF-06`, `IF-07` | `AC-REP-003`, `AC-CLIENT-002`, `AC-CLIENT-007`, `AC-INV-003` | `FI-GAP-005`, `FI-GAP-006`, `FI-GAP-012`, `FI-GAP-019` | `DEC-GAP-004`, `GAP-001`, `GAP-002`, `GAP-008`, `GAP-010`, `GAP-019`; `VQ-02`, `VQ-03`, `VQ-04` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-3-LOCAL-CORE`, `PHASE-4-CLIENT-RUNTIME`; `BL-001`, `BL-002`, `BL-003`, `BL-005` |
| `REQ-006` | `DR-008`, `DR-009`, `DR-010`, `DR-021`, `DR-022` | `IF-02`, `IF-03` | `AC-REP-002`, `AC-CLIENT-003`, `AC-RUN-005`, `AC-EFF-001`, `AC-EFF-002`, `AC-EFF-003`, `AC-EFF-005` | `FI-GAP-027` | `DEC-GAP-001`, `GAP-003`, `GAP-005`, `GAP-010`, `GAP-015`; `VQ-03` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-3-LOCAL-CORE`, `PHASE-4-CLIENT-RUNTIME`, `PHASE-5-CONFORMANCE`; `BL-002`, `BL-003`, `BL-005`, `BL-006` |
| `REQ-007` | `DR-020`, `DR-022` | `IF-01`, `IF-03`, `IF-05`, `IF-08` | `AC-REP-008` | `FI-GAP-004`, `FI-GAP-005`, `FI-GAP-011` | `GAP-003`, `GAP-005`, `GAP-008`, `GAP-011`; `VQ-05`, `VQ-06` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-3-LOCAL-CORE`, `PHASE-4-CLIENT-RUNTIME`; `BL-002`, `BL-003`, `BL-004`, `BL-006` |
| `REQ-008` | `DR-011`, `DR-012` | `IF-06`, `IF-07`, `IF-12` | `AC-REP-001`, `AC-REP-002`, `AC-REP-004`, `AC-MERGE-001`, `AC-MERGE-002`, `AC-MERGE-003`, `AC-MERGE-004`, `AC-MERGE-005`, `AC-MERGE-006`, `AC-UPDATE-003` | `FI-REQ-005`, `FI-REQ-006`, `FI-GAP-001`, `FI-GAP-002`, `FI-GAP-007`, `FI-GAP-008`, `FI-GAP-012` | `GAP-006`, `GAP-007`, `GAP-010`; `VQ-03` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-3-LOCAL-CORE`, `PHASE-4-CLIENT-RUNTIME`, `PHASE-5-CONFORMANCE`; `BL-002`, `BL-003`, `BL-005` |
| `REQ-009` | `DR-015`, `DR-016` | `IF-02`, `IF-03`, `IF-04`, `IF-07`, `IF-12` | `AC-REP-004`, `AC-REP-005`, `AC-REP-006`, `AC-REP-007`, `AC-CLIENT-007`, `AC-UPDATE-004`, `AC-UPDATE-005` | `FI-REQ-001`, `FI-REQ-007`, `FI-GAP-003`, `FI-GAP-004` | `GAP-004`, `GAP-005`, `GAP-006`; **TBD:** no dedicated verification item | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-3-LOCAL-CORE`, `PHASE-5-CONFORMANCE`, `PHASE-6-INTEGRATIONS`; `BL-002`, `BL-003`, `BL-005`, `BL-009` |
| `REQ-010` | `DR-017`, `DR-018`, `DR-033` | `IF-05`, `IF-08`, `IF-12` | `AC-PLAT-003`, `AC-PLAT-004`, `AC-INV-004`, `AC-RUN-001` | `FI-REQ-003`, `FI-GAP-011` | `GAP-003`, `GAP-011`; `VQ-02`, `VQ-11` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-3-LOCAL-CORE`, `PHASE-4-CLIENT-RUNTIME`; `BL-004` |
| `REQ-011` | `DR-019` | `IF-06`, `IF-08`, `IF-15` | `AC-CLIENT-006`, `AC-RUN-012` | `FI-GAP-009`, `FI-GAP-035` | `GAP-011`, `GAP-025`; `VQ-11`, `VQ-16` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-3-LOCAL-CORE`, `PHASE-4-CLIENT-RUNTIME`; `BL-004`, `BL-006` |
| `REQ-012` | `DR-025`, `DR-026`, `DR-027`, `DR-044` | `IF-05`, `IF-08`, `IF-09`, `IF-12`, `IF-15` | `AC-PLAT-002`, `AC-INV-005`, `AC-RUN-002`, `AC-RUN-003`, `AC-RUN-004`, `AC-RUN-005`, `AC-RUN-009`, `AC-EFF-004` | `FI-REQ-008`, `FI-GAP-014`, `FI-GAP-015`, `FI-GAP-031` | `DEC-GAP-006`, `GAP-003`, `GAP-011`, `GAP-015`, `GAP-024`; `VQ-06` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-4-CLIENT-RUNTIME`, `PHASE-5-CONFORMANCE`; `BL-006`, `BL-007` |
| `REQ-013` | `DR-023`, `DR-024` | `IF-01`, `IF-02`, `IF-06`, `IF-09` | `AC-REP-002`, `AC-CLIENT-003`, `AC-CLIENT-004`, `AC-INV-003` | `FI-REQ-002` | `GAP-010`; `VQ-03`, `VQ-12` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-4-CLIENT-RUNTIME`, `PHASE-5-CONFORMANCE`; `BL-005` |
| `REQ-014` | `DR-023`, `DR-026`, `DR-028`, `DR-030` | `IF-06`, `IF-09` | `AC-CLIENT-005`, `AC-CLIENT-008`, `AC-PLAT-004`, `AC-INV-004`, `AC-RUN-006` | `FI-REQ-003`, `FI-GAP-010`, `FI-GAP-015`, `FI-GAP-024` | `GAP-011`, `GAP-022`; `VQ-12` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-4-CLIENT-RUNTIME`, `PHASE-5-CONFORMANCE`; `BL-005`, `BL-006`, `BL-007` |
| `REQ-015` | `DR-028`, `DR-029`, `DR-030`, `DR-037` | `IF-09`, `IF-10` | `AC-PLAT-001`, `AC-INV-001`, `AC-INV-002`, `AC-INV-003`, `AC-INV-004`, `AC-INV-005`, `AC-INV-006` | `FI-REQ-004`, `FI-REQ-008`, `FI-GAP-016`, `FI-GAP-017` | `DEC-GAP-005`, `GAP-012`, `GAP-013`, `GAP-017`; `VQ-07`, `VQ-08`, `VQ-09` | `PHASE-0-EVIDENCE`, `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-3-LOCAL-CORE`, `PHASE-5-CONFORMANCE`, `PHASE-6-INTEGRATIONS`; `BL-007`, `BL-008`, `BL-012` |
| `REQ-016` | `DR-031`, `DR-032` | `IF-11` | `AC-UPDATE-001`, `AC-UPDATE-002`, `AC-UPDATE-003`, `AC-UPDATE-004`, `AC-UPDATE-005`, `AC-UPDATE-006` | `FI-GAP-018` | `GAP-014`; `VQ-14` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-6-INTEGRATIONS`; `BL-009` |
| `REQ-017` | `DR-027`, `DR-033` | `IF-08`, `IF-12` | `AC-CLI-001`, `AC-CLI-002`; `AC-MERGE-006`, `AC-INV-006`, `AC-RUN-001` (command-specific) | `FI-GAP-026`; `FI-REQ-003`, `FI-REQ-005` (command-specific) | `DEC-GAP-002`, `GAP-003`; naming remains a product decision | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-3-LOCAL-CORE`; `BL-003`, `BL-004` |
| `REQ-018` | `DR-020`, `DR-022`, `DR-025` | `IF-01`, `IF-02`, `IF-05`, `IF-06`, `IF-08`, `IF-09` | `AC-PLAT-002`, `AC-PLAT-003`, `AC-RUN-006` | `FI-GAP-028` | `GAP-011`; `VQ-06`, `VQ-11`, `VQ-12` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-4-CLIENT-RUNTIME`; `BL-004`, `BL-006` |
| `REQ-019` | `DR-022`, `DR-030`, `DR-034` | `IF-02`, `IF-05`, `IF-09`, `IF-10`, `IF-11`, `IF-12` | `AC-PLAT-005`, `AC-PLAT-006`, `AC-INV-004` | `FI-GAP-013` | `GAP-008`, `GAP-009`; `VQ-02`, `VQ-05` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-3-LOCAL-CORE`, `PHASE-5-CONFORMANCE`, `PHASE-6-INTEGRATIONS`; `BL-003`, `BL-007`, `BL-008`, `BL-009` |
| `REQ-020` | `DR-002` (direct user) | `IF-14` | `AC-PILOT-ENTRY-001`, `AC-PILOT-ENTRY-002`, `AC-PILOT-EXIT-001` | `FI-GAP-029`; approved `FI-REQ-*` and promoted `FI-GAP-*` cases are additionally required by gate policy | `GAP-016`; evidence policy remains open | `PHASE-5-CONFORMANCE`, `PHASE-7-PILOT`; `BL-007`, `BL-010` |
| `REQ-021` | `DR-035` (candidate) | `IF-06`, `IF-09`, `IF-14` | `AC-PILOT-MATRIX-001`, `AC-PILOT-ENTRY-002`, `AC-PILOT-EXIT-001` | `FI-GAP-029` | `GAP-010`, `GAP-016`; `VQ-03`, `VQ-04` | `PHASE-1-DECISIONS`, `PHASE-4-CLIENT-RUNTIME`, `PHASE-5-CONFORMANCE`, `PHASE-7-PILOT`; `BL-007`, `BL-010` |
| `REQ-022` | `DR-041` (unverified claim) | Evidence intake rather than platform interface | `AC-EVIDENCE-001` | `FI-GAP-020` | `GAP-018`; `VQ-01` | `PHASE-0-EVIDENCE`; no implementation backlog unless verified and separately adopted |
| `REQ-023` | `DR-004`, `DR-005`, `DR-012`, `DR-014`, `DR-018`, `DR-019`, `DR-026`, `DR-030`, `DR-032` (component decisions only) | Informational/non-normative; decomposed into component interfaces | Informational/non-normative; component cases apply | Informational/non-normative; component faults apply | `GAP-001`, `GAP-006`, `GAP-007`, `GAP-010`, `GAP-011`, `GAP-013`, `GAP-014`; `VQ-03`, `VQ-06`, `VQ-07`, `VQ-14` | `PHASE-0-EVIDENCE`, then capability-specific phases; no singular backlog item |
| `REQ-024` | `CTD-002` (direct user), `DR-006`, `DR-007`, `DR-014`; current [sync workflow](../../workflows/skill-authority-and-frozen-sync.md) | `IF-13`; `IF-04`, `IF-06`, `IF-12` (supporting) | `AC-GLOBAL-001`, `AC-GLOBAL-002`, `AC-GLOBAL-003`, `AC-GLOBAL-004`, `AC-GLOBAL-005`, `AC-GLOBAL-006`; `AC-CLIENT-002` (supporting discovery case) | `FI-GAP-019`, `FI-GAP-021`, `FI-GAP-022` | `DEC-GAP-004`, `GAP-001`, `GAP-002`, `GAP-019`; `VQ-02`, `VQ-03`, `VQ-04` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-3-LOCAL-CORE`, `PHASE-4-CLIENT-RUNTIME`; `BL-001`, `BL-003`, `BL-011` |
| `REQ-025` | `CTD-001`, `DR-004`, `DR-005`; current [router](../../../AGENTS.md), [tracker](../../skill-review/tracker.md), [external intake workflow](../../workflows/external-skill-intake.md), and all four publication manifests linked above | `IF-01`, `IF-06`, `IF-09` | `AC-PUB-001`, `AC-PUB-002`, `AC-PUB-003`, `AC-PUB-004` | `FI-GAP-019` (partial: coexistence), `FI-GAP-023` | `GAP-020`; `VQ-03`, `VQ-04` | `PHASE-0-EVIDENCE`, `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-4-CLIENT-RUNTIME`, `PHASE-5-CONFORMANCE`; `BL-001` |
| `REQ-026` | `DR-008`, `DR-011` (candidate context only); **TBD:** user confirmation required and no direct-user/current-authority basis exists | `IF-02`, `IF-03`, `IF-06`, `IF-07` | `AC-REP-009`; `AC-REP-001`, `AC-REP-002`, `AC-REP-003` (supporting parseability/completeness cases) | `FI-GAP-025` | `GAP-021`; `VQ-03`, `VQ-04` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-4-CLIENT-RUNTIME`, `PHASE-5-CONFORMANCE`, `PHASE-7-PILOT`; `BL-002`, `BL-005`, `BL-007` |
| `REQ-027` | `DR-023`, `DR-028`, `DR-030` (candidate/open) | `IF-05`, `IF-06`, `IF-09` | `AC-CLIENT-005`, `AC-CLIENT-008`, `AC-INV-004` (supporting no-secret observation) | `FI-GAP-024`; `FI-GAP-010`, `FI-GAP-013` (supporting trust and redaction cases) | `GAP-009`, `GAP-011`, `GAP-022`; `VQ-12` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-4-CLIENT-RUNTIME`, `PHASE-5-CONFORMANCE`; `BL-006`, `BL-007` |
| `REQ-028` | `DR-021`, `DR-043` | `IF-02`, `IF-03`, `IF-15` | `AC-RUN-005`, `AC-RUN-007`, `AC-RUN-008`; `AC-EFF-002`, `AC-EFF-005` (effectiveness only) | `FI-GAP-027` (policy syntax), `FI-GAP-030`, `FI-GAP-033` | `GAP-023`; `VQ-16`; exact managed/unmanaged boundary and user decision remain open | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-4-CLIENT-RUNTIME`, `PHASE-5-CONFORMANCE`; `BL-006`, `BL-007` |
| `REQ-029` | `DR-026`, `DR-044` | `IF-08`, `IF-15` | `AC-RUN-004`, `AC-RUN-009`, `AC-RUN-011` | `FI-GAP-014`, `FI-GAP-015`, `FI-GAP-031`, `FI-GAP-034` | `GAP-024`; `VQ-06`, `VQ-16` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-4-CLIENT-RUNTIME`, `PHASE-5-CONFORMANCE`; `BL-006`, `BL-007` |
| `REQ-030` | `DR-045` | `IF-08`, `IF-15` | `AC-RUN-010`, `AC-RUN-012` | `FI-GAP-032`, `FI-GAP-035` | `GAP-026`; `VQ-11`, `VQ-16` | `PHASE-1-DECISIONS`, `PHASE-2-CONTRACTS`, `PHASE-3-LOCAL-CORE`, `PHASE-4-CLIENT-RUNTIME`, `PHASE-5-CONFORMANCE`; `BL-004`, `BL-006`, `BL-007` |

## Orphans exposed by the crosswalk

The following missing edges prevent the affected requirements from being
implementation-ready. They are recorded here rather than filled with inferred links:

1. `REQ-001` has no dedicated current-task directive ID for the user's project-rule
   correction.
2. `REQ-002` is an indirect missing-context scope boundary and still needs user
   confirmation; it intentionally has no implementation edges.
3. `REQ-021` remains a candidate pilot topology even though its evidence/interface
   and entry-failure edges now exist.
4. `REQ-023` is intentionally informational/non-normative and decomposes into its
   component requirements rather than receiving one artificial contract.
5. `REQ-026` still requires user confirmation; its candidate acceptance and failure
   edges do not approve fresh-clone semantics.
