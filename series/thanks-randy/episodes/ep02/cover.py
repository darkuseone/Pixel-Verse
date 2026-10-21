"""Cover S01E02 «GRAVY'S A LIQUID?!»: Randy screaming at Officer Patty's blue glove holding Nana's gallon of gravy over the X-ray
belt; price-tag plate on top of the 3:4 grid zone + «Price-Tag Feast» title.  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from stage import view_at
from props import randycast as C
from props import randykit as K
from props.randykit import A, wpt

AIR = K.world('airport')
Z = 1.35
v = view_at(AIR, 560.0, 400.0, Z, 180, 320)
s = 24.0
pat = A(C.patty, *wpt(v, 1250.0, 1180.0 + 60.0 * s), s, t=1.0, flip=True, expr='dead', look=(-0.9, 0.0), hand_n=(14.0, 52.0),
        prop_n=lambda sp, h: C.gravy_jug(sp, (h[0] - 1.0, h[1] - 2.0)))
big, a = K.cu(C.randy, 1.0, AIR, 560.0, 400.0, Z, s, head=(360, 1080), light=K.light_airport, blur=4, acts_after=[pat],
              expr='shout', mouth_=0.95, look=(1.0, 0.1), stache='up', hand_n=(18.0, 60.0))
K.cover_make(big, ["GRAVY'S A", 'LIQUID?!'], n=2, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=96)
print('cover.png')
