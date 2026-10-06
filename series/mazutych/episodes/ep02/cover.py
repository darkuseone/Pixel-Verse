"""Cover S01E02 «Талон на талон»: Мазутыч in tears of joy holding up the fuel coupon against the refinery sunset;
title «ПРЕМИЯ — / ТАЛОНОМ» (= hook text), hazard plate.  python3 cover.py -> cover.png (+ covers/cover_s01e02.png)"""
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
m = A(MC.maz, hx, hy, 12.0, pin='head', t=t, expr='joy', card='talon', look=(0.8, 0.8), beacon=True, mouth_=0.4, blink=False)
def pre(big, v_): K.flare(big, v_, t, 1105, 60, 1.6, 1.0)
def f(big, v_):
    x, y = aout(m, v_, 'hand')
    fx.glow(big, x, y - 80, 420, (255, 236, 170), 0.45)
frame = K.shot(E.GATE, K.light_gate, cx, cy, Z, acts=[m], pre=pre, fx_=f, sx=180, sy=330)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['ПРЕМИЯ —', 'ТАЛОНОМ'], n=2, out=str(out), title_y=150, title_size=76)
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e02.png')
print(out)
