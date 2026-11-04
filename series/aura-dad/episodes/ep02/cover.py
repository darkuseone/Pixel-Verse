"""E02 cover «$340 SKINCARE?!» — Doug screaming with the endless receipt, Lily in her bunny headband in front. python3 cover.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from PIL import Image
import paths as P
import ep02 as E
from stage import view_at
from props import auracast as A
from props import aurakit as K

HERE = pathlib.Path(__file__).resolve().parent


def frame(t=0.4):
    v = view_at(E.KIT, 800, 650, 1.32, 180, 640)

    def draw(CH, v_):
        E.doug_at(CH, v_, t, (850.0, 650.0, 12.0), flip=True, expr='shout', pose=A.DPOSE['shout'], mouth_=0.85,
                  prop_n=lambda L, h: A.receipt(L, h, 12.0, 1.0))
        E.char_at(A.lily, 'lily', CH, v_, t, (730.0, 700.0, 15.0), expr='happy', pose=A.LPOSE['show'], prop_n=A.jar)
    return E.kitchen(v, t, draw)


if __name__ == '__main__':
    dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
    big = K.cover_make(frame(), ['$340 SKINCARE?!'], 2, out=str(HERE / 'cover.png'))
    Image.fromarray(big).save(dst / 'cover_s01e02.png')
    print(HERE / 'cover.png')
