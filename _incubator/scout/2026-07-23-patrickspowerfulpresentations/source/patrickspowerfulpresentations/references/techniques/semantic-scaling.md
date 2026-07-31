# Technique: Semantic Scaling

Read when the deliverable has more information than one viewport can hold at one density: topology, explain, large comparisons, atlases. Not needed for a Tier 1 single-surface build.

## The core rule

**Do not merely shrink the same content. Change the representation according to available space and relevance.**

Geometric zoom magnifies. Semantic zoom changes what is shown. Google Maps is the canonical case: continents, then roads, then buildings and businesses, with qualitatively different representations at each level. Empirical support is real: SemTimeZoom found users significantly faster with semantic zoom than static visualization on complex tasks; ExplorViz demonstrated it for software at scale; Kyrix handles 100M+ points at sub-500ms with a tile-based approach.

## Render densities

Patrick's locked vocabulary (Orb/OmniLink, April 2026): store rich data always, render at the density the context needs.

| Density | Shows |
|---|---|
| micro | a dot or tick; identity and one state signal only |
| compact | name plus one or two decisive metrics |
| standard | the default row or node; name, key metrics, category, status |
| full | complete specifications, evidence, sources |
| atmospheric | the object rendered as its own visual environment; a profile page, a detail canvas |

Atmospheric is a mode, not a step on the ladder; a thing can be atmospheric without passing through full.

## Behaviors

- **Aggregate at distance.** Families instead of items; bundles instead of individual links; a summary badge instead of the suppressed detail it stands for.
- **Expand as space or focus permits.** Groups open into members; bundles split into individual links; the badge is replaced by the metrics it summarized.
- **Preserve spatial position** across scale changes. The reader builds a map; do not reset it. Layout stability across view switches is an asset.
- **Dim, do not delete, unrelated context.** Focus+context beats focus-only: fisheye and degree-of-interest approaches (DOI as a function of importance and distance from focus) measurably speed tasks when information scent is strong.
- **Retain summary badges when detail is suppressed.** The reader should know something is there, not discover its absence later.

## Applied to a comparison atlas

| Scale | Representation |
|---|---|
| far | product families and the dominant tradeoff axis |
| default | individual products with key metrics |
| focused | full specifications and evidence |
| deep | methodology and source-level information |

## Applied to a system map

| Scale | Representation |
|---|---|
| overview | zones or tiers; bundled relationships; aggregate health |
| operational | services or hosts; typed edges; capacity |
| device | individual nodes; ports, drives, interfaces |
| flow | a single path traced through the system, everything else dimmed |

## Anti-patterns

- One fixed representation that only changes size.
- Zoom that reveals nothing new; magnification masquerading as depth.
- Positions that reshuffle on every scale change.
- Deleting context instead of dimming it, so the reader loses their place.
