# Consumer-Scoped Skill Distribution Design

## Goal

Promote `codex-thread-organizer` as an active Codex skill without making it installable for Claude, Cursor, or Gemini, and make that boundary an enforced reusable distribution capability for future skills.

## Chosen Architecture

Use physically separate packages plus one repository distribution manifest:

- `plugins/frozen-skills/skills/<name>/` contains shared active skills discoverable by every supported consumer.
- Dedicated packages such as `plugins/codex-thread-organizer/skills/<name>/` contain restricted active skills and appear only in approved consumer marketplaces.
- `plugins/distribution.json` composes the shared package with declared consumer packages and is the exact allowlist used by the repository synchronizer.

This physical split is required because native plugin discovery is not uniformly controlled by a per-skill manifest array. Claude Code automatically discovers every `SKILL.md` below a plugin's default `skills/` directory and offers no custom skill-path exclusion. The current Codex ingestion validator requires a plugin's `skills` path to resolve to that package's default `skills/` directory. Therefore a restricted skill needs its own valid package, and only its approved consumer marketplace may expose that package.

The native Claude, Codex, Cursor, and Gemini manifests continue to share the common `frozen-skills` plugin identity and release version. Dedicated consumer package versions are aligned with the distribution release. Validator checks reconcile physical package contents, consumer marketplace membership, and `distribution.json`.

## Synchronizer Contract

`sync_frozen_skills.py` must require `--consumer {claude,codex,cursor,gemini}`. It loads the shared entries plus only the selected consumer entries from `distribution.json`.

The old implicit shared-root behavior is intentionally removed. `~/.agents/skills` is a cross-client discovery surface and therefore cannot safely be the default for a consumer-restricted distribution.

Codex receives a verified default destination of `~/.codex/skills`. Other consumers require `--destination` until their consumer-private roots are explicitly qualified and documented. An operator may pass any disjoint destination, including a test directory, but must still identify the consumer whose manifest is authoritative.

The management record is upgraded and includes the consumer. A destination already managed for one consumer is rejected when selected for another consumer. This prevents a later sync from silently adopting, pruning, or overwriting another consumer's managed distribution.

## Promotion

Move `codex-thread-organizer` from `_incubator/frozen-skills/skills/` to `plugins/codex-thread-organizer/skills/codex-thread-organizer/`. Give that package a valid `.codex-plugin/plugin.json`, add it only to the Codex section/package list in `plugins/distribution.json`, and expose its package only in the Codex marketplace catalog. Keep it absent from the shared package and other consumer catalogs.

The skill remains Codex-only in its triggering and operating instructions. Promotion does not create a periodic automation; it only makes the skill eligible for an explicit Codex-targeted install/sync. Periodic operation remains a separate Codex automation that invokes the skill.

## Validation Invariants

Validation must prove:

1. the common native manifests, dedicated package manifests, marketplaces, and `distribution.json` retain aligned versions and identities;
2. the shared and per-consumer distribution lists are valid and duplicate-free after composition;
3. every distribution path is relative, stays inside the plugin root, uses the same-name directory, and contains `SKILL.md`;
4. consumer allowlists may differ intentionally;
5. `codex-thread-organizer` exists only in its dedicated Codex package and Codex distribution/catalog;
6. a Codex sync installs the organizer while Claude, Cursor, and Gemini sync plans do not;
7. sync state is bound to one consumer and rejects cross-consumer reuse;
8. the old consumer-less CLI is rejected.

## Alternatives Rejected

### Treat native per-client manifests as exact per-skill allowlists

Rejected after documentation verification. Claude Code auto-discovers every skill below the default `skills/` directory and does not support a manifest exclusion list for skills. Omitting a skill entry while leaving its source in that directory would still expose it to Claude.

### Duplicate the complete plugin tree per consumer

This would physically isolate packages, but it would duplicate shared skills and references, multiplying maintenance and drift. The consumer manifests already provide the needed eligibility boundary.

## Documentation Authority

Update the authority stack in order:

1. the skill review tracker records the active Codex-only decision and qualification evidence;
2. the synchronization workflow defines shared/consumer packages, the distribution manifest, explicit consumer selection, and state isolation;
3. `AGENTS.md` routes targeting changes through `plugins/distribution.json`, physical packages, and relevant native marketplace manifests;
4. the README explains consumer-scoped installation and the Codex-only organizer.

No document may describe the four skill lists as identical after this change.
