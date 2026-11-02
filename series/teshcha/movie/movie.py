"""«ТЁЩА НА НЕДЕЛЬКУ: ЗАГОВОР» — 16:9 mini-movie. One day by the clock: Tolik's 42nd birthday, an overheard «балкон замуруем»,
an escape foiled by the grannies' network and Lyusya's minibus, a storm of the balcony — TWIST 1: it is a gift, «КАБИНЕТ ТОЛИКА».
At the party Tolik toasts «оставайтесь хоть навсегда» — TWIST 2: she was leaving for good tomorrow; now she stays.
  python3 movie.py prep                      # flashback frames from the season episodes
  python3 movie.py sheet 0 5 12 …            # mini sheet of shots (middle frames)
  python3 movie.py all | shots <i>…          # render (per shot), then python3 mix.py"""
import os
os.environ['PV_WIDE'] = '1'
import sys, pathlib, math, subprocess
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine'))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import stage as ST
from stage import view_at, Light, OUT_W, OUT_H
from scene import Layer, sm, lerp
import overlays as O
import fx
import paths as P
from episode import Episode
from props import folk as F
from props import bytfx as B
from props import decals as D
from props import rusigns as R
from props import teshcast as T
from props import teshkit as K
from props import teshshots as SH
from props.teshshots import u2w, face
import timeline as TL

assert (OUT_W, OUT_H) == (1920, 1080)
SX, SY = 320, 180
COL = dict(K.COL, lyusya=(200, 140, 255), babki=(240, 240, 250), granny=(240, 240, 250), granny2=(220, 230, 250))
EPI = Episode('movie', TL.VOICE, TL.DUR, TL.FPS, colors=COL, slug=TL.SLUG,
              endcard=dict(style='teshcha', lang='ru', sec=3.0, cy=860, promise='СЕЗОН 2: ТЁЩА НА ДАЧЕ'))
SH.init(EPI, day=365)
BK = f'{TL.SLUG}-movie'
HALL, KIT, YARD, MINI = SH.world('hallway'), SH.world('kitchen'), SH.world('yard'), SH.world('minibus')
ROOM, BALC = SH.ROOM, SH.BALC
RED, YEL, INK = (184, 30, 40), (255, 244, 170), (34, 28, 30)
OL = T.OL


def mouth(who, t, k=1.7):
    return min(1.0, EPI.talk(who, t) * k)


def _p(lines, w, h, bg=(250, 248, 240), fg=INK, border=(120, 110, 100), tilt=0, weights=None):
    kw = dict(bg=bg, colors=[fg] * len(lines), border=border, pad=1.0, tilt=tilt)
    if weights: kw['weights'] = weights
    return R.plate(w, h, lines, **kw)


D.attach(HALL, [
    (_p(['ДЕНЬ', '366'], 30, 38, fg=RED, weights=[0.55, 1]), 205, 160),
    (_p(['С ДНЁМ', 'РОЖДЕНИЯ?'], 50, 26, bg=YEL, fg=RED, border=(150, 130, 70), tilt=-4), 1094, 300),
    (_p(['ТАПКИ ТОЛИКА'], 58, 12, bg=(236, 206, 120), border=(120, 84, 30)), 790, 508),
])
D.attach(KIT, [
    (_p(['ВТОРНИК'], 44, 16, fg=RED), 70, 90),
    (_p(['КАША —', 'ДЛЯ МУЖИКА'], 52, 24, bg=YEL, fg=RED, border=(150, 130, 70), tilt=3), 186, 232),
    (_p(['СОЛЕНЬЯ'], 36, 14), 1000, 112),
])
D.attach(YARD, [
    (_p(['ГАРАЖ 13'], 40, 14, bg=(236, 236, 230)), 110, 430),
    (_p(['НЕ ПАРКОВАТЬСЯ!'], 64, 16, bg=(250, 250, 250), fg=RED, border=RED), 270, 440),
    (_p(['ОСТАНОВКА «ДОМ 33»'], 80, 14, bg=(40, 90, 170), fg=(255, 255, 255), border=(20, 40, 90)), 820, 392),
    (_p(['ЛАВОЧКА', 'ИНФОРМБЮРО'], 56, 22, bg=YEL, fg=RED, border=(150, 130, 70), tilt=3), 1040, 420),
])
D.attach(MINI, [
    (_p(['ПРОЕЗД 40 Р.'], 58, 16, bg=YEL, fg=RED, border=(150, 130, 70)), 452, 160),
    (_p(['ОСТАНОВКИ ПО ТРЕБОВАНИЮ'], 78, 14), 598, 166),
    (_p(['ШАПКУ НАДЕНЬ!'], 56, 16, bg=YEL, fg=RED, border=(150, 130, 70), tilt=-6), 236, 418),
])
SIGN = _p(['КАБИНЕТ', 'ТОЛИКА'], 96, 46, bg=(236, 206, 120), fg=(90, 30, 20), border=(120, 70, 30), weights=[0.7, 1])
TAG = _p(['РАЯ.', 'ДОМОЙ'], 36, 22, bg=(250, 250, 240), fg=RED, border=(120, 110, 100))
CEMENT = _p(['ЦЕМЕНТ', 'М-500'], 46, 26, bg=(220, 220, 214), fg=INK, border=(120, 120, 120), weights=[1, 0.6])


# ======================================================================================= lights + scene helper
def light_hall(v):
    lx, ly = v.opt(610.0, 80.0)
    return Light(amb=(1.02, 0.96, 0.88), keys=[(lx, ly, 1500, (255, 210, 140), 0.55)], rim=(-1, -0.4, (255, 220, 170), 0.3), grad=(1.04, 0.9))


def light_night(v):
    return Light(amb=(0.55, 0.6, 0.85), keys=[], rim=(-1, -0.4, (200, 220, 255), 0.3), grad=(1.0, 0.85))


def light_kit(v):
    wx, wy = v.opt(620.0, 120.0)
    return Light(amb=(1.03, 0.98, 0.9), keys=[(wx, wy, 1500, (255, 220, 160), 0.6)], rim=(1, -0.4, (255, 230, 180), 0.35), grad=(1.04, 0.9))


def light_yard(v):
    lx, ly = v.opt(790.0, 170.0)
    return Light(amb=(0.96, 0.99, 1.06), keys=[(lx, ly, 1000, (255, 214, 150), 0.25)], rim=(1, -0.4, (220, 236, 255), 0.35), grad=(1.03, 0.94))


def light_mini(v):
    lx, ly = v.opt(650.0, 110.0)
    return Light(amb=(1.0, 0.95, 0.88), keys=[(lx, ly, 1300, (255, 214, 150), 0.5)], rim=(1, -0.4, (210, 226, 255), 0.35), grad=(1.04, 0.9))


def light_cab(v):
    hx, hy = v.opt(620.0, 120.0)
    return Light(amb=(1.04, 0.95, 0.86), keys=[(hx, hy, 1500, (255, 200, 120), 0.6)], rim=(1, -0.3, (190, 214, 255), 0.35), grad=(1.04, 0.9))


def sc(world, light, cx, cy, Z, t, draw=None, motes=None, snow=None, after=None, vign=0.26):
    v = view_at(world, cx, cy, Z, SX, SY)
    return SH.generic(world, v, t, (lambda CH, v_: draw(CH, v_)) if draw else None, light=light(v), motes=motes, snow=snow,
                      after=after, vign=vign), v


def nightsc(world, cx, cy, Z, t, draw, lamp, Zr=600):
    v = view_at(world, cx, cy, Z, SX, SY)
    CH, FX = K.begin()
    big = v.bg(); night(big, 1.0)
    lx, ly = v.opt(*lamp)
    fx.glow(big, lx, ly, Zr, (255, 214, 140), 0.25)
    draw(CH, v)
    CH.comp(big, Light(amb=(0.7, 0.68, 0.78), keys=[(lx, ly, Zr * 1.4, (255, 220, 150), 0.8)], rim=(-1, -0.4, (255, 220, 150), 0.4),
                        grad=(1.0, 0.85)))
    fx.vignette(big, 0.4)
    return big, v


def night(big, k=1.0):
    big[:] = (big.astype(np.float32) * (1 - k * np.array((0.62, 0.58, 0.4)))).astype(np.uint8)


def blur(big, r=10):
    big[:] = np.asarray(Image.fromarray(big).filter(ImageFilter.GaussianBlur(r)))


