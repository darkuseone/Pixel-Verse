"""«STILL 1986» cast + props in the «Sunset Chrome» manner (props/v86pix.py). Coordinates: sprite px, feet anchor at (0, 0),
x right = facing side, y UP. Rim light and the ink outline are added by v86pix.Act / v86pix.draw — draw functions here do NOT outline.
  vince(sp, ...)   — Vince Velour, 44: «an inverted triangle on toothpicks» (huge padded shoulders, pastel teal blazer with pushed
                     sleeves, pink tee, white linen pants, loafers without socks), a blond perm-mullet, see-through sunset aviators,
                     designer stubble, leather tan, toothpick, a gold chain with a tiny palm; a smartphone in a 1986 brick-phone case
  rey(sp, ...)     — Rey, tow driver: «a fridge in a cap» (square, no neck), neon-orange safety vest over a hibiscus shirt, cap backwards,
                     horseshoe moustache, sleepy lids, a fat TOW receipt book in the pocket
  car(sp, ...)     — Vince's white 80s wedge convertible (pop-up lights, louvered tail lights, pink + cyan side stripe; no real make);
                     vince=dict(...) seats Vince in it
  tow_cab / tow_bed — Rey's flatbed tow truck in two sprites (cab, tilting bed), sign_free — the «FREE PARKING*» bait board
  meter(sp, ...)   — an old Miami Beach parking meter with a «PAY BY APP ONLY» sticker; coin, phone (hand props)"""
import math
import numpy as np
from props import dibspix as DX
from props.dibspix import dark, mix, erode, dilate, ik, EXPR
from props.v86pix import tones, thin, stroke, INK, WHITE, SUN, CYAN, PINK

# ---------------------------------------------------------------- palette
TAN = (214, 146, 104)              # Vince: leather-sofa tan
TAN_J = (196, 128, 92)
BLOND = (240, 200, 112)            # perm mullet
BLOND_D = (196, 146, 70)
TEAL = (96, 216, 206)              # pastel teal blazer
TEE = (255, 112, 172)              # hot-pink tee
LINEN = (246, 240, 226)
LOAFER = (250, 248, 240)
GOLD = (246, 200, 76)
LENS_T, LENS_B = (255, 96, 170), (255, 178, 84)    # aviator gradient: magenta top -> orange bottom
BRICK = (44, 44, 52)
SKIN_R = (176, 116, 82)            # Rey
VEST = (255, 132, 40)
VEST_R = (230, 240, 240)           # reflective stripes
SHIRT_R = (38, 150, 160)           # hibiscus shirt
HIB = (255, 86, 120)
JEANS = (62, 78, 120)
CAP_R = (32, 36, 46)
MOUST = (40, 30, 30)
CAR = (248, 246, 242)              # white wedge
CAR_D = (196, 196, 214)
CHROME = (214, 220, 236)
TIRE = (30, 28, 40)
TOW_W = (238, 236, 230)
TOW_O = (255, 128, 30)
STEEL = (120, 126, 146)
CAR_K = 1.28                       # car sprite scale vs the hero scale (real proportions, owner rule 12.11.2026)
TOW_K = 1.70                       # tow truck sprites vs the hero scale
METER = (150, 158, 176)

XTRA = dict(
    cool=dict(eo=0.7, pu=0.6, bt=0.25, bl=0.0, mo=0.0, mc=0.55, lid=0.4),
    smooth=dict(eo=0.85, pu=0.6, bt=0.1, bl=0.2, mo=0.0, mc=0.95, teeth=True, lid=0.2),
    outraged=dict(eo=1.3, pu=0.32, bt=0.75, bl=0.2, mo=0.9, mc=-0.3),
    scheming=dict(eo=0.55, pu=0.55, bt=0.55, bl=-0.1, mo=0.0, mc=0.7, lid=0.45),
    ecstatic=dict(eo=1.15, pu=0.65, bt=-0.3, bl=0.7, mo=0.8, mc=1.0),
    defeated=dict(eo=0.75, pu=0.6, bt=-0.6, bl=0.2, mo=0.0, mc=-0.5, lid=0.35),
    proudsad=dict(eo=0.8, pu=0.6, bt=-0.45, bl=0.3, mo=0.0, mc=0.45, lid=0.3),
    tired=dict(eo=0.5, pu=0.6, bt=-0.2, bl=0.0, mo=0.0, mc=0.1, lid=0.62),
    chill=dict(eo=0.62, pu=0.6, bt=0.0, bl=0.0, mo=0.0, mc=0.35, lid=0.55),
    gotcha=dict(eo=0.7, pu=0.55, bt=0.35, bl=0.1, mo=0.0, mc=0.85, lid=0.4, teeth=True),
)


def X(expr):
    if isinstance(expr, dict): return dict(expr)                  # smooth mimic (props/mimic.py) passes a ready dict
    return dict(XTRA.get(expr) or EXPR.get(expr, EXPR['normal']))


