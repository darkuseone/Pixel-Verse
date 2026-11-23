"""Cover S01E05 «НЕ ТОТ ЧАТ!»: Эдик in horror with the phone; lanyard plate + sticky-note title.  python3 cover.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent)); sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import ep05 as E
import stage as ST
from kscommon import K
ST.T_NOW[0] = 0.6
big = E.KC.cu(E.FC, 'edik', E.C.edik, 0.6, 0.6, base=(0.0, -0.4), y=1150, sweat=2.0, hand_n=(18.0, 46.0),
              prop_n=lambda sp, h: E.C.phone(sp, h, 'ЧАТ'))
K.cover_make(big, ['НЕ ТОТ', 'ЧАТ!'], out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=110)
print('cover.png')
