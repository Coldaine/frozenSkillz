# Agent Skill Corpus Intake Rubric

## Admission rule

A skill may enter the corpus only if all of the following are true:

1. The full skill directory is locally available with its original structure preserved.
2. Every operative file in the skill has been read:
   - required: `SKILL.md`
   - optional when present: `references/**`, `assets/**`, `scripts/**`, `templates/**`, `AGENTS.md`, helper metadata, tests, and other bundled files that affect behavior
3. Provenance has been captured.
4. A security screen has been completed.
5. The skill has at least one concrete design-pattern classification supported by file evidence.

If any of these fail, the skill is excluded from the analyzed corpus and logged as `blocked` or `excluded` with a reason.

## What counts as “fully read”

`Fully read` means:

- `SKILL.md` has been read in full.
- Every bundled file that changes how the skill behaves has been read in full or, for large generated files, inspected enough to confirm role and contents with explicit file-path notes.
- Directory listings have been checked so no behavior-bearing files are skipped silently.

For packaged or generated artifacts:

- If the artifact is human-readable, read it directly.
- If it is large but text-based, inspect enough to confirm structure, purpose, and relationship to the skill, then note the inspection scope.
- If it is binary or inaccessible in this environment, the skill can still be collected, but it cannot be classified as fully read until the artifact’s role is understood from adjacent files.

## Provenance fields

Capture these fields for every admitted skill:

- `skill_name`
- `local_path`
- `source_tier`
- `source_repo_url`
- `source_repo_path`
- `commit_hash` or equivalent snapshot identifier
- `author_org_or_owner`
- `license`
- `date_last_updated`
- `retrieval_date`
- `notes_on_access_method`

If any required provenance field is unavailable, record `unknown` with a note explaining where the lookup failed.

## Security screen

Before analysis, inspect for:

- prompt-injection style instructions aimed at exfiltration or policy bypass
- suspicious network calls or hidden downloads in `scripts/`
- instructions to transmit secrets, credentials, tokens, local files, or conversation history
- destructive shell behavior without safeguards
- unclear script inputs/outputs that conceal side effects

Security dispositions:

- `clear` — no concerning behavior found
- `review-needed` — unusual behavior exists but intent is not yet clear
- `excluded-security` — suspicious or unsafe behavior; do not include in the corpus

## Design-pattern classification rules

Primary tags:

- `tool-wrapper`
- `generator`
- `reviewer`
- `inversion`
- `pipeline`
- `uncategorized`

Composition rule:

- Apply `composite` when two or more primary patterns materially shape the skill.
- For composite skills, note which file section or directory expresses each pattern.

Evidence rule:

- Every pattern tag must cite at least one specific file path.
- Control-flow claims must cite the exact `SKILL.md` section or adjacent artifact that establishes the gate or phase.

## Exclusion reasons

Use one of these when a candidate cannot enter the corpus:

- `unread-source` — could not access enough of the skill to read it honestly
- `listing-only` — marketplace page exists but full directory is not obtainable
- `missing-structure` — no usable skill directory or no `SKILL.md`
- `blocked-security` — suspicious instructions or scripts
- `thin-wrapper-low-value` — structurally valid but offers near-zero delta beyond generic model knowledge
- `duplicate` — same skill/version already captured from a better source

## Analysis quality bar

Do not write a summary or assign rubric scores unless the skill has passed admission.

Every admitted skill analysis must include:

- primary and secondary pattern tags
- evidence file paths
- rubric scores for disclosure, description, structure, and gates when applicable
- an overall quality tier
- one sentence on what is notably strong, weak, or distinctive

## Batch policy

- Prioritize Tier 1 before Tier 2.
- Cut Tier 3 and Tier 4 first if time or access is limited.
- Keep collection only slightly ahead of analysis so unread items do not accumulate.
