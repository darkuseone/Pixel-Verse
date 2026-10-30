"""«Land of the Fee» — sprite manner «Intaglio Pop» (see series/land-of-the-fee/design/philosophy.md).
Same sprite canvas / IK / face kit / blit as props/dibspix.py (one sprite px = one visible square, 2x..6x for close-ups) and the fast
local rasterisers + fitted Press Start 2P text of props/taigapix.Spr, but its own look — a bank-note engraving:
  * shadows are CUT, not dithered: the mid shadow is the base colour crossed by parallel diagonal engraved lines of the shadow tone,
    the deep shadow adds a second crossing set (cross-hatch) — on a fixed plate grid, so it never boils between frames;
  * highlights are bare cream «paper»; the key light is a flat sunny front-top light (an engraved portrait, not a stage);
  * money-green ink outline (not black), 1 sprite px.
Usage: Act(fn, wx, wy, s_=.., **params) exactly like dibspix.Act (chikit.shot treats it as a direct actor)."""
import numpy as np
from props import dibspix as DX
from props import taigapix as TX
from props.dibspix import dark, mix, erode, dilate, res, res_for, blit, rotate

INK = (18, 52, 40)                                      # banknote green ink
LDIR_FRONT = np.array([-0.30, 0.62, 0.72], np.float32)  # sunny front-top light, a little from the left
PAPER = (252, 246, 226)                                 # cream paper highlight
WHITE = (252, 250, 240)
_HATCH = {}


def tones(base, k=0.32):
    """3-tone ramp (shadow, base, light): the shadow tone sinks toward banknote green-navy ink, the light warms toward cream paper"""
    b = np.array(base, np.float32)
    d = b * 0.50 + np.array((6, 22, 22))
    l = b + (np.array(PAPER, np.float32) - b) * k
    return [tuple(int(v) for v in np.clip(x, 0, 255)) for x in (d, b, l)]


def hatch_masks(shape, k):
    """engraving line patterns on the canvas grid: (diagonal /, anti-diagonal \\); spacing ~3 sprite px at 1x, finer lines at hi-res"""
    key = (shape, k)
    if key not in _HATCH:
        h, w = shape
        rr, cc = np.mgrid[0:h, 0:w]
        sp = 3 if k == 1 else max(4, int(round(2.2 * k)))
        lw = 1 if k <= 2 else max(1, k // 2)
        a = ((rr + cc) % sp) < lw
        b = ((rr - cc) % sp) < lw
        _HATCH[key] = (a, b)
    return _HATCH[key]


class front_light:
    """the shared dibspix lit() reads DX.LDIR at call time: swap it while a «Land of the Fee» sprite is being drawn"""
    def __enter__(s): s.prev = DX.LDIR; DX.LDIR = LDIR_FRONT; return s
    def __exit__(s, *a): DX.LDIR = s.prev


class Spr(TX.Spr):
    def paint(s, mask, pal, val=None, dither=None, bands=(0.26, 0.52, 0.86), ol=True, olc=None, bounce=None, gloss=0.0, engrave=True):
        """3 tones (shadow, base, light): v < b0 deep shadow = cross-hatch of the shadow tone over a mid mix, b0..b1 = base crossed by
        single diagonal lines, b1..b2 = clean base, > b2 = cream paper light"""
        if not mask.any(): return mask
        pal = list(pal)
        if len(pal) == 4: pal = [pal[0], pal[2], pal[3]]
        if len(pal) == 2: pal = [pal[0], pal[1], pal[1]]
        if len(pal) == 1: pal = [dark(pal[0], 0.6), pal[0], pal[0]]
        d, b, l = (np.array(c, np.uint8) for c in pal)
        pal = [tuple(int(x) for x in c) for c in pal]
        mid = np.array(mix(pal[0], pal[1], 0.45), np.uint8)
        if val is None:
            s.col[mask] = b
        else:
            v = np.asarray(val, np.float32)
            b0, b1, b2 = bands
            s.col[mask] = b
            r_, g_, b_ = pal[1]
            skin = r_ > 150 and 15 <= r_ - g_ <= 75 and 0 <= g_ - b_ <= 60
            if engrave and (skin or 585 <= sum(pal[1]) < 700):          # skin: soft solid shade, engraving lines make faces dirty
                s.col[mask & (v < b0)] = mid
                s.col[mask & (v >= b0) & (v < b1)] = np.array(mix(pal[1], pal[0], 0.22), np.uint8)
            elif engrave:
                ha, hb = hatch_masks(mask.shape, s.k)
                deep = mask & (v < b0)
                s.col[deep] = mid
                s.col[deep & (ha | hb)] = d
                sh = mask & (v >= b0) & (v < b1)
                if sum(pal[1]) < 640: s.col[sh & ha] = d                  # white plumage / paper: only the deep shadow is engraved
                else: s.col[sh] = mix(pal[1], pal[0], 0.25)
            else:
                s.col[mask & (v < b1)] = d
            s.col[mask & (v > b2)] = l
            if gloss:
                g = mask & (v > 1.0 - gloss * 0.08)
                s.col[g] = WHITE
        s.m |= mask
        s.keep[mask] = False
        if ol:
            e = mask & ~erode(mask)
            s.col[e] = olc if olc is not None else mix(pal[0], INK, 0.65)
        return mask

    @staticmethod
    def _bounce(ny, m):
        return None

    def outline(s, c=INK, w=1):
        TX.Spr.outline(s, c, w)


thin, stroke = TX.thin, TX.stroke


class Act(DX.Act):
    """direct-draw actor (chikit.shot): paints a feepix Spr under the front light, then blits it like dibspix.Act"""
    def __call__(s, big, v, lt):
        sc = s.scale(v)
        with res(res_for(sc, s.hires)), front_light():
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
    with res(res_for(s, hires)), front_light():
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
