"""Cover S01E02 «СМЕНКУ ЗАБЫЛ!»: Жора in the alaska + family shorts in the zinc basin at the top of the slope, the string bag up,
yelling; the road-sign plate on top of the 3:4 grid zone + the «аляска» title.  python3 cover.py -> cover.png + cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import stage as ST
import ep02 as E
from props import zamkit as K, zamcast as C

t = 1.2
ST.T_NOW[0] = t
Z = 3.1
x, y = 470.0, 300.0
v = K.V('slope', x + 6, y - 75, Z)
S = K.WS['slope'] * 3 * v.Z * 1.25
z = K.A(C.zhora, x, y + E.sitoff(S, v), S, t=t, expr='yelling', mouth_=0.9, look=(0.8, 0.2), blink=False, undies=True, sit=1.0,
        hand_n=(22.0, 70.0), prop_n=E.bag('pelmeni'), hand_f=(-12.0, 34.0))
z.near = 0.99
tz = K.A(C.taz, x + 6, y + 4, S * 1.1, t=t); tz.near = 0.99
big = K.shot('slope', K.light_morning, x + 6, y - 75, Z, acts=[z, tz], t=t, focus=0.9, dof_k=0, snow_n=50)
K.cover_make(big, ['СМЕНКУ', 'ЗАБЫЛ!'], n=2, out=str(pathlib.Path(__file__).parent / 'cover.png'), title_size=92)
print('cover.png')
