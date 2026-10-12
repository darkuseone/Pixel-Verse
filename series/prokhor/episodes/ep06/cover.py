"""Cover S01E06 «МОРЕ ЗА 200 ТЫСЯЧ?!»: selfie — Прохор screams at the travel app (= hook text = first line = first frame).
  python3 cover.py -> cover.png + cover_grid.png (+ covers/cover_s01e06.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_taiga import make
import ep06 as E

t = 1.0
frame, _ = E.K.cu(E.C.prokhor, t, E.LAKE, 380.0, 470.0, 1.2, 25.0, head=(500, 1180), light=E.K.light_taiga2, blur=2,
                  expr='shout', mouth_=0.9, look=(0.2, 0.3), hand_n=(20.0, 40.0), prop_n=lambda sp, h: E.C.phone(sp, h, rec=False))
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['МОРЕ ЗА', '200 ТЫСЯЧ?!'], n=6, out=str(out), title_size=72)
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e06.png')
print(out)
