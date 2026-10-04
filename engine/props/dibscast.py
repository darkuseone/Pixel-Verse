"""Agent Dibs (v2) cast — pixel-puppet heroes drawn with props/dibspix.py.
Each hero has his own silhouette and face build (unique to this series):
  Dibs   — square block head, walrus moustache, bulb nose, ushanka with a gold BSB badge, barrel navy puffer over a tux collar
  Terry  — long and thin, egg head, long pointy nose, eye-bags, pencil moustache, CDS-mask beanie
  Gary   — short and round, moon face, double chin, button nose, rosy cheeks, CDS-mask beanie
  Brad   — V torso, glossy side part, square jaw, megawatt grin, teal fleece vest + lanyard
  Deb    — round face, grey perm cloud, big pink glasses, mustard cardigan, headset
  ladies — Mrs. Wozniak (headscarf, curlers, wrinkles), Rose, Dot
  Marty  — grey rat in a tweed flat cap and a striped scarf
Every draw function: f(sp, pose='stand', t=0, mouth=0, expr='normal', look=0, blink=None, hands=None, props=None, ...)"""
import math
import numpy as np
from props.dibspix import (Spr, EXPR, ik, eye, brow, mouth, stubble, blush, text3, ramp, dark, mix, dilate, erode,
                           XC, YC, CHECK, OUTLINE, WHITE)

LASH = (34, 22, 32)


def _blink(t, blink):
    if blink is not None: return blink
    return 3.28 < (t % 3.4) < 3.39


# ======================================================================================== shared body parts
def glove(sp, x, y, r, pal, ang=0.0, fist=True):
    sp.ell(x, y, r, r * 0.92, pal)
    tx, ty = x + math.cos(ang + 1.2) * r * 0.85, y + math.sin(ang + 1.2) * r * 0.85
    sp.ell(tx, ty, r * 0.42, r * 0.42, pal)
    if fist:
        for k in range(3):
            sp.dot(int(math.floor(x + math.cos(ang) * r * 0.55 - 1 + k)), int(math.floor(y + math.sin(ang) * r * 0.55)), dark(pal[1], 0.9))


def arm(sp, sh, target, l1, l2, r1, r2, pal, bend, glv, hr, cuff=None, quilt=False):
    k, w = ik(sh, target, l1, l2, bend)
    sp.cap(sh, k, r1, r1 * 0.94, pal)
    sp.cap(k, w, r1 * 0.94, r2, pal)
    if quilt:                                                                   # puffer segments
        for a, b, r in ((sh, k, r1), (k, w, r2)):
            mx, my = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            dx, dy = b[0] - a[0], b[1] - a[1]; L = math.hypot(dx, dy) + 1e-6
            px_, py_ = -dy / L, dx / L
            sp.line((mx - px_ * r * 0.8, my - py_ * r * 0.8), (mx + px_ * r * 0.8, my + py_ * r * 0.8), pal[0])
    ang = math.atan2(w[1] - k[1], w[0] - k[0])
    hx, hy = w[0] + math.cos(ang) * hr * 0.9, w[1] + math.sin(ang) * hr * 0.9
    if cuff is not None:
        sp.cap((w[0] - math.cos(ang) * 1.5, w[1] - math.sin(ang) * 1.5), (w[0] + math.cos(ang) * 0.5, w[1] + math.sin(ang) * 0.5), r2 + 0.4, r2 + 0.4, cuff)
    glove(sp, hx, hy, hr, glv, ang)
    return (hx, hy), ang


def leg(sp, hip, knee, ankle, r, pants, boot, boot_len=9.0, boot_h=5.5, sole=(60, 58, 64)):
    sp.cap(hip, knee, r, r * 0.95, pants)
    sp.cap(knee, (ankle[0], ankle[1] + 2), r * 0.95, r * 0.9, pants)
    bx, by = ankle
    m = sp.m_poly([(bx - boot_len * 0.45, by + boot_h), (bx + boot_len * 0.35, by + boot_h), (bx + boot_len * 0.75, by + boot_h * 0.45),
                   (bx + boot_len * 0.75, by), (bx - boot_len * 0.5, by)])
    sp.paint(m, boot, None)
    sp.paint(m & (YC < by + 1.6), [dark(sole, 0.7), sole, mix(sole, (255, 255, 255), 0.25), mix(sole, (255, 255, 255), 0.5)], None)


def legs_for(pose, hipL, hipR, ll, sit=False, step=0.0):
    """knee/ankle positions for both legs"""
    if sit or pose.get('sit'):
        kL = (hipL[0] + ll * 0.95, hipL[1] - 1); aL = (kL[0] + 1.5, 1.0)
        kR = (hipR[0] + ll * 0.95, hipR[1] - 2); aR = (kR[0] + 1.5, 0.5)
        return (kL, aL), (kR, aR)
    sL = pose.get('stepL', 0.0) + step; sR = pose.get('stepR', 0.0) - step
    aL = (hipL[0] - 1 + sL * ll * 0.5, max(0.0, sL * 2.0))
    aR = (hipR[0] + 1 + sR * ll * 0.5, max(0.0, -sR * 2.0) + pose.get('liftR', 0.0))
    kL = ((hipL[0] + aL[0]) / 2 + 0.8, (hipL[1] + aL[1]) / 2 + 0.6)
    kR = ((hipR[0] + aR[0]) / 2 + 1.0 + pose.get('liftR', 0.0) * 0.6, (hipR[1] + aR[1]) / 2 + pose.get('liftR', 0.0) * 0.4)
    return (kL, aL), (kR, aR)


def hand_targets(pose, G):
    """pose -> hand targets (sprite px); pose may carry blend=(other_name, k) to move the hands between two poses"""
    if 'blend' in pose:
        nb, k = pose['blend']
        a = _hand_targets(dict(pose, blend=None, name=pose.get('name', 'stand')), G)
        b = _hand_targets(dict(pose, blend=None, name=nb), G)
        lp = lambda p_, q_: (p_[0] + (q_[0] - p_[0]) * k, p_[1] + (q_[1] - p_[1]) * k)
        return lp(a[0], b[0]), lp(a[1], b[1]), (b if k > 0.5 else a)[2], (b if k > 0.5 else a)[3]
    return _hand_targets(pose, G)


def blend(a, b, k):
    """arm pose between named poses a and b (k = 0..1)"""
    return P_(a, blend=(b, max(0.0, min(1.0, k))))


def _hand_targets(pose, G):
    """pose -> hand targets (sprite px) from the rig geometry G (shL, shR, head, hip, belly, rx = torso half width)"""
    shL, shR, hd, hip, rx = G['shL'], G['shR'], G['head'], G['hip'], G['rx']
    G.setdefault('swing', pose.get('swing', 0.0))
    L, R = G['arm'], G['arm']
    p = pose.get('name', 'stand')
    if p == 'stand':   tl, tr, bl, br = (shL[0] - 4, shL[1] - L * 0.9), (shR[0] + 4, shR[1] - L * 0.9), -1, 1
    elif p == 'hips':  tl, tr, bl, br = (-rx + 1, hip + 7), (rx - 1, hip + 7), 1, -1
    elif p == 'reach': tl, tr, bl, br = (shL[0] - 4, shL[1] - L * 0.9), (shR[0] + L * 0.95, shR[1] - 6), -1, 1
    elif p == 'point': tl, tr, bl, br = (shL[0] - 4, shL[1] - L * 0.9), (shR[0] + L * 0.98, shR[1] + 3), -1, -1
    elif p == 'shout': tl, tr, bl, br = (shL[0] - 7, shL[1] + L * 0.85), (shR[0] + 7, shR[1] + L * 0.85), -1, 1
    elif p == 'arms_up': tl, tr, bl, br = (shL[0] - 9, shL[1] + L * 0.9), (shR[0] + 12, shR[1] + L * 0.9), -1, 1
    elif p == 'hold':  tl, tr, bl, br = (shR[0] + 4, shR[1] - L * 0.45), (shR[0] + L * 0.55, shR[1] - L * 0.35), 1, 1
    elif p == 'hat':   tl, tr, bl, br = (2, hip + 10), (rx * 0.5, hip + 9), 1, 1
    elif p == 'ears':  tl, tr, bl, br = (hd[0] - G['hrx'] - 1, hd[1] - 1), (hd[0] + G['hrx'] * 0.75, hd[1] - 1), 1, -1
    elif p == 'cover': tl, tr, bl, br = (hd[0] + G['hrx'] * 0.2, hd[1] - G['hry'] * 0.55), (hd[0] + G['hrx'] * 0.55, hd[1] - G['hry'] * 0.5), 1, 1
    elif p == 'shrug': tl, tr, bl, br = (shL[0] - 10, shL[1] + 2), (shR[0] + 10, shR[1] + 2), 1, -1
    elif p == 'sit':   tl, tr, bl, br = (shR[0] - 2, hip + 2), (shR[0] + L * 0.5, hip + 4), 1, 1
    elif p == 'wave':  tl, tr, bl, br = (shL[0] - 4, shL[1] - L * 0.9), (shR[0] + 8, shR[1] + L * 0.8), -1, 1
    elif p == 'phone': tl, tr, bl, br = (shL[0] - 4, shL[1] - L * 0.9), (hd[0] - G['hrx'] * 0.7, hd[1] - 2), -1, -1
    elif p == 'sip':   tl, tr, bl, br = (shL[0] - 4, shL[1] - L * 0.9), (hd[0] + G['hrx'] * 0.6, hd[1] - G['hry'] * 0.75), -1, -1
    elif p == 'tiptoe': tl, tr, bl, br = (shL[0] + 6, shL[1] - L * 0.15), (shR[0] + L * 0.55, shR[1] - L * 0.1), 1, 1
    elif p == 'pinch': tl, tr, bl, br = (hd[0] + G['hrx'] * 0.9, hd[1] - G['hry'] * 0.2), (hd[0] + G['hrx'] * 1.5, hd[1] - G['hry'] * 0.1), 1, 1
    elif p == 'leap':  tl, tr, bl, br = (shL[0] + L * 0.5, shL[1] + L * 0.55), (shR[0] + L * 0.8, shR[1] + L * 0.5), -1, 1
    elif p == 'gun':   tl, tr, bl, br = (shR[0] + L * 0.55, shR[1] - L * 0.05), (shR[0] + L * 0.9, shR[1] + L * 0.05), 1, 1
    elif p == 'wheel': tl, tr, bl, br = (shR[0] + L * 0.55, shR[1] - L * 0.25), (shR[0] + L * 0.75, shR[1] - L * 0.15), 1, 1
    elif p == 'run':   tl, tr, bl, br = (shL[0] + G['swing'] * L * 0.5, shL[1] - L * 0.6), (shR[0] - G['swing'] * L * 0.5, shR[1] - L * 0.6), -1, 1
    elif p == 'tears': tl, tr, bl, br = (hd[0] - G['hrx'] * 0.3, hd[1] - G['hry'] * 0.2), (hd[0] + G['hrx'] * 0.9, hd[1] - G['hry'] * 0.1), 1, 1
    else:              tl, tr, bl, br = (shL[0] - 4, shL[1] - L * 0.9), (shR[0] + 4, shR[1] - L * 0.9), -1, 1
    return tl, tr, bl, br


def P_(name, **kw):
    d = dict(name=name); d.update(kw); return d


def walk(name, t, speed=4.2, amp=0.55, lift=0.6):
    """walk/tiptoe/run cycle on top of a named arm pose"""
    s_ = math.sin(t * speed)
    return P_(name, stepL=amp * s_ + 0.15, stepR=-amp * s_ + 0.15, liftR=lift * 4 * max(0.0, -s_), swing=s_)


POSE = {n: P_(n) for n in ('stand', 'hips', 'reach', 'point', 'shout', 'arms_up', 'hold', 'hat', 'ears', 'cover', 'shrug', 'wave', 'phone', 'sip',
                           'tiptoe', 'pinch', 'leap', 'gun', 'wheel', 'run', 'tears')}
POSE['sit'] = P_('sit', sit=True)
POSE['frozen'] = P_('tiptoe', liftR=7.0, stepR=0.5)
POSE['leap'] = P_('leap', stepL=0.8, stepR=-0.5, liftR=5.0)


# ======================================================================================== hand props (drawn at the hand)
def p_coffee(sp, h, ang, t=0.0):
    x, y = h
    m = sp.m_poly([(x - 3, y + 5), (x + 3, y + 5), (x + 2.4, y - 3), (x - 2.4, y - 3)])
    sp.paint(m, [(170, 160, 150), (214, 206, 196), (244, 240, 232), (255, 255, 252)], None)
    sp.rect(x - 2, y - 1, x + 3, y + 2, (150, 92, 56))
    sp.rect(x - 3, y + 5, x + 4, y + 7, (60, 56, 64))
    for k in range(3):
        sp.dot(x - 1 + k + int(1.5 * math.sin(t * 3 + k)), y + 8 + k * 2 + int(2 * ((t * 1.5 + k * 0.33) % 1.0)), (230, 236, 246))


