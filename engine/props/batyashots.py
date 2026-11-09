"""Shared scene helpers for «Батя сам» episodes (E02+), extracted from E01: worlds (bedroom, kitchen, yard) with their local signs,
lights, the blanket mound with the tiger plaid, Batya / Ira in bed, Ira standing, the thermometer LCD, smoke, Tyoma's selfie.
Call init(EPI) once in the episode script. Coordinates are native px of series/batya/bg/*.png."""
import math
import numpy as np
import stage as ST
from stage import view_at, Light
from scene import Layer, sm, lerp
import fx
from props import folk as F
from props import bytfx as BF
from props import decals as D
from props import rusigns as R
from props import batyacast as B
from props import batyakit as K

TALK = [None]
W = K.build()
BED, KIT = W['bedroom'], W['kitchen']
OL = B.OL
EXTRA = {}


def init(epi):
    TALK[0] = epi.talk


def extra_world(name):
    """extra xAI worlds (yard, …) quantized to the series palette, cached"""
    if name not in EXTRA:
        from PIL import Image
        EXTRA[name] = K.q(Image.open(K.BG / f'{name}.png').convert('RGB'))
    return EXTRA[name]

# ---------------------------------------------------------------- world geometry (native px of bg/*.png)
BED_TOP = 432.0            # mattress surface in front of the pillows
UN = 16.0                  # hero unit (world px) at the bed's depth: 1 m ≈ 255 px
BX, BX_L = 540.0, 395.0    # sitting points on the right / left pillow
FLOOR = 640.0              # standing floor line in front of the bed and nightstand

P = lambda w, h, lines, bg, colors, border, **kw: R.plate(w, h, lines, bg=bg, colors=colors, border=border, **kw)
D.attach(BED, [
    (P(26, 12, ['ЧИХАЛИН'], (240, 240, 236), [(40, 90, 170)], (120, 120, 130), pad=0.6), 669, 380),
    (P(30, 12, ['НАСМОРКИН'], (250, 220, 90), [(150, 30, 40)], (140, 110, 40), pad=0.6, tilt=-4), 672, 367),
    (P(24, 11, ['АСПИРИН'], (255, 255, 255), [(40, 120, 70)], (120, 120, 120), pad=0.6, tilt=5), 678, 355),
    (P(32, 12, ['ТЕРРА-ПЛЮХ'], (90, 60, 140), [(255, 230, 120)], (50, 30, 80), pad=0.6), 752, 381),
    (P(28, 10, ['ГОРЧИЧНИКИ'], (240, 220, 160), [(120, 60, 20)], (130, 100, 60), pad=0.5, tilt=-3), 756, 370),
    (P(18, 20, ['МАЛИНА', '2025'], (190, 30, 60), [(255, 240, 240), (255, 220, 220)], (90, 10, 30), pad=0.6, weights=[1, 0.8]), 778, 350),
    (P(88, 16, ['АПТЕКА «У БАТИ»'], (250, 248, 240), [(184, 30, 40)], (120, 30, 30), pad=0.8), 688, 414),
    (P(54, 64, ['ГРАМОТА', 'ЛУЧШИЙ', 'СЛЕСАРЬ', 'ЦЕХА № 3', '1994'], (250, 240, 214), [(150, 30, 30), (40, 40, 60), (40, 40, 60),
       (40, 40, 60), (150, 30, 30)], None, pad=1.0, weights=[1, 0.75, 0.75, 0.7, 0.8]), 688, 138),
    (P(54, 64, ['ДИПЛОМ', 'РЫБАК', 'ГОДА', '2019'], (236, 244, 250), [(40, 70, 150), (30, 30, 40), (30, 30, 40), (40, 70, 150)], None,
       pad=1.0, weights=[1, 0.85, 0.85, 0.8]), 775, 183),
    (P(46, 38, ['ТИХО!', 'БАТЯ', 'БОЛЕЕТ'], (255, 252, 236), [(184, 30, 40), (34, 28, 30), (34, 28, 30)], (170, 160, 140), pad=1.0,
       tilt=-3, hand=True), 1168, 228),
    (P(48, 30, ['СЕРВИЗ —', 'НА СВАДЬБУ', 'ТЁМЫ'], (250, 246, 230), [(34, 28, 30), (184, 30, 40), (184, 30, 40)], (150, 140, 110),
       pad=0.9, tilt=2, weights=[0.8, 0.8, 1]), 126, 328),
    (P(40, 52, ['НОЯБРЬ', '2026'], (250, 248, 240), [(184, 30, 40), (34, 28, 30)], (120, 110, 100), pad=1.0, weights=[0.8, 1],
       stripe=((200, 40, 40), 0.28)), 258, 110),
])
D.attach(KIT, [
    (P(62, 24, ['ИРА —', 'НЕ ТРОГАТЬ!'], (255, 244, 170), [(34, 28, 30), (184, 30, 40)], (150, 130, 70), pad=0.9, tilt=2), 70, 418),
    (P(40, 26, ['БОРЩ', 'НА ЗАВТРА'], (255, 236, 120), [(34, 28, 30), (40, 60, 150)], None, pad=0.9, tilt=-4, hand=True), 150, 236),
    (P(64, 26, ['ДЕЛОВ', 'НА 5 МИНУТ!'], (250, 250, 240), [(34, 28, 30), (184, 30, 40)], (150, 140, 120), pad=0.9, tilt=-2, hand=True), 368, 122),
    (P(70, 80, ['НОЯБРЬ', '2026'], (250, 248, 240), [(184, 30, 40), (34, 28, 30)], (120, 110, 100), pad=1.2, weights=[0.8, 1],
       stripe=((200, 40, 40), 0.28)), 1164, 258),
    (P(26, 11, ['ГРЕЧКА'], (240, 230, 200), [(90, 50, 20)], (120, 100, 70), pad=0.5), 176, 82),
    (P(22, 11, ['СОЛЬ'], (240, 240, 240), [(40, 60, 150)], (120, 120, 130), pad=0.5), 266, 82),
    (P(24, 11, ['САХАР'], (240, 240, 240), [(184, 30, 40)], (120, 120, 130), pad=0.5), 503, 110),
])
LCD = {}


