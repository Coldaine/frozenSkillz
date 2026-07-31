# Route: BUYING

**Fires when** money will be spent on one of the options. Inherits everything from comparison.md and adds price discipline.

**Primary surface:** value analysis (price against capability), with the matrix immediately behind it.

**Read alongside:** domains/comparison.md, techniques/evidence.md (mandatory), techniques/charts.md.

## Additional mechanics

- Prices and availability are **search-verified at build time and timestamped on the page**. A price with no as-of date is a defect on this route.
- Where price varies by channel, condition, or region, show the range and the assumption, not a single number.
- Recurring costs, where they exist, are shown alongside acquisition cost; the reader is choosing a commitment, not a purchase.
- Availability is a first-class column: an option that cannot be bought is not a live option, and should be visibly marked rather than silently ranked.
- Used and refurbished options, where relevant, are their own rows with their own risk notes, not asterisks on the new-price row.

## Conclusion form

Four named calls, each with its reasoning visible: **default pick**, **best value**, **niche pick** (and the niche), and **explicit rejections with reasons**. What should be rejected and why is part of the deliverable, not an omission.

## Intermediates delta

dossier.md: every price entry carries its retrieval date and the channel it came from. verification.md gate G4 checks that no current-status claim rests on training data.

## Anti-patterns

- A recommendation with no rejections.
- Stale prices presented with the same confidence as verified ones.
- A frontier position presented as a purchase recommendation without checking practicality.
