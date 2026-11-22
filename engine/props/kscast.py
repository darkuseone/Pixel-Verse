"""«Ключевой сотрудник» cast + props in the «Дневной свет» manner (props/kspix.py). Sprite px, feet anchor at (0, 0), x right =
facing side, y UP. Rim light + ink outline are added by kspix.Act / kspix.draw — the draw functions here do NOT outline.
  edik(sp, ...)    — Эдик Булкин, 41: «a pear on a matchstick» (narrow shoulders, a round belly, a thin neck), pale-mustard short-sleeve
                     shirt, a short wide brick-red tie, comb-over on a bald top, glasses pushed up on the forehead, a lanyard badge
                     and the TOILET KEY with a big wooden pear tag «WC» (the running gag); coat=True for the 17:59 coat + hat
  fikus(sp, ...)   — Фикус Аркадий: «an old watchman in a pot» — a stooped trunk, two top leaves = brows, a slit mouth in the bark,
                     one yellow leaf (grey hair), a chipped terracotta pot «НЕ ПОЛИВАТЬ ЧАЕМ»
  shef(sp, ...)    — Шеф Громов: «a wardrobe with a small head» — a square burgundy double-breasted jacket, a gold tie, a head 3x
                     narrower than the shoulders, a brush moustache, tan, slicked hair with grey temples, a headset, «РОЛЕКС-ШМОЛЕКС»
  lyuda(sp, ...)   — Людмила Степановна: a «?» with a beehive taller than she is, glasses on a chain, a lilac cardigan, mug «ЛЮДА»
  keyring / mug / briefcase — hand props"""
import math
import numpy as np
from props import dibspix as DX
from props.dibspix import dark, mix, erode, dilate, ik, EXPR
from props.kspix import tones, thin, stroke, INK, WHITE

# ---------------------------------------------------------------- palette
SKIN = (238, 188, 152)
SKIN_S = (206, 140, 104)            # shef: tanning-bed tan
SKIN_L = (240, 200, 176)            # lyuda: powder
SHIRT = (238, 222, 160)             # Эдик: washed mustard shirt
TIE = (178, 72, 54)
TROUS = (112, 96, 76)
SHOE = (52, 40, 36)
HAIR_E = (120, 92, 62)
LANY = (52, 96, 200)
BADGE = (250, 250, 244)
PEAR = (176, 120, 64)               # wooden pear tag of the WC key
BRASS = (222, 186, 84)
COAT = (96, 104, 112)               # Эдик's grey coat
HAT = (70, 64, 60)
SUIT = (128, 34, 52)                # shef burgundy jacket
SUIT_D = (86, 22, 36)
GOLD = (240, 196, 70)
SHIRT_W = (244, 244, 238)
HAIR_S = (40, 34, 34)
GREY = (176, 176, 170)
LEAF = (56, 128, 64)
LEAF_D = (34, 88, 44)
LEAF_Y = (214, 190, 70)
BARK = (128, 92, 60)
POT = (196, 98, 58)
CARDI = (178, 150, 206)             # lyuda lilac cardigan
SKIRT = (84, 70, 96)
HIVE = (150, 84, 50)                # auburn beehive
MUG = (248, 248, 240)

XTRA = dict(
    proud=dict(eo=0.9, pu=0.6, bt=-0.15, bl=0.35, mo=0.0, mc=0.85, lid=0.15),
    beam=dict(eo=1.1, pu=0.62, bt=-0.35, bl=0.55, mo=0.7, mc=1.0),
    scheme=dict(eo=0.6, pu=0.55, bt=0.5, bl=-0.1, mo=0.0, mc=0.7, lid=0.4),
    hopeful=dict(eo=1.05, pu=0.68, bt=-0.5, bl=0.45, mo=0.0, mc=0.55),
    shock=dict(eo=1.4, pu=0.3, bt=-0.65, bl=0.85, mo=0.8, mc=0.0),
    crushed=dict(eo=0.8, pu=0.62, bt=-0.75, bl=0.15, mo=0.0, mc=-0.7, lid=0.3),
    sleepy=dict(eo=0.35, pu=0.6, bt=-0.1, bl=0.0, mo=0.15, mc=-0.1, lid=0.75),
    panic=dict(eo=1.45, pu=0.28, bt=-0.85, bl=0.95, mo=0.95, mc=-0.2),
    deadpan=dict(eo=0.65, pu=0.6, bt=0.0, bl=0.0, mo=0.0, mc=-0.05, lid=0.55),
    boss=dict(eo=0.8, pu=0.55, bt=0.25, bl=0.1, mo=0.0, mc=0.9, lid=0.25),
    bark=dict(eo=1.0, pu=0.45, bt=0.7, bl=-0.2, mo=0.9, mc=-0.1),
    sweet=dict(eo=0.7, pu=0.6, bt=-0.3, bl=0.3, mo=0.0, mc=0.95, lid=0.35),
    pleading=dict(eo=1.15, pu=0.72, bt=-0.8, bl=0.5, mo=0.2, mc=-0.35),
    strict=dict(eo=0.6, pu=0.55, bt=0.45, bl=-0.25, mo=0.0, mc=-0.3, lid=0.45),
    smirk=dict(eo=0.6, pu=0.6, bt=0.3, bl=0.0, mo=0.0, mc=0.6, lid=0.5),
)


def X(expr):
    if isinstance(expr, dict): return dict(expr)
    return dict(XTRA.get(expr) or EXPR.get(expr, EXPR['normal']))


