"""Cast of «Aura Dad» (US): Doug Pruitt (46, «light bulb» silhouette: huge shiny dome with a five-strand comb-over, NO chin — the
head flows straight into the neck, narrow shoulders, round belly, polo tucked into cargo shorts, tube socks, wrap-around shades on the
dome), Kayden (14, «noodle with broccoli»: lanky, curly broccoli top with faded sides, oversized hoodie, phone always out), Tammy (44,
«mug»: pineapple bun, huge cardigan, LIVE LAUGH LATTE mug) and MIRRA (smart-mirror face drawn on glass / a fridge screen).
Same drawing conventions as props/folk.py (anchor (1000,1000) = floor point under the character, H(x, h), +x = facing, 3-tone
shading); the face helpers eye()/mouth() are shared drawing primitives, silhouettes/palettes are this series' own."""
import math
import numpy as np
from scene import Layer
from props.folk import H, cap, ell, ellt, dot, poly, outline, _limb, _merge
from props.teshcast import eye, mouth

OL = (38, 20, 52)                      # dark plum-violet outline (series colour)


def _mix(a, b, k):
    return tuple(int(x + (y - x) * k) for x, y in zip(a, b))


# ======================================================================================= DOUG
DC = dict(skin=(246, 196, 160), skin_hi=(255, 224, 196), skin_sh=(212, 152, 122), cheek=(240, 140, 128), red=(236, 92, 84),
          dome_hi=(255, 246, 232), hair=(150, 112, 80), must=(130, 92, 62), brow=(112, 78, 52),
          polo=(110, 178, 230), polo_hi=(160, 210, 248), polo_sh=(70, 132, 192), collar=(240, 246, 252),
          short=(196, 170, 112), short_hi=(222, 200, 146), short_sh=(156, 130, 80), belt=(96, 62, 40), buckle=(230, 200, 90),
          sock=(250, 250, 246), sock_sh=(206, 208, 214), shoe=(244, 244, 246), shoe_sh=(190, 194, 204), sole=(150, 150, 160),
          shade=(70, 40, 110), shade_hi=(160, 230, 240), holster=(40, 36, 44), legh=(170, 120, 90))
DPOSE = dict(
    stand=dict(n=(2.8, 11.6), f=(-2.6, 11.8), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),
    hips=dict(n=(3.6, 12.6), f=(-3.4, 12.6), bn=-1, bf=1, nleg=(0.16, 0.0), fleg=(-0.16, 0.0)),
    shout=dict(n=(6.0, 21.0), f=(-4.6, 20.6), bn=1, bf=-1, nleg=(0.2, 0.0), fleg=(-0.2, 0.0)),            # arms flung out
    cheer=dict(n=(7.2, 25.4), f=(-5.2, 25.6), bn=1, bf=-1, nleg=(0.18, 0.0), fleg=(-0.18, 0.0)),          # both fists up
    mug=dict(n=(4.6, 16.2), f=(-2.6, 11.8), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),            # coffee mug at the belly
    point=dict(n=(3.2, 19.0), f=(-2.6, 11.8), bn=1, bf=-1, nleg=(0.05, 0.0), fleg=(-0.05, 0.0)),          # thumb at his own chest
    fists=dict(n=(3.8, 15.4), f=(-1.0, 15.2), bn=1, bf=-1, nleg=(0.1, 0.0), fleg=(-0.1, 0.0)),            # fists clenched, mewing hard
)


def _doug_head(Hd, Fh, P, expr, t, m, look, blink, shine, mask=False):
    sk = (P['skin'], P['skin_hi'], P['skin_sh'])
    # no chin: a fat neck as wide as the jaw
    cap(Hd, Fh(0.2, 20.6), Fh(0.7, 23.2), 2.35, 2.25, *sk)
    ell(Hd, Fh(-2.0, 24.9), 0.75, 1.05, P['skin'], 0.1, P['skin_hi'], P['skin_sh'])                      # ear
    ell(Hd, Fh(-2.0, 24.9), 0.38, 0.62, P['cheek'])
    puff = expr == 'mew'
    # the light-bulb dome: wide on top, narrow at the jaw
    ell(Hd, Fh(0.5, 26.4), 3.45, 3.85, P['skin'], 0, P['skin_hi'], P['skin_sh'], th_sh=-0.6)
    ell(Hd, Fh(1.2, 23.4), 2.55 + (0.55 if puff else 0.0), 1.85, P['skin'], 0, None, P['skin_sh'], th_sh=-0.75)
    ell(Hd, Fh(1.7, 22.25), 1.7, 0.42, P['skin_sh'])                                                     # neck crease (no chin)
    ell(Hd, Fh(-0.9, 28.8), 1.3, 0.8, P['dome_hi'], -0.5)                                                # dome shine
    dot(Hd, Fh(0.3, 29.4), (255, 255, 255), 0.35)
    for k in range(5):                                                                                    # five-strand comb-over
        a0 = Fh(-2.5 + 0.1 * k, 26.6 + 0.55 * k)
        a1 = Fh(0.0 + 0.2 * k, 29.6 + 0.12 * k - (0.1 * k * k * 0.1))
        a2 = Fh(2.7 + 0.15 * k, 28.4 + 0.25 * k)
        cap(Hd, a0, a1, 0.1, 0.12, P['hair']); cap(Hd, a1, a2, 0.12, 0.08, P['hair'])
    cap(Hd, Fh(-1.7, 26.4), Fh(-2.3, 25.9), 0.22, 0.16, (168, 150, 140))                                 # grey tuft over the ear
    if mask:                                                                                              # white sheet face mask
        ell(Hd, Fh(1.75, 24.3), 2.35, 2.3, (248, 248, 244), 0, (255, 255, 255), (214, 216, 222))
    # wrap-around shades pushed up on the dome
    cap(Hd, Fh(0.4, 28.7), Fh(3.7, 28.2), 0.62, 0.55, P['shade'])
    cap(Hd, Fh(1.1, 28.95), Fh(2.6, 28.75), 0.14, 0.12, P['shade_hi'])
    cap(Hd, Fh(-1.6, 28.4), Fh(0.5, 28.75), 0.16, 0.16, (30, 26, 34))
    # face
    ex = {'shout': 'shout', 'shock': 'shock', 'smug': 'smug', 'proud': 'normal', 'mew': 'squint', 'angry': 'normal',
          'happy': 'squint', 'sad': 'normal'}.get(expr, 'normal')
    eyes = [(Fh(1.55, 25.55), 0.5), (Fh(2.8, 25.45), 0.58)]
    bl = blink and (t % 3.7) < 0.1 and expr not in ('shout', 'shock')
    for c, r in eyes:
        eye(Hd, c, r, ex, (look, 0.0), iris=(70, 96, 140), lid=P['skin_sh'], blink=bl, bulge=1.05)
    bt = {'angry': 0.65, 'shout': 0.5, 'shock': -0.6, 'proud': -0.35, 'smug': 0.25, 'sad': -0.6, 'mew': 0.55, 'happy': -0.45}.get(expr, 0.0)
    lift = 0.5 if expr in ('shock',) else 0.0
    for k, (c, r) in enumerate(eyes):
        s_ = 1 if k == 0 else -1
        b = c[1] - r - 0.45 - lift
        cap(Hd, (c[0] - 0.55, b - s_ * bt * 0.35 + 0.0), (c[0] + 0.55, b + s_ * bt * 0.35), 0.22, 0.18, P['brow'])
    red = expr in ('shout', 'angry', 'mew')
    if not mask:
      ell(Hd, Fh(1.4, 24.0), 0.75 + (0.45 if puff else 0), 0.5 + (0.3 if puff else 0), P['red'] if red else P['cheek'])
      ell(Hd, Fh(3.25, 24.05), 0.45 + (0.3 if puff else 0), 0.4 + (0.25 if puff else 0), P['red'] if red else P['cheek'])
    ell(Hd, Fh(3.75, 24.75), 0.6, 0.55, P['skin'], 0, P['skin_hi'], P['skin_sh'])                         # button nose
    dot(Hd, Fh(3.6, 24.95), P['skin_hi'], 0.17)
    if puff:                                                                                               # mewing: lips pressed shut
        ell(Hd, Fh(3.05, 23.05), 0.55, 0.22, (190, 100, 96))
        cap(Hd, Fh(2.6, 23.1), Fh(3.5, 23.0), 0.1, 0.1, (120, 50, 50))
        mc = Fh(3.05, 23.05)
    else:
        mm = max(m, {'shout': 0.75, 'shock': 0.55}.get(expr, 0.0))
        mc = Fh(2.9, 23.0 - 0.2 * mm)
        mouth(Hd, mc, 0.75, mm, {'proud': 'grin', 'smug': 'smug', 'happy': 'grin'}.get(expr, 'sad' if expr in ('sad', 'angry') else 'normal'),
              lip=(186, 100, 92))
    cap(Hd, Fh(2.35, 23.72), Fh(3.45, 23.78), 0.2, 0.22, P['must'])                                      # little brush moustache
    if shine > 0:                                                                                          # proud twinkle on the dome
        c = Fh(-0.6, 29.2); r = 0.6 + 1.6 * shine
        cap(Hd, (c[0] - r, c[1]), (c[0] + r, c[1]), 0.12, 0.12, (255, 255, 255))
        cap(Hd, (c[0], c[1] - r), (c[0], c[1] + r), 0.12, 0.12, (255, 255, 255))
        dot(Hd, c, (255, 255, 230), 0.35)
    return mc


