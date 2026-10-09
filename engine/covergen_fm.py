"""Covers of «Florida Man: Allegedly» (US): code-drawn frame from the series' own world + sprites (no AI faces), title as
«Greetings from Florida» postcard letters (yellow -> coral -> magenta, white outline, teal 3D extrusion: props/fmkit.hook_title) and a
booking letterboard plate «FLORIDA MAN / EPISODE N/6» on a mugshot height-chart strip. Faces and text sit inside the central 3:4 zone
(y 240..1680 of 1080x1920).
  from covergen_fm import make;  make(frame_rgb, ['NINE', 'GRAND?!'], n=1, out='cover.png')"""
import numpy as np
from PIL import Image, ImageDraw
import overlays as O
from props import fmkit as K

INK = K.INK


def plate(n, total=6, w=740, h=250):
    """black peg letterboard (mugshot board): white letters «FLORIDA MAN», coral «EPISODE N/6», a strip of height-chart lines on top"""
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, h - 1], fill=INK + (255,))
    d.rectangle([12, 12, w - 13, h - 13], fill=(18, 20, 24, 255))
    for y in range(28, h - 20, 18): d.line([(24, y), (w - 24, y)], fill=(30, 32, 38, 255))
    for x in range(30, w - 20, 34): d.rectangle([x, 14, x + 4, 30 if (x // 34) % 2 else 22], fill=(200, 210, 214, 255))
    f1, f2 = O.pfont(62), O.pfont(32)
    t1 = 'FLORIDA MAN'; b1 = f1.getbbox(t1)
    d.text(((w - (b1[2] - b1[0])) // 2 - b1[0], 70 - b1[1]), t1, font=f1, fill=(246, 246, 240, 255))
    t2 = f'EPISODE {n}/{total}'; b2 = f2.getbbox(t2)
    d.text(((w - (b2[2] - b2[0])) // 2 - b2[0], 170 - b2[1]), t2, font=f2, fill=(255, 132, 110, 255))
    return np.array(img)


def make(frame, title, n=1, out='cover.png', title_y=230, title_size=110, plate_y=1440):
    big = frame.copy()
    t = K.hook_title(title, title_size, depth=18)
    O.overlay(big, t, 0, title_y, 1.0)
    p = plate(n)
    O.overlay(big, p, (big.shape[1] - p.shape[1]) // 2, plate_y, 1.0)
    Image.fromarray(big).save(out)
    return big
