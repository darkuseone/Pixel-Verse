"""Model sheet of the «Прохор. Таёжные лайфхаки» cast, drawn from the real sprites (props/taigacast.py) in the «Морозный лубок» manner:
silhouettes (vs the heroes of other series), moods, faces in close-up, palette.
  python3 series/prokhor/design/cast_sheet.py  ->  series/prokhor/design/cast_sheet.png"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as P
from props import taigapix as TX, taigacast as C
from props import mazpix as MX, mazcast as MC, fmpix as FX, fmcast as FC
from props.dibspix import blit

W, H = 2400, 1800
BG = (26, 36, 54)
SNOWC = (226, 236, 248)
big = np.zeros((H, W, 3), np.uint8); big[:] = BG
for y in range(H):                                          # night sky → dusk band, very quiet
    k = y / H
    big[y] = (np.array(BG) * (1 - 0.35 * k) + np.array((60, 70, 104)) * 0.35 * k).astype(np.uint8)


def put(draw, fn, x, y, s, flip=False, sil=None, post=None, **kw):
    sp = draw(fn, s, flip=flip, **kw)
    if post: post(sp)
    if sil is not None: sp.col[sp.m] = sil
    blit(big, sp, x, y, s, None, flip)
    return sp


def put_head(fn, x, y, s, **kw):
    sp = TX.draw(fn, s, **kw)
    hx, hy = sp.anchors['head']
    blit(big, sp, x - hx * s, y + hy * s, s, None, False)


def snowline(y, x0, x1):
    big[y:y + 10, x0:x1] = SNOWC
    big[y + 10:y + 14, x0:x1] = (170, 196, 230)


im = Image.fromarray(big); d = ImageDraw.Draw(im)
f_t = ImageFont.truetype(P.FONT_PX, 48)
f_s = ImageFont.truetype(str(P.ROOT / 'engine/fonts/JetBrainsMono-Regular.ttf'), 22)
d.text((80, 48), 'МОРОЗНЫЙ ЛУБОК v2', font=f_t, fill=(236, 244, 255))
d.text((84, 124), 'ПРОХОР · МИХАЛ ПОТАПЫЧ — модельный лист · свет: низкое солнце слева + отражённый снег снизу', font=f_s, fill=(150, 170, 200))
big[:] = np.array(im)

# ---------------------------------------------------------------- row 1: silhouettes vs other series
snowline(560, 80, 1240)
put(TX.draw, C.prokhor, 230, 560, 5.0, sil=TX.INK, t=0.3)
put(TX.draw, C.potapych, 560, 560, 4.0, sil=TX.INK, t=0.3)
put(MX.draw, MC.maz, 880, 560, 2.7, sil=(70, 80, 100), t=0.3)
put(FX.draw, FC.fm, 1110, 560, 4.0, sil=(70, 80, 100), t=0.3)

# ---------------------------------------------------------------- row 1 right: palette
im = Image.fromarray(big); d = ImageDraw.Draw(im)
pal = [('ОВЧИНА', C.HAT), ('БОРОДА', C.BEARD), ('НОС', C.NOSE), ('ТЕЛОГРЕЙКА', C.JACKET), ('ИЗОЛЕНТА', C.TAPE), ('ВАЛЕНОК', C.FELT),
       ('КАЛОША', C.GALOSH), ('ПОТАПЫЧ', C.FUR), ('МОРДА', C.FUR_L), ('КОЛПАК', C.CAP_A), ('СНЕГ', TX.SNOW), ('ТУШЬ', TX.INK)]
for i, (n, c) in enumerate(pal):
    x, y = 1360 + (i % 4) * 250, 220 + (i // 4) * 110
    for j, cc in enumerate(TX.tones(c)):
        d.rectangle([x + j * 56, y, x + j * 56 + 50, y + 50], fill=cc)
    d.text((x, y + 58), n, font=f_s, fill=(170, 186, 210))
d.text((1360, 560), 'три плоских тона, жёсткий край, без дизеринга', font=f_s, fill=(120, 140, 170))
big[:] = np.array(im)

# ---------------------------------------------------------------- row 2: moods, full figures
snowline(1120, 80, W - 80)
put(TX.draw, C.tripod, 90, 1120, 5.2, t=0.0)
put(TX.draw, C.prokhor, 230, 1120, 5.2, t=0.3, expr='grin', hand_n=(22, 46))
put(TX.draw, C.prokhor, 470, 1120, 5.2, t=0.3, expr='shout', mouth_=0.8, hand_n=(17, 40), prop_n=lambda sp, h: C.bill(sp, h))
put(TX.draw, C.prokhor, 740, 1120, 5.2, t=0.3, expr='chatter', chatter=1.0, post=lambda sp: C.ice_over(sp, 1.0))
put(TX.draw, C.potapych, 1150, 1120, 4.6, t=0.3, expr='asleep', bubble=0.9)
put(TX.draw, C.potapych, 1600, 1120, 4.6, t=0.3, eyes='one')
put(TX.draw, C.potapych, 2060, 1120, 4.6, t=0.3, expr='boss', prop_n=C.terminal)

# ---------------------------------------------------------------- row 3: faces in close-up (hi-res rig)
for i, (kw) in enumerate([dict(expr='shout', mouth_=0.9), dict(expr='smug'), dict(expr='plead', mouth_=0.3)]):
    put_head(C.prokhor, 230 + i * 380, 1420, 12.0, t=0.3, **kw)
put_head(C.potapych, 1500, 1500, 9.0, t=0.3, expr='boss')
put_head(C.potapych, 2000, 1500, 9.0, t=0.3, expr='yawn', mouth_=1.0)
big[1700:] = (np.array(big[1700:], np.float32) * 0.0 + np.array(BG)).astype(np.uint8)
im = Image.fromarray(big); d = ImageDraw.Draw(im)
d.text((80, 1730), 'силуэт «сугроб с бородой» (пирамида) против «груши меха»; рядом — Мазутыч и Florida Man для сверки', font=f_s, fill=(120, 140, 170))
out = pathlib.Path(__file__).with_name('cast_sheet.png')
im.save(out); print(out)
