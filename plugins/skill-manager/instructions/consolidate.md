# Skill Consolidation

Merge multiple related skills into fewer, better skills.

## When to Consolidate

**Trigger:** Audit finds 3+ skills in same domain with overlapping functionality.

**Common patterns:**
- Presentation skills (12 → 2-3)
- Testing skills (unit-test, e2e-test, integration-test → testing)
- Git skills (commit, branch, rebase → git-workflow)

## Consolidation Process

### Step 1: Analyze Group

List all skills in domain:
```
slide-consult      - Consulting on slide design
slide-export       - Exporting slides to various formats
slide-image        - Adding images to slides
slide-maker-kb     - Knowledge base for slide making
slide-qa           - QA checking slides
slide-research     - Research for slide content
slide-reviewer     - Reviewing slides
slide-script       - Script writing for slides
slide-story        - Storytelling in slides
slide-template     - Slide templates
slide-theme        - Slide themes
```

### Step 2: Identify Core Capabilities

Group by function:
- **Create**: slide-maker-kb, slide-template, slide-theme, slide-story, slide-script
- **Review**: slide-consult, slide-reviewer, slide-qa
- **Enhance**: slide-image, slide-research
- **Output**: slide-export

### Step 3: Design Consolidated Structure

```
presentation-suite/
├── SKILL.md                    # Entry point, router
├── instructions/
│   ├── create.md               # Building presentations
│   ├── review.md               # Reviewing presentations
│   └── export.md               # Export/delivery
├── scripts/
│   ├── validate-structure.sh   # Check slide structure
│   ├── export-format.py        # Format conversion
│   └── image-optimize.sh       # Image optimization
└── templates/
    ├── pitch-deck/             # Industry-specific templates
    ├── status-update/
    └── training/
```

### Step 4: Merge Content

**From slide-template, slide-theme → create.md:**
```markdown
## Templates

### Pitch Deck
- 10-12 slides
- Problem → Solution → Market → Traction → Team → Ask

### Status Update
- 4-6 slides
- Progress → Blockers → Next Steps

### Themes
- Corporate: Blue, clean, professional
- Startup: Bold, colorful, energetic
- Academic: Minimal, data-focused
```

**From slide-consult, slide-reviewer, slide-qa → review.md:**
```markdown
## Review Checklist

### Structure
- [ ] Clear narrative arc
- [ ] One idea per slide
- [ ] Logical flow between slides

### Visual
- [ ] Consistent typography
- [ ] High contrast for readability
- [ ] Images support message (not decoration)

### Content
- [ ] No walls of text
- [ ] Data has context
- [ ] Call to action is clear
```

### Step 5: Migration Path

**Option A: Immediate replacement**
1. Create consolidated skill
2. Delete old skills
3. Test consolidated skill thoroughly

**Option B: Gradual migration**
1. Create consolidated skill
2. Mark old skills `disable-model-invocation: true`
3. Use for 2 weeks, verify consolidated works
4. Delete old skills

**Option C: Keep best, delete rest**
1. Evaluate all in group
2. Keep highest scoring skill
3. Note gaps in kept skill
4. Enhance kept skill if needed
5. Delete others

## Consolidation Decision Matrix

| Situation | Approach | Example |
|-----------|----------|---------|
| All low quality | Create new consolidated | 12 presentation skills → presentation-suite |
| One good, others bad | Keep best, delete rest | 3 git skills → keep git-workflow |
| All good but overlapping | Merge into unified skill | unit-test + e2e-test + integration-test → testing |
| Different but related domains | Create meta-skill that routes | frontend-react + frontend-vue + frontend-angular → frontend-meta |

## Consolidation Output

```markdown
## Consolidation Plan: {domain}

### Current State
{N} skills: {list}

### Consolidated Structure
```
{new-skill-name}/
├── SKILL.md
├── instructions/
│   ├── {topic-1}.md
│   ├── {topic-2}.md
│   └── {topic-3}.md
├── scripts/
│   └── {script-1}.{ext}
└── templates/
    └── ...
```

### Content Mapping

| Old Skill | Content | Goes To |
|-----------|---------|---------|
| {skill-a} | {description} | {new-location} |
| {skill-b} | {description} | {new-location} |

### Migration
- **Approach**: {immediate / gradual / keep-best}
- **Timeline**: {when}
- **Testing**: {how to verify}

### New Skill Score Prediction
- Expected score: {X}/17 (vs current average {Y}/17)
- Key improvements: {specific benefits}
```

## Post-Consolidation

### Verify
1. New skill triggers correctly for all original use cases
2. No loss of functionality
3. Quality score higher than original average

### Document
- Add note in CLAUDE.md or AGENTS.md about consolidation
- Why it was done, what replaced what

### Clean Up
1. Delete old skill directories
2. Update any docs referencing old skill names
3. Re-run audit to confirm improvement
