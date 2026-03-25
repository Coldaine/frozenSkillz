# Skill Search

Search for skills across registries and repositories.

## Search Sources

### Primary Registries

1. **skills.sh** - Central registry
   - Web: https://skills.sh/
   - CLI: `npx skills find [query]` (if available)

2. **GitHub Topics**
   - Search: `topic:claude-skill` or `topic:agent-skill`
   - Filter by stars, recent updates

3. **Awesome Lists**
   - https://github.com/ComposioHQ/awesome-claude-skills
   - https://github.com/littleben/awesomeAgentskills

### Local Sources

Check user's existing skills for patterns:
- `~/.claude/skills/`
- `~/.codex/skills/`
- `~/.agents/skills/`

## Search Process

### Step 1: Understand Need

Clarify with user:
- What domain? (devops, testing, design, data)
- What specific task? (not "help with databases" but "safe production queries")
- Any constraints? (read-only, specific tools, safety requirements)

### Step 2: Query Formulation

Translate to search terms:
- User: "How do I make my React app faster?"
- Query: `react performance optimization`

- User: "Can you help with PR reviews?"
- Query: `pr review code review`

- User: "I need to create a changelog"
- Query: `changelog release notes`

### Step 3: Execute Search

**Using the Skills CLI (automated):**
```powershell
scripts/search-skills.ps1 -Query "your search term" -Limit 10
```

This outputs JSON with:
- `FullName`: Package reference (owner/repo@skill)
- `Installs`: Install count (popularity metric)
- `InstallCommand`: Ready-to-run install command
- `Url`: skills.sh page URL

**Manual search (fallback):**
1. Run query via `npx skills find [query]`
2. Capture top 5-10 results
3. Note: name, description, source URL, install command

### Step 4: Pre-filter

Before evaluation, quickly filter obvious mismatches:
- Description clearly wrong domain? Skip
- Last updated >2 years ago? Flag as potentially stale
- No README or documentation? Flag as risky

## Output Format

```markdown
## Search Results for "{query}"

### 1. {skill-name}
- **Source**: skills.sh
- **Installs**: {N}
- **Description**: {description}
- **Install**: `npx skills add {package}`
- **Preliminary**: {Looks relevant / Check further / Skip - reason}

### 2. ...

## Next Steps

1. Run `/skill-manager evaluate {path}` for promising candidates
2. Or install directly: `scripts/install-skill.ps1 -Package "owner/repo@skill" -Yes`
```

## Post-Search: Evaluate Before Install

**Never install directly from search results.**

Always run evaluation:
```
/skill-manager evaluate candidate-skill/
```

Then compare against existing:
```
/skill-manager compare candidate-skill existing-skill
```
