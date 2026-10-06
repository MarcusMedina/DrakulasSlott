#!/usr/bin/env python3
"""
Skapar sprite-tillstånd (eldstad, dörr) genom att REDIGERA en gemensam basbild, så att
form, vinkel, material och pixelstil är identiska mellan tillstånden.
Nyckeln läses ur shared_dev/.env (prefix sk-or) och skrivs aldrig ut.
Kör: python3 regen_state_edit.py eldstad|dorr
Resultat sparas som <namn>_edit.png i sprites/ för granskning.
"""
import base64, io, json, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

ENV = "/home/marcus/git/MarcusMedina/shared_dev/.env"
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.5-flash-image"
HERE = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(HERE, "sprites")
BAS = os.path.join(HERE, "sprite_bas")

KEEP = ("Edit this pixel art image. Keep EXACTLY the same object shape, outline, camera angle, position, size, "
        "material and pixel style. Keep the background pure black. Change ONLY the following: ")
SETS = {
    "eldstad": {
        "src": os.path.join(DIR, "eld_kamin.png"),
        "base": os.path.join(BAS, "eldstad_tom.png"),
        "base_edit": "Remove the fire, flames, embers, logs and smoke completely. The stone fireplace is cold and empty, "
                     "the inside is dark soot-covered brown-grey stone (not pure black) with a bare stone hearth floor.",
        "edits": {
            "eld_kamin.png": "Add a bright burning wood fire with tall orange and yellow flames and glowing red embers on the hearth.",
            "aska.png": "Add a pile of pale grey ash with a few charred black-brown log stumps on the hearth floor; the fire is completely out, no flames.",
            "eldstad_sonderslagen.png": "The fireplace has been smashed with a sledgehammer: the stones of the arch and back wall are broken, "
                                        "a ragged hole in the back wall leads into dark emptiness (pure black), rubble and stone chunks lie on the hearth and floor.",
        },
    },
    "dorr": {
        "src": os.path.join(DIR, "dorr_stangd.png"),
        "base": os.path.join(DIR, "dorr_stangd.png"),
        "edits": {
            "dörr_öppen.png": "The door is swung open inward toward the viewer's right on its hinges, seen as a narrow slanted door leaf at the right edge; "
                              "the doorway where it used to be is completely empty pure black.",
        },
    },
}

def key():
    for line in open(ENV, encoding="utf-8"):
        if "=" in line:
            v = line.split("=", 1)[1].strip().strip('"').strip("'")
            if v.startswith("sk-or"):
                return v
    raise SystemExit("Ingen sk-or-nyckel hittades")

def edit(base_path, instruction, out_path, k):
    b64 = base64.b64encode(open(base_path, "rb").read()).decode()
    body = json.dumps({"model": MODEL, "modalities": ["image", "text"], "messages": [{"role": "user", "content": [
        {"type": "text", "text": KEEP + instruction},
        {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}}]}]}).encode()
    req = urllib.request.Request(URL, data=body, method="POST",
        headers={"Authorization": f"Bearer {k}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=240) as r:
            d = json.loads(r.read())
        url = d["choices"][0]["message"]["images"][0]["image_url"]["url"]
        img = Image.open(io.BytesIO(base64.b64decode(url.split(",", 1)[1]))).convert("RGB")
        if img.size != (1024, 1024):
            img = img.resize((1024, 1024), Image.NEAREST)
        img.save(out_path)
        return f"OK {os.path.basename(out_path)}"
    except Exception as e:
        return f"FEL {os.path.basename(out_path)}: {type(e).__name__} {e}"

cfg = SETS[sys.argv[1]]
k = key()
if not os.path.exists(cfg["base"]):
    os.makedirs(os.path.dirname(cfg["base"]), exist_ok=True)
    print(edit(cfg["src"], cfg["base_edit"], cfg["base"], k))
with ThreadPoolExecutor(3) as ex:
    jobs = [(n, i) for n, i in cfg["edits"].items()]
    for r in ex.map(lambda j: edit(cfg["base"], j[1], os.path.join(DIR, j[0].replace(".png", "_edit.png")), k), jobs):
        print(r)
