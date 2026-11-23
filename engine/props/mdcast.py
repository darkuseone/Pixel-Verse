"""«MOTION DETECTED» cast + props. Rendering manner = the «Ключевой сотрудник» sprite manner (props/kspix.py: toner specks, dual
rim, ink outline) — owner 23.11.2026: «drawing like the last Russian season»; the characters themselves are new.
Sprite px, feet anchor at (0, 0), x right = facing side, y UP. Rim light + outline are added by kspix.Act / kspix.draw.
  glenn(sp, ...)  — Glenn Hollis, 47: «a coat hanger» — very tall and lanky, long horse face with a huge chin, a sandy FLAT-TOP,
                    big ears, an open red-green TARTAN BATHROBE over a navy golf polo, khaki cargo shorts in November, knobby bare
                    shins, white tube socks in black slides (slipper=False on one foot: the lost slipper)
  doris(sp, ...)  — DORIS, the KNOCKR Pro smart doorbell: a black glossy slab, a big round camera lens = her eye (iris + glint
                    looks around), an LED arc above it = her brow, a round button with an LED ring that glows when she talks;
                    dnd=True — a blue crescent moon on the button (Do Not Disturb)
  trent(sp, ...)  — Trent, the solar guy: short and square, gelled quiff, sunglasses on the head, a HUGE white smile, an orange
                    puffer vest over a white polo, a lanyard badge «SUNNYSIDE SOLAR», a clipboard
  courier(sp,...) — the PARCELZ courier: teal cap + vest, brown shorts, always mid-sprint (only on the camera footage)
  tag(sp, h) / clipboard / mug / phone props"""
import math
import numpy as np
from props import dibspix as DX
from props.dibspix import dark, mix, erode, dilate, ik, EXPR
from props.kspix import tones, thin, stroke, INK, WHITE

# ---------------------------------------------------------------- palette
SKIN = (240, 192, 156)
SKIN_T = (198, 132, 96)            # trent: spray tan
ROBE = (178, 40, 44)               # tartan robe red
ROBE_G = (34, 96, 62)              # tartan green
ROBE_Y = (240, 206, 90)            # tartan thin yellow line
POLO = (40, 60, 120)               # navy golf polo
SHORTS = (190, 168, 112)           # khaki cargo
SOCK = (250, 250, 246)
SLIDE = (36, 36, 40)
HAIR_G = (214, 176, 108)           # sandy flat-top
DEV = (34, 36, 42)                 # doorbell body
DEV_L = (70, 74, 86)
LED = (90, 220, 255)
VEST = (246, 128, 40)              # trent puffer vest
POLO_W = (246, 246, 240)
HAIR_T = (70, 46, 30)
TEAL = (30, 160, 160)              # PARCELZ
BROWN = (120, 84, 50)
TAG = (255, 140, 40)               # «SORRY WE MISSED YOU» door tag

XTRA = dict(
    furious=dict(eo=1.25, pu=0.35, bt=0.85, bl=-0.3, mo=0.95, mc=-0.3),
    smug=dict(eo=0.7, pu=0.55, bt=0.25, bl=0.0, mo=0.0, mc=0.9, lid=0.4),
    proud=dict(eo=0.9, pu=0.6, bt=-0.15, bl=0.35, mo=0.0, mc=0.85, lid=0.15),
    hopeful=dict(eo=1.1, pu=0.68, bt=-0.5, bl=0.45, mo=0.0, mc=0.6),
    shock=dict(eo=1.4, pu=0.3, bt=-0.65, bl=0.85, mo=0.8, mc=0.0),
    crushed=dict(eo=0.8, pu=0.62, bt=-0.75, bl=0.15, mo=0.0, mc=-0.7, lid=0.35),
    panic=dict(eo=1.45, pu=0.28, bt=-0.85, bl=0.95, mo=0.95, mc=-0.2),
    deadpan=dict(eo=0.65, pu=0.6, bt=0.0, bl=0.0, mo=0.0, mc=-0.05, lid=0.55),
    sweet=dict(eo=0.75, pu=0.6, bt=-0.35, bl=0.3, mo=0.0, mc=0.95, lid=0.35),
    smirk=dict(eo=0.6, pu=0.6, bt=0.35, bl=0.0, mo=0.0, mc=0.6, lid=0.5),
    sales=dict(eo=1.05, pu=0.6, bt=-0.4, bl=0.4, mo=0.35, mc=1.0),
    stare=dict(eo=1.0, pu=0.55, bt=0.1, bl=0.0, mo=0.0, mc=-0.1, lid=0.1),
    dead=dict(eo=0.75, pu=0.6, bt=-0.2, bl=-0.1, mo=0.0, mc=-0.35, lid=0.6),
)


