"""Cover S01E05 «$30 FOR FOOTBALL?!»: Randy screaming at the big TV paywall (SUBSCRIBE TO WATCH $29.99/MO); price-tag plate + title.
  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from props import randycast as C
from props import randykit as K
import ep05 as E

big, a = K.cu(C.randy, 1.0, E.LIV, 300.0, 175.0, 1.15, 22.0, head=(800, 1180), light=lambda v_: E.light_liv(v_, 1.0), flip=True,
              pre_fx=lambda b, v_: E.tv(b, v_, 'paywall', 0.3), expr='shout', mouth_=0.95, look=(1.0, 0.0), stache='up',
              hand_n=(18.0, 62.0), prop_n=lambda sp, h: C.remote(sp, h), mitt=False)
K.cover_make(big, ['$30 FOR', 'FOOTBALL?!'], n=5, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=92)
print('cover.png')
