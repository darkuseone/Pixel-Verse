"""Props and vehicles of «Agent Dibs». World props take (CH, cam) with cam = v.cam(wx, wy, unit) (anchor = floor point, +x = facing,
unit = world px per body unit); hand props take (L, hand) in the holder's unit coords. Vehicles are side views facing +x (flip mirrors),
~30 units long. Everything is outlined; tones are (base, hi, sh)."""
import math
import numpy as np
import scene as S
from scene import Layer
from props.folk import H, cap, ell, ellt, dot, poly, outline, _merge, OL
from props.us_props import ltext, rect
from props.chi_cast import T3


# ====================================================================================================== chairs, bomb, small things
def dibs_chair(CH, cam, sign=True, towel=True, t=0.0, tape=True, wob=0.0, only_sign=False):
    """the sacred dibs chair: aluminium lawn chair, green/white webbing, striped towel on the back, duct tape, cardboard sign.
    only_sign=True draws just the cardboard sign (to put it in front of a hero sitting on the chair)"""
    L = Layer(cam)
    if only_sign:
        _chair_sign(L, sign); outline(L, OL); CH.add(L); return
    fr, frh, frs = T3((196, 202, 212), 0.3)
    for x, sg in ((-5.2, -1), (4.8, 1)):                                      # legs
        cap(L, H(x, 0.0), H(x + 0.5 * sg * -1, 9.0), 0.42, 0.42, fr, frh, frs)
    cap(L, H(-4.6, 9.0), H(-6.8 + wob, 23.0), 0.42, 0.42, fr, frh, frs)       # back post
    for k in range(5):                                                         # back webbing
        c = (44, 160, 110) if k % 2 == 0 else (240, 240, 236)
        cap(L, H(-5.0 - 0.35 * k + wob * k * 0.1, 11.0 + 2.5 * k), H(-3.2 - 0.35 * k + wob * k * 0.1, 11.0 + 2.5 * k), 0.95, 0.95, c)
    for k in range(5):                                                         # seat webbing
        c = (44, 160, 110) if k % 2 == 0 else (240, 240, 236)
        cap(L, H(-4.6 + 2.1 * k, 8.4), H(-3.4 + 2.1 * k, 8.4), 0.55, 0.55, c)
    cap(L, H(-2.0, 12.4), H(4.8, 12.4), 0.5, 0.5, fr, frh, frs)                # arm rest
    cap(L, H(4.8, 12.4), H(4.8, 9.0), 0.4, 0.4, fr, frh, frs)
    if towel:                                                                  # striped towel draped over the chair back
        tw = [(-6.4, 22.5), (-2.4, 22.0), (-2.2, 14.6), (-6.0, 14.8)]
        poly(L, [H(*p) for p in tw], (250, 250, 246))
        for k, c in enumerate(((60, 160, 230), (230, 60, 70), (60, 160, 230))):
            cap(L, H(-6.2, 21.0 - k * 2.2), H(-2.3, 20.8 - k * 2.2), 0.7, 0.7, c)
    if tape:
        cap(L, H(-5.0, 4.0), H(-4.0, 5.2), 0.6, 0.6, (150, 156, 164))
        cap(L, H(4.4, 3.4), H(5.2, 4.6), 0.5, 0.5, (150, 156, 164))
    if sign: _chair_sign(L, sign)
    outline(L, OL)
    CH.add(L)


def _chair_sign(L, sign):
    """cardboard sign taped to the seat front"""
    rect(L, H(0.0, 5.6), 11.4, 5.6, 0.0, (176, 134, 84))
    rect(L, H(0.0, 5.6), 10.8, 5.0, 0.0, (206, 164, 108))
    rows = sign if isinstance(sign, (list, tuple)) else [('DIBS.', 2.0), ('I SHOVELED', 0.95), ('THIS. -STOSH', 0.8)]
    yy = 7.5
    for r, hh in rows:
        ltext(L, r, H(0.0, yy), hh, (40, 30, 20)); yy -= hh * 1.2 + 0.7


def bomb(CH, cam, t=0.0, fuse=1.0, r=3.4):
    """cartoon round bomb with a burning fuse; returns world-less unit position of the spark (for glow)"""
    L = Layer(cam)
    ell(L, H(0.0, r), r, r, (40, 42, 54), 0, (110, 116, 140), (14, 14, 20))
    dot(L, H(-1.2, r + 1.2), (200, 210, 235), 0.35)
    cap(L, H(0.8, 2 * r - 0.2), H(1.4, 2 * r + 0.8), 0.7, 0.6, (120, 124, 136))
    pts = [H(1.4, 2 * r + 0.8), H(2.6, 2 * r + 2.0), H(2.0, 2 * r + 3.2), H(3.4, 2 * r + 4.2)]
    n = max(1, int(round(3 * fuse)))
    for a, b in zip(pts[:n], pts[1:n + 1]): cap(L, a, b, 0.22, 0.2, (200, 170, 110), None, (120, 90, 50))
    sp = pts[min(n, 3)]
    if fuse > 0.02:
        for k in range(6):
            ang = t * 17 + k * 1.05
            dot(L, (sp[0] + 0.7 * math.cos(ang) * (0.6 + 0.4 * math.sin(t * 23 + k)), sp[1] - 0.7 * math.sin(ang)),
                (255, 214, 80) if k % 2 else (255, 130, 40), 0.3)
        dot(L, sp, (255, 250, 200), 0.5)
    outline(L, OL)
    CH.add(L)
    return (sp[0] - 1000.0, 1000.0 - sp[1])


def cone(CH, cam, tip=0.0):
    L = Layer(cam)
    poly(L, [H(-2.6, 0.0), H(2.6, 0.0), H(0.5, 9.6), H(-0.5, 9.6)], (255, 122, 24))
    poly(L, [H(-2.0, 3.6), H(2.0, 3.6), H(1.4, 5.8), H(-1.4, 5.8)], (250, 250, 246))
    rect(L, H(0.0, 0.4), 6.6, 0.8, 0.0, (30, 30, 36))
    outline(L, OL)
    CH.add(L)


