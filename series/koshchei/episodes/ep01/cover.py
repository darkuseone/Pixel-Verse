"""Cover S01E01 «ПЕНСИЮ НЕ ДАЮТ?!»: Кощей screams into window 3 of the Соцфонд (= hook text = first line = first frame).
  python3 cover.py -> cover.png + cover_grid.png (+ covers/cover_s01e01.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_kosh import make
import ep01 as E

t = 1.0
frame, _ = E.K.cu(E.C.koshchei, t, E.OFF, 652.0, 330.0, 1.35, 24.0, head=(520, 1120), light=E.K.light_office, blur=3,
                  expr='scream', mouth_=0.95, look=(0.5, 0.1), fire=1.0, hand_n=(9.0, 30.0), hand_f=(-7.0, 30.0))
E.glass(frame, 0, 0, 1080, 1920, 0.6)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['ПЕНСИЮ', 'НЕ ДАЮТ?!'], n=1, out=str(out))
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e01.png')
print(out)
