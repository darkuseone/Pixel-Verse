"""S01E01 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import stage as ST
import covergen_us as CG
from stage import Chars, view_at
from props import us_cast as U, us_props as UP, uskit as K

EP, SLUG = 'ep01', 'sunny-palms-hoa'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['$250', 'FOR A', 'MAILBOX?!']
SIZES = [100, 58, 54]
CHARS = ("on the left a shouting sunburnt Florida man with a bleached blond mullet, gold aviator sunglasses pushed up on his hair, big peeling nose, "
         "teal Hawaiian shirt with pink flowers, holding a pink violation notice in his fist; on the right a smiling woman with a white sun visor, "
         "frosted blonde bob, mint-green polo shirt, lanyard badge and a clipboard, with a too-sweet forced smile; between and in front of them a beige "
         "mailbox on a wooden post with a red flag. Sunny pastel Florida suburb with palm trees behind.")


def ref():
    world = ST.ai_world(P.series(SLUG) / 'bg' / 'yard.png')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))                                          # chunky hero pixels like the close-ups
    v = view_at(world, 335, 470, Z, 180, 372)
    big = v.bg()
    # calm sky in the top third: the title goes there (cover text needs a quiet background)
    h = 720
    ys = np.arange(1920)[:, None].astype(np.float32)
    a = np.clip(1.0 - (ys - 380) / 420.0, 0, 1) ** 0.7
    sky = np.zeros((1920, 1, 3), np.float32)
    for c, (top, bot) in enumerate(((96, 168), (188, 226), (255, 255))): sky[:, 0, c] = top + (bot - top) * np.clip(ys[:, 0] / 900, 0, 1)
    big[:] = (big * (1 - a[..., None]) + sky * a[..., None]).astype(np.uint8)
    for cx, cy, w in ((250, 150, 200), (760, 260, 260), (470, 60, 150)):                                # a few chunky clouds
        for k in range(5):
            x0 = cx - w // 2 + k * w // 6; r = int(w * 0.26 * (1 - abs(k - 2) * 0.22))
            yy, xx = np.ogrid[:1920, :1080]
            m = ((xx - x0) ** 2 + (yy - cy + 12 * (k % 2)) ** 2) < r * r
            big[m] = (250, 252, 255)
    CH = Chars()
    U.dale(CH, v.cam(232.0, 790.0, 15.0), U.DPOSE['stand'], 0.3, 0.9, 'shout', 0.0, False, hand_n=U.H(7.4, 17.0),
           prop_n=lambda L, h: UP.notice(L, h, -0.25, w=6.2, hh=7.8), red=0.7, sweat=0.5)
    CH.comp(big, K.light_yard(v))
    C2 = Chars()
    U.brenda(C2, v.cam(455.0, 790.0, 15.0, flip=True), U.BPOSE['stand'], 0.3, 0.0, 'sweet', 0.0, hand_n=U.H(3.4, 9.6), prop_n=UP.clipboard)
    C2.comp(big, K.light_yard(v))
    C3 = Chars()
    UP.mailbox_world(C3, v, 345.0, 655.0, 1.0, 0.0, s=1.5)
    C3.comp(big)
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e01.png'], 1, TITLE, SIZES)
        print('ok')
