"""S01E01 «ЗАДЕРЖИСЬ НА 5 МИНУТ!» (pilot; 33.6 s, twist at 17.95 s / 53 %, type: the reward is the same problem).
Main question (opened at 0 s, closed at ~60 %): why did the boss keep Эдик «for five minutes»?
HOOK: 17:59, Эдик in his coat and hat at the light switch; the boss (already in HIS coat — the clue) at his door: «Эдик, задержись на
пять минут!» — «Конечно! Я же ключевой сотрудник!» — Фикус Аркадий on the windowsill: «Ключевой. От туалета.» (the WC key on the
lanyard). «Пять минут с шефом — это повышение! Кабинет с окном!» (the empty «СОТРУДНИК ГОДА — ?» frame). Clock 18:05 -> 19:40, Эдик asleep
on the keyboard: «Полтора часа. С сентября перерабатывать можно двести сорок часов в год.» TWIST: the door bursts open, the boss leaves:
«Эдик, свет выключи и фикус полей. Ты же у нас ключевой!» — throws the caretaker's bunch «ЗАВХОЗ». «Повысили… до завхоза.» —
«Поздравляю. Теперь ты уходишь последним.» Night, one lamp: Эдик waters the ficus from his mug — «Чаем не поливать!» — «Пять минут у
начальника — это до утра.» LOOP: 08:00, the boss at the door: «Эдик! Задержись на пять минут!»
  python3 ep01.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import fx
import overlays as O
import stage as ST
from stage import OUT_W, OUT_H
from scene import sm, lerp
from cam25 import glide, kick
from episode import Episode
from props import kscast as C
from props import kskit as K
from props import kspix as KX
from props import mimic as M
from props.kskit import at, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, T0

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='ks', lang='ru', promise='ЗАВТРА: ГДЕ ПРЕМИЯ?'),
              promo='ru')
TAB = (C.XTRA, C.EXPR)
FE = M.Face([(0.0, 'hopeful'), (1.95, 'beam'), (3.4, 'proud'), (4.8, 'proud'), (8.3, 'scheme'), (9.6, 'beam'), (10.4, 'hopeful'),
             (12.45, 'hopeful'), (13.6, 'sleepy'), (17.95, 'shock'), (19.8, 'shock'), (20.6, 'panic'), (21.7, 'crushed'), (25.6, 'crushed'),
             (27.1, 'pleading'), (28.0, 'shock'), (31.3, 'sleepy'), (32.4, 'beam')], TAB, seed=3)
FF = M.Face([(0.0, 'deadpan'), (6.4, 'smirk'), (8.3, 'deadpan'), (16.0, 'deadpan'), (24.05, 'smirk'), (27.1, 'shock'), (27.6, 'angry'),
             (28.68, 'deadpan')], TAB, seed=8)
FS = M.Face([(0.0, 'boss'), (17.95, 'bark'), (19.0, 'boss'), (31.3, 'boss')], TAB, seed=5)
WS_SILL = 2.9                       # the ficus on the windowsill (window wall depth)
SILL = (1040.0, 372.0)


def mouth(who, t):
    return M.mouth(EPI.talk, who, t)


def ekw(t, base=(0.7, 0.0), **kw):
    m = mouth('edik', t)
    return dict(expr=FE.speak(t, m), mouth_=m, blink=FE.blink(t), look=FE.look(t, base), t=t, **kw)


def fkw(t, base=(0.0, 0.0), **kw):
    m = mouth('fikus', t)
    return dict(expr=FF.speak(t, m), mouth_=m, blink=FF.blink(t), look=FF.look(t, base, amp=0.2), t=t, **kw)


def skw(t, base=(0.7, 0.0), **kw):
    m = mouth('shef', t)
    return dict(expr=FS.speak(t, m), mouth_=m, blink=FS.blink(t), look=FS.look(t, base), t=t, **kw)


def floor_actor(fn, wx, wy, Z, **kw):
    return K.A(fn, wx, wy, K.ws_at(wy) * 3 * Z, **kw)


def fikus_sill(Z, t, **kw):
    return K.A(C.fikus, SILL[0], SILL[1], WS_SILL * 3 * Z, **fkw(t, **kw))


def door_open(big, v, k=1.0):
    """the boss's door swung open: a dark doorway + the door leaf against the wall"""
    x0, y0 = v.opt(60.0, 172.0); x1, y1 = v.opt(206.0, 506.0)
    xa, xb = int(max(0, x0)), int(min(OUT_W, x1)); ya, yb = int(max(0, y0)), int(min(OUT_H, y1))
    if xa >= xb or ya >= yb: return
    reg = big[ya:yb, xa:xb].astype(np.float32)
    big[ya:yb, xa:xb] = (reg * (1 - 0.85 * k) + np.array((24, 20, 26)) * 0.85 * k).astype(np.uint8)
    yy = np.linspace(0, 1, yb - ya)[:, None]
    glow = (np.clip(1 - yy * 1.4, 0, 1) * 70 * k)[..., None]
    big[ya:yb, xa:xb] = np.clip(big[ya:yb, xa:xb] + glow * np.array((1.0, 0.8, 0.5)), 0, 255).astype(np.uint8)


