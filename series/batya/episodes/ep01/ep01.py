"""E01 «37,2 — ПОМИРАЮ!» — Batya has 37.2 and is «dying» in bed under three blankets (the tiger plaid on top), dictates a will,
rings a bell for broth. Mum Ira brings a tray in her coat and scarf, sneezes — TWIST (the saviour is the victim): the thermometer
shows 38.9 on HER, and she is going to work. Batya flies out of bed «Не трогай — я сам!», cooks «five minutes» for two hours;
Ira tastes it in bed — «Вкусно, Витя» — and he collapses beside her: «у меня опять тридцать семь и два!» (loop to the hook).
  python3 ep01.py test 1 5 20 | frames t… | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import stage as ST
from stage import view_at, Light
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as BF
from props import decals as D
from props import rusigns as R
from props import batyacast as B
from props import batyakit as K
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG, promo='ru',
              endcard=dict(style='batya', lang='ru', promise='ЗАВТРА: МИНУС 20, НЕ ЗАВОДИТСЯ'))
W = K.build()
BED, KIT = W['bedroom'], W['kitchen']
CUTS, NAMES = TL.CUTS, TL.NAMES
F0, F1 = TL.T0, TL.T1
OL = B.OL

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
LCD = {s: P(44, 16, [s], (176, 198, 150), [(20, 34, 20)], (90, 104, 80), pad=0.5) for s in ('37,2', '38,9')}
WILL = P(52, 60, ['ЗАВЕЩАНИЕ', 'ГАРАЖ — ТЁМЕ', 'УДОЧКИ —', 'НЕ ТРОГАТЬ!'], (252, 250, 240), [(34, 28, 30), (60, 60, 70), (60, 60, 70),
         (184, 30, 40)], (150, 140, 120), pad=0.8, weights=[1, 0.6, 0.6, 0.7], hand=True)


# ---------------------------------------------------------------- helpers
def mouth(who, t, k=1.7):
    return min(1.0, EPI.talk(who, t) * k)


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
    img = LCD[text]
    D.blit(big, v, img, wx - img.shape[1] / 8, wy - img.shape[0] / 8)


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Тридцать семь и два… Тёма, я помираю!» — close on Batya in bed: towel, red nose, sweat, the thermometer «37,2» held up"""
    z = 1.36 + 0.07 * sm(min(1.0, u / 2.8))
    v = view_at(BED, BX + 50, 230, z, 180, 300)
    st = {}

    def draw(CH, v_):
        cam, r = batya_bed(CH, v_, t, 'dying', pose=dict(B.BPOSE['dying'], n=(5.4, 23.8), f=(-0.6, 24.4)),
                           prop_n=thermo_prop(st, 1.7, -0.18))
        st['cam'] = cam
    big = bedroom(v, t, draw)
    lcd(big, v, st['cam'], st, '37,2')
    return big


def r_selfie(t, u, kitchen_=False):
    """«Это мой батя. Он помирает третий час.» — Tyoma's selfie stream: deadpan close-up, Batya moaning in bed behind him"""
    if kitchen_:
        v = view_at(KIT, 560, 330, 1.0, 180, 320)
    else:
        v = view_at(BED, 590, 330, 1.0, 180, 320)

    def draw(CH, v_):
        if not kitchen_:
            batya_bed(CH, v_, t, 'dying', pose=B.BPOSE['forehead'], sick=1.0)
        else:
            cam = v_.cam(470, 650, UN, flip=True)
            r = B.batya(CH, cam, B.BPOSE['shock'], t=t, mouth_=0.4, expr='shock', apron=True, vest=False,
                        prop_n=lambda L, h: F.ell(L, (h[0] + 0.4, h[1] - 1.6), 1.6, 1.2, (240, 240, 246)))     # waving a towel
            face(v_, cam, r, 3.2)
        cam = v_.cam(668, 1040, 26.0, flip=True)
        r = B.tema(CH, cam, B.TPOSE['selfie'], t=t, mouth_=mouth('tema', t), expr='deadpan', prop_n=None, hand_n=F.H(9.5, 17.0),
                   look=0.6)
        face(v_, cam, r, 2.6)

    def after(big, v_):
        if kitchen_:
            smoke(big, v_, t, 450, 300, t0=TL.T0['kitchen'], n=14, rise=360, size=120, a=0.72)
            smoke(big, v_, t, 560, 200, t0=TL.T0['kitchen'] - 0.5, n=8, rise=200, size=150, a=0.45, col=(96, 94, 100))
        vw = '48 012' if kitchen_ else f'{3 + int(9 * min(1.0, u / 2.0))}'
        K.phone_ui(big, t, vw)
    return (kitchen if kitchen_ else bedroom)(v, t, draw, after)


