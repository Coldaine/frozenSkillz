---
name: run-opencode
description: Install, configure, update, health-check, and switch model profiles for OpenCode and the oh-my-openagent (omo) plugin. Use when asked to install/upgrade/update OpenCode, check OpenCode/openagent versions, switch agents between OpenAI and cheap/non-OpenAI models, fix or edit oh-my-openagent.json, inspect which model each agent uses, or back up the OpenCode config.
---

# run-opencode

OpenCode is a terminal AI coding agent (`opencode-ai` on npm). **oh-my-openagent** (*omo*) is a
plugin layered on top that defines the named agents (sisyphus, oracle, …) and their model routing.
Two independently-versioned pieces: the **CLI** and the **omo plugin**.

Model choices live in `~/.config/opencode/oh-my-openagent.json` (its `agents` and `categories`
blocks) — **not** in `opencode.json` (that only loads the plugin) and **not** in `node_modules/`
(a decoy; the running TUI loads from `~/.cache/opencode/packages/`).

Paths use forward slashes; `~` = home. The bundled `driver.mjs` is read-only except its explicit
`backup` / `profile` actions.

## Common tasks

**Health-check / inventory** — CLI & plugin versions (installed vs latest), config validity, and the
per-agent/category model map. Start here for "is OpenCode current?" or "what model is agent X on?":
```bash
node driver.mjs
```

**Switch model profiles** — flip the whole routing between `openai` and `cheap` (no-OpenAI). The
canonical switcher is self-contained and lives with the config; restart the OpenCode TUI after:
```bash
node ~/.config/opencode/profiles/switch.mjs          # show current profile + available
node ~/.config/opencode/profiles/switch.mjs cheap    # DeepSeek/MiMo/Gemini, zero OpenAI
node ~/.config/opencode/profiles/switch.mjs openai   # OpenAI-primary (needs credits)
node ~/.config/opencode/profiles/switch.mjs --undo   # restore the last backup
```

**Back up before any manual edit** (only write the driver makes):
```bash
node driver.mjs backup        # -> ~/.config/opencode/agent-config-backups/<date>/
```

## Always-apply rules

- **Model policy:** never use Claude (`anthropic/*`) in OpenCode; no Kimi-for-coding; DeepSeek V4 /
  MiMo V2.5 are preferred primaries; Gemini handles vision (opencode-go has **no** vision models).
  In the `cheap` profile every fallback chain ends in opencode-go or Gemini — never OpenAI.
- Save `oh-my-openagent.json` as **UTF-8 without BOM**.
- Keep `~/.config/opencode` **npm-only** — Bun reintroduces stale pins.
- `hephaestus` is pinned to `requiresProvider: ["openai"]` upstream — keep an OpenAI fallback in its
  chain, or flag it if it misbehaves on a no-credit account.

## Detailed references (load only when needed)

- **Architecture, prerequisites, install (fresh machine), update + the Bun trap** → [reference.md](reference.md)
- **Configure model routing — full schema, agent/category roster, profile internals** → [reference.md](reference.md)
- **Gotchas & troubleshooting — BOM, cache-vs-node_modules decoy, "everything is Codex"** → [reference.md](reference.md)
- **Human-facing profile guide (for the user, not the agent)** → `~/.config/opencode/model-profiles.md`
