"""«Мазутыч» cast in the «Мазутная гравюра» manner (props/mazpix.py): Мазутыч (+ monowheel «Дин-Дон», car steering wheel),
Зоя in the gas-station window, the tanker truck, queue cars (Lada «six», UAZ «loaf»), wheel display.
Coordinates: sprite px, feet anchor at the origin, +x = facing side, y up. Every draw fn takes the Spr first."""
import math
import numpy as np
from props import dibspix as DX
from props import mazpix as MX
from props.mazpix import INK, tones, stroke, hatch_fill
from props.dibspix import EXPR, ik, dark, mix, erode, dilate

SKIN = (206, 146, 108)
ROBE = (238, 112, 30)
ROBE_D = (206, 88, 28)
STRIPE = (214, 222, 218)
RUBBER = (52, 58, 50)
MUST = (56, 40, 32)
HELMET = (236, 234, 222)
GLOVE = (200, 188, 140)
FUR = (206, 156, 96)
HS = 1.38                       # head scale: caricature, the head is a third of the figure


XTRA = dict(bored=dict(eo=0.85, pu=0.55, bt=0.05, bl=0.1, mo=0.0, mc=-0.1, lid=0.32),
            awe=dict(eo=1.3, pu=0.75, bt=-0.5, bl=0.7, mo=0.3, mc=0.1, round_mouth=True),
            strain=dict(eo=0.35, pu=0.5, bt=0.9, bl=-0.3, mo=0.35, mc=-0.5, lid=0.45),
            proud=dict(eo=0.85, pu=0.6, bt=0.2, bl=0.3, mo=0.0, mc=0.6, lid=0.25),
            joy=dict(eo=1.2, pu=0.8, bt=-0.6, bl=0.7, mo=0.4, mc=0.6, tears=True))


def X(expr):
    e = dict(XTRA.get(expr) or EXPR.get(expr, EXPR['normal']))
    return e


# ======================================================================================== the monowheel «Дин-Дон 3000»
def monowheel(sp, t=0.0, spin=0.0, led=True, face='smile', ax=2.0, ay=11.0, dead=False):
    """electric unicycle seen from the side: tyre, shell with LED arc, pedals; face on the little top display"""
    sp.ell(ax, ay, 9.0, 11.0, tones((40, 40, 46)))
    tyre = sp.m_ell(ax, ay, 9.0, 11.0)[0] & ~sp.m_ell(ax, ay, 7.4, 9.4)[0]
    ang = np.arctan2(DX.YC - ay, DX.XC - ax)
    tread = (np.floor((ang + spin) / (2 * math.pi) * 22) % 2) == 0
    sp.fill(tyre & tread, (24, 22, 26))
    sp.ell(ax, ay + 0.6, 6.6, 8.6, tones((86, 92, 104)))
    if led and not dead:
        arc = sp.m_ell(ax, ay + 0.6, 5.4, 7.4)[0] & ~sp.m_ell(ax, ay + 0.6, 4.4, 6.4)[0] & (DX.YC > ay + 1)
        pulse = 0.75 + 0.25 * math.sin(t * 9)
        sp.fill(arc, (int(80 * pulse), int(230 * pulse), 255), keep=True)
    sp.rect(ax - 1.5, ay + 0.2, ax + 1.5, ay + 1.6, INK)                     # hub slot
    for px_ in (-1, 1):                                                       # pedals
        sp.rect(ax + px_ * 3 - 3, ay + 1, ax + px_ * 3 + 4, ay + 2.2, (60, 60, 64))
    # display on the top of the shell
    sp.rect(ax - 3, ay + 7.6, ax + 4, ay + 11.6, INK)
    scr = (14, 26, 30) if dead else (20, 60, 70)
    sp.rect(ax - 2, ay + 8.4, ax + 3, ay + 10.8, scr)
    if not dead:
        c = (120, 255, 240) if face != 'low' else (255, 90, 70)
        sp.dot(ax - 1, ay + 9.8, c); sp.dot(ax + 1, ay + 9.8, c)
        if face == 'low': sp.dot(ax, ay + 8.6, c)
        else: sp.dot(ax - 1, ay + 8.6, c); sp.dot(ax, ay + 8.4, c); sp.dot(ax + 1, ay + 8.6, c)
    sp.anchors['wheel'] = (ax, ay)


# ======================================================================================== the Lada steering wheel with a fur cover
def steering(sp, cx, cy, steer=0.0, rx=5.6, ry=11.5):
    m, nx, ny = sp.m_ell(cx, cy, rx, ry)
    ring = m & ~sp.m_ell(cx, cy, rx - 1.5, ry - 1.9)[0]
    sp.paint(ring, tones(FUR), DX.lit(nx, ny))
    fur = ((np.floor(DX.XC * 2) + np.floor(DX.YC)) % 2 == 0)
    sp.fill(ring & fur & (DX.YC < cy) & erode(ring), dark(FUR, 0.62))
    for k in range(3):                                                        # three spokes, rotate with steer
        a = steer + k * 2 * math.pi / 3 - math.pi / 2
        sp.line((cx, cy), (cx + math.cos(a) * (rx - 1.2), cy + math.sin(a) * (ry - 1.6)), (40, 38, 40), 1)
    sp.ell(cx, cy, 1.4, 2.2, tones((54, 52, 58)))
    sp.dot(cx, cy, (220, 200, 120))                                           # the little boat logo


def glove(sp, x, y, flat=False):
    sp.ell(x, y, 2.9, 2.5, tones(GLOVE))
    sp.line((x - 1.2, y + 1.6), (x + 1.4, y + 1.6), dark(GLOVE, 0.6))
    if not flat: sp.dot(x + 1.6, y - 0.6, dark(GLOVE, 0.6))


