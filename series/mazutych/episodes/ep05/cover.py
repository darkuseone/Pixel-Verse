"""Cover S01E05 «Биотопливо»: the samovar rig with a glowing jar of gold, Мазутыч proud, Толик cheering;
title «БЕНЗИН / ИЗ СЕМЕЧЕК» (= hook text).  python3 cover.py -> cover.png (+ covers/cover_s01e05.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_maz import make
import ep05 as E

import fx
from props import mazcast as MC
from props.mazshots import A, wpt, aout, SP
t = 1.0; Z = 1.25
cx, cy = 420.0, 470.0
v = E.view_at(E.GI, cx, cy, Z, 180, 330)
rx, ry = wpt(v, 560, 1450); mx, my = wpt(v, 860, 900); tx, ty = wpt(v, 200, 940)
rig = A(MC.still, rx, ry, 13.0, t=t, level=0.6, gauge=0.95, shake=0.0)
m = A(MC.maz, mx, my, 9.0, pin='head', flip=True, t=t, expr='proud', look=(1.0, 0.2), blinker=1.0, ride=False, wheel=False, hold=False, beacon=True)
tl = A(MC.tolik, tx, ty, 9.0, pin='head', t=t, expr='cheer', mouth_=0.5, look=(1.0, 0.0))
def f(big, v_):
    x, y = aout(rig, v_, 'jar')
    fx.glow(big, x, y, 420, (255, 220, 110), 0.6)
frame = E.K.shot(E.GI, E.light_gi, cx, cy, Z, acts=[rig, tl, m], fx_=f, sx=180, sy=330)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['БЕНЗИН', 'ИЗ СЕМЕЧЕК'], n=5, out=str(out), title_size=76)
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e05.png')
print(out)
