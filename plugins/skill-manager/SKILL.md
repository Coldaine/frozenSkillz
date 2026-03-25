---
name: skill-manager
description: Manage your skill portfolio - search, evaluate, compare, audit, and consolidate skills across Claude Code, Codex, and Kimi CLI. Use when adding skills, reviewing existing skills, or cleaning up redundant capabilities.
---

# Skill Manager

Manage your skill portfolio across all agent tools. Search for new skills, evaluate their quality, detect redundancies, and clean up cruft.

## When to Use This Skill

- Searching for skills to solve a specific problem
- Evaluating whether a found skill is worth installing
- Auditing your existing skill portfolio for quality
- Identifying redundant or overlapping skills
- Deciding whether to consolidate multiple skills

## Commands

| Command | Purpose | Script |
|---------|---------|--------|
| `/skill-manager search <query>` | Search skills.sh registry for skills matching query | `scripts/search-skills.ps1` |
| `/skill-manager install <package>` | Install a skill from registry | `scripts/install-skill.ps1` |
| `/skill-manager evaluate <skill-path>` | Score a skill against quality heuristics | Manual analysis |
| `/skill-manager audit` | Review all installed skills for issues | `scripts/list-installed.ps1` |
| `/skill-manager compare <skill1> <skill2>` | Compare two skills for overlap | Manual analysis |
| `/skill-manager consolidate` | Identify merge opportunities | Manual analysis |

## Workflow

### Finding and Installing Skills

1. **Search**: Find candidate skills from registries
2. **Evaluate**: Score each candidate against quality heuristics
3. **Compare**: Check against existing skills for overlap
4. **Decide**: Install, skip, or find alternative

## Quick Start

```powershell
# Search for skills
scripts/search-skills.ps1 -Query "pr review" -Limit 5

# Install a skill
scripts/install-skill.ps1 -Package "owner/repo@skill" -Yes

# List installed skills
scripts/list-installed.ps1
```

See [instructions/search.md](instructions/search.md) for detailed search workflow.
See [instructions/evaluate.md](instructions/evaluate.md) for evaluation criteria.

### Auditing Existing Skills

1. **List**: Find all installed skills across agents
2. **Evaluate**: Score each installed skill
3. **Detect Overlap**: Find semantically similar skills
4. **Recommend**: Suggest deletions or consolidations

See [instructions/audit.md](instructions/audit.md) for audit workflow.
See [instructions/compare.md](instructions/compare.md) for overlap detection.
See [instructions/consolidate.md](instructions/consolidate.md) for merge recommendations.

## Quality Heuristics

All skills are evaluated against 7 principles:

1. **Specific Activation** - Description clearly signals when to use
2. **Complete Workflow** - Steps, inputs, outputs, errors defined
3. **Progressive Disclosure** - Multiple files, lazy loading
4. **Narrow Scope** - One thing well, not five things adequately
5. **Code for Determinism** - Scripts for deterministic tasks
6. **Invocation Control** - Appropriate disable-model-invocation settings
7. **Validation** - Evidence it doesn't harm (ideally helps)

See [instructions/evaluate.md](instructions/evaluate.md) for detailed scoring.

## Skill Discovery

Skills are discovered from:

- `~/.claude/skills/` (Claude Code)
- `~/.codex/skills/` (Codex CLI)
- `~/.agents/skills/` (Kimi CLI)
- External registries (skills.sh, GitHub)

Use `scripts/list-installed.ps1` to enumerate local skills.
