"""«Прохор. Таёжные лайфхаки» cast + props, drawn in the «Морозный лубок» manner (props/taigapix.py).
Coordinates: sprite px, feet anchor at (0, 0), x right = facing side, y UP.
  prokhor(sp, ...)   — Прохор, таёжный блогер-лайфхакер: «сугроб с бородой» (pyramid: ushanka on top, a beard down to the belt)
  potapych(sp, ...)  — Михал Потапыч Топтыгин, медведь-«управляющий» (УК «Берлога»): a huge pear of fur in a nightcap + reading glasses
Props: bill (квитанция), terminal (card reader), pillow, meter (электросчётчик), phone_pole."""
import math
import numpy as np
from props import dibspix as DX
from props.dibspix import dark, mix, erode, dilate, ik, EXPR
from props.taigapix import tones, thin, stroke, INK, WHITE, FROST, SNOW

# ---------------------------------------------------------------- palette
SKIN = (232, 164, 128)              # ruddy, wind-burnt
NOSE = (226, 74, 70)                # frostbitten potato nose
BEARD = (198, 98, 44)               # rust-ginger
BEARD_G = (196, 186, 172)           # one grey streak
JACKET = (62, 74, 92)               # телогрейка: dark blue-grey quilt
TAPE = (52, 112, 226)               # синяя изолента
HAT = (122, 84, 54)                 # ушанка: rabbit fur
HAT_L = (92, 60, 40)                # leather crown
FELT = (156, 154, 160)              # валенки
GALOSH = (176, 36, 40)              # калоши
MITT = (206, 44, 48)                # варежки
ROPE = (176, 140, 86)
WOOD = (170, 112, 60)
STEEL = (190, 198, 210)

FUR = (122, 74, 42)                 # Потапыч
FUR_L = (196, 148, 98)              # muzzle / belly
CAP_A, CAP_B = (64, 92, 190), (236, 236, 246)     # nightcap stripes
GOLD = (222, 184, 70)

XTRA = dict(
    bliss=dict(eo=0.0, pu=0.6, bt=-0.4, bl=0.5, mo=0.0, mc=0.85, shut=True),
    plead=dict(eo=1.15, pu=0.55, bt=-0.85, bl=0.7, mo=0.3, mc=-0.5),
    frozen=dict(eo=0.9, pu=0.4, bt=-0.5, bl=0.3, mo=0.15, mc=-0.3),
    chatter=dict(eo=1.0, pu=0.45, bt=-0.6, bl=0.5, mo=0.0, mc=0.6, teeth=True),
    proud=dict(eo=0.85, pu=0.55, bt=0.15, bl=0.2, mo=0.0, mc=0.9, teeth=True),
    asleep=dict(eo=0.0, pu=0.6, bt=0.0, bl=0.0, mo=0.0, mc=0.1, shut=True),
    yawn=dict(eo=0.0, pu=0.6, bt=-0.3, bl=0.4, mo=1.0, mc=0.0, shut=True),
    boss=dict(eo=0.62, pu=0.55, bt=0.05, bl=0.0, mo=0.0, mc=-0.05, lid=0.62),
)


def X(expr):
    return dict(XTRA.get(expr) or EXPR.get(expr, EXPR['normal']))


# ================================================================================ props held in a hand (callbacks prop(sp, hand))
def bill(sp, h, ang=0.0, amount='9 000 ₽', big=False):
    """квитанция ЖКУ: a paper slip (header band, «ОТОПЛЕНИЕ», the amount in red) held at hand h"""
    x, y = h
    w, hh = (16.0, 20.0) if big else (9.0, 12.0)
    x0, y0 = x - w * 0.15, y - hh * 0.35
    m = sp.m_poly([(x0, y0), (x0 + w, y0 + 0.6), (x0 + w - 0.4, y0 + hh), (x0 - 0.3, y0 + hh - 0.4)])
    sp.paint(m, [(196, 196, 206), (244, 242, 232), (255, 255, 248)], np.clip((DX.XC - x0) / w, 0, 1) * 0.6 + 0.3, olc=(120, 120, 130))
    sp.fill(m & (DX.YC > y0 + hh * 0.80), (90, 120, 170))                                 # blue header band
    sp.txt_box(['КВИТАНЦИЯ'], (x0 + 0.4, y0 + hh * 0.80, x0 + w - 0.6, y0 + hh - 0.5), WHITE, pad=0.2)
    sp.txt_box(['ОТОПЛЕНИЕ'], (x0 + 0.4, y0 + hh * 0.56, x0 + w - 0.6, y0 + hh * 0.78), (40, 40, 50), pad=0.3)
    sp.txt_box([amount], (x0 + 0.4, y0 + hh * 0.14, x0 + w - 0.6, y0 + hh * 0.52), (210, 30, 36), pad=0.3)
    sp.anchors['bill'] = (x0 + w / 2, y0 + hh / 2)