# ================================================================================ hand props
def coin(sp, h):
    x, y = h
    sp.ell(x + 0.8, y + 1.6, 1.5, 1.5, tones(GOLD), gloss=1.0)
    sp.star(x + 0.4, y + 2.2, 0.8)
    sp.anchors['coin'] = (x + 0.8, y + 1.6)


def phone(sp, h, lit=True):
    """a smartphone in a 1986 «brick» case: chunky grey body, keypad bumps, a rubber antenna; the screen glows cyan"""
    x, y = h
    sp.sup(x + 0.6, y + 4.4, 2.2, 5.0, tones(BRICK), n=4.0)
    sp.fill(sp.m_super(x + 0.9, y + 6.4, 1.5, 2.2, 4.0)[0], (120, 230, 255) if lit else (60, 70, 80))
    for q in range(3):
        for r in range(2): sp.dot(x + r * 1.2, y + 1.6 + q * 1.0, (110, 112, 126))
    thin(sp, (x - 0.6, y + 9.0), (x - 0.9, y + 13.6), (60, 60, 70), 0.45)
    sp.blob(x - 0.9, y + 13.8, 0.55, (200, 60, 70))
    sp.anchors['phone'] = (x + 0.9, y + 6.4)


def toothpick(sp, a, b):
    thin(sp, a, b, (236, 210, 150), 0.24)


# ================================================================================ face parts shared by Vince
def aviators(sp, eyes, hy, k=1.0, glint=0.0):
    """see-through sunset aviators over drawn eyes (rule: eyes and brows readable through the glass): teardrop lenses blended
    magenta->orange over whatever is under them, thin gold rims, a bridge, a diagonal reflection"""
    if k <= 0: return
    col = sp.col.astype(np.float32)
    for (ex, w) in eyes:
        m, nx, ny = sp.m_super(ex + 0.2, hy - 0.3, w * 0.62 + 0.6, 2.5, 2.2)
        m &= ~(ny > 0.55) | (np.abs(nx) < 0.85)
        g = np.clip((ny + 1) / 2, 0, 1)[..., None]                                   # 1 at the top
        tint = np.array(LENS_B, np.float32) * (1 - g) + np.array(LENS_T, np.float32) * g
        a = 0.30 * k
        col[m] = col[m] * (1 - a) + tint[m] * a
        sp.col = np.clip(col, 0, 255).astype(np.uint8)
        e = m & ~erode(m)
        sp.fill(e, GOLD)
        thin(sp, (ex - w * 0.4, hy + 0.9), (ex - w * 0.05, hy + 1.8), (255, 255, 255), 0.22, keep=True)   # reflection
        col = sp.col.astype(np.float32)
        sp.m |= m
    (x0, _), (x1, _) = eyes[1], eyes[0]
    thin(sp, (x0 + 1.6, hy + 1.2), (x1 - 1.8, hy + 1.2), GOLD, 0.28)
    if glint > 0: sp.star(eyes[0][0] + 1.0, hy + 1.6, 1.2 * glint)