# ================================================================================ hand props
def keyring(sp, h, n=14, swing=0.0, tag=True):
    """the caretaker's bunch: a big brass ring, a fan of keys, a cardboard tag «ЗАВХОЗ»"""
    x, y = h
    ring = sp.m_ell(x, y - 3.0, 3.2, 3.2)[0] & ~sp.m_ell(x, y - 3.0, 2.3, 2.3)[0]
    sp.fill(ring, BRASS)
    for i in range(n):
        a = -math.pi / 2 + (i - (n - 1) / 2) * 0.17 + swing
        b0 = (x + math.cos(a) * 3.0, y - 3.0 + math.sin(a) * 3.0)
        b1 = (x + math.cos(a) * 8.6, y - 3.0 + math.sin(a) * 8.6)
        c = (BRASS, (190, 196, 204), (160, 120, 70))[i % 3]
        thin(sp, b0, b1, c, 0.42)
        sp.blob(b0[0], b0[1], 0.62, c)
        thin(sp, (b1[0] - 0.6, b1[1]), (b1[0] + 0.4, b1[1] - 0.8), dark(c, 0.7), 0.24)
    if tag:
        ta = -math.pi / 2 + 0.95 + swing
        tx, ty = x + math.cos(ta) * 9.0, y - 3.0 + math.sin(ta) * 9.0
        thin(sp, (x + 2.2, y - 4.6), (tx, ty + 1.8), (230, 230, 220), 0.2)
        sp.sup(tx + 1.0, ty - 0.6, 4.6, 2.2, tones((236, 214, 160)), n=5.0, stripes=False)
        sp.txt_box(['ЗАВХОЗ'], (tx - 3.4, ty - 2.6, tx + 5.4, ty + 1.4), (150, 40, 40), pad=0.2)
    sp.anchors['keys'] = (x, y - 6.0)


def mug(sp, h, label='', tea=True):
    x, y = h
    sp.sup(x + 1.0, y + 1.6, 2.4, 3.0, tones(MUG), n=4.0)
    ring = sp.m_ell(x + 3.6, y + 1.8, 1.6, 1.7)[0] & ~sp.m_ell(x + 3.6, y + 1.8, 0.9, 1.0)[0]
    sp.fill(ring, dark(MUG, 0.8))
    if tea: sp.fill(sp.m_ell(x + 1.0, y + 4.4, 2.0, 0.6)[0], (150, 92, 40))
    if label: sp.txt_box([label], (x - 1.2, y + 0.2, x + 3.2, y + 3.0), (200, 40, 60), pad=0.1)
    sp.anchors['mug'] = (x + 1.0, y + 4.6)


def briefcase(sp, h):
    x, y = h
    sp.sup(x, y - 6.0, 6.4, 4.6, tones((84, 50, 36)), n=4.0)
    thin(sp, (x - 6.0, y - 6.0), (x + 6.0, y - 6.0), (60, 34, 24), 0.3)
    sp.blob(x, y - 2.0, 0.8, GOLD)
    ring = sp.m_ell(x, y - 0.6, 2.2, 1.6)[0] & ~sp.m_ell(x, y - 0.6, 1.4, 0.9)[0] & (DX.YC > y - 1.2)
    sp.fill(ring, (60, 34, 24))


def wc_key(sp, a, scale=1.0, swing=0.0):
    """the toilet key on the lanyard: brass key + a big wooden pear «WC»; a = ring point"""
    x, y = a
    s = scale
    ang = -math.pi / 2 + swing
    kx, ky = x + math.cos(ang) * 4.0 * s, y + math.sin(ang) * 4.0 * s
    thin(sp, (x, y), (kx, ky), BRASS, 0.36 * s)
    thin(sp, (kx - 0.8 * s, ky + 0.8 * s), (kx + 0.4 * s, ky + 0.6 * s), BRASS, 0.3 * s)
    px_, py_ = x + 2.4 * s + math.cos(ang) * 1.6 * s, y + math.sin(ang) * 1.6 * s - 1.2 * s
    pr = sp.union([sp.m_ell(px_, py_ - 3.2 * s, 2.6 * s, 2.8 * s), sp.m_ell(px_, py_ - 0.6 * s, 1.6 * s, 1.8 * s)], tones(PEAR))
    sp.txt_box(['WC'], (px_ - 2.2 * s, py_ - 5.0 * s, px_ + 2.2 * s, py_ - 1.6 * s), (250, 240, 210), pad=0.05)
    sp.anchors['wc'] = (px_, py_ - 2.6 * s)


