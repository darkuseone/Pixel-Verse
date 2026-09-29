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


# ---------------------------------------------------------------- gastronom (shop)
SH_TAMARA = (1165.0, 625.0, 19.0)        # cashier anchor (behind the counter, facing left)
SH_VALERA = (790.0, 712.0, 22.0)         # customer anchor (facing right)
SH_ZINA = (560.0, 690.0, 17.0)           # granny in the queue
LCD = (902, 298, 990, 334)              # customer display on a pole by the register
COUNTER_EDGE = [(880, 425), (1090, 446), (1280, 452)]
TAG = (146, 546, 266, 630)              # big yellow price tag on the deli case
SH_LIGHTS = [(490.0, 32.0), (960.0, 32.0)]


def price_tag(img, box=TAG, name='ДОКТОРСКАЯ', big='199', foot=('*ПО КАРТЕ', 'БЕЗ КАРТЫ 289')):
    a = np.array(img)
    x0, y0, x1, y1 = box
    a[y0 - 2:y1 + 2, x0 - 2:x1 + 2] = (70, 56, 20)
    a[y0:y1, x0:x1] = (250, 218, 60)
    a[y0:y0 + 14, x0:x1] = (214, 40, 36)
    img = Image.fromarray(a)
    cx = (x0 + x1) / 2
    img = text(img, name, cx, y0 + 7, 8, (255, 250, 230))
    img = text(img, big, cx - 6, y0 + 36, 32, (200, 30, 30))
    img = text(img, '*', x1 - 12, y0 + 24, 8, (200, 30, 30))
    img = text(img, foot[0], cx, y1 - 22, 8, (90, 70, 20))
    img = text(img, foot[1], cx, y1 - 10, 8, (90, 70, 20))
    return img


