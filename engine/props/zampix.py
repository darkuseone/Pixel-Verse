"""«Замело» — sprite manner «Морозное утро» (series/zamelo/design/philosophy.md).
Same sprite canvas / IK / face kit / blit as props/dibspix.py (one sprite px = one visible square, 2x..6x for close-ups) and the fast
local rasterisers + fitted Press Start 2P Cyrillic text of props/taigapix.Spr, but its own look:
  * key light = the HIGH frosty sky from the upper left: soft, broad; shadows sink into navy / blue-violet snow shade;
  * tone borders break into short DIAGONAL frost hatches (a knitted-mitten / frosted-glass feel), not dither, not blinds;
  * every hero gets a DUAL RIM after drawing: the top of the silhouette glows snow-white-blue (light reflected by the snow plain
    everywhere around), the sun side glows sunrise orange — volume inside the sprite (Act(rim=...));
  * puffy clothes are drawn as stacked rounded quilts (a down jacket), knits with stripe bands; deep navy ink outline, 1 sprite px.
Usage: Act(fn, wx, wy, s_=.., rim=(snow, sun) | None, **params) like dibspix.Act (depth25.shot25 direct actor)."""
import numpy as np
from props import dibspix as DX
from props import taigapix as TX
from props.dibspix import dark, mix, erode, dilate, res, res_for, blit, rotate

INK = (26, 30, 66)                                      # deep navy ink
LDIR_SKY = np.array([-0.48, 0.66, 0.58], np.float32)    # high frosty sky from the upper left
SNOWRIM = (226, 240, 255)                               # snow-plain bounce on top edges
SUN = (255, 168, 92)                                    # sunrise rim on the sun side
WHITE = (252, 252, 248)
_HT = {}


def tones(base, k=0.32):
    """3-tone ramp (shadow, base, light): shadow navy-violet snow shade, light warm sunrise peach"""
    b = np.array(base, np.float32)
    d = b * 0.54 + np.array((10, 16, 52))
    l = b + (255 - b) * k + np.array((16, 8, -10))
    return [tuple(int(v) for v in np.clip(x, 0, 255)) for x in (d, b, l)]


