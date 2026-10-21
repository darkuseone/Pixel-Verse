"""Cover S01E01 «$89 TURKEY?!»: code frame (Randy screaming at the price, Tom deadpan below with his $89.99 label, the kiosk screen),
price-tag plate on top of the 3:4 grid zone + «Price-Tag Feast» title.  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from stage import view_at
from props import randycast as C
from props import randykit as K
from props.randykit import A, wpt

STORE = K.world('store')
Z = 1.3
v = view_at(STORE, 700.0, 470.0, Z, 180, 320)
s = 24.0
kio = A(C.kiosk, *wpt(v, 990.0 + 6.6 * s, 960.0 + 52.6 * s), s, t=1.0, screen='price', part='back')
big, a = K.cu(C.randy, 1.0, STORE, 700.0, 470.0, Z, s, head=(400, 1010), light=K.light_store, blur=5, acts_after=[kio],
              expr='shout', mouth_=0.95, tremble=0.0, look=(1.0, -0.1), hand_n=(19.0, 66.0), stache='up')
tom = A(C.tom, *wpt(v, 740.0, 1650.0), 19.0, t=1.0, expr='dead', look=(-0.6, 0.2))
tom(big, v, K.light_store(v))
K.cold_vapor(big, 780, 1330, 0.6, 1.0, 1.0)
K.cover_make(big, ['$89', 'TURKEY?!'], n=1, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=112)
print('cover.png')