def cap(big, x, y, text, size=46, fg=(255, 255, 255)):
    img = O.sticker(text, fg=fg, size=size)
    O.overlay(big, img, int(x - img.shape[1] / 2), int(y - img.shape[0] / 2), 1.0)


# ================================================================== 0: HOOK — 17:59, Эдик in coat + hat, the boss at his door
def r_hook(t, u, name='office', clock='17:59', loop=False):
    Z = 1.0 + 0.03 * u
    cx, cy = 236.0, 236.0
    v = K.V(name, cx, cy, Z)
    sh = at(C.shef, v, 250, 1760, 11.0, **skw(t, (0.9, 0.0), coat=True, hand_n=(26.0, 66.0) if t < 1.6 or loop else None,
                                                    prop_f=lambda sp, h: C.briefcase(sp, h)))
    if not loop:
        ed = at(C.edik, v, 790, 1240, 26.0, flip=True, pin='head', near=0.99,
                **ekw(t, (0.9, 0.1), coat=True, hat=True, hand_f=(-12.0, 56.0) if t < 1.0 else None))
    else:
        ed = at(C.edik, v, 790, 1240, 26.0, flip=True, pin='head', near=0.99,
                **ekw(t, (0.9, 0.1), stubble_=1.0, hand_n=(16.0, 40.0), prop_n=lambda sp, h: C.keyring(sp, h, tag=True)))
    return K.shot(name, cx, cy, Z, acts=[sh, ed], par=(-6 + 8 * u, 0), t=t, dof_k=22, clock=clock)


# ================================================================== 1: «Конечно! Я же ключевой сотрудник!» — hat off, beaming
def r_hat(t, u):
    Z = 1.22 + 0.04 * u
    cx, cy = 430.0, 370.0
    v = K.V('office', cx, cy, Z)
    off = t > 2.55
    hn = (14.0, 78.0) if 2.2 < t < 2.9 else ((22.0, 52.0) if t > 3.3 else None)
    ed = at(C.edik, v, 560, 1990, 18.5, near=0.99, **ekw(t, (0.2, 0.1), coat=True, hat=not off, hand_n=hn,
                                                          key_swing=0.5 * math.sin(t * 6)))
    return K.shot('office', cx, cy, Z, acts=[ed], par=(-10 + 14 * u, 0), t=t, dof_k=26)


# ================================================================== 2/12/15: FIKUS close-up on the windowsill
def r_fik(t, u, name='office', expr_base=(0.0, 0.0), stick=None):
    Z = 1.35 + 0.05 * u
    cx, cy = 1020.0, 250.0
    v = K.V(name, cx, cy, Z)
    fk = at(C.fikus, v, 540, 900, 22.0, pin='head', near=0.99, **fkw(t, expr_base))
    big = K.shot(name, cx, cy, Z, acts=[fk], par=(-4 + 8 * u, 0), t=t, dof_k=30)
    return big


