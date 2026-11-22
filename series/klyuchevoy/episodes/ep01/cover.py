"""Cover S01E01 v2 «ЗАДЕРЖИСЬ НА 5 МИНУТ!» (variant A; KS_VAR=B -> episodes/ep01b/cover.png): 17:59 — the boss in his doorway,
Эдик in coat + hat in shock up front; lanyard-badge plate + sticky-note title.  python3 cover.py"""
import os, sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import stage as ST
import ep01 as E
from props import kskit as K, kscast as C

t = 1.0
ST.T_NOW[0] = t
Z = 1.0; cx, cy = 220.0, 250.0
v = E.V('office', cx, cy, Z)
sh = K.at(C.shef, v, 250, 1760, 11.0, expr='bark', mouth_=0.8, look=(0.9, 0.1), t=t, coat=True, prop_f=lambda sp, h: C.briefcase(sp, h))
ed = K.at(C.edik, v, 790, 1250, 25.0, flip=True, pin='head', near=0.99, expr='shock', mouth_=0.6, look=(-0.9, 0.0), t=t, coat=True, hat=True)
big = E.shot('office', cx, cy, Z, acts=[sh, ed], t=t, clock='17:59', pre=lambda b, v_: E.door_open(b, v_, 1.0))
out = pathlib.Path(__file__).resolve().parents[1] / ('ep01' if E.VAR == 'A' else 'ep01b') / 'cover.png'
K.cover_make(big, ['ЗАДЕРЖИСЬ', 'НА 5 МИНУТ!'], out=str(out), title_size=84)
print(out)
