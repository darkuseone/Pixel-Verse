"""Locations of «Валера и кот» from xAI backgrounds (1280x720, grok-imagine-image-2.0 medium 1k) -> pixel worlds
(110-colour palette) + readable pixel text by code (ЖЭК notice, calendar, price tags) + occluder sprites + glow maps.
All coordinates are native image px of series/valera-i-kot/bg/*.png."""
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as PATHS

SLUG = 'valera-i-kot'
BG = PATHS.series(SLUG) / 'bg'

# ---------------------------------------------------------------- kitchen
K_FLOOR = 640               # Valera's feet line in medium shots
K_UNIT = 16.0               # Valera world px per unit at K_FLOOR
RAD = (470, 410, 735, 530)  # radiator box
RAD_TOP = 408               # cat lies on the radiator/blanket
CAT_K = (585.0, 404.0)      # cat anchor on the radiator (floor point under the loaf)
CAT_K_UNIT = 7.0
VALVE = (728.0, 428.0)      # air valve at the top right of the radiator
KETTLE = (1118.0, 362.0)    # kettle spout tip
STOVE_X = 1130.0
WINDOW_OPEN = (660, 80, 780, 160)   # open ventilation pane
LAMP_K = (855.0, 100.0)
CLOCK = (1150.0, 94.0, 26.0)        # centre + radius of the wall clock face
CALENDAR = (1176, 142, 1256, 282)

# ---------------------------------------------------------------- bathroom
B_FEET = 470                # Valera's feet inside the tub (hidden by the tub front)
B_UNIT = 14.6
SHOWER = (492.0, 88.0)      # shower head nozzle
TUB_RIM = [(95, 438), (160, 420), (400, 418), (690, 424), (702, 440)]   # front rim polyline (occluder top)
BULB = (832.0, 105.0)
B_FLOOR = 660               # floor line in front of the tub

# ---------------------------------------------------------------- stairwell
DOOR = (90, 120, 290, 540)
NOTICE = (122, 336, 258, 500)       # A4 notice taped on the entrance door
LAMP_S = (616.0, 92.0)
S_FLOOR = 640


def font(size):
    return ImageFont.truetype(PATHS.FONT_PX, size)


def text(img, txt, cx, cy, size, col, shade=None, off=(1, 1), anchor='c'):
    f = font(size)
    bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    m = Image.new('L', img.size, 0); d = ImageDraw.Draw(m); d.fontmode = '1'
    x = int(cx - tw / 2) if anchor == 'c' else int(cx)
    d.text((x - bb[0], int(cy - th / 2) - bb[1]), txt, font=f, fill=255)
    m = np.array(m) > 127
    a = np.array(img)
    if shade is not None: a[np.roll(np.roll(m, off[1], 0), off[0], 1) & ~m] = shade
    a[m] = col
    return Image.fromarray(a)


def paper(img, box, col=(236, 234, 222), edge=(186, 180, 164), tape=(214, 206, 150)):
    a = np.array(img)
    x0, y0, x1, y1 = box
    a[y0 + 3:y1 + 3, x0 + 3:x1 + 3] = (a[y0 + 3:y1 + 3, x0 + 3:x1 + 3] * 0.55).astype(np.uint8)   # shadow
    a[y0:y1, x0:x1] = col
    a[y0:y1, x1 - 2:x1] = edge; a[y1 - 2:y1, x0:x1] = edge
    for tx in (x0 - 4, x1 - 14):
        a[y0 - 4:y0 + 6, tx:tx + 18] = tape
    return Image.fromarray(a)


