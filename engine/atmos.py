"""Atmosphere for 2.5D shots (owner rules 11–12.11.2026: more particles, volume, light, juicier colour; both channels).
Everything works on the finished output frame (1080x1920 RGB uint8) in output px; seeds are fixed, so particles do not boil.

  juice(big, sat=1.22, con=1.07)                  final grade: saturation + gentle S-curve contrast (owner: «сочнее»)
  motes(big, t, box, n, col, seed, depth=3, drift)  floating dust / pollen in a light beam, 3 depth layers (far tiny, near big soft)
  bokeh(big, t, n, cols, box, seed)               out-of-focus light discs (neon, street lamps) in the far background
  sparks(big, x, y, t, t0, n, col, seed)          a burst of falling sparks (neon tube, metal hit)
  flare(big, x, y, k, col)                        sunset lens flare: ghosts along the line to the frame centre
  screen(big, add)                                additive «screen» blend of an RGB float layer"""
import math
import numpy as np
from PIL import Image, ImageFilter

H_, W_ = 1920, 1080


def screen(big, add):
    add = np.clip(add, 0, 255)
    big[:] = (255 - (255 - big.astype(np.float32)) * (255 - add) / 255).astype(np.uint8)
    return big


def juice(big, sat=1.22, con=1.07, warm=0.0):
    """saturation boost around the luma + soft S-curve; warm > 0 nudges toward sunset orange"""
    f = big.astype(np.float32)
    y = (f[..., 0] * 0.299 + f[..., 1] * 0.587 + f[..., 2] * 0.114)[..., None]
    f = y + (f - y) * sat
    f = (f / 255.0 - 0.5) * con + 0.5
    f = np.clip(f, 0, 1)
    f = f + (f - f * f) * (con - 1.0) * 0.6                          # gentle extra mid-contrast
    out = f * 255.0
    if warm: out = out * (1 + np.array((0.04, 0.0, -0.05)) * warm)
    big[:] = np.clip(out, 0, 255).astype(np.uint8)
    return big


def _disc(r):
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1]
    return np.clip(1.0 - np.sqrt(xx * xx + yy * yy) / (r + 0.5), 0, 1)


def motes(big, t, box=None, n=40, col=(255, 226, 170), seed=1, drift=(8.0, -14.0), px=6, a=0.9, par=0.0):
    """dust / pollen motes: 3 depth layers; near layer bigger, softer and moves faster (parallax `par` px shifts layers)"""
    H_, W_ = big.shape[:2]
    x0, y0, x1, y1 = box or (0, 0, W_, H_)
    r = np.random.default_rng(seed)
    P_ = r.random((n, 4))
    add = np.zeros(big.shape, np.float32)
    for i, (u, w, ph, d) in enumerate(P_):
        layer = 0 if d < 0.55 else (1 if d < 0.88 else 2)
        sp = (0.5, 1.0, 1.8)[layer]
        x = x0 + ((u * (x1 - x0) + drift[0] * sp * t + math.sin(t * 0.7 + ph * 6) * 18 + par * (layer - 1)) % (x1 - x0))
        y = y0 + ((w * (y1 - y0) + drift[1] * sp * t) % (y1 - y0))
        tw = 0.55 + 0.45 * math.sin(t * (1.5 + ph * 2) + ph * 9)
        q = int(px * (1, 1.6, 3.2)[layer])
        ix, iy = int(x) // max(1, px // 2) * max(1, px // 2), int(y) // max(1, px // 2) * max(1, px // 2)
        if layer < 2:
            if 0 <= ix < W_ - q and 0 <= iy < H_ - q:
                add[iy:iy + q, ix:ix + q] += np.array(col, np.float32) * a * tw * (0.55 if layer == 0 else 0.85)
        else:                                                           # near: a soft out-of-focus disc
            R = q * 2; d_ = _disc(R)[..., None] * a * 0.45 * tw
            ya, xa = iy - R, ix - R
            if 0 <= xa and xa + 2 * R + 1 < W_ and 0 <= ya and ya + 2 * R + 1 < H_:
                add[ya:ya + 2 * R + 1, xa:xa + 2 * R + 1] += d_ * np.array(col, np.float32)
    return screen(big, add)