def lcd_img(s):
    if s not in LCD: LCD[s] = P(44, 16, [s], (176, 198, 150), [(20, 34, 20)], (90, 104, 80), pad=0.5)
    return LCD[s]

# ---------------------------------------------------------------- helpers
def mouth(who, t, k=1.7):
    return min(1.0, TALK[0](who, t) * k)


def u2w(v, cam, pt):
    x, y = cam.p(*pt)
    k = ST.PX[0]
    return v.X0 + x * k / v.Z, v.Y0 + (y * k - v.oy) / v.Z


def face(v, cam, r, r_units=3.0):
    K.logface(v, cam, r['head'], r_units)


def light_bed(v):
    lx, ly = v.opt(732.0, 300.0); wx, wy = v.opt(1010.0, 200.0)
    return Light(amb=(1.0, 0.94, 0.86), keys=[(lx, ly, 1300, (255, 190, 110), 0.75)], rim=(1, -0.4, (170, 196, 255), 0.4), grad=(1.03, 0.88))


def light_kit(v):
    lx, ly = v.opt(645.0, 30.0)
    return Light(amb=(1.02, 0.96, 0.88), keys=[(lx, ly, 1500, (255, 210, 140), 0.65)], rim=(-1, -0.4, (170, 196, 255), 0.3), grad=(1.04, 0.9))


def smoke(big, v, t, x, y, t0=-99.0, n=9, rise=260, size=70, a=0.55, col=(120, 118, 122)):
    if t < t0: return
    for i in range(n):
        a_, b, c, d, e = BF.SEED[440 + i % 150]
        life = 1.6 + 0.9 * c
        u = ((t - t0 + d * life) % life) / life
        wx = x + (a_ - 0.5) * 50 + 60 * math.sin(t * 1.1 + i) * u
        ox, oy = v.opt(wx, y - rise * u)
        BF.puff(big, ox, oy, size * v.Z * 3 * (0.5 + 1.1 * u), a * (1 - u) * min(1.0, (t - t0) / 0.4), col)


def world(img, v, t, draw=None, light=None, snow=None, motes=None, after=None, vign=0.28):
    CH, FX = K.begin()
    big = v.bg()
    if draw: draw(CH, v)
    CH.comp(big, light)
    if snow: BF.falling_snow(FX, v, t, *snow, n=50, speed=36)
    if motes: fx.motes(FX, v, t, *motes, n=18, col=(255, 226, 170), seed=5)
    FX.comp(big)
    if after: after(big, v)
    fx.vignette(big, vign)
    return big