def X(expr):
    if isinstance(expr, dict): return dict(expr)
    return dict(XTRA.get(expr) or EXPR.get(expr, EXPR['normal']))


# ================================================================================ hand props
def door_tag(sp, h, s=1.0, ang=0.0):
    """the orange door tag «SORRY WE MISSED YOU» held at its top corner"""
    x, y = h
    c, si = math.cos(ang), math.sin(ang)
    def R(dx, dy): return (x + dx * c - dy * si, y + dx * si + dy * c)
    pts = [R(-1.0 * s, 1.0 * s), R(9.0 * s, 1.0 * s), R(9.0 * s, -13.0 * s), R(-1.0 * s, -13.0 * s)]
    sp.poly(pts, tones(TAG), stripes=False)
    sp.blob(*R(4.0 * s, -0.6 * s), 0.9 * s, (250, 250, 240))
    bx = (min(p[0] for p in pts) + 0.6, min(p[1] for p in pts) + 0.8, max(p[0] for p in pts) - 0.6, max(p[1] for p in pts) - 2.6)
    sp.txt_box(['SORRY', 'WE', 'MISSED', 'YOU'], bx, (40, 20, 10), pad=0.15, lead=0.1)
    sp.anchors['tag'] = R(4.0 * s, -6.0 * s)


def clipboard(sp, h, label='SOLAR'):
    x, y = h
    sp.sup(x + 2.0, y + 1.0, 4.6, 6.0, tones((170, 120, 70)), n=6.0)
    sp.sup(x + 2.0, y + 0.6, 3.8, 5.0, tones((250, 250, 244)), n=6.0, stripes=False)
    sp.fill(sp.m_super(x + 2.0, y + 6.4, 1.6, 0.8, 4.0)[0], (190, 190, 196))
    sp.txt_box([label], (x - 1.4, y + 2.0, x + 5.4, y + 4.6), (220, 120, 20), pad=0.1)
    for q in range(3): thin(sp, (x - 1.0, y + 0.6 - q * 1.4), (x + 5.0, y + 0.6 - q * 1.4), (150, 150, 160), 0.16)


def mug(sp, h, label='#1 DAD'):
    x, y = h
    sp.sup(x + 1.0, y + 1.6, 2.4, 3.0, tones((250, 250, 244)), n=4.0)
    ring = sp.m_ell(x + 3.6, y + 1.8, 1.6, 1.7)[0] & ~sp.m_ell(x + 3.6, y + 1.8, 0.9, 1.0)[0]
    sp.fill(ring, (210, 210, 200))
    if label: sp.txt_box([label], (x - 1.2, y + 0.2, x + 3.2, y + 3.0), (200, 40, 60), pad=0.1)
    sp.anchors['mug'] = (x + 1.0, y + 4.6)


def phone(sp, h):
    x, y = h
    sp.sup(x + 0.6, y + 2.6, 1.8, 3.4, tones((30, 30, 36)), n=5.0, gloss=0.5)
    sp.fill(sp.m_super(x + 0.6, y + 2.6, 1.3, 2.8, 6.0)[0], (120, 200, 255))


def tartan(sp, m, ox, oy, k=1.0):
    """red tartan with green bands and a thin yellow line, drawn into mask m (sprite px grid, fixed -> no boiling)"""
    xx = (DX.XC - ox) / k; yy = (DX.YC - oy) / k
    g = ((np.floor(xx / 4.0) % 2 == 0) & (np.mod(xx, 4.0) < 1.6)) | ((np.floor(yy / 4.0) % 2 == 0) & (np.mod(yy, 4.0) < 1.6))
    both = ((np.floor(xx / 4.0) % 2 == 0) & (np.mod(xx, 4.0) < 1.6)) & ((np.floor(yy / 4.0) % 2 == 0) & (np.mod(yy, 4.0) < 1.6))
    yl = (np.abs(np.mod(xx, 8.0) - 6.0) < 0.25) | (np.abs(np.mod(yy, 8.0) - 6.0) < 0.25)
    col = sp.col.astype(np.int16)
    gm = m & g
    col[gm] = (col[gm] * 0.35 + np.array(ROBE_G) * 0.65).astype(np.int16)
    bm = m & both
    col[bm] = (col[bm] * 0.6).astype(np.int16)
    ym = m & yl & ~both
    col[ym] = (col[ym] * 0.4 + np.array(ROBE_Y) * 0.6).astype(np.int16)
    sp.col = np.clip(col, 0, 255).astype(np.uint8)


