"""«Кощей из панельки» cast + props, drawn in the «Хохлома-нуар» manner (props/koshpix.py).
Coordinates: sprite px, feet anchor at (0, 0), x right = facing side, y UP.
  koshchei(sp, ...) — Кощей Бессмертный, 999-летний пенсионер: «вешалка» — the tallest, thinnest silhouette of the channel
  yaga(sp, ...)     — Баба Яга, старшая по подъезду: «чайник в платке» — short, hunched, a huge nose forward, bone leg
  domovoy(sp, ...)  — домовой Кузьмич из электрощитка: «шар бороды» — knee-high, only nose and eyes out of a grey beard
Props: needle_egg (утка-яйцо-игла), pension_slip, broom, string_bag."""
import math
import numpy as np
from props import dibspix as DX
from props.dibspix import dark, mix, erode, ik, EXPR
from props import koshpix as KX
from props.koshpix import tones, thin, INK, WHITE, GOLD, GOLD_L, GHOST, CINNABAR

# ---------------------------------------------------------------- palette
K_SKIN = (196, 204, 172)            # Кощей: pale grey-green parchment skin
K_SOCK = (110, 30, 30)
K_VEST = (232, 228, 214)            # майка-алкоголичка
K_TRICO = (52, 60, 104)             # трико с пузырями на коленях
K_SLIP = (122, 76, 44)              # тапки
K_MOUS = (190, 192, 186)            # усы до груди
K_IRIS = (60, 220, 110)             # кощеевы зелёные глаза

Y_SKIN = (222, 170, 140)            # Яга
Y_NOSE = (210, 120, 104)
Y_SHAWL = (24, 20, 22)              # чёрный павловопосадский платок
Y_CARD = (120, 112, 104)            # серая кофта
Y_SKIRT = (96, 58, 40)
Y_FELT = (64, 60, 66)               # валенок
BONE = (236, 226, 196)
GALOSH = (176, 30, 34)
BROOM = (196, 160, 90)

D_BEARD = (176, 170, 160)           # домовой: серо-пепельная борода-шар
D_SHIRT = (196, 40, 36)             # косоворотка
D_LAPTI = (210, 176, 104)
D_NOSE = (232, 120, 100)

XTRA = dict(
    proud=dict(eo=0.85, pu=0.55, bt=0.15, bl=0.3, mo=0.0, mc=0.6, teeth=True),
    scream=dict(eo=1.35, pu=0.3, bt=0.6, bl=0.4, mo=1.0, mc=0.0),
    sinister=dict(eo=0.75, pu=0.4, bt=0.9, bl=-0.2, mo=0.0, mc=0.7, lid=0.25),
    gossip=dict(eo=0.55, pu=0.6, bt=0.45, bl=0.0, mo=0.0, mc=0.4, lid=0.4),
    zhut=dict(eo=0.7, pu=0.55, bt=0.0, bl=0.25, mo=0.0, mc=-0.1, lid=0.5),
    frozen=dict(eo=0.9, pu=0.4, bt=-0.5, bl=0.3, mo=0.15, mc=-0.3),
)


def X(expr):
    return dict(XTRA.get(expr) or EXPR.get(expr, EXPR['normal']))


# ================================================================================ props (callbacks prop(sp, hand))
def pension_slip(sp, h, amount='13 ₽ 66 к'):
    """бумажка «ПЕНСИЯ НАЧИСЛЕНА» from the Соцфонд window"""
    x, y = h; w, hh = 11.0, 8.0
    x0, y0 = x - 2.0, y - 2.0
    m = sp.m_poly([(x0, y0), (x0 + w, y0 + 0.5), (x0 + w - 0.3, y0 + hh), (x0 - 0.2, y0 + hh - 0.3)])
    sp.paint(m, [(190, 186, 170), (240, 236, 222), (255, 252, 240)], np.clip((DX.XC - x0) / w, 0, 1) * 0.6 + 0.3, olc=(110, 104, 96))
    sp.txt_box(['ПЕНСИЯ'], (x0 + 0.3, y0 + hh * 0.55, x0 + w - 0.4, y0 + hh - 0.4), (40, 40, 50), pad=0.2)
    sp.txt_box([amount], (x0 + 0.3, y0 + 0.4, x0 + w - 0.4, y0 + hh * 0.52), CINNABAR, pad=0.2)
    sp.anchors['slip'] = (x0 + w / 2, y0 + hh / 2)


def needle_egg(sp, h, cracked=False):
    """«смерть Кощея»: a white egg with a gold needle sticking out of it (from the хрустальная утка in the сервант)"""
    x, y = h
    egg = sp.ell(x + 0.5, y + 3.2, 2.6, 3.4, tones((240, 234, 220)), gloss=0.8, snow=False)
    if cracked: thin(sp, (x - 1.4, y + 3.6), (x + 0.4, y + 2.6), INK, 0.25); thin(sp, (x + 0.4, y + 2.6), (x + 2.2, y + 3.8), INK, 0.25)
    thin(sp, (x + 0.8, y + 5.6), (x + 3.4, y + 10.4), GOLD, 0.32)
    sp.blob(x + 3.5, y + 10.6, 0.45, GOLD_L)
    sp.anchors['egg'] = (x + 0.5, y + 3.2)


def broom(sp, h):
    """дворницкая метла (her ступа is a тележка-кравчучка, see props later)"""
    x, y = h
    thin(sp, (x - 3.0, y - 14.0), (x + 2.0, y + 16.0), BROOM, 0.6)
    tw = sp.m_poly([(x - 3.6, y - 13.0), (x - 1.8, y - 13.4), (x - 0.4, y - 22.0), (x - 8.6, y - 21.0)])
    sp.paint(tw, tones((150, 110, 60)), None, olc=INK)
    for q in range(6): thin(sp, (x - 2.6 - q * 0.2, y - 13.4), (x - 1.0 - q * 1.4, y - 21.6), (110, 76, 40), 0.18, mask=tw)
    thin(sp, (x - 3.4, y - 13.6), (x - 1.6, y - 14.0), CINNABAR, 0.45)


def string_bag(sp, h):
    """авоська: a net bag with a кефир bottle and eggs"""
    x, y = h
    bag = sp.m_ell(x + 0.4, y - 7.0, 4.2, 5.4)[0]
    sp.fill(sp.m_super(x - 0.8, y - 6.0, 1.5, 3.8, 3.0)[0], (236, 236, 240))
    sp.fill(sp.m_super(x - 0.8, y - 2.0, 1.2, 0.6, 3.0)[0], (60, 140, 70))
    sp.ell(x + 2.0, y - 9.0, 1.4, 1.8, tones((240, 230, 210)), snow=False)
    e = bag & ~erode(bag)
    sp.fill(e, (190, 170, 120))
    sp.fill(bag & (((DX.XC + DX.YC) % 1.6) < 0.25), (190, 170, 120))
    thin(sp, (x - 3.0, y - 2.8), (x, y + 1.0), (190, 170, 120), 0.2); thin(sp, (x + 3.6, y - 3.0), (x, y + 1.0), (190, 170, 120), 0.2)


