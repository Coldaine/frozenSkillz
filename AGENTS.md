# AGENTS.md — frozenSkillz Agent Workflows

This is the agent-facing instruction file. Read `CLAUDE.md` for the human-facing quickstart.

## Repository Purpose

Cross-platform agent skill marketplace and quality gate. Skills, rules, and agent workflows that work across Claude Code, Codex, Cursor, Gemini, and Kilo. This repo is the **skill registry**, not a junk drawer — every skill is either active (on the marketplace menu), gated (in `_incubator/` pending review), or experimental (registered but inert).

## Directory Map

```
frozenSkillz/
├── plugins/                        ACTIVE marketplace content
│   ├── frozen-skills/skills/       Active skills (currently only doppler)
│   ├── frozen-rules/               Active rule templates
│   └── skill-injector/             Experimental, inert hooks (replaces old skill-classifier)
├── _incubator/                     GATED — not in marketplace catalogs
│   ├── frozen-rules/               Rules pending review
│   ├── frozen-skills/skills/       Skills pending rework/update
│   ├── skill-manager/              Dry-run skill state manager
│   └── scout/                      Snapshot intake from external repos
├── docs/
│   ├── skill-corpus-analysis/      Intake rubric + analysis template
│   ├── skill-review/               Tracker + per-skill notes
│   └── stacked-pr-workflow/        Supplementary docs for stacked-pr skill
├── .claude-plugin/                 Claude Code marketplace catalog
├── .codex-plugin/                  Codex marketplace catalog
├── .cursor-plugin/                 Cursor marketplace catalog
├── gemini-marketplace.json         Gemini marketplace catalog
└── mcp/                            MCP server config templates
```

## Skill Lifecycle States

| State | Location | In Marketplace? | Installable? |
|---|---|---|---|
| **ACTIVE** | `plugins/` | Yes | Yes |
| **GATED** | `_incubator/` | No | No |
| **SCOUT** | `_incubator/scout/` | No | No |
| **EXPERIMENTAL** | `plugins/skill-injector/` | Yes, flagged | No (hooks not enabled) |

## Workflow 1: Scout Intake (External Skill Evaluation)

This is the **primary workflow** for evaluating skills from external repos. Do NOT blindly copy external skills into this repo. Every external skill must pass the intake rubric before it can be promoted to `_incubator/` or `plugins/`.

### Phase 1: Snapshot

1. Clone or fetch the external repo.
2. Capture the **commit hash** and **repo URL**.
3. Copy the repo contents into `_incubator/scout/<YYYY-MM-DD>-<short-name>/source/`.
4. Create a `README.md` in the scout directory with:
   - Source repo URL
   - Source commit hash
   - Import date
   - Destination path
   - Note: "This is an incubated scout snapshot. Do not promote without review."

Example: `_incubator/scout/2026-06-16-coldaine-infra-skills-frozen-submodule/README.md`

### Phase 2: Intake — Apply the Corpus Intake Rubric

For each candidate skill/artifact in the snapshot, verify all admission rules from `docs/skill-corpus-analysis/corpus-intake-rubric.md`:

