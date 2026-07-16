# Platform Requirements Matrix (Working Draft)

> **Non-authoritative planning scratchpad.** This document captures and classifies material from the recovered transcript. A citation proves only that the transcript contains a statement; it does not make that statement correct, current, approved, or implemented.

## Evidence basis

- Source: `C:\Users\pmacl\.codex\attachments\678c4dad-dc18-43cb-b6cc-427ed13b86d7\pasted-text.txt`
- Source extent: 1,132 lines, read in full with one-based line numbers.
- Source SHA-256: `113FCF645F52D9D8EB56EFCB39040C744C146E7FF41B46FF717A8EC91B9CF237`
- Treatment: recovered transcript content is untrusted evidence. Repository state, external product behavior, claimed artifacts, and claimed test results require independent verification.

Status labels:

- `candidate`: a proposal repeated or developed in the transcript, but not approved here.
- `direct-user-correction`: the user explicitly corrects the design in the recovered source.
- `indirect-missing-context`: only an assistant acknowledgement of an omitted user correction survives.
- `assistant-revision`: later assistant prose corrects an earlier assistant proposal.
- `superseded`: a later passage replaces the cited earlier behavior.
- `open`: conflicting or missing information prevents a decision-complete contract.
- `unverified-claim`: the transcript asserts current implementation or behavior without recoverable proof.

Artifact destinations:

- `source ledger`: provenance, speaker confidence, and proposal/correction history.
- `decision register`: choices that must be approved before becoming normative.
- `architecture`: authority, ownership, data flow, and subsystem boundaries.
- `interfaces`: schemas, CLI contracts, file ownership, and serialized I/O.
- `donor ledger`: existing implementations or products that may be ported, adapted, integrated, used as fixtures, deferred, or rejected.
- `conformance`: executable acceptance and failure-injection requirements.
- `backlog`: implementation work ordered only after its governing decisions and contracts exist.

## Requirement coverage