def trophy(L, h, s=1.0, ang=0.0):
    """golden parking-sign statuette: blue 'P' plate on a pole and a base (hand prop at h)"""
    cx, cy = h[0], h[1]
    rect(L, cx, cy - 1.0 * s, 4.4 * s, 5.6 * s, ang, (230, 184, 40))
    rect(L, cx, cy - 1.0 * s, 3.6 * s, 4.8 * s, ang, (40, 90, 200))
    ltext(L, 'P', (cx, cy - 1.0 * s), 3.2 * s, (250, 250, 250), ang)
    cap(L, (cx, cy + 1.6 * s), (cx, cy + 4.6 * s), 0.35 * s, 0.35 * s, (230, 184, 40), (255, 230, 120), (170, 126, 20))
    rect(L, cx, cy + 4.8 * s, 4.0 * s, 1.0 * s, 0.0, (230, 184, 40))
    rect(L, cx, cy + 5.6 * s, 5.0 * s, 0.9 * s, 0.0, (150, 104, 30))


def briefcase(L, h, ang=0.0, s=1.0):
    cx, cy = h[0] + 1.0 * s, h[1] + 2.0 * s
    cap(L, (cx - 1.4 * s, cy - 2.6 * s), (cx + 1.4 * s, cy - 2.6 * s), 0.5 * s, 0.5 * s, (50, 36, 30))
    rect(L, cx, cy, 7.2 * s, 5.0 * s, ang, (70, 50, 40))
    rect(L, cx, cy, 6.6 * s, 4.4 * s, ang, (96, 70, 54))
    rect(L, cx, cy - 0.2 * s, 6.6 * s, 0.4 * s, ang, (60, 44, 34))
    for dx in (-2.0, 2.0): rect(L, cx + dx * s, cy - 0.2 * s, 0.9 * s, 1.0 * s, ang, (220, 200, 120))


def cuff(L, h, s=1.0):
    """oversize steel handcuff ring around the wrist at h (the joke: it could always slip off)"""
    ell(L, h, 1.9 * s, 1.9 * s, (160, 168, 182), 0, (226, 232, 242), (100, 106, 120))
    ell(L, h, 1.2 * s, 1.2 * s, (40, 40, 50))
    cap(L, (h[0], h[1] + 1.6 * s), (h[0] + 0.8 * s, h[1] + 3.4 * s), 0.3 * s, 0.3 * s, (150, 156, 170))


def thermos(L, h, cup=True):
    cx, cy = h[0] + 0.3, h[1] + 1.4
    cap(L, (cx, cy - 2.8), (cx, cy + 2.4), 1.15, 1.15, (46, 140, 110), (100, 200, 170), (24, 90, 70))
    ell(L, (cx, cy - 3.3), 1.2, 0.6, (240, 240, 240), 0, None, (190, 190, 190))
    cap(L, (cx - 1.0, cy - 0.2), (cx + 1.0, cy - 0.2), 0.28, 0.28, (230, 230, 236))


def coffee_cup(L, h):
    cx, cy = h[0] + 0.3, h[1] - 0.2
    poly(L, [(cx - 1.1, cy - 1.4), (cx + 1.1, cy - 1.4), (cx + 0.8, cy + 1.2), (cx - 0.8, cy + 1.2)], (250, 250, 246))
    rect(L, cx, cy - 0.1, 2.2, 1.0, 0.0, (150, 96, 60))
    ell(L, (cx, cy - 1.4), 1.1, 0.35, (92, 56, 36))


def ketchup(L, h, ang=0.0, squeeze=0.0, col=((214, 28, 36), (255, 90, 90), (140, 10, 20)), cap_col=(250, 250, 246)):
    """squeeze bottle held at h; nozzle points along ang (0 = +x)"""
    ca, sa = math.cos(ang), math.sin(ang)
    c = (h[0] + ca * 0.8, h[1] + sa * 0.8)
    cap(L, (c[0] - ca * 1.2, c[1] - sa * 1.2), (c[0] + ca * 3.4, c[1] + sa * 3.4), 1.25, 0.95, *col)
    cap(L, (c[0] + ca * 3.4, c[1] + sa * 3.4), (c[0] + ca * 4.4, c[1] + sa * 4.4), 0.8, 0.45, cap_col, None, (190, 190, 190))
    dot(L, (c[0] + ca * 4.8, c[1] + sa * 4.8), col[0], 0.28)
    if squeeze > 0:
        for k in range(4):
            d = 5.4 + k * 1.3 * squeeze
            dot(L, (c[0] + ca * d, c[1] + sa * d + 0.18 * k * k), col[0], 0.42)


def hat_in_hand(L, h):
    """black beanie clutched at h (sorry!)"""
    ell(L, (h[0], h[1] - 0.8), 2.0, 1.5, (26, 26, 32), 0, (66, 66, 80), (12, 12, 16))
    ell(L, (h[0], h[1] + 0.2), 2.2, 0.6, (50, 50, 60))


def rolling_pin(L, h, ang=-0.6):
    ca, sa = math.cos(ang), math.sin(ang)
    cap(L, (h[0] - ca * 2.6, h[1] - sa * 2.6), (h[0] + ca * 3.4, h[1] + sa * 3.4), 0.8, 0.8, (214, 168, 108), (240, 206, 150), (158, 112, 64))
    for s_ in (-1, 1): cap(L, (h[0] + s_ * ca * 4.2, h[1] + s_ * sa * 4.2), (h[0] + s_ * ca * 5.0, h[1] + s_ * sa * 5.0), 0.45, 0.45, (170, 120, 70))


def frying_pan(L, h, ang=-0.5):
    ca, sa = math.cos(ang), math.sin(ang)
    cap(L, h, (h[0] + ca * 3.4, h[1] + sa * 3.4), 0.4, 0.4, (60, 50, 44))
    ell(L, (h[0] + ca * 5.8, h[1] + sa * 5.8), 2.6, 2.6, (46, 48, 56), 0, (110, 114, 130), (22, 22, 28))
    ell(L, (h[0] + ca * 5.8, h[1] + sa * 5.8), 1.9, 1.9, (30, 30, 36))


def casserole(L, h):
    cx, cy = h[0] + 0.6, h[1] - 1.2
    rect(L, cx, cy, 6.4, 2.4, 0.0, (236, 236, 244))
    rect(L, cx, cy - 0.6, 5.8, 1.2, 0.0, (214, 150, 70))
    for k in range(4): dot(L, (cx - 2.2 + k * 1.5, cy - 0.7), (240, 200, 90), 0.35)
    rect(L, cx, cy + 1.0, 6.6, 0.6, 0.0, (176, 180, 196))
    ell(L, (h[0] + 0.2, h[1] + 0.1), 1.3, 1.1, (230, 70, 60))                                            # oven mitt


