"""Cover S01E05 «IN-LAWS IN 1 HOUR?!»: Glenn panicking in the messy living room with the phone; plate + neon title."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import stage as ST
import ep05 as E
from props import mdkit as K, mdcast as C

t = 1.0
ST.T_NOW[0] = t
Z = 2.0; cx, cy = 640.0, 212.0
g = E.glenn(t, Z, 620.0, 620.0, hand_n=(14.0, 92.0), prop_n=C.phone, lean=-2.0)
g.P.update(expr='panic', mouth_=0.9, look=(-0.6, 0.1))
big = E.shot(cx, cy, Z, t, E.mess(t, Z) + [g])
out = pathlib.Path(__file__).resolve().parent / 'cover.png'
K.cover_make(big, ['IN-LAWS IN', '1 HOUR?!'], out=str(out), title_size=84)
print(out)
