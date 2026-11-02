"""E04 «Шапку надень!» — the mother-in-law dresses Tolik (41) in a pompom hat, scarf and mittens on an elastic («Сорок один, а голова
одна»). Behind the garages he takes it all off: «Наконец-то свобода!» — TWIST (the network sees everything): the minibus pulls up, the
driver is Lyusya, Raisa's sister: «Толя, шапку надень. Мне Рая звонила.» A minibus of grannies: «Надень шапку, сынок!» SMS: «ВИЖУ.
МОЛОДЕЦ.» Button: Pusya in the same jumpsuit with a pompom: «Я тоже был против. Не помогло.»
  python3 ep04.py test 1 5 20 | frames t… | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import paths as P
import stage as ST
from stage import view_at, Light
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as B
from props import decals as D
from props import rusigns as R
from props import teshcast as T
from props import teshkit as K
from props import teshshots as SH
from props.teshshots import mouth, u2w, face
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=dict(K.COL, lyusya=(200, 140, 255), babki=(240, 240, 250)), slug=TL.SLUG,
              promo='ru', endcard=dict(style='teshcha', lang='ru', promise='ЗАВТРА: ПЯТЬДЕСЯТ ГОЛОСОВЫХ'))
SH.init(EPI, day=101)
HALL = SH.world('hallway')
YARD = SH.world('yard')
MINI = SH.world('minibus')
CUTS, NAMES = TL.CUTS, TL.NAMES
F0 = TL.T0
TOL = (700.0, 692.0, 15.0)        # Tolik in the hallway (floor point, unit), facing left
RAI = (560.0, 700.0, 15.6)        # Raisa facing right
SCARF = ((40, 120, 200), (90, 170, 236), (24, 80, 150))
MITT = ((214, 40, 52), (240, 90, 96), (150, 24, 36))


def _p(lines, w, h, bg=(250, 248, 240), fg=(34, 28, 30), border=(120, 110, 100), tilt=0, stripe=None, weights=None):
    kw = dict(bg=bg, colors=[fg] * len(lines), border=border, pad=1.0, tilt=tilt)
    if stripe: kw['stripe'] = stripe
    if weights: kw['weights'] = weights
    return R.plate(w, h, lines, **kw)


RED = (184, 30, 40)
YEL = (255, 244, 170)
D.attach(HALL, [
    (_p(['ДЕНЬ', '101'], 30, 38, fg=RED, stripe=((200, 40, 40), 0.3), weights=[0.55, 1]), 205, 160),
    (_p(['ШАПКУ', 'НАДЕЛ?'], 52, 28, bg=YEL, fg=RED, border=(150, 130, 70), tilt=-4), 1094, 300),
    (_p(['-2°'], 24, 16, bg=(236, 240, 250), fg=(40, 60, 150)), 980, 250),
    (_p(['ТАПКИ ТОЛИКА'], 58, 12, bg=(236, 206, 120), border=(120, 84, 30)), 790, 508),
    (_p(['ВАРЕЖКИ НЕ ТЕРЯТЬ!'], 66, 14, bg=YEL, fg=RED, border=(150, 130, 70), tilt=3), 205, 300),
])
D.attach(YARD, [
    (_p(['ГАРАЖ 13'], 40, 14, bg=(236, 236, 230)), 110, 430),
    (_p(['НЕ ПАРКОВАТЬСЯ!'], 64, 16, bg=(250, 250, 250), fg=RED, border=RED), 270, 440),
    (_p(['КУПЛЮ', 'ГАРАЖ'], 36, 22, bg=YEL, tilt=-5), 430, 470),
    (_p(['ОСТАНОВКА «ДОМ 33»'], 80, 14, bg=(40, 90, 170), fg=(255, 255, 255), border=(20, 40, 90)), 820, 392),
    (_p(['ВЯЖУ ШАПКИ.', 'НЕДОРОГО. РАЯ'], 52, 24, bg=(250, 250, 240), fg=(40, 60, 150), tilt=3), 1040, 420),
])
D.attach(MINI, [
    (_p(['ПРОЕЗД 40 Р.'], 58, 16, bg=YEL, fg=RED, border=(150, 130, 70)), 452, 160),
    (_p(['ОСТАНОВКИ ПО ТРЕБОВАНИЮ'], 78, 14), 598, 166),
    (_p(['ШАПКУ НАДЕНЬ!'], 56, 16, bg=YEL, fg=RED, border=(150, 130, 70), tilt=-6), 236, 418),
    (_p(['ДЕНЬГИ ПЕРЕДАЁМ'], 62, 14, bg=(236, 206, 120), border=(120, 84, 30)), 140, 646),
])


def light_hall(v):
    lx, ly = v.opt(610.0, 80.0)
    return Light(amb=(1.02, 0.96, 0.88), keys=[(lx, ly, 1200, (255, 210, 140), 0.55)], rim=(-1, -0.4, (255, 220, 170), 0.3), grad=(1.04, 0.9))


def light_yard(v):
    lx, ly = v.opt(790.0, 170.0)
    return Light(amb=(0.96, 0.99, 1.06), keys=[(lx, ly, 900, (255, 214, 150), 0.25)], rim=(1, -0.4, (220, 236, 255), 0.35), grad=(1.03, 0.94))


def light_mini(v):
    lx, ly = v.opt(650.0, 110.0)
    return Light(amb=(1.0, 0.95, 0.88), keys=[(lx, ly, 1100, (255, 214, 150), 0.5)], rim=(1, -0.4, (210, 226, 255), 0.35), grad=(1.04, 0.9))


def hall(v, t, draw=None, after=None):
    return SH.generic(HALL, v, t, draw, light=light_hall(v), motes=(450, 60, 800, 300), after=after)


def yard(v, t, draw=None, after=None):
    return SH.generic(YARD, v, t, draw, light=light_yard(v), snow=(0, 0, 1280, 720), after=after, vign=0.22)


def mini(v, t, draw=None, after=None):
    return SH.generic(MINI, v, t, draw, light=light_mini(v), motes=(420, 100, 800, 330), after=after)


# ---------------------------------------------------------------- winter gear (Tolik's cam units)
def gear(CH, cam, r, scarf=True, mitt=True):
    L = Layer(cam)
    if mitt:                                                                          # mittens on an elastic through the sleeves
        for h in (r['hand_n'], r['hand_f']):
            F.cap(L, h, F.H(0.3, 21.6), 0.07, 0.07, (250, 250, 250))
    if scarf:
        F.ell(L, F.H(0.3, 22.8), 2.1, 0.9, SCARF[0], 0, SCARF[1], SCARF[2])
        for k in range(3): F.cap(L, F.H(-1.4 + k * 1.3, 22.4), F.H(-1.2 + k * 1.3, 23.3), 0.14, 0.14, (240, 240, 250))
        F.cap(L, F.H(1.5, 22.4), F.H(2.1, 18.4), 0.6, 0.65, SCARF[0], SCARF[1], SCARF[2])
        F.cap(L, F.H(1.6, 20.6), F.H(2.0, 20.6), 0.14, 0.14, (240, 240, 250))
        for k in range(4): F.cap(L, F.H(1.6 + k * 0.25, 18.2), F.H(1.6 + k * 0.3, 17.6), 0.08, 0.08, SCARF[2])
    if mitt:
        for h in (r['hand_n'], r['hand_f']):
            F.ell(L, (h[0], h[1] - 0.2), 1.05, 1.45, MITT[0], 0, MITT[1], MITT[2])
            F.ell(L, (h[0] + 0.95, h[1] - 0.1), 0.42, 0.62, MITT[0], 0, MITT[1], MITT[2])
            F.cap(L, (h[0] - 0.95, h[1] + 1.0), (h[0] + 0.95, h[1] + 1.0), 0.32, 0.32, (250, 250, 250))
            F.dot(L, (h[0] - 0.1, h[1] - 0.4), (250, 250, 250), 0.3)
    F.outline(L, T.OL); CH.add(L)


def hat_in_hand(L, h):
    F.ell(L, (h[0] + 0.6, h[1] - 0.9), 1.4, 0.95, (196, 40, 52), 0, (232, 80, 84), (140, 26, 36))
    F.ell(L, (h[0] + 0.5, h[1] - 1.9), 0.6, 0.55, (246, 240, 230))


def tolik(CH, v, t, pos=TOL, flip=True, pose='stand', expr='normal', hat='knit', scarf=True, mitt=True, m=None, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un, flip=flip)
    pp = T.TPOSE[pose] if isinstance(pose, str) else pose
    r = T.tolik(CH, cam, pp, t=t, mouth_=mouth('tolik', t) if m is None else m, expr=expr, hat=hat, **kw)
    gear(CH, cam, r, scarf, mitt)
    face(v, cam, r)
    return cam, r


def raisa(CH, v, t, pos=RAI, pose='stand', expr='sweet', flip=False, pal=None, who='raisa', **kw):
    x, y, un = pos
    cam = v.cam(x, y, un, flip=flip)
    pp = T.RPOSE[pose] if isinstance(pose, str) else pose
    r = T.raisa(CH, cam, pp, t=t, mouth_=mouth(who, t), expr=expr, pal=pal, **kw)
    face(v, cam, r, 3.6)
    return cam, r


def pusya_suit(CH, v, t, x, y, un, m=0.0, expr='deadpan'):
    cam = v.cam(x, y, un)
    r = T.pusya(CH, cam, t=t, mouth_=m, expr=expr, shiver=0.6)
    hc = r['head']
    L = Layer(cam)                                                                    # the same pompom hat as Tolik's
    F.ell(L, (hc[0], hc[1] - 1.05), 1.55, 0.95, (196, 40, 52), 0, (232, 80, 84), (140, 26, 36))
    F.cap(L, (hc[0] - 1.5, hc[1] - 0.55), (hc[0] + 1.5, hc[1] - 0.55), 0.32, 0.32, (140, 26, 36))
    F.ell(L, (hc[0], hc[1] - 2.15), 0.6, 0.55, (246, 240, 230), 0, (255, 255, 255), (206, 200, 196))
    F.outline(L, T.OL); CH.add(L)
    face(v, cam, r, 2.0)
    return cam, r


# ---------------------------------------------------------------- shots: hallway
def r_hook(t, u):
    """«Толечка, на улице минус два. Шапку надень!» — tight two-shot: Raisa yanks a pompom hat onto Tolik, scarf and mittens on"""
    z = 1.22 - 0.06 * sm(u / 3.0)
    v = view_at(HALL, 635, 335, z, 180, 300)
    tug = 0.4 * math.sin(t * 9) * (1 - sm(u / 2.0))

    def draw(CH, v_):
        tolik(CH, v_, t, expr='whine', pose='stand', m=mouth('tolik', t))
        raisa(CH, v_, t, pose=dict(T.RPOSE['offer'], n=(7.4, 20.8 + tug), f=(6.2, 20.0 - tug), bf=1), expr='sweet')
    return hall(v, t, draw)


def r_tolik_mad(t, u):
    """«Раиса Захаровна, мне сорок один год! Я сам решу!» — close on Tolik, fists in mittens, scarf to the ears"""
    x, y, un = TOL
    k = 1.3
    v = view_at(HALL, x - 20, y - 27 * un * k + 60, 1.42, 180, 300)

    def draw(CH, v_):
        tolik(CH, v_, t, pos=(x, y + 50, un * k), pose='fists', expr='angry')
    return hall(v, t, draw)


def r_meningit(t, u):
    """«Сорок один, а голова одна. Без шапки — менингит!» — close on Raisa, finger up, stern"""
    x, y, un = RAI
    k = 1.25
    v = view_at(HALL, x + 50, y - 21 * un * k + 40, 1.42, 180, 300)

    def draw(CH, v_):
        raisa(CH, v_, t, pos=(x, y + 50, un * k), pose=dict(T.RPOSE['stand'], n=(6.4, 18.2)), expr='stern', look=0.4)
    return hall(v, t, draw)


def r_muzhik(t, u):
    """«Я в этом доме мужик!» — Tolik puffs up, fist on chest, pompom bobbing"""
    x, y, un = TOL
    k = 1.3
    v = view_at(HALL, x - 20, y - 27 * un * k + 60, 1.42 + 0.03 * sm(u / 1.5), 180, 300)

    def draw(CH, v_):
        tolik(CH, v_, t, pos=(x, y + 50, un * k), pose='proud', expr='proud')
    return hall(v, t, draw)


def r_hatdown(t, u):
    """«Мужик — в шапке!» — she pulls the hat down over his eyes; at their feet Pusya in the same pompom jumpsuit"""
    v = view_at(HALL, 640, 420, 1.12, 180, 330)
    pull = sm(u / 0.25)

    def draw(CH, v_):
        tolik(CH, v_, t, pose='shock' if pull > 0.5 else 'stand', expr='shock', hat='down' if pull > 0.5 else 'knit', m=0.5)
        raisa(CH, v_, t, pose=dict(T.RPOSE['offer'], n=(7.4, 21.6 - 1.4 * pull), f=(6.2, 20.6 - 1.4 * pull), bf=1), expr='smug')
        pusya_suit(CH, v_, t, 640, 704, 9.0)
    big = hall(v, t, draw)
    if 0.2 < u < 0.45: B.shake(big, t, 6, 40)
    return big


# ---------------------------------------------------------------- shots: the yard
def r_yard(t, u):
    """«Наконец-то свобода! Тут она меня не видит.» — behind the garages, Tolik pulls off the hat and stuffs the scarf away, happy"""
    v = view_at(YARD, 410 + 30 * sm(u / 4), 425, 1.2, 180, 330)
    off = sm((u - 0.6) / 0.8)

    def draw(CH, v_):
        tolik(CH, v_, t, pos=(400, 650, 14.0), flip=False, pose=dict(T.TPOSE['proud'], n=(4.4, 21.0)) if off > 0.5 else 'stand',
              expr='smug' if off > 0.5 else 'whine', hat=None if off > 0.5 else 'knit', scarf=off < 0.9, mitt=off < 0.9,
              prop_n=hat_in_hand if off > 0.5 else None)
    return yard(v, t, draw)


def gazelle(L, x, y, s=1.0):
    """a yellow route minibus facing left, wheels on y; Lyusya's purple perm visible through the windshield"""
    def p(dx, dy): return (x + dx * s, y + dy * s)
    yel, yel_sh, yel_hi = (236, 196, 40), (190, 150, 24), (252, 224, 110)
    F.poly(L, [p(-218, -48), p(196, -48), p(196, -222), p(-150, -222), p(-180, -190), p(-212, -120), p(-220, -70)], yel)
    F.poly(L, [p(-150, -222), p(196, -222), p(196, -232), p(-140, -232)], yel_hi)
    F.poly(L, [p(-206, -120), p(-174, -192), p(-128, -192), p(-128, -120)], (130, 170, 196))           # windshield
    F.ell(L, p(-160, -150), 20 * s, 20 * s, (130, 70, 160), 0, (170, 110, 200), (90, 40, 116))       # Lyusya's perm
    F.ell(L, p(-170, -132), 12 * s, 14 * s, (240, 192, 162))
    for k in range(5):                                                                                  # side windows
        x0 = -112 + k * 60
        F.poly(L, [p(x0, -192), p(x0 + 50, -192), p(x0 + 50, -130), p(x0, -130)], (96, 120, 144))
        F.cap(L, p(x0 + 8, -186), p(x0 + 20, -140), 1.5, 1.5, (170, 196, 214))
    F.poly(L, [p(-212, -84), p(196, -84), p(196, -72), p(-214, -72)], (196, 40, 52))                   # red stripe
    F.cap(L, p(-104, -126), p(-104, -52), 1.2, 1.2, yel_sh); F.cap(L, p(-44, -126), p(-44, -52), 1.2, 1.2, yel_sh)   # sliding door
    F.ell(L, p(-214, -96), 9 * s, 7 * s, (255, 240, 170))                                             # headlight
    F.poly(L, [p(-224, -56), p(-150, -56), p(-150, -44), p(-226, -44)], (80, 80, 86))                  # bumper
    for wx in (-140, 128):
        F.ell(L, p(wx, -18), 30 * s, 30 * s, (40, 40, 46), 0, (70, 70, 80), (24, 24, 30))
        F.ell(L, p(wx, -18), 13 * s, 13 * s, (170, 170, 176))
    F.outline(L, T.OL)


