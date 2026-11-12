"""Model sheet «STILL 1986» from the real sprites (props/v86cast.py, manner props/v86pix.py).  python3 cast_sheet.py -> cast_sheet.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import numpy as np
from PIL import Image, ImageDraw
import overlays as O
from props import v86pix as VX, v86cast as C
from props.dibspix import blit

W, H = 2400, 1500
big = np.zeros((H, W, 3), np.uint8)
yy = np.linspace(0, 1, H)[:, None, None]
big[:] = (np.array((40, 22, 78)) * (1 - yy) + np.array((250, 120, 120)) * yy).astype(np.uint8)
def put(fn, x, y, s, flip=False, **kw):
    sp = VX.draw(fn, s, flip=flip, **kw); blit(big, sp, x, y, s, None, flip); return sp
put(C.vince, 260, 900, 9.0, expr='cool')
put(C.rey, 640, 900, 9.0, expr='chill')
put(C.meter, 900, 900, 9.0)
put(C.sign_free, 1080, 900, 9.0)
put(C.car, 1700, 900, 7.0, vince_kw=dict(expr='smooth', glint=1.0, sparkle=1.0))
for i, e in enumerate(['cool', 'smooth', 'outraged', 'scheming', 'ecstatic', 'defeated', 'shock', 'tired']):
    sp = VX.draw(C.vince, 12.0, expr=e, legs=False)
    hx, hy = sp.anchors['head']
    blit(big, sp, 160 + i * 290 - hx * 12, 1400 + hy * 12 - 0, 12.0, None)
im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
d.text((60, 40), 'STILL 1986 — CAST', font=O.pfont(48), fill=(255, 255, 255))
im.save(pathlib.Path(__file__).with_name('cast_sheet.png')); print('ok')
