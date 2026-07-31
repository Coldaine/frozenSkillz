# The Reasoning Record: What the Agent Thinks Per Moment

You are reading this because you entered Phase 3 with candidate moments in hand. For every moment, fill ALL six fields before anything downstream. A blank field sends the moment to the checklist as UNRESOLVED; it never sends a prompt to the generator. The record is copied into the Master Log entry; it is the longitudinal memory of why every sound exists.

## Field 1: Moment description
What is happening, concretely, in one or two lines. Include actors, distances, and context.

## Field 2: Player experience and intent
What is this moment telling the player, and what should they FEEL? Name every experience type that applies:
- Feedback: "I did a thing" (fired, clicked, dealt damage)
- Threat: "something dangerous is happening" (incoming fire, flooding)
- Reward: "I succeeded" (enemy sunk, objective complete)
- Immersion: "I am in a place" (sea state, engine room, wind)
- Tension: "something is about to happen" (ranging, reload, the approach)
- Release: "the tension broke" (post-battle quiet, survival)
A moment usually carries more than one; name them all. Then pull the matching feel words from the design doc's experience-to-feel map; those become the design intent line (`tier | feel | relation`).

## Field 3: IEZA slot
Interface (non-diegetic action feedback: 2D, short, UI routing, 1-3 variants) | Effect (diegetic action: 3D, 3-6 variants, may duck others) | Zone (diegetic ambient: loop beds, ambience routing) | Affect (non-diegetic mood: 2D, snapshot-aware; musical Affect is out of scope → recommend in the report; non-musical period signals are Effects).

## Field 4: Source physics and layer decomposition
List the 2-5 physical components that make the sound in THIS setting. For weapons and impacts, decompose into layers: attack/transient (under 50ms), body (100-500ms), sub (under 80Hz, felt), mechanical (the action), tail (environmental decay), sweeteners (secondary reactions). Decide the generation strategy here: single composite (default) | layered stems (P1 hero sounds; log stems, wire best composite, checklist the mixdown) | loop bed | variant set.

## Field 5: Perspective and listener context
Who hears it, from where (the design doc's listener perspective rules). Distance tiers are different sounds: close = all layers, mechanical prominent, dry; mid = body + tail, mechanical attenuated; far = body + sub + tail only, long decay. Pick single-tier or the tier set.

## Field 6: Variation, routing, and dependencies
Variation (variant count, pitch/volume randomization, container; loops get seam requirements; continuous states get the triple). Routing (mixer group, ducking per profile, snapshot, spatial settings row). Dependencies (anim + frame sync, co-located VFX sync, non-final assets flagged; parameter couplings like turn rate or impulse magnitude).

## Routing the completed record

- Silence IS the design (Release moments especially) → SILENCE PROPOSAL: specify exactly what stops, for how long, and what fades back in; log it and checklist it under Reasoned non-generations with the same rigor as a generation. Proposing silence is a sound-design choice, not a skipped row.
- Existing audio DEFECTIVE → defect-fix route: variant set to break repetition, material split, perspective correction, or stagger; the fix is designed here, executed in Phases 4-5.
- Musical need (score, adaptive music layers) → OUT OF SCOPE: write the recommendation (what the music should do at this moment) into the run report; do not generate.
- New sound → generate route.
- Trigger owner ambiguous → UNRESOLVED with all candidates listed.

## Filled example (Broadside-correct)

```
moment: Player's fore turret fires a two-gun 12in salvo at a cruiser ~8km off the port bow.
experience: Feedback (I fired) + Tension (now the wait for fall of shot) → feel: weighty, concussive
ieza: Effect
source_physics: cordite propellant detonation + shell engaging rifled bore + turret structure shock + muzzle blast over open water
layers: attack(cordite crack) + body(deep chamber boom) + sub(felt thump) + mechanical(breech and run-out) + tail(long roll over water)
strategy: single composite now; stems flagged for the P3 mixdown pass
perspective: tactical god-cam near the firing ship → close tier of a three-tier set
variation: variant set, 4, pitch +/-10pct, vol +/-2dB; per-gun stagger 30-80ms
routing: Combat group; ducks Ambience -3dB/400ms; 3D log rolloff per profile row
dependencies: Turret_Fire.anim frame sync + muzzle VFX co-location; anim non-final → flagged
route: generate (and the salvo-to-splash gap right after it → separate SILENCE PROPOSAL row)
```

After all records: run the batch cohesion pass in references/aesthetic-direction.md, then return to SKILL.md Phase 4.
