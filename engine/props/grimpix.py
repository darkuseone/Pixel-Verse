"""«Grim Ride» — sprite manner «Lantern Stipple» (see series/grim-ride/design/philosophy.md).
Same sprite canvas / IK / face kit / blit as props/dibspix.py (one sprite px = one visible square, 2x/3x for close-ups), but its own look:
  * 4 tones per material (violet depth, shadow, base, warm glow) with STIPPLE transitions: white-noise dots fixed to the canvas pixel
    (a 1950s horror-comic / old bestiary engraving look), never ordered Bayer and never hatching;
  * the key light comes from BELOW-front (a jack-o'-lantern held under the chin), the scene Light adds a cold moon rim from above;
  * violet-black outline, the whole figure in a 1-sprite-px outer line.
Usage: Act(fn, wx, wy, s_=.., **params) exactly like dibspix.Act (chikit.shot treats it as a direct actor)."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from props import dibspix as DX
from props.dibspix import dark, mix, erode, dilate, ik, EXPR, res, res_for, blit, rotate
import paths as P

INK = (26, 12, 38)                                    # violet-black
LDIR_B = np.array([0.30, -0.52, 0.80], np.float32)    # lantern light from below-front, a little from the facing side
WHITE = (246, 240, 226)
MOON = (150, 186, 255)
_ST = {}


class light_below:
    """the shared dibspix lit() reads DX.LDIR at call time: swap it while a Grim Ride sprite is being drawn"""
    def __enter__(s): s.prev = DX.LDIR; DX.LDIR = LDIR_B; return s
    def __exit__(s, *a): DX.LDIR = s.prev


def stip():
    """white-noise stipple field on the current canvas (fixed per canvas px, so dots never boil between frames)"""
    k = DX.RES
    if k not in _ST:
        rng = np.random.default_rng(1031)
        _ST[k] = rng.random((DX.H, DX.W)).astype(np.float32) - 0.5
    return _ST[k]


def tones(base, k=0.36, glow=(255, 150, 60)):
    """4-tone ramp (depth, shadow, base, glow): shadows sink to violet, the lit side takes the lantern's orange"""
    b = np.array(base, np.float32)
    d = b * 0.34 + np.array((22, 8, 40))
    s = b * 0.64 + np.array((14, 4, 28))
    l = b + (np.array(glow, np.float32) - b) * k + (255 - b) * 0.12
    return [tuple(int(v) for v in np.clip(x, 0, 255)) for x in (d, s, b, l)]


class Spr(DX.Spr):
    def paint(s, mask, pal, val=None, dither=0.26, bands=(0.22, 0.42, 0.80), ol=True, olc=None):
        if not mask.any(): return mask
        pal = list(pal)
        if len(pal) == 3: pal = [pal[0], pal[0], pal[1], pal[2]]
        if len(pal) == 2: pal = [pal[0], pal[0], pal[1], pal[1]]
        if len(pal) == 1: pal = [dark(pal[0], 0.4), dark(pal[0], 0.7), pal[0], pal[0]]
        Pp = np.array(pal, np.uint8)
        if val is None:
            idx = np.full(mask.shape, 2, np.int32)
        else:
            v = np.clip(np.asarray(val, np.float32) + stip() * dither, 0.0, 0.9999)
            idx = np.searchsorted(np.array(bands, np.float32), v).astype(np.int32)
        s.col[mask] = Pp[np.clip(idx, 0, 3)[mask]]
        s.m |= mask
        s.keep[mask] = False
        if ol:
            e = mask & ~erode(mask)
            s.col[e] = olc if olc is not None else mix(pal[0], INK, 0.55)
        return mask

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


def stipple_fill(sp, mask, c, density=0.35):
    sp.fill(mask & (stip() > 0.5 - density), c)


class Act(DX.Act):
    """direct-draw actor (chikit.shot): paints a grimpix Spr with the lantern-from-below key light, then blits it like dibspix.Act"""
    def __call__(s, big, v, lt):
        sc = s.scale(v)
        with res(res_for(sc, s.hires)), light_below():
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
    with res(res_for(s, hires)), light_below():
        sp = Spr(); sp.mirror_text = flip
        fn(sp, **P_)
        if rot: rotate(sp, rot, pivot)
    return sp


def render(fn, s=6, bg=(40, 30, 60), size=(1080, 1920), at=None, flip=False, **P_):
    big = np.zeros((size[1], size[0], 3), np.uint8); big[:] = bg
    sp = draw(fn, s, flip=flip, **P_)
    ox, oy = at or (size[0] // 2, size[1] - 60)
    blit(big, sp, ox, oy, s, None, flip)
    return big