def mop(L, h, ang=-1.2):
    ca, sa = math.cos(ang), math.sin(ang)
    cap(L, (h[0] - ca * 4.0, h[1] - sa * 4.0), (h[0] + ca * 5.0, h[1] + sa * 5.0), 0.3, 0.3, (170, 130, 80))
    for k in range(5):
        cap(L, (h[0] + ca * 5.0 + (k - 2) * 0.4, h[1] + sa * 5.0), (h[0] + ca * 7.2 + (k - 2) * 0.7, h[1] + sa * 7.2 + 0.5), 0.4, 0.5, (240, 240, 232))


def giant_scissors(L, h, open_=0.4):
    for s_ in (-1, 1):
        cap(L, (h[0] - 0.4, h[1]), (h[0] + 5.6, h[1] + s_ * open_ * 2.4), 0.5, 0.2, (210, 214, 226), (250, 252, 255), (140, 146, 160))
        cap(L, (h[0] - 0.4, h[1]), (h[0] - 2.4, h[1] - s_ * 1.4), 0.7, 0.7, (214, 50, 56))
        ell(L, (h[0] - 2.8, h[1] - s_ * 1.7), 0.9, 0.9, (214, 50, 56))


def phone_old(L, h):
    """flip phone"""
    cap(L, (h[0], h[1] + 0.6), (h[0] + 0.5, h[1] - 1.4), 0.8, 0.8, (60, 64, 76), (110, 116, 134), (30, 32, 40))
    cap(L, (h[0] + 0.5, h[1] - 1.4), (h[0] + 1.2, h[1] - 3.0), 0.8, 0.7, (60, 64, 76), (110, 116, 134), (30, 32, 40))
    dot(L, (h[0] + 1.0, h[1] - 2.4), (140, 230, 150), 0.3)


def chicago_dog(CH, cam, t=0.0, s=1.0, bite=0.0):
    """big hero-prop Chicago dog on a paper tray: poppy-seed bun, sausage, neon relish, tomatoes, pickle spear, sport peppers, onions, mustard.
    bite = 0..1 eaten from the +x end"""
    L = Layer(cam)
    rect(L, H(0.0, -0.4), 17.0 * s, 1.6 * s, 0.0, (250, 250, 246))                                   # paper tray
    rect(L, H(0.0, -0.4), 17.0 * s, 0.5 * s, 0.0, (214, 40, 50))
    cap(L, H(-7.0 * s, 1.8 * s), H(7.0 * s, 1.8 * s), 2.6 * s, 2.6 * s, (222, 170, 94), (250, 214, 140), (170, 118, 54))      # bun
    for k in range(10): dot(L, H(-6.0 * s + k * 1.3 * s, 3.9 * s + 0.2 * (k % 2)), (250, 244, 214), 0.28 * s)                # poppy seeds
    cap(L, H(-7.6 * s, 3.4 * s), H(7.6 * s, 3.4 * s), 1.5 * s, 1.5 * s, (178, 78, 56), (226, 124, 92), (130, 46, 34))       # sausage
    cap(L, H(-6.8 * s, 4.6 * s), H(6.8 * s, 4.6 * s), 1.1 * s, 1.1 * s, (120, 255, 60), None, (60, 190, 30))                # neon relish
    for k in range(7):
        dot(L, H(-6.0 * s + k * 2.0 * s, 5.6 * s + 0.2 * (k % 2)), (255, 255, 250), 0.34 * s)                                  # white onion bits
    for x in (-3.4, 2.8): ell(L, H(x * s, 5.9 * s), 1.5 * s, 0.7 * s, (230, 60, 50), 0, (255, 110, 100), (170, 30, 26))      # tomato slices
    cap(L, H(-7.8 * s, 6.0 * s), H(7.8 * s, 6.5 * s), 0.8 * s, 0.8 * s, (96, 150, 60), (150, 210, 100), (50, 100, 30))       # pickle spear
    for x in (-5.0, 4.6): cap(L, H(x * s, 6.4 * s), H(x * s + 2.2 * s, 6.8 * s), 0.55 * s, 0.4 * s, (110, 170, 60))          # sport peppers
    for k in range(8): dot(L, H(-6.4 * s + k * 1.8 * s, 6.9 * s - 0.15 * (k % 2)), (255, 222, 40), 0.3 * s)                 # mustard zigzag
    for k in range(10): dot(L, H(-6.0 * s + k * 1.3 * s + 0.4 * (k % 3), 7.4 * s - 0.4 * (k % 2)), (250, 250, 236), 0.12 * s)    # celery salt
    if bite > 0.01:                                                                                  # big bite taken out of the +x end
        xc = cam.p(1000.0 + (8.4 - 16.8 * bite) * s, 1000.0)[0]
        yy_, xx_ = np.mgrid[0:L.m.shape[0], 0:L.m.shape[1]]
        rr = 3.2 * s * cam.sc
        for k in range(3):
            cy_ = cam.p(1000.0, 1000.0 - (1.8 + 2.2 * k) * s)[1]
            cxx = xc + (rr * 0.5 if not cam.flip else -rr * 0.5)
            L.m[(xx_ - cxx) ** 2 + (yy_ - cy_) ** 2 < rr * rr] = False
        if cam.flip: L.m[:, :int(xc)] = False
        else: L.m[:, int(xc) + int(rr * 0.5):] = False
    outline(L, OL)
    CH.add(L)


def fries(CH, cam, s=1.0):
    L = Layer(cam)
    for k in range(9):
        x = -4.4 + k * 1.1
        cap(L, H(x * s, 2.2 * s), H((x + 0.35 * (k % 3 - 1)) * s, (6.4 + 1.2 * (k % 4)) * s), 0.55 * s, 0.5 * s, (250, 206, 84), (255, 232, 140), (214, 160, 40))
    poly(L, [H(-5.4 * s, 0.0), H(5.4 * s, 0.0), H(4.6 * s, 3.4 * s), H(-4.6 * s, 3.4 * s)], (222, 50, 56))
    rect(L, H(0.0, 1.6 * s), 7.0 * s, 1.0 * s, 0.0, (250, 250, 246))
    outline(L, OL)
    CH.add(L)


# ====================================================================================================== vehicles
def _wheel(L, x, h, r=3.2, rot=0.0):
    ell(L, H(x, h), r, r, (28, 28, 34), 0, (70, 70, 84), None)
    ell(L, H(x, h), r * 0.58, r * 0.58, (176, 182, 196), 0, (230, 234, 244), (110, 116, 130))
    for k in range(5):
        a = rot + k * 1.2566
        cap(L, H(x, h), H(x + math.cos(a) * r * 0.55, h + math.sin(a) * r * 0.55), 0.18, 0.18, (90, 96, 110))
    dot(L, H(x, h), (60, 64, 76), 0.4)


