name: agent-config-megaref
description: Definitive cross-harness reference for configuring agents (rules/instructions, prompts, skills, agents/subagents, hooks, tools/MCP, plugins/extensions, secrets, sandbox, verification). Use to answer "how do I configure X?" with exact file paths, precedence, schemas, and verification steps.
version: 0.2.0
tags:
  - configuration
  - instructions
  - skills
  - agents
  - hooks
  - mcp
  - plugins
  - extensions
  - secrets
  - sandbox
  - observability
---

# Agent Configuration Mega-Reference

## What this skill is (and is not)
**This skill is a *reference operator* skill**: it tells the agent how to locate and explain configuration surfaces for existing agent products (CLI/IDE/agent runtimes).
**It is not** a "build a harness" skill. Do not propose implementing a new harness unless explicitly asked.

## How to use this skill when answering a user
When asked "how do I configure ___":

1. **Identify the host**: (Codex CLI, Claude Code, VS Code/Copilot Agents, Gemini CLI, OpenCode, etc.) + OS + whether it's personal vs team/managed.
2. **Map the request onto a config surface** from the checklist below.
3. Provide **the authoritative location(s)**: exact path(s), precedence order, minimal schema snippet.
4. Provide **verification steps**: how to enumerate loaded config, where logs/caches live.
5. Call out **security/trust gates**: trusted workspace concepts, approvals, secret handling.
6. If any surface is unclear, ask **only the minimum**: host + where they run it + repo root.

---

## Universal configuration surfaces checklist

### A) Instructions / policy / rules (always-on behavior)
- Global instructions (user-wide defaults)
- Repo/workspace instructions (shared project conventions)
- Path-scoped instructions (folder/file-type targeted)
- Org-managed policy (enterprise-enforced rules)
- Conflict resolution (precedence + merge order)

### B) Prompt assets (reusable prompts & command routing)
- Prompt templates / prompt files
- Slash commands (often implemented as prompt files)
- Prompt libraries shipped by extensions/plugins

### C) Skills (portable workflow capsules)
- SKILL.md + optional scripts/assets/references
- Discovery rules, invocation rules, progressive disclosure

### D) Agents / profiles / modes (persona + toolset bundles)
- Custom agent definitions (file-based profiles)
- Model/tool restrictions per profile
- Visibility controls (user-invokable vs internal-only)

### E) Delegation / subagents
- Subagent enablement + gating tools
- Parallelism + context isolation controls

### F) Hooks / lifecycle automation
- Pre/post tool hooks, session start/stop hooks, policy hooks

### G) Tooling inventory
- Built-in vs extension vs MCP-provided tools
- Tool allow/deny rules, trust prompts

### H) Packaging & distribution
- Plugins/extensions, marketplaces/registries
- Repo-shipped capability bundles, team-shared config

### I) Context & filesystem boundaries
- Working directory / project root detection
- Ignore/exclude rules, workspace trust, remote contexts

### J) Secrets & credentials injection
- Env var expansion rules, secret stores, credential helpers

### K) Sandbox & execution environment
- Sandbox on/off + mode, network access, file write boundaries

### L) Approvals & human-in-the-loop gates
- Approval policy, smart approvals, override controls

### M) Model & generation controls
- Model selection, reasoning effort, output styles

### N) Verification & observability
- Show loaded config diagnostics, logs, traces
- List installed extensions/plugins/servers

### O) Updates, channels, feature flags
- Stable vs latest channels, preview builds, experimental toggles

---

# Platform maps (authoritative config locations)

## Claude Code (CLI)
- User settings: ~/.claude/settings.json
- Project: .claude/settings.json, .claude/settings.local.json
- Instructions: CLAUDE.md (project root + nested)
- Global instructions: ~/.claude/CLAUDE.md
- Rules: .claude/rules/*.md (project), ~/.claude/rules/*.md (global)
- Plugins: .claude/plugins/<name>/ with SKILL.md, agents, hooks
- MCP: .mcp.json (project), ~/.claude.json (user)

## OpenAI Codex
- Instructions: AGENTS.md / AGENTS.override.md (global + project)
- Rules: rules/ directory
- Skills: SKILL.md + scripts/assets/references
- Config: config.toml

## VS Code + GitHub Copilot
- Instructions: .github/copilot-instructions.md, AGENTS.md
- Agents: .github/agents/*.agent.md
- MCP: .vscode/mcp.json (project), %APPDATA%/Code/User/mcp.json (global)

## Gemini CLI
- User settings: ~/.gemini/settings.json
- Project: .gemini/settings.json
- Instructions: GEMINI.md
- Extensions: ~/.gemini/extensions/

## OpenCode
- Config: ~/.config/opencode/, opencode.json (project)
- Agent profiles: oh-my-opencode.json
- Instructions: OPENCODE.md

## Kilo Code
- MCP: .kilocode/mcp.json (project)
- Global: VS Code globalStorage path

## Antigravity
- MCP: ~/.gemini/antigravity/mcp_config.json (global only)
- Shares GEMINI.md for instructions

---

# Completeness guardrail
Before finishing an answer, confirm you covered:
1) instructions  2) prompts  3) skills  4) agents  5) subagents
6) hooks  7) tools+permissions  8) packaging  9) context boundaries
10) secrets  11) sandbox  12) approvals  13) model controls
14) updates/flags  15) verification/diagnostics