# ================================================================================ ЭДИК
def edik(sp, t=0.0, expr='proud', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
         legs=True, ox=0.0, oy=0.0, glasses=1.0, sweat=0.0, walk=None, lean=0.0, coat=False, hat=False, stubble_=0.0,
         key_swing=None, tie_up=0.0, crumple=0.0, young=False):
    """ЭДИК. coat=True — the grey coat over the shirt (17:59), hat=True — a knitted hat; stubble_ 0..1 (the morning after);
    key_swing — angle of the WC key (default: a slow sway)"""
    E = X(expr)
    if blink is None: blink = ((t + 1.1) % 4.3) < 0.12
    br = 0.35 * math.sin(t * 2.0)
    bob = abs(math.sin(walk)) * 1.0 if walk is not None else 0.0
    def Q(x, y): return (x + ox + lean * (y / 60.0) * 5.0, y + oy + (bob if y > 10 else 0.3 * bob))
    swing = math.sin(walk) * 4.0 if walk is not None else 0.0
    top_c = COAT if coat else SHIRT
    # ---------------------------------------------------------------- far arm
    shF = Q(-8.0, 52.0 + br * 0.3)
    hf = hand_f if hand_f is not None else Q(-13.5 - swing * 0.6, 32.0)
    kF, eF = ik(shF, hf, 9.0, 8.5, -1.0)
    sp.cap(shF, kF, 3.2, 2.8, tones(dark(top_c, 0.84)))
    sp.cap(kF, eF, 2.2 if not coat else 2.8, 1.9, tones(dark(SKIN if not coat else COAT, 0.86)))
    sp.ell(eF[0], eF[1] - 0.3, 2.3, 2.2, tones(dark(SKIN, 0.86)))
    if prop_f: prop_f(sp, eF)
    sp.anchors['hand_f'] = eF
    # ---------------------------------------------------------------- legs: short, trousers pulled up over the belly
    if legs:
        sw = math.sin(walk) * 2.6 if walk is not None else 0.0
        for k_, dx in enumerate((-3.6, 3.6)):
            near = k_ == 1
            s_ = sw if near else -sw
            fx_, fy_ = dx + s_ * 0.7, 2.4 + max(0.0, s_) * 0.5
            c = TROUS if near else dark(TROUS, 0.86)
            sp.cap(Q(dx * 0.9, 25.0), (fx_ + ox, fy_ + 2.6 + oy), 3.2, 2.6, tones(c))
            sp.sup(fx_ + 1.6 + ox, fy_ + oy, 4.0, 1.9, tones(SHOE if near else dark(SHOE, 0.85)), n=2.4, gloss=0.6)
    # ---------------------------------------------------------------- the pear: belly + narrow shoulders
    cx_ = Q(0.0, 0)[0]
    belly = sp.m_ell(*Q(0.6, 34.0), 15.0, 13.0)
    chest = sp.m_super(*Q(0.0, 49.0), 9.2, 8.0, 2.6)
    body = sp.union([belly, chest], tones(top_c))
    if coat:                                                            # open coat: the shirt + tie show in a V
        vx = [Q(-2.6, 56.0), Q(4.4, 56.0), Q(1.0, 22.0)]
        shirt_m = sp.m_poly(vx) & body
        sp.paint(shirt_m, tones(SHIRT), DX.lit(np.clip((DX.XC - cx_) / 10.0, -0.9, 0.9), np.clip((DX.YC - Q(0, 40)[1]) / 14.0, -0.9, 0.9)))
        for a, b in ((vx[0], vx[2]), (vx[1], vx[2])): thin(sp, a, b, dark(COAT, 0.55), 0.3)
        for q in range(3): sp.blob(*Q(-5.0, 46.0 - q * 7.0), 0.7, (40, 40, 44))
    else:
        for q in range(4): sp.dot(*Q(1.0, 50.0 - q * 6.0), (214, 200, 140))                        # shirt buttons
        thin(sp, Q(-12.6, 28.0), Q(-9.0, 26.0), dark(SHIRT, 0.75), 0.24)                            # belly crease
        sp.fill(sp.m_super(*Q(-4.6, 49.0), 2.0, 1.6, 4.0)[0] & body, dark(SHIRT, 0.86))           # pocket
        for q in range(3): thin(sp, Q(-5.6 + q * 0.9, 50.6), Q(-5.6 + q * 0.9, 52.2), ((40, 60, 160), (200, 40, 40), (30, 30, 30))[q], 0.18)
    sp.fill(sp.m_super(*Q(0.6, 21.6), 13.6, 1.3, 6.0)[0], (60, 42, 32))                            # belt under the belly
    sp.blob(*Q(1.6, 21.6), 0.9, BRASS)
    # tie: short and wide, lies on the belly (tie_up lifts the tip — a gust / panic)
    tie = sp.m_poly([Q(0.0, 56.0), Q(2.0, 56.0), Q(4.2, 40.0 + tie_up), Q(1.0, 37.0 + tie_up * 1.4), Q(-2.2, 40.0 + tie_up)])
    sp.paint(tie, tones(TIE), DX.lit(np.clip((DX.XC - Q(1, 0)[0]) / 4.0, -0.9, 0.9), np.full(DX.XC.shape, 0.3, np.float32)))
    for q in range(3): thin(sp, Q(-1.0, 52.0 - q * 4.0), Q(3.2, 50.0 - q * 4.0), dark(TIE, 0.7), 0.22, mask=tie)
    sp.sup(*Q(1.0, 56.2), 1.8, 1.4, tones(TIE), n=3.0)                                               # knot
    # ---------------------------------------------------------------- neck + head (an egg with a comb-over)
    sp.cap(Q(1.2, 56.0), Q(1.6, 60.6), 2.0, 2.0, tones(dark(SKIN, 0.9)))
    hx, hy = Q(2.0, 68.0)
    head = sp.union([sp.m_ell(hx, hy, 7.0, 8.4), sp.m_ell(hx + 0.6, hy - 4.6, 6.4, 4.4)], tones(SKIN), gloss=0.0)
    sp.ell(hx - 5.6, hy + 0.2, 1.5, 2.3, tones(dark(SKIN, 0.92)))                                     # ear
    thin(sp, (hx - 5.6, hy + 1.2), (hx - 5.4, hy - 0.8), dark(SKIN, 0.7), 0.2)
    sp.glint(hx - 0.8, hy + 7.0, 0.6)                                                                  # bald-spot shine
    # side fringe + the famous comb-over: three strands across the bald top
    if young:                                                                                         # 17 years ago: a full mop of hair
        sp.union([sp.m_ell(hx - 0.2, hy + 6.0, 7.6, 4.2), sp.m_ell(hx - 4.6, hy + 2.6, 2.6, 4.2), sp.m_ell(hx + 4.6, hy + 7.0, 3.4, 2.0)],
                 tones(dark(HAIR_E, 0.9)), exclude=head & (DX.YC < hy + 4.4) & (DX.XC > hx - 3.6))
    sp.fill(sp.m_super(hx - 4.8, hy + 2.6, 1.6, 3.4, 3.0)[0] & head, HAIR_E)
    for q in range(0 if young else 3):
        y0 = hy + 4.8 + q * 1.3
        thin(sp, (hx - 6.2, y0 - 1.6), (hx + 1.0, y0 + 1.2), HAIR_E, 0.3)
        thin(sp, (hx + 1.0, y0 + 1.2), (hx + 5.0, y0 + 0.2 - q * 0.4), HAIR_E, 0.26)
    if stubble_ > 0: DX.stubble(sp, sp.m_ell(hx + 1.8, hy - 5.6, 5.6, 2.6)[0] & head, dark(SKIN, 0.66), 0.28 * stubble_, 5)
    lx, ly = look
    DX.eye(sp, hx + 3.4, hy + 0.8, 3.8, 3.8, E, (90, 120, 70), (lx, ly), blink, lash=INK, skin=SKIN, bold=1, bag=dark(SKIN, 0.82))
    DX.eye(sp, hx - 1.4, hy + 0.8, 3.2, 3.6, E, (90, 120, 70), (lx, ly), blink, lash=INK, skin=SKIN, bold=1)
    DX.brow(sp, hx + 3.4, hy + 4.2, 3.8, E, +1, HAIR_E, th=1.4)
    DX.brow(sp, hx - 1.4, hy + 4.1, 3.2, E, -1, HAIR_E, th=1.4)
    if glasses > 0 and not young:                                                                      # glasses pushed up on the forehead
        gy = hy + 6.8
        for gx, r in ((hx + 3.6, 2.0), (hx - 1.2, 1.7)):
            rr = sp.m_ell(gx, gy, r, r * 0.8)[0] & ~sp.m_ell(gx, gy, r - 0.55, r * 0.8 - 0.55)[0]
            sp.fill(rr, (60, 52, 46))
        thin(sp, (hx + 1.6, gy), (hx + 0.5, gy), (60, 52, 46), 0.25)
        sp.glint(hx + 3.0, gy + 0.6, 0.35)
    sp.ell(hx + 6.8, hy - 1.6, 2.0, 2.2, tones(dark(SKIN, 0.98)), gloss=1.0)                           # round nose
    sp.dot(hx + 6.4, hy - 3.2, dark(SKIN, 0.6))
    DX.blush(sp, hx + 2.0, hy - 2.0, 1.3, 0.8, (236, 120, 110))
    mx, my = hx + 3.2, hy - 5.0
    DX.mouth(sp, mx, my, 4.6, E, mouth_, (160, 80, 70), inside=(96, 26, 36), teeth=(255, 255, 250), skin=SKIN, maxh=5.4)
    thin(sp, (hx - 1.0, hy - 8.2), (hx + 4.6, hy - 8.6), dark(SKIN, 0.8), 0.2)                         # double chin
    if hat:
        sp.union([sp.m_ell(hx + 0.4, hy + 6.2, 7.6, 4.4)], tones(HAT))
        sp.sup(hx + 0.4, hy + 3.0, 7.8, 1.4, tones(dark(HAT, 0.8)), n=4.0)
        sp.blob(hx + 0.4, hy + 11.0, 1.6, (200, 60, 50))
    if sweat > 0:
        for i, (x, y) in enumerate(((hx + 5.0, hy + 4.0), (hx - 2.0, hy + 5.0))[:int(1 + sweat)]):
            yy = y - ((t * 3.5 + i * 1.3) % 3.0)
            sp.ell(x, yy, 0.6, 1.0, tones((170, 220, 255)), ol=False)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 1.0, hy + 0.8), chest=Q(1.0, 46.0))
    # lanyard + badge + the WC key
    if not coat or True:
        thin(sp, Q(-2.2, 57.0), Q(-3.6, 44.0), LANY, 0.4)
        thin(sp, Q(4.0, 57.0), Q(-2.6, 44.0), LANY, 0.4)
        bd = sp.sup(*Q(-3.0, 40.6), 2.6, 3.4, tones(BADGE), n=5.0, stripes=False)
        sp.fill(sp.m_super(*Q(-3.0, 41.8), 1.4, 1.2, 4.0)[0], (120, 150, 200))                       # photo
        sp.fill(sp.m_super(*Q(-3.0, 38.4), 1.8, 0.35, 8.0)[0], (60, 60, 70))
        ks = key_swing if key_swing is not None else 0.25 * math.sin(t * 1.6)
        wc_key(sp, Q(-2.0, 44.2), 1.0, ks)
    # ---------------------------------------------------------------- near arm
    before = sp.m.copy()
    shN = Q(9.0, 52.0 + br * 0.3)
    hn = hand_n if hand_n is not None else Q(14.0 + swing * 0.6, 31.0)
    kN, eN = ik(shN, hn, 9.0, 8.5, -1.0)
    sp.cap(shN, kN, 3.4, 3.0, tones(top_c))
    if not coat: sp.cap(kN, eN, 2.2, 1.9, tones(SKIN))
    else: sp.cap(kN, eN, 2.8, 2.2, tones(COAT))
    if prop_n and getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.ell(eN[0], eN[1] - 0.3, 2.4, 2.3, tones(SKIN))
    if prop_n and not getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m & before
    sp.col[o] = INK


