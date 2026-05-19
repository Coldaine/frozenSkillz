---
name: skill-manager
description: Use when auditing, reviewing, or preparing changes to a multi-client AI skill portfolio across Claude, Codex, Gemini, Opencode, shared .agents roots, plugins, and frozenSkillz archives.
---

# Skill Manager

Manage your skill portfolio across all agent tools. Search for new skills, evaluate quality, detect redundancies, and generate dry-run state reports before changing live client configuration.

## When to Use This Skill

- Searching for skills to solve a specific problem
- Evaluating whether a found skill is worth installing
- Auditing your existing skill portfolio for quality
- Producing a dry-run inventory before touching live skill folders
- Finding stale client config references and duplicate skill names
- Identifying redundant or overlapping skills
- Deciding whether to consolidate multiple skills

## Commands

| Command | Purpose | Script |
|---------|---------|--------|
| `/skill-manager search <query>` | Search skills.sh registry | `skills-cli.ps1 search` |
| `/skill-manager install <package>` | Install a skill | `skills-cli.ps1 install` |
| `/skill-manager list` | List installed skills | `skills-cli.ps1 list` |
| `/skill-manager audit` | Review all skills for issues | `skills-audit.ps1` |
| `/skill-manager inventory` | Inventory live and frozenSkillz skill surfaces | `skills-state.ps1 inventory` |
| `/skill-manager plan` | Show dry-run drift actions from `skill-policy.json` | `skills-state.ps1 plan` |
| `/skill-manager report` | Write `skill-state.lock.json` and latest report | `skills-state.ps1 report` |
| `/skill-manager evaluate <path>` | Score skill against heuristics | Manual analysis |
| `/skill-manager compare <s1> <s2>` | Compare for overlap | Manual analysis |

## Workflow

### Finding and Installing Skills

1. **Search**: Find candidate skills from registries
2. **Evaluate**: Score each candidate against quality heuristics
3. **Compare**: Check against existing skills for overlap
4. **Decide**: Install, skip, or find alternative

## Quick Start

```powershell
# Search for skills
./scripts/skills-cli.ps1 search "pr review" -Limit 5

# Install a skill  
./scripts/skills-cli.ps1 install "owner/repo@skill" -Yes

# List installed skills
./scripts/skills-cli.ps1 list

# Audit your skills
./scripts/skills-audit.ps1

# Inventory current live state without editing it
./scripts/skills-state.ps1 inventory

# Generate a dry-run plan against ../../skill-policy.json
./scripts/skills-state.ps1 plan

# Write ../../skill-state.lock.json and ../../reports/latest-skill-state.md
./scripts/skills-state.ps1 report
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

### Dry-Run State Management

Use `scripts/skills-state.ps1` before any cleanup that touches client runtime folders. It reads live surfaces and writes only inside the frozenSkillz repo when `report` is used.

The dry-run state flow is:

1. `inventory`: discover skill files, config references, plugin cache entries, frozenSkillz published skills, and archived corpora.
2. `plan`: compare inventory to `skill-policy.json` and emit proposed changes only.
3. `report`: persist `skill-state.lock.json` plus `reports/latest-skill-state.md` for review and commits.

Do not copy plugin internals into global skill folders. Treat plugin and system skills as external inventory unless a separate publishing workflow explicitly owns them.

## Skill Discovery

Skills are discovered from:

- `~/.claude/skills/` (Claude Code)
- `~/.codex/skills/` (Codex CLI)
- `~/.agents/skills/` (shared agent skill root)
- `~/.gemini/skills/` and Gemini's disabled skill list
- `~/.config/opencode/` skill files and skill path references
- Codex plugin cache and frozenSkillz published/archived skills
- External registries (skills.sh, GitHub)

Use `skills-state.ps1 inventory` for source classification and `skills-cli.ps1 list` for the simple installed-skill table.