1. **Structure check**: Full skill directory exists with original structure preserved. If the external repo is NOT a skill repo (e.g., it's a plugin with agents, not SKILL.md files), classify each artifact by type (agent, config, validator, etc.) rather than forcing the skill rubric.

2. **Read everything**: Every file that affects behavior must be read — `SKILL.md`, `references/**`, `scripts/**`, `templates/**`, `AGENTS.md`, metadata, tests.

3. **Provenance captured**: For each artifact, record:
   - `skill_name` (or artifact_name)
   - `local_path`
   - `source_tier` (Tier 1 = official/org, Tier 2 = community/common, Tier 3 = individual/niche, Tier 4 = unknown)
   - `source_repo_url`
   - `source_repo_path`
   - `commit_hash`
   - `author_org_or_owner`
   - `license`
   - `date_last_updated`
   - `retrieval_date`
   - `notes_on_access_method`

4. **Security screen**: Inspect every artifact for:
   - Prompt-injection instructions (exfiltration, policy bypass)
   - Suspicious network calls or hidden downloads in scripts
   - Instructions to transmit secrets, credentials, tokens, local files
   - Destructive shell behavior without safeguards
   - Unclear script inputs/outputs that conceal side effects
   - Disposition: `clear`, `review-needed`, or `excluded-security`

5. **Design-pattern classification** (for actual skills):
   - Primary tag: `tool-wrapper`, `generator`, `reviewer`, `inversion`, `pipeline`, `uncategorized`
   - Apply `composite` when 2+ patterns materially shape the skill
   - Every pattern tag must cite at least one file path as evidence

6. **Exclusion**: If any admission rule fails, log the skill as `blocked` or `excluded` with one of:
   - `unread-source`, `listing-only`, `missing-structure`, `blocked-security`, `thin-wrapper-low-value`, `duplicate`

### Phase 3: Analysis — Score and Classify

For every admitted skill, produce an analysis row with:

| Field | Values |
|---|---|
| Primary Pattern | tool-wrapper / pipeline / generator / reviewer / inversion |
| Secondary Pattern | Optional, comma-separated |
| Disclosure (1-5) | How well the skill declares what it does and when to use it |
| Description (1-5) | Quality of activation triggers, negative triggers, clarity |
| Structure (1-5) | Progressive disclosure: SKILL.md as router vs. monolithic blob |
| Gates (1-5) | For pipelines: quality of phase gates and enforcement language. N/A for non-pipeline skills. |
| Quality Tier | Exemplar / Strong / Adequate / Weak / Anti-pattern |
| Notable Feature | One sentence on what is notably strong, weak, or distinctive |

Reference the existing corpus analysis at `docs/skill-corpus-analysis/corpus-analysis-deliverables.md` for the standard of quality expected.

### Phase 4: Compare Against Existing Skills

For each candidate skill, check whether frozenSkillz already has an equivalent:

1. Search `plugins/frozen-skills/skills/` and `_incubator/frozen-skills/skills/` for overlapping skills.
2. Read the existing skill's SKILL.md and compare:
   - Coverage: Does one cover more ground?
   - Structure: Is one more progressively disclosed?
   - Quality: Which scores higher on the rubric?
   - Maintenance: Which is more current?
3. Decision options:
   - **Replace**: Candidate is strictly better → replace existing, archive old
   - **Merge**: Both have useful content → merge into one improved skill
   - **Keep existing**: Existing is better or equivalent → discard candidate
   - **New addition**: No overlap → candidate fills a gap

### Phase 5: Promote or Discard

If promoting a skill:

1. Move it from `_incubator/scout/` to the appropriate `_incubator/<plugin>/skills/` or directly to `plugins/<plugin>/skills/` if it meets the promotion bar.
2. Add it to ALL marketplace manifests:
   - `plugins/<plugin>/.claude-plugin/plugin.json` → `skills[]`
   - `plugins/<plugin>/.codex-plugin/plugin.json` → `skills[]`
   - `plugins/<plugin>/.cursor-plugin/plugin.json` → `skills[]`
   - `plugins/<plugin>/gemini-extension.json` → `skills[]`
3. Bump the plugin version.
4. Update the root marketplace catalogs if the plugin is new:
   - `.claude-plugin/marketplace.json`
   - `.codex-plugin/marketplace.json`
   - `.cursor-plugin/marketplace.json`
   - `gemini-marketplace.json`

If discarding:
- Leave the scout snapshot in place (it documents what was evaluated and why).
- Add an entry to the tracker or a rejection note in the scout README.

### Phase 6: Update Tracker

Update `docs/skill-review/tracker.md`:
- Add a row for the new skill with status, tier, Linear issue, location, and required work.
- Remove any scout entries that have been fully reconciled.

---

## Promotion Bar (from `docs/skill-review/tracker.md`)

A skill may be promoted from `_incubator/` to `plugins/` when it meets the bar set by the `doppler` skill:

- [ ] **Description**: Clear trigger + when-to-use; under ~300 chars; negative triggers where useful
- [ ] **Content current**: Paths, commands, flags actually exist and are verified
- [ ] **Cross-platform**: PowerShell + POSIX where it matters
- [ ] **Scripts verified**: Any referenced `scripts/` have been RUN and work
- [ ] **No opinion leakage**: No project-specific assumptions in a "universal" skill
- [ ] **Progressive disclosure**: Heavy detail in `references/`, SKILL.md stays lean (< ~150 lines)

---

## Quality Reference Standard: `doppler`

`plugins/frozen-skills/skills/doppler/SKILL.md` is the best skill in the repo and the quality bar for all others:
- Security-first approach
- Cross-platform (PowerShell + POSIX)
- Names-only diagnostics (never exposes secret values)
- Complete `references/` + `agents/` directories
- Lean SKILL.md that routes to detail on demand

Use `doppler` as the A/B comparison target when evaluating any candidate skill.

---

## Quick Reference: Common Operations

### Auditing the skill portfolio
```powershell
powershell -NoProfile -File plugins\skill-manager\scripts\skills-state.ps1 inventory
powershell -NoProfile -File plugins\skill-manager\scripts\skills-state.ps1 plan
powershell -NoProfile -File plugins\skill-manager\scripts\skills-audit.ps1
```

### Validating manifests
```powershell
Get-Content .claude-plugin\marketplace.json -Raw | ConvertFrom-Json | Out-Null
Get-Content plugins\frozen-skills\.claude-plugin\plugin.json -Raw | ConvertFrom-Json | Out-Null
python scripts\validate_manifests.py
```

### Promoting a gated skill
1. Move from `_incubator/<plugin>/skills/<name>/` to `plugins/<plugin>/skills/<name>/`
2. Add to ALL 4 plugin manifests (`skills[]` array)
3. Bump plugin version
4. Update `docs/skill-review/tracker.md`
5. Validate manifests
6. Commit

### Scouting an external repo
1. Clone/fetch, capture commit hash
2. Copy to `_incubator/scout/<YYYY-MM-DD>-<name>/source/`
3. Write scout `README.md` with provenance
4. Run intake rubric on every skill/artifact
5. Write analysis to `_incubator/scout/<YYYY-MM-DD>-<name>/analysis.md`
6. Compare against existing skills
7. Promote, merge, or discard each artifact
8. Update tracker

---

## Repair Notes

- `skill-classifier` was renamed to `skill-injector` in May 2026. Code and docs may still reference the old name.
- `session-skill-inferencer` produced junk output in May 2026 and is gated until generation prompts are fixed.
- `_incubator/` was created in May 2026 during the quality gate implementation. Most skills were moved there from `plugins/`.
- The `doppler` skill is the only ACTIVE skill. All others are gated pending review.
- Scout snapshots are for evaluation only. Never promote files from `_incubator/scout/` without running the full intake workflow.

## Related Docs

- `docs/skill-corpus-analysis/corpus-intake-rubric.md` — Full admission rubric
- `docs/skill-corpus-analysis/corpus-analysis-deliverables.md` — Example analysis of Tier 1 skills
- `docs/skill-review/tracker.md` — Skill status board (source of truth)
- `docs/skill-review/session-skill-inferencer-changes.md` — Refactoring rationale
- `docs/branch-prune-sprint-2026-05-27.md` — Historical cleanup outcomes
