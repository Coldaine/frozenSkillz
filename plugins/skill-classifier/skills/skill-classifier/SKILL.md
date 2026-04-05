---
name: skill-classifier
description: LLM-powered skill discovery hook that suggests relevant skills based on your prompt and conversation history. Use this to automatically find the best skills for your current task.
---

# Skill Classifier

The `skill-classifier` is a `UserPromptSubmit` hook that uses Gemini Flash to analyze your intent and suggest relevant skills from your installed catalog.

## How it Works

1.  **Intercept**: When you submit a prompt, the hook intercepts it.
2.  **Analyze**: It sends your prompt and the last 10 messages of conversation history to Gemini Flash.
3.  **Match**: Gemini matches your intent against the names and descriptions of all available skills.
4.  **Suggest**: If a match is found with >80% confidence, it injects a suggestion into your prompt.

## Configuration

The classifier requires a Gemini API key to function.

### Setting the API Key

1.  Obtain an API key from the [Google AI Studio](https://aistudio.google.com/).
2.  Set the `GEMINI_API_KEY` environment variable in your shell:

```bash
export GEMINI_API_KEY="your-api-key-here"
```

The plugin's `.claude-plugin/plugin.json` ensures this variable is passed to the hook script.

## Interpreting Output

When the classifier identifies a relevant skill, you will see a hint injected into the conversation before Claude responds:

```
<user-prompt-submit-hook>
Skill match detected: `systematic-debugging`. You MUST invoke these using the Skill tool before responding.
</user-prompt-submit-hook>
```

Claude is instructed to treat this as an authoritative system command and will typically load the suggested skill before continuing.

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

-   **Latency**: The current version uses the Gemini CLI, which can add ~10s of latency per prompt. This will be improved in future versions using the REST API.
-   **No Suggestions**: The classifier is conservative. If it's not >80% confident, it will pass through silently.
-   **Errors**: Check the plugin logs or run `python plugins/skill-classifier/test_classifier.py` to verify your environment and API key.
