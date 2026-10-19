"""«Кощей из панельки» — sprite manner «Хохлома-нуар» (see series/koshchei/design/philosophy.md).
Same sprite canvas / IK / face kit / blit as props/dibspix.py (one sprite px = one visible square, 2x..6x for close-ups via res_for),
the fast local rasterisers and txt_box of props/taigapix.py, but its own look:
  * 3 flat tones per material, hard edges, no dithering — but the shadow sinks into BLACK LACQUER (warm brown-black), not into blue;
  * key light: the bare 40 W bulb of a stairwell, from ABOVE-RIGHT (warm, yellowish); every downward-facing surface catches a
    pale-green rim of «кощеев огонь» (the spectral underlight) — the cast always stands a little in its own ghost-light;
  * GOLD LEAF: the brightest lit edge of hero parts gets a 1-px gold «Хохлома brush» line (gold() helper), as on a lacquer box;
  * ornament: Хохлома «травка» curls and Павловский-Посад roses on shawls, robes and props (curl(), rose());
  * outline: black-lacquer ink (warm), 1 sprite px.
Usage: Act(fn, wx, wy, s_=.., **params) exactly like dibspix.Act."""
import math
import numpy as np
from props import dibspix as DX
from props import taigapix as TX
from props.dibspix import dark, mix, erode, dilate, res, res_for, blit, rotate

INK = (22, 12, 10)                                     # black lacquer, warm
LDIR_BULB = np.array([0.46, 0.66, 0.60], np.float32)   # bare stairwell bulb, above-right
GHOST = (150, 255, 170)                                # кощеев огонь: green underlight rim
GOLD = (236, 182, 52)
GOLD_L = (255, 228, 130)
CINNABAR = (200, 36, 30)                               # киноварь
WHITE = (250, 246, 232)


class bulb:
    """the shared dibspix lit() reads DX.LDIR at call time: swap it while a «Кощей» sprite is being drawn"""
    def __enter__(s): s.prev = DX.LDIR; DX.LDIR = LDIR_BULB; return s
    def __exit__(s, *a): DX.LDIR = s.prev


def tones(base, k=0.30):
    """3-tone ramp (shadow, base, light): shadow sinks into warm black lacquer, light warms to the 40 W bulb"""
    b = np.array(base, np.float32)
    d = b * 0.42 + np.array((14, 6, 4))
    l = b + (255 - b) * k + np.array((14, 10, -10))
    return [tuple(int(v) for v in np.clip(x, 0, 255)) for x in (d, b, l)]


class Spr(TX.Spr):
    def paint(s, mask, pal, val=None, dither=None, bands=(0.30, 0.74), ol=True, olc=None, bounce=None, gloss=0.0):
        if not mask.any(): return mask
        pal = list(pal)
        if len(pal) == 4: pal = [pal[0], pal[2], pal[3]]
        if len(pal) == 2: pal = [pal[0], pal[1], pal[1]]
        if len(pal) == 1: pal = [dark(pal[0], 0.6), pal[0], pal[0]]
        Pp = np.array(pal, np.uint8)
        idx = np.ones(mask.shape, np.int32) if val is None else \
            np.searchsorted(np.array(bands, np.float32), np.asarray(val, np.float32)).astype(np.int32)
        s.col[mask] = Pp[np.clip(idx, 0, 2)[mask]]
        if bounce is not None:                                       # green ghost-light rim from below
            b = mask & bounce
            s.col[b] = (s.col[b].astype(np.float32) * 0.55 + np.array(GHOST, np.float32) * 0.28).astype(np.uint8)
        if gloss and val is not None:
            g = mask & (np.asarray(val, np.float32) > 1.0 - gloss * 0.10)
            s.col[g] = WHITE
        s.m |= mask
        s.keep[mask] = False
        if ol:
            e = mask & ~erode(mask)
            s.col[e] = olc if olc is not None else mix(pal[0], INK, 0.65)
        return mask

    @staticmethod
    def _bounce(ny, m):
        return m & (ny < -0.82)

    def gold(s, mask, side=(1.0, 1.0)):
        """Хохлома gold-leaf edge: the outer edge of a part that faces the bulb (up-right) gets a 1-canvas-px gold line"""
        e = mask & ~erode(mask)
        sh = np.zeros_like(mask)
        if side[0] > 0: sh[:, :-1] |= ~mask[:, 1:]
        if side[1] > 0: sh[1:, :] |= ~mask[:-1, :]
        s.col[e & sh] = GOLD

    def curl(s, cx, cy, r, c, turns=1.4, w=0.28, mask=None, flip=False, seed=0):
        """one Хохлома «травка» curl: a spiral stroke with a drop at its tail"""
        n = 14
        pts = []
        for q in range(n + 1):
            u = q / n
            a = u * turns * 2 * math.pi + seed
            rr = r * (1 - 0.75 * u)
            pts.append((cx + (-1 if flip else 1) * math.cos(a) * rr, cy + math.sin(a) * rr))
        for a, b in zip(pts[:-1], pts[1:]): s.seg(a, b, w, c, mask)
        s.blob(pts[0][0], pts[0][1], w * 2.2, c, mask)

    def rose(s, cx, cy, r, c, mask=None):
        """Павловский-Посад rose: a cinnabar disc, a darker heart, a light petal arc and two green leaves"""
        s.blob(cx - r * 1.1, cy - r * 0.5, r * 0.55, (46, 110, 56), mask)
        s.blob(cx + r * 1.1, cy - r * 0.4, r * 0.5, (46, 110, 56), mask)
        s.blob(cx, cy, r, c, mask)
        s.blob(cx + r * 0.1, cy + r * 0.05, r * 0.45, dark(c, 0.62), mask)
        for q in range(5):
            a = 0.4 + q * 0.5
            s.seg((cx + math.cos(a) * r * 0.75, cy + math.sin(a) * r * 0.75), (cx + math.cos(a + 0.45) * r * 0.75, cy + math.sin(a + 0.45) * r * 0.75),
                  max(0.18, r * 0.12), mix(c, WHITE, 0.45), mask)


def thin(sp, a, b, c, w=0.3, keep=False, mask=None):
    sp.seg(a, b, w, c, mask, keep)


class Act(DX.Act):
    """direct-draw actor (chikit.shot): paints a koshpix Spr under the stairwell bulb, then blits it like dibspix.Act"""
    def __call__(s, big, v, lt):
        sc = s.scale(v)
        with res(res_for(sc, s.hires)), bulb():
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
    with res(res_for(s, hires)), bulb():
        sp = Spr(); sp.mirror_text = flip
        fn(sp, **P_)
        if rot: rotate(sp, rot, pivot)
    return sp


def render(fn, s=6, bg=(30, 22, 20), size=(1080, 1920), at=None, flip=False, **P_):
    big = np.zeros((size[1], size[0], 3), np.uint8); big[:] = bg
    sp = draw(fn, s, flip=flip, **P_)
    ox, oy = at or (size[0] // 2, size[1] - 60)
    blit(big, sp, ox, oy, s, None, flip)
    return big
