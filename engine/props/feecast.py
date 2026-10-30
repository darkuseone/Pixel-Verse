"""«Land of the Fee» cast + props, drawn in the «Intaglio Pop» manner (props/feepix.py).
Coordinates: sprite px, feet anchor at (0, 0), x right = facing side, y UP.
  duke(sp, ...)   — Duke, bald eagle, ~45: «a barrel with a hook» (a chest wider than a doorway in an 80s red-white-navy track jacket,
                    tiny yellow talons, a white fist of a head with a giant hooked yellow beak, permanently furrowed brows, ONE combed-over
                    feather across the top, aviators on the forehead, a gold chain with a coin medallion); wings are the arms
  sal(sp, ...)    — Sal, Brooklyn street pigeon: «a pear on matchsticks» (fat grey body, tiny head on an oil-slick green-violet neck,
                    orange eyes, pink feet), a french fry in the beak, the head bobs on its own rhythm
  doris(sp, ...)  — Doris, the last human support rep: a mini Minnesota grandma (auburn bouffant, half-moon glasses, a headset, a peach
                    cardigan, a lanyard «REAL HUMAN» and a taxi meter on her belly that counts dollars)
Props: kiosk (XFEENITY self-service stand with the Fee-Bee face), phone, wallet, hummus cup, speaker, fries box, door (EMPLOYEES ONLY)."""
import math
import numpy as np
from props import dibspix as DX
from props.dibspix import dark, mix, erode, dilate, ik, EXPR
from props.feepix import tones, thin, stroke, INK, WHITE, PAPER

# ---------------------------------------------------------------- palette
EAGLE_B = (98, 62, 38)               # dark brown body feathers
EAGLE_W = (246, 244, 236)            # white head / tail
EAGLE_G = (176, 172, 168)            # grey feather shading on the white head
BEAK = (250, 196, 46)                # big yellow beak + talons
BEAK_D = (206, 140, 30)
IRIS_E = (236, 204, 70)              # pale yellow eagle eye
JACK = (40, 54, 116)                 # navy track jacket
GOWN = (176, 210, 232)               # hospital gown pale blue
JRED = (204, 42, 50)
JWHT = (246, 244, 236)
GOLD = (238, 198, 72)
LENS = (40, 70, 80)

PIG = (150, 156, 172)                # pigeon grey-blue
PIG_D = (96, 100, 118)
PIG_NG = (74, 170, 120)              # iridescent neck green
PIG_NV = (150, 92, 170)              # iridescent neck violet
PIG_EYE = (240, 130, 40)
PIG_FOOT = (226, 120, 130)
FRY = (246, 200, 80)

SKIN_D = (244, 204, 180)             # Doris
HAIR_D = (178, 84, 54)               # auburn bouffant
CARD_D = (246, 170, 140)             # peach cardigan
BLOUSE = (250, 240, 220)
SLACK = (64, 70, 110)
LANY = (214, 40, 60)
METER = (40, 40, 46)
LED = (255, 70, 60)

MINT = (110, 240, 196)               # Fee-Bee glow
MINT_D = (40, 150, 120)
KIO = (240, 240, 246)
KIO_D = (120, 116, 150)
PURP = (126, 72, 190)

XTRA = dict(
    proud=dict(eo=0.85, pu=0.55, bt=0.45, bl=0.2, mo=0.0, mc=0.6),
    roar=dict(eo=1.25, pu=0.40, bt=0.75, bl=0.0, mo=1.0, mc=0.0),
    plead=dict(eo=1.15, pu=0.55, bt=-0.6, bl=0.6, mo=0.3, mc=-0.5),
    losing=dict(eo=1.35, pu=0.3, bt=-0.5, bl=0.8, mo=0.85, mc=-0.3),
    dead=dict(eo=0.72, pu=0.55, bt=0.0, bl=0.0, mo=0.0, mc=0.0, lid=0.58),
    sweet=dict(eo=0.0, pu=0.6, bt=-0.3, bl=0.4, mo=0.0, mc=0.9, shut=True),
    warm=dict(eo=0.95, pu=0.62, bt=-0.25, bl=0.35, mo=0.0, mc=0.85),
    joy=dict(eo=1.25, pu=0.65, bt=-0.4, bl=0.7, mo=0.7, mc=0.9),
    puff=dict(eo=0.6, pu=0.5, bt=0.6, bl=-0.2, mo=0.0, mc=-0.3, lid=0.3),
)


def X(expr):
    return dict(XTRA.get(expr) or EXPR.get(expr, EXPR['normal']))


def _rot(pts, o, deg):
    a = math.radians(deg); ca, sa = math.cos(a), math.sin(a)
    return [(o[0] + (x - o[0]) * ca - (y - o[1]) * sa, o[1] + (x - o[0]) * sa + (y - o[1]) * ca) for x, y in pts]


# ================================================================================ Fee-Bee face (on any screen, sprite res)
def feebee_face(sp, cx, cy, r, t=0.0, talk=0.0, expr='smile', glow=True, eq=True):
    """Fee-Bee: a mint glowing disc with two bean eyes and a wide smile (opens with talk), an equalizer under it when she speaks"""
    m = sp.m_ell(cx, cy, r, r)[0]
    sp.fill(m, MINT, keep=True)
    sp.fill(m & (DX.YC > cy + r * 0.45), mix(MINT, (255, 255, 255), 0.45), keep=True)
    sp.fill(m & ~erode(m), MINT_D, keep=True)
    blink = ((t + 0.7) % 3.1) < 0.12
    for ex in (cx - r * 0.36, cx + r * 0.36):
        if blink: thin(sp, (ex - r * 0.12, cy + r * 0.22), (ex + r * 0.12, cy + r * 0.22), (20, 60, 50), max(0.25, r * 0.05), keep=True)
        else:
            sp.blob(ex, cy + r * 0.22, max(0.5, r * 0.13), (20, 60, 50), keep=True)
            sp.blob(ex - r * 0.04, cy + r * 0.28, max(0.3, r * 0.05), (255, 255, 255), keep=True)
    op = min(1.0, talk * 1.4)
    if op < 0.08:                                                                   # idle: a wide customer-service smile
        for q in range(9):
            u = (q - 4) / 4.0
            sp.blob(cx + u * r * 0.48, cy - r * 0.30 + r * 0.16 * u * u, max(0.35, r * 0.06), (20, 60, 50), keep=True)
    else:
        mw, mh = r * 0.5, r * (0.12 + 0.32 * op)
        mm = sp.m_ell(cx, cy - r * 0.26, mw, mh)[0] & (DX.YC < cy - r * 0.16)
        sp.fill(mm, (20, 60, 50), keep=True)
        if op > 0.25: sp.fill(mm & (DX.YC < cy - r * 0.26 - mh * 0.4), (255, 120, 150), keep=True)
    for ex in (cx - r * 0.62, cx + r * 0.62):
        sp.fill(sp.m_ell(ex, cy - r * 0.08, r * 0.14, r * 0.08)[0] & m, (255, 160, 190), keep=True)
    if eq and talk > 0.02:
        for i in range(7):
            h = r * 0.12 + r * 0.55 * talk * abs(math.sin(t * 17 + i * 1.7))
            x = cx - r * 0.75 + i * r * 0.25
            sp.fill(sp.m_super(x, cy - r - 0.6 - h / 2, r * 0.07, h / 2, 4.0)[0], MINT, keep=True)


# ================================================================================ hand props
def phone(sp, h, t=0.0, talk=0.0, screen='feebee'):
    """a smartphone held upright: dark case, the screen shows Fee-Bee (or plain glow)"""
    x, y = h
    m = sp.m_super(x + 0.6, y + 3.6, 2.4, 4.4, 4.0)[0]
    sp.paint(m, tones((36, 36, 44)), None, olc=INK)
    sc = sp.m_super(x + 0.6, y + 3.6, 1.9, 3.8, 4.0)[0]
    sp.fill(sc, (24, 40, 60), keep=True)
    if screen == 'feebee': feebee_face(sp, x + 0.6, y + 4.0, 1.6, t, talk, eq=False)
    sp.anchors['phone'] = (x + 0.6, y + 3.6)


def wallet(sp, h, open_=0.0):
    x, y = h
    if open_ > 0:
        sp.sup(x - 1.6, y + 0.6, 2.4, 1.8, tones((110, 70, 44)), n=3.0)
        sp.sup(x + 2.0, y + 0.8, 2.4, 1.8, tones((126, 82, 52)), n=3.0)
        sp.fill(sp.m_super(x + 0.2, y + 0.7, 0.4, 1.4, 3.0)[0], (60, 40, 26))
    else:
        sp.sup(x + 0.6, y + 0.4, 2.6, 1.7, tones((110, 70, 44)), n=3.0)


def fry(sp, a, b):
    thin(sp, a, b, FRY, 0.5)
    thin(sp, (a[0], a[1] + 0.25), (b[0], b[1] + 0.25), mix(FRY, (255, 255, 220), 0.5), 0.18)


def hummus(sp, t=0.0, lid=True):
    """a small plastic cup of hummus with a peeled foil lid (dropped by the kiosk)"""
    cup = sp.poly([(-3.4, 5.6), (3.4, 5.6), (2.6, 0.0), (-2.6, 0.0)], tones((246, 240, 214)), grad=(5.6, 0.0))
    sp.fill(cup & (DX.YC > 2.0) & (DX.YC < 3.6), (220, 160, 60))
    sp.txt_box(['HUMMUS'], (-2.8, 2.0, 2.8, 3.6), (120, 60, 20), pad=0.1)
    sp.ell(0.0, 5.8, 3.4, 0.9, tones((214, 190, 130)))
    if lid: sp.poly([(0.0, 6.0), (3.6, 6.6), (4.6, 9.0), (1.0, 7.6)], tones((210, 214, 224)), grad=(9.0, 6.0))


def speaker(sp, h=(0.0, 0.0), t=0.0, on=False):
    """a cheap Bluetooth speaker (Sal's «SCREAM» button)"""
    x, y = h
    sp.sup(x, y + 2.0, 3.8, 2.2, tones((44, 44, 54)), n=3.0)
    for q in range(-2, 3): sp.dot(x + q * 1.2, y + 2.0, (90, 90, 104))
    sp.dot(x + 3.0, y + 3.4, (90, 230, 120) if on and int(t * 6) % 2 == 0 else (60, 70, 70))


