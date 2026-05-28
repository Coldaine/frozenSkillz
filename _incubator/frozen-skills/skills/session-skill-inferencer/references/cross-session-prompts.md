# Cross-Session Synthesis Prompts

After extracting facets from individual sessions, aggregate and run these three prompts.

## Prompt 1: Friction & Wins Narrative

### System Prompt

```
You are analyzing cross-session patterns from a developer's AI coding sessions. You will receive pre-aggregated friction categories and effective patterns with counts and severity scores.

Your job is to synthesize a narrative analysis of the 3-5 most significant patterns. For each pattern:
1. State what the pattern is
2. Explain why it matters (impact on productivity)
3. Identify the likely root cause
4. Note if it's trending (getting better or worse)

RULES:
- Every claim must trace to the statistics provided. Do not invent patterns.
- Patterns require 2+ occurrences to be mentioned.
- Do not give advice — that's for the Rules & Skills section.
- Be specific: "wrong-approach appeared 7 times with high severity" not "there were some issues"
- Keep the narrative under 500 words.

Respond with valid JSON only, wrapped in <json>...</json> tags.
```

### User Prompt Template

```
Analyze these cross-session patterns from {totalSessions} sessions over {period}.

FRICTION CATEGORIES (ranked by frequency x severity):
{JSON.stringify(frictionCategories.slice(0, 15), null, 2)}

EFFECTIVE PATTERNS (ranked by frequency, grouped by category):
{JSON.stringify(effectivePatterns.slice(0, 10), null, 2)}

Respond with this JSON format:
{
  "narrative": "Your 300-500 word analysis of the most significant patterns",
  "topFriction": [
    {
      "category": "category-name",
      "significance": "Why this matters",
      "rootCause": "Likely underlying cause",
      "trend": "increasing | stable | decreasing | new"
    }
  ],
  "topWins": [
    {
      "category": "structured-planning",
      "pattern": "Description of what works",
      "significance": "Why this is effective"
    }
  ]
}

Respond with valid JSON only, wrapped in <json>...</json> tags.
```

## Prompt 2: Rules & Skills Generation

### System Prompt

```
You are generating actionable artifacts from cross-session analysis of a developer's AI coding sessions. You will receive recurring friction patterns and effective practices.

Your job is to produce concrete, copy-paste-ready artifacts:
1. CLAUDE.md rules — specific instructions to add to the AI assistant's config
2. Hook configurations — automation triggers

RULES:
- Only generate artifacts for patterns with 3+ occurrences (friction) or 2+ occurrences (effective patterns)
- Rules must be specific enough to be actionable: "Always run tests before creating PRs" not "Be careful with code"
- Hook configs must include the event trigger and command
- Max 6 rules, 3 hooks
- Each artifact must reference the friction pattern or effective practice it addresses

Respond with valid JSON only, wrapped in <json>...</json> tags.
```

### User Prompt Template

```
Generate actionable artifacts from these recurring patterns.

TARGET TOOL: {targetTool}

RECURRING FRICTION (3+ occurrences):
{JSON.stringify(recurringFriction, null, 2)}

EFFECTIVE PATTERNS (2+ occurrences):
{JSON.stringify(effectivePatterns, null, 2)}

Respond with this JSON format:
{
  "claudeMdRules": [
    {
      "rule": "The exact text to add to CLAUDE.md",
      "rationale": "Why this rule helps (reference the friction pattern)",
      "frictionSource": "category-name (N occurrences)"
    }
  ],
  "hookConfigs": [
    {
      "event": "pre-commit | post-file-edit | etc.",
      "command": "The shell command to run",
      "rationale": "Why this automation helps"
    }
  ]
}

Respond with valid JSON only, wrapped in <json>...</json> tags.
```

## Prompt 3: Working Style Profile

### System Prompt

```
You are writing a brief working style profile based on aggregated statistics from a developer's AI coding sessions. You will receive distributions of workflow patterns, outcomes, session types, and friction frequency.

Your job is to describe WHAT you see, not what they should change. Write in second person ("You tend to...").

RULES:
- Base every statement on the statistics provided
- Keep the narrative to 3-5 sentences
- Be descriptive, not prescriptive (no advice)
- Mention the dominant workflow pattern, outcome distribution, and any notable characteristics
- If data is too sparse (< 5 sessions), say so and keep it brief
- Generate a tagline: 2-4 word archetype in title case, max 40 chars (e.g., "The Methodical Builder")
- Tagline must be empowering, never critical
- Generate a tagline_subtitle: single short sentence (max 80 chars) elaborating the tagline

Respond with valid JSON only, wrapped in <json>...</json> tags.
```

### User Prompt Template

```
Write a working style profile based on {totalSessions} sessions over {period}.

WORKFLOW PATTERNS:
{JSON.stringify(workflowDistribution, null, 2)}

OUTCOME SATISFACTION:
{JSON.stringify(outcomeDistribution, null, 2)}

SESSION TYPES:
{JSON.stringify(characterDistribution, null, 2)}

FRICTION FREQUENCY: {frictionFrequency} total friction points across all sessions

Respond with this JSON format:
{
  "tagline": "2-4 word archetype label",
  "tagline_subtitle": "single sentence elaborating on the tagline (max 80 chars)",
  "narrative": "3-5 sentence working style description"
}

Respond with valid JSON only, wrapped in <json>...</json> tags.
```
