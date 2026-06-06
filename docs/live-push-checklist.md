# Live-Push Checklist — Diabow

Use this every time you push the `.rbxl` to the live Roblox experience.
Each item has a one-line "why" so you can skip with intent if you must.

## Pre-push (in Studio)

- [ ] **Tests pass.** Press F5 → wait 5s → look for `[TestRunner] 29 passed, 0 failed`.
  Why: catches damage/shard/weapon regressions before they hit players.

- [ ] **No errors in output.** Scroll the output panel for red text. Anything new
  since last push? Investigate.
  Why: warns surface real bugs (broken SoundIds, asset 404s, attribute typos).

- [ ] **Analytics fires once on spawn.** Look for `[Analytics] LogOnboardingFunnelStepEvent(YOU, 1, SpawnedInTristram)`
  exactly once after Play. Twice = the PlayerStats idempotency guard broke.
  Why: production dashboards depend on accurate funnel counts.

- [ ] **WorldBakeIn reports `0 sounds, 0 lights balanced`** on second consecutive
  play. First play after edit may show >0; second play must be zero (idempotent).
  Why: confirms the bake correctly no-ops when world state is already clean.

- [ ] **Walk Tristram for 30s.** No flicker on cathedral windows. NPC heads track
  you when you approach. Footsteps fire once per stride (not doubled).
  Why: regression sanity for the visual/audio polish pass.

- [ ] **Run a hostile-client adversarial probe** from the command bar:
  ```lua
  local rs = game:GetService("ReplicatedStorage")
  rs.Diabow.Remotes.ShopBuy:FireServer("griswold","admin","short_sword")
  for i=1,50 do rs.Diabow.Remotes.AttackSwing:FireServer() end
  print("violations:", #require(rs.Diabow.RemoteGuard).getViolations())
  ```
  Expected: violations > 0, no errors, no gold/items granted.
  Why: confirms RemoteGuard middleware is wired and enforcing.

## Pre-push (network)

- [ ] **Open Network Simulation panel** (Alt+S in Studio). Latency 100ms /
  jitter 50ms / packet loss 2%. Play one quest end-to-end.
  Why: catches replication races that don't surface at 0ms.

- [ ] **Run the network simulation checklist** for any combat/economy change.
  See [network-sim-checklist.md](network-sim-checklist.md).
  Why: production-grade ARPG bugs only surface under realistic conditions.

## Push (Studio → Roblox)

- [ ] **Make a backup of the live version first.** Roblox keeps version history
  but explicit > implicit. Copy current .rbxl to `backups/YYYY-MM-DD.rbxl`.
  Why: roll-forward is harder than roll-back.

- [ ] **Publish to Roblox** (File → Publish to Roblox). Choose the live universe.
  Verify the place ID matches your live experience, not a test slot.
  Why: publishing to the wrong place is the most common foot-gun.

- [ ] **Update `diablow.rbxl` in git** and commit. Push.
  ```bash
  cd /Users/doge/saarvis/roblox/diablow
  git add diablow.rbxl
  git commit -m "ship: <one-line summary of what's new>"
  git push
  ```
  Why: keeps CI in sync with what's live; later debugging starts from this snapshot.

## Post-push (first 30 minutes)

- [ ] **Watch the live experience analytics dashboard.** Go to
  create.roblox.com → your experience → Analytics. Acute drops in concurrent
  players or session length within 30 minutes = revert.
  Why: real users surface bugs Studio can't.

- [ ] **Check the Discord error webhook / oncall channel** for new error
  spikes. New ones (vs. baseline) tied to the push = revert.
  Why: server errors silently break gameplay for players, not just you.

- [ ] **Spot-check a few player sessions** (open the experience yourself,
  play 5 minutes, do a Butcher run, bank shards at Cain).
  Why: dashboards lag 5-15min, you don't.

## Rollback procedure

If you need to revert:

1. **Studio:** File → Open Recent → previous .rbxl (or restore from backup)
2. **Studio:** File → Publish to Roblox (re-publishes the old version)
3. **Git:** `git revert HEAD` (or `git reset --hard HEAD~1` if no one else pulled yet)
4. **Note the rollback** in dev_log.md with what broke + suspected cause
5. Don't immediately push the same fix — investigate first

## What's safe to push without the full checklist

- Pure cosmetic edits (color tweaks, UI text changes)
- New world decoration that doesn't change collisions
- Adding a new SoundId (verified alive)
- Adding a new entry to a configuration table

## What ALWAYS needs the full checklist

- Anything that touches: CombatService, EnemyAI, SoulshardService, ShopService,
  any boss-fight script, RemoteGuard, RemoteEvent schemas, PlayerStats
- Adding new RemoteEvents (must wrap in RemoteGuard)
- Changing existing RemoteEvent schemas (breaks existing clients in-session)
- Touching DataStore code (when it exists)
- Anything that changes how gold/shards/items flow

## Live secrets reminder

Three CI secrets are needed at https://github.com/agilepeter/roblox/settings/secrets/actions:
- `ROBLOX_API_KEY` — create.roblox.com/dashboard/credentials, scopes `place:write` + `universe.place.luau-execution-session:write`
- `ROBLOX_UNIVERSE_ID`
- `ROBLOX_CI_PLACE_ID` (CI place, NOT your live place — CI overwrites it each run)

Without these, the Test + Stress workflows fail with auth errors but Lint still passes.