def terminal(sp, h, amount='9 000 ₽', glow=1.0):
    """«ТАЙГА-БАНК» card reader in a big paw"""
    x, y = h
    body = sp.m_super(x + 2.0, y + 4.5, 4.6, 7.4, 3.0)[0]
    sp.paint(body, tones((70, 74, 84)), np.clip((DX.YC - y) / 14, 0, 1) * 0.5 + 0.35, olc=INK)
    scr = sp.m_super(x + 2.0, y + 8.2, 3.5, 2.6, 4.0)[0]
    sp.fill(scr, mix((20, 40, 30), (110, 240, 150), 0.25 * glow))
    sp.txt_box([amount], (x - 1.4, y + 6.0, x + 5.4, y + 10.4), (140, 255, 170), pad=0.15)
    for i in range(3):
        for j in range(3):
            sp.fill(sp.m_ell(x - 0.4 + i * 2.4, y + 3.4 - j * 2.0, 0.6, 0.45)[0], (200, 204, 214))
    sp.anchors['terminal'] = (x + 2.0, y + 8.2)


def pillow(sp, h, ang=0.0):
    x, y = h
    m = sp.m_super(x + 1.0, y + 1.0, 7.0, 4.4, 2.4)[0]
    sp.paint(m, tones((236, 236, 244)), np.clip((DX.YC - y + 4) / 9, 0, 1) * 0.7 + 0.2, olc=(110, 120, 150))
    for k in range(-6, 8, 3): sp.fill(m & (np.abs(DX.XC - (x + k)) < 0.35), (110, 140, 210))      # ticking stripes


def phone(sp, h, rec=True):
    x, y = h
    m = sp.m_super(x, y + 3.0, 2.2, 3.8, 4.0)[0]
    sp.paint(m, tones((40, 40, 46)), None, olc=INK)
    sp.fill(sp.m_super(x, y + 3.0, 1.6, 3.0, 4.0)[0], (90, 160, 210))
    if rec: sp.fill(sp.m_ell(x + 0.8, y + 5.6, 0.45, 0.45)[0], (255, 40, 40))


