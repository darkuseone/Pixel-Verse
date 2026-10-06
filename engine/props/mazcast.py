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
            awe=dict(eo=1.3, pu=0.75, bt=-0.5, bl=0.7, mo=0.3, mc=0.1, round_mouth=True))


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
        far_hold=True):
    """Мазутыч, 3/4 to the right. ride: standing on the monowheel (feet on the pedals at y 13); wind: mustache flutter 0..1;
    steer: steering-wheel angle; blinker 0..1: the near arm sticks out and flaps (a mouth-clicked turn signal)"""
    E = X(expr)
    if blink is None: blink = (t % 3.7) < 0.12
    B = 13.0 if ride else 0.0
    br = 0.6 * math.sin(t * 2.2)                                              # breathing
    # ---------------------------------------------------------------- far boot + leg
    sp.sup(-2.0, B + 6.0, 4.0, 6.0, tones(dark(RUBBER, 0.8)), n=2.4)
    sp.ell(1.0, B + 2.2, 5.0, 2.4, tones(dark(RUBBER, 0.8)))
    sp.cap((-2.0, B + 11.0), (-0.5, B + 24.0), 3.6, 4.0, tones(ROBE_D))
    if ride and wheel:
        monowheel(sp, t, spin, face=wheel_face, dead=dead)
    # ---------------------------------------------------------------- far arm (behind the torso)
    shF = (0.5, B + 57.0 + br * 0.4)
    wc = (32.0, B + 45.5)                                                     # steering wheel centre
    hF = (wc[0] - 2.0 + 3.0 * math.sin(steer), wc[1] + 10.0 - 1.5 * abs(math.sin(steer))) if far_hold else (8.0, B + 30.0)
    kF, eF = ik(shF, hF, 12.0, 11.5, -1.0)
    sp.cap(shF, kF, 3.4, 3.0, tones(ROBE_D)); sp.cap(kF, eF, 3.0, 2.6, tones(ROBE_D))
    glove(sp, *eF)
    # ---------------------------------------------------------------- near leg + boot
    sp.cap((5.0, B + 11.0), (3.5, B + 24.0), 3.8, 4.2, tones(ROBE))
    sp.sup(5.0, B + 6.0, 4.2, 6.0, tones(RUBBER), n=2.4)
    sp.ell(8.2, B + 2.2, 5.4, 2.6, tones(RUBBER))
    sp.line((1.5, B + 10.0), (8.5, B + 10.0), (90, 100, 86))                  # boot rim
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
    # ---------------------------------------------------------------- steering wheel + near arm
    sp.outline(INK, 2)                                                        # the double ink line goes around the body before the wheel
    before = sp.m.copy()
    shN = (9.0, B + 56.0 + br * 0.4)
    if hold:
        steering(sp, *wc, steer=steer)
    if blinker > 0:                                                           # near arm out to the side, hand flaps: «щёлк-щёлк»
        flap = math.sin(t * 22.0) * 2.0 * blinker
        hN = (shN[0] + 21.0 * blinker + 4.0, shN[1] + 3.0 + flap)
    else:
        hN = (wc[0] + 1.5 - 3.0 * math.sin(steer), wc[1] + 10.0 + 1.0 * math.sin(steer))
    kN, eN = ik(shN, hN, 12.0, 11.5, -1.0)
    sp.cap(shN, kN, 3.6, 3.2, tones(ROBE)); sp.cap(kN, eN, 3.2, 2.8, tones(ROBE))
    sp.fill(sp.m_cap(kN, eN, 3.2, 2.8)[0] & (np.abs(DX.YC - (kN[1] + eN[1]) / 2) < 1.0), STRIPE)   # sleeve stripe
    glove(sp, *eN, flat=blinker > 0)
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