# ======================================================================================= characters
def tol(CH, v, t, x, y, un, flip=False, pose='stand', expr='normal', m=None, hat=None, bow=False, colander=0.0, party=False,
        gear=False, **kw):
    cam = v.cam(x, y, un, flip=flip)
    pp = T.TPOSE[pose] if isinstance(pose, str) else pose
    r = T.tolik(CH, cam, pp, t=t, mouth_=mouth('tolik', t) if m is None else m, expr=expr, hat=hat, **kw)
    L = Layer(cam)
    if bow:                                                                           # festive bow tie
        F.poly(L, [F.H(0.0, 22.6), F.H(1.1, 23.2), F.H(1.1, 22.0)], (200, 30, 50))
        F.poly(L, [F.H(2.2, 22.6), F.H(1.1, 23.2), F.H(1.1, 22.0)], (200, 30, 50))
        F.dot(L, F.H(1.1, 22.6), (240, 80, 90), 0.3)
    if gear:                                                                          # scarf like in E04
        F.ell(L, F.H(0.3, 22.8), 2.1, 0.9, (40, 120, 200), 0, (90, 170, 236), (24, 80, 150))
        F.cap(L, F.H(1.5, 22.4), F.H(2.1, 18.4), 0.6, 0.65, (40, 120, 200))
    hx, hy = r['top']
    if colander > 0:                                                                  # kitchen colander as a helmet
        dy = (1 - colander) * 4.0
        F.ell(L, (hx + 0.2, hy + 0.9 + dy), 2.7, 1.7, (190, 194, 204), 0, (236, 238, 244), (140, 144, 156))
        F.cap(L, (hx - 2.6, hy + 1.9 + dy), (hx + 3.0, hy + 1.9 + dy), 0.3, 0.3, (140, 144, 156))
        for k in range(5): F.dot(L, (hx - 1.4 + k * 0.75, hy + 0.6 + dy + (k % 2) * 0.5), (60, 60, 70), 0.18)
        F.cap(L, (hx + 2.6, hy + 1.6 + dy), (hx + 3.6, hy + 1.2 + dy), 0.25, 0.25, (140, 144, 156))
    if party:                                                                         # paper party hat
        F.poly(L, [(hx - 1.2, hy + 0.8), (hx + 1.4, hy + 0.8), (hx + 0.3, hy - 3.2)], (90, 200, 220))
        for k in range(3): F.dot(L, (hx - 0.3 + k * 0.4, hy - 0.2 - k * 0.9), (255, 220, 60), 0.25)
        F.dot(L, (hx + 0.3, hy - 3.3), (255, 80, 120), 0.45)
    F.outline(L, OL); CH.add(L)
    face(v, cam, r)
    return cam, r


def rai(CH, v, t, x, y, un, flip=False, pose='stand', expr='sweet', who='raisa', pal=None, **kw):
    cam = v.cam(x, y, un, flip=flip)
    pp = T.RPOSE[pose] if isinstance(pose, str) else pose
    r = T.raisa(CH, cam, pp, t=t, mouth_=mouth(who, t), expr=expr, pal=pal, **kw)
    face(v, cam, r, 3.6)
    return cam, r


def lyu(CH, v, t, x, y, un, **kw):
    return rai(CH, v, t, x, y, un, who='lyusya', pal=T.LYUSYA, **{'expr': 'stern', **kw})


GR = [dict(T.GRANNY[0]), dict(T.GRANNY[1])]


def gran(CH, v, t, i, x, y, un, who=None, **kw):
    return rai(CH, v, t, x, y, un, who=who or ('granny' if i == 0 else 'granny2'), pal=GR[i], **{'expr': 'stern', **kw})


def pus(CH, v, t, x, y, un, expr='deadpan', m=None, hat=False, **kw):
    cam = v.cam(x, y, un)
    r = T.pusya(CH, cam, t=t, mouth_=mouth('pusya', t, 2.0) if m is None else m, expr=expr, **kw)
    if hat:
        hc = r['head']; L = Layer(cam)
        F.ell(L, (hc[0], hc[1] - 1.05), 1.55, 0.95, (196, 40, 52), 0, (232, 80, 84), (140, 26, 36))
        F.ell(L, (hc[0], hc[1] - 2.15), 0.6, 0.55, (246, 240, 230)); F.outline(L, OL); CH.add(L)
    face(v, cam, r, 2.0)
    return cam, r


def sve(CH, v, t, x, y, un, flip=False, pose='stand', expr='tired', **kw):
    cam = v.cam(x, y, un, flip=flip)
    r = T.sveta(CH, cam, T.SPOSE[pose] if isinstance(pose, str) else pose, t=t, mouth_=mouth('sveta', t), expr=expr, **kw)
    face(v, cam, r)
    return cam, r


def cu(world, light, t, who_fn, x, y, un, k=1.35, head=27.0, Z=1.42, dx=0.0, after=None, pre=(), post=(), **kw):
    """close-up on a standing hero: camera on the head; pre/post — extra draw callables (CH, v)"""
    U = un * k
    yy = y + 40
    v0 = view_at(world, x + dx, yy - head * U + 30, Z, SX, SY)

    def draw(CH, v_):
        for f in pre: f(CH, v_)
        who_fn(CH, v_, t, x, yy, U, **kw)
        for f in post: f(CH, v_)
    big = SH.generic(world, v0, t, draw, light=light(v0), after=after)
    return big


# ======================================================================================= props (unit coords of a hero)
def rod(L, h):
    F.cap(L, h, (h[0] + 7.0, h[1] - 9.0), 0.16, 0.08, (120, 80, 40))
    F.ell(L, (h[0] + 0.6, h[1] - 0.4), 0.45, 0.45, (60, 60, 66))
    F.cap(L, (h[0] + 7.0, h[1] - 9.0), (h[0] + 7.6, h[1] - 4.0), 0.04, 0.04, (230, 230, 230))


def mop(L, h):
    F.cap(L, (h[0] - 1.0, h[1] + 3.0), (h[0] + 3.0, h[1] - 9.0), 0.22, 0.22, (170, 120, 70))
    for k in range(6):
        F.cap(L, (h[0] + 3.0, h[1] - 9.0), (h[0] + 2.0 + k * 0.45, h[1] - 11.4), 0.22, 0.18, (230, 226, 210))


def drill(L, h):
    F.poly(L, [(h[0] - 0.4, h[1] - 0.4), (h[0] + 2.4, h[1] - 0.6), (h[0] + 2.4, h[1] - 1.8), (h[0] - 0.6, h[1] - 1.8)], (230, 120, 30))
    F.cap(L, (h[0] + 2.4, h[1] - 1.2), (h[0] + 4.0, h[1] - 1.2), 0.12, 0.08, (200, 200, 210))
    F.cap(L, (h[0], h[1] - 0.4), (h[0] - 0.2, h[1] + 1.2), 0.4, 0.4, (40, 40, 46))


def glass(L, h):
    F.poly(L, [(h[0] - 0.5, h[1] - 0.2), (h[0] + 0.5, h[1] - 0.2), (h[0] + 0.4, h[1] - 2.0), (h[0] - 0.4, h[1] - 2.0)], (220, 120, 60))
    F.cap(L, (h[0] - 0.5, h[1] - 2.0), (h[0] + 0.5, h[1] - 2.0), 0.1, 0.1, (240, 240, 250))


def tape(L, h):
    F.ell(L, h, 0.9, 0.9, (250, 210, 40), 0, (255, 240, 120), (200, 160, 20))
    F.cap(L, (h[0] + 0.6, h[1]), (h[0] + 6.0, h[1] - 0.6), 0.12, 0.12, (250, 220, 60))


def plank(L, h):
    F.poly(L, [(h[0] - 1.0, h[1] + 3.0), (h[0] + 0.6, h[1] + 3.2), (h[0] + 1.6, h[1] - 8.0), (h[0], h[1] - 8.2)], (220, 180, 120))


def mic(L, h):
    F.cap(L, h, (h[0] + 0.6, h[1] - 1.6), 0.25, 0.25, (40, 40, 46)); F.ell(L, (h[0] + 0.7, h[1] - 1.9), 0.5, 0.5, (160, 160, 170))


def gift(L, h):
    F.poly(L, [(h[0] - 1.2, h[1] + 0.6), (h[0] + 1.2, h[1] + 0.6), (h[0] + 1.2, h[1] - 1.6), (h[0] - 1.2, h[1] - 1.6)], (90, 170, 220))
    F.cap(L, (h[0], h[1] + 0.6), (h[0], h[1] - 1.6), 0.25, 0.25, (220, 40, 60))
    F.ell(L, (h[0], h[1] - 1.8), 0.6, 0.35, (220, 40, 60))


def suitcase(L, x, y, s=1.0):
    """Raisa's suitcase by the door (world px)"""
    F.poly(L, [(x - 40 * s, y), (x + 40 * s, y), (x + 40 * s, y - 64 * s), (x - 40 * s, y - 64 * s)], (130, 70, 50))
    F.poly(L, [(x - 40 * s, y - 30 * s), (x + 40 * s, y - 30 * s), (x + 40 * s, y - 36 * s), (x - 40 * s, y - 36 * s)], (90, 50, 36))
    F.cap(L, (x - 14 * s, y - 64 * s), (x - 14 * s, y - 74 * s), 2, 2, (60, 40, 30)); F.cap(L, (x + 14 * s, y - 64 * s), (x + 14 * s, y - 74 * s), 2, 2, (60, 40, 30))
    F.cap(L, (x - 14 * s, y - 74 * s), (x + 14 * s, y - 74 * s), 2, 2, (60, 40, 30))
    F.outline(L, OL)


