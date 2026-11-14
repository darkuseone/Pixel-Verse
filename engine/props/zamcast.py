"""«Замело» cast + props in the «Морозное утро» manner (props/zampix.py). Coordinates: sprite px, feet anchor at (0, 0),
x right = facing side, y UP. Rim light and the ink outline are added by zampix.Act / zampix.draw — draw functions do NOT outline.
  zhora(sp, ...)  — Жора, 42: «a tangerine with an antenna» — a round orange down «alaska» with a fur hood, a tall red-white knitted
                    cone hat «петушок» with a pompon, a striped telnyashka at the neck, a frosty brush moustache, rosy frost cheeks,
                    icicle brows, a potato nose, grey felt valenki, red knitted mittens; a shovel or a phone in the hand
  chayka(sp, ...) — the seagull: a fat scruffy white sea bird, grey wings with black tips, a droopy lid, a yellow beak with a red spot,
                    an orange ring on the leg; the beak talks
  ira(sp, ...)    — Ира, 40: pink flowered halat over a sweater, a grey down shawl, a brown bun with a big claw clip, slippers
  vitek(sp, ...)  — Витёк, 27: a skinny courier in a violet «ОЗНОБ» jacket and cap, a big cube thermal backpack; lean=… bends over
  nina(sp, ...)   — баба Нина: a round granny in a red polka-dot headscarf, big round glasses, a green cardigan, a watering can
  props: phone (with a screen), parcel (ОЗНОБ tape), shovel"""
import math
import numpy as np
from props import dibspix as DX
from props.dibspix import dark, mix, erode, dilate, ik, EXPR
from props.zampix import tones, thin, stroke, INK, WHITE

# ---------------------------------------------------------------- palette
ALASKA = (255, 128, 30)            # Жора's orange down jacket
FUR = (150, 104, 66)
SKIN_Z = (244, 186, 150)
CHEEK = (236, 92, 92)
NOSE = (232, 120, 110)
MOUST = (110, 70, 44)
HAT_R, HAT_W = (214, 36, 48), (248, 246, 240)
PANTS = (52, 60, 92)
VALENKI = (150, 146, 140)
MITT = (200, 40, 50)
TELNIK_B = (40, 70, 160)
SNOWC = (236, 244, 255)
GULL_W, GULL_G = (246, 246, 244), (150, 160, 178)
BEAK = (250, 204, 50)
GULL_LEG = (240, 150, 110)
HALAT = (246, 130, 170)
SHAWL = (170, 170, 178)
HAIR_I = (120, 66, 40)
SKIN_I = (246, 200, 172)
VIOLET = (120, 60, 200)
VIOLET_D = (80, 36, 150)
SKIN_V = (236, 190, 160)
SCARF_N = (214, 40, 50)
CARDI = (80, 140, 90)
SKIN_N = (238, 196, 170)

XTRA = dict(
    proud=dict(eo=1.0, pu=0.6, bt=0.2, bl=0.3, mo=0.0, mc=0.8, teeth=True),
    outraged=dict(eo=1.3, pu=0.32, bt=0.75, bl=0.2, mo=0.9, mc=-0.3),
    gloomy=dict(eo=0.65, pu=0.55, bt=0.55, bl=-0.3, mo=0.0, mc=-0.6, lid=0.45),
    exhausted=dict(eo=0.6, pu=0.6, bt=-0.6, bl=0.2, mo=0.3, mc=-0.4, lid=0.4),
    offended=dict(eo=1.15, pu=0.45, bt=-0.5, bl=0.6, mo=0.6, mc=-0.5),
    cocky=dict(eo=0.9, pu=0.6, bt=0.35, bl=0.1, mo=0.0, mc=0.7, lid=0.25),
    dry=dict(eo=0.55, pu=0.6, bt=0.1, bl=-0.1, mo=0.0, mc=-0.1, lid=0.6),
    chew=dict(eo=0.5, pu=0.6, bt=0.0, bl=0.0, mo=0.0, mc=0.1, lid=0.65),
    cheerful=dict(eo=1.0, pu=0.62, bt=-0.2, bl=0.3, mo=0.0, mc=0.9, teeth=True),
    kind=dict(eo=0.8, pu=0.65, bt=-0.4, bl=0.3, mo=0.0, mc=0.6),
    yelling=dict(eo=1.15, pu=0.5, bt=0.2, bl=0.5, mo=0.9, mc=0.2),
)


def X(expr):
    if isinstance(expr, dict): return dict(expr)                  # smooth mimic (props/mimic.py) passes a ready dict
    return dict(XTRA.get(expr) or EXPR.get(expr, EXPR['normal']))


def _arm_over(sp, before):
    new = sp.m & ~before
    o = dilate(new) & ~sp.m & before
    sp.col[o] = INK


# ================================================================================ hand props
def phone(sp, h, lit=True, screen=(255, 255, 255)):
    """a smartphone held upright: dark body, a bright screen with a violet ОЗНОБ bar"""
    x, y = h
    sp.sup(x + 0.4, y + 4.2, 2.6, 4.6, tones((40, 40, 52)), n=4.0, frost=False)
    sc = sp.m_super(x + 0.4, y + 4.4, 2.0, 3.8, 4.0)[0]
    sp.fill(sc, screen if lit else (60, 70, 90))
    if lit: sp.fill(sc & (DX.YC > y + 6.6), VIOLET)
    sp.anchors['phone'] = (x + 0.4, y + 4.4)


def parcel(sp, x=0.0, y=0.0, w=14.0, h=10.0):
    """a cardboard box with violet ОЗНОБ tape; (x, y) = bottom centre"""
    sp.sup(x, y + h / 2, w / 2, h / 2, tones((206, 160, 100)), n=6.0)
    sp.fill(sp.m_super(x, y + h / 2, 1.4, h / 2, 6.0)[0], VIOLET)
    sp.fill(sp.m_super(x, y + h - 1.0, w / 2, 0.8, 6.0)[0], dark((206, 160, 100), 0.8))
    if sp.k >= 2: sp.txt_box(['ОЗНОБ'], (x - w / 2 + 0.6, y + 1.0, x - 1.6, y + 4.4), VIOLET_D, pad=0.1)
    sp.anchors['parcel'] = (x, y + h / 2)


def soft_blush(sp, cx, cy, rx, ry, col, a=0.42):
    """a soft rosy patch blended into the skin (no checker dots): cold-pinched cheeks"""
    m, nx, ny = sp.m_ell(cx, cy, rx, ry)
    m &= sp.m & ~sp.keep
    if not m.any(): return
    r2 = np.clip(nx * nx + ny * ny, 0, 1)
    w = (1.0 - r2) * a
    c = sp.col.astype(np.float32)
    c[m] = c[m] * (1 - w[m, None]) + np.array(col, np.float32) * w[m, None]
    sp.col = np.clip(c, 0, 255).astype(np.uint8)


def quilt(sp, mask, seams, base, cx, rx, gloss=True):
    """a down jacket: the mask split into horizontal bands by `seams` (y, sprite px, bottom->top); every band is a puffed tube with
    its own light (bright upper half, dark bottom by the seam), a dark seam line with stitches and a nylon gloss streak"""
    ys = [-1e9] + sorted(seams) + [1e9]
    for y0, y1 in zip(ys[:-1], ys[1:]):
        band = mask & (DX.YC >= y0) & (DX.YC < y1)
        if not band.any(): continue
        rows = np.where(band.any(1))[0]
        top_y = max(y0, DX.YC[rows[-1], 0]); bot_y = min(y1, DX.YC[rows[0], 0])
        mid = (min(y1, 1e3) + max(y0, -1e3)) / 2 if abs(y0) < 1e8 and abs(y1) < 1e8 else (top_y + bot_y) / 2
        hh = max(1.0, (min(y1, top_y) - max(y0, bot_y)) / 2 + 0.6)
        ny = np.clip((DX.YC - mid) / hh, -0.95, 0.95)
        nx = np.clip((DX.XC - cx) / rx, -0.95, 0.95)
        sp.paint(band, tones(base), DX.lit(nx * 0.85, ny * 0.8), ol=False)
        if gloss and abs(y0) < 1e8 and abs(y1) < 1e8:
            gl = band & (np.abs(DX.YC - (mid + hh * 0.45)) < 0.32) & (DX.XC > cx - rx * 0.75) & (DX.XC < cx - rx * 0.05)
            sp.fill(gl, mix(base, (255, 255, 255), 0.55))
    for y in seams:
        sm_ = mask & (np.abs(DX.YC - y) < 0.38)
        sp.fill(sm_, dark(base, 0.52))
        for x in np.arange(cx - rx, cx + rx, 2.2):
            sp.fill(sm_ & (np.abs(DX.XC - x) < 0.3) & (np.abs(DX.YC - y) < 0.2), dark(base, 0.35))
    e = mask & ~erode(mask)
    sp.col[e] = mix(dark(base, 0.5), INK, 0.4)


def shovel(sp, h, ang=-1.2, l=40.0, snow=0.0):
    """a real snow shovel (~1.3 m = 0.7 of a hero): wooden handle with a D-grip, a wide aluminium scoop with a rim, at hand h;
    ang = direction from the hand to the scoop (radians)"""
    x, y = h
    ca, sa = math.cos(ang), math.sin(ang)
    a, b = (x - ca * 10.0, y - sa * 10.0), (x + ca * l, y + sa * l)
    thin(sp, a, b, (150, 98, 50), 1.1)
    thin(sp, (a[0] + 0.3, a[1] + 0.3), (b[0] + 0.3, b[1] + 0.3), (214, 160, 96), 0.35)
    sp.ell(a[0] - ca * 1.6, a[1] - sa * 1.6, 2.0, 2.0, tones((40, 40, 50)), frost=False)                     # D-grip
    px, py = -sa, ca
    e = (b[0] + ca * 14.0, b[1] + sa * 14.0)
    pts = [(b[0] + px * 4.0, b[1] + py * 4.0), (e[0] + px * 9.0, e[1] + py * 9.0), (e[0] - px * 9.0, e[1] - py * 9.0),
           (b[0] - px * 4.0, b[1] - py * 4.0)]
    m = sp.m_poly(pts)
    v = np.clip(0.55 + ((DX.XC - b[0]) * px + (DX.YC - b[1]) * py) * 0.04, 0.05, 0.95)
    sp.paint(m, tones((196, 206, 222)), v)
    thin(sp, (e[0] + px * 9.0, e[1] + py * 9.0), (e[0] - px * 9.0, e[1] - py * 9.0), (120, 130, 150), 0.6)   # the rim
    for q in (-4.0, 0.0, 4.0): thin(sp, (b[0] + px * q * 0.5, b[1] + py * q * 0.5), (e[0] + px * q, e[1] + py * q), (160, 172, 190), 0.22)
    if snow > 0:
        sp.union([sp.m_ell((b[0] + e[0]) / 2 + px * 0.6, (b[1] + e[1]) / 2 + py * 0.6, 7.0 * snow, 3.6 * snow)], tones(SNOWC), frost=False)
    sp.anchors['scoop'] = e


