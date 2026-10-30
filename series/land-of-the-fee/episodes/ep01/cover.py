"""Cover S01E01 «REPRESENTATIVE!!»: code frame (Duke roaring into his phone at the kitchen table, feathers flying, Fee-Bee smiling on the
screen), the banknote plate on top of the 3:4 grid zone + «Dollar Neon» title.  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from props import feecast as C
from props import feekit as K
from props.feekit import aout

APT = K.world('apartment')
def fx_(big, v, a):
    hx, hy = aout(a, v, 'head')
    K.feathers(big, 0.45, 0.0, hx, hy - 40, n=16, seed=4)
big, a = K.cu(C.duke, 0.3, APT, 650.0, 330.0, 1.35, 23.0, head=(430, 1180), light=K.light_apt, blur=4, extra_fx=fx_,
              expr='roar', mouth_=1.0, flop=1.0, tremble=0.0, look=(0.9, -0.5), hand_n=(21.0, 47.0),
              prop_n=lambda sp, h: C.phone(sp, h, 0.0, 0.0))
K.cover_make(big, ['REPRESENTATIVE!!'], n=1, out=str(pathlib.Path(__file__).parent / 'cover.png'))
print('cover.png')
