# Network Simulation Checklist

Roblox Studio's **Network simulation** panel (`Alt+S` to toggle) lets you inject
latency, jitter, and packet loss in either direction. This is the primary
defense against exploiter bugs that only surface under bad-network conditions.

The old `IncomingReplicationLag` slider is deprecated — use the new panel.

## When to run this checklist

Run **all of the below scenarios** before merging any PR that touches:

- `CombatService` (damage, swings, hit detection)
- `EnemyAI` (mob targeting, attacks, AoE)
- `SoulshardService` (pickup, banking, scatter)
- `ShopService` (purchases, currency)
- Any boss-fight script (Butcher, SkeletonKing, Diablo, Ash Lord, CowKing)
- `RemoteGuard` itself or any new remote binding

## Scenarios

### 1. Baseline (no simulation)
- Open Studio → Local Play → Start Server + 1 Player
- Confirm gameplay feels normal. This is your control.

### 2. Mild latency (100ms / no loss)
- Network panel: `Send Latency = 100ms`, `Receive Latency = 100ms`
- **Test:** Swing 10 times at a Zombie. All swings should land or miss based on
  visual cone; no swings should silently disappear.
- **Test:** Open shop, buy a club. Gold should deduct, weapon equips.

### 3. Heavy latency (250ms / no loss)
- Network panel: `Send = 250ms`, `Receive = 250ms`
- **Test:** Fight the Butcher. Boss-bar updates should still arrive (may lag).
- **Test:** Banking 5 soulshards at Cain — both `Soulshards_Unbanked` and
  `Soulshards_Banked` attributes must update atomically. **No partial state.**

### 4. Jitter (100ms ± 50ms)
- Network panel: latency 100ms, jitter ±50ms
- **Test:** Walk around. Footsteps should still fire per stride (no clumps).
- **Test:** Cast PowerStrike as Sorcerer. Beam origin must stay at hand even
  with jitter (the `getCastOrigin` helper is called at fire-time).

### 5. Packet loss (5% both directions)
- Network panel: `Outbound Packet Loss = 5%`, `Inbound Packet Loss = 5%`
- **Test:** Fire `AttackSwing` 20 times rapidly. **Expected:** RemoteGuard's
  rate-limit (8/s) should NOT trigger from re-sends (TCP retransmits are
  invisible to userland).
- **Test:** Pick up 10 GoldPiles. Total gold should equal sum of amounts.
- **Test:** Kill the Skeleton King. Quest completion should fire exactly once,
  even if `QuestUpdate` packet drops.

### 6. Mobile profile (200ms / 2% loss / 50ms jitter)
- Network panel approximates a real mobile player on 4G.
- **Test:** Full Cathedral run from entry to Butcher kill. **Must complete.**
- **Test:** Run StressBenchmark in this profile: heartbeat should stay >= 45 Hz.

### 7. Hostile-client simulation
- After the above, use the in-game admin command bar:
  ```
  game.ReplicatedStorage.Diabow.Remotes.ShopBuy:FireServer("griswold","admin","short_sword")
  game.ReplicatedStorage.Diabow.Remotes.ShopBuy:FireServer({hack=true}, 1, nil)
  for i=1,100 do game.ReplicatedStorage.Diabow.Remotes.AttackSwing:FireServer() end
  ```
  All should be silently rejected by RemoteGuard. Check server console for
  `[RemoteGuard] reject` warnings. Run RemoteGuardSpec to verify the same logic.

## What "passes" means

- **No exceptions** in server console (lint with `tail -f`).
- **No client desync** (visual position matches server within 5 studs).
- **No duped or lost loot** (gold/shards/quest state consistent).
- **No silent-reject loops** (RemoteGuard rate-limits engage only on actual abuse).

## Network panel reference

| Property | Where it lives |
|---|---|
| Send/Receive Latency (ms) | Studio Settings → Network → Simulation |
| Send/Receive Jitter (ms) | Same |
| Outbound/Inbound Packet Loss (%) | Same |
| Per-property knobs | Same — toggle each direction independently |

If the panel is missing properties, your Studio build is older than the
expanded network simulation rollout. Update to latest.

## Reference

- [DevForum: Expanding Network Simulation in Studio](https://devforum.roblox.com/t/expanding-network-simulation-in-studio/4665487)
- [Roblox docs: Testing Modes](https://create.roblox.com/docs/studio/testing-modes)
