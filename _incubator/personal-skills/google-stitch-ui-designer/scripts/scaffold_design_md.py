#!/usr/bin/env python3
"""Create a starter .stitch/DESIGN.md from a structured project brief.

Usage:
    python scaffold_design_md.py --brief brief.json --out .stitch/DESIGN.md

The output is intentionally a scaffold. Replace placeholders with extracted
Stitch tokens, screenshots, HTML/CSS, Figma data, or MCP metadata when available.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from textwrap import dedent


def value(data: dict, key: str, default: str) -> str:
    raw = data.get(key)
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    return default


def list_value(data: dict, key: str, default: list[str]) -> list[str]:
    raw = data.get(key)
    if isinstance(raw, list) and raw:
        return [str(item).strip() for item in raw if str(item).strip()]
    return default


def build_design_md(brief: dict) -> str:
    project_name = value(brief, "project_name", "Project")
    description = value(brief, "description", "A digital product.")
    target_users = value(brief, "target_users", "Primary users")
    primary_goal = value(brief, "primary_goal", "Complete the core workflow.")
    business_goal = value(brief, "business_goal", "Increase activation and retention.")
    platform = value(brief, "platform", "responsive web")
    brand_tone = value(brief, "brand_tone", "modern, trustworthy, focused")
    color_direction = value(brief, "color_direction", "accessible neutral system with one primary accent")
    screens = list_value(brief, "screens", ["landing page", "onboarding", "dashboard"])
    style_preferences = list_value(brief, "style_preferences", ["clean", "usable", "polished"])

    screen_rows = "\n".join(f"| {screen} | TBD | TBD |" for screen in screens)

    return dedent(
        f"""
        # Design System: {project_name}

        ## Product context

        {project_name} is {description}

        - Target users: {target_users}
        - Platform: {platform}
        - Primary user goal: {primary_goal}
        - Business goal: {business_goal}

        ## Brand personality

        - Tone: {brand_tone}
        - Style preferences: {", ".join(style_preferences)}
        - Visual character: precise, coherent, and product-led
        - Differentiators: TBD after Stitch generation or artifact intake

        ## Color system

        Color direction: {color_direction}

        Replace placeholder values with exact Stitch tokens when available.

        | Token | Value | Usage |
        |---|---:|---|
        | `--color-background` | `#FFFFFF` | Page background |
        | `--color-surface` | `#F8FAFC` | Cards, panels, navigation surfaces |
        | `--color-surface-muted` | `#F1F5F9` | Subtle panels and inactive states |
        | `--color-primary` | `#2563EB` | Primary actions and active states |
        | `--color-primary-foreground` | `#FFFFFF` | Text/icons on primary surfaces |
        | `--color-secondary` | `#64748B` | Secondary actions and supporting UI |
        | `--color-accent` | `#7C3AED` | Highlights and visual emphasis |
        | `--color-text` | `#0F172A` | Main text |
        | `--color-text-muted` | `#64748B` | Secondary text |
        | `--color-border` | `#E2E8F0` | Borders and dividers |
        | `--color-success` | `#16A34A` | Success states |
        | `--color-warning` | `#D97706` | Warning states |
        | `--color-error` | `#DC2626` | Error/destructive states |

        ## Typography

        Replace with exact font family and scale from Stitch when available.

        | Role | Size | Line height | Weight | Usage |
        |---|---:|---:|---:|---|
        | Display | 48px | 56px | 700 | Hero headlines |
        | H1 | 36px | 44px | 700 | Page titles |
        | H2 | 28px | 36px | 650 | Section titles |
        | H3 | 20px | 28px | 650 | Card titles |
        | Body | 16px | 24px | 400 | Main content |
        | Small | 14px | 20px | 400 | Metadata and help text |
        | Label | 14px | 20px | 600 | Buttons, tabs, form labels |

        ## Spacing

        - Base unit: 4px
        - Page padding: 24px mobile, 48px desktop
        - Section gap: 64px desktop, 40px mobile
        - Card padding: 24px desktop, 16px mobile
        - Form field gap: 16px
        - List row height: 48px minimum

        ## Layout

        - Grid: responsive 12-column desktop grid, single-column mobile stack
        - Max width: 1200px for marketing pages; app shell fills viewport
        - Desktop navigation: TBD from selected Stitch direction
        - Mobile navigation: collapsed menu or bottom nav depending on app type
        - Breakpoints: mobile, tablet, desktop
        - Content density: balanced; increase density for workflow-heavy screens

        ## Screens

        | Screen | Purpose | Implementation target |
        |---|---|---|
        {screen_rows}

        ## Shape and elevation

        - Small radius: 6px
        - Medium radius: 10px
        - Large radius: 16px
        - Card radius: 16px
        - Button radius: 10px
        - Elevation: subtle; use borders for most structure and shadow for overlays/floating panels

        ## Components

        ### Buttons

        - Primary: filled primary background, strong contrast, clear hover/focus/disabled states
        - Secondary: outlined or muted surface treatment
        - Ghost: minimal background, visible hover/focus
        - Destructive: error color with confirmatory copy
        - Loading: spinner or progress text while preserving width

        ### Inputs and forms

        - Field height: 40-44px minimum
        - Labels: persistent visible labels
        - Help text: below field
        - Errors: clear message and recovery guidance
        - Disabled: visibly disabled without low-contrast text

        ### Cards and surfaces

        - Default card: surface background, border, consistent padding
        - Interactive card: hover/focus state and clear affordance
        - Metric card: label, value, delta, optional sparkline
        - Empty card: useful next action, not just blank state

        ### Navigation

        - Active state must be visible.
        - Navigation should scale to all core screens.
        - Mobile behavior must be explicit.

        ### Tables and lists

        - Row height: readable and scannable
        - Header style: clear but not oversized
        - Sorting/filtering: include when user task requires comparison
        - Empty state: explain why no data exists and what to do next

        ### Feedback states

        - Empty: include explanation and next action
        - Loading: skeletons for cards/tables where possible
        - Error: explain problem and recovery path
        - Success: confirm result and offer next step
        - Warning: reserved for meaningful risk

        ## Accessibility rules

        - Maintain strong text/background contrast.
        - Use semantic headings and landmarks.
        - Every form field needs a visible label.
        - Focus states must be visible.
        - Interactive elements must be keyboard reachable.
        - Do not communicate status using color alone.
        - Respect reduced-motion preferences for animations.

        ## Implementation notes

        - Use this file as the source of truth for future UI work.
        - Replace placeholders with exact Stitch tokens after MCP/export intake.
        - Keep component names stable and reusable.
        - Capture any implementation compromises in `.stitch/notes.md`.
        """
    ).strip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Scaffold DESIGN.md from a JSON brief.")
    parser.add_argument("--brief", required=True, help="Path to project brief JSON")
    parser.add_argument("--out", required=True, help="Output path, usually .stitch/DESIGN.md")
    args = parser.parse_args()

    brief_path = Path(args.brief)
    if not brief_path.exists():
        raise SystemExit(f"Brief file not found: {brief_path}")

    try:
        brief = json.loads(brief_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {brief_path}: {exc}") from exc

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(build_design_md(brief), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
