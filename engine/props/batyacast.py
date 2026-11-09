"""Cast of «Батя сам»: Batya (Виктор, 52 — a «wardrobe»: square torso wider than tall, head straight on the shoulders, grey flat-top
crew cut, big grey mutton-chop sideburns, reading glasses on an elastic band pushed up on the forehead, burgundy sweater with a cream
knitted deer/snowflake band, khaki multi-pocket vest, yellow tape measure on the belt, blue track pants with one white stripe, grey wool
socks in brown slippers), Tyoma (son, 19 — a vertical line: thin and tall, a cloud of dark curls, an oversized acid-lime hoodie, black
wide pants, chunky white sneakers, big headphones on the neck, phone always up, half-closed lids), Ira (mum, 48 — a compact barrel:
aubergine bob with a straight fringe, mustard cardigan, reading glasses on a gold chain, coral lipstick).
Same drawing conventions as props/folk.py: anchor (1000,1000) = floor point under the character, H(x, h), +x = facing direction,
3-tone shading from the top-left. Silhouettes and palettes are this series' own (philosophy: series/batya/design/philosophy.md)."""
import math
import numpy as np
from scene import Layer
from props.folk import H, cap, ell, ellt, dot, poly, outline, _limb, _merge
from props.teshcast import eye, mouth

OL = (52, 20, 30)                                                     # «boiled beetroot» outline


def _mix(a, b, k):
    return tuple(int(x + (y - x) * k) for x, y in zip(a, b))


def _sweat(L, F, t, n=3, seed=0, area=((0.0, 24.5), (2.6, 25.8))):
    """sweat drops sliding down (sick / effort)"""
    for i in range(n):
        ph = (t * 0.7 + i * 0.37 + seed * 0.13) % 1.0
        x = area[0][0] + (area[1][0] - area[0][0]) * ((i * 0.61 + seed * 0.3) % 1.0)
        y = area[1][1] - ph * 1.6
        ell(L, F(x, y), 0.2, 0.3, (170, 214, 255), 0, (236, 248, 255), (120, 170, 230))


# ======================================================================================= BATYA
BC = dict(skin=(232, 178, 140), skin_hi=(248, 206, 172), skin_sh=(196, 136, 104), cheek=(226, 120, 104), nose=(214, 128, 106),
          hair=(176, 176, 180), hair_hi=(214, 214, 218), hair_sh=(128, 128, 136), brow=(66, 60, 64),
          sw=(146, 30, 44), sw_hi=(184, 58, 66), sw_sh=(98, 16, 30), knit=(240, 228, 196), knit_sh=(200, 186, 150),
          vest=(118, 118, 66), vest_hi=(150, 150, 90), vest_sh=(82, 82, 42), pocket=(98, 98, 52),
          pants=(44, 58, 120), pants_hi=(70, 88, 156), pants_sh=(28, 38, 84), stripe=(236, 236, 236),
          sock=(150, 150, 150), slip=(116, 70, 40), slip_hi=(150, 98, 60), slip_sh=(80, 46, 24),
          tape=(246, 206, 30), tape_sh=(186, 150, 20), glass=(40, 34, 36), lens=(200, 226, 240),
          apron=(250, 244, 236), apron_sh=(214, 204, 196), flower=(226, 70, 96), leaf=(90, 160, 80))
BPOSE = dict(
    stand=dict(n=(2.8, 11.6), f=(-2.6, 11.8), bn=1, bf=-1, nleg=(0.1, 0.0), fleg=(-0.1, 0.0)),
    fists=dict(n=(3.4, 16.0), f=(-3.4, 15.8), bn=1, bf=-1, nleg=(0.24, 0.0), fleg=(-0.24, 0.0), chest=1.0),   # «Я сам!»
    point=dict(n=(6.6, 19.6), f=(-2.6, 11.8), bn=1, bf=-1, nleg=(0.14, 0.0), fleg=(-0.12, 0.0), chest=1.0),   # finger up/forward
    shock=dict(n=(4.8, 22.2), f=(-3.8, 22.0), bn=1, bf=-1, nleg=(0.12, 0.0), fleg=(-0.12, 0.0)),
    hold=dict(n=(4.6, 15.4), f=(3.6, 15.2), bn=1, bf=1, nleg=(0.08, 0.0), fleg=(-0.08, 0.0)),                 # both hands forward
    bell=dict(n=(4.2, 22.6), f=(-2.4, 14.4), bn=1, bf=-1, nleg=(0.08, 0.0), fleg=(-0.08, 0.0)),               # bell raised high
    dying=dict(n=(5.2, 20.8), f=(-1.0, 22.6), bn=1, bf=-1, nleg=(0.08, 0.0), fleg=(-0.08, 0.0)),              # hand out + hand on brow
    forehead=dict(n=(2.4, 24.6), f=(-2.6, 13.8), bn=1, bf=-1, nleg=(0.08, 0.0), fleg=(-0.08, 0.0)),           # palm on forehead
    stir=dict(n=(5.0, 14.6), f=(4.2, 17.2), bn=1, bf=1, nleg=(0.1, 0.0), fleg=(-0.1, 0.0)),                    # ladle + lid at the stove
)


def _knit_band(T, x0, x1, h0, h1, P, seed=0):
    """cream knitted band across the sweater: zigzag rows + pixel deer (stick figures) + snowflake dots"""
    poly(T, [H(x0, h1), H(x1, h1), H(x1, h0), H(x0, h0)], P['knit'])
    n = 7
    for i in range(n + 1):                                                    # zigzag edges (knitted teeth)
        xa = x0 + (x1 - x0) * i / n; xb = x0 + (x1 - x0) * (i + 0.5) / n
        cap(T, H(xa, h1 - 0.05), H(xb, h1 - 0.42), 0.09, 0.09, P['sw'])
        cap(T, H(xb, h1 - 0.42), H(min(x1, xa + (x1 - x0) / n), h1 - 0.05), 0.09, 0.09, P['sw'])
        cap(T, H(xa, h0 + 0.05), H(xb, h0 + 0.42), 0.09, 0.09, P['sw'])
        cap(T, H(xb, h0 + 0.42), H(min(x1, xa + (x1 - x0) / n), h0 + 0.05), 0.09, 0.09, P['sw'])
    mid = (h0 + h1) / 2
    for k in range(3):                                                        # three tiny deer
        cx = x0 + (x1 - x0) * (0.2 + 0.3 * k)
        c = P['sw_sh']
        cap(T, H(cx - 0.35, mid - 0.05), H(cx + 0.3, mid - 0.05), 0.13, 0.13, c)        # body
        for lx in (-0.3, -0.12, 0.12, 0.28): cap(T, H(cx + lx, mid - 0.1), H(cx + lx, mid - 0.5), 0.06, 0.06, c)
        cap(T, H(cx + 0.3, mid), H(cx + 0.45, mid + 0.3), 0.08, 0.08, c)                  # neck
        dot(T, H(cx + 0.5, mid + 0.34), c, 0.12)                                          # head
        cap(T, H(cx + 0.45, mid + 0.42), H(cx + 0.35, mid + 0.62), 0.04, 0.04, c)         # antlers
        cap(T, H(cx + 0.55, mid + 0.42), H(cx + 0.66, mid + 0.6), 0.04, 0.04, c)
    for k in range(4):
        dot(T, H(x0 + (x1 - x0) * (0.05 + 0.3 * k), mid + 0.1), P['sw'], 0.09)


