"""Props of «Sunny Palms HOA»: mailbox, golf cart, notice, clipboard, paint-chip fan, spray can, stamp, ticket pad, fund jar.
Hand-held props take (L, hand) in character unit coords; world props take a View (v) or a Chars canvas + world coords.
Conventions as in props/us_cast.py (anchor (1000,1000), H(x, h), +x = facing)."""
import math
import numpy as np
from PIL import Image, ImageDraw
import scene as S
from scene import Layer
import paths as P
from props.folk import H, cap, ell, ellt, dot, poly, outline, _merge, OL

BONE = (232, 222, 200)                 # «Bone» and «Ecru Whisper» are the SAME colour: that is the joke
BONE_HI, BONE_SH = (246, 238, 220), (196, 184, 160)
PINK = (255, 168, 200)


def rect(L, *args):
    """rect(L, (cx, cy), w, h, ang, colour) or rect(L, cx, cy, w, h, ang, colour)"""
    if isinstance(args[0], (tuple, list)): (cx, cy), w, h, ang, c = args[0], *args[1:]
    else: cx, cy, w, h, ang, c = args
    ca, sa = math.cos(ang), math.sin(ang)
    pts = [(cx + dx * ca - dy * sa, cy + dx * sa + dy * ca) for dx, dy in ((-w / 2, -h / 2), (w / 2, -h / 2), (w / 2, h / 2), (-w / 2, h / 2))]
    poly(L, pts, c)


