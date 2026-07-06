# Stitch Artifact Intake Guide

Use this guide when the user provides Stitch output or when a Stitch MCP server is available.

## Artifact priority

Prefer structured artifacts over screenshots when possible:

1. `DESIGN.md`
2. Stitch MCP metadata and project theme data
3. exported HTML/CSS
4. screenshots
5. Figma exports
6. copied natural-language summaries

## Intake checklist

For each artifact, capture:

- project name;
- screen name;
- screen purpose;
- route/component target;
- source file or MCP reference;
- design tokens;
- layout rules;
- interaction states;
- responsive requirements;
- implementation risks.

## Recommended `.stitch/notes.md` format

```markdown
# Stitch Artifact Notes

## Source

- Project:
- Screen:
- Artifact type:
- Date imported:

## Screens

| Screen | Purpose | Implementation target | Source artifact |
|---|---|---|---|

## Extracted design language

- Colors:
- Typography:
- Spacing:
- Radius:
- Elevation:
- Components:
- States:

## Implementation risks

- ...

## Visual verification checklist

- Layout:
- Spacing:
- Typography:
- Colors:
- Responsiveness:
- States:
```