def peek_head(L, x, h, kind='dibs', s=1.0, look=1.0):
    """tiny driver head seen through a car window"""
    if kind == 'dibs':
        ell(L, H(x, h), 1.9 * s, 2.0 * s, (226, 150, 120))
        ell(L, H(x, h + 1.4 * s), 2.2 * s, 1.3 * s, (120, 104, 92), 0, (160, 144, 128), (80, 68, 60))
        dot(L, H(x + 1.6 * s * look, h - 0.1 * s), (222, 96, 90), 0.5 * s)
        cap(L, H(x + 0.6 * s * look, h - 0.9 * s), H(x + 2.2 * s * look, h - 0.9 * s), 0.35 * s, 0.35 * s, (78, 58, 44))
        dot(L, H(x + 0.6 * s * look, h + 0.4 * s), (24, 20, 22), 0.3 * s); dot(L, H(x + 1.6 * s * look, h + 0.4 * s), (24, 20, 22), 0.3 * s)
    else:
        sk = (240, 204, 180) if kind == 'terry' else (224, 172, 134)
        ell(L, H(x, h), 1.9 * s, 2.0 * s, sk)
        ell(L, H(x, h + 1.3 * s), 2.1 * s, 1.5 * s, (26, 26, 32))
        dot(L, H(x + 0.5 * s * look, h + 0.2 * s), (24, 20, 22), 0.3 * s); dot(L, H(x + 1.5 * s * look, h + 0.2 * s), (24, 20, 22), 0.3 * s)


def sedan(CH, cam, t=0.0, body=(214, 196, 150), drivers=(('dibs', 3.0),), rot=0.0, shake=0.0, signal=False, text='BUREAU', lights=True,
          tilt=0.0, plume=False):
    """rusty 1990s sedan facing +x, ~30 units long. drivers: [(kind, x_offset_from_centre)] heads seen through the windows"""
    L = Layer(cam)
    sh = shake * math.sin(t * 40)
    b = T3(body, 0.28)
    # shadow-ish body
    ellt(L, H(0.0, 5.0 + sh), 15.2, 3.4, b)
    poly(L, [H(-14.6, 4.0 + sh), H(14.8, 4.0 + sh), H(15.0, 6.6 + sh), H(-14.8, 7.0 + sh)], b[0])
    poly(L, [H(-8.4, 7.4 + sh), H(-5.6, 12.6 + sh), H(5.8, 12.6 + sh), H(9.2, 7.4 + sh)], b[0])                    # cabin
    poly(L, [H(-7.4, 7.6 + sh), H(-5.2, 11.8 + sh), H(5.2, 11.8 + sh), H(8.2, 7.6 + sh)], (40, 56, 76))             # windows
    for (kind, dx) in drivers: peek_head(L, dx, 9.6 + sh, kind, 1.0)
    cap(L, H(0.4, 7.6 + sh), H(0.4, 11.8 + sh), 0.35, 0.35, b[2])                                                   # B pillar
    poly(L, [H(-7.4, 7.6 + sh), H(-6.6, 8.4 + sh), H(-3.0, 8.2 + sh), H(-4.0, 7.6 + sh)], (200, 220, 240)) if False else None
    cap(L, H(-14.0, 3.6 + sh), H(14.6, 3.6 + sh), 0.7, 0.7, (150, 150, 160))                                         # bumpers
    cap(L, H(-14.8, 4.4 + sh), H(-14.8, 6.4 + sh), 0.5, 0.5, (150, 150, 160))
    # rust, door line, marker text
    for (x, h, r) in ((-9.0, 4.4, 0.9), (-5.0, 3.9, 0.7), (11.0, 5.2, 0.8), (3.0, 6.4, 0.6)): ell(L, H(x, h + sh), r, r * 0.6, (150, 92, 54))
    cap(L, H(-1.2, 4.2 + sh), H(-1.2, 7.4 + sh), 0.18, 0.18, b[2])
    if text: ltext(L, text, H(-4.8, 5.4 + sh), 1.2, (40, 40, 60))
    if lights:
        ell(L, H(14.6, 5.4 + sh), 1.1, 0.9, (255, 244, 170)); ell(L, H(-14.6, 5.6 + sh), 0.8, 0.9, (214, 40, 40))
        if signal and int(t * 3) % 2 == 0: ell(L, H(14.4, 4.2 + sh), 0.7, 0.6, (255, 170, 30)); ell(L, H(-14.4, 4.4 + sh), 0.7, 0.6, (255, 170, 30))
    _wheel(L, -9.4, 3.2 + sh, 3.2, rot); _wheel(L, 9.4, 3.2 + sh, 3.2, rot)
    outline(L, OL)
    CH.add(L)


def suv(CH, cam, t=0.0, rot=0.0, shake=0.0, drivers=(), lights=True, doors=0.0, signal=False, antenna=0.0):
    """black SUV facing +x, ~32 units long, tinted windows; signal = blinking orange blinkers, antenna = rear aerial length (units)"""
    L = Layer(cam)
    sh = shake * math.sin(t * 40)
    if antenna > 0:
        cap(L, H(-13.0, 14.0 + sh), H(-13.4, 14.0 + antenna + sh), 0.14, 0.14, (70, 70, 80))
        dot(L, H(-13.4, 14.2 + antenna + sh), (230, 60, 60), 0.4)
    b = T3((30, 32, 42), 0.28)
    poly(L, [H(-15.6, 3.6 + sh), H(15.8, 3.6 + sh), H(16.0, 7.4 + sh), H(-15.8, 8.0 + sh)], b[0])
    poly(L, [H(-15.4, 8.0 + sh), H(-14.0, 14.2 + sh), H(8.0, 14.4 + sh), H(12.6, 8.4 + sh)], b[0])
    poly(L, [H(-13.6, 8.4 + sh), H(-12.8, 13.2 + sh), H(7.2, 13.4 + sh), H(11.2, 8.4 + sh)], (60, 78, 104))
    for (kind, dx) in drivers: peek_head(L, dx, 10.6 + sh, kind, 1.0)
    for x in (-5.0, 1.6): cap(L, H(x, 8.4 + sh), H(x, 13.4 + sh), 0.3, 0.3, b[2])
    cap(L, H(-4.0, 7.0 + sh), H(4.0, 7.0 + sh), 0.3, 0.3, b[2])
    ell(L, H(15.2, 6.2 + sh), 0.9, 1.4, (200, 204, 216), 0, (250, 252, 255), (130, 136, 150))                         # chrome grille
    if lights:
        ell(L, H(15.8, 7.4 + sh), 1.2, 0.9, (255, 246, 190)); ell(L, H(-15.6, 7.0 + sh), 0.8, 1.2, (230, 40, 40))
    cap(L, H(-15.4, 3.6 + sh), H(15.6, 3.6 + sh), 0.7, 0.7, (130, 132, 142))
    if signal and int(t * 3) % 2 == 0:
        ell(L, H(15.9, 5.2 + sh), 0.7, 0.6, (255, 170, 30)); ell(L, H(-15.8, 5.6 + sh), 0.8, 0.7, (255, 170, 30))
    _wheel(L, -9.8, 3.4 + sh, 3.5, rot); _wheel(L, 10.0, 3.4 + sh, 3.5, rot)
    outline(L, OL)
    CH.add(L)


