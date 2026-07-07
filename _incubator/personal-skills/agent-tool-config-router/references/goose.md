# Goose (Block)

Last checked: 2026-07-07. Verify live before changing behavior.

- CLI: `goose` -> `C:\Users\pmacl\.local\bin\goose.exe`, version `1.38.0`
- Config root: `C:\Users\pmacl\.config\goose` (exists; no `config.yaml` at the default path as of 2026-07-07 — inspect the directory before assuming defaults)

Lightly used on this workstation. Before configuring, list the config root and run `goose configure` docs rather than assuming Linux-default paths.

## Verify

```powershell
goose --version
Get-ChildItem "$env:USERPROFILE\.config\goose" -Force
```
