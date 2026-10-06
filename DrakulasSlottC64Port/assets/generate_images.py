#!/usr/bin/env python3
"""
Genererar alla spelbilder för Drakulas Slott via OpenRouter API.

Kör: python3 generate_images.py --key DIN_API_NYCKEL
     python3 generate_images.py --key DIN_API_NYCKEL --dry-run
     python3 generate_images.py --key DIN_API_NYCKEL --only sprites
"""

import argparse
import base64
import json
import os
import time

API_URL = "https://openrouter.ai/api/v1/images/generations"
MODEL = "google/gemini-2.5-flash-image"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Gäller alla rum — inga föremål, inga figurer, ingen text
NO_TEXT = "no text, no letters, no words, no captions, no titles, no watermarks, no labels"
NO_CHARS = "no people, no characters, no figures, no humans, no skeletons, no monsters, no creatures, empty room"
NO_ITEMS = "no items on display, no objects that can be picked up"

STYLE = (
    f"Commodore 64 pixel art with hand-drawn fantasy illustration style, "
    f"16-color limited palette, chunky expressive pixels with visible brushstroke texture, "
    f"gothic dark atmosphere, warm candlelight and cold moonlight contrasts, "
    f"style of classic Sierra On-Line adventure games meets fantasy ink sketch, "
    f"rough organic pixel edges, not sterile — feels hand-crafted and alive. "
    f"{NO_TEXT}, {NO_CHARS}"
)
SPRITE_STYLE = (
    f"Commodore 64 pixel art with hand-drawn fantasy illustration style, "
    f"16-color limited palette, chunky expressive pixels, isolated object centered on solid black background, "
    f"classic adventure game item icon, organic and hand-crafted feel. "
    f"{NO_TEXT}"
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
     1536, 1024, "special"),

    ("special/ending_win.png",
     f"Gothic horror victory scene inside a dark vampire crypt. "
     f"Open wooden coffin in center, pale defeated vampire inside with sharp wooden stake through chest, "
     f"eyes closed, arms crossed. Dawn light piercing from above, dust particles in air, "
     f"extinguished candles, sense of triumph. Dark purple and gold atmosphere. {STYLE}",
     1536, 1024, "special"),

    ("special/ending_lose.png",
     f"Gothic horror game over scene. Tall pale vampire in black cape looming large, "
     f"filling the frame, red glowing eyes, fangs bared, arms outstretched reaching toward viewer. "
     f"Dark castle corridor behind vampire, torchlight creating menacing silhouette from below. "
     f"Extreme close-up from below angle. Deep red and black atmosphere, final, terrifying. {STYLE}",
     1536, 1024, "special"),

    # --- Rumbilder (tomma rum — inga plockvara-föremål, inga figurer) ---
    ("rooms/01_hallen.png",
     f"Gothic castle entrance hall interior. Stone floor with cracked tiles, tall arched doorway "
     f"with stone pillars. Cobwebs in corners. Dark blue-purple atmosphere, "
     f"orange torchlight from off-screen. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/02_lasrummet.png",
     f"Gothic castle reading room. Large empty brick fireplace dominating the back wall, cold and dark, no fire. "
     f"Armchair to one side, ancient bookshelves lining the walls. "
     f"Cold dim atmosphere, only ambient light. The fireplace is clearly unlit and empty. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/03_biblioteket.png",
     f"Gothic castle library interior. Floor-to-ceiling bookshelves packed with ancient leather-bound books. "
     f"Reading table in foreground, empty surface. "
     f"Dusty, dark, candlelight, stone walls between shelves. Deep blue-purple shadows. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/04_vapen_kammaren.png",
     f"Gothic castle armory interior. Stone walls covered with mounted weapons: swords, shields, spears on racks. "
     f"Empty weapon stand in center-foreground. "
     f"Suit of armor in corner, crossed swords on wall. Dark cold atmosphere, dim torchlight. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/05_tornet.png",
     f"Gothic castle tower interior. Circular stone tower room, spiral staircase on curved walls. "
     f"Tall narrow window showing night sky with full moon. Stone balcony ledge through large arched opening. "
     f"Cold blue moonlight, dark stone, empty floor. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/06_lagre_tornet.png",
     f"Gothic castle lower tower storage room. Low-ceilinged stone room at base of tower. "
     f"Empty stone walls, damp moss between stones, small barred window near ceiling. "
     f"Cold blue-grey atmosphere, barely lit. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/07_kapellet.png",
     f"Gothic castle chapel interior. Stone chapel with vaulted ceiling, tall narrow stained glass windows "
     f"in purple and blue. Stone altar at back with crucifix, empty altar surface. Rows of pews. "
     f"Cool purple-blue light through stained glass. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/08_eldstaden_av_tegel.png",
     f"Gothic castle room with massive ornate brick fireplace structure filling the entire back wall, intact and whole. "
     f"Lit torch in iron wall bracket to the side. Heavy stone floor, dark atmosphere. "
     f"Red and brown brick details, orange torchlight. The fireplace opening is empty and dark. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/09_den_gomda_korridoren.png",
     f"Gothic castle hidden corridor, narrow secret passageway behind a wall panel. "
     f"Stone walls close on both sides, empty floor. "
     f"Very dark, cobwebs everywhere, barely lit, mysterious. Deep shadows. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/10_den_hemliga_passagen.png",
     f"Gothic castle secret underground passage. Low tunnel carved through rock, rough uneven ceiling. "
     f"Dripping water, puddles reflecting dim light. Passage curves into darkness ahead. "
     f"Claustrophobic, damp, mysterious. Empty corridor. {STYLE}",
     1536, 1024, "rooms"),

    # Sjön: två olika vyer (slottssidan och kapellsidan) — båten är sprite
    ("rooms/11_sjo_slott.png",
     f"Gothic underground lake cavern viewed from the castle shore. Vast cave, still black lake stretching forward. "
     f"Rocky stone shore in foreground with an iron ring bolted to the rock. "
     f"Stalactites from cavern ceiling. Phosphorescent blue water glow, passage visible on far shore. "
     f"Eerie, vast, silent. Empty shore, no boat. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/11_sjo_kapell.png",
     f"Gothic underground lake cavern viewed from the chapel shore, opposite side. "
     f"Same vast underground lake but viewed from a different rocky shore. "
     f"Stone steps cut into the rock leading up from the water. "
     f"Stalactites, blue phosphorescent water glow, passage behind viewer implied. "
     f"Eerie, vast, silent. Empty shore. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/12_en_bat.png",
     f"View from inside a small empty wooden rowboat on a dark underground lake. "
     f"Empty oarlocks, no oars present. Looking forward across still black water. "
     f"Stone cavern walls and ceiling on both sides, darkness ahead with faint glow. "
     f"Claustrophobic, blue-black water. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/13_alkemistens_laboratorium.png",
     f"Gothic alchemist's laboratory, cluttered stone room with wooden worktable covered in glass flasks, "
     f"bubbling potions, open books. Distillation equipment, colored liquids in fixed flasks, skull on shelf. "
     f"Shelves of mysterious bottles on walls. Green and yellow chemical glow. "
     f"No loose portable items on the table. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/14_forvarings_rummet.png",
     f"Gothic castle storage room filled with old barrels and stacked crates against walls. "
     f"Open floor space in center. Dusty, cluttered, dim light from crack in ceiling. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/15_takskagget.png",
     f"Gothic castle rooftop ledge at night, narrow battlement with low stone parapet. "
     f"Night sky with full moon, bats silhouetted. Empty stone ledge. "
     f"Wind-swept, cold, dangerous height, stone gargoyle in corner. Dark blue night sky, moonlight on grey stone. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/16_galleriet.png",
     f"Gothic castle portrait gallery. Long hall with stone floor, tall walls hung with large painting frames. "
     f"Large empty hooks high on one wall where something large once hung. "
     f"Old paintings of stern faces in gilded frames. Dim candelabra light. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/17_sido_rummet.png",
     f"Gothic castle side room with heavy rusted iron door in far wall, clearly locked. "
     f"Old corroded door with large iron hinges and visible keyhole. "
     f"Dark and unwelcoming, torch on wall casting orange light on rusty door. Empty room. {STYLE}",
     1536, 1024, "rooms"),

    ("rooms/18_wampyrernas_grav.png",
     f"Gothic vampire crypt interior. Underground crypt with vaulted stone ceiling, stone sarcophagi on walls. "
     f"Center: large ornate wooden coffin CLOSED with iron clasps, lid shut. Candles on stone ledges, dripping wax. "
     f"Cobwebs, bat hanging from ceiling. Extremely dark, ominous, purple-black shadows. {STYLE}",
     1536, 1024, "rooms"),

    # --- Plockvara-sprites (föremål spelaren kan ta) ---
    ("sprites/slagga.png",
     f"Heavy sledgehammer, large grey metal hammerhead on long brown wooden handle. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/klocka.png",
     f"Antique grandfather clock, tall dark wood case, round clock face, pendulum visible through glass panel. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/rep.png",
     f"Coiled hemp rope, thick brown rope neatly coiled in a circle. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/pergament_rulle.png",
     f"Rolled parchment scroll with wooden end-caps, yellowed aged paper, slightly unrolled. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/yxa.png",
     f"Medieval battle axe, large single-blade grey metal axe head on dark wood handle. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/aror.png",
     f"Two wooden rowing oars crossed in an X shape, light brown wood, flat paddle ends. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/nyckel.png",
     f"Large old iron skeleton key, ornate round handle, single notch, dark grey slightly rusty metal. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/heligt_vatten.png",
     f"Small glass holy water vial with cork stopper, glowing blue water inside, tiny cross on label. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/olje_flaska.png",
     f"Round-bottomed glass flask with narrow neck, amber brown oil inside. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/lada.png",
     f"Square wooden crate with visible planks and iron corner brackets. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/hink.png",
     f"Simple cylindrical metal bucket with arc handle at top, grey metal, slightly dented. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/fackla.png",
     f"Lit torch, wooden stick with burning orange and yellow flame at top. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/spikar.png",
     f"Cluster of large iron nails, dark grey metal, scattered or bundled together. "
     f"Isolated object centered in frame. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    # --- Tillstånds-sprites (läggs ovanpå rumsbilder vid spelhandelse) ---
    ("sprites/eld_kamin.png",
     f"Roaring fire burning in a fireplace opening, bright orange and yellow flames, "
     f"glowing embers at the base, heat shimmer. Transparent-edge sprite for compositing. "
     f"Isolated on black background. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/aska.png",
     f"Cold pile of grey ash and embers in a fireplace, no fire, scattered charred wood chunks. "
     f"Pale grey and black ash. Isolated on black background. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/eldstad_sonderslagen.png",
     f"Smashed brick fireplace opening — broken bricks and rubble piled at base, "
     f"dark jagged hole in the wall where the fireplace back was, secret passage darkness beyond. "
     f"Isolated on black background. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/dörr_öppen.png",
     f"Heavy rusted iron door standing open, swung wide on large iron hinges, "
     f"darkness visible through the doorway. Door edge and frame only, no surrounding wall. "
     f"Isolated on black background. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/vampyr_i_kista.png",
     f"Interior of an open wooden coffin lid thrown back, pale vampire lying inside — "
     f"black cape, white face, hands crossed on chest, eyes closed, sleeping or dead. "
     f"Coffin interior only, dramatic candle-lit top-down view. Isolated on black background. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/gobelas_fallen.png",
     f"Large heavy woven tapestry/gobelin crumpled on a stone floor — thick fabric in a heap, "
     f"loose iron nails scattered around it. Isolated on black background. {SPRITE_STYLE}",
     1024, 1024, "sprites"),

    ("sprites/ekan_vid_strand.png",
     f"Small wooden rowboat moored at a rocky stone shore, rope tied to an iron ring. "
     f"Boat from above-and-side angle, oarlocks visible, rope taut. "
     f"Isolated on black background. {SPRITE_STYLE}",
     1024, 1024, "sprites"),
]


