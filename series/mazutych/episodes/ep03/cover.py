"""Cover S01E03 «Из-под полы»: Вадик offers a golden «Родниковая» bottle from the glowing boot of a tinted «Приора»;
title «БЕНЗИН / ИЗ-ПОД ПОЛЫ» (= hook text).  python3 cover.py -> cover.png (+ covers/cover_s01e03.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
import fx
import paths as P
from covergen_maz import make
import ep03 as E
from props import mazcast as MC
from props.mazshots import A

from props import mazkit as K
from props.mazshots import wpt, aout
t = 1.0; Z = 1.3
cx, cy = 600.0, 420.0
v = E.view_at(E.GAR, cx, cy, Z, 180, 330)
mx, my = wpt(v, 330, 1000); vx, vy = wpt(v, 780, 980)
m = A(MC.maz, mx, my, 10.5, pin='head', t=t, expr='squint', look=(1.0, 0.0), mouth_=0.0, blink=False)
va = A(MC.vadik, vx, vy, 11.0, pin='head', t=t, expr='sly', pose='offer', bottle=True, flip=True, look=(1.0, 0.0), blink=False)
def f(big, v_):
    hx, hy = aout(va, v_, 'hand')
    fx.glow(big, hx, hy - 40, 380, (255, 220, 110), 0.55)
frame = K.shot(E.GAR, E.light_gar, cx, cy, Z, acts=[m, va], fx_=f, sx=180, sy=330)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['БЕНЗИН', 'ИЗ-ПОД ПОЛЫ'], n=3, out=str(out), title_y=160, title_size=78)
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e03.png')
print(out)