# ================================================================================ ЖОРА
def zhora(sp, t=0.0, expr='proud', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
          legs=True, ox=0.0, oy=0.0, frost=0.0, sweat=0.0, walk=None, lean=0.0, snowcap=0.0, steam=0.0, undies=False, sit=0.0):
    """ЖОРА. frost 0..1 = rime on brows, moustache and hat; snowcap 0..1 = a pile of snow on the hat; walk = phase (radians)"""
    E = X(expr)
    if blink is None: blink = ((t + 0.7) % 4.3) < 0.12
    br = 0.35 * math.sin(t * 2.0)
    bob = abs(math.sin(walk)) * 1.0 if walk is not None else 0.0
    def Q(x, y): return (x + ox + lean * (y / 60.0) * 5.0, y + oy + (bob if y > 10 else 0.3 * bob))
    swing = math.sin(walk) * 4.0 if walk is not None else 0.0
    # ---------------------------------------------------------------- far arm (behind the jacket)
    shF = Q(-12.0, 52.0 + br * 0.3)
    hf = hand_f if hand_f is not None else Q(-15.0 - swing * 0.6, 32.0)
    kF, eF = ik(shF, hf, 10.0, 9.0, -1.0)
    slF = sp.union([sp.m_cap(shF, kF, 5.2, 4.6), sp.m_cap(kF, eF, 4.6, 3.8)], tones(dark(ALASKA, 0.8)), ol=False)
    quilt(sp, slF, [kF[1]], dark(ALASKA, 0.8), (shF[0] + eF[0]) / 2, 6.0, gloss=False)
    sp.ell(eF[0], eF[1] - 0.4, 3.4, 3.2, tones(dark(MITT, 0.85)))
    if prop_f: prop_f(sp, eF)
    sp.anchors['hand_f'] = eF
    # ---------------------------------------------------------------- legs: quilted «ватные» pants + felt valenki with black galoshes
    if legs:
        sw = math.sin(walk) * 2.6 if walk is not None else 0.0
        for k_, dx in enumerate((-4.4, 4.6)):
            near = k_ == 1
            s_ = sw if near else -sw
            fx_, fy_ = dx + s_ * 0.7, max(0.0, s_) * 0.5
            c = PANTS if near else dark(PANTS, 0.86)
            if sit > 0.5:                                                   # sitting (in the basin): thighs forward
                fx_, fy_ = dx * 0.4 + 16.0, 10.0
            if undies:                                                      # bare hairy legs + blue polka-dot «семейники»
                sk = SKIN_Z if near else dark(SKIN_Z, 0.9)
                leg = sp.cap(Q(dx * 0.9, 22.0), (fx_ + ox, fy_ + 6.0 + oy), 3.4, 2.8, tones(sk), frost=False)
                for q in range(7): thin(sp, (fx_ + ox - 1.6 + q * 0.5, fy_ + 8.0 + oy + q * 1.6), (fx_ + ox - 2.2 + q * 0.5, fy_ + 9.0 + oy + q * 1.6), dark(sk, 0.55), 0.13, mask=leg)
                kx = dx * 0.9 + (fx_ - dx * 0.9) * 0.35
                sh = sp.union([sp.m_cap(Q(dx * 0.9, 24.0), Q(kx, 16.0), 5.8, 5.6)], tones((60, 100, 210)), frost=False)
                g = np.random.default_rng(3 + k_)
                for q in range(9): sp.blob(kx + g.uniform(-4.4, 4.4), g.uniform(13, 22), 0.7, WHITE, mask=sh)
            else:
                leg = sp.cap(Q(dx * 0.9, 28.0), (fx_ + ox, fy_ + 12.0 + oy), 4.8, 4.2, tones(c))
                for q in (-1.6, 1.6): thin(sp, Q(dx * 0.9 + q, 27.0), (fx_ + ox + q, fy_ + 13.0 + oy), dark(c, 0.7), 0.22, mask=leg)
                thin(sp, (fx_ + ox - 3.0, fy_ + 19.0 + oy), (fx_ + ox + 2.6, fy_ + 18.4 + oy), dark(c, 0.65), 0.25, mask=leg)  # knee crease
            vk = VALENKI if near else dark(VALENKI, 0.88)
            bt = 7.0 if undies else 13.0
            boot = sp.union([sp.m_cap((fx_ + ox, fy_ + bt + oy), (fx_ + 0.6 + ox, fy_ + 3.0 + oy), 4.8, 4.6),
                             sp.m_super(fx_ + 2.2 + ox, fy_ + 2.6 + oy, 5.8, 2.8, 2.2)], tones(vk))
            g = np.random.default_rng(11 + k_)
            for q in range(26):                                             # felt speckle
                sp.blob(fx_ + ox + g.uniform(-4, 7), fy_ + oy + g.uniform(3, 13), 0.28, dark(vk, 0.78), mask=boot)
            sp.fill(sp.m_super(fx_ + 0.4 + ox, fy_ + bt + 0.4 + oy, 5.2, 1.2, 3.0)[0], mix(vk, (255, 255, 255), 0.2))   # top fold
            gal = boot & (DX.YC < fy_ + oy + 3.6)
            sp.paint(gal, tones((40, 40, 52)), DX.lit(np.zeros_like(DX.XC), np.clip((DX.YC - fy_ - oy - 1.8) / 2.0, -0.9, 0.9)), ol=False)
            thin(sp, (fx_ + ox - 2.0, fy_ + oy + 3.4), (fx_ + ox + 6.0, fy_ + oy + 3.2), (110, 110, 130), 0.2)       # galosh shine
    # ---------------------------------------------------------------- body: the round quilted down «alaska»
    hx, hy = Q(3.4, 67.0)
    cxb = Q(0.6, 0)[0]
    body = sp.union([sp.m_ell(*Q(0.6, 42.0), 16.6, 18.6), sp.m_ell(*Q(0.0, 27.0), 14.6, 6.0), sp.m_ell(*Q(1.0, 55.0), 13.4, 6.4)],
                    tones(ALASKA), ol=False)
    quilt(sp, body, [Q(0, y)[1] for y in (30.0, 36.6, 43.2, 49.8, 56.0)], ALASKA, cxb, 16.6)
    thin(sp, Q(4.2, 59.0), Q(5.0, 23.0), dark(ALASKA, 0.45), 0.4)          # zipper
    for q in range(12): sp.dot(*Q(4.6 + q * 0.03, 24.0 + q * 3.0), (230, 230, 236))
    sp.ell(*Q(4.4, 57.0), 0.8, 1.4, tones((220, 220, 230)), frost=False)  # zipper pull
    pk = sp.m_super(*Q(-9.0, 35.0), 4.0, 3.0, 4.0)[0] & body              # pocket with a flap + button
    sp.fill(pk, dark(ALASKA, 0.78)); sp.fill(pk & ~erode(pk), dark(ALASKA, 0.5))
    sp.blob(*Q(-9.0, 37.2), 0.6, (40, 40, 50))
    sp.fill(sp.m_super(*Q(10.6, 47.0), 2.0, 1.0, 4.0)[0] & body, (40, 70, 160))     # a little sewn-on badge
    tel = sp.m_poly([Q(1.6, 60.0), Q(8.4, 60.0), Q(5.0, 54.4)]) & body     # telnyashka in the collar V
    sp.fill(tel, WHITE)
    for q in range(4): sp.fill(tel & (np.abs(DX.YC - Q(0, 55.2 + q * 1.3)[1]) < 0.32), TELNIK_B)
    # fur collar: scalloped tufts around the neck
    parts = [sp.m_ell(hx - 1.8, hy - 9.0, 11.6, 3.8), sp.m_ell(hx - 8.0, hy - 5.4, 3.8, 4.6)]
    for q in range(9):
        a = math.pi * (0.95 + 1.15 * q / 8)
        parts.append(sp.m_ell(hx - 1.8 + math.cos(a) * 10.6, hy - 9.0 + math.sin(a) * 3.4, 2.2, 1.8))
    collar = sp.union(parts, tones(FUR))
    g = np.random.default_rng(7)
    for q in range(26):
        x0, y0 = g.uniform(hx - 12.0, hx + 9.0), g.uniform(hy - 12.0, hy - 5.0)
        thin(sp, (x0, y0), (x0 + g.uniform(-0.8, 0.8), y0 + g.uniform(0.8, 1.8)), mix(FUR, (255, 230, 190), 0.35) if q % 3 == 0 else dark(FUR, 0.68), 0.2, mask=collar)
    # ---------------------------------------------------------------- head (smooth skin, no frost hatching)
    head = sp.union([sp.m_ell(hx + 0.6, hy, 8.6, 9.0), sp.m_ell(hx + 1.8, hy - 4.4, 7.4, 5.8)], tones(SKIN_Z), frost=False)
    ear = sp.ell(hx - 5.8, hy + 0.2, 1.8, 2.6, tones(dark(SKIN_Z, 0.92)), frost=False)
    thin(sp, (hx - 5.6, hy + 1.4), (hx - 5.9, hy - 1.0), dark(SKIN_Z, 0.7), 0.25)
    soft_blush(sp, hx - 5.8, hy + 0.2, 2.0, 2.6, (230, 80, 80), 0.5)          # frozen red ear
    soft_blush(sp, hx + 5.4, hy - 2.8, 3.0, 2.2, CHEEK, 0.55)
    soft_blush(sp, hx - 1.8, hy - 2.6, 2.2, 1.8, CHEEK, 0.45)
    lx, ly = look
    DX.eye(sp, hx + 4.6, hy + 1.6, 4.4, 4.2, E, (70, 130, 200), (lx, ly), blink, lash=INK, skin=SKIN_Z, bold=1)
    DX.eye(sp, hx - 0.4, hy + 1.6, 3.8, 4.0, E, (70, 130, 200), (lx, ly), blink, lash=INK, skin=SKIN_Z, bold=1)
    if sp.k >= 2:                                                          # eye bags + crow's feet
        thin(sp, (hx + 2.8, hy - 0.8), (hx + 6.4, hy - 0.9), dark(SKIN_Z, 0.8), 0.14)
        for q in range(3): thin(sp, (hx + 7.0, hy + 1.8 - q * 0.9), (hx + 8.2, hy + 2.2 - q * 1.3), dark(SKIN_Z, 0.78), 0.12)
    DX.brow(sp, hx + 4.6, hy + 5.6, 4.8, E, +1, MOUST, th=2, bushy=True)
    DX.brow(sp, hx - 0.4, hy + 5.5, 4.0, E, -1, MOUST, th=2, bushy=True)
    nose = sp.ell(hx + 8.4, hy - 1.4, 2.6, 2.6, tones(NOSE), gloss=1.0, frost=False)      # potato nose
    sp.blob(hx + 8.6, hy - 3.0, 0.5, dark(NOSE, 0.5))                       # nostril
    sp.blob(hx + 7.8, hy - 0.4, 0.45, (255, 230, 220), keep=True)
    mx, my = hx + 4.8, hy - 7.4
    DX.stubble(sp, sp.m_ell(hx + 2.4, hy - 7.6, 6.6, 2.6)[0] & head, dark(SKIN_Z, 0.78), 0.18, 5)
    DX.mouth(sp, mx, my, 5.8, E, mouth_, (150, 60, 60), inside=(90, 24, 34), teeth=(255, 255, 250), skin=SKIN_Z, maxh=6.4)
    must = sp.union([sp.m_ell(mx - 0.4, my + 2.8, 4.6, 1.3), sp.m_ell(mx + 3.0, my + 2.5, 2.4, 1.1)], tones(MOUST))  # brush moustache
    for q in range(9): thin(sp, (mx - 4.2 + q * 1.0, my + 3.6), (mx - 4.5 + q * 1.0, my + 1.7), dark(MOUST, 0.62) if q % 2 else mix(MOUST, (230, 200, 160), 0.3), 0.16, mask=must)
    if frost > 0:                                                          # rime on brows and moustache, icicles
        g = np.random.default_rng(5)
        for q in range(int(18 * frost)):
            x_, y_ = g.uniform(hx - 3, hx + 8), g.choice([hy + 6.0, my + 3.2])
            sp.blob(x_, y_ + g.uniform(-0.5, 0.5), 0.36, SNOWC, keep=True)
        for q in range(int(3 * frost) + 1):
            x_ = mx - 3.0 + q * 2.4
            thin(sp, (x_, my + 1.8), (x_ + 0.2, my + 0.2 - 0.6 * (q % 2)), (200, 230, 255), 0.36, keep=True)
    # ---------------------------------------------------------------- the knitted cone hat «петушок»
    base_y = hy + 8.6
    tip = (hx - 6.0 - 1.4 * math.sin(t * 2.4), hy + 29.0)
    cone = sp.m_poly([(hx - 7.6, base_y), (hx + 8.6, base_y), (tip[0] + 2.0, tip[1]), (tip[0] - 1.2, tip[1] - 0.6)])
    nyc = np.clip((DX.YC - base_y) / 22.0, 0, 1)
    val = DX.lit(np.clip((DX.XC - hx) / 9.0, -0.9, 0.9), nyc * 0.5)
    band = (((DX.YC - base_y) // 3.4).astype(int) % 2) == 0
    sp.paint(cone & band, tones(HAT_R), val, ol=False, frost=False)
    sp.paint(cone & ~band, tones(HAT_W), val, ol=False, frost=False)
    rib = cone & (((DX.XC * 1.2).astype(int) % 2) == 0)                   # knit ribs: darker columns
    c = sp.col.astype(np.float32); c[rib] *= 0.9; sp.col = c.astype(np.uint8)
    e = cone & ~erode(cone); sp.col[e] = mix(dark(HAT_R, 0.5), INK, 0.4)
    cuff = sp.sup(hx + 0.6, base_y + 0.4, 9.2, 2.8, tones(HAT_W), n=3.0, frost=False)
    rb = cuff & (((DX.XC * 1.5).astype(int) % 2) == 0)
    c = sp.col.astype(np.float32); c[rb] *= 0.9; sp.col = c.astype(np.uint8)
    if sp.k >= 2: sp.txt_box(['SPORT'], (hx - 6.0, base_y - 1.6, hx + 7.0, base_y + 2.4), HAT_R, pad=0.1)
    pom = sp.ell(tip[0], tip[1] + 1.0, 3.4, 3.4, tones(HAT_W), frost=False)  # fluffy pompon
    for q in range(14):
        a = q * 0.45
        thin(sp, (tip[0] + math.cos(a) * 1.2, tip[1] + 1.0 + math.sin(a) * 1.2), (tip[0] + math.cos(a) * 3.8, tip[1] + 1.0 + math.sin(a) * 3.8),
             dark(HAT_W, 0.78) if q % 2 else (255, 255, 255), 0.2)
    if snowcap > 0:
        sp.union([sp.m_ell(tip[0] + 1.0, tip[1] + 3.8, 3.8 * snowcap, 2.0 * snowcap),
                  sp.m_ell(hx + 1.0, base_y + 3.4, 7.4 * snowcap, 1.9 * snowcap)], tones(SNOWC), frost=False)
    if sweat > 0:
        for i, (x, y) in enumerate(((hx - 2.0, hy + 4.6), (hx + 6.0, hy + 4.0))[:int(1 + sweat)]):
            yy = y - ((t * 4.0 + i * 1.3) % 3.5)
            sp.ell(x, yy, 0.6, 1.0, tones((170, 220, 255)), ol=False)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 2.0, hy + 1.6), chest=Q(2.0, 44.0), hat=tip)
    # ---------------------------------------------------------------- near arm (over the body)
    before = sp.m.copy()
    shN = Q(13.8, 52.0 + br * 0.3)
    hn = hand_n if hand_n is not None else Q(17.0 + swing * 0.6, 32.0)
    kN, eN = ik(shN, hn, 10.0, 9.0, -1.0)
    slN = sp.union([sp.m_cap(shN, kN, 5.4, 4.8), sp.m_cap(kN, eN, 4.8, 4.0)], tones(ALASKA), ol=False)
    quilt(sp, slN, [kN[1] + 0.3], ALASKA, (shN[0] + eN[0]) / 2, 6.0)
    if prop_n and getattr(prop_n, 'behind', False): prop_n(sp, eN)
    mit = sp.ell(eN[0], eN[1] - 0.4, 3.6, 3.4, tones(MITT), frost=False)
    sp.ell(eN[0] + 2.4, eN[1] + 0.8, 1.4, 1.8, tones(MITT), frost=False)  # thumb
    for q in range(6):                                                     # knitted white zigzag band
        x0 = eN[0] - 3.0 + q * 1.1
        thin(sp, (x0, eN[1] + 1.5 + (q % 2) * 0.6), (x0 + 1.1, eN[1] + 1.5 + ((q + 1) % 2) * 0.6), WHITE, 0.26)
    thin(sp, (eN[0] - 3.2, eN[1] + 2.7), (eN[0] + 3.2, eN[1] + 2.7), WHITE, 0.45)   # cuff stripe
    if prop_n and not getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.anchors['hand'] = eN
    _arm_over(sp, before)


