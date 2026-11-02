"""Shared scene helpers for «Тёща на недельку» episodes (E02+): worlds, lights, the armchair «КРЕСЛО ТОЛИКА», sitting Raisa,
the balcony camp bed, the kitchen, TV with the volume OSD, hand props. Call init(EPI) once in the episode script.
Coordinates are native px of series/teshcha/bg/*.png."""
import math
import numpy as np
import stage as ST
from stage import view_at
from scene import Layer, sm, lerp
import fx
from props import folk as F
from props import bytfx as B
from props import decals as D
from props import rusigns as R
from props import teshcast as T
from props import teshkit as K

TALK = [None]
W = K.build()
LAND, ROOM, BALC = W['landing'], W['room'], W['balcony']
EXTRA = {}
CHAIR = (600.0, 650.0)
CHAIR_TAG = R.plate(72, 20, ['КРЕСЛО ТОЛИКА'], bg=(236, 210, 130), colors=[(60, 30, 20)], border=(90, 60, 30), pad=1.0)
SITB = dict(T.TPOSE['sit'], nleg=(1.45, -0.55), fleg=(1.35, -0.5))


def init(epi, day=1):
    TALK[0] = epi.talk
    K.decorate(W, day=day)


def world(name):
    """extra xAI worlds (kitchen, hallway, yard, office, minibus) quantized to the series palette, cached"""
    if name not in EXTRA:
        from PIL import Image
        EXTRA[name] = K.q(Image.open(K.BG / f'{name}.png').convert('RGB'))
    return EXTRA[name]


def mouth(who, t, k=1.7):
    return min(1.0, TALK[0](who, t) * k)


def u2w(v, cam, pt):
    x, y = cam.p(*pt)
    k = ST.PX[0]
    return v.X0 + x * k / v.Z, v.Y0 + (y * k - v.oy) / v.Z


def face(v, cam, r, r_units=3.0):
    K.logface(v, cam, r['head'], r_units)


# ---------------------------------------------------------------- rooms
def room(v, t, draw=None, tv=0.0, prints=0, px0=800.0, py0=690.0, big_prints=1.0, after=None):
    CH, FX = K.begin()
    big = v.bg()
    if prints:
        L = Layer(v.wcam())
        for i in range(prints):
            g = big_prints
            px, py = px0 - 60 * g - i * 52 * g, py0 + (i % 2) * 14 * g
            F.ell(L, (px, py), 16 * g, 6 * g, (78, 52, 32)); F.ell(L, (px + 18 * g, py), 5 * g, 4 * g, (78, 52, 32))
        CH.add(L)
    if draw: draw(CH, v)
    CH.comp(big, K.light_room(v, tv))
    if tv > 0:
        fx.glow(big, *v.opt(*K.R_TV), 260, (120, 170, 255), 0.18 * tv * (0.8 + 0.2 * math.sin(t * 13)))
    fx.motes(FX, v, t, 760, 120, 1000, 420, n=18, col=(255, 226, 170), seed=5)
    FX.comp(big)
    if after: after(big, v)
    fx.vignette(big, 0.26)
    return big


def generic(world_img, v, t, draw=None, light=None, motes=None, snow=None, after=None, vign=0.28):
    """any extra world: hero light (stage.Light), optional motes box, optional snow box"""
    CH, FX = K.begin()
    big = v.bg()
    if draw: draw(CH, v)
    CH.comp(big, light)
    if motes: fx.motes(FX, v, t, *motes, n=20, col=(255, 236, 190), seed=7)
    if snow: B.falling_snow(FX, v, t, *snow, n=60, speed=50)
    FX.comp(big)
    if after: after(big, v)
    fx.vignette(big, vign)
    return big


def chair(CH, v, s, part, x=None, y=None):
    x = CHAIR[0] if x is None else x; y = CHAIR[1] if y is None else y
    L = Layer(v.wcam()); T.armchair(L, x, y, s, part)
    if part == 'back': K.decal_layer(L, v, CHAIR_TAG, x - 18 * s - 36, y - 236 * s + 14 * s)
    CH.add(L)


