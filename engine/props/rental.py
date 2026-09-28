"""Horse rental «ПРОКАТ ЛОШАДЕЙ» (S01E04): two xAI backgrounds (series/.../bg/rental_ext.png, rental_int.png,
1280x720, grok-imagine-image-2.0 medium 1k) -> pixel world (palette 110) + readable pixel text by code +
foreground occluder sprites + glow maps for lantern flicker. Coordinates = native image px."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as PATHS

BG = PATHS.series() / 'bg'
EXT_FEET = 598            # road line (feet) outside
INT_FEET = 662            # floor line in front of the counter
COUNTER_TOP = 368
STALL_ECO = (528, 757)    # x ranges of stall gates
STALL_COMF = (787, 1022)
GATE_Y = (326, 502)
CURTAIN = (1063, 110, 1270, 500)
LANTERNS = [(505, 212), (1045, 210)]


def _text(img, txt, cx, cy, size, col, shade=None, off=(1, 1)):
    f = ImageFont.truetype(PATHS.FONT_PX, size)
    bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    m = Image.new('L', img.size, 0); d = ImageDraw.Draw(m); d.fontmode = '1'
    d.text((int(cx - tw / 2) - bb[0], int(cy - th / 2) - bb[1]), txt, font=f, fill=255)
    m = np.array(m) > 127
    a = np.array(img)
    if shade is not None: a[np.roll(np.roll(m, off[1], 0), off[0], 1) & ~m] = shade
    a[m] = col
    return Image.fromarray(a)


def _plaque(img, cx, cy, w, h, txt, size=8, wood=(150, 104, 58), col=(60, 34, 20), gold=False):
    a = np.array(img)
    x0, y0 = int(cx - w / 2), int(cy - h / 2)
    a[y0 - 2:y0 + h + 2, x0 - 2:x0 + w + 2] = (40, 24, 14)
    a[y0:y0 + h, x0:x0 + w] = (232, 190, 80) if gold else wood
    a[y0:y0 + 2, x0:x0 + w] = (255, 230, 140) if gold else (186, 136, 84)
    return _text(Image.fromarray(a), txt, cx, cy + 1, size, col)


def exterior():
    img = Image.open(BG / 'rental_ext.png').convert('RGB')
    img = _text(img, 'ПРОКАТ', 587, 222, 24, (74, 42, 22), (206, 160, 104), (2, 2))
    img = _text(img, 'ЛОШАДЕЙ', 587, 254, 24, (74, 42, 22), (206, 160, 104), (2, 2))
    img = _text(img, 'ТАРИФЫ', 880, 370, 8, (60, 36, 20))
    img = _text(img, 'ОТ 1$', 880, 390, 8, (150, 40, 30))
    return img


def interior():
    img = Image.open(BG / 'rental_int.png').convert('RGB')
    chalk, chalk2 = (236, 236, 222), (250, 214, 120)
    img = _text(img, 'ТАРИФЫ', 265, 178, 16, chalk2)
    for i, (a, b) in enumerate((('ЭКОНОМ', '1$'), ('КОМФОРТ', '3$'), ('ПРЕМИУМ', '5$'))):
        y = 206 + i * 24
        img = _text(img, a, 232, y, 8, chalk); img = _text(img, b, 335, y, 16, chalk2)
    img = _text(img, '*АВТОПРОДЛЕНИЕ', 265, 284, 8, (200, 200, 190))
    for i, s in enumerate(('ОТМЕНА', 'ТОЛЬКО', 'ПИСЬМОМ')):
        img = _text(img, s, 430, 214 + i * 18, 8, (60, 34, 20))
    img = _plaque(img, 642, 312, 64, 14, 'ЭКОНОМ')
    img = _plaque(img, 905, 312, 72, 14, 'КОМФОРТ')
    img = _plaque(img, 1166, 178, 76, 16, 'ПРЕМИУМ', gold=True)
    return img


def _sprite(world, x0, y0, x1, y1, mask=None):
    spr = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    spr[..., :3] = world[y0:y1, x0:x1]; spr[..., 3] = 255
    if mask is not None: spr[..., 3] = np.where(mask, 255, 0)
    return spr


def glow_map(shape, pts, r):
    Hh, Ww = shape
    yy, xx = np.mgrid[0:Hh, 0:Ww].astype(np.float32)
    g = np.zeros(shape, np.float32)
    for (x, y) in pts:
        d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2) / r
        g += np.clip(1 - d, 0, 1) ** 1.6
    return g


def build(force=False):
    cache = PATHS.build('props', 'rental.npz')
    if os.path.exists(cache) and not force:
        d = np.load(cache); return {k: d[k] for k in d.files}
    q = lambda im: np.array(im.quantize(colors=110, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'))
    ext, inn = q(exterior()), q(interior())
    # counter occluder: counter body + bell + book
    y0, y1, x1 = 334, 540, 460
    yy, xx = np.mgrid[y0:y1, 0:x1]
    m = (yy >= COUNTER_TOP - 2) | ((xx > 60) & (xx < 122) & (yy > 334)) | ((xx > 196) & (xx < 340) & (yy > 344))
    out = dict(ext=ext, int=inn,
               counter=_sprite(inn, 0, y0, x1, y1, m),
               gate_eco=_sprite(inn, STALL_ECO[0], GATE_Y[0], STALL_ECO[1], GATE_Y[1]),
               gate_comf=_sprite(inn, STALL_COMF[0], GATE_Y[0], STALL_COMF[1], GATE_Y[1]),
               glow_int=glow_map(inn.shape[:2], LANTERNS, 110))
    np.savez_compressed(cache, **out)
    return out


if __name__ == '__main__':
    d = build(True)
    Image.fromarray(d['ext']).save(PATHS.build('props', 'rental_ext.png'))
    Image.fromarray(d['int']).save(PATHS.build('props', 'rental_int.png'))
    print('ok', d['ext'].shape, d['int'].shape)