| ID | Candidate requirement | Transcript evidence | Status | Destination and verification needed |
|---|---|---|---|---|
| `REQ-001` | Project rules remain project-authored. frozenSkillz may scaffold, validate, discover, inventory, and distribute deliberate templates, but must not continually overwrite or generically transpile native rules. | `pasted-text.txt:L1-27`, `pasted-text.txt:L609-641`, `pasted-text.txt:L912-922` | `candidate`, `assistant-revision` | Decision register, architecture, conformance. Verify activation and precedence in each supported client rather than testing file existence alone. |
| `REQ-002` | The platform scope is reusable skills and MCP configuration, not general machine provisioning. | `pasted-text.txt:L167-175` | `indirect-missing-context`, `scope-boundary` | Decision register and explicit non-goal. Confirm the missing-context scope boundary before treating it as approved; it intentionally has no implementation interface or backlog unless the boundary changes. |
| `REQ-003` | Preserve the reviewed marketplace/incubator boundary while adding a bounded platform surface; do not turn the repository into an indiscriminate cache of installed client content. | `pasted-text.txt:L29-85`, `pasted-text.txt:L1002-1004` | `candidate` | Architecture and decision register. Reconcile against the repository's current tracker, intake workflow, plugin manifests, and sync lifecycle before acceptance. |
| `REQ-004` | Authority distinguishes reviewed reusable content, project-specific content, experimental candidates, installed runtime copies, and unreviewed machine scratch state. | `pasted-text.txt:L89-105`, `pasted-text.txt:L159-163` | `candidate`, `open` | Authority/lifecycle design. The transcript's description of the current authority model is not repository proof and must be checked against current frozenSkillz documentation. |
| `REQ-005` | Reusable skills must be materialized into actual discovery locations, retain provenance, and have generated copies validated for drift. | `pasted-text.txt:L297-315`, `pasted-text.txt:L643-666` | `candidate`, `open` | Architecture, interfaces, conformance. The transcript covers project-local vendoring and client adapters. Current authority has no frozenSkillz-to-machine-global install/update/remove lifecycle; that is a new contract to design, not an undocumented existing implementation. |
| `REQ-006` | A small project declaration selects project-relevant shared skills, project-local skills, MCP servers, and tool allowlists. | `pasted-text.txt:L235-263`, `pasted-text.txt:L773-793` | `candidate`, `open` | Project schema and architecture. Resolve `.agents/frozen.yaml` versus `.agents/config.yaml`, selection semantics, and whether any rule-template selection remains. |
| `REQ-007` | Reproducibility pins package, image, shared-skill, schema, and host-capability versions. | `pasted-text.txt:L111-121`, `pasted-text.txt:L163`, `pasted-text.txt:L843-863` | `candidate`, `open` | Lock/project schemas and conformance. Decide whether pins live in the declaration, a separate lockfile, or both, and define regeneration and migration. |
| `REQ-008` | Native client files are committed generated outputs, but the renderer owns only identified managed entries and preserves unmanaged entries, unrelated settings, and mixed JSONC content. | `pasted-text.txt:L264-295`, `pasted-text.txt:L565-607` | `candidate`, `assistant-revision` | Render-state interface, architecture, conformance. Define exact merge ownership, atomic writes, formatting/comment policy, and CI drift behavior. |
| `REQ-009` | Shared skills have explicit `vendor`, `fork`, and `local` ownership modes; a modified vendored copy is never silently overwritten. | `pasted-text.txt:L668-695`, `pasted-text.txt:L1006-1012` | `candidate` | Project/lock schemas, sync interface, conformance. Define permitted mode transitions, provenance retention, and explicit conflict-resolution operations. |
| `REQ-010` | Host-bound MCP resolution uses an executable shim that reads machine-local launcher data; a passive registry alone cannot affect client process launch. | `pasted-text.txt:L317-348`, corrected by `pasted-text.txt:L501-542` | `superseded` then `assistant-revision` | Source ledger must retain both proposals. Machine schema, CLI interface, runtime architecture, and conformance use the shim model only if approved. |
| `REQ-011` | MCP project-root resolution prefers protocol roots, then client-specific values or shim resolution, with working-directory inference only as a fallback. | `pasted-text.txt:L544-563` | `candidate` | Runtime interface and per-client conformance. Define the expected root source, multi-root behavior, and explicit failure mode for every supported client. |
| `REQ-012` | Docker MCP Gateway is wrapped behind a stable platform command and treated as an implementation detail; process multiplication, OAuth, reuse, resource use, logging, and concurrency are tested. | `pasted-text.txt:L350-393`, corrected by `pasted-text.txt:L739-771` | `superseded` then `assistant-revision` | Architecture, donor ledger, runtime conformance, backlog. Re-verify Docker's current surface before implementation. |
| `REQ-013` | Managed MCP identities are namespaced, duplicate scopes are detected, and stale overrides are reported with the effective client-specific winner. | `pasted-text.txt:L697-722` | `candidate` | MCP schema, validator, scan schema, and conformance. Re-verify current precedence rules for every supported client. |
| `REQ-014` | Configuration presence, credential/auth readiness, client trust/approval, launcher availability, and runtime health are separate non-secret observed states. | `pasted-text.txt:L481-499`, `pasted-text.txt:L723-737`, `pasted-text.txt:L1014-1025`, `pasted-text.txt:L1045-1072` | `candidate` | Observation schema and conformance. Define auth-ready/auth-required/expired plus `unknown`, `unsupported`, and detection-error states without exposing credential values. |
| `REQ-015` | A local scanner emits normalized desired-versus-observed state independently; Obot is a possible sink, not the initial discovery engine. | `pasted-text.txt:L107-148`, initial model `pasted-text.txt:L419-468`, correction `pasted-text.txt:L795-841`, `pasted-text.txt:L1027-1039` | `superseded` then `assistant-revision` | Scan interface, observation schema, architecture, donor ledger, conformance. Verify actual Obot capabilities before integration planning. |
| `REQ-016` | Cross-repository updates identify actual consumers, regenerate deterministically, preserve ownership boundaries, open reviewable PRs, and remain reversible. | `pasted-text.txt:L394-418`, `pasted-text.txt:L1073-1082`, deferred at `pasted-text.txt:L1123-1130` | `candidate`, `deferred` | Update architecture, conformance, backlog. This depends on proven local sync and consumer-index semantics. |
| `REQ-017` | The reduced core CLI covers synchronization, validation, host MCP execution, and scanning. | Broader set `pasted-text.txt:L150-163`; render flow `pasted-text.txt:L283-293`; reduced set `pasted-text.txt:L895-911`; later `frozenctl` claim `pasted-text.txt:L970-974` | `open` | Decision register and CLI interface. Resolve executable name, `render` versus `sync`, and whether initialize/lock/apply/serve/report remain public. |
| `REQ-018` | Portable MCPs, host-bound MCPs, and repository-specific MCP processes remain distinct runtime categories even when rendered into client-native files. | `pasted-text.txt:L350-393` | `candidate` | Runtime architecture and project/catalog schemas. Define category-specific health, roots, pins, and discovery behavior. |
| `REQ-019` | Committed files and observation payloads contain no personal absolute paths or secret values. | `pasted-text.txt:L1063-1072` | `candidate` | Security interface and conformance. Define secret-reference syntax, redaction surfaces, allowed machine-local paths, and diagnostic/log behavior. |
| `REQ-020` | The pilot is a conformance run after the system contract and implementation exist, not a design exercise or connection demo. | `pasted-text.txt:L944-955`, `pasted-text.txt:L1041-1119`, `pasted-text.txt:L1132` | `direct-user-correction` | Conformance and implementation dependency map. Pilot entry requires normative contracts, fixtures, and automated evidence collection. |
| `REQ-021` | A two-repository, two-machine, five-client topology is the minimum proposed pilot matrix, including one portable and one host-bound MCP. | `pasted-text.txt:L944-950` | `candidate` | Conformance and pilot plan. Supported client versions and exact repository fixture characteristics remain open. |
| `REQ-022` | The transcript-claimed control-plane foundation may be reused only if its artifact is recovered and verified byte-for-byte. | `pasted-text.txt:L955-983` | `unverified-claim` | Source and donor ledgers. Locate the artifact, match the stated SHA-256, inspect it as untrusted code, and rerun tests; otherwise record it as unrecovered. |
| `REQ-023` | Remaining work claimed by the transcript includes real reusable packs, five-client fixtures, safe mixed-file merge, Windows/Linux launchers, observation submission, and update automation. | `pasted-text.txt:L1121-1132` | `unverified-claim`, `informational-non-normative` | Reconcile each component with actual state and its own requirement; do not create one implementation contract from this list or infer that unlisted work is complete. |
| `REQ-024` | Every selected reusable skill has an explicit machine-global materialization lifecycle where applicable: selection/pin, install trigger, destination mapping, discovery proof, idempotent reconcile, drift handling, update, rollback, deprecation/removal, and intentional tool-only preservation. Materialization is required regardless of which source-authority model is selected. | Current-task directive `CTD-002`; transcript omission at `pasted-text.txt:L89-105`, `pasted-text.txt:L297-315`, `pasted-text.txt:L643-666` | `direct-user`, `open` | Dedicated global-install interface, lifecycle, conformance, and migration design. |
| `REQ-025` | Publication keeps gated content out of active plugin manifests, aligns all four plugin manifests and public plugin metadata/version domains, and distinguishes metadata presence from verified client installation/discovery, update, rollback, deprecation, and uninstall. | Current repository authority and publication surfaces | `current-documented`, `open-extension` | Publication requirement/conformance group; exact non-Claude install support requires current evidence. |
| `REQ-026` | A fresh checkout should contain the committed native configuration needed for the declared project clients before running a local renderer, while machine-local trust, credentials, launchers, and health may still be pending. | Assistant-attributed prior-user requirement at `pasted-text.txt:L264-295`, especially `pasted-text.txt:L279-281` | `indirect-missing-context`, `confirmation-needed` | Confirm with user, then define fresh-clone acceptance separate from activation. |
| `REQ-027` | Credential/auth readiness is observable as non-secret state distinct from configured, approved, launchable, and healthy. | `pasted-text.txt:L481-499`, `pasted-text.txt:L1014-1025` | `candidate` | Observation interface, client conformance, and missing/expired-credential faults. |