# ================================================================================ ЧАЙКА
def chayka(sp, t=0.0, expr='dry', mouth_=0.0, look=(0.5, 0.0), blink=None, chew=0.0, wing=0.0, fly=False, glasses=False):
    """the herring gull in winter plumage, side view facing +x (~30 px: draw it at ~0.2 of a hero's height in two-shots):
    white body, silver-grey back with scalloped coverts, black primaries with white «mirrors», a streaky scruffy winter head,
    a pale yellow eye with a red orbital ring under a droopy lid, a yellow beak with the red gonys spot, pink webbed feet"""
    E = X(expr)
    if blink is None: blink = ((t + 1.9) % 3.9) < 0.12
    br = 0.4 * math.sin(t * 1.7)
    if not fly:
        for k_, dx in enumerate((-1.8, 2.4)):                                # legs + webbed feet + a ring on the near leg
            c = GULL_LEG if k_ else dark(GULL_LEG, 0.85)
            thin(sp, (dx, 7.0), (dx + 0.4, 1.0), c, 0.7)
            sp.poly([(dx - 1.6, 0.0), (dx + 4.0, 0.0), (dx + 0.8, 1.6)], tones(c), frost=False)
            for q in range(3): thin(sp, (dx + 0.6, 1.0), (dx - 1.2 + q * 2.4, 0.1), dark(c, 0.7), 0.15)
        sp.sup(2.6, 4.2, 1.2, 1.0, tones((240, 120, 40)), n=3.0, frost=False)
    sp.poly([(-13.0, 15.0), (-21.0, 12.4), (-20.6, 17.0), (-12.0, 19.0)], tones(GULL_W))           # tail
    body = sp.union([sp.m_ell(0.0, 13.0 + br * 0.2, 12.4, 7.8), sp.m_ell(3.0, 10.2, 9.0, 6.6)], tones(GULL_W), frost=False)
    if fly:
        for s_ in (-1, 1):
            a = 0.5 * math.sin(t * 9.0)
            sp.poly([(-4.0, 16.0), (-14.0, 16.0 + 14.0 * math.cos(a)), (-24.0, 18.0 + 10.0 * math.cos(a)), (-2.0, 19.0)], tones(GULL_G))
    wy = 15.0 + br * 0.2 + wing * 6.0
    wng = sp.union([sp.m_ell(-3.4, wy, 11.2, 4.8, 0.12 + 0.4 * wing)], tones(GULL_G), frost=False)
    tipm = wng & (DX.XC < -9.6)
    sp.fill(tipm, (34, 34, 46))                                            # black primaries
    for q in range(4): sp.blob(-11.6 - q * 2.0, wy - 0.6 + q * 0.4, 0.5, WHITE, mask=wng, keep=True)   # white «mirrors»
    for row in range(3):                                                    # scalloped coverts
        for q in range(5):
            x0 = -6.0 + q * 2.6 - row * 1.2; y0 = wy + 2.2 - row * 1.8
            thin(sp, (x0 - 1.0, y0), (x0, y0 - 0.8), dark(GULL_G, 0.7), 0.18, mask=wng & ~tipm)
            thin(sp, (x0, y0 - 0.8), (x0 + 1.0, y0), dark(GULL_G, 0.7), 0.18, mask=wng & ~tipm)
    thin(sp, (-12.0, wy + 3.2), (4.0, wy + 3.6), mix(GULL_G, (255, 255, 255), 0.4), 0.3, mask=wng)       # white trailing edge
    for q in range(6): thin(sp, (-4.0 + q * 2.2, 6.6), (-3.6 + q * 2.2, 5.6), (220, 224, 234), 0.18, mask=body)  # belly feathers
    # scruffy streaky head
    hx, hy = 9.0, 23.0 + br * 0.4
    sp.cap((5.0, 16.0), (hx - 0.4, hy - 2.0), 4.8, 4.4, tones(GULL_W), frost=False)
    head = sp.union([sp.m_ell(hx, hy, 5.8, 5.2)], tones(GULL_W), frost=False)
    g = np.random.default_rng(3)
    for q in range(22):                                                     # winter streaks on the head and neck
        x_, y_ = g.uniform(hx - 5.0, hx + 3.0), g.uniform(hy - 6.0, hy + 4.0)
        thin(sp, (x_, y_), (x_ - 0.6, y_ - 0.5), (176, 160, 150), 0.16, mask=head | sp.m_cap((5.0, 16.0), (hx - 0.4, hy - 2.0), 4.8, 4.4)[0])
    for q in range(6):                                                      # ruffled feathers on top
        x0 = hx - 3.6 + q * 1.3
        thin(sp, (x0, hy + 4.6), (x0 - 0.6 + (q % 2) * 1.2, hy + 6.6 + (q % 3) * 0.5), GULL_W, 0.42)
    lx, ly = look
    ex, ey = hx + 2.2, hy + 1.2
    sp.ell(ex, ey, 1.95, 1.85, tones((226, 70, 60)), frost=False, ol=False)   # red orbital ring
    DX.eye(sp, ex, ey, 3.2, 3.0, E, (244, 226, 120), (lx, ly), blink, lash=INK, skin=GULL_W, bold=1)
    DX.brow(sp, ex, hy + 3.8, 3.6, E, +1, dark(GULL_G, 0.7), th=1)
    if glasses:
        sp.fill(sp.m_super(ex + 0.2, ey, 3.2, 1.8, 3.0)[0], (30, 30, 40))
        thin(sp, (hx - 1.6, hy + 1.6), (hx + 0.2, hy + 1.6), (30, 30, 40), 0.3)
    # beak: upper fixed with a hooked tip, lower drops with the voice (or chews); the red gonys spot
    m = max(mouth_, 0.35 * chew * (0.5 + 0.5 * math.sin(t * 14.0)))
    bx, by = hx + 4.4, hy - 0.6
    sp.poly([(bx, by + 1.8), (bx + 7.2, by + 0.8), (bx + 8.6, by - 0.4), (bx + 7.6, by - 0.6), (bx, by - 0.2)], tones(BEAK), frost=False)
    a = math.radians(6 + 30 * m)
    sp.poly([(bx, by - 0.4), (bx + 7.0 * math.cos(a), by - 0.6 - 7.0 * math.sin(a)), (bx + 5.4 * math.cos(a), by - 1.9 - 5.4 * math.sin(a)),
             (bx, by - 1.7)], tones(BEAK), frost=False)
    sp.blob(bx + 5.2 * math.cos(a), by - 1.3 - 5.2 * math.sin(a), 0.7, (220, 50, 40))
    thin(sp, (bx + 0.6, by + 1.0), (bx + 2.2, by + 1.0), dark(BEAK, 0.6), 0.2)                    # nostril
    if m > 0.2: sp.fill(sp.m_poly([(bx + 0.4, by - 0.4), (bx + 5.0, by + 0.2), (bx + 5.0 * math.cos(a), by - 1.0 - 5.0 * math.sin(a))]), (150, 40, 50))
    sp.anchors.update(head=(hx, hy), mouth=(bx + 4.0, by), eyes=(ex, ey))


