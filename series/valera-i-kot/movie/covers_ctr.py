"""CTR covers v3 for «ПРОПУСКНОЙ РЕЖИМ» (14.10.2026): the busy scene cover got 0.8 % CTR (2.2k impressions) — in the mobile feed
(~160 px wide) its ten small details turn into mush. Three simple variants for YouTube Test & Compare, each = ONE big readable subject +
<= 2 huge words + hard contrast on a flat bright background, checked at feed size (feed_preview.png).
  A «НЕ ПРОЙДЁШЬ!»   granny Zina, huge furious face + a palm «stop» right into the lens (conflict + the viewer is the one stopped)
  B «БАБКИ VS МУЖИКИ» split: Zina (yellow) vs unshaven Snegurochka-Kolyan (blue), a huge VS — a fight you want to see
  C «СНЕГУРОЧКА?!»     the unshaven Snegurochka giant & shocked, tiny Zina with binoculars spotting him — absurd curiosity gap
  python3 covers_ctr.py -> cover_A/B/C.jpg (+png), cover.jpg/png = A, cover_small.png, feed_preview.png"""
import math
import movie as MV
from movie import *
from endcard import _trim

t = 0.4
W_, H_ = 1920, 1080
DUMMY = BENCH
yy, xx = np.mgrid[0:H_, 0:W_]


def flat_bg(c1, c2, cx, cy, rays=16, k=0.55):
    ang = np.arctan2(yy - cy, xx - cx); r = np.hypot(yy - cy, xx - cx)
    ray = (np.floor((ang + math.pi) / (2 * math.pi) * rays) % 2).astype(bool)
    bg = np.where(ray[..., None], np.array(c1), np.array(c2)).astype(float)
    glow = np.clip(1 - r / 1100, 0, 1)[..., None]
    bg = bg * (k + (1 - k) * glow) + np.array([255, 250, 220]) * (glow ** 4) * 0.6
    px = 12
    bg = np.repeat(np.repeat(bg[::px, ::px], px, 0), px, 1)[:H_, :W_]
    return np.clip(bg, 0, 255).astype(np.uint8)


def sprite(draw):
    """render heroes on two flat backgrounds -> exact RGB + mask (logical canvas 640x360 x3)"""
    v = view_at(DUMMY, 640, 360, 1.0, SX, SY)
    out = []
    for col in ((0, 0, 0), (255, 0, 255)):
        big = np.zeros((H_, W_, 3), np.uint8); big[:] = col
        CH, _ = MV.begin(); draw(CH); CH.comp(big, Light(amb=(1.05, 1.02, 1.0), keys=[], rim=(-1, -0.5, (255, 240, 220), 0.25)))
        out.append(big)
    m = np.all(out[0] == out[1], axis=2)
    return out[0], m


def stamp(big, rgb, m, ow=16, od=28, col_w=(255, 255, 255), col_d=(26, 12, 8)):
    P_ = 40
    mp = np.pad(m, P_)
    w = O._dilate(mp, ow)[P_:-P_, P_:-P_] & ~m
    d = O._dilate(mp, od)[P_:-P_, P_:-P_] & ~m & ~w
    big[d] = col_d; big[w] = col_w; big[m] = rgb[m]


def title(lines, size, width=2400, outline=(18, 24, 52), shadow=(8, 10, 26)):
    return _trim(O.winter_title(lines, size, width=width, outline=outline, shadow=shadow))


def zina_head(CH, hx, hy, unit, mouth=0.9, look=0.0, flip=True, angry=True, hand=None, prop=None):
    vh = MV.hview(DUMMY, 1000 - 0.7 * unit * (-1 if flip else 1), 1000 - 11.8 * unit, 1.0, hx, hy)
    cam = vh.cam(1000, 1000, unit, flip=flip)
    F.babushka(CH, cam, t, 'zina', 'sit', mouth, 'normal', look=look, hand_n=hand, prop_n=prop)
    if angry:                                                                         # furious brows over the big glasses
        L = Layer(cam)
        for x0, x1, h0, h1 in ((0.45, 1.65, 13.15, 12.65), (1.75, 2.95, 12.6, 13.2)):
            F.cap(L, F.H(x0, h0), F.H(x1, h1), 0.26, 0.26, (60, 40, 30))
        F.outline(L); CH.add(L)


def palm(CH, cx, cy, s=1.0):
    """a big 'stop' palm towards the viewer (logical px)"""
    v = view_at(DUMMY, 640, 360, 1.0, SX, SY)
    L = Layer(v.wcam())
    wx, wy = v.X0 + cx, v.Y0 + cy
    skin, hi, sh = (236, 196, 172), (250, 216, 196), (204, 160, 138)
    F.ell(L, (wx, wy), 40 * s, 46 * s, skin, 0, hi, sh)
    for k, (dx, ln) in enumerate(((-30, 46), (-10, 58), (10, 60), (30, 52))):
        F.cap(L, (wx + dx * s, wy - 26 * s), (wx + dx * s * 1.1, wy - (26 + ln) * s), 10 * s, 9 * s, skin, hi, sh)
    F.cap(L, (wx + 38 * s, wy + 4 * s), (wx + 70 * s, wy - 26 * s), 11 * s, 9 * s, skin, hi, sh)        # thumb
    F.cap(L, (wx - 8 * s, wy + 44 * s), (wx - 14 * s, wy + 120 * s), 30 * s, 28 * s, (74, 58, 70))      # sleeve
    F.outline(L); CH.add(L)


