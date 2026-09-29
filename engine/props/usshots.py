"""Shared shot helpers for «Sunny Palms HOA» episodes E02+ (E01 keeps its own copies in ep01.py).
A Shots object binds a world image, the hero anchors and the scene light, and renders the standard close-ups:
  cu_dale / cu_brenda / cu_earl  ->  1080x1920 uint8 frame
Every close-up takes optional hooks:
  behind(CH, v) / front(CH, v)   draw extra lit things (props, Kevin the flamingo, a cat) before / after the hero on the hero canvas
  fx_(big, v, t)                 frame-level effects after compositing (rain, mist, glow)
Anchors are (world x, world y of the feet, unit = world px per body unit)."""
import math
import numpy as np
import stage as ST
from stage import Chars, view_at
import fx
from props import us_cast as U
from props import us_props as UP
from props import uskit as K
from props import bytfx as B


def J(u, p=1.7, k=0.38):
    """jump-cut punch-in: every other `p` seconds of a long shot is framed tighter"""
    return k if int(u / p) % 2 else 0.0


def hit(t, t0, dur=0.35):
    return max(0.0, 1 - (t - t0) / dur) if t >= t0 else 0.0


class Shots:
    def __init__(self, talk, world, dale=(430.0, 592.0, 16.0), brenda=(965.0, 592.0, 16.0), earl=(640.0, 492.0, 11.0),
                 light=None, pond_light=None, vignette=0.28, post=None):
        self.talk, self.world = talk, world
        self.D, self.B, self.E = dale, brenda, earl
        self.light = light or K.light_yard
        self.pond_light = pond_light or K.light_pond
        self.vig = vignette
        self.post = post                       # callable(big, t) applied to every close-up (grade, rain, ...)

    def mouth(self, who, t, k=1.7):
        return min(1.0, self.talk(who, t) * k)

    def _finish(self, big, t, v, fx_):
        if fx_: fx_(big, v, t)
        if self.post: self.post(big, t)
        fx.vignette(big, self.vig)
        return big

    # ------------------------------------------------------------------ Dale
    def cu_dale(self, t, u, expr, Z=2.0, hand=None, prop=None, shades=False, red=0.0, sweat=0.0, look=0.0, lean=0.0, pose=None,
                dx=0.0, dy=0.0, zoom=0.06, paint=None, kmouth=1.7, behind=None, front=None, fx_=None, hand_f=None, prop_f=None,
                visor=False):
        DX, DY, DU = self.D
        Zt = Z + zoom * u
        ST.set_px(ST.px_for_zoom(Zt))
        v = view_at(self.world, DX + 1.5 * DU + dx, DY - 21.0 * DU + dy, Zt, 180, 262)
        CH, _ = K.begin(Zt)
        big = v.bg()
        if behind: behind(CH, v)
        U.dale(CH, v.cam(DX, DY, DU), pose or U.DPOSE['stand'], t, self.mouth('dale', t, kmouth), expr, look, shades, hand_n=hand,
               prop_n=prop, lean=lean, sweat=sweat, red=red, paint=paint, hand_f=hand_f, prop_f=prop_f, visor=visor)
        if front: front(CH, v)
        CH.comp(big, self.light(v))
        return self._finish(big, t, v, fx_)

    # ------------------------------------------------------------------ Brenda
    def cu_brenda(self, t, u, expr, Z=2.0, hand=None, prop=None, pose=None, sweat=0.0, look=0.0, lean=0.0, dx=0.0, dy=0.0,
                  zoom=0.06, hand_f=None, prop_f=None, in_cart=False, kmouth=1.6, behind=None, front=None, fx_=None, outfit='polo',
                  visor=True):
        BX, BY, BU = self.B
        Zt = Z + zoom * u
        ST.set_px(ST.px_for_zoom(Zt))
        v = view_at(self.world, BX - 1.5 * BU + dx, BY - 20.6 * BU + dy, Zt, 180, 262)
        CH, _ = K.begin(Zt)
        big = v.bg()
        if in_cart:
            CB, CF = Chars(), Chars()
            seat = UP.golf_cart(CB, CF, v, BX - 5.5 * BU, BY + 1.5 * BU, u=BU, flip=True, t=t, brake=1.0)
            CB.comp(big, self.light(v))
            if behind: behind(CH, v)
            U.brenda(CH, v.cam(seat[0], seat[1], BU, flip=True), U.BPOSE['sit'], t, self.mouth('brenda', t, kmouth), expr, look, hand_n=hand,
                     prop_n=prop, lean=lean, sweat=sweat, hand_f=hand_f, prop_f=prop_f, outfit=outfit, visor=visor)
            if front: front(CH, v)
            CH.comp(big, self.light(v))
            CF.comp(big, self.light(v))
        else:
            if behind: behind(CH, v)
            U.brenda(CH, v.cam(BX, BY, BU, flip=True), pose or U.BPOSE['stand'], t, self.mouth('brenda', t, kmouth), expr, look, hand_n=hand,
                     prop_n=prop, lean=lean, sweat=sweat, hand_f=hand_f, prop_f=prop_f, outfit=outfit, visor=visor)
            if front: front(CH, v)
            CH.comp(big, self.light(v))
        return self._finish(big, t, v, fx_)

    # ------------------------------------------------------------------ Earl
    def cu_earl(self, t, u, lid=0.5, Z=2.6, look=(0.0, 0.0), paint=None, grin=0.0, dx=0.0, dy=0.0, zoom=0.05, mist=0.0, behind=None,
                front=None, fx_=None, stuff=None, chew=0.0, wet=0.0, ripples=True):
        EX, EY, EU = self.E
        Zt = Z + zoom * u
        ST.set_px(ST.px_for_zoom(Zt))
        v = view_at(self.world, EX + 2.0 * EU + dx, EY - 3.0 * EU + dy, Zt, 180, 330)
        CH, _ = K.begin(Zt)
        big = v.bg()
        if behind: behind(CH, v)
        U.earl(CH, v.cam(EX, EY, EU), t, self.mouth('earl', t, 1.6), lid, look, paint, 0.0, 1.0, True, grin, stuff=stuff, chew=chew)
        if front: front(CH, v)
        CH.comp(big, self.pond_light(v))
        ox, oy = v.opt(EX, EY)
        if ripples:
            for k in range(3):
                ph = (t * 0.5 + k / 3) % 1.0
                rw = int((60 + 300 * ph) * v.Z / 2.6); a = 0.5 * (1 - ph)
                y0 = int(oy) + 4 + k * 3
                x0 = int(ox + 60 - rw); x1 = int(ox + 60 + rw)
                if 0 <= y0 < 1914:
                    seg = big[y0:y0 + 6, max(0, x0):min(1080, x1)]
                    seg[:] = (seg * (1 - a) + np.array((200, 240, 230)) * a).astype(np.uint8)
        if mist > 0:
            for i in range(10):
                r = np.random.default_rng(i)
                cx = ox + 60 + r.uniform(-260, 260); cy = oy - 90 + r.uniform(-170, 120)
                B.puff(big, cx, cy, 90 + 60 * r.random(), 0.55 * mist, UP.BONE)
        return self._finish(big, t, v, fx_)
