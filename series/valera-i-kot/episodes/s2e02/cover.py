"""S02E02 cover «ПЕРФОРАТОР В 8:00?!» — code only: Valera jolted up in bed under a drill bit poking through the ceiling crack, plaster
raining, the cat in a saucepan helmet, «СБ 08:00»; plank + title (covergen2.code_cover).
  python3 cover.py   ->  cover.png, covers/cover_s02e02.png, cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen2 as CG
import overlays as O
from scene import Layer
from stage import view_at
from props import vikit as K, folk as F
import s2e02 as E

HERE = pathlib.Path(__file__).resolve().parent
t = 0.62
x, y, un = E.V_BED
hx, hy = x + 1.5 * un, y - 22.0 * un
v = view_at(E.BED, hx + 6, hy - 10, 1.5, 180, 420)


def draw(CH, v_):
    E.valera(CH, v_, t, (x, y - 4, un), 'shout', 'shout', stubble=1.0)
    E.PK.clip_below(CH, v_, E.BLANKET_Y)
    L = Layer(v_.wcam())                                          # the drill bit through the ceiling crack
    F.cap(L, (hx + 30, -10), (hx + 30, 150), 6, 3, (176, 182, 192), (220, 224, 232), (120, 124, 134))
    for k in range(5): F.cap(L, (hx + 24, 10 + k * 26), (hx + 36, 20 + k * 26), 2, 2, (120, 124, 134))
    F.outline(L); CH.add(L)


big = E.bedroom(v, t, draw, dust=1.8, cat_kw=dict(lid=0.6, tail=0.0, expr='deadpan'), pot=True)
lcd = K.lcd_sticker("СБ 08:00", size=60)
O.overlay(big, lcd, 1080 - lcd.shape[1] - 24, 1440, 1.0)
dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
CG.code_cover(big, 'ВАЛЕРА И КОТ\nСЕЗОН 2 • 2/6', ['ПЕРФОРАТОР', 'В 8:00?!'], [HERE / 'cover.png', dst / 'cover_s02e02.png'])
print(HERE / 'cover.png')