# ======================================================================================== МАЗУТЫЧ
def maz(sp, t=0.0, expr='deadpan', mouth_=0.0, ride=True, spin=0.0, wind=0.0, steer=0.0, blinker=0.0, look=(0.6, 0.0),
        wheel_face='smile', dead=False, beacon=False, confetti=0, soot=0.0, blink=None, wheel=True, hold=True, lean_head=0.0,
        far_hold=True, card=False, pull=False, walk=0.0, sweat=0.0, bottle=False):
    """Мазутыч, 3/4 to the right. ride: standing on the monowheel (feet on the pedals at y 13); wind: mustache flutter 0..1;
    steer: steering-wheel angle; blinker 0..1: the near arm sticks out and flaps (a mouth-clicked turn signal);
    card: holds up the refinery pass «НПЗ»; pull: walking and hauling a rope over the near shoulder (walk = gait phase);
    sweat 0..1: drops of effort"""
    E = X(expr)
    if blink is None: blink = (t % 3.7) < 0.12
    B = 13.0 if ride else 0.0
    if pull: ride, hold, far_hold = False, False, False
    sw = math.sin(walk) * 3.0 if pull else 0.0                                # gait: boots swing
    lf, ln = max(0.0, math.sin(walk)) * 1.5 if pull else 0.0, max(0.0, -math.sin(walk)) * 1.5 if pull else 0.0
    br = 0.6 * math.sin(t * 2.2)                                              # breathing
    # ---------------------------------------------------------------- far boot + leg
    sp.sup(-2.0 - sw, B + 6.0 + lf, 4.0, 6.0, tones(dark(RUBBER, 0.8)), n=2.4)
    sp.ell(1.0 - sw, B + 2.2 + lf, 5.0, 2.4, tones(dark(RUBBER, 0.8)))
    sp.cap((-2.0 - sw, B + 11.0 + lf), (-0.5, B + 24.0), 3.6, 4.0, tones(ROBE_D))
    if ride and wheel:
        monowheel(sp, t, spin, face=wheel_face, dead=dead)
    # ---------------------------------------------------------------- far arm (behind the torso)
    shF = (0.5, B + 57.0 + br * 0.4)
    wc = (32.0, B + 45.5)                                                     # steering wheel centre
    hF = (wc[0] - 2.0 + 3.0 * math.sin(steer), wc[1] + 10.0 - 1.5 * abs(math.sin(steer))) if far_hold else (8.0, B + 30.0)
    if pull: hF = (13.0, B + 50.0)
    kF, eF = ik(shF, hF, 12.0, 11.5, -1.0)
    sp.cap(shF, kF, 3.4, 3.0, tones(ROBE_D)); sp.cap(kF, eF, 3.0, 2.6, tones(ROBE_D))
    glove(sp, *eF)
    # ---------------------------------------------------------------- near leg + boot
    sp.cap((5.0 + sw, B + 11.0 + ln), (3.5, B + 24.0), 3.8, 4.2, tones(ROBE))
    sp.sup(5.0 + sw, B + 6.0 + ln, 4.2, 6.0, tones(RUBBER), n=2.4)
    sp.ell(8.2 + sw, B + 2.2 + ln, 5.4, 2.6, tones(RUBBER))
    sp.line((1.5 + sw, B + 10.0 + ln), (8.5 + sw, B + 10.0 + ln), (90, 100, 86))   # boot rim
    # ---------------------------------------------------------------- torso: long hunched «poker»
    parts = [sp.m_ell(1.5, B + 29.0, 12.5, 8.5), sp.m_ell(3.0, B + 44.0 + br * 0.3, 13.0, 14.0), sp.m_ell(5.5, B + 56.0 + br * 0.5, 12.0, 7.5)]
    tm = sp.union(parts, tones(ROBE))
    for y0 in (B + 33.0, B + 39.5):                                           # reflective stripes
        band = tm & (DX.YC >= y0) & (DX.YC < y0 + 2.4) & erode(tm)
        sp.fill(band, STRIPE)
        sp.fill(band & (DX.XC > 8), (255, 255, 246))
        sp.fill(band & (DX.XC < -6), dark(STRIPE, 0.7))
    sp.line((9.0, B + 24.0), (11.5, B + 61.0), INK)                           # zipper
    sp.rect(12.0, B + 47.0, 16.0, B + 51.0, ROBE_D); sp.line((12, B + 51.0), (16, B + 51.0), INK)   # chest pocket
    sp.rect(13.0, B + 50.0, 14.0, B + 54.0, (60, 90, 200))                    # pen
    stroke(sp, [(-8.0, B + 28.0), (-4.0, B + 26.0)]); stroke(sp, [(-6.0, B + 49.0), (-2.0, B + 46.0)])   # robe creases
    sp.rect(6.0, B + 60.0, 16.0, B + 63.0, ROBE_D)                            # collar
    # ---------------------------------------------------------------- neck + head (big caricature «horse» face, pushed forward)
    hs = HS
    hx, hy = 15.0 + lean_head, B + 64.0 + 13.0 * hs
    def Hp(dx, dy): return (hx + dx * hs, hy + dy * hs)
    sp.cap((9.0, B + 59.0), (12.0 + lean_head * 0.6, B + 70.0), 4.4, 4.4, tones(SKIN))
    sp.ell(*Hp(-9.0, 1.0), 3.0 * hs, 4.6 * hs, tones(SKIN))                    # far ear
    sp.line(Hp(-9.6, 2.0), Hp(-9.0, -1.0), dark(SKIN, 0.6))
    face = sp.union([sp.m_ell(*Hp(0, 0), 10.5 * hs, 13.0 * hs, -0.10), sp.m_ell(*Hp(3.0, -8.0), 8.0 * hs, 6.5 * hs, -0.2)], tones(SKIN))
    # stubble + cheek hatch + wrinkles
    rng = np.random.default_rng(3)
    stub = face & (DX.YC < hy - 4.0 * hs) & erode(face) & (rng.random(face.shape) < 0.5) & DX.CHECK
    sp.fill(stub, (150, 110, 92))
    hatch_fill(sp, face & erode(face) & (DX.XC < hx - 5.0 * hs) & (DX.YC < hy + 3 * hs), dark(SKIN, 0.62), 3)
    stroke(sp, [Hp(2.5, -1.0), Hp(1.5, -5.0), Hp(2.0, -8.0)], dark(SKIN, 0.55))      # nasolabial fold
    sp.line(Hp(-7.0, 3.5), Hp(-5.5, 4.0), dark(SKIN, 0.6))
    sp.line(Hp(-7.0, 2.6), Hp(-5.0, -1.5), (150, 150, 150))                    # grey sideburn
    sp.line(Hp(-6.4, 3.0), Hp(-4.6, -1.0), (180, 176, 170))
    # eyes, mono-brow
    lx, ly = look
    DX.eye(sp, *Hp(4.5, 3.0), 6.0 * hs, 5.0 * hs, E, (96, 128, 150), (lx, ly), blink, lash=INK, skin=SKIN, bag=dark(SKIN, 0.68), bold=1)
    DX.eye(sp, *Hp(-3.5, 3.0), 4.4 * hs, 4.6 * hs, E, (96, 128, 150), (lx, ly), blink, lash=INK, skin=SKIN, bag=dark(SKIN, 0.68))
    bcol = (54, 40, 34)
    DX.brow(sp, *Hp(4.5, 7.0), 7.0 * hs, E, +1, bcol, th=3, bushy=True)
    DX.brow(sp, *Hp(-3.5, 7.0), 5.0 * hs, E, -1, bcol, th=3, bushy=True)
    by_ = 7.0 + E['bl'] * 1.8 - 1.2 * E['bt']
    sp.rect(*Hp(-0.8, by_ - 0.6), *Hp(1.8, by_ + 1.2), bcol)                   # the bridge: mono-brow
    sp.line(Hp(-3.0, 10.5), Hp(3.0, 10.8), dark(SKIN, 0.6))                    # forehead wrinkles
    sp.line(Hp(-1.0, 11.8), Hp(5.0, 12.0), dark(SKIN, 0.6))
    # mouth (under the mustache), gold tooth
    mo = max(mouth_, E['mo'])
    mx, my = Hp(7.0, -10.2)
    if mo > 0.10:
        DX.mouth(sp, mx, my, 7.0 * hs, E, mouth_, INK, skin=SKIN, maxh=5 * hs)
        sp.dot(mx + 1, my - 0.4 + 0.2 * mo, (250, 206, 60), keep=True); sp.dot(mx + 1, my + 0.6, (255, 236, 130), keep=True)
    # potato nose with veins
    nx_, ny_ = Hp(9.0, -2.2)
    sp.ell(nx_, ny_, 5.2 * hs, 4.4 * hs, tones((204, 112, 92)))
    sp.dot(nx_ - 1.0, ny_ - 0.8, (130, 110, 176)); sp.dot(nx_ + 1.4, ny_ + 1.2, (130, 110, 176)); sp.dot(nx_ - 2.4, ny_ + 1.0, (150, 100, 150))
    sp.dot(nx_ + 0.4, ny_ + 1.6, (156, 96, 170)); sp.dot(nx_ + 3.0, ny_ - 3.2, INK)       # nostril
    # the mustache brush: lifts when he talks, flutters in the wind
    lift = 1.0 * min(1.0, mo * 1.6) * hs
    fl = wind * math.sin(t * 31.0) * hs
    mparts = [sp.m_ell(*Hp(3.5, -6.6 + lift / hs), 5.5 * hs, 3.2 * hs, 0.2), sp.m_ell(*Hp(10.0, -6.8 + lift / hs), 6.6 * hs, 3.4 * hs, -0.15),
              sp.m_ell(hx + (15.5 + 1.5 * wind) * hs, hy + (-8.0) * hs + lift + fl, (3.6 + 1.2 * wind) * hs, 2.6 * hs, -0.5 + 0.4 * wind)]
    mm = sp.union(mparts, tones(MUST), flat=-0.05)
    hr = np.random.default_rng(11)
    for k in range(7):                                                        # a few grey hairs, irregular
        x = hx + (hr.random() * 18 + 1.0) * hs; y0 = hy + (-5.0 - hr.random() * 2.0) * hs + lift
        sp.line((x, y0), (x + 0.8 + wind * 2, y0 - 2.0 * hs), (140, 128, 116))
    sp.fill(mm & ~erode(mm), INK)
    if wind > 0.3:                                                            # loose hairs streaming back
        for k in range(3):
            y = hy - (6.0 + k * 1.3) * hs + lift
            sp.line((hx + 1.0 * hs, y), (hx - (3.0 + 3 * wind) * hs, y + fl * 0.6 + 0.6 * k), MUST)
    # ---------------------------------------------------------------- the hard hat (+ jam-jar beacon)
    hcx, hcy = Hp(0.5, 13.0)
    hm = sp.m_ell(hcx, hcy, 12.0 * hs, 8.0 * hs, -0.12)[0] & (DX.YC > hy + 10.0 * hs + (DX.XC - hx) * 0.12)
    sp.paint(hm, tones(HELMET), DX.lit(np.clip((DX.XC - hcx) / (12 * hs), -1, 1), np.clip((DX.YC - hcy) / (8 * hs), -1, 1)))
    sp.ell(*Hp(1.5, 10.5), 14.5 * hs, 2.2 * hs, tones(HELMET), ang=-0.12)
    sp.line(Hp(0.5, 20.5), Hp(1.5, 11.5), dark(HELMET, 0.7))                   # ridge
    bj = Hp(-1.0, 20.0)
    on = beacon and int(t * 6) % 2 == 0
    q = hs
    sp.rect(bj[0] - 2.5 * q, bj[1], bj[0] + 2.5 * q, bj[1] + 5.0 * q, (90, 160, 255) if on else (54, 96, 200))
    sp.rect(bj[0] - 2.5 * q, bj[1], bj[0] - 1.2 * q, bj[1] + 5.0 * q, (150, 200, 255) if on else (90, 140, 230))
    sp.rect(bj[0] - 3.0 * q, bj[1] + 5.0 * q, bj[0] + 3.0 * q, bj[1] + 6.2 * q, (150, 150, 146))     # lid
    sp.rect(bj[0] - 4.0 * q, bj[1] + 1.0 * q, bj[0] + 4.0 * q, bj[1] + 2.4 * q, (176, 176, 168))     # duct tape
    sp.line((bj[0] - 2.5 * q, bj[1]), (bj[0] - 2.5 * q, bj[1] + 5 * q), INK); sp.line((bj[0] + 2.5 * q, bj[1]), (bj[0] + 2.5 * q, bj[1] + 5 * q), INK)
    sp.anchors['head'] = Hp(3.0, 0.0)
    sp.anchors['eyes'] = Hp(1.0, 3.0)
    sp.anchors['beacon'] = (bj[0], bj[1] + 3.0 * q)
    sp.anchors['helmet'] = (hcx, hcy)
    sp.anchors['belt'] = (-10.0, B + 28.0)
    sp.anchors['shoulder'] = (9.0, B + 58.0)
    if sweat > 0:                                                             # drops of effort fly off the forehead
        for k in range(3):
            ph = (t * 2.2 + k * 0.33) % 1.0
            dx_, dy_ = Hp(-6.0 - 10 * ph - 3 * k, 9.0 + 4 * ph - 6 * ph * ph)
            if ph < 0.8 * sweat + 0.2:
                sp.ell(dx_, dy_, 1.2 * hs, 1.7 * hs, tones((150, 210, 255)), ol=True)
    # ---------------------------------------------------------------- steering wheel + near arm
    sp.outline(INK, 2)                                                        # the double ink line goes around the body before the wheel
    before = sp.m.copy()
    shN = (9.0, B + 56.0 + br * 0.4)
    if hold:
        steering(sp, *wc, steer=steer)
    if bottle:                                                                # sniffing a bottle like a sommelier
        hN = (shN[0] + 15.0, shN[1] + 12.0)
    elif card:                                                                # the refinery pass held up proudly
        hN = (shN[0] + 17.0, shN[1] + 1.0)
    elif pull:
        hN = (shN[0] + 7.0, shN[1] - 3.0)
    elif blinker > 0:                                                         # near arm out to the side, hand flaps: «щёлк-щёлк»
        flap = math.sin(t * 22.0) * 2.0 * blinker
        hN = (shN[0] + 21.0 * blinker + 4.0, shN[1] + 3.0 + flap)
    else:
        hN = (wc[0] + 1.5 - 3.0 * math.sin(steer), wc[1] + 10.0 + 1.0 * math.sin(steer))
    kN, eN = ik(shN, hN, 12.0, 11.5, -1.0)
    sp.cap(shN, kN, 3.6, 3.2, tones(ROBE)); sp.cap(kN, eN, 3.2, 2.8, tones(ROBE))
    sp.fill(sp.m_cap(kN, eN, 3.2, 2.8)[0] & (np.abs(DX.YC - (kN[1] + eN[1]) / 2) < 1.0), STRIPE)   # sleeve stripe
    glove(sp, *eN, flat=blinker > 0)
    sp.anchors['hand'] = eN
    if bottle:                                                                # a «Родниковая» bottle of gasoline under the nose
        bottle_prop(sp, eN[0] + 1.0, eN[1] - 2.0, 1.2)
        sp.ell(eN[0], eN[1] + 0.5, 2.0, 1.8, tones(GLOVE))
    if card == 'talon':                                                      # the fuel coupon: pink paper with a red stamp
        cx_, cy_ = eN[0] + 1.0, eN[1] + 3.0
        sp.rect(cx_ - 8, cy_, cx_ + 8, cy_ + 10, (250, 214, 214)); sp.rect(cx_ - 8, cy_ + 8, cx_ + 8, cy_ + 10, (220, 120, 140))
        sp.ptext('10Л', cx_ - 0.5, cy_ + 7.0, (180, 30, 40), size=4, center=True)
        sp.ell(cx_ + 4.5, cy_ + 2.5, 2.0, 2.0, tones((200, 40, 60)), ol=False)
    elif card:
        cx_, cy_ = eN[0] + 1.0, eN[1] + 3.0
        sp.rect(cx_ - 7, cy_, cx_ + 7, cy_ + 10, (246, 244, 236)); sp.rect(cx_ - 7, cy_ + 7, cx_ + 7, cy_ + 10, (200, 40, 40))
        sp.rect(cx_ - 6, cy_ + 1, cx_ - 2, cy_ + 6, (120, 150, 190))
        sp.ptext('НПЗ', cx_ - 1.5, cy_ + 6.0, INK, size=4)
        sp.ell(eN[0], eN[1] + 0.5, 2.0, 1.8, tones(GLOVE))                    # thumb over the card
    if pull:                                                                  # the rope over the near shoulder
        sp.line((shN[0] - 2, shN[1] + 2), (eN[0], eN[1]), (200, 170, 110), 2)
    new = sp.m & ~before
    o = new.copy()
    for _ in range(sp.k): o = dilate(o)
    o &= ~sp.m
    sp.col[o] = INK; sp.m |= o
    if confetti:
        rng = np.random.default_rng(confetti)
        for k in range(14):
            cx_, cy_ = hcx - 12 * hs + rng.random() * 24 * hs, hcy - 2 + rng.random() * 10 * hs
            if sp.m_ell(hcx, hcy, 12.6 * hs, 8.6 * hs)[0][int(sp.OY - cy_ * sp.k), int(sp.OX + cx_ * sp.k)]:
                sp.dot(cx_, cy_, [(255, 60, 80), (255, 220, 60), (80, 220, 255), (120, 255, 120)][k % 4])
    if soot: sp.soot(soot)