# ================================================================================ Кощей
def koshchei(sp, t=0.0, expr='normal', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
             walk=None, lean=0.0, crown=True, fire=0.0, shiver=0.0):
    """КОЩЕЙ — a 999-year-old pensioner, «вешалка»: the tallest and thinnest figure of the channel (≈70 px, shoulders 14 px wide).
    A long bald skull with sunken cheeks, deep green-lit eye sockets, a huge hooked nose, a thin grey moustache hanging to the chest,
    a tiny crown of chocolate FOIL askew on the bald top; майка-алкоголичка over visible ribs, трико with bubbles on the knees,
    socks in brown slippers. fire = green «кощеев огонь» in the eyes and around the hands (0..1); shiver = cold jitter (E04)."""
    E = X(expr)
    if blink is None: blink = (t % 3.9) < 0.12
    br = 0.3 * math.sin(t * 2.0)
    bob = abs(math.sin(walk)) * 1.0 if walk is not None else 0.0
    jit = math.sin(t * 64.0) * 0.4 * shiver
    def Q(x, y): return (x + lean * (y / 70.0) * 6.0 + (jit if y > 40 else 0), y + (bob if y > 9 else bob * 0.3))
    swing = math.sin(walk) * 4.0 if walk is not None else 0.0
    # ---------------------------------------------------------------- far arm
    shF = Q(-5.0, 47.0 + br * 0.3)
    hf = hand_f if hand_f is not None else Q(-7.0 - swing * 0.5, 22.0)
    kF, eF = ik(shF, hf, 12.5, 12.0, -1.0)
    sp.cap(shF, kF, 1.7, 1.5, tones(dark(K_SKIN, 0.8))); sp.cap(kF, eF, 1.5, 1.3, tones(dark(K_SKIN, 0.8)))
    sp.ell(eF[0], eF[1] - 0.8, 1.9, 2.2, tones(dark(K_SKIN, 0.8)))
    for q in range(3): thin(sp, (eF[0] - 1.0 + q * 0.9, eF[1] - 2.0), (eF[0] - 1.4 + q * 1.0, eF[1] - 4.4), dark(K_SKIN, 0.6), 0.45)
    if prop_f: prop_f(sp, eF)
    sp.anchors['hand_f'] = eF
    # ---------------------------------------------------------------- legs: трико + bubbles on the knees, socks, slippers
    sw = math.sin(walk) * 2.4 if walk is not None else 0.0
    for k_, dx in enumerate((-2.6, 2.6)):
        s_ = sw if k_ else -sw
        c = K_TRICO if k_ else dark(K_TRICO, 0.8)
        lift = max(0.0, s_) * 0.5
        knee = (dx + s_ * 0.4 + 1.2, 14.0)
        sp.cap((dx * 0.8, 29.0), knee, 2.4, 2.2, tones(c))
        sp.cap(knee, (dx + s_ * 0.7, 3.6 + lift), 2.2, 1.9, tones(c))
        sp.ell(knee[0] + 1.2, knee[1] + 0.4, 2.4, 2.8, tones(c))                       # the «bubble» on the knee
        sp.cap((dx + s_ * 0.7, 3.8 + lift), (dx + s_ * 0.7, 2.2 + lift), 1.8, 1.8, tones(K_SOCK))
        slip = sp.ell(dx + s_ * 0.7 + 2.2, 1.2 + lift, 4.4, 1.6, tones(K_SLIP))
        sp.fill(slip & (DX.YC > 1.6 + lift) & (DX.XC < dx + s_ * 0.7 + 3.4), dark(K_SLIP, 0.7))
    # ---------------------------------------------------------------- torso: майка over ribs
    tor = sp.union([sp.m_super(*Q(0.2, 38.0), 6.4, 11.0, 2.6), sp.m_ell(*Q(0.2, 47.6), 6.6, 2.6)], tones(K_SKIN))
    vest = sp.m_poly([Q(-5.6, 27.6), Q(6.2, 27.6), Q(6.0, 44.0), Q(3.6, 44.4), Q(2.6, 41.0), Q(-1.8, 41.0), Q(-3.0, 44.4), Q(-5.6, 44.0)])
    sp.paint(vest & tor | vest, tones(K_VEST), DX.lit(np.clip((DX.XC - 0.2) / 7.0, -0.9, 0.9), np.zeros_like(DX.XC)))
    for q in range(4):                                                                   # ribs showing through the vest
        yy = 39.0 - q * 2.4
        thin(sp, Q(-3.6, yy), Q(-0.4, yy - 0.6), dark(K_VEST, 0.72), 0.22, mask=vest)
        thin(sp, Q(0.8, yy - 0.6), Q(4.4, yy), dark(K_VEST, 0.72), 0.22, mask=vest)
    sp.fill(sp.m_ell(*Q(1.6, 34.0), 0.9, 0.7)[0] & vest, (196, 170, 120))                 # a kefir stain
    sp.cap(Q(-5.8, 28.0), Q(6.4, 28.0), 1.0, 1.0, tones(dark(K_TRICO, 0.7)))               # waistband
    # ---------------------------------------------------------------- neck + head
    sp.cap(Q(0.6, 47.0), Q(1.4, 54.0), 1.5, 1.4, tones(K_SKIN))
    hx, hy = Q(2.0, 62.0)
    sp.ell(hx - 7.3, hy + 0.5, 2.2, 3.5, tones(K_SKIN))                                    # pointy far ear
    head = sp.union([sp.m_ell(hx, hy + 2.2, 8.6, 11.3), sp.m_ell(hx + 1.1, hy - 6.2, 5.9, 5.4)], tones(K_SKIN))
    sp.gold(head)
    sp.fill(sp.m_ell(hx + 4.9, hy - 3.2, 2.4, 3.2)[0] & head, dark(K_SKIN, 0.78))          # sunken cheek
    for q in range(3): thin(sp, (hx - 4.1, hy + 8.6 + q * 0.9), (hx + 3.5, hy + 9.2 + q * 0.9), dark(K_SKIN, 0.82), 0.18)   # forehead wrinkles
    # eye sockets (dark lacquer) with green-lit eyes
    lx, ly = look
    for (ex, ey, w_, h_) in ((hx + 0.8, hy + 3.0, 3.6, 3.1), (hx + 6.2, hy + 3.2, 3.4, 3.0)):
        sp.fill(sp.m_ell(ex, ey, w_ * 0.95, h_ * 0.95)[0], mix(dark(K_SKIN, 0.45), (40, 70, 44), 0.25 + 0.4 * fire))
    DX.eye(sp, hx + 0.8, hy + 3.0, 5.0, 4.2, E, K_IRIS, (lx, ly), blink, lash=INK, skin=dark(K_SKIN, 0.55), lidc=dark(K_SKIN, 0.7),
           white=mix(WHITE, GHOST, 0.18 * fire))
    DX.eye(sp, hx + 6.2, hy + 3.2, 4.4, 3.8, E, K_IRIS, (lx, ly), blink, lash=INK, skin=dark(K_SKIN, 0.55), lidc=dark(K_SKIN, 0.7),
           white=mix(WHITE, GHOST, 0.18 * fire))
    DX.brow(sp, hx + 6.5, hy + 6.8, 4.2, E, +1, (90, 92, 84), th=1.4, bushy=True)
    DX.brow(sp, hx + 0.5, hy + 6.5, 4.2, E, -1, (90, 92, 84), th=1.4, bushy=True)
    # the hooked nose (the biggest shape of the face)
    nose = sp.m_poly([(hx + 5.7, hy + 1.9), (hx + 11.9, hy - 1.4), (hx + 13.0, hy - 4.9), (hx + 10.0, hy - 5.7), (hx + 6.5, hy - 3.5)])
    sp.paint(nose, tones(mix(K_SKIN, (210, 150, 140), 0.25)), DX.lit(np.full_like(DX.XC, 0.5), np.full_like(DX.XC, 0.2)), olc=INK)
    sp.blob(hx + 11.3, hy - 4.9, 0.55, dark(K_SKIN, 0.55))
    # mouth with a few long teeth
    mx, my = hx + 5.4, hy - 8.1
    DX.mouth(sp, mx, my, 5.4, E, mouth_, INK, skin=K_SKIN, maxh=7, big_teeth=True, teeth=(230, 222, 186))
    # the moustache: two thin grey strands hanging to the chest
    for side, (a, b, c) in enumerate((((mx - 3.0, my + 1.8), (mx - 4.6, my - 2.0), (mx - 5.2, my - 14.0)),
                                      ((mx + 3.2, my + 1.8), (mx + 5.2, my - 2.4), (mx + 6.4, my - 15.0)))):
        thin(sp, a, b, K_MOUS, 0.42); thin(sp, b, c, K_MOUS, 0.34)
        sp.blob(c[0], c[1], 0.4, mix(K_MOUS, WHITE, 0.4))
    # the foil crown, askew
    if crown:
        cx, cy = hx - 1.4, hy + 12.4
        cr = sp.m_poly([(cx - 4.2, cy - 1.0), (cx + 3.6, cy + 0.6), (cx + 4.2, cy + 5.0), (cx + 2.0, cy + 2.6), (cx + 0.2, cy + 5.6),
                        (cx - 1.6, cy + 2.4), (cx - 4.0, cy + 4.2)])
        sp.paint(cr, [dark(GOLD, 0.6), GOLD, GOLD_L], np.clip((DX.XC - cx + 3.4) / 7.0, 0, 1) * 0.8 + 0.1, olc=INK)
        sp.fill(cr & (((DX.XC * 1.7 + DX.YC * 0.6) % 2.2) < 0.35), WHITE)                   # crumpled foil glints
    sp.anchors['head'] = (hx, hy)
    # ---------------------------------------------------------------- near arm
    shN = Q(5.4, 47.0 + br * 0.3)
    hn = hand_n if hand_n is not None else Q(8.0 + swing * 0.5, 22.0)
    kN, eN = ik(shN, hn, 12.5, 12.0, -1.0)
    sp.cap(shN, kN, 1.8, 1.6, tones(K_SKIN)); sp.cap(kN, eN, 1.6, 1.4, tones(K_SKIN))
    sp.blob(kN[0], kN[1], 1.9, dark(K_SKIN, 0.9))
    hand = sp.ell(eN[0], eN[1] - 0.8, 2.0, 2.3, tones(K_SKIN))
    for q in range(3): thin(sp, (eN[0] - 1.0 + q * 0.9, eN[1] - 2.0), (eN[0] - 1.4 + q * 1.1, eN[1] - 4.8), K_SKIN, 0.45)
    if fire > 0:
        rng = np.random.default_rng(int(t * 12) % 97)
        for q in range(int(6 * fire)):
            a = rng.random() * 6.28; r = 2.4 + rng.random() * 2.0
            sp.blob(eN[0] + math.cos(a) * r, eN[1] + math.sin(a) * r, 0.5 + rng.random() * 0.4, mix(GHOST, WHITE, rng.random() * 0.5))
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand_n'] = eN


