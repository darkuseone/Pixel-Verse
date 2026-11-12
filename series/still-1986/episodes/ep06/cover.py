"""Cover S01E06 «FINALLY?»: Vince holding the game in his studio, the CRT behind (code frame) + VHS plate + chrome title."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common as CM
import stage as ST
import ep06 as E
from props import v86kit as K
ST.T_NOW[0] = 1.5
big = E.r_hook(1.5, 1.5)
K.fran(big, 880, 1250, 420, 1.5, lid=0.6, look=-0.8)
K.cover_make(big, ['FINALLY?'], n=6, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=100)
print('cover.png')
