"""«Grim Ride» cast in the «Lantern Stipple» manner (props/grimpix.py): GRIM (Death) + his rented Class-3 e-bike, EDGAR the raven,
HAROLD (97) + his unlocked e-trike / rocking chair, TODD (decoration dad), KAYDEN and the masked e-bike gang, KEVIN the 12-ft skeleton,
yard props (inflatable pumpkin, countdown sign, tarp).
Coordinates: sprite px, feet anchor at the origin, +x = facing side, y up. Every draw fn takes the Spr first."""
import math
import numpy as np
from props import dibspix as DX
from props import grimpix as GX
from props.grimpix import INK, tones, stroke, stipple_fill
from props.dibspix import EXPR, ik, dark, mix, erode, dilate

CLOAK = (44, 36, 66)
BONE = (236, 226, 198)
GLOW = (150, 255, 110)             # Death's eye glow (toxic green)
FRAME = (226, 232, 236)            # the cheap e-bike: white frame, lime accents
LIME = (170, 240, 60)
TYRE = (34, 32, 40)
STEEL = (150, 156, 170)
FEATHER = (66, 62, 104)
BEAK = (70, 66, 80)
PACK = (90, 230, 150)              # Edgar's tiny fanny pack (the plug's stash)

CLK = [(14, 8, 26), (28, 20, 48), (50, 40, 78), (132, 70, 120)]       # cloak: depth, shadow, base, plum lantern-glow
CLKF = [(10, 6, 20), (22, 16, 40), (40, 32, 64), (104, 56, 98)]

XTRA = dict(
    proud=dict(eo=1.0, pu=0.55, bt=0.3, bl=0.4, mo=0.3, mc=0.4),
    menace=dict(eo=0.8, pu=0.35, bt=0.9, bl=-0.4, mo=0.0, mc=-0.3, lid=0.2),
    whine=dict(eo=1.1, pu=0.7, bt=-0.8, bl=0.6, mo=0.5, mc=-0.6),
    bored=dict(eo=0.8, pu=0.55, bt=0.05, bl=0.0, mo=0.0, mc=-0.1, lid=0.45),
    awe=dict(eo=1.3, pu=0.75, bt=-0.5, bl=0.7, mo=0.3, mc=0.1, round_mouth=True),
    hype=dict(eo=1.2, pu=0.6, bt=-0.4, bl=0.7, mo=0.6, mc=1.0, teeth=True),
    pity=dict(eo=0.9, pu=0.6, bt=-0.6, bl=0.4, mo=0.0, mc=0.3),
)


FONT = dict(DX.FONT3)
FONT.update(N=['1001', '1101', '1011', '1001', '1001'], M=['10001', '11011', '10101', '10001', '10001'],
            W=['10001', '10001', '10101', '11011', '10001'], K=['1001', '1010', '1100', '1010', '1001'])


def txt(sp, s_, i0, j0, c, keep=True):
    """tiny pixel font (3x5, wider N/M/W/K), top-left at (i0, j0); pre-mirrored on flipped sprites"""
    x = i0
    tw = sum(len(FONT.get(ch.upper(), FONT[' '])[0]) + 1 for ch in s_) - 1
    mir = getattr(sp, 'mirror_text', False)
    for ch in s_:
        g = FONT.get(ch.upper(), FONT[' '])
        for r, row in enumerate(g):
            for k, b in enumerate(row):
                if b == '1':
                    xx = x + k
                    if mir: xx = 2 * i0 + tw - 1 - xx
                    sp.dot(xx, j0 - r, c, keep)
        x += len(g[0]) + 1
    return tw


def X(expr):
    return dict(XTRA.get(expr) or EXPR.get(expr, EXPR['normal']))


def vgrad(y_top, y_bot, side=0.0, lo=0.18, hi=0.86):
    """lit value for flat parts under a lantern held low: brighter towards the bottom (and the facing side)"""
    k = np.clip((y_top - DX.YC) / max(1e-3, y_top - y_bot), 0, 1)
    return np.clip(lo + (hi - lo) * k + side * np.clip(DX.XC / 40.0, -1, 1), 0, 0.999).astype(np.float32)


def _wheel(sp, x, y, r, spin, tyre=TYRE, rim=STEEL, spokes=10, hub=STEEL, fat=2.4):
    sp.ell(x, y, r, r, tones(tyre))
    inner = sp.m_ell(x, y, r - fat, r - fat)[0]
    sp.fill(inner, (20, 14, 30))
    ang = np.arctan2(DX.YC - y, DX.XC - x)
    tread = (np.floor((ang + spin) / (2 * math.pi) * 26) % 2) == 0
    sp.fill(sp.m_ell(x, y, r, r)[0] & ~sp.m_ell(x, y, r - 0.9, r - 0.9)[0] & tread, dark(tyre, 0.6))
    sp.fill(inner & ~sp.m_ell(x, y, r - fat - 1.0, r - fat - 1.0)[0], rim)
    for k in range(spokes):
        a = spin + k * 2 * math.pi / spokes
        sp.line((x, y), (x + math.cos(a) * (r - fat - 0.6), y + math.sin(a) * (r - fat - 0.6)), dark(rim, 0.75))
    sp.ell(x, y, 1.6, 1.6, tones(hub), ol=False)
    sp.dot(x, y, INK)


def crescent(sp, top, d=1, k=1.0):
    """the scythe blade: a thin crescent hooking from the top of the shaft, d = +1 to the right, -1 to the left"""
    out, inn = [], []
    for i in range(13):
        q = i / 12
        a = math.pi * 0.5 * q
        out.append((top[0] + d * 34 * k * math.sin(a), top[1] + 4 * k - 22 * k * (1 - math.cos(a)) + 2 * k * q))
        inn.append((top[0] + d * 30 * k * math.sin(a) * (1 - 0.15 * q), top[1] - 2.2 * k - 17 * k * (1 - math.cos(a)) * q))
    m = sp.m_poly(out + inn[::-1])
    sp.paint(m, tones((200, 208, 226), glow=(255, 200, 160)), vgrad(top[1] + 4 * k, top[1] - 20 * k, 0.0, 0.35, 0.95))
    sp.line((top[0] + d * 3 * k, top[1] + 2.2 * k), (top[0] + d * 26 * k, top[1] - 4 * k), (252, 252, 255))
    sp.rect(top[0] - 2.0 * k, top[1] - 2.5 * k, top[0] + 2.0 * k, top[1] + 3.0 * k, (60, 60, 70))
    return m


# ======================================================================================== the e-bike «PALE HORSE 2» (rented, 13%)
BIKE = dict(rw=(-24.0, 12.0), fw=(27.0, 12.0), r=11.5, bb=(0.0, 13.0), seat=(-9.0, 37.0), head=(19.0, 36.0), bar=(15.0, 49.0))


def ebike(sp, t=0.0, spin=0.0, crank=0.0, batt=13, dead=False, scythe=True, far=True):
    """cheap white step-through-ish Class-3 e-bike, lime accents, rear rack with the scythe zip-tied on, display on the bar"""
    B = BIKE
    rw, fw, bb, seat, head = B['rw'], B['fw'], B['bb'], B['seat'], B['head']
    if scythe:                                                                # the scythe: zip-tied diagonally to the rear rack
        a, b = (-38.0, 22.0), (-14.0, 108.0)
        sp.cap(a, b, 1.3, 1.3, tones((120, 84, 52)))
        blade = crescent(sp, (-14.0, 108.0), -1, 1.0)
        for y in (30.0, 36.0):                                                # zip ties
            xx = a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1])
            sp.rect(xx - 2.0, y - 0.6, xx + 2.2, y + 0.8, (20, 20, 24))
            sp.dot(xx + 2.2, y + 0.8, (20, 20, 24)); sp.dot(xx + 3.2, y + 1.6, (20, 20, 24))
    if far:                                                                   # far crank arm + pedal
        ca = crank + math.pi
        p = (bb[0] + 5.5 * math.cos(ca), bb[1] + 5.5 * math.sin(ca))
        sp.line(bb, p, (60, 60, 70), 1); sp.rect(p[0] - 2, p[1] - 0.6, p[0] + 2, p[1] + 0.8, (50, 50, 60))
    _wheel(sp, *rw, B['r'], spin)
    _wheel(sp, *fw, B['r'], spin)
    tub = tones(FRAME, glow=(255, 200, 150))
    sp.cap(bb, rw, 1.5, 1.5, tub)                                             # chainstay
    sp.cap((seat[0] + 1.0, seat[1] - 4.0), rw, 1.1, 1.1, tub)                 # seatstay
    sp.cap((-30.0, 31.0), (-7.0, 32.0), 0.9, 0.9, tones(STEEL))              # rear rack
    sp.cap((-30.0, 31.0), (-27.0, 13.0), 0.7, 0.7, tones(STEEL))
    sp.cap(bb, (seat[0] + 1.0, seat[1] - 3.0), 1.5, 1.5, tub)                 # seat tube
    sp.cap(bb, head, 2.6, 2.2, tub)                                           # down tube (fat)
    # battery pack on the down tube with the «13%» sticker
    bat = sp.m_cap((3.0, 18.0), (14.5, 31.0), 4.0, 4.0)
    sp.paint(bat[0], tones((70, 74, 88)), DX.lit(bat[1], bat[2]))
    sp.fill(bat[0] & (np.abs((DX.XC - 3.0) * 0.75 - (DX.YC - 18.0) * 0.66) < 0.6), LIME)
    led = (255, 70, 60) if batt < 10 else LIME
    if not dead:
        sp.fill(sp.m_cap((6.0, 20.0), (8.5, 23.0), 0.7, 0.7)[0], led, keep=True)
    txt(sp, f'{batt}%', 4.0, 27.0, (255, 236, 120) if not dead else (120, 110, 100))
    sp.cap(head, (head[0] + 1.5, head[1] + 9.0), 1.6, 1.6, tub)               # head tube
    sp.cap((head[0] - 0.5, head[1]), fw, 1.1, 1.1, tones(STEEL))              # fork
    sp.fill(sp.m_cap((head[0] - 0.5, head[1]), fw, 1.4, 1.4)[0] & (np.abs(DX.YC - 24) < 1.5), LIME)   # lime fork band
    # saddle + post, fender over the rear wheel
    sp.cap((seat[0] + 1.0, seat[1] - 3.5), (seat[0], seat[1]), 0.8, 0.8, tones(STEEL))
    sp.ell(seat[0] - 1.0, seat[1] + 0.8, 5.0, 1.8, tones((40, 36, 46)))
    fen = sp.m_ell(*rw, B['r'] + 2.2, B['r'] + 2.2)[0] & ~sp.m_ell(*rw, B['r'] + 1.0, B['r'] + 1.0)[0] & (DX.YC > rw[1] + 3) & (DX.XC < rw[0] + 6)
    sp.paint(fen, tones(FRAME), vgrad(26, 14))
    # stem, handlebar, display, headlight
    st = (head[0] + 1.5, head[1] + 9.0)
    sp.cap(st, (st[0] - 1.0, st[1] + 3.0), 1.0, 1.0, tones(STEEL))
    sp.cap((st[0] - 1.0, st[1] + 3.0), B['bar'], 1.0, 1.0, tones((50, 50, 58)))
    sp.rect(st[0] - 0.5, st[1] + 1.5, st[0] + 4.0, st[1] + 4.6, INK)
    sp.rect(st[0] + 0.3, st[1] + 2.2, st[0] + 3.4, st[1] + 4.0, (30, 60, 40) if not dead else (10, 10, 14), keep=True)
    if not dead and int(t * 3) % 2 == 0: sp.dot(st[0] + 1.5, st[1] + 3.0, (255, 80, 60), keep=True)
    sp.ell(head[0] + 4.0, head[1] + 5.0, 1.8, 1.4, tones((240, 236, 200)), ol=True)
    # chainring + near crank + pedal
    sp.ell(*bb, 3.4, 3.4, tones((70, 70, 80)))
    p = (bb[0] + 5.5 * math.cos(crank), bb[1] + 5.5 * math.sin(crank))
    sp.line(bb, p, (90, 90, 100), 1); sp.rect(p[0] - 2.2, p[1] - 0.6, p[0] + 2.2, p[1] + 0.9, (70, 70, 80))
    sp.line((bb[0] - 2.0, bb[1] + 2.6), (rw[0], rw[1] + 1.2), (60, 56, 70)); sp.line((bb[0] - 2.0, bb[1] - 2.6), (rw[0], rw[1] - 1.2), (60, 56, 70))
    sp.anchors.update(bike_bar=B['bar'], bike_display=(st[0] + 2.0, st[1] + 3.0), bike_seat=seat, rear=(rw[0], 0.5), front=(fw[0], 0.5))
    return p


