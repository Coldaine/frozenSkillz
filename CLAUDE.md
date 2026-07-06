# frozenSkillz

Cross-platform agent skills, rules, and plugin metadata for reusable agent workflows.

Agents should read `AGENTS.md` first. Humans can use this file as the quickstart.

## Quickstart

```bash
/plugin marketplace add Coldaine/frozenSkillz
/plugin install frozen-skills@coldaine-skills
```

## Active Plugin

| Plugin | Status | Purpose |
|---|---|---|
| `frozen-skills` | active | Installable skills that passed the quality gate. |
| `skill-injector` | experimental, untested | Prompt hook and subagent prompt quality gate. Review before enabling. |

## Active Skills

- `doppler`: Doppler CLI and secret-injection workflows with strict secret hygiene.
- `external-skill-intake`: Sandbox, evaluate, and package external skill/plugin/agent repos.

Most historical reference skills are gated in `_incubator/` until they pass the review bar in `docs/skill-review/tracker.md`.

## External Skill Intake

Use `external-skill-intake` and `docs/workflows/external-skill-intake.md` before bringing in outside repos. Do not import external repositories directly into `plugins/`.

## Validation

```powershell
Get-Content .claude-plugin/marketplace.json -Raw | ConvertFrom-Json | Out-Null
Get-Content plugins/frozen-skills/.claude-plugin/plugin.json -Raw | ConvertFrom-Json | Out-Null
python scripts/validate_manifests.py
git diff --check
```

## Repository Map

```text
plugins/frozen-skills/       Active installable skill plugin
plugins/skill-injector/      Experimental hook plugin
_incubator/                  Gated skills and scout snapshots
AGENTS.md                    Agent router and operating contract
```
