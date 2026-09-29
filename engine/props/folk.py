"""Cast of «Валера и кот»: Valera (retired warrant officer), the cat Dembel, grannies Zina & Lyuba, cashier Tamara,
housing-office clerk Nina Petrovna. Drawn with scene.py-style primitives on a stage.Chars canvas.
Convention: anchor (1000,1000) = floor point under the character, H(x, h) -> (1000 + x, 1000 - h), +x = facing direction
(ACam.flip mirrors). Shading: 3 tones from a top-left light (hi / base / sh), heroes get scene light later (stage.Light)."""
import math
import numpy as np
import scene as S
from scene import Layer, win

OL = (30, 20, 18)
LIGHT = (-0.55, -0.83)            # light direction in screen space (from top-left)


def H(x, h):
    return (1000.0 + x, 1000.0 - h)


def _tone(L, w, m, nx, ny, base, hi, sh, th_hi=0.42, th_sh=-0.30):
    L.set(w, m, base)
    if hi is None and sh is None: return
    flip = -1.0 if getattr(L.cam, 'flip', False) else 1.0
    d = nx * LIGHT[0] * flip + ny * LIGHT[1]
    if hi is not None: L.set(w, m & (d > th_hi), hi)
    if sh is not None: L.set(w, m & (d < th_sh), sh)


def cap(L, a, b, r0, r1, c, hi=None, sh=None):
    """capsule with directional 3-tone shading"""
    cm = L.cam
    ax, ay = cm.p(*a); bx, by = cm.p(*b); r0 *= cm.sc; r1 *= cm.sc
    R = max(r0, r1) + 1
    w = win(min(ax, bx) - R, max(ax, bx) + R, min(ay, by) - R, max(ay, by) + R)
    if w is None: return
    X = S.XX[w]; Y = S.YY[w]
    dx, dy = bx - ax, by - ay; l2 = dx * dx + dy * dy + 1e-6
    t = np.clip(((X - ax) * dx + (Y - ay) * dy) / l2, 0, 1)
    ex = X - (ax + t * dx); ey = Y - (ay + t * dy)
    r = r0 + (r1 - r0) * t
    m = ex * ex + ey * ey <= r * r
    rr = np.maximum(r, 0.6)
    _tone(L, w, m, ex / rr, ey / rr, c, hi, sh)


def ell(L, cxy, rx, ry, c, ang=0.0, hi=None, sh=None, th_hi=0.42, th_sh=-0.30):
    cm = L.cam
    if getattr(cm, 'flip', False): ang = -ang
    cx, cy = cm.p(*cxy); rx *= cm.sc; ry *= cm.sc
    R = max(rx, ry) + 1
    w = win(cx - R, cx + R, cy - R, cy + R)
    if w is None: return
    X = S.XX[w] - cx; Y = S.YY[w] - cy
    ca, sa = math.cos(ang), math.sin(ang)
    u = X * ca + Y * sa; v = -X * sa + Y * ca
    m = (u / rx) ** 2 + (v / ry) ** 2 <= 1
    nx = (u / rx) * ca - (v / ry) * sa; ny = (u / rx) * sa + (v / ry) * ca
    _tone(L, w, m, nx, ny, c, hi, sh, th_hi, th_sh)


def ellt(L, cxy, rx, ry, tones, ang=0.0):
    """ellipse with a (base, hi, sh) tone triple"""
    ell(L, cxy, rx, ry, tones[0], ang, tones[1], tones[2])


def dot(L, xy, c, r=0.5):
    S.dot(L, xy, c, r)


def poly(L, pts, c):
    """filled polygon in unit coords"""
    from PIL import Image, ImageDraw
    cm = L.cam
    sp = [cm.p(*p) for p in pts]
    xs = [p[0] for p in sp]; ys = [p[1] for p in sp]
    w = win(min(xs) - 1, max(xs) + 1, min(ys) - 1, max(ys) + 1)
    if w is None: return
    y0, x0 = w[0].start, w[1].start
    hh, ww = w[0].stop - y0, w[1].stop - x0
    img = Image.new('L', (ww, hh), 0)
    ImageDraw.Draw(img).polygon([(x - x0, y - y0) for x, y in sp], fill=1)
    L.set(w, np.array(img).astype(bool), c)


def recolor(L, mask, pairs):
    """map exact colours inside mask: pairs = [(src, dst), ...]"""
    col = L.col
    for src, dst in pairs:
        m = mask & L.m & (col[..., 0] == src[0]) & (col[..., 1] == src[1]) & (col[..., 2] == src[2])
        col[m] = dst


def band_mask(L, cxy, period, bow=0.0, width=1.0, ang=0.0):
    """screen mask of alternate stripes (period in units) across a part centred at cxy; bow bends stripes"""
    cm = L.cam
    cx, cy = cm.p(*cxy); p = max(2.0, period * cm.sc)
    X = S.XX - cx; Y = S.YY - cy
    ca, sa = math.cos(ang), math.sin(ang)
    v = -X * sa + Y * ca; u = X * ca + Y * sa
    v = v - bow * (u / max(1.0, width * cm.sc)) ** 2 * p
    return (np.floor(v / p).astype(np.int64) % 2) == 1


def outline(L, c=OL):
    S.outline(L, c)


# ======================================================================================= VALERA
VC = dict(skin=(238, 186, 150), skin_hi=(252, 212, 180), skin_sh=(204, 146, 116), nose=(214, 98, 92), nose_hi=(240, 140, 128),
          cheek=(230, 142, 126), hair=(92, 86, 84), hair_hi=(128, 122, 118), must=(86, 66, 52), must_hi=(122, 96, 76),
          brow=(70, 54, 44), eye=(26, 20, 18), white=(244, 244, 240),
          tel_w=(238, 240, 246), tel_w_hi=(252, 252, 255), tel_w_sh=(196, 204, 222),
          tel_b=(44, 74, 160), tel_b_hi=(66, 100, 190), tel_b_sh=(30, 50, 118),
          pants=(58, 66, 104), pants_hi=(78, 88, 132), pants_sh=(42, 48, 78), lamp=(222, 226, 236),
          slip=(128, 86, 58), slip_hi=(156, 110, 76), slip_sh=(96, 62, 42),
          towel=(236, 214, 120), towel_hi=(250, 234, 160), towel_sh=(206, 176, 84), towel_st=(206, 92, 70),
          ushanka=(98, 92, 88), ushanka_hi=(130, 124, 118), ushanka_sh=(70, 66, 64),
          camo=(96, 112, 70), camo_hi=(118, 136, 88), camo_sh=(70, 84, 52), camo_a=(70, 62, 44), camo_b=(132, 128, 86),
          boot=(40, 36, 34), boot_hi=(66, 60, 56), sheet=(236, 238, 242), sheet_hi=(252, 252, 255), sheet_sh=(196, 204, 218))

