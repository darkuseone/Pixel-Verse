"""Model sheet «Ключевой сотрудник» from the real sprites (props/kscast.py, manner props/kspix.py).  python3 cast_sheet.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import numpy as np
from PIL import Image, ImageDraw
import overlays as O
from props import kspix as KX, kscast as C
from props.dibspix import blit

W, H = 2400, 1560
big = np.zeros((H, W, 3), np.uint8)
yy = np.linspace(0, 1, H)[:, None, None]
big[:] = (np.array((226, 214, 180)) * (1 - yy) + np.array((176, 160, 128)) * yy).astype(np.uint8)
big[880:] = (big[880:] * 0.86).astype(np.uint8)
def put(fn, x, y, s, flip=False, **kw):
    sp = KX.draw(fn, s, flip=flip, **kw); blit(big, sp, x, y, s, None, flip); return sp
put(C.edik, 300, 880, 9.0, expr='proud')
put(C.edik, 620, 880, 9.0, expr='hopeful', coat=True, hat=True)
put(C.fikus, 900, 880, 9.0, expr='deadpan')
put(C.shef, 1300, 880, 9.0, expr='boss')
put(C.shef, 1700, 880, 9.0, expr='bark', coat=True, hand_n=(26.0, 44.0), prop_n=lambda sp, h: C.keyring(sp, h))
put(C.lyuda, 2050, 880, 9.0, expr='strict', prop_n=lambda sp, h: C.mug(sp, h, 'ЛЮДА'))
for i, e in enumerate(['proud', 'beam', 'hopeful', 'shock', 'panic', 'crushed', 'sleepy', 'scheme']):
    sp = KX.draw(C.edik, 12.0, expr=e, legs=False)
    hx, hy = sp.anchors['head']
    blit(big, sp, 150 + i * 200 - hx * 12, 1490 + hy * 12 - 460, 12.0, None)
for i, e in enumerate(['deadpan', 'smirk', 'shock', 'strict']):
    sp = KX.draw(C.fikus, 7.0, expr=e, mouth_=0.6 if i == 1 else 0.0)
    blit(big, sp, 1780 + i * 150, 1530, 7.0, None)
im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
d.text((60, 40), 'КЛЮЧЕВОЙ СОТРУДНИК — КАСТ', font=O.pfont(44), fill=(40, 30, 26))
im.save(pathlib.Path(__file__).with_name('cast_sheet.png')); print('ok')
