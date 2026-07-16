# Agent Router

This repository is a marketplace and intake boundary for reusable agent skills, rules, hooks, and plugin metadata. Keep active marketplace content small, reviewed, and installable.

## Source Authority — Read This First

**`frozenSkillz` is upstream.** Author, review, test, version, and release published skills in this repository under `plugins/frozen-skills/skills/`.

Copies under `C:\Users\<user>\.agents\skills`, `.claude\skills`, `.codex\skills`, `.cursor\skills`, `.gemini\skills`, or any other client runtime are **downstream installation outputs**. Do not author there, do not treat runtime divergence as a newer source, and never reverse-sync a runtime copy into this repository automatically. Flow changes outward from this repository; verification flows back as a pass/fail report only.

## Authority Order

1. `docs/skill-review/tracker.md`: active, gated, scout, and promotion status.
2. `docs/workflows/external-skill-intake.md`: required workflow for evaluating external repos.
3. Active skill files under `plugins/frozen-skills/skills/`: installable behavior and references.
4. `README.md` and `CLAUDE.md`: human-facing overview and quickstart.

If documents disagree, follow the highest applicable source above and fix the stale downstream doc.

## Task Routes

| Task | Read first |
|---|---|
| Evaluate an external skill/plugin/agent repo | `plugins/frozen-skills/skills/external-skill-intake/SKILL.md`, then `docs/workflows/external-skill-intake.md` |
| Check whether a skill is active or gated | `docs/skill-review/tracker.md` |
| Promote a gated skill | `docs/skill-review/tracker.md` and the relevant plugin manifests |
| Update installable frozen-skills content | `plugins/frozen-skills/.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json`, `gemini-extension.json` |
| Deploy or compare installed skill roots | `docs/workflows/skill-authority-and-frozen-sync.md`; always compare from repo source to runtime destination |
| Update marketplace catalog metadata | `.claude-plugin/marketplace.json`, `.codex-plugin/marketplace.json`, `.cursor-plugin/marketplace.json`, `gemini-marketplace.json` |

## Operating Contract

- Keep `AGENTS.md` a router. Put long procedures in `docs/workflows/`.
- Do not import external repositories directly into `plugins/`.
- Keep scout `source/` directories read-only.
- Keep active `SKILL.md` files lean and route heavy detail to `references/` or `templates/`.
- Treat this repository as the only authoring source for published frozen skills; runtime roots are deployment destinations.
- Never copy an installed skill back into `plugins/frozen-skills/skills/` automatically. Recreate reviewed changes in this repository with provenance and tests.
- Update all four plugin manifests when adding or removing active frozen-skills skills.
- Bump aligned plugin and marketplace versions when public plugin metadata changes.
- Validate changed JSON and every manifest `skills[].path` before publishing.

## Commands

```powershell
git diff --check
python scripts/validate_manifests.py
```

For JSON manifests touched in a change, parse them with PowerShell `ConvertFrom-Json` and verify referenced skill paths exist.
