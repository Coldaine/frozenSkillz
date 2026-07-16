# Skill Review Tracker

> **Source of truth** for the skill quality gate. Most skills are held in `_incubator/`
> (de-registered from the marketplace) until they pass a review pass. Active marketplace
> skills are limited to reviewed, installable workflows.

**Established:** 2026-05-28
**Gate decision:** strict — `doppler` and `external-skill-intake` are active and on the
marketplace menu; older reference/workflow skills remain gated pending review.
**Holding location:** `_incubator/` (in-repo, easy to promote back; not installable).
**Linear:** planning lives in Linear — project **frozenSkillz** (under the *ClaudeReconfigurations*
initiative, team Moosegoose/MOO), parent intake [MOO-561](https://linear.app/moosegoose/issue/MOO-561)
+ one triage sub-issue per gated skill (MOO-562 … MOO-570). Also registered in Notion → Builder Lab →
Projects (per the documented "Issues live in Linear; design/projects live in Builder Lab" split).
This file stays the in-repo source of truth for required work; Linear tracks status. Keep them in sync.

---

## How this works

1. Gated skills live under `_incubator/` and are **not** listed in any marketplace catalog, so they cannot be installed.
2. Each skill below has a status and a list of required work. Take a pass at one, do the work, then **promote** it.
3. **Promote** = move the skill dir back to its plugin's `skills/` folder, re-add it to the relevant manifests
   (the three root marketplace catalogs + the plugin's own `plugin.json` / `gemini-extension.json` `skills[]` array),
   and bump the plugin version.
4. Update this tracker when status changes.
5. Scout snapshots live under `_incubator/scout/` until they are reconciled into the skill rows below or deleted.

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

| Skill | Tier | Linear | Status | Location | Required work |
|---|---|---|---|---|---|
| `doppler` | A | — (done) | ✅ **ACTIVE** (on menu) | `plugins/frozen-skills/skills/doppler` | None — reference standard. |
| `external-skill-intake` | A | — | ✅ **ACTIVE** (on menu) | `plugins/frozen-skills/skills/external-skill-intake` | Workflow for sandboxing, scoring, evaluating, and packaging external inspiration repos before promotion. |
| `plugin-authoring-guide` ("skill guide") | A | MOO-562 | 🛑 gated · **rework** | `_incubator/frozen-skills/skills/` | **Rework** (user directive). |
| `mcp-deployment-guide` ("MCP guide") | A | MOO-563 | 🛑 gated · **update** | `_incubator/frozen-skills/skills/` | **Update** (user directive). |
| `agent-config-megaref` | A | MOO-564 | 🛑 gated · **light update** | `_incubator/frozen-skills/skills/` | Light update **+ confer/cross-reference with the LLM archiver project** (user directive). |
| `setup-rules` | B | MOO-568 | 🛑 gated | `_incubator/frozen-rules/skills/` | Tiny fix + verify rule install flow. |
| `gh-common-workflows` | B | MOO-565 | 🛑 gated | `_incubator/frozen-skills/skills/` | De-opinionate (remove NORTH_STAR / Codex-specific assumptions); verify refs. |
| `stacked-pr-workflow` | B | MOO-566 | 🛑 gated | `_incubator/frozen-skills/skills/` | Run + verify the 7 PowerShell helpers; decide if niche is worth keeping. |
| `skill-manager` | B | MOO-567 | 🛑 gated | `_incubator/skill-manager/` | Verify scripts + registry assumptions (`skills.sh`, `~/.agents/skills`). |
| `session-skill-inferencer` | C | MOO-569 | 🛑 gated · **highest concern** | `_incubator/frozen-skills/skills/` | Fix generation quality before any promotion (see below). |
| `skill-injector` (was skill-classifier) | C | MOO-570 | 🧪 **registered · experimental/UNTESTED** | `plugins/skill-injector/` | Test end-to-end before enabling; finish internal rename (scripts/module + ADR/doc prose still say "classifier"). |

Legend: ✅ active · 🛑 gated (in `_incubator/`) · 🧪 inert/experimental · Tier A = strong reference, B = functional/narrow, C = rework.

---

## Scout intake

| Intake | Status | Location | Required work |
|---|---|---|---|
| `coldaine-infra/skills/frozen` submodule snapshot (`c2868ee2c0b49eaecdbd365bc00ffec0685487fe`) | scout · incubated | `_incubator/scout/2026-06-16-coldaine-infra-skills-frozen-submodule/` | Compare against current `_incubator/` and `plugins/skill-injector/`; frozen-rules + `gh-common-workflows` matched current incubator files in the 2026-06-16 audit, but `agent-config-megaref`, `mcp-deployment-guide`, `plugin-authoring-guide`, and old `skill-classifier` hook/script/test files have deltas that need review before promotion or deletion. |

---

## Per-skill notes

### `doppler` — ACTIVE
Security-first reference skill: lean `SKILL.md` (rules + intent table + workflow), progressive
`references/` (setup, commands, CI/fallbacks), gated `references/homelab-notes.md` for coldaine/ESO/Shipwright
only, and `evals/triggers.json` for description routing checks. Synced from
`C:\Users\pmacl\.agents\skills\doppler` on 2026-07-16 to match the promotion bar (WHAT/WHEN description,
no project diary in the body, progressive disclosure).
Use it as the quality bar for everything else.

### `external-skill-intake` — ACTIVE
Required workflow for evaluating external skill/plugin/agent repos. It keeps source snapshots read-only under
`_incubator/scout/`, requires inventory, artifact rubrics, live eval evidence, and a packaging decision before any
candidate idea moves into active marketplace content.

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

### `skill-injector` (renamed from `skill-classifier`) — registered, experimental/UNTESTED
- Built by a parallel session and merged to `main` (PRs #22/#23): two hooks sharing a swappable LLM backend
  (Ollama default, Gemini CLI fallback) — a `UserPromptSubmit` hook that injects a relevant-skill suggestion, and a
  `PreToolUse` (Agent/Task) hook that injects advisory feedback on subagent prompts.
- **Renamed 2026-05-28:** the plugin directory, the skill folder, and all four plugin manifests are now
  `skill-injector`. Re-registered in all four marketplace catalogs, flagged `experimental` / UNTESTED.
- **Still NOT installed or enabled** anywhere (`~/.claude/settings.json`, `~/.claude.json`, this repo — no
  `enabledPlugins`). The hooks do **not** run; it is dormant code until someone installs + enables the plugin.
- **TODO before relying on it:** test end-to-end; then finish the rename internally — the Python scripts/module
  (`skill_classifier.py`), the env vars (`SKILL_CLASSIFIER_*`), the ADRs, and the SKILL.md/README prose still say
  "classifier". Left as-is for now to avoid breaking the untested hook wiring.

---

## Loose ends to reconcile when promoting

- **`mcp/` templates** (`mcp/github.json`, `mcp/notebooklm.json`) left at repo root; `mcp-deployment-guide` references them.
- **`docs/stacked-pr-workflow/`** supplementary docs left in place for the gated `stacked-pr-workflow` skill.
- **Root `README.md`** and **`CLAUDE.md`** still describe the pre-gate lineup and the old `skill-classifier` name —
  update them (and the plugin's own README + ADRs) to `skill-injector`, and point them here, once the gate is settled.

---

## Personal skills intake (2026-07-06)

Reference copies of the user's own `~/.agents/skills` personal skills, brought in so frozenSkillz owns a copy for
evaluation (the "own a reference copy of all my skills" directive). **Held in `_incubator/personal-skills/` — gated,
not installable, in no manifest.** Deliberately separate from the marketplace-candidate gated skills above.

**Rewrite rule:** live edit in `~/.agents/skills/<name>/`, then mirror into `_incubator/personal-skills/<name>/`, update this
tracker row, and **commit + push in frozenSkillz the same session**. Opening an Issue is not enough. “Gated” means not
marketplace-promoted — not “leave uncommitted.” Full contract: `docs/workflows/skill-authority-and-frozen-sync.md`.

**Excluded on purpose:**
- `deepinit` — ships in the OMC package (`oh-my-claude-sisyphus/skills`); an *installed plugin* skill, not authored here. Not intake material.
- `doppler` — already **ACTIVE** in `plugins/frozen-skills/skills/`.

**Drift found during intake (fix separately):**
- `edit-opencode-config` lived only in `~/.claude/skills/` (real dir, not a `.agents` junction) — missing from the canonical `~/.agents/skills` root. Copied here from `.claude`.
- `~/.claude/skills/omc-learned/` holds learner notes (`edit-opencode-config.md`, `phantom-substrate-inheritance.md`) — a half-promoted staging area to reconcile.

| Skill | Provenance | Status | Work before promotion |
|---|---|---|---|
| `chat-history` | authored (hardened 2026-07-06) | 🛑 gated | De-personalize (paths, Pieces, UTC-5); run `artifact_hunt.py` / `extract_chat_history.py`. |
| `retrospective` | authored (`author: pmacl`) | 🛑 gated | De-personalize (agent-control-plane paths); run `session_timeline.py`. |
| `project-docs` | authored (rewritten 2026-07-16; [#37](https://github.com/Coldaine/frozenSkillz/issues/37)) | 🛑 gated · evaluate | Live + incubator synced: kill PROGRESS/`docs/history` defaults; Issues/plans + promote-then-delete; AGENTS router; CLAUDE→AGENTS; restored `SKILL.md`. Still gated — do not marketplace-promote until promotion bar + de-personalization pass. |
| `skill-install` | authored | 🛑 gated | Verify recipes/paths. |
| `run-opencode` | authored | 🛑 gated | Verify commands. |
| `edit-opencode-config` | authored (was `.claude`-only) | 🛑 gated | Fix canonical-root drift; verify. |
| `phantom-substrate-inheritance` | authored | 🛑 gated | Review. |
| `review-claudemd` | authored | 🛑 gated | Review; overlap-check vs `claude-md-enhancer`. |
| `rich-visual-responses` | authored | 🛑 gated | Review. |
| `insight-extractor` | authored | 🛑 gated · **needs fix** | **No YAML frontmatter** (add `name`/`description`); **self-contradictory paths** — `skill.md` uses `~/.Codex/…`, `skill.yaml` uses `~/.claude/…` (pick one canonical). |
| `claude-md-enhancer` | **provenance unconfirmed** | 🛑 gated · confirm origin | Confirm authored vs downloaded; overlap-check vs `review-claudemd`. |
| `nlm-skill` | **provenance unconfirmed** | 🛑 gated · confirm origin | Confirm authored vs downloaded. |
| `skill-finder` | **provenance unconfirmed** | 🛑 gated · confirm origin | Confirm authored vs downloaded. |
| `context7-mcp` | **provenance unconfirmed** | 🛑 gated · thin/redundant? | Likely overlaps global `~/.claude/rules/context7.md` — decide keep/drop. |
| `google-stitch-ui-designer` | **provenance unconfirmed** | 🛑 gated · confirm origin | External-tool guide; confirm authored vs downloaded. |

Next pass: confirm provenance on the 5 unconfirmed, fix `insight-extractor` frontmatter, then decide which earn promotion toward active (each needs de-personalization + manifest entries + version bump per the promotion bar).

### PR #35 review findings (routed 2026-07-06)

Automated review of the intake PR — **Kilo 13 + Copilot 7, all WARNING (0 critical)**. These are gated reference copies = faithful snapshots of the live `~/.agents/skills` source, so fixes land in the **live source and re-sync at promotion**, not in the frozen snapshot. Routed here as promotion-work:

**Expected — de-personalization (the headline promotion gate):**
- `chat-history/SKILL.md` L43/L61/L214 (`D:\_projects`), L68 (`C:\Users\pmacl`).
- `retrospective/SKILL.md` L81 (`pmacl`), L132/L278 (`D:\_projects`).
- `edit-opencode-config/SKILL.md` L31 (`pmacl`).

**Genuine bugs to fix in the LIVE source, then re-sync:**
- `chat-history/extract-chats.sh` L59 — `while read` missing `-r` (backslash corruption). *Real bug.*
- `chat-history/extract_chat_history.py` L15 — docstring lists a `gemini` extractor that isn't implemented; implement or drop.
- `insight-extractor` — no YAML frontmatter; self-contradictory paths (`~/.Codex` vs `~/.claude`) at L7/L43/L55.
- `review-claudemd/SKILL.md` L4 — frontmatter `name` ≠ dir name (breaks discovery/dedupe); L15 — duplicate `-name "AGENTS.md"` in the `find` example.
- `run-opencode/driver.mjs` L8 — header says all-but-`backup` is read-only, but `profile` also writes `oh-my-openagent.json[c]`; fix the comment.

These do not block the *intake* (faithful capture); they are the evaluation TODO that must clear before any skill here is promoted to active.
