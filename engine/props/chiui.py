"""UI overlays for «Agent Dibs» E02 (Free Trial): Cloakify HUD, pop-up window with a microscopic X, Sleepytime mattress ad (letterboxed,
with Skip counter / SKIP button), cookie banner, receipt, floppy disk. Everything is drawn at 1080x1920 with the pixel font (crisp, mode '1')."""
import math
import numpy as np
from PIL import Image, ImageDraw
import overlays as O
from stage import OUT_W, OUT_H

NAVY, NAVY_D = (18, 34, 96), (8, 14, 44)
CYAN, MINT, RED = (96, 232, 255), (110, 255, 170), (236, 56, 64)


def _canvas(w, h):
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    return img, ImageDraw.Draw(img)


def _txt(d, xy, s, size, col, anchor='la', outline=None):
    f = O.pfont(size)
    d.fontmode = '1'
    if outline:
        for dx in (-2, 0, 2):
            for dy in (-2, 0, 2):
                if dx or dy: d.text((xy[0] + dx, xy[1] + dy), s, font=f, fill=outline, anchor=anchor)
    d.text(xy, s, font=f, fill=col, anchor=anchor)


def blit(big, img, x, y, k=1.0):
    O.overlay(big, np.array(img), int(x), int(y), k)


def _bevel(d, x0, y0, x1, y1, fill, hi=(255, 255, 255), lo=(120, 124, 140), bw=4):
    d.rectangle([x0, y0, x1, y1], fill=fill)
    d.rectangle([x0, y0, x1, y0 + bw - 1], fill=hi); d.rectangle([x0, y0, x0 + bw - 1, y1], fill=hi)
    d.rectangle([x0, y1 - bw + 1, x1, y1], fill=lo); d.rectangle([x1 - bw + 1, y0, x1, y1], fill=lo)


