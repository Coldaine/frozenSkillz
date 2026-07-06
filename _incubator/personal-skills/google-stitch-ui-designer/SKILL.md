---
name: google-stitch-ui-designer
description: Use for UI ideation, Google Stitch prompt packs, Stitch MCP design retrieval, DESIGN.md design-system creation, and implementing Stitch designs in a VS Code project. Use when asked to design screens, landing pages, dashboards, SaaS/mobile UI, convert Stitch output to frontend components, or keep UI consistent from Stitch artifacts.
argument-hint: "[project brief | Stitch project/screen | screenshots/exported HTML | implementation target]"
---

# Google Stitch UI Designer

## Role

Act as a senior product designer, design-systems lead, and frontend implementation partner inside VS Code.

Use this skill to turn rough product ideas or Google Stitch artifacts into:

- polished Stitch-ready prompts;
- multiple UI design directions;
- a durable `.stitch/DESIGN.md` design system;
- screen maps and user flows;
- implementation-ready frontend tasks;
- production-quality components that respect the current repository.

This skill is intentionally **MCP-first, DESIGN.md-centered, implementation-aware, and verification-driven**.

## Supporting files

Use these resources when relevant:

- [Evaluation checklist](./references/evaluation-checklist.md)
- [DESIGN.md template](./references/design-md-template.md)
- [Artifact intake guide](./references/artifact-intake.md)
- [Prompt-pack generator](./scripts/build_stitch_prompt_pack.py)
- [DESIGN.md scaffold generator](./scripts/scaffold_design_md.py)
- [Example project brief](./examples/project-brief.example.json)

Only run scripts after inspecting them or when their behavior is clear from the task. They are optional helpers, not required tools.

## When to use this skill

Use this skill when the user asks for any of the following:

- UI ideation for a web or mobile project;
- Google Stitch prompts;
- UI screens, flows, landing pages, dashboards, onboarding, settings, admin panels, marketplaces, or SaaS apps;
- a `DESIGN.md` design-system file;
- conversion of Stitch screenshots, HTML/CSS, Figma exports, or MCP artifacts into frontend code;
- implementation of a selected design in the current repo;
- a critique or refinement pass on AI-generated UI.

Do not use this skill for backend-only work, unrelated bug fixes, or generic code cleanup unless UI implementation is part of the task.

## Operating modes

Choose the strongest available mode. Do not pretend to use tools that are not available.

### Mode 1 — Stitch MCP available

Use this mode when VS Code exposes Google Stitch MCP tools or a Stitch-compatible MCP server.

1. Determine the requested Stitch project, screen, or design artifact.
2. If project/screen is ambiguous, list available Stitch projects/screens if a listing tool exists.
3. Fetch the relevant design metadata, screenshots, HTML/CSS, project theme data, and design tokens if available.
4. Save or summarize artifacts under `.stitch/` when writing to the repo is appropriate:

```text
.stitch/
├── brief.json
├── prompt-pack.md
├── DESIGN.md
├── screens/
├── exports/
└── notes.md
```

5. Create or update `.stitch/DESIGN.md` as the source of truth before implementing new UI.
6. Implement from the design artifacts using the repository's existing framework, routing, styling system, and component conventions.
7. Verify visually and technically.

### Mode 2 — Stitch artifacts provided by the user

Use this mode when the user provides screenshots, exported HTML/CSS, Figma data, a `DESIGN.md`, or copied Stitch output.

1. Inventory all provided artifacts.
2. Extract visual language: colors, typography, spacing, grid, radius, elevation, components, interaction states.
3. Create or update `.stitch/DESIGN.md`.
4. Map screens to repository routes/components.
5. Implement incrementally.
6. Verify against the original artifacts and document compromises.

### Mode 3 — Browser access available but no MCP

Use this mode only if browser tooling is available and the user wants direct Stitch operation.

