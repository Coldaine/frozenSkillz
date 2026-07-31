# Technique: Charts and Analytical Graphics

Read in Phase 1 when writing the chart manifest, and in Phase 3 when building charts.

## The forcing function

For every chart, write ONE sentence stating the structure it reveals that a table cannot show as clearly. **If the sentence cannot be written, the chart is cut.** No exceptions. This is what keeps decorative charts out.

## Charts that carry a message

price versus performance; cost versus benchmark score; capacity versus power; capability versus price; Pareto-efficiency frontiers; performance across reasoning levels; throughput versus latency; historical pricing; feature coverage.

## Rules

- Preserve the underlying data points. Never replace a meaningful scatterplot with decorative score gauges.
- Distinguish, visibly and separately: efficient-frontier membership; overall recommendation; special-purpose recommendation; operational constraints. **A product may sit on a two-variable frontier without being the best practical choice**, and the deliverable must be able to say so.
- Annotate major jumps, outliers, and misleading comparisons directly on the chart.
- Avoid radar charts where a table or aligned bar comparison reads more easily.
- Do not collapse materially different variants into one label to make a chart tidier.
- Missing values are absent and annotated, never interpolated to complete a line or frontier.

## Benchmark and frontier views

Make the landscape visible rather than reporting isolated scores. Show all relevant candidates, variants and reasoning levels, cost assumptions, score assumptions, source or confidence, frontier status, and practical recommendation status. The reader should be able to see why one item dominates another.

## Decision matrices

Use when several dimensions matter. Show the dimensions explicitly rather than hiding them inside an unexplained aggregate. Ratings are anchored to written definitions, internally consistent, and accompanied by raw values where possible. Weighted scores are allowed only if component scores remain inspectable.
