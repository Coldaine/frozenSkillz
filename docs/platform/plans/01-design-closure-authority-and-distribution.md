# Plan 1: Design Closure, Authority, and Distribution

> **Status:** draft / **superseded for v1 critical path** by
> [REFINED-V1.md](../REFINED-V1.md) (2026-07-21). Keep this file as the long-form
> decision checklist and backlog; do not treat completing every section as a gate
> before shipping project-native config persistence.
>
> Original status: draft plan. Evidence capture is substantially complete; authority
> and product decisions are not yet approved.

## Outcome

Produce an approved system contract that connects frozenSkillz's existing intake,
review, promotion, and publication lifecycle to the real places where agents discover
skills, while keeping marketplace/plugin installation, personal machine-global
installation, and project vendoring as distinct distribution lanes.

This plan ends with approved normative documents. It does not implement the control
plane, alter current manifests, or migrate live skill directories.

## Inputs

- [Planning evidence pack](../evidence/README.md)
- [Source ledger](../evidence/source-ledger.md)
- [Decision register](../evidence/decision-register.md)
- [Current/proposed authority and installation analysis](../evidence/authority-lifecycle-and-installation.md)
- [Supplemental control-plane architecture review](../evidence/supplemental-control-plane-review.md)
- [Requirements matrix](../evidence/requirements-matrix.md)
- [Interface inventory](../evidence/interfaces-and-schemas.md)
- Current `AGENTS.md`, tracker, external-intake workflow, authority/sync workflow,
  README, active plugin content, and all publication manifests

## Recommended authority candidate

The design should evaluate this as the leading steady-state model, not silently treat
it as approved:

1. Candidates may originate in personal roots, project repositories, or external
   sources, but enter frozenSkillz through its existing evidence and review gates.
2. `_incubator/` remains gated and non-installable.
3. After promotion, `plugins/frozen-skills/skills/<name>/` is the active reviewed
   reusable source and the manifests identify what is publishable.
4. Active content is then installed or reconciled into real discovery surfaces:
   plugin-managed runtime, selected personal machine-global roots, and/or a project
   vendor copy. Git checkout presence alone is never treated as installation.
5. Project forks, project-local skills, and project rules remain authoritative in
   project Git.
6. Client caches, compatibility mirrors, junctions, and generated adapters are
   derived execution surfaces with provenance and drift checks.
7. Machine-local launchers, credentials, client approval, and runtime health remain
   machine state rather than project or publication authority.

The alternative is to retain the current personal-live-first model, where ordinary
personal edits begin in `C:\Users\pmacl\.agents\skills` and reviewed reusable deltas
flow into frozenSkillz for publication. The user must explicitly select or modify the
steady-state model; the migration cannot be inferred.

A third option is a phased/per-artifact transition: each skill records its current
authority and target steady state, so frozen-only and live-first skills can migrate at
different times. This is useful for safety but must converge; "hybrid" cannot become
an undocumented permanent authority rule.

For presentation, evaluate the supplemental five-plane lens: governance/publication,
project intent, distribution/materialization, execution, and observation. It is only
useful if distribution remains a first-class responsibility and observations remain
stale-able facts rather than desired-state authority. The lens must not pre-decide
the active reviewed-source direction above.

## Phase 1A: Evidence closure

1. Finish the independent source-coverage, authority, and cross-document consistency
   audits of the evidence pack.
2. Classify each finding as correction, added requirement, factual verification,
   product decision, or deferred scope.
3. Recover and hash-verify the transcript-claimed foundation, or record it as
   unavailable and exclude it from implementation status.
4. Inventory the current active/gated skills, publication manifests, personal roots,
   client-specific copies/junctions, plugin installations, and obvious drift without
   modifying them.
5. Reconcile the current root MCP files and the hard-coded skill audit into the donor
   and verification ledgers.

**Exit gate:** every material source segment and current repository lifecycle stage
has a status and destination; no implementation claim remains ambiguous.

## Phase 1B: Authority and lifecycle decision

Write and approve explicit state machines for:

- candidate/scout -> gated -> review-ready -> active -> published -> installed ->
  observed current/drifted -> updated/deprecated/revoked/removed;
- clean vendor -> update available -> update PR -> current, or local modification ->
  blocked conflict -> restore/merge/convert to fork;
- desired project state -> lock -> materialized native state -> validation -> client
  approval -> healthy/unhealthy;
- host capability registration, version compatibility, launchability, and health;
- observation collection, redaction, optional submission, freshness, and expiry.

Close these decisions explicitly:

1. Active reviewed source authority and migration from the current live-first model.
2. Global plugin, personal, and project distribution lanes and precedence.
3. Copy, junction/link, plugin-native, and generated-adapter policy per client/OS.
4. Project rules versus reusable skills/templates.
5. `vendor`, `fork`, and `local` ownership and mode transitions.
6. Deprecation, revocation, rollback, uninstall, and stale-copy cleanup.

**Exit gate:** one lifecycle matrix names the authority, install target, update
direction, drift behavior, and removal behavior for every artifact class.

## Phase 1C: Public system contract

Resolve and specify, without contradictory aliases:

- project desired-state manifest and committed lock;
- active artifact/MCP catalog and version relationships;
- skill provenance and render-state representation;
- machine capability registry and allowed secret/environment references;
- client adapter contract and four distinct support matrices: publication,
  project rendering, machine-global discovery, and inventory-only;
- MCP logical identity, tool allowlists, namespace/collision policy, root binding,
  direct/gateway/project-process categories, and trust/health states;
- independently select managed discovery filtering for visibility/context shaping
  and call-time rejection for hard authorization; define each selected policy's
  defaults, errors, audit evidence, unmanaged/direct-route boundary, and whether
  sampling-driven tool use or other capabilities are outside scope or mediated;
- independent MCP session semantics, backend process/container sharing eligibility,
  auth/consent isolation, local daemon peer security, and cleanup;
- runtime root-source order/lifecycle and, separately, canonicalized containment
  within authorized roots; post-initialization client roots may narrow access but do
  not establish pre-launch identity or provide OS sandboxing;
- observation schema and optional transport boundary;
- CLI executable name, public commands, JSON I/O, exit codes, dry-run, conflicts,
  atomicity, and compatibility policy;
- cross-repository update contract, even if automation is deferred.

Every interface must include schema/version migration, source and consumer ownership,
stable identity, deterministic serialization where committed, secret redaction, path
safety, digest verification, unknown/unsupported states, and rollback behavior.

**Exit gate:** every approved requirement maps to an architecture owner, interface,
acceptance ID, plausible failure ID, and implementation phase.

## Phase 1D: Approval and repository transition plan

1. Present the design in bounded sections: governance/publication, project intent,
   distribution/materialization, execution, observation, security, and rollout.
2. Record user approval or correction for each section.
3. Run an adversarial review for unclassified contradictions, orphan requirements,
   untestable criteria, and accidental scope expansion.
4. Identify the exact current authority files that the approved transition changes.
5. Write a non-destructive migration procedure for existing `.agents` content,
   active frozen content, tool-only skills, plugin caches, and project copies.

**Plan 1 complete when:** the approved design can be implemented without choosing a
new authority rule, public filename, command, lifecycle state, support boundary,
tool-policy threat model, backend-sharing rule, root-security rule, or failure policy
inside implementation code.

## Explicit non-actions

- Do not modify active plugin content or manifests merely to demonstrate the design.
- Do not copy/delete current personal skills before migration and rollback are approved.
- Do not treat the three planning documents as an authority change.
- Do not select pilot repositories or machines to settle unresolved contracts.
- Do not incorporate the unattached claimed foundation unless recovered and verified.