def fries_box(sp, t=0.0):
    """a red fries carton «FREE FRIES (FOR PIGEONS)» on the window ledge"""
    sp.poly([(-3.0, 5.6), (3.0, 5.6), (2.2, 0.0), (-2.2, 0.0)], tones((214, 40, 46)), grad=(5.6, 0.0))
    for q in range(5):
        fry(sp, (-2.2 + q * 1.1, 5.0), (-2.6 + q * 1.3, 7.8 + (q % 2) * 0.8))
    sp.txt_box(['FREE'], (-2.2, 1.2, 2.2, 4.2), (255, 230, 120), pad=0.1)


# ================================================================================ DUKE — the bald eagle
def _wing_hand(sp, e, d, open_=0.6, col=EAGLE_B):
    """feather «fingers» (primaries) fanning from the wrist e along direction d (radians)"""
    for i in range(4):
        a = d + (i - 1.5) * (0.22 + 0.25 * open_)
        L = 5.6 - abs(i - 1.5) * 0.6
        ex, ey = e[0] + math.cos(a) * L, e[1] + math.sin(a) * L
        sp.cap(e, (ex, ey), 1.5, 0.75, tones(col if i < 3 else dark(col, 0.85)))
    sp.ell(e[0], e[1], 2.2, 2.0, tones(col))


