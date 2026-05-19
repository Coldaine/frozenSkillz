# Agents Skills Corpus Needing Relevance Analysis

Archived on 2026-05-19 from `C:\Users\pmacl\.agents\skills`.

This is the full shared `.agents/skills` corpus as it existed during the Claude/Codex/Gemini skill-surface cleanup. It is intentionally stored outside the active `plugins/frozen-skills/skills/` publication path.

## Purpose

This archive is the huge corpus that needs to be analyzed before any of it is treated as active, current, or worth republishing. Do not assume these skills are relevant just because they existed in the shared `.agents` directory.

Each skill needs a rework decision:

- keep and publish through the normal frozen skills flow;
- rewrite for a specific client runtime;
- merge into another skill;
- delete because it is stale, duplicated, client-specific, or tool-dependent.

## Archived Skills

- `chat-history`
- `claude-md-enhancer`
- `gemini-extractor`
- `google-stitch-ui-designer`
- `gws-gmail`
- `gws-gmail-read`
- `gws-gmail-send`
- `gws-shared`
- `insight-extractor`
- `omc-learned`
- `omc-reference`
- `pr-review-dashboard`
- `pr-triage`
- `pr-visual-summary`
- `retrospective`
- `review-claudemd`
- `review-repo-docs`
- `skill-finder`

## Rework Checks

Before reactivation, inspect:

- whether the skill assumes Claude, Codex, Gemini, Opencode, or another client;
- whether referenced tools actually exist in the target runtime;
- whether the skill duplicates plugin-provided skills;
- whether the instructions are still accurate;
- whether the skill belongs in a global shared root, a client-local root, or a project-local root.
