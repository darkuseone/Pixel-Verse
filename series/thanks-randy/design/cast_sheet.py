"""Model sheet of the «Thanks, Randy» cast, drawn from the real sprites (props/randycast.py) in the «Fridge-Light Sitcom» manner:
silhouettes (vs heroes of other series), the cast in the store, faces in close-up, palette.
  python3 series/thanks-randy/design/cast_sheet.py  ->  series/thanks-randy/design/cast_sheet.png"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as P
from props import randypix as RX, randycast as C, randykit as K
from props import fmpix as FX, fmcast as FC
from props.dibspix import blit

W, H = 2400, 1800
big = np.zeros((H, W, 3), np.uint8); big[:] = (34, 26, 40)


def put(draw, fn, x, y, s, sil=None, flip=False, **kw):
    sp = draw(fn, s, flip=flip, **kw)
    if sil is not None: sp.col[sp.m] = sil
    blit(big, sp, x, y, s, None, flip)
    return sp


def put_head(fn, x, y, s, **kw):
    sp = RX.draw(fn, s, **kw)
    hx, hy = sp.anchors['head']
    box = np.zeros((500, 500, 3), np.uint8); box[:] = (58, 46, 64)
    blit(box, sp, 250 - hx * s, 250 + hy * s, s, None, False)
    big[y - 250:y + 250, x - 250:x + 250] = box


# row 1 left: silhouettes (ours vs Florida Man)
big[560:572, 60:1240] = (90, 70, 96)
put(RX.draw, C.randy, 200, 560, 5.0, sil=RX.INK, t=1)
put(RX.draw, C.tom, 400, 560, 5.0, sil=RX.INK, t=1)
put(RX.draw, C.joyce, 560, 560, 5.0, sil=RX.INK, t=1)
put(RX.draw, C.brayden, 720, 560, 5.0, sil=RX.INK, t=1, stick=False)
put(FX.draw, FC.fm, 1060, 560, 4.0, sil=(80, 76, 92), t=0.3)
# row 2: the cast in the store
v_bg = np.array(Image.open(P.series('thanks-randy') / 'bg' / 'store.png').convert('RGB').resize((1280, 720)))
big[620:1340, 60:1340] = v_bg
put(RX.draw, C.kiosk, 1040, 1320, 7.0, t=1, screen='alarm', lamp='red', part='back')
put(RX.draw, C.joyce, 1040 + 28.5 * 7, 1320 - 33 * 7, 7.0, t=1, sit=True, knit=1.0, expr='sweet')
put(RX.draw, C.randy, 760, 1320, 7.0, t=1, expr='shout', mouth_=0.8, stache='up', hand_n=(17.0, 66.0))
put(RX.draw, C.brayden, 300, 1320, 7.0, t=1, expr='lazy')
put(RX.draw, C.tom, 540, 1320, 7.0, t=1, expr='dead')
# right column: faces in close-up
for i, (fn, kw) in enumerate([(C.randy, dict(expr='losing', mouth_=0.6, tremble=0.0)), (C.tom, dict(expr='dead', mouth_=0.5)),
                              (C.joyce, dict(expr='nosy')), (C.brayden, dict(expr='lazy', stick=False))]):
    x, y = 1620 + (i % 2) * 520, 380 + (i // 2) * 560
    put_head(fn, x, y, 22.0 if fn is not C.tom else 18.0, t=1, **kw)
im = Image.fromarray(big); d = ImageDraw.Draw(im)
f_t = ImageFont.truetype(P.FONT_PX, 44); f_s = ImageFont.truetype(str(P.ROOT / 'engine/fonts/JetBrainsMono-Regular.ttf'), 22)
d.text((70, 48), 'FRIDGE-LIGHT SITCOM', font=f_t, fill=(255, 186, 60))
d.text((74, 112), 'THANKS, RANDY - cast sheet: warm lamp above + cold freezer below, frost-crystal shadows, plum ink', font=f_s, fill=(200, 180, 210))
d.text((74, 150), 'silhouettes: brick on a pear / boulder with legs / dandelion on a match / noodle   vs   Florida Man (olive on toothpicks)', font=f_s, fill=(160, 150, 170))
pal = [('POLO', C.POLO), ('APRON', C.APRON), ('KHAKI', C.KHAKI), ('FLAT-TOP', C.HAIR), ('TOM', C.TURK), ('NET', C.NET), ('LABEL', C.LABEL),
       ('PERM', C.PERM), ('CARDIGAN', C.CARD), ('SKIRT', C.SKIRT), ('VEST', C.VEST), ('INK', RX.INK)]
for i, (n, c) in enumerate(pal):
    x, y = 70 + (i % 6) * 210, 1420 + (i // 6) * 150
    d.rectangle([x, y, x + 90, y + 90], fill=c, outline=(250, 240, 230), width=3)
    d.text((x, y + 100), n, font=f_s, fill=(220, 210, 230))
im.save(pathlib.Path(__file__).parent / 'cast_sheet.png'); print('cast_sheet.png')