# ======================================================================================== ЗОЯ (gas-station cashier, behind the window)
JACKET = (46, 86, 172)
HAIR = (118, 40, 88)
ZSKIN = (232, 176, 146)


def gas_logo(sp, x, y, k=1.0):
    """the «ГАЗПРОПАЛ» logo: a blue gas flame that has gone out (a wisp of smoke)"""
    sp.poly([(x - 2.5 * k, y), (x + 2.5 * k, y), (x + 1.2 * k, y + 4.5 * k), (x, y + 6.5 * k), (x - 1.6 * k, y + 4.0 * k)], tones((60, 120, 230)))
    sp.line((x + 0.5 * k, y + 7.0 * k), (x - 0.5 * k, y + 9.0 * k), (170, 170, 176)); sp.line((x - 0.5 * k, y + 9.0 * k), (x + 0.6 * k, y + 11 * k), (170, 170, 176))


def zoya(sp, t=0.0, expr='deadpan', mouth_=0.0, mega=False, mega_up=1.0, gum=0.0, look=(0.3, 0.0), blink=None, chew=True, pose='desk'):
    """Зоя from the waist up (y 0 = desk line): pyramid body, aubergine beehive tower, gold hoops, blue eyeshadow, megaphone"""
    E = X(expr)
    if blink is None: blink = (t % 4.1) < 0.12
    br = 0.5 * math.sin(t * 2.0)
    body = sp.union([sp.m_ell(0.0, 6.0, 22.0, 18.0), sp.m_ell(0.0, 20.0 + br * 0.3, 17.0, 10.0)], tones(JACKET))
    sp.poly([(-3.0, 30.0), (5.0, 30.0), (1.0, 18.0)], tones((236, 236, 230)))                  # shirt V
    sp.line((1.0, 18.0), (1.0, 0.0), INK)
    sp.rect(8.0, 16.0, 16.0, 20.0, (240, 240, 232)); sp.line((9, 18), (15, 18), (60, 60, 70))   # name tag
    gas_logo(sp, -9.0, 15.0)                                                                       # «ГАЗПРОПАЛ» gone-out flame
    hatch_fill(sp, body & (DX.XC < -12), dark(JACKET, 0.6))
    # head
    hx, hy = 2.0, 42.0
    sp.cap((1.0, 28.0), (2.0, 34.0), 5.5, 5.5, tones(ZSKIN))
    face = sp.union([sp.m_ell(hx, hy, 11.0, 12.0), sp.m_ell(hx + 1.0, hy - 10.5, 8.0, 4.4)], tones(ZSKIN))   # + double chin
    sp.line((hx - 5.0, hy - 9.0), (hx + 6.0, hy - 9.0), dark(ZSKIN, 0.7))
    DX.blush(sp, hx + 6.5, hy - 3.5, 3.0, 2.0, (236, 120, 130))
    DX.blush(sp, hx - 5.5, hy - 3.5, 2.4, 2.0, (236, 120, 130))
    # eyes with heavy blue shadow + lashes
    lx, ly = look
    for ex, ew in ((hx + 4.6, 5.6), (hx - 4.2, 5.0)):
        sp.ell(ex, hy + 3.4, ew * 0.62, 2.6, tones((90, 130, 230)), ol=False)
    DX.eye(sp, hx + 4.6, hy + 2.2, 5.6, 4.6, E, (110, 70, 40), (lx, ly), blink, lash=INK, skin=ZSKIN, bold=2, flick=False)
    DX.eye(sp, hx - 4.2, hy + 2.2, 5.0, 4.4, E, (110, 70, 40), (lx, ly), blink, lash=INK, skin=ZSKIN, bold=2, flick=True)
    for ex in (hx + 7.4, hx + 6.2, hx - 7.0):
        sp.dot(ex, hy + 4.6, INK)
    DX.brow(sp, hx + 4.6, hy + 7.0, 6.0, E, +1, (70, 30, 40), th=1, arch=1.6)
    DX.brow(sp, hx - 4.2, hy + 7.0, 5.0, E, -1, (70, 30, 40), th=1, arch=1.6)
    sp.ell(hx + 2.0, hy - 1.0, 2.0, 2.0, tones(ZSKIN))                        # nose
    sp.dot(hx + 2.0, hy - 2.0, dark(ZSKIN, 0.6))
    sp.dot(hx - 6.0, hy - 5.0, (60, 30, 30))                                  # beauty mark
    chewm = (0.25 * (0.5 + 0.5 * math.sin(t * 9.0))) if chew else 0.0
    mo = max(mouth_, chewm * (1 if mouth_ < 0.05 else 0))
    DX.mouth(sp, hx + 1.5, hy - 5.5, 6.0, E, mo, (210, 36, 100), inside=(110, 20, 40), skin=ZSKIN, maxh=5)
    if gum > 0.05:
        sp.ell(hx + 2.0 + gum * 2, hy - 6.0, 2.0 + 5.0 * gum, 2.0 + 5.0 * gum, tones((255, 150, 200)))
    # beehive tower + earrings
    hair = sp.union([sp.m_ell(hx - 1.0, hy + 15.0, 13.5, 10.0), sp.m_ell(hx - 2.0, hy + 28.0, 10.0, 12.0), sp.m_ell(hx - 2.5, hy + 40.0, 6.5, 5.5)],
                    tones(HAIR))
    sp.ell(hx + 6.0, hy + 9.0, 6.0, 3.0, tones(HAIR), ang=-0.3)               # fringe
    for k in range(4):
        stroke(sp, [(hx - 8.0 + k * 3, hy + 14.0), (hx - 6.0 + k * 3, hy + 30.0 - k)], dark(HAIR, 0.62))
    sp.dot(hx + 3.0, hy + 33.0, (240, 220, 80)); sp.dot(hx + 4.0, hy + 32.0, (240, 220, 80))   # hairpin
    for ex, ey in ((hx + 11.0, hy - 3.0),):
        ring = sp.m_ell(ex, ey, 2.6, 3.4)[0] & ~sp.m_ell(ex, ey, 1.6, 2.4)[0]
        sp.fill(ring, (250, 206, 60)); sp.fill(ring & (DX.XC > ex), (255, 246, 160))
    sp.anchors['head'] = (hx, hy)
    sp.anchors['mouth'] = (hx + 1.5, hy - 5.5)
    # megaphone in the near hand (raised to the mouth) or the hand on the desk with rhinestone nails
    if mega:
        k = mega_up
        mx, my = hx + 9.0, hy - 5.0 - (1 - k) * 20
        cone = sp.m_poly([(mx, my - 2.5), (mx, my + 2.5), (mx + 16, my + 7.0), (mx + 16, my - 7.0)])
        sp.paint(cone, tones((240, 238, 228)), DX.lit(np.zeros(cone.shape, np.float32), np.clip((DX.YC - my) / 7, -1, 1)))
        sp.fill(cone & (np.abs(DX.XC - (mx + 9)) < 1.2), (220, 40, 50))
        sp.fill(cone & ~erode(cone), INK)
        sp.ell(mx + 16, my, 1.4, 7.0, tones((60, 60, 66)))
        sp.rect(mx + 2, my - 7.0, mx + 4.5, my - 2.5, (40, 40, 44))           # handle
        sp.ell(mx + 2.5, my - 7.0, 3.0, 2.6, tones(ZSKIN))
        sp.cap((12.0, 18.0), (mx + 2.0, my - 7.5), 3.4, 3.0, tones(JACKET))
    elif pose == 'ballet':                                                    # deadpan port de bras over the beehive, pinky out
        sh = (14.0, 24.0); el = (27.0, 58.0); wr = (16.0, 86.0); hd = (4.0, 93.0)
        sp.cap(sh, el, 3.6, 3.2, tones(JACKET)); sp.cap(el, wr, 3.2, 2.8, tones(JACKET))
        sp.cap(wr, hd, 2.6, 2.2, tones(ZSKIN))
        sp.ell(*hd, 3.0, 2.6, tones(ZSKIN)); sp.line((hd[0] - 2, hd[1] + 2), (hd[0] - 5, hd[1] + 4), ZSKIN)
        sp.dot(hd[0] - 5, hd[1] + 4, (255, 120, 200), keep=True)
    elif pose == 'point':                                                     # lazy point out of the window, to the refinery
        sh = (14.0, 24.0)
        sp.cap(sh, (30.0, 30.0), 3.6, 3.2, tones(JACKET)); sp.cap((30.0, 30.0), (44.0, 38.0), 3.2, 2.8, tones(JACKET))
        sp.ell(46.0, 39.0, 2.8, 2.4, tones(ZSKIN)); sp.line((47.0, 40.0), (52.0, 42.0), ZSKIN)
        sp.dot(52.0, 42.0, (255, 120, 200), keep=True)
    else:
        sp.ell(10.0, 2.0, 4.0, 2.4, tones(ZSKIN))
        for k in range(3): sp.dot(12.0 + k * 0.0, 1.0 + k, (255, 120, 200), keep=True)
    sp.outline(INK, 2)


