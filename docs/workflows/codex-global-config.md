# Codex Global Configuration

This repository owns reviewed, machine-global Codex configuration under
`config/codex/global/`. This lane is for Codex-native prompts and custom-agent
profiles that must apply across projects; it is separate from skill distribution.

The first profile pairs two artifacts:

- `agents/chrome-pilot.toml` defines the fast Luna browser worker.
- `AGENTS.browser-delegation.md` requires the primary agent to delegate browser
  work to that worker whenever browser use is required.

Install or refresh the profile:

```powershell
python scripts/sync_codex_global_config.py --apply
```

Check for drift without writing:

```powershell
python scripts/sync_codex_global_config.py --check
```

The synchronizer owns the complete `~/.codex/agents/chrome-pilot.toml` file and
only the marked browser-delegation block inside `~/.codex/AGENTS.md`. It preserves
all other global instructions and fails on malformed or duplicate markers.
