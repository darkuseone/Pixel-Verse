"""S01E02 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import stage as ST
import covergen_us as CG
from stage import Chars, view_at
from props import us_cast as U, us_props as UP, uskit as K

EP, SLUG = 'ep02', 'sunny-palms-hoa'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['EMOTIONAL', 'SUPPORT', 'FLAMINGO']
SIZES = [56, 76, 64]
CHARS = ("on the left a sunburnt Florida man with a bleached blond mullet and gold aviator sunglasses on his face, big peeling nose, teal Hawaiian shirt "
         "with pink flowers, smugly hugging a pink plastic lawn flamingo that wears a yellow safety vest and tiny gold aviator sunglasses; "
         "on the right a smiling woman with a white sun visor, frosted blonde bob, mint-green polo shirt and lanyard badge, holding a huge thick blue "
         "rulebook binder, with a too-sweet forced smile. Sunny pastel Florida suburb with palm trees behind.")


def ref():
    world = ST.ai_world(P.series(SLUG) / 'bg' / 'yard.png')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))
    v = view_at(world, 335, 470, Z, 180, 372)
    big = v.bg()
    CG.calm_sky(big)
    CH = Chars()
    U.dale(CH, v.cam(232.0, 790.0, 15.0), U.DPOSE['hold'], 0.3, 0.0, 'smug', 0.0, True, hand_n=U.H(7.4, 11.0), red=0.35)
    CH.comp(big, K.light_yard(v))
    C1 = Chars()
    UP.flamingo(C1, v.cam(292.0, 730.0, 13.5), 0.3, True, True, 0.0, 0.0)
    C1.comp(big, K.light_yard(v))
    C2 = Chars()
    U.brenda(C2, v.cam(468.0, 790.0, 15.0, flip=True), U.BPOSE['stand'], 0.3, 0.0, 'sweet', 0.0, hand_n=U.H(4.4, 8.6), prop_n=lambda L, h: UP.binder(L, h, -0.1, 5.4, 7.0))
    C2.comp(big, K.light_yard(v))
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e02.png'], 2, TITLE, SIZES)
        print('ok')
