"""«Thanks, Randy» — sprite manner «Fridge-Light Sitcom» (see series/thanks-randy/design/philosophy.md).
Same sprite canvas / IK / face kit / blit as props/dibspix.py (one sprite px = one visible square, 2x..6x for close-ups) and the fast
local rasterisers + fitted Press Start 2P text of props/taigapix.Spr, but its own look:
  * the key light is the WARM kitchen / store lamp from ABOVE (tops of heads, flat-top, perm and shoulders glow warm yellow);
  * every downward-facing surface catches the COLD blue light of an open fridge / freezer (chins, bellies, palms glow icy);
  * shadows are not dithered and not hatched: the tone border breaks into tiny pixel FROST CRYSTALS («+» flakes on a fixed grid,
    never boiling between frames), on Tom the frost is his skin;
  * plum ink outline (not black), 1 sprite px: warm and cold sit in one world.
Usage: Act(fn, wx, wy, s_=.., **params) exactly like dibspix.Act (chikit.shot treats it as a direct actor)."""
import numpy as np
from props import dibspix as DX
from props import taigapix as TX
from props.dibspix import dark, mix, erode, dilate, res, res_for, blit, rotate

INK = (52, 26, 48)                                      # plum ink
LDIR_TOP = np.array([-0.22, 0.80, 0.56], np.float32)    # warm lamp from above, a little from the left
COLD = (176, 226, 255)                                  # fridge bounce from below
FROST = (236, 248, 255)
WHITE = (252, 250, 244)
_FLAKE = {}


def tones(base, k=0.30):
    """3-tone ramp (shadow, base, light): shadow cool plum-blue (fridge side), light warm yellow (lamp side)"""
    b = np.array(base, np.float32)
    d = b * 0.56 + np.array((10, 8, 34))
    l = b + (255 - b) * k + np.array((18, 10, -14))
    return [tuple(int(v) for v in np.clip(x, 0, 255)) for x in (d, b, l)]


def flake_mask(shape, k):
    """fixed «+» frost-crystal pattern on a 5x5 grid of canvas px (k-scaled): the tone border breaks into tiny flakes"""
    key = (shape, k)
    if key not in _FLAKE:
        h, w = shape
        q = max(1, k)
        rr, cc = np.mgrid[0:h, 0:w]
        r5, c5 = (rr // q) % 5, (cc // q) % 5
        off = ((rr // (5 * q)) % 2) * 2                                    # staggered rows
        c5 = (c5 + off) % 5
        _FLAKE[key] = ((r5 == 2) & (c5 >= 1) & (c5 <= 3)) | ((c5 == 2) & (r5 >= 1) & (r5 <= 3))
    return _FLAKE[key]


class top_light:
    """the shared dibspix lit() reads DX.LDIR at call time: swap it while a «Thanks, Randy» sprite is being drawn"""
    def __enter__(s): s.prev = DX.LDIR; DX.LDIR = LDIR_TOP; return s
    def __exit__(s, *a): DX.LDIR = s.prev


class Spr(TX.Spr):
    def paint(s, mask, pal, val=None, dither=None, bands=(0.32, 0.72), ol=True, olc=None, bounce=None, gloss=0.0, frost=True):
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
            if frost:                                                      # crystal flakes of the darker tone across each border
                fl = flake_mask(mask.shape, s.k)
                for b in bands:
                    near = (v >= b) & (v < b + 0.09) & fl
                    idx[near] -= 1
        s.col[mask] = Pp[np.clip(idx, 0, 2)[mask]]
        if bounce is not None:
            b = mask & bounce
            s.col[b] = (s.col[b].astype(np.float32) * 0.50 + np.array(COLD, np.float32) * 0.50).astype(np.uint8)
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
        return m & (ny < -0.66)

    def outline(s, c=INK, w=1):
        TX.Spr.outline(s, c, w)

    def sparkle(s, mask, n=6, seed=2, col=FROST):
        """ice glints: tiny 4-point stars (Tom, frozen things)"""
        rng = np.random.default_rng(seed)
        ys, xs = np.nonzero(mask)
        if not len(xs): return
        for i in rng.choice(len(xs), min(n, len(xs)), replace=False):
            x = (xs[i] - s.OX + 0.5) / s.k; y = (s.OY - ys[i] - 0.5) / s.k
            TX.thin(s, (x - 0.9, y), (x + 0.9, y), col, 0.16, keep=True)
            TX.thin(s, (x, y - 0.9), (x, y + 0.9), col, 0.16, keep=True)


thin, stroke = TX.thin, TX.stroke


class Act(DX.Act):
    """direct-draw actor (chikit.shot): paints a randypix Spr under the warm top light, then blits it like dibspix.Act"""
    def __call__(s, big, v, lt):
        sc = s.scale(v)
        with res(res_for(sc, s.hires)), top_light():
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
    with res(res_for(s, hires)), top_light():
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
