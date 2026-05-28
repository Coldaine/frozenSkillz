---
name: plugin-authoring-guide
description: >
  Complete reference for creating Claude Code plugins from scratch. Covers
  directory structure, plugin.json manifest, SKILL.md format, agents, hooks,
  MCP servers, commands, rules, marketplace publishing, and testing.
  Use when building a new plugin, adding skills to an existing plugin, or
  publishing a plugin marketplace.
version: 1.0.0
tags:
  - plugins
  - skills
  - authoring
  - marketplace
  - hooks
  - agents
---

# Claude Code Plugin Authoring Guide

## Plugin Directory Structure

```
my-plugin/
├── .claude-plugin/           # Claude Code manifest directory
│   └── plugin.json           # Manifest (optional — auto-discovery works without it)
├── .codex-plugin/            # Codex CLI manifest directory
│   └── plugin.json
├── .cursor-plugin/           # Cursor manifest directory
│   └── plugin.json
├── gemini-extension.json      # Gemini CLI manifest
├── skills/                   # Agent skills (SKILL.md in subdirectories)
│   └── my-skill/
│       ├── SKILL.md          # Required — instructions + frontmatter
│       ├── references/       # Optional — docs loaded on demand
│       ├── scripts/          # Optional — executable helpers
│       └── assets/           # Optional — templates, data files
├── commands/                 # Slash commands (Markdown files)
├── agents/                   # Subagent definitions (Markdown files)
├── hooks/
│   └── hooks.json            # Hook configurations
├── .mcp.json                 # MCP server definitions
├── .lsp.json                 # LSP server configurations
├── scripts/                  # Hook and utility scripts
├── LICENSE
└── README.md
```

**Critical**: Only `plugin.json` goes inside `.claude-plugin/`. All component directories (`skills/`, `agents/`, `hooks/`, `commands/`) go at the plugin root.

---

## Plugin Manifest (plugin.json)

Located at `.claude-plugin/plugin.json`. Optional — if omitted, Claude Code auto-discovers components and derives the plugin name from the directory name.

### Cross-Platform Manifests
To support multiple agent products, include manifests for each:
- **Codex**: `.codex-plugin/plugin.json`
- **Cursor**: `.cursor-plugin/plugin.json`
- **Gemini**: `gemini-extension.json`

Manifests follow a universal structure:

```json
{
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin provides",
  "author": {
    "name": "Author Name",
    "url": "https://github.com/author"
  },
  "repository": "https://github.com/author/plugin",
  "license": "MIT",
  "keywords": ["keyword1", "keyword2"],
  "commands": ["./commands/"],
  "agents": "./agents/",
  "skills": "./skills/",
  "hooks": "./hooks/hooks.json",
  "mcpServers": "./.mcp.json",
  "lspServers": "./.lsp.json"
}
```

Only `name` is required if you include a manifest. All component paths are optional and supplement (not replace) default directories. Paths must be relative, starting with `./`.

Use `${CLAUDE_PLUGIN_ROOT}` in hooks, MCP configs, and scripts for absolute path resolution.

---

## SKILL.md Format

Skills follow the [Agent Skills](https://agentskills.io) open standard. Each skill is a directory containing a `SKILL.md` with YAML frontmatter + Markdown body.

### Frontmatter Fields

```yaml
---
name: my-skill                      # Required. Kebab-case, max 64 chars. Becomes /slash-command name.
description: >                      # Required. Max 1024 chars. Claude uses this for auto-invocation.
  What this skill does and when
  to use it. Include trigger keywords.
version: 1.0.0                     # Optional. Semver.
tags: [tag1, tag2]                  # Optional. Discovery keywords.
---
```

**Claude Code extended fields** (beyond the open standard):

| Field | Purpose | Example |
|-------|---------|---------|
| `argument-hint` | Autocomplete hint | `[issue-number]` |
| `disable-model-invocation` | Only user can invoke via `/name` | `true` |
| `user-invocable` | `false` = hidden from `/` menu, only Claude can invoke | `false` |
| `model` | Model override when active | `sonnet` |
| `context` | Run in forked subagent context | `fork` |
| `agent` | Subagent type when `context: fork` | `Explore` |

### Invocation Controls

| Setting | User Invokes | Claude Invokes | Description in Context |
|---------|-------------|----------------|----------------------|
| (default) | Yes | Yes | Always loaded |
| `disable-model-invocation: true` | Yes | No | NOT loaded |
| `user-invocable: false` | No | Yes | Always loaded |

### Dynamic Context Injection

Run shell commands before skill content is sent to Claude:

```yaml
---
name: pr-summary
description: Summarize a pull request
context: fork
agent: Explore
---

## Context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
```

### String Substitutions

| Variable | Description |
|----------|-------------|
| `$ARGUMENTS` | All arguments passed when invoking |
| `$ARGUMENTS[N]` | Specific argument by 0-based index |
| `$N` | Shorthand for `$ARGUMENTS[N]` |
| `${CLAUDE_SESSION_ID}` | Current session ID |

### Progressive Disclosure (Three-Tier Loading)

1. **Metadata** (~100 tokens): `name` + `description` always in context
2. **Instructions** (<5000 tokens target): Full SKILL.md body loads on activation
3. **Resources** (as needed): `scripts/`, `references/`, `assets/` loaded when referenced

Keep SKILL.md under 500 lines. Move detailed reference material to `references/`.

---

## Agents (Subagents)

Markdown files in `agents/` with YAML frontmatter.

```markdown
---
name: code-reviewer
description: Reviews code for quality. Use proactively after code changes.
tools: Read, Grep, Glob, Bash
model: sonnet
maxTurns: 50
---

You are a senior code reviewer. Analyze code and provide
specific, actionable feedback on quality and security.
```

### Agent Fields

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier (lowercase, hyphens) |
| `description` | Yes | When to delegate to this agent |
| `tools` | No | Tool allowlist. Inherits all if omitted |
| `disallowedTools` | No | Tool denylist |
| `model` | No | `sonnet`, `opus`, `haiku`, or `inherit` |
| `permissionMode` | No | `default`, `acceptEdits`, `bypassPermissions`, etc. |
| `maxTurns` | No | Maximum agentic turns |
| `skills` | No | Skills to preload at startup |
| `mcpServers` | No | MCP servers available to this agent |
| `memory` | No | `user`, `project`, or `local` |

---

## Hooks

Located at `hooks/hooks.json` or inline in `plugin.json`.

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format-code.sh"
          }
        ]
      }
    ]
  }
}
```

### Hook Events

| Event | When |
|-------|------|
| `PreToolUse` | Before tool execution |
| `PostToolUse` | After successful tool use |
| `PostToolUseFailure` | After tool failure |
| `UserPromptSubmit` | When user submits a prompt |
| `SessionStart` | At session start |
| `SessionEnd` | At session end |
| `Stop` | When Claude attempts to stop |
| `SubagentStart` / `SubagentStop` | Subagent lifecycle |
| `Notification` | When notifications are sent |
| `PreCompact` | Before context compaction |
| `TaskCompleted` | When a task is marked done |

### Hook Types

- `command` — Execute shell commands/scripts
- `prompt` — Evaluate a prompt with an LLM
- `agent` — Run an agentic verifier with tools

---

## MCP Servers

Located at `.mcp.json` in plugin root.

```json
{
  "mcpServers": {
    "my-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/my-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "DB_PATH": "${CLAUDE_PLUGIN_ROOT}/data"
      }
    }
  }
}
```

Plugin MCP servers start automatically when the plugin is enabled.

---

## Commands (Legacy, Still Works)

Plain Markdown files in `commands/`. A file at `commands/review.md` creates `/review`.

```markdown
---
description: Review code for bugs and security
disable-model-invocation: true
---