# ================================================================================ ФИКУС АРКАДИЙ
def fikus(sp, t=0.0, expr='deadpan', mouth_=0.0, look=(0.0, 0.0), blink=None, leaves=1.0, garland=False, medal=False, wet=0.0, pot=True):
    """ФИКУС АРКАДИЙ: brows = the two top leaves (bt raises/frowns them), the mouth = a slit in the bark (mouth_ opens it).
    garland=True — a blinking garland (E03), medal=True — the «СОТРУДНИК ГОДА» medal (E06)"""
    E = X(expr)
    talk = max(mouth_, E['mo'] * 0.6)
    wob = 0.4 * math.sin(t * 1.3) + talk * 0.8 * math.sin(t * 31)
    if pot:
        pt = sp.union([sp.m_super(0.0, 7.0, 9.6, 7.0, 3.0), sp.m_super(0.0, 14.2, 10.8, 1.8, 6.0)], tones(POT))
        chip = sp.m_poly([(5.6, 16.4), (9.0, 16.4), (8.0, 13.4)])
        sp.col[chip & pt] = dark(POT, 0.62)
        sp.fill(sp.m_super(0.0, 15.6, 9.6, 0.6, 6.0)[0], (70, 48, 34))                              # soil
        sp.fill(sp.m_super(0.0, 6.6, 7.6, 2.8, 6.0)[0], (240, 228, 196))                              # paper label
        sp.txt_box(['НЕ ПОЛИВАТЬ', 'ЧАЕМ'], (-7.4, 4.0, 7.4, 9.2), (40, 30, 26), pad=0.2, lead=0.2)
        if medal:
            thin(sp, (-3.0, 14.0), (0.0, 9.0), (200, 40, 40), 0.5); thin(sp, (3.0, 14.0), (0.0, 9.0), (40, 80, 200), 0.5)
            sp.ell(0.0, 7.0, 2.6, 2.6, tones(GOLD), gloss=1.0)
    # trunk: a stooped watchman's back
    tr = [(0.0, 15.0), (-1.6, 24.0), (-0.6, 33.0), (1.4, 41.0)]
    for a, b in zip(tr[:-1], tr[1:]): sp.cap(a, b, 2.6, 2.2, tones(BARK))
    for q in range(5): thin(sp, (-1.6 + (q % 2) * 1.6, 17.0 + q * 4.6), (-0.6 + (q % 2) * 1.6, 18.4 + q * 4.6), dark(BARK, 0.65), 0.2)
    # leaves: crown behind / around the face
    rng = np.random.default_rng(5)
    LV = [(-7.0, 46.0, -0.5), (8.0, 47.0, 0.4), (-10.0, 39.0, -0.9), (10.6, 39.4, 0.9), (-4.0, 53.0, -0.2), (4.6, 54.0, 0.25),
          (0.4, 58.0, 0.0), (-12.0, 31.0, -1.2), (12.4, 31.6, 1.2), (-8.4, 26.0, -1.5), (9.2, 25.4, 1.45)]
    for i, (x, y, a) in enumerate(LV):
        sway = 0.06 * math.sin(t * 1.1 + i) * leaves + (0.05 * talk * math.sin(t * 29 + i))
        c = LEAF_Y if i == 3 else (LEAF if i % 2 else dark(LEAF, 0.9))
        ang = a + sway
        m, nx, ny = sp.m_ell(x, y, 5.2, 2.4, ang)
        sp.paint(m, tones(c), DX.lit(nx, ny))
        thin(sp, (x - math.cos(ang) * 4.2, y - math.sin(ang) * 4.2), (x + math.cos(ang) * 4.2, y + math.sin(ang) * 4.2), dark(c, 0.62), 0.18)
        thin(sp, (x * 0.15, 41.0 + (y - 41.0) * 0.2), (x - math.cos(ang) * 4.0 * np.sign(x or 1), y - math.sin(ang) * 4.0 * np.sign(x or 1)),
             dark(BARK, 0.8), 0.22)
    # the face on the upper trunk: a bark «forehead», brow-leaves, watchman eyes, a knot nose, a slit mouth
    fx, fy = 1.0 + wob * 0.2, 37.0
    sp.sup(fx, fy, 5.8, 8.0, tones(BARK), n=2.2)
    for q in range(3): thin(sp, (fx - 3.6, fy + 4.4 + q * 1.0), (fx + 3.4, fy + 4.0 + q * 1.0), dark(BARK, 0.66), 0.16)
    bt = E['bt']
    for side in (-1, 1):                                                                                # brow leaves
        bx, by = fx + side * 2.6, fy + 3.6 + E['bl'] * 1.0
        ang = side * (0.30 + bt * 0.55) + (0.12 * talk * math.sin(t * 23) * side)
        m, nx, ny = sp.m_ell(bx + side * 2.8, by, 4.4, 1.5, ang)
        sp.paint(m, tones(LEAF_D), DX.lit(nx, ny))
    lx, ly = look
    DX.eye(sp, fx + 2.2, fy + 1.0, 2.8, 2.6, E, (70, 52, 30), (lx, ly), blink, lash=(36, 24, 16), skin=BARK, bold=1)
    DX.eye(sp, fx - 2.0, fy + 1.0, 2.6, 2.6, E, (70, 52, 30), (lx, ly), blink, lash=(36, 24, 16), skin=BARK, bold=1)
    sp.ell(fx + 0.6, fy - 1.4, 1.4, 1.5, tones(dark(BARK, 1.12)))                                            # knot nose
    mx, my = fx + 0.4, fy - 4.4
    mo = max(talk, 0.0)
    if mo > 0.08:
        mm = sp.m_ell(mx, my, 2.8, 0.5 + 2.0 * mo)[0]
        sp.fill(mm, (46, 24, 18)); sp.fill(mm & (DX.YC < my - 0.8 * mo), (150, 70, 60))
    else:
        thin(sp, (mx - 2.6, my + E['mc'] * 0.7), (mx, my), (50, 30, 20), 0.3)
        thin(sp, (mx, my), (mx + 2.6, my + E['mc'] * 0.7), (50, 30, 20), 0.3)
    if garland:
        cols = ((255, 60, 60), (60, 220, 90), (255, 214, 60), (70, 140, 255))
        for i in range(14):
            u = i / 13.0
            x, y = -12 + 24 * u, 28 + 22 * u + 3.0 * math.sin(u * 9)
            on = (int(t * 4) + i) % 3 != 0
            sp.blob(x, y, 0.9, cols[i % 4] if on else dark(cols[i % 4], 0.45), keep=on)
    if wet > 0:
        for i in range(3):
            yy = 50 - ((t * 3.0 + i * 0.3) % 1.0) * 30.0
            sp.blob(-6 + i * 6, yy, 0.5, (160, 100, 50))
    sp.anchors.update(head=(fx, fy), mouth=(mx, my), eyes=(fx, fy + 2.0))


