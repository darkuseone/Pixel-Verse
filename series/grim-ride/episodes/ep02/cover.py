"""Cover S01E02: Death squints at the captcha on his phone (code frame, no AI) + title «DEATH VS / CAPTCHA?» + tombstone plate.
  python3 cover.py   -> cover.png (+ series/grim-ride/covers/cover_s01e02.png)"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import shutil
import numpy as np
from PIL import Image
import ep02 as E
from props import grimkit as K
from props import grimpix as GX
import covergen_grim as CG

t = 0.4
big, _ = E.grim_cu(t, 0.0, 'squint', head=(380, 900), sc=14.0, fx_=E.phone_glow, look=(0.8, -0.4), mouth_=0.3)
ph = E.KIT.phone(t, 'captcha', 0.6, taps=E.TAPS)
small = np.array(Image.fromarray(ph[280:1560, 100:980]).resize((440, 640), Image.NEAREST))
big[700:1340, 600:1040] = small
big[692:700, 592:1048] = GX.INK; big[1340:1348, 592:1048] = GX.INK; big[692:1348, 592:600] = GX.INK; big[692:1348, 1040:1048] = GX.INK
here = pathlib.Path(__file__).parent
CG.make(big, ['DEATH VS', 'CAPTCHA?'], n=2, out=str(here / 'cover.png'), title_y=150, plate_y=1420)
dst = here.parents[1] / 'covers' / 'cover_s01e02.png'
shutil.copy(here / 'cover.png', dst)
print(dst)
