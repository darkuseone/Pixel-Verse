"""S01E01 «FREE PARKING?» (pilot; 45.0 s, twist at 25.58 s / 57 %, type: the reward is the same problem).
Main question (opened at 0 s, closed at ~76 %): can you park for free on Ocean Drive?
HOOK: Vince in his white convertible on Ocean Drive at sunset — «Ocean Drive. Sunset. And I'm parking for FREE, baby.» Fran, the neon
flamingo on the roof of The Palms, lights up: «Honey. Nobody parks free on Ocean Drive.» Vince flips a quarter at the meter — «It's
eighty-six. Parking's a QUARTER.» — the coin bounces off «PAY BY APP ONLY». «Honey, it's twenty twenty-six. There's an APP.» The app:
$14.00/hour + a $3.50 CONVENIENCE FEE. «New plan. If I never STOP, it's not PARKING.» He circles the block: sunset -> neon night ->
dawn, «Lap forty-seven. Send this to your friend who does this.» TWIST: a glowing «FREE PARKING*» board at a tow truck ramp — he drives
up — CLANK, the bed lifts. Rey: «Tow and storage. Three-fifty, amigo.» — «It SAID free!» — the asterisk: «Parking's free. The RIDE'S
three-fifty.» — «FINE! I'll pay in QUARTERS!» — «Tow's pay-by-APP, amigo.» (callback). Towed down Ocean Drive: «Still the coolest
guy on Ocean Drive.» Fran (neon in the cab's back window): «Coolest guy on a TOW truck, honey.»
Clue in the first half: the TOW-AWAY ZONE sign and the tow truck's beacon glow in the laps; «PAY BY APP» plate on the street.
  python3 ep01.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import fx
import atmos as AT
import overlays as O
import stage as ST
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
from cam25 import glide, kick
from episode import Episode
from props import v86cast as C
from props import v86kit as K
from props import mimic as M
from props.v86kit import A, wpt, aout, WSV
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='v86', lang='us', promise='TOMORROW: THE FEES'))
TAB = (C.XTRA, C.EXPR)
FV = M.Face([(0.0, 'smooth'), (3.9, 'cool'), (7.2, 'smooth'), (10.1, 'shock'), (14.4, 'outraged'), (17.4, 'scheming'), (19.4, 'cool'),
             (22.4, 'tired'), (25.6, 'ecstatic'), (27.95, 'shock'), (31.0, 'outraged'), (34.6, 'nervous'), (36.8, 'defeated'),
             (38.8, 'proudsad')], TAB, seed=3)
FR = M.Face([(0.0, 'chill'), (31.0, 'chill'), (37.0, 'gotcha')], TAB, seed=8)
OCEAN_Y = 616.0                 # ground line of a car parked at the far curb of Ocean Drive (world px)
SIDE_Y = 612.0
FRAN_W = (505.0, 233.0)         # Fran on the roof of The Palms (bottom centre, world px)
FRAN_H = 104.0                   # her height in world px


def mouth(who, t):
    return M.mouth(EPI.talk, who, t)


def vface(t, base=(0.7, 0.0), **kw):
    m = mouth('vince', t)
    return dict(expr=FV.speak(t, m), mouth_=m, blink=FV.blink(t), look=FV.look(t, base), **kw), M.bob(t, m)


def rface(t, base=(0.7, 0.0)):
    m = mouth('rey', t)
    return dict(expr=FR.speak(t, m), mouth_=m, blink=FR.blink(t), look=FR.look(t, base)), M.bob(t, m)


def V(name, cx, cy, Z):
    return view_at(K.world(name), cx, cy, Z, 180, 320)


def car_at_head(v, hx, hy, z):
    """world ground point of the car that puts seated Vince's head at output (hx, hy)"""
    S = WSV * 3 * v.Z * z
    return wpt(v, hx + 3.08 * S, hy + 63.2 * S)


def fran_on_roof(big, v, t, on=1.0, look=0.0):
    x, y = v.opt(*FRAN_W)
    K.fran(big, x, y, FRAN_H * 3 * v.Z, t, talk=mouth('fran', t), on=on, look=look)


def fg(acts, near=0.99):
    for a in acts: a.near = near
    return acts