# ================================================================================ ИРА
def ira(sp, t=0.0, expr='normal', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, box=False, legs=True, yell=0.0,
        prop_n=None, point=False):
    """ИРА: halat with flowers over a sweater, a grey down shawl over the shoulders, a bun with a claw clip; box=True holds a parcel"""
    E = X(expr)
    if blink is None: blink = ((t + 2.2) % 4.4) < 0.12
    br = 0.3 * math.sin(t * 1.8)
    if legs:
        for k_, dx in enumerate((-2.6, 2.8)):
            sp.cap((dx, 18.0), (dx + 0.4, 4.0), 2.4, 2.0, tones((200, 150, 130) if k_ else (176, 130, 116)))
            sp.sup(dx + 2.0, 1.8, 4.2, 1.8, tones((240, 120, 160)), n=2.4)                      # slippers with a pompon
            sp.blob(dx + 4.6, 2.6, 1.0, WHITE)
    hf = hand_f if hand_f is not None else (-9.6, 34.0)
    kF, eF = ik((-8.0, 50.0 + br), hf, 8.0, 7.0, -1.0)
    sp.cap((-8.0, 50.0 + br), kF, 3.2, 2.6, tones(dark(HALAT, 0.82))); sp.cap(kF, eF, 2.6, 2.2, tones(dark(HALAT, 0.82)))   # far arm
    sp.ell(eF[0], eF[1], 1.7, 1.6, tones(dark(SKIN_I, 0.88)))
    hal = sp.poly([(-8.6, 52.0), (9.4, 52.0), (11.6, 18.0), (-10.6, 18.0)], tones(HALAT),
                  val=np.clip(0.75 - (DX.XC - 1.0) * 0.03, 0.05, 0.98))
    g = np.random.default_rng(4)
    for q in range(16):                                                     # little white flowers
        x, y = g.uniform(-9, 10), g.uniform(20, 50)
        for a in range(4): sp.blob(x + math.cos(a * 1.57) * 0.7, y + math.sin(a * 1.57) * 0.7, 0.45, WHITE, mask=hal)
        sp.blob(x, y, 0.35, (255, 220, 80), mask=hal)
    thin(sp, (-9.6, 33.0), (10.6, 33.0), dark(HALAT, 0.6), 0.6)              # belt
    for q in (-5.0, 0.4, 6.0): thin(sp, (q, 31.0), (q + (q * 0.12), 19.0), dark(HALAT, 0.78), 0.22, mask=hal)   # folds
    thin(sp, (2.0, 52.0), (4.6, 33.0), dark(HALAT, 0.62), 0.3, mask=hal)      # lapel edge
    sp.blob(9.0, 33.6, 1.0, dark(HALAT, 0.6))                                  # belt knot
    shawl = sp.union([sp.m_ell(0.4, 51.0, 11.6, 5.0), sp.m_ell(-6.0, 45.0, 5.0, 6.0)], tones(SHAWL))
    for q in range(10):
        x0 = -10.0 + q * 2.2
        thin(sp, (x0, 47.0), (x0 + 0.3, 44.4 - (q % 2)), dark(SHAWL, 0.75), 0.25)                    # fringe
    hx, hy = 1.6, 62.0
    sp.cap((1.2, 53.0), (1.4, 56.0), 2.2, 2.2, tones(dark(SKIN_I, 0.9)))
    head = sp.union([sp.m_ell(hx, hy, 6.0, 6.8), sp.m_ell(hx + 0.8, hy - 2.8, 5.0, 3.8)], tones(SKIN_I), frost=False)
    lx, ly = look
    DX.eye(sp, hx + 3.0, hy + 1.0, 3.6, 3.6, E, (90, 120, 60), (lx, ly), blink, lash=INK, skin=SKIN_I, bold=2, flick=True)
    DX.eye(sp, hx - 1.4, hy + 1.0, 3.2, 3.4, E, (90, 120, 60), (lx, ly), blink, lash=INK, skin=SKIN_I, bold=2, flick=True)
    DX.brow(sp, hx + 3.0, hy + 4.2, 3.4, E, +1, HAIR_I, th=1)
    DX.brow(sp, hx - 1.4, hy + 4.1, 3.0, E, -1, HAIR_I, th=1)
    sp.ell(hx + 5.4, hy - 0.8, 1.2, 1.6, tones(dark(SKIN_I, 0.95)))
    soft_blush(sp, hx + 3.4, hy - 2.0, 2.0, 1.4, (240, 120, 130), 0.45)
    mx, my = hx + 3.0, hy - 4.2
    DX.mouth(sp, mx, my, 3.8, E, mouth_, (210, 70, 90), inside=(110, 30, 50), skin=SKIN_I, maxh=4.4)
    hair = sp.union([sp.m_ell(hx - 0.8, hy + 4.4, 6.6, 3.4), sp.m_ell(hx - 4.6, hy + 0.6, 2.4, 5.0), sp.m_ell(hx - 3.6, hy + 9.4, 4.2, 3.6)],
                    tones(HAIR_I), exclude=head & (DX.YC < hy + 3.6) & (DX.XC > hx - 3.4))
    sp.sup(hx - 3.4, hy + 7.4, 3.6, 1.2, tones((60, 200, 190)), n=3.0)                                  # claw clip
    for q in range(4): thin(sp, (hx - 6.0 + q * 1.6, hy + 8.0), (hx - 6.0 + q * 1.6, hy + 6.0), (30, 140, 130), 0.25)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my))
    before = sp.m.copy()
    hn = hand_n if hand_n is not None else ((9.0, 36.0) if box else (9.0, 30.0))
    kN, eN = ik((8.4, 50.0 + br), hn, 8.0, 7.0, -1.0)
    sp.cap((8.4, 50.0 + br), kN, 3.2, 2.8, tones(HALAT)); sp.cap(kN, eN, 2.6, 2.2, tones(HALAT))
    if box: parcel(sp, eN[0] - 1.0, eN[1] - 4.0, 13.0, 9.0)
    sp.ell(eN[0], eN[1], 1.8, 1.7, tones(SKIN_I))
    if prop_n: prop_n(sp, eN)
    if point: thin(sp, (eN[0] + 1.2, eN[1] + 0.2), (eN[0] + 4.0, eN[1] - 0.8), SKIN_I, 0.8)
    sp.anchors['hand'] = eN
    _arm_over(sp, before)


# ================================================================================ ВИТЁК
def vitek(sp, t=0.0, expr='cheerful', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, legs=True, phone_up=False, lean=0.0):
    """ВИТЁК: skinny, violet ОЗНОБ jacket, a cap with ОЗНОБ, a big cube thermal backpack; lean > 0 bends the upper body forward"""
    E = X(expr)
    if blink is None: blink = ((t + 0.3) % 3.7) < 0.12
    br = 0.3 * math.sin(t * 2.2)
    def Q(x, y): return (x + lean * max(0.0, y - 26.0) * 0.45, y - lean * max(0.0, y - 26.0) * 0.18)
    if legs:
        for k_, dx in enumerate((-2.4, 2.6)):
            sp.cap((dx, 28.0), (dx + 0.6, 4.0), 2.6, 2.2, tones((40, 44, 60) if k_ else (32, 36, 50)))
            sp.sup(dx + 1.8, 1.8, 4.0, 1.8, tones((236, 236, 240)), n=2.4)                           # white sneakers in the snow
    bag = sp.sup(*Q(-10.0, 44.0), 8.0, 9.0, tones(VIOLET), n=5.0)                                     # cube backpack
    sp.fill(bag & (np.abs(DX.YC - Q(0, 44.0)[1]) < 0.4), VIOLET_D)
    if sp.k >= 2: sp.txt_box(['ОЗНОБ'], (Q(-17.4, 0)[0], Q(0, 46.0)[1], Q(-8.0, 0)[0], Q(0, 50.0)[1]), (255, 255, 255), pad=0.1)
    sp.cap(Q(-5.0, 50.0 + br), Q(-7.0, 34.0), 2.8, 2.4, tones(dark(VIOLET, 0.82)))
    jk = sp.union([sp.m_super(*Q(0.4, 41.0), 7.6, 13.0, 3.0)], tones(VIOLET), ol=False)
    quilt(sp, jk, [Q(0, y)[1] for y in (33.0, 40.0, 47.0)], VIOLET, Q(0.4, 0)[0], 7.6)
    thin(sp, Q(-4.6, 52.0), Q(-3.6, 30.0), (40, 30, 60), 0.6)                                           # backpack strap
    thin(sp, Q(2.0, 53.0), Q(2.4, 29.0), (230, 230, 240), 0.35)
    sp.fill(jk & (np.abs(DX.YC - Q(0, 40.0)[1]) < 0.6), (200, 240, 90))                               # reflective stripe
    hx, hy = Q(1.8, 62.0)
    sp.cap(Q(1.2, 53.0), (hx - 0.2, hy - 6.0), 2.0, 2.0, tones(dark(SKIN_V, 0.9)))
    head = sp.union([sp.m_ell(hx, hy, 5.4, 6.4), sp.m_ell(hx + 0.8, hy - 2.6, 4.6, 3.6)], tones(SKIN_V), frost=False)
    lx, ly = look
    DX.eye(sp, hx + 2.8, hy + 0.8, 3.4, 3.4, E, (90, 70, 50), (lx, ly), blink, lash=INK, skin=SKIN_V, bold=1)
    DX.eye(sp, hx - 1.4, hy + 0.8, 3.0, 3.2, E, (90, 70, 50), (lx, ly), blink, lash=INK, skin=SKIN_V, bold=1)
    DX.brow(sp, hx + 2.8, hy + 3.8, 3.2, E, +1, (90, 60, 40), th=1)
    sp.ell(hx + 5.0, hy - 0.8, 1.2, 1.6, tones(dark(SKIN_V, 0.95)))
    soft_blush(sp, hx + 3.6, hy - 1.6, 1.8, 1.2, (236, 110, 110), 0.5)
    mx, my = hx + 2.8, hy - 4.0
    DX.mouth(sp, mx, my, 4.0, E, mouth_, (170, 80, 80), inside=(90, 24, 34), skin=SKIN_V, maxh=4.4)
    sp.union([sp.m_ell(hx - 0.2, hy + 4.4, 6.0, 2.8)], tones(VIOLET))                                 # cap
    sp.sup(hx + 5.2, hy + 3.0, 3.6, 0.9, tones(VIOLET_D), n=2.4)                                       # visor
    if sp.k >= 2: sp.txt_box(['ОЗНОБ'], (hx - 4.4, hy + 3.6, hx + 3.6, hy + 6.4), (255, 255, 255), pad=0.1)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my))
    before = sp.m.copy()
    shN = Q(6.0, 50.0 + br)
    hn = hand_n if hand_n is not None else Q(10.0, 34.0)
    kN, eN = ik(shN, hn, 8.0, 7.6, -1.0)
    sp.cap(shN, kN, 3.0, 2.6, tones(VIOLET)); sp.cap(kN, eN, 2.6, 2.2, tones(VIOLET))
    if phone_up: phone(sp, (eN[0] - 0.4, eN[1] - 1.0))
    sp.ell(eN[0], eN[1], 1.8, 1.7, tones(SKIN_V))
    sp.anchors['hand'] = eN
    _arm_over(sp, before)


# ================================================================================ БАБА НИНА
def nina(sp, t=0.0, expr='kind', mouth_=0.0, look=(0.6, 0.0), blink=None, can=True, legs=True):
    """баба Нина: a round granny in a red polka-dot headscarf, big round glasses, a green cardigan, a watering can"""
    E = X(expr)
    if blink is None: blink = ((t + 3.0) % 4.8) < 0.13
    br = 0.3 * math.sin(t * 1.5)
    if legs:
        for dx in (-3.0, 3.0):
            sp.cap((dx, 16.0), (dx, 4.0), 2.6, 2.2, tones((120, 90, 80)))
            sp.sup(dx + 1.4, 1.8, 3.8, 1.8, tones((60, 50, 50)), n=2.4)
    sp.cap((-9.0, 42.0 + br), (-10.0, 28.0), 3.2, 2.8, tones(dark(CARDI, 0.82)))
    body = sp.union([sp.m_ell(0.4, 30.0, 12.0, 15.0), sp.m_ell(0.0, 42.0, 10.0, 5.0)], tones(CARDI))
    sp.fill(body & (DX.YC < 20.0), (120, 70, 110))                                                     # skirt
    kn = body & (DX.YC >= 20.0) & ((((DX.XC * 1.4).astype(int) + (DX.YC * 1.4).astype(int)) % 3) == 0)
    c_ = sp.col.astype(np.float32); c_[kn] *= 0.88; sp.col = c_.astype(np.uint8)                       # knit
    for q in range(4): sp.dot(3.0, 26.0 + q * 4.0, (230, 220, 180))
    hx, hy = 1.6, 54.0
    head = sp.union([sp.m_ell(hx, hy, 6.4, 6.6)], tones(SKIN_N), frost=False)
    lx, ly = look
    DX.eye(sp, hx + 3.0, hy + 0.8, 3.4, 3.2, E, (80, 110, 150), (lx, ly), blink, lash=INK, skin=SKIN_N, bold=1)
    DX.eye(sp, hx - 1.4, hy + 0.8, 3.0, 3.0, E, (80, 110, 150), (lx, ly), blink, lash=INK, skin=SKIN_N, bold=1)
    for ex, r in ((hx + 3.0, 2.6), (hx - 1.4, 2.4)):                                                  # big round glasses
        ring = sp.m_ell(ex, hy + 0.8, r + 0.5, r + 0.5)[0] & ~sp.m_ell(ex, hy + 0.8, r - 0.1, r - 0.1)[0]
        sp.fill(ring, (60, 50, 60))
    sp.ell(hx + 5.6, hy - 1.0, 1.4, 1.6, tones(dark(SKIN_N, 0.95)))
    soft_blush(sp, hx + 3.8, hy - 1.8, 2.0, 1.3, (236, 110, 110), 0.5)
    mx, my = hx + 3.0, hy - 4.0
    DX.mouth(sp, mx, my, 3.6, E, mouth_, (170, 90, 90), inside=(90, 24, 34), skin=SKIN_N, maxh=3.8)
    for q in range(3): thin(sp, (hx + 4.6, hy - 2.0 - q * 0.8), (hx + 5.6, hy - 2.4 - q * 0.8), dark(SKIN_N, 0.8), 0.15)   # wrinkles
    scarf = sp.union([sp.m_ell(hx - 0.6, hy + 3.4, 7.6, 5.4), sp.m_ell(hx - 4.8, hy - 1.0, 3.0, 5.0)], tones(SCARF_N),
                     exclude=head & (DX.YC < hy + 3.0) & (DX.XC > hx - 3.6))
    g = np.random.default_rng(6)
    for q in range(12): sp.blob(g.uniform(hx - 7, hx + 5), g.uniform(hy - 4, hy + 8), 0.5, WHITE, mask=scarf)
    sp.poly([(hx - 1.0, hy - 6.0), (hx + 1.6, hy - 9.6), (hx + 3.0, hy - 6.4)], tones(SCARF_N))            # the knot under the chin
    sp.anchors.update(head=(hx, hy), mouth=(mx, my))
    before = sp.m.copy()
    kN, eN = ik((8.0, 42.0 + br), (12.0, 32.0), 7.0, 7.0, -1.0)
    sp.cap((8.0, 42.0 + br), kN, 3.2, 2.8, tones(CARDI)); sp.cap(kN, eN, 2.8, 2.4, tones(CARDI))
    if can:
        c = sp.sup(eN[0] + 5.0, eN[1] - 1.0, 4.0, 3.4, tones((90, 170, 220)), n=3.0)
        thin(sp, (eN[0] + 8.0, eN[1] - 0.6), (eN[0] + 13.0, eN[1] + 3.0), (70, 140, 190), 0.8)
        sp.ell(eN[0] + 13.4, eN[1] + 3.4, 1.0, 1.0, tones((70, 140, 190)))
        if int(t * 8) % 2 == 0:
            for q in range(3): sp.blob(eN[0] + 13.6 + q * 0.5, eN[1] + 1.8 - q * 1.6, 0.35, (170, 220, 255))
    sp.ell(eN[0], eN[1], 1.8, 1.7, tones(SKIN_N))
    _arm_over(sp, before)


