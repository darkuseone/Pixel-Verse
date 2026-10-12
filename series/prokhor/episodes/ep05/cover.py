"""Cover S01E05 «ШТРАФ ЗА КОСТЁР?!»: selfie — the fine slapped onto Прохор's forehead (= hook text = first line = first frame).
  python3 cover.py -> cover.png + cover_grid.png (+ covers/cover_s01e05.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_taiga import make
import ep05 as E

t = 1.0
def f(big, v, a): E.slip_on(big, v, a, 1.0, 0.0, dx=2.0, dy=9.0, s=0.8)
frame, _ = E.K.cu(E.C.prokhor, t, E.TAIGA, 640.0, 470.0, 1.25, 25.0, head=(500, 1180), light=E.K.light_taiga2, blur=2, extra_fx=f,
                  expr='shout', mouth_=0.9, look=(0.2, 0.3), hand_n=(20.0, 30.0))
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['ШТРАФ ЗА', 'КОСТЁР?!'], n=5, out=str(out))
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e05.png')
print(out)