def sack(L, x, y, s=1.0):
    F.poly(L, [(x - 34 * s, y), (x + 34 * s, y), (x + 28 * s, y - 70 * s), (x - 28 * s, y - 70 * s)], (200, 196, 186))
    F.poly(L, [(x - 28 * s, y - 70 * s), (x + 28 * s, y - 70 * s), (x + 18 * s, y - 80 * s), (x - 18 * s, y - 80 * s)], (176, 172, 160))
    F.outline(L, OL)


def gazelle(L, x, y, s=1.0):
    """yellow route minibus facing left (as in E04), Lyusya's purple perm in the windshield"""
    def p(dx, dy): return (x + dx * s, y + dy * s)
    yel, yel_sh, yel_hi = (236, 196, 40), (190, 150, 24), (252, 224, 110)
    F.poly(L, [p(-218, -48), p(196, -48), p(196, -222), p(-150, -222), p(-180, -190), p(-212, -120), p(-220, -70)], yel)
    F.poly(L, [p(-206, -120), p(-174, -192), p(-128, -192), p(-128, -120)], (130, 170, 196))
    F.ell(L, p(-160, -150), 20 * s, 20 * s, (130, 70, 160)); F.ell(L, p(-170, -132), 12 * s, 14 * s, (240, 192, 162))
    for k in range(5):
        x0 = -112 + k * 60
        F.poly(L, [p(x0, -192), p(x0 + 50, -192), p(x0 + 50, -130), p(x0, -130)], (96, 120, 144))
    F.poly(L, [p(-212, -84), p(196, -84), p(196, -72), p(-214, -72)], (196, 40, 52))
    F.ell(L, p(-214, -96), 9 * s, 7 * s, (255, 240, 170))
    for wx in (-140, 128):
        F.ell(L, p(wx, -18), 30 * s, 30 * s, (40, 40, 46)); F.ell(L, p(wx, -18), 13 * s, 13 * s, (170, 170, 176))
    F.outline(L, OL)


def wheel_ring(L):
    cx, cy, rx, ry = 215.0, 548.0, 112.0, 60.0
    for i in range(28):
        a0, a1 = i / 28 * 6.283, (i + 1) / 28 * 6.283
        F.cap(L, (cx + rx * math.cos(a0), cy + ry * math.sin(a0)), (cx + rx * math.cos(a1), cy + ry * math.sin(a1)), 12, 12, (214, 190, 150))
    F.outline(L, OL)


# ======================================================================================= the balcony cabinet (world px of BALC)
CHX, CHY, CHS = 790.0, 676.0, 0.9                                   # Tolik's armchair in the cabinet


def cabinet(L, t, k=1.0, lights=True):
    """the balcony turned into «КАБИНЕТ ТОЛИКА»: k = how far the works went (0.4 = half done, 1 = finished)"""
    wood, wood_d = (206, 160, 104), (170, 124, 74)
    ST.wrect(L, 180, 470, 1010, 560, wood)                                            # panelled wall under the window
    for xx in range(190, 1010, 34): ST.wrect(L, xx, 470, xx + 3, 560, wood_d)
    if k > 0.5:
        ST.wrect(L, 1000, 0, 1280, 720, wood)                                         # the junk corner is panelled over
        for xx in range(1006, 1280, 34): ST.wrect(L, xx, 0, xx + 3, 720, wood_d)
        ST.wrect(L, 1040, 150, 1250, 420, (150, 40, 50))                              # a carpet on the wall
        ST.wrect(L, 1056, 166, 1234, 404, (190, 70, 60))
        F.ell(L, (1145, 285), 60, 80, (230, 190, 90)); F.ell(L, (1145, 285), 30, 40, (150, 40, 50))
        F.ell(L, (600, 690), 230, 34, (170, 50, 60)); F.ell(L, (600, 690), 190, 24, (200, 90, 80))   # rug
        x0, y0 = 300, 640                                                                 # oil heater
        for i in range(6): F.cap(L, (x0 + i * 12, y0), (x0 + i * 12, y0 - 70), 5, 5, (220, 220, 226))
        F.ell(L, (x0 + 30, y0 - 78), 6, 4, (240, 90, 60))
    else:
        for i in range(4): ST.wrect(L, 1010 + i * 40, 60 + i * 10, 1040 + i * 40, 700, wood)   # panels leaning, half done
    if k > 0.9:
        T.tv_rubin(L, 990, 640, 0.9)
        for x0, x1 in ((280, 350), (940, 1010)):                                      # warm drapes on the window
            F.poly(L, [(x0, 50), (x1, 50), (x1 + 6, 470), (x0 - 6, 470)], (170, 50, 60))
            for xx in range(x0 + 8, x1, 16): F.cap(L, (xx, 56), (xx + 2, 466), 1.5, 1.5, (140, 36, 46))
        F.poly(L, [(270, 40), (1020, 40), (1020, 62), (270, 62)], (150, 40, 50))
        F.poly(L, [(560, 470), (720, 470), (720, 478), (560, 478)], (120, 80, 50))                # a shelf with a trophy
        F.poly(L, [(630, 470), (650, 470), (656, 440), (624, 440)], (240, 200, 60)); F.ell(L, (640, 434), 14, 10, (250, 214, 70))
    if lights:                                                                       # garland along the window top
        for i in range(22):
            x = 300 + i * 32; y = 72 + 8 * math.sin(i * 0.8)
            on = (int(t * 3) + i) % 3 != 0
            F.dot(L, (x, y), [(255, 80, 90), (255, 220, 60), (90, 200, 255), (120, 230, 120)][i % 4] if on else (90, 80, 70), 5)
    F.outline(L, OL)


def balc(v, t, draw=None, k=1.0, warm=True, after=None, snow=40):
    CH, FX = K.begin()
    big = v.bg()
    L = Layer(v.wcam()); cabinet(L, t, k); CH.add(L)
    if draw: draw(CH, v)
    CH.comp(big, light_cab(v) if warm else K.light_balcony(v))
    B.falling_snow(FX, v, t, 300, 80, 990, 440, n=snow, speed=50)
    FX.comp(big)
    if k > 0.5: D.blit(big, v, SIGN, 1086, 40)
    if after: after(big, v)
    fx.vignette(big, 0.28)
    return big


def bview(cx, cy, Z):
    return view_at(BALC, cx, cy, Z, SX, SY)


def tol_chair(CH, v, t, un=13.0, x=CHX, y=CHY, s=CHS, **kw):
    SH.chair(CH, v, s, 'back', x, y)
    seat = y - 64 * s
    pose = kw.pop('pose', dict(T.TPOSE['sit'], nleg=(1.45, -0.3), fleg=(1.35, -0.25)))
    cam, r = tol(CH, v, t, x - 4, seat + 13.6 * un, un, pose=pose, **kw)
    SH.chair(CH, v, s, 'front', x, y)
    return cam, r


# ======================================================================================= flashbacks (season episodes)
FBW, FBH = 486, 797
FB_LABEL = dict(ep01='СЕРИЯ 1', ep02='СЕРИЯ 2', ep03='СЕРИЯ 3', ep05='СЕРИЯ 5')


def prep():
    for c in TL.CLIPS:
        d = pathlib.Path(P.build(BK, f'fb/{c["ep"]}')); d.mkdir(parents=True, exist_ok=True)
        if len(list(d.glob('*.png'))) > 10: continue
        src = ROOT / 'series' / TL.SLUG / 'episodes' / c['ep'] / 'final.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(c['a']), '-i', str(src), '-t', str(c['b'] - c['a'] + 0.1),
                        '-vf', f'fps=30,crop=1080:1770:0:150,scale={FBW}:{FBH}:flags=area', str(d / '%04d.png')], check=True)
        print(d)


def fb_frame(ep, i):
    d = pathlib.Path(P.build(BK, f'fb/{ep}'))
    fs = sorted(d.glob('*.png'))
    if not fs: prep(); fs = sorted(d.glob('*.png'))
    return np.array(Image.open(fs[max(0, min(len(fs) - 1, i))]).convert('RGB'))


