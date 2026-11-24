"""Cover S01E04 «$38 TO SHIP A MUG?!»: Glenn furious at the post office counter with the $8 mug; plate + neon title."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import stage as ST
import ep04 as E
from props import mdkit as K, mdcast as C

t = 1.0
ST.T_NOW[0] = t
Z = 2.1; cx, cy = E.PG[0] + 6.0, 400.0
g = K.A(C.glenn, E.PG[0], E.PG[1], K.ws_at(E.PG[1], 'postoffice') * 3 * Z, flip=True,
        **E.gkw(t, hand_n=(14.0, 90.0), prop_n=lambda sp, h: E._mug_at(sp, *h), lean=-2.0))
g.P.update(expr='furious', mouth_=0.85, look=(-0.6, 0.1))
big = E.shot('postoffice', cx, cy, Z, t, [g])
out = pathlib.Path(__file__).resolve().parent / 'cover.png'
K.cover_make(big, ['$38 TO SHIP', 'A MUG?!'], out=str(out), title_size=80)
print(out)