ROUTE = _p(['33', 'ДОМ — РЫНОК'], 64, 30, bg=(250, 250, 250), fg=RED, border=(40, 40, 46), weights=[1, 0.5])


def r_bus(t, u):
    """the minibus screeches in from the right and stops right next to him"""
    v = view_at(YARD, 600, 380, 0.95, 180, 330)
    bx = 670 + 600 * (1 - sm(u / 0.5))

    def draw(CH, v_):
        tolik(CH, v_, t, pos=(455, 650, 12.0), flip=False, pose='shock', expr='shock', hat=None, scarf=False, mitt=False, m=0.6,
              prop_n=hat_in_hand)
        L = Layer(v_.wcam()); gazelle(L, bx, 700, 0.75); CH.add(L)
    big = yard(v, t, draw)
    D.blit(big, v, ROUTE, bx - 20, 700 - 150)
    fx.speed_lines(big, t, 0.9)
    if 0.45 < u < 0.75: B.shake(big, t, 7, 30)
    return big


# ---------------------------------------------------------------- shots: the minibus
def wheel(L):
    """the fur-covered steering wheel in front of the driver (redrawn over her)"""
    cx, cy, rx, ry = 215.0, 548.0, 112.0, 60.0
    n = 28
    for i in range(n):
        a0, a1 = i / n * 6.283, (i + 1) / n * 6.283
        F.cap(L, (cx + rx * math.cos(a0), cy + ry * math.sin(a0)), (cx + rx * math.cos(a1), cy + ry * math.sin(a1)), 12, 12,
              (214, 190, 150), (236, 214, 176), (170, 146, 110))
    F.cap(L, (cx - 30, cy + 10), (cx + 30, cy + 10), 14, 14, (60, 50, 44))
    F.outline(L, T.OL)


