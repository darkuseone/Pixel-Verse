"""E06 cover «AURA BATTLE?!» — Doug vs Brett face to face, kids with phones. python3 cover.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
from PIL import Image
import paths as P
import ep06 as E
from stage import view_at
from props import auracast as A
from props import aurakit as K

HERE = pathlib.Path(__file__).resolve().parent


def frame(t=0.4):
    v = view_at(E.CUL, 650, 600, 1.25, 180, 760)

    def draw(CH, v_):
        E.brett_at(CH, v_, t, (E.BX - 20, E.FY, 10.0), expr='smug', pose=A.BPOSE['flex'])
        E.doug_at(CH, v_, t, (E.DX + 20, E.FY + 10, 10.4), expr='angry', pose=A.DPOSE['fists'], mouth_=0.0)
    return E.cul(v, t, draw)


if __name__ == '__main__':
    dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
    big = K.cover_make(frame(), ['AURA BATTLE?!'], 6, out=str(HERE / 'cover.png'))
    Image.fromarray(big).save(dst / 'cover_s01e06.png')
    print(HERE / 'cover.png')
