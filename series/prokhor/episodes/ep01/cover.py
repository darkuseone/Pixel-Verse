"""Cover S01E01 v2 «9 000 ЗА ТЕПЛО?!»: selfie — Прохор shakes the heating bill at his phone in front of his snowy cabin
(= hook text = first line = first frame).  python3 cover.py -> cover.png + cover_grid.png (+ covers/cover_s01e01.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_taiga import make
import ep01 as E

t = 0.6
def f(big, v, a):
    hx, hy = E.aout(a, v, 'mouth')
    E.K.breath(big, hx + 30, hy + 10, t, 1.2, scale=1.8, period=1.1)
frame, _ = E.K.cu(E.C.prokhor, t, E.PORCH, 380.0, 330.0, 1.25, 25.0, head=(340, 1110), light=E.K.light_porch, blur=2, extra_fx=f,
                  expr='shout', mouth_=0.9, look=(0.6, 0.0), hand_n=(17.0, 44.0), prop_n=E.bill_prop())
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['9 000 ЗА', 'ТЕПЛО?!'], n=1, out=str(out))
(P.series(E.SLUG) / 'covers').mkdir(exist_ok=True)
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e01.png')
print(out)
