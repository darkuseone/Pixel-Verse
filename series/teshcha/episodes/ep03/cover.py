"""E03 cover «ЕЩЁ ТАРЕЛОЧКУ?!» — code only: Tolik with full cheeks at the food mountain, Raisa behind with a plate;
doily plate + «тёщин халат» title.   python3 cover.py -> cover.png, covers/cover_s01e03.png, cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import overlays as O
import ep03 as E
from stage import view_at
from scene import Layer
from props import teshcast as T
from props import teshkit as K
from props import teshshots as SH

HERE = pathlib.Path(__file__).resolve().parent


def frame(t=0.41):
    v = view_at(E.KIT, 890, 340, 1.42, 170, 300)

    def draw(CH, v_):
        E.raisa_st(CH, v_, t, 'sweet', pos=(790, 700, 15.6), prop_n=E.held_plate('cutlet'))
        E.tolik_sit(CH, v_, t, 'whine', k=1.25)
        E.food_table(CH, v_, t, 3)
    return E.kitchen(v, t, draw, steam=(1250, E.TOP - 60))


def cover(big):
    out = big.astype(np.float32)
    shade = np.zeros((out.shape[0], 1, 1), np.float32); shade[:700] = 0.45; shade[700:860, 0, 0] = np.linspace(0.45, 0.0, 160)
    out = (out * (1 - shade)).astype(np.uint8)
    d = K.doily(780, 210, ['ТЁЩА НА НЕДЕЛЬКУ', 'СЕРИЯ 3/6'])
    O.overlay(out, d, (1080 - d.shape[1]) // 2, 250, 1.0)
    ttl = K.title_trim(K.hook_title(['ЕЩЁ', 'ТАРЕЛОЧКУ?!'], 84, width=1400))
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
    for o in (HERE / 'cover.png', dst / 'cover_s01e03.png'): img.save(o)
    grid(); print(HERE / 'cover.png')