# ================================================================== 0: HOOK — CU Vince cruising Ocean Drive at sunset
def r_hook(t, u):
    Z = 1.35
    cx = 470.0 + 46.0 * u
    v = V('ocean', cx, 360.0, Z)
    kw, dy = vface(t, (0.8, -0.1), hair_wind=0.7, glint=sm((u - 0.4) / 0.3) * (1 - sm((u - 1.2) / 0.3)), sparkle=1.0 if 2.6 < u < 3.6 else 0.0)
    wx, wy = car_at_head(v, 400, 1000 + dy * 10, 3.3)
    acts = fg(K.car_group(v, wx, wy, t, vince_kw=kw, speed=14.0, z=3.3))
    def f(big, _):
        AT.flare(big, 640, 330, 0.8)
    big = K.shot('ocean', K.light_sunset, cx, 360.0, Z, acts=acts, par=(-14 + 8 * u, 0), focus=0.95, dof_k=26, fx_=f, t=t,
                 rays=dict(src=(620, 330), a=0.30), bokeh_=True)
    return big


# ================================================================== 1: FRAN lights up — wide, the car rolls to the curb
def r_fran_on(t, u):
    Z = 1.0
    cx = lerp(470.0, 560.0, glide(u / 3.2))
    v = V('ocean', cx, 380.0, Z)
    xcar = lerp(170.0, 600.0, glide(min(1.0, u / 2.7)))
    kw, dy = vface(t, (-0.2, -0.6))
    acts = K.car_group(v, xcar, OCEAN_Y, t, vince_kw=kw, speed=10.0 * (1 - min(1, u / 2.7)))
    on = 0.0 if u < 0.07 else (1.0 if u > 0.55 else (1.0 if (int(u * 22) % 3) else 0.15))
    def f(big, _): fran_on_roof(big, v, t, on=on, look=-0.6)
    return K.shot('ocean', K.light_sunset, cx, 380.0, Z, acts=acts, par=(-10 + 6 * u, 0), fx_=f, t=t, dof_k=14)


# ================================================================== 2: METER — «Watch me. It's eighty-six. Parking's a QUARTER.»
def r_meter(t, u):
    Z = 2.1
    cx = 610.0 + 6.0 * u
    v = V('ocean', cx, 520.0, Z)
    toss = 9.05
    up = 7.6 < t < toss
    hand = (25.0, 74.0 + 3.0 * math.sin(t * 9)) if up else ((30.0, 66.0) if t < 7.6 else (32.0, 70.0))
    kw, dy = vface(t, (0.9, 0.2), hand_n=hand)
    acts = K.car_group(v, 560.0, OCEAN_Y, t, vince_kw=kw)
    S = WSV * 3 * v.Z
    mw = (650.0, OCEAN_Y - 16.0)                                           # meter on the sidewalk just behind the door
    meter = A(C.meter, mw[0], mw[1], S * 1.10, t=t)
    acts = [meter] + acts
    def f(big, _):
        vi = acts[2]
        if hasattr(vi, 'last') and t < toss + 0.9:
            hx, hy = aout(vi, v, 'hand')
            if t < toss:                                                   # flipping in the hand
                k = (t * 2.6) % 1.0; cy = hy - 40 - 140 * math.sin(math.pi * k)
                coin(big, hx, cy, S * 1.4, t)
            else:                                                          # tossed toward the slot
                mx, my = v.opt(mw[0], mw[1] - 46 * WSV * 1.10)
                k = (t - toss) / 0.9
                coin(big, lerp(hx, mx, k), lerp(hy - 40, my, k) - 260 * math.sin(math.pi * k), S * 1.4, t)
    return K.shot('ocean', K.light_sunset, cx, 520.0, Z, acts=acts, par=(-8 + 10 * u / 2.8, 0), fx_=f, t=t)


def coin(big, x, y, s, t):
    sp = K.VX.draw(C.coin, s, h=(0.0, 0.0))
    w = abs(math.cos(t * 14))                                              # spinning: squash horizontally
    K.VX.blit(big, sp, x, y, s, None)
    if w < 0.3: big[int(y) - 4:int(y) + 4, int(x) - 30:int(x) + 30] = np.maximum(big[int(y) - 4:int(y) + 4, int(x) - 30:int(x) + 30], 200)


