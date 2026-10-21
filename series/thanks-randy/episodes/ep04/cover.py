"""Cover S01E04 «RANDY, NO!»: Randy in welding goggles lowers frozen Tom on a hook into the boiling Fry-Hard 3000; price-tag plate + title.
  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from stage import view_at
from props import randycast as C
from props import randykit as K
from props.randykit import A, wpt
import ep04 as E

v = view_at(E.YARD, 400.0, 420.0, 1.3, 180, 320)
fr = A(C.fryer, *wpt(v, 860.0, 1900.0), 22.0, t=1.0)
tom = A(C.tom, *wpt(v, 830.0, 1500.0), 20.0, t=1.0, expr='dead', look=(-0.7, 0.3))
big, a = K.cu(C.randy, 1.0, E.YARD, 400.0, 420.0, 1.3, 22.0, head=(330, 1060), light=E.light_yard, blur=4, acts_after=[fr, tom],
              expr='proud', mouth_=0.0, goggles=True, look=(1.0, 0.4), stache='up', hand_n=(19.0, 58.0),
              prop_n=lambda sp, h: C.hook_pole(sp, h, 20.0))
K.cold_vapor(big, 860, 1300, 0.5, 1.0, 1.0)
K.cover_make(big, ['RANDY,', 'NO!'], n=4, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=124)
print('cover.png')
