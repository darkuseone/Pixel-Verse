"""S01E03 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import stage as ST
import covergen_us as CG
from stage import Chars, view_at
from scene import Layer
from props import us_cast as U, us_props as UP, uskit as K

EP, SLUG = 'ep03', 'sunny-palms-hoa'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['SUSPICIOUS', 'MAN', '(WALKING)']
SIZES = [60, 100, 60]
CHARS = ("on the left a sunburnt Florida man with a bleached blond mullet and gold aviator sunglasses, teal Hawaiian shirt with pink flowers, "
         "cargo shorts, walking nervously with a black garbage bag over his shoulder and glancing sideways guiltily; on the right a woman with a white sun "
         "visor and frosted blonde bob peeking over a green hedge, holding binoculars to her eyes and a smartphone, with a too-sweet forced smile. "
         "Sunny pastel Florida suburb with palm trees behind.")


def ref():
    world = ST.ai_world(P.series(SLUG) / 'bg' / 'yard.png')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))
    v = view_at(world, 335, 470, Z, 180, 372)
    big = v.bg()
    CG.calm_sky(big)
    CH = Chars()
    U.dale(CH, v.cam(232.0, 790.0, 15.0), U.dwalk(0.6, 8.0, 0.4, carry=False), 0.6, 0.0, 'sly', 0.5, True, hand_n=U.H(3.0, 19.0), prop_n=UP.trash_bag, red=0.3)
    CH.comp(big, K.light_yard(v))
    C2 = Chars()
    U.brenda(C2, v.cam(470.0, 790.0, 15.0, flip=True), U.BPOSE['stand'], 0.3, 0.0, 'evil', 0.0, hand_n=U.H(5.8, 18.0), prop_n=UP.binoculars, hand_f=U.H(3.4, 15.0),
             prop_f=lambda L, h: UP.phone(L, h, 0.0, screen='ring'))
    C2.comp(big, K.light_yard(v))
    C3 = Chars()                                                                        # hedge in front of Brenda
    L = Layer(v.cam(470.0, 790.0, 15.0).__class__(0, 0, 0, 0, 1) and v.wcam())
    for i in range(9):
        UP.ell(L, (395 + i * 26, 640 + 8 * ((i * 3) % 4)), 30, 26, (44, 120, 60), 0, (86, 170, 84), (26, 78, 44))
    UP.outline(L, UP.OL)
    C3.add(L)
    C3.comp(big, K.light_yard(v))
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e03.png'], 3, TITLE, SIZES)
        print('ok')
