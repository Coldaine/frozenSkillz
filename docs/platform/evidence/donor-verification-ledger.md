# Donor Verification Ledger

> **Status:** non-authoritative candidate inventory. Nothing listed here is approved
> for import, and no whole-repository merge is implied.

Apply the existing external-intake rule to every external donor: inventory before
judgment, isolate source evidence, run narrow evaluations, and adapt only the useful
concept. The default outcomes are `adapt`, `fixture`, `defer`, or `reject`, not bulk
merge.

| Donor/evidence source | Current evidence | Potentially reusable element | Current disposition | Required next proof |
|---|---|---|---|---|
| Current frozenSkillz tracker, intake workflow, active plugin manifests, and marketplace catalogs | Present in this branch and authoritative for current lifecycle/status | Gating, promotion bar, active publication, aligned manifests/versioning | `integrate-as-current-truth` | Model installation, update, drift, deprecation, rollback, and removal without weakening the existing gate |
| `scripts/skill-audit.sh` and `docs/skill-audit-2026-06-07.md` | Present; hard-coded to `hephastus` and `/d/_projects` | Skill-surface vocabulary and a backward-compatibility fixture | `fixture-and-retire-engine` | Define normalized discovery and prove equivalent-or-better bounded results |
| Root `mcp/notebooklm.json` and `mcp/github.json` | Present; current lifecycle/consumer status not yet reconciled | Seed evidence for logical MCP catalog decisions | `verify` | Determine whether each is active, stale, placeholder, secret-safe, pinned, and consumed |
| `D:\_projects\ai-config-registry` at local commit `2b47e76` | Local repository exists; 31 tests passed on 2026-07-16 using `.venv\Scripts\python.exe -m pytest -q` | Scanner parsers, redaction/security tests, normalized inventory vocabulary, report/dashboard fixtures | `adapt-narrowly` | Map its output to the proposed observation contract; do not treat it as project desired state, lock, renderer, launcher, or reconciliation engine |
| `D:\_projects\portfolio-control-service-demo` at local commit `11320e7` | Local repository exists; earlier survey identified evidence/reporting patterns, but this ledger has not re-evaluated them | Evidence bundles, status schemas, report presentation | `evaluate` | Select exact files, record license/provenance, and run a narrow packaging evaluation |
| `D:\_projects\ProjectBroadsideStudio` at local commit `300aa9f` | Local repository exists | Project-owned rules/configuration fixture and generated-artifact behavior | `fixture-candidate` | Identify exact native client surfaces and ensure test data can be safely minimized |
| `D:\_projects\comet-kvm-codex-plugin` at local commit `bbe7c33` | Local repository exists | Codex/plugin project fixture and host-bound capability examples | `fixture-candidate` | Inventory current config paths and separate project intent from machine-local KVM facts |
| `D:\_projects\TechdealsHandoff` at local commit `f82248c` | Local repository exists | Mixed project settings and operational configuration fixture | `fixture-candidate` | Identify non-secret, stable fixture slice and ownership boundaries |
| `NetworkConfig`, `dcc-mcp-core`, remote `agent-control-plane`, `coldain-infra-archive`, `ColdReviewer`, `chronograph`, and `oh-my-openagent` | Surfaced by repository surveys; not re-verified in this working branch | Plan/apply/verify, MCP abstractions, inventory, review, and client-surface patterns | `defer-pending-scout` | Resolve exact repo identity/commit, inventory scoped files, license/provenance, and compare against current contracts |
| Local directory `D:\_projects\TokenRouter` | Directory exists at commit `c746e2b`, but its origin reports `https://github.com/tashfeenahmed/freellmapi` | No reliable donor conclusion yet | `identity-conflict` | Reconcile directory name, remote identity, and intended candidate before using any evidence |
| Branch `codex/agent-tool-config-router` in frozenSkillz | Exists separately from this branch; candidate is gated/in development rather than active publication | Inventory/router vocabulary and session-format research | `evaluate-after-merge-state-clear` | Avoid coupling this design branch to unmerged commits; inspect its final reviewed state later |
| Claimed downloadable control-plane foundation | Transcript lines 957-983 claim code, tests, and SHA-256 `b75cd5f21879db4e3b19e48261770c3cc5edae796986a6692abb5a8996bd77a9`, but provide no path, URL, archive name, commit, diff, or test output | Potential schemas, fixtures, CLI, and CI only if recovered exactly | `unverified-claim` | Recover artifact, verify bytes against the hash, inspect as untrusted code, rerun tests, and compare to approved contracts; otherwise mark unavailable |

## Adoption rule

No donor determines architecture by existing first. Contracts and acceptance criteria
come first. A donor is useful only when a specific artifact can satisfy a named
requirement without importing stale authority, project-specific assumptions, secret
surfaces, or incompatible lifecycle semantics.
