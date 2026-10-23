"""S02E06 cover «+32 ДОМА?!» — code only: Valera melting by the fan in his telnyashka, the thermometer at +32, the pane shut.
  python3 cover.py   ->  cover.png, covers/cover_s02e06.png, cover_grid.png"""
import sys, pathlib, math; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen2 as CG
import overlays as O
from stage import view_at
import s2e06 as E

HERE = pathlib.Path(__file__).resolve().parent
t = 0.37
x, y, un = 800.0, 660.0, 16.5
fx_, fy_ = E.face_w(x, y, un, flip=True, h=20.6)
v = view_at(E.KIT, 700, fy_, 1.5, 180, 372)


def draw(CH, v_):
    E.v_cold(CH, v_, t, (x, y, un), 'hips', 'shout', cold=0.0, hat=None, tint=(1.12, 0.94, 0.9))
    E.fan(CH, v_, t, fx_ - 80, fy_ + 160)


big = E.kitchen(v, t, draw, warm=1.0, k_open=0.0, therm=32, drift_k=0.0,
                cat_kw=dict(mouth=0.0, lid=0.85, tail=1.0, expr='blissful'))
E.sweat(big, v, t, fx_ - 6, fy_ - 30)
th = E.img_thermo(32)
O.overlay(big, th, 330, 930, 1.0)
dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
CG.code_cover(big, 'ВАЛЕРА И КОТ\nСЕЗОН 2 • 6/6', ['+32 ДОМА?!'], [HERE / 'cover.png', dst / 'cover_s02e06.png'])
print(HERE / 'cover.png')
