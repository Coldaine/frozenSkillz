# Supplemental Control-Plane Architecture Review

> **Status:** non-authoritative planning evidence. This review preserves useful
> material from a second user-supplied architecture note without accepting the
> note's claim that it is canonical.

## Source metadata

| Field | Value |
|---|---|
| Captured source | `C:\Users\pmacl\.codex\attachments\e02c11ce-7010-490a-8d14-ea3bace784df\pasted-text.txt` |
| Size | 17 physically collapsed lines; 8,176 bytes |
| SHA-256 | `D7C20EDDB06DF94914686B64CFFD161E5BFE78140B1E2AE0E894C1CAB827358B` |
| Evidence notation | `supplement:Lx-Ly`, using one-based physical line numbers from the captured source |
| Capture date | 2026-07-16 |
| Treatment | User-supplied secondary architecture reference; statements remain proposals until reconciled and approved |

The file calls itself a canonical blueprint, but a source cannot promote itself into
repository authority. Current authority remains the router, tracker, workflows,
active plugin content, and publication metadata identified in the
[platform router](../README.md). This document records the differential between the
supplement, those authorities, and the existing planning evidence pack.

## Result at a glance

Most of the supplement is already represented: project-owned specialization,
committed native files, structural merge, `vendor`/`fork`/`local` ownership,
logical host launchers, tool selection, local scan output, optional observation
sinks, consumer update PRs, and the proposed failure profile.

Three additions are worth preserving:

1. Decide the tool-policy guarantees independently. Filtering discovery is visibility
   and context shaping; rejecting disallowed dispatch is the authorization boundary.
2. Define cross-client MCP session isolation before allowing process or container
   reuse. Sharing a backend process is not the same as sharing one protocol session.
3. Replace root deny-lists with canonicalized containment inside explicitly
   authorized project/workspace roots and fail before launch when containment cannot
   be proved.

## Disposition matrix

| Supplemental element | Disposition | Reconciled treatment |
|---|---|---|
| Definition / intent / execution / observation framing | `adapt` | Use a five-plane presentation so distribution is not omitted: governance/publication, project intent, distribution/materialization, execution, and observation. These are responsibility planes, not five interchangeable sources of truth. |
| "Configuration last mile" thesis | `retain-as-positioning-candidate` | A safe thesis is that frozenSkillz reconciles reviewed reusable artifacts and project intent into verified client discovery and execution state. Named competitive claims require current evidence immediately before publication. |
| Project-native files committed for clone readiness | `retain-bounded` | Preserve the existing candidate promise of configuration-complete clones. Do not imply that machine credentials, trust, launchers, or runtime health are present. |
| `frozen`/`frozenctl`, `sync`/`render`, exact YAML filenames | `keep-open` | The note supplies preferences, not backward-compatibility evidence. One public name and command model must be explicitly selected. |
| Tool filtering in `tools/list` plus blocking `tools/call` | `add-as-open-security-contract` | Discovery filtering reduces context; call-time blocking is the enforcement point. The user must decide which guarantees the managed proxy makes; either may be specified without pretending that hiding alone is access control. |
| One daemon and one backend container for all IDEs | `defer-as-conditional-optimization` | Preserve independent MCP client sessions. Reuse a process/container only for backend types that declare and prove safe multi-session behavior. |
| Preventing "duplicate OAuth state" through reuse | `reject-wording` | HTTP authorization transactions require unique single-use state and per-flow PKCE, audience/resource binding, secure token storage, and explicit consent/identity rules. Token passthrough or cross-audience reuse is prohibited. Stdio credentials use a separate machine secret/environment contract. |
| `roots/list`, client environment, then cwd deny-list | `adapt` | Client roots may confirm or narrow allowed roots but do not by themselves establish project identity or OS containment. Canonicalize and prove containment within authorized roots; otherwise fail closed. |
| Central "Frozen Renovator" GitHub App | `defer-name-and-mechanism` | Keep `DR-032` and `IF-11` mechanism-neutral until local sync, consumer discovery, permissions, retries, deterministic diffs, and rollback pass. |
| Exact client file tree | `fixture-candidate` | Verify every path and client version before adding it to a supported matrix. Presence of a file does not prove discovery or activation. |
| Seven named failure tests | `retain-as-minimum-profile` | Map them into the broader fault catalog. The one-backend assertion is conditional on the sharing decision; tool-jailbreak and runtime-root cases need explicit additions. |

## Five responsibility planes

This is a presentation lens for the still-open design, not an authority decision:

| Plane | Candidate responsibility | Must not be confused with |
|---|---|---|
| Governance and publication | Review, gate, promote, version, and publish reusable definitions in frozenSkillz | Proof that an artifact is installed or discovered |
| Project intent | Project-owned capability selection, native rules, project-local skills, and committed reproducible state | Machine executable paths, credentials, or global selection |
| Distribution and materialization | Reconcile approved artifacts into plugin-managed, machine-global, project-vendored, and client-adapter discovery surfaces with provenance | Source authority or runtime health |
| Execution | Resolve machine capabilities, launch managed MCP traffic, enforce approved runtime policy, and report launchability | Project capability selection or desired-state authority |
| Observation | Record local desired-versus-observed facts and optionally submit them to an index | An always-current source of desired state or proof of correctness |