# ================================================================================ set pieces
def seedlings(sp, t=0.0, n=4):
    """a windowsill box with tomato seedlings under a violet grow lamp"""
    sp.sup(0.0, 3.0, 14.0, 3.0, tones((140, 90, 60)), n=4.0)
    for q in range(n):
        x = -10.0 + q * 6.6
        thin(sp, (x, 5.0), (x + 0.4, 12.0 + q % 2), (60, 150, 60), 0.5)
        for s_ in (-1, 1): sp.ell(x + s_ * 1.6, 11.0 + q % 2, 1.6, 0.9, tones((90, 190, 80)), ang=s_ * 0.5, frost=False)


def snow_pile(sp, w=20.0, h=8.0):
    sp.union([sp.m_ell(0.0, h * 0.4, w / 2, h * 0.6), sp.m_ell(-w * 0.2, h * 0.7, w * 0.3, h * 0.5)], tones(SNOWC), frost=False)


# ================================================================================ ТЁМА (сын, 10)
KID_SUIT = (60, 150, 230)
KID_HAT = (250, 200, 40)
SKIN_T = (248, 204, 176)


def tyoma(sp, t=0.0, expr='normal', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, legs=True, sit=0.0,
          socks=False):
    """ТЁМА, 10: a round kid in a puffy blue snow suit with reflective stripes, a yellow knitted hat with a big pompon and ear flaps,
    a striped scarf, rosy cheeks, a gap tooth; ~0.75 of Жора's height. sit 0..1 = sitting on a sled (legs forward)"""
    E = X(expr)
    if blink is None: blink = ((t + 1.1) % 3.8) < 0.12
    br = 0.3 * math.sin(t * 2.4)
    if legs:
        for k_, dx in enumerate((-2.6, 2.8)):
            c = KID_SUIT if k_ else dark(KID_SUIT, 0.86)
            if sit > 0.5:
                sp.cap((dx * 0.6, 14.0), (dx + 10.0, 6.0), 3.4, 3.0, tones(c))
                sp.sup(dx + 12.0, 5.0, 3.0, 2.2, tones((40, 40, 60) if not socks else (240, 240, 240)), n=2.4)
            else:
                sp.cap((dx, 18.0), (dx + 0.4, 4.0), 3.4, 3.0, tones(c))
                sp.sup(dx + 1.6, 2.0, 4.0, 2.2, tones((40, 40, 60) if not socks else (240, 240, 240)), n=2.4)
    oy = -6.0 if sit > 0.5 else 0.0
    body = sp.union([sp.m_ell(0.4, 28.0 + oy, 10.6, 12.0), sp.m_ell(0.0, 37.0 + oy, 8.6, 5.0)], tones(KID_SUIT), ol=False)
    quilt(sp, body, [21.0 + oy, 27.0 + oy, 33.0 + oy], KID_SUIT, 0.4, 10.6)
    sp.fill(body & (np.abs(DX.YC - (24.0 + oy)) < 0.5), (230, 240, 120))                                  # reflective stripe
    sc = sp.union([sp.m_ell(1.0, 40.6 + oy, 7.4, 2.4), sp.m_cap((-4.0, 40.0 + oy), (-6.0, 32.0 + oy), 1.6, 1.4)], tones((220, 40, 60)))
    for q in range(5): sp.fill(sc & (np.abs(DX.XC - (-5.0 + q * 2.8)) < 0.6), WHITE)                     # striped scarf
    hx, hy = 1.4, 49.0 + oy
    head = sp.union([sp.m_ell(hx, hy, 7.2, 7.2), sp.m_ell(hx + 1.0, hy - 2.8, 6.0, 4.4)], tones(SKIN_T), frost=False)
    soft_blush(sp, hx + 3.6, hy - 2.2, 2.4, 1.8, (240, 100, 100), 0.55)
    soft_blush(sp, hx - 2.4, hy - 2.0, 1.8, 1.6, (240, 100, 100), 0.45)
    lx, ly = look
    DX.eye(sp, hx + 3.2, hy + 0.6, 4.0, 4.4, E, (90, 140, 70), (lx, ly), blink, lash=INK, skin=SKIN_T, bold=1)
    DX.eye(sp, hx - 1.6, hy + 0.6, 3.6, 4.2, E, (90, 140, 70), (lx, ly), blink, lash=INK, skin=SKIN_T, bold=1)
    DX.brow(sp, hx + 3.2, hy + 4.0, 3.4, E, +1, (170, 110, 60), th=1)
    sp.ell(hx + 6.4, hy - 1.0, 1.5, 1.5, tones(dark(SKIN_T, 0.95)), frost=False)
    sp.blob(hx + 7.2, hy - 2.2, 0.5, (190, 210, 240), keep=True)                                          # a runny nose drop
    mx, my = hx + 3.2, hy - 4.2
    DX.mouth(sp, mx, my, 4.2, E, mouth_, (200, 80, 90), inside=(110, 30, 50), teeth=(255, 255, 250), skin=SKIN_T, maxh=4.6)
    hat = sp.union([sp.m_ell(hx - 0.2, hy + 3.4, 7.8, 5.0), sp.m_cap((hx - 5.4, hy + 2.0), (hx - 6.4, hy - 4.6), 1.8, 1.6)],
                   tones(KID_HAT), exclude=head & (DX.YC < hy + 3.6) & (DX.XC > hx - 4.6), frost=False)
    for q in range(8): thin(sp, (hx - 6.0 + q * 1.6, hy + 3.0), (hx - 6.2 + q * 1.6, hy + 7.6), dark(KID_HAT, 0.82), 0.22, mask=hat)
    sp.ell(hx - 0.6, hy + 9.6, 2.8, 2.8, tones((240, 80, 60)), frost=False)                               # pompon
    sp.anchors.update(head=(hx, hy), mouth=(mx, my))
    before = sp.m.copy()
    hn = hand_n if hand_n is not None else (8.0, 26.0 + oy)
    kN, eN = ik((7.0, 35.0 + oy + br), hn, 6.0, 6.0, -1.0)
    sp.cap((7.0, 35.0 + oy + br), kN, 3.0, 2.6, tones(KID_SUIT)); sp.cap(kN, eN, 2.6, 2.2, tones(KID_SUIT))
    if prop_n: prop_n(sp, eN)
    sp.ell(eN[0], eN[1], 2.2, 2.0, tones((240, 120, 40)), frost=False)                                    # orange mitten
    sp.anchors['hand'] = eN
    _arm_over(sp, before)


# ================================================================================ ВАХТЁРША тётя Валя (за стеклом будки, по пояс)
VAL_CARDI = (150, 70, 90)
VAL_HAIR = (190, 120, 80)
SKIN_VA = (236, 196, 172)


def valya(sp, t=0.0, expr='deadpan', mouth_=0.0, look=(0.6, 0.0), blink=None, knit=0.0, hand_n=None, sniff=0.0):
    """тётя Валя: a square stern watchwoman seated behind her desk (drawn from the waist): a ginger perm «химия», big glasses on a
    bead chain, a burgundy cardigan over a turtleneck, a brooch; knit 0..1 = knitting needles moving; sniff 0..1 = the nose up"""
    E = X(expr)
    if blink is None: blink = ((t + 0.5) % 4.6) < 0.12
    br = 0.3 * math.sin(t * 1.4)
    body = sp.union([sp.m_super(0.0, 20.0, 12.4, 12.0, 3.4), sp.m_ell(0.0, 31.0, 10.6, 5.0)], tones(VAL_CARDI))
    sp.fill(sp.m_poly([(-2.4, 36.0), (3.6, 36.0), (0.6, 26.0)]) & body, (60, 60, 80))                       # turtleneck V
    for q in range(4): sp.dot(1.2, 14.0 + q * 4.0, (230, 220, 190))
    sp.ell(-5.6, 30.0, 1.4, 1.4, tones((220, 180, 60)), gloss=1.0, frost=False)                             # brooch
    hx, hy = 1.4, 43.0 + sniff * 0.8
    sp.cap((1.0, 34.0), (1.2, 37.0), 2.4, 2.4, tones(dark(SKIN_VA, 0.9)))
    head = sp.union([sp.m_super(hx, hy, 6.8, 7.0, 2.4), sp.m_ell(hx + 0.6, hy - 3.6, 6.0, 3.8)], tones(SKIN_VA), frost=False)
    soft_blush(sp, hx + 3.6, hy - 2.0, 1.8, 1.2, (230, 120, 120), 0.4)
    lx, ly = look
    DX.eye(sp, hx + 3.0, hy + 0.8, 3.6, 3.2, E, (110, 90, 60), (lx, ly), blink, lash=INK, skin=SKIN_VA, bold=2)
    DX.eye(sp, hx - 1.6, hy + 0.8, 3.2, 3.0, E, (110, 90, 60), (lx, ly), blink, lash=INK, skin=SKIN_VA, bold=2)
    for ex, r in ((hx + 3.0, 2.6), (hx - 1.6, 2.4)):                                                       # big glasses
        ring = sp.m_ell(ex, hy + 0.8, r + 0.6, r + 0.4)[0] & ~sp.m_ell(ex, hy + 0.8, r, r - 0.2)[0]
        sp.fill(ring, (80, 40, 50))
    for q in range(10): sp.blob(hx - 4.4 - q * 0.4, hy + 0.6 - q * 1.4, 0.3, (220, 190, 120))             # bead chain
    DX.brow(sp, hx + 3.0, hy + 3.8, 3.2, E, +1, dark(VAL_HAIR, 0.7), th=1)
    sp.ell(hx + 5.8, hy - 0.8 + sniff * 0.8, 1.6, 1.8, tones(dark(SKIN_VA, 0.95)), frost=False)
    if sniff > 0.3:
        for q in range(3): thin(sp, (hx + 8.0 + q, hy + 1.0 + q * 0.6), (hx + 9.4 + q, hy + 1.6 + q * 0.6), (200, 220, 240), 0.2)   # sniff lines
    mx, my = hx + 3.0, hy - 4.4
    DX.mouth(sp, mx, my, 3.8, E, mouth_, (170, 60, 80), inside=(90, 24, 34), skin=SKIN_VA, maxh=4.0)
    for q in range(3): thin(sp, (hx + 5.0, hy - 3.4 - q * 0.8), (hx + 6.0, hy - 3.8 - q * 0.8), dark(SKIN_VA, 0.8), 0.14)
    parts = [sp.m_ell(hx - 0.6, hy + 4.6, 8.2, 4.2), sp.m_ell(hx - 5.6, hy + 0.4, 3.2, 5.4)]
    for q in range(10):
        a = math.pi * (0.05 + 0.95 * q / 9)
        parts.append(sp.m_ell(hx - 0.6 + math.cos(a) * 7.6, hy + 4.2 + math.sin(a) * 4.2, 1.8, 1.8))
    hair = sp.union(parts, tones(VAL_HAIR), exclude=head & (DX.YC < hy + 3.6) & (DX.XC > hx - 4.0), frost=False)
    g = np.random.default_rng(9)
    for q in range(30): sp.blob(g.uniform(hx - 8, hx + 7), g.uniform(hy, hy + 9), 0.4, dark(VAL_HAIR, 0.78), mask=hair)   # curls
    sp.anchors.update(head=(hx, hy), mouth=(mx, my))
    before = sp.m.copy()
    for side, base in ((-1, (-9.0, 28.0)), (1, (9.0, 28.0))):
        hn = hand_n if (hand_n is not None and side == 1) else (side * 3.0 + knit * math.sin(t * 9 + side) * 1.0, 16.0)
        kN, eN = ik(base, hn, 7.0, 7.0, -1.0 if side > 0 else 1.0)
        sp.cap(base, kN, 3.2, 2.8, tones(VAL_CARDI)); sp.cap(kN, eN, 2.8, 2.4, tones(VAL_CARDI))
        sp.ell(eN[0], eN[1], 1.8, 1.6, tones(SKIN_VA), frost=False)
    if knit > 0:
        thin(sp, (-4.0, 15.0), (6.0, 21.0 + math.sin(t * 9) * 1.0), (200, 200, 210), 0.3)
        thin(sp, (4.0, 15.0), (-6.0, 21.0 - math.sin(t * 9) * 1.0), (200, 200, 210), 0.3)
        sp.ell(0.0, 13.0, 4.0, 2.0, tones((255, 120, 60)))                                                    # the knitting
    _arm_over(sp, before)