# ================================================================================ Прохор (v2, 12.10.2026: bigger head, clean big shapes)
def prokhor(sp, t=0.0, expr='normal', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
            hat_off=False, sweat=0.0, frost=0.0, walk=None, chatter=0.0, legs=True, lean=0.0, steam=0.0, camo=False, swollen=0.0):
    """ПРОХОР v2 — city man gone taiga lumberjack, a caricature you read at a glance: a BIG head (≈40 % of the height) with huge eyes,
    a frostbitten potato nose, a wide talking mouth under a ginger moustache and a clean, chunky ginger beard down to the chest; a
    big puffy ushanka (one flap down, one sticking up like a wing); a stocky quilted телогрейка with blue electrical tape, rope belt,
    axe at the back, valenki in red galoshes, red mittens. walk = phase (legs, bob, arm swing)."""
    E = X(expr)
    if blink is None: blink = (t % 3.7) < 0.12
    br = 0.35 * math.sin(t * 2.2)
    bob = abs(math.sin(walk)) * 1.2 if walk is not None else 0.0
    jit = (math.sin(t * 70.0) * 0.45) if chatter else 0.0
    def Q(x, y): return (x + lean * (y / 50.0) * 5.0 + (jit if y > 30 else 0), y + (bob if y > 9 else bob * 0.3))
    swing = math.sin(walk) * 5.0 if walk is not None else 0.0

    # ---------------------------------------------------------------- far arm (behind)
    shF = Q(-11.0, 32.0 + br * 0.3)
    hf = hand_f if hand_f is not None else Q(-16.0 - swing * 0.6, 18.0)
    kF, eF = ik(shF, hf, 9.0, 8.5, -1.0)
    sp.cap(shF, kF, 3.6, 3.2, tones(dark(JACKET, 0.78))); sp.cap(kF, eF, 3.2, 2.9, tones(dark(JACKET, 0.78)))
    sp.ell(eF[0], eF[1] - 0.6, 3.1, 2.9, tones(dark(MITT, 0.78)))
    if prop_f: prop_f(sp, eF)
    sp.anchors['hand_f'] = eF
    # axe in the belt at the back
    sp.cap(Q(-12.0, 13.0), Q(-18.0, 29.0), 1.0, 0.9, tones(WOOD))
    blade = sp.m_poly([Q(-20.4, 26.0), Q(-16.0, 29.2), Q(-15.4, 31.8), Q(-21.6, 30.4)])
    sp.paint(blade, tones(STEEL), np.clip((DX.YC - 26) / 6, 0, 1) * 0.7 + 0.2, gloss=0.6)
    # ---------------------------------------------------------------- legs: valenki in galoshes
    if legs:
        sw = math.sin(walk) * 2.6 if walk is not None else 0.0
        for k_, dx in enumerate((-5.4, 5.4)):
            s_ = sw if k_ else -sw
            c = FELT if k_ else dark(FELT, 0.82)
            lift = max(0.0, s_) * 0.5
            sp.cap((dx * 0.9, 11.0), (dx + s_ * 0.7, 3.4 + lift), 4.0, 4.2, tones(c))
            sp.ell(dx + s_ * 0.7 + 1.8, 2.4 + lift, 5.4, 2.8, tones(c))
            gal = sp.m_ell(dx + s_ * 0.7 + 1.9, 1.7 + lift, 5.6, 2.3)[0]
            sp.paint(gal, tones(GALOSH), DX.lit(np.zeros_like(DX.XC), np.clip((DX.YC - 1.7 - lift) / 2.3, -1, 1)), gloss=0.7)
    # ---------------------------------------------------------------- телогрейка
    hem = sp.m_poly([Q(-16.4, 9.4), Q(17.6, 9.4), Q(15.0, 15.0), Q(-14.0, 15.0)])
    hem_n = (np.clip((DX.XC - 0.5) / 17.0, -0.9, 0.9) * 0.85, np.full_like(DX.XC, -0.05))
    body = sp.union([sp.m_super(*Q(0.8, 22.5), 15.0, 13.5, 3.0), sp.m_ell(*Q(0.8, 33.0), 13.6, 4.8), (hem,) + hem_n], tones(JACKET))
    sp.fill(body & (np.abs(((DX.YC - bob - 11.0) % 3.6) - 1.8) > 1.62), dark(JACKET, 0.66))                 # quilting rows (subtle)
    for (a, b) in ((Q(-11.0, 27.0), Q(-5.0, 23.0)), (Q(-10.6, 23.2), Q(-5.4, 27.2)), (Q(10.0, 11.4), Q(15.0, 13.4))):
        sp.fill(sp.m_cap(a, b, 1.0, 1.0)[0] & body, TAPE)
    sp.cap(Q(-14.6, 15.4), Q(16.0, 15.4), 0.9, 0.9, tones(ROPE))                                             # rope belt
    if camo:                                                                                                 # «маскхалат» of fir branches
        FIR = (50, 110, 70)
        cape = sp.union([sp.m_ell(*Q(0.8, 24.0), 18.5, 15.5), sp.m_ell(*Q(-6.0, 14.0), 12.0, 7.0), sp.m_ell(*Q(8.0, 14.0), 12.0, 7.0)], tones(FIR))
        for q in range(26):
            a = q * 2.4; x0 = 0.8 + math.cos(a) * (6 + (q % 5) * 2.4); y0 = 24.0 + math.sin(a) * (5 + (q % 4) * 2.4)
            thin(sp, Q(x0, y0), Q(x0 + 2.2, y0 - 1.6), dark(FIR, 0.62), 0.28, mask=cape)
            thin(sp, Q(x0, y0), Q(x0 - 2.0, y0 - 1.8), mix(FIR, (180, 230, 160), 0.35), 0.22, mask=cape)
    # ---------------------------------------------------------------- head
    hx, hy = Q(3.0, 47.5)
    face = sp.union([sp.m_ell(hx, hy, 10.0, 10.4), sp.m_ell(hx + 2.4, hy - 4.0, 8.4, 6.6)], tones(SKIN))
    lx, ly = look
    DX.eye(sp, hx + 4.2, hy + 2.4, 5.6, 5.8, E, (70, 120, 160), (lx, ly), blink, lash=INK, skin=SKIN, bold=1)
    DX.eye(sp, hx - 2.8, hy + 2.4, 4.8, 5.4, E, (70, 120, 160), (lx, ly), blink, lash=INK, skin=SKIN, bold=1)
    Eb = dict(E, bl=E['bl'] * 0.7)
    BROW = (150, 70, 34)
    DX.brow(sp, hx + 4.4, hy + 7.6, 6.2, Eb, +1, BROW, th=3, bushy=True)
    DX.brow(sp, hx - 2.9, hy + 7.5, 5.0, Eb, -1, BROW, th=3, bushy=True)
    if sp.k >= 2:
        for q in range(3): thin(sp, (hx + 7.4, hy + 2.6 - q * 1.0), (hx + 8.8, hy + 3.2 - q * 1.5), dark(SKIN, 0.72), 0.2)    # crow's feet
    DX.blush(sp, hx - 0.4, hy - 2.6, 2.6, 1.6, (232, 100, 96))
    mx, my = hx + 4.0, hy - 5.8
    mo = max(mouth_, E['mo'])
    # beard: jaw + cheeks + a chunky spade down to the chest, with a clean hole around the mouth
    hole = sp.m_ell(mx, my + 0.4 - mo * 1.6, 5.2 + mo * 0.6, 2.6 + mo * 3.2)[0]
    bd = sp.union([sp.m_ell(hx + 1.6, hy - 9.0, 11.0, 7.6), sp.m_ell(hx + 2.2, hy - 15.0, 9.0, 9.2), sp.m_ell(hx - 7.6, hy - 3.0, 3.2, 5.6)],
                  tones(BEARD), exclude=hole)
    for i, (a, b) in enumerate((((-5.0, -10.0), (-3.6, -20.0)), ((0.0, -12.0), (0.4, -24.0)), ((5.0, -12.0), (4.0, -22.0)),
                                ((8.6, -9.0), (7.0, -17.0)), ((-2.4, -15.0), (-1.4, -22.0)))):
        stroke(sp, [(hx + a[0], hy + a[1]), (hx + (a[0] + b[0]) / 2 + 0.8, hy + (a[1] + b[1]) / 2), (hx + b[0], hy + b[1])], dark(BEARD, 0.62), 0.32)
    for (a, b) in (((-3.0, -8.0), (-2.0, -13.0)), ((3.0, -10.4), (3.6, -15.0))):
        thin(sp, (hx + a[0], hy + a[1]), (hx + b[0], hy + b[1]), mix(BEARD, (255, 220, 160), 0.45), 0.3)
    if frost: sp.frost(bd & (DX.YC > hy - 16), 0.02 * frost, 6)
    DX.mouth(sp, mx, my, 6.6, E, mouth_, (120, 40, 34), inside=(80, 20, 28), skin=SKIN, maxh=9, big_teeth=False)
    if chatter and sp.k >= 2:
        sp.fill(sp.m_ell(mx, my - 0.5, 3.2, 1.1)[0], WHITE, keep=True)
        for q in range(-3, 4): thin(sp, (mx + q * 0.95, my - 1.5), (mx + q * 0.95, my + 0.5), (170, 170, 184), 0.12, keep=True)
    ms = sp.union([sp.m_ell(mx - 2.6, my + 2.6, 4.2, 1.9, 0.3), sp.m_ell(mx + 2.8, my + 2.6, 3.8, 1.8, -0.3)], tones(mix(BEARD, (240, 150, 80), 0.25)))
    thin(sp, (mx - 5.0, my + 2.2), (mx - 1.0, my + 3.0), dark(BEARD, 0.62), 0.25); thin(sp, (mx + 1.0, my + 3.0), (mx + 5.2, my + 2.2), dark(BEARD, 0.62), 0.25)
    if swollen > 0:                                                                                     # toothache: a balloon cheek + bandage
        sp.ell(hx - 3.6, hy - 4.6, 6.0 * swollen + 2.0, 5.4 * swollen + 2.0, tones(mix(SKIN, (240, 120, 110), 0.35)), gloss=0.6)
    nose = sp.ell(hx + 8.6, hy - 1.0, 4.2, 3.6, tones(NOSE), gloss=1.0)
    sp.fill(sp.m_ell(hx + 7.4, hy - 2.8, 0.7, 0.5)[0], dark(NOSE, 0.5))
    if frost: sp.frost(sp.m_ell(hx + 1.0, hy + 6.8, 8.0, 1.6)[0] & sp.m, 0.10 * frost, 9)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), nose=(hx + 8.6, hy - 1.0), eyes=(hx + 0.8, hy + 2.4))
    # ---------------------------------------------------------------- ushanka
    if not hat_off:
        wing = sp.ell(hx + 12.2, hy + 12.4, 5.0, 2.8, tones(HAT), ang=0.55)                            # far flap up like a wing
        sp.ell(hx + 0.2, hy + 12.6, 11.6, 6.0, tones(HAT_L))                                         # crown
        band = sp.union([sp.m_ell(hx + 0.6, hy + 8.6, 12.4, 3.4), sp.m_ell(hx + 9.6, hy + 9.2, 3.4, 3.4)], tones(HAT))
        flap = sp.cap((hx - 10.4, hy + 7.4), (hx - 11.0, hy - 3.4), 3.4, 3.0, tones(HAT))              # near flap down
        for (a, b) in (((-8.0, 9.6), (-6.4, 7.8)), ((-3.0, 10.2), (-1.4, 8.2)), ((2.6, 10.2), (4.2, 8.2)), ((7.6, 10.0), (9.0, 8.2)),
                       ((-11.4, 3.0), (-10.0, 1.4)), ((-11.0, -0.6), (-9.8, -2.0))):
            thin(sp, (hx + a[0], hy + a[1]), (hx + b[0], hy + b[1]), dark(HAT, 0.6), 0.35)
        thin(sp, (hx - 11.2, hy - 5.6), (hx - 10.4, hy - 9.6), (230, 220, 200), 0.22)                  # untied string
        sp.sup(hx - 2.0, hy + 14.0, 2.0, 1.1, tones(TAPE), n=3.0)                                    # изолента on the crown
        if camo:
            for q in range(5):
                a = -1.0 + q * 0.5
                thin(sp, (hx - 1.0, hy + 16.0), (hx - 1.0 + math.cos(a + 1.57) * 7.0, hy + 16.0 + math.sin(a + 1.57) * 6.0), (50, 110, 70), 0.6)
        if frost: sp.frost(band, 0.05 * frost, 12)
    else:
        sp.ell(hx, hy + 8.2, 9.8, 4.4, tones(SKIN), gloss=0.9)                                      # bald dome
        for q in range(4): thin(sp, (hx - 9.4 + q * 0.5, hy + 4.0 + q * 1.4), (hx - 11.6, hy + 3.0 + q * 1.6), BEARD, 0.4)
    if sweat > 0:
        for i, (x, y) in enumerate(((hx - 4.0, hy + 5.0), (hx + 7.0, hy + 4.0), (hx - 7.4, hy + 0.5))[:int(1 + 2 * sweat)]):
            yy = y - ((t * 4.0 + i * 1.3) % 4.0)
            sp.ell(x, yy, 0.8, 1.2, tones((170, 220, 255)), ol=False, snow=False); sp.dot(x - 0.2, yy + 0.4, WHITE)
    sp.outline(INK, 1)
    # ---------------------------------------------------------------- near arm + mitten
    before = sp.m.copy()
    shN = Q(13.0, 32.0 + br * 0.3)
    hn = hand_n if hand_n is not None else Q(19.0 + swing * 0.6, 18.0)
    kN, eN = ik(shN, hn, 9.0, 8.5, -1.0)
    sp.cap(shN, kN, 3.7, 3.3, tones(JACKET)); sp.cap(kN, eN, 3.3, 3.0, tones(JACKET))
    if prop_n and getattr(prop_n, 'behind', False): prop_n(sp, eN)
    mit = sp.ell(eN[0] + 0.4, eN[1] - 0.4, 3.3, 3.0, tones(MITT))
    sp.ell(eN[0] + 2.4, eN[1] + 1.6, 1.3, 1.6, tones(MITT))
    sp.fill(mit & (np.abs(DX.YC - (eN[1] - 0.2)) < 0.45) & DX.CHECK, WHITE)
    if prop_n and not getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