# ================================================================== 3: BONK — insert: the coin bounces off «PAY BY APP ONLY»
def r_bonk(t, u):
    Z = 1.45
    v = V('ocean', 640.0, 470.0, Z)
    s = 24.0
    mx, my = 540.0, 1650.0
    meter = A(C.meter, *wpt(v, mx, my), s, t=t, rim=(K.VX.SUN, K.PINK))
    meter.near = 0.99
    def pre(big, _): big[:] = K.blur(big, 10)
    def f(big, _):
        sx, sy = mx, my - 44.6 * s
        if u < 0.15:
            k = u / 0.15; cx, cy = lerp(1000, sx + 30, k), lerp(600, sy, k)
        else:
            k = (u - 0.15) / 0.55; cx, cy = sx + 30 + 700 * k, sy - 380 * math.sin(math.pi * min(1, k * 0.9)) + 600 * k * k
        coin(big, cx, cy, 16.0, t)
        if 0.13 < u < 0.3: AT.sparks(big, sx + 20, sy, t, 10.18, n=10, col=(255, 230, 120), seed=3, life=0.25, speed=500, px=8)
    return K.shot('ocean', K.light_sunset, 640.0, 470.0, Z, acts=[meter], pre=pre, focus=0.99, dof_k=0, fx_=f, t=t,
                  kick=kick(t, [(10.2, 0.8)]), motes=False)


# ================================================================== 4: FRAN CU — «Honey, it's twenty twenty-six. There's an APP.»
def r_fran_cu(t, u):
    Z = 1.45
    v = V('ocean', 505.0, 220.0, Z)
    def pre(big, _): big[:] = K.blur(big, 7)
    def f(big, _):
        K.fran(big, 560, 1430, 1080, t, talk=mouth('fran', t), on=1.0, lid=0.6, look=0.6 * math.sin(t * 0.7))
    return K.shot('ocean', K.light_sunset, 505.0, 220.0, Z * (1 + 0.012 * u), pre=pre, dof_k=0, fx_=f, t=t, bloom=(200, 30, 0.7))


# ================================================================== 5: APP — the phone: $14.00 / HOUR + $3.50 CONVENIENCE FEE
def r_app(t, u):
    Z = 1.4
    v = V('ocean', 600.0, 420.0, Z)
    kw, dy = vface(t, (0.9, 0.5), hand_n=(26.0, 60.0))
    wx, wy = car_at_head(v, 300, 1340 + dy * 10, 2.6)
    acts = fg(K.car_group(v, wx, wy, t, vince_kw=kw, z=2.6))
    def f(big, _):
        ph = K.phone_screen(t, t_fee=15.75)
        ph = np.array(Image.fromarray(ph).resize((int(ph.shape[1] * 1.15), int(ph.shape[0] * 1.15)), Image.NEAREST))
        O.overlay(big, ph, 200, 190 + int(8 * math.sin(t * 3)), 1.0)
        if ST.LOG[0] is not None: ST.log('card', bbox=(470, 230, 470 + ph.shape[1], 230 + ph.shape[0]))
    return K.shot('ocean', K.light_sunset, 600.0, 420.0, Z, acts=acts, focus=0.97, dof_k=30, fx_=f, t=t, kick=kick(t, [(15.75, 0.9)]))


# ================================================================== 6: PLAN — ECU: «New plan. If I never STOP…»
def r_plan(t, u):
    Z = 1.35
    v = V('ocean', 640.0, 400.0, Z)
    kw, dy = vface(t, (0.9, 0.0), glint=sm((u - 0.2) / 0.25) * (1 - sm((u - 0.9) / 0.3)))
    wx, wy = car_at_head(v, 470, 1080 + dy * 12, 4.4)
    acts = fg(K.car_group(v, wx, wy, t, vince_kw=kw, z=4.4 * (1 + 0.02 * u)))
    def f(big, _):
        if 0.25 < u < 1.1: AT.flare(big, 600, 860, 0.7 * math.sin(math.pi * (u - 0.25) / 0.85), col=(255, 120, 200))
    return K.shot('ocean', K.light_sunset, 640.0, 400.0, Z, acts=acts, focus=0.98, dof_k=34, fx_=f, t=t, bokeh_=True, par=(6 * u, 0))


