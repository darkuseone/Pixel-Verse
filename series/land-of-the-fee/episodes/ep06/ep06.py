"""S01E06 «$89 TO SIT?!» (31.0 s, twist at 17.30 s / 56 %, type: the reward is the same problem). Season finale.
HOOK: Duke at the Penny Air gate counter screams at the fare breakdown — «EIGHTY-NINE bucks?! To SIT?!» (BASIC FARE $19, SEAT $89,
CARRY-ON $65, BREATHING $5). The kiosk Fee-Bee: «Sounds like you said — CARRY-ON! Wings count!» — «I'm a BALD EAGLE. I'm on the
DOLLAR!» — Sal on the bag sizer: «Then fold in HALF. Like the dollar.» — Duke squeezed into the sizer (FITS! +$65) — he breaks out:
«I'm an EAGLE. I'll fly MYSELF! Sal, the SCREAM!» — Sal's speaker plays the hawk scream (E05's Rex), Duke flies south over the sea and
lands on a sunset beach: «No fees. No bots.» TWIST: the coconut on the palm wakes up as Fee-Bee — «Welcome to paradise, Duke! RESORT
fee!» — BEACH ACCESS $25, LOUNGER $40/HR, SUNSET: PREMIUM. Sal is already on the lounger with a cocktail: «Got here free. Checked BAG.»
— the coconut: «Sounds like you said — UPGRADE!» — BUTTON: Duke's very first scream from E01, «REPRESENTATIVE!!» (season loop),
«SEASON 2: TAX SEASON».  Clue in the first half: «POWERED BY FEE-BEE» on the gate pillar, the kiosk is Fee-Bee.
  python3 ep06.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import overlays as O
import stage as ST
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
from episode import Episode
from props import feecast as C
from props import feekit as K
from props.feekit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, SCREAM, FOLD, PRICES

EPI = Episode('ep06', VOICE, DUR, FPS, colors=K.COL, slug=SLUG,
              endcard=dict(style='fee', lang='us', promise='SEASON 2: TAX SEASON', cy=1470))
GATE, BEACH = K.world('gate'), K.world('beach')
SIZER = (345.0, 470.0)                         # the bag-sizer frame in gate.png: bottom centre (world px)
COCO = (1040.0, 242.0)                         # the coconut cluster on the palm in beach.png (world px)
LOUNGER = (250.0, 548.0)                       # the lounger seat in beach.png (world px)
BILL = ['BASIC FARE   $19', 'SEAT         $89', 'CARRY-ON     $65', 'BREATHING    $5']


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def V(world_, cx, cy, Z):
    return view_at(world_, cx, cy, Z, 180, 320)


def coco_act(v_unused, t, s, awake):
    return A(C.coconut, COCO[0], COCO[1], s, pin='center', t=t, talk=mouth('feebee', t, 1.6), awake=awake)


# ================================================================== 0: HOOK — at the Penny Air counter: «EIGHTY-NINE bucks?! To SIT?!»
def r_hook(t, u):
    dx, dy = K.shake(t, 0.05, 24, 0.9)
    def fx_(big, v, a):
        hx, hy = aout(a, v, 'head')
        K.feathers(big, t, 0.12, hx, hy - 60, n=14, seed=21)
    big, a = K.cu(C.duke, t, GATE, 200.0, 360.0, 1.35, 22.0, head=(400, 880), light=K.light_mall, blur=4, extra_fx=fx_,
                  expr='roar', mouth_=max(0.5, mouth('duke', t, 2.0)), flop=1.0, tremble=0.8, look=(0.9, 0.4), hand_n=(24.0, 34.0))
    b = K.bill_ui(BILL, total='TOTAL $178', title='PENNY AIR', hi=1, w=500)
    k = sm(u / 0.25)
    x0 = int(lerp(OUT_W, OUT_W - b.shape[1] - 20, k))
    O.overlay(big, b, x0, 1220, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(x0, 1220, min(OUT_W, x0 + b.shape[1]), 1220 + b.shape[0]))
    return K.shift(big, dx, dy)


# ================================================================== 1: KIOSK — «Sounds like you said — CARRY-ON! Wings count!»
def r_kiosk(t, u):
    big = K.dof(K.shot(GATE, K.light_mall, 220.0, 380.0, 1.3), 9)
    big[:] = (big * 0.62).astype(np.uint8)
    t_st = 4.60
    scr = K.screen_ui(t, mouth('feebee', t, 1.6), 'PENNY AIR', stamp='WINGS = CARRY-ON +$65' if t >= t_st else None,
                      stamp_k=sm((t - t_st) / 0.12), w=700, h=1060, sub='SELF CHECK-IN • FEE-BEE AI')
    x0, y0 = (OUT_W - scr.shape[1]) // 2, 600
    O.overlay(big, scr, x0, y0, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(x0, y0, x0 + scr.shape[1], y0 + scr.shape[0]))
    if t >= t_st: K.dollars(big, t, t_st, OUT_W // 2, y0 + scr.shape[0] - 160, n=8, seed=6)
    return big


# ================================================================== 2: DOLLAR — Duke proud by the sizer, Sal on top: «Then fold in HALF.»
def r_dollar(t, u):
    k = sm(u / 4.15)
    Z = 1.1 + 0.06 * k
    cx, cy = 420.0, 330.0
    puff = sm((t - 5.32) / 0.35)
    duke = A(C.duke, 420.0, 640.0, 11.5 * Z, t=t, expr='proud' if t < 7.9 else 'glare', mouth_=mouth('duke', t, 1.8), puff=puff,
             look=(-0.6, -0.2) if t >= 7.9 else (0.8, 0.0), hand_n=(20.0, 30.0))
    sal = A(C.sal, 330.0, 272.0, 13.5 * Z, t=t, expr='dead', mouth_=mouth('sal', t, 2.2), look=(0.9, -0.3))
    return K.shot(GATE, K.light_mall, cx, cy, Z, acts=[sal, duke])


# ================================================================== 3: FOLD — Duke squeezed inside the sizer: FITS! +$65
def r_fold(t, u):
    Z = 1.5
    cx, cy = SIZER[0], 365.0
    sq = sm((t - FOLD) / 0.25)
    duke = A(C.duke, SIZER[0], SIZER[1] - 4, lerp(10.0, 8.0, sq), t=t, expr='panic', mouth_=0.0, tremble=1.0, flop=1.0,
             look=(0.0, 0.6), hand_n=(12.0, 30.0), hand_f=(-12.0, 30.0))
    fr = A(C.sizer_front, SIZER[0], SIZER[1], 31.0, t=t, w=19.0, h=23.0)
    def fx_(big, v_):
        K.feathers(big, t, FOLD + 0.1, 540, 1000, n=12, seed=23)
    big = K.shot(GATE, K.light_mall, cx, cy, Z, acts=[duke, fr], fx_=fx_)
    dx, dy = K.shake(t, FOLD, 16, 0.5)
    return K.shift(big, dx, dy)


# ================================================================== 4: TAKEOFF — he breaks out: «I'll fly MYSELF! Sal, the SCREAM!»
def r_takeoff(t, u):
    Z = 1.0
    cx, cy = 700.0, 350.0
    v = V(GATE, cx, cy, Z)
    go = sm((t - 13.30) / 0.85)
    fly = t * 2.8 if t >= 12.2 else None
    duke = A(C.duke, 620.0 + 260 * go, 650.0 - 330 * go, 13.0, t=t, expr='roar' if t < 12.2 else 'glare', mouth_=mouth('duke', t, 1.8),
             fly=fly, puff=0.6 if t < 12.2 else 0.0, flop=0.8, look=(0.9, -0.3) if t >= 12.2 else (0.6, 0.0),
             hand_n=None if fly else (22.0, 38.0), rot=-24.0 * go, pivot=(0.0, 30.0))
    sal = A(C.sal, 800.0, 432.0, 11.0, t=t, flip=True, expr='dead', mouth_=mouth('sal', t, 2.2), look=(-0.8, 0.0),
            speaker_=True, speaker_on=t >= 13.90)
    def fx_(big, v_):
        K.feathers(big, t, 10.80, 420, 1500, n=14, seed=25)
        if t >= 13.3: K.speed_lines(big, t, go, n=12, seed=27)
    return K.shot(GATE, K.light_mall, cx, cy, Z, acts=[sal, duke], fx_=fx_)


# ================================================================== 5: SEA — over the sea and onto the sand: «No fees. No bots.»
def r_sea(t, u):
    k = sm(u / 3.1)
    Z = 1.0
    cx, cy = 600.0 + 60 * k, 400.0
    v = V(BEACH, cx, cy, Z)
    land = 16.30
    q = min(1.0, (t - CUTS[5]) / (land - CUTS[5]))
    if t < land:
        ox, oy = lerp(-120, 560, sm(q)), lerp(420, 1560, q * q) + math.sin(t * 7) * 12
        duke = A(C.duke, *wpt(v, ox, oy), 12.0, t=t, expr='joy', mouth_=mouth('duke', t, 1.8), fly=t * 2.8, shades='eyes',
                 rot=lerp(-30.0, -6.0, q), pivot=(0.0, 30.0), look=(1.0, 0.2))
    else:
        duke = A(C.duke, *wpt(v, 560, 1840), 12.0, t=t, expr='content' if t < 16.9 else 'smug', mouth_=mouth('duke', t, 1.8),
                 shades='eyes', puff=sm((t - land) / 0.4), look=(0.0, 0.0), hand_n=(18.0, 32.0))
    def fx_(big, v_):
        if t < land: K.speed_lines(big, t, 0.5, n=10, seed=29)
    big = K.shot(BEACH, K.light_beach, cx, cy, Z, acts=[duke], fx_=fx_)
    dx, dy = K.shake(t, land, 12, 0.3)
    return K.shift(big, dx, dy)


# ================================================================== 6: TWIST — the coconut wakes up as Fee-Bee: «Welcome to paradise! RESORT fee!»
def r_twist(t, u):
    k = sm(u / 2.65)
    Z = 1.55 + 0.15 * k
    cx, cy = COCO[0], 330.0
    awake = sm((t - TWIST + 0.1) / 0.3)
    coco = A(C.coconut, COCO[0], COCO[1], 19.0 * Z, pin='center', t=t, talk=mouth('feebee', t, 1.6), awake=awake)
    big = K.shot(BEACH, K.light_beach, cx, cy, Z, acts=[coco])
    return big


# ================================================================== 7: PRICES — BEACH ACCESS $25, LOUNGER $40/HR, SUNSET: PREMIUM
def r_prices(t, u):
    Z = 1.0
    cx, cy = 600.0, 400.0
    v = V(BEACH, cx, cy, Z)
    hit = sum(t >= x for x in PRICES)
    duke = A(C.duke, *wpt(v, 790, 1860), 12.0, t=t, expr='shock' if hit < 3 else 'stunned', shades='eyes', look=(-0.7, -0.4),
             tremble=0.5 if hit == 3 else 0.0, hand_n=(14.0, 26.0))
    def fx_(big, v_):
        for x in PRICES:
            if t >= x: K.dollars(big, t, x, 380, 1500, n=6, seed=int(x * 10))
    return K.shot(BEACH, K.light_beach, cx, cy, Z, acts=[duke], fx_=fx_)


# ================================================================== 8: SAL — on the lounger with a cocktail: «Got here free. Checked BAG.»
def r_sal(t, u):
    k = sm(u / 2.5)
    Z = 1.45 + 0.08 * k
    cx, cy = LOUNGER[0] + 10, 450.0
    sal = A(C.sal, LOUNGER[0] + 10, LOUNGER[1], 14.0 * Z, t=t, expr='content', mouth_=mouth('sal', t, 2.2), look=(0.4, -0.3),
            bob=False)
    glass = A(lambda sp, t=0.0: C.cocktail(sp, (0.0, 0.0)), LOUNGER[0] + 78, LOUNGER[1] - 34, 26.0 * Z, t=t)
    def fx_(big, v_):
        hx, hy = aout(sal, v_, 'head')
        K.label(big, 'CHECKED BAG #2', int(hx) - 60, int(hy) + 170, fg=(20, 20, 30), bg=(255, 214, 60), size=40)
    return K.shot(BEACH, K.light_beach, cx, cy, Z, acts=[sal, glass], fx_=fx_)


# ================================================================== 9: UPGRADE — the coconut, closer: «Sounds like you said — UPGRADE!»
def r_upgrade(t, u):
    Z = 1.8
    cx, cy = COCO[0], 300.0
    coco = A(C.coconut, COCO[0], COCO[1], 19.0 * Z, pin='center', t=t, talk=mouth('feebee', t, 1.6), awake=1.0)
    big = K.shot(BEACH, K.light_beach, cx, cy, Z, acts=[coco])
    dx, dy = K.handheld(t, 0.6)
    return K.shift(big, dx, dy)


# ================================================================== 10: BUTTON — E01's first scream: «REPRESENTATIVE!!» (season loop)
def r_button(t, u):
    inhale = t < 26.80
    def fx_(big, v, a):
        if not inhale:
            hx, hy = aout(a, v, 'head')
            K.feathers(big, t, 26.85, hx, hy - 60, n=16, seed=31)
    big, a = K.cu(C.duke, t, BEACH, 640.0, 360.0, 1.35, 22.0, head=(540, 1060), light=K.light_beach, blur=4, extra_fx=fx_,
                  expr='puff' if inhale else 'roar', mouth_=0.0 if inhale else max(0.5, mouth('duke', t, 2.0)), shades='eyes',
                  puff=1.0 if inhale else 0.3, flop=0.0 if inhale else 1.0, tremble=0.0 if inhale else 0.8, look=(0.0, 0.0),
                  hand_n=(24.0, 34.0), hand_f=(-24.0, 34.0))
    dx, dy = K.shake(t, 26.80, 26, 1.0)
    return K.shift(big, dx, dy)


R = [r_hook, r_kiosk, r_dollar, r_fold, r_takeoff, r_sea, r_twist, r_prices, r_sal, r_upgrade, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

P1 = K.st('BEACH ACCESS $25', fg=(255, 90, 110), size=42)
P2 = K.st('LOUNGER $40/HR', fg=(255, 214, 80), size=42)
P3 = K.st('SUNSET: PREMIUM', fg=(130, 255, 200), size=42)
SEND = K.st_lines(['SEND THIS TO SOMEONE', 'WHO PAID FOR A SEAT'], size=40, colors=[(255, 255, 255), (130, 255, 200)])
SUNSET = K.st_lines(['SUNSET+', '$9.99/MIN'], size=54, colors=[(255, 214, 80), (255, 90, 110)])
S2 = K.st_lines(['SEASON 2:', 'TAX SEASON'], size=60, colors=[(255, 255, 255), (130, 255, 200)])
CHOICE = K.st_lines(['WHERE DO FEES END?', 'A) NOWHERE  B) NOWHERE'], size=40, colors=[(255, 214, 80), (130, 255, 200)])
SHOW = K.Show(EPI, 6, ['$89 TO SIT?!'], hook_t=(0.08, 2.00), hook_y=330, hook_size=54,
              stickers=[(K.st('FITS! +$65', fg=(255, 214, 80), size=80), FOLD + 0.4, CUTS[4], 540, 330),
                        (K.st("SHE'S EVERYWHERE?!", fg=(255, 90, 110), size=48), TWIST + 0.03, CUTS[7], 540, 1160),
                        (P1, PRICES[0], CUTS[8], 430, 420),
                        (P2, PRICES[1], CUTS[8], 430, 520),
                        (P3, PRICES[2], CUTS[8], 430, 620),
                        (SEND, 22.20, CUTS[9] - 0.05, 540, 340),
                        (SUNSET, 25.60, CUTS[10], 540, 1160),
                        (S2, 28.30, 29.98, 540, 640),
                        (CHOICE, 29.00, DUR, 540, 390)],
              flashes=[TWIST, SCREAM, 26.80], mosaics=[CUTS[5], CUTS[10]],
              cap_y={0: 600, 1: 450, 2: 1420, 3: 1420, 4: 1420, 5: 1420, 6: 1420, 7: 1180, 8: 1420, 9: 1420, 10: 600})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