def minivan(CH, cam, t=0.0, rot=0.0, shake=0.0, driver=True, door=0.0, blinker=False, sticker=True):
    """silver minivan facing +x (Brad's): sloped hood, sliding side door, stickers"""
    L = Layer(cam)
    sh = shake * math.sin(t * 40)
    b = T3((206, 212, 224), 0.22)
    poly(L, [H(-15.4, 3.6 + sh), H(15.2, 3.6 + sh), H(15.4, 6.6 + sh), H(12.0, 9.4 + sh), H(-15.4, 9.6 + sh)], b[0])
    poly(L, [H(-15.2, 9.4 + sh), H(-14.4, 14.8 + sh), H(7.6, 14.8 + sh), H(12.0, 9.6 + sh)], b[0])                  # tall cabin
    poly(L, [H(-13.8, 9.8 + sh), H(-13.2, 14.0 + sh), H(7.0, 14.0 + sh), H(10.6, 9.8 + sh)], (74, 96, 126))
    if driver:
        ell(L, H(5.4, 11.8 + sh), 1.7, 1.9, (244, 208, 178)); ell(L, H(5.2, 13.0 + sh), 1.8, 1.0, (92, 62, 40))
        dot(L, H(6.0, 12.0 + sh), (30, 30, 36), 0.3)
        cap(L, H(5.0, 9.8 + sh), H(7.0, 10.6 + sh), 0.5, 0.5, (240, 242, 246))                                  # arms on the wheel at 10 and 2
    cap(L, H(-3.6, 9.8 + sh), H(-3.6, 14.0 + sh), 0.3, 0.3, b[2]); cap(L, H(-12.0, 9.8 + sh), H(-12.0, 14.0 + sh), 0.3, 0.3, b[2])
    rect(L, H(-8.0 + door * 3.0, 6.4 + sh), 10.0, 5.6, 0.0, b[1]) if False else None
    cap(L, H(-12.4, 4.2 + sh), H(-12.4, 9.4 + sh), 0.2, 0.2, b[2]); cap(L, H(-2.6, 4.2 + sh), H(-2.6, 9.4 + sh), 0.2, 0.2, b[2])   # sliding door seams
    cap(L, H(-12.4, 8.6 + sh), H(-2.6, 8.6 + sh), 0.18, 0.18, b[2]); cap(L, H(-3.4, 6.6 + sh), H(-3.0, 6.6 + sh), 0.3, 0.3, (120, 124, 136))
    cap(L, H(-15.4, 3.6 + sh), H(15.4, 3.6 + sh), 0.7, 0.7, (130, 132, 142))
    if sticker:
        rect(L, H(-14.4, 6.2 + sh), 1.4, 2.0, 0.0, (250, 250, 250)); ltext(L, '26.2', H(-14.4, 6.2 + sh), 0.5, (40, 40, 60))
    ell(L, H(15.0, 6.4 + sh), 1.0, 1.0, (255, 246, 190)); ell(L, H(-15.2, 7.4 + sh), 0.7, 1.4, (214, 40, 40))
    if blinker and int(t * 3) % 2 == 0: ell(L, H(15.2, 4.6 + sh), 0.7, 0.6, (255, 170, 30))
    cap(L, H(-13.0, 15.4 + sh), H(6.0, 15.4 + sh), 0.35, 0.35, (150, 154, 168))                                      # roof rack
    _wheel(L, -9.8, 3.4 + sh, 3.3, rot); _wheel(L, 9.6, 3.4 + sh, 3.3, rot)
    outline(L, OL)
    CH.add(L)


def taxi(CH, cam, t=0.0, rot=0.0, shake=0.0, driver=True, arm_out=False):
    """yellow cab facing +x with a roof light and a checker stripe"""
    L = Layer(cam)
    sh = shake * math.sin(t * 40)
    b = T3((252, 206, 24), 0.28)
    poly(L, [H(-15.4, 3.8 + sh), H(15.6, 3.8 + sh), H(15.8, 6.8 + sh), H(-15.6, 7.2 + sh)], b[0])
    poly(L, [H(-8.8, 7.4 + sh), H(-6.2, 12.6 + sh), H(5.6, 12.6 + sh), H(9.4, 7.4 + sh)], b[0])
    poly(L, [H(-7.8, 7.8 + sh), H(-5.6, 11.8 + sh), H(5.0, 11.8 + sh), H(8.4, 7.8 + sh)], (50, 66, 86))
    if driver:
        ell(L, H(4.4, 9.8 + sh), 1.8, 1.9, (210, 160, 130)); ell(L, H(4.3, 11.0 + sh), 2.0, 1.1, (20, 20, 26))
        dot(L, H(5.2, 10.0 + sh), (24, 20, 22), 0.3)
    if arm_out:
        cap(L, H(5.6, 8.4 + sh), H(9.2, 9.2 + sh), 0.8, 0.7, (210, 160, 130)); ell(L, H(9.8, 9.2 + sh), 0.8, 0.7, (210, 160, 130))
    for k in range(10):                                                                                               # checker stripe
        rect(L, H(-13.4 + k * 3.0, 5.2 + sh), 1.5, 0.9, 0.0, (20, 20, 26) if k % 2 == 0 else (250, 250, 246))
    rect(L, H(0.0, 13.4 + sh), 5.0, 1.5, 0.0, (250, 250, 240))
    ltext(L, 'TAXI', H(0.0, 13.4 + sh), 1.0, (30, 30, 40))
    cap(L, H(-15.2, 3.8 + sh), H(15.4, 3.8 + sh), 0.7, 0.7, (150, 150, 160))
    ell(L, H(15.4, 5.6 + sh), 1.1, 0.9, (255, 246, 190)); ell(L, H(-15.4, 5.8 + sh), 0.8, 0.9, (214, 40, 40))
    _wheel(L, -9.4, 3.2 + sh, 3.2, rot); _wheel(L, 9.4, 3.2 + sh, 3.2, rot)
    outline(L, OL)
    CH.add(L)


