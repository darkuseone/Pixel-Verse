"""Cover S01E03 «МАЛИНА ПО 900?!»: selfie — Прохор screams at the berry price, a handful of raspberries in the mitten.
  python3 cover.py -> cover.png + cover_grid.png (+ covers/cover_s01e03.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_taiga import make
import ep03 as E

t = 1.0
frame, _ = E.K.cu(E.C.prokhor, t, E.GLADE, 640.0, 380.0, 1.25, 25.0, head=(470, 1150), light=E.K.light_taiga2, blur=2,
                  expr='shout', mouth_=0.9, look=(0.3, 0.2), hand_n=(18.0, 42.0), prop_n=E.berries)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['МАЛИНА', 'ПО 900?!'], n=3, out=str(out))
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e03.png')
print(out)
