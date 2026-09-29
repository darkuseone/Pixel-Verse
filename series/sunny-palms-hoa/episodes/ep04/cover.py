"""S01E04 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import stage as ST
import covergen_us as CG
from stage import Chars, view_at
from props import us_cast as U, us_props as UP, uskit as K

EP, SLUG = 'ep04', 'sunny-palms-hoa'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['NO PERMIT', 'FOR THE', 'HURRICANE']
SIZES = [58, 72, 58]
CHARS = ("on the left a grinning sunburnt Florida man with a bleached blond mullet blowing in the wind and gold aviator sunglasses, teal Hawaiian shirt, "
         "sitting in a folding lawn chair holding a beer can, a blue cooler next to him; on the right a woman with a white sun visor and perfectly still "
         "frosted blonde bob, mint polo shirt, calmly holding a mint umbrella and a pink violation ticket with a too-sweet smile, completely dry; a violent "
         "hurricane behind them with dark green-gray clouds, bending palm trees, slanted rain, and pink plastic flamingos and a mailbox flying through the air. "
         "Sunny-yellow lightning glow, dramatic but funny.")


def ref():
    world = ST.ai_world(P.series(SLUG) / 'bg' / 'yard_storm.png')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))
    v = view_at(world, 335, 470, Z, 180, 372)
    big = v.bg()
    CH = Chars()
    UP.lawn_chair(CH, v.cam(232.0, 790.0, 15.0))
    U.dale(CH, v.cam(232.0, 790.0, 15.0), U.DPOSE['stand'], 0.3, 0.0, 'smug', 0.0, True, hand_n=U.H(6.6, 12.4), prop_n=UP.koozie_can, red=0.35, legs=False)
    CH.comp(big, K.light_storm(v))
    C1 = Chars()
    UP.cooler(C1, v.cam(340.0, 800.0, 11.0))
    C1.comp(big, K.light_storm(v))
    C2 = Chars()
    UP.umbrella(C2, v.cam(470.0, 790.0, 15.0, flip=True), 3.6, 12.0, 31.0)
    C2.comp(big, K.light_storm(v))
    C3 = Chars()
    U.brenda(C3, v.cam(470.0, 790.0, 15.0, flip=True), U.BPOSE['stand'], 0.3, 0.0, 'sweet', 0.0, hand_n=U.H(3.6, 12.0), prop_n=lambda L, h: UP.notice(L, h, -0.2, 5.6, 7.0, '$500'))
    C3.comp(big, K.light_storm(v))
    C4 = Chars()
    for i, (x, y) in enumerate(((190, 250), (420, 200), (300, 320))):
        UP.flamingo(C4, v.cam(x, y, 5.0), 0.3 + i, True, True, 0.0, 0.0)
    C4.comp(big, K.light_storm(v))
    UP.rain(big, 1.0, 1.0, 0.35, 140)
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e04.png'], 4, TITLE, SIZES)
        print('ok')