def bokeh(big, t, n=14, cols=((255, 90, 200), (90, 236, 255), (255, 200, 120)), box=None, seed=3, r=(18, 46), a=0.32):
    """soft out-of-focus light discs (neon, lamps) drifting very slowly: depth behind the heroes"""
    H_, W_ = big.shape[:2]
    x0, y0, x1, y1 = box or (0, 0, W_, int(H_ * 0.47))
    g = np.random.default_rng(seed)
    add = np.zeros(big.shape, np.float32)
    for i in range(n):
        R = int(g.uniform(*r)); c = np.array(cols[i % len(cols)], np.float32)
        x = int(x0 + g.random() * (x1 - x0) + math.sin(t * 0.3 + i) * 10); y = int(y0 + g.random() * (y1 - y0) + math.cos(t * 0.25 + i) * 6)
        d_ = _disc(R); ring = np.clip(d_ * 1.6, 0, 1) ** 0.6 * (0.7 + 0.3 * (d_ < 0.25))
        ya, xa = y - R, x - R
        ys, xs = max(0, ya), max(0, xa); ye, xe = min(H_, ya + 2 * R + 1), min(W_, xa + 2 * R + 1)
        if ys >= ye or xs >= xe: continue
        sub = ring[ys - ya:ye - ya, xs - xa:xe - xa][..., None]
        add[ys:ye, xs:xe] += sub * c * a * (0.75 + 0.25 * math.sin(t * 1.3 + i))
    return screen(big, add)


def sparks(big, x, y, t, t0, n=14, col=(255, 200, 240), seed=5, life=0.7, speed=420.0, px=6):
    """burst of sparks from (x, y) at t0, falling with gravity, fading"""
    H_, W_ = big.shape[:2]
    u = t - t0
    if u < 0 or u > life: return big
    g = np.random.default_rng(seed)
    k = 1 - u / life
    for i in range(n):
        a = g.uniform(-math.pi, 0.2); v = speed * g.uniform(0.4, 1.0)
        sx = x + math.cos(a) * v * u; sy = y + math.sin(a) * v * u + 900 * u * u
        q = px if g.random() < 0.7 else px * 2
        ix, iy = int(sx), int(sy)
        if 0 <= ix < W_ - q and 0 <= iy < H_ - q:
            c = np.array(col, np.float32) * k + np.array((255, 255, 255), np.float32) * (1 - k) * 0.3
            reg = big[iy:iy + q, ix:ix + q].astype(np.float32)
            big[iy:iy + q, ix:ix + q] = np.clip(reg + c * k, 0, 255).astype(np.uint8)
    return big


def flare(big, x, y, k=1.0, col=(255, 170, 110)):
    """sunset lens flare: a soft halo at the sun + 4 ghost discs toward and past the frame centre"""
    if k <= 0: return big
    H_, W_ = big.shape[:2]
    add = np.zeros(big.shape, np.float32)
    cx, cy = W_ / 2, H_ / 2
    for j, (f, R, a) in enumerate(((0.0, 260, 0.30), (0.45, 50, 0.16), (0.8, 90, 0.10), (1.25, 36, 0.18), (1.6, 140, 0.07))):
        px_, py_ = x + (cx - x) * f, y + (cy - y) * f
        d_ = _disc(R)[..., None]
        ya, xa = int(py_) - R, int(px_) - R
        ys, xs = max(0, ya), max(0, xa); ye, xe = min(H_, ya + 2 * R + 1), min(W_, xa + 2 * R + 1)
        if ys >= ye or xs >= xe: continue
        c = np.array(col if j % 2 == 0 else (150, 220, 255), np.float32)
        add[ys:ye, xs:xe] += d_[ys - ya:ye - ya, xs - xa:xe - xa] ** (2.0 if j == 0 else 0.8) * c * a * k
    return screen(big, add)
