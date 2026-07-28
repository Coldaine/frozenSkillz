# Agent Router

This repository is a marketplace and intake boundary for reusable agent skills, rules, hooks, and plugin metadata. Keep active marketplace content small, reviewed, and installable.

## Authority Order

1. `docs/skill-review/tracker.md`: active, gated, scout, and promotion status.
2. `docs/workflows/skill-authority-and-frozen-sync.md`: distribution authority and computer synchronization contract.
3. `docs/workflows/external-skill-intake.md`: required workflow for evaluating external repos.
4. Active skill files under `plugins/`: shared skills under `plugins/frozen-skills/` and restricted skills in dedicated packages.
5. `README.md` and `CLAUDE.md`: human-facing overview and quickstart.

If documents disagree, follow the highest applicable source above and fix the stale downstream doc.

## Task Routes

| Task | Read first |
|---|---|
| Evaluate an external skill/plugin/agent repo | `plugins/frozen-skills/skills/external-skill-intake/SKILL.md`, then `docs/workflows/external-skill-intake.md` |
| Land scout/intake into `_incubator` (files + tracker) | `docs/workflows/external-skill-intake.md` (repo landing), then Completion Contract in `docs/workflows/skill-authority-and-frozen-sync.md`; **commit, push, PR** |
| Check whether a skill is active or gated | `docs/skill-review/tracker.md` |
| Promote a gated skill | `docs/skill-review/tracker.md`, `plugins/distribution.json`, then the shared or dedicated consumer package and relevant marketplace manifests |
| Update installable frozen-skills content | `plugins/distribution.json`, the shared or dedicated package source, and relevant native manifests/catalogs |
| Synchronize active skills to a computer | `docs/workflows/skill-authority-and-frozen-sync.md`, then `scripts/sync_frozen_skills.py` |
| Reconcile a local edit with frozenSkillz | `docs/workflows/skill-authority-and-frozen-sync.md`, then `docs/skill-review/tracker.md` if promotion is needed |
| Rewrite / fix a personal or gated skill | `docs/workflows/skill-authority-and-frozen-sync.md` (Completion Contract + personal/gated sync), then the skill under `_incubator/` or `plugins/`; update tracker; **commit and push** |
| Update marketplace catalog metadata | `.claude-plugin/marketplace.json`, `.codex-plugin/marketplace.json`, `.cursor-plugin/marketplace.json`, `gemini-marketplace.json` |

## Operating Contract

- Keep `AGENTS.md` a router. Put long procedures in `docs/workflows/`.
- Do not import external repositories directly into `plugins/`.
- Keep scout `source/` directories read-only.
- Keep active `SKILL.md` files lean and route heavy detail to `references/` or `templates/`.
- Treat `plugins/frozen-skills/skills` as the shared active package. Restricted skills live in dedicated plugin packages. `plugins/distribution.json` composes their exact consumer allowlists.
- Treat synchronized copies under a consumer-specific destination as managed runtime output; protect local changes as conflicts rather than silently reversing the authority flow.
- Treat `~/.agents/skills` as the authoring source only for personal or gated skills; mirror those into `_incubator/` for durable review.
- **Repo landing done means committed+pushed in this repo** (scout/intake under `_incubator/`, personal/gated mirrors, or `plugins/`). Tracker updates without git are incomplete. “Stay gated” ≠ “skip git.” See Completion Contract in `docs/workflows/skill-authority-and-frozen-sync.md`.
- Put cross-consumer skills in the shared package; put restricted skills only in dedicated packages listed for approved consumers in `plugins/distribution.json` and the matching marketplace catalogs. Keep release versions aligned.
- Bump aligned plugin and marketplace versions when public plugin metadata changes.
- Validate changed JSON, every `distribution.json` skill path, and every native manifest component path before publishing.

## Commands

```powershell
git diff --check
python scripts/validate_manifests.py
python -m unittest discover -s tests -v
```

For JSON manifests touched in a change, parse them with PowerShell `ConvertFrom-Json` and verify referenced distribution/component paths exist.