def r_will(t, u):
    """«Пиши завещание! Удочки — не трогать!» — the camera slides from the nightstand pharmacy to Batya ringing the bell, the will in hand"""
    x = lerp(700, 610, sm(min(1.0, u / 1.6)))
    v = view_at(BED, x, 300, 1.15, 180, 320)

    def draw(CH, v_):
        st = {}
        cam, r = batya_bed(CH, v_, t, 'dying', pose=dict(B.BPOSE['bell'], n=(4.8, 27.2), f=(1.6, 15.6)), prop_n=lambda L, h: B.bell(L, h, t, 0.6),
                           prop_f=lambda L, h: st.update(h=h))
        st['cam'] = cam
        DRAW_WILL[0] = (cam, st.get('h'))
    big = bedroom(v, t, draw)
    cam, h = DRAW_WILL[0]
    if h is not None:
        wx, wy = u2w(v, cam, h)
        D.blit(big, v, WILL, wx - 30, wy - 52)
    return big


DRAW_WILL = [(None, None)]


def r_bell(t, u):
    """«Ира-а! Бульончику! И пульт!» — close on Batya ringing the bell like mad, the frame shakes"""
    v = view_at(BED, BX + 40, 220, 1.4, 180, 300)

    def draw(CH, v_):
        batya_bed(CH, v_, t, 'shout', pose=dict(B.BPOSE['bell'], n=(4.8 + 0.6 * math.sin(t * 22), 27.0)),
                  prop_n=lambda L, h: B.bell(L, h, t, 1.0))
    big = bedroom(v, t, draw)
    BF.shake(big, t, 7, 34)
    fx.speed_lines(big, t, 0.5)
    return big


def ira_stand(CH, v, t, x, expr='dry', pose=None, coat=True, prop_n=None, un=UN, floor=FLOOR + 6, **kw):
    cam = v.cam(x, floor, un, flip=True)
    r = B.ira(CH, cam, pose or B.IPOSE['tray'], t=t, mouth_=mouth('ira', t), expr=expr, coat=coat, scarf=True, sick=0.8,
              prop_n=prop_n, **kw)
    face(v, cam, r, 2.6)
    return cam, r


def r_ira_in(t, u):
    """«Несу, Витя. Только не помирай.» — Ira comes in from the hallway in her coat and scarf with the tray, red nose (the clue)"""
    v = view_at(BED, 960, 330, 1.0, 180, 320)
    x = lerp(1150, 1010, sm(min(1.0, u / 1.8)))

    def draw(CH, v_):
        ira_stand(CH, v_, t, x, 'tired', prop_n=lambda L, h: B.tray(L, h, t))
    return bedroom(v, t, draw)


def r_sneeze(t, u):
    """Ira sneezes over Batya: a spray of droplets, he flinches"""
    v = view_at(BED, 680, 320, 0.98, 180, 320)

    def draw(CH, v_):
        batya_bed(CH, v_, t, 'shock', pose=B.BPOSE['forehead'])
        cam, r = ira_stand(CH, v_, t, 830, 'tired', pose=B.IPOSE['sneeze'], prop_f=lambda L, h: B.tray(L, h, t))
        hx, hy = u2w(v_, cam, r['mouth'])
        L = Layer(v_.wcam())
        for i in range(22):
            a, b, c, d, e = BF.SEED[i]
            k = min(1.0, u / 0.35) * (0.6 + 0.4 * c)
            F.dot(L, (hx - 220 * k * (0.6 + 0.6 * a), hy + (b - 0.5) * 80 * k + 40 * k * k), (170, 214, 255), 2.2 + 2 * d)
        CH.add(L)
    big = bedroom(v, t, draw)
    BF.shake(big, t, 6, 30)
    return big


def r_cover(t, u):
    """«Ира, не чихай на меня! Я болею!» — Batya pulls the blanket up to his nose, offended"""
    v = view_at(BED, BX + 30, 250, 1.36, 180, 300)

    def draw(CH, v_):
        batya_bed(CH, v_, t, 'angry', pose=B.BPOSE['hold'], cover=0.75, towel=True)
    return bedroom(v, t, draw)


