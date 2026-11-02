"""Cast of «Тёща на недельку»: Tolik (lanky son-in-law, mullet, teal «Абибас» tracksuit), Raisa Zakharovna (square mother-in-law,
pink curlers, tattooed brows, gold teeth, rose-print robe), Pusya (2-kg toy terrier in a knitted sweater, bass voice), Sveta (the tired
wife). Same drawing conventions as props/folk.py: anchor (1000,1000) = floor point under the character, H(x, h), +x = facing
direction (ACam.flip mirrors), 3-tone shading from the top-left. Own silhouettes/palettes: nothing is shared with other series' rigs.
World props for the flat (plaid «челнок» bags, the armchair «ТОЛИКОВО», camp bed, ficus, carpet roll, TV) are drawn in world px."""
import math
import numpy as np
from scene import Layer
from props import folk as F
from props.folk import H, cap, ell, ellt, dot, poly, outline, band_mask, recolor, _limb, _merge, _D

OL = (40, 22, 28)


def _mix(a, b, k):
    return tuple(int(x + (y - x) * k) for x, y in zip(a, b))


# ======================================================================================= shared face parts
def eye(L, c, r, expr='normal', look=(0.0, 0.0), white=(246, 244, 238), iris=(60, 40, 30), lid=None, blink=False, lash=None,
        bulge=1.0):
    """one eye at c (unit coords) with radius r: white, iris, pupil, two highlights, upper lid; expr changes the shape"""
    if blink or expr == 'closed':
        cap(L, (c[0] - r, c[1]), (c[0] + r, c[1] + 0.05), 0.13, 0.13, (40, 26, 26)); return
    if expr in ('squint', 'smug', 'sweet'):
        ell(L, c, r * 1.05, r * 0.55, white)
        dot(L, (c[0] + look[0] * r * 0.3, c[1] + 0.05), iris, r * 0.48)
        dot(L, (c[0] + look[0] * r * 0.3, c[1] + 0.05), (20, 14, 14), r * 0.24)
        if lid is not None: cap(L, (c[0] - r * 1.1, c[1] - r * 0.42), (c[0] + r * 1.1, c[1] - r * 0.5), r * 0.32, r * 0.3, lid)
        if lash is not None: cap(L, (c[0] - r * 1.1, c[1] - r * 0.5), (c[0] + r * 1.15, c[1] - r * 0.6), 0.12, 0.12, lash)
        return
    rr = r * bulge * (1.3 if expr in ('shout', 'shock', 'scream') else 1.0)
    ell(L, c, rr, rr * 1.1, white)
    ir = rr * (0.36 if expr in ('shout', 'shock', 'scream') else 0.55)
    ix, iy = c[0] + look[0] * rr * 0.35, c[1] + look[1] * rr * 0.35
    dot(L, (ix, iy), iris, ir)
    dot(L, (ix, iy), (18, 12, 12), ir * 0.52)
    dot(L, (ix + ir * 0.35, iy - ir * 0.4), (255, 255, 255), ir * 0.3)
    dot(L, (ix - ir * 0.3, iy + ir * 0.35), (230, 236, 255), ir * 0.14)
    if lid is not None and expr not in ('shout', 'shock', 'scream'):
        cap(L, (c[0] - rr, c[1] - rr * 0.62), (c[0] + rr, c[1] - rr * 0.72), 0.16, 0.16, lid)
    if lash is not None:
        cap(L, (c[0] - rr * 1.05, c[1] - rr * 0.8), (c[0] + rr * 1.1, c[1] - rr * 0.95), 0.13, 0.13, lash)
        cap(L, (c[0] + rr * 1.0, c[1] - rr * 0.9), (c[0] + rr * 1.45, c[1] - rr * 1.25), 0.1, 0.06, lash)


def mouth(L, c, w, m, expr='normal', lip=None, inner=(92, 22, 30), teeth=(250, 248, 240), tongue=(222, 96, 104), gold=None,
          smile=0.0):
    """mouth centred at c, half-width w. m 0..1 open; open mouths show upper teeth and a tongue; gold = indices of gold teeth"""
    if m > 0.08:
        rw = w * (0.85 + 0.35 * m); rh = w * (0.25 + 0.95 * m)
        ell(L, (c[0], c[1] + rh * 0.35), rw, rh, inner)
        ell(L, (c[0] + 0.05, c[1] + rh * 0.95), rw * 0.62, rh * 0.42, tongue)
        ty = c[1] + rh * 0.35 - rh * 0.72
        cap(L, (c[0] - rw * 0.72, ty), (c[0] + rw * 0.72, ty), rh * 0.2, rh * 0.2, teeth)
        if gold:
            for gi in gold:
                gx = c[0] - rw * 0.55 + gi * rw * 0.36
                ell(L, (gx, ty + 0.02), rw * 0.15, rh * 0.2, (246, 196, 60))
                dot(L, (gx - 0.04, ty - 0.05), (255, 244, 180), rw * 0.06)
        if lip is not None:
            cap(L, (c[0] - rw, c[1] + rh * 0.3), (c[0] - rw * 0.2, c[1] - rh * 0.4), 0.2, 0.2, lip)
            cap(L, (c[0] - rw * 0.2, c[1] - rh * 0.4), (c[0] + rw, c[1] + rh * 0.3), 0.2, 0.2, lip)
        return
    col = lip if lip is not None else (120, 50, 50)
    if expr == 'grin':                                                                     # sugary toothy smile
        ell(L, (c[0], c[1] + 0.05), w * 1.05, w * 0.42, inner)
        poly(L, [(c[0] - w * 1.05, c[1] - 0.05), (c[0] + w * 1.05, c[1] - 0.12), (c[0] + w * 1.2, c[1] - 0.6), (c[0] - w * 1.2, c[1] - 0.5)],
             (1, 1, 1))
        L.m[(L.col == 1).all(-1)] = False
        cap(L, (c[0] - w * 0.8, c[1] + 0.02), (c[0] + w * 0.8, c[1] - 0.02), w * 0.16, w * 0.16, teeth)
        if gold:
            ell(L, (c[0] + w * 0.25, c[1] + 0.02), w * 0.17, w * 0.17, (246, 196, 60))
            dot(L, (c[0] + w * 0.2, c[1] - 0.04), (255, 244, 180), w * 0.06)
        cap(L, (c[0] - w * 1.15, c[1] - 0.15), (c[0], c[1] + w * 0.48), 0.2, 0.2, col)
        cap(L, (c[0], c[1] + w * 0.48), (c[0] + w * 1.15, c[1] - 0.2), 0.2, 0.2, col)
        cap(L, (c[0] - w * 1.15, c[1] - 0.15), (c[0] + w * 1.15, c[1] - 0.2), 0.16, 0.16, col)
        return
    if expr in ('smug', 'sweet', 'proud', 'happy') or smile > 0.3:
        cap(L, (c[0] - w, c[1] - 0.15), (c[0], c[1] + 0.12), 0.16, 0.16, col)
        cap(L, (c[0], c[1] + 0.12), (c[0] + w, c[1] - 0.22), 0.16, 0.16, col)
        if gold and expr == 'sweet':
            ell(L, (c[0] + w * 0.3, c[1] + 0.02), w * 0.22, 0.16, (246, 196, 60))
    elif expr in ('sad', 'angry', 'whine', 'tired'):
        cap(L, (c[0] - w, c[1] + 0.15), (c[0], c[1] - 0.08), 0.15, 0.15, col)
        cap(L, (c[0], c[1] - 0.08), (c[0] + w, c[1] + 0.18), 0.15, 0.15, col)
    else:
        cap(L, (c[0] - w, c[1]), (c[0] + w, c[1] - 0.04), 0.15, 0.15, col)


