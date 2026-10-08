"""Cover S01E04: Death in the headlights of the masked e-bike gang in the gangway + «DEATH BUYS / A DONGLE?».
  python3 cover.py   -> cover.png (+ series/grim-ride/covers/cover_s01e04.png)"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import shutil
import ep04 as E
import covergen_grim as CG

big = E.r_gang(2.4, 0.5)
here = pathlib.Path(__file__).parent
CG.make(big, ['DEATH BUYS', 'A DONGLE?'], n=4, out=str(here / 'cover.png'), title_y=150, plate_y=1440)
dst = here.parents[1] / 'covers' / 'cover_s01e04.png'
shutil.copy(here / 'cover.png', dst)
print(dst)
