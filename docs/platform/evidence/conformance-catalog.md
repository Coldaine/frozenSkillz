# Platform Conformance Catalog (Working Draft)

> **Non-authoritative planning scratchpad.** These are candidate acceptance contracts extracted or derived from the recovered transcript. `source-explicit` means the transcript states the outcome; `source-derived` means the outcome is an inference needed to make a stated requirement testable. Neither means the project has approved or implemented it. `decision-needed` marks an outcome that cannot become normative until the linked gap is resolved.

## Test record contract

Every eventual conformance result should record:

- acceptance ID and requirement IDs;
- fixture repository commit and frozenSkillz commit;
- operating system, architecture, client name, and exact client version;
- input manifest/lock/catalog/machine-state digests;
- command, exit code, stdout/stderr capture, and changed-file digest list;
- observed configuration, approval, launcher, and runtime-health states;
- pass/fail result with machine-readable evidence path.

The evidence format itself remains blocked by `GAP-016` in `requirements-matrix.md`.

## Repository and synchronization correctness

| Acceptance ID | Candidate expected outcome | Evidence | Requirement | Status |
|---|---|---|---|---|
| `AC-REP-001` | Every managed native MCP file parses under the exact parser semantics of its target client. | `pasted-text.txt:L1045-1049` | `REQ-008` | `source-explicit`; client/version matrix needed |
| `AC-REP-002` | Every declared managed MCP appears in every client declared as a target, with no undeclared managed MCP added. | `pasted-text.txt:L1045-1049` | `REQ-006`, `REQ-008`, `REQ-013` | `source-explicit` |
| `AC-REP-003` | Every selected skill exists at the effective discovery path for each target client. Every explicitly declared nonstandard rule path resolves, and every in-scope native rule discovered by the approved scanner exists; rule activation is tested separately by `AC-CLIENT-001`. | `pasted-text.txt:L1045-1049` | `REQ-001`, `REQ-005` | `source-explicit`; declaration/discovery distinction clarified |
| `AC-REP-004` | A second synchronization from unchanged inputs produces no tracked-content diff and identical managed digests. | `pasted-text.txt:L1049-1050` | `REQ-008`, `REQ-009` | `source-explicit` |
| `AC-REP-005` | Deleting an unchanged vendored artifact and synchronizing restores byte-identical content and provenance. | `pasted-text.txt:L1049-1051` | `REQ-009` | `source-explicit` |
| `AC-REP-006` | Modifying a vendored artifact causes an explicit conflict outcome; no local byte is silently overwritten. | `pasted-text.txt:L1050-1052`, `pasted-text.txt:L1006-1012` | `REQ-009` | `source-explicit`; conflict CLI needed |
| `AC-REP-007` | Synchronization leaves forked and local artifacts unchanged, including their contents and ownership mode. | `pasted-text.txt:L1051-1052` | `REQ-009` | `source-explicit` |
| `AC-REP-008` | All executable/package/image/shared-skill/schema/host-version selections are pinned according to the approved lock contract; unresolved or mismatched pins fail validation before launch. | `pasted-text.txt:L843-863` | `REQ-007` | `source-derived`; `DEC-GAP-001` blocks exact form |

## Managed-output and structural-merge safety

| Acceptance ID | Candidate expected outcome | Evidence | Requirement | Status |
|---|---|---|---|---|
| `AC-MERGE-001` | Synchronization changes only server names or subtrees recorded as managed by the approved ownership contract. | `pasted-text.txt:L580-605` | `REQ-008` | `source-explicit` |
| `AC-MERGE-002` | Unmanaged MCP servers remain semantically unchanged after synchronization. | `pasted-text.txt:L584-590` | `REQ-008` | `source-explicit` |
| `AC-MERGE-003` | Unrelated Kilo settings remain semantically unchanged; the byte/comment/order guarantee is deferred until `GAP-007` is decided. | `pasted-text.txt:L578-607`, `pasted-text.txt:L1073-1082` | `REQ-008` | `source-explicit`, `decision-needed` |
| `AC-MERGE-004` | Any operation that cannot preserve the approved ownership boundary aborts before changing tracked content and reports the blocking file and entry. | `pasted-text.txt:L584-592` | `REQ-008` | `source-derived`; atomicity blocked by `GAP-006` |
| `AC-MERGE-005` | Render-state records the source digest and renderer version used to produce every managed output and detects drift from either. | `pasted-text.txt:L591-605` | `REQ-008` | `source-explicit`; schema needed |
| `AC-MERGE-006` | CI regeneration from the same approved inputs exits successfully with zero diff; any managed-output drift produces a nonzero result and identifies affected files. | `pasted-text.txt:L289-295`, `pasted-text.txt:L591-592` | `REQ-008` | `source-explicit` |

