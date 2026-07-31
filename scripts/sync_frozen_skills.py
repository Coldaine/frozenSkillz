#!/usr/bin/env python3
"""Synchronize one consumer or deployment's frozen-skills into a local skill root."""

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


MANIFEST_PATHS = {
    "claude": Path(".claude-plugin/plugin.json"),
    "codex": Path(".codex-plugin/plugin.json"),
    "cursor": Path(".cursor-plugin/plugin.json"),
    "gemini": Path("gemini-extension.json"),
}
DISTRIBUTION_PATH = Path("distribution.json")
DEFAULT_DESTINATIONS = {"codex": "~/.codex/skills"}
STATE_FILE = ".frozen-skills-sync.json"
STATE_SCHEMA = 2
IGNORED_NAMES = {".DS_Store", "Thumbs.db", "__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}
SKILL_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")
DIGEST_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class SyncError(RuntimeError):
    """Raised when the distribution or destination cannot be synchronized safely."""


class TargetChangedError(SyncError):
    """Raised when a destination changes after its synchronization plan."""

    def __init__(self, target: Path, current_digest: str | None):
        """Record the target and newly observed digest for conflict reporting."""

        super().__init__(f"Destination changed after planning: {target}")
        self.target = target
        self.current_digest = current_digest


@dataclass(frozen=True)
class SkillSource:
    """A validated active skill and the digest of its reviewed source tree."""

    name: str
    path: Path
    digest: str


@dataclass(frozen=True)
class Action:
    """One planned synchronization action and the target state it observed."""

    kind: str
    name: str
    detail: str
    observed_digest: str | None = None


@dataclass(frozen=True)
class SyncResult:
    """The complete synchronization plan or apply result."""

    actions: tuple[Action, ...]

    @property
    def conflicts(self) -> tuple[Action, ...]:
        """Return actions that require human conflict resolution."""

        return tuple(action for action in self.actions if action.kind == "conflict")

    @property
    def changes(self) -> tuple[Action, ...]:
        """Return actions that make or record a distribution change."""

        return tuple(
            action
            for action in self.actions
            if action.kind in {"install", "update", "adopt", "remove", "forget", "state"}
        )


def _load_json(path: Path) -> dict:
    """Load a JSON object or raise a synchronization-specific error."""

    try:
        with path.open("r", encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, json.JSONDecodeError) as exc:
        raise SyncError(f"Cannot read JSON from {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SyncError(f"Expected a JSON object in {path}")
    return data


def _validate_safe_name(name: str, kind: str, source: Path) -> None:
    """Reject names that could escape a destination root."""

    if (
        not isinstance(name, str)
        or not SKILL_NAME_PATTERN.fullmatch(name)
        or name in {".", ".."}
    ):
        raise SyncError(f"Unsafe {kind} name {name!r} in {source}")


def _validate_skill_name(name: str, source: Path) -> None:
    """Reject skill names that could escape a destination root."""

    _validate_safe_name(name, "skill", source)


def _skill_entry_set(data: dict, source: Path) -> tuple[tuple[str, str], ...]:
    """Return a validated ordered name/path tuple from one distribution section."""

    entries = data.get("skills")
    if not isinstance(entries, list):
        raise SyncError(f"Distribution section has no skills list: {source}")

    normalized: list[tuple[str, str]] = []
    seen: set[str] = set()
    for entry in entries:
        if not isinstance(entry, dict):
            raise SyncError(f"Invalid skill entry in {source}: {entry!r}")
        name = entry.get("name")
        relative_path = entry.get("path")
        if not isinstance(name, str) or not name:
            raise SyncError(f"Skill entry has no name in {source}")
        _validate_skill_name(name, source)
        if not isinstance(relative_path, str) or not relative_path:
            raise SyncError(f"Skill {name!r} has no path in {source}")
        if name in seen:
            raise SyncError(f"Duplicate skill {name!r} in {source}")
        seen.add(name)
        normalized.append((name, Path(relative_path).as_posix()))
    return tuple(normalized)


def _iter_skill_files(root: Path) -> Iterable[Path]:
    """Yield deterministic source files while rejecting symbolic links."""

    for path in sorted(root.rglob("*"), key=lambda item: item.as_posix()):
        relative_parts = path.relative_to(root).parts
        if any(part in IGNORED_NAMES for part in relative_parts):
            continue
        if path.is_symlink():
            raise SyncError(f"Skill source must not contain symbolic links: {path}")
        if path.is_file() and path.suffix not in IGNORED_SUFFIXES:
            yield path


def digest_directory(root: Path) -> str:
    """Hash a skill tree with explicit path and per-file content framing."""

    if not root.is_dir():
        raise SyncError(f"Skill path is not a directory: {root}")

    digest = hashlib.sha256()
    found_file = False
    for path in _iter_skill_files(root):
        found_file = True
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(len(relative).to_bytes(8, "big"))
        digest.update(relative)
        file_digest = hashlib.sha256()
        content_length = 0
        with path.open("rb") as handle:
            while chunk := handle.read(1024 * 1024):
                content_length += len(chunk)
                file_digest.update(chunk)
        digest.update(content_length.to_bytes(8, "big"))
        digest.update(file_digest.digest())
    if not found_file:
        raise SyncError(f"Skill directory is empty: {root}")
    return digest.hexdigest()


def _resolve_distribution_skill(source_root: Path, name: str, relative_path: str) -> Path:
    """Resolve and validate one distribution-listed skill source directory."""

    candidate = (source_root / relative_path).resolve()
    try:
        candidate.relative_to(source_root)
    except ValueError as exc:
        raise SyncError(
            f"Skill path escapes plugins source root: {relative_path}"
        ) from exc
    if candidate.name != name:
        raise SyncError(
            f"Skill {name!r} must use a same-name directory, found {relative_path!r}"
        )
    if not (candidate / "SKILL.md").is_file():
        raise SyncError(f"Skill {name!r} has no SKILL.md: {candidate}")
    return candidate


def validate_deployments(
    distribution: dict,
    source: Path,
    available_by_consumer: dict[str, set[str]],
) -> dict[str, dict]:
    """Validate the optional deployment subsets against the active distribution."""

    deployments = distribution.get("deployments", {})
    if not isinstance(deployments, dict):
        raise SyncError(f"Distribution deployments must be an object: {source}")

    validated: dict[str, dict] = {}
    for name, entry in deployments.items():
        _validate_safe_name(name, "deployment", source)
        if not isinstance(entry, dict):
            raise SyncError(f"Deployment {name!r} must be an object: {source}")
        description = entry.get("description")
        if not isinstance(description, str) or not description.strip():
            raise SyncError(f"Deployment {name!r} has no description: {source}")
        deployment_consumer = entry.get("consumer")
        if deployment_consumer not in available_by_consumer:
            raise SyncError(
                f"Deployment {name!r} must name one consumer of "
                f"{sorted(available_by_consumer)}: {source}"
            )
        names = entry.get("skills")
        if not isinstance(names, list) or not names:
            raise SyncError(f"Deployment {name!r} has no skills: {source}")
        available = available_by_consumer[deployment_consumer]
        selected: list[str] = []
        for skill_name in names:
            _validate_safe_name(skill_name, "skill", source)
            if skill_name in selected:
                raise SyncError(
                    f"Deployment {name!r} contains duplicate skill {skill_name!r}: {source}"
                )
            if skill_name not in available:
                raise SyncError(
                    f"Deployment {name!r} skill {skill_name!r} is not active for "
                    f"consumer {deployment_consumer!r}"
                )
            selected.append(skill_name)
        validated[name] = {
            "description": description,
            "consumer": deployment_consumer,
            "skills": tuple(selected),
        }
    return validated


def load_distribution(
    repo_root: Path, consumer: str | None = None, *, deployment: str | None = None
) -> tuple[Path, str, str, tuple[SkillSource, ...]]:
    """Validate all manifests and load one consumer or deployment's distribution."""

    if consumer is not None and consumer not in MANIFEST_PATHS:
        raise SyncError(f"Unknown skill consumer: {consumer!r}")

    source_root = (repo_root / "plugins").resolve()
    plugin_root = source_root / "frozen-skills"
    manifests: dict[str, tuple[Path, dict]] = {}
    for manifest_consumer, relative_manifest in MANIFEST_PATHS.items():
        manifest = plugin_root / relative_manifest
        if not manifest.is_file():
            raise SyncError(f"Required manifest is missing: {manifest}")
        data = _load_json(manifest)
        manifests[manifest_consumer] = (manifest, data)

    baseline_manifest, baseline_data = manifests["claude"]
    plugin_name = baseline_data.get("name")
    version = baseline_data.get("version")
    if plugin_name != "frozen-skills" or not isinstance(version, str) or not version:
        raise SyncError(f"Invalid plugin identity or version in {baseline_manifest}")

    for manifest_consumer, (manifest, data) in manifests.items():
        if manifest_consumer == "claude":
            continue
        if data.get("name") != plugin_name:
            raise SyncError(f"Plugin name differs in {manifest}")
        if data.get("version") != version:
            raise SyncError(f"Plugin version differs in {manifest}")

    distribution_path = source_root / DISTRIBUTION_PATH
    distribution = _load_json(distribution_path)
    if (
        distribution.get("schema") != 1
        or distribution.get("plugin") != plugin_name
        or distribution.get("version") != version
    ):
        raise SyncError(
            f"Distribution identity, schema, or version differs in {distribution_path}"
        )
    consumers = distribution.get("consumers")
    if not isinstance(consumers, dict) or set(consumers) != set(MANIFEST_PATHS):
        raise SyncError(
            f"Distribution consumers must be exactly {sorted(MANIFEST_PATHS)}"
        )
    consumer_packages = distribution.get("consumer_packages")
    if (
        not isinstance(consumer_packages, dict)
        or set(consumer_packages) != set(MANIFEST_PATHS)
        or any(not isinstance(packages, list) for packages in consumer_packages.values())
        or any(
            not isinstance(package, str)
            or not SKILL_NAME_PATTERN.fullmatch(package)
            or package == "frozen-skills"
            for packages in consumer_packages.values()
            for package in packages
        )
        or any(
            len(packages) != len(set(packages))
            for packages in consumer_packages.values()
        )
    ):
        raise SyncError(
            "Distribution consumer_packages must map exactly "
            f"{sorted(MANIFEST_PATHS)} to unique safe package-name lists; "
            "'frozen-skills' is reserved for shared skills"
        )

    shared_skills = _skill_entry_set(
        {"skills": distribution.get("shared")}, distribution_path
    )
    for name, relative_path in shared_skills:
        parts = Path(relative_path).parts
        if (
            len(parts) < 3
            or parts[:2] != ("frozen-skills", "skills")
            or ".." in parts
        ):
            raise SyncError(f"Shared skill {name!r} is outside frozen-skills/skills")
    consumer_skills = {
        manifest_consumer: _skill_entry_set(
            {"skills": entries}, distribution_path
        )
        for manifest_consumer, entries in consumers.items()
    }
    for manifest_consumer, entries in consumer_skills.items():
        shared_names = {name for name, _path in shared_skills}
        duplicated = shared_names & {name for name, _path in entries}
        if duplicated:
            raise SyncError(
                f"Consumer {manifest_consumer!r} duplicates shared skills: "
                f"{sorted(duplicated)}"
            )
        allowed_packages = set(consumer_packages[manifest_consumer])
        for name, relative_path in entries:
            parts = Path(relative_path).parts
            if (
                len(parts) < 3
                or parts[0] not in allowed_packages
                or parts[1] != "skills"
                or ".." in parts
            ):
                raise SyncError(
                    f"Consumer {manifest_consumer!r} skill {name!r} is outside its "
                    "declared consumer packages"
                )

    all_distribution_entries = list(shared_skills)
    for entries in consumer_skills.values():
        all_distribution_entries.extend(entries)
    for name, relative_path in all_distribution_entries:
        _resolve_distribution_skill(source_root, name, relative_path)

    shared_names = {name for name, _path in shared_skills}
    deployments = validate_deployments(
        distribution,
        distribution_path,
        {
            manifest_consumer: shared_names | {name for name, _path in entries}
            for manifest_consumer, entries in consumer_skills.items()
        },
    )

    if deployment is not None:
        selected_deployment = deployments.get(deployment)
        if selected_deployment is None:
            raise SyncError(f"Unknown deployment {deployment!r} in {distribution_path}")
        if consumer is not None and consumer != selected_deployment["consumer"]:
            raise SyncError(
                f"Deployment {deployment!r} targets consumer "
                f"{selected_deployment['consumer']!r}, not the requested {consumer!r}; "
                "a deployment already selects its own consumer"
            )
        consumer = selected_deployment["consumer"]
    if consumer is None:
        raise SyncError("A consumer or a deployment must be selected")

    selected_skills = shared_skills + consumer_skills[consumer]
    if deployment is not None:
        path_by_name = dict(selected_skills)
        selected_skills = tuple(
            (name, path_by_name[name]) for name in deployments[deployment]["skills"]
        )

    sources: list[SkillSource] = []
    for name, relative_path in selected_skills:
        candidate = _resolve_distribution_skill(source_root, name, relative_path)
        sources.append(SkillSource(name, candidate, digest_directory(candidate)))

    return source_root, version, consumer, tuple(sources)


def _empty_state(consumer: str, deployment: str | None = None) -> dict:
    """Return a new empty synchronization management record."""

    state = {
        "schema": STATE_SCHEMA,
        "plugin": "frozen-skills",
        "consumer": consumer,
        "skills": {},
    }
    if deployment is not None:
        state["deployment"] = deployment
    return state


def _owner_label(deployment: str | None) -> str:
    """Describe which distribution scope owns a destination."""

    if deployment is None:
        return "the full consumer distribution"
    return f"deployment {deployment!r}"


def load_state(destination: Path, consumer: str, deployment: str | None = None) -> dict:
    """Load and validate the destination's management record."""

    path = destination / STATE_FILE
    if not path.exists():
        return _empty_state(consumer, deployment)
    data = _load_json(path)
    if data.get("schema") != STATE_SCHEMA or data.get("plugin") != "frozen-skills":
        raise SyncError(
            f"Unsupported or unrelated sync state: {path}; use a fresh consumer-specific "
            "destination or migrate the state deliberately"
        )
    state_consumer = data.get("consumer")
    if state_consumer != consumer:
        raise SyncError(
            f"Destination is managed for consumer {state_consumer!r}, not {consumer!r}: {path}"
        )
    state_deployment = data.get("deployment")
    if state_deployment is not None:
        _validate_safe_name(state_deployment, "deployment", path)
    if state_deployment != deployment:
        raise SyncError(
            f"Destination is managed by {_owner_label(state_deployment)}, not "
            f"{_owner_label(deployment)}: {path}; use a separate destination or "
            "deliberately remove the existing managed state"
        )
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
    """Return a destination tree digest, or None when it is absent."""

    is_junction = getattr(os.path, "isjunction", lambda _path: False)
    if target.is_symlink() or is_junction(target):
        raise SyncError(f"Skill destination must be a real directory, not a link: {target}")
    if not target.exists():
        return None
    if not target.is_dir():
        raise SyncError(f"Skill destination is not a directory: {target}")
    return digest_directory(target)


def _validate_direction(repo_root: Path, destination: Path) -> None:
    """Require an outward destination disjoint from the source repository."""

    if destination == repo_root or repo_root in destination.parents:
        raise SyncError("Destination must be outside the frozenSkillz repository")
    if destination in repo_root.parents:
        raise SyncError("Destination must not contain the frozenSkillz repository")


def plan_sync(
    sources: tuple[SkillSource, ...],
    destination: Path,
    state: dict,
    *,
    prune: bool,
    force: bool,
    exact: bool = False,
) -> tuple[Action, ...]:
    """Plan safe distribution changes from one observed destination snapshot."""

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
        actions.append(Action(kind, source.name, detail, current_digest))

    if prune:
        for name in sorted(set(recorded) - active_names):
            target = destination / name
            current_digest = _target_digest(target)
            prior_entry = recorded.get(name)
            prior_digest = prior_entry.get("digest") if isinstance(prior_entry, dict) else None
            if current_digest is None:
                actions.append(
                    Action("forget", name, "managed skill is already absent", current_digest)
                )
            elif prior_digest and current_digest == prior_digest:
                actions.append(
                    Action(
                        "remove",
                        name,
                        "no longer listed in the selected distribution",
                        current_digest,
                    )
                )
            elif force:
                actions.append(
                    Action(
                        "remove",
                        name,
                        "remove locally modified retired skill (--force)",
                        current_digest,
                    )
                )
            else:
                actions.append(
                    Action(
                        "conflict",
                        name,
                        "retired managed skill has local modifications",
                        current_digest,
                    )
                )

    if exact and destination.exists():
        known_names = active_names | set(recorded) | {STATE_FILE}
        for entry in sorted(destination.iterdir(), key=lambda item: item.name):
            if entry.name not in known_names:
                actions.append(
                    Action(
                        "conflict",
                        entry.name,
                        "deployment destination contains unmanaged content",
                    )
                )

    return tuple(actions)


def _remove_path(path: Path) -> None:
    """Remove one explicitly selected file, link, or directory tree."""

    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        shutil.rmtree(path)


def _replace_directory(
    source: Path,
    target: Path,
    expected_source_digest: str,
    observed_target_digest: str | None,
) -> None:
    """Stage and replace one skill while preserving a failed rollback backup."""

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
        staged_digest = digest_directory(staged)
        if staged_digest != expected_source_digest:
            raise SyncError(
                f"Reviewed source changed while staging {source}; rerun synchronization"
            )
        current_target_digest = _target_digest(target)
        if current_target_digest != observed_target_digest:
            raise TargetChangedError(target, current_target_digest)
        if target.exists():
            os.replace(target, backup)
        os.replace(staged, target)
        _remove_path(backup)
    except Exception:
        if backup.exists() and not target.exists():
            try:
                os.replace(backup, target)
            except Exception as restore_error:
                raise SyncError(
                    f"Replacing {target} failed and rollback also failed; "
                    f"the original copy is preserved at {backup}"
                ) from restore_error
        raise
    finally:
        _remove_path(staged)


def _write_state(destination: Path, state: dict) -> None:
    """Atomically write the synchronization management record."""

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
    consumer: str | None = None,
    apply: bool,
    prune: bool,
    force: bool,
    deployment: str | None = None,
) -> SyncResult:
    """Check or apply one consumer or deployment distribution to one skill root."""

    repo_root = repo_root.resolve()
    destination = destination.resolve()
    _validate_direction(repo_root, destination)
    if deployment is not None and not prune:
        raise SyncError(
            "Deployment synchronization requires --prune so the destination "
            "converges to the exact deployment"
        )
    source_root, version, consumer, sources = load_distribution(
        repo_root, consumer, deployment=deployment
    )
    state = load_state(destination, consumer, deployment)
    actions = list(
        plan_sync(
            sources,
            destination,
            state,
            prune=prune,
            force=force,
            exact=deployment is not None,
        )
    )
    if state["skills"] and state.get("plugin_version") != version:
        actions.append(
            Action(
                "state",
                "frozen-skills",
                "management record plugin version differs",
            )
        )
    result = SyncResult(tuple(actions))

    if not apply or result.conflicts:
        return result

    source_by_name = {source.name: source for source in sources}
    for action in actions:
        if action.kind == "state":
            continue
        target = destination / action.name
        if action.kind in {"install", "update"}:
            source = source_by_name[action.name]
            try:
                _replace_directory(
                    source.path,
                    target,
                    source.digest,
                    action.observed_digest,
                )
            except TargetChangedError as exc:
                return SyncResult(
                    tuple(actions)
                    + (
                        Action(
                            "conflict",
                            action.name,
                            "destination changed after the synchronization plan was created; rerun",
                            exc.current_digest,
                        ),
                    )
                )
        elif action.kind == "remove":
            current_digest = _target_digest(target)
            if current_digest != action.observed_digest:
                return SyncResult(
                    tuple(actions)
                    + (
                        Action(
                            "conflict",
                            action.name,
                            "destination changed after the synchronization plan was created; rerun",
                            current_digest,
                        ),
                    )
                )
            _remove_path(target)
        else:
            current_digest = _target_digest(target)
            if current_digest != action.observed_digest:
                return SyncResult(
                    tuple(actions)
                    + (
                        Action(
                            "conflict",
                            action.name,
                            "destination changed after the synchronization plan was created; rerun",
                            current_digest,
                        ),
                    )
                )

    for source in sources:
        current_digest = _target_digest(destination / source.name)
        if current_digest != source.digest:
            return SyncResult(
                tuple(actions)
                + (
                    Action(
                        "conflict",
                        source.name,
                        "destination changed before synchronization state was recorded; rerun",
                        current_digest,
                    ),
                )
            )
    if prune:
        for action in actions:
            if action.kind not in {"remove", "forget"}:
                continue
            current_digest = _target_digest(destination / action.name)
            if current_digest is not None:
                return SyncResult(
                    tuple(actions)
                    + (
                        Action(
                            "conflict",
                            action.name,
                            "retired destination reappeared before state was recorded; rerun",
                            current_digest,
                        ),
                    )
                )

    next_skills = dict(state["skills"])
    for source in sources:
        next_skills[source.name] = {
            "digest": source.digest,
            "source": source.path.relative_to(source_root).as_posix(),
        }
    if prune:
        for name in set(next_skills) - set(source_by_name):
            del next_skills[name]

    next_state = {
        "schema": STATE_SCHEMA,
        "plugin": "frozen-skills",
        "consumer": consumer,
        "plugin_version": version,
        "skills": next_skills,
    }
    if deployment is not None:
        next_state["deployment"] = deployment
    _write_state(destination, next_state)
    return result


def _expanded_path(value: str) -> Path:
    """Expand user and environment markers in a command-line path."""

    return Path(os.path.expandvars(os.path.expanduser(value)))


def resolve_destination(consumer: str, destination: Path | None) -> Path:
    """Resolve an explicit destination or one verified consumer-private default."""

    if destination is not None:
        return destination
    default = DEFAULT_DESTINATIONS.get(consumer)
    if default is None:
        raise SyncError(
            f"--destination is required for consumer {consumer!r}; no private default "
            "has been qualified"
        )
    return _expanded_path(default)


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""

    parser = argparse.ArgumentParser(
        description=(
            "Synchronize one consumer's frozen-skills distribution, or one named "
            "deployment subset of it, into a local skill root. The command refuses "
            "to overwrite local changes unless --force is supplied."
        )
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="report drift without writing")
    mode.add_argument("--apply", action="store_true", help="apply the synchronization plan")
    parser.add_argument(
        "--consumer",
        choices=tuple(MANIFEST_PATHS),
        help="consumer whose exact shared-plus-restricted distribution should be synchronized",
    )
    parser.add_argument(
        "--deployment",
        help=(
            "named deployment subset from plugins/distribution.json:deployments; "
            "supplies its own consumer and requires explicit --destination and --prune"
        ),
    )
    parser.add_argument(
        "--destination",
        type=_expanded_path,
        help=(
            "local skill root (Codex default: ~/.codex/skills; required otherwise "
            "and always required with --deployment)"
        ),
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
        help=(
            "remove previously managed skills no longer listed in the selected "
            "distribution or deployment"
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="overwrite conflicting local content (use only after reviewing the plan)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the synchronizer and return its documented process status."""

    args = build_parser().parse_args(argv)
    try:
        if args.deployment is not None:
            if args.destination is None:
                raise SyncError(
                    "--deployment requires an explicit --destination; there is no "
                    "default deployment destination"
                )
            if not args.prune:
                raise SyncError(
                    "--deployment requires --prune so the destination converges to "
                    "the exact deployment"
                )
            destination = args.destination
        elif args.consumer is None:
            raise SyncError("One of --consumer or --deployment is required")
        else:
            destination = resolve_destination(args.consumer, args.destination)
        result = sync(
            args.repo_root,
            destination,
            consumer=args.consumer,
            apply=args.apply,
            prune=args.prune,
            force=args.force,
            deployment=args.deployment,
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
        selection = (
            f"deployment {args.deployment}"
            if args.deployment is not None
            else f"{args.consumer} skills"
        )
        print(f"Synchronized {selection} into {destination.resolve()}")
    else:
        print("Local skills match the reviewed frozen-skills distribution.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
