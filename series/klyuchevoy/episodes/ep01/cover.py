"""Cover S01E01 «ЗАДЕРЖИСЬ НА 5 МИНУТ!»: code frame (17:59 — the boss in his coat at his door, Эдик in coat + hat in shock up front,
the clock over the door), the lanyard-badge plate on top of the 3:4 grid zone + sticky-note title.  python3 cover.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import stage as ST
import ep01 as E
from props import kskit as K, kscast as C

t = 1.2
ST.T_NOW[0] = t
Z = 1.0; cx, cy = 236.0, 236.0
v = K.V('office', cx, cy, Z)
sh = K.at(C.shef, v, 250, 1760, 11.0, expr='bark', mouth_=0.8, look=(0.9, 0.0), t=t, coat=True, hand_n=(26.0, 66.0),
                   prop_f=lambda sp, h: C.briefcase(sp, h))
ed = K.at(C.edik, v, 790, 1240, 26.0, flip=True, pin='head', near=0.99, expr='shock', mouth_=0.6, look=(0.9, 0.1), t=t, coat=True, hat=True)
big = K.shot('office', cx, cy, Z, acts=[sh, ed], t=t, dof_k=18, clock='17:59')
K.cover_make(big, ['ЗАДЕРЖИСЬ', 'НА 5 МИНУТ!'], out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=84)
print('cover.png')
