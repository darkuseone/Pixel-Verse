"""Cover S01E04 «ТАКСИ — 3000?!»: Жора in the window yelling at the taxi app with ×7 surge, the road-sign plate on top of the 3:4 grid
zone + the «аляска» title.  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import overlays as O
import stage as ST
import ep04 as E
from props import zamkit as K, zamcast as C

t = 1.2
ST.T_NOW[0] = t
Z, cx, cy = 1.32, 712.0, 330.0
v = K.V('facade', cx, cy, Z)
S = K.S_of(v, 'facade')
z = K.A(C.zhora, 600.0, 690.0, S, t=t, expr='outraged', mouth_=0.9, look=(0.7, -0.2), blink=False, hand_n=(18.0, 60.0), prop_n=C.phone)
z.near = E.NEAR_ROOM
def f(big, _):
    ph = E.taxi_screen(5.0, t_up=0.0, w=440, h=720)
    O.overlay(big, ph, 650, 840, 1.0)
big = K.shot('facade', K.light_window, cx, cy, Z, acts=[z], focus=0.42, dof_k=18, fx_=f, t=t, snow_n=50)
K.cover_make(big, ['ТАКСИ —', '3000?!'], n=4, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=90)
print('cover.png')
