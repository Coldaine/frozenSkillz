# frozenSkillz

Cross-platform agent skills, rules, and plugin metadata for reusable agent workflows.

Agents should read `AGENTS.md` first. Humans can use this file as the quickstart.

## Quickstart

Synchronize the reviewed distribution into the computer's shared skill root:

```powershell
python scripts/sync_frozen_skills.py --check
python scripts/sync_frozen_skills.py --apply
```

Claude Code can alternatively install a plugin-managed copy:

```bash
/plugin marketplace add Coldaine/frozenSkillz
/plugin install frozen-skills@coldaine-skills
```

The marketplace command does not populate `~/.agents/skills`. Cross-platform manifests are packaging metadata; use the synchronizer for a verified local copy.

## Active Plugin

| Plugin | Status | Purpose |
|---|---|---|
| `frozen-skills` | active | Installable package containing the manifest-listed reviewed skills. `_incubator/` content is not installed. |
| `skill-injector` | experimental, untested | Prompt hook and subagent prompt quality gate. Review before enabling. |

## Active Skills

- `doppler`: Doppler CLI and secret-injection workflows with strict secret hygiene.
- `external-skill-intake`: Sandbox, evaluate, and package external skill/plugin/agent repos.
- `omc-reference`: Configure and troubleshoot the separate Oh My ClaudeCode installation without applying OMC workflow rules to ordinary Codex work.

Most historical reference skills are gated in `_incubator/` until they pass the review bar in `docs/skill-review/tracker.md`.

## External Skill Intake

Use `external-skill-intake` and `docs/workflows/external-skill-intake.md` before bringing in outside repos. Do not import external repositories directly into `plugins/`.

## Validation

```powershell
Get-Content .claude-plugin/marketplace.json -Raw | ConvertFrom-Json | Out-Null
Get-Content plugins/frozen-skills/.claude-plugin/plugin.json -Raw | ConvertFrom-Json | Out-Null
python -m pip install -r requirements-validation.txt
python scripts/validate_manifests.py
python scripts/validate_skills.py
python -m unittest discover -s tests -v
git diff --check
```

## Repository Map

```text
plugins/frozen-skills/       Active installable skill plugin
plugins/skill-injector/      Experimental hook plugin
scripts/sync_frozen_skills.py Manifest-driven local synchronizer
_incubator/                  Gated skills and scout snapshots
AGENTS.md                    Agent router and operating contract
```
