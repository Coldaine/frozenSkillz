# Cursor (IDE + cursor-agent CLI)

Last checked: 2026-07-07. Verify live before changing behavior.

- IDE: `C:\Program Files\cursor\` (`cursor` CLI -> `resources\app\bin\cursor.cmd`)
- Agent CLI: `cursor-agent` -> `C:\Users\pmacl\AppData\Local\cursor-agent\cursor-agent.ps1`
- Config root: `C:\Users\pmacl\.cursor`

## Config surfaces

| Surface | Path | Notes |
|---|---|---|
| MCP servers | `C:\Users\pmacl\.cursor\mcp.json` | Currently: Pieces, morph-mcp, notebooklm-mcp, context7. |
| Rules | `C:\Users\pmacl\.cursor\rules\` plus IDE Settings -> Rules | |
| Skills | `C:\Users\pmacl\.cursor\skills\` and `skills-cursor\` | Global skill surfaces; personal source of truth stays `C:\Users\pmacl\.agents\skills`. |
| Plugins | `C:\Users\pmacl\.cursor\plugins\`, `extensions\` | |
| Sessions (data) | `C:\Users\pmacl\.cursor\projects\`, `ai-tracking\`, `worktrees\` | Transcript/evidence sources for retrospectives. |
| Setup audit | `C:\Users\pmacl\.cursor\CURSOR_CONFIGURATION_REPORT.md` | Generated 2026-05-26. Key finding: ~95% of config is global, ~5% per-project; more installed than used. Read before restructuring Cursor config. |

## Configuration pattern

Config is intentionally global-first (user hops between many repos). Recently opened repos generally have no `.cursor/rules/`, `.cursor/mcp.json`, or `.cursor/skills/`. Before adding project-level Cursor config, check the audit report and confirm the global surface does not already cover it.

## Verify

```powershell
cursor-agent --version
Get-Content "$env:USERPROFILE\.cursor\mcp.json" -Raw | ConvertFrom-Json | ForEach-Object { $_.mcpServers.PSObject.Properties.Name }
```
