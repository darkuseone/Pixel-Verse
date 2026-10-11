"""YouTube cover 1920x1080 for «FLORIDA MAN ON TRIAL»: Florida Man in the county jumpsuit shrieking at the defense table, Judge Tanner with
the gavel, Mort; title «GUILTY OF FLORIDA?!» + (ALLEGEDLY).   python3 cover.py -> cover.png + cover.jpg (<= 2 MB)"""
import movie as M
from movie import *

t = 0.5
v0 = view_at(COURT, 640, 360, 1.25, SX, SY)
def at(px, py): return K.wpt(v0, px, py)
acts = [A(C.tanner, *at(1500, 560), 19.0, flip=True, pin='head', t=t, uniform='judge', jobs=8, gavel=True, expr='angry', hand_n=(12.0, 64.0),
          look=(-0.6, 0.0)),
        A(C.fm, *at(470, 600), 22.0, pin='head', t=t, jumpsuit=True, expr='shriek', mouth_=0.95, sweat=1.0, glasses_drop=1.0, look=(0.4, 0.2)),
        A(C.mort, *at(1000, 760), 15.0, pin='head', t=t, expr='smug', look=(-0.3, 0.0), cam=True)]
def pre(big, v): big[:] = K.dof(big, 7)
big = K.shot(COURT, light_court, 640, 360, 1.25, acts=acts, pre=pre, sx=SX, sy=SY)
shade = np.linspace(0.55, 0.0, 380)[:, None, None]
big[:380] = (big[:380] * (1 - shade)).astype(np.uint8)
ti = K.hook_title(['GUILTY OF FLORIDA?!'], 86, width=OUT_W, depth=16)
O.overlay(big, ti, 0, 30, 1.0)
st = K.allegedly_stamp(60)
O.overlay(big, st, 1150, 190, 1.0)
from PIL import Image
im = Image.fromarray(big)
im.save(HERE / 'cover.png')
q = 92
while True:
    im.save(HERE / 'cover.jpg', quality=q)
    if (HERE / 'cover.jpg').stat().st_size <= 2_000_000 or q < 60: break
    q -= 4
print(HERE / 'cover.jpg', (HERE / 'cover.jpg').stat().st_size)
