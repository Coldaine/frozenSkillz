# frozenSkillz — Claude Code Plugin Marketplace

Universal skills, rules, and tools for cross-project agent workflows, distributed as a Claude Code plugin marketplace.

## Plugins

| Plugin | Category | Status | Description |
|--------|----------|--------|-------------|
| **frozen-skills** | reference | ✅ Active | Universal cross-project skills (agent config reference, MCP deployment guide, plugin authoring guide) |
| **frozen-rules** | standards | ✅ Active | Universal rule templates (Ansible, documentation, submodules) with setup skill |
| **skill-classifier** | development | 🚧 Experimental | Gemini-powered skill discovery hook — classifies user prompts and suggests relevant skills |

## Installation

```bash
# Add the marketplace
/plugin marketplace add Coldaine/frozenSkillz

# Install individual plugins
/plugin install frozen-skills@coldaine-skills
/plugin install frozen-rules@coldaine-skills
/plugin install skill-classifier@coldaine-skills  # Experimental
```

## Skills Included

### frozen-skills
- `agent-config-megaref` — Definitive reference for configuring agents across Claude Code, Gemini CLI, VS Code, OpenCode, etc.
- `mcp-deployment-guide` — MCP server deployment guide across all AI tools
- `plugin-authoring-guide` — Complete reference for creating Claude Code plugins, skills, agents, hooks, and marketplaces

### frozen-rules
- `setup-rules` — Install and customize rule templates into `.claude/rules/`
- Rule templates: `ansible-playbooks.md`, `documentation-frontmatter.md`, `submodule-workflow.md`

### skill-classifier (experimental)
- Two-layer skill activation: fast LLM classification (Gemini Flash) + detailed guidance from loaded skills
- Requires `GEMINI_API_KEY` environment variable
- See `plugins/skill-classifier/docs/decisions/` for 6 ADRs documenting architecture

## Design Principles

- **Universal skills** — Work across Claude Code, Gemini CLI, VS Code, and other AI tools
- **Reference, not execution** — Skills explain *how to configure*, not *implement new harnesses*
- **Plugin-first** — All capability packaged as installable plugins, not monolithic repo
- **Versioned and discoverable** — Marketplace enables versioning, selective install, and portability
