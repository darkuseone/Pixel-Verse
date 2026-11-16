"""Model sheet of «Замело»: heroes + expressions.  python3 series/zamelo/design/cast_sheet.py -> cast_sheet.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import numpy as np
from PIL import Image
from props import zampix as ZX, zamcast as C
from props.dibspix import blit

W, H = 1800, 1400
big = np.zeros((H, W, 3), np.uint8)
for y in range(H): big[y] = np.array((150, 184, 230)) * (1 - y / H) + np.array((236, 242, 255)) * (y / H)
big[860:880] = (236, 244, 255)


def put(fn, x, y, s, **kw):
    sp = ZX.draw(fn, s, **kw); blit(big, sp, x, y, s, None, False)


put(C.zhora, 220, 860, 8.0, expr='proud', hand_n=(22.0, 30.0), prop_n=lambda sp, h: C.shovel(sp, h, ang=-1.45, l=24.0))
put(C.ira, 600, 860, 8.0, expr='yelling', mouth_=0.6, box=True)
put(C.vitek, 900, 860, 8.0, expr='cheerful', phone_up=True, hand_n=(10.0, 44.0))
put(C.nina, 1180, 860, 8.0, expr='kind')
put(C.chayka, 1500, 860, 10.0, expr='dry', chew=1.0, t=0.3)
emos = [('proud', 0), ('outraged', .7), ('gloomy', 0), ('exhausted', .3), ('offended', .6), ('cocky', 0)]
for i, (e, m) in enumerate(emos):
    pan = np.zeros((300, 280, 3), np.uint8); pan[:] = (200, 216, 240)
    sp = ZX.draw(C.zhora, 12.0, expr=e, mouth_=m, frost=1.0 if e == 'exhausted' else 0.0)
    blit(pan, sp, 110, 1010, 12.0, None, False)
    big[900:1200, 20 + i * 290:300 + i * 290] = pan
for i, (e, m) in enumerate([('dry', 0), ('dry', .7)]):
    pan = np.zeros((180, 280, 3), np.uint8); pan[:] = (200, 216, 240)
    sp = ZX.draw(C.chayka, 8.0, expr=e, mouth_=m)
    blit(pan, sp, 80, 230, 8.0, None, False)
    big[1210:1390, 20 + i * 290:300 + i * 290] = pan
Image.fromarray(big).save(str(pathlib.Path(__file__).parent / 'cast_sheet.png'))
print('ok')