# ======================================================================================== vehicles
def _wheel(sp, x, y, r, spin, rim=(170, 170, 160)):
    sp.ell(x, y, r, r, tones((36, 36, 40)))
    sp.ell(x, y, r * 0.5, r * 0.5, tones(rim))
    a = spin
    sp.line((x + math.cos(a) * r * 0.45, y + math.sin(a) * r * 0.45), (x - math.cos(a) * r * 0.45, y - math.sin(a) * r * 0.45), dark(rim, 0.6))
    sp.dot(x, y, INK)


def tanker(sp, t=0.0, spin=0.0, bounce=0.0, lights=True):
    """Soviet tanker truck, side view facing +x: orange tank «ОГНЕОПАСНО», light-blue cab, driver silhouette"""
    b = bounce
    sp.rect(-14, 7 + b, 112, 12 + b, (40, 36, 34))                             # chassis
    tank = sp.sup(26.0, 30.0 + b, 41.0, 15.0, tones((236, 120, 30)), n=3.2)
    for x in (-4.0, 26.0, 56.0):
        sp.fill(tank & (np.abs(DX.XC - x) < 0.7), dark((236, 120, 30), 0.6))
    sp.ptext('ОГНЕОПАСНО', 26.0, 34.0 + b, INK, size=6, center=True)
    sp.rect(18, 45 + b, 34, 47 + b, (60, 56, 52)); sp.rect(24, 47 + b, 28, 50 + b, (60, 56, 52))   # hatch on top
    sp.rect(-15, 12 + b, -13, 40 + b, (70, 64, 60))                            # ladder
    for y in range(14, 40, 4): sp.line((-15.0, y + b), (-12.0, y + b), (110, 104, 96))
    # cab + hood
    cab = sp.m_poly([(70.0, 10.0 + b), (98.0, 10.0 + b), (98.0, 26.0 + b), (94.0, 44.0 + b), (72.0, 44.0 + b), (70.0, 40.0 + b)])
    sp.paint(cab, tones((116, 176, 196)), DX.lit(np.clip((DX.XC - 84) / 16, -1, 1) * 0.5, np.clip((DX.YC - 26 - b) / 18, -1, 1)))
    hood = sp.m_poly([(97.0, 10.0 + b), (118.0, 10.0 + b), (119.0, 24.0 + b), (110.0, 28.0 + b), (97.0, 28.0 + b)])
    sp.paint(hood, tones((116, 176, 196)), DX.lit(np.clip((DX.XC - 108) / 12, -1, 1) * 0.4, np.clip((DX.YC - 19 - b) / 10, -1, 1)))
    for k in range(3): sp.line((112.0, 13.0 + k * 3 + b), (117.0, 13.0 + k * 3 + b), INK)    # grille slots
    win = sp.m_poly([(80.0, 29.0 + b), (93.0, 29.0 + b), (90.0, 41.0 + b), (80.0, 41.0 + b)])
    sp.fill(win, (190, 230, 240)); sp.fill(win & hatch_mask_(), (150, 200, 220)); sp.fill(win & ~erode(win), INK)
    sp.ell(85.0, 34.0 + b, 3.0, 3.6, tones((40, 34, 40)), ol=False)            # driver silhouette + cap
    sp.rect(82.0, 37.0 + b, 89.0, 38.5 + b, (30, 26, 30))
    sp.rect(71.0, 20.0 + b, 74.0, 22.0 + b, INK)                               # door handle
    sp.rect(116.0, 6.0 + b, 121.0, 10.0 + b, (190, 190, 180))                  # bumper
    sp.ell(117.0, 20.0 + b, 1.6, 2.2, tones((255, 240, 180) if lights else (180, 170, 140)))
    sp.rect(66.0, 40.0 + b, 68.0, 52.0 + b, (60, 56, 52))                      # exhaust pipe
    for x in (-4.0, 8.0, 100.0): _wheel(sp, x, 7.5, 7.5, spin)
    sp.ell(100.0, 12.0 + b, 9.5, 5.0, tones((40, 40, 44)), clip=DX.YC > 12.0 + b)   # mudguard
    sp.anchors['exhaust'] = (67.0, 52.0 + b)
    sp.anchors['window'] = (86.0, 35.0 + b)
    sp.anchors['tank'] = (26.0, 30.0 + b)
    sp.anchors['front'] = (121.0, 12.0)
    sp.outline(INK, 2)


def hatch_mask_():
    return MX.hatch_mask(3)


CAR_COLS = [(232, 228, 214), (196, 60, 52), (206, 186, 140), (100, 46, 80), (70, 120, 170), (86, 132, 90)]


