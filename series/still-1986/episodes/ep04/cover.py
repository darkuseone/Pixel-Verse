"""Cover S01E04 «SICK DAY?»: Vince fake-coughing into the phone in the midnight line at BYTE BUY (code frame) + VHS plate + chrome title."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common as CM
import stage as ST
import ep04 as E
from props import v86kit as K
ST.T_NOW[0] = 1.6
big = E.r_hook(1.6, 1.6)
K.fran(big, 880, 1250, 420, 1.6, lid=0.6, look=-0.8)
K.cover_make(big, ['SICK', 'DAY?'], n=4, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=110)
print('cover.png')
