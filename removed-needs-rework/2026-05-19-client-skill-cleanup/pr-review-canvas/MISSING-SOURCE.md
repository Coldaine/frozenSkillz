# pr-review-canvas Missing Source

`pr-review-canvas` was removed from active Claude and Codex references on 2026-05-19.

At cleanup time:

- `C:\Users\pmacl\.claude\skills\pr-review-canvas` was a junction to `C:\Users\pmacl\.agents\skills\pr-review-canvas`.
- `C:\Users\pmacl\.agents\skills\pr-review-canvas` did not exist.
- `C:\Users\pmacl\.codex\skills\pr-review-canvas` did not exist.
- `C:\Users\pmacl\.codex\config.toml` still had disabled entries pointing at both missing paths.

No authoritative `SKILL.md` source was found during the cleanup pass. Recreate or recover this skill before publishing it again.