def city_truck(CH, cam, t=0.0, rot=0.0):
    """orange street-crew pickup with an amber beacon and «STREETS» on the door"""
    L = Layer(cam)
    b = T3((246, 134, 32), 0.28)
    poly(L, [H(-15.0, 3.8), H(15.0, 3.8), H(15.2, 7.0), H(-15.0, 7.4)], b[0])
    poly(L, [H(2.0, 7.4), H(4.4, 13.0), H(12.0, 13.0), H(13.6, 7.4)], b[0])
    poly(L, [H(3.4, 7.8), H(5.0, 12.0), H(11.0, 12.0), H(12.4, 7.8)], (60, 80, 104))
    rect(L, H(-7.0, 8.0), 14.0, 1.4, 0.0, b[2])                                                                       # truck bed rail
    ltext(L, 'STREETS', H(8.0, 5.4), 1.1, (30, 30, 40))
    cap(L, H(7.4, 13.4), H(10.0, 13.4), 0.5, 0.5, (60, 60, 70))
    ell(L, H(8.7, 14.2), 1.0, 0.8, (255, 190, 30) if int(t * 4) % 2 == 0 else (150, 100, 20))
    cap(L, H(-15.0, 3.8), H(15.2, 3.8), 0.7, 0.7, (150, 150, 160))
    ell(L, H(15.0, 5.6), 1.0, 0.9, (255, 246, 190)); ell(L, H(-15.0, 6.0), 0.8, 0.9, (214, 40, 40))
    _wheel(L, -8.6, 3.2, 3.3, rot); _wheel(L, 9.4, 3.2, 3.3, rot)
    outline(L, OL)
    CH.add(L)


def squad_truck(CH, cam, t=0.0, rot=0.0):
    """white bomb-squad box truck with a blue stripe"""
    L = Layer(cam)
    b = T3((240, 242, 248), 0.12)
    poly(L, [H(-16.0, 3.8), H(16.0, 3.8), H(16.0, 7.2), H(-16.0, 7.6)], b[0])
    rect(L, H(-3.6, 12.0), 22.0, 9.6, 0.0, b[0])
    poly(L, [H(8.4, 7.4), H(9.6, 13.4), H(14.4, 13.4), H(16.0, 7.4)], b[0])
    poly(L, [H(9.6, 8.0), H(10.4, 12.6), H(13.8, 12.6), H(15.0, 8.0)], (70, 96, 130))
    rect(L, H(-3.6, 9.6), 22.0, 1.2, 0.0, (40, 90, 200))
    ltext(L, 'BOMB SQUAD', H(-3.6, 12.2), 1.6, (30, 50, 120))
    ell(L, H(10.4, 14.0), 1.1, 0.8, (255, 50, 50) if int(t * 5) % 2 == 0 else (60, 120, 255))
    ell(L, H(15.8, 5.6), 1.0, 0.9, (255, 246, 190))
    cap(L, H(-16.0, 3.8), H(16.0, 3.8), 0.7, 0.7, (150, 150, 160))
    _wheel(L, -9.6, 3.2, 3.3, rot); _wheel(L, 10.4, 3.2, 3.3, rot)
    outline(L, OL)
    CH.add(L)


def robot(CH, cam, t=0.0, sad=0.0, back=0.0):
    """bomb-disposal robot on tracks: camera head, gripper arm; sad = head droops, back = reverse jitter"""
    L = Layer(cam)
    ell(L, H(0.0, 2.2), 5.6, 2.2, (60, 64, 76), 0, (110, 116, 134), (30, 32, 40))                                     # tracks
    for k in range(4): dot(L, H(-3.6 + k * 2.4, 2.0), (30, 32, 40), 0.8)
    rect(L, H(0.0, 5.2), 7.0, 3.2, 0.0, (220, 190, 40))
    rect(L, H(0.0, 5.2), 6.2, 2.4, 0.0, (240, 214, 70))
    cap(L, H(1.0, 6.6), H(2.4, 9.2 - 1.6 * sad), 0.6, 0.6, (90, 94, 108))                                              # neck
    ell(L, H(3.0, 10.0 - 2.0 * sad), 1.8, 1.4, (50, 54, 66), 0, (100, 106, 124), (24, 26, 34))
    dot(L, H(4.0, 10.0 - 2.0 * sad), (255, 80, 80) if sad < 0.5 else (120, 160, 255), 0.7)                             # eye
    cap(L, H(-1.0, 6.4), H(-3.2, 8.6), 0.6, 0.5, (90, 94, 108)); cap(L, H(-3.2, 8.6), H(-5.6, 7.0), 0.5, 0.4, (90, 94, 108))   # claw arm
    if sad > 0.3:
        ell(L, H(3.4, 8.4 - 2.0 * sad), 0.3, 0.7, (170, 220, 255), 0, (230, 246, 255), None)                         # tear
    outline(L, OL)
    CH.add(L)


def tank(CH, cam, t=0.0, droop=0.0, rot=0.0, hatch=True, salute=0.0):
    """small cartoon tank facing +x; droop = barrel tips down (respect), hatch with a commander"""
    L = Layer(cam)
    o = T3((106, 122, 66), 0.28)
    ell(L, H(0.0, 3.4), 14.4, 3.2, (50, 54, 46), 0, (90, 96, 82), (28, 30, 26))                                        # tracks
    for k in range(7): ell(L, H(-10.0 + k * 3.3, 3.2), 1.5, 1.5, (36, 38, 34), 0, (84, 90, 78), None)
    poly(L, [H(-13.0, 5.0), H(13.0, 5.0), H(11.0, 9.0), H(-11.0, 9.0)], o[0])
    ell(L, H(0.0, 11.0), 6.6, 3.4, o[0], 0, o[1], o[2])                                                                 # turret
    ang = 0.0 + 0.5 * droop
    cap(L, H(5.0, 11.2), H(18.0, 11.2 - 7.0 * math.sin(ang) * 1.0 - 0.2), 0.9, 0.8, o[0], o[1], o[2])                  # barrel
    ell(L, H(18.4, 10.6 - 3.0 * droop), 1.0, 0.9, (40, 42, 36))
    if hatch:
        ell(L, H(-1.8, 13.6), 2.0, 0.8, o[2])
        ell(L, H(-1.8, 15.4), 1.6, 1.8, (230, 180, 150))
        ell(L, H(-1.8, 16.8), 1.9, 1.1, (70, 82, 40), 0, (110, 126, 70), (40, 50, 24))                                 # helmet
        dot(L, H(-1.0, 15.6), (24, 20, 22), 0.3)
        if salute > 0:
            cap(L, H(-0.6, 13.6), H(0.4, 16.4), 0.5, 0.5, (70, 82, 40)); dot(L, H(0.4, 16.8), (230, 180, 150), 0.5)
    cap(L, H(-6.0, 14.0), H(-6.0, 18.0), 0.14, 0.14, (60, 60, 60))                                                      # antenna
    outline(L, OL)
    CH.add(L)


