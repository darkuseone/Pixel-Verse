"""Model sheet of «Батя сам», drawn by the real rig (engine/props/batyacast.py) -> design/cast_sheet.png
  python3 series/batya/design/cast_sheet.py
Panels: the three heroes full height (warm room light), their silhouettes (readability test), 3 x 4 expressions, palette swatches."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import View, Chars
from props import batyacast as B
import overlays as O

OUT = pathlib.Path(__file__).resolve().parent / 'cast_sheet.png'
CREAM, INK = (246, 236, 214), (52, 20, 30)


def panel(draw, Z=1.0, bg=CREAM, size=2000):
    world = np.zeros((size, size, 3), np.uint8); world[:] = bg
    v = View(world, 0, 0, Z)
    ST.set_px(1)
    CH = Chars(); big = v.bg()
    box = {}
    draw(CH, v, box)
    CH.comp(big)
    return big, box


def cast_row():
    def d(CH, v, box):
        B.batya(CH, v.cam(78, 610, 16.0), B.BPOSE['fists'], t=0.3, expr='fists')
        B.tema(CH, v.cam(190, 610, 16.0), B.TPOSE['film'], t=0.3, expr='deadpan')
        B.ira(CH, v.cam(292, 610, 16.0), B.IPOSE['hips'], t=0.3, expr='dry', specs=True)
    big, _ = panel(d)
    return big


def silhouettes(img):
    m = (np.abs(img.astype(int) - np.array(CREAM)).sum(-1) > 30)
    out = np.zeros_like(img); out[:] = CREAM; out[m] = INK
    return out


FACES = [('batya', ['dying', 'fists', 'shock', 'happy']), ('tema', ['deadpan', 'smug', 'shock', 'happy']),
         ('ira', ['dry', 'sick', 'shock', 'happy'])]


def face(who, e):
    def d(CH, v, box):
        if who == 'batya':
            cam = v.cam(140, 300 + 23.7 * 40, 40); r = B.batya(CH, cam, B.BPOSE['stand'], t=0.4, expr=e, sick=1.0 if e == 'dying' else 0.0,
                                                    towel=(e == 'dying'), mouth_=0.6 if e == 'fists' else 0.0)
        elif who == 'tema':
            cam = v.cam(140, 300 + 27.4 * 40, 40); r = B.tema(CH, cam, B.TPOSE['stand'], t=0.4, expr=e, prop_n=None)
        else:
            cam = v.cam(140, 300 + 21.5 * 44, 44); r = B.ira(CH, cam, B.IPOSE['stand'], t=0.4, expr=e, sick=1.0 if e == 'sick' else 0.0,
                                                 scarf=(e == 'sick'), specs=(e == 'dry'))
        box['p'] = cam.p(*r['head'])
    big, box = panel(d)
    cx, cy = int(box['p'][0] * ST.UP), int(box['p'][1] * ST.UP)
    return Image.fromarray(big).crop((cx - 330, cy - 340, cx + 330, cy + 320)).resize((264, 264), Image.NEAREST)


SW = [('БАТЯ', [B.BC['sw'], B.BC['knit'], B.BC['vest'], B.BC['tape'], B.BC['pants'], B.BC['hair']]),
      ('ТЁМА', [B.TC['hood'], B.TC['hair'], B.TC['pants'], B.TC['shoe'], B.TC['cans']]),
      ('МАМА ИРА', [B.IC['hair'], B.IC['card'], B.IC['blouse'], B.IC['lip'], B.IC['slip']])]


if __name__ == '__main__':
    row = cast_row()
    a = Image.fromarray(row).crop((0, 0, 1080, 1920)).resize((540, 960), Image.NEAREST)
    s = Image.fromarray(silhouettes(np.array(a)))
    W_, H_ = 540 * 2 + 264 * 4 + 60, 1100
    sheet = Image.new('RGB', (W_, H_), CREAM)
    sheet.paste(a, (20, 70)); sheet.paste(s, (560, 70))
    for i, (who, es) in enumerate(FACES):
        for j, e in enumerate(es):
            sheet.paste(face(who, e), (1120 + j * 264, 70 + i * 264))
    d = ImageDraw.Draw(sheet)
    f = O.pfont(22); fs = O.pfont(14)
    d.text((20, 22), 'БАТЯ САМ — КАСТ', font=f, fill=INK)
    d.text((560, 30), 'СИЛУЭТ: КВАДРАТ / ПАЛКА / БОЧОНОК', font=fs, fill=INK)
    d.text((1120, 30), 'ЭМОЦИИ', font=fs, fill=INK)
    y = 70 + 3 * 264 + 24
    for k, (name, cols) in enumerate(SW):
        x0 = 1120 + k * 352
        d.text((x0, y), name, font=fs, fill=INK)
        for i, c in enumerate(cols):
            d.rectangle([x0 + i * 52, y + 28, x0 + i * 52 + 44, y + 72], fill=tuple(c), outline=INK, width=3)
    sheet.save(OUT); print(OUT)
