"""Agent Dibs (v2) — pixel-puppet engine. Unique look of this series (other series use the capsule rig of props/folk.py):
every hero is drawn at SPRITE resolution (one sprite pixel = one big visible pixel; close-ups at 2x, see res()), with hand-placed pixel art:
4-tone cel shading broken by Bayer dithering, a darker «sel-out» line around every part, a navy outer outline,
front-3/4 heads with detailed faces (sclera, iris, pupil, highlight, lids, brows, nose shading, teeth/tongue mouths,
stubble, blush, wrinkles). The finished sprite is lit by the scene Light at sprite resolution and blown up by an
integer factor straight onto the 1080x1920 frame.

Coordinates: sprite px, origin at the feet (x right = facing side, y UP). Pixel (i, j) covers [i, i+1) x [j, j+1)."""
import math
import numpy as np
from PIL import Image, ImageDraw
from stage import OUT_W, OUT_H

_B4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) / 16.0 - 0.47
_GRIDS = {}


def _grids(k):
    """canvas + coordinate grids at k sub-pixels per sprite px (k = 1 normal, k = 2 hi-res for close-ups)"""
    if k not in _GRIDS:
        w_, h_, ox_, oy_ = 220 * k, 176 * k, 110 * k, 160 * k
        rr, cc = np.mgrid[0:h_, 0:w_]
        xc = ((cc - ox_ + 0.5) / k).astype(np.float32)
        yc = ((oy_ - rr - 0.5) / k).astype(np.float32)
        bay = np.tile(_B4, (h_ // 4 + 1, w_ // 4 + 1))[:h_, :w_]
        _GRIDS[k] = (w_, h_, ox_, oy_, rr, cc, xc, yc, bay, (rr + cc) % 2 == 0)
    return _GRIDS[k]


RES = 1                                             # sub-pixels per sprite px of the sprites being drawn now
W, H, OX, OY, _RR, _CC, XC, YC, BAYER, CHECK = _grids(1)   # feet anchor: column OX, row OY (rows above it are y > 0)
HIRES_AT = 10.25                                    # output px per sprite px from which heroes are drawn at 2x (close-ups)
HIRES3_AT = 15.0                                    # ... and at 3x (extreme close-ups / inserts): a sprite px stays <= ~7.5 output px


def set_res(k):
    """switch the drawing grids (also the copies imported by props.dibscast) to k sub-pixels per sprite px"""
    global RES, W, H, OX, OY, _RR, _CC, XC, YC, BAYER, CHECK
    RES = k
    W, H, OX, OY, _RR, _CC, XC, YC, BAYER, CHECK = _grids(k)
    import sys
    dc = sys.modules.get('props.dibscast')
    if dc is not None: dc.XC, dc.YC, dc.CHECK = XC, YC, CHECK


class res:
    """with res(2): ... — draw sprites at 2x resolution (same geometry in sprite px, twice the pixels): close-ups stay crisp"""
    def __init__(s, k): s.k = int(k)
    def __enter__(s): s.prev = RES; set_res(s.k); return s
    def __exit__(s, *a): set_res(s.prev)


def res_for(scale, hires=None):
    """sub-pixels per sprite px for an on-screen scale: 2 for close-ups (>= HIRES_AT output px per sprite px), 3 for extreme close-ups
    (>= HIRES3_AT); hires=True forces at least 2, hires=False forces 1, an int forces exactly that"""
    if hires is False: return 1
    if hires is not True and isinstance(hires, int): return hires
    k = 3 if scale >= HIRES3_AT else (2 if scale >= HIRES_AT else 1)
    return max(k, 2) if hires else k
LDIR = np.array([-0.52, 0.56, 0.64], np.float32)    # light from the upper left, a little from the front
OUTLINE = (24, 18, 40)
WHITE = (246, 244, 238)


def dark(c, k=0.7):
    return tuple(int(v * k) for v in c)


def mix(a, b, k):
    return tuple(int(x + (y - x) * k) for x, y in zip(a, b))


def ramp(base, k=0.30):
    """4-tone ramp (dark, mid, base, light) from a base colour, hue-shifted: shadows cooler, lights warmer"""
    b = np.array(base, np.float32)
    d = b * 0.50 + np.array((6, 4, 22)); m = b * 0.74 + np.array((4, 2, 12))
    l = b + (255 - b) * k + np.array((6, 4, -4))
    return [tuple(int(v) for v in np.clip(x, 0, 255)) for x in (d, m, b, l)]


def erode(m):
    return m & np.roll(m, 1, 0) & np.roll(m, -1, 0) & np.roll(m, 1, 1) & np.roll(m, -1, 1)


def dilate(m):
    return m | np.roll(m, 1, 0) | np.roll(m, -1, 0) | np.roll(m, 1, 1) | np.roll(m, -1, 1)


def lit(nx, ny, flat=0.0):
    """lit value 0..1 from a 2D normal (unit disc coords, y up)"""
    nz = np.sqrt(np.clip(1.0 - nx * nx - ny * ny, 0.0, 1.0))
    d = nx * LDIR[0] + ny * LDIR[1] + nz * LDIR[2]
    return np.clip(0.12 + 0.78 * d + flat, 0.0, 1.0)


# ======================================================================================== the sprite canvas
class Spr:
    def __init__(s):
        s.k, s.W, s.H, s.OX, s.OY = RES, W, H, OX, OY           # resolution of this canvas (see res())
        s.col = np.zeros((H, W, 3), np.uint8)
        s.m = np.zeros((H, W), bool)
        s.keep = np.zeros((H, W), bool)             # pixels that survive soot (eye whites, teeth)
        s.anchors = {}
        s.mirror_text = False                       # set by Act when the sprite will be flipped: text is drawn pre-mirrored

    # ---------------------------------------------------------------- painting
    def paint(s, mask, pal, val=None, dither=0.16, bands=(0.26, 0.49, 0.75), ol=True, olc=None):
        if not mask.any(): return mask
        P = np.array(pal, np.uint8)
        n = len(pal)
        if val is None:
            idx = np.full(mask.shape, n - 2 if n > 2 else n - 1, np.int32)
        else:
            v = np.clip(val + BAYER * dither, 0.0, 0.9999)
            bb = np.array(bands[:n - 1] if n <= 4 else np.linspace(0, 1, n + 1)[1:-1], np.float32)
            idx = np.searchsorted(bb, v).astype(np.int32)
            idx = np.clip(idx, 0, n - 1)
        s.col[mask] = P[idx[mask]]
        s.m |= mask
        s.keep[mask] = False
        if ol:
            e = mask & ~erode(mask)
            s.col[e] = olc if olc is not None else dark(pal[0], 0.72)
        return mask

    def fill(s, mask, c, keep=False):
        s.col[mask] = c; s.m |= mask; s.keep[mask] = keep
        return mask

    def _blk(s, hx, hy, n, c, keep=False):
        """n x n block of canvas pixels, bottom-left at sub-pixel coords (hx, hy) from the feet anchor (y up)"""
        r1, c0 = s.OY - hy, s.OX + hx
        r0, c1 = max(0, r1 - n), min(s.W, c0 + n); r1, c0 = min(s.H, r1), max(0, c0)
        if r0 < r1 and c0 < c1:
            s.col[r0:r1, c0:c1] = c; s.m[r0:r1, c0:c1] = True; s.keep[r0:r1, c0:c1] = keep

    def dot(s, i, j, c, keep=False):
        """one sprite px (k x k canvas px at hi-res): details and the tiny font keep their size at any resolution"""
        s._blk(int(i) * s.k, int(j) * s.k, s.k, c, keep)

    def rect(s, i0, j0, i1, j1, c, keep=False):
        """pixels i0..i1-1, j0..j1-1"""
        k = s.k
        r0, r1 = s.OY - int(j1 * k), s.OY - int(j0 * k); c0, c1 = s.OX + int(i0 * k), s.OX + int(i1 * k)
        r0, r1 = max(0, r0), min(s.H, r1); c0, c1 = max(0, c0), min(s.W, c1)
        if r0 < r1 and c0 < c1:
            s.col[r0:r1, c0:c1] = c; s.m[r0:r1, c0:c1] = True; s.keep[r0:r1, c0:c1] = keep

    def line(s, a, b, c, th=1, keep=False):
        """line th sprite px thick; at hi-res it steps on the finer grid, so diagonals come out smoother"""
        (x0, y0), (x1, y1) = a, b
        k = s.k
        n = int(max(abs(x1 - x0), abs(y1 - y0)) * 2 * k) + 1
        for q in range(n + 1):
            x = x0 + (x1 - x0) * q / n; y = y0 + (y1 - y0) * q / n
            s._blk(math.floor(x * k) - (th * k) // 2, math.floor(y * k) - (th * k) // 2, th * k, c, keep)

    def stamp(s, rows, i0, j0, pal, flip=False, keep=None):
        """ASCII stamp: rows top->bottom, pal maps chars -> colours ('.' / ' ' transparent); (i0, j0) = top-left pixel"""
        for r, row in enumerate(rows):
            for k, ch in enumerate(row[::-1] if flip else row):
                if ch in pal:
                    s.dot(i0 + k, j0 - r, pal[ch], keep=(keep is not None and ch in keep))

    # ---------------------------------------------------------------- shapes (return masks)
    def m_ell(s, cx, cy, rx, ry, ang=0.0):
        u, v = XC - cx, YC - cy
        if ang:
            ca, sa = math.cos(ang), math.sin(ang); u, v = u * ca + v * sa, -u * sa + v * ca
        nx, ny = u / rx, v / ry
        return (nx * nx + ny * ny) <= 1.0, nx, ny

    def m_super(s, cx, cy, rx, ry, n=2.6):
        nx, ny = (XC - cx) / rx, (YC - cy) / ry
        return (np.abs(nx) ** n + np.abs(ny) ** n) <= 1.0, nx, ny

    def m_cap(s, a, b, r0, r1):
        ax, ay = a; bx, by = b
        dx, dy = bx - ax, by - ay; l2 = dx * dx + dy * dy + 1e-6
        t = np.clip(((XC - ax) * dx + (YC - ay) * dy) / l2, 0, 1)
        ex = XC - (ax + t * dx); ey = YC - (ay + t * dy)
        r = r0 + (r1 - r0) * t
        return ex * ex + ey * ey <= r * r, ex / np.maximum(r, 0.6), ey / np.maximum(r, 0.6)

    def m_poly(s, pts):
        img = Image.new('L', (s.W, s.H), 0)
        ImageDraw.Draw(img).polygon([(s.OX + x * s.k, s.OY - y * s.k) for x, y in pts], fill=255)
        return np.array(img) > 127

    # ---------------------------------------------------------------- shaded primitives
    def ell(s, cx, cy, rx, ry, pal, ang=0.0, flat=0.0, ol=True, olc=None, dither=0.16, clip=None):
        m, nx, ny = s.m_ell(cx, cy, rx, ry, ang)
        if clip is not None: m = m & clip
        return s.paint(m, pal, lit(nx, ny, flat), dither=dither, ol=ol, olc=olc)

    def sup(s, cx, cy, rx, ry, pal, n=2.6, flat=0.0, ol=True, olc=None, clip=None):
        m, nx, ny = s.m_super(cx, cy, rx, ry, n)
        if clip is not None: m = m & clip
        return s.paint(m, pal, lit(nx * 0.92, ny * 0.92, flat), ol=ol, olc=olc)

    def cap(s, a, b, r0, r1, pal, flat=0.0, ol=True, olc=None, clip=None):
        m, nx, ny = s.m_cap(a, b, r0, r1)
        if clip is not None: m = m & clip
        return s.paint(m, pal, lit(nx, ny, flat), ol=ol, olc=olc)

    def union(s, parts, pal, flat=0.0, ol=True, olc=None, dither=0.16, exclude=None):
        """several shapes painted as ONE volume (no inner outlines): parts = [(mask, nx, ny), ...] from m_ell/m_super"""
        M = np.zeros((s.H, s.W), bool); V = np.full((s.H, s.W), -1.0, np.float32); Z = np.full((s.H, s.W), -1.0, np.float32)
        for m, nx, ny in parts:
            nz = np.sqrt(np.clip(1.0 - nx * nx - ny * ny, 0.0, 1.0))
            take = m & (nz > Z)
            V[take] = lit(nx * 0.92, ny * 0.92, flat)[take]; Z[take] = nz[take]; M |= m
        if exclude is not None: M &= ~exclude
        return s.paint(M, pal, V, dither=dither, ol=ol, olc=olc)

    def poly(s, pts, pal, val=None, ol=True, olc=None, grad=None):
        m = s.m_poly(pts)
        if grad is not None:                                            # (y_top, y_bottom): lighter at the top
            y0, y1 = grad
            val = np.clip((YC - y1) / max(1e-3, (y0 - y1)), 0, 1) * 0.7 + 0.15 - (XC * 0.006)
        return s.paint(m, pal, val, ol=ol, olc=olc)

    # ---------------------------------------------------------------- finishing
    def outline(s, c=OUTLINE):
        o = dilate(s.m) & ~s.m
        s.col[o] = c; s.m |= o

    def soot(s, k):
        if k <= 0: return
        tgt = s.m & ~s.keep
        col = s.col.astype(np.float32)
        col[tgt] = col[tgt] * (1 - k) + np.array((30, 26, 30), np.float32) * k
        s.col = np.clip(col, 0, 255).astype(np.uint8)

    def clip_below(s, h):
        """erase everything below height h (a hero leaning out of a window)"""
        r = s.OY - int(h * s.k)
        if r < s.H: s.m[max(0, r):] = False


# ======================================================================================== tiny pixel font (labels, badges)
FONT3 = {
    'A': ['010', '101', '111', '101', '101'], 'B': ['110', '101', '110', '101', '110'], 'C': ['011', '100', '100', '100', '011'],
    'D': ['110', '101', '101', '101', '110'], 'E': ['111', '100', '110', '100', '111'], 'G': ['011', '100', '101', '101', '011'],
    'I': ['111', '010', '010', '010', '111'], 'K': ['101', '101', '110', '101', '101'], 'L': ['100', '100', '100', '100', '111'],
    'N': ['101', '111', '111', '101', '101'], 'O': ['010', '101', '101', '101', '010'], 'P': ['110', '101', '110', '100', '100'],
    'R': ['110', '101', '110', '101', '101'], 'S': ['011', '100', '010', '001', '110'], 'T': ['111', '010', '010', '010', '010'],
    'U': ['101', '101', '101', '101', '111'], 'Y': ['101', '101', '010', '010', '010'], '!': ['010', '010', '010', '000', '010'],
    ' ': ['000', '000', '000', '000', '000'], '.': ['000', '000', '000', '000', '010'], '-': ['000', '000', '111', '000', '000'],
    'F': ['111', '100', '110', '100', '100'], 'H': ['101', '101', '111', '101', '101'], 'J': ['001', '001', '001', '101', '010'],
    'M': ['101', '111', '111', '101', '101'], 'Q': ['010', '101', '101', '110', '011'], 'V': ['101', '101', '101', '101', '010'],
    'W': ['101', '101', '111', '111', '101'], 'X': ['101', '101', '010', '101', '101'], 'Z': ['111', '001', '010', '100', '111'],
    ':': ['000', '010', '000', '010', '000'], "'": ['010', '010', '000', '000', '000'], '?': ['110', '001', '010', '000', '010'],
    '0': ['111', '101', '101', '101', '111'], '1': ['010', '110', '010', '010', '111'], '2': ['110', '001', '010', '100', '111'],
    '3': ['110', '001', '010', '001', '110'], '4': ['101', '101', '111', '001', '001'], '5': ['111', '100', '110', '001', '110'],
    '6': ['011', '100', '111', '101', '111'], '7': ['111', '001', '010', '010', '010'], '8': ['111', '101', '111', '101', '111'],
    '9': ['111', '101', '111', '001', '110'], '$': ['011', '110', '010', '011', '110'], '/': ['001', '001', '010', '100', '100'],
}


def text3(sp, txt, i0, j0, c, keep=False):
    """3x5 pixel text, top-left at (i0, j0); pre-mirrored when the sprite will be flipped, so it always reads left to right"""
    x = i0
    tw = 4 * len(txt) - 1
    mir = getattr(sp, 'mirror_text', False)
    for ch in txt:
        g = FONT3.get(ch.upper(), FONT3[' '])
        for r, row in enumerate(g):
            for k, b in enumerate(row):
                if b == '1':
                    xx = x + k
                    if mir: xx = 2 * i0 + tw - 1 - xx
                    sp.dot(xx, j0 - r, c, keep)
        x += 4


# ======================================================================================== IK
def ik(o, target, l1, l2, bend=1.0):
    dx, dy = target[0] - o[0], target[1] - o[1]
    d = max(1e-3, min(math.hypot(dx, dy), l1 + l2 - 1e-3))
    a = math.atan2(dy, dx)
    c1 = max(-1.0, min(1.0, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)))
    a1 = a + bend * math.acos(c1)
    k = (o[0] + math.cos(a1) * l1, o[1] + math.sin(a1) * l1)
    e = (o[0] + math.cos(a) * d, o[1] + math.sin(a) * d)
    return k, e


# ======================================================================================== expressions
# eo eye openness, pu pupil size, bt brow tilt (+ angry / - worried), bl brow lift, mo base mouth open, mc mouth curve (+ smile),
# lid heavy upper lid, shut eyes shut (happy arcs if mc > 0.3), teeth show teeth when closed, round 'o' mouth
EXPR = dict(
    normal=dict(eo=1.0, pu=0.6, bt=0.10, bl=0.0, mo=0.0, mc=0.0),
    shout=dict(eo=1.2, pu=0.45, bt=0.55, bl=0.0, mo=0.95, mc=0.0),
    angry=dict(eo=0.85, pu=0.5, bt=0.8, bl=-0.3, mo=0.25, mc=-0.6),
    smug=dict(eo=0.8, pu=0.6, bt=0.3, bl=0.0, mo=0.0, mc=0.75, lid=0.32),
    deadpan=dict(eo=0.7, pu=0.6, bt=0.0, bl=0.0, mo=0.0, mc=0.0, lid=0.55),
    shock=dict(eo=1.35, pu=0.32, bt=-0.6, bl=0.8, mo=0.75, mc=0.0),
    cheer=dict(eo=1.1, pu=0.6, bt=-0.2, bl=0.5, mo=0.85, mc=0.9),
    smile=dict(eo=1.0, pu=0.62, bt=-0.2, bl=0.25, mo=0.0, mc=1.0, teeth=True),
    grin=dict(eo=1.05, pu=0.6, bt=-0.25, bl=0.35, mo=0.35, mc=1.0, teeth=True),
    nervous=dict(eo=1.15, pu=0.45, bt=-0.6, bl=0.4, mo=0.0, mc=-0.35),
    sad=dict(eo=0.95, pu=0.62, bt=-0.75, bl=0.2, mo=0.0, mc=-0.75),
    cry=dict(eo=1.0, pu=0.7, bt=-0.85, bl=0.3, mo=0.35, mc=-0.85, tears=True),
    stunned=dict(eo=1.25, pu=0.3, bt=-0.2, bl=0.5, mo=0.15, mc=0.0),
    content=dict(eo=0.0, pu=0.6, bt=-0.3, bl=0.3, mo=0.0, mc=0.9, shut=True),
    sly=dict(eo=0.7, pu=0.6, bt=0.5, bl=0.0, mo=0.0, mc=0.65, lid=0.35),
    panic=dict(eo=1.4, pu=0.3, bt=-0.8, bl=0.9, mo=0.9, mc=-0.2),
    ope=dict(eo=1.25, pu=0.4, bt=-0.6, bl=0.6, mo=0.5, mc=0.0, round_mouth=True),
    blank=dict(eo=0.9, pu=0.5, bt=0.0, bl=0.0, mo=0.0, mc=-0.1),
    sleepy=dict(eo=0.45, pu=0.6, bt=0.0, bl=0.0, mo=0.0, mc=0.0, lid=0.75),
    squint=dict(eo=0.5, pu=0.6, bt=0.4, bl=-0.2, mo=0.0, mc=-0.2, lid=0.5),
    glare=dict(eo=0.85, pu=0.45, bt=0.85, bl=-0.3, mo=0.0, mc=-0.35, lid=0.3),
    teary=dict(eo=1.0, pu=0.7, bt=-0.7, bl=0.3, mo=0.2, mc=-0.4, tears=True),
    wind=dict(eo=0.6, pu=0.5, bt=-0.4, bl=0.6, mo=0.7, mc=-0.2, tears=True),
)


# ======================================================================================== face kit
def eye(sp, cx, cy, w, h, X, iris, look=(0.0, 0.0), blink=False, lash=(30, 20, 30), skin=(230, 180, 150), lidc=None,
        bold=1, bag=None, white=WHITE, flick=False, slit=False):
    """detailed eye centred at (cx, cy) (sprite px), w x h px"""
    eo = X['eo']
    if blink or X.get('shut'):
        y = int(round(cy))
        if X.get('shut') and X['mc'] > 0.3:                                       # happy ^ ^
            for k in range(int(w)):
                u = (k - (w - 1) / 2) / max(1.0, (w - 1) / 2)
                sp.dot(int(round(cx - w / 2 + k)), y + int(round(1.4 * (1 - u * u))), lash)
        else:
            sp.line((cx - w / 2, cy), (cx + w / 2 - 1, cy - 0.4), lash, 1)
        if bag is not None: sp.line((cx - w / 2 + 1, cy - 2), (cx + w / 2 - 2, cy - 2), bag)
        return
    hh = max(2.0, h * min(1.25, max(0.35, eo)))
    m, nx, ny = sp.m_ell(cx, cy, w / 2.0, hh / 2.0)
    if not m.any(): return
    sp.fill(m, white, keep=True)
    sp.fill(m & (ny < -0.45), mix(white, (180, 186, 210), 0.6), keep=True)            # lower sclera shadow
    # iris + pupil
    ix = cx + look[0] * w * 0.2; iy = cy + look[1] * hh * 0.15 + (0.12 * hh if X.get('look_up') else 0.0)
    ri = max(1.0, min(w, hh) * 0.40)
    mi, _, _ = sp.m_ell(ix, iy, ri, ri)
    mi &= m
    sp.fill(mi, iris, keep=True)
    sp.fill(mi & (YC < iy - ri * 0.2), dark(iris, 0.72), keep=True)
    rp = max(0.7, ri * (0.35 + 0.5 * X['pu']))
    mp, _, _ = sp.m_ell(ix, iy, max(0.6, rp * 0.35) if slit else rp, ri * 0.95 if slit else rp)
    sp.fill(mp & m, (14, 12, 18), keep=True)
    sp.dot(int(math.floor(ix - ri * 0.45)), int(math.floor(iy + ri * 0.35)), (255, 255, 255), keep=True)   # highlight
    if w >= 7: sp.dot(int(math.floor(ix + ri * 0.4)), int(math.floor(iy - ri * 0.5)), (220, 230, 255), keep=True)
    # heavy upper lid
    lid = X.get('lid', 0.0)
    if lid > 0:
        ytop = cy + hh / 2 - lid * hh
        ml = m & (YC > ytop)
        sp.fill(ml, lidc or skin)
        edge = m & ~ml & dilate(ml)
        sp.fill(edge, lash)
    # contour: thick upper lash line, outer flick, thin lower line
    e = m & ~erode(m)
    top = e & (YC > cy - 0.2)
    sp.fill(top, lash)
    for _ in range((bold - 1) + (sp.k - 1)): top = top | (dilate(top) & ~m & (YC > cy)); sp.fill(top, lash)
    if flick: sp.dot(int(math.floor(cx - w / 2 - 1)), int(math.floor(cy + hh * 0.25)), lash)
    sp.fill(e & (YC <= cy - 0.2), mix(skin, lash, 0.45))
    if bag is not None:
        sp.line((cx - w / 2 + 1, cy - hh / 2 - 1.2), (cx + w / 2 - 2, cy - hh / 2 - 1.2), bag)
    if X.get('tears'):
        sp.ell(cx + w * 0.2, cy - hh / 2 - 2 - (sp.anchors.get('tear', 0.0)), 1.2, 1.8, [(90, 150, 220), (130, 190, 240), (170, 220, 255), (230, 246, 255)], ol=False)


def brow(sp, cx, cy, w, X, side, col, th=2, bushy=False, arch=0.8):
    """tapered arched brow; side = +1 for the near eye (inner end on its +x side), -1 for the far eye"""
    bt, bl = X['bt'], X['bl']
    y = cy + bl * 1.8
    x_o, x_i = cx - side * w / 2, cx + side * w / 2
    y_o = y + 0.9 * bt - 0.5 * abs(bt)
    y_i = y - 2.2 * bt
    top, bot = [], []
    n = max(2, int(abs(x_i - x_o)) + 1)
    for k in range(n + 1):
        u = k / n
        x = x_o + (x_i - x_o) * u
        yy = y_o + (y_i - y_o) * u + arch * math.sin(math.pi * min(1.0, u * 1.15)) * (1 - max(0.0, bt) * 0.8)
        tk = th * (0.6 + 0.4 * u)
        top.append((x, yy + tk / 2)); bot.append((x, yy - tk / 2))
    m = sp.m_poly(top + bot[::-1])
    sp.fill(m, col)
    if bushy:
        for k in range(0, n, 2):
            x, yy = top[k]
            sp.dot(int(math.floor(x)), int(math.floor(yy)), col)


def mouth(sp, mx, my, w, X, m, lipc, inside=(92, 22, 34), teeth=WHITE, tongue=(220, 96, 110), skin=None, maxh=7, big_teeth=False):
    """mouth centred at (mx, my): closed curve / open with teeth and tongue / 'o'"""
    mc = X['mc']
    mo = max(m, X['mo'])
    if X.get('round_mouth') and mo > 0.05:
        r = 1.5 + 1.4 * mo
        mm, _, _ = sp.m_ell(mx, my - 0.5, r * 0.8, r)
        sp.fill(mm, inside, keep=False)
        sp.fill(mm & ~erode(mm), lipc)
        sp.fill(mm & (YC < my - 0.5 - r * 0.35) & erode(mm), tongue)
        return
    if mo > 0.10:
        hw = w / 2 * (0.75 + 0.25 * mo) + max(0.0, mc) * 1.0
        hh = 1.0 + mo * maxh / 2
        cyy = my - hh * 0.35 + mc * 0.6
        mm, nx, ny = sp.m_ell(mx, cyy, hw, hh)
        if mc > 0.3:                                                          # smile: flatten the top
            mm &= YC < cyy + hh * 0.55
        elif mc < -0.3:
            mm &= YC > cyy - hh * 0.6
        sp.fill(mm, inside)
        inner = erode(mm)
        if X.get('teeth') and mc > 0.5:                                               # megawatt grin: all teeth, thin dark gap
            sp.fill(inner, teeth, keep=True)
            sp.fill(inner & (np.abs(YC - (cyy + hh * 0.05)) < 0.5) & (mo > 0.3), (200, 200, 210), keep=True)
            for k in range(-int(hw) + 2, int(hw) - 1, 2): sp.fill(inner & (np.abs(XC - (mx + k + 0.5)) < 0.5) & (YC > cyy + hh * 0.05), (214, 214, 224), keep=True)
            sp.fill(mm & ~erode(mm), lipc)
            return
        sp.fill(inner & (YC > cyy + hh * 0.35), teeth, keep=True)                     # upper teeth row
        if big_teeth: sp.fill(inner & (YC > cyy + hh * 0.05) & (np.abs(XC - mx) < hw * 0.6), teeth, keep=True)
        if mo > 0.45:
            sp.fill(inner & (YC < cyy - hh * 0.35), tongue)
            if mo > 0.7: sp.fill(inner & (YC < cyy - hh * 0.6), dark(tongue, 0.86))
        sp.fill(mm & ~erode(mm), lipc)
        return
    # closed: curved line, corners up for a smile
    if X.get('teeth') and mc > 0.5:
        hw = int(w / 2 + 1)
        for k in range(-hw, hw + 1):
            u = k / hw
            y = my + mc * 1.8 * u * u
            sp.dot(int(mx + k), int(math.floor(y)), teeth, keep=True)
            sp.dot(int(mx + k), int(math.floor(y)) + 1, lipc)
            sp.dot(int(mx + k), int(math.floor(y)) - 1, lipc)
        for k in range(-hw + 2, hw - 1, 2): sp.dot(int(mx + k), int(math.floor(my + mc * 1.8 * (k / hw) ** 2)), (200, 204, 214), keep=True)
        return
    hw = w / 2
    pts = []
    for k in range(int(-hw), int(hw) + 1):
        u = k / max(1.0, hw)
        y = my + mc * 1.6 * u * u - (0.4 * mc if abs(u) < 0.3 else 0)
        pts.append((mx + k, y))
    for (x, y) in pts: sp.dot(int(math.floor(x)), int(math.floor(y)), lipc)
    if skin is not None:                                                          # lower lip volume
        for (x, y) in pts[1:-1]: sp.dot(int(math.floor(x)), int(math.floor(y)) - 1, mix(skin, lipc, 0.35))


def stubble(sp, mask, col, density=0.5, seed=1):
    rng = np.random.default_rng(seed)
    r = rng.random(mask.shape) < density
    sp.fill(mask & r & CHECK, col)


def blush(sp, cx, cy, rx, ry, col):
    m, _, _ = sp.m_ell(cx, cy, rx, ry)
    sp.fill(m & CHECK & sp.m, col)


# ======================================================================================== lighting + compositing on the frame
def light_sprite(col, m, x0, y0, s, lt, scale=1.0):
    if lt is None: return col.astype(np.float32)
    h, w = m.shape
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    ox, oy = x0 + (xx + 0.5) * s, y0 + (yy + 0.5) * s
    g = (lt.grad[0] + (lt.grad[1] - lt.grad[0]) * np.clip(oy / OUT_H, 0, 1))[..., None]
    out = col.astype(np.float32) * lt.amb * g
    for (x, y, r, c, a) in lt.keys:
        d = np.sqrt((ox - x) ** 2 + (oy - y) ** 2) / r
        fall = np.clip(1 - d, 0, 1) ** 1.5 * a * lt.flick
        out = out * (1 + fall[..., None] * 0.35) + fall[..., None] * np.array(c, np.float32) * 0.45
    if lt.rim is not None:
        dx, dy, c, a = lt.rim
        sx, sy = int(np.sign(dx)), int(np.sign(dy))
        nb = np.roll(np.roll(m, -sy, 0), -sx, 1)
        edge = m & ~nb
        out[edge] = out[edge] * (1 - a) + np.array(c, np.float32) * a
    return out


def blit(big, sp, ox, oy, s, lt=None, flip=False, alpha=1.0, ghost=None, shadow=0.0):
    """paste a finished sprite: (ox, oy) = output px of the feet anchor, s = output px per sprite px (float ok: nearest sampling)"""
    s = max(1.0, float(s))
    k = getattr(sp, 'k', 1)
    col, m = sp.col, sp.m
    if flip: col, m = col[:, ::-1], m[:, ::-1]
    rows = np.where(m.any(1))[0]; cols = np.where(m.any(0))[0]
    if len(rows) == 0: return
    r0, r1, c0, c1 = rows[0], rows[-1] + 1, cols[0], cols[-1] + 1
    ax = (sp.W - sp.OX) if flip else sp.OX
    x0 = ox + (c0 - ax) * s / k; y0 = oy + (r0 - sp.OY) * s / k
    BH, BW = big.shape[:2]
    if shadow > 0:
        rx, ry = 13 * s, 3.2 * s
        X0, X1 = int(max(0, ox - rx)), int(min(BW, ox + rx)); Y0, Y1 = int(max(0, oy - ry)), int(min(BH, oy + ry))
        if X0 < X1 and Y0 < Y1:
            yy, xx = np.mgrid[Y0:Y1, X0:X1].astype(np.float32)
            d = ((xx - ox) / rx) ** 2 + ((yy - oy) / ry) ** 2
            q = np.floor(np.clip(1 - d, 0, 1) * 3) / 3
            reg = big[Y0:Y1, X0:X1]
            reg[:] = (reg * (1 - shadow * q[..., None])).astype(np.uint8)
    s = s / k                                                               # output px per canvas px
    sub = col[r0:r1, c0:c1]; sm = m[r0:r1, c0:c1]
    hh, ww = sm.shape
    X0, Y0 = max(0, int(math.floor(x0))), max(0, int(math.floor(y0)))
    X1, Y1 = min(BW, int(math.ceil(x0 + ww * s))), min(BH, int(math.ceil(y0 + hh * s)))
    if X0 >= X1 or Y0 >= Y1: return
    ci = np.floor((np.arange(X0, X1) + 0.5 - x0) / s).astype(int); ri = np.floor((np.arange(Y0, Y1) + 0.5 - y0) / s).astype(int)
    vx = (ci >= 0) & (ci < ww); vy = (ri >= 0) & (ri < hh)
    ci = np.clip(ci, 0, ww - 1); ri = np.clip(ri, 0, hh - 1)
    lc = np.clip(light_sprite(sub, sm, x0, y0, s, lt), 0, 255).astype(np.uint8)
    u = lc[ri[:, None], ci[None, :]]
    mm = sm[ri[:, None], ci[None, :]] & vy[:, None] & vx[None, :]
    reg = big[Y0:Y1, X0:X1]
    if ghost is not None:                                                   # invisibility cloak: see-through + shimmering cyan edge
        a = ghost
        reg[mm] = np.clip(reg[mm] * (1 - a) + (u[mm] * 0.86 + np.array((120, 240, 255)) * 0.14) * a, 0, 255).astype(np.uint8)
        k = max(1, int(round(s)))
        ed = mm & ~(np.roll(mm, k, 0) & np.roll(mm, -k, 0) & np.roll(mm, k, 1) & np.roll(mm, -k, 1))
        reg[ed] = (150, 244, 255)
        return
    if alpha >= 1.0:
        reg[mm] = u[mm]
    else:
        reg[mm] = np.clip(reg[mm] * (1 - alpha) + u[mm] * alpha, 0, 255).astype(np.uint8)


def rotate(sp, deg, pivot=(0.0, 0.0)):
    """rotate a finished sprite in place (nearest neighbour) around pivot (sprite px from the feet anchor, y up); anchors follow"""
    cx, cy = sp.OX + pivot[0] * sp.k, sp.OY - pivot[1] * sp.k
    rgba = np.zeros((sp.H, sp.W, 4), np.uint8); rgba[..., :3] = sp.col; rgba[..., 3] = sp.m * 255
    img = Image.fromarray(rgba).rotate(deg, resample=Image.NEAREST, center=(cx, cy))
    a = np.array(img)
    sp.col = a[..., :3].copy(); sp.m = a[..., 3] > 127; sp.keep = sp.keep & sp.m
    ca, sa = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    for k, (x, y) in list(sp.anchors.items()):
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            dx, dy = x - pivot[0], y - pivot[1]
            sp.anchors[k] = (pivot[0] + dx * ca - dy * sa, pivot[1] + dx * sa + dy * ca)


class Act:
    """direct-draw actor for chikit.shot: Act(draw_fn, wx, wy, s=..., **params); draw_fn(sp, **params) paints a Spr"""
    direct = True

    def __init__(s, fn, wx, wy, s_=None, un=None, flip=False, shadow=0.0, ghost=None, alpha=1.0, post=None, pin=None, rot=0.0, pivot=(0.0, 0.0),
                 hires=None, **P):
        """(wx, wy) = world position of the feet anchor, or of the sprite anchor named by `pin` (e.g. pin='head' for close-ups);
        rot = degrees counter-clockwise around `pivot` (sprite px from the feet anchor, y up);
        hires: None = 2x / 3x sprite resolution automatically from HIRES_AT / HIRES3_AT (close-ups), True = at least 2x, False = 1x"""
        s.fn, s.wx, s.wy, s.s, s.un, s.flip, s.shadow, s.ghost, s.alpha, s.post, s.pin, s.P = fn, wx, wy, s_, un, flip, shadow, ghost, alpha, post, pin, P
        s.rot, s.pivot, s.hires = rot, pivot, hires

    def scale(s, v):
        if s.s is not None: return float(s.s)
        return max(1.0, s.un * v.Z * 3.0 * 0.25)

    def __call__(s, big, v, lt):
        sc = s.scale(v)
        with res(res_for(sc, s.hires)):
            sp = Spr()
            sp.mirror_text = s.flip
            s.fn(sp, **s.P)
            if s.post: s.post(sp)
            if s.rot: rotate(sp, s.rot, s.pivot)
        ox, oy = v.opt(s.wx, s.wy)
        if s.pin:
            px, py = sp.anchors[s.pin]
            ox -= (-px if s.flip else px) * sc; oy += py * sc
        blit(big, sp, ox, oy, sc, lt, s.flip, s.alpha, s.ghost, s.shadow)
        s.last = sp


def draw(fn, s=6.0, flip=False, hires=None, **P):
    """a finished sprite at the resolution its on-screen scale s needs (2x for close-ups, 3x for extreme close-ups)"""
    with res(res_for(s, hires)):
        sp = Spr(); sp.mirror_text = flip
        fn(sp, **P)
    return sp


def render(fn, s=6, bg=(60, 70, 96), size=(1080, 1920), at=None, flip=False, **P):
    """test helper: one sprite on a plain frame"""
    big = np.zeros((size[1], size[0], 3), np.uint8); big[:] = bg
    sp = draw(fn, s, **P)
    ox, oy = at or (size[0] // 2, size[1] - 60)
    blit(big, sp, ox, oy, s, None, flip)
    return big
