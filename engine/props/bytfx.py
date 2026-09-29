"""Everyday-life props and effects for «Валера и кот»: shower spray, snow blowing through a window pane, a water jet,
steam puffs (alpha on the output frame), heat haze over a radiator, and hand props (basin, ladle, screwdriver, phone...).
Particles are drawn in world coords on a stage.Chars canvas (emissive, no hero light)."""
import math
import numpy as np
import scene as S
from scene import Layer
from stage import OUT_W, OUT_H
from props.folk import cap, ell, poly, dot, outline

_R = np.random.default_rng(11)
SEED = _R.random((600, 5))


# ---------------------------------------------------------------- particles (world coords)
def spray(FX, v, t, src, spread=70, drop=330, n=70, col=(200, 230, 255), col2=(150, 196, 236), speed=2.2):
    """shower spray: streaks from src fanning down over `drop` world px"""
    L = Layer(v.wcam())
    for i in range(n):
        a, b, c, d, e = SEED[i]
        u = (t * speed + a) % 1.0
        ang = (b - 0.5) * 0.9
        x = src[0] + math.sin(ang) * drop * u + (c - 0.5) * 6
        y = src[1] + 8 + drop * u * (0.85 + 0.3 * d)
        ln = 10 + 10 * e
        cap(L, (x, y), (x + math.sin(ang) * ln * 0.3, y - ln), 0.9, 0.6, col if i % 3 else col2)
    FX.add(L)


def snow_in(FX, v, t, box, n=40, drift=(-60, 160), col=(236, 244, 255)):
    """snowflakes blowing in through an open pane box=(x0,y0,x1,y1): drift left+down, fading out"""
    L = Layer(v.wcam())
    x0, y0, x1, y1 = box
    for i in range(n):
        a, b, c, d, e = SEED[100 + i]
        life = 2.2 + 1.5 * c
        u = ((t + d * 9) % life) / life
        x = x0 + a * (x1 - x0) + drift[0] * u * (0.6 + 0.8 * e) + 10 * math.sin(t * 2 + i)
        y = y0 + b * (y1 - y0) + drift[1] * u * (0.7 + 0.6 * e)
        if u < 0.9: dot(L, (x, y), col, 1.2 + 1.0 * c)
    FX.add(L)


def falling_snow(FX, v, t, x0, y0, x1, y1, n=60, col=(236, 244, 255), speed=40):
    L = Layer(v.wcam())
    k = 1.0 / max(1.0, v.Z * 0.7)                         # flakes keep a sane on-screen size in close-ups
    for i in range(n):
        a, b, c, d, e = SEED[200 + i % 300]
        x = x0 + (a * (x1 - x0) + 14 * math.sin(t * (0.8 + c) + i)) % (x1 - x0)
        y = y0 + (b * (y1 - y0) + t * speed * k * (0.6 + 0.8 * d)) % (y1 - y0)
        dot(L, (x, y), col, (0.9 + 1.2 * e) * k)
    FX.add(L)


def jet(FX, v, t, t0, p0, p1, arc=40, col=(150, 78, 36), col2=(196, 112, 52), width=5.0, grow=0.25):
    """arcing water jet from p0 to p1 (world), grows over `grow` s after t0; droplets splash at p1"""
    if t < t0: return
    k = min(1.0, (t - t0) / grow)
    L = Layer(v.wcam())
    pts = []
    for i in range(13):
        s = i / 12 * k
        x = p0[0] + (p1[0] - p0[0]) * s + 2.0 * math.sin(t * 30 + i)
        y = p0[1] + (p1[1] - p0[1]) * s - arc * math.sin(math.pi * s)
        pts.append((x, y))
    for i in range(12):
        cap(L, pts[i], pts[i + 1], width * (1 - 0.3 * i / 12), width * (1 - 0.3 * (i + 1) / 12), col if (i + int(t * 20)) % 3 else col2)
    if k >= 1:
        for i in range(14):
            a, b, c, d, e = SEED[300 + i]
            u = ((t * 3 + a) % 1.0)
            ang = -math.pi / 2 + (b - 0.5) * 2.4
            x = p1[0] + math.cos(ang) * 30 * u; y = p1[1] + math.sin(ang) * 26 * u + 40 * u * u
            dot(L, (x, y), col2 if i % 2 else col, 1.6 * (1 - u) + 0.6)
    FX.add(L)


# ---------------------------------------------------------------- output-frame effects
def puff(big, cx, cy, r, a, col=(240, 244, 250)):
    """soft stepped white puff blended onto the output frame (steam, breath, dust)"""
    x0, x1 = int(max(0, cx - r)), int(min(OUT_W, cx + r)); y0, y1 = int(max(0, cy - r)), int(min(OUT_H, cy + r))
    if x0 >= x1 or y0 >= y1 or a <= 0: return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    f = np.clip(1 - np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r, 0, 1)
    f = np.floor(f * 4) / 4 * a
    # pixelate the mask in 6px cells for the pixel look
    f = f[::6, ::6].repeat(6, 0).repeat(6, 1)[:y1 - y0, :x1 - x0]
    reg = big[y0:y1, x0:x1].astype(np.float32)
    big[y0:y1, x0:x1] = np.clip(reg * (1 - f[..., None]) + np.array(col, np.float32) * f[..., None], 0, 255).astype(np.uint8)


