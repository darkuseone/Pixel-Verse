"""Cover S01E05: Death frozen as a yard decoration, a ghost kid poking him + «DEATH PLAYS / DECORATION?».
  python3 cover.py   -> cover.png (+ series/grim-ride/covers/cover_s01e05.png)"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import shutil
import ep05 as E
import covergen_grim as CG

big = E.r_hook(0.45, 0.45)
here = pathlib.Path(__file__).parent
CG.make(big, ['DEATH PLAYS', 'DECORATION?'], n=5, out=str(here / 'cover.png'), title_y=150, plate_y=1440, title_size=72)
dst = here.parents[1] / 'covers' / 'cover_s01e05.png'
shutil.copy(here / 'cover.png', dst)
print(dst)
