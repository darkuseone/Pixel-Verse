"""Cover S01E06 «СЛАДОСТЬ ИЛИ ГАДОСТЬ?!»: trick-or-treaters at door 13, Кощей in shock (= hook).
  python3 cover.py -> cover.png + cover_grid.png (+ covers/cover_s01e06.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_kosh import make
import ep06 as E

frame = E.r_hook(1.0, 1.0)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ["СЛАДОСТЬ", "ИЛИ ГАДОСТЬ?!"], n=6, title_size=76, out=str(out))
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e06.png')
print(out)