def ltext(L, txt, uxy, h_units, col, ang=0.0):
    """pixel-font text centred at unit coords uxy on a layer (font height ~ h_units)"""
    from PIL import ImageFont
    cm = L.cam
    size = max(6, int(round(h_units * cm.sc)))
    f = ImageFont.truetype(P.FONT_PX, size); bb = f.getbbox(txt)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    img = Image.new('L', (tw + 4, th + 4), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text((2 - bb[0], 2 - bb[1]), txt, font=f, fill=255)
    if ang: img = img.rotate(-math.degrees(ang), expand=True)
    m = np.array(img) > 127; ys, xs = np.nonzero(m)
    cx, cy = cm.p(*uxy)
    yy = (ys + int(cy - m.shape[0] / 2)); xx = (xs + int(cx - m.shape[1] / 2))
    ok = (yy >= 0) & (yy < L.m.shape[0]) & (xx >= 0) & (xx < L.m.shape[1])
    L.col[yy[ok], xx[ok]] = col; L.m[yy[ok], xx[ok]] = True


# ---------------------------------------------------------------- hand-held
def notice(L, h, ang=0.0, w=5.4, hh=7.0, txt='$250', crumple=0.0):
    """pink violation notice held at hand h"""
    cx, cy = h[0] + 0.3, h[1] - 0.4
    rect(L, cx + 0.25, cy + 0.25, w, hh, ang, (214, 120, 150))                   # shadow edge
    rect(L, cx, cy, w, hh, ang, PINK)
    rect(L, cx, cy - hh * 0.36, w - 0.5, 1.3, ang, (200, 40, 70))               # red header
    for k in range(3):
        cap(L, (cx - w * 0.36, cy - hh * 0.1 + k * 0.8), (cx + w * (0.36 - 0.1 * k), cy - hh * 0.1 + k * 0.8), 0.12, 0.12, (150, 90, 110))
    ltext(L, txt, (cx, cy + hh * 0.22), min(2.3, w * 0.84 / len(txt)), (200, 24, 50))
    if crumple > 0:
        for k in range(4):
            cap(L, (cx - w * 0.4 + k * w * 0.25, cy - hh * 0.4), (cx - w * 0.35 + k * w * 0.25, cy + hh * 0.4), 0.15, 0.15, (200, 120, 146))


def clipboard(L, h, ang=-0.15, w=5.4, hh=7.6, title='FORM 27-B'):
    cx, cy = h[0] + 0.6, h[1] - 0.6
    rect(L, cx, cy, w + 0.8, hh + 0.8, ang, (110, 72, 42))
    rect(L, cx, cy, w, hh, ang, (250, 250, 246))
    rect(L, cx, cy - hh * 0.52, 2.4, 1.0, ang, (200, 204, 212))                   # clip
    ltext(L, title, (cx, cy - hh * 0.22), 1.1, (60, 70, 120), ang)
    for k in range(5):
        cap(L, (cx - w * 0.38, cy + hh * (-0.02 + 0.13 * k)), (cx + w * (0.38 - 0.06 * k), cy + hh * (-0.02 + 0.13 * k)), 0.1, 0.1, (150, 158, 176))


def pen(L, h, ang=-0.9):
    cap(L, h, (h[0] + math.cos(ang) * 2.8, h[1] + math.sin(ang) * 2.8), 0.28, 0.28, (40, 60, 150))
    dot(L, (h[0] + math.cos(ang) * 2.9, h[1] + math.sin(ang) * 2.9), (20, 20, 30), 0.25)


def chip_fan(L, h, ang=-1.3, spread=0.28, big=1.0):
    """fan of paint chips; every strip is (almost) the same beige"""
    tones = [BONE, (233, 222, 198), (231, 223, 200), BONE, (232, 221, 199)]
    for k, c in enumerate(tones):
        a = ang + (k - 2) * spread
        L2 = 5.2 * big
        cap(L, h, (h[0] + math.cos(a) * L2, h[1] + math.sin(a) * L2), 0.95 * big, 0.95 * big, (252, 252, 250), None, (150, 140, 120))
        cap(L, h, (h[0] + math.cos(a) * L2 * 0.96, h[1] + math.sin(a) * L2 * 0.96), 0.66 * big, 0.66 * big, c, BONE_HI, BONE_SH)
        dot(L, (h[0] + math.cos(a) * L2 * 0.8, h[1] + math.sin(a) * L2 * 0.8), (170, 160, 140), 0.2)
    dot(L, h, (190, 190, 200), 0.5)


def spray_can(L, h, ang=-0.5, on=0.0):
    ca, sa = math.cos(ang), math.sin(ang)
    a = (h[0] - ca * 1.0, h[1] - sa * 1.0); b = (h[0] + ca * 3.4, h[1] + sa * 3.4)
    cap(L, a, b, 0.95, 0.95, (214, 218, 226), (250, 252, 255), (156, 162, 178))
    cap(L, (a[0] + ca * 1.4, a[1] + sa * 1.4), (a[0] + ca * 2.4, a[1] + sa * 2.4), 1.0, 1.0, BONE, None, BONE_SH)     # label = the colour
    cap(L, b, (b[0] + ca * 0.7, b[1] + sa * 0.7), 0.55, 0.5, (60, 64, 76))
    cap(L, (b[0] + ca * 0.5, b[1] + sa * 0.5), (b[0] + ca * 1.1, b[1] + sa * 1.1 - 0.4), 0.28, 0.28, (250, 250, 250))
    return (b[0] + ca * 1.6, b[1] + sa * 1.6)


def koozie_can(L, h):
    cap(L, (h[0], h[1] - 1.6), (h[0], h[1] + 1.4), 0.95, 0.95, (126, 236, 88), (190, 255, 150), (84, 176, 56))
    cap(L, (h[0], h[1] - 2.3), (h[0], h[1] - 1.7), 0.8, 0.8, (214, 218, 224))


def stamp_tool(L, h, press=0.0):
    y = h[1] + 1.4 * press
    cap(L, (h[0], y - 3.4), (h[0], y - 1.4), 0.7, 0.7, (150, 80, 50), (190, 116, 80), (110, 56, 34))
    rect(L, h[0], y - 0.7, 3.8, 1.1, 0, (60, 60, 70))
    rect(L, h[0], y, 3.0, 0.5, 0, (200, 40, 50))


def ticket_pad(L, h, ang=-0.2, txt='$250', k=0.8):
    rect(L, h[0] + 0.5, h[1] - 0.4, 4.6 * k, 6.0 * k, ang, (150, 60, 90))
    rect(L, h[0] + 0.5, h[1] - 0.4, 4.2 * k, 5.6 * k, ang, PINK)
    ltext(L, txt, (h[0] + 0.5, h[1] - 0.2), 1.4, (200, 24, 50), ang)


def mailbox_held(L, h, ang=0.0, s=1.0):
    """the whole mailbox carried at the chest (its post ripped off)"""
    cx, cy = h[0] - 1.5, h[1] - 0.6
    cap(L, (cx - 2.4 * s, cy), (cx + 2.4 * s, cy), 2.0 * s, 2.0 * s, BONE, BONE_HI, BONE_SH)
    ell(L, (cx + 4.6 * s, cy), 0.9 * s, 1.9 * s, BONE_SH)
    cap(L, (cx - 3.6 * s, cy - 1.6 * s), (cx - 3.6 * s, cy - 4.4 * s), 0.25, 0.25, (200, 40, 50))
    rect(L, cx - 3.2 * s, cy - 4.2 * s, 1.6, 0.9, 0, (214, 46, 56))
    for (x, y) in ((cx - 1.0 * s, cy + 1.5 * s), (cx + 1.6 * s, cy + 1.7 * s)):
        dot(L, (x, y), (150, 100, 70), 0.3)
    dot(L, (cx - 3.4 * s, cy + 1.6 * s), (140, 120, 100), 0.3)                          # a bit of the wooden post still stuck on
    cap(L, (cx - 0.4 * s, cy + 2.0 * s), (cx - 0.4 * s, cy + 3.8 * s), 0.9, 0.9, (150, 110, 70), (180, 140, 96), (110, 78, 48))


# ---------------------------------------------------------------- world props
def mailbox_world(CH, v, x, y, painted=0.0, t=0.0, wob=0.0, s=1.0, flag_up=True, tint=None):
    """mailbox with its centre at world (x, y); s = size in world px per 'unit' of 1.0 == 30 px body length.
    painted 0..1 shows a fresh coat: rust/dents disappear (the colour stays exactly the same)"""
    cam = v.cam(x, y, 8.0 * s)
    L = Layer(cam)
    c, hi, sh = BONE, BONE_HI, BONE_SH
    cap(L, H(-2.6, 0.0), H(2.6, 0.0), 2.35, 2.35, c, hi, sh)
    ell(L, H(5.2, 0.0), 1.0, 2.2, sh if painted < 0.5 else (210, 200, 176))
    dot(L, H(5.5, 0.0), (120, 110, 96), 0.35)
    cap(L, H(-4.4, -1.5), H(-4.4, -5.2), 0.35, 0.35, (206, 44, 52))                       # flag arm
    rect(L, H(-3.6, -5.2), 2.2, 1.3, 0, (232, 52, 60))
    if not flag_up:
        pass
    if painted < 0.5:
        for (px_, py_, r) in ((-1.5, 1.6, 0.5), (0.8, 2.0, 0.4), (-3.0, 0.8, 0.45), (2.6, 1.2, 0.35)):
            dot(L, H(px_, py_), (150, 96, 64), r)
        cap(L, H(-2.0, 1.0), H(-2.3, 2.3), 0.16, 0.12, (170, 110, 76))
    else:
        cap(L, H(-1.4, -1.5), H(1.2, -1.7), 0.35, 0.3, (252, 250, 240))                   # fresh gloss streak
    outline(L, OL)
    CH.add(L)


def golf_cart(CH_back, CH_front, v, x, y, u=4.6, flip=True, t=0.0, brake=0.0, beacon=True):
    """HOA golf cart: draws body+seat into CH_back and canopy/dash/front wheel into CH_front (Brenda goes between).
    Anchor (x,y) = ground under the cart centre. Returns the seat point (world) for Brenda."""
    cam = v.cam(x, y, u, flip)
    bounce = 0.12 * math.sin(t * 9.0) * (1 - brake)
    A = Layer(cam)
    for wx in (-11.0, 11.0):                                                            # far-side wheels first (dark)
        ell(A, H(wx, 3.3 + bounce * 0.2), 3.3, 3.3, (28, 28, 34))
    cap(A, H(-15.5, 6.6 + bounce), H(15.0, 6.6 + bounce), 3.5, 3.4, (250, 248, 240), (255, 255, 255), (196, 200, 208))
    ell(A, H(16.5, 7.2 + bounce), 3.0, 3.1, (250, 248, 240), 0, (255, 255, 255), (196, 200, 208))
    cap(A, H(-16.0, 9.5 + bounce), H(-16.0, 4.0 + bounce), 1.5, 1.5, (236, 234, 226))
    cap(A, H(-9.5, 10.4 + bounce), H(-2.5, 10.4 + bounce), 1.9, 1.9, (232, 214, 170), (250, 236, 196), (190, 168, 120))    # seat
    cap(A, H(-11.0, 10.4 + bounce), H(-11.0, 16.4 + bounce), 1.3, 1.3, (232, 214, 170), (250, 236, 196), (190, 168, 120))  # backrest
    rect(A, H(-1.0, 6.4)[0], H(-1.0, 6.4)[1], 6.0, 3.0, 0, (36, 96, 190))                 # HOA plate
    ltext(A, 'HOA', H(-1.0, 6.4), 1.9, (255, 255, 255))
    outline(A, OL)
    CH_back.add(A)
    B = Layer(cam)
    cap(B, H(5.5, 9.8 + bounce), H(4.0, 14.2 + bounce), 0.55, 0.55, (70, 74, 86))       # steering column
    ell(B, H(3.4, 14.8 + bounce), 0.9, 2.2, (40, 42, 52), 0.5)                           # wheel
    poly(B, [H(7.0, 10.0 + bounce), H(8.8, 13.2 + bounce), H(8.4, 30.6 + bounce), H(6.8, 30.6 + bounce)], (200, 226, 240))   # windshield
    cap(B, H(-13.5, 10.6), H(-13.5, 30.8), 0.5, 0.5, (240, 240, 240)); cap(B, H(8.8, 12.0), H(8.8, 30.8), 0.5, 0.5, (240, 240, 240))
    ell(B, H(-2.0, 31.6), 16.0, 1.5, (120, 226, 190), 0, (170, 250, 220), (70, 168, 136))  # mint canopy
    ell(B, H(-2.0, 30.4), 15.0, 0.5, (70, 168, 136))
    for wx in (-11.0, 11.0):                                                            # near wheels
        ell(B, H(wx, 3.3 + bounce * 0.2), 3.4, 3.4, (24, 24, 30)); ell(B, H(wx, 3.3 + bounce * 0.2), 1.6, 1.6, (196, 200, 210), 0, (240, 242, 250), (140, 144, 158))
    on = beacon and (int(t * 5) % 2 == 0)
    cap(B, H(-12.8, 33.0), H(-12.8, 34.2), 0.7, 0.7, (255, 168, 0) if on else (190, 120, 0))
    cap(B, H(-13.6, 33.2), H(-13.6, 40.0), 0.2, 0.2, (200, 200, 210))
    poly(B, [H(-13.6, 40.0), H(-9.6, 39.0), H(-13.6, 37.6)], (255, 90, 160))                # pink pennant
    outline(B, OL)
    CH_front.add(B)
    return (x + (-1 if flip else 1) * (-5.5) * u, y - 1.5 * u)


def skid_puffs(FX, v, t, t0, x, y, n=7, drift=1.0):
    """tyre smoke: puffs rising from ground point (x, y) after t0"""
    L = Layer(v.wcam())
    u = t - t0
    if u < 0 or u > 1.4: return
    for i in range(n):
        ph = u - i * 0.06
        if ph < 0: continue
        r = 5 + 26 * min(1.0, ph / 0.7)
        px_, py_ = x + drift * (-30 * ph - i * 6), y - 18 * ph
        a = max(0.0, 1 - ph / 1.2)
        if a > 0.15: ell(L, (px_, py_), r, r * 0.7, (232, 232, 236))
    FX.add(L)


# ---------------------------------------------------------------- interior insert: the Beautification Fund
def fund_jar(CH, v, t, level=0.94, pop=0.0):
    """fills the empty jar (world x 258-372, y 295-435) with bills/coins, sticks a label, and draws the BAHAMAS chart on the cork board
    (world x 320-625, y 70-285)"""
    L = Layer(v.wcam())
    fill_top = 435 - 115 * min(1.0, level)
    yy = 432
    k = 0
    while yy > fill_top + 4:
        for xx in range(266, 366, 20):
            jit = ((k * 37) % 7) - 3
            c = (86, 168, 96) if (k + xx) % 3 else (120, 196, 120)
            ell(L, (xx + 8 + jit, yy - 6), 12, 6, c, ((k % 5) - 2) * 0.12)
            dot(L, (xx + 8 + jit, yy - 6), (46, 110, 60), 3)
            k += 1
        yy -= 9
    for (cx, cy) in ((286, fill_top + 2), (330, fill_top - 1), (352, fill_top + 5)):
        ell(L, (cx, cy), 5, 4, (255, 214, 70), 0, (255, 240, 150), (200, 150, 30))        # coins on top
    rect(L, 315, 380, 84, 26, 0, (252, 250, 240))                                        # label
    rect(L, 315, 380, 84, 4, 0, (255, 100, 170))
    CH.add(L)


def fund_insert(big, v, t, level=0.94, pop=0.0, title=('BAHAMAS', '2027')):
    """cork-board chart + jar label drawn straight onto the frame (output px, positions via the view v):
    BAHAMAS 2027 card, thermometer bar `level` (0..1), jar label. pop 0..1 bounces the percentage."""
    from PIL import ImageFont
    import overlays as O
    W_, H_ = big.shape[1], big.shape[0]
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    def o(x, y): return v.opt(x, y)
    def txt(s_, cx, cy, size, col, stroke=None):
        f = ImageFont.truetype(P.FONT_PX, max(8, int(size * v.Z * 3)))
        bb = f.getbbox(s_)
        pos = (cx - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1])
        if stroke:
            for dx in (-3, 0, 3):
                for dy in (-3, 0, 3): d.text((pos[0] + dx, pos[1] + dy), s_, font=f, fill=stroke)
        d.text(pos, s_, font=f, fill=col)
    def box(x0, y0, x1, y1, fill, outline_=None, w=3):
        a, b = o(x0, y0), o(x1, y1)
        d.rectangle([a, b], fill=fill, outline=outline_, width=w)
    box(352, 92, 592, 150, (252, 250, 240), (40, 60, 120), 4)                                # card
    txt(title[0], *o(472, 112), 12, (24, 96, 200)); txt(title[1], *o(472, 136), 12, (255, 90, 160))
    box(352, 176, 592, 210, (236, 236, 240), (40, 40, 60), 4)                                # thermometer track
    fx = 352 + 240 * min(1.0, level)
    box(354, 178, fx, 208, (232, 48, 64))
    for k in range(1, 10):
        a = o(352 + 24 * k, 178); d.line([a, (a[0], a[1] + 10)], fill=(255, 255, 255), width=2)
    pct = f'{int(round(level * 100))}%'
    k = 1.0 + 0.35 * math.sin(min(pop, 1.0) * math.pi) if pop > 0 else 1.0
    txt(pct, *o(472, 242 + 0), 14 * k, (255, 236, 90) if level < 0.999 else (140, 255, 150), (30, 20, 40))
    box(272, 368, 360, 396, (252, 250, 240), (255, 100, 170), 3)                              # jar label
    txt('BEAUTIFICATION', *o(316, 376), 5.2, (60, 60, 90)); txt('FUND', *o(316, 388), 6.0, (200, 40, 70))
    O.overlay(big, np.array(im), 0, 0, 1.0)