def r_fb(t, s, u):
    fr = fb_frame(s['ep'], int(max(0.0, u - 0.25) * 30))
    bgi = np.array(Image.fromarray(fr).resize((OUT_W, int(OUT_W * FBH / FBW)), Image.NEAREST))
    y0 = (bgi.shape[0] - OUT_H) // 2
    big = bgi[y0:y0 + OUT_H].copy()
    blur(big, 16); big[:] = (big * 0.35).astype(np.uint8)
    ph = np.full((FBH + 40, FBW + 40, 3), 244, np.uint8); ph[20:20 + FBH, 20:20 + FBW] = fr
    ph = np.array(Image.fromarray(ph).rotate(-2.0, resample=Image.NEAREST, expand=True, fillcolor=(0, 0, 0)))
    m = ph.sum(2) > 0
    x0, yy0 = (OUT_W - ph.shape[1]) // 2, (OUT_H - ph.shape[0]) // 2
    reg = big[yy0:yy0 + ph.shape[0], x0:x0 + ph.shape[1]]; reg[m] = ph[m]
    O.overlay(big, img('fbl_' + s['ep'], lambda: K.title_trim(K.hook_title(['ВОСПОМИНАНИЕ'], 44, width=900))), 120, 120, 1.0)
    O.overlay(big, img('fbe_' + s['ep'], lambda: O.make_badge(FB_LABEL[s['ep']], 30)), 1460, 940, 1.0)
    if u < 0.12: O.flash(big, 0.6 * (1 - u / 0.12))
    return big


_IMG = {}


def img(key, fn):
    if key not in _IMG: _IMG[key] = fn()
    return _IMG[key]


# ======================================================================================= 0. cold open (night hallway)
def r_hook(t, s, u):
    """«Сегодня мне сорок два. А тёща готовит заговор.» — night, Tolik among the coats with a flashlight under his chin"""
    def draw(CH, v):
        tol(CH, v, t, 760, 732, 20.0, flip=True, pose=dict(T.TPOSE['phone'], n=(3.0, 21.0)), expr='shock', look=0.6,
            prop_n=lambda L, h: B.flashlight(L, h, -1.9))
    big, v = nightsc(HALL, 720, 160 - 10 * sm(u / 3), 1.3 + 0.05 * sm(u / 3), t, draw, (760, 260), 700)
    return big


def r_evidence(t, s, u):
    """three inserts: cement sack, tape measure, suitcase «РАЯ. ДОМОЙ» — each in a torch spot"""
    i = min(2, int(u / 1.0))
    def draw(CH, v):
        L = Layer(v.wcam())
        if i == 0: sack(L, 980, 700, 1.4)
        elif i == 1:
            F.ell(L, (410, 340), 22, 22, (250, 210, 40), 0, (255, 240, 120), (200, 160, 20)); F.ell(L, (410, 340), 8, 8, (60, 60, 60))
            F.outline(L, OL)
        else: suitcase(L, 1080, 700, 1.3)
        CH.add(L)
    pos = [(980, 620), (410, 330), (1080, 640)][i]
    big, v = nightsc(HALL, pos[0], pos[1], 1.42 + 0.06 * (u % 1.0), t, draw, pos, 600)
    if i == 0: D.blit(big, v, CEMENT, 980 - 32, 700 - 70)
    if i == 2: D.blit(big, v, TAG, 1080 - 18, 700 - 60)
    if (u % 1.0) < 0.08: O.flash(big, 0.4)
    return big


def r_closet(t, s, u):
    def draw(CH, v):
        tol(CH, v, t, 760, 692, 14.0, flip=True, pose=dict(T.TPOSE['phone'], n=(3.0, 21.0)), expr='shock',
            prop_n=lambda L, h: B.flashlight(L, h, -1.9))
        pus(CH, v, t, 640, 700, 8.0, expr='deadpan', m=0.0)
    big, v = nightsc(HALL, 720, 420, 0.95, t, draw, (740, 360), 700)
    return big


def r_pusya_closet(t, s, u):
    def draw(CH, v): pus(CH, v, t, 640, 700, 19.0, expr='deadpan')
    big, v = nightsc(HALL, 640, 620, 1.42, t, draw, (640, 560), 700)
    return big


