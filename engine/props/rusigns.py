"""Russian inscriptions as decals (Press Start 2P has Cyrillic; the decal pixel font of decals.py is Latin-only).
Rule 10.10.2026: every inscription is FITTED into its plate — the biggest crisp size (multiple of 8 decal px) whose lines fit inside
border + padding, centred; nothing crosses the plate edge. Output: RGBA in decal px (decals.WS per world px), for decals.attach().
  img = plate(80, 24, ['ВОДУ', 'БЕРЕГИ!'], bg=..., fg=..., border=...)   # w, h in WORLD px"""
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as PATHS
from props import decals as D

WS = D.WS


def _font(size):
    return ImageFont.truetype(PATHS.FONT_PX, size)


def plate(w, h, lines, bg=(244, 240, 226), fg=(30, 28, 30), border=(40, 34, 30), bw=1.0, pad=1.5, colors=None, weights=None,
          lead=0.45, tilt=0.0, wear=0.0, seed=0, round_=0.0, stripe=None, hand=False, transparent=False):
    W_, H_ = int(round(w * WS)), int(round(h * WS))
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    b = int(round(bw * WS)) if border is not None else 0
    if not transparent:
        r = int(round_ * WS)
        if border is not None:
            d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], r, fill=border + (255,))
            d.rounded_rectangle([b, b, W_ - 1 - b, H_ - 1 - b], max(0, r - b), fill=bg + (255,))
        else:
            d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], r, fill=bg + (255,))
        if stripe:
            sc, fr = stripe
            d.rectangle([b, b, W_ - 1 - b, b + int((H_ - 2 * b) * fr)], fill=sc + (255,))
    p = int(round(pad * WS))
    aw, ah = W_ - 2 * (b + p), H_ - 2 * (b + p)
    weights = weights or [1.0] * len(lines)
    colors = colors or [fg] * len(lines)
    best = None
    for base in range(8, 400, 8):                                      # biggest size that fits
        sizes = [max(8, int(base * wt) // 8 * 8) for wt in weights]
        ws_ = [_font(s).getlength(l) for l, s in zip(lines, sizes)]
        th = sum(sizes) + sum(int(s * lead) for s in sizes[1:])
        if max(ws_) <= aw and th <= ah: best = (sizes, ws_, th)
        else: break
    if best is None:
        raise ValueError(f'inscription does not fit: {lines} in {w}x{h} world px')
    sizes, ws_, th = best
    y = b + p + (ah - th) // 2
    for l, s, lw, c in zip(lines, sizes, ws_, colors):
        x = b + p + (aw - lw) / 2
        if hand:
            rng = np.random.default_rng(seed)
            for ch in l:
                d.text((x + rng.normal(0, s * 0.04), y + rng.normal(0, s * 0.05)), ch, font=_font(s), fill=c + (255,))
                x += _font(s).getlength(ch)
        else:
            d.text((x, y), l, font=_font(s), fill=c + (255,))
        y += s + int(s * lead)
    a = np.array(im)
    if wear > 0: D.weather(a, wear, seed)
    if tilt: a = D.rotate(a, tilt)
    return a
