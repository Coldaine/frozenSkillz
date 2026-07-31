# Engine Wiring (Unity)

You are reading this because you entered Phase 4 with imported clips. Walk the attach ladder top to bottom for each sound; take the FIRST rung that applies. The ladder always ends in an attachment or a logged reason code. It never waits for a ruling; if a better architecture is warranted, wire by the best available means now and put the recommendation in the run report.

## Attach ladder

1. A sound bank / audio event registry exists (named in the profile AND present on disk) → register the clip(s) and their per-category playback settings there. VERIFY the bank asset saves and reloads with the entries intact.
2. The trigger script already plays a clip (existing AudioSource/PlayOneShot call with a serialized reference) → assign the reference on the prefab. Zero code edits.
3. The trigger script has a serialized but null AudioClip/AudioSource field → assign it. Zero code edits.
4. No hook exists → add an AudioSource to the target prefab (settings per the profile table, `playOnAwake=false` for events, `true`+loop for ambience, one AudioSource per concurrently-audible sound) AND add the minimal hook: one serialized field plus one PlayOneShot call inside the existing method that represents the event. Record the exact diff in the log entry.
5. Target ambiguous (multiple candidate prefabs/scripts) → `UNRESOLVED - needs human mapping`, list all candidates, move to the next sound.

Prefab rules for rungs 2-4: operate on the PREFAB asset, not a scene instance. For prefab variants, wire the base when all variants share the sound; note the choice in the log. VERIFY after every attach: prefab saves, reloads, reference non-null, settings persisted.

## Annotate the site

Every wired sound leaves a note IN THE CODE at its trigger site, tagged `[AUDIO:<InventoryID> rev<N>]` so code, Master Log, and checklist are greppable to each other.

- Rung 4 (hook added): full block comment above the hook: the tag line, the gap (what had no sound and why it matters), the thinking (intent line in plain words: tier, feel, relation), and the clip path with a pointer to the Master Log.
- Rungs 2-3 (reference-only wiring, code untouched otherwise): one line above the play call or serialized field: `// [AUDIO:<ID> rev<N>] <ClipName>: <one-line why>. Full record: docs/audio/Audio_Master_Log.md`.
- Rung 1 (bank registration, no code site): put the tag and the one-line why in the bank entry's notes/description field if it has one; otherwise the log and inventory carry it alone.

Comments are exempt from the code edit limits below; they are always permitted and never count as a hook. Record the annotated file path in the log entry's Site Tag field. On regeneration, update the existing tag's rev in place; never stack duplicate tags.

## Code edit limits (rung 4)

Permitted: one field + one call in an existing method. Forbidden: Update()-driven audio, coroutines, new components beyond AudioSource, restructuring gameplay logic. IF the minimal hook is impossible without restructuring → `NEEDS CODE HOOK` in the checklist with a one-line description of the hook required, move on.

## Failure handling

| Symptom | Action |
|---|---|
| Compile error appears mid-run | HALT all writes immediately. Log the state of every touched asset in the run report. This is one of the three global halts. |
| Clip reference null after save/reload | Prefab variant override conflict likely. `WIRING FAILED` + prefab path; no blind retries. |
| AssetDatabase refresh does not surface the file | Confirm path under Assets/, extension, console import errors. One retry, then `IMPORT FAILED`. |
| Unity MCP write call errors | Stop further writes this run; log touched-asset state in the run report; finish Phase 5 with what succeeded. |

Return to SKILL.md Phase 6 after the batch. Silence proposals wire nothing but still get their site tag as a comment at the transition they shape, when a code site exists.