# ================================================================== 7-8: LAPS — sunset -> neon night -> dawn, LAP 1 … 47
def lap_frame(name, light, t, x, lap, look=0.0):
    Z = 1.0
    cx = 600.0
    v = V(name, cx, 380.0, Z)
    kw, dy = vface(t, (0.9, 0.0), hair_wind=0.9)
    acts = K.car_group(v, x, OCEAN_Y + 22, t, vince_kw=kw, speed=20.0, lights=name == 'ocean_night')
    def f(big, _): fran_on_roof(big, v, t, look=look)
    big = K.shot(name, light, cx, 380.0, Z, acts=acts, par=(0, 0), fx_=f, t=t, bokeh_=name == 'ocean_night', dof_k=12)
    fx.speed_lines(big, t, 0.25)
    return big


def lap_x(t, t0, period=1.5):
    k = ((t - t0) % period) / period
    return lerp(160.0, 1180.0, k)


def r_laps_a(t, u):
    if u < 1.45:
        return lap_frame('ocean', K.light_sunset, t, lap_x(t, 19.35, 1.45), 1)
    big = lap_frame('ocean_night', K.light_night, t, lap_x(t, 20.8, 1.6), 12)
    if u < 1.65:                                                           # time cut: a quick dissolve sunset -> night
        k = (u - 1.45) / 0.2
        a = lap_frame('ocean', K.light_sunset, t, lap_x(t, 19.35, 1.45), 1)
        big = (a * (1 - k) + big * k).astype(np.uint8)
    return big


def r_laps_b(t, u):
    if u < 1.3:
        return lap_frame('ocean_night', K.light_night, t, lap_x(t, 22.4, 1.3), 30, look=0.6)
    big = lap_frame('ocean', K.light_dawn if hasattr(K, 'light_dawn') else K.light_sunset, t, lap_x(t, 23.7, 1.9), 47, look=0.9)
    big = dawn(big)
    if u < 1.5:
        k = (u - 1.3) / 0.2
        a = lap_frame('ocean_night', K.light_night, t, lap_x(t, 22.4, 1.3), 30)
        big = (a * (1 - k) + big * k).astype(np.uint8)
    return big


def dawn(big):
    """the same sunset world graded to a cooler pink dawn"""
    f = big.astype(np.float32) * np.array((0.96, 0.92, 1.06), np.float32) + np.array((6, 4, 14), np.float32)
    return np.clip(f, 0, 255).astype(np.uint8)


# ================================================================== 9: TWIST — the «FREE PARKING*» ramp, he drives up
TILT = 11.5
TRUCK = (760.0, SIDE_Y)


def r_twist(t, u):
    Z = 1.5
    cx = lerp(520.0, 580.0, glide(u / 2.3))
    v = V('side', cx, 470.0, Z)
    kw, dy = vface(t, (0.9, 0.1), hair_wind=0.4)
    S = WSV * 3 * v.Z
    t_ramp = 26.95
    sign = A(C.sign_free, 482.0, SIDE_Y + 30.0, S * 2.4, t=t, rim=(K.VX.SUN, K.PINK))
    sign.near = 0.97
    rk, rdy = rface(t, (-0.9, 0.0))
    rey = A(C.rey, 640.0, SIDE_Y + 36.0, S * 1.06, t=t, point=True, hand_n=(-6.0, 70.0 + 4 * math.sin(t * 8)), **rk)
    if t < t_ramp:
        xc = lerp(230.0, 470.0, glide((t - 25.58) / (t_ramp - 25.58)))
        acts = K.tow_group(v, *TRUCK, t, tilt=TILT, beacon=True) + K.car_group(v, xc, SIDE_Y + 14, t, vince_kw=kw, speed=8.0) + [rey, sign]
    else:
        cu = lerp(0.04, 0.55, glide((t - t_ramp) / 0.9))
        acts = K.tow_group(v, *TRUCK, t, tilt=TILT, car_u=cu, vince_kw=kw) + [rey, sign]
    def f(big, _):
        sx, sy = v.opt(482.0, SIDE_Y + 30.0 - 28 * WSV * 2.4)
        fx.glow(big, int(sx), int(sy), 260, K.PINK, 0.30 + 0.12 * math.sin(t * 9))
    return K.shot('side', K.light_dusk, cx, 470.0, Z, acts=acts, par=(-8 + 8 * u, 0), fx_=f, t=t, bokeh_=True, dof_k=16)


