---
paths:
  - "ansible/**/*.yml"
---

# Ansible Playbook & Role Rules

## Playbook Header

Every playbook in `ansible/playbooks/` **MUST** have a comment header:

```yaml
---
# playbook-name.yml
# One-line description
#
# Usage:
#   ansible-playbook playbooks/name.yml --ask-vault-pass
#   ansible-playbook playbooks/name.yml -l hostname --ask-vault-pass
#
# What it does:
#   1. Step one
#   2. Step two
#
# Prerequisites:
#   - List prerequisites
```

## Rules

- **NEVER hardcode secrets** in playbooks, roles, or templates. Secrets come from a secret store.
- **NEVER run playbooks** from an AI agent — tell the user to run the command manually.
- **ALWAYS use `--ask-vault-pass`** in usage examples when vault-encrypted variables are involved.
- **ALWAYS use `--limit` / `-l`** when targeting a single machine. Never default to all hosts.

## Host Vars & Group Vars

- `ansible/inventory/host_vars/<hostname>.yml` — per-machine variables.
- `ansible/group_vars/all/` — shared variables.
- If the project uses a database as source of truth, YAML files are for Ansible-specific variables only.

## Templates

- Templates live in `ansible/roles/<role>/templates/`.
- **ALWAYS test Jinja2 filter precedence** — use parentheses for compound expressions.

## Archived Playbooks

`ansible/playbooks/archive/` contains deprecated playbooks. To revive one:
1. Move it to `ansible/playbooks/`
2. Update all template paths
3. Update the header with current usage
