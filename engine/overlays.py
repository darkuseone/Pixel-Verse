"""Full-resolution (1080x1920) overlays shared by episodes: pixel titles in the cover style, season badge,
word-by-word karaoke captions, bouncing stickers, flash / mosaic transitions."""
import math, re
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as P

OUT_W, OUT_H = 1080, 1920
_pf = {}


def pfont(size):
    if size not in _pf: _pf[size] = ImageFont.truetype(P.FONT_PX, size)
    return _pf[size]


def overlay(big, img, x0, y0, k=1.0):
    """alpha-blend RGBA img onto big at (x0,y0), clipped."""
    h, w = img.shape[:2]
    xa, ya = max(0, x0), max(0, y0); xb, yb = min(big.shape[1], x0 + w), min(big.shape[0], y0 + h)
    if xa >= xb or ya >= yb or k <= 0: return
    src = img[ya - y0:yb - y0, xa - x0:xb - x0]
    region = big[ya:yb, xa:xb]
    al = src[..., 3:4].astype(np.float32) / 255 * k
    region[:] = (region * (1 - al) + src[..., :3] * al).astype(np.uint8)


def _dilate(m, r, step=2):
    d = m.copy()
    for dx in range(-r, r + 1, step):
        for dy in range(-r, r + 1, step):
            if dx * dx + dy * dy <= r * r: d |= np.roll(np.roll(m, dy, 0), dx, 1)
    return d


