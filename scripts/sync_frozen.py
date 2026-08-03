#!/usr/bin/env python3
"""Synchronize one consumer's reviewed skills and native global configuration."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import sync_codex_global_config
import sync_frozen_skills


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--consumer", choices=("codex",), required=True)
    parser.add_argument("--skills-destination", type=Path)
    parser.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
    args = parser.parse_args(argv)

    skills_common = ["--consumer", args.consumer]
    if args.skills_destination:
        skills_common.extend(["--destination", str(args.skills_destination)])
    config_common = ["--codex-home", str(args.codex_home)]

    if args.check:
        results = (
            sync_frozen_skills.main(["--check", *skills_common]),
            sync_codex_global_config.main(["--check", *config_common]),
        )
        return 2 if 2 in results else 1 if 1 in results else 0

    preflight = (
        sync_frozen_skills.main(["--check", *skills_common]),
        sync_codex_global_config.main(["--check", *config_common]),
    )
    if 2 in preflight:
        print("Synchronization refused because preflight found a conflict.", file=sys.stderr)
        return 2
    applied = (
        sync_frozen_skills.main(["--apply", *skills_common]),
        sync_codex_global_config.main(["--apply", *config_common]),
    )
    return 2 if 2 in applied else 0


if __name__ == "__main__":
    raise SystemExit(main())
