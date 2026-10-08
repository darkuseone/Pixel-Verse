"""Cover S01E01 «Кто крайний?»: Мазутыч on the monowheel straining, towing his dead «six» on a rope towards АЗС «ГАЗПРОПАЛ» with
«БЕНЗИНА НЕТ»; title «ГДЕ / БЕНЗИН?!» (= hook text = first line, v3), hazard plate. Everything from the series' own world and sprites.
  python3 cover.py   ->  cover.png (+ copy in series/mazutych/covers/cover_s01e01.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_maz import make
import ep01 as E
from props import mazkit as K
from props import mazcast as MC

t = 1.2
Z = 1.15
cx, cy = 1083.0, 0.0 + 330 / 1.15
v = E.view_at(E.HW, cx, cy, Z, 180, 330)
hx, hy = E.wpt(v, 640, 930)
cxw, cyw = E.wpt(v, 40, 1450)
car = E.A(MC.lada, cxw, cyw, 6.0, col=(232, 228, 214), driver=False)
m = E.A(MC.maz, hx, hy, 5.8, pin='head', t=t, expr='strain', wind=0.8, mouth_=0.3, beacon=True, sweat=1.0, spin=1.0, rot=-10.0)
def f(big, v_):
    E.rope(big, E.aout(m, v_, 'belt'), E.aout(car, v_, 'front'), sag=20, w=14)
    ox, oy = E.aout(m, v_, 'wheel')
    E.sparks(big, ox, oy + 60, t, 22, 260)
    K.flare(big, v_, t, 664, 205, 1.2, 0.8)
    K.wind_lines(big, t, 0.5)
frame = K.shot(E.HW, K.light_hw, cx, cy, Z, acts=[car, m], fx_=f, sx=180, sy=330)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['ГДЕ', 'БЕНЗИН?!'], n=1, out=str(out), title_y=130, title_size=84)
dst = P.series(E.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
shutil.copy(out, dst / 'cover_s01e01.png')
print(out)
