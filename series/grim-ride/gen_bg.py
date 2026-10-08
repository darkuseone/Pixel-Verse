"""xAI backgrounds for «Grim Ride» (16:9, grok-imagine-image-2.0 medium 1k, ~$0.06 each). Skips existing files.
  python3 series/grim-ride/gen_bg.py [names...]
Heroes, the e-bike / trike, Kevin the 12-ft skeleton, inflatables, signs, light and particles are drawn in code on top;
backgrounds have no people and no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Detailed HD pixel art game background, modern indie pixel-art adventure game look, crisp visible pixels, rich environmental detail, '
         'American suburb on Halloween night, deep violet night sky with a big full moon and thin clouds, warm orange glow of jack-o-lanterns '
         'and porch lights, cold blue moonlight, wide 16:9 scene. No characters, no people, no animals, no vehicles, no text, no letters, '
         'no numbers, no flags, no symbols; any signs and papers are completely blank. ')
BG = {
    'street': 'Side view of a long empty suburban street running left to right across the lower third of the frame: smooth asphalt with '
              'a sidewalk and a curb, a row of two-story suburban houses with lit windows, lawns covered with Halloween decorations: '
              'carved glowing jack-o-lanterns on porch steps, fake tombstones on the lawns, orange string lights on the roofs, fake '
              'spider webs on the bushes, bare autumn trees with orange leaves, fallen leaves on the road, street lamps, mailboxes, '
              'a full moon above the roofs. Long empty street, plenty of space on the road.',
    'todd_yard': 'Front view of an over-decorated suburban front lawn on Halloween night: a two-story house with garage behind, the roof '
                 'outlined with purple and orange lights, fake fog on the grass, a few fake tombstones, carved jack-o-lanterns on the '
                 'steps, a fake spider web over the garage door, purple spotlights on the lawn, a driveway on the right, a sidewalk '
                 'across the bottom of the frame, a big empty area of lawn in the middle of the frame. Full moon.',
    'porch': 'Front view of the wooden front porch of a small old house on Halloween night: weathered white wooden boards, porch posts, '
             'a warm yellow porch light by the door, a screen door, a doormat, potted dead plants, a single carved jack-o-lantern on the '
             'top step, cobwebs, a wooden floor with empty space in the middle and on the left of the porch for furniture, steps down to '
             'a lawn with fallen leaves in the lower part, a bare tree and the full moon on the right.',
    'gangway': 'A narrow dark gangway alley between two suburban houses at night seen from its open end: wooden fences on both sides, '
               'trash and recycling bins, a garden hose, a broken plastic skeleton decoration leaning on the fence, a single dim motion '
               'light above a side door, puddles on cracked concrete, a strip of violet night sky with the full moon above, fog low on the ground. '
               'Empty concrete path in the middle and lower part of the frame.',
    'hilltop': 'A grassy hilltop at night above a small American suburban town: the town lights and glowing jack-o-lanterns far below '
               'in the valley, a winding road, a single old bare oak tree on the left, a water tower in the distance, a huge full moon low '
               'over the horizon on the right, deep violet sky with stars, fog in the valley. Empty grass and a dirt path in the lower part.',
}

if __name__ == '__main__':
    names = sys.argv[1:] or list(BG)
    for n in names:
        p = OUT / f'{n}.png'
        if p.exists():
            print('skip', p); continue
        xai.generate(STYLE + BG[n], [str(p)], '16:9')
