# Consumer-Scoped Skill Distribution Implementation Plan

**Goal:** Promote `codex-thread-organizer` only to Codex and add enforceable per-consumer skill allowlists and synchronization.

**Architecture:** Keep shared skills in the common `frozen-skills` package, keep restricted skills in dedicated consumer packages, compose them through `plugins/distribution.json`, require a consumer on every sync, and bind each destination's state record to one consumer.

**Tech Stack:** Python 3 standard library, JSON manifests, Markdown authority docs, `unittest`.

---

### Task 1: Encode the distribution contract in tests

**Files:**
- Modify: `tests/test_sync_frozen_skills.py`
- Modify: `tests/test_codex_thread_organizer.py`

1. Replace the manifest-divergence rejection test with tests proving `distribution.json` consumer lists are valid and selected independently.
2. Add tests requiring an explicit consumer at the CLI boundary.
3. Add tests proving Codex has a private default destination and other consumers require an explicit destination.
4. Add tests proving state records include the consumer and reject cross-consumer reuse.
5. Change organizer packaging assertions to require an active source and Codex-only manifest membership.
6. Run the focused tests and confirm they fail for the intended missing behavior.

### Task 2: Implement consumer-aware validation and synchronization

**Files:**
- Modify: `scripts/sync_frozen_skills.py`
- Modify: `scripts/validate_manifests.py`

1. Replace the manifest tuple with a named consumer-to-manifest mapping.
2. Validate common plugin identity/version while allowing consumer skill lists to differ.
3. Load sources from only the selected consumer manifest.
4. Require a consumer argument and select a safe destination.
5. Upgrade the state schema to record the consumer and reject mismatches.
6. Run focused tests until green.

### Task 3: Promote and qualify the organizer

**Files:**
- Move: `_incubator/frozen-skills/skills/codex-thread-organizer/` to `plugins/codex-thread-organizer/skills/codex-thread-organizer/`
- Modify: `plugins/frozen-skills/.codex-plugin/plugin.json`
- Modify: all four marketplace/plugin version surfaces
- Modify: `docs/skill-review/tracker.md`

1. Move the reviewed skill into the active source tree.
2. Rewrite gated/manual-install wording as active Codex-only distribution wording.
3. Create its valid dedicated Codex plugin, add it only to the Codex distribution/package list, and expose it only in the Codex marketplace.
4. Bump aligned plugin and marketplace versions.
5. Record the promotion and remaining automation qualification boundary in the tracker.

### Task 4: Reconcile authority and user documentation

**Files:**
- Modify: `docs/workflows/skill-authority-and-frozen-sync.md`
- Modify: `AGENTS.md`
- Modify: `README.md`

1. Replace the identical-manifest contract with shared plus dedicated consumer packages and an exact distribution manifest.
2. Document explicit `--consumer` usage, Codex's default, destination isolation, state ownership, and pruning behavior.
3. Update promotion and reporting rules to name targeted consumers.
4. Remove every stale claim that all consumers receive the same skills.

### Task 5: Verify non-leakage and publish

1. Run the organizer packaging tests and complete unit suite.
2. Run manifest validation and JSON parsing.
3. Run isolated Codex, Claude, Cursor, and Gemini smoke checks; prove only Codex receives `codex-thread-organizer`.
4. Run `git diff --check` and audit the diff for `_tmp/` or unrelated changes.
5. Commit and push the completed branch.
6. Open a non-draft PR, self-review the current head, inspect checks and all review threads, address valid feedback, and merge only when the head is clean.
