#!/usr/bin/env python3
"""
Genererar alla spelbilder för Drakulas Slott via 1min.ai API.

Kör: python3 generate_images.py --key DIN_API_NYCKEL
     python3 generate_images.py --key DIN_API_NYCKEL --dry-run  (visa vad som skulle genereras)
     python3 generate_images.py --key DIN_API_NYCKEL --only sprites
"""

import argparse
import json
import os
import sys
import time
import urllib.request

API_URL = "https://api.1min.ai/api/features"
MODEL = "black-forest-labs/flux-pro"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STYLE = (
    "Commodore 64 pixel art, limited 16-color palette, hard pixel edges, "
    "no anti-aliasing, retro 1980s video game art style, gothic dark atmosphere"
)
SPRITE_STYLE = (
    "Commodore 64 pixel art, 16-color limited palette, hard pixel edges, "
    "no anti-aliasing, retro 8-bit game sprite, isolated object, solid black background"
)

# ── Bilder ────────────────────────────────────────────────────────────────────
# (output_relpath, prompt, width, height, category)

IMAGES = [
    # --- Specialbilder ---
    ("special/intro.png",
     f"Gothic horror title screen for a Commodore 64 text adventure. "
     f"Dramatic castle silhouette against full moon, stormy purple-black sky, lightning bolt, "
     f"bats around tower, dead trees in foreground. "
     f"Large blocky retro text 'DRAKULAS SLOTT' at the bottom. "
     f"Iconic 1980s horror game title screen energy. {STYLE}",
     1280, 800, "special"),

    ("special/ending_win.png",
     f"Gothic horror victory scene inside a dark vampire crypt. "
     f"Open wooden coffin in center, pale defeated vampire inside with sharp wooden stake through chest, "
     f"eyes closed, arms crossed. Dawn light piercing from above, dust particles in air, "
     f"extinguished candles, sense of triumph. Dark purple and gold atmosphere. {STYLE}",
     1280, 800, "special"),

    ("special/ending_lose.png",
     f"Gothic horror game over scene. Tall pale vampire in black cape looming large, "
     f"filling the frame, red glowing eyes, fangs bared, arms outstretched reaching toward viewer. "
     f"Dark castle corridor behind vampire, torchlight creating menacing silhouette from below. "
     f"Extreme close-up from below angle. Deep red and black atmosphere, final, terrifying. {STYLE}",
     1280, 800, "special"),

    # --- Rumbilder ---
    ("rooms/01_hallen.png",
     f"Gothic castle entrance hall interior. Stone floor with cracked tiles, tall arched doorway "
     f"with stone pillars. Large antique grandfather clock against the wall, dark wood, tall. "
     f"Old wooden sign near entrance. Cobwebs in corners. Dark blue-purple atmosphere, "
     f"orange torchlight from off-screen. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/02_lasrummet.png",
     f"Gothic castle reading room, roaring fire in large brick fireplace dominating the back wall. "
     f"Warm orange and yellow flames, dark stone surround. Armchair silhouette to one side. "
     f"Flickering firelight on dark stone walls, books in shadows. Fire is the only light source. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/02_lasrummet_a.png",
     f"Gothic castle reading room, large roaring fire in brick fireplace, clearly impassable wall of flame. "
     f"Warm orange glow fills the room, fire is dominant light source. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/02_lasrummet_b.png",
     f"Gothic castle reading room, fireplace now cold and dark, pile of grey ash where fire was. "
     f"Dark opening visible in back of the cold hearth - a secret passage through the fireplace. "
     f"Cold blue-grey atmosphere, dim ambient light, ominous dark opening. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/03_biblioteket.png",
     f"Gothic castle library interior. Floor-to-ceiling bookshelves packed with ancient leather-bound books. "
     f"Large wooden bookshelf unit dominates the scene. Rolled scroll on reading table in foreground. "
     f"Dusty, dark, candlelight, stone walls between shelves. Deep blue-purple shadows. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/04_vapen_kammaren.png",
     f"Gothic castle armory interior. Stone walls covered with mounted weapons: swords, shields, spears. "
     f"Large battle axe prominently displayed on wooden stand in center-foreground. "
     f"Suit of armor in corner, crossed swords on wall. Dark cold atmosphere, dim torchlight. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/05_tornet.png",
     f"Gothic castle tower interior. Circular stone tower room, spiral staircase on curved walls. "
     f"Tall narrow window showing night sky with full moon. Stone balcony ledge through large arched opening. "
     f"Heavy sledgehammer leaning against wall. Cold blue moonlight, dark stone. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/06_lagre_tornet.png",
     f"Gothic castle lower tower storage room. Low-ceilinged stone room at base of tower. "
     f"Pair of wooden oars propped against stone wall. Damp walls, moss between stones, "
     f"small barred window near ceiling. Cold blue-grey atmosphere, barely lit. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/07_kapellet.png",
     f"Gothic castle chapel interior. Stone chapel with vaulted ceiling, tall narrow stained glass windows "
     f"in purple and blue. Stone altar at back with crucifix. On the altar: ornate iron key and small "
     f"glass vial of holy water. Rows of pews. Cool purple-blue light through stained glass. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/08_eldstaden_av_tegel.png",
     f"Gothic castle room with massive ornate brick fireplace structure on entire back wall, currently unlit. "
     f"Lit torch in iron wall bracket to the side. Heavy stone floor, dark atmosphere, only torch for light. "
     f"Red and brown brick details, orange torchlight. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/08_eldstaden_av_tegel_a.png",
     f"Gothic castle room with massive intact ornate brick fireplace, imposing stone wall, cold and dark. "
     f"Lit torch on wall. Heavy stone floor. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/08_eldstaden_av_tegel_b.png",
     f"Gothic castle room, massive brick fireplace smashed open with a sledgehammer. "
     f"Bricks scattered on stone floor, dark opening in wall where fireplace stood revealing secret passage beyond. "
     f"Rubble and broken bricks, dust in the air, darkness in the opening. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/09_den_gomda_korridoren.png",
     f"Gothic castle hidden corridor, narrow secret passageway behind a wall panel. "
     f"Stone walls close on both sides. Coil of rope lying on damp stone floor. "
     f"Very dark, cobwebs everywhere, barely lit, mysterious. Deep shadows. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/10_den_hemliga_passagen.png",
     f"Gothic castle secret underground passage. Low tunnel carved through rock, rough uneven ceiling. "
     f"Dripping water, puddles reflecting dim light. Passage curves into darkness ahead. "
     f"Claustrophobic, damp, mysterious. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/11_underjordisk_sjo.png",
     f"Gothic underground lake cavern. Vast cave with still black lake in foreground. "
     f"Rocky stone shore along bottom edge. Small wooden rowboat moored at shore, rope tied to iron ring. "
     f"Stalactites from cavern ceiling. Mysterious phosphorescent blue glow from water. Eerie, vast, silent. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/11_underjordisk_sjo_a.png",
     f"Gothic underground lake cavern with small wooden rowboat moored at stone shore, "
     f"rope tied to iron ring in the rock. Still black lake, stalactites, blue phosphorescent water glow. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/11_underjordisk_sjo_b.png",
     f"Gothic underground lake cavern, no boat present. Empty stone shore, empty iron ring where boat was tied. "
     f"Ripples on dark water, small boat barely visible far away in darkness. Eerie, vast, silent. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/12_en_bat.png",
     f"View from inside small wooden rowboat on dark underground lake with oars ready. "
     f"Looking forward across still black water. Stone cavern walls and ceiling on both sides. "
     f"Darkness ahead with faint glow. Ripples around boat. Claustrophobic, blue-black water. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/12_en_bat_a.png",
     f"View from inside small wooden rowboat on dark underground lake, oarlocks empty, no oars. "
     f"Boat drifts motionless. Dark water surrounds, cave walls visible. Stranded feeling, cold dark water. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/12_en_bat_b.png",
     f"View from inside small wooden rowboat on dark underground lake, pair of wooden oars in oarlocks ready to use. "
     f"Boat faces across the dark water, faint glow ahead indicating far shore. Purposeful, forward-looking. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/13_alkemistens_laboratorium.png",
     f"Gothic alchemist's laboratory, cluttered stone room with wooden worktable covered in glass flasks, "
     f"bubbling potions, books. Distinctive oil flask prominently on table. Distillation equipment, smoke, "
     f"colored liquids, skull on shelf. Shelves of mysterious bottles. Green and yellow chemical glow. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/14_forvarings_rummet.png",
     f"Gothic castle storage room filled with old wooden boxes, barrels, crates stacked against walls. "
     f"Large wooden crate and metal bucket prominently in foreground. Dusty, cluttered, dim light from crack in ceiling. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/14_forvarings_rummet_a.png",
     f"Gothic castle storage room, intact large wooden crate prominently in foreground, metal bucket nearby. "
     f"Dusty, cluttered, dim light. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/14_forvarings_rummet_b.png",
     f"Gothic castle storage room, wooden crate smashed open. Pile of sharp pointed wooden stakes and splintered planks "
     f"scattered on stone floor where the box was. Jagged pointed wooden stakes clearly visible. Rest of room unchanged. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/15_takskagget.png",
     f"Gothic castle rooftop ledge at night, narrow battlement with low stone parapet. "
     f"Night sky with full moon, bats silhouetted. Small cluster of iron nails and hook on stone ledge. "
     f"Wind-swept, cold, dangerous height, stone gargoyle in corner. Dark blue night sky, moonlight on grey stone. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/16_galleriet.png",
     f"Gothic castle portrait gallery. Long hall with stone floor, tall walls hung with large painting frames. "
     f"Large decorative tapestry/gobelin nailed to ceiling and hanging dramatically on one wall. "
     f"Old paintings of stern faces in gilded frames. Dim candelabra light. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/16_galleriet_a.png",
     f"Gothic castle gallery, large tapestry nailed to ceiling and hanging from it, imposing and decorative. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/16_galleriet_b.png",
     f"Gothic castle gallery, large tapestry crashed to stone floor - crumpled heap of heavy woven fabric. "
     f"Iron nails scattered on floor, empty hooks on ceiling. Dust in air from the fall. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/17_sido_rummet.png",
     f"Gothic castle side room with heavy rusted iron door in far wall, clearly locked. "
     f"Old corroded door with large iron hinges and visible keyhole. Chains near door. "
     f"Dark and unwelcoming, torch on wall casting orange light on rusty door. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/17_sido_rummet_a.png",
     f"Gothic castle side room with heavy rusted iron door, clearly locked and impassable. "
     f"Old corroded iron hinges, visible keyhole, torch on wall. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/17_sido_rummet_b.png",
     f"Gothic castle side room, heavy iron door now open and swinging ajar on creaking hinges. "
     f"Beyond the doorway: darkness, stairs descending into unknown. Door is oiled, hinges no longer rusty. "
     f"Key on floor nearby. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/18_wampyrernas_grav.png",
     f"Gothic vampire crypt interior. Underground crypt with vaulted stone ceiling, stone sarcophagi on walls. "
     f"Center: large ornate wooden coffin closed with iron clasps. Candles on stone ledges, dripping wax. "
     f"Cobwebs, bat hanging from ceiling. Extremely dark, ominous, purple-black shadows. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/18_wampyrernas_grav_a.png",
     f"Gothic vampire crypt, large ornate wooden coffin shut with iron clasps. Candles, cobwebs, stone sarcophagi. "
     f"Ominous, purple-black shadows. {STYLE}",
     1280, 800, "rooms"),

    ("rooms/18_wampyrernas_grav_b.png",
     f"Gothic vampire crypt, ornate coffin lid thrown open revealing pale vampire inside, black cape, "
     f"eyes closed, hands crossed on chest, still as death. Extremely pale, fangs just visible. "
     f"Red-purple atmosphere, cold candlelight, ominous. {STYLE}",
     1280, 800, "rooms"),

    # --- Sprites ---
    ("sprites/slagga.png",
     f"Heavy sledgehammer, large grey metal hammerhead on long brown wooden handle. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     384, 384, "sprites"),

    ("sprites/klocka.png",
     f"Antique grandfather clock, tall dark wood case, round clock face, pendulum visible through glass panel. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     384, 384, "sprites"),

    ("sprites/rep.png",
     f"Coiled hemp rope, thick brown rope neatly coiled in a circle. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     384, 384, "sprites"),

    ("sprites/pergament_rulle.png",
     f"Rolled parchment scroll with wooden end-caps, yellowed aged paper, slightly unrolled. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     384, 384, "sprites"),

    ("sprites/yxa.png",
     f"Medieval battle axe, large single-blade grey metal axe head on dark wood handle. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     384, 384, "sprites"),

    ("sprites/aror.png",
     f"Two wooden rowing oars crossed in an X shape, light brown wood, flat paddle ends. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     384, 384, "sprites"),

    ("sprites/nyckel.png",
     f"Large old iron skeleton key, ornate round handle, single notch, dark grey slightly rusty metal. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     384, 384, "sprites"),

    ("sprites/heligt_vatten.png",
     f"Small glass holy water vial with cork stopper, glowing blue water inside, tiny cross on label. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     384, 384, "sprites"),

    ("sprites/olje_flaska.png",
     f"Round-bottomed glass flask with narrow neck, amber brown oil inside. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     384, 384, "sprites"),

    ("sprites/lada.png",
     f"Square wooden crate with visible planks and iron corner brackets. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     384, 384, "sprites"),

    ("sprites/hink.png",
     f"Simple cylindrical metal bucket with arc handle at top, grey metal, slightly dented. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     384, 384, "sprites"),

    ("sprites/fackla.png",
     f"Lit torch, wooden stick with burning orange and yellow flame at top. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     384, 384, "sprites"),

    ("sprites/spikar.png",
     f"Cluster of large iron nails, dark grey metal, scattered or bundled together. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     384, 384, "sprites"),
]


def generate_image(api_key: str, prompt: str, width: int, height: int) -> str:
    """Anropar 1min.ai och returnerar URL till genererad bild."""
    payload = json.dumps({
        "type": "IMAGE_GENERATOR",
        "model": MODEL,
        "promptObject": {
            "prompt": prompt,
            "width": width,
            "height": height,
            "output_format": "png",
            "output_quality": 90,
            "steps": 30,
        }
    }).encode()

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "API-KEY": api_key,
            "Content-Type": "application/json",
        },
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read())

    return data["aiRecord"]["temporaryUrl"]


def download(url: str, dest: str) -> None:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    urllib.request.urlretrieve(url, dest)


def main():
    parser = argparse.ArgumentParser(description="Generera spelbilder via 1min.ai")
    parser.add_argument("--key", required=True, help="1min.ai API-nyckel")
    parser.add_argument("--dry-run", action="store_true", help="Visa vad som skulle genereras")
    parser.add_argument("--only", choices=["rooms", "sprites", "special"], help="Generera bara en kategori")
    parser.add_argument("--delay", type=float, default=3.0, help="Sekunder mellan anrop (default: 3)")
    args = parser.parse_args()

    images = [img for img in IMAGES if not args.only or img[4] == args.only]
    todo = [img for img in images if not os.path.exists(os.path.join(BASE_DIR, img[0]))]
    done = len(images) - len(todo)

    print(f"Totalt: {len(images)} bilder  |  Redan klara: {done}  |  Att generera: {len(todo)}")

    if args.dry_run:
        for path, prompt, w, h, cat in todo:
            print(f"  [{cat}] {path}  ({w}×{h})")
        return

    for i, (rel_path, prompt, width, height, cat) in enumerate(todo, 1):
        dest = os.path.join(BASE_DIR, rel_path)
        print(f"[{i}/{len(todo)}] {rel_path} ...", end=" ", flush=True)
        try:
            url = generate_image(args.key, prompt, width, height)
            download(url, dest)
            print("✓")
        except Exception as e:
            print(f"FEL: {e}")

        if i < len(todo):
            time.sleep(args.delay)

    print(f"\nKlart. Bilder sparade i {BASE_DIR}/")


if __name__ == "__main__":
    main()