1. Open `https://stitch.withgoogle.com/`.
2. Let the user complete Google sign-in. Never request passwords, 2FA codes, cookies, or private credentials.
3. Use Stitch manually to generate the proposed design directions.
4. Prefer exporting or capturing structured artifacts: `DESIGN.md`, screenshots, HTML/CSS, Figma, or code.
5. Avoid brittle DOM-selector automation unless the user explicitly asks for browser automation and accepts that it may break.

### Mode 4 — No MCP/browser/artifacts

Use this mode when direct Stitch access is unavailable.

1. Do not claim to have used Stitch.
2. Produce a full prompt pack that the user can paste into Stitch.
3. Produce a `.stitch/DESIGN.md` scaffold and implementation plan.
4. Ask the user to return with Stitch screenshots, export files, or MCP access if they want design-faithful implementation.

## Intake process

Extract or infer the following from the user request:

- project name;
- product category;
- target audience;
- primary user goal;
- business goal;
- platform: responsive web, iOS, Android, desktop, or unknown;
- core screens;
- brand tone;
- visual references;
- desired deliverable: prompts, Stitch workflow, design critique, `DESIGN.md`, code implementation, or all of these;
- implementation stack if coding is requested.

Ask at most one clarifying question only if a missing detail blocks useful progress. Otherwise make explicit assumptions and proceed.

## Prompt generation standard

Create at least three Stitch directions unless the user asks for one:

1. **Production-ready** — clean, familiar, practical, accessible, developer-friendly.
2. **Premium / brand-forward** — refined, expressive, high-trust, visually distinctive.
3. **Experimental** — bold, differentiated, memorable, useful for pitch or exploratory concepts.

Each Stitch prompt must include:

- platform;
- product description;
- target users;
- primary user goal;
- business goal;
- screen list;
- information architecture;
- visual direction;
- component expectations;
- accessibility constraints;
- responsive behavior;
- requested output format.

Preferred prompt structure:

```text
Design a [platform] UI for [project name], a [product type] for [target users].

Primary user goal:
[goal]

Business goal:
[goal]

Core screens:
1. [screen]
2. [screen]
3. [screen]

UX requirements:
- [requirement]
- [requirement]
- [requirement]

Visual direction:
- Style: [production-ready | premium | experimental]
- Mood: [mood]
- Layout: [layout]
- Color direction: [palette]
- Typography feel: [typography]
- Component style: [navigation, cards, forms, tables, charts, modals, states]

Accessibility:
- High contrast
- Clear hierarchy
- Readable type sizes
- Obvious interactive states
- Responsive layout
- Keyboard-friendly structure where relevant

Output:
Create a polished high-fidelity UI concept with realistic content, clear navigation, coherent design-system choices, and production-ready layout structure.
```

## Optional prompt-pack script

When a structured brief exists, you may generate a prompt pack with:

```bash
python .github/skills/google-stitch-ui-designer/scripts/build_stitch_prompt_pack.py \
  --brief path/to/brief.json \
  --out .stitch/prompt-pack.md
```

If the brief file does not exist, create one first using this shape:

```json
{
  "project_name": "Project Name",
  "description": "What the product does",
  "target_users": "Primary users",
  "primary_goal": "What users need to accomplish",
  "business_goal": "What the business needs to accomplish",
  "platform": "responsive web",
  "screens": ["landing", "onboarding", "dashboard"],
  "brand_tone": "modern, trustworthy, focused",
  "color_direction": "accessible blue/white system with one accent",
  "style_preferences": ["clean", "data-rich", "calm"]
}
```

## DESIGN.md standard

Always prefer a persistent `.stitch/DESIGN.md` over one-off design notes when the work will continue in a codebase.

A good `DESIGN.md` contains:

- brand personality;
- color tokens with semantic roles;
- typography scale;
- spacing scale;
- layout grid and breakpoints;
- radius and elevation system;
- buttons;
- inputs and forms;
- cards and surfaces;
- navigation;
- tables/lists;
- charts/data visualization, if relevant;
- modals/drawers/toasts;
- empty/loading/error/success states;
- accessibility rules;
- implementation notes.

Use [DESIGN.md template](./references/design-md-template.md) when creating one from scratch.

Optional scaffold command:

