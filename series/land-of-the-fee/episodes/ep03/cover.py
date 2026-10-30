"""Cover S01E03 «$40 FOR A HUG?!»: code frame (Duke in a gown and a neck brace roaring in the ER, the itemised bill), banknote plate on top of
the 3:4 grid zone + «Dollar Neon» title.  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import overlays as O
from props import feecast as C
from props import feekit as K
from props.feekit import aout

ER = K.world('er')
def fx_(big, v, a):
    hx, hy = aout(a, v, 'head')
    K.feathers(big, 0.45, 0.0, hx, hy - 40, n=14, seed=7)
big, a = K.cu(C.duke, 0.3, ER, 400.0, 330.0, 1.35, 21.0, head=(470, 980), light=K.light_store, blur=4, extra_fx=fx_,
              gown=True, brace=True, expr='roar', mouth_=1.0, flop=1.0, look=(0.6, 0.9), hand_n=(22.0, 30.0), hand_f=(-16.0, 30.0))
b = K.bill_ui(['SKIN-TO-SKIN CONTACT $39.99', 'TISSUE (USED) $12'], hi=0, w=640)
O.overlay(big, b, 420, 1260, 1.0)
K.cover_make(big, ['$40 FOR A HUG?!'], n=3, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=66)
print('cover.png')
