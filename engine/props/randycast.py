"""«Thanks, Randy» cast + props, drawn in the «Fridge-Light Sitcom» manner (props/randypix.py).
Coordinates: sprite px, feet anchor at (0, 0), x right = facing side, y UP.
  randy(sp, ...)    — Randy Kowalczyk, 48, Ohio sitcom dad: «brick on a pear» (square flat-top head, narrow shoulders, huge bottom,
                      skinny legs in cargo shorts in November, white dad sneakers), push-broom moustache, turkey oven mitt
  tom(sp, ...)      — Tom, a 22 lb frozen turkey in a red net: «a boulder with legs», a face drawn in frost, deadpan
  joyce(sp, ...)    — Nana Joyce, 82: «a dandelion on a match» (tiny, a huge lavender perm, magnifying glasses, a giant purse)
  brayden(sp, ...)  — cousin Brayden, 24: «a noodle» (long, thin, a pea-sized man-bun, puffer vest over a hoodie, a selfie stick)
Props: kiosk (Shop'n'Weep self-checkout with a bagging shelf), wallet, cap."""
import math
import numpy as np
from props import dibspix as DX
from props.dibspix import dark, mix, erode, dilate, ik, EXPR
from props.randypix import tones, thin, stroke, INK, WHITE, FROST, COLD

# ---------------------------------------------------------------- palette
SKIN = (238, 176, 140)              # Randy: ruddy Midwestern
SKIN_J = (240, 200, 184)            # Joyce: powdered
SKIN_B = (226, 186, 150)            # Brayden
NOSE = (226, 118, 100)
HAIR = (104, 74, 52)                # Randy's flat-top
GREY = (176, 172, 168)
POLO = (52, 118, 84)                # forest-green polo
APRON = (246, 238, 216)
APRON_T = (196, 44, 52)             # red trim / letters
KHAKI = (190, 164, 112)             # cargo shorts
SOCK = (248, 248, 246)
SHOE = (244, 244, 240)
NAVY = (40, 58, 120)
MITT_B = (150, 92, 46)              # turkey oven mitt: brown body
FEATH = ((226, 96, 40), (246, 176, 48), (176, 70, 36), (236, 200, 90))
WATTLE = (214, 40, 44)

TURK = (232, 214, 218)              # Tom: frozen raw skin (pink-white)
NET = (204, 36, 48)
LABEL = (252, 222, 64)
ICE_EYE = (232, 244, 252)

PERM = (190, 160, 232)              # Joyce lavender perm
CARD = (214, 166, 52)               # mustard cardigan
SKIRT = (124, 60, 104)              # plum skirt
STOCK = (226, 196, 170)
PURSE = (150, 40, 64)
GOLD = (234, 196, 80)
GLASS_F = (196, 150, 64)

VEST = (52, 60, 58)                 # Brayden: charcoal puffer vest
HOOD = (170, 174, 182)              # heather hoodie
JOG = (110, 114, 124)
BHAIR = (120, 84, 56)

KIO = (214, 218, 224)               # kiosk plastic
KIO_D = (82, 88, 100)
SCREEN_BG = (20, 34, 58)

XTRA = dict(
    proud=dict(eo=0.85, pu=0.55, bt=0.15, bl=0.3, mo=0.0, mc=0.9, teeth=True),
    losing=dict(eo=1.35, pu=0.3, bt=-0.7, bl=0.9, mo=0.85, mc=-0.3),
    plead=dict(eo=1.15, pu=0.55, bt=-0.85, bl=0.7, mo=0.3, mc=-0.5),
    strain=dict(eo=0.35, pu=0.5, bt=0.6, bl=-0.2, mo=0.4, mc=-0.6, teeth=True),
    nosy=dict(eo=1.0, pu=0.55, bt=-0.2, bl=0.5, mo=0.0, mc=0.45, lid=0.15),
    sweet=dict(eo=0.0, pu=0.6, bt=-0.3, bl=0.4, mo=0.0, mc=0.9, shut=True),
    fine=dict(eo=0.75, pu=0.55, bt=0.35, bl=0.0, mo=0.0, mc=0.55, lid=0.3),
    lazy=dict(eo=0.65, pu=0.6, bt=0.0, bl=0.0, mo=0.0, mc=0.25, lid=0.5),
    hype=dict(eo=0.95, pu=0.6, bt=-0.2, bl=0.35, mo=0.4, mc=0.8, lid=0.25),
    dead=dict(eo=0.72, pu=0.55, bt=0.0, bl=0.0, mo=0.0, mc=0.0, lid=0.58),
)


def X(expr):
    return dict(XTRA.get(expr) or EXPR.get(expr, EXPR['normal']))


def _hnorm(m, cx, rx):
    """flat-ish normals for a polygon part of a union (lit as a vertical cylinder)"""
    return (m, np.clip((DX.XC - cx) / rx, -0.9, 0.9) * 0.85, np.full_like(DX.XC, 0.05))


# ================================================================================ hand props
def turkey_mitt(sp, h, open_=0.0, flip_up=False):
    """Randy's turkey oven mitt (a kid's «hand turkey»): a brown thumb-head with a red wattle and an eye, a fan of feather fingers"""
    x, y = h
    for i, a in enumerate((1.9, 1.35, 0.8, 0.25)):                                   # feather fingers fan out behind the palm
        a = a + open_ * 0.25 * (i - 1.5)
        ex, ey = x - 0.6 + math.cos(a) * 5.4, y + 0.6 + math.sin(a) * 5.4
        sp.cap((x - 0.4, y + 0.4), (ex, ey), 1.9, 1.5, tones(FEATH[i]))
    sp.ell(x, y - 0.2, 3.6, 3.2, tones(MITT_B))                                       # palm / body
    hx, hy = x + 3.2, y + 1.2                                                        # thumb = the turkey head
    sp.ell(hx, hy, 1.9, 1.9, tones(MITT_B))
    sp.ell(hx + 1.9, hy - 0.2, 0.9, 0.6, tones((240, 190, 60)), ol=False)            # beak
    sp.ell(hx + 1.3, hy - 1.6, 0.6, 1.1, tones(WATTLE), ol=False)                    # wattle
    sp.dot(hx + 0.4, hy + 0.5, (20, 16, 20))
    for q in range(3): thin(sp, (x - 2.0, y - 2.6 + q * 1.2), (x + 1.6, y - 2.0 + q * 1.2), dark(MITT_B, 0.7), 0.18)   # quilting
    sp.anchors['mitt'] = (x, y)


def wallet(sp, h):
    x, y = h
    sp.sup(x + 0.6, y + 0.4, 2.6, 1.7, tones((110, 70, 44)), n=3.0)


def cap(sp, h):
    """Randy's mesh-back trucker cap held in the hand"""
    x, y = h
    sp.ell(x + 1.0, y + 1.0, 3.6, 2.4, tones((196, 44, 52)))
    sp.ell(x + 4.2, y - 0.2, 2.6, 0.8, tones((196, 44, 52)))


def shoe_prop(sp, h):
    x, y = h
    sp.ell(x + 1.4, y, 4.2, 2.0, tones(SHOE))
    sp.fill(sp.m_ell(x + 1.4, y, 4.2, 2.0)[0] & (DX.YC < y - 0.8), (150, 150, 156))


def phone(sp, h, live=True):
    x, y = h
    m = sp.m_super(x, y + 3.0, 2.0, 3.6, 4.0)[0]
    sp.paint(m, tones((36, 36, 42)), None, olc=INK)
    sp.fill(sp.m_super(x, y + 3.0, 1.5, 2.9, 4.0)[0], (110, 190, 240))
    if live: sp.fill(sp.m_ell(x - 0.6, y + 5.4, 0.45, 0.45)[0], (255, 40, 40))