# ================================================================================ Михал Потапыч
def potapych(sp, t=0.0, expr='asleep', mouth_=0.0, look=(0.6, -0.1), blink=None, eyes=None, glasses=True, cap=True, bubble=None,
             hand_n=None, prop_n=None, slump=0.0, snore=True):
    """МИХАЛ ПОТАПЫЧ — a huge pear of brown fur sitting in his den: tiny heavy-lidded eyes behind round reading glasses on a string,
    striped nightcap with a pompon, a glossy black nose, a lighter muzzle and belly, claws. Asleep he slumps and blows a snot bubble.
    eyes: None (from expr) | 'one' (only the near eye opens: the twist) ; bubble: 0..1 size of the nose bubble (None = from t while asleep)"""
    E = X(expr)
    asleep = expr in ('asleep', 'yawn') and eyes is None
    if blink is None: blink = (t % 4.6) < 0.14
    breathe = 0.8 * math.sin(t * (1.6 if asleep else 2.4))
    sl = slump
    def Q(x, y): return (x + sl * (y / 70.0) * 6.0, y - sl * (y / 70.0) * 4.0)

    # far leg / far arm
    sp.cap((-12.0, 9.0), (-26.0, 5.0), 7.4, 6.4, tones(dark(FUR, 0.8)))
    sp.ell(-29.0, 6.0, 5.0, 7.0, tones(dark(FUR, 0.8)))
    shF = Q(-14.0, 46.0)
    sp.cap(shF, Q(-24.0, 26.0), 6.6, 5.6, tones(dark(FUR, 0.8)))
    # body (pear) + belly
    body = sp.union([sp.m_ell(0.0, 28.0 + breathe * 0.3, 30.0, 27.0 + breathe * 0.4), sp.m_ell(*Q(2.0, 48.0), 22.0, 14.0)], tones(FUR))
    sp.fur(body, dark(FUR, 0.70), step=4.2, ln=2.6, ang=-1.9, seed=21)
    bel = sp.ell(7.0, 26.0 + breathe * 0.3, 17.0, 18.0 + breathe * 0.4, tones(FUR_L), flat=0.05)
    sp.fur(bel, dark(FUR_L, 0.82), step=4.6, ln=2.0, ang=-1.7, seed=22)
    # near leg with a padded foot
    sp.cap((8.0, 9.0), (24.0, 5.0), 8.0, 7.0, tones(FUR))
    foot = sp.ell(29.0, 7.0, 5.6, 7.6, tones(FUR))
    sp.ell(31.0, 7.0, 3.4, 5.2, tones((90, 64, 56)), snow=False)
    for q in range(4): sp.ell(32.4, 2.4 + q * 2.8, 1.0, 0.9, tones((70, 50, 46)), snow=False)
    # ---------------------------------------------------------------- head
    hx, hy = Q(8.0, 64.0)
    hx += 0.0; hy += -sl * 2.0
    for ex, ey in ((hx - 12.0, hy + 11.0), (hx + 8.0, hy + 13.0)):
        sp.ell(ex, ey, 5.2, 4.8, tones(FUR)); sp.ell(ex + 0.6, ey - 0.4, 2.8, 2.4, tones((96, 60, 42)), snow=False)
    head = sp.union([sp.m_ell(hx, hy, 16.0, 14.0), sp.m_ell(hx - 2.0, hy - 6.0, 15.0, 9.0)], tones(FUR))
    sp.fur(head, dark(FUR, 0.70), step=3.6, ln=2.0, ang=-1.9, seed=23)
    mz = sp.union([sp.m_ell(hx + 8.0, hy - 5.0, 10.0, 7.0)], tones(FUR_L))
    sp.fur(mz, dark(FUR_L, 0.84), step=3.4, ln=1.2, ang=-1.6, seed=24)
    # eyes: small, heavy-lidded bureaucrat
    lx, ly = look
    if eyes == 'one':
        Ef = dict(X('asleep'))
        DX.eye(sp, hx - 1.0, hy + 3.0, 3.0, 2.6, Ef, (60, 40, 30), (lx, ly), True, lash=INK, skin=FUR)
        DX.eye(sp, hx + 6.0, hy + 3.2, 3.6, 3.0, X('boss'), (120, 70, 30), (lx, ly), False, lash=INK, skin=FUR, lidc=dark(FUR, 0.9))
    else:
        DX.eye(sp, hx - 1.0, hy + 3.0, 3.0, 2.6, E, (120, 70, 30), (lx, ly), blink, lash=INK, skin=FUR, lidc=dark(FUR, 0.9))
        DX.eye(sp, hx + 6.0, hy + 3.2, 3.6, 3.0, E, (120, 70, 30), (lx, ly), blink, lash=INK, skin=FUR, lidc=dark(FUR, 0.9))
    Eb = dict(E, bt=E['bt'] * 0.6)
    DX.brow(sp, hx + 6.2, hy + 6.4, 4.0, Eb, +1, dark(FUR, 0.5), th=1, bushy=True)
    DX.brow(sp, hx - 1.2, hy + 6.2, 3.4, Eb, -1, dark(FUR, 0.5), th=1, bushy=True)
    # nose + mouth
    nx_, ny_ = hx + 15.0, hy - 1.8
    sp.ell(nx_, ny_, 3.6, 2.6, tones((40, 34, 36)), gloss=1.2, snow=False)
    thin(sp, (nx_ - 1.0, ny_ - 2.4), (nx_ - 1.6, ny_ - 5.0), dark(FUR_L, 0.55), 0.3)
    mx, my = hx + 10.6, hy - 8.0
    mo = max(mouth_, E['mo'])
    if mo > 0.10:
        hw = 3.4 + 2.0 * mo; hh = 1.0 + 4.2 * mo
        mm = sp.m_ell(mx, my - hh * 0.4, hw, hh)[0]
        sp.fill(mm, (70, 20, 24)); inner = erode(mm)
        sp.fill(inner & (DX.YC < my - hh * 0.9), (200, 90, 100))                               # tongue
        for sgn in (-1, 1):                                                                     # fangs
            fx_ = mx + sgn * hw * 0.55
            sp.fill(sp.m_poly([(fx_ - 0.7, my + hh * 0.5 - 0.2), (fx_ + 0.7, my + hh * 0.5 - 0.2), (fx_, my + hh * 0.5 - 2.2)]) & mm, WHITE, keep=True)
        sp.fill(mm & ~erode(mm), INK)
    else:
        stroke(sp, [(mx - 3.4, my + 0.4 + 0.6 * E['mc']), (mx - 1.0, my), (mx + 1.6, my + 0.2), (mx + 3.0, my + 0.8 + 0.6 * E['mc'])], INK, 0.32)
    # glasses on a string
    if glasses:
        gy = hy + 2.2 + (-1.6 if expr in ('asleep',) and eyes is None else 0.0)
        for gx, r in ((hx + 6.0, 3.0), (hx - 1.0, 2.6)):
            ring = sp.m_ell(gx, gy, r, r * 0.9)[0] & ~sp.m_ell(gx, gy, r - 0.45, r * 0.9 - 0.45)[0]
            sp.fill(ring, GOLD)
            sp.fill(sp.m_ell(gx - r * 0.4, gy + r * 0.3, 0.5, 0.4)[0], WHITE)
        thin(sp, (hx + 2.7, gy + 0.3), (hx + 3.3, gy + 0.3), GOLD, 0.25)
        stroke(sp, [(hx - 3.6, gy), (hx - 6.0, gy - 6.0), (hx - 2.0, hy - 14.0), (hx + 4.0, hy - 16.0)], GOLD, 0.16)
    # nightcap
    if cap:
        tip = (hx - 22.0, hy + 14.0 + 2.0 * math.sin(t * 1.3))
        cm = sp.m_poly([(hx - 13.0, hy + 9.0), (hx + 6.0, hy + 14.6), (tip[0] + 2.0, tip[1] + 1.0), (tip[0], tip[1] - 1.2)])
        sp.paint(cm, tones(CAP_B), DX.lit(np.zeros_like(DX.XC), np.zeros_like(DX.XC) + 0.4))
        band = (((DX.XC - DX.YC * 0.7) // 3.0) % 2 == 0) & cm
        sp.fill(band, CAP_A); sp.fill(cm & ~erode(cm), INK)
        sp.ell(hx - 4.0, hy + 11.0, 10.4, 2.4, tones(CAP_B), ang=0.25)                             # cuff
        sp.ell(tip[0] - 1.0, tip[1] - 1.4, 2.6, 2.6, tones(CAP_B))                                 # pompon
        sp.fur(sp.m_ell(tip[0] - 1.0, tip[1] - 1.4, 2.6, 2.6)[0], (200, 200, 220), step=1.2, ln=0.8, seed=31)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), nose=(nx_, ny_), eye=(hx + 6.0, hy + 3.2), belly=(7.0, 26.0))
    sp.outline(INK, 1)
    # snot bubble while asleep
    if (asleep and snore) or bubble:
        b = bubble if bubble is not None else 0.5 + 0.5 * math.sin(t * 1.6)
        if b > 0.08:
            r = 0.8 + 3.6 * b
            bm = sp.m_ell(nx_ + 1.4 + r * 0.6, ny_ - 1.6 - r * 0.2, r, r * 0.92)[0]
            sp.fill(bm & ~sp.m, mix((170, 210, 230), (255, 255, 255), 0.3))
            sp.fill(bm & ~erode(bm) & ~sp.m, (110, 150, 180))
            sp.fill(sp.m_ell(nx_ + 0.8 + r * 0.3, ny_ - 0.8 - r * 0.2 + r * 0.4, r * 0.25, r * 0.2)[0], WHITE)
            sp.m |= bm
    # near arm: rests on the belly asleep, or holds a prop
    before = sp.m.copy()
    shN = Q(18.0, 46.0)
    hn = hand_n if hand_n is not None else ((16.0, 22.0) if asleep else (30.0, 30.0))
    kN, eN = ik(shN, hn, 12.0, 11.0, -1.0)
    sp.cap(shN, kN, 7.0, 6.2, tones(FUR)); sp.cap(kN, eN, 6.2, 5.4, tones(FUR))
    pw = sp.ell(eN[0] + 1.0, eN[1], 5.0, 4.4, tones(FUR))
    sp.fur(pw, dark(FUR, 0.66), step=2.0, ln=1.4, seed=25)
    for q in range(3):
        c0 = (eN[0] + 4.6, eN[1] + 2.2 - q * 2.0)
        sp.fill(sp.m_cap(c0, (c0[0] + 2.0, c0[1] - 0.8), 0.7, 0.3)[0], (236, 230, 214))
    if prop_n: prop_n(sp, (eN[0] + 2.0, eN[1] + 2.0))
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


