"""S02E01 cover «+14 ДОМА?!» — built from code only (owner 22.10.2026: no xAI edit, no neural faces): the series' kitchen,
shivering Valera in the ushanka with icicles, the cold cat on the radiator, snow through the open pane, the big «+14» thermometer;
blue enamel plank at the top of the 3:4 grid zone and the frosty title under it (covergen2.enamel_plank / title).
  python3 cover.py [Z sy dx]   ->  cover.png, covers/cover_s02e01.png, cover_grid.png"""
import sys, pathlib, math; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import numpy as np
from PIL import Image
import paths as P
import covergen2 as CG
import overlays as O
import s2e01 as E
from stage import view_at
from props import panelka as PK

HERE = pathlib.Path(__file__).resolve().parent
TITLE = ['+14 ДОМА?!']
PLANK = 'ВАЛЕРА И КОТ\nСЕЗОН 2 • 1/6'


def frame(Z=1.55, sy=360, dx=-10.0, t=0.37):
    x, y, un = 745.0, 660.0, 16.5                                        # Valera right by the radiator (closer than in the episode)
    fx_, fy_ = E.face_w(x, y, un, flip=True, h=20.6)
    v = view_at(E.KIT, 680 + dx, fy_, Z, 180, sy)

    def draw(CH, v_):
        E.v_cold(CH, v_, t, (x, y, un), 'shiver', 'shout', cold=0.56)
    big = E.kitchen(v, t, draw, snow=70, cat_kw=dict(mouth=0.0, lid=0.55, tail=0.2, expr='grumpy', tint=(0.86, 0.95, 1.18)))
    E.breath(big, v, t, fx_ - 30, fy_ + 10)
    th = E.img_thermo_big()
    th = np.array(Image.fromarray(th).resize((th.shape[1] * 3 // 4, th.shape[0] * 3 // 4), Image.NEAREST))
    O.overlay(big, th, 1080 - th.shape[1] - 12, 1080, 1.0)
    return big


def cover(big):
    """plank + title drawn on the 540x960 cover grid, pasted 2x over the full-res code frame (scene keeps its own pixel)"""
    small = np.array(Image.fromarray(big).resize((CG.W, CG.H), Image.NEAREST))
    F = small.copy()
    yb = CG.enamel_plank(F, PLANK, 136, 24)
    CG.title(F, TITLE, yb + 22, 64, max_w=524, gap=10)
    m = np.any(F != small, axis=2)
    m2 = np.repeat(np.repeat(m, 2, 0), 2, 1)
    F2 = np.repeat(np.repeat(F, 2, 0), 2, 1)
    out = big.astype(np.float32)
    shade = np.zeros((out.shape[0], 1, 1), np.float32)                    # dark band under plank + title, fading down
    shade[:560] = 0.42
    shade[560:720, 0, 0] = np.linspace(0.42, 0.0, 160)
    out = (out * (1 - shade)).astype(np.uint8)
    out[m2] = F2[m2]
    return out


def grid():
    """TikTok / Reels profile tile preview: the 3:4 centre crop at 1/4 size"""
    im = Image.open(HERE / 'cover.png')
    w, h = im.size; h34 = int(w * 4 / 3); y0 = (h - h34) // 2
    im.crop((0, y0, w, y0 + h34)).resize((w // 4, h34 // 4), Image.LANCZOS).save(HERE / 'cover_grid.png')
    print(HERE / 'cover_grid.png')


if __name__ == '__main__':
    a = [float(s) for s in sys.argv[1:]]
    img = Image.fromarray(cover(frame(*a)))
    dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
    for o in (HERE / 'cover.png', dst / 'cover_s02e01.png'): img.save(o)
    print(HERE / 'cover.png')
    grid()
