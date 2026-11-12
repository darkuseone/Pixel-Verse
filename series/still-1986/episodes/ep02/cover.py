"""Cover S01E02 «$40... RIGHT?»: Vince fanning cash at the NEON PALACE box office (code frame) + VHS plate + chrome title."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common as CM
import stage as ST
import ep02 as E
from props import v86kit as K
ST.T_NOW[0] = 2.2
big = E.r_hook(2.2, 2.2)
K.fran(big, 880, 1250, 420, 2.2, lid=0.6, look=-0.8)
K.cover_make(big, ['$40...', 'RIGHT?'], n=2, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=96)
print('cover.png')
