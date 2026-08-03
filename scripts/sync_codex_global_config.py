#!/usr/bin/env python3
"""Check or apply reviewed frozenSkillz global Codex configuration."""

from __future__ import annotations

import argparse
import os
import sys
import tempfile
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "config/codex/global"
START_MARKER = "<!-- frozenSkillz:browser-delegation:start -->"
END_MARKER = "<!-- frozenSkillz:browser-delegation:end -->"


class ConfigError(RuntimeError):
    """Raised when global Codex configuration cannot be synchronized safely."""


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigError(f"Cannot read {path}: {exc}") from exc


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(handle, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def _managed_block(fragment: str) -> str:
    return f"{START_MARKER}\n{fragment.strip()}\n{END_MARKER}"


def _render_agents(current: str, fragment: str) -> str:
    block = _managed_block(fragment)
    start_count = current.count(START_MARKER)
    end_count = current.count(END_MARKER)
    if start_count != end_count or start_count > 1:
        raise ConfigError("AGENTS.md has malformed browser-delegation markers")
    if start_count == 1:
        start = current.index(START_MARKER)
        end = current.index(END_MARKER, start) + len(END_MARKER)
        return current[:start] + block + current[end:]

    legacy = fragment.strip()
    if legacy in current:
        return current.replace(legacy, block, 1)

    if current and not current.endswith("\n"):
        current += "\n"
    separator = "\n" if current else ""
    return f"{current}{separator}{block}\n"


def synchronize(source: Path, codex_home: Path, apply: bool) -> tuple[bool, list[str]]:
    fragment_path = source / "AGENTS.browser-delegation.md"
    agent_source = source / "agents/chrome-pilot.toml"
    fragment = _read(fragment_path)
    agent = _read(agent_source)

    agents_target = codex_home / "AGENTS.md"
    agent_target = codex_home / "agents/chrome-pilot.toml"
    current_agents = _read(agents_target) if agents_target.exists() else ""
    desired_agents = _render_agents(current_agents, fragment)

    changes: list[str] = []
    if current_agents != desired_agents:
        changes.append(f"update {agents_target}")
    current_agent = _read(agent_target) if agent_target.exists() else None
    if current_agent != agent:
        changes.append(f"update {agent_target}")

    if apply:
        if current_agents != desired_agents:
            _atomic_write(agents_target, desired_agents)
        if current_agent != agent:
            _atomic_write(agent_target, agent)
    return not changes, changes


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
    args = parser.parse_args(argv)

    try:
        clean, changes = synchronize(args.source.resolve(), args.codex_home.resolve(), args.apply)
    except ConfigError as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 2

    if changes:
        verb = "Applied" if args.apply else "Required"
        for change in changes:
            print(f"{verb}: {change}")
    else:
        print("Global Codex configuration is current.")
    return 0 if args.apply or clean else 1


if __name__ == "__main__":
    raise SystemExit(main())
