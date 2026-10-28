"""CTR cover v2 (28.10.2026, YouTube CTR of v1 = 0.86-0.97 %: muted brown refinery, a neutral «О»-mouth, text «ЭТО Я?!» that does not
explain itself and spoils the twist). Now: Мазутыч's huge panicking face left, an empty fuel pump right showing «0,00», one last drop
from the nozzle, «БЕНЗИНА НЕТ» plate, warm red-orange-yellow sunburst; title «КТО СЛИЛ?!» complements the video title
«Куда пропал бензин?». Bottom-right timestamp corner empty.
  python3 cover_ctr.py      -> cover_ctr.png/.jpg/_small.png (code only)
  python3 cover_ctr.py xai  -> the same scene as a reference -> xAI edit x2 -> pixelized -> same title: cover_xai1/2.* ('new' = regenerate)"""
import sys, math
import movie as MV
from movie import *
import thumb16 as T

Wd, Hd = OUT_W, OUT_H
big = T.sunburst(Wd, Hd, (1150, 560), [(255, 206, 40), (255, 140, 30), (236, 70, 40)], rays=22, px=8, core_r=420, rot=0.12)


def sprite_rgba(fn, s, size, head, flip=False, **kw):
    key = (255, 0, 255)
    a = MV.portrait(fn, s, size, bg=key, head=head, flip=flip, **kw)
    m = ~((a[..., 0] == 255) & (a[..., 1] == 0) & (a[..., 2] == 255))
    out = np.zeros(a.shape[:2] + (4,), np.uint8)
    out[m, :3] = a[m]; out[m, 3] = 255
    return out


# the empty pump (right), drawn in chunky pixels
im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
px0, py0, px1, py1 = 1230, 380, 1640, 1080
d.rectangle([px0 - 14, py0 - 14, px1 + 14, py1 + 20], fill=INK)
d.rectangle([px0, py0, px1, py1], fill=(214, 40, 40))
d.rectangle([px0, py0, px1, py0 + 60], fill=(250, 240, 230))
d.text(((px0 + px1) / 2, py0 + 31), 'АИ-95', font=O.pfont(44), fill=(214, 40, 40), anchor='mm')
d.rectangle([px0 + 34, py0 + 92, px1 - 34, py0 + 300], fill=INK)                            # the display
d.rectangle([px0 + 48, py0 + 106, px1 - 48, py0 + 286], fill=(40, 34, 20))
d.text(((px0 + px1) / 2, py0 + 196), '0,00', font=O.pfont(92), fill=(255, 214, 60), anchor='mm')
d.text((px1 - 62, py0 + 270), 'Л', font=O.pfont(34), fill=(255, 214, 60), anchor='rm')
for k in range(3):                                                                         # stripes
    d.rectangle([px0, py0 + 360 + k * 46, px1, py0 + 380 + k * 46], fill=(255, 214, 60) if k % 2 == 0 else (250, 240, 230))
big = np.array(im)
# «БЕНЗИНА НЕТ» plate hanging crooked off the pump top
plate = T.rot(T.pixel_text('БЕНЗИНА НЕТ', 36, (20, 16, 14), bg=(255, 236, 120), border=(20, 16, 14), pad=10), -5)
O.overlay(big, plate, (px0 + px1) // 2 - plate.shape[1] // 2, py0 + 340, 1.0)
# hose from the pump down to the nozzle in his hand zone, the last drop
hose_a = (px0 - 6, py0 + 560)
nx, ny = 900, 600                                                   # the nozzle points at his eye: he looks into it
M.rope(big, hose_a, (nx + 150, ny + 60), sag=220, w=28, col=(30, 30, 34))
im = Image.fromarray(big); d = ImageDraw.Draw(im)
d.polygon([(nx + 60, ny - 34), (nx + 190, ny - 34), (nx + 190, ny + 30), (nx + 150, ny + 120), (nx + 110, ny + 120), (nx + 120, ny + 30),
           (nx + 60, ny + 30)], fill=(52, 54, 62), outline=INK, width=8)                     # body + grip
d.rectangle([nx - 110, ny - 14, nx + 64, ny + 14], fill=(160, 160, 168), outline=INK, width=6)   # spout pointing left
d.arc([nx + 100, ny + 10, nx + 170, ny + 80], 0, 180, fill=INK, width=8)                         # trigger guard
big = np.array(im)
MV.drop(big, nx - 98, ny + 64, 26)
# Мазутыч: a huge panicking face, left, looking at the pump
hero = sprite_rgba(MC.maz, 15.5, (1100, 1300), head=(0.42, 0.36), expr='panic', look=(0.9, 0.2), beacon=True, ride=False, mouth_=1.0,
                   t=1.0, sweat=1.0)
O.overlay(big, T.sticker(T.boost(hero), 12, 20), -50, -40, 1.0)

def pump_text(a):
    """xAI leaves the pump blank (as asked): re-letter the display, the header strip and the plate in code.
    Display box measured on both raws (28.10.2026): x 1290-1630, y 470-680; white header y 380-440."""
    x0, y0, x1, y1 = 1296, 476, 1624, 674
    im = Image.fromarray(a); d = ImageDraw.Draw(im); d.fontmode = '1'
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    fs = 120
    while O.pfont(fs).getlength('0,00') > (x1 - x0) * 0.82: fs -= 6
    d.text((cx, cy - 6), '0,00', font=O.pfont(fs), fill=(255, 214, 60), anchor='mm')
    d.text((x1 - 22, y1 - 22), 'Л', font=O.pfont(34), fill=(255, 214, 60), anchor='rb')
    hy = 410
    d.text((cx, hy), 'АИ-95', font=O.pfont(44), fill=(214, 40, 40), anchor='mm')
    a[:] = np.array(im)
    pl = T.rot(T.pixel_text('БЕНЗИНА НЕТ', 36, (20, 16, 14), bg=(255, 236, 120), border=(20, 16, 14), pad=10), -5)
    O.overlay(a, pl, int(cx - pl.shape[1] / 2), y1 + 70, 1.0)


def add_text(big):
    from endcard import _trim
    title = _trim(K.hook_title(['КТО СЛИЛ?!'], 122, width=1500))
    O.overlay(big, title, Wd - title.shape[1] - 24, 14, 1.0)
    tag = T.pixel_text('МАЗУТЫЧ • ФИЛЬМ', 30, (255, 236, 160), bg=(20, 16, 14), pad=8, bw=0)
    O.overlay(big, tag, 40, Hd - tag.shape[0] - 36, 1.0)
    fx.vignette(big, 0.18)
    return big


if 'xai' in sys.argv:
    for i, a in enumerate(T.ai_versions(big, MV.HERE, fresh='new' in sys.argv, emotion=
                                        "the mustached oil worker in the white hard hat is PANICKING, screaming with a huge wide-open "
                                        "mouth and bulging eyes, sweat drops flying, staring into the empty fuel nozzle with one last "
                                        "golden drop; the red fuel pump on the right has a blank black display and a blank yellow plate.")):
        pump_text(a)
        T.save(add_text(a), MV.HERE, f'cover_xai{i + 1}')
else:
    T.save(add_text(big), MV.HERE, 'cover_ctr')
