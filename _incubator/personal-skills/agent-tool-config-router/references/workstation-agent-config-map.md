# Workstation Agent Config Map

Last checked: 2026-07-07.

This file is local to Patrick's workstation. Verify live files before changing behavior.

## Claude Code and OMC

| Surface | Path or command | Role |
|---|---|---|
| Vanilla Claude root | `C:\Users\pmacl\.claude` | Default `claude` config root. Should stay free of OMC markers unless intentionally changed. |
| OMC Claude root | `C:\Users\pmacl\.claude-omcc` | Explicit OMC profile root. |
| PowerShell launchers | `C:\Users\pmacl\OneDrive\Documents\PowerShell\Microsoft.PowerShell_profile.ps1` | Defines `claudeDanger`, `claudeOmc`, `claudeOmcDanger`, `claudeOmcSafe`, `omcProfile`, and aliases. |
| OMC CLI | `omcProfile` | Runs `omc` with `CLAUDE_CONFIG_DIR=C:\Users\pmacl\.claude-omcc`. |
| OMC package | `oh-my-claude-sisyphus` | Global npm package providing `omc`; verify with `omcProfile --version` and `npm list -g oh-my-claude-sisyphus --depth=0`. |

Expected launch behavior:

```powershell
claude          # vanilla Claude Code
claudeDanger    # vanilla + --dangerously-skip-permissions
omcc            # OMC profile + --dangerously-skip-permissions
claudeOmc       # same as omcc
omccSafe        # OMC profile without danger mode
claudeOmcSafe   # same as omccSafe
omcProfile      # OMC CLI against .claude-omcc
```

Verify:

```powershell
Get-Command claudeDanger,claudeOmc,claudeOmcDanger,claudeOmcSafe,omcProfile,omcc,omccSafe
claude --version
omcc --version
omccSafe --version
omcProfile --version
```

## Other Agent Tools

Per-tool detail lives in sibling files: `codex.md`, `cursor.md`, `gemini-antigravity.md`, `opencode.md`, `kilo.md`, `copilot-cli.md`, `goose.md`, `openrouter.md`.

Installed as of 2026-07-07: Codex 0.142.5, Cursor (+cursor-agent), Gemini CLI + Antigravity, OpenCode 1.17.12 (+oh-my-openagent), Kilo 7.3.54, Copilot CLI 1.0.50, Goose 1.38.0. Also present: `C:\Users\pmacl\.continue\skills` (vestigial Continue surface holding gws-* skills — confirm whether Continue is still in use before touching).

Session-learnings store: `D:\_projects\agent-control-plane` — Accounts/Learnings/Meta per project, markdown only (no database). The one real session database on this machine is OpenCode's `opencode.db`; see `opencode.md`.

## Skill Surfaces

| Surface | Path | Role |
|---|---|---|
| Live personal shared skills | `C:\Users\pmacl\.agents\skills` | Current personal skill source for shared-discovery clients. |
| Claude compatibility skills | `C:\Users\pmacl\.claude\skills` | Compatibility surface; personal skills should be junctions or intentional exceptions. |
| Codex system/runtime skills | `C:\Users\pmacl\.codex\skills` | Runtime/system surface; do not author personal skills here by default. |
| Frozen active skills | `D:\_projects\frozenSkillz\plugins\frozen-skills\skills` | Reviewed marketplace skills. |
| Frozen gated personal skills | `D:\_projects\frozenSkillz\_incubator\personal-skills` | Evaluation/reference copies, not installable. |

## Durable Policy

The current policy record is:

```text
D:\_projects\coldaine-configurations\configurations\2026-07-07-agent-tool-configuration-policy.md
```

When live behavior changes, update that policy record or add a superseding dated record in the same folder.