# ================================================================================ ШЕФ ГРОМОВ
def shef(sp, t=0.0, expr='boss', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
         legs=True, ox=0.0, oy=0.0, coat=False, walk=None, hat_dm=False):
    """ШЕФ ГРОМОВ. coat=True — a long black coat over the jacket (going home); hat_dm — a Ded Moroz hat (E03)"""
    E = X(expr)
    if blink is None: blink = ((t + 2.4) % 4.9) < 0.13
    br = 0.3 * math.sin(t * 1.6)
    bob = abs(math.sin(walk)) * 1.2 if walk is not None else 0.0
    def Q(x, y): return (x + ox, y + oy + (bob if y > 10 else 0.3 * bob))
    swing = math.sin(walk) * 4.0 if walk is not None else 0.0
    jc = (44, 40, 46) if coat else SUIT
    shF = Q(-17.0, 64.0 + br)
    hf = hand_f if hand_f is not None else Q(-21.0 - swing * 0.5, 38.0)
    kF, eF = ik(shF, hf, 11.0, 10.0, -1.0)
    sp.cap(shF, kF, 5.0, 4.4, tones(dark(jc, 0.8)))
    sp.cap(kF, eF, 4.0, 3.4, tones(dark(jc, 0.8)))
    sp.ell(eF[0], eF[1] - 0.4, 3.2, 3.0, tones(dark(SKIN_S, 0.85)))
    if prop_f: prop_f(sp, eF)
    sp.anchors['hand_f'] = eF
    if legs:
        sw = math.sin(walk) * 2.4 if walk is not None else 0.0
        for k_, dx in enumerate((-6.0, 6.0)):
            near = k_ == 1
            s_ = sw if near else -sw
            c = (40, 36, 44) if near else (30, 28, 34)
            sp.cap(Q(dx, 30.0), (dx + s_ * 0.7 + ox, 4.0 + oy), 5.0, 4.2, tones(c))
            sp.sup(dx + 2.4 + s_ * 0.7 + ox, 1.8 + oy, 5.8, 2.2, tones((24, 20, 22)), n=2.4, gloss=1.0)
    # the wardrobe: square torso, belly pushed forward
    tor = sp.union([sp.m_super(*Q(0.0, 50.0), 19.0, 20.0, 4.4), sp.m_ell(*Q(5.0, 40.0), 16.0, 12.0)], tones(jc))
    vx = [Q(-2.0, 70.0), Q(8.0, 70.0), Q(3.0, 52.0)]
    sh = sp.m_poly(vx) & tor
    sp.paint(sh, tones(SHIRT_W), None)
    tie = sp.m_poly([Q(2.0, 69.0), Q(4.2, 69.0), Q(5.6, 53.0), Q(3.1, 50.0), Q(0.8, 53.0)]) & tor
    sp.paint(tie, tones(GOLD), DX.lit(np.clip((DX.XC - Q(3, 0)[0]) / 3.0, -0.9, 0.9), np.full(DX.XC.shape, 0.3, np.float32)), gloss=0.6)
    for a, b in ((vx[0], vx[2]), (vx[1], vx[2])): thin(sp, a, b, dark(jc, 0.5), 0.36)
    if not coat:
        for r in range(3):
            for c_ in (-4.0, 7.0): sp.blob(*Q(c_, 46.0 - r * 6.0), 0.8, GOLD)                    # double-breasted gold buttons
        sp.fill(sp.m_super(*Q(-10.0, 58.0), 3.2, 1.0, 5.0)[0] & tor, dark(jc, 0.7))                # breast pocket
        thin(sp, Q(-11.6, 58.8), Q(-8.4, 59.6), WHITE, 0.4)
    else:
        sp.fill(sp.m_super(*Q(-4.0, 66.0), 5.0, 3.0, 3.0)[0] & tor, (70, 66, 74))                  # coat collar
        sp.fill(sp.m_super(*Q(10.0, 66.0), 5.0, 3.0, 3.0)[0] & tor, (70, 66, 74))
    # small head straight on the shoulders
    hx, hy = Q(3.0, 77.0)
    sp.cap(Q(3.0, 68.0), Q(3.0, 72.0), 3.6, 3.6, tones(dark(SKIN_S, 0.9)))
    head = sp.union([sp.m_ell(hx, hy, 5.8, 6.6), sp.m_ell(hx + 0.6, hy - 3.6, 5.6, 3.6)], tones(SKIN_S))
    sp.ell(hx - 4.8, hy + 0.2, 1.2, 1.9, tones(dark(SKIN_S, 0.92)))
    sp.fill(sp.m_super(hx - 4.9, hy + 0.2, 0.7, 1.0, 3.0)[0], (30, 30, 34))                       # headset earpiece
    thin(sp, (hx - 4.6, hy - 0.6), (hx + 1.4, hy - 4.0), (30, 30, 34), 0.2)
    DX.stubble(sp, sp.m_ell(hx + 1.4, hy - 4.0, 5.0, 2.6)[0] & head, dark(SKIN_S, 0.72), 0.35, 9)
    lx, ly = look
    DX.eye(sp, hx + 2.6, hy + 0.6, 3.4, 3.2, E, (70, 46, 30), (lx, ly), blink, lash=INK, skin=SKIN_S, bold=1)
    DX.eye(sp, hx - 1.4, hy + 0.6, 3.0, 3.0, E, (70, 46, 30), (lx, ly), blink, lash=INK, skin=SKIN_S, bold=1)
    DX.brow(sp, hx + 2.6, hy + 4.0, 3.2, E, +1, HAIR_S, th=1.2, bushy=True)
    DX.brow(sp, hx - 1.4, hy + 3.9, 2.8, E, -1, HAIR_S, th=1.2, bushy=True)
    sp.ell(hx + 5.4, hy - 1.0, 1.6, 1.8, tones(dark(SKIN_S, 0.98)), gloss=1.0)
    mx, my = hx + 2.6, hy - 3.8
    DX.mouth(sp, mx, my, 4.0, E, mouth_, (120, 60, 50), inside=(84, 20, 30), teeth=(255, 255, 250), skin=SKIN_S, maxh=4.4)
    sp.union([sp.m_super(mx, my + 1.4, 3.6, 1.0, 3.0)], tones(HAIR_S))                              # brush moustache
    for q in range(5): thin(sp, (mx - 3.0 + q * 1.4, my + 2.2), (mx - 3.2 + q * 1.4, my + 0.6), (70, 64, 64), 0.16)
    if hat_dm:
        sp.union([sp.m_poly([(hx - 6.4, hy + 3.4), (hx + 6.4, hy + 3.4), (hx - 4.0, hy + 13.0)])], tones((220, 40, 40)))
        sp.sup(hx, hy + 3.4, 6.8, 1.4, tones(WHITE), n=3.0)
        sp.blob(hx - 4.2, hy + 13.2, 1.5, WHITE)
    else:
        hair = sp.union([sp.m_ell(hx - 0.4, hy + 5.0, 6.0, 2.6), sp.m_ell(hx - 3.6, hy + 2.6, 2.6, 3.0)], tones(HAIR_S),
                        exclude=head & (DX.YC < hy + 4.0) & (DX.XC > hx - 3.0))
        sp.fill(sp.m_ell(hx - 4.0, hy + 1.4, 1.2, 1.8)[0] & hair, GREY)                             # grey temples
        thin(sp, (hx - 3.0, hy + 6.2), (hx + 4.0, hy + 5.6), (90, 86, 90), 0.2, mask=hair)        # comb lines
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 0.8, hy + 0.8), chest=Q(2.0, 52.0))
    before = sp.m.copy()
    shN = Q(17.0, 64.0 + br)
    hn = hand_n if hand_n is not None else Q(22.0 + swing * 0.5, 38.0)
    kN, eN = ik(shN, hn, 11.0, 10.0, -1.0)
    sp.cap(shN, kN, 5.2, 4.6, tones(jc))
    sp.cap(kN, eN, 4.2, 3.6, tones(jc))
    w_ = (kN[0] + (eN[0] - kN[0]) * 0.86, kN[1] + (eN[1] - kN[1]) * 0.86)
    sp.ell(w_[0], w_[1], 2.0, 1.3, tones(GOLD), gloss=1.0)                                            # «Ролекс-Шмолекс»
    if prop_n and getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.ell(eN[0], eN[1] - 0.4, 3.4, 3.2, tones(SKIN_S))
    if prop_n and not getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m & before
    sp.col[o] = INK