# ================================================================================ RANDY
def randy(sp, t=0.0, expr='normal', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
          mitt=True, walk=None, lean=0.0, sweat=0.0, stache=None, cap_on=False, shoe_off=False, soot=0.0, legs=True, tremble=0.0,
          belly=0.0, gravy=0.0, brows=True, goggles=False):
    """RANDY — square brick head with a 90s flat-top, a push-broom moustache across the whole face, bead eyes with whites, caterpillar
    brows, a potato nose; a pear body in a forest-green polo under an apron «KISS THE COOK (DON'T)»; cargo shorts in November, skinny
    hairy legs, knee socks, chunky white dad sneakers; a turkey oven mitt on the near hand, a Bluetooth earpiece, a pencil behind the ear.
    stache: None | 'up' (pride) | 'droop' ; tremble 0..1 shakes the moustache and head (rage)"""
    E = X(expr)
    if blink is None: blink = ((t + 1.7) % 3.9) < 0.12
    br = 0.35 * math.sin(t * 2.0)
    bob = abs(math.sin(walk)) * 1.0 if walk is not None else 0.0
    jit = math.sin(t * 60.0) * 0.35 * tremble
    def Q(x, y): return (x + lean * (y / 60.0) * 5.0 + (jit if y > 56 else 0), y + (bob if y > 12 else bob * 0.3))
    swing = math.sin(walk) * 4.0 if walk is not None else 0.0

    # ---------------------------------------------------------------- far arm (behind)
    shF = Q(-8.6, 52.0 + br * 0.3)
    hf = hand_f if hand_f is not None else Q(-12.0 - swing * 0.6, 38.0)
    kF, eF = ik(shF, hf, 8.0, 7.6, -1.0)
    sp.cap(shF, kF, 3.4, 2.4, tones(dark(POLO, 0.8)))
    sp.cap(kF, eF, 2.3, 2.0, tones(dark(SKIN, 0.88)))
    sp.ell(eF[0], eF[1] - 0.4, 2.3, 2.2, tones(dark(SKIN, 0.88)))
    if prop_f: prop_f(sp, eF)
    sp.anchors['hand_f'] = eF
    # ---------------------------------------------------------------- legs: skinny, hairy, knee socks, dad sneakers
    if legs:
        sw = math.sin(walk) * 2.4 if walk is not None else 0.0
        for k_, dx in enumerate((-3.8, 3.8)):
            s_ = sw if k_ else -sw
            near = k_ == 1
            sk = SKIN if near else dark(SKIN, 0.86)
            lift = max(0.0, s_) * 0.5
            fx_, fy_ = dx + s_ * 0.7, 2.4 + lift
            sp.cap((dx * 0.8, 23.0), (fx_, fy_ + 9.0), 1.9, 1.7, tones(sk))
            for q in range(3): thin(sp, (dx * 0.8 - 0.8 + q * 0.7, 20.0 - q * 2.4), (dx * 0.8 - 0.2 + q * 0.7, 19.0 - q * 2.4), dark(HAIR, 0.8), 0.14)
            sock = sp.cap((fx_, fy_ + 10.0), (fx_, fy_ + 1.0), 1.9, 2.0, tones(SOCK if near else dark(SOCK, 0.88)))
            sp.fill(sock & (np.abs(DX.YC - (fy_ + 8.6)) < 0.45), NAVY)
            sp.fill(sock & (np.abs(DX.YC - (fy_ + 7.4)) < 0.45), APRON_T)
            if shoe_off and near:
                sp.ell(fx_ + 1.4, fy_ - 0.4, 3.6, 1.8, tones(SOCK))
            else:
                sh = sp.ell(fx_ + 1.8, fy_ - 0.2, 5.4, 2.7, tones(SHOE if near else dark(SHOE, 0.9)))
                sp.fill(sh & (DX.YC < fy_ - 1.6), (150, 152, 160))                                        # chunky sole
                thin(sp, (fx_ - 0.6, fy_ + 0.6), (fx_ + 3.2, fy_ + 0.2), NAVY, 0.4)                          # side stripe
    # ---------------------------------------------------------------- cargo shorts
    sh_ = sp.union([sp.m_super(*Q(0.4, 27.0), 12.0, 5.6, 3.2), sp.m_ell(*Q(-3.6, 23.6), 4.4, 3.0), sp.m_ell(*Q(4.6, 23.6), 4.6, 3.0)], tones(KHAKI))
    pk = sp.m_super(*Q(9.6, 24.6), 2.4, 2.4, 3.0)[0] & sh_
    sp.paint(pk, tones(dark(KHAKI, 0.9)), None)
    thin(sp, Q(7.4, 26.8), Q(11.8, 26.8), dark(KHAKI, 0.6), 0.22)
    # ---------------------------------------------------------------- pear body: green polo
    bk = 1.0 + 0.32 * belly
    body = sp.union([sp.m_ell(*Q(1.6 + 2.0 * belly, 38.0), 15.4 * bk, 12.6 * (1.0 + 0.18 * belly)), sp.m_ell(*Q(1.0, 49.0), 11.6, 8.6)], tones(POLO))
    # apron (front = +x side of the pear)
    ap = body & (DX.XC > Q(-4.0, 40)[0]) & (DX.YC < Q(0, 54.0)[1]) & (DX.YC > Q(0, 27.0)[1])
    sp.paint(ap, tones(APRON), DX.lit(np.clip((DX.XC - 4.0) / 15.0, -0.9, 0.9), np.clip((DX.YC - 40.0) / 14.0, -0.9, 0.9)))
    sp.fill(ap & ~erode(ap) & (DX.XC > Q(-3.4, 40)[0]), APRON_T)
    thin(sp, Q(-1.4, 54.0), Q(-3.0, 58.6), APRON_T, 0.5); thin(sp, Q(9.0, 54.0), Q(7.6, 58.8), APRON_T, 0.5)    # neck strap
    sp.txt_box(['KISS THE', 'COOK', "(DON'T)"], (Q(-3.8, 0)[0], Q(0, 33.0)[1], Q(8.0, 0)[0], Q(0, 51.0)[1]), APRON_T, alt=(['KISS', 'COOK'],), pad=0.5)
    # collar
    sp.ell(*Q(3.2, 56.8), 5.6, 1.8, tones(dark(POLO, 0.9)))
    # ---------------------------------------------------------------- head: a brick
    hx, hy = Q(3.4, 66.0)
    hx += jit
    sp.ell(hx + 0.6, hy - 9.2, 7.6, 3.4, tones(dark(SKIN, 0.94)))                       # double chin
    head = sp.sup(hx, hy, 9.6, 9.6, tones(SKIN), n=3.6)
    sp.ell(hx - 7.4, hy + 0.2, 1.8, 2.6, tones(dark(SKIN, 0.92)))                      # ear
    thin(sp, (hx - 7.6, hy + 1.6), (hx - 7.2, hy - 1.0), dark(SKIN, 0.65), 0.22)
    # flat-top: a flat brush of hair on top, grey temples
    ft = sp.sup(hx - 0.6, hy + 10.4, 10.0, 3.4, tones(HAIR), n=6.0)
    sp.fill(ft & (DX.XC < hx - 6.8), GREY)
    sp.fill(sp.m_super(hx - 7.6, hy + 5.0, 1.6, 3.2, 4.0)[0] & head, GREY)            # grey sideburn
    for q in range(-9, 10, 2):
        thin(sp, (hx + q * 0.9, hy + 8.2), (hx + q * 0.9, hy + 13.4), dark(HAIR, 0.68) if hx + q * 0.9 > hx - 6.8 else dark(GREY, 0.8), 0.16)
    sp.fill(ft & (DX.YC > hy + 13.0), mix(HAIR, (255, 230, 170), 0.35))              # lamp-lit flat top
    lx, ly = look
    DX.eye(sp, hx + 5.2, hy + 2.6, 4.4, 4.2, E, (110, 84, 52), (lx, ly), blink, lash=INK, skin=SKIN, bold=1)
    DX.eye(sp, hx - 0.8, hy + 2.6, 3.8, 4.0, E, (110, 84, 52), (lx, ly), blink, lash=INK, skin=SKIN, bold=1)
    if brows:
        DX.brow(sp, hx + 5.4, hy + 6.4, 5.4, E, +1, HAIR, th=3, bushy=True)
        DX.brow(sp, hx - 0.8, hy + 6.3, 4.4, E, -1, HAIR, th=3, bushy=True)
    if goggles:                                                                       # welding goggles: two green lenses on a strap
        thin(sp, (hx - 7.6, hy + 3.0), (hx + 9.0, hy + 3.4), (40, 40, 44), 0.7)
        for (ex, r) in ((hx + 5.2, 2.9), (hx - 0.8, 2.6)):
            sp.ell(ex, hy + 2.8, r + 0.5, r + 0.3, tones((60, 60, 66)), ol=False)
            sp.ell(ex, hy + 2.8, r - 0.2, r - 0.4, tones((70, 170, 110)), ol=False, gloss=1.0)
    if sp.k >= 2:
        for q in range(2): thin(sp, (hx + 1.4, hy + 9.2 + q * 1.1), (hx + 6.4, hy + 9.4 + q * 1.1), dark(SKIN, 0.78), 0.14)   # forehead lines
    DX.blush(sp, hx + 1.6, hy - 2.6, 2.8, 1.8, (232, 110, 100))
    DX.blush(sp, hx + 9.0, hy - 3.0, 1.6, 1.4, (232, 110, 100))
    DX.stubble(sp, sp.m_ell(hx + 3.6, hy - 7.6, 7.4, 3.0)[0] & head, dark(SKIN, 0.7), 0.35, 3)
    mx, my = hx + 5.2, hy - 6.0
    DX.mouth(sp, mx, my, 6.0, E, mouth_, (150, 60, 56), inside=(90, 20, 30), skin=SKIN, maxh=6.5)
    # push-broom moustache
    up = 1.0 if stache == 'up' else (-1.0 if stache == 'droop' else 0.0)
    sj = math.sin(t * 50.0) * 0.3 * tremble
    if gravy > 0:                                                                     # gravy moustache + drips on the chin
        sp.fill(sp.m_ell(mx, my - 0.6, 4.2, 1.3)[0] & head, (120, 70, 34))
        for q in range(3):
            yy = my - 2.0 - ((t * 2.0 + q * 0.4) % 1.0) * 4.0 * gravy
            sp.ell(mx - 2.0 + q * 2.0, yy, 0.6, 0.9, tones((132, 78, 36)), ol=False)
    msk = sp.union([sp.m_ell(mx - 0.6, my + 2.4 + sj, 7.0, 2.1), sp.m_ell(mx + 4.6, my + 2.4 + up * 0.8 - sj, 3.0, 1.8, 0.4 * up),
                    sp.m_ell(mx - 6.2, my + 2.4 + up * 0.8 + sj, 2.6, 1.7, -0.4 * up)], tones(HAIR))
    for q in range(-14, 16, 2):
        thin(sp, (mx + q * 0.5, my + 2.8 + sj), (mx + q * 0.5 + 0.1, my + 0.6 + sj), dark(HAIR, 0.62), 0.16, mask=msk)
    sp.fill(msk & (DX.YC > my + 3.6 + sj), mix(HAIR, (255, 220, 160), 0.30))
    # potato nose
    sp.ell(hx + 9.6, hy - 0.8, 3.2, 2.8, tones(NOSE), gloss=1.0)
    sp.dot(hx + 8.6, hy - 2.4, dark(NOSE, 0.55))
    if sp.k >= 2:
        thin(sp, (hx + 8.6, hy + 0.2), (hx + 10.0, hy - 0.6), dark(NOSE, 0.75), 0.12)
    # earpiece + pencil
    sp.ell(hx - 7.6, hy + 0.4, 1.0, 1.5, tones((60, 62, 70)), ol=False)
    sp.dot(hx - 7.6, hy + 1.0, (80, 170, 255))
    thin(sp, (hx - 8.8, hy + 1.8), (hx - 5.8, hy + 6.4), (240, 196, 60), 0.5)
    thin(sp, (hx - 8.8, hy + 1.8), (hx - 8.4, hy + 2.4), (236, 140, 150), 0.55)
    if cap_on:
        sp.ell(hx - 0.4, hy + 11.0, 9.8, 3.6, tones((196, 44, 52)))
        sp.ell(hx + 9.2, hy + 8.6, 5.0, 1.2, tones((196, 44, 52)))
    if sweat > 0:
        for i, (x, y) in enumerate(((hx - 4.0, hy + 5.0), (hx + 7.6, hy + 5.6), (hx - 6.0, hy + 0.5))[:int(1 + 2 * sweat)]):
            yy = y - ((t * 4.0 + i * 1.3) % 4.0)
            sp.ell(x, yy, 0.7, 1.1, tones((170, 220, 255)), ol=False); sp.dot(x - 0.2, yy + 0.4, WHITE)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), nose=(hx + 9.6, hy - 0.8), eyes=(hx + 2.2, hy + 2.6), belly=(4.0, 38.0))
    if soot: sp.soot(soot)
    sp.outline(INK, 1)
    # ---------------------------------------------------------------- near arm + turkey mitt
    before = sp.m.copy()
    shN = Q(11.0, 52.0 + br * 0.3)
    hn = hand_n if hand_n is not None else Q(15.0 + swing * 0.6, 38.0)
    kN, eN = ik(shN, hn, 8.0, 7.6, -1.0)
    sp.cap(shN, kN, 3.5, 2.5, tones(POLO))
    sp.cap(kN, eN, 2.4, 2.1, tones(SKIN))
    if prop_n and getattr(prop_n, 'behind', False): prop_n(sp, eN)
    if mitt: turkey_mitt(sp, eN)
    else: sp.ell(eN[0], eN[1] - 0.4, 2.4, 2.3, tones(SKIN))
    if prop_n and not getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


