"""Cast of «Agent Dibs» (US channel): Dibs, Brad, Terry & Gary (the «villains»), Mrs. Wozniak, Deb (bust), Marty the rat, silhouettes.
Rig conventions as in props/us_cast.py: anchor (1000,1000) = floor point under the character, H(x, h) -> (1000 + x, 1000 - h),
+x = facing direction (ACam.flip mirrors), 3-tone shading from a top-left light; heroes get scene light later (stage.Light).
One generic humanoid rig (`human`) + one generic 3/4 head (`head`), characters differ by spec dicts and small callbacks."""
import math
import numpy as np
import scene as S
from scene import Layer
from props.folk import H, cap, ell, ellt, dot, poly, outline, _limb, _merge, _D, OL
from props.us_props import ltext, rect


def T3(base, k=0.30):
    """(base, hi, sh) tone triple derived from a base colour"""
    return (base, tuple(min(255, int(c + (255 - c) * k)) for c in base), tuple(int(c * (1 - k * 1.25)) for c in base))


def lerpc(a, b, k):
    return tuple(int(x + (y - x) * k) for x, y in zip(a, b))


# ---------------------------------------------------------------------------------------------------- poses
POSE = dict(
    # arms as IK hand targets (x, h) in body units (+x = facing); bn/bf = elbow bend side; legs = (thigh angle, shin angle)
    stand=dict(n=(3.6, 10.2), f=(-3.0, 10.4), bn=1, bf=-1, nleg=(0.06, 0.0), fleg=(-0.06, 0.0)),
    hold=dict(n=(6.6, 14.4), f=(5.6, 14.6), bn=1, bf=1, nleg=(0.10, 0.0), fleg=(-0.10, 0.0)),
    shout=dict(n=(6.0, 25.6), f=(-4.6, 25.0), bn=1, bf=-1, nleg=(0.25, 0.0), fleg=(-0.25, 0.0)),
    cheer=dict(n=(8.6, 26.0), f=(-3.0, 10.6), bn=-1, bf=-1, nleg=(0.16, 0.0), fleg=(-0.16, 0.0)),
    point=dict(n=(10.6, 17.8), f=(-3.0, 10.6), bn=1, bf=-1, nleg=(0.14, 0.0), fleg=(-0.14, 0.0)),
    shrug=dict(n=(5.4, 17.0), f=(-4.6, 17.0), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
    hips=dict(n=(2.8, 11.0), f=(-2.8, 11.0), bn=-1, bf=1, nleg=(0.20, 0.0), fleg=(-0.20, 0.0)),
    slump=dict(n=(2.6, 8.4), f=(-2.4, 8.4), bn=1, bf=-1, nleg=(0.03, 0.0), fleg=(-0.03, 0.0)),
    sit=dict(n=(4.8, 11.4), f=(3.6, 11.6), bn=1, bf=1, nleg=(1.5, 0.0), fleg=(1.4, 0.0)),
    ears=dict(n=(2.4, 23.6), f=(-1.6, 23.4), bn=-1, bf=1, nleg=(0.06, 0.0), fleg=(-0.06, 0.0)),            # hands over the ears
    cover=dict(n=(3.2, 21.4), f=(-1.0, 21.0), bn=-1, bf=1, nleg=(0.16, 0.0), fleg=(-0.16, 0.0)),           # hands over the mouth
    wave=dict(n=(5.6, 23.6), f=(-3.0, 10.6), bn=-1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
    hat=dict(n=(3.8, 14.0), f=(3.0, 14.2), bn=1, bf=1, nleg=(0.06, 0.0), fleg=(-0.06, 0.0)),               # hat held at the belly (sorry!)
    reach=dict(n=(9.6, 16.4), f=(-2.6, 10.8), bn=1, bf=-1, nleg=(0.22, 0.0), fleg=(-0.22, 0.0)),
    arms_up=dict(n=(4.4, 28.6), f=(-3.6, 28.2), bn=1, bf=-1, nleg=(0.1, 0.0), fleg=(-0.1, 0.0)),
    hang=dict(n=(3.6, 30.0), f=(-2.0, 12.0), bn=-1, bf=1, nleg=(0.5, 0.2), fleg=(-0.2, 0.6)),             # dangling from one hand overhead
    drive=dict(n=(5.6, 14.4), f=(5.2, 15.6), bn=1, bf=1, nleg=(1.5, 0.0), fleg=(1.4, 0.0)),
    brace=dict(n=(7.8, 15.0), f=(6.9, 15.4), bn=1, bf=1, nleg=(0.45, 0.0), fleg=(-0.45, 0.0)),
)


def walk(t, speed=8.0, amp=0.42, carry=False):
    s = math.sin(t * speed)
    p = dict(n=(3.6 - 2.0 * s, 10.6 + 0.4 * abs(s)), f=(-3.0 + 2.0 * s, 10.6), bn=1, bf=-1,
             nleg=(amp * s, 0.28 * max(0, -s)), fleg=(-amp * s, 0.28 * max(0, s)))
    if carry: p.update(n=(6.6, 14.4 + 0.3 * abs(s)), f=(5.6, 14.6 + 0.3 * abs(s)), bn=1, bf=1)
    return p


def blend(a, b, k):
    o = dict(a if k < 0.5 else b)
    for kk in ('n', 'f', 'nleg', 'fleg'):
        o[kk] = (a[kk][0] + (b[kk][0] - a[kk][0]) * k, a[kk][1] + (b[kk][1] - a[kk][1]) * k)
    return o


# ---------------------------------------------------------------------------------------------------- expressions
# eo = eye openness, pu = pupil size, bt = brow tilt (+ angry / - worried), bl = brow lift, mo = base mouth open, mc = mouth curve (+ smile),
# teeth = show teeth when closed, lid = heavy upper lid, shut = eyes shut (happy arcs if mc>0)
EXPR = dict(
    normal=dict(eo=1.0, pu=0.6, bt=0.10, bl=0.0, mo=0.0, mc=0.0),
    shout=dict(eo=1.25, pu=0.5, bt=0.45, bl=0.0, mo=0.9, mc=0.0),
    angry=dict(eo=0.9, pu=0.55, bt=0.65, bl=0.0, mo=0.25, mc=-0.5),
    smug=dict(eo=0.7, pu=0.6, bt=0.25, bl=0.0, mo=0.0, mc=0.7, lid=0.4),
    deadpan=dict(eo=0.75, pu=0.6, bt=0.0, bl=0.0, mo=0.0, mc=0.0, lid=0.5),
    shock=dict(eo=1.35, pu=0.38, bt=-0.6, bl=0.5, mo=0.7, mc=0.0),
    cheer=dict(eo=1.1, pu=0.6, bt=-0.2, bl=0.35, mo=0.8, mc=0.8),
    smile=dict(eo=1.0, pu=0.62, bt=-0.2, bl=0.2, mo=0.0, mc=1.0, teeth=True),
    grin=dict(eo=1.05, pu=0.6, bt=-0.25, bl=0.3, mo=0.35, mc=1.0, teeth=True),
    nervous=dict(eo=1.15, pu=0.45, bt=-0.55, bl=0.25, mo=0.0, mc=-0.25),
    sad=dict(eo=0.95, pu=0.62, bt=-0.7, bl=0.1, mo=0.0, mc=-0.7),
    cry=dict(eo=1.0, pu=0.7, bt=-0.8, bl=0.2, mo=0.3, mc=-0.8, tears=True),
    stunned=dict(eo=1.2, pu=0.36, bt=-0.2, bl=0.3, mo=0.12, mc=0.0),
    content=dict(eo=0.0, pu=0.6, bt=-0.3, bl=0.2, mo=0.0, mc=0.9, shut=True),
    wistful=dict(eo=0.85, pu=0.7, bt=-0.5, bl=0.15, mo=0.0, mc=0.35, look_up=True),
    sly=dict(eo=0.75, pu=0.6, bt=0.45, bl=0.0, mo=0.0, mc=0.6, lid=0.3),
    panic=dict(eo=1.4, pu=0.34, bt=-0.7, bl=0.6, mo=0.85, mc=-0.1),
    ope=dict(eo=1.25, pu=0.42, bt=-0.6, bl=0.5, mo=0.45, mc=0.0, round_mouth=True),
    blank=dict(eo=0.9, pu=0.5, bt=0.0, bl=0.0, mo=0.0, mc=-0.1),
    sleepy=dict(eo=0.45, pu=0.6, bt=0.0, bl=0.0, mo=0.0, mc=0.0, lid=0.7),
)


def head(Hd, F, HS, expr, t, mouth, look, blink=True, shades=False, sweat=0.0, blush=0.0, **kw):
    """generic 3/4 head facing +x. F(x, y) maps head-local coordinates (origin = head centre, ~3 units radius) to layer coords.
    HS: skin(3 tones), skull(rx, ry), jaw(cx, cy, rx, ry), nose(r, col), eye(iris col, scale), brow(col, thick), stache(col, size) | None,
    lip, teeth, back(Hd, F), front(Hd, F, ctx) callbacks."""
    X = EXPR.get(expr, EXPR['normal'])
    sk, skh, sks = HS['skin']
    if blush > 0:
        sk, skh, sks = [lerpc(c, (250, 84, 76), blush) for c in HS['skin']]
    if 'back' in HS: HS['back'](Hd, F, ctx=kw)
    rx, ry = HS.get('skull', (2.95, 3.4))
    cx, cy, jrx, jry = HS.get('jaw', (1.15, -1.9, 2.5, 1.85))
    # neck + skull + jaw + chin + ear
    cap(Hd, F(-0.3, -4.0), F(-0.1, -2.0), 1.75, 1.75, sk, skh, sks)
    ell(Hd, F(0.0, 0.0), rx, ry, sk, -0.06, skh, sks)
    ell(Hd, F(cx, cy), jrx, jry, sk, 0.12, None, sks)
    ell(Hd, F(cx + 1.2, cy - 0.55), 1.2, 1.0, sk, 0.2, skh, None)
    ell(Hd, F(-1.75, -0.4), 0.65, 0.95, sk, 0, None, sks)
    ell(Hd, F(-1.7, -0.4), 0.3, 0.55, sks)
    if HS.get('sil'):
        if 'front' in HS: HS['front'](Hd, F, shades=shades, expr=expr, t=t, ctx=kw)
        return
    if 'cheeks' in HS: ell(Hd, F(*HS['cheeks'][:2]), HS['cheeks'][2], HS['cheeks'][3], HS['cheeks'][4])
    # eyes
    ex = 0.12 * look
    er = HS.get('eye', ((60, 110, 180), 1.0))
    es = er[1]
    eyes = [(F(0.65 + ex, 0.55), 0.56 * es), (F(2.05 + ex, 0.45), 0.7 * es)]
    bl_ = blink and (t % 3.3) < 0.11
    if shades:
        pass
    else:
        for k, (e_, r) in enumerate(eyes):
            if bl_ or X.get('shut'):
                if X.get('shut') and X['mc'] > 0.3:                                   # happy arcs ^ ^
                    cap(Hd, (e_[0] - r * 1.1, e_[1] + 0.12), (e_[0], e_[1] - 0.3), 0.15, 0.15, HS.get('lash', OL))
                    cap(Hd, (e_[0], e_[1] - 0.3), (e_[0] + r * 1.1, e_[1] + 0.12), 0.15, 0.15, HS.get('lash', OL))
                else:
                    cap(Hd, (e_[0] - r, e_[1] + 0.05), (e_[0] + r, e_[1] - 0.02), 0.14, 0.14, HS.get('lash', OL))
                continue
            rr = r * (1.0 + 0.3 * max(0.0, X['eo'] - 1.0) * 2)
            eo = max(0.25, min(1.2, X['eo']))
            ell(Hd, e_, rr * 1.12, rr * 1.12 * min(1.0, 0.55 + 0.45 * eo), HS.get('white', (248, 246, 240)))
            dy_ = 0.18 * rr if X.get('look_up') else 0.0
            pu = X['pu']
            dot(Hd, (e_[0] + 0.1 + ex, e_[1] + 0.04 - dy_), er[0], rr * (0.62 if pu > 0.5 else 0.5))
            dot(Hd, (e_[0] + 0.1 + ex, e_[1] + 0.04 - dy_), (24, 20, 22), rr * pu * 0.62)
            dot(Hd, (e_[0] + 0.02 + ex, e_[1] - 0.14 - dy_), (255, 255, 255), rr * 0.16)
            if X.get('lid'):
                lidk = X['lid']
                ell(Hd, (e_[0], e_[1] - rr * 0.55 + lidk * rr * 0.35), rr * 1.2, rr * (0.55 + lidk * 0.35), sk, 0, None, None)
                cap(Hd, (e_[0] - rr * 1.15, e_[1] - rr * 0.1 + lidk * rr * 0.1), (e_[0] + rr * 1.15, e_[1] - rr * 0.14 + lidk * rr * 0.1),
                    0.13, 0.13, sks)
            if X.get('tears'):
                ell(Hd, (e_[0] + 0.3, e_[1] + 0.3 + 1.6 * ((t * 1.5 + k * 0.3) % 1.0)), 0.25, 0.42, (170, 220, 255), 0, (230, 246, 255), None)
    # brows (layer y grows downward, so "up" is minus)
    bcol, bth = HS.get('brow', ((80, 54, 40), 0.34))
    for k, (e_, r) in enumerate(eyes):
        base = e_[1] - r - 0.72 - X['bl'] * 0.55 - (0.35 if shades else 0.0)
        s_ = 1 if k == 0 else -1
        bt = X['bt']
        cap(Hd, (e_[0] - 0.8, base - s_ * bt * 0.36), (e_[0] + 0.8, base + s_ * bt * 0.36), bth, bth * 0.9, bcol)
    # nose
    nr, ncol = HS.get('nose', (1.0, None))
    nsk = ncol or sk
    ell(Hd, F(3.15, -0.5), 1.05 * nr, 0.95 * nr, nsk, 0, lerpc(nsk, (255, 255, 255), 0.25), lerpc(nsk, (0, 0, 0), 0.25))
    dot(Hd, F(3.75, -0.8), lerpc(nsk, (0, 0, 0), 0.3), 0.16)
    # mouth
    m = max(mouth, X['mo'])
    mc_ = X['mc']
    mx, my = 2.35, -2.3
    lipc = HS.get('lip', (150, 62, 56))
    teeth = HS.get('teeth', (252, 250, 244))
    if X.get('round_mouth') and m > 0.05:
        ell(Hd, F(mx + 0.2, my), 0.75 + 0.3 * m, 0.9 + 0.6 * m, (104, 30, 34))
        ell(Hd, F(mx + 0.2, my - 0.5 * m), 0.4, 0.3, (200, 98, 100))
    elif m > 0.08 or (X.get('teeth') and mc_ > 0.5 and m > 0.04):
        w = 1.05 + 0.45 * m + 0.5 * max(0.0, mc_)
        ell(Hd, F(mx, my - 0.15 * m), w, 0.35 + 1.0 * m, (104, 30, 34))
        ell(Hd, F(mx + 0.05, my + 0.2 + 0.45 * m), w * 0.9, 0.28 + 0.12 * m, teeth)
        ell(Hd, F(mx + 0.15, my - 0.55 * m - 0.1), 0.6 + 0.3 * m, 0.22 + 0.28 * m, (200, 98, 100))
    else:
        if X.get('teeth') and mc_ > 0.5:
            ell(Hd, F(mx, my), 1.5, 0.5, lipc)
            ell(Hd, F(mx, my + 0.02), 1.32, 0.38, teeth)
            cap(Hd, F(mx - 1.2, my + 0.02), F(mx + 1.2, my + 0.02), 0.05, 0.05, (210, 214, 220))
        else:
            c0 = F(mx - 1.0, my - 0.15 * mc_ + 0.05); c1 = F(mx + 0.2, my - 0.35 * mc_ - 0.05 * (mc_ < 0)); c2 = F(mx + 1.5, my + 0.3 * mc_)
            cap(Hd, c0, c1, 0.17, 0.17, lipc)
            cap(Hd, c1, c2, 0.17, 0.14, lipc)
    if 'stache' in HS and HS['stache']:
        sc_, ssz = HS['stache']
        sy = my + 1.0 + 0.1 * m
        cap(Hd, F(mx - 0.7, sy), F(mx + 1.3, sy + 0.05), 0.3 * ssz, 0.26 * ssz, sc_)
        ell(Hd, F(mx + 0.3, sy - 0.1), 0.6 * ssz, 0.28 * ssz, sc_)
    if 'front' in HS: HS['front'](Hd, F, shades=shades, expr=expr, t=t, ctx=kw)
    if sweat > 0.05:
        for k, (x, h) in enumerate(((-0.9, 2.0), (3.0, 2.2), (-0.4, 1.2))):
            yy = h - sweat * 1.4 * ((t * 1.5 + k * 0.33) % 1.0)
            ell(Hd, F(x, yy), 0.24, 0.4, (170, 220, 255), 0, (230, 246, 255), None)


def human(CH, cam, K, pose=None, t=0.0, mouth=0.0, expr='normal', look=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
          lean=0.0, legs=True, blink=True, shades=False, sweat=0.0, blush=0.0, back=None, front=None, wob=0.0, soot=0.0, clip_h=None, **kw):
    """generic humanoid. K spec: skin, sleeve, pants (3-tone tuples), shoe, torso(T, bc, br, ln), shoulders, hips, hy, head spec HS,
    leg/arm lengths + radii, pelvis, boot(A, e, ang). back(L) draws things behind the body (e.g. a folded chair), front(L) over it."""
    pose = pose or POSE['stand']
    br = 0.18 * math.sin(t * 2.3) + wob
    sk = K['skin']
    L = Layer(cam)
    ln = lean
    shx, shy = K.get('shoulders', (3.0, 17.2))
    hpx, hpy = K.get('hips', (1.4, 8.8))
    sh_n, sh_f = H(shx + ln, shy + br), H(-shx + ln, shy + 0.2 + br)
    hp_n, hp_f = H(hpx, hpy), H(-hpx + 0.2, hpy)
    l1, l2 = K.get('leg_len', (4.3, 4.2))
    r1, r2 = K.get('leg_r', (1.7, 1.25))
    a1, a2 = K.get('arm_len', (3.8, 3.6))
    q1, q2 = K.get('arm_r', (1.5, 1.2))
    if back: back(L)

    def leg(A, hp, ang, side):
        k, e = _limb(A, hp, *ang, l1, l2, r1, r2, *K['skin'])
        d1 = _D(ang[0]); d2 = _D(ang[1])
        pc = K['pants']
        cap(A, hp, (k[0] + d1[0] * 0.4, k[1] + d1[1] * 0.4 + 0.2), r1 + 0.35, r1 + 0.1, *pc)
        cap(A, (k[0] - d1[0] * 0.2, k[1]), (e[0] - d2[0] * 0.2, e[1] - d2[1] * 0.2), r1 + 0.1, r2 + 0.2, *pc)
        K['boot'](A, e, ang)
        return k, e

    if legs:
        A = Layer(cam); leg(A, hp_f, pose['fleg'], -1); _merge(L, A)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(*pose['f'])
    ka, ea = _limb(A, sh_f, 0, 0, a1, a2, q1, q2 * 0.95, *K['sleeve'], target=tf, bend=pose.get('bf', -1))
    cap(A, ka, ea, q2 * 0.95, q2 * 0.9, *K['skin']) if K.get('bare_forearm') else None
    ellt(A, ea, 1.2, 1.12, K.get('glove', sk))
    if prop_f: prop_f(A, ea)
    _merge(L, A)
    A = Layer(cam)
    if legs:
        ellt(A, H(0.2, hpy + 0.6), K.get('pelvis', (3.9, 2.4))[0], K.get('pelvis', (3.9, 2.4))[1], K['pants'])
        leg(A, hp_n, pose['nleg'], 1)
    else:
        ellt(A, H(0.2, hpy + 0.6), K.get('pelvis', (3.9, 2.4))[0] + 0.3, K.get('pelvis', (3.9, 2.4))[1] + 0.6, K['pants'])
    _merge(L, A)
    T = Layer(cam)
    bc = H(1.0 + 0.3 * ln, hpy + 3.8 + br * 0.5)
    K['torso'](T, bc, br, ln)
    _merge(L, T)
    Hd = Layer(cam)
    hy = K.get('hy', 21.3)
    hx = 0.9 + ln * 1.3
    hsc = K.get('hsc', 1.0)
    def F(x, y): return H(hx + x * hsc, hy + y * hsc + br)
    head(Hd, F, K['HS'], expr, t, mouth, look, blink, shades, sweat, blush, **kw)
    _merge(L, Hd)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(*pose['n'])
    kna, ena = _limb(A, sh_n, 0, 0, a1, a2, q1 + 0.05, q2, *K['sleeve'], target=tn, bend=pose.get('bn', 1))
    ellt(A, ena, 1.28, 1.2, K.get('glove', sk))
    if prop_n: prop_n(A, ena)
    _merge(L, A)
    if front: front(L)
    if clip_h is not None:                                              # nothing is drawn below height clip_h (leaning out of a window)
        yc = int(round(cam.p(1000.0, 1000.0 - clip_h)[1]))
        if 0 <= yc < L.m.shape[0]: L.m[yc:, :] = False
        elif yc < 0: L.m[:] = False
    if soot > 0:                                                       # cartoon soot: everything goes black except eye whites and teeth
        m = L.m; col = L.col.astype(np.float32)
        tgt = m & ~(col.min(axis=2) > 232)
        col[tgt] = col[tgt] * (1 - soot) + np.array((28, 24, 24), np.float32) * soot
        L.col = np.clip(col, 0, 255).astype(np.uint8)
    outline(L, OL)
    CH.add(L)
    return dict(head=H(hx, hy + br), mouth=F(2.4, -2.25), hand_n=ena, hand_f=ea, belly=bc, shoulder=sh_n)


# ====================================================================================================== DIBS
DSK = T3((226, 150, 120), 0.28)
JACKET = T3((38, 58, 120), 0.28)
PANTS_BK = T3((30, 30, 40), 0.30)


def _dibs_back(L):
    """folded lawn chair strapped to his back (aluminium frame + green/white webbing), leaning behind the shoulders"""
    p0, p1 = (-3.4, 6.0), (-7.4, 25.5)
    dx, dy = p1[0] - p0[0], p1[1] - p0[1]; n = math.hypot(dx, dy); ux, uy = dx / n, dy / n; px_, py_ = -uy, ux
    for sgn in (-1, 1):                                                           # aluminium frame rails
        a = (p0[0] + px_ * 1.7 * sgn, p0[1] + py_ * 1.7 * sgn); b = (p1[0] + px_ * 1.7 * sgn, p1[1] + py_ * 1.7 * sgn)
        cap(L, H(*a), H(*b), 0.42, 0.42, (196, 202, 212), (240, 244, 250), (130, 136, 150))
    for k in range(9):                                                            # webbing slats
        c = (44, 160, 110) if k % 2 == 0 else (240, 240, 236)
        f = (k + 0.5) / 9
        ctr = (p0[0] + dx * f, p0[1] + dy * f)
        cap(L, H(ctr[0] - px_ * 1.7, ctr[1] - py_ * 1.7), H(ctr[0] + px_ * 1.7, ctr[1] + py_ * 1.7), 0.78, 0.78, c)
    cap(L, H(-3.0, 15.0), H(0.8, 17.4), 0.3, 0.3, (60, 44, 36))                    # strap


def _dibs_torso(T, bc, br, ln):
    P = JACKET
    ellt(T, bc, 5.9, 5.8, P)
    ellt(T, H(0.2 + ln, 16.8 + br), 5.0, 3.1, P)
    # white shirt collar + bow tie at the neck
    poly(T, [H(0.6 + ln, 18.8 + br), H(3.0 + ln, 17.4 + br), H(1.6 + ln, 15.6 + br), H(-0.2 + ln, 17.0 + br)], (246, 246, 248))
    poly(T, [H(1.5 + ln, 17.7 + br), H(0.4 + ln, 18.8 + br), H(0.4 + ln, 16.6 + br)], (200, 30, 50))
    poly(T, [H(1.7 + ln, 17.7 + br), H(2.9 + ln, 18.7 + br), H(2.9 + ln, 16.6 + br)], (200, 30, 50))
    dot(T, H(1.6 + ln, 17.7 + br), (150, 20, 36), 0.4)
    # zipper + BSB letters in yellow
    cap(T, H(2.5 + ln, 15.4), H(2.3 + ln, 6.8), 0.15, 0.15, (190, 196, 210))
    ltext(T, 'BSB', (2.2 + ln * 0.7, 12.8 + br * 0.5), 1.7, (255, 214, 60))
    # chest pocket flap, hem
    cap(T, H(-2.2 + ln, 6.6), H(3.6 + ln, 6.6), 0.35, 0.35, P[2])


def _dibs_boot(A, e, ang):
    ell(A, (e[0] + 0.9, e[1] + 0.1), 2.5, 1.45, (74, 62, 52), 0, (110, 96, 82), (44, 36, 30))
    cap(A, (e[0] - 0.9, e[1] - 1.3), (e[0] + 0.5, e[1] - 1.2), 1.1, 1.0, (222, 212, 190), (250, 244, 228), (170, 160, 140))   # fur trim
    ell(A, (e[0] + 0.9, e[1] + 1.1), 2.6, 0.5, (30, 26, 24))


def _dibs_back_head(Hd, F, ctx=None):
    """ushanka ear flaps (behind the head)"""
    ctx = ctx or {}
    fl = ctx.get('flap', 0.0)
    fur, fh, fs = T3((120, 104, 92), 0.28)
    ang = 0.35 * math.sin(fl)
    ell(Hd, F(-2.3, -0.8 + 1.2 * math.sin(fl * 1.7) * 0.3), 1.2, 2.5, fur, 0.1 + ang, fh, fs)


def _dibs_front_head(Hd, F, shades=False, expr='normal', t=0.0, ctx=None):
    ctx = ctx or {}
    fur, fh, fs = T3((120, 104, 92), 0.28)
    # ushanka: fur band above the brow, crown, near ear flap
    cap(Hd, F(-2.4, 3.1), F(3.2, 3.5), 0.95, 0.95, fur, fh, fs)
    ell(Hd, F(0.4, 4.3), 3.2, 1.5, fur, 0, fh, fs)
    fl = ctx.get('flap', 0.0)
    cap(Hd, F(-1.9, 2.4), F(-2.5 + 0.5 * math.sin(fl), -1.8 + 0.4 * math.cos(fl)), 1.15, 0.8, fur, fh, fs)
    # earpiece with a curly wire
    ell(Hd, F(-1.3, -0.1), 0.42, 0.5, (236, 226, 200), 0, (255, 250, 232), (190, 180, 150))
    for k in range(6):
        cap(Hd, F(-1.45 - 0.1 * k, -0.7 - 0.45 * k), F(-0.95 - 0.1 * k, -0.8 - 0.45 * k), 0.07, 0.07, (230, 230, 240))
    if shades:                                                                     # sunglasses at night
        for cx, cy, w, h in ((0.65, 0.55, 0.85, 0.7), (2.1, 0.45, 1.0, 0.8)):
            rect_h(Hd, F, cx, cy, w, h, (14, 14, 20))
            cap(Hd, F(cx - w * 0.5, cy + h * 0.2), F(cx - w * 0.1, cy + h * 0.5), 0.12, 0.1, (96, 120, 170))
        cap(Hd, F(1.4, 0.58), F(1.2, 0.55), 0.13, 0.13, (14, 14, 20))
        cap(Hd, F(-0.2, 0.55), F(-1.9, 0.5), 0.12, 0.12, (14, 14, 20))


def rect_h(Hd, F, cx, cy, w, h, c):
    poly(Hd, [F(cx - w, cy + h), F(cx + w, cy + h), F(cx + w, cy - h), F(cx - w, cy - h)], c)


DIBS_HS = dict(skin=DSK, skull=(3.35, 3.5), jaw=(1.1, -1.9, 2.8, 2.0), nose=(1.05, (222, 96, 90)), eye=((70, 96, 140), 1.35),
               brow=((60, 46, 40), 0.5), stache=((78, 58, 44), 1.15), lip=(150, 62, 56), cheeks=(1.6, -1.2, 1.1, 0.7, (232, 120, 110)),
               back=_dibs_back_head, front=_dibs_front_head)
DIBS = dict(skin=DSK, sleeve=JACKET, pants=PANTS_BK, torso=_dibs_torso, boot=_dibs_boot, HS=DIBS_HS, pelvis=(4.2, 2.6), hsc=1.0,
            glove=T3((40, 40, 48)))


def dibs(CH, cam, pose=None, t=0.0, mouth=0.0, expr='normal', look=0.0, shades=False, chair=True, flap=0.0, **kw):
    """Special Agent Dibs. expr: normal shout angry smug deadpan shock cheer stunned content cry sad sly panic; shades = sunglasses on;
    chair = folded lawn chair on the back; flap = ear-flap flutter phase"""
    return human(CH, cam, DIBS, pose, t, mouth, expr, look, shades=shades, back=_dibs_back if chair else None, flap=flap, **kw)


# ====================================================================================================== BRAD
BRSK = T3((244, 208, 178), 0.28)
FLEECE = T3((38, 176, 158), 0.28)
SHIRT_W = T3((240, 242, 246), 0.12)
KHAKI = T3((204, 178, 124), 0.28)


def _brad_torso(T, bc, br, ln):
    ellt(T, bc, 5.2, 5.5, SHIRT_W)                                               # long-sleeve shirt
    ellt(T, H(0.2 + ln, 16.6 + br), 4.6, 3.0, SHIRT_W)
    ellt(T, bc, 4.5, 5.3, FLEECE)                                                # sleeveless fleece vest
    ellt(T, H(0.5 + ln, 16.2 + br), 3.7, 2.8, FLEECE)
    cap(T, H(0.0 + ln, 18.3 + br), H(2.5 + ln, 17.2 + br), 1.0, 0.9, FLEECE[1], None, FLEECE[2])        # fleece collar
    cap(T, H(2.4 + ln, 17.4 + br), H(2.5 + ln, 14.0), 0.14, 0.14, (210, 240, 236))                         # quarter zip
    cap(T, H(1.8 + ln, 17.9 + br), H(3.0 + ln, 11.6), 0.2, 0.2, (210, 40, 52))                             # lanyard
    rect(T, H(3.0 + ln, 10.8), 1.9, 2.6, 0.0, (250, 250, 248))
    dot(T, H(3.0 + ln, 11.3), (60, 120, 200), 0.45)
    dot(T, H(1.4 + ln, 13.6), (22, 120, 108), 0.5)                               # tiny logo


def _brad_boot(A, e, ang):
    ell(A, (e[0] + 1.0, e[1] + 0.3), 2.2, 1.05, (250, 250, 252), 0, None, (206, 210, 216))
    ell(A, (e[0] + 1.0, e[1] + 1.0), 2.3, 0.4, (160, 166, 176))


def _brad_back(Hd, F, ctx=None):
    hc = T3((92, 62, 40), 0.3)
    ell(Hd, F(-1.0, 1.2), 3.2, 3.0, hc[0], 0.1, hc[1], hc[2])


def _brad_front(Hd, F, shades=False, expr='normal', t=0.0, ctx=None):
    hc = T3((92, 62, 40), 0.3)
    ell(Hd, F(0.2, 3.0), 3.4, 1.7, hc[0], 0.05, hc[1], hc[2])                    # volume on top
    cap(Hd, F(-1.6, 2.2), F(3.4, 2.7), 0.7, 0.45, hc[0], hc[1], hc[2])           # side-swept fringe
    cap(Hd, F(0.6, 3.6), F(3.0, 2.9), 0.28, 0.2, (190, 150, 110))                # gel shine
    ell(Hd, F(-1.35, -0.1), 0.34, 0.45, (236, 238, 245), 0, None, (180, 184, 196))   # bluetooth earpiece
    dot(Hd, F(-1.35, 0.1), (90, 170, 255), 0.18)


BRAD_HS = dict(skin=BRSK, skull=(3.0, 3.35), jaw=(1.1, -1.9, 2.4, 1.8), nose=(0.85, None), eye=((90, 130, 90), 1.3),
               brow=((92, 62, 40), 0.3), lip=(212, 104, 108), teeth=(255, 255, 252), cheeks=(1.7, -1.0, 0.8, 0.5, (240, 160, 150)),
               back=_brad_back, front=_brad_front)
BRAD = dict(skin=BRSK, sleeve=SHIRT_W, pants=KHAKI, torso=_brad_torso, boot=_brad_boot, HS=BRAD_HS, glove=BRSK)


def brad(CH, cam, pose=None, t=0.0, mouth=0.0, expr='smile', look=0.0, **kw):
    """Brad from Naperville. expr: smile grin ope panic nervous smug shock sad stunned cheer"""
    return human(CH, cam, BRAD, pose, t, mouth, expr, look, **kw)


# ====================================================================================================== TERRY & GARY
def _thug_torso(rx, ry, top):
    def f(T, bc, br, ln):
        P = T3((30, 30, 38), 0.26)
        ellt(T, bc, rx, ry, P)
        ellt(T, H(0.2 + ln, top + br), rx - 0.9, 3.0, P)
        for k in range(4):                                                   # quilted puffer bands
            yy = bc[1] - (k - 1.6) * 2.1
            cap(T, (bc[0] - rx * 0.8, yy), (bc[0] + rx * 0.8, yy), 0.16, 0.16, P[2])
        cap(T, H(2.4 + ln, top - 1.0), H(2.2 + ln, 6.6), 0.15, 0.15, (150, 154, 168))
        cap(T, H(0.0 + ln, top + 1.4 + br), H(2.5 + ln, top + 0.4 + br), 1.1, 1.0, P[1], None, P[2])     # collar
    return f


def _thug_boot(A, e, ang):
    ell(A, (e[0] + 0.9, e[1] + 0.3), 2.3, 1.2, (28, 28, 34), 0, (66, 66, 80), (14, 14, 18))
    ell(A, (e[0] + 0.9, e[1] + 1.0), 2.4, 0.4, (110, 110, 120))


def _thug_front(color):
    def f(Hd, F, shades=False, expr='normal', t=0.0, ctx=None):
        ctx = ctx or {}
        bn = T3((26, 26, 32), 0.28)
        if not ctx.get('nohat'):                                              # black beanie with a drama-mask patch and «CDS»
            ell(Hd, F(0.3, 3.5), 3.3, 2.3, bn[0], 0, bn[1], bn[2])
            cap(Hd, F(-2.8, 2.5), F(3.4, 2.9), 0.95, 0.9, bn[1], None, bn[2])
            ell(Hd, F(1.6, 3.2), 0.85, 0.85, (246, 246, 250), 0, None, (190, 194, 206))
            dot(Hd, F(1.35, 3.35), (30, 30, 36), 0.14); dot(Hd, F(1.85, 3.35), (30, 30, 36), 0.14)
            cap(Hd, F(1.2, 2.95), F(1.5, 2.85), 0.08, 0.08, (30, 30, 36)); cap(Hd, F(1.5, 2.85), F(2.0, 3.0), 0.08, 0.08, (30, 30, 36))
        if shades:
            for cx, cy, w, h in ((0.65, 0.55, 0.85, 0.7), (2.05, 0.45, 1.0, 0.8)):
                rect_h(Hd, F, cx, cy, w, h, (12, 12, 18))
                cap(Hd, F(cx - w * 0.5, cy + h * 0.2), F(cx - w * 0.1, cy + h * 0.5), 0.12, 0.1, (96, 120, 170))
            cap(Hd, F(1.4, 0.58), F(1.2, 0.55), 0.13, 0.13, (12, 12, 18))
    return f


TERRY_HS = dict(skin=T3((240, 204, 180), 0.28), skull=(2.8, 3.5), jaw=(1.0, -2.0, 2.3, 1.9), nose=(1.2, None), eye=((100, 120, 90), 1.3),
                brow=((60, 44, 36), 0.34), lip=(190, 100, 100), cheeks=(1.7, -1.1, 0.8, 0.5, (240, 160, 150)), front=_thug_front('terry'))
TERRY = dict(skin=TERRY_HS['skin'], sleeve=T3((30, 30, 38), 0.26), pants=T3((24, 24, 30), 0.3), torso=_thug_torso(4.7, 5.8, 18.0),
             boot=_thug_boot, HS=TERRY_HS, shoulders=(2.8, 18.2), hips=(1.2, 9.6), hy=22.3, leg_len=(4.8, 4.7), arm_len=(4.0, 3.9),
             pelvis=(3.6, 2.4), hsc=0.97, glove=T3((30, 30, 38), 0.26))
GARY_HS = dict(skin=T3((224, 172, 134), 0.28), skull=(3.1, 3.2), jaw=(1.1, -1.8, 2.7, 1.9), nose=(0.95, None), eye=((80, 70, 50), 1.3),
               brow=((50, 36, 30), 0.34), lip=(180, 90, 92), cheeks=(1.7, -1.0, 1.0, 0.6, (236, 140, 120)), front=_thug_front('gary'))
GARY = dict(skin=GARY_HS['skin'], sleeve=T3((30, 30, 38), 0.26), pants=T3((24, 24, 30), 0.3), torso=_thug_torso(6.2, 5.2, 15.8),
            boot=_thug_boot, HS=GARY_HS, shoulders=(3.4, 15.6), hips=(1.5, 7.6), hy=19.6, leg_len=(3.6, 3.5), arm_len=(3.4, 3.3),
            pelvis=(4.4, 2.5), hsc=1.08, glove=T3((30, 30, 38), 0.26))


def terry(CH, cam, pose=None, t=0.0, mouth=0.0, expr='nervous', look=0.0, **kw):
    return human(CH, cam, TERRY, pose, t, mouth, expr, look, **kw)


def gary(CH, cam, pose=None, t=0.0, mouth=0.0, expr='normal', look=0.0, **kw):
    return human(CH, cam, GARY, pose, t, mouth, expr, look, **kw)


# ====================================================================================================== MRS. WOZNIAK
ROBE = T3((236, 160, 196), 0.26)


def _mrsw_torso(T, bc, br, ln):
    ellt(T, bc, 5.6, 5.8, ROBE)
    ellt(T, H(0.2 + ln, 16.4 + br), 4.8, 3.0, ROBE)
    ell(T, H(2.4 + ln, 13.4), 1.2, 4.4, ROBE[2], 0.08)                                # robe opening
    poly(T, [H(0.6 + ln, 18.6 + br), H(2.6 + ln, 17.4 + br), H(1.8 + ln, 15.0 + br), H(0.0 + ln, 16.8 + br)], (252, 244, 232))   # nightgown collar
    cap(T, H(-4.4 + ln, 9.6), H(5.2 + ln, 9.2), 0.5, 0.5, (250, 244, 232))                                                   # belt
    for k, (x, h) in enumerate(((-2.6, 13.0), (-0.8, 11.4), (0.6, 14.4), (-3.2, 15.8), (3.0, 10.4))):                       # quilting dots
        dot(T, H(x + ln, h), ROBE[2], 0.3)


def _mrsw_boot(A, e, ang):
    ell(A, (e[0] + 0.8, e[1] + 0.3), 2.3, 1.1, (250, 244, 240), 0, None, (200, 190, 190))              # fluffy slipper
    ell(A, (e[0] + 1.0, e[1] - 0.1), 1.4, 0.6, (255, 190, 210))


def _mrsw_back(Hd, F, ctx=None):
    hc = T3((214, 214, 222), 0.3)
    ell(Hd, F(-1.2, 0.8), 3.3, 3.1, hc[0], 0.1, hc[1], hc[2])


def _mrsw_front(Hd, F, shades=False, expr='normal', t=0.0, ctx=None):
    hc = T3((214, 214, 222), 0.3)
    ell(Hd, F(0.2, 2.6), 3.2, 1.7, hc[0], 0, hc[1], hc[2])
    for k, (x, y) in enumerate(((-1.2, 3.6), (0.5, 4.0), (2.0, 3.6))):                               # pink curlers
        cap(Hd, F(x, y), F(x + 0.1, y + 1.5), 0.72, 0.72, (255, 140, 190), (255, 190, 220), (214, 96, 150))
        dot(Hd, F(x, y + 1.6), (236, 236, 244), 0.3)
    # big round glasses
    for cx, cy, r in ((0.65, 0.5, 0.95), (2.1, 0.4, 1.15)):
        ell(Hd, F(cx, cy), r, r, (250, 250, 255), 0, None, None)
    for cx, cy, r in ((0.65, 0.5, 1.15), (2.1, 0.4, 1.35)):
        ring(Hd, F, cx, cy, r, (60, 50, 60))
    cap(Hd, F(1.6, 0.5), F(1.2, 0.5), 0.12, 0.12, (60, 50, 60))
    dot(Hd, F(-0.8, -1.0), (255, 240, 200), 0.3)                                                     # pearl earring
    # wrinkles
    cap(Hd, F(2.4, -0.3), F(3.0, -0.6), 0.06, 0.06, HS_MW['skin'][2]); cap(Hd, F(1.2, -1.2), F(1.8, -1.5), 0.06, 0.06, HS_MW['skin'][2])


def ring(Hd, F, cx, cy, r, c):
    """thin ring (glasses rim) made of 10 short segments"""
    pts = [(cx + r * math.cos(a), cy + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 11)]
    for a, b in zip(pts[:-1], pts[1:]): cap(Hd, F(*a), F(*b), 0.1, 0.1, c)


HS_MW = dict(skin=T3((236, 192, 166), 0.26), skull=(3.0, 3.2), jaw=(1.1, -1.8, 2.5, 1.8), nose=(1.1, None), eye=((90, 110, 140), 1.1),
             brow=((170, 170, 180), 0.3), lip=(196, 100, 110), back=_mrsw_back, front=_mrsw_front)
MRSW = dict(skin=HS_MW['skin'], sleeve=ROBE, pants=ROBE, torso=_mrsw_torso, boot=_mrsw_boot, HS=HS_MW, pelvis=(4.2, 2.8),
            leg_len=(4.0, 3.8), hsc=1.0, glove=HS_MW['skin'])


def mrs_w(CH, cam, pose=None, t=0.0, mouth=0.0, expr='deadpan', look=0.0, **kw):
    """Mrs. Wozniak (block lady): robe, curlers, glasses. expr: deadpan angry sly smug shock"""
    return human(CH, cam, MRSW, pose, t, mouth, expr, look, **kw)


# ====================================================================================================== DEB (bust at her desk)
CARD = T3((176, 120, 170), 0.28)


def _deb_torso(T, bc, br, ln):
    ellt(T, bc, 5.4, 5.6, CARD)
    ellt(T, H(0.2 + ln, 16.4 + br), 4.8, 3.0, CARD)
    # Christmas yoke pattern: little trees and snowflake dots
    for k, x in enumerate((-2.6, -0.4, 1.8, 3.4)):
        poly(T, [H(x + ln, 15.4 + br), H(x - 0.7 + ln, 13.6 + br), H(x + 0.7 + ln, 13.6 + br)], (70, 168, 96))
        dot(T, H(x + ln, 15.9 + br), (255, 220, 90), 0.2)
    for k in range(6): dot(T, H(-3.0 + k * 1.2 + ln, 12.0), (250, 250, 255), 0.18)
    cap(T, H(-1.8 + ln, 18.0 + br), H(2.0 + ln, 17.0 + br), 0.3, 0.3, (250, 214, 100))               # glasses chain
    cap(T, H(2.0 + ln, 17.0 + br), H(2.6 + ln, 13.6), 0.14, 0.14, (250, 214, 100))
    rect(T, H(3.0 + ln, 12.8), 0.9, 2.0, 0.0, (60, 60, 70))


def _deb_back(Hd, F, ctx=None):
    hc = T3((178, 160, 158), 0.3)
    for k, (x, y) in enumerate(((-2.4, 1.6), (-1.4, 3.2), (0.4, 3.8), (-2.8, -0.2), (-2.2, -1.8))):
        ell(Hd, F(x, y), 1.5, 1.5, hc[0], 0, hc[1], hc[2])


def _deb_front(Hd, F, shades=False, expr='normal', t=0.0, ctx=None):
    hc = T3((178, 160, 158), 0.3)
    for k, (x, y) in enumerate(((-1.2, 3.4), (0.4, 4.0), (1.9, 3.5), (3.0, 2.6))):                    # curly perm on top
        ell(Hd, F(x, y), 1.35, 1.3, hc[0], 0, hc[1], hc[2])
    for cx, cy, r in ((0.65, 0.5, 1.2), (2.1, 0.4, 1.4)):
        ring(Hd, F, cx, cy, r, (150, 90, 60))
    cap(Hd, F(1.65, 0.5), F(1.2, 0.5), 0.1, 0.1, (150, 90, 60))
    dot(Hd, F(-1.0, -1.0), (255, 214, 120), 0.3)


HS_DEB = dict(skin=T3((246, 214, 188), 0.26), skull=(3.0, 3.3), jaw=(1.1, -1.8, 2.5, 1.8), nose=(0.9, None), eye=((90, 140, 130), 1.25),
              brow=((140, 120, 110), 0.28), lip=(222, 110, 120), cheeks=(1.7, -1.0, 0.9, 0.55, (246, 160, 156)), back=_deb_back, front=_deb_front)
DEB = dict(skin=HS_DEB['skin'], sleeve=CARD, pants=CARD, torso=_deb_torso, boot=_mrsw_boot, HS=HS_DEB, pelvis=(4.2, 2.8), glove=HS_DEB['skin'])


def deb(CH, cam, pose=None, t=0.0, mouth=0.0, expr='smile', look=0.0, **kw):
    """Deb (Control): always legs=False behind the desk. expr: smile grin nervous shock sad smug blank"""
    kw.setdefault('legs', False)
    return human(CH, cam, DEB, pose, t, mouth, expr, look, **kw)


# ====================================================================================================== MARTY (rat)
RAT = T3((124, 120, 134), 0.26)
BELLY = T3((196, 190, 200), 0.2)
CAPB = T3((120, 92, 64), 0.28)


def marty(CH, cam, t=0.0, mouth=0.0, expr='deadpan', look=(0.0, 0.0), fry=False, cap_on=True, scarf=True, blink=True, sit=True):
    """Marty the informant rat, seated, 3/4 to +x. Anchor = the surface he sits on, unit ~ 0.4 human units. expr: deadpan smug wide sad glare"""
    L = Layer(cam)
    br = 0.12 * math.sin(t * 1.8)
    # tail
    for k in range(7):
        a = (-4.4 - 1.1 * k, 0.4 + 0.8 * math.sin(k * 0.8 + t * 1.2) + 0.2 * k)
        b = (-4.4 - 1.1 * (k + 1), 0.4 + 0.8 * math.sin((k + 1) * 0.8 + t * 1.2) + 0.2 * (k + 1))
        cap(L, H(*a), H(*b), 0.42 - 0.03 * k, 0.4 - 0.03 * k, (214, 150, 150), (240, 190, 190), (170, 110, 116))
    # body (pear shape), belly, hind foot
    ellt(L, H(-0.8, 4.0), 5.0, 4.2, RAT)
    ell(L, H(1.2, 3.6), 3.0, 3.2, BELLY[0], 0, BELLY[1], BELLY[2])
    ell(L, H(1.4, 0.7), 2.4, 1.0, (214, 150, 150), 0, (240, 190, 190), (170, 110, 116))
    ell(L, H(-2.6, 0.9), 2.0, 1.0, (214, 150, 150), 0, (240, 190, 190), (170, 110, 116))
    if scarf:                                                                                       # red-white scarf
        cap(L, H(-1.2, 7.6 + br), H(3.2, 7.4 + br), 1.15, 1.15, (210, 50, 56), (240, 100, 100), (150, 24, 36))
        for k in range(4): cap(L, H(-0.6 + k * 1.1, 8.4 + br), H(-0.6 + k * 1.1, 6.6 + br), 0.38, 0.38, (250, 246, 240))
        cap(L, H(0.2, 6.9 + br), H(0.0, 4.4), 0.7, 0.55, (210, 50, 56), (240, 100, 100), (150, 24, 36))
    # head: skull, snout, cheek
    hx = 0.4
    ell(L, H(hx, 10.6 + br), 3.8, 3.3, RAT[0], 0, RAT[1], RAT[2])
    ell(L, H(hx + 3.6, 9.8 + br), 3.0, 1.9, RAT[0], -0.15, RAT[1], RAT[2])                          # snout
    ell(L, H(hx + 6.2, 9.9 + br), 0.7, 0.62, (232, 140, 150), 0, (255, 190, 196), (190, 100, 110))   # pink nose
    # ears
    ell(L, H(hx - 1.8, 13.8 + br), 2.0, 2.2, RAT[0], 0, RAT[1], RAT[2]); ell(L, H(hx - 1.8, 13.7 + br), 1.2, 1.4, (232, 160, 170))
    ell(L, H(hx + 1.2, 14.0 + br), 1.7, 1.9, RAT[0], 0, RAT[1], RAT[2]); ell(L, H(hx + 1.2, 13.9 + br), 1.0, 1.2, (232, 160, 170))
    # eyes (heavy lids), brows
    lid = {'deadpan': 0.55, 'smug': 0.45, 'wide': 0.0, 'sad': 0.35, 'glare': 0.5}.get(expr, 0.5)
    for k, (ex, ey, r) in enumerate(((hx + 1.2, 11.4, 0.85), (hx + 3.3, 11.2, 1.05))):
        e_ = H(ex + 0.4 * look[0], ey + br + 0.3 * look[1])
        if blink and (t % 3.7) < 0.12:
            cap(L, (e_[0] - r, e_[1]), (e_[0] + r, e_[1]), 0.15, 0.15, (24, 20, 24)); continue
        ell(L, H(ex, ey + br), r * 1.15, r * 1.15, (250, 248, 244))
        dot(L, (e_[0] + 0.2, e_[1]), (22, 18, 22), r * 0.7)
        dot(L, (e_[0] - 0.05, e_[1] - 0.3), (255, 255, 255), r * 0.2)
        ell(L, H(ex, ey + br + r * (0.5 - lid * 0.9)), r * 1.25, r * (0.55 + lid * 0.9) * 0.62, RAT[0])           # drooping upper lid
        cap(L, H(ex - r * 1.2, ey + br + r * (0.45 - lid * 0.8)), H(ex + r * 1.2, ey + br + r * (0.45 - lid * 0.8) + (0.25 if k else 0.0)),
            0.14, 0.14, RAT[2])
    if expr == 'glare':
        cap(L, H(hx + 0.2, 13.0 + br), H(hx + 1.9, 12.4 + br), 0.2, 0.2, (40, 36, 40)); cap(L, H(hx + 2.5, 12.3 + br), H(hx + 4.2, 12.9 + br), 0.2, 0.2, (40, 36, 40))
    # mouth + buck teeth, whiskers
    m = max(mouth, 0.35 if expr == 'wide' else 0.0)
    my = 8.9 + br
    if m > 0.08:
        ell(L, H(hx + 3.6, my - 0.2 * m), 1.7, 0.3 + 0.9 * m, (96, 30, 36))
        poly(L, [H(hx + 3.0, my + 0.4), H(hx + 3.9, my + 0.4), H(hx + 3.5, my - 0.8 - 0.4 * m)], (252, 248, 236))
        poly(L, [H(hx + 3.9, my + 0.4), H(hx + 4.7, my + 0.4), H(hx + 4.3, my - 0.8 - 0.4 * m)], (252, 248, 236))
    else:
        cap(L, H(hx + 2.4, my + 0.2), H(hx + 5.2, my + (0.5 if expr == 'smug' else 0.0)), 0.14, 0.14, (60, 38, 44))
        poly(L, [H(hx + 4.4, my + 0.1), H(hx + 5.0, my + 0.1), H(hx + 4.7, my - 1.0)], (252, 248, 236))
    for sy in (-0.7, 0.0, 0.7):
        cap(L, H(hx + 5.0, 9.8 + br + sy), H(hx + 8.6, 9.8 + br + sy * 2.2 + 0.5), 0.07, 0.04, (236, 236, 244))
        cap(L, H(hx + 4.6, 9.7 + br + sy), H(hx + 4.0, 8.0 + br + sy * 2.0), 0.0, 0.0, (236, 236, 244)) if False else None
    if cap_on:                                                                                      # tweed flat cap (восьмиклинка)
        ell(L, H(hx - 0.2, 13.4 + br), 3.9, 1.5, CAPB[0], 0.06, CAPB[1], CAPB[2])
        ell(L, H(hx + 2.4, 12.9 + br), 2.8, 0.8, CAPB[0], -0.12, CAPB[1], CAPB[2])
        dot(L, H(hx + 0.4, 14.3 + br), CAPB[2], 0.3); dot(L, H(hx - 1.0, 13.9 + br), CAPB[1], 0.3)
    # arms + hands (holding a fry)
    cap(L, H(2.8, 6.0), H(4.4, 3.8 + br), 0.9, 0.7, RAT[0], RAT[1], RAT[2])
    ell(L, H(4.8, 3.6 + br), 0.9, 0.75, (232, 170, 176))
    if fry:
        cap(L, H(4.6, 3.5 + br), H(6.0, 6.2 + br), 0.5, 0.5, (250, 206, 84), (255, 232, 140), (214, 160, 40))
        cap(L, H(4.8, 3.4 + br), H(5.2, 6.6 + br), 0.45, 0.45, (244, 196, 70), (255, 226, 130), (200, 148, 36))
    outline(L, OL)
    CH.add(L)
    return dict(head=H(hx, 10.6 + br), mouth=H(hx + 3.6, my))


# ====================================================================================================== SILHOUETTES (Chief, Sal, cabbie)
def _sil_front(kind):
    def f(Hd, F, shades=False, expr='normal', t=0.0, ctx=None):
        c = (14, 16, 26)
        if kind == 'chief':                                                    # fedora-ish committee hat
            ell(Hd, F(0.3, 2.9), 3.9, 0.7, c); ell(Hd, F(0.3, 4.0), 2.5, 1.5, c)
        elif kind == 'sal':                                                    # chef hat
            ell(Hd, F(0.2, 3.6), 3.0, 1.4, c); cap(Hd, F(-1.6, 3.8), F(-1.6, 5.8), 1.1, 1.1, c); cap(Hd, F(1.6, 3.8), F(1.6, 5.8), 1.1, 1.1, c)
            ell(Hd, F(0.0, 6.0), 2.6, 1.5, c)
        elif kind == 'cabbie':                                                 # newsboy cap
            ell(Hd, F(0.3, 3.4), 3.4, 1.8, c); ell(Hd, F(2.6, 2.9), 2.4, 0.6, c)
    return f


def _sil_spec(kind, col=(14, 16, 26), wide=1.0):
    tones = (col, col, col)
    hs = dict(skin=tones, skull=(3.0, 3.4), jaw=(1.1, -1.9, 2.5, 1.9), sil=True, front=_sil_front(kind))
    def torso(T, bc, br, ln):
        ellt(T, bc, 5.2 * wide, 5.4, tones); ellt(T, H(0.2 + ln, 16.4 + br), 4.7 * wide, 3.0, tones)
    return dict(skin=tones, sleeve=tones, pants=tones, torso=torso, boot=lambda A, e, a: ell(A, (e[0] + 0.9, e[1] + 0.3), 2.3, 1.2, col), HS=hs,
                glove=tones)


SIL = {k: _sil_spec(k) for k in ('chief', 'sal', 'cabbie')}


def silhouette(CH, cam, kind='chief', pose=None, t=0.0, mouth=0.0, **kw):
    kw.setdefault('legs', False)
    return human(CH, cam, SIL[kind], pose, t, mouth, 'blank', 0.0, **kw)


# ====================================================================================================== block ladies (variants of Mrs. W)
def lady_spec(robe, hair, curlers=(255, 140, 190), skin=(236, 192, 166), glasses=True):
    R = T3(robe, 0.26)
    hc = T3(hair, 0.3)

    def torso(T, bc, br, ln):
        ellt(T, bc, 5.6, 5.8, R); ellt(T, H(0.2 + ln, 16.4 + br), 4.8, 3.0, R)
        ell(T, H(2.4 + ln, 13.4), 1.2, 4.4, R[2], 0.08)
        poly(T, [H(0.6 + ln, 18.6 + br), H(2.6 + ln, 17.4 + br), H(1.8 + ln, 15.0 + br), H(0.0 + ln, 16.8 + br)], (252, 244, 232))
        cap(T, H(-4.4 + ln, 9.6), H(5.2 + ln, 9.2), 0.5, 0.5, (250, 244, 232))
        for k, (x, h) in enumerate(((-2.6, 13.0), (-0.8, 11.4), (0.6, 14.4), (-3.2, 15.8), (3.0, 10.4))): dot(T, H(x + ln, h), R[2], 0.3)

    def back(Hd, F, ctx=None):
        ell(Hd, F(-1.2, 0.8), 3.3, 3.1, hc[0], 0.1, hc[1], hc[2])

    def front(Hd, F, shades=False, expr='normal', t=0.0, ctx=None):
        ell(Hd, F(0.2, 2.6), 3.2, 1.7, hc[0], 0, hc[1], hc[2])
        for k, (x, y) in enumerate(((-1.2, 3.6), (0.5, 4.0), (2.0, 3.6))):
            cap(Hd, F(x, y), F(x + 0.1, y + 1.5), 0.72, 0.72, curlers, tuple(min(255, c + 40) for c in curlers), tuple(int(c * 0.7) for c in curlers))
            dot(Hd, F(x, y + 1.6), (236, 236, 244), 0.3)
        if glasses:
            for cx, cy, r in ((0.65, 0.5, 0.95), (2.1, 0.4, 1.15)): ell(Hd, F(cx, cy), r, r, (250, 250, 255), 0, None, None)
            for cx, cy, r in ((0.65, 0.5, 1.15), (2.1, 0.4, 1.35)): ring(Hd, F, cx, cy, r, (60, 50, 60))
            cap(Hd, F(1.6, 0.5), F(1.2, 0.5), 0.12, 0.12, (60, 50, 60))
        dot(Hd, F(-0.8, -1.0), (255, 240, 200), 0.3)

    sk = T3(skin, 0.26)
    hs = dict(HS_MW, skin=sk, back=back, front=front)
    return dict(skin=sk, sleeve=R, pants=R, torso=torso, boot=_mrsw_boot, HS=hs, pelvis=(4.2, 2.8), leg_len=(4.0, 3.8), hsc=1.0, glove=sk)


LADIES = dict(
    mrs_w=MRSW,
    rose=lady_spec((150, 196, 236), (236, 236, 242), (255, 214, 120), (232, 184, 150)),
    dot=lady_spec((176, 226, 190), (120, 90, 70), (170, 150, 255), (214, 160, 130)),
    lou=lady_spec((255, 224, 120), (190, 200, 224), (255, 140, 190), (240, 200, 176)),
    bea=lady_spec((226, 170, 230), (70, 62, 66), (130, 220, 200), (200, 150, 120)),
)


def lady(CH, cam, who='mrs_w', pose=None, t=0.0, mouth=0.0, expr='deadpan', look=0.0, **kw):
    return human(CH, cam, LADIES[who], pose, t, mouth, expr, look, **kw)


# ====================================================================================================== STREETS WORKER (E03)
def _worker_torso(T, bc, br, ln):
    J = T3((70, 74, 88), 0.26); V = T3((255, 132, 24), 0.26)
    ellt(T, bc, 5.4, 5.6, J); ellt(T, H(0.2 + ln, 16.6 + br), 4.8, 3.0, J)
    ellt(T, bc, 4.7, 5.3, V); ellt(T, H(0.5 + ln, 16.2 + br), 4.0, 2.8, V)
    for yy in (9.6, 12.8): cap(T, H(-3.9 + ln, yy), H(4.6 + ln, yy - 0.2), 0.55, 0.55, (236, 246, 150))
    cap(T, H(1.7 + ln, 18.0 + br), H(1.5 + ln, 8.0), 0.45, 0.45, (236, 246, 150))


def _worker_boot(A, e, ang):
    ell(A, (e[0] + 1.0, e[1] + 0.3), 2.3, 1.2, (110, 76, 40), 0, (150, 110, 64), (66, 44, 22))
    ell(A, (e[0] + 1.0, e[1] + 1.0), 2.4, 0.4, (40, 40, 44))


def _worker_front(Hd, F, shades=False, expr='normal', t=0.0, ctx=None):
    ell(Hd, F(0.2, 3.0), 3.5, 2.0, (255, 214, 60), 0, (255, 240, 150), (200, 150, 20))
    cap(Hd, F(-3.0, 2.2), F(3.9, 2.4), 0.8, 0.6, (255, 214, 60), (255, 240, 150), (200, 150, 20))
    cap(Hd, F(0.0, 5.0), F(0.4, 2.2), 0.45, 0.45, (230, 184, 30))


WORKER_HS = dict(skin=T3((206, 150, 116), 0.28), skull=(3.1, 3.4), jaw=(1.1, -1.9, 2.6, 1.9), nose=(1.1, (210, 120, 100)), eye=((90, 96, 100), 1.0),
                 brow=((120, 120, 126), 0.42), stache=((150, 150, 156), 1.2), lip=(150, 76, 76), front=_worker_front)
WORKER = dict(skin=WORKER_HS['skin'], sleeve=T3((70, 74, 88), 0.26), pants=T3((52, 56, 70), 0.3), torso=_worker_torso, boot=_worker_boot,
              HS=WORKER_HS, glove=T3((236, 200, 90), 0.2))


def worker(CH, cam, pose=None, t=0.0, mouth=0.0, expr='deadpan', look=0.0, **kw):
    """Streets Department worker: hard hat, orange hi-vis vest, grey moustache. expr: deadpan blank normal sleepy"""
    return human(CH, cam, WORKER, pose, t, mouth, expr, look, **kw)
