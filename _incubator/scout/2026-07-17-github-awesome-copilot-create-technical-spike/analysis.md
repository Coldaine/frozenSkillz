# Analysis: GitHub awesome-copilot create-technical-spike

## Scope

- Selected artifacts: source/skills/create-technical-spike/SKILL.md
- Reason this scope is narrow enough: the upstream target contains one standalone skill file and no routed references.
- Out-of-scope artifacts: all other awesome-copilot skills, plugins, extensions, hooks, examples, and catalog documentation.

## Rubric Scores

| Artifact | Type | Average | Recommendation |
|---|---|---:|---|
| source/skills/create-technical-spike/SKILL.md | skill | 3.5 | Incubate; evaluate the concept, then adapt rather than importing unchanged. |

## Detailed Notes

### source/skills/create-technical-spike/SKILL.md

| Dimension | Score | Rationale |
|---|---:|---|
| Purpose clarity | 5 | It explicitly creates time-boxed technical-spike documents for consequential development decisions. |
| Activation or invocation clarity | 4 | The frontmatter is clear, but concrete trigger and exclusion examples are absent. |
| Output contract | 5 | It supplies a complete document shape, naming convention, phases, and completion criteria. |
| Reuse value | 4 | The spike structure is broadly useful after host and ceremony reduction. |
| Progressive disclosure or structure | 2 | Template, taxonomy, strategy, and tool guidance are monolithic in one 6.5 KB file. |
| Safety/security risk | 3 | It names execution and edit tools without permission, secret, isolation, or rollback rules. |
| Portability | 2 | Input interpolation and named Copilot/VS Code tools will not resolve uniformly across hosts. |
| Testability/evaluability | 4 | The document contract and decision outcome can be compared repeatably, but no eval ships upstream. |
| Maintenance burden | 4 | One file is bounded, though host tool names can drift. |
| Fit with frozenSkillz scope | 5 | It directly targets reusable agent planning and uncertainty reduction. |
| Trigger clarity | 4 | The intended use is clear from the description and title. |
| Negative triggers | 1 | It does not say when a spike is unnecessary or when implementation should continue directly. |
| Reference and template routing | 2 | The large template is embedded rather than routed. |
| Gate quality before action | 4 | It requires a question, timebox, success criteria, evidence, and recommendation, but not a cheapest-probe or parallel-progress decision. |

Average: 49 / 14 = 3.5.

## Summary Recommendation

- Recommended outcome: incubate for later, with likely adapt-concept-only packaging after eval.
- Evidence: strong explicit research sequence and decision contract; weak portability, negative triggers, and protection against process overhead.
- Open questions: Does the full spike document improve decisions enough to justify its cost? Can a lean adaptation use web research and local inspection first while known implementation continues?
