"""Cover S01E03 «STILL FROZEN?!»: 3 AM, Randy blasting a hair dryer at Tom, ice flying; price-tag plate + title.
  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from stage import view_at
from props import randycast as C
from props import randykit as K
from props.randykit import A, wpt
import ep03 as E

v = view_at(E.KIT, 560.0, 330.0, 1.35, 180, 320)
tom = A(C.tom, *wpt(v, 850.0, 1700.0), 20.0, t=1.0, expr='dead', look=(-0.6, 0.2))
big, a = K.cu(C.randy, 1.0, E.KIT, 560.0, 330.0, 1.35, 23.0, head=(330, 1060), light=E.light_kit, blur=4, acts_after=[tom],
              expr='shout', mouth_=0.95, sweat=1.0, look=(1.0, 0.2), mitt=False, hand_n=(19.0, 62.0), prop_n=lambda sp, h: C.hair_dryer(sp, h))
nx, ny = K.aout(a, v, 'hand')
E.dryer_wind(big, nx + 200, ny - 40, 0.4)
K.cold_vapor(big, 880, 1430, 0.5, 1.0, 1.0)
K.cover_make(big, ['STILL', 'FROZEN?!'], n=3, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=112)
print('cover.png')
