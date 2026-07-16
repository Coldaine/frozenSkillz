# Platform Non-Goals and Boundaries

> Working architecture scratchpad. This file mixes current repository invariants,
> direct-user constraints, and candidate safety boundaries. Candidate items constrain
> nothing until approved; none claim that a control plane, CLI, catalog, scanner, or
> installer exists.

## Boundary status

- **Current repository invariants:** tracker/gating authority, read-only scout source,
  active plugin content/manifests as publication surfaces, and current live-personal
  source behavior remain in force now.
- **Direct-user constraints:** project rules stay project-owned; reviewed skills must
  be materialized into real discovery directories; the existing frozenSkillz
  lifecycle must be understood before redesign.
- **Candidate safety boundaries:** vendor/fork/local mechanics, generated-file
  ownership, launcher, inventory, security, and v1 exclusions below require explicit
  design approval before becoming normative.

## Repository Boundary

frozenSkillz remains a reviewed marketplace and intake boundary. A proposed platform
surface may extend its ability to publish, validate, distribute, and observe reusable
artifacts, but it must not turn the repository into an indiscriminate copy of every
client installation or project configuration.

The existing authority chain remains in force until deliberately changed:

1. `docs/skill-review/tracker.md` governs active, gated, scout, and promotion status.
2. External source intake follows the repository workflow and keeps scout sources
   read-only.
3. Active plugin skill files define installable behavior.
4. Marketplace and plugin manifests define public availability.

Any approved authority transition must update the router, tracker, external-intake
and sync workflows, affected active skill files, all four plugin manifests, all four
root marketplace catalogs, and public documentation together.

## Ownership Boundaries

| Owner | Owns | Does not own |
|---|---|---|
| frozenSkillz governance | Intake evidence, review status, promotion gate, active reviewed publication copy, manifests, versioning, reusable validation and scaffolds; active reusable source only if the authority transition is approved | Project intent, machine credentials, client trust, arbitrary installed caches |
| Project Git | Project-local skills, project forks, project rules, capability selection, and any committed generated client artifacts approved by the design | Machine-global credentials, approval state, or host executable paths |
| Machine-local state | Installed clients, discovery surfaces, launchers, credentials, secret values, approvals, runtime health, and local observations | Reusable review status or project desired state |
| Client/plugin manager | Its installation cache and runtime loading behavior | Authoritative reusable source or project intent |
| Observation/index service | Submitted observations, freshness, and comparison views | Desired state, automatic promotion, or authority over source files |

The phrase “derived runtime state” must never be read as “optional.” A skill still
has to be installed, copied, linked, or plugin-loaded into a discovery surface before
an agent can use it.

## Rules Boundary

Project rules are not reusable skills and remain in project-native locations such as
`AGENTS.md`, `.claude/rules/`, `.cursor/rules/`, `.github/instructions/`, and other
client-native surfaces.

frozenSkillz may:

- provide one-time scaffolds and reviewed examples;
- validate known rule formats and referenced paths;
- discover and inventory standard locations automatically;
- accept `rules.extra` for nonstandard project locations;
- propose reviewed updates through ordinary project pull requests.

frozenSkillz must not:

- continuously overwrite project rules from a central copy;
- assume one generic rule format preserves every client's activation and precedence;
- translate arbitrary rules between clients as a v1 platform feature;
- treat a project rule delta as reusable-skill drift.

## Skill Distribution Boundary

Marketplace/plugin installation, machine-global personal installation, and project
vendoring are different lanes.

- A marketplace plugin may install active skills into a client-managed runtime.
- A machine-global personal lane must reconcile skills into real client discovery
  roots or compatible mirrors.
- A project lane may vendor pinned shared skills and keep local/forked skills in
  project Git.

No lane may install gated `_incubator/` content without a promotion decision. No lane
may silently overwrite a modified vendor, project fork, project-local skill, or
intentional tool-only skill.

## Client Boundary

The repository's current publication clients are not automatically the same clients
supported by future project rendering or inventory.

Each client capability must be classified independently:

- marketplace/plugin publication;
- machine-global skill discovery;
- project skill discovery;
- MCP configuration rendering;
- rule discovery and validation;
- approval and runtime-health observation.

Client support claims require current documentation and fixture evidence. The design
must not claim universal `.agents/skills` discovery, universal rule semantics, or
identical precedence across clients.

## MCP and Machine Boundary

Project Git may select a logical MCP capability, but the machine owns its executable
implementation, credentials, approval, and runtime health.

The proposed platform is not general machine provisioning. It does not own package
manager policy, operating-system configuration, Docker installation, user accounts,
or arbitrary workstation bootstrap.

It may eventually define a narrow launcher contract that:

- resolves a reviewed logical MCP identifier to a host implementation;
- binds the correct project root without relying only on the current directory;
- checks availability and compatible version;
- passes secret references without storing secret values;
- reports explicit unsupported, unavailable, approval-pending, and unhealthy states.

No committed project file should contain personal absolute executable paths or secret
values. No machine registry has an effect unless an actual launcher reads it.

## Generated Configuration Boundary

If native client files are generated or structurally merged, the managed surface must
be explicit.

- Managed namespaced entries may be reconciled from project intent and a lock.
- Unmanaged servers and unrelated client settings must be preserved.
- Mixed files such as JSONC must not be destructively rewritten.
- Client UI edits to managed entries are drift, not a second source of truth.
- Idempotence and source/output hashes are validation concerns, not permission to
  erase unknown content.

Bidirectional synchronization from arbitrary client UI state is a non-goal. A future
workflow may import or explain a detected delta, but must require an explicit ownership
decision before changing source authority.

## Inventory Boundary

Local scanning and central indexing are separate responsibilities.

A local observation may describe repository identity, selected capabilities, installed
skills, native configuration, launcher availability, approval state, runtime health,
and drift. It must distinguish desired, configured, approved, healthy, unknown, and
stale states.

An index or UI may receive normalized observations, but:

- it is not the initial discovery engine;
- it does not become authority over project Git or reviewed source;
- it cannot infer downstream gateway contents from a wrapper entry without explicit
  observation data;
- it must not receive secret values;
- device identity, local paths, retention, authentication, and redaction require an
  approved data policy.

Full central inventory integration is not a prerequisite for defining a stable local
observation schema.

## Security and Trust Boundary

The platform must not:

- bypass client trust or approval dialogs;
- execute an unreviewed scout or gated artifact as part of validation;
- accept arbitrary commands from an untrusted project declaration;
- copy outside approved roots through path traversal, symlink, or junction escape;
- print, commit, or submit secret values;
- grant cross-repository automation direct write access to default branches;
- treat a successful process start as proof that configuration, trust, tool exposure,
  and behavior are all correct.

Publication, installation, launch, and observation are separate trust boundaries and
need separate failure reporting.

## Candidate Product Non-Goals

If approved for v1, the platform would not attempt to provide:

- generic machine provisioning or fleet configuration management;
- a new MCP protocol or replacement gateway;
- generic cross-client rule transpilation;
- automatic trust-dialog approval;
- blind bidirectional sync from client configuration UIs;
- automatic promotion of every live or discovered skill;
- automatic rewriting of project forks or local skills;
- a single universal skill directory for every client and operating system;
- one combined support claim for publication, project rendering, global discovery,
  and inventory;
- central inventory as authority over project or publication intent;
- implementation status based on an unattached archive, hash, transcript claim, or
  design document.

## Decisions That Remain Outside This Boundary Document

This file constrains the design but does not decide:

- the active reusable-skill authority transition;
- CLI name, commands, language, or packaging;
- project manifest and lock schema;
- exact per-client discovery targets and adapter behavior;
- copy versus junction versus plugin-native installation policy;
- direct MCP versus gateway routing;
- central observation backend;
- cross-repository update automation;
- migration order, rollout cohorts, or pilot repositories.

Those choices belong in an approved system contract after the current lifecycle and
proposed extension have been reconciled.
