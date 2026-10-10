"""Stage: logical 360x640 canvas (x3 -> 1080x1920) over a big world image (code-drawn or AI background).
Camera View maps world px -> screen; characters are drawn with scene.py primitives on a logical layer."""
import math, os
import numpy as np
import scene as S
from scene import ell as _ell0

WIDE = os.environ.get('PV_WIDE') == '1'           # 16:9 (1920x1080) for long-form; default stays 9:16
W, H, UP = (640, 360, 3) if WIDE else (360, 640, 3)
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


DECALS = {}                                        # id(world) -> [world, [(img, wx, wy, ws)], [anim fns]] (props/decals.py)
T_NOW = [0.0]                                      # time of the frame being rendered (set by episode.Episode), for animated decals


class View:
    """world px -> logical screen px. X0,Y0 world top-left, Z zoom (1 = 360 world px across)."""
    def __init__(s, world, X0, Y0, Z, oy=0, hlog=H, wlog=W):
        """hlog/wlog: visible logical height/width used for clamping (a split-screen half)"""
        s.world = world; s.Z = Z; s.oy = oy
        WW, WH = world.shape[1], world.shape[0]
        s.X0 = min(max(X0, 0.0), WW - wlog / Z); s.Y0 = min(max(Y0, 0.0), WH - hlog / Z)
    def cam(s, wx, wy, unit, flip=False):
        """camera for a character drawn around anchor (1000,1000) placed at world (wx,wy), `unit` world px per unit.
        Divided by the current character pixel size PX (see set_px)."""
        k = PX[0]
        return ACam(1000.0, 1000.0, (wx - s.X0) * s.Z / k, ((wy - s.Y0) * s.Z + s.oy) / k, unit * s.Z / k, flip)
    def wcam(s):
        """camera in raw world px (for props drawn in world coordinates)"""
        k = PX[0]
        return ACam(0.0, 0.0, -s.X0 * s.Z / k, (-s.Y0 * s.Z + s.oy) / k, s.Z / k)
    def pt(s, wx, wy):
        """world -> character-canvas px (divided by PX)"""
        k = PX[0]
        return ((wx - s.X0) * s.Z / k, ((wy - s.Y0) * s.Z + s.oy) / k)
    def opt(s, wx, wy):
        """world -> output (1080x1920) px"""
        return ((wx - s.X0) * s.Z * UP, ((wy - s.Y0) * s.Z + s.oy) * UP)
    def grid(s):
        WW, WH = s.world.shape[1], s.world.shape[0]
        xs = (s.X0 + (np.arange(OUT_W) + 0.5) / (UP * s.Z)).astype(np.int32).clip(0, WW - 1)
        ys = (s.Y0 + (np.arange(OUT_H) + 0.5 - s.oy * UP) / (UP * s.Z)).astype(np.int32).clip(0, WH - 1)
        return xs, ys
    def bg(s):
        xs, ys = s.grid()
        out = s.world[ys[:, None], xs[None, :]]
        if id(s.world) in DECALS:
            from props import decals
            decals.draw(out, s)
        return out


def view_at(world, wx, wy, Z, sx=180, sy=400, hlog=H, wlog=W):
    return View(world, wx - sx / Z, wy - sy / Z, Z, hlog=hlog, wlog=wlog)


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


# ---------------------------------------------------------------- character pixel size
# Heroes are drawn on a canvas of (W/PX, H/PX): in close-ups PX=2 so hero pixels are as chunky as the zoomed background.
PX = [1]
_GRIDS = {}

def set_px(k):
    k = int(k)
    if k not in _GRIDS:
        h, w = H // k, W // k
        _GRIDS[k] = (w, h) + tuple(a.astype(np.float32) + 0.5 for a in np.mgrid[0:h, 0:w])[::-1]
    w, h, xx, yy = _GRIDS[k]
    S.W, S.H, S.XX, S.YY = w, h, xx, yy
    PX[0] = k

def px_for_zoom(Z):
    if WIDE: return 2 if Z >= 1.5 else 1
    return 2 if Z >= 2.3 else 1


