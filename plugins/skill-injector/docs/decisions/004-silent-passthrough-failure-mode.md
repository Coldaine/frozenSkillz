# ADR-004: Silent Passthrough as the Only Failure Mode

**Status:** Accepted
**Date:** 2026-02-08
**Deciders:** pmacl

## Context

The classifier hook sits in the critical path between the user pressing Enter and Claude receiving the prompt. Any failure — network timeout, missing CLI, malformed LLM response, no matching skills — needs a defined behavior.

Options:
1. **Silent passthrough** — exit with zero output. Claude never knows the hook ran.
2. **Error reporting** — output an error message that Claude or the user sees.
3. **Retry** — retry the LLM call on failure.
4. **Fallback to keywords** — if LLM fails, try keyword matching.

## Decision

Silent passthrough on every failure path. No exceptions.

## Rationale

### No suggestion is better than a wrong suggestion

A wrong skill suggestion trains the user to distrust and eventually disable the hook. A missing suggestion has no cost — the user never knew one was possible. The asymmetry is stark:

| Outcome | User Experience | Trust Impact |
|---------|----------------|-------------|
| Correct suggestion | Skill activates, better outcome | Builds trust |
| No suggestion | Normal Claude behavior | Neutral |
| Wrong suggestion | Claude loads wrong skill, wasted time | Erodes trust |
| Error message | User sees "hook failed" noise | Erodes trust |
| Delay from retry | User waits longer for no benefit | Erodes trust |

Three of four failure modes erode trust. Only silence is neutral.

### Hooks must never block the prompt

A user who types a prompt expects Claude to respond. If the hook hangs, errors loudly, or retries, it blocks that expectation. The hook is an enhancement, not a gate — if it can't enhance, it must get out of the way.

### Implementation: every function returns early

Every function in the pipeline has an empty-return path:

```python
def main():
    try:
        payload = json.loads(sys.stdin.read())
    except Exception:
        return  # Can't parse input → silent

    skills = get_skills()
    if not skills:
        return  # No skills found → silent

    suggested = classify(prompt, context, skills)
    if not suggested:
        return  # LLM returned nothing → silent

    # Only reach output if everything succeeded
    json.dump(output, sys.stdout)
```

Errors are logged to stderr (visible in debug mode, invisible to the user and to Claude).

### Retry is worse than silence

The Gemini CLI takes ~10s per call. A retry would add another 10s. Even with the REST API (~300ms), a retry adds latency with no guarantee of success (if the network is down, it's still down). The calculus never favors retrying.

### Keyword fallback defeats the purpose

If we added a keyword fallback for when the LLM fails, we'd need to maintain a keyword map — which is exactly what ADR-001 decided against. The fallback would also have lower accuracy, meaning it would fire precisely when the primary system failed, giving the user a worse experience when things are already going wrong.

## Consequences

- **Positive:** The hook can never degrade the user experience. At worst, it has no effect.
- **Positive:** Simple error handling — every error path does the same thing (return).
- **Negative:** When the backend is down, the user gets zero skill suggestions with no indication why. They might not even know the hook exists. This is by design — the hook should be invisible infrastructure, not a visible feature.