## Client behavior

These candidates apply to Claude Code, Cursor, VS Code, Kilo, and Antigravity only after the supported-version matrix in `GAP-010` is approved.

| Acceptance ID | Candidate expected outcome | Evidence | Requirement | Status |
|---|---|---|---|---|
| `AC-CLIENT-001` | A behavior fixture proves that each intended project rule activates under its target condition and does not activate outside it. | `pasted-text.txt:L609-641`, `pasted-text.txt:L1053-1058` | `REQ-001` | `source-derived`; activation fixtures needed |
| `AC-CLIENT-002` | Each intended project skill is discoverable by the target client from the actual materialized discovery location. | `pasted-text.txt:L643-666`, `pasted-text.txt:L1053-1059` | `REQ-005` | `source-explicit`; machine-global lifecycle unresolved |
| `AC-CLIENT-003` | The client exposes every declared relevant MCP/tool and no undeclared managed MCP/tool for the fixture project. | `pasted-text.txt:L1055-1060` | `REQ-006`, `REQ-013` | `source-explicit` |
| `AC-CLIENT-004` | A stale definition at another scope is detected, and the report identifies the effective client-specific winner without claiming field merging. | `pasted-text.txt:L697-722`, `pasted-text.txt:L1059-1061` | `REQ-013` | `source-explicit`; current precedence must be verified |
| `AC-CLIENT-005` | Configuration presence, non-secret credential/auth readiness, trust/approval, launcher availability, and runtime health are emitted as separate states. | `pasted-text.txt:L481-499`, `pasted-text.txt:L723-737`, `pasted-text.txt:L1014-1025`, `pasted-text.txt:L1060-1062` | `REQ-014`, `REQ-027` | `source-derived`; unknown/auth-state model needed |
| `AC-CLIENT-006` | Each MCP receives the approved project root or root set regardless of process working directory; missing root support fails explicitly rather than silently using an unrelated directory. | `pasted-text.txt:L544-563`, `pasted-text.txt:L1061-1062` | `REQ-011` | `source-explicit`; multi-root policy needed |
| `AC-CLIENT-007` | Generated adapter copies match the canonical selected skill digest and drift is reported without overwriting project-owned content. | `pasted-text.txt:L643-666` | `REQ-005`, `REQ-009` | `source-derived`; discovery precedence unresolved |
| `AC-CLIENT-008` | Missing, expired, present-but-unverified, and ready credential/auth states are reported without exposing values and without being collapsed into approval or health. | `pasted-text.txt:L481-499`, `pasted-text.txt:L1014-1025` | `REQ-014`, `REQ-027` | `source-derived`; client detection support open |

## Machine-global materialization

| Acceptance ID | Candidate expected outcome | Evidence | Requirement | Status |
|---|---|---|---|---|
| `AC-GLOBAL-001` | A selected reviewed skill revision/digest maps only to approved machine-global/client discovery targets and records the chosen copy/link/plugin method. | Current-task directive `CTD-002` | `REQ-024` | `direct-user-derived`; interface needed |
| `AC-GLOBAL-002` | After reconcile, every target client in the approved global-discovery matrix actually discovers the selected skill; metadata or file presence alone is insufficient. | Current-task directive `CTD-002` | `REQ-024` | `direct-user-derived`; client fixtures needed |
| `AC-GLOBAL-003` | Repeating reconcile with unchanged selection/source produces zero content and state diff. | Safety derivation | `REQ-024` | `decision-needed` |
| `AC-GLOBAL-004` | Local drift or intentional tool-only content is detected and never silently overwritten or deleted. | Current repository tool-root distinctions | `REQ-024` | `decision-needed` |
| `AC-GLOBAL-005` | Updating a selected skill preserves the previous good version for the approved rollback operation; rollback restores discovery and provenance. | Lifecycle gap | `REQ-024` | `decision-needed` |
| `AC-GLOBAL-006` | Deprecation/removal affects only owned install surfaces, reports remaining plugin/project/tool-only copies, and leaves no unreported stale shadow. | Lifecycle gap | `REQ-024` | `decision-needed` |