# ================================================================================ ЛЮДМИЛА СТЕПАНОВНА
def lyuda(sp, t=0.0, expr='strict', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
          legs=True, ox=0.0, oy=0.0, glasses_on=True, walk=None):
    """ЛЮДМИЛА СТЕПАНОВНА: straight as a ruler, a beehive above everyone, glasses on a chain"""
    E = X(expr)
    if blink is None: blink = ((t + 0.4) % 5.1) < 0.12
    br = 0.25 * math.sin(t * 1.5)
    def Q(x, y): return (x + ox, y + oy)
    shF = Q(-6.5, 48.0 + br)
    hf = hand_f if hand_f is not None else Q(-8.0, 30.0)
    kF, eF = ik(shF, hf, 8.0, 8.0, -1.0)
    sp.cap(shF, kF, 2.6, 2.2, tones(dark(CARDI, 0.82)))
    sp.cap(kF, eF, 2.2, 1.8, tones(dark(CARDI, 0.82)))
    sp.ell(eF[0], eF[1] - 0.3, 1.9, 1.8, tones(dark(SKIN_L, 0.86)))
    if prop_f: prop_f(sp, eF)
    sp.anchors['hand_f'] = eF
    if legs:
        for k_, dx in enumerate((-2.2, 2.4)):
            c = (200, 170, 150) if k_ else (176, 150, 132)                                            # tights
            sp.cap(Q(dx, 16.0), Q(dx, 3.0), 1.8, 1.4, tones(c))
            sp.sup(*Q(dx + 1.4, 1.4), 3.0, 1.4, tones((90, 40, 50)), n=2.4, gloss=0.6)
    skirt = sp.poly([Q(-6.8, 30.0), Q(7.6, 30.0), Q(8.8, 14.0), Q(-7.6, 14.0)], tones(SKIRT), val=None)
    tor = sp.union([sp.m_super(*Q(0.4, 39.0), 7.6, 11.0, 3.4)], tones(CARDI))
    for q in range(5): sp.blob(*Q(0.8, 46.0 - q * 3.6), 0.55, (240, 236, 250))
    for yy in range(31, 50, 2): thin(sp, Q(-6.6, yy), Q(-5.0, yy), dark(CARDI, 0.78), 0.14, mask=tor)  # knit
    sp.fill(sp.m_poly([Q(-1.4, 50.0), Q(3.0, 50.0), Q(0.8, 46.6)]) & tor, (250, 250, 250))           # collar
    hx, hy = Q(1.4, 57.0)
    sp.cap(Q(1.0, 49.0), Q(1.2, 52.0), 1.8, 1.8, tones(dark(SKIN_L, 0.9)))
    head = sp.union([sp.m_ell(hx, hy, 5.4, 6.6), sp.m_ell(hx + 0.4, hy - 3.4, 4.8, 3.4)], tones(SKIN_L))
    lx, ly = look
    DX.eye(sp, hx + 2.6, hy + 0.6, 3.0, 2.8, E, (90, 70, 110), (lx, ly), blink, lash=INK, skin=SKIN_L, bold=1, flick=True)
    DX.eye(sp, hx - 1.2, hy + 0.6, 2.6, 2.6, E, (90, 70, 110), (lx, ly), blink, lash=INK, skin=SKIN_L, bold=1)
    DX.brow(sp, hx + 2.6, hy + 3.6, 3.0, E, +1, (110, 60, 40), th=1.0, arch=1.4)
    DX.brow(sp, hx - 1.2, hy + 3.5, 2.6, E, -1, (110, 60, 40), th=1.0, arch=1.4)
    if glasses_on:                                                                                     # reading glasses low on the nose
        gy = hy - 0.6
        for gx, r in ((hx + 2.8, 1.8), (hx - 1.0, 1.5)):
            rr = sp.m_super(gx, gy, r, r * 0.7, 3.0)[0] & ~sp.m_super(gx, gy, r - 0.45, r * 0.7 - 0.45, 3.0)[0]
            sp.fill(rr, (150, 60, 90))
        thin(sp, (hx - 3.4, gy), (hx - 6.0, hy - 10.0), GOLD, 0.15)                                    # the chain
    sp.ell(hx + 4.8, hy - 1.6, 1.2, 1.6, tones(dark(SKIN_L, 0.96)))
    DX.blush(sp, hx + 2.4, hy - 2.6, 1.6, 0.9, (236, 130, 140))
    mx, my = hx + 2.2, hy - 4.0
    DX.mouth(sp, mx, my, 3.4, E, mouth_, (196, 40, 70), inside=(100, 24, 36), teeth=(255, 255, 250), skin=SKIN_L, maxh=3.8)
    sp.dot(hx + 3.6, hy - 1.0, (110, 70, 60))                                                          # a mole
    # the beehive: taller than she is
    hive = sp.union([sp.m_ell(hx - 0.6, hy + 9.0, 6.2, 9.0), sp.m_ell(hx - 1.0, hy + 3.0, 5.8, 3.4), sp.m_ell(hx - 3.6, hy + 1.0, 2.4, 4.0)],
                    tones(HIVE), exclude=head & (DX.YC < hy + 3.0) & (DX.XC > hx - 2.4))
    for q in range(5):
        a0 = 0.8 + q * 0.5
        thin(sp, (hx - 0.6 + math.cos(a0) * 5.4, hy + 9.0 + math.sin(a0) * 8.0), (hx - 0.6 - math.cos(a0) * 3.0, hy + 12.0 - q * 2.0),
             dark(HIVE, 0.7), 0.18, mask=hive)
    thin(sp, (hx + 2.0, hy + 14.0), (hx + 4.4, hy + 16.8), (40, 40, 40), 0.24)                         # a pencil stuck in it
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 0.8, hy + 0.6), chest=Q(0.6, 42.0))
    before = sp.m.copy()
    shN = Q(7.4, 48.0 + br)
    hn = hand_n if hand_n is not None else Q(9.0, 30.0)
    kN, eN = ik(shN, hn, 8.0, 8.0, -1.0)
    sp.cap(shN, kN, 2.8, 2.4, tones(CARDI))
    sp.cap(kN, eN, 2.3, 1.9, tones(CARDI))
    if prop_n and getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.ell(eN[0], eN[1] - 0.3, 2.0, 1.9, tones(SKIN_L))
    if prop_n and not getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m & before
    sp.col[o] = INK