def lada(sp, col=(232, 228, 214), t=0.0, honk=0.0, rust=0, spin=0.0, driver=True, web=False, sign=None, tint=False, trunk=0.0, rims=False,
         police=False):
    """boxy Soviet sedan «six», side view facing +x, ~64 px long"""
    body = sp.m_poly([(-30.0, 6.0), (32.0, 6.0), (33.0, 14.0), (30.0, 17.0), (12.0, 18.0), (6.0, 27.0), (-14.0, 27.0), (-20.0, 18.0),
                      (-30.0, 17.0), (-31.0, 12.0)])
    sp.paint(body, tones(col), DX.lit(np.clip(DX.XC / 32, -1, 1) * 0.3, np.clip((DX.YC - 16) / 11, -1, 1)))
    w1 = sp.m_poly([(-12.0, 19.0), (-3.0, 19.0), (-3.0, 25.5), (-12.0, 25.5), (-17.0, 19.0)])
    w2 = sp.m_poly([(-1.0, 19.0), (10.0, 19.0), (5.0, 25.5), (-1.0, 25.5)])
    for w in (w1, w2):
        if tint:
            sp.fill(w, (18, 18, 24)); sp.fill(w & hatch_mask_() & (DX.YC > 22), (44, 46, 60)); sp.fill(w & ~erode(w), INK)
        else:
            sp.fill(w, (150, 190, 214)); sp.fill(w & hatch_mask_(), (110, 150, 180)); sp.fill(w & ~erode(w), INK)
    if driver and not tint: sp.ell(3.0, 21.0, 2.4, 2.8, tones((40, 34, 40)), ol=False, clip=w2)
    if trunk > 0:                                                             # open boot full of «Родниковая» bottles
        sp.rect(-31.0, 13.0, -15.0, 18.0, (20, 16, 18))
        for k in range(5): bottle_prop(sp, -29.0 + k * 3.2, 14.5, 0.55)
        a = math.radians(20 + 70 * trunk)
        sp.line((-15.0, 18.0), (-15.0 - math.cos(a) * 17, 18.0 + math.sin(a) * 17), dark(col, 0.7), 2)
    sp.line((-30.0, 12.0), (33.0, 12.0), dark(col, 0.65))
    if police:                                                                # patrol «six»: blue stripe, «ДПС», light bar
        sp.fill(body & (DX.YC > 10.0) & (DX.YC < 13.5), (40, 80, 190))
        sp.ptext('ДПС', 6.0, 18.0, (40, 80, 190), size=4, center=True)
        on = int(t * 6) % 2 == 0
        sp.rect(-8.0, 27.0, -1.0, 29.5, (255, 60, 60) if on else (120, 30, 30))
        sp.rect(-1.0, 27.0, 6.0, 29.5, (60, 120, 255) if not on else (30, 50, 120))
        sp.rect(-8.0, 26.6, 6.0, 27.2, (60, 60, 66))
    sp.rect(31.0, 6.0, 35.0, 9.0, (200, 200, 196)); sp.rect(-33.0, 6.0, -29.0, 9.0, (200, 200, 196))   # chrome bumpers
    sp.rect(30.5, 12.0, 33.0, 15.0, (255, 240, 190))                           # headlight
    sp.rect(-31.0, 12.0, -29.5, 15.0, (220, 40, 40))
    sp.rect(-4.0, 13.0, -1.0, 14.0, INK)
    if rust:
        rng = np.random.default_rng(rust)
        for k in range(6): sp.dot(-28 + rng.random() * 56, 7 + rng.random() * 6, (150, 80, 40))
    for x in (-19.0, 20.0): _wheel(sp, x, 5.0, 5.2, spin, rim=(220, 220, 230) if rims else (170, 170, 160))
    if sign:                                                                  # cardboard in the rear window
        sp.rect(-13.0, 27.0, 11.0, 36.0, (214, 186, 140)); sp.line((-13.0, 27.0), (11.0, 27.0), (150, 120, 80))
        sp.ptext(sign, -1.0, 34.0, (190, 30, 36), size=4, center=True)
    if web:                                                                   # cobwebs: it has been here since spring
        for (cx_, cy_) in ((-28.0, 16.0), (8.0, 26.0), (30.0, 15.0)):
            for a in range(5):
                an = a * 0.6 + 0.3
                sp.line((cx_, cy_), (cx_ + math.cos(an) * 6 * (1 if cx_ < 0 else -1), cy_ - math.sin(an) * 6), (236, 236, 240))
            for r in (2.5, 4.5):
                sp.line((cx_ + (r if cx_ < 0 else -r), cy_), (cx_, cy_ - r), (236, 236, 240))
        sp.rect(-3.0, 4.0, -1.5, 5.0, (200, 200, 200))
    sp.anchors['front'] = (35.0, 8.0)
    sp.anchors['back'] = (-33.0, 8.0)
    sp.outline(INK, 2)


def buhanka(sp, col=(90, 120, 80), t=0.0, spin=0.0):
    """UAZ «loaf» van, side view facing +x"""
    body = sp.sup(0.0, 18.0, 28.0, 13.0, tones(col), n=3.4)
    for x in (-18.0, -6.0, 8.0):
        w = sp.m_poly([(x, 21.0), (x + 9.0, 21.0), (x + 9.0, 27.0), (x, 27.0)])
        sp.fill(w, (150, 190, 214)); sp.fill(w & ~erode(w), INK)
    sp.ell(21.0, 23.0, 5.0, 4.0, tones((150, 190, 214)), clip=DX.XC < 25)
    sp.ell(19.0, 23.0, 2.2, 2.6, tones((40, 34, 40)), ol=False)
    sp.line((-27.0, 15.0), (27.0, 15.0), dark(col, 0.6))
    sp.rect(26.0, 9.0, 29.0, 12.0, (255, 240, 190))
    for x in (-16.0, 16.0): _wheel(sp, x, 5.0, 5.6, spin)
    sp.outline(INK, 2)


VESTA = (206, 40, 44)


def vesta(sp, col=VESTA, t=0.0, spin=0.0, bow=1.0, flap=0.0, plug=False):
    """«Веста-Шместа»: the brand-new award hatchback (E06), side view facing +x, ~70 px long. Chrome «X» on the nose,
    a gift ribbon around the body + a huge bow on the roof (bow 0..1 = how much is left), fuel flap (flap 0..1 open) hides a socket"""
    body = sp.m_poly([(-33.0, 6.0), (34.0, 6.0), (35.5, 12.0), (34.0, 16.5), (19.0, 20.0), (9.0, 30.0), (-15.0, 31.0), (-27.0, 23.0),
                      (-34.0, 18.0), (-34.5, 10.0)])
    sp.paint(body, tones(col), DX.lit(np.clip(DX.XC / 34, -1, 1) * 0.3, np.clip((DX.YC - 17) / 12, -1, 1)))
    gl = sp.m_poly([(-25.0, 22.0), (16.0, 21.0), (8.0, 28.5), (-14.5, 29.5)])
    sp.fill(gl, (150, 196, 220)); sp.fill(gl & hatch_mask_(), (110, 156, 186)); sp.fill(gl & ~erode(gl), INK)
    sp.rect(-5.0, 21.0, -3.5, 29.5, dark(col, 0.55))                         # B-pillar
    sp.line((-33.0, 14.0), (33.0, 16.0), dark(col, 0.62))                   # sporty character line
    sp.line((-31.0, 9.5), (33.0, 9.5), dark(col, 0.7))
    sp.rect(-2.0, 17.0, 1.0, 18.0, (230, 230, 236))                          # door handle
    for a, b in (((29.0, 8.0), (35.0, 16.0)), ((29.0, 16.0), (35.0, 8.0))):  # the chrome «X» face
        sp.line(a, b, (236, 236, 244), 2)
    sp.rect(30.0, 15.0, 34.5, 17.0, (255, 246, 200))                         # slit headlight
    sp.rect(-34.0, 15.0, -31.0, 18.0, (230, 40, 40))
    # fuel flap on the rear quarter
    fx0, fy0, fx1, fy1 = -26.0, 14.5, -21.0, 19.5
    if flap > 0:
        sp.rect(fx0, fy0, fx1, fy1, (24, 24, 28))
        sp.ell(-23.5, 17.0, 2.0, 2.0, tones((60, 60, 66)), ol=False)
        for dx, dy in ((-0.8, 0.6), (0.8, 0.6), (0.0, -0.8)): sp.dot(-23.5 + dx, 17.0 + dy, (12, 12, 14))
        w = (fx1 - fx0) * (1 - 0.85 * flap)
        sp.rect(fx0 - w, fy0, fx0, fy1, dark(col, 0.85)); sp.line((fx0 - w, fy0), (fx0 - w, fy1), INK)
        if plug: sp.rect(-24.5, 16.0, -14.0, 18.0, (40, 40, 44))
    else:
        sp.line((fx0, fy0), (fx1, fy0), dark(col, 0.55)); sp.line((fx0, fy1), (fx1, fy1), dark(col, 0.55))
        sp.line((fx0, fy0), (fx0, fy1), dark(col, 0.55)); sp.line((fx1, fy0), (fx1, fy1), dark(col, 0.55))
    for x in (-20.0, 21.0): _wheel(sp, x, 5.0, 5.8, spin, rim=(226, 226, 236))
    if bow > 0:                                                               # gift ribbon + the bow
        rb = (250, 214, 60)
        sp.fill(body & (np.abs(DX.XC + 4.0) < 1.6), rb)
        sp.fill(body & (np.abs(DX.YC - 12.0) < 1.2), rb)
        k = bow
        for sx in (-1.0, 1.0):
            sp.ell(-4.0 + sx * 6.0 * k, 35.0, 6.0 * k, 4.2 * k, tones((230, 36, 50)), ang=sx * 0.35)
            sp.cap((-4.0, 32.0), (-4.0 + sx * 7.0 * k, 27.0), 1.4, 1.0, tones((230, 36, 50)))
        sp.ell(-4.0, 33.5, 2.4, 2.2, tones((200, 26, 40)))
    sp.anchors['front'] = (36.0, 9.0)
    sp.anchors['back'] = (-35.0, 9.0)
    sp.anchors['flap'] = (-23.5, 17.0)
    sp.outline(INK, 2)


