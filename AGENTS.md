# Agent Router

This repository is a marketplace and intake boundary for reusable agent skills, rules, hooks, and plugin metadata. Keep active marketplace content small, reviewed, and installable.

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
| Compare live skill roots to frozenSkillz | `docs/workflows/skill-authority-and-frozen-sync.md`, then `docs/skill-review/tracker.md` if promotion is needed |
| Update marketplace catalog metadata | `.claude-plugin/marketplace.json`, `.codex-plugin/marketplace.json`, `.cursor-plugin/marketplace.json`, `gemini-marketplace.json` |

## Operating Contract

- Keep `AGENTS.md` a router. Put long procedures in `docs/workflows/`.
- Do not import external repositories directly into `plugins/`.
- Keep scout `source/` directories read-only.
- Keep active `SKILL.md` files lean and route heavy detail to `references/` or `templates/`.
- Treat `C:\Users\pmacl\.agents\skills` as the live personal skill source and this repo as the reviewed frozen publication boundary.
- Update all four plugin manifests when adding or removing active frozen-skills skills.
- Bump aligned plugin and marketplace versions when public plugin metadata changes.
- Validate changed JSON and every manifest `skills[].path` before publishing.

## Commands

```powershell
git diff --check
python scripts/validate_manifests.py
```

For JSON manifests touched in a change, parse them with PowerShell `ConvertFrom-Json` and verify referenced skill paths exist.
