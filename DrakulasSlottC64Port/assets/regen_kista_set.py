#!/usr/bin/env python3
"""
Genererar om alla fyra kist-sprites med identisk kameravinkel.
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
    "Classic hexagonal tapered wooden vampire coffin lying horizontally, wider at the head end on the LEFT, "
    "narrower at the foot end on the RIGHT, resting on a low rectangular grey stone pedestal. "
    "Camera: straight side view from the front, only slightly elevated, the long side of the coffin faces the viewer, "
    "NOT isometric, NOT top-down, no diagonal rotation. "
)
STYLE = (
    "Isolated object centered on solid pure black background. Commodore 64 pixel art style, limited palette, "
    "chunky expressive pixels, classic 1980s adventure game sprite. "
    "IMPORTANT: black is used as transparency, so the object itself must contain NO pure black pixels: use dark navy, dark purple or dark maroon for shadows and outlines, and fill the inside of the coffin completely with rich red velvet lining. "
    "no text, no letters, no words, no watermarks."
)
VARIANTS = {
    "kista_stangd.png": "The coffin lid is closed. Dark brown wood with iron corner bands. ",
    "vampyr_i_kista.png": "The lid is removed. A pale vampire in a dark maroon and navy cape (not black) lying on red velvet sleeps inside, arms crossed on chest, eyes closed. ",
    "vampyr_dad.png": "The lid is removed. A pale vampire in a dark maroon and navy cape (not black) lying on red velvet, head on the LEFT end, arms at his sides, eyes closed, a wooden stake standing upright in his chest with a little dark red blood, lifeless grey-white skin. ",
    "vampyr_vaknar.png": "The lid is removed. A pale vampire in a dark maroon and navy cape (not black) is sitting up halfway inside the coffin, glowing red eyes, fangs bared, arms reaching forward, menacing. ",
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

import sys
k = key()
only = sys.argv[1:]
if only:
    jobs = [(f"{n[:-4]}_v{i}.png", VARIANTS[n]) for n in only for i in (1, 2, 3)]
else:
    jobs = list(VARIANTS.items())
with ThreadPoolExecutor(4) as ex:
    for res in ex.map(lambda i: gen(i, k), jobs):
        print(res)
