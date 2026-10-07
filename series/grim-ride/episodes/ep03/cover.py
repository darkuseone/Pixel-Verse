"""Cover S01E03: the endless trick-or-treat line to Harold's door, Death at the end with a pillowcase + «FULL-SIZE / BAR HOUSE?».
  python3 cover.py   -> cover.png (+ series/grim-ride/covers/cover_s01e03.png)"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import shutil
import ep03 as E
import covergen_grim as CG

big = E.r_hook(0.5, 0.5)
here = pathlib.Path(__file__).parent
CG.make(big, ['FULL-SIZE', 'BAR HOUSE?'], n=3, out=str(here / 'cover.png'), title_y=150, plate_y=1440)
dst = here.parents[1] / 'covers' / 'cover_s01e03.png'
shutil.copy(here / 'cover.png', dst)
print(dst)