## Publication and verified plugin installation

| Acceptance ID | Candidate expected outcome | Evidence | Requirement | Status |
|---|---|---|---|---|
| `AC-PUB-001` | No gated/scout/personal-reference skill appears in any active frozen-skills plugin manifest unless separately promoted; all listed skill paths exist. | Current tracker and manifests | `REQ-025` | `current-authority` |
| `AC-PUB-002` | The four plugin manifests have aligned active skill IDs/paths and plugin version; the four root catalog entries are synchronized according to the separately versioned catalog metadata contract. | Current router/filesystem; tracker count defect | `REQ-025` | `current-authority`; catalog rule clarification needed |
| `AC-PUB-003` | Each client claimed as plugin-install supported completes install, discovery, update, and uninstall fixtures on an exact supported version. A manifest file alone cannot pass this case. | Current README supports Claude explicitly and qualifies other formats | `REQ-025` | `verification-needed` |
| `AC-PUB-004` | Deprecation, revocation, rollback, and uninstall leave an auditable result across published metadata and verified installed copies. | Proposed lifecycle extension | `REQ-025` | `decision-needed` |

## Fresh-clone readiness

| Acceptance ID | Candidate expected outcome | Evidence | Requirement | Status |
|---|---|---|---|---|
| `AC-REP-009` | A fresh checkout at the declared commit contains parseable committed native project configuration and selected vendored/generated content before local sync; machine-local approval, auth, launcher, and health are reported separately rather than treated as missing project configuration. | Assistant-attributed prior-user requirement at `pasted-text.txt:L264-295` | `REQ-026` | `confirmation-needed` |

## CLI contract

| Acceptance ID | Candidate expected outcome | Evidence | Requirement | Status |
|---|---|---|---|---|
| `AC-CLI-001` | The approved executable exposes exactly the approved public commands/options and a stable version/contract identifier; deprecated aliases behave only according to the approved compatibility policy. | Transcript conflict at `pasted-text.txt:L150-163`, `pasted-text.txt:L283-293`, `pasted-text.txt:L895-911`, `pasted-text.txt:L970-974` | `REQ-017` | `decision-needed` |
| `AC-CLI-002` | JSON modes emit schema-valid data on stdout, diagnostics on stderr, and the approved stable exit classification without partial mutation. | Derived from the proposed automation boundary | `REQ-017` | `decision-needed` |

## Recovered implementation evidence

| Acceptance ID | Candidate expected outcome | Evidence | Requirement | Status |
|---|---|---|---|---|
| `AC-EVIDENCE-001` | If the claimed foundation is recovered, its exact bytes match SHA-256 `b75cd5f21879db4e3b19e48261770c3cc5edae796986a6692abb5a8996bd77a9`, its contents/provenance are inventoried as untrusted donor evidence, and its claimed tests are rerun cleanly. A missing or mismatched artifact is recorded as unavailable, not implemented. | `pasted-text.txt:L957-983` | `REQ-022` | `verification-needed` |

## Windows and Linux equivalence

| Acceptance ID | Candidate expected outcome | Evidence | Requirement | Status |
|---|---|---|---|---|
| `AC-PLAT-001` | The same project commit and approved machine capabilities produce the same logical MCP, skill, and rule inventory on Windows and Linux. | `pasted-text.txt:L1063-1069` | `REQ-004`, `REQ-015` | `source-explicit` |
| `AC-PLAT-002` | Every selected portable MCP fixture launches and passes its health check on both platforms. | `pasted-text.txt:L1065-1069` | `REQ-012`, `REQ-018` | `source-explicit`; health definition needed |
| `AC-PLAT-003` | Every selected host-bound MCP resolves to the platform-specific implementation declared for that machine. | `pasted-text.txt:L1067-1070` | `REQ-010`, `REQ-018` | `source-explicit` |
| `AC-PLAT-004` | An unsupported host capability reports unavailable with a stable error classification and does not guess a path or implementation. | `pasted-text.txt:L1068-1071` | `REQ-010`, `REQ-014` | `source-explicit`; error schema needed |
| `AC-PLAT-005` | Committed outputs contain no user-specific absolute path; any such path causes validation failure before commit/publish. | `pasted-text.txt:L1070-1072` | `REQ-019` | `source-explicit`; allowed-path policy needed |
| `AC-PLAT-006` | Committed outputs and observation payloads contain no secret value across fixture inputs, rendered files, stdout, stderr, or serialized reports. | `pasted-text.txt:L1071-1072` | `REQ-019` | `source-explicit`; redaction contract needed |

