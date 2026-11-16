"""Cover S01E06 «РАСТАЯЛО!»: Жора waist-deep in the meltwater lake at the door, shocked; the plate on top of the 3:4 grid zone + the title.
  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import stage as ST
import ep06 as E
from props import zamkit as K, zamcast as C

t = 22.5
ST.T_NOW[0] = t
Z, cx, cy = 1.55, 530.0, 470.0
v = K.V('flood', cx, cy, Z)
S = K.S_of(v, 'flood')
z = K.A(C.zhora, 520.0, 705.0, S, t=t, expr='shock', mouth_=0.8, look=(0.3, -0.2), blink=False, hand_n=(26.0, 66.0), hand_f=(-22.0, 66.0))
z.near = 0.99
def f(big, _):
    E.water_front(big, v, t, a=0.45)
    E.ripple(big, v, 520.0, E.WL, t)
big = K.shot('flood', K.light_morning, cx, cy, Z, acts=[z], focus=0.8, dof_k=8, fx_=f, t=t, snow=False)
K.cover_make(big, ['РАСТАЯЛО!'], n=6, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=96)
print('cover.png')
