# Skill Evaluation

Evaluate a skill against 7 quality heuristics. Output a structured report with scores and specific recommendations.

## Input

Path to a skill directory containing SKILL.md

## Evaluation Process

### 1. Specific Activation (0-3 points)

**What to check:**
- Does the description tell WHEN to use the skill, not just what it contains?
- Would this trigger for irrelevant queries?
- Is the scope clear from the description alone?

**Scoring:**
- 0: Vague like "Helps with code" - triggers for everything
- 1: Somewhat specific but could be clearer
- 2: Clear scope but might catch edge cases
- 3: Precise trigger conditions, minimal false positives

**Example good:** "Safe read-only PostgreSQL queries for analytics. Use when exploring production data without modifying."

**Example bad:** "Database helper" - triggers for any DB mention.

---

### 2. Complete Workflow (0-3 points)

**What to check:**
- Are there clear steps to execute?
- Are inputs defined?
- Are outputs specified?
- Are stop conditions documented?
- Is there error handling?

**Scoring:**
- 0: Just knowledge/tips, no process
- 1: Some steps but gaps in inputs/outputs/errors
- 2: Most elements present but unclear in places
- 3: Complete process with all elements defined

**Look for:**
```markdown
## Inputs Needed
- X, Y, Z

## Steps
1. Do A
2. Do B
3. Do C

## Stop Conditions
- Stop if X happens

## Error Handling
- If Y fails, do Z
```

---

### 3. Progressive Disclosure (0-3 points)

**What to check:**
- Is SKILL.md a lightweight index or a monolith?
- Are there separate files in `instructions/`, `scripts/`, `templates/`, `references/`?
- Are large reference materials externalized?

**Scoring:**
- 0: Everything in one 500+ line SKILL.md
- 1: Some separation but main file still heavy
- 2: Good structure but could be better
- 3: SKILL.md is navigation, details loaded on demand

**Check for directories:**
- `instructions/` - Detailed guidance
- `scripts/` - Executable scripts
- `templates/` - Output templates
- `examples/` - Usage examples
- `references/` - Large reference docs

---

### 4. Narrow Scope (0-3 points)

**What to check:**
- Can you describe what this skill does in 10 words or less?
- Does it try to cover multiple unrelated domains?
- Would you use this skill 3+ times in a typical week?

**Scoring:**
- 0: "Backend development" - tries to cover everything
- 1: Still too broad, covers 2-3 distinct areas
- 2: Reasonably focused but some scope creep
- 3: Laser-focused on single well-defined problem

**Red flags:**
- Multiple "When to Use" sections for unrelated tasks
- Description uses "and" to connect unrelated capabilities
- Would need to be completely rewritten for a different codebase

---

### 5. Code for Determinism (0-3 points)

**What to check:**
- Are there scripts in `scripts/` directory?
- Do scripts handle deterministic tasks (parsing, formatting, validation)?
- Is LLM reserved for judgment/reasoning?

**Scoring:**
- 0: No scripts, everything is LLM prompts
- 1: Some scripts but minimal
- 2: Good script coverage but some gaps
- 3: Deterministic work scripted, LLM for decisions only

**Good patterns:**
- `scripts/validate.sh` - Check if query is read-only
- `scripts/format-results.py` - Consistent output formatting
- `scripts/health-check.sh` - Environment validation

---

### 6. Invocation Control (0-2 points)

**What to check:**
- Does the skill have side effects (write, deploy, send)?
- If yes, is `disable-model-invocation: true` set?
- Is `user-invocable: false` used appropriately for background knowledge?

**Scoring:**
- 0: Side effects but auto-invokes (dangerous)
- 1: Mixed - some control but inconsistent
- 2: Appropriate controls for all side-effect skills

**Critical checks:**
- Skills that write files/deploy/send messages MUST have `disable-model-invocation: true`
- Background knowledge skills (conventions, context) should have `user-invocable: false`

---

### 7. Validation (0-2 points)

**What to check:**
- Is there evidence this skill works (evals, tests, real usage)?
- At minimum, has it been used 3+ times without issues?
- Does the skill have obvious failure modes?

**Scoring:**
- 0: Unknown quality, never tested
- 1: Informally tested ("seems to work")
- 2: Some validation (evals or real usage evidence)

**Note:** Full formal evals are aspirational. "Used 3 times successfully" is valid for internal skills.

---

## Output Format

Use [templates/evaluation-report.md](templates/evaluation-report.md):

```markdown
# Skill Evaluation: {skill-name}

## Overall Score: {X}/17

| Heuristic | Score | Notes |
|-----------|-------|-------|
| Specific Activation | X/3 | |
| Complete Workflow | X/3 | |
| Progressive Disclosure | X/3 | |
| Narrow Scope | X/3 | |
| Code for Determinism | X/3 | |
| Invocation Control | X/2 | |
| Validation | X/2 | |

## Summary

{One sentence verdict: Install / Fix and Install / Skip}

## Specific Issues

1. {Issue} → {Fix}
2. {Issue} → {Fix}

## Recommendations

- {Action item}
```

---

## Quick Scoring Guide

**Total score interpretation:**
- **15-17**: Excellent skill, install immediately
- **12-14**: Good skill, minor improvements suggested
- **8-11**: Okay skill, notable issues to fix
- **5-7**: Poor skill, major rework needed
- **0-4**: Reject, don't install

**Dealbreakers (auto-reject regardless of other scores):**
- Side effects + auto-invoke = DANGEROUS
- Monolithic SKILL.md >500 lines without externalized content
- Description so vague it triggers for everything
