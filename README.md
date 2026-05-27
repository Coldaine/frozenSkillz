# frozenSkillz

Cross-platform agent skills, rules, and plugin metadata for reusable agent workflows.

This repository is maintained as a plugin marketplace and source/registry boundary for shared skills. It is not intended to be a junk drawer for every local client cache or experimental skill copy.

## Plugins

| Plugin | Category | Status | Purpose |
| --- | --- | --- | --- |
| `frozen-skills` | reference | active | Shared skills for agent configuration, MCP deployment, plugin authoring, GitHub PR work, stacked PR workflows, session-skill inference, and Doppler secret handling. |
| `frozen-rules` | standards | active | Rule templates for Ansible, documentation frontmatter, and submodule workflows, plus the `setup-rules` helper skill. |
| `skill-classifier` | development | experimental | UserPromptSubmit hook and skill docs for LLM-assisted skill suggestions. |
| `skill-manager` | development | dry-run | Skill inventory, policy, and reconciliation reporting across local agent client roots. |

## Install

Claude Code marketplace:

```bash
/plugin marketplace add Coldaine/frozenSkillz
/plugin install frozen-skills@coldaine-skills
/plugin install frozen-rules@coldaine-skills
/plugin install skill-classifier@coldaine-skills
/plugin install skill-manager@coldaine-skills
```

Cross-platform manifests are also present for Codex, Cursor, and Gemini-compatible consumers where supported by those clients.

## Key Skills

`frozen-skills` currently registers:

- `agent-config-megaref`: reference for configuring agent clients and harnesses
- `mcp-deployment-guide`: MCP server deployment guidance across AI tools
- `plugin-authoring-guide`: plugin, skill, agent, hook, and marketplace authoring guidance
- `gh-common-workflows`: GitHub CLI workflows for PR triage, review, merge, and close decisions
- `session-skill-inferencer`: analyze coding sessions and generate reusable skills, rules, or hooks
- `stacked-pr-workflow`: convert messy branch or PR state into reviewable stacked PRs using `git`, `gh`, and optional Graphite compatibility
- `doppler`: Doppler CLI and secret-injection workflow guidance that avoids exposing secret values

## Repository Layout

```text
.claude-plugin/                  Marketplace catalog
.codex-plugin/                   Codex-facing marketplace metadata
.cursor-plugin/                  Cursor-facing marketplace metadata
gemini-marketplace.json          Gemini-facing marketplace metadata
plugins/
  frozen-skills/                 Shared reusable skills
  frozen-rules/                  Rule templates and setup helper
  skill-classifier/              Experimental skill-classifier hook
  skill-manager/                 Dry-run skill state manager
docs/
  stacked-pr-workflow/           Design notes and helper-script docs
  experimentation/               Experimental or exploratory notes, if present
removed-needs-rework/            Quarantined material that is not active publication content
```

## Validation

This repo does not use a single package manager. Validate the touched surface directly:

```powershell
# JSON manifests
Get-Content .claude-plugin/marketplace.json -Raw | ConvertFrom-Json | Out-Null
Get-Content plugins/frozen-skills/.claude-plugin/plugin.json -Raw | ConvertFrom-Json | Out-Null

# Skill-manager dry-run checks
powershell -NoProfile -File plugins\skill-manager\scripts\skills-state.ps1 inventory
powershell -NoProfile -File plugins\skill-manager\scripts\skills-state.ps1 plan
powershell -NoProfile -File plugins\skill-manager\scripts\skills-audit.ps1
```

For skill additions, verify every manifest `skills[].path` exists under the plugin directory and run `git diff --check` before publishing or merging.

## Contribution Rules

- Add shared skills under `plugins/frozen-skills/skills/<name>/SKILL.md`.
- Add rule templates under `plugins/frozen-rules/rules/<name>.md`.
- Keep plugin manifests and marketplace versions aligned when adding public skills.
- Keep archived or questionable imports under `removed-needs-rework/` until reviewed.
- Do not commit secret values, client runtime caches, or local installed-skill copies.
