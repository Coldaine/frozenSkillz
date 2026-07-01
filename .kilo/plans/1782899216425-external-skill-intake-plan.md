# External Skill Intake Active Skill Plan

## Goal

Create an implementation-ready, active workflow for evaluating external skill/plugin/agent repos without dumping them into active marketplace content. The outcome is a loadable `external-skill-intake` skill plus repo documentation that routes agents through a scoped, sandboxed, evaluatable workflow.

## Current Context

- `main` is protected enough for this work; no branch-protection changes are in scope.
- Current working tree already contains earlier uncommitted edits to `CLAUDE.md` and a new `AGENTS.md`. Treat these as draft context, not as final shape.
- Existing source docs:
  - `docs/skill-corpus-analysis/corpus-intake-rubric.md`
  - `docs/skill-corpus-analysis/corpus-analysis-deliverables.md`
  - `docs/skill-review/tracker.md`
  - `_incubator/scout/2026-06-25-project-docs-self-enforcing/`
- The current intake rubric is `SKILL.md`-centric and does not cover large plugin repos with agents, hooks, configs, eval cases, or templates.

## Decisions

- New active skill name: `external-skill-intake`.
- Put the detailed workflow in `docs/workflows/external-skill-intake.md`.
- Keep `AGENTS.md` as a lean router, not a long workflow container.
- Keep `CLAUDE.md` as a human quickstart/router.
- Do not import external repos into `plugins/` directly.
- Scout snapshots stay read-only under `_incubator/scout/<date>-<repo>/source/`.
- Mined ideas go first to scout analysis files and `extracted-patterns/`, not active plugin content.
- The active skill v1 should be references/templates first, not script-heavy.
- No branch-protection changes.

## Target Files

Create:

- `docs/workflows/external-skill-intake.md`
- `plugins/frozen-skills/skills/external-skill-intake/SKILL.md`
- `plugins/frozen-skills/skills/external-skill-intake/references/artifact-rubrics.md`
- `plugins/frozen-skills/skills/external-skill-intake/references/scout-sandbox-layout.md`
- `plugins/frozen-skills/skills/external-skill-intake/references/live-eval-protocol.md`
- `plugins/frozen-skills/skills/external-skill-intake/references/packaging-decision-gate.md`
- `plugins/frozen-skills/skills/external-skill-intake/templates/inventory.md`
- `plugins/frozen-skills/skills/external-skill-intake/templates/analysis.md`
- `plugins/frozen-skills/skills/external-skill-intake/templates/eval-case.md`
- `plugins/frozen-skills/skills/external-skill-intake/templates/decision-log.md`

Update as needed:

- `AGENTS.md`
- `CLAUDE.md`
- `README.md`
- `docs/skill-review/tracker.md`
- `plugins/frozen-skills/.claude-plugin/plugin.json`
- `plugins/frozen-skills/.codex-plugin/plugin.json`
- `plugins/frozen-skills/.cursor-plugin/plugin.json`
- `plugins/frozen-skills/gemini-extension.json`
- Root marketplace catalogs only if they mirror plugin version or skill metadata.

## Implementation Tasks

1. Create a feature branch from `main`.
2. Inspect `git diff` first and preserve any existing user/agent changes.
3. Rework repository docs:
   - `CLAUDE.md`: concise human quickstart, points agents to `AGENTS.md`.
   - `AGENTS.md`: concise agent router that points to `docs/workflows/external-skill-intake.md`, `docs/skill-review/tracker.md`, and the active skill.
   - `README.md`: remove stale `skill-classifier` naming, clarify gated vs active status, point external intake work to the workflow doc.
4. Add `docs/workflows/external-skill-intake.md` with the full workflow:
   - snapshot
   - inventory
   - scope selection
   - artifact-specific rubric scoring
   - sandboxed live evals
   - decision log
   - promotion or discard path
5. Add the active skill at `plugins/frozen-skills/skills/external-skill-intake/`.
6. Keep `SKILL.md` lean:
   - trigger/negative trigger
   - required workflow order
   - links to references/templates
   - clear rule: do not promote directly from scout source.
7. Add artifact-specific rubrics covering:
   - `skill`
   - `agent`
   - `command`
   - `hook`
   - `config`
   - `template`
   - `eval-case`
   - `documentation-pattern`