def doug(CH, cam, pose=None, t=0.0, mouth_=0.0, expr='normal', look=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
         lean=0.0, shake=0.0, shine=0.0, blink=True, outline_=True, bob=0.0, mask=False, band=False):
    """expr: normal | shout | shock | proud | smug | angry | sad | happy | mew (cheeks puffed, lips pressed, tongue up).
    shine: 0..1 twinkle star on the dome. bob: belly/breath bob amplitude."""
    pose = pose or DPOSE['stand']
    P = DC
    br = 0.15 * math.sin(t * 2.3) + bob * math.sin(t * 9.0)
    jx = shake * math.sin(t * 45.0)
    ln = lean + jx
    sh_n, sh_f = H(1.6 + ln, 20.4 + br), H(-1.2 + ln, 20.6 + br)
    hp_n, hp_f = H(1.0, 11.4), H(-0.6, 11.4)
    polo = (P['polo'], P['polo_hi'], P['polo_sh'])
    sk = (P['skin'], P['skin_hi'], P['skin_sh'])
    shorts = (P['short'], P['short_hi'], P['short_sh'])
    L = Layer(cam)

    def leg(hp, lg, side):
        A = Layer(cam)
        k, e = _limb(A, hp, *lg, 5.6, 5.4, 1.05, 0.72, *sk)
        for j in range(3):                                                                               # hairy shins
            dot(A, (k[0] + (e[0] - k[0]) * (0.25 + 0.2 * j) + 0.25, k[1] + (e[1] - k[1]) * (0.25 + 0.2 * j)), P['legh'], 0.1)
        cap(A, (e[0], e[1] - 3.3), (e[0], e[1] - 0.4), 0.82, 0.8, P['sock'], None, P['sock_sh'])          # tube socks
        cap(A, (e[0] - 0.7, e[1] - 2.6), (e[0] + 0.7, e[1] - 2.6), 0.12, 0.12, (110, 150, 220))
        ellt(A, (e[0] + 0.9, e[1] + 0.25), 1.9, 0.85, (P['shoe'], (255, 255, 255), P['shoe_sh']))           # dad sneakers
        cap(A, (e[0] - 0.9, e[1] + 0.95), (e[0] + 2.7, e[1] + 0.95), 0.25, 0.25, P['sole'])
        cap(A, hp, (k[0] * 0.55 + hp[0] * 0.45, k[1] * 0.55 + hp[1] * 0.45 - 0.0), 1.45, 1.55, *shorts)   # cargo shorts leg
        ell(A, (hp[0] + (k[0] - hp[0]) * 0.45 + 0.9 * side, hp[1] + (k[1] - hp[1]) * 0.45), 0.6, 0.75, P['short_sh'])  # cargo pocket
        _merge(L, A, OL)
        return e

    leg(hp_f, pose['fleg'], -1)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(pose['f'][0] + jx, pose['f'][1])
    ka, ea = _limb(A, sh_f, 0, 0, 4.1, 3.9, 0.82, 0.62, *sk, target=tf, bend=pose.get('bf', -1))
    ell(A, sh_f, 1.25, 1.05, P['polo'], 0, P['polo_hi'], P['polo_sh'])                                    # short sleeve
    ellt(A, ea, 0.85, 0.8, sk)
    if prop_f: prop_f(A, ea)
    _merge(L, A, OL)
    leg(hp_n, pose['nleg'], 1)
    # torso: narrow chest + big round belly in a tucked polo
    T = Layer(cam)
    ellt(T, H(0.0, 11.9), 2.7, 1.6, shorts)
    ellt(T, H(0.25 + ln * 0.5, 18.7 + br), 2.55, 2.6, polo)
    ellt(T, H(1.2 + ln * 0.3, 15.3 + br * 0.6), 3.55, 3.75, polo)
    cap(T, H(-2.0, 12.4), H(4.0, 12.6), 0.55, 0.55, P['belt'])
    ell(T, H(3.4, 12.6), 0.5, 0.45, P['buckle'])
    ell(T, H(-1.6, 12.0), 0.7, 0.95, P['holster'])                                                         # phone holster
    cap(T, H(0.9 + ln * 0.6, 21.3 + br), H(1.5 + ln * 0.5, 18.7 + br), 0.16, 0.16, P['polo_sh'])          # placket + buttons
    dot(T, H(1.25 + ln * 0.55, 20.1 + br), P['collar'], 0.17); dot(T, H(1.4 + ln * 0.5, 19.2 + br), P['collar'], 0.17)
    poly(T, [H(-1.2 + ln * 0.6, 21.5 + br), H(1.0 + ln * 0.6, 21.0 + br), H(0.4 + ln * 0.6, 20.3 + br)], P['collar'])
    poly(T, [H(1.0 + ln * 0.6, 21.0 + br), H(2.6 + ln * 0.6, 21.3 + br), H(1.6 + ln * 0.6, 20.2 + br)], P['collar'])
    cap(T, H(2.8 + ln * 0.3, 16.5 + br * 0.6), H(4.0 + ln * 0.3, 14.6), 0.12, 0.12, P['polo_hi'])          # belly shine fold
    _merge(L, T, OL)
    Hd = Layer(cam)
    hx = 0.35 + ln * 1.1
    def Fh(x, h): return H(hx + x - 0.35, h + br)
    mc = _doug_head(Hd, Fh, P, expr, t, mouth_, look, blink, shine, mask)
    if band: spa_band(Hd, Fh(0.6, 27.6), 3.3, 1.0)
    _merge(L, Hd, OL)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(pose['n'][0] + jx, pose['n'][1])
    kna, ena = _limb(A, sh_n, 0, 0, 4.1, 3.9, 0.85, 0.64, *sk, target=tn, bend=pose.get('bn', 1))
    ell(A, sh_n, 1.3, 1.08, P['polo'], 0, P['polo_hi'], P['polo_sh'])
    ellt(A, ena, 0.88, 0.82, sk)
    if prop_n: prop_n(A, ena)
    _merge(L, A, OL)
    if outline_: outline(L, OL)
    CH.add(L)
    return dict(hand_n=ena, hand_f=ea, mouth=mc, head=Fh(1.0, 25.4), top=Fh(0.5, 30.3), chin=Fh(1.8, 22.3))