def steam(big, v, t, x, y, t0=-99.0, t1=1e9, n=6, rise=160, size=46, a=0.55, seed=0):
    """rising steam column from world (x, y) active in [t0, t1)"""
    if t < t0: return
    fade = 1.0 if t < t1 else max(0.0, 1 - (t - t1) / 0.8)
    for i in range(n):
        a_, b, c, d, e = SEED[400 + (i + seed) % 150]
        life = 1.4 + 0.8 * c
        u = ((t - t0 + d * life) % life) / life
        wx = x + (a_ - 0.5) * 30 + 22 * math.sin(t * 1.5 + i) * u
        wy = y - rise * u
        ox, oy = v.opt(wx, wy)
        puff(big, ox, oy, size * v.Z * 3 * (0.5 + 0.9 * u), a * fade * (1 - u) * min(1.0, (t - t0) / 0.3))


def haze(big, v, t, box, amp=6, a=1.0):
    """heat shimmer over a radiator: shift pixel rows inside the (world) box horizontally with a moving sine"""
    x0, y0 = v.opt(box[0], box[1]); x1, y1 = v.opt(box[2], box[3])
    x0, x1 = int(max(0, x0)), int(min(OUT_W, x1)); y0, y1 = int(max(0, y0)), int(min(OUT_H, y1))
    if x1 - x0 < 8 or y1 - y0 < 8: return
    reg = big[y0:y1, x0:x1].copy()
    for yy in range(0, y1 - y0, 6):
        k = (1 - yy / max(1, y1 - y0)) * a
        s = int(round(amp * k * math.sin(t * 7 + yy * 0.05) / 6)) * 6
        if s: big[y0 + yy:y0 + yy + 6, x0:x1] = np.roll(reg[yy:yy + 6], s, 1)


def shake(big, t, amp=10, freq=31.0):
    dx = int(amp * math.sin(t * freq)); dy = int(amp * 0.6 * math.sin(t * freq * 1.3 + 1))
    big[:] = np.roll(np.roll(big, dy, 0), dx, 1)


# ---------------------------------------------------------------- hand props (callables for folk.valera prop_n/prop_f)
def basin(L, c, fill=None, steam_t=None, scale=1.0, tilt=0.0):
    """galvanized oval basin (тазик) centred at c (unit coords of the layer), fill = water colour or None"""
    k = scale
    ell(L, c, 4.6 * k, 1.6 * k, (150, 158, 166), tilt, (196, 204, 212), (112, 118, 126))
    ell(L, (c[0], c[1] + 1.1 * k), 4.0 * k, 1.8 * k, (136, 144, 152), tilt, (176, 184, 192), (104, 110, 118))
    ell(L, (c[0], c[1] - 0.2 * k), 3.9 * k, 1.1 * k, fill or (92, 98, 106), tilt)
    if fill: ell(L, (c[0] - 1.0 * k, c[1] - 0.4 * k), 1.2 * k, 0.3 * k, tuple(min(255, int(x * 1.3)) for x in fill), tilt)
    for sx in (-1, 1):
        cap(L, (c[0] + sx * 4.6 * k, c[1] - 0.2 * k), (c[0] + sx * 5.4 * k, c[1] + 0.3 * k), 0.35 * k, 0.35 * k, (120, 126, 134))


def ladle(L, hand, fill=None):
    cap(L, hand, (hand[0] + 2.6, hand[1] - 0.8), 0.28, 0.28, (170, 176, 184))
    ell(L, (hand[0] + 3.6, hand[1] - 0.6), 1.3, 0.9, (150, 158, 166), 0, (196, 204, 212), (112, 118, 126))
    if fill: ell(L, (hand[0] + 3.6, hand[1] - 0.95), 1.0, 0.35, fill)


def screwdriver(L, hand, ang=-0.6):
    d = (math.cos(ang), math.sin(ang))
    cap(L, hand, (hand[0] + d[0] * 1.6, hand[1] + d[1] * 1.6), 0.55, 0.5, (200, 60, 50), None, (150, 40, 34))
    cap(L, (hand[0] + d[0] * 1.6, hand[1] + d[1] * 1.6), (hand[0] + d[0] * 3.6, hand[1] + d[1] * 3.6), 0.16, 0.14, (190, 196, 204))


def phone_handset(L, hand):
    cap(L, (hand[0] - 0.4, hand[1] - 1.6), (hand[0] + 0.4, hand[1] + 1.6), 0.55, 0.55, (40, 40, 44), None, (24, 24, 28))
    ell(L, (hand[0] - 0.5, hand[1] - 1.9), 0.7, 0.5, (40, 40, 44)); ell(L, (hand[0] + 0.5, hand[1] + 1.9), 0.7, 0.5, (40, 40, 44))


def sausage(L, hand, ang=0.2):
    d = (math.cos(ang), math.sin(ang))
    cap(L, (hand[0] - d[0] * 2.6, hand[1] - d[1] * 2.6), (hand[0] + d[0] * 2.6, hand[1] + d[1] * 2.6), 0.95, 0.95,
        (214, 128, 120), (236, 160, 150), (180, 100, 96))
    for s in (-1, 1): dot(L, (hand[0] + s * d[0] * 3.4, hand[1] + s * d[1] * 3.4), (170, 150, 110), 0.35)


def flashlight(L, hand, ang=0.0):
    d = (math.cos(ang), math.sin(ang))
    cap(L, hand, (hand[0] + d[0] * 2.4, hand[1] + d[1] * 2.4), 0.45, 0.55, (70, 70, 76), None, (44, 44, 50))
    ell(L, (hand[0] + d[0] * 2.6, hand[1] + d[1] * 2.6), 0.45, 0.6, (255, 244, 190), ang)
