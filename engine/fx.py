"""Particles and frame effects that glue code heroes into painted (xAI) backgrounds.
Particle layers are drawn on a stage.Chars canvas (composited WITHOUT hero lighting, i.e. emissive).
Frame effects work on the 1080x1920 output image."""
import math
import numpy as np
import scene as S
from scene import Layer, cap, dot
from stage import ell, OUT_W, OUT_H, UP

_R = np.random.default_rng(7)
SEEDS = _R.random((400, 4))


# ---------------------------------------------------------------- particles (world coords)
def embers(FX, v, x, y, t, n=26, h=160, spread=22, col=((255, 210, 90), (255, 140, 40), (230, 80, 30))):
    """sparks rising from a fire at world (x,y)"""
    L = Layer(v.wcam())
    for i in range(n):
        a, b, c, d = SEEDS[i]
        life = 1.2 + 1.3 * a
        u = ((t + d * 7) % life) / life
        px = x + (b - 0.5) * spread + math.sin(t * (2 + 3 * c) + i) * 10 * u
        py = y - u * h * (0.6 + 0.6 * c)
        if u < 0.92: dot(L, (px, py), col[i % 3], 1.1 * (1 - u) + 0.5)
    FX.add(L)


def flames(FX, v, x, y, t, w=30, h=44):
    """animated pixel flames over a baked campfire"""
    L = Layer(v.wcam())
    for i, (cc, s) in enumerate((((230, 70, 20), 1.0), ((255, 150, 40), 0.72), ((255, 230, 120), 0.42))):
        for j in range(5):
            ph = t * (9 + j) + j * 1.7 + i
            fx = x + (j - 2) * w * 0.18 * s + math.sin(ph) * 2.5
            fh = h * s * (0.6 + 0.4 * abs(math.sin(ph * 0.7 + j))) * (1.0 if j in (1, 2, 3) else 0.6)
            cap(L, (fx, y), (fx + math.sin(ph * 1.3) * 3, y - fh), w * 0.14 * s, 1.0, cc)
    FX.add(L)


def motes(FX, v, t, x0, y0, x1, y1, n=60, col=(255, 236, 170), speed=(6, 16), seed=0):
    """floating dust in light"""
    L = Layer(v.wcam())
    for i in range(n):
        a, b, c, d = SEEDS[(i + seed) % len(SEEDS)]
        x = x0 + ((a * (x1 - x0) + t * (speed[0] + speed[1] * c)) % (x1 - x0))
        y = y0 + ((b * (y1 - y0) + 5 * math.sin(t * 0.8 + i)) % (y1 - y0))
        if (i + int(t * 3 + d * 10)) % 5: dot(L, (x, y), col, 0.6 + 0.7 * c)
    FX.add(L)


def fireflies(FX, v, t, x0, y0, x1, y1, n=14):
    L = Layer(v.wcam())
    for i in range(n):
        a, b, c, d = SEEDS[100 + i]
        x = x0 + a * (x1 - x0) + 18 * math.sin(t * (0.6 + c) + i)
        y = y0 + b * (y1 - y0) + 10 * math.sin(t * (0.9 + d) + 2 * i)
        k = 0.5 + 0.5 * math.sin(t * 3 + i * 1.3)
        if k > 0.35: dot(L, (x, y), (220, 255, 140), 0.7 + 0.8 * k)
    FX.add(L)


def dust_puffs(FX, v, t, events, col=(226, 196, 150)):
    """events: list of (t0, x, y, size) -> expanding fading dust clouds"""
    L = Layer(v.wcam())
    for (t0, x, y, s) in events:
        u = t - t0
        if not (0 <= u < 0.7): continue
        for j in range(6):
            a, b, c, d = SEEDS[200 + (j + int(t0 * 10)) % 150]
            r = s * (0.4 + 1.2 * u) * (0.6 + 0.6 * c)
            ox = (a - 0.5) * s * 2.2 * (0.3 + u); oy = -b * s * 0.8 * u
            if u < 0.55 or (j % 2 == 0): ell(L, (x + ox, y + oy - r * 0.4), r, r * 0.75, col)
    FX.add(L)


def gallop_dust(t, x_of_t, y, t0, t1, rate=7, size=9):
    return [(tt, x_of_t(tt), y, size) for tt in np.arange(t0, t1, 1.0 / rate)]


# ---------------------------------------------------------------- frame effects (output px)
_VIG = None

def vignette(big, a=0.35):
    global _VIG
    if _VIG is None:
        yy, xx = np.mgrid[0:OUT_H, 0:OUT_W].astype(np.float32)
        d = ((xx - OUT_W / 2) / (OUT_W * 0.62)) ** 2 + ((yy - OUT_H / 2) / (OUT_H * 0.66)) ** 2
        _VIG = np.floor(np.clip(d - 0.35, 0, 1) * 6) / 6                  # stepped
    big[:] = (big * (1 - a * _VIG[..., None])).astype(np.uint8)


def grade(big, mult=(1, 1, 1), lift=(0, 0, 0)):
    big[:] = np.clip(big * np.array(mult, np.float32) + np.array(lift, np.float32), 0, 255).astype(np.uint8)


def glow(big, cx, cy, r, col, a):
    """additive round light pool (output px), stepped for pixel look"""
    Hh, Ww = big.shape[:2]
    x0, x1 = int(max(0, cx - r)), int(min(Ww, cx + r)); y0, y1 = int(max(0, cy - r)), int(min(Hh, cy + r))
    if x0 >= x1 or y0 >= y1 or a <= 0: return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    f = np.clip(1 - np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) / r, 0, 1) ** 1.6
    f = np.floor(f * 6) / 6
    reg = big[y0:y1, x0:x1].astype(np.float32)
    big[y0:y1, x0:x1] = np.clip(reg + f[..., None] * np.array(col, np.float32) * a, 0, 255).astype(np.uint8)


def shafts(big, t, angle=0.55, a=0.10, col=(255, 230, 170), width=90, gap=260, x_off=0):
    """animated diagonal god-rays across the frame (additive, stepped)"""
    yy, xx = np.mgrid[0:OUT_H:4, 0:OUT_W:4].astype(np.float32)
    u = xx * math.cos(angle) + yy * math.sin(angle) + x_off + t * 25
    band = (np.sin(u / gap * 2 * math.pi) * 0.5 + 0.5) ** 6
    band *= np.clip(1 - yy / OUT_H * 1.1, 0, 1)
    band = np.floor(band * 4) / 4
    m = np.repeat(np.repeat(band, 4, 0), 4, 1)[:OUT_H, :OUT_W]
    big[:] = np.clip(big + m[..., None] * np.array(col, np.float32) * a, 0, 255).astype(np.uint8)


def speed_lines(big, t, k=1.0, y0=0, y1=OUT_H):
    r = np.random.default_rng(int(t * 30))
    for i in range(int(18 * k)):
        y = int(r.integers(y0, y1)); x = int(r.integers(-300, OUT_W)); ln = int(r.integers(120, 380))
        big[y:y + 4, max(0, x):max(0, min(OUT_W, x + ln))] = (255, 246, 220)


def flash_burst(big, cx, cy, k):
    """camera-flash burst: white radial + global lift"""
    if k <= 0: return
    glow(big, cx, cy, 700, (255, 255, 255), 1.4 * k)
    big[:] = np.clip(big.astype(np.float32) * (1 - 0.5 * k) + 255 * 0.5 * k, 0, 255).astype(np.uint8)