# ======================================================================================== GRIM (Death)
def bony_hand(sp, x, y, d=1.0, grip=True, point=False):
    """palm + four long finger bones; d = +1 fingers forward (+x)"""
    sp.ell(x, y, 2.4, 2.0, tones(BONE))
    if grip:                                                                  # fingers curled round a grip
        for k in range(4):
            sp.line((x + d * 1.5, y + 1.2 - k * 0.9), (x + d * 3.6, y + 0.2 - k * 0.9), dark(BONE, 0.8))
        sp.line((x + d * 3.6, y + 1.0), (x + d * 3.6, y - 2.4), INK)
    elif point:
        sp.line((x + d * 1.5, y + 0.8), (x + d * 7.5, y + 1.4), BONE); sp.line((x + d * 1.5, y + 0.2), (x + d * 7.5, y + 0.8), dark(BONE, 0.7))
        for k in range(3): sp.line((x + d * 1.4, y - 0.6 - k * 0.8), (x + d * 2.8, y - 1.6 - k * 0.8), dark(BONE, 0.75))
    else:                                                                     # open claw, fingers spread
        for k in range(4):
            a = -0.5 + k * 0.38
            sp.line((x + d * 1.4, y), (x + d * (1.4 + 5.0 * math.cos(a)), y + 5.0 * math.sin(a)), BONE)
            sp.dot(x + d * (1.4 + 5.0 * math.cos(a)), y + 5.0 * math.sin(a), dark(BONE, 0.6))
    sp.line((x - d * 1.8, y - 0.4), (x - d * 0.4, y - 1.6), dark(BONE, 0.6))


def skull(sp, hx, hy, E, mouth_=0.0, look=(0.6, 0.0), blink=False, glow=1.0, hs=1.0, jaw_drop=0.0):
    """the face: bone skull 3/4 right in the hood opening, glowing eyes in deep sockets, floating brow ridges, clacking jaw"""
    def Hp(dx, dy): return (hx + dx * hs, hy + dy * hs)
    mo = max(mouth_, E['mo'])
    drop = (1.2 + 3.4 * mo + jaw_drop) * hs
    # jaw (behind the cranium): drops when talking
    jaw = sp.union([sp.m_ell(*Hp(2.6, -6.0), 4.6 * hs, 2.8 * hs, -0.1)], tones(BONE))
    jm = sp.m_ell(*Hp(2.6, -6.0), 4.6 * hs, 2.8 * hs, -0.1)[0]
    if drop > 0.5:                                                            # move the jaw down: redraw shifted
        sp.m &= ~(jm & ~sp.m_ell(*Hp(0.0, 0.0), 7.2 * hs, 7.6 * hs)[0])
        jaw = sp.union([sp.m_ell(hx + 2.6 * hs, hy - 6.0 * hs - drop, 4.6 * hs, 2.6 * hs, -0.1)], tones(BONE))
        sp.fill(sp.m_poly([Hp(-1.0, -4.6), Hp(6.4, -4.6), (hx + 6.4 * hs, hy - 4.6 * hs - drop), (hx - 1.0 * hs, hy - 4.6 * hs - drop)]),
                (16, 6, 24))
        for k in range(4):                                                    # lower teeth
            x = hx + (0.0 + k * 1.6) * hs
            sp.rect(x, hy - 4.8 * hs - drop, x + 1.0 * hs, hy - 3.6 * hs - drop, BONE, keep=True)
        if mo > 0.6:                                                          # a tongue-less void with a violet glow
            sp.fill(sp.m_ell(hx + 2.6 * hs, hy - 5.2 * hs - drop * 0.5, 2.0 * hs, drop * 0.3)[0], (70, 30, 90))
    # cranium + cheekbone
    cr = sp.union([sp.m_ell(*Hp(0.0, 0.5), 7.0 * hs, 7.6 * hs), sp.m_ell(*Hp(3.0, -3.0), 4.8 * hs, 3.6 * hs, -0.2)], tones(BONE))
    stipple_fill(sp, cr & (DX.XC < hx - 3.5 * hs) & erode(cr), dark(BONE, 0.7), 0.3)
    stroke(sp, [Hp(-4.0, 5.5), Hp(-2.0, 6.2)], dark(BONE, 0.62))             # a hairline crack (character)
    stroke(sp, [Hp(-2.0, 6.2), Hp(-1.5, 4.6)], dark(BONE, 0.62))
    # upper teeth
    for k in range(5):
        x = hx + (-0.6 + k * 1.5) * hs
        sp.rect(x, hy - 4.6 * hs, x + 1.1 * hs, hy - 3.0 * hs, BONE, keep=True)
        sp.line((x + 1.2 * hs, hy - 4.6 * hs), (x + 1.2 * hs, hy - 3.0 * hs), dark(BONE, 0.55))
    sp.line(Hp(-1.0, -4.7), Hp(6.5, -4.7), INK)
    # nose cavity (upside-down heart)
    sp.fill(sp.m_poly([Hp(3.4, -0.6), Hp(5.0, -0.6), Hp(4.6, -2.4), Hp(4.0, -2.8)]), (20, 8, 30))
    # eye sockets + glowing eyes
    lx, ly = look
    for (ex, ew, eh, near) in ((4.6, 4.6, 4.4, True), (-1.6, 3.8, 4.2, False)):
        cx, cy = Hp(ex, 1.6)
        sp.fill(sp.m_ell(cx, cy, ew * 0.66 * hs, eh * 0.66 * hs)[0], (18, 6, 28))
        if glow > 0:
            g = tuple(int(c * (0.45 + 0.55 * glow)) for c in GLOW)
            DX.eye(sp, cx, cy, ew * 1.0 * hs, eh * 0.95 * hs, E, g, (lx, ly), blink, lash=(18, 6, 28), skin=BONE,
                   white=mix(g, (255, 255, 255), 0.55), lidc=(18, 6, 28))
    # floating brow ridges (bone): they carry the anger / hurt
    DX.brow(sp, *Hp(4.6, 5.2), 5.6 * hs, E, +1, (96, 70, 104), th=2)
    DX.brow(sp, *Hp(-1.6, 5.2), 4.6 * hs, E, -1, (80, 58, 90), th=2)
    sp.anchors['skull'] = (hx, hy)


def hood(sp, hx, hy, wind=0.0, t=0.0, hs=1.0):
    """the question-mark hood: a tall cowl hooking forward over the face; returns the opening mask"""
    def Hp(dx, dy): return (hx + dx * hs, hy + dy * hs)
    fl = wind * math.sin(t * 17.0) * 0.8
    parts = [sp.m_ell(*Hp(-3.0, 1.0), 11.5 * hs, 12.5 * hs, 0.1), sp.m_ell(*Hp(-1.0, 11.0), 8.0 * hs, 7.0 * hs, -0.3)]
    tip = sp.m_poly([Hp(-8.0, 12.0), Hp(-3.0, 19.0), Hp(4.0, 20.0 + fl), Hp(10.0, 17.0 + fl), Hp(12.5, 12.0 + fl), Hp(9.5, 13.0),
                     Hp(6.0, 14.0), Hp(2.0, 11.0)])
    cowl = sp.union(parts, CLK, exclude=None)
    sp.paint(tip | cowl, CLK, vgrad(hy + 20 * hs, hy - 12 * hs, 0.1))
    stroke(sp, [Hp(-7.0, 10.0), Hp(-2.0, 15.0), Hp(5.0, 16.0)], mix(CLOAK, INK, 0.5))    # a fold line of the hook
    op = sp.m_ell(*Hp(3.2, -0.5), 8.0 * hs, 9.2 * hs, 0.08)[0]
    sp.fill(op & sp.m, (14, 6, 22))
    sp.fill(op & ~erode(op) & (DX.YC > hy + 2 * hs), mix(CLOAK, (150, 186, 255), 0.25))    # moonlit rim of the opening
    return op


GRIM_STYLE = dict(hs=1.25)


