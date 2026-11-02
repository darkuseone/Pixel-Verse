"""E06 cover «ТЁЩА УЕЗЖАЕТ?!» — code only: Raisa at the door with bags and Pusya, Tolik stunned;
doily plate + «тёщин халат» title.   python3 cover.py -> cover.png, covers/cover_s01e06.png, cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import overlays as O
import ep06 as E
from stage import view_at
from scene import Layer
from props import teshcast as T
from props import teshkit as K
from props import teshshots as SH

HERE = pathlib.Path(__file__).resolve().parent


def frame(t=0.41):
    v = view_at(E.HALL, 850, 285, 1.2, 180, 300)

    def draw(CH, v_):
        L = E.Layer(v_.wcam()); E.T.chelnok(L, 985, 700, 80, 62, 0.1, 21); E.T.chelnok(L, 1010, 650, 66, 50, -0.12, 22); CH.add(L)
        cam, r = E.raisa(CH, v_, t, 948, 700, 15.6, pose='hold', flip=True, expr='sweet', look=0.4)
        wx, wy = E.u2w(v_, cam, r['hand_n'])
        c = v_.cam(wx + 4, wy + 2.6 * 5.6, 5.6); rp = E.T.pusya(CH, c, t=t, expr='smug', shiver=1.2); E.face(v_, c, rp, 2.0)
        E.tolik(CH, v_, t, 742, 692, 15.0, pose='shock', expr='shock', m=0.8)
    return E.hall(v, t, draw)


def cover(big):
    out = big.astype(np.float32)
    shade = np.zeros((out.shape[0], 1, 1), np.float32); shade[:700] = 0.45; shade[700:860, 0, 0] = np.linspace(0.45, 0.0, 160)
    out = (out * (1 - shade)).astype(np.uint8)
    d = K.doily(780, 210, ['ТЁЩА НА НЕДЕЛЬКУ', 'СЕРИЯ 6/6'])
    O.overlay(out, d, (1080 - d.shape[1]) // 2, 250, 1.0)
    ttl = K.title_trim(K.hook_title(['ТЁЩА', 'УЕЗЖАЕТ?!'], 84, width=1400))
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
    for o in (HERE / 'cover.png', dst / 'cover_s01e06.png'): img.save(o)
    grid(); print(HERE / 'cover.png')
