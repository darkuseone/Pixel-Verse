"""Cover S01E05: Florida Man shrieking as the $3,400 rent notice slaps onto the trailer (code frame, no AI)
+ title «$3,400 FOR / A SHED?!» + booking letterboard plate.   python3 cover.py   -> cover.png (+ series/florida-man/covers/cover_s01e05.png)"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import shutil
import ep05 as E
import covergen_fm as CG

big = E.r_hook(0.9, 0.9)
here = pathlib.Path(__file__).parent
CG.make(big, ['$3,400 FOR', 'A SHED?!'], n=5, out=str(here / 'cover.png'), shift=300, title_size=92)
dst = here.parents[1] / 'covers' / 'cover_s01e05.png'
shutil.copy(here / 'cover.png', dst)
print(dst)