def grim(sp, t=0.0, expr='proud', mouth_=0.0, look=(0.6, 0.0), blink=None, ride=True, spin=0.0, crank=None, wind=0.0, batt=13, dead=False,
         raven=False, raven_mouth=0.0, raven_expr='deadpan', pose='bar', glow=1.0, scythe=True, jaw_drop=0.0, hood_back=0.0, shake=0.0,
         lean=0.0, carry=0.0):
    """GRIM, 3/4 to the right. ride: on the e-bike (pose 'bar' = both hands on the bar, 'phone' = near hand holds a phone up,
    'shout' = near arm raised with an open claw); ride=False: standing, cloak to the ground, scythe upright in the far hand
    (pose 'stand' / 'point' / 'claw' / 'phone' / 'loom' = arms raised over a victim). wind 0..1: cloak and tatters stream back."""
    E = X(expr)
    if blink is None: blink = (t % 4.3) < 0.1
    if crank is None: crank = spin * 0.6
    hs = GRIM_STYLE['hs']
    br = 0.5 * math.sin(t * 2.0)
    sh = shake * math.sin(t * 40.0)
    if ride:
        pedal = ebike(sp, t, spin, crank, batt, dead, scythe)
        hip = (-6.0, 40.0)
        # bony shins down to the pedals (the cloak covers the thighs)
        for k, ph in ((1, crank + math.pi), (0, crank)):
            p = (BIKE['bb'][0] + 5.5 * math.cos(ph), BIKE['bb'][1] + 5.5 * math.sin(ph) + 1.0)
            kn, ft = ik(hip, p, 15.0, 15.0, 1.0)
            c = dark(BONE, 0.7) if k else BONE
            sp.line(kn, ft, c, 1); sp.line((kn[0] + 0.8, kn[1]), (ft[0] + 0.8, ft[1]), dark(c, 0.8), 1)
            sp.ell(ft[0] + 1.4, ft[1] + 0.6, 2.6, 1.0, tones(c))
        base = (-4.0, 38.0)
    else:
        base = (-2.0, 0.0)
    # ---------------------------------------------------------------- the cloak tail streaming in the wind (behind)
    if wind > 0.05 or not ride:
        rng = np.random.default_rng(5)
        tail = [(-10.0, 72.0 if ride else 80.0)]
        n = 6
        for k in range(n + 1):
            q = k / n
            x = -14.0 - (26.0 + 8.0 * wind) * wind * (0.4 + 0.6 * q) - (0 if ride else 4.0 * q)
            y = (70.0 - 34.0 * q if ride else 78.0 - 74.0 * q) + wind * 4.0 * math.sin(t * 13.0 + q * 5.0)
            tail.append((x, y))
        rag = []
        for k in range(5):                                                     # ragged hem tatters
            q = 1.0 - k / 4
            rag.append((tail[-1][0] + 6.0 * k + rng.random() * 2, tail[-1][1] - (3.0 + rng.random() * 3) * (k % 2)))
        tail += rag + [(-4.0, base[1] + (2.0 if ride else 0.0))]
        sp.poly(tail, CLK, val=vgrad(80, base[1], 0.0, 0.1, 0.7))
    # ---------------------------------------------------------------- far arm (sleeve + bony hand)
    if ride:
        shF = (2.0, 66.0 + br * 0.3); hF = (BIKE['bar'][0] - 2.0, BIKE['bar'][1] + 0.5)
    else:
        shF = (-2.0, 70.0 + br * 0.3); hF = (-13.0, 46.0)
    kF, eF = ik(shF, hF, 14.0, 13.0, -1.0)
    sp.cap(shF, kF, 3.6, 3.6, CLKF); sp.cap(kF, eF, 3.6, 4.6, CLKF)
    if not ride and scythe:                                                   # the scythe upright in the far hand
        sp.cap((eF[0] - 0.5, -2.0), (eF[0] + 1.0, 112.0), 1.3, 1.3, tones((120, 84, 52)))
        top = (eF[0] + 1.0, 112.0)
        crescent(sp, top, +1, 1.0)
    bony_hand(sp, *eF, d=1.0, grip=True)
    # ---------------------------------------------------------------- body: the cloak
    if ride:
        parts = [sp.m_ell(-5.0, 44.0, 12.0, 8.0), sp.m_ell(-1.0 + lean * 0.3, 58.0 + br * 0.3, 11.5, 13.0, -0.35),
                 sp.m_ell(4.0 + lean * 0.6, 68.0 + br * 0.5, 9.0, 6.0, -0.4)]
        body = sp.union(parts, CLK)
        hem = sp.m_poly([(-16.0, 42.0), (8.0, 40.0), (12.0, 32.0), (9.0, 33.5), (6.0, 30.0), (3.0, 33.0), (-1.0, 29.0), (-4.0, 33.0),
                         (-8.0, 30.0), (-11.0, 34.0), (-16.0, 33.0)])
        sp.paint(hem, CLK, vgrad(42, 29, 0.0, 0.3, 0.95))
        stroke(sp, [(-8.0, 46.0), (-4.0, 36.0)], mix(CLOAK, INK, 0.5)); stroke(sp, [(2.0, 50.0), (4.0, 38.0)], mix(CLOAK, INK, 0.5))
        neck = (8.0 + lean, 72.0 + br * 0.5)
    else:
        pts = [(-10.0, 82.0), (6.0, 82.0), (12.0, 60.0), (15.0, 30.0), (18.0, 0.0), (14.0, 2.0), (10.0, -0.5), (6.0, 2.0), (2.0, -0.5),
               (-3.0, 2.0), (-8.0, -0.5), (-12.0, 2.0), (-17.0, 0.0), (-15.0, 30.0), (-14.0, 60.0)]
        sp.paint(sp.m_poly(pts), CLK, vgrad(82, 0, 0.12, 0.12, 0.92))
        for x0, x1 in ((-4.0, -7.0), (5.0, 8.0), (10.0, 14.0)):
            stroke(sp, [(x0, 60.0), (x1, 4.0)], mix(CLOAK, INK, 0.5))
        sp.ell(9.0, -0.5, 3.0, 1.2, tones(BONE)); sp.ell(-6.0, -0.5, 2.6, 1.1, tones(dark(BONE, 0.8)))     # bony toes under the hem
        neck = (4.0 + lean, 84.0 + br * 0.5)
    # ---------------------------------------------------------------- hood + skull
    hx, hy = neck[0] + 9.0 * hs + sh, neck[1] + 8.0 * hs
    op = hood(sp, hx - 3.0 * hs, hy, wind, t, hs)
    skull(sp, hx + 0.6 * hs, hy - 0.8 * hs, E, mouth_, look, blink, glow, hs * 0.9, jaw_drop)
    sp.anchors['head'] = (hx, hy)
    sp.anchors['eyes'] = (hx + 2.0 * hs, hy + 1.0 * hs)
    sp.anchors['hood_top'] = (hx - 3.0 * hs, hy + 18.0 * hs)
    sp.outline(INK, 1)
    # ---------------------------------------------------------------- near arm (over the body)
    before = sp.m.copy()
    shN = (neck[0] + 1.0, neck[1] - 6.0)
    if pose in ('ear', 'twophones'):
        hN = (hx - 3.5 * hs, hy - 1.5 * hs)
    elif ride and pose == 'phone':
        hN = (shN[0] + 12.0, shN[1] + 6.0)
    elif ride and pose == 'shout':
        hN = (shN[0] + 8.0, shN[1] + 20.0)
    elif ride:
        hN = (BIKE['bar'][0] + 1.0, BIKE['bar'][1] + 1.0)
    elif pose == 'point':
        hN = (shN[0] + 22.0, shN[1] + 2.0)
    elif pose == 'claw':
        hN = (shN[0] + 12.0, shN[1] + 16.0)
    elif pose == 'loom':
        hN = (shN[0] + 3.0, shN[1] + 26.0)
    elif pose == 'phone':
        hN = (shN[0] + 12.0, shN[1] + 4.0)
    else:
        hN = (shN[0] + 6.0, shN[1] - 22.0)
    kN, eN = ik(shN, hN, 13.0, 12.0, -1.0 if not (pose in ('claw', 'loom', 'shout', 'ear', 'twophones')) else 1.0)
    sp.cap(shN, kN, 3.8, 3.8, CLK); sp.cap(kN, eN, 3.8, 5.0, CLK)
    if pose in ('phone',):
        bony_hand(sp, *eN, d=1.0, grip=False)
        sp.rect(eN[0] + 0.5, eN[1] - 1.0, eN[0] + 4.5, eN[1] + 7.0, (30, 30, 40))
        sp.rect(eN[0] + 1.2, eN[1] - 0.2, eN[0] + 3.8, eN[1] + 6.2, (120, 255, 200), keep=True)
        sp.dot(eN[0] + 2.0, eN[1] + 4.6, (240, 60, 60), keep=True)
        sp.anchors['phone'] = (eN[0] + 2.5, eN[1] + 3.0)
    elif pose in ('ear', 'twophones'):                                        # phone pressed to the side of the skull
        sp.rect(eN[0] - 1.5, eN[1] - 4.0, eN[0] + 2.5, eN[1] + 5.0, (30, 30, 40))
        sp.rect(eN[0] - 0.8, eN[1] - 3.2, eN[0] + 1.8, eN[1] + 4.2, (120, 255, 200), keep=True)
        bony_hand(sp, eN[0] + 0.5, eN[1] - 2.0, d=1.0, grip=True)
        sp.anchors['phone'] = (eN[0] + 0.5, eN[1])
        if pose == 'twophones':                                               # the second phone held at the jaw
            px, py = hx + 8.5 * hs, hy - 7.5 * hs
            sp.cap((shN[0] + 2.0, shN[1] - 4.0), (px - 2.0, py - 3.0), 3.4, 4.2, CLK)
            sp.rect(px - 2.5, py - 4.5, px + 1.5, py + 4.5, (30, 30, 40))
            sp.rect(px - 1.8, py - 3.8, px + 0.8, py + 3.8, (255, 200, 90), keep=True)
            bony_hand(sp, px - 1.0, py - 3.0, d=1.0, grip=True)
            sp.anchors['phone2'] = (px, py)
    else:
        bony_hand(sp, *eN, d=1.0, grip=(ride and pose == 'bar') or pose == 'stand', point=pose == 'point')
        if carry: sack(sp, eN[0] + 1.0, eN[1] - 1.0, carry)
    sp.anchors['hand'] = eN
    sp.anchors['pocket'] = (neck[0] - 3.0, neck[1] - 20.0)
    new = sp.m & ~before
    o = dilate(new) if sp.k == 1 else dilate(dilate(new))
    o &= ~sp.m
    sp.col[o] = INK; sp.m |= o
    if raven:
        r = sp.anchors.get('bike_display', (22.0, 48.0))
        raven_on(sp, r[0] + 1.5, r[1] + 1.6, 0.62, t=t, expr=raven_expr, mouth_=raven_mouth, look=(-0.8, 0.0))


