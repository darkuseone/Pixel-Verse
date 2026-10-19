"""Cover S01E05 «СВЕТ ОТКЛЮЧАТ?!»: Галина with the bolt cutters at the box, Кощей with a zucchini lantern (= hook).
  python3 cover.py -> cover.png + cover_grid.png (+ covers/cover_s01e05.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_kosh import make
import ep05 as E

frame = E.r_hook(1.0, 1.0)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ["СВЕТ", "ОТКЛЮЧАТ?!"], n=5, out=str(out))
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e05.png')
print(out)
