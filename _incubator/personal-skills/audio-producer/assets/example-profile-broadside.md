# Example Profile: Broadside (1895-1930 naval combat sim)

A completed `docs/audio/PROFILE.md` showing the specificity every section needs. Use as the model when authoring a profile; do not copy content across projects.

## 1. Sonic Identity
Heavy industry at sea: steel, steam, and cordite. Breech-loading naval rifles from 3-inch quick-firers to 15-inch main battery; riveted steel hulls and decks; reciprocating triple-expansion engines and steam turbines fed by coal or oil-fired boilers; voice pipes, engine-order telegraph bells, bugles, klaxons. Never age-of-sail, never modern electronics.

## 2. Vocabulary Tables
ALLOWED anchors: early 20th century battleship; dreadnought era; steel warship; cordite propellant; riveted steel hull; coal-fired; WW1 naval; naval rifle; quick-firing gun; engine-order telegraph.

| BANNED (too early) | BANNED (too late) |
|---|---|
| black powder | missile, rocket |
| wooden deck, wooden warship | jet, afterburner |
| cannon ball | radar ping, sonar ping |
| age of sail, rigging creak | autocannon, CIWS, gatling |
| musket, cutlass | helicopter |
| carronade | electronic alarm, sci-fi |

("Cannon" alone tolerated only for small-caliber QF guns; prefer "naval gun", "naval rifle", "main battery".)

## 3. Category Table
| Category | Duration (s) | Loop | Variants | Example prompt |
|---|---|---|---|---|
| weapon-main (12-15in) | 3.0-4.5 | n | 4 | "Battleship main battery 12-inch naval gun firing, deafening cordite blast with deep concussive thump, muzzle report rolling across open water, early 20th century dreadnought, heard from the deck, long low rumble tail" |
| weapon-secondary (3-6in) | 1.5-2.5 | n | 4 | "6-inch quick-firing naval gun, sharp cordite crack, steel turret interior echo, rapid breech mechanism clank after the shot, WW1 era warship" |
| impact-armor | 1.5-2.5 | n | 3 | "Large caliber shell striking riveted steel armor plate, violent metallic clang with tearing steel shriek and debris ring, early 20th century battleship hull" |
| impact-water | 2.0-3.5 | n | 3 | "Heavy naval shell plunging into the sea, towering water column splash, deep whump followed by cascading spray, heard from a warship deck" |
| shell-flight | 1.0-2.0 | n | 2 | "Large artillery shell passing overhead, deep tearing whoosh, doppler, open sea, no explosion" |
| damage-fire | 4-5 | y | 1 (layered bed x2) | "Fierce shipboard fire in a steel compartment, roaring flames, groaning heated steel plate, distant secondary pops, early 20th century warship" |
| ambience-engine | 4-5 | y | 1 (layered bed x3) | "Steam turbine and reciprocating engine room, rhythmic mechanical pounding, hissing steam, coal-fired boiler roar, riveted steel hull, seamless loop" |
| ambience-deck | 4-5 | y | 1 (layered bed x2) | "Open deck of a steaming steel warship, wind over superstructure, bow wash, distant funnel roar, faint machinery hum through the deck, seamless loop" |
| alarm-signal | 1.0-3.0 | n | 1 | "Ship klaxon battle stations alarm, harsh mechanical horn, steel corridor echo, early 20th century warship" |
| ui-shipyard | 0.5-1.0 | n | 1 | Mechanical-industrial, 2D: "heavy drafting stamp on paper", "brass switch clunk", "pencil on blueprint". Never bleeps. |

## 4. Distance Tiers
Engagements span hundreds of meters to ~15km: three tiers (close/mid/far) for weapon-main, weapon-secondary, impact-armor, impact-water. Far tier = filtered low-frequency rumble arriving after the visual flash, elongated tail; not the close clip attenuated. Single-tier for all other categories.

## 5. Wiring Configuration
Integration mode: sound-bank/event. Sim layer raises audio events; visual-layer audio system resolves via bank asset at `Assets/Audio/AudioBank.asset` (STATUS: architecture not yet built; produce mode runs generate+import and logs `NOT WIRED - awaiting audio event system` until the human rules on and lands the event system). Direct per-prefab AudioSources rejected: couples audio to gameplay objects and violates the sim/visual decoupling.

AudioSource settings (applied via bank entries):
| Category | spatialBlend | rolloff | minDist | maxDist | volume | pitch var |
|---|---|---|---|---|---|---|
| weapon-main | 1.0 | Log | 50 | 4000 | 1.0 | +/-0.04 |
| weapon-secondary | 1.0 | Log | 25 | 2500 | 0.9 | +/-0.06 |
| impact-armor / impact-water | 1.0 | Log | 20 | 3000 | 0.9 | +/-0.08 |
| shell-flight | 1.0 | Linear | 30 | 1500 | 0.7 | +/-0.05 |
| damage-fire | 1.0 | Log | 10 | 800 | 0.8 | 0 |
| ambience-* | 0.6 | Linear | 15 | 600 | 0.5 | 0 |
| alarm-signal | 0.8 | Log | 10 | 1200 | 0.9 | 0 |
| ui-shipyard | 0.0 | n/a | n/a | n/a | 0.8 | 0 |

Mixer bus map: Master → Combat / Ambience / Alarms / UI (to be created with the bank); ducking rule: T1 weapon fire ducks Ambience -3dB for ~400ms. Import: one-shots DecompressOnLoad mono; ambience Streaming; UI 2D. AudioRandomContainer: check Unity version at first wire.

Distances UNCALIBRATED against the project's ModelScale ruling (per-ship ~15.0-18.0 m/unit); calibrate before first wire.

## 6. Conventions
`Assets/Audio/SFX/<Category>/<Subject>_<Action>_<Tier>_Var<N>.wav`. Target format WAV 44.1k; convert mp3 tool output, trim loop seams.

## 7. Budgets
Per-run cap: 60 generation calls. Variants per the category table. Critic retries: 2. Serialized Unity owner rule: this pipeline is the only editor writer while running; hard stop if any live test run is active.