# ======================================================================================== EDGAR the raven
def raven_on(sp, x0, y0, k=1.0, t=0.0, expr='deadpan', mouth_=0.0, look=(1.0, 0.0), blink=None, flap=0.0, bag=True, cam=False, gesture=None):
    """Edgar standing at (x0, y0) (his feet), k = scale. cam=True: head turned to the camera (both eyes)"""
    E = X(expr)
    if blink is None: blink = (t % 3.3) < 0.1
    def Q(dx, dy): return (x0 + dx * k, y0 + dy * k)
    fe = tones(FEATHER, k=0.30, glow=(210, 120, 200))
    # tail
    sp.poly([Q(-4.0, 5.0), Q(-14.0, -1.0), Q(-12.0, 3.0), Q(-15.0, 2.0), Q(-6.0, 10.0)], fe, val=vgrad(y0 + 10 * k, y0, 0.0, 0.1, 0.6))
    # legs + claws
    for dx in (-1.0, 2.0):
        sp.line(Q(dx, 4.0), Q(dx + 0.5, 0.2), (80, 74, 70))
        sp.line(Q(dx - 1.5, 0.0), Q(dx + 2.5, 0.0), (80, 74, 70))
    # body
    body = sp.union([sp.m_ell(*Q(0.0, 9.0), 7.0 * k, 7.6 * k, -0.2), sp.m_ell(*Q(3.0, 13.0), 5.0 * k, 5.0 * k)], fe)
    if bag:                                                                   # the tiny fanny pack (the plug's stash)
        sp.fill(body & (np.abs(DX.YC - (y0 + 6.0 * k)) < 0.7 * max(1, k)), (30, 30, 34))
        sp.ell(*Q(4.0, 5.6), 2.4 * k, 1.8 * k, tones(PACK))
        sp.line(Q(2.4, 6.4), Q(5.6, 6.4), dark(PACK, 0.5))
    # wing (with a gesture: 'up' = a wing raised like a hand)
    if gesture == 'up':
        sp.poly([Q(-2.0, 13.0), Q(4.0, 26.0), Q(8.0, 27.0), Q(3.0, 16.0), Q(2.0, 9.0)], fe, val=vgrad(y0 + 27 * k, y0 + 8 * k, 0.0, 0.2, 0.7))
    else:
        sp.ell(*Q(-2.0, 9.0 + flap * 2.0), 5.0 * k, 5.5 * k, tones(dark(FEATHER, 0.85), k=0.3, glow=(210, 120, 200)), ang=-0.4 - flap * 0.8)
        for j in range(3): stroke(sp, [Q(-5.0 + j * 1.6, 7.0 - j), Q(-8.0 + j * 1.2, 4.0 - j)], mix(FEATHER, INK, 0.6))
    # head
    hx, hy = Q(4.0, 18.5)
    sp.ell(hx, hy, 5.4 * k, 5.2 * k, fe)
    for j in range(3):                                                        # messy crest
        sp.line((hx - (2.0 - j * 1.6) * k, hy + 4.4 * k), (hx - (3.2 - j * 1.8) * k, hy + (7.2 - j * 0.6) * k), FEATHER, max(1, int(k)))
    # beak: big, the lower half opens with speech
    mo = max(mouth_, E['mo'])
    bx, by = hx + 3.4 * k, hy - 0.4 * k
    if cam:
        bx = hx + 0.6 * k
    up = sp.m_poly([(bx, by + 2.0 * k), (bx + 10.0 * k, by - 1.2 * k), (bx, by - 1.0 * k)])
    sp.paint(up, tones(BEAK, glow=(255, 190, 120)), vgrad(by + 2 * k, by - 1 * k, 0.0, 0.3, 0.9))
    lo = sp.m_poly([(bx, by - 1.0 * k), (bx + 8.0 * k, by - 1.6 * k - mo * 3.0 * k), (bx, by - 3.0 * k - mo * 2.0 * k)])
    sp.paint(lo, tones(dark(BEAK, 0.85)), vgrad(by, by - 4 * k, 0.0, 0.3, 0.9))
    if mo > 0.15:
        sp.fill(sp.m_poly([(bx, by - 1.0 * k), (bx + 7.0 * k, by - 1.3 * k), (bx + 6.0 * k, by - 1.4 * k - mo * 2.4 * k),
                           (bx, by - 2.6 * k - mo * 1.4 * k)]), (150, 60, 90))
    sp.dot(bx + 1.6 * k, by + 0.6 * k, INK)                                    # nostril
    # eye(s): white with a small pupil, heavy deadpan lid, one tufty brow
    lx, ly = look
    if cam:
        for ex, w in ((hx - 1.8 * k, 2.8), (hx + 2.4 * k, 3.0)):
            DX.eye(sp, ex, hy + 1.2 * k, w * k, 2.8 * k, E, (40, 30, 30), (lx, ly), blink, lash=INK, skin=FEATHER, lidc=dark(FEATHER, 0.8))
        DX.brow(sp, hx + 2.4 * k, hy + 3.8 * k, 3.4 * k, E, +1, (20, 18, 30), th=max(1, int(k)))
        DX.brow(sp, hx - 1.8 * k, hy + 3.8 * k, 3.0 * k, E, -1, (20, 18, 30), th=max(1, int(k)))
    else:
        DX.eye(sp, hx + 1.2 * k, hy + 1.4 * k, 4.4 * k, 3.8 * k, E, (40, 30, 30), (lx, ly), blink, lash=INK, skin=FEATHER, lidc=dark(FEATHER, 0.8))
        DX.brow(sp, hx + 1.2 * k, hy + 4.0 * k, 3.8 * k, E, +1, (20, 18, 30), th=max(1, int(k)))
    sp.anchors['raven_head'] = (hx, hy)
    sp.anchors['raven_beak'] = (bx + 4 * k, by)


def edgar(sp, t=0.0, expr='deadpan', mouth_=0.0, look=(1.0, 0.0), blink=None, flap=0.0, bag=True, cam=False, gesture=None, perch=True):
    """Edgar alone (close-ups): standing on a short branch / handlebar stub"""
    if perch:
        sp.cap((-14.0, -0.5), (16.0, -0.5), 1.4, 1.4, tones((70, 70, 80)))
    raven_on(sp, 0.0, 0.0, 1.0, t, expr, mouth_, look, blink, flap, bag, cam, gesture)
    sp.anchors['head'] = sp.anchors['raven_head']
    sp.outline(INK, 1)


# ======================================================================================== HAROLD (97) + e-trike + rocking chair
HSKIN = (226, 178, 150)
CARDI = (200, 160, 70)            # mustard cardigan
PANTS = (176, 160, 120)           # khaki, belted at the chest
SUSP = (200, 50, 50)
HELM = (28, 26, 34)
FLAME = (255, 120, 30)


def flames(sp, mask, x0, x1, y0, k=1.0):
    """orange/yellow flame decal licking right->left inside mask"""
    for i in range(int((x1 - x0) / (5 * k)) + 1):
        x = x0 + i * 5 * k
        tri = sp.m_poly([(x, y0), (x + 4.5 * k, y0), (x - 4.0 * k, y0 + (3.0 + (i % 2) * 2.0) * k)])
        sp.fill(tri & mask, FLAME)
        tri2 = sp.m_poly([(x + 1.0 * k, y0), (x + 3.5 * k, y0), (x - 1.0 * k, y0 + (1.6 + (i % 2)) * k)])
        sp.fill(tri2 & mask, (255, 220, 70))


def trike(sp, t=0.0, spin=0.0, flag=1.0, unlocked=True):
    """black e-trike: one front wheel, two rear wheels, chopper ape-hanger bars, bucket seat, orange safety flag, flame decals"""
    _wheel(sp, -15.0, 9.0, 8.0, spin * 0.9, tyre=dark(TYRE, 0.8), spokes=8)                 # far rear wheel (peeks above)
    pole_top = (-26.0, 66.0)
    sp.line((-22.0, 14.0), pole_top, (180, 180, 190), 1)
    fl = 2.5 * math.sin(t * 9.0) * flag
    flagm = sp.m_poly([pole_top, (pole_top[0] - 13.0, pole_top[1] - 3.5 + fl), (pole_top[0], pole_top[1] - 7.0)])
    sp.paint(flagm, tones((255, 110, 30)), vgrad(pole_top[1], pole_top[1] - 7))
    ch = sp.m_poly([(-24.0, 8.0), (-18.0, 15.0), (10.0, 14.0), (22.0, 20.0), (24.0, 16.0), (12.0, 7.0), (-10.0, 5.0)])
    sp.paint(ch, tones(HELM, glow=(160, 120, 200)), vgrad(20, 5, 0.1, 0.25, 0.85))
    flames(sp, ch, -18.0, 12.0, 6.0)
    sp.rect(-22.0, 14.0, -8.0, 22.0, (40, 40, 50)); sp.line((-22, 22), (-8, 22), INK)        # battery box
    sp.dot(-10.0, 19.0, LIME, keep=True)
    if unlocked:
        sp.rect(-58.0, 40.0, -24.0, 47.0, (250, 230, 60))                                    # placard on the flag pole
        sp.line((-58.0, 40.0), (-24.0, 40.0), INK); sp.line((-58.0, 47.0), (-24.0, 47.0), INK)
        txt(sp, 'UNLOCKED', -56.0, 45.0, (200, 20, 30))
    sp.sup(-11.0, 22.0, 7.0, 6.0, tones((70, 30, 30)), n=2.2)                                 # bucket seat
    sp.sup(-16.0, 30.0, 3.0, 9.0, tones((70, 30, 30)), n=2.2)                                 # backrest
    sp.cap((19.0, 18.0), (24.0, 9.0), 1.3, 1.3, tones(STEEL))                                 # fork
    _wheel(sp, 24.0, 9.0, 8.0, spin, spokes=8)
    _wheel(sp, -18.0, 8.0, 8.0, spin * 0.9, spokes=8)                                         # near rear wheel
    sp.cap((19.0, 18.0), (16.0, 38.0), 1.2, 1.2, tones(STEEL))                                # ape-hanger bars
    sp.cap((16.0, 38.0), (10.0, 38.5), 1.2, 1.2, tones(STEEL))
    sp.ell(22.0, 19.0, 2.2, 1.8, tones((255, 240, 190)))                                      # headlight
    sp.anchors.update(trike_seat=(-10.0, 25.0), trike_grip=(10.5, 38.5), trike_flag=pole_top, front=(24.0, 0.5), rear=(-18.0, 0.5))


def rocking_chair(sp, rock=0.0):
    WOOD = (130, 80, 46)
    sp.cap((-14.0, 0.5), (12.0, 0.5 + rock), 1.3, 1.3, tones(WOOD))                           # rocker
    for x in (-10.0, 8.0): sp.line((x, 1.0), (x + 1.0, 18.0), dark(WOOD, 0.8), 1)
    sp.rect(-12.0, 17.0, 10.0, 20.0, WOOD)                                                    # seat
    sp.cap((-12.0, 18.0), (-15.0, 52.0), 1.6, 1.6, tones(WOOD))                               # back posts
    for y in (28.0, 36.0, 44.0): sp.line((-13.0, y), (-15.0, y + 2.0), dark(WOOD, 0.7), 2)