def p_card(sp, h, ang, t=0.0, lines=('LINE:', "THAT'S", 'OUR BOMB')):
    """big cue card held up (Terry reads his line)"""
    x, y = h[0] - 2, h[1] - 3
    w = 4 * max(len(l) for l in lines) + 3; hh = 6 * len(lines) + 4
    sp.rect(x - 1, y - 1, x + w + 1, y + hh + 1, (40, 30, 30))
    sp.rect(x, y, x + w, y + hh, (252, 250, 240))
    sp.rect(x, y + hh - 2, x + w, y + hh, (214, 50, 60))
    for k, l in enumerate(lines): text3(sp, l, x + 2, y + hh - 4 - 6 * k, (214, 50, 60) if k == 0 else (30, 34, 60), keep=True)


def p_beanie(sp, h, ang, t=0.0):
    x, y = h
    sp.ell(x + 1, y - 1, 5.5, 3.6, ramp((40, 40, 50)))
    sp.rect(x - 4, y - 4, x + 6, y - 2, (30, 30, 38))
    sp.ell(x + 1, y + 0.5, 1.6, 1.4, [(170, 170, 176), (210, 210, 214), (240, 240, 242), (255, 255, 255)], ol=False)


def p_binoculars(sp, h, ang, t=0.0):
    x, y = h
    for dx in (-3, 3):
        sp.cap((x + dx, y - 2), (x + dx, y + 4), 2.6, 2.4, [(14, 14, 18), (30, 30, 38), (52, 52, 64), (90, 90, 110)])
        sp.ell(x + dx, y + 4.5, 2.2, 1.2, [(60, 80, 120), (90, 120, 170), (130, 170, 220), (200, 230, 255)], ol=False)
    sp.rect(x - 1, y, x + 2, y + 3, (40, 40, 48))


def p_popcorn(sp, h, ang, t=0.0):
    x, y = h
    m = sp.m_poly([(x - 5, y + 4), (x + 5, y + 4), (x + 4, y - 6), (x - 4, y - 6)])
    sp.paint(m, [(160, 160, 160), (220, 220, 220), (250, 250, 248), (255, 255, 255)], None)
    for k in range(-4, 5, 3): sp.fill(m & (np.abs(XC - (x + k + 0.5)) < 0.9), (214, 40, 50))
    for k in range(6):
        sp.ell(x - 4 + k * 1.6, y + 5.5 + (k % 2), 1.5, 1.3, [(200, 160, 80), (240, 210, 130), (255, 240, 190), (255, 252, 230)], ol=False)


def p_knit(sp, h, ang, t=0.0):
    x, y = h
    sw = int(round(1.2 * math.sin(t * 6)))
    sp.line((x - 6, y - 3 + sw), (x + 8, y + 7 - sw), (200, 206, 220), 1)
    sp.line((x - 5, y + 6 - sw), (x + 9, y - 2 + sw), (200, 206, 220), 1)
    sp.ell(x + 1, y + 1, 5, 3, ramp((236, 110, 160)))
    for k in range(4): sp.dot(x - 2 + k * 2, y + 1, (180, 60, 110))
    sp.ell(x + 10, y - 3, 2.6, 2.6, ramp((240, 120, 170)))


def p_phone(sp, h, ang, t=0.0):
    x, y = h
    sp.rect(x - 2, y - 3, x + 3, y + 6, (40, 42, 52))
    sp.rect(x - 1, y + 2, x + 2, y + 5, (130, 220, 150))
    sp.dot(x, y - 2, (90, 94, 108))


def p_shovel(sp, h, ang, t=0.0, a=-0.75):
    """snow shovel held like a gun: wooden handle with a D-grip, red plastic blade (a = handle direction, 0 = forward)"""
    ca, sa = math.cos(a), math.sin(a)
    x, y = h
    wood = [(110, 74, 40), (150, 106, 60), (190, 144, 88), (226, 186, 124)]
    sp.cap((x - ca * 7, y - sa * 7), (x + ca * 24, y + sa * 24), 1.7, 1.7, wood)
    sp.cap((x - ca * 7 - sa * 3, y - sa * 7 + ca * 3), (x - ca * 7 + sa * 3, y - sa * 7 - ca * 3), 1.5, 1.5, wood)
    bx, by = x + ca * 30, y + sa * 30
    blade = sp.m_poly([(bx - sa * 9 - ca * 5, by + ca * 9 - sa * 5), (bx + sa * 9 - ca * 5, by - ca * 9 - sa * 5),
                       (bx + sa * 10 + ca * 8, by - ca * 10 + sa * 8), (bx - sa * 10 + ca * 8, by + ca * 10 + sa * 8)])
    sp.paint(blade, [(130, 24, 30), (190, 40, 44), (232, 70, 62), (255, 130, 110)], np.clip(0.75 - (XC - bx) * 0.03, 0, 1))
    sp.line((bx - sa * 6 + ca * 5, by + ca * 6 + sa * 5), (bx + sa * 6 + ca * 5, by - ca * 6 + sa * 5), (236, 242, 252))


def p_sandwich(sp, h, ang, t=0.0, bites=0):
    """big sub: bun, lettuce, tomato, cheese; `bites` chunks gone from the front end"""
    x, y = h[0] + 2, h[1] + 1
    e = 13 - 3 * bites
    bun = [(150, 96, 40), (204, 146, 70), (236, 186, 104), (252, 222, 150)]
    sp.cap((x - 8, y - 2.2), (x + e, y - 2.2), 2.4, 2.4, bun)
    sp.rect(x - 9, y - 0.8, x + e + 1, y + 0.4, (110, 210, 80)); sp.rect(x - 8, y + 0.2, x + e, y + 1.2, (220, 70, 64))
    sp.rect(x - 8, y + 1.0, x + e - 1, y + 1.8, (250, 206, 90))
    sp.cap((x - 8, y + 3.2), (x + e, y + 3.2), 2.6, 2.6, bun)
    for k in range(3): sp.dot(x - 5 + k * 4, y + 5, (255, 240, 200))
    if bites:
        for k in range(bites): sp.ell(x + e + 1.5, y + 1.0 - 2.4 + k * 2.4, 1.6, 1.4, [(0, 0, 0)] * 4, ol=False)
        sp.m[(XC > x + e + 0.5) & (np.abs(YC - (y + 1)) < 6) & (np.abs(XC - (x + e + 1.5)) < 2.5)] = False


def p_phone_ad(sp, h, ang, t=0.0):
    """smartphone playing the mattress ad"""
    x, y = h
    sp.rect(x - 3, y - 4, x + 4, y + 9, (22, 22, 28))
    sp.rect(x - 2, y - 3, x + 3, y + 8, (60, 70, 150))
    sp.rect(x - 2, y + 1, x + 3, y + 4, (236, 120, 150))
    sp.dot(x, y + 6, (255, 240, 170)); sp.dot(x + 1, y + 6, (255, 240, 170))


PROPS = dict(coffee=p_coffee, card=p_card, beanie=p_beanie, binoculars=p_binoculars, popcorn=p_popcorn, knit=p_knit, phone=p_phone,
             shovel=p_shovel, sandwich=p_sandwich, phone_ad=p_phone_ad)


def _prop(sp, which, h, ang, t):
    if which is None: return
    if callable(which): which(sp, h, ang, t); return
    PROPS[which](sp, h, ang, t)


# ======================================================================================== DIBS
D_SKIN = [(150, 74, 70), (196, 110, 92), (228, 150, 120), (248, 190, 158)]
D_NOSE = [(160, 52, 64), (206, 82, 88), (236, 118, 116), (255, 168, 156)]
D_JACKET = [(16, 18, 38), (28, 36, 70), (44, 58, 104), (72, 92, 148)]
D_PANTS = [(28, 28, 36), (44, 46, 58), (62, 66, 82), (90, 96, 118)]
D_BOOT = [(60, 38, 28), (96, 62, 42), (128, 88, 58), (166, 122, 84)]
D_GLOVE = [(14, 14, 18), (30, 30, 36), (48, 48, 58), (76, 76, 90)]
D_FUR = [(72, 50, 36), (108, 78, 56), (142, 108, 78), (180, 146, 108)]
D_FURL = [(128, 104, 80), (170, 142, 110), (204, 180, 146), (232, 214, 186)]
D_STACHE = [(56, 36, 28), (84, 58, 42), (112, 82, 58), (146, 112, 80)]