# ================================================================================ VINCE
def vince(sp, t=0.0, expr='cool', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
          legs=True, ox=0.0, oy=0.0, shades=1.0, glint=0.0, pick=True, sweat=0.0, walk=None, lean=0.0, sparkle=0.0, hair_wind=0.0):
    """VINCE VELOUR. ox, oy shift the whole figure (seated in the car: legs=False, oy < 0). hair_wind 0..1 blows the mullet back"""
    E = X(expr)
    if blink is None: blink = ((t + 0.9) % 4.1) < 0.12
    br = 0.35 * math.sin(t * 2.1)
    bob = abs(math.sin(walk)) * 1.0 if walk is not None else 0.0
    def Q(x, y): return (x + ox + lean * (y / 60.0) * 5.0, y + oy + (bob if y > 10 else 0.3 * bob))
    swing = math.sin(walk) * 4.0 if walk is not None else 0.0
    wind = hair_wind * (1.0 + 0.15 * math.sin(t * 13))
    # ---------------------------------------------------------------- far arm (behind the blazer)
    shF = Q(-13.0, 57.0 + br * 0.3)
    hf = hand_f if hand_f is not None else Q(-14.0 - swing * 0.6, 38.0)
    kF, eF = ik(shF, hf, 10.0, 9.0, -1.0)
    sp.cap(shF, kF, 4.6, 3.8, tones(dark(TEAL, 0.82)))
    sp.ell(kF[0], kF[1], 3.6, 2.6, tones(dark(TEAL, 0.78)))                                     # scrunched sleeve at the elbow
    sp.cap(kF, eF, 2.8, 2.4, tones(dark(TAN, 0.86)))
    sp.ell(eF[0], eF[1] - 0.3, 2.8, 2.6, tones(dark(TAN, 0.86)))
    if prop_f: prop_f(sp, eF)
    sp.anchors['hand_f'] = eF
    # ---------------------------------------------------------------- back of the mullet (behind the shoulders)
    hx, hy = Q(3.0, 69.0)
    tail = sp.union([sp.m_cap((hx - 4.6, hy + 1.0), (hx - 7.4 - 3.0 * wind, hy - 8.6 + 4.0 * wind), 4.2, 3.4),
                     sp.m_ell(hx - 7.0 - 3.5 * wind, hy - 8.0 + 4.5 * wind, 3.4, 2.6)], tones(BLOND))
    for q in range(4):
        thin(sp, (hx - 5.4 - q * 0.6, hy + 0.6), (hx - 8.2 - q * 0.5 - 3.0 * wind, hy - 8.0 + 4.0 * wind), BLOND_D, 0.2, mask=tail)
    # ---------------------------------------------------------------- legs: white linen, bare ankles, loafers
    if legs:
        sw = math.sin(walk) * 2.6 if walk is not None else 0.0
        for k_, dx in enumerate((-3.2, 3.4)):
            near = k_ == 1
            s_ = sw if near else -sw
            fx_, fy_ = dx + s_ * 0.7, 2.6 + max(0.0, s_) * 0.5
            c = LINEN if near else dark(LINEN, 0.88)
            sp.cap(Q(dx * 0.9, 34.0), (fx_ + ox, fy_ + 3.2 + oy), 3.2, 1.9, tones(c))
            sp.ell(fx_ + ox, fy_ + 2.2 + oy, 1.3, 1.1, tones(TAN if near else dark(TAN, 0.85)))      # bare ankle
            lf = sp.sup(fx_ + 2.0 + ox, fy_ + oy, 4.4, 1.8, tones(LOAFER if near else dark(LOAFER, 0.88)), n=2.4)
            sp.fill(lf & (DX.YC < fy_ + oy - 1.0), (168, 160, 150))
            thin(sp, (fx_ + 2.4 + ox, fy_ + 1.2 + oy), (fx_ + 4.6 + ox, fy_ + 1.0 + oy), GOLD, 0.25)   # horsebit
    # ---------------------------------------------------------------- torso: the inverted triangle
    bp = sp.m_poly([Q(-16.5, 59.5), Q(19.0, 59.5), Q(10.6, 33.0), Q(-9.6, 33.0)])
    bnx = np.clip((DX.XC - Q(1.2, 0)[0]) / 18.0, -0.9, 0.9); bny = np.clip((DX.YC - Q(0, 47.0)[1]) / 16.0, -0.9, 0.9)
    blazer = sp.union([(bp, bnx, bny), sp.m_ell(*Q(-14.2, 57.4), 5.6, 3.8), sp.m_ell(*Q(16.6, 57.4), 5.6, 3.8)], tones(TEAL))
    vx = [Q(3.0, 59.4), Q(11.4, 59.4), Q(6.0, 34.0)]                                             # V opening: the hot-pink tee
    tee = sp.m_poly(vx) & blazer
    sp.paint(tee, tones(TEE), DX.lit(np.clip((DX.XC - Q(7, 0)[0]) / 6.0, -0.9, 0.9), np.clip((DX.YC - Q(0, 47)[1]) / 14.0, -0.9, 0.9)))
    for side in (0, 1):                                                                           # lapel shadows
        a, b = (vx[0], vx[2]) if side == 0 else (vx[1], vx[2])
        thin(sp, a, b, dark(TEAL, 0.55), 0.3)
    thin(sp, Q(-9.6, 33.4), Q(10.6, 33.4), dark(TEAL, 0.6), 0.3)
    for q in range(2): sp.dot(*Q(-1.0, 40.0 + q * 4.0), (236, 236, 226))                            # buttons
    sp.fill(sp.m_super(*Q(-6.5, 51.0), 2.2, 1.2, 4.0)[0] & blazer, dark(TEAL, 0.8))               # breast pocket
    pk = Q(-6.5, 52.0); sp.ell(pk[0] - 0.6, pk[1] + 0.8, 0.9, 0.9, tones(PINK), ol=False)           # pink pocket square
    # gold chain + tiny palm pendant on the tee
    for q in range(9):
        a = math.pi * (1.1 + 0.8 * q / 8)
        sp.blob(*Q(7.2 + math.cos(a) * 3.0, 58.4 + math.sin(a) * 4.2), 0.42, GOLD)
    px_, py_ = Q(7.2, 53.4)
    thin(sp, (px_, py_), (px_, py_ - 2.0), (150, 110, 60), 0.3)
    for a in (-0.9, -0.3, 0.3, 0.9): thin(sp, (px_, py_), (px_ + math.sin(a) * 1.6, py_ + math.cos(a) * 0.9), (60, 190, 120), 0.3)
    # ---------------------------------------------------------------- neck + head
    sp.cap(Q(3.2, 57.0), Q(3.4, 61.0), 2.8, 2.8, tones(dark(TAN, 0.92)))
    head = sp.union([sp.m_ell(hx + 0.4, hy, 7.6, 8.2), sp.m_super(hx + 1.2, hy - 4.0, 6.8, 4.2, 3.2)], tones(TAN))
    sp.ell(hx - 5.6, hy + 0.4, 1.6, 2.4, tones(dark(TAN, 0.92)))                                  # ear
    sp.blob(hx - 5.6, hy - 1.8, 0.45, GOLD)                                                        # stud
    DX.stubble(sp, sp.m_ell(hx + 2.0, hy - 6.6, 6.0, 2.2)[0] & head, dark(TAN, 0.76), 0.12, 5)
    lx, ly = look
    eyes = [(hx + 4.4, 4.4), (hx - 0.6, 3.8)]
    DX.eye(sp, eyes[0][0], hy + 1.4, 4.4, 4.0, E, (30, 170, 236), (lx, ly), blink, lash=INK, skin=TAN, bold=1)
    DX.eye(sp, eyes[1][0], hy + 1.4, 3.8, 3.8, E, (30, 170, 236), (lx, ly), blink, lash=INK, skin=TAN, bold=1)
    aviators(sp, eyes, hy + 1.4, shades, glint)
    DX.brow(sp, hx + 4.4, hy + 5.2, 4.4, E, +1, BLOND_D, th=2)
    DX.brow(sp, hx - 0.6, hy + 5.1, 3.8, E, -1, BLOND_D, th=2)
    sp.ell(hx + 7.8, hy - 1.0, 1.7, 2.2, tones(dark(TAN, 0.98)), gloss=1.0)                       # nose
    sp.dot(hx + 7.4, hy - 2.8, dark(TAN, 0.6))
    if sp.k >= 2:
        thin(sp, (hx + 6.4, hy - 3.2), (hx + 7.2, hy - 4.8), dark(TAN, 0.7), 0.12)                # smile fold
    DX.blush(sp, hx + 3.4, hy - 2.8, 2.0, 1.2, (236, 110, 100))
    mx, my = hx + 3.8, hy - 5.2
    DX.mouth(sp, mx, my, 5.2, E, mouth_, (150, 70, 60), inside=(90, 24, 34), teeth=(255, 255, 252), skin=TAN, maxh=5.6)
    if pick and max(mouth_, E['mo']) < 0.45: toothpick(sp, (mx + 2.0, my + 0.2), (mx + 6.0, my + 1.4))
    if sparkle > 0 and E['mc'] > 0.5: sp.star(mx + 1.0, my + 0.4, 1.4 * sparkle)
    # perm-mullet: a big blond cloud on top, feathered bangs swept up and back
    top = [(hx - 0.6, hy + 8.6, 8.0, 3.8), (hx + 5.0, hy + 8.2, 3.6, 2.6), (hx - 5.8, hy + 4.6, 3.0, 4.6)]
    for q in range(7):
        a = math.pi * (0.12 + 0.84 * q / 6)
        top.append((hx - 0.6 + math.cos(a) * 7.4 - wind * 1.2, hy + 7.2 + math.sin(a) * 3.6, 2.4, 2.0))
    hair = sp.union([sp.m_ell(cx, cy, rx, ry) for (cx, cy, rx, ry) in top], tones(BLOND),
                    exclude=head & (DX.YC < hy + 6.0) & (DX.XC > hx - 4.6))
    for (cx, cy, rx, ry) in top[3:]:
        thin(sp, (cx - rx * 0.5, cy + ry * 0.2), (cx + rx * 0.3, cy + ry * 0.55), (255, 238, 180), 0.24, mask=hair)
        thin(sp, (cx - rx * 0.4, cy - ry * 0.3), (cx + rx * 0.4, cy - ry * 0.2), BLOND_D, 0.18, mask=hair)
    sp.fill(sp.m_super(hx - 4.6, hy + 2.0, 1.2, 3.4, 3.0)[0] & head, BLOND)                    # sideburn
    if sweat > 0:
        for i, (x, y) in enumerate(((hx - 2.0, hy + 4.6), (hx + 6.0, hy + 4.0))[:int(1 + sweat)]):
            yy = y - ((t * 4.0 + i * 1.3) % 3.5)
            sp.ell(x, yy, 0.6, 1.0, tones((170, 220, 255)), ol=False)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 2.0, hy + 1.2), chest=Q(2.0, 48.0))
    # ---------------------------------------------------------------- near arm (over the body)
    before = sp.m.copy()
    shN = Q(16.0, 57.0 + br * 0.3)
    hn = hand_n if hand_n is not None else Q(18.0 + swing * 0.6, 37.0)
    kN, eN = ik(shN, hn, 10.0, 9.0, -1.0)
    sp.cap(shN, kN, 4.8, 4.0, tones(TEAL))
    sp.ell(kN[0], kN[1], 3.8, 2.7, tones(dark(TEAL, 0.9)))
    sp.cap(kN, eN, 2.9, 2.5, tones(TAN))
    w_ = (kN[0] + (eN[0] - kN[0]) * 0.78, kN[1] + (eN[1] - kN[1]) * 0.78)
    sp.ell(w_[0], w_[1], 1.6, 1.0, tones(GOLD), gloss=1.0)                                        # gold watch
    if prop_n and getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.ell(eN[0], eN[1] - 0.3, 2.9, 2.7, tones(TAN))
    if prop_n and not getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m & before
    sp.col[o] = INK


