# Kilo Code

Last checked: 2026-07-07. Verify live before changing behavior.

- CLI: `kilo` -> `C:\Users\pmacl\AppData\Roaming\npm\kilo.ps1`, version `7.3.54`
- Config roots: `C:\Users\pmacl\.kilo` AND `C:\Users\pmacl\.kilocode` — both exist

## Known ambiguity: duplicated roots

Both `.kilo` and `.kilocode` contain a `skills\` directory and an identical `package.json` depending on `@kilocode/plugin@7.2.20`. Which root the current CLI actually reads has NOT been verified. Before changing Kilo config:

1. Check Kilo's own docs/`--help` for the canonical root.
2. Test with a marker file to confirm which `skills\` directory is discovered.
3. Record the answer here and in the coldaine-configurations policy record, then consider retiring the stale root.

## Surfaces

| Surface | Path | Notes |
|---|---|---|
| Plugin package | `<root>\package.json` -> `@kilocode/plugin@7.2.20` | Same in both roots. |
| Skills | `<root>\skills\` | Personal source of truth stays `C:\Users\pmacl\.agents\skills`. |

## Verify

```powershell
kilo --version
Get-Content "$env:USERPROFILE\.kilo\package.json","$env:USERPROFILE\.kilocode\package.json"
```
