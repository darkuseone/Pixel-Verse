"""E01 cover «MINUS 400?!» — code only: Doug's shocked face in the kitchen + Kayden's phone «-400»; the AURA DAD app badge at the
top of the 3:4 grid zone and the holographic title under it.   python3 cover.py -> cover.png, cover_grid.png, covers/cover_s01e01.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from PIL import Image
import paths as P
import ep01 as E
from stage import view_at
from props import auracast as A
from props import aurakit as K

HERE = pathlib.Path(__file__).resolve().parent


def frame(t=0.4):
    x, y, un = E.DOUG
    k = 1.3
    hy = y - 25.4 * un * k
    v = view_at(E.KIT, x - 0.6 * un * k, hy, 1.4, 180, 330 + 300 / 1.4 * 0.0 + 260)

    def draw(CH, v_):
        E.doug_at(CH, v_, t, (x, y, un), k, expr='shout', pose=A.DPOSE['shout'], mouth_=0.85)
    big = E.kitchen(v, t, draw)
    E.phone_big(big, -400, t, 720, 1020, 0.6)
    return big


if __name__ == '__main__':
    dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
    big = K.cover_make(frame(), ['MINUS 400?!'], 1, out=str(HERE / 'cover.png'))
    Image.fromarray(big).save(dst / 'cover_s01e01.png')
    print(HERE / 'cover.png')
