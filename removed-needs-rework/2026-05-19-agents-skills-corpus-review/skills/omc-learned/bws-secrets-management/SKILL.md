---
name: bws-secrets-management
description: >
  How Bitwarden Secrets Manager (BWS) works, CLI commands, SDK usage,
  and how this user manages secrets across all projects. BWS_ACCESS_TOKEN
  is always in the environment. Secrets are stored locally and loaded
  instantly — no cloud calls on startup.
triggers:
  - BWS
  - bitwarden
  - secret
  - secrets
  - API key
  - access token
  - credential
  - env var secret
  - rotate secret
  - add secret
  - Sync-FromBWS
  - bws run
  - bws secret
  - MCP server secret
  - missing API key
---

# Bitwarden Secrets Manager (BWS)

## What BWS Is

Bitwarden Secrets Manager is a secrets management service for storing API keys, tokens, passwords, and certificates. Secrets are organized into **projects** and accessed via **machine accounts** with scoped access tokens.

- **BWS CLI** (`bws`): Rust-based CLI for scripting and injection
- **BWS SDK**: Bindings for Rust, Python, Node.js, C#, Go, Java, PHP, Ruby
- **`bws run`**: Injects all project secrets as env vars into a child process

---

## Authentication

BWS authenticates via an access token tied to a machine account.

```bash
# Set once — this user always has it in the environment
export BWS_ACCESS_TOKEN="0.xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx.xxxxx:xxxxx=="

# Or pass inline per command
bws secret list --access-token <TOKEN>
```

**On this machine**: `BWS_ACCESS_TOKEN` is stored in Windows Credential Manager and loaded into the environment automatically on every terminal open. No manual setup needed.

---

## CLI Quick Reference

### Secrets

```bash
bws secret list                          # List all accessible secrets
bws secret list <PROJECT_ID>             # List secrets in a project
bws secret get <SECRET_ID>               # Get a single secret (JSON)
bws secret get <SECRET_ID> -o yaml       # Get as YAML
bws secret create <KEY> <VALUE> <PROJECT_ID>            # Create
bws secret create <KEY> <VALUE> <PROJECT_ID> --note "x"  # Create with note
bws secret edit <SECRET_ID> --value <NEW_VALUE>          # Update value
bws secret delete <SECRET_ID>            # Delete
bws secret delete <ID1> <ID2>            # Delete multiple
```

### Projects

```bash
bws project list                         # List all projects
bws project get <PROJECT_ID>             # Get project details
bws project create "<NAME>"              # Create project
bws project edit <PROJECT_ID> --name "x" # Rename
bws project delete <PROJECT_ID>          # Delete
```

### Inject Secrets as Env Vars (`bws run`)

This is the killer feature. Runs any command with all project secrets injected as environment variables:

```bash
bws run -- 'npm run start'                           # Inject all secrets
bws run --project-id <ID> -- 'docker compose up -d'  # Filter by project
bws run --no-inherit-env -- 'my-app'                  # Clean env (only secrets)
bws run --shell fish -- 'echo $MY_SECRET'             # Specific shell
```

By default, secret **names** become env var names. For POSIX-safe names:
```bash
bws run --uuids-as-keynames -- 'your-command'
# or
export BWS_UUIDS_AS_KEYNAMES=true
```

### Output Formats

```bash
bws secret list -o json    # Default
bws secret list -o yaml
bws secret list -o table
bws secret list -o tsv
bws secret list -o env     # KEY=VALUE format — great for .env generation
bws secret list -o none
```

### Configuration & Profiles

```bash
bws config server-base https://vault.bitwarden.eu          # Self-hosted
bws config server-base http://dev.example.com --profile dev # Named profile
bws secret get <ID> --profile dev                           # Use profile
```

---

## SDK (Programmatic Access)

Core SDK is Rust. Language bindings available:

**Python:**
```bash
pip install bws-sdk  # or: uv add bws-sdk
```

```python
from bws_sdk import BitwardenClient, SecretIdentifierRequest

client = BitwardenClient()
client.access_token_login(access_token)
secret = client.secrets.get(SecretIdentifierRequest(id="<uuid>"))
print(secret.value)
```

**Node.js:**
```bash
npm install @bitwarden/sdk-napi
```

