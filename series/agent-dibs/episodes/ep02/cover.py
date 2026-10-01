"""S01E02 cover.  python3 cover.py ref | ai | make"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import paths as P
import stage as ST
import fx
import covergen_dibs as CG
from stage import Chars, view_at
from props import chi_cast as C, chi_props as PR, chikit as K

EP, SLUG = 'ep02', 'agent-dibs'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['FREE', 'TRIAL?']
SIZES = [118, 112]
CHARS = ("on the left a see-through, glass-like ghostly special agent outlined in glowing cyan (the checkered marble floor shows through his body), "
         "with a grey fur hat with ear flaps, black sunglasses, a big round pink nose, a brown mustache and a navy-blue puffer jacket, "
         "tiptoeing with a red snow shovel and looking shocked with his mouth open; on the right a chubby security guard in a black puffer jacket "
         "and black beanie with a yellow badge, holding a huge sandwich and staring straight at him with wide eyes. "
         "Luxurious villain skyscraper lobby with black-and-white checkered marble floor, neon cyan and magenta light strips and a gold elevator behind.")


def ref():
    world = K.world('lair_lobby')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))
    wcx, wcy, sx, sy = 640.0, 420.0, 180, 372
    v = view_at(world, wcx, wcy, Z, sx, sy)
    big = v.bg()
    CG.calm_night(big)
    un = 15.0
    CH = Chars()
    C.gary(CH, v.cam(wcx + 105.0, wcy + 330.0, 14.0, True), C.POSE['hold'], 0.3, 0.1, 'shock', 0.0, hand_n=C.H(4.4, 12.8),
           prop_n=lambda L, h: PR.sandwich(L, h, bites=1), front=PR.guard_badge)
    CH.comp(big, K.light_lobby(v))
    G = Chars()
    C.dibs(G, v.cam(wcx - 92.0, wcy + 322.0, un), C.POSE['stand'], 0.3, 0.9, 'shock', 0.0, True, chair=False,
           prop_n=lambda L, h: PR.shovel(L, h, -1.95), hand_n=C.H(4.6, 12.6), sweat=0.6)
    K.ghost_comp(G, big, K.light_lobby(v), 0.46, t=0.3)
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        (P.series(SLUG) / 'covers').mkdir(exist_ok=True)
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e02.png'], 2, TITLE, SIZES)
        print('ok')
