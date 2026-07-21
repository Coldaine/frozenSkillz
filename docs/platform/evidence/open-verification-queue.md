# Open Verification Queue

> **Status:** factual research queue. Product and authority choices belong in the
> decision register, not here.

| ID | Claim or surface to verify | Required evidence | Why it blocks design confidence |
|---|---|---|---|
| VQ-01 | Recover the SHA-identified control-plane foundation, or establish that it is unavailable | Exact artifact path/URL/name, SHA-256 match, source inventory, clean test rerun | The transcript otherwise overstates implementation progress |
| VQ-02 | Enumerate current machine-global skill roots and their real copy/junction/cache state | Read-only filesystem inventory with target resolution, hashes, client ownership, and drift classification | Distribution cannot be designed from assumed discovery paths |
| VQ-03 | Verify supported clients' project and global skill/rule/MCP discovery and precedence | Current official docs plus minimal fixtures on exact installed versions | Transcript client claims are time-sensitive and partly self-contradictory |
| VQ-04 | Separate publication, project-rendering, personal-global, and inventory-only client matrices | Manifest inspection, installed client/version inventory, and fixture results | Current repository and transcript name different client sets |
| VQ-05 | Reconcile root `mcp/*.json` files | Consumer search, package/version resolution, secret scan, launch test where safe | Their status determines catalog migration and loose-end cleanup |
| VQ-06 | Verify Docker MCP Gateway's current CLI, catalog/profile behavior, lifecycle, OAuth, logging, and concurrent-client process model | Current official documentation and controlled Windows/Linux process tests | The wrapper contract must hide real instability without inventing behavior |
| VQ-07 | Verify Obot ingestion/index/UI capabilities and constraints | Current API/schema/auth docs or a live disposable integration | Obot is only a candidate sink; persistence and transport cannot be assumed |
| VQ-08 | Map `ai-config-registry` output and security behavior to a bounded observation-schema candidate | Current scanner run, golden output, redaction tests, gap matrix | It is a tested scanner prototype, not the proposed control plane |
| VQ-09 | Define and verify compatibility expectations for `scripts/skill-audit.sh` | Golden legacy report plus normalized new-scan comparison | Replacing hard-coded discovery must not silently lose useful coverage |
| VQ-10 | Resolve donor repository identities and exact commits | `gh repo list`, remotes, commit IDs, licenses, scoped inventories | Earlier surveys are discovery, not adoption evidence |
| VQ-11 | Verify actual project-root mechanisms per supported MCP client | Protocol roots behavior, client variables, shim invocation, cwd failure fixtures | `.` was explicitly rejected and fallback order needs evidence |
| VQ-12 | Inventory current trust/approval and health observability per client | Read-only client state/API evidence and controlled launch results | Configured, approved, and healthy must remain distinct even when a client exposes no detection API |
| VQ-13 | Establish source-transcript retention policy | User decision on committing the full source versus retaining only hash/line ledger, plus secret/privacy scan | The attachment path is not a durable repository artifact |
| VQ-14 | Verify update-consumer discovery surfaces | Repository manifests, code search, clone inventory, and GitHub authorization boundaries | Cross-repository PR automation must target real consumers only |
| VQ-15 | Re-verify any named competitive or IDE-sync positioning immediately before public use | Current primary documentation and dated capability matrix for Smithery, MCP-Get, relevant proxies, VS Code, Cursor, and any other named product | Time-sensitive marketing comparisons must not become architecture assumptions or stale public claims |
| VQ-16 | Verify the managed proxy/session contract against every selected client and reusable backend | Exact client/backend/version fixtures covering stdio startup, initialization/capabilities, roots, auth, IDs, callbacks, cancellation, notifications, tool-list changes, disconnect, and process/container reuse | Generic MCP semantics do not prove that a particular client/backend pair can be mediated or safely shared |

## Evidence discipline

- Record exact version, date, path/URL, command, result, and limitations.
- Prefer current official documentation for client, protocol, Docker, and Obot facts.
- Use fixtures to prove discovery and precedence; file existence is not activation.
- Treat `unknown` as a supported result when a client exposes no trustworthy signal.
- Do not let verification silently choose an authority or product policy.
- Route every resolved item to the decision register, interface contract, donor ledger,
  or conformance case it changes.