def duke(sp, t=0.0, expr='normal', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
         walk=None, lean=0.0, puff=0.0, flop=0.0, shades='head', tremble=0.0, fly=None, legs=True, jacket=True, sweat=0.0,
         gown=False, brace=False):
    """DUKE — barrel chest in a navy 80s track jacket (red chest stripe, white piping, popped collar, zip half open over brown chest
    feathers), a gold chain with a coin medallion, short feathered «trousers» and tiny yellow talons, a white tail peeking under the
    jacket; a white fist of a head with heavy furrowed brows (always glaring), pale yellow eyes, a giant hooked yellow beak (the mouth),
    one long combed-over feather (flop 0..1: it lifts and flaps when he roars), aviators on the forehead (shades='head'|'eyes'|None).
    puff 0..1 swells the chest (pride); fly = phase -> wings spread and beat, legs tucked"""
    E = X(expr)
    E['bt'] = max(E['bt'], 0.42)                                   # an eagle can only look disappointed
    if blink is None: blink = ((t + 0.9) % 4.1) < 0.12
    br = 0.35 * math.sin(t * 2.0)
    bob = abs(math.sin(walk)) * 1.0 if walk is not None else 0.0
    jit = math.sin(t * 60.0) * 0.4 * tremble
    def Q(x, y): return (x + lean * (y / 70.0) * 6.0 + (jit if y > 52 else 0), y + (bob if y > 12 else bob * 0.3))
    swing = math.sin(walk) * 4.0 if walk is not None else 0.0
    pk = 1.0 + 0.10 * puff
    flying = fly is not None
    beat = math.sin(fly * 2 * math.pi) if flying else 0.0
    # ---------------------------------------------------------------- far wing (behind)
    shF = Q(-12.0, 44.0 + br * 0.3)
    if flying:
        a = math.radians(150 - 40 * beat)
        kF = (shF[0] + math.cos(a) * 10, shF[1] + math.sin(a) * 10); eF = (kF[0] + math.cos(a + 0.2) * 9, kF[1] + math.sin(a + 0.2) * 9)
    else:
        hf = hand_f if hand_f is not None else Q(-17.0 - swing * 0.6, 26.0)
        kF, eF = ik(shF, hf, 9.0, 8.0, -1.0)
    if gown: jacket = False
    sl = tones(dark(JACK, 0.8)) if jacket else (tones(dark(GOWN, 0.85)) if gown else tones(dark(EAGLE_B, 0.85)))
    sp.cap(shF, kF, 4.0, 3.2, sl)
    sp.cap(kF, eF, 3.2, 2.4, sl)
    _wing_hand(sp, eF, math.atan2(eF[1] - kF[1], eF[0] - kF[0]), 0.9 if flying else 0.5, dark(EAGLE_B, 0.85))
    if prop_f: prop_f(sp, eF)
    sp.anchors['hand_f'] = eF
    # ---------------------------------------------------------------- tail + legs
    sp.union([sp.m_ell(*Q(-13.0, 15.0), 5.0, 2.2, 0.5), sp.m_ell(*Q(-15.0, 13.4), 4.0, 1.8, 0.7)], tones(EAGLE_W))
    if legs and not flying:
        sw = math.sin(walk) * 2.4 if walk is not None else 0.0
        for k_, dx in enumerate((-5.0, 5.0)):
            s_ = sw if k_ else -sw
            near = k_ == 1
            c = EAGLE_B if near else dark(EAGLE_B, 0.85)
            fx_, fy_ = dx + s_ * 0.7, 1.6 + max(0.0, s_) * 0.4
            sp.cap(Q(dx * 0.8, 15.0), (fx_, fy_ + 3.6), 3.0, 2.4, tones(c))                       # feathered «trousers»
            for q in range(3): thin(sp, (dx * 0.8 - 1.8 + q * 1.4, 10.0), (dx * 0.8 - 1.2 + q * 1.4, 7.0), dark(c, 0.7), 0.2)
            sp.cap((fx_, fy_ + 2.6), (fx_, fy_ + 0.6), 1.2, 1.2, tones(BEAK))
            for q, (tx, ty) in enumerate(((2.8, -0.6), (1.6, -0.9), (-1.6, -0.6))):                  # three talons + claws
                sp.cap((fx_, fy_ + 0.4), (fx_ + tx, fy_ + ty), 0.8, 0.6, tones(BEAK if near else dark(BEAK, 0.9)), ol=False)
                sp.dot(fx_ + tx + (0.6 if tx > 0 else -0.6), fy_ + ty - 0.2, (40, 34, 30))
    elif flying:
        for dx in (-3.0, 2.0):
            sp.ell(*Q(dx - 4.0, 12.0), 2.6, 1.6, tones(EAGLE_B))
            sp.ell(*Q(dx - 6.6, 11.4), 1.2, 0.8, tones(BEAK), ol=False)
    # ---------------------------------------------------------------- barrel body: jacket over chest feathers
    bx, by = Q(1.4, 32.0)
    if jacket:
        body = sp.union([sp.m_ell(bx, by, 16.4 * pk, 18.6), sp.m_ell(*Q(1.0, 46.0), 13.0 * pk, 7.4)], tones(JACK))
        vee = sp.m_poly([Q(1.8, 52.0), Q(11.6, 52.0), Q(8.6, 34.0)]) & body                            # open zip: chest feathers
        sp.paint(vee, tones(EAGLE_B), DX.lit(np.clip((DX.XC - 6.0) / 8.0, -0.9, 0.9), np.full_like(DX.XC, 0.3)))
        for q in range(4): thin(sp, Q(4.0 + q * 1.6, 47.0 - q * 2.2), Q(6.0 + q * 1.6, 46.0 - q * 2.2), dark(EAGLE_B, 0.7), 0.25, mask=vee)
        thin(sp, Q(8.6, 34.0), Q(9.4, 15.0), (220, 220, 226), 0.35, mask=body)                          # zipper
        band = body & (DX.YC < Q(0, 40.0)[1] + (DX.XC - bx) * 0.25) & (DX.YC > Q(0, 35.0)[1] + (DX.XC - bx) * 0.25)
        sp.paint(band & ~vee, tones(JRED), DX.lit(np.clip((DX.XC - bx) / 16.0, -0.9, 0.9), np.full_like(DX.XC, 0.25)))
        for off in (34.2, 40.8):
            thin(sp, Q(bx - 16.0, off - 4.0), Q(bx + 16.0, off + 4.0), JWHT, 0.35, mask=body & ~vee)
        sp.fill(body & (DX.YC < Q(0, 15.6)[1]), dark(JACK, 0.7))                                          # ribbed hem
        for q in range(-14, 16, 2): thin(sp, Q(bx + q, 13.2), Q(bx + q, 15.4), dark(JACK, 0.55), 0.15, mask=body)
        col_ = sp.union([sp.m_ell(*Q(-1.0, 52.0), 5.0, 3.0, 0.4), sp.m_ell(*Q(13.0, 51.6), 3.6, 2.6, -0.5)], tones(JRED))   # popped collar
        # gold chain + coin medallion
        for q in range(9):
            a = math.pi * (1.08 + 0.84 * q / 8)
            sp.blob(*Q(6.6 + math.cos(a) * 5.6, 50.4 + math.sin(a) * 7.6), 0.5, GOLD)
        mx_, my_ = Q(6.6, 41.2)
        sp.ell(mx_, my_, 2.6, 2.6, tones(GOLD), gloss=1.0)
        sp.ell(mx_, my_, 1.7, 1.7, tones(dark(GOLD, 0.82)), ol=False)
        sp.dot(mx_ - 0.4, my_ + 0.2, (250, 240, 200)); sp.dot(mx_ + 0.6, my_ - 0.4, (180, 130, 40))
        sp.anchors['medal'] = (mx_, my_)
    else:
        body = sp.union([sp.m_ell(bx, by, 16.0 * pk, 18.4), sp.m_ell(*Q(1.0, 46.0), 13.0 * pk, 7.4)], tones(GOWN if gown else EAGLE_B))
        if gown:                                                                                          # hospital gown: tiny diamond print, ties
            for q in range(-14, 16, 4):
                for r_ in range(16, 52, 4):
                    sp.blob(bx + q + (r_ % 8) * 0.5, r_, 0.45, dark(GOWN, 0.72), mask=body)
            thin(sp, Q(-2.0, 50.0), Q(-4.0, 44.0), (250, 250, 250), 0.3, mask=body)
        for q in range(0 if gown else 14):
            x_ = bx - 12 + (q % 7) * 4 + (q // 7) * 2; y_ = by + 8 - (q // 7) * 10
            thin(sp, (x_, y_), (x_ + 1.6, y_ - 1.6), dark(EAGLE_B, 0.7), 0.3, mask=body)
    # ---------------------------------------------------------------- neck ruff + head
    hx, hy = Q(4.6, 62.0)
    hx += jit
    ruff = sp.union([sp.m_ell(hx - 0.4, hy - 8.6, 8.6, 3.6)] + [sp.m_ell(hx - 7.0 + q * 2.4, hy - 10.6 - (q % 2) * 0.8, 1.6, 2.0) for q in range(7)],
                    tones(EAGLE_W))
    if brace:                                                                                            # beige foam neck brace
        br_ = sp.sup(hx - 0.2, hy - 8.4, 9.6, 3.2, tones((236, 214, 180)), n=3.0)
        thin(sp, (hx - 9.0, hy - 8.4), (hx + 8.6, hy - 8.4), (200, 176, 140), 0.25, mask=br_)
        sp.fill(sp.m_super(hx + 3.0, hy - 8.4, 1.6, 1.4, 3.0)[0], (210, 210, 220))
    head = sp.union([sp.m_ell(hx, hy, 9.6, 8.8), sp.m_ell(hx - 3.6, hy + 1.4, 6.6, 7.2), sp.m_ell(hx + 3.4, hy - 3.8, 6.4, 4.6)], tones(EAGLE_W))
    for q in range(5):                                                                                  # feather flicks on the head
        thin(sp, (hx - 8.0 + q * 1.4, hy + 4.0 - q * 1.8), (hx - 6.4 + q * 1.4, hy + 3.0 - q * 1.8), EAGLE_G, 0.22, mask=head)
    for q in range(3):
        sp.cap((hx - 9.0, hy - 2.0 - q * 2.2), (hx - 11.4, hy - 3.6 - q * 2.2), 0.9, 0.4, tones(EAGLE_W))   # ragged nape
    sp.fill(head & (DX.YC > hy + 5.5) & (DX.XC > hx - 2.0), mix(EAGLE_W, PAPER, 0.6))
    # eyes: near big, far small, both pale yellow under the brow ridge
    lx, ly = look
    DX.eye(sp, hx + 5.4, hy + 1.6, 4.6, 4.0, E, IRIS_E, (lx, ly), blink, lash=INK, skin=EAGLE_W, bold=1, lidc=EAGLE_W)
    DX.eye(sp, hx - 0.6, hy + 1.8, 3.2, 3.4, E, IRIS_E, (lx, ly), blink, lash=INK, skin=EAGLE_W, bold=1, lidc=EAGLE_W)
    DX.brow(sp, hx + 5.6, hy + 5.0, 6.6, E, -1, (92, 88, 96), th=3, bushy=False, arch=0.4)               # heavy glaring brow ridge (inner
    DX.brow(sp, hx - 0.6, hy + 5.0, 4.2, E, +1, (92, 88, 96), th=2.4, arch=0.4)                          # ends point at the beak root)
    if shades == 'eyes':
        for (ex, r) in ((hx + 5.4, 2.8), (hx - 0.6, 2.2)):
            sp.ell(ex, hy + 1.6, r + 0.5, r, tones(GOLD), ol=False)
            sp.ell(ex, hy + 1.6, r, r - 0.4, tones(LENS), ol=False, gloss=1.0)
        thin(sp, (hx + 1.8, hy + 2.2), (hx + 2.8, hy + 2.2), GOLD, 0.3)
    # beak: upper hook + lower mandible that drops open (the mouth)
    op = max(mouth_, E['mo'])
    root = (hx + 7.4, hy - 3.6)
    up = [(hx + 6.6, hy + 0.2), (hx + 11.0, hy + 0.8), (hx + 15.4, hy - 0.4), (hx + 18.2, hy - 3.0), (hx + 18.6, hy - 5.8), (hx + 17.2, hy - 6.8),
          (hx + 16.6, hy - 5.0), (hx + 13.0, hy - 3.8), (hx + 7.4, hy - 4.2)]
    lo = [(hx + 7.4, hy - 4.0), (hx + 13.0, hy - 3.8), (hx + 16.0, hy - 4.6), (hx + 14.4, hy - 6.0), (hx + 10.0, hy - 6.6), (hx + 7.0, hy - 5.8)]
    BK = 1.3
    up = [(root[0] + (x - root[0]) * BK, root[1] + (y - root[1]) * BK) for x, y in up]
    lo = [(root[0] + (x - root[0]) * BK, root[1] + (y - root[1]) * BK) for x, y in lo]
    ang = -34.0 * op
    lo2 = _rot(lo, root, ang)
    if op > 0.05:
        gape = sp.m_poly([root, (root[0] + 9.0, hy - 4.0), lo2[2], lo2[3], lo2[4]])
        sp.fill(gape, (150, 34, 48))
        sp.fill(gape & (DX.YC < root[1] - 2.0 - 3.0 * op), (236, 110, 130))                               # tongue
        sp.fill(gape & ~erode(gape), (110, 24, 36))
    sp.poly(lo2, tones(BEAK_D), grad=(hy - 3.8, hy - 6.6 - 4 * op))
    upm = sp.poly(up, tones(BEAK), grad=(hy + 0.8, hy - 6.8))
    sp.fill(upm & (DX.YC > hy - 0.6) & (DX.XC < hx + 11.0), mix(BEAK, (255, 240, 170), 0.5))            # cere highlight
    sp.blob(hx + 11.0, hy - 0.8, 0.45, (90, 60, 20))                                                    # nostril
    if op <= 0.05: thin(sp, (hx + 8.0, hy - 4.0), (hx + 16.0, hy - 3.9), (150, 90, 20), 0.22)        # gape line
    if sp.k >= 2: thin(sp, (hx + 18.0, hy - 1.0), (hx + 20.6, hy - 4.6), (255, 236, 160), 0.2)          # hook shine
    sp.anchors.update(head=(hx, hy), mouth=(hx + 15.0, hy - 4.6), beak=(hx + 21.0, hy - 6.0), eyes=(hx + 2.4, hy + 1.6), belly=(bx, by),
                      back=Q(-9.0, 47.0))
    # the combed-over feather + aviators on the forehead
    fl = flop * (0.6 + 0.4 * math.sin(t * 22.0))
    base = (hx - 7.0, hy + 6.0); mid_ = (hx + 0.0, hy + 10.6 + 4.0 * fl); tip = (hx + 8.4 - 2.0 * fl, hy + 8.4 + 9.0 * fl)
    stroke(sp, [base, mid_, tip], (120, 116, 112), 1.05)
    stroke(sp, [base, mid_, tip], EAGLE_W, 0.7)
    if shades == 'head':
        for (ex, r) in ((hx + 4.4, 2.4), (hx - 1.0, 2.0)):
            sp.ell(ex, hy + 8.4, r + 0.5, r - 0.2, tones(GOLD), ol=False)
            sp.ell(ex, hy + 8.4, r, r - 0.7, tones(LENS), ol=False, gloss=1.0)
        thin(sp, (hx + 1.0, hy + 8.6), (hx + 2.0, hy + 8.6), GOLD, 0.3)
    if sweat > 0:
        for i, (x, y) in enumerate(((hx - 4.0, hy + 6.0), (hx + 8.6, hy + 5.0))[:int(1 + sweat)]):
            yy = y - ((t * 4.0 + i * 1.3) % 4.0)
            sp.ell(x, yy, 0.7, 1.1, tones((170, 220, 255)), ol=False); sp.dot(x - 0.2, yy + 0.4, WHITE)
    sp.outline(INK, 1)
    # ---------------------------------------------------------------- near wing (arm) + prop
    before = sp.m.copy()
    shN = Q(12.4, 44.0 + br * 0.3)
    if flying:
        a = math.radians(30 + 40 * beat)
        kN = (shN[0] + math.cos(a) * 10, shN[1] + math.sin(a) * 10); eN = (kN[0] + math.cos(a - 0.2) * 9, kN[1] + math.sin(a - 0.2) * 9)
    else:
        hn = hand_n if hand_n is not None else Q(17.6 + swing * 0.6, 26.0)
        kN, eN = ik(shN, hn, 9.0, 8.0, -1.0)
    sl = tones(JACK) if jacket else (tones(GOWN) if gown else tones(EAGLE_B))
    a1 = sp.cap(shN, kN, 4.2, 3.4, sl)
    a2 = sp.cap(kN, eN, 3.4, 2.6, sl)
    if jacket:
        for (p0, p1, mm) in ((shN, kN, a1), (kN, eN, a2)):                                               # sleeve stripes
            nx_, ny_ = p1[1] - p0[1], -(p1[0] - p0[0]); L = math.hypot(nx_, ny_) or 1.0
            o = (nx_ / L * 1.6, ny_ / L * 1.6)
            thin(sp, (p0[0] + o[0], p0[1] + o[1]), (p1[0] + o[0], p1[1] + o[1]), JRED, 0.6, mask=mm)
            thin(sp, (p0[0] + o[0] * 0.4, p0[1] + o[1] * 0.4), (p1[0] + o[0] * 0.4, p1[1] + o[1] * 0.4), JWHT, 0.3, mask=mm)
        sp.ell(eN[0], eN[1], 2.6, 2.4, tones(JRED))                                                        # red cuff
    if prop_n and getattr(prop_n, 'behind', False): prop_n(sp, eN)
    _wing_hand(sp, eN, math.atan2(eN[1] - kN[1], eN[0] - kN[0]), 0.9 if flying else 0.5)
    if prop_n and not getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


# ================================================================================ SAL — the pigeon
def sal(sp, t=0.0, expr='dead', mouth_=0.0, look=(0.5, 0.0), blink=None, bob=True, fry_=False, walk=None, ruffle=0.0, prop=None,
        speaker_=False, speaker_on=False):
    """SAL — a fat grey pear of a city pigeon on two pink matchsticks: dark wing bars, a charcoal tail, a tiny head on an oil-slick
    green/violet neck, orange eyes with heavy deadpan lids, a dark beak with a white cere, a french fry in the beak; the head bobs"""
    E = X(expr)
    if blink is None: blink = ((t + 0.4) % 3.7) < 0.12
    ph = (t * 1.6) % 1.0
    hb = (math.sin(ph * 2 * math.pi) * 1.1 if bob else 0.0) + (math.sin(walk * 2) * 1.6 if walk is not None else 0.0)
    # feet
    for dx in (-1.6, 1.8):
        sp.cap((dx, 4.6), (dx + 0.4, 0.8), 0.55, 0.5, tones(PIG_FOOT), ol=False)
        for tx in (1.4, -1.0, 0.4):
            thin(sp, (dx + 0.4, 0.6), (dx + 0.4 + tx, 0.2), dark(PIG_FOOT, 0.8), 0.32)
    # tail
    sp.poly([(-6.0, 9.0), (-12.6, 5.6), (-12.0, 3.8), (-5.0, 6.0)], tones((70, 72, 86)), grad=(9.0, 3.8))
    # body
    body = sp.union([sp.m_ell(0.0, 9.6, 7.8 + ruffle, 6.6 + ruffle * 0.6), sp.m_ell(2.6, 13.4, 4.6, 4.0)], tones(PIG))
    sp.fill(body & (DX.YC < 6.0), mix(PIG, (220, 224, 236), 0.35))
    wing = sp.union([sp.m_ell(-2.0, 10.6, 6.0, 4.2, -0.15)], tones(PIG_D))
    for q, xx in enumerate((-2.6, 0.2)):
        thin(sp, (xx - 1.6, 12.4 - q * 0.4), (xx + 0.8, 8.4 - q * 0.4), (40, 40, 50), 0.6, mask=wing)
    # neck (iridescent)
    hx, hy = 4.6 + hb, 18.6
    neck = sp.union([sp.m_ell(3.2 + hb * 0.5, 14.8, 3.6, 3.2)], tones(PIG_NG))
    sp.fill(neck & (DX.XC < 3.0 + hb * 0.5), PIG_NV)
    sp.fill(neck & (DX.YC > 16.0), mix(PIG_NG, (200, 255, 220), 0.4))
    head = sp.ell(hx, hy, 3.4, 3.0, tones(mix(PIG, (110, 120, 150), 0.3)))
    lx, ly = look
    DX.eye(sp, hx + 1.2, hy + 0.6, 2.4, 2.4, E, PIG_EYE, (lx, ly), blink, lash=INK, skin=mix(PIG, (110, 120, 150), 0.3), bold=1)
    # beak + cere; mouth = the beak opening
    op = max(mouth_, E['mo'])
    sp.poly([(hx + 2.6, hy + 0.2), (hx + 5.2, hy - 0.4), (hx + 2.6, hy - 0.8)], tones((60, 50, 54)))
    if op > 0.1:
        sp.poly([(hx + 2.6, hy - 0.9), (hx + 4.8, hy - 1.4 - op * 1.4), (hx + 2.6, hy - 1.6 - op * 0.8)], tones((60, 50, 54)))
    sp.ell(hx + 2.8, hy + 0.4, 0.7, 0.5, tones((240, 240, 244)), ol=False)                                  # cere
    if fry_:
        fy = hy - 0.6 - op * 0.6
        fry(sp, (hx + 3.2, fy), (hx + 6.0, fy - 2.6))
    sp.anchors.update(head=(hx, hy), mouth=(hx + 4.0, hy - 0.4), eyes=(hx + 1.2, hy + 0.6))
    if prop: prop(sp)
    sp.outline(INK, 1)
    if speaker_:
        speaker(sp, (-9.0, 0.0), t, speaker_on)


# ================================================================================ DORIS — the last human
def doris(sp, t=0.0, expr='warm', mouth_=0.0, look=(0.5, 0.0), blink=None, hand_n=None, hand_f=None, meter='$0.00', wave=None):
    """DORIS — a mini Minnesota grandma: sensible shoes, navy slacks, a floral blouse under a peach cardigan, a red lanyard with a
    «REAL HUMAN» badge and a taxi meter on her belly (meter text), a big teased auburn bouffant with a headset band over it and a
    mic arm, half-moon glasses on the nose on a bead chain, rosy cheeks, smile lines"""
    E = X(expr)
    if blink is None: blink = ((t + 1.3) % 4.4) < 0.13
    br = 0.25 * math.sin(t * 2.2)
    # legs + shoes
    for k_, dx in enumerate((-2.6, 2.6)):
        c = SLACK if k_ else dark(SLACK, 0.85)
        sp.cap((dx, 16.0), (dx, 2.6), 2.2, 1.9, tones(c))
        sp.ell(dx + 1.0, 1.4, 3.0, 1.5, tones((60, 44, 40)))
    # far arm
    shF = (-5.6, 31.0 + br)
    hf = hand_f if hand_f is not None else (-7.4, 19.0)
    kF, eF = ik(shF, hf, 6.0, 5.6, -1.0)
    sp.cap(shF, kF, 2.2, 1.9, tones(dark(CARD_D, 0.84))); sp.cap(kF, eF, 1.9, 1.6, tones(dark(CARD_D, 0.84)))
    sp.ell(eF[0], eF[1], 1.5, 1.4, tones(dark(SKIN_D, 0.9)))
    # torso: cardigan open over a blouse
    tor = sp.union([sp.m_ell(0.6, 24.0, 8.6, 9.6), sp.m_ell(0.4, 31.0, 7.6, 4.0)], tones(CARD_D))
    bl = tor & (DX.XC > -1.0) & (DX.XC < 5.4) & (DX.YC > 16.0)
    sp.paint(bl, tones(BLOUSE), None)
    for q in range(6): sp.dot(0.6 + (q % 3) * 1.6, 30.0 - q * 2.2, (230, 110, 140))                   # floral dots
    for q in range(4): sp.dot(5.8, 28.4 - q * 3.0, (250, 240, 220))                                  # buttons
    # lanyard + badge + taxi meter
    thin(sp, (-1.4, 34.0), (1.8, 23.0), LANY, 0.45); thin(sp, (5.4, 34.0), (2.8, 23.0), LANY, 0.45)
    bd = sp.m_super(2.4, 21.6, 2.8, 1.6, 4.0)[0]
    sp.fill(bd, (250, 250, 246)); sp.fill(bd & ~erode(bd), INK)
    sp.txt_box(['REAL', 'HUMAN'], (-0.2, 20.2, 5.0, 23.0), (30, 60, 140), pad=0.1)
    mtr = sp.m_super(2.2, 14.6, 5.2, 3.6, 4.0)[0]
    sp.paint(mtr, tones(METER), None, olc=INK)
    win = sp.m_super(2.2, 14.6, 4.4, 2.2, 4.0)[0]
    sp.fill(win, (30, 10, 12), keep=True)
    sp.txt_box([meter], (-2.0, 12.6, 6.4, 16.6), LED, pad=0.1)
    sp.anchors['meter'] = (2.2, 14.6)
    # head: back hair -> face -> bangs dome -> headset
    hx, hy = 1.8, 40.6
    puffs = [(hx - 1.0, hy + 4.6, 8.6, 7.4), (hx - 6.0, hy + 0.6, 4.6, 6.4), (hx + 5.2, hy + 3.0, 3.6, 4.6), (hx - 6.8, hy - 4.0, 3.2, 4.0)]
    back = sp.union([sp.m_ell(cx, cy, rx, ry) for (cx, cy, rx, ry) in puffs], tones(HAIR_D))
    for q in range(7):
        a = math.pi * (0.1 + 0.8 * q / 6)
        thin(sp, (hx - 1.0 + math.cos(a) * 5.0, hy + 4.6 + math.sin(a) * 4.2), (hx - 1.0 + math.cos(a) * 7.8, hy + 4.6 + math.sin(a) * 6.6),
             mix(HAIR_D, (255, 220, 180), 0.45), 0.24, mask=back)
    face = sp.union([sp.m_ell(hx + 0.8, hy, 5.8, 6.2), sp.m_ell(hx + 1.6, hy - 2.8, 4.8, 3.8)], tones(SKIN_D))
    bang = sp.union([sp.m_ell(hx + 0.4, hy + 5.4, 6.4, 3.0, -0.12), sp.m_ell(hx + 4.6, hy + 4.4, 2.8, 2.0, -0.4)], tones(HAIR_D))
    thin(sp, (hx - 3.6, hy + 5.8), (hx + 3.0, hy + 6.6), mix(HAIR_D, (255, 220, 180), 0.45), 0.24, mask=bang)
    lx, ly = look
    for (ex, ew) in ((hx + 3.8, 3.4), (hx - 1.0, 3.0)):
        DX.eye(sp, ex, hy + 1.0, ew, 3.2, E, (90, 130, 180), (lx, ly), blink, lash=(60, 30, 30), skin=SKIN_D, bold=1, flick=True)
    for (ex, r) in ((hx + 3.8, 2.0), (hx - 1.0, 1.8)):                                                # half-moon reading glasses
        lens = sp.m_ell(ex, hy - 0.2, r + 0.4, r * 0.75)[0] & (DX.YC < hy - 0.1)
        sp.fill(lens & ~erode(lens), (150, 90, 160))
    thin(sp, (hx + 1.4, hy - 0.3), (hx + 2.0, hy - 0.3), (150, 90, 160), 0.2)
    DX.brow(sp, hx + 3.8, hy + 3.8, 3.2, E, -1, dark(HAIR_D, 0.7), th=1)
    DX.brow(sp, hx - 1.0, hy + 3.7, 2.8, E, +1, dark(HAIR_D, 0.7), th=1)
    for (bx_, by_, rx_) in ((hx + 4.2, hy - 2.0, 1.5), (hx - 1.8, hy - 1.8, 1.2)):
        sp.fill(sp.m_ell(bx_, by_, rx_, rx_ * 0.7)[0] & face, mix(SKIN_D, (240, 110, 120), 0.45))
    if sp.k >= 2:
        thin(sp, (hx + 5.8, hy - 1.0), (hx + 4.8, hy - 3.6), dark(SKIN_D, 0.78), 0.14)
        thin(sp, (hx - 2.6, hy - 1.0), (hx - 1.8, hy - 3.4), dark(SKIN_D, 0.8), 0.14)
        for q in range(2): thin(sp, (hx + 5.6, hy + 1.6 - q * 0.8), (hx + 6.4, hy + 1.2 - q * 0.8), dark(SKIN_D, 0.8), 0.12)
    sp.ell(hx + 6.4, hy - 0.6, 1.4, 1.3, tones(dark(SKIN_D, 0.95)))
    mx, my = hx + 2.8, hy - 3.8
    DX.mouth(sp, mx, my, 4.0, E, mouth_ * 0.8, (200, 70, 90), inside=(110, 30, 50), skin=SKIN_D, maxh=3.6)
    stroke(sp, [(hx - 6.4, hy + 1.0), (hx - 3.6, hy + 11.2), (hx + 3.6, hy + 11.0), (hx + 7.0, hy + 2.0)], (50, 50, 60), 0.5)   # headset band
    sp.ell(hx + 7.0, hy + 0.6, 1.3, 1.7, tones((50, 50, 60)))
    stroke(sp, [(hx + 7.0, hy - 0.6), (hx + 7.4, hy - 3.4), (hx + 5.4, hy - 4.4)], (50, 50, 60), 0.3)
    sp.blob(hx + 5.2, hy - 4.4, 0.6, (30, 30, 36))
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 0.8, hy + 1.2))
    sp.outline(INK, 1)
    # near arm
    before = sp.m.copy()
    shN = (7.4, 31.0 + br)
    if wave is not None: hn = (12.0 + math.sin(wave * 9) * 1.6, 40.0)
    else: hn = hand_n if hand_n is not None else (9.0, 19.0)
    kN, eN = ik(shN, hn, 6.0, 5.6, -1.0 if wave is None else 1.0)
    sp.cap(shN, kN, 2.3, 2.0, tones(CARD_D)); sp.cap(kN, eN, 2.0, 1.7, tones(CARD_D))
    sp.ell(eN[0], eN[1], 1.6, 1.5, tones(SKIN_D))
    sp.anchors['hand'] = eN; sp.anchors['hand_f'] = eF
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


