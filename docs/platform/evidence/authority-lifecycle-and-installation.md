# Authority, Lifecycle, and Installation

> Working architecture scratchpad. This file records current repository truth,
> proposed extensions, and unresolved decisions. It is not an authority change and
> does not claim that the proposed platform exists.

## Why This Needs Reconciliation

The current repository already has a review and publication lifecycle. The proposed
platform adds project selection, installation, client discovery, and observation.
Those concerns must be connected without implying that an agent can consume a skill
directly from the frozenSkillz Git checkout.

Source authority and execution location are separate questions:

- **Source authority** identifies the copy from which reviewed changes are approved.
- **Publication authority** identifies what frozenSkillz offers through its manifests.
- **Installation state** identifies the copies or links placed where clients discover them.
- **Project authority** identifies project-local skills, forks, rules, and selections.
- **Observation state** reports what is present; it does not become authority over intent.

## Current Documented Lifecycle

The following is current repository truth, not a proposal:

1. `docs/skill-review/tracker.md` is the source of truth for active, gated,
   scout, and promotion status.
2. External scout snapshots remain read-only under `_incubator/scout/`. External
   intake requires inventory, narrow scope, rubric scoring, at least one sandboxed
   live evaluation, a packaging decision, and frozenSkillz-owned adaptation; scout
   source is never simply moved into active content.
3. Personal reference intake under `_incubator/personal-skills/` is a distinct gated
   evidence lane, separate from external scout source and ordinary gated marketplace
   candidates.
4. Gated skills remain under `_incubator/` and are not installable or listed in the
   active plugin `skills[]` arrays.
5. Promotion moves or adapts a reviewed skill into the appropriate active plugin
   `skills/` directory, adds it to all four plugin manifest `skills[]` arrays, bumps
   the plugin version, and updates the tracker. Root marketplace catalogs register
   plugins rather than individual skills; their plugin entry/version/description is
   synchronized separately when public plugin metadata changes.
6. Catalog registration, reviewed/active status, installation, enablement, and
   runtime loading are independent axes. `skill-injector` is the current proof: it is
   registered experimental/untested content but is not installed, enabled, or loaded.
7. Active frozen-skills content lives under
   `plugins/frozen-skills/skills/<skill-name>/` and must be registered in the
   supported plugin manifests.
8. On the documented Windows workstation, personal shared skills are currently
   authored and installed under `C:\Users\pmacl\.agents\skills`.
9. The frozen copy is currently the reviewed, publishable copy, while the live
   `.agents` copy remains the source for ordinary personal-skill edits. An active
   frozen skill with no live counterpart is an explicit exception for which
   frozenSkillz is already the source.
10. A live skill is not automatically promoted. Broad reuse, the promotion bar,
   manifest changes, versioning, and validation still apply.

There is a current documentation defect to preserve visibly until fixed: the tracker
says promotion updates "all three" root marketplace catalogs, while the router,
README, and filesystem identify four catalog formats. The tracker remains the status
authority, but its count is stale and must not be copied into the new contract.

### Current publication snapshot (2026-07-16)

| Surface | Current state |
|---|---|
| Active reviewed frozen skills | `doppler`, `external-skill-intake` |
| Registered experimental plugin | `skill-injector`; cataloged but not installed, enabled, or runtime-loaded |
| frozen-skills plugin version | `2.1.0` in the four plugin manifests |
| Root catalog metadata version | `2.2.0`; a different version namespace from the plugin version |

This lifecycle is documented in `AGENTS.md`,
`docs/skill-review/tracker.md`, and
`docs/workflows/skill-authority-and-frozen-sync.md`. Any future authority change
must update those surfaces together instead of creating a competing architecture
document.

## Proposed Lifecycle Extension

The proposal preserves the existing intake and promotion gate, then adds a **new**
frozen-to-install/materialize lifecycle that current authority does not document:
explicit
publication, materialization, and observation stages:

```text
candidate or external source
  -> scout/reference capture
  -> gated evaluation copy
  -> review and promotion decision
  -> active reviewed plugin source
  -> versioned marketplace/plugin publication
  -> installation or project materialization
  -> client discovery and approval
  -> runtime health and drift observation
  -> reviewed update, fork, deprecation, or removal
```

