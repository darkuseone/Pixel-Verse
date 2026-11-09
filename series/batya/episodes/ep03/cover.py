"""E03 cover «КОВЁР — НА СНЕГ!» — code only: Batya shouting with the carpet roll under his arm, first snow;
tape-measure plate + knitted title on top (profile grid: plate at y≈260, title under it, faces below, nothing important under y 1520).
  python3 cover.py -> cover.png, covers/cover_s01e03.png, cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import overlays as O
import ep03 as E
from stage import view_at
from props import batyacast as B
from props import batyakit as K

HERE = pathlib.Path(__file__).resolve().parent


def frame(t=0.41):
    v = view_at(E.YARD, 590, 300, 1.4, 180, 230)
    st = {}

    def draw(CH, v_):
        cam = v_.cam(575, E.YF + 70, E.YU * 1.55)
        r = B.batya(CH, cam, dict(B.BPOSE['stand'], bn=-1), t=t, mouth_=0.8, expr='shout', hat=True, frost=0.4,
                    hand_n=E.F.H(3.0, 15.0), prop_n=E.roll_on_shoulder)
        st.update(cam=cam, r=r)
    return E.yard(v, t, draw)


def cover(big):
    out = big.astype(np.float32)
    shade = np.zeros((out.shape[0], 1, 1), np.float32); shade[:640] = 0.5; shade[640:820, 0, 0] = np.linspace(0.5, 0.0, 180)
    out = (out * (1 - shade)).astype(np.uint8)
    tp = K.tape(820, 150, ['БАТЯ САМ', 'СЕРИЯ 3/6'])
    O.overlay(out, tp, (1080 - tp.shape[1]) // 2, 230, 1.0)
    ttl = K.title_trim(K.hook_title(['КОВЁР —', 'НА СНЕГ!'], 96, width=1500))
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
    for o in (HERE / 'cover.png', dst / 'cover_s01e03.png'): img.save(o)
    grid(); print(HERE / 'cover.png')
