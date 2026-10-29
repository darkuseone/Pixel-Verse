"""Model sheet of the «Land of the Fee» cast in the «Intaglio Pop» manner: python3 cast_sheet.py -> cast_sheet.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import numpy as np
from PIL import Image, ImageDraw
import overlays as O
from props import feepix as FX, feecast as C
from props.dibspix import blit

W, H = 1920, 1080
big = np.zeros((H, W, 3), np.uint8); big[:] = (244, 238, 214)
for y in range(0, H, 6): big[y] = (236, 230, 204)
def put(fn, s, x, y, **kw):
    blit(big, FX.draw(fn, s, **kw), x, y, s)
put(C.duke, 9.0, 250, 900, expr='proud', puff=1.0)
put(C.duke, 9.0, 620, 900, expr='roar', flop=1.0, t=0.3, hand_n=(21.0, 47.0), prop_n=lambda sp, h: C.phone(sp, h, 0.0, 0.0))
put(C.duke, 7.0, 980, 700, expr='glare', fly=0.25, shades='eyes')
put(C.sal, 11.0, 1250, 900, expr='dead')
put(C.doris, 11.0, 1480, 900, expr='warm', meter='$19.99')
put(C.kiosk, 9.0, 1760, 900, talk=0.6)
im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
f, f2 = O.pfont(40), O.pfont(20)
d.text((60, 50), 'LAND OF THE FEE — CAST (INTAGLIO POP)', font=f, fill=(18, 70, 48))
for x, name, sub in ((250, 'DUKE', 'proud / roar'), (980, 'DUKE', 'flying'), (1250, 'SAL', 'deadpan pigeon'), (1480, 'DORIS', 'the last human'),
                     (1760, 'FEE-BEE', 'AI on every screen')):
    d.text((x - f2.getlength(name) / 2, 960), name, font=f2, fill=(200, 40, 48))
    d.text((x - O.pfont(14).getlength(sub) / 2, 994), sub, font=O.pfont(14), fill=(18, 70, 48))
im.save(pathlib.Path(__file__).parent / 'cast_sheet.png'); print('cast_sheet.png')