# ================================================================================ world props (drawn as sprites)
def meter(sp, t=0.0, rub=0, spin=0.0, snow_cap=True):
    """old Soviet electricity meter «СО-2» on a plank: a black box, a window with the spinning disc and the rouble drum counter"""
    box = sp.m_super(0.0, 10.0, 8.0, 10.0, 3.6)[0]
    sp.paint(box, tones((50, 52, 60)), np.clip((DX.YC) / 20, 0, 1) * 0.6 + 0.2, olc=INK)
    win = sp.m_super(0.0, 12.6, 6.0, 5.0, 4.0)[0]
    sp.fill(win, (210, 220, 220))
    disc_y = 9.6
    sp.fill(sp.m_super(0.0, disc_y, 5.2, 0.9, 3.0)[0], (180, 184, 190))
    ph = (spin * 1.0) % 1.0
    mk = -4.6 + 9.2 * ph
    sp.fill(sp.m_super(mk, disc_y, 0.6, 0.9, 3.0)[0], (200, 30, 36))                          # red mark on the disc
    dig = sp.m_super(0.0, 14.2, 5.4, 1.8, 6.0)[0]
    sp.fill(dig, (24, 24, 28))
    sp.txt_box([f'{int(rub):05d}'], (-5.2, 12.6, 5.2, 15.8), WHITE, pad=0.1)
    sp.txt_box(['СО-2'], (-6.0, 3.0, 6.0, 6.2), (220, 220, 210), pad=0.2)
    if snow_cap:
        sp.sup(0.0, 20.4, 9.0, 1.8, tones((236, 244, 255)), n=2.0, snow=False)
    sp.outline(INK, 1)
    sp.anchors['dial'] = (0.0, 14.2)


