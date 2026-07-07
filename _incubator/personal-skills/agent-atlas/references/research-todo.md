# Agent Atlas — Research TODO

Created 2026-07-07. This is the fill-in contract for a future research agent. The per-tool
reference files in this directory are first drafts built only from live filesystem scouting;
they have NOT had web research or deep on-machine investigation. Work through this file
tool by tool, updating the tool's reference file and ticking boxes here.

## Rules for the research agent

1. Web research the official docs/repo for each tool; cite the URL and the date checked.
2. Verify every claim locally before writing it (run the command, read the file). Tag anything
   you could not verify as `[unverified]`.
3. Update the `Last checked:` date in each reference file you touch.
4. Never open or copy auth/token files (`auth.json`, `secrets/`, `google_accounts.json`).
   Record names, locations, and owners only. Load the `doppler` skill for key handling.
5. Durable policy decisions go to `D:\_projects\coldaine-configurations`, not here.

## Canonical checklist — what we must know for EVERY agent

Each tool's reference file is complete when it answers all of these:

1. **Identity & install** — install channel (npm/binary/installer/winget), exact package name,
   installed version, how to update, release-notes/changelog URL.
2. **Launch surface** — commands and aliases, interactive vs headless/CI modes,
   permission/danger flags, env vars honored (esp. config-dir overrides like `CLAUDE_CONFIG_DIR`).
3. **Config precedence** — global root(s), project-level files, env overrides; the full
   precedence order and config file format.
4. **Instruction/context files** — which files it auto-reads (CLAUDE.md, AGENTS.md, GEMINI.md,
   rules dirs), discovery order, and any size limits.
5. **Skills** — discovery paths, supported skill format, whether it honors
   `C:\Users\pmacl\.agents\skills`, install/update mechanism.
6. **Plugins/extensions** — mechanism, marketplace, currently installed set.
7. **MCP** — where servers are configured (global vs project), supported transports,
   currently configured servers.
8. **Subagents/orchestration** — supported? how are they defined and invoked?
9. **Hooks/automation** — lifecycle hooks, event system, scheduled/background execution.
10. **Models & providers** — supported providers, how model selection works, OpenRouter
    support, local-model support.
11. **Auth & secrets** — auth flow, where tokens live, what must never be committed,
    Doppler integration status.
12. **Session/data stores** — transcript location and format, retention behavior,
    llm-archiver parser status (`D:\_projects\llm-archiver\tools\`).
13. **Sandboxing & permissions model** — what it can touch by default, how to restrict/expand.
14. **Web capabilities** — built-in search/fetch tooling.
15. **Known issues on this machine** — with upstream issue links where relevant.
16. **Verification commands** — commands that prove which config the tool actually loaded.

## Per-tool status

Legend: [x] drafted from live scouting · [ ] missing / needs research.
"Deep pass" = full run through the canonical checklist with web research.

### claude-code / OMC (in SKILL.md + workstation-agent-config-map.md)
- [x] Launcher split, config roots, versions (live-verified 2026-07-07)
- [ ] Deep pass: config precedence, hooks, MCP config locations, headless/CI usage
- [ ] OMC (`oh-my-claude-sisyphus`): upstream repo URL, what it actually modifies, update procedure
- [ ] Decide whether Claude/OMC content should move into its own `claude-omc.md` reference file

### codex.md
- [x] Version, config.toml top keys, plugin list, sessions path, secrets boundary
- [ ] Deep pass: full config.toml schema, `.omc` marker in sessions (what wrote it?), hooks/,
      rules/, automations/, memories/ semantics; sandbox modes; headless usage; MCP support
- [ ] morph-mcp mismatch warning: root cause and fix or suppression

### cursor.md
- [x] mcp.json servers, global-first pattern, audit report pointer
- [ ] Deep pass: cursor-agent CLI capabilities/version, skills vs skills-cursor difference,
      rules format, project-level `.cursor/` layout, worktrees behavior
- [ ] Act on the 2026-05-26 audit finding: prune installed-but-unused surface

### gemini-antigravity.md
- [x] settings.json keys, Antigravity surfaces, GEMINI.md
- [ ] Deep pass: why `gemini --version` returns empty scripted; Antigravity vs Gemini CLI
      responsibility split; extensions system; trusted_hooks/policies semantics
- [ ] MCP servers currently configured in settings.json (`mcpServers` key contents)

### opencode.md
- [x] Version, OMOA config, providers, opencode.db schema (from agent-control-plane notes)
- [ ] Deep pass: oh-my-openagent upstream repo and update procedure; profiles/ semantics;
      which providers are ACTIVE (not just available); prune stale .bak files decision
- [ ] Confirm opencode.db schema still matches (notes are from 2026-06-08, v1.17.12 now)

### kilo.md
- [ ] **BLOCKER: canonical root** — `.kilo` vs `.kilocode` (marker-file test), then retire the stale one
- [ ] Deep pass: what Kilo actually is on this machine (CLI vs VS Code extension), skills
      discovery, provider/model config, session storage (llm-archiver has kilo.yaml)

### copilot-cli.md
- [x] Version, config root, events.jsonl session format
- [ ] Deep pass: agents/ and hooks/ dirs semantics, MCP support, model selection,
      relationship to VS Code Copilot and `gh` auth

### goose.md
- [ ] Deep pass: everything — config file location on Windows (no config.yaml at default path),
      provider setup, extensions/MCP, session storage (llm-archiver has goose.yaml)

### qwen.md
- [ ] Is Qwen CLI still installed anywhere? (no command on PATH 2026-07-07, root has no chats)
- [ ] Decide: document properly or mark retired and stop tracking

### openrouter.md
- [x] Provider-not-app framing, opencode consumption, key hygiene
- [ ] Enumerate which tools COULD route through OpenRouter and which currently do
- [ ] Record the Doppler project/config that holds the OpenRouter key name (names only)

### Not yet covered at all
- [ ] `.continue` (Continue?) — root exists holding gws-* skills; in use or vestigial?
- [ ] `kimi` — llm-archiver has kimi.yaml but no reference file here; installed?
- [ ] VS Code itself as an agent host (Copilot Chat, extensions) — worth a reference file?
- [ ] `C:\Users\pmacl\.agents\skills` — document the shared-skills discovery contract per tool
      (which tools actually read it: verified list, not assumption)