def raisa_sit(CH, v, t, s=0.65, unit=12.0, drop=0.0, x=None, **kw):
    seat = CHAIR[1] - 64 * s
    xx = (CHAIR[0] if x is None else x) + 6
    cam = v.cam(xx, seat + 6.4 * unit - drop, unit)
    kw.setdefault('expr', 'sweet')
    kw.setdefault('pose', T.RPOSE['sit'])
    pose = kw.pop('pose')
    r = T.raisa(CH, cam, pose, t=t, mouth_=mouth('raisa', t), **kw)
    face(v, cam, r, 3.6)
    return cam, r


def balcony(v, t, draw=None, snow=70):
    CH, FX = K.begin()
    big = v.bg()
    if draw: draw(CH, v)
    CH.comp(big, K.light_balcony(v))
    B.falling_snow(FX, v, t, 280, 100, 960, 470, n=snow, speed=60)
    B.snow_in(FX, v, t, (300, 150, 900, 300), n=30, drift=(-120, 260))
    FX.comp(big)
    fx.vignette(big, 0.34)
    return big


def tolik_bed(CH, v, t, k=1.0, expr='cold', m=None, shake=0.07, pillow=False, **kw):
    L = Layer(v.wcam()); T.campbed(L, K.B_BED[0], K.B_BED[1], 240, 1.6); CH.add(L)
    un = 11.0 * k
    seat = K.B_BED[1] - 58
    cam = v.cam(K.B_BED[0] + 10, seat + 13.6 * un, un, flip=True)
    hn = kw.pop('hand_n', F.H(3.4, 16.4)); hf = kw.pop('hand_f', F.H(2.8, 16.8))
    r = T.tolik(CH, cam, SITB, t=t, mouth_=mouth('tolik', t) if m is None else m, expr=expr, hat='knit', blanket=True, cold=0.35,
                shake=shake, hand_n=hn, hand_f=hf, **kw)
    if pillow:                                                   # pillow pressed to the side of the head
        P = Layer(cam)
        F.ell(P, F.H(-1.6, 27.0), 2.4, 1.8, (236, 236, 246), 0.3, (255, 255, 255), (196, 200, 220))
        F.outline(P, T.OL); CH.add(P)
    face(v, cam, r)
    return cam, r


def tolik_cu_balcony(t, u, m=None, expr='shout', k=1.55, pillow=False, shake=0.05, **kw):
    un = 11.0 * k
    seat = K.B_BED[1] - 58
    fx_, fy_ = K.B_BED[0] + 10 - 2.0 * un, seat + 13.6 * un - 27.0 * un
    v = view_at(BALC, fx_, fy_, 1.42, 180, 300)

    def draw(CH, v_):
        L = Layer(v_.wcam()); T.campbed(L, K.B_BED[0], K.B_BED[1], 240, 1.6); CH.add(L)
        cam = v_.cam(K.B_BED[0] + 10, seat + 13.6 * un, un, flip=True)
        mm = mouth('tolik', t) if m is None else m
        hn = kw.get('hand_n', F.H(3.4, 16.4)); hf = kw.get('hand_f', F.H(-1.0, 29.6) if pillow else F.H(2.8, 16.8))
        r = T.tolik(CH, cam, SITB, t=t, mouth_=mm, expr=expr, hat='knit', blanket=True, cold=0.35, shake=shake, hand_n=hn, hand_f=hf)
        if pillow:                                                   # big pillow pressed over the head and the ear
            P = Layer(cam)
            F.ell(P, F.H(-2.1, 29.0), 3.3, 2.2, (236, 236, 246), -0.5, (255, 255, 255), (196, 200, 220))
            for k_ in range(3): F.cap(P, F.H(-3.8 + k_ * 1.0, 27.8 + k_ * 0.8), F.H(-3.1 + k_ * 1.0, 28.4 + k_ * 0.8), 0.12, 0.12, (200, 204, 222))
            F.outline(P, T.OL); CH.add(P)
        face(v_, cam, r)
    return balcony(v, t, draw, snow=50)


