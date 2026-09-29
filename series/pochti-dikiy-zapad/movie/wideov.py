"""16:9 overlays for the feature cut: chapter HUD (day counter, Molniya's income), captions at the bottom, stickers.
All coordinates are output px on a 1920x1080 frame."""
import math
import numpy as np
from PIL import Image, ImageDraw
import overlays as O
import paths as P

W, H = 1920, 1080
CAP_Y = 905           # captions centre
_HUD = {}


def carrot_icon(n=1, s=4):
    c = np.zeros((16 * s, (12 * n + 4) * s, 4), np.uint8)
    for k in range(n):
        x0 = k * 12 * s
        for i in range(10):
            w = max(1, 5 - i // 2)
            c[(4 + i) * s:(5 + i) * s, x0 + (6 - w // 2) * s:x0 + (6 + w - w // 2) * s] = (236, 128, 40, 255)
        c[0:4 * s, x0 + 5 * s:x0 + 7 * s] = (84, 160, 60, 255); c[s:3 * s, x0 + 3 * s:x0 + 9 * s] = (84, 160, 60, 255)
    return c


def _panel(lines, icon_lines=()):
    """small translucent HUD panel: list of (text, colour, size) ; returns RGBA array"""
    from PIL import ImageFont
    rows = []
    for txt, col, size in lines:
        f = O.pfont(size)
        bb = f.getbbox(txt); rows.append((txt, col, size, bb[2] - bb[0], bb[3] - bb[1]))
    ic = icon_lines[0] if icon_lines else None
    w = max(r[3] for r in rows) + 44 + (ic.shape[1] + 12 if ic is not None else 0)
    h = sum(r[4] + 14 for r in rows) + 26
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), 14, fill=(20, 12, 10, 150))
    y = 16
    for txt, col, size, tw, th in rows:
        d.fontmode = '1'
        f = O.pfont(size); bb = f.getbbox(txt)
        d.text((22 - bb[0], y - bb[1]), txt, font=f, fill=col + (235,))
        y += th + 14
    out = np.array(img)
    if ic is not None:
        oy = h - ic.shape[0] - 12
        reg = out[oy:oy + ic.shape[0], w - ic.shape[1] - 14:w - 14]
        m = ic[..., 3] > 0
        reg[m] = ic[m]
    return out


def hud(big, t, day, income, income_from=None, bump_at=None, x=40, y=34):
    """day: int shown as «ДЕНЬ N». income: carrots (Molniya's total). Bumps (pops) at bump_at seconds (chapter time)."""
    key = ('d', day, income, income_from)
    if key not in _HUD:
        ic = carrot_icon(1, 3)
        _HUD[key] = (_panel([(f'ДЕНЬ {day}', (255, 236, 170), 26)]),
                     _panel([(f'ДОХОД  ×{income}', (255, 190, 90), 24)], [ic]))
    a, b = _HUD[key]
    O.overlay(big, a, x, y, 1.0)
    if income is not None:
        O.overlay(big, b, x, y + a.shape[0] + 10, 1.0)


def stickers(big, items, t):
    for img, a, b, cx, cy in items: O.draw_sticker(big, img, t, a, b, cx, cy)


def title_card(big, lines, k, y=380, size=72):
    img = O.pixel_title(lines, size, width=W)
    O.overlay(big, img, 0, y, k)


def ptext(big, txt, x, y, size=28, col=(255, 236, 170), anchor='l', outline=(20, 12, 8)):
    """pixel-font text with a dark outline straight onto the frame"""
    f = O.pfont(size)
    bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    img = Image.new('L', (tw + 16, th + 16), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text((8 - bb[0], 8 - bb[1]), txt, font=f, fill=255)
    m = np.array(img) > 127
    dil = O._dilate(m, max(2, size // 12))
    x0 = int(x - (tw / 2 if anchor == 'c' else tw if anchor == 'r' else 0)) - 8; y0 = int(y - th / 2) - 8
    rgba = np.zeros(m.shape + (4,), np.uint8)
    rgba[dil] = outline + (255,); rgba[m] = col + (255,)
    O.overlay(big, rgba, x0, y0, 1.0)
