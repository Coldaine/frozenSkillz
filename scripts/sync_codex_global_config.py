#!/usr/bin/env python3
"""Check, apply, diff, or roll back reviewed global Codex configuration."""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = REPO_ROOT / "config/codex/global"
START_MARKER = "<!-- frozenSkillz:browser-delegation:start -->"
END_MARKER = "<!-- frozenSkillz:browser-delegation:end -->"
MANAGEMENT_ROOT = Path(".frozenSkillz/codex-global-config")
STATE_FILE = "state.json"
STATE_SCHEMA = 1


class ConfigError(RuntimeError):
    """Raised when global Codex configuration cannot be synchronized safely."""


@dataclass(frozen=True)
class Change:
    key: str
    target: Path
    current: str | None
    desired: str


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise ConfigError(f"Cannot read {path}: {exc}") from exc


def _digest(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()


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


def _find_block(current: str) -> tuple[int, int, str] | None:
    start_count = current.count(START_MARKER)
    end_count = current.count(END_MARKER)
    if start_count != end_count or start_count > 1:
        raise ConfigError("AGENTS.md has malformed browser-delegation markers")
    if start_count == 0:
        return None
    start = current.find(START_MARKER)
    end_start = current.find(END_MARKER, start + len(START_MARKER))
    if start < 0 or end_start < 0 or end_start <= start:
        raise ConfigError("AGENTS.md has malformed browser-delegation markers")
    end = end_start + len(END_MARKER)
    return start, end, current[start:end]


def _render_agents(current: str, fragment: str) -> tuple[str, str | None]:
    block = _managed_block(fragment)
    found = _find_block(current)
    if found:
        start, end, existing = found
        return current[:start] + block + current[end:], existing

    legacy = fragment.strip()
    if legacy in current:
        return current.replace(legacy, block, 1), None

    if current and not current.endswith("\n"):
        current += "\n"
    separator = "\n" if current else ""
    return f"{current}{separator}{block}\n", None


def _load_state(codex_home: Path) -> dict:
    path = codex_home / MANAGEMENT_ROOT / STATE_FILE
    if not path.exists():
        return {"schema": STATE_SCHEMA, "managed": {}}
    try:
        state = json.loads(_read(path))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Cannot parse management state {path}: {exc}") from exc
    if state.get("schema") != STATE_SCHEMA or not isinstance(state.get("managed"), dict):
        raise ConfigError(f"Unsupported management state: {path}")
    return state


def _source_revision(source: Path) -> str:
    try:
        revision = subprocess.run(
            ["git", "-C", str(source), "rev-parse", "HEAD"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        dirty = subprocess.run(
            ["git", "-C", str(source), "status", "--porcelain", "--", str(source)],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
        return f"{revision}+dirty" if dirty else revision
    except (OSError, subprocess.CalledProcessError):
        return "unversioned"


def plan(source: Path, codex_home: Path) -> tuple[list[Change], list[str], dict]:
    fragment = _read(source / "AGENTS.browser-delegation.md")
    agent = _read(source / "agents/chrome-pilot.toml")
    state = _load_state(codex_home)
    recorded = state["managed"]

    agents_target = codex_home / "AGENTS.md"
    if agents_target.is_symlink():
        raise ConfigError(f"Refusing to replace symlinked target: {agents_target}")
    agents_target_exists = agents_target.exists()
    current_agents = _read(agents_target) if agents_target_exists else ""
    desired_agents, current_block = _render_agents(current_agents, fragment)
    desired_block = _managed_block(fragment)

    conflicts: list[str] = []
    prior_block_digest = recorded.get("AGENTS.md#browser-delegation")
    if current_block is not None and current_block != desired_block:
        if prior_block_digest is None or _digest(current_block) != prior_block_digest:
            conflicts.append("managed browser-delegation block was modified locally")

    changes: list[Change] = []
    if current_agents != desired_agents:
        changes.append(
            Change(
                "AGENTS.md#browser-delegation",
                agents_target,
                current_agents if agents_target_exists else None,
                desired_agents,
            )
        )

    agent_target = codex_home / "agents/chrome-pilot.toml"
    if agent_target.is_symlink():
        raise ConfigError(f"Refusing to replace symlinked target: {agent_target}")
    current_agent = _read(agent_target) if agent_target.exists() else None
    prior_agent_digest = recorded.get("agents/chrome-pilot.toml")
    if current_agent != agent:
        if current_agent is not None and (
            prior_agent_digest is None or _digest(current_agent) != prior_agent_digest
        ):
            conflicts.append(f"unmanaged or locally modified agent file: {agent_target}")
        changes.append(Change("agents/chrome-pilot.toml", agent_target, current_agent, agent))

    next_state = {
        "schema": STATE_SCHEMA,
        "source_revision": _source_revision(source),
        "source_digest": _digest(fragment + "\0" + agent),
        "managed": {
            "AGENTS.md#browser-delegation": _digest(desired_block),
            "agents/chrome-pilot.toml": _digest(agent),
        },
    }
    return changes, conflicts, next_state


def _transaction_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")


def apply_changes(codex_home: Path, changes: list[Change], state: dict) -> str | None:
    state_path = codex_home / MANAGEMENT_ROOT / STATE_FILE
    current_state = _load_state(codex_home)
    comparable_keys = ("schema", "source_revision", "source_digest", "managed")
    state_changed = any(current_state.get(key) != state.get(key) for key in comparable_keys)
    if not changes and not state_changed:
        return None
    transaction = _transaction_id()
    transaction_dir = codex_home / MANAGEMENT_ROOT / "transactions" / transaction
    transaction_dir.mkdir(parents=True)
    manifest = {"schema": 1, "transaction": transaction, "targets": []}

    for index, change in enumerate(changes):
        backup_name = f"{index}.backup"
        entry = {
            "key": change.key,
            "target": str(change.target.relative_to(codex_home)),
            "existed": change.current is not None,
            "backup": backup_name if change.current is not None else None,
        }
        if change.current is not None:
            _atomic_write(transaction_dir / backup_name, change.current)
        manifest["targets"].append(entry)

    if state_path.exists():
        shutil.copy2(state_path, transaction_dir / "state.backup.json")
        manifest["state_existed"] = True
    else:
        manifest["state_existed"] = False
    _atomic_write(transaction_dir / "manifest.json", json.dumps(manifest, indent=2) + "\n")

    try:
        for change in changes:
            observed = _read(change.target) if change.target.exists() else None
            if observed != change.current:
                raise ConfigError(
                    f"Target changed after planning; rerun before applying: {change.target}"
                )
            _atomic_write(change.target, change.desired)
            if _read(change.target) != change.desired:
                raise ConfigError(f"Post-write verification failed: {change.target}")
        state["last_transaction"] = transaction
        _atomic_write(state_path, json.dumps(state, indent=2, sort_keys=True) + "\n")
    except BaseException as exc:
        try:
            rollback(codex_home, transaction)
        except BaseException as rollback_exc:
            raise ConfigError(
                f"Apply failed and rollback also failed for transaction {transaction}: "
                f"{exc}; rollback: {rollback_exc}"
            ) from rollback_exc
        if isinstance(exc, ConfigError):
            raise
        raise ConfigError(
            f"Apply failed and transaction {transaction} was rolled back: {exc}"
        ) from exc
    return transaction


def rollback(codex_home: Path, transaction: str) -> None:
    transaction_dir = codex_home / MANAGEMENT_ROOT / "transactions" / transaction
    manifest_path = transaction_dir / "manifest.json"
    if not manifest_path.is_file():
        raise ConfigError(f"Unknown transaction: {transaction}")
    try:
        manifest = json.loads(_read(manifest_path))
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Cannot parse transaction manifest: {exc}") from exc
    for entry in manifest["targets"]:
        target = (codex_home / entry["target"]).resolve()
        if codex_home.resolve() not in target.parents:
            raise ConfigError(f"Transaction target escapes Codex home: {target}")
        if entry["existed"]:
            _atomic_write(target, _read(transaction_dir / entry["backup"]))
        elif target.exists():
            target.unlink()
    state_path = codex_home / MANAGEMENT_ROOT / STATE_FILE
    state_backup = transaction_dir / "state.backup.json"
    if manifest.get("state_existed"):
        _atomic_write(state_path, _read(state_backup))
    elif state_path.exists():
        state_path.unlink()


def print_diff(changes: list[Change]) -> None:
    for change in changes:
        current = (change.current or "").splitlines(keepends=True)
        desired = change.desired.splitlines(keepends=True)
        sys.stdout.writelines(
            difflib.unified_diff(
                current,
                desired,
                fromfile=f"live/{change.key}",
                tofile=f"reviewed/{change.key}",
            )
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--diff", action="store_true")
    mode.add_argument("--rollback", metavar="TRANSACTION")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--codex-home", type=Path, default=Path.home() / ".codex")
    args = parser.parse_args(argv)
    codex_home = args.codex_home.resolve()

    try:
        if args.rollback:
            rollback(codex_home, args.rollback)
            print(f"Rolled back transaction {args.rollback}.")
            return 0
        changes, conflicts, state = plan(args.source.resolve(), codex_home)
        if conflicts:
            for conflict in conflicts:
                print(f"CONFLICT: {conflict}", file=sys.stderr)
            return 2
        if args.diff:
            print_diff(changes)
            return 1 if changes else 0
        if args.apply:
            transaction = apply_changes(codex_home, changes, state)
            if transaction:
                print(f"Applied global Codex configuration ({transaction}).")
            else:
                print("Global Codex configuration is current.")
            return 0
        if changes:
            for change in changes:
                print(f"Required: update {change.target}")
            return 1
        print("Global Codex configuration is current.")
        return 0
    except ConfigError as exc:
        print(f"FAILED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
