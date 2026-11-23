"""Cover S01E06 «СОТРУДНИК ГОДА?!»: the boss proudly holding the ficus with its medal; lanyard plate + sticky-note title.  python3 cover.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import ep06 as E
import stage as ST
from kscommon import K
t = E.T0['s4'] + 0.5
ST.T_NOW[0] = t
big = E.r_hug(t, 0.5)
K.cover_make(big, ['СОТРУДНИК', 'ГОДА?!'], out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=84)
print('cover.png')