# ======================================================================================= KAYDEN
KC = dict(skin=(232, 186, 150), skin_hi=(248, 210, 180), skin_sh=(196, 146, 116), pimple=(226, 120, 110),
          hair=(84, 56, 40), hair_hi=(124, 88, 62), hair_sh=(58, 38, 28), fade=(120, 98, 84), brow=(70, 46, 32),
          hood=(176, 182, 192), hood_hi=(210, 214, 222), hood_sh=(132, 138, 152), string=(170, 255, 90),
          pant=(48, 50, 60), pant_hi=(72, 74, 86), pant_sh=(32, 34, 42), shoe=(240, 240, 244), shoe_b=(170, 255, 90), sole=(60, 60, 70),
          phone=(30, 30, 40), screen=(120, 250, 210))
KPOSE = dict(
    stand=dict(n=(3.0, 12.0), f=(-2.4, 12.4), bn=1, bf=-1, nleg=(0.06, 0.0), fleg=(-0.08, 0.0)),
    phone=dict(n=(6.4, 21.0), f=(-2.4, 12.4), bn=1, bf=-1, nleg=(0.08, 0.0), fleg=(-0.1, 0.0)),            # phone held out at the dad
    look=dict(n=(3.6, 19.4), f=(2.6, 19.0), bn=1, bf=1, nleg=(0.06, 0.0), fleg=(-0.08, 0.0)),              # reading his phone
    shock=dict(n=(5.8, 22.4), f=(-4.6, 22.0), bn=1, bf=-1, nleg=(0.14, 0.0), fleg=(-0.14, 0.0)),
)


