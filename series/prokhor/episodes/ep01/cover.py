"""Cover S01E01 «9 000 ЗА ТЕПЛО?!»: Прохор in the frozen izba screaming at the heating bill (= hook text = first line = first frame).
  python3 cover.py -> cover.png + cover_grid.png (+ covers/cover_s01e01.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_taiga import make
import ep01 as E

t = 0.6
def f(big, v, a):
    hx, hy = E.aout(a, v, 'mouth')
    E.K.breath(big, hx + 30, hy + 10, t, 1.2, scale=1.8, period=1.1)
frame, _ = E.K.cu(E.C.prokhor, t, E.IZBA, 600.0, 330.0, 1.35, 25.0, head=(400, 1130), light=E.K.light_izba, blur=3, extra_fx=f,
                  expr='shout', mouth_=0.9, look=(0.8, 0.0), frost=1.0, hand_n=(15.0, 41.0), prop_n=E.bill_prop())
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['9 000 ЗА', 'ТЕПЛО?!'], n=1, out=str(out))
(P.series(E.SLUG) / 'covers').mkdir(exist_ok=True)
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e01.png')
print(out)
