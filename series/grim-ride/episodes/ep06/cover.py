"""Cover S01E06: Death and Harold on the hilltop under a 1:59 AM clock + «DEATH'S LAST / MINUTE?».
  python3 cover.py   -> cover.png (+ series/grim-ride/covers/cover_s01e06.png)"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import shutil
import ep06 as E
import covergen_grim as CG

big = E.r_hook(0.9, 0.9)
here = pathlib.Path(__file__).parent
CG.make(big, ["DEATH'S LAST", 'MINUTE?'], n=6, out=str(here / 'cover.png'), title_y=150, plate_y=1650, title_size=72)
dst = here.parents[1] / 'covers' / 'cover_s01e06.png'
shutil.copy(here / 'cover.png', dst)
print(dst)