class Chars:
    """character canvas at the current PX; comp() grades (scene light) and upsamples onto the frame"""
    def __init__(s):
        s.k = PX[0]
        s.col = np.zeros((S.H, S.W, 3), np.uint8); s.m = np.zeros((S.H, S.W), bool)
    def add(s, L):
        s.col[L.m] = L.col[L.m]; s.m |= L.m
    def comp(s, big, light=None):
        if s.m.any():
            col = s.col.astype(np.float32)
            if light is not None: col = light.apply(col, s.m, s.k)
            f = UP * s.k
            m = np.repeat(np.repeat(s.m, f, 0), f, 1)
            c = np.repeat(np.repeat(np.clip(col, 0, 255).astype(np.uint8), f, 0), f, 1)
            big[m] = c[m]
        s.col[:] = 0; s.m[:] = False


class Light:
    """scene lighting for heroes so they sit inside the painted background:
    amb   - ambient multiplier (r,g,b) (e.g. cool blue at night, warm at sunset)
    keys  - list of (x, y, radius, (r,g,b), strength) in OUTPUT px: warm light pools (fire, lanterns, sun)
    rim   - (dx, dy, (r,g,b), strength): edge light on the side facing direction (dx,dy)
    grad  - top-to-bottom brightness (top, bottom) multipliers (sky light from above)"""
    def __init__(s, amb=(1, 1, 1), keys=(), rim=None, grad=(1.0, 1.0), flick=1.0):
        s.amb = np.array(amb, np.float32); s.keys = list(keys); s.rim = rim; s.grad = grad; s.flick = flick
    def apply(s, col, m, k):
        h, w = m.shape
        f = UP * k
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        ox, oy = (xx + 0.5) * f, (yy + 0.5) * f
        g = np.linspace(s.grad[0], s.grad[1], h, dtype=np.float32)[:, None, None]
        out = col * s.amb * g
        for (x, y, r, c, a) in s.keys:
            d = np.sqrt((ox - x) ** 2 + (oy - y) ** 2) / r
            fall = np.clip(1 - d, 0, 1) ** 1.5 * a * s.flick
            out = out * (1 + fall[..., None] * 0.35) + fall[..., None] * np.array(c, np.float32) * 0.45
        if s.rim is not None:
            dx, dy, c, a = s.rim
            sx, sy = int(np.sign(dx)), int(np.sign(dy))
            nb = np.roll(np.roll(m, -sy, 0), -sx, 1)
            edge = m & ~nb
            edge2 = edge | (m & ~np.roll(np.roll(nb, -sy, 0), -sx, 1))
            out[edge2] = out[edge2] * (1 - a) + np.array(c, np.float32) * a
        return out


def shadow(big, v, wx, wy, rx, ry, a=0.45):
    """soft contact shadow under a hero (world coords of the feet centre, radii in world px)"""
    cx, cy = v.opt(wx, wy); Rx, Ry = rx * v.Z * UP, ry * v.Z * UP
    x0, x1 = int(max(0, cx - Rx)), int(min(OUT_W, cx + Rx)); y0, y1 = int(max(0, cy - Ry)), int(min(OUT_H, cy + Ry))
    if x0 >= x1 or y0 >= y1: return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    d = ((xx - cx) / Rx) ** 2 + ((yy - cy) / Ry) ** 2
    q = np.floor(np.clip(1 - d, 0, 1) * 3) / 3                    # stepped, pixel-art style
    reg = big[y0:y1, x0:x1]
    reg[:] = (reg * (1 - a * q[..., None])).astype(np.uint8)


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


def px_text(CH, txt, cx, cy, size, col):
    """pixel-font text straight onto a Chars canvas (cx, cy in that canvas' px)"""
    from PIL import Image, ImageDraw, ImageFont
    import paths as P
    f = ImageFont.truetype(P.FONT_PX, size); bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    img = Image.new('L', (tw + 4, th + 4), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text((2 - bb[0], 2 - bb[1]), txt, font=f, fill=255)
    m = np.array(img) > 127; ys, xs = np.nonzero(m)
    yy = ys + int(cy - th / 2) - 2; xx = xs + int(cx - tw / 2) - 2
    h, w = CH.m.shape
    ok = (yy >= 0) & (yy < h) & (xx >= 0) & (xx < w)
    CH.col[yy[ok], xx[ok]] = col; CH.m[yy[ok], xx[ok]] = True
