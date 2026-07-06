# run-opencode — reference

Detailed material for the `run-opencode` skill. Loaded on demand; the lean overview is in SKILL.md.

## Contents
- Architecture (the three layers)
- Prerequisites
- Install (fresh machine)
- Update (and the Bun trap)
- Configure model routing (schema, policy, roster)
- Profiles (how the switcher works)
- Gotchas
- Troubleshooting

## Architecture (the three layers)

1. **OpenCode** reads `~/.config/opencode/opencode.json` — minimal; registers MCP servers and loads
   the plugin via `"plugin": ["oh-my-openagent"]`. No model choices here.
2. **oh-my-openagent** (npm `oh-my-openagent`) — the orchestration plugin. The TUI loads it from
   `~/.cache/opencode/packages/` (currently 4.8.1, with a legacy `oh-my-opencode` alias tree at the
   same 4.8.1 — harmless). The `node_modules/` under `~/.config/opencode` is a **decoy**, not the
   load path; bumping its version is a no-op for the running TUI.
3. **`~/.config/opencode/oh-my-openagent.json`** — the file you edit. Holds the `agents` and
   `categories` blocks. `.jsonc` is also valid.

## Prerequisites

- **Node** + **npm** — run the driver and the CLI.
- **bun** — required by the omo installer/updater (`winget install Oven-sh.Bun` if absent).
- OpenCode CLI on PATH: `opencode --version`.

## Install (fresh machine)

> Mutating — touches a live install. Sourced from official docs (opencode.ai, omo.dev).

1. **OpenCode CLI** (bun is fastest):
   ```bash
   bun add -g opencode-ai            # or: npm install -g opencode-ai
   # or curl bootstrap:  curl -fsSL https://opencode.ai/install | bash
   ```
2. **oh-my-openagent** — official installer; do **not** `npm/bun add -g` it:
   ```bash
   bunx oh-my-openagent install      # TUI walks subscriptions + model routing
   ```
   Registers `"plugin": ["oh-my-openagent"]` in `opencode.json`; requires OpenCode >= 1.4.0.
3. **Auth + verify:**
   ```bash
   opencode auth login
   bunx oh-my-openagent doctor       # System/Config/Plugin/Tools/Models/Team checks
   ```

## Update (and the Bun trap)

- **OpenCode CLI:** `opencode upgrade` (or `opencode upgrade <version>` to pin).
- **omo plugin** — check first (read-only): `bunx oh-my-openagent get-local-version`.

> ⚠️ **The Bun trap (verified from history).** The official updater `bunx oh-my-openagent install`
> uses **Bun**, which fights npm inside `~/.config/opencode` and reintroduces a stale nested
> `@opencode-ai/sdk` ("there's always old pin stuff"). Keep `~/.config/opencode` **npm-only**. After
> any bun-based install touches it, clean up:
> ```bash
> cd ~/.config/opencode && rm -f bun.lock && npm prune
> ```

## Configure model routing (schema, policy, roster)

Edit `~/.config/opencode/oh-my-openagent.json`. Back up first: `node driver.mjs backup`.

Per-entry schema (in both `agents` and `categories`):
- `model`: `"provider/model"` (provider list in `~/.config/opencode/AVAILABLE_PROVIDERS.md`)
- `reasoningEffort`: `none|minimal|low|medium|high|xhigh|max` (OpenAI + DeepSeek; `xhigh`→`max` for
  DeepSeek). MiMo takes neither effort field.
- `variant`: `max|high|medium|low|xhigh` (OpenAI/Gemini effort knob).
- `fallback_models`: array; string OR object form (`{ "model": …, "variant"/"reasoningEffort": … }`), mixable.

Example (DeepSeek primary, OpenAI fallback):
```jsonc
"oracle": {
  "model": "opencode-go/deepseek-v4-pro",
  "reasoningEffort": "high",
  "fallback_models": [ { "model": "openai/gpt-5.5", "variant": "xhigh" } ]
}
```

**Roster (authoritative, from omo source).** Agents (14): `sisyphus prometheus metis atlas hephaestus
oracle momus explore librarian multimodal-looker sisyphus-junior athena athena-junior council-member`
(the last three have no hardcoded model requirement → resolve via categories/defaults). Categories (8):
`quick deep ultrabrain writing artistry visual-engineering unspecified-low unspecified-high`.

**Vision:** opencode-go has no vision models; use Google Gemini (`gemini-3.1-pro-preview`,
`gemini-3-flash-preview`) for `multimodal-looker`/`visual-engineering`/`artistry`.

After editing, re-run `node driver.mjs` to confirm it parses and shows the new routing.
(See also the companion skill `omc-learned/edit-opencode-config`.)

## Profiles (how the switcher works)

Two saved profiles live at `~/.config/opencode/profiles/{openai,cheap}.json`, each a full
`{ agents, categories }` block covering all 14 agents + 8 categories. Regenerate with
`node ~/.config/opencode/profiles/build-profiles.mjs`.

- **Canonical switcher:** `~/.config/opencode/profiles/switch.mjs` — self-contained (no dependency on
  the skill folder), has `--undo`, validates JSON before writing, backs up first, writes BOM-free.
- `node driver.mjs profile <name>` is a convenience alias (it writes its pre-switch backup into a
  dated subfolder; switch.mjs writes flat timestamped backups — both under `agent-config-backups/`).
- After any switch, **restart the OpenCode TUI** (config is read at launch).

## Gotchas

- **UTF-8 BOM breaks `oh-my-openagent.json`** for strict `JSON.parse`/`ConvertFrom-Json`. PowerShell's
  old `Out-File` adds one; use `[System.IO.File]::WriteAllText($p,$c,(New-Object System.Text.UTF8Encoding $false))`
  or PS7 `Set-Content -Encoding utf8`. omo 4.8.1 strips it, but write clean anyway.
- **TUI loads from `~/.cache/opencode/packages/`, not `~/.config/opencode/node_modules/`** (decoy).
- **Two version numbers:** CLI (`opencode-ai`) and omo plugin upgrade separately.
- **"Everything is Codex/OpenAI" is a config-content bug, not a parse failure.** omo's hardcoded
  `AGENT_MODEL_REQUIREMENTS` defaults are OpenAI-heavy, so any agent without an explicit non-OpenAI
  primary lands on OpenAI. Fix the `agents` block (and use the `cheap` profile).
- **Don't global-install omo;** if you run the bun installer, follow with `rm -f bun.lock && npm prune`.

## Troubleshooting

| Symptom | Fix |
|---|---|
| Driver: `config ✗ INVALID: Unexpected token '﻿'` | BOM — re-save UTF-8 without BOM. Driver tolerates it for reading. |
| `opencode: command not found` | CLI not on PATH; `bun add -g opencode-ai` (or npm), reopen shell. |
| `node_modules/oh-my-openagent` not resolvable via `require` | Expected — read its version from `node_modules/oh-my-openagent/package.json` directly. |
| omo reports update available | `bunx oh-my-openagent install`, then the npm-only cleanup (back up first). |
| hephaestus won't run on non-OpenAI | Upstream `requiresProvider: ["openai"]`; keep an OpenAI fallback in its chain. |
