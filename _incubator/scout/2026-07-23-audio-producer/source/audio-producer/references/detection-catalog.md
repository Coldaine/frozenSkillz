# Detection Catalog: Where the Agent Looks

You are reading this because you entered Phase 1. The unit of work is the MOMENT: a place in the game where something happens that may need sound. Run both lanes; each hit becomes a candidate-moment row in the working inventory, not yet a sound.

## Lane A: Imagine from the design docs

Play the game in your head. Work system by system through the scope using the design bible, sourcebooks, and scene flow, and enumerate every moment a player should HEAR or deliberately NOT hear:

- Player actions (fire, build, select, steer, toggle)
- System feedback (hit/miss, damage states, warnings, resource and threshold events)
- Continuous states (engines, machinery, weather, fire: anything with a duration wants a start-cue + loop + stop-cue triple)
- Dramatic beats: state entries and exits, victories, destructions, and the SILENCES between them; a designed silence (the gap between salvo and splash, the hush after a sinking) is a candidate moment too
- UI for the scope's screens

Lane A finds the moments no one coded yet; on an early codebase it is most of the list.

## Lane B: Scan the repo signals (eight families, concrete patterns)

1. Code
   - Audio calls with null/placeholder refs: grep `AudioSource|PlayOneShot|PlayClipAtPoint|PlayScheduled` in Assets/Scripts, then inspect owning prefabs for null/placeholder clips.
   - Event-bus calls to unregistered events: grep `Play\(\"` and diff the string set against the registry/bank.
   - Silent action verbs: grep `void (Fire|Shoot|Hit|Impact|Explode|Detonate|Launch|Open|Close|Reload|Damage|Die|Sink|Flood|Board|Dock|Land)` and check the method body (and its callees one level down) for any audio; a hit with none is a silent action.
   - Process coroutines (`IEnumerator` methods representing a duration: winch, loading, raising) with no audio across the span.
   - Debug.Log strings that telegraph events the designer cared about but never sonified.
2. Animation
   - Clips with animation event markers whose handler has no clip assigned.
   - Clips depicting an obviously sound-making action with NO markers at all; record the frame where the sound should fire.
   - Animator state transitions (Loaded → Firing → Empty → Reload is four sonic moments).
3. Physics and collision
   - `OnCollisionEnter|OnCollisionStay|OnTriggerEnter` handlers with no audio response.
   - Handlers that DO play audio but with one hardcoded clip: no variation or material awareness is a DEFECTIVE moment (sound-design bug), not COVERED.
4. VFX
   - Particle systems (muzzle flash, splash, smoke, fire, debris, sparks) with no co-located AudioSource; the eye sees a bang the ear doesn't hear.
   - VFX that intensify over time with no audio intensity parameter → candidate for an adaptive layered bed, not a one-shot.
5. UI
   - Selectable/Button/Slider/Toggle/Dropdown with no click/hover/valueChanged audio.
   - Menu open/close, panel swaps, tab changes, modals, notification toasts, objective updates.
6. Game state and narrative
   - State machine transitions (Exploration → Combat → Victory/Sinking/Surrender/Pause) with no cue or snapshot swap.
   - Threshold crossings: hull integrity, flooding level, ammunition low → warning audio moments.
   - Narrative and scripted beats from dialogue/scene-flow docs; propose silence where release is the experience.
7. Zone and ambient
   - Trigger volumes marked as ambience/weather/interior areas with no bed; ambience managers with empty slots; biome/weather/time transitions with no crossfade.
8. Movement and foley
   - Locomotion per surface (each surface is a variant set).
   - Vehicle/ship motion parameters (turn rate, speed, list) with no coupled audio; signature feedback often lives here.
   - Object manipulation: hatches, winches, levers, capstans.

## Context budget (do not read the whole project)

Read design docs fully. Scripts: grep first (the patterns above), then read ONLY the hit files plus at most one level of callees. Scenes: NEVER read raw scene YAML; query the Unity MCP for hierarchy and components. Prefabs: MCP component queries, not file text. On large scopes, walk system by system and treat the inventory file as the running state: once a candidate row is written, drop the file contents from working memory. Blowing the context window mid-walk loses the run.

## Merge and classify

Deduplicate Lane A against Lane B (the same moment found twice merges; keep the richer trigger detail). Classify: MISSING (no audio), PLACEHOLDER (temp/test/borrowed clip), DEFECTIVE (audio exists but variation-blind, material-blind, phasing, or mis-perspectived), COVERED (skip). Each row records: ID, moment (one line), source signal (file:line, prefab, anim+frame, or design-doc section), scope category, and any parameter it should couple to.

## Working inventory

Maintain `docs/audio/Inventory_<scope>.md` (table: ID, moment, category, IEZA, class, variants, tiers, priority, confidence, trigger owner, route, status). Agent-owned, updated every run, never an approval artifact. Status: `Not produced`, `Produced`, `Wired`, `Silence proposed`, `Rejected (rev N)`, `UNRESOLVED`, `IMPORT FAILED`, `WIRING FAILED`, `OUT OF SCOPE - music`.

Sanity checks: every continuous state has loop AND transition items; every P1 item has a trigger owner or an explicit UNRESOLVED; a combat-scale scope under ~10 or over ~60 moments usually means a derivation error; recheck scope, then proceed without asking.

Return to SKILL.md Phase 2.
