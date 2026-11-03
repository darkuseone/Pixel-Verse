"""xAI backgrounds for «Aura Dad» (16:9 1280x720, grok-imagine-image-2.0 medium 1k, ~$0.06 each). Skips existing files.
  python3 series/aura-dad/gen_bg.py [names...]
Heroes, MIRRA's face, phone screens, signs, light and particles are drawn in code; backgrounds have no people, no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Detailed HD pixel art game background, bright cheerful American suburban sitcom look, modern indie pixel-art adventure game '
         'style, crisp visible pixels, rich environmental detail, saturated warm desert colours with lavender and aqua accents, Arizona '
         'suburb, wide 16:9 scene, front view, eye level. No characters, no people, no animals, no text, no letters, no numbers, no '
         'symbols; any signs, labels, calendars, posters, screens and papers are completely blank. ')
BG = {
    'kitchen': 'A sunny open-plan kitchen of a beige stucco suburban house in Phoenix, Arizona, morning. Back wall: white shaker cabinets, '
               'a stainless steel double-door fridge on the left, a big window in the centre with a view of a desert backyard with a tall '
               'saguaro cactus, gravel, a pool fence and bright blue sky; a coffee maker and a fruit bowl on the counter; a blank framed '
               'wooden sign on the wall; a wall clock; pendant lamps. In the foreground right a light wood breakfast table with two chairs '
               'and a coffee mug; terracotta tile floor. The middle of the floor is clear empty space.',
    'bathroom': 'A suburban master bathroom in Arizona, bright morning light. In the exact centre of the back wall above a white double '
                'vanity sink with a quartz top: one large oval mirror with a thin brushed metal frame, the mirror glass is plain soft '
                'grey-blue with a gentle diagonal shine and reflects nothing. Around it: lavender painted walls, white subway tiles, two wall '
                'sconces, a small window with frosted glass on the right, a towel ring with a fluffy aqua towel, a succulent in a pot, '
                'toothbrush cup, soap dispenser, a bath mat on light grey tile floor. The space in front of the sink is clear.',
}


def main(names):
    for n in names or BG:
        out = OUT / f'{n}.png'
        if out.exists(): print('skip', out); continue
        xai.generate(STYLE + BG[n], [str(out)], aspect='16:9')
        print('ok', out)


if __name__ == '__main__':
    main(sys.argv[1:])
