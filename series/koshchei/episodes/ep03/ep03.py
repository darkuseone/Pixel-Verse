"""S01E03 «РЕМОНТ В 7 УТРА?!» (19.10.2026; 30.0 s, twist at 16.45 s / 55 %).
HOOK: Кощей asleep in his coffin on two stools; a drill bit bursts out of the ceiling two centimetres from his nose, plaster rains:
«В семь утра?! Я только лёг!» DOOR: up one floor — Змей Горыныч in three hard hats with three drills: «Тишина — с двадцати трёх. А сейчас —
день.» — «Я — Кощей Бессмертный!» — head 3: «А я — трёхголовый. И что?» REVENGE (23:01): green fire, chains, the bulb pops — «У-у-у-у!
Спокойной ночи, соседушка.» — the three heads hide under three blankets. TWIST (success is worse than failure): the doorbell — Галина
Аркадьевна with a folder «УК ТРИДЕВЯТОЕ ЦАРСТВО»: «Шум после двадцати трёх. Штраф.» — «Вы ж — в Соцфонде!» — «По совместительству.» —
«А он — сверлит!» — «Он — днём. По закону.» (plaster on her perm, she does not blink). Кузьмич: «Жуть.» LOOP: morning, he lies down,
the drill bit comes out of the ceiling again (= first frame).
  python3 ep03.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import fx
import overlays as O
import stage as ST
from stage import OUT_W, OUT_H
from scene import sm, lerp
from episode import Episode
from props import koshcast as C
from props import koshkit as K
from props import decals as D
from props import rusigns as R
from props.koshkit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

COL = dict(K.COL, gorynych2=K.COL['gorynych'], gorynych3=K.COL['gorynych'])
EPI = Episode('ep03', VOICE, DUR, FPS, colors=COL, slug=SLUG, endcard=dict(style='kosh', lang='ru'))
FLAT = K.world('flat')
STAIRS = K.world('stairs')
CAL = K.calendar(4)
WP = 5.0                         # flat
WS = 5.4                         # stairs
FL_S = 606.0                     # stairs floor
CX, CY = 700.0, 690.0            # coffin centre on the flat floor
BILL = R.plate(40, 50, ['ШТРАФ', '500 ₽'], bg=(244, 240, 226), fg=(30, 28, 30), border=(34, 70, 130), bw=1.0, colors=[(190, 30, 34), (30, 28, 30)])


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def flat_cal(big, v):
    D.blit(big, v, CAL, 1146.0, 250.0)


def coffin_acts(t, Z, expr='normal', m=0.0, jump=0.0, look=(0.0, 0.6), sink=0.0):
    """the coffin on two stools; Кощей bolt upright in it (classic vampire rise), drawn BEHIND the coffin's front so only his upper
    body shows above the rim; sink 0..1 lowers him back into it"""
    cf = A(C.coffin, CX, CY, WP * 1.65 * 3 * Z, flip=True, t=t, jump=jump, lid=1.0)
    k = A(C.koshchei, CX - 6 * WP, CY - (10.0 - 40.0 * sink) * WP, WP * 3 * Z, t=t, expr=expr, mouth_=m, look=look,
          hand_n=(16.0, 50.0), hand_f=(-12.0, 50.0))
    return cf, k


def drill_bit(big, x, y_tip, t, k=1.0):
    """a drill bit spinning down out of the ceiling to (x, y_tip) output px + falling plaster"""
    if k <= 0: return
    y_tip = int(y_tip)
    big[0:y_tip, int(x) - 22:int(x) + 22] = (150, 156, 166)
    for yy in range(0, y_tip, 24):
        o = ((yy // 24 + int(t * 30)) % 2) * 10
        big[yy:yy + 12, int(x) - 22 + o:int(x) - 6 + o] = (90, 96, 106)
    big[y_tip - 10:y_tip + 10, int(x) - 8:int(x) + 8] = (210, 214, 222)
    rng = np.random.default_rng(int(t * 24))
    for i in range(14):
        px = x + (rng.random() - 0.5) * 220; py = (t * 900 + i * 137) % max(1, y_tip + 200)
        q = 10 + int(rng.random() * 12)
        if 0 <= py < OUT_H - q and 0 <= px < OUT_W - q: big[int(py):int(py) + q, int(px):int(px) + q] = (226, 220, 206)


# ================================================================== 0: HOOK — the drill bit at his nose
def r_hook(t, u, loop=False):
    Z = 2.0
    m = mouth('koshchei', t)
    awake = loop and t < 29.25
    cf, k = coffin_acts(t, Z, expr='content' if awake else 'scream', m=0.0 if awake else max(0.4, m),
                        jump=0.0 if awake else 1.0, look=(0.0, 1.0), sink=(0.55 * sm((t - 28.4) / 0.6) if awake else 0.0))
    bit_k = 0.0 if awake else 1.0
    def f(big, v):
        flat_cal(big, v)
        hx, hy = aout(k, v, 'head')
        drill_bit(big, hx + 90, hy - 230 + (0 if not loop else 300 * (1 - sm((t - 29.25) / 0.2))), t, bit_k)
    big = K.shot(FLAT, K.light_flat, CX - 2 * WP, CY - 64.0 * WP, Z, acts=[k, cf], fx_=f, sy=330)
    if bit_k: K.CK.shake(big, t, 8, 40)
    return big


# ================================================================== 1: DOOR — Горыныч in three hard hats, three drills
def gor(t, Z, x=830.0, **kw):
    spin = t * 9
    return A(C.gorynych, x, FL_S, WS * 1.15 * 3 * Z, flip=True, t=t, hats=True, drills=[0.2 + 0.1 * math.sin(spin), -0.1, -0.3],
             mouths=(0.0, mouth('gorynych2', t), mouth('gorynych3', t)), looks=[(0.8, 0.0)] * 3, **kw)


def r_door(t, u):
    Z = 1.0
    run = sm(u / 0.9)
    k = A(C.koshchei, lerp(160.0, 520.0, run), FL_S, WS * 3 * Z, t=t, expr='angry', mouth_=0.0, look=(0.8, 0.0),
          walk=t * 12 if run < 1 else None, hand_n=(12.0, 30.0))
    g = gor(t, Z, exprs=('deadpan', 'smug' if speaking('gorynych2', t) else 'deadpan', 'deadpan'))
    return K.shot(STAIRS, K.light_stairs, 620.0, 410.0, Z, acts=[g, k], sy=330)


# ================================================================== 2: HAUGHTY — «Я — Кощей Бессмертный!»
def r_haughty(t, u):
    big, a = K.cu(C.koshchei, t, STAIRS, 560.0, 330.0, 1.3, 20.0, head=(480, 900), light=K.light_stairs, blur=2,
                  expr='shout' if speaking('koshchei', t) else 'proud', mouth_=mouth('koshchei', t), look=(0.6, 0.0),
                  hand_n=(22.0, 54.0), fire=0.6)
    return big


# ================================================================== 3: HEADS — «А я — трёхголовый. И что?»
def r_heads(t, u):
    big, a = K.cu(C.gorynych, t, STAIRS, 760.0, 330.0, 1.3, 16.0, head=(600, 1000), light=K.light_stairs, blur=2, flip=True, hats=True,
                  drills=[0.2, 0.0, -0.2], mouths=(0.0, 0.0, mouth('gorynych3', t)), exprs=('deadpan', 'deadpan', 'smug'),
                  looks=[(0.8, 0.0)] * 3)
    return big


# ================================================================== 4: REVENGE — 23:01: green fire, chains, the bulb pops
def r_revenge(t, u):
    Z = 1.25
    fire = sm(u / 0.3)
    k = A(C.koshchei, 560.0, FL_S, WS * 3 * Z, t=t, expr='sinister' if not speaking('koshchei', t) else 'scream', mouth_=mouth('koshchei', t),
          look=(0.4, 0.0), hand_n=(22.0, 56.0), hand_f=(-18.0, 56.0), fire=fire)
    pop = t > 13.35
    def f(big, v):
        ha = aout(k, v, 'hand_n'); hf = aout(k, v, 'hand_f')
        K.green_fire(big, ha[0], ha[1], t, r=110, k=fire, seed=5); K.green_fire(big, hf[0], hf[1], t, r=110, k=fire, seed=6)
        if pop: K.darken(big, 0.55)
        hx, hy = aout(k, v, 'head')
        if pop: K.eyes_glow(big, [(hx + 10, hy - 20), (hx + 70, hy - 16)], k=0.8, r=18)
    big = K.shot(STAIRS, K.light_stairs if not pop else K.light_dark, 600.0, 360.0, Z, acts=[k], fx_=f, sy=330)
    if 13.3 < t < 13.5: O.flash(big, 0.6)
    return big


# ================================================================== 5: DUVETS — three heads under three blankets
def r_duvets(t, u):
    hide = sm(u / 0.6)
    big, a = K.cu(C.gorynych, t, FLAT, 640.0, 330.0, 1.2, 15.0, head=(560, 1050), light=lambda v: K.light_dark(v, 0.25), blur=2,
                  duvet=hide, exprs=('panic', 'panic', 'panic'), mouths=(0.5, 0.6, 0.5), looks=[(0.0, 0.6)] * 3)
    K.darken(big, 0.25)
    return big


# ================================================================== 6: TWIST — the doorbell: Галина from the УК with a fine
def galina_at(t, Z, x=430.0, **kw):
    return A(C.galina, x, FL_S, WS * 1.15 * 3 * Z, flip=True, t=t, expr='deadpan' if not speaking('galina', t) else 'normal',
             mouth_=mouth('galina', t), look=(0.8, 0.0), **kw)


def folder(sp, h):
    x, y = h
    m = sp.m_poly([(x - 1.0, y - 3.0), (x + 9.0, y - 3.0), (x + 9.0, y + 9.0), (x - 1.0, y + 9.0)])
    sp.paint(m, [(30, 50, 100), (40, 70, 130), (70, 100, 170)], None, olc=(20, 20, 40))
    sp.txt_box(['УК', 'ТРИДЕВЯТОЕ', 'ЦАРСТВО'], (x - 0.4, y - 2.4, x + 8.4, y + 8.4), (240, 230, 200), pad=0.2)


def r_doorbell(t, u):
    Z = 1.35
    k = A(C.koshchei, 230.0, FL_S, WS * 3 * Z, t=t, expr='stunned', mouth_=mouth('koshchei', t), look=(0.8, 0.0), hand_n=(10.0, 30.0))
    g = galina_at(t, Z, prop_f=folder, hand_f=(-4.0, 20.0), hand_n=(10.0, 26.0),
                  prop_n=(lambda sp, h: None))
    def f(big, v):
        if t > 18.2:
            ga = aout(g, v, 'hand_n')
            pop = min(1.0, (t - 18.2) / 0.15)
            img = BILL
            D.blit(big, v, img, wpt(v, ga[0] - 60, ga[1] - 120)[0], wpt(v, ga[0] - 60, ga[1] - 120)[1], k=pop)
    return K.shot(STAIRS, K.light_stairs, 330.0, 360.0, Z, acts=[k, g], fx_=f, sy=330)


# ================================================================== 7: FAKE — «Вы ж — в Соцфонде!» — «По совместительству.»
def r_fake(t, u):
    Z = 1.55
    k = A(C.koshchei, 250.0, FL_S, WS * 3 * Z, t=t, expr='shout' if speaking('koshchei', t) else 'stunned', mouth_=mouth('koshchei', t),
          look=(0.8, 0.0), hand_n=(22.0, 50.0) if speaking('koshchei', t) else (10.0, 30.0))
    g = galina_at(t, Z, x=420.0, prop_f=folder, hand_f=(-4.0, 20.0))
    return K.shot(STAIRS, K.light_stairs, 330.0, 380.0, Z, acts=[k, g], sy=330)


# ================================================================== 8: LAW — «А он — сверлит!» — «Он — днём. По закону.» + plaster
def r_law(t, u):
    Z = 1.35
    k = A(C.koshchei, 240.0, FL_S, WS * 3 * Z, t=t, expr='shout' if speaking('koshchei', t) else 'sad', mouth_=mouth('koshchei', t),
          look=(0.2, 0.9), hand_n=(14.0, 70.0) if t < 25.1 else (10.0, 30.0))
    g = galina_at(t, Z, x=430.0, prop_f=folder, hand_f=(-4.0, 20.0))
    def f(big, v):
        if t > 26.0:
            hx, hy = aout(g, v, 'head')
            rng = np.random.default_rng(int(t * 20))
            for i in range(26):
                ph = ((t - 26.0) * 1.6 + i * 0.07) % 1.0
                px = hx - 160 + rng.random() * 320; py = hy - 500 + ph * 560
                q = 12 + int(rng.random() * 14)
                big[int(py):int(py) + q, int(px):int(px) + q] = (226, 220, 206)
    return K.shot(STAIRS, K.light_stairs, 340.0, 360.0, Z, acts=[k, g], fx_=f, sy=330)


# ================================================================== 9: Кузьмич in his box (ears covered): «Жуть.»
def r_zhut(t, u):
    def pre(big, v):
        x0, y0 = v.opt(430.0, 150.0); x1, y1 = v.opt(512.0, 262.0)
        big[int(y0):int(y1), int(x0):int(x1)] = (24, 22, 22)
    big, a = K.cu(C.domovoy, t, STAIRS, 470.0, 190.0, 4.4, 30.0, head=(560, 1010), light=K.light_stairs, pre_fx=pre,
                  expr='zhut', mouth_=mouth('kuzmich', t, 2.0), look=(0.0, -0.1), glow=(int(t * 3) % 2) * 1.0)
    return big


def r_loop(t, u):
    return r_hook(t, u, loop=True)


R_ = [r_hook, r_door, r_haughty, r_heads, r_revenge, r_duvets, r_doorbell, r_fake, r_law, r_zhut, r_loop]
assert len(R_) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 3, ['РЕМОНТ', 'В 7 УТРА?!'], hook_t=(0.10, 2.70), hook_y=230,
              stickers=[(K.st('7:00', fg=(255, 220, 110), size=84), 0.3, 2.6, 860, 1180),
                        (K.st('23:01', fg=(120, 255, 150), size=84), 11.9, 13.2, 540, 560),
                        (K.st('ШТРАФ', fg=(255, 90, 80), size=90), 16.6, 18.2, 540, 520),
                        (K.st('ПО СОВМЕСТИТЕЛЬСТВУ', fg=(200, 190, 255), size=52), 21.5, 22.8, 540, 560)],
              flashes=[TWIST], mosaics=[],
              cap_y={0: 1640, 1: 1640, 2: 1640, 3: 1580, 4: 1640, 5: 1600, 6: 1640, 7: 1640, 8: 1640, 9: 1520, 10: 1640})


def render(t):
    i = max(0, min(len(R_) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R_[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