def pixel_title(lines, size=64, width=OUT_W):
    """series cover-style title: Press Start 2P, yellow->orange stepped gradient, dark outline + shadow. RGBA"""
    f = pfont(size)
    out = np.zeros((len(lines) * (size + 44) + 40, width, 4), np.uint8)
    y = 20
    for line in lines:
        bb = f.getbbox(line); tw = bb[2] - bb[0]; th = bb[3] - bb[1]
        img = Image.new('L', (width, th + 40), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
        d.text(((width - tw) // 2 - bb[0], 16 - bb[1]), line, font=f, fill=255)
        m = np.array(img) > 127
        dil = _dilate(m, 8)
        shd = np.roll(np.roll(dil, 10, 0), 6, 1)
        reg = out[y:y + m.shape[0]]
        reg[shd] = (20, 10, 6, 255); reg[dil] = (42, 22, 12, 255)
        rows = np.where(m.any(1))[0]; r0, r1 = rows[0], rows[-1]
        for yy in range(m.shape[0]):
            k = (yy - r0) / max(1, r1 - r0)
            col = (255, 236, 120) if k < 0.34 else (255, 200, 70) if k < 0.67 else (255, 150, 50)
            reg[yy][m[yy]] = col + (255,)
        reg[m & ~np.roll(m, 8, 0)] = (255, 250, 214, 255)
        y += th + 44
    return out


def make_badge(text, size=34):
    font = ImageFont.truetype(P.FONT_BOLD, size)
    img = Image.new('RGBA', (620, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    tw = d.textlength(text, font=font)
    d.rounded_rectangle((0, 0, tw + 36, 58), 14, fill=(20, 12, 10, 120))
    d.text((18, 9), text, font=font, fill=(255, 244, 214, 200))
    return np.array(img)


# ---------------------------------------------------------------- karaoke captions
TAG = re.compile(r'\[[^\]]*\]')


def is_punch(word):
    core = re.sub(r'[^\wЁё-]', '', word)
    return len(core) >= 2 and core.upper() == core and any(ch.isalpha() for ch in core)


def word_times(env, t0, a, b, words, thr=0.12):
    """distribute words over the voiced frames (100 Hz envelope) of the clip [a,b] placed at t0."""
    i0, i1 = int(a * 100), max(int(a * 100) + 1, int(b * 100))
    e = env[i0:i1] if len(env) > i0 else np.zeros(1)
    voiced = e > thr * (e.max() + 1e-9)
    idx = np.nonzero(voiced)[0]
    if len(idx) == 0: idx = np.arange(len(e))
    wts = np.array([len(w) + 1.5 for w in words], np.float32); cum = np.concatenate([[0], np.cumsum(wts)]) / wts.sum()
    n = len(idx)
    out = []
    for k, w in enumerate(words):
        s = idx[min(n - 1, int(cum[k] * n))]; e_ = idx[min(n - 1, max(int(cum[k + 1] * n) - 1, 0))] + 1
        out.append((w, t0 + s / 100.0, t0 + e_ / 100.0))
    return out


def chunk_words(wt, max_words=3, max_chars=16):
    chunks, cur = [], []
    for w in wt:
        cur.append(w)
        text = ' '.join(x[0] for x in cur)
        if len(cur) >= max_words or len(text) >= max_chars or w[0][-1] in '.!?,:…':
            chunks.append(cur); cur = []
    if cur: chunks.append(cur)
    # merge a dangling 1-word chunk made only of a short word into the previous one
    return chunks


def caption_sprite(words, color, size=86):
    font = ImageFont.truetype(P.FONT_BOLD, size)
    img = Image.new('RGBA', (OUT_W, size * 2 + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    space = d.textlength(' ', font=font)
    parts = [(w, d.textlength(w, font=font)) for w in words]
    tw = sum(p[1] for p in parts) + space * (len(parts) - 1)
    if tw > OUT_W - 80:
        return caption_sprite(words, color, int(size * (OUT_W - 80) / tw))
    x = (OUT_W - tw) / 2
    for w, wl in parts:
        c = color if is_punch(w) else (255, 255, 255)
        d.text((x, 20), w, font=font, fill=c + (255,), stroke_width=9, stroke_fill=(16, 10, 8, 255))
        x += wl + space
    return np.array(img)


class Captions:
    def __init__(s, items):
        """items: list of (t_start, t_end, [words], color)"""
        s.items = [(a, b, caption_sprite(ws, col)) for a, b, ws, col in items]

    def draw(s, big, t, cy):
        for a, b, img in s.items:
            if a <= t < b:
                k = min(1.0, (t - a) / 0.06)
                pop = 1.0 + 0.12 * (1 - min(1.0, (t - a) / 0.1))
                im = img if pop <= 1.001 else _scale(img, pop)
                overlay(big, im, (OUT_W - im.shape[1]) // 2, cy - im.shape[0] // 2, k)


def _scale(img, f):
    h, w = img.shape[:2]
    return np.array(Image.fromarray(img).resize((int(w * f), int(h * f)), Image.NEAREST))


# ---------------------------------------------------------------- stickers
def sticker(text, fg=(255, 236, 120), size=72, icon=None):
    """pixel-font sticker with dark outline + soft glow; optional RGBA icon on the left"""
    f = pfont(size)
    bb = f.getbbox(text); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    iw = icon.shape[1] + 16 if icon is not None else 0
    W_, H_ = tw + iw + 80, max(th, icon.shape[0] if icon is not None else 0) + 80
    m_img = Image.new('L', (W_, H_), 0); d = ImageDraw.Draw(m_img); d.fontmode = '1'
    d.text((40 + iw - bb[0], (H_ - th) // 2 - bb[1]), text, font=f, fill=255)
    m = np.array(m_img) > 127
    out = np.zeros((H_, W_, 4), np.uint8)
    if icon is not None:
        oy = (H_ - icon.shape[0]) // 2
        out[oy:oy + icon.shape[0], 40:40 + icon.shape[1]] = icon
        m = m | (out[..., 3] > 0)
    glow = _dilate(m, 22, 4)
    out[glow & ~m] = (255, 220, 110, 70)
    ol = _dilate(m, 8)
    out[ol & ~m] = (30, 14, 8, 255)
    txt = np.array(m_img) > 127
    rows = np.where(txt.any(1))[0]
    if len(rows):
        r0, r1 = rows[0], rows[-1]
        for yy in range(r0, r1 + 1):
            k = (yy - r0) / max(1, r1 - r0)
            c = tuple(int(v * (1.0 if k < 0.5 else 0.82)) for v in fg)
            out[yy][txt[yy]] = c + (255,)
    return out


def draw_sticker(big, img, t, t0, t1, cx, cy):
    if not (t0 <= t < t1): return
    u = t - t0
    pop = min(1.0, u / 0.12)
    s = 0.3 + 0.7 * pop + 0.18 * math.sin(min(u, 0.5) * 18) * math.exp(-u * 6)
    bounce = -abs(math.sin(u * 7)) * 34 * math.exp(-u * 2.2)
    im = _scale(img, max(0.2, s))
    fade = 1 - max(0.0, (t - (t1 - 0.15)) / 0.15)
    overlay(big, im, int(cx - im.shape[1] / 2), int(cy - im.shape[0] / 2 + bounce), fade)


# ---------------------------------------------------------------- transitions
def flash(big, k):
    if k <= 0: return
    big[:] = (big * (1 - k) + 255 * k).astype(np.uint8)


def mosaic(big, block):
    if block <= 1: return
    h, w = big.shape[:2]
    hb, wb = h // block, w // block
    small = big[:hb * block, :wb * block].reshape(hb, block, wb, block, 3).mean((1, 3)).astype(np.uint8)
    big[:hb * block, :wb * block] = np.repeat(np.repeat(small, block, 0), block, 1)