# ================================================================== 3: INSERT — the WC key on the lanyard
def r_key(t, u):
    Z = 1.3
    cx, cy = 430.0, 380.0
    v = K.V('office', cx, cy, Z)
    ed = at(C.edik, v, 540 + 20 * math.sin(t * 3), 1000, 44.0, pin='wc', near=0.99,
            **ekw(t, coat=True, key_swing=0.55 * math.sin((t - 6.4) * 5.5) * math.exp(-(t - 6.4) * 0.4)))
    return K.shot('office', cx, cy, Z, acts=[ed], par=(4 * u, 0), t=t, dof_k=34)


# ================================================================== 4: whisper to camera, rubbing hands
def r_whisper(t, u):
    Z = 1.3
    cx, cy = 560.0, 360.0
    v = K.V('office', cx, cy, Z)
    rub = math.sin(t * 16) * 1.6
    ed = at(C.edik, v, 540, 860, 34.0, pin='head', near=0.99,
            **ekw(t, (0.0, 0.0), hand_n=(9.0 + rub, 41.0), hand_f=(-2.0 - rub, 42.0), sweat=0.0))
    big = K.shot('office', cx, cy, Z, acts=[ed], par=(-6 + 10 * u, 0), t=t, dof_k=36)
    return big


# ================================================================== 5: the empty «СОТРУДНИК ГОДА — ?» frame — the dream
def r_board(t, u):
    Z = 1.55 + 0.35 * glide(u / 2.0)
    cx, cy = 600.0, 240.0
    v = K.V('office', cx, cy, Z)
    ed = at(C.edik, v, 210, 1330, 30.0, pin='head', near=0.99, **ekw(t, (0.9, 0.5)))
    def f(big, v_):
        fx_, fy_ = v_.opt(617.0, 236.0)
        for i in range(4): M.sparkle(big, fx_ + 140 * math.cos(t * 2 + i * 1.6), fy_ + 160 * math.sin(t * 2.4 + i * 1.6), t + i, px=8)
    return K.shot('office', cx, cy, Z, acts=[ed], par=(8 - 12 * u, 0), t=t, dof_k=24, fx_=f)


# ================================================================== 6: CLOCK — 18:05 -> 19:40
def r_clock(t, u):
    k = glide(u / 1.15)
    mins = int(lerp(18 * 60 + 5, 19 * 60 + 40, k))
    big = K.clock_insert(t, f'{mins // 60:02d}:{mins % 60:02d}')
    cap(big, 540, 1560, f'{mins // 60:02d}:{mins % 60:02d}', size=88, fg=(255, 232, 110))
    return big


# ================================================================== 7: 19:40 — asleep on the keyboard
def r_sleep(t, u):
    Z = 1.55 + 0.05 * u
    cx, cy = 560.0, 400.0
    v = K.V('office_night', cx, cy, Z)
    ed = at(C.edik, v, 640, 1010, 25.0, pin='head', near=0.99, legs=False,
            **ekw(t, (0.6, -0.8), hand_n=(16.0, 34.0), hand_f=(8.0, 34.0)))
    def f(big, v_):
        hx, hy = v_.opt(470.0, 300.0)
        for i in range(3):
            k = ((t * 0.8 + i / 3) % 1.0)
            cap(big, hx + 60 * i + 40 * k, hy - 120 * k - 40 * i, 'z', size=40 + 14 * i, fg=(200, 220, 255))
        mx, my = v_.opt(505.0, 372.0)
        n = int(((t - 13.6) * 9) % 14) + 1
        cap(big, mx, my, 'Ж' * min(n, 7), size=30, fg=(140, 255, 160))
    return K.shot('office_night', cx, cy, Z, acts=[ed], par=(-6 + 8 * u, 0), t=t, dof_k=20, fx_=f, clock='19:40')


