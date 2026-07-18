# frozenSkillz

Cross-platform agent skills, rules, and plugin metadata for reusable agent workflows.

`frozenSkillz` is the reviewed source repository and marketplace. `frozen-skills` is the active distribution inside it. The four aligned plugin manifests define the distribution: only their entries under `plugins/frozen-skills/skills/` are synchronized or packaged. Content under `_incubator/` is stored for review and is never installed.

This repository is not a dumping ground for local client caches, raw external repos, or unreviewed experimental skill copies.

## Plugins

| Plugin | Category | Status | Purpose |
|---|---|---|---|
| `frozen-skills` | reference | active | Installable package for reviewed skills. Installs `doppler`, `external-skill-intake`, `omc-reference`, and `pdm-cli-operations`. |
| `skill-injector` | development | experimental, untested | UserPromptSubmit hook and subagent prompt quality gate for LLM-assisted skill suggestions. Review/test before enabling. |

Historical reference/workflow skills remain gated in `_incubator/` until they pass the quality bar in `docs/skill-review/tracker.md`.

## Synchronize a Computer

Clone or update this repository on each computer, then run the cross-platform synchronizer:

```powershell
python scripts/sync_frozen_skills.py --check
python scripts/sync_frozen_skills.py --apply
```

The default destination is `~/.agents/skills`, the shared personal skill root used by Codex and other clients that discover Agent Skills. The synchronizer:

- validates that the Claude, Codex, Cursor, and Gemini manifests have the same version and active skill list;
- installs or updates only those manifest-listed skills;
- leaves unrelated personal skills alone;
- records managed content in `~/.agents/skills/.frozen-skills-sync.json`;
- refuses to overwrite an unmanaged or locally modified destination skill.

Use `--destination <path>` for another local skill root. Use `--prune` to remove unchanged, previously managed skills that have left the active manifests. `--force` overwrites local conflicts and should be used only after reviewing the reported plan.

The destination must be disjoint from the repository: it cannot be inside the frozenSkillz checkout or contain that checkout. This enforces outward-only deployment and prevents reverse synchronization into reviewed source.

After pulling a new revision on any computer, `--check` exits nonzero when that computer needs synchronization; `--apply` converges it to the reviewed distribution.

## Deployment Profiles

Files under `profiles/*.json` define named deployment subsets of the same manifest-approved active distribution. A profile can select active skills; it cannot activate `_incubator/` content or bypass the four-manifest agreement.

Profile synchronization requires a dedicated explicit destination and `--prune` for both planning and application:

```powershell
python scripts/sync_frozen_skills.py --check --profile hermes-ops --destination /srv/hermes/skill-sets/hermes-ops --prune
python scripts/sync_frozen_skills.py --apply --profile hermes-ops --destination /srv/hermes/skill-sets/hermes-ops --prune
```

The management record binds a destination to either the full distribution or one named profile. The synchronizer refuses to reuse that destination for another owner and treats any unmanaged top-level content in a profile destination as a conflict; use a fresh dedicated destination instead. Profile synchronization materializes an exact managed subset in a directory. It is not a native Hermes skill bundle and does not configure a consumer's mounts, skill search path, or reload behavior.

## Client-managed Plugin Install

Claude Code can instead let its marketplace manage a client-specific plugin copy:

```bash
/plugin marketplace add Coldaine/frozenSkillz
/plugin install frozen-skills@coldaine-skills
```

That command installs the same four manifest-listed skills into Claude Code's plugin-managed location. It does not populate `~/.agents/skills` and does not install anything from `_incubator/`.

The Codex, Cursor, and Gemini manifests are packaging metadata and a consistency contract. Their presence alone is not an installer. Use `sync_frozen_skills.py` for a verified local installation unless a specific client provides and documents its own plugin installer.

## Active Skills

`frozen-skills` currently registers:

- `doppler`: Doppler CLI and secret-injection workflow guidance that avoids exposing secret values.
- `external-skill-intake`: sandbox, inventory, score, evaluate, and package external skill/plugin/agent repos before any promotion.
- `omc-reference`: maintain Oh My ClaudeCode as a separate Claude Code plugin from Codex without importing OMC workflow rules into ordinary Codex work.
- `pdm-cli-operations`: inspect and operate Proxmox fleets through the official PDM client, with exact target selection and terminal task proof for mutations.

## External Skill Intake

Do not import external repositories directly into `plugins/`. Evaluate them through:

- `plugins/frozen-skills/skills/external-skill-intake/SKILL.md`
- `docs/workflows/external-skill-intake.md`
- `_incubator/scout/<YYYY-MM-DD>-<repo>/`

Candidate source stays read-only under `source/`; mined ideas go to scout analysis files, eval runs, decision logs, and adapted frozenSkillz-owned paths only after review.

## Repository Layout

```text
.claude-plugin/                  Claude Code marketplace catalog
.codex-plugin/                   Codex-facing marketplace metadata
.cursor-plugin/                  Cursor-facing marketplace metadata
gemini-marketplace.json          Gemini-facing marketplace metadata
plugins/
  frozen-skills/                 Active installable skill plugin
  skill-injector/                Experimental hook plugin
scripts/
  sync_frozen_skills.py          Manifest-driven local synchronizer
_incubator/                      Gated skills and scout snapshots
docs/
  skill-review/                  Quality gate and tracker
  workflows/                     Long-form workflows
```

For the source-to-computer authority model and synchronization process, see
`docs/workflows/skill-authority-and-frozen-sync.md`.

## Validation

This repo does not use a single package manager. Validate the touched surface directly:

```powershell
# JSON manifests
Get-Content .claude-plugin/marketplace.json -Raw | ConvertFrom-Json | Out-Null
Get-Content .codex-plugin/marketplace.json -Raw | ConvertFrom-Json | Out-Null
Get-Content .cursor-plugin/marketplace.json -Raw | ConvertFrom-Json | Out-Null
Get-Content gemini-marketplace.json -Raw | ConvertFrom-Json | Out-Null
Get-Content plugins/frozen-skills/.claude-plugin/plugin.json -Raw | ConvertFrom-Json | Out-Null
Get-Content plugins/frozen-skills/.codex-plugin/plugin.json -Raw | ConvertFrom-Json | Out-Null
Get-Content plugins/frozen-skills/.cursor-plugin/plugin.json -Raw | ConvertFrom-Json | Out-Null
Get-Content plugins/frozen-skills/gemini-extension.json -Raw | ConvertFrom-Json | Out-Null

# Repo checks
python -m pip install -r requirements-validation.txt
python scripts/validate_manifests.py
python scripts/validate_skills.py
python -m unittest discover -s tests -v
git diff --check
```

For skill additions, verify every manifest `skills[].path` exists under the plugin directory.

## Contribution Rules

- Add shared active skills under `plugins/frozen-skills/skills/<name>/SKILL.md` only after passing the review gate.
- Treat `plugins/frozen-skills/skills` as the source for active distributed skills. Make reviewed changes here, then synchronize them outward to local computers.
- Treat managed copies under `~/.agents/skills` as runtime outputs. Do not silently copy local edits back into the reviewed source.
- Keep external scout snapshots under `_incubator/scout/` and never edit scout `source/` after import.
- Keep plugin manifests and marketplace versions aligned when adding public skills.
- Do not commit secret values, client runtime caches, or local installed-skill copies.
