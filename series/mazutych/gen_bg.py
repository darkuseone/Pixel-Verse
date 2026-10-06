"""xAI backgrounds for «Мазутыч» (16:9, grok-imagine-image-2.0 medium 1k, ~$0.04-0.06 each). Skips existing files.
  python3 series/mazutych/gen_bg.py [names...]
Heroes, cars, the tanker truck, signs, the plan banner, light and particles are drawn in code on top; backgrounds have no people and no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Detailed HD pixel art game background, modern indie pixel-art adventure game look, crisp visible pixels, rich environmental detail, '
         'post-Soviet provincial town, late autumn golden-hour dusk, purple-orange sky, wide 16:9 scene. No characters, no people, no animals, '
         'no vehicles, no text, no letters, no numbers, no flags, no symbols; any signs, boards, banners and papers are completely blank. ')
BG = {
    'highway_azs': 'Side view of a cracked two-lane provincial highway running left to right across the lower third of the frame, with puddles '
                   'and potholes. On the right side a small shabby gas station: a flat canopy on thin poles with two old fuel pumps, a small '
                   'white-and-blue cashier kiosk, a tall blank price board on a pole. Behind the road: a dry yellow field with birch trees and '
                   'leaning power-line poles, grey nine-storey Soviet panel apartment blocks on the horizon on the left, and far away on the '
                   'horizon in the middle a big oil refinery with distillation columns, tanks and a very tall flare stack burning a bright flame. '
                   'Long empty road, sky with long glowing clouds.',
    'refinery_gate': 'Front view of the main entrance of an old Soviet-era oil refinery: a wide sliding steel gate in the centre bottom, '
                     'a small brick checkpoint booth with a lit window and a turnstile on the left, a tall concrete fence with barbed wire, '
                     'a huge empty blank billboard frame mounted high above the gate, behind it a maze of pipes, distillation columns, spherical '
                     'tanks and steam, and a very tall flare stack on the right burning a huge bright orange flame. Orange sodium lamps, '
                     'wide empty cracked asphalt in front of the gate in the lower third.',
    'azs_window': 'Close-up front view of the cashier window of a shabby small-town gas station kiosk at dusk: a big glass window in the centre '
                  'with a metal speaking grille and a small cash tray slot at the bottom, the frame painted white and blue with peeling paint, '
                  'a few blank faded stickers on the glass, inside a warm-lit cramped room with shelves of snacks, a coffee machine, a small TV '
                  'and a calendar (blank); the area just behind the glass in the middle is empty where a cashier would sit; a dusty ledge '
                  'in the foreground.',
    'garages': 'Night in a Soviet garage cooperative: a long row of old metal garages with rusty swing doors, side view running left to '
               'right, a single weak street lamp, a muddy dirt alley with puddles in the lower third, tires stacked, an old fridge, '
               'graffiti-free walls with blank paper notices, power lines, panel apartment blocks dark on the horizon, the distant refinery '
               'flare glowing orange in the sky, deep purple night sky. Empty alley.',
    'garage_inside': 'Interior of a cramped Soviet garage workshop at night, front view: concrete walls with shelves of jars, tools hanging '
                     'on a pegboard, a bare bulb, an old workbench on the left, sacks and buckets on the floor, a calendar (blank), an '
                     'inspection pit in the floor, the closed double garage doors at the back, warm yellow light and deep shadows, empty '
                     'space in the middle of the floor.',
    'assembly_hall': 'A Soviet-era factory assembly hall interior: a wooden stage with red velvet curtains and a podium, a long blank '
                     'banner above the stage, rows of wooden seats in the foreground seen from behind, wall-mounted lamps, a bust pedestal '
                     'without any statue, a framed blank honor board, warm stage lights and dust in the air, empty stage floor.',
}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    total = 0.0
    for n in names:
        p = OUT / f'{n}.png'
        if p.exists():
            continue
        total += xai.generate(STYLE + BG[n], [str(p)], aspect='16:9')
    print('total $%.3f' % total)
