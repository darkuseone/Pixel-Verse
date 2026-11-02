"""16:9 cover for «ТЁЩА НА НЕДЕЛЬКУ: ЗАГОВОР» by the CTR rules (docs/covers.md): Tolik's huge terrified face in the colander helmet
(left, ~50 % of the height), Raisa smaller on the right, sweetly smiling with a cement sack; warm sunburst; one huge word «ЗАМУРУЮТ?!»
(complements the video title, does not spoil the twists); bottom-right timestamp corner empty. Code only.
  python3 cover.py  -> cover.png / cover.jpg / cover_small.png"""
import movie as MV
from movie import *
import thumb16 as TH

Wd, Hd = OUT_W, OUT_H
big = TH.sunburst(Wd, Hd, (560, 620), [(255, 206, 40), (255, 140, 30), (236, 70, 40)], rays=22, px=8, core_r=380, rot=0.1)
v = view_at(ROOM, 320, 180, 1.0, SX, SY)                      # any view: only its camera maths is used


def draw_tolik(CH):
    MV.tol(CH, v, 1.0, 165, 1006, 30.0, pose=dict(T.TPOSE['shock'], n=(5.6, 21.4), f=(-3.6, 21.0)), expr='scream', m=1.0,
           colander=1.0, look=0.5)


def draw_raisa(CH):
    L = Layer(v.wcam()); MV.sack(L, 505, 356, 1.2); CH.add(L)
    MV.rai(CH, v, 1.0, 425, 360, 11.0, flip=True, pose='hips', expr='sweet', look=-0.6)


hero = TH.sticker(TH.boost(TH.rgba(draw_tolik, K.begin)), 12, 20)
side = TH.sticker(TH.boost(TH.rgba(draw_raisa, K.begin)), 9, 15)
O.overlay(big, side, 0, 0, 1.0)
O.overlay(big, hero, 0, 0, 1.0)
plate = TH.rot(TH.pixel_text('ЦЕМЕНТ', 34, (20, 16, 14), bg=(230, 230, 222), border=(20, 16, 14), pad=8), -4)
O.overlay(big, plate, 1440, 900, 1.0)
from endcard import _trim
title = _trim(K.hook_title(['ЗАМУРУЮТ?!'], 132, width=1500))
O.overlay(big, title, Wd - title.shape[1] - 30, 24, 1.0)
tag = TH.pixel_text('ТЁЩА НА НЕДЕЛЬКУ • ФИЛЬМ', 30, (255, 236, 160), bg=(20, 16, 14), pad=8, bw=0)
O.overlay(big, tag, 40, Hd - tag.shape[0] - 36, 1.0)
fx.vignette(big, 0.16)
TH.save(big, HERE, 'cover')
