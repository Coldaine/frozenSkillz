# Gemini CLI and Antigravity

Last checked: 2026-07-07. Verify live before changing behavior.

- CLI: `gemini` -> `C:\Users\pmacl\.local\bin\gemini.ps1` (`gemini --version` returned empty in a scripted call on 2026-07-07 — verify interactively)
- Config root: `C:\Users\pmacl\.gemini` (shared by Gemini CLI and Antigravity)

## Config surfaces

| Surface | Path | Notes |
|---|---|---|
| Main settings | `C:\Users\pmacl\.gemini\settings.json` | Top keys: `model`, `general`, `security`, `ui`, `tools`, `experimental`, `mcpServers`, `skills`, `ide`, `agents`, `context`. |
| Global context | `C:\Users\pmacl\.gemini\GEMINI.md` | Gemini's analog of a global CLAUDE.md. |
| Skills | `C:\Users\pmacl\.gemini\skills\` | Personal source of truth stays `C:\Users\pmacl\.agents\skills`. |
| Extensions | `C:\Users\pmacl\.gemini\extensions\`, `extension_integrity.json` | |
| Antigravity | `C:\Users\pmacl\.gemini\antigravity\`, `antigravity-cli\`, `antigravity-ide\`, `antigravity-browser-profile\` | Antigravity IDE/CLI/browser surfaces live under the Gemini root, not their own root. |
| Trust / policy | `trusted_hooks.json`, `trustedFolders.json`, `policies\` | |
| Sessions (data) | `C:\Users\pmacl\.gemini\history\`, `projects.json`, `state.json` | |
| Accounts | `google_accounts.json` | Treat as sensitive; do not copy contents into docs. |

## Verify

```powershell
gemini --version
Get-Content "$env:USERPROFILE\.gemini\settings.json" -Raw | ConvertFrom-Json | ForEach-Object { $_.PSObject.Properties.Name }
```
