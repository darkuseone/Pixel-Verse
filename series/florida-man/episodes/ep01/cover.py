"""Cover S01E01: Florida Man shrieking at the $9,000 A/C invoice, the dead condenser smoking behind (code frame, no AI)
+ title «NINE / GRAND?!» + booking letterboard plate.   python3 cover.py   -> cover.png (+ series/florida-man/covers/cover_s01e01.png)"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import shutil
import ep01 as E
from props import fmcast as C
from props import fmkit as K
import covergen_fm as CG

t = 0.9
def pre(big, v):
    E.ac_actor(v, t)(big, v, K.light_sun(v))
    E.ac_smoke(big, v, t)
big, a = E.cu(E.YARD, K.light_sun, C.fm, t, 600.0, 450.0, 31.0, (520, 1010), Z=1.35, blur=6, pre_=pre, expr='shriek', mouth_=0.95,
              sweat=1.0, glasses_drop=1.0, look=(0.0, 0.2))
K.invoice_card(big, 600, 1120, 440, ang=8.0)
here = pathlib.Path(__file__).parent
CG.make(big, ['NINE', 'GRAND?!'], n=1, out=str(here / 'cover.png'))
dst = here.parents[1] / 'covers' / 'cover_s01e01.png'
dst.parent.mkdir(exist_ok=True)
shutil.copy(here / 'cover.png', dst)
print(dst)
