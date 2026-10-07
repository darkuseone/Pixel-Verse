"""Model sheet of the «Grim Ride» cast in the «Lantern Stipple» manner -> cast_sheet.png
  python3 series/grim-ride/design/cast_sheet.py"""
import sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / 'engine'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from props import grimpix as GX, grimcast as GC
from props.dibspix import blit

W, H = 2400, 1700
BG = (24, 16, 36)
LINE = (70, 56, 96)
INKT = (200, 188, 226)
DIM = (120, 104, 150)
F = pathlib.Path(__file__).parent / 'fonts'
f_title = ImageFont.truetype(str(F / 'InstrumentSerif-Italic.ttf'), 64)
f_lab = ImageFont.truetype(str(F / 'Jura-Medium.ttf'), 22)
f_small = ImageFont.truetype(str(F / 'Jura-Light.ttf'), 18)

big = np.zeros((H, W, 3), np.uint8); big[:] = BG
# faint moonlit gradient top, lantern warmth bottom
yy = np.linspace(0, 1, H)[:, None, None]
big[:] = np.clip(big + (1 - yy) * np.array((10, 14, 30)) + (yy ** 3) * np.array((40, 16, 6)), 0, 255).astype(np.uint8)


def put(fn, x, y, s, **kw):
    sp = GX.draw(fn, s, t=0.35, **kw)
    blit(big, sp, x, y, s)
    return sp


def silhouette(fn, x, y, s, col=(10, 6, 16), **kw):
    sp = GX.draw(fn, s, t=0.35, **kw)
    sp.col[:] = col
    blit(big, sp, x, y, s)


# ---------------------------------------------------------------- row 1: the cast at the same scale, silhouettes under them
GROUND = 800
cast = [
    ('GRIM', 'question mark', GC.grim, dict(expr='proud', wind=0.5, spin=0.6, raven=True), 420, 5.4),
    ('EDGAR', 'comma', GC.edgar, dict(expr='deadpan', cam=False), 760, 8.0),
    ('HAROLD, 97', 'bobblehead', GC.harold, dict(pose='ride', expr='grin', spin=1.0), 1290, 5.4),
    ('TODD', 'pear', GC.todd, dict(expr='hype', mouth_=0.4), 1640, 5.6),
    ('KAYDEN', 'bean', GC.kayden, dict(spin=0.7), 1950, 5.4),
    ('KEVIN, 12 FT', 'store-bought', GC.kevin, dict(turn=0.5), 2250, 3.4),
]
for name, sil, fn, kw, x, s in cast:
    put(fn, x, GROUND, s, **kw)
    silhouette(fn, x, GROUND + 330, s * 0.42, **kw)

# ---------------------------------------------------------------- row 2: faces (expressions at close-up resolution)
EY = 1450
faces = [(GC.grim, 'head', dict(ride=False, scythe=False), e, 6.4) for e in ('proud', 'menace', 'panic', 'whine', 'stunned')] + \
        [(GC.edgar, 'head', dict(perch=False), e, 9.0) for e in ('deadpan', 'sly')] + \
        [(GC.harold, 'head', dict(pose='stand'), e, 7.5) for e in ('bored', 'grin')] + \
        [(GC.todd, 'head', dict(phone=False), e, 8.0) for e in ('hype', 'pity')]
CARD = (54, 44, 80)
fx0 = 140
for i, (fn, pin, kw, e, s) in enumerate(faces):
    sp = GX.draw(fn, s, t=1.4, expr=e, hires=2, **kw)
    hx, hy = sp.anchors[pin]
    cx = fx0 + i * 194
    # crop: window 170 x 210 around the head
    tmp = np.zeros((420, 420, 3), np.uint8); tmp[:] = CARD
    blit(tmp, sp, 210 - hx * s, 210 + hy * s, s)
    crop = tmp[95:305, 125:295]
    big[EY - 105:EY + 105, cx - 85:cx + 85] = crop
    big[EY - 106, cx - 86:cx + 86] = LINE; big[EY + 105, cx - 86:cx + 86] = LINE
    big[EY - 106:EY + 106, cx - 86] = LINE; big[EY - 106:EY + 106, cx + 85] = LINE

# ---------------------------------------------------------------- palettes (4-tone ramps)
im = Image.fromarray(big); d = ImageDraw.Draw(im)
pals = [('CLOAK', GC.CLK), ('BONE', GX.tones(GC.BONE)), ('GLOW', GX.tones(GC.GLOW)), ('FEATHER', GX.tones(GC.FEATHER, k=0.3, glow=(210, 120, 200))),
        ('HELMET', GX.tones(GC.HELM, glow=(170, 120, 210))), ('CARDIGAN', GX.tones(GC.CARDI)), ('TEE', GX.tones(GC.TEE)), ('HOODIE', GX.tones(GC.HOODIE, glow=(160, 110, 200)))]
px0, py0 = 140, 1600
for i, (nm, p) in enumerate(pals):
    x = px0 + i * 260
    for k, c in enumerate(p):
        d.rectangle([x + k * 44, py0, x + k * 44 + 40, py0 + 40], fill=tuple(int(v) for v in c))
    d.text((x, py0 + 50), nm, font=f_small, fill=DIM)

# ---------------------------------------------------------------- labels, rules, light diagram
d.text((120, 60), 'Lantern Stipple', font=f_title, fill=(236, 226, 255))
d.text((124, 140), 'GRIM RIDE  ·  CAST MODEL SHEET  ·  SEASON 1', font=f_lab, fill=DIM)
d.line([(120, 190), (W - 120, 190)], fill=LINE, width=1)
for name, sil, fn, kw, x, s in cast:
    tw = d.textlength(name, font=f_lab)
    d.text((x - tw / 2, GROUND + 26), name, font=f_lab, fill=INKT)
    tw = d.textlength(sil, font=f_small)
    d.text((x - tw / 2, GROUND + 345), sil, font=f_small, fill=DIM)
d.line([(120, GROUND + 380), (W - 120, GROUND + 380)], fill=LINE, width=1)
d.text((120, EY - 150), 'FACES  ·  2× SPRITE RESOLUTION', font=f_small, fill=DIM)
d.text((120, py0 - 40), 'FOUR TONES PER MATERIAL  ·  DEPTH / SHADOW / BASE / LANTERN GLOW  ·  STIPPLE TRANSITIONS', font=f_small, fill=DIM)
# light diagram (top right): moon above-behind, lantern below-front
lx, ly = W - 330, 70
d.ellipse([lx, ly, lx + 34, ly + 34], outline=(150, 186, 255), width=2)
d.text((lx + 50, ly + 6), 'MOON  ·  rim, above', font=f_small, fill=(150, 186, 255))
d.ellipse([lx, ly + 60, lx + 34, ly + 94], fill=(255, 140, 60))
d.text((lx + 50, ly + 66), 'LANTERN  ·  key, below', font=f_small, fill=(255, 160, 90))
im.save(pathlib.Path(__file__).parent / 'cast_sheet.png')
print('ok')
