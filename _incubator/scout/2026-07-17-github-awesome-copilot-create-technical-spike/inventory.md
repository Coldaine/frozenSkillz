# Inventory: GitHub awesome-copilot create-technical-spike

## Provenance

- Source URL: https://github.com/github/awesome-copilot
- Commit or version: cf04ddde790008b3cf01dcdbb1f7213cd6e55a71
- Import date: 2026-07-17
- License: MIT; source/LICENSE
- Reviewer: Codex planning_skill_intake
- Scout path: _incubator/scout/2026-07-17-github-awesome-copilot-create-technical-spike

## Artifact Counts

| Type | Count | Notable paths |
|---|---:|---|
| skill | 1 | source/skills/create-technical-spike/SKILL.md |
| agent | 0 | — |
| command | 0 | — |
| hook | 0 | — |
| config | 0 | — |
| template | 0 | The skill embeds one Markdown spike template rather than routing to a separate template file. |
| eval-case | 0 | No upstream eval artifact; one frozenSkillz eval definition exists outside source. |
| documentation-pattern | 0 | — |

## Risks

- Secret surfaces: none named, but the skill does not define secret-reading or data-handling boundaries.
- Tool or platform assumptions: GitHub Copilot/VS Code-style input interpolation and named search/searchResults, fetch/githubRepo, codebase, runTasks, editFiles, and vscodeAPI tools.
- External dependencies: filesystem access, web/repository research, and optional prototype execution.
- License or provenance concerns: root MIT license is explicit and preserved; no scoped license ambiguity observed.
- Generated or low-quality material: the large embedded template can encourage document creation before the cheapest investigation is known.

## Initial Scope Recommendation

- Evaluate: the one-question, time-boxed research sequence and the distinction between research, prototype, decision, and follow-up.
- Defer: the embedded document schema and status-history ceremony until a live eval shows they help rather than delay action.
- Discard: host-specific tool names and unresolved input interpolation in any frozenSkillz-owned adaptation.
- Needs more evidence: a three-variant live eval against a real technical unknown, including elapsed effort and whether implementation continued in parallel.
