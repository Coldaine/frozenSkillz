# Frozen authority and deterministic chat recovery

## Decision

`frozenSkillz` is the upstream authoring and release repository for every skill it publishes. Installed copies in `.agents`, Claude, Codex, Cursor, Gemini, and other client roots are downstream deployment outputs. They are never sources to reverse-sync into this repository.

The `chat-history` skill is promoted into the active `frozen-skills` plugin with deterministic, read-only tooling for incident-time conversation inventory. The tooling distinguishes a user conversation from its child workers and evidence streams, so a single workflow with many children is reported once while retaining the child evidence.

## Why

The previous documentation said to author in the live `.agents` copy and later mirror it into this repository. That made the reviewed repository downstream of an unreviewed runtime copy, guaranteed drift, and made release provenance impossible to establish. It also encouraged transcript recovery by broad text search, which over-counted child workers and missed known storage surfaces.

The corrected flow is outward-only:

1. Author, review, test, and version the skill in `frozenSkillz`.
2. Publish or deploy that exact tree to supported client roots.
3. Verify installed copies against the repository source.
4. Treat local divergence as drift to repair, never as authority to import automatically.

## Tooling boundary

`llm-archiver` remains the fleet-wide knowledge source for tool locations, parser roles, and stitching concepts. `frozenSkillz` owns the released skill and carries a provenance-pinned registry snapshot, so incident recovery does not depend on a second repository being present or runnable.

The deterministic inventory projects only conversation transcripts as user-facing conversations. Subagent transcripts attach to their parent; indexes, event logs, wire records, state databases, and UI events remain evidence or discovery surfaces and do not inflate the conversation count.

## Safety

- Recovery commands are read-only.
- Deployment refuses reverse direction and unexpected destination drift unless explicitly forced.
- The registry snapshot records its upstream source and commit.
- Tests cover workflow-child collapse, terminal-state inference, and event/index de-duplication.
