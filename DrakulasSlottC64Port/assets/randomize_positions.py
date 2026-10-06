#!/usr/bin/env python3
"""
Slumpar positioner och zoom för sprites som bara har auto-default (px=[-1,-1]).
Kör: python3 randomize_positions.py
"""

import json
import os
import random
from PIL import Image

BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
ROOMS_DIR   = os.path.join(BASE_DIR, "rooms")
SPRITES_DIR = os.path.join(BASE_DIR, "sprites")
POSITIONS   = os.path.join(BASE_DIR, "sprite_positions.json")
SENTINEL    = [-1, -1]

# Slumpintervall
X_PCT_MIN, X_PCT_MAX = 20, 80   # horisontellt
Y_PCT_MIN, Y_PCT_MAX = 55, 83   # nedre halvan — saker ligger på golv/hyllor
SCALE_MIN,  SCALE_MAX  = 0.28, 0.52
ROT_CHOICES = [0, 0, 0, 0, 0, -8, -5, 5, 8, -12, 12]  # mestadels rakt


def load_positions() -> dict:
    try:
        with open(POSITIONS) as f:
            return json.load(f)
    except Exception:
        return {}


def room_size(room_base: str) -> tuple[int, int]:
    path = os.path.join(ROOMS_DIR, room_base + ".png")
    if not os.path.exists(path):
        return 1536, 1024  # fallback
    with Image.open(path) as img:
        return img.size  # (w, h)


def sprite_size(sprite_name: str, room_h: int, scale: float) -> tuple[int, int]:
    path = os.path.join(SPRITES_DIR, sprite_name)
    if not os.path.exists(path):
        return int(room_h * scale), int(room_h * scale)
    with Image.open(path) as img:
        sw_raw, sh_raw = img.size
    sh = max(1, int(room_h * scale))
    sw = max(1, int(sw_raw * sh / sh_raw))
    return sw, sh


def main():
    random.seed()
    data = load_positions()
    updated = 0

    for key, entry in data.items():
        if entry.get("px") != SENTINEL:
            continue  # redan sparad manuellt

        room_base, sprite_base = key.split("__", 1)
        sprite_name = sprite_base + ".png"

        rw, rh = room_size(room_base)
        scale  = round(random.uniform(SCALE_MIN, SCALE_MAX), 3)
        rot    = random.choice(ROT_CHOICES)

        sw, sh = sprite_size(sprite_name, rh, scale)

        # Spritens centrum hamnar vid (cx, cy)
        pct_x = random.uniform(X_PCT_MIN, X_PCT_MAX)
        pct_y = random.uniform(Y_PCT_MIN, Y_PCT_MAX)
        cx    = int(rw * pct_x / 100)
        cy    = int(rh * pct_y / 100)
        sx    = cx - sw // 2
        sy    = cy - sh // 2

        entry["px"]       = [sx, sy]
        entry["pct"]      = [round(pct_x, 1), round(pct_y, 1)]
        entry["scale"]    = scale
        entry["rotation"] = rot
        updated += 1
        print(f"  {key}: pct=({pct_x:.1f}%,{pct_y:.1f}%) scale={scale} rot={rot}°")

    if updated:
        with open(POSITIONS, "w") as f:
            json.dump(data, f, indent=2)
        print(f"\n{updated} positioner slumpade och sparade.")
    else:
        print("Inga osparade positioner hittades.")


if __name__ == "__main__":
    main()