# ================================================================================ GLENN
def glenn(sp, t=0.0, expr='smug', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
          legs=True, ox=0.0, oy=0.0, walk=None, lean=0.0, sweat=0.0, robe=True, slipper=True, run=None, seated=False):
    """GLENN. walk — walk phase; run — sprint phase (big stride, robe flaps back); seated — sits (knees forward);
    slipper=False — the near foot is only a white sock"""
    E = X(expr)
    if blink is None: blink = ((t + 0.7) % 4.1) < 0.12
    br = 0.35 * math.sin(t * 2.0)
    ph = run if run is not None else walk
    bob = abs(math.sin(ph)) * (2.4 if run is not None else 1.0) if ph is not None else 0.0
    sh_ = 14.0 if seated else 0.0
    def Q(x, y): return (x + ox + lean * (y / 80.0) * 6.0, y + oy + (bob if y > 12 else 0.3 * bob) - (sh_ if y > 12 else 0.0))
    swing = math.sin(ph) * (9.0 if run is not None else 4.0) if ph is not None else 0.0
    flap = (6.0 + 2.0 * math.sin(t * 17)) if run is not None else 0.0
    # ---------------------------------------------------------------- far arm
    shF = Q(-8.0, 76.0 + br * 0.3)
    hf = hand_f if hand_f is not None else Q(-11.0 - swing * 0.7, 52.0 + (6.0 if run is not None else 0.0))
    kF, eF = ik(shF, hf, 12.0, 11.0, -1.0)
    sp.cap(shF, kF, 3.0, 2.6, tones(dark(ROBE if robe else POLO, 0.82)))
    sp.cap(kF, eF, 2.4, 1.8, tones(dark(ROBE if robe else SKIN, 0.82)))
    sp.ell(eF[0], eF[1] - 0.3, 2.2, 2.1, tones(dark(SKIN, 0.86)))
    if prop_f: prop_f(sp, eF)
    sp.anchors['hand_f'] = eF
    # ---------------------------------------------------------------- robe back panel (behind the legs when running)
    if robe:
        back = sp.m_poly([Q(-7.0, 74.0), Q(-9.5 - flap, 34.0), Q(-6.0 - flap * 1.6, 22.0), Q(3.0, 24.0), Q(4.0, 70.0)])
        sp.paint(back, tones(dark(ROBE, 0.78)), np.full(DX.XC.shape, 0.5, np.float32))
        tartan(sp, back, ox, oy)
    # ---------------------------------------------------------------- legs: long knobby shins, tube socks, slides
    if legs:
        sw = math.sin(ph) * (7.0 if run is not None else 3.0) if ph is not None else 0.0
        for k_, dx in enumerate((-2.6, 2.8)):
            near = k_ == 1
            s_ = sw if near else -sw
            if seated:
                hip = Q(dx * 0.9, 34.0)
                knee = (hip[0] + 13.0, hip[1] + 1.0)
                foot = (knee[0] + 1.0, 1.6 + oy)
            else:
                hip = Q(dx * 0.9, 34.0)
                foot = (dx + s_ * 1.4 + ox, 1.6 + max(0.0, s_) * (0.9 if run is not None else 0.3) + oy)
                knee = ((hip[0] + foot[0]) / 2 + (2.6 if run is not None and s_ > 0 else 0.8), (hip[1] + foot[1]) / 2 + 0.6)
            sk = SKIN if near else dark(SKIN, 0.86)
            sh_c = SHORTS if near else dark(SHORTS, 0.86)
            sp.cap(hip, knee, 3.6, 3.0, tones(sh_c)) if seated else sp.cap(hip, (hip[0] * 0.7 + knee[0] * 0.3, hip[1] * 0.7 + knee[1] * 0.3 - 2.0), 3.8, 3.4, tones(sh_c))
            sp.cap(knee if not seated else knee, (foot[0], foot[1] + 5.0), 1.6, 1.3, tones(sk))
            sp.ell(knee[0] + 0.4, knee[1], 1.9, 1.7, tones(sk))                                             # knobby knee
            sp.cap((foot[0], foot[1] + 5.4), (foot[0], foot[1] + 1.2), 1.7, 1.7, tones(SOCK if near else dark(SOCK, 0.88)), stripes=False)
            thin(sp, (foot[0] - 1.6, foot[1] + 5.0), (foot[0] + 1.6, foot[1] + 5.0), (200, 40, 40), 0.3)   # sock stripe
            if slipper or not near:
                sp.sup(foot[0] + 1.8, foot[1] + 0.2, 4.2, 1.1, tones(SLIDE if near else dark(SLIDE, 0.85)), n=2.4, gloss=0.4)
                sp.fill(sp.m_super(foot[0] + 1.0, foot[1] + 1.4, 2.0, 0.6, 4.0)[0], (220, 220, 220))
            else:
                sp.sup(foot[0] + 1.6, foot[1] + 0.6, 3.6, 1.2, tones(SOCK), n=2.4, stripes=False)
        # cargo pockets
        sp.fill(sp.m_super(*Q(3.6, 30.0 if not seated else 46.0), 1.8, 2.2, 4.0)[0], dark(SHORTS, 0.8))
    # ---------------------------------------------------------------- torso: long narrow polo, a little gut, robe open
    chest = sp.m_super(*Q(0.4, 64.0), 8.4, 13.0, 2.4)
    gut = sp.m_ell(*Q(2.2, 46.0), 8.6, 8.0)
    body = sp.union([chest, gut], tones(POLO))
    thin(sp, Q(1.0, 76.0), Q(1.0, 70.0), dark(POLO, 0.6), 0.3)                                            # placket
    sp.blob(*Q(1.0, 73.0), 0.5, (230, 230, 230)); sp.blob(*Q(1.0, 71.0), 0.5, (230, 230, 230))
    sp.fill(sp.m_super(*Q(-3.6, 70.0), 1.4, 1.0, 4.0)[0] & body, (240, 196, 70))                         # tiny golf logo
    if robe:
        for side, x0, x1 in ((-1, -8.6, -3.2), (1, 6.0, 9.6)):
            pts = [Q(x0, 78.0), Q(x1, 78.0), Q(x1 + side * (1.0 + flap * 0.2), 26.0), Q(x0 + side * (2.0 + flap * 0.3), 26.0)]
            m = sp.m_poly(pts)
            sp.paint(m, tones(ROBE), DX.lit(np.clip((DX.XC - Q(0, 0)[0]) / 10.0, -0.9, 0.9), np.full(DX.XC.shape, 0.2, np.float32)))
            tartan(sp, m, ox, oy)
            e = m & ~erode(m)
            sp.col[e] = dark(ROBE, 0.5)
        thin(sp, Q(-8.0, 46.0), Q(-3.0, 44.0), (200, 60, 60), 0.6)                                       # dangling belt
        thin(sp, Q(-3.0, 44.0), Q(-4.0, 34.0 - flap * 0.6), (200, 60, 60), 0.6)
        sp.fill(sp.m_super(*Q(-5.4, 48.0), 0.9, 0.8, 4.0)[0], dark(ROBE, 0.55))
    # ---------------------------------------------------------------- neck + the long horse head
    sp.cap(Q(1.6, 77.0), Q(2.4, 82.0), 2.2, 2.0, tones(dark(SKIN, 0.9)))
    thin(sp, Q(2.6, 79.2), Q(3.6, 80.0), dark(SKIN, 0.68), 0.3)                                            # adam's apple
    hx, hy = Q(3.0, 91.0)
    head = sp.union([sp.m_ell(hx, hy + 2.0, 6.4, 8.6), sp.m_ell(hx + 1.8, hy - 6.0, 5.6, 4.4)], tones(SKIN))   # long face + big chin
    sp.ell(hx - 5.8, hy + 1.4, 1.8, 2.8, tones(dark(SKIN, 0.92)))                                       # big ear
    thin(sp, (hx - 6.0, hy + 2.6), (hx - 5.6, hy + 0.0), dark(SKIN, 0.68), 0.22)
    # sandy FLAT-TOP: a flat brick on top
    ft = sp.union([sp.m_super(hx - 0.2, hy + 9.6, 6.8, 2.4, 6.0), sp.m_super(hx - 4.8, hy + 5.4, 1.8, 3.0, 3.0)], tones(HAIR_G))
    for q in range(7): thin(sp, (hx - 6.0 + q * 2.0, hy + 11.6), (hx - 6.0 + q * 2.0, hy + 8.0), dark(HAIR_G, 0.78), 0.16)
    lx, ly = look
    DX.eye(sp, hx + 3.2, hy + 3.2, 3.4, 3.6, E, (70, 120, 170), (lx, ly), blink, lash=INK, skin=SKIN, bold=1, bag=dark(SKIN, 0.84))
    DX.eye(sp, hx - 1.2, hy + 3.2, 2.9, 3.4, E, (70, 120, 170), (lx, ly), blink, lash=INK, skin=SKIN, bold=1)
    DX.brow(sp, hx + 3.2, hy + 6.6, 3.6, E, +1, dark(HAIR_G, 0.7), th=1.3)
    DX.brow(sp, hx - 1.2, hy + 6.5, 3.0, E, -1, dark(HAIR_G, 0.7), th=1.3)
    sp.cap((hx + 5.2, hy + 2.6), (hx + 7.2, hy - 1.0), 1.0, 1.6, tones(dark(SKIN, 0.98)))                 # long nose
    sp.dot(hx + 6.6, hy - 1.4, dark(SKIN, 0.6))
    DX.blush(sp, hx + 1.6, hy - 0.6, 1.2, 0.8, (236, 120, 110))
    mx, my = hx + 3.6, hy - 3.4
    DX.mouth(sp, mx, my, 4.4, E, mouth_, (160, 80, 70), inside=(96, 26, 36), teeth=(255, 255, 250), skin=SKIN, maxh=5.6)
    thin(sp, (hx + 2.0, hy - 8.6), (hx + 5.6, hy - 8.4), dark(SKIN, 0.72), 0.22)                          # chin cleft line
    sp.dot(hx + 3.8, hy - 7.4, dark(SKIN, 0.75))
    if sweat > 0:
        for i, (x, y) in enumerate(((hx + 5.0, hy + 6.0), (hx - 2.0, hy + 7.0))[:int(1 + sweat)]):
            yy = y - ((t * 3.5 + i * 1.3) % 3.0)
            sp.ell(x, yy, 0.6, 1.0, tones((170, 220, 255)), ol=False)
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 1.0, hy + 3.2), chest=Q(1.0, 60.0))
    # ---------------------------------------------------------------- near arm
    before = sp.m.copy()
    shN = Q(8.4, 76.0 + br * 0.3)
    hn = hand_n if hand_n is not None else Q(11.0 + swing * 0.7, 51.0 + (6.0 if run is not None else 0.0))
    kN, eN = ik(shN, hn, 12.0, 11.0, -1.0)
    sp.cap(shN, kN, 3.2, 2.8, tones(ROBE if robe else POLO))
    if robe:
        sp.cap(kN, eN, 2.6, 2.0, tones(ROBE))
        cm = sp.m_cap(kN, eN, 2.6, 2.0)[0]; tartan(sp, cm, ox, oy)
    else: sp.cap(kN, eN, 1.9, 1.7, tones(SKIN))
    if prop_n and getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.ell(eN[0], eN[1] - 0.3, 2.3, 2.2, tones(SKIN))
    if prop_n and not getattr(prop_n, 'behind', False): prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m & before
    sp.col[o] = INK


