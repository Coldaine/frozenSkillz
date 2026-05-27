# Doppler CI, Fallback, And Docker Patterns

Use this reference for CI/CD, service tokens, fallback files, and container workflows.

## Service Tokens

Create read-only tokens for runtime/test jobs and read/write tokens only for jobs that manage secrets.

```shell
doppler configs tokens create -p my-project -c dev ci-dev --plain
doppler configs tokens create -p my-project -c prd deploy-prd --plain
```

Store the token in the CI provider as `DOPPLER_TOKEN`.

The service token determines project/config. Do not rely on `doppler setup` inside CI.

## GitHub Actions

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    env:
      DOPPLER_TOKEN: ${{ secrets.DOPPLER_TOKEN }}
    steps:
      - uses: actions/checkout@v4
      - name: Install Doppler
        run: (curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh || wget -t 3 -qO- https://cli.doppler.com/install.sh) | sh
      - name: Test
        run: doppler run -- uv run pytest
```

## GitLab CI

```yaml
test:
  variables:
    DOPPLER_TOKEN: $DOPPLER_TOKEN
  script:
    - apt-get update && apt-get install -y curl ca-certificates
    - curl -Ls --tlsv1.2 --proto "=https" --retry 3 https://cli.doppler.com/install.sh | sh
    - doppler run -- ./scripts/test.sh
```

## CircleCI Or Restricted Linux Executors

```yaml
- run:
    name: Install Doppler locally
    command: (curl -Ls https://cli.doppler.com/install.sh || wget -qO- https://cli.doppler.com/install.sh) | sh -s -- --no-install --no-package-manager
- run:
    name: Run with secrets
    command: ./doppler run -- ./build.sh
```

## Docker

Environment injection:

```shell
doppler run -- docker run --rm my-image ./start.sh
```

Pass a service token into a container that already has Doppler installed:

```shell
docker run --rm -e DOPPLER_TOKEN my-image doppler run -- ./start.sh
```

Use env-file output only in ephemeral CI contexts where the generated file is not committed:

```shell
doppler secrets download --no-file --format docker > .env.docker
docker run --rm --env-file .env.docker my-image
rm .env.docker
```

## Fallback Files

Fallback files are encrypted snapshots for availability. They are not source artifacts.

```shell
doppler run -- ./start.sh
doppler run --fallback-only -- ./start.sh
doppler run --no-fallback -- ./start.sh
doppler run clean --dry-run
doppler run clean --all
```

Cross-token fallback pattern:

```shell
doppler secrets download --passphrase "$DOPPLER_FALLBACK_PASSPHRASE" -p my-project -c prd ./doppler.json
doppler run --fallback ./doppler.json --passphrase "$DOPPLER_FALLBACK_PASSPHRASE" -- ./start.sh
```

Never hardcode the fallback passphrase. Store it in the CI provider or deployment secret store.

## Anti-Patterns

- Committing `.env`, `doppler.json`, rendered config files with credentials, or service tokens.
- Printing `doppler run -- printenv` in logs.
- Using `--no-verify-tls` outside a temporary diagnostic.
- Assuming mounted secrets are also injected into the environment.
- Using one production service token across unrelated jobs or repositories.