def bedroom(v, t, draw=None, after=None):
    return world(BED, v, t, draw, light_bed(v), snow=(925, 60, 1100, 330), motes=(640, 230, 840, 420), after=after)


def kitchen(v, t, draw=None, after=None):
    return world(KIT, v, t, draw, light_kit(v), snow=(760, 90, 1000, 300), motes=(520, 40, 780, 260), after=after)


# ---------------------------------------------------------------- blankets: red plaid, green wool, the tiger plaid on top
def tiger_face(L, x, y, s=1.0):
    F.ell(L, (x - 26 * s, y - 24 * s), 10 * s, 9 * s, (236, 150, 50)); F.ell(L, (x + 26 * s, y - 24 * s), 10 * s, 9 * s, (236, 150, 50))
    F.ell(L, (x - 26 * s, y - 24 * s), 5 * s, 4.5 * s, (40, 26, 20)); F.ell(L, (x + 26 * s, y - 24 * s), 5 * s, 4.5 * s, (40, 26, 20))
    F.ell(L, (x, y), 34 * s, 28 * s, (240, 156, 50), 0, (252, 190, 90), (200, 116, 30))
    for k in (-1, 1):
        F.cap(L, (x + k * 30 * s, y - 6 * s), (x + k * 14 * s, y - 2 * s), 2.6 * s, 2.0 * s, (40, 26, 20))
        F.cap(L, (x + k * 32 * s, y + 6 * s), (x + k * 16 * s, y + 6 * s), 2.6 * s, 2.0 * s, (40, 26, 20))
        F.ell(L, (x + k * 12 * s, y - 8 * s), 6 * s, 4.5 * s, (250, 220, 70)); F.dot(L, (x + k * 12 * s, y - 8 * s), (20, 16, 14), 2.4 * s)
    F.cap(L, (x - 6 * s, y - 24 * s), (x + 6 * s, y - 24 * s), 2.4 * s, 2.4 * s, (40, 26, 20))
    F.ell(L, (x, y + 10 * s), 16 * s, 10 * s, (250, 244, 232))
    F.poly(L, [(x - 6 * s, y + 3 * s), (x + 6 * s, y + 3 * s), (x, y + 9 * s)], (60, 30, 30))


def blankets(CH, v, top, x0, x1, t=0.0, tiger=True, fly=0.0):
    """blanket mound over the bed from the line `top` down to the foot of the bed: a turned-down white sheet on top, the tiger plaid,
    red and green blanket edges hanging at the sides; fly 0..1 = the tiger plaid thrown into the air"""
    L = Layer(v.wcam())
    foot = 610.0
    cx = (x0 + x1) / 2
    def edge(xx):                                                                           # soft bumpy top line (belly, knees)
        return top + 10 * math.cos((xx - cx) / (x1 - x0) * 3.1) * -1 + 6 * math.sin((xx - x0) * 0.045)
    if fly <= 0:
        F.poly(L, [(x0 - 26, top + 30), (x0 - 4, top + 26), (x0 - 18, foot + 4), (x0 - 52, foot + 8)], (176, 40, 44))       # red edge, left
        for k in range(3): F.cap(L, (x0 - 34 + k * 9, top + 34), (x0 - 46 + k * 9, foot), 1.8, 1.8, (230, 210, 120))
        F.poly(L, [(x1 - 2, top + 30), (x1 + 22, top + 34), (x1 + 14, foot), (x1 - 10, foot - 4)], (70, 120, 80))           # green edge, right
    if tiger:
        dx, dy, rot = -420 * fly, -520 * fly * (1.2 - fly), 0.6 * fly
        def T(px, py):
            px -= cx; py -= (top + foot) / 2
            c, s_ = math.cos(rot), math.sin(rot)
            return (cx + px * c - py * s_ + dx, (top + foot) / 2 + px * s_ + py * c + dy)
        n = 14
        topl = [T(x0 + (x1 - x0) * i / n, edge(x0 + (x1 - x0) * i / n)) for i in range(n + 1)]
        F.poly(L, topl + [T(x1 + 8, foot), T(x0 - 22, foot)], (236, 146, 44))
        F.poly(L, [T(x0 - 22, foot), T(x1 + 8, foot), T(x1 + 2, foot - 70), T(x0 - 14, foot - 70)], (214, 120, 32))  # shade toward foot
        for k in range(8):                                                                   # tapered wavy tiger stripes in pairs
            xa = x0 + 12 + k * (x1 - x0 - 20) / 8
            ya = edge(xa) + 30 + (k % 2) * 24
            F.cap(L, T(xa, ya), T(xa - 10, ya + 34), 5.0, 1.2, (44, 30, 22))
            F.cap(L, T(xa + 9, ya + 4), T(xa + 2, ya + 28), 3.6, 1.0, (44, 30, 22))
            F.cap(L, T(xa - 4, foot - 70), T(xa - 16, foot - 30), 4.6, 1.2, (44, 30, 22))
        for k in range(3):                                                                   # soft folds
            xa = x0 + (x1 - x0) * (0.25 + 0.25 * k)
            F.cap(L, T(xa, edge(xa) + 50), T(xa - 18, foot - 20), 2.0, 2.6, (206, 112, 30))
        tiger_face(L, *T(cx - 6, edge(cx) + 74), 1.45)
        if fly <= 0:                                                                          # turned-down white sheet
            sh = [(x0 - 6 + (x1 - x0 + 12) * i / n, edge(x0 + (x1 - x0) * i / n) - 4) for i in range(n + 1)]
            F.poly(L, sh + [(p_[0], p_[1] + 20) for p_ in sh[::-1]], (246, 242, 234))
            F.poly(L, [(p_[0], p_[1] + 16) for p_ in sh] + [(p_[0], p_[1] + 22) for p_ in sh[::-1]], (204, 196, 186))
    F.outline(L, OL)
    CH.add(L)


