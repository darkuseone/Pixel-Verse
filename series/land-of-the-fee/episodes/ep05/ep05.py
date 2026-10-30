"""S01E05 «$600 NOSEBLEEDS?!» (34.4 s, twist at 17.55 s / 51 %, type: the hunter asks for help). The season's peak.
HOOK: Duke at his kitchen table screams at TicketMaxed — «SIX HUNDRED?! For NOSEBLEEDS?!» (REX & THE TALONS, «THE SCREAM YOU KNOW»).
Fee-Bee: «You're in the QUEUE! You are number — four MILLION!» — «I'm a BALD EAGLE. I'm on the DOLLAR!» — Sal: «So you're face value.
Nobody PAYS face value.» The cart: SERVICE FEE, FACILITY FEE, CONVENIENCE FEE, FEE FEE — «What's a FEE fee?!» — «It's the fee for the
FEES!» — «Forget it. I'll get in like an EAGLE.» — he flies over the stadium wall. TWIST: on the curb outside sits Rex himself, the
red-tailed hawk whose scream every movie gives to the eagle: «Six hundred. For my OWN show.» — «I've been screaming FOR you for forty
years.» — «Get me in, kid. I'll scream for you.» On stage Rex lets out the legendary scream — the arena roars; Duke joins in — a wimpy
chirp — the arena roars LOUDER. The jumbotron: «Two birds detected! TWO tickets! Plus FEES!» — Sal on the speaker stack: «Majestic.»
Clue in the first half: the event line «THE SCREAM YOU KNOW», Sal's speaker gag from E04.
  python3 ep05.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from props import feepix as FX
from props.dibspix import blit
from props.feekit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, REX_SCREAM, CHIRP

EPI = Episode('ep05', VOICE, DUR, FPS, colors=K.COL, slug=SLUG,
              endcard=dict(style='fee', lang='us', promise='NEXT: $89 TO SIT?! (FINALE)', cy=1470))
APT, STAD, STAGE = K.world('apartment'), K.world('stadium'), K.world('stage')
SCREEN = (447.0, 133.0, 833.0, 320.0)            # the jumbotron in stage.png (world px)


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def V(world_, cx, cy, Z):
    return view_at(world_, cx, cy, Z, 180, 320)


def insert_ui(t, img):
    big = K.dof(K.shot(APT, K.light_apt, 640.0, 330.0, 1.4), 9)
    big[:] = (big * 0.6).astype(np.uint8)
    x0, y0 = (OUT_W - img.shape[1]) // 2, 520
    O.overlay(big, img, x0, y0, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(x0, y0, x0 + img.shape[1], y0 + img.shape[0]))
    return big


# ================================================================== 0: HOOK — at the laptop: «SIX HUNDRED?! For NOSEBLEEDS?!»
def r_hook(t, u):
    dx, dy = K.shake(t, 0.05, 24, 0.9)
    v0 = V(APT, 650.0, 330.0, 1.35)
    lap = A(C.laptop, 688.0, 398.0, 19.0, t=t)
    def fx_(big, v, a):
        hx, hy = aout(a, v, 'head')
        K.feathers(big, t, 0.12, hx, hy - 60, n=14, seed=15)
    big, a = K.cu(C.duke, t, APT, 650.0, 330.0, 1.35, 22.0, head=(400, 880), light=K.light_apt, blur=4, extra_fx=fx_, acts_after=[lap],
                  expr='roar', mouth_=max(0.5, mouth('duke', t, 2.0)), flop=1.0, tremble=0.8, look=(0.9, 0.4), hand_n=(24.0, 34.0))
    tk = K.ticket_ui(t, 'price', price=600 + int(sm(u / 2.2) * 49), w=560, h=760)
    tk = np.array(Image.fromarray(tk).resize((int(tk.shape[1] * 0.78), int(tk.shape[0] * 0.78)), Image.NEAREST))
    O.overlay(big, tk, OUT_W - tk.shape[1] - 20, 1060, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(OUT_W - tk.shape[1] - 20, 1060, OUT_W - 20, 1060 + tk.shape[0]))
    return K.shift(big, dx, dy)


# ================================================================== 1: QUEUE — «You're in the QUEUE! You are number — four MILLION!»
def r_queue(t, u):
    return insert_ui(t, K.ticket_ui(t, 'queue', w=760, h=980))


# ================================================================== 2: DOLLAR — Duke at the window, Sal on the ledge: «So you're face value.»
def r_dollar(t, u):
    k = sm(u / 6.1)
    Z = 1.0 + 0.08 * k
    cx, cy = 820.0 + 10 * k, 362.0
    puff = sm((t - 5.76) / 0.35)
    duke = A(C.duke, 690.0, 698.0, 15.0 * Z, t=t, expr='proud' if t < 8.3 else 'glare', mouth_=mouth('duke', t, 1.8), puff=puff,
             look=(0.8, 0.0), hand_n=(20.0, 30.0))
    sal = A(C.sal, 905.0, 389.0, 13.5 * Z, t=t, expr='dead', mouth_=mouth('sal', t, 2.2), look=(-0.9, -0.2))
    box = A(lambda sp, t=0.0: C.fries_box(sp, t), 966.0, 390.0, 11.0 * Z, t=t)
    return K.shot(APT, K.light_apt, cx, cy, Z, acts=[sal, box, duke])


# ================================================================== 3: CART — the fees pop in: «What's a FEE fee?!» — «It's the fee for the FEES!»
def r_cart(t, u):
    step = 1 + sum(t >= x for x in (12.00, 12.55, 13.10, 13.65))
    return insert_ui(t, K.ticket_ui(t, 'cart', step=step, w=760, h=980))


# ================================================================== 4: WALL — «Forget it. I'll get in like an EAGLE.» (over the stadium wall)
def r_wall(t, u):
    k = u / (CUTS[5] - CUTS[4])
    Z = 1.0
    cx, cy = 600.0 + 120 * sm(k), 360.0
    v = V(STAD, cx, cy, Z)
    ox, oy = lerp(-60, 860, k), lerp(1500, 420, k) + math.sin(t * 7) * 14
    duke = A(C.duke, *wpt(v, ox, oy), 9.0, t=t, expr='glare', mouth_=mouth('duke', t, 1.8), fly=t * 2.6, rot=-30.0, pivot=(0.0, 30.0),
             shades='eyes', look=(1.0, -0.3))
    def fx_(big, v_): K.speed_lines(big, t, 0.5, n=12, seed=9)
    return K.shot(STAD, K.light_mall, cx, cy, Z, acts=[duke], fx_=fx_)


# ================================================================== 5: TWIST — on the curb sits Rex himself: «Six hundred. For my OWN show.»
def r_twist(t, u):
    k = sm(u / 2.5)
    Z = 1.2 + 0.1 * k
    cx, cy = 960.0, 430.0
    v = V(STAD, cx, cy, Z)
    rex = A(C.rex, *wpt(v, 660, 1840), 15.0 * Z / 1.2, t=t, flip=True, expr='sad', mouth_=mouth('rex', t, 1.6), look=(0.4, 0.6),
            hand_n=(14.0, 26.0), hand_f=(-12.0, 26.0))
    return K.shot(STAD, K.light_mall, cx, cy, Z, acts=[rex])


# ================================================================== 6: REX — «I've been screaming FOR you for forty years.» — «Get me in, kid.»
def r_rex(t, u):
    k = sm(u / 5.3)
    Z = 1.1
    cx, cy = 900.0 - 40 * k, 430.0
    v = V(STAD, cx, cy, Z)
    duke = A(C.duke, *wpt(v, 280, 1860), 15.0, t=t, expr='shock' if t < 22.0 else 'stunned', mouth_=0.15, look=(0.9, 0.0),
             hand_n=(18.0, 28.0), hand_f=(-14.0, 28.0))
    rex = A(C.rex, *wpt(v, 800, 1850), 14.0, t=t, flip=True, expr='sad' if t < 23.0 else 'proud', mouth_=mouth('rex', t, 1.6), look=(0.8, 0.0),
            hand_n=(20.0, 40.0) if t >= 23.0 else (14.0, 26.0))
    return K.shot(STAD, K.light_mall, cx, cy, Z, acts=[duke, rex])


# ================================================================== 7: STAGE — Rex's legendary scream; Duke joins in: a chirp; the arena goes wild
def r_stage(t, u):
    Z = 1.0
    cx, cy = 640.0, 380.0
    v = V(STAGE, cx, cy, Z)
    scream = REX_SCREAM <= t < REX_SCREAM + 1.6
    chirp = CHIRP[0] <= t < CHIRP[1]
    rex = A(C.rex, 745.0, 486.0, 9.2, t=t, flip=True, expr='roar' if scream else 'proud', mouth_=1.0 if scream else 0.0, flop=1.0,
            look=(0.3, -0.6), hand_n=(26.0, 60.0) if scream else (18.0, 40.0), tremble=0.8 if scream else 0.0)
    duke = A(C.duke, 545.0, 490.0, 9.6, t=t, expr='stunned' if chirp else ('puff' if t > 26.9 else 'joy'),
             mouth_=(0.45 + 0.35 * abs(math.sin(t * 26))) if chirp else 0.0, puff=1.0 if 26.9 < t < CHIRP[1] else 0.0, look=(0.3, -0.6))
    def fx_(big, v_):
        wild = 1.0 if t > CHIRP[0] + 0.6 else (0.6 if t > REX_SCREAM else 0.25)
        K.crowd(big, t, 1500, n=16, k=wild, seed=5)
        if scream: K.feathers(big, t, REX_SCREAM, 620, 1100, n=10, seed=17, cols=((176, 112, 70), (116, 72, 44)))
    big = K.shot(STAGE, K.light_store, cx, cy, Z, acts=[duke, rex], fx_=fx_, vig=0.3)
    dx, dy = K.shake(t, REX_SCREAM, 22, 1.2)
    if CHIRP[0] + 0.7 <= t: dx, dy = K.shake(t, CHIRP[0] + 0.7, 18, 1.0)
    return K.shift(big, dx, dy)


# ================================================================== 8: JUMBO — the jumbotron Fee-Bee: «Two birds detected! TWO tickets! Plus FEES!»
def jumbo_ui(t, talk, w=772, h=374):
    a = np.zeros((h, w, 3), np.uint8); a[:] = (20, 30, 60)
    for y in range(0, h, 6): a[y] = (24, 36, 70)
    sp = FX.draw(lambda s_: C.feebee_face(s_, 0.0, 40.0, 30.0, t, talk), 4.0)
    blit(a, sp, w // 2, h + 20, 4.0)
    return a


def r_jumbo(t, u):
    Z = 1.0
    cx, cy = 640.0, 330.0
    v = V(STAGE, cx, cy, Z)
    rex = A(C.rex, 745.0, 486.0, 9.2, t=t, flip=True, expr='stunned', look=(0.0, 0.9))
    duke = A(C.duke, 545.0, 490.0, 9.6, t=t, expr='shock' if t > 31.8 else 'stunned', look=(0.0, 0.9))
    def pre(big, v_):                                                     # the jumbotron is part of the set: behind the birds
        x0, y0 = v_.opt(SCREEN[0] + 10, SCREEN[1] + 10); x1, y1 = v_.opt(SCREEN[2] - 10, SCREEN[3] - 10)
        img = jumbo_ui(t, mouth('feebee', t, 1.5), int(x1 - x0), int(y1 - y0))
        X0, Y0 = int(max(0, x0)), int(max(0, y0)); X1, Y1 = int(min(OUT_W, x1)), int(min(OUT_H, y1))
        if X1 > X0 and Y1 > Y0: big[Y0:Y1, X0:X1] = img[Y0 - int(y0):Y1 - int(y0), X0 - int(x0):X1 - int(x0)]
    def fx_(big, v_):
        K.crowd(big, t, 1500, n=16, k=0.7, seed=5)
        if t >= 31.80: K.dollars(big, t, 31.80, 540, 700, n=12, seed=19)
    return K.shot(STAGE, K.light_store, cx, cy, Z, acts=[duke, rex], fx_=fx_, pre=pre, vig=0.3)


# ================================================================== 9: BUTTON — Sal on the speaker stack, to camera: «Majestic.»
def r_button(t, u):
    big, a = K.cu(C.sal, t, STAGE, 185.0, 260.0, 1.3, 30.0, head=(560, 860), light=K.light_store, blur=5,
                  expr='dead', mouth_=mouth('sal', t, 2.2), look=(-0.2, -0.6), bob=t < 32.3)
    return big


R = [r_hook, r_queue, r_dollar, r_cart, r_wall, r_twist, r_rex, r_stage, r_jumbo, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SEND = K.st_lines(['SEND THIS TO SOMEONE', 'WHO PAID FEES FOR FEES'], size=38, colors=[(255, 255, 255), (130, 255, 200)])
VIRAL = K.st_lines(['EAGLE SOUNDS LIKE A DOLPHIN', '4.1M VIEWS'], size=36, colors=[(255, 255, 255), (255, 214, 80)])
CHOICE = K.st_lines(['WHO SCREAMS BETTER?', 'A) DUKE  B) REX'], size=42, colors=[(255, 214, 80), (130, 255, 200)])
SHOW = K.Show(EPI, 5, ['$600 NOSEBLEEDS?!'], hook_t=(0.08, 2.00), hook_y=330, hook_size=54,
              stickers=[(K.st('FEE FEE?!', fg=(255, 90, 110), size=72), 13.70, 15.00, 540, 330),
                        (K.st('REX?!', fg=(255, 214, 80), size=70), 17.58, 19.80, 205, 330),
                        (SEND, 25.90, 28.40, 540, 340),
                        (VIRAL, 29.20, 31.70, 540, 1080),
                        (CHOICE, 32.40, DUR, 540, 390)],
              flashes=[TWIST, REX_SCREAM, CHIRP[0] + 0.7], mosaics=[CUTS[4], CUTS[7]],
              cap_y={0: 600, 1: 450, 2: 1420, 3: 450, 4: 1420, 5: 1420, 6: 1420, 7: 1180, 8: 1420, 9: 620})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
