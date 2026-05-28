---
name: mcp-deployment-guide
description: >
  Reference guide for deploying and configuring MCP servers across all AI tools.
  Covers config file locations, format differences, secrets management, and
  deployment patterns for Claude Code, VS Code, Gemini CLI, OpenCode,
  Kilo Code, Antigravity, and other MCP-compatible clients.
version: 1.2.0
tags:
  - mcp
  - deployment
  - configuration
  - secrets
---

# MCP Server Deployment Guide

## Quick Reference: Config File Locations

| Tool | Windows Global | Linux Global | Project-Level |
|------|----------------|--------------|---------------|
| **Claude Code** | %USERPROFILE%\.claude.json | ~/.claude.json | .mcp.json |
| **Claude Desktop** | %APPDATA%\Claude\claude_desktop_config.json | ~/.config/Claude/claude_desktop_config.json | N/A |
| **VS Code** | %APPDATA%\Code\User\mcp.json | ~/.config/Code/User/mcp.json | .vscode/mcp.json |
| **Gemini CLI** | %USERPROFILE%\.gemini\settings.json | ~/.gemini/settings.json | .gemini/settings.json |
| **Antigravity** | %USERPROFILE%\.gemini\antigravity\mcp_config.json | ~/.gemini/antigravity/mcp_config.json | N/A |
| **Kilo Code** | (VS Code globalStorage path) | (VS Code globalStorage path) | .kilocode/mcp.json |
| **OpenCode** | %USERPROFILE%\.config\opencode\mcp.json | ~/.config/opencode/mcp.json | opencode.json |

## Configuration Formats

### Claude Code (.mcp.json or ~/.claude.json)
```json
{"mcpServers":{"name":{"command":"npx","args":["-y","pkg"],"env":{"KEY":"${KEY}"}}}}
```

### VS Code (.vscode/mcp.json)
```json
{"mcpServers":{"name":{"command":"npx","args":["-y","pkg"],"env":{"KEY":"${env:KEY}"}}}}
```
Note: VS Code uses `${env:VAR}` not `${VAR}`.

### Gemini CLI (.gemini/settings.json)
```json
{"mcpServers":{"name":{"command":"npx","args":["-y","pkg"]}}}
```

### Kilo Code (.kilocode/mcp.json)
```json
{"mcpServers":{"name":{"url":"https://example.com/mcp","type":"http"}}}
```

## Secrets Pattern

**Never hardcode API keys in config files.** Use environment variable substitution.

| Tool | Env Var Syntax |
|------|----------------|
| Claude Code | `${VAR}` |
| VS Code | `${env:VAR}` |
| Gemini CLI | `${VAR}` |
| OpenCode | `${VAR}` |
| Kilo Code | Via VS Code settings |

## Server Types

| Type | When to Use | Example |
|------|------------|---------|
| **stdio** | Local process, per-session | `npx -y firecrawl-mcp` |
| **HTTP/SSE** | Remote or long-running | MCP on a Pi or VM |
| **Docker** | Containerized | Docker MCP Toolkit |

## Configuration Templates

This repository provides ready-to-use MCP configuration templates in the `mcp/` directory:

- **GitHub**: `mcp/github.json` — Standard configuration for `@modelcontextprotocol/server-github`.
- **NotebookLM**: `mcp/notebooklm.json` — Placeholder configuration for NotebookLM.

To use these templates, copy the content into your tool's configuration file (e.g., `.mcp.json` for Claude Code) and ensure the required environment variables are set.

## Adding a New MCP Server

1. Set up the secret (add to store, sync to env vars)
2. Configure in each tool using the formats above or use a template from `mcp/`
3. Test connectivity in each configured tool

## Common Pitfalls

- VS Code uses `${env:VAR}` not `${VAR}`
- Kilo Code project config takes precedence over global on name collision
- Claude Code project config is `.mcp.json` (dot-prefixed)
- Antigravity is global-only — no project-level MCP config
- OneDrive redirection on Windows can move config files unexpectedly
