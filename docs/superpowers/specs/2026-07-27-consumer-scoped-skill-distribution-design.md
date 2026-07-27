# Consumer-Scoped Skill Distribution Design

## Goal

Promote `codex-thread-organizer` as an active Codex skill without making it installable for Claude, Cursor, or Gemini, and make that boundary an enforced reusable distribution capability for future skills.

## Chosen Architecture

Use each existing consumer plugin manifest as that consumer's exact skill allowlist:

- Claude: `plugins/frozen-skills/.claude-plugin/plugin.json`
- Codex: `plugins/frozen-skills/.codex-plugin/plugin.json`
- Cursor: `plugins/frozen-skills/.cursor-plugin/plugin.json`
- Gemini: `plugins/frozen-skills/gemini-extension.json`

The manifests continue to share the `frozen-skills` plugin identity and release version, but their ordered `skills` lists may differ intentionally. A skill is active for a consumer only when its reviewed source exists under `plugins/frozen-skills/skills/<name>/` and that consumer's manifest lists it.

This uses the manifests that already control packaging instead of adding a second consumer-target database. It also avoids duplicating skill source trees per consumer. Raw repository presence is not installation or eligibility; manifest membership is.

## Synchronizer Contract

`sync_frozen_skills.py` must require `--consumer {claude,codex,cursor,gemini}`. It loads and installs only the selected consumer manifest.

The old implicit shared-root behavior is intentionally removed. `~/.agents/skills` is a cross-client discovery surface and therefore cannot safely be the default for a consumer-restricted distribution.

Codex receives a verified default destination of `~/.codex/skills`. Other consumers require `--destination` until their consumer-private roots are explicitly qualified and documented. An operator may pass any disjoint destination, including a test directory, but must still identify the consumer whose manifest is authoritative.

The management record is upgraded and includes the consumer. A destination already managed for one consumer is rejected when selected for another consumer. This prevents a later sync from silently adopting, pruning, or overwriting another consumer's managed distribution.

## Promotion

Move `codex-thread-organizer` from `_incubator/frozen-skills/skills/` to `plugins/frozen-skills/skills/`. Add it only to the Codex plugin manifest. Keep it absent from the Claude, Cursor, and Gemini manifests.

The skill remains Codex-only in its triggering and operating instructions. Promotion does not create a periodic automation; it only makes the skill eligible for an explicit Codex-targeted install/sync. Periodic operation remains a separate Codex automation that invokes the skill.

## Validation Invariants

Validation must prove:

1. all consumer manifests retain the same plugin name and version;
2. every manifest has a valid, duplicate-free skill list;
3. every listed path is relative, stays inside the plugin root, uses the same-name directory, and contains `SKILL.md`;
4. differing consumer allowlists are valid;
5. `codex-thread-organizer` is listed only for Codex;
6. a Codex sync installs the organizer while Claude, Cursor, and Gemini sync plans do not;
7. sync state is bound to one consumer and rejects cross-consumer reuse;
8. the old consumer-less CLI is rejected.

## Alternatives Rejected

### Add a central per-skill `consumers` registry

This would make targeting visible in one place, but it would duplicate the install authority already expressed by four manifests and create reconciliation risk unless all manifests were generated. Manifest generation is unnecessary for the current scale.

### Duplicate the plugin tree per consumer

This would physically isolate packages, but it would duplicate shared skills and references, multiplying maintenance and drift. The consumer manifests already provide the needed eligibility boundary.

## Documentation Authority

Update the authority stack in order:

1. the skill review tracker records the active Codex-only decision and qualification evidence;
2. the synchronization workflow defines consumer allowlists, explicit consumer selection, and state isolation;
3. `AGENTS.md` routes manifest changes to the relevant consumer manifests rather than requiring identical membership;
4. the README explains consumer-scoped installation and the Codex-only organizer.

No document may describe the four skill lists as identical after this change.
