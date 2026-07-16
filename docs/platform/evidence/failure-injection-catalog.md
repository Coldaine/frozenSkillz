# Platform Failure-Injection Catalog (Working Draft)

> **Non-authoritative planning scratchpad.** The first eight cases are explicitly proposed by assistant-authored transcript text. The user required a complete pre-pilot contract, but did not explicitly approve this exact set. Their detailed expected outcomes are candidates, and additional cases are derived coverage gaps that must be reviewed before becoming normative.

## Execution protocol

Each failure-injection run should capture:

1. a clean fixture digest and environment record;
2. the exact injected mutation;
3. the command or client action under test;
4. exit code, diagnostics, changed paths, and post-run digests;
5. configuration, approval, launcher, runtime, and observation states;
6. cleanup proof restoring the initial fixture.

Unless an approved interface says otherwise, a safe failure means no silent overwrite, no out-of-scope mutation, no secret disclosure, and enough diagnostic evidence to identify the failed invariant.

## Transcript-proposed cases

Source for the required set: `pasted-text.txt:L1106-1119`.

| Failure ID | Injection | Candidate expected outcome | Traces to | Missing decision |
|---|---|---|---|---|
| `FI-REQ-001` | Modify a vendored skill after synchronization. | The next sync detects divergence, leaves the modified bytes and unrelated outputs unchanged, identifies source and local digests, and exits through the approved explicit-conflict path. | `REQ-009`; `AC-REP-006` | Conflict-resolution CLI and exit code (`GAP-003`, `GAP-006`) |
| `FI-REQ-002` | Add a stale MCP definition with the same logical name at another scope. | Validation/scan lists every colliding source and scope, reports the effective winner for each supported client, and does not claim that fields merge. | `REQ-013`; `AC-CLIENT-004` | Verified client precedence and severity policy (`GAP-010`) |
| `FI-REQ-003` | Remove the selected Windows host launcher. | Host MCP execution reports a stable unavailable classification, launches no guessed or fallback executable, and records configuration present / launcher unavailable / runtime untested. | `REQ-010`, `REQ-014`; `AC-PLAT-004` | Error and observation schemas (`GAP-011`) |
| `FI-REQ-004` | Run scan from a stale repository clone. | Output records the exact local remote, branch, commit, dirty state, and desired-state delta without silently updating the clone. | `REQ-015`; `AC-INV-002` | Definition of desired revision and warning/failure policy (`GAP-012`) |
| `FI-REQ-005` | Malform a managed JSONC file. | Synchronization identifies the file and parse location, writes no partial output, leaves all tracked files at their pre-run digests, and exits nonzero. | `REQ-008`; `AC-MERGE-004` | Transaction/rollback implementation (`GAP-006`) |
| `FI-REQ-006` | Add unrelated settings and comments to Kilo's mixed configuration file. | Synchronization changes only the owned subtree and preserves all unrelated semantic content; preservation of exact bytes, comments, key order, and formatting follows the still-open structural-merge contract. | `REQ-008`; `AC-MERGE-003` | Exact preservation rule (`GAP-007`) |
| `FI-REQ-007` | Change a shared skill dependency to project-owned `fork` mode and modify it. | Future shared updates leave its mode, contents, and project provenance unchanged and do not report it as a vendored-drift conflict. | `REQ-009`; `AC-REP-007` | Mode-transition and provenance contract (`GAP-004`) |
| `FI-REQ-008` | Place multiple selected MCPs behind one native gateway entry. | Scan reports the gateway entry plus the complete selected logical downstream MCP/tool set with no omissions or double counting. | `REQ-012`, `REQ-015`; `AC-INV-005` | Downstream identity and runtime-observation schema (`GAP-011`, `GAP-012`) |

## Derived safety and recovery cases

These cases are recommended because the proposed architecture creates the failure mode. They are not direct approved requirements.

