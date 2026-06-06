"""
DIABLOW — Tristram NPC voice line generator.

Generates ElevenLabs MP3s for every NPC dialogue line.
Output: /Users/doge/saarvis/roblox/diablow/audio/<npc>_<line_id>.mp3

Uses ElevenLabs public voices chosen to match D1 character vibes.
After running this script: upload all MP3s to Roblox via the
companion `upload_audio.py` (needs Roblox Open Cloud API key).
"""

import os
import sys
import time
from pathlib import Path

import requests

ROOT = Path("/Users/doge/saarvis/roblox/diablow")
AUDIO_DIR = ROOT / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Pull API key from automations/.env
_env_path = Path("/Users/doge/saarvis/automations/.env")
API_KEY = os.getenv("ELEVENLABS_API_KEY")
if not API_KEY and _env_path.exists():
    for line in _env_path.read_text().splitlines():
        if line.startswith("ELEVENLABS_API_KEY="):
            API_KEY = line.split("=", 1)[1].strip()
            break
if not API_KEY:
    sys.exit("ELEVENLABS_API_KEY not found in env or automations/.env")

# Voice mapping — public ElevenLabs voices chosen for D1 character vibe
VOICE_BY_NPC = {
    # NPC          voice_id                  stability  similarity  style  speed   character note
    "cain":      ("JBFqnCBsd6RMkjVDRZzb",     0.75,      0.85,       0.0,   0.80),  # George — older British scholar
    "griswold":  ("nPczCjzI2devNBz1zQrb",     0.70,      0.80,       0.0,   0.90),  # Brian — deep, gruff
    "pepin":     ("pNInz6obpgDQGcFmaJgB",     0.70,      0.85,       0.0,   0.95),  # Adam — warm, fatherly
    "adria":     ("XB0fDUnXU5powFXDhCwa",     0.55,      0.75,       0.4,   0.85),  # Charlotte — exotic, witchy
    "ogden":     ("IKne3meq5aSn9XLyUdCD",     0.65,      0.80,       0.0,   1.0),   # Charlie — warm jovial innkeeper
    "gillian":   ("pFZP5JQG7iQjIQuC4Bku",     0.50,      0.80,       0.0,   1.0),   # Lily — young woman
    "farnham":   ("onwK4e9ZLuTAKqWW03F9",     0.30,      0.65,       0.5,   0.75),  # Daniel — slurring drunk (low stability + slow)
    "wirt":      ("pFZP5JQG7iQjIQuC4Bku",     0.40,      0.70,       0.5,   1.1),   # Lily — smug boy (higher style, faster)
    "narrator":  ("JBFqnCBsd6RMkjVDRZzb",     0.85,      0.90,       0.0,   0.85),  # George — Cain-style opening narration
}

