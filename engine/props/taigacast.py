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


# ================================================================================ Прохор
def prokhor(sp, t=0.0, expr='normal', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
            hat_off=False, sweat=0.0, frost=0.4, breath=None, lean=0.0, walk=None, chatter=0.0, legs=True, beard_items=True):
    """ПРОХОР — «сугроб с бородой»: pyramid silhouette (small head in an ushanka with ONE ear-flap up like a wing, a wide quilted
    телогрейка patched with blue electrical tape, a rust-ginger beard down to the rope belt with a wooden spoon, a fishing float and a
    pine cone living in it), frostbitten potato nose, frosted brows, valenki in red galoshes, red mittens. Axe in the belt at the back."""
    E = X(expr)
    if blink is None: blink = (t % 3.7) < 0.12
    br = 0.35 * math.sin(t * 2.2)
    jit = (math.sin(t * 60.0) * 0.35) if chatter else 0.0
    def Q(x, y): return (x + lean * (y / 50.0) * 4.0 + (jit if y > 30 else 0), y)

    # ---------------------------------------------------------------- far arm (behind)
    shF = Q(-9.0, 38.0 + br * 0.3)
    hf = hand_f if hand_f is not None else Q(-15.0, 24.0)
    kF, eF = ik(shF, hf, 9.0, 8.4, -1.0)
    sp.cap(shF, kF, 3.4, 3.0, tones(dark(JACKET, 0.8))); sp.cap(kF, eF, 3.0, 2.6, tones(dark(JACKET, 0.8)))
    sp.ell(eF[0], eF[1] - 0.6, 2.6, 2.4, tones(dark(MITT, 0.8)))
    if prop_f: prop_f(sp, eF)
    sp.anchors['hand_f'] = eF

    # ---------------------------------------------------------------- the axe in the belt at the back (silhouette element)
    sp.cap(Q(-12.0, 18.0), Q(-17.5, 33.0), 0.9, 0.8, tones(WOOD))
    blade = sp.m_poly([Q(-19.6, 30.6), Q(-15.6, 33.4), Q(-15.0, 35.6), Q(-20.6, 34.4)])
    sp.paint(blade, tones(STEEL), np.clip((DX.YC - 30) / 6, 0, 1) * 0.7 + 0.2, gloss=0.6)

    # ---------------------------------------------------------------- legs: valenki in galoshes
    if legs:
        sw = math.sin(walk) * 2.4 if walk is not None else 0.0
        for k_, dx in enumerate((-5.0, 5.0)):
            s_ = sw if k_ else -sw
            c = FELT if k_ else dark(FELT, 0.82)
            sp.cap((dx * 0.9, 12.0), (dx + s_ * 0.6, 3.0), 3.4, 3.6, tones(c))
            sp.ell(dx + s_ * 0.6 + 1.6, 2.2, 4.8, 2.6, tones(c))
            gal = sp.m_ell(dx + s_ * 0.6 + 1.7, 1.6, 5.0, 2.2)[0]
            sp.paint(gal, tones(GALOSH), DX.lit(np.zeros_like(DX.XC), np.clip((DX.YC - 1.6) / 2.2, -1, 1)), gloss=0.7)
    # ---------------------------------------------------------------- телогрейка (quilted, flared hem)
    hem = sp.m_poly([Q(-15.6, 10.6), Q(16.4, 10.6), Q(14.0, 18.0), Q(-13.0, 18.0)])
    hem_n = (np.clip((DX.XC - 0.5) / 16.0, -0.9, 0.9) * 0.85, np.full_like(DX.XC, -0.05))
    body = sp.union([sp.m_super(*Q(0.5, 26.0), 14.0, 15.5, 3.4), sp.m_ell(*Q(0.5, 39.5), 12.0, 5.0), (hem,) + hem_n], tones(JACKET))
    qx = DX.XC - lean * (DX.YC / 50.0) * 4.0
    sp.fill(body & (np.abs(((DX.YC - 13.0) % 3.4) - 1.7) > 1.48), dark(JACKET, 0.62))       # quilting rows
    sp.fill(body & (np.abs(((qx + 12.0) % 4.0) - 2.0) > 1.68) & (np.abs(((DX.YC - 14.7) % 3.4) - 1.7) < 0.32), dark(JACKET, 0.7))   # stitches
    for (a, b) in ((Q(-10.0, 34.0), Q(-4.0, 30.0)), (Q(-9.6, 30.2), Q(-4.4, 34.2)), (Q(9.0, 14.0), Q(14.0, 16.4))):   # изолента patches
        sp.fill(sp.m_cap(a, b, 0.9, 0.9)[0] & body, TAPE)
        thin(sp, a, b, mix(TAPE, WHITE, 0.45), 0.18)
    sp.anchors['chest'] = Q(2.0, 30.0)

    # ---------------------------------------------------------------- head (drawn before the beard: the beard covers chin + cheeks)
    hx, hy = Q(4.0, 53.5)
    sp.cap(Q(2.0, 41.0), Q(3.0, 47.0), 3.4, 3.4, tones(SKIN))
    face = sp.union([sp.m_ell(hx, hy, 6.2, 6.8), sp.m_ell(hx + 1.6, hy - 3.2, 5.4, 3.8)], tones(SKIN))
    lx, ly = look
    DX.eye(sp, hx + 2.8, hy + 1.3, 3.6, 3.4, E, (70, 120, 160), (lx, ly), blink, lash=INK, skin=SKIN)
    DX.eye(sp, hx - 1.8, hy + 1.3, 3.0, 3.1, E, (70, 120, 160), (lx, ly), blink, lash=INK, skin=SKIN)
    Eb = dict(E, bl=E['bl'] * 0.5)
    BROW = mix(BEARD, BEARD_G, 0.35)
    DX.brow(sp, hx + 2.9, hy + 4.0, 4.0, Eb, +1, BROW, th=2, bushy=True)
    DX.brow(sp, hx - 1.8, hy + 4.0, 3.2, Eb, -1, BROW, th=2, bushy=True)
    if sp.k >= 2:                                                                       # crow's feet + under-eye bags
        for q in range(3): thin(sp, (hx + 4.6, hy + 1.6 - q * 0.8), (hx + 5.6, hy + 2.0 - q * 1.1), dark(SKIN, 0.7), 0.16)
        thin(sp, (hx + 1.6, hy - 0.4), (hx + 3.8, hy - 0.5), dark(SKIN, 0.82), 0.16)
    DX.blush(sp, hx + 0.6, hy - 1.6, 2.0, 1.3, (230, 90, 90))
    nose = sp.ell(hx + 6.4, hy - 1.2, 2.8, 2.4, tones(NOSE), gloss=1.0)                 # potato nose
    sp.fill(sp.m_ell(hx + 5.6, hy - 2.4, 0.5, 0.4)[0], dark(NOSE, 0.5))
    # beard: chin + cheeks + a long fan down to the belt; mouth is drawn on top of it
    bd = sp.union([sp.m_ell(*Q(4.6, 34.0), 10.6, 13.6), sp.m_ell(hx + 0.5, hy - 5.4, 7.2, 5.2), sp.m_ell(*Q(5.0, 23.0), 7.4, 5.0)],
                  tones(BEARD), exclude=~(DX.YC > 19.6))
    grey = bd & (np.abs((DX.XC - (hx - 2.0)) + (DX.YC - 30.0) * 0.18) < 1.2) & (DX.YC < 40.0)
    sp.fill(grey, BEARD_G)
    sp.fur(bd, dark(BEARD, 0.66), step=2.0, ln=1.8, ang=-1.75, seed=3)
    sp.fur(bd & (DX.YC > hy - 9), mix(BEARD, (255, 210, 150), 0.4), step=3.0, ln=1.2, ang=-1.6, seed=5)
    if beard_items:
        sp.cap(Q(10.0, 30.0), Q(14.6, 37.0), 0.6, 0.6, tones(WOOD))                           # wooden spoon handle
        sp.ell(*Q(15.2, 38.0), 1.4, 1.1, tones(WOOD))
        fl = Q(1.0, 24.0)                                                                       # fishing float on a line
        thin(sp, (fl[0], fl[1] + 4.0), fl, (220, 220, 220), 0.15)
        sp.ell(fl[0], fl[1] - 0.6, 0.9, 1.4, tones((236, 40, 40)), gloss=0.8)
        sp.fill(sp.m_ell(fl[0], fl[1] - 1.4, 0.9, 0.7)[0], WHITE)
        cone = sp.ell(*Q(8.6, 25.6), 1.6, 2.2, tones((150, 96, 52)))                             # pine cone
        for q in range(3): thin(sp, Q(7.2, 24.4 + q * 1.2), Q(10.0, 24.4 + q * 1.2), dark((150, 96, 52), 0.6), 0.16)
    # moustache + mouth
    mx, my = hx + 3.6, hy - 5.0
    mo = max(mouth_, E['mo'])
    if mo > 0.10 or (E.get('teeth') and E['mc'] > 0.5):
        DX.mouth(sp, mx, my, 4.4, E, mouth_, (120, 40, 34), inside=(80, 20, 28), maxh=5)
    else:                                                                               # closed: a thin line under the moustache
        c_ = E['mc']
        stroke(sp, [(mx - 2.2, my + 0.2 + 0.9 * c_), (mx, my - 0.1 - 0.2 * c_), (mx + 2.2, my + 0.2 + 0.9 * c_)], (110, 36, 30), 0.26)
    if chatter and sp.k >= 2:
        sp.fill(sp.m_ell(mx, my - 0.6, 2.2, 0.8)[0], WHITE, keep=True)
        for q in range(-2, 3): thin(sp, (mx + q * 0.9, my - 1.3), (mx + q * 0.9, my + 0.1), (180, 180, 190), 0.1, keep=True)
    ms = sp.union([sp.m_ell(mx - 1.6, my + 1.6, 3.4, 1.4, 0.25), sp.m_ell(mx + 2.4, my + 1.5, 3.0, 1.3, -0.3)], tones(mix(BEARD, BEARD_G, 0.2)))
    sp.fur(ms, dark(BEARD, 0.62), step=1.4, ln=1.0, ang=-2.4, seed=8)
    if frost: sp.frost(sp.m_ell(hx + 2.0, hy + 4.0, 6.0, 1.4)[0] & sp.m, 0.25 * frost, 9)  # frost on the brows
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), nose=(hx + 6.4, hy - 1.2), eyes=(hx + 0.6, hy + 1.3))

    # ---------------------------------------------------------------- ushanka: ONE flap up like a wing, one down
    if not hat_off:
        wing = sp.ell(hx + 8.6, hy + 9.8, 3.8, 2.5, tones(HAT), ang=0.5)                     # far flap sticking up-out like a wing
        sp.fur(wing, dark(HAT, 0.62), step=1.4, ln=0.9, ang=-0.8, seed=13)
        thin(sp, (hx + 11.8, hy + 11.6), (hx + 13.6, hy + 10.0), (220, 210, 190), 0.16)
        crown = sp.sup(hx - 0.2, hy + 9.4, 7.6, 4.0, tones(HAT_L), n=2.4)
        band = sp.union([sp.m_ell(hx + 0.4, hy + 6.7, 8.2, 2.3), sp.m_ell(hx + 6.8, hy + 7.4, 2.4, 2.5)], tones(HAT))
        flap = sp.cap((hx - 5.8, hy + 5.6), (hx - 6.4, hy - 3.6), 2.6, 2.4, tones(HAT))           # near flap hanging down
        thin(sp, (hx - 6.4, hy - 5.8), (hx - 5.6, hy - 9.4), (220, 210, 190), 0.18)             # untied string
        sp.fur(band | flap, dark(HAT, 0.62), step=1.6, ln=1.0, ang=-1.9, seed=11)
        sp.fill(sp.m_super(hx - 1.6, hy + 10.4, 1.6, 0.9, 3.0)[0], TAPE)                          # изолента on the crown
        if frost: sp.frost(band, 0.12 * frost, 12)
    else:
        bald = sp.ell(hx, hy + 6.0, 6.6, 3.6, tones(SKIN), gloss=0.8)
        for q in range(3): thin(sp, (hx - 5.4 + q * 0.4, hy + 3.4 + q * 1.0), (hx - 7.2, hy + 2.6 + q * 1.1), BEARD, 0.3)
    if sweat > 0:
        for i, (x, y) in enumerate(((hx - 3.0, hy + 4.0), (hx + 5.2, hy + 3.0), (hx - 5.0, hy + 0.5))[:int(1 + 2 * sweat)]):
            yy = y - ((t * 4.0 + i * 1.3) % 4.0)
            sp.ell(x, yy, 0.6, 0.9, tones((170, 220, 255)), ol=False, snow=False); sp.dot(x - 0.2, yy + 0.3, WHITE)
    sp.outline(INK, 1)

    # ---------------------------------------------------------------- near arm + red mitten
    before = sp.m.copy()
    shN = Q(11.0, 38.0 + br * 0.3)
    hn = hand_n if hand_n is not None else Q(17.0, 24.0)
    kN, eN = ik(shN, hn, 9.0, 8.4, -1.0)
    sp.cap(shN, kN, 3.5, 3.1, tones(JACKET)); sp.cap(kN, eN, 3.1, 2.7, tones(JACKET))
    for q in (0.35, 0.7):
        a = (shN[0] + (eN[0] - shN[0]) * q, shN[1] + (eN[1] - shN[1]) * q)
        thin(sp, (a[0] - 2.6, a[1] + 1.0), (a[0] + 2.6, a[1] - 1.0), dark(JACKET, 0.62), 0.2)
    if prop_n and getattr(prop_n, 'behind', False): prop_n(sp, eN)
    mit = sp.ell(eN[0] + 0.4, eN[1] - 0.4, 2.7, 2.5, tones(MITT))
    sp.ell(eN[0] + 2.0, eN[1] + 1.4, 1.0, 1.3, tones(MITT))                                       # thumb
    sp.fill(mit & (np.abs(DX.YC - (eN[1] - 0.2)) < 0.35) & DX.CHECK, WHITE)                      # knitted pattern
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
    sp.fur(body, dark(FUR, 0.66), step=2.6, ln=2.2, ang=-1.9, seed=21)
    bel = sp.ell(7.0, 26.0 + breathe * 0.3, 17.0, 18.0 + breathe * 0.4, tones(FUR_L), flat=0.05)
    sp.fur(bel, dark(FUR_L, 0.78), step=3.0, ln=1.6, ang=-1.7, seed=22)
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
    sp.fur(head, dark(FUR, 0.66), step=2.4, ln=1.8, ang=-1.9, seed=23)
    mz = sp.union([sp.m_ell(hx + 8.0, hy - 5.0, 10.0, 7.0)], tones(FUR_L))
    sp.fur(mz, dark(FUR_L, 0.8), step=2.2, ln=1.0, ang=-1.6, seed=24)
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
    """encase a finished sprite in an ice block (applied as Act(post=...)): tint icy, frosty specks, a translucent block with glints"""
    m = sp.m.copy()
    ys, xs = np.nonzero(m)
    if not len(xs): return
    sp.col[m] = (sp.col[m].astype(np.float32) * (1 - 0.45 * k) + np.array((170, 214, 250)) * 0.45 * k).astype(np.uint8)
    y0, y1, x0, x1 = ys.min() - 3 * sp.k, ys.max() + 3 * sp.k, xs.min() - 4 * sp.k, xs.max() + 4 * sp.k
    blk = np.zeros_like(m); blk[max(0, y0):y1, max(0, x0):x1] = True
    rim = blk & ~erode(erode(blk))
    out = blk & ~m
    sp.col[out] = (210, 236, 255)
    sp.col[rim] = (240, 250, 255)
    rr, cc = np.mgrid[0:sp.H, 0:sp.W]
    diag = blk & ((((cc * 0.8 - rr) / sp.k) % 14.0) < 1.0)
    sp.col[diag] = (250, 254, 255)
    sp.m |= blk


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