# ================================================================================ props for E02
def avoska(sp, h, kind='smenka', t=0.0):
    """a string bag (авоська) hanging from hand/hook h: kind 'smenka' (bunny slippers) / 'pelmeni' (frozen white dumplings, frost)"""
    x, y = h
    for q in range(5): thin(sp, (x, y), (x - 4.0 + q * 2.0, y - 6.0), (200, 60, 60), 0.25)
    bag = sp.m_ell(x, y - 11.0, 5.4, 6.0)[0]
    if kind == 'smenka':
        sp.ell(x - 1.6, y - 11.0, 2.6, 3.6, tones((250, 200, 220)), frost=False)
        sp.ell(x + 1.8, y - 12.0, 2.6, 3.6, tones((250, 200, 220)), frost=False)
        for e_ in (-1.6, 1.8): sp.ell(x + e_, y - 7.6, 0.7, 1.6, tones((250, 180, 210)), frost=False)    # bunny ears
    else:
        g = np.random.default_rng(4)
        for q in range(9):
            sp.ell(x + g.uniform(-3.4, 3.4), y - 11.0 + g.uniform(-4, 4), 1.6, 1.2, tones((246, 240, 226)), frost=False)
        for q in range(8): sp.blob(x + g.uniform(-4, 4), y - 11 + g.uniform(-5, 5), 0.3, (220, 240, 255), keep=True)
    for q in range(-4, 5, 2): thin(sp, (x + q, y - 5.0), (x + q * 0.8, y - 17.0), (200, 60, 60), 0.18)        # the net
    for yy in (-8.0, -11.0, -14.0): thin(sp, (x - 5.0, y + yy), (x + 5.0, y + yy), (200, 60, 60), 0.18)
    sp.anchors['bag'] = (x, y - 11.0)


def taz(sp, t=0.0, back=False):
    """a zinc washing basin (the «sled» of Жора): side view, ~0.6 m"""
    sp.sup(0.0, 4.0, 13.0, 4.0, tones((180, 190, 206)), n=2.2, gloss=1.0)
    thin(sp, (-13.0, 8.0), (13.0, 8.0), (220, 228, 240), 0.8)
    for x in (-13.6, 13.6): sp.ell(x, 7.0, 1.4, 1.0, tones((150, 160, 176)))


def ledyanka(sp, t=0.0):
    """a red plastic «ледянка» sled under Тёма"""
    sp.sup(2.0, 2.4, 11.0, 2.4, tones((230, 50, 60)), n=2.4, gloss=1.0)
    thin(sp, (12.0, 3.0), (14.0, 7.0), (230, 50, 60), 1.2)


# ================================================================================ ГОША (сосед, 55)
DUB = (206, 170, 120)              # sheepskin coat «дублёнка»
DUB_FUR = (246, 236, 214)
MINK = (110, 74, 50)
SKIN_G = (238, 186, 160)


def gosha(sp, t=0.0, expr='sly', mouth_=0.0, look=(0.6, 0.0), blink=None, sit=False, hand_n=None, hand_f=None, prop_n=None,
          prop_f=None, legs=True):
    """ГОША: a sly round neighbour in a beige sheepskin «дублёнка» with a white fur collar, a mink «пирожок» hat, a thin moustache,
    a red nose, narrow sly eyes; sit=True — lounging in a folding chair (the chair is drawn too)"""
    E = X(expr)
    if blink is None: blink = ((t + 2.6) % 4.1) < 0.12
    br = 0.3 * math.sin(t * 1.6)
    oy = -14.0 if sit else 0.0
    if sit:                                                                 # the folding chair: green canvas on an aluminium frame
        thin(sp, (-10.0, 0.0), (6.0, 20.0), (190, 196, 210), 0.7); thin(sp, (6.0, 0.0), (-8.0, 20.0), (190, 196, 210), 0.7)
        sp.poly([(-12.0, 20.0), (8.0, 20.0), (6.0, 16.0), (-11.0, 16.0)], tones((60, 140, 90)))
        sp.poly([(-13.0, 18.0), (-11.0, 44.0), (-6.0, 44.0), (-8.0, 18.0)], tones((60, 140, 90)))
    if legs:
        for k_, dx in enumerate((-3.0, 3.2)):
            c = (60, 56, 70) if k_ else (50, 46, 58)
            if sit:
                sp.cap((dx * 0.6, 22.0), (dx + 12.0, 18.0), 3.4, 3.0, tones(c)); sp.cap((dx + 12.0, 18.0), (dx + 13.0, 4.0), 3.0, 2.6, tones(c))
                sp.sup(dx + 15.0, 2.0, 4.0, 2.0, tones((70, 50, 40)), n=2.4)
            else:
                sp.cap((dx, 26.0), (dx + 0.4, 4.0), 3.6, 3.0, tones(c)); sp.sup(dx + 1.8, 2.0, 4.4, 2.0, tones((70, 50, 40)), n=2.4)
    hf = hand_f if hand_f is not None else (-12.0, 34.0 + oy)
    kF, eF = ik((-10.0, 50.0 + oy + br), hf, 8.0, 7.6, 1.0)
    sp.cap((-10.0, 50.0 + oy + br), kF, 4.0, 3.4, tones(dark(DUB, 0.82))); sp.cap(kF, eF, 3.4, 3.0, tones(dark(DUB, 0.82)))
    if prop_f: prop_f(sp, eF)
    sp.ell(eF[0], eF[1], 2.0, 1.8, tones(SKIN_G), frost=False)
    body = sp.union([sp.m_ell(0.4, 37.0 + oy, 12.6, 15.0), sp.m_ell(0.0, 49.0 + oy, 10.0, 5.0)], tones(DUB))
    for q in range(5): sp.blob(2.4, 30.0 + oy + q * 4.0, 0.7, (90, 60, 40))                               # toggle buttons
    thin(sp, (2.0, 52.0 + oy), (2.6, 24.0 + oy), dark(DUB, 0.6), 0.3)
    fur = sp.union([sp.m_ell(0.8, 52.0 + oy, 9.4, 3.2), sp.m_cap((2.0, 52.0 + oy), (3.6, 36.0 + oy), 2.2, 1.6)], tones(DUB_FUR), frost=False)
    g = np.random.default_rng(13)
    for q in range(18): sp.blob(g.uniform(-8, 10), g.uniform(48, 55) + oy, 0.35, dark(DUB_FUR, 0.85), mask=fur)
    hx, hy = 2.0, 61.0 + oy
    head = sp.union([sp.m_ell(hx, hy, 7.0, 7.4), sp.m_ell(hx + 1.0, hy - 3.2, 6.0, 4.4)], tones(SKIN_G), frost=False)
    soft_blush(sp, hx + 3.8, hy - 2.2, 2.2, 1.6, (230, 100, 100), 0.5)
    lx, ly = look
    DX.eye(sp, hx + 3.4, hy + 1.0, 3.6, 3.0, E, (90, 70, 40), (lx, ly), blink, lash=INK, skin=SKIN_G, bold=1)
    DX.eye(sp, hx - 1.4, hy + 1.0, 3.2, 2.8, E, (90, 70, 40), (lx, ly), blink, lash=INK, skin=SKIN_G, bold=1)
    DX.brow(sp, hx + 3.4, hy + 4.0, 3.4, E, +1, (120, 90, 70), th=1)
    sp.ell(hx + 6.6, hy - 1.2, 2.0, 2.0, tones((236, 120, 110)), gloss=1.0, frost=False)                  # red nose
    mx, my = hx + 3.4, hy - 4.8
    DX.mouth(sp, mx, my, 4.2, E, mouth_, (160, 70, 70), inside=(90, 24, 34), teeth=(255, 246, 200), skin=SKIN_G, maxh=4.6)
    thin(sp, (mx - 2.6, my + 1.4), (mx + 2.8, my + 1.4), (90, 60, 40), 0.35)                            # thin moustache
    for q in range(3): thin(sp, (hx + 5.6, hy + 1.4 - q * 0.8), (hx + 6.8, hy + 1.8 - q * 1.1), dark(SKIN_G, 0.78), 0.12)
    hat = sp.union([sp.m_super(hx - 0.4, hy + 7.2, 7.4, 3.2, 3.0)], tones(MINK), frost=False)            # mink «пирожок»
    for q in range(16): thin(sp, (hx - 7.0 + q * 0.9, hy + 5.0), (hx - 7.2 + q * 0.9, hy + 9.6), mix(MINK, (200, 160, 120), 0.3 if q % 2 else 0.0), 0.2, mask=hat)
    sp.fill(sp.m_super(hx - 0.4, hy + 9.6, 6.8, 0.8, 4.0)[0] & hat, dark(MINK, 0.7))
    sp.anchors.update(head=(hx, hy), mouth=(mx, my))
    before = sp.m.copy()
    hn = hand_n if hand_n is not None else (10.0, 36.0 + oy)
    kN, eN = ik((10.0, 50.0 + oy + br), hn, 8.0, 7.6, -1.0)
    sp.cap((10.0, 50.0 + oy + br), kN, 4.2, 3.6, tones(DUB)); sp.cap(kN, eN, 3.6, 3.2, tones(DUB))
    sp.fill(sp.m_ell(eN[0] - 0.4, eN[1] + 1.8, 3.0, 1.0)[0], DUB_FUR)                                   # fur cuff
    if prop_n: prop_n(sp, eN)
    sp.ell(eN[0], eN[1], 2.0, 1.8, tones(SKIN_G), frost=False)
    sp.anchors['hand'] = eN
    _arm_over(sp, before)


def thermos(sp, h):
    x, y = h
    sp.sup(x + 0.6, y + 4.0, 1.8, 5.0, tones((200, 50, 50)), n=4.0, gloss=1.0)
    sp.sup(x + 0.6, y + 9.4, 1.4, 0.8, tones((220, 220, 230)), n=4.0)


def caviar(sp, h, empty=False, ladle=True):
    """a glass jar of red caviar (or empty, with a few eggs stuck to the glass)"""
    x, y = h
    jar = sp.sup(x + 0.6, y + 3.0, 2.8, 3.2, [(150, 170, 190), (200, 220, 236), (240, 248, 255)], n=3.0)
    if not empty:
        g = np.random.default_rng(2)
        sp.fill(sp.m_super(x + 0.6, y + 2.4, 2.4, 2.2, 3.0)[0] & jar, (230, 70, 40))
        for q in range(12): sp.blob(x + 0.6 + g.uniform(-2, 2), y + 2.4 + g.uniform(-1.8, 1.8), 0.4, (255, 140, 80), mask=jar)
    else:
        for q in range(3): sp.blob(x - 0.6 + q * 1.1, y + 1.0 + q * 0.4, 0.4, (230, 70, 40))
    sp.sup(x + 0.6, y + 6.6, 3.0, 0.8, tones((220, 200, 60)), n=4.0)                                    # lid rim
    if ladle and not empty: thin(sp, (x + 1.6, y + 4.0), (x + 4.0, y + 10.0), (200, 200, 210), 0.4)
    sp.anchors['jar'] = (x + 0.6, y + 3.0)


# ================================================================================ the white right-hand-drive «Corolla» (no real badge)
CAR_W = (246, 246, 242)