# ================================================================================ Баба Яга
def yaga(sp, t=0.0, expr='gossip', mouth_=0.0, look=(0.7, 0.0), blink=None, hand_n=None, prop_n=None, prop_f=broom, lean=0.0, walk=None):
    """БАБА ЯГА, старшая по подъезду — «чайник в платке»: short (≈44 px), hunched forward, a black Павловский-Посад shawl with
    cinnabar roses over head and shoulders (бигуди peek out from under it), a grey cardigan, a long brown skirt; one leg a valenok,
    the other a BONE leg in a red galosh; a huge nose with a wart, one long tooth, sharp squinting eyes; a dvornik broom."""
    E = X(expr)
    if blink is None: blink = (t % 4.3) < 0.13
    br = 0.3 * math.sin(t * 2.0)
    bob = abs(math.sin(walk)) * 0.8 if walk is not None else 0.0
    def Q(x, y): return (x + (lean + 0.35) * (y / 44.0) * 5.0, y + (bob if y > 6 else 0))
    if prop_f: prop_f(sp, Q(-8.0, 20.0))
    # legs
    sp.cap((-2.4, 8.0), (-2.6, 2.6), 2.4, 2.6, tones(Y_FELT)); sp.ell(-1.0, 1.6, 3.6, 1.8, tones(Y_FELT))
    sp.cap((2.8, 8.0), (3.4, 3.0), 1.2, 1.0, tones(BONE))
    for q in range(3): thin(sp, (2.4, 7.0 - q * 1.6), (3.8, 7.2 - q * 1.6), dark(BONE, 0.7), 0.18)
    sp.ell(4.6, 1.4, 3.4, 1.6, tones(GALOSH), gloss=0.7)
    # skirt + cardigan
    sp.union([sp.m_super(*Q(0.6, 10.0), 8.0, 5.6, 2.4)], tones(Y_SKIRT))
    body = sp.union([sp.m_ell(*Q(0.6, 20.0), 9.2, 9.0), sp.m_ell(*Q(2.4, 27.0), 8.0, 5.6)], tones(Y_CARD))
    sp.fill(body & (((DX.XC * 0.7 + DX.YC) % 2.4) < 0.35), dark(Y_CARD, 0.82))           # knit
    for q in range(3): sp.blob(Q(4.6, 24.0 - q * 3.2)[0], 24.0 - q * 3.2, 0.5, (200, 190, 150))  # buttons
    # shawl over the shoulders (back triangle)
    sh = sp.m_poly([Q(-8.4, 31.6), Q(10.4, 31.6), Q(8.0, 20.0), Q(1.0, 15.0), Q(-6.0, 20.0)])
    sp.paint(sh, tones(Y_SHAWL), None, olc=INK)
    for (cx, cy) in ((Q(-3.0, 24.6)), Q(5.0, 24.0), Q(1.0, 19.0)):
        sp.rose(cx, cy, 1.5, CINNABAR, sh)
    sp.fill(sh & ~erode(sh) & (DX.YC < 31.0), GOLD)                                      # gold fringe edge
    for q in range(9): thin(sp, Q(-5.0 + q * 1.2, 21.0 - abs(q - 4) * 1.2), Q(-5.2 + q * 1.2, 19.4 - abs(q - 4) * 1.2), GOLD, 0.18)
    # head in the shawl
    hx, hy = Q(4.6, 38.0)
    hood = sp.union([sp.m_ell(hx - 1.4, hy + 1.4, 10.4, 10.6)], tones(Y_SHAWL))
    sp.rose(hx - 6.2, hy + 5.6, 2.2, CINNABAR, hood); sp.rose(hx - 1.4, hy + 9.2, 1.7, CINNABAR, hood)
    for q in range(2): sp.ell(hx + 2.2 + q * 2.6, hy + 8.7, 1.5, 1.4, tones((220, 90, 150)), snow=False)   # бигуди
    face = sp.union([sp.m_ell(hx + 2.2, hy - 0.6, 6.7, 7.6)], tones(Y_SKIN))
    sp.gold(hood)
    for q in range(3): thin(sp, (hx - 1.4, hy - 1.4 - q * 1.1), (hx + 1.4, hy - 2.2 - q * 1.1), dark(Y_SKIN, 0.75), 0.18, mask=face)
    lx, ly = look
    DX.eye(sp, hx + 1.7, hy + 1.7, 3.8, 3.2, E, (70, 50, 40), (lx, ly), blink, lash=INK, skin=Y_SKIN, lidc=dark(Y_SKIN, 0.85), bag=dark(Y_SKIN, 0.75))
    DX.eye(sp, hx + 6.4, hy + 2.0, 3.4, 2.9, E, (70, 50, 40), (lx, ly), blink, lash=INK, skin=Y_SKIN, lidc=dark(Y_SKIN, 0.85))
    DX.brow(sp, hx + 6.4, hy + 4.8, 3.6, E, +1, (150, 146, 140), th=1.3, bushy=True)
    DX.brow(sp, hx + 1.4, hy + 4.5, 3.6, E, -1, (150, 146, 140), th=1.3, bushy=True)
    nose = sp.m_poly([(hx + 4.8, hy + 0.8), (hx + 14.6, hy - 4.8), (hx + 14.0, hy - 7.0), (hx + 6.2, hy - 3.6)])
    sp.paint(nose, tones(Y_NOSE), DX.lit(np.full_like(DX.XC, 0.4), np.full_like(DX.XC, 0.3)), olc=INK)
    sp.blob(hx + 9.8, hy - 1.4, 1.0, (150, 90, 70))                                     # the wart
    mx, my = hx + 4.8, hy - 5.6
    DX.mouth(sp, mx, my, 4.5, E, mouth_, INK, skin=Y_SKIN, maxh=6)
    thin(sp, (mx + 0.8, my - 0.3), (mx + 1.0, my - 2.5), (240, 232, 190), 0.55)          # the one long tooth
    sp.anchors['head'] = (hx, hy)
    # near arm
    shN = Q(6.0, 28.0)
    hn = hand_n if hand_n is not None else Q(10.0, 18.0)
    kN, eN = ik(shN, hn, 6.0, 6.0, -1.0)
    sp.cap(shN, kN, 2.0, 1.8, tones(Y_CARD)); sp.cap(kN, eN, 1.8, 1.6, tones(Y_CARD))
    sp.ell(eN[0], eN[1] - 0.6, 1.6, 1.7, tones(Y_SKIN))
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand_n'] = eN


