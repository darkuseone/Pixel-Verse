"""S02E03 cover «40 БАНОК?!» — code only: the jar mountain at Valera's door up to the ceiling, the cat on top, Valera panicking.
  python3 cover.py   ->  cover.png, covers/cover_s02e03.png, cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen2 as CG
from stage import view_at
import s2e03 as E

HERE = pathlib.Path(__file__).resolve().parent
t = 0.5
v = view_at(E.LAND, 405, 330, 1.25, 180, 440)


def draw(CH, v_, top):
    E.valera(CH, v_, t, (500.0, 640.0, 13.5), "shrug", "shout", flip=True)
    E.F.cat(CH, v_.cam(top[0] - 22, top[1] + 4, 5.5), t=t, pose='loaf', lid=0.6, tail=0.2, expr='smug')


big, _ = E.landing(v, t, draw, label=True)
dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
CG.code_cover(big, 'ВАЛЕРА И КОТ\nСЕЗОН 2 • 3/6', ['40 БАНОК?!'], [HERE / 'cover.png', dst / 'cover_s02e03.png'])
print(HERE / 'cover.png')
