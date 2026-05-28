# Skill Comparison

Compare two skills to detect overlap, conflicts, and redundancy.

## When to Compare

- Before installing a new skill (compare to existing)
- During audit to find redundancies
- When considering consolidation

## Comparison Dimensions

### 1. Domain Overlap

**Check:** What domains do both skills cover?

| Relationship | Action |
|--------------|--------|
| Same domain, different tasks | Keep both |
| Same domain, same task, different approach | Evaluate which is better |
| Same domain, same task, similar approach | Consolidate |
| One is subset of other | Keep superset, delete subset |

**Example:**
- Skill A: "React performance optimization"
- Skill B: "React component memoization"
→ B is subset of A, keep A only

### 2. Trigger Overlap

**Check:** Do descriptions trigger for the same queries?

**Test prompts:**
- "Help me optimize this"
- "Make this faster"
- "Review my code"

If both skills activate for same prompt → potential conflict.

### 3. Capability Overlap

**Check:** Do they provide similar outputs?

Compare:
- What steps each takes
- What outputs each produces
- What tools each uses

### 4. Quality Differential

If similar, which is better?

Run evaluation on both:
- Higher score wins
- If tied, prefer: more scripts, better progressive disclosure, clearer description

## Comparison Output

```markdown
## Skill Comparison: {skill-a} vs {skill-b}

### Domain
- {skill-a}: {domain}
- {skill-b}: {domain}
- **Overlap**: {None / Partial / High}

### Triggers
- Test prompt "{example}":
  - {skill-a}: {Activates / Doesn't activate}
  - {skill-b}: {Activates / Doesn't activate}

### Capabilities
| Aspect | {skill-a} | {skill-b} |
|--------|-----------|-----------|
| Steps | X | Y |
| Outputs | X | Y |
| Scripts | X | Y |

### Quality Scores
- {skill-a}: {X}/17
- {skill-b}: {Y}/17

### Recommendation
{Keep A / Keep B / Keep both / Consolidate / Delete both}

**Rationale**: {Why}
```

## Automated Overlap Detection

For audit: Compare all pairs of installed skills.

**Quick heuristic:**
1. Extract keywords from each description
2. Calculate Jaccard similarity: `|A ∩ B| / |A ∪ B|`
3. Flag pairs with similarity > 0.6 for manual review

**Keywords to extract:**
- Technology names (react, postgres, docker)
- Task verbs (test, deploy, review, optimize)
- Domain nouns (frontend, database, security)

Example:
- A: "React performance optimization"
- B: "Frontend performance tuning"
- Keywords A: {react, performance, optimization}
- Keywords B: {frontend, performance, tuning}
- Intersection: {performance} = 1
- Union: {react, performance, optimization, frontend, tuning} = 5
- Similarity: 1/5 = 0.2 → Low overlap

Example:
- A: "React testing best practices"
- B: "React component testing"
- Keywords A: {react, testing, best-practices}
- Keywords B: {react, component, testing}
- Intersection: {react, testing} = 2
- Union: {react, testing, best-practices, component} = 4
- Similarity: 2/4 = 0.5 → Moderate overlap, review
