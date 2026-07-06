---
name: edit-opencode-config
description: Inspect, back up, and safely edit OpenCode agent/category model choices in oh-my-openagent.json
triggers:
  - "edit my opencode config"
  - "change which model an opencode agent uses"
  - "edit openagent / oh-my-openagent config"
  - "rebalance opencode agents off codex/openai"
  - "back up my opencode agent choices"
  - "update opencode agent models"
---

# Edit OpenCode (oh-my-openagent) config

How to inspect, back up, and edit the per-agent and per-category model choices for OpenCode
on this machine. The model choices do NOT live in `opencode.json` — they live in the
`oh-my-openagent` plugin's config file.

## The three layers (where things actually live)

1. **OpenCode** reads `~/.config/opencode/opencode.json`. On this machine it is minimal — it
   registers MCP servers and loads the plugin via `"plugin": ["oh-my-openagent"]`. **No model
   choices here.** Don't edit this to change models.
2. **oh-my-openagent** (npm plugin `oh-my-openagent`, the OpenCode analog of oh-my-opencode).
   Plugin code lives in `~/.config/opencode/node_modules/` — never hand-edit it.
3. **`~/.config/opencode/oh-my-openagent.json`** ← **this is the file you edit.** `.jsonc` is
   also valid (comments + trailing commas). Project overrides may exist at
   `.opencode/oh-my-openagent.json[c]` walked from cwd up to `$HOME`.

Windows path note: `~/.config/opencode` resolves to `C:\Users\<user>\.config\opencode`
(this user: `C:\Users\pmacl\.config\opencode`). The docs also list `%APPDATA%\opencode\` as a
valid user-config location, but on this machine the live file is under `~/.config/opencode`.

## Inputs
- Which agent(s) or category(ies) to change.
- The target model as `provider/model` (provider list is in
  `~/.config/opencode/AVAILABLE_PROVIDERS.md`).
- Optional: reasoning effort and fallback chain.

## Workflow

### 1. Inspect current state
Read `~/.config/opencode/oh-my-openagent.json`. The two sections that matter:
- `agents` — named agents and their `model` / `variant` / `fallback_models`.
- `categories` — model profiles the `task()` tool delegates to by task weight.

Named agents on this machine: `sisyphus` (orchestrator), `prometheus` (planner),
`metis` (analysis), `atlas` (executor), `hephaestus` (builder), `oracle` (architecture),
`momus` (critic), `explore` (search), `librarian` (docs lookup),
`multimodal-looker` (vision), `sisyphus-junior` (light sub-orchestrator).

Categories: `quick`, `deep`, `ultrabrain`, `unspecified-low`, `unspecified-high`,
`writing`, `visual-engineering`, `artistry`.

### 2. ALWAYS back up before editing
Copy the live file into a dated folder (keeps it out of the ~37 plugin `.bak` files that
clutter the config root):
```bash
D=$(date +%F)   # if date is unavailable, use the known current date
mkdir -p "$HOME/.config/opencode/agent-config-backups/$D"
cp "$HOME/.config/opencode/oh-my-openagent.json" \
   "$HOME/.config/opencode/agent-config-backups/$D/oh-my-openagent.snapshot.json"
cp "$HOME/.config/opencode/opencode.json" \
   "$HOME/.config/opencode/agent-config-backups/$D/opencode.snapshot.json"
```
Optionally also write a readable `agent-model-choices.md` table beside the snapshots.

### 3. Edit `oh-my-openagent.json`
Use exact-string Edit on the `agents` / `categories` block. Schema per entry:
- `model`: `"provider/model"` (e.g. `"anthropic/claude-opus-4-8"`, `"openai/gpt-5.5-fast"`).
- `variant`: `max | high | medium | low | xhigh` (effort knob for most models).
- `reasoningEffort`: `none | minimal | low | medium | high | xhigh | max` (OpenAI reasoning only).
- `fallback_models`: array, **string OR object form, mixable**:
  ```jsonc
  "fallback_models": [
    "opencode-go/glm-5.1",                              // string = no extra settings
    { "model": "openai/gpt-5.4", "variant": "high" },  // object = per-model settings
    { "model": "openai/gpt-5.5", "reasoningEffort": "high", "maxTokens": 8192 }
  ]
  ```
- Other valid per-entry fields: `temperature`, `top_p`, `maxTokens`, `prompt`,
  `prompt_append`, `thinking` (Anthropic), `tools`, `disable`, `permission`.

Example — move the architecture advisor off OpenAI:
```jsonc
"oracle": {
  "model": "anthropic/claude-opus-4-8",
  "variant": "xhigh",
  "fallback_models": [
    { "model": "openai/gpt-5.5-fast", "variant": "xhigh" },
    "opencode-go/glm-5.1"
  ]
}
```

### 4. Verify
- Re-read the file and confirm the edit is present.
- Validate JSON parses: `node -e "JSON.parse(require('fs').readFileSync(process.argv[1],'utf8'))" <file>`
  (only if the file is `.json`, not `.jsonc`).
- Report the diff (old model → new model) back to the user.

## Model resolution order (for reasoning about behavior)
1. UI-selected model (primary agents) → 2. user config override (this file) →
3. category default → 4. user `fallback_models` → 5. built-in provider fallback chain →
6. system default. Fallbacks fire on quota/rate-limit/API errors.

## Pitfalls
- **Do not edit `opencode.json` to change models** — wrong layer; it only loads the plugin.
- **Claude models reject `reasoningEffort`** — it's auto-stripped; use `variant` for Claude.
- Unsupported `variant`/`reasoningEffort` values are silently downgraded to the nearest supported.
- The plugin auto-writes `.bak` files on its own edits; that is NOT a substitute for the dated
  backup — make the dated snapshot yourself before editing.
- A migrations file (`oh-my-openagent.json.migrations.json`) records applied model-version
  migrations (e.g. `openai/gpt-5.4 -> openai/gpt-5.5`); don't fight a migration by reverting blindly.
- Updating the npm plugin version does NOT change model choices (they live in this JSON), and
  changing this JSON does NOT require a plugin update.

## Success criteria
- A dated backup exists under `agent-config-backups/<date>/` before any edit.
- `oh-my-openagent.json` still parses as valid JSON/JSONC.
- The requested agent/category now resolves to the intended `model` with intended fallbacks.
- User is shown the old→new diff.