# ====================================================================================================== crowd and windows
def puffer_person(CH, cam, col=(30, 30, 38), hat=(200, 60, 60), t=0.0, phase=0.0, look=0.0, hands_up=0.0, scarf=None, face=True, hat_on=True):
    """generic winter pedestrian seen from the side/3-4: puffer coat, beanie, hands near the mouth"""
    L = Layer(cam)
    b = math.sin(t * 3 + phase) * 0.15
    P = T3(col, 0.26)
    ellt(L, H(0.0, 7.0), 5.0, 6.4, P)
    for k in range(3): cap(L, H(-4.0, 5.0 + k * 2.4), H(4.0, 5.0 + k * 2.4), 0.14, 0.14, P[2])
    cap(L, H(-2.0, 1.0), H(-2.0, 0.0), 1.6, 1.4, (30, 30, 36)); cap(L, H(2.0, 1.0), H(2.0, 0.0), 1.6, 1.4, (30, 30, 36))
    ell(L, H(0.8, 14.4 + b), 2.9, 3.0, (236, 196, 166), 0, (252, 224, 196), (190, 140, 112))
    if hat_on:
        ell(L, H(0.6, 16.6 + b), 3.2, 2.0, hat, 0, tuple(min(255, c + 40) for c in hat), tuple(int(c * 0.65) for c in hat))
        dot(L, H(0.6, 19.0 + b), tuple(min(255, c + 60) for c in hat), 0.9)
    else:                                                                                              # helmet clutched in the hand
        ell(L, H(4.8, 10.0), 2.2, 1.6, hat, 0, tuple(min(255, c + 40) for c in hat), tuple(int(c * 0.65) for c in hat))
        ell(L, H(0.8, 17.0 + b), 2.6, 1.3, (40, 30, 26))
    if face:
        for dx in (-0.4, 1.8):
            ell(L, H(1.0 + dx, 14.8 + b), 0.62, 0.7, (250, 248, 244)); dot(L, H(1.2 + dx + 0.2 * look, 14.8 + b), (24, 20, 22), 0.3)
    if scarf: cap(L, H(-1.6, 11.4), H(3.0, 11.2), 1.0, 1.0, scarf)
    h = hands_up
    cap(L, H(3.0, 9.0), H(4.4 + 0.2 * h, 12.0 + 3.0 * h), 1.1, 1.0, *P)
    ell(L, H(4.6 + 0.2 * h, 12.8 + 3.2 * h), 0.9, 0.9, (250, 230, 200))
    outline(L, OL)
    CH.add(L)


def sky_poles(big, v, t):
    """no-op placeholder to keep imports symmetrical"""
    return big


def knit(L, h, t=0.0):
    """two knitting needles + a pink scarf-in-progress held at h (Deb)"""
    sw = 0.3 * math.sin(t * 6.0)
    cap(L, (h[0] - 1.2, h[1] + 1.4 + sw), (h[0] + 3.4, h[1] - 3.0 - sw), 0.2, 0.2, (210, 214, 224), (250, 252, 255), (130, 136, 150))
    cap(L, (h[0] + 1.2, h[1] + 1.8 - sw), (h[0] - 3.0, h[1] - 2.8 + sw), 0.2, 0.2, (210, 214, 224), (250, 252, 255), (130, 136, 150))
    ell(L, (h[0] + 0.4, h[1] + 1.8), 2.6, 1.7, (255, 140, 190), 0, (255, 190, 220), (214, 90, 140))
    for k in range(4): cap(L, (h[0] - 1.6 + k * 1.1, h[1] + 1.0), (h[0] - 1.6 + k * 1.1, h[1] + 2.6), 0.14, 0.14, (214, 90, 140))
    dot(L, (h[0] + 4.0, h[1] + 3.6), (255, 120, 170), 1.0)                                              # yarn ball


def cue_card(L, h, ang=0.0, lines=('LINE:', "THAT'S OUR BOMB")):
    """tiny index card with a line of dialogue (Terry reading his part off his hand)"""
    cx, cy = h[0] + 0.4, h[1] - 1.2
    rect(L, cx, cy, 6.2, 3.4, ang, (252, 252, 246))
    rect(L, cx, cy - 1.3, 6.2, 0.5, ang, (214, 50, 56))
    for i, r in enumerate(lines): ltext(L, r, (cx, cy - 0.3 + i * 1.1), min(0.8, 5.6 / max(6, len(r)) * 1.4), (40, 40, 60), ang)


def smoke_puff(big, cx, cy, r, a, col=(40, 38, 42)):
    """soot-grey puff on the output frame"""
    from props.bytfx import puff
    puff(big, cx, cy, r, a, col)


# ====================================================================================================== E02 hand props
def shovel(L, h, ang=-1.25):
    """snow shovel (red blade, wooden handle with a D-grip), held at h; ang = handle direction (0 = +x)"""
    ca, sa = math.cos(ang), math.sin(ang)
    cap(L, (h[0] - ca * 3.2, h[1] - sa * 3.2), (h[0] + ca * 7.6, h[1] + sa * 7.6), 0.3, 0.3, (176, 134, 84), (214, 176, 116), (112, 80, 44))
    cap(L, (h[0] - ca * 3.2 - sa * 0.9, h[1] - sa * 3.2 + ca * 0.9), (h[0] - ca * 3.2 + sa * 0.9, h[1] - sa * 3.2 - ca * 0.9), 0.3, 0.3, (112, 80, 44))
    bx, by = h[0] + ca * 9.4, h[1] + sa * 9.4
    rect(L, bx, by, 3.4, 5.2, ang, (226, 56, 50))
    rect(L, bx - ca * 0.4, by - sa * 0.4, 2.6, 4.4, ang, (250, 96, 84))


