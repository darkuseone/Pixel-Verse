"""Cover S01E02 «ONE BULB OUT?!»: night, Glenn on the stepladder, furious, the dead string in his hand; notification plate + neon title."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import stage as ST
import ep02 as E
from props import mdkit as K

t = 1.0
ST.T_NOW[0] = t
Z = 2.0; cx, cy = 742.0, 196.0
lit = 0.0
g = K.A(E.C.glenn, 712.0, 640.0, K.ws_at(640.0) * 3 * Z, flip=True, **E.gkw(t, hand_n=(14.0, 88.0), lean=-2.0,
        prop_n=lambda sp, h: E.C.light_string(sp, h, lit=0.0, t=t)))
g.P.update(expr='furious', mouth_=0.85, look=(-0.6, 0.1))
big = E.shot(cx, cy, Z, t, [g])
out = pathlib.Path(__file__).resolve().parent / 'cover.png'
K.cover_make(big, ['ONE BULB OUT?!'], out=str(out), title_size=70)
print(out)
