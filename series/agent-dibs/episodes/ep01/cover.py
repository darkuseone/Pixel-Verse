"""S01E01 cover.  python3 cover.py ref | ai | make"""
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

EP, SLUG = 'ep01', 'agent-dibs'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['CALLED', 'DIBS!']
SIZES = [96, 132]
CHARS = ("on the left a shouting special agent with a big brown mustache, a big round pink nose, a grey fur hat with ear flaps and a navy-blue "
         "puffer jacket, pointing one finger at a green-and-white aluminium folding lawn chair standing on the right in the snow; under the "
         "chair sits a big round black cartoon bomb with a short burning fuse throwing orange sparks; a blank cardboard sign is taped to the chair. "
         "Snowy Chicago side street at night with brick two-flat buildings, cars buried in snow, orange street lamps, an elevated train far away.")


def ref():
    world = K.world('dibs_row')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))                                          # chunky hero pixels like the close-ups
    wcx, wcy, sx, sy = 640.0, 420.0, 180, 372
    v = view_at(world, wcx, wcy, Z, sx, sy)
    big = v.bg()
    CG.calm_night(big)
    un = 15.0
    CH = Chars()
    C.dibs(CH, v.cam(wcx - 92.0, wcy + 322.0, un), C.POSE['point'], 0.3, 0.9, 'shout', 0.0, False, chair=False, flap=0.3)
    CH.comp(big, K.light_street(v))
    cu = un * 0.62 * 1.15
    ax, ay = wcx + 66.0, wcy + 206.0
    C2 = Chars()
    PR.dibs_chair(C2, v.cam(ax, ay, cu), t=0.3)
    C2.comp(big, K.light_street(v))
    C3 = Chars()
    bx, by, bu = ax - 30.0, ay + 26.0, cu * 1.5
    sp = PR.bomb(C3, v.cam(bx, by, bu), 0.3, 1.0)
    C3.comp(big, K.light_street(v))
    ox, oy = v.opt(bx + sp[0] * bu, by - sp[1] * bu)
    fx.glow(big, ox, oy, 300 * Z, (255, 150, 50), 0.85)
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        (P.series(SLUG) / 'covers').mkdir(exist_ok=True)
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e01.png'], 1, TITLE, SIZES)
        print('ok')
