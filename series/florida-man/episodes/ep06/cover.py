"""Cover S01E06: Florida Man shrieking on top of the jail fence at night, climbing IN (code frame, no AI)
+ title «JAIL'S / CHEAPER?!» + booking letterboard plate.   python3 cover.py   -> cover.png (+ series/florida-man/covers/cover_s01e06.png)"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import shutil
import ep06 as E
import covergen_fm as CG

big = E.r_hook(0.9, 0.9, siren_k=0.0)
here = pathlib.Path(__file__).parent
CG.make(big, ["JAIL'S", 'CHEAPER?!'], n=6, out=str(here / 'cover.png'), shift=300, title_size=92)
dst = here.parents[1] / 'covers' / 'cover_s01e06.png'
shutil.copy(here / 'cover.png', dst)
print(dst)
