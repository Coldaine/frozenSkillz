# Artifact Rubrics

Score each applicable dimension from 1 to 5 and include a short rationale. Use `N/A` only when the dimension cannot structurally apply.

## Shared Dimensions

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Purpose clarity | Unclear or implied | Mostly clear | Explicit and narrow |
| Activation or invocation clarity | Hidden or ambiguous | Some triggers or usage notes | Clear trigger, command, lifecycle, or use case |
| Output contract | None | Partial expected output | Specific output shape and success criteria |
| Reuse value | One-off | Reusable with edits | Broadly reusable in frozenSkillz scope |
| Progressive disclosure or structure | Monolithic | Some separation | Lean entrypoint plus routed detail |
| Safety/security risk | High unmanaged risk | Known risks partially mitigated | Risks explicit and mitigated |
| Portability | Tool or OS locked without reason | Some portability gaps | Cross-tool or scoped honestly |
| Testability/evaluability | Cannot be tested | Manually inspectable | Repeatable eval or validation path |
| Maintenance burden | High or unclear | Moderate | Low, bounded, and documented |
| Fit with frozenSkillz scope | Out of scope | Adjacent | Directly supports reusable agent workflows |

## Artifact-Specific Dimensions

### skill

- Trigger clarity.
- Negative triggers.
- Reference and template routing.
- Gate quality before action.

### agent

- Role boundaries.
- Assumptions and constraints.
- Allowed tools or capabilities.
- Handoff contract and final response expectations.

### command

- Deterministic invocation.
- Side-effect clarity.
- Failure modes.
- Idempotence or rollback guidance.

### hook

- Lifecycle event clarity.
- Install and enablement risk.
- Failure passthrough behavior.
- Side effects and data exposure.

### config

- Schema clarity.
- Environment coupling.
- Secret risk.
- Safe defaults.

### template

- Specificity.
- Reusable variables.
- Output consistency.
- Examples or filled sample quality.

### eval-case

- Reproducibility.
- Scoring clarity.
- Baseline comparability.
- Stored inputs and outputs.

### documentation-pattern

- Authority flow.
- Self-enforcement.
- Drift resistance.
- Clear legal homes for overflow content.

## Recommendation Bands

- 4.5 to 5.0: Strong candidate for adaptation or active packaging.
- 3.5 to 4.4: Useful pattern, needs focused cleanup or eval proof.
- 2.5 to 3.4: Incubate or mine for small ideas only.
- 1.0 to 2.4: Discard unless a specific, low-risk fragment is valuable.
