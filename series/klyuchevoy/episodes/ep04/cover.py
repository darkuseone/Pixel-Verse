"""Cover S01E04 «ОТПУСК В ФЕВРАЛЕ?!»: Людмила with the chart, Эдик outraged; lanyard plate + sticky-note title.  python3 cover.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import ep04 as E
import stage as ST
from kscommon import K, C
t = 1.0
ST.T_NOW[0] = t
Z = 1.2; cx, cy = 480.0, 300.0
v = K.V('office', cx, cy, Z)
ly = K.at(C.lyuda, v, 300, 1840, 15.5, expr='strict', look=(0.9, 0.0), t=t, hand_n=(12.0, 40.0), prop_n=lambda sp, h: C.clipboard(sp, h))
ed = K.at(C.edik, v, 760, 1180, 25.0, flip=True, pin='head', near=0.99, expr='bark', mouth_=0.8, look=(-0.9, 0.1), t=t,
          hand_n=(18.0, 64.0), hand_f=(-6.0, 56.0))
big = E.shot('office', cx, cy, Z, acts=[ly, ed], t=t)
K.cover_make(big, ['ОТПУСК', 'В ФЕВРАЛЕ?!'], out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=86)
print('cover.png')
