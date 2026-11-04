"""E04 cover «HE MOGGED ME?!» — tiny-headed giant Brett flexing, Doug looking up in shock. python3 cover.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from PIL import Image
import paths as P
import ep04 as E
from stage import view_at
from props import auracast as A
from props import aurakit as K

HERE = pathlib.Path(__file__).resolve().parent


def frame(t=0.4):
    v = view_at(E.CUL, 650, 590, 1.3, 180, 760)

    def draw(CH, v_):
        E.brett_at(CH, v_, t, (E.BX, E.FY, 10.0), expr='smug', pose=A.BPOSE['flex'], lift=6.0)
        E.doug_at(CH, v_, t, (E.DX + 20, E.FY + 20, 10.4), expr='shout', pose=A.DPOSE['shout'], look=0.0, mouth_=0.8)
    return E.cul(v, t, draw)


if __name__ == '__main__':
    dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
    big = K.cover_make(frame(), ['HE MOGGED ME?!'], 4, out=str(HERE / 'cover.png'))
    Image.fromarray(big).save(dst / 'cover_s01e04.png')
    print(HERE / 'cover.png')