# ================================================================================ REY
def rey(sp, t=0.0, expr='chill', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, legs=True,
        ox=0.0, oy=0.0, point=False):
    """REY — the tow driver: a fridge in a backwards cap"""
    E = X(expr)
    if blink is None: blink = ((t + 2.3) % 4.7) < 0.13
    br = 0.3 * math.sin(t * 1.7)
    def Q(x, y): return (x + ox, y + oy)
    # far arm
    shF = Q(-13.0, 52.0 + br)
    hf = hand_f if hand_f is not None else Q(-15.0, 33.0)
    kF, eF = ik(shF, hf, 9.0, 8.5, -1.0)
    sp.cap(shF, kF, 4.0, 3.4, tones(dark(SHIRT_R, 0.8)))
    sp.cap(kF, eF, 3.0, 2.6, tones(dark(SKIN_R, 0.85)))
    sp.ell(eF[0], eF[1] - 0.4, 2.8, 2.6, tones(dark(SKIN_R, 0.85)))
    if legs:
        for k_, dx in enumerate((-5.0, 5.0)):
            c = JEANS if k_ else dark(JEANS, 0.86)
            sp.cap(Q(dx, 28.0), Q(dx, 5.0), 4.4, 3.8, tones(c))
            sp.sup(*Q(dx + 2.0, 2.2), 5.4, 2.4, tones((70, 54, 44)), n=2.4)                        # work boots
    # the fridge: a square torso, hibiscus shirt, orange safety vest
    tor = sp.sup(*Q(0.0, 41.0), 14.4, 15.0, tones(SHIRT_R), n=4.2)
    rng = np.random.default_rng(3)
    for q in range(14):                                                                            # hibiscus flowers
        x, y = rng.uniform(-12, 12), rng.uniform(28, 54)
        for a in range(5): sp.blob(*Q(x + math.cos(a * 1.26) * 1.0, y + math.sin(a * 1.26) * 1.0), 0.6, HIB, mask=tor)
        sp.blob(*Q(x, y), 0.4, (255, 220, 90), mask=tor)
    vest = tor & ~(sp.m_poly([Q(-3.4, 57.0), Q(5.4, 57.0), Q(1.4, 36.0)]))
    sp.paint(vest, tones(VEST), DX.lit(np.clip((DX.XC - Q(0, 0)[0]) / 15.0, -0.9, 0.9), np.clip((DX.YC - Q(0, 41)[1]) / 15.0, -0.9, 0.9)))
    for yy in (33.0, 37.0): sp.fill(vest & (np.abs(DX.YC - Q(0, yy)[1]) < 0.7), VEST_R)
    pkt = sp.m_super(*Q(-7.0, 44.0), 3.2, 3.8, 4.0)[0] & vest
    sp.paint(pkt, tones((250, 246, 230)), None)                                                      # TOW receipt book in the pocket
    sp.txt_box(['TOW'], (Q(-10.0, 0)[0], Q(0, 41.0)[1], Q(-4.0, 0)[0], Q(0, 47.4)[1]), (210, 40, 40), pad=0.3)
    thin(sp, Q(-5.2, 48.2), Q(-4.6, 52.0), (40, 60, 160), 0.35)                                    # pen
    # head: no neck, sits right on the fridge
    hx, hy = Q(1.6, 63.0)
    head = sp.union([sp.m_super(hx, hy, 7.6, 7.8, 3.0)], tones(SKIN_R))
    sp.ell(hx - 6.4, hy, 1.6, 2.4, tones(dark(SKIN_R, 0.9)))
    DX.stubble(sp, sp.m_ell(hx + 1.0, hy - 4.6, 7.0, 3.0)[0] & head, dark(SKIN_R, 0.62), 0.5, 7)
    lx, ly = look
    DX.eye(sp, hx + 3.8, hy + 1.6, 3.6, 3.2, E, (70, 46, 30), (lx, ly), blink, lash=INK, skin=SKIN_R, bold=1)
    DX.eye(sp, hx - 1.2, hy + 1.6, 3.2, 3.0, E, (70, 46, 30), (lx, ly), blink, lash=INK, skin=SKIN_R, bold=1)
    DX.brow(sp, hx + 3.8, hy + 4.6, 4.0, E, +1, MOUST, th=2, bushy=True)
    DX.brow(sp, hx - 1.2, hy + 4.5, 3.4, E, -1, MOUST, th=2, bushy=True)
    sp.ell(hx + 6.8, hy - 0.6, 2.0, 2.2, tones(dark(SKIN_R, 0.95)), gloss=1.0)
    mx, my = hx + 3.2, hy - 4.6
    DX.mouth(sp, mx, my, 4.6, E, mouth_, (120, 60, 50), inside=(80, 20, 30), skin=SKIN_R, maxh=4.6)
    ms = sp.union([sp.m_ell(mx, my + 1.6, 4.4, 1.2), sp.m_cap((mx - 3.8, my + 1.4), (mx - 4.4, my - 3.4), 0.9, 0.8),
                   sp.m_cap((mx + 3.8, my + 1.4), (mx + 4.2, my - 3.4), 0.9, 0.8)], tones(MOUST))          # horseshoe moustache
    # cap backwards
    sp.union([sp.m_ell(hx - 0.4, hy + 6.4, 8.0, 3.4)], tones(CAP_R))
    sp.sup(hx - 8.6, hy + 4.4, 3.4, 1.0, tones(CAP_R), n=2.4)                                     # brim to the back
    sp.blob(hx - 0.4, hy + 9.6, 0.6, (90, 90, 100))
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 1.4, hy + 1.6))
    # near arm
    before = sp.m.copy()
    shN = Q(13.0, 52.0 + br)
    hn = hand_n if hand_n is not None else (Q(22.0, 58.0) if point else Q(15.0, 33.0))
    kN, eN = ik(shN, hn, 9.0, 8.5, -1.0)
    sp.cap(shN, kN, 4.2, 3.6, tones(SHIRT_R))
    sp.cap(kN, eN, 3.2, 2.8, tones(SKIN_R))
    if prop_n: prop_n(sp, eN)
    sp.ell(eN[0], eN[1] - 0.4, 3.0, 2.8, tones(SKIN_R))
    if point: thin(sp, (eN[0] + 1.6, eN[1] + 0.6), (eN[0] + 4.6, eN[1] + 1.8), SKIN_R, 0.9)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m & before
    sp.col[o] = INK


