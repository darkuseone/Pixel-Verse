"""Cover S01E02 «ПРЕМИИ НЕ БУДЕТ?!»: the cash window — Людмила behind the glass with the «ОТКАЗАНО» stamp, Эдик in shock up front with
his calculator; lanyard-badge plate + sticky-note title.  python3 cover.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import stage as ST
import ep02 as E
from props import kskit as K, kscast as C

t = 1.2
ST.T_NOW[0] = t
Z = 1.15; cx, cy = 620.0, 330.0
v = K.V('kassa', cx, cy, Z)
ly = K.at(C.lyuda, v, 720, 1040, 16.0, pin='head', near=0.99, expr='strict', look=(0.6, -0.2), t=t, hand_n=(10.0, 44.0))
ed = K.at(C.edik, v, 330, 1330, 26.0, pin='head', near=0.99, expr='shock', mouth_=0.7, look=(0.9, 0.2), t=t, sweat=1.0,
          hand_n=(18.0, 58.0), prop_n=lambda sp, h: C.calc(sp, h))
def f(big, v_):
    E.glass(big, v_)
    E.stamp_fx(big, 740, 1230, t, 0.0)
big = K.shot('kassa', cx, cy, Z, acts=[ly, ed], t=t, dof_k=18, fx_=f)
K.cover_make(big, ['ПРЕМИИ', 'НЕ БУДЕТ?!'], out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=92)
print('cover.png')
