#!/usr/bin/env python3
"""Verify the pinned chat-history source registry against an llm-archiver checkout."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path
from typing import Sequence


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(registry_path: Path, upstream: Path) -> list[str]:
    registry = json.loads(registry_path.read_text(encoding="utf-8"))
    findings: list[str] = []
    for item in registry["imports"]:
        path = upstream / item["path"]
        if not path.is_file():
            findings.append(f"missing: {item['path']}")
        elif sha256(path) != item["sha256"]:
            findings.append(f"changed: {item['path']}")
    try:
        commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=upstream, check=True, capture_output=True, text=True).stdout.strip()
        if commit != registry["upstream"]["commit"]:
            findings.append(f"upstream commit moved: {registry['upstream']['commit']} -> {commit}")
    except (OSError, subprocess.CalledProcessError):
        findings.append("unable to read upstream git commit")
    return findings


def default_upstream(repo: Path) -> Path:
    configured = os.environ.get("LLM_ARCHIVER_PATH")
    if configured:
        return Path(configured).expanduser()
    sibling = repo.parent / "llm-archiver"
    return sibling if sibling.exists() else Path.home() / "llm-archiver"


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    repo = Path(__file__).resolve().parents[1]
    parser.add_argument("--registry", type=Path, default=repo / "plugins/frozen-skills/skills/chat-history/references/source-registry.json")
    parser.add_argument("--upstream", type=Path, default=default_upstream(repo), help="llm-archiver checkout; defaults to LLM_ARCHIVER_PATH, a sibling checkout, then ~/llm-archiver")
    args = parser.parse_args(argv)
    findings = verify(args.registry, args.upstream)
    if findings:
        print("registry drift detected")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print("registry snapshot matches imported llm-archiver files and commit")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