# ================================================================================ VINCE'S CAR
def _wheel(sp, x, y, r, t, spin):
    sp.ell(x, y, r, r, tones(TIRE))
    rim_ = sp.ell(x, y, r * 0.62, r * 0.62, tones(CHROME), gloss=1.0)
    a0 = t * spin
    for q in range(5):
        a = a0 + q * 2 * math.pi / 5
        thin(sp, (x, y), (x + math.cos(a) * r * 0.56, y + math.sin(a) * r * 0.56), dark(CHROME, 0.6), 0.45, mask=rim_)
    sp.blob(x, y, r * 0.16, dark(CHROME, 0.55))
    sp.star(x - r * 0.3, y + r * 0.3, 0.9)


def car(sp, t=0.0, vince_kw=None, speed=0.0, lights=False, glow=0.0, stripe=True, part='all'):
    """the white wedge, side view facing +x, ~150 px long (draw at CAR_K x the hero scale: real ~4.4 m = 2.4 heights of a man);
    part='back' (seat back only) / 'front' (everything that hides a seated hero) / 'all'; vince_kw seats Vince (part='all' only,
    for the model sheet; in shots Vince is a separate actor between 'back' and 'front', see v86kit.car_group)"""
    if part in ('all', 'back'):
        sp.cap((-21.0, 26.0), (-18.5, 40.0), 3.4, 3.0, tones((246, 236, 220)))
        sp.anchors.update(seat=(-6.0, 22.0))
        if part == 'back': return
    if vince_kw is not None and part == 'all':
        kw = dict(vince_kw); kw.setdefault('legs', False); kw.setdefault('ox', -6.0); kw.setdefault('oy', -17.0)
        kw.setdefault('hand_n', (10.4, 37.0)); kw.setdefault('hand_f', (-16.0, 31.0))
        vince(sp, t=t, **kw)
    ring = sp.m_ell(13.0, 40.0, 1.8, 5.4)[0] & ~sp.m_ell(13.0, 40.0, 0.9, 4.2)[0]                  # steering wheel (edge-on)
    sp.fill(ring, (40, 36, 50))
    thin(sp, (13.0, 40.0), (10.0, 34.0), (40, 36, 50), 0.6)
    body = sp.poly([(-74.0, 7.0), (-75.5, 27.0), (-44.0, 30.4), (-26.0, 31.2), (16.0, 31.2), (24.0, 30.0), (68.0, 22.0),
                    (76.5, 15.5), (73.0, 7.0)], tones(CAR), val=np.clip(0.95 - (31.0 - DX.YC) / 30.0, 0.05, 0.98))
    sp.fill(body & (DX.YC < 12.5), dark(CAR, 0.82))                                               # rocker panel shade
    for (wx, r) in ((-48.0, 12.4), (49.0, 12.4)):                                                # wheel arches
        arch = sp.m_ell(wx, 10.0, r, r)[0]
        sp.fill(arch & body, (34, 26, 56))
    if stripe:
        for y, c in ((20.4, PINK), (18.6, CYAN)):
            sp.fill(body & (np.abs(DX.YC - y) < 0.55) & ~sp.m_ell(-48, 10, 12.6, 12.6)[0] & ~sp.m_ell(49, 10, 12.6, 12.6)[0], c)
    thin(sp, (-26.0, 31.3), (16.0, 31.3), CHROME, 0.5)                                             # door top chrome
    thin(sp, (-6.0, 30.8), (-6.0, 9.0), dark(CAR, 0.7), 0.22)                                      # door seam
    thin(sp, (-2.6, 25.6), (1.6, 25.6), CHROME, 0.4)                                               # handle
    for q in range(4): thin(sp, (-40.0, 24.6 - q * 1.6), (-28.0, 24.6 - q * 1.6), dark(CAR, 0.62), 0.32)   # side louvers
    tl = sp.m_super(-73.4, 22.0, 1.6, 4.4, 4.0)[0]                                                 # louvered tail light
    sp.fill(tl, (230, 40, 70)); sp.fill(tl & ((np.floor(DX.YC * 1.0).astype(int)) % 2 == 0), (120, 16, 40))
    sp.fill(sp.m_super(74.0, 11.5, 2.6, 2.0, 3.0)[0], CHROME)                                    # bumpers
    sp.fill(sp.m_super(-74.2, 10.0, 2.0, 2.4, 3.0)[0], CHROME)
    if lights:                                                                                     # pop-up headlights up
        sp.sup(60.0, 26.4, 4.0, 2.6, tones(CAR), n=4.0)
        sp.fill(sp.m_super(63.4, 26.4, 0.9, 2.0, 3.0)[0], (255, 250, 210))
    # windshield + mirror
    gl = sp.m_poly([(18.0, 31.0), (27.0, 46.0), (30.0, 46.0), (22.0, 31.0)])
    sp.paint(gl, [(150, 210, 240), (190, 236, 255), (236, 250, 255)], np.clip((DX.XC - 18) / 12.0, 0, 1), ol=False, stripes=False)
    thin(sp, (18.0, 31.0), (27.4, 46.4), CHROME, 0.5); thin(sp, (27.4, 46.4), (30.4, 46.4), CHROME, 0.5)
    sp.ell(23.0, 35.0, 1.8, 1.2, tones(CAR))
    sp.star(28.4, 44.6, 1.0)
    _wheel(sp, -48.0, 10.0, 10.0, t, -speed)
    _wheel(sp, 49.0, 10.0, 10.0, t, -speed)
    sp.anchors.update(seat=(-6.0, 22.0), front=(76.0, 15.0), rear=(-75.0, 15.0), dash=(14.0, 36.0))


