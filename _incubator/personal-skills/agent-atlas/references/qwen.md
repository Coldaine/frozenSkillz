# Qwen CLI

Last checked: 2026-06-08 survey (root re-confirmed 2026-07-07). Verify live before changing behavior.

- Config root: `C:\Users\pmacl\.qwen` (exists; minimal contents: `installation_id`, `output-language.md`, empty `logs.json`, debug txt)
- No CLI found on PATH as of 2026-07-07

## Session data

Expected chat locations `~\.qwen\tmp\*\chats\*.json` contained **no chat files** in the 2026-06-08 survey — there is no live Qwen transcript history on this machine. Session IDs are path-derived (file move breaks identity). Format details and open questions: `D:\_projects\agent-control-plane\capture\scratch\qwen-session-reconstruction.md`; parser: `D:\_projects\llm-archiver\tools\qwen.yaml`.

## Verify

```powershell
Get-ChildItem "$env:USERPROFILE\.qwen" -Recurse -File | Select-Object FullName,Length
```
