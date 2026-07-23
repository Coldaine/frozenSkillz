# Route: EXPLAIN / SYNTHESIZE

**Fires when** the reader's task is to understand how a system, process, architecture, mechanism, or event works. Comparison is optional and often absent.

**Primary surface:** chosen in the plan and justified: annotated diagram, layered map, causal model, sequence walkthrough, or annotated narrative. State which and why.

**Read alongside:** techniques/relationship-grammar.md (mandatory), techniques/visual-thesis.md, techniques/semantic-scaling.md if the system exceeds one view, techniques/evidence.md.

## Choosing the primary surface

| If the content is... | Lead with |
|---|---|
| components and their connections | annotated architecture diagram |
| an ordered process across actors | sequence walkthrough with lanes |
| causes and effects | causal model; distinguish established from hypothesized links |
| layered abstraction (protocol, stack) | layered map with each layer's contract stated |
| a mechanism unfolding over time | annotated narrative with staged states |

## Considerations

- Structure, flow, and causality **are** the content. A matrix that flattens them into rows is a failure of the route, not a stylistic choice.
- The unit is what the reader reasons about (features, subsystems, decisions), not the raw entities the data arrived as (files, rows, log lines). Recorded correction: file-level exhibits were wrong; features were right.
- Every relationship uses the grammar; undifferentiated lines waste the diagram.
- Evidence layering still applies: what is documented about the system, what is observed, and what is inferred are visually distinct. Do not let a clean diagram imply certainty the sources do not support.
- Annotate the non-obvious: why a component exists, what breaks if it is removed, where the diagram simplifies.

## Conclusion form

Key mechanisms; load-bearing dependencies; what breaks the model; open questions about the system. Not a recommendation.

## Intermediates delta

plan.md: the primary-surface choice with justification, and the relationship channels in use with their meanings. The chart-manifest rule generalizes: for each diagram, one sentence stating what structure it reveals that prose cannot.

## Anti-patterns

- A component list styled as a diagram, with lines that mean nothing.
- Simplification that removes the difficulty the reader came for.
- Certainty implied by clean rendering.