# ================================================================================ REY'S TOW TRUCK
def tow_cab(sp, t=0.0, beacon=True, rey_kw=None):
    """cab + hood facing +x (x -30 .. +50); rey_kw draws Rey's head + shoulder in the driver window"""
    cab = sp.sup(-6.0, 34.0, 24.0, 25.0, tones(TOW_W), n=5.0)
    hood = sp.sup(32.0, 24.0, 17.0, 13.0, tones(TOW_W), n=4.4)
    sp.fill((cab | hood) & (np.abs(DX.YC - 24.0) < 2.2), TOW_O)                                     # orange stripe
    win = sp.m_super(4.0, 47.0, 12.0, 8.6, 4.0)[0]
    sp.paint(win, [(40, 40, 70), (60, 70, 110), (90, 110, 160)], np.clip((DX.YC - 40) / 14.0, 0, 1), ol=False, stripes=False)
    if rey_kw is not None:
        kw = dict(rey_kw); kw.update(legs=False, ox=2.0, oy=-14.0)
        before = sp.m.copy()
        rey(sp, t=t, **kw)
        cut = sp.m & ~before & ~(win | (DX.YC > 56.0))                                         # only what shows in the window
        sp.m[cut] = False
        sp.m |= before
        sp.anchors['rey_head'] = sp.anchors['head']
    thin(sp, (4.0 - 12.0, 55.6), (4.0 + 12.0, 55.6), dark(TOW_W, 0.6), 0.4)
    door = (-24.0, 9.0, -3.0, 21.0)
    sp.txt_box(["REY'S", 'TOWING'], door, (210, 40, 40), alt=(["REY'S"],), pad=0.6)
    sp.txt_box(['24 HR'], (-3.0, 14.0, 12.0, 21.0), INK, pad=0.6)
    if beacon:
        on = (int(t * 4) % 2) == 0
        sp.sup(-6.0, 61.0, 12.0, 2.4, tones((255, 170, 30) if on else (190, 110, 20)), n=4.0)
    sp.ell(47.0, 27.0, 2.2, 2.6, tones((255, 250, 220)), gloss=1.0)                                  # headlight
    sp.fill(sp.m_super(49.0, 12.0, 2.0, 3.0, 3.0)[0], CHROME)
    sp.fill(sp.m_super(-28.0, 30.0, 1.4, 16.0, 4.0)[0], dark(TOW_W, 0.7))                           # exhaust stack
    _wheel(sp, -12.0, 10.0, 10.0, t, 0.0)
    _wheel(sp, 34.0, 10.0, 10.0, t, 0.0)
    sp.anchors.update(window=(4.0, 47.0), head=(4.0, 47.0))


