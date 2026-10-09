"""«Florida Man: Allegedly» cast in the «Tabloid Sun» manner (props/fmpix.py): FLORIDA MAN, MORT POUCH, ESQ. (pelican lawyer),
DEPUTY DARLENE, TANNER (the face of the system, a new job every episode), the IGUANA, background LOCALS, and the props
(chicken tender sub, invoice, recliner, hand truck, A/C condenser, TV cart, shopping basket).
Coordinates: sprite px, feet anchor at the origin, +x = facing side, y up. Every draw fn takes the Spr first."""
import math
import numpy as np
from props import dibspix as DX
from props import fmpix as FX
from props.fmpix import INK, WHITE, tones, stroke, ht_fill
from props.dibspix import EXPR, ik, dark, mix, erode, dilate

# ---------------------------------------------------------------- palette («postcard from Florida»)
TAN = (200, 126, 74)                # Florida Man: saddle-leather tan
TAN_F = dark(TAN, 0.84)
PEEL = (246, 186, 170)              # sunburn peel on the scalp
DENIM = (74, 116, 176)
CROC = (255, 122, 34)
PACK = (255, 86, 160)               # hot-pink fanny pack
BRAID = (214, 194, 150)
SUBBREAD = (222, 168, 92)
SUBWRAP = (236, 248, 240)
SUBSTRIPE = (40, 176, 150)
TEAL = (40, 196, 196)

XTRA = dict(
    zen=dict(eo=0.8, pu=0.55, bt=-0.15, bl=0.1, mo=0.0, mc=0.35),
    shriek=dict(eo=1.45, pu=0.28, bt=-0.85, bl=1.0, mo=1.0, mc=-0.3),
    weak=dict(eo=0.6, pu=0.6, bt=-0.6, bl=0.2, mo=0.15, mc=-0.5, lid=0.5),
    bliss=dict(eo=0.0, pu=0.6, bt=-0.4, bl=0.5, mo=0.45, mc=0.3, shut=True, round_mouth=True),
    proud=dict(eo=0.9, pu=0.55, bt=0.0, bl=0.2, mo=0.0, mc=0.9, teeth=True),
    bored=dict(eo=0.8, pu=0.55, bt=0.05, bl=0.0, mo=0.0, mc=-0.1, lid=0.42),
    chipper=dict(eo=1.15, pu=0.6, bt=-0.3, bl=0.6, mo=0.0, mc=1.0, teeth=True),
    shiver=dict(eo=1.2, pu=0.5, bt=-0.6, bl=0.6, mo=0.25, mc=0.8, teeth=True),
    frozen=dict(eo=0.0, pu=0.6, bt=-0.2, bl=0.2, mo=0.0, mc=0.45, shut=True),
)


def X(expr):
    return dict(XTRA.get(expr) or EXPR.get(expr, EXPR['normal']))


FONT = dict(DX.FONT3)
FONT.update(N=['1001', '1101', '1011', '1001', '1001'], M=['10001', '11011', '10101', '10001', '10001'],
            W=['10001', '10001', '10101', '11011', '10001'], K=['1001', '1010', '1100', '1010', '1001'])
FONT.update({'*': ['000', '101', '010', '101', '000'], ',': ['000', '000', '000', '010', '100'], '%': ['101', '001', '010', '100', '101'], '#': ['101', '111', '101', '111', '101']})


def txt(sp, s_, i0, j0, c, keep=True):
    """tiny pixel font (3x5, wider N/M/W/K), top-left at (i0, j0); pre-mirrored on flipped sprites; returns the width"""
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


def txt_w(s_):
    return sum(len(FONT.get(ch.upper(), FONT[' '])[0]) + 1 for ch in s_) - 1


FLORIDA = ['XXXXXX..', 'XXXXXXX.', '.....XX.', '....XXX.', '....XXXX', '.....XXX', '.....XXX', '......XX', '......X.']


# ======================================================================================== props
def sub(sp, h, ang=0.0, k=1.0, bite=False):
    """the chicken tender sub: a long roll in mint-striped deli paper, lettuce and a tender poking out; h = the hand holding it"""
    ca, sa = math.cos(ang), math.sin(ang)
    def R(x, y): return (h[0] + (x * ca - y * sa) * k, h[1] + (x * sa + y * ca) * k)
    sp.cap(R(-6.0, 0.4), R(8.5, 0.4), 2.2 * k, 2.2 * k, tones(SUBBREAD), gloss=0.4)
    for q in range(5):                                                         # lettuce frills
        sp.dot(*R(-3.0 + q * 2.4, -1.6), (120, 200, 70))
    sp.dot(*R(7.0, -1.2), (230, 70, 60)); sp.dot(*R(-1.0, -1.8), (230, 70, 60))
    sp.cap(R(8.0, 0.0), R(10.2, 0.2), 1.2 * k, 1.0 * k, tones((214, 150, 70)))   # the tender sticking out
    w = sp.m_cap(R(-6.6, 0.4), R(2.2, 0.4), 2.7 * k, 2.7 * k)[0]               # deli paper over the back half
    sp.paint(w, tones(SUBWRAP), DX.lit(*sp.m_cap(R(-6.6, 0.4), R(2.2, 0.4), 2.7 * k, 2.7 * k)[1:]))
    for q in range(3):
        sp.fill(w & (np.abs((DX.XC - R(-5.0 + q * 2.6, 0)[0]) * ca + (DX.YC - R(-5.0 + q * 2.6, 0)[1]) * sa) < 0.55), SUBSTRIPE)
    if bite: sp.fill(sp.m_ell(*R(10.0, 1.6), 1.6, 1.6)[0], (0, 0, 0)); sp.m &= ~sp.m_ell(*R(10.0, 1.6), 1.6, 1.6)[0]


def invoice(sp, h, amount='$9,000', k=1.0):
    """an A/C repair invoice held up to the camera: COOL-RITE header, the amount in red"""
    x0, y0 = h[0] - 3.0, h[1] - 4.0
    w, hh = 39.0, 18.0
    sp.rect(x0, y0, x0 + w, y0 + hh, (250, 250, 240))
    sp.rect(x0, y0 + hh - 7.0, x0 + w, y0 + hh, (40, 120, 200))
    txt(sp, 'COOL-RITE', x0 + 2, y0 + hh - 1.0, (255, 255, 255))
    txt(sp, 'TOTAL', x0 + 2, y0 + hh - 8.6, (60, 60, 70))
    txt(sp, amount, x0 + w - 2 - txt_w(amount), y0 + 6.4, (226, 30, 40))
    sp.line((x0 + 2, y0 + 7.4), (x0 + w - 2, y0 + 7.4), (226, 30, 40))
    o = sp.m_poly([(x0, y0), (x0 + w, y0), (x0 + w, y0 + hh), (x0, y0 + hh)])
    e = o & ~erode(o); sp.fill(e, INK)
    sp.anchors['invoice'] = (x0 + w / 2, y0 + hh / 2)


def tablet(sp, h, k=1.0, screen=(120, 220, 255)):
    sp.rect(h[0] - 1.0, h[1] - 1.0, h[0] + 8.0, h[1] + 6.0, (40, 44, 52))
    sp.rect(h[0] - 0.2, h[1] - 0.2, h[0] + 7.2, h[1] + 5.2, screen, keep=True)
    sp.rect(h[0] + 0.8, h[1] + 3.0, h[0] + 5.0, h[1] + 3.8, (255, 255, 255), keep=True)


def basket(sp, h):
    """red plastic supermarket basket held by its handle at h"""
    x, y = h
    sp.line((x - 3.0, y - 1.0), (x, y + 1.5), (60, 60, 64)); sp.line((x, y + 1.5), (x + 3.0, y - 1.0), (60, 60, 64))
    m = sp.m_poly([(x - 7.0, y - 1.0), (x + 7.0, y - 1.0), (x + 5.5, y - 8.0), (x - 5.5, y - 8.0)])
    sp.paint(m, tones((220, 40, 50)), np.clip((DX.YC - (y - 8)) / 7.0, 0, 1) * 0.6 + 0.2)
    for q in range(4): sp.fill(m & (np.abs(DX.XC - (x - 4.5 + q * 3.0)) < 0.5) & (DX.YC < y - 2.5) & (DX.YC > y - 7.0), (150, 20, 30))
    sp.rect(x - 4.0, y - 1.0, x + 1.0, y + 2.0, (250, 250, 240)); sp.rect(x + 1.0, y - 1.0, x + 4.5, y + 1.0, (120, 200, 255))   # ice cream