## Cross-repository update safety

| Acceptance ID | Candidate expected outcome | Evidence | Requirement | Status |
|---|---|---|---|---|
| `AC-UPDATE-001` | A shared-definition change selects every actual consuming repository and no non-consumer in the golden repository set. | `pasted-text.txt:L394-418`, `pasted-text.txt:L1073-1078` | `REQ-016` | `source-explicit`; consumer-index contract needed |
| `AC-UPDATE-002` | Repeated update generation from identical inputs produces identical project diffs and metadata. | `pasted-text.txt:L1075-1079` | `REQ-016` | `source-explicit` |
| `AC-UPDATE-003` | Update generation preserves unrelated Kilo and client settings according to the approved structural-merge contract. | `pasted-text.txt:L1078-1080` | `REQ-008`, `REQ-016` | `source-explicit`; `GAP-007` blocks precision |
| `AC-UPDATE-004` | Update generation never modifies `fork` or `local` artifacts. | `pasted-text.txt:L1079-1081` | `REQ-009`, `REQ-016` | `source-explicit` |
| `AC-UPDATE-005` | Any ambiguous overwrite aborts that repository update before a branch/PR mutation and reports the conflict. | `pasted-text.txt:L1080-1082` | `REQ-009`, `REQ-016` | `source-explicit`; automation transaction policy needed |
| `AC-UPDATE-006` | Reverting the generated project PR restores the pre-update managed state without requiring out-of-band machine repair. | `pasted-text.txt:L1081-1082` | `REQ-016` | `source-explicit` |

## Inventory fidelity

| Acceptance ID | Candidate expected outcome | Evidence | Requirement | Status |
|---|---|---|---|---|
| `AC-INV-001` | Against a hand-built golden inventory, normalized scan output achieves 100% precision and 100% recall for all in-scope entities. | `pasted-text.txt:L1083-1093` | `REQ-015` | `source-explicit`; golden governance needed |
| `AC-INV-002` | Scan reports exact repository remote identity, clone/worktree path, branch, commit, and dirty state. | `pasted-text.txt:L129-142`, `pasted-text.txt:L1027-1036`, `pasted-text.txt:L1085-1091` | `REQ-015` | `source-explicit`; duplicate-clone semantics needed |
| `AC-INV-003` | Scan reports every in-scope skill, rule, MCP, client, source file, provenance, and scope exactly once unless the schema explicitly models duplicates. | `pasted-text.txt:L1029-1036`, `pasted-text.txt:L1089-1092` | `REQ-005`, `REQ-013`, `REQ-015` | `source-explicit`; identity keys needed |
| `AC-INV-004` | Scan reports machine launcher availability and resolution without exposing secret values. | `pasted-text.txt:L129-142`, `pasted-text.txt:L1091-1093` | `REQ-010`, `REQ-014`, `REQ-019` | `source-explicit` |
| `AC-INV-005` | Scan reports both the gateway process entry and every selected logical downstream MCP/tool behind it. | `pasted-text.txt:L795-841`, `pasted-text.txt:L1092-1093` | `REQ-012`, `REQ-015` | `source-explicit` |
| `AC-INV-006` | Local JSON output remains complete and schema-valid when no central sink is configured or the sink is unavailable. | `pasted-text.txt:L824-841` | `REQ-015` | `source-derived`; sink failure policy needed |

## Runtime and gateway behavior