def r_twist(t, u):
    """TWIST «Тридцать восемь и девять. Я на работу.» — Tyoma's lime sleeve holds the thermometer to Ira's forehead: «38,9»"""
    v = view_at(BED, 840, 290, 1.38, 180, 330)
    st = {}

    def draw(CH, v_):
        cam, r = ira_stand(CH, v_, t, 860, 'dry', pose=B.IPOSE['stand'], coat=True)
        hx, hy = u2w(v_, cam, r['head'])
        L = Layer(v_.wcam())                                                              # Tyoma's arm from the left edge
        F.cap(L, (hx - 220, hy + 110), (hx - 52, hy - 24), 15, 12, B.TC['hood'], B.TC['hood_hi'], B.TC['hood_sh'])
        F.ell(L, (hx - 46, hy - 26), 9, 8, B.TC['skin'], 0, B.TC['skin_hi'], B.TC['skin_sh'])
        F.outline(L, OL); CH.add(L)
        tc = v_.cam(hx - 46, hy - 26, UN)
        Lt = Layer(tc)
        st['m'] = B.thermometer(Lt, F.H(0, 0), ang=-0.12, size=1.6)
        F.outline(Lt, OL); CH.add(Lt)
        st['cam'] = tc
    big = bedroom(v, t, draw)
    lcd(big, v, st['cam'], st, '38,9')
    if u < 0.35: BF.shake(big, t, 9, 40)
    return big


def r_jump(t, u):
    """«Ира, ложись! Не трогай — я сам!» — Batya flies out of bed, the tiger plaid flies at the camera; «ИСЦЕЛЕНИЕ!»"""
    v = view_at(BED, 520, 330, 0.96, 180, 320)
    k = sm(min(1.0, u / 0.5))

    def draw(CH, v_):
        blankets(CH, v_, BED_TOP - 4, 330, 650, t, tiger=False)
        cam = v_.cam(lerp(500, 520, k), FLOOR + 50, UN * 1.05)
        r = B.batya(CH, cam, B.BPOSE['fists'], t=t, mouth_=mouth('batya', t), expr='fists' if u > 0.4 else 'shout',
                    sick=max(0.0, 1 - 2 * u), vest=False)
        face(v_, cam, r, 3.2)
        if u < 0.9: blankets(CH, v_, BED_TOP - 10, 330, 650, t, tiger=True, fly=min(1.0, u / 0.9))
    big = bedroom(v, t, draw)
    if u < 0.4: fx.speed_lines(big, t, 1.2)
    return big


def r_kitchen(t, u):
    """«Делов-то — пять минут!» — Batya in mum's flowery apron at the stove with a ladle, the pot steaming"""
    v = view_at(KIT, 520, 320, 1.08, 180, 320)

    def draw(CH, v_):
        L = Layer(v_.wcam())                                                              # big pot on the front-right burner
        F.poly(L, [(420, 366), (500, 366), (494, 300), (426, 300)], (200, 70, 60))
        F.ell(L, (460, 300), 34, 9, (150, 40, 34)); F.ell(L, (460, 300), 28, 6, (236, 196, 120))
        F.cap(L, (410, 318), (424, 318), 3, 3, (60, 40, 30)); F.cap(L, (496, 318), (510, 318), 3, 3, (60, 40, 30))
        F.outline(L, OL); CH.add(L)
        cam = v_.cam(610, 652, UN, flip=True)
        sw = 0.5 * math.sin(t * 6.0)
        r = B.batya(CH, cam, B.BPOSE['stir'], t=t, mouth_=mouth('batya', t), expr='smug', apron=True, vest=False, sick=0.0,
                    hand_n=F.H(6.8 + sw, 21.4), hand_f=F.H(3.4, 15.4),
                    prop_n=lambda L, h: (F.cap(L, h, (h[0] + 1.5, h[1] + 2.4), 0.16, 0.14, (180, 186, 196)),
                                         F.ell(L, (h[0] + 1.7, h[1] + 2.7), 0.7, 0.42, (200, 206, 216), 0, (240, 244, 250), (140, 146, 160))))
        face(v_, cam, r, 3.2)
    return kitchen(v, t, draw, after=lambda big, v_: BF.steam(big, v_, t, 460, 296, n=8, rise=160, size=50, a=0.5))


