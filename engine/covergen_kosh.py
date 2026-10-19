"""Covers of «Кощей из панельки» (RU): code-drawn frame from the series' own world + sprites, title in the series style
(«хохломское золото»: props/koshkit.hook_title) and a BLACK-LACQUER plate with a gold Хохлома curl frame and cinnabar berries
«КОЩЕЙ ИЗ ПАНЕЛЬКИ • СЕРИЯ N/6» on top of the profile-grid 3:4 zone (rule 10.10.2026); nothing important under y 1520.
  from covergen_kosh import make;  make(frame_rgb, ['ПЕНСИЮ', 'НЕ ДАЮТ?!'], n=1, out='cover.png')   (+ cover_grid.png next to it)"""
import math
import numpy as np
from PIL import Image, ImageDraw
import overlays as O
from props import koshkit as K
from props import koshpix as KX
from covergen_taiga import grid_preview, GRID

GOLD, CIN, INK = KX.GOLD, KX.CINNABAR, KX.INK


def plate(n, total=6, w=880, h=156):
    a = np.zeros((h, w, 4), np.uint8)
    a[..., :3] = (20, 12, 10); a[..., 3] = 255
    img = Image.fromarray(a); d = ImageDraw.Draw(img)
    d.rectangle([6, 6, w - 7, h - 7], outline=GOLD + (255,), width=6)
    d.rectangle([16, 16, w - 17, h - 17], outline=CIN + (255,), width=2)
    for cx in (40, w - 40):                                                  # gold curls + cinnabar berries in the corners
        for k in range(18):
            u = k / 18; a_ = u * 2.6 * math.pi; r = 22 * (1 - 0.7 * u)
            d.ellipse([cx + math.cos(a_) * r - 4, h / 2 + math.sin(a_) * r - 4, cx + math.cos(a_) * r + 4, h / 2 + math.sin(a_) * r + 4], fill=GOLD + (255,))
        for dy in (-34, 34): d.ellipse([cx - 9, h / 2 + dy - 9, cx + 9, h / 2 + dy + 9], fill=CIN + (255,))
    d.fontmode = '1'
    f1, f2 = O.pfont(44), O.pfont(28)
    t1 = 'КОЩЕЙ ИЗ ПАНЕЛЬКИ'; b1 = f1.getbbox(t1)
    while b1[2] - b1[0] > w - 170: f1 = O.pfont(f1.size - 2); b1 = f1.getbbox(t1)
    d.text(((w - (b1[2] - b1[0])) // 2 - b1[0], 38 - b1[1]), t1, font=f1, fill=(255, 220, 110))
    t2 = f'СЕРИЯ {n}/{total}'; b2 = f2.getbbox(t2)
    d.text(((w - (b2[2] - b2[0])) // 2 - b2[0], 100 - b2[1]), t2, font=f2, fill=(120, 255, 150))
    return np.array(img)


def make(frame, title, n=1, out='cover.png', title_size=86, plate_y=None):
    big = frame.copy()
    p = plate(n)
    py = GRID[0] + 20 if plate_y is None else plate_y
    t = K.title_trim(K.hook_title(title, title_size))
    ty = py + p.shape[0] + 20
    shade = np.zeros((big.shape[0], 1, 1), np.float32)
    y1 = ty + t.shape[0]
    shade[GRID[0]:y1, 0, 0] = 0.45
    n_ = len(shade[y1:y1 + 120]); shade[y1:y1 + n_, 0, 0] = np.linspace(0.45, 0.0, 120)[:n_]
    big = (big * (1 - shade)).astype(np.uint8)
    O.overlay(big, p, (big.shape[1] - p.shape[1]) // 2, py, 1.0)
    O.overlay(big, t, (big.shape[1] - t.shape[1]) // 2, ty, 1.0)
    Image.fromarray(big).save(out)
    grid_preview(big, out.replace('cover.png', 'cover_grid.png'))
    return big
