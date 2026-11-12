"""Cover S01E03 «BOAT DAY?»: Vince on the marina dock at sunset (code frame) + VHS plate + chrome title."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common as CM
import stage as ST
import ep03 as E
from props import v86kit as K
ST.T_NOW[0] = 2.4
big = E.r_hook(2.4, 2.4)
K.fran(big, 880, 1250, 420, 2.4, lid=0.6, look=-0.8)
K.cover_make(big, ['BOAT', 'DAY?'], n=3, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=110)
print('cover.png')