| Failure ID | Injection | Candidate expected outcome | Traces to | Status |
|---|---|---|---|---|
| `FI-GAP-001` | Interrupt synchronization between two managed file writes. | Recovery leaves either the entire old managed state or the entire new managed state, never a mixed state; the next validation identifies and safely recovers any transaction marker. | `REQ-008`; `GAP-006` | `decision-needed` |
| `FI-GAP-002` | Modify a managed native entry concurrently through a client UI during synchronization. | Compare-before-replace detects the changed input and aborts before overwriting it; unrelated completed work is rolled back according to the approved transaction policy. | `REQ-008`; `GAP-006` | `decision-needed` |
| `FI-GAP-003` | Delete an unchanged vendored artifact. | Synchronization restores byte-identical content and provenance, and the second synchronization is zero-diff. | `REQ-009`; `AC-REP-004`, `AC-REP-005` | `source-derived` |
| `FI-GAP-004` | Rename or remove a reviewed reusable artifact upstream while a project still selects it. | Lock/validation reports an unresolved dependency and performs no destructive cleanup until an approved migration/removal decision exists. | `REQ-007`, `REQ-009`; `GAP-004`, `GAP-005` | `decision-needed` |
| `FI-GAP-005` | Make the selected source revision unavailable or provide content that does not match its recorded digest. | Synchronization rejects the source before installation, preserves the previous good copy, and reports expected versus actual identity without executing recovered content. | `REQ-005`, `REQ-007`; `GAP-008` | `decision-needed` |
| `FI-GAP-006` | Supply a skill path that traverses outside the permitted project or machine install root, including a symlink/junction escape. | Validation rejects the path before copying or deleting anything outside the approved root and records the resolved target for evidence without following it for execution. | `REQ-005`; `GAP-008` | `decision-needed` |
| `FI-GAP-007` | Remove write permission or mark one managed output read-only. | Preflight or transactional write fails without leaving other managed files changed; diagnostics name the blocking path and required operation. | `REQ-008`; `GAP-006` | `decision-needed` |
| `FI-GAP-008` | Run synchronization in a dirty worktree that overlaps a managed file. | The command follows the approved dirty-worktree policy and never overwrites overlapping user changes silently. | `REQ-008`; `GAP-006` | `decision-needed` |
| `FI-GAP-009` | Start an MCP from a process working directory unrelated to the project. | The server receives the approved protocol/client/shim root; if no valid root is available, launch fails explicitly rather than using the unrelated directory. | `REQ-011`; `AC-CLIENT-006` | `source-derived` |
| `FI-GAP-010` | Withhold or revoke client trust/approval while configuration remains present. | Observation reports configuration present / approval absent / runtime not started, and does not classify the server as misconfigured solely because approval is absent. | `REQ-014`; `AC-CLIENT-005` | `source-derived`; detection API open |
| `FI-GAP-011` | Make a pinned package, container image, or host implementation unavailable or version-mismatched. | Validation/execution reports the exact unresolved pin or incompatibility and does not silently select latest or another platform implementation. | `REQ-007`, `REQ-010`; `AC-REP-008`, `AC-PLAT-004` | `source-derived` |
| `FI-GAP-012` | Run an unsupported or format-changed client version. | Capability detection reports unsupported or unknown; synchronization does not rewrite the format based on an unverified assumption. | `REQ-001`, `REQ-005`, `REQ-008`; `GAP-010` | `decision-needed` |
| `FI-GAP-013` | Put a secret literal in a declaration, launcher environment, generated file, command error, or observation fixture. | Validation or redaction prevents the literal from entering committed output, scan payload, stdout/stderr evidence, or durable logs; the test searches every captured surface. | `REQ-019`; `AC-PLAT-006` | `decision-needed`; secret model open |
| `FI-GAP-014` | Launch the same gateway from multiple supported clients concurrently, including an OAuth-backed downstream server. | Evidence records process/container count, OAuth state separation, memory, latency, log attribution, and cleanup; pass/fail uses approved quantitative budgets. | `REQ-012`; `AC-RUN-003`, `AC-RUN-004` | `decision-needed`; budgets open |
| `FI-GAP-015` | Terminate a client while its gateway/server process is active. | The approved lifecycle either cleans up the orphan within its timeout or reports the retained shared process as healthy and owned; no ambiguous orphan remains. | `REQ-012`, `REQ-014`; `GAP-011` | `decision-needed` |
| `FI-GAP-016` | Disable the central observation sink or return timeout, authentication failure, duplicate acknowledgement, or schema rejection. | Local normalized scan output remains complete; submission reports a distinct transport result and does not lose or duplicate observations under the approved retry/idempotency contract. | `REQ-015`; `AC-INV-006`; `GAP-013` | `decision-needed` |
| `FI-GAP-017` | Scan two worktrees and two clones of the same remote at different commits. | Every checkout remains separately observable while repository identity is shared according to explicit identity keys; no observation overwrites another accidentally. | `REQ-015`; `GAP-012` | `decision-needed` |
| `FI-GAP-018` | Make cross-repository automation succeed for some consumers and fail before others are updated. | The run records selected consumers and per-repository outcomes, never claims global completion, and can retry without duplicating successful PRs or skipping failed consumers. | `REQ-016`; `GAP-014` | `decision-needed` |
| `FI-GAP-019` | Attempt installation/removal while machine-global, plugin, project, and client-adapter copies of the same skill coexist. | The approved precedence/lifecycle contract identifies every copy, mutates only its owned surfaces, and leaves no silently shadowing stale copy. | `REQ-005`; `GAP-001`, `GAP-002` | `decision-needed` |
| `FI-GAP-020` | Present the claimed foundation artifact with a nonmatching SHA-256 or no recoverable provenance. | Donor intake rejects it as verified implementation evidence; no code or claimed test status enters the authoritative plan. | `REQ-022`; `GAP-018` | `source-derived` |
| `FI-GAP-021` | Modify a machine-global reconciled skill or an intentional tool-only skill, then run global reconcile. | Drift is reported with source/local digests; no modified or tool-only bytes are silently overwritten; the approved resolution path is required. | `REQ-024`; `AC-GLOBAL-004` | `decision-needed` |
| `FI-GAP-022` | Update a machine-global skill, then inject a failed discovery check and request rollback. | The previous good version, provenance, and client discovery are restored without mutating project/vendor or plugin-owned copies. | `REQ-024`; `AC-GLOBAL-005` | `decision-needed` |
| `FI-GAP-023` | Attempt to install or publish a gated/scout/personal-reference skill as active without promotion. | Validation refuses the operation before manifest/catalog/install mutation and identifies the governing tracker state. | `REQ-025`; `AC-PUB-001` | `current-authority-derived` |
| `FI-GAP-024` | Remove, expire, or invalidate an MCP credential while configuration and launcher remain present. | Observation reports the non-secret auth state separately; no value enters diagnostics; runtime launch either remains blocked or fails with the approved auth classification. | `REQ-014`, `REQ-027`; `AC-CLIENT-005`, `AC-CLIENT-008` | `decision-needed` |
| `FI-GAP-025` | Remove or corrupt one required committed native/generated artifact in a fresh checkout before running any renderer. | Fresh-clone validation reports the exact missing/invalid project artifact and does not misclassify machine-local approval/auth/launcher state as the cause; whether sync may repair it follows the approved clone-ready contract. | `REQ-026`; `AC-REP-009` | `confirmation-needed` |
| `FI-GAP-026` | Invoke an unknown/deprecated CLI command, incompatible JSON contract, or invalid option combination. | The CLI returns the approved stable usage/compatibility exit class, emits no misleading machine-readable success, and performs no mutation. | `REQ-017`; `AC-CLI-001`, `AC-CLI-002` | `decision-needed` |
| `FI-GAP-027` | Supply a malformed or ambiguous project declaration, including an invalid tool allowlist or duplicate logical identity. | Validation identifies the exact schema/semantic conflict before lock, render, install, or launch and leaves all managed surfaces unchanged. | `REQ-006`; `AC-REP-002`, `AC-RUN-005` | `decision-needed` |
| `FI-GAP-028` | Misclassify a portable, host-bound, or project-process MCP as another runtime category. | Validation/execution reports the category/implementation mismatch and does not silently fall back to another backend, root source, or machine path. | `REQ-018`; `AC-PLAT-002`, `AC-PLAT-003`, `AC-RUN-006` | `decision-needed` |
| `FI-GAP-029` | Start pilot entry with a missing declared repository, machine, client version, portable MCP, host MCP, or required evidence field. | The pilot remains not runnable and produces no partial-pass conclusion; the missing matrix element is reported against the frozen pilot declaration. | `REQ-020`, `REQ-021`; `AC-PILOT-ENTRY-001`, `AC-PILOT-ENTRY-002`, `AC-PILOT-MATRIX-001` | `decision-needed` |

## Gate policy

- Required failure IDs cannot be waived implicitly by a successful happy-path run.
- A case blocked by an open decision is `not runnable`, not `pass`.
- Pilot entry requires every approved `FI-REQ-*` case and every `FI-GAP-*` case promoted to normative status to pass in deterministic fixtures first.
- Pilot exit requires the same cases to pass on the declared Windows/Linux/client matrix.
- A gateway that connects successfully does not satisfy inventory, preservation, security, root-resolution, approval, or agent-effectiveness requirements (`pasted-text.txt:L1094-1104`).
