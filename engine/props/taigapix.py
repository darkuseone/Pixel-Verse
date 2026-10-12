"""«Прохор. Таёжные лайфхаки» — sprite manner «Морозный лубок» (see series/prokhor/design/philosophy.md).
Same sprite canvas / IK / face kit / blit as props/dibspix.py (one sprite px = one visible square, 2x..6x for close-ups), but its own look:
  * 3 flat tones per material with HARD edges, no dithering (a painted lubok / folk toy), shadows sink into cold violet-blue,
    the lit side warms to the low orange winter sun;
  * the key light is the LOW winter sun from the LEFT (long side light), and every downward-facing surface catches a pale blue
    SNOW BOUNCE rim — heroes always stand in snow, the snow lights them from below;
  * fur (beard, ushanka, the bear) is drawn with short flick strokes, quilting with stitch rows; frost specks on brows and beards;
  * spruce-night ink outline (dark green-black), 1 sprite px.
Usage: Act(fn, wx, wy, s_=.., **params) exactly like dibspix.Act (chikit.shot treats it as a direct actor)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from props import dibspix as DX
from props.dibspix import dark, mix, erode, dilate, ik, EXPR, res, res_for, blit, rotate
import paths as P

INK = (16, 32, 32)                                     # spruce-night ink
LDIR_LOW = np.array([-0.74, 0.30, 0.60], np.float32)   # low winter sun from the left
SNOW = (200, 228, 255)                                 # snow bounce from below
FROST = (236, 246, 255)
WHITE = (250, 250, 244)


class low_sun:
    """the shared dibspix lit() reads DX.LDIR at call time: swap it while a «Прохор» sprite is being drawn"""
    def __enter__(s): s.prev = DX.LDIR; DX.LDIR = LDIR_LOW; return s
    def __exit__(s, *a): DX.LDIR = s.prev


def tones(base, k=0.30):
    """3-tone ramp (shadow, base, light): shadow cold violet-blue (snow dusk), light warm (low sun)"""
    b = np.array(base, np.float32)
    d = b * 0.50 + np.array((8, 14, 44))
    l = b + (255 - b) * k + np.array((16, 6, -12))
    return [tuple(int(v) for v in np.clip(x, 0, 255)) for x in (d, b, l)]


class Spr(DX.Spr):
    def dot(s, i, j, c, keep=False):
        """detail dot: a hard sprite px at 1-2x, a small round blob at hi-res (no square «mush» specks in close-ups)"""
        if s.k < 3: return DX.Spr.dot(s, i, j, c, keep)
        s.blob(int(i) + 0.5, int(j) + 0.5, 0.58, c, keep=keep)

    # ---- fast local rasterisers (bbox only; the full-canvas masks of dibspix are too slow for hundreds of tiny marks at 5-6x)
    def _put(s, y0, x0, m, c, keep):
        sub = s.col[y0:y0 + m.shape[0], x0:x0 + m.shape[1]]
        sub[m] = c
        s.m[y0:y0 + m.shape[0], x0:x0 + m.shape[1]] |= m
        kk = s.keep[y0:y0 + m.shape[0], x0:x0 + m.shape[1]]; kk[m] = keep

    def blob(s, x, y, r, c, mask=None, keep=False):
        k = s.k; cx = s.OX + x * k; cy = s.OY - y * k; R = max(0.5, r * k)
        x0, x1 = int(max(0, cx - R - 1)), int(min(s.W, cx + R + 2)); y0, y1 = int(max(0, cy - R - 1)), int(min(s.H, cy + R + 2))
        if x0 >= x1 or y0 >= y1: return
        yy, xx = np.mgrid[y0:y1, x0:x1]
        m = (xx + 0.5 - cx) ** 2 + (yy + 0.5 - cy) ** 2 <= R * R
        if mask is not None: m &= mask[y0:y1, x0:x1]
        s._put(y0, x0, m, c, keep)

    def seg(s, a, b, w, c, mask=None, keep=False):
        k = s.k
        ax, ay = s.OX + a[0] * k, s.OY - a[1] * k; bx, by = s.OX + b[0] * k, s.OY - b[1] * k
        R = max(0.5, w * k)
        x0, x1 = int(max(0, min(ax, bx) - R - 1)), int(min(s.W, max(ax, bx) + R + 2))
        y0, y1 = int(max(0, min(ay, by) - R - 1)), int(min(s.H, max(ay, by) + R + 2))
        if x0 >= x1 or y0 >= y1: return
        yy, xx = np.mgrid[y0:y1, x0:x1]
        px, py = xx + 0.5 - ax, yy + 0.5 - ay; dx, dy = bx - ax, by - ay
        L = dx * dx + dy * dy
        u = np.clip((px * dx + py * dy) / L, 0, 1) if L > 0 else np.zeros(px.shape)
        m = (px - u * dx) ** 2 + (py - u * dy) ** 2 <= R * R
        if mask is not None: m &= mask[y0:y1, x0:x1]
        s._put(y0, x0, m, c, keep)

    def paint(s, mask, pal, val=None, dither=None, bands=(0.30, 0.74), ol=True, olc=None, bounce=None, gloss=0.0):
        if not mask.any(): return mask
        pal = list(pal)
        if len(pal) == 4: pal = [pal[0], pal[2], pal[3]]
        if len(pal) == 2: pal = [pal[0], pal[1], pal[1]]
        if len(pal) == 1: pal = [dark(pal[0], 0.6), pal[0], pal[0]]
        Pp = np.array(pal, np.uint8)
        if val is None:
            idx = np.ones(mask.shape, np.int32)
        else:
            idx = np.searchsorted(np.array(bands, np.float32), np.asarray(val, np.float32)).astype(np.int32)
        s.col[mask] = Pp[np.clip(idx, 0, 2)[mask]]
        if bounce is not None:
            b = mask & bounce
            s.col[b] = (s.col[b].astype(np.float32) * 0.45 + np.array(SNOW, np.float32) * 0.55).astype(np.uint8)
        if gloss and val is not None:
            g = mask & (np.asarray(val, np.float32) > 1.0 - gloss * 0.10)
            s.col[g] = WHITE
        s.m |= mask
        s.keep[mask] = False
        if ol:
            e = mask & ~erode(mask)
            s.col[e] = olc if olc is not None else mix(pal[0], INK, 0.6)
        return mask

    @staticmethod
    def _bounce(ny, m):
        return m & (ny < -0.62)

    def ell(s, cx, cy, rx, ry, pal, ang=0.0, flat=0.0, ol=True, olc=None, dither=None, clip=None, gloss=0.0, snow=True):
        m, nx, ny = s.m_ell(cx, cy, rx, ry, ang)
        if clip is not None: m = m & clip
        return s.paint(m, pal, DX.lit(nx, ny, flat), ol=ol, olc=olc, bounce=s._bounce(ny, m) if snow else None, gloss=gloss)

    def sup(s, cx, cy, rx, ry, pal, n=2.6, flat=0.0, ol=True, olc=None, clip=None, gloss=0.0, snow=True):
        m, nx, ny = s.m_super(cx, cy, rx, ry, n)
        if clip is not None: m = m & clip
        return s.paint(m, pal, DX.lit(nx * 0.92, ny * 0.92, flat), ol=ol, olc=olc, bounce=s._bounce(ny, m) if snow else None, gloss=gloss)

    def cap(s, a, b, r0, r1, pal, flat=0.0, ol=True, olc=None, clip=None, gloss=0.0, snow=True):
        m, nx, ny = s.m_cap(a, b, r0, r1)
        if clip is not None: m = m & clip
        return s.paint(m, pal, DX.lit(nx, ny, flat), ol=ol, olc=olc, bounce=s._bounce(ny, m) if snow else None, gloss=gloss)

    def union(s, parts, pal, flat=0.0, ol=True, olc=None, dither=None, exclude=None, gloss=0.0, snow=True):
        M = np.zeros((s.H, s.W), bool); V = np.full((s.H, s.W), -1.0, np.float32); Z = np.full((s.H, s.W), -1.0, np.float32)
        NY = np.zeros((s.H, s.W), np.float32)
        for m, nx, ny in parts:
            nz = np.sqrt(np.clip(1.0 - nx * nx - ny * ny, 0.0, 1.0))
            take = m & (nz > Z)
            V[take] = DX.lit(nx * 0.92, ny * 0.92, flat)[take]; Z[take] = nz[take]; NY[take] = ny[take]; M |= m
        if exclude is not None: M &= ~exclude
        return s.paint(M, pal, V, ol=ol, olc=olc, bounce=s._bounce(NY, M) if snow else None, gloss=gloss)

    def outline(s, c=INK, w=1):
        o = s.m.copy()
        for _ in range(w * s.k): o = dilate(o)
        o &= ~s.m
        s.col[o] = c; s.m |= o

    def fur(s, mask, col, step=2.2, ln=1.6, ang=-1.9, seed=1, w=0.28, keep=False):
        """short flick strokes over a fur mass (beard, ushanka, the bear): fixed in sprite px, never boil between frames"""
        rng = np.random.default_rng(seed)
        ys, xs = np.nonzero(mask[::max(1, int(step * s.k)), ::max(1, int(step * s.k))])
        if not len(xs): return
        q = max(1, int(step * s.k))
        for r_, c_ in zip(ys, xs):
            x = (c_ * q - s.OX + 0.5) / s.k + (rng.random() - 0.5) * step
            y = (s.OY - r_ * q - 0.5) / s.k + (rng.random() - 0.5) * step
            a = ang + (rng.random() - 0.5) * 0.6
            b = (x + math.cos(a) * ln, y + math.sin(a) * ln)
            s.seg((x, y), b, w, col, mask, keep)

    def frost(s, mask, density=0.12, seed=4):
        """frost specks (hoarfrost) on brows, beard, ushanka"""
        rng = np.random.default_rng(seed)
        ys, xs = np.nonzero(mask)
        if not len(xs): return
        n = max(1, int(len(xs) * density / max(1, s.k * s.k)))
        for i in rng.choice(len(xs), min(n, len(xs)), replace=False):
            x = (xs[i] - s.OX + 0.5) / s.k; y = (s.OY - ys[i] - 0.5) / s.k
            if s.k < 3: DX.Spr.dot(s, x, y, FROST)
            else: s.blob(x, y, 0.36, FROST)

    def ptext(s, txt, i0, j0, col, size=8, keep=False, center=False):
        """Press Start 2P text (Cyrillic) at sprite resolution: glyph cell = `size` sprite px; (i0, j0) top-left (or top-centre)"""
        f = ImageFont.truetype(P.FONT_PX, max(4, int(size * s.k)))
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

    def txt_box(s, lines, box, col, alt=(), pad=0.4, keep=True, scribble=None, lead=0.35):
        """Cyrillic text FITTED into a plate (rule 10.10.2026): box = (x0, y0, x1, y1) sprite px, y up. Press Start 2P at the biggest
        canvas size that fits inside box minus pad, centred; if even 6 canvas px do not fit, alt variants, then grey «small print» dashes"""
        x0, y0, x1, y1 = box
        aw, ah = (x1 - x0 - 2 * pad) * s.k, (y1 - y0 - 2 * pad) * s.k
        for cand in (lines,) + tuple(alt):
            cand = [cand] if isinstance(cand, str) else list(cand)
            best = None
            for size in range(int(min(ah, 200)), 5, -1):
                f = ImageFont.truetype(P.FONT_PX, size)
                w_ = max(f.getlength(l) for l in cand); h_ = size * len(cand) + int(size * lead) * (len(cand) - 1)
                if w_ <= aw and h_ <= ah: best = (size, f); break
            if best: break
        else:
            sc = scribble or mix(col, (200, 200, 200), 0.5)
            cy = (y0 + y1) / 2
            nrow = max(1, int((y1 - y0 - 2 * pad) // 1.6))
            for q in range(min(nrow, 3)):
                yy = cy + (q - (min(nrow, 3) - 1) / 2) * 1.6
                s.line((x0 + pad + 0.3, yy), (x1 - pad - 0.8 - (q % 2) * 1.5, yy), sc)
            return 0
        size, f = best
        H_ = size * len(cand) + int(size * lead) * (len(cand) - 1)
        img = Image.new('L', (int(aw) + 4, H_ + 4), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        y = 2
        for l in cand:
            d.text(((aw + 4 - f.getlength(l)) / 2, y), l, font=f, fill=255)
            y += size + int(size * lead)
        m = np.array(img) > 127
        if s.mirror_text: m = m[:, ::-1]
        ys, xs = np.nonzero(m)
        cxc = (x0 + x1) / 2 * s.k; cyc = (y0 + y1) / 2 * s.k
        cc = (s.OX + cxc - (aw + 4) / 2 + xs).astype(int)
        rr = (s.OY - cyc - (H_ + 4) / 2 + ys).astype(int)
        ok = (cc >= 0) & (cc < s.W) & (rr >= 0) & (rr < s.H)
        s.col[rr[ok], cc[ok]] = col; s.m[rr[ok], cc[ok]] = True; s.keep[rr[ok], cc[ok]] = keep
        return size


def thin(sp, a, b, c, w=0.3, keep=False, mask=None):
    """a stroke w sprite px thick (thinner than sp.line at hi-res: wrinkles, strings, cracks); fast local raster"""
    sp.seg(a, b, w, c, mask, keep)


def stroke(sp, pts, c=INK, w=0.3):
    for a, b in zip(pts[:-1], pts[1:]): thin(sp, a, b, c, w)


class Act(DX.Act):
    """direct-draw actor (chikit.shot): paints a taigapix Spr under the low winter sun, then blits it like dibspix.Act"""
    def __call__(s, big, v, lt):
        sc = s.scale(v)
        with res(res_for(sc, s.hires)), low_sun():
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
    with res(res_for(s, hires)), low_sun():
        sp = Spr(); sp.mirror_text = flip
        fn(sp, **P_)
        if rot: rotate(sp, rot, pivot)
    return sp


def render(fn, s=6, bg=(90, 110, 140), size=(1080, 1920), at=None, flip=False, **P_):
    big = np.zeros((size[1], size[0], 3), np.uint8); big[:] = bg
    sp = draw(fn, s, flip=flip, **P_)
    ox, oy = at or (size[0] // 2, size[1] - 60)
    blit(big, sp, ox, oy, s, None, flip)
    return big