# ================================================================================ KIOSK (XFEENITY self-service) + DOOR
def kiosk(sp, t=0.0, talk=0.0, chute=0.0):
    """a white self-service pillar with a big tilted tablet head (the Fee-Bee face) and a dispenser chute; chute 0..1 = the flap open"""
    sp.sup(0.0, 1.4, 9.0, 1.6, tones(KIO_D), n=3.0)
    pil = sp.poly([(-4.2, 2.6), (4.2, 2.6), (3.4, 38.0), (-3.4, 38.0)], tones(KIO), grad=(38.0, 2.6))
    sp.fill(pil & (np.abs(DX.YC - 30.0) < 0.6), PURP)
    sp.fill(pil & (np.abs(DX.YC - 28.6) < 0.4), MINT_D)
    ch = sp.m_super(0.0, 16.0, 3.2, 2.0, 4.0)[0]
    sp.fill(ch, (40, 40, 50))
    if chute > 0: sp.fill(sp.m_super(0.0, 14.6 - 1.4 * chute, 3.0, 0.5, 4.0)[0], (180, 180, 190))
    sp.txt_box(['FEE-BEE'], (-3.2, 21.0, 3.2, 23.6), PURP, pad=0.1)
    hd = sp.m_super(0.0, 48.0, 12.0, 10.0, 4.0)[0]
    sp.paint(hd, tones(KIO), DX.lit(np.clip(DX.XC / 12.0, -0.9, 0.9), np.clip((DX.YC - 48.0) / 10.0, -0.9, 0.9)))
    sc = sp.m_super(0.0, 48.0, 10.4, 8.4, 4.0)[0]
    sp.fill(sc, (24, 36, 60), keep=True)
    feebee_face(sp, 0.0, 49.0, 6.6, t, talk)
    sp.anchors.update(screen=(0.0, 48.0), chute=(0.0, 15.0), head=(0.0, 48.0))