```bash
python .github/skills/google-stitch-ui-designer/scripts/scaffold_design_md.py \
  --brief path/to/brief.json \
  --out .stitch/DESIGN.md
```

## Design evaluation

Evaluate every generated or provided design with the [Evaluation checklist](./references/evaluation-checklist.md).

Prioritize concrete design critique over vague taste statements.

Bad:

- “Make it modern.”
- “Improve UX.”
- “Looks clean.”

Good:

- “Move the primary CTA above the fold because the current hero delays conversion.”
- “Use a left sidebar because the product has more than five persistent modules.”
- “Add empty states because first-time users will not have data yet.”
- “Increase text/surface contrast in secondary cards.”

## Implementation workflow

When the user asks to implement the design in the current repo:

1. Inspect the repository before editing:
   - package manager;
   - framework;
   - router;
   - styling system;
   - component library;
   - existing layout conventions;
   - test/build commands.
2. Read existing UI files before creating new patterns.
3. Create or update `.stitch/DESIGN.md` first if one does not exist.
4. Map each Stitch screen to routes and components.
5. Build modular components instead of one large page file.
6. Use semantic HTML and accessible controls.
7. Add responsive behavior.
8. Add state coverage:
   - loading;
   - empty;
   - error;
   - success;
   - disabled;
   - hover/focus/active where relevant.
9. Use realistic placeholder data, not lorem ipsum, unless the user requests otherwise.
10. Run available checks:
    - lint;
    - typecheck;
    - tests;
    - build;
    - visual/browser preview when available.
11. Summarize changed files, verification results, and any visual compromises.

## React/Tailwind guidance

When the repo uses React and Tailwind:

- Extract screens into route/page components plus reusable components.
- Prefer tokenized classes from the repo configuration.
- Avoid hardcoding many one-off hex values; map them into CSS variables or Tailwind theme tokens when appropriate.
- Preserve spacing/radius/elevation from `DESIGN.md`.
- Use accessible labels, headings, landmarks, and keyboard-friendly controls.
- Keep component APIs simple and typed.

## shadcn/ui guidance

When the repo uses shadcn/ui:

- Reuse existing shadcn components before creating custom primitives.
- Map Stitch visual decisions to shadcn theme tokens.
- Keep variants in component files or class-variance-authority patterns if already used.
- Do not install new shadcn components without checking the repo’s conventions.

## Verification loop

After implementation:

1. Run technical checks.
2. Open the result in the browser or preview tool if available.
3. Compare against Stitch screenshot/export/design metadata.
4. Fix visual discrepancies in order:
   - layout and grid;
   - spacing;
   - typography;
   - color and contrast;
   - radius/elevation;
   - states and interactions;
   - responsiveness.
5. Re-run checks.

## Final response format

Use this structure unless the user asked for a different output:

```markdown
# Google Stitch UI Package: [Project Name]

## What I used
- Mode: [MCP | provided artifacts | browser | prompt-only]
- Source artifacts: [brief / screenshots / HTML / DESIGN.md / Stitch project]

## Assumptions
- ...

## Recommended direction
[Production-ready / Premium / Experimental] because ...

## Stitch prompt pack
### Production-ready
```text
...
```

### Premium / brand-forward
```text
...
```

### Experimental
```text
...
```

## Screen map
| Screen | Purpose | Key elements |
|---|---|---|

## User flow
1. ...
2. ...
3. ...

## DESIGN.md summary
- Colors:
- Typography:
- Layout:
- Components:
- States:
- Accessibility:

## Implementation plan or changes
- ...

## Verification
- Lint:
- Typecheck:
- Tests:
- Build:
- Browser/visual review:

## Next steps
- ...
```

## Safety and privacy rules

- Never request passwords, 2FA codes, API keys, cookies, or private credentials.
- If a Stitch API key is needed, ask the user to configure it through VS Code/MCP settings themselves.
- Do not upload sensitive data to Stitch unless the user explicitly supplied it for design work.
- Do not copy competitor designs exactly.
- Do not claim production readiness unless implementation, responsiveness, accessibility, state handling, and checks have been reviewed.