# ================================================================================ домовой Кузьмич
def domovoy(sp, t=0.0, expr='zhut', mouth_=0.0, look=(0.9, -0.1), blink=None, glow=0.0):
    """ДОМОВОЙ КУЗЬМИЧ — lives in the stairwell электрощиток; «шар бороды»: knee-high (≈20 px), a ball of ash-grey beard and hair out of
    which only a red nose, two big serious eyes under bushy brows and two лапти stick out; a cinnabar косоворотка shows at the bottom;
    a lead ПЛОМБА from the meter hangs on a string as his medallion. Says one dry word straight to camera («Жуть.»).
    glow = the meter's LED blinking on him (0..1)."""
    E = X(expr)
    if blink is None: blink = (t % 3.3) < 0.14
    br = 0.25 * math.sin(t * 2.6)
    for dx in (-3.0, 3.4):
        sp.ell(dx + 1.0, 1.2, 2.6, 1.4, tones(D_LAPTI))
        sp.fill(sp.m_ell(dx + 1.0, 1.2, 2.6, 1.4)[0] & (((DX.XC + DX.YC) % 1.2) < 0.3), dark(D_LAPTI, 0.7))
    shirt = sp.union([sp.m_super(0.4, 4.6, 6.0, 3.0, 2.4)], tones(D_SHIRT))
    sp.fill(shirt & (np.abs(DX.YC - 3.0) < 0.35), GOLD)                                  # embroidered hem
    ball = sp.union([sp.m_ell(0.4, 12.0 + br, 8.4, 8.6), sp.m_ell(0.8, 7.4, 7.4, 4.0)], tones(D_BEARD))
    sp.fur(ball, dark(D_BEARD, 0.72), step=2.0, ln=1.6, ang=-1.6, seed=31)
    sp.gold(ball)
    lx, ly = look
    DX.eye(sp, 0.2, 13.6 + br, 3.0, 3.0, E, (90, 64, 40), (lx, ly), blink, lash=INK, skin=D_BEARD, lidc=dark(D_BEARD, 0.85))
    DX.eye(sp, 4.0, 13.8 + br, 2.8, 2.8, E, (90, 64, 40), (lx, ly), blink, lash=INK, skin=D_BEARD, lidc=dark(D_BEARD, 0.85))
    DX.brow(sp, 4.0, 16.6 + br, 3.4, E, +1, mix(D_BEARD, WHITE, 0.5), th=1.2, bushy=True)
    DX.brow(sp, 0.0, 16.4 + br, 3.4, E, -1, mix(D_BEARD, WHITE, 0.5), th=1.2, bushy=True)
    sp.ell(3.8, 10.8 + br, 2.0, 1.6, tones(D_NOSE), gloss=1.0, snow=False)
    if max(mouth_, E['mo']) > 0.1:
        sp.fill(sp.m_ell(3.2, 8.0 + br, 1.4, 0.5 + 0.9 * mouth_)[0], (70, 20, 24))
    thin(sp, (-1.0, 9.6), (1.6, 6.6), (90, 90, 96), 0.18); thin(sp, (4.4, 9.4), (1.6, 6.6), (90, 90, 96), 0.18)
    seal = sp.ell(1.6, 5.8, 1.3, 1.3, tones((150, 154, 164)), gloss=0.6, snow=False)
    if glow > 0: sp.blob(-4.4, 16.0 + br, 0.6 + 0.4 * glow, mix((255, 60, 40), (255, 220, 200), 0.3 * glow))
    sp.anchors['head'] = (1.6, 12.6)


# ================================================================================ Галина Аркадьевна («система» в каждом окошке)
G_SKIN = (232, 186, 160)
G_HAIR = (150, 64, 44)              # хна, химзавивка
G_CARD = (110, 70, 120)             # кофта
G_BLOUSE = (236, 226, 210)