# ================================================================== 9: TWIST — the door bursts open, the boss leaves in his coat
def r_twist(t, u):
    Z = 1.0
    cx, cy = 300.0, 360.0
    v = K.V('office_night', cx, cy, Z)
    w = glide(u / 1.8)
    sh = floor_actor(C.shef, lerp(132.0, 250.0, w), 514.0 + 10 * w, Z, **skw(t, (0.9, 0.2), coat=True, walk=t * 8.0 if u < 1.8 else None,
                                                                            prop_f=lambda sp, h: C.briefcase(sp, h)))
    ed = at(C.edik, v, 820, 980 - 60 * sm(u / 0.3), 25.0, flip=True, pin='head', near=0.99,
            **ekw(t, (0.9, 0.0), tie_up=4.0 * math.exp(-u * 3)))
    def pre(big, v_): door_open(big, v_, min(1.0, u / 0.12))
    def f(big, v_):
        hx, hy = aout(ed, v, 'head') if hasattr(ed, 'last') else (820, 980)
        if u < 1.2: M.shock(big, hx + 60, hy - 200, 70, px=8, k=1.0 - u / 1.2)
    big = K.shot('office_night', cx, cy, Z, acts=[sh, ed], par=(-4, 0), t=t, dof_k=18, fx_=f, clock='19:42',
                 kick=kick(t, [(TWIST, 1.0)]), pre=pre)
    return big


def r_twist_door(t, u):
    big = r_twist(t, u)
    return big


# ================================================================== 10: THROW — the bunch «ЗАВХОЗ» flies, Эдик catches it and sags
def keys_actor(wx, wy, s, swing=0.0, tag=True):
    return K.A(lambda sp, **kw: C.keyring(sp, (0.0, 12.0), swing=swing, tag=tag), wx, wy, s)


def r_throw(t, u):
    Z = 1.2
    cx, cy = 330.0, 390.0
    v = K.V('office_night', cx, cy, Z)
    t_hit = 20.55
    sh = floor_actor(C.shef, 220.0, 520.0, Z, flip=False,
                     **skw(t, (0.9, 0.0), coat=True, hand_n=(24.0, 70.0) if t < 20.1 else (30.0, 50.0), prop_f=lambda sp, h: C.briefcase(sp, h)))
    caught = t >= t_hit
    sag = (6.0 * math.exp(-(t - t_hit) * 3.0) * math.cos((t - t_hit) * 14) + 4.0) if caught else 0.0
    ed = floor_actor(C.edik, 440.0, 530.0, Z, flip=True, oy=-sag,
                     **ekw(t, (-0.9, 0.3), hand_n=(18.0, 44.0) if not caught else (16.0, 30.0 - sag),
                           prop_n=(lambda sp, h: C.keyring(sp, h, tag=True)) if caught else None))
    acts = [sh, ed]
    if not caught:
        k = (t - 19.8) / (t_hit - 19.8)
        if k > 0.25:
            kk = (k - 0.25) / 0.75
            x = lerp(300.0, 405.0, kk); y = lerp(330.0, 380.0, kk) - 90 * math.sin(math.pi * kk)
            acts.append(keys_actor(x, y, K.ws_at(520.0) * 3 * Z * 1.2, swing=t * 9))
    return K.shot('office_night', cx, cy, Z, acts=acts, par=(-4 + 6 * u, 0), t=t, dof_k=18, clock='19:42',
                  kick=kick(t, [(t_hit, 0.8)]))


# ================================================================== 11: «Повысили… до завхоза.»
def r_zavhoz(t, u):
    Z = 1.3
    cx, cy = 420.0, 380.0
    v = K.V('office_night', cx, cy, Z)
    ed = at(C.edik, v, 540, 700, 28.0, pin='head', near=0.99,
            **ekw(t, (0.3, -0.4), hand_n=(15.0, 50.0), prop_n=lambda sp, h: C.keyring(sp, h, tag=True, swing=0.1 * math.sin(t * 2))))
    return K.shot('office_night', cx, cy, Z, acts=[ed], par=(4 - 6 * u, 0), t=t, dof_k=30, clock='19:43')


