# Analysis: AaravKashyap12 advise-project-approach

## Scope

- Selected artifacts: source/skills/advise-project-approach/SKILL.md and source/skills/advise-project-approach/agents/openai.yaml
- Reason this scope is narrow enough: this is the complete target skill, while evaluation is limited to its mid-build research-and-recommendation mode.
- Out-of-scope artifacts: pre-build pricing depth, post-build review quality, packaged dist artifact, and all non-target repository files.

## Rubric Scores

| Artifact | Type | Average | Recommendation |
|---|---|---:|---|
| source/skills/advise-project-approach/SKILL.md | skill | 4.1 | Incubate; strong research discipline, but split and live-evaluate before adaptation. |
| source/skills/advise-project-approach/agents/openai.yaml | config | N/A | Preserve as provenance; no independent packaging decision before the skill is evaluated. |

## Detailed Notes

### source/skills/advise-project-approach/SKILL.md

| Dimension | Score | Rationale |
|---|---:|---|
| Purpose clarity | 5 | It explicitly covers evidence-based project strategy before, during, and after implementation. |
| Activation or invocation clarity | 5 | Frontmatter, operating modes, and mode-selection rules are concrete. |
| Output contract | 5 | It defines separate detailed contracts for pre-build and mid/post-build work. |
| Reuse value | 5 | Local inspection, comparable research, cost reality, and failure conditions transfer broadly. |
| Progressive disclosure or structure | 2 | Nearly all behavior lives in one 21.9 KB entrypoint with no routed references. |
| Safety/security risk | 5 | Read-only defaults, mutation permission boundaries, and explicit sensitive-file exclusions are strong. |
| Portability | 4 | Core behavior is host neutral, but quality depends on browsing and one OpenAI metadata file accompanies it. |
| Testability/evaluability | 4 | Fixed fixtures can test evidence and recommendation quality, though no upstream eval is included. |
| Maintenance burden | 2 | Pricing, ecosystem freshness, repo signals, security, and two output modes in one file create high review burden. |
| Fit with frozenSkillz scope | 5 | It directly supports reusable research and project-strategy workflows. |
| Trigger clarity | 5 | Broad positive triggers are explicit and tied to three lifecycle modes. |
| Negative triggers | 5 | It excludes narrow single-bug debugging and isolated edits unless broader direction is requested. |
| Reference and template routing | 1 | Heavy research rules and embedded output templates are not routed to references or templates. |
| Gate quality before action | 5 | It requires evidence status, constraints, primary-source freshness, tradeoffs, and failure conditions before confident advice. |

Average: 58 / 14 = 4.14, rounded to 4.1.

### source/skills/advise-project-approach/agents/openai.yaml

The 310-byte config provides a display name, short description, and default
prompt. It is useful packaging metadata but does not independently implement,
constrain, or validate the workflow, so an independent rubric average would be
misleading.

## Summary Recommendation

- Recommended outcome: incubate for later, likely adapt or split the concept after live eval.
- Evidence: unusually strong research freshness, safety, tradeoff, and output discipline; weak progressive disclosure and potentially excessive scope for one technical unknown.
- Open questions: Can a lean trigger route pricing, comparable research, and output templates only when needed? Does the candidate materially outperform baseline without delaying ongoing implementation?
