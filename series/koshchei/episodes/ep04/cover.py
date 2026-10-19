"""Cover S01E04 «БАТАРЕИ ЛЕДЯНЫЕ?!»: Кощей hugs the ice-cold radiator, an icicle on his nose (= hook).
  python3 cover.py -> cover.png + cover_grid.png (+ covers/cover_s01e04.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_kosh import make
import ep04 as E

frame = E.r_hook(1.0, 1.0)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['БАТАРЕИ', 'ЛЕДЯНЫЕ?!'], n=4, out=str(out))
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e04.png')
print(out)
