"""Nightly SKILL.md version ledger.

Sweeps known skill roots, hashes every SKILL.md, and appends a row the first
time each (skill, content-hash) pair is seen, so grades can attach to the skill
version that was actually live. Run before condense.

The ledger is committed on purpose: `first_seen` for a given content hash is
unreconstructable once that SKILL.md is edited and the old bytes leave disk, and
it is the join key that keeps an old grade attached to the version it graded.

Two properties keep it commit-friendly:

- **Append-only.** Existing rows are never rewritten, so a nightly run with no
  skill changes produces no diff at all. There is deliberately no `last_seen`
  field; it would rewrite all 200+ rows every night to record something nothing
  reads. "Which version is current" is answered by the newest `first_seen`.
- **HOME-relative paths.** Rows store `~/...` posix paths, so the ledger carries
  no local username and stays comparable across machines.
"""
import hashlib
import json
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


def _relative(path: Path) -> str:
    """HOME-relative posix form, so no local username enters the ledger."""
    try:
        return "~/" + path.resolve().relative_to(HOME).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def _load_rows() -> dict:
    if not LEDGER.exists():
        return {}
    rows = {}
    for line in LEDGER.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        r = json.loads(line)
        rows[(r["name"], r["sha256"])] = r
    return rows


def sweep():
    today = date.today().isoformat()
    known = _load_rows()
    new_rows = []
    found = 0
    for root in ROOTS:
        if not root.exists():
            continue
        for f in root.rglob("SKILL.md"):
            name = f.parent.name
            sha = hashlib.sha256(f.read_bytes()).hexdigest()[:16]
            found += 1
            key = (name, sha)
            if key in known:
                continue
            row = {"name": name, "sha256": sha, "path": _relative(f),
                   "first_seen": today}
            known[key] = row
            new_rows.append(row)

    if new_rows:
        with LEDGER.open("a", encoding="utf-8") as fh:
            for r in sorted(new_rows, key=lambda r: (r["name"], r["sha256"])):
                fh.write(json.dumps(r) + "\n")

    print(f"swept {found} SKILL.md files, {len(new_rows)} new version(s), "
          f"ledger has {len(known)} (name, version) rows")


def current_hash(name: str) -> str:
    """Newest live hash for a skill name, for condense.py.

    Ties on first_seen (the same version present in several roots or plugin
    caches) resolve to the most canonical root by ROOTS order, then by hash for
    determinism — never by position in the file.
    """
    rows = _load_rows()

    def root_rank(path: str) -> int:
        for i, root in enumerate(ROOTS):
            if path.startswith("~/" + root.relative_to(HOME).as_posix()):
                return len(ROOTS) - i
        return 0

    best, best_key = None, None
    for r in rows.values():
        if r["name"] != name:
            continue
        key = (r["first_seen"], root_rank(r["path"]), r["sha256"])
        if best is None or key > best_key:
            best, best_key = r, key
    return best["sha256"] if best else "unknown"


if __name__ == "__main__":
    sweep()
