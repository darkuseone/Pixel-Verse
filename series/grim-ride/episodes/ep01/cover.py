"""Cover S01E01: Death's wheelie on the e-bike under the full moon (code frame, no AI) + title «DEATH GOT / AN E-BIKE?» + tombstone plate.
  python3 cover.py   -> cover.png (+ series/grim-ride/covers/cover_s01e01.png)"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import shutil, math
import numpy as np
from stage import view_at
import ep01 as E
from props import grimcast as GC
from props import grimkit as K
import covergen_grim as CG

t = 0.42
cx = 400.0
v = view_at(E.STREET, cx, 300.0, 1.25, 180, 320)
g = E.put(v, GC.grim, 600, 1560, 10.5, t=t, expr='proud', mouth_=0.85, wind=1.0, spin=3.0, batt=13, raven=True, rot=24.0, pivot=E.WHEELIE['pivot'])
def f(big, v_):
    K.speed_streaks(big, t, 0.7)
    K.leaves(big, t, 18, seed=2, speed=1.6)
    K.glow_ring(big, 760, 860, 330, (150, 255, 110), 0.12)
big = K.shot(E.STREET, K.light_street, cx, 300.0, 1.25, acts=[g], fx_=f, sx=180, sy=320)
here = pathlib.Path(__file__).parent
CG.make(big, ['DEATH GOT', 'AN E-BIKE?'], n=1, out=str(here / 'cover.png'), title_y=150, plate_y=1420)
dst = here.parents[1] / 'covers' / 'cover_s01e01.png'
dst.parent.mkdir(exist_ok=True)
shutil.copy(here / 'cover.png', dst)
print(dst)