# ---------------------------------------------------------------- E02: Kevin the (plastic) emotional support flamingo
FL = dict(pk=(255, 124, 172), hi=(255, 176, 208), sh=(212, 84, 134), dk=(226, 96, 146), beak=(255, 224, 208), vest=(255, 214, 60),
          vest_hi=(255, 240, 150), vest_sh=(208, 160, 30))


def flamingo(CH, cam, t=0.0, vest=True, shades=True, wob=0.0, tilt=0.0):
    """pink plastic lawn flamingo on one leg, ESA vest + tiny aviators; anchor = foot on the ground, ~18 units tall"""
    P = FL
    L = Layer(cam)
    cap(L, H(0.7, 6.4), H(2.6, 5.2), 0.3, 0.3, P['dk'])                                    # tucked leg
    cap(L, H(0.0, 0.0), H(0.2, 6.6), 0.36, 0.3, P['pk'], P['hi'], P['sh'])                  # standing leg
    cap(L, H(-0.9, 0.1), H(1.1, 0.1), 0.3, 0.3, P['pk'])
    poly(L, [H(-2.6, 9.8 + wob), H(-5.8, 7.6), H(-5.0, 10.6 + wob)], P['sh'])                # tail feathers
    ell(L, H(0.4, 9.0 + wob), 3.5 + wob * 0.6, 2.4 - wob * 0.4, P['pk'], -0.22, P['hi'], P['sh'])
    ell(L, H(-0.1 + tilt, 9.3 + wob), 2.2, 1.3, P['hi'], -0.3, None, P['pk'])                # wing
    pts = [H(3.0, 10.4 + wob), H(4.3, 12.4), H(3.4, 14.6), H(4.2, 16.6)]
    for a, b in zip(pts, pts[1:]): cap(L, a, b, 0.8, 0.7, P['pk'], P['hi'], P['sh'])         # S-neck
    ell(L, H(4.7, 17.4), 1.15, 1.0, P['pk'], 0, P['hi'], P['sh'])
    cap(L, H(5.6, 17.4), H(7.0, 16.5), 0.62, 0.42, P['beak'])
    cap(L, H(6.6, 16.7), H(7.5, 16.2), 0.44, 0.3, (30, 26, 30))
    if vest:
        ell(L, H(0.6, 9.2 + wob), 2.6, 2.2, P['vest'], -0.2, P['vest_hi'], P['vest_sh'])
        cap(L, H(-1.4, 9.8), H(2.6, 8.4), 0.22, 0.22, (200, 200, 208))
        ltext(L, 'ESA', (0.7, 9.0), 1.15, (60, 44, 60))
    if shades:
        ell(L, H(4.9, 17.7), 0.72, 0.6, (232, 190, 60)); ell(L, H(4.9, 17.7), 0.56, 0.44, (50, 60, 112))
        dot(L, H(4.7, 17.9), (170, 196, 240), 0.14)
        cap(L, H(4.2, 17.7), H(3.6, 17.5), 0.1, 0.1, (232, 190, 60))
    else:
        dot(L, H(4.9, 17.7), (20, 18, 22), 0.28)
    dot(L, H(0.0, 10.5), (255, 255, 255), 0.3)                                              # plastic glint
    outline(L, OL)
    CH.add(L)


