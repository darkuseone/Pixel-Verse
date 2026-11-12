"""«STILL 1986» — sprite manner «Sunset Chrome» (series/still-1986/design/philosophy.md).
Same sprite canvas / IK / face kit / blit as props/dibspix.py (one sprite px = one visible square, 2x..6x for close-ups) and the fast
local rasterisers + fitted Press Start 2P text of props/taigapix.Spr, but its own look:
  * key light = the LOW SUNSET from the left (warm peach on the lit side), shadows sink into indigo / aubergine;
  * tone borders break into thin horizontal «blinds» (retro sunset stripes / chrome), not dither, not frost, not hatching;
  * every hero gets a DUAL RIM after drawing: the sunset side of the silhouette glows peach, the far side glows neon (cyan or
    magenta) — the volume of 2.5D inside the sprite itself (Act(rim=...));
  * chrome / glass highlights: white with a tiny cross star; deep indigo ink outline, 1 sprite px.
Usage: Act(fn, wx, wy, s_=.., rim=(sun, neon) | None, **params) like dibspix.Act (chikit.shot / depth25.shot25 direct actor)."""
import numpy as np
from props import dibspix as DX
from props import taigapix as TX
from props.dibspix import dark, mix, erode, dilate, res, res_for, blit, rotate

INK = (28, 18, 64)                                      # deep indigo ink
LDIR_SUN = np.array([-0.66, 0.36, 0.66], np.float32)    # low sunset from the left
SUN = (255, 178, 120)                                   # sunset rim
CYAN = (90, 236, 255)                                   # neon rims
PINK = (255, 90, 200)
WHITE = (255, 252, 246)
_BL = {}


def tones(base, k=0.32):
    """3-tone ramp (shadow, base, light): shadow indigo-aubergine, light warm sunset peach"""
    b = np.array(base, np.float32)
    d = b * 0.52 + np.array((18, 6, 46))
    l = b + (255 - b) * k + np.array((20, 6, -16))
    return [tuple(int(v) for v in np.clip(x, 0, 255)) for x in (d, b, l)]


