# PDM CLI operations evals

Labeled prompts for description routing. See `triggers.json`.

## How to run

1. Use a fresh agent session per prompt (no prior PDM context).
2. Record whether `$pdm-cli-operations` (or equivalent) was loaded.
3. Score: trigger rate ≥ 0.5 when `should_trigger` is true; < 0.5 when false.
4. Do not rewrite the skill description solely to fit the validation split.

## Negatives to protect

- Native PVE/PBS break-glass (`qm`, `pvesh`, node SSH) when the user did not ask for PDM.
- Installing WSL or a container only to obtain the PDM client.
- Ordinary app config / cloud infra unrelated to the standing PDM API.
