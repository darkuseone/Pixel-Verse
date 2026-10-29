"""S01E01 «REPRESENTATIVE!» (pilot; 31.0 s, twist at 17.70 s / 57 %, type: the reward is the same problem).
HOOK: Duke, a bald eagle in an 80s track jacket, screams into his phone at the kitchen table — «REPRESENTATIVE!!» The XFEENITY support
AI Fee-Bee: «Sounds like you said — UPGRADE! Done!» (+$20/mo). Duke puffs his chest: «I'm a BALD EAGLE. I'm on the DOLLAR!» — Sal
the pigeon on the window ledge: «Not on YOURS.» (a moth flies out of Duke's wallet). Duke flies to the XFEENITY store: «Fine. I'm talking
to a HUMAN.» The kiosk: «HUMAN! NOW!» — «Sounds like you said — HUMMUS!» (a cup of hummus drops out). The EMPLOYEES ONLY door bursts
open in holy light — Doris: «Hi, hon! I'm a REAL human!» TWIST: «That's nineteen ninety-nine a MINUTE.» (a taxi meter on her belly) —
«For WHAT?!» — «Eye contact's EXTRA, hon.» — «Forget it! I'll take the ROBOT!» — the kiosk: «Sounds like you said — HUMAN!» (ka-ching)
— Duke inhales for the mighty eagle scream -> a wimpy real bald-eagle chirp. Sal, on his head, to camera: «Majestic.»
Clue in the first half: the store window «*HUMANS AVAILABLE (FEES APPLY)», the wall screen «NO HUMANS! (YAY!)».
  python3 ep01.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, CHIRP

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG,
              endcard=dict(style='fee', lang='us', promise='NEXT: $95 TO APPLY?!'))
APT, MALL, STORE = K.world('apartment'), K.world('mall'), K.world('store')


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def V(world_, cx, cy, Z):
    return view_at(world_, cx, cy, Z, 180, 320)


def W(v, ox, oy):
    return wpt(v, ox, oy)


def rot_pt(x, y, deg):
    a = math.radians(deg); return x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a)


def meter_at(t):
    return '$59.97' if t >= 27.40 else ('$39.98' if t >= 22.95 else ('$19.99' if t >= 17.72 else '$0.00'))


# ================================================================== 0: HOOK — CU, screaming into the phone at the kitchen table
def r_hook(t, u):
    m = mouth('duke', t, 2.0)
    dx, dy = K.shake(t, 0.05, 26, 0.9)
    def fx_(big, v, a):
        hx, hy = aout(a, v, 'head')
        K.feathers(big, t, 0.12, hx, hy - 60, n=16, seed=4)
    big, a = K.cu(C.duke, t, APT, 650.0, 330.0, 1.35, 24.0, head=(430, 900), light=K.light_apt, blur=4, extra_fx=fx_,
                  expr='roar', mouth_=max(0.6, m), flop=1.0, tremble=0.8, look=(0.9, -0.5), hand_n=(21.0, 47.0),
                  prop_n=lambda sp, h: C.phone(sp, h, t, 0.0))
    return K.shift(big, dx, dy)


# ================================================================== 1: PHONE — Fee-Bee: «Sounds like you said — UPGRADE! Done!»
def r_phone(t, u):
    v = V(APT, 640.0, 330.0, 1.4)
    big = K.dof(K.shot(APT, K.light_apt, 640.0, 330.0, 1.4), 9)
    big[:] = (big * 0.62).astype(np.uint8)
    k = sm((t - 3.20) / 0.12)
    scr = K.screen_ui(t, mouth('feebee', t, 1.6), 'XFEENITY SUPPORT', stamp='UPGRADED! +$20/MO' if t >= 3.2 else None, stamp_k=k,
                      w=700, h=1060)
    z = 1.0 + 0.04 * u
    if z != 1.0:
        from PIL import Image
        scr = np.array(Image.fromarray(scr).resize((int(scr.shape[1] * z), int(scr.shape[0] * z)), Image.NEAREST))
    x0, y0 = (OUT_W - scr.shape[1]) // 2, 600 - int((z - 1) * 300)
    O.overlay(big, scr, x0, y0, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(x0, y0, x0 + scr.shape[1], y0 + scr.shape[0]))
    if t >= 3.22: K.dollars(big, t, 3.22, OUT_W // 2, y0 + scr.shape[0] - 160, n=8, seed=2)
    return big


# ================================================================== 2: PROUD — «I'm a BALD EAGLE. I'm on the DOLLAR!» (dolly in)
def r_proud(t, u):
    k = sm(u / 2.6)
    Z = 0.96 + 0.16 * k
    cx, cy = 560.0 - 20 * k, 372.0 + 8 * k
    m = mouth('duke', t, 1.8)
    puff = sm((t - 3.95) / 0.35)
    duke = A(C.duke, 512.0, 690.0, 15.0 * Z, t=t, expr='proud', mouth_=m, puff=puff, look=(0.2, -0.3),
             hand_n=(20.0, 30.0) if t < 5.4 else (8.0, 44.0), hand_f=(-15.0, 30.0))
    def fx_(big, v):
        if t < 4.9:
            hx, hy = v.opt(512.0 + 2.0 * 5.0, 690.0 - 34 * 5.0)
            K.feathers(big, t, 3.98, hx, hy, n=8, seed=7, spread=320, cols=((98, 62, 38), (246, 244, 236)))
    return K.shot(APT, K.light_apt, cx, cy, Z, acts=[duke], fx_=fx_)


# ================================================================== 3: SAL — on the window ledge: «Not on YOURS.» + a moth from the wallet
def r_sal(t, u):
    k = sm(u / 2.0)
    Z = 1.0 + 0.08 * k
    cx, cy = 820.0 + 10 * k, 362.0
    v = V(APT, cx, cy, Z)
    op = sm((t - 7.95) / 0.2)
    duke = A(C.duke, 690.0, 698.0, 15.0 * Z, t=t, expr='glare' if t < 8.0 else 'stunned', mouth_=0.0, look=(0.8, 0.2),
             hand_n=(21.0, 38.0) if t > 7.7 else (16.0, 26.0), prop_n=lambda sp, h: C.wallet(sp, h, op))
    sal = A(C.sal, 905.0, 389.0, 13.5 * Z, t=t, expr='dead', mouth_=mouth('sal', t, 2.2), look=(-0.9, -0.2))
    box = A(lambda sp, t=0.0: C.fries_box(sp, t), 966.0, 390.0, 11.0 * Z, t=t)
    def fx_(big, v):
        if t >= 8.15:
            hx, hy = aout(duke, v, 'hand')
            K.moth(big, t, 8.15, hx, hy - 120, q=9)
    return K.shot(APT, K.light_apt, cx, cy, Z, acts=[sal, box, duke], fx_=fx_)


# ================================================================== 4: FLY — crossing over the strip mall to XFEENITY, Sal riding
def r_fly(t, u):
    k = u / (CUTS[5] - CUTS[4])
    Z = 1.0
    cx, cy = 560.0 + 210 * sm(k), 360.0
    v = V(MALL, cx, cy, Z)
    ox, oy = lerp(-60, 760, k), lerp(980, 820, k) + math.sin(t * 7.0) * 18
    s = 8.5
    rot = -38.0
    wx, wy = W(v, ox, oy)
    duke = A(C.duke, wx, wy, s, t=t, expr='glare', mouth_=mouth('duke', t, 1.8), fly=t * 2.6, look=(1.0, 0.0), rot=rot, pivot=(0.0, 30.0),
             shades='eyes')
    bx, by = rot_pt(-9.0, 47.0 - 30.0, rot)
    sx_, sy_ = ox + bx * s, oy - (by + 30.0) * s
    sal = A(C.sal, *W(v, sx_ - 10, sy_ + 30), s * 0.9, t=t, expr='dead', look=(1.0, 0.2), bob=False, rot=-12.0)
    def fx_(big, v):
        K.speed_lines(big, t, 0.6, n=14, seed=4)
    return K.shot(MALL, K.light_mall, cx, cy, Z, acts=[duke, sal], fx_=fx_)


# ================================================================== 5: KIOSK — «HUMAN! NOW!» — «Sounds like you said — HUMMUS!»
KIO = (705.0, 640.0)


def kiosk_act(t, s, chute=0.0, at=KIO):
    return A(C.kiosk, at[0], at[1], s, t=t, talk=mouth('feebee', t, 1.5), chute=chute)


def r_kiosk(t, u):
    k = sm(u / 3.5)
    Z = 1.25 + 0.08 * k
    cx, cy = 770.0 - 6 * k, 430.0
    v = V(STORE, cx, cy, Z)
    s = 9.6 * Z
    walk = (t - 11.15) * 9.0 if t < 11.55 else None
    dx_ = 885.0 - 60.0 * sm((t - 11.15) / 0.40)
    duke = A(C.duke, dx_, 650.0, s * 1.05, t=t, flip=True, expr='roar' if t < 12.6 else 'glare', mouth_=mouth('duke', t, 2.0),
             walk=walk, look=(0.9, -0.4), flop=0.7 if t < 12.6 else 0.0, hand_n=(22.0, 46.0) if t < 12.6 else (17.0, 26.0))
    acts = [kiosk_act(t, s, chute=sm((t - 14.15) / 0.1) * (1 - sm((t - 14.6) / 0.2)))]
    if t >= 14.15:
        h0 = 15.0 * s / (3 * Z)
        fy = min(1.0, (t - 14.15) / 0.3)
        hx_, hy_ = KIO[0] + 14.0, KIO[1] - h0 * (1 - fy * fy) - 2.0
        acts.append(A(C.hummus, hx_, hy_, s * 1.1, t=t, rot=40.0 * (1 - fy)))
    acts.append(duke)
    return K.shot(STORE, K.light_store, cx, cy, Z, acts=acts)


# ================================================================== 6: DOOR — EMPLOYEES ONLY bursts open, holy light: «Hi, hon! I'm a REAL human!»
DOOR = (1060.0, 409.0)


def r_door(t, u):
    k = sm(u / 2.9)
    Z = 1.12 + 0.08 * k
    cx, cy = 1000.0, 400.0
    v = V(STORE, cx, cy, Z)
    op = sm((t - 14.70) / 0.18)
    glow = sm((t - 14.72) / 0.3)
    dw = A(C.door, DOOR[0], DOOR[1], 11.0 * Z, t=t, open_=op, glow=glow)
    w_ = sm((t - 15.0) / 1.2)
    doris = A(C.doris, DOOR[0] - 6.0 * w_, DOOR[1] + 40.0 * w_, (8.4 + 2.0 * w_) * Z, t=t, expr='joy' if t < 16.2 else 'warm',
              mouth_=mouth('doris', t, 1.6), look=(-0.7, 0.0), meter='$0.00', wave=t if t > 15.6 else None)
    duke = A(C.duke, 895.0, 702.0, 16.0 * Z, t=t, expr='shock' if t < 15.4 else 'cry', mouth_=0.35 if t < 15.4 else 0.15, look=(1.0, 0.4),
             hand_f=(-14.0, 40.0), hand_n=(18.0, 52.0))
    def fx_(big, v):
        ox, oy = v.opt(DOOR[0], DOOR[1] - 30.0)
        K.holy_light(big, t, 14.72, ox, oy, k=glow * 0.6, w0=240, w1=1100)
    acts = [dw] + ([doris] if t >= 14.9 else []) + [duke]
    big = K.shot(STORE, lambda v: K.light_store(v, glow), cx, cy, Z, acts=acts, fx_=fx_)
    dx, dy = K.shake(t, 14.70, 22, 0.35)
    return K.shift(big, dx, dy)


# ================================================================== 7: TWIST — CU Doris + the taxi meter: «That's nineteen ninety-nine a MINUTE.»
def r_twist(t, u):
    def fx_(big, v, a):
        if t >= 17.72:
            mx, my = aout(a, v, 'meter')
            K.dollars(big, t, 17.72, mx, my - 40, n=10, seed=9)
    big, a = K.cu(C.doris, t, STORE, 1000.0, 380.0, 1.3, 29.0 + 2.0 * sm(u / 2.4), head=(560, 700), light=lambda v: K.light_store(v, 0.6),
                  blur=5, extra_fx=fx_, expr='warm', mouth_=mouth('doris', t, 1.6), look=(-0.3, -0.2), meter=meter_at(t))
    return big


# ================================================================== 8: WHAT — two-shot: «For WHAT?!» — «Eye contact's EXTRA, hon.» (+$19.99)
def r_what(t, u):
    Z = 1.15
    cx, cy = 950.0, 420.0
    v = V(STORE, cx, cy, Z)
    duke = A(C.duke, 852.0, 694.0, 14.0 * Z / 1.15, t=t, expr='roar' if t < 21.1 else 'shock', mouth_=mouth('duke', t, 2.0), flop=0.8 if t < 21.1 else 0.2,
             look=(0.9, 0.3), hand_n=(24.0, 40.0) if t < 21.1 else (18.0, 30.0), tremble=0.6 if t < 21.1 else 0.0)
    doris = A(C.doris, 1012.0, 602.0, 11.0, t=t, flip=True, expr='warm', mouth_=mouth('doris', t, 1.6), look=(0.8, 0.3), meter=meter_at(t))
    def fx_(big, v):
        if t >= 22.95:
            mx, my = aout(doris, v, 'meter')
            K.dollars(big, t, 22.95, mx, my - 30, n=8, seed=12)
    big = K.shot(STORE, lambda v: K.light_store(v, 0.5), cx, cy, Z, acts=[doris, duke], fx_=fx_)
    dx, dy = K.shake(t, 20.16, 16, 0.4)
    return K.shift(big, dx, dy)


# ================================================================== 9: RUN — «Forget it! I'll take the ROBOT!» (dash back to the kiosk)
def r_run(t, u):
    k = u / (CUTS[10] - CUTS[9])
    Z = 1.12
    cx, cy = 880.0 - 170.0 * sm(k), 420.0
    dxw = 930.0 - 250.0 * k
    duke = A(C.duke, dxw, 690.0, 14.5, t=t, flip=True, expr='panic', mouth_=mouth('duke', t, 2.0), walk=t * 14.0, lean=0.35,
             look=(1.0, 0.0), flop=1.0, hand_n=(26.0, 50.0), hand_f=(-20.0, 46.0), sweat=1.0)
    def fx_(big, v):
        K.speed_lines(big, t, 0.5, n=12, seed=6)
    return K.shot(STORE, lambda v: K.light_store(v, 0.3), cx, cy, Z, acts=[kiosk_act(t, 10.8 * Z / 1.25), duke], fx_=fx_)


# ================================================================== 10: KIOSK 2 — «Sounds like you said — HUMAN!» (ka-ching, $59.97)
def r_kiosk2(t, u):
    k = sm(u / 2.1)
    Z = 1.45 + 0.08 * k
    cx, cy = 680.0, 470.0
    s = 11.0 * Z
    duke = A(C.duke, 770.0, 692.0, s * 1.05, t=t, flip=True, expr='plead' if t < 27.4 else 'shock', mouth_=0.1, look=(0.9, -0.3),
             hand_n=(20.0, 40.0), hand_f=(-12.0, 46.0))
    def fx_(big, v):
        if t >= 27.40:
            ox, oy = v.opt(KIO[0], KIO[1] - 160.0)
            K.dollars(big, t, 27.40, ox, oy, n=12, seed=14)
    return K.shot(STORE, K.light_store, cx, cy, Z, acts=[kiosk_act(t, s, at=(630.0, 670.0)), duke], fx_=fx_)


# ================================================================== 11: BUTTON — the mighty scream = a wimpy chirp. Sal (on his head): «Majestic.»
def r_button(t, u):
    inh = sm((t - 27.60) / 0.45) * (1 - sm((t - CHIRP[1]) / 0.3))
    chirp = CHIRP[0] <= t < CHIRP[1]
    m = (0.45 + 0.35 * abs(math.sin(t * 26.0))) if chirp else (0.0 if t < CHIRP[0] else 0.05)
    expr = 'puff' if t < CHIRP[0] else ('stunned' if chirp else 'sad')
    sal_box = {}
    def after(big, v, a):
        hx, hy = aout(a, v, 'head')
        sp = K.FX.draw(C.sal, 13.0, t=t, expr='dead', mouth_=mouth('sal', t, 2.2), look=(-0.2, -0.6), bob=t < 29.3)
        K.blit(big, sp, hx - 40, hy - 9.6 * 17.0, 13.0, K.light_store(v))
        if t >= CHIRP[0] and t < CHIRP[0] + 1.6:
            K.feathers(big, t, CHIRP[0], hx + 140, hy + 40, n=6, seed=21, spread=220)
    big, a = K.cu(C.duke, t, STORE, 700.0, 430.0, 1.3, 17.0 + 1.2 * inh, head=(470, 1080), light=K.light_store, blur=4, extra_fx=after,
                  expr=expr, mouth_=m, puff=inh, flop=0.0 if t < CHIRP[1] else 0.0, look=(0.9, -0.6) if chirp else (0.3, 0.2),
                  hand_n=(16.0, 26.0), shades='head')
    return big


R = [r_hook, r_phone, r_proud, r_sal, r_fly, r_kiosk, r_door, r_twist, r_what, r_run, r_kiosk2, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SEND = K.st_lines(['SEND THIS TO SOMEONE', 'WHO YELLS AT BOTS'], size=40, colors=[(255, 255, 255), (130, 255, 200)])
CHOICE = K.st_lines(["WHO'S WORSE?", 'A) BOT  B) $19.99 HUMAN'], size=40, colors=[(255, 214, 80), (130, 255, 200)])
SHOW = K.Show(EPI, 1, ['REPRESENTATIVE!!'], hook_t=(0.08, 1.90), hook_y=330, hook_size=58,
              stickers=[(K.st('HUMMUS?!', fg=(255, 214, 80), size=60), 14.40, 14.70, 300, 760),
                        (K.st('HUMAN FEE $19.99/MIN', fg=(255, 214, 80), size=48), 17.72, 20.05, 540, 300),
                        (K.st('+$19.99', fg=(130, 255, 160), size=60), 22.95, 23.40, 700, 760),
                        (SEND, 23.50, 25.45, 540, 340),
                        (K.st('$59.97', fg=(255, 90, 90), size=72), 27.42, 27.55, 760, 700),
                        (CHOICE, 28.95, 31.0, 540, 1450)],
              flashes=[14.72, TWIST], mosaics=[CUTS[4]],
              cap_y={0: 1420, 1: 470, 2: 1300, 3: 1420, 4: 1420, 5: 1400, 6: 1420, 7: 470, 8: 640, 9: 1420, 10: 1450, 11: 560})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
