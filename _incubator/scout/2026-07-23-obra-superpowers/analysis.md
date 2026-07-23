# Analysis: obra/superpowers v6.1.1

## Scope

- Selected artifact: `skills/brainstorming/`.
- Reason: the operator requested a one-at-a-time doctree, intent, evidence, and letter-grade review.
- Out of scope for this pass: grades for the remaining 13 skills and any repo-wide adoption claim.

## Grade Meaning

Letter grades are evidence-backed editorial assessments, not unpublished benchmark results. Each
grade combines the frozenSkillz rubric, current source, documented real-agent behavior, maintenance
response, and unresolved risk. Confidence describes the evidence base supporting the grade.

## Review Status

| Artifact | Type | Rubric average | Letter grade | Confidence | Recommendation |
|---|---|---:|---:|---|---|
| `skills/brainstorming/` | skill | 4.0/5 | B- | moderate | Incubate; mine patterns only after the full review |

## `brainstorming`

### Intent and Doctree

The skill turns an idea into an approved design and written specification before planning or
implementation. Its required flow is context inspection, one-at-a-time clarification, alternative
comparison, incremental design approval, spec creation, self-review, written-spec review, and
handoff to `writing-plans`.

```text
brainstorming/
├── SKILL.md
├── spec-document-reviewer-prompt.md
├── visual-companion.md
└── scripts/
    ├── frame-template.html
    ├── helper.js
    ├── server.cjs
    ├── start-server.sh
    └── stop-server.sh
```

The support tree is not passive documentation. It includes an optional authenticated local
HTTP/WebSocket companion for diagrams and comparisons. It should start only after explicit consent
and only when a visual question would benefit from it.

### Rubric Scores

| Dimension | Score | Rationale |
|---|---:|---|
| Purpose clarity | 5 | Explicit design-before-implementation purpose |
| Activation or invocation clarity | 4 | Strong trigger, but its universal scope risks over-triggering |
| Output contract | 5 | Defines conversation, spec, review, and handoff artifacts |
| Reuse value | 4 | Broadly useful for substantial design work; heavy for bounded changes |
| Progressive disclosure or structure | 5 | Core workflow routes companion and review detail to support files |
| Safety/security risk | 4 | Companion is opt-in and hardened, but still adds a local service surface |
| Portability | 3 | Cross-harness prose exists; companion and helpers retain shell/runtime assumptions |
| Testability/evaluability | 4 | Server and trigger tests exist; behavior eval corpus is external to the release |
| Maintenance burden | 3 | Eight-file companion and cross-harness behavior require active maintenance |
| Fit with frozenSkillz scope | 4 | Directly relevant methodology, but not suitable for wholesale adoption yet |
| Trigger clarity | 4 | Creative-work trigger is unmistakable |
| Negative triggers | 2 | It explicitly rejects a small-task exemption instead of defining exclusions |
| Reference and template routing | 5 | Supporting material has clear entrypoints and conditional loading |
| Gate quality before action | 4 | Strong approval gates; branch/output-location ordering remains problematic |

Average: **4.0/5**. The letter grade is **B-**, rather than mapping mechanically to the numeric
average, because unresolved operational problems affect normal use in Codex and Git repositories.

### Forensic Findings

| Finding | Status | Confidence | Evidence |
|---|---|---|---|
| Models skipped design or collapsed it into one response before hard gates were added | fixed | moderate | [`7f2ee61`](https://github.com/obra/superpowers/commit/7f2ee614b6d65af34bd6b689f48f79f742a9d43c) describes three tested variants but publishes no result table |
| Written-spec review was skipped and planning could overwrite the design | fixed | strong | [#565](https://github.com/obra/superpowers/issues/565), maintainer confirmation, and [`ec3f7f1`](https://github.com/obra/superpowers/commit/ec3f7f1027a61629fc67270a9a5ccb21a432a194) |
| Brainstorming-to-worktree handoff was structurally inconsistent | historical | moderate | [#1080](https://github.com/obra/superpowers/issues/1080) includes a real session; maintainer says worktree support was rewritten in 5.1 |
| Companion initially exposed content/events without authentication and later integration contained real defects | fixed | strong | [`cb5bb88`](https://github.com/obra/superpowers/commit/cb5bb885fd7cf00a1820f20d922df06ec02d4bed) and [`7fbae02`](https://github.com/obra/superpowers/commit/7fbae0252fe90778ce0c06fde3bf5f87aa396fc2) with named regressions and test counts |
| Concrete default spec path can win over repository output-path instructions | unresolved | moderate | [#939](https://github.com/obra/superpowers/issues/939) has reproduction and workaround; v6.1.1 still places the concrete default before its override note |
| Spec commit can happen before a feature branch/worktree decision | unresolved | strong | Current flow says write and commit before handoff; [#1246](https://github.com/obra/superpowers/issues/1246) contains multiple independent reports |
| Recommendations may be shallow until challenged | unresolved | limited | [#1266](https://github.com/obra/superpowers/issues/1266) reports repeated flips but provides no transcripts |
| Skill may trigger too broadly | unresolved | limited | [#1222](https://github.com/obra/superpowers/issues/1222) names several harnesses but reporter could not provide transcripts |
| Codex can collapse outputs under `Worked for...` | unresolved | moderate | [#1100](https://github.com/obra/superpowers/issues/1100) includes screenshot evidence and multiple Codex confirmations |
| Persistent companion state defaults inside the project when `--project-dir` is used | current | strong | Current script and [#975](https://github.com/obra/superpowers/issues/975) agree on `.superpowers/brainstorm/` behavior |

### Assessment

The skill has a clear, valuable intent and a maintainership history that responds to concrete
failures. Its strongest elements are explicit approval gates, one-question-at-a-time clarification,
alternative comparison, and a written decision artifact.

It does not earn an A-range grade because the current contract remains overbroad, orders spec
commits before isolation decisions, gives a concrete output path more salience than repository
authority, and does not require an evidence basis before recommending an option. The optional
companion is substantially hardened but materially raises complexity and maintenance cost.

## Summary Recommendation

- Recommended outcome: incubate for later; do not import wholesale.
- Potential concepts to adapt: evidence-aware design gates, incremental user approval, and explicit
  separation between design and implementation planning.
- Open questions: review the remaining skills and determine whether the methodology works better as
  selected independent skills or as a tightly coupled suite.