def recliner(sp, t=0.0, foot=1.0, worn=True, col=(112, 132, 70)):
    """a puffy avocado-green vinyl recliner, side view facing +x, footrest out (foot 0..1); seat top y~15, footrest pad top y~13"""
    T = tones(col)
    sp.union([sp.m_super(-1.0, 7.6, 10.4, 7.6, 3.4), sp.m_super(-11.0, 22.0, 4.8, 15.0, 2.6, )], T)      # body + backrest, one volume
    for q in range(3): sp.line((-14.0, 19.0 + q * 5.0), (-9.0, 19.8 + q * 5.0), dark(col, 0.72))         # tufting
    sp.line((-6.0, 15.0), (9.0, 15.0), dark(col, 0.7))                                                  # seat line
    sp.union([sp.m_super(0.0, 18.0, 9.6, 3.0, 3.0), sp.m_ell(9.2, 17.6, 2.8, 3.4)], tones(mix(col, (255, 230, 200), 0.08)))   # armrest scroll
    sp.rect(-11.0, -0.5, 9.0, 1.0, dark(col, 0.45))
    if foot > 0.02:
        a_ = foot
        sp.cap((8.0, 6.0), (8.0 + 6.0 * a_, 9.0 + 0.6 * a_), 1.0, 1.0, tones((60, 60, 64)))            # linkage
        sp.union([sp.m_super(13.0 + 8.0 * a_, 11.0 + 0.6 * a_, 5.6, 2.6, 3.0)], T)                      # footrest pad
    if worn:
        sp.rect(-14.6, 29.0, -10.6, 31.6, (196, 200, 206)); sp.rect(2.0, 18.4, 5.6, 20.6, (196, 200, 206))   # duct tape
        sp.dot(-4.0, 9.0, dark(col, 0.5)); sp.dot(-2.0, 10.4, (240, 220, 180))
    sp.anchors.update(seat=(0.0, 15.0), foot=(13.0 + 8.0 * foot, 13.6))


def hand_truck(sp, t=0.0, spin=0.0):
    """a red two-wheel hand truck seen from the side, leaning back; handles up at x~-10, nose plate at x~6"""
    _wheel(sp, -2.0, 3.6, 3.6, spin)
    sp.cap((-2.0, 4.0), (-14.0, 40.0), 1.0, 1.0, tones((220, 40, 40)))
    sp.cap((4.0, 1.2), (-2.0, 3.0), 0.8, 0.8, tones((180, 180, 186)))
    sp.rect(2.0, 0.4, 8.0, 1.6, (170, 170, 176))
    sp.cap((-14.0, 40.0), (-11.0, 42.0), 1.0, 1.0, tones((40, 40, 44)))
    sp.anchors.update(handle=(-12.5, 41.0))


def _wheel(sp, x, y, r, spin, tyre=(36, 36, 40), rim=(180, 186, 196)):
    sp.ell(x, y, r, r, tones(tyre))
    sp.ell(x, y, r * 0.5, r * 0.5, tones(rim))
    for q in range(3):
        a = spin + q * 2.1
        sp.line((x, y), (x + math.cos(a) * r * 0.45, y + math.sin(a) * r * 0.45), dark(rim, 0.6))


def ac_unit(sp, t=0.0, dead=False, fan=0.0):
    """an outdoor A/C condenser: grey box, louvred sides, fan grille on top, a «COOL-RITE» sticker; the fan dies when dead"""
    G = (176, 182, 184)
    box = sp.m_super(0.0, 12.0, 13.0, 12.0, 4.0)[0]
    sp.paint(box, tones(G), np.clip((DX.YC - 0) / 24, 0, 1) * 0.6 + 0.25 + 0.15 * (DX.XC < -6))
    for q in range(9):                                                            # louvres
        y = 3.0 + q * 2.2
        sp.fill(box & (np.abs(DX.YC - y) < 0.45) & (np.abs(DX.XC) < 11.5), dark(G, 0.62))
    sp.ell(0.0, 24.4, 12.0, 2.4, tones((70, 74, 80)))                              # fan grille top
    a = fan
    for q in range(3):
        aa = a + q * 2.094
        sp.line((0.0, 24.4), (math.cos(aa) * 9.0, 24.4 + math.sin(aa) * 1.8), (40, 42, 46))
    sp.rect(-11.0, 14.0, -2.0, 19.0, (40, 120, 200)); txt(sp, 'COOL', -10.0, 18.0, (255, 255, 255))
    if dead: sp.rect(4.0, 16.0, 10.0, 18.0, (230, 60, 50))                           # red fault light
    sp.rect(-13.0, -0.5, 13.0, 0.5, (90, 90, 96))                                  # concrete pad
    sp.anchors.update(top=(0.0, 26.0))


def tv_cart(sp, t=0.0, on=True):
    """small CRT TV with rabbit ears on a rolling cart"""
    sp.rect(-7.0, 0.0, 7.0, 1.0, (60, 60, 66)); sp.cap((-6.0, 1.0), (-6.0, 12.0), 0.7, 0.7, tones((150, 150, 156)))
    sp.cap((6.0, 1.0), (6.0, 12.0), 0.7, 0.7, tones((150, 150, 156))); sp.rect(-7.0, 12.0, 7.0, 13.0, (90, 90, 96))
    sp.ell(-6.0, 0.5, 1.2, 1.2, tones((30, 30, 34))); sp.ell(6.0, 0.5, 1.2, 1.2, tones((30, 30, 34)))
    box = sp.m_super(0.0, 19.0, 7.5, 6.0, 4.0)[0]; sp.paint(box, tones((70, 60, 50)), np.full(DX.XC.shape, 0.5, np.float32))
    scr = sp.m_super(-0.8, 19.0, 5.2, 4.2, 3.0)[0]
    if on:
        ph = int(t * 8)
        sp.fill(scr, (120, 220, 200) if ph % 2 else (150, 240, 220), keep=True)
        sp.fill(scr & (np.abs(DX.YC - (17.0 + (t * 6) % 5)) < 0.5), (230, 255, 250), keep=True)
    else:
        sp.fill(scr, (30, 40, 40))
    sp.line((1.0, 25.0), (-4.0, 31.0), (170, 170, 176)); sp.line((2.0, 25.0), (7.0, 30.0), (170, 170, 176))