def harold(sp, t=0.0, expr='bored', mouth_=0.0, look=(0.6, 0.0), blink=None, pose='stand', spin=0.0, flag=1.0, rock=0.0, wave=0.0,
           toss=0.0, wind=0.0, offer=0.0):
    """HAROLD, 97: a tiny shrivelled «bobblehead» under a giant black helmet with flames, coke-bottle glasses magnifying the eyes,
    khaki pants belted at the chest, red suspenders, white orthopedic sneakers. pose 'stand' / 'rock' (rocking chair) / 'ride' (e-trike)"""
    E = X(expr)
    if blink is None: blink = (t % 3.9) < 0.12
    sit = pose in ('rock', 'ride')
    if pose == 'ride':
        trike(sp, t, spin, flag)
        ox, oy = sp.anchors['trike_seat']
    elif pose == 'rock':
        rocking_chair(sp, rock)
        ox, oy = (-2.0, 19.0)
    else:
        ox, oy = (0.0, 0.0)
    # legs + sneakers
    if sit:
        hip = (ox, oy + 1.0)
        for k, (kn, ft) in enumerate((((ox + 9.0, oy + 3.0), (ox + 11.0, oy - 8.0)), ((ox + 10.0, oy + 4.0), (ox + 13.0, oy - 7.0)))):
            if pose == 'ride': ft = (ft[0] + 6.0, ft[1] + 2.0)
            c = dark(PANTS, 0.8) if k == 0 else PANTS
            sp.cap(hip, kn, 3.0, 2.4, tones(c)); sp.cap(kn, ft, 2.0, 1.6, tones(c))
            sp.rect(ft[0] - 1.6, ft[1] - 1.0, ft[0] + 1.6, ft[1] + 1.0, (246, 246, 240))      # socks
            sp.sup(ft[0] + 1.6, ft[1] - 2.0, 3.4, 1.8, tones((246, 244, 236)), n=2.2)
            sp.line((ft[0] + 0.2, ft[1] - 1.4), (ft[0] + 3.2, ft[1] - 1.4), (150, 160, 190))     # velcro
        base = oy
    else:
        for k, dx in enumerate((-2.5, 2.5)):
            c = dark(PANTS, 0.8) if k == 0 else PANTS
            sp.cap((dx * 0.6, 22.0), (dx, 6.0), 2.6, 2.0, tones(c))
            sp.rect(dx - 1.6, 3.0, dx + 1.8, 6.0, (246, 246, 240))
            sp.sup(dx + 1.4, 1.8, 3.4, 1.9, tones((246, 244, 236) if k else (220, 218, 212)), n=2.2)
            sp.line((dx, 2.6), (dx + 3.0, 2.6), (150, 160, 190))
        base = 20.0
    # torso: pants pulled up to the chest, cardigan, suspenders
    hx0 = ox + 1.0
    body = sp.union([sp.m_ell(hx0, base + 6.0, 6.2, 5.0), sp.m_ell(hx0 + 0.5, base + 13.0, 5.4, 6.0)], tones(CARDI))
    pants = body & (DX.YC < base + 10.0)
    sp.paint(pants, tones(PANTS), vgrad(base + 10, base, 0.1))
    sp.rect(hx0 - 5.0, base + 9.0, hx0 + 6.0, base + 10.4, (60, 40, 30))                     # the belt, at the chest
    sp.rect(hx0 + 1.5, base + 9.0, hx0 + 3.0, base + 10.4, (230, 200, 90))
    for dx in (-2.0, 3.0): sp.line((hx0 + dx, base + 10.4), (hx0 + dx + 0.6, base + 18.0), SUSP)
    sp.rect(hx0 + 4.0, base + 13.0, hx0 + 5.4, base + 15.0, (110, 40, 120))                  # raisin box in the breast pocket
    # arms: skinny, big knuckly hands (liver spots)
    shN = (hx0 + 3.0, base + 17.0)
    if pose == 'ride':
        hN = sp.anchors['trike_grip']
    elif wave > 0:
        hN = (shN[0] + 6.0 + 2.0 * math.sin(t * 14.0) * wave, shN[1] + 9.0)
    elif toss > 0:
        hN = (shN[0] + 9.0, shN[1] + 2.0 + 8.0 * toss)
    elif offer > 0:
        hN = (shN[0] + 10.0 * offer + 2.0, shN[1] - 2.0)
    elif pose == 'rock':
        hN = (shN[0] + 5.0, shN[1] - 9.0)
    else:
        hN = (shN[0] + 3.0, shN[1] - 11.0)
    kN, eN = ik(shN, hN, 7.0, 7.0, -1.0)
    sp.cap(shN, kN, 2.0, 1.6, tones(CARDI)); sp.cap(kN, eN, 1.6, 1.2, tones(HSKIN))
    sp.ell(*eN, 2.2, 1.9, tones(HSKIN)); sp.dot(eN[0] - 0.6, eN[1] + 0.6, (176, 120, 90))
    sp.anchors['hand'] = eN
    # head: small wrinkly face, giant ears, big nose, white tufty brows, coke-bottle glasses
    hx, hy = hx0 + 3.0, base + 27.0
    sp.cap((hx0 + 1.5, base + 18.0), (hx - 0.5, hy - 5.0), 2.0, 2.0, tones(HSKIN))
    sp.ell(hx - 7.4, hy + 0.5, 3.0, 4.6, tones(HSKIN))                                        # big ear
    sp.dot(hx - 6.6, hy + 0.5, dark(HSKIN, 0.6)); sp.dot(hx - 7.4, hy + 2.6, (230, 230, 230))  # ear hair
    face = sp.union([sp.m_ell(hx, hy, 7.2, 8.0), sp.m_ell(hx + 1.5, hy - 5.2, 4.6, 3.4)], tones(HSKIN))
    for j in range(3): sp.line((hx - 4.0, hy - 2.0 - j * 1.6), (hx - 2.0, hy - 2.6 - j * 1.6), dark(HSKIN, 0.68))   # cheek wrinkles
    sp.line((hx + 2.0, hy - 2.0), (hx + 1.0, hy - 6.0), dark(HSKIN, 0.62))
    DX.blush(sp, hx + 3.5, hy - 2.5, 1.8, 1.2, (230, 120, 110))
    lx, ly = look
    for ex, w, side in ((hx + 3.4, 3.8, 1), (hx - 1.6, 3.4, -1)):
        lens = sp.m_ell(ex, hy + 1.6, w * 0.7, w * 0.7)[0]
        sp.fill(lens, (232, 238, 246))
        DX.eye(sp, ex, hy + 1.6, w, w * 0.92, E, (90, 120, 150), (lx, ly), blink, lash=(60, 40, 40), skin=(232, 238, 246),
               lidc=mix(HSKIN, (232, 238, 246), 0.4))
        sp.fill(lens & ~erode(lens), (150, 120, 70))                                          # gold wire rims
        sp.dot(ex + w * 0.3, hy + 1.6 + w * 0.35, (255, 255, 255), keep=True)                 # lens glint
        DX.brow(sp, ex, hy + 1.6 + w * 0.7 + 0.8, w + 1.0, E, side, (236, 236, 232), th=2, bushy=True)
    sp.line((hx + 0.6, hy + 2.0), (hx + 1.6, hy + 2.0), (150, 120, 70))                       # bridge
    sp.ell(hx + 5.6, hy - 1.6, 2.4, 2.6, tones((214, 150, 130)))                              # nose
    sp.dot(hx + 6.4, hy - 3.0, dark(HSKIN, 0.5))
    DX.mouth(sp, hx + 3.0, hy - 5.0, 4.4, E, mouth_, (150, 80, 80), inside=(90, 20, 30), skin=HSKIN, maxh=4, big_teeth=True)
    # the giant helmet with flames
    hm = sp.m_ell(hx - 0.5, hy + 8.0, 11.5, 9.5, -0.1)[0] & (DX.YC > hy + 6.0 + (DX.XC - hx) * 0.12)
    sp.paint(hm, tones(HELM, glow=(170, 120, 210)), DX.lit(np.clip((DX.XC - hx) / 11, -1, 1), np.clip((DX.YC - hy - 8) / 9.5, -1, 1)))
    flames(sp, hm, hx - 10.0, hx + 10.0, hy + 7.0, 1.0)
    for k in range(3): sp.line((hx - 4.0 + k * 3.0, hy + 16.5), (hx - 3.0 + k * 3.0, hy + 13.5), (60, 60, 70))   # vents
    sp.rect(hx + 4.0, hy + 6.4, hx + 13.0, hy + 7.8, HELM)                                     # visor
    sp.line((hx - 5.0, hy + 4.0), (hx - 2.0, hy - 7.0), (40, 40, 44))                          # chin strap
    sp.anchors['head'] = (hx, hy)
    sp.outline(INK, 1)


# ======================================================================================== TODD (decoration dad)
TSKIN = (238, 186, 150)
TEE = (255, 130, 40)
CARGO = (170, 150, 104)
CAP = (200, 40, 50)


