#!/usr/bin/env python3
"""Synchronize reviewed frozen-skills content into a local agent skill root."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


MANIFEST_PATHS = (
    Path(".claude-plugin/plugin.json"),
    Path(".codex-plugin/plugin.json"),
    Path(".cursor-plugin/plugin.json"),
    Path("gemini-extension.json"),
)
STATE_FILE = ".frozen-skills-sync.json"
STATE_SCHEMA = 1
IGNORED_NAMES = {".DS_Store", "Thumbs.db", "__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}
SKILL_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
DIGEST_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class SyncError(RuntimeError):
    """Raised when the distribution or destination cannot be synchronized safely."""


@dataclass(frozen=True)
class SkillSource:
    name: str
    path: Path
    digest: str


@dataclass(frozen=True)
class Action:
    kind: str
    name: str
    detail: str


@dataclass(frozen=True)
class SyncResult:
    actions: tuple[Action, ...]

    @property
    def conflicts(self) -> tuple[Action, ...]:
        return tuple(action for action in self.actions if action.kind == "conflict")

    @property
    def changes(self) -> tuple[Action, ...]:
        return tuple(
            action
            for action in self.actions
            if action.kind in {"install", "update", "adopt", "remove", "forget"}
        )


def _load_json(path: Path) -> dict:
    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise SyncError(f"Cannot read JSON from {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SyncError(f"Expected a JSON object in {path}")
    return data


def _validate_skill_name(name: str, source: Path) -> None:
    if not SKILL_NAME_PATTERN.fullmatch(name) or name in {".", ".."}:
        raise SyncError(f"Unsafe skill name {name!r} in {source}")


def _manifest_skill_set(data: dict, manifest: Path) -> tuple[tuple[str, str], ...]:
    entries = data.get("skills")
    if not isinstance(entries, list):
        raise SyncError(f"Manifest has no skills list: {manifest}")

    normalized: list[tuple[str, str]] = []
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise SyncError(f"Invalid skill entry in {manifest}: {entry!r}")
        name = entry.get("name")
        relative_path = entry.get("path")
        if not isinstance(name, str) or not name:
            raise SyncError(f"Skill entry has no name in {manifest}")
        _validate_skill_name(name, manifest)
        if not isinstance(relative_path, str) or not relative_path:
            raise SyncError(f"Skill {name!r} has no path in {manifest}")
        if name in seen:
            raise SyncError(f"Duplicate skill {name!r} in {manifest}")
        seen.add(name)
        normalized.append((name, Path(relative_path).as_posix()))
    return tuple(normalized)


def _iter_skill_files(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative_parts = path.relative_to(root).parts
        if any(part in IGNORED_NAMES for part in relative_parts):
            continue
        if path.is_symlink():
            raise SyncError(f"Skill source must not contain symbolic links: {path}")
        if path.is_file() and path.suffix not in IGNORED_SUFFIXES:
            yield path


def digest_directory(root: Path) -> str:
    if not root.is_dir():
        raise SyncError(f"Skill path is not a directory: {root}")

    digest = hashlib.sha256()
    found_file = False
    for path in _iter_skill_files(root):
        found_file = True
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        with path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                digest.update(chunk)
    if not found_file:
        raise SyncError(f"Skill directory is empty: {root}")
    return digest.hexdigest()


def load_distribution(repo_root: Path) -> tuple[Path, str, tuple[SkillSource, ...]]:
    plugin_root = (repo_root / "plugins/frozen-skills").resolve()
    manifests: list[tuple[Path, dict, tuple[tuple[str, str], ...]]] = []
    for relative_manifest in MANIFEST_PATHS:
        manifest = plugin_root / relative_manifest
        if not manifest.is_file():
            raise SyncError(f"Required manifest is missing: {manifest}")
        data = _load_json(manifest)
        manifests.append((manifest, data, _manifest_skill_set(data, manifest)))

    baseline_manifest, baseline_data, baseline_skills = manifests[0]
    plugin_name = baseline_data.get("name")
    version = baseline_data.get("version")
    if plugin_name != "frozen-skills" or not isinstance(version, str) or not version:
        raise SyncError(f"Invalid plugin identity or version in {baseline_manifest}")

    for manifest, data, skills in manifests[1:]:
        if data.get("name") != plugin_name:
            raise SyncError(f"Plugin name differs in {manifest}")
        if data.get("version") != version:
            raise SyncError(f"Plugin version differs in {manifest}")
        if skills != baseline_skills:
            raise SyncError(
                f"Active skill list differs between {baseline_manifest} and {manifest}"
            )

    resolved_plugin_root = plugin_root.resolve()
    sources: list[SkillSource] = []
    for name, relative_path in baseline_skills:
        candidate = (plugin_root / relative_path).resolve()
        try:
            candidate.relative_to(resolved_plugin_root)
        except ValueError as exc:
            raise SyncError(f"Skill path escapes plugin root: {relative_path}") from exc
        if candidate.name != name:
            raise SyncError(
                f"Skill {name!r} must use a same-name directory, found {relative_path!r}"
            )
        if not (candidate / "SKILL.md").is_file():
            raise SyncError(f"Skill {name!r} has no SKILL.md: {candidate}")
        sources.append(SkillSource(name, candidate, digest_directory(candidate)))

    return plugin_root, version, tuple(sources)


def _empty_state() -> dict:
    return {"schema": STATE_SCHEMA, "plugin": "frozen-skills", "skills": {}}


def load_state(destination: Path) -> dict:
    path = destination / STATE_FILE
    if not path.exists():
        return _empty_state()
    data = _load_json(path)
    if data.get("schema") != STATE_SCHEMA or data.get("plugin") != "frozen-skills":
        raise SyncError(f"Unsupported or unrelated sync state: {path}")
    if not isinstance(data.get("skills"), dict):
        raise SyncError(f"Invalid skills state in {path}")
    for name, entry in data["skills"].items():
        if not isinstance(name, str):
            raise SyncError(f"Invalid skill name in {path}")
        _validate_skill_name(name, path)
        if not isinstance(entry, dict) or not DIGEST_PATTERN.fullmatch(
            str(entry.get("digest", ""))
        ):
            raise SyncError(f"Invalid digest for skill {name!r} in {path}")
    return data


def _target_digest(target: Path) -> str | None:
    if not target.exists():
        return None
    if not target.is_dir():
        raise SyncError(f"Skill destination is not a directory: {target}")
    return digest_directory(target)


def plan_sync(
    sources: tuple[SkillSource, ...],
    destination: Path,
    state: dict,
    *,
    prune: bool,
    force: bool,
) -> tuple[Action, ...]:
    actions: list[Action] = []
    recorded = state["skills"]
    active_names = {source.name for source in sources}

    for source in sources:
        target = destination / source.name
        current_digest = _target_digest(target)
        prior_entry = recorded.get(source.name)
        prior_digest = prior_entry.get("digest") if isinstance(prior_entry, dict) else None

        if current_digest == source.digest:
            kind = "current" if prior_digest == source.digest else "adopt"
            detail = "already matches reviewed source"
        elif current_digest is None:
            kind = "install"
            detail = "destination skill is missing"
        elif prior_digest and current_digest == prior_digest:
            kind = "update"
            detail = "managed copy differs from reviewed source"
        elif force:
            kind = "update"
            detail = "overwrite locally modified or unmanaged copy (--force)"
        else:
            kind = "conflict"
            detail = "destination has locally modified or unmanaged content"
        actions.append(Action(kind, source.name, detail))

    if prune:
        for name in sorted(set(recorded) - active_names):
            target = destination / name
            current_digest = _target_digest(target)
            prior_entry = recorded.get(name)
            prior_digest = prior_entry.get("digest") if isinstance(prior_entry, dict) else None
            if current_digest is None:
                actions.append(Action("forget", name, "managed skill is already absent"))
            elif prior_digest and current_digest == prior_digest:
                actions.append(Action("remove", name, "no longer listed in active manifests"))
            elif force:
                actions.append(
                    Action("remove", name, "remove locally modified retired skill (--force)")
                )
            else:
                actions.append(
                    Action("conflict", name, "retired managed skill has local modifications")
                )

    return tuple(actions)


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def _replace_directory(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    nonce = uuid.uuid4().hex
    staged = target.parent / f".{target.name}.frozen-skills-stage-{nonce}"
    backup = target.parent / f".{target.name}.frozen-skills-backup-{nonce}"
    try:
        shutil.copytree(
            source,
            staged,
            ignore=shutil.ignore_patterns(".DS_Store", "Thumbs.db", "__pycache__", "*.pyc", "*.pyo"),
        )
        if target.exists():
            os.replace(target, backup)
        os.replace(staged, target)
        _remove_path(backup)
    except Exception:
        if backup.exists() and not target.exists():
            os.replace(backup, target)
        raise
    finally:
        _remove_path(staged)
        _remove_path(backup)


def _write_state(destination: Path, state: dict) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / STATE_FILE
    staged = destination / f".{STATE_FILE}.{uuid.uuid4().hex}.tmp"
    try:
        with staged.open("w", encoding="utf-8", newline="\n") as handle:
            json.dump(state, handle, indent=2, sort_keys=True)
            handle.write("\n")
        os.replace(staged, target)
    finally:
        if staged.exists():
            staged.unlink()


def sync(
    repo_root: Path,
    destination: Path,
    *,
    apply: bool,
    prune: bool,
    force: bool,
) -> SyncResult:
    plugin_root, version, sources = load_distribution(repo_root.resolve())
    destination = destination.resolve()
    state = load_state(destination)
    actions = plan_sync(sources, destination, state, prune=prune, force=force)
    result = SyncResult(actions)

    if not apply or result.conflicts:
        return result

    source_by_name = {source.name: source for source in sources}
    for action in actions:
        target = destination / action.name
        if action.kind in {"install", "update"}:
            _replace_directory(source_by_name[action.name].path, target)
        elif action.kind == "remove":
            _remove_path(target)

    next_skills = dict(state["skills"])
    for source in sources:
        next_skills[source.name] = {
            "digest": source.digest,
            "source": source.path.relative_to(plugin_root).as_posix(),
        }
    if prune:
        for name in set(next_skills) - set(source_by_name):
            del next_skills[name]

    next_state = {
        "schema": STATE_SCHEMA,
        "plugin": "frozen-skills",
        "plugin_version": version,
        "skills": next_skills,
    }
    _write_state(destination, next_state)
    return result


def _expanded_path(value: str) -> Path:
    return Path(os.path.expandvars(os.path.expanduser(value)))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Synchronize manifest-listed frozen-skills into a local skill root. "
            "The command refuses to overwrite local changes unless --force is supplied."
        )
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report drift without writing")
    mode.add_argument("--apply", action="store_true", help="apply the synchronization plan")
    parser.add_argument(
        "--destination",
        type=_expanded_path,
        default=_expanded_path("~/.agents/skills"),
        help="local skill root (default: ~/.agents/skills)",
    )
    parser.add_argument(
        "--repo-root",
        type=_expanded_path,
        default=Path(__file__).resolve().parent.parent,
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--prune",
        action="store_true",
        help="remove previously managed skills no longer listed in the manifests",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite conflicting local content (use only after reviewing the plan)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = sync(
            args.repo_root,
            args.destination,
            apply=args.apply,
            prune=args.prune,
            force=args.force,
        )
    except SyncError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for action in result.actions:
        print(f"{action.kind.upper():8} {action.name}: {action.detail}")

    if result.conflicts:
        print("Synchronization refused because conflicts require review.", file=sys.stderr)
        return 2
    if args.check and result.changes:
        print("Local skills differ from the reviewed frozen-skills distribution.")
        return 1
    if args.apply:
        print(f"Synchronized skills into {args.destination.resolve()}")
    else:
        print("Local skills match the reviewed frozen-skills distribution.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
