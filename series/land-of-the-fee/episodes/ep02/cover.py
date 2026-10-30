"""Cover S01E02 «$95 TO APPLY?!»: code frame (Duke roaring at the application on the tablet in the leasing office), the banknote plate on
top of the 3:4 grid zone + «Dollar Neon» title.  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from props import feecast as C
from props import feekit as K
from props.feekit import aout

OFF = K.world('leasing')
def fx_(big, v, a):
    hx, hy = aout(a, v, 'head')
    K.feathers(big, 0.45, 0.0, hx, hy - 40, n=16, seed=5)
big, a = K.cu(C.duke, 0.3, OFF, 300.0, 380.0, 1.3, 23.0, head=(430, 1030), light=K.light_apt, blur=4, extra_fx=fx_,
              expr='roar', mouth_=1.0, flop=1.0, look=(0.9, -0.6), hand_n=(22.0, 44.0),
              prop_n=lambda sp, h: C.tablet(sp, h, 0.0, 0.0, screen='form'))
K.cover_make(big, ['$95 TO APPLY?!'], n=2, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=72)
print('cover.png')