def todd(sp, t=0.0, expr='hype', mouth_=0.0, look=(0.6, 0.0), blink=None, phone=True, point=0.0, walk=None):
    """TODD: a «pear» — narrow shoulders, wide hips in khaki cargo shorts, socks + sandals, teal fanny pack, orange SPOOKY tee,
    backwards red cap with sunglasses on it, goatee; phone held up (filming everything)"""
    E = X(expr)
    if blink is None: blink = (t % 3.5) < 0.11
    br = 0.5 * math.sin(t * 2.4)
    sw = math.sin(walk) * 2.5 if walk is not None else 0.0
    for k, dx in enumerate((-4.0, 5.0)):                                                      # hairy calves, socks, sandals
        s_ = sw if k else -sw
        c = dark(TSKIN, 0.85) if k == 0 else TSKIN
        sp.cap((dx * 0.8, 22.0), (dx + s_, 6.0), 3.2, 2.6, tones(c))
        stipple_fill(sp, sp.m_cap((dx * 0.8, 20.0), (dx + s_, 9.0), 2.6, 2.0)[0], (90, 60, 50), 0.12)
        sp.rect(dx + s_ - 2.2, 2.0, dx + s_ + 2.4, 8.0, (246, 246, 240))                     # white tube socks
        sp.line((dx + s_ - 2.2, 7.0), (dx + s_ + 2.4, 7.0), (60, 120, 220))
        sp.sup(dx + s_ + 1.5, 1.2, 4.4, 1.6, tones((90, 60, 40)), n=2.2)                      # sandal
        sp.line((dx + s_ - 1.0, 3.0), (dx + s_ + 2.0, 1.4), (60, 40, 30))
    hips = sp.union([sp.m_ell(0.5, 26.0, 13.0, 9.0), sp.m_ell(1.0, 20.0, 11.0, 5.0)], tones(CARGO))
    for dx in (-10.0, 9.0):                                                                   # cargo pockets
        sp.rect(dx - 2.0, 17.0, dx + 2.5, 23.0, dark(CARGO, 0.85)); sp.line((dx - 2, 23), (dx + 2.5, 23), INK)
    tee = sp.union([sp.m_ell(1.0, 38.0, 10.0, 9.0), sp.m_ell(1.5, 46.0 + br * 0.3, 8.6, 6.0)], tones(TEE))
    sp.ell(3.0, 40.0, 3.6, 3.0, tones((40, 20, 40)), ol=False)                                # jack-o'-lantern print
    sp.dot(2.0, 41.0, TEE); sp.dot(4.0, 41.0, TEE); sp.rect(1.5, 38.6, 4.6, 39.4, TEE); sp.dot(3.0, 43.4, (60, 120, 40))
    sp.rect(-9.0, 29.0, 12.0, 31.0, (30, 30, 34))                                            # fanny pack strap
    sp.sup(6.0, 29.5, 5.0, 3.0, tones((40, 200, 200)), n=2.4); sp.line((2.0, 30.0), (10.0, 30.0), dark((40, 200, 200), 0.5))
    # far arm
    sp.cap((-6.0, 48.0), (-9.0, 36.0), 2.6, 2.4, tones(dark(TSKIN, 0.85))); sp.ell(-9.5, 34.5, 2.4, 2.2, tones(dark(TSKIN, 0.85)))
    # head
    hx, hy = 4.0, 60.0
    sp.cap((2.0, 50.0), (3.0, 54.0), 3.4, 3.4, tones(TSKIN))
    sp.ell(hx - 6.6, hy, 2.0, 3.0, tones(TSKIN))
    face = sp.union([sp.m_ell(hx, hy, 7.0, 7.6), sp.m_ell(hx + 1.0, hy - 5.0, 5.4, 3.6)], tones(TSKIN))
    DX.stubble(sp, face & (DX.YC < hy - 2.0), dark(TSKIN, 0.7), 0.35, 2)
    sp.ell(hx + 3.0, hy - 7.6, 2.4, 1.8, tones((110, 70, 40)))                               # goatee
    lx, ly = look
    DX.eye(sp, hx + 3.2, hy + 1.4, 4.2, 3.8, E, (70, 120, 70), (lx, ly), blink, lash=INK, skin=TSKIN)
    DX.eye(sp, hx - 2.0, hy + 1.4, 3.6, 3.6, E, (70, 120, 70), (lx, ly), blink, lash=INK, skin=TSKIN)
    DX.brow(sp, hx + 3.2, hy + 4.6, 4.6, E, +1, (110, 70, 40), th=1)
    DX.brow(sp, hx - 2.0, hy + 4.6, 4.0, E, -1, (110, 70, 40), th=1)
    sp.ell(hx + 6.0, hy - 1.0, 2.0, 1.8, tones(TSKIN)); sp.dot(hx + 6.4, hy - 2.2, dark(TSKIN, 0.55))
    DX.mouth(sp, hx + 3.0, hy - 4.6, 5.0, E, mouth_, (170, 70, 70), skin=TSKIN, maxh=5)
    cap = sp.m_ell(hx - 0.5, hy + 5.0, 7.6, 4.8)[0] & (DX.YC > hy + 4.0)
    sp.paint(cap, tones(CAP), DX.lit(np.clip((DX.XC - hx) / 8, -1, 1), np.clip((DX.YC - hy - 5) / 5, -1, 1)))
    sp.cap((hx - 7.0, hy + 5.0), (hx - 11.0, hy + 4.0), 1.2, 1.2, tones(CAP))               # bill backwards
    sp.rect(hx + 1.0, hy + 7.0, hx + 7.0, hy + 8.4, (20, 20, 26)); sp.dot(hx + 3.5, hy + 8.0, (120, 220, 255))   # shades on the cap
    sp.anchors['head'] = (hx, hy)
    sp.outline(INK, 1)
    # near arm: phone up (filming) or pointing
    before = sp.m.copy()
    shN = (6.0, 48.0 + br * 0.3)
    hN = (shN[0] + 10.0, shN[1] + 8.0) if phone else ((shN[0] + 14.0, shN[1] + 2.0) if point else (shN[0] + 3.0, shN[1] - 13.0))
    kN, eN = ik(shN, hN, 7.0, 7.0, -1.0)
    sp.cap(shN, kN, 2.8, 2.6, tones(TSKIN)); sp.cap(kN, eN, 2.6, 2.2, tones(TSKIN))
    sp.ell(*eN, 2.4, 2.2, tones(TSKIN))
    if phone:
        sp.rect(eN[0] - 1.0, eN[1] - 0.5, eN[0] + 2.5, eN[1] + 6.5, (30, 30, 40))
        sp.rect(eN[0] - 0.4, eN[1] + 0.2, eN[0] + 1.9, eN[1] + 5.8, (120, 200, 255), keep=True)
        sp.dot(eN[0] + 0.7, eN[1] + 6.0, (255, 60, 60), keep=True)                            # REC
    elif point:
        sp.line((eN[0] + 1.6, eN[1]), (eN[0] + 4.6, eN[1] + 0.4), TSKIN, 1)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


# ======================================================================================== KAYDEN + the masked e-bike gang
HOODIE = (54, 54, 68)
MASK = (22, 20, 26)


def moto(sp, t=0.0, spin=0.0, col=(30, 30, 36)):
    """a chunky electric dirt bike (moped-sized), knobby tyres, big battery box, long seat, wide bars"""
    _wheel(sp, -22.0, 10.0, 10.0, spin, fat=3.4, spokes=12)
    _wheel(sp, 25.0, 10.0, 10.0, spin, fat=3.4, spokes=12)
    sp.cap((-22.0, 10.0), (-4.0, 18.0), 1.8, 1.8, tones(STEEL))                               # swingarm
    sp.cap((25.0, 10.0), (18.0, 34.0), 1.6, 1.6, tones((200, 160, 40)))                       # gold fork
    frame = sp.m_poly([(-10.0, 18.0), (-14.0, 30.0), (14.0, 32.0), (18.0, 34.0), (12.0, 18.0)])
    sp.paint(frame, tones(col, glow=(160, 120, 210)), vgrad(34, 18, 0.1))
    sp.rect(-6.0, 20.0, 8.0, 28.0, (60, 64, 76)); sp.fill(sp.m_poly([(-5, 21), (7, 21), (7, 22), (-5, 22)]), LIME)
    sp.sup(-12.0, 32.0, 10.0, 2.0, tones((24, 24, 28)), n=3.0)                                 # long seat
    sp.cap((18.0, 34.0), (16.0, 41.0), 1.2, 1.2, tones(STEEL))
    sp.cap((12.0, 42.0), (20.0, 41.0), 1.2, 1.2, tones((30, 30, 34)))                         # bars
    sp.ell(21.0, 33.0, 2.0, 2.0, tones((240, 250, 255)))                                      # headlight
    sp.anchors.update(moto_bar=(14.0, 42.0), moto_peg=(-2.0, 16.0), moto_seat=(-10.0, 34.0), rear=(-22.0, 0.5))


def kayden(sp, t=0.0, expr='bored', mouth_=0.0, look=(0.7, 0.0), blink=None, spin=0.0, col=HOODIE, string=LIME, bike=True, n=0):
    """KAYDEN (13) on the dirt e-bike: standing on the pegs, black hoodie up, a skull-print balaclava (only the eyes show),
    joggers, chunky white sneakers. col / string recolour the hoodie for the gang members"""
    E = X(expr)
    if blink is None: blink = ((t + n * 1.3) % 3.1) < 0.1
    if bike: moto(sp, t, spin)
    peg = sp.anchors.get('moto_peg', (0.0, 0.0))
    hip = (peg[0] - 3.0, peg[1] + 21.0)
    for k, dx in enumerate((-1.0, 1.5)):                                                      # joggers + sneakers
        c = dark((60, 60, 70), 0.8) if k == 0 else (60, 60, 70)
        ft = (peg[0] + dx * 2, peg[1] + 1.0)
        kn = (hip[0] + 9.0, hip[1] - 9.0)
        sp.cap(hip, kn, 3.4, 3.0, tones(c)); sp.cap(kn, ft, 3.0, 2.4, tones(c))
        sp.sup(ft[0] + 1.5, ft[1] - 0.5, 4.6, 2.2, tones((248, 248, 248) if k else (220, 220, 224)), n=2.2)
        sp.line((ft[0] - 2.0, ft[1] - 1.2), (ft[0] + 5.0, ft[1] - 1.2), (200, 40, 50))
    body = sp.union([sp.m_ell(hip[0] + 2.0, hip[1] + 8.0, 8.0, 9.0, -0.3), sp.m_ell(hip[0] + 5.0, hip[1] + 15.0, 8.0, 6.0, -0.4)], tones(col, glow=(160, 110, 200)))
    sp.rect(hip[0] + 1.0, hip[1] + 4.0, hip[0] + 9.0, hip[1] + 8.0, dark(col, 0.8))          # kangaroo pocket
    sp.line((hip[0] + 9.0, hip[1] + 17.0), (hip[0] + 9.5, hip[1] + 11.0), string)             # drawstrings
    sp.line((hip[0] + 11.0, hip[1] + 17.0), (hip[0] + 11.5, hip[1] + 12.0), string)
    hx, hy = hip[0] + 8.0, hip[1] + 25.0
    sp.ell(hx - 1.0, hy, 7.6, 8.0, tones(col, glow=(160, 110, 200)))                          # hood
    mk = sp.union([sp.m_ell(hx + 1.0, hy - 0.5, 5.8, 6.6)], tones(MASK))
    # skull print on the mask: white sockets, nose, teeth
    sp.fill(mk & sp.m_ell(hx + 3.6, hy + 1.2, 2.6, 2.4)[0], (236, 236, 228))
    sp.fill(mk & sp.m_ell(hx - 0.8, hy + 1.2, 2.2, 2.2)[0], (220, 220, 214))
    sp.fill(mk & sp.m_poly([(hx + 1.2, hy - 1.0), (hx + 2.6, hy - 1.0), (hx + 1.9, hy - 2.4)]), (236, 236, 228))
    for k in range(4): sp.rect(hx - 1.0 + k * 1.6, hy - 5.0, hx - 0.2 + k * 1.6, hy - 3.6, (236, 236, 228))
    lx, ly = look
    DX.eye(sp, hx + 3.6, hy + 1.2, 3.4, 2.6, E, (110, 70, 40), (lx, ly), blink, lash=INK, skin=MASK, lidc=(200, 150, 120))
    DX.eye(sp, hx - 0.8, hy + 1.2, 3.0, 2.4, E, (110, 70, 40), (lx, ly), blink, lash=INK, skin=MASK, lidc=(200, 150, 120))
    sp.anchors['head'] = (hx, hy)
    bar = sp.anchors.get('moto_bar', (hip[0] + 16.0, hip[1] + 8.0))
    for k in (0, 1):                                                                          # arms to the bars
        sh = (hip[0] + 6.0 - k, hip[1] + 16.0)
        kk, ee = ik(sh, (bar[0] + k, bar[1]), 8.0, 8.0, -1.0)
        c = dark(col, 0.85) if k else col
        sp.cap(sh, kk, 2.6, 2.4, tones(c)); sp.cap(kk, ee, 2.4, 2.2, tones(c))
        if k == 0: sp.fill(sp.m_cap(kk, ee, 2.4, 2.2)[0] & (np.abs(DX.XC - (kk[0] + ee[0]) / 2) < 0.8), string)   # reflective sleeve band
        sp.ell(ee[0], ee[1], 1.8, 1.8, tones((40, 40, 46)))                                   # gloves
    sp.outline(INK, 1)


