# frozenSkillz — Claude Code Plugin Marketplace

Universal skills, rules, and tools for cross-project agent workflows.

## What This Is

A **Claude Code plugin marketplace** containing four plugins:

1. **frozen-skills** — Universal cross-project skills (agent config reference, MCP deployment guide)
2. **frozen-rules** — Universal rule templates (Ansible, documentation, submodules)
3. **skill-classifier** — WIP Gemini-powered skill discovery hook

4. **skill-manager** - Dry-run skill inventory, policy, and reconciliation reports

## Installation

### Add the marketplace:
```bash
/plugin marketplace add Coldaine/frozenSkillz
```

### Install individual plugins:
```bash
/plugin install frozen-skills@coldaine-skills
/plugin install frozen-rules@coldaine-skills
/plugin install skill-classifier@coldaine-skills  # Experimental
/plugin install skill-manager@coldaine-skills     # Dry-run skill state manager
```

## Marketplace Structure

```
frozenSkillz/
├── .claude-plugin/
│   └── marketplace.json       # Marketplace catalog
├── plugins/
│   ├── frozen-skills/         # Universal skills
│   │   ├── .claude-plugin/plugin.json
│   │   └── skills/
│   │       ├── agent-config-megaref/SKILL.md
│   │       ├── mcp-deployment-guide/SKILL.md
│   │       └── plugin-authoring-guide/SKILL.md
│   ├── frozen-rules/          # Universal rules
│   │   ├── .claude-plugin/plugin.json
│   │   ├── rules/             # Raw rule templates
│   │   │   ├── ansible-playbooks.md
│   │   │   ├── documentation-frontmatter.md
│   │   │   └── submodule-workflow.md
│   │   └── skills/
│   │       └── setup-rules/SKILL.md
│   └── skill-classifier/      # WIP discovery hook
│       ├── .claude-plugin/plugin.json
│       ├── hooks/hooks.json
│       ├── scripts/skill_classifier.py
│       ├── test_classifier.py
│       ├── mock_input.json
│       ├── mock_transcript.jsonl
│       └── docs/decisions/    # 6 ADRs
└── CLAUDE.md (this file)
```

## Plugin Descriptions

### frozen-skills (reference)

**Category**: reference  
**Version**: 1.0.0  
**Skills**:
- `agent-config-megaref` — Definitive reference for configuring agents across Claude Code, Gemini CLI, VS Code, OpenCode, etc.
- `mcp-deployment-guide` — MCP server deployment guide across all AI tools
- `plugin-authoring-guide` — Complete reference for creating Claude Code plugins, skills, agents, hooks, and marketplaces
- `gh-common-workflows` — Opinionated GitHub CLI workflows for PR triage, review, merge, and close decisions
- `graphite-stacked-pr-workflow` — Graphite workflow for converging messy or clean work into reviewable stacked PRs

**Use when**: Answering "how do I configure X?", "where do I deploy MCP servers?", "how do I write a plugin?", or "how do I get from a messy branch/PR state to a clean stacked PR workflow?"

### frozen-rules (standards)

**Category**: standards  
**Version**: 1.0.0  
**Skills**:
- `setup-rules` — Helps install and customize rule templates

**Rule Templates**:
- `ansible-playbooks.md` — Ansible playbook header format, secrets, manual execution
- `documentation-frontmatter.md` — Documentation frontmatter requirements
- `submodule-workflow.md` — Git submodule workflow rules

**Use when**: Establishing project standards for Ansible, docs, or submodules

**Note**: Rules must be copied to `.claude/rules/` in each project. The `setup-rules` skill guides you through this.

### skill-classifier (development, experimental)

**Category**: development  
**Version**: 0.1.0  
**Status**: WIP  

**What it does**: UserPromptSubmit hook that calls Gemini Flash to classify user prompts and suggest relevant skills.

**Architecture**: Two-layer skill activation:
1. **Layer 1 (hook)**: Fast LLM classification (Gemini Flash) — "what category of task?"
2. **Layer 2 (skills)**: Detailed guidance from loaded skills — "here's how to do it"

**Requirements**:
- Python >=3.9
- `google-generativeai` package
- `GEMINI_API_KEY` environment variable

**ADRs**:
- 001: LLM-only classification (no keyword matching)
- 002: Gemini Flash CLI as MVP
- 003: Hook output format (JSON with suggestions)
- 004: Silent passthrough on failure
- 005: Two-layer skill activation
- 006: Transcript parsing strategy

### skill-manager (development)

**Category**: development
**Version**: 0.2.0
**Status**: Dry-run only

**What it does**: Inventories live and archived skill roots across Claude, Codex, Gemini, OpenCode, shared `.agents`, plugin caches, and this repository, then compares that inventory to `skill-policy.json`.

**Commands**:
- `scripts/skills-state.ps1 inventory` - print discovered skill/config state
- `scripts/skills-state.ps1 plan` - print proposed actions without mutating live folders
- `scripts/skills-state.ps1 report` - write `skill-state.lock.json` and `reports/latest-skill-state.md`

**Use when**: Deciding which skills should remain enabled, which duplicated skill copies need review, or whether stale config references exist before touching any live client folders.

## Development

This repo uses regular Git branches. Check `git status` for the current branch before committing.

### Design Principles

1. **Universal skills** — Work across Claude Code, Gemini CLI, VS Code, and other AI tools
2. **Reference, not execution** — Skills explain *how to configure*, not *implement new harnesses*
3. **Database of decisions** — ADRs document architecture choices for the classifier
4. **Plugin-first** — All capability packaged as installable plugins, not monolithic repo

5. **Dry-run before mutation** - Skill portfolio changes are planned and reported before any live client root is edited

### Why a Marketplace?

Skills and rules need to:
- **Be versioned** — Track what's deployed across projects
- **Be discoverable** — Users install what they need, not everything
- **Be portable** — Work in any Claude Code project
- **Be maintainable** — Update once, deploy everywhere

A marketplace solves all of these.

## Usage Examples

### Installing frozen-skills

```bash
/plugin marketplace add Coldaine/frozenSkillz
/plugin install frozen-skills@coldaine-skills
```

Then invoke skills:
```
/skill agent-config-megaref
"How do I configure MCP servers in VS Code?"
```

### Installing frozen-rules

```bash
/plugin install frozen-rules@coldaine-skills
/skill setup-rules
"Install the ansible-playbooks rule"
```

The agent will guide you through copying templates to `.claude/rules/`.

### Testing skill-classifier (experimental)

```bash
/plugin install skill-classifier@coldaine-skills
```

Requires `GEMINI_API_KEY` set. Hook runs on every prompt, classifies it, and suggests skills.

Test it:
```bash
cd plugins/skill-classifier
python test_classifier.py
```

### Testing skill-manager (dry-run)

```bash
cd plugins/skill-manager
pwsh ./scripts/skills-state.ps1 inventory
pwsh ./scripts/skills-state.ps1 plan
pwsh ./scripts/skills-state.ps1 report
```

`report` writes `skill-state.lock.json` and `reports/latest-skill-state.md` at the repo root. The script reports proposed actions only; live client folders are not modified.

## Contributing

1. Skills go in `plugins/frozen-skills/skills/<name>/SKILL.md`
2. Rules go in `plugins/frozen-rules/rules/<name>.md`
3. Classifier improvements go in `plugins/skill-classifier/`
4. Skill portfolio policy changes go in `skill-policy.json`
5. Update plugin versions and marketplace.json when adding/changing plugins

## License

MIT