def generate_and_save(api_key: str, prompt: str, width: int, height: int, dest: str) -> None:
    """Anropar OpenRouter, får base64-PNG, sparar till disk."""
    import subprocess
    size_str = f"{width}x{height}"
    payload = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "n": 1,
        "size": size_str,
    })
    result = subprocess.run(
        [
            "curl", "-s", "-X", "POST", API_URL,
            "-H", f"Authorization: Bearer {api_key}",
            "-H", "Content-Type: application/json",
            "-d", payload,
        ],
        capture_output=True, text=True, timeout=120,
    )
    data = json.loads(result.stdout)
    if "error" in data:
        raise RuntimeError(data["error"].get("message", str(data["error"]))[:200])

    item = data["data"][0]
    os.makedirs(os.path.dirname(dest), exist_ok=True)

    if "b64_json" in item:
        with open(dest, "wb") as f:
            f.write(base64.b64decode(item["b64_json"]))
    elif "url" in item:
        subprocess.run(["curl", "-s", "-o", dest, item["url"]], check=True, timeout=60)
    else:
        raise RuntimeError(f"Okänt responsformat: {list(item.keys())}")


def main():
    parser = argparse.ArgumentParser(description="Generera spelbilder via OpenRouter")
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
            generate_and_save(args.key, prompt, width, height, dest)
            print("✓")
        except Exception as e:
            print(f"FEL: {e}")

        if i < len(todo):
            time.sleep(args.delay)

    print(f"\nKlart. Bilder sparade i {BASE_DIR}/")


if __name__ == "__main__":
    main()