def r_twist(t, u):
    """TWIST: «Толя, шапку надень. Мне Рая звонила.» — the driver is Lyusya, Raisa's sister (purple perm, leather jacket), phone at ear"""
    v = view_at(MINI, 260, 400, 1.42, 170, 300)

    def draw(CH, v_):
        raisa(CH, v_, t, pos=(240, 720, 17.0), pose=dict(T.RPOSE['sit'], n=(6.6, 17.4)), expr='stern', pal=T.LYUSYA, who='lyusya',
              look=0.7, prop_n=lambda L, h: T.phone(L, h, -1.75))
        L = Layer(v_.wcam()); wheel(L); CH.add(L)
    big = mini(v, t, draw)
    if u < 0.3: B.shake(big, t, 9, 40)
    return big


def r_babki(t, u):
    """«Надень шапку, сынок!» — the whole minibus of grannies turns to him and wags fingers"""
    v = view_at(MINI, 900, 440, 1.2 + 0.05 * sm(u / 2), 180, 330)
    wag = 0.8 * math.sin(t * 11)

    def draw(CH, v_):
        raisa(CH, v_, t, pos=(805, 600, 10.0), pose=dict(T.RPOSE['sit'], n=(4.6, 15.6 + wag)), expr='stern', pal=T.GRANNY[1], who='babki',
              flip=True, look=-0.6)
        raisa(CH, v_, t, pos=(935, 650, 12.5), pose=dict(T.RPOSE['sit'], n=(5.0, 16.0 - wag)), expr='stern', pal=T.GRANNY[0], who='babki',
              flip=True, look=-0.6)
        raisa(CH, v_, t, pos=(1045, 740, 15.5), pose=dict(T.RPOSE['sit'], n=(5.2, 16.4 + wag)), expr='sweet', who='babki', flip=True,
              pal=dict(T.GRANNY[1], hair=(230, 230, 236), curl=(236, 236, 240), curl_hi=(255, 255, 255), curl_sh=(180, 180, 190),
                       robe=(170, 60, 70), robe_hi=(200, 90, 100), robe_sh=(120, 40, 50)), look=-0.6)
    return mini(v, t, draw)