# Canonical D1 Tristram dialogue. Lines selected from the actual game.
# Some are slightly condensed for v1 TTS length.
LINES = {
    # ----- DECKARD CAIN — village elder, "Stay a while and listen" -----
    "cain_greet": "Hmm... greetings, friend. You have arrived in Tristram in a time of need. Stay a while and listen, for I have much to tell.",
    "cain_butcher": "It is a long, sad tale. But if you would like to hear of it, I shall tell you. The Butcher dwells beneath us — a creature of pure rage. May the Light grant you the strength to face him.",
    "cain_king": "Of King Leoric? Once a great and noble man, he was driven to madness by the demon Diablo's whispers. The dead now serve him in the catacombs.",
    "cain_farewell": "May Light guide your steps, traveler. And remember — knowledge is the only true weapon against the dark.",

    # ----- GRISWOLD — blacksmith -----
    "griswold_greet": "Well, met, traveler. I am Griswold — Tristram's blacksmith. If it's good steel you need, you've come to the right place.",
    "griswold_wares": "I've a fine selection of arms and armor. None of it is fancy, but every piece will hold up against what hunts in those tunnels.",
    "griswold_warning": "Be careful down there, friend. The cathedral was sealed for good reason. Whatever Lazarus stirred up... it's still down there.",

    # ----- PEPIN — healer -----
    "pepin_greet": "Greetings. I am Pepin, Tristram's healer. Tell me, are you injured? Sit a moment — I shall mix you a draught.",
    "pepin_potions": "Take these healing potions. The herbs grow wild on the hillside — there is no cost to you. Only return them, drained, that I may refill them.",
    "pepin_farewell": "Walk in the Light, friend. And do not let the darkness claim you.",

    # ----- ADRIA — witch -----
    "adria_greet": "Hssss... you come to the witch, do you? Few of the villagers dare to cross my bridge. What is it you seek, traveler?",
    "adria_scrolls": "I have scrolls of power, staves of binding, and elixirs no priest of Zakarum would touch. They have a price. They are worth it.",
    "adria_warning": "Beware the deep dark, traveler. There are things below this town older than the cathedral. Older than the kingdom of Khanduras itself.",

    # ----- OGDEN — innkeeper -----
    "ogden_greet": "Welcome to the Tavern of the Rising Sun, friend! A warm fire, a soft bed, and an ear for your tale — all yours for a few coins.",
    "ogden_gillian": "My barmaid Gillian — sweet girl. She tends to her sick grandmother in the cottage just there. Be kind to her, would you?",
    "ogden_farewell": "Safe travels, friend. And if you make it back from the dark — there'll be a mug waiting for you.",

    # ----- GILLIAN — barmaid -----
    "gillian_greet": "Oh! Hello, traveler. I... I'm Gillian. I help Ogden in the tavern and care for my grandmother. Is there something I can do for you?",
    "gillian_grandma": "My grandmother, she... she barely eats now. The demons in the cathedral — I think they reach her even in her dreams. Please, can you help us?",

    # ----- FARNHAM — the drunk -----
    "farnham_greet": "Heh... oh, look. Fresh meat. *hic* Pull up a... pull up a stool, friend. You'll need a drink before you go down there. *hic*",
    "farnham_butcher": "The Butcher! Hee hee hee! Oh, the Butcher... *hic*... He made... he made buttons of my friends. Buttons! *hic*",

    # ----- WIRT — peg-leg boy -----
    "wirt_greet": "Heh. Look what we have here. Fresh blood for the cathedral. You wanna buy something? I got... things. Things you can't get from old Griswold.",
    "wirt_warning": "Take your time. I'll be here. Unlike SOME people in this town... *whistles*",

    # ----- KAEL RILLS — dying townsman at cathedral steps -----
    "kael_dying": "Please... traveler... the Butcher... he killed my men... my men are still down there... please... find them...",

    # ----- NARRATOR — opening intro -----
    "narrator_intro": "The village of Tristram. Once a quiet town in the kingdom of Khanduras. Now — a place where the dead walk, the cathedral burns red with witchlight, and only fools or heroes still tread its streets. Stay a while. And listen.",
}

# Group lines by NPC for clean console output
def npc_of(line_id: str) -> str:
    return line_id.split("_", 1)[0]

def synth(line_id: str, text: str) -> bool:
    """Generate one MP3. Returns True on success."""
    out_path = AUDIO_DIR / f"{line_id}.mp3"
    if out_path.exists() and out_path.stat().st_size > 1000:
        print(f"  [cached] {line_id}.mp3")
        return True

    npc = "narrator" if line_id.startswith("narrator_") else line_id.split("_", 1)[0]
    if npc == "kael":
        npc = "farnham"  # use drunk slurring voice for the dying townsman — fits

    cfg = VOICE_BY_NPC.get(npc)
    if not cfg:
        print(f"  [skip] no voice mapped for {npc}")
        return False
    voice_id, stability, sim, style, speed = cfg

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": stability,
            "similarity_boost": sim,
            "style": style,
            "use_speaker_boost": True,
        },
    }
    params = {"output_format": "mp3_44100_128"}
    headers = {"xi-api-key": API_KEY, "Content-Type": "application/json"}

    try:
        resp = requests.post(url, headers=headers, json=payload, params=params, timeout=60)
        resp.raise_for_status()
        out_path.write_bytes(resp.content)
        kb = out_path.stat().st_size // 1024
        print(f"  [ok]  {line_id}.mp3 ({kb} KB)")
        time.sleep(0.4)  # gentle rate limit
        return True
    except Exception as e:
        print(f"  [err] {line_id}: {e}")
        return False


def main():
    print(f"Generating {len(LINES)} Tristram voice lines to {AUDIO_DIR}")
    print(f"Voice mapping: {len(VOICE_BY_NPC)} distinct ElevenLabs voices")
    print()
    ok = 0
    for line_id, text in LINES.items():
        if synth(line_id, text):
            ok += 1
    print()
    print(f"Done. {ok}/{len(LINES)} generated.")
    # Write a manifest the upload script + Roblox config can read
    manifest_path = ROOT / "audio_manifest.json"
    import json
    manifest = {
        line_id: {
            "text": LINES[line_id],
            "npc": npc_of(line_id) if not line_id.startswith("narrator_") else "narrator",
            "file": f"audio/{line_id}.mp3",
            "voice_id": (VOICE_BY_NPC.get("narrator" if line_id.startswith("narrator_") else
                         ("farnham" if line_id.startswith("kael_") else npc_of(line_id))) or [None])[0],
            "asset_id": None,  # populated after upload_audio.py runs
        }
        for line_id in LINES
    }
    manifest_path.write_text(json.dumps(manifest, indent=2))
    print(f"Manifest written: {manifest_path}")


if __name__ == "__main__":
    main()
