"""Shared helpers for the NEW blocks of the feature cut (16:9). Import first: it switches the engine to wide mode."""
import os
os.environ['PV_WIDE'] = '1'
import sys, pathlib, math, json
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine')); sys.path.insert(0, str(HERE))
import numpy as np
from PIL import Image, ImageDraw
import paths as P
import stage as ST
from stage import Chars, Light, shadow, ell, wrect, px_text, OUT_W, OUT_H, UP
import widecam as WC
from widecam import View, view_at, halves
import scene as S
from scene import Layer, cap, dot, outline, sm, lerp
import overlays as O
import fx
import wideov as WO
from episode import Episode, COL
from props import chars as C

FPS = 30
COLM = dict(COL, bartender=(210, 210, 210))
_W = {}


def bgworld(name, colors=110):
    """xAI background -> quantized 1280x720 world (cached)"""
    if name in _W: return _W[name]
    cache = P.build('props', f'movie_{name}.npy')
    if os.path.exists(cache):
        a = np.load(cache)
    else:
        p = HERE / 'bg' / f'{name}.png'
        if not p.exists(): p = P.series() / 'bg' / f'{name}.png'
        im = Image.open(p).convert('RGB')
        if im.size != (1280, 720): im = im.resize((1280, 720), Image.BOX)
        a = np.array(im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'))
        np.save(cache, a)
    _W[name] = a
    return a


def episode(name, voice, dur):
    return Episode(name, voice, dur, FPS, colors=COLM)


def begin(Z):
    ST.set_px(ST.px_for_zoom(Z))
    return Chars(), Chars()


def shot(v, t, draw, light=None, vig=0.3, speed=0.0):
    """generic hybrid shot: bg + draw(CH, FX, big, v) + scene light on heroes + emissive particles + vignette"""
    CH, FX = begin(v.Z)
    big = v.bg()
    draw(CH, FX, big, v)
    CH.comp(big, light); FX.comp(big)
    if vig: fx.vignette(big, vig)
    if speed: fx.speed_lines(big, t, speed)
    return big


def flash_at(big, t, times, dur=0.15, k=0.7):
    for fa in times:
        if fa <= t < fa + dur: O.flash(big, k * (1 - (t - fa) / dur))


def zoom_crop(img, z, cx=0.5, cy=0.5):
    """digital push-in on a finished frame"""
    if z <= 1.0001: return img
    h, w = img.shape[:2]
    ww, hh = int(w / z), int(h / z)
    x0 = int((w - ww) * cx); y0 = int((h - hh) * cy)
    return np.array(Image.fromarray(img[y0:y0 + hh, x0:x0 + ww]).resize((w, h), Image.LANCZOS))


def sepia(img, k=1.0):
    g = (img[..., 0] * 0.3 + img[..., 1] * 0.59 + img[..., 2] * 0.11)[..., None]
    s = np.clip(g * np.array([1.08, 0.92, 0.7]) + np.array([16, 8, 0]), 0, 255)
    return (img * (1 - k) + s * k).astype(np.uint8)


def wv(world, cx, cy, Z):
    """view centred on world point (cx,cy) at wide zoom Z"""
    return ST.View(world, cx - ST.W / 2 / Z, cy - ST.H / 2 / Z, Z)


def crt(big, k=1.0):
    """TV-commercial look: rounded dark corners, scanlines"""
    h, w = big.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = ((xx - w / 2) / (w / 2)) ** 4 + ((yy - h / 2) / (h / 2)) ** 4
    f = big.astype(np.float32) * (1 - 0.55 * k * np.clip(d - 0.55, 0, 1))[..., None]
    f[::4] *= 1 - 0.18 * k
    big[:] = np.clip(f, 0, 255).astype(np.uint8)


def bgworld_t(name, items, tag, colors=110):
    """background + baked pixel text. items: [(text, cx, cy, size, colour, shade)]  (native 1280x720 px)"""
    key = f'{name}_{tag}'
    if key in _W: return _W[key]
    cache = P.build('props', f'movie_{key}.npy')
    if os.path.exists(cache):
        a = np.load(cache)
    else:
        from props.rental import _text
        p = HERE / 'bg' / f'{name}.png'
        if not p.exists(): p = P.series() / 'bg' / f'{name}.png'
        im = Image.open(p).convert('RGB')
        if im.size != (1280, 720): im = im.resize((1280, 720), Image.BOX)
        for txt, cx, cy, size, col, shade in items:
            im = _text(im, txt, cx, cy, size, col, shade)
        a = np.array(im.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB'))
        np.save(cache, a)
    _W[key] = a
    return a


def load_chapter(dirname, modname):
    """import a copied chapter module (its own timeline.py) without clashing with other chapters"""
    import importlib
    p = str(HERE / 'chapters' / dirname)
    sys.path.insert(0, p); sys.modules.pop('timeline', None)
    try:
        return importlib.import_module(modname)
    finally:
        sys.modules.pop('timeline', None); sys.path.remove(p)