# ======================================================================================== FLORIDA MAN
def fm(sp, t=0.0, expr='zen', mouth_=0.0, look=(0.6, 0.0), blink=None, pose='stand', hand_n=None, hand_f=None, prop_n=None, prop_f=None,
       sweat=0.0, frost=0.0, glasses_drop=0.0, walk=None, sway=0.0, shaka=False, belly_jiggle=0.0, legs=True):
    """FLORIDA MAN — «olive on toothpicks»: a round sun-cured belly on stick legs, tiny bald peeling head, neon shield sunglasses that
    never come off (they slide down when prices hit), a braided goatee down to the belly with a fishing lure on the end, gold tooth,
    toothpick, Florida-map tattoo on the belly, frayed jorts, hot-pink fanny pack, ONE neon-orange croc (the other foot bare).
    pose: 'stand' | 'sit' (in the recliner: hips at the seat, legs out on the footrest) | 'lie' (use rot=90 on the actor)"""
    E = X(expr)
    if blink is None: blink = (t % 4.1) < 0.12
    sit = pose == 'sit'
    hy = 15.0 if sit else 24.0                                   # hip height
    dy = hy - 24.0                                               # upper-body offset
    def Q(x, y): return (x, y + dy)
    br = 0.4 * math.sin(t * 2.0)
    jig = belly_jiggle * math.sin(t * 22.0)

    # ---------------------------------------------------------------- far arm (behind)
    shF = Q(-4.6, 49.0 + br * 0.3)
    hf = hand_f if hand_f is not None else Q(-7.5, 31.5)
    kF, eF = ik(shF, hf, 8.6, 8.2, -1.0)
    sp.cap(shF, kF, 1.9, 1.7, tones(TAN_F)); sp.cap(kF, eF, 1.7, 1.5, tones(TAN_F))
    sp.ell(*eF, 1.9, 1.8, tones(TAN_F))
    if prop_f: prop_f(sp, eF)
    sp.anchors['hand_f'] = eF

    # ---------------------------------------------------------------- legs
    if legs:
        if sit:
            for k_, (dx, c) in enumerate(((-2.0, TAN_F), (2.0, TAN))):
                sp.cap((dx, 16.0), (dx + 13.0, 15.5), 2.2, 1.9, tones(c))
                sp.cap((dx + 13.0, 15.5), (dx + 24.0, 15.0), 1.8, 1.5, tones(c))
                sp.ell(dx + 13.2, 16.2, 2.0, 1.7, tones(c))                                       # knobby knee
            sp.sup(26.5, 17.5, 1.8, 3.6, tones(CROC), n=2.2)                                     # croc sole up
            for q in range(3): sp.dot(27.0, 15.5 + q * 1.4, dark(CROC, 0.55))
            sp.ell(22.6, 17.2, 1.3, 3.0, tones(TAN_F))                                           # bare far foot
            for q in range(4): sp.dot(23.5, 15.0 + q * 1.1, dark(TAN, 0.6))
        else:
            sw = math.sin(walk) * 3.0 if walk is not None else 0.0
            for k_, (dx, c) in enumerate(((-3.2, TAN_F), (4.4, TAN))):
                s_ = sw if k_ else -sw
                sp.cap((dx * 0.9, 21.0), (dx + s_, 3.2), 1.8, 1.4, tones(c))
                sp.ell(dx + s_ * 0.5 + 0.3, 12.0, 1.9, 1.6, tones(c))                              # knobby knees
                if k_ == 1:                                                                       # the ONE croc
                    sp.sup(dx + s_ + 2.4, 1.8, 4.4, 2.0, tones(CROC), n=2.2, gloss=0.5)
                    for q in range(3): sp.dot(dx + s_ + 1.0 + q * 1.6, 3.0, dark(CROC, 0.5))
                    sp.line((dx + s_ - 1.6, 2.6), (dx + s_ - 1.6, 0.8), dark(CROC, 0.7))
                else:                                                                             # bare foot, five toes
                    sp.ell(dx + s_ + 1.8, 1.2, 3.4, 1.3, tones(c))
                    for q in range(4): sp.dot(dx + s_ + 3.0 + q * 0.0 + (q % 2), 0.4 + q * 0.0, dark(TAN, 0.6))
    # ---------------------------------------------------------------- jorts + fanny pack
    sh = sp.union([sp.m_ell(*Q(0.5, 27.5), 9.6, 5.4), sp.m_cap(Q(-3.0, 26.0), Q(-3.2, 20.0) if not sit else (8.0, 16.0), 3.4, 3.0),
                   sp.m_cap(Q(4.0, 26.0), Q(4.6, 20.0) if not sit else (10.0, 16.5), 3.6, 3.2)], tones(DENIM))
    fr = sh & ~erode(sh) & (DX.YC < (20.8 if not sit else 17.6))                                  # frayed hem
    sp.fill(fr & DX.CHECK, (236, 236, 228))
    sp.sup(*Q(10.0, 26.0), 3.6, 2.4, tones(PACK), n=2.4, gloss=0.3)
    sp.line(Q(7.0, 26.4), Q(13.0, 26.4), dark(PACK, 0.5))

    # ---------------------------------------------------------------- belly + chest
    bel = sp.union([sp.m_ell(*Q(3.6 + jig * 0.3, 37.0), 11.6, 10.4), sp.m_ell(*Q(1.5, 47.6), 7.6, 5.0)], tones(TAN), gloss=0.35)
    sp.dot(*Q(9.5, 30.0), dark(TAN, 0.5))                                                          # navel
    for q in range(6): sp.dot(*Q(2.0 + (q * 7) % 6, 45.0 + (q * 3) % 4), dark(TAN, 0.62))         # chest hair
    sp.line(Q(-1.0, 44.4), Q(4.0, 44.0), dark(TAN, 0.72))                                         # pec line
    # tattoo: the state of Florida with a heart on his town
    tx, ty = Q(-1.0, 41.0)
    sp.stamp(FLORIDA, int(tx), int(ty), {'X': (34, 128, 132)})
    sp.dot(int(tx) + 5, int(ty) - 6, (226, 40, 60))
    if sweat > 0:
        for i, (x, y) in enumerate(((10.0, 41.0), (-3.0, 38.0), (6.0, 33.0), (12.0, 36.0), (-5.0, 45.0))[:int(1 + 4 * sweat)]):
            yy = y - ((t * 5.0 + i * 1.7) % 6.0)
            sp.ell(*Q(x, yy), 0.9, 1.3, tones((170, 230, 255)), ol=False); sp.dot(*Q(x - 0.2, yy + 0.6), WHITE)

    # ---------------------------------------------------------------- head
    hx, hyy = Q(4.2, 61.6)
    sp.cap(Q(2.5, 51.0), Q(3.4, 55.0), 2.8, 2.8, tones(TAN))
    sp.ell(hx - 5.4, hyy - 0.4, 1.6, 2.3, tones(TAN))                                             # ear
    face = sp.union([sp.m_ell(hx, hyy, 6.4, 7.4), sp.m_ell(hx + 2.2, hyy - 4.8, 4.8, 3.2)], tones(TAN), gloss=0.5)
    DX.stubble(sp, face & (DX.YC < hyy - 3.4) & ((DX.XC < hx + 0.5) | (DX.YC < hyy - 7.0)), (176, 150, 110), 0.22, 3)
    for q in range(4):                                                                           # sunburn peel on the dome
        sp.dot(hx - 2.4 + q * 1.6, hyy + 5.6 - (q % 2) * 0.6, PEEL)
    lx, ly = look
    Eb = dict(E, bl=E['bl'] * 0.35, bt=E['bt'] * 0.55)
    DX.eye(sp, hx + 2.8, hyy + 0.9, 3.4, 3.2, E, (60, 110, 150), (lx, ly), blink, lash=INK, skin=TAN)
    DX.eye(sp, hx - 1.6, hyy + 0.9, 3.0, 3.0, E, (60, 110, 150), (lx, ly), blink, lash=INK, skin=TAN)
    DX.brow(sp, hx + 3.0, hyy + 3.9, 3.6, Eb, +1, (120, 80, 50), th=1)
    DX.brow(sp, hx - 1.6, hyy + 3.9, 3.0, Eb, -1, (120, 80, 50), th=1)
    # nose (sunburnt tip)
    sp.ell(hx + 6.0, hyy - 2.0, 2.0, 1.8, tones((214, 112, 84)), gloss=1.0)
    # mouth + gold tooth + toothpick
    mx, my = hx + 3.2, hyy - 5.4
    DX.mouth(sp, mx, my, 5.6, E, mouth_, (96, 40, 30), skin=TAN, maxh=6)
    mo = max(mouth_, E['mo'])
    if mo > 0.1 and not E.get('round_mouth'):
        hh = 1.0 + mo * 5 / 2; cyy = my - hh * 0.35 + E['mc'] * 0.6
        sp.dot(mx + 0.6, cyy + hh * 0.5, (255, 206, 60), keep=True)
    elif E['mc'] > 0.2 and E.get('teeth'):
        sp.dot(mx + 0.5, my + 0.4, (255, 206, 60), keep=True)
    if mo < 0.5:
        sp.line((mx + 2.6, my + 0.2), (mx + 5.6, my - 0.9), (226, 196, 140))
    # the shield sunglasses (slide down with sweat / panic)
    gd = -2.4 * glasses_drop
    gl = sp.m_poly([(hx - 5.8, hyy + 2.9 + gd), (hx + 7.6, hyy + 2.7 + gd), (hx + 7.4, hyy - 0.9 + gd), (hx + 4.8, hyy - 0.3 + gd),
                    (hx + 3.8, hyy - 1.1 + gd), (hx - 5.6, hyy - 0.7 + gd)])
    k_ = np.clip((hyy + 2.9 + gd - DX.YC) / 3.8, 0, 1)
    gcol = [(40, 214, 222), (120, 140, 230), (246, 76, 172), (255, 170, 62)]
    for i, c in enumerate(gcol):
        sp.fill(gl & (k_ >= i / 4) & (k_ < (i + 1) / 4 + (0.01 if i == 3 else 0)), c)
    sp.fill(gl & (np.abs((DX.XC - hx) + (DX.YC - hyy - gd) * 1.2 - 0.5) < 0.6), GLX)
    sp.fill(gl & ~erode(gl), INK)
    sp.anchors.update(head=(hx, hyy), mouth=(mx, my), eyes=(hx + 1.0, hyy + 0.6 + gd), glasses=(hx + 1.0, hyy + 1.0 + gd))

    # ---------------------------------------------------------------- the braided goatee with a fishing lure
    pts = [(mx + 0.2, my - 1.8), (mx + 0.9, my - 5.6), (mx + 1.8, my - 9.6), (mx + 2.6, my - 13.6), (mx + 3.0, my - 17.4), (mx + 3.2, my - 20.6)]
    pts = [(x + sway * (i / 5.0) ** 1.5 * 3.0, y) for i, (x, y) in enumerate(pts)]
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        for q in range(3):
            u = (q + 0.5) / 3
            c = BRAID if (i * 3 + q) % 2 else dark(BRAID, 0.74)
            sp.ell(a[0] + (b[0] - a[0]) * u + (0.35 if (i * 3 + q) % 2 else -0.35), a[1] + (b[1] - a[1]) * u, 1.6, 1.05, tones(c),
                   olc=dark(BRAID, 0.5))
    sp.rect(pts[-2][0] - 1.4, pts[-2][1] - 0.4, pts[-2][0] + 1.6, pts[-2][1] + 0.6, (255, 86, 160))               # pink hair tie
    lx_, ly_ = pts[-1]
    sp.ell(lx_, ly_ - 2.2, 0.9, 1.9, tones((236, 60, 50)), gloss=0.6)                                # the lure
    sp.dot(lx_, ly_ - 1.0, WHITE); sp.dot(lx_ - 0.4, ly_ - 2.0, (20, 20, 20))
    sp.line((lx_, ly_ - 4.2), (lx_ + 0.8, ly_ - 5.2), (196, 200, 210)); sp.line((lx_ + 0.8, ly_ - 5.2), (lx_ + 1.4, ly_ - 4.4), (196, 200, 210))
    sp.anchors['lure'] = (lx_, ly_ - 4.0)
    sp.outline(INK, 1)

    # ---------------------------------------------------------------- near arm (in front)
    before = sp.m.copy()
    shN = Q(6.6, 49.0 + br * 0.3)
    hn = hand_n if hand_n is not None else Q(15.6, 30.5)
    if shaka: hn = Q(16.0, 62.0)
    kN, eN = ik(shN, hn, 8.6, 8.2, -1.0)
    sp.cap(shN, kN, 2.0, 1.8, tones(TAN)); sp.cap(kN, eN, 1.8, 1.6, tones(TAN))
    sp.ell(*eN, 2.0, 1.9, tones(TAN))
    if shaka:                                                                                    # hang loose: thumb up-out, pinky down-out
        sp.cap((eN[0] + 0.6, eN[1] + 1.0), (eN[0] + 2.6, eN[1] + 3.6), 0.8, 0.7, tones(TAN))
        sp.cap((eN[0] + 0.6, eN[1] - 1.0), (eN[0] + 2.8, eN[1] - 3.2), 0.8, 0.7, tones(TAN))
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o
    if frost > 0: frost_over(sp, frost, t)


