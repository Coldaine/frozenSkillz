#!/usr/bin/env python3
"""Deploy a reviewed skill outward from frozenSkillz to a runtime skill root."""

from __future__ import annotations

import argparse
import hashlib
import shutil
import tempfile
from pathlib import Path
from typing import Sequence


IGNORED = {"__pycache__", ".DS_Store"}


def validate_direction(source: Path, destination: Path) -> None:
    source = source.resolve()
    destination = destination.resolve()
    if source == destination or source in destination.parents:
        raise ValueError("destination must be outside the repository source skill")
    if destination in source.parents:
        raise ValueError("refusing reverse synchronization into the repository source")


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def tree_files(root: Path) -> dict[str, str]:
    if not root.exists():
        return {}
    return {
        str(path.relative_to(root)).replace("\\", "/"): file_hash(path)
        for path in root.rglob("*")
        if path.is_file() and not any(part in IGNORED for part in path.parts)
    }


def trees_match(source: Path, destination: Path) -> bool:
    return tree_files(source) == tree_files(destination)


def validate_source_skill(source: Path) -> None:
    if not source.joinpath("SKILL.md").is_file():
        raise ValueError(f"source is not a skill: {source}")


def deploy(source: Path, destination: Path, *, force: bool = False) -> None:
    validate_direction(source, destination)
    validate_source_skill(source)
    if destination.exists() and not trees_match(source, destination) and not force:
        raise ValueError("destination drift detected; inspect it or pass --force to replace it from frozenSkillz")
    if destination.exists() and trees_match(source, destination):
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=destination.parent) as tmp:
        staged = Path(tmp) / destination.name
        shutil.copytree(source, staged, ignore=shutil.ignore_patterns(*IGNORED))
        backup = Path(tmp) / "previous"
        if destination.exists():
            destination.replace(backup)
        try:
            staged.replace(destination)
        except OSError:
            if backup.exists() and not destination.exists():
                backup.replace(destination)
            raise


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill")
    parser.add_argument("--target-root", type=Path, default=Path.home() / ".agents/skills")
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)
    source = args.repo_root / "plugins/frozen-skills/skills" / args.skill
    destination = args.target_root / args.skill
    validate_direction(source, destination)
    validate_source_skill(source)
    if args.check:
        print("synced" if trees_match(source, destination) else "drift")
        return 0 if trees_match(source, destination) else 1
    deploy(source, destination, force=args.force)
    print(f"deployed {source} -> {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
