"""S01E06 «МОРЕ ЗА 200 ТЫСЯЧ?!» (12.10.2026, v2 format; ~31.4 s, twist at 16.2 s / 52 %, type «награду забрал другой»). Season finale.
SELFIE: the travel app — «ТУР НА МОРЕ 200 000 ₽» — «Двести тыщ за море?!» — «Лайфхак последний: море — своими руками!» WIDE (tripod):
the DIY beach on the frozen lake — «Самовар — прорубь. Ёлка — пальма. Лыжи — шезлонг!» (the towel «М. П.» is already on the chair).
TRIPOD CAM: he lounges on the skis, the phone plays sea waves — «Всё включено. Ноль рублей.» A shadow falls. TWIST: the bear in swim
trunks sits down on HIS chair, a stake sign «ОТЕЛЬ «БЕРЛОГА» · ALL INCLUSIVE» thuds into the snow, the whole taiga rolls in with
suitcases. «Это моё море!» — «Было ваше. Теперь — курорт.» Button: the bear hands him a bill — «Девять тысяч. За тепло.» — and the
season loops into the first frames of E01 (he screams at the heating bill in his icy cabin) + «СЕЗОН 2: ИПОТЕКА НА БЕРЛОГУ».
  python3 ep06.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import fx
import overlays as O
import paths as P
import stage as ST
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
from episode import Episode
from props import taigacast as C
from props import taigafauna as F
from props import taigabeach as B
from props import taigakit as K
from props import rusigns as R
from props import decals as D
from props.taigakit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, LOOP_T

EPI = Episode('ep06', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='taiga', lang='ru'))
LAKE = K.world('lake')
W = 3.0                      # lake shore: world px per sprite px
GROUND = 660.0
PX = 575.0                   # Прохор on the shore
HOLE = (768.0, 606.0)        # the ice hole («море»)
SAMOVAR = (722.0, 604.0)
PALM = (505.0, 646.0)
CHAIR = (665.0, 668.0)       # the ski deckchair
BSIGN = (470.0, 656.0)       # «ПЛЯЖ «У ПРОХОРА»»
HSIGN = (560.0, 684.0)       # «ОТЕЛЬ «БЕРЛОГА»» (after the twist)
BEACH = R.plate(56, 26, ['ПЛЯЖ', '«У ПРОХОРА»'], bg=(250, 210, 60), colors=[(30, 30, 40), (180, 30, 30)], border=(60, 50, 40),
                weights=[1.0, 0.8], hand=True, seed=61)
HOTEL = R.plate(96, 36, ['ОТЕЛЬ «БЕРЛОГА»', 'ALL INCLUSIVE'], bg=(60, 40, 120), colors=[(255, 220, 90), (255, 255, 255)],
                border=(255, 220, 90), weights=[1.0, 0.8], bw=1.6)
QUEUE = [('moose', 800.0, 584.0, 0.55, (120, 180, 100)), ('squirrel', 775.0, 592.0, 0.62, (240, 190, 60)),
         ('hare', 748.0, 600.0, 0.66, (80, 140, 220)), ('fox', 728.0, 614.0, 0.72, (220, 80, 60))]


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def post(sp, t=0.0, top=26.0):
    sp.cap((0.0, 0.0), (0.0, top), 1.0, 1.0, C.tones(B.WOOD))
    sp.outline(C.INK, 1)


def steam(big, v, t, k=1.0):
    ox, oy = v.opt(*HOLE)
    for i in range(5):
        ph = (t * 0.5 + i / 5) % 1.0
        K.puff(big, ox + (i - 2) * 30 * v.Z + 40 * ph * v.Z, oy - 200 * ph * v.Z, (30 + 50 * ph) * v.Z, 0.5 * (1 - ph) * k)


def beach(t, Z, chair=True, sign_hotel=False):
    """the DIY beach acts (back to front) + the decal signs"""
    acts = [A(B.ice_hole, HOLE[0], HOLE[1], W * 0.85 * 3 * Z, t=t), A(B.samovar, *SAMOVAR, W * 0.85 * 3 * Z, t=t),
            A(B.palm_fir, *PALM, W * 1.1 * 3 * Z, t=t), A(post, *BSIGN, W * 3 * Z, t=t, top=26.0)]
    if chair: acts.append(A(B.ski_chair, *CHAIR, W * 3 * Z, t=t))
    if sign_hotel: acts.append(A(post, *HSIGN, W * 3 * Z, t=t, top=30.0))
    return acts


def signs_fx(t, hotel_t=None):
    def f(big, v):
        steam(big, v, t, 0.8)
        D.blit(big, v, BEACH, BSIGN[0] - 28.0, BSIGN[1] - 26.0 * W - 13.0)
        if hotel_t is not None and t >= hotel_t:
            drop = 1 - sm((t - hotel_t) / 0.15)
            D.blit(big, v, HOTEL, HSIGN[0] - 48.0, HSIGN[1] - 30.0 * W - 18.0 - 200.0 * drop)
    return f


def bill_prop(sp, h):
    C.bill(sp, h, amount='9 000 ₽')


# ================================================================== 0: SELFIE — the travel app
def r_selfie(t, u):
    m = mouth('prokhor', t)
    hook = t < 2.2
    pan = sm((t - 3.0) / 2.6)
    def f(big, v, a):
        hx, hy = aout(a, v, 'mouth')
        K.breath(big, hx + 30, hy + 10, t, 0.5 + 0.6 * m, scale=1.6, period=1.3)
    big, a = K.cu(C.prokhor, t, LAKE, 380.0 + 360.0 * pan, 470.0, 1.2, 24.0 if hook else 21.0, head=(520, 1240) if hook else (430, 1150),
                  light=K.light_taiga2, blur=2, extra_fx=f, expr='shout' if hook else ('sly' if t < 4.0 else 'grin'),
                  mouth_=max(0.4 if hook else 0.0, m), look=(0.3, 0.2) if hook else (-0.6, 0.0), hand_n=(20.0, 30.0) if hook else (22.0, 34.0))
    big = K.shift(big, *K.handheld(t, 1.2))
    if t < 0.3: K.CK.shake(big, t, 12, 33)
    if t > 2.2: K.blog_frame(big, t)
    K.phone_card(big, t, 0.15, 2.2, ['ТАЙГА-ТУР', 'Море, 7 ночей, всё включено', 'Цена: 200 000 ₽'], icon='Т', icon_col=(30, 140, 200),
                 y=700, colors=[(30, 30, 40), (90, 90, 100), (200, 30, 40)])
    return big


# ================================================================== 1: WIDE (tripod) — the DIY beach
def r_build(t, u):
    Z = 1.0
    pt = 'samovar' if t < 7.6 else ('palm' if t < 9.2 else 'chair')
    hn = {'samovar': (24.0, 40.0), 'palm': (-2.0, 44.0), 'chair': (24.0, 36.0)}[pt]
    a = A(C.prokhor, PX, GROUND, W * 3 * Z, t=t, flip=(pt == 'palm'), expr='proud' if not speaking('prokhor', t) else 'grin',
          mouth_=mouth('prokhor', t), look=(0.8, 0.2), hand_n=hn if pt != 'palm' else (24.0, 44.0))
    tp = A(C.tripod, 778.0, GROUND + 26.0, W * 1.05 * 3 * Z, t=t, flip=True)
    return K.shot(LAKE, K.light_taiga2, 622.0, 480.0, Z, acts=beach(t, Z) + [a, tp], fx_=signs_fx(t), sy=330)


# ================================================================== 2: TRIPOD CAM — «Всё включено. Ноль рублей.»
def r_lounge(t, u):
    Z = 1.55
    shadow = sm((t - 15.2) / 0.8)
    a = A(C.prokhor, CHAIR[0] - 4.0, CHAIR[1] - 14.0, W * 0.9 * 3 * Z, t=t, expr='bliss' if not speaking('prokhor', t) else 'smug',
          mouth_=mouth('prokhor', t), look=(0.6, 0.6), rot=-58, pivot=(0.0, 0.0), hand_n=(22.0, 40.0),
          prop_n=lambda sp, h: C.phone(sp, h, rec=False))
    acts = beach(t, Z, chair=True) + [a]
    big = K.shot(LAKE, K.light_taiga2, CHAIR[0] + 20.0, 520.0, Z, acts=acts, fx_=signs_fx(t), sy=330)
    K.blog_frame(big, t)
    if shadow > 0:                                                                            # something huge blocks the sun
        big[:] = (big * (1 - 0.45 * shadow)).astype(np.uint8)
    return big


# ================================================================== 3: TWIST — the bear in trunks takes his chair, the hotel sign, the queue
def r_resort(t, u):
    Z = 0.95
    sit = sm(u / 0.35)
    acts = beach(t, Z, chair=True, sign_hotel=t >= 16.35)
    for i, (kind, x, y, s, col) in enumerate(QUEUE):                                          # the taiga rolls in with suitcases
        k = sm((u - 0.2 - i * 0.15) / 0.9)
        acts.append(A(F.critter, lerp(x + 200.0, x, k), y, W * s * 1.1 * 3 * Z, t=t, kind=kind, flip=True, expr='grin',
                      walk=t * 9.0 if k < 1 else None, look=(-0.8, 0.0), hand_n=(9.0, 16.0),
                      prop_n=(lambda c: (lambda sp, h: B.suitcase(sp, h, col=c)))(col)))
    acts.append(A(C.potapych, CHAIR[0] - 6.0, lerp(CHAIR[1] - 200.0, CHAIR[1] - 4.0, sit), W * 0.85 * 3 * Z, t=t, expr='boss', trunks=True,
                  mouth_=0.0, look=(-0.8, -0.2), bubble=0.0, snore=False, hand_n=(28.0, 40.0)))
    pa = A(C.prokhor, PX - 85.0, GROUND + 10.0, W * 3 * Z, t=t, expr='shock', mouth_=0.6, look=(0.8, 0.2), hand_n=(18.0, 52.0),
           hand_f=(-12.0, 50.0), rot=-30 * (1 - sm((u - 0.35) / 0.5)), pivot=(0.0, 0.0))
    acts.append(pa)
    big = K.shot(LAKE, K.light_taiga2, 625.0, 480.0, Z, acts=acts, fx_=signs_fx(t, hotel_t=16.35), sy=330)
    if u < 0.5: K.CK.shake(big, t, 14 * (1 - u * 2), 34)
    return big


# ================================================================== 4: «Это моё море!»
def r_mine(t, u):
    big, a = K.cu(C.prokhor, t, LAKE, 560.0, 450.0, 1.3, 22.0, head=(560, 960), light=K.light_taiga2, blur=3,
                  expr='shout', mouth_=mouth('prokhor', t), look=(0.7, 0.0), hand_n=(18.0, 52.0), hand_f=(-10.0, 48.0))
    return big


# ================================================================== 5: the bear on the chair: «Было ваше. Теперь — курорт.» (the fox cannonballs)
def r_bear(t, u):
    def f(big, v, a):
        if t > 23.6:                                                                          # a splash from the ice hole behind
            p = min(1.0, (t - 23.6) / 0.6)
            for i in range(26):
                ang = -math.pi * (0.15 + 0.7 * (i / 25)); r = 380 * p
                x = int(860 + math.cos(ang) * r); y = int(560 + math.sin(ang) * r + 600 * p * p)
                if 0 <= x < OUT_W - 16 and 0 <= y < OUT_H - 16: big[y:y + 16, x:x + 16] = (190, 220, 250)
    big, a = K.cu(C.potapych, t, LAKE, 760.0, 470.0, 1.4, 15.0, head=(430, 860), light=K.light_taiga2, blur=3, extra_fx=f,
                  expr='boss', trunks=True, mouth_=mouth('bear', t, 1.5), look=(0.3, -0.4), bubble=0.0, snore=False, hand_n=(30.0, 30.0))
    return big


# ================================================================== 6: BUTTON — the bill: «Девять тысяч. За тепло.»
def r_bill(t, u):
    Z = 1.4
    give = sm((t - 25.2) / 0.5)
    b = A(C.potapych, CHAIR[0] + 20.0, CHAIR[1] - 4.0, W * 0.85 * 3 * Z, t=t, flip=True, expr='boss', trunks=True, mouth_=mouth('bear', t, 1.5),
          look=(-0.8, -0.2), bubble=0.0, snore=False, hand_n=(lerp(28.0, 40.0, give), lerp(40.0, 34.0, give)),
          prop_n=bill_prop if give < 0.9 else None)
    a = A(C.prokhor, CHAIR[0] - 105.0, GROUND, W * 3 * Z, t=t, expr='shock' if give < 1 else 'frozen', mouth_=0.3, look=(0.8, 0.0),
          hand_n=(20.0, 34.0), prop_n=bill_prop if give >= 0.9 else None, frost=sm((t - 26.6) / 0.9))
    return K.shot(LAKE, K.light_taiga2, CHAIR[0] - 45.0, 500.0, Z, acts=beach(t, Z, chair=True)[:3] + [A(B.ski_chair, *CHAIR, W * 3 * Z, t=t), b, a],
                  fx_=signs_fx(t), sy=330)


# ================================================================== 7: LOOP — the first frames of E01
_LOOP = {}


def r_loop(t, u):
    i = min(66, max(4, int((u + 0.1) * 30) + 1))                                    # hold on E01's hook (its next line is not ours)
    if i not in _LOOP:
        _LOOP.clear()
        _LOOP[i] = np.array(Image.open(pathlib.Path(__file__).resolve().parents[4] / 'build' / 'prokhor-ep06' / 'loop' / f'{i:04d}.png').convert('RGB'))
    big = _LOOP[i].copy()
    if u < 0.12: big[:] = np.clip(big.astype(np.int16) + int(255 * (1 - u / 0.12)), 0, 255).astype(np.uint8)    # white flash into the loop
    return big


R = [r_selfie, r_build, r_lounge, r_resort, r_mine, r_bear, r_bill, r_loop]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 6, ['МОРЕ ЗА', '200 ТЫСЯЧ?!'], hook_t=(0.10, 2.2), hook_y=250,
              stickers=[(K.st('ЛАЙФХАК №6', fg=(255, 214, 80)), 2.3, 4.6, 540, 520),
                        (K.st('ALL INCLUSIVE', fg=(255, 90, 80), size=72), 16.5, 18.6, 540, 300),
                        (K.st('СЕЗОН 2:', fg=(255, 236, 120), size=72), 29.2, DUR, 540, 1440),
                        (K.st('ИПОТЕКА НА БЕРЛОГУ', fg=(255, 120, 90), size=60), 29.3, DUR, 540, 1550)],
              flashes=[TWIST, LOOP_T], mosaics=[],
              cap_y={0: 1720, 1: 1150, 2: 1150, 3: 1150, 4: 1640, 5: 1640, 6: 1790, 7: 1640})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])                                                                # (E01's loop frames carry their own captions)
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
