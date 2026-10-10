"""Cover S01E02 v2 «Талон на талон»: Мазутыч's outraged face + the pink coupon shoved at the lens (the hook frame);
title «ПРЕМИЮ ДАЛИ / ТАЛОНОМ?!» (= hook text = first line), hazard plate.  python3 cover.py -> cover.png (+ covers/cover_s01e02.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import fx
import paths as P
from covergen_maz import make
import ep02 as E
from props import mazkit as K
from props import mazcast as MC
from props.mazshots import A, wpt, aout

t = 1.0
Z = 1.2
cx, cy = 1000.0, 360.0
v = E.view_at(E.GATE, cx, cy, Z, 180, 330)
hx, hy = wpt(v, 500, 980)
m = A(MC.maz, hx, hy, 12.0, pin='head', t=t, expr='shock', look=(0.6, 0.8), beacon=True, mouth_=0.7, blink=False)
def pre(big, v_): K.flare(big, v_, t, 1105, 60, 1.6, 1.0)
frame = K.shot(E.GATE, K.light_gate, cx, cy, Z, acts=[m], pre=pre, sx=180, sy=330)
E.coupon(frame, t, 600, 1330, 1.15, rot=-10)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['ПРЕМИЮ ДАЛИ', 'ТАЛОНОМ?!'], n=2, out=str(out), title_size=70)
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e02.png')
print(out)
