"""S01E01 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen2 as CG
from PIL import Image

EP, SLUG = 'ep01', 'valera-i-kot'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['ЛЕДЯНАЯ!']
CHARS = ("a heavyset bald middle-aged man with a thin comb-over, huge bushy brown walrus moustache, red bulbous nose, bushy "
         "eyebrows, skin turned light blue from cold, icicles hanging from his moustache, screaming with wide eyes and hugging "
         "himself under an ice-cold shower spray in an old shabby tiled bathroom with a rusty bathtub; in the bottom right corner "
         "a fat ginger tabby cat with half-closed bored eyes looks at the viewer.")


def ref():
    import numpy as np
    import ep01 as E
    import stage as ST
    from stage import view_at, Chars
    from props import folk as F
    from props import bytfx as B
    from props import panelka as PK
    t = 0.9
    fx_, fy_ = E.face_w(E.SHOWER_V[0], E.SHOWER_V[1], PK.B_UNIT, h=20.6)
    v = view_at(E.BATH, fx_ - 15, fy_, 1.8, 170, 420)
    CH, FX = E.begin(v.Z)
    big = v.bg()
    E.valera_shower(CH, v, t, pose=F.VPOSE['shiver'], expr='shout', mouth=0.8, outfit='towel', cold=0.7, wet=1, breath=False)
    CH.comp(big, E.light_bath(v))
    B.spray(FX, v, t, PK.SHOWER, spread=60, drop=260, n=90)
    FX.comp(big)
    ST.set_px(2); CH2 = Chars()
    from stage import ACam
    F.cat(CH2, ACam(1000.0, 1000.0, 152, 322, 4.6), t, "sit", 0.0, 0.6)
    CH2.comp(big)
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e01.png'], 1, TITLE)
        print('ok')