The active reviewed-source direction within the first plane remains the authority
transition question in `DR-006`; the distribution plane is mandatory regardless of
which source-authority model is selected.

## MCP protocol and security reconciliation

Current official MCP material confirms that tools are discovered with `tools/list`
and invoked with `tools/call`; discovery is paginated and servers can notify clients
that the tool list changed. It also defines a stateful initialization and capability
negotiation for each client/server connection. The protocol does not standardize a
shared local daemon that multiplexes several IDE stdio sessions into one initialized
backend session.

Relevant primary references:

- [MCP architecture and connections](https://modelcontextprotocol.io/specification/2025-11-25/architecture)
- [MCP lifecycle and capability negotiation](https://modelcontextprotocol.io/specification/2025-11-25/basic/lifecycle)
- [MCP tools](https://modelcontextprotocol.io/specification/2025-11-25/server/tools)
- [MCP roots](https://modelcontextprotocol.io/specification/2025-11-25/client/roots)
- [MCP transports](https://modelcontextprotocol.io/specification/2025-11-25/basic/transports)
- [MCP security guidance](https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices)

If a full managed proxy is approved, its contract must cover at least:

- an independent client-facing MCP session per managed MCP client-to-proxy connection;
- request/response ID routing, cancellation, progress, tasks, notifications, and
  server-initiated requests;
- per-session protocol version, capabilities, roots, logging, and auth context;
- separately specified fail-closed behavior for discovery policy and dispatch policy;
- filtering every `tools/list` page and every list-change refresh when discovery
  filtering is selected;
- rejecting a disallowed `tools/call` before backend dispatch with a stable,
  protocol-valid, non-secret error when hard authorization is selected;
- an explicit policy scope: server tools exposed through `tools/list`/`tools/call`
  only, or additional mediation for sampling-driven tool use and other capabilities;
- no arbitrary backend-launch executable, shell fragment, launch argument, or
  environment expansion from project-controlled input;
- same-user authentication and endpoint permissions for any local socket or named
  pipe;
- protocol-only stdout for stdio and redacted diagnostics/audit evidence.

Process or container reuse may be an implementation optimization behind that
contract. It cannot weaken any of those session boundaries.

## Root safety correction

The supplied hard-coded deny-list (`/`, `/etc`, `/usr`, `/tmp`, and `C:\Windows`) is
neither complete nor portable. It can reject legitimate worktrees while still
missing symlink, junction, reparse-point, UNC, device-path, drive-alias, case, mount,
or encoded escapes.

The candidate safety invariant is:

1. select the intended project/root through the approved root-source contract;
2. resolve and canonicalize the candidate root using platform-aware link and alias
   handling;
3. require containment inside an explicitly authorized root set;
4. after initialization, allow roots from a client that advertised the capability to
   confirm or further narrow that set, and define how later root-list changes affect
   an active backend;
5. refuse launch before starting the backend if the root is absent, ambiguous, or
   outside the set.

`roots/list` is a server-to-client request after capability negotiation, so it cannot
be required to establish pre-initialization launch identity. If a later
root-list-change removes or narrows an active root, the approved lifecycle must
constrain, restart, or terminate the affected session rather than silently continuing
with stale access.

MCP roots communicate intended filesystem boundaries; they are not an OS sandbox.
Actual containment of a local process needs permissions, sandboxing, or containers.

## External-positioning verification

The supplement's named comparisons should not enter a normative plan. Current
primary sources show that Smithery manages connection/auth/session/tool-call
lifecycle, not merely binaries; MCP-Get supports discovery, installation, updating,
and removal; and VS Code currently supports workspace and user MCP configuration,
discovery, trust, and some Settings Sync behavior. The useful product boundary is
therefore the narrower project-intent-to-verified-client-state reconciliation claim,
not a claim that every adjacent product only installs binaries or that IDE sync never
handles MCP configuration.

Primary references:

- [Smithery documentation](https://smithery.ai/docs)
- [MCP-Get getting started](https://mcp-get.com/getting-started)
- [VS Code MCP server configuration](https://code.visualstudio.com/docs/agent-customization/mcp-servers)

## Explicit user decisions still required

| Question ID | Decision | Why it cannot be inferred |
|---|---|---|
| `Q-SUP-001` | Does the reviewed reusable-source authority transition to frozenSkillz, remain personal-live-first, or migrate per artifact? | The supplement chooses frozenSkillz while current documented authority remains live-first; materialization is required under every option. |
| `Q-SUP-002` | Which tool-policy guarantees and scope are required: filtered server-tool discovery, server-tool call rejection, both, and/or mediation of sampling-driven tool use? | The guarantees solve different problems and change the proxy interface, errors, logging, and conformance burden independently. |
| `Q-SUP-003` | Is backend reuse opt-in after isolation proof, required wherever isolated multi-session behavior is supported and proven, or excluded from v1? | The answer determines whether a session broker/daemon is v1 architecture or a later optimization; universal reuse is not safe for single-session backends. |

Secondary questions remain in the existing evidence pack: fresh-clone readiness,
canonical CLI/manifest names, mixed-file preservation strength, and the eventual
cross-repository automation mechanism.
