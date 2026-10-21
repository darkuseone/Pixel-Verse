"""Cover S01E06 «$199 TV?!»: Randy screaming against the frosty Best Bye door, the «65" $199» pyramid behind; price-tag plate + title.
  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from props import randycast as C
from props import randykit as K
import ep06 as E


def ex(big, v, a):
    mx, my = K.aout(a, v, 'mouth')
    E.breath(big, mx + 40, my, 0.4, 1.0, 1.6)
    E.frost(big, 'right', 0.7)


big, a = K.cu(C.randy, 1.0, E.OUT, 600.0, 470.0, 1.25, 21.0, head=(420, 1160), light=E.light_out, blur=3, extra_fx=ex,
              expr='shout', mouth_=0.95, tremble=0.0, look=(1.0, -0.1), stache='up', hand_n=(22.0, 72.0))
K.cover_make(big, ['$199 TV?!'], n=6, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=104)
print('cover.png')
