"""E02 cover «7 УТРА. ГРОМКОСТЬ 100!» — code only: Raisa in Tolik's armchair, the TV at volume 100 in front, Tolik behind with a
pillow, screaming; doily plate + «тёщин халат» title.   python3 cover.py -> cover.png, covers/cover_s01e02.png, cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import overlays as O
import ep02 as E
from stage import view_at
from scene import Layer
from props import teshcast as T
from props import teshkit as K
from props import teshshots as SH

HERE = pathlib.Path(__file__).resolve().parent


def frame(t=0.41):
    v = view_at(SH.ROOM, 700, 380, 1.3, 180, 330)

    def draw(CH, v_):
        c2 = v_.cam(792.0, 705.0, 13.0, flip=True)
        T.tolik(CH, c2, T.TPOSE['shock'], t=t, mouth_=1.0, expr='scream')
        SH.chair(CH, v_, 0.85, 'back')
        cam, r = SH.raisa_sit(CH, v_, t, s=0.85, unit=15.0, expr='sweet', look=0.8)
        SH.chair(CH, v_, 0.85, 'front')
        E.tv(CH, v_, t, 100, x=760, y=660, s=1.5)
    return SH.room(v, t, draw, tv=1.0)


def cover(big):
    out = big.astype(np.float32)
    shade = np.zeros((out.shape[0], 1, 1), np.float32); shade[:700] = 0.45; shade[700:860, 0, 0] = np.linspace(0.45, 0.0, 160)
    out = (out * (1 - shade)).astype(np.uint8)
    d = K.doily(780, 210, ['ТЁЩА НА НЕДЕЛЬКУ', 'СЕРИЯ 2/6'])
    O.overlay(out, d, (1080 - d.shape[1]) // 2, 250, 1.0)
    ttl = K.title_trim(K.hook_title(['7 УТРА.', 'ГРОМКОСТЬ 100!'], 84, width=1400))
    if ttl.shape[1] > 1040:
        f = 1040 / ttl.shape[1]; ttl = np.array(Image.fromarray(ttl).resize((int(ttl.shape[1] * f), int(ttl.shape[0] * f)), Image.NEAREST))
    O.overlay(out, ttl, (1080 - ttl.shape[1]) // 2, 500, 1.0)
    return out


def grid():
    im = Image.open(HERE / 'cover.png'); w, h = im.size; h34 = int(w * 4 / 3); y0 = (h - h34) // 2
    im.crop((0, y0, w, y0 + h34)).resize((w // 4, h34 // 4), Image.LANCZOS).save(HERE / 'cover_grid.png')


if __name__ == '__main__':
    img = Image.fromarray(cover(frame()))
    dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
    for o in (HERE / 'cover.png', dst / 'cover_s01e02.png'): img.save(o)
    grid(); print(HERE / 'cover.png')