# ================================================================================ TOM — the frozen turkey
def tom(sp, t=0.0, expr='dead', mouth_=0.0, look=(-0.2, 0.0), blink=None, frost=1.0, char=0.0, price='$89.99', tilt=0.0, face=True):
    """TOM — a 22 lb frozen turkey lying breast-up in a red net: a plump boulder, two drumsticks with paper frills, a yellow price
    label; the face is drawn IN FROST on the breast: tired half-lidded eyes, two icy brows, a crack for a mouth that spits ice
    crumbs when he talks. char 0..1 = soot after the fryer (E04)."""
    E = X(expr)
    if blink is None: blink = ((t + 2.9) % 5.3) < 0.14
    # far drumstick behind
    sp.cap((7.0, 9.0), (13.4, 15.4), 2.8, 2.2, tones(dark(TURK, 0.86)))
    sp.ell(14.0, 16.2, 1.4, 1.2, tones(WHITE))
    body = sp.union([sp.m_super(-1.0, 8.6, 12.4, 8.2, 2.4), sp.m_ell(4.2, 9.8, 8.6, 7.6), sp.m_ell(-9.0, 6.0, 4.0, 4.6)], tones(TURK))
    face_z = sp.m_ell(6.2, 9.4, 6.4, 5.6)[0] if face else np.zeros_like(body)
    netm = body & ~face_z
    sp.fill(netm & (((DX.XC + DX.YC) % 3.4) < 0.38), NET)                                         # red net (not over the face)
    sp.fill(netm & (((DX.XC - DX.YC) % 3.4) < 0.38), NET)
    sp.fill(face_z & body & ~erode(face_z), NET)                                                   # the net frames the face
    sp.fill(sp.m_ell(-1.0, 16.4, 9.0, 1.4)[0] & body, mix(TURK, FROST, 0.7))                     # frost crust on top
    lab = sp.m_super(-6.6, 9.4, 4.6, 3.0, 4.0)[0] & body                                         # price label on the back half
    sp.fill(lab, LABEL)
    sp.fill(lab & ~erode(lab), dark(LABEL, 0.6))
    sp.txt_box([price], (-11.0, 6.8, -2.2, 12.0), (190, 30, 40), pad=0.3)
    # near drumstick + paper frill
    sp.cap((10.6, 4.4), (16.4, 9.6), 3.0, 2.4, tones(TURK))
    fr = sp.ell(17.2, 10.4, 1.7, 1.4, tones(WHITE))
    for q in range(4): sp.dot(16.0 + q * 0.8, 11.8 + (q % 2) * 0.5, WHITE)
    # the face in frost
    fx_, fy_ = 6.0, 9.6
    if not face:
        if frost: sp.sparkle(body, n=int(4 + 4 * frost), seed=int(t * 0) + 11)
        if char: sp.soot(char)
        sp.anchors.update(head=(fx_, fy_), mouth=(fx_, fy_ - 3.6), top=(0.0, 17.0))
        sp.outline(INK, 1)
        return
    DX.eye(sp, fx_ - 2.4, fy_ + 1.0, 4.4, 4.2, E, (70, 120, 180), look, blink, lash=(50, 80, 140), skin=TURK, white=ICE_EYE, bold=2)
    DX.eye(sp, fx_ + 2.6, fy_ + 1.2, 4.2, 4.0, E, (70, 120, 180), look, blink, lash=(50, 80, 140), skin=TURK, white=ICE_EYE, bold=2)
    DX.brow(sp, fx_ - 2.4, fy_ + 4.6, 4.2, E, -1, (170, 220, 255), th=2)
    DX.brow(sp, fx_ + 2.8, fy_ + 4.8, 4.0, E, +1, (170, 220, 255), th=2)
    mo = max(mouth_, E['mo'])
    mx, my = fx_ + 0.2, fy_ - 3.6
    if mo > 0.1:
        mm = sp.m_ell(mx, my, 2.4 + mo * 0.8, 0.5 + mo * 1.0)[0]
        sp.fill(mm, (60, 80, 130))
        sp.fill(mm & ~erode(mm), (120, 160, 210))
        for q in range(3):                                                                         # ice crumbs falling out
            ph = (t * 3.0 + q * 0.33) % 1.0
            sp.dot(mx - 1.0 + q * 1.0, my - 1.4 - ph * 4.0, FROST)
    else:
        pts = [(mx - 2.4, my + 0.2), (mx - 1.2, my - 0.3), (mx - 0.2, my + 0.3), (mx + 0.9, my - 0.3), (mx + 2.2, my + 0.1)]
        stroke(sp, pts, (70, 100, 160), 0.26)
    if frost:
        sp.sparkle(body, n=int(4 + 4 * frost), seed=7)
        for q in range(6):                                                                         # frost specks
            sp.dot(-9.0 + q * 3.1, 14.0 + (q % 3) * 0.8, FROST)
    if char: sp.soot(char)
    sp.anchors.update(head=(fx_, fy_), mouth=(mx, my), top=(0.0, 17.0))
    sp.outline(INK, 1)


# ================================================================================ NANA JOYCE
def joyce(sp, t=0.0, expr='normal', mouth_=0.0, look=(0.5, 0.0), blink=None, sit=False, knit=None, purse='side', hand_n=None,
          hand_f=None, prop_n=None, squint=0.0, glare=True, robe=False, perm=None, card=None):
    """NANA JOYCE — tiny (to Randy's waist): a huge lavender perm helmet wider than her shoulders, magnifying glasses that make her
    eyes three times bigger (lashes, irises, crow's feet), rouge circles, pink lips, a mustard cardigan with a turkey brooch, pearls,
    a plum skirt, beige stockings, black orthopedic shoes, a giant quilted purse. sit=True: anchor = the seat under her, legs dangle;
    knit = phase (needles clicking, a lavender scarf growing)"""
    E = X(expr)
    if blink is None: blink = ((t + 1.1) % 4.3) < 0.13
    br = 0.25 * math.sin(t * 2.4)
    dy = -13.5 if sit else 0.0
    PERM_, CARD_ = perm or PERM, card or CARD
    def Q(x, y): return (x, y + dy)
    # ---------------------------------------------------------------- legs
    if sit:
        for k_, dz in enumerate((-1.6, 1.6)):
            c = STOCK if k_ else dark(STOCK, 0.88)
            sp.cap((1.0 + dz * 0.3, 2.6), (8.6 + dz * 0.2, 2.2), 2.4, 1.9, tones(SKIRT if True else c))
            sp.cap((8.6 + dz * 0.2, 2.0), (9.4 + dz * 0.4, -7.0), 1.2, 1.1, tones(c))
            sp.ell(10.6 + dz * 0.4, -8.0, 2.4, 1.3, tones((40, 34, 40)))
        sk = sp.union([sp.m_ell(2.4, 4.6, 7.4, 3.8), sp.m_ell(7.4, 3.4, 3.0, 2.2)], tones(SKIRT))
    else:
        for k_, dx in enumerate((-2.2, 2.2)):
            c = STOCK if k_ else dark(STOCK, 0.88)
            sp.cap((dx, 12.0), (dx, 2.4), 1.3, 1.2, tones(c))
            sp.ell(dx + 1.0, 1.3, 2.6, 1.4, tones((40, 34, 40)))
        sk = sp.poly([(-6.0, 11.2), (7.6, 11.2), (5.6, 21.6), (-4.6, 21.6)], tones(SKIRT), grad=(21.6, 11.2))
    # ---------------------------------------------------------------- purse at her side (behind the near arm)
    if purse == 'side':
        px, py = (-7.6, 1.0) if sit else (-8.0, 7.0)
        pm = sp.sup(px, py + 4.0, 5.4, 4.4, tones(PURSE), n=2.6)
        for q in range(-4, 5, 2):
            thin(sp, (px + q - 3, py + 1.0), (px + q + 3, py + 7.4), dark(PURSE, 0.7), 0.18, mask=pm)
            thin(sp, (px + q + 3, py + 1.0), (px + q - 3, py + 7.4), dark(PURSE, 0.7), 0.18, mask=pm)
        sp.ell(px, py + 8.0, 1.2, 0.9, tones(GOLD), gloss=1.0)
        stroke(sp, [(px - 3.4, py + 8.0), (px - 2.0, py + 11.4), (px + 2.0, py + 11.4), (px + 3.4, py + 8.0)], dark(PURSE, 0.6), 0.5)
    # ---------------------------------------------------------------- far arm
    AC = (236, 150, 180) if robe else CARD_
    shF = Q(-3.6, 28.6 + br)
    hf = hand_f if hand_f is not None else (Q(5.4, 18.4) if knit is not None else Q(-5.0, 19.0))
    kF, eF = ik(shF, hf, 4.8, 4.6, -1.0)
    sp.cap(shF, kF, 1.8, 1.5, tones(dark(AC, 0.84))); sp.cap(kF, eF, 1.5, 1.3, tones(dark(AC, 0.84)))
    sp.ell(eF[0], eF[1], 1.3, 1.2, tones(dark(SKIN_J, 0.9)))
    # ---------------------------------------------------------------- cardigan torso
    tor = sp.union([sp.m_ell(*Q(0.6, 24.6), 7.0, 6.6), sp.m_ell(*Q(0.4, 20.8), 6.6, 3.4)], tones((236, 150, 180) if robe else CARD_))
    if robe:                                                                                   # fluffy pink bathrobe down to the ankles
        sp.union([sp.m_super(*Q(0.6, 13.0), 7.4, 9.0, 2.6)], tones((236, 150, 180)))
        for q in range(6): thin(sp, Q(-5.0 + q * 2.0, 22.0), Q(-5.4 + q * 2.0, 6.0), (220, 130, 166), 0.18)
        thin(sp, Q(-6.0, 17.6), Q(7.0, 17.6), (210, 110, 150), 0.5)
    for q in range(3): sp.dot(*Q(3.8, 27.0 - q * 2.4), (240, 232, 210))                          # buttons
    thin(sp, Q(3.2, 30.6), Q(3.0, 18.6), dark(CARD, 0.7), 0.2)
    bx, by = Q(-0.6, 25.4)                                                                        # turkey brooch
    for i in range(4): sp.dot(bx - 1.2 + i * 0.8, by + 1.2, FEATH[i])
    sp.dot(bx, by, (150, 92, 46)); sp.dot(bx + 0.8, by, WATTLE)
    for q in range(7):                                                                            # pearls
        a = math.pi * (0.15 + 0.7 * q / 6)
        sp.blob(*Q(1.2 + math.cos(a) * 3.6, 30.2 - math.sin(a) * 1.6), 0.55, (250, 246, 236))
    # ---------------------------------------------------------------- head
    hx, hy = Q(1.6, 35.4)
    face = sp.union([sp.m_ell(hx, hy, 5.4, 5.8), sp.m_ell(hx + 1.0, hy - 2.6, 4.4, 3.6)], tones(SKIN_J))
    lx, ly = look
    sq = dict(E, eo=E['eo'] * (1 - 0.45 * squint), lid=max(E.get('lid', 0.0), 0.3 * squint))
    for (ex, ew) in ((hx + 3.4, 5.0), (hx - 1.8, 4.6)):                                          # magnified eyes behind the lenses
        DX.eye(sp, ex, hy + 1.0, ew, 4.8, sq, (110, 150, 120), (lx, ly), blink, lash=(40, 24, 40), skin=SKIN_J, bold=2, flick=True)
    for (ex, r) in ((hx + 3.4, 3.4), (hx - 1.8, 3.2)):                                           # glasses: round lenses + frame
        ring = sp.m_ell(ex, hy + 1.0, r + 0.45, r + 0.45)[0] & ~sp.m_ell(ex, hy + 1.0, r - 0.15, r - 0.15)[0]
        sp.fill(ring, GLASS_F)
        if glare: thin(sp, (ex - r * 0.55, hy + 1.0 + r * 0.25), (ex - r * 0.15, hy + 1.0 + r * 0.65), (255, 255, 255), 0.28, keep=True)
    thin(sp, (hx + 0.0, hy + 1.4), (hx + 1.4, hy + 1.4), GLASS_F, 0.3)
    thin(sp, (hx - 5.0, hy + 1.6), (hx - 6.4, hy + 0.8), GLASS_F, 0.3)
    DX.brow(sp, hx + 3.4, hy + 5.0, 3.6, E, +1, dark(PERM, 0.7), th=1)
    DX.brow(sp, hx - 1.8, hy + 4.8, 3.2, E, -1, dark(PERM, 0.7), th=1)
    DX.blush(sp, hx + 3.6, hy - 2.4, 1.6, 1.2, (236, 120, 150))
    DX.blush(sp, hx - 2.6, hy - 2.2, 1.4, 1.1, (236, 120, 150))
    if sp.k >= 2:
        for q in range(3): thin(sp, (hx - 0.6 + q * 1.4, hy - 4.6), (hx - 0.2 + q * 1.4, hy - 3.2), dark(SKIN_J, 0.8), 0.12)   # lip lines
        thin(sp, (hx + 5.0, hy - 1.4), (hx + 3.8, hy - 3.6), dark(SKIN_J, 0.78), 0.14)                                  # smile fold
    sp.ell(hx + 5.6, hy - 0.4, 1.4, 1.3, tones(dark(SKIN_J, 0.95)))                              # little nose
    mx, my = hx + 2.2, hy - 3.8
    DX.mouth(sp, mx, my, 3.8, E, mouth_ * 0.7, (214, 80, 120), inside=(110, 30, 50), skin=SKIN_J, maxh=3.4)
    # perm helmet: a dome + rows of curls, wider than her shoulders
    curls = [(hx - 0.2, hy + 7.6, 8.6, 5.0)]
    for q in range(9):
        a = math.pi * (0.04 + 0.92 * q / 8)
        curls.append((hx - 0.2 + math.cos(a) * 8.4, hy + 4.6 + math.sin(a) * 5.8, 2.6, 2.4))
    for q in range(4):
        curls.append((hx - 7.6 + (q % 2) * 0.6, hy + 2.0 - q * 2.0, 2.2, 2.0))                     # back curls down to the collar
    perm = sp.union([sp.m_ell(cx, cy, rx, ry) for (cx, cy, rx, ry) in curls], tones(PERM_), exclude=face & (DX.YC < hy + 4.6) & (DX.XC > hx - 4.2))
    for (cx, cy, rx, ry) in curls[1:]:
        thin(sp, (cx - rx * 0.4, cy + ry * 0.3), (cx + rx * 0.2, cy + ry * 0.5), mix(PERM_, (255, 255, 255), 0.55), 0.24, mask=perm)
        thin(sp, (cx - rx * 0.5, cy - ry * 0.2), (cx + rx * 0.4, cy - ry * 0.4), dark(PERM_, 0.72), 0.18, mask=perm)
    if robe:                                                                                   # pink foam curlers in the perm
        for q in range(5):
            a = math.pi * (0.15 + 0.7 * q / 4)
            cx_, cy_ = hx - 0.2 + math.cos(a) * 6.6, hy + 6.0 + math.sin(a) * 4.6
            sp.sup(cx_, cy_, 1.6, 0.9, tones((250, 120, 170)), n=3.0)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 0.8, hy + 1.0))
    sp.outline(INK, 1)
    # ---------------------------------------------------------------- near arm (+ knitting needles)
    before = sp.m.copy()
    shN = Q(5.2, 28.6 + br)
    hn = hand_n if hand_n is not None else (Q(8.2, 19.6) if knit is not None else Q(7.0, 19.0))
    kN, eN = ik(shN, hn, 4.8, 4.6, -1.0)
    sp.cap(shN, kN, 1.9, 1.6, tones(AC)); sp.cap(kN, eN, 1.6, 1.4, tones(AC))
    sp.ell(eN[0], eN[1], 1.4, 1.3, tones(SKIN_J))
    if knit is not None:
        a = math.sin(knit * 7.0) * 0.35
        n1 = (eN[0] + math.cos(1.1 + a) * 7.0, eN[1] + math.sin(1.1 + a) * 7.0)
        n2 = (eF[0] + math.cos(0.5 - a) * 7.0, eF[1] + math.sin(0.5 - a) * 7.0)
        thin(sp, eN, n1, (210, 214, 224), 0.32); thin(sp, eF, n2, (210, 214, 224), 0.32)
        sc = sp.union([sp.m_ell((eN[0] + eF[0]) / 2, (eN[1] + eF[1]) / 2 - 2.2, 2.6, 2.4),
                       sp.m_ell((eN[0] + eF[0]) / 2 + 0.6, (eN[1] + eF[1]) / 2 - 5.0, 2.0, 2.6)], tones(PERM))
        for q in range(4): thin(sp, ((eN[0] + eF[0]) / 2 - 2.0, (eN[1] + eF[1]) / 2 - 1.2 - q * 1.4),
                                ((eN[0] + eF[0]) / 2 + 2.0, (eN[1] + eF[1]) / 2 - 1.2 - q * 1.4), dark(PERM, 0.7), 0.16, mask=sc)
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand'] = eN; sp.anchors['hand_f'] = eF
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


