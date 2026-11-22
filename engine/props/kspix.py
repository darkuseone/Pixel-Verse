"""«Ключевой сотрудник» — sprite manner «Дневной свет» (series/klyuchevoy/design/philosophy.md).
Same sprite canvas / IK / face kit / blit as props/dibspix.py (one sprite px = one visible square, 2x..6x for close-ups) and the
local rasterisers + fitted text of props/taigapix.Spr, but its own office look:
  * key light = the FLUORESCENT TUBE overhead (flat, a little green), shadows sink into olive-brown linoleum tones;
  * tone borders break into sparse «toner specks» (a photocopy of a photocopy), fixed on the canvas -> no boiling;
  * a DUAL RIM after drawing: the desk-lamp side glows amber, the far side glows monitor-cyan (Act(rim=...));
  * glass / bald-spot highlight = one clean white square; coffee-brown ink outline, 1 sprite px.
Usage: Act(fn, wx, wy, s_=.., rim=(lamp, monitor) | None, **params) like dibspix.Act."""
import numpy as np
from props import dibspix as DX
from props import taigapix as TX
from props.dibspix import dark, mix, erode, dilate, res, res_for, blit, rotate

INK = (40, 30, 26)                                      # coffee-brown ink
LDIR_TUBE = np.array([-0.22, 0.80, 0.56], np.float32)   # the tube is overhead, a little to the left
LAMP = (255, 196, 110)                                  # desk lamp rim (amber)
MONI = (120, 236, 230)                                  # monitor rim (cyan)
WHITE = (252, 252, 244)
_SP = {}


def tones(base, k=0.30):
    """3-tone ramp (shadow, base, light): shadow olive-brown, light pale fluorescent"""
    b = np.array(base, np.float32)
    d = b * 0.54 + np.array((22, 18, 6))
    l = b + (255 - b) * k + np.array((-2, 10, 4))
    return [tuple(int(v) for v in np.clip(x, 0, 255)) for x in (d, b, l)]


def specks(shape, k):
    """sparse toner specks: ~1 of 3 sprite px on a fixed hash grid (k canvas px per sprite px) — no boiling between frames"""
    key = (shape, k)
    if key not in _SP:
        rr = np.arange(shape[0])[:, None] // max(1, k)
        cc = np.arange(shape[1])[None, :] // max(1, k)
        h = (rr * 73856093 ^ cc * 19349663) % 7
        _SP[key] = np.broadcast_to((h == 0) | (h == 3), shape).copy()
    return _SP[key]


class tube_light:
    """dibspix.lit() reads DX.LDIR at call time: swap it while a «Ключевой сотрудник» sprite is drawn"""
    def __enter__(s): s.prev = DX.LDIR; DX.LDIR = LDIR_TUBE; return s
    def __exit__(s, *a): DX.LDIR = s.prev


class Spr(TX.Spr):
    def paint(s, mask, pal, val=None, dither=None, bands=(0.30, 0.68), ol=True, olc=None, bounce=None, gloss=0.0, stripes=True):
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
            if stripes:                                                    # toner specks scattered over each tone border
                sp_ = specks(mask.shape, s.k)
                for b in bands:
                    idx[(v >= b) & (v < b + 0.12) & sp_] -= 1
                    idx[(v < b) & (v > b - 0.06) & sp_] += 1
        s.col[mask] = Pp[np.clip(idx, 0, 2)[mask]]
        if gloss and val is not None:
            g = mask & (np.asarray(val, np.float32) > 1.0 - gloss * 0.09)
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

    def glint(s, x, y, r=0.5, col=WHITE):
        """one clean white square (glass, bald spot, watch)"""
        s.fill(s.m_super(x, y, r, r, 8.0)[0], col, keep=True)

    def outline(s, c=INK, w=1):
        TX.Spr.outline(s, c, w)

    def rim(s, left=LAMP, right=MONI, a=0.55, top=0.30):
        """dual rim on the SILHOUETTE: left edge amber (desk lamp), right edge cyan (monitor), top edge a soft amber.
        Eye whites / teeth (keep) stay clean. Call before outline()."""
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
    """direct-draw actor: paints a kspix Spr under the tube light, adds the dual rim and the ink outline, blits like dibspix.Act.
    rim=(left, right) in SCREEN terms (swapped for flipped sprites), None = no rim."""
    def __init__(s, fn, wx, wy, s_=None, rim=(LAMP, MONI), **kw):
        s.rimc = rim
        DX.Act.__init__(s, fn, wx, wy, s_=s_, **kw)

    def __call__(s, big, v, lt):
        sc = s.scale(v)
        with res(res_for(sc, s.hires)), tube_light():
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


def draw(fn, s=6.0, flip=False, hires=None, rim=(LAMP, MONI), rot=0.0, pivot=(0.0, 0.0), **P_):
    with res(res_for(s, hires)), tube_light():
        sp = Spr(); sp.mirror_text = flip
        fn(sp, **P_)
        if rim:
            l, r = rim
            if flip: l, r = r, l
            sp.rim(l, r)
        if not getattr(sp, 'no_outline', False): sp.outline(INK, 1)
        if rot: rotate(sp, rot, pivot)
    return sp
