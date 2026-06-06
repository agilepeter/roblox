# Diablow

**Date conceived:** 2026-05-26
**Genre:** Atmospheric homage / explorable scene (NOT a money game)
**Trend rationale:** None — this is a learning project. Peter wants to build something in a world HE understands so the engine concepts stick. Diablo 1 Tristram (1996) is iconic, small, and has well-documented landmarks.

## The one-sentence experience
> Walk into the village of Tristram at perpetual dusk, hear the trickle of the fountain, see the cathedral's red glow pulsing in the north, and recognize every building — Griswold's forge, Ogden's tavern, Adria's hut across the river, Wirt sneering in the corner.

## Scope (v1)
Not a game. A walkable scene. Player spawns at the south entry road past the hanging corpse, walks into town, can enter the cathedral foyer (sealed dungeon door), can wander between every landmark. No combat. No monetization. Pure vibe.

## The 14 landmarks (from canonical D1 isometric map)
1. **Wirt** — far NW corner, leaning against broken wall
2. **Caves entry** — NW, sealed stone arch (visual only, no dungeon)
3. **Hell entry** — W mid, glowing red rift (visual only)
4. **Pepin** — SW, small stone healer cottage
5. **Cain** — center-S, robed scholar at the fountain
6. **Griswold** — NW of fountain, open forge with anvil
7. **Gillian** — W of fountain, between her grandmother's cottage and tavern
8. **Ogden** — tavern center (Tavern of the Rising Sun, hanging sign)
9. **Farnham** — slumped on a tavern bench, S of tavern
10. **Town Portals area** — open paved area E of buildings
11. **Adria** — far E across river, twisted timber hut on island
12. **Catacombs entry** — E mid, before river
13. **Slain Townsman (Kael Rills)** — N, lying bloody at cathedral steps
14. **Cathedral** — N, dominant gothic spire, red glow from doorway

## Atmosphere lock
- **Lighting:** perpetual overcast dusk. Cool blue-grey sky. Never night, never bright.
- **Palette:** muted browns + mossy green + slate grey + cold blue shadow. Warm orange only at forge / tavern windows / cathedral doorway. Blood red only at cathedral and corpse.
- **Sound (future):** water trickle from fountain, distant wind, crow caw, faint hammer-on-anvil, muffled tavern murmur, creak of swinging corpse rope. NEVER crickets (per memory).
- **Materials:** Stone = important buildings (cathedral, smithy, Pepin). Wood/thatch = civilian (tavern, cottages). Twisted timber = Adria.

## Iconic specific touches (the "this is Tristram" tells)
1. Swinging corpse on dead tree at south entry
2. Red-glowing cathedral doorway dead N — first thing you see entering town
3. NPCs in loose ring around central fountain, Cain on east side
4. Wounded townsman bleeding at cathedral steps
5. Two streams forking around Adria's island with rickety footbridges
6. Wirt isolated in far NW corner past a lone bridge
7. Burned-out cottages framing southern entry
8. Cracked bell in cathedral tower (never rings)

## NOT in v1
- Combat / monsters / dungeon descent
- NPC dialogue (just static figures with name billboards for v1)
- Quests
- Monetization
- Inventory
- Sound (Studio mute fine; add later)

## NOT to include (canon errors to avoid)
- Cain's burned house / cage → that's Diablo 2's Rogue Encampment, NOT D1. In D1 Cain is alive at the fountain.

## Build plan
- **Hour 1:** Lighting + ground + folders
- **Hour 2:** Cathedral (hero asset, gets the most polish)
- **Hour 3:** Fountain + civilian buildings (tavern, smithy, Pepin, Gillian)
- **Hour 4:** River + bridges + Adria across the river
- **Hour 5:** Iconic props (hanging tree, slain townsman, cemetery, burned houses, Wirt corner)
- **Hour 6:** NPC billboards + final atmosphere pass

## Why this game now
Peter's quote: "i'm not enjoying creating these games i don't understand. but they have been fun for understanding how you build stuff."

Diablo 1 Tristram is small (~14 landmarks), fixed-layout (not random), well-documented, and visually iconic. Perfect scope for someone who wants to understand 3D world building without having to ship a money-making game.

## Reuse from prior factory games
- LightingSetup Script pattern (steal-a-nightmare daylight) → adapt for Tristram dusk
- AdminPanel LocalScript (verbatim, teleport buttons re-pointed)
- Folder structure: Workspace.World, ServerScriptService, StarterPlayerScripts
- Security audit habit: log every Creator Store import

## Open questions
- Walk-in cathedral? (just foyer, sealed door to "dungeon") — YES for v1
- Wirt's "click for items" interaction? — NO for v1, billboards only
- Cow easter egg in east pasture? — YES, gotta have it
