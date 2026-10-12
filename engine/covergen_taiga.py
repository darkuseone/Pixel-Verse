"""Covers of «Прохор. Таёжные лайфхаки» (RU): code-drawn frame from the series' own world + sprites, title in the series style
(campfire stepped fill, spruce ink outline, snow caps, icicles: props/taigakit.hook_title) and a BIRCH-BARK plate
«ТАЁЖНЫЕ ЛАЙФХАКИ • СЕРИЯ N/6» on top of the profile-grid 3:4 zone (rule 10.10.2026); nothing important under y 1520.
  from covergen_taiga import make;  make(frame_rgb, ['9 000 ЗА', 'ТЕПЛО?!'], n=1, out='cover.png')   (+ cover_grid.png next to it)"""
import numpy as np
from PIL import Image, ImageDraw
import overlays as O
from props import taigakit as K

INK = K.INK
GRID = (240, 1680)
SAFE_BOTTOM = 1520


def plate(n, total=6, w=860, h=150):
    """birch bark: white with black bark dashes and two horizontal lenticels bands, ink lettering"""
    rng = np.random.default_rng(n)
    a = np.zeros((h, w, 4), np.uint8)
    a[..., :3] = (238, 234, 222); a[..., 3] = 255
    a[:8], a[-8:], a[:, :8], a[:, -8:] = (40, 36, 34, 255), (40, 36, 34, 255), (40, 36, 34, 255), (40, 36, 34, 255)
    for _ in range(90):
        y = int(rng.integers(10, h - 14)); x = int(rng.integers(10, w - 40)); ln = int(rng.integers(10, 46))
        if y < 20 or y > h - 20: a[y:y + 4, x:x + ln, :3] = (52, 46, 42)
    img = Image.fromarray(a); d = ImageDraw.Draw(img); d.fontmode = '1'
    f1, f2 = O.pfont(46), O.pfont(28)
    t1 = 'ТАЁЖНЫЕ ЛАЙФХАКИ'; b1 = f1.getbbox(t1)
    while b1[2] - b1[0] > w - 70: f1 = O.pfont(f1.size - 2); b1 = f1.getbbox(t1)
    d.text(((w - (b1[2] - b1[0])) // 2 - b1[0], 36 - b1[1]), t1, font=f1, fill=(30, 28, 30))
    t2 = f'СЕРИЯ {n}/{total}'; b2 = f2.getbbox(t2)
    d.text(((w - (b2[2] - b2[0])) // 2 - b2[0], 98 - b2[1]), t2, font=f2, fill=(190, 40, 34))
    return np.array(img)


def grid_preview(cover, out):
    """what the TikTok / Reels profile grid shows: the central 3:4 crop, with the date / views band greyed"""
    c = cover[GRID[0]:GRID[1]].copy()
    c[SAFE_BOTTOM - GRID[0]:] = (c[SAFE_BOTTOM - GRID[0]:] * 0.4).astype(np.uint8)
    im = Image.fromarray(c).resize((360, 480), Image.LANCZOS)
    d = ImageDraw.Draw(im); d.text((8, 452), '12.10   ▶ 128K', fill=(255, 255, 255))
    im.save(out)


def make(frame, title, n=1, out='cover.png', title_size=86, plate_y=None):
    big = frame.copy()
    p = plate(n)
    py = GRID[0] + 20 if plate_y is None else plate_y
    t = K.title_trim(K.hook_title(title, title_size))
    ty = py + p.shape[0] + 24
    shade = np.zeros((big.shape[0], 1, 1), np.float32)
    y1 = ty + t.shape[0]
    shade[GRID[0]:y1, 0, 0] = 0.40
    n_ = len(shade[y1:y1 + 120]); shade[y1:y1 + n_, 0, 0] = np.linspace(0.40, 0.0, 120)[:n_]
    big = (big * (1 - shade)).astype(np.uint8)
    O.overlay(big, p, (big.shape[1] - p.shape[1]) // 2, py, 1.0)
    O.overlay(big, t, (big.shape[1] - t.shape[1]) // 2, ty, 1.0)
    Image.fromarray(big).save(out)
    grid_preview(big, out.replace('cover.png', 'cover_grid.png'))
    return big
