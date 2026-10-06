"""«Мазутыч» — sprite manner «Мазутная гравюра» (see series/mazutych/design/philosophy.md).
Same sprite canvas / IK / face kit / blit as props/dibspix.py (one sprite px = one visible square, 2x/3x for close-ups), but its own look:
  * 3 tones per material, NO dithering: the shadow band is 45° ink HATCHING (linocut / satirical-magazine cartoon), deep shadow solid;
  * warm crude-oil ink lines: every part outlined in INK, the whole figure in a double (2 sprite px) INK outline;
  * key light from the UPPER RIGHT (the refinery flare), narrow «oil sheen» highlight streaks.
Usage: Act(fn, wx, wy, s_=.., **params) exactly like dibspix.Act (chikit.shot treats it as a direct actor)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from props import dibspix as DX
from props.dibspix import dark, mix, erode, dilate, ik, EXPR, res, res_for, blit, rotate
import paths as P

INK = (30, 20, 16)                  # crude-oil black, warm
LDIR_R = np.array([0.56, 0.58, 0.60], np.float32)     # light from the upper right (the flare)
WHITE = (250, 244, 228)


class light_right:
    """the shared dibspix lit() reads DX.LDIR at call time: swap it while a Мазутыч sprite is being drawn"""
    def __enter__(s): s.prev = DX.LDIR; DX.LDIR = LDIR_R; return s
    def __exit__(s, *a): DX.LDIR = s.prev


def tones(base, k=0.34):
    """3-tone ramp (shadow, base, light): shadow cooler and purple-ish (dusk sky), light warmer (sodium / flare)"""
    b = np.array(base, np.float32)
    d = b * 0.52 + np.array((14, 4, 26))
    l = b + (255 - b) * k + np.array((10, 4, -10))
    return [tuple(int(v) for v in np.clip(x, 0, 255)) for x in (d, b, l)]


def hatch_mask(step=3):
    """45° hatch lines, one sprite px wide, every `step` sprite px (constant in sprite px at any resolution)"""
    return ((np.floor(DX.XC) + np.floor(DX.YC)) % step) == 0


class Spr(DX.Spr):
    def paint(s, mask, pal, val=None, dither=None, bands=(0.24, 0.44, 0.86), ol=True, olc=None, sheen=True):
        if not mask.any(): return mask
        pal = list(pal)
        if len(pal) == 4: pal = [pal[0], pal[2], pal[3]]                 # accept 4-tone ramps from shared helpers
        if len(pal) == 2: pal = [pal[0], pal[1], pal[1]]
        if len(pal) == 1: pal = [dark(pal[0], 0.6), pal[0], pal[0]]
        d, b, l = (np.array(c, np.uint8) for c in pal)
        if val is None:
            s.col[mask] = b
        else:
            v = np.asarray(val, np.float32)
            out = np.empty(mask.shape + (3,), np.uint8); out[:] = b
            deep = v < bands[0]
            mid = (v >= bands[0]) & (v < bands[1])
            out[deep] = d
            out[mid & hatch_mask(3)] = d
            out[(v >= bands[1]) & (v < bands[1] + 0.05) & hatch_mask(5)] = d     # a few lone strokes where the shadow fades out
            if sheen: out[v >= bands[2]] = l
            s.col[mask] = out[mask]
        s.m |= mask
        s.keep[mask] = False
        if ol:
            e = mask & ~erode(mask)
            s.col[e] = olc if olc is not None else INK
        return mask

    def outline(s, c=INK, w=2):
        """double outer ink line (w sprite px)"""
        m = s.m
        o = m.copy()
        for _ in range(w * s.k): o = dilate(o)
        o &= ~m
        s.col[o] = c; s.m |= o

    def ptext(s, txt, i0, j0, col, size=8, keep=False, center=False):
        """Press Start 2P text (Cyrillic) rasterised at sprite resolution: glyph cells are `size` sprite px; (i0, j0) = top-left
        (or top-centre if center); drawn pre-mirrored when the sprite will be flipped"""
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
    """polyline of ink strokes (sprite px)"""
    for a, b in zip(pts[:-1], pts[1:]): sp.line(a, b, c, th)


def hatch_fill(sp, mask, c=INK, step=3):
    sp.fill(mask & hatch_mask(step), c)


class Act(DX.Act):
    """direct-draw actor (chikit.shot): paints a mazpix Spr with the right-hand key light, then blits it like dibspix.Act"""
    def __call__(s, big, v, lt):
        sc = s.scale(v)
        with res(res_for(sc, s.hires)), light_right():
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


def draw(fn, s=6.0, flip=False, hires=None, **P_):
    with res(res_for(s, hires)), light_right():
        sp = Spr(); sp.mirror_text = flip
        fn(sp, **P_)
    return sp


def render(fn, s=6, bg=(60, 50, 70), size=(1080, 1920), at=None, flip=False, **P_):
    big = np.zeros((size[1], size[0], 3), np.uint8); big[:] = bg
    sp = draw(fn, s, flip=flip, **P_)
    ox, oy = at or (size[0] // 2, size[1] - 60)
    blit(big, sp, ox, oy, s, None, flip)
    return big