def monowheel_solo(sp, t=0.0, spin=0.0, face='smile'):
    """the wheel alone (model sheet, inserts)"""
    monowheel(sp, t, spin, face=face if face != 'dead' else 'smile', dead=face == 'dead')
    sp.outline(INK, 2)


# ======================================================================================== ТОЛИК (tanker driver)
LEATHER = (66, 48, 42)
TRACK = (44, 56, 130)
TSKIN = (226, 156, 124)


def tolik(sp, t=0.0, expr='grin', mouth_=0.0, look=(0.5, 0.0), blink=None, pull=False, walk=0.0, lean=False, wave=0.0, clip=None):
    """Толик, tanker driver: «square» — stocky in a leather jacket, three-stripe tracksuit, slippers over white socks, flat cap,
    round bald head, toothpick, gold chain. lean: leaning out of the cab window (arm on the door); clip: erase below this height"""
    E = X(expr)
    if blink is None: blink = (t % 3.3) < 0.12
    sw = math.sin(walk) * 3.0 if pull else 0.0
    # legs: tracksuit + socks + slippers
    for side, dx, c in ((-1, -4.0, dark(TRACK, 0.8)), (1, 4.0, TRACK)):
        x = dx + side * sw
        sp.cap((x, 5.0), (dx * 0.6, 26.0), 4.4, 4.8, tones(c))
        sp.line((x + 2.5, 6.0), (dx * 0.6 + 2.5, 25.0), (236, 236, 236))
        sp.line((x + 3.5, 6.0), (dx * 0.6 + 3.5, 25.0), (236, 236, 236))
        sp.rect(x - 3, 1.0, x + 3, 5.0, (246, 246, 240))                     # white socks
        sp.ell(x + 2.0, 0.8, 5.0, 1.6, tones((40, 40, 46)))                   # slipper
    # torso: square leather jacket with a belly
    body = sp.sup(0.0, 38.0, 15.0, 15.0, tones(LEATHER), n=3.0)
    sp.ell(4.0, 30.0, 10.0, 8.0, tones(LEATHER), ol=False)
    sp.line((6.0, 23.0), (8.0, 52.0), (30, 22, 20))
    for y in (30.0, 40.0): sp.dot(10.0, y, (200, 190, 170))                   # press studs
    sp.rect(-14.0, 22.5, 14.0, 25.0, dark(LEATHER, 0.7))                      # jacket hem
    sp.poly([(-2.0, 53.0), (10.0, 53.0), (4.0, 46.0)], tones((236, 230, 220)))   # vest under the jacket
    sp.line((0.0, 51.0), (8.0, 51.0), (250, 210, 70)); sp.dot(4.0, 49.0, (250, 210, 70))   # gold chain
    # arms
    sh = (9.0, 49.0)
    if pull: hn = (sh[0] + 7.0, sh[1] - 4.0)
    elif lean: hn = (sh[0] + 16.0, sh[1] - 8.0 + wave * 3 * math.sin(t * 14))
    else: hn = (sh[0] + 6.0, 30.0)
    k, e = ik(sh, hn, 11.0, 10.0, -1.0)
    sp.cap(sh, k, 4.0, 3.6, tones(LEATHER)); sp.cap(k, e, 3.6, 3.2, tones(LEATHER))
    sp.ell(*e, 3.0, 2.8, tones(TSKIN))
    if pull: sp.line((sh[0] - 2, sh[1] + 2), e, (200, 170, 110), 2)
    # head: round, bald, cap, stubble, toothpick
    hs = 1.3
    hx, hy = 6.0, 64.0
    def Hp(dx, dy): return (hx + dx * hs, hy + dy * hs)
    sp.cap((4.0, 52.0), (5.0, 58.0), 6.0, 6.0, tones(TSKIN))
    face = sp.union([sp.m_ell(*Hp(0, 0), 10.5 * hs, 10.0 * hs), sp.m_ell(*Hp(1.5, -6.0), 9.0 * hs, 5.5 * hs)], tones(TSKIN))
    rng = np.random.default_rng(5)
    sp.fill(face & (DX.YC < hy - 3 * hs) & erode(face) & (rng.random(face.shape) < 0.5) & DX.CHECK, (160, 120, 104))
    sp.ell(*Hp(-9.5, 0.5), 2.6 * hs, 3.6 * hs, tones(TSKIN))                  # ear
    DX.eye(sp, *Hp(4.8, 1.5), 4.6 * hs, 4.0 * hs, E, (90, 70, 50), look, blink, lash=INK, skin=TSKIN)
    DX.eye(sp, *Hp(-2.5, 1.5), 3.8 * hs, 3.8 * hs, E, (90, 70, 50), look, blink, lash=INK, skin=TSKIN)
    DX.brow(sp, *Hp(4.8, 5.0), 5.0 * hs, E, +1, (70, 46, 36), th=2)
    DX.brow(sp, *Hp(-2.5, 5.0), 4.0 * hs, E, -1, (70, 46, 36), th=2)
    sp.ell(*Hp(8.5, -1.5), 3.4 * hs, 3.0 * hs, tones((214, 128, 104)))       # broad nose
    sp.dot(*Hp(9.5, -3.0), INK)
    mx, my = Hp(5.0, -6.0)
    DX.mouth(sp, mx, my, 6.0 * hs, E, mouth_, INK, skin=TSKIN, maxh=4 * hs)
    if mouth_ < 0.15:
        sp.line((mx + 2, my), (mx + 9, my + 1.5), (220, 200, 150))           # toothpick
    DX.blush(sp, *Hp(7.0, -3.0), 2.4 * hs, 1.6 * hs, (230, 120, 110))
    # flat cap
    cap = sp.union([sp.m_ell(*Hp(-0.5, 8.0), 11.5 * hs, 4.5 * hs, -0.08)], tones((72, 72, 80)))
    sp.ell(*Hp(9.0, 6.0), 5.0 * hs, 1.6 * hs, tones((60, 60, 68)), ang=-0.15)
    sp.line(Hp(-8.0, 9.5), Hp(6.0, 10.5), (96, 96, 104))
    sp.anchors['head'] = Hp(2.0, 0.0)
    sp.anchors['shoulder'] = sh
    if clip is not None: sp.clip_below(clip)
    sp.outline(INK, 2)


# ======================================================================================== БОРИС БОРИСЫЧ (boss)
SUIT = (92, 98, 124)
BSKIN = (236, 168, 140)