def yarn_ball(sp, h=(0.0, 0.0), t=0.0):
    x, y = h
    m = sp.ell(x, y + 2.2, 2.4, 2.2, tones(PERM))
    for q in range(3): thin(sp, (x - 2.0, y + 1.0 + q * 1.2), (x + 2.0, y + 2.2 + q * 1.0), dark(PERM, 0.7), 0.18, mask=m)
    thin(sp, (x - 2.2, y + 0.6), (x - 7.0, y + 0.2), PERM, 0.26)


# ================================================================================ BRAYDEN
def brayden(sp, t=0.0, expr='lazy', mouth_=0.0, look=(0.7, 0.0), blink=None, stick=True, hand_n=None, hand_f=None, walk=None):
    """BRAYDEN — a noodle: long skinny legs in grey joggers, chunky white sneakers, a heather hoodie under a charcoal puffer vest,
    a long face with sleepy lids and dark circles, chin scruff, a tiny man-bun the size of a pea, an AirPod, a selfie stick with
    a phone streaming LIVE"""
    E = X(expr)
    if blink is None: blink = ((t + 0.6) % 3.3) < 0.12
    br = 0.3 * math.sin(t * 1.8)
    sw = math.sin(walk) * 2.4 if walk is not None else 0.0
    for k_, dx in enumerate((-2.6, 2.6)):
        s_ = sw if k_ else -sw
        c = JOG if k_ else dark(JOG, 0.86)
        sp.cap((dx * 0.8, 42.0), (dx + s_, 4.0), 2.4, 1.9, tones(c))
        sh = sp.ell(dx + s_ + 1.6, 2.2, 4.6, 2.4, tones(SHOE if k_ else dark(SHOE, 0.9)))
        sp.fill(sh & (DX.YC < 1.0), (160, 160, 166))
    # far arm
    shF = (-4.4, 61.0 + br)
    hf = hand_f if hand_f is not None else (-5.0, 42.0)
    kF, eF = ik(shF, hf, 10.0, 9.6, -1.0)
    sp.cap(shF, kF, 1.9, 1.6, tones(dark(HOOD, 0.84))); sp.cap(kF, eF, 1.6, 1.4, tones(dark(HOOD, 0.84)))
    sp.ell(eF[0], eF[1], 1.5, 1.4, tones(dark(SKIN_B, 0.88)))
    hoodie = sp.union([sp.m_super(0.6, 51.0, 6.4, 13.0, 2.6), sp.m_ell(0.4, 41.0, 6.2, 3.0)], tones(HOOD))
    vest = sp.union([sp.m_super(0.8, 53.0, 6.8, 10.6, 2.8)], tones(VEST))
    for q in range(5): sp.fill(vest & (np.abs(DX.YC - (45.0 + q * 3.6)) < 0.32), dark(VEST, 0.66))      # puffer baffles
    thin(sp, (3.6, 63.0), (3.4, 43.0), (180, 184, 190), 0.25)                                         # zip
    sp.ell(-2.4, 64.4, 4.6, 2.4, tones(HOOD))                                                          # hood behind the neck
    for q in range(2): thin(sp, (2.6 + q * 1.4, 63.6), (2.8 + q * 1.4, 58.6), (240, 240, 244), 0.2)    # drawstrings
    sp.cap((1.0, 63.0), (1.6, 68.0), 2.0, 2.0, tones(SKIN_B))                                          # neck
    hx, hy = 2.2, 74.0
    head = sp.union([sp.m_ell(hx, hy, 5.8, 7.4), sp.m_ell(hx + 1.0, hy - 4.2, 4.6, 3.8)], tones(SKIN_B))
    sp.ell(hx - 4.8, hy + 0.4, 1.3, 2.0, tones(dark(SKIN_B, 0.92)))                                  # ear
    sp.ell(hx - 4.6, hy - 0.4, 0.7, 1.1, tones(WHITE), ol=False)                                    # AirPod
    hair = sp.union([sp.m_ell(hx - 0.4, hy + 5.6, 6.0, 3.2)], tones(BHAIR), exclude=sp.m_ell(hx + 3.2, hy + 3.4, 3.4, 1.8)[0])
    for q in range(5): thin(sp, (hx - 4.0 + q * 1.8, hy + 5.0), (hx - 5.0 + q * 1.8, hy + 7.6), dark(BHAIR, 0.68), 0.16, mask=hair)
    sp.ell(hx - 2.4, hy + 9.4, 1.6, 1.5, tones(BHAIR))                                                # pea-sized man-bun
    sp.ell(hx - 2.0, hy + 8.2, 1.0, 0.5, tones((60, 60, 70)), ol=False)                             # hair tie
    lx, ly = look
    DX.eye(sp, hx + 3.0, hy + 1.6, 3.6, 3.6, E, (90, 110, 80), (lx, ly), blink, lash=INK, skin=SKIN_B, bag=dark(SKIN_B, 0.72))
    DX.eye(sp, hx - 1.4, hy + 1.6, 3.2, 3.4, E, (90, 110, 80), (lx, ly), blink, lash=INK, skin=SKIN_B, bag=dark(SKIN_B, 0.72))
    DX.brow(sp, hx + 3.0, hy + 4.4, 3.4, E, +1, BHAIR, th=1)
    DX.brow(sp, hx - 1.4, hy + 4.3, 3.0, E, -1, BHAIR, th=1)
    sp.ell(hx + 5.4, hy - 0.6, 1.4, 1.8, tones(dark(SKIN_B, 0.95)))                                # nose
    mx, my = hx + 2.6, hy - 4.4
    DX.mouth(sp, mx, my, 3.8, E, mouth_, (160, 90, 80), inside=(90, 24, 34), skin=SKIN_B, maxh=5)
    DX.stubble(sp, sp.m_ell(hx + 2.4, hy - 6.6, 3.0, 1.8)[0] & head, dark(BHAIR, 0.85), 0.55, 5)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my))
    sp.outline(INK, 1)
    before = sp.m.copy()
    shN = (5.0, 61.0 + br)
    hn = hand_n if hand_n is not None else ((9.0, 56.0) if stick else (6.0, 42.0))
    kN, eN = ik(shN, hn, 10.0, 9.6, -1.0)
    sp.cap(shN, kN, 2.0, 1.7, tones(HOOD)); sp.cap(kN, eN, 1.7, 1.5, tones(HOOD))
    sp.ell(eN[0], eN[1], 1.6, 1.5, tones(SKIN_B))
    if stick:                                                                                        # selfie stick + phone streaming LIVE
        tip = (eN[0] + 15.0, eN[1] + 10.0)
        thin(sp, eN, tip, (40, 40, 46), 0.5)
        m = sp.m_super(tip[0] + 1.0, tip[1] + 1.0, 1.6, 3.0, 4.0)[0]
        sp.paint(m, tones((36, 36, 42)), None, olc=INK)
        sp.fill(sp.m_super(tip[0] + 1.0, tip[1] + 1.0, 1.1, 2.4, 4.0)[0], (110, 190, 240))
        sp.fill(sp.m_ell(tip[0] + 0.6, tip[1] + 3.0, 0.4, 0.4)[0], (255, 40, 40))
        sp.anchors['phone'] = (tip[0] + 1.0, tip[1] + 1.0)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


# ================================================================================ KIOSK — Shop'n'Weep self-checkout
def kiosk(sp, t=0.0, lamp='green', screen='idle', alarm=0.0, part='all', bag_on=True):
    """a self-checkout station seen 3/4 from the customer side (customer stands on the LEFT): a cabinet with the scanner glass on top,
    the screen on a post facing the customer, a light pole with the lane number, and on the RIGHT a bagging shelf with a tall bag rack
    and a big hanging plastic bag (it hides whoever sits on the shelf behind it — only a few lavender curls peek over: the clue).
    part: 'all' | 'back' (everything but the hanging bag) | 'front' (only the bag).  anchors: 'bag' = top of the bagging shelf,
    'screen' = the screen centre, 'lamp'.  screen: 'idle' | 'price' | 'alarm' | 'glitch'"""
    sp.anchors.update(screen=(-6.6, 52.6), lamp=(8.0, 68.6), bag=(24.0, 33.0), bagtop=(24.0, 65.0))
    if part in ('all', 'back'):
        _kiosk_back(sp, t, lamp, screen, alarm)
    if part in ('all', 'front') and bag_on:
        bag_prop(sp, (24.0, 33.4), t=t)
    sp.outline(INK, 1)