# ======================================================================================== KEVIN the 12-ft skeleton + yard props
def kevin(sp, t=0.0, look=(0.0, 0.0), turn=0.0, eyes_on=True, wave=0.0):
    """the store-bought 12-ft yard skeleton (Home Despot), LCD eyes; turn rotates the head (looks down/at someone)"""
    E = dict(EXPR['blank']); E['eo'] = 1.0
    b = tones((228, 222, 206), glow=(255, 170, 110))
    for dx in (-8.0, 8.0):                                                                     # legs (on stakes)
        sp.line((dx, 0.0), (dx, -6.0), (90, 90, 100), 1)
        sp.cap((dx * 0.7, 66.0), (dx, 36.0), 2.4, 2.0, b); sp.cap((dx, 36.0), (dx, 4.0), 2.0, 1.8, b)
        sp.ell(dx + 2.0, 2.0, 4.0, 2.0, b)
    sp.ell(0.0, 68.0, 11.0, 6.0, b)                                                            # pelvis
    sp.fill(sp.m_ell(0.0, 67.0, 4.0, 3.0)[0], (16, 8, 24))
    sp.cap((0.0, 70.0), (0.0, 110.0), 2.0, 2.0, b)                                             # spine
    for k in range(6):                                                                         # ribs
        y = 106.0 - k * 5.5
        w = 14.0 - abs(k - 2) * 1.6
        rib = sp.m_ell(0.0, y, w, 2.8)[0] & ~sp.m_ell(0.0, y + 0.6, w - 1.8, 1.8)[0]
        sp.paint(rib, b, vgrad(y + 3, y - 3))
    sp.cap((-16.0, 112.0), (16.0, 112.0), 2.0, 2.0, b)                                         # shoulders
    for sd in (-1, 1):
        el = (sd * 22.0, 86.0); hd = (sd * 22.0 + (sd * 6.0 if wave and sd > 0 else 0.0), 62.0 + (40.0 * wave if sd > 0 else 0.0))
        sp.cap((sd * 16.0, 112.0), el, 2.2, 2.0, b); sp.cap(el, hd, 2.0, 1.8, b)
        for f in range(4): sp.line(hd, (hd[0] + sd * (f - 1.5) * 1.6, hd[1] - 6.0), (228, 222, 206))
    hx, hy = 2.0 + 6.0 * turn, 128.0 - 3.0 * abs(turn)
    sp.cap((0.0, 112.0), (hx * 0.5, hy - 8.0), 2.0, 2.0, b)
    sp.union([sp.m_ell(hx, hy, 12.0, 13.0), sp.m_ell(hx + 2.0 * turn, hy - 9.0, 8.0, 5.0)], b)
    g = (255, 150, 40) if eyes_on else (60, 40, 30)
    for ex in (hx - 4.5 + 2.0 * turn, hx + 4.5 + 2.0 * turn):
        sp.fill(sp.m_ell(ex, hy + 1.0, 3.6, 4.0)[0], (16, 8, 24))
        DX.eye(sp, ex, hy + 1.0, 5.0, 5.0, E, g, (look[0] + turn, look[1] - abs(turn) * 0.6), False, lash=(16, 8, 24),
               skin=(228, 222, 206), white=mix(g, (255, 255, 220), 0.5))
    sp.fill(sp.m_poly([(hx + 2.0 * turn - 1.5, hy - 3.0), (hx + 2.0 * turn + 1.5, hy - 3.0), (hx + 2.0 * turn, hy - 6.0)]), (16, 8, 24))
    for k in range(6): sp.rect(hx - 5.0 + 2.0 * turn + k * 1.8, hy - 11.0, hx - 4.0 + 2.0 * turn + k * 1.8, hy - 8.0, (240, 236, 222))
    sp.line((hx - 5.5 + 2 * turn, hy - 9.6), (hx + 5.5 + 2 * turn, hy - 9.6), INK)
    sp.anchors['head'] = (hx, hy)
    sp.outline(INK, 1)


def pumpkin_inflatable(sp, t=0.0, squash=0.0):
    k = 1.0 + 0.03 * math.sin(t * 3.0)
    bodyp = [sp.m_ell(dx, 16.0 * k, 9.0, 15.0 * k * (1 - squash)) for dx in (-10.0, 0.0, 10.0)]
    sp.union(bodyp, tones((255, 120, 30), glow=(255, 220, 120)))
    for dx in (-5.0, 5.0): stroke(sp, [(dx, 3.0), (dx * 1.2, 16.0), (dx, 29.0 * k)], (200, 80, 20))
    sp.cap((0.0, 30.0 * k), (2.0, 35.0 * k), 1.6, 1.6, tones((60, 120, 40)))
    for pts in (((-9, 19), (-5, 23), (-3, 19)), ((3, 19), (7, 23), (9, 19))):
        sp.fill(sp.m_poly([(x, y * k) for x, y in pts]), (255, 236, 120), keep=True)
    sp.fill(sp.m_poly([(-9, 12 * k), (9, 12 * k), (6, 7 * k), (2, 9 * k), (-2, 7 * k), (-6, 9 * k)]), (255, 236, 120), keep=True)
    sp.outline(INK, 1)


def countdown_sign(sp, days=5, flip=0.0, t=0.0):
    """Todd's lawn sign «HALLOWEEN IN: N DAYS» (the season counter)"""
    sp.line((-14.0, 0.0), (-14.0, 20.0), (120, 90, 60), 1); sp.line((14.0, 0.0), (14.0, 20.0), (120, 90, 60), 1)
    sp.rect(-22.0, 18.0, 22.0, 46.0, (30, 20, 40))
    sp.rect(-21.0, 19.0, 21.0, 45.0, (250, 120, 30))
    txt(sp, 'HALLOWEEN', -19.0, 43.0, (30, 20, 40))
    txt(sp, 'IN:', -5.0, 36.5, (30, 20, 40))
    sp.rect(-19.0, 21.0, -5.0, 31.0, (250, 246, 230))
    sp.ptext(str(days), -12.0, 30.0, (180, 20, 30), size=8, center=True)
    txt(sp, 'DAYS' if days != 1 else 'DAY', -2.0, 28.0, (30, 20, 40))
    sp.outline(INK, 1)


def tarp(sp, t=0.0, lift=0.0):
    """a grey tarp over the trike (the clue): bumps of a handlebar and a flag pole; lift 0..1 = yanked away up and back"""
    if lift >= 1.0: return
    dy = lift * 30.0; dx = -lift * 40.0
    pts = [(-26 + dx, 0 + dy), (-24 + dx, 18 + dy), (-14 + dx, 26 + dy), (8 + dx, 24 + dy), (14 + dx, 40 + dy), (18 + dx, 38 + dy),
           (22 + dx, 22 + dy), (28 + dx, 2 + dy)]
    sp.poly(pts, tones((120, 124, 140)), val=vgrad(40 + dy, dy, 0.1))
    for x in (-16.0, -4.0, 8.0): stroke(sp, [(x + dx, 2 + dy), (x + 3 + dx, 22 + dy)], (80, 84, 100))
    sp.rect(-15.0 + dx, 7.0 + dy, 18.0 + dx, 14.0 + dy, (250, 230, 60))                       # the sticker peeks out
    txt(sp, 'UNLOCKED', -14.0 + dx, 12.0 + dy, (200, 20, 30))
    sp.outline(INK, 1)


# ======================================================================================== trick-or-treaters, MOM, small props
KSKIN = [(236, 190, 156), (190, 130, 96), (150, 98, 70), (246, 206, 176)]


def kid_face(sp, hx, hy, E, look, blink, skin, mouth_=0.0, hs=1.0):
    DX.eye(sp, hx + 2.0 * hs, hy + 0.6 * hs, 2.6 * hs, 2.6 * hs, E, (90, 70, 50), look, blink, lash=INK, skin=skin)
    DX.eye(sp, hx - 1.6 * hs, hy + 0.6 * hs, 2.4 * hs, 2.5 * hs, E, (90, 70, 50), look, blink, lash=INK, skin=skin)
    DX.mouth(sp, hx + 0.8 * hs, hy - 2.4 * hs, 2.6 * hs, E, mouth_, (170, 70, 70), skin=skin, maxh=3)
    DX.blush(sp, hx + 3.2 * hs, hy - 1.0 * hs, 1.0, 0.8, (240, 120, 120))


