# Codex (OpenAI Codex CLI)

Last checked: 2026-07-07. Verify live before changing behavior.

- CLI: `codex` -> `C:\Users\pmacl\.local\bin\codex.ps1`, version `codex-cli 0.142.5`
- Config root: `C:\Users\pmacl\.codex`

## Config surfaces

| Surface | Path | Notes |
|---|---|---|
| Main config | `C:\Users\pmacl\.codex\config.toml` | Top keys: `approval_policy`, `model`, `model_reasoning_effort`, `personality`, `sandbox_mode`, `web_search`, `service_tier`, `notify`, `[agents]`, `[plugins.*]`. |
| Plugins | `[plugins."<name>@openai-curated"]` blocks in `config.toml`, plus `C:\Users\pmacl\.codex\plugins\` | Curated set enabled: github, vercel, documents, spreadsheets, presentations, superpowers, notion, jam, coderabbit, cloudflare, hugging-face, computer-use, browser. |
| Skills | `C:\Users\pmacl\.codex\skills` | Runtime/system surface. Do NOT author personal skills here; personal skills live in `C:\Users\pmacl\.agents\skills`. |
| Rules / hooks | `C:\Users\pmacl\.codex\rules\`, `C:\Users\pmacl\.codex\hooks\` | |
| Sessions (data) | `C:\Users\pmacl\.codex\sessions\<year>\` | Also contains an `.omc` marker directory. Transcript ground truth for retrospectives. |
| Secrets | `C:\Users\pmacl\.codex\secrets\`, `auth.json` | Never open or copy values. Record names/owners only; see the `doppler` skill. |

## Known issues

- `morph-mcp` version mismatch warning at startup (pre-existing, unrelated to Claude/OMC launchers).

## Verify

```powershell
codex --version
Get-Command codex
Select-String -Path "$env:USERPROFILE\.codex\config.toml" -Pattern '^(model|approval_policy|sandbox_mode)'
```