Review the code I've selected for:
- Potential bugs
- Security concerns
- Performance issues
```

Skills are preferred over commands for new development (they support bundled resources).

---

## Rules (.claude/rules/)

Not part of plugins, but related. Rules are always-on context, not invokable commands.

- **Project rules**: `.claude/rules/*.md` — auto-loaded
- **User rules**: `~/.claude/rules/*.md` — global, lower priority
- **Path-scoped**: Add `paths: src/api/**/*.ts` in frontmatter

---

## Publishing as a Marketplace

A marketplace is a repository containing multiple plugins. Add `.claude-plugin/marketplace.json` at the repo root:

```json
{
  "name": "my-marketplace",
  "owner": {
    "name": "Author",
    "url": "https://github.com/author"
  },
  "plugins": [
    {
      "name": "my-plugin",
      "source": "./plugins/my-plugin",
      "description": "What it does",
      "version": "1.0.0"
    }
  ]
}
```

### Plugin Source Types

| Type | Format |
|------|--------|
| Relative path | `"source": "./plugins/my-plugin"` |
| GitHub | `"source": {"source": "github", "repo": "owner/repo"}` |
| Git URL | `"source": {"source": "url", "url": "https://..."}` |
| npm | Package reference |
| pip | Package reference |

### Installation Commands

```bash
# Add a marketplace
/plugin marketplace add owner/repo          # GitHub
/plugin marketplace add ./local-path        # Local
/plugin marketplace add https://url.git     # Git URL

# Install a plugin from marketplace
/plugin install my-plugin@marketplace-name
```

### Team Configuration (.claude/settings.json)

```json
{
  "extraKnownMarketplaces": {
    "my-marketplace": {
      "source": {
        "source": "github",
        "repo": "org/claude-plugins"
      }
    }
  },
  "enabledPlugins": {
    "my-plugin@my-marketplace": true
  }
}
```

---

## Testing and Development

```bash
# Load plugin without installing (development mode)
claude --plugin-dir ./my-plugin

# Debug plugin loading
claude --debug

# Validate plugin structure
claude plugin validate .

# Install/uninstall
claude plugin install <plugin>@<marketplace>
claude plugin uninstall <plugin>
claude plugin enable <plugin>
claude plugin disable <plugin>
claude plugin update <plugin>
```

After installing, restart Claude Code to load the plugin.

### Skill Location Priority (Highest Wins)

| Level | Path |
|-------|------|
| Enterprise | Managed settings |
| Personal | `~/.claude/skills/<name>/SKILL.md` |
| Project | `.claude/skills/<name>/SKILL.md` |
| Plugin | `<plugin>/skills/<name>/SKILL.md` (namespaced as `plugin:skill`) |

---

## Writing Good Descriptions

The `description` field is the primary trigger for auto-invocation. It must clearly state **what** the skill does and **when** to use it.

**Good**: "Complete reference for creating Claude Code plugins from scratch. Covers directory structure, plugin.json manifest, SKILL.md format, agents, hooks, MCP servers, commands, rules, marketplace publishing, and testing. Use when building a new plugin or publishing a marketplace."

**Bad**: "Helps with plugins."

---

## Checklist: New Plugin

1. Create directory with name matching your plugin
2. Add `.claude-plugin/plugin.json` (or rely on auto-discovery)
3. Add skills to `skills/<name>/SKILL.md` with proper frontmatter
4. Add agents, hooks, commands, MCP servers as needed
5. Test with `claude --plugin-dir ./my-plugin`
6. Validate with `claude plugin validate .`
7. If publishing: add `marketplace.json`, push to GitHub
8. Install: `/plugin marketplace add owner/repo` then `/plugin install name@marketplace`
