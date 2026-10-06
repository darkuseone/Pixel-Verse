"""Model sheet of the «Мазутыч» cast, drawn from the real sprites (props/mazcast.py): silhouettes, turnaround of moods, props.
  python3 series/mazutych/design/cast_sheet.py   ->  series/mazutych/design/cast_sheet.png"""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import paths as P
from props import mazpix as MX, mazcast as MC
from props.dibspix import blit

W, H = 2400, 1800
BG = (38, 28, 44)
PAPER = (232, 222, 200)
INK = MX.INK
ORANGE = (238, 112, 30)
big = np.zeros((H, W, 3), np.uint8); big[:] = BG


def put(fn, x, y, s, flip=False, sil=None, **kw):
    sp = MX.draw(fn, s, flip=flip, **kw)
    if sil is not None:
        sp.col[sp.m] = sil
    blit(big, sp, x, y, s, None, flip)


# oil-slick bands (the title fill) as the only decoration: thin horizontal stripes under the headings
def slick(y, x0=80, x1=W - 80, h=6):
    cols = [(150, 60, 170), (60, 170, 190), (230, 190, 70)]
    seg = (x1 - x0) / 3
    for i, c in enumerate(cols):
        big[y:y + h, int(x0 + i * seg):int(x0 + (i + 1) * seg)] = c


# ---------------------------------------------------------------- row 1: silhouettes | full figures
slick(250)
for k, (fn, kw, s) in enumerate([(MC.maz, dict(t=0.3), 6.2), (MC.zoya, dict(t=0.3, mega=True), 7.0), (MC.monowheel_solo, dict(), 10.0)]):
    put(fn, 260 + k * 260, 1020, s * 0.62, sil=INK, **kw)
put(MC.maz, 1080, 1020, 5.2, t=0.3, expr='deadpan', wind=0.4)
put(MC.maz, 1450, 1020, 5.2, t=0.5, expr='shock', mouth_=0.7, wind=1.0, blinker=1.0, steer=0.5, beacon=True)
put(MC.zoya, 2020, 1000, 5.6, t=0.3, mega=True, mouth_=0.6)

# ---------------------------------------------------------------- row 2: Мазутыч moods (heads) + wheel faces + truck
slick(1090)
for k, (ex, mo) in enumerate([('deadpan', 0.0), ('stunned', 0.0), ('shock', 0.8), ('sly', 0.0), ('sad', 0.0)]):
    sp = MX.draw(MC.maz, 5.6, t=0.2 + k, expr=ex, mouth_=mo, wind=0.3 if k == 2 else 0.0, blink=False)
    hx, hy = sp.anchors['head']
    blit(big, sp, 190 + k * 260 - hx * 5.6, 1385 + hy * 5.6, 5.6, None)
big[1545:, :1400] = BG
for k, f in enumerate(['smile', 'low', 'dead']):
    put(MC.monowheel_solo, 1640 + k * 200, 1690, 8.0, face=f)
put(MC.tanker, 1500, 1430, 4.2)
put(MC.lada, 2160, 1430, 4.6, col=(196, 60, 52))

# ---------------------------------------------------------------- type: sparse, clinical
img = Image.fromarray(big); d = ImageDraw.Draw(img); d.fontmode = '1'
fp = ImageFont.truetype(P.FONT_PX, 64); fs = ImageFont.truetype(P.FONT_PX, 18)
d.text((80, 90), 'МАЗУТЫЧ', font=fp, fill=PAPER)
d.text((80, 180), 'МАЗУТНАЯ ГРАВЮРА · МОДЕЛЬНЫЙ ЛИСТ · СЕЗОН 1', font=fs, fill=(170, 150, 140))
d.text((80, 285), 'СИЛУЭТЫ: КОЧЕРГА / ПИРАМИДА / ПОНЧИК', font=fs, fill=(170, 150, 140))
d.text((1000, 285), 'МАЗУТЫЧ · 52 · ОПЕРАТОР УСТАНОВКИ', font=fs, fill=ORANGE)
d.text((1900, 285), 'ЗОЯ · КАССА АЗС «ЛУК-ОЙ»', font=fs, fill=(255, 120, 200))
d.text((80, 1125), 'МИМИКА: ПАМЯТНИК · БЕНЗОВОЗ · ШОК · ХИТРО · ОДИН И ТОТ ЖЕ', font=fs, fill=(170, 150, 140))
d.text((1560, 1125), 'ДИН-ДОН 3000 · БЕНЗОВОЗ · «ШЕСТЁРКА»', font=fs, fill=(90, 230, 255))
d.text((80, H - 60), 'ТЕНЬ = ШТРИХ 45° · КОНТУР = МАЗУТ ×2 · СВЕТ СПРАВА, ОТ ФАКЕЛА', font=fs, fill=(120, 104, 100))
img.save(pathlib.Path(__file__).with_name('cast_sheet.png'))
print('ok')
