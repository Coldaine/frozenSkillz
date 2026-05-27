# Graphite Command Map

This skill should route users toward the smallest `gt` command that preserves a coherent stack.

## Core Lifecycle

| Situation | Preferred command |
|----------|-------------------|
| Repo not initialized | `gt init` |
| Create next slice on top of current branch | `gt create` |
| Update current slice and keep descendants aligned | `gt modify` |
| Publish or refresh PRs | `gt submit` |
| Publish whole stack | `gt submit --stack` |
| Pull trunk and restack what can be restacked | `gt sync` |
| View stack | `gt log short` / `gt ls` |
| Open current PR or stack page | `gt pr` / `gt pr --stack` |

## Repair And Restructuring

| Situation | Preferred command |
|----------|-------------------|
| Branch exists but Graphite metadata is missing or wrong | `gt track` |
| Child is attached to wrong parent | `gt move --onto <parent>` |
| Linear order is wrong between trunk and current branch | `gt reorder` |
| One branch should become several | `gt split` |
| Branch should become one commit | `gt squash` |
| Staged hunks belong in older commits | `gt absorb` |
| Branch should disappear but keep file state | `gt pop` |
| Branch should disappear and descendants should be restacked | `gt delete` or `gt fold` |

## Navigation

| Goal | Command |
|------|---------|
| Go to parent | `gt down` |
| Go to child | `gt up` |
| Go to stack root near trunk | `gt bottom` |
| Go to stack tip | `gt top` |
| Open branch picker | `gt checkout` |

## Multi-Machine Collaboration

| Situation | Preferred command |
|----------|-------------------|
| Pull remote branch or stack to this machine | `gt get` |
| Build on top of someone else's branch without editing it | `gt freeze` |
| Resume editing a frozen branch | `gt unfreeze` |

## Verification

Use these commands before deciding a stack is healthy:

```bash
gt log short
gt info --diff --stat
gt submit --dry-run --stack
```

If local scripts are available, also run the parent-diff verifier and PR base audit helpers.
