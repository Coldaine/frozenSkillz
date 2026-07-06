#!/usr/bin/env python3
"""Build a Google Stitch prompt pack from a structured project brief.

Usage:
    python build_stitch_prompt_pack.py --brief brief.json --out .stitch/prompt-pack.md

The script has no third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import dedent

DIRECTIONS = [
    {
        "name": "Production-ready",
        "slug": "production-ready",
        "style": "clean, familiar, accessible, developer-friendly, practical, conversion-aware",
        "layout": "clear navigation, predictable sections, strong hierarchy, reusable components",
    },
    {
        "name": "Premium / brand-forward",
        "slug": "premium-brand-forward",
        "style": "refined, high-trust, polished, expressive, differentiated without becoming confusing",
        "layout": "more visual rhythm, stronger brand moments, richer cards, carefully controlled whitespace",
    },
    {
        "name": "Experimental",
        "slug": "experimental",
        "style": "bold, memorable, concept-forward, high-contrast, differentiated, suitable for exploration or pitch use",
        "layout": "less conventional composition, distinctive hero structure, expressive visual modules, clear fallbacks for usability",
    },
]


def required(value: object, fallback: str) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return fallback


def listify(value: object, fallback: list[str]) -> list[str]:
    if isinstance(value, list) and value:
        return [str(item).strip() for item in value if str(item).strip()]
    if isinstance(value, str) and value.strip():
        return [value.strip()]
    return fallback


def numbered(items: list[str]) -> str:
    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def bullets(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def build_prompt(brief: dict, direction: dict) -> str:
    project_name = required(brief.get("project_name"), "the product")
    description = required(brief.get("description"), "a digital product")
    target_users = required(brief.get("target_users"), "the target users")
    primary_goal = required(brief.get("primary_goal"), "complete the core workflow quickly and confidently")
    business_goal = required(brief.get("business_goal"), "increase activation and retention")
    platform = required(brief.get("platform"), "responsive web")
    screens = listify(brief.get("screens"), ["landing page", "onboarding", "dashboard", "detail view", "settings"])
    brand_tone = required(brief.get("brand_tone"), "modern, trustworthy, and clear")
    color_direction = required(brief.get("color_direction"), "an accessible palette with strong contrast and one clear accent color")
    style_preferences = listify(brief.get("style_preferences"), ["modern", "usable", "polished"])

    return dedent(
        f"""
        Design a {platform} UI for {project_name}, {description}.

        Target users:
        {target_users}

        Primary user goal:
        {primary_goal}

        Business goal:
        {business_goal}

        Core screens:
        {numbered(screens)}

        UX requirements:
        - Make the primary user goal obvious on the first screen.
        - Use realistic product content, not lorem ipsum.
        - Keep primary and secondary actions visually distinct.
        - Include first-run/empty states where relevant.
        - Preserve a connected flow across all screens.

        Visual direction:
        - Direction: {direction["name"]}
        - Style: {direction["style"]}
        - Layout: {direction["layout"]}
        - Brand tone: {brand_tone}
        - Color direction: {color_direction}
        - Style preferences: {", ".join(style_preferences)}
        - Typography feel: readable, structured, polished, with clear heading/body/label hierarchy.
        - Component style: navigation, cards, forms, tables/lists, charts if useful, modals/drawers, empty/loading/error/success states.

        Accessibility:
        - High contrast.
        - Clear hierarchy.
        - Readable type sizes.
        - Obvious hover/focus/active/disabled states.
        - Responsive layout for desktop and mobile.
        - Keyboard-friendly structure where applicable.

        Output:
        Create a polished high-fidelity UI concept with realistic content, clear navigation, coherent design-system choices, and production-ready layout structure. Also include a concise design-system summary that can become DESIGN.md.
        """
    ).strip()


def build_followups(brief: dict) -> str:
    screens = listify(brief.get("screens"), ["landing page", "onboarding", "dashboard"])
    return dedent(
        f"""
        ## Follow-up refinement prompts

        Use these after Stitch generates the first design.

        ### Strengthen the selected direction

        ```text
        Refine this UI while preserving the selected design system. Improve visual hierarchy, tighten spacing, clarify primary CTAs, add realistic empty/loading/error states, and ensure the layout works on desktop and mobile.
        ```

        ### Generate connected flow

        ```text
        Create a connected user flow across these screens: {", ".join(screens)}. Preserve the same navigation, colors, typography, spacing, component style, and content tone across every screen.
        ```

        ### Create DESIGN.md content

        ```text
        Create a concise DESIGN.md for this interface. Include product context, brand personality, semantic color tokens, typography scale, spacing scale, layout grid, radius/elevation, components, empty/loading/error/success states, accessibility rules, and implementation notes.
        ```

        ### Developer handoff

        ```text
        Produce a developer handoff for this UI. Include route structure, component breakdown, responsive behavior, required states, token mapping, and implementation risks.
        ```
        """
    ).strip()


def build_markdown(brief: dict) -> str:
    project_name = required(brief.get("project_name"), "Project")
    prompts = []
    for direction in DIRECTIONS:
        prompts.append(
            f"""### {direction['name']}\n\n```text\n{build_prompt(brief, direction)}\n```"""
        )

    screen_rows = "\n".join(
        f"| {screen} | Define and support the core product flow | Navigation, primary action, realistic content, states |"
        for screen in listify(brief.get("screens"), ["landing page", "onboarding", "dashboard"])
    )

    return dedent(
        f"""
        # Google Stitch Prompt Pack: {project_name}

        ## Brief summary

        - Project: {project_name}
        - Description: {required(brief.get('description'), 'Not specified')}
        - Target users: {required(brief.get('target_users'), 'Not specified')}
        - Platform: {required(brief.get('platform'), 'responsive web')}
        - Primary user goal: {required(brief.get('primary_goal'), 'Not specified')}
        - Business goal: {required(brief.get('business_goal'), 'Not specified')}

        ## Screen map

        | Screen | Purpose | Key elements |
        |---|---|---|
        {screen_rows}

        ## Stitch prompts

        {chr(10).join(prompts)}

        {build_followups(brief)}
        """
    ).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a Google Stitch prompt pack from a JSON brief.")
    parser.add_argument("--brief", required=True, help="Path to project brief JSON")
    parser.add_argument("--out", required=False, help="Output markdown path. Prints to stdout if omitted.")
    args = parser.parse_args()

    brief_path = Path(args.brief)
    if not brief_path.exists():
        raise SystemExit(f"Brief file not found: {brief_path}")

    try:
        brief = json.loads(brief_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {brief_path}: {exc}") from exc

    markdown = build_markdown(brief)

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(markdown, encoding="utf-8")
        print(f"Wrote {out_path}")
    else:
        print(markdown)


if __name__ == "__main__":
    main()
