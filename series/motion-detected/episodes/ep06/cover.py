"""Cover S01E06 «FINAL ATTEMPT!»: dawn, Glenn in the sleeping bag on the porch, Doris beside; plate + neon title."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import stage as ST
import ep06 as E
from props import mdkit as K, mdcast as C

t = 1.0
ST.T_NOW[0] = t
Z = 1.8; cx, cy = E.GX - 20.0, 360.0
g = E.glenn(t, Z, y=E.FEET + 2, seated=True, oy=-18.0, hand_n=(14.0, 52.0), hand_f=(10.0, 46.0))
g.P.update(expr='furious', mouth_=0.8, look=(-0.4, 0.1))
bag = K.A(C.sleeping_bag, E.GX - 4.0, E.FEET + 4, K.ws_at(E.FEET) * 1.5 * 3 * Z, flip=True, rim=None)
bag.near = 0.99
big = E.shot(cx, cy, Z, t, [E.doris_act(t, Z), g, bag])
out = pathlib.Path(__file__).resolve().parent / 'cover.png'
K.cover_make(big, ['FINAL ATTEMPT!'], out=str(out), title_size=74)
print(out)