| Acceptance ID | Candidate expected outcome | Evidence | Requirement | Status |
|---|---|---|---|---|
| `AC-RUN-001` | The host-MCP shim reads the approved machine registry, resolves the logical ID, and launches only the declared platform implementation. | `pasted-text.txt:L501-542` | `REQ-010` | `source-explicit`; CLI/error contract needed |
| `AC-RUN-002` | Project-native files invoke a stable platform gateway contract rather than embedding Docker's complete current CLI syntax. | `pasted-text.txt:L739-756` | `REQ-012` | `source-explicit` |
| `AC-RUN-003` | Gateway tests record startup latency and compare it with the approved budget. | `pasted-text.txt:L758-771` | `REQ-012` | `source-explicit`; budget missing |
| `AC-RUN-004` | Concurrent-client tests identify process/container reuse, duplicate OAuth state, memory use, log attribution, and orphan cleanup. | `pasted-text.txt:L758-771` | `REQ-012` | `source-explicit`; pass thresholds missing |
| `AC-RUN-005` | Tool-level allowlists are reflected in the effective exposed tool set, including downstream gateway inventory. | `pasted-text.txt:L773-793` | `REQ-006`, `REQ-012` | `source-explicit`; unsupported-client behavior needed |
| `AC-RUN-006` | Portable, host-bound, and project-process MCP categories each report category-appropriate roots, pins, availability, and health. | `pasted-text.txt:L384-393`, `pasted-text.txt:L895-911` | `REQ-018` | `source-derived`; observation schema needed |

## Agent-effectiveness candidates

These are questions, not pass/fail gates, until `GAP-015` is resolved.

| Acceptance ID | Evaluation question | Evidence | Requirement | Status |
|---|---|---|---|---|
| `AC-EFF-001` | Does the evaluated agent select the intended tool for each benchmark task? | `pasted-text.txt:L1094-1099` | `REQ-006` | `decision-needed` |
| `AC-EFF-002` | Are unrelated tools absent or sufficiently hidden under the approved exposure policy? | `pasted-text.txt:L1096-1100` | `REQ-006` | `decision-needed` |
| `AC-EFF-003` | Are tool names and descriptions discriminative under the benchmark workload? | `pasted-text.txt:L1098-1100` | `REQ-006` | `decision-needed` |
| `AC-EFF-004` | Does gateway-mediated discovery outperform direct exposure under a defined metric? | `pasted-text.txt:L1101-1104` | `REQ-012` | `decision-needed` |
| `AC-EFF-005` | Does tool-level filtering reduce wrong-tool calls relative to an unfiltered baseline? | `pasted-text.txt:L1101-1104` | `REQ-006` | `decision-needed` |

## Pilot entry and exit gates

| Gate ID | Candidate gate | Evidence | Status |
|---|---|---|---|
| `AC-PILOT-ENTRY-001` | Authority/lifecycle decisions, schemas, CLI contracts, supported-client matrix, and conformance evidence format are approved before pilot execution. | User correction at `pasted-text.txt:L952-955`; contract at `pasted-text.txt:L1041-1119` | `source-explicit`; decisions remain open |
| `AC-PILOT-ENTRY-002` | Local core, client adapters, runtime wrappers, and the automated acceptance/failure-injection harness pass in deterministic fixtures before deployment to pilot machines. | `pasted-text.txt:L944-950`, `pasted-text.txt:L1121-1132` | `source-derived` |
| `AC-PILOT-MATRIX-001` | The proposed matrix contains one Python repository, one infrastructure repository, one Windows 11 machine, one Linux machine, all five transcript-proposed project clients, one portable MCP, and one host-bound MCP. | `pasted-text.txt:L944-950` | `source-explicit`; support status, exact fixtures, and versions remain open |
| `AC-PILOT-EXIT-001` | Pilot success requires all approved repository, client, platform, update, inventory, security, runtime, and required failure-injection cases to pass; gateway connection alone is not success. | `pasted-text.txt:L1041-1119` | `source-explicit`; aggregation/waiver policy needed |

## Acceptance gaps that prevent a decision-complete plan

- Exact semantics and evidence for the existing machine-global skill installation lifecycle (`GAP-001`, `GAP-002`).
- Exact CLI, manifest, lock, schema migration, and conflict-resolution interfaces (`GAP-003` through `GAP-006`).
- Byte-versus-semantic preservation rules for mixed JSONC files (`GAP-007`).
- Install-root integrity and secret/redaction test corpus (`GAP-008`, `GAP-009`).
- Exact client versions, supported capabilities, and behavior on format drift (`GAP-010`).
- Health, approval, root, timeout, retry, and shutdown state machines (`GAP-011`).
- Repository discovery identity, staleness, and duplicate semantics (`GAP-012`).
- Sink and cross-repository automation failure contracts (`GAP-013`, `GAP-014`).
- Quantitative effectiveness metrics (`GAP-015`).
- Reproducible pilot evidence, pass aggregation, and waiver policy (`GAP-016`).

No pilot may be used to decide these contracts implicitly. The contracts are inputs to the pilot.