def calc(sp, h, text='40000'):
    """a desk calculator in the hand: grey body, a green display, button grid"""
    x, y = h
    sp.sup(x + 1.0, y + 3.6, 3.2, 4.4, tones((92, 92, 100)), n=4.0)
    sp.fill(sp.m_super(x + 1.0, y + 6.2, 2.6, 1.1, 6.0)[0], (150, 220, 150))
    for r in range(3):
        for c in range(3): sp.dot(x - 0.6 + c * 1.3, y + 1.0 + r * 1.3, (220, 220, 214))
    sp.anchors['calc'] = (x + 1.0, y + 6.2)


def loupe(sp, h):
    """a big magnifying glass: brass ring, glass with a white glint, a wooden handle"""
    x, y = h
    thin(sp, (x, y), (x + 2.6, y + 3.6), (110, 70, 40), 0.7)
    ring = sp.m_ell(x + 5.0, y + 7.0, 3.6, 3.6)[0]
    sp.fill(ring & ~sp.m_ell(x + 5.0, y + 7.0, 2.8, 2.8)[0], BRASS)
    sp.fill(sp.m_ell(x + 5.0, y + 7.0, 2.8, 2.8)[0], (200, 230, 240))
    sp.glint(x + 4.0, y + 8.0, 0.5)
    sp.anchors['loupe'] = (x + 5.0, y + 7.0)