def bag_prop(sp, at=(24.0, 33.4), t=0.0, w=23.0, h=31.6, held=False):
    """the big white «THANK YOU» plastic bag hanging on the rack (bottom-centre at `at`); held=True: crumpled in a fist"""
    x, y = at
    sway = math.sin(t * 1.7) * 0.4
    if held:
        m = sp.union([sp.m_ell(x, y - 4.0, 5.0, 6.0), sp.m_ell(x + 1.0, y + 1.6, 2.4, 2.4)], tones((236, 238, 240)))
        for q in range(4): thin(sp, (x - 3.0 + q * 1.6, y - 8.0), (x - 2.0 + q * 1.4, y - 1.0), (190, 196, 206), 0.2, mask=m)
        return
    bag = sp.m_poly([(x - w / 2 + sway, y + h), (x + w / 2 + sway, y + h), (x + w / 2 - 1.0, y), (x - w / 2 + 1.0, y)])
    sp.paint(bag, tones((236, 238, 240)), np.clip((DX.XC - (x - w / 2)) / w, 0, 1) * 0.5 + 0.3, olc=(170, 176, 186))
    for q in range(3): thin(sp, (x - w / 2 + 3 + q * 4 + sway, y + h - 1.0), (x - w / 2 + 2.4 + q * 4.2, y + 1.0), (206, 210, 220), 0.18, mask=bag)
    sp.fill(bag & (np.abs(DX.YC - (y + h * 0.55)) < 2.4) & (np.abs(DX.XC - x) < 5.2), (220, 50, 56))      # red «THANK YOU» smiley print
    sp.txt_box(['THANK', 'YOU!'], (x - 5.0, y + h * 0.55 - 2.2, x + 5.0, y + h * 0.55 + 2.2), (255, 255, 255), pad=0.15)
    for q in (-1, 1): thin(sp, (x + q * (w / 2 - 1.4) + sway, y + h), (x + q * (w / 2 - 0.8), y + h + 1.6), (200, 204, 210), 0.3)


def _kiosk_back(sp, t, lamp, screen, alarm):
    # bagging shelf on the right (behind the cabinet in depth)
    sp.sup(24.0, 31.0, 13.0, 2.0, tones(KIO_D), n=5.0)
    for x in (13.0, 35.0):
        sp.cap((x, 2.0), (x, 30.0), 1.0, 1.0, tones((150, 156, 166)))
    sp.ell(24.0, 1.4, 13.6, 1.4, tones((70, 74, 84)))
    for x in (12.4, 35.6):                                                                     # tall bag rack posts
        sp.cap((x, 33.0), (x, 66.0), 0.5, 0.5, tones((200, 204, 210)))
    thin(sp, (12.4, 66.0), (35.6, 66.0), (200, 204, 210), 0.45)
    # cabinet
    cab = sp.sup(0.0, 17.0, 10.4, 17.0, tones(KIO), n=5.0)
    sp.fill(cab & (DX.YC < 6.0), (64, 70, 82))
    door = sp.m_super(0.4, 19.0, 7.6, 9.6, 5.0)[0]
    sp.fill(door & ~erode(door), dark(KIO, 0.7))
    sp.fill(sp.m_super(0.0, 31.0, 7.4, 1.2, 4.0)[0], (60, 64, 72))                             # coin slot band
    sp.txt_box(["SHOP'N", 'WEEP'], (-6.0, 14.0, 6.8, 24.0), (196, 40, 36), pad=0.6)
    top = sp.sup(-1.0, 35.0, 11.4, 1.6, tones((40, 44, 52)), n=5.0)                           # scanner glass
    for q in range(3):
        thin(sp, (-8.0 + q * 3.0, 35.4), (2.0 + q * 3.0, 34.6), (255, 60, 60) if (int(t * 6) + q) % 2 else (180, 30, 40), 0.18, mask=top)
    sp.cap((-6.0, 36.0), (-6.4, 46.0), 1.2, 1.2, tones(KIO_D))                                # screen post + screen
    scr = sp.m_poly([(-12.4, 46.0), (-1.0, 47.6), (-1.0, 59.4), (-12.4, 58.2)])
    sp.paint(scr, tones((52, 56, 66)), None, olc=INK)
    inner = sp.m_poly([(-11.6, 46.9), (-1.8, 48.3), (-1.8, 58.5), (-11.6, 57.3)])
    blink = int(t * 4) % 2 == 0
    if screen == 'alarm':
        sp.fill(inner, (200, 30, 40) if blink or alarm < 0.5 else (120, 20, 30))
        sp.txt_box(['!'], (-10.6, 48.6, -2.8, 56.8), WHITE, pad=0.4)
    elif screen == 'price':
        sp.fill(inner, SCREEN_BG)
        sp.txt_box(['$89'], (-11.0, 49.0, -2.4, 56.4), (255, 230, 80), pad=0.3)
    elif screen == 'glitch':
        sp.fill(inner, SCREEN_BG)
        rng = np.random.default_rng(int(t * 20))
        for q in range(5):
            y = 48.0 + rng.random() * 9.0
            sp.fill(inner & (np.abs(DX.YC - y) < 0.6), (int(rng.integers(60, 255)), int(rng.integers(60, 255)), 255))
    else:
        sp.fill(inner, SCREEN_BG)
        sp.fill(inner & (DX.YC > 55.6), (40, 150, 90))
    sp.cap((8.0, 35.0), (8.0, 66.0), 0.6, 0.6, tones((160, 166, 176)))                         # light pole with the lane number
    lc = dict(green=(70, 230, 110), red=(255, 60, 60), amber=(255, 190, 40))[lamp]
    on = lamp != 'red' or blink or alarm < 0.5
    sp.sup(8.0, 68.6, 2.2, 2.8, tones(lc if on else dark(lc, 0.45)), n=2.4, gloss=0.6 if on else 0.0)
    sp.sup(8.0, 73.6, 2.6, 2.2, tones((240, 240, 236)), n=4.0)
    sp.txt_box(['3'], (5.8, 71.6, 10.2, 75.6), (40, 44, 52), pad=0.2)


# ================================================================================ E02 — airport
TSA = (46, 64, 110)                 # navy uniform shirt
TSA_P = (40, 40, 48)                # black trousers
GLOVE = (90, 150, 230)              # blue nitrile gloves
SKIN_P = (196, 140, 110)
HAIR_P = (70, 46, 36)
GRAVY = (128, 74, 34)


def patty(sp, t=0.0, expr='dead', mouth_=0.0, look=(-0.7, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, chew=True, bubble=0.0):
    """OFFICER PATTY (TSA) — «a mailbox»: short, square and solid, navy uniform shirt with a shoulder patch and a badge, black trousers,
    blue nitrile gloves, hair pulled into a tight bun, heavy unimpressed lids, a jaw that never stops chewing gum (bubble 0..1)"""
    E = X(expr)
    if blink is None: blink = ((t + 0.4) % 4.1) < 0.12
    br = 0.25 * math.sin(t * 1.6)
    for k_, dx in enumerate((-4.0, 4.0)):
        c = TSA_P if k_ else dark(TSA_P, 0.85)
        sp.cap((dx, 24.0), (dx, 3.0), 3.4, 3.0, tones(c))
        sp.ell(dx + 1.6, 1.6, 4.4, 1.9, tones((24, 22, 26)), gloss=0.8)
    shF = (-9.4, 45.0 + br)
    hf = hand_f if hand_f is not None else (-11.0, 26.0)
    kF, eF = ik(shF, hf, 8.6, 8.0, -1.0)
    sp.cap(shF, kF, 3.0, 2.6, tones(dark(TSA, 0.82))); sp.cap(kF, eF, 2.4, 2.1, tones(dark(GLOVE, 0.85)))
    sp.ell(eF[0], eF[1], 2.2, 2.0, tones(dark(GLOVE, 0.85)))
    body = sp.sup(0.6, 35.0, 11.4, 13.4, tones(TSA), n=3.4)
    sp.fill(body & (np.abs(DX.YC - 23.0) < 0.9), (30, 30, 34))                                 # belt
    sp.fill(sp.m_super(3.6, 23.0, 1.4, 0.9, 3.0)[0], (210, 200, 150))
    for q in range(4): sp.dot(4.6, 44.0 - q * 4.6, (220, 220, 230))                            # buttons
    thin(sp, (4.0, 47.0), (4.0, 24.4), dark(TSA, 0.6), 0.22)
    sp.sup(-3.0, 40.6, 2.6, 2.6, tones((200, 170, 60)), n=2.4, gloss=0.8)                      # badge
    sp.ell(-8.4, 42.0, 2.2, 2.8, tones((180, 40, 40)))                                         # shoulder patch
    sp.txt_box(['TSA'], (-1.0, 33.0, 9.6, 37.6), (230, 230, 240), pad=0.2)
    sp.ell(1.6, 48.4, 5.6, 1.8, tones(dark(TSA, 0.9)))                                         # collar
    hx, hy = 2.0, 56.6
    jaw = math.sin(t * 9.0) * 0.6 if chew and mouth_ < 0.1 else 0.0
    head = sp.union([sp.m_ell(hx, hy, 7.6, 8.2), sp.m_ell(hx + 1.2, hy - 4.0 + jaw * 0.4, 6.4, 4.6)], tones(SKIN_P))
    sp.ell(hx - 6.4, hy + 0.6, 1.5, 2.2, tones(dark(SKIN_P, 0.9)))
    hair = sp.union([sp.m_ell(hx - 0.8, hy + 5.2, 7.8, 4.0), sp.m_ell(hx - 6.0, hy + 2.0, 2.4, 4.6)], tones(HAIR_P),
                    exclude=sp.m_ell(hx + 3.0, hy + 2.6, 5.0, 2.0)[0])
    sp.ell(hx - 6.6, hy + 7.6, 3.0, 2.8, tones(HAIR_P))                                        # tight bun
    for q in range(4): thin(sp, (hx - 6.0 + q * 2.4, hy + 7.6), (hx - 4.0 + q * 2.4, hy + 4.2), dark(HAIR_P, 0.7), 0.16, mask=hair)
    lx, ly = look
    DX.eye(sp, hx + 3.6, hy + 1.2, 4.0, 3.8, E, (90, 70, 50), (lx, ly), blink, lash=INK, skin=SKIN_P, bag=dark(SKIN_P, 0.78))
    DX.eye(sp, hx - 1.8, hy + 1.2, 3.6, 3.6, E, (90, 70, 50), (lx, ly), blink, lash=INK, skin=SKIN_P, bag=dark(SKIN_P, 0.78))
    DX.brow(sp, hx + 3.6, hy + 4.4, 4.0, E, +1, HAIR_P, th=2)
    DX.brow(sp, hx - 1.8, hy + 4.2, 3.6, E, -1, HAIR_P, th=2)
    sp.ell(hx + 6.4, hy - 1.0, 1.7, 2.0, tones(dark(SKIN_P, 0.95)))
    mx, my = hx + 3.0, hy - 5.0 + jaw
    DX.mouth(sp, mx, my, 4.6, E, mouth_, (150, 70, 70), inside=(90, 24, 34), skin=SKIN_P, maxh=5)
    if bubble > 0:
        sp.ell(mx + 1.6, my - 0.4, 1.0 + 3.6 * bubble, 1.0 + 3.4 * bubble, tones((255, 150, 200)), gloss=1.0)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my))
    sp.outline(INK, 1)
    before = sp.m.copy()
    shN = (10.6, 45.0 + br)
    hn = hand_n if hand_n is not None else (13.0, 26.0)
    kN, eN = ik(shN, hn, 8.6, 8.0, -1.0)
    sp.cap(shN, kN, 3.1, 2.7, tones(TSA)); sp.cap(kN, eN, 2.5, 2.2, tones(GLOVE))
    sp.ell(eN[0], eN[1], 2.4, 2.1, tones(GLOVE))
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


