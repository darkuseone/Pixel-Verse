"""Shared episode kit for «Валера и кот»: camera helpers, per-location hero light, occluders and the standard overlay
pass (badge, hook title, stickers, karaoke captions, flashes, mosaic, teaser)."""
import math
import numpy as np
import stage as ST
from stage import Chars, Light
from scene import sm, lerp
import overlays as O
from props import panelka as PK

COL = dict(valera=(120, 200, 255), cat=(255, 170, 70), zina=(255, 150, 190), lyuba=(200, 170, 255),
           tamara=(150, 230, 140), nina=(255, 130, 110), robot=(200, 200, 200))


def begin(Z):
    ST.set_px(ST.px_for_zoom(Z))
    return Chars(), Chars()


def face_w(x, y, un, flip=False, fwd=1.4, h=21.0):
    """world point of Valera's face (between eyes and nose) for close-up framing"""
    return (x - fwd * un) if flip else (x + fwd * un), y - h * un


def occlude(big, v, spr, xy):
    ST.blit_world(big, v, spr, int(xy[0]), int(xy[1]))


def light_bath(v):
    bx, by = v.opt(*PK.BULB)
    return Light(amb=(0.96, 1.0, 1.07), keys=[(bx, by, 900, (255, 214, 150), 0.7)], rim=(1, -0.3, (196, 222, 255), 0.35), grad=(1.06, 0.9))


def light_cold(v):
    bx, by = v.opt(*PK.BULB)
    return Light(amb=(0.9, 1.0, 1.16), keys=[(bx, by, 700, (220, 230, 255), 0.35)], rim=(1, -0.3, (210, 236, 255), 0.45), grad=(1.08, 0.9))


def light_kit(v):
    lx, ly = v.opt(*PK.LAMP_K)
    return Light(amb=(1.0, 0.96, 0.93), keys=[(lx, ly, 1100, (255, 196, 130), 0.8)], rim=(-1, -0.4, (186, 212, 255), 0.35), grad=(1.04, 0.9))


def light_shop(v):
    keys = []
    for p in PK.SH_LIGHTS:
        x, y = v.opt(*p); keys.append((x, y, 1300, (226, 255, 236), 0.45))
    return Light(amb=(0.95, 1.02, 0.97), keys=keys, rim=(-1, -0.2, (206, 228, 255), 0.3), grad=(1.08, 0.88))


class Show:
    """per-episode overlay config: badge, hook (lines, t0, t1), stickers [(img, t0, t1, cx, cy)], captions,
    flashes, mosaic transitions, teaser text for the last second"""
    def __init__(s, epi, n, hook, hook_t=(0.2, 2.2), stickers=(), flashes=(), mosaics=(), cap_y=None, cap_default=1330,
                 teaser=None, hook_y=170):
        s.epi = epi
        s.badge = O.make_badge(f'СЕЗОН 1 • СЕРИЯ {n}/6')
        s.hook = O.winter_title(hook, 64) if hook else None
        s.hook_t, s.hook_y = hook_t, hook_y
        s.stickers = list(stickers); s.flashes = list(flashes); s.mosaics = list(mosaics)
        s.cap_y = cap_y or {}; s.cap_default = cap_default
        s.teaser = O.winter_title([teaser], 40) if teaser else None

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


def lcd_sticker(txt, col=(120, 255, 140), size=72):
    """green LCD-style sticker (register display) as an RGBA image"""
    from PIL import Image, ImageDraw
    f = O.pfont(size)
    bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    W_, H_ = tw + 64, th + 56
    img = np.zeros((H_, W_, 4), np.uint8)
    img[...] = (30, 30, 34, 255)
    img[8:-8, 8:-8] = (12, 34, 18, 255)
    m = Image.new('L', (W_, H_), 0); d = ImageDraw.Draw(m); d.fontmode = '1'
    d.text(((W_ - tw) // 2 - bb[0], (H_ - th) // 2 - bb[1]), txt, font=f, fill=255)
    m = np.array(m) > 127
    img[m] = col + (255,)
    return img