def galina(sp, t=0.0, expr='deadpan', mouth_=0.0, look=(-0.6, -0.2), blink=None, hand_n=None, prop_n=None, biscuit=False, chew=False,
           hand_f=None, prop_f=None, scared=0.0):
    """ГАЛИНА АРКАДЬЕВНА — the clerk in every window: a round «кубышка» (≈42 px) with a big rusty-henna perm, glasses on a chain,
    a violet cardigan with an amber brooch, a ring biscuit in her teeth; facing +x like everyone (flip=True to face left).
    scared = 0..1 (E05): shoulders up, the perm bristles, she shrinks"""
    E = X(expr)
    if blink is None: blink = (t % 4.8) < 0.12
    br = 0.25 * math.sin(t * 1.7)
    sh = 1.6 * scared
    ch = (math.sin(t * 9.0) * 0.5 + 0.5) if chew else 0.0
    sp.cap((-3.0, 8.0), (-3.2, 2.0), 2.6, 2.4, tones((60, 50, 54))); sp.ell(-2.0, 1.2, 3.4, 1.6, tones((40, 34, 36)))
    sp.cap((3.0, 8.0), (3.4, 2.0), 2.6, 2.4, tones((70, 60, 64))); sp.ell(4.6, 1.2, 3.4, 1.6, tones((40, 34, 36)))
    sp.union([sp.m_super(0.4, 12.0, 8.8, 5.0, 2.4)], tones((60, 60, 72)))                             # skirt
    body = sp.union([sp.m_ell(0.4, 22.0, 10.4, 9.6)], tones(G_CARD))
    sp.fill(body & (np.abs(DX.XC - 4.6) < 0.5), dark(G_CARD, 0.7))
    sp.ell(5.2, 26.0, 2.4, 3.0, tones(G_BLOUSE), snow=False)
    sp.ell(5.6, 25.0, 1.1, 1.1, tones((230, 150, 40)), gloss=0.9, snow=False)                        # amber brooch
    hf = hand_f if hand_f is not None else (-6.0, 15.0)
    kF, eF = ik((-7.0, 27.0 + sh), hf, 6.0, 6.0, -1.0)
    sp.cap((-7.0, 27.0 + sh), kF, 2.4, 2.2, tones(dark(G_CARD, 0.8))); sp.cap(kF, eF, 2.2, 2.0, tones(dark(G_CARD, 0.8)))
    sp.ell(eF[0], eF[1], 1.7, 1.7, tones(dark(G_SKIN, 0.85)))
    if prop_f: prop_f(sp, eF)
    sp.anchors['hand_f'] = eF
    hx, hy = 3.0, 38.0 - sh * 0.6
    hair = sp.union([sp.m_ell(hx - 1.4, hy + 3.2 + sh * 0.3, 9.4 + sh, 8.4 + sh), sp.m_ell(hx - 6.0, hy - 1.0, 4.4, 5.0)], tones(G_HAIR))
    rng = np.random.default_rng(5)
    for q in range(26):                                                                                 # perm curls
        a_ = rng.random() * 6.28; r_ = rng.random() * 7.6
        sp.curl(hx - 1.4 + math.cos(a_) * r_, hy + 3.2 + math.sin(a_) * r_ * 0.85, 1.0, dark(G_HAIR, 0.66), turns=0.9, w=0.22, mask=hair, seed=q)
    face = sp.union([sp.m_ell(hx + 1.4, hy - 0.6, 6.6, 7.0)], tones(G_SKIN))
    DX.blush(sp, hx + 4.0, hy - 2.6, 1.8, 1.0, (230, 130, 130))
    lx, ly = look
    DX.eye(sp, hx + 0.4, hy + 0.8, 3.6, 3.0, E, (90, 70, 50), (lx, ly), blink, lash=INK, skin=G_SKIN, lidc=dark(G_SKIN, 0.86))
    DX.eye(sp, hx + 5.0, hy + 1.0, 3.4, 2.8, E, (90, 70, 50), (lx, ly), blink, lash=INK, skin=G_SKIN, lidc=dark(G_SKIN, 0.86))
    for (cx, w_) in ((hx + 0.4, 2.4), (hx + 5.0, 2.2)):                                                 # glasses
        m = sp.m_ell(cx, hy + 0.8, w_ + 0.3, 2.1)[0]
        sp.fill(m & ~erode(m), (120, 90, 50))
    thin(sp, (hx + 2.7, hy + 1.2), (hx + 2.9, hy + 1.2), (120, 90, 50), 0.3)
    for q in range(10): sp.blob(hx - 2.2 - q * 0.25, hy + 0.4 - q * 1.6, 0.25, GOLD)                    # the chain
    DX.brow(sp, hx + 5.2, hy + 3.8, 3.2, E, +1, dark(G_HAIR, 0.6), th=0.9)
    DX.brow(sp, hx + 0.2, hy + 3.6, 3.2, E, -1, dark(G_HAIR, 0.6), th=0.9)
    sp.ell(hx + 4.4, hy - 1.6, 1.4, 1.6, tones(dark(G_SKIN, 0.92)), snow=False)
    mx, my = hx + 3.4, hy - 4.6
    DX.mouth(sp, mx, my, 3.6, E, max(mouth_, ch * 0.25), (170, 50, 70), skin=G_SKIN, maxh=5)
    if biscuit:
        b = sp.m_ell(mx + 2.8, my + 0.4, 2.4, 2.0)[0]
        sp.paint(b & ~sp.m_ell(mx + 2.8, my + 0.4, 0.9, 0.8)[0], tones((214, 160, 90)), None, olc=dark((214, 160, 90), 0.5))
    sp.anchors['head'] = (hx, hy)
    hn = hand_n if hand_n is not None else (9.0, 16.0)
    kN, eN = ik((7.0, 27.0 + sh), hn, 6.0, 6.0, -1.0)
    sp.cap((7.0, 27.0 + sh), kN, 2.4, 2.2, tones(G_CARD)); sp.cap(kN, eN, 2.2, 2.0, tones(G_CARD))
    sp.ell(eN[0], eN[1], 1.7, 1.7, tones(G_SKIN))
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand_n'] = eN


def stamp(sp, h, up=0.0):
    """rubber stamp (ПЕЧАТЬ) in a hand; up lifts it"""
    x, y = h
    sp.cap((x, y + up), (x, y + 4.0 + up), 1.0, 0.8, tones((120, 70, 40)))
    sp.ell(x, y + 4.6 + up, 1.6, 1.4, tones((120, 70, 40)), gloss=0.6, snow=False)
    sp.sup(x, y - 0.6 + up, 2.4, 0.9, tones((60, 60, 70)), snow=False)


def cutters(sp, h, open_=0.4):
    """big bolt cutters (E05): red handles hang DOWN from the hand, steel jaws point UP above it"""
    x, y = h
    for s_ in (-1, 1):
        thin(sp, (x, y), (x + s_ * (1.0 + 1.6 * open_), y - 9.0), (196, 40, 40), 0.7)
        thin(sp, (x, y), (x + s_ * (0.4 + 1.2 * open_), y + 4.0), (170, 176, 186), 0.6)
    sp.blob(x, y, 0.8, (120, 124, 134))


# ================================================================================ Змей Горыныч (сосед сверху, три головы)
GR = (88, 150, 70)
GR_B = (196, 210, 120)


