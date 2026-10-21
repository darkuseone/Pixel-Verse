"""CTR cover 1920x1080 for «СЛЕДСТВИЕ ПО БЕНЗИНУ» (own idea, not the face+sunburst template of other movies):
Мазутыч the detective, a giant shocked face, holds a magnifying glass over the valve plate with HIS OWN name; behind him the tank
«ПЛАН 148%» bursts with a fountain of golden gasoline; warm sunset-orange refinery sky. Text «ЭТО Я?!» top-right; a yellow-black
case-file tag «ДЕЛО №1: БЕНЗИН» small. Bottom-right timestamp zone empty.
  python3 cover.py -> cover.png + cover.jpg (<= 2 MB) + cover_small.png (320x180)"""
import math
import movie as MV
from movie import *

t = 0.4
OUTD = HERE


def sprite_rgba(fn, s, size, head, flip=False, **kw):
    """sprite rendered on a key colour -> RGBA with a sticker outline (thick white + ink)"""
    key = (255, 0, 255)
    a = MV.portrait(fn, s, size, bg=key, head=head, flip=flip, **kw)
    m = ~((a[..., 0] == 255) & (a[..., 1] == 0) & (a[..., 2] == 255))
    out = np.zeros(a.shape[:2] + (4,), np.uint8)
    pad = 26
    big_m = np.pad(m, pad)
    d1 = O._dilate(big_m, 14)[pad:-pad, pad:-pad] if hasattr(O, '_dilate') else m
    d2 = O._dilate(big_m, 22)[pad:-pad, pad:-pad] if hasattr(O, '_dilate') else m
    out[d2] = (30, 20, 16, 255)
    out[d1] = (255, 255, 255, 255)
    out[m, :3] = a[m]; out[m, 3] = 255
    return out


# background: the tank farm, warm and saturated, the tank with its plan number and a gasoline fountain
v = view_at(TANK, 760.0, 330.0, 1.05, SX, SY)
bg = v.bg().astype(float)
H, W = bg.shape[:2]
g = bg.mean(2, keepdims=True)
bg = np.clip(g + (bg - g) * 1.6, 0, 255) * 1.3 + 20
yy, xx = np.mgrid[0:H, 0:W]
for (cx, cy, c, r) in ((1300, 120, (255, 150, 40), 900), (300, 900, (255, 70, 40), 700), (1700, 600, (255, 210, 60), 600)):
    k = np.clip(1 - np.hypot(xx - cx, yy - cy) / r, 0, 1)[..., None] ** 1.4
    bg = bg * (1 - 0.5 * k) + np.array(c) * 0.5 * k
big = np.clip(bg, 0, 255).astype(np.uint8)
big[:] = M.dof(big, 3)
MV.tank_fx(t, 148, hose=False)(big, v)
# the fountain from the tank seam
for i in range(160):
    ph = i / 160
    x = int(1180 + ph * 700 + 40 * math.sin(i))
    y = int(520 - math.sin(ph * math.pi) * 420 + 20 * math.cos(i * 1.7))
    s_ = 22 if i % 4 else 30
    if 0 <= x < W - s_ and 0 <= y < H - s_:
        big[y:y + s_, x:x + s_] = (255, 214, 90) if i % 5 else (190, 120, 255)
fx.glow(big, 1500, 360, 700, (255, 220, 120), 0.35)

# the hero: a huge shocked face, left
hero = sprite_rgba(MC.maz, 15.5, (1100, 1300), head=(0.42, 0.36), expr='shock', look=(0.7, 0.5), beacon=True, ride=False, mouth_=1.0,
                   t=1.0)
O.overlay(big, hero, -60, -60, 1.0)

# magnifying glass over the plate with his name
gx, gy, gr = 1150, 760, 210
plate = Image.new('RGB', (2 * gr, 2 * gr), (250, 230, 120)); d = ImageDraw.Draw(plate); d.fontmode = '1'
d.rectangle([10, 90, 2 * gr - 10, 2 * gr - 90], fill=(250, 230, 120), outline=INK, width=8)
d.text((gr, 150), 'ОТВЕТСТВ.:', font=O.pfont(30), fill=INK, anchor='mm')
d.text((gr, 230), 'МАЗУРОВ', font=O.pfont(46), fill=(200, 30, 36), anchor='mm')
d.text((gr, 300), 'Г.П.', font=O.pfont(44), fill=(200, 30, 36), anchor='mm')
pa = np.array(plate)
yy2, xx2 = np.mgrid[0:2 * gr, 0:2 * gr]
circ = np.hypot(xx2 - gr, yy2 - gr) <= gr
reg = big[gy - gr:gy + gr, gx - gr:gx + gr]
reg[circ] = pa[circ]
ring = (np.hypot(xx2 - gr, yy2 - gr) <= gr) & (np.hypot(xx2 - gr, yy2 - gr) > gr - 26)
reg[ring] = (60, 60, 66)
ring2 = (np.hypot(xx2 - gr, yy2 - gr) <= gr - 26) & (np.hypot(xx2 - gr, yy2 - gr) > gr - 34)
reg[ring2] = (200, 200, 210)
for k in range(40):                                                         # the handle towards the hero's hand
    x, y = int(gx - gr * 0.7 - k * 9), int(gy + gr * 0.7 + k * 7)
    big[y - 22:y + 22, x - 22:x + 22] = INK
    big[y - 16:y + 16, x - 16:x + 16] = (120, 70, 40)
big[gy - gr + 40:gy - gr + 70, gx - 120:gx - 60] = (255, 255, 255)             # glint

# text: «ЭТО Я?!» top-right + case tag
title = K.hook_title(['ЭТО Я?!'], 140, width=1160)
O.overlay(big, title, 760, 10, 1.0)
tag = Image.new('RGBA', (560, 90), (0, 0, 0, 0)); d = ImageDraw.Draw(tag); d.fontmode = '1'
d.rectangle([0, 0, 559, 89], fill=(250, 214, 40, 255), outline=(20, 16, 14, 255), width=6)
for k in range(0, 560, 40): d.polygon([(k, 89), (k + 20, 89), (k + 40, 70), (k + 20, 70)], fill=(20, 16, 14, 255))
d.text((280, 34), 'ДЕЛО: БЕНЗИН', font=O.pfont(36), fill=(20, 16, 14), anchor='mm')
O.overlay(big, np.array(tag.rotate(-4, expand=True, resample=Image.NEAREST)), 1180, 300, 1.0)

Image.fromarray(big).save(OUTD / 'cover.png')
Image.fromarray(big).save(OUTD / 'cover.jpg', quality=90)
Image.fromarray(big).resize((320, 180), Image.LANCZOS).save(OUTD / 'cover_small.png')
print(OUTD / 'cover.png', (OUTD / 'cover.jpg').stat().st_size // 1024, 'KB')