def door(sp, t=0.0, open_=0.0, glow=1.0):
    """EMPLOYEES ONLY door in the white back wall: a grey frame, the leaf swings in (narrows) and bright light pours from inside"""
    W_, H_ = 26.0, 56.0
    fr = sp.m_super(0.0, H_ / 2 + 0.6, W_ / 2 + 1.6, H_ / 2 + 1.2, 6.0)[0]
    sp.paint(fr, tones((170, 168, 186)), None, olc=INK)
    inner = sp.m_super(0.0, H_ / 2, W_ / 2, H_ / 2, 8.0)[0]
    sp.fill(inner, mix((255, 250, 220), (255, 255, 255), 0.4 * glow) if open_ > 0.02 else (60, 60, 70), keep=True)
    if open_ < 0.999:
        w = W_ * (1 - open_ * 0.86)
        x0 = -W_ / 2
        leaf = sp.m_poly([(x0, 0.0), (x0 + w, 0.0 + 2.0 * open_), (x0 + w, H_ - 2.0 * open_), (x0, H_)])
        sp.paint(leaf, tones((214, 212, 224)), None, olc=INK)
        if open_ < 0.35:
            sp.ell(x0 + w - 2.6, H_ * 0.48, 1.0, 0.8, tones((200, 170, 60)), ol=False)
            pl = sp.m_super(x0 + w / 2, H_ * 0.72, w * 0.40, 5.4, 4.0)[0]
            sp.fill(pl, (204, 36, 46)); sp.fill(pl & ~erode(pl), INK)
            sp.txt_box(['EMPLOYEES', 'ONLY'], (x0 + w / 2 - w * 0.36, H_ * 0.72 - 4.6, x0 + w / 2 + w * 0.36, H_ * 0.72 + 4.6), (255, 255, 255), pad=0.2)
    sp.anchors.update(center=(0.0, H_ / 2), head=(0.0, H_ * 0.8))


# ================================================================================ E02: MADISON (leasing agent) + props
SKIN_M = (236, 196, 164)
HAIR_M = (226, 190, 120)             # honey blonde high ponytail
BLAZER = (214, 196, 170)             # oversized beige blazer
TOP_M = (250, 250, 246)
JEAN_M = (110, 140, 190)
LATTE = (196, 150, 110)


def tablet(sp, h, t=0.0, talk=0.0, screen='feebee'):
    """a tablet held up in the hand: white bezel, the screen shows Fee-Bee (or a form)"""
    x, y = h
    m = sp.m_super(x + 1.0, y + 3.4, 4.4, 3.4, 4.0)[0]
    sp.paint(m, tones((236, 236, 242)), None, olc=INK)
    sc = sp.m_super(x + 1.0, y + 3.4, 3.7, 2.7, 4.0)[0]
    sp.fill(sc, (24, 36, 60), keep=True)
    if screen == 'feebee': feebee_face(sp, x + 1.0, y + 3.6, 2.0, t, talk, eq=False)
    else:
        for q in range(3): thin(sp, (x - 1.8, y + 5.0 - q * 1.3), (x + 3.6, y + 5.0 - q * 1.3), (200, 210, 230), 0.25, keep=True)
    sp.anchors['tablet'] = (x + 1.0, y + 3.4)


def latte(sp, h, sip=0.0):
    """an iced latte in a clear cup with a green straw"""
    x, y = h
    cup = sp.poly([(x - 1.6, y + 4.6), (x + 1.6, y + 4.6), (x + 1.2, y - 0.4), (x - 1.2, y - 0.4)], tones((230, 236, 240)), grad=(y + 4.6, y - 0.4))
    sp.fill(cup & (DX.YC < y + 3.4), LATTE)
    sp.fill(cup & (DX.YC < y + 1.4), dark(LATTE, 0.8))
    thin(sp, (x + 0.4, y + 4.4), (x + 1.2 - sip, y + 7.2), (60, 170, 90), 0.35)
    sp.ell(x, y + 4.7, 1.8, 0.5, tones((240, 244, 248)), ol=False)


def madison(sp, t=0.0, expr='hype', mouth_=0.0, look=(0.5, 0.0), blink=None, hand_n=None, hand_f=None, point=False, sip=0.0):
    """MADISON, 23, leasing agent: white sneakers, mom jeans, a cropped white top under an oversized beige blazer, a huge honey-blonde
    high ponytail with a claw clip, long lashes, glossy lips, an iced latte in the far hand and a tablet (Fee-Bee) in the near one;
    point=True: the latte straw points UP (at the roof)"""
    E = X(expr)
    if blink is None: blink = ((t + 0.6) % 3.6) < 0.12
    br = 0.25 * math.sin(t * 2.4)
    for k_, dx in enumerate((-2.2, 2.2)):
        c = JEAN_M if k_ else dark(JEAN_M, 0.86)
        sp.cap((dx, 21.0), (dx * 1.1, 3.0), 2.4, 2.0, tones(c))
        sp.ell(dx * 1.1 + 1.0, 1.4, 2.8, 1.5, tones((246, 246, 244)))
        sp.fill(sp.m_ell(dx * 1.1 + 1.0, 1.4, 2.8, 1.5)[0] & (DX.YC < 0.6), (190, 190, 196))
    # far arm (latte)
    shF = (-4.6, 37.0 + br)
    hf = hand_f if hand_f is not None else ((-1.0, 47.0) if point else (-6.4, 26.0))
    kF, eF = ik(shF, hf, 6.0, 5.8, -1.0)
    sp.cap(shF, kF, 2.4, 2.0, tones(dark(BLAZER, 0.85))); sp.cap(kF, eF, 2.0, 1.7, tones(dark(BLAZER, 0.85)))
    sp.ell(eF[0], eF[1], 1.3, 1.2, tones(dark(SKIN_M, 0.9)))
    latte(sp, (eF[0], eF[1] - 1.0), sip)
    # torso: oversized blazer open over a cropped top
    tor = sp.union([sp.m_super(0.8, 30.0, 7.6, 9.2, 2.8)], tones(BLAZER))
    top = tor & (DX.XC > -1.0) & (DX.XC < 4.4) & (DX.YC > 24.0)
    sp.paint(top, tones(TOP_M), None)
    sp.fill(tor & (DX.YC < 22.0) & (DX.XC > -1.0) & (DX.XC < 4.4), JEAN_M)
    thin(sp, (-1.0, 38.0), (0.4, 26.0), dark(BLAZER, 0.7), 0.25); thin(sp, (4.4, 38.0), (3.4, 26.0), dark(BLAZER, 0.7), 0.25)
    sp.dot(-2.6, 30.0, (240, 220, 160))
    # head
    hx, hy = 1.6, 45.2
    sp.cap((hx - 0.6, 39.0), (hx - 0.2, 41.0), 1.4, 1.4, tones(SKIN_M))
    pony = sp.union([sp.m_ell(hx - 4.6, hy + 7.6, 3.0, 2.6), sp.m_ell(hx - 7.4, hy + 4.0, 2.4, 4.6, 0.4), sp.m_ell(hx - 8.4, hy - 0.6, 1.8, 3.2, 0.2)],
                    tones(HAIR_M))
    face = sp.union([sp.m_ell(hx, hy, 5.0, 5.6), sp.m_ell(hx + 1.0, hy - 2.6, 4.0, 3.2)], tones(SKIN_M))
    hair = sp.union([sp.m_ell(hx - 0.6, hy + 4.0, 5.6, 2.8, -0.15), sp.m_ell(hx - 4.0, hy + 1.0, 2.0, 3.6)], tones(HAIR_M))
    sp.sup(hx - 3.2, hy + 6.8, 1.8, 0.9, tones((214, 70, 110)), n=3.0)                                     # claw clip
    thin(sp, (hx - 4.0, hy + 4.0), (hx + 3.6, hy + 5.4), mix(HAIR_M, (255, 250, 220), 0.5), 0.25, mask=hair)
    lx, ly = look
    for (ex, ew) in ((hx + 3.0, 3.2), (hx - 1.4, 2.8)):
        DX.eye(sp, ex, hy + 0.8, ew, 3.0, E, (110, 90, 60), (lx, ly), blink, lash=(40, 24, 30), skin=SKIN_M, bold=2, flick=True)
    DX.brow(sp, hx + 3.0, hy + 3.8, 3.0, E, -1, dark(HAIR_M, 0.6), th=1)
    DX.brow(sp, hx - 1.4, hy + 3.7, 2.6, E, +1, dark(HAIR_M, 0.6), th=1)
    for (bx_, by_, rx_) in ((hx + 3.6, hy - 2.0, 1.3), (hx - 2.2, hy - 1.8, 1.1)):
        sp.fill(sp.m_ell(bx_, by_, rx_, rx_ * 0.7)[0] & face, mix(SKIN_M, (240, 120, 130), 0.4))
    sp.ell(hx + 5.6, hy - 0.4, 1.1, 1.1, tones(dark(SKIN_M, 0.95)))
    mx, my = hx + 2.4, hy - 3.4
    DX.mouth(sp, mx, my, 3.6, E, mouth_ * 0.8, (226, 90, 130), inside=(110, 30, 50), skin=SKIN_M, maxh=3.2)
    for (ex_, ey_) in ((hx - 4.4, hy - 1.0),):
        sp.blob(ex_, ey_, 0.6, (240, 210, 90))                                                             # hoop earring
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 0.8, hy + 0.8))
    sp.outline(INK, 1)
    # near arm (tablet)
    before = sp.m.copy()
    shN = (6.6, 37.0 + br)
    hn = hand_n if hand_n is not None else (9.6, 29.0)
    kN, eN = ik(shN, hn, 6.0, 5.8, -1.0)
    sp.cap(shN, kN, 2.5, 2.1, tones(BLAZER)); sp.cap(kN, eN, 2.1, 1.8, tones(BLAZER))
    sp.ell(eN[0], eN[1], 1.4, 1.3, tones(SKIN_M))
    tablet(sp, eN, t, 0.0)
    sp.anchors['hand'] = eN; sp.anchors['hand_f'] = eF
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


