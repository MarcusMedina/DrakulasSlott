#!/usr/bin/env -S uv run
# /// script
# dependencies = ["Pillow", "pygame"]
# ///
"""
Interaktiv sprite-placerare.

Startar med ett urvalsfönster — välj rum och sprite med piltangenterna.
Tryck Enter för att gå till placeringsläget.

Placeringsläge:
  Piltangenter          — flytta 10 px
  Shift + piltangenter  — flytta 1 px
  ] / [                 — förstora / förminska sprite (10%)
  Shift + ] / [         — förstora / förminska sprite (1%)
  R                     — byt rum (nästa i listan)
  Shift+R               — byt rum (föregående)
  P                     — byt sprite (nästa)
  Shift+P               — byt sprite (föregående)
  S                     — spara till sprite_positions.json + PNG-preview
  Escape                — tillbaka till urval
  Q                     — avsluta
"""

import argparse
import json
import os
import sys

try:
    from PIL import Image, ImageChops
except ImportError:
    sys.exit("Saknar Pillow. Kör: uv run sprite_placer.py")

try:
    import pygame
except ImportError:
    sys.exit("Saknar pygame. Kör: uv run sprite_placer.py")

BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
ROOMS_DIR     = os.path.join(BASE_DIR, "rooms")
SPRITES_DIR   = os.path.join(BASE_DIR, "sprites")
POSITIONS     = os.path.join(BASE_DIR, "sprite_positions.json")
PREVIEW_DIR   = os.path.join(BASE_DIR, "preview")
SPRITE_CFG    = os.path.join(BASE_DIR, "sprite_config.json")


def load_sprite_config() -> dict:
    try:
        with open(SPRITE_CFG) as f:
            return json.load(f)
    except Exception:
        return {}


def load_positions() -> dict:
    try:
        with open(POSITIONS) as f:
            return json.load(f)
    except Exception:
        return {}

WIN_W, WIN_H  = 1280, 820
PANEL_H       = 30       # statusrad längst ned
SCALE_DEFAULT = 0.35     # sprite-höjd som andel av rumshöjd
SCALE_MIN     = 0.05
SCALE_MAX     = 1.20


# ── Bildhjälpare ─────────────────────────────────────────────────────────────

def list_pngs(folder: str) -> list[str]:
    return sorted(f for f in os.listdir(folder) if f.lower().endswith(".png"))


def load_room(name: str) -> Image.Image:
    return Image.open(os.path.join(ROOMS_DIR, name)).convert("RGBA")


def build_sprite(name: str, room_h: int, scale: float) -> Image.Image:
    raw = Image.open(os.path.join(SPRITES_DIR, name)).convert("RGBA")
    h   = max(1, int(room_h * scale))
    w   = max(1, int(raw.width * h / raw.height))
    spr = raw.resize((w, h), Image.LANCZOS)
    r, g, b, a = spr.split()
    thr  = 30
    mr   = r.point(lambda v: 255 if v > thr else 0)
    mg   = g.point(lambda v: 255 if v > thr else 0)
    mb   = b.point(lambda v: 255 if v > thr else 0)
    mask = ImageChops.lighter(ImageChops.lighter(mr, mg), mb)
    spr.putalpha(mask)
    return spr


def composite(room: Image.Image, sprite: Image.Image, x: int, y: int) -> Image.Image:
    out = room.copy().convert("RGBA")
    out.paste(sprite, (x, y), sprite)
    return out.convert("RGB")


def pil_to_surf(img: Image.Image, w: int, h: int) -> "pygame.Surface":
    small = img.resize((w, h), Image.LANCZOS)
    return pygame.image.fromstring(small.tobytes(), small.size, small.mode)


# ── Urvalsfönster ─────────────────────────────────────────────────────────────