def gravy_jug(sp, h, tilt=0.0, level=1.0, label=True):
    """a gallon plastic jug of Nana's gravy held by the handle (h = hand); tilt in degrees (drinking)"""
    x, y = h
    a = math.radians(tilt)
    ca, sa = math.cos(a), math.sin(a)
    def R(px, py): return (x + px * ca - py * sa, y + px * sa + py * ca)
    pts = [R(-1.0, -2.0), R(9.0, -2.0), R(9.6, 9.0), R(6.0, 12.6), R(4.0, 14.6), R(1.8, 14.6), R(1.8, 12.6), R(-1.6, 9.0)]
    jug = sp.m_poly(pts)
    sp.paint(jug, tones((236, 232, 220)), np.clip((DX.XC - x + 2) / 12, 0, 1) * 0.5 + 0.3, olc=(150, 140, 120))
    if level > 0:
        lv = sp.m_poly([R(-0.6, -1.6), R(8.6, -1.6), R(9.2, -1.6 + 10.0 * level), R(-1.2, -1.6 + 10.0 * level)]) & jug
        sp.paint(lv, tones(GRAVY), None)
    sp.paint(sp.m_poly([R(1.6, 14.4), R(4.2, 14.4), R(4.2, 16.0), R(1.6, 16.0)]), tones((200, 40, 40)), None)      # red cap
    if label:
        lb = sp.m_poly([R(0.2, 1.0), R(8.2, 1.0), R(8.2, 7.4), R(0.2, 7.4)]) & jug
        sp.fill(lb, (252, 246, 226))
        cx, cy = R(4.2, 4.2)
        if abs(tilt) < 30: sp.txt_box(["NANA'S", 'GRAVY'], (cx - 3.8, cy - 3.0, cx + 3.8, cy + 3.0), (150, 40, 30), pad=0.2)
    sp.anchors['jug_mouth'] = R(3.0, 16.0)


def tsa_bin(sp, t=0.0, part='all', w=34.0, h=7.0):
    """grey plastic TSA bin, side view (feet at its bottom centre); part 'back' | 'front' | 'all' so things can sit inside"""
    GR = (150, 156, 166)
    if part in ('all', 'back'):
        sp.sup(0.0, h * 0.62, w / 2 - 0.6, h * 0.5, tones(dark(GR, 0.7)), n=6.0)
    if part in ('all', 'front'):
        m = sp.m_poly([(-w / 2, h), (w / 2, h), (w / 2 - 1.6, 0.0), (-w / 2 + 1.6, 0.0)])
        sp.paint(m, tones(GR), np.clip((DX.YC) / h, 0, 1) * 0.6 + 0.25, olc=INK)
        thin(sp, (-w / 2 + 0.4, h - 0.6), (w / 2 - 0.4, h - 0.6), (200, 206, 214), 0.3)
        sp.txt_box(['PLEASE REMOVE DIGNITY'], (-w / 2 + 3.0, 1.4, w / 2 - 3.0, h - 1.8), (230, 230, 236), pad=0.2)
    sp.outline(INK, 1)


# ================================================================================ E03 — the turkey hotline
CHEESE = (250, 200, 60)
SWEAT = (196, 60, 52)                # Carol's turkey sweater (cranberry)
HAIR_C = (236, 206, 120)             # Wisconsin blonde bob


def hair_dryer(sp, h, on=True, t=0.0):
    """a pink hair dryer blowing at the turkey (nozzle forward = +x)"""
    x, y = h
    sp.cap((x, y), (x + 1.0, y - 5.0), 1.2, 1.1, tones((236, 110, 160)))                          # handle
    body = sp.ell(x + 2.6, y + 1.4, 4.2, 2.6, tones((240, 120, 170)))
    sp.cap((x + 5.6, y + 1.4), (x + 9.0, y + 1.4), 1.6, 1.3, tones((210, 90, 140)))               # nozzle
    sp.ell(x + 0.2, y + 1.6, 1.4, 2.0, tones((80, 70, 80)))                                         # back grille
    thin(sp, (x + 0.6, y - 5.0), (x - 2.0, y - 9.0), (40, 40, 44), 0.3)                            # cord
    sp.anchors['nozzle'] = (x + 9.4, y + 1.4)


def cell(sp, h, glow=True):
    """a phone held to the ear"""
    x, y = h
    m = sp.m_super(x + 0.6, y + 2.6, 1.6, 3.4, 4.0)[0]
    sp.paint(m, tones((40, 40, 46)), None, olc=INK)
    if glow: sp.fill(sp.m_super(x + 0.6, y + 2.6, 1.1, 2.8, 4.0)[0], (120, 200, 250))


def dip_bowl(sp, h):
    """a bowl of seven-layer dip with chips sticking out"""
    x, y = h
    sp.ell(x + 1.0, y + 1.6, 5.6, 2.6, tones((240, 236, 226)))
    sp.ell(x + 1.0, y + 3.2, 5.0, 1.4, tones((150, 110, 60)))
    for q in range(4): sp.cap((x - 2.4 + q * 1.8, y + 3.0), (x - 2.8 + q * 1.8, y + 6.0), 0.7, 0.5, tones((236, 190, 80)))


def carol(sp, t=0.0, expr='hype', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
          hair=HAIR_C, sweater=SWEAT, headset=True, cheese=True, panic=0.0, seed=0):
    """CAROL (Butterbutt Turkey Talk-Line) — «a cupcake»: round body in a cranberry turkey sweater with a big knitted turkey, a
    Wisconsin blonde bob with bangs, cheese-wedge earrings, a phone headset with a mic, rosy cheeks, a sing-song smile that cracks
    into panic (panic 0..1: sweat drops, hair frizz). Variants (other operators): hair / sweater colours, cheese=False"""
    E = X(expr)
    if blink is None: blink = ((t + 0.9 + seed * 0.7) % 3.7) < 0.12
    br = 0.3 * math.sin(t * 2.2 + seed)
    for k_, dx in enumerate((-3.0, 3.0)):
        c = (60, 56, 70) if k_ else (48, 44, 56)
        sp.cap((dx, 16.0), (dx, 3.0), 2.2, 2.0, tones(c))
        sp.ell(dx + 1.2, 1.4, 3.2, 1.5, tones((110, 70, 50)))
    shF = (-8.0, 34.0 + br)
    hf = hand_f if hand_f is not None else (-10.0, 20.0)
    kF, eF = ik(shF, hf, 6.6, 6.4, -1.0)
    sp.cap(shF, kF, 2.6, 2.2, tones(dark(sweater, 0.82))); sp.cap(kF, eF, 2.2, 1.9, tones(dark(sweater, 0.82)))
    sp.ell(eF[0], eF[1], 1.7, 1.6, tones(dark(SKIN_J, 0.9)))
    if prop_f: prop_f(sp, eF)
    body = sp.union([sp.m_ell(0.6, 25.0, 11.2, 10.4), sp.m_ell(0.4, 16.0, 9.6, 3.6)], tones(sweater))
    for q in range(4): sp.fill(body & (np.abs(DX.YC - (17.0 + q * 0.0)) < 0.5) & (((DX.XC * 2).astype(int) % 2) == 0), WHITE)   # knit hem
    tx, ty = 3.0, 25.0                                                                                # knitted turkey on the sweater
    for i in range(4): sp.ell(tx - 1.0 + i * 0.9, ty + 2.6, 0.9, 2.2, tones(FEATH[i]), ol=False)
    sp.ell(tx + 1.2, ty, 2.6, 2.2, tones(MITT_B), ol=False)
    sp.dot(tx + 2.6, ty + 0.8, WATTLE)
    hx, hy = 2.0, 40.0
    head = sp.union([sp.m_ell(hx, hy, 6.4, 6.8), sp.m_ell(hx + 1.0, hy - 3.2, 5.2, 3.6)], tones(SKIN_J))
    lx, ly = look
    DX.eye(sp, hx + 3.2, hy + 1.2, 3.8, 3.8, E, (80, 130, 190), (lx, ly), blink, lash=INK, skin=SKIN_J, flick=True)
    DX.eye(sp, hx - 1.6, hy + 1.2, 3.4, 3.6, E, (80, 130, 190), (lx, ly), blink, lash=INK, skin=SKIN_J, flick=True)
    DX.brow(sp, hx + 3.2, hy + 4.2, 3.6, E, +1, dark(hair, 0.7), th=1)
    DX.brow(sp, hx - 1.6, hy + 4.0, 3.2, E, -1, dark(hair, 0.7), th=1)
    DX.blush(sp, hx + 4.0, hy - 2.0, 1.6, 1.2, (240, 120, 120))
    DX.blush(sp, hx - 2.4, hy - 2.0, 1.4, 1.1, (240, 120, 120))
    sp.ell(hx + 5.6, hy - 0.4, 1.4, 1.5, tones(dark(SKIN_J, 0.95)))
    mx, my = hx + 2.6, hy - 3.6
    DX.mouth(sp, mx, my, 4.2, E, mouth_, (200, 70, 90), inside=(110, 30, 50), skin=SKIN_J, maxh=5)
    bob = sp.union([sp.m_ell(hx - 0.6, hy + 4.4, 7.6, 4.6), sp.m_ell(hx - 5.6, hy - 0.6, 3.0, 5.6), sp.m_ell(hx + 6.0, hy + 1.6, 2.2, 3.8)],
                   tones(hair), exclude=sp.m_ell(hx + 2.4, hy + 0.6, 4.6, 3.4)[0])
    for q in range(5): thin(sp, (hx - 3.0 + q * 1.8, hy + 7.8), (hx - 2.4 + q * 1.8, hy + 4.2), dark(hair, 0.72), 0.16, mask=bob)
    if panic > 0:                                                                                     # frizz + sweat
        for q in range(int(6 * panic)): thin(sp, (hx - 6 + q * 2.0, hy + 8.4), (hx - 7 + q * 2.4, hy + 10.6), hair, 0.3)
        for i in range(int(1 + 2 * panic)):
            yy = hy + 4.0 - ((t * 4 + i * 1.3) % 4.0)
            sp.ell(hx + 6.4 - i * 1.6, yy, 0.6, 0.9, tones((170, 220, 255)), ol=False)
    if cheese:                                                                                        # cheese-wedge earring
        sp.paint(sp.m_poly([(hx - 6.0, hy - 2.4), (hx - 4.0, hy - 2.4), (hx - 5.0, hy - 4.6)]), tones(CHEESE), None)
    if headset:
        stroke(sp, [(hx - 6.0, hy + 1.0), (hx - 4.0, hy + 8.4), (hx + 2.0, hy + 9.0), (hx + 6.4, hy + 4.0)], (40, 40, 46), 0.4)
        sp.ell(hx - 5.8, hy + 0.4, 1.4, 1.8, tones((50, 50, 56)))
        stroke(sp, [(hx - 5.6, hy - 1.0), (hx - 1.0, hy - 4.6), (hx + 1.0, hy - 4.2)], (40, 40, 46), 0.3)
        sp.dot(hx + 1.2, hy - 4.2, (60, 60, 66))
    sp.anchors.update(head=(hx, hy), mouth=(mx, my))
    sp.outline(INK, 1)
    before = sp.m.copy()
    shN = (9.4, 34.0 + br)
    hn = hand_n if hand_n is not None else (11.0, 20.0)
    kN, eN = ik(shN, hn, 6.6, 6.4, -1.0)
    sp.cap(shN, kN, 2.7, 2.3, tones(sweater)); sp.cap(kN, eN, 2.3, 2.0, tones(sweater))
    sp.ell(eN[0], eN[1], 1.8, 1.7, tones(SKIN_J))
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