def rubber_duck(sp, t=0.0, bob=1.0):
    y = math.sin(t * 2.2) * 0.4 * bob
    sp.ell(0.0, 2.2 + y, 3.2, 2.2, tones((252, 214, 40)))
    sp.ell(2.2, 4.8 + y, 1.8, 1.7, tones((252, 214, 40)))
    sp.ell(3.9, 4.6 + y, 1.0, 0.5, tones((240, 120, 40)), ol=False)
    sp.dot(2.6, 5.4 + y, (20, 20, 20))


def dumbbell(sp, t=0.0):
    thin(sp, (-4.0, 1.4), (4.0, 1.4), (150, 150, 160), 0.5)
    for x in (-4.2, 4.2): sp.sup(x, 1.4, 1.2, 1.6, tones((50, 50, 60)), n=3.0)


def keyring(sp, h, t=0.0, n=7):
    """Sal's giant landlord key ring, hanging from his beak: a brass ring with a fan of keys that jingle"""
    x, y = h
    ring = sp.m_ell(x, y - 1.6, 1.6, 1.6)[0] & ~sp.m_ell(x, y - 1.6, 0.9, 0.9)[0]
    sp.fill(ring, (214, 170, 60))
    for i in range(n):
        a = -math.pi / 2 + (i - n / 2) * 0.26 + math.sin(t * 14 + i) * 0.10
        x1, y1 = x + math.cos(a) * 1.6, y - 1.6 + math.sin(a) * 1.6
        x2, y2 = x + math.cos(a) * 5.4, y - 1.6 + math.sin(a) * 5.4
        thin(sp, (x1, y1), (x2, y2), (226, 196, 90) if i % 2 else (190, 196, 206), 0.32)
        sp.blob(x1, y1, 0.45, (226, 196, 90) if i % 2 else (190, 196, 206))


def briefcase(sp, h=(0.0, 0.0), t=0.0):
    """a tiny leather briefcase standing on its base (h = base centre)"""
    x, y = h
    sp.sup(x, y + 2.4, 3.6, 2.4, tones((110, 66, 40)), n=3.4)
    stroke(sp, [(x - 1.2, y + 4.7), (x - 1.0, y + 5.8), (x + 1.0, y + 5.8), (x + 1.2, y + 4.7)], (60, 40, 30), 0.35)
    thin(sp, (x - 3.4, y + 3.0), (x + 3.4, y + 3.0), (214, 170, 60), 0.22)
    sp.blob(x, y + 3.0, 0.45, (214, 170, 60))



# ================================================================================ E03: DR. CHUCK (doctor / insurance agent) + NURSE
SKIN_C = (232, 188, 160)
HAIR_C = (120, 96, 80)
COAT = (246, 248, 250)
SHIRT_C = (190, 214, 236)
TIE = (150, 40, 60)
SCRUB = (240, 150, 180)
SKIN_N = (196, 140, 110)
HAIR_N = (60, 40, 34)


def chuck(sp, t=0.0, expr='dead', mouth_=0.0, look=(0.5, 0.0), blink=None, mode='doctor', hand_n=None, hand_f=None, phone_=False, spin=0.0,
          phone_f=False, headset=None):
    """DR. CHUCK, 50s, the same tired man in two jobs: mode 'doctor' = white coat + stethoscope + name tag DR. CHUCK; mode 'insurer' =
    no coat, a phone headset + a lanyard UNITED WE BILL. Both: thinning comb-forward hair, huge eye bags, a five-o'clock shadow,
    a short tie with the SAME coffee stain (the clue)"""
    E = X(expr)
    if blink is None: blink = ((t + 0.8) % 4.0) < 0.13
    br = 0.25 * math.sin(t * 1.8)
    for k_, dx in enumerate((-2.6, 2.6)):
        c = (70, 74, 90) if k_ else dark((70, 74, 90), 0.85)
        sp.cap((dx, 22.0), (dx, 3.0), 2.4, 2.1, tones(c))
        sp.ell(dx + 1.2, 1.4, 3.0, 1.5, tones((50, 40, 36)))
    shF = (-6.4, 40.0 + br)
    hf = hand_f if hand_f is not None else (-8.0, 27.0)
    kF, eF = ik(shF, hf, 6.6, 6.2, -1.0)
    armc = COAT if mode == 'doctor' else SHIRT_C
    sp.cap(shF, kF, 2.6, 2.2, tones(dark(armc, 0.86))); sp.cap(kF, eF, 2.2, 1.9, tones(dark(armc, 0.86)))
    sp.ell(eF[0], eF[1], 1.5, 1.4, tones(dark(SKIN_C, 0.9)))
    if phone_f: phone(sp, eF, t, 0.0, screen=None)
    tor = sp.union([sp.m_super(0.6, 32.0, 8.4, 10.6, 2.6)], tones(SHIRT_C))
    thin(sp, (2.2, 41.6), (2.6, 30.0), TIE, 0.9, mask=tor)
    sp.blob(2.4, 34.0, 0.9, (150, 110, 70))                                                       # the coffee stain
    if mode == 'doctor':
        coat = tor & ((DX.XC < -0.6) | (DX.XC > 5.0))
        sp.paint(coat, tones(COAT), None)
        sp.poly([(-7.6, 24.0), (-2.0, 24.0), (-2.6, 16.0), (-7.8, 17.0)], tones(COAT)); sp.poly([(4.4, 24.0), (9.4, 24.0), (9.6, 17.0), (5.0, 16.0)], tones(COAT))
        stroke(sp, [(-0.8, 41.0), (-1.6, 34.0), (0.4, 30.6)], (70, 74, 90), 0.4)                   # stethoscope
        stroke(sp, [(5.4, 41.0), (6.2, 34.0), (4.4, 30.6)], (70, 74, 90), 0.4)
        sp.blob(2.4, 29.8, 1.0, (190, 196, 206))
        tag = sp.m_super(6.6, 37.0, 2.4, 1.0, 4.0)[0]; sp.fill(tag, (250, 250, 250)); sp.fill(tag & ~erode(tag), INK)
        sp.txt_box(['DR. CHUCK'], (4.4, 36.0, 8.8, 38.0), (30, 60, 140), pad=0.1)
    else:
        thin(sp, (-1.4, 41.0), (1.6, 30.0), (200, 40, 60), 0.4); thin(sp, (5.6, 41.0), (3.6, 30.0), (200, 40, 60), 0.4)
        tag = sp.m_super(2.6, 28.6, 2.6, 1.4, 4.0)[0]; sp.fill(tag, (250, 250, 250)); sp.fill(tag & ~erode(tag), INK)
        sp.txt_box(['UNITED', 'WE BILL'], (0.2, 27.4, 5.0, 29.8), (200, 40, 60), pad=0.1)
    hx, hy = 1.8, 48.6
    sp.cap((hx - 0.4, 42.0), (hx, 44.0), 1.8, 1.8, tones(SKIN_C))
    face = sp.union([sp.m_ell(hx, hy, 5.8, 6.2), sp.m_ell(hx + 0.8, hy - 2.6, 4.8, 3.8)], tones(SKIN_C))
    if sp.k <= 2: DX.stubble(sp, sp.m_ell(hx + 1.0, hy - 3.6, 5.0, 2.6)[0] & face, mix(SKIN_C, (110, 100, 100), 0.45), 0.25, 5)
    else: sp.fill(sp.m_ell(hx + 1.0, hy - 3.8, 5.0, 2.4)[0] & face, mix(SKIN_C, (150, 140, 140), 0.25))   # shadow, not a checker
    hair = sp.union([sp.m_ell(hx - 3.8, hy + 2.4, 2.6, 3.4), sp.m_ell(hx - 0.6, hy + 5.4, 4.6, 1.6, -0.1)], tones(HAIR_C))
    for q in range(4): thin(sp, (hx - 3.0 + q * 1.6, hy + 6.2), (hx - 1.0 + q * 1.8, hy + 4.8), dark(HAIR_C, 0.7), 0.2)   # comb-forward strands
    lx, ly = look
    for (ex, ew) in ((hx + 3.4, 3.2), (hx - 1.4, 2.8)):
        DX.eye(sp, ex, hy + 1.0, ew, 2.8, E, (110, 120, 90), (lx, ly), blink, lash=(50, 34, 30), skin=SKIN_C, bold=1,
               bag=dark(SKIN_C, 0.72))
    DX.brow(sp, hx + 3.4, hy + 3.6, 3.2, E, -1, dark(HAIR_C, 0.8), th=1.4)
    DX.brow(sp, hx - 1.4, hy + 3.5, 2.8, E, +1, dark(HAIR_C, 0.8), th=1.4)
    sp.ell(hx + 6.0, hy - 0.6, 1.6, 1.5, tones(dark(SKIN_C, 0.95)))
    mx, my = hx + 2.6, hy - 3.6
    DX.mouth(sp, mx, my, 4.0, E, mouth_ * 0.8, (150, 80, 70), inside=(90, 24, 30), skin=SKIN_C, maxh=3.4)
    if headset if headset is not None else mode == 'insurer':                                    # phone headset
        stroke(sp, [(hx - 5.4, hy + 1.0), (hx - 2.0, hy + 6.8), (hx + 3.6, hy + 6.4), (hx + 6.2, hy + 1.6)], (40, 40, 46), 0.45)
        sp.ell(hx + 6.0, hy + 0.8, 1.2, 1.6, tones((40, 40, 46)))
        stroke(sp, [(hx + 6.0, hy - 0.4), (hx + 6.0, hy - 3.0), (hx + 4.2, hy - 3.6)], (40, 40, 46), 0.3)
        sp.blob(hx + 4.0, hy - 3.6, 0.55, (20, 20, 24))
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 0.8, hy + 1.0))
    sp.outline(INK, 1)
    before = sp.m.copy()
    shN = (7.6, 40.0 + br)
    hn = hand_n if hand_n is not None else (10.0, 27.0)
    kN, eN = ik(shN, hn, 6.6, 6.2, -1.0)
    sp.cap(shN, kN, 2.7, 2.3, tones(armc)); sp.cap(kN, eN, 2.3, 2.0, tones(armc))
    sp.ell(eN[0], eN[1], 1.6, 1.5, tones(SKIN_C))
    if phone_: phone(sp, eN, t, 0.0, screen=None)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


