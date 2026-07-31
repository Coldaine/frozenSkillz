# Profile Authoring (self-authored, non-blocking)

You are reading this because Preflight found no `docs/audio/PROFILE.md`, or the run learned something the profile should capture. The profile is the project's audio content: setting vocabulary, categories, wiring settings, conventions, budgets. The AGENT writes and maintains it from what the project already contains; it is not an interview gate and it never blocks a run.

## Sources, in priority order

1. Design documents in the repo: extract setting, period, materials, technology level, tone.
2. Existing audio assets and AudioSources: conventions and any distance regime already in force.
3. The user, ONLY IF the repo has neither design docs nor existing audio and the setting is genuinely undeterminable. Then ask ONE batched message (setting + "what should this never sound like" + budget) and proceed with stated defaults if unanswered in-conversation.

## Sections to write (all seven; draft beats absent)

1. Sonic identity: 2-3 sentences: what the world sounds like, what it never sounds like, materials and period.
2. Vocabulary tables: 6-12 ALLOWED anchor phrases; BANNED terms in BOTH directions (too-early/primitive AND too-late/modern). Prompts containing banned terms auto-fail in Phase 2.
3. Category table: one row per category derived from the game's systems (not a generic list): duration, loop y/n, variant count, one example prompt in the allowed vocabulary.
4. Distance tiers: IF gameplay ranges span an order of magnitude → close/mid/far tiers for loud categories (far = a different, filtered, delayed sound, not a quieter one). ELSE state single-tier.
5. Wiring configuration: integration target (sound bank/registry path if one exists; otherwise direct AudioSource, with a run-report recommendation if the project's architecture suggests a bank) plus: the mixer bus map (e.g. Master → Combat/Ambience/UI/Music) with any ducking rules, per-category import settings (load type, mono), and whether AudioRandomContainer is available (Unity 2023.1 / Unity 6 and later; detect by API presence, not version string); and the per-category AudioSource settings table. Calibrate distances against a known-size object in the project; mark UNCALIBRATED if you could not.
6. Conventions: folder taxonomy + filename pattern (adopt existing; invent and record if none), target audio format and conversions.
7. Budgets: per-run generation-call cap (default 60), variants per category (3-5 for high-frequency triggers, 1 for stingers), critic retry cap (default 2).

## Maintenance

The profile is living. When a run calibrates a distance, discovers a convention, or adds a category, update the profile in the same run and note the change in the run report. First-run drafts are expected to be partly provisional; mark provisional values and refine on later runs.

Completed example: `assets/example-profile-broadside.md`.

Return to the SKILL.md phase that sent you here.
