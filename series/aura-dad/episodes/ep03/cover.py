"""E03 cover «AURA FARMING?!» — Doug in shades, cool pose with the spatula, the pool behind. python3 cover.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from PIL import Image
import paths as P
import ep03 as E
from stage import view_at
from props import auracast as A
from props import aurakit as K

HERE = pathlib.Path(__file__).resolve().parent


def frame(t=0.4):
    v = view_at(E.YARD, 470, 600, 1.25, 180, 760)

    def draw(CH, v_):
        E.doug_at(CH, v_, t, (480.0, 610.0, 12.5), expr='smug', pose=A.DPOSE['point'], mouth_=0.0, shine=1.0, prop_n=E.spatula)
    return E.yard(v, t, draw)


if __name__ == '__main__':
    dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
    big = K.cover_make(frame(), ['AURA FARMING?!'], 3, out=str(HERE / 'cover.png'))
    Image.fromarray(big).save(dst / 'cover_s01e03.png')
    print(HERE / 'cover.png')
