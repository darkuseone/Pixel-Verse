"""«Grim Ride» shared shot helpers for E02+ (E01 keeps its own copies in ep01.py).
  from props.grimshots import Kit
  KIT = Kit(EPI)      # mouth/talk from the episode; worlds, placement, close-ups, inserts are shared
Coordinates: world px of the xAI backgrounds (1280x720); output 1080x1920."""
import math
import numpy as np
from PIL import Image
import stage as ST
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
from props import grimpix as GX
from props import grimcast as GC
from props import grimkit as K
from props import bytfx as B
from props.dibspix import blit

A, wpt, aout = K.A, K.wpt, K.aout
LANE = 650.0                       # street: riders' feet
WALK = 668.0                       # Todd's yard: the sidewalk
LAWN = 560.0
PFLOOR = 492.0                     # porch floor
WHEELIE = dict(rot=22.0, pivot=(-24.0, 0.5))


def put(v, fn, ox, oy, s, **kw):
    """an actor whose feet anchor lands on output point (ox, oy) of view v; sprites above ~7 px per sprite px are drawn at 2x"""
    if s > 7.0: kw.setdefault('hires', True)
    return A(fn, *wpt(v, ox, oy), s, **kw)


def raisin(big, x, y, s=1.0):
    w, h = int(46 * s), int(60 * s)
    x, y = int(x - w / 2), int(y - h / 2)
    if 0 <= x < OUT_W - w and 0 <= y < OUT_H - h:
        big[y - 4:y + h + 4, x - 4:x + w + 4] = GX.INK
        big[y:y + h, x:x + w] = (120, 40, 140)
        big[y + h // 3:y + 2 * h // 3, x + 6:x + w - 6] = (250, 220, 90)


def rings(big, x, y, t, col=(150, 255, 110), n=3, r0=30, r1=220):
    """«ringing» circles around a point (a phone buzzing in a pocket)"""
    for i in range(n):
        ph = (t * 2.2 + i / n) % 1.0
        r = int(r0 + (r1 - r0) * ph)
        a = 1 - ph
        yy, xx = np.ogrid[-r:r + 1, -r:r + 1]
        ring = np.abs(np.sqrt(xx * xx + yy * yy) - r) < 6
        ys, xs = np.nonzero(ring)
        ys = ys + int(y - r); xs = xs + int(x - r)
        ok = (ys >= 0) & (ys < OUT_H) & (xs >= 0) & (xs < OUT_W)
        big[ys[ok], xs[ok]] = (big[ys[ok], xs[ok]] * (1 - 0.8 * a) + np.array(col) * 0.8 * a).astype(np.uint8)


class Kit:
    def __init__(s, epi):
        s.epi = epi
        s.STREET = K.world('street'); s.YARD = K.world('todd_yard'); s.PORCH = K.world('porch')
        s.GANG = K.world('gangway'); s.HILL = K.world('hilltop')

    def mouth(s, who, t, k=1.8):
        return min(1.0, s.epi.talk(who, t) * k)

    def cu(s, world, light, fn, t, cx, cy, sc, head, Z=1.4, flip=False, blur=0, pre_=None, fx_=None, pin='head', extra=(), **kw):
        """close-up: the sprite anchor `pin` sits at output point `head`; the background is zoomed only Z (<= ~1.45), optionally soft"""
        kw.setdefault('t', t)
        v0 = view_at(world, cx, cy, Z, 180, 320)
        hx, hy = wpt(v0, *head)
        a = A(fn, hx, hy, sc, flip=flip, pin=pin, **kw)
        def pre(big, v):
            if pre_: pre_(big, v)
            if blur: big[:] = K.dof(big, blur)
        big = K.shot(world, light, cx, cy, Z, acts=list(extra) + [a], pre=pre, fx_=(lambda b, v: fx_(b, v, a)) if fx_ else None, sx=180, sy=320)
        return big, a

    def edgar_cu(s, world, light, t, cx=520.0, cy=470.0, sc=20.0, at=(540, 1640), blur=8, expr='deadpan', **kw):
        v = view_at(world, cx, cy, 1.6, 180, 320)
        big = K.dof(v.bg(), blur)
        sp = GX.draw(GC.edgar, sc, t=t, expr=expr, mouth_=s.mouth('edgar', t, 2.0), cam=True, look=(0.0, 0.0), **kw)
        blit(big, sp, at[0], at[1], sc, light(v))
        fx.vignette(big, 0.3)
        return big

    def phone(s, t, mode, u, **kw):
        big = np.zeros((OUT_H, OUT_W, 3), np.uint8)
        K.phone_app(big, t, mode, u, **kw)
        return big
