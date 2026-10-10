"""Cover S01E04: Florida Man shrieking with the $8,000 insurance letter (code frame, no AI)
+ title «$8,000 / INSURANCE?!» + booking letterboard plate.   python3 cover.py   -> cover.png (+ series/florida-man/covers/cover_s01e04.png)"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import shutil
import ep04 as E
import covergen_fm as CG

big = E.r_hook(0.9, 0.9)
here = pathlib.Path(__file__).parent
CG.make(big, ['$8,000', 'INSURANCE?!'], n=4, out=str(here / 'cover.png'), shift=300, title_size=92)
dst = here.parents[1] / 'covers' / 'cover_s01e04.png'
shutil.copy(here / 'cover.png', dst)
print(dst)