def dibs(sp, pose='stand', t=0.0, mouth_=0.0, expr='normal', look=0.0, blink=None, shades=False, hands=None, props=None,
         soot=0.0, sweat=0.0, flap=0.0, legs=True, clip_h=None, breath=True, beard=0.0):
    pose = POSE[pose] if isinstance(pose, str) else pose
    X = EXPR.get(expr, EXPR['normal'])
    br = (0.6 * math.sin(t * 2.2)) if breath else 0.0
    hipy = 22.0
    hipL, hipR = (-8.0, hipy), (7.0, hipy)
    G = dict(shL=(-18.0, 53.0 + br), shR=(15.0, 53.0 + br), head=(3.0, 82.0 + br), hip=hipy, rx=21.0, arm=26.0, hrx=17.0, hry=16.5)
    tl, tr, bl, bR = hand_targets(pose, G)
    if hands:
        tl = hands.get('L', tl); tr = hands.get('R', tr)
    props = props or {}
    # back arm
    hl, al = arm(sp, G['shL'], tl, 14, 13, 5.4, 4.8, D_JACKET, bl, D_GLOVE, 3.8, cuff=D_JACKET[1:] + [D_JACKET[3]], quilt=True)
    _prop(sp, props.get('L'), hl, al, t)
    # legs
    if legs:
        (kL, aL), (kR, aR) = legs_for(pose, hipL, hipR, 25.0 if pose.get('sit') else 11.0)
        leg(sp, hipL, kL, aL, 6.4, D_PANTS, D_BOOT, 11, 7)
        leg(sp, hipR, kR, aR, 6.4, D_PANTS, D_BOOT, 11, 7)
        for a in (aL, aR):                                                       # snow on the boot toes
            sp.rect(a[0] - 2, a[1] + 6, a[0] + 4, a[1] + 7, (236, 242, 252))
    # torso: barrel puffer over a tux
    tm = sp.sup(1.0, 39.0 + br * 0.5, 21.5, 20.5, D_JACKET, n=2.3)
    for k in range(5):                                                           # quilting
        yq = 25 + k * 6.2 + br * 0.5
        sp.fill(tm & erode(erode(tm)) & (np.abs(YC - (yq + 0.012 * XC * XC)) < 0.5), D_JACKET[0])
    sp.fill(tm & (YC < 21.0) & (YC > 18.0), D_JACKET[1])                          # hem band
    sp.fill(tm & (np.abs(XC - 4.5) < 0.6) & (YC < 56), (150, 156, 178))            # zipper
    sp.rect(4, 42, 6, 45, (200, 206, 222))
    sp.cap((-10, 57.5 + br), (17, 57.5 + br), 3.4, 3.4, D_JACKET)                    # puffer collar
    collar = sp.m_poly([(-1, 62 + br), (9, 62 + br), (4, 55 + br)])
    sp.paint(collar, [(170, 170, 176), (214, 214, 220), (244, 244, 246), (255, 255, 255)], None)
    sp.stamp(['##.##', '#####', '##.##'], 2, 60 + int(br), {'#': (200, 30, 44)})       # red bow tie (the tux under the puffer)
    sp.dot(4, 59 + int(br), (120, 14, 24))
    text3(sp, 'BSB', -13, 50 + int(br), (255, 150, 40))
    # head: square block with heavy jowls
    hx, hy = G['head']
    face = sp.union([sp.m_super(hx, hy, 17.5, 16.0, 2.8), sp.m_super(hx + 2.5, hy - 9.5, 17.0, 10.5, 2.2)], D_SKIN)
    sp.ell(hx - 16.0, hy + 0.5, 3.4, 4.6, D_SKIN)                                    # ear
    sp.dot(hx - 16, hy + 0, D_SKIN[0]); sp.dot(hx - 16, hy + 1, D_SKIN[0]); sp.dot(hx - 15, hy - 1, D_SKIN[1])
    stubble(sp, face & (YC < hy - 12) & (XC > hx - 13) & erode(erode(face)), (176, 104, 100), 0.7, 3)
    if beard > 0.02:                                                             # time-lapse beard
        sp.ell(hx + 4, hy - 16 - 4 * beard, 13 + 3 * beard, 3 + 7 * beard, D_STACHE)
    sp.line((hx - 3, hy + 9), (hx + 4, hy + 9), D_SKIN[1])                         # forehead crease
    # eyes + brows
    bl_ = _blink(t, blink)
    lk = (look, 0.0)
    if not shades:
        eye(sp, hx - 4.0, hy + 2.0, 9, 7, X, (66, 110, 168), lk, bl_, LASH, D_SKIN[2], lidc=D_SKIN[1], bag=D_SKIN[1], bold=1)
        eye(sp, hx + 9.5, hy + 2.0, 7, 6.5, X, (66, 110, 168), lk, bl_, LASH, D_SKIN[2], lidc=D_SKIN[1], bag=D_SKIN[1], bold=1)
        brow(sp, hx - 4.0, hy + 7.5, 10, X, +1, (70, 46, 34), th=3, bushy=True)
        brow(sp, hx + 9.5, hy + 7.5, 7, X, -1, (70, 46, 34), th=3, bushy=True)
    else:
        brow(sp, hx - 4.0, hy + 8.5, 10, X, +1, (70, 46, 34), th=2, bushy=True)
        brow(sp, hx + 9.5, hy + 8.5, 7, X, -1, (70, 46, 34), th=2, bushy=True)
        sh = sp.m_poly([(hx - 10, hy + 6.5), (hx + 15, hy + 6.5), (hx + 14, hy - 1), (hx + 7, hy - 2), (hx + 4, hy + 2), (hx + 1, hy - 2), (hx - 9, hy - 1)])
        sp.paint(sh, [(6, 6, 10), (14, 14, 20), (24, 26, 36), (44, 48, 66)], None, olc=(4, 4, 8))
        sp.line((hx - 7, hy + 5), (hx - 4, hy + 2), (150, 170, 220)); sp.line((hx + 9, hy + 5), (hx + 11, hy + 3), (120, 140, 190))
        sp.dot(hx - 6, hy + 5, (255, 255, 255)); sp.line((hx - 10, hy + 4), (hx - 15, hy + 1), (10, 10, 14))
    # bulb nose (red from the cold)
    sp.ell(hx + 8.0, hy - 5.0, 5.8, 5.0, D_NOSE)
    sp.dot(hx + 6, hy - 2, (255, 220, 212)); sp.dot(hx + 7, hy - 2, (255, 220, 212)); sp.dot(hx + 6, hy - 3, (255, 196, 186))
    sp.dot(hx + 9, hy - 8, D_NOSE[0]); sp.dot(hx + 10, hy - 8, D_NOSE[0])
    blush(sp, hx - 5, hy - 5, 4.5, 2.6, (226, 108, 100)); blush(sp, hx + 15, hy - 4, 2.0, 2.0, (226, 108, 100))
    # mouth under a walrus moustache
    mo = max(mouth_, X['mo'])
    mouth(sp, hx + 7.5, hy - 16.0, 9, X, mouth_, (120, 46, 50), skin=D_SKIN[2], maxh=9)
    st = sp.m_poly([(hx - 1, hy - 9.5), (hx + 4, hy - 8.5), (hx + 8, hy - 9.5), (hx + 12, hy - 8.5), (hx + 17, hy - 10.5), (hx + 19, hy - 15),
                    (hx + 18, hy - 19 - mo * 1.5), (hx + 15, hy - 16), (hx + 11, hy - 14.5), (hx + 8, hy - 15), (hx + 4, hy - 14.5),
                    (hx + 0, hy - 16), (hx - 3, hy - 19 - mo * 1.5), (hx - 4, hy - 14)])
    sp.paint(st, D_STACHE, np.clip(0.85 - (hy - 9.5 - YC) * 0.08, 0, 1))
    for k in range(-2, 18, 2):                                                     # strands
        sp.dot(hx + k, hy - 12 - (k % 4 == 0), D_STACHE[0]); sp.dot(hx + k + 1, hy - 10, D_STACHE[3])
    sp.dot(hx + 7, hy - 14, D_STACHE[0]); sp.dot(hx + 8, hy - 13, D_STACHE[0])
    if sweat > 0.05:
        for k, (dx, dy) in enumerate(((-12, 10), (15, 8), (-8, 4))):
            yy = hy + dy - 6 * ((t * 1.4 + k * 0.37) % 1.0) * sweat
            sp.ell(hx + dx, yy, 1.4, 2.0, [(80, 140, 210), (120, 180, 240), (170, 220, 255), (236, 248, 255)], ol=True)
    # ushanka: fur crown above the head, light fur band on the forehead, flaps tied up
    fl = 1.5 * math.sin(flap) if flap else 0.0
    sp.ell(hx, hy + 19, 18.0, 8.0, D_FUR, dither=0.3)
    sp.cap((hx - 18.5, hy + 12 + fl), (hx - 20, hy + 19 + fl), 3.6, 3.0, D_FUR)
    sp.cap((hx + 19, hy + 11 - fl), (hx + 21, hy + 18 - fl), 3.4, 2.8, D_FUR)
    band = sp.cap((hx - 17.5, hy + 13.0), (hx + 18.5, hy + 12.5), 3.8, 3.8, D_FURL)
    sp.fill(band & CHECK & (YC > hy + 14) & ~erode(band), D_FURL[1])                     # fluffy edge
    sp.ell(hx + 4, hy + 13, 3.2, 2.7, [(150, 104, 24), (210, 160, 40), (244, 204, 80), (255, 240, 160)])
    sp.dot(hx + 4, hy + 13, (200, 40, 50)); sp.dot(hx + 3, hy + 13, (200, 40, 50))
    # front arm + props
    hr_, ar_ = arm(sp, G['shR'], tr, 14, 13, 5.6, 5.0, D_JACKET, bR, D_GLOVE, 4.0, cuff=D_JACKET[1:] + [D_JACKET[3]], quilt=True)
    _prop(sp, props.get('R'), hr_, ar_, t)
    sp.anchors.update(head=(hx, hy), handR=hr_, handL=hl, mouth=(hx + 6.0, hy - 15.5))
    if clip_h is not None: sp.clip_below(clip_h)
    sp.outline()
    sp.soot(soot)


# ======================================================================================== TERRY (tall, thin, nervous)
T_SKIN = [(158, 112, 104), (204, 156, 140), (236, 196, 178), (252, 224, 208)]
PUFF = [(14, 14, 20), (28, 28, 38), (46, 46, 60), (74, 74, 94)]
BEANIE = [(10, 10, 14), (22, 22, 28), (36, 36, 46), (60, 60, 76)]


def cds_patch(sp, x, y):
    """white comedy-mask patch with tiny letters CDS on the beanie (the theatre clue)"""
    sp.ell(x, y, 3.2, 3.6, [(170, 170, 180), (214, 214, 220), (244, 244, 248), (255, 255, 255)])
    sp.dot(x - 1, y + 1, (30, 30, 36)); sp.dot(x + 1, y + 1, (30, 30, 36))
    sp.dot(x - 1, y - 1, (30, 30, 36)); sp.dot(x, y - 2, (30, 30, 36)); sp.dot(x + 1, y - 1, (30, 30, 36))


def beanie(sp, hx, hy, rx, top, pal=BEANIE):
    sp.ell(hx, hy + top * 0.55, rx + 1.5, top * 0.62, pal)
    cuff = sp.cap((hx - rx - 1, hy + top * 0.2), (hx + rx + 1, hy + top * 0.2), 3.2, 3.2, pal)
    for k in range(int(hx - rx), int(hx + rx) + 1, 2): sp.fill(cuff & (np.abs(XC - k - 0.5) < 0.5) & erode(cuff), pal[0])
    cds_patch(sp, hx + rx * 0.35, hy + top * 0.25)


