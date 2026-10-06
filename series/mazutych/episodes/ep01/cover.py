"""Cover S01E01 «Круговорот»: Мазутыч close on the monowheel with the Lada steering wheel, the queue and «БЕНЗИНА НЕТ» behind him,
title «НЕФТЯНИК / БЕЗ БЕНЗИНА» (= hook text = first line), hazard plate. Everything from the series' own world and sprites.
  python3 cover.py   ->  cover.png (+ copy in series/mazutych/covers/cover_s01e01.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
import paths as P
from covergen_maz import make
import ep01 as E
from props import mazkit as K
from props import mazcast as MC

t = 1.2
Z = 1.3
cx, cy = 1003.0 + 180 / Z, 0.0 + 330 / Z
v = E.view_at(E.HW, cx, cy, Z, 180, 330)
hx, hy = E.wpt(v, 400, 980)
acts = E.queue_acts(t, Z, 0.0)[5:] + [E.A(MC.maz, hx, hy, 9.5, pin='head', t=t, expr='glare', wind=1.0, mouth_=0.0, beacon=True,
                                          look=(1.0, 0.6), steer=0.35, spin=1.0)]
def f(big, v_):
    K.flare(big, v_, t, 664, 205, 1.2, 0.8)
    K.wind_lines(big, t, 0.6)
frame = K.shot(E.HW, K.light_hw, cx, cy, Z, acts=acts, fx_=f, sx=180, sy=330)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['НЕФТЯНИК', 'БЕЗ БЕНЗИНА'], n=1, out=str(out), title_y=200, title_size=70)
dst = P.series(E.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
shutil.copy(out, dst / 'cover_s01e01.png')
print(out)
