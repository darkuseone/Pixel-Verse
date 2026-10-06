"""Cover S01E04 «Без прав»: the cop raises his striped baton and whistles at Мазутыч on the monowheel, patrol lights wash;
title «ДПС ТОРМОЗИТ / МОНОКОЛЕСО» (= hook text).  python3 cover.py -> cover.png (+ covers/cover_s01e04.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_maz import make
import ep04 as E
from props import mazkit as K
from props import mazcast as MC
from props.mazshots import A, wpt

t = 0.2; Z = 1.3
cx, cy = E.PX + 60, 420.0
v = E.view_at(E.HW, cx, cy, Z, 180, 330)
mx, my = wpt(v, 300, 1020); cxw, cyw = wpt(v, 790, 960)
m = A(MC.maz, mx, my, 9.5, pin='head', t=t, expr='shock', look=(1.0, 0.0), mouth_=0.5, blink=False, beacon=True, wind=0.4)
c = A(MC.inspector, cxw, cyw, 11.0, pin='head', t=t, expr='glare', pose='stop', whistle=True, flip=True, look=(1.0, 0.0), blink=False)
frame = K.shot(E.HW, K.light_hw, cx, cy, Z, acts=[m, c], sx=180, sy=330)
E.lights(frame, t, 0.2)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['ДПС ТОРМОЗИТ', 'МОНОКОЛЕСО'], n=4, out=str(out), title_y=150, title_size=68)
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e04.png')
print(out)