OPERATORS = [dict(hair=(90, 60, 40), sweater=(60, 110, 70), cheese=False, seed=1), dict(hair=(200, 200, 206), sweater=(214, 150, 50), cheese=True, seed=2),
             dict(hair=(150, 50, 40), sweater=(70, 90, 160), cheese=False, seed=3), dict(hair=(40, 34, 30), sweater=(170, 60, 120), cheese=True, seed=4),
             dict(hair=(236, 206, 120), sweater=(120, 80, 50), cheese=False, seed=5)]


# ================================================================================ E04 — the fryer and the fire department
FIRE_R = (206, 34, 36)
TURNOUT = (196, 160, 70)            # tan turnout coat with reflective bands
REFL = (230, 240, 120)


def fryer(sp, t=0.0, flames=1.0, boil=1.0):
    """«FRY-HARD 3000»: a tall aluminium turkey-fryer pot on a three-leg propane burner, a hose to a white propane tank"""
    for x in (-7.0, 0.0, 7.0):
        sp.cap((x * 0.9, 9.0), (x, 0.0), 0.8, 0.8, tones((60, 60, 66)))
    sp.sup(0.0, 9.6, 8.6, 1.2, tones((50, 50, 56)), n=5.0)
    if flames > 0:
        for q in range(7):
            ph = (t * 6.0 + q * 0.37) % 1.0
            h_ = (2.0 + 2.4 * (1 - ph)) * flames
            sp.ell(-5.4 + q * 1.8, 10.6 + h_ * 0.4, 0.8, h_ * 0.5, tones((70, 150, 255) if ph < 0.5 else (255, 180, 60)), ol=False)
    pot = sp.sup(0.0, 19.0, 8.0, 8.4, tones((196, 202, 212)), n=3.6, gloss=0.8)
    sp.fill(pot & (np.abs(DX.YC - 20.0) < 2.4) & (np.abs(DX.XC) < 6.0), (230, 220, 200))
    sp.txt_box(['FRY-HARD', '3000'], (-6.0, 17.4, 6.0, 22.6), (196, 40, 36), pad=0.2)
    sp.ell(0.0, 27.2, 8.4, 1.2, tones((120, 124, 132)))
    if boil > 0:
        for q in range(6):
            ph = (t * 4.0 + q * 0.21) % 1.0
            sp.ell(-6.0 + q * 2.4, 27.6 + ph * 2.0 * boil, 0.7 + 0.5 * ph, 0.7 + 0.5 * ph, tones((240, 200, 90)), ol=False)
    thin(sp, (7.6, 2.0), (18.0, 1.0), (40, 40, 44), 0.4)                                            # hose
    tank = sp.sup(21.0, 6.2, 3.6, 6.0, tones((236, 236, 232)), n=2.6, gloss=0.7)
    sp.cap((21.0, 12.0), (21.0, 13.4), 1.2, 1.2, tones((150, 150, 156)))
    sp.anchors.update(pot_top=(0.0, 27.6))
    sp.outline(INK, 1)


def hook_pole(sp, h, length=16.0):
    """a long steel lifting hook held at h, pointing forward-down (the turkey hangs on its end)"""
    x, y = h
    e = (x + length * 0.8, y - length * 0.25)
    thin(sp, (x, y), e, (170, 176, 186), 0.5)
    stroke(sp, [e, (e[0] + 0.6, e[1] - 1.6), (e[0] - 0.6, e[1] - 2.4)], (170, 176, 186), 0.4)
    sp.anchors['hook_end'] = (e[0], e[1] - 2.4)