# ================================================================== 10: LIFT — CLANK, the bed rises with the car on it
def r_lift(t, u):
    Z = 1.15
    v = V('side', 690.0, 430.0, Z)
    kw, dy = vface(t, (-0.5, -0.4), sweat=1.0)
    tilt = TILT * (1 - glide(min(1.0, (u - 0.05) / 0.7)))
    acts = K.tow_group(v, *TRUCK, t, tilt=tilt, car_u=0.55, vince_kw=kw, chains=True)
    def f(big, _):
        if 0.0 < u < 0.4: AT.sparks(big, 420, 1450, t, 27.95, n=16, col=(255, 210, 120), seed=8, life=0.4, speed=600, px=8)
    return K.shot('side', K.light_dusk, 690.0, 430.0, Z, acts=acts, fx_=f, t=t, kick=kick(t, [(27.95, 1.2)]), dof_k=14)


# ================================================================== 11: REY — «Tow and storage. Three-fifty, amigo.»
def r_rey(t, u):
    Z = 1.35
    v = V('side', 640.0, 360.0, Z)
    rk, dy = rface(t, (-0.8, 0.0))
    S = WSV * 3 * v.Z * 2.9
    wx, wy = wpt(v, 560, 2080 + dy * 10)
    rey = A(C.rey, wx, wy, S, t=t, flip=True, hand_n=(18.0, 52.0), hand_f=(-12.0, 34.0), **rk)
    rey.near = 0.99
    def f(big, _):
        if u > 0.6:
            O.draw_sticker(big, ST_350, t, 29.4, 31.0, 820, 520)
    return K.shot('side', K.light_dusk, 640.0, 360.0, Z, acts=[rey], focus=0.99, dof_k=30, fx_=f, t=t, par=(-6 + 6 * u, 0), bokeh_=True)


# ================================================================== 12: SAID — Vince up on the bed: «It SAID free!»
def r_said(t, u):
    Z = 1.3
    v = V('side', 560.0, 330.0, Z)
    kw, dy = vface(t, (-0.9, 0.6), hand_n=(30.0, 76.0))
    wx, wy = car_at_head(v, 520, 940 + dy * 10, 2.4)
    acts = fg(K.car_group(v, wx, wy, t, vince_kw=kw, z=2.4, rot=3.0))
    return K.shot('side', K.light_dusk, 560.0, 330.0, Z, acts=acts, focus=0.98, dof_k=28, t=t, kick=kick(t, [(31.1, 0.6)]), bokeh_=True)


# ================================================================== 13: STAR — the fine print
def r_star(t, u):
    big = K.fine_print(u, t_zoom=0.55)
    AT.juice(big, 1.15, 1.05)
    fx.vignette(big, 0.25)
    return big


# ================================================================== 14: COINS — «FINE! I'll pay in QUARTERS!»
def r_coins(t, u):
    Z = 1.3
    v = V('side', 560.0, 330.0, Z)
    def quarters(sp, h):
        for i in range(5): C.coin(sp, (h[0] - 2.0 + i * 1.3, h[1] - 0.5 + (i % 2) * 1.2))
    kw, dy = vface(t, (0.9, 0.3), hand_n=(26.0, 74.0 + 2 * math.sin(t * 11)), prop_n=quarters)
    wx, wy = car_at_head(v, 430, 1010 + dy * 10, 2.9)
    acts = fg(K.car_group(v, wx, wy, t, vince_kw=kw, z=2.9, rot=2.0))
    return K.shot('side', K.light_dusk, 560.0, 330.0, Z, acts=acts, focus=0.98, dof_k=30, t=t, bokeh_=True)


# ================================================================== 15: TOW APP — Rey's phone: pay-by-app + the convenience fee again
def r_tow_app(t, u):
    Z = 1.35
    v = V('side', 700.0, 360.0, Z)
    rk, dy = rface(t, (0.6, 0.0))
    S = WSV * 3 * v.Z * 2.4
    wx, wy = wpt(v, 300, 1960 + dy * 10)
    rey = A(C.rey, wx, wy, S, t=t, hand_n=(22.0, 60.0), **rk)
    rey.near = 0.99
    def f(big, _):
        ph = K.phone_screen(t, t_fee=37.75, title="Rey'sTow", zone='TOW + STORAGE', rate='$350', unit='PAY BY APP ONLY')
        O.overlay(big, ph, 330, 280 + int(6 * math.sin(t * 3)), 1.0)
        if ST.LOG[0] is not None: ST.log('card', bbox=(520, 300, 520 + ph.shape[1], 300 + ph.shape[0]))
    return K.shot('side', K.light_dusk, 700.0, 360.0, Z, acts=[rey], focus=0.99, dof_k=30, fx_=f, t=t, kick=kick(t, [(37.75, 0.7)]))