# ================================================================================ DORIS (KNOCKR Pro)
def doris(sp, t=0.0, expr='deadpan', mouth_=0.0, look=(0.0, 0.0), blink=None, dnd=False, ring=None, glow=1.0):
    """DORIS: the slab is 12 x 28 sprite px; the lens (her eye) at the top, the LED brow arc above it, the button + LED ring below.
    mouth_ (talk) brightens the LED ring in pulses; dnd — moon icon; ring — 0..1 «ding» flash of the button"""
    E = X(expr)
    if blink is None: blink = ((t + 0.4) % 5.3) < 0.10
    talk = max(mouth_, 0.0)
    body = sp.sup(0.0, 14.0, 6.2, 14.0, tones(DEV), n=4.0, gloss=0.8)
    sp.fill(sp.m_super(0.0, 14.0, 5.4, 13.2, 4.0)[0] & ~sp.m_super(0.0, 14.0, 4.8, 12.6, 4.0)[0], DEV_L)         # bevel
    # LED brow arc (expression)
    bt = E['bt']; bl = E.get('bl', 0.0)
    for i in range(9):
        u = (i - 4) / 4.0
        x = u * 3.6
        y = 25.2 + (1.0 - u * u) * (0.9 + 0.5 * bl) - u * bt * 1.4
        on = 0.55 + 0.45 * glow
        sp.blob(x, y, 0.55, tuple(int(c * on) for c in LED), keep=True)
    # the lens = eye: dark glass, iris ring, pupil, glint; lid from E['lid'] / blink
    ex, ey = 0.0, 20.0
    sp.ell(ex, ey, 4.0, 4.0, tones((20, 22, 28)), gloss=0.0)
    iris = sp.m_ell(ex + look[0] * 0.8, ey + look[1] * 0.8, 2.6, 2.6)[0]
    sp.fill(iris, (40, 70, 110))
    rr = sp.m_ell(ex + look[0] * 0.8, ey + look[1] * 0.8, 2.6, 2.6)[0] & ~sp.m_ell(ex + look[0] * 0.8, ey + look[1] * 0.8, 2.0, 2.0)[0]
    sp.fill(rr, (90, 150, 200))
    sp.fill(sp.m_ell(ex + look[0] * 1.0, ey + look[1] * 1.0, 1.1 + 0.3 * E['eo'], 1.1 + 0.3 * E['eo'])[0], (8, 8, 12))
    sp.glint(ex + 1.2 + look[0] * 0.6, ey + 1.3 + look[1] * 0.6, 0.55)
    lid = 1.0 if blink else E.get('lid', 0.0)
    if lid > 0.05:
        cut = sp.m_ell(ex, ey, 4.1, 4.1)[0] & (DX.YC > ey + 4.0 - lid * 6.4)
        sp.fill(cut, DEV_L)
        thin(sp, (ex - 3.6, ey + 4.0 - lid * 6.4), (ex + 3.6, ey + 4.0 - lid * 6.4), (12, 12, 14), 0.3)
    # tiny «KNOCKR» plate
    sp.txt_box(['KNOCKR'], (-4.2, 13.6, 4.2, 15.6), (150, 156, 170), pad=0.05)
    # the button + LED ring (her «mouth»): pulses while she talks
    bx, by = 0.0, 7.0
    puls = 0.45 + 0.55 * min(1.0, talk * (0.8 + 0.4 * math.sin(t * 40))) if talk > 0.05 else 0.35
    if ring: puls = max(puls, ring)
    rcol = mix(DEV_L, LED, puls) if not dnd else mix(DEV_L, (120, 140, 255), 0.6)
    ringm = sp.m_ell(bx, by, 3.6, 3.6)[0] & ~sp.m_ell(bx, by, 2.6, 2.6)[0]
    sp.fill(ringm, rcol, keep=True)
    sp.ell(bx, by, 2.5, 2.5, tones((58, 60, 70)), gloss=0.6)
    if dnd:                                                                                   # crescent moon
        moon = sp.m_ell(bx, by, 1.6, 1.6)[0] & ~sp.m_ell(bx + 0.9, by + 0.6, 1.4, 1.4)[0]
        sp.fill(moon, (150, 170, 255), keep=True)
    sp.anchors.update(head=(0.0, 20.0), mouth=(bx, by), eyes=(ex, ey), btn=(bx, by))
    sp.no_outline = False


