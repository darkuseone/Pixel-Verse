"""Cover S01E03 «РЕМОНТ В 7 УТРА?!»: Кощей bolt upright in his coffin, a drill bit out of the ceiling at his crown (= hook).
  python3 cover.py -> cover.png + cover_grid.png (+ covers/cover_s01e03.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_kosh import make
import ep03 as E

t = 1.0
frame = E.r_hook(t, t)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['РЕМОНТ', 'В 7 УТРА?!'], n=3, out=str(out))
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e03.png')
print(out)
