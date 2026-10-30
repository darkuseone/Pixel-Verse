"""Cover S01E06 «$89 TO SIT?!»: code frame (Duke roaring at the Penny Air fare breakdown at the gate), banknote plate on top of the 3:4
grid zone + «Dollar Neon» title.  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import overlays as O
from props import feecast as C
from props import feekit as K
from props.feekit import aout

GATE = K.world('gate')
def fx_(big, v, a):
    hx, hy = aout(a, v, 'head')
    K.feathers(big, 0.45, 0.0, hx, hy - 40, n=14, seed=21)
big, a = K.cu(C.duke, 0.3, GATE, 200.0, 360.0, 1.35, 22.0, head=(400, 1160), light=K.light_mall, blur=4, extra_fx=fx_,
              expr='roar', mouth_=1.0, flop=1.0, look=(0.9, 0.4), hand_n=(24.0, 34.0))
b = K.bill_ui(['BASIC FARE   $19', 'SEAT         $89', 'CARRY-ON     $65', 'BREATHING    $5'], total='TOTAL $178', title='PENNY AIR',
              hi=1, w=400)
O.overlay(big, b, 1080 - b.shape[1] - 24, 1340, 1.0)
K.cover_make(big, ['$89 TO SIT?!'], n=6, out=str(pathlib.Path(__file__).parent / 'cover.png'))
print('cover.png')
