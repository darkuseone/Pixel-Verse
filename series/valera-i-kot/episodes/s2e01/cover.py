"""S02E01 cover «+14 ДОМА?!» (same look as S01: blue enamel plank at the top of the 3:4 grid zone, frosty title under it).
  python3 cover.py ref | ai | make | grid"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen2 as CG
from PIL import Image

EP, SLUG = 's2e01', 'valera-i-kot'
HERE = pathlib.Path(__file__).resolve().parent
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = HERE / 'cover_ai_source.jpg'
TITLE = ['+14 ДОМА?!']
CHARS = ("a heavyset middle-aged man with a huge bushy brown walrus moustache covered in tiny icicles and a red bulbous nose, wearing a "
         "grey ushanka fur hat with ear flaps, a blue-and-white striped sailor undershirt (telnyashka) and blue track pants, shivering, "
         "hugging himself and shouting in outrage with frosty breath, in a shabby Soviet kitchen in winter: snow blowing in through a wide-open "
         "small ventilation window pane, a snowdrift on the windowsill, a big room thermometer on the window frame; a fat ginger cat with "
         "half-closed eyes lying on a cold radiator, looking betrayed. Lower half of the image: the man's face and the thermometer.")


def ref():
    import s2e01 as E
    t = 1.2
    big = E.r_hook(t, 0.8)
    Image.fromarray(big).save(REF); print(REF)


def grid():
    """TikTok / Reels profile tile preview: the 3:4 centre crop at 1/4 size"""
    im = Image.open(HERE / 'cover.png')
    w, h = im.size; h34 = int(w * 4 / 3); y0 = (h - h34) // 2
    im.crop((0, y0, w, y0 + h34)).resize((w // 4, h34 // 4), Image.LANCZOS).save(HERE / 'cover_grid.png')
    print(HERE / 'cover_grid.png')


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [HERE / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s02e01.png'], 1, TITLE,
                plank='ВАЛЕРА И КОТ\nСЕЗОН 2 • 1/6')
        grid()
    elif cmd == 'grid': grid()
