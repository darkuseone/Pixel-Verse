"""CTR cover 1920x1080 for «VINCE VELOUR'S GUIDE TO 1986» (docs/covers.md §«Обложка длинного видео 16:9»): one dominant screaming face
(Vince, shades off, ~45 % of the frame height, left) holding up a receipt that rolls down to the floor, a small deadpan neon Fran,
a bright pink/orange pixel sunburst instead of the studio, one huge word «FREE*» + a red «*FEES APPLY» stamp top-right,
the bottom-right timestamp corner empty.   python3 cover.py [s] -> cover.png + cover.jpg (<= 2 MB) + cover_small.png (320x180)"""
import sys, math, pathlib
import movie as M
from movie import *
from PIL import Image, ImageDraw

HERE = pathlib.Path(__file__).resolve().parent
t = 0.5
S = float(sys.argv[1]) if len(sys.argv) > 1 else 21.0
HX, HY = 500, 470                                                     # Vince's head (output px)
v0 = K.V('tvstudio', 640.0, 360.0, 1.25)
kw = dict(expr='shock', mouth_=1.0, sweat=2.0, shades=0.0, look=(0.15, 0.05), blink=False, legs=False,
          hand_n=(34.0, 100.0), hand_f=(-26.0, 98.0), lean=0.0)
a = K.A(C.vince, *K.wpt(v0, HX, HY), S, pin='head', t=t, **kw)
a.near = 0.99
plain = K.shot('tvstudio', M.studio_light, 640.0, 360.0, 1.25, acts=[], t=t, motes=False, dof_k=0)
full = K.shot('tvstudio', M.studio_light, 640.0, 360.0, 1.25, acts=[a], t=t, motes=False, dof_k=0)
mask = (np.abs(full.astype(int) - plain.astype(int)).sum(2) > 10)
H, W = full.shape[:2]
lab = np.zeros_like(mask)
ys, xs = np.where(mask)
x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
lab[y0:y1 + 1, x0:x1 + 1] = True
mask &= lab

# bright sunburst behind the face (US family: hot pink / sunset orange, cyan on the right)
yy, xx = np.mgrid[0:H, 0:W]
cx, cy = 600, 470
ang = np.arctan2(yy - cy, xx - cx); r = np.hypot(yy - cy, xx - cx)
ray = (np.floor((ang + math.pi) / (2 * math.pi) * 20) % 2).astype(bool)
c1, c2 = np.array([255, 60, 160]), np.array([255, 150, 60])
bg = np.where(ray[..., None], c1, c2).astype(float)
glow = np.clip(1 - r / 900, 0, 1)[..., None]
bg = bg * (0.62 + 0.38 * glow) + np.array([255, 240, 160]) * (glow ** 3) * 0.85
cyan = np.clip((xx - 1150) / 770, 0, 1)[..., None]
bg = bg * (1 - cyan * 0.8) + np.array([40, 200, 255]) * cyan * 0.8
bg = bg * 0.84 + K.blur(plain, 9).astype(float) * 0.16              # a ghost of the studio so the place still reads
px = 12
bg = np.repeat(np.repeat(bg[::px, ::px], px, 0), px, 1)[:H, :W]
big = np.clip(bg, 0, 255).astype(np.uint8)


def outline(big, mask, src):
    P_ = 30
    mp = np.pad(mask, P_)
    ol_w = O._dilate(mp, 14)[P_:-P_, P_:-P_] & ~mask
    ol_d = O._dilate(mp, 24)[P_:-P_, P_:-P_] & ~mask & ~ol_w
    big[ol_d] = (28, 16, 48); big[ol_w] = (255, 255, 255)
    big[mask] = src[mask]


# the receipt: from his raised hand, a long curling strip down to the bottom-left
rc = Image.new('RGBA', (230, 1100), (0, 0, 0, 0)); d = ImageDraw.Draw(rc); d.fontmode = '1'
d.rectangle([0, 0, 229, 1099], fill=(250, 248, 238, 255))
rows = [('PARKING', '$14'), ('TOW', '$350'), ('TICKET', '$250'), ('CASH FEE', '$4'), ('GAME', '$441'), ('ROOF', '$9.99'),
        ('OPEN ROOF', '$19.99'), ('CALLS', '$86'), ('1986', '$9.99'), ('CONVENIENCE', '$3.50'), ('FEE FEE', '$1')]
f = O.pfont(24); fb = O.pfont(30)
d.text((14, 16), 'RECEIPT', font=fb, fill=(30, 18, 60, 255))
for i, (n, p) in enumerate(rows):
    y = 70 + i * 66
    d.text((12, y), n, font=f, fill=(60, 50, 80, 255)); d.text((216 - f.getlength(p), y + 28), p, font=f, fill=(210, 40, 110, 255))
d.text((12, 70 + len(rows) * 66 + 10), 'TOTAL', font=fb, fill=(30, 18, 60, 255))
d.text((12, 70 + len(rows) * 66 + 46), '$$$$$$', font=fb, fill=(210, 40, 110, 255))
rc = rc.rotate(-8, expand=True, resample=Image.NEAREST)
rca = np.array(rc)
hx, hy = K.aout(a, v0, 'hand')                                       # the receipt hangs from his raised hand
RX, RY = int(hx) - 150, int(hy) - 30
rm = np.zeros((H, W), bool); rsrc = np.zeros_like(big)
hh, ww = min(H - RY, rca.shape[0]), min(W - RX, rca.shape[1])
sub = rca[:hh, :ww]
rm[RY:RY + hh, RX:RX + ww] = sub[..., 3] > 0
rsrc[RY:RY + hh, RX:RX + ww] = sub[..., :3]

# composite: receipt behind Vince's body but in front of the burst; one common outline for both
allm = mask | rm
src = np.where(mask[..., None], full, rsrc)
outline(big, allm, src)

# small deadpan Fran on the right, glowing (neon needs no outline)
K.fran(big, 1360, 1010, 470, t, talk=0.0, lid=0.75, look=-1.0)

# one huge word + the stamp, top-right, clear of the faces and the bottom-right timestamp
ti = K.title_trim(K.chrome_title(['FREE*'], 210, width=1300))
O.overlay(big, ti, 1920 - ti.shape[1] - 60, 40, 1.0)
stp = O.sticker('*FEES APPLY', fg=(255, 60, 80), size=54)
O.overlay(big, stp, 1920 - stp.shape[1] - 40, 40 + ti.shape[0] + 6, 1.0)
AT.juice(big, 1.15, 1.06)

im = Image.fromarray(big)
im.save(HERE / 'cover.png')
im.resize((320, 180), Image.LANCZOS).save(HERE / 'cover_small.png')
q = 92
while True:
    im.save(HERE / 'cover.jpg', quality=q)
    if (HERE / 'cover.jpg').stat().st_size <= 2_000_000 or q < 60: break
    q -= 4
print(HERE / 'cover.jpg', (HERE / 'cover.jpg').stat().st_size)