def trick_or_treater(sp, t=0.0, costume='ghost', expr='normal', look=(0.6, 0.0), blink=None, n=0, pail=True, groan=0.0, mouth_=0.0):
    """a kid in a Halloween costume, ~36 sprite px tall: ghost sheet / pumpkin suit / dino onesie / witch / robot box / vampire;
    groan 0..1: shoulders drop, mouth open (the line's collective «aww»)"""
    E = X(expr if groan < 0.5 else 'sad')
    if blink is None: blink = ((t + n * 0.7) % 3.4) < 0.1
    skin = KSKIN[n % 4]
    sag = 1.5 * groan
    for dx in (-2.0, 2.0):                                                        # sneakers
        sp.sup(dx + 0.8, 1.2, 2.4, 1.4, tones((240, 240, 240) if n % 2 else (60, 60, 200)), n=2.2)
    hx, hy = 1.0, 28.0 - sag
    if costume == 'ghost':
        sh = sp.m_poly([(-7.5, 3.0), (-6.0, 22.0), (-4.0, 31.0 - sag), (1.0, 35.0 - sag), (6.0, 31.0 - sag), (8.0, 22.0), (9.0, 3.0), (6.0, 5.0),
                        (3.0, 2.5), (0.0, 5.0), (-3.0, 2.5)])
        sp.paint(sh, tones((236, 236, 240), glow=(255, 200, 150)), vgrad(35, 2, 0.1, 0.25, 0.9))
        for ex in (hx + 2.4, hx - 1.4):
            sp.ell(ex, hy + 1.0, 1.3, 1.8 + groan, tones((20, 14, 30)), ol=False)
        if groan > 0.3: sp.ell(hx + 0.8, hy - 4.0, 1.4, 1.8, tones((20, 14, 30)), ol=False)
    else:
        bodyc = {'pumpkin': (255, 130, 30), 'dino': (90, 190, 90), 'witch': (60, 30, 90), 'robot': (170, 176, 190), 'vampire': (30, 26, 40)}[costume]
        if costume == 'pumpkin':
            sp.union([sp.m_ell(dx, 11.0, 4.6, 8.5) for dx in (-4.0, 0.5, 5.0)], tones(bodyc, glow=(255, 220, 120)))
            for dx in (-2.0, 3.0): stroke(sp, [(dx, 4.0), (dx * 1.2, 11.0), (dx, 18.0)], (200, 80, 20))
        elif costume == 'robot':
            sp.rect(-6.0, 4.0, 7.0, 20.0, (150, 156, 170)); sp.rect(-6.0, 4.0, 7.0, 5.0, INK)
            sp.rect(-3.0, 11.0, 4.0, 16.0, (60, 64, 80))
            for k, c in enumerate(((255, 80, 80), (80, 255, 120), (80, 160, 255))): sp.dot(-2.0 + k * 2.5, 13.0, c, keep=True)
        else:
            sp.union([sp.m_ell(1.0, 12.0, 6.0, 9.0)], tones(bodyc, glow=(200, 140, 220)))
            if costume == 'vampire':
                sp.poly([(-7.0, 21.0), (-9.0, 3.0), (10.0, 3.0), (8.0, 21.0)], tones((140, 20, 30)), val=vgrad(21, 3, 0.0, 0.2, 0.7))
                sp.union([sp.m_ell(1.0, 12.0, 5.0, 8.5)], tones((30, 26, 40)))
                sp.poly([(-1.0, 20.0), (3.0, 20.0), (1.0, 15.0)], tones((240, 240, 240)))
            if costume == 'dino':
                for k in range(4): sp.poly([(-5.0 - k * 0.3, 8.0 + k * 4), (-8.0 - k * 0.3, 10.0 + k * 4), (-5.0, 12.0 + k * 4)], tones((240, 200, 60)))
        sp.ell(hx, hy - 1.0, 5.0, 5.4, tones(skin))
        kid_face(sp, hx + 0.5, hy - 0.5, E, look, blink, skin, mouth_=max(mouth_, 0.6 * groan))
        if costume == 'pumpkin':
            sp.cap((hx, hy + 4.5), (hx + 1.0, hy + 7.0), 1.0, 1.0, tones((60, 120, 40)))
        elif costume == 'dino':
            hood = sp.m_ell(hx - 0.5, hy + 0.5, 6.4, 6.8)[0] & ~sp.m_ell(hx + 1.0, hy - 1.0, 4.4, 4.6)[0] & (DX.YC > hy - 4.0)
            sp.paint(hood, tones(bodyc), vgrad(hy + 7, hy - 4))
            sp.ell(hx + 1.0, hy + 5.5, 4.0, 1.6, tones((90, 190, 90)))
            for k in range(3): sp.poly([(hx - 3.0 + k * 2.5, hy + 6.0), (hx - 2.0 + k * 2.5, hy + 9.0), (hx - 1.0 + k * 2.5, hy + 6.0)], tones((240, 200, 60)))
        elif costume == 'witch':
            sp.ell(hx, hy + 4.0, 8.0, 1.2, tones((40, 20, 60)))
            sp.poly([(hx - 4.0, hy + 4.5), (hx + 4.0, hy + 4.5), (hx - 2.0, hy + 14.0)], tones((40, 20, 60)))
            sp.rect(hx - 4.0, hy + 4.5, hx + 4.0, hy + 5.6, (150, 255, 110))
        elif costume == 'robot':
            sp.rect(hx - 5.0, hy - 5.0, hx + 6.0, hy + 5.0, (170, 176, 190)); sp.rect(hx - 3.0, hy - 2.5, hx + 4.0, hy + 2.5, (30, 40, 60))
            sp.dot(hx - 1.0, hy, (120, 255, 200), keep=True); sp.dot(hx + 2.0, hy, (120, 255, 200), keep=True)
            sp.line((hx, hy + 5.0), (hx, hy + 8.0), (120, 120, 130)); sp.dot(hx, hy + 8.0, (255, 80, 80), keep=True)
        elif costume == 'vampire':
            sp.ell(hx - 0.5, hy + 3.5, 5.0, 2.4, tones((24, 20, 30)))
            sp.dot(hx + 1.0, hy - 3.6, (250, 250, 250), keep=True); sp.dot(hx + 2.0, hy - 3.6, (250, 250, 250), keep=True)
    if pail:                                                                      # the jack-o'-lantern candy pail
        px, py = 7.5, 9.0 - sag
        sp.ell(px, py, 3.4, 3.0, tones((255, 120, 30)))
        sp.dot(px - 1.0, py + 0.5, INK); sp.dot(px + 1.0, py + 0.5, INK); sp.line((px - 1.5, py - 1.0), (px + 1.5, py - 1.0), INK)
        sp.line((px - 3.0, py + 2.5), (px, py + 6.0), (40, 40, 40)); sp.line((px + 3.0, py + 2.5), (px, py + 6.0), (40, 40, 40))
    sp.anchors['head'] = (hx, hy)
    sp.outline(INK, 1)


MSKIN = (240, 196, 168)
VEST = (40, 170, 170)


def mom(sp, t=0.0, expr='squint', mouth_=0.0, look=(-0.8, 0.0), blink=None, point=0.0):
    """MOM: tall «exclamation mark» — puffer vest, leggings, white sneakers, high blonde ponytail, giant iced-coffee tumbler"""
    E = X(expr)
    if blink is None: blink = (t % 3.2) < 0.1
    for dx in (-2.5, 2.5):
        sp.cap((dx * 0.6, 34.0), (dx, 5.0), 2.6, 2.0, tones((40, 36, 50)))
        sp.sup(dx + 1.4, 2.0, 3.6, 1.8, tones((250, 250, 250)), n=2.2)
    sp.union([sp.m_ell(0.0, 38.0, 7.0, 6.0)], tones((40, 36, 50)))
    sp.union([sp.m_ell(0.5, 48.0, 7.6, 9.0)], tones((236, 230, 236)))                           # long-sleeve top
    vest = sp.union([sp.m_ell(0.5, 48.0, 8.4, 9.4)], tones(VEST))
    sp.fill(vest & (np.abs(DX.XC - 1.5) < 2.0), (236, 230, 236))
    for y in (44.0, 48.0, 52.0): sp.line((-7.0, y), (8.0, y), dark(VEST, 0.6))                  # puffer quilting
    sp.cap((-5.0, 54.0), (-6.0, 40.0), 2.0, 1.8, tones((236, 230, 236)))                         # far arm + the tumbler
    sp.rect(-8.5, 37.0, -3.5, 46.0, (250, 240, 230)); sp.rect(-8.5, 44.0, -3.5, 45.0, (60, 140, 90))
    sp.line((-5.0, 46.0), (-4.0, 50.0), (60, 140, 90), 1)
    hx, hy = 2.0, 63.0
    sp.cap((1.0, 56.0), (1.5, 58.0), 2.4, 2.4, tones(MSKIN))
    sp.union([sp.m_ell(hx, hy, 5.6, 6.6), sp.m_ell(hx + 1.0, hy - 4.0, 4.0, 3.0)], tones(MSKIN))
    DX.eye(sp, hx + 2.4, hy + 1.0, 3.2, 2.8, E, (60, 110, 160), look, blink, lash=INK, skin=MSKIN, flick=True)
    DX.eye(sp, hx - 1.8, hy + 1.0, 2.8, 2.7, E, (60, 110, 160), look, blink, lash=INK, skin=MSKIN, flick=True)
    DX.brow(sp, hx + 2.4, hy + 3.6, 3.6, E, +1, (150, 110, 60), th=1, arch=1.2)
    DX.brow(sp, hx - 1.8, hy + 3.6, 3.2, E, -1, (150, 110, 60), th=1, arch=1.2)
    sp.ell(hx + 4.2, hy - 1.0, 1.4, 1.4, tones(MSKIN))
    DX.mouth(sp, hx + 2.2, hy - 3.6, 3.6, E, mouth_, (200, 80, 90), skin=MSKIN, maxh=4)
    hair = sp.union([sp.m_ell(hx - 0.5, hy + 4.0, 6.4, 4.0), sp.m_ell(hx - 3.0, hy + 2.0, 3.0, 5.0)], tones((236, 200, 110)))
    sw = 1.5 * math.sin(t * 6.0)
    sp.union([sp.m_ell(hx - 2.0, hy + 9.0, 2.0, 2.0), sp.m_ell(hx - 4.0 + sw * 0.3, hy + 4.0, 2.2, 5.0, 0.3 + sw * 0.05)], tones((236, 200, 110)))
    sp.rect(hx - 3.0, hy + 7.0, hx - 1.0, hy + 8.0, (255, 120, 180))                            # scrunchie
    sp.anchors['head'] = (hx, hy)
    shN = (5.0, 54.0)
    hN = (shN[0] + 14.0 * point + 4.0, shN[1] - 8.0 + 10.0 * point)
    kN, eN = ik(shN, hN, 7.0, 7.0, -1.0)
    sp.cap(shN, kN, 2.2, 2.0, tones((236, 230, 236))); sp.cap(kN, eN, 2.0, 1.8, tones((236, 230, 236)))
    sp.ell(*eN, 1.8, 1.6, tones(MSKIN))
    if point > 0.3: sp.line((eN[0] + 1.0, eN[1]), (eN[0] + 4.0, eN[1] + 0.6), MSKIN, 1)
    sp.outline(INK, 1)


def sack(sp, x, y, fill=0.2):
    """Death's trick-or-treat pillowcase hanging from a bony hand at (x, y)"""
    m = sp.m_poly([(x - 2.0, y), (x + 2.0, y), (x + 5.0, y - 8.0), (x + 4.0, y - 16.0 - 4 * fill), (x - 4.0, y - 16.0 - 4 * fill), (x - 5.0, y - 8.0)])
    sp.paint(m, tones((236, 232, 222)), vgrad(y, y - 20, 0.1))
    stroke(sp, [(x - 1.0, y - 2.0), (x - 2.0, y - 12.0)], (190, 186, 176))
    sp.anchors['sack'] = (x, y - 10.0)
