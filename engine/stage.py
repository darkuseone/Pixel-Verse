"""Stage: logical 360x640 canvas (x3 -> 1080x1920) over a big world image (code-drawn or AI background).
Camera View maps world px -> screen; characters are drawn with scene.py primitives on a logical layer."""
import math
import numpy as np
import scene as S
from scene import ell as _ell0

W, H, UP = 360, 640, 3
OUT_W, OUT_H = W * UP, H * UP
S.W, S.H = W, H
S.YY, S.XX = [a.astype(np.float32) + 0.5 for a in np.mgrid[0:H, 0:W]]


class ACam:
    def __init__(s, ax, ay, sx, sy, sc, flip=False): s.ax, s.ay, s.sx, s.sy, s.sc, s.flip = ax, ay, sx, sy, sc, flip
    def p(s, x, y):
        X = (x - s.ax) * s.sc
        return (s.sx + (-X if s.flip else X), s.sy + (y - s.ay) * s.sc)


def ell(L, cxy, rx, ry, c, ang=0.0, **kw):
    if getattr(L.cam, 'flip', False): ang = -ang
    return _ell0(L, cxy, rx, ry, c, ang, **kw)
S.ell = ell


class View:
    """world px -> logical screen px. X0,Y0 world top-left, Z zoom (1 = 360 world px across)."""
    def __init__(s, world, X0, Y0, Z, oy=0):
        s.world = world; s.Z = Z; s.oy = oy
        WW, WH = world.shape[1], world.shape[0]
        s.X0 = min(max(X0, 0.0), WW - W / Z); s.Y0 = min(max(Y0, 0.0), WH - H / Z)
    def cam(s, wx, wy, unit, flip=False):
        """camera for a character drawn around anchor (1000,1000) placed at world (wx,wy), `unit` world px per unit"""
        return ACam(1000.0, 1000.0, (wx - s.X0) * s.Z, (wy - s.Y0) * s.Z + s.oy, unit * s.Z, flip)
    def wcam(s):
        """camera in raw world px (for props drawn in world coordinates)"""
        return ACam(0.0, 0.0, -s.X0 * s.Z, -s.Y0 * s.Z + s.oy, s.Z)
    def pt(s, wx, wy): return ((wx - s.X0) * s.Z, (wy - s.Y0) * s.Z + s.oy)
    def grid(s):
        WW, WH = s.world.shape[1], s.world.shape[0]
        xs = (s.X0 + (np.arange(OUT_W) + 0.5) / (UP * s.Z)).astype(np.int32).clip(0, WW - 1)
        ys = (s.Y0 + (np.arange(OUT_H) + 0.5 - s.oy * UP) / (UP * s.Z)).astype(np.int32).clip(0, WH - 1)
        return xs, ys
    def bg(s):
        xs, ys = s.grid()
        return s.world[ys[:, None], xs[None, :]]


def view_at(world, wx, wy, Z, sx=180, sy=400):
    return View(world, wx - sx / Z, wy - sy / Z, Z)


def sample(v, arr):
    """sample any world-aligned array (e.g. a glow map) on the output grid of view v"""
    xs, ys = v.grid()
    return arr[ys[:, None], xs[None, :]]


def blit_world(big, v, spr, x_left, y_top):
    """composite an RGBA sprite given in world px (foreground occluders, extra props)"""
    xs, ys = v.grid()
    sx = xs - x_left; sy = ys - y_top
    okx = (sx >= 0) & (sx < spr.shape[1]); oky = (sy >= 0) & (sy < spr.shape[0])
    if not okx.any() or not oky.any(): return
    cx = np.nonzero(okx)[0]; cy = np.nonzero(oky)[0]
    sub = spr[sy[cy][:, None], sx[cx][None, :]]
    m = sub[..., 3] > 0
    reg = big[cy[0]:cy[-1] + 1, cx[0]:cx[-1] + 1]
    reg[m] = sub[..., :3][m]


class Chars:
    """logical-resolution character canvas; comp() upsamples x3 onto the frame"""
    def __init__(s):
        s.col = np.zeros((H, W, 3), np.uint8); s.m = np.zeros((H, W), bool)
    def add(s, L):
        s.col[L.m] = L.col[L.m]; s.m |= L.m
    def comp(s, big):
        m = np.repeat(np.repeat(s.m, UP, 0), UP, 1)
        c = np.repeat(np.repeat(s.col, UP, 0), UP, 1)
        big[m] = c[m]
        s.col[:] = 0; s.m[:] = False


def wrect(L, x0, y0, x1, y1, c):
    ax, ay = L.cam.p(x0, y0); bx, by = L.cam.p(x1, y1)
    xa, xb = sorted((ax, bx)); ya, yb = sorted((ay, by))
    w = S.win(xa, xb, ya, yb)
    if w is None: return
    X = S.XX[w]; Y = S.YY[w]
    L.set(w, (X >= xa) & (X < xb) & (Y >= ya) & (Y < yb), c)


def ai_world(path, size=None, colors=110):
    """AI background -> world image: optional resize (BOX) + palette quantization (no dither)."""
    from PIL import Image
    im = Image.open(path).convert('RGB')
    if size: im = im.resize(size, Image.BOX)
    q = im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
    return np.array(q)