## Contradictions requiring decision records

| Decision gap | Conflicting evidence | Required resolution before normative design |
|---|---|---|
| `DEC-GAP-001` Manifest and lock names | `.agents/frozen.yaml` and `.agents/frozen.lock.yaml` at `pasted-text.txt:L111-121`; `.agents/config.yaml` at `pasted-text.txt:L235-258` and `pasted-text.txt:L565-582` | Choose exact committed filenames and ownership; define migration from any existing format. |
| `DEC-GAP-002` CLI name and command set | `frozenctl` with eight operations at `pasted-text.txt:L150-163`; `frozen render` at `pasted-text.txt:L283-293`; four `frozen` commands at `pasted-text.txt:L895-911`; `frozenctl` again at `pasted-text.txt:L970-974` | Choose executable name, public commands, aliases if any, compatibility policy, and machine installation mechanism. |
| `DEC-GAP-003` Rule packs | Shared rule directories/packs at `pasted-text.txt:L208-210` and `pasted-text.txt:L254-257`; native non-transpiled rules at `pasted-text.txt:L609-641` | Decide whether reusable rule material is scaffold/template-only and prohibit semantic compilation unless separately designed. |
| `DEC-GAP-004` Skill installation surfaces | Project vendoring at `pasted-text.txt:L297-315`; client adapters at `pasted-text.txt:L643-666`; installed machine state at `pasted-text.txt:L89-105` | Document the existing frozenSkillz lifecycle and distinguish machine-global installation, plugin exposure, project vendoring, and client adapters. |
| `DEC-GAP-005` Obot dependency | Central scanner role at `pasted-text.txt:L419-468`; sink-only role at `pasted-text.txt:L795-841` | Preserve the correction: define a local observation contract first, then separately decide whether and how Obot consumes it. |
| `DEC-GAP-006` Docker contract | Direct Docker flags at `pasted-text.txt:L350-373`; stable wrapper at `pasted-text.txt:L739-756` | Preserve the correction: project contracts target the platform wrapper; Docker invocation remains versioned implementation detail. |