Intake, gating, review, active source, and plugin metadata have repository procedures.
Frozen-to-personal-global install/update/remove, project vendoring, client discovery,
runtime observation, and cross-surface cleanup are proposed platform responsibilities
and do not currently exist as one documented lifecycle.

The extension must preserve these invariants:

- `_incubator/` content never becomes installable merely because it exists in Git.
- Promotion remains a reviewed, manifest-aware, versioned action.
- Installed copies are necessary execution surfaces even when they are not the
  durable source of an active reusable skill.
- Project-local skills and project forks remain owned by project Git.
- Project rules remain in project-native locations; frozenSkillz may scaffold,
  validate, inventory, and offer reference patterns without continuously replacing them.
- Observation reports presence, provenance, approval, health, and drift without
  changing desired state.

## Authority Transition Question

Current documentation gives the live personal `.agents\skills` copy ordinary edit
authority and treats frozenSkillz as the reviewed publication copy. The proposed
cross-machine model appears to require a different steady state for active reusable
skills.

The decision to confirm is a lifecycle-object matrix, not necessarily one immediate
global flip:

> After transition, does frozenSkillz Git own the active reviewed source for a
> reusable skill, with machine-global, plugin-managed, and project-vendored copies
> treated as installed or materialized execution state, while project forks and
> project-local skills remain authoritative in project Git?

This is not a choice between “Git” and “a directory.” Agents still require files in
their real discovery directories. The choice is which lifecycle stage owns changes
and how reviewed content is reconciled into those required directories.

A phased/per-artifact transition is valid if every artifact has an explicit current
authority and target steady state. For example, an active frozen-only skill and a
personal live-first skill may migrate at different times. Hybrid transition state must
not become permanent ambiguity.

### Provisional authority matrix

| Lifecycle object | Current documented authority | Proposed steady-state authority | Status |
|---|---|---|---|
| External scout source | External origin; frozen snapshot is read-only evidence | Same | Preserve |
| Gated marketplace candidate | Tracker governs status; location is `_incubator/` | frozenSkillz review copy and tracker | Clarify for personal-skill intake |
| Active reviewed reusable skill | Live `.agents` copy normally leads; frozen copy is publishable | Active frozenSkillz plugin source | **Authority transition required** |
| Marketplace/plugin metadata | frozenSkillz manifests and versions | Same | Preserve and extend |
| Personal shared skill on this workstation | `.agents\skills` is currently both authored and installed | Client-discoverable installed copy with explicit selection/provenance/reconcile state | Materialization required; source/update direction depends on transition |
| Plugin-installed copy/cache | Client or plugin runtime surface | Derived installation state | Preserve as non-authoritative runtime |
| Plugin/package-provided skill | Package/plugin origin; excluded from personal intake when appropriate | Derived install governed by its package/plugin lane | Preserve and inventory separately |
| Intentional tool-only skill | Tool-specific real root by exception | Explicit tool-owned source or reconciled install, never silently classified as drift | Decision needed |
| Project-vendored shared skill | Not yet defined as a platform lifecycle | Project commit pins a reviewed upstream revision; mode is `vendor` | Proposed |
| Project fork or local skill | Project Git | Project Git | Preserve |
| Project rules | Project Git and native rule locations | Project Git and native rule locations | Preserve |
| Machine launcher, credentials, approval, health | Machine-local | Machine-local | Preserve and formalize |
| Central inventory record | Not yet a repository authority | Observation only | Proposed |

## Distribution and Discovery Lanes

The architecture needs three separate distribution lanes. They may share catalog
metadata and validation, but they do not have identical targets or ownership.

### 1. Marketplace/plugin lane

**Input:** active reviewed skills and aligned marketplace/plugin manifests.

**Distribution:** Claude Code has a documented marketplace/install command in the
current README. Codex, Cursor, and Gemini metadata surfaces exist in the repository,
but these authority files do not prove equivalent install/discovery behavior.

**Discovery:** where a verified client/plugin mechanism exists, its cache path is
client-managed and must not be treated as an authoring location. Other formats remain
metadata/publication candidates until current docs and fixtures prove installation.

**Authority:** active plugin source and publication metadata remain in frozenSkillz;
the installed plugin copy is derived runtime state.

