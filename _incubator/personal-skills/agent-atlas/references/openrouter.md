# OpenRouter (provider, not an app)

Last checked: 2026-07-07.

OpenRouter has no config root of its own on this machine. It is a model-routing API provider consumed by agent tools; "setting up OpenRouter" always means configuring some tool's provider settings plus a key.

## Where it appears

| Consumer | Where | Notes |
|---|---|---|
| OpenCode | `C:\Users\pmacl\.config\opencode\AVAILABLE_PROVIDERS.md` lists `openrouter`; credentials in `C:\Users\pmacl\.local\share\opencode\auth.json` | Never open auth.json; record key names only. |
| Environment | No `OPENROUTER_*` variables set in the current session as of 2026-07-07 | Re-check with the command below before assuming. |

## Key handling

Keys belong in Doppler (see the `doppler` skill) or the consuming tool's own auth store — never in dotfiles, docs, or this repo. Record only: key name, which Doppler project/config holds it, and which tool consumes it.

## Verify

```powershell
Get-ChildItem env: | Where-Object Name -match 'OPENROUTER' | ForEach-Object Name
Select-String -Path "$env:USERPROFILE\.config\opencode\AVAILABLE_PROVIDERS.md" -Pattern 'openrouter'
```
