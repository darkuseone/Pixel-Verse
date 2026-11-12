"""Cover S01E01 «FREE PARKING?»: code frame (Vince grinning in his white convertible at the Ocean Drive sunset, Fran glowing on the
roof of The Palms), VHS-label plate on top of the 3:4 grid zone + chrome «FREE PARKING?».  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import stage as ST
import ep01 as E
from props import v86kit as K

ST.T_NOW[0] = 1.6
big = E.r_hook(1.6, 1.6)
v = E.V('ocean', 470.0 + 46.0 * 1.6, 360.0, 1.35)
K.fran(big, 900, 1330, 520, 1.6, talk=0.0, lid=0.6, look=-0.8)
K.cover_make(big, ['FREE', 'PARKING?'], n=1, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=92)
print('cover.png')