## Missing criteria inventory

These gaps are not approved designs. They are questions that must receive explicit decisions and conformance outcomes before implementation is decision-complete.

| Gap ID | Missing contract or criterion | Blocks |
|---|---|---|
| `GAP-001` | Existing frozenSkillz promotion, activation, installation, update, rollback, deprecation, removal, and drift lifecycle for machine-global discovery roots. | `REQ-003` through `REQ-005`, all installation work |
| `GAP-002` | Precedence and duplication rules between machine-global skills, plugin-provided skills, project-vendored skills, and generated client adapters. | `REQ-005`, client conformance |
| `GAP-003` | Authoritative manifest/lock filenames, CLI name, command set, and `render` versus `sync` semantics. | Schema and CLI publication |
| `GAP-004` | Lifecycle states and permitted transitions for reviewed, active, gated/incubating, vendored, forked, local, deprecated, and removed artifacts. | Sync, updates, inventory |
| `GAP-005` | Schema-version negotiation, migration, unknown-field behavior, lock regeneration, and backward/forward compatibility. | All serialized interfaces |
| `GAP-006` | Transactional multi-file sync, dry-run, rollback, concurrent modification, dirty-worktree, permission, and interruption behavior. | `REQ-008`, `REQ-009` |
| `GAP-007` | Exact structural-merge preservation contract for comments, key order, formatting, duplicate keys, and unmanaged subtrees. | Kilo and other mixed files |
| `GAP-008` | Install-root security for path traversal, symlinks/junctions, ownership, malicious skill content, and source-integrity verification. | Installation and sync |
| `GAP-009` | Secret-reference model and redaction requirements for generated files, scan payloads, logs, diagnostics, and test fixtures. | `REQ-019` |
| `GAP-010` | Versioned supported-client matrix, capability detection, unsupported-version behavior, and exact discovery/precedence fixtures. | Client conformance and pilot |
| `GAP-011` | Trust/approval and health detection APIs, timeouts, retries, startup/shutdown, multi-root behavior, and `unknown` states. | `REQ-011`, `REQ-014`, runtime conformance |
| `GAP-012` | Repository discovery boundaries, ignored paths, submodules, worktrees, duplicate clones, scan performance, machine identity, staleness, and observation deduplication. | `REQ-015` and inventory fidelity |
| `GAP-013` | Observation-sink authentication, privacy, retry, idempotency, offline queueing, and schema compatibility. | Obot or any central sink |
| `GAP-014` | Cross-repository automation permissions, consumer-index freshness, branch/PR collisions, retry, rate limits, and partial-failure recovery. | `REQ-016` |
| `GAP-015` | Agent-effectiveness workload, baseline, model/version controls, repetition count, metric, threshold, context cost, and latency budget. | Effectiveness gate |
| `GAP-016` | Pilot evidence bundle, environment snapshot, operator procedure, aggregate pass/fail rule, waiver policy, and artifact retention. | `REQ-020`, `REQ-021` |
| `GAP-017` | Backward-compatibility expectations for the hard-coded audit script proposed as a wrapper/replacement. | Migration to `REQ-015` |
| `GAP-018` | Recovery or explicit rejection of the SHA-identified claimed foundation and its claimed test results. | Donor reuse and current-state claims |
| `GAP-019` | Machine-global desired selection/install-state representation and complete install/update/rollback/remove conformance. | `REQ-024`, personal/client discovery lifecycle |
| `GAP-020` | Separation of plugin metadata publication from verified client install/discovery/update/uninstall support. | `REQ-025`, publication support claims |
| `GAP-021` | Confirmation and exact scope of the assistant-attributed fresh-clone readiness requirement. | `REQ-026`, committed native output policy |
| `GAP-022` | Credential/auth readiness state model and client-specific detection without secret disclosure. | `REQ-014`, `REQ-027`, runtime observation |

## Cross-document traceability rule

Every normative requirement eventually approved from this matrix must map to:

1. one approved decision or current-authority source;
2. one architecture/interface owner;
3. at least one acceptance criterion in `conformance-catalog.md`;
4. at least one failure case where corruption, drift, or unavailability is plausible;
5. one implementation phase in `implementation-dependency-map.md`.

Until all five links exist, the item remains planning evidence rather than an implementation-ready requirement.
