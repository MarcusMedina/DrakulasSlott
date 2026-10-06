#!/usr/bin/env python3
"""
Genererar om klocka.png som ett fickur med guldkedja.

Kör: python3 regen_klocka.py --key DIN_OPENROUTER_NYCKEL
"""

import argparse
import base64
import os
import urllib.request
import urllib.error
import json

API_URL = "https://openrouter.ai/api/v1/images/generations"
MODEL   = "google/gemini-2.5-flash-image"
OUT     = os.path.join(os.path.dirname(os.path.abspath(__file__)), "sprites", "klocka.png")

NO_TEXT = "no text, no letters, no words, no captions, no titles, no watermarks, no labels, no numbers on the clock face"

PROMPT = (
    f"A classic antique pocket watch with a gold chain. Round gold case, hinged lid slightly open "
    f"revealing an ornate clock face with Roman numerals — wait, NO numerals, just decorative hands. "
    f"The chain drapes elegantly. Old-fashioned, Victorian era feel. "
    f"Isolated object centered on solid black background. "
    f"Commodore 64 pixel art style, 16-color limited palette, chunky expressive pixels, "
    f"classic 1980s adventure game item icon, hand-crafted feel, warm gold tones. "
    f"{NO_TEXT}"
)


def generate(api_key: str) -> None:
    payload = json.dumps({
        "model": MODEL,
        "prompt": PROMPT,
        "size": "1024x1024",
        "response_format": "b64_json",
        "n": 1,
    }).encode()

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    print(f"Genererar fickur-sprite...")
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"HTTP {e.code}: {e.read().decode()}")
        return

    b64 = data["data"][0]["b64_json"]
    img_bytes = base64.b64decode(b64)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "wb") as f:
        f.write(img_bytes)
    print(f"Sparat: {OUT}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True, help="OpenRouter API-nyckel")
    args = parser.parse_args()
    generate(args.key)


if __name__ == "__main__":
    main()
