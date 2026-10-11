"""CTR cover 1920x1080 v2 (12.10.2026, docs/covers.md §«Обложка длинного видео 16:9»): one dominant shrieking face (Florida Man, ~45 % of
frame, left), secondary angry judge with gavel (right), bright saturated neon sunburst instead of the dark courtroom, 1 huge word + stamp,
bottom-right timestamp zone empty.   python3 cover.py -> cover.png + cover.jpg (<= 2 MB) + cover_small.png (mobile preview 320x180)"""
import sys, math
import movie as M
from movie import *

t = 0.5
v0 = view_at(COURT, 640, 360, 1.25, SX, SY)
def at(px, py): return K.wpt(v0, px, py)
FMS, FMX, FMY = float(sys.argv[1]) if len(sys.argv) > 1 else 40.0, 330, 560
acts = [A(C.fm, *at(FMX, FMY), FMS, pin='head', t=t, jumpsuit=True, expr='shriek', mouth_=1.0, sweat=1.0, glasses_drop=1.0, look=(0.5, 0.1)),
        A(C.tanner, *at(1500, 680), 23.0, flip=True, pin='head', t=t, uniform='judge', jobs=8, gavel=True, expr='angry',
          hand_n=(12.0, 64.0), look=(-0.7, 0.1))]
plain = K.shot(COURT, light_court, 640, 360, 1.25, acts=[], sx=SX, sy=SY)
full = K.shot(COURT, light_court, 640, 360, 1.25, acts=acts, sx=SX, sy=SY)
mask = (np.abs(full.astype(int) - plain.astype(int)).sum(2) > 6)
mask[:190] = False                                                    # decal flicker at the top is not a character
H, W = full.shape[:2]
# bright neon sunburst (US family: hot pink / cyan / sunshine) centred behind the main face
yy, xx = np.mgrid[0:H, 0:W]
cx, cy = 560, 470
ang = np.arctan2(yy - cy, xx - cx); r = np.hypot(yy - cy, xx - cx)
ray = (np.floor((ang + math.pi) / (2 * math.pi) * 18) % 2).astype(bool)
c1, c2 = np.array([255, 70, 160]), np.array([255, 140, 60])
bg = np.where(ray[..., None], c1, c2).astype(float)
glow = np.clip(1 - r / 900, 0, 1)[..., None]
bg = bg * (0.65 + 0.35 * glow) + np.array([255, 240, 150]) * (glow ** 3) * 0.8
cyan = np.clip((xx - 1150) / 770, 0, 1)[..., None]
bg = bg * (1 - cyan * 0.85) + np.array([40, 200, 255]) * cyan * 0.85
# faint court silhouette so the place still reads (bench + seal), blurred and tinted
court = K.dof(plain.copy(), 9).astype(float)
bg = bg * 0.82 + court * 0.18
# pixelate the background to the series' pixel grid
px = 12
small = bg[::px, ::px]
bg = np.repeat(np.repeat(small, px, 0), px, 1)[:H, :W]
big = np.clip(bg, 0, 255).astype(np.uint8)
# thick white + dark outline around the characters so they pop off the background
P = 30                                                                # pad: O._dilate rolls, so edges would wrap around
mp = np.pad(mask, P)
ol_w = O._dilate(mp, 14)[P:-P, P:-P] & ~mask
ol_d = O._dilate(mp, 24)[P:-P, P:-P] & ~mask & ~ol_w
big[ol_d] = (28, 16, 48); big[ol_w] = (255, 255, 255)
big[mask] = full[mask]
# one huge word + the series stamp, top-right, away from faces and the bottom-right timestamp
from endcard import _trim
ti = _trim(K.hook_title(['GUILTY?!'], 150, width=1800, depth=24))
O.overlay(big, ti, 1920 - ti.shape[1] - 50, 50, 1.0)
st = K.allegedly_stamp(64)
O.overlay(big, st, 1920 - st.shape[1] - 90, 50 + ti.shape[0] + 14, 1.0)
from PIL import Image
im = Image.fromarray(big)
im.save(HERE / 'cover.png')
im.resize((320, 180), Image.LANCZOS).save(HERE / 'cover_small.png')
q = 92
while True:
    im.save(HERE / 'cover.jpg', quality=q)
    if (HERE / 'cover.jpg').stat().st_size <= 2_000_000 or q < 60: break
    q -= 4
print(HERE / 'cover.jpg', (HERE / 'cover.jpg').stat().st_size)
