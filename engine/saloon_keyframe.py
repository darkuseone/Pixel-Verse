"""Code-only detailed pixel-art keyframe: saloon «Пыльный кактус».
Canvas 360x640 logical px -> x3 = 1080x1920. Flat material colors + stepped (Bayer-dithered) lighting
+ final palette quantization for a cohesive pixel-art look."""
import numpy as np, math
from PIL import Image, ImageDraw, ImageFont
import paths as PATHS
import scene as S

W, H = 360, 640
S.W, S.H = W, H
S.YY, S.XX = [a.astype(np.float32) + 0.5 for a in np.mgrid[0:H, 0:W]]
XX, YY = S.XX, S.YY
rng = np.random.default_rng(11)
FONT = PATHS.FONT_PX
BAYER4 = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + 0.5) / 16.0
BAY = np.tile(BAYER4, (H // 4, W // 4))

F = np.zeros((H, W, 3), np.float32)
MAT = np.zeros((H, W), np.int16)      # material id (for lighting rules)
EMIT = np.zeros((H, W), np.float32)   # emissive (not darkened)


def C(*c): return np.array(c, np.float32)
def rect(x0, y0, x1, y1, col, mat=0, emit=0.0):
    x0, y0, x1, y1 = int(max(0, x0)), int(max(0, y0)), int(min(W, x1)), int(min(H, y1))
    if x0 >= x1 or y0 >= y1: return
    F[y0:y1, x0:x1] = col; MAT[y0:y1, x0:x1] = mat; EMIT[y0:y1, x0:x1] = emit
def mask_put(m, col, mat=0, emit=0.0):
    F[m] = col; MAT[m] = mat; EMIT[m] = emit
def ellm(cx, cy, rx, ry): return ((XX - cx) / rx) ** 2 + ((YY - cy) / ry) ** 2 <= 1
def poly(pts):
    img = Image.new('L', (W, H), 0); ImageDraw.Draw(img).polygon([tuple(p) for p in pts], fill=1)
    return np.array(img).astype(bool)
def line(x0, y0, x1, y1, col, w=1):
    img = Image.new('L', (W, H), 0); ImageDraw.Draw(img).line((x0, y0, x1, y1), fill=1, width=w)
    mask_put(np.array(img).astype(bool), col)
def text(s, cx, cy, size, col, shadow=None, emit=0.0):
    f = ImageFont.truetype(FONT, size); bb = f.getbbox(s); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    img = Image.new('L', (W, H), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text((int(cx - tw / 2) - bb[0], int(cy - th / 2) - bb[1]), s, font=f, fill=255)
    m = np.array(img) > 127
    if shadow is not None: mask_put(np.roll(np.roll(m, 1, 0), 1, 1) & ~m, shadow)
    mask_put(m, col, emit=emit)

# ---------------------------------------------------------------- materials
WOOD = [C(58, 34, 22), C(84, 50, 30), C(110, 68, 40), C(134, 86, 52), C(160, 108, 66)]
WALL_TOP, WALL_BOT, FLOOR_Y, BAR_TOP, BAR_FRONT_BOT = 62, 430, 505, 430, 505

def planks_v(x0, x1, y0, y1, pw, base, seed=0, seam=None):
    r = np.random.default_rng(seed)
    x = x0
    while x < x1:
        w = pw + r.integers(-2, 3)
        tone = base + r.uniform(-9, 9)
        rect(x, y0, x + w, y1, tone)
        # grain
        for g in range(r.integers(2, 4)):
            gx = x + r.integers(2, max(3, w - 2)); ph = r.uniform(0, 6)
            ys = np.arange(y0, y1)
            xs = (gx + 1.2 * np.sin(ys * 0.07 + ph)).astype(int)
            ok = (xs >= x) & (xs < x + w)
            F[ys[ok], xs[ok]] = tone * 0.86
        for k in range(r.integers(0, 2)):  # knot
            ky = r.integers(y0 + 6, max(y0 + 7, y1 - 6)); kx = x + w // 2
            m = ellm(kx, ky, 1.8, 2.6); F[m] = tone * 0.7
        F[y0:y1, x] = (seam if seam is not None else tone * 0.55)
        x += w

# ---------------------------------------------------------------- back wall + ceiling
planks_v(0, W, WALL_TOP, WALL_BOT, 15, C(118, 76, 46), seed=1)
rect(0, 0, W, WALL_TOP, C(46, 28, 20))
for bx in range(0, W, 60):  # ceiling beams
    rect(bx, 0, bx + 20, WALL_TOP, C(70, 42, 26)); rect(bx, 0, bx + 3, WALL_TOP, C(92, 58, 36))
rect(0, WALL_TOP - 8, W, WALL_TOP, C(78, 48, 30)); rect(0, WALL_TOP - 1, W, WALL_TOP + 1, C(40, 24, 16))
# wainscot rail
rect(0, 300, W, 305, C(88, 54, 32)); rect(0, 300, W, 301, C(150, 102, 62))

# ---------------------------------------------------------------- window (right) with light
wx0, wy0, wx1, wy1 = 292, 118, 352, 238
rect(wx0 - 5, wy0 - 5, wx1 + 5, wy1 + 7, C(70, 42, 26))
for y in range(wy0, wy1):
    k = (y - wy0) / (wy1 - wy0)
    F[y, wx0:wx1] = C(255, 232, 178) * (1 - k) + C(240, 176, 112) * k
EMIT[wy0:wy1, wx0:wx1] = 1
# desert outside: mesa + cactus silhouettes
mes = poly([(wx0, 210), (wx0 + 12, 196), (wx0 + 30, 196), (wx0 + 38, 206), (wx1, 204), (wx1, wy1), (wx0, wy1)])
F[mes] = C(214, 132, 92); EMIT[mes] = 1
cm = ellm(wx0 + 46, 214, 2.5, 12) | ellm(wx0 + 41, 212, 1.6, 4) | ellm(wx0 + 51, 209, 1.6, 4)
F[cm] = C(120, 120, 70); EMIT[cm] = 1
rect(wx0, (wy0 + wy1) // 2 - 1, wx1, (wy0 + wy1) // 2 + 2, C(70, 42, 26))  # mullions
rect((wx0 + wx1) // 2 - 1, wy0, (wx0 + wx1) // 2 + 2, wy1, C(70, 42, 26))
rect(wx0 - 8, wy1 + 4, wx1 + 8, wy1 + 9, C(96, 60, 36)); rect(wx0 - 8, wy1 + 4, wx1 + 8, wy1 + 5, C(150, 100, 60))
# torn curtains
for side, x in ((0, wx0 - 3), (1, wx1 - 9)):
    for i in range(12):
        rect(x + (i % 3), wy0 - 4 + i * 10, x + 12 - (i % 2), wy0 + 6 + i * 10, C(150, 50, 44) if i % 2 else C(132, 42, 38))

# ---------------------------------------------------------------- saloon sign
rect(96, 72, 264, 106, C(60, 34, 20)); rect(99, 75, 261, 103, C(174, 118, 66)); rect(99, 75, 261, 78, C(206, 150, 88))
for nx in (103, 255): rect(nx, 87, nx + 2, 89, C(220, 210, 190))
text('ПЫЛЬНЫЙ', 180, 84, 8, C(250, 226, 150), C(70, 34, 18))
text('КАКТУС', 180, 96, 8, C(250, 226, 150), C(70, 34, 18))
# bull skull above sign
sk = ellm(180, 62, 9, 6); F[sk] = C(232, 222, 200)
for s in (-1, 1):
    hm = poly([(180 + s * 7, 60), (180 + s * 24, 50), (180 + s * 28, 44), (180 + s * 22, 55), (180 + s * 8, 64)])
    F[hm] = C(236, 226, 206)
rect(176, 61, 178, 63, C(40, 26, 20)); rect(182, 61, 184, 63, C(40, 26, 20))

# ---------------------------------------------------------------- mirror + back bar shelves
rect(118, 122, 242, 214, C(64, 38, 22)); rect(122, 126, 238, 210, C(92, 112, 118))
for i in range(0, 90, 3):  # mirror sheen diagonals
    line(126 + i, 206, 150 + i, 130, C(118, 140, 146))
rect(122, 126, 238, 130, C(140, 164, 168))
for i in range(7): F[ellm(150 + i * 10, 150, 1.2, 2)] = C(255, 230, 150)                   # chandelier reflection
rect(122, 180, 238, 210, C(78, 90, 92))                                                    # reflected shelves
for x in range(126, 236, 7): rect(x, 186 + (x % 3), x + 3, 198, C(96, 120, 100) if x % 2 else C(120, 96, 80))
for sy in (236, 270, 304):
    rect(84, sy, 276, sy + 5, C(96, 60, 34)); rect(84, sy, 276, sy + 1, C(160, 108, 64)); rect(84, sy + 5, 276, sy + 7, C(40, 24, 16))
BOTTLE_COLS = [C(70, 120, 60), C(120, 70, 40), C(160, 90, 40), C(200, 190, 170), C(90, 60, 110), C(150, 40, 40), C(60, 100, 120)]
def bottle(x, base, col, h, kind):
    if kind == 0:  # wine bottle
        rect(x, base - h, x + 6, base, col); rect(x + 2, base - h - 6, x + 4, base - h, col)
    elif kind == 1:  # squat flask
        m = ellm(x + 4, base - h * 0.4, 4.5, h * 0.4); F[m] = col; rect(x + 3, base - h, x + 5, base - h * 0.7, col)
    else:  # jug
        rect(x, base - h, x + 8, base, col); rect(x + 8, base - h + 3, x + 10, base - 4, col * 0.8)
    rect(x + 1, base - h + 2, x + 2, base - 3, np.minimum(col * 1.5 + 30, 255))       # highlight
    rect(x + 1, base - h // 2 - 2, x + 5, base - h // 2 + 2, C(230, 214, 170))       # label
for sy in (236, 270, 304):
    x = 88
    while x < 268:
        if 120 < x < 240 and sy == 236: x += 1; continue
        k = int(rng.integers(0, 3)); h = int(rng.integers(14, 22)); col = BOTTLE_COLS[int(rng.integers(0, len(BOTTLE_COLS)))]
        bottle(x, sy, col, h, k); x += int(rng.integers(9, 13))
# glasses row on top shelf under mirror
for gx in range(126, 236, 9):
    rect(gx, 226, gx + 6, 236, C(190, 210, 214)); rect(gx + 1, 227, gx + 2, 235, C(240, 250, 250))

# ---------------------------------------------------------------- left wall: poster, menu board, rifle
rect(10, 118, 72, 196, C(236, 218, 170)); rect(10, 194, 72, 196, C(200, 176, 124)); rect(70, 118, 72, 196, C(200, 176, 124))
mask_put(poly([(64, 118), (72, 118), (72, 128)]), C(118, 76, 46))
text('РОЗЫСК', 41, 128, 8, C(130, 34, 26))
fm = ellm(41, 157, 10, 12); F[fm] = C(226, 176, 136)
rect(27, 142, 55, 146, C(46, 40, 48)); F[ellm(41, 138, 9, 6)] = C(46, 40, 48)
rect(30, 152, 52, 157, C(24, 20, 24)); rect(34, 153, 36, 155, C(250, 250, 250)); rect(46, 153, 48, 155, C(250, 250, 250))
rect(31, 163, 51, 166, C(34, 26, 24))
text('$500', 41, 184, 8, C(70, 50, 30))
rect(8, 214, 76, 292, C(70, 42, 26)); rect(11, 217, 73, 289, C(38, 50, 42))
text('МЕНЮ', 42, 226, 8, C(236, 236, 220))
for i, s in enumerate(('ВИСКИ 5¢', 'ВОДА 9¢', 'МОРКОВЬ', '   50¢')):
    text(s, 42, 241 + i * 12, 8, C(214, 214, 196) if i != 3 else C(250, 190, 90))
line(20, 104, 80, 110, C(60, 40, 30), 3); line(28, 105, 50, 107, C(140, 140, 150), 2)  # rifle on hooks
# wall clock + horseshoe + lantern
F[ellm(270, 90, 11, 11)] = C(96, 60, 34); F[ellm(270, 90, 8, 8)] = C(236, 226, 196)
line(270, 90, 270, 84, C(30, 20, 16)); line(270, 90, 274, 92, C(30, 20, 16))
F[ellm(270, 106, 2, 5)] = C(200, 160, 70)
hsm = ellm(92, 136, 8, 9) & ~ellm(92, 136, 5, 6) & (YY > 131); F[hsm] = C(150, 150, 160)
for side, lx_ in ((0, 8), (1, 346)):
    rect(lx_ - 1, 318, lx_ + 2, 326, C(40, 30, 26)); rect(lx_ - 5, 326, lx_ + 6, 342, C(60, 50, 40))
    fl2 = ellm(lx_ + 0.5, 334, 3.5, 5.5); F[fl2] = C(255, 214, 110); EMIT[fl2] = 1

# ---------------------------------------------------------------- chandelier (lit)
rect(178, 0, 181, 30, C(40, 30, 26))
cm2 = ellm(180, 36, 34, 6) & ~ellm(180, 36, 30, 3.5); F[cm2] = C(90, 70, 50)
for i in range(7):
    x = 150 + i * 10
    rect(x - 1, 26, x + 2, 34, C(236, 226, 200))
    fl = ellm(x + 0.5, 23, 1.6, 3.2); F[fl] = C(255, 214, 110); EMIT[fl] = 1
    F[ellm(x + 0.5, 23.5, 0.8, 1.6)] = C(255, 250, 220)

# ---------------------------------------------------------------- bartender (behind counter)
bx = 196
F[ellm(bx, 398, 27, 36)] = C(238, 236, 228)                         # shirt torso
F[ellm(bx, 404, 20, 34) & (np.abs(XX - bx) > 6)] = C(56, 60, 78)    # dark vest (open front)
rect(bx - 1, 372, bx + 1, 430, C(200, 196, 186))                    # shirt placket
for by in (380, 390, 400, 410): rect(bx - 1, by, bx + 1, by + 2, C(90, 80, 70))
for side in (-1, 1):                                                  # arms, sleeve garters
    ax = bx + side * 26
    F[ellm(ax, 392, 8, 16)] = C(238, 236, 228)
    rect(ax - 7, 386, ax + 7, 390, C(190, 40, 40))
F[ellm(bx - 14, 414, 9, 7)] = C(232, 180, 136); F[ellm(bx + 12, 416, 9, 7)] = C(232, 180, 136)   # hands
rect(bx - 6, 402, bx + 6, 420, C(196, 214, 218)); rect(bx - 5, 404, bx - 3, 418, C(250, 255, 255))  # glass
F[poly([(bx - 22, 408), (bx - 4, 404), (bx + 2, 424), (bx - 18, 426)])] = C(236, 230, 212)          # towel
line(bx - 18, 414, bx - 4, 412, C(200, 60, 50))
F[ellm(bx, 366, 5, 3)] = C(190, 40, 40); F[ellm(bx - 6, 366, 4, 3)] = C(170, 30, 30); F[ellm(bx + 6, 366, 4, 3)] = C(170, 30, 30)  # bow tie
F[ellm(bx, 340, 15, 17)] = C(232, 180, 136)                          # head
F[ellm(bx, 346, 15, 11) & (YY > 346)] = C(214, 160, 118)              # jaw shade
F[ellm(bx, 327, 13, 7) & (YY < 330)] = C(246, 200, 160)               # bald shine top
F[ellm(bx - 14, 338, 4, 7)] = C(60, 44, 36); F[ellm(bx + 14, 338, 4, 7)] = C(60, 44, 36)          # side hair
F[ellm(bx - 16, 342, 3, 4)] = C(214, 160, 118); F[ellm(bx + 16, 342, 3, 4)] = C(214, 160, 118)    # ears
for ex in (-6, 6):
    F[ellm(bx + ex, 338, 3, 2.5)] = C(250, 250, 244); rect(bx + ex - 1, 337, bx + ex + 1, 340, C(30, 20, 18))
    rect(bx + ex - 4, 333, bx + ex + 4, 335, C(60, 44, 36))                                        # brows
F[ellm(bx, 344, 3.5, 3)] = C(220, 140, 110)                           # nose
F[ellm(bx - 9, 346, 3, 2)] = C(236, 150, 130); F[ellm(bx + 9, 346, 3, 2)] = C(236, 150, 130)      # blush
F[poly([(bx - 17, 351), (bx - 3, 347), (bx, 350), (bx + 3, 347), (bx + 17, 351), (bx + 19, 346), (bx + 14, 355), (bx, 352), (bx - 14, 355), (bx - 19, 346)])] = C(60, 36, 24)
# ---------------------------------------------------------------- bar counter
rect(0, BAR_TOP, W, BAR_TOP + 10, C(150, 96, 56)); rect(0, BAR_TOP, W, BAR_TOP + 2, C(196, 138, 84))
rect(0, BAR_TOP + 10, W, BAR_TOP + 12, C(40, 24, 16))
planks_v(0, W, BAR_TOP + 12, BAR_FRONT_BOT, 30, C(112, 70, 40), seed=4, seam=C(56, 32, 20))
for px0 in range(4, W, 30):  # raised panels
    rect(px0 + 4, BAR_TOP + 20, px0 + 24, BAR_FRONT_BOT - 12, C(100, 62, 36))
    rect(px0 + 4, BAR_TOP + 20, px0 + 24, BAR_TOP + 21, C(150, 100, 60))
rect(0, BAR_FRONT_BOT - 8, W, BAR_FRONT_BOT - 5, C(200, 160, 70))   # brass foot rail
rect(0, BAR_FRONT_BOT - 8, W, BAR_FRONT_BOT - 7, C(250, 220, 130))
# counter items: beer tap, mugs, oil lamp, bowl of peanuts
rect(240, 404, 246, 430, C(200, 160, 70)); rect(236, 402, 250, 407, C(220, 186, 96)); rect(242, 396, 244, 404, C(60, 30, 20))
for mx in (60, 256):
    rect(mx, 414, mx + 12, 430, C(214, 190, 120)); rect(mx + 12, 417, mx + 16, 427, C(170, 150, 96))
    rect(mx, 412, mx + 12, 417, C(250, 248, 236)); rect(mx + 2, 418, mx + 4, 428, C(240, 220, 150))
lx = 94  # oil lamp
F[ellm(lx, 422, 8, 7)] = C(180, 130, 60); rect(lx - 4, 398, lx + 5, 416, C(210, 226, 220))
fl = ellm(lx + 0.5, 408, 2.5, 5); F[fl] = C(255, 214, 110); EMIT[fl] = 1
F[ellm(lx + 0.5, 409, 1.2, 2.5)] = C(255, 250, 220)
F[ellm(140, 427, 11, 4) & (YY < 430)] = C(160, 110, 60)
for i in range(9): rect(132 + (i * 5) % 17, 422 + (i % 2), 135 + (i * 5) % 17, 424 + (i % 2), C(214, 170, 110))

# ---------------------------------------------------------------- floor (perspective planks)
VPX, VPY = 180, 260
for y in range(FLOOR_Y, H):
    F[y, :] = C(128, 82, 48) * (0.9 + 0.1 * (y - FLOOR_Y) / (H - FLOOR_Y))
for k in range(-16, 17):
    xb = 180 + k * 34
    line(VPX + (xb - VPX) * (FLOOR_Y - VPY) / (H - VPY), FLOOR_Y, xb, H, C(76, 46, 28))
yy = FLOOR_Y
step = 7
while yy < H:
    rect(0, int(yy), W, int(yy) + 1, C(96, 60, 36)); yy += step; step *= 1.22
for i in range(160):  # sawdust + scuffs
    x, y = int(rng.integers(0, W)), int(rng.integers(FLOOR_Y + 2, H))
    F[y, x] = C(196, 150, 96) if i % 3 else C(90, 56, 34)

# ---------------------------------------------------------------- piano + pianist (left background, in front of bar)
rect(0, 432, 58, 520, C(52, 30, 22)); rect(0, 432, 58, 436, C(90, 58, 36))
rect(0, 470, 64, 478, C(40, 24, 16)); rect(2, 464, 60, 470, C(240, 236, 224))
for kx in range(4, 60, 5): rect(kx, 464, kx + 2, 468, C(24, 20, 20))
rect(20, 440, 40, 458, C(236, 226, 196)); line(22, 446, 38, 446, C(90, 80, 70)); line(22, 451, 38, 451, C(90, 80, 70))
F[ellm(66, 452, 9, 16)] = C(70, 90, 110)            # pianist back
F[ellm(68, 428, 7, 7)] = C(214, 164, 124)
F[ellm(68, 423, 11, 3)] = C(50, 40, 34); F[ellm(68, 419, 6, 5)] = C(50, 40, 34)   # bowler hat
rect(58, 466, 62, 474, C(214, 164, 124))

# ---------------------------------------------------------------- foreground poker table (bottom-left)
F[ellm(58, 612, 86, 26)] = C(40, 90, 54); F[ellm(58, 612, 86, 26) & (YY > 622)] = C(30, 70, 42)
F[ellm(58, 606, 84, 22) & ~ellm(58, 606, 78, 18)] = C(90, 56, 34)
for i, (cx, cy) in enumerate(((36, 600), (46, 604), (70, 598), (84, 606))):
    rect(cx, cy, cx + 9, cy + 12, C(246, 244, 236)); rect(cx + 2, cy + 2, cx + 4, cy + 4, C(190, 30, 30) if i % 2 else C(20, 20, 20))
for i in range(6):
    F[ellm(100 + i * 2, 606 - i * 2, 5, 2)] = C(200, 40, 40) if i % 2 else C(240, 240, 240)
F[ellm(18, 600, 6, 3)] = C(214, 190, 120); rect(12, 588, 24, 600, C(214, 190, 120)); rect(12, 586, 24, 590, C(250, 248, 236))
# a sleeping patron's arm + hat on table
F[ellm(128, 598, 14, 6)] = C(110, 70, 40); F[ellm(130, 590, 11, 4)] = C(90, 60, 40)
# spittoon + barrel
F[ellm(330, 616, 14, 9)] = C(180, 140, 60); F[ellm(330, 610, 10, 3)] = C(60, 40, 20); F[ellm(328, 614, 2, 5)] = C(240, 210, 130)

# ---------------------------------------------------------------- characters (engine primitives, big scale)
class ACam:
    def __init__(s, ax, ay, sx, sy, sc, flip=False): s.ax, s.ay, s.sx, s.sy, s.sc, s.flip = ax, ay, sx, sy, sc, flip
    def p(s, x, y):
        X = (x - s.ax) * s.sc
        return (s.sx + (-X if s.flip else X), s.sy + (y - s.ay) * s.sc)
_e0 = S.ell
def ell_flip(L, cxy, rx, ry, c, ang=0.0, **kw):
    if getattr(L.cam, 'flip', False): ang = -ang
    return _e0(L, cxy, rx, ry, c, ang, **kw)
S.ell = ell_flip

def comp_layer(L):
    m = L.m; F[m] = L.col[m].astype(np.float32); MAT[m] = 2

# stool
F[ellm(118, 486, 16, 4)] = C(150, 40, 40); F[ellm(118, 484, 16, 3)] = C(186, 60, 50)
for sx in (106, 130): line(sx, 488, sx - 4 + (sx - 106) // 3, 560, C(80, 50, 30), 3)
line(104, 530, 132, 530, C(80, 50, 30), 2)
# Billy (hatless — the hat is on Molniya), sitting, glass in hand
Lb = S.Layer(ACam(1000, 1000, 118, 482, 7.2))
pose = dict(nleg=(1.45, 0.05), fleg=(1.35, 0.15), narm=(1.25, 2.05), farm=(0.6, 1.2))
S.CC['mst'] = (96, 60, 36)
S.cowboy(Lb, (1000, 1000), 0.08, pose, hat_on=False, mouth=0.0)
S.ell(Lb, (1000.4, 1000 - 11.3), 2.8, 1.5, (104, 66, 40), 0.1, hi=(136, 90, 56))     # hair on top
S.cap(Lb, (998.2, 1000 - 11.0), (997.6, 1000 - 8.6), 0.9, 0.6, (104, 66, 40))           # sideburn
S.outline(Lb, (26, 16, 12)); comp_layer(Lb)
hx, hy = Lb.cam.p(1000.6 + 0.08 * 9.7, 1000 - 9.7)   # head centre
hx, hy = int(hx), int(hy)
SK, SKD, HAIR, HAIRH = C(236, 186, 144), C(206, 150, 112), C(104, 66, 40), C(140, 92, 56)
head = ellm(hx + 1, hy, 17, 19); mask_put(head | ellm(hx + 1, hy + 7, 15, 14), SK, 2)
mask_put(ellm(hx - 3, hy + 9, 13, 9) & (YY > hy + 6), SKD, 2)                             # jaw shade
mask_put(ellm(hx - 13, hy + 1, 4, 6), SKD, 2)                                              # ear
mask_put(ellm(hx - 2, hy - 12, 18, 10) & (YY < hy - 5), HAIR, 2)                           # hair
for dx_, ln in ((-14, 9), (-6, 11), (2, 10), (9, 7)):
    line(hx + dx_, hy - 14, hx + dx_ + 6, hy - 14 - ln * 0.6, HAIR, 4)
mask_put(ellm(hx - 4, hy - 16, 8, 3), HAIRH, 2)
ex, ey = hx + 8, hy - 1
mask_put(ellm(ex, ey, 3.4, 3.8), C(250, 250, 244), 2); rect(ex + 1, ey - 2, ex + 4, ey + 2, C(30, 20, 16)); F[ey - 1, ex + 2] = C(255, 255, 255)
mask_put(ellm(ex + 1, ey - 1, 3.8, 2.4) & (YY < ey - 1), SKD, 2)                          # sad heavy lid
line(ex - 5, ey - 7, ex + 5, ey - 5, HAIR, 2)                                              # droopy brow
mask_put(ellm(hx + 15, hy + 3, 4, 3.5), C(222, 160, 120), 2)                               # nose
mask_put(ellm(hx + 3, hy + 6, 4, 2.6), C(236, 150, 130), 2)                                # red cheek
mask_put(poly([(hx + 4, hy + 9), (hx + 18, hy + 8), (hx + 20, hy + 13), (hx + 12, hy + 11), (hx + 6, hy + 14)]), C(96, 60, 36), 2)  # mustache
line(hx + 9, hy + 15, hx + 15, hy + 16, C(150, 70, 60), 1)                                  # mouth
for i in range(18):
    sx_, sy_ = hx - 6 + (i * 7) % 20, hy + 10 + (i * 5) % 8
    if not (hx + 4 < sx_ and sy_ < hy + 14): F[sy_, sx_] = C(170, 120, 92)
gx, gy = Lb.cam.p(1000 + 4.2, 1000 - 7.4)
rect(gx - 3, gy - 8, gx + 5, gy + 2, C(200, 220, 222)); rect(gx - 2, gy - 4, gx + 4, gy + 1, C(214, 150, 60)); rect(gx - 2, gy - 8, gx - 1, gy + 1, C(250, 255, 255))
# Molniya (faces left, wearing Billy's hat, carrot in mouth)
Lh = S.Layer(ACam(1000, 1000, 352, 612, 6.2, flip=True))
P = S.stand_pose(0); P.update(lid=0.55, ear=0.25, neck=-0.95, head=0.62, jaw=0.2)
T, hs, hd_, up = S.draw_horse(Lh, 1000, 1000 - 19, P, 0.0, 0.0, saddle=True)
pos, rot = S.head_hat_anchor(1000, 1000 - 19, P); S.hat(Lh, pos, rot)
he = (hs[0] + hd_[0] * 8.5, hs[1] + hd_[1] * 8.5); dn = (-hd_[1], hd_[0])
c0 = (he[0] + dn[0] * 1.4 - hd_[0] * 0.6, he[1] + dn[1] * 1.4 - hd_[1] * 0.6)
S.cap(Lh, c0, (c0[0] + 4.6, c0[1] + 0.7), 1.3, 0.45, (236, 128, 40), hi=(255, 176, 90))
for a in (-0.5, 0.0, 0.5): S.cap(Lh, c0, (c0[0] - 2.0, c0[1] - 1.2 - a), 0.45, 0.25, (84, 160, 60))
S.draw_ears(Lh, hs, hd_, up, P['ear'])
S.outline(Lh, (30, 18, 12)); comp_layer(Lh)
ecx, ecy = Lh.cam.p(hs[0] + hd_[0] * 2.0 + up[0] * 1.0, hs[1] + hd_[1] * 2.0 + up[1] * 1.0)
F[ellm(ecx, ecy, 4.2, 4.2)] = C(30, 18, 14); F[ellm(ecx - 1, ecy + 1, 2.4, 2.4)] = C(70, 44, 30)
F[int(ecy) + 1, int(ecx) - 2] = C(255, 255, 255); F[int(ecy) + 1, int(ecx) - 1] = C(255, 255, 255)
F[ellm(ecx, ecy - 1.5, 5.0, 3.2) & (YY < ecy - 0.5)] = C(120, 70, 40)                      # half-lid (deadpan)
line(ecx - 5, ecy - 1, ecx + 5, ecy - 1, C(40, 22, 14), 1)

# ---------------------------------------------------------------- lighting pass (stepped + dithered)
Lm = np.full((H, W), 0.62, np.float32)
def glow(cx, cy, r, amp):
    d = np.sqrt((XX - cx) ** 2 + (YY - cy) ** 2) / r
    return amp * np.clip(1 - d, 0, 1) ** 1.6
Lm += glow(180, 30, 330, 0.75)            # chandelier
Lm += glow(95, 408, 110, 0.55)            # oil lamp
Lm += glow(322, 180, 150, 0.45)           # window
Lm += glow(8, 334, 70, 0.35) + glow(346, 334, 70, 0.35)
# window beam (diagonal band toward floor, left)
bx0, by0, bdx, bdy = 322, 180, -0.62, 1.0
t = ((XX - bx0) * bdx + (YY - by0) * bdy) / (bdx * bdx + bdy * bdy)
px, py = bx0 + t * bdx, by0 + t * bdy
dist = np.sqrt((XX - px) ** 2 + (YY - py) ** 2)
beam = (t > 0) & (dist < 30 + 0.12 * t)
Lm += beam * 0.28 * np.clip(1 - t / 700, 0, 1)
# ceiling / top & bottom darkening (vignette)
vig = ((XX - 180) / 230) ** 2 + ((YY - 330) / 420) ** 2
Lm -= np.clip(vig - 0.45, 0, 1) * 0.45
# quantize light into steps with bayer dithering
steps = 6
Lq = np.floor(np.clip(Lm, 0.05, 1.35) * steps + (BAY - 0.5) * 0.45) / steps
Lsm = np.floor(np.clip(Lm, 0.05, 1.35) * 3 + 0.5) / 3
warm = np.stack([np.ones_like(Lq) * 1.06, np.ones_like(Lq) * 0.98, np.ones_like(Lq) * 0.86], -1)
cool = np.stack([np.ones_like(Lq) * 0.82, np.ones_like(Lq) * 0.86, np.ones_like(Lq) * 1.06], -1)
# bartender counts as hero (no dither noise)
MAT[322:430, 150:242] = np.where(np.abs(F[322:430, 150:242] - C(118, 76, 46)).sum(-1) > 60, 2, MAT[322:430, 150:242])
tint = np.where((Lq > 0.75)[..., None], warm, np.where((Lq < 0.5)[..., None], cool, 1.0))
chars = MAT == 2
tint = np.where(chars[..., None], 1.0, tint)
Lq = np.where(chars, np.clip(Lsm, 0.8, 0.95), Lq)       # heroes: flat readable light, no dither noise
out = F * Lq[..., None] * 1.15 * tint
out = np.where(EMIT[..., None] > 0, F, out)
# light shafts: faint additive specks in the beam (dust)
dust = beam & (rng.random((H, W)) > 0.994)
out[dust] = out[dust] * 0.4 + 170
out = np.clip(out, 0, 255).astype(np.uint8)

img = Image.fromarray(out)
q = img.quantize(colors=110, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
q.resize((W * 3, H * 3), Image.NEAREST).save(PATHS.build('saloon_keyframe.png'))
q.resize((W, H)).save(PATHS.build('saloon_small.png'))
print('ok')