def ice_over(sp, k=1.0, t=0.0):
    """encase a finished sprite in an ice block (Act(post=...)), growing from the feet up: k 0..1 = how high the ice has climbed.
    Icy tint + frost on the covered part, a translucent block with a bright rim and diagonal glints"""
    m = sp.m.copy()
    ys, xs = np.nonzero(m)
    if not len(xs) or k <= 0: return
    y0, y1, x0, x1 = ys.min() - 3 * sp.k, ys.max() + 3 * sp.k, xs.min() - 4 * sp.k, xs.max() + 4 * sp.k
    top = int(y1 - (y1 - y0) * min(1.0, k))
    rr, cc = np.mgrid[0:sp.H, 0:sp.W]
    cov = m & (rr >= top)
    sp.col[cov] = (sp.col[cov].astype(np.float32) * 0.55 + np.array((170, 214, 250)) * 0.45).astype(np.uint8)
    blk = (rr >= max(0, top)) & (rr < y1) & (cc >= max(0, x0)) & (cc < x1)
    if k < 1.0:                                                       # a jagged crystal front while it climbs
        jag = ((cc // max(1, 3 * sp.k)) % 2 == 0) & (rr < top + 2 * sp.k)
        blk &= ~jag
    rim = blk & ~erode(erode(blk))
    out = blk & ~m
    sp.col[out] = (206, 234, 255)
    sp.col[rim] = (244, 252, 255)
    diag = blk & ((((cc * 0.8 - rr) / sp.k) % 14.0) < 1.0)
    sp.col[diag] = (252, 255, 255)
    sp.m |= blk


def tripod(sp, t=0.0, rec=True, screen=None):
    """a cheap camera tripod with his smartphone on top (the blogger's camera): three thin legs, a clamp, the phone with a red REC dot"""
    for (fx_, a) in ((-8.0, 0.0), (8.0, 0.0), (1.5, 0.0)):
        thin(sp, (fx_, a), (0.0, 30.0), (60, 64, 72), 0.55)
        thin(sp, (fx_ * 0.98, a + 0.4), (0.0, 30.0), (150, 156, 168), 0.22)
    sp.cap((0.0, 29.0), (0.0, 33.0), 0.8, 0.8, tones((60, 64, 72)))
    ph = sp.m_super(0.0, 36.6, 2.8, 4.6, 4.0)[0]
    sp.paint(ph, tones((34, 34, 40)), None, olc=INK)
    sp.fill(sp.m_super(0.0, 36.6, 2.1, 3.8, 4.0)[0], screen or (60, 110, 160))
    if rec and int(t * 2) % 2 == 0: sp.fill(sp.m_ell(-1.0, 39.6, 0.7, 0.7)[0], (255, 40, 40))
    sp.fill(sp.m_ell(1.2, 39.6, 0.6, 0.6)[0], (20, 20, 24))                     # the lens
    sp.outline(INK, 1)
    sp.anchors['phone'] = (0.0, 36.6)


def bear_paw(sp, t=0.0, bill_=True, reach=1.0):
    """the bear's huge furry forearm coming in from the right (pointing left), claws, the bill pinned under it"""
    a, b = (34.0, 20.0), (34.0 - 26.0 * reach, 20.0)
    arm = sp.cap(a, b, 9.0, 7.4, tones(FUR))
    sp.fur(arm, dark(FUR, 0.7), step=4.0, ln=2.4, ang=3.0, seed=41)
    pw = sp.ell(b[0] - 2.0, b[1], 7.2, 6.4, tones(FUR))
    for q in range(4):
        c0 = (b[0] - 8.4, b[1] + 4.2 - q * 2.8)
        sp.fill(sp.m_cap(c0, (c0[0] - 2.6, c0[1] - 0.8), 0.9, 0.35)[0], (236, 230, 214))
    if bill_: bill(sp, (b[0] - 14.0, b[1] - 6.0), big=True)
    sp.outline(INK, 1)


def den_sign(sp, text=('НЕ', 'БУДИТЬ!')):
    """a plywood sign on a stake stuck into the den mound"""
    sp.cap((0.0, 0.0), (0.4, 16.0), 0.8, 0.7, tones(WOOD))
    pl = sp.m_poly([(-9.0, 12.0), (9.0, 12.6), (8.6, 24.0), (-8.8, 23.4)])
    sp.paint(pl, tones((214, 178, 120)), np.clip((DX.YC - 12) / 12, 0, 1) * 0.6 + 0.25, olc=(110, 80, 50))
    sp.txt_box(list(text), (-8.0, 13.2, 8.0, 22.8), (170, 30, 30), pad=0.4)
    sp.sup(0.0, 24.6, 9.6, 1.4, tones((236, 244, 255)), n=2.0, snow=False)
    sp.outline(INK, 1)


def stump_desk(sp, t=0.0, lamp=0.0):
    """the bear's office: a tree stump as a desk with a green-shaded desk lamp (lamp 0..1 on), an abacus, a mug, a stamp and folders"""
    st = sp.union([sp.m_super(0.0, 9.0, 15.0, 9.0, 3.2), sp.m_ell(0.0, 18.0, 15.0, 2.6)], tones((150, 104, 62)))
    sp.fill(sp.m_ell(0.0, 18.0, 13.6, 2.0)[0], (196, 150, 96))
    for r in (3.0, 6.0, 9.0, 12.0):
        ring = sp.m_ell(0.0, 18.0, r, r * 0.16)[0] & ~sp.m_ell(0.0, 18.0, r - 0.35, r * 0.16 - 0.2)[0]
        sp.fill(ring, (150, 104, 62))
    for x in (-10.0, -4.0, 3.0, 9.0): thin(sp, (x, 15.0), (x + 0.4, 1.0), dark((150, 104, 62), 0.6), 0.22)
    # folders
    for i, (c, lab) in enumerate((((60, 90, 160), 'ДОЛЖНИКИ'), ((150, 60, 50), 'ПЕНИ'), ((70, 120, 70), 'ДОЛЖНИКИ-2'))):
        y0 = 18.6 + i * 2.6
        sp.sup(-6.0 + (i % 2) * 0.8, y0 + 1.2, 6.6, 1.3, tones(c), n=4.0, snow=False)
        sp.txt_box([lab], (-12.0 + (i % 2) * 0.8, y0, -0.2 + (i % 2) * 0.8, y0 + 2.4), WHITE, pad=0.1)
    # abacus
    sp.sup(8.0, 21.6, 5.0, 3.2, tones((120, 76, 40)), n=4.0, snow=False)
    for r_ in range(3):
        y = 20.2 + r_ * 1.4
        thin(sp, (3.4, y), (12.6, y), (200, 200, 200), 0.14)
        for q in range(6):
            x = 4.4 + q * 1.4 + (2.6 if (q + r_) % 3 == 0 else 0)
            sp.fill(sp.m_ell(min(x, 12.0), y, 0.55, 0.5)[0], (220, 60, 50) if q % 2 else (240, 220, 160))
    # mug «ЛУЧШЕМУ УПРАВЛЯЮЩЕМУ»
    sp.sup(-12.2, 21.4, 2.4, 3.0, tones((236, 236, 240)), n=3.0, snow=False)
    sp.txt_box(['ЛУЧШ.', 'УПР.'], (-14.4, 19.0, -10.0, 23.8), (30, 50, 120), pad=0.1)
    # desk lamp
    thin(sp, (10.0, 25.0), (11.6, 32.0), (40, 60, 40), 0.5)
    sp.ell(10.0, 24.6, 2.4, 0.9, tones((40, 70, 50)), snow=False)
    sh = sp.m_poly([(8.4, 31.0), (15.6, 33.6), (15.0, 35.8), (9.6, 35.4)])
    sp.paint(sh, tones((40, 120, 70)), np.clip((DX.YC - 31) / 5, 0, 1) * 0.6 + 0.25)
    if lamp > 0: sp.fill(sp.m_ell(12.4, 32.0, 2.4, 0.9)[0], mix((80, 80, 70), (255, 240, 170), lamp), keep=True)
    sp.anchors['lamp'] = (12.4, 31.6)
    sp.outline(INK, 1)
