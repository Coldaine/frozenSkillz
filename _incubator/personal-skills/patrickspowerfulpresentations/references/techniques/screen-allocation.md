# Technique: Screen-Space Allocation

Read in Phase 3 for any multi-panel or wide-composition build.

"Wide desktop, no empty space" is necessary but not sufficient: a deliverable can satisfy it and still put small information on a large canvas.

## Density targets

Information density comes from strong grouping and typography, not smaller text. Useful anchor from dashboard research: roughly **4-7 visual groupings per screen**, each using one or two encoding channels, with clear hierarchy signaling what matters most. Many data points through position, length, and small multiples with consistent scales is good density; many different encoding types, colors, chart types, and interaction modes on one screen is noise.

## When information exceeds the viewport

- Side panels collapse and the main surface **reclaims** their space rather than leaving a gap where the panel was.
- Secondary analyses become tabbed drawers, not stacked scroll.
- Repeated objects aggregate (see semantic-scaling.md).
- Important labels persist; secondary prose disappears before metrics do.
- Representation changes rather than shrinking.
- Internal scroll inside a large table or panel is acceptable and preferable to breaking the page structure.
- Pagination, tabs, and detail pages beat endless scrolling.

## Layout stability

Layout stays stable across view switches. The reader's spatial memory is an asset; every reflow spends it. Where a view must reflow, animate the transition so the mapping between before and after is visible.

## Composition anti-patterns

- One narrow column of text centered in a large screen.
- Enlarged mobile layouts.
- A card per fact.
- Excessive padding that forces scrolling through sparse content.
- Oversized headings followed by little information.
- Dead regions left behind by collapsed panels.
