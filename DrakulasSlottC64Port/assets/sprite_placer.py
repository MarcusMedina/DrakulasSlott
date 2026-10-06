#!/usr/bin/env -S uv run
# /// script
# dependencies = ["Pillow", "pygame"]
# ///
"""
Interaktiv sprite-placerare.

Startar med ett urvalsfönster — välj rum och sprite med piltangenterna.
Tryck Enter för att gå till placeringsläget.

Placeringsläge:
  Piltangenter          — flytta 1 px
  Shift + piltangenter  — flytta 10 px
  + / -                 — förstora / förminska sprite (10%)
  Shift + + / -         — förstora / förminska sprite (1%)
  , / .                 — rotera -15° / +15°
  Shift + , / .         — rotera -1° / +1°
  R                     — byt rum (nästa i listan)
  Shift+R               — byt rum (föregående)
  P                     — byt sprite (nästa i filtrerad lista)
  Shift+P               — byt sprite (föregående)
  Space                 — visa alla sprites i aktuellt rum
  S                     — spara till sprite_positions.json + PNG-preview
  Escape                — tillbaka till urval
  Q                     — avsluta

OBS: Sprites listan är FILTRERAD per rum.
  item-sprites visas alltid (kan plockas upp och lämnas var som helst).
  state-sprites visas bara i de rum de tillhör.
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

WIN_W, WIN_H  = 1280, 820
PANEL_H       = 30
SCALE_DEFAULT = 0.35
SCALE_MIN     = 0.05
SCALE_MAX     = 1.20

# Sentinel: px [-1,-1] betyder "beräkna från pct när rummet laddas"
_SENTINEL_PX  = [-1, -1]


# ── Config & positions ────────────────────────────────────────────────────────

def load_sprite_config() -> dict:
    try:
        with open(SPRITE_CFG) as f:
            cfg = json.load(f)
        # Ta bort meta-nycklar som _comment
        return {k: v for k, v in cfg.items() if not k.startswith("_")}
    except Exception:
        return {}


def load_positions() -> dict:
    try:
        with open(POSITIONS) as f:
            return json.load(f)
    except Exception:
        return {}


def save_positions(data: dict) -> None:
    with open(POSITIONS, "w") as f:
        json.dump(data, f, indent=2)


# ── Filtrering: vilka sprites visas i vilket rum ──────────────────────────────

def sprites_for_room(room_name: str, all_sprites: list[str], sprite_cfg: dict) -> list[str]:
    """
    Returnerar sprites relevanta för detta rum.
      item  (all_rooms=True)  → visas alltid
      state (all_rooms=False) → visas bara om rummet finns i home_rooms
    """
    room_base = os.path.splitext(room_name)[0]
    result = []
    for s in all_sprites:
        info  = sprite_cfg.get(s, {})
        stype = info.get("type", "item")
        if info.get("all_rooms", stype == "item"):
            result.append(s)
        else:
            home_rooms = info.get("home_rooms", [])
            if room_base in home_rooms:
                result.append(s)
    return result or all_sprites   # fallback: visa allt om filter ger tomt


# ── Auto-seed standardpositioner ─────────────────────────────────────────────

def seed_all_defaults(all_sprites: list[str], sprite_cfg: dict) -> int:
    """
    Skapar standardposter i sprite_positions.json för alla sprites som har
    ett default_room men ingen sparad position än.
    Positionen sätts till 50%x / 70%y (beräknas i pixlar när rummet laddas).
    """
    data = load_positions()
    added = 0
    for sprite_file in all_sprites:
        info = sprite_cfg.get(sprite_file, {})
        default_room = info.get("default_room")
        if not default_room:
            continue
        key = f"{default_room}__{os.path.splitext(sprite_file)[0]}"
        if key in data:
            continue
        data[key] = {
            "px":       _SENTINEL_PX,
            "pct":      [50.0, 70.0],
            "scale":    SCALE_DEFAULT,
            "rotation": 0,
        }
        added += 1
        print(f"  Auto-default: {key}")
    if added:
        save_positions(data)
        print(f"{added} standardpositioner tillagda i sprite_positions.json")
    return added


# ── Bildhjälpare ──────────────────────────────────────────────────────────────

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
                     rooms: list[str], filtered_sprites: list[str],
                     all_sprites: list[str],
                     ri: int, si: int, focus: int,
                     sprite_cfg: dict | None = None,
                     saved_pos: dict | None = None) -> None:
    """Ritar urvalspanelen med typ-indikatorer och ✓ för sparade positioner."""
    W, H  = screen.get_size()
    col_w = W // 2
    cfg   = sprite_cfg or {}
    pos   = saved_pos  or {}

    cur_room = os.path.splitext(rooms[ri])[0] if rooms else ""

    TYPE_COLOR = {
        "item":  (255, 200,  60),
        "state": (140, 160, 255),
    }

    screen.fill((20, 20, 30))

    # Rum-kolumn använder rooms, sprite-kolumn använder filtered_sprites
    cols = [
        (0, rooms,            ri, "RUM"),
        (1, filtered_sprites, si, f"SPRITES  [{len(filtered_sprites)}/{len(all_sprites)}]"),
    ]
    for col, items, idx, label in cols:
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

            if col == 1:
                info       = cfg.get(name, {})
                stype      = info.get("type", "")
                base_color = TYPE_COLOR.get(stype, (180, 180, 180))
                color      = (255, 255, 120) if gi == idx else base_color

                skey    = f"{cur_room}__{os.path.splitext(name)[0]}"
                entry   = pos.get(skey, {})
                is_default = entry.get("px") == _SENTINEL_PX if entry else False
                checked = "⬡ " if is_default else ("✓ " if skey in pos else "  ")

                tag = f"[{stype}]" if stype else ""
                txt = font.render(f"{checked}{name}  {tag}", True, color)
            else:
                color = (255, 220, 80) if gi == idx else (180, 180, 180)
                txt   = font.render(f"  {name}", True, color)

            screen.blit(txt, (x0 + 4, y + 1))

    legend_y = H - 42
    pygame.draw.rect(screen, (20, 20, 30), (0, legend_y - 4, W, 46))
    leg_item  = font.render("■ item = plockvara (gul)", True, TYPE_COLOR["item"])
    leg_state = font.render("■ state = händelsestyrd (blå)", True, TYPE_COLOR["state"])
    leg_check = font.render("✓ = sparad   ⬡ = auto-default (placera och spara)", True, (160, 220, 160))
    hint      = font.render("Enter = öppna placeraren   Tab = byt kolumn   Q = avsluta",
                             True, (140, 140, 140))
    screen.blit(leg_item,  (12,  legend_y))
    screen.blit(leg_state, (260, legend_y))
    screen.blit(leg_check, (530, legend_y))
    screen.blit(hint,      (W // 2 - hint.get_width() // 2, legend_y + 18))
    pygame.display.flip()


# ── Placeringsläge ────────────────────────────────────────────────────────────

class Placer:
    def __init__(self, rooms: list[str], sprites: list[str], ri: int, si: int,
                 all_sprites: list[str], sprite_cfg: dict):
        self.rooms       = rooms
        self.sprites     = sprites    # filtrerad lista för aktuellt rum
        self.all_sprites = all_sprites
        self.sprite_cfg  = sprite_cfg
        self.ri          = ri
        self.si          = si
        self.scale       = SCALE_DEFAULT
        self.rotation    = 0
        self.dragging    = False
        self._load_room()
        self._load_sprite()
        self._center()

    def _load_room(self):
        self.room_img    = load_room(self.rooms[self.ri])
        self.rw, self.rh = self.room_img.size
        scale = min(WIN_W / self.rw, (WIN_H - PANEL_H) / self.rh, 1.0)
        self.disp_w = int(self.rw * scale)
        self.disp_h = int(self.rh * scale)

    def _load_sprite(self):
        raw = build_sprite(self.sprites[self.si], self.rh, self.scale)
        if self.rotation % 360 != 0:
            raw = raw.rotate(-self.rotation, expand=True, resample=Image.BICUBIC)
        self.sprite_img = raw
        self.sw, self.sh = self.sprite_img.size

    def _center(self):
        """Ladda sparad position; hantera auto-default (sentinel px); fall back på standard."""
        key = (f"{os.path.splitext(self.rooms[self.ri])[0]}"
               f"__{os.path.splitext(self.sprites[self.si])[0]}")
        if os.path.exists(POSITIONS):
            try:
                with open(POSITIONS) as f:
                    data = json.load(f)
                if key in data:
                    entry = data[key]
                    self.scale    = entry.get("scale",    SCALE_DEFAULT)
                    self.rotation = entry.get("rotation", 0)
                    self._load_sprite()
                    px = entry.get("px", _SENTINEL_PX)
                    if px and px != _SENTINEL_PX:
                        self.sx, self.sy = px
                    else:
                        # Auto-default: beräkna från pct
                        pct = entry.get("pct", [50.0, 70.0])
                        self.sx = int(self.rw * pct[0] / 100) - self.sw // 2
                        self.sy = int(self.rh * pct[1] / 100) - self.sh // 2
                    return
            except Exception:
                pass
        self.scale    = SCALE_DEFAULT
        self.rotation = 0
        self._load_sprite()
        self.sx = (self.rw - self.sw) // 2
        self.sy = int(self.rh * 0.70) - self.sh // 2

    def move(self, dx: int, dy: int):
        self.sx = max(-(self.sw // 2), min(self.rw - self.sw // 2, self.sx + dx))
        self.sy = max(-(self.sh // 2), min(self.rh - self.sh // 2, self.sy + dy))

    def disp_to_room(self, mx: int, my: int) -> tuple[int, int]:
        rx = int(mx * self.rw / self.disp_w)
        ry = int(my * self.rh / self.disp_h)
        return rx, ry

    def start_drag(self, mx: int, my: int) -> bool:
        rx, ry = self.disp_to_room(mx, my)
        if self.sx <= rx <= self.sx + self.sw and self.sy <= ry <= self.sy + self.sh:
            self._drag_offset = (rx - self.sx, ry - self.sy)
        else:
            self.sx = rx - self.sw // 2
            self.sy = ry - self.sh // 2
            self._drag_offset = (self.sw // 2, self.sh // 2)
        self.dragging = True
        return True

    def drag_to(self, mx: int, my: int):
        if not self.dragging:
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
        old_sprite = self.sprites[self.si] if self.sprites else None
        self.ri    = (self.ri + d) % len(self.rooms)
        # Uppdatera filtrerad sprite-lista för det nya rummet
        self.sprites = sprites_for_room(self.rooms[self.ri], self.all_sprites, self.sprite_cfg)
        if old_sprite and old_sprite in self.sprites:
            self.si = self.sprites.index(old_sprite)
        else:
            self.si = 0
        self._load_room()
        self._load_sprite()
        self._center()

    def cycle_sprite(self, d: int):
        self.si = (self.si + d) % len(self.sprites)
        self.scale    = SCALE_DEFAULT
        self.rotation = 0
        self._load_sprite()
        self._center()

    def render(self, screen: "pygame.Surface", font: "pygame.Font",
               sprite_cfg: dict | None = None):
        comp = composite(self.room_img, self.sprite_img, self.sx, self.sy)
        surf = pil_to_surf(comp, self.disp_w, self.disp_h)
        screen.fill((0, 0, 0))
        screen.blit(surf, (0, 0))

        sname = self.sprites[self.si]
        stype = (sprite_cfg or {}).get(sname, {}).get("type", "?")
        BADGE = {"item": ((60, 40, 0), (255, 200, 60)), "state": ((20, 20, 80), (140, 160, 255))}
        bg_c, fg_c = BADGE.get(stype, ((40, 40, 40), (200, 200, 200)))
        badge_txt  = font.render(f" {'PLOCKVARA' if stype == 'item' else 'HÄNDELSE'} ", True, fg_c)
        bw, bh     = badge_txt.get_size()
        pygame.draw.rect(screen, bg_c, (8, 8, bw + 4, bh + 4), border_radius=4)
        screen.blit(badge_txt, (10, 10))

        # Visa om detta är en auto-default position (inte ännu manuellt sparad)
        key = (f"{os.path.splitext(self.rooms[self.ri])[0]}"
               f"__{os.path.splitext(sname)[0]}")
        pos_data = load_positions()
        entry = pos_data.get(key, {})
        if entry.get("px") == _SENTINEL_PX:
            note = font.render("⬡ AUTO-DEFAULT — flytta och tryck S för att spara", True, (255, 180, 60))
            screen.blit(note, (10, bh + 18))

        pct_x  = (self.sx + self.sw // 2) / self.rw * 100
        pct_y  = (self.sy + self.sh // 2) / self.rh * 100
        status = (f"  [{stype}] {self.rooms[self.ri]}  +  {sname}"
                  f"   px({self.sx},{self.sy})  {pct_x:.1f}%,{pct_y:.1f}%"
                  f"   skala {self.scale*100:.0f}%   rot {self.rotation}°"
                  f"   +/- storlek   ,/. rotera   ↑↓←→ 1px  Shift=10px   dra   R/P byt   Space=alla   S spara   Esc")
        lbl = font.render(status, True, (200, 200, 200))
        pygame.draw.rect(screen, (20, 20, 20), (0, self.disp_h, WIN_W, PANEL_H))
        screen.blit(lbl, (4, self.disp_h + 7))
        pygame.display.flip()

    def render_all(self, screen: "pygame.Surface", font: "pygame.Font",
                   sprite_cfg: dict | None = None):
        """Visa alla sparade sprites för aktuellt rum på en gång."""
        pos_data  = load_positions()
        room_base = os.path.splitext(self.rooms[self.ri])[0]
        cfg       = sprite_cfg or {}

        result = self.room_img.copy().convert("RGBA")
        count  = 0
        for key, entry in pos_data.items():
            if not key.startswith(room_base + "__"):
                continue
            sprite_name = key[len(room_base) + 2:] + ".png"
            sprite_path = os.path.join(SPRITES_DIR, sprite_name)
            if not os.path.exists(sprite_path):
                continue
            sc  = entry.get("scale", SCALE_DEFAULT)
            rot = entry.get("rotation", 0)
            px  = entry.get("px", _SENTINEL_PX)
            if px == _SENTINEL_PX:
                pct = entry.get("pct", [50.0, 70.0])
                spr_tmp = build_sprite(sprite_name, self.rh, sc)
                sw, sh  = spr_tmp.size
                sx = int(self.rw * pct[0] / 100) - sw // 2
                sy = int(self.rh * pct[1] / 100) - sh // 2
            else:
                sx, sy = px
            spr = build_sprite(sprite_name, self.rh, sc)
            if rot % 360 != 0:
                spr = spr.rotate(-rot, expand=True, resample=Image.BICUBIC)
            result.paste(spr, (sx, sy), spr)
            count += 1

        surf = pil_to_surf(result.convert("RGB"), self.disp_w, self.disp_h)
        screen.fill((0, 0, 0))
        screen.blit(surf, (0, 0))

        n_item  = sum(1 for k in pos_data if k.startswith(room_base + "__")
                      and cfg.get(k[len(room_base)+2:]+".png", {}).get("type") == "item")
        n_state = sum(1 for k in pos_data if k.startswith(room_base + "__")
                      and cfg.get(k[len(room_base)+2:]+".png", {}).get("type") == "state")

        status = (f"  RUMSÖVERSIKT: {self.rooms[self.ri]}"
                  f"   {count} sprites  ({n_item} item, {n_state} state)"
                  f"   Space / valfri tangent = tillbaka till redigering")
        lbl = font.render(status, True, (200, 200, 200))
        pygame.draw.rect(screen, (20, 20, 20), (0, self.disp_h, WIN_W, PANEL_H))
        screen.blit(lbl, (4, self.disp_h + 7))

        badge = font.render(f"  ALLA SPRITES — {self.rooms[self.ri]}  ", True, (255, 255, 200))
        bw, bh = badge.get_size()
        pygame.draw.rect(screen, (60, 40, 10), (8, 8, bw + 4, bh + 4), border_radius=4)
        screen.blit(badge, (10, 10))
        pygame.display.flip()

    def save(self):
        data: dict = load_positions()
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
        save_positions(data)
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

    rooms       = list_pngs(ROOMS_DIR)
    all_sprites = list_pngs(SPRITES_DIR)

    if not rooms:       sys.exit(f"Inga PNG-filer i {ROOMS_DIR}")
    if not all_sprites: sys.exit(f"Inga PNG-filer i {SPRITES_DIR}")

    sprite_cfg = load_sprite_config()

    # Auto-seed standardpositioner vid uppstart
    print("Kontrollerar standardpositioner...")
    seed_all_defaults(all_sprites, sprite_cfg)

    ri = rooms.index(args.room) if args.room in rooms else 0

    # Filtrerad sprite-lista för startrummet
    filtered_sprites = sprites_for_room(rooms[ri], all_sprites, sprite_cfg)
    si = (filtered_sprites.index(args.sprite)
          if args.sprite in filtered_sprites else 0)

    pygame.init()
    screen = pygame.display.set_mode((WIN_W, WIN_H))
    pygame.display.set_caption("Sprite Placer — Drakulas Slott")
    font  = pygame.font.SysFont("monospace", 13)
    clock = pygame.time.Clock()

    MODE_SELECT   = "select"
    MODE_PLACE    = "place"
    MODE_OVERVIEW = "overview"
    mode          = MODE_SELECT
    focus         = 0
    placer: Placer | None = None

    def draw_select():
        selection_screen(screen, font, rooms, filtered_sprites, all_sprites,
                         ri, si, focus, sprite_cfg, load_positions())

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
                        if focus == 0:
                            ri = (ri - 1) % len(rooms)
                            # Uppdatera filtrerad sprite-lista för nytt rum
                            old = filtered_sprites[si] if filtered_sprites else None
                            filtered_sprites[:] = sprites_for_room(rooms[ri], all_sprites, sprite_cfg)
                            si = filtered_sprites.index(old) if old in filtered_sprites else 0
                        else:
                            si = (si - 1) % len(filtered_sprites)

                    elif event.key == pygame.K_DOWN:
                        if focus == 0:
                            ri = (ri + 1) % len(rooms)
                            old = filtered_sprites[si] if filtered_sprites else None
                            filtered_sprites[:] = sprites_for_room(rooms[ri], all_sprites, sprite_cfg)
                            si = filtered_sprites.index(old) if old in filtered_sprites else 0
                        else:
                            si = (si + 1) % len(filtered_sprites)

                    elif event.key == pygame.K_RETURN:
                        placer = Placer(rooms, list(filtered_sprites), ri, si,
                                        all_sprites, sprite_cfg)
                        mode   = MODE_PLACE
                        placer.render(screen, font, sprite_cfg)
                        continue

                    elif event.key in (pygame.K_q, pygame.K_ESCAPE):
                        running = False
                        continue

                    draw_select()

                # ── Översikt ──
                elif mode == MODE_OVERVIEW and placer:
                    mode = MODE_PLACE
                    placer.render(screen, font, sprite_cfg)
                    continue

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
                    elif event.key == pygame.K_SPACE:
                        mode = MODE_OVERVIEW
                        placer.render_all(screen, font, sprite_cfg)
                        continue
                    elif event.key == pygame.K_r:
                        placer.cycle_room(-1 if shift else 1)
                        # Synka tillbaka ri och si samt filtered_sprites
                        ri = placer.ri
                        si = placer.si
                        filtered_sprites[:] = list(placer.sprites)
                    elif event.key == pygame.K_p:
                        placer.cycle_sprite(-1 if shift else 1)
                        si = placer.si
                    elif event.key == pygame.K_s:
                        placer.save(); continue
                    elif event.key == pygame.K_ESCAPE:
                        ri, si = placer.ri, placer.si
                        filtered_sprites[:] = list(placer.sprites)
                        mode = MODE_SELECT
                        draw_select()
                        continue
                    elif event.key in (pygame.K_q,):
                        running = False; continue
                    else:
                        continue
                    placer.render(screen, font, sprite_cfg)

            elif event.type == pygame.MOUSEBUTTONDOWN and mode == MODE_OVERVIEW and placer:
                mode = MODE_PLACE
                placer.render(screen, font, sprite_cfg)

            elif event.type == pygame.MOUSEBUTTONDOWN and mode == MODE_PLACE and placer:
                if event.button == 1:
                    placer.start_drag(*event.pos)
                    placer.render(screen, font, sprite_cfg)

            elif event.type == pygame.MOUSEMOTION and mode == MODE_PLACE and placer:
                if placer.dragging:
                    placer.drag_to(*event.pos)
                    placer.render(screen, font, sprite_cfg)

            elif event.type == pygame.MOUSEBUTTONUP and mode == MODE_PLACE and placer:
                if event.button == 1:
                    placer.stop_drag()

    pygame.quit()


if __name__ == "__main__":
    main()
