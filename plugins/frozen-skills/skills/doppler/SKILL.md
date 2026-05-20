---
name: doppler
description: Doppler secrets management platform. Use when installing or configuring the Doppler CLI, setting up doppler.yaml, running commands with doppler run, adding CI service tokens, debugging secret injection without exposing values, using fallback files, mounting secrets, or managing dev/staging/production configs.
---

# Doppler

Use Doppler as a secrets injection layer. Prefer CLI-driven environment injection (`doppler run -- ...`) over in-process SDK calls, vault enumeration, or committed secret files.

## Operating Rules

- Do not print secret values into transcripts unless the user explicitly asks for the value.
- Prefer names-only or boolean checks: `doppler secrets --only-names`, `test -n "$VAR"`, or PowerShell `if ($env:VAR)`.
- Do not commit `.env`, downloaded secret exports, service tokens, fallback files, or rendered config files containing credentials.
- Use service tokens only in CI/production secret stores, never in repo files.
- Treat `doppler.yaml` as safe repo configuration: it names project/config only.
- Use `doppler run -- ...` for normal application execution. Application code should read ordinary environment variables.
- Use `--silent` for destructive secret-management commands where possible; some CLI versions print a secrets table after mutation.
- For current command syntax, verify with `doppler --version` and `doppler <command> --help` before changing scripts or docs.

## Core Model

| Concept | Meaning |
|---|---|
| Workplace | Top-level Doppler organization |
| Project | Secret namespace for an app, service, or shared secret group |
| Config | Environment within a project, such as `dev`, `stg`, or `prd` |
| Secret | Key-value pair injected into child processes |
| Service token | Revocable token scoped to a project/config for CI or production |
| CLI token | Developer login token saved by `doppler login` |

Resolution order for most CLI commands is service token, explicit flags, local scoped config, then parent scoped config.

## Quick Start

Install:

```shell
# Windows
winget install doppler

# macOS
brew install dopplerhq/cli/doppler

# Linux / CI
(curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh || wget -t 3 -qO- https://cli.doppler.com/install.sh) | sh
```

Set up a repo:

```shell
doppler login
doppler setup -p my-project -c dev
doppler run -- python app.py
```

Commit a team setup file:

```yaml
setup:
  project: my-project
  config: dev

flags:
  analytics: false
  env-warning: false
  update-check: false
```

Then teammates can run:

```shell
doppler setup --no-interactive
doppler run -- your-command
```

## Running Commands

POSIX shells:

```shell
doppler run -- uv run pytest
doppler run -p my-project -c dev -- ./scripts/test.sh
doppler run --command './configure && ./process-jobs'
```

PowerShell:

```powershell
doppler run -- uv run pytest
doppler run -p my-project -c dev -- powershell -NoProfile -File .\scripts\test.ps1
doppler run --command "uv run pytest"
```

Use `--command` for shell operators, pipelines, and command strings. Use `-- ...` for normal argv forwarding.

## Safe Diagnostics

Check active config:

```shell
doppler configure
doppler configure debug
doppler secrets --only-names
```

Check whether a secret is injected without printing the value:

```shell
doppler run -- sh -c 'test -n "$DATABASE_URL" && echo DATABASE_URL=set || echo DATABASE_URL=missing'
```

```powershell
doppler run -- powershell -NoProfile -Command "if ($env:DATABASE_URL) { 'DATABASE_URL=set' } else { 'DATABASE_URL=missing' }"
```

Only use raw value commands for intentional secret handling:

```shell
doppler secrets get SECRET_NAME --plain
```

## Adding Secrets

```shell
doppler secrets set API_KEY value
printf '%s' "$CERT_CONTENTS" | doppler secrets set CERT_PEM
doppler secrets upload secrets.env
```

PowerShell:

```powershell
doppler secrets set API_KEY value
Get-Content -Raw .\cert.pem | doppler secrets set CERT_PEM
doppler secrets upload .\secrets.env
```

Prefer piping multiline values instead of pasting them into shell history.

## CI And Production

Create one service token per project/config and store it in the CI provider's secret store as `DOPPLER_TOKEN`:

```shell
doppler configs tokens create -p my-project -c prd ci-token --plain
```

GitHub Actions pattern:

```yaml
- name: Install Doppler CLI
  run: (curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh || wget -t 3 -qO- https://cli.doppler.com/install.sh) | sh
- name: Run tests
  run: doppler run -- uv run pytest
  env:
    DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
```

Service token project/config takes precedence over `doppler setup` and `-p`/`-c` flags.

## Fallback Files

Doppler may write encrypted fallback/cache files under the configured Doppler directory. Use them for availability, not as repo artifacts.

```shell
doppler run --fallback-only -- ./start.sh
doppler run --no-fallback -- ./start.sh
doppler run clean --dry-run
```

If a fallback must move between build and deploy stages, use a dedicated passphrase from the CI secret store, not a literal in YAML:

```shell
doppler secrets download --passphrase "$DOPPLER_FALLBACK_PASSPHRASE" -p my-project -c prd
doppler run --fallback ./doppler.json --passphrase "$DOPPLER_FALLBACK_PASSPHRASE" -- ./start.sh
```

## Mounting Secrets

`doppler run --mount ...` exposes secrets through an ephemeral mounted file path and does not inject the secrets into the environment. The path is available as `DOPPLER_CLI_SECRETS_PATH`.

```shell
doppler run --mount secrets.json -- cat secrets.json
doppler run --mount .env --mount-format env -- ./start.sh
doppler run --mount config.yml --mount-template config.yml.tmpl -- ./start.sh
```

Some frameworks reject named pipes or ephemeral files. If that happens, use environment injection with plain `doppler run -- ...`.

## References

Load these only when needed:

- [references/commands.md](references/commands.md): command reference, platform notes, and troubleshooting.
- [references/ci-fallbacks.md](references/ci-fallbacks.md): CI, service tokens, fallback files, and Docker patterns.

## Review Checklist

Before promoting or committing Doppler work:

- `doppler --version`
- `doppler configure debug`
- `doppler secrets --only-names`
- Run the target command through `doppler run -- ...`
- Confirm no secret values were added to files, logs, diffs, or transcripts.