**Other languages**: C#, Go, Java, PHP, Ruby — see [sdk-sm repo](https://github.com/bitwarden/sdk-sm).

---

## How This User Manages Secrets

### The Pattern (Local-First, No Cloud on Startup)

```
BWS Cloud ──(one-time sync)──► Local Credential Store ──(every shell open)──► Env Vars
                                (encrypted at rest)                            (instant)
```

| Phase | When | What Happens |
|-------|------|-------------|
| **Sync** | Once, or on rotation | Fetch secrets by UUID → local credential store |
| **Load** | Every terminal open | Read local store → set env vars (<10ms) |

No cloud calls on startup. Terminal opens instantly.

### Windows Commands (PowerShell)

| Command | What It Does |
|---------|-------------|
| `Sync-FromBWS` | Fetch managed secrets from BWS → Credential Manager |
| `Sync-FromBWS -UserLevel` | Same + persist to `HKCU\Environment` (for IDEs/MCP) |
| `Add-Secret NAME VALUE` | Store in Credential Manager + set session env var |
| `Add-Secret NAME VALUE -UserLevel` | Same + persist for IDE processes |
| `Remove-Secret NAME` | Remove from Credential Manager + env |
| `Load-Secrets` | Read Credential Manager → session env vars (auto on startup) |
| `secrets` | List all managed secrets and their status |

### Linux Commands (Bash — KeePassXC)

| Command | What It Does |
|---------|-------------|
| `sync-from-bws` | Fetch managed secrets from BWS → KeePassXC |
| `add-secret NAME VALUE` | Store in KeePassXC + set session env var |
| `remove-secret NAME` | Remove from KeePassXC + env |
| `load-secrets` | Read KeePassXC → session env vars (auto on startup) |
| `secrets` | List managed secrets and status |

### Bootstrap (New Machine)

```powershell
# Windows
Add-Secret BWS_ACCESS_TOKEN '<token>'
Sync-FromBWS -UserLevel

# Linux (KeePassXC must be running)
add-secret BWS_ACCESS_TOKEN '<token>'
sync-from-bws
```

---

## MCP Server Secrets

MCP servers need API keys. Here's the correct approach:

**Do NOT use `env` blocks in mcp.json for secrets.** VS Code does not expand `${VAR}` in env blocks — it passes the literal string.

**Do use environment variable inheritance.** MCP servers are child processes of the IDE. They inherit all env vars from the parent:

```
User-level env var (HKCU\Environment)
  → IDE inherits at launch
    → MCP server child process inherits from IDE
```

```json
// CORRECT — no env block needed, secrets come from environment
{
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": ["-y", "exa-mcp-server"]
    }
  }
}
```

**To add an MCP secret:**
1. Add the secret to BWS (if not already there)
2. Sync with `-UserLevel` so it persists in `HKCU\Environment`
3. **Full restart** of VS Code / Codex (not just reload)

**Why user-level?** Apps launched from Start Menu, File Explorer, or IDE extensions don't inherit terminal session vars. Only `HKCU\Environment` (Windows) works universally.

---

## Common Patterns

### Get a secret value in a script
```bash
MY_KEY=$(bws secret get <UUID> | jq -r '.value')
```

### Generate a .env file
```bash
bws secret list -o env > .env
```

### Docker with BWS
```bash
docker run -e BWS_ACCESS_TOKEN=$BWS_ACCESS_TOKEN myimage
# Inside Dockerfile entrypoint:
# export DB_PASS=$(bws secret get <UUID> | jq -r '.value')
```

### CI/CD (GitHub Actions)
```yaml
- uses: bitwarden/sm-action@v2
  with:
    access_token: ${{ secrets.BWS_ACCESS_TOKEN }}
    secrets: |
      SECRET_UUID > MY_ENV_VAR
```

---

## Troubleshooting

**"bws: command not found"**: Install from [github.com/bitwarden/sdk-sm/releases](https://github.com/bitwarden/sdk-sm/releases) and add to PATH.

**"Unauthorized"**: Check `BWS_ACCESS_TOKEN` is set and the machine account has access to the target project.

**MCP server missing API key**: Secret needs to be user-level (`HKCU\Environment`), not just session-scoped. Run `Sync-FromBWS -UserLevel` then fully restart the IDE.

**Secret not loading in terminal**: Run `secrets` to check status. Run `Load-Secrets` manually if needed.
