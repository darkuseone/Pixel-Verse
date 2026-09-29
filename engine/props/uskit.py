"""Shared episode kit for «Sunny Palms HOA»: scene light per location and the standard overlay pass
(badge, neon hook title, stickers, karaoke captions, flashes, mosaic, teaser)."""
import math
import numpy as np
import stage as ST
from stage import Chars, Light
from scene import sm, lerp
import overlays as O

COL = dict(dale=(255, 214, 74), brenda=(255, 120, 190), earl=(140, 235, 110))


def begin(Z):
    ST.set_px(ST.px_for_zoom(Z))
    return Chars(), Chars()


def light_yard(v):
    """sunny Florida morning: warm sun from the upper left, cool sky fill on the right"""
    return Light(amb=(1.04, 1.0, 0.94), rim=(-1, -0.5, (255, 236, 190), 0.35), grad=(1.06, 0.93))


def light_pond(v):
    return Light(amb=(0.92, 1.04, 0.98), rim=(-1, -0.5, (230, 255, 210), 0.3), grad=(1.05, 0.9))


def light_storm(v):
    """hurricane: dark, cold green-gray; a weak rim from the flashing sky"""
    return Light(amb=(0.72, 0.82, 0.9), rim=(-1, -0.6, (190, 214, 255), 0.35), grad=(0.96, 0.84))


def light_int(v):
    return Light(amb=(1.03, 0.98, 0.92), rim=(-1, -0.2, (255, 232, 180), 0.4), grad=(1.04, 0.92))


class Show:
    """per-episode overlay config: badge, hook (lines, t0, t1), stickers [(img, t0, t1, cx, cy)], captions,
    flashes, mosaic transitions, teaser text for the last second"""
    def __init__(s, epi, n, hook, hook_t=(0.15, 2.4), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1330,
                 teaser=None, hook_y=150, total=6):
        s.epi = epi
        s.badge = O.make_badge(f'SEASON 1 • EP {n}/{total}')
        s.hook = O.neon_title(hook, 64) if hook else None
        s.hook_t, s.hook_y = hook_t, hook_y
        s.stickers = list(stickers); s.flashes = list(flashes); s.mosaics = list(mosaics)
        s.cap_y = cap_y or {}; s.cap_default = cap_default
        s.teaser = O.neon_title([teaser], 40) if teaser else None

    def apply(s, big, t, shot):
        for img, t0, t1, cx, cy in s.stickers: O.draw_sticker(big, img, t, t0, t1, cx, cy)
        O.overlay(big, s.badge, 36, 96, 1.0)
        if s.hook is not None and s.hook_t[0] <= t < s.hook_t[1]:
            k = min(1.0, (t - s.hook_t[0]) / 0.1) * (1 - sm((t - (s.hook_t[1] - 0.2)) / 0.2))
            O.overlay(big, s.hook, 0, s.hook_y, k)
        s.epi.captions.draw(big, t, s.cap_y.get(shot, s.cap_default))
        dur = s.epi.dur
        if s.teaser is not None and t >= dur - 0.8:
            O.overlay(big, s.teaser, 0, 1560, min(1.0, (t - (dur - 0.8)) / 0.15))
        for fa in s.flashes:
            if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
        for ma in s.mosaics:
            if ma <= t < ma + 0.3: O.mosaic(big, int(lerp(40, 1, (t - ma) / 0.3)))
        return big
