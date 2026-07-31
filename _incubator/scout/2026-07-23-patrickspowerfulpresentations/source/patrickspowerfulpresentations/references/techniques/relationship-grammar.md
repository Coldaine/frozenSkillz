# Technique: Relationship Grammar

Read for explain, topology, and any deliverable containing diagrams. Optional pattern elsewhere.

## The principle

**Relationships themselves carry information.** A line that means only "connected" wastes every channel it has.

## The channels

| Channel | Carries |
|---|---|
| Color | relationship type or medium |
| Width | capacity or importance |
| Dash | certainty, or installation / completion state |
| Opacity | relevance to current focus |
| Badge | a measurement on the link |
| Halo | selection, or active route |
| Direction | flow |
| Bundling | summarized relationships at distant scale |

Encoded meaning must be discoverable in place, not only in a corner key; the self-explanatory-label rule applies to encodings.

## Layout channels (what the arrangement itself asserts)

- **Reading axis.** The dominant direction is never neutral. Left-to-right commonly reads as flow or time; top-to-bottom as hierarchy or priority. Decide what it asserts and keep it consistent; an ambiguous axis means the reader invents a meaning, usually wrong.
- **Adjacency and proximity.** Nearness reads as kinship even with no line drawn. Good for soft grouping; bad for precise relationships, which need a line or a label.
- **Containment and nesting.** The strongest statement of "part of" or "scoped within." Good for membership and boundaries; bad for sequence, since containers are about inside/outside, not before/after.
- **Size.** Magnitude, importance, volume, frequency; ranked pre-attentively.
- **Alignment and negative space.** Isolation reads as importance; a clean grid makes the reader trust the diagram. If the point is that one region is crowded and another sparse, that must be the actual layout, not faked with spacing.

## Layout families worth knowing

| Family | Use when | Fails when |
|---|---|---|
| Node-link | relationships are few enough to trace individually | hairball territory; dozens of crossing edges |
| Hierarchical edge bundling | many edges between grouped nodes; package-level patterns matter | individual edge identity matters |
| Dependency structure matrix | edge count defeats node-link; direction matters | reader needs spatial intuition |
| BioFabric (nodes as lines, edges as verticals) | overlap must be impossible by construction | audience is unfamiliar with the idiom |
| Layered flow / Sankey | throughput or magnitude along a path | relationships are not flows |
| Linked multi-panel | one subject, several coordinated views (tree + map + chart, hover syncs all) | panels do not genuinely share a subject |
| Timeline tracks | hierarchical events over time | no temporal dimension |

Treemaps: only worth it above roughly a thousand leaf nodes; below that, simpler representations win.

## Anti-patterns

- Undifferentiated lines in a diagram whose whole point is that the connections differ.
- A legend that is the only place encodings are explained.
- Curved organic layouts that destroy an informative layered structure.
- Animation on edges that encodes nothing.