def hatch(shape, k):
    """diagonal frost hatches: every 3rd diagonal of sprite px, fixed in the canvas -> no boiling between frames"""
    key = (shape, k)
    if key not in _HT:
        rr, cc = np.mgrid[0:shape[0], 0:shape[1]]
        _HT[key] = ((rr // max(1, k) + cc // max(1, k)) % 3) == 0
    return _HT[key]


class sky_light:
    """the shared dibspix lit() reads DX.LDIR at call time: swap it while a «Замело» sprite is being drawn"""
    def __enter__(s): s.prev = DX.LDIR; DX.LDIR = LDIR_SKY; return s
    def __exit__(s, *a): DX.LDIR = s.prev


class Spr(TX.Spr):
    def paint(s, mask, pal, val=None, dither=None, bands=(0.30, 0.70), ol=True, olc=None, bounce=None, gloss=0.0, frost=True):
        if not mask.any(): return mask
        pal = list(pal)
        if len(pal) == 4: pal = [pal[0], pal[2], pal[3]]
        if len(pal) == 2: pal = [pal[0], pal[1], pal[1]]
        if len(pal) == 1: pal = [dark(pal[0], 0.6), pal[0], pal[0]]
        Pp = np.array(pal, np.uint8)
        if val is None:
            idx = np.ones(mask.shape, np.int32)
        else:
            v = np.asarray(val, np.float32)
            idx = np.searchsorted(np.array(bands, np.float32), v).astype(np.int32)
            if frost:                                                       # frost hatches across each tone border
                ht = hatch(mask.shape, s.k)
                for b in bands:
                    idx[(v >= b) & (v < b + 0.11) & ht] -= 1
        s.col[mask] = Pp[np.clip(idx, 0, 2)[mask]]
        if gloss and val is not None:
            g = mask & (np.asarray(val, np.float32) > 1.0 - gloss * 0.10)
            s.col[g] = WHITE
        s.m |= mask
        s.keep[mask] = False
        if ol:
            e = mask & ~erode(mask)
            s.col[e] = olc if olc is not None else mix(pal[0], INK, 0.55)
        return mask

    def ell(s, cx, cy, rx, ry, pal, ang=0.0, flat=0.0, ol=True, olc=None, dither=None, clip=None, gloss=0.0, frost=True):
        m, nx, ny = s.m_ell(cx, cy, rx, ry, ang)
        if clip is not None: m = m & clip
        return s.paint(m, pal, DX.lit(nx, ny, flat), ol=ol, olc=olc, gloss=gloss, frost=frost)

    def sup(s, cx, cy, rx, ry, pal, n=2.6, flat=0.0, ol=True, olc=None, clip=None, gloss=0.0, frost=True):
        m, nx, ny = s.m_super(cx, cy, rx, ry, n)
        if clip is not None: m = m & clip
        return s.paint(m, pal, DX.lit(nx * 0.92, ny * 0.92, flat), ol=ol, olc=olc, gloss=gloss, frost=frost)

    def cap(s, a, b, r0, r1, pal, flat=0.0, ol=True, olc=None, clip=None, gloss=0.0, frost=True):
        m, nx, ny = s.m_cap(a, b, r0, r1)
        if clip is not None: m = m & clip
        return s.paint(m, pal, DX.lit(nx, ny, flat), ol=ol, olc=olc, gloss=gloss, frost=frost)

    def union(s, parts, pal, flat=0.0, ol=True, olc=None, dither=None, exclude=None, gloss=0.0, frost=True):
        M = np.zeros((s.H, s.W), bool); V = np.full((s.H, s.W), -1.0, np.float32); Z = np.full((s.H, s.W), -1.0, np.float32)
        for m, nx, ny in parts:
            nz = np.sqrt(np.clip(1.0 - nx * nx - ny * ny, 0.0, 1.0))
            take = m & (nz > Z)
            V[take] = DX.lit(nx * 0.92, ny * 0.92, flat)[take]; Z[take] = nz[take]; M |= m
        if exclude is not None: M &= ~exclude
        return s.paint(M, pal, V, ol=ol, olc=olc, gloss=gloss, frost=frost)

    def poly(s, pts, pal, val=None, ol=True, olc=None, grad=None, frost=True):
        m = s.m_poly(pts)
        if grad is not None:
            y0, y1 = grad
            val = np.clip((DX.YC - y1) / max(1e-3, (y0 - y1)), 0, 1) * 0.7 + 0.15 - (DX.XC * 0.006)
        return s.paint(m, pal, val, ol=ol, olc=olc, frost=frost)

    def glint(s, x, y, r=1.0, col=WHITE):
        """icy glint: a tiny 4-point star"""
        TX.thin(s, (x - r, y), (x + r, y), col, 0.16, keep=True)
        TX.thin(s, (x, y - r), (x, y + r), col, 0.16, keep=True)
        s.blob(x, y, 0.32, col, keep=True)

    def outline(s, c=INK, w=1):
        TX.Spr.outline(s, c, w)

    def rim(s, top=SNOWRIM, side=SUN, a=0.58, side_a=0.50):
        """dual rim on the SILHOUETTE: the top edge glows snow-white-blue (the snow plain lights everything), the left edge glows
        sunrise orange, 1 sprite px wide. Eye whites / teeth (keep) stay clean. Call before outline()."""
        m = s.m; k = s.k
        def edge(dy, dx):
            nb = m.copy()
            for q in range(1, k + 1): nb &= np.roll(np.roll(m, dy * q, 0), dx * q, 1)
            return m & ~nb & ~s.keep
        col = s.col.astype(np.float32)
        for msk, c, aa in ((edge(1, 0), top, a), (edge(0, 1), side, side_a)):
            if c is None or not msk.any(): continue
            col[msk] = col[msk] * (1 - aa) + np.array(c, np.float32) * aa
        s.col = np.clip(col, 0, 255).astype(np.uint8)


thin, stroke = TX.thin, TX.stroke


class Act(DX.Act):
    """direct-draw actor: paints a zampix Spr under the frosty sky light, adds the dual rim (snow + sun) and the ink outline,
    then blits it like dibspix.Act. rim=(top_colour, side_colour), None = no rim. The sun side rim follows the flip."""
    def __init__(s, fn, wx, wy, s_=None, rim=(SNOWRIM, SUN), **kw):
        s.rimc = rim
        DX.Act.__init__(s, fn, wx, wy, s_=s_, **kw)

    def __call__(s, big, v, lt):
        sc = s.scale(v)
        with res(res_for(sc, s.hires)), sky_light():
            sp = Spr()
            sp.mirror_text = s.flip
            s.fn(sp, **s.P)
            if s.post: s.post(sp)
            if s.rimc: sp.rim(*s.rimc)
            if not getattr(sp, 'no_outline', False): sp.outline(INK, 1)
            if s.rot: rotate(sp, s.rot, s.pivot)
        ox, oy = v.opt(s.wx, s.wy)
        if s.pin:
            px, py = sp.anchors[s.pin]
            ox -= (-px if s.flip else px) * sc; oy += py * sc
        blit(big, sp, ox, oy, sc, lt, s.flip, s.alpha, s.ghost, s.shadow)
        s.last = sp


def draw(fn, s=6.0, flip=False, hires=None, rim=(SNOWRIM, SUN), rot=0.0, pivot=(0.0, 0.0), **P_):
    with res(res_for(s, hires)), sky_light():
        sp = Spr(); sp.mirror_text = flip
        fn(sp, **P_)
        if rim: sp.rim(*rim)
        if not getattr(sp, 'no_outline', False): sp.outline(INK, 1)
        if rot: rotate(sp, rot, pivot)
    return sp


def render(fn, s=6, bg=(150, 176, 210), size=(1080, 1920), at=None, flip=False, **P_):
    big = np.zeros((size[1], size[0], 3), np.uint8); big[:] = bg
    sp = draw(fn, s, flip=flip, **P_)
    ox, oy = at or (size[0] // 2, size[1] - 60)
    blit(big, sp, ox, oy, s, None, flip)
    return big