def nurse(sp, t=0.0, expr='warm', mouth_=0.0, look=(0.5, 0.0), blink=None, hug=0.0, hand_n=None, hand_f=None):
    """the NURSE: pink scrubs, a tight bun with a pencil, a lanyard, teal crocs; hug 0..1 opens both arms wide"""
    E = X(expr)
    if blink is None: blink = ((t + 0.3) % 3.9) < 0.12
    for k_, dx in enumerate((-2.4, 2.4)):
        c = SCRUB if k_ else dark(SCRUB, 0.86)
        sp.cap((dx, 21.0), (dx, 3.0), 2.4, 2.1, tones(c))
        sp.ell(dx + 1.0, 1.5, 2.9, 1.6, tones((60, 190, 180)))
    shF = (-5.6, 37.0)
    hf = hand_f if hand_f is not None else ((-13.0, 40.0) if hug > 0.5 else (-7.0, 26.0))
    kF, eF = ik(shF, hf, 6.0, 5.8, -1.0)
    sp.cap(shF, kF, 2.3, 2.0, tones(dark(SCRUB, 0.86))); sp.cap(kF, eF, 1.9, 1.6, tones(dark(SKIN_N, 0.9)))
    sp.ell(eF[0], eF[1], 1.4, 1.3, tones(dark(SKIN_N, 0.9)))
    tor = sp.union([sp.m_super(0.6, 29.6, 7.8, 9.2, 2.6)], tones(SCRUB))
    sp.fill(sp.m_poly([(-0.6, 38.6), (4.4, 38.6), (1.9, 34.6)]) & tor, dark(SCRUB, 0.75))           # v-neck
    hx, hy = 1.8, 44.6
    face = sp.union([sp.m_ell(hx, hy, 5.2, 5.8), sp.m_ell(hx + 0.8, hy - 2.4, 4.2, 3.4)], tones(SKIN_N))
    hair = sp.union([sp.m_ell(hx - 0.8, hy + 4.4, 5.4, 2.6, -0.1), sp.m_ell(hx - 3.6, hy + 7.6, 2.8, 2.6), sp.m_ell(hx - 4.4, hy + 1.6, 1.8, 3.0)],
                    tones(HAIR_N))
    thin(sp, (hx - 6.0, hy + 9.0), (hx - 1.4, hy + 6.8), (240, 200, 60), 0.35)                       # pencil in the bun
    lx, ly = look
    for (ex, ew) in ((hx + 3.2, 3.2), (hx - 1.4, 2.8)):
        DX.eye(sp, ex, hy + 0.8, ew, 3.0, E, (70, 50, 34), (lx, ly), blink, lash=(30, 20, 20), skin=SKIN_N, bold=2, flick=True)
    DX.brow(sp, hx + 3.2, hy + 3.8, 3.0, E, -1, HAIR_N, th=1)
    DX.brow(sp, hx - 1.4, hy + 3.7, 2.6, E, +1, HAIR_N, th=1)
    sp.ell(hx + 5.6, hy - 0.4, 1.3, 1.3, tones(dark(SKIN_N, 0.95)))
    mx, my = hx + 2.4, hy - 3.4
    DX.mouth(sp, mx, my, 3.8, E, mouth_ * 0.8, (170, 70, 90), inside=(100, 30, 40), skin=SKIN_N, maxh=3.4)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 0.8, hy + 0.8))
    sp.outline(INK, 1)
    before = sp.m.copy()
    shN = (7.0, 37.0)
    hn = hand_n if hand_n is not None else ((16.0, 40.0) if hug > 0.5 else (9.0, 26.0))
    kN, eN = ik(shN, hn, 6.0, 5.8, -1.0)
    sp.cap(shN, kN, 2.4, 2.1, tones(SCRUB)); sp.cap(kN, eN, 2.0, 1.7, tones(SKIN_N))
    sp.ell(eN[0], eN[1], 1.5, 1.4, tones(SKIN_N))
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


def receipt(sp, t=0.0, n=4, lines=None):
    """a long paper receipt curling out of a printer, itemised"""
    L = lines or ['SKIN-TO-SKIN $39.99', 'ICE PACK $180', 'ASPIRIN $45', 'TISSUE (USED) $12']
    h = 4.2 * len(L) + 2.0
    m = sp.m_super(0.0, h / 2, 7.0, h / 2, 6.0)[0]
    sp.paint(m, tones((252, 250, 240)), None, olc=(160, 160, 160))
    for i, line in enumerate(L):
        sp.txt_box([line], (-6.4, h - 4.0 - i * 4.2, 6.4, h - 1.2 - i * 4.2), (40, 40, 50) if i else (200, 40, 48), pad=0.1)


# ================================================================================ E04: the hatchback, the Sky Patrol drone, the officer
CAR = (206, 52, 48)
CAR_D = (140, 34, 34)
RUST = (150, 90, 40)
COP = (54, 70, 110)
COP_HAT = (150, 120, 80)


DUKE_IN_CAR = 0.355            # Duke's scale relative to the car's (the car is 3.5 m long = 52 sprite px; Duke 1.9 m = 80 sprite px)


def hatchback(sp, t=0.0, part='all', sale=False, honk=0.0, drive=0.0):
    """a tiny dented 2009 red hatchback, side view facing right: rust spots, a bungee-corded bumper, a donut spare; the windows are
    LEFT OPEN (transparent) so whoever sits inside shows through; part='body' paints only the body around the window holes.
    sale=True: a «FOR SALE $500 OBO» card in the rear window; drive = wheel rotation phase"""
    W2, base = 26.0, 3.2
    bob = math.sin(t * 9.0) * 0.25 * (1.0 if drive else 0.0)
    body = sp.union([sp.m_super(0.0, 9.0 + bob, W2, 5.6, 3.0), sp.m_super(-3.0, 17.4 + bob, 15.4, 5.2, 2.6)], tones(CAR))
    win = sp.m_super(-1.6, 18.0 + bob, 13.2, 3.8, 3.0)[0] & body
    pillar = (DX.XC > -2.6) & (DX.XC < -0.6)
    hole = win & ~pillar
    sp.m[hole] = False                                                                              # see-through windows
    sp.fill(win & pillar, CAR_D)
    for (x, y, r) in ((-18.0, 7.0, 1.6), (12.0, 11.0, 1.2), (-6.0, 6.0, 1.0)):                     # rust + dents
        sp.fill(sp.m_ell(x, y + bob, r * 1.4, r)[0] & body & ~hole, RUST)
    thin(sp, (-25.0, 6.0 + bob), (-19.0, 6.4 + bob), (40, 40, 44), 0.6)                             # bungee-corded bumper
    sp.ell(-26.0, 11.0 + bob, 1.6, 3.0, tones((40, 40, 44)))
    sp.ell(24.6, 10.2 + bob, 1.4, 1.2, tones((255, 236, 160)), ol=False, gloss=1.0)                 # headlight
    sp.ell(-25.2, 13.0 + bob, 0.9, 1.0, tones((220, 40, 40)), ol=False)
    for wx in (-15.0, 15.0):
        sp.ell(wx, base + 1.0, 4.4, 4.4, tones((30, 30, 36)))
        sp.ell(wx, base + 1.0, 2.0, 2.0, tones((180, 180, 190)))
        a = drive * 6.0
        thin(sp, (wx + math.cos(a) * 1.8, base + 1.0 + math.sin(a) * 1.8), (wx - math.cos(a) * 1.8, base + 1.0 - math.sin(a) * 1.8), (90, 90, 100), 0.3)
    if sale:
        pl = sp.m_super(-11.0, 18.2 + bob, 3.4, 2.6, 4.0)[0]
        sp.fill(pl, (252, 250, 240)); sp.m |= pl
        sp.txt_box(['FOR', 'SALE', '$500'], (-14.0, 16.0 + bob, -8.0, 20.6 + bob), (200, 40, 48), pad=0.1)
    if honk > 0:
        for q in range(3):
            thin(sp, (27.5 + q * 1.2, 14.0 - q * 1.2), (28.5 + q * 1.2, 15.0 + q * 0.6), (255, 255, 255), 0.25)
    sp.anchors.update(seat=(-2.0, 9.0), seat_p=(8.0, 9.0), center=(0.0, 12.0))
    sp.outline(INK, 1)
    sp.m[hole] = False


def drone(sp, t=0.0, siren=True):
    """the SKY PATROL police drone: four rotors (blurred), a white body with a blue stripe, a red/blue siren bar, a loudspeaker"""
    y0 = 10.0 + math.sin(t * 5.0) * 0.6
    sp.sup(0.0, y0, 7.0, 2.6, tones((240, 242, 248)), n=3.0)
    sp.fill(sp.m_super(0.0, y0 - 0.4, 6.6, 0.6, 4.0)[0], (40, 70, 150))
    sp.txt_box(['SKY PATROL'], (-5.6, y0 + 0.2, 5.6, y0 + 2.2), (40, 70, 150), pad=0.1)
    for x in (-9.0, 9.0):
        thin(sp, (x * 0.6, y0 + 1.0), (x, y0 + 3.0), (80, 80, 90), 0.4)
        blade = sp.m_ell(x, y0 + 3.4, 4.0, 0.6)[0]
        sp.fill(blade & ((DX.XC * 3 + int(t * 40)) % 2 < 1), (190, 196, 210)); sp.m |= blade
    on = int(t * 6) % 2 == 0
    sp.sup(-1.8, y0 + 3.0, 1.6, 0.9, tones((230, 40, 40) if (siren and on) else (120, 40, 40)), n=3.0)
    sp.sup(1.8, y0 + 3.0, 1.6, 0.9, tones((40, 90, 240) if (siren and not on) else (40, 50, 120)), n=3.0)
    sp.ell(5.0, y0 - 2.6, 1.6, 1.2, tones((60, 60, 70)))                                            # loudspeaker
    sp.ell(-3.0, y0 - 2.4, 1.0, 1.0, tones((30, 30, 36)))                                            # camera
    sp.dot(-3.0, y0 - 2.4, (255, 60, 60))
    sp.anchors.update(center=(0.0, y0), head=(0.0, y0))
    sp.outline(INK, 1)


