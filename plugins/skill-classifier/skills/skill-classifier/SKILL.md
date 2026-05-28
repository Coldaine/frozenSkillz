---
name: skill-classifier
description: LLM-powered skill discovery hook that suggests relevant skills based on your prompt and conversation history. Use this to automatically find the best skills for your current task.
---

# Skill Classifier

The `skill-classifier` is a `UserPromptSubmit` hook that uses a small, fast LLM to
analyze your intent and suggest relevant skills from your installed catalog. The
LLM backend is swappable — **Ollama** (local) by default, with the **Gemini CLI**
as a fallback.

## How it Works

1.  **Intercept**: When you submit a prompt, the hook intercepts it.
2.  **Analyze**: It sends your prompt and the last 10 messages of conversation
    history to the configured LLM backend.
3.  **Match**: The model matches your intent against the names and descriptions
    of all available skills.
4.  **Suggest**: If a match is found with >80% confidence, it injects a
    suggestion into your prompt.

## Configuration

Backend selection and configuration are documented in detail in the plugin
[`README.md`](../../README.md). Quick reference:

| Env var | Default | Purpose |
| --- | --- | --- |
| `SKILL_CLASSIFIER_BACKEND` | `auto` | `ollama`, `gemini`, or `auto` (try Ollama, then Gemini) |
| `SKILL_CLASSIFIER_MODEL` | `llama3.2:3b` | Ollama model tag |
| `OLLAMA_HOST` | `http://localhost:11434` | Ollama server URL |
| `GEMINI_API_KEY` | — | Required only for the Gemini fallback |

### Default: Ollama (local, no API key)

1.  Install [Ollama](https://ollama.com) and pull a small model:
    ```bash
    ollama pull llama3.2:3b
    ```
2.  Make sure the Ollama server is running (`ollama serve`, or the desktop app).

That's it — no API key, no Python packages (the backend uses only the standard
library). If Ollama is not running, the hook fails fast (~1s) and silently
passes through.

### Fallback: Gemini CLI

1.  Install the `gemini` CLI and obtain a key from
    [Google AI Studio](https://aistudio.google.com/).
2.  Set the `GEMINI_API_KEY` environment variable:
    ```bash
    export GEMINI_API_KEY="your-api-key-here"
    ```

In `auto` mode the classifier uses Ollama when reachable and otherwise falls
back to Gemini.

## Interpreting Output

When the classifier identifies a relevant skill, you will see a hint injected
into the conversation before Claude responds:

```
<user-prompt-submit-hook>
Skill match detected: `systematic-debugging`. You MUST invoke these using the Skill tool before responding.
</user-prompt-submit-hook>
```

Claude is instructed to treat this as an authoritative system command and will
typically load the suggested skill before continuing.

## Example Usage

### Scenario: Debugging
**User**: "I'm getting a 401 error in my login flow and I've checked the headers but everything looks right."
**Classifier**: Detects `systematic-debugging` is relevant.
**Claude**: Loads `systematic-debugging` and begins a structured investigation.

### Scenario: Planning
**User**: "Let's map out how to implement the new payment gateway."
**Classifier**: Detects `writing-plans` is relevant.
**Claude**: Loads `writing-plans` to help structure the implementation strategy.

## Troubleshooting

-   **Latency**: With Ollama resident, round-trip is typically well under 2s. The
    Gemini CLI adds process-startup latency (~8s on Windows), so it is best kept
    as a fallback. A down/unreachable Ollama is detected with a fast TCP
    pre-check (~1s) so the hook never stalls a prompt.
-   **No Suggestions**: The classifier is conservative. If it's not >80%
    confident, it will pass through silently.
-   **Errors**: Run `python plugins/skill-classifier/test_classifier.py` to verify
    your environment, or `python plugins/skill-classifier/test_llm_backend.py`
    for the backend unit tests. Set `SKILL_CLASSIFIER_BACKEND` explicitly to
    diagnose a specific backend.