def thug_torso(sp, cx, cy, rx, ry, br, n=2.2):
    tm = sp.sup(cx, cy + br * 0.5, rx, ry, PUFF, n=n)
    for k in range(int((ry * 2) // 6)):
        yq = cy - ry + 5 + k * 6 + br * 0.5
        sp.fill(tm & erode(erode(tm)) & (np.abs(YC - (yq + 0.015 * (XC - cx) ** 2)) < 0.5), PUFF[0])
    sp.fill(tm & (np.abs(XC - (cx + 3.5)) < 0.6) & (YC < cy + ry - 3), (110, 112, 128))
    return tm


def terry(sp, pose='stand', t=0.0, mouth_=0.0, expr='nervous', look=0.0, blink=None, shades=False, hands=None, props=None,
          soot=0.0, sweat=0.0, legs=True, clip_h=None, breath=True, hat=True):
    pose = POSE[pose] if isinstance(pose, str) else pose
    X = EXPR.get(expr, EXPR['normal'])
    br = (0.5 * math.sin(t * 2.4 + 1)) if breath else 0.0
    hipy = 34.0
    hipL, hipR = (-5.0, hipy), (5.0, hipy)
    G = dict(shL=(-12.0, 70.0 + br), shR=(11.0, 70.0 + br), head=(3.0, 94.0 + br), hip=hipy, rx=13.0, arm=30.0, hrx=12.0, hry=15.0)
    tl, tr, bl, bR = hand_targets(pose, G)
    if hands: tl = hands.get('L', tl); tr = hands.get('R', tr)
    props = props or {}
    hl, al = arm(sp, G['shL'], tl, 16, 15, 3.8, 3.4, PUFF, bl, PUFF, 3.2, quilt=True)
    _prop(sp, props.get('L'), hl, al, t)
    if legs:
        (kL, aL), (kR, aR) = legs_for(pose, hipL, hipR, 16.0)
        leg(sp, hipL, kL, aL, 4.2, [(18, 18, 24), (30, 30, 40), (44, 44, 58), (66, 66, 86)], [(16, 16, 20), (30, 30, 36), (46, 46, 56), (74, 74, 90)], 10, 5)
        leg(sp, hipR, kR, aR, 4.2, [(18, 18, 24), (30, 30, 40), (44, 44, 58), (66, 66, 86)], [(16, 16, 20), (30, 30, 36), (46, 46, 56), (74, 74, 90)], 10, 5)
    thug_torso(sp, 0.0, 53.0, 14.0, 21.0, br, n=2.4)
    hx, hy = G['head']
    sp.cap((1.5, 72 + br), (2.5, 82 + br), 3.6, 3.4, T_SKIN)                           # long neck
    sp.dot(3, 77 + int(br), T_SKIN[1]); sp.dot(4, 77 + int(br), T_SKIN[1])             # adam's apple
    sp.cap((-6, 72 + br), (11, 72 + br), 4.2, 4.2, PUFF)                                # collar
    face = sp.union([sp.m_ell(hx, hy, 11.5, 15.0), sp.m_ell(hx + 3.0, hy - 8.0, 9.5, 8.5)], T_SKIN)   # egg head + forward chin
    sp.ell(hx - 10.5, hy + 0, 2.6, 4.0, T_SKIN)
    sp.dot(hx - 11, hy, T_SKIN[0])
    bl_ = _blink(t, blink)
    lk = (look, 0.0)
    if not shades:
        eye(sp, hx - 2.5, hy + 2.0, 7, 6.5, X, (96, 128, 72), lk, bl_, LASH, T_SKIN[2], lidc=T_SKIN[1], bag=(196, 150, 160))
        eye(sp, hx + 7.5, hy + 2.0, 6, 6.0, X, (96, 128, 72), lk, bl_, LASH, T_SKIN[2], lidc=T_SKIN[1], bag=(196, 150, 160))
    brow(sp, hx - 2.5, hy + 7.0, 8, X, +1, (60, 44, 36), th=1.6, arch=1.2)
    brow(sp, hx + 7.5, hy + 7.0, 6, X, -1, (60, 44, 36), th=1.6, arch=1.0)
    sp.line((hx - 3, hy + 9.5), (hx + 5, hy + 9.5), T_SKIN[1])                               # worry lines
    if X['bt'] < -0.3: sp.line((hx - 2, hy + 11), (hx + 4, hy + 11), T_SKIN[1])
    if shades:
        sh = sp.m_poly([(hx - 7, hy + 5), (hx + 12, hy + 5), (hx + 11, hy - 1), (hx + 5, hy - 1), (hx + 3, hy + 2), (hx + 1, hy - 1), (hx - 6, hy - 1)])
        sp.paint(sh, [(6, 6, 10), (14, 14, 20), (24, 26, 36), (44, 48, 66)], None, olc=(4, 4, 8))
        sp.dot(hx - 4, hy + 3, (255, 255, 255))
    # long pointy nose, starting under the eyes
    nm = sp.m_poly([(hx + 3.5, hy - 0.5), (hx + 5.5, hy - 0.5), (hx + 14.5, hy - 8), (hx + 12.5, hy - 10), (hx + 4, hy - 9.5)])
    sp.paint(nm, T_SKIN, np.clip(0.85 - (XC - hx) * 0.035, 0, 1), olc=T_SKIN[0])
    sp.dot(hx + 7, hy - 9, T_SKIN[0]); sp.dot(hx + 13, hy - 8, T_SKIN[3])
    # pencil moustache + mouth
    mouth(sp, hx + 6.0, hy - 13.0, 7, X, mouth_, (150, 80, 80), skin=T_SKIN[2], maxh=6)
    if mouth_ < 0.1 and X['mo'] < 0.1: sp.line((hx + 3, hy - 11.5), (hx + 10, hy - 11.5), (60, 44, 36))
    if sweat > 0.05 or X['bt'] < -0.5:
        for k, (dx, dy) in enumerate(((-9, 8), (9, 9))):
            yy = hy + dy - 5 * ((t * 1.3 + k * 0.5) % 1.0)
            sp.ell(hx + dx, yy, 1.2, 1.8, [(80, 140, 210), (120, 180, 240), (170, 220, 255), (236, 248, 255)])
    if hat: beanie(sp, hx, hy + 10, 12.0, 11.0)
    hr_, ar_ = arm(sp, G['shR'], tr, 16, 15, 4.0, 3.6, PUFF, bR, PUFF, 3.3, quilt=True)
    _prop(sp, props.get('R'), hr_, ar_, t)
    sp.anchors.update(head=(hx, hy), handR=hr_, handL=hl)
    if clip_h is not None: sp.clip_below(clip_h)
    sp.outline()
    sp.soot(soot)


# ======================================================================================== GARY (short, round, cheerful)
G_SKIN = [(148, 92, 66), (194, 132, 96), (226, 168, 126), (246, 204, 164)]


def gary(sp, pose='stand', t=0.0, mouth_=0.0, expr='normal', look=0.0, blink=None, shades=False, hands=None, props=None,
         soot=0.0, sweat=0.0, legs=True, clip_h=None, breath=True, hat=True, badge=False):
    pose = POSE[pose] if isinstance(pose, str) else pose
    X = EXPR.get(expr, EXPR['normal'])
    br = (0.7 * math.sin(t * 2.0 + 2)) if breath else 0.0
    hipy = 15.0
    hipL, hipR = (-7.0, hipy), (7.0, hipy)
    G = dict(shL=(-19.0, 44.0 + br), shR=(16.0, 44.0 + br), head=(3.0, 64.0 + br), hip=hipy, rx=22.0, arm=21.0, hrx=16.0, hry=15.0)
    tl, tr, bl, bR = hand_targets(pose, G)
    if hands: tl = hands.get('L', tl); tr = hands.get('R', tr)
    props = props or {}
    hl, al = arm(sp, G['shL'], tl, 11, 10, 4.8, 4.4, PUFF, bl, PUFF, 3.6, quilt=True)
    _prop(sp, props.get('L'), hl, al, t)
    if legs:
        (kL, aL), (kR, aR) = legs_for(pose, hipL, hipR, 7.5)
        dk = [(18, 18, 24), (30, 30, 40), (44, 44, 58), (66, 66, 86)]
        leg(sp, hipL, kL, aL, 5.2, dk, [(16, 16, 20), (30, 30, 36), (46, 46, 56), (74, 74, 90)], 10, 5)
        leg(sp, hipR, kR, aR, 5.2, dk, [(16, 16, 20), (30, 30, 36), (46, 46, 56), (74, 74, 90)], 10, 5)
    thug_torso(sp, 0.0, 31.0, 22.5, 18.5, br, n=2.0)
    if badge:                                                                                   # yellow SECURITY plate on the chest
        sp.rect(-17, 36 + int(br), 6, 44 + int(br), (36, 36, 44)); sp.rect(-16, 37 + int(br), 5, 43 + int(br), (250, 214, 60))
        text3(sp, 'GUARD', -15, 42 + int(br), (36, 36, 44), keep=True)
    hx, hy = G['head']
    face = sp.union([sp.m_ell(hx, hy, 15.5, 14.5), sp.m_ell(hx + 3, hy - 11.5, 12.5, 5.5)], G_SKIN)      # moon face + double chin
    sp.line((hx - 5, hy - 12), (hx + 10, hy - 12), G_SKIN[1])
    sp.ell(hx - 14.5, hy - 0.5, 3.0, 4.0, G_SKIN)
    bl_ = _blink(t, blink)
    lk = (look, 0.0)
    if not shades:
        eye(sp, hx - 3.5, hy + 1.5, 7, 6.0, X, (110, 76, 46), lk, bl_, LASH, G_SKIN[2], lidc=G_SKIN[1])
        eye(sp, hx + 7.0, hy + 1.5, 6, 5.5, X, (110, 76, 46), lk, bl_, LASH, G_SKIN[2], lidc=G_SKIN[1])
    else:
        sh = sp.m_poly([(hx - 8, hy + 4.5), (hx + 11, hy + 4.5), (hx + 10, hy - 1), (hx + 4, hy - 1), (hx + 2, hy + 1), (hx, hy - 1), (hx - 7, hy - 1)])
        sp.paint(sh, [(6, 6, 10), (14, 14, 20), (24, 26, 36), (44, 48, 66)], None, olc=(4, 4, 8))
        sp.dot(hx - 5, hy + 3, (255, 255, 255))
    brow(sp, hx - 3.5, hy + 6.5, 8, X, +1, (50, 36, 30), th=2.4)
    brow(sp, hx + 7.0, hy + 6.5, 6, X, -1, (50, 36, 30), th=2.4)
    sp.ell(hx + 4.5, hy - 3.0, 3.2, 2.7, G_SKIN, olc=G_SKIN[0])                               # button nose
    sp.dot(hx + 3, hy - 2, (255, 230, 200)); sp.dot(hx + 5, hy - 5, G_SKIN[0])
    blush(sp, hx - 6, hy - 5, 4.0, 2.4, (236, 120, 110)); blush(sp, hx + 10, hy - 5, 3.0, 2.2, (236, 120, 110))
    mouth(sp, hx + 4.0, hy - 8.5, 9, X, mouth_, (150, 70, 70), skin=G_SKIN[2], maxh=7)
    if sweat > 0.05:
        for k, (dx, dy) in enumerate(((-11, 8), (12, 7))):
            yy = hy + dy - 5 * ((t * 1.3 + k * 0.5) % 1.0)
            sp.ell(hx + dx, yy, 1.2, 1.8, [(80, 140, 210), (120, 180, 240), (170, 220, 255), (236, 248, 255)])
    if hat: beanie(sp, hx, hy + 8, 15.5, 11.0)
    hr_, ar_ = arm(sp, G['shR'], tr, 11, 10, 5.0, 4.6, PUFF, bR, PUFF, 3.8, quilt=True)
    _prop(sp, props.get('R'), hr_, ar_, t)
    sp.anchors.update(head=(hx, hy), handR=hr_, handL=hl)
    if clip_h is not None: sp.clip_below(clip_h)
    sp.outline()
    sp.soot(soot)


# ======================================================================================== shared helpers for the rest of the cast
def hair_cloud(sp, cx, cy, rx, ry, pal, a0=-0.35, a1=math.pi + 0.35, r=3.6, n=14, inner=True, seed=0):
    """curly perm / cloud of hair: bumps along an elliptical arc (angles a0..a1, counter-clockwise from +x) + a filled core"""
    parts = []
    if inner: parts.append(sp.m_ell(cx, cy, rx * 0.86, ry * 0.86))
    for k in range(n):
        a = a0 + (a1 - a0) * k / (n - 1)
        rr = r * (0.85 + 0.3 * ((k * 7 + seed) % 3) / 2)
        parts.append(sp.m_ell(cx + math.cos(a) * rx, cy + math.sin(a) * ry, rr, rr))
    m = sp.union(parts, pal, dither=0.28)
    for k in range(n):                                                           # curl marks
        a = a0 + (a1 - a0) * (k + 0.5) / (n - 1)
        sp.dot(int(cx + math.cos(a) * rx * 0.8), int(cy + math.sin(a) * ry * 0.8), pal[0])
    return m


def rings(sp, cx, cy, r, col, th=1):
    """thin ring (glasses frames)"""
    m, _, _ = sp.m_ell(cx, cy, r, r * 0.92)
    e = m & ~erode(m)
    if th > 1: e = e | (dilate(e) & m & ~erode(erode(m)))
    sp.fill(e, col)
    return m


def old_lines(sp, hx, hy, X, skin, side_w=8):
    """wrinkles for the old ladies: crow's feet, nasolabial folds, forehead"""
    c = skin[1]
    sp.line((hx - 9, hy + 2), (hx - 11, hy + 3), c); sp.line((hx - 9, hy + 0), (hx - 11, hy - 1), c)
    sp.line((hx - 3, hy + 9), (hx + 6, hy + 9), c); sp.line((hx - 2, hy + 10.5), (hx + 5, hy + 10.5), c)
    sp.line((hx + 1, hy - 5), (hx - 1, hy - 10), c); sp.line((hx + 9, hy - 5), (hx + 10, hy - 10), c)


# ======================================================================================== DEB (dispatcher, at her desk)
DEB_SKIN = [(160, 100, 90), (206, 146, 124), (238, 190, 164), (252, 222, 200)]
DEB_HAIR = [(118, 116, 132), (162, 160, 176), (202, 200, 214), (236, 234, 244)]
DEB_CARD = [(120, 84, 22), (176, 126, 34), (220, 168, 58), (246, 208, 118)]
DEB_BLOUSE = [(176, 180, 196), (214, 218, 230), (240, 242, 248), (255, 255, 255)]
DEB_PINK = (232, 86, 160)


def deb(sp, pose='hold', t=0.0, mouth_=0.0, expr='smile', look=0.0, blink=None, hands=None, props=None, sweat=0.0, legs=False,
        clip_h=None, breath=True, headset=True, lean=0.0):
    pose = POSE[pose] if isinstance(pose, str) else pose
    X = EXPR.get(expr, EXPR['normal'])
    br = (0.5 * math.sin(t * 2.1 + 0.5)) if breath else 0.0
    G = dict(shL=(-15.0, 48.0 + br), shR=(13.0, 48.0 + br), head=(2.0 + lean, 66.0 + br), hip=18.0, rx=18.0, arm=22.0, hrx=14.0, hry=13.5)
    tl, tr, bl, bR = hand_targets(pose, G)
    if pose.get('name') == 'hold': tl, tr, bl, bR = (-2.0, 34.0), (10.0, 35.0), 1, 1
    if hands: tl = hands.get('L', tl); tr = hands.get('R', tr)
    props = props if props is not None else {'R': 'knit'}
    hl, al = arm(sp, G['shL'], tl, 12, 11, 4.6, 4.0, DEB_CARD, bl, DEB_SKIN, 3.0, cuff=DEB_BLOUSE)
    _prop(sp, props.get('L'), hl, al, t)
    sp.cap((1.0, 40 + br), (2.0, 55 + br), 4.2, 4.0, DEB_SKIN)                                              # neck
    # torso: mustard cardigan over a white blouse with a round collar + pearls
    tm = sp.sup(0.0, 31.0 + br * 0.5, 18.0, 18.5, DEB_CARD, n=2.2)
    sp.fill(tm & CHECK & (np.abs(XC - 0.0) > 5) & ((YC.astype(int) % 3) == 0), DEB_CARD[1])               # knit texture
    bl_m = sp.m_poly([(-5, 49.5 + br), (9, 49.5 + br), (3, 30 + br)])
    sp.paint(bl_m, DEB_BLOUSE, None)
    for k in range(4): sp.dot(5 if k % 2 else 4, 42 - k * 4 + int(br), (120, 84, 22))                     # cardigan buttons
    for k in range(-3, 9): sp.dot(k, int(48.5 + br - 0.12 * (k - 3) ** 2), (250, 246, 236), keep=True)       # pearls
    sp.cap((-6, 50 + br), (11, 50 + br), 2.4, 2.4, DEB_BLOUSE)                                              # collar
    hx, hy = G['head']
    # hair back mass first (behind the face)
    sp.ell(hx - 2, hy + 3, 16.5, 14.5, DEB_HAIR, dither=0.3)
    face = sp.union([sp.m_ell(hx, hy, 13.5, 13.5), sp.m_ell(hx + 1.5, hy - 6, 12.5, 8.0)], DEB_SKIN)
    sp.ell(hx - 12.5, hy - 1, 2.6, 3.6, DEB_SKIN)
    sp.dot(hx - 13, hy - 5, DEB_PINK); sp.dot(hx - 13, hy - 6, DEB_PINK)                                  # earring
    bl_ = _blink(t, blink)
    lk = (look, 0.0)
    eye(sp, hx - 3.5, hy + 0.5, 7, 7, X, (120, 84, 50), lk, bl_, LASH, DEB_SKIN[2], lidc=DEB_SKIN[1], flick=True, bold=2)
    eye(sp, hx + 7.0, hy + 0.5, 6, 6.5, X, (120, 84, 50), lk, bl_, LASH, DEB_SKIN[2], lidc=DEB_SKIN[1], flick=False, bold=2)
    brow(sp, hx - 3.5, hy + 7.5, 7, X, +1, (120, 116, 128), th=1.2, arch=1.4)
    brow(sp, hx + 7.0, hy + 7.5, 5, X, -1, (120, 116, 128), th=1.2, arch=1.2)
    # big pink glasses
    rings(sp, hx - 3.5, hy + 0.5, 5.6, DEB_PINK, th=2); rings(sp, hx + 7.2, hy + 0.5, 4.8, DEB_PINK, th=2)
    sp.line((hx + 2, hy + 2), (hx + 3, hy + 2), DEB_PINK); sp.line((hx - 9, hy + 2), (hx - 12, hy + 1), DEB_PINK)
    sp.dot(hx - 6, hy + 4, (255, 255, 255)); sp.dot(hx - 5, hy + 3, (255, 255, 255)); sp.dot(hx + 5, hy + 3, (255, 255, 255))
    # nose, lipstick, blush
    sp.ell(hx + 4.5, hy - 4.5, 2.6, 2.4, DEB_SKIN, olc=DEB_SKIN[0])
    sp.dot(hx + 3, hy - 3, DEB_SKIN[3])
    blush(sp, hx - 6, hy - 5, 3.6, 2.2, (240, 120, 130)); blush(sp, hx + 10, hy - 5, 2.4, 2.0, (240, 120, 130))
    mouth(sp, hx + 3.5, hy - 9.5, 8, X, mouth_, (196, 52, 92), skin=DEB_SKIN[2], maxh=7)
    if sweat > 0.05:
        yy = hy + 8 - 5 * ((t * 1.3) % 1.0)
        sp.ell(hx + 11, yy, 1.2, 1.8, [(80, 140, 210), (120, 180, 240), (170, 220, 255), (236, 248, 255)])
    # perm on top: curls over the forehead and the sides
    hair_cloud(sp, hx - 1, hy + 6, 14.5, 9.0, DEB_HAIR, a0=-0.15, a1=math.pi + 0.25, r=3.4, n=13, inner=False, seed=2)
    if headset:
        sp.line((hx - 14, hy + 2), (hx - 9, hy + 15), (40, 40, 48), 2); sp.line((hx - 9, hy + 15), (hx + 4, hy + 17), (40, 40, 48), 2)
        sp.ell(hx - 13.5, hy + 0.5, 2.8, 3.6, [(20, 20, 26), (40, 40, 50), (64, 64, 78), (100, 100, 120)])
        sp.line((hx - 12, hy - 2), (hx - 5, hy - 9), (40, 40, 48)); sp.line((hx - 5, hy - 9), (hx - 1, hy - 10), (40, 40, 48))
        sp.ell(hx - 0.5, hy - 10, 1.4, 1.2, [(20, 20, 26), (40, 40, 50), (64, 64, 78), (100, 100, 120)], ol=False)
        if int(t * 3) % 2 == 0: sp.dot(hx - 13, hy - 1, (90, 240, 120))
    hr_, ar_ = arm(sp, G['shR'], tr, 12, 11, 4.8, 4.2, DEB_CARD, bR, DEB_SKIN, 3.1, cuff=DEB_BLOUSE)
    _prop(sp, props.get('R'), hr_, ar_, t)
    sp.anchors.update(head=(hx, hy), handR=hr_, handL=hl)
    if clip_h is not None: sp.clip_below(clip_h)
    sp.outline()


# ======================================================================================== BRAD (Naperville dad)
B_SKIN = [(150, 92, 64), (198, 136, 98), (232, 178, 132), (250, 214, 174)]
B_HAIR = [(110, 70, 30), (160, 112, 50), (206, 160, 80), (246, 222, 150)]
B_VEST = [(10, 70, 76), (20, 112, 116), (40, 160, 158), (110, 210, 200)]
B_SHIRT = [(110, 140, 190), (150, 180, 224), (190, 214, 244), (230, 240, 255)]
B_KHAKI = [(120, 100, 66), (164, 140, 96), (200, 178, 132), (230, 214, 176)]
B_SHOE = [(170, 174, 186), (214, 218, 228), (244, 246, 250), (255, 255, 255)]


def brad(sp, pose='stand', t=0.0, mouth_=0.0, expr='grin', look=0.0, blink=None, hands=None, props=None, legs=True, clip_h=None,
         breath=True, shades_up=True, ting=0.0):
    pose = POSE[pose] if isinstance(pose, str) else pose
    X = EXPR.get(expr, EXPR['normal'])
    br = (0.5 * math.sin(t * 2.3 + 3)) if breath else 0.0
    hipy = 30.0
    hipL, hipR = (-5.5, hipy), (5.5, hipy)
    G = dict(shL=(-17.0, 63.0 + br), shR=(15.0, 63.0 + br), head=(3.0, 84.0 + br), hip=hipy, rx=17.0, arm=27.0, hrx=12.5, hry=14.0)
    tl, tr, bl, bR = hand_targets(pose, G)
    if hands: tl = hands.get('L', tl); tr = hands.get('R', tr)
    props = props or {}
    hl, al = arm(sp, G['shL'], tl, 14, 13, 4.4, 3.8, B_SHIRT, bl, B_SKIN, 3.2)
    _prop(sp, props.get('L'), hl, al, t)
    if legs:
        (kL, aL), (kR, aR) = legs_for(pose, hipL, hipR, 14.0)
        leg(sp, hipL, kL, aL, 5.0, B_KHAKI, B_SHOE, 12, 6, sole=(250, 250, 252))
        leg(sp, hipR, kR, aR, 5.0, B_KHAKI, B_SHOE, 12, 6, sole=(250, 250, 252))
        for a in (aL, aR): sp.rect(a[0] - 3, a[1] + 3, a[0] + 5, a[1] + 4, (40, 120, 220))                 # dad-shoe swoosh stripe
    sp.cap((1.5, 56 + br), (2.5, 72 + br), 4.0, 3.8, B_SKIN)                                                # neck
    # V torso: shirt, fleece vest on top, lanyard
    sp.poly([(-17, 66 + br), (17, 66 + br), (11, 30), (-10, 30)], B_SHIRT, grad=(66, 30))
    vest = sp.m_poly([(-16, 64 + br), (-3, 64 + br), (3, 52 + br), (9, 64 + br), (16, 64 + br), (11, 28), (-10, 28)])
    sp.paint(vest, B_VEST, np.clip((YC - 28) / 36 * 0.6 + 0.2 - XC * 0.008, 0, 1), dither=0.3)
    sp.fill(vest & (np.abs(XC - 3.0 - (YC - 52) * 0.0) < 0.6) & (YC < 52 + br), (200, 220, 220))          # zipper
    sp.cap((-8, 31), (13, 31), 1.6, 1.6, B_VEST)
    sp.line((-6, 63 + br), (1, 44 + br), (214, 40, 50), 1); sp.line((12, 63 + br), (5, 44 + br), (214, 40, 50), 1)
    sp.rect(0, 38 + int(br), 7, 45 + int(br), (250, 250, 250)); sp.rect(1, 42 + int(br), 6, 44 + int(br), (40, 120, 220))
    text3(sp, 'PTA', 0, 41 + int(br), (30, 30, 40))
    hx, hy = G['head']
    face = sp.union([sp.m_ell(hx, hy + 1, 12.5, 13.5), sp.m_super(hx + 2, hy - 7.5, 11.5, 7.5, 3.0)], B_SKIN)     # square jaw
    sp.dot(hx + 6, hy - 14, B_SKIN[0])                                                                       # cleft chin
    sp.ell(hx - 11.5, hy - 0.5, 2.6, 3.8, B_SKIN)
    bl_ = _blink(t, blink)
    lk = (look, 0.0)
    eye(sp, hx - 2.5, hy + 1.5, 7, 6, X, (50, 140, 230), lk, bl_, LASH, B_SKIN[2], lidc=B_SKIN[1])
    eye(sp, hx + 7.5, hy + 1.5, 6, 5.5, X, (50, 140, 230), lk, bl_, LASH, B_SKIN[2], lidc=B_SKIN[1])
    brow(sp, hx - 2.5, hy + 6.5, 8, X, +1, (120, 80, 36), th=1.8, arch=0.8)
    brow(sp, hx + 7.5, hy + 6.5, 6, X, -1, (120, 80, 36), th=1.8, arch=0.6)
    nm = sp.m_poly([(hx + 3.5, hy + 0), (hx + 5.5, hy + 0), (hx + 9.5, hy - 5.5), (hx + 7.5, hy - 7), (hx + 4, hy - 6.5)])
    sp.paint(nm, B_SKIN, np.clip(0.8 - (XC - hx) * 0.04, 0, 1), olc=B_SKIN[0])
    mouth(sp, hx + 4.5, hy - 10.0, 11, X, mouth_, (150, 60, 60), skin=B_SKIN[2], maxh=7)
    # glossy side part
    hair = sp.m_poly([(hx - 13, hy + 3), (hx - 13, hy + 10), (hx - 8, hy + 16), (hx + 2, hy + 17.5), (hx + 11, hy + 15), (hx + 15, hy + 9),
                      (hx + 13, hy + 7), (hx + 6, hy + 10), (hx - 2, hy + 9), (hx - 9, hy + 8), (hx - 11, hy + 3)])
    sp.paint(hair, B_HAIR, np.clip((YC - (hy + 6)) / 11.0, 0, 1) * 0.8 + 0.1)
    sp.line((hx - 6, hy + 15), (hx - 7, hy + 11), B_HAIR[0])                                                # the part
    sp.line((hx - 3, hy + 15), (hx + 9, hy + 13), B_HAIR[3]); sp.line((hx - 2, hy + 16), (hx + 6, hy + 15), (255, 250, 220))  # gloss
    if shades_up:                                                                                            # wraparounds on the head
        sh = sp.m_poly([(hx - 9, hy + 17), (hx + 12, hy + 15), (hx + 12, hy + 12.5), (hx - 8, hy + 14.5)])
        sp.paint(sh, [(10, 14, 20), (24, 30, 44), (40, 60, 90), (90, 160, 220)], np.clip((XC - hx + 9) / 21, 0, 1))
    if ting > 0.05:                                                                                          # tooth sparkle
        cx_, cy_ = hx + 10, hy - 9
        c = (255, 255, 230)
        for d in range(1, int(1 + 4 * ting)): sp.dot(cx_ + d, cy_, c, keep=True); sp.dot(cx_ - d, cy_, c, keep=True); sp.dot(cx_, cy_ + d, c, keep=True); sp.dot(cx_, cy_ - d, c, keep=True)
    hr_, ar_ = arm(sp, G['shR'], tr, 14, 13, 4.6, 4.0, B_SHIRT, bR, B_SKIN, 3.3)
    _prop(sp, props.get('R'), hr_, ar_, t)
    sp.anchors.update(head=(hx, hy), handR=hr_, handL=hl)
    if clip_h is not None: sp.clip_below(clip_h)
    sp.outline()


# ======================================================================================== the window ladies (busts)
L_SKIN = [(160, 108, 96), (206, 154, 136), (236, 196, 176), (252, 226, 210)]
LADIES = dict(
    mrs_w=dict(robe=(222, 92, 130), hair=(200, 196, 204), scarf=(206, 40, 52), glasses=None, curlers=True, iris=(90, 110, 140)),
    rose=dict(robe=(70, 120, 210), hair=(246, 244, 250), scarf=None, glasses=(150, 40, 60), curlers=False, iris=(100, 80, 60), bun=True),
    dot=dict(robe=(70, 160, 100), hair=(120, 80, 50), scarf=None, glasses=None, curlers=False, iris=(80, 110, 70), net=True),
)


def lady(sp, who='mrs_w', pose='hold', t=0.0, mouth_=0.0, expr='deadpan', look=0.0, blink=None, hands=None, props=None, legs=False,
         clip_h=24.0, breath=True):
    pose = POSE[pose] if isinstance(pose, str) else pose
    L = LADIES[who]
    X = EXPR.get(expr, EXPR['normal'])
    br = (0.4 * math.sin(t * 2.0 + len(who))) if breath else 0.0
    G = dict(shL=(-14.0, 46.0 + br), shR=(12.0, 46.0 + br), head=(2.0, 66.0 + br), hip=16.0, rx=16.0, arm=20.0, hrx=12.0, hry=13.0)
    tl, tr, bl, bR = hand_targets(pose, G)
    if pose.get('name') == 'hold': tl, tr, bl, bR = (-1.0, 58.0), (9.0, 58.0), 1, 1
    if hands: tl = hands.get('L', tl); tr = hands.get('R', tr)
    props = props or {}
    robe = ramp(L['robe'])
    hl, al = arm(sp, G['shL'], tl, 11, 10, 4.4, 4.0, robe, bl, L_SKIN, 2.8)
    sp.cap((1.0, 38 + br), (2.0, 52 + br), 4.0, 3.8, L_SKIN)
    tm = sp.sup(0.0, 30.0, 16.5, 17.0, robe, n=2.2)
    sp.fill(tm & CHECK & ((YC.astype(int) + XC.astype(int)) % 6 == 0), robe[3])                                # terry-cloth dots
    lap = sp.m_poly([(-6, 47 + br), (2, 30), (10, 47 + br)])
    sp.fill(lap & ~erode(lap), robe[0])
    hx, hy = G['head']
    if L.get('bun'): sp.ell(hx - 3, hy + 13, 6, 5, ramp(L['hair']), dither=0.3)
    face = sp.union([sp.m_ell(hx, hy, 12.0, 13.0), sp.m_ell(hx + 2, hy - 7, 11.0, 7.0)], L_SKIN)               # soft jowls
    sp.ell(hx - 11.0, hy - 1, 2.4, 3.6, L_SKIN)
    bl_ = _blink(t, blink)
    lk = (look, 0.0)
    eye(sp, hx - 2.5, hy + 1.0, 6, 5, X, L['iris'], lk, bl_, LASH, L_SKIN[2], lidc=L_SKIN[1], bag=L_SKIN[1], flick=True)
    eye(sp, hx + 7.0, hy + 1.0, 5, 4.5, X, L['iris'], lk, bl_, LASH, L_SKIN[2], lidc=L_SKIN[1], bag=L_SKIN[1])
    brow(sp, hx - 2.5, hy + 6.0, 6, X, +1, dark(L['hair'], 0.6), th=1.2, arch=1.2)
    brow(sp, hx + 7.0, hy + 6.0, 4, X, -1, dark(L['hair'], 0.6), th=1.2, arch=1.0)
    old_lines(sp, hx, hy, X, L_SKIN)
    if L['glasses']:
        rings(sp, hx - 2.5, hy + 1, 4.6, L['glasses'], th=2); rings(sp, hx + 7.2, hy + 1, 4.0, L['glasses'], th=2)
        sp.line((hx + 2, hy + 2), (hx + 3, hy + 2), L['glasses']); sp.dot(hx - 4, hy + 3, (255, 255, 255))
    sp.ell(hx + 5, hy - 3.5, 2.6, 2.6, L_SKIN, olc=L_SKIN[0])
    blush(sp, hx - 5, hy - 4, 3.0, 2.0, (230, 130, 130))
    mouth(sp, hx + 4, hy - 9.5, 7, X, mouth_, (170, 70, 90), skin=L_SKIN[2], maxh=6)
    hp = ramp(L['hair'])
    if L['scarf'] is not None:                                                                 # babushka headscarf with a polka pattern
        sc = ramp(L['scarf'])
        if L['curlers']:
            for k in range(4): sp.cap((hx - 6 + k * 4, hy + 9.5), (hx - 4 + k * 4, hy + 9.5), 1.8, 1.8, ramp((240, 150, 190)))
        hole = sp.m_ell(hx + 2.0, hy - 1.5, 11.0, 11.5)[0] & (YC < hy + 8.5)
        m = sp.union([sp.m_ell(hx - 1, hy + 6, 15.0, 11.0), sp.m_ell(hx - 9, hy - 3, 6, 10)], sc, dither=0.25, exclude=hole)
        sp.fill(m & CHECK & ((XC.astype(int) % 4) == 0) & ((YC.astype(int) % 4) == 0), (255, 240, 230))
        sp.ell(hx - 4, hy - 12, 3.4, 2.6, sc)                                                    # knot under the chin
        sp.cap((hx - 5, hy - 13), (hx - 8, hy - 18), 1.8, 1.4, sc)
    else:
        hair_cloud(sp, hx - 1, hy + 5, 13.0, 8.5, hp, a0=-0.1, a1=math.pi + 0.2, r=3.0, n=12, inner=False, seed=len(who))
        if L.get('net'):
            for k in range(-12, 12, 3): sp.line((hx + k, hy + 13), (hx + k + 3, hy + 6), (70, 60, 60))
    hr_, ar_ = arm(sp, G['shR'], tr, 11, 10, 4.6, 4.2, robe, bR, L_SKIN, 2.9)
    _prop(sp, props.get('R'), hr_, ar_, t)
    sp.anchors.update(head=(hx, hy), handR=hr_, handL=hl)
    if clip_h is not None: sp.clip_below(clip_h)
    sp.outline()


# ======================================================================================== MARTY (rat informant)
R_FUR = [(70, 70, 84), (104, 104, 120), (140, 140, 156), (182, 182, 196)]
R_PINK = [(170, 90, 100), (214, 128, 136), (240, 166, 170), (255, 206, 206)]
R_CAP = [(60, 44, 30), (96, 72, 48), (130, 102, 70), (168, 140, 100)]


def marty(sp, pose='sit', t=0.0, mouth_=0.0, expr='deadpan', look=0.0, blink=None, hands=None, props=None, legs=True, clip_h=None, breath=True):
    X = EXPR.get(expr, EXPR['normal'])
    br = (0.4 * math.sin(t * 3.0)) if breath else 0.0
    # tail curling behind
    pts = [(-6 - 9 * math.sin(k * 0.35) - k * 0.6, 3 + k * 1.4 + 2 * math.sin(t * 2 + k * 0.4)) for k in range(14)]
    for a, b in zip(pts[:-1], pts[1:]): sp.cap(a, b, 1.6, 1.4, R_PINK)
    # body: pear on haunches, light belly
    body = sp.union([sp.m_ell(0, 13 + br * 0.4, 11.5, 13.0), sp.m_ell(-3, 7, 10, 7)], R_FUR, dither=0.3)
    sp.ell(3, 12, 6, 9, ramp((200, 196, 206)), dither=0.25)
    for x in (-6, 4): sp.ell(x, 1.5, 4.5, 1.8, R_PINK)                                           # feet
    for x in (-5, -4, 5, 6): sp.dot(x + 2, 1, R_PINK[0])
    # striped scarf
    sc = sp.cap((-9, 25 + br), (10, 25 + br), 3.0, 3.0, ramp((40, 90, 190)))
    sp.fill(sc & ((XC.astype(int) % 4) < 2), (226, 230, 236))
    tail_ = sp.cap((6, 24 + br), (9, 13 + br), 2.4, 2.2, ramp((40, 90, 190)))
    sp.fill(tail_ & ((YC.astype(int) % 4) < 2), (226, 230, 236))
    # arms (front paws)
    tr = (hands or {}).get('R', (8.0, 18.0)); tl = (hands or {}).get('L', (-4.0, 17.0))
    sp.cap((-6, 22), tl, 2.2, 1.8, R_FUR); sp.ell(tl[0], tl[1], 2.0, 1.8, R_PINK)
    hx, hy = 2.0, 36.0 + br
    # ears
    for ex, ey, r in ((hx - 8, hy + 8, 5.5), (hx + 2, hy + 9.5, 4.6)):
        sp.ell(ex, ey, r, r, R_FUR); sp.ell(ex + 0.5, ey - 0.5, r * 0.6, r * 0.6, R_PINK, ol=False)
    head = sp.union([sp.m_ell(hx, hy, 9.5, 8.5), sp.m_ell(hx + 8, hy - 3, 8.5, 5.0)], R_FUR)
    sp.ell(hx + 15.5, hy - 2.5, 2.0, 1.8, R_PINK)                                                  # nose
    sp.dot(hx + 15, hy - 2, R_PINK[3])
    # whiskers
    for k, (dy, l) in enumerate(((0.5, 7), (-1.5, 8), (-3.5, 6))):
        sp.line((hx + 12, hy - 3 + dy * 0.3), (hx + 12 + l, hy - 3 + dy + 0.4 * math.sin(t * 5 + k)), (226, 226, 234))
        sp.line((hx + 9, hy - 3 + dy * 0.3), (hx + 9 - 4, hy - 3 + dy * 1.2), (210, 210, 220))
    bl_ = _blink(t, blink)
    eye(sp, hx + 1.5, hy + 1.5, 5, 5, X, (20, 16, 24), (look, 0.0), bl_, (14, 12, 18), R_FUR[2], lidc=R_FUR[1], white=(232, 232, 236))
    eye(sp, hx + 8.0, hy + 1.5, 4, 4.5, X, (20, 16, 24), (look, 0.0), bl_, (14, 12, 18), R_FUR[2], lidc=R_FUR[1], white=(232, 232, 236))
    brow(sp, hx + 1.5, hy + 5.5, 5, X, +1, R_FUR[0], th=1.2)
    brow(sp, hx + 8.0, hy + 5.5, 4, X, -1, R_FUR[0], th=1.2)
    mo = max(mouth_, X['mo'])
    sp.line((hx + 7, hy - 6.5 - mo * 2), (hx + 13, hy - 6), R_FUR[0])                              # mouth line
    if mo > 0.15:
        mm, _, _ = sp.m_ell(hx + 10, hy - 7 - mo * 1.2, 3.0, 0.6 + mo * 1.8)
        sp.fill(mm, (90, 24, 36))
    sp.rect(hx + 10, hy - 7, hx + 12, hy - 4.5, (250, 244, 200), keep=True)                       # buck teeth
    sp.dot(hx + 10, hy - 5, (200, 190, 150), keep=True)
    # tweed flat cap
    cap = sp.union([sp.m_ell(hx - 1, hy + 6.5, 10.5, 4.5), sp.m_ell(hx + 8, hy + 5, 6.5, 2.2)], R_CAP, dither=0.35)
    sp.fill(cap & CHECK & (((XC + YC).astype(int) % 3) == 0), R_CAP[0])
    sp.line((hx + 4, hy + 4), (hx + 14, hy + 4), R_CAP[0])
    sp.anchors.update(head=(hx, hy), handR=tr, handL=tl)
    if clip_h is not None: sp.clip_below(clip_h)
    sp.outline()


# ======================================================================================== bomb-squad tech (padded suit + helmet)
T_SUIT = [(30, 46, 30), (50, 74, 48), (76, 104, 70), (120, 150, 108)]


def tech(sp, pose='stand', t=0.0, mouth_=0.0, expr='nervous', look=0.0, blink=None, hands=None, props=None, legs=True, clip_h=None,
         breath=True, helmet=True):
    pose = POSE[pose] if isinstance(pose, str) else pose
    X = EXPR.get(expr, EXPR['normal'])
    br = (0.5 * math.sin(t * 2.6)) if breath else 0.0
    hipy = 24.0
    hipL, hipR = (-8.0, hipy), (8.0, hipy)
    G = dict(shL=(-19.0, 56.0 + br), shR=(17.0, 56.0 + br), head=(2.0, 78.0 + br), hip=hipy, rx=20.0, arm=24.0, hrx=13.0, hry=13.0)
    tl, tr, bl, bR = hand_targets(pose, G)
    if hands: tl = hands.get('L', tl); tr = hands.get('R', tr)
    props = props or {}
    hl, al = arm(sp, G['shL'], tl, 13, 12, 6.0, 5.4, T_SUIT, bl, D_GLOVE, 3.8, quilt=True)
    _prop(sp, props.get('L'), hl, al, t)
    if legs:
        (kL, aL), (kR, aR) = legs_for(pose, hipL, hipR, 12.0)
        leg(sp, hipL, kL, aL, 7.0, T_SUIT, D_GLOVE, 12, 7)
        leg(sp, hipR, kR, aR, 7.0, T_SUIT, D_GLOVE, 12, 7)
    tm = sp.sup(0.0, 42.0 + br * 0.5, 21.0, 21.0, T_SUIT, n=2.6)
    sp.fill(tm & (np.abs(YC - (46 + br * 0.5)) < 4) & (np.abs(XC) < 14), (210, 190, 60))                    # chest plate
    text3(sp, 'BOMB', -7, 48 + int(br), (30, 30, 30))
    hx, hy = G['head']
    if helmet:
        hm = sp.ell(hx, hy + 1, 14.5, 14.0, T_SUIT)
        vis = sp.m_poly([(hx - 7, hy + 6), (hx + 14, hy + 6), (hx + 13, hy - 7), (hx - 6, hy - 7)])
        sp.paint(vis, [(20, 30, 50), (40, 60, 90), (70, 110, 150), (160, 210, 240)], np.clip((YC - hy + 7) / 13, 0, 1), olc=(10, 14, 20))
        sp.line((hx - 4, hy + 4), (hx + 1, hy - 4), (220, 240, 255)); sp.line((hx - 2, hy + 4), (hx + 3, hy - 4), (170, 210, 240))
        bl_ = _blink(t, blink)
        eye(sp, hx + 3, hy + 0, 5, 4, X, (60, 50, 40), (look, 0.0), bl_, LASH, (190, 160, 140), white=(170, 180, 200))
        eye(sp, hx + 10, hy + 0, 4, 4, X, (60, 50, 40), (look, 0.0), bl_, LASH, (190, 160, 140), white=(170, 180, 200))
    else:
        face = sp.ell(hx, hy, 11.5, 13.0, T_SKIN)
        sp.rect(hx - 10, hy + 9, hx + 10, hy + 13, (90, 70, 50))
        bl_ = _blink(t, blink)
        eye(sp, hx - 2.5, hy + 1.5, 6, 5.5, X, (60, 50, 40), (look, 0.0), bl_, LASH, T_SKIN[2], lidc=T_SKIN[1])
        eye(sp, hx + 7, hy + 1.5, 5, 5, X, (60, 50, 40), (look, 0.0), bl_, LASH, T_SKIN[2], lidc=T_SKIN[1])
        brow(sp, hx - 2.5, hy + 6, 6, X, +1, (90, 70, 50), th=1.5); brow(sp, hx + 7, hy + 6, 4, X, -1, (90, 70, 50), th=1.5)
        sp.ell(hx + 5, hy - 3, 2.4, 2.6, T_SKIN, olc=T_SKIN[0])
        mouth(sp, hx + 4, hy - 8.5, 7, X, mouth_, (150, 80, 80), skin=T_SKIN[2], maxh=6)
    hr_, ar_ = arm(sp, G['shR'], tr, 13, 12, 6.2, 5.6, T_SUIT, bR, D_GLOVE, 4.0, quilt=True)
    _prop(sp, props.get('R'), hr_, ar_, t)
    sp.anchors.update(head=(hx, hy), handR=hr_, handL=hl)
    if clip_h is not None: sp.clip_below(clip_h)
    sp.outline()


# ======================================================================================== the villain's cat (white, smug, diamond collar)
C_FUR = [(150, 150, 178), (198, 198, 218), (234, 234, 244), (255, 255, 255)]


def cat(sp, pose='sit', t=0.0, mouth_=0.0, expr='smug', look=0.0, blink=None, lid=0.55, tail=0.5, legs=True, clip_h=None, **_):
    X = dict(EXPR.get(expr, EXPR['normal'])); X['lid'] = lid * 0.75; X['eo'] = 1.0
    br = 0.3 * math.sin(t * 2.0)
    # tail curling around the paws
    sw = math.sin(t * 2.3) * tail
    pts = [(-10 - 3 * math.sin(k * 0.4) + k * 0.9, 2 + k * 0.6 + 4 * math.sin(k * 0.35 + sw)) for k in range(16)]
    for a, b in zip(pts[:-1], pts[1:]): sp.cap(a, b, 2.6, 2.6, C_FUR)
    body = sp.union([sp.m_ell(0, 10 + br * 0.3, 10.5, 11.0), sp.m_ell(1, 4, 9.5, 5.0)], C_FUR, dither=0.3)
    for k in range(-8, 9, 3): sp.dot(k, int(20 + br), C_FUR[1])
    for x in (-4, 4): sp.ell(x, 1.6, 3.0, 1.8, C_FUR)                                              # front paws
    hx, hy = 1.0, 26.0 + br
    for ex in (-6.5, 6.5):                                                                         # ears
        ear = sp.m_poly([(hx + ex - 3.5, hy + 5), (hx + ex + 3.5, hy + 5), (hx + ex + ex * 0.15, hy + 12)])
        sp.paint(ear, C_FUR, None)
        sp.fill(ear & erode(ear) & (YC < hy + 10), (240, 160, 176))
    sp.union([sp.m_ell(hx, hy, 10.0, 8.5), sp.m_ell(hx, hy - 3, 11.5, 5.5)], C_FUR, dither=0.28)     # fluffy round face
    bl_ = _blink(t, blink)
    for ex, w in ((-4.2, 6.0), (4.6, 6.0)):
        eye(sp, hx + ex, hy + 1.0, w, 6.5, X, (214, 196, 60), (look, 0.0), bl_, (60, 50, 70), C_FUR[2], lidc=C_FUR[1], slit=True)
    sp.poly([(hx - 1.4, hy - 2.5), (hx + 1.6, hy - 2.5), (hx + 0.1, hy - 4.2)], [(170, 80, 100), (220, 120, 140), (244, 160, 176), (255, 200, 210)])
    sp.line((hx, hy - 4.2), (hx - 1.6, hy - 5.6), (120, 90, 110)); sp.line((hx, hy - 4.2), (hx + 1.6, hy - 5.6), (120, 90, 110))
    for k, dy in enumerate((-3.0, -4.6)):                                                          # whiskers
        sp.line((hx - 4, hy + dy), (hx - 13, hy + dy + 1 - k), (236, 236, 246)); sp.line((hx + 4, hy + dy), (hx + 13, hy + dy + 1 - k), (236, 236, 246))
    sp.cap((hx - 7, hy - 8.5), (hx + 7, hy - 8.5), 1.2, 1.2, [(150, 104, 24), (210, 160, 40), (244, 204, 80), (255, 240, 160)])   # gold collar
    sp.ell(hx + 0.5, hy - 10.6, 1.6, 1.8, [(90, 160, 220), (150, 210, 250), (210, 240, 255), (255, 255, 255)])                    # diamond
    sp.dot(hx, hy - 10, (255, 255, 255), keep=True)
    sp.anchors.update(head=(hx, hy))
    if clip_h is not None: sp.clip_below(clip_h)
    sp.outline()


# ======================================================================================== more hand props (E03–E06)
def p_cards(sp, h, ang, t=0.0):
    """a fan of playing cards"""
    x, y = h
    for k, a in enumerate((-0.5, -0.17, 0.17, 0.5)):
        cx, cy = x + 1 + math.sin(a) * 5, y + 4 + math.cos(a) * 3
        m = sp.m_poly([(cx - 2.6, cy - 4), (cx + 2.6, cy - 4), (cx + 2.6 + a * 2, cy + 4), (cx - 2.6 + a * 2, cy + 4)])
        sp.paint(m, [(170, 170, 176), (220, 220, 226), (250, 250, 250), (255, 255, 255)], None, olc=(60, 60, 70))
        sp.dot(int(cx), int(cy + 1), (214, 40, 50) if k % 2 else (30, 30, 40))


def p_clipboard(sp, h, ang, t=0.0, title='DONE'):
    x, y = h[0] - 1, h[1] - 6
    sp.rect(x - 1, y - 1, x + 18, y + 22, (40, 30, 24))
    sp.rect(x, y, x + 17, y + 21, (150, 110, 70))
    sp.rect(x + 2, y + 2, x + 15, y + 18, (250, 250, 244))
    sp.rect(x + 6, y + 18, x + 11, y + 22, (170, 170, 180))
    text3(sp, title, x + 3, y + 16, (214, 40, 50), keep=True)
    for k in range(3): sp.rect(x + 3, y + 9 - k * 3, x + 14 - (k % 2) * 3, y + 10 - k * 3, (120, 126, 150))


def p_flip(sp, h, ang, t=0.0):
    """old flip phone held at the ear"""
    x, y = h
    sp.rect(x - 2, y - 5, x + 3, y + 8, (60, 64, 80))
    sp.rect(x - 1, y + 1, x + 2, y + 6, (150, 205, 140))
    sp.line((x + 2, y + 8), (x + 3, y + 13), (40, 42, 52))
    sp.dot(x + 3, y + 13, (214, 40, 50))


def p_ketchup(sp, h, ang, t=0.0, squeeze=0.0):
    """red squeeze bottle, cap pointing forward-down"""
    x, y = h
    m = sp.m_poly([(x - 3, y - 6), (x + 3, y - 6), (x + 3.5 + squeeze, y + 6), (x - 3.5 - squeeze, y + 6)])
    sp.paint(m, [(120, 10, 20), (180, 24, 32), (224, 44, 48), (255, 120, 110)], np.clip(0.8 - (XC - x) * 0.05, 0, 1))
    sp.rect(x - 2, y - 9, x + 3, y - 6, (250, 250, 246)); sp.rect(x - 0.5, y - 12, x + 1.5, y - 9, (250, 250, 246))
    sp.rect(x - 2, y - 2, x + 3, y + 2, (250, 250, 246)); sp.dot(x, y, (214, 40, 50))


def p_mustard(sp, h, ang, t=0.0):
    x, y = h
    m = sp.m_poly([(x - 3, y - 6), (x + 3, y - 6), (x + 3, y + 6), (x - 3, y + 6)])
    sp.paint(m, [(150, 110, 10), (210, 170, 20), (246, 214, 50), (255, 244, 140)], np.clip(0.8 - (XC - x) * 0.05, 0, 1))
    sp.rect(x - 1, y + 6, x + 2, y + 10, (246, 214, 50))


def p_dog(sp, h, ang, t=0.0, bites=0):
    """Chicago-style hot dog: poppy-seed bun, green relish, onions, tomato wedges, pickle spear, sport peppers, mustard"""
    x, y = h[0] + 2, h[1]
    e = 9 - 4 * bites
    if e < -8: return
    bun = [(150, 96, 40), (204, 146, 70), (236, 186, 104), (252, 222, 150)]
    sp.cap((x - 8, y - 1), (x + e, y - 1), 2.6, 2.6, bun)
    for k in range(-7, e, 3): sp.dot(k + x, int(y + 1), (40, 30, 30))
    sp.cap((x - 9, y + 2.0), (x + e + 1, y + 2.0), 1.6, 1.6, [(120, 40, 30), (170, 60, 44), (206, 90, 64), (236, 140, 110)])     # sausage
    sp.cap((x - 7, y + 3.4), (x + e - 1, y + 3.4), 0.9, 0.9, [(150, 130, 10), (214, 190, 20), (246, 222, 60), (255, 246, 150)])   # mustard
    for k in range(-6, e - 1, 3):
        sp.dot(x + k, int(y + 4.5), (40, 220, 80)); sp.dot(x + k + 1, int(y + 4.5), (250, 250, 240))
    sp.cap((x - 6, y + 5.5), (x + e - 3, y + 6.0), 0.8, 0.8, [(30, 90, 30), (50, 140, 50), (80, 180, 70), (140, 220, 120)])     # pickle spear
    if e > 0: sp.ell(x + e - 2, y + 5.2, 1.4, 1.0, [(160, 30, 30), (210, 50, 44), (240, 90, 80), (255, 160, 150)])               # tomato


def p_fries(sp, h, ang, t=0.0):
    x, y = h
    for k in range(5): sp.rect(x - 4 + k * 2, y + 3, x - 3 + k * 2, y + 9 + (k % 2) * 2, (246, 204, 80))
    m = sp.m_poly([(x - 5, y + 4), (x + 6, y + 4), (x + 5, y - 5), (x - 4, y - 5)])
    sp.paint(m, [(140, 20, 24), (200, 36, 40), (232, 60, 60), (255, 130, 120)], None)
    sp.rect(x - 2, y - 2, x + 3, y + 2, (255, 214, 60))


PROPS.update(cards=p_cards, clipboard=p_clipboard, flip=p_flip, ketchup=p_ketchup, mustard=p_mustard, dog=p_dog, fries=p_fries)


# ======================================================================================== BEA (311 operator, at her console)
BEA_SKIN = [(96, 58, 44), (140, 88, 64), (176, 118, 86), (206, 154, 118)]
BEA_HAIR = [(14, 10, 14), (30, 22, 26), (52, 40, 44), (86, 70, 72)]
BEA_CARD = [(90, 70, 130), (130, 104, 176), (166, 140, 210), (206, 186, 240)]


def bea(sp, pose='hold', t=0.0, mouth_=0.0, expr='deadpan', look=0.0, blink=None, hands=None, props=None, legs=False, clip_h=None,
        breath=True, gum=0.0, **_):
    pose = POSE[pose] if isinstance(pose, str) else pose
    X = EXPR.get(expr, EXPR['normal'])
    br = (0.4 * math.sin(t * 1.8)) if breath else 0.0
    G = dict(shL=(-14.0, 46.0 + br), shR=(12.0, 46.0 + br), head=(2.0, 66.0 + br), hip=16.0, rx=16.0, arm=21.0, hrx=12.0, hry=13.0)
    tl, tr, bl, bR = hand_targets(pose, G)
    if pose.get('name') == 'hold': tl, tr, bl, bR = (-2.0, 30.0), (12.0, 31.0), 1, 1
    if hands: tl = hands.get('L', tl); tr = hands.get('R', tr)
    props = props or {}
    hl, al = arm(sp, G['shL'], tl, 11, 11, 4.2, 3.6, BEA_CARD, bl, BEA_SKIN, 2.8)
    sp.cap((1.0, 38 + br), (2.0, 54 + br), 3.8, 3.6, BEA_SKIN)                                              # neck
    tm = sp.sup(0.0, 30.0 + br * 0.5, 16.0, 17.5, BEA_CARD, n=2.2)
    sp.fill(tm & CHECK & ((YC.astype(int) % 4) == 0), BEA_CARD[1])
    polo = sp.m_poly([(-5, 48.5 + br), (9, 48.5 + br), (2, 34 + br)])
    sp.paint(polo, [(20, 90, 110), (30, 130, 150), (50, 170, 186), (120, 220, 230)], None)
    sp.rect(-11, 38 + int(br), -2, 43 + int(br), (250, 250, 244)); text3(sp, '311', -10, 42 + int(br), (214, 40, 50), keep=True)
    hx, hy = G['head']
    sp.ell(hx - 2, hy + 2, 13.5, 13.0, BEA_HAIR, dither=0.3)                                                # hair behind
    face = sp.union([sp.m_ell(hx, hy, 11.5, 12.5), sp.m_ell(hx + 1.5, hy - 6, 10.5, 7.0)], BEA_SKIN)
    sp.ell(hx - 10.5, hy - 1, 2.4, 3.4, BEA_SKIN)
    ring = sp.m_ell(hx - 10.5, hy - 6.5, 2.6, 3.2)[0]; sp.fill(ring & ~erode(ring), (246, 200, 60))         # gold hoop earring
    bl_ = _blink(t, blink)
    X2 = dict(X); X2['lid'] = min(0.42, max(X.get('lid', 0.0), 0.26)); X2['eo'] = max(X['eo'], 1.1) if not X.get('shut') else X['eo']   # bored lids, eyes open
    eye(sp, hx - 2.5, hy + 1.0, 7, 6, X2, (70, 44, 30), (look, 0.0), bl_, LASH, BEA_SKIN[2], lidc=BEA_SKIN[1], flick=True, bold=2)
    eye(sp, hx + 7.0, hy + 1.0, 6, 5.5, X2, (70, 44, 30), (look, 0.0), bl_, LASH, BEA_SKIN[2], lidc=BEA_SKIN[1], bold=2)
    sp.line((hx - 6.5, hy + 3), (hx - 8.5, hy + 4.5), LASH)                                                 # winged liner
    brow(sp, hx - 2.5, hy + 6.5, 7, X, +1, BEA_HAIR[0], th=1.4, arch=1.6)
    brow(sp, hx + 7.0, hy + 6.5, 5, X, -1, BEA_HAIR[0], th=1.4, arch=1.4)
    sp.ell(hx + 4.5, hy - 3.5, 2.6, 2.6, BEA_SKIN, olc=BEA_SKIN[0]); sp.dot(hx + 3, hy - 2, BEA_SKIN[3])
    mouth(sp, hx + 3.5, hy - 8.5, 7, X, mouth_, (150, 50, 80), skin=BEA_SKIN[2], maxh=6)
    if gum > 0.05:                                                                                          # pink bubble
        r = 1.5 + 5.0 * gum
        sp.ell(hx + 4.5 + r * 0.4, hy - 8.5, r, r, [(200, 80, 130), (240, 120, 170), (255, 170, 210), (255, 230, 246)])
    hair_cloud(sp, hx - 1, hy + 5, 12.5, 8.0, BEA_HAIR, a0=-0.05, a1=math.pi + 0.15, r=2.8, n=12, inner=False, seed=4)
    bun = sp.union([sp.m_ell(hx - 2, hy + 16, 6.5, 5.5), sp.m_ell(hx + 1, hy + 18, 5, 4.5)], BEA_HAIR, dither=0.3)
    sp.line((hx - 9, hy + 14), (hx + 7, hy + 21), (246, 200, 60), 1); sp.dot(hx + 7, hy + 21, (250, 140, 160))   # pencil in the bun
    sp.line((hx - 12, hy + 2), (hx - 8, hy + 14), (40, 40, 48), 2)                                         # headset band
    sp.ell(hx - 11.5, hy + 0.5, 2.4, 3.2, [(20, 20, 26), (40, 40, 50), (64, 64, 78), (100, 100, 120)])
    sp.line((hx - 10, hy - 2), (hx - 3, hy - 8), (40, 40, 48)); sp.ell(hx - 2.5, hy - 8.5, 1.2, 1.0, [(20, 20, 26)] * 3 + [(90, 90, 100)], ol=False)
    hr_, ar_ = arm(sp, G['shR'], tr, 11, 11, 4.4, 3.8, BEA_CARD, bR, BEA_SKIN, 2.9)
    for k in range(3): sp.dot(int(hr_[0] + 2 + k), int(hr_[1] + 2), (214, 40, 120))                         # long nails
    _prop(sp, props.get('R'), hr_, ar_, t)
    sp.anchors.update(head=(hx, hy), handR=hr_, handL=hl)
    if clip_h is not None: sp.clip_below(clip_h)
    sp.outline()


# ======================================================================================== WORKER (Streets crew foreman)
W_SKIN = [(150, 86, 70), (198, 128, 104), (230, 168, 138), (248, 204, 176)]
W_VEST = [(150, 50, 10), (210, 84, 16), (250, 124, 30), (255, 186, 90)]
W_FLAN = [(90, 20, 24), (140, 34, 36), (180, 54, 50), (220, 100, 90)]
W_BEARD = [(110, 104, 100), (150, 144, 140), (190, 186, 182), (226, 224, 222)]
W_HAT = [(150, 110, 10), (210, 170, 20), (246, 210, 50), (255, 244, 150)]
W_JEANS = [(30, 44, 80), (44, 64, 110), (62, 90, 146), (100, 130, 186)]


def worker(sp, pose='stand', t=0.0, mouth_=0.0, expr='deadpan', look=0.0, blink=None, hands=None, props=None, legs=True, clip_h=None,
           breath=True, **_):
    pose = POSE[pose] if isinstance(pose, str) else pose
    X = EXPR.get(expr, EXPR['normal'])
    br = (0.6 * math.sin(t * 1.9)) if breath else 0.0
    hipy = 24.0
    hipL, hipR = (-8.0, hipy), (8.0, hipy)
    G = dict(shL=(-19.0, 56.0 + br), shR=(17.0, 56.0 + br), head=(3.0, 78.0 + br), hip=hipy, rx=21.0, arm=25.0, hrx=13.0, hry=13.0)
    tl, tr, bl, bR = hand_targets(pose, G)
    if hands: tl = hands.get('L', tl); tr = hands.get('R', tr)
    props = props or {}
    hl, al = arm(sp, G['shL'], tl, 13, 12, 5.0, 4.4, W_FLAN, bl, [(90, 70, 40), (140, 110, 60), (180, 150, 90), (210, 190, 130)], 3.6)
    _prop(sp, props.get('L'), hl, al, t)
    if legs:
        (kL, aL), (kR, aR) = legs_for(pose, hipL, hipR, 12.0)
        boot = [(60, 40, 24), (100, 70, 40), (140, 100, 60), (180, 140, 90)]
        leg(sp, hipL, kL, aL, 6.4, W_JEANS, boot, 12, 7)
        leg(sp, hipR, kR, aR, 6.4, W_JEANS, boot, 12, 7)
    sp.cap((1.5, 58 + br), (2.5, 68 + br), 6.0, 6.0, W_SKIN)                                                  # thick neck
    tm = sp.sup(0.0, 40.0 + br * 0.5, 21.0, 19.5, W_FLAN, n=2.3)
    sp.fill(tm & (((XC.astype(int) // 3) + (YC.astype(int) // 3)) % 2 == 0), W_FLAN[1])                      # flannel check
    vest = sp.m_poly([(-20, 56 + br), (-5, 58 + br), (2, 40), (9, 58 + br), (19, 56 + br), (20, 24), (-21, 24)])
    vest &= tm
    sp.paint(vest, W_VEST, np.clip((YC - 22) / 38 * 0.6 + 0.2, 0, 1))
    sp.fill(vest & ((np.abs(YC - 36) < 1.2) | (np.abs(YC - 44) < 1.2)), (214, 220, 230))                     # reflective stripes
    text3(sp, 'STREETS', -16, 31, (30, 30, 30))
    hx, hy = G['head']
    face = sp.union([sp.m_ell(hx, hy, 13.0, 13.0), sp.m_ell(hx + 2, hy - 7, 12.0, 8.0)], W_SKIN)
    sp.ell(hx - 12.5, hy, 2.6, 3.6, W_SKIN)
    beard_m = sp.union([sp.m_ell(hx + 2.5, hy - 10.0, 12.5, 7.5), sp.m_ell(hx - 6, hy - 5, 4.5, 5)], W_BEARD, dither=0.3,
                       exclude=sp.m_ell(hx + 4.5, hy - 7.5, 4.6, 2.6 + mouth_ * 2.5 + X['mo'] * 2)[0])
    for k in range(-8, 13, 3): sp.dot(hx + k, int(hy - 12 - (k % 2)), W_BEARD[0])
    bl_ = _blink(t, blink)
    X2 = dict(X); X2['lid'] = min(0.4, max(X.get('lid', 0.0), 0.25)); X2['eo'] = max(X['eo'], 0.95) if not X.get('shut') else X['eo']
    eye(sp, hx - 2.5, hy + 1.5, 6.5, 5.5, X2, (90, 110, 120), (look, 0.0), bl_, LASH, W_SKIN[2], lidc=W_SKIN[1], bag=W_SKIN[1])
    eye(sp, hx + 7.0, hy + 1.5, 5.5, 5.0, X2, (90, 110, 120), (look, 0.0), bl_, LASH, W_SKIN[2], lidc=W_SKIN[1], bag=W_SKIN[1])
    brow(sp, hx - 2.5, hy + 6.0, 7, X, +1, W_BEARD[0], th=2.2, bushy=True)
    brow(sp, hx + 7.0, hy + 6.0, 5, X, -1, W_BEARD[0], th=2.2, bushy=True)
    sp.ell(hx + 6.0, hy - 2.5, 3.6, 3.2, [(150, 60, 60), (200, 96, 90), (232, 136, 122), (250, 180, 164)])   # red nose
    mouth(sp, hx + 4.5, hy - 7.5, 6, X, mouth_, (120, 50, 50), skin=W_SKIN[2], maxh=5)
    sp.line((hx + 7, hy - 7.5), (hx + 13, hy - 6), (230, 200, 140))                                         # toothpick
    hat = sp.union([sp.m_ell(hx - 0.5, hy + 12, 13.5, 8.0), sp.m_ell(hx + 1, hy + 8.8, 16.0, 2.4)], W_HAT)
    sp.fill(hat & (np.abs(XC - hx) < 1.0) & (YC > hy + 10), W_HAT[3])
    hr_, ar_ = arm(sp, G['shR'], tr, 13, 12, 5.2, 4.6, W_FLAN, bR, [(90, 70, 40), (140, 110, 60), (180, 150, 90), (210, 190, 130)], 3.8)
    _prop(sp, props.get('R'), hr_, ar_, t)
    sp.anchors.update(head=(hx, hy), handR=hr_, handL=hl)
    if clip_h is not None: sp.clip_below(clip_h)
    sp.outline()


def driver(fn, car_x, car_y, car_un, dx, flip=False, h=9.6, size=3.6, **P):
    """a sprite hero seen through a car window (vehicle props in chi_props are ~30 units long, windows at 7.6–11.8 units)"""
    sp = Spr(); fn(sp, **P)
    hy = sp.anchors['head'][1]
    head_px = 34.0
    un_act = 4.0 * size * car_un / head_px
    clip = hy - 2.0 * car_un / (size * car_un / head_px)
    from props.dibspix import Act
    return Act(fn, car_x + dx * car_un * (-1 if flip else 1), car_y - h * car_un, un=un_act, flip=flip, pin='head', clip_h=clip, **P)
