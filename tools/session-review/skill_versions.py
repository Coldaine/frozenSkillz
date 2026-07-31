"""Nightly SKILL.md version ledger.

Sweeps known skill roots, hashes every SKILL.md, and upserts a JSONL ledger so
grades can attach to the skill version that was actually live. Run before condense.
"""
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

HOME = Path.home()
ROOTS = [
    HOME / ".agents" / "skills",
    HOME / ".claude" / "skills",
    HOME / ".cursor" / "skills",
    HOME / ".cursor" / "skills-cursor",
    HOME / ".codex" / "skills",
    HOME / ".codex" / "plugins" / "cache",
]
LEDGER = Path(__file__).parent / "skill-versions.jsonl"


def sweep():
    today = date.today().isoformat()
    rows = {}
    if LEDGER.exists():
        for line in LEDGER.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            rows[(r["name"], r["sha256"])] = r
    found = 0
    for root in ROOTS:
        if not root.exists():
            continue
        for f in root.rglob("SKILL.md"):
            name = f.parent.name
            sha = hashlib.sha256(f.read_bytes()).hexdigest()[:16]
            key = (name, sha)
            if key in rows:
                rows[key]["last_seen"] = today
            else:
                rows[key] = {"name": name, "sha256": sha, "path": str(f),
                             "first_seen": today, "last_seen": today}
            found += 1
    with LEDGER.open("w", encoding="utf-8") as fh:
        for r in sorted(rows.values(), key=lambda r: (r["name"], r["first_seen"])):
            fh.write(json.dumps(r) + "\n")
    print(f"swept {found} SKILL.md files, ledger has {len(rows)} (name, version) rows")


def current_hash(name: str) -> str:
    """Latest live hash for a skill name, for condense.py."""
    if not LEDGER.exists():
        return "unknown"
    best = None
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if r["name"] == name and (best is None or r["last_seen"] >= best["last_seen"]):
            best = r
    return best["sha256"] if best else "unknown"


if __name__ == "__main__":
    sweep()
