# Generation

You are reading this because you entered Phase 4 with completed reasoning records in hand. Prompts are ASSEMBLED from record fields, never free-prosed; a sound without a record does not reach this file. Project content comes from PROFILE.md; feel comes from Sound_Design.md and the per-sound intent line; this file is the generic craft.

## Physics and layer decomposition (from the record, Field 4)

The components and layers were named in the reasoning record; restate them here only to build the prompt. For weapon and impact sounds, think in layers: attack/transient (under 50ms, the crack), body (100-500ms, the boom), sub (under 80Hz, the felt weight), mechanical (the action: breech, hinge, traverse), tail (environmental decay), sweeteners (secondary reactions). The prompt names components explicitly; that is what separates a specific sound from a generic one. Distance tiers map to layer emphasis: close = all layers with mechanical prominent; mid = body + tail with mechanical attenuated; far = body + sub + tail only, long decay, no mechanical.

## Generation strategy (pick one per sound)

- Single composite: the default for most one-shots and UI.
- Layered stems: P1 hero sounds where weight matters; generate attack, body, and tail as separate clips, log them as stems for a later mixdown pass, wire the best composite meanwhile, and add a stem-mixdown item to the checklist.
- Loop bed: Zone sounds; layered desynced beds when the duration cap forces it.
- Variant set: high-frequency triggers; N per the profile.

## Prompt construction formula

`[Subject with scale] + [action] + [2-3 setting anchors from the profile ALLOWED table] + [listener perspective from Sound_Design.md] + [texture and tail derived from the intent line's feel words and tier rules] + [negative steering: model drift + anti-targets]`

Checks per prompt, all must pass before calling the tool:
- Zero terms from the profile BANNED tables (either direction).
- Zero implied anti-targets from the emotional targets section.
- Tier consistency: descriptor weight matches the tier (see the cohesion pass in references/aesthetic-direction.md).
- Family palette phrases present.

Rules:
- Loops: IF the tool signature has a loop parameter → use it. ELSE append "seamless loop" and note in the log that loop points need trimming.
- Distance tiers: a far-tier prompt describes a different sound (filtered, delayed, elongated, environmental), not the close sound quieter. Write each tier independently, same intent line.
- Variants: vary texture and tail words, never the subject; variants must be interchangeable at one trigger.
- Regeneration: change the prompt materially (perspective, texture emphasis, duration), guided by the reject pattern if one was identified; increment the revision.
- IF the discovered signature exposes prompt_influence → 0.5-0.6 for material-critical sounds (weapons, impacts), 0.2-0.3 for ambience.
- Duration: profile category value clamped to the discovered cap (official ElevenLabs MCP: 5.0s). Ambience beyond the cap → layered beds of 2-3 desynced short loops; treat each layer as its own sound in the inventory.

## Format handling

1. Preflight recorded which output formats the discovered tool accepts. For LOOPS, request WAV/PCM at the source (`output_format=pcm_44100` or the signature's WAV option); that eliminates mp3 seam padding entirely. PCM may be tier-restricted; on rejection fall back to mp3 plus the trim chain below.
2. Trim chain for mp3 loops, in preference order: ffmpeg (decode to WAV, trim edge silence under -60dB); ELSE a Python stdlib script via bash (`wave`/`audioop`: decode, strip encoder padding, rewrap). IF neither exists → loops are `GENERATION FAILED - no audio tooling for loop trim` and are NOT imported: an untrimmed mp3 loop produces a loud percussive click on every wrap and ruins the bed. Importing a known-clicking loop is worse than no loop. One-shots may import as mp3 or WAV freely.
3. Move to the convention path with the convention name BEFORE the AssetDatabase sees it.

## Objective self-audit (always runs; no LLM required)

After every generation, check with ffmpeg/sox if available: near-silence (mean level under -50dBFS), clipping risk (peak above -0.3dBFS), duration mismatch (delivered length off the requested by more than 30 percent), and for loops a seam discontinuity (compare the first and last 10ms). Any failure → regenerate once with the defect named in the revised prompt; still failing → keep the best take and add the flag to the log entry and an auto-flagged checklist item. No audio tooling available → skip silently and rely on human review.

## Listening critic loop (optional, never a blocker)

Scope: run the critic ONLY on P0/P1 moments (T1/T2 hero and core-loop sounds); skip UI clicks and P3 polish to conserve time and credits (the profile may widen or narrow this). IF an audio-capable evaluator is available (multimodal model via CLI or MCP accepting audio files):

1. Send each variant with (a) the profile Sonic Identity, (b) this sound's design intent line, (c) the relevant anti-targets. Ask for: setting fit 1-5 (including a wrong-character check: does anything the prompt excluded, like modern artillery character, come through), intent fit 1-5 (does it FEEL like the intent line, and does it avoid the anti-targets), artifact check (clicks, warble, shimmer, truncation), loop seam audibility for loops. Name the offending element for any score under 4.
2. Keep variants scoring 4+ on both axes with no artifacts. None pass → revise using the named element, regenerate, retries per profile (default 2). Retries spent → `GENERATION FAILED` in the log with the last verdict; continue.
3. One-line verdict goes in the Master Log entry.

ELSE: keep all variants, `Pending Review`; give the human A/B material.

Return to SKILL.md Phase 5.
