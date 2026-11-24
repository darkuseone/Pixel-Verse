"""Cover S01E03 «$25 LIMIT?!»: Glenn furious with Kyle's scratch-off in the office break room; plate + neon title."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import stage as ST
import ep03 as E
from props import mdkit as K, mdcast as C

t = 1.0
ST.T_NOW[0] = t
Z = 2.1; cx, cy = E.GX - 4.0, 380.0
g = E.glenn(t, Z, hand_n=(14.0, 92.0), prop_n=C.scratch_off, lean=-2.0)
g.P.update(expr='furious', mouth_=0.85, look=(-0.6, 0.1))
big = E.shot(cx, cy, Z, t, [g])
out = pathlib.Path(__file__).resolve().parent / 'cover.png'
K.cover_make(big, ['$25 LIMIT?!'], out=str(out), title_size=88)
print(out)
