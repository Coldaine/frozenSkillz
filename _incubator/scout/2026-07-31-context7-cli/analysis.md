# Analysis — context7-cli (2026-07-31)

Scope: single question — is this safe and functional as the key-rotation transport for the
`context7-mcp` rewrite? Full artifact rubric not run; this is a tool intake, not a skill intake.

## Security read (source, pinned `e2f1935`)

- **Network:** exactly one endpoint in code — `https://context7.com/api` (`src/api.rs:18`).
  The only other URL in `src/` is a github.com link in help text. No telemetry, no update
  checks, no secondary hosts.
- **Process execution:** none. No `Command::new`/`spawn` anywhere; the binary never runs
  other programs. No `build.rs`.
- **Key handling:** keys wrapped in a zeroize-on-drop newtype; config written
  `chmod 600` to XDG path; keys masked in logs/list output. Env override
  `CONTEXT7_API_KEYS` (comma-separated) read at runtime (`src/storage.rs:216`).
- **Dependencies:** pinned versions in Cargo.toml + committed Cargo.lock; standard crates
  (reqwest, clap, serde, tokio, zeroize). `deny.toml`/`clippy.toml` present.
- **Supply chain:** crates.io package matches the repo (v0.5.2, same repository field,
  343 downloads). Single author (proton.me address), repo created and pushed in one day
  (2026-07-15), 0 stars — young and unvetted by community, which is why we build from this
  reviewed snapshot rather than trusting release binaries.

## Function

- `context7 library <name>` / `context7 docs <id> --query ... --text` — the `--text` mode
  is explicitly designed for LLM context windows; `--json` for pipes.
- **Multi-key rotation:** keys from env or config are shuffled per run; on rate-limit the
  client retries with exponential backoff (500ms→1s→2s, up to 5 attempts) rotating through
  keys. This directly addresses the standing `context7-mcp` failure (quota-blocked in 10+
  sessions per the 2026-07-31 regrade).
- Windows x86_64 supported; single static binary; bilingual EN/PT (comments are PT).

## Fit

Replaces the context7 **MCP server** in agent workflows: agents shell out to the CLI
instead of loading an MCP that 27/39 sessions never used. The rewritten skill becomes a
thin routing instruction over this binary. Owner note: multi-key rotation multiplies
free-tier quota — ToS-gray with Upstash/Context7; owner's call, recorded here.
