#!/usr/bin/env python3
"""
Skapar kist-varianterna genom att REDIGERA vampyr_i_kista.png (basbilden), så att kista,
piedestal, kamera och pixelstil är identiska. Bara vampyr/lock ändras.
Nyckeln läses ur shared_dev/.env (prefix sk-or) och skrivs aldrig ut.
Kör: python3 regen_kista_edit.py [kista_stangd.png vampyr_dad.png vampyr_vaknar.png]
"""
import base64, io, json, os, sys, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from PIL import Image

ENV = "/home/marcus/git/MarcusMedina/shared_dev/.env"
URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.5-flash-image"
DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites")
SRC = os.path.join(DIR, "vampyr_i_kista.png")
BASE = os.path.join(os.path.dirname(DIR), "sprite_bas", "kista_tom.png")

KEEP = ("Edit this pixel art image. Keep EXACTLY the same stone pedestal, the same wooden coffin shape, the same "
        "camera angle, same position, same size, same pixel style and same red velvet lining. Keep the background pure black "
        "and use no pure black inside the object. Change ONLY the following: ")
EDITS = {
    "vampyr_i_kista.png": "Add a pale vampire sleeping inside, head at the LEFT end, in a dark maroon and navy cape, arms crossed on his chest, eyes closed.",
    "kista_stangd.png": "Close the coffin with a wooden lid that matches the coffin wood and fits its exact outline; no vampire visible.",
    "vampyr_dad.png": "Add a dead pale vampire lying inside, head at the LEFT end, dark maroon and navy cape, lifeless grey-white skin, eyes closed, arms at his sides, a SMALL wooden stake sticking up from his chest with a little dark red blood.",
    "vampyr_vaknar.png": "Add a pale vampire sitting up with his upper body upright and clearly rising above the coffin edge, at the LEFT end, dark maroon and navy cape with high red collar, glowing red eyes, fangs bared, both arms stretched forward over the coffin, menacing.",
}

def key():
    for line in open(ENV, encoding="utf-8"):
        if "=" in line:
            v = line.split("=", 1)[1].strip().strip('"').strip("'")
            if v.startswith("sk-or"):
                return v
    raise SystemExit("Ingen sk-or-nyckel hittades")

def edit(name, k):
    b64 = base64.b64encode(open(BASE, "rb").read()).decode()
    body = json.dumps({"model": MODEL, "modalities": ["image", "text"], "messages": [{"role": "user", "content": [
        {"type": "text", "text": KEEP + EDITS[name]},
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
        out = os.path.join(DIR, name.replace(".png", "_edit.png"))
        img.save(out)
        return f"OK {out}"
    except Exception as e:
        return f"FEL {name}: {type(e).__name__} {e}"

def make_base(k):
    global BASE
    os.makedirs(os.path.dirname(BASE), exist_ok=True)
    real = BASE
    BASE = SRC
    EDITS["_tom.png"] = "Remove the vampire completely. The coffin is open and empty, showing only the red velvet lining inside."
    r = edit("_tom.png", k)
    BASE = real
    os.replace(os.path.join(DIR, "_tom_edit.png"), real)
    return r

k = key()
if not os.path.exists(BASE):
    print(make_base(k))
names = sys.argv[1:] or list(EDITS)
with ThreadPoolExecutor(3) as ex:
    for r in ex.map(lambda n: edit(n, k), names):
        print(r)
