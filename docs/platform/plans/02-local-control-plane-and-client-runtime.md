# Plan 2: Local Control Plane and Client Runtime

> **Status:** draft / **v1 backlog**. Critical path for agent-config persistence is
> [REFINED-V1.md](../REFINED-V1.md) deliverables D2–D3 (project native files +
> existing `sync_frozen_skills.py`), not this full control plane.
>
> Original status: draft and blocked on Plan 1 approval.

## Outcome

Implement the approved offline/local system that can resolve reviewed artifacts,
install or vendor them safely, render only owned native configuration, launch logical
MCP capabilities through stable machine resolution, and emit normalized local
desired-versus-observed state.

This plan deliberately stops before central observation, cross-repository automation,
and the operational pilot.

## Entry gates

- [Plan 1](01-design-closure-authority-and-distribution.md) is approved.
- Normative lifecycle, schema, CLI, security, client-support, and migration contracts
  exist outside the planning evidence pack.
- Every v1 requirement has acceptance and failure IDs.
- The claimed foundation, if used at all, has passed donor intake and clean tests.

## Phase 2A: Contract fixtures and executable skeleton

1. Check in versioned positive and negative fixtures for every approved schema.
2. Implement parsers/validators that reject unknown incompatible versions and unsafe
   paths before mutation.
3. Establish the approved CLI executable, stable machine-readable output, exit-code
   taxonomy, dry-run mode, and diagnostic redaction.
4. Record contract compatibility tests before adding client adapters.

**Exit gate:** schemas and CLI behavior are executable, deterministic, and have no
hidden fallback to transcript-era filenames or command aliases.

## Phase 2B: Transactional distribution and synchronization core

1. Resolve active reviewed versions and verify source revisions/digests.
2. Implement each approved lane separately:
   - marketplace/plugin publication/install handoff;
   - machine-global personal reconcile;
   - project vendor/fork/local materialization.
3. Implement provenance, ownership modes, clean-vendor update, modified-vendor
   conflict, fork/local preservation, deprecation/removal, and rollback.
4. Preflight all destinations and perform atomic multi-file updates with transaction
   recovery and compare-before-replace concurrency checks.
5. Reject path traversal, symlink/junction escape, case collision, out-of-root delete,
   unreviewed content, and digest mismatch.
6. Make unchanged repeated operations zero-diff.

**Exit gate:** repository, install, sync, provenance, transaction, conflict, and path
safety fixtures pass without any client-specific behavior.

## Phase 2C: Client discovery and native configuration adapters

For each exact supported client/version in the approved matrices:

1. Detect installation and supported format capabilities.
2. Materialize skills into the real global/project discovery locations using the
   approved copy/link/plugin policy.
3. Discover and validate project-native rule surfaces without generic transpilation.
4. Render or structurally merge only namespaced managed MCP entries.
5. Preserve unmanaged servers, unrelated settings, and the approved JSONC
   comment/order/format guarantees.
6. Detect cross-scope duplicates and report the effective client-specific winner.
7. Record configured, auth-required/auth-ready/expired, approval-pending, launchable,
   healthy, unhealthy, unsupported, and unknown states separately without recording
   credential values.

**Exit gate:** exact-version fixtures prove discovery and behavior, not merely file
existence, and an unsupported/new format fails without destructive rewriting.

## Phase 2D: MCP execution and root binding

1. Implement the stable logical-ID execution shim using the approved machine registry.
2. Resolve portable, host-bound, and project-process MCPs without allowing a project
   declaration to inject arbitrary commands.
3. Enforce pins and host minimum versions; missing or incompatible implementations
   fail explicitly without guessing.
4. Implement the approved root-source order and lifecycle rather than assuming cwd.
   If authorized-root containment is retained, canonicalize the selected root and
   enforce the approved boundary; handle post-initialization root-list changes without
   silently preserving stale broader access.
5. Hide Docker Gateway or another backend behind the stable platform interface.
6. Implement only the approved tool-policy guarantees and downstream gateway
   inventory. If discovery filtering is selected, cover every page/refresh; if hard
   authorization is selected, reject disallowed calls before backend dispatch.
7. If a managed proxy/session broker is retained, preserve an independent stateful
   MCP session for every managed client relationship. Reuse a backend process or
   container only for implementations declared and proven safe for isolated
   multi-session operation.
8. For retained broker/reuse capabilities, test simultaneous-client startup,
   transport-appropriate authorization isolation, request/callback routing,
   capabilities, roots, cancellation, notifications, process/container reuse,
   resource budgets, log attribution, timeout, shutdown, and orphan handling.

**Exit gate:** portable and host-bound fixtures pass on deterministic Windows and
Linux environments with correct roots, pins, exposure, failure classes, and cleanup.

## Phase 2E: Local normalized scanner

1. Discover in-scope repositories, clones, worktrees, native files, skills, rules,
   MCPs, clients, launchers, gateway downstreams, provenance, trust, health, and drift.
2. Preserve distinct repository identity and checkout identity across duplicate clones
   and worktrees.
3. Emit the approved versioned JSON schema locally even when no sink exists.
4. Redact secret values and apply the approved local-path/privacy classification.
5. Wrap or replace the hard-coded `skill-audit.sh` engine while retaining the approved
   legacy coverage fixture.
6. Adapt only proven scanner/redaction components from `ai-config-registry`; do not
   inherit its authority or desired-state semantics.

**Exit gate:** local output matches a bounded hand-built golden inventory with the
approved precision/recall rule and remains complete when all network sinks are absent.

## Phase 2F: Deterministic pre-integration conformance

Automate all approved repository, merge, client, platform, runtime, inventory,
security, and failure-injection cases that do not require a central service or real
consumer PRs. Required cases include vendor drift, stale MCP collision, missing host
launcher, stale clone, malformed JSONC, mixed settings/comments, fork conversion,
gateway downstream discovery and every retained conditional runtime case, including
direct tool-policy bypass, paginated tool refresh, authorization isolation,
cross-session ID/cancellation isolation, dynamic root narrowing, and runtime path
escape; also interrupted sync, concurrent modification, unavailable pins, secret
injection, install-path escape, unsupported clients, and duplicate clones.

**Plan 2 complete when:** the local system and all declared adapters pass deterministic
fixtures on Windows and Linux, produce a reproducible evidence bundle, and leave no
required local case blocked or mislabeled as pass.

## Explicit non-actions

- No central sink is required for local scan correctness.
- No cross-repository update PR is opened in this plan.
- No pilot machine/repository is used to compensate for a missing fixture.
- No client parity is claimed without an exact-version behavioral fixture.
- No installation lane mutates a surface owned by another lane.
