"""Cast of «Sunny Palms HOA» (US channel): Dale (Florida Man), Brenda (HOA president), Earl (the grandfathered gator).
Same rig conventions as props/folk.py: anchor (1000,1000) = floor point under the character, H(x, h) -> (1000 + x, 1000 - h),
+x = facing direction (ACam.flip mirrors), 3-tone shading (hi / base / sh) from a top-left light, heroes get scene light later
(stage.Light). Everything is drawn with folk.py primitives on a stage.Chars canvas."""
import math
import numpy as np
import scene as S
from scene import Layer
from props.folk import (H, cap, ell, ellt, dot, poly, outline, _limb, _merge, _D, band_mask, recolor, OL, vblend)

# ======================================================================================= DALE
DC = dict(skin=(228, 146, 112), skin_hi=(246, 178, 142), skin_sh=(190, 106, 86), peel=(252, 228, 210), burn=(214, 92, 84),
          hair=(238, 208, 110), hair_hi=(255, 238, 162), hair_sh=(190, 156, 72), stache=(184, 142, 74), brow=(132, 90, 44),
          eye=(30, 24, 22), white=(246, 244, 238), iris=(66, 120, 190), red=(232, 120, 120),
          shirt=(30, 150, 162), shirt_hi=(64, 182, 188), shirt_sh=(18, 104, 120), fl_pink=(244, 94, 146), fl_yel=(255, 222, 84),
          fl_leaf=(24, 96, 72), tank=(242, 240, 228), tank_hi=(255, 254, 246), tank_sh=(206, 200, 176),
          short=(196, 168, 106), short_hi=(224, 198, 136), short_sh=(150, 124, 78), pocket=(170, 142, 88),
          sock=(246, 246, 242), sock_sh=(206, 208, 210), strap=(70, 46, 34), sole=(126, 90, 58),
          chain=(244, 200, 64), gold=(236, 192, 60), lens=(56, 70, 116), glint=(170, 196, 240),
          can=(214, 218, 224), can_sh=(160, 166, 176), kooz=(126, 236, 88), kooz_sh=(84, 176, 56), pale=(244, 214, 194))

