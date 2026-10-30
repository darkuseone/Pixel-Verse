"""S01E02 «$95 TO APPLY?!» (30.0 s, twist at 17.56 s / 59 %, type: the villain is family).
HOOK: Duke at the Liberty Lofts leasing desk screams at the application on a tablet — «NINETY-FIVE bucks?! Just to APPLY?!» Madison (leasing
agent, iced latte): «Plus the AMENITY fee!» — the amenities: a kiddie pool with one rubber duck, a dumbbell on a mat «FITNESS CENTER».
«I'm a BALD EAGLE. I'm on the DOLLAR!» — Sal on the cabana chair, keys in his beak: «Dollar's broke too.» The portal: «Sounds like you
said — PET fee!» — «I'm not a PET!» — «You have FEATHERS, sir.» — «Who's the LANDLORD?! I'll talk to HIM!» TWIST: the roof, Sal on the
vent with a tiny briefcase: «S.P. Holdings. Sal Pigeon.» — «You don't even PAY rent!» — «Pigeons don't pay rent. We COLLECT it.» —
the portal: «Sounds like you said — RENEW!» (ka-ching) — Sal to camera: «Welcome home.»
Clue in the first half: «MANAGED BY S.P. HOLDINGS LLC» on the office door, Sal's giant key ring jingling in the courtyard.
  python3 ep02.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import overlays as O
import stage as ST
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
from episode import Episode
from props import feecast as C
from props import feekit as K
from props.feekit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

EPI = Episode('ep02', VOICE, DUR, FPS, colors=dict(K.COL, madison=(255, 150, 200)), slug=SLUG,
              endcard=dict(style='fee', lang='us', promise='NEXT: $40 FOR A HUG?!', cy=1470))
OFF, YARD, ROOF = K.world('leasing'), K.world('courtyard'), K.world('roof')
VENT = (683.0, 314.0)            # Sal's perch: the round vent cap on top of the HVAC unit


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def V(world_, cx, cy, Z):
    return view_at(world_, cx, cy, Z, 180, 320)


def sal_keys(t):
    return lambda sp: C.keyring(sp, (sp.anchors['mouth'][0] + 1.0, sp.anchors['mouth'][1] - 0.4), t)


def insert(t, world_, brand, stamp=None, t_stamp=99.0, who='feebee'):
    big = K.dof(K.shot(world_, K.light_store, 500.0, 360.0, 1.3), 9)
    big[:] = (big * 0.62).astype(np.uint8)
    scr = K.screen_ui(t, mouth(who, t, 1.6), brand, stamp=stamp if t >= t_stamp else None, stamp_k=sm((t - t_stamp) / 0.12),
                      w=700, h=1060, sub='POWERED BY FEE-BEE AI')
    x0, y0 = (OUT_W - scr.shape[1]) // 2, 600
    O.overlay(big, scr, x0, y0, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(x0, y0, x0 + scr.shape[1], y0 + scr.shape[0]))
    if t >= t_stamp: K.dollars(big, t, t_stamp, OUT_W // 2, y0 + scr.shape[0] - 160, n=8, seed=3)
    return big


# ================================================================== 0: HOOK — CU at the leasing desk: «NINETY-FIVE bucks?! Just to APPLY?!»
def r_hook(t, u):
    dx, dy = K.shake(t, 0.05, 26, 0.9)
    def fx_(big, v, a):
        hx, hy = aout(a, v, 'head')
        K.feathers(big, t, 0.12, hx, hy - 60, n=16, seed=5)
    big, a = K.cu(C.duke, t, OFF, 300.0, 380.0, 1.3, 24.0, head=(440, 900), light=K.light_apt, blur=4, extra_fx=fx_,
                  expr='roar', mouth_=max(0.5, mouth('duke', t, 2.0)), flop=1.0, tremble=0.8, look=(0.9, -0.6), hand_n=(22.0, 44.0),
                  prop_n=lambda sp, h: C.tablet(sp, h, t, 0.0, screen='form'))
    return K.shift(big, dx, dy)


# ================================================================== 1: AMENITIES — pan across the courtyard «resort» (Madison VO)
def r_amen(t, u):
    k = sm(u / (CUTS[2] - CUTS[1]))
    Z = 1.0
    cx, cy = 300.0 + 560.0 * k, 400.0
    duck = A(C.rubber_duck, 520.0, 606.0, 10.0, t=t)
    db = A(C.dumbbell, 1000.0, 640.0, 11.0, t=t)
    return K.shot(YARD, K.light_mall, cx, cy, Z, acts=[duck, db])


# ================================================================== 2: DOLLAR — «I'm a BALD EAGLE. I'm on the DOLLAR!» — Sal: «Dollar's broke too.»
def r_dollar(t, u):
    k = sm(u / 4.6)
    Z = 1.0 + 0.06 * k
    cx, cy = 340.0 - 20 * k, 420.0
    puff = sm((t - 4.82) / 0.35)
    duke = A(C.duke, 446.0, 692.0, 11.4 * Z, t=t, expr='proud', mouth_=mouth('duke', t, 1.8), puff=puff, look=(-0.6, -0.2), flip=True,
             hand_n=(20.0, 30.0), hand_f=(-15.0, 30.0))
    sal = A(C.sal, 196.0, 498.0, 10.5 * Z, t=t, expr='dead', mouth_=mouth('sal', t, 2.2), look=(0.8, -0.3), prop=sal_keys(t))
    duck = A(C.rubber_duck, 520.0, 606.0, 10.0 * Z, t=t)
    return K.shot(YARD, K.light_mall, cx, cy, Z, acts=[duck, sal, duke])


# ================================================================== 3: TABLET — «Sounds like you said — PET fee!»
def r_tablet(t, u):
    return insert(t, OFF, 'LIBERTY LOFTS PORTAL', 'PET FEE +$50/MO', 11.05)


# ================================================================== 4: PET — «I'm not a PET!» — «You have FEATHERS, sir.»
def r_pet(t, u):
    k = sm(u / 3.5)
    Z = 1.04 + 0.06 * k
    cx, cy = 560.0, 420.0
    duke = A(C.duke, 470.0, 702.0, 16.6 * Z, t=t, expr='roar' if t < 12.7 else 'glare', mouth_=mouth('duke', t, 2.0), look=(0.9, 0.3),
             flop=0.8 if t < 12.7 else 0.0, hand_n=(24.0, 40.0) if t < 12.7 else (17.0, 26.0))
    mad = A(C.madison, 664.0, 690.0, 16.6 * Z, t=t, flip=True, expr='smug' if t >= 12.7 else 'hype', mouth_=mouth('madison', t, 1.6),
            look=(0.8, 0.2), sip=sm((t - 14.95) / 0.3))
    return K.shot(OFF, K.light_apt, cx, cy, Z, acts=[mad, duke])


# ================================================================== 5: LANDLORD — CU: «Who's the LANDLORD?! I'll talk to HIM!»
def r_lord(t, u):
    dx, dy = K.shake(t, 15.12, 18, 0.5)
    big, a = K.cu(C.duke, t, OFF, 560.0, 380.0, 1.35, 21.0 + 1.5 * sm(u / 2.4), head=(500, 900), light=K.light_apt, blur=4,
                  expr='roar', mouth_=mouth('duke', t, 2.0), flop=1.0, tremble=0.6, look=(0.6, 0.4), hand_n=(26.0, 54.0))
    return K.shift(big, dx, dy)


# ================================================================== 6: TWIST — the roof: Sal on the vent with a briefcase: «S.P. Holdings. Sal Pigeon.»
def r_twist(t, u):
    k = sm(u / 0.9)
    Z = 2.3 - 1.2 * k
    cx, cy = lerp(683.0, 640.0, k), lerp(300.0, 410.0, k)
    s_sal = 2.4 * 3 * Z
    sal = A(C.sal, VENT[0], VENT[1], s_sal, t=t, expr='sly' if t < 19.0 else 'dead', mouth_=mouth('sal', t, 2.2), look=(-0.2, -0.5),
            prop=sal_keys(t))
    case = A(C.briefcase, VENT[0] - 22.0, VENT[1], s_sal * 0.9, t=t)
    acts = [case, sal]
    if t >= 18.25:
        f = sm((t - 18.25) / 0.6)
        duke = A(C.duke, lerp(380.0, 556.0, f), lerp(560.0, 652.0, f), 3.8 * 3 * Z, t=t, expr='shock', mouth_=0.3,
                 fly=t * 2.6 if f < 0.95 else None, look=(0.9, -0.5))
        acts.append(duke)
    return K.shot(ROOF, K.light_mall, cx, cy, Z, acts=acts)


# ================================================================== 7: RENT — «You don't even PAY rent!» — «Pigeons don't pay rent. We COLLECT it.»
def r_rent(t, u):
    Z = 1.15
    cx, cy = 640.0, 420.0
    duke = A(C.duke, 556.0, 652.0, 3.8 * 3 * Z, t=t, expr='roar' if t < 22.3 else 'shock', mouth_=mouth('duke', t, 2.0),
             look=(0.9, -0.6), flop=0.8 if t < 22.3 else 0.0, hand_n=(26.0, 56.0) if t < 22.3 else (16.0, 28.0), tremble=0.5 if t < 22.3 else 0)
    s_sal = 2.4 * 3 * Z
    sal = A(C.sal, VENT[0], VENT[1], s_sal, t=t, expr='dead', mouth_=mouth('sal', t, 2.2), look=(-0.9, -0.3), prop=sal_keys(t))
    case = A(C.briefcase, VENT[0] - 22.0, VENT[1], s_sal * 0.9, t=t)
    big = K.shot(ROOF, K.light_mall, cx, cy, Z, acts=[case, sal, duke])
    dx, dy = K.shake(t, 20.66, 14, 0.35)
    return K.shift(big, dx, dy)


# ================================================================== 8: RENEW — the portal: «Sounds like you said — RENEW!» (ka-ching)
def r_renew(t, u):
    return insert(t, ROOF, 'LIBERTY LOFTS PORTAL', 'RENEWED! RENT +10%', 26.95)


# ================================================================== 9: BUTTON — Sal on the vent, to camera: «Welcome home.»
def r_button(t, u):
    def after(big, v, a):
        hx, hy = aout(a, v, 'head')
    big, a = K.cu(C.sal, t, ROOF, 683.0, 300.0, 1.35, 30.0, head=(560, 860), light=K.light_mall, blur=4,
                  expr='dead', mouth_=mouth('sal', t, 2.2), look=(-0.2, -0.6), prop=sal_keys(t), bob=t < 27.4)
    return big


R = [r_hook, r_amen, r_dollar, r_tablet, r_pet, r_lord, r_twist, r_rent, r_renew, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SEND = K.st_lines(['SEND THIS TO', 'YOUR LANDLORD'], size=44, colors=[(255, 255, 255), (130, 255, 200)])
CHOICE = K.st_lines(['RENT A NEST?', 'A) PAY  B) SQUAT'], size=42, colors=[(255, 214, 80), (130, 255, 200)])
SHOW = K.Show(EPI, 2, ['$95 TO APPLY?!'], hook_t=(0.08, 2.00), hook_y=330, hook_size=70,
              stickers=[(K.st('RESORT-STYLE!', fg=(130, 255, 200), size=56), 3.40, 4.70, 540, 330),
                        (K.st('LANDLORD?!', fg=(255, 214, 80), size=72), 17.58, 19.40, 540, 330),
                        (SEND, 22.60, 25.10, 540, 340),
                        (CHOICE, 28.00, 30.0, 540, 390)],
              flashes=[TWIST], mosaics=[CUTS[3], CUTS[8]],
              cap_y={0: 1420, 1: 1380, 2: 1400, 3: 470, 4: 1460, 5: 1420, 6: 1450, 7: 1420, 8: 470, 9: 1250})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
