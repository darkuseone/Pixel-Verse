"""CTR cover 1920x1080 for «ПРОПУСКНОЙ РЕЖИМ» (docs/covers.md §«Обложка длинного видео 16:9»): one dominant face — Kolyan as an
unshaven Snegurochka in shock (~45 % of the height, left), granny Zina smaller with binoculars (right), warm RU sunburst, 1 huge word
«ПРОПУСК?!» top-right, bottom-right timestamp zone empty.
  python3 cover.py -> cover.png + cover.jpg (<= 2 MB) + cover_small.png (320x180)"""
import math
import movie as MV
from movie import *

t = 0.5
v0 = view_at(BENCH, 640, 360, 1.0, SX, SY)


def heroes(CH):
    x, y, un = 1000.0, 1000.0, 15.0
    vh = MV.hview(BENCH, x + 1.6 * un, y - 23.4 * un, 2.15, 205, 205)
    M.kolyan(CH, vh.cam(x, y, un), M.STAND, t, 0.9, 'shock', costume='snegurochka', look=0.6)
    vz = MV.hview(BENCH, 1000 - 1.0 * 12.5, 1000 - 11.8 * 12.5, 1.6, 505, 200)
    F.babushka(CH, vz.cam(1000, 1000, 12.5, flip=True), t, 'zina', 'sit', 0.0, 'smug', hand_n=F.H(2.8, 12.0),
               prop_n=lambda L, h: MV.binoculars(L, (h[0] - 0.6, h[1] - 0.2)))


plain = v0.bg()
full = plain.copy()
CH, _ = MV.begin(); heroes(CH); CH.comp(full, MV.light_bench(v0))
mask = (np.abs(full.astype(int) - plain.astype(int)).sum(2) > 6)
H, W = full.shape[:2]
yy, xx = np.mgrid[0:H, 0:W]
cx, cy = 620, 560
ang = np.arctan2(yy - cy, xx - cx); r = np.hypot(yy - cy, xx - cx)
ray = (np.floor((ang + math.pi) / (2 * math.pi) * 18) % 2).astype(bool)
bg = np.where(ray[..., None], np.array([255, 200, 60]), np.array([255, 128, 40])).astype(float)
glow = np.clip(1 - r / 900, 0, 1)[..., None]
bg = bg * (0.7 + 0.3 * glow) + np.array([255, 246, 190]) * (glow ** 3) * 0.8
red = np.clip((xx - 1200) / 720, 0, 1)[..., None]
bg = bg * (1 - red * 0.55) + np.array([200, 36, 44]) * red * 0.55
loc = np.array(Image.fromarray(plain).filter(ImageFilter.GaussianBlur(9))).astype(float)
bg = bg * 0.82 + loc * 0.18
px = 12
small = bg[::px, ::px]
bg = np.repeat(np.repeat(small, px, 0), px, 1)[:H, :W]
big = np.clip(bg, 0, 255).astype(np.uint8)
rng = np.random.default_rng(4)
for _ in range(160):                                                   # snow
    x = int(rng.uniform(0, W - 8)); y = int(rng.uniform(0, H - 8)); s_ = int(rng.choice([6, 8, 10]))
    big[y:y + s_, x:x + s_] = (255, 255, 255)
P_ = 30
mp = np.pad(mask, P_)
ol_w = O._dilate(mp, 14)[P_:-P_, P_:-P_] & ~mask
ol_d = O._dilate(mp, 24)[P_:-P_, P_:-P_] & ~mask & ~ol_w
big[ol_d] = (40, 18, 12); big[ol_w] = (255, 255, 255)
big[mask] = full[mask]
from endcard import _trim
ti = _trim(O.winter_title(['ПРОПУСК?!'], 136, width=1900))
O.overlay(big, ti, 1920 - ti.shape[1] - 40, 40, 1.0)
tag = MV.badge('ВАЛЕРА И КОТ • НОВОГОДНИЙ ФИЛЬМ', 30)
O.overlay(big, tag, 1920 - tag.shape[1] - 60, 60 + ti.shape[0], 1.0)
im = Image.fromarray(big)
im.save(MV.HERE / 'cover.png')
im.resize((320, 180), Image.LANCZOS).save(MV.HERE / 'cover_small.png')
q = 92
while True:
    im.save(MV.HERE / 'cover.jpg', quality=q)
    if (MV.HERE / 'cover.jpg').stat().st_size <= 2_000_000 or q < 60: break
    q -= 4
print(MV.HERE / 'cover.jpg', (MV.HERE / 'cover.jpg').stat().st_size)