GLX = (255, 255, 250)


def frost_over(sp, k, t=0.0):
    """frost on everything facing up + icicles hanging from the lowest edges (freezer aisle)"""
    m = sp.m
    top = m & ~np.roll(m, sp.k, 0)                                 # canvas rows go down: the pixel above is empty
    fr = top.copy()
    for _ in range(max(1, int(round(2 * k * sp.k)))): fr |= np.roll(fr, 1, 0) & m
    sp.col[fr] = (226, 244, 255)
    sp.col[m & (FX.halftone() < -0.46 + 0.07 * k) & ~sp.keep] = (236, 248, 255)
    if k > 0.5:                                                    # icicles under the lowest rim pixels (every few columns)
        bot = m & ~np.roll(m, -sp.k, 0)
        ys, xs = np.nonzero(bot)
        for y, x in zip(ys[::7], xs[::7]):
            n = int((2 + (x * 7 % 3)) * sp.k * k)
            y1 = min(sp.H, y + 1 + n)
            sp.col[y + 1:y1, x] = (200, 236, 255); sp.m[y + 1:y1, x] = True


# ======================================================================================== MORT POUCH, ESQ. (pelican lawyer)
FEATH = (140, 130, 118)            # grey-brown body
NECK = (120, 70, 44)               # chestnut neck
HEADW = (248, 246, 236)
CROWN = (246, 214, 110)
BILL = (248, 214, 118)
POUCH = (88, 82, 66)
TIE = (210, 40, 56)