def kolyan_head(CH, hx, hy, unit, expr='shock', mouth=0.9, flip=False):
    vh = MV.hview(DUMMY, 1000 + 1.6 * unit * (-1 if flip else 1), 1000 - 23.4 * unit, 1.0, hx, hy)
    M.kolyan(CH, vh.cam(1000, 1000, unit, flip=flip), M.STAND, t, mouth, expr, costume='snegurochka', look=0.6 * (-1 if flip else 1))


def save(name, big):
    im = Image.fromarray(big)
    im.save(MV.HERE / f'cover_{name}.png')
    q = 92
    while True:
        im.save(MV.HERE / f'cover_{name}.jpg', quality=q)
        if (MV.HERE / f'cover_{name}.jpg').stat().st_size <= 2_000_000 or q < 60: break
        q -= 4
    return im


# ---------------------------------------------------------------- A: «НЕ ПРОЙДЁШЬ!»
def cover_a():
    big = flat_bg((255, 214, 40), (255, 168, 30), 640, 560)
    for k in range(-2, 12):                                                           # red-white barrier stripes along the bottom
        x0 = k * 200
        poly = [(x0, 1080), (x0 + 100, 1080), (x0 + 220, 900), (x0 + 120, 900)]
        im = Image.fromarray(big); ImageDraw.Draw(im).polygon(poly, fill=(220, 30, 36) if k % 2 == 0 else (255, 255, 255)); big = np.array(im)
    big[880:900] = (30, 14, 10)
    rgb, m = sprite(lambda CH: (zina_head(CH, 200, 196, 32.0, mouth=1.0, look=1.0), palm(CH, 420, 230, 1.15)))
    stamp(big, rgb, m)
    ti = title(['НЕ', 'ПРОЙДЁШЬ!'], 132)
    O.overlay(big, ti, 1920 - ti.shape[1] - 30, 40, 1.0)
    return save('A', big)


# ---------------------------------------------------------------- B: «БАБКИ VS МУЖИКИ»
def cover_b():
    left = flat_bg((255, 210, 40), (255, 150, 30), 480, 540)
    right = flat_bg((70, 170, 255), (30, 110, 230), 1440, 540)
    big = left.copy()
    split = (xx > 960 + (yy - 540) * 0.25)
    big[split] = right[split]
    im = Image.fromarray(big); d = ImageDraw.Draw(im)
    d.line([(960 - 135 - 10, 0), (960 + 135 - 10, 1080)], fill=(255, 255, 255), width=26); big = np.array(im)
    rgb, m = sprite(lambda CH: (zina_head(CH, 165, 200, 30.0, mouth=1.0, look=1.0),
                                kolyan_head(CH, 470, 205, 14.0, 'shock', 0.9, flip=True)))
    stamp(big, rgb, m)
    vs = title(['VS'], 220, outline=(120, 10, 10), shadow=(40, 0, 0))
    O.overlay(big, vs, 960 - vs.shape[1] // 2, 560 - vs.shape[0] // 2, 1.0)
    t1 = title(['БАБКИ'], 120); t2 = title(['МУЖИКИ'], 120)
    O.overlay(big, t1, 40, 30, 1.0); O.overlay(big, t2, 1920 - t2.shape[1] - 40, 30, 1.0)
    return save('B', big)


# ---------------------------------------------------------------- C: «СНЕГУРОЧКА?!»
def cover_c():
    big = flat_bg((90, 190, 255), (40, 130, 240), 620, 560)
    rng = np.random.default_rng(3)
    for _ in range(140):
        x = int(rng.uniform(0, 1900)); y = int(rng.uniform(0, 1060)); s_ = int(rng.choice([8, 12, 16]))
        big[y:y + s_, x:x + s_] = (255, 255, 255)
    rgb, m = sprite(lambda CH: (kolyan_head(CH, 230, 210, 17.0, 'shock', 1.0),
                                zina_head(CH, 545, 270, 12.0, mouth=0.0, look=-1.0, flip=True, angry=False,
                                          hand=F.H(2.8, 12.0), prop=lambda L, h: MV.binoculars(L, (h[0] - 0.6, h[1] - 0.2)))))
    stamp(big, rgb, m)
    ti = title(['СНЕГУРОЧКА?!'], 120)
    O.overlay(big, ti, 1920 - ti.shape[1] - 30, 30, 1.0)
    return save('C', big)


A, B_, C = cover_a(), cover_b(), cover_c()
A.save(MV.HERE / 'cover.png'); A.save(MV.HERE / 'cover.jpg', quality=90)
A.resize((320, 180), Image.LANCZOS).save(MV.HERE / 'cover_small.png')
# feed preview: how they look in the mobile feed (168x94) and the sidebar (320x180) on YouTube dark theme
fp = Image.new('RGB', (1060, 520), (15, 15, 15)); d = ImageDraw.Draw(fp)
for i, (nm, im) in enumerate((('A', A), ('B', B_), ('C', C))):
    fp.paste(im.resize((320, 180), Image.LANCZOS), (20 + i * 345, 20)); d.text((20 + i * 345, 205), f'{nm} 320x180', fill=(200, 200, 200))
    fp.paste(im.resize((168, 94), Image.LANCZOS), (20 + i * 345, 240)); d.text((20 + i * 345, 340), f'{nm} 168x94 (лента)', fill=(200, 200, 200))
    fp.paste(im.resize((120, 68), Image.LANCZOS), (20 + i * 345, 370)); d.text((20 + i * 345, 445), f'{nm} 120x68', fill=(200, 200, 200))
fp.save(MV.HERE / 'feed_preview.png')
print('ok')