def r_title(t, s, u):
    big, v = sc(HALL, light_night, 700, 380, 1.0, t)
    night(big, 0.85); blur(big, 6)
    d = img('title_doily', lambda: K.doily(900, 220, ['ТЁЩА НА НЕДЕЛЬКУ', 'ФИЛЬМ']))
    k = sm(u / 0.4)
    O.overlay(big, d, (OUT_W - d.shape[1]) // 2, 250, k)
    tt = img('title_main', lambda: K.title_trim(K.hook_title(['ЗАГОВОР'], 150, width=1800)))
    O.overlay(big, tt, (OUT_W - tt.shape[1]) // 2, 520, sm((u - 0.4) / 0.3))
    return big


# ======================================================================================= chapter cards
CARD = dict(card_0700=('07:00', 'ВТОРНИК, ТОЛЕЧКА', KIT, light_kit, 900, 400), card_0830=('08:30', '«ЗАМУРУЕМ»', HALL, light_hall, 640, 400),
            card_1000=('10:00', 'ПОБЕГ', YARD, light_yard, 640, 400), card_1200=('17:00', 'РАЗВЕДКА', HALL, light_hall, 700, 380),
            card_1300=('17:30', 'ШТУРМ', BALC, K.light_balcony, 640, 400), card_1500=('18:30', 'КАК МУЖИК', BALC, light_cab, 640, 400),
            card_1900=('20:00', 'ПРАЗДНИК', ROOM, K.light_room, 640, 400), card_2100=('23:00', 'КАБИНЕТ', BALC, light_cab, 640, 400))


def r_card(t, s, u):
    tm, label, W, lf, cx, cy = CARD[s['name']]
    big, v = sc(W, lf, cx, cy, 0.9 + 0.03 * u, t)
    blur(big, 8); big[:] = (big * 0.45).astype(np.uint8)
    clk = img('clk_' + tm, lambda: K.title_trim(K.hook_title([tm], 190, width=1400)))
    lab = img('lab_' + label, lambda: K.title_trim(K.hook_title([label], 70, width=1700)))
    k = sm(u / 0.25)
    O.overlay(big, clk, (OUT_W - clk.shape[1]) // 2, 300 - int(30 * (1 - k)), k)
    O.overlay(big, lab, (OUT_W - lab.shape[1]) // 2, 620, sm((u - 0.3) / 0.25))
    return big


# ======================================================================================= 1. 07:00 kitchen
STOOL = (900.0, 690.0)
TOP = 452.0


def tol_stool(CH, v, t, un=12.0, **kw):
    seat = STOOL[1] - 86
    L = Layer(v.wcam())
    F.ell(L, (STOOL[0] - 6, seat + 4), 34, 9, (150, 96, 60)); F.cap(L, (STOOL[0] - 24, seat + 8), (STOOL[0] - 29, STOOL[1]), 3.5, 3, (110, 70, 44))
    F.cap(L, (STOOL[0] + 20, seat + 8), (STOOL[0] + 24, STOOL[1]), 3.5, 3, (110, 70, 44)); F.outline(L, OL); CH.add(L)
    return tol(CH, v, t, STOOL[0] - 10, seat + 13.6 * un, un, pose=dict(T.TPOSE['sit'], nleg=(1.45, -0.3), fleg=(1.35, -0.25)), **kw)


def porridge(CH, v):
    L = Layer(v.wcam())
    F.ell(L, (1010, TOP + 2), 40, 12, (244, 244, 236), 0, (255, 255, 255), (200, 204, 210)); F.ell(L, (1010, TOP - 2), 28, 8, (240, 220, 170))
    F.cap(L, (1030, TOP - 6), (1060, TOP - 40), 2.5, 2.5, (200, 200, 210))
    F.outline(L, OL); CH.add(L)


def r_kitchen_wide(t, s, u):
    def draw(CH, v):
        rai(CH, v, t, 720, 690, 12.6, pose='hold', expr='sweet')
        sve(CH, v, t, 520, 700, 13.0, pose=dict(T.SPOSE['stand'], f=(-2.6, 10.6)), expr='smile', prop_f=gift)
        tol_stool(CH, v, t, 12.0, expr='proud', bow=True, m=0.0)
        porridge(CH, v)
    big, v = sc(KIT, light_kit, 800 + 30 * sm(u / 2), 420, 0.82, t, draw)
    B.steam(big, v, t, 720 + 30, 500, -99, n=6, rise=120, size=40, a=0.4)
    return big


def r_raisa_kasha(t, s, u, expr='sweet'):
    return cu(KIT, light_kit, t, rai, 720, 690, 12.6, k=1.4, head=20.5, dx=40, pose='stand', expr=expr)


def r_tolik_shirt(t, s, u, expr='proud', sticker=None):
    un = 12.0 * 1.4
    seat = STOOL[1] - 86
    v = view_at(KIT, STOOL[0] + 10, seat + 13.6 * un - 27 * un + 70, 1.42, SX, SY)
    def draw(CH, v_):
        tol_stool(CH, v_, t, un, expr=expr, bow=True)
        porridge(CH, v_)
    return SH.generic(KIT, v, t, draw, light=light_kit(v))


def r_sveta_wink(t, s, u):
    return cu(KIT, light_kit, t, sve, 520, 700, 13.0, k=1.35, head=24.0, dx=30, pose=dict(T.SPOSE['stand'], f=(-2.6, 10.6)),
              expr='smile', prop_f=gift, blink=False)


def r_tolik_sulk(t, s, u):
    return r_tolik_shirt(t, s, u, expr='sad')


def r_pusya_k(t, s, u):
    def draw(CH, v): pus(CH, v, t, 1100, 700, 19.0)
    return sc(KIT, light_kit, 1100, 610, 1.42, t, draw)[0]


# ======================================================================================= 2. 08:30 hallway: «замуруем»
RPH = (440.0, 700.0, 14.0)                                          # Raisa at the wall phone, facing left


def raisa_phone(CH, v, t, un=14.0, **kw):
    return rai(CH, v, t, RPH[0], RPH[1], un, flip=True, pose=dict(T.RPOSE['offer'], n=(5.6, 16.6)), expr='smug', look=0.5,
               prop_n=lambda L, h: T.phone(L, h, -1.9), **kw)


def r_hall_sneak(t, s, u):
    def draw(CH, v):
        L = Layer(v.wcam()); suitcase(L, 1090, 700, 1.0); CH.add(L)
        raisa_phone(CH, v, t, 13.0)
        tol(CH, v, t, 820 - 40 * sm(u / 2.0), 700, 13.5, flip=True, pose='shiver', expr='shock', m=0.0)
    big, v = sc(HALL, light_hall, 760, 400, 0.78, t, draw, motes=(450, 60, 800, 300))
    D.blit(big, v, TAG, 1090 - 18, 700 - 50)
    return big


def r_raisa_phone(t, s, u):
    return cu(HALL, light_hall, t, lambda CH, v, t_, x, y, un, **kw: raisa_phone(CH, v, t_, un), RPH[0], RPH[1], 14.0, k=1.25, head=20.5, dx=-40)


def r_zamuruem(t, s, u):
    big = r_tolik_coats(t, s, u, k=1.7)
    B.shake(big, t, 10, 40)
    return big


def r_suitcase_cu(t, s, u):
    def draw(CH, v):
        L = Layer(v.wcam()); suitcase(L, 1090, 700, 1.0); CH.add(L)
    big, v = sc(HALL, light_hall, 1090, 640, 1.42 + 0.05 * u, t, draw)
    D.blit(big, v, TAG, 1090 - 18, 700 - 50)
    return big


def r_tolik_coats(t, s, u, k=1.45, expr='shock'):
    return cu(HALL, light_hall, t, tol, 800, 700, 13.5, k=k, head=27.0, dx=-30, flip=True, pose='shiver', expr=expr)


def r_tolik_coats2(t, s, u):
    return r_tolik_coats(t, s, u, expr='angry')


def r_pusya_h(t, s, u):
    def draw(CH, v): pus(CH, v, t, 640, 700, 19.0, expr='smug')
    return sc(HALL, light_hall, 640, 610, 1.42, t, draw)[0]


# ======================================================================================= 3. 10:00 escape
def r_tolik_rod(t, s, u):
    def draw(CH, v):
        tol(CH, v, t, 900 + 60 * sm(u / 3), 700, 14.0, pose=dict(T.TPOSE['stand'], n=(3.6, 15.0)), expr='smug', gear=True, hat='knit',
            prop_n=rod)
        pus(CH, v, t, 640, 704, 8.5, m=0.0)
    return sc(HALL, light_hall, 840, 380, 0.85, t, draw, motes=(450, 60, 800, 300))[0]


BENCH = [(930.0, 640.0), (1050.0, 640.0)]                           # grannies on the bus-stop bench (world floor points)


def bench(CH, v, un=11.5):
    L = Layer(v.wcam()); sy = 640 - 6.4 * un
    F.poly(L, [(870, sy - 4), (1110, sy - 4), (1110, sy + 8), (870, sy + 8)], (150, 100, 60))
    for x in (885, 1095): F.cap(L, (x, sy + 8), (x, 645), 4, 4, (90, 70, 50))
    F.outline(L, OL); CH.add(L)


def grannies(CH, v, t, un=11.5, i_talk=None):
    bench(CH, v, un)
    for i, (x, y) in enumerate(BENCH):
        gran(CH, v, t, i, x, y, un, flip=True, pose='sit', expr='sweet' if i == 0 else 'stern', look=-0.7)


def r_sneak_yard(t, s, u):
    def draw(CH, v):
        grannies(CH, v, t)
        tol(CH, v, t, 260 + 120 * u / 2.0, 660, 12.5, pose=dict(T.TPOSE['stand'], n=(3.6, 15.0), nleg=(0.3, 0.0), fleg=(-0.3, 0.0)),
            expr='smug', gear=True, hat='knit', prop_n=rod, m=0.0)
    return sc(YARD, light_yard, 640, 420, 0.75, t, draw, snow=(0, 0, 1280, 720))[0]


def r_granny1(t, s, u):
    return cu(YARD, light_yard, t, lambda CH, v, t_, x, y, un, **kw: gran(CH, v, t_, 0, x, y, un, flip=True,
              pose=dict(T.RPOSE['sit'], n=(6.0, 15.0)), expr='sweet', look=-0.7), BENCH[0][0], BENCH[0][1], 11.5, k=1.4, head=20.5, dx=-20, pre=(lambda CH, v_: bench(CH, v_),))


def r_granny2(t, s, u):
    return cu(YARD, light_yard, t, lambda CH, v, t_, x, y, un, **kw: gran(CH, v, t_, 1, x, y, un, flip=True,
              pose=dict(T.RPOSE['sit'], n=(5.6, 15.6)), expr='stern', look=-0.5, prop_n=lambda L, h: T.phone(L, h, -1.9)),
              BENCH[1][0], BENCH[1][1], 11.5, k=1.4, head=20.5, dx=-20, pre=(lambda CH, v_: bench(CH, v_),))


def r_tolik_run(t, s, u):
    def draw(CH, v):
        tol(CH, v, t, 300 + 260 * u / 1.3, 660, 12.5, pose=dict(T.TPOSE['shock'], nleg=(0.5, 0.0), fleg=(-0.5, 0.0)), expr='scream',
            gear=True, hat='knit', m=0.6)
    big = sc(YARD, light_yard, 420 + 150 * u / 1.3, 420, 0.9, t, draw, snow=(0, 0, 1280, 720))[0]
    fx.speed_lines(big, t, 1.0)
    return big


def r_bus_arrive(t, s, u):
    bx = 680 + 600 * (1 - sm(u / 0.7))
    def draw(CH, v):
        tol(CH, v, t, 460, 660, 12.0, pose='shock', expr='shock', gear=True, hat='knit', m=0.6)
        L = Layer(v.wcam()); gazelle(L, bx, 705, 0.75); CH.add(L)
    big, v = sc(YARD, light_yard, 600, 400, 0.85, t, draw, snow=(0, 0, 1280, 720))
    if 0.6 < u < 1.0: B.shake(big, t, 6, 30)
    return big


def r_lyusya(t, s, u, expr='stern'):
    def draw(CH, v):
        lyu(CH, v, t, 240, 720, 17.0, pose=dict(T.RPOSE['sit'], n=(6.6, 17.4)), expr=expr, look=0.7)
        L = Layer(v.wcam()); wheel_ring(L); CH.add(L)
    return sc(MINI, light_mini, 280, 400, 1.3, t, draw)[0]


def r_lyusya2(t, s, u):
    return r_lyusya(t, s, u, expr='sweet')


def r_tolik_betray(t, s, u):
    return cu(YARD, light_yard, t, tol, 460, 660, 12.0, k=1.5, head=27.0, dx=40, pose='shock', expr='scream', gear=True, hat='knit')


def babki(CH, v, t):
    gran(CH, v, t, 1, 805, 600, 10.0, who='babki', flip=True, pose=dict(T.RPOSE['sit'], n=(4.6, 15.6 + 0.8 * math.sin(t * 11))), look=-0.6)
    gran(CH, v, t, 0, 935, 650, 12.5, who='babki', flip=True, pose=dict(T.RPOSE['sit'], n=(5.0, 16.0 - 0.8 * math.sin(t * 11))), look=-0.6)


def r_babki(t, s, u):
    return sc(MINI, light_mini, 880, 440, 1.2, t, lambda CH, v: babki(CH, v, t))[0]


def r_bus_ride(t, s, u):
    def draw(CH, v):
        babki(CH, v, t)
        tol(CH, v, t, 610, 724, 14.0, pose=dict(T.TPOSE['stand'], n=(3.0, 13.0)), expr='sad', hat='knit', gear=True, prop_n=rod, m=0.0,
            shake=0.03)
    big = sc(MINI, light_mini, 720 + 20 * math.sin(t * 2), 420, 0.95, t, draw)[0]
    B.shake(big, t, 3, 12)
    return big


def r_tolik_hat(t, s, u):
    return cu(MINI, light_mini, t, tol, 610, 724, 14.0, k=1.35, head=27.0, dx=20, pose=dict(T.TPOSE['stand'], n=(3.0, 13.0)),
              expr='sad', hat='knit', gear=True)


# ======================================================================================= 4. 17:00 recon
def r_spy_glass(t, s, u):
    """POV through the balcony door glass: Raisa with a tape measure, Lyusya with a plank, Sveta with a drill — half-built panels"""
    v = bview(640, 430, 0.82)
    def draw(CH, v_):
        sve(CH, v_, t, 430, 690, 12.0, pose=dict(T.SPOSE['keys'], n=(4.0, 15.0)), expr='tired', prop_n=drill)
        rai(CH, v_, t, 640, 690, 12.0, pose=dict(T.RPOSE['offer'], n=(6.0, 12.0)), expr='stern', prop_n=tape)
        lyu(CH, v_, t, 860, 690, 12.5, pose=dict(T.RPOSE['hold'], n=(4.0, 12.0)), prop_n=plank, flip=True)
    def after(big, v_):
        h, w = big.shape[:2]
        big[:, :140] = (big[:, :140] * 0.25).astype(np.uint8); big[:, w - 140:] = (big[:, w - 140:] * 0.25).astype(np.uint8)
        big[:90] = (big[:90] * 0.25).astype(np.uint8); big[h - 90:] = (big[h - 90:] * 0.25).astype(np.uint8)
        for i in range(4):                                                            # glass reflections
            x0 = 300 + i * 360 + int(30 * math.sin(t))
            for k in range(40): big[200 + k * 8:206 + k * 8, x0 + k * 4:x0 + k * 4 + 30] = np.minimum(255, big[200 + k * 8:206 + k * 8, x0 + k * 4:x0 + k * 4 + 30].astype(np.int16) + 30)
        B.puff(big, 960, 760, 200, 0.18 * (0.5 + 0.5 * math.sin(t * 2)))                 # breath fog
    return balc(v, t, draw, k=0.4, after=after)


def r_tolik_spy(t, s, u):
    return cu(HALL, light_hall, t, tol, 700, 700, 14.0, k=1.45, head=27.0, flip=True, pose='shiver', expr='angry')


def r_colander(t, s, u):
    c = sm(u / 0.6)
    def draw(CH, v):
        tol(CH, v, t, 700, 700, 14.0, flip=True, pose=dict(T.TPOSE['proud'], n=(3.6, 15.0)), expr='proud', colander=c, prop_n=mop, m=0.0)
        pus(CH, v, t, 560, 704, 8.5, m=0.0)
    return sc(HALL, light_hall, 660, 380, 0.85, t, draw, motes=(450, 60, 800, 300))[0]


def r_pusya_col(t, s, u):
    return r_pusya_h(t, s, u)


def r_tolik_farewell(t, s, u):
    return cu(HALL, light_hall, t, tol, 700, 700, 14.0, k=1.45, head=27.0, flip=True, pose=dict(T.TPOSE['proud'], n=(3.6, 15.0)),
              expr='proud', colander=1.0, prop_n=mop)


# ======================================================================================= 5. 17:30 storm — TWIST 1
TWX = 270.0


def family(CH, v, t, expr_r='sweet'):
    sve(CH, v, t, 430, 690, 12.0, flip=True, pose='stand', expr='guilty')
    rai(CH, v, t, 540, 690, 12.0, flip=True, pose='hips', expr=expr_r)
    lyu(CH, v, t, 640, 690, 12.5, flip=True, pose='stand')


def r_storm(t, s, u):
    """he bursts in with a mop and a colander: «Руки вверх! Мужика не замуруешь!»"""
    v = bview(330, 380, 1.15)
    def draw(CH, v_):
        tol(CH, v_, t, 200 + 120 * sm(u / 0.6), 700, 14.0, pose=dict(T.TPOSE['fists'], n=(3.6, 15.0)), expr='scream', colander=1.0,
            prop_n=mop)
    big = balc(v, t, draw, k=1.0)
    fx.speed_lines(big, t, 0.8)
    return big


def r_reveal(t, s, u):
    """freeze: the balcony is a cosy «КАБИНЕТ ТОЛИКА»: panels, carpet, heater, his armchair, a TV, garland; the family stands there"""
    v = bview(640 - 10 * sm(u / 4), 410, 0.62 + 0.04 * sm(u / 4))
    def draw(CH, v_):
        SH.chair(CH, v_, CHS, 'back', CHX, CHY); SH.chair(CH, v_, CHS, 'front', CHX, CHY)
        family(CH, v_, t)
        tol(CH, v_, t, TWX, 700, 12.5, pose=dict(T.TPOSE['fists'], n=(3.6, 15.0)), expr='shock', colander=1.0, prop_n=mop, m=0.4)
    big = balc(v, t, draw, k=1.0)
    if u < 0.15: O.flash(big, 0.7 * (1 - u / 0.15))
    return big


def r_raisa_gift(t, s, u):
    v = bview(560, 730 - 20.5 * 12 * 1.45 + 30, 1.42)
    return balc(v, t, lambda CH, v_: rai(CH, v_, t, 540, 730, 12.0 * 1.45, flip=True, pose='hips', expr='sweet', look=-0.4))


def r_sveta_surp(t, s, u):
    v = bview(440, 740 - 24 * 12 * 1.4 + 30, 1.42)
    return balc(v, t, lambda CH, v_: sve(CH, v_, t, 430, 740, 12.0 * 1.4, flip=True, pose='shrug', expr='guilty'))


def r_tolik_stun(t, s, u):
    c = 1.0 - sm((u - 0.3) / 0.6) * 0.0
    v = bview(TWX + 10, 740 - 27.2 * 12.5 * 1.45 + 30, 1.42)
    def draw(CH, v_):
        tol(CH, v_, t, TWX, 740, 12.5 * 1.45, pose='stand', expr='shock', colander=max(0.0, 1.0 - sm((u - 0.4) / 0.5) * 1.8))
    return balc(v, t, draw)


def r_lyusya_cement(t, s, u):
    v = bview(650, 735 - 20.5 * 12.5 * 1.45 + 30, 1.42)
    def draw(CH, v_):
        L = Layer(v_.wcam()); sack(L, 760, 735, 1.0); CH.add(L)
        lyu(CH, v_, t, 640, 735, 12.5 * 1.45, flip=True, pose='stand')
    big = balc(v, t, draw)
    D.blit(big, v, CEMENT, 760 - 23, 735 - 52)
    return big


def r_pusya_awk(t, s, u):
    v = bview(CHX, CHY - 120, 1.42)
    def draw(CH, v_):
        SH.chair(CH, v_, CHS, 'back', CHX, CHY)
        pus(CH, v_, t, CHX + 6, CHY - 64 * CHS + 2, 16.0)
        SH.chair(CH, v_, CHS, 'front', CHX, CHY)
    return balc(v, t, draw)


# ======================================================================================= 6. 18:30 «как мужик»
def r_tolik_drill(t, s, u):
    v = bview(560, 740 - 27.2 * 13 * 1.4 + 30, 1.42)
    return balc(v, t, lambda CH, v_: tol(CH, v_, t, 540, 740, 13 * 1.4, pose=dict(T.TPOSE['phone'], n=(4.6, 19.0)), expr='proud',
                                          prop_n=drill))


def r_sparks(t, s, u):
    v = bview(520, 400, 0.95)
    def draw(CH, v_):
        tol(CH, v_, t, 520, 700, 13.0, pose=dict(T.TPOSE['phone'], n=(4.6, 19.0)), expr='shock', prop_n=drill, shake=0.08, m=0.5)
    def after(big, v_):
        cx, cy = v_.opt(640, 450)
        rng = np.random.default_rng(int(t * 30))
        for i in range(30):
            a = rng.random() * 6.28; d = rng.random() * 160
            x, y = int(cx + math.cos(a) * d), int(cy + math.sin(a) * d * 0.6)
            if 0 <= x < OUT_W - 8 and 0 <= y < OUT_H - 8: big[y:y + 8, x:x + 8] = (255, 230, 120)
        if u > 1.6: big[:] = (big * 0.12).astype(np.uint8)
    big = balc(v, t, draw, after=after)
    if u < 1.6: B.shake(big, t, 6, 40)
    return big


def r_dark(t, s, u):
    """«Толечка, не трогай. Ты мужик — тебе нельзя.» — darkness, two pairs of eyes; then a candle lights Raisa's face"""
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8) + 8
    bl = (t % 2.1) < 0.12
    for (x, y) in ((760, 500), (1160, 460)):
        if not bl:
            for dx in (-40, 40):
                big[y - 14:y + 14, x + dx - 18:x + dx + 18] = (240, 240, 230)
                big[y - 6:y + 8, x + dx - 6:x + dx + 8] = (20, 20, 20)
    return big


def r_tolik_touched(t, s, u):
    v = bview(620, 740 - 27.2 * 13 * 1.4 + 30, 1.42)
    def draw(CH, v_):
        tol(CH, v_, t, 600, 740, 13 * 1.4, pose='stand', expr='sad')
    def after(big, v_):
        big[:] = (big * 0.55).astype(np.uint8)
        cx, cy = 1350, 820; fx.glow(big, cx, cy, 700, (255, 200, 110), 0.5)
        big[cy - 40:cy + 120, cx - 14:cx + 14] = (240, 236, 220)
        fl = int(8 * math.sin(t * 17))
        big[cy - 90 + fl:cy - 40, cx - 10:cx + 10] = (255, 200, 80)
    return balc(v, t, draw, after=after)


# ======================================================================================= 7. 20:00 party (room)
TABLE_Y = 560.0


def table(L, t, cake=True):
    F.poly(L, [(330, TABLE_Y), (930, TABLE_Y), (960, 700), (300, 700)], (240, 236, 226))
    for x in range(330, 930, 40): F.cap(L, (x, TABLE_Y + 4), (x - 10, 698), 1.2, 1.2, (220, 60, 70))
    for i, x in enumerate((380, 470, 560, 680, 790, 880)):
        F.ell(L, (x, TABLE_Y + 22), 26, 8, (244, 244, 236), 0, (255, 255, 255), (200, 204, 210))
        F.ell(L, (x, TABLE_Y + 18), 14, 5, [(240, 220, 150), (200, 70, 60), (150, 200, 90)][i % 3])
    for x in (430, 740):
        F.poly(L, [(x - 8, TABLE_Y + 12), (x + 8, TABLE_Y + 12), (x + 6, TABLE_Y - 30), (x - 6, TABLE_Y - 30)], (220, 120, 60))
    if cake:
        F.poly(L, [(590, TABLE_Y + 10), (670, TABLE_Y + 10), (670, TABLE_Y - 30), (590, TABLE_Y - 30)], (250, 214, 220))
        F.ell(L, (630, TABLE_Y - 30), 40, 9, (255, 236, 240))
        for k in range(6):
            x = 602 + k * 11
            F.cap(L, (x, TABLE_Y - 34), (x, TABLE_Y - 50), 1.5, 1.5, (120, 200, 255))
            F.ell(L, (x, TABLE_Y - 55 + math.sin(t * 15 + k)), 2.5, 4, (255, 210, 80))
    F.outline(L, OL)


def guests(CH, v, t, freeze=False):
    gran(CH, v, t, 0, 380, 640, 11.0, pose='stand', expr='sweet')
    gran(CH, v, t, 1, 470, 640, 11.0, pose='stand', expr='sweet')
    lyu(CH, v, t, 820, 640, 11.5, flip=True, pose='stand', expr='sweet')
    sve(CH, v, t, 900, 650, 11.5, flip=True, pose='stand', expr='smile')


def party(v, t, draw, cake=True, tv=1.0, osd=None, after=None):
    def d(CH, v_):
        L = Layer(v_.wcam()); SH.tv_big(L, 1150, 640, 1.2, t, osd=osd); CH.add(L)
        draw(CH, v_)
        L = Layer(v_.wcam()); table(L, t, cake); CH.add(L)
    def aft(big, v_):
        for i in range(18):                                                          # garland on the wall carpet
            x, y = v_.opt(480 + i * 22, 140 + 10 * math.sin(i * 0.9))
            c = [(255, 80, 90), (255, 220, 60), (90, 200, 255), (120, 230, 120)][(i + int(t * 3)) % 4]
            if 0 <= x < OUT_W - 12 and 0 <= y < OUT_H - 12: big[int(y):int(y) + 12, int(x):int(x) + 12] = c
        if after: after(big, v_)
    return SH.room(v, t, d, tv=tv, after=aft)


def rv(cx, cy, Z):
    return view_at(ROOM, cx, cy, Z, SX, SY)


def r_party_wide(t, s, u):
    def draw(CH, v):
        guests(CH, v, t)
        rai(CH, v, t, 300, 660, 12.0, pose='offer', expr='sweet')
        tol(CH, v, t, 630, 640, 12.0, pose='proud', expr='proud', party=True, bow=True, m=0.0)
        pus(CH, v, t, 980, 700, 7.5, hat=True, m=0.0)
    return party(rv(640 + 30 * sm(u / 3), 400, 0.72), t, draw)


def r_cake(t, s, u):
    return party(rv(630, TABLE_Y - 40, 1.42), t, lambda CH, v: None)


def r_raisa_plate(t, s, u):
    v = rv(320, 660 - 21 * 12 * 1.45 + 40, 1.42)
    return party(v, t, lambda CH, v_: rai(CH, v_, t, 300, 700, 12 * 1.45, pose='offer', expr='sweet', prop_n=lambda L, h: (
        F.ell(L, (h[0] + 1.2, h[1] - 0.3), 2.6, 0.8, (244, 244, 236)), F.ell(L, (h[0] + 1.2, h[1] - 0.8), 1.6, 0.6, (140, 80, 40)))), cake=False)


def r_karaoke(t, s, u):
    v = rv(800, 420, 1.1)
    def draw(CH, v_):
        gran(CH, v_, t, 0, 760, 680, 13.0, pose=dict(T.RPOSE['call'], n=(4.0, 18.6)), expr='shout', prop_n=mic)
    return party(v, t, draw, osd=100, cake=False)


def r_toast(t, s, u, expr='proud', loud=False):
    U = 12.0 * 1.45
    v = rv(640, 680 - 27.2 * U + 30, 1.42)
    def draw(CH, v_):
        tol(CH, v_, t, 630, 680, U, pose=dict(T.TPOSE['proud'], n=(4.2, 22.0)) if not loud else 'shock', expr=expr, party=True,
            bow=True, prop_n=glass)
    return party(v, t, draw, cake=False)


def r_toast2(t, s, u):
    return r_toast(t, s, u, expr='scream', loud=True)


def r_freeze(t, s, u):
    big = r_party_wide(t - u, s, 0.0)
    g = big.mean(2, keepdims=True)
    big[:] = (big * 0.5 + g * 0.5).astype(np.uint8)
    return big


def r_raisa_leaving(t, s, u):
    v = rv(320, 660 - 21 * 12 * 1.45 + 40, 1.42)
    return party(v, t, lambda CH, v_: rai(CH, v_, t, 300, 700, 12 * 1.45, pose='hold', expr='shock', look=0.5), cake=False)


def r_suitcase_reveal(t, s, u):
    big = r_suitcase_cu(t, s, u)
    if u < 0.12: O.flash(big, 0.6)
    return big


def r_sveta_said(t, s, u):
    v = rv(900, 650 - 27 * 11.5 * 1.5 * 0.9 + 60, 1.42)
    return party(v, t, lambda CH, v_: sve(CH, v_, t, 900, 690, 11.5 * 1.5, flip=True, pose='shrug', expr='smile'), cake=False)


def r_raisa_stay(t, s, u):
    big = party(rv(320, 660 - 21 * 12 * 1.45 + 40, 1.42), t,
                lambda CH, v_: rai(CH, v_, t, 300, 700, 12 * 1.45, pose='hips', expr='sweet'), cake=False)
    rng = np.random.default_rng(5)
    for i in range(70):
        x = int(rng.random() * OUT_W); y = int((rng.random() * OUT_H + u * 500) % OUT_H)
        big[y:y + 12, x:x + 12] = [(255, 80, 120), (255, 220, 60), (90, 200, 255), (120, 230, 120)][i % 4]
    return big


def r_lyusya_too(t, s, u):
    v = rv(820, 640 - 21 * 11.5 * 1.45 + 40, 1.42)
    def draw(CH, v_):
        cam, r = lyu(CH, v_, t, 820, 680, 11.5 * 1.45, flip=True, pose='offer', expr='sweet')
        wx, wy = u2w(v_, cam, r['hand_n'])
        L = Layer(v_.wcam()); T.chelnok(L, wx - 20, wy + 50, 80, 60, 0.15, 11); CH.add(L)
    return party(v, t, draw, cake=False)


def r_tolik_weak(t, s, u):
    return r_toast(t, s, u, expr='whine')


# ======================================================================================= 8. 23:00 the cabinet at night
def r_cab_pan(t, s, u):
    v = bview(560 + 160 * sm(u / 2.2), 420, 0.9)
    def draw(CH, v_):
        tol_chair(CH, v_, t, 12.5, expr='smug', m=0.0, prop_n=lambda L, h: SH.remote(L, h, -1.2))
    return balc(v, t, draw, after=lambda big, v_: night(big, 0.25))


def r_cab_alone(t, s, u):
    un = 12.5 * 1.35
    seat = CHY - 64 * CHS
    v = bview(CHX + 10, seat + 13.6 * un - 27 * un + 70, 1.42)
    return balc(v, t, lambda CH, v_: tol_chair(CH, v_, t, un, expr='proud', prop_n=lambda L, h: SH.remote(L, h, -1.2)))


def r_door_raisa(t, s, u):
    v = bview(260, 420, 1.15)
    def draw(CH, v_):
        rai(CH, v_, t, 180, 700, 14.0, pose=dict(T.RPOSE['offer'], n=(6.4, 16.0)), expr='sweet', prop_n=lambda L, h: (
            F.ell(L, (h[0] + 0.8, h[1] - 0.8), 1.5, 1.0, (196, 40, 52)), F.ell(L, (h[0] + 0.7, h[1] - 1.9), 0.6, 0.55, (246, 240, 230))))
    return balc(v, t, draw)


def r_pusya_chair(t, s, u):
    return r_pusya_awk(t, s, u)


def r_end(t, s, u):
    v = bview(620, 400, 0.78)
    def draw(CH, v_):
        SH.chair(CH, v_, CHS, 'back', CHX, CHY)
        pus(CH, v_, t, CHX + 6, CHY - 64 * CHS + 2, 9.0, m=0.0)
        SH.chair(CH, v_, CHS, 'front', CHX, CHY)
        rai(CH, v_, t, 220, 700, 12.5, pose='hips', expr='sweet')
        tol(CH, v_, t, 620, 700, 12.5, pose='stand', expr='whine', hat='knit', gear=True, m=0.0)
    return balc(v, t, draw)


# ======================================================================================= assembly
SHOT = dict(hook=r_hook, evidence=r_evidence, closet=r_closet, pusya_closet=r_pusya_closet, title=r_title,
            kitchen_wide=r_kitchen_wide, raisa_kasha=r_raisa_kasha, tolik_shirt=r_tolik_shirt, raisa_kasha2=r_raisa_kasha,
            sveta_wink=r_sveta_wink, tolik_sulk=r_tolik_sulk, pusya_k=r_pusya_k,
            hall_sneak=r_hall_sneak, raisa_phone=r_raisa_phone, zamuruem=r_zamuruem, raisa_phone2=r_raisa_phone, suitcase_cu=r_suitcase_cu,
            tolik_coats=r_tolik_coats, tolik_coats2=r_tolik_coats2, pusya_h=r_pusya_h,
            tolik_rod=r_tolik_rod, sneak_yard=r_sneak_yard, granny1=r_granny1, granny2=r_granny2, tolik_run=r_tolik_run,
            bus_arrive=r_bus_arrive, lyusya=r_lyusya, tolik_betray=r_tolik_betray, lyusya2=r_lyusya2, babki=r_babki, bus_ride=r_bus_ride,
            tolik_hat=r_tolik_hat,
            spy_glass=r_spy_glass, tolik_spy=r_tolik_spy, colander=r_colander, pusya_col=r_pusya_col, tolik_farewell=r_tolik_farewell,
            pusya_s4=r_pusya_col,
            storm=r_storm, reveal=r_reveal, raisa_gift=r_raisa_gift, sveta_surp=r_sveta_surp, tolik_stun=r_tolik_stun,
            lyusya_cement=r_lyusya_cement, pusya_awk=r_pusya_awk,
            tolik_drill=r_tolik_drill, sparks=r_sparks, dark=r_dark, tolik_touched=r_tolik_touched,
            party_wide=r_party_wide, cake=r_cake, raisa_plate=r_raisa_plate, karaoke=r_karaoke, toast=r_toast, toast2=r_toast2,
            freeze=r_freeze, raisa_leaving=r_raisa_leaving, suitcase_reveal=r_suitcase_reveal, sveta_said=r_sveta_said,
            raisa_stay=r_raisa_stay, lyusya_too=r_lyusya_too, tolik_weak=r_tolik_weak,
            cab_pan=r_cab_pan, cab_alone=r_cab_alone, door_raisa=r_door_raisa, pusya_chair=r_pusya_chair, end=r_end)
for nm in CARD: SHOT[nm] = r_card
for c in TL.CLIPS: SHOT[[s for s in TL.SHOTS if s.get('ep') == c['ep']][0]['name']] = r_fb

STICK = []


def stickers():
    if not STICK:
        def st(txt, fg, size, name, dt0, dt1, cx, cy):
            s = TL.first(name); STICK.append((O.sticker(txt, fg=fg, size=size), s['t0'] + dt0, s['t1'] + dt1, cx, cy))
        st('ЦЕМЕНТ', (220, 220, 214), 80, 'evidence', 0.1, -2.0, 1500, 300)
        st('РУЛЕТКА', (255, 220, 60), 80, 'evidence', 1.1, -1.0, 1500, 300)
        st('ЧЕМОДАН', (230, 150, 110), 80, 'evidence', 2.1, 0.0, 1500, 300)
        st('ЗАБЫЛИ?!', (255, 120, 150), 100, 'tolik_sulk', 0.2, 0.0, 1450, 260)
        st('ЗАМУРУЕМ?!', (255, 120, 150), 120, 'zamuruem', 0.0, 0.0, 960, 240)
        st('РАЯ. ДОМОЙ', (230, 150, 110), 70, 'suitcase_cu', 0.2, 0.0, 1450, 260)
        st('ЗВОНИ РАЕ!', (255, 222, 80), 90, 'granny2', 0.3, 0.0, 1400, 260)
        st('ДУРШЛАГ', (200, 210, 230), 80, 'pusya_col', 0.3, 0.0, 1450, 260)
        st('С ДНЁМ РОЖДЕНИЯ!', (255, 222, 80), 90, 'raisa_gift', 0.5, 0.0, 960, 200)
        st('42!', (255, 222, 80), 140, 'cake', 0.2, 0.0, 1450, 300)
        st('ГРОМКОСТЬ 100', (90, 255, 110), 70, 'karaoke', 0.3, 0.0, 1400, 240)
        st('НА ПРОЩАНИЕ?!', (255, 120, 150), 100, 'suitcase_reveal', 0.1, 0.0, 960, 240)
        st('НАВСЕГДА!', (255, 222, 80), 110, 'raisa_stay', 0.4, 0.0, 1400, 260)
    return STICK


NOCAP = ('title', 'evidence') + tuple(CARD) + tuple(s['name'] for s in TL.SHOTS if s['kind'] == 'flash')
NOHUD = ('title',) + tuple(CARD) + tuple(s['name'] for s in TL.SHOTS if s['kind'] == 'flash')
CLOCK = [('card_0700', '07:00'), ('card_0830', '08:30'), ('card_1000', '10:00'), ('card_1200', '17:00'), ('card_1300', '17:30'),
         ('card_1500', '18:30'), ('card_1900', '20:00'), ('card_2100', '23:00')]
MOSAIC_AT = ('kitchen_wide', 'hall_sneak', 'tolik_rod', 'spy_glass', 'storm', 'party_wide', 'cab_pan')
HOOK = [None]


def hud(big, t):
    O.overlay(big, img('badge', lambda: O.make_badge('ТЁЩА НА НЕДЕЛЬКУ • ЗАГОВОР', 26)), 34, 30, 1.0)
    cur = None
    for nm, tm in CLOCK:
        if TL.T0[nm] <= t: cur = tm
    if cur: O.overlay(big, img('clock' + cur, lambda: O.make_badge('ВРЕМЯ ' + cur, 26)), OUT_W - 260, 30, 1.0)


def render(t):
    s = TL.shot_at(t)
    u = t - s['t0']
    big = SHOT[s['name']](t, s, u)
    if s is TL.SHOTS[0]:
        if HOOK[0] is None: HOOK[0] = K.title_trim(K.hook_title(['ТЁЩА ГОТОВИТ', 'ЗАГОВОР?!'], 90, width=1500))
        if 0.06 <= t < 2.8:
            k = min(1.0, (t - 0.06) / 0.1) * (1 - sm((t - 2.6) / 0.2))
            O.overlay(big, HOOK[0], (OUT_W - HOOK[0].shape[1]) // 2, 60, k)
    for im, t0, t1, cx, cy in stickers(): O.draw_sticker(big, im, t, t0, t1, cx, cy)
    if s['name'] not in NOCAP: EPI.captions.draw(big, t, 960)
    if s['name'] not in NOHUD: hud(big, t)
    if s['name'] in MOSAIC_AT and u < 0.3: O.mosaic(big, int(lerp(40, 1, u / 0.3)))
    return big


CUTS, NAMES = TL.CUTS, TL.NAMES


def sheet(ids):
    tiles = []
    for x in ids:
        i = int(x)
        s = TL.SHOTS[i]; tm = (s['t0'] + s['t1']) / 2
        im = Image.fromarray(render(tm)).resize((480, 270), Image.LANCZOS)
        ImageDraw.Draw(im).text((6, 4), f'{NAMES[i]} {tm:.1f}', fill=(255, 255, 0))
        tiles.append(im)
    cols = 4; rows = (len(tiles) + cols - 1) // cols
    sh = Image.new('RGB', (480 * cols, 270 * rows))
    for k, im in enumerate(tiles): sh.paste(im, ((k % cols) * 480, (k // cols) * 270))
    out = P.build(BK, 'msheet.png'); sh.save(out); print(out)


if __name__ == '__main__':
    if sys.argv[1] == 'prep': prep()
    elif sys.argv[1] == 'sheet': sheet(sys.argv[2:])
    else: EPI.main(render, __file__)
