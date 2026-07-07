# OpenCode (+ oh-my-openagent)

Last checked: 2026-07-07. Verify live before changing behavior.

- CLI: `opencode` -> `C:\Users\pmacl\AppData\Roaming\npm\opencode.ps1`, version `1.17.12`
- Config root: `C:\Users\pmacl\.config\opencode`
- Data root: `C:\Users\pmacl\.local\share\opencode`

## Config surfaces

| Surface | Path | Notes |
|---|---|---|
| OMOA config | `C:\Users\pmacl\.config\opencode\oh-my-openagent.json` | `oh-my-openagent` is the OpenCode analog of OMC. Many timestamped `.bak`/`backup` siblings exist — the un-suffixed file is live. |
| Profiles | `C:\Users\pmacl\.config\opencode\profiles\`, `model-profiles.md`, `burner-vs-code-opus.jsonc` | |
| Providers | `C:\Users\pmacl\.config\opencode\AVAILABLE_PROVIDERS.md` | Lists `openrouter` among available providers. See `references/openrouter.md`. |
| Agent contract | `C:\Users\pmacl\.config\opencode\AGENTS.md` | |
| Skills | `C:\Users\pmacl\.config\opencode\skills\` | Personal source of truth stays `C:\Users\pmacl\.agents\skills`. |
| LSP | `C:\Users\pmacl\.config\opencode\lsp.json` | |

## Data / session store

| Surface | Path | Notes |
|---|---|---|
| Session database | `C:\Users\pmacl\.local\share\opencode\opencode.db` (+ `-shm`, `-wal`) | SQLite. The only real agent-session database on this machine; other tools use jsonl/dirs. Query read-only; never edit while OpenCode runs. |
| Storage / snapshots | `storage\`, `snapshot\`, `tool-output\`, `repos\`, `log\` | |
| Auth | `C:\Users\pmacl\.local\share\opencode\auth.json`, `account.json` | Secrets. Never open or copy values; see the `doppler` skill. |

## Verify

```powershell
opencode --version
Test-Path "$env:USERPROFILE\.local\share\opencode\opencode.db"
```
