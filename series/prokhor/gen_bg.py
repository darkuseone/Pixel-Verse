"""xAI backgrounds for «Прохор. Таёжные лайфхаки» (16:9, grok-imagine-image-2.0 medium 1k, ~$0.06 each). Skips existing files.
  python3 series/prokhor/gen_bg.py [names...]
Heroes, signs, the meter, the bill, light and particles are drawn in code on top; backgrounds have no people, no animals and no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Detailed HD pixel art game background, modern indie pixel-art adventure game look, crisp visible pixels, rich environmental detail, '
         'Siberian taiga in deep winter, low orange winter sun, long blue shadows on the snow, wide 16:9 scene. No characters, no people, '
         'no animals, no text, no letters, no numbers, no flags, no symbols; any signs, boards, papers and labels are completely blank. ')
BG = {
    'izba': 'Interior of a tiny old Russian log cabin (izba) frozen inside: front view, log walls covered with white hoarfrost, icicles hanging '
            'from the ceiling beams, a big white Russian clay stove on the left with a small black iron fire door at waist height (cold, no fire), '
            'a wooden table in the middle with a brass samovar, a patterned red carpet hanging on the right wall, a small frosted window with '
            'low orange sun light, shelves with pickle jars, felt boots drying on the stove ledge, an old radio, a tear-off calendar (blank), '
            'a blank framed certificate on the wall. Empty floor space in the middle foreground. Cold blue-violet light with warm sun rays.',
    'taiga': 'Side view of a snowy taiga clearing: on the left a small dark log cabin with a snow-covered roof and a wooden door; in the middle '
             'a big rounded snow mound with a dark cave entrance hole at its base, roots and a little steam rising from a vent hole on top '
             '(a bear den); on the right one very tall pine tree; dense dark spruce forest behind; deep fresh snow with footprints in the lower '
             'third of the frame; a wooden mailbox on a post; low orange winter sun near the horizon, pink-violet sky, sparkling snow.',
    'den': 'Interior of a cozy bear den under the snow: a rounded earthen cave seen from the front, walls of packed earth and hanging tree roots, '
           'a thick bed of dry grass, moss and old blankets on the floor in the centre, a small ventilation hole in the ceiling with a beam of '
           'cold blue light, a few icicles at the entrance on the left, warm brown and amber tones, soft dusty air. Empty bed in the centre '
           'where a big sleeping animal would lie.',
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
