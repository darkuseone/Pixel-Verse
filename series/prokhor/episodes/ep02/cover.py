"""Cover S01E02 «ПВЗ ЗА 40 КМ?!»: selfie — Прохор screams at the app ping (= hook text = first line = first frame).
  python3 cover.py -> cover.png + cover_grid.png (+ covers/cover_s01e02.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_taiga import make
import ep02 as E

t = 1.0
frame, _ = E.K.cu(E.C.prokhor, t, E.PORCH, 420.0, 360.0, 1.25, 25.0, head=(470, 1150), light=E.K.light_porch, blur=2,
                  expr='shout', mouth_=0.9, look=(0.2, 0.3), hand_n=(18.0, 40.0), prop_n=E.box_prop)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['ПВЗ ЗА', '40 КМ?!'], n=2, out=str(out))
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e02.png')
print(out)
