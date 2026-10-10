"""Covers of «Florida Man: Allegedly» (US): code-drawn frame from the series' own world + sprites (no AI faces), title as
«Greetings from Florida» postcard letters (yellow -> coral -> magenta, white outline, teal 3D extrusion: props/fmkit.hook_title) and a
booking letterboard plate «FLORIDA MAN / EPISODE N/6» on a mugshot height-chart strip.
Layout = profile-grid rule (10.10.2026, covergen_maz): TikTok / Reels profile grids show only the central 3:4 (y 240..1680) and lay the
date / views over its bottom, so the series plate sits at the TOP of the 3:4 zone, the title right under it, faces in the middle,
nothing that matters below y 1520.
  from covergen_fm import make;  make(frame_rgb, ['NINE', 'GRAND?!'], n=1, out='cover.png')"""
import numpy as np
from PIL import Image, ImageDraw
import overlays as O
from props import fmkit as K

INK = K.INK


GRID = (240, 1680)
SAFE_BOTTOM = 1520


def plate(n, total=6, w=740, h=250):
    """black peg letterboard (mugshot board): white letters «FLORIDA MAN», coral «EPISODE N/6», a strip of height-chart lines on top"""
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, h - 1], fill=INK + (255,))
    d.rectangle([12, 12, w - 13, h - 13], fill=(18, 20, 24, 255))
    for y in range(28, h - 20, 18): d.line([(24, y), (w - 24, y)], fill=(30, 32, 38, 255))
    for x in range(30, w - 20, 34): d.rectangle([x, 14, x + 4, 30 if (x // 34) % 2 else 22], fill=(200, 210, 214, 255))
    t1, t2 = 'FLORIDA MAN', f'EPISODE {n}/{total}'
    s1 = int(h * 0.25)
    while O.pfont(s1).getbbox(t1)[2] - O.pfont(s1).getbbox(t1)[0] > w - 60: s1 -= 2       # always inside the board
    s2 = int(s1 * 0.52)
    f1, f2 = O.pfont(s1), O.pfont(s2)
    b1, b2 = f1.getbbox(t1), f2.getbbox(t2)
    y1_ = int(h * 0.30); y2_ = int(h * 0.68)
    d.text(((w - (b1[2] - b1[0])) // 2 - b1[0], y1_ - b1[1]), t1, font=f1, fill=(246, 246, 240, 255))
    d.text(((w - (b2[2] - b2[0])) // 2 - b2[0], y2_ - b2[1]), t2, font=f2, fill=(255, 132, 110, 255))
    return np.array(img)


def make(frame, title, n=1, out='cover.png', title_y=None, title_size=104, plate_y=None, shift=0, grid_preview=True):
    """plate at the top of the 3:4 grid zone, title right under it, soft dark band behind both; shift moves the scene down"""
    big = frame.copy()
    if shift > 0: big = np.concatenate([np.repeat(big[:1], shift, 0), big[:-shift]], 0)
    p = plate(n, w=600, h=190)
    py = GRID[0] + 22 if plate_y is None else plate_y
    t = K.hook_title(title, title_size, depth=16)
    ty = py + p.shape[0] + 4 if title_y is None else title_y
    y1 = ty + t.shape[0]
    shade = np.zeros((big.shape[0], 1, 1), np.float32)
    shade[GRID[0]:y1, 0, 0] = 0.40
    n_ = len(shade[y1:y1 + 140]); shade[y1:y1 + n_, 0, 0] = np.linspace(0.40, 0.0, 140)[:n_]
    big = (big * (1 - shade)).astype(np.uint8)
    O.overlay(big, p, (big.shape[1] - p.shape[1]) // 2, py, 1.0)
    O.overlay(big, t, 0, ty, 1.0)
    Image.fromarray(big).save(out)
    if grid_preview:                                        # what the profile grid shows (3:4 crop + date / views overlay)
        g = big[GRID[0]:GRID[1]].copy()
        g[SAFE_BOTTOM - GRID[0]:] = (g[SAFE_BOTTOM - GRID[0]:] * 0.45).astype(np.uint8)
        Image.fromarray(g).resize((270, 360), Image.LANCZOS).save(str(out).replace('.png', '_grid.png'))
    return big
