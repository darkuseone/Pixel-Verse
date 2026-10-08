"""Covers of «Grim Ride» (US): code-drawn frame from the series' own world + sprites (no AI faces), title in the series style
(neon-yellow -> pumpkin stepped fill, violet-black outline, acid-green halo: props/grimkit.hook_title) and a mossy tombstone plate
«GRIM RIDE / EPISODE N/6». Faces and text sit inside the central 3:4 zone (y 240..1680 of 1080x1920).
  from covergen_grim import make;  make(frame_rgb, ['DEATH GOT', 'AN E-BIKE?'], n=1, out='cover.png')"""
import numpy as np
from PIL import Image, ImageDraw
import overlays as O
from props import grimkit as K

INK = K.INK
STONE = (150, 146, 170)


def plate(n, total=6, w=700, h=230):
    """tombstone plate: rounded top, grey stone with stipple and a crack, green moss at the bottom, «GRIM RIDE» + «EPISODE N/6»"""
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    r = 110
    d.rectangle([0, r, w - 1, h - 1], fill=INK); d.pieslice([0, 0, w - 1, 2 * r], 180, 360, fill=INK)
    d.rectangle([12, r, w - 13, h - 13], fill=STONE); d.pieslice([12, 12, w - 13, 2 * r - 12], 180, 360, fill=STONE)
    a = np.array(img)
    rng = np.random.default_rng(31)
    st = (a[..., :3] == STONE).all(-1) & (rng.random((h, w)) < 0.10)
    a[st] = (112, 106, 136, 255)
    yy, xx = np.mgrid[0:h, 0:w]
    moss = (a[..., 3] > 0) & ~(a[..., :3] == INK).all(-1) & (yy > h - 46 + 10 * np.sin(xx / 23.0))
    a[moss] = (90, 170, 70, 255)
    img = Image.fromarray(a); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.line([(w - 120, 60), (w - 100, 100), (w - 130, 140)], fill=(90, 84, 110), width=6)          # crack
    f1, f2 = O.pfont(60), O.pfont(30)
    t1 = 'GRIM RIDE'; b1 = f1.getbbox(t1)
    d.text(((w - (b1[2] - b1[0])) // 2 - b1[0] + 4, 64 - b1[1] + 4), t1, font=f1, fill=(60, 50, 80))
    d.text(((w - (b1[2] - b1[0])) // 2 - b1[0], 64 - b1[1]), t1, font=f1, fill=(250, 246, 236))
    t2 = f'EPISODE {n}/{total}'; b2 = f2.getbbox(t2)
    d.text(((w - (b2[2] - b2[0])) // 2 - b2[0], 146 - b2[1]), t2, font=f2, fill=(255, 150, 40))
    return np.array(img)


def make(frame, title, n=1, out='cover.png', title_y=250, title_size=80, plate_y=1470):
    big = frame.copy()
    t = K.hook_title(title, title_size)
    O.overlay(big, t, 0, title_y, 1.0)
    p = plate(n)
    O.overlay(big, p, (big.shape[1] - p.shape[1]) // 2, plate_y, 1.0)
    Image.fromarray(big).save(out)
    return big