VPOSE = dict(
    # arms as IK hand targets (x, h) in body units (+x = facing); bn/bf = elbow bend side (+1 back/down, -1 forward/out)
    stand=dict(n=(3.9, 10.4), f=(-3.1, 10.6), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
    hips=dict(n=(2.9, 10.9), f=(-2.9, 10.9), bn=-1, bf=1, nleg=(0.18, 0.0), fleg=(-0.18, 0.0)),
    proud=dict(n=(2.3, 16.6), f=(-3.0, 10.8), bn=1, bf=-1, nleg=(0.18, 0.0), fleg=(-0.18, 0.0)),        # thumb to chest
    point=dict(n=(10.2, 17.6), f=(-3.0, 10.8), bn=1, bf=-1, nleg=(0.12, 0.0), fleg=(-0.12, 0.0)),
    salute=dict(n=(0.2, 23.3), f=(-3.0, 10.8), bn=-1, bf=-1, nleg=(0.0, 0.0), fleg=(0.0, 0.0)),
    shout=dict(n=(6.0, 25.4), f=(-5.0, 25.0), bn=1, bf=-1, nleg=(0.25, 0.0), fleg=(-0.25, 0.0)),
    shiver=dict(n=(-0.2, 14.4), f=(2.3, 14.0), bn=1, bf=-1, nleg=(0.04, 0.0), fleg=(-0.04, 0.0)),        # hugging himself
    hold=dict(n=(6.4, 14.0), f=(5.6, 14.2), bn=1, bf=1, nleg=(0.08, 0.0), fleg=(-0.08, 0.0)),
    overhead=dict(n=(5.4, 27.0), f=(-3.4, 27.0), bn=1, bf=-1, nleg=(0.1, 0.0), fleg=(-0.1, 0.0)),
    phone=dict(n=(2.2, 20.6), f=(-3.0, 10.8), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
    strain=dict(n=(7.8, 15.0), f=(6.9, 15.4), bn=1, bf=1, nleg=(0.45, 0.0), fleg=(-0.45, 0.0)),
    fist=dict(n=(5.6, 25.2), f=(-3.0, 10.8), bn=1, bf=-1, nleg=(0.15, 0.0), fleg=(-0.15, 0.0)),
    shrug=dict(n=(5.6, 17.0), f=(-4.8, 17.0), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
    sit=dict(n=(4.6, 11.0), f=(3.6, 11.4), bn=1, bf=1, nleg=(1.55, 0.0), fleg=(1.45, 0.0)),
)


def vwalk(t, speed=7.0, amp=0.35):
    s = math.sin(t * speed)
    return dict(n=(3.9 - 2.2 * s, 10.6 + 0.4 * abs(s)), f=(-3.1 + 2.2 * s, 10.7), bn=1, bf=-1,
                nleg=(amp * s, 0.25 * max(0, -s)), fleg=(-amp * s, 0.25 * max(0, s)))


def vblend(a, b, k):
    o = dict(a if k < 0.5 else b)
    for kk in ('n', 'f', 'nleg', 'fleg'):
        o[kk] = (a[kk][0] + (b[kk][0] - a[kk][0]) * k, a[kk][1] + (b[kk][1] - a[kk][1]) * k)
    return o


def _D(th):
    """limb direction for angle th (0 = straight down, +pi/2 = forward)"""
    return (math.sin(th), math.cos(th))


def _limb(L, o, th1, th2, l1, l2, r1, r2, col, hi, sh, target=None, bend=1.0):
    """two-segment limb from o by angles (th1, th2) or, if target is given, by 2-bone IK towards target"""
    if target is not None:
        dx, dy = target[0] - o[0], target[1] - o[1]
        d = max(1e-3, min(math.hypot(dx, dy), l1 + l2 - 1e-3))
        a = math.atan2(dy, dx)
        c1 = max(-1.0, min(1.0, (l1 * l1 + d * d - l2 * l2) / (2 * l1 * d)))
        a1 = a + bend * math.acos(c1)
        k = (o[0] + math.cos(a1) * l1, o[1] + math.sin(a1) * l1)
        e = (o[0] + math.cos(a) * d, o[1] + math.sin(a) * d)
    else:
        d1 = _D(th1); k = (o[0] + d1[0] * l1, o[1] + d1[1] * l1)
        d2 = _D(th2); e = (k[0] + d2[0] * l2, k[1] + d2[1] * l2)
    cap(L, o, k, r1, r1 * 0.92, col, hi, sh)
    cap(L, k, e, r1 * 0.92, r2, col, hi, sh)
    return k, e


def _merge(L, A, ol=OL):
    """outline part layer A and paint it over L"""
    if ol is not None: outline(A, ol)
    L.col[A.m] = A.col[A.m]; L.m |= A.m


def _valera_head(Hd, F, P, expr, t, mouth, look, cold, wet, hat, outfit, blink, cam):
    """3/4 head facing +x: egg skull, bald shiny top, thin horseshoe fringe + comb-over, bushy brows, red bulb nose,
    walrus moustache, jowls. F(x, h) maps head-local coords (x ~ -3..5, h ~ 17.5..24.8) to unit coords."""
    stub = tuple(int(c * 0.92) for c in P['skin_sh'])
    cap(Hd, F(0.5, 17.6), F(0.7, 19.4), 1.9, 1.9, P['skin'], P['skin_hi'], P['skin_sh'])            # neck
    ell(Hd, F(1.5, 18.95), 2.7, 1.35, P['skin'], 0, None, P['skin_sh'])                             # jowls / double chin
    ell(Hd, F(0.75, 21.35), 3.15, 3.45, P['skin'], -0.08, P['skin_hi'], P['skin_sh'])              # skull
    ell(Hd, F(2.0, 19.35), 2.1, 0.95, stub, 0.1)                                                    # stubble jaw
    ell(Hd, F(-1.05, 21.0), 0.72, 1.02, P['skin'], 0, None, P['skin_sh'])                           # ear
    ell(Hd, F(-0.98, 21.0), 0.34, 0.58, P['skin_sh'])
    ell(Hd, F(0.6, 24.05), 1.1, 0.42, P['skin_hi'], -0.15)                                          # bald shine
    bald = hat is None and outfit not in ('street', 'sheet')
    if bald:
        for pts in (((-0.4, 22.9), (-1.6, 22.5), (-2.2, 21.6), (-2.25, 20.4)),):                    # horseshoe fringe
            for i in range(len(pts) - 1):
                cap(Hd, F(*pts[i]), F(*pts[i + 1]), 0.5, 0.45, P['hair'], P['hair_hi'], None)
        for k2 in range(3):                                                                         # comb-over strands
            y0 = 23.55 + k2 * 0.28
            cap(Hd, F(-1.6 + k2 * 0.2, y0 - 0.2), F(0.2 + k2 * 0.3, y0 + 0.55), 0.13, 0.13, P['hair'])
            cap(Hd, F(0.2 + k2 * 0.3, y0 + 0.55), F(2.0 + k2 * 0.1, y0 + 0.2 - k2 * 0.1), 0.13, 0.12, P['hair'])
        if wet > 0:
            for k2 in range(3):
                x0 = 0.6 + k2 * 0.55
                cap(Hd, F(x0, 24.3 - k2 * 0.1), F(x0 + 0.25, 22.9 - k2 * 0.35), 0.13, 0.1, P['hair'])
    # eyes (near eye bigger), baggy lids
    ex = 0.12 * look
    eyes = [(F(1.45 + ex, 21.95), 0.36), (F(2.75 + ex, 21.85), 0.45)]
    bl = blink and (t % 3.7) < 0.12
    for e_, r in eyes:
        ell(Hd, (e_[0] - 0.05, e_[1] + r * 1.05), r * 1.1, r * 0.45, P['skin_sh'])                   # eye bag
    if expr == 'blissful' or bl:
        for e_, r in eyes: cap(Hd, (e_[0] - r, e_[1] + 0.05), (e_[0] + r, e_[1] - 0.02), 0.13, 0.13, P['eye'])
    elif expr in ('squint', 'sly', 'whisper'):
        for e_, r in eyes:
            ell(Hd, e_, r * 1.1, r * 0.5, P['white']); dot(Hd, (e_[0] + 0.1 + ex, e_[1] + 0.02), P['eye'], r * 0.45)
            cap(Hd, (e_[0] - r * 1.1, e_[1] - r * 0.45), (e_[0] + r * 1.1, e_[1] - r * 0.5), 0.12, 0.12, P['skin_sh'])
    else:
        big = expr in ('shout', 'shock')
        for e_, r in eyes:
            rr = r * (1.25 if big else 1.0)
            ell(Hd, e_, rr, rr * 1.08, P['white'])
            dot(Hd, (e_[0] + 0.08 + ex, e_[1] + 0.03), P['eye'], rr * (0.42 if big else 0.52))
            dot(Hd, (e_[0] + 0.02 + ex, e_[1] - 0.1), (255, 255, 255), rr * 0.16)
            if not big:
                cap(Hd, (e_[0] - rr, e_[1] - rr * 0.55), (e_[0] + rr, e_[1] - rr * 0.65), 0.14, 0.14, P['skin_sh'])
    bt = {'angry': 0.55, 'shout': -0.2, 'shock': -0.5, 'proud': -0.2, 'smug': 0.25, 'sly': 0.4, 'sad': -0.55,
          'whisper': 0.35, 'blissful': -0.25, 'squint': 0.3}.get(expr, 0.0)
    lift = 0.35 if expr in ('shock', 'shout') else 0.0
    for k2, (e_, r) in enumerate(eyes):
        base = e_[1] - r - 0.62 - lift
        s_ = 1 if k2 == 0 else -1
        cap(Hd, (e_[0] - 0.62, base - s_ * bt * 0.32), (e_[0] + 0.62, base + s_ * bt * 0.32), 0.34, 0.28, P['brow'])
    # nose, cheek
    ell(Hd, F(2.0, 20.55), 0.75, 0.45, P['cheek'])
    ell(Hd, F(3.6, 20.95), 0.98, 0.88, P['nose'], 0, P['nose_hi'], None)
    dot(Hd, F(3.35, 21.3), (255, 214, 200), 0.14)
    # mouth under the moustache
    m = max(mouth, {'shout': 0.8, 'shock': 0.6}.get(expr, 0.0))
    mc = F(3.0, 19.3)
    if m > 0.08:
        ell(Hd, mc, 0.75 + 0.35 * m, 0.25 + 0.8 * m, (96, 30, 30))
        ell(Hd, (mc[0] + 0.1, mc[1] + 0.35 * m), 0.45 + 0.25 * m, 0.18 + 0.22 * m, (196, 96, 96))
    elif expr in ('smug', 'proud', 'blissful'):
        cap(Hd, F(2.35, 19.3), F(3.7, 19.55), 0.13, 0.13, (110, 50, 40))
    elif expr in ('sad', 'angry'):
        cap(Hd, F(2.35, 19.5), F(3.7, 19.25), 0.13, 0.13, (110, 50, 40))
    # walrus moustache
    my = 20.05 + 0.35 * m
    ell(Hd, F(2.35, my), 1.3, 0.6, P['must'], 0.12, P['must_hi'], None)
    ell(Hd, F(3.65, my + 0.02), 1.15, 0.6, P['must'], -0.1, P['must_hi'], None)
    cap(Hd, F(1.25, my - 0.1), F(1.05, my - 1.2), 0.42, 0.22, P['must'])
    cap(Hd, F(4.65, my - 0.05), F(4.8, my - 1.1), 0.4, 0.2, P['must'])
    if cold > 0.5:                                                                                  # icicles
        for k2 in range(5):
            cap(Hd, F(1.6 + k2 * 0.65, my - 0.4), F(1.6 + k2 * 0.65, my - 1.0 - (k2 % 2) * 0.45), 0.15, 0.04, (220, 240, 255))
    if outfit == 'street' or hat == 'ushanka':
        ell(Hd, F(0.7, 24.0), 3.7, 1.9, P['ushanka'], 0, P['ushanka_hi'], P['ushanka_sh'])
        cap(Hd, F(-2.8, 23.1), F(4.2, 23.1), 0.9, 0.9, P['ushanka_hi'], None, P['ushanka'])
        cap(Hd, F(-2.0, 22.5), F(-2.2, 19.8), 1.0, 0.8, P['ushanka'], P['ushanka_hi'], P['ushanka_sh'])
        dot(Hd, F(1.1, 23.2), (190, 160, 70), 0.35)


def valera(CH, cam, pose=None, t=0.0, mouth=0.0, expr='normal', outfit='home', look=0.0, tint=None, belly_wob=0.0,
           breath=True, cold=0.0, wet=0.0, blink=True, hat=None, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
           lean=0.0):
    """expr: normal | shout | angry | proud | smug | sly | blissful | shock | whisper | sad | squint
    outfit: home (telnyashka) | towel (bare torso + towel) | street (ushanka + camo) | sheet (bedsheet) | robe
    tint: (r,g,b) multiplier (rusty after the radiator water); cold 0..1 bluish skin + icicles; look: eye shift.
    hand_n / hand_f: IK targets (unit coords, e.g. H(x, h)); prop_n / prop_f: callables(L, hand_point) drawn in the hand.
    lean: forward lean of the upper body (units shift of head/shoulders)."""
    pose = pose or VPOSE['stand']
    br = 0.18 * math.sin(t * 2.2) if breath else 0.0
    wob = belly_wob
    P = VC.copy()
    if cold > 0:
        tgt = {'skin': (150, 196, 255), 'skin_hi': (196, 226, 255), 'skin_sh': (104, 150, 226), 'nose': (86, 120, 232),
               'cheek': (120, 170, 250)}
        for k2, v2 in tgt.items(): P[k2] = tuple(int(a + (b - a) * cold) for a, b in zip(P[k2], v2))
    if tint is not None:
        for k2 in list(P):
            if k2 in ('eye', 'white'): continue
            P[k2] = tuple(int(min(255, c * m)) for c, m in zip(P[k2], tint))
    top = {'home': ('tel_w', 'tel_w_hi', 'tel_w_sh'), 'towel': ('skin', 'skin_hi', 'skin_sh'),
           'street': ('camo', 'camo_hi', 'camo_sh'), 'sheet': ('sheet', 'sheet_hi', 'sheet_sh'), 'robe': None}[outfit]
    tc = [P[k2] for k2 in top] if top else [(150, 60, 56), (178, 80, 72), (118, 44, 42)]
    legc = [P['pants'], P['pants_hi'], P['pants_sh']] if outfit not in ('towel', 'robe') else [P['skin'], P['skin_hi'], P['skin_sh']]
    footc = (P['boot'], P['boot_hi'], P['boot']) if outfit == 'street' else (P['slip'], P['slip_hi'], P['slip_sh'])
    ln = lean
    sh_n, sh_f = H(3.2 + ln, 17.4 + br), H(-3.0 + ln, 17.6 + br)
    hp_n, hp_f = H(1.5, 8.6), H(-1.3, 8.6)
    L = Layer(cam)
    # ---------------------------------------------------------------- far arm + far leg
    A = Layer(cam)
    kf, ef = _limb(A, hp_f, *VPOSE['stand']['fleg'] if pose.get('fleg') is None else pose['fleg'], 4.2, 4.1, 1.75, 1.35, *legc)
    ellt(A, (ef[0] + 0.9, ef[1] + 0.35), 1.9, 0.85, footc)
    _merge(L, A)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(pose['f'][0], pose['f'][1])
    ka, ea = _limb(A, sh_f, 0, 0, 3.9, 3.6, 1.45, 1.15, *tc, target=tf, bend=pose.get('bf', -1))
    ell(A, ea, 1.2, 1.12, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_f: prop_f(A, ea)
    _merge(L, A)
    # ---------------------------------------------------------------- pelvis + near leg
    A = Layer(cam)
    ellt(A, H(0.2, 9.4), 3.7, 2.4, legc)
    kn, en = _limb(A, hp_n, *pose['nleg'], 4.2, 4.1, 1.85, 1.4, *legc)
    ellt(A, (en[0] + 0.9, en[1] + 0.35), 2.0, 0.9, footc)
    if outfit in ('home', 'street'):
        d1 = _D(pose['nleg'][0]); d2 = _D(pose['nleg'][1])
        o = hp_n; k = (o[0] + d1[0] * 4.2, o[1] + d1[1] * 4.2); e = (k[0] + d2[0] * 3.9, k[1] + d2[1] * 3.9)
        for off in (-0.6, -0.2):
            cap(A, (o[0] + off, o[1] + 0.5), (k[0] + off, k[1]), 0.15, 0.15, P['lamp'])
            cap(A, (k[0] + off, k[1]), (e[0] + off, e[1] - 0.4), 0.15, 0.15, P['lamp'])
    if outfit == 'robe':
        ellt(A, H(0.9, 9.6), 5.0, 3.6, tc)
    _merge(L, A)
    # ---------------------------------------------------------------- torso
    bc = H(1.1 + wob * 0.3 + ln * 0.3, 12.6 + br * 0.5)
    T = Layer(cam)
    ellt(T, bc, 5.3 + wob * 0.2, 5.4, tc)
    ellt(T, H(0.1 + ln, 16.6 + br), 4.4, 3.0, tc)
    if outfit == 'home':
        stripe = band_mask(T, bc, 0.95, bow=0.35, width=5.0)
        recolor(T, stripe, [(P['tel_w'], P['tel_b']), (P['tel_w_hi'], P['tel_b_hi']), (P['tel_w_sh'], P['tel_b_sh'])])
        ell(T, H(1.9 + wob * 0.3, 8.3), 3.9, 1.3, P['skin'], 0, P['skin_hi'], P['skin_sh'])      # belly peeks out
        dot(T, H(2.3 + wob * 0.3, 8.4), P['skin_sh'], 0.28)
    elif outfit == 'towel':
        for k2 in range(5):
            a = k2 * 1.1
            x0, y0 = 0.9 + ln + 1.3 * math.sin(a * 1.7), 15.7 + 0.8 * math.cos(a * 2.3)
            cap(T, H(x0, y0), H(x0 + 0.25, y0 - 0.35), 0.09, 0.07, P['hair'])
        dot(T, H(2.3, 11.4), P['skin_sh'], 0.3)
        ell(T, H(0.9, 8.4), 4.9, 2.3, P['towel'], 0, P['towel_hi'], P['towel_sh'])
        for yy in (7.9, 9.1):
            cap(T, H(-3.7, yy), H(5.5, yy), 0.2, 0.2, P['towel_st'])
        cap(T, H(3.7, 9.0), H(4.3, 6.0), 0.9, 1.3, P['towel'], P['towel_hi'], P['towel_sh'])
    elif outfit == 'street':
        cm1 = band_mask(T, bc, 2.2, bow=0.1, width=5.0, ang=0.6)
        cm2 = band_mask(T, bc, 3.1, bow=-0.3, width=5.0, ang=-0.4)
        recolor(T, cm1 & ~cm2, [(P['camo'], P['camo_a']), (P['camo_hi'], P['camo_b']), (P['camo_sh'], P['camo_a'])])
        recolor(T, cm2 & ~cm1, [(P['camo'], P['camo_b'])])
        cap(T, H(1.3 + ln, 18.5), H(1.5, 7.4), 0.22, 0.22, (60, 70, 44))
    elif outfit == 'robe':
        cap(T, H(-0.8 + ln, 18.2), H(2.8, 11.0), 0.8, 0.8, (236, 214, 120))
        cap(T, H(-4.0, 11.6), H(6.0, 11.6), 0.5, 0.5, (236, 214, 120))
    _merge(L, T)
    # ---------------------------------------------------------------- head
    Hd = Layer(cam)
    hx = 0.9 + ln * 1.2
    hc = H(hx, 21.2 + br)
    def F(x, h): return H(hx + x - 0.9, h + br)
    _valera_head(Hd, F, P, expr, t, mouth, look, cold, wet, hat, outfit, blink, cam)
    _merge(L, Hd)
    mc = F(3.0, 19.3)
    if outfit == 'street':                                                         # jacket collar over the neck
        Cl = Layer(cam)
        ell(Cl, H(0.8 + ln, 17.9 + br), 2.9, 0.8, P['camo_sh'])
        _merge(L, Cl)
    # ---------------------------------------------------------------- near arm (front)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(pose['n'][0], pose['n'][1])
    kna, ena = _limb(A, sh_n, 0, 0, 3.9, 3.6, 1.5, 1.2, *tc, target=tn, bend=pose.get('bn', 1))
    if outfit == 'home':
        s1 = band_mask(A, sh_n, 0.9, ang=math.atan2(kna[0] - sh_n[0], kna[1] - sh_n[1]) * -1)
        recolor(A, s1, [(P['tel_w'], P['tel_b']), (P['tel_w_hi'], P['tel_b_hi']), (P['tel_w_sh'], P['tel_b_sh'])])
    ell(A, ena, 1.25, 1.18, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_n: prop_n(A, ena)
    _merge(L, A)
    if outfit == 'sheet':
        Sh = Layer(cam)
        ell(Sh, H(0.8, 13.0), 6.3, 9.8, P['sheet'], 0, P['sheet_hi'], P['sheet_sh'])
        ell(Sh, H(0.4 + ln, 22.6), 3.9, 3.1, P['sheet'], 0, P['sheet_hi'], P['sheet_sh'])
        fm = Layer(cam); ell(fm, F(2.4, 21.0), 2.3, 1.9, (1, 1, 1))
        Sh.m &= ~fm.m
        _merge(L, Sh)
    outline(L, OL)
    CH.add(L)
    return dict(hand_n=ena, hand_f=ea, head=hc, mouth=mc, belly=bc, top=F(0.9, 24.6))


# ======================================================================================= CAT
KC = dict(fur=(232, 142, 60), fur_hi=(248, 178, 98), fur_sh=(196, 108, 44), stripe=(170, 84, 34),
          white=(246, 240, 228), white_sh=(214, 204, 190), pink=(236, 150, 150), nose=(214, 112, 116),
          iris=(156, 204, 86), pupil=(22, 20, 18), mouth=(92, 34, 34), whisk=(250, 246, 236), ol=(52, 28, 14))


def cat_head(L, c, r=3.5, lid=0.55, mouth=0.0, look=(0.0, 0.0), t=0.0, expr='deadpan', P=KC):
    """frontal fat-cat head centred at c (unit coords), r = half-width. lid: 0 open .. 1 closed"""
    cx, cy = c
    def Q(x, y): return (cx + x * r / 3.5, cy - y * r / 3.5)
    k = r / 3.5
    # ears (left one torn)
    for sx in (-1, 1):
        base = [Q(sx * 1.2, 2.2), Q(sx * 3.3, 1.2), Q(sx * 2.9, 4.4)]
        poly(L, base, P['fur'])
        poly(L, [Q(sx * 1.7, 2.2), Q(sx * 2.9, 1.6), Q(sx * 2.7, 3.6)], P['pink'])
    poly(L, [Q(-2.75, 4.5), Q(-2.2, 3.3), Q(-2.95, 3.6)], (0, 0, 0))                # notch (masked below)
    L.m[(L.col == 0).all(-1)] = False
    # head (wide cheeks)
    ell(L, Q(0, 0.2), 3.55 * k, 3.05 * k, P['fur'], 0, P['fur_hi'], P['fur_sh'])
    ell(L, Q(-2.6, -0.7), 1.3 * k, 1.1 * k, P['fur'], 0.3)                           # cheek fluff
    ell(L, Q(2.6, -0.7), 1.3 * k, 1.1 * k, P['fur'], -0.3)
    for x0 in (-0.9, 0.0, 0.9):                                                      # forehead stripes
        cap(L, Q(x0 * 1.1, 3.0), Q(x0 * 0.7, 1.7), 0.28 * k, 0.12 * k, P['stripe'])
    for sx in (-1, 1):
        cap(L, Q(sx * 3.3, 0.6), Q(sx * 2.4, 0.4), 0.2 * k, 0.1 * k, P['stripe'])
        cap(L, Q(sx * 3.4, -0.3), Q(sx * 2.5, -0.3), 0.2 * k, 0.1 * k, P['stripe'])
    # muzzle
    ell(L, Q(-0.75, -1.05), 1.15 * k, 0.9 * k, P['white'], 0, None, P['white_sh'])
    ell(L, Q(0.75, -1.05), 1.15 * k, 0.9 * k, P['white'], 0, None, P['white_sh'])
    ell(L, Q(0, -1.9), 0.9 * k, 0.55 * k, P['white'])
    # eyes
    for sx in (-1, 1):
        e = Q(sx * 1.35 + look[0], 0.55 + look[1])
        ell(L, e, 0.8 * k, 0.7 * k, P['iris'])
        cap(L, (e[0], e[1] - 0.45 * k), (e[0], e[1] + 0.45 * k), 0.16 * k, 0.16 * k, P['pupil'])
        dot(L, (e[0] + 0.25 * k, e[1] - 0.25 * k), (255, 255, 255), 0.12 * k)
        if lid > 0.02:                                                              # heavy upper lid
            lt = e[1] - 0.75 * k + lid * 1.3 * k
            poly(L, [(e[0] - 0.95 * k, e[1] - 0.9 * k), (e[0] + 0.95 * k, e[1] - 0.9 * k),
                     (e[0] + 0.95 * k, lt), (e[0] - 0.95 * k, lt)], P['fur_sh'])
            cap(L, (e[0] - 0.85 * k, lt), (e[0] + 0.85 * k, lt), 0.12 * k, 0.12 * k, P['ol'])
    if expr == 'smug':
        for sx in (-1, 1): cap(L, Q(sx * 0.7, 1.6), Q(sx * 2.0, 1.45), 0.15 * k, 0.15 * k, P['stripe'])
    # nose + mouth
    poly(L, [Q(-0.45, -0.45), Q(0.45, -0.45), Q(0, -0.95)], P['nose'])
    if mouth > 0.1:
        ell(L, Q(0, -1.55 - 0.25 * mouth), (0.45 + 0.2 * mouth) * k, (0.25 + 0.5 * mouth) * k, P['mouth'])
    cap(L, Q(0, -0.95), Q(0, -1.25), 0.08 * k, 0.08 * k, P['ol'])
    cap(L, Q(0, -1.25), Q(-0.55, -1.45), 0.08 * k, 0.08 * k, P['ol'])
    cap(L, Q(0, -1.25), Q(0.55, -1.45), 0.08 * k, 0.08 * k, P['ol'])
    return Q


def cat_whiskers(L, Q, k=1.0, P=KC):
    for sx in (-1, 1):
        for j, dy in enumerate((-0.9, -1.2, -1.5)):
            cap(L, Q(sx * 1.6, dy), Q(sx * 4.2, dy + 0.35 - j * 0.35), 0.05 * k, 0.05 * k, P['whisk'])


def cat(CH, cam, t=0.0, pose='loaf', mouth=0.0, lid=0.55, look=(0.0, 0.0), expr='deadpan', tail=0.0, tint=None, towel=False):
    """Dembel. pose: loaf (lying, head frontal) | sit | walk | bath (only the head + towel turban above foam)"""
    P = KC if tint is None else {k: tuple(int(min(255, c * m)) for c, m in zip(v, tint)) for k, v in KC.items()}
    L = Layer(cam)
    br = 0.12 * math.sin(t * 1.6)
    k = 1.0
    if pose == 'loaf':
        # tail curled along the front
        for i in range(7):
            a0 = -2.6 + i * 0.55; a1 = a0 + 0.55
            p0 = (1000 - 5.2 * math.cos(a0 * 0.5) + 0.3 * math.sin(t * 1.3 + i) * tail, 1000 - 1.1 - 0.4 * math.sin(a0))
            p1 = (1000 - 5.2 * math.cos(a1 * 0.5) + 0.3 * math.sin(t * 1.3 + i + 1) * tail, 1000 - 1.1 - 0.4 * math.sin(a1))
            cap(L, p0, p1, 0.85, 0.8, P['fur'] if i % 2 else P['stripe'], None, None)
        ell(L, H(0.0, 3.3 + br), 6.6, 3.5 + br, P['fur'], 0, P['fur_hi'], P['fur_sh'])
        for j in range(4):                                                           # back stripes
            cap(L, H(-4.2 + j * 1.9, 6.4 + br), H(-4.6 + j * 1.9, 4.3 + br), 0.38, 0.2, P['stripe'])
        ell(L, H(3.3, 0.9), 1.3, 0.6, P['white'], 0, None, P['white_sh'])           # paws
        ell(L, H(5.2, 0.9), 1.3, 0.6, P['white'], 0, None, P['white_sh'])
        ell(L, H(4.5, 3.4 + br), 2.2, 1.9, P['white'], 0, None, P['white_sh'])       # chest
        hc = H(4.4, 6.9 + br)
        Q = cat_head(L, hc, 3.5, lid, mouth, look, t, expr, P)
    elif pose == 'sit':
        tl = [H(-2.0, 0.7)]
        for i in range(6):
            a = i * 0.5 + 0.3 * math.sin(t * 1.4 + i * 0.6) * (0.4 + tail)
            tl.append((tl[-1][0] - 1.3 * math.cos(a), tl[-1][1] - 0.5 * math.sin(a) * (1 if i < 3 else -1)))
        for i in range(6): cap(L, tl[i], tl[i + 1], 0.8, 0.75, P['fur'] if i % 2 else P['stripe'])
        ell(L, H(0.0, 4.6 + br), 4.6, 5.0, P['fur'], 0, P['fur_hi'], P['fur_sh'])
        ell(L, H(0.0, 5.3 + br), 2.4, 3.4, P['white'], 0, None, P['white_sh'])
        for sx in (-1, 1):
            cap(L, H(sx * 1.5, 4.0), H(sx * 1.6, 0.8), 0.95, 0.9, P['fur'], P['fur_hi'], P['fur_sh'])
            ell(L, H(sx * 1.65, 0.6), 1.15, 0.6, P['white'], 0, None, P['white_sh'])
        hc = H(0.0, 11.4 + br)
        Q = cat_head(L, hc, 3.7, lid, mouth, look, t, expr, P)
    elif pose == 'bath':
        hc = H(0.0, 3.0)
        Q = cat_head(L, hc, 3.6, lid, mouth, look, t, expr, P)
        if towel:
            ell(L, H(0.0, 6.9), 3.4, 1.7, (240, 244, 250), 0, (255, 255, 255), (200, 210, 226))
            ell(L, H(0.9, 8.3), 1.9, 1.3, (240, 244, 250), 0.4, (255, 255, 255), (200, 210, 226))
    else:  # walk
        ph = t * 6.0
        for i, (lx, off) in enumerate(((-3.6, 0.0), (3.2, math.pi), (-2.8, math.pi), (4.0, 0.0))):
            sw = 0.5 * math.sin(ph + off)
            cap(L, H(lx, 4.0), H(lx + sw, 0.6), 0.95, 0.85, P['fur_sh'] if i < 2 else P['fur'])
            ell(L, H(lx + sw + 0.3, 0.5), 1.0, 0.5, P['white'])
        for i in range(5):
            cap(L, H(-5.4 - i * 0.9, 5.2 + i * 0.9 + 0.3 * math.sin(t * 3 + i)), H(-6.3 - i * 0.9, 6.1 + (i + 1) * 0.9 + 0.3 * math.sin(t * 3 + i + 1)),
                0.8, 0.75, P['fur'] if i % 2 else P['stripe'])
        ell(L, H(0.0, 5.0 + br), 6.2, 3.3, P['fur'], 0, P['fur_hi'], P['fur_sh'])
        for j in range(4): cap(L, H(-4.0 + j * 1.9, 8.1), H(-4.3 + j * 1.9, 6.1), 0.36, 0.2, P['stripe'])
        hc = H(5.4, 8.0 + br)
        Q = cat_head(L, hc, 3.3, lid, mouth, look, t, expr, P)
    outline(L, P['ol'])
    if cam.sc > 4.5:
        W = Layer(cam); cat_whiskers(W, Q, 1.0, P); L.col[W.m] = W.col[W.m]; L.m |= W.m
    CH.add(L)
    return dict(head=hc)


# ======================================================================================= TAMARA (cashier)
TC = dict(skin=(240, 196, 168), skin_hi=(252, 218, 194), skin_sh=(210, 158, 132), hair=(236, 196, 110), hair_hi=(252, 226, 150),
          hair_sh=(196, 150, 72), roots=(120, 84, 52), shadow=(90, 150, 220), lips=(200, 40, 60), vest=(128, 34, 46),
          vest_hi=(160, 52, 64), vest_sh=(96, 24, 34), blouse=(244, 244, 238), blouse_sh=(206, 206, 204), gum=(250, 140, 190),
          gold=(236, 196, 70), badge=(236, 236, 226), eye=(30, 24, 30), white=(248, 248, 244))


def tamara(CH, cam, t=0.0, mouth=0.0, expr='bored', gum=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None, look=0.0,
           chew=True):
    """cashier behind the counter (full figure, the counter occluder hides the legs). Anchor = floor point.
    expr: bored | annoyed | smug | sigh; gum 0..1 = bubble size (pops at 1)."""
    P = TC
    L = Layer(cam)
    br = 0.12 * math.sin(t * 1.9)
    ch = (0.25 * (1 + math.sin(t * 9.0))) if chew and mouth < 0.1 else 0.0
    sh_n, sh_f = H(2.6, 16.8 + br), H(-2.6, 17.0 + br)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(-2.6, 11.0)
    ka, ea = _limb(A, sh_f, 0, 0, 3.6, 3.4, 1.1, 0.9, P['blouse'], None, P['blouse_sh'], target=tf, bend=-1)
    ell(A, ea, 0.9, 0.85, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_f: prop_f(A, ea)
    _merge(L, A)
    T = Layer(cam)
    ell(T, H(0.3, 9.0), 3.6, 3.0, (60, 60, 70))                                         # skirt
    ell(T, H(0.4, 13.6), 3.9, 4.4, P['blouse'], 0, None, P['blouse_sh'])               # blouse / bust
    ell(T, H(0.1, 12.9), 3.8, 4.3, P['vest'], 0, P['vest_hi'], P['vest_sh'])
    ell(T, H(1.3, 14.6), 1.1, 2.4, P['blouse'], 0.1)                                  # blouse opening
    cap(T, H(2.2, 14.4), H(3.3, 14.2), 0.55, 0.55, P['badge'])                           # name badge
    _merge(L, T)
    Hd = Layer(cam)
    hc = H(0.8, 20.6 + br)
    def F(x, h): return H(x, h + br)
    cap(Hd, F(0.5, 17.2), F(0.7, 18.8), 1.2, 1.2, P['skin'], P['skin_hi'], P['skin_sh'])
    for (x, h, rx, ry) in ((-1.9, 21.6, 1.9, 2.1), (-0.3, 23.0, 2.0, 1.7), (1.6, 22.9, 1.8, 1.6), (-2.4, 19.6, 1.5, 1.8),
                           (2.6, 21.9, 1.3, 1.3), (-0.8, 21.2, 2.4, 2.4)):
        ell(Hd, F(x, h), rx, ry, P['hair'], 0, P['hair_hi'], P['hair_sh'])           # perm cloud (back)
    ell(Hd, F(0.9, 20.4), 2.6, 2.9, P['skin'], 0, P['skin_hi'], P['skin_sh'])        # face
    for (x, h, r) in ((-0.6, 22.6, 1.0), (0.6, 23.1, 1.0), (1.8, 22.7, 0.9), (2.7, 22.0, 0.8), (-1.3, 21.9, 0.9)):
        ell(Hd, F(x, h), r, r * 0.9, P['hair'], 0, P['hair_hi'], P['hair_sh'])       # curls on top
    ell(Hd, F(-0.8, 20.2), 0.5, 0.75, P['skin'], 0, None, P['skin_sh'])              # ear
    ell(Hd, F(-0.8, 19.2), 0.32, 0.4, P['gold'])                                        # earring
    lid = {'bored': 0.55, 'annoyed': 0.45, 'smug': 0.5, 'sigh': 0.8}.get(expr, 0.55)
    for (x, h, r) in ((1.35, 21.0, 0.42), (2.55, 20.95, 0.48)):
        e_ = F(x + 0.1 * look, h)
        ell(Hd, (e_[0], e_[1] + r * 0.15), r, r * 0.8, P['white'])
        dot(Hd, (e_[0] + 0.08 + 0.1 * look, e_[1] + r * 0.3), P['eye'], r * 0.48)
        lt = e_[1] - r * 0.65 + lid * r * 1.25                                        # heavy blue-shadowed upper lid
        poly(Hd, [(e_[0] - r * 1.15, e_[1] - r * 0.9), (e_[0] + r * 1.15, e_[1] - r * 0.9),
                  (e_[0] + r * 1.15, lt), (e_[0] - r * 1.15, lt)], P['shadow'])
        cap(Hd, (e_[0] - r * 1.1, lt), (e_[0] + r * 1.15, lt - 0.05), 0.09, 0.09, P['eye'])          # lash line
        cap(Hd, (e_[0] - r, e_[1] - r * 1.45), (e_[0] + r * 1.1, e_[1] - r * (1.6 if expr != 'annoyed' else 1.2)), 0.09, 0.09, P['roots'])
    ell(Hd, F(3.35, 20.0), 0.45, 0.55, P['skin'], 0, P['skin_hi'], P['skin_sh'])      # nose
    dot(Hd, F(1.2, 19.6), (120, 60, 50), 0.12)                                         # beauty mark
    m = max(mouth, ch)
    mc = F(2.7, 18.8)
    if m > 0.08:
        ell(Hd, mc, 0.55 + 0.2 * m, 0.2 + 0.45 * m, (110, 20, 30))
        ell(Hd, (mc[0], mc[1] - 0.12 - 0.3 * m), 0.6, 0.16, P['lips']); ell(Hd, (mc[0], mc[1] + 0.12 + 0.3 * m), 0.55, 0.18, P['lips'])
    else:
        ell(Hd, mc, 0.62, 0.22, P['lips'])
        if expr == 'smug': cap(Hd, (mc[0] + 0.3, mc[1]), (mc[0] + 0.7, mc[1] - 0.2), 0.1, 0.1, (110, 20, 30))
    if gum > 0.05:
        g = min(gum, 1.0)
        ell(Hd, (mc[0] + 0.3 + g * 0.8, mc[1]), 0.4 + 1.4 * g, 0.4 + 1.3 * g, P['gum'], 0, (255, 190, 220), (220, 110, 160))
    _merge(L, Hd)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(3.6, 10.8)
    kn, en = _limb(A, sh_n, 0, 0, 3.6, 3.4, 1.15, 0.95, P['blouse'], None, P['blouse_sh'], target=tn, bend=1)
    ell(A, en, 0.95, 0.9, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_n: prop_n(A, en)
    _merge(L, A)
    outline(L, OL)
    CH.add(L)
    return dict(head=hc, mouth=mc, hand_n=en, hand_f=ea)


# ======================================================================================= GRANNIES
GZ = dict(skin=(236, 196, 172), skin_hi=(250, 216, 196), skin_sh=(204, 160, 138), coat=(74, 58, 70), coat_hi=(98, 80, 94),
          coat_sh=(54, 42, 52), fur=(104, 74, 52), fur_hi=(140, 104, 76), hat=(86, 58, 42), hat_hi=(118, 84, 62),
          glass=(210, 230, 240), frame=(60, 40, 30), lips=(184, 70, 80), boot=(52, 44, 40), bag=(236, 214, 120))
GL = dict(skin=(242, 200, 176), skin_hi=(252, 220, 200), skin_sh=(210, 162, 140), coat=(70, 96, 84), coat_hi=(90, 120, 104),
          coat_sh=(50, 72, 62), shawl=(176, 172, 168), shawl_hi=(206, 202, 198), shawl_sh=(140, 136, 134), cheek=(236, 134, 124),
          boot=(92, 84, 76), thermos=(196, 60, 50))


def babushka(CH, cam, t=0.0, who='zina', pose='sit', mouth=0.0, expr='normal', look=0.0, hand_n=None, prop_n=None,
             knit=False, tint=None):
    """grannies of the entrance bench. who: zina (thin, tall fur hat, big glasses) | lyuba (round, grey shawl, valenki).
    pose: sit (on a bench at h=0, anchor = bench seat point under the hips... feet hang to h=-6) | stand."""
    P = dict(GZ if who == 'zina' else GL)
    if tint is not None: P = {k: tuple(int(min(255, c * m)) for c, m in zip(v, tint)) for k, v in P.items()}
    L = Layer(cam)
    br = 0.1 * math.sin(t * 1.7 + (0 if who == 'zina' else 1.3))
    sit = pose == 'sit'
    base = 0.0 if sit else 7.0                                   # hip height above the anchor
    fat = 1.0 if who == 'zina' else 1.3
    # legs / boots
    A = Layer(cam)
    if sit:
        for sx, c0 in ((-0.9, P['coat_sh']), (0.9, P['coat'])):
            cap(A, H(sx, 0.4), H(sx + 3.0, 0.2), 1.2 * fat, 1.1 * fat, c0)
            cap(A, H(sx + 3.0, 0.2), H(sx + 3.1, -4.6), 1.0 * fat, 0.9 * fat, c0)
            ell(A, H(sx + 3.5, -5.2), 1.4 * fat, 0.8, P['boot'])
    else:
        for sx, c0 in ((-0.9, P['coat_sh']), (0.9, P['coat'])):
            cap(A, H(sx, 7.0), H(sx, 0.8), 1.0 * fat, 0.9 * fat, c0)
            ell(A, H(sx + 0.5, 0.5), 1.3 * fat, 0.7, P['boot'])
    _merge(L, A)
    # body (coat)
    T = Layer(cam)
    ell(T, H(0.3, base + 4.0), 3.4 * fat, 4.6, P['coat'], 0, P['coat_hi'], P['coat_sh'])
    ell(T, H(0.4, base + 7.4), 3.0 * fat, 2.6, P['coat'], 0, P['coat_hi'], P['coat_sh'])
    if who == 'zina':
        ell(T, H(0.6, base + 9.3), 3.0, 1.2, P['fur'], 0, P['fur_hi'], None)             # fur collar
    else:
        ell(T, H(0.4, base + 8.6), 3.8, 2.4, P['shawl'], 0, P['shawl_hi'], P['shawl_sh'])  # shawl over shoulders
    _merge(L, T)
    # head
    Hd = Layer(cam)
    hy = base + 11.8 + br
    def F(x, h): return H(x, hy + h)
    if who == 'zina':
        ell(Hd, F(0.7, 0.0), 2.1, 2.4, P['skin'], 0, P['skin_hi'], P['skin_sh'])
        ell(Hd, F(0.5, 2.6), 2.4, 1.9, P['hat'], 0, P['hat_hi'], None)                      # tall fur hat
        ell(Hd, F(0.4, 3.7), 2.1, 1.3, P['hat'], 0, P['hat_hi'], None)
        cap(Hd, F(2.5, 0.2), F(3.6, -0.6), 0.45, 0.2, P['skin'])                              # sharp nose
        for x in (1.1, 2.3):                                                                   # big glasses
            ell(Hd, F(x + 0.1 * look, 0.45), 0.72, 0.68, P['frame']); ell(Hd, F(x + 0.1 * look, 0.45), 0.58, 0.54, P['glass'])
            dot(Hd, F(x + 0.15 + 0.15 * look, 0.4), (30, 24, 30), 0.2)
        cap(Hd, F(1.6, 0.5), F(1.8, 0.5), 0.1, 0.1, P['frame'])
        mc = F(2.2, -1.4)
        if mouth > 0.08: ell(Hd, mc, 0.45, 0.2 + 0.4 * mouth, (110, 30, 40))
        else: cap(Hd, (mc[0] - 0.4, mc[1]), (mc[0] + 0.4, mc[1] - (0.12 if expr == 'smug' else 0)), 0.12, 0.12, P['lips'])
        for k in range(3): cap(Hd, F(-0.5 + k * 0.4, -1.1 - k * 0.2), F(-0.1 + k * 0.4, -1.3 - k * 0.2), 0.05, 0.05, P['skin_sh'])
    else:
        ell(Hd, F(0.6, 0.6), 3.0, 3.2, P['shawl'], 0, P['shawl_hi'], P['shawl_sh'])          # shawl around the head
        ell(Hd, F(0.9, 0.0), 2.0, 2.1, P['skin'], 0, P['skin_hi'], P['skin_sh'])
        cap(Hd, F(-0.8, -2.2), F(2.4, -2.4), 0.7, 0.7, P['shawl_sh'])                           # knot
        for x in (0.5, 1.8):
            cap(Hd, F(x - 0.3, 0.45), F(x + 0.3, 0.45), 0.12, 0.12, (30, 24, 30))               # squinty eyes
        ell(Hd, F(0.2, -0.5), 0.55, 0.35, P['cheek']); ell(Hd, F(2.2, -0.5), 0.5, 0.33, P['cheek'])
        ell(Hd, F(2.4, -0.1), 0.45, 0.45, P['skin'], 0, P['skin_hi'], P['skin_sh'])           # round nose
        mc = F(1.5, -1.1)
        if mouth > 0.08: ell(Hd, mc, 0.4, 0.18 + 0.35 * mouth, (110, 30, 40))
        else: cap(Hd, (mc[0] - 0.35, mc[1]), (mc[0] + 0.35, mc[1]), 0.1, 0.1, (150, 70, 70))
    _merge(L, Hd)
    # near arm
    A = Layer(cam)
    shn = H(2.0, base + 8.6)
    tn = hand_n if hand_n is not None else (H(3.8, base + 4.6) if sit else H(3.0, base + 3.4))
    kn, en = _limb(A, shn, 0, 0, 2.8, 2.7, 1.0 * fat, 0.8 * fat, P['coat'], P['coat_hi'], P['coat_sh'], target=tn, bend=1)
    ell(A, en, 0.75, 0.7, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_n: prop_n(A, en)
    if knit and who == 'lyuba':
        ph = t * 6
        cap(A, (en[0] - 1.5, en[1] - 0.3), (en[0] + 1.5 + 0.3 * math.sin(ph), en[1] - 1.6), 0.08, 0.08, (220, 220, 230))
        ell(A, (en[0] - 0.4, en[1] + 0.8), 1.3, 0.9, (190, 70, 70))                              # knitting
    _merge(L, A)
    outline(L, OL)
    CH.add(L)
    return dict(head=F(1.0, 0.0), mouth=mc, hand_n=en)


def plastic_bag(L, hand, open_=1.0):
    """white 'майка' bag with red stripes hanging from the hand"""
    c = (hand[0], hand[1] + 2.4)
    ell(L, c, 1.8 + 0.4 * open_, 2.3, (240, 240, 236), 0, (255, 255, 255), (206, 206, 204))
    cap(L, (hand[0] - 0.6, hand[1] + 0.2), (c[0] - 1.2, c[1] - 1.4), 0.25, 0.25, (240, 240, 236))
    cap(L, (hand[0] + 0.6, hand[1] + 0.2), (c[0] + 1.2, c[1] - 1.4), 0.25, 0.25, (240, 240, 236))
    for dy in (0.3, 1.1): cap(L, (c[0] - 1.9, c[1] + dy), (c[0] + 1.9, c[1] + dy), 0.18, 0.18, (200, 50, 50))


def string_bag(L, hand):
    """авоська with a loaf and a bottle of kefir"""
    c = (hand[0], hand[1] + 2.6)
    ell(L, (c[0] - 0.6, c[1]), 1.4, 0.8, (220, 170, 100)); cap(L, (c[0] + 0.8, c[1] - 1.2), (c[0] + 0.8, c[1] + 1.0), 0.5, 0.5, (244, 244, 250))
    for k in range(5):
        cap(L, (hand[0], hand[1]), (c[0] - 2.0 + k, c[1] + 1.8), 0.07, 0.07, (60, 60, 60))
    for dy in (0.0, 1.0): cap(L, (c[0] - 2.1, c[1] + dy), (c[0] + 2.1, c[1] + dy), 0.07, 0.07, (60, 60, 60))


def valera_prone(CH, cam, t=0.0, crawl=0.0, mouth=0.0, expr='whisper', look=0.0, P=VC):
    """Valera crawling on his belly under a white bedsheet (snow camouflage). Anchor = ground under the belly, facing +x.
    crawl: 0 = frozen still, 1 = full shuffle."""
    L = Layer(cam)
    ph = t * 7.0
    bob = 0.25 * crawl * abs(math.sin(ph))
    sw = 0.8 * crawl * math.sin(ph)
    S = (P['sheet'], P['sheet_hi'], P['sheet_sh'])
    # arms/hands in front (under the sheet edge)
    A = Layer(cam)
    for k, (dx, off) in enumerate(((10.6, 0.0), (9.4, math.pi))):
        x = dx + 0.6 * crawl * math.sin(ph + off)
        ell(A, H(x, 0.75), 1.05, 0.8, P['skin'], 0, P['skin_hi'], P['skin_sh'])
        cap(A, H(x - 2.2, 1.6), H(x - 0.5, 0.9), 0.9, 0.8, *S)
    _merge(L, A)
    # body lump: butt, back, belly sagging into the snow
    B_ = Layer(cam)
    ellt(B_, H(-6.0 + 0.2 * sw, 3.0 + bob), 3.4, 2.7, S)
    ellt(B_, H(0.0, 3.4 + bob), 7.8, 3.3, S)
    ellt(B_, H(1.2, 1.1), 5.2, 1.6, S)                                           # the belly under the sheet
    for x0 in (-3.5, -0.5, 2.6):                                                 # sheet folds
        cap(B_, H(x0, 5.6 + bob), H(x0 + 1.2, 2.2 + bob), 0.18, 0.12, P['sheet_sh'])
    ell(B_, H(-9.0, 1.2), 1.6, 0.9, P['boot'])                                   # boot heels sticking out
    ell(B_, H(-8.4, 0.6), 1.5, 0.8, P['boot'])
    _merge(L, B_)
    # head at the front with the ushanka, the sheet draped over it
    Hd = Layer(cam)
    def F(x, h): return H(7.6 + (x - 0.75) * 0.95, 3.2 + bob + (h - 21.0) * 0.95)
    _valera_head(Hd, F, P, expr, t, mouth, look, 0.0, 0.0, 'ushanka', 'street', True, cam)
    ellt(Hd, F(0.2, 24.4), 3.9, 1.9, S)                                          # sheet over the hat
    cap(Hd, F(-2.6, 24.0), F(-3.2, 20.2), 1.2, 0.8, *S)
    _merge(L, Hd)
    outline(L, OL)
    CH.add(L)
    return dict(head=F(2.0, 21.0), mouth=F(3.0, 19.3))


def flip_phone(L, hand):
    cap(L, (hand[0] - 0.2, hand[1] - 1.2), (hand[0] + 0.1, hand[1] + 0.9), 0.5, 0.45, (60, 64, 76), None, (40, 42, 52))
    dot(L, (hand[0] - 0.15, hand[1] - 0.9), (140, 220, 255), 0.22)


def flying_sheet(CH, cam, k, P=VC):
    """bedsheet thrown off: k 0..1 flight progress (up and back)"""
    L = Layer(cam)
    x, h = -2.0 - 9.0 * k, 16.0 + 14.0 * math.sin(math.pi * min(1.0, k * 0.9))
    for i in range(4):
        ell(L, H(x + i * 1.6 * (1 - k * 0.4), h - i * 0.9 + math.sin(k * 12 + i) * 0.8), 3.2, 1.8, P['sheet'], 0.4 * math.sin(k * 7 + i),
            P['sheet_hi'], P['sheet_sh'])
    outline(L, OL)
    CH.add(L)