def shop():
    img = Image.fromarray(q(Image.open(BG / 'shop.png').convert('RGB')))
    img = price_tag(img)
    a = np.array(img)
    x0, y0, x1, y1 = LCD
    a[y0 - 3:y1 + 3, x0 - 3:x1 + 3] = (30, 30, 34)                         # display housing
    a[y0:y1, x0:x1] = (12, 30, 16)                                          # dark green LCD glass
    a[y1 + 3:340, (x0 + x1) // 2 - 3:(x0 + x1) // 2 + 3] = (60, 60, 66)    # pole
    return Image.fromarray(a)


def lcd_digits(world_view_big, v, txt, col=(120, 255, 140)):
    """draw green digits on the shop LCD (output frame, via the view)"""
    from overlays import pfont
    x0, y0 = v.opt(LCD[0], LCD[1]); x1, y1 = v.opt(LCD[2], LCD[3])
    w, h = int(x1 - x0), int(y1 - y0)
    if w < 12 or h < 8: return
    f = pfont(max(8, int(h * 0.62) // 8 * 8))
    bb = f.getbbox(txt)
    img = Image.new('L', (w, h), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text(((w - (bb[2] - bb[0])) // 2 - bb[0], (h - (bb[3] - bb[1])) // 2 - bb[1]), txt, font=f, fill=255)
    m = np.array(img) > 127
    X0, Y0 = int(x0), int(y0)
    big = world_view_big
    ys, xs = np.nonzero(m)
    ys = ys + Y0; xs = xs + X0
    ok = (ys >= 0) & (ys < big.shape[0]) & (xs >= 0) & (xs < big.shape[1])
    big[ys[ok], xs[ok]] = col


def counter_occluder(world):
    Hh, Ww = world.shape[:2]
    m = Image.new('L', (Ww, Hh), 0)
    ImageDraw.Draw(m).polygon(COUNTER_EDGE + [(1280, 720), (880, 720)], fill=1)
    m = np.array(m).astype(bool)
    x0, x1, y0, y1 = 870, 1280, 415, 720
    spr = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    spr[..., :3] = world[y0:y1, x0:x1]; spr[..., 3] = np.where(m[y0:y1, x0:x1], 255, 0)
    return spr, x0, y0


# ---------------------------------------------------------------- courtyard (wide) + entrance/bench close-up
Y_BENCH = (465, 608, 522)               # wide yard: bench x0, x1, seat y
Y_DOOR = (345, 402, 422, 540)
Y_WINDOW = (395, 165, 478, 230)         # Valera's lit window on the 2nd floor
Y_SANDBOX = (728, 540, 918, 585)
Y_UNIT = 4.8                            # seated grannies / Valera at the facade depth
B_SEAT = 553                            # close-up: bench seat y
B_ZINA = (712.0, 553.0, 12.5)           # seated anchors (hips on the seat)
B_LYUBA = (872.0, 553.0, 12.5)
B_DOOR_EDGE = 497                       # right edge of the door (Valera peeks out here)
B_FLOOR = 690
B_UNIT = 14.5
B_NOTICE = (655, 296, 845, 414)


def bench_world(notice_lines, crossed=(), hand=()):
    img = Image.fromarray(q(Image.open(BG / 'bench.png').convert('RGB')))
    return np.array(notice(img, notice_lines, B_NOTICE, crossed, hand))


# ---------------------------------------------------------------- basement + hot-spring sandbox (E05)
BS_VALVE = (1030.0, 390.0, 70.0)       # handwheel centre + radius
BS_TAG = (1098, 452, 1250, 548)         # cardboard sign «НЕ ТРОГАТЬ!» hung on the valve
BS_BULB = (515.0, 150.0)
BS_GAUGES = [(135.0, 290.0, 26.0), (818.0, 340.0, 12.0)]
BS_JOINTS = [(930.0, 470.0), (250.0, 220.0), (420.0, 360.0), (840.0, 160.0)]
PL_WATER = 505                          # pool close-up: waterline for the grannies
PL_ZINA = (560.0, 640.0, 24.0)          # seated anchors (hips) under water
PL_LYUBA = (830.0, 650.0, 24.0)
PL_X = (170, 1120)
SP_WATER = 598                          # wide yard_spring: waterline
SP_ZINA = (790.0, 628.0, 5.6)
SP_LYUBA = (880.0, 630.0, 5.6)


def basement():
    img = Image.fromarray(q(Image.open(BG / 'basement.png').convert('RGB')))
    a = np.array(img)
    x0, y0, x1, y1 = BS_TAG
    a[y0 + 3:y1 + 3, x0 + 3:x1 + 3] = (a[y0 + 3:y1 + 3, x0 + 3:x1 + 3] * 0.5).astype(np.uint8)
    a[y0:y1, x0:x1] = (196, 168, 120)                                   # cardboard
    a[y0:y0 + 3, x0:x1] = (150, 124, 84); a[y1 - 3:y1, x0:x1] = (150, 124, 84)
    img = Image.fromarray(a)
    img = text(img, 'НЕ', (x0 + x1) / 2, y0 + 20, 16, (180, 30, 30))
    img = text(img, 'ТРОГАТЬ!', (x0 + x1) / 2, y0 + 46, 16, (180, 30, 30))
    img = text(img, 'ЖЭК №3', (x0 + x1) / 2, y0 + 74, 8, (60, 40, 30))
    a = np.array(img)
    for k in range(6):                                                  # wire to the wheel
        a[y0 - 2 - k * 6:y0 - k * 6, x0 + 30 - k * 5:x0 + 34 - k * 5] = (140, 140, 150)
    return a


def clip_below(CH, v, wy, x0=-1e9, x1=1e9):
    """hide Chars pixels whose world y is below the waterline wy (inside world x-range) — bathers in a pool"""
    import stage as ST
    k = ST.PX[0]
    h, w = CH.m.shape
    ys = (np.arange(h) + 0.5) * k                                        # logical px
    xs = (np.arange(w) + 0.5) * k
    wy_rows = v.Y0 + (ys - v.oy) / v.Z
    wx_cols = v.X0 + xs / v.Z
    m = (wy_rows[:, None] > wy) & (wx_cols[None, :] > x0) & (wx_cols[None, :] < x1)
    CH.m &= ~m


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
    shp = np.array(shop())
    yard = q(Image.open(BG / 'yard.png').convert('RGB'))
    cnt, cx_, cy_ = counter_occluder(shp)
    out = dict(kitchen=kit, bath=bath, stair=stair, tub=tub, tub_xy=np.array([tx, ty]), shop=shp, counter=cnt,
               counter_xy=np.array([cx_, cy_]), yard=yard,
               glow_k=glow_map(kit.shape[:2], [LAMP_K], 260), glow_b=glow_map(bath.shape[:2], [BULB], 220),
               glow_s=glow_map(stair.shape[:2], [LAMP_S], 240))
    np.savez_compressed(cache, **out)
    return out


if __name__ == '__main__':
    d = build(True)
    for k in ('kitchen', 'bath', 'stair'):
        Image.fromarray(d[k]).save(PATHS.build('props', f'{k}.png'))
    print('ok', {k: v.shape for k, v in d.items()})
