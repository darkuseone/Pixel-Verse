"""xAI backgrounds for «Батя сам» (16:9 1280x720, grok-imagine-image-2.0, ~$0.04–0.06 each). Skips existing files.
  python3 series/batya/gen_bg.py [names...]
Heroes, blankets, the nightstand pharmacy, pots, smoke, signs, labels, light and particles are drawn in code; backgrounds have no
people, no text."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / 'engine'))
import xai

OUT = pathlib.Path(__file__).resolve().parent / 'bg'
OUT.mkdir(exist_ok=True)
STYLE = ('Detailed HD pixel art game background, cosy retro 90s sitcom look, modern indie pixel-art adventure game style, crisp visible '
         'pixels, rich environmental detail, warm saturated colours, small Soviet panel-block apartment in late November, wide 16:9 scene, '
         'front view, eye level. No characters, no people, no animals, no text, no letters, no numbers, no symbols; any signs, labels, '
         'calendars, certificates, posters and papers are completely blank. ')
BG = {
    'bedroom': 'The parents\' bedroom in the evening, warm yellow lamp light and a cold dark blue window. In the centre-left a wide double '
               'bed with a tall glossy polished dark-wood headboard against the back wall, a smooth plain beige bedspread and two white '
               'pillows, the top of the bed is clear and flat. On the back wall above the bed a huge red-and-burgundy oriental carpet '
               'hanging on the wall. To the right of the bed a small polished wooden nightstand with an empty top and a table lamp with a '
               'pleated orange shade. On the far left a tall lacquered brown wall unit with glass doors, crystal glassware and porcelain '
               'behind the glass. On the right a window with white tulle and heavy curtains, dark blue November evening sky, snowflakes and '
               'lit windows of panel blocks outside, a radiator under the window. On the far right edge a half-open white-painted door to a '
               'dark hallway. Parquet floor with a small rug. Blank framed certificate and a blank wall calendar on the walls.',
    'kitchen': 'A tiny Soviet panel-block kitchen in the evening, warm ceiling lamp light, dark blue window. In the centre-left an old white '
               'four-burner gas stove with an oven, the stove top is clear and empty, a light-blue tiled wall behind it with a rooster tile '
               'strip, a small extractor hood. On the far left an old white rounded fridge with many fridge magnets. On the back wall a '
               'window with tulle and pots of seedlings on the sill, wooden wall cupboards with glass jars of buckwheat and salt. On the right '
               'a small kitchen table with a checked oilcloth tablecloth, a stool, a radio on a shelf, a blank wall calendar. Worn linoleum '
               'floor. The floor in the middle is clear empty space.',
}


def main(names):
    for n in names or BG:
        out = OUT / f'{n}.png'
        if out.exists(): print('skip', out); continue
        xai.generate(STYLE + BG[n], [str(out)], aspect='16:9')
        print('ok', out)


if __name__ == '__main__':
    main(sys.argv[1:])
