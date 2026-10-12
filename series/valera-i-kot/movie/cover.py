"""CTR cover 1920x1080 for «ПРОПУСКНОЙ РЕЖИМ» — a staged scene, not the face+sunburst template (owner, 12.10.2026):
the entrance bench turned into a border checkpoint: a striped barrier with «ПРЕДЪЯВИТЕ ОЛИВЬЕ», granny Zina raising a «СТОЙ!» sign,
Lyuba with binoculars and the visitors log, a queue of Ded Moroz (Semenych), an unshaven Snegurochka (Kolyan) and Valera with a white
towel flag and a basin of olivier; the cat on the canopy listening through a tin can on a string; New-Year fireworks glow, confetti.
Title «ПРОПУСК ЕСТЬ?!» top-left; bottom-right timestamp zone empty.
  python3 cover.py -> cover.png + cover.jpg (<= 2 MB) + cover_small.png (320x180)"""
import math
import movie as MV
from movie import *

t = 0.37
Z = 0.62
v = view_at(BENCH, 640, 380, Z, SX, SY)
BFv, U = PK.B_FLOOR, PK.B_UNIT
CAT_C = (1062.0, 216.0, 5.4)                    # the cat sitting on the mailbox


def octagon_sign(txt, r=150):
    im = Image.new('RGBA', (2 * r + 20, 2 * r + 20), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = r + 10
    pts = [(c + r * math.cos(math.pi / 8 + k * math.pi / 4), c + r * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    d.polygon(pts, fill=(255, 255, 255, 255))
    pts2 = [(c + (r - 12) * math.cos(math.pi / 8 + k * math.pi / 4), c + (r - 12) * math.sin(math.pi / 8 + k * math.pi / 4)) for k in range(8)]
    d.polygon(pts2, fill=(214, 30, 36, 255))
    f = R._font(48)
    d.text((c - f.getlength(txt) / 2, c - 26), txt, font=f, fill=(255, 255, 255, 255))
    return np.array(im)


def draw_world(L):
    """striped barrier + post, the sign stick, thermos on the bench, the string from the cat to Lyuba"""
    F.cap(L, (650, 690), (650, 470), 7, 7, (60, 60, 64))                                   # barrier post
    for k in range(10):                                                                     # striped pole
        a = (650 - k * 26, 478); b = (650 - (k + 1) * 26, 478)
        F.cap(L, a, b, 8.5, 8.5, (220, 30, 36) if k % 2 == 0 else (250, 250, 250))
    F.ell(L, (650, 478), 12, 12, (90, 90, 96))
    F.cap(L, (995, 552), (995, 512), 9, 8, (60, 120, 80), (90, 160, 110), (40, 90, 60))      # thermos
    F.ell(L, (995, 510), 10, 4, (200, 200, 210))


def heroes(CH, v):
    zx, zy, zu = PK.B_ZINA
    lx, ly, lu = PK.B_LYUBA
    # bench crew
    F.babushka(CH, v.cam(lx, ly, lu, flip=True), t, 'lyuba', 'sit', 0.0, 'smug', hand_n=F.H(2.8, 12.0),
               prop_n=lambda L, h: MV.binoculars(L, (h[0] - 0.6, h[1] - 0.2)))
    F.babushka(CH, v.cam(zx, zy, zu, flip=True), t, 'zina', 'sit', 0.7, 'normal', hand_n=F.H(3.6, 15.6))
    # the queue behind the barrier
    F.valera(CH, v.cam(250, BFv, U), F.VPOSE['stand'], t, 0.0, 'sad', 'street', look=0.8, hand_n=F.H(4.4, 13.0),
             prop_n=lambda L, h: MV.towel_flag(L, h, t), hand_f=F.H(3.6, 11.0),
             prop_f=lambda L, h: B.basin(L, (h[0] + 0.4, h[1] - 1.0), fill=(236, 220, 160), scale=0.8))
    M.kolyan(CH, v.cam(385, BFv, U), M.STAND, t, 0.8, 'shock', costume='snegurochka', look=0.8)
    M.semenych(CH, v.cam(530, BFv, U * 0.95), dict(F.VPOSE['shout'], n=(6.0, 23.0)), t, 0.8, 'shout', costume='ded_moroz',
               look=0.8, prop_f=lambda L, h: MV.sack(L, h, t))
    # the cat on the canopy with the tin can
    x, y, un = CAT_C
    cam = v.cam(x, y, un)
    F.cat(CH, cam, t=t, pose='sit', mouth=0.0, lid=0.7, look=(0.5, 0.3), expr='smug', tail=0.6)
    L = Layer(cam); MV.tin_can(L, F.H(3.4, 14.4)); F.outline(L); CH.add(L)


plain = v.bg()
full = plain.copy()
CH, _ = MV.begin()
L = Layer(v.wcam()); draw_world(L); F.outline(L); CH.add(L)
heroes(CH, v)
CH.comp(full, MV.light_bench(v))
mask = (np.abs(full.astype(int) - plain.astype(int)).sum(2) > 6)
H, W = full.shape[:2]

# brighten the night: warm, saturated, fireworks colour washes
bg = plain.astype(float)
g = bg.mean(2, keepdims=True)
bg = np.clip(g + (bg - g) * 1.5, 0, 255) * 1.25 + 18
yy, xx = np.mgrid[0:H, 0:W]
for (cx, cy, c, r) in ((300, 120, (255, 80, 160), 520), (1450, 160, (60, 200, 255), 560), (900, 60, (255, 210, 60), 480),
                       (1700, 700, (255, 120, 40), 500)):
    k = np.clip(1 - np.hypot(xx - cx, yy - cy) / r, 0, 1)[..., None] ** 1.6
    bg = bg * (1 - 0.45 * k) + np.array(c) * 0.45 * k
big = np.clip(bg, 0, 255).astype(np.uint8)
# heroes pop: dark + white outline, then the heroes themselves (also brightened a touch)
P_ = 30
mp = np.pad(mask, P_)
ol_w = O._dilate(mp, 8)[P_:-P_, P_:-P_] & ~mask
ol_d = O._dilate(mp, 14)[P_:-P_, P_:-P_] & ~mask & ~ol_w
big[ol_d] = (30, 14, 10); big[ol_w] = (255, 255, 255)
hf = full.astype(float); hg = hf.mean(2, keepdims=True)
big[mask] = np.clip(hg + (hf - hg) * 1.25, 0, 255)[mask].astype(np.uint8)

# the string: cat's can -> Lyuba's lap
im = Image.fromarray(big); d = ImageDraw.Draw(im)
ax, ay = v.opt(CAT_C[0] + 3.4 * CAT_C[2], CAT_C[1] - 14.4 * CAT_C[2] + 6)
bx, by = v.opt(PK.B_LYUBA[0] - 3.0 * PK.B_LYUBA[2], PK.B_LYUBA[1] - 4.0 * PK.B_LYUBA[2])
pts = [(ax + (bx - ax) * k / 20, ay + (by - ay) * k / 20 + 60 * math.sin(math.pi * k / 20)) for k in range(21)]
d.line(pts, fill=(255, 255, 240), width=5)
cx_, cy_ = bx, by + 10
d.rounded_rectangle([cx_ - 22, cy_ - 30, cx_ + 22, cy_ + 30], 8, fill=(180, 184, 192), outline=(40, 40, 46), width=4)
d.rectangle([cx_ - 22, cy_ - 8, cx_ + 22, cy_ + 12], fill=(200, 40, 40))
big = np.array(im)

# the «СТОЙ!» sign Zina raises, on a stick from her hand
hx, hy = v.opt(PK.B_ZINA[0] - 3.6 * PK.B_ZINA[2], PK.B_ZINA[1] - 15.6 * PK.B_ZINA[2])
im = Image.fromarray(big); d = ImageDraw.Draw(im)
d.line([(hx, hy + 20), (hx - 40, hy - 230)], fill=(40, 30, 20), width=22); d.line([(hx, hy + 20), (hx - 40, hy - 230)], fill=(150, 110, 60), width=14)
big = np.array(im)
st = octagon_sign('СТОЙ!', 130)
O.overlay(big, st, int(hx - 40 - st.shape[1] / 2), int(hy - 230 - st.shape[0] / 2), 1.0)

# props / jokes as plates (fitted Russian lettering)
def plate_at(arr, wx, wy, scale=1.0, tilt=0.0):
    p = Image.fromarray(arr)
    if tilt: p = p.rotate(tilt, resample=Image.NEAREST, expand=True)
    p = p.resize((int(p.width * scale), int(p.height * scale)), Image.NEAREST)
    x, y = v.opt(wx, wy)
    O.overlay(big, np.array(p), int(x - p.width / 2), int(y - p.height / 2), 1.0)


plate_at(R.plate(150, 40, ['ПРЕДЪЯВИТЕ', 'ОЛИВЬЕ'], bg=(255, 236, 120), colors=[(30, 28, 30), (200, 30, 36)], border=(30, 28, 30),
                 bw=1.5, pad=2.5), 535, 505, 0.6, -3)
plate_at(R.plate(110, 52, ['ОЧЕРЕДЬ', 'ЗДЕСЬ →'], bg=(240, 234, 214), colors=[(30, 28, 30), (40, 60, 150)], border=(120, 90, 50),
                 bw=1.5, pad=2.5), 330, 640, 0.5, 4)
plate_at(R.plate(120, 50, ['ЖУРНАЛ', 'ПОСЕЩЕНИЙ'], bg=(60, 100, 60), fg=(250, 240, 200), border=(30, 50, 30), bw=1.5, pad=2.5),
         PK.B_LYUBA[0] - 2 * PK.B_LYUBA[2], PK.B_LYUBA[1] + 30, 0.5, -6)

# confetti + snow
rng = np.random.default_rng(12)
for _ in range(260):
    x = int(rng.uniform(0, W - 14)); y = int(rng.uniform(0, H * 0.75)); c = [(255, 86, 160), (60, 200, 255), (255, 214, 40), (120, 230, 120), (255, 255, 255)][rng.integers(5)]
    sw, sh = (12, 6) if rng.random() < 0.5 else (6, 12)
    if x > W - 300 and y > H - 140: continue
    big[y:y + sh, x:x + sw] = c

# title
from endcard import _trim
ti = _trim(O.winter_title(['ПРОПУСК', 'ЕСТЬ?!'], 112, width=1100))
O.overlay(big, ti, 40, 30, 1.0)
tag = MV.badge('ВАЛЕРА И КОТ • НОВОГОДНИЙ ФИЛЬМ', 28)
O.overlay(big, tag, 60, 40 + ti.shape[0] + 6, 1.0)
fx.vignette(big, 0.25)
im = Image.fromarray(big)
im.save(MV.HERE / 'cover.png')
im.resize((320, 180), Image.LANCZOS).save(MV.HERE / 'cover_small.png')
q = 92
while True:
    im.save(MV.HERE / 'cover.jpg', quality=q)
    if (MV.HERE / 'cover.jpg').stat().st_size <= 2_000_000 or q < 60: break
    q -= 4
print(MV.HERE / 'cover.jpg', (MV.HERE / 'cover.jpg').stat().st_size)
