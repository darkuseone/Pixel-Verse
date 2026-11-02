"""E04 cover «ШАПКУ НАДЕНЬ!» — code only: Raisa yanks a pompom hat onto Tolik in the hallway;
doily plate + «тёщин халат» title.   python3 cover.py -> cover.png, covers/cover_s01e04.png, cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import overlays as O
import ep04 as E
from stage import view_at
from scene import Layer
from props import teshcast as T
from props import teshkit as K
from props import teshshots as SH

HERE = pathlib.Path(__file__).resolve().parent


def frame(t=0.41):
    v = view_at(E.HALL, 635, 290, 1.22, 180, 300)

    def draw(CH, v_):
        E.tolik(CH, v_, t, expr='shout', pose='stand', m=0.8)
        E.raisa(CH, v_, t, pose=dict(E.T.RPOSE['offer'], n=(7.4, 21.4), f=(6.2, 20.4), bf=1), expr='sweet')
    return E.hall(v, t, draw)


def cover(big):
    out = big.astype(np.float32)
    shade = np.zeros((out.shape[0], 1, 1), np.float32); shade[:700] = 0.45; shade[700:860, 0, 0] = np.linspace(0.45, 0.0, 160)
    out = (out * (1 - shade)).astype(np.uint8)
    d = K.doily(780, 210, ['ТЁЩА НА НЕДЕЛЬКУ', 'СЕРИЯ 4/6'])
    O.overlay(out, d, (1080 - d.shape[1]) // 2, 250, 1.0)
    ttl = K.title_trim(K.hook_title(['ШАПКУ', 'НАДЕНЬ!'], 84, width=1400))
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
    for o in (HERE / 'cover.png', dst / 'cover_s01e04.png'): img.save(o)
    grid(); print(HERE / 'cover.png')
