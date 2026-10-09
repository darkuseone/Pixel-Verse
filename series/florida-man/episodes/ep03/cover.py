"""Cover S01E03: Florida Man shrieking at the hospital billing window (code frame, no AI)
+ title «$2,000 / ICE PACK?!» + booking letterboard plate.   python3 cover.py   -> cover.png (+ series/florida-man/covers/cover_s01e03.png)"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import shutil
import ep03 as E
import covergen_fm as CG

big = E.r_hook(0.9, 0.9)
here = pathlib.Path(__file__).parent
CG.make(big, ['$2,000', 'ICE PACK?!'], n=3, out=str(here / 'cover.png'), title_y=210, title_size=92, plate_y=1690)
dst = here.parents[1] / 'covers' / 'cover_s01e03.png'
shutil.copy(here / 'cover.png', dst)
print(dst)