def tow_bed(sp, t=0.0, tilt=0.0, chains=False, spin=0.0):
    """chassis + rear dual wheels + the flat deck (x -88 .. +82, front end at +82 next to the cab). tilt = degrees: the rear end
    goes DOWN to the street (a ramp) around the pivot (24, 20). anchors: deck_rear, deck_front, deck(u) helper points"""
    sp.fill(sp.m_super(0.0, 14.0, 80.0, 2.4, 6.0)[0], (50, 52, 70))                               # chassis rail
    a = math.radians(tilt)
    px, py = 24.0, 20.0
    def R(x, y):
        dx, dy = x - px, y - py
        return (px + dx * math.cos(a) - dy * math.sin(a), py + dx * math.sin(a) + dy * math.cos(a))
    deck = [R(-88.0, 19.0), R(82.0, 19.0), R(82.0, 26.0), R(-88.0, 26.0)]
    sp.poly(deck, tones(STEEL), val=np.full(DX.XC.shape, 0.55, np.float32))
    for q in range(-84, 80, 6): thin(sp, R(q, 25.4), R(q + 3.0, 25.4), dark(STEEL, 0.7), 0.3)       # tread plate
    for q in range(-84, 82, 14): thin(sp, R(q, 20.0), R(q, 25.0), dark(STEEL, 0.55), 0.25)
    sp.fill(sp.m_poly([R(-88.0, 19.0), R(-80.0, 19.0), R(-80.0, 26.0), R(-88.0, 26.0)]), TOW_O)      # orange rear end
    sp.sup(80.0, 32.0, 3.0, 8.0, tones(STEEL), n=4.0)                                                # headboard
    sp.ell(76.0, 30.0, 2.6, 2.6, tones((60, 60, 74)))                                                # winch drum
    if chains:
        for q in range(8): sp.blob(76.0 - q * 2.0, 31.0 - q * 0.3, 0.55, (180, 186, 200))
    for x in (-44.0, -26.0): _wheel(sp, x, 10.0, 10.0, t, -spin)
    sp.anchors.update(deck_rear=R(-86.0, 26.0), deck_front=R(70.0, 26.0))
    sp.tilt = tilt


