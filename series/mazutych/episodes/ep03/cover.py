"""Cover S01E03 v2 «Из-под полы»: the hook frame — Мазутыч in price shock with the «gasoline» bottle and its «500» tag;
title «БЕНЗИН / ПО 500?!» (= hook text = first line).  python3 cover.py -> cover.png (+ covers/cover_s01e03.png)"""
import sys, pathlib, shutil; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
from covergen_maz import make
import ep03 as E

frame = E.maz_cu(1.0, 0.0, 'shock', bottle=True, hold=False, look=(0.4, 0.6), sz=17.0, head=(560, 1000), wind=0.5, mouth_=0.7, blink=False)
E.price_tag(frame, 1.0, 600, 1360, 1.5)
out = pathlib.Path(__file__).with_name('cover.png')
make(frame, ['БЕНЗИН', 'ПО 500?!'], n=3, out=str(out), title_y=150, title_size=80)
shutil.copy(out, P.series(E.SLUG) / 'covers' / 'cover_s01e03.png')
print(out)
