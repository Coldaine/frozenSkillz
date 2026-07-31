# Aesthetic Direction

You are reading this because you entered Phase 2. This is the sound designer reasoning layer: decide what everything should FEEL like before anything is generated, so a batch of AI clips reads as one deliberately designed game. Functional coverage without this layer produces a stock-library grab bag.

## The design doc

Load `docs/audio/Sound_Design.md`; author it on first run from the design docs' tone and pillars, the profile's sonic identity, and any reference titles the user has named. Living document, agent-maintained, never a blocking gate. ALL six sections required; draft beats absent:

1. Listener perspective. One sentence naming exactly where the listener sits (deck-level, god-cam at tactical height, cockpit). Every clip is described from this position; a deck-level main gun and a god-cam main gun are different sounds. IF multiple camera modes → pick the dominant one, note how the exception is handled.
2. Emotional targets, keyed as an experience-to-feel map: for each experience type the game uses (Feedback, Threat, Reward, Immersion, Tension, Release), 2-3 target adjectives + at least 1 anti-target per scope. Field 2 of every reasoning record pulls its feel words from this map. Anti-targets are enforced like banned terms: a prompt whose texture words imply the anti-target fails the check in Phase 3.
3. Mix hierarchy. Tiers T1 (owns the moment; everything else conceptually ducks) through T4 (bed; never consciously noticed). Assign every profile category a tier. Note frequency ownership per tier so descriptions do not fight: a T1 weapon gets "deep, dominant low end"; a T3 UI click gets "small, dry, mid-high, no tail".
4. Palette cohesion rules. 2-4 traits every clip in a family shares (tail character, air/space, wet/dry, grit level). These become mandatory phrases in every prompt of that family.
5. Dynamics plan. Name the loudest moment and the quietest. State where silence and contrast are designed beats, and mark gaps that must NOT be filled with sound; these seed the silence-proposal route in Phase 3.
6. Reference anchors. 2-4 named works to emulate and 1-2 to avoid, each with WHAT specific quality is borrowed or refused (not "sounds like X" but "X's sense of distance-delayed heavy gunfire").

## Per-sound design intent

The intent line is derived from the reasoning record (Field 2 feel words + Field 6 tier and relations). For every sound, BEFORE its prompt, write one line:
`[tier] | feel: <2-3 words from the targets> | relation: <contrast/layer/sibling note>`
Example: `T1 | feel: weighty, concussive | relation: dwarfs secondaries; splash answers it seconds later`.
Copy the line into the Master Log entry's Design Intent field. Its words are the source for the prompt's texture-and-tail section in Phase 3.

## Batch cohesion pass

Read the batch's reasoning records, intent lines, and draft prompts as a SET (silence proposals included; a designed silence adjacent to a huge sound is a relation both rows must state):
- VERIFY every clip family carries its mandatory palette phrases.
- VERIFY tier logic: no T3/T4 prompt uses dominant/huge/powerful descriptors; no two categories claim the same frequency ownership at the same tier.
- VERIFY relations are reciprocal: if A dwarfs B, B's prompt must read smaller than A's.
IF a check fails → fix the prompt. IF the doc itself is wrong → fix the doc and note the change in the run report.

## Feedback maintenance

When the human's deletions share a cause (all rejects read "too arcade", "too clean"), that is aesthetic feedback, not just per-clip rejection: update the emotional targets or palette rules in the same run, note it in the run report, and apply the updated doc to the regenerations.

Return to SKILL.md (the phase that sent you here).
