"""S01E03 cover.  python3 cover.py ref | ai | make"""
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
import ep03 as E

EP, SLUG = 'ep03', 'agent-dibs'
REF, RAW = P.build(f'{SLUG}-{EP}', 'cover_ref.png'), P.build(f'{SLUG}-{EP}', 'cover_ai.png')
SRC = P.episode(EP, SLUG) / 'cover_ai_source.jpg'
TITLE = ['12 MPH', 'CHASE!']
SIZES = [112, 118]
CHARS = ("on the left a shouting special agent gripping the steering wheel of a rusty beige 1990s sedan, with pale pinkish-peach skin, a grey fur hat with ear flaps, "
         "black sunglasses, a HUGE round red-pink nose, a thick brown mustache and a navy-blue puffer jacket; the dashboard speedometer needle sits at 12 mph; "
         "through the windshield ahead a black SUV is sinking into a huge pothole full of icy water, only its roof, two scared faces in the windows and "
         "a red-tipped antenna still visible. Night street under an elevated train with orange sparks, falling snow, street lamps.")


def ref():
    world = K.world('avenue_under_L')
    Z = 1.05
    ST.set_px(ST.px_for_zoom(2.4))
    wcx, wcy, sx, sy = 640.0, 470.0, 180, 372
    v = view_at(world, wcx, wcy, Z, sx, sy)
    big = v.bg()
    E.draw_hole(big, v, wcx + 95.0, wcy + 52.0, 130.0, 26.0)
    CG.calm_night(big)
    un = 13.0
    ax, ay = wcx - 80.0, wcy + 304.0
    wheel, dash = E.interior_parts(ax, ay, un, 0.3)
    B = Chars()
    PR.suv(B, v.cam(wcx + 95.0, wcy + 96.0, 4.8), 0.3, signal=True, drivers=(('terry', -6.0), ('gary', 2.0)), antenna=10.0)
    B.comp(big, K.light_avenue(v))
    W = Chars(); wheel(W, v); W.comp(big, K.light_avenue(v))
    D = Chars()
    C.dibs(D, v.cam(ax, ay, un), E.DRIVE_POSE, 0.3, 0.9, 'shout', 0.0, True, chair=False, flap=0.5)
    D.comp(big, K.light_avenue(v))
    F = Chars(); dash(F, v); F.comp(big, K.light_avenue(v))
    Image.fromarray(big).save(REF); print(REF)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd == 'ref': ref()
    elif cmd == 'ai': CG.ai(REF, RAW, CHARS)
    elif cmd == 'make':
        (P.series(SLUG) / 'covers').mkdir(exist_ok=True)
        CG.make(RAW, SRC, [P.episode(EP, SLUG) / 'cover.png', P.series(SLUG) / 'covers' / 'cover_s01e03.png'], 3, TITLE, SIZES)
        print('ok')