def mort(sp, t=0.0, expr='deadpan', mouth_=0.0, look=(0.8, 0.0), blink=None, lump=None, gulp=0.0, glasses=True, perch=True, cam=False,
         lift=0.0):
    """MORT POUCH, ESQ. — «ladle»: a perched brown pelican in the classic pose (long bill resting down along the chest), white head
    with a yellow comb-over, half-moon reading glasses on the bill, red tie with an ESQ. pin under the pouch.
    The olive pouch hangs under the bill and shows what he swallowed (lump='sub' / 'cash'); gulp 0..1 = swallowing now (the lump
    slides down the neck); lift 0..1 raises the bill towards the camera (when he talks, it lifts a bit by itself)."""
    E = X(expr)
    if blink is None: blink = (t % 3.7) < 0.12
    br = 0.35 * math.sin(t * 2.0)
    mo = max(mouth_, E['mo'])
    # feet gripping the perch
    for dx in (-2.4, 2.4):
        sp.cap((dx, 5.0), (dx + 0.4, 1.2), 1.0, 0.9, tones((60, 60, 64)))
        sp.sup(dx + 1.6, 0.8, 3.0, 1.0, tones((76, 74, 72)), n=2.0)
    # body: an upright oval, the folded wing with pale-edged scallops, tail tip down-left
    sp.union([sp.m_ell(-1.0, 13.0, 7.6, 10.4, 0.18), sp.m_ell(-7.0, 4.4, 3.4, 2.2, 0.8)], tones(FEATH))
    wing = sp.m_ell(-2.6, 12.0, 6.0, 8.8, 0.25)
    sp.paint(wing[0], tones(dark(FEATH, 0.86)), DX.lit(wing[1], wing[2]))
    for q in range(4):
        y = 6.0 + q * 3.0
        sp.fill(wing[0] & (np.abs(DX.YC - y - 0.5 * (DX.XC + 2.6)) < 0.5) & (DX.XC < -2.0 + q), mix(dark(FEATH, 0.86), (230, 222, 206), 0.45))
    # neck: thick chestnut column, a white stripe at the back
    sp.cap((1.4, 20.0 + br * 0.2), (3.0, 30.0), 3.6, 3.0, tones(NECK))
    sp.cap((-0.8, 21.0), (1.2, 31.0), 1.2, 1.2, tones(HEADW), ol=False)
    if gulp > 0:                                                                                 # the lump slides down the neck
        gy = 30.0 - 9.0 * gulp
        sp.ell(2.6, gy, 3.6, 2.2, tones(dark(NECK, 0.9)))
    # tie under the pouch, ESQ. pin
    tk = (4.6, 22.4)
    sp.ell(*tk, 1.4, 1.2, tones(TIE))
    sp.fill(sp.m_poly([(tk[0] - 1.0, tk[1] - 0.8), (tk[0] + 1.2, tk[1] - 0.8), (tk[0] + 2.0, tk[1] - 9.0), (tk[0] + 0.6, tk[1] - 10.4),
                       (tk[0] - 0.6, tk[1] - 8.6)]), TIE)
    for q in range(3): sp.line((tk[0] - 0.4, tk[1] - 3.0 - q * 2.4), (tk[0] + 1.4, tk[1] - 2.0 - q * 2.4), (150, 20, 40))
    sp.dot(tk[0] + 0.6, tk[1] - 5.2, (255, 214, 70), keep=True)
    # head
    hx, hy = 4.4, 35.6
    sp.union([sp.m_ell(hx, hy, 5.6, 4.8), sp.m_ell(hx - 1.8, hy - 3.0, 3.4, 3.0)], tones(HEADW), gloss=0.4)
    sp.fill(sp.m_ell(hx - 0.4, hy + 3.4, 4.6, 1.8)[0] & (DX.YC > hy + 2.4), CROWN)                     # yellow crown
    for q in range(4):                                                                           # the yellow comb-over
        sp.line((hx - 4.0 + q * 1.2, hy + 2.6 - 0.1 * q), (hx + 1.4 + q * 0.9, hy + 4.2 - 0.25 * q), CROWN if q % 2 else dark(CROWN, 0.82))
    # bill: resting down along the chest (a = -0.95 rad), lifting when he talks
    ang = -0.95 + 0.30 * min(1.0, mo * 1.6) + 0.75 * lift
    B = (hx + 3.0, hy - 0.2)
    L = 18.0
    T = (B[0] + L * math.cos(ang), B[1] + L * math.sin(ang))
    open_ = 0.30 * mo
    la = ang - open_
    B2 = (B[0] - 0.4, B[1] - 1.4)
    T2 = (B2[0] + (L - 1.0) * math.cos(la), B2[1] + (L - 1.0) * math.sin(la))
    # pouch: hangs from the lower mandible towards the chest (sags more when full)
    sag = 3.4 + (2.4 if lump else 0.0)
    nx, ny = math.sin(la), -math.cos(la)                                                         # «down» side of the lower mandible
    if nx > 0: nx, ny = -nx, -ny
    pts = [B2]
    for q in range(1, 9):
        u = q / 8
        x = B2[0] + (T2[0] - B2[0]) * u; y = B2[1] + (T2[1] - B2[1]) * u
        d = sag * math.sin(math.pi * min(1.0, u * 1.1)) ** 0.8
        pts.append((x + nx * d, y + ny * d))
    pts.append(T2)
    pm = sp.m_poly(pts + [(B2[0] + (T2[0] - B2[0]) * 0.9, B2[1] + (T2[1] - B2[1]) * 0.9)])
    sp.paint(pm, tones(POUCH), np.clip(0.75 - np.abs(DX.XC - B2[0]) * 0.02, 0, 1))
    if lump:
        c = ((B2[0] + T2[0]) / 2 + nx * sag * 0.45, (B2[1] + T2[1]) / 2 + ny * sag * 0.45)
        lm = sp.m_cap((c[0] - 3.4 * math.cos(la), c[1] - 3.4 * math.sin(la)), (c[0] + 3.4 * math.cos(la), c[1] + 3.4 * math.sin(la)), 1.5, 1.5)[0] & pm
        sp.fill(lm, mix(POUCH, SUBBREAD, 0.35)); sp.fill(lm & ~erode(lm), dark(POUCH, 0.6))
    sp.cap(B2, T2, 0.9, 0.6, tones(dark(BILL, 0.86)))                                                 # lower mandible
    up = sp.m_cap(B, T, 1.8, 0.9)
    sp.paint(up[0], tones(BILL), DX.lit(up[1], up[2]), gloss=0.6)
    sp.line((B[0] + 1.0, B[1] + 0.4), (T[0] - 0.6, T[1] + 0.6), dark(BILL, 0.72))                      # culmen ridge
    sp.ell(T[0] + 0.2, T[1] - 0.4, 1.1, 1.3, tones((236, 110, 56)))                                  # hooked orange tip
    # eye: pale, heavy-lidded, with a feather brow
    ex, ey = hx + 1.4, hy + 0.8
    DX.eye(sp, ex, ey, 3.0, 2.8, E, (230, 214, 140), look, blink, lash=INK, skin=HEADW, white=(252, 252, 246))
    DX.brow(sp, ex + 0.2, ey + 2.6, 3.4, E, +1, (214, 206, 186), th=1)
    if glasses:                                                                                     # round reading glasses on the bill base
        for (gx, gy, r) in ((ex + 2.6, ey - 0.6, 1.6), (ex + 5.4, ey - 1.6, 1.3)):
            ring = sp.m_ell(gx, gy, r, r)[0]
            sp.fill(ring & ~erode(ring), (226, 186, 60)); sp.fill(erode(ring) & (DX.XC < gx) & (DX.YC > gy), (220, 240, 250))
        sp.line((ex + 4.2, ey - 1.0), (ex + 4.2, ey - 1.0), (226, 186, 60))
    sp.anchors.update(head=(hx, hy), eyes=(ex, ey), mouth=((B[0] + T[0]) / 2, (B[1] + T[1]) / 2), tip=T, pouch=pts[4])
    sp.outline(INK, 1)


def FX_dots(d):
    return FX.halftone() < d - 0.5


# ======================================================================================== DEPUTY DARLENE
DSKIN = (240, 190, 160)
SHIRT = (214, 190, 140)            # tan uniform shirt
TROUS = (56, 92, 64)               # sheriff green trousers
HAIR = (246, 214, 120)             # teased platinum-brass blonde
HAT = (186, 156, 98)