# ======================================================================================= TOLIK
TC = dict(skin=(242, 196, 162), skin_hi=(254, 222, 194), skin_sh=(206, 152, 122), cheek=(236, 150, 136), stub=(196, 160, 136),
          hair=(122, 80, 46), hair_hi=(160, 112, 66), hair_sh=(88, 56, 32), must=(98, 62, 36), brow=(86, 54, 32),
          suit=(34, 176, 168), suit_hi=(86, 216, 202), suit_sh=(20, 122, 120), stripe=(248, 248, 242), tank=(240, 226, 128),
          tank_sh=(206, 186, 92), sock=(160, 160, 166), slip=(60, 84, 150), slip_hi=(90, 116, 186), slip_sh=(40, 56, 108),
          hat=(196, 40, 52), hat_hi=(232, 80, 84), hat_sh=(140, 26, 36), blanket=(196, 56, 52), blanket_hi=(228, 96, 80),
          blanket_sh=(140, 34, 36), plaid=(40, 84, 60))
TPOSE = dict(
    stand=dict(n=(2.6, 13.4), f=(-2.2, 13.6), bn=1, bf=-1, nleg=(0.04, 0.0), fleg=(-0.04, 0.0)),
    proud=dict(n=(3.2, 20.6), f=(-2.6, 14.0), bn=1, bf=-1, nleg=(0.18, 0.0), fleg=(-0.2, 0.0), chest=1.0),     # fist on chest
    fists=dict(n=(3.6, 17.6), f=(-3.2, 17.4), bn=1, bf=-1, nleg=(0.22, 0.0), fleg=(-0.22, 0.0), chest=1.0),    # «Я мужик!» pose
    shock=dict(n=(5.2, 20.4), f=(-3.6, 20.6), bn=1, bf=-1, nleg=(0.1, 0.0), fleg=(-0.1, 0.0)),                 # hands up, jaw drop
    cheeks=dict(n=(2.9, 25.6), f=(-0.6, 25.8), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),              # «Home Alone» hands
    phone=dict(n=(4.0, 20.2), f=(-2.2, 13.6), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),               # phone at the ear
    carry=dict(n=(1.6, 7.2), f=(0.4, 7.4), bn=1, bf=1, nleg=(0.35, 0.0), fleg=(-0.3, 0.0), lean=1.8),         # dragging a bag low
    sit=dict(n=(4.4, 13.8), f=(3.6, 14.0), bn=1, bf=1, nleg=(1.55, 0.0), fleg=(1.45, 0.0)),
    shiver=dict(n=(0.2, 19.0), f=(2.4, 18.6), bn=1, bf=-1, nleg=(0.04, 0.0), fleg=(-0.04, 0.0)),               # hugging himself
)


def _stripes(L, a, b, off, col, n=3, gap=0.18, r=0.07):
    """three tracksuit stripes along a limb segment a->b, offset to the outer side"""
    dx, dy = b[0] - a[0], b[1] - a[1]; l = math.hypot(dx, dy) + 1e-6
    nx, ny = -dy / l, dx / l
    for i in range(n):
        o = off + (i - (n - 1) / 2) * gap
        cap(L, (a[0] + nx * o, a[1] + ny * o), (b[0] + nx * o, b[1] + ny * o), r, r, col)


def _tolik_head(Hd, Fh, P, expr, t, m, look, hat, blink, cold):
    cap(Hd, Fh(-0.1, 21.9), Fh(0.5, 25.4), 0.85, 0.82, P['skin'], P['skin_hi'], P['skin_sh'])               # long thin neck
    ell(Hd, Fh(0.95, 23.7), 0.42, 0.55, P['skin_sh'])                                                         # Adam's apple
    dot(Hd, Fh(1.0, 23.85), P['skin_hi'], 0.18)
    if hat is None:                                                                                         # mullet tail behind
        cap(Hd, Fh(-1.6, 27.4), Fh(-2.1, 23.6), 1.15, 0.95, P['hair'], P['hair_hi'], P['hair_sh'])
        for k in range(3):
            cap(Hd, Fh(-2.3 + k * 0.45, 24.4), Fh(-2.5 + k * 0.5, 22.9 - (k % 2) * 0.4), 0.32, 0.16, P['hair'])
    ell(Hd, Fh(0.7, 27.25), 2.25, 2.75, P['skin'], -0.05, None, P['skin_sh'], th_sh=-0.72)                       # narrow long skull
    ell(Hd, Fh(1.55, 25.35), 1.65, 1.05, P['skin'], 0.1)                                # chin
    ell(Hd, Fh(1.9, 25.15), 0.95, 0.42, _mix(P['skin_sh'], P['stub'], 0.5), 0.12)                                  # stubble
    ell(Hd, Fh(-1.15, 27.1), 1.05, 1.45, P['skin'], 0.15, P['skin_hi'], P['skin_sh'])                       # big sticking-out ear
    ell(Hd, Fh(-1.1, 27.1), 0.55, 0.9, P['cheek'])
    if hat is None or hat == 'down':
        ell(Hd, Fh(0.35, 29.15), 2.35, 1.25, P['hair'], 0.05, P['hair_hi'], P['hair_sh'])                    # short top
        for k in range(4):                                                                                   # spiky bangs
            x0 = 0.6 + k * 0.55
            poly(Hd, [Fh(x0 - 0.35, 29.1), Fh(x0 + 0.4, 29.1), Fh(x0 + 0.25 + 0.15 * k, 28.0 - (k % 2) * 0.35)], P['hair'])
        cap(Hd, Fh(-0.8, 28.6), Fh(-1.6, 27.9), 0.5, 0.4, P['hair'])                                          # sideburn
    else:                                                                                                    # knitted hat with pompon
        ell(Hd, Fh(0.6, 29.0), 2.55, 1.75, P['hat'], 0, P['hat_hi'], P['hat_sh'])
        cap(Hd, Fh(-1.9, 28.0), Fh(3.0, 28.0), 0.55, 0.55, P['hat_sh'])
        for k in range(5): cap(Hd, Fh(-1.3 + k * 0.95, 28.4), Fh(-1.1 + k * 0.95, 30.0), 0.12, 0.12, P['hat_sh'])
        ell(Hd, Fh(0.4, 31.0), 0.95, 0.9, (246, 240, 230), 0, (255, 255, 255), (206, 200, 196))
    lk = (look, 0.0)
    eyes = [(Fh(1.15, 27.5), 0.56), (Fh(2.35, 27.4), 0.66)]
    bl = blink and (t % 3.3) < 0.1 and expr not in ('shout', 'scream', 'shock')
    ex = {'scream': 'shout', 'shout': 'shout', 'shock': 'shock', 'proud': 'normal', 'smug': 'smug', 'sad': 'normal',
          'whine': 'normal', 'angry': 'normal', 'cold': 'normal'}.get(expr, 'normal')
    for c, r in eyes:
        ell(Hd, (c[0] - 0.05, c[1] + r * 1.05), r * 1.0, r * 0.35, P['skin_sh'])                           # eye bags
        eye(Hd, c, r, ex, lk, lid=P['skin_sh'], blink=bl, bulge=1.1)
    bt = {'angry': 0.6, 'shout': -0.4, 'scream': -0.6, 'shock': -0.7, 'proud': -0.25, 'smug': 0.3, 'sad': -0.6, 'whine': -0.7,
          'cold': -0.4}.get(expr, 0.0)
    lift = 0.45 if expr in ('shout', 'scream', 'shock') else 0.0
    for k, (c, r) in enumerate(eyes):
        s_ = 1 if k == 0 else -1
        base = c[1] - r - 0.5 - lift
        cap(Hd, (c[0] - 0.6, base - s_ * bt * 0.4), (c[0] + 0.6, base + s_ * bt * 0.4), 0.27, 0.22, P['brow'])
    if hat == 'down':                                                                                        # hat yanked down over the eyes
        ell(Hd, Fh(0.7, 28.9), 2.75, 2.1, P['hat'], 0, P['hat_hi'], P['hat_sh'])
        cap(Hd, Fh(-2.0, 27.0), Fh(3.4, 27.0), 0.62, 0.62, P['hat_sh'])
        for k in range(6): cap(Hd, Fh(-1.6 + k * 0.95, 27.4), Fh(-1.4 + k * 0.95, 30.0), 0.12, 0.12, P['hat_sh'])
        ell(Hd, Fh(0.4, 31.2), 0.95, 0.9, (246, 240, 230), 0, (255, 255, 255), (206, 200, 196))
    ell(Hd, Fh(1.9, 26.1), 0.7, 0.4, P['cheek'])
    poly(Hd, [Fh(3.0, 26.9), Fh(4.45, 25.85), Fh(3.05, 25.65)], P['skin_sh'])                                   # long pointy nose
    poly(Hd, [Fh(3.05, 26.8), Fh(4.3, 25.95), Fh(3.15, 25.9)], P['skin'])
    dot(Hd, Fh(3.6, 26.4), P['skin_hi'], 0.16)
    mm = max(m, {'scream': 0.95, 'shout': 0.7, 'shock': 0.55}.get(expr, 0.0))
    mc = Fh(2.75, 24.95 - 0.25 * mm)
    mouth(Hd, mc, 0.82, mm, {'proud': 'proud', 'smug': 'smug'}.get(expr, 'sad' if expr in ('sad', 'whine', 'angry') else 'normal'),
          lip=(176, 96, 88))
    cap(Hd, Fh(2.35, 25.55), Fh(3.45, 25.68), 0.2, 0.2, P['must'])                                             # pencil moustache
    if cold > 0.4:
        dot(Hd, Fh(4.1, 25.75), (200, 230, 255), 0.22)                                                         # icicle drip at the nose
    return mc


