# Inventory: WondelAI skills pragmatic-programmer

## Provenance

- Source URL: https://github.com/wondelai/skills
- Commit or version: ed2930cf8496336641441eef513ad2ad857b65a1; skill metadata version 1.4.0
- Import date: 2026-07-17
- License: root MIT and skill frontmatter MIT; source/LICENSE
- Reviewer: Codex planning_skill_intake
- Scout path: _incubator/scout/2026-07-17-wondelai-skills-pragmatic-programmer

## Artifact Counts

| Type | Count | Notable paths |
|---|---:|---|
| skill | 1 | source/pragmatic-programmer/SKILL.md |
| agent | 0 | — |
| command | 0 | — |
| hook | 0 | — |
| config | 0 | — |
| template | 0 | — |
| eval-case | 0 | No upstream eval artifact; one frozenSkillz eval definition exists outside source. |
| documentation-pattern | 6 | source/pragmatic-programmer/references/*.md |

## Risks

- Secret surfaces: none named; the tracer/prototype guidance does not add isolation or secret-handling boundaries for experiments.
- Tool or platform assumptions: content is mostly host-neutral; root-host symlinks assume a filesystem that supports symlinks, but they were not imported.
- External dependencies: no runtime dependency; examples mention common deployment, database, and Python tooling.
- License or provenance concerns: MIT is explicit in root and frontmatter. The skill is a secondary framework based on a separately copyrighted book and includes an Amazon affiliate-tagged link; adaptation needs a wording/provenance review.
- Generated or low-quality material: the forced 10/10 score and broad trigger surface can produce performative audits instead of the requested narrow action.

## Initial Scope Recommendation

- Evaluate: the tracer-bullet versus prototype decision guide, iteration loop, and warning against confusing production and disposable code.
- Defer: DRY, contracts, broken windows, reversibility, estimation, and knowledge-portfolio references.
- Discard: the forced universal 10/10 score and affiliate link in any frozenSkillz-owned adaptation.
- Needs more evidence: live comparison of baseline, whole candidate, and a narrow frozenSkillz adaptation on a mid-build uncertainty where implementation must continue.