# ================================================================== 13: WIDE — the dark office, one lamp, Эдик walks to the ficus
def r_wide(t, u):
    Z = lerp(0.95, 0.70, glide(u / 1.5))
    cx, cy = lerp(780.0, 880.0, glide(u / 1.5)), 380.0
    v = K.V('office_night', cx, cy, Z)
    ex = lerp(760.0, 905.0, min(1.0, u / 1.5))
    ed = floor_actor(C.edik, ex, 560.0, Z, walk=t * 7.0, prop_n=lambda sp, h: C.mug(sp, h, ''), **ekw(t, (0.9, 0.0)))
    fk = fikus_sill(Z, t)
    return K.shot('office_night', cx, cy, Z, acts=[fk, ed], par=(6 - 10 * u, 0), t=t, dof_k=10, clock='19:45')


# ================================================================== 14: TEA — «Чаем не поливать!»
def r_tea(t, u):
    Z = 1.45
    cx, cy = 1000.0, 300.0
    v = K.V('office_night', cx, cy, Z)
    fk = at(C.fikus, v, 700, 1180, 17.0, near=0.95, **fkw(t, (-0.8, 0.0), wet=1.0 if t > 27.4 else 0.0))
    ed = at(C.edik, v, 230, 880, 24.0, pin='head', near=0.99,
            **ekw(t, (0.9, -0.3), hand_n=(22.0, 60.0), prop_n=lambda sp, h: C.mug(sp, h, '')))
    def f(big, v_):
        if hasattr(ed, 'last') and t < 27.9:
            mx, my = aout(ed, v, 'mug')
            px, py = 640, 760
            for i in range(26):
                k = i / 25.0
                x = lerp(mx, px, k) + 6 * math.sin(t * 20 + i); y = lerp(my, py, k) + 60 * math.sin(math.pi * k) * -0.4
                big[int(y) - 7:int(y) + 7, int(x) - 7:int(x) + 7] = (150, 92, 40)
    return K.shot('office_night', cx, cy, Z, acts=[fk, ed], par=(-4 + 6 * u, 0), t=t, dof_k=26, fx_=f,
                  kick=kick(t, [(27.35, 0.7)]), clock='19:46')


# ================================================================== 16: LOOP — 08:00, the boss again
def r_loop(t, u):
    return r_hook(t, u, name='office_morning', clock='08:00', loop=True)


ST_240 = K.st('240 ЧАСОВ В ГОД', fg=(255, 232, 110), size=56)
ST_VSE = K.st('ВСЁ?!', fg=(255, 120, 110), size=90)
ST_ZAV = K.st('ЗАВХОЗ?!', fg=(255, 232, 110), size=84)
ST_TIME = K.st('+1,5 ЧАСА', fg=(140, 236, 150), size=60)
ST_MORNING = K.st('08:00', fg=(255, 232, 110), size=70)


def r_fik1(t, u): return r_fik(t, u)
def r_f240(t, u): return r_fik(t, u, 'office_night')
def r_fik4(t, u): return r_fik(t, u, 'office_night')
def r_f6(t, u): return r_fik(t, u, 'office_night')


R = [r_hook, r_hat, r_fik1, r_key, r_whisper, r_board, r_clock, r_sleep, r_f240, r_twist, r_throw, r_zavhoz, r_fik4, r_wide, r_tea,
     r_f6, r_loop]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, ['ЗАДЕРЖИСЬ', 'НА 5 МИНУТ!'], hook_t=(0.10, 2.2), hook_y=230, hook_size=76,
              stickers=[(ST_TIME, 12.9, 13.6, 540, 420),
                        (ST_240, 16.3, 17.95, 540, 360),
                        (ST_VSE, 18.0, 19.6, 330, 560),
                        (ST_ZAV, 20.65, 21.7, 540, 520),
                        (ST_MORNING, 31.4, 32.5, 760, 420)],
              flashes=[TWIST, 20.55, 31.32], mosaics=[12.45],
              cap_y={0: 1500, 1: 1240, 2: 1560, 3: 1560, 4: 1500, 5: 1560, 6: 1720, 7: 1380, 8: 1580, 9: 1560, 10: 1500, 11: 1560,
                     12: 1580, 13: 1400, 14: 1560, 15: 1580, 16: 1560})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
