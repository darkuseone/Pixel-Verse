"""Cover S01E01 «ОСТАВЛЕН У ДВЕРИ?!»: code frame (Жора yelling in his open window, snow level with the sill, the ОЗНОБ push on
the phone), the road-sign plate on top of the 3:4 grid zone + the «аляска» title.  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import overlays as O
import stage as ST
import ep01 as E
from props import zamkit as K, zamcast as C

t = 1.2
ST.T_NOW[0] = t
Z, cx, cy = 1.32, 712.0, 330.0
v = K.V('facade', cx, cy, Z)
S = K.S_of(v, 'facade')
wx, wy = E.feet_for_head(v, 400, 1250, S)
z = K.A(C.zhora, wx, wy, S, t=t, expr='outraged', mouth_=0.9, look=(0.7, -0.2), blink=False, hand_n=(18.0, 60.0), prop_n=E.phone_n, frost=0.3)
z.near = E.NEAR_ROOM
def f(big, _):
    ph = K.push_screen(1.0, w=440, h=720, t_push=0.0)
    O.overlay(big, ph, 650, 840, 1.0)
big = K.shot('facade', K.light_window, cx, cy, Z, acts=[z], focus=0.42, dof_k=18, fx_=f, t=t, snow_n=50)
K.cover_make(big, ['ОСТАВИЛИ', 'У ДВЕРИ?!'], n=1, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=86)
print('cover.png')