def kayden(CH, cam, pose=None, t=0.0, mouth_=0.0, expr='bored', look=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
           blink=True, outline_=True, screen=None, pal=None):
    """pal: palette overrides (his friends). expr: bored (half-lidded, lips pressed: always mewing) | flat | shock | smirk.  screen: colour of the phone screen glow"""
    pose = pose or KPOSE['stand']
    P = dict(KC, **pal) if pal else KC
    br = 0.12 * math.sin(t * 1.9)
    sh_n, sh_f = H(1.5, 21.8 + br), H(-1.3, 22.0 + br)
    hp_n, hp_f = H(0.8, 12.6), H(-0.6, 12.6)
    hood = (P['hood'], P['hood_hi'], P['hood_sh'])
    pant = (P['pant'], P['pant_hi'], P['pant_sh'])
    L = Layer(cam)
    for hp, lg in ((hp_f, pose['fleg']), (hp_n, pose['nleg'])):
        A = Layer(cam)
        k, e = _limb(A, hp, *lg, 6.4, 6.0, 1.15, 1.1, *pant)                                                 # baggy pants
        ell(A, (e[0], e[1] - 0.9), 1.35, 0.7, P['pant'])
        ellt(A, (e[0] + 1.0, e[1] + 0.2), 2.15, 1.05, (P['shoe'], (255, 255, 255), (200, 204, 214)))       # chunky sneakers
        cap(A, (e[0] - 0.4, e[1] + 0.1), (e[0] + 1.8, e[1] - 0.4), 0.28, 0.2, P['shoe_b'])
        cap(A, (e[0] - 1.1, e[1] + 1.05), (e[0] + 3.0, e[1] + 1.05), 0.3, 0.3, P['sole'])
        _merge(L, A, OL)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(*pose['f'])
    ka, ea = _limb(A, sh_f, 0, 0, 4.9, 4.5, 1.1, 0.95, *hood, target=tf, bend=pose.get('bf', -1))
    ell(A, ea, 0.75, 0.72, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_f: prop_f(A, ea)
    _merge(L, A, OL)
    T = Layer(cam)                                                                                            # oversized hoodie
    poly(T, [H(-2.8, 22.4 + br), H(3.0, 22.4 + br), H(3.6, 12.0), H(-3.2, 12.0)], P['hood'])
    ellt(T, H(0.2, 18.0 + br * 0.5), 3.2, 4.6, hood)
    cap(T, H(-3.0, 12.4), H(3.5, 12.4), 0.7, 0.7, P['hood_sh'])                                              # ribbed hem
    poly(T, [H(-0.6, 16.4), H(2.9, 16.4), H(3.2, 13.6), H(-0.9, 13.6)], P['hood_sh'])                        # kangaroo pocket
    ellt(T, H(-0.9, 22.0 + br), 2.4, 1.2, hood)                                                              # hood bunched at the neck
    cap(T, H(1.3, 21.4 + br), H(1.5, 18.2 + br), 0.13, 0.13, P['string']); dot(T, H(1.5, 18.0 + br), P['string'], 0.24)
    cap(T, H(2.1, 21.4 + br), H(2.4, 18.6 + br), 0.13, 0.13, P['string']); dot(T, H(2.4, 18.4 + br), P['string'], 0.24)
    _merge(L, T, OL)
    Hd = Layer(cam)
    def Fh(x, h): return H(x, h + br)
    cap(Hd, Fh(0.2, 21.8), Fh(0.5, 23.6), 0.85, 0.85, P['skin'], P['skin_hi'], P['skin_sh'])
    ell(Hd, Fh(0.7, 25.6), 2.35, 2.6, P['skin'], 0, P['skin_hi'], P['skin_sh'], th_sh=-0.7)                  # long teen face
    ell(Hd, Fh(1.5, 23.6), 1.6, 1.0, P['skin'], 0.15)                                                        # jaw pushed forward (mewing)
    ell(Hd, Fh(-1.35, 25.6), 0.6, 0.85, P['skin'], 0, P['skin_hi'], P['skin_sh'])                           # ear
    ell(Hd, Fh(-1.3, 25.6), 0.3, 0.5, P['pimple'])
    ell(Hd, Fh(-0.9, 27.0), 1.15, 0.9, _mix(P['fade'], P['skin'], 0.35))                                     # faded side
    for i, (x, h, r) in enumerate([(-0.6, 28.4, 1.15), (0.6, 28.9, 1.2), (1.8, 28.5, 1.1), (2.6, 27.8, 0.9), (-1.4, 27.6, 0.9),
                                   (0.0, 29.6, 1.0), (1.3, 29.7, 0.95), (2.4, 29.1, 0.8)]):           # broccoli curls
        ell(Hd, Fh(x, h), r, r * 0.9, P['hair'], 0, P['hair_hi'], P['hair_sh'])
        dot(Hd, Fh(x - 0.2, h + 0.2), P['hair_sh'], r * 0.3)
    for x in (2.2, 3.0):
        ell(Hd, Fh(x, 27.1), 0.55, 0.5, P['hair'], 0, P['hair_hi'], None)                                      # curls over the forehead
    ex = {'bored': 'squint', 'flat': 'squint', 'shock': 'shock', 'smirk': 'smug'}.get(expr, 'normal')
    eyes = [(Fh(1.45, 25.75), 0.48), (Fh(2.6, 25.7), 0.55)]
    bl = blink and (t % 2.9) < 0.1 and expr != 'shock'
    for c, r in eyes:
        eye(Hd, c, r, ex, (look, 0.0), iris=(84, 56, 34), lid=P['skin_sh'], blink=bl)
        if expr in ('bored', 'flat'):
            cap(Hd, (c[0] - r * 1.1, c[1] - r * 0.5), (c[0] + r * 1.1, c[1] - r * 0.5), r * 0.45, r * 0.45, P['skin'])  # heavy lids
            cap(Hd, (c[0] - r * 1.1, c[1] - r * 0.05), (c[0] + r * 1.1, c[1] - r * 0.05), 0.1, 0.1, P['skin_sh'])
    for k, (c, r) in enumerate(eyes):
        s_ = 1 if k == 0 else -1
        bt = {'shock': -0.5, 'smirk': 0.3}.get(expr, 0.0)
        b = c[1] - r - 0.5 - (0.4 if expr == 'shock' else 0)
        cap(Hd, (c[0] - 0.5, b - s_ * bt * 0.3), (c[0] + 0.5, b + s_ * bt * 0.3), 0.16, 0.14, P['brow'])
    for (x, h) in ((1.0, 24.4), (3.0, 26.6), (2.9, 24.2)):
        dot(Hd, Fh(x, h), P['pimple'], 0.16)                                                                  # teen skin
    ell(Hd, Fh(3.25, 24.95), 0.45, 0.65, P['skin'], 0, P['skin_hi'], P['skin_sh'])                           # nose
    mm = max(mouth_, {'shock': 0.6}.get(expr, 0.0))
    mc = Fh(2.55, 23.45 - 0.2 * mm)
    mouth(Hd, mc, 0.55, mm, {'smirk': 'smug'}.get(expr, 'normal'), lip=(176, 106, 96))
    _merge(L, Hd, OL)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(*pose['n'])
    kna, ena = _limb(A, sh_n, 0, 0, 4.9, 4.5, 1.15, 0.98, *hood, target=tn, bend=pose.get('bn', 1))
    ell(A, ena, 0.78, 0.74, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_n: prop_n(A, ena)
    _merge(L, A, OL)
    if outline_: outline(L, OL)
    CH.add(L)
    return dict(hand_n=ena, hand_f=ea, mouth=mc, head=Fh(1.0, 25.8), top=Fh(0.6, 30.4))


# ======================================================================================= TAMMY
TC = dict(skin=(240, 190, 156), skin_hi=(252, 214, 184), skin_sh=(204, 150, 120), cheek=(236, 136, 140), lip=(196, 70, 96),
          hair=(196, 132, 70), hair_hi=(232, 172, 104), hair_sh=(150, 96, 48), brow=(130, 84, 46),
          card=(186, 156, 226), card_hi=(214, 192, 244), card_sh=(146, 116, 188), tee=(250, 248, 244), tee_sh=(214, 210, 214),
          legg=(60, 56, 76), legg_hi=(84, 80, 100), slip=(255, 214, 230), slip_hi=(255, 240, 246), mug=(250, 250, 248), mug_sh=(206, 206, 214))
TPOSE = dict(
    stand=dict(n=(3.0, 10.4), f=(-2.6, 10.6), bn=1, bf=-1, nleg=(0.04, 0.0), fleg=(-0.04, 0.0)),
    mug=dict(n=(3.4, 18.6), f=(1.8, 14.0), bn=1, bf=1, nleg=(0.04, 0.0), fleg=(-0.04, 0.0)),              # mug at the chin
    hug=dict(n=(3.0, 16.6), f=(2.4, 16.8), bn=1, bf=1, nleg=(0.04, 0.0), fleg=(-0.04, 0.0)),              # mug in both hands, blissful
)


def tammy(CH, cam, pose=None, t=0.0, mouth_=0.0, expr='tired', look=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
          blink=True, outline_=True, mask=False, patches=False, band=False):
    """mask: white sheet face mask; patches: gold under-eye patches; band: bunny-ear spa headband.
    expr: tired (half-lidded, unimpressed) | bliss (eyes closed, serene smile) | roll (eyes rolled up) | smirk | shock"""
    pose = pose or TPOSE['stand']
    P = TC
    br = 0.12 * math.sin(t * 1.7)
    sh_n, sh_f = H(1.4, 19.4 + br), H(-1.2, 19.6 + br)
    hp_n, hp_f = H(0.7, 10.6), H(-0.5, 10.6)
    card = (P['card'], P['card_hi'], P['card_sh'])
    L = Layer(cam)
    for hp, lg in ((hp_f, pose['fleg']), (hp_n, pose['nleg'])):
        A = Layer(cam)
        k, e = _limb(A, hp, *lg, 5.4, 5.0, 0.95, 0.7, P['legg'], P['legg_hi'], None)
        ellt(A, (e[0] + 0.9, e[1] + 0.35), 1.8, 0.95, (P['slip'], P['slip_hi'], P['slip']))                # fuzzy slippers
        for j in range(4): dot(A, (e[0] + 0.1 + j * 0.5, e[1] - 0.25), P['slip_hi'], 0.2)
        _merge(L, A, OL)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(*pose['f'])
    ka, ea = _limb(A, sh_f, 0, 0, 4.0, 3.7, 1.15, 0.95, *card, target=tf, bend=pose.get('bf', -1))
    ell(A, ea, 0.72, 0.7, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_f: prop_f(A, ea)
    _merge(L, A, OL)
    T = Layer(cam)
    ellt(T, H(0.5, 15.6 + br * 0.5), 2.9, 4.6, (P['tee'], (255, 255, 255), P['tee_sh']))
    poly(T, [H(-3.2, 20.0 + br), H(-0.4, 20.0 + br), H(0.4, 6.6), H(-3.8, 6.4)], P['card'])                 # long open cardigan
    poly(T, [H(1.8, 20.0 + br), H(3.6, 19.6 + br), H(4.8, 6.8), H(2.6, 6.6)], P['card'])
    cap(T, H(-0.4, 20.0 + br), H(0.4, 6.8), 0.3, 0.3, P['card_sh']); cap(T, H(1.8, 20.0 + br), H(2.6, 6.8), 0.3, 0.3, P['card_sh'])
    for j in range(5): cap(T, H(-3.4 + j * 0.1, 18 - j * 2.6), H(-0.5, 18 - j * 2.6), 0.08, 0.08, P['card_sh'])   # knit ribs
    _merge(L, T, OL)
    Hd = Layer(cam)
    def Fh(x, h): return H(x, h + br)
    cap(Hd, Fh(0.3, 19.6), Fh(0.5, 21.2), 0.8, 0.8, P['skin'], P['skin_hi'], P['skin_sh'])
    ell(Hd, Fh(-0.3, 23.2), 2.2, 2.4, P['hair'], 0, P['hair_hi'], P['hair_sh'])                              # hair behind
    ell(Hd, Fh(0.7, 23.1), 2.3, 2.45, P['skin'], 0, P['skin_hi'], P['skin_sh'], th_sh=-0.7)
    ell(Hd, Fh(0.1, 26.0), 2.4, 1.0, P['hair'], 0.05, P['hair_hi'], P['hair_sh'])
    ell(Hd, Fh(0.1, 27.6), 1.5, 1.35, P['hair'], 0, P['hair_hi'], P['hair_sh'])                              # pineapple bun
    for (x, h, a) in ((-0.8, 28.7, -0.6), (0.3, 29.1, 0.0), (1.2, 28.6, 0.6)):
        cap(Hd, Fh(x * 0.6, 28.2), Fh(x, h), 0.28, 0.12, P['hair'])                                          # loose strands up
    cap(Hd, Fh(-0.9, 26.6), Fh(1.0, 26.8), 0.25, 0.25, (240, 120, 170))                                     # scrunchie
    cap(Hd, Fh(2.4, 25.8), Fh(3.0, 22.6), 0.22, 0.12, P['hair'])                                             # loose strand at the face
    if mask: ell(Hd, Fh(1.4, 22.7), 2.0, 2.1, (248, 248, 244), 0, (255, 255, 255), (214, 216, 222))
    ex = {'tired': 'squint', 'bliss': 'closed', 'roll': 'normal', 'smirk': 'smug', 'shock': 'shock'}.get(expr, 'normal')
    eyes = [(Fh(1.35, 23.5), 0.46), (Fh(2.45, 23.45), 0.52)]
    bl = blink and (t % 4.3) < 0.1 and expr not in ('bliss',)
    lk = (look, -1.0) if expr == 'roll' else (look, 0.0)
    for c, r in eyes:
        if ex == 'closed':
            cap(Hd, (c[0] - r, c[1] - 0.05), (c[0], c[1] + 0.12), 0.12, 0.12, (60, 40, 40))
            cap(Hd, (c[0], c[1] + 0.12), (c[0] + r, c[1] - 0.05), 0.12, 0.12, (60, 40, 40))
        else:
            eye(Hd, c, r, ex, lk, iris=(60, 120, 90), lid=(200, 150, 190), lash=(40, 26, 30), blink=bl)
    for k, (c, r) in enumerate(eyes):
        s_ = 1 if k == 0 else -1
        bt = {'tired': 0.15, 'roll': -0.3, 'bliss': -0.4, 'smirk': 0.35, 'shock': -0.5}.get(expr, 0.0)
        b = c[1] - r - 0.45
        cap(Hd, (c[0] - 0.5, b - s_ * bt * 0.3), (c[0] + 0.5, b + s_ * bt * 0.3), 0.14, 0.12, P['brow'])
    if patches:
        for (c, r) in eyes: ell(Hd, (c[0] + 0.05, c[1] + r * 1.25), r * 1.15, r * 0.45, (250, 200, 70), 0.15, (255, 236, 150), (210, 150, 40))
    elif not mask:
        ell(Hd, Fh(1.2, 22.5), 0.6, 0.38, P['cheek']); ell(Hd, Fh(2.8, 22.5), 0.38, 0.34, P['cheek'])
    ell(Hd, Fh(3.0, 23.0), 0.42, 0.55, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    mm = max(mouth_, {'shock': 0.5}.get(expr, 0.0))
    mc = Fh(2.3, 21.7 - 0.2 * mm)
    mouth(Hd, mc, 0.6, mm, {'bliss': 'happy', 'smirk': 'smug'}.get(expr, 'normal'), lip=P['lip'])
    for (x, h) in ((-1.2, 22.6),):
        ell(Hd, Fh(x, h), 0.35, 0.5, (250, 200, 80))                                                           # earring
    if band: spa_band(Hd, Fh(0.4, 25.4), 2.6, 0.85)
    _merge(L, Hd, OL)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(*pose['n'])
    kna, ena = _limb(A, sh_n, 0, 0, 4.0, 3.7, 1.2, 0.98, *card, target=tn, bend=pose.get('bn', 1))
    ell(A, ena, 0.75, 0.72, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_n: prop_n(A, ena)
    _merge(L, A, OL)
    if outline_: outline(L, OL)
    CH.add(L)
    return dict(hand_n=ena, hand_f=ea, mouth=mc, head=Fh(1.0, 23.2), top=Fh(0.2, 28.8))


# ======================================================================================= props (unit coords at a hand)
def phone(L, h, ang=0.0, glow=(120, 250, 210), w=0.95, hh=1.8):
    """smartphone held at hand h, screen facing the viewer side"""
    c = (h[0] + 0.3, h[1] - 0.9)
    ca, sa = math.cos(ang), math.sin(ang)
    def R(x, y): return (c[0] + x * ca - y * sa, c[1] + x * sa + y * ca)
    poly(L, [R(-w, -hh), R(w, -hh), R(w, hh), R(-w, hh)], (28, 26, 36))
    poly(L, [R(-w + 0.18, -hh + 0.25), R(w - 0.18, -hh + 0.25), R(w - 0.18, hh - 0.3), R(-w + 0.18, hh - 0.3)], glow)
    cap(L, R(-w + 0.4, -hh + 0.7), R(w - 0.4, -hh + 0.7), 0.12, 0.12, (255, 255, 255))
    cap(L, R(-w + 0.4, -0.2), R(w - 0.5, -0.2), 0.2, 0.2, (40, 30, 60))
    ell(L, (h[0], h[1]), 0.62, 0.58, (240, 196, 160))                                                       # thumb over the edge


def mug(L, h, col=(250, 250, 248), band=(186, 156, 226), steam=None):
    """coffee mug held at hand h (unit coords)"""
    c = (h[0] + 0.5, h[1] - 0.6)
    ell(L, (c[0] + 1.1, c[1]), 0.55, 0.6, col)
    ell(L, (c[0] + 1.1, c[1]), 0.25, 0.3, (0, 0, 0)); L.m[(L.col == 0).all(-1)] = False
    poly(L, [(c[0] - 0.9, c[1] - 1.1), (c[0] + 0.9, c[1] - 1.1), (c[0] + 0.85, c[1] + 0.95), (c[0] - 0.85, c[1] + 0.95)], col)
    cap(L, (c[0] - 0.85, c[1] - 0.1), (c[0] + 0.85, c[1] - 0.1), 0.28, 0.28, band)
    ell(L, (c[0], c[1] - 1.1), 0.9, 0.22, (110, 66, 40))


# ======================================================================================= MIRRA (face on glass, world px)
def mirra(L, cx, cy, s, t, talk=0.0, expr='calm', glow=(90, 240, 230)):
    """MIRRA's face drawn in world px (L = Layer(v.wcam())): two rounded glowing eyes with highlights, a mouth bar that opens with
    talk (0..1), little lash ticks; expr: calm | smug (half-lid) | happy (arcs) | sad.  s = world px per face unit (face ~ 10 units)."""
    def W(x, y): return (cx + x * s, cy + y * s)
    dark = _mix(glow, (10, 30, 40), 0.55)
    bl = (t % 3.9) < 0.12
    for sx in (-1, 1):
        ec = W(sx * 2.6, -1.0)
        if bl or expr == 'happy':
            cap(L, W(sx * 2.6 - 1.3, -0.8), W(sx * 2.6, -1.8), 0.35 * s, 0.35 * s, glow)
            cap(L, W(sx * 2.6, -1.8), W(sx * 2.6 + 1.3, -0.8), 0.35 * s, 0.35 * s, glow)
            continue
        ell(L, ec, 1.35 * s, 1.75 * s, glow)
        ell(L, (ec[0] + 0.15 * s, ec[1] + 0.25 * s), 0.75 * s, 1.0 * s, dark)
        dot(L, (ec[0] + 0.45 * s, ec[1] - 0.5 * s), (255, 255, 255), 0.42 * s)
        dot(L, (ec[0] - 0.3 * s, ec[1] + 0.55 * s), (230, 255, 255), 0.2 * s)
        if expr in ('smug', 'calm'):
            cut = -0.55 if expr == 'calm' else -0.05
            poly(L, [W(sx * 2.6 - 1.6, -3.0), W(sx * 2.6 + 1.6, -3.0), W(sx * 2.6 + 1.6, -1.0 + cut - (0.3 if sx > 0 else 0)),
                     W(sx * 2.6 - 1.6, -1.0 + cut + (0.0 if sx > 0 else -0.3))], (1, 2, 3))
            L.m[(L.col == (1, 2, 3)).all(-1)] = False
            cap(L, W(sx * 2.6 - 1.4, -1.0 + cut - 0.1), W(sx * 2.6 + 1.4, -1.0 + cut - 0.2), 0.2 * s, 0.2 * s, glow)
    o = max(0.0, min(1.0, talk))
    if o > 0.08:
        ell(L, W(0, 2.4), 1.7 * s, (0.35 + 0.95 * o) * s, glow)
        ell(L, W(0, 2.4 + 0.1 * o), 1.25 * s, (0.15 + 0.7 * o) * s, dark)
    elif expr == 'sad':
        cap(L, W(-1.6, 2.8), W(0, 2.1), 0.3 * s, 0.3 * s, glow); cap(L, W(0, 2.1), W(1.6, 2.8), 0.3 * s, 0.3 * s, glow)
    else:
        cap(L, W(-1.7, 2.1), W(0, 2.8), 0.3 * s, 0.3 * s, glow); cap(L, W(0, 2.8), W(1.7, 2.1), 0.3 * s, 0.3 * s, glow)


def spa_band(Hd, c, w, s=1.0, col=(255, 182, 214), hi=(255, 220, 236)):
    """fluffy bunny-ear spa headband across the head at c (unit coords), half-width w"""
    cap(Hd, (c[0] - w, c[1] + 0.2 * s), (c[0] + w, c[1] - 0.1 * s), 0.55 * s, 0.55 * s, col, hi, None)
    for dx in (-0.55, 0.7):
        ell(Hd, (c[0] + dx * w * 0.6, c[1] - 1.5 * s), 0.55 * s, 1.35 * s, col, 0.15 * (1 if dx > 0 else -1), hi, None)
        ell(Hd, (c[0] + dx * w * 0.6, c[1] - 1.4 * s), 0.25 * s, 0.85 * s, (255, 140, 180), 0.15 * (1 if dx > 0 else -1))


# ======================================================================================= LILY (11, the «Sephora kid»)
LC = dict(skin=(246, 204, 176), skin_hi=(255, 226, 202), skin_sh=(214, 160, 132), cheek=(250, 150, 160), hair=(232, 186, 100),
          hair_hi=(250, 216, 140), hair_sh=(190, 140, 64), tee=(255, 240, 248), tee_sh=(226, 200, 216), skirt=(186, 156, 226),
          skirt_hi=(214, 192, 244), skirt_sh=(146, 116, 188), sock=(255, 255, 255), shoe=(255, 150, 200), cup=(150, 230, 210),
          cup_sh=(100, 180, 170))
LPOSE = dict(
    stand=dict(n=(2.2, 7.2), f=(-1.9, 7.4), bn=1, bf=-1, nleg=(0.04, 0.0), fleg=(-0.04, 0.0)),
    show=dict(n=(4.4, 12.4), f=(-1.9, 7.4), bn=1, bf=-1, nleg=(0.06, 0.0), fleg=(-0.06, 0.0)),        # shows a jar / the receipt
    cup=dict(n=(2.8, 10.4), f=(2.0, 10.2), bn=1, bf=1, nleg=(0.04, 0.0), fleg=(-0.04, 0.0)),         # hugs the tumbler
)


def lily(CH, cam, pose=None, t=0.0, mouth_=0.0, expr='happy', look=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
         blink=True, outline_=True, mask=False, patches=True, band=True, pal=None):
    """11-year-old beauty vlogger: ~19 units tall, big head, high side ponytail with a scrunchie, gold under-eye patches,
    bunny spa headband.  expr: happy | proud | shock | smug.  pal: palette overrides (the store's crowd of Sephora kids)"""
    pose = pose or LPOSE['stand']
    P = dict(LC, **pal) if pal else LC
    br = 0.1 * math.sin(t * 2.6)
    sh_n, sh_f = H(1.0, 12.6 + br), H(-0.9, 12.7 + br)
    hp_n, hp_f = H(0.5, 6.6), H(-0.4, 6.6)
    sk = (P['skin'], P['skin_hi'], P['skin_sh'])
    L = Layer(cam)
    for hp, lg in ((hp_f, pose['fleg']), (hp_n, pose['nleg'])):
        A = Layer(cam)
        k, e = _limb(A, hp, *lg, 3.4, 3.1, 0.62, 0.5, *sk)
        cap(A, (e[0], e[1] - 1.6), (e[0], e[1] - 0.3), 0.55, 0.55, P['sock'])
        ellt(A, (e[0] + 0.6, e[1] + 0.2), 1.25, 0.6, (P['shoe'], (255, 200, 228), (210, 100, 150)))
        _merge(L, A, OL)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(*pose['f'])
    ka, ea = _limb(A, sh_f, 0, 0, 2.7, 2.5, 0.55, 0.45, *sk, target=tf, bend=pose.get('bf', -1))
    ell(A, ea, 0.55, 0.52, *sk[:1], 0, sk[1], sk[2])
    if prop_f: prop_f(A, ea)
    _merge(L, A, OL)
    T = Layer(cam)
    poly(T, [H(-2.6, 7.6), H(3.0, 7.6), H(2.0, 4.4), H(-1.8, 4.4)], P['skirt'])                              # pleated skirt
    for j in range(4): cap(T, H(-1.6 + j * 1.1, 7.4), H(-1.4 + j * 1.1, 4.6), 0.08, 0.08, P['skirt_sh'])
    ellt(T, H(0.2, 10.2 + br * 0.5), 2.1, 2.8, (P['tee'], (255, 255, 255), P['tee_sh']))                    # oversized tee
    ell(T, H(0.6, 10.4), 0.9, 0.7, (255, 150, 200))                                                         # heart print
    _merge(L, T, OL)
    Hd = Layer(cam)
    def Fh(x, h): return H(x, h + br)
    cap(Hd, Fh(0.2, 12.6), Fh(0.3, 13.8), 0.6, 0.6, *sk)
    cap(Hd, Fh(-1.6, 18.4), Fh(-3.0, 14.6), 0.95, 0.6, P['hair'], P['hair_hi'], P['hair_sh'])               # side ponytail
    ell(Hd, Fh(-1.4, 18.0), 0.5, 0.4, (170, 140, 255))                                                       # scrunchie
    ell(Hd, Fh(0.6, 16.4), 2.75, 2.85, P['skin'], 0, P['skin_hi'], P['skin_sh'], th_sh=-0.7)                # big round kid head
    ell(Hd, Fh(0.2, 18.4), 2.8, 1.5, P['hair'], 0.1, P['hair_hi'], P['hair_sh'])
    cap(Hd, Fh(1.5, 18.6), Fh(3.0, 17.5), 0.5, 0.35, P['hair'])                                              # side-swept bangs
    ell(Hd, Fh(-1.6, 16.3), 0.5, 0.7, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if mask: ell(Hd, Fh(1.3, 15.9), 2.2, 2.2, (248, 248, 244), 0, (255, 255, 255), (214, 216, 222))
    ex = {'happy': 'normal', 'proud': 'squint', 'shock': 'shock', 'smug': 'smug'}.get(expr, 'normal')
    eyes = [(Fh(1.2, 16.5), 0.55), (Fh(2.45, 16.45), 0.62)]
    bl = blink and (t % 3.1) < 0.1 and expr != 'shock'
    for c, r in eyes:
        eye(Hd, c, r, ex, (look, 0.0), iris=(90, 140, 210), lid=(220, 170, 200), lash=(50, 30, 40), blink=bl, bulge=1.15)
    for k, (c, r) in enumerate(eyes):
        s_ = 1 if k == 0 else -1
        b = c[1] - r - 0.5 - (0.3 if expr == 'shock' else 0)
        cap(Hd, (c[0] - 0.45, b + s_ * 0.05), (c[0] + 0.45, b - s_ * 0.05), 0.13, 0.11, P['hair_sh'])
    if patches:
        for (c, r) in eyes: ell(Hd, (c[0] + 0.05, c[1] + r * 1.3), r * 1.1, r * 0.45, (250, 200, 70), 0.15, (255, 236, 150), (210, 150, 40))
    elif not mask:
        ell(Hd, Fh(1.0, 15.3), 0.55, 0.35, P['cheek'])
    ell(Hd, Fh(3.05, 15.75), 0.35, 0.4, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    mm = max(mouth_, {'shock': 0.55}.get(expr, 0.0))
    mc = Fh(2.2, 14.6 - 0.2 * mm)
    mouth(Hd, mc, 0.55, mm, {'happy': 'grin', 'proud': 'smug', 'smug': 'smug'}.get(expr, 'normal'), lip=(230, 100, 130))
    if band: spa_band(Hd, Fh(0.4, 18.3), 2.7, 0.8)
    _merge(L, Hd, OL)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(*pose['n'])
    kna, ena = _limb(A, sh_n, 0, 0, 2.7, 2.5, 0.58, 0.46, *sk, target=tn, bend=pose.get('bn', 1))
    ell(A, ena, 0.56, 0.53, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_n: prop_n(A, ena)
    _merge(L, A, OL)
    if outline_: outline(L, OL)
    CH.add(L)
    return dict(hand_n=ena, hand_f=ea, mouth=mc, head=Fh(1.1, 16.3), top=Fh(0.3, 19.6))


KID_PALS = [dict(hair=(80, 50, 34), hair_hi=(120, 80, 52), hair_sh=(56, 34, 22), tee=(200, 240, 255), skirt=(120, 200, 180),
                 skirt_hi=(160, 230, 210), skirt_sh=(80, 150, 140), shoe=(120, 200, 255)),
            dict(hair=(40, 30, 30), hair_hi=(80, 60, 56), hair_sh=(24, 18, 18), skin=(186, 130, 96), skin_hi=(210, 156, 120),
                 skin_sh=(150, 98, 70), tee=(255, 250, 200), skirt=(255, 170, 120), skirt_hi=(255, 200, 160), skirt_sh=(220, 130, 90)),
            dict(hair=(200, 90, 50), hair_hi=(236, 130, 80), hair_sh=(150, 60, 30), tee=(230, 255, 220), skirt=(255, 150, 200),
                 skirt_hi=(255, 190, 220), skirt_sh=(210, 100, 150), shoe=(170, 255, 90))]


# ======================================================================================= SKYLAR (teen store clerk)
SC = dict(skin=(226, 172, 136), skin_hi=(244, 198, 164), skin_sh=(190, 134, 104), hair=(40, 28, 34), hair_hi=(90, 64, 80),
          hair_sh=(24, 16, 20), top=(34, 32, 40), top_hi=(64, 60, 74), top_sh=(20, 18, 24), lip=(200, 80, 110), tag=(250, 250, 250))
SPOSE = dict(
    stand=dict(n=(2.8, 12.4), f=(-2.4, 12.6), bn=1, bf=-1),
    lean=dict(n=(4.6, 13.8), f=(3.6, 13.6), bn=1, bf=1),                 # elbows on the counter
    spray=dict(n=(6.4, 18.0), f=(-2.4, 12.6), bn=1, bf=-1),              # tester bottle held out
)


def skylar(CH, cam, pose=None, t=0.0, mouth_=0.0, expr='bored', look=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
           blink=True, outline_=True, gum=0.0):
    """bored teen clerk, drawn waist-up behind a counter (legs are never seen): high ponytail, winged liner, black tee + name tag.
    expr: bored | flat | smirk.  Anchor = floor point under her (hidden by the counter)."""
    pose = pose or SPOSE['stand']
    P = SC
    br = 0.1 * math.sin(t * 1.6)
    sh_n, sh_f = H(1.4, 21.0 + br), H(-1.2, 21.2 + br)
    sk = (P['skin'], P['skin_hi'], P['skin_sh'])
    top = (P['top'], P['top_hi'], P['top_sh'])
    L = Layer(cam)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(*pose['f'])
    ka, ea = _limb(A, sh_f, 0, 0, 3.9, 3.6, 0.75, 0.6, *sk, target=tf, bend=pose.get('bf', -1))
    ell(A, sh_f, 1.0, 0.9, *top[:1], 0, top[1], top[2])
    ell(A, ea, 0.66, 0.62, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_f: prop_f(A, ea)
    _merge(L, A, OL)
    T = Layer(cam)
    ellt(T, H(0.3, 16.6 + br * 0.5), 2.6, 5.0, top)
    poly(T, [H(-2.2, 13.0), H(2.8, 13.0), H(3.2, 6.0), H(-2.6, 6.0)], P['top'])
    poly(T, [H(1.4, 18.6), H(3.0, 18.6), H(3.0, 17.4), H(1.4, 17.4)], P['tag'])                                # name tag
    cap(T, H(1.6, 18.0), H(2.8, 18.0), 0.1, 0.1, (60, 60, 70))
    _merge(L, T, OL)
    Hd = Layer(cam)
    def Fh(x, h): return H(x, h + br)
    cap(Hd, Fh(0.2, 21.0), Fh(0.4, 22.6), 0.7, 0.7, *sk)
    cap(Hd, Fh(-0.6, 27.6), Fh(-2.6, 23.0), 0.9, 0.5, P['hair'], P['hair_hi'], P['hair_sh'])                 # high ponytail
    ell(Hd, Fh(0.7, 24.4), 2.1, 2.45, P['skin'], 0, P['skin_hi'], P['skin_sh'], th_sh=-0.7)
    ell(Hd, Fh(0.4, 26.3), 2.3, 1.0, P['hair'], 0.05, P['hair_hi'], P['hair_sh'])                             # slicked-back hair
    ell(Hd, Fh(-0.6, 27.2), 0.8, 0.6, P['hair'], 0, P['hair_hi'], P['hair_sh'])                               # bun knot
    ell(Hd, Fh(-1.2, 24.4), 0.45, 0.65, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    dot(Hd, Fh(-1.2, 23.7), (230, 230, 240), 0.22)                                                            # stud
    ex = {'bored': 'squint', 'flat': 'squint', 'smirk': 'smug'}.get(expr, 'normal')
    eyes = [(Fh(1.3, 24.7), 0.45), (Fh(2.35, 24.65), 0.5)]
    bl = blink and (t % 2.6) < 0.12
    for c, r in eyes:
        eye(Hd, c, r, ex, (look, 0.0), iris=(70, 50, 40), lid=(150, 110, 140), lash=(20, 14, 18), blink=bl)
        cap(Hd, (c[0] + r * 0.8, c[1] - r * 0.4), (c[0] + r * 1.6, c[1] - r * 0.9), 0.1, 0.06, (20, 14, 18))   # winged liner
    for k, (c, r) in enumerate(eyes):
        b = c[1] - r - 0.45
        cap(Hd, (c[0] - 0.45, b), (c[0] + 0.45, b - 0.1), 0.12, 0.1, P['hair'])
    ell(Hd, Fh(2.85, 24.1), 0.35, 0.48, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    mm = max(mouth_, 0.0)
    mc = Fh(2.2, 23.0 - 0.2 * mm)
    if gum > 0 and mm < 0.1:
        ell(Hd, (mc[0] + 0.5, mc[1]), 0.3 + 1.2 * gum, 0.3 + 1.2 * gum, (255, 150, 200), 0, (255, 200, 228), None)
    mouth(Hd, mc, 0.5, mm, {'smirk': 'smug'}.get(expr, 'normal'), lip=P['lip'])
    _merge(L, Hd, OL)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(*pose['n'])
    kna, ena = _limb(A, sh_n, 0, 0, 3.9, 3.6, 0.78, 0.62, *sk, target=tn, bend=pose.get('bn', 1))
    ell(A, sh_n, 1.05, 0.95, P['top'], 0, P['top_hi'], P['top_sh'])
    ell(A, ena, 0.68, 0.64, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_n: prop_n(A, ena)
    _merge(L, A, OL)
    if outline_: outline(L, OL)
    CH.add(L)
    return dict(hand_n=ena, hand_f=ea, mouth=mc, head=Fh(1.0, 24.4), top=Fh(0.3, 27.8), tag=H(2.2, 18.0))


# ======================================================================================= more props
def tumbler(L, h, col=(150, 230, 210), sh=(100, 180, 170)):
    """giant STANLEE tumbler with a straw, held at hand h"""
    c = (h[0] + 0.4, h[1] - 1.2)
    poly(L, [(c[0] - 0.9, c[1] - 2.0), (c[0] + 0.9, c[1] - 2.0), (c[0] + 0.7, c[1] + 2.0), (c[0] - 0.7, c[1] + 2.0)], col)
    cap(L, (c[0] + 0.5, c[1] - 1.6), (c[0] + 0.5, c[1] + 1.6), 0.18, 0.18, sh)
    cap(L, (c[0] - 1.0, c[1] - 2.1), (c[0] + 1.0, c[1] - 2.1), 0.3, 0.3, (240, 240, 244))
    cap(L, (c[0] + 0.2, c[1] - 2.2), (c[0] + 0.6, c[1] - 3.6), 0.12, 0.12, (255, 150, 200))
    ell(L, (c[0] + 1.1, c[1] - 0.6), 0.45, 0.9, col)


def jar(L, h, col=(255, 200, 220), lid=(230, 190, 90)):
    """skincare jar held at hand h"""
    c = (h[0] + 0.5, h[1] - 0.6)
    ell(L, c, 0.9, 0.7, col, 0, (255, 236, 244), None)
    cap(L, (c[0] - 0.9, c[1] - 0.6), (c[0] + 0.9, c[1] - 0.6), 0.28, 0.28, lid)


def bottle(L, h, col=(214, 186, 255)):
    """tester spray bottle held at hand h"""
    c = (h[0] + 0.3, h[1] - 1.0)
    poly(L, [(c[0] - 0.45, c[1] - 0.9), (c[0] + 0.45, c[1] - 0.9), (c[0] + 0.5, c[1] + 0.9), (c[0] - 0.5, c[1] + 0.9)], col)
    cap(L, (c[0], c[1] - 1.0), (c[0], c[1] - 1.5), 0.2, 0.2, (240, 240, 244))
    cap(L, (c[0], c[1] - 1.5), (c[0] + 0.5, c[1] - 1.5), 0.12, 0.12, (240, 240, 244))


def basket(L, h, items=((255, 200, 220), (150, 250, 190), (214, 186, 255), (255, 214, 120), (120, 230, 240))):
    """store basket hanging from hand h, overflowing with jars and bottles"""
    c = (h[0] + 0.2, h[1] + 2.4)
    cap(L, (c[0] - 1.6, c[1] - 1.2), (h[0], h[1]), 0.1, 0.1, (40, 30, 40))
    cap(L, (c[0] + 1.6, c[1] - 1.2), (h[0], h[1]), 0.1, 0.1, (40, 30, 40))
    for i, col in enumerate(items):
        x = c[0] - 1.4 + i * 0.7
        cap(L, (x, c[1] - 1.0), (x + 0.1 * (i % 2), c[1] - 2.0 - 0.4 * (i % 3)), 0.32, 0.3, col)
    poly(L, [(c[0] - 2.0, c[1] - 1.2), (c[0] + 2.0, c[1] - 1.2), (c[0] + 1.6, c[1] + 0.9), (c[0] - 1.6, c[1] + 0.9)], (30, 30, 36))
    for j in range(4): cap(L, (c[0] - 1.6 + j * 1.05, c[1] - 1.0), (c[0] - 1.4 + j * 0.95, c[1] + 0.7), 0.1, 0.1, (80, 80, 90))


def receipt(L, h, length=8.0, wob=0.0):
    """a long paper receipt hanging from hand h down towards the floor"""
    x0, y0 = h
    pts = [(x0 + 0.3 * math.sin(wob + i * 0.6) * (i / 10), y0 + length * i / 10) for i in range(11)]
    for a, b in zip(pts, pts[1:]):
        cap(L, a, b, 0.55, 0.55, (252, 250, 244))
    for i in range(1, 10):
        cap(L, (pts[i][0] - 0.35, pts[i][1]), (pts[i][0] + 0.25, pts[i][1]), 0.05, 0.05, (150, 150, 160))


FRIEND_PALS = [dict(hood=(70, 120, 220), hood_hi=(110, 160, 250), hood_sh=(44, 80, 170), string=(255, 255, 255),
                    hair=(30, 22, 20), hair_hi=(70, 52, 44), hair_sh=(16, 12, 10), skin=(170, 112, 80), skin_hi=(200, 140, 104),
                    skin_sh=(132, 84, 58), shoe_b=(255, 90, 90)),
               dict(hood=(240, 120, 60), hood_hi=(255, 160, 100), hood_sh=(190, 80, 36), string=(40, 40, 50),
                    hair=(230, 200, 120), hair_hi=(250, 230, 160), hair_sh=(190, 150, 80), shoe_b=(90, 200, 255))]


def burger(L, x, y, s=1.0, ang=0.0):
    """a flipped burger patty in world px"""
    from props.folk import ell as fell
    fell(L, (x, y), 14 * s, 5 * s, (110, 64, 40), ang, (150, 96, 60), (80, 44, 28))
    fell(L, (x - 3 * s, y - 2 * s), 6 * s, 1.5 * s, (160, 110, 70), ang)


def speaker(L, x, y, s=1.0):
    """MIRRA's patio smart speaker (world px): a lavender cylinder with a dark face screen on top of it"""
    from props.folk import ell as fell, poly as fpoly, cap as fcap
    fpoly(L, [(x - 16 * s, y - 44 * s), (x + 16 * s, y - 44 * s), (x + 16 * s, y), (x - 16 * s, y)], (186, 156, 226))
    fell(L, (x, y - 44 * s), 16 * s, 5 * s, (214, 192, 244))
    fpoly(L, [(x - 12 * s, y - 38 * s), (x + 12 * s, y - 38 * s), (x + 12 * s, y - 14 * s), (x - 12 * s, y - 14 * s)], (18, 24, 38))
    return (x - 12 * s, y - 38 * s, x + 12 * s, y - 14 * s)
