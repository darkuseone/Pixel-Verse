"""Cover S01E05 «ROOF LOCKED?»: Vince in the rain holding the game over his head in his open convertible (code frame)."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common as CM
import stage as ST
import ep05 as E
from props import v86kit as K
ST.T_NOW[0] = 1.2
big = E.r_hook(1.2, 1.2)
K.cover_make(big, ['ROOF', 'LOCKED?'], n=5, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=100)
print('cover.png')
