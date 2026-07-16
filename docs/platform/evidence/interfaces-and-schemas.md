# Interfaces and Schemas Inventory

> **Status:** non-authoritative inventory. Names and shapes below are requirements to
> resolve, not approved file formats or APIs.

The transcript alternates between `.agents/frozen.yaml`,
`.agents/frozen.lock.yaml`, and `.agents/config.yaml`; between `frozen` and
`frozenctl`; and between `render`, `sync`, and a larger command set. Those conflicts
remain open until one coherent contract is approved.

| ID | Contract | Authority and purpose | Minimum required content | Material open questions |
|---|---|---|---|---|
| IF-01 | Active artifact catalog | frozenSkillz publication state; identifies only reviewed installable skills/MCP definitions/templates | Stable ID, kind, source path, version/revision/digest, lifecycle state, compatibility, deprecation/revocation | Whether MCP catalog entries share plugin versioning; how external package/image pins relate to frozenSkillz revisions |
| IF-02 | Project desired-state manifest | Project Git; selects capabilities and provenance intent, never machine paths or secret values | Schema version, project identity, selected skills and ownership modes, selected MCPs/tools, supported clients, unusual native-rule paths | Final filename; inheritance; whether client matrix is declared or inferred; whether rules appear only as discovered metadata |
| IF-03 | Project lock | Project Git; resolves desired state reproducibly | Exact skill revision/digest, package/image versions, schema/catalog versions, selected tools, renderer/adapter compatibility | Separate file versus manifest section; regeneration rules; unknown/removed artifact behavior |
| IF-04 | Skill provenance state | Project or install sidecar; proves origin and drift without rewriting arbitrary skill prose | Artifact ID, source revision/digest, ownership mode, materialized paths, content hash, last sync result | Lock-only, adjacent sidecar, or injected frontmatter; mode transitions; deleted/renamed artifacts |
| IF-05 | Machine capability registry | Machine-local; maps project-selected logical MCPs to executable implementations | Logical ID, OS/architecture, command/backend, version facts, environment/secret handles, availability | Exact Windows/Linux locations; allowed command/path forms; registration authority; precedence and revocation |
| IF-06 | Client adapter contract | frozenSkillz code; isolates discovery paths and native formats by client/version | Detect, support check, target discovery paths, structural merge, scan, root binding, trust/health observation | V1 client/version matrix; unsupported-version behavior; copy versus junction policy; comment/ordering guarantees |
| IF-07 | Managed render state | Project-local generated state; bounds what sync owns and supports drift/rollback | Renderer/adapter version, input and output hashes, managed identities/subtrees, previous successful transaction | Committed or ignored; atomic multi-file protocol; concurrent UI edits; recovery after interruption |
| IF-08 | MCP execution shim | Installed executable; turns logical host-bound IDs into real processes | ID resolution, project-root input, version enforcement, environment/secret reference resolution, stable errors/exit codes | CLI executable name; Docker/direct routing; roots/list integration; concurrency/process reuse |
| IF-09 | Observation schema | Scanner output; records desired versus observed without becoming authority | Schema version, collection time, pseudonymous machine ID, repo/clone/revision, artifacts/scopes/provenance, clients, launchers, non-secret auth readiness, trust/health/drift/staleness, redacted errors | Path privacy, deduplication, multiple clones/worktrees, unknown/auth states, retention and schema negotiation |
| IF-10 | Observation transport | Optional machine-to-index submission, separate from scanning | Authentication, idempotency key, retries/backoff, offline queue, payload limits, server acknowledgement | Whether Obot is the sink; ownership; retention; deletion; fleet identity collisions |
| IF-11 | Cross-repository update contract | frozenSkillz/updater; produces ordinary consumer PRs after local sync semantics are proven | Consumer identity, eligibility proof, pinned source delta, deterministic generation, branch/PR policy, partial-failure log, rollback | GitHub App/workflow/script; authorization; stale consumer index; branch collisions; rate limits |
| IF-12 | CLI contract | User/CI boundary for lock, materialization, validation, MCP execution, and scanning | Syntax, stdin/stdout/stderr, JSON modes, exit codes, dry-run, conflict-resolution flow, transactional guarantees | `frozen` versus `frozenctl`; public verbs; whether `render` is internal to `sync`; compatibility aliases |
| IF-13 | Machine-global install selection and state | Machine/user desired selection plus reconciler state; connects reviewed source to real personal/client discovery roots without conflating those roots with source authority | Selected artifact/revision/digest, destination/client mapping, install method, provenance, previous good state, drift, deprecation/removal, rollback | File/registry location; global versus per-client selection; copy/junction/plugin policy; migration from existing live-first skills |
| IF-14 | Conformance evidence and pilot declaration | Versioned proof boundary fixed before deterministic or operational runs | Contract/harness version, required IDs, fixture/repository commits, machine/OS/client versions, input digests, commands/results, changed files, observed states, evidence paths, aggregation, waiver/abort/retention rules | Storage format/location, signature/attestation, privacy, evidence retention, waiver authority |

## Cross-cutting invariants

Every normative schema and interface must specify:

- a version and compatibility/migration policy;
- authoritative producer and consumers;
- stable identity and collision behavior;
- validation errors and machine-readable exit/status values;
- atomicity, concurrency, rollback, and partial-failure behavior where it writes;
- secret-value exclusion and diagnostic redaction;
- path traversal, symlink/junction escape, case-collision, and overwrite safety;
- deterministic serialization where committed output is expected;
- provenance and digest verification before installation or execution;
- explicit `unknown`/unsupported states rather than guessed success.

## Client matrices must remain separate

The design must not collapse these into an ambiguous claim of "all clients":

1. marketplace metadata/publication clients currently represented by frozenSkillz manifests;
2. clients with verified plugin installation and discovery behavior;
3. project configuration/rendering clients;
4. machine-global personal skill clients;
5. inventory-only clients and ecosystems.

Each matrix needs supported, experimental, and unsupported status plus the exact
client versions and fixtures used as evidence.