def notice(img, lines, box=NOTICE, crossed=(), handwritten=()):
    """ЖЭК notice: lines = [(text, size, colour)], crossed = indices of struck-through lines,
    handwritten = [(text, size, colour, dy)] scribbles added under the struck lines"""
    img = paper(img, box)
    x0, y0, x1, y1 = box
    cx = (x0 + x1) / 2
    y = y0 + 16
    ys = []
    for i, (t, size, col) in enumerate(lines):
        img = text(img, t, cx, y, size, col)
        ys.append((y, size, t))
        y += size + 8
    a = np.array(img)
    f = font(8)
    for i in crossed:
        yy, size, t = ys[i]
        tw = font(size).getbbox(t)[2]
        a[int(yy) - 1:int(yy) + 2, int(cx - tw / 2) - 3:int(cx + tw / 2) + 3] = (200, 40, 40)
    img = Image.fromarray(a)
    for (t, size, col, dy) in handwritten:
        img = text(img, t, cx + 6, dy, size, col)
    return img


def q(im, colors=110):
    return np.array(im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'))


def glow_map(shape, pts, r):
    Hh, Ww = shape
    yy, xx = np.mgrid[0:Hh, 0:Ww].astype(np.float32)
    g = np.zeros(shape, np.float32)
    for (x, y) in pts:
        d = np.sqrt((xx - x) ** 2 + (yy - y) ** 2) / r
        g += np.clip(1 - d, 0, 1) ** 1.6
    return g


def kitchen(day=1):
    img = Image.fromarray(q(Image.open(BG / 'kitchen.png').convert('RGB')))
    x0, y0, x1, y1 = CALENDAR
    a = np.array(img)
    a[y0 + 62:y1 - 6, x0 + 6:x1 - 6] = (238, 234, 222)                  # blank lower half of the calendar
    img = Image.fromarray(a)
    img = text(img, 'ДЕКАБРЬ', (x0 + x1) / 2, y0 + 72, 8, (170, 40, 36))
    img = text(img, str(day), (x0 + x1) / 2, y0 + 104, 32, (40, 36, 40))
    return img


def tub_occluder(world):
    """front of the bathtub (below the rim polyline) as an RGBA sprite in world px"""
    from PIL import ImageDraw
    Hh, Ww = world.shape[:2]
    m = Image.new('L', (Ww, Hh), 0)
    pts = TUB_RIM + [(702, 600), (95, 600)]
    ImageDraw.Draw(m).polygon(pts, fill=1)
    m = np.array(m).astype(bool)
    x0, x1, y0, y1 = 80, 720, 400, 610
    spr = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    spr[..., :3] = world[y0:y1, x0:x1]; spr[..., 3] = np.where(m[y0:y1, x0:x1], 255, 0)
    return spr, x0, y0


NOTICE_E01 = [('ОБЪЯВЛЕНИЕ', 8, (40, 36, 40)), ('ГОРЯЧЕЙ', 16, (170, 30, 30)), ('ВОДЫ НЕТ', 16, (170, 30, 30)),
              ('С 01.12', 8, (40, 36, 40)), ('ПО 15.12', 8, (40, 36, 40)), ('ЖЭК №3', 8, (60, 60, 120))]


def build(force=False):
    cache = PATHS.build('props', 'panelka.npz')
    if os.path.exists(cache) and not force:
        d = np.load(cache); return {k: d[k] for k in d.files}
    kit = np.array(kitchen(1))                                  # text is drawn after quantization (keeps pure reds)
    bath = q(Image.open(BG / 'bathroom.png').convert('RGB'))
    stair = np.array(notice(Image.fromarray(q(Image.open(BG / 'stairwell.png').convert('RGB'))), NOTICE_E01))
    tub, tx, ty = tub_occluder(bath)
    out = dict(kitchen=kit, bath=bath, stair=stair, tub=tub, tub_xy=np.array([tx, ty]),
               glow_k=glow_map(kit.shape[:2], [LAMP_K], 260), glow_b=glow_map(bath.shape[:2], [BULB], 220),
               glow_s=glow_map(stair.shape[:2], [LAMP_S], 240))
    np.savez_compressed(cache, **out)
    return out


if __name__ == '__main__':
    d = build(True)
    for k in ('kitchen', 'bath', 'stair'):
        Image.fromarray(d[k]).save(PATHS.build('props', f'{k}.png'))
    print('ok', {k: v.shape for k, v in d.items()})
