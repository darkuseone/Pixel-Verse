"""CTR cover v2 (28.10.2026, YouTube CTR of v1 = 0.86-0.97 %: dark night, six equal small figures, unreadable in 320x180).
One huge shocked Valera face left, granny Zina right slamming a striped barrier across his chest («НЕ ПУЩУ!»), the cat sitting
on the barrier, warm yellow-orange-red sunburst, garland + snow. Bottom-right timestamp corner empty.
  python3 cover_ctr.py      -> cover_ctr.png/.jpg/_small.png (code only)
  python3 cover_ctr.py xai  -> the same scene as a reference -> xAI edit x2 -> pixelized -> same title: cover_xai1/2.*"""
import sys, math
import movie as MV
from movie import *
import thumb16 as T

t = 0.37
WV = np.zeros((1200, 2400, 3), np.uint8)
v = View(WV, 0, 0, 1.0)
Wd, Hd = ST.OUT_W, ST.OUT_H
LG = 1 / ST.UP                                            # output px -> logical px

big = T.sunburst(Wd, Hd, (1000, 520), [(255, 206, 40), (255, 140, 30), (236, 70, 40)], rays=24, px=8, core_r=380)
rng = np.random.default_rng(3)
for _ in range(90):                                       # snow: pixel flakes
    x, y = int(rng.uniform(0, Wd - 16)), int(rng.uniform(0, Hd - 16)); s = int(rng.choice([8, 8, 16]))
    if x > Wd - 300 and y > Hd - 140: continue
    big[y:y + s, x:x + s] = (255, 255, 255)

# Valera: huge shocked face, left, facing right
val = T.rgba(lambda CH: F.valera(CH, v.cam(130, 720, 26.5), F.VPOSE['stand'], t, 1.0, 'shock', 'street', look=0.5, stubble=1.0), MV.begin)
O.overlay(big, T.sticker(T.boost(val)), 0, 0, 1.0)

# Zina: standing right, flipped (faces left), shouting, her near hand holding the barrier boom
ZX, ZY, ZU = 1460 * LG, 1110 * LG, 13.0
zina = T.rgba(lambda CH: F.babushka(CH, v.cam(ZX, ZY, ZU, flip=True), t, 'zina', 'stand', 1.0, 'angry', hand_n=F.H(7.0, 11.5)),
              MV.begin)
hx, hy = (ZX - 7.0 * ZU) * ST.UP, (ZY - 11.5 * ZU) * ST.UP
O.overlay(big, T.sticker(T.boost(zina)), 0, 0, 1.0)

# the barrier boom: from her hand across Valera's chest (in front of him)
im = Image.fromarray(big); d = ImageDraw.Draw(im)
x0, y0, x1, y1 = hx + 40, hy - 6, 300, hy + 110
d.line([(x0, y0), (x1, y1)], fill=(28, 16, 12), width=70)
d.line([(x0, y0), (x1, y1)], fill=(255, 255, 255), width=56)
n = 9
for k in range(n):
    if k % 2: continue
    a = (x0 + (x1 - x0) * k / n, y0 + (y1 - y0) * k / n); b = (x0 + (x1 - x0) * (k + 1) / n, y0 + (y1 - y0) * (k + 1) / n)
    d.line([a, b], fill=(222, 30, 36), width=44)
big = np.array(im)
kpp = T.pixel_text('КПП', 44, (222, 30, 36), bg=(255, 236, 120), border=(28, 16, 12), pad=8)
kx = 640; ky = y0 + (y1 - y0) * (x0 - kx) / (x0 - x1) + 26                # hangs right under the boom
O.overlay(big, T.rot(kpp, -4), int(kx - kpp.shape[1] / 2), int(ky), 1.0)

# the cat sits on the boom, deadpan-smug, looking at the viewer
cx = 1010
cy = y0 + (y1 - y0) * (x0 - cx) / (x0 - x1) - 26
cat = T.rgba(lambda CH: F.cat(CH, v.cam(cx * LG, cy * LG, 4.6), t=t, pose='sit', mouth=0.0, lid=0.6, look=(0.0, 0.2), expr='smug',
                              tail=0.6), MV.begin)
O.overlay(big, T.sticker(T.boost(cat), 7, 12), 0, 0, 1.0)

# the olivier basin Valera is not allowed to bring home (bottom, in his hand zone)
def add_text(big):
    from endcard import _trim
    ti = _trim(O.winter_title(['НЕ ПУЩУ!'], 140, width=1300))
    O.overlay(big, ti, Wd - ti.shape[1] - 30, 18, 1.0)
    tag = MV.badge('ВАЛЕРА И КОТ • ФИЛЬМ', 30)
    O.overlay(big, tag, 40, Hd - tag.shape[0] - 40, 1.0)
    fx.vignette(big, 0.18)
    return big


if 'xai' in sys.argv:
    for i, a in enumerate(T.ai_versions(big, MV.HERE, fresh='new' in sys.argv, emotion="the man in the ushanka is SCREAMING in shock with a huge open mouth and "
                                         "bulging eyes, the old lady in glasses is furiously yelling and blocking him with the red-white "
                                         "barrier, the ginger cat sitting on the barrier looks smug and unimpressed.")):
        k2 = T.rot(T.pixel_text('КПП', 60, (222, 30, 36), bg=(255, 236, 120), border=(28, 16, 12), pad=20), -3)
        O.overlay(a, k2, 642 - k2.shape[1] // 2, 842 - k2.shape[0] // 2, 1.0)          # xAI leaves the plate blank
        T.save(add_text(a), MV.HERE, f'cover_xai{i + 1}')
else:
    T.save(add_text(big), MV.HERE, 'cover_ctr')
