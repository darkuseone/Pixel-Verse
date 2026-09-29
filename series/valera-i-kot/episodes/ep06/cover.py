"""S01E06 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen2 as CG
from PIL import Image

EP, SLUG = 'ep06', 'valera-i-kot'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['С ЛЁГКИМ', 'ПАРОМ?!']
CHARS = ("a heavyset bald middle-aged man with a thin comb-over, huge bushy brown walrus moustache and a red bulbous nose, wearing a "
         "blue-and-white striped sailor undershirt (telnyashka) and blue track pants, triumphantly holding a metal washbasin high over "
         "his head and shouting with joy, in a cozy shabby Soviet kitchen decorated for New Year's Eve: a string of colorful garland "
         "lights, golden tinsel on the radiator, snow falling outside the frosty window; a fat ginger cat with half-closed eyes and a "
         "tinsel collar lying on the radiator, completely unimpressed.")


def ref():
    import ep06 as E
    from stage import view_at
    t = 4.3
    v = view_at(E.KIT, 742, 430, 0.95, 180, 410)
    x, y, un = E.LIFT_V
    def draw(CH, v_):
        E.F.valera(CH, v_.cam(x, y, un), E.F.VPOSE['overhead'], t, 0.8, 'shout', 'home', hand_n=(1000 + 5.6, 1000 - 27.5),
                   hand_f=(1000 - 3.6, 1000 - 27.5))
        L = E.Layer(v_.cam(x, y, un)); E.B.basin(L, (1000 + 1.0, 1000 - 28.4), scale=1.15); E.F.outline(L); CH.add(L)
    big = E.kitchen_frame(v, t, draw, cat=True, cat_kw=dict(lid=0.85, mouth=0.0))
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e06.png'], 6, TITLE)
        print('ok')
