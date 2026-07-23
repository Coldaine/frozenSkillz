# Forensic Evaluation: Brainstorming Against Real-Agent Evidence

## Claim

- Claim being evaluated: Superpowers `brainstorming` reliably establishes a safe, evidence-grounded
  design handoff across supported coding-agent harnesses.
- Candidate artifact: `source/skills/brainstorming/`
- Decision this finding informs: whether to adopt, adapt, defer, or discard the skill.

## Evidence Set

| Source | Type | Version/harness | Result |
|---|---|---|---|
| [Commit `7f2ee61`](https://github.com/obra/superpowers/commit/7f2ee614b6d65af34bd6b689f48f79f742a9d43c) | maintainer commit | pre-4.3 behavior, Claude | Agents skipped or collapsed the described process; hard gates added |
| [Issue #565](https://github.com/obra/superpowers/issues/565) | reproduction + maintainer confirmation | regression from `7f2ee61` | Review gate removed and plan/design paths collided; fixed |
| [Issue #1080](https://github.com/obra/superpowers/issues/1080) | source audit + one transcript summary | 5.0.7, Claude Code | Worktree skill was not invoked; support later rewritten |
| [Commits `cb5bb88`](https://github.com/obra/superpowers/commit/cb5bb885fd7cf00a1820f20d922df06ec02d4bed) and [`7fbae02`](https://github.com/obra/superpowers/commit/7fbae0252fe90778ce0c06fde3bf5f87aa396fc2) | code, security review, tests | companion before 6.1.1 | Missing auth and six named integration defects; fixed with regression coverage |
| [Issue #939](https://github.com/obra/superpowers/issues/939) | reproduction + workaround | 5.0.6, Claude Code | Concrete default path overrode project instruction; still structurally relevant |
| [Issue #1246](https://github.com/obra/superpowers/issues/1246) | multiple independent reports | Claude Code and Codex reports | Spec/plan commits on primary branch and excessive commit friction |
| [Issue #1266](https://github.com/obra/superpowers/issues/1266) | repeated-behavior report | unspecified | Recommendations changed after deeper analysis; no transcripts supplied |
| [Issue #1222](https://github.com/obra/superpowers/issues/1222) | cross-harness report | Pi, Codex, Claude Code | Over-triggering alleged; maintainer requested unavailable transcripts |
| [Issue #1100](https://github.com/obra/superpowers/issues/1100) | screenshot + confirmations | Codex app 5.0.7 era | Output intermittently collapsed and easy to miss |
| [Issue #975](https://github.com/obra/superpowers/issues/975) | source-confirmed behavior | companion | Persistent state placed under project `.superpowers/` |

## Assessment

- Status: mixed; several historical defects are fixed, while path, branch-ordering, evidence-rigor,
  state-location, over-triggering, and Codex-rendering concerns remain unresolved or unclear.
- Corroborating evidence: current v6.1.1 source, issue reproductions, maintainer comments, fix commits,
  and in-tree companion tests.
- Contradicting evidence: successful users and the project’s continued adoption show the workflow can
  be useful, but no evidence inspected here establishes universal reliability.
- Confidence: moderate.
- Supports: B- editorial grade, selective adaptation, continued forensic review.
- Does not support: a measured improvement claim, a current failure rate, or wholesale rejection.

## Reviewer Notes

The strongest evidence concerns specific regressions corroborated by fixes. Reports without
transcripts remain labeled limited. Historical defects inform maintenance quality but are not
counted as current defects when the pinned source contains the fix.
