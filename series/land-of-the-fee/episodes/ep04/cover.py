"""Cover S01E04 «$400 A MONTH?!»: code frame (Duke crammed in the tiny hatchback roaring, head through the roof), banknote plate on top of the
3:4 grid zone + «Dollar Neon» title.  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from stage import view_at
from props import feecast as C
from props import feekit as K
from props.feekit import A, wpt

ST_ = K.world('street')
v = view_at(ST_, 600.0, 560.0, 1.4, 180, 320)
cs = 40.0
duke = A(C.duke, *wpt(v, 620 - 2 * cs, 2540 - 5 * cs), cs * 0.5, t=0.3, legs=False, expr='roar', mouth_=1.0, flop=1.0, look=(-0.6, 0.6),
         hand_n=(34.0, 40.0), hand_f=(-30.0, 40.0))
car = A(C.hatchback, *wpt(v, 620, 2540), cs, t=0.3)
def pre(big, v_): big[:] = K.dof(big, 5)
big = K.shot(ST_, K.light_mall, 600.0, 560.0, 1.4, acts=[duke, car], pre=pre)
K.cover_make(big, ['$400 A MONTH?!'], n=4, out=str(pathlib.Path(__file__).parent / 'cover.png'))
print('cover.png')