# ================================================================================ TRENT
def trent(sp, t=0.0, expr='sales', mouth_=0.0, look=(0.6, 0.0), blink=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None, walk=None):
    E = X(expr)
    if blink is None: blink = ((t + 1.9) % 4.6) < 0.12
    br = 0.3 * math.sin(t * 2.2)
    bob = abs(math.sin(walk)) * 1.0 if walk is not None else 0.0
    def Q(x, y): return (x, y + (bob if y > 10 else 0.3 * bob))
    sw = math.sin(walk) * 3.0 if walk is not None else 0.0
    shF = Q(-9.0, 50.0 + br * 0.3)
    hf = hand_f if hand_f is not None else Q(-12.0, 31.0)
    kF, eF = ik(shF, hf, 8.6, 8.0, -1.0)
    sp.cap(shF, kF, 3.0, 2.6, tones(dark(POLO_W, 0.84)))
    sp.cap(kF, eF, 2.2, 1.9, tones(dark(SKIN_T, 0.86)))
    sp.ell(eF[0], eF[1] - 0.3, 2.2, 2.1, tones(dark(SKIN_T, 0.86)))
    if prop_f: prop_f(sp, eF)
    for k_, dx in enumerate((-3.4, 3.4)):                                                                  # dark jeans, white sneakers
        near = k_ == 1
        s_ = sw if near else -sw
        fx_ = dx + s_
        sp.cap(Q(dx * 0.9, 24.0), (fx_, 3.6), 3.4, 2.8, tones((60, 76, 120) if near else (46, 58, 96)))
        sp.sup(fx_ + 1.6, 1.4, 4.0, 1.6, tones((250, 250, 250) if near else (220, 220, 220)), n=2.4, stripes=False)
    torso = sp.sup(*Q(0.0, 38.0), 10.6, 14.0, tones(POLO_W), n=2.8)
    vest = sp.sup(*Q(0.0, 38.4), 11.2, 13.6, tones(VEST), n=2.6)                                           # puffer vest
    for q in range(4): thin(sp, Q(-10.6, 30.0 + q * 5.0), Q(10.6, 30.0 + q * 5.0), dark(VEST, 0.72), 0.3, mask=vest)
    zip_ = sp.m_poly([Q(-2.6, 52.0), Q(2.6, 52.0), Q(0.6, 25.0), Q(-0.6, 25.0)])
    sp.paint(zip_, tones(POLO_W), None)
    thin(sp, Q(0.0, 52.0), Q(0.0, 25.0), (170, 170, 170), 0.22)
    thin(sp, Q(-3.0, 52.6), Q(-1.6, 40.0), (40, 140, 60), 0.35); thin(sp, Q(3.0, 52.6), Q(1.6, 40.0), (40, 140, 60), 0.35)
    sp.sup(*Q(-1.0, 37.0), 3.0, 3.6, tones((250, 250, 244)), n=5.0, stripes=False)
    sp.txt_box(['SUNNY', 'SIDE'], (Q(-3.6, 34.4)[0], Q(-3.6, 34.4)[1], Q(1.6, 39.6)[0], Q(1.6, 39.6)[1]), (230, 140, 20), pad=0.05)
    sp.cap(Q(0.8, 52.0), Q(1.2, 56.0), 2.4, 2.4, tones(dark(SKIN_T, 0.9)))
    hx, hy = Q(1.6, 64.0)
    head = sp.union([sp.m_super(hx, hy, 7.0, 7.8, 2.6), sp.m_ell(hx + 0.6, hy - 5.0, 6.4, 3.6)], tones(SKIN_T))     # square jaw
    sp.ell(hx - 6.0, hy + 0.4, 1.4, 2.0, tones(dark(SKIN_T, 0.92)))
    sp.union([sp.m_ell(hx, hy + 7.0, 7.2, 3.0), sp.m_ell(hx + 4.6, hy + 9.4, 4.6, 2.6)], tones(HAIR_T), gloss=0.9)  # gelled quiff
    for gx in (hx + 3.6, hx - 1.0):                                                                          # sunglasses on the head
        sp.sup(gx, hy + 9.0, 2.0, 1.1, tones((20, 20, 24)), n=3.0, gloss=0.8)
    lx, ly = look
    DX.eye(sp, hx + 3.4, hy + 1.4, 3.2, 3.2, E, (60, 110, 60), (lx, ly), blink, lash=INK, skin=SKIN_T, bold=1)
    DX.eye(sp, hx - 1.2, hy + 1.4, 2.8, 3.0, E, (60, 110, 60), (lx, ly), blink, lash=INK, skin=SKIN_T, bold=1)
    DX.brow(sp, hx + 3.4, hy + 4.4, 3.4, E, +1, HAIR_T, th=1.2)
    DX.brow(sp, hx - 1.2, hy + 4.3, 3.0, E, -1, HAIR_T, th=1.2)
    sp.ell(hx + 6.6, hy - 1.0, 1.6, 1.8, tones(dark(SKIN_T, 0.98)), gloss=1.0)
    mx, my = hx + 3.0, hy - 4.0
    DX.mouth(sp, mx, my, 5.6, E, max(mouth_, 0.35), (150, 70, 60), inside=(96, 26, 36), teeth=(255, 255, 255), skin=SKIN_T, maxh=4.4)
    if (int(t * 3) % 4) == 0: sp.glint(mx + 1.6, my + 0.4, 0.5)                                                # tooth «ting»
    sp.anchors.update(head=(hx, hy), mouth=(mx, my), eyes=(hx + 1.0, hy + 1.4))
    before = sp.m.copy()
    shN = Q(9.4, 50.0 + br * 0.3)
    hn = hand_n if hand_n is not None else Q(12.0, 34.0)
    kN, eN = ik(shN, hn, 8.6, 8.0, -1.0)
    sp.cap(shN, kN, 3.2, 2.8, tones(POLO_W))
    sp.cap(kN, eN, 2.2, 1.9, tones(SKIN_T))
    sp.ell(eN[0], eN[1] - 0.3, 2.3, 2.2, tones(SKIN_T))
    if prop_n: prop_n(sp, eN)
    sp.anchors['hand'] = eN
    new = sp.m & ~before
    o = dilate(new) & ~sp.m & before
    sp.col[o] = INK


