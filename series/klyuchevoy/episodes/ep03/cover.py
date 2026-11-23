"""Cover S01E03 «КОРПОРАТИВА НЕ БУДЕТ!»: the boss shouting with the phone «ТЁЩА»; lanyard plate + sticky-note title.  python3 cover.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import ep03 as E
import stage as ST
from kscommon import K
ST.T_NOW[0] = 0.8
big = E.r_hook(0.8, 0.8)
K.cover_make(big, ['КОРПОРАТИВА', 'НЕ БУДЕТ!'], out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=74)
print('cover.png')
