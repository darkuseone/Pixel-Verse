"""CTR cover 1920x1080 for «Дембельский альбом» (docs/covers.md §«Обложка длинного видео 16:9»): one dominant face — Nina Petrovna
from the ZhEK screaming under the icy shower in Valera's bath (~45 % of the height, left), Valera smaller with his «Зенит» (sly),
warm RU sunburst instead of the bathroom, icy spray, 1 huge word «ЛЕДЯНАЯ!» top-right, bottom-right timestamp zone empty.
  python3 cover.py -> cover.png + cover.jpg (<= 2 MB) + cover_small.png (320x180)"""
import math
import movie as M
from movie import *
from PIL import Image

t = 0.5
v0 = view_at(BATH, 640, 360, 1.0, SX, SY)


def heroes(CH):
    x, y, un = M.NB
    hx, hy = x - 0.95 * un, y - 9.5 * un
    vh = M.hview(BATH, hx, hy, 1.68, 196, 214)
    F.nina(CH, vh.cam(x, y, un, flip=True), t, 0.95, 'shock', True, cap_=True, cold=0.85, foam=False)
    x2, y2, u2 = 1000.0, 1000.0, 15.0
    fx_, fy_ = K.face_w(x2, y2, u2, flip=True, h=20.6)
    vv = M.hview(BATH, fx_, fy_, 0.78, 478, 196)
    F.valera(CH, vv.cam(x2, y2, u2, flip=True), dict(F.VPOSE['phone'], n=(2.6, 21.2), f=(3.6, 20.4)), t, 0.0, 'sly', 'home',
             hat='ushanka', prop_n=lambda L, h: M.zenit(L, (h[0] - 0.4, h[1])))


plain = v0.bg()
full = plain.copy()
CH, _ = M.begin(); heroes(CH); CH.comp(full, K.light_cold(v0))
mask = (np.abs(full.astype(int) - plain.astype(int)).sum(2) > 6)
H, W = full.shape[:2]
# warm RU sunburst (yellow / orange / red) centred behind the main face, icy blue on the far left where the water comes from
yy, xx = np.mgrid[0:H, 0:W]
cx, cy = 600, 560
ang = np.arctan2(yy - cy, xx - cx); r = np.hypot(yy - cy, xx - cx)
ray = (np.floor((ang + math.pi) / (2 * math.pi) * 18) % 2).astype(bool)
c1, c2 = np.array([255, 196, 60]), np.array([255, 120, 40])
bg = np.where(ray[..., None], c1, c2).astype(float)
glow = np.clip(1 - r / 900, 0, 1)[..., None]
bg = bg * (0.7 + 0.3 * glow) + np.array([255, 246, 190]) * (glow ** 3) * 0.8
red = np.clip((xx - 1200) / 720, 0, 1)[..., None]
bg = bg * (1 - red * 0.6) + np.array([214, 40, 44]) * red * 0.6
bath = np.array(Image.fromarray(plain).filter(ImageFilter.GaussianBlur(9))).astype(float)
bg = bg * 0.82 + bath * 0.18
px = 12
small = bg[::px, ::px]
bg = np.repeat(np.repeat(small, px, 0), px, 1)[:H, :W]
big = np.clip(bg, 0, 255).astype(np.uint8)
# icy spray falling on her (behind the outline), cold streaks
rng = np.random.default_rng(3)
for _ in range(260):
    x = int(rng.uniform(150, 1050)); y = int(rng.uniform(-40, 1000)); L_ = int(rng.uniform(30, 80))
    big[max(0, y):min(H, y + L_), x:x + 6] = (196, 232, 255)
P_ = 30
mp = np.pad(mask, P_)
ol_w = O._dilate(mp, 14)[P_:-P_, P_:-P_] & ~mask
ol_d = O._dilate(mp, 24)[P_:-P_, P_:-P_] & ~mask & ~ol_w
big[ol_d] = (40, 18, 12); big[ol_w] = (255, 255, 255)
big[mask] = full[mask]
for _ in range(120):                                                   # a few drops in front of her
    x = int(rng.uniform(200, 1000)); y = int(rng.uniform(0, 1000)); L_ = int(rng.uniform(20, 50))
    big[y:min(H, y + L_), x:x + 5] = (226, 244, 255)
from endcard import _trim
ti = _trim(O.winter_title(['ЛЕДЯНАЯ!'], 136, width=1900))
O.overlay(big, ti, 1920 - ti.shape[1] - 40, 40, 1.0)
tag = M.badge('ВАЛЕРА И КОТ • ДЕМБЕЛЬСКИЙ АЛЬБОМ', 30)
O.overlay(big, tag, 1920 - tag.shape[1] - 60, 60 + ti.shape[0], 1.0)
im = Image.fromarray(big)
im.save(M.HERE / 'cover.png')
im.resize((320, 180), Image.LANCZOS).save(M.HERE / 'cover_small.png')
q = 92
while True:
    im.save(M.HERE / 'cover.jpg', quality=q)
    if (M.HERE / 'cover.jpg').stat().st_size <= 2_000_000 or q < 60: break
    q -= 4
print(M.HERE / 'cover.jpg', (M.HERE / 'cover.jpg').stat().st_size)
