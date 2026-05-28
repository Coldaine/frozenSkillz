# Skill Review Tracker

> **Source of truth** for the skill quality gate. Most skills are held in `_incubator/`
> (de-registered from the marketplace) until they pass a review pass. Only the **Doppler**
> skill is currently active and promoted. `skill-classifier` ships separately as **experimental**.

**Established:** 2026-05-28
**Gate decision:** strict — only `doppler` active; every other reference/workflow skill is gated pending review.
**Holding location:** `_incubator/` (in-repo, easy to promote back; not installable).

---

## How this works

1. Gated skills live under `_incubator/` and are **not** listed in any marketplace catalog, so they cannot be installed.
2. Each skill below has a status and a list of required work. Take a pass at one, do the work, then **promote** it.
3. **Promote** = move the skill dir back to its plugin's `skills/` folder, re-add it to the four manifests
   (`.claude-plugin`/`.codex-plugin`/`.cursor-plugin` marketplace catalogs as needed, plus the plugin's own
   `plugin.json` / `gemini-extension.json` `skills[]` array), and bump the plugin version.
4. Update this tracker when status changes.

### Promotion bar ("ready")
A skill may be promoted when it meets the bar set by `doppler` (the reference standard):

- [ ] Description: clear trigger + when-to-use; under ~300 chars; negative triggers where useful.
- [ ] Content is current and factually verified (paths, commands, flags actually exist).
- [ ] Cross-platform where it matters (PowerShell + POSIX).
- [ ] Any referenced `scripts/` have been **run** and work (existence ≠ correctness).
- [ ] No project-specific or opinionated assumptions leaking into a "universal" skill.
- [ ] Progressive disclosure: heavy detail in `references/`, SKILL.md stays lean.

---

## Status board

| Skill | Tier | Status | Location | Required work |
|---|---|---|---|---|
| `doppler` | A | ✅ **ACTIVE** | `plugins/frozen-skills/skills/doppler` | None — reference standard. |
| `plugin-authoring-guide` ("skill guide") | A | 🛑 gated · **rework** | `_incubator/frozen-skills/skills/` | **Rework** (user directive). |
| `mcp-deployment-guide` ("MCP guide") | A | 🛑 gated · **update** | `_incubator/frozen-skills/skills/` | **Update** (user directive). |
| `agent-config-megaref` | A | 🛑 gated · **light update** | `_incubator/frozen-skills/skills/` | Light update **+ confer/cross-reference with the LLM archiver project** (user directive). |
| `setup-rules` | B | 🛑 gated | `_incubator/frozen-rules/skills/` | Tiny fix + verify rule install flow. |
| `gh-common-workflows` | B | 🛑 gated | `_incubator/frozen-skills/skills/` | De-opinionate (remove NORTH_STAR / Codex-specific assumptions); verify refs. |
| `stacked-pr-workflow` | B | 🛑 gated | `_incubator/frozen-skills/skills/` | Run + verify the 7 PowerShell helpers; decide if niche is worth keeping. |
| `skill-manager` | B | 🛑 gated | `_incubator/skill-manager/` | Verify scripts + registry assumptions (`skills.sh`, `~/.agents/skills`). |
| `session-skill-inferencer` | C | 🛑 gated · **highest concern** | `_incubator/frozen-skills/skills/` | Fix generation quality before any promotion (see below). |
| `skill-classifier` | C | 🧪 experimental (registered) | `plugins/skill-classifier/` | Not gated — actively being refactored (swappable backend). Re-review after that lands. |

Legend: ✅ active · 🛑 gated (in `_incubator/`) · 🧪 experimental · Tier A = strong reference, B = functional/narrow, C = rework.

---

## Per-skill notes

### `doppler` — ACTIVE
Best skill in the repo: security-first, cross-platform, names-only diagnostics, complete `references/` + `agents/`.
Use it as the quality bar for everything else.

### `plugin-authoring-guide` ("skill guide") — REWORK
- **User directive:** needs to be reworked.
- Currently comprehensive (11.6kb) and structurally fine, but rework per user. Re-verify every claim against
  current Claude Code plugin/skill docs (frontmatter fields, invocation controls, hook events) — the platform moves fast.

### `mcp-deployment-guide` ("MCP guide") — UPDATE
- **User directive:** probably needs updating.
- Re-verify config-file locations and env-var substitution syntax per tool; confirm the `mcp/` templates
  (`github.json`, `notebooklm.json`, left at repo root) are still accurate.

### `agent-config-megaref` — LIGHT UPDATE + ARCHIVER CROSS-REFERENCE
- **User directive:** needs a little updating, **and must confer / cross-reference with the LLM archiver project**
  (`D:\_projects\llm-archiver`) because they hold some of the same information.
- The overlap is the **per-tool file-path knowledge** (where each agent tool stores config / sessions). The archiver
  is the canonical source for tool coverage and on-disk locations — reconcile this skill's platform maps against it so
  the two don't drift. See `D:\_projects\llm-archiver\docs\CONSUMERS.md` and `schema\base.sql`.

### `setup-rules` — small fix
- Remove the uncertain `claude rules list   # (if such a command exists)` line; verify the actual rules-load behavior.
- Small installer for the 3 templates in `_incubator/frozen-rules/rules/` (all present).

### `gh-common-workflows` — de-opinionate
- Bakes in project-specific assumptions ("NORTH_STAR alignment", "canonical scope docs") and Codex-specific framing.
- Make it genuinely universal or scope it down honestly. References present and intact.

### `stacked-pr-workflow` — verify scripts
- Complete (4 workflow docs + 7 PowerShell helpers + graphite maps; supplementary docs in `docs/stacked-pr-workflow/`).
- "Files exist" was verified; **script correctness was not**. Run each `.ps1` before promoting. Decide whether this
  niche workflow earns a slot.

### `skill-manager` — verify scripts + assumptions
- Full `instructions/` + `scripts/` + `templates/` present. Depends on the `skills.sh` registry and assumptions like
  `~/.agents/skills/` (Kimi). Run the scripts and confirm the registry/path assumptions hold.

### `session-skill-inferencer` — highest concern, fix generation quality
- **This skill produced the 5 junk auto-generated skill dirs that were deleted from the repo root on 2026-05-28**
  (e.g. `gemma-35b-mtp-locallargelanguagemodels/`). Names were garbage; bodies were raw chat fragments.
- Structurally fine and self-documenting, but its *output* is the slop the gate exists to stop. Do **not** promote
  until the generation prompts produce clean, well-named, genuinely useful skills. See
  `docs/skill-review/session-skill-inferencer-changes.md` for prior refactor rationale.

### `skill-classifier` — experimental, not gated
- Left registered as experimental and **physically in place** (`plugins/skill-classifier/`) because it has active
  uncommitted refactor work on branch `feat/skill-classifier-swappable-backend` (swappable Ollama/Gemini backend +
  subagent-prompt quality gate). Gating it would stomp in-flight work. Re-review once that refactor lands.

---

## Loose ends to reconcile when promoting

- **`mcp/` templates** (`mcp/github.json`, `mcp/notebooklm.json`) left at repo root; `mcp-deployment-guide` references them.
- **`docs/stacked-pr-workflow/`** supplementary docs left in place for the gated `stacked-pr-workflow` skill.
- **codex/cursor catalogs** still carry a stale `skill-classifier` v0.1.0 entry (claude catalog is v0.3.0); sync when the
  classifier refactor lands.
- **Root `README.md`** and **`CLAUDE.md`** still describe the pre-gate skill lineup — update them to point here once the
  gate is settled.