def batya_bed(CH, v, t, expr='dying', pose=None, x=BX, un=UN, sick=1.0, towel=True, cover=0.0, flip=False, **kw):
    """Batya sitting up in bed (no legs) under the blankets; cover 0..1 pulls the blanket up to his nose"""
    cam = v.cam(x, BED_TOP + 9.6 * un, un, flip=flip)
    r = B.batya(CH, cam, pose or B.BPOSE['dying'], t=t, mouth_=mouth('batya', t), expr=expr, legs=False, vest=False, sick=sick,
                towel=towel, **kw)
    top = BED_TOP + 9.6 * un - (13.4 + 8.6 * cover) * un
    blankets(CH, v, top, x - 6.2 * un, x + 6.6 * un, t)
    if cover > 0.5:                                                                         # fists clutching the blanket edge
        L = Layer(v.wcam())
        for dx in (-1.6, 1.8):
            F.ell(L, (x + dx * un, top + 4), 1.1 * un, 0.9 * un, B.BC['skin'], 0, B.BC['skin_hi'], B.BC['skin_sh'])
        F.outline(L, OL); CH.add(L)
    face(v, cam, r, 3.2)
    return cam, r


def ira_bed(CH, v, t, expr='sick', x=BX, un=UN, pose=None, **kw):
    cam = v.cam(x, BED_TOP + 9.6 * un, un, flip=True)
    r = B.ira(CH, cam, pose or B.IPOSE['spoon'], t=t, mouth_=mouth('ira', t), expr=expr, legs=False, scarf=True, sick=1.0, **kw)
    face(v, cam, r, 2.6)
    return cam, r


def thermo_prop(store, size=1.5, ang=-0.25):
    def f(L, h): store['m'] = B.thermometer(L, h, ang=ang, size=size)
    return f


def lcd(big, v, cam, store, text):
    if 'm' not in store: return
    wx, wy = u2w(v, cam, store['m'])
    img = lcd_img(text)
    D.blit(big, v, img, wx - img.shape[1] / 8, wy - img.shape[0] / 8)


def ira_stand(CH, v, t, x, expr='dry', pose=None, coat=True, prop_n=None, un=UN, floor=FLOOR + 6, **kw):
    cam = v.cam(x, floor, un, flip=True)
    r = B.ira(CH, cam, pose or B.IPOSE['tray'], t=t, mouth_=mouth('ira', t), expr=expr, coat=coat, scarf=True, sick=0.8,
              prop_n=prop_n, **kw)
    face(v, cam, r, 2.6)
    return cam, r
