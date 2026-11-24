"""Cover S01E01 «I WAS HOME!»: Glenn on the porch at dusk, furious, waving the SORRY WE MISSED YOU tag, Doris with the DND moon;
notification plate «● MOTION DETECTED» + neon title (profile grid: plate at y≈250, nothing important below 1520).  python3 cover.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import stage as ST
import ep01 as E
from props import mdkit as K, mdcast as C

t = 1.0
ST.T_NOW[0] = t
E.sp_t[0] = t
Z = 1.45; cx, cy = 436.0, 250.0
g = E.glenn_act(E.GX, E.FEET, t, Z, hand_n=(15.0, 96.0), prop_n=E.tag_n, lean=-2.0)
g.P.update(expr='furious', mouth_=0.85, look=(-0.6, 0.1))
big = E.shot('porch', cx, cy, Z, acts=[E.doris_act(t, Z, dnd=True), g], t=t)
out = pathlib.Path(__file__).resolve().parent / 'cover.png'
K.cover_make(big, ['I WAS HOME!'], out=str(out), title_size=88)
print(out)
