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
| Session database | `C:\Users\pmacl\.local\share\opencode\opencode.db` (+ `-shm`, `-wal`) | SQLite. The only real agent-session database on this machine; other tools use jsonl/dirs. Query read-only; never edit while OpenCode runs. Schema notes below. |
| Storage / snapshots | `storage\`, `snapshot\`, `tool-output\`, `repos\`, `log\` | |
| Auth | `C:\Users\pmacl\.local\share\opencode\auth.json`, `account.json` | Secrets. Never open or copy values; see the `doppler` skill. |

## opencode.db schema (reverse-engineered 2026-06-08)

Full notes: `D:\_projects\agent-control-plane\capture\scratch\opencode-session-reconstruction.md`; parser: `D:\_projects\llm-archiver\tools\opencode.yaml`.

- Tables: `session` (id `ses_*`) -> `message` (id `msg_*`, FK `session_id`) -> `part` (id `prt_*`, FK `message_id`); plus `session_message` (meta-only stream: `agent-switched` / `model-switched`, ordered by `seq` — NOT chat turns, and its ids also use the `msg_` prefix).
- All `data` columns are JSON text; timestamps are epoch ms.
- Gotchas: user prompt text lives in `message.data.summary`, not in parts; one user turn spawns multiple assistant `message` rows (order by `time_created`, not `parentID`); subagent linkage is `session.parent_id` (session-to-session), while `message.data.parentID` is intra-session threading.
- `part.data.type` values: `step-start`, `reasoning`, `text`, `tool` (with `callID`, `state.status/input/output`), `step-finish`.
- The DB was 664 MB in June 2026 — always filter by session, never full-scan.

## Verify

```powershell
opencode --version
Test-Path "$env:USERPROFILE\.local\share\opencode\opencode.db"
sqlite3 "$env:USERPROFILE\.local\share\opencode\opencode.db" "SELECT id,title,parent_id FROM session ORDER BY time_updated DESC LIMIT 5"
```
