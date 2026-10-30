"""S01E03 «$40 FOR A HUG?!» (30.8 s, twist at 17.42 s / 57 %, type: bureaucratic recursion).
HOOK: Duke in a hospital gown and a neck brace screams at the itemised ER bill — «FORTY bucks?! For a HUG?!» (SKIN-TO-SKIN CONTACT $39.99).
FLASHBACK: Duke flies majestically — SMACK into the mirror glass of Panorama Tower. The nurse hugs him «there, there» — the printer prints
+$39.99. «I'm a BALD EAGLE. I'm on the DOLLAR!» — Sal on the vitals monitor: «Dollar don't cover THIS.» (the whiteboard: ICE PACK $180,
TISSUE (USED) $12). The insurer's Fee-Bee: «Sounds like you said — PRE-EXISTING! Doctor's note, please!» — «Doc! A NOTE!» — Dr. Chuck:
«I need your INSURANCE approval first.» TWIST: a split screen — DOCTOR | INSURANCE — the same tired face; the wide shot: one Chuck in one
chair between two desks, a phone at each ear: «Doctor says YES.» — «Insurance says NO.» — «So who do I CALL?» — «Me.» Duke faints, the
nurse catches him in a hug (+$39.99) — Sal to camera: «Don't hug her BACK. That's double.»
Clue in the first half: the same coffee stain on Chuck's tie; the diploma «CHUCK, CLAIMS DEPT.» comes with the reveal.
  python3 ep03.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, SMACK

EPI = Episode('ep03', VOICE, DUR, FPS, colors=K.COL, slug=SLUG,
              endcard=dict(style='fee', lang='us', promise='NEXT: $400 A MONTH?!', cy=1470))
ER, TOWER, BILL = K.world('er'), K.world('tower'), K.world('billing')
MON = (462.0, 172.0)             # Sal's perch: the top of the vitals monitor
BILL_LINES = ['SKIN-TO-SKIN CONTACT $39.99', 'ICE PACK $180', 'ASPIRIN (1) $45', 'TISSUE (USED) $12']


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def V(world_, cx, cy, Z):
    return view_at(world_, cx, cy, Z, 180, 320)


def light_er(v, g=0.0):
    return K.light_store(v, g)


def duke_kw(t, **kw):
    d = dict(gown=True, brace=True, shades='head')
    d.update(kw)
    return d


# ================================================================== 0: HOOK — CU in the ER: «FORTY bucks?! For a HUG?!» + the bill
def r_hook(t, u):
    dx, dy = K.shake(t, 0.05, 24, 0.9)
    def fx_(big, v, a):
        hx, hy = aout(a, v, 'head')
        K.feathers(big, t, 0.12, hx, hy - 60, n=14, seed=7)
    big, a = K.cu(C.duke, t, ER, 400.0, 330.0, 1.35, 20.0, head=(470, 700), light=light_er, blur=4, extra_fx=fx_,
                  **duke_kw(t, expr='roar', mouth_=max(0.5, mouth('duke', t, 2.0)), flop=1.0, tremble=0.8, look=(0.6, 0.9),
                            hand_n=(22.0, 30.0), hand_f=(-16.0, 30.0)))
    b = K.bill_ui(BILL_LINES, total='TOTAL $4,276.99', hi=0, w=780)
    k = sm(u / 0.25)
    y0 = int(lerp(OUT_H, 1130, k))
    O.overlay(big, b, (OUT_W - b.shape[1]) // 2, y0, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=((OUT_W - b.shape[1]) // 2, y0, (OUT_W + b.shape[1]) // 2, y0 + b.shape[0]))
    return K.shift(big, dx, dy)


# ================================================================== 1: FLASHBACK — Duke flies majestically into Panorama Tower: SMACK
def r_flash(t, u):
    Z = 1.0
    cx, cy = 700.0, 330.0
    v = V(TOWER, cx, cy, Z)
    s = 9.0
    acts = []
    if t < SMACK:
        k = (t - CUTS[1]) / (SMACK - CUTS[1])
        ox, oy = lerp(-80, 700, k), lerp(1200, 900, k) + math.sin(t * 7) * 14
        acts.append(A(C.duke, *wpt(v, ox, oy), s, t=t, expr='proud', fly=t * 2.6, rot=-38.0, pivot=(0.0, 30.0), shades='eyes', look=(1.0, 0.0)))
    else:
        k = sm((t - SMACK) / 0.5)
        ox, oy = 700, 900 + 260 * k
        acts.append(A(C.duke, *wpt(v, ox, oy), s * 1.05, t=t, expr='stunned', mouth_=0.3, flop=1.0, rot=12.0 * (1 - k), legs=False,
                      shades='eyes', look=(0.0, 0.0), hand_n=(18.0, 58.0), hand_f=(-14.0, 58.0)))
    def fx_(big, v):
        if t < SMACK: K.speed_lines(big, t, 0.6, n=14, seed=8)
        K.crack(big, t, SMACK, 820, 560, r=260)
        K.feathers(big, t, SMACK, 800, 600, n=18, seed=9)
    big = K.shot(TOWER, K.light_mall, cx, cy, Z, acts=acts, fx_=fx_)
    dx, dy = K.shake(t, SMACK, 30, 0.45)
    return K.shift(big, dx, dy)


# ================================================================== 2: HUG — the nurse hugs Duke; the printer prints +$39.99
def r_hug(t, u):
    Z = 1.0
    cx, cy = 330.0, 330.0
    duke = A(C.duke, 300.0, 668.0, 6.3 * 3 * Z, t=t, **duke_kw(t, expr='sad', look=(-0.8, 0.0), hand_n=(18.0, 30.0), hand_f=(-14.0, 30.0)))
    nurse = A(C.nurse, 214.0, 664.0, 8.5 * 3 * Z, t=t, expr='sweet', hug=1.0, look=(0.9, 0.0))
    return K.shot(ER, light_er, cx, cy, Z, acts=[duke, nurse])


# ================================================================== 3: DOLLAR — «I'm a BALD EAGLE…» — Sal on the monitor: «Dollar don't cover THIS.» (pan to the board)
def r_dollar(t, u):
    k = sm((t - 8.10) / 1.6)
    Z = 1.0
    cx, cy = lerp(380.0, 880.0, k), 330.0
    puff = sm((t - 5.32) / 0.35)
    duke = A(C.duke, 300.0, 668.0, 6.3 * 3 * Z, t=t, **duke_kw(t, expr='proud', mouth_=mouth('duke', t, 1.8), puff=puff, look=(0.2, -0.3),
                                                               hand_n=(20.0, 30.0), hand_f=(-15.0, 30.0)))
    sal = A(C.sal, MON[0], MON[1], 3.2 * 3 * Z, t=t, expr='dead', mouth_=mouth('sal', t, 2.2), look=(-0.6, -0.3))
    return K.shot(ER, light_er, cx, cy, Z, acts=[sal, duke])


# ================================================================== 4: PHONE — the insurer's Fee-Bee: «PRE-EXISTING! Doctor's note, please!»
def r_phone(t, u):
    big = K.dof(K.shot(ER, light_er, 400.0, 330.0, 1.3), 9)
    big[:] = (big * 0.62).astype(np.uint8)
    t_st = 12.80
    scr = K.screen_ui(t, mouth('feebee', t, 1.6), 'UNITED WE BILL', stamp='PRE-EXISTING: FLYING' if t >= t_st else None,
                      stamp_k=sm((t - t_st) / 0.12), w=700, h=1060, sub='INSURANCE AI • POWERED BY FEE-BEE')
    x0, y0 = (OUT_W - scr.shape[1]) // 2, 600
    O.overlay(big, scr, x0, y0, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(x0, y0, x0 + scr.shape[1], y0 + scr.shape[0]))
    return big


# ================================================================== 5: DOC — «Doc! A NOTE!» — Dr. Chuck: «I need your INSURANCE approval first.»
def r_doc(t, u):
    k = sm(u / 3.7)
    Z = 1.04 + 0.05 * k
    cx, cy = 450.0, 350.0
    duke = A(C.duke, 320.0, 668.0, 6.3 * 3 * Z, t=t, **duke_kw(t, expr='roar' if t < 15.1 else 'plead', mouth_=mouth('duke', t, 2.0),
                                                               look=(0.9, 0.2), flop=0.8 if t < 15.1 else 0.0, hand_n=(24.0, 44.0)))
    doc = A(C.chuck, 580.0, 664.0, 8.3 * 3 * Z, t=t, flip=True, mode='doctor', expr='dead', mouth_=mouth('chuck', t, 1.6), look=(0.8, 0.2))
    return K.shot(ER, light_er, cx, cy, Z, acts=[doc, duke])


# ================================================================== 6: TWIST — split: DOCTOR | INSURANCE — the same tired face
def r_twist(t, u):
    l_, a = K.cu(C.chuck, t, BILL, 240.0, 380.0, 1.3, 26.0, head=(540, 860), light=K.light_store, blur=5, mode='doctor', flip=False,
                 expr='dead', mouth_=mouth('chuck', t, 1.6), look=(0.6, 0.0), phone_=True, hand_n=(8.6, 50.0))
    r_, b = K.cu(C.chuck, t, BILL, 900.0, 380.0, 1.3, 26.0, head=(540, 860), light=K.light_store, blur=5, mode='insurer', flip=True,
                 expr='dead', mouth_=0.0, look=(0.6, 0.0))
    big = K.split(l_, r_)
    K.label(big, 'DOCTOR', 270, 520, bg=(30, 60, 120))
    K.label(big, 'INSURANCE', 810, 520, bg=(170, 30, 50))
    return big


# ================================================================== 7: WIDE — one Chuck, one chair, two desks, a phone at each ear
def r_wide(t, u):
    Z = 0.34
    cx, cy = 600.0, 400.0
    v = V(BILL, cx, cy, Z)
    right = t >= 19.35
    ch = A(C.chuck, 688.0 + (8.0 if right else 0.0), 712.0, 8.3 * 3 * Z, t=t, flip=not right, mode='doctor', headset=True,
           expr='dead', mouth_=mouth('chuck', t, 1.6), look=(0.8, 0.0), phone_=True, phone_f=True, hand_n=(8.6, 50.0), hand_f=(-5.6, 50.0))
    big = K.shot(BILL, K.light_store, cx, cy, Z, acts=[ch], vig=0.0)
    y_top = int(v.opt(0, 0)[1]); y_bot = int(v.opt(0, 720)[1])
    big[:max(0, y_top)] = (16, 20, 36); big[min(OUT_H, y_bot):] = (16, 20, 36)
    K.label(big, 'DOCTOR', int(v.opt(200, 0)[0]), y_top + 60, bg=(30, 60, 120), size=28)
    K.label(big, 'INSURANCE', int(v.opt(920, 0)[0]), y_top + 60, bg=(170, 30, 50), size=28)
    return big


# ================================================================== 8: CALL — CU Duke, broken: «So who do I CALL?»
def r_call(t, u):
    big, a = K.cu(C.duke, t, ER, 400.0, 330.0, 1.35, 20.0 + 1.4 * sm(u / 2.1), head=(500, 860), light=light_er, blur=4,
                  **duke_kw(t, expr='sad', mouth_=mouth('duke', t, 1.6), look=(0.6, 0.2), hand_n=(16.0, 26.0), sweat=1.0))
    return big


# ================================================================== 9: ME — CU Chuck with both phones: «Me.»
def r_me(t, u):
    big, a = K.cu(C.chuck, t, BILL, 680.0, 380.0, 1.3, 24.0, head=(540, 820), light=K.light_store, blur=5, mode='doctor', headset=True,
                  expr='dead', mouth_=mouth('chuck', t, 1.6), look=(0.0, -0.2), phone_=True, phone_f=True, hand_n=(8.6, 50.0), hand_f=(-5.6, 50.0))
    return big


# ================================================================== 10: FAINT — Duke faints; the nurse catches him in a hug (+$39.99)
def r_faint(t, u):
    Z = 1.0
    cx, cy = 330.0, 330.0
    f = sm((t - 24.40) / 0.35)
    duke = A(C.duke, 300.0 - 30 * f, 668.0, 6.3 * 3 * Z, t=t, rot=26.0 * f, pivot=(0.0, 0.0),
             **duke_kw(t, expr='blank' if f > 0.5 else 'stunned', look=(0.0, 0.6), hand_n=(18.0, 40.0), hand_f=(-16.0, 46.0), legs=True))
    nurse = A(C.nurse, 196.0, 664.0, 8.5 * 3 * Z, t=t, expr='sweet' if t > 24.8 else 'warm', hug=1.0 if t > 24.6 else 0.0,
              mouth_=mouth('nurse', t, 1.6), look=(0.9, 0.0))
    return K.shot(ER, light_er, cx, cy, Z, acts=[nurse, duke])


# ================================================================== 11: BUTTON — Sal on the monitor, to camera: «Don't hug her BACK. That's double.»
def r_button(t, u):
    big, a = K.cu(C.sal, t, ER, MON[0], 210.0, 1.35, 30.0, head=(560, 860), light=light_er, blur=4,
                  expr='dead', mouth_=mouth('sal', t, 2.2), look=(-0.2, -0.6), bob=t < 27.2)
    return big


R = [r_hook, r_flash, r_hug, r_dollar, r_phone, r_doc, r_twist, r_wide, r_call, r_me, r_faint, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SEND = K.st_lines(['SEND THIS TO SOMEONE', 'DOING OPEN ENROLLMENT'], size=38, colors=[(255, 255, 255), (130, 255, 200)])
CHOICE = K.st_lines(['WORST LINE ON THE BILL?', 'A) HUG  B) USED TISSUE'], size=38, colors=[(255, 214, 80), (130, 255, 200)])
SHOW = K.Show(EPI, 3, ['$40 FOR A HUG?!'], hook_t=(0.08, 2.00), hook_y=330, hook_size=66,
              stickers=[(K.st('BIRD vs WINDOW: 0-1', fg=(255, 214, 80), size=50), SMACK + 0.05, CUTS[2], 540, 330),
                        (K.st('+$39.99', fg=(130, 255, 160), size=72), 4.70, 5.25, 700, 600),
                        (K.st('SAME GUY?!', fg=(255, 214, 80), size=72), 17.45, 19.60, 540, 330),
                        (K.st('+$39.99', fg=(130, 255, 160), size=72), 26.62, 27.05, 700, 600),
                        (SEND, 24.45, 26.50, 540, 340),
                        (CHOICE, 28.80, 30.8, 540, 390)],
              flashes=[SMACK, TWIST], mosaics=[CUTS[1], CUTS[2]],
              cap_y={0: 1050, 1: 1420, 2: 1420, 3: 1420, 4: 470, 5: 1450, 6: 1500, 7: 1420, 8: 1420, 9: 1420, 10: 1420, 11: 560})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
