"""Cover S01E02 «ЗВОНЯТ ИЗ БАНКА?!»: Кощей with the ringing push-button phone at his ear (= hook text = first line = first frame).
  python3 cover.py -> cover.png + cover_grid.png (+ covers/cover_s01e02.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_kosh import make
import ep02 as E

t = 1.0
frame, _ = E.K.cu(E.C.koshchei, t, E.FLAT, 600.0, 330.0, 1.3, 24.0, head=(520, 1130), light=E.K.light_flat, blur=3, pre_fx=E.flat_fx(t),
                  expr='shock', mouth_=0.6, look=(-0.3, 0.2), hand_f=(-7.0, 63.0), prop_f=E.phone_at_ear, hand_n=(9.0, 30.0))
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['ЗВОНЯТ', 'ИЗ БАНКА?!'], n=2, out=str(out))
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e02.png')
print(out)
