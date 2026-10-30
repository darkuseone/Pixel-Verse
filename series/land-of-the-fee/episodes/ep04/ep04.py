"""S01E04 «$400 A MONTH?!» (33.0 s, twist at 17.55 s / 53 %, type: success is worse than failure).
HOOK: Duke crammed into a tiny dented 2009 hatchback (head through the roof, wings out of the windows) screams at the State Fee letter —
«FOUR HUNDRED a month?! It's a 2009 HATCHBACK!» The dashboard Fee-Bee: «Sounds like you said — ADD a DRIVER!» (Sal is on the hood).
«I'm a BALD EAGLE. I'm on the DOLLAR!» — «Dollar can't afford gas either.» Duke puts the car up for sale: «Eagles don't NEED cars! Sal, hit
the SCREAM!» — Sal's Bluetooth speaker plays the epic movie-eagle scream, Duke soars over the jammed interstate: «No insurance! No GAS!»
TWIST: a Sky Patrol police drone, sirens: «Unregistered DRONE! Land NOW!» — on the shoulder: «No flight plan. No license. No AIRCRAFT
insurance.» — «That's nine hundred a MONTH.» — «I'm a BIRD!» — «Birds got a PILOT'S license?» — his old hatchback crawls by, Sal at the
wheel: «Need a ride? Twenty BUCKS.» (honk)
Clue in the first half: a Sky Patrol drone passes behind the house while Sal talks.
  python3 ep04.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, SCREAM

EPI = Episode('ep04', VOICE, DUR, FPS, colors=K.COL, slug=SLUG,
              endcard=dict(style='fee', lang='us', promise='NEXT: $600 NOSEBLEEDS?!', cy=1470))
STREET, HWY, SHO = K.world('street'), K.world('highway'), K.world('shoulder')
IC = 0.50                         # cartoon: Duke is bigger than the car allows (C.DUKE_IN_CAR = true scale)


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def V(world_, cx, cy, Z):
    return view_at(world_, cx, cy, Z, 180, 320)


def car_acts(v, ox, oy, cs, t, duke=None, sal=None, sale=False, drive=0.0, honk=0.0, sal_driver=None):
    """the hatchback with its feet at output (ox, oy), cs output px per car sprite px; Duke sits inside (head through the roof), Sal on
    the hood (sal=dict) or at the wheel (sal_driver=dict). Returns actors in depth order (who is inside is drawn before the body)"""
    acts = []
    if duke is not None:
        acts.append(A(C.duke, *wpt(v, ox - 2.0 * cs, oy - 5.0 * cs), cs * IC, t=t, legs=False, **duke))
    if sal_driver is not None:
        acts.append(A(C.sal, *wpt(v, ox + 5.0 * cs, oy - 6.0 * cs), cs * 0.55, t=t, **sal_driver))
    acts.append(A(C.hatchback, *wpt(v, ox, oy), cs, t=t, sale=sale, drive=drive, honk=honk))
    if sal is not None:
        acts.append(A(C.sal, *wpt(v, ox + 17.0 * cs, oy - 14.0 * cs), cs * 0.42, t=t, **sal))
    return acts


def insert(t, world_, brand, stamp, t_stamp, cx=600.0, cy=520.0):
    big = K.dof(K.shot(world_, K.light_mall, cx, cy, 1.3), 9)
    big[:] = (big * 0.62).astype(np.uint8)
    scr = K.screen_ui(t, mouth('feebee', t, 1.6), brand, stamp=stamp if t >= t_stamp else None, stamp_k=sm((t - t_stamp) / 0.12),
                      w=700, h=1060, sub='POWERED BY FEE-BEE AI')
    x0, y0 = (OUT_W - scr.shape[1]) // 2, 600
    O.overlay(big, scr, x0, y0, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(x0, y0, x0 + scr.shape[1], y0 + scr.shape[0]))
    if t >= t_stamp: K.dollars(big, t, t_stamp, OUT_W // 2, y0 + scr.shape[0] - 160, n=8, seed=4)
    return big


# ================================================================== 0: HOOK — head through the roof of the tiny hatchback + the letter
def r_hook(t, u):
    Z = 1.4
    cx, cy = 600.0, 560.0
    v = V(STREET, cx, cy, Z)
    cs = 40.0
    duke = dict(expr='roar', mouth_=max(0.5, mouth('duke', t, 2.0)), flop=1.0, tremble=0.8, look=(-0.6, 0.6),
                hand_n=(34.0, 40.0), hand_f=(-30.0, 40.0))
    def pre(big, v_): big[:] = K.dof(big, 5)
    def fx_(big, v_):
        K.feathers(big, t, 0.12, 740, 1000, n=12, seed=11)
    big = K.shot(STREET, K.light_mall, cx, cy, Z, acts=car_acts(v, 720, 2280, cs, t, duke=duke), pre=pre, fx_=fx_)
    b = K.bill_ui(['2009 HATCHBACK', 'DENTS: 14', 'NEW PREMIUM'], total='$400 / MONTH', title='STATE FEE INSURANCE', hi=2, w=470)
    k = sm(u / 0.25)
    x0 = int(lerp(-b.shape[1], 20, k))
    O.overlay(big, b, x0, 480, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(max(0, x0), 480, x0 + b.shape[1], 480 + b.shape[0]))
    dx, dy = K.shake(t, 0.05, 24, 0.9)
    return K.shift(big, dx, dy)


# ================================================================== 1: DASH — «Sounds like you said — ADD a DRIVER!»
def r_dash(t, u):
    return insert(t, STREET, 'STATE FEE INSURANCE', 'DRIVER ADDED: SAL +$80', 5.30)


# ================================================================== 2: DOLLAR — in the car on the street; Sal on the hood (a drone passes behind: clue)
def r_dollar(t, u):
    k = sm(u / 4.9)
    Z = 1.6
    cx, cy = 610.0 - 20 * k, 520.0
    v = V(STREET, cx, cy, Z)
    cs = 4.0 * 3 * Z
    puff = sm((t - 6.05) / 0.35)
    duke = dict(expr='proud', mouth_=mouth('duke', t, 1.8), puff=puff, look=(0.3, -0.3), hand_n=(30.0, 42.0), hand_f=(-28.0, 42.0))
    sal = dict(expr='dead', mouth_=mouth('sal', t, 2.2), look=(-0.9, 0.2))
    acts = car_acts(v, 540, 1820, cs, t, duke=duke, sal=sal)
    if 7.6 <= t < 9.4:
        f = (t - 7.6) / 1.8
        acts.insert(0, A(C.drone, *wpt(v, lerp(1150, -100, f), 330 + math.sin(t * 3) * 10), 4.0, t=t, siren=False))
    return K.shot(STREET, K.light_mall, cx, cy, Z, acts=acts)


# ================================================================== 3: SELL — out of the car, FOR SALE $500: «Eagles don't NEED cars! Sal, hit the SCREAM!»
def r_sell(t, u):
    Z = 1.45
    cx, cy = 600.0, 520.0
    v = V(STREET, cx, cy, Z)
    cs = 4.0 * 3 * Z
    sal = dict(expr='dead', look=(-0.6, 0.4), speaker_=True, speaker_on=t >= 13.70)
    acts = car_acts(v, 700, 1840, cs, t, sal=sal, sale=True)
    duke = A(C.duke, *wpt(v, 250, 1860), cs * IC * 1.05, t=t, expr='proud' if t < 12.4 else 'roar', mouth_=mouth('duke', t, 1.8),
             puff=0.6, look=(0.6, -0.4), hand_n=(26.0, 60.0) if t > 12.4 else (20.0, 30.0))
    return K.shot(STREET, K.light_mall, cx, cy, Z, acts=[duke] + acts)


# ================================================================== 4: TAKEOFF — the epic (borrowed) scream; Duke launches into the sky
def r_takeoff(t, u):
    k = sm(u / 1.05)
    Z = 1.45
    cx, cy = 600.0, 520.0 - 120.0 * k
    v = V(STREET, cx, cy, Z)
    cs = 4.0 * 3 * Z
    sal = dict(expr='dead', look=(-0.6, 0.6), speaker_=True, speaker_on=True)
    acts = car_acts(v, 700, 1840 + 120 * 3 * Z * k, cs, t, sal=sal, sale=True)
    oy = lerp(1860, 900, k)
    duke = A(C.duke, *wpt(v, 250 + 200 * k, oy), cs * IC * 1.05, t=t, expr='roar', mouth_=0.9, fly=t * 3.0, look=(0.5, -0.8),
             rot=-15.0 * k, pivot=(0.0, 30.0))
    def fx_(big, v_):
        K.feathers(big, t, SCREAM + 0.05, 330, 1500, n=14, seed=13)
        K.speed_lines(big, t, 0.5 * k, n=12, seed=6, horizontal=False)
    return K.shot(STREET, K.light_mall, cx, cy, Z, acts=[duke] + acts, fx_=fx_)


# ================================================================== 5: SOAR — over the jammed interstate: «No insurance! No GAS!»
def r_soar(t, u):
    k = u / (CUTS[6] - CUTS[5])
    Z = 1.0
    cx, cy = 520.0 + 200 * sm(k), 380.0
    v = V(HWY, cx, cy, Z)
    ox, oy = lerp(-40, 640, k), lerp(900, 760, k) + math.sin(t * 7.0) * 16
    duke = A(C.duke, *wpt(v, ox, oy), 8.5, t=t, expr='joy', mouth_=mouth('duke', t, 1.8), fly=t * 2.6, look=(1.0, 0.0), rot=-38.0,
             pivot=(0.0, 30.0), shades='eyes')
    acts = [duke]
    if t >= 16.80:
        f = sm((t - 16.8) / 0.7)
        acts.append(A(C.drone, *wpt(v, lerp(1180, 900, f), lerp(480, 640, f)), 9.0, t=t, siren=True))
    def fx_(big, v_): K.speed_lines(big, t, 0.6, n=14, seed=4)
    return K.shot(HWY, K.light_mall, cx, cy, Z, acts=acts, fx_=fx_)


# ================================================================== 6: TWIST — the Sky Patrol drone: «Unregistered DRONE! Land NOW!»
def r_twist(t, u):
    Z = 1.1
    cx, cy = 700.0, 360.0
    v = V(HWY, cx, cy, Z)
    duke = A(C.duke, *wpt(v, 330, 1250 + math.sin(t * 6) * 20), 10.0, t=t, expr='shock', mouth_=0.4, fly=t * 3.0, look=(0.9, -0.3),
             flop=1.0)
    dr = A(C.drone, *wpt(v, 780 + math.sin(t * 2) * 20, 860), 16.0, t=t, siren=True)
    big = K.shot(HWY, K.light_mall, cx, cy, Z, acts=[duke, dr])
    on = int(t * 6) % 2 == 0
    tint = np.array((255, 40, 40) if on else (40, 80, 255), np.float32)
    big[:] = np.clip(big * 0.86 + tint * 0.14, 0, 255).astype(np.uint8)
    return big


# ================================================================== 7: TICKET — on the shoulder: «No flight plan. No license. No AIRCRAFT insurance.»
def r_ticket(t, u):
    k = sm(u / 5.3)
    Z = 1.1
    cx, cy = 600.0 - 30 * k, 470.0
    v = V(SHO, cx, cy, Z)
    duke = A(C.duke, *wpt(v, 300, 1830), 14.0, t=t, expr='stunned' if t < 23.6 else 'shock', mouth_=0.1, look=(0.9, 0.1),
             hand_n=(18.0, 28.0), hand_f=(-14.0, 28.0))
    cop = A(C.officer, *wpt(v, 790, 1830), 18.4, t=t, flip=True, expr='glare', mouth_=mouth('officer', t, 1.6), look=(0.8, 0.1), ticket=True)
    dr = A(C.drone, *wpt(v, 820 + math.sin(t * 2) * 14, 560), 10.0, t=t, siren=True)
    return K.shot(SHO, K.light_mall, cx, cy, Z, acts=[dr, duke, cop])


# ================================================================== 8: BIRD — «I'm a BIRD!» — «Birds got a PILOT'S license?»
def r_bird(t, u):
    k = sm(u / 3.3)
    Z = 1.1 + 0.15 * k
    cx, cy = 580.0, 470.0
    v = V(SHO, cx, cy, Z)
    sc = Z / 1.1
    duke = A(C.duke, *wpt(v, 300 - 40 * k, 1830 + 60 * k), 14.0 * sc, t=t, expr='roar' if t < 26.7 else 'shock', mouth_=mouth('duke', t, 2.0),
             flop=0.9 if t < 26.7 else 0.0, tremble=0.6 if t < 26.7 else 0.0, look=(0.9, -0.2), hand_n=(26.0, 56.0) if t < 26.7 else (18.0, 28.0))
    cop = A(C.officer, *wpt(v, 800 + 30 * k, 1840 + 60 * k), 18.4 * sc, t=t, flip=True, expr='dead', mouth_=mouth('officer', t, 1.6),
            look=(0.8, 0.1), ticket=True)
    big = K.shot(SHO, K.light_mall, cx, cy, Z, acts=[duke, cop])
    dx, dy = K.shake(t, 25.50, 14, 0.35)
    return K.shift(big, dx, dy)


# ================================================================== 9: BUTTON — his old hatchback crawls by, Sal at the wheel: «Need a ride? Twenty BUCKS.»
def r_button(t, u):
    Z = 1.1
    cx, cy = 560.0, 470.0
    v = V(SHO, cx, cy, Z)
    f = sm(u / 1.6)
    cs = 17.0
    duke = A(C.duke, *wpt(v, 250, 1830), 14.0, t=t, expr='dead' if t < 30.5 else 'sad', look=(0.9, 0.0), hand_n=(18.0, 28.0), hand_f=(-14.0, 28.0))
    sal = dict(expr='dead', mouth_=mouth('sal', t, 2.2), look=(-0.4, -0.6), bob=False)
    acts = car_acts(v, lerp(1500, 760, f), 1880, cs, t, sal_driver=sal, sale=True, drive=t * (1 - f) * 3, honk=1.0 if 31.1 <= t < 31.6 else 0.0)
    return K.shot(SHO, K.light_mall, cx, cy, Z, acts=[duke] + acts)


R = [r_hook, r_dash, r_dollar, r_sell, r_takeoff, r_soar, r_twist, r_ticket, r_bird, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SEND = K.st_lines(['SEND THIS TO SOMEONE WHOSE', 'INSURANCE WENT UP', 'FOR NO REASON'], size=36,
                  colors=[(255, 255, 255), (130, 255, 200), (130, 255, 200)])
CHOICE = K.st_lines(['WHAT COSTS MORE?', 'A) THE CAR  B) THE WINGS'], size=40, colors=[(255, 214, 80), (130, 255, 200)])
SHOW = K.Show(EPI, 4, ['$400 A MONTH?!'], hook_t=(0.08, 2.00), hook_y=330, hook_size=70,
              stickers=[(K.st('FREEDOM!', fg=(130, 255, 200), size=72), SCREAM + 0.1, 15.0, 540, 330),
                        (K.st('DRONE?!', fg=(255, 214, 80), size=80), 17.57, 19.6, 540, 330),
                        (SEND, 20.30, 22.60, 540, 360),
                        (K.st('AIRCRAFT INSURANCE: $900/MO', fg=(255, 214, 80), size=40), 23.80, 25.40, 540, 360),
                        (CHOICE, 31.00, 33.0, 540, 390)],
              flashes=[TWIST, SCREAM], mosaics=[CUTS[5], CUTS[7]],
              cap_y={0: 1460, 1: 470, 2: 1420, 3: 1420, 4: 1420, 5: 1420, 6: 1500, 7: 1420, 8: 1420, 9: 1420})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
