#!/usr/bin/env python3
"""
Genererar om dörr-paret med identiskt dörrblad.
Läser OpenRouter-nyckeln ur shared_dev/.env (identifieras via prefix sk-or) utan att skriva ut den.
Kör: python3 regen_kista_set.py
"""
import base64, json, os, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

ENV = "/home/marcus/git/MarcusMedina/shared_dev/.env"
API_URL = "https://openrouter.ai/api/v1/images/generations"
MODEL = "google/gemini-2.5-flash-image"
OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")

CAMERA = (
    "A single heavy gothic pointed-arch door leaf made of dark brown vertical wooden planks with two horizontal "
    "rusty iron bands, iron rivets and a round iron keyhole plate at mid height, hinges on the RIGHT side. "
    "No door frame, no wall, no surrounding arch. Camera: straight front view at eye level. "
)
STYLE = (
    "Isolated object centered on solid pure black background. Commodore 64 pixel art style, limited palette, "
    "chunky expressive pixels, classic 1980s adventure game sprite. "
    "no text, no letters, no words, no watermarks."
)
VARIANTS = {
    "dörr_öppen.png": "The same door is swung wide open inward, seen from the front as a narrow slanted panel attached to the hinge side on the right, the doorway itself empty. The ENTIRE background including the empty doorway is flat pure black (#000000), absolutely no white or grey background. ",
}

def key():
    for line in open(ENV, encoding="utf-8"):
        if "=" in line:
            v = line.split("=", 1)[1].strip().strip('"').strip("'")
            if v.startswith("sk-or"):
                return v
    raise SystemExit("Ingen sk-or-nyckel hittades")

def gen(item, k):
    name, variant = item
    body = json.dumps({"model": MODEL, "prompt": CAMERA + variant + STYLE, "size": "1024x1024",
                       "response_format": "b64_json", "n": 1}).encode()
    req = urllib.request.Request(API_URL, data=body, method="POST",
        headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            d = json.loads(r.read())
        with open(os.path.join(OUT_DIR, name), "wb") as f:
            f.write(base64.b64decode(d["data"][0]["b64_json"]))
        return f"OK {name}"
    except urllib.error.HTTPError as e:
        return f"FEL {name}: HTTP {e.code}"

k = key()
with ThreadPoolExecutor(4) as ex:
    for res in ex.map(lambda i: gen(i, k), VARIANTS.items()):
        print(res)
