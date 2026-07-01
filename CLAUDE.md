# frozenSkillz — Cross-Platform Agent Plugin Marketplace

Universal skills, rules, and tools for cross-project agent workflows. Works across Claude Code, Codex, Cursor, Gemini, and Kilo.

> **Agents:** Read `AGENTS.md` for the full skill intake workflow, quality gate, and evaluation rubric.

## Quickstart

```bash
/plugin marketplace add Coldaine/frozenSkillz
/plugin install frozen-skills@coldaine-skills
```

## Plugins

| Plugin | Status | Purpose |
|---|---|---|
| `frozen-skills` | active | Shared skills (doppler, stacked-pr, etc.) |
| `frozen-rules` | active | Rule templates (Ansible, docs, submodules) |
| `skill-injector` | experimental | LLM skill-suggestion hook + subagent prompt quality gate |
| `skill-manager` | gated | Skill inventory, audit, and reconciliation |

## Install

```bash
/plugin install frozen-skills@coldaine-skills
/plugin install frozen-rules@coldaine-skills
/plugin install skill-injector@coldaine-skills
/plugin install skill-manager@coldaine-skills
```

## Key Skills

- `doppler` — Doppler CLI and secret-injection workflows (security-first, cross-platform)
- `stacked-pr-workflow` — Convert messy branches into reviewable stacked PRs
- `agent-config-megaref` — Reference for configuring agent clients
- `mcp-deployment-guide` — MCP server deployment across AI tools
- `plugin-authoring-guide` — Plugin, skill, agent, hook, and marketplace authoring
- `gh-common-workflows` — GitHub CLI workflows for PR triage, review, merge
- `session-skill-inferencer` — Analyze coding sessions, generate skills/rules/hooks

> Most non-Doppler skills are **gated** in `_incubator/` pending review. See `AGENTS.md` for the promotion bar.

## Repository Layout

```
frozenSkillz/
├── plugins/                  Active marketplace content
│   ├── frozen-skills/skills/ Active skills
│   ├── frozen-rules/         Rule templates
│   └── skill-injector/       Experimental hooks
├── _incubator/               Gated content (not in marketplace)
├── docs/                     Workflow docs, rubric, tracker
├── .claude-plugin/           Claude Code marketplace catalog
├── .codex-plugin/            Codex marketplace catalog
├── .cursor-plugin/           Cursor marketplace catalog
├── gemini-marketplace.json   Gemini marketplace catalog
├── mcp/                      MCP server config templates
├── CLAUDE.md (this file)
└── AGENTS.md                 Agent-facing workflow docs
```

## Validation

```powershell
Get-Content .claude-plugin/marketplace.json -Raw | ConvertFrom-Json | Out-Null
Get-Content plugins/frozen-skills/.claude-plugin/plugin.json -Raw | ConvertFrom-Json | Out-Null
python scripts/validate_manifests.py
```

## Contributing

1. Add skills to `plugins/frozen-skills/skills/<name>/SKILL.md`
2. Add rules to `plugins/frozen-rules/rules/<name>.md`
3. Update manifests and versions when adding/changing skills
4. Run `python scripts/validate_manifests.py` before publishing

## License

MIT
