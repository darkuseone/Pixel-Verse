"""«Florida Man: Allegedly» — sprite manner «Tabloid Sun» (see series/florida-man/design/philosophy.md).
Same sprite canvas / IK / face kit / blit as props/dibspix.py (one sprite px = one visible square, 2x/3x for close-ups), but its own look:
  * 4 tones per material (teal depth, shadow, base, sun-bleached light) with HALFTONE transitions: round clustered dots on a 45° screen,
    growing towards the dark (cheap tabloid newsprint), fixed to the sprite pixel so nothing boils between frames;
  * the key light is the noon sun almost straight ABOVE: tops of heads, shoulders, bellies and beaks flare, short hard shadows below;
    `gloss` materials (skin, sunglasses, beaks) get white sun glints on their brightest pixels;
  * dark-teal outline instead of black (heroes belong to the heat, not to the night).
Usage: Act(fn, wx, wy, s_=.., **params) exactly like dibspix.Act (chikit.shot treats it as a direct actor)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from props import dibspix as DX
from props.dibspix import dark, mix, erode, dilate, ik, EXPR, res, res_for, blit, rotate
import paths as P

INK = (14, 44, 54)                                     # dark teal outline
LDIR_SUN = np.array([0.22, 0.84, 0.50], np.float32)   # noon sun: high above, a little from the front-facing side
WHITE = (250, 248, 238)
GLINT = (255, 255, 246)
_HT = {}


class sun:
    """the shared dibspix lit() reads DX.LDIR at call time: swap it while a Florida Man sprite is being drawn"""
    def __enter__(s): s.prev = DX.LDIR; DX.LDIR = LDIR_SUN; return s
    def __exit__(s, *a): DX.LDIR = s.prev


def halftone():
    """clustered-dot threshold field (-0.5 .. 0.5) on a 45° screen with a period of 4 sprite px (k*4 canvas px at hi-res):
    0 at the dot centres, so dark tones grow as round dots — newsprint, not Bayer, not stipple"""
    k = DX.RES
    if k not in _HT:
        rr, cc = np.mgrid[0:DX.H, 0:DX.W].astype(np.float32)
        per = 4.0 * k
        u = (cc + rr) / math.sqrt(2.0); v = (cc - rr) / math.sqrt(2.0)
        du = (u / per) % 1.0 - 0.5; dv = (v / per) % 1.0 - 0.5
        d = np.sqrt(du * du + dv * dv) / math.sqrt(0.5)            # 0 dot centre .. 1 cell corner
        _HT[k] = (d - 0.5).astype(np.float32)
    return _HT[k]


def tones(base, k=0.30):
    """4-tone ramp (depth, shadow, base, light): shadows sink to teal, the lit side bleaches towards warm white"""
    b = np.array(base, np.float32)
    d = b * 0.54 + np.array((2, 20, 28))
    s = b * 0.79 + np.array((2, 9, 13))
    l = b + (255 - b) * k + np.array((10, 6, -6))
    return [tuple(int(v) for v in np.clip(x, 0, 255)) for x in (d, s, b, l)]


class Spr(DX.Spr):
    def dot(s, i, j, c, keep=False):
        """detail dot: a hard sprite px at 1-2x, a small round blob at hi-res (close-ups: no square «mush» specks)"""
        if s.k < 3: return DX.Spr.dot(s, i, j, c, keep)
        cx, cy = int(i) + 0.5, int(j) + 0.5
        s.fill(s.m_ell(cx, cy, 0.58, 0.58)[0], c, keep)

    def paint(s, mask, pal, val=None, dither=0.30, bands=(0.22, 0.44, 0.80), ol=True, olc=None, gloss=0.0):
        """gloss > 0: pixels lit above 1-gloss*0.12 turn into white sun glints (skin, lenses, beaks)"""
        if not mask.any(): return mask
        pal = list(pal)
        if len(pal) == 3: pal = [pal[0], pal[0], pal[1], pal[2]]
        if len(pal) == 2: pal = [pal[0], pal[0], pal[1], pal[1]]
        if len(pal) == 1: pal = [dark(pal[0], 0.4), dark(pal[0], 0.7), pal[0], pal[0]]
        Pp = np.array(pal, np.uint8)
        if val is None:
            idx = np.full(mask.shape, 2, np.int32)
        else:
            vv = np.asarray(val, np.float32)
            dk = dither * (1.0, 1.0, 0.75, 0.6)[min(3, s.k)]              # big halftone cells at 2x/3x: calmer transitions
            v = np.clip(vv + halftone() * dk, 0.0, 0.9999)
            idx = np.searchsorted(np.array(bands, np.float32), v).astype(np.int32)
        s.col[mask] = Pp[np.clip(idx, 0, 3)[mask]]
        if gloss and val is not None:
            g = mask & (np.asarray(val, np.float32) > 1.0 - gloss * 0.12) & (halftone() < 0.0)
            s.col[g] = GLINT
        s.m |= mask
        s.keep[mask] = False
        if ol:
            e = mask & ~erode(mask)
            s.col[e] = olc if olc is not None else mix(pal[0], INK, 0.55)
        return mask

    def ell(s, cx, cy, rx, ry, pal, ang=0.0, flat=0.0, ol=True, olc=None, dither=0.30, clip=None, gloss=0.0):
        m, nx, ny = s.m_ell(cx, cy, rx, ry, ang)
        if clip is not None: m = m & clip
        return s.paint(m, pal, DX.lit(nx, ny, flat), dither=dither, ol=ol, olc=olc, gloss=gloss)

    def sup(s, cx, cy, rx, ry, pal, n=2.6, flat=0.0, ol=True, olc=None, clip=None, gloss=0.0):
        m, nx, ny = s.m_super(cx, cy, rx, ry, n)
        if clip is not None: m = m & clip
        return s.paint(m, pal, DX.lit(nx * 0.92, ny * 0.92, flat), ol=ol, olc=olc, gloss=gloss)

    def cap(s, a, b, r0, r1, pal, flat=0.0, ol=True, olc=None, clip=None, gloss=0.0):
        m, nx, ny = s.m_cap(a, b, r0, r1)
        if clip is not None: m = m & clip
        return s.paint(m, pal, DX.lit(nx, ny, flat), ol=ol, olc=olc, gloss=gloss)

    def union(s, parts, pal, flat=0.0, ol=True, olc=None, dither=0.30, exclude=None, gloss=0.0):
        M = np.zeros((s.H, s.W), bool); V = np.full((s.H, s.W), -1.0, np.float32); Z = np.full((s.H, s.W), -1.0, np.float32)
        for m, nx, ny in parts:
            nz = np.sqrt(np.clip(1.0 - nx * nx - ny * ny, 0.0, 1.0))
            take = m & (nz > Z)
            V[take] = DX.lit(nx * 0.92, ny * 0.92, flat)[take]; Z[take] = nz[take]; M |= m
        if exclude is not None: M &= ~exclude
        return s.paint(M, pal, V, dither=dither, ol=ol, olc=olc, gloss=gloss)

    def outline(s, c=INK, w=1):
        o = s.m.copy()
        for _ in range(w * s.k): o = dilate(o)
        o &= ~s.m
        s.col[o] = c; s.m |= o

    def ptext(s, txt, i0, j0, col, size=8, keep=False, center=False):
        """Press Start 2P text rasterised at sprite resolution (glyph cell = `size` sprite px); pre-mirrored on flipped sprites"""
        f = ImageFont.truetype(P.FONT_PX, size * s.k)
        bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
        img = Image.new('L', (tw + 2, th + 2), 0); dd = ImageDraw.Draw(img); dd.fontmode = '1'
        dd.text((-bb[0], -bb[1]), txt, font=f, fill=255)
        m = np.array(img) > 127
        if s.mirror_text: m = m[:, ::-1]
        ys, xs = np.nonzero(m)
        x0 = int(i0 * s.k - (tw / 2 if center else 0)); y0 = int(j0 * s.k)
        cc = s.OX + x0 + xs; rr = s.OY - y0 + ys
        ok = (cc >= 0) & (cc < s.W) & (rr >= 0) & (rr < s.H)
        s.col[rr[ok], cc[ok]] = col; s.m[rr[ok], cc[ok]] = True; s.keep[rr[ok], cc[ok]] = keep
        return tw / s.k


def stroke(sp, pts, c=INK, th=1):
    for a, b in zip(pts[:-1], pts[1:]): sp.line(a, b, c, th)


def ht_fill(sp, mask, c, density=0.35):
    """halftone dots of colour c inside mask (tattoo shading, sweat sheen, frost)"""
    sp.fill(mask & (halftone() < density - 0.5), c)


class Act(DX.Act):
    """direct-draw actor (chikit.shot): paints an fmpix Spr under the noon sun, then blits it like dibspix.Act"""
    def __call__(s, big, v, lt):
        sc = s.scale(v)
        with res(res_for(sc, s.hires)), sun():
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


def draw(fn, s=6.0, flip=False, hires=None, rot=0.0, pivot=(0.0, 0.0), **P_):
    with res(res_for(s, hires)), sun():
        sp = Spr(); sp.mirror_text = flip
        fn(sp, **P_)
        if rot: rotate(sp, rot, pivot)
    return sp


def render(fn, s=6, bg=(120, 200, 210), size=(1080, 1920), at=None, flip=False, **P_):
    big = np.zeros((size[1], size[0], 3), np.uint8); big[:] = bg
    sp = draw(fn, s, flip=flip, **P_)
    ox, oy = at or (size[0] // 2, size[1] - 60)
    blit(big, sp, ox, oy, s, None, flip)
    return big
