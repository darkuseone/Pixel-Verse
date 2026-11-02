"""E01 cover «Я К ВАМ НА НЕДЕЛЬКУ!» — code only (no xAI edit, no neural faces): the landing, Tolik screaming in the doorway, the
mother-in-law in curlers with Pusya and the plaid bags in front; the embroidered doily plate at the top of the 3:4 grid zone and the
«тёщин халат» title under it.   python3 cover.py  ->  cover.png, series covers/cover_s01e01.png, cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import overlays as O
import ep01 as E
from stage import view_at
from scene import Layer
from props import teshcast as T
from props import teshkit as K

HERE = pathlib.Path(__file__).resolve().parent


def frame(t=0.41):
    x, y, un = E.DOOR
    k = 1.32
    hy = y + 70 - 27.2 * un * k
    v = view_at(E.LAND, 905, hy, 1.42, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(1000, 640, un * 1.15, flip=True)
        T.tolik(CH, cam, T.TPOSE['shock'], t=t, mouth_=0.9, expr='shout')
        L = Layer(v_.wcam()); T.chelnok(L, 1000, 640, 120, 92, 0.06, 4); T.chelnok(L, 1070, 660, 110, 86, -0.05, 2); CH.add(L)
        cam2 = v_.cam(830, 680, 18.0)
        r = T.raisa(CH, cam2, T.RPOSE['hold'], t=t, expr='sweet')
        px, py = E.u2w(v_, cam2, (1003.4, 990.4))
        T.pusya(CH, v_.cam(px, py, 18.0 * 0.62), t=t, expr='deadpan')
    return E.landing(v, t, draw, extra_pile=False)


def cover(big):
    out = big.astype(np.float32)
    shade = np.zeros((out.shape[0], 1, 1), np.float32)
    shade[:700] = 0.45
    shade[700:860, 0, 0] = np.linspace(0.45, 0.0, 160)
    out = (out * (1 - shade)).astype(np.uint8)
    d = K.doily(780, 210, ['ТЁЩА НА НЕДЕЛЬКУ', 'СЕРИЯ 1/6'])
    O.overlay(out, d, (1080 - d.shape[1]) // 2, 250, 1.0)
    ttl = K.title_trim(K.hook_title(['Я К ВАМ', 'НА НЕДЕЛЬКУ!'], 84, width=1400))
    if ttl.shape[1] > 1040:
        f = 1040 / ttl.shape[1]
        ttl = np.array(Image.fromarray(ttl).resize((int(ttl.shape[1] * f), int(ttl.shape[0] * f)), Image.NEAREST))
    O.overlay(out, ttl, (1080 - ttl.shape[1]) // 2, 500, 1.0)
    return out


def grid():
    im = Image.open(HERE / 'cover.png')
    w, h = im.size; h34 = int(w * 4 / 3); y0 = (h - h34) // 2
    im.crop((0, y0, w, y0 + h34)).resize((w // 4, h34 // 4), Image.LANCZOS).save(HERE / 'cover_grid.png')
    print(HERE / 'cover_grid.png')


if __name__ == '__main__':
    img = Image.fromarray(cover(frame()))
    dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
    for o in (HERE / 'cover.png', dst / 'cover_s01e01.png'): img.save(o)
    print(HERE / 'cover.png')
    grid()