def dunn(sp, t=0.0, expr='dead', mouth_=0.0, look=(-0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None, soot=0.4):
    """CAPTAIN DUNN — «a fridge with a helmet»: a tall square man in a tan turnout coat with yellow reflective bands, black boots,
    a red helmet with a CAPTAIN shield and a long back brim, a soot-smeared square jaw, a grey walrus moustache, a toothpick"""
    E = X(expr)
    if blink is None: blink = ((t + 1.4) % 4.4) < 0.12
    br = 0.25 * math.sin(t * 1.5)
    for k_, dx in enumerate((-4.6, 4.6)):
        c = (40, 40, 44) if k_ else (30, 30, 34)
        sp.cap((dx, 30.0), (dx, 4.0), 4.0, 3.6, tones(TURNOUT if k_ else dark(TURNOUT, 0.85)))
        sp.fill(sp.m_super(dx, 14.0, 4.0, 0.9, 4.0)[0], REFL)
        sp.sup(dx + 1.2, 3.0, 5.0, 3.4, tones(c), n=3.0)
    shF = (-11.0, 60.0 + br)
    hf = hand_f if hand_f is not None else (-13.0, 38.0)
    kF, eF = ik(shF, hf, 10.0, 9.4, -1.0)
    sp.cap(shF, kF, 3.6, 3.2, tones(dark(TURNOUT, 0.82))); sp.cap(kF, eF, 3.2, 2.8, tones(dark(TURNOUT, 0.82)))
    sp.ell(eF[0], eF[1], 2.6, 2.4, tones((60, 50, 40)))
    if prop_f: prop_f(sp, eF)
    coat = sp.sup(0.8, 46.0, 13.0, 17.0, tones(TURNOUT), n=4.0)
    for y in (34.0, 40.0): sp.fill(coat & (np.abs(DX.YC - y) < 1.0), REFL)
    for q in range(4): sp.dot(3.6, 56.0 - q * 4.6, (40, 40, 44))
    sp.txt_box(['DUNN'], (-8.0, 49.0, 2.0, 53.6), (40, 30, 20), pad=0.2)
    hx, hy = 2.6, 70.0
    head = sp.union([sp.m_super(hx, hy, 7.6, 8.2, 3.2), sp.m_super(hx + 1.0, hy - 4.6, 7.2, 4.4, 3.0)], tones((214, 160, 124)))
    lx, ly = look
    DX.eye(sp, hx + 3.8, hy + 1.6, 3.8, 3.4, E, (80, 100, 120), (lx, ly), blink, lash=INK, skin=(214, 160, 124), bag=(170, 120, 90))
    DX.eye(sp, hx - 1.8, hy + 1.6, 3.4, 3.2, E, (80, 100, 120), (lx, ly), blink, lash=INK, skin=(214, 160, 124), bag=(170, 120, 90))
    DX.brow(sp, hx + 3.8, hy + 4.4, 4.4, E, +1, (150, 150, 156), th=2, bushy=True)
    DX.brow(sp, hx - 1.8, hy + 4.2, 3.8, E, -1, (150, 150, 156), th=2, bushy=True)
    sp.ell(hx + 7.0, hy - 0.8, 2.0, 2.2, tones((200, 130, 100)))
    mx, my = hx + 3.6, hy - 5.6
    DX.mouth(sp, mx, my, 5.0, E, mouth_, (140, 70, 60), inside=(90, 24, 34), skin=(214, 160, 124), maxh=5)
    sp.union([sp.m_ell(mx - 0.4, my + 2.0, 5.2, 1.7), sp.m_ell(mx - 4.4, my + 0.6, 1.6, 2.4), sp.m_ell(mx + 4.0, my + 0.6, 1.6, 2.4)],
             tones((176, 176, 180)))                                                                   # grey walrus moustache
    if mouth_ < 0.2: thin(sp, (mx + 2.4, my - 0.6), (mx + 6.4, my - 1.6), (230, 200, 140), 0.25)       # toothpick
    sp.fill(sp.m_ell(hx - 2.0, hy - 3.0, 4.0, 2.2)[0] & head, (110, 90, 80))                            # soot smear
    sp.ell(hx - 0.4, hy + 7.0, 9.6, 3.6, tones(FIRE_R), gloss=0.6)                                    # helmet dome
    sp.ell(hx - 7.0, hy + 4.4, 5.6, 1.4, tones(dark(FIRE_R, 0.85)), ang=-0.2)                          # long back brim
    sp.sup(hx + 4.6, hy + 7.4, 2.2, 2.6, tones((236, 200, 80)), n=2.2)                                # shield
    sp.anchors.update(head=(hx, hy), mouth=(mx, my))
    if soot: sp.soot(soot * 0.35)
    sp.outline(INK, 1)
    before = sp.m.copy()
    shN = (12.6, 60.0 + br)
    hn = hand_n if hand_n is not None else (15.0, 38.0)
    kN, eN = ik(shN, hn, 10.0, 9.4, -1.0)
    sp.cap(shN, kN, 3.7, 3.3, tones(TURNOUT)); sp.cap(kN, eN, 3.3, 2.9, tones(TURNOUT))
    sp.ell(eN[0], eN[1], 2.7, 2.5, tones((60, 50, 40)))
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


def fire_truck(sp, t=0.0, lights=True):
    """the front of a Maple Falls FD engine (side view, facing right): cab with windows, chrome bumper, a light bar, «MAPLE FALLS FD» on
    the door, the ladder on top running back off the canvas; the burning part of the ladder is drawn as fire FX over it"""
    body = sp.sup(-40.0, 26.0, 70.0, 18.0, tones(FIRE_R), n=6.0)
    cab = sp.sup(18.0, 34.0, 14.0, 22.0, tones(FIRE_R), n=5.0)
    sp.fill(sp.m_super(22.0, 44.0, 8.0, 7.0, 5.0)[0], (140, 190, 230))                             # windscreen
    sp.fill(sp.m_super(10.0, 44.0, 5.0, 6.0, 5.0)[0], (120, 170, 210))                             # side window
    sp.fill(sp.m_super(-40.0, 20.0, 70.0, 1.2, 6.0)[0] | sp.m_super(18.0, 20.0, 14.0, 1.2, 6.0)[0], (240, 240, 236))   # white stripe
    sp.txt_box(['MAPLE FALLS', 'FD'], (2.0, 24.0, 28.0, 34.0), (255, 236, 160), pad=0.4)
    sp.sup(33.0, 10.0, 2.0, 5.0, tones((210, 214, 222)), n=4.0, gloss=0.8)                           # bumper
    for x in (20.0, -20.0, -70.0):                                                                  # wheels
        sp.ell(x, 7.0, 7.0, 7.0, tones((30, 30, 34)))
        sp.ell(x, 7.0, 3.2, 3.2, tones((190, 194, 204)), gloss=0.6)
    blink = int(t * 6) % 2 == 0
    for q in range(4):                                                                              # light bar
        c = (255, 40, 40) if (q % 2 == 0) == blink else (255, 230, 120)
        sp.sup(12.0 + q * 4.0, 57.6, 1.8, 1.2, tones(c if lights else dark(c, 0.5)), n=3.0, gloss=0.8 if lights else 0.0)
    for x0 in range(-108, 30, 6):                                                                   # ladder on top
        thin(sp, (x0, 47.0), (x0, 52.0), (200, 204, 212), 0.4)
    thin(sp, (-110.0, 47.0), (30.0, 47.0), (200, 204, 212), 0.5)
    thin(sp, (-110.0, 52.0), (30.0, 52.0), (200, 204, 212), 0.5)
    sp.anchors.update(ladder=(-60.0, 50.0), door=(14.0, 26.0))
    sp.outline(INK, 1)


def extinguisher(sp, h):
    x, y = h
    sp.sup(x + 0.4, y - 3.0, 2.0, 4.6, tones((210, 30, 36)), n=2.6, gloss=0.7)
    sp.cap((x + 0.4, y + 1.8), (x + 2.8, y + 3.2), 0.6, 0.5, tones((40, 40, 44)))
    stroke(sp, [(x + 1.6, y + 1.2), (x + 3.6, y + 0.4), (x + 4.4, y - 1.6)], (30, 30, 34), 0.35)


def inflatable_turkey(sp, t=0.0, sway=1.0):
    """a giant inflatable lawn turkey (decor), wobbling"""
    w = math.sin(t * 1.4) * 1.4 * sway
    for i, c in enumerate(FEATH):
        a = 1.9 - i * 0.42 + w * 0.05
        sp.ell(-2.0 + math.cos(a) * 10.0, 22.0 + math.sin(a) * 10.0, 4.0, 7.0, tones(c), ang=a - 1.57)
    sp.ell(0.0 + w * 0.3, 16.0, 9.0, 10.0, tones(MITT_B))
    sp.ell(6.0 + w * 0.6, 26.0, 3.6, 3.6, tones(MITT_B))
    sp.ell(9.6 + w * 0.6, 25.6, 1.6, 1.0, tones((240, 190, 60)))
    sp.ell(8.4 + w * 0.6, 23.6, 0.9, 1.6, tones(WATTLE))
    sp.dot(6.6 + w * 0.6, 27.0, (20, 16, 20))
    sp.ell(0.0, 1.0, 5.0, 1.0, tones((60, 60, 66)))
    sp.outline(INK, 1)


# ================================================================================ E05 — Thanksgiving dinner and the paywall
ROAST = (206, 132, 56)


def roast(sp, t=0.0, tag=True, steam=True):
    """a golden store-bought roast turkey on a white platter, a big yellow «SHOP'N'WEEP $139» price sticker still on it"""
    sp.ell(0.0, 1.4, 16.0, 2.0, tones((240, 240, 236)), gloss=0.6)
    body = sp.union([sp.m_super(-1.0, 8.6, 12.4, 7.0, 2.4), sp.m_ell(4.0, 9.6, 8.6, 6.6)], tones(ROAST), gloss=0.9)
    sp.cap((7.0, 7.0), (13.0, 12.6), 3.0, 2.4, tones(dark(ROAST, 0.9)))
    sp.ell(13.8, 13.4, 1.6, 1.4, tones(WHITE))
    for q in range(5): thin(sp, (-9.0 + q * 3.6, 12.6), (-7.6 + q * 3.6, 5.0), dark(ROAST, 0.72), 0.2, mask=body)
    if tag:
        lab = sp.m_super(-3.0, 9.6, 5.4, 3.0, 4.0)[0] & body
        sp.fill(lab, LABEL)
        sp.fill(lab & ~erode(lab), dark(LABEL, 0.6))
        sp.txt_box(['$139'], (-8.0, 7.0, 2.0, 12.2), (190, 30, 40), pad=0.3)
    sp.anchors.update(head=(0.0, 9.0), top=(0.0, 16.0))
    sp.outline(INK, 1)


def remote(sp, h):
    x, y = h
    sp.sup(x + 1.0, y + 1.6, 1.2, 3.6, tones((40, 40, 46)), n=4.0)
    sp.dot(x + 1.0, y + 4.0, (255, 60, 60))


def tiny_tv(sp, h, t=0.0, final=False):
    """Nana's 1998 portable TV: a beige box with a rabbit-ears antenna, a snowy little screen"""
    x, y = h
    box = sp.sup(x + 3.0, y + 3.4, 4.4, 3.6, tones((216, 204, 176)), n=4.0)
    scr = sp.m_super(x + 2.4, y + 3.6, 2.8, 2.4, 4.0)[0]
    rng = np.random.default_rng(int(t * 20))
    sn = rng.random(scr.shape) < 0.5
    sp.fill(scr, (70, 80, 90)); sp.fill(scr & sn, (200, 210, 220))
    thin(sp, (x + 3.0, y + 7.0), (x + 0.6, y + 11.4), (180, 180, 186), 0.22)
    thin(sp, (x + 3.4, y + 7.0), (x + 6.6, y + 11.0), (180, 180, 186), 0.22)
    sp.anchors['tiny_screen'] = (x + 2.4, y + 3.6)


# ================================================================================ E06 — Black Friday at Best Bye
BB_BLUE = (30, 70, 170)
BB_YEL = (252, 214, 40)
BOX = (196, 160, 110)
GRANNIES = [dict(perm=(236, 236, 240), card=(70, 130, 170)), dict(perm=(200, 120, 90), card=(120, 160, 90)),
            dict(perm=(150, 150, 160), card=(200, 90, 120)), dict(perm=(240, 200, 120), card=(110, 90, 160))]


def kyle(sp, t=0.0, expr='dead', mouth_=0.0, look=(-0.7, 0.0), blink=None, hand_n=None, hand_f=None):
    """KYLE (Best Bye) — «a question mark»: a slouching teenager in a blue store polo with a yellow name tag and a lanyard, long greasy
    bangs over one eye, a few pimples, heavy sleepy lids, a scanner gun in hand"""
    E = X(expr)
    if blink is None: blink = ((t + 2.0) % 3.1) < 0.14
    for k_, dx in enumerate((-2.4, 2.4)):
        sp.cap((dx, 30.0), (dx, 3.0), 2.4, 2.0, tones((60, 60, 70) if k_ else (48, 48, 56)))
        sp.ell(dx + 1.4, 1.6, 3.6, 1.8, tones((40, 40, 46)))
    sp.cap((-5.0, 50.0), (-7.0, 30.0), 1.8, 1.5, tones(dark(BB_BLUE, 0.85)))
    body = sp.union([sp.m_super(1.6, 41.0, 6.6, 11.4, 2.6)], tones(BB_BLUE))
    sp.fill(sp.m_super(3.6, 46.0, 2.6, 1.4, 4.0)[0], BB_YEL)
    sp.txt_box(['KYLE'], (1.2, 44.8, 6.2, 47.4), (30, 30, 40), pad=0.1)
    thin(sp, (1.0, 52.0), (3.6, 47.0), (230, 200, 60), 0.3)
    hx, hy = 4.0, 59.0                                                                           # slouch: head forward
    head = sp.union([sp.m_ell(hx, hy, 5.6, 6.6), sp.m_ell(hx + 0.8, hy - 3.4, 4.6, 3.6)], tones(SKIN_B))
    lx, ly = look
    DX.eye(sp, hx + 2.8, hy + 1.0, 3.4, 3.2, E, (80, 100, 80), (lx, ly), blink, lash=INK, skin=SKIN_B, bag=dark(SKIN_B, 0.75))
    sp.union([sp.m_ell(hx - 0.6, hy + 4.4, 6.0, 3.4)], tones((110, 80, 50)))
    bang = sp.m_poly([(hx - 2.0, hy + 6.0), (hx + 3.0, hy + 5.4), (hx + 0.0, hy - 1.2), (hx - 2.4, hy + 0.6)])
    sp.paint(bang, tones((110, 80, 50)), None)
    for (x, y) in ((hx + 3.6, hy - 2.0), (hx + 1.4, hy - 3.6), (hx - 2.0, hy - 1.4)): sp.dot(x, y, (220, 110, 110))
    sp.ell(hx + 5.6, hy - 0.4, 1.2, 1.5, tones(dark(SKIN_B, 0.95)))
    mx, my = hx + 2.4, hy - 4.0
    DX.mouth(sp, mx, my, 3.2, E, mouth_, (160, 90, 80), inside=(90, 24, 34), skin=SKIN_B, maxh=4)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my))
    sp.outline(INK, 1)
    before = sp.m.copy()
    hn = hand_n if hand_n is not None else (8.0, 34.0)
    kN, eN = ik((6.0, 50.0), hn, 7.6, 7.2, -1.0)
    sp.cap((6.0, 50.0), kN, 1.9, 1.6, tones(BB_BLUE)); sp.cap(kN, eN, 1.6, 1.4, tones(SKIN_B))
    sp.sup(eN[0] + 2.0, eN[1] + 0.6, 2.6, 1.4, tones((50, 50, 56)), n=3.0)                       # scanner gun
    sp.dot(eN[0] + 4.4, eN[1] + 0.6, (255, 60, 60))
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m
    sp.col[o] = INK; sp.m |= o


def tv_box(sp, t=0.0, flap=0.0, price='$199'):
    """a big flat cardboard TV box standing upright (a TV pictured on it, «65"», a yellow «$199» doorbuster tag); flap 0..1 opens the top
    flap (Nana inside)"""
    box = sp.sup(0.0, 18.0, 15.0, 18.0, tones(BOX), n=6.0)
    sp.fill(sp.m_super(0.0, 19.0, 11.6, 10.4, 6.0)[0], (30, 30, 40))
    sp.fill(sp.m_super(0.0, 19.0, 10.6, 9.4, 6.0)[0], (60, 140, 220))
    sp.fill(sp.m_ell(-3.0, 22.0, 4.0, 3.0)[0] & box, (110, 200, 120))
    sp.txt_box(['65"'], (-13.0, 31.0, -3.0, 35.4), (30, 30, 40), pad=0.2)
    tag = sp.m_super(8.4, 4.6, 5.0, 2.8, 4.0)[0]
    sp.fill(tag, BB_YEL); sp.fill(tag & ~erode(tag), (120, 90, 10))
    sp.txt_box([price], (3.8, 2.4, 13.0, 6.8), (196, 30, 40), pad=0.2)
    if flap > 0:
        a = flap * 2.4
        thin(sp, (-15.0, 36.0), (-15.0 + 15.0 * math.cos(a), 36.0 + 15.0 * math.sin(a)), dark(BOX, 0.8), 1.0)
        thin(sp, (15.0, 36.0), (15.0 - 15.0 * math.cos(a), 36.0 + 15.0 * math.sin(a)), dark(BOX, 0.8), 1.0)
    sp.anchors.update(top=(0.0, 36.0))
    sp.outline(INK, 1)


def folding_chair(sp, t=0.0, name='JOYCE', sub='SINCE TUE', tent=False):
    """a folding camping chair with a hand-written cardboard name sign taped on; tent=True: a zipped dome tent behind it"""
    if tent:
        sp.paint(sp.m_poly([(-16.0, 0.0), (16.0, 0.0), (0.0, 22.0)]), tones((90, 140, 90)), np.clip((DX.XC + 16) / 32, 0, 1) * 0.6 + 0.2)
        thin(sp, (0.0, 1.0), (0.0, 18.0), (60, 60, 60), 0.3)
    for (a, b) in (((-6.0, 0.0), (5.0, 12.0)), ((6.0, 0.0), (-5.0, 12.0))):
        thin(sp, a, b, (60, 60, 70), 0.5)
    sp.sup(0.0, 12.0, 7.0, 1.4, tones((40, 80, 160)), n=3.0)
    sp.sup(-1.0, 18.0, 6.0, 5.0, tones((40, 80, 160)), n=3.0)
    card = sp.m_super(0.0, 18.0, 6.4, 3.4, 4.0)[0]
    sp.fill(card, (236, 214, 170))
    sp.txt_box([name, sub], (-5.8, 15.0, 5.8, 21.0), (40, 40, 50), pad=0.2)
    sp.outline(INK, 1)


def walker(sp, h):
    """a granny walker with tennis balls (held at h)"""
    x, y = h
    for dx in (0.0, 6.0):
        thin(sp, (x + dx, y), (x + dx + 1.0, y - 14.0), (200, 204, 212), 0.4)
        sp.ell(x + dx + 1.0, y - 14.6, 1.0, 1.0, tones((210, 230, 60)), ol=False)
    thin(sp, (x, y), (x + 6.0, y), (200, 204, 212), 0.4)