def deck_point(u, tilt, px=24.0, py=20.0):
    """a point on the deck top (sprite px of tow_bed): u = 0 rear end .. 1 front end"""
    a = math.radians(tilt)
    x, y = -86.0 + u * 156.0, 26.0
    dx, dy = x - px, y - py
    return (px + dx * math.cos(a) - dy * math.sin(a), py + dx * math.sin(a) + dy * math.cos(a))


def sign_free(sp, t=0.0, glow=1.0):
    """the bait: a hand-painted A-frame board «FREE PARKING*» with a pink neon border (tiny asterisk!)"""
    sp.cap((-8.0, 0.0), (-6.0, 26.0), 0.8, 0.8, tones((120, 80, 50)))
    sp.cap((8.0, 0.0), (6.0, 26.0), 0.8, 0.8, tones((120, 80, 50)))
    board = sp.sup(0.0, 28.0, 14.0, 9.0, tones((252, 244, 220)), n=6.0)
    e = board & ~erode(erode(board))
    sp.fill(e, mix(PINK, (255, 255, 255), 0.25 * glow))
    sp.txt_box(['FREE', 'PARKING'], (-12.0, 21.0, 11.0, 36.0), (230, 40, 110), pad=0.4)
    sp.blob(11.4, 34.6, 0.7, (230, 40, 110))                                                         # the asterisk
    sp.anchors.update(star=(11.4, 34.6), board=(0.0, 28.0))


# ================================================================================ PARKING METER
def meter(sp, t=0.0, sticker=True, flag=True):
    sp.cap((0.0, 0.0), (0.0, 38.0), 1.4, 1.4, tones(METER))
    head = sp.sup(0.0, 46.0, 6.0, 8.6, tones(METER), n=2.6, gloss=1.0)
    win = sp.m_ell(0.0, 49.0, 4.0, 3.6)[0]
    sp.paint(win, [(200, 220, 230), (230, 244, 250), (255, 255, 255)], np.clip((DX.YC - 46) / 6.0, 0, 1), ol=False, stripes=False)
    if flag: sp.fill(sp.m_super(0.0, 49.6, 2.6, 1.2, 4.0)[0], (230, 40, 60))
    sp.fill(sp.m_super(0.0, 42.0, 1.6, 0.4, 4.0)[0], (40, 40, 50))                                  # coin slot
    if sticker:
        st = sp.m_super(0.0, 44.6, 5.4, 3.0, 6.0)[0]
        sp.fill(st, (255, 214, 60)); sp.fill(st & ~erode(st), (200, 120, 20))
        sp.txt_box(['PAY BY', 'APP ONLY'], (-5.2, 41.8, 5.2, 47.4), INK, pad=0.2)
    sp.star(-3.6, 52.6, 1.0)
    sp.anchors.update(slot=(0.0, 42.0), head=(0.0, 46.0))