def r_inhat(t, u):
    """«Надел, надел... Откуда она всё видит?!» — Tolik in the aisle, hat back on, scarf, looking around paranoid"""
    v = view_at(MINI, 560, 385, 1.26, 180, 300)

    def draw(CH, v_):
        tolik(CH, v_, t, pos=(560, 724, 15.0), flip=False, pose='phone', expr='sad' if u < 1.4 else 'shock', look=math.sin(t * 4) * 0.8,
              prop_n=lambda L, h: T.phone(L, h, -1.75))
    return mini(v, t, draw)


def r_sms(t, u):
    """insert: the phone screen — a message from «ТЁЩА»: «ВИЖУ. МОЛОДЕЦ.»"""
    big = r_inhat(t, 2.0)
    im = Image.fromarray(big).filter(ImageFilter.GaussianBlur(14))
    big = (np.asarray(im).astype(np.float32) * 0.55).astype(np.uint8)
    W_, H_ = 620, 1040
    ph = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(ph)
    d.rounded_rectangle((0, 0, W_ - 1, H_ - 1), 60, fill=(30, 30, 36, 255), outline=(10, 10, 12, 255), width=8)
    d.rounded_rectangle((28, 90, W_ - 28, H_ - 90), 24, fill=(236, 240, 246, 255))
    d.rectangle((28, 90, W_ - 28, 210), fill=(80, 140, 210, 255))
    f1, f2 = O.pfont(46), O.pfont(58)
    d.text((W_ // 2, 150), 'ТЁЩА', font=f1, fill=(255, 255, 255, 255), anchor='mm')
    pop = sm(u / 0.2)
    if pop > 0:
        y0 = 330
        d.rounded_rectangle((60, y0, W_ - 70, y0 + 220), 36, fill=(255, 255, 255, 255), outline=(200, 206, 214, 255), width=4)
        d.text((W_ // 2 - 5, y0 + 70), 'ВИЖУ.', font=f2, fill=(30, 30, 36, 255), anchor='mm')
        d.text((W_ // 2 - 5, y0 + 150), 'МОЛОДЕЦ.', font=f2, fill=(184, 30, 40, 255), anchor='mm')
        d.text((W_ - 90, y0 + 250), '07:41', font=O.pfont(30), fill=(120, 126, 140, 255), anchor='rm')
    a = np.asarray(ph)
    sc = 0.92 + 0.08 * sm(u / 0.15)
    if sc != 1.0:
        a = np.asarray(ph.resize((int(W_ * sc), int(H_ * sc)), Image.NEAREST))
    O.overlay(big, a, (big.shape[1] - a.shape[1]) // 2, 360, 1.0)
    return big


# ---------------------------------------------------------------- button + loop
def r_button(t, u):
    """«Я тоже был против. Не помогло.» — Pusya on the hallway rug in the same pompom hat and knitted suit, deadpan to camera"""
    v = view_at(HALL, 330, 600, 1.42, 180, 330)

    def draw(CH, v_):
        pusya_suit(CH, v_, t, 330, 690, 19.0, m=mouth('pusya', t, 2.0))
    return hall(v, t, draw)


def r_loop(t, u):
    big = r_hook(t, u + 0.3)
    fx.speed_lines(big, t, 0.8)
    return big


SHOT = dict(hook=r_hook, tolik_mad=r_tolik_mad, meningit=r_meningit, muzhik=r_muzhik, hatdown=r_hatdown, yard=r_yard, bus=r_bus,
            twist=r_twist, babki=r_babki, inhat=r_inhat, sms=r_sms, button=r_button, loop=r_loop)


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


SHOW = K.Show(EPI, 1, 4, ['ШАПКУ', 'НАДЕНЬ!'], hook_t=(0.06, 2.8), hook_y=200,
              stickers=[(O.sticker('41 ГОД!', fg=(90, 225, 215), size=80), F0['tolik_mad'] + 0.4, F0['meningit'], 540, 560),
                        (O.sticker('МИНУС 2!', fg=(150, 200, 255), size=80), F0['meningit'] + 0.3, F0['muzhik'], 560, 520),
                        (O.sticker('ЛЮСЯ?!', fg=(200, 140, 255), size=110), TL.TWIST + 0.3, F0['babki'], 620, 520)],
              flashes=[TL.TWIST + 0.02], mosaics=[F0['yard'], F0['sms']],
              cap_y={'hook': 1500, 'button': 880, 'sms': 1600, 'babki': 1350}, cap_default=1380)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