def sandwich(L, h, bites=0, t=0.0):
    """big sub sandwich (bun, lettuce, tomato, cheese), `bites` chunks missing from the +x end"""
    cx, cy = h[0] + 1.2, h[1] - 0.2
    e = 3.4 - 0.7 * bites
    cap(L, (cx - 3.4, cy + 0.9), (cx + e, cy + 0.9), 0.95, 0.95, (222, 170, 94), (250, 214, 140), (170, 118, 54))
    cap(L, (cx - 3.5, cy + 0.2), (cx + e + 0.1, cy + 0.2), 0.45, 0.45, (120, 220, 80))
    cap(L, (cx - 3.3, cy - 0.15), (cx + e, cy - 0.15), 0.4, 0.4, (230, 80, 70))
    cap(L, (cx - 3.3, cy - 0.45), (cx + e - 0.2, cy - 0.45), 0.35, 0.35, (250, 206, 90))
    cap(L, (cx - 3.4, cy - 1.0), (cx + e, cy - 1.0), 0.85, 0.85, (222, 170, 94), (250, 214, 140), (170, 118, 54))


def guard_badge(L):
    """yellow SECURITY plate pinned on the chest (Gary at the lobby desk)"""
    rect(L, H(2.9, 12.2), 6.6, 1.7, 0.0, (36, 36, 44))
    rect(L, H(2.9, 12.2), 6.2, 1.3, 0.0, (250, 214, 60))
    ltext(L, 'SECURITY', H(2.9, 12.2), 0.62, (36, 36, 44))


def phone_ad(L, h, t=0.0):
    """smartphone showing the mattress ad (Terry walks off to watch it)"""
    rect(L, h[0] + 0.6, h[1] - 0.4, 2.6, 4.4, 0.0, (22, 22, 28))
    rect(L, h[0] + 0.6, h[1] - 0.4, 2.1, 3.9, 0.0, (60, 70, 150))
    rect(L, h[0] + 0.6, h[1] + 0.6, 1.7, 0.9, 0.0, (236, 120, 150))
    dot(L, (h[0] + 0.6, h[1] - 1.6), (255, 240, 170), 0.35)


# ====================================================================================================== E03 props
def sign_board(CH, cam, lines, w=24.0, col=(250, 214, 60), tcol=(30, 30, 40), pole=14.0):
    """street sign on a pole; lines = [(text, height_units), ...]"""
    L = Layer(cam)
    hh = 2.6 + sum(sz * 1.35 + 0.5 for _, sz in lines)
    cap(L, H(0.0, 0.0), H(0.0, pole), 0.5, 0.5, (96, 98, 110))
    rect(L, H(0.0, pole + hh / 2), w + 1.2, hh + 1.2, 0.0, (28, 28, 34))
    rect(L, H(0.0, pole + hh / 2), w, hh, 0.0, col)
    y = pole + hh - 1.8
    for r, sz in lines:
        ltext(L, r, H(0.0, y), sz, tcol); y -= sz * 1.35 + 0.5
    outline(L, OL)
    CH.add(L)


def headset(L):
    """call-centre headset over the head of a character whose head centre is H(0.9, 21.3)"""
    c = (40, 44, 58)
    cap(L, H(-0.9, 22.4), H(-0.5, 24.8), 0.3, 0.3, c)
    cap(L, H(-0.5, 24.8), H(2.8, 25.1), 0.3, 0.3, c)
    cap(L, H(2.8, 25.1), H(3.5, 23.6), 0.3, 0.3, c)
    ell(L, H(-0.85, 21.0), 1.0, 1.35, c, 0, (90, 96, 118), (20, 22, 30))
    cap(L, H(-0.6, 20.0), H(3.0, 18.5), 0.15, 0.15, (30, 30, 38))
    dot(L, H(3.2, 18.4), (46, 46, 56), 0.5)


def beard(L, k, col=(116, 92, 70)):
    """growing beard (k = 0..1) under the chin of Dibs (head centre H(0.9, 21.3))"""
    if k <= 0.02: return
    hi, sh = tuple(min(255, int(x * 1.3)) for x in col), tuple(int(x * 0.7) for x in col)
    ell(L, H(1.5, 19.4 - 2.4 * k), 1.3 + 2.0 * k, 0.9 + 3.6 * k, col, 0, hi, sh)
    cap(L, H(-0.2, 19.8), H(2.9, 19.6), 0.5 + 0.35 * k, 0.5 + 0.2 * k, col)


def cards(L, h):
    """fan of three playing cards held at h"""
    for k, a in enumerate((-0.35, 0.0, 0.35)):
        rect(L, h[0] + 0.8 + (k - 1) * 0.9, h[1] - 1.8, 2.0, 3.0, a, (252, 252, 248))
        dot(L, (h[0] + 0.8 + (k - 1) * 0.9, h[1] - 1.8), (214, 40, 50) if k != 1 else (30, 30, 40), 0.45)


def mustard(L, h, ang=0.0):
    """yellow mustard squeeze bottle used as a sniper rifle (with a scope), held at h"""
    ca, sa = math.cos(ang), math.sin(ang)
    c = (h[0] + ca * 1.0, h[1] + sa * 1.0)
    cap(L, (c[0] - ca * 3.0, c[1] - sa * 3.0), (c[0] + ca * 3.2, c[1] + sa * 3.2), 1.25, 0.95, (255, 214, 28), (255, 240, 120), (200, 150, 10))
    cap(L, (c[0] + ca * 3.2, c[1] + sa * 3.2), (c[0] + ca * 6.4, c[1] + sa * 6.4), 0.35, 0.3, (255, 214, 28), None, (200, 150, 10))
    cap(L, (c[0] + ca * 0.2, c[1] + sa * 0.2 - 1.6), (c[0] + ca * 2.6, c[1] + sa * 2.6 - 1.6), 0.5, 0.5, (40, 44, 56), (90, 96, 116), (20, 22, 30))
    dot(L, (c[0] + ca * 2.9, c[1] + sa * 2.9 - 1.6), (120, 220, 255), 0.5)


def counter_sign(CH, cam, lines, w=22.0, col=(250, 244, 226), tcol=(190, 30, 40)):
    """hand-painted sign leaning on the counter; lines = [(text, height_units)]"""
    L = Layer(cam)
    hh = 1.8 + sum(sz * 1.35 + 0.4 for _, sz in lines)
    rect(L, H(0.0, hh / 2), w + 1.0, hh + 1.0, 0.0, (36, 28, 24))
    rect(L, H(0.0, hh / 2), w, hh, 0.0, col)
    y = hh - 1.2
    for r, sz in lines:
        ltext(L, r, H(0.0, y), sz, tcol); y -= sz * 1.35 + 0.4
    outline(L, OL)
    CH.add(L)
