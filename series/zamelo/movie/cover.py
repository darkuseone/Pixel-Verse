"""CTR cover 1920x1080 for «ЗАМЕЛО! СОБРАНИЕ ЖИЛЬЦОВ» (MrBeast-style «about to happen», owner 16.11.2026):
one huge terrified face (Жора, ~50 % of the height, left), a GIANT УК receipt «50 400 ₽» falling on him from the top right (the moment
before impact, motion lines + its shadow on him), the smug neighbours behind voting «ЗА!» with raised hands (contrast emotion),
a bright warm RU sunburst, thick white + navy sticker outlines, the bottom-right timestamp corner empty.
  python3 cover.py -> cover.png + cover.jpg (<= 2 MB) + cover_small.png (320x180 phone preview)"""
import os
os.environ['PV_WIDE'] = '1'
import sys, math, pathlib
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine'))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import overlays as O
from props import zampix as ZX, zamcast as C, zamkit as K
from props.dibspix import blit

W, H = 1920, 1080
KEY = np.array((1, 254, 3), np.uint8)
t = 0.4


def layer(fn, scale, x, y, **kw):
    """draw a sprite on a key-coloured canvas with its HEAD at the output point (x, y) -> (rgb, mask)"""
    can = np.zeros((H, W, 3), np.uint8); can[:] = KEY
    sp = ZX.draw(fn, scale, t=t, **kw)
    hx, hy = sp.anchors.get('head', (0.0, 0.0))
    if kw.get('flip'): hx = -hx
    blit(can, sp, x - hx * scale, y + hy * scale, scale, None, False)
    m = np.any(can != KEY, axis=2)
    return can, m


def stick(big, rgb, m, w_in=12, w_out=22, col=(24, 30, 70)):
    P = 40
    mp = np.pad(m, P)
    a = O._dilate(mp, w_in)[P:-P, P:-P] & ~m
    b = O._dilate(mp, w_out)[P:-P, P:-P] & ~m & ~a
    big[b] = col; big[a] = (255, 255, 255); big[m] = rgb[m]


# ---------------------------------------------------------------- background: warm sunburst + a hint of the snowy landing, pixelated
yy, xx = np.mgrid[0:H, 0:W]
cx, cy = 560, 560
ang = np.arctan2(yy - cy, xx - cx); r = np.hypot(yy - cy, xx - cx)
ray = (np.floor((ang + math.pi) / (2 * math.pi) * 20) % 2).astype(bool)
c1, c2 = np.array([255, 196, 40]), np.array([255, 120, 30])
bg = np.where(ray[..., None], c1, c2).astype(float)
glow = np.clip(1 - r / 1000, 0, 1)[..., None]
bg = bg * (0.7 + 0.3 * glow) + np.array([255, 250, 200]) * (glow ** 3) * 0.7
red = np.clip((xx - 1100) / 820, 0, 1)[..., None]
bg = bg * (1 - red * 0.55) + np.array([230, 40, 60]) * red * 0.55
land = np.array(Image.open(ROOT / 'series' / 'zamelo' / 'bg' / 'landing.png').convert('RGB').resize((W, H)).filter(ImageFilter.GaussianBlur(8)),
                float)
bg = bg * 0.8 + land * 0.2
px = 12
bg = np.repeat(np.repeat(bg[::px, ::px], px, 0), px, 1)[:H, :W]
big = np.clip(bg, 0, 255).astype(np.uint8)
snow = (yy > 950 + 20 * np.sin(xx / 70.0))                      # a snowdrift along the bottom (the series' snow)
big[snow] = (236, 242, 255)

# ---------------------------------------------------------------- the neighbours behind, voting «ЗА!» (smaller, smug)
for fn, x, y, s, kw in ((C.gosha, 1270, 560, 6.6, dict(expr='smug', mouth_=0.6, hand_f=(-12.0, 86.0), hand_n=(14.0, 40.0),
                                                        look=(-0.8, 0.0))),
                        (C.nina, 1520, 640, 6.4, dict(expr='kind', mouth_=0.5, hand_n=(10.0, 70.0), look=(-0.8, 0.0))),
                        (C.vitek, 1760, 560, 6.4, dict(expr='cheerful', mouth_=0.6, hand_n=(10.0, 82.0), look=(-0.8, 0.0)))):
    rgb, m = layer(fn, s, x, y, flip=True, **kw)
    stick(big, rgb, m, 8, 14)

