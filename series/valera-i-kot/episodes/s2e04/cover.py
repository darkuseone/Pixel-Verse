"""S02E04 cover «ШТРАФ ЗА СЧЁТЧИК?!» — code only: the peephole fisheye with the two «поверщики» in orange vests; plank + title.
  python3 cover.py   ->  cover.png, covers/cover_s02e04.png, cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen2 as CG
import overlays as O
import s2e04 as E

HERE = pathlib.Path(__file__).resolve().parent
from stage import view_at
t = 1.1
v = view_at(E.LAND, 672, 230, 1.2, 180, 330)
big = E.landing(v, t, lambda CH, v_: E.duo(CH, v_, t, E.S_PEEP, E.K_PEEP, sexpr='smug', kexpr='sly'))
for (x, y) in ((E.S_PEEP[0] - 1.0 * E.S_PEEP[2], E.S_PEEP[1] - 13.4 * E.S_PEEP[2]), (E.K_PEEP[0] - 1.0 * E.K_PEEP[2], E.K_PEEP[1] - 16.0 * E.K_PEEP[2])):
    E.D.blit(big, v, E.VEST_TAG, x - 11, y, ws=4)
st = O.sticker('ШТРАФ 5 000', fg=(255, 120, 110), size=72)
O.overlay(big, st, 1080 - st.shape[1] - 30, 1420, 1.0)
dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
CG.code_cover(big, 'ВАЛЕРА И КОТ\nСЕЗОН 2 • 4/6', ['ШТРАФ ЗА', 'СЧЁТЧИК?!'], [HERE / 'cover.png', dst / 'cover_s02e04.png'])
print(HERE / 'cover.png')