# ================================================================================ PARCELZ courier (sprinting, tiny on camera)
def courier(sp, t=0.0, run=0.0, arm_up=False, look=(0.8, 0.0)):
    E = X('stare')
    sw = math.sin(run) * 6.0
    for k_, dx in enumerate((-2.0, 2.0)):
        s_ = sw if k_ else -sw
        sp.cap((dx * 0.8, 26.0), (dx + s_, 3.0 + max(0, s_) * 0.6), 3.0, 2.4, tones(BROWN if k_ else dark(BROWN, 0.85)))
        sp.cap((dx + s_, 3.0 + max(0, s_) * 0.6), (dx + s_, 1.0), 1.4, 1.4, tones(SKIN))
        sp.sup(dx + s_ + 1.4, 0.8, 3.2, 1.2, tones((40, 40, 40)), n=2.4)
    sp.sup(1.0, 38.0, 8.6, 12.0, tones(TEAL), n=2.6)
    sp.txt_box(['PARCELZ'], (-6.0, 36.0, 8.0, 40.0), (250, 250, 240), pad=0.05)
    sp.cap((1.2, 50.0), (1.4, 53.0), 2.0, 2.0, tones(SKIN))
    sp.ell(2.4, 59.0, 6.0, 6.4, tones(SKIN))
    sp.union([sp.m_ell(2.0, 63.0, 6.4, 3.0), sp.m_super(7.0, 61.4, 3.6, 0.9, 4.0)], tones(TEAL))
    DX.eye(sp, 5.4, 59.4, 2.6, 2.6, E, (60, 50, 40), look, False, lash=INK, skin=SKIN, bold=1)
    DX.mouth(sp, 5.2, 55.0, 3.0, E, 0.2, (150, 70, 60), inside=(96, 26, 36), teeth=(255, 255, 255), skin=SKIN, maxh=2.0)
    hn = (12.0, 56.0) if arm_up else (10.0 - sw * 0.4, 34.0)
    kN, eN = ik((8.0, 46.0), hn, 7.0, 7.0, -1.0)
    sp.cap((8.0, 46.0), kN, 2.6, 2.2, tones(TEAL)); sp.cap(kN, eN, 1.9, 1.7, tones(SKIN))
    sp.ell(eN[0], eN[1], 2.0, 2.0, tones(SKIN))
    sp.anchors.update(head=(2.4, 59.0), hand=eN)


def chair(sp, t=0.0):
    """a plain wooden kitchen chair in profile (seat faces right)"""
    W_ = (150, 100, 60)
    for x in (-6.0, 6.0): sp.cap((x, 0.0), (x, 16.0), 1.0, 1.0, tones(dark(W_, 0.85)))
    sp.sup(0.0, 17.0, 8.0, 1.4, tones(W_), n=4.0)
    sp.cap((-7.0, 17.0), (-7.4, 38.0), 1.2, 1.2, tones(W_))
    for q in range(3): sp.cap((-7.2, 24.0 + q * 5.0), (-6.8, 24.0 + q * 5.0), 1.0, 1.0, tones(dark(W_, 0.9)))