def boss(sp, t=0.0, expr='smug', mouth_=0.0, look=(0.6, 0.0), blink=None, pose='stand', clip=None, money=False):
    """Борис Борисыч, «ball»: round belly in a grey-blue suit over the orange robe, white helmet (bosses wear white), no neck,
    double chin, tiny eyes, thin mustache, gold watch. pose: stand / pat (arm out to the right) / podium (both arms up) / key"""
    E = X(expr)
    if blink is None: blink = (t % 3.9) < 0.12
    br = 0.6 * math.sin(t * 2.0)
    for dx in (-5.0, 5.0):                                                    # short legs + shoes
        sp.cap((dx, 4.0), (dx * 0.8, 16.0), 4.2, 4.6, tones((54, 56, 70)))
        sp.ell(dx + 2.5, 2.0, 5.0, 2.4, tones((30, 26, 28)))
    body = sp.union([sp.m_ell(0.0, 32.0 + br * 0.3, 21.0, 21.0), sp.m_ell(2.0, 22.0, 18.0, 12.0)], tones(SUIT))
    sp.poly([(0.0, 52.0), (10.0, 52.0), (5.0, 30.0)], tones(ROBE))           # orange robe in the jacket's V
    sp.line((5.0, 30.0), (5.0, 14.0), dark(SUIT, 0.6))
    for y in (24.0, 34.0): sp.dot(7.0, y, (220, 200, 120))                    # buttons strain on the belly
    sp.rect(12.0, 40.0, 17.0, 43.0, (240, 240, 236))                          # pen in the breast pocket
    hatch_fill(sp, body & (DX.XC < -12), dark(SUIT, 0.55))
    # arms
    sh = (14.0, 44.0); shf = (-12.0, 44.0)
    if pose == 'pat': hn = (36.0, 50.0)
    elif pose == 'podium': hn = (22.0, 70.0)
    elif pose == 'key': hn = (30.0, 40.0)
    else: hn = (20.0, 22.0)
    hf = (-24.0, 66.0) if pose == 'podium' else (-18.0, 22.0)
    for s_, h_, c in ((shf, hf, dark(SUIT, 0.8)), (sh, hn, SUIT)):
        k, e = ik(s_, h_, 11.0, 11.0, -1.0 if s_ is sh else 1.0)
        sp.cap(s_, k, 4.6, 4.0, tones(c)); sp.cap(k, e, 4.0, 3.6, tones(c))
        sp.ell(*e, 3.4, 3.0, tones(BSKIN))
        if s_ is sh: sp.rect(e[0] - 4.0, e[1] - 1.0, e[0] - 1.5, e[1] + 1.5, (250, 210, 70)); hand = e
    if money:
        sp.rect(hand[0] - 3, hand[1] - 7, hand[0] + 6, hand[1] - 1, (70, 50, 40))   # barsetka
        sp.rect(hand[0] - 2, hand[1] - 2, hand[0] + 5, hand[1] + 3, (120, 180, 110))
    # head straight on the shoulders: wide, double chin, red cheeks
    hs = 1.3
    hx, hy = 4.0, 60.0
    def Hp(dx, dy): return (hx + dx * hs, hy + dy * hs)
    face = sp.union([sp.m_ell(*Hp(0, 0), 11.5 * hs, 10.0 * hs), sp.m_ell(*Hp(1.0, -8.0), 10.0 * hs, 4.5 * hs)], tones(BSKIN))
    sp.line(Hp(-6.0, -6.5), Hp(8.0, -6.5), dark(BSKIN, 0.68))                # chin fold
    DX.blush(sp, *Hp(7.0, -2.0), 3.0 * hs, 2.0 * hs, (230, 110, 110))
    DX.blush(sp, *Hp(-5.0, -2.0), 2.4 * hs, 2.0 * hs, (230, 110, 110))
    DX.eye(sp, *Hp(4.6, 2.5), 4.0 * hs, 3.2 * hs, E, (70, 90, 120), look, blink, lash=INK, skin=BSKIN, bag=dark(BSKIN, 0.7))
    DX.eye(sp, *Hp(-2.4, 2.5), 3.4 * hs, 3.0 * hs, E, (70, 90, 120), look, blink, lash=INK, skin=BSKIN, bag=dark(BSKIN, 0.7))
    DX.brow(sp, *Hp(4.6, 5.6), 4.4 * hs, E, +1, (90, 70, 60), th=1)
    DX.brow(sp, *Hp(-2.4, 5.6), 3.6 * hs, E, -1, (90, 70, 60), th=1)
    sp.ell(*Hp(8.0, -0.5), 2.8 * hs, 2.4 * hs, tones((222, 140, 120)))       # button nose
    mx, my = Hp(5.5, -4.5)
    DX.mouth(sp, mx, my, 5.5 * hs, E, mouth_, INK, skin=BSKIN, maxh=4 * hs)
    sp.line(Hp(2.0, -2.8), Hp(9.0, -2.8), (110, 90, 80))                     # thin mustache
    # white helmet + badge
    hcx, hcy = Hp(0.0, 9.5)
    hm = sp.m_ell(hcx, hcy, 12.5 * hs, 7.5 * hs)[0] & (DX.YC > hy + 7.0 * hs)
    sp.paint(hm, tones((248, 248, 244)), DX.lit(np.clip((DX.XC - hcx) / (12 * hs), -1, 1), np.clip((DX.YC - hcy) / (8 * hs), -1, 1)))
    sp.ell(*Hp(1.0, 7.5), 14.5 * hs, 2.0 * hs, tones((248, 248, 244)))
    sp.rect(*Hp(-1.5, 11.0), *Hp(2.5, 14.0), (220, 40, 40))                   # badge
    sp.anchors['head'] = Hp(2.0, 0.0); sp.anchors['hand'] = hand
    if clip is not None: sp.clip_below(clip)
    sp.outline(INK, 2)


# ======================================================================================== ВАДИК (garage dealer)
VTRACK = (40, 40, 48)
VSKIN = (214, 170, 140)


def vadik(sp, t=0.0, expr='sly', mouth_=0.0, look=(0.7, 0.0), blink=None, pose='stand', clip=None, bottle=False):
    """Вадик, «hooded pole»: tall thin, black tracksuit with red stripes, hood up under an eight-panel cap, narrow face,
    pencil mustache, sunflower husk on the lip, man-bag on the wrist, pointy shoes. pose: stand / offer (bottle forward) / nod"""
    E = X(expr)
    if blink is None: blink = (t % 3.1) < 0.12
    for dx, c in ((-3.0, dark(VTRACK, 0.8)), (3.0, VTRACK)):
        sp.cap((dx, 4.0), (dx * 0.6, 36.0), 3.2, 3.6, tones(c))
        sp.line((dx + 2.0, 6.0), (dx * 0.6 + 2.0, 35.0), (210, 40, 40))
        sp.poly([(dx - 3.0, 0.0), (dx + 7.0, 0.0), (dx + 3.0, 4.0), (dx - 3.0, 4.0)], tones((24, 22, 24)))   # pointy shoes
    body = sp.sup(0.0, 50.0, 10.0, 16.0, tones(VTRACK), n=2.6)
    sp.line((4.0, 36.0), (5.0, 66.0), (180, 180, 186))                         # zipper
    sp.line((-9.0, 40.0), (-7.0, 64.0), (210, 40, 40))
    sh = (6.0, 62.0)
    hn = (24.0, 52.0) if pose == 'offer' else (10.0, 38.0)
    k, e = ik(sh, hn, 12.0, 11.0, -1.0)
    sp.cap(sh, k, 3.2, 3.0, tones(VTRACK)); sp.cap(k, e, 3.0, 2.8, tones(VTRACK))
    sp.ell(*e, 2.6, 2.4, tones(VSKIN))
    if pose != 'offer':
        sp.rect(e[0] - 3, e[1] - 6, e[0] + 4, e[1] - 1, (70, 50, 40)); sp.line((e[0], e[1] - 1), (e[0], e[1]), (70, 50, 40))   # man-bag
    if bottle:
        bottle_prop(sp, e[0] + 1.0, e[1] - 2.0)
    # head: narrow, hooded, cap
    hs = 1.3
    hx, hy = 4.0, 78.0
    def Hp(dx, dy): return (hx + dx * hs, hy + dy * hs)
    sp.ell(*Hp(-1.0, 1.0), 10.0 * hs, 12.5 * hs, tones(VTRACK))               # the hood around the face
    face = sp.union([sp.m_ell(*Hp(1.5, -1.0), 7.0 * hs, 10.0 * hs)], tones(VSKIN))
    DX.eye(sp, *Hp(4.0, 2.0), 3.8 * hs, 2.8 * hs, E, (70, 60, 40), look, blink, lash=INK, skin=VSKIN, bag=dark(VSKIN, 0.7))
    DX.eye(sp, *Hp(-1.5, 2.0), 3.0 * hs, 2.6 * hs, E, (70, 60, 40), look, blink, lash=INK, skin=VSKIN)
    DX.brow(sp, *Hp(4.0, 4.6), 3.8 * hs, E, +1, (40, 30, 26), th=1)
    DX.brow(sp, *Hp(-1.5, 4.6), 3.0 * hs, E, -1, (40, 30, 26), th=1)
    sp.poly([Hp(6.0, 1.0), Hp(10.0, -3.0), Hp(6.5, -3.5)], tones((200, 150, 120)))   # long nose
    mx, my = Hp(5.0, -6.0)
    DX.mouth(sp, mx, my, 4.5 * hs, E, mouth_, INK, skin=VSKIN, maxh=3 * hs)
    sp.line(Hp(3.0, -4.6), Hp(8.0, -4.6), (50, 36, 30))                       # pencil mustache
    if mouth_ < 0.15: sp.dot(*Hp(8.0, -6.5), (230, 230, 220))                # sunflower husk
    cap = sp.ell(*Hp(-0.5, 10.0), 9.5 * hs, 4.0 * hs, tones((70, 66, 70)))   # eight-panel cap
    sp.ell(*Hp(7.0, 8.0), 4.5 * hs, 1.4 * hs, tones((60, 56, 60)), ang=-0.15)
    sp.dot(*Hp(-0.5, 13.6), (200, 40, 40))
    sp.anchors['head'] = Hp(1.0, 0.0); sp.anchors['hand'] = e
    if clip is not None: sp.clip_below(clip)
    sp.outline(INK, 2)


def bottle_prop(sp, x, y, k=1.0, full=True):
    """plastic «Родниковая» water bottle full of golden gasoline"""
    sp.rect(x - 2 * k, y - 1 * k, x + 2 * k, y + 9 * k, (230, 200, 90) if full else (200, 220, 230))
    sp.rect(x - 2 * k, y + 3 * k, x + 2 * k, y + 5 * k, (60, 120, 220))
    sp.rect(x - 1 * k, y + 9 * k, x + 1 * k, y + 11 * k, (40, 110, 200))
    sp.dot(x - 1 * k, y + 7 * k, (255, 250, 210))


# ======================================================================================== ИНСПЕКТОР ДПС СТОЛБОВ
COP = (44, 56, 90)
VEST = (190, 240, 60)
CSKIN = (226, 160, 128)


