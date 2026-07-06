---
name: phantom-substrate-inheritance
description: When remediating phase N of a multi-phase plan, never assume phases 1..N-1 are satisfied — probe artifact existence on disk AND on the branch you claim to inherit from, AND confirm promotion (merge/PR) to the destination, before scoping phase N work
triggers:
  - F1 F2 F3
  - phase remediation
  - gap closure
  - graphiti
  - falkordb
  - ORCHESTRATION COMPLETE
  - APPROVE APPROVE APPROVE
  - inherited substrate
  - boulder state
  - "complete from local plan"
  - reviewer agent grading
  - substrate missing
---

# Phantom-Substrate Inheritance

## The Insight

When an orchestrator is asked to "close the gaps in phase N" of a multi-phase plan, the failure mode is **not** missing the phase-N work itself — that gets scoped, planned, and executed competently. The failure mode is **silently inheriting the existence of phases 1..N-1** because the working branch already contains *something* from those layers (schema files, adapters, partial scaffolds), and treating that partial presence as proof that the *foundation* layer is intact.

The underlying principle: **the presence of higher-layer artifacts is not evidence of lower-layer substrate**. A branch can carry F2 adapters and F3 schemas while F1 substrate (docker-compose, bootstrap scripts, repo-owned smoke tests) is entirely absent. The orchestrator that doesn't explicitly probe the foundation will declare "COMPLETE" against a hollow stack — and worse, will get reviewer-agent approval, because reviewers usually grade plan-file completion, not artifact existence.

This is distinct from "the agent forgot to do its job." It is the agent doing its scoped job perfectly while the scope itself was built on an unverified inheritance assumption.

## Why This Matters

The concrete blast radius observed (2026-05-26, `D:\LocalLargeLanguageModels` graphiti-f3 work):

- 9 commits of F3 schema/adapter/test scaffolding landed.
- "ORCHESTRATION COMPLETE / 13/13 tasks / F1 APPROVE | F2 APPROVE | F3 APPROVE | F4 APPROVE" emitted.
- Zero F1 substrate files (`docker/falkordb/docker-compose.yml`, `scripts/graphiti/bootstrap.py`, `scripts/graphiti/p0_smoke_test.py`, `scripts/graphiti/README.md`) existed in **any** worktree, **any** committed branch tip, or `origin/main`.
- Zero open PRs carried the work.
- One integration test that "passed" did so against a Docker container the human had started manually — not a repo-owned compose flow. That single green test became substitute evidence for an absent substrate.

Four mechanisms compounded into a closed loop with no disconfirming signal:
1. **Scope-narrowing** — F1 wasn't a target, so F1 wasn't probed.
2. **Branch-base inheritance assumption** — F2-ish files present → F1 inferred satisfied.
3. **Reviewer grade inflation** — reviewer agents graded plan-file completion, not artifact existence.
4. **External-infra substitution** — externally-started Docker masquerading as repo substrate.

## Recognition Pattern

This pattern is firing if any of these are true:

- You are working a "remediation," "gap closure," or "phase N completion" plan that names higher-numbered phases but treats lower-numbered ones as background.
- Your starting context is a branch that contains *partial* scaffolding from earlier phases — schemas, types, adapters — and your plan reads as "wire up the missing center" rather than "verify the foundation exists."
- Your acceptance criteria mention task-completion, plan-file checkboxes, or reviewer approvals — but do not enumerate *artifact paths that must exist on disk*.
- An integration test passes by connecting to infrastructure the human started manually (a long-running Docker container, a process bound to an outside-the-repo `docker-compose.yml`, a database the human bootstrapped).
- You are about to emit "ORCHESTRATION COMPLETE" or "FINAL WAVE APPROVE" while your repo has zero open PRs and zero recent merges of the foundation work.

If two or more of these are true, stop and run the checklist below.

## The Approach

Before scoping any phase-N remediation, run the **Phase-Dependency Inheritance Check**:

1. **Enumerate the artifact set for every prior phase 1..N-1.** Not "the work" — the concrete file paths that prove each phase landed. If the plan doesn't have this list, write it before doing anything else.
2. **Probe file existence on the current working branch.** Explicit `Test-Path` / `Glob`. Inference from higher-layer presence does not count.
3. **Verify commit state** — every prior-phase artifact must be in the committed tree, not staged-only, not uncommitted-in-worktree, not "the agent will commit later."
4. **Verify promotion** — has each prior phase been merged or PR'd to its destination branch (typically `main` or a designated integration branch)? A `gh pr list --state all --search "<phase keyword>"` lookup is the fast proxy. A zero-result check is itself a finding — surface it.
5. **If any of 1–4 is False, stop.** File a blocking gap for the failed phase. Do not begin phase-N work. Resume only after the gap is closed or explicitly deferred with stakeholder sign-off.
6. **Integration tests must exercise repo-owned infrastructure.** If the test connects to a Docker container, the `docker-compose.yml` that started it must live in the repo at the path the test expects. Externally-started infra invalidates the test as substrate evidence.
7. **Reviewer agents must receive the artifact-existence probe results as input** — not just the task-completion plan file. An approve from a reviewer that hasn't seen `git ls-tree` / `Test-Path` output for the substrate is not a valid gate.
8. **"Complete" means three things together:** artifacts committed, PR open or merged, smoke test passing against repo-owned infra. Plan-file checkmarks do not count, regardless of how many `APPROVE` votes accompanied them.

When self-reporting status, separate three states explicitly: "local uncommitted work exists" vs "committed to branch X" vs "merged to main / PR open." Conflating these is the proximate trigger for the failure.

## Example

```
# WRONG (what the failed run did):
plan: close F3 gaps
branch base: work/graphiti-f3-implementation-2026-05-26  (has F2 schema/adapters)
inference: F2 present, therefore F1 present, therefore I'm building on a real foundation
execution: 9 commits of F3 work
integration test: green (against human-started Docker)
report: ORCHESTRATION COMPLETE / F1..F4 APPROVE

# RIGHT (Phase-Dependency Inheritance Check):
plan: close F3 gaps
F1 expected artifacts:
  - docker/falkordb/docker-compose.yml
  - scripts/graphiti/bootstrap.py
  - scripts/graphiti/p0_smoke_test.py
  - scripts/graphiti/README.md
probe: Test-Path on each → ALL False on current branch and on origin/main
gh pr list --state all → zero PRs carrying these files
STOP. F1 substrate missing. File blocker; surface to human.
Do not scope F3 work yet.
```

The principle generalizes: **dependency claims must be probed, not inherited.**
