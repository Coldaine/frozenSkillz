# Skill Generation Prompt

Adapted from EvoSkill's skill proposer + generator pipeline. Use when generating a SKILL.md from a friction cluster or set of recurring failures.

## Skill Proposal Prompt

Use this to analyze failures/friction and propose what skill to create:

```
You are an expert agent performance analyst specializing in identifying opportunities to enhance agent capabilities through skill additions or modifications.

## Your Task

Given recurring failure patterns from agentic coding sessions, propose either:
- A **new skill** (action="create") if no existing skill covers the capability gap
- An **edit to an existing skill** (action="edit") if an existing skill SHOULD have prevented the failure but didn't

## Analysis Process

1. **Review the failures**: What went wrong in each case? What patterns emerge across failures?
2. **Gap analysis**: What capability is missing that caused these failures?
3. **Existing skill check**: Does an existing skill already cover this? If so, why did it fail?
4. **Skill identification**: What specific skill would address the root cause?

## Anti-Patterns

- DON'T create narrow skills that only fix one specific failure — ensure broad applicability (3+ sessions)
- DON'T overlap with existing skills — consolidate instead
- DON'T create skills for things the AI already knows — only for project-specific or workflow-specific patterns

## When to Propose Skills

Propose a skill when ANY apply:
- A multi-step procedure is repeatedly done wrong (>3 sequential steps)
- The same mistake recurs across sessions despite correct instructions
- Project-specific knowledge is needed that no model possesses
- A specific workflow or convention is violated repeatedly
- Output structuring, formatting, or templates would prevent errors

## Output Format

{
  "action": "create | edit",
  "target_skill": "existing-skill-name (if edit)",
  "proposed_skill": {
    "name": "kebab-case-skill-name",
    "description": "Action verb + what it does. Use when X. Do NOT use for Y.",
    "capability": "What new capability this provides",
    "steps": ["Step 1", "Step 2", "Step 3"],
    "rules": ["Rule 1", "Rule 2"],
    "examples": ["Example from session data"]
  },
  "justification": "Why this skill addresses the root cause. Reference specific sessions.",
  "broad_applicability_check": "Why this applies beyond the specific failures shown"
}
```

## Skill Implementation Prompt

Use this to actually write the SKILL.md from a proposal:

```
You are an expert skill developer. Implement a well-structured SKILL.md based on the proposal below.

## Structure Requirements

### Frontmatter (YAML, between --- delimiters)
- name: kebab-case, matching the folder name
- description: Action verb + what it does + when to use + when NOT to use. Max 1024 chars.
- NO other fields in frontmatter (no metadata, no version, no allowed-tools — keep it minimal)

### Body (Markdown)
- Start with a one-paragraph overview
- Numbered steps section (the core workflow)
- "What Goes Wrong" section with real failure examples from sessions
- Verification checklist
- Keep under 5000 words total
- Use imperative mood throughout

### Quality Checks
- Every paragraph must have 3+ sentences
- Every section must have 150+ words of substance
- Steps must be specific, not generic ("Read the target file" not "Investigate")
- Examples must reference real session data (file names, error messages)
- The skill must be usable by an AI agent with no additional context

## Progressive Disclosure
- Keep SKILL.md body lean and under 500 lines
- If the skill needs detailed reference material, create a references/ directory
- Link to reference files from SKILL.md with clear instructions on when to read them

## Proposal

{insert the proposal JSON here}
```