def _batya_head(Hd, Fh, P, expr, t, m, look, blink, sick, glasses, towel):
    # head sits straight on the shoulders: wide rounded-square skull, double chin
    ell(Hd, Fh(0.95, 23.75), 3.1, 2.8, P['skin'], 0, P['skin_hi'], P['skin_sh'], th_sh=-0.6)
    ell(Hd, Fh(1.4, 21.45), 2.45, 1.1, P['skin'], 0.05, None, P['skin_sh'])                       # double chin
    cap(Hd, Fh(0.2, 20.9), Fh(2.8, 21.0), 0.24, 0.24, P['skin_sh'])                              # chin fold
    ell(Hd, Fh(-1.75, 23.7), 0.78, 1.08, P['skin'], 0.1, P['skin_hi'], P['skin_sh'])             # ear
    ell(Hd, Fh(-1.7, 23.7), 0.4, 0.66, P['cheek'])
    # grey flat-top crew cut: a flat dense «площадка», bristle texture inside (no spikes on top)
    poly(Hd, [Fh(-1.95, 25.0), Fh(-1.75, 26.75), Fh(3.25, 26.85), Fh(3.65, 25.6), Fh(2.9, 25.85), Fh(-0.9, 25.75)], P['hair'])
    cap(Hd, Fh(-1.6, 26.7), Fh(3.1, 26.8), 0.2, 0.2, P['hair_hi'])
    for k in range(10): cap(Hd, Fh(-1.4 + k * 0.5, 26.35), Fh(-1.32 + k * 0.5, 25.95), 0.06, 0.05, P['hair_sh'])
    # mutton-chop sideburns: furry «котлеты» from the temple down to the jaw, in front of the ear
    poly(Hd, [Fh(-1.3, 25.4), Fh(-0.45, 25.4), Fh(-0.2, 23.4), Fh(0.35, 21.9), Fh(-0.4, 21.3), Fh(-1.25, 22.6)], P['hair'])
    rng = np.random.default_rng(3)
    for k in range(10):                                                                        # fluffy irregular edge + strands
        hk = 25.2 - k * 0.38
        ell(Hd, Fh(-0.75 + 0.06 * k + 0.25 * (rng.random() - 0.5), hk), 0.42 + 0.03 * k, 0.32, P['hair'], rng.random(), P['hair_hi'], P['hair_sh'])
    for k in range(5): dot(Hd, Fh(-1.05 + 0.18 * k, 24.6 - k * 0.55), P['hair_sh'], 0.09)
    # eyes: small, deep-set, heavy lids
    exm = {'shout': 'shout', 'shock': 'shock', 'scream': 'shout', 'smug': 'smug', 'proud': 'smug', 'happy': 'squint'}.get(expr, 'normal')
    if expr == 'dying': exm = 'normal'
    eyes = [(Fh(1.25, 24.15), 0.55), (Fh(2.65, 24.1), 0.6)]
    bl = blink and (t % 3.7) < 0.1 and expr not in ('shout', 'shock', 'scream')
    for c, r in eyes:
        ell(Hd, (c[0] - 0.05, c[1] + r * 1.15), r * 1.05, r * 0.38, _mix(P['skin_sh'], P['cheek'], 0.4 * sick))   # bags
        eye(Hd, c, r, exm, (look, 0.1 if expr == 'dying' else 0.0), iris=(70, 96, 120), lid=P['skin_sh'], blink=bl,
            bulge=1.0)
        if expr in ('dying', 'sad', 'whine'):                                                   # drooping upper lid
            cap(Hd, (c[0] - r * 1.05, c[1] - r * 0.25), (c[0] + r * 1.05, c[1] - r * 0.5), r * 0.42, r * 0.42, P['skin_sh'])
    # bushy brush eyebrows
    bt = {'angry': 0.75, 'fists': 0.6, 'shout': -0.35, 'shock': -0.75, 'dying': -0.85, 'sad': -0.7, 'whine': -0.85, 'smug': 0.25,
          'proud': -0.2, 'happy': -0.3}.get(expr, 0.0)
    lift = 0.5 if expr in ('shout', 'shock', 'scream') else 0.0
    for k, (c, r) in enumerate(eyes):
        s_ = 1 if k == 0 else -1
        base = c[1] - r - 0.45 - lift
        cap(Hd, (c[0] - 0.68, base - s_ * bt * 0.42), (c[0] + 0.68, base + s_ * bt * 0.42), 0.3, 0.25, P['brow'])
        cap(Hd, (c[0] - 0.5, base - 0.1 - s_ * bt * 0.4), (c[0] + 0.45, base - 0.1 + s_ * bt * 0.4), 0.09, 0.08, _mix(P['brow'], P['hair'], 0.6))
    # reading glasses on an elastic band, pushed up on the forehead
    if glasses:
        cap(Hd, Fh(-1.7, 26.25), Fh(1.0, 26.35), 0.11, 0.11, P['glass'])
        for gx in (1.45, 2.6):
            ell(Hd, Fh(gx, 26.35), 0.46, 0.34, P['glass']); ell(Hd, Fh(gx, 26.35), 0.34, 0.23, P['lens'])
            dot(Hd, Fh(gx - 0.12, 26.45), (255, 255, 255), 0.1)
        cap(Hd, Fh(1.9, 26.38), Fh(2.15, 26.38), 0.07, 0.07, P['glass'])
    # potato nose (red when sick)
    nz = _mix(P['nose'], (226, 60, 60), sick)
    ell(Hd, Fh(3.45, 23.35), 1.0, 0.85, nz, 0, _mix(P['skin_hi'], (255, 160, 150), sick), _mix(P['skin_sh'], (170, 40, 40), sick))
    dot(Hd, Fh(3.25, 23.62), (255, 236, 220), 0.18)
    dot(Hd, Fh(3.6, 22.85), _mix(P['skin_sh'], (120, 30, 30), sick), 0.18)
    ell(Hd, Fh(2.1, 22.75), 0.8, 0.45, _mix(P['cheek'], (240, 80, 80), sick))
    mm = max(m, {'shout': 0.75, 'scream': 0.95, 'shock': 0.55}.get(expr, 0.0))
    mc = Fh(2.5, 21.95 - 0.25 * mm)
    mouth(Hd, mc, 0.95, mm, {'smug': 'smug', 'proud': 'proud', 'happy': 'happy'}.get(expr, 'sad' if expr in ('dying', 'sad', 'whine', 'angry') else 'normal'),
          lip=(170, 84, 78))
    if sick > 0.3:
        _sweat(Hd, Fh, t, n=3, area=((0.2, 23.4), (2.8, 25.0)))
        cap(Hd, Fh(3.9, 22.85), Fh(4.0, 22.35 - 0.2 * math.sin(t * 2)), 0.12, 0.08, (190, 226, 255))           # runny nose
    if towel:                                                                                # wet folded towel on the forehead
        poly(Hd, [Fh(-0.4, 24.95), Fh(3.5, 25.05), Fh(3.6, 26.05), Fh(-0.5, 25.95)], (240, 244, 250))
        cap(Hd, Fh(-0.4, 25.0), Fh(3.5, 25.1), 0.13, 0.13, (186, 200, 226))
        cap(Hd, Fh(-0.5, 25.95), Fh(3.6, 26.05), 0.1, 0.1, (210, 220, 240))
        for k in range(2): ell(Hd, Fh(0.6 + k * 1.9, 24.75 - 0.4 * ((t * 0.8 + k * 0.5) % 1.0)), 0.13, 0.2, (150, 196, 250))
    return mc


