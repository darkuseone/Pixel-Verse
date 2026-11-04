"""E05 cover «$200 HAIR?!» — bald Doug pouring the serum, the maned basset in front. python3 cover.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from PIL import Image
import paths as P
import ep05 as E
from stage import view_at
from props import auracast as A
from props import aurakit as K
from props import folk as F

HERE = pathlib.Path(__file__).resolve().parent


def frame(t=0.4):
    v = view_at(E.BATH, 640, 640, 1.2, 180, 720)

    def draw(CH, v_):
        E.doug_at(CH, v_, t, (720.0, 668.0, 13.6), expr='shock', pose=A.DPOSE['stand'], hand_n=F.H(1.6, 32.4), mouth_=0.7, wet=1.0,
                  prop_n=lambda L, h: A.serum(L, (h[0], h[1] + 2.4)))
        E.dog_at(CH, v_, t, (520.0, 700.0, 13.0), mane=1.0, wind=1.0)
    return E.bathroom(v, t, draw, 0.0, 'smug', morning=True)


if __name__ == '__main__':
    dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
    big = K.cover_make(frame(), ['$200 HAIR?!'], 5, out=str(HERE / 'cover.png'))
    Image.fromarray(big).save(dst / 'cover_s01e05.png')
    print(HERE / 'cover.png')
