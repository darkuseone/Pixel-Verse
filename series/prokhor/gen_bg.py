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

# v2 (owner 12.10.2026: «более качественный задний фон, арт-дизайн», less noisy): clean cartoon pixel art, bold shapes, big readable masses
STYLE2 = ('Clean stylized 16-bit cartoon pixel art game background, bold readable shapes, big simple masses, limited soft palette, smooth '
          'pixel gradients, uncluttered, cozy and charming, like a modern indie pixel adventure game, Siberian taiga in deep winter, '
          'low orange winter sun, long blue shadows, wide 16:9 scene. No characters, no people, no animals, no text, no letters, no numbers; '
          'any signs and boards are blank. ')
BG2 = {
    'taiga2': 'Side view of a wide snowy taiga clearing. On the far left a small cozy log cabin with a snowy roof, a lit window and a wooden '
              'porch. In the center-right a huge rounded snow-covered mound with a LARGE dark cave entrance at ground level (the entrance is '
              'about a third of the image height and wide), thick roots around the entrance, a thin steam plume rising from a vent on top. '
              'A tall pine on the far right. Flat open snowy ground across the whole lower third with a trail of footprints from the cabin to '
              'the cave. Dense spruce forest behind, pink-violet evening sky, a big low orange sun.',
    'den2': 'Interior of a big cozy bear den under the snow, front view: a large rounded earthen cave, hanging tree roots, a thick round '
            'nest of hay and old patterned wool blankets in the center on the floor, a soft beam of light from a vent hole in the ceiling, '
            'warm amber light, uncluttered, a big empty space in the center for a huge sleeping animal, the cave entrance glowing blue on '
            'the far left edge.',
    'porch': 'Close view of the front of an old log cabin in deep winter: a log wall on the left half with a small frosted window glowing '
             'warm, snow on the porch steps, a neat stack of firewood, icicles hanging from the roof edge, an old enamel basin on a nail; '
             'the right half opens to a snowy taiga clearing with spruce trees and a big low orange sun, pink-violet sky.',
}


if __name__ == '__main__':
    if sys.argv[1:2] == ['v2']:
        total = 0.0
        for n in sys.argv[2:] or list(BG2):
            p = OUT / f'{n}.png'
            if not p.exists(): total += xai.generate(STYLE2 + BG2[n], [str(p)], aspect='16:9')
        print('total $%.3f' % total); sys.exit()
    names = sys.argv[1:] or list(BG)
    total = 0.0
    for n in names:
        p = OUT / f'{n}.png'
        if p.exists():
            continue
        total += xai.generate(STYLE + BG[n], [str(p)], aspect='16:9')
    print('total $%.3f' % total)
