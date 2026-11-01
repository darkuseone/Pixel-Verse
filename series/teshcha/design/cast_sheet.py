"""Model sheet of the cast, drawn by the real rig (engine/props/teshcast.py) -> design/cast_sheet.png
  python3 series/teshcha/design/cast_sheet.py"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[3] / 'engine'))
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import View, Chars
from props import teshcast as T
from props import folk as F
import overlays as O

HEADPX = dict(tolik=(560, 520), raisa=(620, 560), pusya=(540, 1560), sveta=(560, 560))
CAM = [None]
OUT = pathlib.Path(__file__).resolve().parent / 'cast_sheet.png'


def panel(draw, Z=1.0, bg=(250, 236, 214)):
    world = np.zeros((2000, 2000, 3), np.uint8); world[:] = bg
    v = View(world, 0, 0, Z)
    ST.set_px(1)
    CH = Chars(); big = v.bg()
    draw(CH, v)
    CH.comp(big)
    return big


def row():
    def d(CH, v):
        T.tolik(CH, v.cam(60, 600, 17.5), t=0.3, expr='scream', mouth_=0.0, pose=T.TPOSE['shock'])
        T.raisa(CH, v.cam(170, 600, 17.5), t=0.3, expr='sweet', pose=T.RPOSE['hold'])
        T.pusya(CH, v.cam(196, 402, 4.6), t=0.3, expr='deadpan')
        T.sveta(CH, v.cam(290, 600, 17.5), t=0.3, expr='guilty', pose=T.SPOSE['keys'], prop_n=T.keys)
    return panel(d)


def faces():
    out = []
    for name, fn in [('tolik', lambda CH, v, e: (CAM.__setitem__(0, v.cam(140, 1290, 40)), T.tolik(CH, CAM[0], expr=e, t=0.4))[1]),
                     ('raisa', lambda CH, v, e: (CAM.__setitem__(0, v.cam(140, 1080, 40)), T.raisa(CH, CAM[0], expr=e, t=0.4))[1]),
                     ('pusya', lambda CH, v, e: (CAM.__setitem__(0, v.cam(180, 480, 50)), T.pusya(CH, CAM[0], expr=e, t=0.4, mouth_=0.6 if e == 'shock' else 0))[1]),
                     ('sveta', lambda CH, v, e: (CAM.__setitem__(0, v.cam(140, 1185, 44)), T.sveta(CH, CAM[0], expr=e, t=0.4))[1])]:
        exprs = {'tolik': ['scream', 'proud', 'smug', 'whine'], 'raisa': ['sweet', 'stern', 'shout', 'smug'],
                 'pusya': ['deadpan', 'shock', 'smug', 'sleepy'], 'sveta': ['guilty', 'tired', 'smile', 'shock']}[name]
        for e in exprs:
            box = {}
            img = panel(lambda CH, v: box.update(r=fn(CH, v, e), v=v))
            cm = box['v']
            hx, hy = box['r']['head']
            import stage
            # head is in unit coords of the character cam: map via a fresh cam of the same params
            hp = CAM[0].p(*box['r']['head']); cx, cy = int(hp[0] * 3), int(hp[1] * 3)
            out.append(Image.fromarray(img).crop((cx - 300, cy - 300, cx + 300, cy + 300)).resize((270, 270), Image.NEAREST))
    return out


if __name__ == '__main__':
    a = Image.fromarray(row()).resize((540, 960), Image.NEAREST)
    fs = faces()
    sheet = Image.new('RGB', (540 + 270 * 4, 1080), (40, 22, 28))
    sheet.paste(a, (0, 60))
    for i, f in enumerate(fs):
        sheet.paste(f, (540 + (i % 4) * 270, (i // 4) * 270))
    sheet.save(OUT); print(OUT)
