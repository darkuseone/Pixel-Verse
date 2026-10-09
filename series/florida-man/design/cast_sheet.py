"""Model sheet of the «Florida Man: Allegedly» cast in the «Tabloid Sun» manner -> cast_sheet.png
  python3 series/florida-man/design/cast_sheet.py"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'engine'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from props import fmpix as FX, fmcast as C
from props.dibspix import blit

W, H = 2400, 1700
BG = (236, 226, 204)                  # sun-bleached newsprint
LINE = (190, 176, 150)
INKT = (14, 44, 54)
DIM = (120, 110, 96)
F = pathlib.Path(__file__).parent / 'fonts'
f_title = ImageFont.truetype(str(F / 'InstrumentSerif-Italic.ttf'), 64)
f_lab = ImageFont.truetype(str(F / 'Jura-Medium.ttf'), 22)
f_small = ImageFont.truetype(str(F / 'Jura-Light.ttf'), 18)

big = np.zeros((H, W, 3), np.uint8); big[:] = BG
yy, xx = np.mgrid[0:H, 0:W]
dots = (((xx + yy) // 6) % 2 == 0) & (((xx - yy) // 6) % 2 == 0) & ((xx % 6) < 2) & ((yy % 6) < 2)
big[dots & (yy > H - 260)] = (224, 210, 184)                       # halftone floor band


def put(fn, x, y, s, **kw):
    sp = FX.draw(fn, s, t=0.35, **kw)
    blit(big, sp, x, y, s)
    return sp


def silhouette(fn, x, y, s, col=(14, 44, 54), **kw):
    sp = FX.draw(fn, s, t=0.35, **kw)
    sp.col[:] = col
    blit(big, sp, x, y, s)


GROUND = 820
cast = [
    ('FLORIDA MAN', 'olive on toothpicks', C.fm, dict(expr='zen', prop_n=lambda sp, h: C.sub(sp, (h[0] + 1, h[1] + 1))), 380, 7.4),
    ('MORT POUCH, ESQ.', 'ladle', C.mort, dict(expr='deadpan', lump='sub'), 900, 9.0),
    ('DEPUTY DARLENE', 'mushroom', C.darlene, dict(expr='bored', gum=0.5, prop_n=lambda sp, h: C.basket(sp, h)), 1380, 7.2),
    ('TANNER', 'lit match', C.tanner, dict(expr='chipper', jobs=8, thumbs=True, hand_n=(11.0, 50.0)), 1880, 7.0),
    ('IGUANA', 'falls when cold', C.iguana, dict(), 2220, 6.0),
]
for name, sil, fn, kw, x, s in cast:
    put(fn, x, GROUND, s, **kw)
    silhouette(fn, x, H - 100, s * 0.36, **kw)

# close-up row: faces at 3x
faces = [(C.fm, dict(expr='shriek', glasses_drop=1.0, sweat=1.0, mouth_=0.9), 300), (C.fm, dict(expr='zen', frost=1.0), 640),
         (C.mort, dict(expr='smug', lift=0.6), 980), (C.darlene, dict(expr='bored', mouth_=0.3), 1320),
         (C.tanner, dict(expr='shiver', frost=1.0, shiver=1.0), 1660), (C.tanner, dict(expr='chipper', sweat=1.0), 2000)]
for fn, kw, x in faces:
    sp = FX.draw(fn, 15.0, t=0.4, **kw)
    px, py = sp.anchors['head']
    sub = np.zeros((300, 300, 3), np.uint8); sub[:] = (250, 244, 228)
    blit(sub, sp, 150 - px * 15.0, 160 + py * 15.0, 15.0)
    big[1000:1300, x - 150:x + 150] = sub
    big[996:1000, x - 150:x + 150] = INKT; big[1300:1304, x - 150:x + 150] = INKT
    big[996:1304, x - 154:x - 150] = INKT; big[996:1304, x + 150:x + 154] = INKT

im = Image.fromarray(big); d = ImageDraw.Draw(im)
d.text((60, 40), 'Tabloid Sun', font=f_title, fill=INKT)
d.text((64, 120), 'FLORIDA MAN: ALLEGEDLY — cast model sheet · noon sun from above · 45° halftone · teal ink', font=f_small, fill=DIM)
for name, sil, fn, kw, x, s in cast:
    d.text((x - 110, GROUND + 30), name, font=f_lab, fill=INKT)
    d.text((x - 110, GROUND + 60), sil, font=f_small, fill=DIM)
d.text((60, 960), 'faces at 3x  ·  shriek / frozen zen / smug / bored / shiver / chipper', font=f_small, fill=DIM)
d.text((60, H - 44), 'silhouette test: every type reads in solid ink', font=f_small, fill=DIM)
d.line([(60, 150), (W - 60, 150)], fill=LINE, width=2)
im.save(pathlib.Path(__file__).parent / 'cast_sheet.png')
print('ok')