def selection_screen(screen: "pygame.Surface", font: "pygame.Font",
                     rooms: list[str], sprites: list[str],
                     ri: int, si: int, focus: int,
                     sprite_cfg: dict | None = None,
                     saved_pos: dict | None = None) -> None:
    """Ritar urvalspanelen med typ-indikatorer och ✓ för sparade positioner."""
    W, H  = screen.get_size()
    col_w = W // 2
    cfg   = sprite_cfg or {}
    pos   = saved_pos  or {}

    # Aktuellt rum (för att kolla sparade positioner)
    cur_room = os.path.splitext(rooms[ri])[0] if rooms else ""

    # Färger per sprite-typ
    TYPE_COLOR = {
        "item":  (255, 200,  60),   # varm gul  — plockvara
        "state": (140, 160, 255),   # blålila   — händelsestyrd
    }

    screen.fill((20, 20, 30))

    for col, items, idx, label in [
        (0, rooms,   ri, "RUM"),
        (1, sprites, si, "SPRITES"),
    ]:
        x0     = col * col_w
        active = (focus == col)
        hdr_color = (200, 160, 80) if active else (120, 100, 60)
        pygame.draw.rect(screen, (30, 30, 45), (x0, 0, col_w, H))
        if active:
            pygame.draw.rect(screen, (60, 60, 100), (x0, 0, col_w, H), 2)

        hdr = font.render(f"── {label} ──  (Tab för att byta)", True, hdr_color)
        screen.blit(hdr, (x0 + 12, 10))

        row_h   = 22
        visible = (H - 50) // row_h
        start   = max(0, idx - visible // 2)

        for i, name in enumerate(items[start:start + visible]):
            gi = start + i
            y  = 40 + i * row_h
            bg = (50, 50, 80) if gi == idx else (30, 30, 45)
            pygame.draw.rect(screen, bg, (x0 + 2, y - 1, col_w - 4, row_h - 2))

            if col == 1:  # sprite-kolumn
                info       = cfg.get(name, {})
                stype      = info.get("type", "")
                base_color = TYPE_COLOR.get(stype, (180, 180, 180))
                color      = (255, 255, 120) if gi == idx else base_color

                # ✓ om sparad position finns för aktuellt rum + denna sprite
                skey    = f"{cur_room}__{os.path.splitext(name)[0]}"
                checked = "✓ " if skey in pos else "  "

                # Typ-tagg
                tag = f"[{stype}]" if stype else ""
                txt = font.render(f"{checked}{name}  {tag}", True, color)
            else:
                color = (255, 220, 80) if gi == idx else (180, 180, 180)
                txt   = font.render(f"  {name}", True, color)

            screen.blit(txt, (x0 + 4, y + 1))

    # Förklaring längst ned
    legend_y = H - 42
    pygame.draw.rect(screen, (20, 20, 30), (0, legend_y - 4, W, 46))
    leg_item  = font.render("■ item = plockvara (gul)", True, TYPE_COLOR["item"])
    leg_state = font.render("■ state = händelsestyrd (blå)", True, TYPE_COLOR["state"])
    leg_check = font.render("✓ = sparad position för valt rum", True, (160, 220, 160))
    hint      = font.render("Enter = öppna placeraren   Tab = byt kolumn   Q = avsluta",
                             True, (140, 140, 140))
    screen.blit(leg_item,  (12,        legend_y))
    screen.blit(leg_state, (260,       legend_y))
    screen.blit(leg_check, (560,       legend_y))
    screen.blit(hint,      (W // 2 - hint.get_width() // 2, legend_y + 18))
    pygame.display.flip()


# ── Placeringsläge ────────────────────────────────────────────────────────────

class Placer:
    def __init__(self, rooms: list[str], sprites: list[str], ri: int, si: int):
        self.rooms    = rooms
        self.sprites  = sprites
        self.ri       = ri
        self.si       = si
        self.scale    = SCALE_DEFAULT
        self.rotation = 0
        self._load_room()
        self._load_sprite()
        self._center()

    def _load_room(self):
        self.room_img  = load_room(self.rooms[self.ri])
        self.rw, self.rh = self.room_img.size
        scale = min((WIN_W) / self.rw, (WIN_H - PANEL_H) / self.rh, 1.0)
        self.disp_w = int(self.rw * scale)
        self.disp_h = int(self.rh * scale)
        self._load_sprite()

    def _load_sprite(self):
        raw = build_sprite(self.sprites[self.si], self.rh, self.scale)
        if self.rotation % 360 != 0:
            raw = raw.rotate(-self.rotation, expand=True, resample=Image.BICUBIC)
        self.sprite_img = raw
        self.sw, self.sh = self.sprite_img.size

    def _center(self):
        """Försök ladda sparad position; fall tillbaka på standard-mitten."""
        key = (f"{os.path.splitext(self.rooms[self.ri])[0]}"
               f"__{os.path.splitext(self.sprites[self.si])[0]}")
        if os.path.exists(POSITIONS):
            try:
                with open(POSITIONS) as f:
                    data = json.load(f)
                if key in data:
                    entry = data[key]
                    self.scale    = entry.get("scale",    self.scale)
                    self.rotation = entry.get("rotation", 0)
                    self._load_sprite()
                    self.sx, self.sy = entry["px"]
                    return
            except Exception:
                pass
        # Ingen sparad position — återställ till default
        self.scale    = SCALE_DEFAULT
        self.rotation = 0
        self._load_sprite()
        self.sx = (self.rw - self.sw) // 2
        self.sy = int(self.rh * 0.70) - self.sh // 2

    def move(self, dx: int, dy: int):
        self.sx = max(-(self.sw // 2), min(self.rw - self.sw // 2, self.sx + dx))
        self.sy = max(-(self.sh // 2), min(self.rh - self.sh // 2, self.sy + dy))

    def disp_to_room(self, mx: int, my: int) -> tuple[int, int]:
        """Konvertera muskoordinater (display) till rum-pixlar."""
        rx = int(mx * self.rw / self.disp_w)
        ry = int(my * self.rh / self.disp_h)
        return rx, ry

    def start_drag(self, mx: int, my: int) -> bool:
        """Starta drag om musen är inom spritens bounding box. Returnerar True vid träff."""
        rx, ry = self.disp_to_room(mx, my)
        if self.sx <= rx <= self.sx + self.sw and self.sy <= ry <= self.sy + self.sh:
            self._drag_offset = (rx - self.sx, ry - self.sy)
            self.dragging = True
            return True
        # Klick utanför — teleportera spritens centrum dit ändå
        self.sx = rx - self.sw // 2
        self.sy = ry - self.sh // 2
        self._drag_offset = (self.sw // 2, self.sh // 2)
        self.dragging = True
        return True

    def drag_to(self, mx: int, my: int):
        if not getattr(self, "dragging", False):
            return
        rx, ry = self.disp_to_room(mx, my)
        ox, oy = self._drag_offset
        self.sx = max(-(self.sw // 2), min(self.rw - self.sw // 2, rx - ox))
        self.sy = max(-(self.sh // 2), min(self.rh - self.sh // 2, ry - oy))

    def stop_drag(self):
        self.dragging = False

    def rescale(self, delta: float):
        cx = self.sx + self.sw // 2
        cy = self.sy + self.sh // 2
        self.scale = max(SCALE_MIN, min(SCALE_MAX, self.scale + delta))
        self._load_sprite()
        self.sx = cx - self.sw // 2
        self.sy = cy - self.sh // 2

    def rotate(self, delta: int):
        cx = self.sx + self.sw // 2
        cy = self.sy + self.sh // 2
        self.rotation = (self.rotation + delta) % 360
        self._load_sprite()
        self.sx = cx - self.sw // 2
        self.sy = cy - self.sh // 2

    def cycle_room(self, d: int):
        self.ri = (self.ri + d) % len(self.rooms)
        self._load_room()
        self._center()

    def cycle_sprite(self, d: int):
        self.si = (self.si + d) % len(self.sprites)
        self._load_sprite()
        self._center()

    def render(self, screen: "pygame.Surface", font: "pygame.Font",
               sprite_cfg: dict | None = None):
        comp = composite(self.room_img, self.sprite_img, self.sx, self.sy)
        surf = pil_to_surf(comp, self.disp_w, self.disp_h)
        screen.fill((0, 0, 0))
        screen.blit(surf, (0, 0))

        pct_x  = (self.sx + self.sw // 2) / self.rw * 100
        pct_y  = (self.sy + self.sh // 2) / self.rh * 100
        sname  = self.sprites[self.si]
        stype  = (sprite_cfg or {}).get(sname, {}).get("type", "?")
        status = (f"  [{stype}] {self.rooms[self.ri]}  +  {sname}"
                  f"   px({self.sx},{self.sy})  {pct_x:.1f}%,{pct_y:.1f}%"
                  f"   skala {self.scale*100:.0f}%   rot {self.rotation}°"
                  f"   +/- storlek   ,/. rotera   ↑↓←→ 1px  Shift=10px   dra med mus   R/P byt   S spara   Esc")
        lbl = font.render(status, True, (200, 200, 200))
        pygame.draw.rect(screen, (20, 20, 20), (0, self.disp_h, WIN_W, PANEL_H))
        screen.blit(lbl, (4, self.disp_h + 7))
        pygame.display.flip()

    def save(self):
        data: dict = {}
        if os.path.exists(POSITIONS):
            try:
                with open(POSITIONS) as f:
                    data = json.load(f)
            except Exception:
                pass
        key   = (f"{os.path.splitext(self.rooms[self.ri])[0]}"
                 f"__{os.path.splitext(self.sprites[self.si])[0]}")
        pct_x = (self.sx + self.sw // 2) / self.rw * 100
        pct_y = (self.sy + self.sh // 2) / self.rh * 100
        data[key] = {
            "px":       [self.sx, self.sy],
            "pct":      [round(pct_x, 1), round(pct_y, 1)],
            "scale":    round(self.scale, 4),
            "rotation": self.rotation,
        }
        with open(POSITIONS, "w") as f:
            json.dump(data, f, indent=2)
        os.makedirs(PREVIEW_DIR, exist_ok=True)
        out = os.path.join(PREVIEW_DIR, f"{key}.png")
        composite(self.room_img, self.sprite_img, self.sx, self.sy).save(out)
        print(f"Sparat: {key}  px=({self.sx},{self.sy})  "
              f"pct=({pct_x:.1f}%,{pct_y:.1f}%)  scale={self.scale:.3f}")
        print(f"Preview: {out}")
        pygame.display.set_caption(f"✓ Sparat — {key}")


# ── Huvudloop ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("room",   nargs="?", help="Startrum (filnamn)")
    parser.add_argument("sprite", nargs="?", help="Startsprite (filnamn)")
    args = parser.parse_args()

    rooms   = list_pngs(ROOMS_DIR)
    sprites = list_pngs(SPRITES_DIR)

    if not rooms:   sys.exit(f"Inga PNG-filer i {ROOMS_DIR}")
    if not sprites: sys.exit(f"Inga PNG-filer i {SPRITES_DIR}")

    ri = rooms.index(args.room)     if args.room   in rooms   else 0
    si = sprites.index(args.sprite) if args.sprite in sprites else 0

    pygame.init()
    screen     = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Sprite Placer — Drakulas Slott")
    font       = pygame.font.SysFont("monospace", 13)
    clock      = pygame.time.Clock()
    sprite_cfg = load_sprite_config()

    MODE_SELECT  = "select"
    MODE_PLACE   = "place"
    mode         = MODE_SELECT
    focus        = 0
    placer: Placer | None = None

    def draw_select():
        selection_screen(screen, font, rooms, sprites, ri, si, focus,
                         sprite_cfg, load_positions())

    draw_select()

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                shift = bool(event.mod & pygame.KMOD_SHIFT)

                # ── Urval ──
                if mode == MODE_SELECT:
                    if event.key == pygame.K_TAB:
                        focus = 1 - focus
                    elif event.key == pygame.K_UP:
                        if focus == 0: ri = (ri - 1) % len(rooms)
                        else:          si = (si - 1) % len(sprites)
                    elif event.key == pygame.K_DOWN:
                        if focus == 0: ri = (ri + 1) % len(rooms)
                        else:          si = (si + 1) % len(sprites)
                    elif event.key == pygame.K_RETURN:
                        placer = Placer(rooms, sprites, ri, si)
                        mode   = MODE_PLACE
                        placer.render(screen, font, sprite_cfg)
                        continue
                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        running = False
                        continue
                    draw_select()

                # ── Placering ──
                elif mode == MODE_PLACE and placer:
                    step = 10 if shift else 1
                    if event.key == pygame.K_UP:       placer.move(0, -step)
                    elif event.key == pygame.K_DOWN:   placer.move(0,  step)
                    elif event.key == pygame.K_LEFT:   placer.move(-step, 0)
                    elif event.key == pygame.K_RIGHT:  placer.move( step, 0)
                    elif event.key in (pygame.K_PLUS, pygame.K_KP_PLUS, pygame.K_EQUALS):
                        placer.rescale(0.01 if shift else 0.10)
                    elif event.key in (pygame.K_MINUS, pygame.K_KP_MINUS):
                        placer.rescale(-0.01 if shift else -0.10)
                    elif event.key == pygame.K_PERIOD:
                        placer.rotate(1 if shift else 15)
                    elif event.key == pygame.K_COMMA:
                        placer.rotate(-1 if shift else -15)
                    elif event.key == pygame.K_r:
                        placer.cycle_room(-1 if shift else 1)
                    elif event.key == pygame.K_p:
                        placer.cycle_sprite(-1 if shift else 1)
                    elif event.key == pygame.K_s:
                        placer.save(); continue
                    elif event.key == pygame.K_ESCAPE:
                        ri, si = placer.ri, placer.si
                        mode   = MODE_SELECT
                        draw_select()
                        continue
                    elif event.key in (pygame.K_q,):
                        running = False; continue
                    else:
                        continue
                    placer.render(screen, font, sprite_cfg)

            # ── Mus-drag (bara i placeringsläget) ──
            elif event.type == pygame.MOUSEBUTTONDOWN and mode == MODE_PLACE and placer:
                if event.button == 1:
                    placer.start_drag(*event.pos)
                    placer.render(screen, font, sprite_cfg)

            elif event.type == pygame.MOUSEMOTION and mode == MODE_PLACE and placer:
                if getattr(placer, "dragging", False):
                    placer.drag_to(*event.pos)
                    placer.render(screen, font, sprite_cfg)

            elif event.type == pygame.MOUSEBUTTONUP and mode == MODE_PLACE and placer:
                if event.button == 1:
                    placer.stop_drag()

    pygame.quit()


if __name__ == "__main__":
    main()