# ---------------------------------------------------------------- Cloakify HUD (floats next to Dibs's shoulder)
def hud(big, x, y, secs, t=0.0, label='FREE TRIAL', k=1.0, scale=1.0):
    """CLOAKIFY panel with the remaining trial time (secs, int) — turns red at <= 3"""
    w, h = int(430 * scale), int(150 * scale)
    img, d = _canvas(w, h)
    hot = secs <= 3
    edge = RED if hot and int(t * 4) % 2 == 0 else CYAN
    d.rectangle([0, 0, w - 1, h - 1], fill=NAVY_D + (200,), outline=edge + (255,), width=5)
    d.rectangle([10, 10, w - 11, 14], fill=edge + (255,))
    _txt(d, (22, 26), 'CLOAKIFY', int(26 * scale), CYAN)
    _txt(d, (w - 22, 26), label, int(18 * scale), (220, 230, 255), 'ra')
    col = (255, 90, 90) if hot else MINT
    _txt(d, (w // 2, int(96 * scale)), f'00:{secs:02d}', int(58 * scale), col, 'mm', outline=NAVY_D)
    blit(big, img, x - w // 2, y - h // 2, k)


# ---------------------------------------------------------------- pop-up window
def popup(big, cx, cy, t, w=700, k=1.0, dodge=0.0, bird=True, shake=0.0):
    """YOUR FREE TRIAL HAS ENDED. window with a microscopic close button (and a tiny bird on its corner that looks the same)"""
    h = int(w * 0.64)
    img, d = _canvas(w + 40, h + 40)
    d.rectangle([22, 22, w + 22, h + 22], fill=(0, 0, 0, 120))                               # drop shadow
    d.rectangle([0, 0, w, h], fill=NAVY_D + (255,))
    d.rectangle([5, 5, w - 5, h - 5], fill=(232, 234, 240, 255))
    d.rectangle([5, 5, w - 5, 60], fill=NAVY + (255,))
    _txt(d, (22, 20), 'CLOAKIFY', 26, (255, 255, 255))
    xx, yy = w - 30, 24                                                                      # the tiny X: 14 px
    d.rectangle([xx - 3, yy - 3, xx + 15, yy + 15], fill=(200, 50, 56, 255))
    for i in range(10): d.point((xx + 2 + i, yy + 2 + i), fill=(255, 255, 255, 255)); d.point((xx + 11 - i, yy + 2 + i), fill=(255, 255, 255, 255))
    if bird:                                                                                  # a tiny black "bird" next to the X
        bx, by = xx - 58, yy + 6
        for i in range(7):
            d.rectangle([bx + i * 2, by - (3 - abs(i - 3)) * 2 + 4, bx + i * 2 + 1, by - (3 - abs(i - 3)) * 2 + 5], fill=(10, 10, 14, 255))
    _txt(d, (w // 2, 118), 'YOUR FREE TRIAL', int(w * 0.060), (150, 20, 34), 'mm')
    _txt(d, (w // 2, 118 + int(w * 0.075)), 'HAS ENDED.', int(w * 0.060), (150, 20, 34), 'mm')
    _txt(d, (w // 2, int(h * 0.60)), 'Keep being invisible', int(w * 0.036), NAVY_D, 'mm')
    _txt(d, (w // 2, int(h * 0.60) + int(w * 0.050)), 'for $39.99/mo', int(w * 0.044), NAVY_D, 'mm')
    bw, bh = int(w * 0.62), int(h * 0.15)
    _bevel(d, (w - bw) // 2, int(h * 0.76), (w + bw) // 2, int(h * 0.76) + bh, (70, 200, 100), (170, 255, 190), (30, 120, 56))
    _txt(d, (w // 2, int(h * 0.76) + bh // 2 + 2), 'UPGRADE', int(w * 0.046), (255, 255, 255), 'mm')
    _txt(d, (30, h - 22), 'maybe later', 16, (140, 144, 160), 'lm')
    ox = dodge * 60 * math.sin(t * 14) + shake * math.sin(t * 60) * 6
    blit(big, img, cx - w // 2 + ox, cy - h // 2, k)
    return (cx - w // 2 + xx + 6 + ox, cy - h // 2 + yy + 6)                                 # centre of the X in output px


# ---------------------------------------------------------------- Sleepytime Mattress ad
_AD = {}


def _ad_art():
    """180x135 pixel-art ad frame, upscaled x6 to 1080x810 (cached)"""
    if 'art' in _AD: return _AD['art']
    W_, H_ = 180, 135
    img = Image.new('RGB', (W_, H_)); d = ImageDraw.Draw(img)
    for y in range(H_):                                                                       # night gradient
        k = y / H_
        d.line([(0, y), (W_, y)], fill=(int(24 + 60 * k), int(18 + 24 * k), int(78 + 52 * k)))
    rng = np.random.default_rng(4)
    for _ in range(46): d.point((int(rng.integers(0, W_)), int(rng.integers(0, 70))), fill=(240, 240, 255))
    d.ellipse([132, 12, 156, 36], fill=(255, 238, 170)); d.ellipse([140, 8, 162, 32], fill=(34, 26, 92))   # crescent
    d.rectangle([14, 86, 166, 104], fill=(70, 74, 150)); d.rectangle([14, 86, 166, 90], fill=(120, 126, 214))   # mattress
    d.rectangle([14, 104, 166, 110], fill=(40, 44, 100))
    d.rectangle([22, 110, 30, 124], fill=(60, 40, 30)); d.rectangle([150, 110, 158, 124], fill=(60, 40, 30))
    d.rectangle([22, 72, 56, 86], fill=(236, 240, 255)); d.rectangle([22, 72, 56, 75], fill=(255, 255, 255))   # pillow
    d.rectangle([56, 78, 150, 88], fill=(236, 120, 150))                                                      # blanket
    d.rectangle([56, 78, 150, 80], fill=(255, 170, 190))
    d.ellipse([28, 62, 46, 78], fill=(236, 190, 160))                                                         # sleeping spy: head
    d.rectangle([20, 60, 54, 66], fill=(40, 40, 50)); d.rectangle([26, 52, 48, 60], fill=(40, 40, 50))        # fedora over the eyes
    d.rectangle([28, 66, 44, 68], fill=(30, 30, 38))
    for i, (zx, zy, s) in enumerate(((62, 56, 5), (72, 44, 7), (86, 30, 9))):                                 # Z z Z
        d.line([(zx, zy), (zx + s, zy), (zx, zy + s), (zx + s, zy + s)], fill=(255, 255, 255), width=2)
    _AD['art'] = img.resize((1080, 810), Image.NEAREST)
    return _AD['art']


def ad_full(big, t, n=5, skip=False, t0=0.0, pulse=0.0):
    """full-screen letterboxed mattress ad over the whole frame (big is replaced); n = Skip-in counter; skip=True shows the SKIP button"""
    big[:] = (6, 6, 10)
    art = np.array(_ad_art())
    y0 = (OUT_H - 810) // 2
    big[y0:y0 + 810] = art
    img, d = _canvas(1080, 810)
    bob = int(6 * math.sin((t - t0) * 6))
    _txt(d, (540, 70 + bob), 'SLEEPYTIME', 112, (255, 226, 90), 'mm', outline=(40, 20, 80))
    _txt(d, (540, 176 + bob), 'MATTRESS', 92, (255, 255, 255), 'mm', outline=(40, 20, 80))
    _txt(d, (540, 700), 'SLEEP LIKE A SPY!', 54, (110, 240, 255), 'mm', outline=(10, 14, 60))
    _txt(d, (540, 770), '*NOT A REAL SPY', 22, (170, 176, 230), 'mm')
    blit(big, img, 0, y0)
    _skip_ui(big, 1080 - 30, y0 + 810 - 30, n, skip, pulse)
    pb = int(1080 * min(1.0, max(0.0, (t - t0) / 8.0)))
    big[y0 + 810 - 10:y0 + 810, :pb] = (255, 214, 60)
    return big


def _skip_ui(big, rx, by, n, skip, pulse=0.0):
    """YouTube-style skip control anchored at its right-bottom corner (rx, by)"""
    if skip:
        w, h = 270 + int(14 * pulse), 100 + int(8 * pulse)
        img, d = _canvas(w, h)
        d.rectangle([0, 0, w - 1, h - 1], fill=(255, 255, 255, 255), outline=(20, 20, 20, 255), width=6)
        _txt(d, (w // 2 - 24, h // 2 + 2), 'SKIP', 46, (10, 10, 10), 'mm')
        tx = w // 2 + 56
        d.polygon([(tx, h // 2 - 20), (tx + 30, h // 2), (tx, h // 2 + 20)], fill=(10, 10, 10, 255))
        d.rectangle([tx + 34, h // 2 - 20, tx + 40, h // 2 + 20], fill=(10, 10, 10, 255))
    else:
        w, h = 330, 84
        img, d = _canvas(w, h)
        d.rectangle([0, 0, w - 1, h - 1], fill=(20, 20, 24, 215), outline=(210, 210, 214, 255), width=4)
        _txt(d, (w // 2, h // 2 + 2), f'Skip in {n}', 32, (255, 255, 255), 'mm')
    blit(big, img, rx - w, by - h)


def ad_pip(big, t, n, box=(640, 330, 1040, 630), t0=0.0, skip=False, pulse=0.0):
    """small picture-in-picture of the ad (reaction shots) with its Skip counter underneath"""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    art = Image.fromarray(np.array(_ad_art())).resize((w, h), Image.NEAREST)
    big[y0 - 8:y1 + 8, x0 - 8:x1 + 8] = (255, 255, 255)
    big[y0 - 4:y1 + 4, x0 - 4:x1 + 4] = (10, 10, 14)
    big[y0:y1, x0:x1] = np.array(art)
    img, d = _canvas(w, 60)
    if skip:
        d.rectangle([w - 190, 6, w - 2, 54], fill=(255, 255, 255, 255), outline=(10, 10, 10, 255), width=4)
        _txt(d, (w - 96, 31), 'SKIP >', 26, (10, 10, 10), 'mm')
    else:
        d.rectangle([w - 190, 6, w - 2, 54], fill=(20, 20, 24, 230), outline=(210, 210, 214, 255), width=3)
        _txt(d, (w - 96, 31), f'Skip in {n}', 22, (255, 255, 255), 'mm')
    blit(big, img, x0, y1 + 12)
    pb = int(w * min(1.0, max(0.0, (t - t0) / 8.0)))
    big[y1 - 6:y1, x0:x0 + pb] = (255, 214, 60)


# ---------------------------------------------------------------- cookie banner, receipt, disk
def cookies(big, cy, t, k=1.0):
    w, h = 980, 330
    img, d = _canvas(w, h)
    d.rectangle([0, 0, w - 1, h - 1], fill=(250, 250, 252, 255), outline=(20, 24, 40, 255), width=8)
    _txt(d, (w // 2, 66), 'ACCEPT ALL COOKIES?', 52, (20, 24, 40), 'mm')
    _txt(d, (w // 2, 120), 'we promise nothing', 22, (120, 124, 140), 'mm')
    for i, x in enumerate((260, 720)):
        _bevel(d, x - 190, 168, x + 190, 292, (70, 200, 100), (170, 255, 190), (30, 120, 56))
        _txt(d, (x, 232), 'YES', 60, (255, 255, 255), 'mm')
    blit(big, img, (OUT_W - w) // 2 + int(6 * math.sin(t * 40)), cy - h // 2, k)


def receipt(w=560):
    """RGBA receipt sprite"""
    rows = [('SUBSCRIBED:', None), ('CLOAKIFY', '$39.99/MO'), ('SLEEPYTIME CLUB', '$79/MO'), ('BEEF OF THE MONTH', '$24/MO'),
            (None, None), ('TOTAL', '$142.99/MO'), ('THANK YOU, AGENT!', None)]
    h = 76 + len(rows) * 62
    img, d = _canvas(w, h + 24)
    d.rectangle([0, 0, w - 1, h], fill=(252, 250, 240, 255), outline=(30, 30, 30, 255), width=5)
    for i in range(0, w, 24): d.polygon([(i, h), (i + 12, h + 22), (i + 24, h)], fill=(252, 250, 240, 255), outline=(30, 30, 30, 255))
    y = 40
    for a, b in rows:
        if a is None:
            d.line([(24, y + 30), (w - 24, y + 30)], fill=(30, 30, 30, 255), width=4)
        elif b is None:
            _txt(d, (w // 2, y + 28), a, 26 if a.startswith('THANK') else 30, (30, 30, 30), 'mm')
        else:
            _txt(d, (26, y + 28), a, 20, (30, 30, 30), 'lm'); _txt(d, (w - 26, y + 28), b, 20, (170, 20, 34), 'rm')
        y += 62
    return np.array(img)


def disk(scale=4):
    """floppy disk sprite 'DOOMSDAY (FINAL FINAL v2)' (RGBA, scale x logical 48 px)"""
    s = 48
    img = Image.new('RGBA', (s, s), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    d.rectangle([0, 0, s - 1, s - 1], fill=(36, 36, 44, 255)); d.rectangle([0, 0, 2, s - 1], fill=(60, 60, 72, 255))
    d.polygon([(s - 9, 0), (s - 1, 8), (s - 1, 0)], fill=(0, 0, 0, 0))
    d.rectangle([10, 0, 36, 14], fill=(190, 194, 204, 255)); d.rectangle([28, 3, 33, 11], fill=(36, 36, 44, 255))
    d.rectangle([6, 22, s - 7, s - 2], fill=(246, 246, 240, 255)); d.rectangle([6, 22, s - 7, 25], fill=(220, 60, 60, 255))
    for yy in (30, 35, 40): d.line([(9, yy), (s - 10, yy)], fill=(120, 124, 140, 255), width=1)
    return Image.fromarray(np.array(img)).resize((s * scale, s * scale), Image.NEAREST)


def disk_labeled(w=420):
    """big readable disk for the close-up"""
    img, d = _canvas(w, w)
    d.rectangle([0, 0, w - 1, w - 1], fill=(36, 36, 44, 255), outline=(10, 10, 14, 255), width=6)
    d.rectangle([int(w * 0.22), 0, int(w * 0.76), int(w * 0.30)], fill=(190, 194, 204, 255))
    d.rectangle([int(w * 0.58), int(w * 0.06), int(w * 0.70), int(w * 0.24)], fill=(36, 36, 44, 255))
    d.rectangle([int(w * 0.12), int(w * 0.46), int(w * 0.88), int(w * 0.96)], fill=(248, 248, 242, 255))
    d.rectangle([int(w * 0.12), int(w * 0.46), int(w * 0.88), int(w * 0.52)], fill=(220, 60, 60, 255))
    _txt(d, (w // 2, int(w * 0.64)), 'DOOMSDAY', 40, (20, 20, 30), 'mm')
    _txt(d, (w // 2, int(w * 0.76)), '(FINAL', 28, (20, 20, 30), 'mm')
    _txt(d, (w // 2, int(w * 0.85)), 'FINAL v2)', 28, (20, 20, 30), 'mm')
    return np.array(img)