def r_smoke(t, u):
    return r_selfie(t, u, kitchen_=True)


def r_taste(t, u):
    """«Вкусно, Витя. Спасибо.» — Ira in bed in her scarf tastes the broth from a spoon, a tray on her lap"""
    v = view_at(BED, 500, 300, 1.12, 180, 320)

    def draw(CH, v_):
        cam, r = ira_bed(CH, v_, t, 'happy', x=BX, prop_n=B.spoon)
        blankets(CH, v_, BED_TOP + 9.6 * UN - 9.8 * UN, BX - 6 * UN, BX + 6.4 * UN, t)
        L = Layer(v_.wcam())                                                              # tray with the bowl on her lap
        F.cap(L, (BX - 70, 470), (BX + 60, 470), 4, 4, (176, 120, 70), (206, 150, 96), (130, 84, 44))
        F.ell(L, (BX - 6, 458), 30, 13, (246, 246, 240), 0, (255, 255, 255), (206, 210, 216)); F.ell(L, (BX - 6, 452), 22, 6, (236, 196, 90))
        F.outline(L, OL); CH.add(L)
    return bedroom(v, t, draw, after=lambda big, v_: BF.steam(big, v_, t, BX - 6, 446, n=5, rise=90, size=30, a=0.4))


def r_button(t, u):
    """«Ира… у меня опять тридцать семь и два!» — Batya sinks into bed beside her, puts the towel on his own forehead"""
    v = view_at(BED, 470, 300, 1.12, 180, 320)
    k = sm(min(1.0, u / 0.8))

    def draw(CH, v_):
        ira_bed(CH, v_, t, 'tired', x=BX, pose=B.IPOSE['stand'])
        batya_bed(CH, v_, t, 'dying', x=BX_L, pose=B.BPOSE['forehead'], sick=0.6 + 0.4 * k, towel=k > 0.5)
        blankets(CH, v_, BED_TOP + 9.6 * UN - 9.8 * UN, BX - 6 * UN, BX + 6.4 * UN, t, tiger=False)
    return bedroom(v, t, draw)


def r_loop(t, u):
    return r_hook(t, 0.0)


SHOT = dict(hook=r_hook, selfie=r_selfie, will=r_will, bell=r_bell, ira_in=r_ira_in, sneeze=r_sneeze, cover=r_cover, twist=r_twist,
            jump=r_jump, kitchen=r_kitchen, smoke=r_smoke, taste=r_taste, button=r_button, loop=r_loop)


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


QUESTION = K.question('ВАШ БАТЯ ПОМИРАЕТ ПРИ…?', 'ПИШИ ЦИФРУ')


def extra(big, t, shot):
    if TL.DUR - 2.6 <= t < TL.DUR - 1.0:
        k = min(1.0, (t - (TL.DUR - 2.6)) / 0.12)
        O.overlay(big, QUESTION, (big.shape[1] - QUESTION.shape[1]) // 2, 230, k)


SHOW = K.Show(EPI, 1, 1, ['37,2', 'ПОМИРАЮ!'], hook_t=(0.06, 2.9), hook_y=250,
              stickers=[(O.sticker('АПЧХИ!', fg=(170, 214, 255), size=96), F0['sneeze'], F0['cover'] + 0.3, 600, 430),
                        (O.sticker('38,9?!', fg=(255, 120, 110), size=120), TL.TWIST + 0.25, F0['jump'], 540, 520),
                        (O.sticker('ИСЦЕЛЕНИЕ!', fg=(255, 236, 120), size=84), F0['jump'] + 0.25, F0['kitchen'], 540, 560),
                        (O.sticker('ПРОШЛО: 5 МИН', fg=(255, 255, 255), size=58), F0['kitchen'] + 0.2, F0['smoke'], 540, 470),
                        (O.sticker('ПРОШЛО: 2 ЧАСА', fg=(255, 214, 60), size=58), F0['smoke'] + 0.1, F0['taste'], 540, 470)],
              flashes=[TL.TWIST + 0.02], mosaics=[F0['kitchen']], extra=extra,
              cap_y={'hook': 1460, 'twist': 1460, 'selfie': 1460, 'smoke': 1460}, cap_default=1400)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
