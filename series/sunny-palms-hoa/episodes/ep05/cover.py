"""S01E05 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import stage as ST
import covergen_us as CG
from stage import Chars, view_at
from props import us_cast as U, us_props as UP, uskit as K

EP, SLUG = 'ep05', 'sunny-palms-hoa'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['FREE', 'HOT DOG', '$47.63']
SIZES = [80, 68, 84]
CHARS = ("on the left an outraged sunburnt Florida man with a bleached blond mullet and gold aviator sunglasses pushed up on his hair, teal Hawaiian shirt, "
         "holding out an empty paper plate; on the right a smiling woman with a white sun visor, frosted blonde bob and mint-green polo shirt, holding barbecue "
         "tongs with one single plain hot dog and, in her other hand, a payment tablet showing three green tip buttons, with a too-sweet forced smile. "
         "Pastel clubhouse patio barbecue with grill smoke behind them.")


def ref():
    world = ST.ai_world(P.series(SLUG) / 'bg' / 'clubhouse.png')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))
    v = view_at(world, 400, 400, Z, 180, 372)
    big = v.bg()
    CG.calm_sky(big)
    CH = Chars()
    U.dale(CH, v.cam(300.0, 720.0, 15.0), U.DPOSE['hold'], 0.3, 0.0, 'shout', 0.0, False, hand_n=U.H(7.4, 12.6), red=0.6, sweat=0.4,
           prop_n=lambda L, h: UP.ell(L, h, 3.4, 1.0, (250, 250, 246), 0, (255, 255, 255), (196, 200, 208)))
    CH.comp(big, K.light_yard(v))
    C2 = Chars()
    U.brenda(C2, v.cam(500.0, 720.0, 15.0, flip=True), U.BPOSE['stand'], 0.3, 0.0, 'sweet', 0.0, hand_n=U.H(5.0, 14.6),
             prop_n=lambda L, h: (UP.tongs(L, h, -0.2), UP.hot_dog(L, (h[0] + 2.9, h[1] + 0.6))),
             hand_f=U.H(3.6, 12.6), prop_f=lambda L, h: UP.phone(L, h, 0.0, 6.0, 8.0, 'feed'))
    C2.comp(big, K.light_yard(v))
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e05.png'], 5, TITLE, SIZES)
        print('ok')
