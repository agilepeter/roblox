# Diabow Testing Setup — How to Wire Up CI

Author: Claude Opus 4.7 polish-pass, 2026-06-06

This document explains how to take the testing infrastructure that lives inside
`diablow.rbxl` and connect it to GitHub Actions for PR-gating CI.

## What's already done (inside the .rbxl)

1. **Analytics** — `ReplicatedStorage.Diabow.Analytics` wraps
   `AnalyticsService`. Instrumented in CombatService, SoulshardService,
   ButcherFight, DiabloFight, ShopService, PlayerStats, GoldPickupService.
   In Studio it prints `[Analytics] LogX(...)` to output for verification.
   In production it calls the real service. Free dashboards at
   create.roblox.com → Analytics for your experience (24h lag).

2. **RemoteGuard** — `ReplicatedStorage.Diabow.RemoteGuard` is a middleware
   wrapper. Currently bound to: `AttackSwing`, `ShopBuy`, `RequestShop`,
   `UsePotion`. Schema validation + rate limiting + jail-on-abuse.
   Extend by replacing `remote.OnServerEvent:Connect(handler)` with
   `RemoteGuard.bind(remote, {schema={...}, budget=N, window=1}, handler)`.

3. **TestRunner + Specs** — `ServerStorage.DiabowTests/`:
   - `TestRunner` — Jest-Lua-style `describe/it/expect` runner.
   - `WeaponsSpec`, `CombatMathSpec`, `ShardMathSpec`, `RemoteGuardSpec`.
   - `StressBenchmark` — 4 scenarios (baseline, 100 mobs, 200 particles, 50 lights).
   - Entry: `ServerScriptService.DiabowTestsRunner` auto-runs in Studio,
     exposes `_G.RunDiabowTests()` and `_G.RunStressBenchmark()` for headless CI.
   - Current state: **29 specs passing**.

4. **debug.profilebegin labels** on: `EnemyAI/heartbeat`, `EnemyAI/tickEnemy`,
   `CombatService/swing`, `DiabloFight/phaseLoop`, `SoulshardService/magnet`.
   Open MicroProfiler (Ctrl+F6 or `Ctrl+P` to pause), search for those labels.

## What's on disk (waiting for git)

```
/Users/doge/saarvis/roblox/diablow/
├── rokit.toml              # Toolchain manager: rojo + selene + stylua + run-in-roblox
├── selene.toml             # Lint config (deny roblox-specific errors)
├── stylua.toml             # Format config
├── default.project.json    # Rojo project — STUB, needs source extraction
├── .github/workflows/
│   ├── lint.yml            # Selene + StyLua on every PR
│   ├── test.yml            # Run DiabowTests via Open Cloud Luau Execution API
│   └── stress.yml          # Nightly stress benchmark via Open Cloud
└── docs/
    ├── testing-setup.md    # This file
    └── network-sim-checklist.md  # Pre-merge checklist for network/multiplayer
```

## Setup steps (one-time)

### 1. Initialize git
```bash
cd /Users/doge/saarvis/roblox/diablow
git init -b main
git remote add origin git@github.com:YOUR-ORG/diablow.git  # or whatever
```

### 2. Install Rokit + tools
```bash
curl -fsSL https://raw.githubusercontent.com/rojo-rbx/rokit/main/scripts/install.sh | sh
rokit install
```

### 3. Convert .rbxl → Rojo source tree

Currently `default.project.json` is a stub pointing to non-existent `src/`
folders. Two options:

**Option A (low effort, low fidelity):** keep editing `.rbxl` in Studio. Use
Rojo only as a one-way exporter for CI:
```bash
# Periodically: Studio File → Save As → diablow.rbxlx (XML, not binary)
# Then Rojo can read it for CI builds.
# Tedious but no source-tree migration needed.
```

**Option B (high effort, real CI):** Use `remodel` or `rbx-dom` tooling to
explode the .rbxl into an on-disk Lua tree. Rojo builds from disk for CI;
Studio sync brings changes back. This is what professional Roblox studios do.
A few days of migration work.

### 4. GitHub secrets

Add these to your repo (Settings → Secrets → Actions):

- `ROBLOX_API_KEY` — Open Cloud key. Create at https://create.roblox.com/dashboard/credentials
  with permissions: `place:write`, `universe.place.luau-execution-session:write`.
- `ROBLOX_UNIVERSE_ID` — your universe ID
- `ROBLOX_CI_PLACE_ID` — a dedicated place in your universe for CI runs
  (separate from your live place — CI overwrites it each run)

### 5. Push to trigger CI

```bash
git add -A
git commit -m "Initial test infrastructure"
git push -u origin main
```

The 3 workflows should fire. `lint.yml` and `test.yml` on every PR. `stress.yml`
nightly + on workflow_dispatch.

## Open Cloud Luau Execution API quick reference

The crucial endpoint:
```
POST https://apis.roblox.com/cloud/v2/universes/{U}/places/{P}/luau-execution-session-tasks
Header: x-api-key: {KEY}
Body: { "script": "return _G.RunDiabowTests()", "timeout": "30s" }
```

Returns a session you can poll, or wait (up to ~5 min) for. The script runs on
a real Roblox server with full access to your game's services. Whatever your
script `return`s is delivered back via the API. So `RunDiabowTests` returning
`{ success = true, passed = 29, failed = 0 }` is what CI parses for pass/fail.

## Running tests locally

```bash
# Open diablow.rbxl in Studio
# Hit Play (F5)
# Output panel shows: [DiabowTests] running 4 spec files | [TestRunner] 29 passed, 0 failed
```

Or via command bar in Studio:
```lua
_G.RunDiabowTests()         -- runs specs, prints summary
_G.RunStressBenchmark()     -- runs perf scenarios, prints results (~15s)
```

## Skipped (intentionally)

- **ProfileStore / save data versioning** — Diabow currently has zero
  DataStore usage (player state is all transient attributes). Skip until you
  actually want saves. When you add a save layer, see
  https://madstudioroblox.github.io/ProfileStore/

## Reference

- [Open Cloud Luau Execution](https://create.roblox.com/docs/cloud/reference/features/luau-execution)
- [Roblox/place-ci-cd-demo](https://github.com/Roblox/place-ci-cd-demo) — reference workflow
- [Roblox/jest-roblox](https://github.com/Roblox/jest-roblox) — official Jest port (alternative to our minimal TestRunner)
- [Selene docs](https://kampfkarren.github.io/selene/)
- [StyLua](https://github.com/JohnnyMorganz/StyLua)
- [Rokit](https://github.com/rojo-rbx/rokit)
