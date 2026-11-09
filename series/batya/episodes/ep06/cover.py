"""E06 cover «ДЕНЬ МАТЕРИ — ПОДАРОК САМИ!» — code only: proud Batya with the three-legged stool, babushka reaching for it;
tape-measure plate + knitted title on top (profile grid: plate at y≈260, title under it, faces below, nothing important under y 1520).
  python3 cover.py -> cover.png, covers/cover_s01e06.png, cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import overlays as O
import ep06 as E
from stage import view_at
from props import batyacast as B
from props import batyakit as K

HERE = pathlib.Path(__file__).resolve().parent


def frame(t=0.41):
    v = view_at(E.GAR, 640, 215, 1.0, 180, 230)

    def draw(CH, v_):
        L = E.Layer(v_.wcam())
        E.stool(L, 660, 585, 1.3, 0.14)
        E.F.outline(L, E.OL); CH.add(L)
        cam = v_.cam(790, E.GF - 30, 16.0, flip=True)
        B.babushka(CH, cam, dict(B.IPOSE['stand'], n=(4.5, 18.0), f=(-4.0, 18.0)), t=t, mouth_=0.8, expr='happy')
        cam = v_.cam(530, E.GF + 30, 18.0)
        B.batya(CH, cam, B.BPOSE['point'], t=t, mouth_=0.8, expr='proud')
    return E.garage(v, t, draw)


def cover(big):
    out = big.astype(np.float32)
    shade = np.zeros((out.shape[0], 1, 1), np.float32); shade[:640] = 0.5; shade[640:820, 0, 0] = np.linspace(0.5, 0.0, 180)
    out = (out * (1 - shade)).astype(np.uint8)
    tp = K.tape(820, 150, ['БАТЯ САМ', 'СЕРИЯ 6/6'])
    O.overlay(out, tp, (1080 - tp.shape[1]) // 2, 230, 1.0)
    ttl = K.title_trim(K.hook_title(['ДЕНЬ МАТЕРИ —', 'ПОДАРОК САМИ!'], 96, width=1900))
    if ttl.shape[1] > 1020:
        f = 1020 / ttl.shape[1]; ttl = np.array(Image.fromarray(ttl).resize((int(ttl.shape[1] * f), int(ttl.shape[0] * f)), Image.NEAREST))
    O.overlay(out, ttl, (1080 - ttl.shape[1]) // 2, 410, 1.0)
    return out


def grid():
    im = Image.open(HERE / 'cover.png'); w, h = im.size; h34 = int(w * 4 / 3); y0 = (h - h34) // 2
    im.crop((0, y0, w, y0 + h34)).resize((w // 4, h34 // 4), Image.LANCZOS).save(HERE / 'cover_grid.png')


if __name__ == '__main__':
    img = Image.fromarray(cover(frame()))
    dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
    for o in (HERE / 'cover.png', dst / 'cover_s01e06.png'): img.save(o)
    grid(); print(HERE / 'cover.png')