def corolla(sp, t=0.0, snow=0.0, lights=False, blink=False, chains=False, speed=0.0, gosha_kw=None):
    """a white 90s Japanese sedan, side view facing +x, ~4.4 m long (draw at 1.28 x hero scale like v86 cars): the driver sits on the
    RIGHT (the far side here, so we see the wheel on the right of the cabin = a right-hand drive joke); snow 0..1 = still buried
    (a white cap over everything); blink = the indicators + headlights flash (the key fob)"""
    body = sp.poly([(-70.0, 8.0), (-71.0, 24.0), (-50.0, 27.0), (-36.0, 44.0), (16.0, 44.0), (32.0, 27.0), (66.0, 24.0), (70.0, 14.0),
                    (68.0, 8.0)], tones(CAR_W), val=np.clip(0.9 - (44.0 - DX.YC) / 46.0, 0.05, 0.98))
    sp.fill(body & (DX.YC < 12.0), dark(CAR_W, 0.8))
    for (wx_, r) in ((-44.0, 11.0), (44.0, 11.0)):
        sp.fill(sp.m_ell(wx_, 10.0, r, r)[0] & body, (30, 30, 50))
    win = sp.m_poly([(-46.0, 27.6), (-34.0, 42.0), (-10.0, 42.0), (-10.0, 27.6)]) | sp.m_poly([(-7.0, 27.6), (-7.0, 42.0), (14.0, 42.0), (27.0, 27.6)])
    sp.paint(win, [(40, 60, 100), (80, 110, 160), (160, 200, 240)], np.clip((DX.YC - 27) / 15.0, 0, 1), ol=False, frost=False)
    if gosha_kw is not None:                                                  # Гоша's head in the window (the right seat = the far side)
        pass
    thin(sp, (-46.0, 27.4), (27.0, 27.4), (200, 204, 216), 0.5)
    thin(sp, (-8.5, 43.0), (-8.5, 9.0), dark(CAR_W, 0.7), 0.25); thin(sp, (16.0, 24.0), (16.0, 9.0), dark(CAR_W, 0.7), 0.25)
    for xh in (-20.0, 6.0): thin(sp, (xh, 22.0), (xh + 4.0, 22.0), (190, 196, 210), 0.5)
    sp.sup(-68.0, 18.0, 2.0, 3.0, tones((230, 50, 60)), n=3.0)                                              # tail light
    hl = sp.sup(67.0, 18.0, 2.4, 2.4, tones((255, 250, 220)), n=3.0, gloss=1.0)
    sp.fill(sp.m_super(-62.0, 18.0, 1.6, 1.4, 3.0)[0], (255, 160, 40) if (blink and int(t * 6) % 2 == 0) else (200, 120, 40))   # indicator
    sp.fill(sp.m_super(70.0, 10.0, 2.0, 2.4, 3.0)[0], (200, 204, 216))
    sp.fill(sp.m_super(-71.0, 10.0, 2.0, 2.4, 3.0)[0], (200, 204, 216))
    for wx_ in (-44.0, 44.0):
        sp.ell(wx_, 10.0, 9.4, 9.4, tones((30, 30, 40)))
        rim_ = sp.ell(wx_, 10.0, 5.4, 5.4, tones((190, 196, 210)), gloss=1.0)
        for q in range(5):
            a = t * speed + q * 1.256
            thin(sp, (wx_, 10.0), (wx_ + math.cos(a) * 5.0, 10.0 + math.sin(a) * 5.0), (120, 126, 146), 0.4, mask=rim_)
        if chains:
            for q in range(10):
                a = q * 0.628 + t * speed
                sp.blob(wx_ + math.cos(a) * 9.4, 10.0 + math.sin(a) * 9.4, 0.7, (180, 186, 200))
    if snow > 0:                                                              # still buried: a snow cap, melting down with the digging
        cap = sp.union([sp.m_ell(0.0, 4.0, 80.0, 30.0 + 26.0 * snow), sp.m_ell(-14.0, 30.0 * snow + 14.0, 48.0, 24.0 * snow + 8.0)],
                       tones((236, 244, 255)), frost=False)
        cap &= (DX.YC > 0.0)
        sp.fill(cap & (DX.YC < 10.0), (196, 212, 246))
        sp.fill(cap & (DX.YC < 4.0), (150, 170, 226))
    sp.anchors.update(front=(70.0, 14.0), roof=(-10.0, 44.0), win=(4.0, 34.0))


def flag(sp, t=0.0, label='ЖОРА', col=(230, 50, 60), lean=0.0):
    """a stick with a flag pushed into the snow over a buried car; the label is fitted inside the cloth"""
    thin(sp, (0.0, 0.0), (lean, 34.0), (150, 100, 56), 0.7)
    w = math.sin(t * 5.0) * 1.2
    cloth = sp.poly([(lean, 34.0), (lean + 22.0, 33.0 + w), (lean + 22.0, 22.0 + w), (lean, 23.0)], tones(col), frost=False)
    sp.txt_box([label], (lean + 1.0, 23.4 + w * 0.5, lean + 21.4, 32.6 + w * 0.5), (255, 255, 255), pad=0.5)


# ================================================================================ huskies + the dog sled (E04)
HUSKY_D = (90, 96, 110)
HUSKY_L = (238, 238, 240)


def husky(sp, t=0.0, run=True, lie=False, stare=False, ph=0.0, harness=(220, 50, 60)):
    """a Siberian husky, side view facing +x (~0.6 m at the shoulder = 1/3 of a man): grey back with a white belly and face mask,
    curled tail, blue eyes; run = gallop cycle; lie = lying flat (lunch break); stare = sitting, looking at the camera with huge eyes"""
    a = (t * 9.0 + ph) if run else 0.0
    if lie:
        body = sp.union([sp.m_ell(0.0, 5.0, 12.0, 4.6), sp.m_ell(11.0, 6.0, 4.6, 4.0)], tones(HUSKY_D))
        sp.fill(body & (DX.YC < 4.0), HUSKY_L)
        for dx in (8.0, 14.0): sp.cap((dx, 2.0), (dx + 6.0, 1.0), 1.2, 1.0, tones(HUSKY_L))
        hx, hy = 15.0, 7.0
    elif stare:
        sp.ell(-2.0, 7.0, 7.0, 6.0, tones(HUSKY_D)); sp.ell(0.0, 13.0, 5.6, 7.4, tones(HUSKY_D))
        sp.fill(sp.m_ell(1.4, 12.0, 3.0, 6.0)[0], HUSKY_L)
        for dx in (-1.0, 2.6): sp.cap((dx, 9.0), (dx + 0.6, 0.6), 1.2, 1.0, tones(HUSKY_L))
        hx, hy = 1.4, 22.0
    else:
        k = math.sin(a)
        for i, (dx, s_) in enumerate(((-8.0, 1), (-5.0, -1), (6.0, -1), (9.0, 1))):
            c = HUSKY_D if i % 2 else dark(HUSKY_D, 0.85)
            thin(sp, (dx, 8.0), (dx + s_ * k * 3.0, 0.6 + max(0, s_ * k) * 1.4), c, 1.1)
            sp.blob(dx + s_ * k * 3.0, 0.6, 0.9, HUSKY_L)
        body = sp.union([sp.m_ell(0.0, 10.0 + abs(k) * 0.8, 11.0, 4.6)], tones(HUSKY_D))
        sp.fill(body & (DX.YC < 8.6 + abs(k) * 0.8), HUSKY_L)
        hx, hy = 12.0, 14.0 + abs(k) * 0.8
        sp.cap((7.0, 12.0), (hx - 1.0, hy - 1.0), 3.2, 2.8, tones(HUSKY_D))
    if not stare:                                                           # curled tail
        tx = -12.0 if not lie else -12.0
        sp.cap((tx, 9.0 if not lie else 5.0), (tx - 2.0, 14.0 if not lie else 8.0), 1.8, 1.4, tones(HUSKY_D))
        sp.ell(tx - 1.0, 14.6 if not lie else 8.6, 1.8, 1.8, tones(HUSKY_L))
        thin(sp, (-6.0, 13.0 if not lie else 9.0), (6.0, 13.0 if not lie else 9.0), harness, 0.7)            # harness
        thin(sp, (6.0, 13.0 if not lie else 9.0), (7.0, 8.0 if not lie else 4.0), harness, 0.6)
    head = sp.ell(hx, hy, 3.8, 3.4, tones(HUSKY_D))
    sp.fill(sp.m_ell(hx + 1.0, hy - 0.8, 3.0, 2.2)[0] & head, HUSKY_L)                                        # face mask
    sp.ell(hx + 3.6 if not stare else hx, hy - 1.0, 1.8, 1.4, tones(HUSKY_L))                                 # muzzle
    sp.blob(hx + 5.0 if not stare else hx, hy - 0.6, 0.7, (30, 30, 40))                                       # nose
    for ex in ((hx + 1.0,) if not stare else (hx - 1.4, hx + 1.4)):
        r = 1.4 if stare else 0.8
        sp.ell(ex, hy + 0.6, r, r * 1.1, [(240, 240, 250), (250, 250, 255), (255, 255, 255)], frost=False)
        sp.blob(ex + (0.2 if stare else 0.3), hy + 0.6, r * 0.62, (90, 170, 240), keep=True)
        sp.blob(ex + (0.2 if stare else 0.3), hy + 0.6, r * 0.3, (20, 20, 30), keep=True)
        sp.blob(ex - r * 0.3, hy + 0.6 + r * 0.4, r * 0.22, (255, 255, 255), keep=True)
    for s_ in ((-1.6, 1.4),) if not stare else ((-2.6, 1.6), (2.6, 1.6)):                                    # ears
        sp.poly([(hx + s_[0] - 1.0, hy + 2.4), (hx + s_[0], hy + 5.6), (hx + s_[0] + 1.2, hy + 2.6)], tones(HUSKY_D))
    if not stare and not lie and run: thin(sp, (hx + 4.0, hy - 2.2), (hx + 4.6, hy - 3.6), (240, 110, 130), 0.5)     # tongue
    sp.anchors.update(head=(hx, hy))


def sled(sp, t=0.0, plate=True):
    """the dog sled «нарты» of ЯМЩИК Go: two curved runners, a slatted wooden bed, a rear handle bar, a checker taxi plate"""
    for dy in (0.0, 1.6):
        thin(sp, (-26.0, 2.0 + dy * 0.2), (22.0, 2.0 + dy * 0.2), (120, 80, 40), 0.9)
    sp.cap((22.0, 2.0), (26.0, 8.0), 0.9, 0.9, tones((120, 80, 40)))
    for x in range(-22, 20, 6): thin(sp, (x, 2.0), (x, 7.0), (150, 100, 50), 0.7)
    sp.poly([(-24.0, 7.0), (20.0, 7.0), (20.0, 9.0), (-24.0, 9.0)], tones((200, 150, 90)))
    thin(sp, (-24.0, 7.0), (-26.0, 22.0), (120, 80, 40), 0.9)
    thin(sp, (-26.0, 22.0), (-20.0, 22.0), (120, 80, 40), 0.9)
    if plate:
        pl = sp.sup(-2.0, 13.0, 8.0, 3.2, tones((250, 214, 40)), n=5.0)
        for i in range(8):
            x0 = -9.0 + i * 1.8
            sp.fill(pl & (DX.XC >= x0) & (DX.XC < x0 + 0.9) & (DX.YC > 13.0 + (0.0 if i % 2 else -1.6)) & (DX.YC < 14.6 + (0.0 if i % 2 else -1.6)), (30, 30, 40))
        thin(sp, (-2.0, 9.0), (-2.0, 10.0), (60, 60, 70), 0.6)
    sp.anchors.update(seat=(-6.0, 9.0), front=(26.0, 8.0), rear=(-24.0, 9.0))


def ushanka_vitek(sp, h):
    """Витёк's taxi ushanka: drawn on top of the head anchor (checker band)"""
    x, y = h
    sp.union([sp.m_ell(x - 0.2, y + 4.6, 6.4, 3.6), sp.m_cap((x - 5.0, y + 3.0), (x - 6.0, y - 3.0), 1.8, 1.6)], tones((90, 70, 60)))
    band = sp.m_super(x - 0.2, y + 3.4, 6.4, 1.0, 4.0)[0]
    sp.fill(band, (250, 214, 40))
    for i in range(7): sp.fill(band & (DX.XC >= x - 6.0 + i * 1.8) & (DX.XC < x - 5.1 + i * 1.8), (30, 30, 40))


# ================================================================================ ДИСПЕТЧЕР УК (в окне будки, по пояс) — E05
FURCOAT = (120, 80, 60)