def gramota(sp, h, back=False):
    """a framed certificate held in front of the chest"""
    x, y = h
    sp.sup(x, y + 2.0, 7.0, 5.0, tones((200, 160, 70)), n=6.0, stripes=False)
    sp.fill(sp.m_super(x, y + 2.0, 6.0, 4.0, 6.0)[0], (250, 244, 226) if not back else (236, 236, 232))
    if not back:
        sp.txt_box(['ГРАМОТА'], (x - 5.6, y + 3.0, x + 5.6, y + 5.6), (190, 40, 40), pad=0.1)
        for q in range(2): thin(sp, (x - 4.0, y + 1.6 - q * 1.3), (x + 4.0, y + 1.6 - q * 1.3), (120, 120, 120), 0.18)
    else:
        sp.txt_box(['СЧЁТ'], (x - 5.6, y + 3.0, x + 5.6, y + 5.6), (40, 40, 44), pad=0.1)
    sp.anchors['gramota'] = (x, y + 2.0)


def wardrobe(sp, t=0.0, tilt=0.0):
    """a heavy soviet office wardrobe (pushed across the floor in the flashback)"""
    sp.sup(0.0, 30.0, 12.0, 30.0, tones((120, 76, 44)), n=8.0)
    sp.fill(sp.m_super(0.0, 30.0, 10.4, 28.0, 8.0)[0], (140, 92, 54))
    thin(sp, (0.0, 2.0), (0.0, 58.0), (80, 50, 30), 0.4)
    for x in (-2.5, 2.5): sp.fill(sp.m_super(x, 32.0, 0.5, 2.0, 4.0)[0], (220, 190, 90))
    sp.fill(sp.m_super(0.0, 61.0, 12.6, 1.4, 8.0)[0], (100, 62, 36))
    sp.anchors['top'] = (0.0, 60.0)


def office_chair(sp, t=0.0):
    """a black office chair seen from the side-front: seat, back, gas lift, five-star base"""
    sp.sup(0.0, 22.0, 9.0, 2.4, tones((46, 46, 54)), n=3.0)                                   # seat
    sp.sup(-6.0, 34.0, 3.0, 10.0, tones((46, 46, 54)), n=3.0)                                 # back
    thin(sp, (-4.0, 26.0), (-1.0, 22.0), (30, 30, 34), 0.6)
    sp.cap((0.0, 20.0), (0.0, 6.0), 0.9, 0.9, tones((70, 70, 78)))
    for dx in (-8.0, -3.0, 3.0, 8.0):
        thin(sp, (0.0, 5.0), (dx, 2.0), (30, 30, 34), 0.7)
        sp.blob(dx, 1.4, 1.0, (24, 24, 28))
    sp.anchors['seat'] = (0.0, 24.0)


def envelope(sp, h, label='ПРЕМИЯ'):
    """a paper envelope held in the hand"""
    x, y = h
    sp.sup(x + 3.0, y + 2.0, 5.0, 3.2, tones((240, 232, 210)), n=6.0, stripes=False)
    thin(sp, (x - 1.8, y + 4.8), (x + 3.0, y + 1.8), (190, 180, 150), 0.2)
    thin(sp, (x + 3.0, y + 1.8), (x + 7.8, y + 4.8), (190, 180, 150), 0.2)
    sp.txt_box([label], (x - 1.4, y - 0.8, x + 7.4, y + 1.6), (190, 40, 40), pad=0.1)
    sp.anchors['envelope'] = (x + 3.0, y + 2.0)
