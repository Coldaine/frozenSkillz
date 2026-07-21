# Plan to Finish the Platform Plan

> **Status:** working process contract, not an approved platform design.

## Objective

Produce a decision-complete, evidence-backed platform design that preserves every
material requirement and correction from the supplied discussion, reconciles them
with the real frozenSkillz lifecycle, and can be converted into an implementation
plan without reopening hidden architectural questions.

## Work packages

| ID | Work package | Output | Exit condition | Status |
|---|---|---|---|---|
| PF-01 | Preserve and fingerprint the source | Source metadata and source ledger | All 1,132 lines covered; damaged/missing speaker context disclosed | Complete |
| PF-02 | Run independent reasoning passes | Decision, architecture, and conformance audits | Three full-file passes independently completed | Complete |
| PF-03 | Reconcile with current repository truth | Authority/lifecycle document and corrected decision register | Current documented lifecycle separated from proposed replacement | In progress |
| PF-04 | Close authority and product choices | Explicit decision records | Each `open-decision` has an owner, options, recommendation, and answer | Not started |
| PF-05 | Specify normative contracts | Architecture, lifecycle/state machines, schemas, CLI, security, and adapter contracts | No contradictory names, states, or ownership semantics remain | Not started |
| PF-06 | Build the traceability and conformance model | Requirements, conformance, failure-injection, and evidence matrices | Every `MUST` has an acceptance ID and expected evidence | In progress |
| PF-07 | Verify time-sensitive and implementation claims | Verification ledger with current evidence | Supported claims verified; unsupported claims removed or bounded | In progress |
| PF-08 | Adversarial design review | Cross-document audit and red-team findings | No unclassified contradiction, orphan requirement, or untestable criterion | In progress |
| PF-09 | User design review | Section-by-section approval record | Authority, distribution, desired state, execution, observation, security, and rollout approved | Not started |
| PF-10 | Write the implementation plan | Ordered implementation tasks with gates and rollback | Plan implements the approved design through pre-pilot completion | Blocked on PF-09 |

## Required reasoning passes

The design receives multiple passes for different failure modes. A single summary
pass is not sufficient.

1. **Extraction pass:** distinguish direct user directives from assistant proposals,
   source damage, inference, and claims of completion.
2. **Chronology pass:** mark later corrections and ensure superseded ideas do not
   reappear under new names.
3. **Current-state pass:** compare proposals with the tracker, intake workflow,
   active plugin manifests, live personal root, and real install/discovery surfaces.
4. **Lifecycle pass:** model intake through removal for active source, global/plugin
   installation, and project vendoring separately.
5. **Interface pass:** ensure filenames, command names, schemas, ownership, versions,
   and compatibility behavior agree across documents.
6. **Security/failure pass:** challenge supply chain, secrets, path safety, trust,
   concurrency, atomicity, rollback, stale state, and partial failure.
7. **Traceability pass:** map every retained requirement to design text, an
   implementation owner, an acceptance case, and evidence output.
8. **Approval pass:** present the design in bounded sections and record explicit user
   approval or correction before implementation planning.

## First decision to close

The source and current repository documentation conflict on authority direction. Do
not answer this as "frozenSkillz or `.agents`?" Installation location does not decide
source authority. Confirm or correct each lifecycle row:

| Lifecycle row | Recommended candidate | Decision status |
|---|---|---|
| Candidate origin | May be personal, project, or external, entering the appropriate frozenSkillz intake lane | Candidate |
| Review/gate status | Tracker and frozenSkillz review workflows | Current-documented |
| Ordinary editing before promotion | Original personal/project source or read-only external evidence plus frozen adaptation | Candidate |
| Active reviewed reusable source | `plugins/frozen-skills/skills/<name>/` after promotion | **Open authority transition** |
| Personal global desired selection | Explicit machine/user selection derived from reviewed content | Open |
| Installed personal/client copy | Actual verified discovery roots or plugin installation with provenance | Direct-user requirement; mechanics open |
| Project vendor | Project lock and committed materialized copy pinned to reviewed upstream | Candidate |
| Project fork/local skill | Project Git | Candidate |
| Client cache/compatibility mirror | Derived execution surface | Candidate |

A phased/per-artifact migration may preserve live-first authority for some skills while
others use frozen-first authority, but each row needs a recorded current state and
target steady state. Hybrid state cannot remain an undocumented default.

For every chosen row, separately define:

- candidate and experimental origins;
- active reviewed source;
- marketplace/plugin installation;
- personal machine-global installation;
- project vendoring/forking/local ownership;
- client-specific discovery mirrors and caches;
- update direction, provenance, drift, rollback, deprecation, and removal;
- migration of existing `.agents\skills` and active frozen copies without loss.

## Decision-closing order

After the authority matrix, close one bounded decision at a time in this order:

1. Distribution lanes and supported client matrices.
2. Project manifest and lock names, ownership, and commit policy.
3. Skill ownership modes and provenance representation.
4. Native client-file managed/unmanaged merge contract.
5. MCP catalog, tool allowlists, namespacing, root binding, and machine registry.
6. Public CLI name and command/exit-code contract.
7. Observation schema, privacy, transport, staleness, and optional central sink.
8. Cross-repository consumer discovery and reviewable update authorization.
9. Security, revocation, rollback, and compatibility policy.
10. V1 support boundary and explicit deferrals.

## Stop conditions

Do not begin platform implementation merely because these scratch files exist. Do
not choose pilot repositories or machines as a substitute for contract design. The
next phase begins only after the definition of a decision-complete design in
[README.md](README.md) is met and the approved design is recorded outside this
working directory.