def disp(sp, t=0.0, expr='deadpan', mouth_=0.0, look=(0.6, 0.0), blink=None, chew=0.0):
    """the УК dispatcher: a bored lady in a fox fur hat and a fur coat, heavy blue eye shadow, gold hoop earrings, a phone at the ear,
    a sandwich in the other hand (drawn from the waist)"""
    E = X(expr)
    if blink is None: blink = ((t + 1.7) % 4.4) < 0.12
    body = sp.poly([(-14.0, 4.0), (14.0, 4.0), (12.6, 26.0), (8.0, 31.0), (-8.0, 31.0), (-12.6, 26.0)], tones(FURCOAT))
    g = np.random.default_rng(17)
    for q in range(46): sp.blob(g.uniform(-12, 12), g.uniform(6, 30), 0.4, dark(FURCOAT, 0.75), mask=body)
    col_ = sp.union([sp.m_ell(-4.0, 31.0, 6.0, 3.2), sp.m_ell(5.0, 31.0, 6.0, 3.2)], tones((220, 120, 50)), frost=False)   # fox collar
    for q in range(16): thin(sp, (-9.0 + q * 1.2, 28.6), (-9.4 + q * 1.2, 33.4), (255, 220, 190) if q % 3 == 0 else (190, 96, 40), 0.25, mask=col_)
    sp.ell(0.0, 14.0, 0.7, 0.7, tones((240, 200, 70)), gloss=1.0, ol=False); sp.ell(0.0, 20.0, 0.7, 0.7, tones((240, 200, 70)), gloss=1.0, ol=False)
    sp.sup(0.0, 3.0, 22.0, 3.0, tones((150, 110, 80)), n=4.0, frost=False)                                  # the desk ledge
    hx, hy = 1.4, 40.0
    head = sp.union([sp.m_ell(hx, hy, 6.4, 6.8), sp.m_ell(hx + 0.8, hy - 3.0, 5.4, 4.0)], tones((240, 196, 170)), frost=False)
    soft_blush(sp, hx + 3.6, hy - 2.0, 2.0, 1.4, (240, 110, 130), 0.5)
    lx, ly = look
    DX.eye(sp, hx + 3.0, hy + 0.8, 3.6, 3.2, E, (80, 120, 90), (lx, ly), blink, lash=INK, skin=(240, 196, 170), bold=2, flick=True,
           lidc=(120, 150, 230))
    DX.eye(sp, hx - 1.6, hy + 0.8, 3.2, 3.0, E, (80, 120, 90), (lx, ly), blink, lash=INK, skin=(240, 196, 170), bold=2, flick=True,
           lidc=(120, 150, 230))
    DX.brow(sp, hx + 3.0, hy + 3.8, 3.2, E, +1, (90, 50, 40), th=1)
    sp.ell(hx + 5.6, hy - 0.8, 1.3, 1.6, tones((230, 186, 160)), frost=False)
    mx, my = hx + 3.0, hy - 4.2
    m = max(mouth_, 0.3 * chew * (0.5 + 0.5 * math.sin(t * 11)))
    DX.mouth(sp, mx, my, 3.8, E, m, (210, 40, 80), inside=(110, 30, 50), skin=(240, 196, 170), maxh=4.0)
    sp.ell(hx - 5.0, hy - 2.6, 1.2, 1.6, tones((240, 200, 70)), gloss=1.0, ol=False)                     # gold hoop
    hat = sp.union([sp.m_ell(hx - 0.4, hy + 6.6, 9.0, 5.0)], tones((220, 120, 50)), frost=False)          # fox fur hat
    for q in range(30): thin(sp, (hx - 8 + q * 0.55, hy + 3.0), (hx - 8.4 + q * 0.55, hy + 10.6), mix((220, 120, 50), (255, 230, 200), 0.3 if q % 3 == 0 else 0.0), 0.2, mask=hat)
    kN, eN = ik((9.0, 28.0), (hx + 6.0, hy - 1.0), 7.0, 7.0, -1.0)                                        # the phone at the ear
    sp.cap((9.0, 28.0), kN, 3.2, 2.8, tones(FURCOAT)); sp.cap(kN, eN, 2.8, 2.4, tones(FURCOAT))
    sp.sup(eN[0] + 0.6, eN[1] + 1.4, 1.4, 3.0, tones((40, 40, 50)), n=4.0)
    sp.ell(eN[0], eN[1], 1.7, 1.6, tones((240, 196, 170)), frost=False)
    kF, eF = ik((-9.0, 28.0), (-4.0, 22.0 + 2 * math.sin(t * 3)), 6.0, 6.0, 1.0)                           # the sandwich
    sp.cap((-9.0, 28.0), kF, 3.0, 2.6, tones(FURCOAT)); sp.cap(kF, eF, 2.6, 2.2, tones(FURCOAT))
    sp.sup(eF[0] + 2.6, eF[1] + 1.6, 3.4, 1.4, tones((230, 190, 120)), n=3.0)
    sp.sup(eF[0] + 2.6, eF[1] + 2.4, 3.0, 0.5, tones((230, 90, 90)), n=3.0, ol=False)
    sp.ell(eF[0], eF[1], 1.6, 1.5, tones((240, 196, 170)), frost=False)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my))


# ================================================================================ the УК grader (E05), drawn small, blit at ×3.2 hero scale
GRADER = (255, 140, 30)


def grader(sp, t=0.0, blade=0.0, beacon=True, vitek_kw=None, spin=0.0, snow=True):
    """an orange road grader «СУГРОБ-СЕРВИС», side view facing +x, ~8.5 m long = 120 u (14 u/m: blit at ~2.1x the hero scale):
    rear engine with a grille and an exhaust, tall glass cab with Витёк, a long arched front beam, a curved blade under it
    (blade 0..1 lowered), rear tandem + front wheel, a flashing beacon, snow on the roof"""
    O_ = GRADER
    for x in (-46.0, -26.0):                                                                               # rear tandem tyres
        sp.ell(x, 10.0, 10.0, 10.0, tones((34, 34, 42)))
        for q in range(10):
            a = q * 0.628 + t * spin * 0.2
            thin(sp, (x + math.cos(a) * 8.6, 10 + math.sin(a) * 8.6), (x + math.cos(a) * 10.0, 10 + math.sin(a) * 10.0), (60, 60, 70), 0.6)
        r_ = sp.ell(x, 10.0, 5.2, 5.2, tones((236, 196, 60)))
        for q in range(5):
            a = t * spin + q * 1.256
            sp.blob(x + math.cos(a) * 3.4, 10 + math.sin(a) * 3.4, 0.7, (150, 110, 30), mask=r_)
    sp.sup(-36.0, 22.0, 16.0, 3.0, tones((60, 60, 72)), n=4.0)                                               # tandem beam
    sp.sup(-34.0, 31.0, 26.0, 8.0, tones(O_), n=5.0)                                                         # engine hood
    sp.sup(-59.0, 31.0, 2.6, 7.0, tones((50, 50, 60)), n=4.0)                                                # rear grille
    for q in range(5): thin(sp, (-60.6, 25.6 + q * 2.6), (-57.4, 25.6 + q * 2.6), (120, 120, 130), 0.4)
    for q in range(6): thin(sp, (-50.0 + q * 4.0, 36.0), (-50.0 + q * 4.0, 27.0), dark(O_, 0.62), 0.5)      # hood louvres
    sp.sup(-44.0, 44.0, 1.4, 6.0, tones((70, 70, 80)), n=4.0)                                                # exhaust
    thin(sp, (-45.0, 50.4), (-43.0, 50.4), (30, 30, 36), 0.8)
    sp.txt_box(['СУГРОБ-СЕРВИС'], (-56.0, 26.0, -14.0, 33.0), (40, 30, 30), pad=0.3)
    sp.sup(-4.0, 40.0, 11.0, 16.0, tones(O_), n=6.0)                                                         # cab
    win = sp.m_super(-3.4, 43.0, 9.0, 11.6, 6.0)[0]
    sp.paint(win, [(56, 86, 140), (110, 150, 200), (196, 226, 250)], np.clip((DX.YC - 32) / 22.0, 0, 1), ol=False, frost=False)
    thin(sp, (-3.4, 31.6), (-3.4, 54.4), dark(O_, 0.7), 0.8, mask=win)                                       # window post
    if vitek_kw is not None:                                                                                 # Витёк at the wheel
        sp.ell(1.4, 41.0, 4.2, 4.4, tones((236, 190, 160)), frost=False)
        sp.ell(0.8, 45.4, 4.8, 2.4, tones((240, 200, 40)), frost=False)                                     # hard hat
        sp.blob(3.6, 41.6, 0.7, (20, 20, 30)); thin(sp, (2.0, 38.6), (4.6, 39.0), (150, 60, 60), 0.4)
        thin(sp, (4.0, 36.0), (8.0, 34.0), (40, 40, 50), 0.8)                                               # the wheel
    for d in (-1.0, 1.0): thin(sp, (-4.0 + d * 0.6, 24.0), (-4.0 + d * 0.6, 23.0), (60, 60, 70), 0.4)
    for q in range(4): thin(sp, (-14.4, 12.0 + q * 3.6), (-11.6, 12.0 + q * 3.6), (70, 70, 80), 0.5)       # ladder
    thin(sp, (8.0, 52.0), (12.0, 54.0), (40, 40, 50), 0.5); sp.sup(12.6, 52.0, 1.0, 2.2, tones((40, 40, 50)), n=3.0)   # mirror
    if snow:
        sp.sup(-4.0, 56.6, 12.0, 1.8, tones((246, 250, 255)), n=3.0, frost=False)
        sp.sup(-34.0, 39.4, 24.0, 1.4, tones((246, 250, 255)), n=3.0, frost=False)
    if beacon:
        on = int(t * 5) % 2 == 0
        sp.sup(-4.0, 59.4, 3.0, 1.8, tones((255, 200, 40) if on else (170, 110, 20)), n=3.0)
    sp.poly([(4.0, 26.0), (60.0, 30.0), (62.0, 24.0), (8.0, 20.0)], tones(O_))                               # arched front beam
    sp.sup(60.0, 22.0, 4.0, 4.0, tones(O_), n=4.0)
    sp.ell(58.0, 10.0, 10.0, 10.0, tones((34, 34, 42)))                                                      # front tyre
    for q in range(10):
        a = q * 0.628 + t * spin * 0.2
        thin(sp, (58 + math.cos(a) * 8.6, 10 + math.sin(a) * 8.6), (58 + math.cos(a) * 10.0, 10 + math.sin(a) * 10.0), (60, 60, 70), 0.6)
    r_ = sp.ell(58.0, 10.0, 5.2, 5.2, tones((236, 196, 60)))
    for q in range(5):
        a = t * spin + q * 1.256
        sp.blob(58 + math.cos(a) * 3.4, 10 + math.sin(a) * 3.4, 0.7, (150, 110, 30), mask=r_)
    by = 8.0 - 6.0 * blade                                                                                   # the blade (moldboard)
    thin(sp, (14.0, 22.0), (18.0, by + 10.0), (60, 60, 72), 1.4); thin(sp, (34.0, 26.0), (30.0, by + 10.0), (60, 60, 72), 1.4)
    sp.sup(24.0, by + 13.0, 18.0, 2.0, tones((70, 70, 80)), n=4.0)                                           # circle
    sp.poly([(6.0, by + 11.0), (42.0, by + 11.0), (44.0, by + 4.0), (42.0, by), (6.0, by), (4.0, by + 4.0)], tones((206, 212, 226)))
    thin(sp, (6.0, by + 0.4), (42.0, by + 0.4), (120, 126, 140), 0.6)
    if snow: sp.sup(46.0, by + 4.0, 3.6, 4.0, tones((246, 250, 255)), n=2.6, frost=False)
    sp.anchors.update(blade=(44.0, by + 4.0), cab=(-3.4, 43.0))


def receipt_img(w=520, h=760, total=1400, extra=None, t=0.0, t_extra=0.0):
    """the УК «СУГРОБ-СЕРВИС» receipt (an RGBA overlay, drawn at 1/4 and upscaled = pixel look)"""
    from PIL import Image as _I, ImageDraw as _D
    import overlays as _O
    S_ = 4
    wl, hl = w // S_, h // S_
    im = _I.new('RGBA', (wl, hl), (0, 0, 0, 0)); d = _D.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, wl - 1, hl - 1], fill=(250, 248, 236, 255), outline=(120, 120, 120, 255))
    for x in range(0, wl, 6): d.polygon([(x, hl - 1), (x + 3, hl - 5), (x + 6, hl - 1)], fill=(0, 0, 0, 0))
    def tx(y, s, size, col=(30, 30, 40)):
        f = _O.pfont(size)
        while f.getlength(s) > wl - 12 and size > 4: size -= 1; f = _O.pfont(size)
        d.text(((wl - f.getlength(s)) / 2, y), s, font=f, fill=col)
    tx(8, 'УК «СУГРОБ-СЕРВИС»', 9, (30, 60, 150))
    tx(24, 'КВИТАНЦИЯ ЗА ЯНВАРЬ', 6, (80, 80, 90))
    d.line([(8, 36), (wl - 8, 36)], fill=(120, 120, 130), width=1)
    rows = [('ТЕПЛО', '4210'), ('ВОДА', '1080')]
    f = _O.pfont(6)
    for i, (a, b) in enumerate(rows):
        d.text((8, 44 + i * 13), a, font=f, fill=(40, 40, 50)); d.text((wl - 8 - f.getlength(b), 44 + i * 13), b, font=f, fill=(40, 40, 50))
    tx(74, 'УБОРКА СНЕГА:', 6, (200, 40, 40))
    tx(86, f'{total} ₽', 12, (200, 40, 40))
    if extra and t >= t_extra:
        tx(112, 'ПЕРЕРАСЧЁТ:', 6, (200, 40, 40)); tx(124, extra, 12, (200, 40, 40))
    a = np.array(im.resize((wl * S_, hl * S_), _I.NEAREST))
    return a