# ================================================================== 16: DRIVE — towed down Ocean Drive at sunset
def r_drive(t, u):
    Z = 1.55
    xt = lerp(430.0, 640.0, u / 3.0)
    k = WSV * C.TOW_K
    cxw = xt + C.deck_point(0.55, 0.0)[0] * k
    v = V('ocean', cxw + 20.0, 470.0, Z)
    kw, dy = vface(t, (0.6, -0.2), hair_wind=1.0)
    acts = K.tow_group(v, xt, OCEAN_Y + 20, t, tilt=0.0, car_u=0.55, vince_kw=kw, spin=12.0)
    def f(big, _):
        O.draw_sticker(big, ST_FUND, t, 39.4, 41.7, 540, 560)
    big = K.shot('ocean', K.light_sunset, cxw + 20.0, 470.0, Z, acts=acts, par=(-14 + 10 * u, 0), fx_=f, t=t, dof_k=18,
                 rays=dict(src=(600, 300), a=0.25))
    fx.speed_lines(big, t, 0.2)
    return big


# ================================================================== 17: BUTTON — Fran in the cab's back window: «Coolest guy on a TOW truck, honey.»
def r_button(t, u):
    Z = 1.3
    xt = 700.0 + 8.0 * u
    k = WSV * C.TOW_K * 1.15
    cx = xt + 116.0 * k - 40.0
    cy = OCEAN_Y + 26 - 47.0 * k
    v = V('ocean', cx, cy, Z)
    kw, dy = vface(t, (0.9, 0.0), hair_wind=1.0)
    acts = K.tow_group(v, xt, OCEAN_Y + 26, t, tilt=0.0, car_u=0.55, vince_kw=kw, spin=6.0, z=1.15)
    def f(big, _):
        cab = acts[-1]
        if hasattr(cab, 'last'):
            wx_, wy_ = aout(cab, v, 'window')
            sc = cab.scale(v)
            K.fran(big, int(wx_ - 8.0 * sc), int(wy_ - 13.0 * sc), 62.0 * sc, t, talk=mouth('fran', t), lid=0.6, look=-0.4)
    return K.shot('ocean', K.light_sunset, cx, cy, Z, acts=acts, par=(-10 + 4 * u, 0), fx_=f, t=t, bokeh_=True, dof_k=18)


ST_350 = K.st('$350', fg=(255, 214, 80), size=80)
ST_FUND = K.st('GAME FUND: $70 -> -$280', fg=(90, 236, 255), size=44)
R = [r_hook, r_fran_on, r_meter, r_bonk, r_fran_cu, r_app, r_plan, r_laps_a, r_laps_b, r_twist, r_lift, r_rey, r_said, r_star, r_coins,
     r_tow_app, r_drive, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 1, ['FREE', 'PARKING?'], hook_t=(0.10, 2.6), hook_y=250, hook_size=86,
              stickers=[(K.st('LAP 1', fg=(255, 214, 80), size=56), 19.5, 20.75, 540, 520),
                        (K.st('LAP 12', fg=(90, 236, 255), size=56), 21.0, 22.35, 540, 520),
                        (K.st('LAP 30', fg=(90, 236, 255), size=56), 22.5, 23.65, 540, 520),
                        (K.st('LAP 47', fg=(255, 110, 200), size=64), 23.8, 25.5, 540, 520),
                        (K.st('FREE?!', fg=(255, 110, 200), size=84), 25.65, 27.6, 540, 560)],
              flashes=[TWIST, 27.95, 32.57], mosaics=[19.35],
              cap_y={0: 1500, 1: 1180, 2: 1240, 3: 1180, 4: 520, 5: 1640, 6: 1500, 7: 1200, 8: 1200, 9: 1190, 10: 1200, 11: 1100,
                     12: 1520, 13: 1500, 14: 1520, 15: 1620, 16: 1240, 17: 1480})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