8. Add sandbox layout guidance:
   - `_incubator/scout/<YYYY-MM-DD>-<repo>/README.md`
   - `source/`
   - `inventory.md`
   - `analysis.md`
   - `decisions.md`
   - `evals/cases/`
   - `evals/runs/`
   - `extracted-patterns/`
9. Add live eval protocol:
   - define baseline output without candidate material
   - define candidate-inspired output
   - define frozenSkillz-adapted output
   - score outputs with repeatable criteria
   - require prompts, inputs, outputs, and scorer notes to be persisted under `evals/runs/`
10. Add packaging decision gate:
   - whole import
   - adapt concept only
   - merge into existing skill
   - incubate for later
   - discard
   - require rationale and affected paths for every decision.
11. Register the new skill in all `frozen-skills` plugin manifests.
12. Bump the `frozen-skills` plugin version consistently across plugin manifests.
13. Update `docs/skill-review/tracker.md` so `external-skill-intake` is listed as active or newly promoted, and note that it is the workflow for evaluating external inspiration repos.
14. Validate manifests and docs.
15. Open a PR against `main`.

## Rubric Requirements

Each artifact rubric should score 1-5 and include a short rationale. Use `N/A` only where the dimension is structurally inapplicable.

Minimum shared dimensions:

- Purpose clarity
- Activation or invocation clarity
- Output contract
- Reuse value
- Progressive disclosure or structure
- Safety/security risk
- Portability
- Testability/evaluability
- Maintenance burden
- Fit with frozenSkillz scope

Additional dimensions by artifact type:

- `skill`: trigger clarity, negative triggers, references, gate quality
- `agent`: role boundaries, assumptions, allowed tools, handoff contract
- `command`: deterministic invocation, side effects, failure modes
- `hook`: lifecycle event, install risk, failure passthrough, side effects
- `config`: schema clarity, environment coupling, secret risk
- `template`: specificity, reusable variables, output consistency
- `eval-case`: reproducibility, scoring clarity, baseline comparability
- `documentation-pattern`: authority flow, self-enforcement, drift resistance

## Live Eval Protocol

For candidate repos like `solutions-architect-skills`, run at least one eval case before recommending promotion of any large pattern.

Each eval case should include:

- user task prompt
- target artifact(s)
- baseline instructions
- candidate-inspired instructions
- frozenSkillz-adapted instructions
- expected output contract
- scoring rubric
- stored outputs
- final scorer notes

Do not claim a candidate improves outcomes unless eval outputs are persisted and scored.

## Validation

Run the appropriate checks after implementation:

- `git diff --check`
- Parse changed JSON manifests with PowerShell `ConvertFrom-Json`.
- `python scripts/validate_manifests.py`
- Verify every manifest `skills[].path` exists.
- Read the new `SKILL.md` and confirm it is lean and routes to references/templates.
- Confirm `AGENTS.md` is a router, not a long duplicated workflow.
- Confirm `CLAUDE.md` still works as a human quickstart.
- Confirm no scout source files were promoted directly.

## Risks And Guardrails

- Risk: recreating a junk drawer. Guardrail: source is read-only; every promotion requires inventory, analysis, eval, and decision log.
- Risk: rubric bloat. Guardrail: artifact rubrics must be concise and scoring-oriented.
- Risk: AGENTS.md becoming a second workflow manual. Guardrail: route to `docs/workflows/external-skill-intake.md`.
- Risk: importing Claude-only artifacts into a cross-platform marketplace. Guardrail: packaging decision gate must record platform scope honestly.
- Risk: scripts added before workflow proves useful. Guardrail: v1 is references/templates only unless repeated manual pain is observed.

## Review Checklist

Before PR is ready:

- New skill is active in manifests.
- Workflow handles non-`SKILL.md` artifacts.
- Sandbox layout is explicit.
- Live eval protocol is explicit enough for another agent to execute.
- Documentation no longer says `skill-classifier` where it should say `skill-injector`.
- Tracker reflects the new active intake skill.
- No unrelated scout source files are modified.

## Out Of Scope

- Changing GitHub branch protection.
- Cloning or evaluating `solutions-architect-skills` itself.
- Adding automation scripts for v1.
- Creating Linear issues unless explicitly requested in the implementation session.