def zoya(sp, t=0.0, expr='deadpan', mouth_=0.0, mega=False, mega_up=1.0, gum=0.0, look=(0.3, 0.0), blink=None, chew=True):
    """Зоя from the waist up (y 0 = desk line): pyramid body, aubergine beehive tower, gold hoops, blue eyeshadow, megaphone"""
    E = X(expr)
    if blink is None: blink = (t % 4.1) < 0.12
    br = 0.5 * math.sin(t * 2.0)
    body = sp.union([sp.m_ell(0.0, 6.0, 22.0, 18.0), sp.m_ell(0.0, 20.0 + br * 0.3, 17.0, 10.0)], tones(JACKET))
    sp.poly([(-3.0, 30.0), (5.0, 30.0), (1.0, 18.0)], tones((236, 236, 230)))                  # shirt V
    sp.line((1.0, 18.0), (1.0, 0.0), INK)
    sp.rect(8.0, 16.0, 16.0, 20.0, (240, 240, 232)); sp.line((9, 18), (15, 18), (60, 60, 70))   # name tag
    sp.ell(-9.0, 18.0, 3.2, 3.6, tones((176, 120, 210)))                                          # onion logo «ЛУК-ОЙ»
    sp.line((-9.0, 21.0), (-9.5, 23.5), (90, 190, 70)); sp.line((-9.0, 21.0), (-8.0, 23.5), (90, 190, 70))
    sp.dot(-10.0, 16.6, (120, 200, 255))                                                          # the onion's tear
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
    sp.anchors['front'] = (121.0, 12.0)
    sp.outline(INK, 2)


def hatch_mask_():
    return MX.hatch_mask(3)


CAR_COLS = [(232, 228, 214), (196, 60, 52), (206, 186, 140), (100, 46, 80), (70, 120, 170), (86, 132, 90)]


def lada(sp, col=(232, 228, 214), t=0.0, honk=0.0, rust=0, spin=0.0, driver=True):
    """boxy Soviet sedan «six», side view facing +x, ~64 px long"""
    body = sp.m_poly([(-30.0, 6.0), (32.0, 6.0), (33.0, 14.0), (30.0, 17.0), (12.0, 18.0), (6.0, 27.0), (-14.0, 27.0), (-20.0, 18.0),
                      (-30.0, 17.0), (-31.0, 12.0)])
    sp.paint(body, tones(col), DX.lit(np.clip(DX.XC / 32, -1, 1) * 0.3, np.clip((DX.YC - 16) / 11, -1, 1)))
    w1 = sp.m_poly([(-12.0, 19.0), (-3.0, 19.0), (-3.0, 25.5), (-12.0, 25.5), (-17.0, 19.0)])
    w2 = sp.m_poly([(-1.0, 19.0), (10.0, 19.0), (5.0, 25.5), (-1.0, 25.5)])
    for w in (w1, w2):
        sp.fill(w, (150, 190, 214)); sp.fill(w & hatch_mask_(), (110, 150, 180)); sp.fill(w & ~erode(w), INK)
    if driver: sp.ell(3.0, 21.0, 2.4, 2.8, tones((40, 34, 40)), ol=False, clip=w2)
    sp.line((-30.0, 12.0), (33.0, 12.0), dark(col, 0.65))
    sp.rect(31.0, 6.0, 35.0, 9.0, (200, 200, 196)); sp.rect(-33.0, 6.0, -29.0, 9.0, (200, 200, 196))   # chrome bumpers
    sp.rect(30.5, 12.0, 33.0, 15.0, (255, 240, 190))                           # headlight
    sp.rect(-31.0, 12.0, -29.5, 15.0, (220, 40, 40))
    sp.rect(-4.0, 13.0, -1.0, 14.0, INK)
    if rust:
        rng = np.random.default_rng(rust)
        for k in range(6): sp.dot(-28 + rng.random() * 56, 7 + rng.random() * 6, (150, 80, 40))
    for x in (-19.0, 20.0): _wheel(sp, x, 5.0, 5.2, spin)
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


def monowheel_solo(sp, t=0.0, spin=0.0, face='smile'):
    """the wheel alone (model sheet, inserts)"""
    monowheel(sp, t, spin, face=face if face != 'dead' else 'smile', dead=face == 'dead')
    sp.outline(INK, 2)