def binder(L, h, ang=-0.1, w=6.0, hh=8.0, title='BYLAWS'):
    """thick HOA rulebook"""
    cx, cy = h[0] + 0.6, h[1] - 0.8
    rect(L, cx + 0.4, cy + 0.4, w + 1.0, hh + 0.6, ang, (18, 30, 70))
    rect(L, cx, cy, w, hh, ang, (36, 74, 168))
    rect(L, cx - w * 0.46, cy, 0.9, hh, ang, (24, 50, 120))                                  # spine
    rect(L, cx + 0.3, cy - hh * 0.12, w * 0.7, hh * 0.34, ang, (250, 250, 246))              # label
    ltext(L, title, (cx + 0.3, cy - hh * 0.12), min(1.3, w * 0.62 / len(title)), (30, 40, 90), ang)
    ltext(L, '4,212 PG', (cx + 0.3, cy + hh * 0.30), 0.9, (200, 210, 240), ang)


def cert_insert(big, t, hl=0.0):
    """full-screen insert: the online «Emotional Support Flamingo» certificate; hl 0..1 highlights the fine print (NOVELTY)"""
    import overlays as O
    W_, H_ = big.shape[1], big.shape[0]
    big[:] = (big * 0.32).astype(np.uint8)
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    x0, y0, x1, y1 = 110, 330, 970, 1400
    wob = int(6 * math.sin(t * 5))
    y0 += wob; y1 += wob
    d.rectangle([x0 - 14, y0 - 14, x1 + 14, y1 + 14], fill=(30, 16, 40, 255))
    d.rectangle([x0, y0, x1, y1], fill=(250, 244, 222, 255), outline=(214, 170, 60, 255), width=12)
    d.rectangle([x0 + 26, y0 + 26, x1 - 26, y1 - 26], outline=(120, 70, 150, 255), width=4)
    def ctext(s_, cy, size, col, stroke=None):
        f = O.pfont(size); bb = f.getbbox(s_)
        pos = ((x0 + x1) // 2 - (bb[2] - bb[0]) / 2 - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1])
        if stroke:
            for dx in (-3, 0, 3):
                for dy in (-3, 0, 3): d.text((pos[0] + dx, pos[1] + dy), s_, font=f, fill=stroke)
        d.text(pos, s_, font=f, fill=col)
    ctext('OFFICIAL', y0 + 110, 40, (120, 70, 150, 255))
    ctext('EMOTIONAL', y0 + 190, 52, (40, 40, 90, 255))
    ctext('SUPPORT', y0 + 260, 52, (40, 40, 90, 255))
    ctext('FLAMINGO', y0 + 350, 74, (230, 60, 130, 255))
    ctext('CERTIFICATE', y0 + 430, 40, (120, 70, 150, 255))
    for k in range(5):                                                                     # five stars
        cx, cy = 260 + k * 140, y0 + 540
        pts = []
        for i in range(10):
            r = 52 if i % 2 == 0 else 22
            a = -math.pi / 2 + i * math.pi / 5
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        d.polygon(pts, fill=(255, 196, 40, 255), outline=(150, 100, 20, 255))
    ctext('5.0 (2 REVIEWS)', y0 + 640, 34, (60, 60, 80, 255))
    d.ellipse([(x0 + x1) // 2 - 120, y0 + 690, (x0 + x1) // 2 + 120, y0 + 880], fill=(214, 170, 60, 255), outline=(150, 100, 20, 255), width=8)
    ctext('ONLY', y0 + 748, 30, (255, 255, 255, 255)); ctext('$19.99', y0 + 820, 44, (255, 255, 255, 255))
    k = min(1.0, hl)
    size = int(20 + 12 * k)
    lines_ = ('*NOVELTY ITEM.', 'NOT A LEGAL DOCUMENT.')
    if k > 0:
        f = O.pfont(size); tw = max(f.getbbox(l_)[2] - f.getbbox(l_)[0] for l_ in lines_)
        cx0 = (x0 + x1) // 2 - tw // 2 - 26
        d.rectangle([cx0, y0 + 920, cx0 + tw + 52, y0 + 920 + size * 2 + 78], fill=(255, 236, 90, int(255 * k)), outline=(230, 40, 60, 255), width=8)
    for i_, l_ in enumerate(lines_):
        ctext(l_, y0 + 960 + i_ * (size + 24), size, (200, 30, 50, 255) if k > 0 else (140, 140, 150, 255))
    O.overlay(big, np.array(im), 0, 0, 1.0)


# ---------------------------------------------------------------- E03: phone, NeighborNet feed, Ring night footage, shovel, tape
def phone(L, h, ang=0.0, w=3.6, hh=6.6, screen='feed'):
    """smartphone held at hand h; screen: feed (green app) | ring (blue camera app) | truck (photo roll of a pickup)"""
    cx, cy = h[0] + 0.4, h[1] - 0.6
    rect(L, cx, cy, w + 0.5, hh + 0.5, ang, (18, 18, 26))
    bg = {'feed': (236, 244, 236), 'ring': (20, 40, 90), 'truck': (28, 30, 40)}[screen]
    rect(L, cx, cy, w, hh, ang, bg)
    if screen == 'feed':
        rect(L, cx, cy - hh * 0.36, w, hh * 0.22, ang, (44, 170, 96))
        for k in range(3): cap(L, (cx - w * 0.36, cy - hh * 0.05 + k * hh * 0.17), (cx + w * (0.36 - 0.12 * k), cy - hh * 0.05 + k * hh * 0.17), 0.12, 0.12, (150, 160, 150))
        UP_dot = dot; UP_dot(L, (cx + w * 0.3, cy - hh * 0.36), (238, 60, 60), 0.4)
    elif screen == 'ring':
        ell(L, (cx, cy - hh * 0.05), w * 0.28, w * 0.28, (70, 150, 255)); dot(L, (cx, cy - hh * 0.05), (12, 24, 60), w * 0.12)
        cap(L, (cx - w * 0.36, cy + hh * 0.34), (cx + w * 0.36, cy + hh * 0.34), 0.13, 0.13, (238, 60, 60))
    else:
        rect(L, cx, cy + hh * 0.05, w * 0.7, hh * 0.22, ang, (220, 60, 60))
        dot(L, (cx - w * 0.22, cy + hh * 0.2), (240, 240, 240), 0.42); dot(L, (cx + w * 0.22, cy + hh * 0.2), (240, 240, 240), 0.42)
        rect(L, cx + w * 0.1, cy - hh * 0.06, w * 0.34, hh * 0.1, ang, (170, 210, 250))


def trash_bag(L, h):
    cx, cy = h[0] + 0.2, h[1] + 2.4
    ell(L, (cx, cy), 2.6, 3.0, (36, 36, 44), 0, (86, 88, 104), (18, 18, 24))
    poly(L, [(cx - 0.5, cy - 2.8), (cx - 1.4, cy - 4.4), (cx - 0.1, cy - 3.6)], (36, 36, 44))
    poly(L, [(cx + 0.3, cy - 2.8), (cx + 1.5, cy - 4.2), (cx + 0.2, cy - 3.4)], (36, 36, 44))
    dot(L, (cx - 0.9, cy - 0.6), (150, 154, 170), 0.3)


def shovel(L, h, ang=-0.5):
    ca, sa = math.cos(ang), math.sin(ang)
    cap(L, (h[0] - ca * 3.5, h[1] - sa * 3.5), (h[0] + ca * 7.5, h[1] + sa * 7.5), 0.38, 0.38, (176, 128, 78), (210, 164, 110), (120, 84, 48))
    b0 = (h[0] + ca * 7.5, h[1] + sa * 7.5)
    ell(L, (b0[0] + ca * 1.6, b0[1] + sa * 1.6), 1.7, 2.3, (176, 184, 196), ang + 1.57, (226, 232, 240), (120, 128, 142))


def tape_hold(L, h):
    rect(L, h[0] + 0.3, h[1] - 0.5, 2.6, 2.4, 0.0, (255, 214, 50))
    rect(L, h[0] + 0.3, h[1] - 0.5, 1.6, 0.6, 0.0, (30, 30, 34))
    cap(L, (h[0] + 1.6, h[1] - 0.2), (h[0] + 3.6, h[1] + 0.4), 0.16, 0.16, (250, 236, 120))


NN_COMMENTS = [('Doug K.', (230, 120, 60), 'Saw him last week too.', 'Also walking.'),
               ('Linda P.', (170, 90, 200), 'He was wearing SHORTS.', 'In public.'),
               ('Hank R.', (60, 150, 210), 'Is this the guy with', 'the flamingo?'),
               ('Marge T.', (220, 90, 130), 'Has anyone seen Mr. Whiskers?', 'Orange. Fat. Judgmental.')]


def neighbornet_feed(big, t, u):
    """full-screen fake neighbourhood-app feed (fictional «NeighborNet»): Brenda's post with a blurry Ring photo and pop-in comments"""
    import overlays as O
    W_, H_ = 1080, 1920
    im = Image.new('RGB', (W_, H_), (232, 238, 232)); d = ImageDraw.Draw(im); d.fontmode = '1'
    def txt(s_, x, y, size, col, anchor='l'):
        f = O.pfont(size); bb = f.getbbox(s_)
        px = x if anchor == 'l' else (x - (bb[2] - bb[0]) // 2 if anchor == 'c' else x - (bb[2] - bb[0]))
        d.text((px - bb[0], y - bb[1]), s_, font=f, fill=col)
    d.rectangle([0, 0, W_, 70], fill=(20, 30, 24)); txt('9:41', 40, 22, 26, (255, 255, 255)); txt('87%', W_ - 40, 22, 26, (255, 255, 255), 'r')
    d.rectangle([0, 70, W_, 220], fill=(44, 170, 96)); txt('neighbornet', 320, 118, 46, (255, 255, 255))
    d.ellipse([W_ - 150, 100, W_ - 70, 180], fill=(255, 255, 255)); d.ellipse([W_ - 100, 90, W_ - 60, 130], fill=(238, 60, 60))
    txt('5', W_ - 80, 100, 26, (255, 255, 255), 'c')
    d.rectangle([0, 220, W_, 300], fill=(255, 255, 255)); txt('Feed', 110, 248, 26, (90, 90, 90)); txt('SAFETY!', 470, 248, 26, (220, 40, 50)); txt('Lost & Found', 770, 248, 26, (90, 90, 90))
    d.rectangle([380, 292, 640, 300], fill=(220, 40, 50))
    d.rectangle([30, 330, W_ - 30, 1050], fill=(255, 255, 255), outline=(200, 208, 200), width=4)
    d.ellipse([60, 356, 170, 466], fill=(255, 150, 200)); d.ellipse([70, 366, 160, 400], fill=(255, 255, 255))
    txt('Brenda W.', 200, 366, 30, (30, 40, 40)); txt('HOA PRESIDENT', 200, 414, 20, (44, 170, 96)); txt('9 min ago - Sunny Palms', 200, 448, 18, (130, 130, 130))
    txt('SUSPICIOUS MAN', 60, 500, 40, (220, 40, 50)); txt('(WALKING)', 60, 556, 40, (220, 40, 50))
    txt('Ring footage attached. Be advised.', 60, 616, 20, (90, 90, 90))
    # blurry Ring photo
    ph = Image.new('RGB', (900, 340), (150, 200, 240)); pd = ImageDraw.Draw(ph)
    pd.rectangle([0, 190, 900, 340], fill=(90, 160, 80)); pd.rectangle([620, 150, 700, 210], fill=(232, 222, 200)); pd.rectangle([654, 210, 666, 290], fill=(120, 80, 50))
    pd.rectangle([340, 100, 420, 180], fill=(228, 146, 112)); pd.rectangle([310, 90, 350, 190], fill=(238, 208, 110)); pd.rectangle([320, 180, 430, 260], fill=(30, 150, 162))
    pd.rectangle([330, 260, 420, 330], fill=(196, 168, 106)); pd.ellipse([430, 200, 500, 280], fill=(30, 30, 38))
    ph = ph.resize((45, 17), Image.BOX).resize((900, 340), Image.NEAREST)
    im.paste(ph, (90, 660))
    d.rectangle([300, 700, 560, 990 - 40], outline=(238, 60, 60), width=6); d.rectangle([300, 700, 560, 736], fill=(238, 60, 60)); txt('PERSON - WALKING', 310, 710, 16, (255, 255, 255))
    cnt = int(147 * min(1.0, max(0.0, u / 2.7)) ** 1.6)
    txt(f'{cnt} comments', 60, 1010, 24, (60, 60, 60)); txt('Like    Reply', W_ - 60, 1010, 24, (44, 140, 96), 'r')
    for k, (nm, col, l1, l2) in enumerate(NN_COMMENTS):
        t0 = 0.35 + 0.6 * k
        if u < t0: continue
        pop = min(1.0, (u - t0) / 0.18)
        y0 = 1090 + k * 200 + int((1 - pop) * 40)
        d.rounded_rectangle([30, y0, W_ - 30, y0 + 176], 18, fill=(255, 255, 255), outline=(200, 208, 200), width=3)
        d.ellipse([56, y0 + 26, 136, y0 + 106], fill=col)
        txt(nm, 160, y0 + 24, 26, (30, 40, 40)); txt(l1, 160, y0 + 72, 22, (70, 70, 70)); txt(l2, 160, y0 + 110, 22, (70, 70, 70))
    d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], 60, outline=(10, 10, 14), width=26)
    big[:] = np.array(im)


def ring_look(big, t, motion=True):
    """turn a rendered frame into night doorbell-cam footage: IR grade, fisheye, scanlines, noise, HUD"""
    import overlays as O
    H_, W_ = big.shape[:2]
    f = big.astype(np.float32)
    g = f[..., 0] * 0.3 + f[..., 1] * 0.59 + f[..., 2] * 0.11
    g = np.clip((g - 10) * 0.78, 0, 255)
    out = np.stack([g * 0.72, g * 1.0, g * 0.86], -1) + 8
    yy, xx = np.mgrid[0:H_, 0:W_].astype(np.float32)
    nx, ny = (xx - W_ / 2) / (W_ / 2), (yy - H_ / 2) / (H_ / 2)
    r2 = nx * nx + ny * ny
    k = 1 + 0.16 * r2
    sx = np.clip((nx * k * W_ / 2 + W_ / 2).astype(np.int32), 0, W_ - 1); sy = np.clip((ny * k * H_ / 2 + H_ / 2).astype(np.int32), 0, H_ - 1)
    out = out[sy, sx]
    out[::4] *= 0.86
    rng = np.random.default_rng(int(t * 30))
    out += rng.normal(0, 7, out.shape[:2])[..., None]
    out *= (1 - 0.55 * np.clip(r2 - 0.35, 0, 1))[..., None]
    out = np.clip(out, 0, 255).astype(np.uint8)
    im = Image.fromarray(out); d = ImageDraw.Draw(im); d.fontmode = '1'
    def txt(s_, x, y, size, col):
        ff = O.pfont(size); bb = ff.getbbox(s_); d.text((x - bb[0], y - bb[1]), s_, font=ff, fill=col)
    sec = 17 + int(t * 1.0)
    txt(f'03:04:{sec % 60:02d} AM', 50, 190, 32, (230, 255, 230))
    txt('FRONT DOOR', 50, 240, 22, (200, 240, 200))
    if int(t * 2) % 2 == 0:
        d.ellipse([W_ - 190, 190, W_ - 158, 222], fill=(255, 60, 60)); txt('REC', W_ - 140, 192, 30, (255, 255, 255))
    if motion and int(t * 3) % 2 == 0: txt('MOTION DETECTED', 50, H_ - 330, 30, (255, 236, 90))
    big[:] = np.array(im)


def binoculars(L, h, ang=0.0):
    """chunky black binoculars held at hand h (raised to the eyes)"""
    for dx in (-1.35, 1.35):
        cap(L, (h[0] + dx, h[1] + 1.4), (h[0] + dx, h[1] - 1.6), 1.15, 1.0, (34, 34, 42), (80, 80, 96), (16, 16, 22))
        ell(L, (h[0] + dx, h[1] - 1.8), 1.0, 0.7, (110, 140, 210), 0, (190, 210, 250), (60, 80, 140))
    cap(L, (h[0] - 1.35, h[1] - 0.2), (h[0] + 1.35, h[1] - 0.2), 0.5, 0.5, (52, 52, 64))


# ---------------------------------------------------------------- E04: storm props
def lawn_chair(CH, cam, t=0.0):
    """folding aluminium lawn chair with green/white webbing (drawn behind a seated hero, anchor = floor)"""
    L = Layer(cam)
    for x in (-5.4, 4.6):
        cap(L, H(x, 0.0), H(x + (0.6 if x < 0 else -0.6), 9.0), 0.4, 0.4, (200, 204, 214), (240, 244, 250), (140, 144, 158))
    cap(L, H(-5.0, 9.0), H(-6.6, 24.0), 0.4, 0.4, (200, 204, 214), (240, 244, 250), (140, 144, 158))
    for k, h in enumerate(range(0, 7)):                                                   # striped back webbing
        c = (44, 160, 110) if k % 2 == 0 else (240, 240, 236)
        cap(L, H(-5.4 - 0.2 * k, 10.0 + 2.0 * k), H(-3.4 - 0.2 * k, 10.0 + 2.0 * k), 0.85, 0.85, c)
    for k in range(5):                                                                     # seat webbing
        c = (44, 160, 110) if k % 2 == 0 else (240, 240, 236)
        cap(L, H(-4.6 + 2.2 * k, 8.4), H(-3.4 + 2.2 * k, 8.4), 0.5, 0.5, c)
    cap(L, H(-2.0, 12.6), H(4.6, 12.6), 0.5, 0.5, (200, 204, 214))                         # arm rest
    outline(L, OL)
    CH.add(L)


def cooler(CH, cam):
    """blue/white cooler with a beer can on the lid; anchor = floor"""
    L = Layer(cam)
    rect(L, H(0.0, 3.0), 9.0, 6.0, 0, (40, 110, 200))
    rect(L, H(0.0, 6.6), 9.4, 1.4, 0, (250, 250, 252))
    rect(L, H(0.0, 1.0), 9.0, 1.2, 0, (28, 80, 150))
    cap(L, H(-1.8, 8.2), H(1.8, 8.2), 0.4, 0.4, (250, 250, 252))
    koozie_can(L, H(3.2, 8.8))
    outline(L, OL)
    CH.add(L)


def umbrella(CH, cam, hand_x=3.4, hand_h=13.0, top_h=31.0):
    """pastel-mint umbrella held above the hero (canopy + handle), drawn over the hero"""
    L = Layer(cam)
    cap(L, H(hand_x, hand_h), H(1.4, top_h - 1.0), 0.28, 0.28, (170, 176, 190))
    ell(L, H(1.4, top_h), 12.0, 3.6, (120, 226, 190), 0, (190, 250, 224), (70, 168, 136))
    for k in range(-2, 3): cap(L, H(1.4 + k * 4.4, top_h - 1.0), H(1.4 + k * 3.0, top_h + 2.6), 0.14, 0.14, (70, 168, 136))
    cap(L, H(1.4, top_h + 3.0), H(1.4, top_h + 4.2), 0.3, 0.2, (170, 176, 190))
    outline(L, OL)
    CH.add(L)


def weeds(CH, cam):
    """pond weed draped on a soaked head"""
    L = Layer(cam)
    for k, (x0, y0, x1, y1) in enumerate(((-1.4, 25.6, -2.4, 23.0), (-0.2, 26.0, -0.7, 24.2), (1.0, 26.0, 1.7, 24.4), (2.2, 25.4, 3.1, 23.9))):
        cap(L, H(x0, y0), H(x1, y1), 0.34, 0.2, (40, 120, 60), (80, 170, 84), (24, 84, 44))
    ell(L, H(0.8, 25.9), 1.5, 0.5, (52, 140, 70))
    CH.add(L)


def rain(big, t, k=1.0, slant=0.35, n=170, col=(196, 222, 255)):
    """slanted rain streaks over the frame (k = intensity 0..1) + a slight darkening"""
    import overlays as O
    if k <= 0: return
    H_, W_ = big.shape[:2]
    rng = np.random.default_rng(int(t * 30) % 100000)
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i in range(int(n * k)):
        x = rng.uniform(-100, W_ + 300); y = rng.uniform(-150, H_); l = rng.uniform(80, 170)
        d.line([(x, y), (x - l * slant, y + l)], fill=col + (int(rng.uniform(90, 180)),), width=int(rng.integers(2, 5)))
    big[:] = (big.astype(np.float32) * (1 - 0.18 * k)).astype(np.uint8)
    O.overlay(big, np.array(im), 0, 0, 1.0)


def rainbow(big, a=0.30, cx=540, cy=1800, r0=1500, band=42):
    import overlays as O
    H_, W_ = big.shape[:2]
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for i, c in enumerate(((255, 70, 70), (255, 150, 60), (255, 236, 80), (90, 210, 100), (80, 160, 255), (160, 100, 230))):
        r = r0 - i * band
        d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=c + (int(255 * a),), width=band)
    O.overlay(big, np.array(im), 0, 0, 1.0)


# ---------------------------------------------------------------- E05: BBQ props + payment tablet
def hot_dog(L, h, ang=0.0, bun=True, mustard=True):
    cx, cy = h
    if bun:
        cap(L, (cx - 2.4, cy + 0.5), (cx + 2.4, cy + 0.5), 1.05, 1.05, (232, 180, 100), (252, 214, 140), (186, 132, 64))
    cap(L, (cx - 2.7, cy - 0.2), (cx + 2.7, cy - 0.2), 0.8, 0.8, (190, 84, 60), (226, 124, 92), (140, 52, 38))
    if mustard:
        for k in range(6): dot(L, (cx - 2.2 + k * 0.9, cy - 0.8 + 0.25 * (k % 2)), (250, 214, 40), 0.24)


def tongs(L, h, ang=-0.2):
    ca, sa = math.cos(ang), math.sin(ang)
    for s_ in (-1, 1):
        cap(L, (h[0] - ca * 1.5, h[1] - sa * 1.5), (h[0] + ca * 3.6 + s_ * 0.4, h[1] + sa * 3.6 + s_ * 0.7), 0.24, 0.3, (190, 196, 208), (240, 244, 250), (130, 136, 150))


def tablet_ui(big, t, state, u, amp=0.0):
    """full-screen fake payment tablet («TAPPY»): a smiley that talks with the voice envelope + tip / receipt / guilt / review / video screens"""
    import overlays as O
    from PIL import ImageFont
    W_, H_ = 1080, 1920
    im = Image.new('RGB', (W_, H_), (18, 20, 28)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([40, 60, W_ - 40, H_ - 60], 56, fill=(246, 248, 252))
    def txt(s_, cx, cy, size, col, anchor='c', stroke=None):
        f = O.pfont(size); bb = f.getbbox(s_)
        x = cx - (bb[2] - bb[0]) / 2 if anchor == 'c' else (cx if anchor == 'l' else cx - (bb[2] - bb[0]))
        pos = (x - bb[0], cy - (bb[3] - bb[1]) / 2 - bb[1])
        if stroke:
            for dx in (-2, 0, 2):
                for dy in (-2, 0, 2): d.text((pos[0] + dx, pos[1] + dy), s_, font=f, fill=stroke)
        d.text(pos, s_, font=f, fill=col)
    def button(x0, y0, x1, y1, label, right='', fill=(44, 170, 96), col=(255, 255, 255), size=56, border=None, shift=0):
        d.rounded_rectangle([x0 + shift, y0, x1 + shift, y1], 34, fill=fill, outline=border, width=6 if border else 0)
        txt(label, x0 + shift + 50, (y0 + y1) // 2, size, col, 'l')
        if right: txt(right, x1 + shift - 50, (y0 + y1) // 2, int(size * 0.8), col, 'r')
    txt('TAPPY', 140, 130, 34, (44, 170, 96), 'l'); txt('SUNNY PALMS HOA BBQ', W_ - 110, 130, 20, (130, 136, 150), 'r')
    # smiley
    cx, cy, r = 540, 330, 150
    sad = state == 'guilt'
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 214, 74), outline=(40, 40, 50), width=10)
    ex = 0 if state != 'video' else int(6 * math.sin(t * 3))
    for sx in (-1, 1):
        d.ellipse([cx + sx * 56 - 20 + ex, cy - 40 - 20, cx + sx * 56 + 20 + ex, cy - 40 + 20], fill=(30, 30, 40))
        d.ellipse([cx + sx * 56 - 8 + ex, cy - 60, cx + sx * 56 + 4 + ex, cy - 48], fill=(255, 255, 255))
    m = min(1.0, amp * 1.6)
    if sad:
        d.arc([cx - 70, cy + 40, cx + 70, cy + 130], 200, 340, fill=(40, 40, 50), width=12)
        d.polygon([(cx + 84, cy - 10), (cx + 70, cy + 34), (cx + 98, cy + 34)], fill=(110, 180, 255))
        d.line([(cx - 90, cy - 96), (cx - 30, cy - 76)], fill=(40, 40, 50), width=10); d.line([(cx + 90, cy - 96), (cx + 30, cy - 76)], fill=(40, 40, 50), width=10)
        if m > 0.1: d.ellipse([cx - 40, cy + 60, cx + 40, cy + 60 + int(20 + 40 * m)], fill=(120, 30, 40))
    else:
        h_ = int(16 + 64 * m)
        d.chord([cx - 84, cy + 20, cx + 84, cy + 20 + 2 * h_ + 30], 0, 180, fill=(120, 30, 40), outline=(40, 40, 50), width=8)
        d.chord([cx - 60, cy + 34, cx + 60, cy + 34 + 60], 0, 180, fill=(255, 255, 255)) if m > 0.35 else None
    def slide(k, t0=0.0):
        return int((1 - min(1.0, max(0.0, (u - t0 - 0.22 * k) / 0.22))) * 900)
    if state in ('tip', 'video'):
        txt('Add a tip?' if state == 'tip' else 'Tip this video?', 540, 590, 72 if state == 'tip' else 60, (30, 40, 50))
        txt('Your tip supports the HOA president' if state == 'tip' else 'Your tip supports the creator', 540, 668, 22, (130, 136, 150))
        for k, (pc, amt) in enumerate((('20%', '$9.53'), ('25%', '$11.91'), ('30%', '$14.29'))):
            y0 = 760 + k * 190
            press = (state == 'tip' and 2.9 < u < 3.3 and k == 0) or (state == 'video' and 3.8 < u < 4.2 and k == 2)
            button(110, y0, 970, y0 + 150, pc, amt, fill=(24, 130, 70) if press else (44, 170, 96), shift=slide(k))
        button(110, 1330, 970, 1450, 'Custom Tip', '', fill=(255, 255, 255), col=(44, 170, 96), size=44, border=(44, 170, 96), shift=slide(3))
        txt('no tip', 540, 1590, 16, (206, 210, 214))
    elif state == 'receipt':
        txt('YOUR RECEIPT', 540, 590, 56, (30, 40, 50))
        txt('HOT DOG', 130, 690, 34, (30, 40, 50), 'l'); txt('FREE!', 950, 690, 34, (30, 170, 90), 'r')
        items = (('Bun surcharge', '1.50'), ('Condiment tax', '2.15'), ('Convenience fee', '3.99'), ('Plate fee', '2.50'), ('Napkin fee', '2.89'),
                 ('Suggested donation', '15.00'), ('Service fee 18%', '9.60'), ('Tip 20%', '10.00'))
        for k, (a_, b_) in enumerate(items):
            if u < 0.25 + 0.34 * k: continue
            y = 780 + k * 78
            txt(a_, 130, y, 28, (70, 76, 90), 'l'); txt('$' + b_, 950, y, 28, (70, 76, 90), 'r')
            d.line([(130, y + 34), (950, y + 34)], fill=(220, 224, 230), width=3)
        if u > 0.25 + 0.34 * 8:
            txt('TOTAL', 130, 1500, 60, (220, 40, 50), 'l'); txt('$47.63', 950, 1500, 60, (220, 40, 50), 'r')
    elif state == 'guilt':
        txt('Are you sure?', 540, 600, 68, (30, 40, 50))
        txt('Brenda worked really hard.', 540, 690, 30, (90, 100, 140))
        button(110, 800, 970, 950, 'Add tip', '$14.29', shift=slide(0))
        txt('no thanks (Brenda will be notified)', 540, 1120, 16, (206, 210, 214))
    elif state == 'review':
        txt('Rate your visit!', 540, 600, 56, (30, 40, 50))
        for k in range(5):
            cxs, cys = 190 + k * 175, 780
            sc = 1.0 + 0.12 * math.sin(t * 8 + k)
            pts = []
            for i in range(10):
                rr = (70 if i % 2 == 0 else 30) * sc
                a = -math.pi / 2 + i * math.pi / 5
                pts.append((cxs + rr * math.cos(a), cys + rr * math.sin(a)))
            d.polygon(pts, fill=(255, 196, 40), outline=(150, 100, 20))
        txt('Leave a review?', 540, 960, 46, (30, 40, 50))
        button(110, 1060, 970, 1210, '5 STARS', '', shift=slide(0))
        txt('skip', 540, 1330, 16, (206, 210, 214))
    big[:] = np.array(im)


# ---------------------------------------------------------------- E06: election props
def podium_front(CH, cam, w=15.0, h=12.6, flip_mic=False):
    """wooden lectern with a microphone, drawn OVER the lower body of a hero standing behind it; anchor = hero's floor point"""
    L = Layer(cam)
    rect(L, H(1.0, h / 2), w, h, 0, (150, 100, 60))
    rect(L, H(1.0, h - 0.5), w + 1.0, 1.4, 0, (176, 124, 76))
    rect(L, H(1.0, h * 0.5), w - 2.6, h - 3.4, 0, (128, 84, 48))
    ell(L, H(1.0, h * 0.55), 2.2, 1.6, (232, 190, 90), 0, (250, 226, 140), (176, 130, 40))
    cap(L, H(4.6, h), H(5.2, h + 5.6), 0.22, 0.22, (170, 176, 190))
    ell(L, H(5.4, h + 6.2), 0.9, 1.1, (40, 40, 48), 0, (90, 90, 104), (20, 20, 28))
    outline(L, OL)
    CH.add(L)


def ballot_in_mouth(CH, cam, wl=0.0, name='DALE'):
    """Earl's soggy ballot held in his jaws (Earl units: anchor = waterline)"""
    L = Layer(cam)
    rect(L, H(8.2, wl + 3.0), 2.8, 3.6, -0.15, (252, 252, 248))
    rect(L, H(8.2, wl + 3.0), 2.8, 0.7, -0.15, (60, 70, 140))
    ltext(L, name, (8.2, wl + 3.4), 0.55, (40, 40, 60), -0.15)
    for k, (x, h) in enumerate(((7.4, 1.0), (8.0, 0.4), (9.0, 1.2))):
        cap(L, H(x, wl + 1.6), H(x, wl + h - 0.5), 0.2, 0.16, (150, 200, 240))
    outline(L, OL)
    CH.add(L)


def ballot_box(CH, v, x, y, s=1.0):
    """glass ballot box with a slot on a table; centre-bottom at world (x, y)"""
    cam = v.cam(x, y, 8.0 * s)
    L = Layer(cam)
    rect(L, H(0.0, 4.6), 9.0, 9.0, 0, (200, 226, 240))
    rect(L, H(0.0, 4.6), 8.0, 8.0, 0, (226, 240, 250))
    rect(L, H(0.0, 9.4), 9.6, 1.2, 0, (176, 124, 76))
    cap(L, H(-2.0, 9.4), H(2.0, 9.4), 0.25, 0.25, (30, 30, 36))                                   # slot
    rect(L, H(0.0, 0.6), 9.6, 1.2, 0, (150, 100, 60))
    rect(L, H(0.0, 4.4), 5.0, 1.6, 0, (252, 252, 248))
    ltext(L, 'BALLOTS', (0.0, 4.4), 0.62, (60, 70, 140))
    outline(L, OL)
    CH.add(L)


def ballot_paper(CH, v, x, y, s=1.0, ang=0.0):
    L = Layer(v.cam(x, y, 8.0 * s))
    rect(L, H(0.0, 0.0), 3.0, 4.2, ang, (252, 252, 248))
    rect(L, H(0.0, 1.4), 3.0, 0.7, ang, (60, 70, 140))
    outline(L, OL)
    CH.add(L)


def tally_overlay(big, v, brenda, dale, x=560, y=470):
    """chalk-style scoreboard drawn onto the frame at world (x, y)"""
    import overlays as O
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    a, b = v.opt(x - 70, y - 50), v.opt(x + 70, y + 50)
    d.rectangle([a, b], fill=(32, 54, 48, 255), outline=(150, 100, 60, 255), width=10)
    f = O.pfont(int(9 * v.Z * 3))
    for i, (nm, n) in enumerate((('BRENDA', brenda), ('DALE', dale))):
        cx = a[0] + (b[0] - a[0]) * (0.28 + 0.44 * i)
        bb = f.getbbox(nm); d.text((cx - (bb[2] - bb[0]) / 2 - bb[0], a[1] + 24), nm, font=f, fill=(250, 250, 240, 255))
        for k in range(n):
            xx = cx - 10 * v.Z * 3 + k * 8 * v.Z * 3
            d.line([(xx, a[1] + 90 * v.Z), (xx, a[1] + 150 * v.Z)], fill=(250, 250, 240, 255), width=max(3, int(3 * v.Z)))
    O.overlay(big, np.array(im), 0, 0, 1.0)


def crowd_back(CH, v, n=14, y=690.0, x0=60.0, x1=1220.0, u=6.8, t=0.0, cheer=1.0, seed=6):
    """neighbours seen from behind (heads, shoulders, visors, cheering arms) in a row along world y"""
    rng = np.random.default_rng(seed)
    hair = ((238, 208, 110), (200, 200, 208), (110, 74, 48), (36, 30, 34), (226, 226, 230), (196, 96, 60), (240, 236, 220))
    shirt = ((226, 90, 120), (60, 150, 210), (255, 200, 60), (120, 200, 150), (160, 110, 210), (240, 240, 236), (240, 140, 60))
    skin = ((238, 186, 150), (212, 160, 120), (170, 118, 84), (244, 208, 180))
    for i in range(n):
        x = lerp_(x0, x1, (i + 0.5 * (i % 2)) / n) + float(rng.uniform(-14, 14)); yy = y + float(rng.uniform(-10, 24))
        cam = v.cam(x, yy, u * float(rng.uniform(0.9, 1.1)))
        L = Layer(cam)
        b = 0.3 * math.sin(t * 7 + i * 1.7) * cheer
        sc = shirt[int(rng.integers(0, len(shirt)))]
        ell(L, H(0.0, 6.0), 4.6, 5.2, sc, 0, tuple(min(255, c + 30) for c in sc), tuple(int(c * 0.7) for c in sc))
        ell(L, H(0.0, 13.6 + b), 2.5, 2.8, skin[int(rng.integers(0, len(skin)))], 0, None, None)
        hc = hair[int(rng.integers(0, len(hair)))]
        ell(L, H(0.0, 14.6 + b), 2.9, 2.7, hc, 0, tuple(min(255, c + 24) for c in hc), tuple(int(c * 0.75) for c in hc))
        if i % 3 == 0: ell(L, H(0.0, 16.4 + b), 3.4, 0.9, (250, 250, 246), 0, None, (196, 200, 208))                 # sun visor
        for sx in (-1, 1):                                                                                             # cheering arms
            if (i + (sx > 0)) % 2 == 0:
                cap(L, H(sx * 3.8, 9.0), H(sx * 5.0, 17.5 + 2.0 * math.sin(t * 9 + i + sx) * cheer), 0.9, 0.8, sc)
                dot(L, H(sx * 5.0, 18.4 + 2.0 * math.sin(t * 9 + i + sx) * cheer), skin[i % len(skin)], 0.9)
        outline(L, OL)
        CH.add(L)


def lerp_(a, b, k): return a + (b - a) * k
