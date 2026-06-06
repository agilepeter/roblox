# Diablow — Dev Log

## 2026-05-26 — Conception + scaffold

**Concept locked.** See `concept.md`.

Game #3 in the factory. First game NOT pursuing $1M-month goal — pure atmosphere homage to D1 Tristram (1996). Peter wants to build in a world he understands so engine concepts land.

**References on desktop (5 Tristram maps):**
- `Diablo_tristram_map.webp` — D2-style 3D recreation, useful for color
- `TristramMap.jpg` — top-down recreation w/ green fields (likely D2 version)
- `hey-i-made-a-tristram-diablo-1-map-for-d-d-...webp` — D&D battlemap, top-down layout
- `0508240d1cdcef4f349cdb181ec43ada.jpg` — **CANONICAL** labeled isometric, 14 numbered landmarks
- `images.jpg` — small screenshot, atmosphere reference

**Research synthesis from general-purpose agent (2026-05-26):**
Confirmed 14 landmarks, river layout (E-side, forks around Adria's island), bridges (2 E + 1 W to Wirt), cathedral at N with red doorway glow. Canon correction: Cain is ALIVE at the fountain in D1 (the burned-house Cain is Diablo 2 retcon).

## SECURITY AUDIT LOG

| Date | Asset | Source | Scripts | Action | Status |
|---|---|---|---|---|---|
| _none yet_ | | | | | |

(Same audit habit as steal-a-nightmare. Every Creator Store insert logged here.)

## Build session 1 — 2026-05-26 night — SHIPPED

Built Tristram on `diablow.rbxl` (Peter saved file mid-session).

### Phases shipped
- **P1 Lighting**: dusk (ClockTime 17.0, Brightness 2.3, atmosphere haze 0.25, blue-grey tint). Tuned brighter mid-session per Peter feedback ("dusk but enough light to see"). LightingSetup Script in SSS persists across play sessions.
- **P2 Ground**: 280×360 main town, east bank, Adria island, rocky cliffs ringing 3 sides, south entry road, spawn at (0,1,180).
- **P3 Cathedral**: 55 parts. Hero asset. Tall spire (peak y=127), cross, two flanking turrets, red doorway glow via 3 stacked PointLights, cracked bell, ivy on west wall, blood pool on doorstep, gothic arches, stained-red windows.
- **P4 Fountain + cobble paths**: Octagonal stone fountain w/ water particles + soft cool PointLight. Paths radiating to cathedral, tavern, smithy, Pepin, Gillian, entry, east. 4 benches. 14 lanterns with orange glow.
- **P5 Civilian buildings**: Tavern (44 parts, 2-story half-timber, Rising Sun sign, chimney smoke, 4 glowing windows), Smithy (open forge, glowing coals, ember particles, anvil, weapon rack, hammer hood), Pepin cottage (stone, herbs, drying rack, green-tinted windows), Gillian's grandmother cottage (12 parts).
- **P6 River + bridges**: Main N-S river along east, forks around Adria island (E branch), W stream for Wirt bridge. 29 bank stones (random rotation). 3 wooden plank bridges with railings.
- **P7 Adria + Wirt**: Twisted timber witch hut on island (24 parts, crooked walls, GREEN window glow, smoking cauldron, hanging bone totems, dead tree). Wirt corner with broken stone wall fragments + scattered crates + broken barrel.
- **P8 Iconic props**: Hanging tree + corpse + crow + warning sign at S entry. Slain Townsman (Kael Rills) at cathedral steps w/ sword + large blood pool. NW cemetery with broken iron fence + 9 crooked headstones + open grave. 3 burned cottages along S perimeter with smoldering embers + smoke particles. Cow pasture E with wooden fence + the canon black-and-white cow.
- **P9 NPC voiceovers**: 24 MP3s generated via ElevenLabs to `audio/` (~3MB total). Per-NPC voice mapping (George=Cain/Narrator, Brian=Griswold, Adam=Pepin, Charlotte=Adria, Charlie=Ogden, Lily=Gillian/Wirt, Daniel=Farnham). `audio_manifest.json` written with asset_id placeholders.
- **P10 NPCs**: 8 canon characters built as static Models with distinguishing accessories — Cain (robed, staff w/ glowing orb, beard, hood), Griswold (apron, hammer), Pepin (satchel, scholarly), Adria (witch staff w/ green crystal, dark purple robe, raven hair), Ogden (white apron, red shirt), Gillian (apron, brown hair), Farnham (tankard, half-pauldron, slumped), Wirt (peg leg, smug hat). Kael wired as ninth dialogue target.
- **P11 Dialogue system**: ReplicatedStorage.Diabow.Lines (ModuleScript w/ 24 canon D1 quotes), DialogueShow + NarratorShow RemoteEvents, DialogueService (per-player line cycle), DialogueGUI (parchment-style panel, typewriter effect, audio playback if asset_id set), Narrator overlay (auto-fires 3s after spawn).
- **P12 Ambient sounds**: 9 Sound objects positioned (cathedral drone, tavern murmur, forge fire, forge hammer, fountain water, rope creak, bell toll, 2 crow caws, wind global). AmbientSoundLoop Script fires hammer every 4-7s, bell every 90-180s, crow every 12-25s. Best-effort catalog IDs — may need swap if specific ones don't load.
- **P13 Narrator intro**: Fires on player join via NarratorShow. Full canon-tone intro "The village of Tristram. Once a quiet town..." displays in centered top panel with typewriter + audio.
- **P14 Upload script**: `upload_audio.py` does Roblox Open Cloud Assets API upload for all 24 MP3s. Updates manifest with asset IDs, emits `studio_patch.luau` to paste into Studio Command Bar (wires IDs into Lines module).

### Audio voice mapping locked

| NPC | ElevenLabs voice | Why |
|---|---|---|
| Cain | George (older British scholar) | Wise, gravelly, "Stay a while and listen" |
| Griswold | Brian (deep American) | Burly blacksmith |
| Pepin | Adam (warm American) | Fatherly healer |
| Adria | Charlotte (Swedish exotic) | Witchy, lower stability for raspy effect |
| Ogden | Charlie (Australian warm) | Jovial innkeeper |
| Gillian | Lily (young female) | Sweet barmaid |
| Farnham | Daniel (British) | Low stability + slow speed for slurring drunk |
| Wirt | Lily (young female, high style) | Boy voice approximation, smug |
| Kael Rills | Daniel (British, slower) | Dying delirium |
| Narrator | George (Cain-voice) | Mirrors Cain narrating town intro |

### Cost estimate for audio upload
- ~30s × 24 clips = 12 minutes of audio
- Roblox audio upload: ~35 Robux per <60s clip = 840 Robux for batch
- ~$3 USD worth of Robux

### Status end of session 2026-05-26
**Playable atmosphere walkthrough.**
- Walk in from S spawn — hanging tree + corpse first sight
- Cathedral with red glow + slain Kael at steps dead N
- Fountain + Cain in town square, NPCs ringing it
- Tavern (Ogden + Farnham + Gillian), Smithy (Griswold), Pepin cottage, Adria across the river, Wirt in NW
- Press E within 12 studs of any NPC → canon D1 dialogue with typewriter effect
- Narrator intro plays automatically 3s after spawn
- Audio silent until upload_audio.py is run (needs Roblox Open Cloud API key from Peter)

### NEXT-SESSION pickup
1. Peter creates Roblox Open Cloud API key at create.roblox.com/dashboard/credentials (1 min)
2. Find user ID at roblox.com/users
3. `ROBLOX_API_KEY=... ROBLOX_CREATOR_ID=... ROBLOX_CREATOR_TYPE=User python upload_audio.py`
4. Audio uploads + manifest gets asset IDs + studio_patch.luau emitted
5. Paste studio_patch.luau into Studio Command Bar — all dialogue now has voice acting

### v2 ideas (not session 1)
- Walkable cathedral foyer (sealed dungeon door)
- Lazarus-style sermon ambient that triggers when standing on cathedral steps
- Day/night cycle (rare, since canon is perpetual dusk — maybe cycle for Blood Moon event)
- Wirt's "spend gold for random item" shop interaction
- Click-the-cow Easter egg (8 clicks → "Yup, that's a cow all right" + secret cow level reference)
- Butcher quest hook: enter cathedral + screams + Butcher silhouette behind sealed gate

## Build session 2 — 2026-05-27 — RPG layer shipped

Peter wanted full Diablo: combat, boss, economy, expanded world. All built in one big push.

### Combat Foundation (Phase A)
- Server-authoritative architecture. PlayerStats Script initializes HP=30, Stamina=100, Gold=50 (starter), EquippedWeapon=fists, EquippedArmor=none.
- HP regen 1/sec out of combat, Stamina regen 3/sec always.
- CombatService Script handles AttackSwing RemoteEvent: weapon cooldown, stamina drain, 60° front cone hit detection, damage + knockback, boss bar updates for Butcher.
- Weapons ModuleScript: fists (1 dmg free), club (5/30g), short sword (12/80g), long sword (22/200g), butcher_cleaver (18, loot drop). Armor: leather (-2 dmg / 50g), chain (-5 dmg / 180g). Potions: healing_lesser (+20 HP / 25g), healing_full (+100 HP / 80g).
- CombatHUD LocalScript: HP bar (red, bottom-left), Stamina bar (green, above HP), Gold counter (top-left), Weapon indicator, Boss bar (top center, appears when Butcher engaged), hit flash overlay, click-to-attack, Q=lesser potion, R=full potion, B=open shop.

### Cathedral Interior (Phase B)
- Walkable interior: stone floor + dark ceiling + 10 pews + 6 wall torches with flame particles + 5 stained-red windows + entry threshold trigger.
- Stair pit descends 22 studs to Butcher Chamber.
- Butcher Chamber: 60×50 bloody-stone chamber, 5 meat hooks with hanging corpses + chain + drip-blood particles, center red light shaft, butcher's altar, portcullis gate at S entrance (4 bars).
- Bloodstained walls (8 splatters) + 6 floor blood pools.

### The Butcher (Phase C)
- 80 HP, 12 dmg/cleaver, 2.5s swing speed.
- Bald yellowish brute, bloody apron, single glowing yellow cyclops eye + scarred shut eye, crooked grin with stained teeth, BIG cleaver with bloodstained blade.
- StairBottomTrigger fires "AH, FRESH MEAT!" narrator overlay + slams portcullis (Tween) + activates AI when player crosses threshold.
- On death: portcullis raises, drops Butcher's Cleaver as WeaponPickup + 100 gold pile, victory narration, sets QuestButcher=done for all players.

### Catacombs Entry combat zone (Phase D)
- Located SOUTH of Adria across her bridge (canon landmark #12). Self-contained, doesn't disturb the original Tristram scene.
- Gothic stone archway + iron-grate pit + green fog particles + ominous green PointLight.
- 6 broken tombstones scattered around + 5 bone props.
- 5 tagged MobSpawn points around the arch.
- Warning sign near Adria's bridge: "BEWARE — The dead climb from below".

### Enemy AI + Spawner + Gold + Death (Phase E)
- EnemyTemplates in ServerStorage: FallenOne (5 HP, 1 dmg, 6g drop), Zombie (8 HP, 2 dmg, 9g drop).
- EnemySpawner Script maintains 4 fallen + 3 zombies at all times, respawn ~3s after death.
- EnemyAI Script (Heartbeat): chase nearest player within 25 studs, melee in range with cooldown, retreat to zone center if player leaves CatacombsZone radius (30 studs), wander idle.
- GoldPickupService: touch-tagged GoldPile parts add gold to player + tween float-up.
- PlayerDeathService: respawn at town entry on death, HP restored to max, gold + weapons + potions PERSIST through death (the design choice — they learn but don't lose progress).

### Griswold + Adria Shops (Phase F+G)
- ShopService Script handles ShopOpen + ShopBuy RemoteEvents server-authoritatively.
- Catalogues ModuleScript: Griswold sells 3 weapons + 2 armor. Adria sells 2 potion tiers.
- ShopGUI LocalScript v2 (POLISHED 2026-05-27 mid-session): parchment-theme modal, item-type icons (⚔🛡🧪), equipped/owned indicators, gold pill, balance-aware Buy button ("NOT ENOUGH" state), smooth open/close transitions, click-outside-or-Esc to close, status feedback line.
- Both NPCs got a second ProximityPrompt: "Browse Wares" (B key) in addition to "Speak" (E key).

### Butcher Fight Wiring (Phase H)
- ButcherFight Script: unanchors Butcher's HRP + welds body parts, listens for StairBottomTrigger, slams portcullis (tween 12 studs down), narrator yells "AH, FRESH MEAT!" to all clients.
- On death: portcullis raises back, drops cleaver + 100 gold pile, fires victory narration, marks quest done.
- WeaponPickup tag system: touch dropped weapon → equip + float-fade-destroy.

### Map Expansion (Tier 1/2/3)
**Cliffs pushed back** from inner edges (x=-160/290, z=-210) to outer ring (x=-280/375, z=-340) creating a 100-stud wilderness buffer around the village.

**Tier 1 (canon landmarks from labeled D1 map):**
- Caves Entry NW: rocky cave mouth with stalactites + stalagmites + 4 bat parts + dark interior void. (Landmark #2)
- Hell Entry W: huge red Neon rift sealed by iron bars + sulfurous fog + jagged rock surround. (Landmark #3)
- South Road extension: 7 cobble tiles extending S 140 studs, 4 dead trees lining road, broken merchant cart, fallen "TRISTRAM 1 MILE" signpost, distant mist particle volume.

**Tier 2 (lore-deep ruins):**
- King Leoric's Manor (NE, beyond cathedral): collapsed gothic keep with partial walls, broken throne with crown lying on it, dried blood pool, fallen headless knight statue, broken sword, 2 red wall-torches. Future Skeleton King boss zone.
- Archbishop Lazarus' cottage (W, past Hell entry): stone shack with door ajar, desk with scattered scrolls + knocked-over candle, dark blood stain on floor, CHARRED PENTAGRAM on the floor, single dark cracked window. Sign: "abandoned — but recently".
- Sirian's Mill (S on river): stone-and-wood mill tower with conical thatched roof + functioning water wheel with 6 paddles + 12-spoke rim. Sign: "idle — the miller fled".

**Tier 3 (atmospheric):**
- Outer Village Gate (S end of road): twin towers with crenellations, broken half-dropped portcullis (7 bars), hanging chain, "TRISTRAM" sign overhead, guard skeleton + rusted helmet at base.
- Caravan Camp (SE outskirts): overturned wagon with broken wheel, tarp draped, scattered crates + barrels, spilled cloth, dead-horse skeleton (skull + 6 ribs), cold campfire with ash. "Trader's last camp — they didn't make town".
- Standing Stones (N cliff overlook): raised grass mound with 6 weathered standing stones in a ring (random heights, all with glowing blue runes), central low altar with offering bowl, spectral blue PointLight + drifting wisp particles. "Older than Khanduras".

### Cain dialogue patched (Phase I)
- 6 lines now (was 4). New `cain_quest` line appears 2nd in cycle, gives player explicit hint: "cross Adria's bridge to the south, the dead climb from the Catacombs, even bare hands will cleanse them, then visit Griswold".
- Added `cain_leoric` and `cain_lazarus` lines that reference the Tier 2 ruin landmarks.
- Griswold and Adria greet lines updated to mention "Press B to browse my wares."

### POLISH PASS (mid-session)
**Shop GUI v2**: parchment theme, smooth animations, type-coded item badges (weapon=red, armor=blue, potion=purple), equipped/owned indicators, balance-aware Buy buttons, status feedback line, click-outside-to-close.

**Enemy templates v2**: FallenOne — hunched lean-forward pose, hood covering most of face revealing only 2 red glowing eyes, sunken jaw, long claw-like arms, RAISED rusty curved dagger with blood. Zombie — hunched bloated torso with exposed ribcage on cloth wrap, jaundiced skin (yellow-green), bloated head with sunken yellow glowing eyes in dark sockets, gaping jaw with rotten teeth + green drool, outstretched hungry arms with bony claw fingers, bloody patches on tattered legs.

**Gold piles v2**: Now actual coin stacks. Original detection part becomes invisible bigger touch volume. 3-12 actual coin parts (count scales with amount) cylindered + stacked + scattered around center, neon yellow gold material, ground glow PointLight. Sparkle particle emitter. Coins spin at 60°/sec while pile bobs gently up/down.

### Cost so far
- $0 — all Roblox MCP work + ElevenLabs API for voice generation (in saarvis pipeline)
- 24 NPC voice MP3s sitting at `diablow/audio/` (~3MB) — Peter still needs to upload via Open Cloud when ready (estimated 840 Robux / $3)

### What player experiences end-of-session (the canonical first-time loop)
1. Spawn at south entry road. Hanging tree + corpse first sight. Narrator overlay fades in: "The village of Tristram. Once a quiet town in the kingdom of Khanduras..."
2. Walk N. Pass under Tristram outer gate (skeleton + helmet at base). See cathedral with red glow dead ahead, NPCs ringing the fountain.
3. Talk to Cain (E key). Gets hint: "Cross Adria's bridge. The dead climb from the Catacombs."
4. Most players: ignore Cain, walk to cathedral first. Step on stair trigger → portcullis SLAMS. "AH, FRESH MEAT!" → Butcher charges → player dies in 3 hits (Bare Fists do 1 dmg vs 80 HP boss).
5. Respawn at town entry. *Oh.* Walk to Griswold. *No gold.* Realize they need to earn.
6. Cross Adria's bridge S. See Catacombs Entry with green fog + dead climbing out. Fight them — fists can kill Fallen Ones in 5 hits. Earn gold.
7. Return to Griswold. Open shop (B). Buy Wooden Club. Maybe a Healing Potion from Adria.
8. Return to cathedral. Survive Butcher (much longer fight with club, manageable with short sword, easy with long sword).
9. Butcher dies. Drop Butcher's Cleaver (18 dmg) + 100 gold. Quest complete.

### Build state files
- Total Workspace.Tristram: ~750 parts (was ~350 pre-session-2)
- 9 active NPCs + Kael (dialogue)
- 7 enemies live in Catacombs (4 fallen + 3 zombies)
- 1 boss (Butcher) in cathedral chamber
- 9 new map landmarks (Catacombs + Caves + Hell + SouthRoad + Leoric + Lazarus + Mill + Gate + Caravan + Stones = actually 10 with Catacombs)

### NEXT-SESSION pickup
- Audio upload (Peter creates Roblox Open Cloud API key, runs upload_audio.py, pastes studio_patch.luau)
- Skeleton King boss at Leoric's Manor (uses same boss-fight pattern as Butcher)
- Lazarus quest: enter cottage triggers a vision (LocalScript overlay), grants a "Scroll of Town Portal" item
- Standing Stones altar — touch with X gold offering for permanent +5 max HP buff
- Click-the-cow easter egg
- Wirt's random-item shop

## Build session 9 — 2026-06-01 — Bloody Caves (T3 dungeon) shipped

Third dungeon tier. D1-canonical Caves (L9-12) progression after Catacombs. Built top-to-bottom in one push with a research-workflow plan (7 parallel agents: 4 asset scouts, 1 bug auditor, 1 layout designer, 1 Hell-scout for T4).

### What shipped

- **Bloody Caves** at world X=3500, Y=-200, persistent streaming. 8 rooms with branching paths:
  - `CaveMouthDescent` (atmospheric entry)
  - `SulfurJunction` (3-way hub, central sulfur lava pool + bridge, Maw door locked here)
  - **West branch**: `BloodspringHollow` (3 blood pools + viper ledges) → `ChokingVents` (4 telegraphed lava vents + narrow ledges over lava channel)
  - **Hidden**: `AdriaForgottenCache` (off ChokingVents south wall, stalagmite-disguised door, 3 guardian-viper spawns on entry, reward chest)
  - **East branch**: `GoatmanWarrens` (3 burrow shelves + bone piles) → `LavaChasm` (chasm + chain bridge + kill-plane lava floor)
  - **Boss arena**: `TheBleedingMaw` (110×110, skull-shaped, lava moat, raised dais, 4 dais lava-jet vents for phase 3, 4 ceiling SummonSpawn points for phase 2)
- **Surface entry**: cave-mouth portal behind Adria's Hut at world (215, 5, 18), teleports to dungeon entry. East-of-town placement gives Caves its own compass direction (N=Catacombs, NW=Hell, E=Caves).
- **3 new mob templates** in `ServerStorage.EnemyTemplates`:
  - `CaveGoatman` — 50 HP, ws=14, AttackRange=5.5, Cooldown=0.6, AggroRange=60, dark-fur recolor of surface Goatman + red horn-tip light
  - `CaveViper` — procedural 8-segment Motor6D chain, 25 HP, ws=28, AttackRange=4, Cooldown=0.5, AggroRange=55, red head light
  - `BloodDemon` — 1.5× R15 dummy, crimson recolor, 90 HP, ws=6, AttackRange=7, Cooldown=1.0, AggroRange=65, blood-drip particle emitter
- **Boss: The Defiler (LazarusHound)** — scaled BloodDemon (1.6× of BloodDemon = 2.4× R15), 2400 HP, AttackRange=9, Cooldown=1.4, AggroRange=90, HitConeDegrees=70.
  - **Stash pattern**: anchored at world (3880, -700, 0) on script load. Activation = `RunService.Heartbeat` at 1Hz checks (BothBranchesCleared==true) AND (player HRP inside Maw bbox). NEVER `Part.Touched`.
  - **Phase 1** (100-50%): vanilla EnemyAI melee + stalk via attribute reads.
  - **Phase 2** (≤50%, single fire): summons 2 CaveVipers + 2 CaveGoatmen at the 4 ceiling SummonSpawn points + ScreenShake.
  - **Phase 3** (≤25%, single fire): activates 4 dais lava-jet vents on 1.5s telegraph + 2s plume rolling cycle (22 dmg cone) + WalkSpeed × 1.3.
  - **On death**: drops GoldPile (180-260) + fires `BossDefeated` + `LadderUpdate(kind=LazarusHound)` + `QuestProgress(CainDialogueStage=caves_cleared)`. Opens Maw→Sulfur one-way shortcut (collapsed-stalactite-pile CanCollide=false).
- **4 new server scripts**:
  - `LazarusHoundController.server` — boss FSM, region trigger, phase transitions, summons, vents, post-kill shortcut
  - `BloodyCavesGate.server` — per-room MobCount + Cleared tracking, flips `BothBranchesCleared` when both ChokingVents AND LavaChasm cleared, unlocks Maw door
  - `BloodyCavesHiddenDoor.server` — Adria Cache atomic CanCollide+Transparency toggle + 3 guardian-viper spawn
  - `BloodyCavesPortal.server` — cave-mouth Touched → teleport to dungeon
- **EnemySpawner** refactored: dict-driven TARGET now has `surface` + `catacombs` (renamed from `dungeon` to match attribute) + `bloody_caves` (CaveGoatman=19, CaveViper=12, BloodDemon=6 = 37 ambient mobs). `pickSpawn` reads `sp:GetAttribute("Zone")` with X-inference fallback; for bloody_caves it also filters by per-spawn `Kind` (room-flavored mob composition) and excludes `GuardianSpawn` points.
- **EnemyAI** patched: added `LazarusHound` to `isBossEnemy` allowlist + `zoneCenterFor` (Defiler uses HomePosition while not BossActivated, otherwise roams free like the Butcher).
- **3 new remotes**: `BossDefeated`, `QuestProgress`, `ScreenShake`.
- **Latent fix**: 44 existing MobSpawn points had `Zone=(none)` (the per-zone aggro fix from earlier in the day relied on this attribute but no one backfilled). Backfilled by X-coordinate inference; renamed internal `dungeon` → `catacombs` for consistency.
- **Cleanup**: 12 stray catalog Models removed from Workspace top level (leftover from the previous swing-animation hunt).

### What we learned (3 new bugs, all in [diablow_bugs_fixed.md](../../.claude/projects/-Users-doge-saarvis/memory/diablow_bugs_fixed.md))

1. `Model:ScaleTo()` silently nulls `PrimaryPart` → `PivotTo()` becomes a no-op
2. Plan's `ACTIVE_POS` was world Y=-45 (200 studs above the actual dais) — sanity-check coordinates against source geometry, not paper math
3. Manually resizing an HRP after `ScaleTo` detaches the rig — only ScaleTo is safe for resizing R15 humanoid models

### Validation

- 38/38 build-time validation checks passed (rooms, templates, attributes, anim≤cooldown ratios, tags, remotes)
- Bloody Caves spawn saturated at 37 mobs after 24s
- Force-flip test confirmed: BothBranchesCleared=true → Maw door unlocks → player-in-Maw + 1Hz Heartbeat → boss unanchors + moves from stash to dais → phase logic wired to HealthChanged
- TestHook script removed post-sign-off

### Next: Hell tier (T4) research delivered

- Recommended: "Hell's Vestibule" as T4 **penultimate** chapter, not the finale. Andariel (Maiden of Anguish) as Lesser-Evil capstone. Diablo himself reserved for T5 "Inner Sanctum / The Burning Throne."
- Visual: hard cool-palette pivot away from Caves' warm red — obsidian black + bone white base, sulphur green-yellow flame, bruise-purple void accents. Forged citadel architecture (chains, gibbets, sigil floors, screaming faces) — NOT another organic cave.
- Mob archetypes (one new mechanic per sub-floor): F1 Hellspawn Knight (kite-required armored melee), F2 Soul Burner (telegraphed floor AoE — new mechanic), F3 Chain Fiend (ranged grappler — positioning mechanic), F4 Gibbering Maw (flying swarm-tier).
- Mid-dungeon mini-boss: "The Butcher Reborn" (D1 callback, corridor charge).
- Top risks + mitigations: aesthetic saturation vs Caves → cool palette + citadel arch; progression budget → Lesser Evil capstone, Diablo at T5; difficulty cliff → one mechanic per floor.
