"""Model sheet of the «Кощей из панельки» cast, drawn from the real sprites (props/koshcast.py) in the «Хохлома-нуар» manner:
silhouettes (vs the heroes of other series), palette, moods, faces in close-up.
  python3 series/koshchei/design/cast_sheet.py  ->  series/koshchei/design/cast_sheet.png"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as P
from props import koshpix as KX, koshcast as C
from props import taigapix as TX, taigacast as TC, mazpix as MX, mazcast as MC, grimpix as GX, grimcast as GC
from props.dibspix import blit

W, H = 2400, 1800
BG = (24, 16, 14)                                           # black lacquer
big = np.zeros((H, W, 3), np.uint8); big[:] = BG
yy, xx = np.mgrid[0:H, 0:W]
glow = np.clip(1 - ((xx - W * 0.5) / (W * 0.7)) ** 2 - ((yy - H * 0.1) / (H * 0.9)) ** 2, 0, 1)    # one bare bulb, top centre
big[:] = np.clip(np.array(BG) + glow[..., None] * np.array((30, 22, 10)), 0, 255).astype(np.uint8)


def put(draw, fn, x, y, s, sil=None, **kw):
    sp = draw(fn, s, **kw)
    if sil is not None: sp.col[sp.m] = sil
    blit(big, sp, x, y, s)
    return sp


def put_head(fn, x, y, s, **kw):
    sp = KX.draw(fn, s, **kw)
    hx, hy = sp.anchors['head']
    blit(big, sp, x - hx * s, y + hy * s, s)


def floor(y, x0, x1):                                       # gold Хохлома rule with a cinnabar underline
    big[y:y + 4, x0:x1] = KX.GOLD
    big[y + 4:y + 8, x0:x1] = KX.CINNABAR


im = Image.fromarray(big); d = ImageDraw.Draw(im)
f_t = ImageFont.truetype(P.FONT_PX, 48)
f_s = ImageFont.truetype(str(P.ROOT / 'engine/fonts/JetBrainsMono-Regular.ttf'), 22)
d.text((80, 48), 'ХОХЛОМА-НУАР', font=f_t, fill=KX.GOLD_L)
d.text((84, 124), 'КОЩЕЙ · ЯГА · КУЗЬМИЧ — модельный лист · свет: лампочка 40 Вт сверху-справа + зелёный «кощеев огонь» снизу',
       font=f_s, fill=(200, 170, 120))
big[:] = np.array(im)

# ---------------------------------------------------------------- row 1: silhouettes vs other series
floor(600, 80, 1300)
put(KX.draw, C.koshchei, 190, 600, 5.0, sil=KX.INK, t=0.5)
put(KX.draw, C.yaga, 400, 600, 5.0, sil=KX.INK, t=0.5)
put(KX.draw, C.domovoy, 560, 600, 5.0, sil=KX.INK, t=0.5)
grey = (74, 62, 58)
put(TX.draw, TC.prokhor, 760, 600, 4.4, sil=grey, t=0.3)
put(MX.draw, MC.maz, 990, 600, 2.4, sil=grey, t=0.3)
put(GX.draw, GC.grim, 1190, 600, 2.4, sil=grey, t=0.3)

# ---------------------------------------------------------------- row 1 right: palette
im = Image.fromarray(big); d = ImageDraw.Draw(im)
pal = [('КОЖА', C.K_SKIN), ('МАЙКА', C.K_VEST), ('ТРИКО', C.K_TRICO), ('ГЛАЗА', C.K_IRIS), ('ПЛАТОК', C.Y_SHAWL), ('КИНОВАРЬ', KX.CINNABAR),
       ('КОФТА', C.Y_CARD), ('КОСТЬ', C.BONE), ('БОРОДА', C.D_BEARD), ('РУБАХА', C.D_SHIRT), ('ЗОЛОТО', KX.GOLD), ('ЛАК', KX.INK)]
for i, (n, c) in enumerate(pal):
    x, y = 1400 + (i % 4) * 240, 220 + (i // 4) * 110
    for j, cc in enumerate(KX.tones(c)):
        d.rectangle([x + j * 56, y, x + j * 56 + 50, y + 50], fill=cc)
    d.text((x, y + 58), n, font=f_s, fill=(200, 170, 120))
d.text((1400, 560), 'три плоских тона, тень уходит в чёрный лак', font=f_s, fill=(150, 120, 90))
d.text((84, 620), 'силуэты: «вешалка» · «чайник в платке» · «шар бороды»   |   серым: Прохор, Мазутыч, Grim (сверка)', font=f_s, fill=(150, 120, 90))
big[:] = np.array(im)

# ---------------------------------------------------------------- row 2: moods, full figures
floor(1150, 80, W - 80)
put(KX.draw, C.koshchei, 180, 1150, 6.0, t=0.5, expr='scream', mouth_=1.0, hand_n=(14, 44))
put(KX.draw, C.koshchei, 420, 1150, 6.0, t=0.5, expr='proud', hand_n=(10, 54), fire=1.0)
put(KX.draw, C.koshchei, 660, 1150, 6.0, t=0.5, expr='sad', prop_n=C.pension_slip, hand_n=(12, 34))
put(KX.draw, C.koshchei, 900, 1150, 6.0, t=0.5, expr='sinister', prop_n=C.needle_egg, hand_n=(12, 38))
put(KX.draw, C.yaga, 1150, 1150, 7.0, t=0.5, expr='gossip')
put(KX.draw, C.yaga, 1420, 1150, 7.0, t=0.5, expr='angry', mouth_=0.6)
put(KX.draw, C.domovoy, 1700, 1150, 9.0, t=0.5, expr='zhut')
put(KX.draw, C.domovoy, 1950, 1150, 9.0, t=0.5, expr='deadpan', mouth_=0.6, glow=1.0)
put(KX.draw, C.domovoy, 2200, 1150, 9.0, t=0.5, expr='shock')

# ---------------------------------------------------------------- row 3: faces in close-up (hi-res rig)
put_head(C.koshchei, 260, 1500, 13.0, t=0.5, expr='scream', mouth_=1.0, fire=0.6)
put_head(C.koshchei, 700, 1500, 13.0, t=0.5, expr='sinister')
put_head(C.yaga, 1200, 1520, 15.0, t=0.5, expr='sly')
put_head(C.domovoy, 1720, 1560, 16.0, t=0.5, expr='zhut')
put_head(C.domovoy, 2120, 1560, 16.0, t=0.5, expr='shock')
big[1730:] = BG
im = Image.fromarray(big); d = ImageDraw.Draw(im)
d.text((80, 1748), 'смешная деталь: корона из фольги, пузыри трико на коленях · бигуди под платком, костяная нога в галоше · пломба на шее',
       font=f_s, fill=(150, 120, 90))
out = pathlib.Path(__file__).with_name('cast_sheet.png')
im.save(out); print(out)