def officer(sp, t=0.0, expr='glare', mouth_=0.0, look=(0.5, 0.0), blink=None, hand_n=None, hand_f=None, ticket=False):
    """the SKY PATROL officer: a campaign hat, mirrored aviators pushed up on the hat, a horseshoe moustache, a navy uniform with a gold badge,
    a ticket book in the far hand, a pen in the near one"""
    E = X(expr)
    if blink is None: blink = ((t + 1.4) % 4.2) < 0.13
    for k_, dx in enumerate((-2.8, 2.8)):
        c = COP if k_ else dark(COP, 0.86)
        sp.cap((dx, 22.0), (dx, 3.0), 2.6, 2.2, tones(c))
        sp.ell(dx + 1.2, 1.4, 3.2, 1.6, tones((24, 24, 28)), gloss=1.0)
    shF = (-6.6, 41.0)
    hf = hand_f if hand_f is not None else ((-4.0, 29.0) if ticket else (-8.0, 27.0))
    kF, eF = ik(shF, hf, 6.8, 6.4, -1.0)
    sp.cap(shF, kF, 2.7, 2.3, tones(dark(COP, 0.86))); sp.cap(kF, eF, 2.3, 2.0, tones(dark(COP, 0.86)))
    sp.ell(eF[0], eF[1], 1.5, 1.4, tones(dark(SKIN_C, 0.9)))
    if ticket:
        tk = sp.m_super(eF[0] + 1.4, eF[1] + 2.6, 2.6, 3.4, 4.0)[0]
        sp.fill(tk, (252, 250, 236)); sp.m |= tk; sp.fill(tk & ~erode(tk), INK)
        for q in range(3): thin(sp, (eF[0] - 0.4, eF[1] + 4.2 - q * 1.2), (eF[0] + 3.0, eF[1] + 4.2 - q * 1.2), (120, 120, 130), 0.2)
    tor = sp.union([sp.m_super(0.6, 32.6, 8.8, 10.8, 2.6)], tones(COP))
    sp.ell(-3.4, 36.0, 1.4, 1.6, tones((236, 196, 70)), gloss=1.0)                                  # badge
    thin(sp, (-8.0, 23.6), (9.2, 23.6), (30, 30, 34), 0.9)                                          # belt
    hx, hy = 1.8, 49.0
    sp.cap((hx - 0.4, 42.4), (hx, 44.4), 1.9, 1.9, tones(SKIN_C))
    face = sp.union([sp.m_ell(hx, hy, 5.8, 6.0), sp.m_ell(hx + 0.8, hy - 2.6, 4.8, 3.8)], tones(SKIN_C))
    lx, ly = look
    for (ex, ew) in ((hx + 3.4, 3.2), (hx - 1.4, 2.8)):
        DX.eye(sp, ex, hy + 0.8, ew, 2.8, E, (80, 100, 120), (lx, ly), blink, lash=(40, 30, 30), skin=SKIN_C, bold=1)
    DX.brow(sp, hx + 3.4, hy + 3.4, 3.4, E, -1, (90, 70, 50), th=1.6)
    DX.brow(sp, hx - 1.4, hy + 3.3, 2.8, E, +1, (90, 70, 50), th=1.6)
    sp.ell(hx + 6.0, hy - 0.6, 1.6, 1.5, tones(dark(SKIN_C, 0.95)))
    mx, my = hx + 2.6, hy - 3.8
    DX.mouth(sp, mx, my, 4.0, E, mouth_ * 0.8, (150, 80, 70), inside=(90, 24, 30), skin=SKIN_C, maxh=3.4)
    stroke(sp, [(hx - 0.4, my - 2.4), (hx - 0.2, my + 0.8), (hx + 5.4, my + 0.8), (hx + 5.6, my - 2.4)], (100, 76, 54), 0.7)   # horseshoe moustache
    hat = sp.union([sp.m_super(hx + 0.4, hy + 6.4, 9.6, 1.0, 4.0), sp.m_ell(hx + 0.4, hy + 8.8, 4.8, 2.8)], tones(COP_HAT))
    thin(sp, (hx - 3.6, hy + 7.6), (hx + 4.4, hy + 7.6), (60, 50, 40), 0.4)
    for ex in (hx - 1.6, hx + 2.6): sp.ell(ex, hy + 7.6, 1.4, 0.9, tones((140, 170, 200)), ol=False, gloss=1.0)   # aviators on the hat
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 0.8, hy + 0.8))
    sp.outline(INK, 1)
    before = sp.m.copy()
    shN = (7.8, 41.0)
    hn = hand_n if hand_n is not None else ((9.6, 29.0) if ticket else (10.0, 27.0))
    kN, eN = ik(shN, hn, 6.8, 6.4, -1.0)
    sp.cap(shN, kN, 2.8, 2.4, tones(COP)); sp.cap(kN, eN, 2.4, 2.1, tones(SKIN_C))
    sp.ell(eN[0], eN[1], 1.6, 1.5, tones(SKIN_C))
    if ticket: thin(sp, eN, (eN[0] - 2.4, eN[1] + 2.0), (40, 40, 160), 0.35)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


# ================================================================================ E05: REX the red-tailed hawk (rock star) + laptop
_REX = dict(EAGLE_W=(176, 112, 70), EAGLE_G=(130, 84, 52), EAGLE_B=(116, 72, 44), BEAK=(84, 84, 96), BEAK_D=(60, 60, 72),
            IRIS_E=(170, 100, 40), JACK=(34, 34, 40), JRED=(70, 70, 84), JWHT=(206, 206, 216), GOLD=(206, 206, 216), LENS=(20, 20, 26))


def rex(sp, t=0.0, **kw):
    """REX, the red-tailed hawk whose scream every movie gives to the bald eagle: the same bird-of-prey build as Duke but leaner, a rusty
    brown head and tail, a dark grey beak, a black leather jacket with silver piping and a silver chain, dark aviators ON the eyes, the
    long head feather standing up like a mohawk (flop)"""
    g = globals()
    old = {k: g[k] for k in _REX}
    g.update(_REX)
    try:
        kw.setdefault('shades', 'eyes'); kw.setdefault('flop', 0.9); kw.setdefault('puff', -0.6)
        duke(sp, t=t, **kw)
    finally:
        g.update(old)


def laptop(sp, t=0.0, screen='ticket'):
    """an open laptop on the table (side-ish view): the screen faces the viewer a little, a sticker «TICKETMAXED»"""
    sp.poly([(-9.0, 0.0), (9.0, 0.0), (8.0, 1.6), (-8.0, 1.6)], tones((170, 174, 186)), grad=(1.6, 0.0))
    lid = sp.m_super(0.0, 8.8, 8.4, 6.6, 4.0)[0]
    sp.paint(lid, tones((60, 64, 76)), None, olc=INK)
    sc = sp.m_super(0.0, 8.8, 7.4, 5.6, 4.0)[0]
    sp.fill(sc, (240, 60, 90) if (screen == 'ticket' and int(t * 3) % 2) else (30, 40, 70), keep=True)
    sp.txt_box(['$600'], (-6.0, 6.2, 6.0, 11.4), (255, 255, 255), pad=0.2)
    sp.anchors.update(screen=(0.0, 8.8))


# ================================================================================ E06: the coconut Fee-Bee, a cocktail, the bag sizer
def coconut(sp, t=0.0, talk=0.0, awake=1.0):
    """a coconut on the palm that wakes up as a Fee-Bee speaker: brown husk, then two glowing eyes and a mint smile (awake 0..1)"""
    m = sp.ell(0.0, 4.0, 4.2, 4.0, tones((120, 76, 40)))
    for q in range(5): thin(sp, (-3.0 + q * 1.4, 7.2), (-2.4 + q * 1.4, 1.0), (90, 56, 30), 0.25, mask=m)
    if awake > 0.05:
        k = min(1.0, awake)
        for ex in (-1.4, 1.4):
            sp.blob(ex, 5.0, 0.7 * k, MINT, keep=True)
            sp.blob(ex - 0.15, 5.2, 0.25 * k, (255, 255, 255), keep=True)
        op = min(1.0, talk * 1.4)
        if op < 0.08:
            for q in range(7):
                u = (q - 3) / 3.0
                sp.blob(u * 1.8, 2.8 + 0.6 * u * u, 0.32 * k, MINT, keep=True)
        else:
            mm = sp.m_ell(0.0, 2.6, 1.8, 0.5 + 1.2 * op)[0]
            sp.fill(mm, MINT, keep=True); sp.fill(erode(mm), (20, 60, 50), keep=True)
    sp.anchors.update(head=(0.0, 4.0), center=(0.0, 4.0))


def cocktail(sp, h):
    x, y = h
    sp.poly([(x - 1.6, y + 4.0), (x + 1.6, y + 4.0), (x + 0.3, y + 1.0), (x - 0.3, y + 1.0)], tones((255, 150, 80)), grad=(y + 4.0, y + 1.0))
    thin(sp, (x, y + 1.0), (x, y - 0.6), (220, 220, 230), 0.25)
    sp.ell(x, y - 0.8, 1.2, 0.3, tones((220, 220, 230)), ol=False)
    sp.sup(x + 1.6, y + 4.8, 1.2, 0.6, tones((255, 80, 140)), n=2.0, ol=False)                    # tiny umbrella
    thin(sp, (x + 1.6, y + 4.8), (x + 0.6, y + 3.4), (240, 240, 240), 0.15)


def sizer_front(sp, t=0.0, w=19.0, h=22.0):
    """the front bars of the metal carry-on sizer frame (drawn OVER whoever is squeezed inside)"""
    for x in (-w / 2, w / 2):
        thin(sp, (x, 0.0), (x, h), (150, 150, 160), 0.9)
    thin(sp, (-w / 2, h), (w / 2, h), (150, 150, 160), 0.9)
    pl = sp.m_super(0.0, h - 2.6, 4.6, 1.6, 4.0)[0]
    sp.fill(pl, (255, 214, 60)); sp.m |= pl
    sp.txt_box(['MAX'], (-4.0, h - 4.0, 4.0, h - 1.2), (20, 20, 30), pad=0.1)
