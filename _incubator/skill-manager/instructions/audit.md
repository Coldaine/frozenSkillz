# Skill Portfolio Audit

Review all installed skills for quality, overlap, and cruft.

## Audit Steps

### Step 1: Inventory

Use `scripts/list-installed.ps1` to find all skills:

Output format:
```
AGENT          SKILL                    PATH
-----          -----                    ----
claude-code    docx                     ~/.claude/skills/docx
claude-code    pdf                      ~/.claude/skills/pdf
claude-code    slide-consult            ~/.claude/skills/slide-consult
...
kimi           frontend-testing         ~/.agents/skills/frontend-testing-best-practices
```

### Step 2: Evaluate Each Skill

Run `/skill-manager evaluate {path}` for every skill.

Track scores in table:
```
Skill                    Score  Issues
-----                    -----  ------
docx                     14/17  Minor
docx                     12/17  No scripts
slide-consult            8/17   Monolithic, vague trigger
...
```

### Step 3: Detect Overlaps

For each skill pair with Jaccard similarity > 0.6:
Run `/skill-manager compare {skill-a} {skill-b}`

### Step 4: Identify Problems

**Categories:**

| Category | Criteria | Action |
|----------|----------|--------|
| **Excellent** | Score >= 14, no overlaps | Keep, use as examples |
| **Good** | Score 11-13, minor issues | Keep, note improvements |
| **Needs Work** | Score 8-10, notable issues | Flag for fixing or deletion |
| **Poor** | Score < 8 | Recommend deletion |
| **Redundant** | High overlap with another | Recommend consolidation |
| **Unused** | Never triggered in 30 days | Consider deletion |

### Step 5: Generate Report

## Audit Output Format

```markdown
# Skill Portfolio Audit

## Summary
- **Total skills**: {N}
- **Across agents**: Claude Code ({N}), Codex ({N}), Kimi ({N})
- **Excellent**: {N} | **Good**: {N} | **Needs Work**: {N} | **Poor**: {N}
- **Redundant pairs**: {N}

## Top Issues

### 1. Redundant Skills
| Group | Skills | Recommendation |
|-------|--------|----------------|
| Presentations | slide-consult, slide-export, slide-image, ... (12 total) | Consolidate to 2-3 skills |

### 2. Poor Quality Skills
| Skill | Score | Issue | Recommendation |
|-------|-------|-------|----------------|
| {name} | {X}/17 | {problem} | Fix or delete |

### 3. Missing Capabilities
Based on installed skills, you have:
- ✅ Document processing (docx, pdf, pptx, xlsx)
- ❌ Git workflows
- ❌ Database queries
- ❌ DevOps/deployment

Consider adding: git-workflow, postgres-safe-queries, docker-containers

## Action Items

### Immediate (This Session)
1. Delete: {skill} ({reason})
2. Consolidate: {skills} into {new-name}

### Short Term (This Week)
1. Fix {skill}: {specific issue}
2. Evaluate candidates: git-workflow, postgres-safe-queries

### Long Term (This Month)
1. Create missing skills for identified gaps
```

## Specific Checks

### Check for Skill Sprawl

**Pattern:** Many skills in same domain with tiny differences

**Example:** 12 presentation skills (slide-consult, slide-export, slide-image, slide-maker-kb, slide-qa, slide-research, slide-reviewer, slide-script, slide-story, slide-template, slide-theme)

**Recommendation:** Consolidate to:
- `presentation-create` (building slides)
- `presentation-review` (reviewing slides)

### Check for Auto-Invoke Dangers

**Pattern:** Skills with side effects that auto-invoke

**Check:**
- Does skill write files? → Should have `disable-model-invocation: true`
- Does skill deploy? → Should have `disable-model-invocation: true`
- Does skill send messages? → Should have `disable-model-invocation: true`

### Check for Zombie Skills

**Pattern:** Skills that never trigger

**Indicators:**
- Description is too specific ("Q1 2024 budget meeting prep")
- Description is too vague but buried by other skills
- Domain is obsolete ("AngularJS 1.x patterns")

### Check for Monoliths

**Pattern:** Single-file skills >500 lines

**Flag for:** Progressive disclosure refactoring

## Maintenance Schedule

- **Weekly**: Glance at audit summary after adding new skills
- **Monthly**: Full re-audit, clean up "Needs Work" and "Poor" skills
- **Quarterly**: Review consolidated skills, update for new patterns