# ---------------------------------------------------------------- props
def tv_big(L, x, y, s, t, osd=None, glow=1.0):
    """box TV on a little stand at floor point (x, y): soap opera on screen (two pixel faces) + optional volume OSD level 0..100"""
    A = Layer(L.cam)
    F.poly(A, [(x - 40 * s, y), (x + 40 * s, y), (x + 36 * s, y - 30 * s), (x - 36 * s, y - 30 * s)], (96, 60, 40))   # stand
    F.poly(A, [(x - 52 * s, y - 30 * s), (x + 52 * s, y - 30 * s), (x + 52 * s, y - 108 * s), (x - 52 * s, y - 108 * s)], (110, 74, 48))
    sx0, sy0, sx1, sy1 = x - 44 * s, y - 100 * s, x + 26 * s, y - 38 * s
    F.poly(A, [(sx0, sy0), (sx1, sy0), (sx1, sy1), (sx0, sy1)], (70, 110, 160))
    fl = 0.5 + 0.5 * math.sin(t * 2.3)
    F.ell(A, (sx0 + 20 * s, sy1 - 18 * s), 9 * s, 11 * s, (238, 196, 160)); F.ell(A, (sx0 + 20 * s, sy1 - 28 * s), 10 * s, 6 * s, (90, 50, 30))
    F.ell(A, (sx1 - 20 * s, sy1 - 18 * s + 2 * fl), 9 * s, 11 * s, (238, 196, 160)); F.ell(A, (sx1 - 20 * s, sy1 - 30 * s), 11 * s, 5 * s, (220, 180, 80))
    for k in range(3): F.ell(A, (x + 40 * s, y - (92 - k * 18) * s), 4 * s, 4 * s, (200, 190, 170))
    F.cap(A, (x - 12 * s, y - 108 * s), (x - 30 * s, y - 140 * s), 1.4, 1.4, (170, 170, 176))
    F.cap(A, (x + 8 * s, y - 108 * s), (x + 26 * s, y - 142 * s), 1.4, 1.4, (170, 170, 176))
    if osd is not None:                                           # green volume OSD
        F.poly(A, [(sx0 + 4 * s, sy0 + 4 * s), (sx1 - 4 * s, sy0 + 4 * s), (sx1 - 4 * s, sy0 + 16 * s), (sx0 + 4 * s, sy0 + 16 * s)], (10, 30, 14))
        n = int(round(osd / 10))
        for k in range(10):
            c = (90, 255, 110) if k < n else (30, 70, 40)
            F.poly(A, [(sx0 + (8 + k * 5) * s, sy0 + 7 * s), (sx0 + (11 + k * 5) * s, sy0 + 7 * s), (sx0 + (11 + k * 5) * s, sy0 + 13 * s),
                       (sx0 + (8 + k * 5) * s, sy0 + 13 * s)], c)
    F.outline(A, T.OL)
    L.col[A.m] = A.col[A.m]; L.m |= A.m
    return (sx0, sy0, sx1, sy1)


def remote(L, h, ang=-1.2):
    d = (math.cos(ang), math.sin(ang))
    a = (h[0] - d[0] * 0.3, h[1] - d[1] * 0.3); b = (h[0] + d[0] * 2.0, h[1] + d[1] * 2.0)
    F.cap(L, a, b, 0.45, 0.42, (40, 40, 46))
    for k in range(3):
        p = (a[0] + (b[0] - a[0]) * (0.35 + k * 0.2), a[1] + (b[1] - a[1]) * (0.35 + k * 0.2))
        F.dot(L, p, (220, 60, 60) if k == 0 else (200, 200, 210), 0.16)


def headphones(L, cam, head_c, r=3.4):
    """big old headphones over Raisa's curlers: band over the top, two cups at the ears (unit coords of her head cam)"""
    hx, hy = head_c
    F.cap(L, (hx - r * 0.9, hy - r * 0.2), (hx - r * 0.2, hy - r * 1.35), 0.45, 0.45, (40, 40, 48))
    F.cap(L, (hx - r * 0.2, hy - r * 1.35), (hx + r * 0.7, hy - r * 1.1), 0.45, 0.45, (40, 40, 48))
    F.ell(L, (hx - r * 0.95, hy + r * 0.05), r * 0.38, r * 0.5, (220, 40, 60), 0, (250, 100, 110), (150, 20, 40))
