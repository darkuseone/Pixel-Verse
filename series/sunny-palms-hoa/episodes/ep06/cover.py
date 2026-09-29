"""S01E06 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import stage as ST
import covergen_us as CG
from stage import Chars, view_at
from props import us_cast as U, us_props as UP, uskit as K

EP, SLUG = 'ep06', 'sunny-palms-hoa'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['VOTE', 'DALE']
SIZES = [96, 104]
CHARS = ("on the left a smug sunburnt Florida man with a bleached blond mullet, white president's sun visor with a pink stripe, teal Hawaiian shirt, "
         "holding a big clipboard titled FINES, grinning; on the right a horrified woman with frosted blonde bob and mint-green polo shirt, sweating, "
         "holding a pink notice with the number $250; in the front-right a green alligator head peeking out of a pond with a small round I VOTED sticker on its snout. "
         "Pastel clubhouse patio with a pond and bunting behind them.")


def ref():
    world = ST.ai_world(P.series(SLUG) / 'bg' / 'clubhouse.png')
    Z = 1.0
    ST.set_px(ST.px_for_zoom(2.4))
    v = view_at(world, 930, 420, Z, 180, 372)
    big = v.bg()
    CG.calm_sky(big)
    CH = Chars()
    U.dale(CH, v.cam(830.0, 645.0, 11.5), U.DPOSE['hold'], 0.3, 0.0, 'smug', 0.0, False, visor=True, hand_n=U.H(6.4, 12.4),
           prop_n=lambda L, h: UP.clipboard(L, h, -0.12, w=4.6, hh=6.2, title='FINES'))
    CH.comp(big, K.light_yard(v))
    C2 = Chars()
    U.brenda(C2, v.cam(985.0, 645.0, 11.5, flip=True), U.BPOSE['stand'], 0.3, 0.0, 'hollow', 0.0, hand_n=U.H(3.4, 12.4),
             prop_n=lambda L, h: UP.notice(L, h, -0.2, 5.4, 6.8, '$250'), sweat=0.9)
    U.earl(C2, v.cam(1090.0, 650.0, 6.0), 0.3, 0.0, 0.5, (-0.6, 0.0), None, 0.0, 1.0, True)
    C2.comp(big, K.light_yard(v))
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e06.png'], 6, TITLE, SIZES)
        print('ok')