def inspector(sp, t=0.0, expr='glare', mouth_=0.0, look=(0.7, 0.0), blink=None, pose='stand', whistle=False, clip=None):
    """Инспектор Столбов, «post in a cap»: tall rectangle, huge aerodrome cap with a red band, acid-green reflective vest,
    striped baton, whistle, square jaw, red cheeks. pose: stand / stop (baton up) / wave (baton waving) / point"""
    E = X(expr)
    if blink is None: blink = (t % 3.5) < 0.12
    for dx, c in ((-4.0, dark(COP, 0.8)), (4.0, COP)):
        sp.cap((dx, 4.0), (dx * 0.7, 34.0), 4.0, 4.4, tones(c))
        sp.line((dx + 3.0, 6.0), (dx * 0.7 + 3.0, 33.0), (200, 40, 40))       # red trouser piping
        sp.ell(dx + 2.5, 2.0, 5.0, 2.4, tones((24, 22, 26)))
    body = sp.sup(0.0, 52.0, 12.5, 19.0, tones(COP), n=4.0)
    vest = sp.m_super(0.0, 50.0, 11.5, 16.0, 4.0)[0]
    sp.paint(vest, tones(VEST), DX.lit(np.clip(DX.XC / 12, -1, 1) * 0.6, np.clip((DX.YC - 50) / 16, -1, 1)))
    for y in (42.0, 54.0): sp.fill(vest & (np.abs(DX.YC - y) < 1.2), (230, 232, 230))
    sp.ptext('ДПС', 0.0, 51.0, INK, size=5, center=True)
    sh = (9.0, 66.0); shf = (-9.0, 66.0)
    if pose == 'stop': hn = (25.0, 80.0)
    elif pose == 'wave': hn = (26.0, 76.0 + 4.0 * math.sin(t * 16))
    elif pose == 'point': hn = (30.0, 64.0)
    else: hn = (14.0, 44.0)
    k, e = ik(sh, hn, 13.0, 12.0, -1.0)
    sp.cap(shf, (-14.0, 44.0), 3.6, 3.2, tones(dark(COP, 0.8))); sp.ell(-14.0, 43.0, 3.0, 2.8, tones(CSKIN))
    sp.cap(sh, k, 3.8, 3.4, tones(COP)); sp.cap(k, e, 3.4, 3.0, tones(COP))
    sp.ell(*e, 3.0, 2.8, tones(CSKIN))
    if pose in ('stop', 'wave', 'point'):                                     # striped baton
        a = math.radians(70 if pose == 'stop' else 20)
        for i in range(6):
            p0 = (e[0] + math.cos(a) * i * 2.4, e[1] + math.sin(a) * i * 2.4)
            p1 = (e[0] + math.cos(a) * (i + 1) * 2.4, e[1] + math.sin(a) * (i + 1) * 2.4)
            sp.line(p0, p1, (250, 250, 246) if i % 2 else (30, 30, 34), 2)
    hs = 1.3
    hx, hy = 3.0, 82.0
    def Hp(dx, dy): return (hx + dx * hs, hy + dy * hs)
    sp.cap((2.0, 68.0), (3.0, 74.0), 5.0, 5.0, tones(CSKIN))
    face = sp.union([sp.m_super(*Hp(1.0, -1.0), 9.5 * hs, 10.0 * hs, 3.2)], tones(CSKIN))   # square jaw
    DX.blush(sp, *Hp(6.5, -3.0), 2.6 * hs, 2.0 * hs, (230, 100, 100))
    DX.blush(sp, *Hp(-4.5, -3.0), 2.2 * hs, 2.0 * hs, (230, 100, 100))
    DX.eye(sp, *Hp(4.6, 2.0), 4.2 * hs, 3.4 * hs, E, (60, 80, 110), look, blink, lash=INK, skin=CSKIN)
    DX.eye(sp, *Hp(-2.6, 2.0), 3.6 * hs, 3.2 * hs, E, (60, 80, 110), look, blink, lash=INK, skin=CSKIN)
    DX.brow(sp, *Hp(4.6, 5.0), 4.6 * hs, E, +1, (60, 46, 40), th=2)
    DX.brow(sp, *Hp(-2.6, 5.0), 3.8 * hs, E, -1, (60, 46, 40), th=2)
    sp.ell(*Hp(8.0, -1.0), 2.6 * hs, 2.6 * hs, tones((214, 130, 110)))
    mx, my = Hp(5.0, -6.0)
    DX.mouth(sp, mx, my, 5.0 * hs, E, mouth_, INK, skin=CSKIN, maxh=4 * hs)
    if whistle:
        sp.rect(mx, my - 1.0, mx + 5.0, my + 1.4, (220, 220, 210)); sp.dot(mx + 5.0, my - 1.4, (240, 240, 230))
    # the aerodrome cap
    sp.ell(*Hp(0.5, 10.5), 14.0 * hs, 5.5 * hs, tones(COP))
    sp.rect(*Hp(-9.0, 6.0), *Hp(10.0, 9.0), (200, 40, 40))                    # red band
    sp.ell(*Hp(7.0, 6.0), 6.0 * hs, 1.6 * hs, tones((20, 20, 24)), ang=-0.1)  # visor
    sp.ell(*Hp(1.0, 11.0), 2.0 * hs, 2.0 * hs, tones((240, 200, 60)))         # cockade
    sp.anchors['head'] = Hp(1.0, 0.0); sp.anchors['hand'] = e
    if clip is not None: sp.clip_below(clip)
    sp.outline(INK, 2)


def sign20(sp, k=1.0):
    """a speed-limit «20» sign on a crooked pole, stuck in the ground right where the patrol stands"""
    sp.line((0.0, 0.0), (1.0, 34.0), (150, 150, 156), 2)
    sp.ell(1.0, 40.0, 8.0, 8.0, tones((220, 40, 40)))
    sp.ell(1.0, 40.0, 6.0, 6.0, tones((246, 246, 240)), ol=False)
    sp.ptext('20', 1.0, 44.0, INK, size=6, center=True)
    sp.outline(INK, 2)


def bush(sp, w=30.0, seed=1):
    rng = np.random.default_rng(seed)
    parts = [sp.m_ell(-w / 2 + i * w / 4 + rng.random() * 3, 6 + rng.random() * 8, 7 + rng.random() * 4, 6 + rng.random() * 4) for i in range(5)]
    sp.union(parts, tones((70, 100, 50)))
    for i in range(14):
        sp.dot(-w / 2 + rng.random() * w, 4 + rng.random() * 14, (120, 150, 60))
    sp.outline(INK, 2)


def still(sp, t=0.0, shake=0.0, gauge=0.2, level=0.0, drop=-1.0):
    """the home-made «biofuel» rig: brass samovar + pressure cooker + gauge + copper coil into a glass jar; a bucket of husks.
    shake 0..1 rattles it, gauge 0..1 moves the needle into the red, level = golden liquid in the jar, drop 0..1 = a falling drop"""
    j = shake * math.sin(t * 60.0) * 1.2
    sp.ell(-26.0, 6.0, 7.0, 6.0, tones((140, 140, 150)))                     # bucket of sunflower husks
    sp.rect(-32.0, 10.0, -20.0, 13.0, (40, 36, 30))
    for k in range(6): sp.dot(-31.0 + k * 2, 12.5 + (k % 2), (230, 228, 210))
    body = sp.union([sp.m_ell(0.0 + j, 18.0, 12.0, 14.0), sp.m_ell(0.0 + j, 32.0, 7.0, 3.0)], tones((214, 150, 60)))   # samovar
    sp.rect(-9.0 + j, 2.0, 9.0 + j, 5.0, tones((180, 120, 50))[1])
    sp.line((11.0 + j, 14.0), (16.0 + j, 12.0), (180, 120, 50), 2)          # tap
    pot = sp.sup(0.0 + j, 40.0, 10.0, 6.0, tones((170, 174, 184)), n=3.0)   # pressure cooker
    sp.rect(-11.0 + j, 46.0, 11.0 + j, 48.0, (90, 92, 100))
    gx, gy = 0.0 + j, 53.0                                                   # gauge
    sp.ell(gx, gy, 4.5, 4.5, tones((246, 246, 240)))
    sp.fill(sp.m_ell(gx, gy, 4.0, 4.0)[0] & (DX.XC > gx + 1.5) & (DX.YC > gy - 1), (220, 60, 60))
    a = math.radians(160 - 150 * gauge)
    sp.line((gx, gy), (gx + math.cos(a) * 3.4, gy + math.sin(a) * 3.4), INK)
    for k in range(5):                                                       # copper coil down to the jar
        y = 44.0 - k * 6.0
        sp.line((10.0 + j, 44.0 - k * 6.0 + 3), (24.0, y), (200, 110, 60), 2)
        sp.line((24.0, y), (14.0 + j, y - 3), (170, 90, 50), 2)
    sp.line((24.0, 18.0), (30.0, 14.0), (200, 110, 60), 2)
    jar = sp.m_super(32.0, 6.0, 6.0, 7.0, 3.0)[0]                           # glass jar
    sp.fill(jar, (150, 190, 210)); sp.fill(jar & (DX.YC < 0.0 + 13.0 * level), (240, 200, 70))
    sp.fill(jar & ~erode(jar), INK)
    if 0 <= drop <= 1:
        sp.ell(30.0, 14.0 - drop * 7.0, 1.2, 1.6, tones((250, 210, 70)))
    sp.anchors['steam'] = (0.0 + j, 50.0); sp.anchors['jar'] = (32.0, 8.0)
    sp.outline(INK, 2)
