"""Cover S01E04 «К ВРАЧУ ЧЕРЕЗ МЕСЯЦ?!»: selfie — Прохор with a balloon cheek screams at the polyclinic app (= hook text = first line).
  python3 cover.py -> cover.png + cover_grid.png (+ covers/cover_s01e04.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_taiga import make
import ep04 as E

t = 1.0
frame, _ = E.K.cu(E.C.prokhor, t, E.BIRCH, 760.0, 400.0, 1.2, 25.0, head=(500, 1150), light=E.K.light_taiga2, blur=2,
                  expr='shout', mouth_=0.9, look=(0.2, 0.3), swollen=1.0, hand_n=(20.0, 40.0), prop_n=E.phone_prop)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['К ВРАЧУ', 'ЧЕРЕЗ МЕСЯЦ?!'], n=4, out=str(out), title_size=66)
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e04.png')
print(out)
