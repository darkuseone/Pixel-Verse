"""Cover S01E02 v2 «ГОДОВАЯ ПРЕМИЯ!»: Людмила hands Эдик the bonus envelope, he beams; lanyard plate + sticky-note title.  python3 cover.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import stage as ST
import ep02 as E
from props import kskit as K, kscast as C

t = 1.0
ST.T_NOW[0] = t
Z = 1.2; cx, cy = 480.0, 300.0
v = K.V('office', cx, cy, Z)
ly = K.at(C.lyuda, v, 300, 1840, 15.5, expr='strict', look=(0.9, 0.0), t=t, hand_n=(12.0, 40.0), prop_n=lambda sp, h: C.calc(sp, h))
ed = K.at(C.edik, v, 760, 1180, 25.0, flip=True, pin='head', near=0.99, expr='beam', mouth_=0.8, look=(-0.9, 0.1), t=t,
          hand_n=(18.0, 62.0), prop_n=lambda sp, h: C.envelope(sp, h))
big = E.shot('office', cx, cy, Z, acts=[ly, ed], t=t)
K.cover_make(big, ['ГОДОВАЯ', 'ПРЕМИЯ!'], out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=90)
print('cover.png')