def darlene(sp, t=0.0, expr='bored', mouth_=0.0, look=(0.7, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
            gum=0.0, chew=True, walk=None, aviators=False):
    """DEPUTY DARLENE — «mushroom»: a giant teased blonde cloud under a campaign hat on a boxy tan-and-green uniform; aviators low on
    the nose so heavy bored lids hang over them; pink lips chewing gum (gum 0..1 = the bubble), gold star, shoulder radio, duty belt"""
    E = X(expr)
    if blink is None: blink = (t % 4.4) < 0.12
    br = 0.4 * math.sin(t * 1.8)
    ch = (0.25 + 0.25 * math.sin(t * 9.0)) if chew else 0.0
    sw = math.sin(walk) * 2.6 if walk is not None else 0.0
    # far arm
    shF = (-6.0, 47.0)
    hf = hand_f if hand_f is not None else (-8.5, 30.0)
    kF, eF = ik(shF, hf, 8.2, 8.0, -1.0)
    sp.cap(shF, (shF[0] + (kF[0] - shF[0]) * 0.45, shF[1] + (kF[1] - shF[1]) * 0.45), 2.6, 2.6, tones(dark(SHIRT, 0.86)))
    sp.cap((shF[0] + (kF[0] - shF[0]) * 0.4, shF[1] + (kF[1] - shF[1]) * 0.4), kF, 2.0, 1.9, tones(dark((236, 150, 130), 0.86)))
    sp.cap(kF, eF, 1.9, 1.6, tones(dark((236, 150, 130), 0.86))); sp.ell(*eF, 2.0, 1.9, tones(dark(DSKIN, 0.86)))
    if prop_f: prop_f(sp, eF)
    # legs + boots
    for k_, dx in enumerate((-3.6, 4.0)):
        s_ = sw if k_ else -sw
        c = TROUS if k_ else dark(TROUS, 0.85)
        sp.cap((dx * 0.9, 26.0), (dx + s_, 4.0), 3.4, 3.0, tones(c))
        sp.line((dx + 2.0, 24.0), (dx + s_ + 2.4, 5.0), (196, 170, 90))                       # trouser stripe
        sp.sup(dx + s_ + 1.2, 2.2, 4.4, 2.4, tones((30, 28, 30)), n=2.4, gloss=0.6)
    # boxy torso + duty belt + badge + radio
    tor = sp.union([sp.m_super(0.0, 37.0 + br * 0.2, 10.0, 11.0, 3.2)], tones(SHIRT))
    sp.rect(-10.0, 26.0, 10.6, 29.0, (30, 30, 32))
    sp.rect(-1.0, 26.4, 1.6, 28.6, (200, 180, 90))                                              # buckle
    sp.sup(7.6, 26.6, 2.0, 2.6, tones((40, 40, 44)), n=2.6); sp.sup(-7.0, 26.6, 2.4, 2.4, tones((40, 40, 44)), n=2.6)  # pouches
    sp.line((0.6, 47.0), (0.6, 29.0), dark(SHIRT, 0.7))                                         # placket
    for q in range(4): sp.dot(1.4, 45.0 - q * 4.5, (240, 236, 220))
    sp.rect(2.6, 40.0, 7.6, 45.0, dark(SHIRT, 0.86)); sp.line((2.6, 45.0), (7.6, 45.0), dark(SHIRT, 0.6))    # pocket flap
    star = [(4.6, 44.4), (5.3, 42.9), (6.9, 42.8), (5.7, 41.8), (6.2, 40.2), (4.6, 41.2), (3.0, 40.2), (3.5, 41.8), (2.3, 42.8), (3.9, 42.9)]
    sp.fill(sp.m_poly(star), (255, 206, 70)); sp.dot(4.6, 42.4, (255, 250, 200), keep=True)
    sp.rect(-7.0, 41.0, -2.0, 42.4, (30, 30, 34)); sp.rect(-6.4, 41.4, -2.6, 42.0, (230, 230, 220))      # name plate
    sp.sup(-6.0, 48.0, 2.0, 2.6, tones((40, 40, 44)), n=2.4); sp.line((-6.0, 50.0), (-6.4, 53.0), (40, 40, 44))  # shoulder radio
    if not aviators:                                                                            # aviators hooked on the placket
        for cx_ in (0.0, 2.6):
            lm = sp.m_ell(cx_, 44.4, 1.3, 1.0)[0]; sp.fill(lm, (40, 56, 76)); sp.fill(lm & ~erode(lm), (214, 176, 60))
    # head
    hx, hy = 3.6, 60.0
    sp.cap((2.6, 49.0), (3.0, 53.0), 3.0, 3.0, tones(DSKIN))
    # the hair cloud (behind the face)
    hair = sp.union([sp.m_ell(hx - 1.8, hy + 4.0, 10.6, 8.6), sp.m_ell(hx - 8.4, hy - 1.0, 5.4, 7.0), sp.m_ell(hx + 6.4, hy + 3.0, 5.2, 5.4),
                     sp.m_ell(hx - 6.0, hy - 6.0, 4.2, 3.4)], tones(HAIR), gloss=0.5)
    for q in range(7): sp.dot(hx - 9.0 + q * 2.6, hy + 9.0 - (q % 3), dark(HAIR, 0.7))            # curl texture
    for q in range(5): sp.dot(hx - 11.0 + (q % 2), hy - 1.0 - q * 1.6, dark(HAIR, 0.66))
    face = sp.union([sp.m_ell(hx + 0.8, hy, 6.0, 6.6), sp.m_ell(hx + 2.2, hy - 4.4, 4.6, 3.2)], tones(DSKIN), gloss=0.5)
    DX.blush(sp, hx + 4.6, hy - 2.0, 1.6, 1.0, (236, 120, 120))
    lx, ly = look
    DX.eye(sp, hx + 3.6, hy + 1.6, 3.4, 3.0, E, (90, 120, 80), (lx, ly), blink, lash=INK, skin=DSKIN)
    DX.eye(sp, hx - 0.6, hy + 1.6, 3.0, 2.8, E, (90, 120, 80), (lx, ly), blink, lash=INK, skin=DSKIN)
    DX.brow(sp, hx + 3.8, hy + 4.6, 3.6, E, +1, (150, 100, 60), th=1, arch=1.4)
    DX.brow(sp, hx - 0.6, hy + 4.6, 3.0, E, -1, (150, 100, 60), th=1, arch=1.4)
    sp.ell(hx + 6.4, hy - 1.0, 1.6, 1.6, tones(DSKIN))                                          # nose
    if aviators:                                                                                # aviators LOW on the nose
        for cx_, w in ((hx + 3.9, 2.1), (hx - 0.4, 1.8)):
            lm = sp.m_ell(cx_, hy - 1.3, w, 1.4)[0]
            sp.fill(lm, (40, 56, 76)); sp.fill(lm & (DX.YC > hy - 1.0) & (DX.XC < cx_), (150, 210, 236)); sp.fill(lm & ~erode(lm), (214, 176, 60))
        sp.line((hx + 1.4, hy - 0.4), (hx + 1.8, hy - 0.4), (200, 170, 70))
    mo = min(0.7, max(mouth_ * 0.8, E['mo'], ch * 0.35))
    DX.mouth(sp, hx + 3.6, hy - 4.4, 3.8, E, mo, (200, 60, 100), skin=DSKIN, maxh=3)
    if gum > 0.02:                                                                              # the gum bubble
        r = 0.8 + 3.6 * gum
        sp.ell(hx + 5.6 + r * 0.6, hy - 4.4, r, r, tones((255, 140, 190)), gloss=0.8)
    # the campaign hat on top of the hair
    sp.union([sp.m_ell(hx - 0.6, hy + 12.4, 14.6, 1.8)], tones(HAT))
    crown = sp.union([sp.m_super(hx - 0.6, hy + 16.6, 6.0, 4.4, 2.6)], tones(HAT))
    sp.fill(crown & (DX.YC < hy + 14.0) & (DX.YC > hy + 12.8), (60, 44, 30))                     # band
    sp.line((hx - 0.6, hy + 20.6), (hx - 0.6, hy + 17.6), dark(HAT, 0.6))                         # the pinch
    sp.anchors.update(head=(hx, hy), mouth=(hx + 3.6, hy - 4.4))
    sp.outline(INK, 1)
    # near arm
    before = sp.m.copy()
    shN = (7.6, 47.0)
    hn = hand_n if hand_n is not None else (11.0, 30.0)
    kN, eN = ik(shN, hn, 8.2, 8.0, -1.0)
    sp.cap(shN, (shN[0] + (kN[0] - shN[0]) * 0.45, shN[1] + (kN[1] - shN[1]) * 0.45), 2.7, 2.7, tones(SHIRT))
    sp.cap((shN[0] + (kN[0] - shN[0]) * 0.4, shN[1] + (kN[1] - shN[1]) * 0.4), kN, 2.1, 2.0, tones((236, 150, 130)))   # sunburnt forearm
    sp.cap(kN, eN, 2.0, 1.7, tones((236, 150, 130))); sp.ell(*eN, 2.1, 2.0, tones(DSKIN))
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


# ======================================================================================== TANNER
TSKIN = (238, 196, 166)
POLO = (34, 56, 112)
KHAKI = (196, 176, 126)
HAIRB = (110, 72, 40)
TIPS = (250, 230, 150)
JOBS = [('COOL-RITE', (40, 120, 200)), ('PUBBIX', (40, 176, 150)), ('HOSPITAL', (230, 230, 240)), ('DR PAWS', (255, 140, 60)),
        ('SUNSURE', (255, 206, 70)), ('MGMT', (150, 110, 200)), ('FWC', (90, 160, 80)), ('JAIL', (200, 60, 60))]


def tanner(sp, t=0.0, expr='chipper', mouth_=0.0, look=(0.7, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
           thumbs=False, jobs=1, uniform='ac', walk=None, frost=0.0, shiver=0.0, sweat=0.0):
    """TANNER — «lit match»: tall and thin, spiky frosted tips, a megawatt grin, Bluetooth earpiece, a lanyard with one badge per job.
    uniform 'ac' = navy COOL-RITE work polo + khakis (E01)"""
    E = X(expr)
    if blink is None: blink = (t % 3.3) < 0.11
    shv = shiver * math.sin(t * 60.0) * 0.6
    sw = math.sin(walk) * 2.6 if walk is not None else 0.0
    shF = (-4.0 + shv, 52.0)
    hf = hand_f if hand_f is not None else (-6.0, 33.0)
    kF, eF = ik(shF, hf, 9.4, 9.0, -1.0)
    sp.cap(shF, kF, 1.9, 1.7, tones(dark(POLO, 0.86))); sp.cap(kF, eF, 1.6, 1.4, tones(dark(TSKIN, 0.86)))
    sp.ell(*eF, 1.8, 1.7, tones(dark(TSKIN, 0.86)))
    if prop_f: prop_f(sp, eF)
    for k_, dx in enumerate((-2.6, 3.0)):                                                      # long thin legs, white sneakers
        s_ = sw if k_ else -sw
        c = KHAKI if k_ else dark(KHAKI, 0.86)
        sp.cap((dx * 0.9, 31.0), (dx + s_, 4.0), 2.6, 2.2, tones(c))
        sp.sup(dx + s_ + 1.6, 2.0, 4.0, 2.0, tones((246, 246, 246)), n=2.2)
        sp.line((dx + s_ - 0.6, 1.0), (dx + s_ + 4.4, 1.0), (200, 60, 60))
    tor = sp.union([sp.m_super(0.4 + shv, 42.0, 6.6, 11.0, 2.6)], tones(POLO))
    sp.rect(-6.0, 30.0, 7.0, 32.0, (60, 46, 30))                                               # belt
    sp.rect(2.0 + shv, 44.0, 6.4 + shv, 47.0, (240, 240, 240)); txt(sp, 'T', 3.4 + shv, 46.6, (34, 56, 112))   # name patch
    # lanyard + badges
    sp.line((-1.0 + shv, 52.0), (1.6 + shv, 41.0), (40, 176, 150)); sp.line((4.0 + shv, 52.0), (1.6 + shv, 41.0), (40, 176, 150))
    for q in range(max(1, jobs)):
        name, c = JOBS[q % len(JOBS)]
        y = 40.0 - q * 2.4
        sp.rect(0.0 + shv + (q % 2) * 0.6, y - 2.6, 3.6 + shv + (q % 2) * 0.6, y, c); sp.dot(1.0 + shv + (q % 2) * 0.6, y - 1.0, (255, 255, 255))
    # head
    hx, hy = 3.0 + shv, 64.0
    sp.cap((2.0 + shv, 53.0), (2.6 + shv, 57.0), 2.4, 2.4, tones(TSKIN))
    sp.ell(hx - 4.8, hy - 0.4, 1.4, 2.2, tones(TSKIN))
    sp.ell(hx - 5.4, hy - 1.0, 1.0, 1.4, tones((200, 206, 214)), gloss=1.0)                       # earpiece
    face = sp.union([sp.m_ell(hx, hy, 5.6, 7.0), sp.m_ell(hx + 1.6, hy - 5.0, 4.2, 2.8)], tones(TSKIN), gloss=0.5)
    lx, ly = look
    DX.eye(sp, hx + 2.6, hy + 1.2, 3.4, 3.4, E, (60, 140, 220), (lx, ly), blink, lash=INK, skin=TSKIN)
    DX.eye(sp, hx - 1.4, hy + 1.2, 3.0, 3.2, E, (60, 140, 220), (lx, ly), blink, lash=INK, skin=TSKIN)
    DX.brow(sp, hx + 2.8, hy + 4.4, 3.4, E, +1, HAIRB, th=1)
    DX.brow(sp, hx - 1.4, hy + 4.4, 2.8, E, -1, HAIRB, th=1)
    sp.ell(hx + 5.4, hy - 1.2, 1.4, 1.6, tones(TSKIN))
    if E.get('teeth') and mouth_ < 0.15 and E['mo'] < 0.2:                         # the megawatt grin: one clean row of teeth
        mx_, my_ = hx + 2.8, hy - 4.6
        gm = sp.m_super(mx_, my_ - 0.2, 3.4, 1.5, 2.4)[0] & (DX.YC < my_ + 0.6 + 0.12 * (DX.XC - mx_) ** 2)
        sp.fill(gm, (252, 252, 248), keep=True); sp.fill(gm & (np.abs(DX.YC - (my_ - 0.4)) < 0.25 * sp.k / max(1, sp.k)), (214, 214, 220), keep=True)
        sp.fill(gm & ~erode(gm), (170, 70, 70))
    else:
        DX.mouth(sp, hx + 2.8, hy - 4.6, 5.4, E, mouth_, (180, 80, 80), skin=TSKIN, maxh=5)
    # spiky frosted tips: one hair mass (skull cap + spikes), dark roots, blond tips
    # gelled frosted tips: a skull-hugging cap + short spikes radiating out of it (dark roots, blond tips)
    hm = sp.m_ell(hx - 0.3, hy + 0.6, 6.5, 7.8)[0] & (DX.YC > hy + 4.2 + 0.25 * np.clip(DX.XC - hx, 0, 9)) & ~sp.m_ell(hx + 0.4, hy - 0.4, 5.6, 7.0)[0]
    hm |= sp.m_ell(hx - 0.3, hy + 0.6, 6.5, 7.8)[0] & (DX.YC > hy + 5.6)
    for q in range(9):
        a = math.radians(20 + q * 18)
        bx, by_ = hx - 0.3 + 6.0 * math.cos(a), hy + 0.6 + 7.2 * math.sin(a)
        L = 3.2 + 1.2 * ((q * 5) % 3) / 2
        tx_, ty_ = bx + L * math.cos(a + 0.25), by_ + L * math.sin(a + 0.25)
        px_, py_ = -math.sin(a) * 1.3, math.cos(a) * 1.3
        hm |= sp.m_poly([(bx - px_, by_ - py_), (bx + px_, by_ + py_), (tx_, ty_)])
    sp.paint(hm, tones(HAIRB), np.clip((DX.YC - hy - 3.0) / 9.0, 0, 1) * 0.5 + 0.3, gloss=0.3)
    dist = np.sqrt(((DX.XC - hx + 0.3) / 6.5) ** 2 + ((DX.YC - hy - 0.6) / 7.8) ** 2)
    sp.fill(hm & (dist > 1.12) & ~(hm & ~erode(hm)), TIPS)
    sp.fill(hm & (dist > 1.02) & (dist <= 1.12) & DX.CHECK, TIPS)
    if sweat > 0:
        for i, (x, y) in enumerate(((hx + 0.6, hy + 5.4), (hx - 4.4, hy + 2.6), (hx + 3.6, hy + 5.0))[:int(1 + 2 * sweat)]):
            yy = y - ((t * 4.0 + i * 1.3) % 4.0)
            sp.ell(x, yy, 0.8, 1.2, tones((170, 230, 255)), ol=False); sp.dot(x, yy + 0.5, WHITE)
        sp.fill(sp.m_ell(hx - 1.0, 49.0, 3.0, 2.0)[0] & tor, dark(POLO, 0.7))              # sweat patch
    sp.anchors.update(head=(hx, hy), mouth=(hx + 2.8, hy - 4.6))
    sp.outline(INK, 1)
    before = sp.m.copy()
    shN = (6.0 + shv, 52.0)
    hn = hand_n if hand_n is not None else ((10.0, 58.0) if thumbs else (8.4, 33.0))
    kN, eN = ik(shN, hn, 9.4, 9.0, -1.0)
    sp.cap(shN, kN, 2.0, 1.8, tones(POLO)); sp.cap(kN, eN, 1.7, 1.5, tones(TSKIN))
    if thumbs:                                                                       # a clear THUMBS-UP: horizontal fist, thumb up on its back edge
        fx_, fy = eN[0] + 1.2, eN[1] + 0.4
        sp.sup(fx_, fy, 2.8, 2.1, tones(TSKIN), n=2.4)
        for q in range(3): sp.line((fx_ + 0.2 + q * 0.0, fy + 1.2 - q * 1.1), (fx_ + 2.4, fy + 1.2 - q * 1.1), dark(TSKIN, 0.7))
        sp.cap((fx_ - 1.6, fy + 1.4), (fx_ - 1.9, fy + 4.8), 1.15, 1.0, tones(TSKIN))
        sp.dot(fx_ - 1.8, fy + 5.0, (250, 220, 210))
    else:
        sp.ell(*eN, 1.9, 1.8, tones(TSKIN))
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o
    if frost > 0: frost_over(sp, frost, t)


# ======================================================================================== IGUANA
IGG = (110, 170, 74)


def iguana(sp, t=0.0, stiff=False, blink=None, look=(1.0, 0.0), pant=0.0):
    """a green iguana, side view facing +x: crest spikes, dewlap, banded tail; stiff=True = cold-stunned (legs straight out, eyes shut)"""
    if blink is None: blink = (t % 2.9) < 0.15
    tail = [(-6.0, 3.0), (-12.0, 2.0), (-18.0, 2.6), (-23.0, 1.6)]
    for i, (a, b) in enumerate(zip([(-2.0, 3.4)] + tail[:-1], tail)):
        sp.cap(a, b, 2.0 - i * 0.45, 1.6 - i * 0.4, tones(IGG if i % 2 == 0 else (80, 120, 60)))
    body = sp.union([sp.m_ell(1.0, 4.0, 7.0, 3.0), sp.m_ell(8.6, 5.6, 3.6, 2.6, -0.2)], tones(IGG))
    sp.ell(7.6, 3.0, 1.8, 2.0, tones((180, 200, 120)))                                          # dewlap
    for q in range(6):                                                                         # crest
        x = -3.0 + q * 2.0
        sp.line((x, 6.4 + 0.3 * q), (x + 0.6, 8.0 + 0.3 * q), (200, 220, 110))
    for (x, ang) in ((-2.0, -1), (5.0, 1)):                                                    # legs
        if stiff:
            sp.line((x, 2.0), (x + ang * 2.0, 4.0 + 2.6), (80, 120, 60)); sp.line((x, 2.0), (x - ang * 0.5, -0.4), (80, 120, 60))
        else:
            sp.line((x, 2.0), (x + 1.4, -0.2), (80, 120, 60)); sp.line((x + 1.4, -0.2), (x + 2.6, -0.2), (80, 120, 60))
    if stiff or blink:
        sp.line((9.0, 6.6), (10.6, 6.6), INK)
    else:
        sp.dot(9.6, 6.4, (255, 220, 60)); sp.dot(10.0, 6.4, INK)
    if pant > 0 and int(t * 6) % 2: sp.dot(12.0, 4.4, (230, 80, 90))
    sp.anchors.update(head=(9.0, 6.0))
    sp.outline(INK, 1)


# ======================================================================================== LOCALS (background Floridians)
LOCALS = dict(
    retiree=dict(skin=(236, 190, 160), shirt=(80, 190, 200), shorts=(230, 226, 200), hair='visor', hairc=(250, 250, 250)),
    curlers=dict(skin=(214, 160, 128), shirt=(250, 140, 180), shorts=(250, 140, 180), hair='curlers', hairc=(150, 90, 60)),
    tank=dict(skin=(150, 100, 70), shirt=(250, 250, 244), shorts=(230, 120, 40), hair='cap', hairc=(40, 40, 44)),
    grandpa=dict(skin=(240, 200, 170), shirt=(250, 250, 244), shorts=(70, 110, 170), hair='bald', hairc=(240, 240, 240)),
)


def local(sp, t=0.0, kind='retiree', pose='sit', expr='content', mouth_=0.0, look=(0.6, 0.0), blink=None, frost=0.0, prop=None):
    """a background Floridian living in the freezer aisle; pose 'sit' (aluminium lawn chair), 'pool' (in a kiddie pool of ice), 'stand'"""
    L = LOCALS[kind]
    E = X(expr)
    if blink is None: blink = ((t + len(kind)) % 3.8) < 0.12
    sk = L['skin']
    if pose == 'sit':
        sp.line((-6.0, 0.0), (5.0, 12.0), (190, 196, 204)); sp.line((5.0, 0.0), (-6.0, 12.0), (190, 196, 204))
        sp.rect(-7.0, 11.0, 7.0, 13.0, (60, 200, 170)); sp.rect(-8.0, 11.0, -6.0, 30.0, (60, 200, 170))
        for q in range(4): sp.line((-7.6, 14.0 + q * 4.0), (-6.4, 14.0 + q * 4.0), (240, 250, 250))
        hip = 14.0
        sp.cap((0.0, hip), (9.0, hip), 2.8, 2.5, tones(L['shorts']))                                 # thigh
        sp.cap((9.0, hip), (10.0, 2.0), 1.8, 1.6, tones(sk)); sp.sup(11.2, 1.2, 3.0, 1.2, tones((240, 240, 240)), n=2.2)
    elif pose == 'pool':
        sp.ell(2.0, 2.4, 15.0, 3.6, tones((90, 170, 240)))
        hip = 4.6
        sp.cap((0.0, hip), (10.0, hip), 2.8, 2.5, tones(L['shorts']))
        sp.fill(sp.m_ell(2.0, 4.0, 13.0, 1.8)[0], (220, 244, 255))                                   # ice water over the legs
        for q in range(6): sp.rect(-8.0 + q * 3.6, 4.6 + (q % 2), -6.4 + q * 3.6, 6.4 + (q % 2), (240, 250, 255))
    else:
        for dx in (-2.6, 2.6):
            sp.cap((dx, 20.0), (dx, 3.0), 2.0, 1.8, tones(sk)); sp.sup(dx + 1.2, 1.4, 3.2, 1.4, tones((240, 240, 240)), n=2.2)
        hip = 21.0
        sp.union([sp.m_ell(0.0, hip, 6.6, 3.6)], tones(L['shorts']))
    sp.union([sp.m_ell(0.0, hip + 9.0, 6.4, 8.6)], tones(L['shirt']))                                 # torso sits on the hips
    if kind == 'retiree':
        for q in range(4): sp.dot(-3.0 + q * 2.0, hip + 10.0 - (q % 2) * 3, (255, 230, 90))         # palm print
    hx, hy = 1.0, hip + 22.0
    sp.cap((0.6, hip + 16.0), (1.0, hip + 18.0), 2.0, 2.0, tones(sk))
    sp.union([sp.m_ell(hx, hy, 5.0, 5.4)], tones(sk))
    DX.eye(sp, hx + 2.0, hy + 0.6, 2.6, 2.6, E, (80, 80, 90), look, blink, lash=INK, skin=sk)
    DX.eye(sp, hx - 1.4, hy + 0.6, 2.4, 2.4, E, (80, 80, 90), look, blink, lash=INK, skin=sk)
    DX.mouth(sp, hx + 2.0, hy - 3.0, 3.0, E, mouth_, (150, 70, 60), skin=sk, maxh=3)
    sp.ell(hx + 4.4, hy - 0.8, 1.2, 1.2, tones(sk))
    if L['hair'] == 'visor':
        sp.union([sp.m_ell(hx - 1.0, hy + 3.8, 4.8, 2.2)], tones(L['hairc']))
        sp.rect(hx - 4.0, hy + 3.4, hx + 4.0, hy + 4.6, (250, 250, 250)); sp.rect(hx + 2.0, hy + 3.0, hx + 8.0, hy + 3.8, (60, 200, 170))
    elif L['hair'] == 'curlers':
        sp.union([sp.m_ell(hx - 0.6, hy + 3.4, 6.0, 3.6)], tones(L['hairc']))
        for q in range(4): sp.cap((hx - 4.0 + q * 2.6, hy + 5.4), (hx - 3.0 + q * 2.6, hy + 5.4), 0.9, 0.9, tones((120, 200, 255)))
    elif L['hair'] == 'cap':
        sp.union([sp.m_ell(hx - 0.4, hy + 3.4, 5.4, 2.6)], tones(L['hairc'])); sp.rect(hx + 2.0, hy + 2.6, hx + 8.0, hy + 3.4, L['hairc'])
    else:
        sp.ell(hx - 4.4, hy + 0.6, 1.4, 2.2, tones(L['hairc']))
    sp.outline(INK, 1)
    before = sp.m.copy()                                                                             # near arm: hand on the lap / holding
    sh = (3.4, hip + 14.0)
    hn = (8.0, hip + 4.0) if pose != 'stand' else (7.0, hip + 2.0)
    kN, eN = ik(sh, hn, 6.0, 6.0, -1.0)
    sp.cap(sh, kN, 1.8, 1.6, tones(L['shirt'])); sp.cap(kN, eN, 1.5, 1.3, tones(sk)); sp.ell(*eN, 1.6, 1.5, tones(sk))
    if pose == 'stand': sp.rect(eN[0] - 1.0, eN[1], eN[0] + 1.6, eN[1] + 3.0, (250, 210, 120)); sp.ell(eN[0] + 0.3, eN[1] + 3.6, 1.6, 1.4, tones((255, 160, 200)))  # ice cream cone
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o
    sp.anchors.update(head=(hx, hy))
    if frost > 0: frost_over(sp, frost, t)


def van(sp, t=0.0, frost=1.0):
    """a white COOL-RITE A/C service van, side view facing +x; frosted windows (the repairman's own A/C is dead too)"""
    W_ = (240, 242, 238)
    body = sp.union([sp.m_super(0.0, 14.0, 26.0, 9.0, 4.0), sp.m_super(16.0, 21.0, 10.0, 7.0, 3.0)], tones(W_))
    sp.fill(body & (np.abs(DX.YC - 12.0) < 1.6), (40, 120, 200))
    txt(sp, 'COOL-RITE', -18.0, 20.0, (40, 120, 200))
    for (x0, x1) in ((8.0, 14.0), (17.0, 24.0)):
        wm = sp.m_poly([(x0, 18.0), (x1, 18.0), (x1 - (1.6 if x1 > 20 else 0), 25.0), (x0, 25.0)])
        sp.fill(wm, (150, 200, 230)); sp.fill(wm & (FX.halftone() < -0.2 + 0.3 * frost), (236, 248, 255))
    _wheel(sp, -16.0, 4.6, 4.6, 0.0); _wheel(sp, 16.0, 4.6, 4.6, 0.0)
    sp.ell(26.0, 14.0, 1.0, 1.4, tones((255, 236, 160)))
    sp.outline(INK, 1)