# ---------------------------------------------------------------- the falling giant receipt (top right) + its shadow on Жора
rw, rh = 520, 640
rc = Image.new('RGBA', (rw // 4, rh // 4), (0, 0, 0, 0)); d = ImageDraw.Draw(rc); d.fontmode = '1'
d.rectangle([0, 0, rw // 4 - 1, rh // 4 - 1], fill=(252, 250, 238, 255), outline=(120, 120, 120, 255))
for x in range(0, rw // 4, 6): d.polygon([(x, rh // 4 - 1), (x + 3, rh // 4 - 5), (x + 6, rh // 4 - 1)], fill=(0, 0, 0, 0))


def tx(y, s, size, col):
    f = O.pfont(size)
    while f.getlength(s) > rw // 4 - 10 and size > 4: size -= 1; f = O.pfont(size)
    d.text(((rw // 4 - f.getlength(s)) / 2, y), s, font=f, fill=col)


tx(8, 'УК «СУГРОБ-СЕРВИС»', 10, (30, 60, 150))
tx(26, 'СТАРШЕМУ ПО ДОМУ', 7, (80, 80, 90))
d.line([(8, 40), (rw // 4 - 8, 40)], fill=(120, 120, 130))
tx(50, 'УБОРКА СНЕГА', 9, (40, 40, 50))
tx(64, 'ВЕСЬ ДОМ', 9, (40, 40, 50))
tx(96, '50 400', 30, (220, 30, 40))
tx(132, 'РУБЛЕЙ', 12, (220, 30, 40))
tx(156, 'ДО ПЯТНИЦЫ!', 9, (40, 40, 50))
rc = rc.resize((rw, rh), Image.NEAREST).rotate(-18, resample=Image.NEAREST, expand=True)
rca = np.array(rc)
ox, oy = 560, -30
# motion lines above the receipt (it falls)
for q in range(7):
    x0 = ox + 80 + q * 70
    big[max(0, oy + 20 + (q % 2) * 30):max(0, oy + 110 + (q % 2) * 30), x0:x0 + 12] = (255, 255, 255)
shadow = Image.new('L', (W, H), 0)
ImageDraw.Draw(shadow).ellipse([260, 300, 980, 560], fill=120)
sh = np.array(shadow.filter(ImageFilter.GaussianBlur(30)), float)[..., None] / 255.0

# ---------------------------------------------------------------- Жора: the huge terrified face, looking up at the receipt
rgb, m = layer(C.zhora, 19.0, 470, 760, expr='shock', mouth_=1.0, look=(0.5, 1.0), blink=False, sweat=2.0, frost=0.0,
               hand_n=(30.0, 92.0), hand_f=(-26.0, 92.0))
stick(big, rgb, m, 14, 26)
big[:] = np.clip(big.astype(float) * (1 - sh * 0.45), 0, 255).astype(np.uint8)     # the receipt's shadow falls on him

# the receipt itself, with a sticker outline
ra = rca[..., 3] > 0
rr = np.zeros((H, W, 3), np.uint8); mm = np.zeros((H, W), bool)
sy0 = max(0, -oy); dy0 = max(0, oy)
hh, ww = min(rca.shape[0] - sy0, H - dy0), min(rca.shape[1], W - ox)
rr[dy0:dy0 + hh, ox:ox + ww] = rca[sy0:sy0 + hh, :ww, :3]; mm[dy0:dy0 + hh, ox:ox + ww] = ra[sy0:sy0 + hh, :ww]
stick(big, rr, mm, 10, 18)

# ---------------------------------------------------------------- the series plate (small, top-left)
pl = K.badge(0)
im = Image.new('RGBA', (430, 64), (0, 0, 0, 0)); dd = ImageDraw.Draw(im); dd.fontmode = '1'
dd.rounded_rectangle([0, 0, 429, 63], 12, fill=(250, 250, 250, 240)); dd.rounded_rectangle([5, 5, 424, 58], 9, fill=(32, 84, 176, 240))
dd.text((26, 20), 'ЗАМЕЛО! • ФИЛЬМ', font=O.pfont(22), fill=(255, 255, 255))
O.overlay(big, np.array(im), 40, 36, 1.0)

out = Image.fromarray(big)
out.save(HERE / 'cover.png')
out.resize((320, 180), Image.LANCZOS).save(HERE / 'cover_small.png')
q = 92
while True:
    out.save(HERE / 'cover.jpg', quality=q)
    if (HERE / 'cover.jpg').stat().st_size <= 2_000_000 or q < 60: break
    q -= 4
print(HERE / 'cover.jpg', (HERE / 'cover.jpg').stat().st_size)