DPOSE = dict(
    # arms as IK hand targets (x, h) in body units (+x = facing); bn/bf = elbow bend side; legs = (thigh angle, shin angle)
    stand=dict(n=(3.6, 10.2), f=(-3.0, 10.4), bn=1, bf=-1, nleg=(0.06, 0.0), fleg=(-0.06, 0.0)),
    hold=dict(n=(6.6, 14.4), f=(5.6, 14.6), bn=1, bf=1, nleg=(0.10, 0.0), fleg=(-0.10, 0.0)),            # carrying something at the chest
    shout=dict(n=(6.0, 25.6), f=(-4.6, 25.0), bn=1, bf=-1, nleg=(0.25, 0.0), fleg=(-0.25, 0.0)),
    cheer=dict(n=(8.6, 26.0), f=(-3.0, 10.6), bn=-1, bf=-1, nleg=(0.16, 0.0), fleg=(-0.16, 0.0)),        # fist pump
    point=dict(n=(10.6, 17.8), f=(-3.0, 10.6), bn=1, bf=-1, nleg=(0.14, 0.0), fleg=(-0.14, 0.0)),
    spray=dict(n=(9.4, 17.0), f=(-2.4, 11.0), bn=1, bf=-1, nleg=(0.18, 0.0), fleg=(-0.18, 0.0)),        # arm out with the can
    shrug=dict(n=(5.4, 17.0), f=(-4.6, 17.0), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
    hips=dict(n=(2.8, 11.0), f=(-2.8, 11.0), bn=-1, bf=1, nleg=(0.20, 0.0), fleg=(-0.20, 0.0)),
    slump=dict(n=(2.6, 8.4), f=(-2.4, 8.4), bn=1, bf=-1, nleg=(0.03, 0.0), fleg=(-0.03, 0.0)),
    paper=dict(n=(5.4, 19.8), f=(4.6, 20.0), bn=1, bf=1, nleg=(0.06, 0.0), fleg=(-0.06, 0.0)),          # reading the notice at face height
)


def dwalk(t, speed=8.0, amp=0.42, carry=False):
    s = math.sin(t * speed)
    p = dict(n=(3.6 - 2.0 * s, 10.6 + 0.4 * abs(s)), f=(-3.0 + 2.0 * s, 10.6), bn=1, bf=-1,
             nleg=(amp * s, 0.28 * max(0, -s)), fleg=(-amp * s, 0.28 * max(0, s)))
    if carry: p.update(n=(6.6, 14.4 + 0.3 * abs(s)), f=(5.6, 14.6 + 0.3 * abs(s)), bn=1, bf=1)
    return p


def _aviators(Hd, F, P, look, down):
    if down:                                                     # lenses over the eyes
        for cx, cy, r in ((1.45, 21.95, 0.95), (2.85, 21.85, 1.1)):
            e_ = F(cx + 0.1 * look, cy)
            ell(Hd, e_, r, r * 0.92, P['gold']); ell(Hd, e_, r * 0.82, r * 0.74, P['lens'])
            dot(Hd, (e_[0] - r * 0.3, e_[1] - r * 0.3), P['glint'], r * 0.18)
        cap(Hd, F(2.05, 22.15), F(2.25, 22.1), 0.12, 0.12, P['gold'])
        cap(Hd, F(0.5, 22.1), F(-0.8, 21.9), 0.1, 0.1, P['gold'])
    else:                                                        # pushed up on the hair
        cap(Hd, F(-0.4, 24.7), F(0.2, 24.8), 0.13, 0.13, P['gold'])
        for cx, cy, r in ((0.9, 24.85, 0.85), (2.3, 24.6, 0.95)):
            ell(Hd, F(cx, cy), r, r * 0.6, P['gold'], -0.2); ell(Hd, F(cx, cy), r * 0.78, r * 0.42, P['lens'], -0.2)
            dot(Hd, F(cx - 0.3, cy + 0.15), P['glint'], 0.16)
        cap(Hd, F(1.6, 24.75), F(1.8, 24.7), 0.13, 0.13, P['gold'])


def _dale_head(Hd, F, P, expr, t, mouth, look, shades, blink, sweat=0.0, red=0.0, beard=1.0):
    """3/4 head facing +x: lean sunburnt face, bleach-blond mullet, peeling nose, soul patch. F(x, h) head-local coords."""
    sk = {k: tuple(int(c + (r - c) * red) for c, r in zip(P[k], (250, 84, 76))) for k in ('skin', 'skin_hi', 'skin_sh')}
    # mullet (behind the head)
    ell(Hd, F(-1.7, 20.6), 1.35, 2.2, P['hair'], 0.1, P['hair_hi'], P['hair_sh'])
    cap(Hd, F(-2.0, 19.2), F(-2.7, 16.4), 0.95, 0.55, P['hair'], None, P['hair_sh'])                           # the mullet tail
    cap(Hd, F(-1.5, 18.4), F(-1.9, 16.2), 0.6, 0.3, P['hair_sh'])
    cap(Hd, F(0.5, 17.4), F(0.7, 19.2), 1.75, 1.75, sk['skin'], sk['skin_hi'], sk['skin_sh'])                 # neck
    ell(Hd, F(0.8, 21.4), 2.95, 3.4, sk['skin'], -0.06, sk['skin_hi'], sk['skin_sh'])                         # skull
    ell(Hd, F(1.95, 19.5), 2.5, 1.85, sk['skin'], 0.12, None, sk['skin_sh'])                                  # jaw
    ell(Hd, F(3.15, 18.95), 1.2, 1.0, sk['skin'], 0.2, sk['skin_hi'], None)                                    # chin
    ell(Hd, F(-0.95, 21.0), 0.65, 0.95, sk['skin'], 0, None, sk['skin_sh'])                                   # ear
    ell(Hd, F(-0.9, 21.0), 0.3, 0.55, sk['skin_sh'])
    # hair on top: spiky bleached tuft + sideburn
    ell(Hd, F(0.5, 24.2), 3.0, 1.35, P['hair'], 0, P['hair_hi'], P['hair_sh'])
    for k, (x0, x1, h1) in enumerate(((-1.2, -1.9, 25.7), (-0.2, -0.4, 26.0), (0.9, 1.2, 26.1), (1.9, 2.6, 25.5))):
        cap(Hd, F(x0, 24.5), F(x1, h1), 0.6, 0.12, P['hair'], P['hair_hi'], None)
    cap(Hd, F(1.6, 24.0), F(3.4, 23.2), 0.62, 0.35, P['hair'], P['hair_hi'], P['hair_sh'])                    # swoop over the forehead
    cap(Hd, F(-0.3, 22.9), F(-0.5, 20.9), 0.55, 0.4, P['hair'])
    # sunburn cheek + eyes
    ell(Hd, F(2.05, 20.55), 0.95, 0.55, P['burn'])
    ex = 0.12 * look
    eyes = [(F(1.45 + ex, 21.95), 0.56), (F(2.85 + ex, 21.85), 0.7)]
    bl = blink and (t % 3.3) < 0.11
    hide = shades
    if not hide:
        if expr in ('smug', 'deadpan', 'sly') or bl:
            for e_, r in eyes:
                if bl: cap(Hd, (e_[0] - r, e_[1] + 0.05), (e_[0] + r, e_[1] - 0.02), 0.13, 0.13, P['eye'])
                else:
                    ell(Hd, e_, r * 1.1, r * 0.6, P['white']); dot(Hd, (e_[0] + 0.1 + ex, e_[1] + 0.05), P['eye'], r * 0.5)
                    cap(Hd, (e_[0] - r * 1.15, e_[1] - r * 0.5), (e_[0] + r * 1.15, e_[1] - r * 0.6), 0.16, 0.16, sk['skin_sh'])
        else:
            big = expr in ('shout', 'shock', 'cheer')
            for e_, r in eyes:
                rr = r * (1.3 if big else 1.05)
                ell(Hd, e_, rr, rr * 1.1, P['white'])
                if red > 0.3: ell(Hd, e_, rr * 0.95, rr * 1.0, P['red'], 0, None, None); ell(Hd, e_, rr * 0.7, rr * 0.78, P['white'])
                dot(Hd, (e_[0] + 0.1 + ex, e_[1] + 0.04), P['iris'], rr * 0.62)
                dot(Hd, (e_[0] + 0.1 + ex, e_[1] + 0.04), P['eye'], rr * (0.32 if big else 0.4))
                dot(Hd, (e_[0] + 0.02 + ex, e_[1] - 0.12), (255, 255, 255), rr * 0.16)
    bt = {'angry': 0.6, 'shout': 0.45, 'shock': -0.6, 'cheer': -0.15, 'smug': 0.2, 'sly': 0.4, 'sad': -0.55, 'deadpan': 0.05,
          'incredulous': -0.35, 'manic': 0.7}.get(expr, 0.15)
    lift = 0.4 if expr in ('shock', 'cheer', 'incredulous') else 0.0
    for k, (e_, r) in enumerate(eyes):
        base = e_[1] - r - 0.72 - lift - (0.35 if hide else 0.0)
        s_ = 1 if k == 0 else -1
        cap(Hd, (e_[0] - 0.8, base - s_ * bt * 0.36), (e_[0] + 0.8, base + s_ * bt * 0.36), 0.34, 0.3, P['brow'])
    if shades is not None: _aviators(Hd, F, P, look, shades)
    elif True: _aviators(Hd, F, P, look, False)
    # nose (big, peeling), moustache, soul patch, mouth
    ell(Hd, F(3.95, 20.9), 1.05, 0.95, sk['skin'], 0, sk['skin_hi'], sk['skin_sh'])
    for (x, h, r) in ((3.7, 21.3, 0.22), (4.3, 20.7, 0.18), (3.5, 20.5, 0.16)): dot(Hd, F(x, h), P['peel'], r)
    dot(Hd, F(4.55, 20.6), sk['skin_sh'], 0.16)
    m = max(mouth, {'shout': 0.9, 'shock': 0.7, 'cheer': 0.8, 'manic': 0.8}.get(expr, 0.0))
    mc = F(3.2, 19.15)
    if m > 0.08:
        ell(Hd, mc, 0.95 + 0.4 * m, 0.3 + 0.85 * m, (104, 30, 34))
        ell(Hd, (mc[0] + 0.05, mc[1] - 0.22 - 0.3 * m), 0.85 + 0.3 * m, 0.24, P['white'])                     # upper teeth
        ell(Hd, (mc[0] + 0.15, mc[1] + 0.4 * m), 0.55 + 0.3 * m, 0.2 + 0.25 * m, (200, 98, 100))              # tongue
    elif expr in ('smug', 'cheer', 'sly'):
        cap(Hd, F(2.3, 19.3), F(3.9, 19.6), 0.14, 0.14, (120, 52, 44))
        cap(Hd, F(3.9, 19.6), F(4.2, 19.95), 0.12, 0.1, (120, 52, 44))
    else:
        cap(Hd, F(2.4, 19.45), F(3.9, 19.3), 0.14, 0.14, (120, 52, 44))
    my = 19.95 + 0.35 * m
    cap(Hd, F(2.6, my), F(4.4, my + 0.05), 0.3, 0.26, P['stache'])
    ell(Hd, F(3.2, 18.35 - 0.3 * m), 0.4, 0.5, P['stache'])
    if beard > 0:
        for k in range(6): dot(Hd, F(1.4 + 0.5 * k, 18.6 + 0.15 * (k % 2)), P['stache'], 0.11)
    if sweat > 0.05:
        for k, (x, h) in enumerate(((-0.4, 23.2), (3.6, 23.4), (0.1, 22.4))):
            yy = h - sweat * 1.4 * ((t * 1.5 + k * 0.33) % 1.0)
            ell(Hd, F(x, yy), 0.24, 0.4, (170, 220, 255), 0, (230, 246, 255), None)


def dale(CH, cam, pose=None, t=0.0, mouth=0.0, expr='normal', look=0.0, shades=False, hand_n=None, hand_f=None, prop_n=None,
         prop_f=None, lean=0.0, sweat=0.0, red=0.0, paint=None, legs=True, blink=True):
    """expr: normal | shout | angry | smug | sly | shock | cheer | deadpan | incredulous | manic | sad
    shades: False (pushed up on the hair) | True (down over the eyes) | None (hidden entirely)
    paint: (r,g,b) overspray tint on shirt/skin, or None. hand_n / hand_f: IK targets; prop_n / prop_f: callables(L, hand)."""
    P = DC
    pose = pose or DPOSE['stand']
    br = 0.18 * math.sin(t * 2.3)
    sk = (P['skin'], P['skin_hi'], P['skin_sh'])
    L = Layer(cam)
    ln = lean
    sh_n, sh_f = H(3.0 + ln, 17.2 + br), H(-3.0 + ln, 17.4 + br)
    hp_n, hp_f = H(1.4, 8.8), H(-1.2, 8.8)

    def leg(A, hp, ang, foot_dx):
        k, e = _limb(A, hp, *ang, 4.3, 4.2, 1.7, 1.25, *sk)
        d1 = _D(ang[0]); d2 = _D(ang[1])
        # cargo shorts to the knee, white sock on the lower shin, sandal
        cap(A, hp, (hp[0] + d1[0] * 3.6, hp[1] + d1[1] * 3.6), 2.2, 2.1, P['short'], P['short_hi'], P['short_sh'])
        cap(A, (k[0] + d2[0] * 1.4, k[1] + d2[1] * 1.4), (e[0] - d2[0] * 0.2, e[1] - d2[1] * 0.2), 1.3, 1.25, P['sock'], None, P['sock_sh'])
        ell(A, (e[0] + 0.9, e[1] + 0.4), 2.0, 0.85, P['sole'], 0, None, P['strap'])
        cap(A, (e[0] - 0.4, e[1] - 0.3), (e[0] + 1.3, e[1] + 0.1), 0.35, 0.3, P['strap'])
        return k, e

    # far arm + far leg
    if legs:
        A = Layer(cam); leg(A, hp_f, pose['fleg'], -0.4); _merge(L, A)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(*pose['f'])
    ka, ea = _limb(A, sh_f, 0, 0, 3.8, 3.6, 1.5, 1.2, P['shirt'], P['shirt_hi'], P['shirt_sh'], target=tf, bend=pose.get('bf', -1))
    cap(A, ka, ea, 1.15, 1.1, *sk)
    ellt(A, ea, 1.2, 1.12, sk)
    if prop_f: prop_f(A, ea)
    _merge(L, A)
    # pelvis + near leg
    A = Layer(cam)
    if legs:
        ellt(A, H(0.2, 9.4), 3.9, 2.4, (P['short'], P['short_hi'], P['short_sh']))
        leg(A, hp_n, pose['nleg'], 0.4)
        cap(A, H(1.9, 8.6), H(2.5, 7.5), 0.9, 0.85, P['pocket'])                                             # cargo pocket
    else:
        ellt(A, H(0.2, 9.4), 4.2, 3.0, (P['short'], P['short_hi'], P['short_sh']))
    _merge(L, A)
    # torso: Hawaiian shirt hanging open over a yellowed tank, gold chain
    bc = H(1.0 + 0.3 * ln, 12.6 + br * 0.5)
    T = Layer(cam)
    ellt(T, bc, 5.1, 5.5, (P['shirt'], P['shirt_hi'], P['shirt_sh']))
    ellt(T, H(0.2 + ln, 16.6 + br), 4.5, 3.0, (P['shirt'], P['shirt_hi'], P['shirt_sh']))
    ellt(T, H(2.4 + 0.3 * ln, 13.2), 2.0, 5.1, (P['tank'], P['tank_hi'], P['tank_sh']), 0.05)                # tank under the open shirt
    ell(T, H(3.3 + 0.3 * ln, 15.2), 1.1, 1.4, P['skin'], 0, P['skin_hi'], P['skin_sh'])                       # chest V
    cap(T, H(2.3 + ln, 17.2), H(3.1 + ln, 14.0), 0.13, 0.13, P['chain'])
    ell(T, H(3.0 + ln * 0.9, 13.6), 0.32, 0.32, P['chain'])
    fl = band_mask(T, bc, 2.6, bow=0.1, width=5.0, ang=0.5) & band_mask(T, bc, 3.3, bow=-0.2, width=5.0, ang=-0.7)
    recolor(T, fl, [(P['shirt'], P['fl_pink']), (P['shirt_hi'], P['fl_yel']), (P['shirt_sh'], P['fl_leaf'])])
    for (x, h, c) in ((-2.6, 12.0, 'fl_yel'), (-0.6, 9.9, 'fl_pink'), (-3.4, 15.0, 'fl_pink'), (0.2, 15.6, 'fl_yel')):
        dot(T, H(x + ln * 0.5, h), P[c], 0.55); dot(T, H(x + 0.6 + ln * 0.5, h - 0.4), P['fl_leaf'], 0.3)
    _merge(L, T)
    # head
    Hd = Layer(cam)
    hx = 0.9 + ln * 1.3
    hc = H(hx, 21.3 + br)
    def F(x, h): return H(hx + x - 0.9, h + br)
    _dale_head(Hd, F, P, expr, t, mouth, look, shades, blink, sweat, red)
    _merge(L, Hd)
    # near arm (front)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(*pose['n'])
    kna, ena = _limb(A, sh_n, 0, 0, 3.8, 3.6, 1.55, 1.25, P['shirt'], P['shirt_hi'], P['shirt_sh'], target=tn, bend=pose.get('bn', 1))
    cap(A, kna, ena, 1.2, 1.15, *sk)
    ellt(A, ena, 1.28, 1.2, sk)
    if prop_n: prop_n(A, ena)
    _merge(L, A)
    if paint is not None:                                                                                    # overspray on cloth and skin
        m = L.m; col = L.col.astype(np.float32)
        yy = np.arange(L.m.shape[0])[:, None]; xx = np.arange(L.m.shape[1])[None, :]
        speck = (((xx * 73856093) ^ (yy * 19349663)) % 100) < 55
        col[m & speck] = col[m & speck] * 0.35 + np.array(paint, np.float32) * 0.65
        L.col = np.clip(col, 0, 255).astype(np.uint8)
    outline(L, OL)
    CH.add(L)
    return dict(head=hc, mouth=F(3.2, 19.15), hand_n=ena, hand_f=ea, belly=bc)


# ======================================================================================= BRENDA
BC = dict(skin=(240, 186, 148), skin_hi=(254, 212, 178), skin_sh=(208, 144, 112), blush=(246, 132, 132),
          hair=(246, 224, 148), hair_hi=(255, 246, 196), hair_sh=(206, 176, 98), hair_dk=(184, 146, 76),
          visor=(250, 250, 246), visor_hi=(255, 255, 255), visor_sh=(200, 206, 212), band=(255, 130, 176), band_sh=(214, 92, 138),
          eye=(38, 28, 26), white=(248, 248, 244), iris=(60, 150, 190), lid=(120, 176, 226), lash=(40, 24, 22),
          lips=(238, 92, 96), lips_hi=(255, 140, 140), teeth=(255, 255, 250), teeth_sh=(216, 220, 226), pearl=(250, 246, 240),
          polo=(144, 222, 188), polo_hi=(184, 244, 214), polo_sh=(96, 172, 142), collar=(170, 236, 204),
          capri=(224, 202, 156), capri_hi=(244, 224, 178), capri_sh=(178, 154, 108), shoe=(250, 250, 250), shoe_sh=(206, 210, 216),
          lan=(40, 190, 200), badge=(252, 252, 250), badge_ln=(60, 60, 70), board=(150, 100, 60), board_sh=(110, 70, 40),
          paper=(252, 252, 248), clip=(200, 204, 212))

BPOSE = dict(
    stand=dict(n=(3.4, 10.4), f=(-3.0, 10.6), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
    board=dict(n=(3.4, 13.6), f=(2.0, 13.0), bn=1, bf=1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),              # clipboard held at the belly
    show=dict(n=(8.2, 18.4), f=(2.0, 13.0), bn=1, bf=1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),               # holds something up to the viewer
    point=dict(n=(10.6, 17.4), f=(2.0, 13.0), bn=1, bf=1, nleg=(0.08, 0.0), fleg=(-0.08, 0.0)),
    write=dict(n=(5.4, 12.6), f=(2.6, 13.4), bn=1, bf=1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
    wave=dict(n=(5.6, 23.6), f=(2.0, 13.0), bn=-1, bf=1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
    hands=dict(n=(3.8, 12.2), f=(2.2, 12.2), bn=1, bf=1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),              # hands clasped: sweet
    sit=dict(n=(4.8, 11.4), f=(3.6, 11.6), bn=1, bf=1, nleg=(1.5, 0.0), fleg=(1.4, 0.0)),
)


def _brenda_head(Hd, F, P, expr, t, mouth, look, blink, visor=True, sweat=0.0):
    """3/4 head facing +x: round face, frosted asymmetric bob under a white sun visor, huge toothy smile."""
    # back of the bob
    ell(Hd, F(-1.4, 21.0), 2.2, 3.0, P['hair'], 0.1, P['hair_hi'], P['hair_sh'])
    ell(Hd, F(-1.8, 18.9), 1.7, 1.8, P['hair'], 0.2, None, P['hair_sh'])
    cap(Hd, F(0.3, 17.4), F(0.5, 19.0), 1.5, 1.5, P['skin'], P['skin_hi'], P['skin_sh'])                       # neck
    ell(Hd, F(0.9, 20.5), 2.75, 3.0, P['skin'], 0, P['skin_hi'], P['skin_sh'])                                # face
    ell(Hd, F(2.3, 19.4), 2.2, 1.6, P['skin'], 0.1, P['skin_hi'], P['skin_sh'])                               # soft jaw
    # ear + pearl earring
    ell(Hd, F(-0.7, 20.6), 0.5, 0.75, P['skin'], 0, None, P['skin_sh'])
    dot(Hd, F(-0.7, 19.4), P['pearl'], 0.38)
    # blush
    ell(Hd, F(1.6, 19.9), 0.8, 0.5, P['blush']); ell(Hd, F(3.3, 19.8), 0.55, 0.4, P['blush'])
    # bob: side curtain over the ear, asymmetric long side, volume on top
    ell(Hd, F(-0.6, 20.6), 1.35, 2.7, P['hair'], 0.05, P['hair_hi'], P['hair_sh'])
    cap(Hd, F(-1.0, 22.0), F(-0.9, 18.2), 1.0, 0.85, P['hair'], P['hair_hi'], P['hair_sh'])
    ell(Hd, F(0.3, 23.2), 3.0, 1.3, P['hair'], 0, P['hair_hi'], P['hair_sh'])
    poly(Hd, [F(0.4, 23.2), F(3.2, 22.6), F(2.4, 21.9), F(0.2, 22.4)], P['hair'])                              # side-swept bangs
    cap(Hd, F(1.1, 23.0), F(3.0, 22.4), 0.4, 0.3, P['hair_hi'])
    if visor:
        cap(Hd, F(-1.9, 23.85), F(3.5, 23.95), 0.5, 0.5, P['visor'], P['visor_hi'], P['visor_sh'])
        cap(Hd, F(-1.9, 23.45), F(3.5, 23.55), 0.2, 0.2, P['band'])
        ell(Hd, F(4.0, 24.1), 2.4, 0.5, P['visor'], -0.08, P['visor_hi'], P['visor_sh'])                       # brim
        ell(Hd, F(4.1, 23.88), 2.2, 0.18, P['band_sh'], -0.08)
    # eyes: big, lashed, blue shadow
    ex = 0.12 * look
    eyes = [(F(1.5 + ex, 21.6), 0.62), (F(2.9 + ex, 21.55), 0.74)]
    bl = blink and (t % 4.1) < 0.12
    lidk = {'sweet': 0.0, 'evil': 0.5, 'shock': 0.0, 'hollow': 0.25, 'cheer': 0.0, 'bright': 0.0, 'dread': 0.0}.get(expr, 0.0)
    for k, (e_, r) in enumerate(eyes):
        if bl or expr == 'sweet_closed':
            ell(Hd, (e_[0], e_[1] + 0.1), r * 1.2, r * 0.75, P['lid'])
            cap(Hd, (e_[0] - r * 1.2, e_[1] + 0.15), (e_[0] + r * 1.2, e_[1] + 0.15), 0.13, 0.13, P['lash'])
            continue
        big = expr in ('shock', 'dread', 'bright')
        rr = r * (1.25 if big else 1.0)
        ell(Hd, e_, rr * 1.15, rr * 1.2, P['white'])
        if expr in ('sweet', 'cheer'):                                          # happy crescent-ish: bright iris
            dot(Hd, (e_[0] + 0.08 + ex, e_[1] + 0.05), P['iris'], rr * 0.72)
        else:
            dot(Hd, (e_[0] + 0.08 + ex, e_[1] + 0.05), P['iris'], rr * (0.55 if expr in ('shock', 'dread') else 0.7))
        dot(Hd, (e_[0] + 0.08 + ex, e_[1] + 0.05), P['eye'], rr * (0.2 if expr in ('shock', 'dread') else 0.36))
        dot(Hd, (e_[0] - 0.02 + ex, e_[1] - 0.14), (255, 255, 255), rr * 0.2)
        # upper lid / shadow, lashes
        lt = e_[1] - rr * 1.05 + lidk * rr * 1.7
        poly(Hd, [(e_[0] - rr * 1.25, e_[1] - rr * 1.3), (e_[0] + rr * 1.25, e_[1] - rr * 1.3), (e_[0] + rr * 1.25, lt), (e_[0] - rr * 1.25, lt)], P['lid'])
        cap(Hd, (e_[0] - rr * 1.25, lt), (e_[0] + rr * 1.3, lt - 0.05), 0.13, 0.13, P['lash'])
        cap(Hd, (e_[0] + rr * 1.1, lt), (e_[0] + rr * 1.5, lt - 0.35), 0.1, 0.06, P['lash'])
    bt = {'sweet': -0.25, 'evil': 0.55, 'shock': -0.6, 'hollow': 0.05, 'cheer': -0.3, 'bright': -0.45, 'dread': -0.5}.get(expr, -0.15)
    for k, (e_, r) in enumerate(eyes):
        base = e_[1] - r - 0.85 - (0.35 if expr in ('shock', 'bright', 'dread') else 0.0)
        s_ = 1 if k == 0 else -1
        cap(Hd, (e_[0] - 0.7, base - s_ * bt * 0.32), (e_[0] + 0.7, base + s_ * bt * 0.32), 0.24, 0.2, P['hair_dk'])
    ell(Hd, F(3.55, 20.2), 0.5, 0.45, P['skin'], 0, P['skin_hi'], P['skin_sh'])                               # button nose
    # mouth
    m = max(mouth, {'shock': 0.5, 'dread': 0.25}.get(expr, 0.0))
    mc = F(2.45, 18.85)
    grin = expr in ('sweet', 'evil', 'cheer', 'bright', 'hollow') and m < 0.12
    if grin or (m > 0.08 and expr in ('sweet', 'evil', 'cheer', 'bright', 'hollow')):
        w = 1.45 + 0.05 * m; hh = 0.5 + 0.3 * m
        ell(Hd, mc, w, hh, P['lips'], 0, P['lips_hi'], None)
        if m < 0.14:                                                                    # tight-lipped teeth grin
            ell(Hd, (mc[0], mc[1] - 0.05), w * 0.86, hh * 0.7, P['teeth'], 0, None, P['teeth_sh'])
            cap(Hd, (mc[0] - w * 0.8, mc[1] - 0.02), (mc[0] + w * 0.8, mc[1] - 0.02), 0.06, 0.06, P['teeth_sh'])
        else:                                                                           # talking: dark mouth, upper teeth strip
            ell(Hd, (mc[0], mc[1] + 0.02), w * 0.86, hh * 0.74, (128, 38, 52))
            ell(Hd, (mc[0], mc[1] - hh * 0.36), w * 0.8, hh * 0.3, P['teeth'], 0, None, P['teeth_sh'])
            ell(Hd, (mc[0], mc[1] + hh * 0.42), w * 0.5, hh * 0.24, (214, 96, 104))
    elif m > 0.08:
        ell(Hd, mc, 0.55 + 0.35 * m, 0.25 + 0.7 * m, (120, 34, 44))
        ell(Hd, mc, 0.7 + 0.35 * m, 0.14 + 0.25 * m, P['lips'], 0, None, None) if m < 0.2 else None
    else:
        cap(Hd, (mc[0] - 0.7, mc[1] + 0.05), (mc[0] + 0.7, mc[1] + 0.05 + (0.15 if expr == 'dread' else -0.1)), 0.16, 0.16, P['lips'])
    if sweat > 0.05:
        for k, (x, h) in enumerate(((-0.1, 23.0), (3.4, 23.6), (0.2, 22.2))):
            yy = h - sweat * 1.4 * ((t * 1.5 + k * 0.33) % 1.0)
            ell(Hd, F(x, yy), 0.24, 0.4, (170, 220, 255), 0, (230, 246, 255), None)


def brenda(CH, cam, pose=None, t=0.0, mouth=0.0, expr='sweet', look=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
           lean=0.0, sweat=0.0, legs=True, blink=True, visor=True):
    """expr: sweet | evil | shock | hollow | cheer | bright | dread"""
    P = BC
    pose = pose or BPOSE['stand']
    br = 0.16 * math.sin(t * 2.0 + 1.1)
    sk = (P['skin'], P['skin_hi'], P['skin_sh'])
    L = Layer(cam)
    ln = lean
    sh_n, sh_f = H(2.8 + ln, 16.4 + br), H(-2.6 + ln, 16.6 + br)
    hp_n, hp_f = H(1.2, 8.4), H(-1.0, 8.4)

    def leg(A, hp, ang):
        k, e = _limb(A, hp, *ang, 4.0, 3.9, 1.6, 1.15, *sk)
        d1 = _D(ang[0]); d2 = _D(ang[1])
        cap(A, hp, (k[0] + d1[0] * 0.4, k[1] + d1[1] * 0.4 + 0.2), 2.0, 1.75, P['capri'], P['capri_hi'], P['capri_sh'])
        cap(A, (k[0] - d1[0] * 0.2, k[1]), (k[0] + d2[0] * 1.6, k[1] + d2[1] * 1.6), 1.7, 1.4, P['capri'], P['capri_hi'], P['capri_sh'])
        ell(A, (e[0] + 0.8, e[1] + 0.3), 1.9, 0.85, P['shoe'], 0, None, P['shoe_sh'])
        return k, e

    if legs:
        A = Layer(cam); leg(A, hp_f, pose['fleg']); _merge(L, A)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(*pose['f'])
    ka, ea = _limb(A, sh_f, 0, 0, 3.4, 3.3, 1.35, 1.0, P['polo'], P['polo_hi'], P['polo_sh'], target=tf, bend=pose.get('bf', -1))
    cap(A, ka, ea, 0.95, 0.9, *sk); ellt(A, ea, 1.0, 0.95, sk)
    if prop_f: prop_f(A, ea)
    _merge(L, A)
    A = Layer(cam)
    if legs:
        ellt(A, H(0.2, 9.0), 3.6, 2.4, (P['capri'], P['capri_hi'], P['capri_sh']))
        leg(A, hp_n, pose['nleg'])
    else:
        ellt(A, H(0.2, 9.0), 4.0, 3.0, (P['capri'], P['capri_hi'], P['capri_sh']))
    _merge(L, A)
    T = Layer(cam)
    ellt(T, H(0.9 + 0.3 * ln, 12.4 + br * 0.5), 4.6, 5.0, (P['polo'], P['polo_hi'], P['polo_sh']))
    ellt(T, H(0.3 + ln, 15.8 + br), 4.2, 2.9, (P['polo'], P['polo_hi'], P['polo_sh']))
    cap(T, H(2.2 + ln, 17.0), H(3.1 + ln, 11.6), 0.22, 0.22, P['lan'])                                        # lanyard
    ell(T, H(3.0 + ln, 11.2), 0.95, 1.2, P['badge'], 0, None, P['visor_sh'])
    dot(T, H(2.85 + ln, 11.6), P['polo_sh'], 0.35); cap(T, H(2.5 + ln, 10.6), H(3.6 + ln, 10.6), 0.08, 0.08, P['badge_ln'])
    poly(T, [H(-0.4 + ln, 17.8 + br), H(0.9 + ln, 19.2 + br), H(1.7 + ln, 17.6 + br), H(0.6 + ln, 16.8 + br)], P['collar'])   # popped collar
    poly(T, [H(1.9 + ln, 17.4 + br), H(3.2 + ln, 18.6 + br), H(3.4 + ln, 17.0 + br), H(2.4 + ln, 16.4 + br)], P['collar'])
    _merge(L, T)
    Hd = Layer(cam)
    hx = 0.9 + ln * 1.3
    hc = H(hx, 20.8 + br)
    def F(x, h): return H(hx + x - 0.9, h + br)
    _brenda_head(Hd, F, P, expr, t, mouth, look, blink, visor, sweat)
    _merge(L, Hd)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(*pose['n'])
    kna, ena = _limb(A, sh_n, 0, 0, 3.4, 3.3, 1.4, 1.05, P['polo'], P['polo_hi'], P['polo_sh'], target=tn, bend=pose.get('bn', 1))
    cap(A, kna, ena, 1.0, 0.95, *sk); ellt(A, ena, 1.05, 1.0, sk)
    if prop_n: prop_n(A, ena)
    _merge(L, A)
    outline(L, OL)
    CH.add(L)
    return dict(head=hc, mouth=F(2.45, 18.85), hand_n=ena, hand_f=ea)


# ======================================================================================= EARL
EC = dict(skin=(98, 136, 64), skin_hi=(150, 186, 92), skin_sh=(58, 92, 46), belly=(200, 200, 124), eye=(240, 204, 64),
          eye_sh=(196, 152, 40), pupil=(20, 18, 16), lid=(84, 118, 56), tooth=(250, 248, 236), mouth=(120, 44, 48),
          nostril=(30, 46, 28), water=(46, 104, 100), water_hi=(120, 186, 170), pad=(84, 168, 80), pad_hi=(140, 210, 110))


def earl(CH, cam, t=0.0, mouth=0.0, lid=0.5, look=(0.0, 0.0), paint=None, water_y=0.0, ripple=1.0, blink=True, grin=0.0):
    """Earl in profile facing +x, floating in the pond: only eyes, snout and the top of the head show above the waterline
    (h = water_y). lid: 0 wide open .. 1 shut; paint: (r,g,b) overspray on the snout; anchor = waterline centre under the eye."""
    P = EC
    L = Layer(cam)
    bob = 0.12 * math.sin(t * 1.4)
    wl = water_y + bob * 0.3
    def hh(h): return h + bob
    # snout (long, flat), lower jaw sliver, head bulk
    ell(L, H(2.4, hh(wl + 0.3)), 6.6, 1.5, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    ell(L, H(-2.0, hh(wl + 0.6)), 4.2, 2.1, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    ell(L, H(7.6, hh(wl + 0.5)), 1.6, 1.0, P['skin'], 0, P['skin_hi'], P['skin_sh'])                         # snout tip
    dot(L, H(8.4, hh(wl + 1.05)), P['nostril'], 0.38)
    dot(L, H(7.2, hh(wl + 1.25)), P['skin_hi'], 0.25)
    # eye ridge + eye
    ell(L, H(-0.3, hh(wl + 2.5)), 1.8, 1.45, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    e = H(-0.1, hh(wl + 2.65))
    ell(L, e, 1.25, 1.15, P['eye'], 0, None, P['eye_sh'])
    px_, py_ = look
    ell(L, (e[0] + 0.25 + 0.35 * px_, e[1] + 0.05 + 0.3 * py_), 0.32, 1.0, P['pupil'])                       # vertical slit
    dot(L, (e[0] - 0.05, e[1] - 0.45), (255, 255, 240), 0.2)
    cl = lid + (1.0 if (blink and (t % 3.9) < 0.14) else 0.0)
    cl = min(1.0, cl)
    if cl > 0.02:                                                                                           # heavy deadpan eyelid, clipped to the eyeball
        A = Layer(cam)
        ell(A, e, 1.32, 1.22, P['lid'], 0, P['skin_hi'], None)
        ly = cam.p(*e)[1] + (-1.22 + 2.44 * cl) * cam.sc
        A.m[int(round(ly)):, :] = False
        L.col[A.m] = A.col[A.m]; L.m |= A.m
        cap(L, (e[0] - 1.25, e[1] - 1.22 + 2.44 * cl), (e[0] + 1.25, e[1] - 1.22 + 2.44 * cl), 0.14, 0.14, P['skin_sh'])
    # mouth line + teeth, jaw drops when talking
    m = max(mouth, grin)
    ell(L, H(3.2, hh(wl + 0.05 - 0.55 * m)), 5.2, 0.32 + 0.6 * m, P['skin_sh'] if m < 0.08 else P['mouth'])
    if m > 0.08:
        for k in range(6): poly(L, [H(0.6 + k * 1.05, hh(wl + 0.25)), H(1.0 + k * 1.05, hh(wl + 0.25)), H(0.8 + k * 1.05, hh(wl - 0.35))], P['tooth'])
    else:
        for k in range(4): poly(L, [H(4.0 + k * 1.05, hh(wl + 0.05)), H(4.4 + k * 1.05, hh(wl + 0.05)), H(4.2 + k * 1.05, hh(wl - 0.45))], P['tooth'])
    # bumps on the back of the head
    for k in range(3): ell(L, H(-4.2 - k * 1.3, hh(wl + 1.1 - 0.15 * k)), 0.7, 0.5, P['skin_sh'])
    if paint is not None:
        m2 = L.m; col = L.col.astype(np.float32)
        yy = np.arange(L.m.shape[0])[:, None]; xx = np.arange(L.m.shape[1])[None, :]
        speck = (((xx * 73856093) ^ (yy * 19349663)) % 100) < 97
        ex_, ey_ = cam.p(*e); er = 1.5 * cam.sc                                                          # the eye stays clean: «Not the eyes.»
        speck &= ((xx - ex_) ** 2 + (yy - ey_) ** 2) > er * er
        col[m2 & speck] = col[m2 & speck] * 0.04 + np.array(paint, np.float32) * 0.96
        L.col = np.clip(col, 0, 255).astype(np.uint8)
    outline(L, (24, 44, 30))
    # waterline clip: nothing below h = water_y is drawn (the head sinks into the pond)
    x0, ycut = cam.p(1000.0, 1000.0 - wl)
    ycut = int(round(ycut))
    if 0 <= ycut < L.m.shape[0]: L.m[ycut:, :] = False
    elif ycut < 0: L.m[:] = False
    CH.add(L)
    return dict(eye=e, mouth=H(3.2, hh(wl)), water=1000.0 - wl)
