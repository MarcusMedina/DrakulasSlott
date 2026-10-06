#!/usr/bin/env -S uv run
# /// script
# dependencies = ["Pillow", "pygame"]
# ///
"""
Interaktiv sprite-placerare — flytta en sprite med piltangenterna.

Kör: uv run sprite_placer.py <rumsbild> <sprite>

Kontroller:
  Piltangenter          — flytta 10 px
  Shift + piltangenter  — flytta 1 px
  S                     — spara position till sprite_positions.json + PNG-preview
  Q / Escape            — avsluta
"""

import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageChops
except ImportError:
    sys.exit("Pillow saknas. Kör: uv run sprite_placer.py ...")

try:
    import pygame
except ImportError:
    sys.exit("pygame saknas. Kör: uv run sprite_placer.py ...")

BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
POSITIONS = os.path.join(BASE_DIR, "sprite_positions.json")

DISPLAY_MAX_W = 1280
DISPLAY_MAX_H = 800


def make_sprite(path: str, room_h: int) -> Image.Image:
    raw = Image.open(path).convert("RGBA")
    h   = int(room_h * 0.35)
    w   = int(raw.width * h / raw.height)
    spr = raw.resize((w, h), Image.LANCZOS)
    r, g, b, a = spr.split()
    thr   = 30
    mr    = r.point(lambda v: 255 if v > thr else 0)
    mg    = g.point(lambda v: 255 if v > thr else 0)
    mb    = b.point(lambda v: 255 if v > thr else 0)
    mask  = ImageChops.lighter(ImageChops.lighter(mr, mg), mb)
    spr.putalpha(mask)
    return spr


def composite_pil(room: Image.Image, sprite: Image.Image, x: int, y: int) -> Image.Image:
    out = room.copy().convert("RGBA")
    out.paste(sprite, (x, y), sprite)
    return out.convert("RGB")


def pil_to_surface(img: Image.Image) -> "pygame.Surface":
    return pygame.image.fromstring(img.tobytes(), img.size, img.mode)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("room",   help="Rumsbild (relativ eller absolut sökväg)")
    parser.add_argument("sprite", help="Sprite (relativ eller absolut sökväg)")
    args = parser.parse_args()

    def resolve(p):
        return p if (os.path.isabs(p) or os.path.exists(p)) else os.path.join(BASE_DIR, p)

    room_path   = resolve(args.room)
    sprite_path = resolve(args.sprite)

    room_img   = Image.open(room_path).convert("RGBA")
    sprite_img = make_sprite(sprite_path, room_img.height)

    rw, rh = room_img.size
    sw, sh = sprite_img.size

    # Startposition: mitten horisontellt, 70% ner
    sx = (rw - sw) // 2
    sy = int(rh * 0.70) - sh // 2

    scale   = min(DISPLAY_MAX_W / rw, DISPLAY_MAX_H / rh, 1.0)
    disp_w  = int(rw * scale)
    disp_h  = int(rh * scale)

    pygame.init()
    screen = pygame.display.set_mode((disp_w, disp_h + 28))
    room_name   = os.path.basename(room_path)
    sprite_name = os.path.basename(sprite_path)
    pygame.display.set_caption(f"{room_name} + {sprite_name}")
    font = pygame.font.SysFont("monospace", 13)
    clock = pygame.time.Clock()

    def redraw():
        comp  = composite_pil(room_img, sprite_img, sx, sy)
        small = comp.resize((disp_w, disp_h), Image.LANCZOS)
        surf  = pil_to_surface(small)
        screen.fill((30, 30, 30))
        screen.blit(surf, (0, 0))

        pct_x = (sx + sw // 2) / rw * 100
        pct_y = (sy + sh // 2) / rh * 100
        txt = (f"  px ({sx}, {sy})   centrum {pct_x:.1f}%, {pct_y:.1f}%"
               f"   ↑↓←→=10px  Shift=1px  S=spara  Q=avsluta")
        label = font.render(txt, True, (200, 200, 200))
        screen.blit(label, (4, disp_h + 6))
        pygame.display.flip()

    def save_pos():
        data: dict = {}
        if os.path.exists(POSITIONS):
            try:
                with open(POSITIONS) as f:
                    data = json.load(f)
            except Exception:
                pass

        key   = f"{os.path.splitext(room_name)[0]}__{os.path.splitext(sprite_name)[0]}"
        pct_x = (sx + sw // 2) / rw * 100
        pct_y = (sy + sh // 2) / rh * 100
        data[key] = {"px": [sx, sy], "pct": [round(pct_x, 1), round(pct_y, 1)]}
        with open(POSITIONS, "w") as f:
            json.dump(data, f, indent=2)

        out_dir  = os.path.join(BASE_DIR, "preview")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, f"{key}.png")
        composite_pil(room_img, sprite_img, sx, sy).save(out_path)
        print(f"Sparat: {key}  px=({sx},{sy})  pct=({pct_x:.1f}%, {pct_y:.1f}%)")
        print(f"Preview: {out_path}")
        pygame.display.set_caption(f"Sparat! {key}")

    redraw()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                shift = bool(event.mod & pygame.KMOD_SHIFT)
                step  = 1 if shift else 10
                if event.key == pygame.K_UP:
                    sx_new, sy_new = sx, sy - step
                elif event.key == pygame.K_DOWN:
                    sx_new, sy_new = sx, sy + step
                elif event.key == pygame.K_LEFT:
                    sx_new, sy_new = sx - step, sy
                elif event.key == pygame.K_RIGHT:
                    sx_new, sy_new = sx + step, sy
                elif event.key == pygame.K_s:
                    save_pos(); continue
                elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                    running = False; continue
                else:
                    continue

                sx = max(-(sw // 2), min(rw - sw // 2, sx_new))
                sy = max(-(sh // 2), min(rh - sh // 2, sy_new))
                redraw()

    pygame.quit()


if __name__ == "__main__":
    main()
