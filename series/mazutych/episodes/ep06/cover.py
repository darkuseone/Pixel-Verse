"""Cover S01E06 «Почётный нефтяник»: the red «Веста-Шместа» with a giant bow under the spotlights, Мазутыч in tears of joy, confetti;
title «ЗА 25 ЛЕТ — / МАШИНА?!» (= hook text = first line, v2).  python3 cover.py -> cover.png (+ covers/cover_s01e06.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_maz import make
import ep06 as E

import fx
from props import mazcast as MC
from props.mazshots import A, wpt, aout, SP, CAR
t = 1.0; Z = 1.6
cx, cy = 790.0, 430.0
v = E.view_at(E.HALL, cx, cy, Z, 180, 420)
mx, my = wpt(v, 730, 1000)
car = A(MC.vesta, 770.0, E.STAGE_Y - 4, CAR * Z, t=t, bow=1.0)
m = A(MC.maz, mx, my, 8.6, pin='head', flip=True, t=t, expr='joy', look=(1.0, 0.2), beacon=True, mouth_=0.4)
def f(big, v_):
    E.spots(big, v_, t, 2.0)
    x, y = v_.opt(770, E.STAGE_Y - 40)
    fx.glow(big, x, y, 460, (255, 230, 160), 0.35)
frame = E.K.shot(E.HALL, E.light_hall, cx, cy, Z, acts=[car, m], fx_=f, sx=180, sy=420)
E.K.confetti(frame, 3.6, 2.9, n=200, seed=2)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['ЗА 25 ЛЕТ —', 'МАШИНА?!'], n=6, out=str(out), title_y=150, title_size=72)
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e06.png')
print(out)
