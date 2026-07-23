# Example Walk: Broadside Combat Scope (reasoning trace excerpts)

The kind of trace Phase 1-3 produces. Era-correct for 1895-1930; every moment shows the record compressed to its decision.

## Moment A: Helm input, ship heels into a turn
Detection: Lane B family 8; `HelmController` turn handling has no coupled audio; `turnRate` is serialized.
Record: Experience = Immersion + Feedback. IEZA = Effect. Physics = steel hull working under list, water pressure along the lee side, anchor chain and fittings shifting. Not a one-shot: continuous, coupled to `turnRate`.
Route: generate a working-steel groan loop bed (layered x2), wire volume to `turnRate`. Signature naval feedback; confidence high.

## Moment B: Full broadside, four turrets
Detection: Lane B family 1; `FireBroadside()` plays ONE hardcoded clip four times synchronously → DEFECTIVE (phasing, flat).
Record: Experience = Feedback + Tension. Defect fix: 4 close-tier main battery variants, one per turret, 30-80ms stagger, plus a single felt sub layer for the volley as a whole. Ducks Ambience -3dB/400ms.
Route: defect fix.

## Moment C: The ranging silence
Detection: Lane A; the design bible's core loop is the fight you committed to; the salvo-to-splash wait IS the dread.
Record: Experience = Tension → Release deferred. The design decision is to NOT fill 6-10 seconds of flight time: combat bed drops slightly, no stinger, wind and machinery only.
Route: SILENCE PROPOSAL, logged with full rigor; checklist verify: reads as dread, not as broken audio.

## Moment D: Shell strikes armor at 8km (observed from the firing ship)
Detection: Lane B families 3+4; impact handler silent, splinter VFX has no co-located source.
Record: Experience = Feedback + Reward. Physics = steel penetrating face-hardened plate, spall, structure ring. Perspective = FAR tier: filtered low thump arriving after the flash, elongated, no mechanical. AudioSource placed at the VFX spawn point, volume scaled by impulse if exposed.
Route: generate, far tier of a three-tier set.

## Moment E: Battle stations
Detection: Lane B family 6; `Exploration → Combat` transition has no cue.
Record: Experience = Threat + Tension. Musical stinger would be Affect → OUT OF SCOPE (recommendation to the report). But the diegetic period answer is generatable: klaxon or bugle call, Effect, 2D-ish (0.8 blend), followed by the Combat snapshot swap.
Route: generate the diegetic signal; recommend the musical layer in the report.