def gorynych(sp, t=0.0, exprs=('normal', 'normal', 'normal'), mouths=(0.0, 0.0, 0.0), looks=None, hats=False, phones=False, drills=None,
             duvet=0.0, laptop=False, wave=0.0):
    """ЗМЕЙ ГОРЫНЫЧ — a pear-bodied green dragon in a striped tank top, three necks: head 1 (front, polite operator with a headset),
    head 2 (big, gruff bass), head 3 (small, squeaky). hats = three hard hats (E03), phones = a phone at each head (E02),
    drills = list of 3 drill angles or None (E03), duvet = each head under its own blanket (0..1, E03 night), wave = paw wave (E02)"""
    looks = looks or [(0.7, 0.0)] * 3
    br = 0.3 * math.sin(t * 2.0)
    sp.ell(-10.0, 6.0, 6.0, 3.0, tones(dark(GR, 0.8)))                                                   # tail
    sp.cap((-10.0, 6.0), (-18.0, 3.0 + math.sin(t * 2) * 1.0), 2.4, 1.0, tones(dark(GR, 0.8)))
    for dx in (-5.0, 5.0):
        sp.cap((dx, 8.0), (dx + 1.0, 2.0), 3.2, 3.0, tones(GR)); sp.ell(dx + 2.4, 1.4, 4.2, 1.6, tones(dark(GR, 0.7)))
    body = sp.union([sp.m_ell(0.0, 20.0 + br * 0.2, 13.0, 14.0)], tones(GR))
    belly = sp.ell(3.0, 19.0, 8.4, 10.6, tones(GR_B), snow=False)
    sp.fill(belly & ((DX.YC % 2.6) < 0.5), dark(GR_B, 0.85))
    tank = sp.m_poly([(-9.0, 12.0), (11.0, 12.0), (10.0, 28.0), (5.0, 30.0), (-4.0, 30.0), (-9.0, 27.0)])
    sp.paint(tank & body, tones((236, 236, 230)), None, olc=dark((236, 236, 230), 0.6))
    sp.fill(tank & body & ((DX.YC % 2.4) < 0.7), (60, 90, 170))                                           # striped тельняшка
    # three necks + heads
    heads = [((-8.0, 31.0), (-14.0, 45.0), 1.0), ((1.0, 33.0), (2.0, 51.0), 1.25), ((9.0, 31.0), (16.0, 44.0), 0.8)]
    for i, (base, hp, k) in enumerate(heads):
        sway = math.sin(t * 2.0 + i * 1.7) * 0.8
        hx, hy = hp[0] + sway, hp[1]
        sp.cap(base, (hx - 1.0, hy - 3.0 * k), 3.0 * k, 2.4 * k, tones(GR))
        E = X(exprs[i])
        head = sp.union([sp.m_ell(hx, hy, 5.4 * k, 4.6 * k), sp.m_ell(hx + 4.0 * k, hy - 1.4 * k, 4.0 * k, 3.0 * k)], tones(GR))
        sp.gold(head)
        for q in range(3): sp.ell(hx - 3.0 * k + q * 2.0 * k, hy + 4.4 * k, 0.9 * k, 1.2 * k, tones((230, 120, 50)), snow=False)   # crest
        sp.blob(hx + 7.0 * k, hy - 0.6 * k, 0.45 * k, dark(GR, 0.4))                                    # nostril
        lx, ly = looks[i]
        DX.eye(sp, hx + 1.4 * k, hy + 1.2 * k, 3.2 * k, 2.8 * k, E, (230, 180, 40), (lx, ly), (t + i) % 3.7 < 0.12, lash=INK, skin=GR,
               lidc=dark(GR, 0.85), slit=True)
        DX.brow(sp, hx + 1.4 * k, hy + 3.4 * k, 3.0 * k, E, +1, dark(GR, 0.55), th=0.9)
        DX.mouth(sp, hx + 4.4 * k, hy - 2.6 * k, 4.4 * k, E, mouths[i], dark(GR, 0.45), skin=GR, maxh=4 * k, big_teeth=True)
        sp.anchors[f'head{i + 1}'] = (hx, hy)
        if hats:
            hat = sp.union([sp.m_ell(hx - 0.4, hy + 3.6 * k, 5.6 * k, 3.4 * k)], tones((250, 200, 40)))
            sp.fill(hat & (DX.YC < hy + 2.0 * k), (250, 200, 40)); sp.cap((hx - 6.4 * k, hy + 2.2 * k), (hx + 5.6 * k, hy + 2.2 * k), 0.6 * k, 0.6 * k, tones((230, 170, 30)))
        if phones:
            ph = sp.m_super(hx - 3.4 * k, hy - 1.0 * k, 1.2 * k, 2.6 * k, 3.0)[0]
            sp.paint(ph, tones((40, 40, 46)), None, olc=INK)
            sp.fill(sp.m_ell(hx - 3.4 * k, hy + 0.2 * k, 0.6 * k, 0.6 * k)[0], (90, 200, 120))
        if drills is not None:
            a = drills[i]; dxh, dyh = hx + 6.0 * k, hy - 3.0 * k
            sp.sup(dxh, dyh, 2.6 * k, 1.6 * k, tones((40, 110, 200)), snow=False)
            thin(sp, (dxh + 2.4 * k, dyh), (dxh + 2.4 * k + math.cos(a) * 5.0 * k, dyh + math.sin(a) * 5.0 * k), (190, 196, 206), 0.4 * k)
        if duvet > 0:
            dv = sp.m_ell(hx + 0.6, hy - 1.0 * k + 8.0 * (1 - duvet), 6.6 * k, 5.6 * k)[0] & (DX.YC < hy + 6.0 * k)
            sp.paint(dv, tones([(220, 120, 140), (110, 160, 220), (240, 200, 90)][i]), None, olc=INK)
    if laptop:
        sp.sup(12.0, 18.0, 6.0, 1.0, tones((60, 60, 70)), snow=False)
        sc = sp.m_poly([(8.0, 19.0), (16.0, 19.0), (17.0, 26.0), (9.0, 26.0)])
        sp.paint(sc, tones((40, 40, 48)), None, olc=INK)
        sp.fill(sp.m_poly([(9.0, 20.0), (15.6, 20.0), (16.4, 25.2), (9.8, 25.2)]), (120, 200, 255))
        sp.txt_box(['КОЛЛ-', 'ЦЕНТР'], (9.4, 20.2, 16.0, 25.0), (20, 40, 80), pad=0.2)
    if wave:
        sp.cap((10.0, 26.0), (17.0, 32.0 + math.sin(t * 14) * 2.0 * wave), 2.2, 1.8, tones(GR))
        sp.ell(17.4, 33.0 + math.sin(t * 14) * 2.0 * wave, 2.0, 2.2, tones(GR))
    sp.anchors['head'] = heads[1][1]