The current repository metadata matrix includes Claude, Codex, Cursor, and Gemini
manifests. Verified installation is presently a narrower matrix. Both are distinct
from any future project-configuration adapter matrix.

### 2. Machine-global personal lane

**Current Windows targets:**

| Surface | Current documented role |
|---|---|
| `C:\Users\pmacl\.agents\skills` | Canonical live personal skill root and real installed copy |
| `C:\Users\pmacl\.claude\skills` | Claude compatibility mirror; personal skills should normally be junctions to `.agents\skills` |
| `C:\Users\pmacl\.config\opencode\skills` | OpenCode-specific real root, normally empty unless intentionally tool-only |
| `C:\Users\pmacl\.codex\skills` | Codex system/runtime surface; not a personal authoring root |
| `.gemini\skills`, `.cursor\skills`, `.kilo\skills` | Tool-specific roots; independent copies are possible drift unless intentionally tool-only |

**Proposed extension:** if active reusable authority moves to frozenSkillz, an install
or reconcile operation must materialize the selected reviewed versions into the real
global discovery targets. The design must decide where copies, directory junctions,
or client-native plugin installation are appropriate. It must detect local drift and
must not silently erase intentional tool-only content.

### 3. Project lane

**Input:** a project-owned declaration and lock selecting reviewed shared skills and
project-local capabilities.

**Distribution:** shared skills are proposed to be vendored into the project at a
pinned revision. Project-local skills and forks remain authored in the project.

**Discovery:** `.agents/skills/` may be the canonical project copy, but each supported
client still needs a verified discovery target or adapter. No universal discovery
path should be assumed. Cross-platform projects should prefer deterministic generated
copies over committed Windows-specific junctions or fragile symlinks.

**Authority modes:**

- `vendor`: reviewed upstream source plus a pinned, updateable project copy;
- `fork`: began from a shared skill but is now project-owned;
- `local`: originated in the project and has no automatic upstream relationship.

The project lane must keep project rules separate from reusable skills. Standard rule
locations should be discovered automatically; only nonstandard locations need an
explicit `rules.extra` declaration.

## Reconciliation Flows

### Current live-to-frozen flow

```text
live .agents skill
  -> compare with active or gated frozen copy
  -> evaluate broad reusability and promotion bar
  -> update active frozen source or leave the delta local
  -> update manifests/version when promotion changes public content
```

### Required materialization flow, independent of source-authority choice

```text
selected reviewed source under the approved authority model
  -> versioned publication, global selection, or project lock
  -> client-specific installation/materialization
  -> discovery/approval check
  -> drift and health observation
  -> reviewed update or explicit fork/local resolution
```

The materialization contract is required even if personal authoring remains live-first:
agents and clients still need verified discovery surfaces, compatible mirrors, plugin
installation, or project copies. The authority transition controls source/update
direction, not whether installation exists. Any transition plan must support both
flows long enough to inventory and reconcile existing live copies and must not flip
authority by deleting or overwriting the live tree.

## Unresolved Decisions

1. Confirm or reject the proposed active-skill authority transition.
2. Define the transition state for a personal skill that exists in live `.agents`,
   `_incubator/personal-skills`, and an active plugin path with different content.
3. Decide whether machine-global personal installation uses copies, junctions,
   plugin-native installation, or a client-specific combination.
4. Define the exact global and project discovery targets for every supported client
   and OS, with versioned verification evidence.
5. Separate and name the marketplace publication matrix, project adapter matrix,
   machine-global discovery matrix, and inventory-only matrix.
6. Decide the project declaration and lock filenames and which generated artifacts
   are committed.
7. Decide where provenance and drift hashes live; do not assume nonstandard
   `SKILL.md` frontmatter is portable.
8. Define update behavior for clean vendor copies, modified vendor copies, forks,
   local skills, and intentionally tool-only global skills.
9. Define publication rollback, deprecation, revocation, and uninstall behavior.
10. Define what observation data may leave a machine and how stale observations are
    represented.
11. Correct the tracker/catalog-count mismatch and define plugin-manifest versus root-
    catalog version/update rules.
12. Include the external-intake workflow, active skill files, all four plugin
    manifests, and all four marketplace catalogs in any approved authority migration.
