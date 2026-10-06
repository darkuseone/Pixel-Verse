"""Covers of «Мазутыч» (RU): code-drawn frame from the series' own world + sprites (no AI faces), title in the series style
(oil-slick gradient fill, thick crude-oil outline with drips: props/mazkit.hook_title) and a yellow-black hazard plate
«МАЗУТЫЧ • СЕРИЯ N/6». Faces and text sit inside the central 3:4 zone (y 240..1680 of 1080x1920).
  from covergen_maz import make;  make(frame_rgb, ['НЕФТЯНИК', 'БЕЗ БЕНЗИНА'], n=1, out='cover.png')"""
import numpy as np
from PIL import Image, ImageDraw
import overlays as O
from props import mazkit as K

INK = K.INK


def plate(n, total=6, w=820, h=150):
    """hazard plate: black-yellow diagonal stripes frame, black field, white «МАЗУТЫЧ» + amber «СЕРИЯ N/6»"""
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, h - 1], fill=INK)
    a = np.array(img)
    yy, xx = np.mgrid[0:h, 0:w]
    stripe = ((xx + yy) // 28) % 2 == 0
    border = (xx < 22) | (xx >= w - 22) | (yy < 18) | (yy >= h - 18)
    a[border & stripe] = (250, 204, 40, 255)
    a[border & ~stripe] = (24, 18, 14, 255)
    img = Image.fromarray(a); d = ImageDraw.Draw(img); d.fontmode = '1'
    f1, f2 = O.pfont(54), O.pfont(28)
    t1 = 'МАЗУТЫЧ'; b1 = f1.getbbox(t1)
    d.text(((w - (b1[2] - b1[0])) // 2 - b1[0], 32 - b1[1]), t1, font=f1, fill=(250, 244, 228))
    t2 = f'СЕРИЯ {n}/{total}'; b2 = f2.getbbox(t2)
    d.text(((w - (b2[2] - b2[0])) // 2 - b2[0], 100 - b2[1]), t2, font=f2, fill=(255, 168, 40))
    return np.array(img)


def make(frame, title, n=1, out='cover.png', title_y=250, title_size=78, plate_y=1530):
    big = frame.copy()
    t = K.hook_title(title, title_size)
    O.overlay(big, t, 0, title_y, 1.0)
    p = plate(n)
    O.overlay(big, p, (big.shape[1] - p.shape[1]) // 2, plate_y, 1.0)
    Image.fromarray(big).save(out)
    return big
