# Google Stitch UI Evaluation Checklist

Use this checklist for every Stitch-generated, user-provided, or implemented UI.

## Product fit

- Is the primary user goal obvious within the first few seconds?
- Does the first screen explain who the product is for?
- Does the UI support the business goal without hiding the user goal?
- Is the level of polish appropriate for the audience?
- Does the design feel differentiated enough without harming usability?

## Information architecture

- Are primary and secondary actions distinct?
- Is navigation scalable for the number of modules?
- Are screens connected in a logical user flow?
- Are detail screens, settings, and success states accounted for?
- Are first-run and returning-user states considered?

## Visual hierarchy

- Are headings, supporting copy, controls, and data grouped clearly?
- Is spacing consistent?
- Are important elements visually prioritized?
- Are cards, rows, tables, and forms aligned?
- Is density appropriate for consumer, prosumer, or enterprise use?

## Components

- Buttons: clear variants, states, and sizes.
- Inputs: labels, help text, errors, disabled states.
- Cards: consistent padding, radius, borders, shadows.
- Navigation: clear active states and responsive behavior.
- Tables/lists: readable, sortable/filterable where needed.
- Modals/drawers: purposeful, accessible, dismissible.
- Charts: labeled, readable, not decorative-only.

## Accessibility

- Text contrast appears sufficient.
- Body text is readable.
- Touch targets are large enough on mobile.
- Interactive elements are obvious without relying only on color.
- Focus states are visible.
- Form fields have labels.
- Error states explain how to recover.

## Implementation feasibility

- Can this be built with the repo’s current stack?
- Does it require a new component library?
- Are token decisions clear enough to encode?
- Are responsive breakpoints obvious?
- Are image/icon dependencies identified?
- Are loading, empty, error, and success states defined?

## Review language

Prefer concrete critique:

- “Increase card header/body contrast because metric cards currently scan as one block.”
- “Move filters above the results list because filtering is the main task.”
- “Convert the top nav to a left nav because the app has many persistent workspaces.”
- “Add an empty state because new users will not have reports yet.”

Avoid vague critique:

- “Make it pop.”
- “Modernize it.”
- “Improve the UI.”