def tolik(CH, cam, pose=None, t=0.0, mouth_=0.0, expr='normal', look=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
          lean=None, hat=None, blanket=False, cold=0.0, blink=True, shake=0.0, outline_=True):
    """expr: normal | scream | shout | shock | proud | smug | sad | whine | angry | cold.  hat: None | 'knit'.
    blanket: plaid blanket over the shoulders (balcony). shake: tremble amplitude (units)."""
    pose = pose or TPOSE['stand']
    P = dict(TC)
    if cold > 0:
        for k, v in dict(skin=(196, 210, 240), skin_hi=(222, 232, 255), skin_sh=(150, 164, 214), cheek=(170, 180, 240)).items():
            P[k] = _mix(P[k], v, cold * 0.6)
    br = 0.15 * math.sin(t * 2.4)
    jx = shake * math.sin(t * 47.0)
    ln = (pose.get('lean', 0.0) if lean is None else lean) + jx
    sh_n, sh_f = H(1.4 + ln, 21.7 + br), H(-1.3 + ln, 21.9 + br)
    hp_n, hp_f = H(0.9, 13.6), H(-0.7, 13.6)
    suit = (P['suit'], P['suit_hi'], P['suit_sh'])
    foot = (P['slip'], P['slip_hi'], P['slip_sh'])
    L = Layer(cam)
    # far leg + far arm
    A = Layer(cam)
    kf, ef = _limb(A, hp_f, *pose['fleg'], 6.9, 6.4, 1.0, 0.82, *suit)
    _stripes(A, hp_f, kf, -0.55, P['stripe']); _stripes(A, kf, ef, -0.5, P['stripe'])
    cap(A, (ef[0], ef[1] - 0.2), (ef[0] + 0.3, ef[1] + 0.1), 0.6, 0.6, P['sock'])
    ellt(A, (ef[0] + 1.0, ef[1] + 0.4), 1.75, 0.6, foot)
    _merge(L, A, OL)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(pose['f'][0] + jx, pose['f'][1])
    ka, ea = _limb(A, sh_f, 0, 0, 4.6, 4.3, 0.92, 0.7, *suit, target=tf, bend=pose.get('bf', -1))
    _stripes(A, sh_f, ka, -0.5, P['stripe']); _stripes(A, ka, ea, -0.45, P['stripe'])
    ell(A, ea, 0.95, 0.88, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_f: prop_f(A, ea)
    _merge(L, A, OL)
    # near leg + pelvis
    A = Layer(cam)
    ellt(A, H(0.1, 14.2), 2.3, 1.7, suit)
    kn, en = _limb(A, hp_n, *pose['nleg'], 6.9, 6.4, 1.05, 0.85, *suit)
    _stripes(A, hp_n, kn, 0.55, P['stripe']); _stripes(A, kn, en, 0.5, P['stripe'])
    cap(A, (en[0], en[1] - 0.2), (en[0] + 0.3, en[1] + 0.1), 0.62, 0.62, P['sock'])
    ellt(A, (en[0] + 1.05, en[1] + 0.4), 1.85, 0.62, foot)
    _merge(L, A, OL)
    # torso: narrow chest, pot belly forward; open jacket shows the yellow tank top
    T = Layer(cam)
    chest = 1.0 + 0.25 * pose.get('chest', 0.0)
    ellt(T, H(0.15 + ln * 0.6, 19.4 + br), 2.35 * chest, 3.5, suit)
    ellt(T, H(1.0 + ln * 0.35, 16.0 + br * 0.5), 2.9, 2.35, suit)
    poly(T, [H(0.9 + ln * 0.7, 22.0 + br), H(2.2 + ln * 0.6, 21.6 + br), H(3.5 + ln * 0.35, 15.6), H(2.6 + ln * 0.35, 14.2),
             H(1.2 + ln * 0.4, 17.0)], P['tank'])
    ell(T, H(2.7 + ln * 0.35, 15.3), 1.1, 0.9, P['tank_sh'])                                                 # belly in the tank
    cap(T, H(1.0 + ln * 0.7, 22.0 + br), H(1.3 + ln * 0.4, 14.2), 0.14, 0.14, (200, 200, 196))              # zipper edges
    cap(T, H(2.2 + ln * 0.6, 21.6 + br), H(3.3 + ln * 0.35, 15.0), 0.14, 0.14, (200, 200, 196))
    cap(T, H(-1.4 + ln * 0.6, 22.2 + br), H(1.6 + ln * 0.7, 22.4 + br), 0.55, 0.45, P['suit_sh'])          # collar
    cap(T, H(-0.9, 13.4), H(2.6, 13.4), 0.35, 0.35, P['suit_sh'])                                             # jacket hem band
    _merge(L, T, OL)
    # head
    Hd = Layer(cam)
    hx = 0.4 + ln * 1.15
    def Fh(x, h): return H(hx + x - 0.4, h + br)
    mc = _tolik_head(Hd, Fh, P, expr, t, mouth_, look, hat, blink, cold)
    _merge(L, Hd, OL)
    # near arm
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(pose['n'][0] + jx, pose['n'][1])
    kna, ena = _limb(A, sh_n, 0, 0, 4.6, 4.3, 0.95, 0.72, *suit, target=tn, bend=pose.get('bn', 1))
    _stripes(A, sh_n, kna, 0.5, P['stripe']); _stripes(A, kna, ena, 0.45, P['stripe'])
    ell(A, ena, 0.98, 0.9, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_n: prop_n(A, ena)
    _merge(L, A, OL)
    if blanket:
        B = Layer(cam)
        poly(B, [H(-2.2 + ln * 0.6, 22.6 + br), H(2.0 + ln * 0.6, 22.6 + br), H(1.4 + ln * 0.3, 15.0), H(-3.0, 13.6)], P['blanket'])
        ellt(B, H(-0.6 + ln * 0.5, 19.0 + br), 2.4, 3.6, (P['blanket'], P['blanket_hi'], P['blanket_sh']))
        m1 = band_mask(B, H(0.4, 18.2), 0.55, width=4.0); m2 = band_mask(B, H(0.4, 18.2), 0.55, width=4.0, ang=1.57)
        recolor(B, m1 & m2, [(P['blanket'], P['plaid']), (P['blanket_hi'], P['plaid']), (P['blanket_sh'], P['plaid'])])
        m3 = band_mask(B, H(0.2, 18.0), 1.1, width=4.0, ang=1.57) & ~band_mask(B, H(0.45, 18.0), 1.1, width=4.0, ang=1.57)
        recolor(B, m3, [(P['blanket'], (236, 200, 90))])
        cap(B, H(-2.0 + ln * 0.6, 22.6 + br), H(2.6 + ln * 0.6, 22.6 + br), 0.9, 0.9, P['blanket_hi'], None, P['blanket'])
        _merge(L, B, OL)
    if outline_: outline(L, OL)
    CH.add(L)
    return dict(hand_n=ena, hand_f=ea, mouth=mc, head=Fh(0.9, 27.2), top=Fh(0.5, 30.4))


# ======================================================================================= RAISA (тёща)
RC = dict(skin=(240, 192, 162), skin_hi=(252, 216, 190), skin_sh=(206, 150, 124), rouge=(236, 128, 136), brow=(70, 34, 26),
          lip=(204, 28, 56), hair=(222, 92, 36), hair_hi=(250, 140, 66), curl=(255, 150, 196), curl_hi=(255, 196, 226),
          curl_sh=(214, 94, 150), net=(110, 70, 96), robe=(250, 206, 216), robe_hi=(255, 228, 234), robe_sh=(222, 160, 178),
          rose=(206, 34, 84), rose_hi=(240, 86, 124), rose_sh=(150, 20, 60), leaf=(84, 150, 82), gold=(246, 196, 60),
          gold_hi=(255, 240, 170), pearl=(250, 248, 240), slip=(176, 40, 92), slip_hi=(214, 80, 130), pom=(255, 236, 246))
LYUSYA = dict(hair=(120, 60, 150), hair_hi=(160, 100, 190), curl=(130, 70, 160), curl_hi=(170, 110, 200), curl_sh=(90, 40, 116),
              net=(130, 70, 160), robe=(86, 60, 50), robe_hi=(120, 90, 74), robe_sh=(60, 40, 34), rose=(70, 48, 40), rose_hi=(96, 70, 58),
              rose_sh=(56, 38, 32), leaf=(70, 48, 40), lip=(150, 40, 120), slip=(40, 40, 46), slip_hi=(70, 70, 80), pom=(40, 40, 46))
GRANNY = [dict(hair=(200, 200, 206), hair_hi=(236, 236, 240), curl=(206, 206, 212), curl_hi=(240, 240, 244), curl_sh=(160, 160, 170),
               net=(150, 150, 160), robe=(80, 110, 170), robe_hi=(120, 150, 206), robe_sh=(56, 80, 130), rose=(240, 240, 250),
               rose_hi=(255, 255, 255), rose_sh=(200, 200, 220), leaf=(80, 110, 170)),
          dict(hair=(150, 90, 60), hair_hi=(190, 130, 90), curl=(160, 100, 66), curl_hi=(200, 140, 100), curl_sh=(110, 66, 40),
               net=(110, 66, 40), robe=(90, 140, 90), robe_hi=(130, 180, 120), robe_sh=(60, 100, 60), rose=(230, 200, 80),
               rose_hi=(250, 230, 130), rose_sh=(180, 150, 50), leaf=(60, 100, 60))]
RPOSE = dict(
    stand=dict(n=(3.6, 9.4), f=(-3.4, 9.6), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
    hips=dict(n=(3.6, 10.6), f=(-3.6, 10.6), bn=-1, bf=1, nleg=(0.16, 0.0), fleg=(-0.16, 0.0)),
    offer=dict(n=(6.6, 11.6), f=(-3.3, 9.6), bn=1, bf=-1, nleg=(0.1, 0.0), fleg=(-0.1, 0.0)),      # hands a bag forward
    hold=dict(n=(4.2, 11.6), f=(3.4, 11.8), bn=1, bf=1, nleg=(0.08, 0.0), fleg=(-0.08, 0.0)),      # holds Pusya at the chest
    point=dict(n=(7.2, 14.4), f=(-3.3, 9.6), bn=1, bf=-1, nleg=(0.1, 0.0), fleg=(-0.1, 0.0)),
    call=dict(n=(3.8, 18.6), f=(-3.4, 9.6), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),    # hand at the mouth, calling
    sit=dict(n=(4.4, 8.4), f=(3.6, 8.6), bn=1, bf=1, nleg=(1.5, 0.0), fleg=(1.42, 0.0)),
)


def _rose(L, c, r, P):
    ell(L, c, r, r * 0.9, P['rose'], 0, P['rose_hi'], P['rose_sh'])
    cap(L, (c[0] - r * 0.5, c[1] - r * 0.1), (c[0] + r * 0.3, c[1] - r * 0.4), r * 0.18, r * 0.12, P['rose_sh'])
    cap(L, (c[0] - r * 0.3, c[1] + r * 0.3), (c[0] + r * 0.5, c[1] + r * 0.05), r * 0.16, r * 0.1, P['rose_sh'])
    ell(L, (c[0] + r * 1.05, c[1] + r * 0.45), r * 0.55, r * 0.28, P['leaf'], 0.5)


def _robe_roses(L, cxy, rx, ry, P, seed=0):
    """big roses scattered inside the robe part (only where L already has the robe)"""
    pts = [(-0.55, 0.45), (0.35, 0.6), (0.15, -0.1), (-0.4, -0.55), (0.55, -0.45), (-0.05, 0.05)]
    keep = L.m.copy()
    for i, (a, b) in enumerate(pts):
        _rose(L, (cxy[0] + a * rx, cxy[1] - b * ry), 1.05 + 0.2 * ((i + seed) % 2), P)
    L.m &= keep


def _raisa_head(Hd, Fh, P, expr, t, m, look, blink, call):
    ell(Hd, Fh(1.0, 16.2), 2.7, 1.4, P['skin'], 0, None, P['skin_sh'])                                       # double chin
    ell(Hd, Fh(0.6, 18.6), 3.05, 3.0, P['skin'], 0, None, P['skin_sh'], th_sh=-0.72)                               # round face
    ell(Hd, Fh(-1.75, 18.4), 0.7, 0.95, P['skin'], 0, None, P['skin_sh'])                                       # ear
    ell(Hd, Fh(-1.75, 17.15), 0.42, 0.55, P['gold'], 0, P['gold_hi'], None)                                     # gold hoop earring
    ell(Hd, Fh(-1.75, 17.15), 0.2, 0.3, P['skin_sh'])
    # curlers dome: pink plastic rollers over orange henna curls, hairnet
    for (x, h, r) in ((-1.2, 21.1, 0.95), (1.9, 21.0, 0.9), (-2.1, 19.6, 0.85), (2.9, 19.9, 0.7)):
        ell(Hd, Fh(x, h), r, r * 0.9, P['hair'], 0, P['hair_hi'], None)
    rollers = [(-1.8, 20.8), (-0.6, 21.6), (0.7, 21.8), (2.0, 21.3), (-1.2, 22.6), (0.1, 23.0), (1.4, 22.7), (-2.4, 19.9), (2.9, 20.3)]
    for i, (x, h) in enumerate(rollers):
        ell(Hd, Fh(x, h), 0.72, 0.6, P['curl'], 0.3 * ((i % 3) - 1), P['curl_hi'], P['curl_sh'])
        dot(Hd, Fh(x + 0.15, h + 0.02), P['curl_sh'], 0.22)
    for k in range(5):                                                                                         # hairnet arcs
        a0, a1 = -2.6 + k * 1.25, -2.0 + k * 1.25
        cap(Hd, Fh(a0, 22.6 - abs(k - 2) * 0.5), Fh(a1, 23.1 - abs(k - 1.5) * 0.5), 0.05, 0.05, P['net'])
    for k in range(3):                                                                                         # curls on the forehead
        ell(Hd, Fh(0.9 + k * 0.9, 20.75 - (k % 2) * 0.15), 0.42, 0.36, P['hair'], 0, P['hair_hi'], None)
    eyes = [(Fh(1.15, 18.95), 0.5), (Fh(2.5, 18.9), 0.6)]
    bl = blink and (t % 4.1) < 0.1
    ex = {'sweet': 'sweet', 'smug': 'smug', 'shock': 'shock', 'shout': 'shout', 'angry': 'normal', 'stern': 'normal'}.get(expr, 'normal')
    for c, r in eyes:
        eye(Hd, c, r, ex, (look, 0.0), iris=(70, 110, 60), lid=(214, 140, 170), lash=(30, 20, 24), blink=bl)
    for k, (c, r) in enumerate(eyes):                                                                          # tattooed brows, high arch
        s_ = 1 if k == 0 else -1
        lift = 0.25 if expr in ('shock', 'shout') else 0.0
        b = c[1] - r - 0.75 - lift
        pts = [(c[0] - 0.7, b + 0.3), (c[0] - 0.1, b - 0.35), (c[0] + 0.7, b + 0.05)]
        if expr in ('angry', 'stern'): pts = [(c[0] - 0.7, b + 0.1 * s_), (c[0], b - 0.05), (c[0] + 0.7, b + 0.25 * s_)]
        cap(Hd, pts[0], pts[1], 0.17, 0.19, P['brow']); cap(Hd, pts[1], pts[2], 0.19, 0.13, P['brow'])
    ell(Hd, Fh(1.15, 17.6), 0.75, 0.45, P['rouge']); ell(Hd, Fh(3.0, 17.6), 0.45, 0.4, P['rouge'])
    ell(Hd, Fh(3.25, 18.05), 0.62, 0.55, P['skin'], 0, P['skin_hi'], P['skin_sh'])                            # round nose
    dot(Hd, Fh(3.05, 18.25), P['skin_hi'], 0.14)
    dot(Hd, Fh(0.55, 17.25), (110, 64, 50), 0.22)                                                             # mole
    mm = max(m, {'shout': 0.7, 'shock': 0.5}.get(expr, 0.0))
    mc = Fh(2.55, 16.85 - 0.2 * mm)
    mouth(Hd, mc, 0.95, mm, {'sweet': 'grin'}.get(expr, expr if expr in ('smug', 'angry') else 'normal'), lip=P['lip'], gold=[1, 2])
    return mc


def raisa(CH, cam, pose=None, t=0.0, mouth_=0.0, expr='sweet', look=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
          blink=True, outline_=True, pal=None):
    """expr: sweet (sugary smile with a gold tooth) | smug | stern | angry | shock | shout | normal. Anchor = floor.
    pal: palette overrides (RC keys) — her sister Lyusya and the minibus grannies are recoloured Raisas."""
    pose = pose or RPOSE['stand']
    P = dict(RC, **pal) if pal else RC
    br = 0.12 * math.sin(t * 2.0)
    sh_n, sh_f = H(3.1, 15.0 + br), H(-2.9, 15.2 + br)
    sit = pose is RPOSE['sit'] or pose.get('nleg', (0, 0))[0] > 1.0
    hp_n, hp_f = H(1.3, 6.4), H(-1.1, 6.4)
    robe = (P['robe'], P['robe_hi'], P['robe_sh'])
    skin = (P['skin'], P['skin_hi'], P['skin_sh'])
    L = Layer(cam)
    for side, hp, lg in ((-1, hp_f, pose['fleg']), (1, hp_n, pose['nleg'])):                               # stumpy legs + slippers
        A = Layer(cam)
        k, e = _limb(A, hp, *lg, 3.3, 3.1, 1.5, 1.15, *skin)
        ellt(A, (e[0] + 1.0, e[1] + 0.45), 1.75, 0.75, (P['slip'], P['slip_hi'], P['slip']))
        ell(A, (e[0] + 2.2, e[1] + 0.1), 0.6, 0.55, P['pom'])
        _merge(L, A, OL)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(*pose['f'])
    ka, ea = _limb(A, sh_f, 0, 0, 3.5, 3.3, 1.45, 1.2, *robe, target=tf, bend=pose.get('bf', -1))
    ell(A, ea, 1.15, 1.05, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_f: prop_f(A, ea)
    _merge(L, A, OL)
    # the «wardrobe» body in a rose-print robe
    T = Layer(cam)
    ellt(T, H(0.4, 10.4 + br * 0.5), 5.0, 5.6, robe)
    if not sit:
        poly(T, [H(-4.2, 9.0), H(4.9, 9.0), H(5.4, 3.0), H(-4.7, 3.0)], P['robe'])                             # robe skirt to the knees
    else:
        poly(T, [H(-4.0, 9.0), H(5.0, 9.0), H(8.0, 6.6), H(7.6, 4.2), H(-3.0, 5.0)], P['robe'])
    ellt(T, H(1.7, 12.6 + br), 3.6, 2.5, robe)                                                                 # bosom
    _robe_roses(T, H(0.6, 9.4), 4.6, 6.0, P)
    cap(T, H(-1.0, 15.6 + br), H(2.6, 9.6), 0.42, 0.42, P['rose_sh'])                                          # robe overlap edge
    cap(T, H(-4.4, 9.1), H(5.3, 9.1), 0.45, 0.45, P['rose'])                                                   # belt
    ell(T, H(2.9, 9.0), 0.75, 0.55, P['rose'], 0, P['rose_hi'], None)
    _merge(L, T, OL)
    from stage import ACam
    piv = H(0.8, 11.2 + br); sp = cam.p(*piv)
    Hd = Layer(ACam(piv[0], piv[1], sp[0], sp[1], cam.sc * 1.2, cam.flip))
    hx = 0.6
    def Fh(x, h): return H(hx + x - 0.6, h + br)
    cap(Hd, Fh(0.4, 14.6), Fh(0.8, 16.4), 1.6, 1.6, P['skin'], P['skin_hi'], P['skin_sh'])                    # short neck
    for k in range(9):                                                                                          # pearl beads
        a = -0.9 + k * 0.23
        dot(Hd, Fh(0.9 + 2.2 * math.sin(a), 15.3 - 0.9 * math.cos(a) + 0.5), P['pearl'], 0.3)
    mc = _raisa_head(Hd, Fh, P, expr, t, mouth_, look, blink, False)
    _merge(L, Hd, OL)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(*pose['n'])
    kna, ena = _limb(A, sh_n, 0, 0, 3.5, 3.3, 1.5, 1.22, *robe, target=tn, bend=pose.get('bn', 1))
    ell(A, ena, 1.18, 1.08, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    dot(A, (ena[0] + 0.4, ena[1] - 0.3), P['gold'], 0.32)                                                      # gold ring
    if prop_n: prop_n(A, ena)
    _merge(L, A, OL)
    if outline_: outline(L, OL)
    CH.add(L)
    def U(p): return (piv[0] + (p[0] - piv[0]) * 1.2, piv[1] + (p[1] - piv[1]) * 1.2)
    return dict(hand_n=ena, hand_f=ea, mouth=U(mc), head=U(Fh(1.6, 18.6)), top=U(Fh(0.4, 23.6)), lap=H(3.0, 9.6))


# ======================================================================================= PUSYA (toy terrier, frontal)
PC = dict(fur=(220, 176, 120), fur_hi=(244, 210, 160), fur_sh=(180, 132, 84), pink=(240, 160, 168), nose=(34, 26, 28),
          knit=(206, 40, 92), knit_hi=(238, 90, 132), knit_sh=(150, 22, 64), zig=(255, 246, 236), white=(250, 248, 240),
          iris=(70, 40, 24), pom=(255, 246, 236))


def pusya(CH, cam, t=0.0, mouth_=0.0, expr='deadpan', look=(0.0, 0.0), shiver=1.0, sweater=True, ball=0.0, outline_=True,
          blink=True, ears_down=False):
    """frontal sitting toy terrier, anchor = floor point under the body. ~8 units tall incl. ears.
    expr: deadpan | smug | shock | sleepy.  shiver: tremble amount. ball: 0..1 swelling into a ball (E03)."""
    P = PC
    jx = 0.07 * shiver * math.sin(t * 61.0) + 0.04 * shiver * math.sin(t * 37.0)
    def Q(x, h): return H(x + jx, h)
    L = Layer(cam)
    A = Layer(cam)
    for sx in (-1, 1):                                                                                        # hind paws + thin front legs
        ell(A, Q(sx * 1.3, 0.35), 0.75, 0.4, P['fur'], 0, P['fur_hi'], P['fur_sh'])
        cap(A, Q(sx * 0.55, 2.2), Q(sx * 0.6, 0.25), 0.3, 0.26, P['fur'], P['fur_hi'], P['fur_sh'])
        ell(A, Q(sx * 0.62, 0.22), 0.38, 0.24, P['fur'], 0, P['fur_hi'], None)
    cap(A, Q(1.6, 1.0), Q(2.5, 2.2), 0.22, 0.12, P['fur'])                                                     # rat tail
    _merge(L, A, OL)
    B = Layer(cam)
    bw = 1.75 + 1.8 * ball
    if sweater:
        ellt(B, Q(0, 2.45 + ball * 0.6), bw, 1.9 + 1.3 * ball, (P['knit'], P['knit_hi'], P['knit_sh']))
        mk = band_mask(B, Q(0, 2.6), 0.42, bow=0.3, width=bw)
        recolor(B, mk, [(P['knit'], P['knit_sh'])])
        for i in range(5):                                                                                    # white zigzag band
            x0 = -bw * 0.9 + i * bw * 0.45
            cap(B, Q(x0, 2.2), Q(x0 + bw * 0.22, 2.55), 0.12, 0.12, P['zig'])
            cap(B, Q(x0 + bw * 0.22, 2.55), Q(x0 + bw * 0.45, 2.2), 0.12, 0.12, P['zig'])
        cap(B, Q(-1.2, 4.0), Q(1.2, 4.0), 0.45, 0.45, P['knit_hi'], None, P['knit'])                           # ribbed collar
        ell(B, Q(0.75, 3.75), 0.42, 0.42, P['pom'])                                                           # pompon tie
        cap(B, Q(0.3, 3.95), Q(0.7, 3.6), 0.08, 0.08, P['pom'])
    else:
        ellt(B, Q(0, 2.4), bw, 1.9 + 1.3 * ball, (P['fur'], P['fur_hi'], P['fur_sh']))
    _merge(L, B, OL)
    Hd = Layer(cam)
    hc = Q(0, 5.4)
    for sx in (-1, 1):                                                                                        # giant radar ears
        if ears_down:                                                                                         # ears pressed flat (too loud)
            poly(Hd, [Q(sx * 0.9, 6.5), Q(sx * 1.6, 5.3), Q(sx * 3.6, 4.6)], P['fur'])
            poly(Hd, [Q(sx * 1.1, 6.2), Q(sx * 1.6, 5.5), Q(sx * 3.2, 4.85)], P['pink'])
            continue
        poly(Hd, [Q(sx * 0.7, 6.3), Q(sx * 1.75, 5.5), Q(sx * 3.2, 9.0)], P['fur'])
        poly(Hd, [Q(sx * 1.0, 6.25), Q(sx * 1.65, 5.85), Q(sx * 2.85, 8.4)], P['pink'])
    ell(Hd, hc, 1.7, 1.55, P['fur'], 0, None, P['fur_sh'], th_sh=-0.72)                                              # apple head
    ell(Hd, Q(0, 4.55), 0.85, 0.62, P['fur_hi'])                                                              # muzzle
    bl = blink and (t % 3.9) < 0.09
    e_ex = {'shock': 'shock', 'smug': 'squint', 'sleepy': 'squint'}.get(expr, 'normal')
    for sx in (-1, 1):                                                                                        # bulging eyes, slightly apart
        c = Q(sx * 0.82, 5.55)
        ell(Hd, (c[0], c[1] + 0.05), 0.82, 0.8, P['fur_sh'])
        eye(Hd, c, 0.68, e_ex, (look[0] + sx * 0.25, look[1]), white=P['white'], iris=P['iris'], blink=bl, bulge=1.0,
            lid=P['fur_sh'] if expr in ('deadpan', 'sleepy') else None)
        if expr in ('deadpan', 'sleepy') and not bl:                                                           # heavy unimpressed lids
            lt = c[1] - 0.68 + (0.55 if expr == 'deadpan' else 0.8)
            E = Layer(Hd.cam); ell(E, c, 0.7, 0.77, P['fur'])                                                  # lid clipped to the eyeball
            Y = Layer(Hd.cam); poly(Y, [(c[0] - 0.9, c[1] - 1.0), (c[0] + 0.9, c[1] - 1.0), (c[0] + 0.9, lt), (c[0] - 0.9, lt)], P['fur'])
            mk = E.m & Y.m
            Hd.col[mk] = P['fur_hi']; Hd.m |= mk
            ln_ = Layer(Hd.cam); cap(ln_, (c[0] - 0.72, lt), (c[0] + 0.72, lt), 0.1, 0.1, P['fur_sh'])
            mk2 = ln_.m & E.m; Hd.col[mk2] = P['fur_sh']
    for sx in (-1, 1):
        cap(Hd, Q(sx * 0.4, 6.5), Q(sx * 1.2, 6.65), 0.08, 0.08, P['fur_sh'])                                   # worried brow folds
    ell(Hd, Q(0, 4.85), 0.32, 0.24, P['nose']); dot(Hd, Q(-0.1, 4.92), (120, 110, 110), 0.08)
    mm = max(mouth_, 0.5 if expr == 'shock' else 0.0)
    mc = Q(0, 4.3)
    if mm > 0.08:
        mouth(Hd, mc, 0.55, mm, inner=(90, 20, 30), teeth=(255, 255, 255))
    else:
        cap(Hd, Q(-0.35, 4.35), Q(0, 4.25), 0.07, 0.07, P['fur_sh']); cap(Hd, Q(0, 4.25), Q(0.35, 4.35), 0.07, 0.07, P['fur_sh'])
    _merge(L, Hd, OL)
    if outline_: outline(L, OL)
    CH.add(L)
    return dict(head=hc, mouth=mc, top=Q(0, 8.9))


# ======================================================================================= SVETA (wife)
SC = dict(skin=(240, 198, 170), skin_hi=(252, 222, 198), skin_sh=(204, 156, 130), hair=(178, 134, 78), hair_hi=(214, 172, 110),
          hair_sh=(132, 96, 54), hood=(140, 124, 170), hood_hi=(172, 156, 200), hood_sh=(104, 90, 134), jeans=(64, 92, 150),
          jeans_hi=(90, 122, 182), jeans_sh=(44, 64, 108), shoe=(236, 236, 236), shoe_sh=(176, 176, 180), lip=(196, 104, 110),
          scr=(226, 60, 60))
SPOSE = dict(
    stand=dict(n=(2.4, 10.8), f=(-2.0, 11.0), bn=1, bf=-1, nleg=(0.04, 0.0), fleg=(-0.04, 0.0)),
    keys=dict(n=(4.8, 16.6), f=(-2.0, 11.0), bn=1, bf=-1, nleg=(0.04, 0.0), fleg=(-0.04, 0.0)),     # shows the keys
    climb=dict(n=(3.0, 12.0), f=(-2.4, 11.0), bn=1, bf=-1, nleg=(0.75, -0.4), fleg=(-0.2, 0.15)),   # on the stairs, near leg up
    shrug=dict(n=(4.0, 15.6), f=(-3.6, 15.6), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
)


def sveta(CH, cam, pose=None, t=0.0, mouth_=0.0, expr='tired', look=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
          blink=True, outline_=True):
    """expr: tired | guilty | sad | smile | shock"""
    pose = pose or SPOSE['stand']
    P = SC
    br = 0.12 * math.sin(t * 2.3)
    sh_n, sh_f = H(1.6, 18.6 + br), H(-1.5, 18.8 + br)
    hp_n, hp_f = H(0.8, 10.8), H(-0.7, 10.8)
    hood = (P['hood'], P['hood_hi'], P['hood_sh']); jeans = (P['jeans'], P['jeans_hi'], P['jeans_sh'])
    L = Layer(cam)
    for hp, lg, r in ((hp_f, pose['fleg'], 1.05), (hp_n, pose['nleg'], 1.1)):
        A = Layer(cam)
        k, e = _limb(A, hp, *lg, 5.4, 5.1, r, r * 0.78, *jeans)
        ellt(A, (e[0] + 0.85, e[1] + 0.4), 1.5, 0.6, (P['shoe'], P['shoe'], P['shoe_sh']))
        _merge(L, A, OL)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(*pose['f'])
    ka, ea = _limb(A, sh_f, 0, 0, 3.8, 3.5, 1.0, 0.82, *hood, target=tf, bend=pose.get('bf', -1))
    ell(A, ea, 0.85, 0.8, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_f: prop_f(A, ea)
    _merge(L, A, OL)
    T = Layer(cam)
    ellt(T, H(0.3, 14.6 + br * 0.5), 2.9, 4.4, hood)
    cap(T, H(-1.6, 19.2 + br), H(1.8, 19.2 + br), 0.9, 0.9, P['hood_sh'])                                      # hood bunched at the neck
    poly(T, [H(0.4, 13.2), H(2.8, 13.2), H(2.6, 11.4), H(0.6, 11.4)], P['hood_sh'])                             # front pocket
    cap(T, H(0.9, 18.4), H(1.1, 16.6), 0.08, 0.08, (236, 236, 240)); cap(T, H(1.6, 18.4), H(1.8, 16.8), 0.08, 0.08, (236, 236, 240))
    _merge(L, T, OL)
    Hd = Layer(cam)
    hx = 0.6
    def Fh(x, h): return H(hx + x - 0.6, h + br)
    cap(Hd, Fh(0.3, 19.0), Fh(0.6, 20.6), 0.85, 0.85, P['skin'], P['skin_hi'], P['skin_sh'])
    cap(Hd, Fh(-1.6, 23.8), Fh(-3.0, 20.4), 0.95, 0.6, P['hair'], P['hair_hi'], P['hair_sh'])                  # ponytail
    ell(Hd, Fh(-1.5, 23.7), 0.55, 0.55, P['scr'])                                                              # scrunchie
    ell(Hd, Fh(0.7, 22.4), 2.35, 2.65, P['skin'], 0, None, P['skin_sh'], th_sh=-0.72)
    ell(Hd, Fh(0.4, 24.1), 2.5, 1.35, P['hair'], 0.05, P['hair_hi'], P['hair_sh'])
    cap(Hd, Fh(-1.3, 23.6), Fh(-1.6, 21.2), 0.7, 0.5, P['hair'])
    cap(Hd, Fh(2.4, 24.0), Fh(2.9, 22.2), 0.35, 0.15, P['hair'])                                                 # loose strand
    ell(Hd, Fh(-1.1, 22.2), 0.55, 0.8, P['skin'], 0, None, P['skin_sh'])
    eyes = [(Fh(1.1, 22.6), 0.5), (Fh(2.2, 22.55), 0.56)]
    bl = blink and (t % 3.6) < 0.1
    ex = {'shock': 'shock', 'smile': 'normal'}.get(expr, 'normal')
    for c, r in eyes:
        ell(Hd, (c[0], c[1] + r * 1.0), r * 0.95, r * 0.32, (214, 168, 170))                                    # tired eye bags
        eye(Hd, c, r, ex, (look, 0.0), iris=(90, 110, 150), lid=P['skin_sh'], lash=(40, 28, 26), blink=bl)
    bt = {'guilty': -0.5, 'tired': -0.3, 'sad': -0.6, 'shock': -0.4}.get(expr, 0.0)
    for k, (c, r) in enumerate(eyes):
        s_ = 1 if k == 0 else -1
        b = c[1] - r - 0.45
        cap(Hd, (c[0] - 0.5, b - s_ * bt * 0.28), (c[0] + 0.5, b + s_ * bt * 0.28), 0.16, 0.13, P['hair_sh'])
    poly(Hd, [Fh(2.8, 22.0), Fh(3.4, 21.3), Fh(2.8, 21.15)], P['skin_sh'])
    mc = Fh(2.05, 20.75 - 0.2 * mouth_)
    mouth(Hd, mc, 0.56, mouth_, 'sad' if expr in ('guilty', 'sad', 'tired') else 'happy' if expr == 'smile' else 'normal', lip=P['lip'])
    _merge(L, Hd, OL)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(*pose['n'])
    kna, ena = _limb(A, sh_n, 0, 0, 3.8, 3.5, 1.02, 0.84, *hood, target=tn, bend=pose.get('bn', 1))
    ell(A, ena, 0.88, 0.82, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_n: prop_n(A, ena)
    _merge(L, A, OL)
    if outline_: outline(L, OL)
    CH.add(L)
    return dict(hand_n=ena, hand_f=ea, mouth=mc, head=Fh(1.2, 22.4), top=Fh(0.4, 25.3))


# ======================================================================================= hand props (unit coords)
def phone(L, h, ang=-1.9):
    """smartphone at the ear / in the hand"""
    d = (math.cos(ang), math.sin(ang))
    a = (h[0] - d[0] * 0.2, h[1] - d[1] * 0.2); b = (h[0] + d[0] * 1.6, h[1] + d[1] * 1.6)
    cap(L, a, b, 0.48, 0.48, (36, 36, 44)); cap(L, a, b, 0.32, 0.32, (70, 110, 170))


def keys(L, h, t=0.0):
    """bunch of keys hanging from a finger (the tag «КВАРТИРАНТАМ» is a decal drawn by the episode)"""
    sw = 0.25 * math.sin(t * 6)
    ell(L, (h[0], h[1] + 0.5), 0.5, 0.5, (190, 190, 196)); ell(L, (h[0], h[1] + 0.5), 0.3, 0.3, (1, 1, 1))
    L.m[(L.col == 1).all(-1)] = False
    for i, (dx, ln) in enumerate(((-0.4, 1.8), (0.1, 2.1), (0.5, 1.6))):
        a = (h[0] + dx * 0.4, h[1] + 0.9); b = (h[0] + dx + sw, h[1] + 0.9 + ln)
        cap(L, a, b, 0.2, 0.16, (214, 184, 90) if i == 1 else (196, 198, 206))
        ell(L, a, 0.32, 0.32, (214, 184, 90) if i == 1 else (196, 198, 206))
    cap(L, (h[0], h[1] + 0.9), (h[0] + 0.9 + sw, h[1] + 2.6), 0.08, 0.08, (236, 230, 210))                       # tag string


def bag_handle(L, h):
    """the handle loop of a plaid bag held in the hand (the bag body is a world prop)"""
    cap(L, (h[0] - 0.6, h[1] + 0.2), (h[0] + 0.6, h[1] + 0.2), 0.25, 0.25, (40, 50, 120))


# ======================================================================================= world props (world px via v.wcam())
PLAID = [(214, 40, 48), (40, 70, 168), (244, 244, 236)]


def chelnok(L, x, y, w, h, tilt=0.0, seed=0, burst=0.0):
    """plaid «челнок» bag standing on the floor point (x, y) (bottom centre), w x h world px; burst 0..1 zipper open with jars"""
    ca, sa = math.cos(tilt), math.sin(tilt)
    def R(px, py): return (x + px * ca - py * sa, y + px * sa + py * ca)
    A = Layer(L.cam)
    poly(A, [R(-w / 2, 0), R(w / 2, 0), R(w / 2 * 0.96, -h), R(-w / 2 * 0.96, -h)], PLAID[2])
    keep = A.m.copy()
    cam = A.cam
    sc = cam.sc
    cx, cy = cam.p(x, y)
    import scene as S
    X = S.XX - cx; Y = S.YY - cy
    u = (X * ca + Y * sa) / sc; vv = (-X * sa + Y * ca) / sc
    cell = max(6.0, w / 6.0)
    gx = (np.floor(u / cell + seed * 0.37).astype(int)) % 3; gy = (np.floor(vv / cell).astype(int)) % 3
    A.col[keep & (gx == 0)] = PLAID[0]
    A.col[keep & (gy == 0)] = PLAID[1]
    A.col[keep & (gx == 0) & (gy == 0)] = (120, 30, 70)
    fine = keep & (((np.floor(u / (cell / 3)).astype(int)) % 3 == 1) & ((np.floor(vv / (cell / 3)).astype(int)) % 3 == 1))
    A.col[fine] = (250, 250, 240)
    cap(A, R(-w * 0.32, -h), R(-w * 0.18, -h - h * 0.32), 2.0, 2.0, (40, 50, 120))                             # handles
    cap(A, R(-w * 0.18, -h - h * 0.32), R(-w * 0.04, -h), 2.0, 2.0, (40, 50, 120))
    cap(A, R(w * 0.04, -h), R(w * 0.18, -h - h * 0.32), 2.0, 2.0, (40, 50, 120))
    cap(A, R(w * 0.18, -h - h * 0.32), R(w * 0.32, -h), 2.0, 2.0, (40, 50, 120))
    cap(A, R(-w / 2 * 0.9, -h + 2), R(w / 2 * 0.9, -h + 2), 1.4, 1.4, (60, 60, 70))                            # zipper
    if burst > 0:
        for i in range(5):
            jx = -w * 0.36 + i * w * 0.18
            jy = -h - 4 - burst * (h * 0.18 + 5 * (i % 2))
            F.ell(A, R(jx, jy), w * 0.075, h * 0.16, (150, 196, 120), 0, (200, 236, 170), (100, 150, 80))
            cap(A, R(jx - w * 0.06, jy - h * 0.15), R(jx + w * 0.06, jy - h * 0.15), 1.8, 1.8, (196, 196, 206))
    outline(A, OL)
    _merge(L, A, None)


def carpet_roll(L, x, y, length, r, ang=-0.25):
    """rolled-up wall carpet leaning: base at (x, y)"""
    d = (math.sin(ang), -math.cos(ang))
    a = (x, y); b = (x + d[0] * length, y + d[1] * length)
    A = Layer(L.cam)
    cap(A, a, b, r, r, (170, 40, 40), (206, 70, 60), (120, 24, 30))
    mk = band_mask(A, ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), r * 0.7, ang=ang)
    recolor(A, mk, [((170, 40, 40), (226, 170, 70)), ((206, 70, 60), (240, 200, 110)), ((120, 24, 30), (176, 120, 40))])
    ell(A, b, r * 0.95, r * 0.95, (120, 24, 30)); ell(A, b, r * 0.55, r * 0.55, (226, 170, 70)); ell(A, b, r * 0.2, r * 0.2, (90, 20, 24))
    outline(A, OL)
    _merge(L, A, None)


def ficus(L, x, y, s=1.0):
    A = Layer(L.cam)
    poly(A, [(x - 16 * s, y), (x + 16 * s, y), (x + 20 * s, y - 26 * s), (x - 20 * s, y - 26 * s)], (186, 92, 52))
    cap(A, (x - 22 * s, y - 26 * s), (x + 22 * s, y - 26 * s), 3 * s, 3 * s, (210, 116, 70))
    cap(A, (x, y - 26 * s), (x + 2 * s, y - 80 * s), 2.2 * s, 1.6 * s, (110, 80, 50))
    for i in range(11):
        a = i * 2.4
        lx = x + math.sin(a) * (14 + 10 * (i % 3)) * s; ly = y - (40 + i * 5.5) * s
        F.ell(A, (lx, ly), 9 * s, 5 * s, (60, 140, 70), a, (100, 186, 100), (36, 96, 50))
    outline(A, OL)
    _merge(L, A, None)


def tv_rubin(L, x, y, s=1.0):
    """old box TV standing on the floor point (x, y)"""
    A = Layer(L.cam)
    poly(A, [(x - 34 * s, y), (x + 34 * s, y), (x + 34 * s, y - 56 * s), (x - 34 * s, y - 56 * s)], (110, 74, 48))
    poly(A, [(x - 28 * s, y - 8 * s), (x + 14 * s, y - 8 * s), (x + 14 * s, y - 50 * s), (x - 28 * s, y - 50 * s)], (60, 70, 76))
    F.ell(A, (x - 8 * s, y - 36 * s), 12 * s, 6 * s, (110, 124, 132))
    for k in range(3): F.ell(A, (x + 24 * s, y - (44 - k * 12) * s), 3.5 * s, 3.5 * s, (200, 190, 170))
    cap(A, (x - 10 * s, y - 56 * s), (x - 26 * s, y - 84 * s), 1.2, 1.2, (170, 170, 176))                      # antenna
    cap(A, (x + 6 * s, y - 56 * s), (x + 22 * s, y - 86 * s), 1.2, 1.2, (170, 170, 176))
    outline(A, OL)
    _merge(L, A, None)


def armchair(L, x, y, s=1.0, part='back'):
    """old brown armchair, 3/4 view facing the camera-right. part: back (backrest + seat, drawn behind the sitter) | front (near
    armrest drawn over the sitter's hip). (x, y) = floor point under the seat front centre."""
    A = Layer(L.cam)
    col = ((134, 74, 52), (170, 104, 74), (96, 50, 36))
    if part == 'back':
        poly(A, [(x - 70 * s, y - 60 * s), (x + 40 * s, y - 70 * s), (x + 34 * s, y - 236 * s), (x - 74 * s, y - 226 * s)], col[0])
        F.ell(A, (x - 18 * s, y - 228 * s), 56 * s, 20 * s, col[0], 0.0, col[1], col[2])
        for k in range(3):                                                                      # button tufts
            F.ell(A, (x - 18 * s, y - (200 - k * 40) * s), 4 * s, 4 * s, col[2])
        poly(A, [(x - 70 * s, y - 64 * s), (x + 64 * s, y - 70 * s), (x + 70 * s, y - 40 * s), (x - 64 * s, y - 34 * s)], col[1])
        poly(A, [(x - 64 * s, y - 34 * s), (x + 70 * s, y - 40 * s), (x + 66 * s, y), (x - 60 * s, y + 4 * s)], col[2])
        F.ell(A, (x - 90 * s, y - 70 * s), 18 * s, 40 * s, col[0], 0, col[1], col[2])                         # far armrest
        F.ell(A, (x - 22 * s, y - 206 * s), 34 * s, 16 * s, (246, 242, 230))                                  # crocheted doily
        for k in range(8):
            a = k * 0.785
            F.ell(A, (x - 22 * s + math.cos(a) * 30 * s, y - 206 * s + math.sin(a) * 13 * s), 5 * s, 4 * s, (246, 242, 230))
        F.ell(A, (x - 22 * s, y - 206 * s), 18 * s, 8 * s, (226, 220, 206))
        for sx in (-50, 50):
            cap(A, (x + sx * s, y), (x + sx * s * 1.05, y + 12 * s), 3 * s, 2.5 * s, (70, 40, 26))
    else:
        return
    outline(A, OL)
    _merge(L, A, None)


def campbed(L, x, y, w, s=1.0):
    """folding camp bed (раскладушка) seen from the side: (x, y) floor centre"""
    A = Layer(L.cam)
    for sx in (-1, 1):
        cap(A, (x + sx * w * 0.45, y), (x - sx * w * 0.3, y - 34 * s), 1.8 * s, 1.8 * s, (170, 176, 186))
    cap(A, (x - w / 2, y - 34 * s), (x + w / 2, y - 34 * s), 2.4 * s, 2.4 * s, (170, 176, 186))
    poly(A, [(x - w / 2, y - 36 * s), (x + w / 2, y - 36 * s), (x + w / 2 - 6 * s, y - 26 * s), (x - w / 2 + 6 * s, y - 26 * s)],
         (60, 110, 80))
    for k in range(9):
        xx = x - w / 2 + 8 * s + k * (w - 16 * s) / 8
        cap(A, (xx, y - 35 * s), (xx + 2 * s, y - 27 * s), 0.8 * s, 0.8 * s, (190, 196, 206))
    outline(A, OL)
    _merge(L, A, None)
