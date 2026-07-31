# Visual Style Brief for Presenting Research and Comparisons

(Patrick's authored brief, preserved as written. Addenda from past-chat corrections at the end.)

## Core objective

* Present complex information as a **rich, explorable visual document**.
* The artifact should feel closer to:

  * an interactive research report;
  * a technical magazine feature;
  * a consulting decision brief;
  * a product comparison atlas;
  * a benchmark explorer;
  * an annotated visual essay.
* It does not need to look or behave like an operational dashboard.
* Dashboard ideas such as compact summaries, hover detail, filters, and coordinated views may be used where they improve comprehension.
* The purpose is to help the reader **understand the information**, compare alternatives, inspect evidence, and form conclusions.

## Information-first presentation

* Start from the information that needs to be communicated, not from a standard page template.
* Present the evidence clearly enough that the reader can reason from it.
* Do not replace useful information with an oversimplified recommendation.
* Do not perform so much synthesis that the underlying comparison disappears.
* Show:

  * meaningful specifications;
  * capabilities;
  * prices;
  * performance;
  * tradeoffs;
  * uncertainty;
  * evidence quality;
  * important caveats.
* Separate:

  * raw facts;
  * derived metrics;
  * interpretation;
  * recommendations.

## Artifact structure

* Prefer **multiple distinct pages or workspaces** over one continuous scroll.
* Each page should answer a specific class of question.
* Good page types include:

  * Overview;
  * Market or option landscape;
  * Detailed comparison;
  * Benchmark frontier;
  * Product or model profiles;
  * Pricing and value;
  * Capability matrix;
  * Risks and limitations;
  * Recommendations;
  * Sources and methodology.
* Pages should feel substantial and purpose-built, not like sections of one long landing page.
* Navigation should make it easy to move directly to the desired analysis.

## Wide desktop composition

* Design primarily for a wide desktop display.
* Use horizontal space for:

  * side-by-side comparisons;
  * matrices;
  * large charts;
  * dense rows;
  * evidence panels;
  * visual profiles.
* Avoid layouts that look like enlarged mobile pages.
* Avoid placing one narrow column of text in the center of a large screen.
* Use the available viewport instead of shrinking information into tiny cards surrounded by empty space.
* Internal scrolling inside a large table or panel is acceptable when it preserves the overall page structure.
* Pagination, tabs, and detail pages are preferable to endless scrolling.

## High information density

* Show a lot of useful information at once, but organize it deliberately.
* Prefer:

  * dense comparison rows;
  * compact specification blocks;
  * sortable tables;
  * feature matrices;
  * small multiples;
  * score strips;
  * benchmark plots;
  * annotated diagrams;
  * structured callouts.
* Avoid one large card for every individual fact.
* Avoid excessive padding that forces the reader to scroll through sparse content.
* Information density should come from strong grouping and typography, not merely smaller text.

## Comparison as the primary visual language

* When presenting alternatives, make comparison direct and explicit.
* Place comparable information in the same visual position.
* Use consistent dimensions across options.
* Support:

  * side-by-side comparison;
  * sortable comparison rows;
  * highlighted differences;
  * filters;
  * grouping by class or price tier;
  * elimination based on constraints;
  * comparisons against a reference product.
* Do not make the reader open five separate product pages and remember the differences.
* Profiles may provide depth, but a shared comparison surface should remain available.

## Charts and analytical graphics

* Use charts when they reveal structure that tables cannot show as clearly.
* Charts should carry a specific analytical message.
* Good examples include:

  * price versus performance;
  * cost versus benchmark score;
  * capacity versus power;
  * capability versus price;
  * Pareto-efficiency frontiers;
  * performance across reasoning levels;
  * throughput versus latency;
  * historical pricing;
  * feature coverage.
* Preserve the underlying data points.
* Do not replace a meaningful scatterplot with decorative score gauges.
* Clearly distinguish:

  * efficient frontier membership;
  * overall recommendation;
  * special-purpose recommendation;
  * operational constraints.
* A product may be on a two-variable frontier without being the best practical choice.

## Benchmark and frontier views

* For model or hardware comparisons, make the benchmark landscape visible rather than reporting isolated scores.
* Show:

  * all relevant candidates;
  * variants and reasoning levels;
  * cost assumptions;
  * score assumptions;
  * source or confidence;
  * frontier status;
  * practical recommendation status.
* Allow the reader to understand why one item dominates another.
* Avoid collapsing materially different variants into one product label.
* Use annotations to explain major jumps, outliers, and misleading comparisons.

## Rich visual profiles

* Each major option may have a dense profile card or detail page.
* A useful profile can include:

  * image or recognizable silhouette;
  * price;
  * primary role;
  * standout strengths;
  * principal limitations;
  * important specifications;
  * benchmark summary;
  * fit by use case;
  * source quality;
  * recommendation status.
* These should not all be identical generic cards.
* Adapt the visual form to the subject:

  * hardware may show ports, drives, dimensions, and topology;
  * models may show benchmark bands, cost, context, and tool-use capability;
  * software may show architecture, workflow, integration, and maintenance status.

## Progressive detail

* Important information should be visible without interaction.
* Hover and click should provide more detail, not rescue an otherwise empty interface.

### At rest

* Show the information needed for rapid scanning and comparison.
* Preserve names, key metrics, category, recommendation status, and major limitations.

### On hover

* Reveal:

  * exact values;
  * methodology;
  * source notes;
  * secondary specifications;
  * definitions;
  * explanations of unusual ratings;
  * expanded visual detail.
* Use structured hover panels rather than tiny generic tooltips.

### On click

* Open a substantial detail page, comparison drawer, or pinned inspector.
* Maintain the surrounding context when useful.
* Allow direct comparison with neighboring alternatives.

## Recommendations

* Recommendations should be opinionated but visibly grounded.
* State:

  * the default recommendation;
  * the best value;
  * the strongest overall option;
  * the appropriate niche option;
  * what should be rejected and why.
* Avoid producing a long list of theoretically valid possibilities without making choices.
* Do not make recommendations so aggressively that the reader loses access to the underlying evidence.
* The ideal structure is:

```text
Evidence
→ visible tradeoffs
→ clear interpretation
→ opinionated recommendation
```

## Decision matrices

* Use decision matrices when several dimensions matter.
* Show the dimensions explicitly rather than hiding them inside an unexplained aggregate score.
* Ratings should be:

  * anchored to definitions;
  * internally consistent;
  * accompanied by raw values where possible.
* Weighted scores may be useful, but the user should still be able to inspect the component scores.
* Avoid radar charts when a table or aligned bar comparison is easier to read.

## Callouts and annotation

* Use callouts to direct attention to important structural insights.
* Good callouts explain:

  * why an option is unusual;
  * which feature changes the decision;
  * where a comparison is misleading;
  * why a product is not in the same class;
  * what a benchmark fails to capture;
  * which constraint dominates the result.
* Callouts should be attached to the relevant visual evidence.
* Prefer several precise annotations over one generic summary box.

## Visual richness

* Rich styling is welcome when it improves comprehension and makes the artifact engaging.
* Suitable techniques include:

  * strong colored borders;
  * meaningful background treatments;
  * silhouettes or product imagery;
  * diagrammatic components;
  * mini charts;
  * subtle depth;
  * editorial typography;
  * visual grouping;
  * layered annotations.
* Avoid making every element the same rounded dark card.
* Avoid generic neon SaaS styling unless the subject genuinely calls for it.
* Different information types should have different visual treatments.

## Images and diagrams

* Use images when they help the reader understand:

  * physical form;
  * scale;
  * port layout;
  * product family;
  * industrial design;
  * installation constraints.
* Use diagrams when relationships or architecture matter.
* Annotate images when the important information is not self-evident.
* Do not add decorative images that consume space without adding information.
* Prefer custom visual explanations over stock illustration.

## Tables

* Tables should be dense, sortable, and designed for comparison.
* Freeze important columns where appropriate.
* Use:

  * grouped headers;
  * inline bars;
  * icons;
  * color coding;
  * difference highlighting;
  * expandable rows.
* Keep important distinctions visible without requiring horizontal memory.
* Provide clear units and definitions.
* Do not hide most specifications behind repeated "view more" controls.

## Sources and evidence

* Make sourcing visible without overwhelming the main presentation.
* Support:

  * inline source indicators;
  * hover citations;
  * methodology panels;
  * source-quality labels;
  * a dedicated sources page.
* Clearly mark:

  * measured values;
  * manufacturer claims;
  * community reports;
  * estimates;
  * inferred values;
  * unknowns.
* Conflicting evidence should be shown rather than silently flattened into one confident number.

## Interaction

* Interaction should help the reader explore the information.
* Useful interactions include:

  * sorting;
  * filtering;
  * search;
  * highlighting differences;
  * selecting a reference item;
  * changing comparison dimensions;
  * switching between chart and table views;
  * revealing deeper context on hover;
  * pinning details;
  * saving or sharing a comparison.
* Avoid interactions that merely add animation.
* The artifact should remain understandable in its initial state.

## Navigation

* Prefer clear, explicit navigation.
* Good patterns include:

  * tabs;
  * page navigation;
  * an atlas or index page;
  * a persistent comparison tray;
  * breadcrumbs;
  * linked profiles.
* The reader should always understand:

  * where they are;
  * what question the page answers;
  * where deeper information lives;
  * how to return to the comparison.

## Tone and visual personality

* The artifact should feel:

  * intelligent;
  * researched;
  * specific;
  * visually ambitious;
  * authoritative without pretending certainty;
  * professional without becoming sterile.
* It may be dramatic or beautiful, but should remain information-led.
* Avoid both extremes:

  * plain document formatting with no visual thinking;
  * flashy interface styling with little substantive information.

## Common preferred artifact types

* Product comparison atlas
* Hardware buying guide
* Model benchmark frontier
* Research landscape
* Technical architecture explainer
* Market or tooling survey
* Decision brief
* Capability matrix
* Pricing and value analysis
* Visual implementation playbook

## Anti-patterns

Avoid:

* long single-page scrolling reports;
* sparse card grids;
* mobile-first narrow columns on desktop;
* one generic template applied to every subject;
* oversized headings followed by little information;
* recommendation lists without comparison evidence;
* charts that hide the underlying data;
* unexplained scores;
* excessive summary that removes nuance;
* decorative dashboards with no real operational purpose;
* interfaces that require hovering over everything to learn anything;
* making the reader repeatedly open and close isolated detail pages;
* generic "pros and cons" cards where a structured comparison would be clearer;
* presenting fundamentally different products as though they belong in one class;
* doing so much decision-making for the reader that the useful information is no longer visible.

## Acceptance questions

At a glance, can the reader determine:

* What options exist?
* Which options are genuinely comparable?
* What are the key dimensions?
* Where are the major tradeoffs?
* What is unusually strong or weak?
* What does each option cost?
* Which claims are measured versus inferred?
* What is recommended, and why?

With interaction, can the reader:

* inspect exact values;
* see sources;
* understand rating logic;
* compare selected items;
* change the comparison basis;
* explore edge cases;
* open a detailed profile without losing the broader context?

If not, the presentation is probably either too sparse, too linear, or too focused on summarizing conclusions instead of presenting the underlying information.

---

# Addenda: where the rest of the doctrine lives

Everything above is Patrick's authored brief, verbatim. The corrections and techniques that used to be appended here now live in dedicated files, so there is one source of truth per rule:

| Rule | File |
|---|---|
| Evidence tiers, unknowns, conflicts, no fabricated data, completion claims | `techniques/evidence.md` |
| Visual thesis, reference verification, the five design languages, aesthetic direction | `techniques/visual-thesis.md` |
| Semantic scaling, render densities, scale ladders | `techniques/semantic-scaling.md` |
| Screen-space allocation, density targets, layout stability | `techniques/screen-allocation.md` |
| Relationship grammar, layout channels and families | `techniques/relationship-grammar.md` |
| Chart manifest rule, frontier vs practical, decision matrices | `techniques/charts.md` |
| Actionability test, gates, rubric, test set | `evaluation.md` and `intermediates.md` (verification schema) |
| Non-comparable classes | `domains/comparison.md` |
| Revision protocol, interactivity honesty, unit of analysis, no em dashes | `SKILL.md` phases 1, 3, and 6 |

**Precedence:** this brief was written comparison-first. Its matrix-centric passages apply on the comparison and buying routes; on research, explain, topology, plans/results, and narrative, the route file in `domains/` governs which surface leads. `techniques/evidence.md` outranks everything here.
