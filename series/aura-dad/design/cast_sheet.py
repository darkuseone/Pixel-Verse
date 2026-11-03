"""Model sheet of the cast, drawn by the real rig (engine/props/auracast.py) -> design/cast_sheet.png
  python3 series/aura-dad/design/cast_sheet.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import numpy as np
from PIL import Image
import stage as ST
from stage import View, Chars
from scene import Layer
from props import auracast as A

OUT = pathlib.Path(__file__).resolve().parent / 'cast_sheet.png'


def panel(draw, Z=1.0, bg=(236, 226, 248)):
    world = np.zeros((2000, 2000, 3), np.uint8); world[:] = bg
    v = View(world, 0, 0, Z)
    ST.set_px(1)
    CH = Chars(); big = v.bg()
    draw(CH, v)
    CH.comp(big)
    return big


def row():
    def d(CH, v):
        A.kayden(CH, v.cam(60, 600, 16.5), t=0.3, expr='bored', pose=A.KPOSE['phone'], prop_n=A.phone)
        A.doug(CH, v.cam(165, 600, 16.5), t=0.3, expr='shout', pose=A.DPOSE['shout'])
        A.tammy(CH, v.cam(275, 600, 16.5), t=0.3, expr='tired', pose=A.TPOSE['mug'], prop_n=A.mug)
        L = Layer(v.wcam()); A.mirra(L, 180, 120, 9, 0.5, talk=0.5); CH.add(L)
    return panel(d)


def faces():
    out = []
    spec = [('doug', ['shout', 'mew', 'proud', 'shock'], lambda CH, cam, e: A.doug(CH, cam, expr=e, t=0.4, shine=1.0 if e == 'proud' else 0)),
            ('kayden', ['bored', 'shock', 'smirk', 'flat'], lambda CH, cam, e: A.kayden(CH, cam, expr=e, t=0.4)),
            ('tammy', ['tired', 'bliss', 'roll', 'smirk'], lambda CH, cam, e: A.tammy(CH, cam, expr=e, t=0.4))]
    for name, exprs, fn in spec:
        for e in exprs:
            box = {}
            def d(CH, v):
                cam = v.cam(140, 1300, 40); box['cam'] = cam; box['r'] = fn(CH, cam, e)
            img = panel(d)
            hp = box['cam'].p(*box['r']['head']); cx, cy = int(hp[0] * 3), int(hp[1] * 3)
            out.append(Image.fromarray(img).crop((cx - 420, cy - 400, cx + 420, cy + 440)).resize((270, 270), Image.NEAREST))
    return out


if __name__ == '__main__':
    a = Image.fromarray(row()).resize((540, 960), Image.NEAREST)
    fs = faces()
    sheet = Image.new('RGB', (540 + 270 * 4, 960), (38, 20, 52))
    sheet.paste(a, (0, 0))
    for i, f in enumerate(fs):
        sheet.paste(f, (540 + 270 * (i % 4), 100 + 280 * (i // 4)))
    sheet.save(OUT); print(OUT)
