# Analysis: WondelAI skills pragmatic-programmer

## Scope

- Selected artifacts: source/pragmatic-programmer/SKILL.md and source/pragmatic-programmer/references/tracer-bullets.md
- Reason this scope is narrow enough: only the tracer-bullet/prototype portion directly addresses progress under implementation uncertainty.
- Out-of-scope artifacts: the other five references and all unrelated WondelAI skills, plugins, catalogs, and host symlinks.

## Rubric Scores

| Artifact | Type | Average | Recommendation |
|---|---|---:|---|
| source/pragmatic-programmer/SKILL.md | skill | 3.9 | Incubate; do not install the whole broad skill merely to obtain tracer-bullet guidance. |
| source/pragmatic-programmer/references/tracer-bullets.md | documentation-pattern | 4.0 | Strong concept candidate; evaluate a narrow, independently worded adaptation. |

## Detailed Notes

### source/pragmatic-programmer/SKILL.md

| Dimension | Score | Rationale |
|---|---:|---|
| Purpose clarity | 4 | Seven meta-principles are explained clearly, but the overall purpose is broad. |
| Activation or invocation clarity | 5 | Frontmatter gives many explicit phrases and adjacent decision contexts. |
| Output contract | 3 | It mandates a score and fixes but does not define one coherent output for all trigger modes. |
| Reuse value | 4 | The concepts are broadly reusable, though only a subset fits the current planning need. |
| Progressive disclosure or structure | 4 | Six references are routed, but the entrypoint itself remains 16.5 KB. |
| Safety/security risk | 3 | It is mainly advisory but lacks experiment isolation, secret boundaries, and mutation permissions. |
| Portability | 5 | The prose is mostly host and platform neutral. |
| Testability/evaluability | 3 | A diagnostic table is repeatable but subjective, and no upstream eval is supplied. |
| Maintenance burden | 3 | One large entrypoint plus six long references creates a substantial upkeep surface. |
| Fit with frozenSkillz scope | 4 | Useful engineering guidance, but broader than a focused uncertainty-to-progress workflow. |
| Trigger clarity | 5 | Trigger phrases and related contexts are explicit. |
| Negative triggers | 4 | It routes code-level quality and refactoring elsewhere, though it does not exclude narrow tasks generally. |
| Reference and template routing | 4 | Deep topics route to named references with use conditions. |
| Gate quality before action | 3 | The diagnostic promotes reflection but can impose a full audit before a narrow action. |

Average: 54 / 14 = 3.86, rounded to 3.9.

### source/pragmatic-programmer/references/tracer-bullets.md

| Dimension | Score | Rationale |
|---|---:|---|
| Purpose clarity | 5 | It distinguishes thin production slices from disposable experiments. |
| Activation or invocation clarity | 4 | The opening states when to load it, though it depends on the parent skill. |
| Output contract | 4 | The decision guide and iteration cycle imply a concrete choice and action. |
| Reuse value | 5 | The uncertainty classification applies across many software domains. |
| Progressive disclosure or structure | 4 | It is a routed deep reference with a table of contents, though still long. |
| Safety/security risk | 3 | It warns against shipping prototypes but tells prototypes to ignore correctness without requiring isolation or secret hygiene. |
| Portability | 5 | Guidance is tool and platform neutral. |
| Testability/evaluability | 4 | A fixed scenario can test whether the agent selects and scopes the right technique. |
| Maintenance burden | 3 | The concept is stable, but the long examples and checklist add review burden. |
| Fit with frozenSkillz scope | 5 | It directly supports progress-oriented implementation under uncertainty. |
| Authority flow | 3 | It distinguishes prototype and production authority but does not connect decisions to project authority documents. |
| Self-enforcement | 3 | Warnings are explicit but not paired with operational controls. |
| Drift resistance | 4 | The core distinction is stable and not tied to current APIs. |
| Clear legal homes for overflow content | 4 | It clearly separates disposable work from retained production slices and suggests separate branches or repositories. |

Average: 56 / 14 = 4.0.

## Summary Recommendation

- Recommended outcome: incubate for later; likely adapt the tracer/prototype concept only after eval and provenance review.
- Evidence: the narrow reference gives a strong progress loop, while the parent skill is broad, score-heavy, and expensive to load.
- Open questions: Does a lean adaptation improve time-to-working-slice over baseline? How much original wording can be safely retained versus independently restated from general engineering practice?