def blinds(shape, k):
    """horizontal stripes: every other sprite-px row (k canvas px thick), fixed in the canvas -> no boiling between frames"""
    key = (shape, k)
    if key not in _BL:
        rr = np.arange(shape[0])[:, None]
        _BL[key] = np.broadcast_to(((rr // max(1, k)) % 2) == 0, shape).copy()
    return _BL[key]


class sunset_light:
    """the shared dibspix lit() reads DX.LDIR at call time: swap it while a «STILL 1986» sprite is being drawn"""
    def __enter__(s): s.prev = DX.LDIR; DX.LDIR = LDIR_SUN; return s
    def __exit__(s, *a): DX.LDIR = s.prev


class Spr(TX.Spr):
    def paint(s, mask, pal, val=None, dither=None, bands=(0.30, 0.70), ol=True, olc=None, bounce=None, gloss=0.0, stripes=True):
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
            if stripes:                                                    # sunset blinds across each tone border
                bl = blinds(mask.shape, s.k)
                for b in bands:
                    idx[(v >= b) & (v < b + 0.10) & bl] -= 1
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

    def ell(s, cx, cy, rx, ry, pal, ang=0.0, flat=0.0, ol=True, olc=None, dither=None, clip=None, gloss=0.0, stripes=True):
        m, nx, ny = s.m_ell(cx, cy, rx, ry, ang)
        if clip is not None: m = m & clip
        return s.paint(m, pal, DX.lit(nx, ny, flat), ol=ol, olc=olc, gloss=gloss, stripes=stripes)

    def sup(s, cx, cy, rx, ry, pal, n=2.6, flat=0.0, ol=True, olc=None, clip=None, gloss=0.0, stripes=True):
        m, nx, ny = s.m_super(cx, cy, rx, ry, n)
        if clip is not None: m = m & clip
        return s.paint(m, pal, DX.lit(nx * 0.92, ny * 0.92, flat), ol=ol, olc=olc, gloss=gloss, stripes=stripes)

    def cap(s, a, b, r0, r1, pal, flat=0.0, ol=True, olc=None, clip=None, gloss=0.0, stripes=True):
        m, nx, ny = s.m_cap(a, b, r0, r1)
        if clip is not None: m = m & clip
        return s.paint(m, pal, DX.lit(nx, ny, flat), ol=ol, olc=olc, gloss=gloss, stripes=stripes)

    def union(s, parts, pal, flat=0.0, ol=True, olc=None, dither=None, exclude=None, gloss=0.0, stripes=True):
        M = np.zeros((s.H, s.W), bool); V = np.full((s.H, s.W), -1.0, np.float32); Z = np.full((s.H, s.W), -1.0, np.float32)
        for m, nx, ny in parts:
            nz = np.sqrt(np.clip(1.0 - nx * nx - ny * ny, 0.0, 1.0))
            take = m & (nz > Z)
            V[take] = DX.lit(nx * 0.92, ny * 0.92, flat)[take]; Z[take] = nz[take]; M |= m
        if exclude is not None: M &= ~exclude
        return s.paint(M, pal, V, ol=ol, olc=olc, gloss=gloss, stripes=stripes)

    def poly(s, pts, pal, val=None, ol=True, olc=None, grad=None, stripes=True):
        m = s.m_poly(pts)
        if grad is not None:
            y0, y1 = grad
            val = np.clip((DX.YC - y1) / max(1e-3, (y0 - y1)), 0, 1) * 0.7 + 0.15 - (DX.XC * 0.006)
        return s.paint(m, pal, val, ol=ol, olc=olc, stripes=stripes)

    def star(s, x, y, r=1.0, col=WHITE):
        """chrome / glass glint: a tiny 4-point star"""
        TX.thin(s, (x - r, y), (x + r, y), col, 0.16, keep=True)
        TX.thin(s, (x, y - r), (x, y + r), col, 0.16, keep=True)
        s.blob(x, y, 0.32, col, keep=True)

    def outline(s, c=INK, w=1):
        TX.Spr.outline(s, c, w)

    def rim(s, left=SUN, right=CYAN, a=0.62, top=0.35):
        """dual rim light on the SILHOUETTE: the left edge (sunset side) and the right edge (neon side), 1 sprite px wide;
        the top edge gets a softer sunset glow. Eye whites / teeth (keep) stay clean. Call before outline()."""
        m = s.m; k = s.k
        def edge(dy, dx):
            nb = m.copy()
            for q in range(1, k + 1): nb &= np.roll(np.roll(m, dy * q, 0), dx * q, 1)
            return m & ~nb & ~s.keep
        col = s.col.astype(np.float32)
        for msk, c, aa in ((edge(1, 0), left, a * top), (edge(0, 1), left, a), (edge(0, -1), right, a)):
            if c is None or not msk.any(): continue
            col[msk] = col[msk] * (1 - aa) + np.array(c, np.float32) * aa
        s.col = np.clip(col, 0, 255).astype(np.uint8)


thin, stroke = TX.thin, TX.stroke


class Act(DX.Act):
    """direct-draw actor: paints a v86pix Spr under the sunset key light, adds the dual rim (sunset + neon) and the ink outline,
    then blits it like dibspix.Act. rim=(left_colour, right_colour) in SCREEN terms (swapped for flipped sprites), None = no rim."""
    def __init__(s, fn, wx, wy, s_=None, rim=(SUN, CYAN), **kw):
        s.rimc = rim
        DX.Act.__init__(s, fn, wx, wy, s_=s_, **kw)

    def __call__(s, big, v, lt):
        sc = s.scale(v)
        with res(res_for(sc, s.hires)), sunset_light():
            sp = Spr()
            sp.mirror_text = s.flip
            s.fn(sp, **s.P)
            if s.post: s.post(sp)
            if s.rimc:
                l, r = s.rimc
                if s.flip: l, r = r, l
                sp.rim(l, r)
            if not getattr(sp, 'no_outline', False): sp.outline(INK, 1)
            if s.rot: rotate(sp, s.rot, s.pivot)
        ox, oy = v.opt(s.wx, s.wy)
        if s.pin:
            px, py = sp.anchors[s.pin]
            ox -= (-px if s.flip else px) * sc; oy += py * sc
        blit(big, sp, ox, oy, sc, lt, s.flip, s.alpha, s.ghost, s.shadow)
        s.last = sp


def draw(fn, s=6.0, flip=False, hires=None, rim=(SUN, CYAN), rot=0.0, pivot=(0.0, 0.0), **P_):
    with res(res_for(s, hires)), sunset_light():
        sp = Spr(); sp.mirror_text = flip
        fn(sp, **P_)
        if rim:
            l, r = rim
            if flip: l, r = r, l
            sp.rim(l, r)
        if not getattr(sp, 'no_outline', False): sp.outline(INK, 1)
        if rot: rotate(sp, rot, pivot)
    return sp


def render(fn, s=6, bg=(40, 30, 70), size=(1080, 1920), at=None, flip=False, **P_):
    big = np.zeros((size[1], size[0], 3), np.uint8); big[:] = bg
    sp = draw(fn, s, flip=flip, **P_)
    ox, oy = at or (size[0] // 2, size[1] - 60)
    blit(big, sp, ox, oy, s, None, flip)
    return big