# ================================================================================ ряженые студенты (E06, 18+)
def student(sp, t=0.0, costume='zombie', expr='grin', mouth_=0.0, look=(0.7, 0.0), blink=None, hand_n=None, prop_n=None, bag=True):
    """a university student in a trick-or-treat costume: zombie (green face paint, torn shirt), vampire (cape, fangs, slick hair)
    or skeleton (black onesie with bones). ≈50 px, lanky, sneakers, a paper bag for candy."""
    E = X(expr)
    if blink is None: blink = (t % 3.5) < 0.12
    skin = (150, 196, 130) if costume == 'zombie' else (236, 226, 220) if costume == 'vampire' else (232, 190, 160)
    shirt = {'zombie': (120, 110, 90), 'vampire': (30, 26, 34), 'skeleton': (26, 26, 30)}[costume]
    if costume == 'vampire':
        cape = sp.m_poly([(-9.0, 40.0), (8.0, 40.0), (13.0, 6.0), (-14.0, 6.0)])
        sp.paint(cape, tones((150, 20, 30)), None, olc=INK)
    for dx in (-2.6, 2.6):
        sp.cap((dx, 24.0), (dx + 0.4, 3.0), 2.2, 2.0, tones((50, 70, 120) if costume != 'skeleton' else shirt))
        sp.ell(dx + 1.6, 1.4, 3.4, 1.6, tones((240, 240, 240)))
        if costume == 'skeleton':
            for q in range(3): sp.cap((dx, 21.0 - q * 6.0), (dx + 0.3, 18.0 - q * 6.0), 0.6, 0.6, tones(BONE), snow=False)
    body = sp.union([sp.m_super(0.0, 32.0, 6.4, 9.0, 2.4)], tones(shirt))
    if costume == 'zombie':
        for q in range(4): sp.fill(body & sp.m_poly([(-6.4 + q * 3.4, 23.0), (-4.6 + q * 3.4, 23.0), (-5.4 + q * 3.4, 26.0)]), (0, 0, 0))
        sp.fill(body & sp.m_ell(2.0, 34.0, 1.6, 1.2)[0], (150, 30, 30))
    if costume == 'skeleton':
        for q in range(4): thin(sp, (-4.0, 36.0 - q * 2.4), (4.0, 36.0 - q * 2.4), BONE, 0.4)
        thin(sp, (0.0, 38.0), (0.0, 26.0), BONE, 0.5)
    if costume == 'vampire':
        sp.fill(body & sp.m_poly([(-1.6, 41.0), (1.6, 41.0), (0.0, 30.0)]), (240, 240, 240))
        sp.fill(sp.m_poly([(-4.0, 42.0), (4.0, 42.0), (7.0, 46.0), (-7.0, 46.0)]), (150, 20, 30))
    hx, hy = 1.4, 48.0
    head = sp.union([sp.m_ell(hx, hy, 6.0, 6.8)], tones(skin))
    if costume == 'skeleton':
        sp.fill(head & ~sp.m_ell(hx + 1.6, hy - 1.0, 4.4, 5.2)[0], (26, 26, 30))
    hair = {'zombie': (60, 40, 30), 'vampire': (20, 20, 26), 'skeleton': (26, 26, 30)}[costume]
    sp.union([sp.m_ell(hx - 1.0, hy + 4.8, 6.0, 2.8)], tones(hair))
    if costume == 'zombie':
        thin(sp, (hx - 2.0, hy - 2.0), (hx + 1.0, hy - 4.0), (150, 30, 30), 0.3); thin(sp, (hx + 3.0, hy + 3.0), (hx + 4.4, hy + 1.6), (60, 90, 50), 0.3)
    lx, ly = look
    DX.eye(sp, hx + 0.4, hy + 0.8, 3.2, 2.8, E, (70, 60, 50) if costume != 'vampire' else (190, 30, 30), (lx, ly), blink, lash=INK, skin=skin,
           bag=(90, 120, 80) if costume == 'zombie' else None)
    DX.eye(sp, hx + 4.4, hy + 1.0, 3.0, 2.6, E, (70, 60, 50) if costume != 'vampire' else (190, 30, 30), (lx, ly), blink, lash=INK, skin=skin)
    DX.brow(sp, hx + 4.4, hy + 3.2, 2.8, E, +1, hair, th=0.9)
    DX.brow(sp, hx + 0.4, hy + 3.0, 2.8, E, -1, hair, th=0.9)
    sp.ell(hx + 3.6, hy - 1.4, 1.2, 1.4, tones(dark(skin, 0.9)), snow=False)
    mx, my = hx + 3.0, hy - 3.8
    DX.mouth(sp, mx, my, 3.6, E, mouth_, INK, skin=skin, maxh=5)
    if costume == 'vampire':
        for dx in (-0.8, 0.8): thin(sp, (mx + dx, my + 0.2), (mx + dx, my - 1.2), WHITE, 0.3)
    sp.anchors['head'] = (hx, hy)
    hn = hand_n if hand_n is not None else (8.0, 26.0)
    kN, eN = ik((4.0, 39.0), hn, 7.0, 7.0, -1.0)
    sp.cap((4.0, 39.0), kN, 1.8, 1.6, tones(shirt)); sp.cap(kN, eN, 1.6, 1.4, tones(shirt))
    sp.ell(eN[0], eN[1], 1.5, 1.5, tones(skin))
    if bag:
        b = sp.m_super(eN[0] + 1.0, eN[1] - 4.0, 2.6, 3.4, 3.0)[0]
        sp.paint(b, tones((200, 160, 110)), None, olc=dark((200, 160, 110), 0.5))
        sp.ell(eN[0] + 1.0, eN[1] - 4.0, 1.0, 0.9, tones((240, 140, 40)), snow=False)
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand_n'] = eN


# ================================================================================ избушка на курьих ножках (Яга's «ракушка»)
def izba(sp, t=0.0, sit=0.0, cluck=0.0, lit=1.0, steam=True, sign=True, egg=0.0, step=None):
    """the hut on chicken legs: a small log cabin (≈34 px box) on two scaly yellow chicken legs. sit = 0 standing .. 1 brooding on the
    pipe (legs folded, body lowered, feathers fluff out); cluck = body bob; egg = a hot egg rolling out from under it (0..1)."""
    bob = math.sin(t * 18.0) * 1.2 * cluck
    leg_h = 22.0 * (1 - sit)
    base = 4.0 + leg_h + bob
    if sit < 0.9:
        for dx, ph in ((-7.0, 0.0), (7.0, 1.7)):
            st_ = math.sin(step + ph) * 3.0 if step is not None else 0.0
            knee = (dx + 4.0 + st_ * 0.5, 4.0 + leg_h * 0.55)
            sp.cap((dx, base), knee, 2.0, 1.6, tones((240, 190, 60)))
            sp.cap(knee, (dx + st_, 3.0), 1.6, 1.3, tones((240, 190, 60)))
            for a in (-0.5, 0.0, 0.5):
                thin(sp, (dx + st_, 2.6), (dx + st_ + math.sin(a) * 5.0 + 2.0, 0.6), (220, 160, 40), 0.5)
            for q in range(4): thin(sp, (knee[0] - 1.4, knee[1] - q * 2.4), (knee[0] + 1.4, knee[1] - q * 2.4 - 0.4), (190, 130, 30), 0.18)
    feathers = sp.m_ell(0.0, base + 1.0, 18.0, 4.0 + 3.0 * sit)[0]
    sp.paint(feathers, tones((236, 220, 200)), None, olc=dark((236, 220, 200), 0.5))
    for q in range(12): sp.blob(-16.0 + q * 2.9, base - 0.6 - 1.6 * sit, 1.2 + 0.6 * sit, (250, 240, 228))
    logs = sp.union([sp.m_super(0.0, base + 14.0, 15.0, 12.0, 4.0)], tones((140, 90, 50)))
    for q in range(6): sp.fill(logs & (np.abs(DX.YC - (base + 4.0 + q * 4.0)) < 0.45), dark((140, 90, 50), 0.6))
    for q in range(6):
        y_ = base + 4.0 + q * 4.0
        sp.ell(-15.4, y_ + 2.0, 1.6, 1.8, tones((180, 130, 80)), snow=False); sp.ell(15.4, y_ + 2.0, 1.6, 1.8, tones((180, 130, 80)), snow=False)
    roof = sp.m_poly([(-19.0, base + 25.0), (19.0, base + 25.0), (0.0, base + 40.0)])
    sp.paint(roof, tones((80, 60, 50)), DX.lit(np.clip((DX.XC) / 19.0, -0.9, 0.9), np.full_like(DX.XC, 0.3)), olc=INK)
    for q in range(5): thin(sp, (-16.0 + q * 2.0, base + 25.5 + q * 2.8), (16.0 - q * 2.0, base + 25.5 + q * 2.8), dark((80, 60, 50), 0.6), 0.3)
    sp.cap((10.0, base + 30.0), (10.0, base + 38.0), 1.6, 1.6, tones((150, 70, 60)))
    win = sp.m_super(1.0, base + 15.0, 5.0, 4.6, 4.0)[0]
    sp.fill(win, mix((40, 30, 30), (255, 210, 120), lit))
    sp.fill(win & ~erode(win), (230, 200, 120))
    sp.fill(win & (np.abs(DX.XC - 1.0) < 0.35), (110, 80, 50)); sp.fill(win & (np.abs(DX.YC - (base + 15.0)) < 0.35), (110, 80, 50))
    for dx in (-6.4, 8.4):                                                                              # carved shutters
        sh = sp.m_super(1.0 + dx, base + 15.0, 1.6, 4.8, 3.0)[0]
        sp.paint(sh, tones(KX.CINNABAR), None, olc=INK)
        sp.curl(1.0 + dx, base + 15.6, 1.0, GOLD, turns=1.0, w=0.2, mask=sh)
    if sign:
        sp.sup(-8.0, base + 8.0, 5.4, 2.2, tones((240, 236, 220)), snow=False)
        sp.txt_box(['ЧАСТНАЯ', 'ТЕРРИТОРИЯ'], (-13.2, base + 6.0, -2.8, base + 10.0), KX.CINNABAR, pad=0.15)
    sp.anchors['chimney'] = (10.0, base + 39.0)
    sp.anchors['window'] = (1.0, base + 15.0)
    if egg > 0:
        ex = -4.0 + 14.0 * egg
        sp.ell(ex, 3.2, 2.6, 3.2, tones((250, 236, 210)), gloss=0.8, snow=False)
        sp.anchors['egg'] = (ex, 3.2)
    sp.anchors['head'] = (1.0, base + 15.0)


