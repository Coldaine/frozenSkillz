# Optional automation scripts

These scripts are **not bundled** in the incubating skill. Consuming projects implement them locally.

Reference implementations live in Scratch: `D:\_projects\Scratch\tools\`

| Script | Purpose |
|--------|---------|
| `icepanel-layout.ps1` | Fetch model objects → scaffold DiagramCreate JSON with grid zones |
| `icepanel-push-diagrams.ps1` | POST full DiagramCreate bodies from `imports/diagrams/` |
| `icepanel-driver.ps1` | General REST driver (import, list, create-diagram with body file) |
| `icepanel-ui-debug.ps1` | Diagnose blank canvas (diagram count) |
| `icepanel-healthcheck.ps1` | Auth smoke test |

Run with Doppler when using API keys:

```bash
doppler run -- powershell -NoProfile -File .\tools\icepanel-push-diagrams.ps1 portfolio
```

Document script paths in your project overlay (e.g. `scratch-overlay.md`).