def batya(CH, cam, pose=None, t=0.0, mouth_=0.0, expr='normal', look=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
          lean=None, legs=True, vest=True, apron=False, sick=0.0, glasses=True, towel=False, blink=True, shake=0.0, outline_=True,
          hat=False, frost=0.0):
    """expr: normal | shout | shock | dying | sad | whine | angry | fists | smug | proud | happy.
    legs=False: only from the hips up (in bed under the blankets). apron: mum's frilly flowery apron. sick 0..1: red nose, sweat."""
    pose = pose or BPOSE['stand']
    P = dict(BC)
    br = 0.12 * math.sin(t * 2.0)
    jx = shake * math.sin(t * 43.0)
    ln = (pose.get('lean', 0.0) if lean is None else lean) + jx
    sh_n, sh_f = H(2.2 + ln, 19.4 + br), H(-2.7 + ln, 19.6 + br)
    hp_n, hp_f = H(1.3, 10.4), H(-1.6, 10.4)
    pants = (P['pants'], P['pants_hi'], P['pants_sh'])
    foot = (P['slip'], P['slip_hi'], P['slip_sh'])
    sw = (P['sw'], P['sw_hi'], P['sw_sh'])
    L = Layer(cam)
    if legs:
        for hp, lg, side in ((hp_f, pose['fleg'], -1), (hp_n, pose['nleg'], 1)):
            A = Layer(cam)
            k_, e_ = _limb(A, hp, *lg, 5.3, 4.9, 1.45, 1.2, *pants)
            cap(A, (hp[0] + side * 1.05, hp[1]), (e_[0] + side * 1.0, e_[1] - 0.6), 0.14, 0.14, P['stripe'])      # one white stripe
            cap(A, (e_[0], e_[1] - 0.25), (e_[0] + 0.25, e_[1] + 0.05), 0.95, 0.9, P['sock'])                   # wool sock
            for k in range(3): cap(A, (e_[0] - 0.6, e_[1] - 0.6 + k * 0.3), (e_[0] + 0.7, e_[1] - 0.6 + k * 0.3), 0.05, 0.05, (120, 120, 120))
            ellt(A, (e_[0] + 0.9 * (1 if side > 0 else 0.6), e_[1] + 0.35), 2.0, 0.62, foot)                    # slipper
            _merge(L, A, OL)
    # far arm
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(pose['f'][0] + jx, pose['f'][1])
    kf, ef = _limb(A, sh_f, 0, 0, 4.3, 4.0, 1.3, 1.0, *sw, target=tf, bend=pose.get('bf', -1))
    cap(A, (ef[0] - 0.3, ef[1]), (ef[0] + 0.3, ef[1]), 0.85, 0.85, P['sw_sh'])                                 # ribbed cuff
    ell(A, ef, 1.0, 0.95, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_f: prop_f(A, ef)
    _merge(L, A, OL)
    # torso: the «wardrobe» — square block wider than tall, belly pushes the sweater forward
    T = Layer(cam)
    chest = 1.0 + 0.12 * pose.get('chest', 0.0)
    poly(T, [H(-3.6 + ln * 0.5, 20.4 + br), H(2.9 * chest + ln * 0.5, 20.6 + br), H(3.9 * chest + ln * 0.3, 16.0),
             H(4.4 * chest, 12.6), H(3.6, 9.6), H(-3.2, 9.6), H(-3.9, 13.0)], P['sw'])
    ellt(T, H(0.0 + ln * 0.4, 16.6 + br), 3.9, 3.9, sw)
    ellt(T, H(1.2, 12.6), 3.3 * chest, 2.8, sw)                                                               # belly
    _knit_band(T, -3.4 + ln * 0.5, 3.5 * chest + ln * 0.4, 16.2 + br, 18.0 + br, P)
    for k in range(9): cap(T, H(-3.1 + k * 0.82, 9.7), H(-3.0 + k * 0.82, 10.4), 0.16, 0.16, P['sw_sh'])      # ribbed hem
    cap(T, H(-1.0 + ln * 0.5, 20.5 + br), H(2.2 + ln * 0.5, 20.6 + br), 0.55, 0.5, P['sw_sh'])               # collar
    if vest and not apron:
        vt = (P['vest'], P['vest_hi'], P['vest_sh'])
        poly(T, [H(-3.4 + ln * 0.5, 20.3 + br), H(-1.3 + ln * 0.5, 20.4 + br), H(-0.9, 11.0), H(-3.3, 10.2), H(-4.0, 13.4)], P['vest'])
        poly(T, [H(2.5 + ln * 0.5, 20.4 + br), H(3.0 + ln * 0.5, 20.2 + br), H(4.0, 15.6), H(4.2, 12.4), H(3.3, 10.4), H(3.0, 11.2)], P['vest'])
        cap(T, H(-1.3 + ln * 0.5, 20.4 + br), H(-0.9, 11.0), 0.16, 0.16, P['vest_sh'])
        cap(T, H(2.5 + ln * 0.5, 20.4 + br), H(3.0, 11.2), 0.16, 0.16, P['vest_sh'])
        for (px, ph) in ((-2.4, 15.6), (-2.3, 12.0), (3.4, 15.0), (3.5, 12.0)):                                # four pockets
            w_ = 0.75 if px < 0 else 0.45
            poly(T, [H(px - w_, ph + 0.75), H(px + w_, ph + 0.75), H(px + w_ - 0.05, ph - 0.7), H(px - w_ + 0.05, ph - 0.7)], P['pocket'])
            cap(T, H(px - w_, ph + 0.75), H(px + w_, ph + 0.75), 0.13, 0.13, P['vest_sh'])
            dot(T, H(px, ph + 0.55), (210, 196, 120), 0.1)
        dot(T, H(-2.1, 16.8), (240, 60, 50), 0.16)                                                             # pen in the pocket
        cap(T, H(-2.1, 16.7), H(-2.1, 17.6), 0.09, 0.09, (60, 80, 180))
    if apron:                                                                                                   # mum's frilly apron
        poly(T, [H(-1.5, 19.6 + br), H(2.6, 19.8 + br), H(4.3, 12.6), H(3.5, 9.4), H(-2.6, 9.4), H(-3.0, 13.4)], P['apron'])
        for k in range(10): ell(T, H(-2.5 + k * 0.62, 9.45), 0.36, 0.28, P['apron_sh'])                       # frill
        for (fx_, fh) in ((-1.2, 17.6), (1.4, 16.4), (-0.6, 13.6), (2.3, 12.4), (0.4, 11.0), (2.8, 15.0)):     # flowers
            for a in range(5):
                an = a * 1.256
                dot(T, H(fx_ + 0.3 * math.cos(an), fh + 0.3 * math.sin(an)), P['flower'], 0.17)
            dot(T, H(fx_, fh), (250, 220, 90), 0.12)
            cap(T, H(fx_ + 0.2, fh - 0.3), H(fx_ + 0.55, fh - 0.6), 0.09, 0.09, P['leaf'])
        cap(T, H(-1.5, 19.6 + br), H(-2.2, 20.6 + br), 0.13, 0.13, P['apron_sh'])
    # belt + yellow tape measure on the hip
    cap(T, H(-3.2, 10.0), H(3.6, 10.0), 0.3, 0.3, (60, 40, 30))
    poly(T, [H(2.0, 11.2), H(3.3, 11.2), H(3.3, 9.6), H(2.0, 9.6)], P['tape'])
    ell(T, H(2.65, 10.4), 0.42, 0.42, P['tape_sh'])
    cap(T, H(2.0, 9.9), H(2.3, 9.9), 0.12, 0.12, (210, 210, 210))
    _merge(L, T, OL)
    # head
    Hd = Layer(cam)
    hx = 0.4 + ln * 1.0

    def Fh(x, h): return H(hx + x - 0.4, h + br)
    mc = _batya_head(Hd, Fh, P, expr, t, mouth_, look, blink, sick, glasses and not hat, towel)
    if hat:                                                                                   # burgundy knitted hat with a pompon
        ell(Hd, Fh(0.85, 26.2), 3.25, 1.75, P['sw'], 0, P['sw_hi'], P['sw_sh'])
        cap(Hd, Fh(-2.3, 25.3), Fh(4.0, 25.4), 0.62, 0.62, P['knit'])
        for k in range(7): cap(Hd, Fh(-1.6 + k * 0.85, 25.8), Fh(-1.5 + k * 0.85, 27.3), 0.1, 0.1, P['sw_sh'])
        ell(Hd, Fh(0.6, 28.2), 0.95, 0.85, P['knit'], 0, (255, 255, 255), P['knit_sh'])
    if frost > 0:                                                                             # frost on brows / sideburns
        for k in range(9): dot(Hd, Fh(-0.9 + (k % 5) * 0.85, 24.9 - (k // 5) * 2.2 + 0.2 * (k % 2)), (236, 246, 255), 0.13 * frost + 0.05)
    _merge(L, Hd, OL)
    # near arm
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(pose['n'][0] + jx, pose['n'][1])
    kn, en = _limb(A, sh_n, 0, 0, 4.3, 4.0, 1.35, 1.05, *sw, target=tn, bend=pose.get('bn', 1))
    cap(A, (en[0] - 0.3, en[1]), (en[0] + 0.3, en[1]), 0.9, 0.9, P['sw_sh'])
    ell(A, en, 1.05, 1.0, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_n: prop_n(A, en)
    _merge(L, A, OL)
    if outline_: outline(L, OL)
    CH.add(L)
    return dict(hand_n=en, hand_f=ef, mouth=mc, head=Fh(1.4, 23.7), top=Fh(0.9, 27.0))


# ======================================================================================= TYOMA (son)
TC = dict(skin=(240, 202, 176), skin_hi=(252, 226, 204), skin_sh=(204, 160, 136), cheek=(236, 168, 150),
          hair=(66, 44, 34), hair_hi=(104, 74, 56), hair_sh=(40, 26, 20), brow=(56, 38, 30), fuzz=(150, 120, 100),
          hood=(172, 222, 54), hood_hi=(206, 246, 110), hood_sh=(118, 170, 30), string=(250, 250, 244),
          pants=(36, 36, 44), pants_hi=(64, 64, 76), pants_sh=(20, 20, 26), shoe=(246, 246, 246), shoe_sh=(196, 200, 210),
          sole=(210, 210, 220), phone=(30, 30, 36), phone_hi=(80, 84, 96), cans=(28, 28, 32), cans_hi=(70, 70, 80))
TPOSE = dict(
    film=dict(n=(5.6, 23.4), f=(-1.6, 15.0), bn=1, bf=-1, nleg=(0.06, 0.0), fleg=(-0.06, 0.0)),        # phone up, filming
    selfie=dict(n=(6.2, 26.4), f=(-1.4, 15.0), bn=1, bf=-1, nleg=(0.06, 0.0), fleg=(-0.06, 0.0)),      # phone at arm's length to himself
    stand=dict(n=(2.2, 14.0), f=(-2.0, 14.2), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
    shrug=dict(n=(4.4, 19.2), f=(-3.8, 19.4), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
)


def _tema_head(Hd, Fh, P, expr, t, m, look, blink):
    cap(Hd, Fh(0.2, 23.0), Fh(0.5, 25.4), 0.62, 0.58, P['skin'], P['skin_hi'], P['skin_sh'])                # thin neck
    ell(Hd, Fh(0.75, 27.3), 1.95, 2.45, P['skin'], 0.0, P['skin_hi'], P['skin_sh'], th_sh=-0.7)             # narrow face
    ell(Hd, Fh(1.25, 25.3), 1.25, 0.8, P['skin'], 0.12)                                                       # chin
    ell(Hd, Fh(-0.95, 27.1), 0.6, 0.85, P['skin'], 0.1, P['skin_hi'], P['skin_sh'])                         # ear
    dot(Hd, Fh(-0.95, 26.5), (210, 210, 220), 0.14)                                                          # earring stud
    lid = 0.0 if expr in ('shock', 'shout') else 0.55                                                         # deadpan half-closed lids
    eyes = [(Fh(1.05, 27.45), 0.5), (Fh(2.1, 27.4), 0.55)]
    bl = blink and (t % 4.1) < 0.1 and expr not in ('shock', 'shout')
    for c, r in eyes:
        eye(Hd, c, r, 'shock' if expr == 'shock' else 'normal', (look, 0.15), iris=(96, 70, 40), lid=P['skin_sh'], blink=bl, bulge=1.0)
        if lid > 0 and not bl:
            poly(Hd, [(c[0] - r * 1.15, c[1] - r * 1.3), (c[0] + r * 1.15, c[1] - r * 1.3), (c[0] + r * 1.15, c[1] - r * (1.1 - 2 * lid)),
                      (c[0] - r * 1.15, c[1] - r * (1.1 - 2 * lid))], P['skin'])
            cap(Hd, (c[0] - r * 1.05, c[1] - r * (1.1 - 2 * lid)), (c[0] + r * 1.05, c[1] - r * (1.1 - 2 * lid)), 0.12, 0.12, P['skin_sh'])
    for k, (c, r) in enumerate(eyes):                                                                        # flat thin brows
        up = 0.4 if expr == 'shock' else 0.0
        s_ = 1 if k == 0 else -1
        tilt = 0.18 if expr == 'smug' else 0.0
        cap(Hd, (c[0] - 0.5, c[1] - r - 0.55 - up + s_ * tilt), (c[0] + 0.5, c[1] - r - 0.55 - up - s_ * tilt), 0.13, 0.11, P['brow'])
    poly(Hd, [Fh(2.6, 27.1), Fh(3.25, 26.0), Fh(2.6, 25.85)], P['skin_sh'])                                   # straight nose
    poly(Hd, [Fh(2.6, 27.0), Fh(3.1, 26.05), Fh(2.65, 26.0)], P['skin'])
    for k in range(3): dot(Hd, Fh(0.6 + k * 0.5, 26.3 - (k % 2) * 0.3), (226, 150, 140), 0.13)                # a couple of pimples
    mm = max(m, 0.5 if expr == 'shock' else 0.0)
    mc = Fh(2.0, 25.15 - 0.2 * mm)
    mouth(Hd, mc, 0.62, mm, 'smug' if expr in ('smug', 'happy') else 'normal', lip=(190, 120, 116))
    # a cloud of dark curls: overlapping circles, falling over the forehead
    rng = np.random.default_rng(7)
    ell(Hd, Fh(0.55, 30.0), 2.75, 1.75, P['hair_sh'])                                                        # hair mass over the skull
    poly(Hd, [Fh(-1.9, 28.9), Fh(3.0, 29.1), Fh(2.9, 30.0), Fh(-1.9, 30.0)], P['hair_sh'])
    for i in range(26):
        a = math.pi * (0.02 + 0.96 * i / 25)
        r_ = 2.25 + 0.25 * rng.random()
        cx_, ch_ = 0.6 + r_ * math.cos(a) * 1.05, 28.6 + r_ * math.sin(a) * 1.1
        ell(Hd, Fh(cx_, ch_), 0.78, 0.74, P['hair'], 0, P['hair_hi'], P['hair_sh'])
    for i in range(7):                                                                                        # fringe curls over the brow
        ell(Hd, Fh(0.0 + i * 0.48, 29.25 - (i % 2) * 0.2), 0.55, 0.48, P['hair'], 0, P['hair_hi'], P['hair_sh'])
    for i in range(14):
        a = rng.random() * math.pi; r_ = 1.6 + rng.random() * 1.4
        dot(Hd, Fh(0.6 + r_ * math.cos(a), 29.2 + r_ * math.sin(a) * 0.9), P['hair_hi'], 0.12)
    return mc


def phone_up(L, h, P=TC, screen=(70, 120, 200)):
    """vertical phone held by the hand h; we see its back with the camera and a red REC dot"""
    poly(L, [(h[0] - 0.55, h[1] - 2.4), (h[0] + 0.6, h[1] - 2.4), (h[0] + 0.6, h[1] + 0.2), (h[0] - 0.55, h[1] + 0.2)], P['phone'])
    cap(L, (h[0] - 0.55, h[1] - 2.4), (h[0] + 0.6, h[1] - 2.4), 0.1, 0.1, P['phone_hi'])
    dot(L, (h[0] - 0.2, h[1] - 2.0), (120, 130, 150), 0.2); dot(L, (h[0] - 0.2, h[1] - 2.0), (20, 20, 26), 0.11)
    dot(L, (h[0] + 0.25, h[1] - 2.05), (240, 50, 50), 0.12)


def tema(CH, cam, pose=None, t=0.0, mouth_=0.0, expr='deadpan', look=0.0, hand_n=None, hand_f=None, prop_n='phone', prop_f=None,
         lean=None, hood_up=False, blink=True, outline_=True):
    """expr: deadpan | smug | shock | happy. prop_n='phone' = filming (phone in the near hand)."""
    pose = pose or TPOSE['film']
    P = dict(TC)
    br = 0.1 * math.sin(t * 2.2)
    ln = pose.get('lean', 0.0) if lean is None else lean
    sh_n, sh_f = H(1.5 + ln, 22.0 + br), H(-1.5 + ln, 22.1 + br)
    hp_n, hp_f = H(0.7, 13.6), H(-0.7, 13.6)
    pants = (P['pants'], P['pants_hi'], P['pants_sh'])
    hood = (P['hood'], P['hood_hi'], P['hood_sh'])
    L = Layer(cam)
    for hp, lg, side in ((hp_f, pose['fleg'], -1), (hp_n, pose['nleg'], 1)):                                   # wide pants, chunky sneakers
        A = Layer(cam)
        k_, e_ = _limb(A, hp, *lg, 7.0, 6.6, 1.2, 1.15, *pants)
        cap(A, (e_[0] - 1.1, e_[1] - 0.4), (e_[0] + 1.1, e_[1] - 0.4), 0.3, 0.3, P['pants_sh'])
        ellt(A, (e_[0] + 0.9, e_[1] + 0.25), 2.05, 0.95, (P['shoe'], (255, 255, 255), P['shoe_sh']))
        cap(A, (e_[0] - 1.0, e_[1] + 0.95), (e_[0] + 2.8, e_[1] + 0.95), 0.32, 0.32, P['sole'])
        for k in range(3): dot(A, (e_[0] + 0.4 + k * 0.5, e_[1] - 0.1), (210, 60, 60), 0.1)
        _merge(L, A, OL)
    A = Layer(cam)                                                                                              # far arm in a long sleeve
    tf = hand_f if hand_f is not None else H(pose['f'][0], pose['f'][1])
    kf, ef = _limb(A, sh_f, 0, 0, 5.0, 4.7, 1.15, 1.0, *hood, target=tf, bend=pose.get('bf', -1))
    ell(A, ef, 0.62, 0.6, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    cap(A, (ef[0] - 0.9, ef[1] - 0.6), (ef[0] + 0.1, ef[1] - 0.2), 0.75, 0.7, P['hood_sh'])                   # sleeve swallows the hand
    if prop_f: prop_f(A, ef)
    _merge(L, A, OL)
    T = Layer(cam)                                                                                              # boxy oversized hoodie
    poly(T, [H(-2.9 + ln * 0.5, 22.6 + br), H(2.9 + ln * 0.5, 22.6 + br), H(3.3, 14.6), H(3.0, 12.4), H(-2.9, 12.4), H(-3.2, 14.6)], P['hood'])
    ellt(T, H(0.0 + ln * 0.4, 18.6 + br), 3.1, 4.3, hood)
    poly(T, [H(-1.2, 16.2), H(2.3, 16.2), H(2.7, 13.6), H(-1.5, 13.6)], P['hood_sh'])                         # kangaroo pocket
    cap(T, H(-1.2, 16.2), H(2.3, 16.2), 0.12, 0.12, P['hood_hi'])
    for k in range(7): cap(T, H(-2.7 + k * 0.9, 12.45), H(-2.65 + k * 0.9, 13.0), 0.12, 0.12, P['hood_sh'])  # ribbed hem
    cap(T, H(0.3, 22.0), H(0.5, 19.0), 0.1, 0.1, P['string']); cap(T, H(1.3, 22.0), H(1.5, 18.8), 0.1, 0.1, P['string'])
    dot(T, H(0.5, 18.9), P['string'], 0.16); dot(T, H(1.5, 18.7), P['string'], 0.16)
    ellt(T, H(-1.0 + ln * 0.5, 23.0 + br), 2.4, 1.0, hood)                                                     # bunched hood
    cap(T, H(-1.2 + ln * 0.5, 23.6 + br), H(2.3 + ln * 0.5, 23.2 + br), 0.55, 0.55, P['cans'], P['cans_hi'])  # headphones on the neck
    ell(T, H(-1.4 + ln * 0.5, 23.2 + br), 0.75, 0.9, P['cans'], 0, P['cans_hi'])
    ell(T, H(2.4 + ln * 0.5, 22.9 + br), 0.75, 0.9, P['cans'], 0, P['cans_hi'])
    _merge(L, T, OL)
    Hd = Layer(cam)
    hx = 0.3 + ln * 1.0

    def Fh(x, h): return H(hx + x - 0.3, h + br)
    mc = _tema_head(Hd, Fh, P, expr, t, mouth_, look, blink)
    _merge(L, Hd, OL)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(pose['n'][0], pose['n'][1])
    kn, en = _limb(A, sh_n, 0, 0, 5.0, 4.7, 1.2, 1.0, *hood, target=tn, bend=pose.get('bn', 1))
    ell(A, en, 0.66, 0.62, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_n == 'phone': phone_up(A, en)
    elif prop_n: prop_n(A, en)
    _merge(L, A, OL)
    if outline_: outline(L, OL)
    CH.add(L)
    return dict(hand_n=en, hand_f=ef, mouth=mc, head=Fh(1.0, 27.4), top=Fh(0.6, 31.0))


# ======================================================================================= IRA (mum)
IC = dict(skin=(244, 200, 172), skin_hi=(255, 224, 200), skin_sh=(208, 156, 130), cheek=(240, 150, 140),
          hair=(104, 36, 86), hair_hi=(150, 70, 128), hair_sh=(70, 20, 58), brow=(80, 30, 60),
          card=(214, 164, 40), card_hi=(240, 196, 80), card_sh=(166, 120, 20), blouse=(46, 92, 86), button=(120, 76, 30),
          pants=(52, 46, 70), pants_hi=(80, 74, 100), pants_sh=(32, 28, 46), slip=(200, 50, 60), pom=(255, 220, 226),
          lip=(222, 96, 86), glass=(196, 156, 60), coat=(150, 104, 70), coat_hi=(186, 138, 98), coat_sh=(106, 70, 46),
          scarf=(150, 160, 176), scarf_hi=(190, 200, 214), scarf_sh=(110, 118, 136))
IPOSE = dict(
    stand=dict(n=(2.2, 9.6), f=(-2.0, 9.8), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
    tray=dict(n=(4.0, 12.6), f=(3.4, 12.8), bn=1, bf=1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),        # carrying a tray
    hips=dict(n=(1.9, 10.8), f=(-1.9, 10.9), bn=-1, bf=1, nleg=(0.12, 0.0), fleg=(-0.12, 0.0)),      # hands on hips
    spoon=dict(n=(2.6, 18.6), f=(3.2, 13.0), bn=1, bf=1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),       # spoon to the mouth
    sneeze=dict(n=(2.9, 18.2), f=(3.0, 12.6), bn=1, bf=1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
)


def _ira_head(Hd, Fh, P, expr, t, m, look, blink, sick, specs):
    cap(Hd, Fh(0.4, 17.8), Fh(0.6, 19.6), 0.7, 0.65, P['skin'], P['skin_hi'], P['skin_sh'])
    poly(Hd, [Fh(-1.95, 23.9), Fh(2.9, 24.1), Fh(3.0, 21.0), Fh(2.3, 19.5), Fh(-1.8, 19.3), Fh(-2.1, 21.4)], P['hair'])   # bob back
    ell(Hd, Fh(0.85, 21.4), 2.3, 2.45, P['skin'], 0, P['skin_hi'], P['skin_sh'], th_sh=-0.7)                   # round face
    ell(Hd, Fh(1.2, 19.75), 1.4, 0.8, P['skin'], 0.1)
    ell(Hd, Fh(-1.05, 21.3), 0.55, 0.8, P['skin'], 0.1, P['skin_hi'], P['skin_sh'])
    dot(Hd, Fh(-1.05, 20.5), (246, 200, 70), 0.2)                                                               # gold earring
    ex = 'shock' if expr == 'shock' else 'squint' if expr in ('happy', 'sweet') else 'normal'
    eyes = [(Fh(1.15, 21.45), 0.5), (Fh(2.25, 21.4), 0.55)]
    bl = blink and (t % 3.5) < 0.1 and expr != 'shock'
    for c, r in eyes:
        eye(Hd, c, r, ex, (look, 0.0), iris=(70, 110, 60), lid=P['skin_sh'], blink=bl, lash=(40, 20, 30))
        if expr in ('tired', 'dry', 'sick') and not bl:                                                       # tired heavy lid
            cap(Hd, (c[0] - r * 1.05, c[1] - r * 0.35), (c[0] + r * 1.05, c[1] - r * 0.55), r * 0.38, r * 0.38, P['skin_sh'])
    for k, (c, r) in enumerate(eyes):
        s_ = 1 if k == 0 else -1
        bt = {'angry': 0.5, 'dry': 0.2, 'shock': -0.6, 'sick': -0.5, 'tired': -0.3}.get(expr, 0.0)
        base = c[1] - r - 0.55 - (0.35 if expr == 'shock' else 0)
        cap(Hd, (c[0] - 0.5, base - s_ * bt * 0.3), (c[0] + 0.5, base + s_ * bt * 0.3), 0.15, 0.11, P['brow'])
    if specs:                                                                                                    # glasses on the nose + gold chain
        for c, r in eyes:
            ell(Hd, c, r * 1.35, r * 1.2, P['glass']); ell(Hd, c, r * 1.15, r * 1.0, (230, 240, 246))
            eye(Hd, c, r, ex, (look, 0.0), iris=(70, 110, 60), lid=P['skin_sh'], blink=bl, lash=(40, 20, 30))
        cap(Hd, (eyes[0][0][0] + 0.6, eyes[0][0][1]), (eyes[1][0][0] - 0.65, eyes[1][0][1]), 0.08, 0.08, P['glass'])
        cap(Hd, (eyes[0][0][0] - 0.65, eyes[0][0][1]), Fh(-0.9, 19.0), 0.06, 0.06, P['glass'])
    nz = _mix(P['skin'], (230, 70, 70), sick)
    poly(Hd, [Fh(2.55, 21.7), Fh(3.15, 20.75), Fh(2.6, 20.55)], _mix(P['skin_sh'], (190, 50, 50), sick))         # small upturned nose
    poly(Hd, [Fh(2.55, 21.6), Fh(3.0, 20.8), Fh(2.62, 20.7)], nz)
    ell(Hd, Fh(1.9, 20.6), 0.55, 0.33, _mix(P['cheek'], (240, 80, 80), sick))
    mm = max(m, 0.5 if expr == 'shock' else 0.0)
    mc = Fh(2.1, 19.85 - 0.2 * mm)
    mouth(Hd, mc, 0.6, mm, 'smug' if expr in ('happy', 'sweet', 'smug') else 'sad' if expr in ('tired', 'sick') else 'normal', lip=P['lip'])
    # aubergine bob: helmet with a dead-straight fringe
    ell(Hd, Fh(0.7, 23.15), 2.55, 1.45, P['hair'], 0, P['hair_hi'], P['hair_sh'])
    poly(Hd, [Fh(-0.3, 23.4), Fh(3.15, 23.4), Fh(3.15, 22.6), Fh(-0.3, 22.6)], P['hair'])                     # straight fringe
    cap(Hd, Fh(-0.2, 22.62), Fh(3.1, 22.62), 0.1, 0.1, P['hair_sh'])
    cap(Hd, Fh(-0.1, 24.15), Fh(2.4, 24.35), 0.16, 0.16, P['hair_hi'])
    poly(Hd, [Fh(-1.85, 23.0), Fh(-0.5, 23.0), Fh(-0.4, 19.9), Fh(-2.0, 19.7)], P['hair'])                      # side
    if sick > 0.3: _sweat(Hd, Fh, t, n=2, seed=3, area=((0.4, 22.0), (2.4, 23.0)))
    return mc


def ira(CH, cam, pose=None, t=0.0, mouth_=0.0, expr='dry', look=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
        coat=False, scarf=False, legs=True, sick=0.0, specs=False, blink=True, outline_=True):
    """expr: dry | tired | happy | sweet | shock | angry | sick. coat: going-out coat; scarf: knitted grey scarf; sick: red nose."""
    pose = pose or IPOSE['stand']
    P = dict(IC)
    br = 0.1 * math.sin(t * 2.3)
    sh_n, sh_f = H(1.6, 17.6 + br), H(-1.7, 17.7 + br)
    hp_n, hp_f = H(0.8, 9.6), H(-0.8, 9.6)
    pants = (P['pants'], P['pants_hi'], P['pants_sh'])
    top = (P['coat'], P['coat_hi'], P['coat_sh']) if coat else (P['card'], P['card_hi'], P['card_sh'])
    L = Layer(cam)
    if legs:
        for hp, lg in ((hp_f, pose['fleg']), (hp_n, pose['nleg'])):
            A = Layer(cam)
            k_, e_ = _limb(A, hp, *lg, 5.0, 4.6, 1.05, 0.85, *pants)
            ellt(A, (e_[0] + 0.7, e_[1] + 0.3), 1.45, 0.55, (P['slip'], (230, 90, 100), (150, 30, 40)))
            dot(A, (e_[0] + 1.6, e_[1] - 0.2), P['pom'], 0.42)                                                # pompon slippers
            _merge(L, A, OL)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(pose['f'][0], pose['f'][1])
    kf, ef = _limb(A, sh_f, 0, 0, 3.8, 3.5, 0.95, 0.8, *top, target=tf, bend=pose.get('bf', -1))
    ell(A, ef, 0.72, 0.7, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_f: prop_f(A, ef)
    _merge(L, A, OL)
    T = Layer(cam)                                                                                              # compact barrel body
    poly(T, [H(-2.3, 18.4 + br), H(2.3, 18.4 + br), H(2.9, 13.0), H(2.8, 7.2 if coat else 8.6), H(-2.7, 7.2 if coat else 8.6), H(-2.9, 13.0)], top[0])
    ellt(T, H(0.0, 14.6 + br), 2.85, 4.0, top)
    if not coat:
        poly(T, [H(0.1, 18.3 + br), H(1.5, 18.3 + br), H(1.0, 13.4), H(0.6, 13.4)], P['blouse'])               # blouse in the V
        for k in range(4): dot(T, H(1.15 - k * 0.05, 16.4 - k * 1.8), P['button'], 0.2)
        for k in range(8): cap(T, H(-2.6 + k * 0.72, 8.7), H(-2.55 + k * 0.72, 9.3), 0.1, 0.1, P['card_sh'])   # knit hem
        cap(T, H(0.1, 18.3 + br), H(1.0, 8.7), 0.12, 0.12, P['card_sh'])
    else:
        cap(T, H(0.9, 18.2), H(1.3, 7.3), 0.12, 0.12, P['coat_sh'])
        for k in range(3): dot(T, H(1.6, 16.0 - k * 2.4), (60, 40, 30), 0.2)
    if scarf:
        sc = (P['scarf'], P['scarf_hi'], P['scarf_sh'])
        ellt(T, H(0.2, 18.4 + br), 2.4, 1.0, sc)
        cap(T, H(1.4, 18.0), H(1.8, 13.6), 0.6, 0.5, *sc)
        for k in range(4): cap(T, H(1.2 + k * 0.2, 13.5), H(1.25 + k * 0.2, 12.9), 0.07, 0.07, P['scarf_sh'])
    _merge(L, T, OL)
    Hd = Layer(cam)

    def Fh(x, h): return H(x, h + br)
    mc = _ira_head(Hd, Fh, P, expr, t, mouth_, look, blink, sick, specs)
    _merge(L, Hd, OL)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(pose['n'][0], pose['n'][1])
    kn, en = _limb(A, sh_n, 0, 0, 3.8, 3.5, 1.0, 0.82, *top, target=tn, bend=pose.get('bn', 1))
    ell(A, en, 0.75, 0.72, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_n: prop_n(A, en)
    _merge(L, A, OL)
    if outline_: outline(L, OL)
    CH.add(L)
    return dict(hand_n=en, hand_f=ef, mouth=mc, head=Fh(1.0, 21.5), top=Fh(0.7, 24.6))


# ======================================================================================= props (unit coords, held in a hand)
def thermometer(L, h, ang=-0.6, size=1.0):
    """digital thermometer in a hand: white body, grey metal tip; the LCD digits are a decal added by the shot"""
    d = (math.cos(ang), math.sin(ang))
    a = (h[0] + d[0] * 0.2 * size, h[1] + d[1] * 0.2 * size)
    b = (h[0] + d[0] * 3.4 * size, h[1] + d[1] * 3.4 * size)
    cap(L, a, b, 0.42 * size, 0.3 * size, (244, 244, 248), (255, 255, 255), (196, 200, 210))
    cap(L, b, (b[0] + d[0] * 0.7 * size, b[1] + d[1] * 0.7 * size), 0.16 * size, 0.12 * size, (180, 186, 196))
    m = (h[0] + d[0] * 1.6 * size, h[1] + d[1] * 1.6 * size)
    cap(L, (m[0] - d[0] * 0.6 * size, m[1] - d[1] * 0.6 * size), (m[0] + d[0] * 0.6 * size, m[1] + d[1] * 0.6 * size), 0.24 * size, 0.24 * size,
        (178, 196, 150))
    return m


def bell(L, h, t=0.0, ring=1.0):
    """brass hand bell, swinging"""
    sw = 0.45 * ring * math.sin(t * 22.0)
    top = (h[0] + 0.1, h[1] - 0.6)
    cap(L, (h[0], h[1] + 0.2), top, 0.28, 0.24, (90, 56, 30))
    cx, cy = top[0] + sw * 0.8, top[1] - 1.5
    poly(L, [(cx - 0.6, cy - 0.5), (cx + 0.6, cy - 0.5), (cx + 1.3, cy + 1.1), (cx - 1.3, cy + 1.1)], (226, 176, 60))
    ell(L, (cx, cy - 0.45), 0.62, 0.45, (240, 200, 90))
    cap(L, (cx - 1.3, cy + 1.1), (cx + 1.3, cy + 1.1), 0.2, 0.2, (176, 126, 30))
    dot(L, (cx - 0.3, cy), (255, 240, 180), 0.2)
    dot(L, (cx + sw * 0.6, cy + 1.45), (150, 100, 30), 0.26)


def ladle(L, h):
    cap(L, (h[0], h[1] + 0.3), (h[0] + 2.6, h[1] - 2.2), 0.16, 0.14, (180, 186, 196))
    ell(L, (h[0] + 2.9, h[1] - 2.3), 0.75, 0.45, (200, 206, 216), 0, (240, 244, 250), (140, 146, 160))


def spoon(L, h):
    cap(L, (h[0], h[1]), (h[0] + 1.4, h[1] - 1.2), 0.1, 0.08, (200, 206, 216))
    ell(L, (h[0] + 1.55, h[1] - 1.3), 0.35, 0.22, (220, 226, 236))


def tray(L, h, t=0.0, steam=True):
    """tray with a bowl of broth, a slice of lemon and a jar of raspberry jam (carried with both hands)"""
    cap(L, (h[0] - 3.6, h[1] - 0.2), (h[0] + 1.0, h[1] - 0.2), 0.26, 0.26, (176, 120, 70), (206, 150, 96), (130, 84, 44))
    ell(L, (h[0] - 1.6, h[1] - 0.9), 1.5, 0.75, (246, 246, 240), 0, (255, 255, 255), (206, 210, 216))
    ell(L, (h[0] - 1.6, h[1] - 1.2), 1.15, 0.32, (236, 196, 90))
    ell(L, (h[0] + 0.0, h[1] - 0.9), 0.55, 0.75, (176, 30, 60), 0, (214, 60, 90), (120, 16, 40))       # raspberry jam jar
    cap(L, (h[0] - 0.5, h[1] - 1.6), (h[0] + 0.5, h[1] - 1.6), 0.2, 0.2, (240, 240, 236))


def pills_box(L, x, y, w, hgt, col, stripe):
    poly(L, [(x, y), (x + w, y), (x + w, y - hgt), (x, y - hgt)], col)
    cap(L, (x + 0.1 * w, y - hgt * 0.55), (x + 0.9 * w, y - hgt * 0.55), hgt * 0.12, hgt * 0.12, stripe)


def battery(L, h, w=1.0):
    """car battery «АКБ» held in front: black box, red and blue terminals, a carry strap"""
    x, y = h[0] + 0.6 * w, h[1]
    poly(L, [(x - 1.6 * w, y - 1.8 * w), (x + 1.6 * w, y - 1.8 * w), (x + 1.6 * w, y + 0.6 * w), (x - 1.6 * w, y + 0.6 * w)], (34, 34, 40))
    poly(L, [(x - 1.6 * w, y - 1.8 * w), (x + 1.6 * w, y - 1.8 * w), (x + 1.5 * w, y - 1.5 * w), (x - 1.5 * w, y - 1.5 * w)], (70, 70, 82))
    cap(L, (x - 1.0 * w, y - 1.9 * w), (x - 1.0 * w, y - 2.2 * w), 0.22 * w, 0.22 * w, (210, 40, 40))
    cap(L, (x + 1.0 * w, y - 1.9 * w), (x + 1.0 * w, y - 2.2 * w), 0.22 * w, 0.22 * w, (40, 80, 200))
    poly(L, [(x - 1.0 * w, y - 0.9 * w), (x + 1.0 * w, y - 0.9 * w), (x + 1.0 * w, y - 0.2 * w), (x - 1.0 * w, y - 0.2 * w)], (246, 206, 30))


def battery_world(L, x, y, s=1.0):
    """battery lying in bed, world px (bottom-centre x, y)"""
    poly(L, [(x - 22 * s, y - 26 * s), (x + 22 * s, y - 26 * s), (x + 22 * s, y), (x - 22 * s, y)], (34, 34, 40))
    poly(L, [(x - 22 * s, y - 26 * s), (x + 22 * s, y - 26 * s), (x + 20 * s, y - 22 * s), (x - 20 * s, y - 22 * s)], (70, 70, 82))
    cap(L, (x - 13 * s, y - 27 * s), (x - 13 * s, y - 31 * s), 3 * s, 3 * s, (210, 40, 40))
    cap(L, (x + 13 * s, y - 27 * s), (x + 13 * s, y - 31 * s), 3 * s, 3 * s, (40, 80, 200))
    poly(L, [(x - 13 * s, y - 15 * s), (x + 13 * s, y - 15 * s), (x + 13 * s, y - 6 * s), (x - 13 * s, y - 6 * s)], (246, 206, 30))


NB = [dict(coat=(70, 90, 130), hat=(110, 80, 50), scarf=(200, 60, 60), skin=(236, 190, 160)),
      dict(coat=(120, 60, 50), hat=(60, 60, 70), scarf=(230, 200, 80), skin=(226, 176, 146)),
      dict(coat=(60, 100, 70), hat=(150, 40, 60), scarf=(240, 240, 240), skin=(240, 200, 172)),
      dict(coat=(90, 80, 110), hat=(120, 110, 100), scarf=(90, 150, 200), skin=(232, 186, 150))]


def neighbour(CH, cam, t=0.0, kind=0, mouth_=0.0, expr='normal', held=True):
    """a neighbour in a winter coat and fur hat holding his car battery (the queue in E02)"""
    P = NB[kind % len(NB)]
    sk = (P['skin'], _mix(P['skin'], (255, 255, 255), 0.25), _mix(P['skin'], (120, 70, 50), 0.25))
    co = (P['coat'], _mix(P['coat'], (255, 255, 255), 0.2), _mix(P['coat'], (0, 0, 0), 0.3))
    br = 0.1 * math.sin(t * 2.2 + kind)
    L = Layer(cam)
    for x0 in (-0.9, 0.9):
        cap(L, H(x0, 9.5), H(x0, 0.6), 0.9, 0.8, (40, 40, 48))
        ellt(L, H(x0 + 0.6, 0.4), 1.4, 0.55, ((50, 36, 30), (80, 60, 50), (30, 20, 16)))
    ellt(L, H(0.0, 13.8 + br), 3.0, 6.0, co)
    for k in range(4): dot(L, H(0.9, 17.0 - k * 2.0), (40, 30, 30), 0.2)
    ellt(L, H(0.2, 19.6 + br), 2.2, 0.9, (P['scarf'], _mix(P['scarf'], (255, 255, 255), 0.3), _mix(P['scarf'], (0, 0, 0), 0.3)))
    ell(L, H(0.6, 22.2 + br), 2.0, 2.2, sk[0], 0, sk[1], sk[2])
    ell(L, H(2.4, 21.9 + br), 0.55, 0.45, _mix(P['skin'], (230, 90, 90), 0.5))                   # red frosty nose
    eye(L, H(1.2, 22.7 + br), 0.38, 'shock' if expr == 'shock' else 'normal', (0.4, 0.0), iris=(70, 60, 50))
    eye(L, H(2.0, 22.7 + br), 0.42, 'shock' if expr == 'shock' else 'normal', (0.4, 0.0), iris=(70, 60, 50))
    cap(L, H(0.8, 23.5 + br), H(1.5, 23.4 + br), 0.12, 0.1, (70, 50, 40)); cap(L, H(1.7, 23.4 + br), H(2.4, 23.5 + br), 0.12, 0.1, (70, 50, 40))
    mouth(L, H(1.7, 21.0 + br), 0.5, mouth_, 'happy' if expr == 'happy' else 'normal', lip=(170, 90, 80))
    ellt(L, H(0.5, 25.1 + br), 2.4, 1.3, (P['hat'], _mix(P['hat'], (255, 255, 255), 0.25), _mix(P['hat'], (0, 0, 0), 0.3)))   # fur hat
    for sx in (-1.6,): ellt(L, H(sx, 22.6 + br), 0.7, 1.4, (P['hat'], _mix(P['hat'], (255, 255, 255), 0.25), _mix(P['hat'], (0, 0, 0), 0.3)))
    hand = H(2.8, 14.0)
    cap(L, H(1.6, 18.6), hand, 0.85, 0.75, *co)
    ell(L, hand, 0.7, 0.65, sk[0], 0, sk[1], sk[2])
    if held: battery(L, (hand[0] + 0.4, hand[1] + 0.4), 0.9)
    outline(L, OL)
    CH.add(L)
    return dict(head=H(0.8, 22.2 + br), mouth=H(1.7, 21.0 + br))


def hot_water_bottle(L, x, y, s=1.0):
    ell(L, (x, y), 18 * s, 13 * s, (214, 60, 60), 0, (240, 100, 100), (160, 30, 30))
    cap(L, (x + 16 * s, y - 4 * s), (x + 24 * s, y - 8 * s), 4 * s, 3.5 * s, (160, 30, 30))

