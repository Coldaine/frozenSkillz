# Inventory — context7-cli @ e2f1935 (v0.5.2)

Rust crate, ~10 source modules under `src/`:

| File | Role |
|---|---|
| `api.rs` | HTTP client, `BASE_URL = https://context7.com/api`, key-rotation retry (shuffle + 500ms→1s→2s backoff, 5 attempts) |
| `storage.rs` | Key hierarchy: `CONTEXT7_API_KEYS` env (comma-separated) → XDG `config.toml` (chmod 600); zeroize newtype |
| `cli.rs` | clap commands: `library`/`lib`/`search`, `docs`, `keys add/list/remove`, `health` |
| `health.rs` | key/API health checks |
| `output.rs` | colored / `--json` / `--text` (LLM-context) rendering |
| `i18n.rs` | EN/PT strings |
| `errors.rs`, `platform.rs`, `lib.rs`, `main.rs` | support |

Also: `tests/`, `docs/`, `packaging/`, CI under `.github/`, `deny.toml`, `clippy.toml`,
dual LICENSE, `Cargo.lock` committed. No `build.rs`. No agent-instruction files.
