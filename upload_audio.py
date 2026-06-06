"""
DIABLOW — Upload generated audio to Roblox via Open Cloud Assets API.

This script uploads every MP3 in audio/ to Roblox, captures the asset IDs,
updates audio_manifest.json, and emits a Luau patch script you paste into
Studio to wire the IDs into the dialogue system.

Prerequisites
-------------
1. Roblox Open Cloud API key with `asset:write` scope:
   https://create.roblox.com/dashboard/credentials → Create API key
   Add "Universe API" and "Open Cloud API" → Asset (read + write)
2. Your Roblox user ID (or group ID if uploading as a group).
3. Run generate_audio.py first so audio/*.mp3 + audio_manifest.json exist.

Usage
-----
    export ROBLOX_API_KEY="..."        # your Open Cloud key
    export ROBLOX_CREATOR_ID="123..."  # your user OR group ID
    export ROBLOX_CREATOR_TYPE="User"  # "User" or "Group"
    python upload_audio.py

The script polls each upload operation until Roblox finishes processing
the audio (usually 1-10 seconds per file). Final output: a Luau snippet
you paste into Studio Command Bar to fill in all the asset IDs.

Cost note: audio uploads on Roblox cost Robux per second of audio
(typically 35 Robux per <60s clip). 24 clips × ~$0.05 = ~$1.20 USD of
Robux. Roblox audio also takes time to moderate (usually <1 min, can
take longer for first-time uploaders).
"""

import json
import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).parent
AUDIO_DIR = ROOT / "audio"
MANIFEST_PATH = ROOT / "audio_manifest.json"
PATCH_OUT = ROOT / "studio_patch.luau"

API_KEY = os.getenv("ROBLOX_API_KEY")
CREATOR_ID = os.getenv("ROBLOX_CREATOR_ID")
CREATOR_TYPE = os.getenv("ROBLOX_CREATOR_TYPE", "User")  # "User" or "Group"

if not API_KEY:
    sys.exit("ROBLOX_API_KEY not set. Get one at create.roblox.com/dashboard/credentials")
if not CREATOR_ID:
    sys.exit("ROBLOX_CREATOR_ID not set. Find your user id at roblox.com/users (URL has it)")
if not MANIFEST_PATH.exists():
    sys.exit(f"{MANIFEST_PATH} not found. Run generate_audio.py first.")

manifest = json.loads(MANIFEST_PATH.read_text())

CREATE_URL = "https://apis.roblox.com/assets/v1/assets"
OP_URL = "https://apis.roblox.com/assets/v1/operations/"


def upload_one(line_id: str, file_path: Path) -> str | None:
    """Upload one MP3. Returns Roblox asset ID, or None on failure."""
    metadata = {
        "assetType": "Audio",
        "displayName": f"Tristram - {line_id}",
        "description": f"Diablow Tristram NPC dialogue: {line_id}",
        "creationContext": {
            "creator": (
                {"userId": CREATOR_ID} if CREATOR_TYPE == "User"
                else {"groupId": CREATOR_ID}
            ),
            "expectedPrice": 0,
        },
    }

    with open(file_path, "rb") as f:
        files = {
            "request": (None, json.dumps(metadata), "application/json"),
            "fileContent": (file_path.name, f, "audio/mpeg"),
        }
        resp = requests.post(
            CREATE_URL,
            headers={"x-api-key": API_KEY},
            files=files,
            timeout=60,
        )
    if resp.status_code != 200:
        print(f"  [err] {line_id}: HTTP {resp.status_code} {resp.text[:200]}")
        return None

    op_path = resp.json().get("path")  # e.g. "operations/abc123"
    if not op_path:
        print(f"  [err] {line_id}: no operation path in response")
        return None

    # Poll until done
    for attempt in range(30):
        time.sleep(2)
        op = requests.get(
            f"https://apis.roblox.com/assets/v1/{op_path}",
            headers={"x-api-key": API_KEY},
            timeout=20,
        )
        if op.status_code != 200:
            continue
        body = op.json()
        if body.get("done"):
            if body.get("error"):
                print(f"  [err] {line_id}: {body['error']}")
                return None
            asset_id = body.get("response", {}).get("assetId")
            if asset_id:
                print(f"  [ok]  {line_id} → asset {asset_id}")
                return str(asset_id)
            print(f"  [err] {line_id}: done but no assetId")
            return None
    print(f"  [err] {line_id}: poll timeout after 60s")
    return None


def main():
    print(f"Uploading {len(manifest)} audio files to Roblox as {CREATOR_TYPE} {CREATOR_ID}")
    print()
    successes, failures = 0, 0
    for line_id, entry in manifest.items():
        if entry.get("asset_id"):
            print(f"  [skip] {line_id} already has asset {entry['asset_id']}")
            successes += 1
            continue
        path = ROOT / entry["file"]
        if not path.exists():
            print(f"  [skip] {line_id}: file missing ({path})")
            failures += 1
            continue
        asset_id = upload_one(line_id, path)
        if asset_id:
            entry["asset_id"] = asset_id
            MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))  # save as we go
            successes += 1
        else:
            failures += 1

    print()
    print(f"Done. {successes} succeeded, {failures} failed.")

    # Emit a Luau patch script
    lines_with_ids = [
        f'    ["{lid}"] = "{entry["asset_id"]}",'
        for lid, entry in manifest.items()
        if entry.get("asset_id")
    ]
    patch = f"""-- DIABLOW Studio Patch — paste into Studio Command Bar.
-- Generated by upload_audio.py on {time.strftime("%Y-%m-%d %H:%M:%S")}.
-- Updates ReplicatedStorage.Diabow.Lines with audio asset IDs.
local ReplicatedStorage = game:GetService("ReplicatedStorage")
local Lines = require(ReplicatedStorage.Diabow.Lines)

local idMap = {{
{chr(10).join(lines_with_ids)}
}}

for _, npcData in pairs(Lines) do
    for _, line in ipairs(npcData.lines) do
        if idMap[line.id] then
            line.audioAssetId = idMap[line.id]
        end
    end
end

-- Write the new module source so it persists
local module = ReplicatedStorage.Diabow.Lines
local newSource = "return " .. (function(t)
    -- Pretty-print the Lines table as Luau
    local function ser(v, depth)
        depth = depth or 0
        local indent = string.rep("    ", depth)
        if type(v) == "table" then
            local isArray = #v > 0
            local items = {{}}
            for k, val in pairs(v) do
                local key
                if type(k) == "number" then key = "" else key = ("[\\"" .. tostring(k) .. "\\"] = ") end
                if k == "textColor" and typeof(val) == "Color3" then
                    table.insert(items, indent .. "    " .. key .. string.format("Color3.fromRGB(%d, %d, %d)", val.R*255, val.G*255, val.B*255))
                else
                    table.insert(items, indent .. "    " .. key .. ser(val, depth + 1))
                end
            end
            return "{{\\n" .. table.concat(items, ",\\n") .. "\\n" .. indent .. "}}"
        elseif type(v) == "string" then
            return '"' .. v:gsub('"', '\\\\"') .. '"'
        else
            return tostring(v)
        end
    end
    return ser(t)
end)(Lines)
module.Source = newSource

print("[Diabow] Audio asset IDs wired. Test by talking to any NPC.")
"""
    PATCH_OUT.write_text(patch)
    print(f"Patch written: {PATCH_OUT}")
    print("Next step: open Studio, paste the contents of studio_patch.luau into the Command Bar, press Enter.")


if __name__ == "__main__":
    main()
