"""S02E05 cover «ПОСЫПАНО?!» — code only: Valera flying across the icy yard on his back past the «ПОСЫПАНО. УК «УЮТ»» sign.
  python3 cover.py   ->  cover.png, covers/cover_s02e05.png, cover_grid.png"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import covergen2 as CG
import s2e05 as E

HERE = pathlib.Path(__file__).resolve().parent
big = E.r_hook(0.9, 1.4, gy=585.0)
dst = P.series(E.TL.SLUG) / 'covers'; dst.mkdir(exist_ok=True)
CG.code_cover(big, 'ВАЛЕРА И КОТ\nСЕЗОН 2 • 5/6', ['ПОСЫПАНО?!'], [HERE / 'cover.png', dst / 'cover_s02e05.png'])
print(HERE / 'cover.png')
