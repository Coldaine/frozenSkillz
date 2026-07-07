# GitHub Copilot CLI

Last checked: 2026-07-07. Verify live before changing behavior.

- CLI: `copilot` -> `C:\Users\pmacl\AppData\Roaming\npm\copilot.ps1`, version `GitHub Copilot CLI 1.0.50`
- Related: `gh` -> `C:\Program Files\GitHub CLI\gh.exe` (auth is shared via GitHub account, not local key files)
- Config root: `C:\Users\pmacl\.copilot`

## Surfaces

| Surface | Path | Notes |
|---|---|---|
| Config | `C:\Users\pmacl\.copilot\config.json` | Currently minimal (only `firstLaunchAt`). |
| Agents / hooks | `C:\Users\pmacl\.copilot\agents\`, `hooks\` | |
| Skills | `C:\Users\pmacl\.copilot\skills\` | Personal source of truth stays `C:\Users\pmacl\.agents\skills`. |
| Sessions (data) | `C:\Users\pmacl\.copilot\session-state\`, `logs\`, `vscode.session.*` | Also used by the VS Code integration. |

## Verify

```powershell
copilot --version
gh auth status
```
