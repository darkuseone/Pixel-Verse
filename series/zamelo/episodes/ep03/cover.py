"""Cover S01E03 «ГДЕ МОЯ МАШИНА?!»: Жора with the shovel among identical car-shaped snow mounds with flags, yelling; the road-sign
plate on top of the 3:4 grid zone + the «аляска» title.  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import stage as ST
import ep03 as E
from props import zamkit as K, zamcast as C

t = 1.2
ST.T_NOW[0] = t
Z, cx, cy = 1.7, 540.0, 430.0
v = K.V('carfield', cx, cy, Z)
z = K.A(C.zhora, 500.0, 640.0, E.S_of(v) * 1.15, t=t, expr='outraged', mouth_=0.9, look=(0.6, -0.2), blink=False, hand_n=(22.0, 40.0),
        prop_n=lambda sp, h: C.shovel(sp, h, ang=1.3, l=30.0), hand_f=(-14.0, 66.0))
z.near = 0.99
big = K.shot('carfield', K.light_morning, cx, cy, Z, acts=E.flags(v, t) + [z], t=t, focus=0.85, dof_k=8, snow_n=60)
K.cover_make(big, ['ГДЕ МОЯ', 'МАШИНА?!'], n=3, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=84)
print('cover.png')
