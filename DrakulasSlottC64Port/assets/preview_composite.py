#!/usr/bin/env python3
"""
Förhandsvisning: kompositera en sprite ovanpå en rumsbild.

Kör: python3 preview_composite.py <rumsbild> <sprite> [--out output.png] [--pos center|bottom|bottomleft]

Exempel:
  python3 preview_composite.py rooms/02_lasrummet.png sprites/eld_kamin.png
  python3 preview_composite.py rooms/07_kapellet.png sprites/nyckel.png --pos bottomleft
  python3 preview_composite.py rooms/11_sjo_slott.png sprites/ekan_vid_strand.png --pos bottom
"""

import argparse
import os
import sys

try:
    from PIL import Image
except ImportError:
    print("Pillow saknas. Kör: pip install Pillow")
    sys.exit(1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def composite(room_path: str, sprite_path: str, out_path: str, pos: str) -> None:
    room = Image.open(room_path).convert("RGBA")
    sprite_raw = Image.open(sprite_path).convert("RGBA")

    # Skala spriten till ~30% av rumsbildens höjd
    sprite_h = int(room.height * 0.35)
    ratio = sprite_h / sprite_raw.height
    sprite_w = int(sprite_raw.width * ratio)
    sprite = sprite_raw.resize((sprite_w, sprite_h), Image.LANCZOS)

    # Gör svart bakgrund transparent (threshold-mask)
    r, g, b, a = sprite.split()
    from PIL import ImageChops
    # Pixlar mörkare än tröskeln → transparenta
    threshold = 30
    mask_r = r.point(lambda x: 255 if x > threshold else 0)
    mask_g = g.point(lambda x: 255 if x > threshold else 0)
    mask_b = b.point(lambda x: 255 if x > threshold else 0)
    # Pixel är synlig om minst en kanal är ljus
    from PIL import ImageFilter
    combined = ImageChops.lighter(ImageChops.lighter(mask_r, mask_g), mask_b)
    sprite.putalpha(combined)

    # Positionering
    rw, rh = room.size
    sw, sh = sprite.size
    margin = 20

    # Stöd för "X%,Y%" — spritens centrum placeras vid den procenten av rummet
    if "," in pos and "%" in pos:
        px_str, py_str = pos.replace("%", "").split(",")
        cx = int(rw * float(px_str.strip()) / 100)
        cy = int(rh * float(py_str.strip()) / 100)
        x = cx - sw // 2
        y = cy - sh // 2
    else:
        positions = {
            "center":      ((rw - sw) // 2, (rh - sh) // 2),
            "bottom":      ((rw - sw) // 2, rh - sh - margin),
            "bottomleft":  (margin,          rh - sh - margin),
            "bottomright": (rw - sw - margin, rh - sh - margin),
            "topleft":     (margin,           margin),
        }
        x, y = positions.get(pos, positions["bottom"])

    room.paste(sprite, (x, y), sprite)
    room.convert("RGB").save(out_path)
    print(f"Sparad: {out_path}")


def main():
    parser = argparse.ArgumentParser(description="Förhandsvisning sprite + rum")
    parser.add_argument("room",   help="Rumsbild (relativ till assets/ eller absolut)")
    parser.add_argument("sprite", help="Sprite (relativ till assets/ eller absolut)")
    parser.add_argument("--out",  default=None, help="Utdatafil (default: preview_<rum>_<sprite>.png)")
    parser.add_argument("--pos",  default="bottom",
                        help="Position: fördefinierad (center/bottom/bottomleft/bottomright/topleft) "
                             "eller 'X%%,Y%%' procentkoordinater för spritens centrum (t.ex. '50%%,65%%')")
    args = parser.parse_args()

    def resolve(p):
        if os.path.isabs(p):
            return p
        if os.path.exists(p):
            return p
        return os.path.join(BASE_DIR, p)

    room_path   = resolve(args.room)
    sprite_path = resolve(args.sprite)

    if not os.path.exists(room_path):
        print(f"Hittar inte: {room_path}")
        sys.exit(1)
    if not os.path.exists(sprite_path):
        print(f"Hittar inte: {sprite_path}")
        sys.exit(1)

    if args.out:
        out_path = args.out
    else:
        room_name   = os.path.splitext(os.path.basename(room_path))[0]
        sprite_name = os.path.splitext(os.path.basename(sprite_path))[0]
        out_path = os.path.join(BASE_DIR, f"preview_{room_name}_{sprite_name}.png")

    composite(room_path, sprite_path, out_path, args.pos)


if __name__ == "__main__":
    main()
