"""Cover S01E02: Florida Man shrieking through the deli glass at the «SUB $14.99» sign (code frame, no AI)
+ title «$15 FOR / A SUB?!» + booking letterboard plate.   python3 cover.py   -> cover.png (+ series/florida-man/covers/cover_s01e02.png)"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import shutil
import ep02 as E
import covergen_fm as CG

big = E.r_hook(0.9, 0.9)
here = pathlib.Path(__file__).parent
CG.make(big, ['$15 FOR', 'A SUB?!'], n=2, out=str(here / 'cover.png'), title_y=200, plate_y=1690)
dst = here.parents[1] / 'covers' / 'cover_s01e02.png'
shutil.copy(here / 'cover.png', dst)
print(dst)