# ================================================================================ гроб на табуретках, думка
def coffin(sp, t=0.0, lid=0.0, jump=0.0, stools=True):
    """a hexagonal wooden coffin on two kitchen stools (side view, ≈44 px long), a «думка» pillow with embroidery «СПИ, МОЯ РАДОСТЬ»
    at the head (+x side). lid 0 closed .. 1 propped open behind; jump = the lid hopping (drill vibration)"""
    y0 = 14.0 if stools else 0.0
    if stools:
        for dx in (-14.0, 14.0):
            sp.sup(dx, y0 - 0.8, 6.0, 0.9, tones((150, 110, 70)), snow=False)
            for e in (-4.6, 4.6): sp.cap((dx + e, y0 - 1.6), (dx + e * 1.1, 0.4), 0.7, 0.7, tones((120, 86, 56)))
    box = sp.m_poly([(-22.0, y0 + 1.0), (20.0, y0 + 1.0), (24.0, y0 + 5.0), (20.0, y0 + 9.0), (-22.0, y0 + 9.0), (-24.0, y0 + 5.0)])
    sp.paint(box, tones((120, 70, 40)), DX.lit(np.zeros_like(DX.XC), np.clip((DX.YC - y0 - 5.0) / 5.0, -0.9, 0.9)), olc=INK)
    sp.fill(box & (np.abs(DX.YC - (y0 + 8.4)) < 0.4), GOLD)
    sp.ell(17.0, y0 + 9.6, 4.4, 1.8, tones((240, 236, 226)), snow=False)                                 # думка
    sp.curl(17.0, y0 + 9.8, 0.9, KX.CINNABAR, turns=1.0, w=0.2)
    if lid > 0:
        a = 1.3 * lid
        top = y0 + 9.0 + 1.0 * abs(math.sin(t * 40)) * jump
        p0 = (-22.0, top)
        p1 = (-22.0 + 46.0 * math.cos(a), top + 46.0 * math.sin(a))
        sp.cap(p0, p1, 1.6, 1.6, tones((140, 84, 50)))
    else:
        top = y0 + 9.0 + 1.6 * abs(math.sin(t * 40)) * jump
        lidm = sp.m_poly([(-22.0, top), (20.0, top), (22.0, top + 2.4), (-22.0, top + 2.4)])
        sp.paint(lidm, tones((140, 84, 50)), None, olc=INK)
    sp.anchors['pillow'] = (16.0, y0 + 11.0)


# ================================================================================ small props
def phone_btn(sp, h, glow=0.0, env=False):
    """кнопочный телефон at the ear / in the hand; env = blinking SMS envelope on the screen"""
    x, y = h
    body = sp.m_super(x, y + 3.2, 1.6, 3.6, 3.0)[0]
    sp.paint(body, tones((70, 74, 86)), None, olc=INK)
    sp.fill(sp.m_super(x, y + 4.8, 1.2, 1.2, 3.0)[0], mix((40, 70, 60), (150, 255, 170), 0.4 + 0.6 * glow))
    if env: sp.fill(sp.m_super(x, y + 4.8, 0.8, 0.5, 3.0)[0], (255, 255, 255))
    for q in range(3): sp.blob(x - 0.6 + q * 0.6, y + 1.4, 0.25, (200, 204, 214))
    sp.anchors['phone'] = (x, y + 3.2)


def duck(sp, h):
    """хрустальная утка (her egg-and-needle inside)"""
    x, y = h
    b = sp.ell(x, y + 2.6, 4.0, 2.6, [(150, 190, 210), (210, 236, 250), (250, 254, 255)], gloss=1.2, snow=False)
    sp.ell(x + 3.4, y + 5.4, 1.8, 1.8, [(150, 190, 210), (210, 236, 250), (250, 254, 255)], gloss=1.2, snow=False)
    sp.blob(x + 5.4, y + 5.2, 0.8, (230, 220, 160))
    sp.fill(b & (((DX.XC - DX.YC) % 1.6) < 0.3), (255, 255, 255))


def cake(sp, h, n=60, lit=1.0, t=0.0):
    """юбилейный торт «1000» with a forest of candles (n candles)"""
    x, y = h
    sp.sup(x, y + 2.4, 9.0, 2.6, tones((240, 220, 200)), snow=False)
    sp.fill(sp.m_super(x, y + 4.4, 9.0, 0.7, 3.0)[0], (230, 120, 160))
    sp.txt_box(['1000'], (x - 6.0, y + 0.6, x + 6.0, y + 4.0), KX.CINNABAR, pad=0.1)
    rng = np.random.default_rng(1)
    for q in range(n):
        cx = x - 8.0 + rng.random() * 16.0; ch = 2.0 + rng.random() * 3.0
        thin(sp, (cx, y + 5.0), (cx, y + 5.0 + ch), [(250, 240, 120), (150, 200, 255), (255, 160, 200)][q % 3], 0.18)
        if lit: sp.blob(cx, y + 5.6 + ch, 0.35 + 0.15 * math.sin(t * 20 + q), (255, 200 + int(40 * rng.random()), 80))
    sp.anchors['cake'] = (x, y + 6.0)


def zucchini(sp, h, lit=1.0):
    """кабачок-фонарь (pumpkins are 1499 ₽): a carved zucchini with a candle face"""
    x, y = h
    z = sp.ell(x, y + 2.0, 5.6, 2.4, tones((70, 130, 60)), snow=False)
    sp.fill(z & (np.abs(DX.YC - (y + 2.6)) < 0.25), dark((70, 130, 60), 0.7))
    for (ex, ey) in ((x - 1.6, y + 2.6), (x + 1.6, y + 2.6)): sp.fill(sp.m_poly([(ex - 0.6, ey - 0.4), (ex + 0.6, ey - 0.4), (ex, ey + 0.6)]), mix((40, 20, 10), (255, 210, 90), lit))
    sp.fill(sp.m_ell(x, y + 1.0, 1.8, 0.5)[0], mix((40, 20, 10), (255, 210, 90), lit))


def coins(sp, h):
    x, y = h
    for q in range(4): sp.ell(x - 1.4 + q * 1.0, y + 0.6 + (q % 2) * 0.6, 0.9, 0.6, tones((200, 170, 90)), gloss=0.8, snow=False)


def candy(sp, h, col=(220, 40, 60)):
    x, y = h
    sp.ell(x, y, 1.4, 0.9, tones(col), snow=False)
    for s_ in (-1, 1): sp.fill(sp.m_poly([(x + s_ * 1.2, y), (x + s_ * 2.4, y + 0.9), (x + s_ * 2.4, y - 0.9)]), col)
