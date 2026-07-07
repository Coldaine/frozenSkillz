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
| Sessions (data) | `C:\Users\pmacl\.copilot\session-state\<uuid>\events.jsonl`, `logs\`, `vscode.session.*` | Also used by the VS Code integration. |

## Session format (observed 2026-06-08)

`events.jsonl` — one JSON event per line, each with `id`, `parentId`, `type`, `timestamp`, `data`. Event graph: `session.start` -> `user.message` -> (`assistant.turn_start` -> `assistant.message` -> tool events -> `assistant.turn_end`)* -> `session.shutdown`. Native `sessionId` is in the `session.start` event. Parser: `D:\_projects\llm-archiver\tools\copilot_cli.yaml`.

## Verify

```powershell
copilot --version
gh auth status
```
