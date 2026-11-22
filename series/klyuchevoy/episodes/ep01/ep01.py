"""S01E01 v2 «ЗАДЕРЖИСЬ НА 5 МИНУТ!» (standard «голливудский уровень» 22.11.2026; 35.6 s, twist at 19.83 s / 56 %, type: the reward is
the same problem). Variant A = xAI office (this file, KS_VAR=A), variant B = the office drawn in code (episodes/ep01b, KS_VAR=B).
STORY (works as a radio play): 17:59, Эдик in his coat at the light switch. The boss from his office: «Булкин! Задержись на пять минут.
Разговор есть.» Эдик to the ficus: «Аркадий, слышал? Разговор! Меня повышают!» — «Семнадцать лет назад он так же сказал. Ты потом до ночи
шкаф двигал.» (flashback: young Эдик with hair pushing a wardrobe at 23:40) — «Тогда я был стажёр. А сейчас я — ключевой!» — «У тебя ключ
от туалета.» Clock 18:00 -> 21:00: «Девять вечера… Он проверяет мою преданность.» TWIST: the door, the boss in his coat: «О, Булкин, ты
ещё тут? Отлично! Закроешь офис.» (throws the keyring) — «А… разговор?» — «Так это и был разговор! Свет не забудь.» (he flicks the light
off himself, door slam). In the dark: «Аркадий… меня повысили.» — «До сторожа. Зарплата та же.» LOOP: 08:00, Эдик asleep on the chair
with the keys: «Булкин! Задержись на пять минут!» — «Разговор?!»
No background blur (owner 22.11.2026): dof_k = 0 everywhere except the key insert.
  python3 ep01.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, os, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
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
from props import mimic as M
from props.kskit import at, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, T0

VAR = os.environ.get('KS_VAR', 'A')
EP = 'ep01' if VAR == 'A' else 'ep01b'


def WN(n): return n if VAR == 'A' else 'code_' + n


EPI = Episode(EP, VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='ks', lang='ru', promise='ЗАВТРА: ГДЕ ПРЕМИЯ?'),
              promo='ru')
TAB = (C.XTRA, C.EXPR)
FE = M.Face([(0.0, 'shock'), (0.9, 'hopeful'), (3.1, 'beam'), (6.6, 'hopeful'), (8.0, 'crushed'), (10.9, 'proud'), (14.3, 'shock'),
             (15.4, 'crushed'), (16.4, 'sleepy'), (19.83, 'sleepy'), (20.4, 'shock'), (21.4, 'beam'), (22.6, 'panic'), (23.6, 'hopeful'),
             (25.3, 'crushed'), (28.0, 'crushed'), (32.1, 'sleepy'), (34.27, 'beam')], TAB, seed=3)
FF = M.Face([(0.0, 'deadpan'), (6.55, 'deadpan'), (14.3, 'smirk'), (16.0, 'deadpan'), (30.0, 'deadpan'), (31.3, 'smirk')], TAB, seed=8)
FS = M.Face([(0.0, 'boss'), (19.83, 'shock'), (20.6, 'sweet'), (21.6, 'boss'), (25.3, 'sweet'), (32.1, 'boss')], TAB, seed=5)
WS_SILL = 2.9
SILL = (1040.0, 372.0)


def mouth(who, t): return M.mouth(EPI.talk, who, t)


def kw_(F, who, t, base, **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), t=t, **kw)


def ekw(t, base=(0.7, 0.0), **kw): return kw_(FE, 'edik', t, base, **kw)
def fkw(t, base=(0.0, 0.0), **kw): return kw_(FF, 'fikus', t, base, **kw)
def skw(t, base=(0.7, 0.0), **kw): return kw_(FS, 'shef', t, base, **kw)


def floor_actor(fn, wx, wy, Z, **kw):
    return K.A(fn, wx, wy, K.ws_at(wy) * 3 * Z, **kw)


def door_open(big, v, k=1.0):
    """the boss's door open: a dark doorway with a warm glow from his office"""
    x0, y0 = v.opt(60.0, 172.0); x1, y1 = v.opt(206.0, 506.0)
    xa, xb = int(max(0, x0)), int(min(OUT_W, x1)); ya, yb = int(max(0, y0)), int(min(OUT_H, y1))
    if xa >= xb or ya >= yb: return
    reg = big[ya:yb, xa:xb].astype(np.float32)
    reg = reg * (1 - 0.85 * k) + np.array((40, 30, 26)) * 0.85 * k
    yy = np.linspace(0, 1, yb - ya)[:, None, None]
    reg += np.clip(1 - yy * 1.3, 0, 1) * 60 * k * np.array((1.0, 0.75, 0.45))
    big[ya:yb, xa:xb] = np.clip(reg, 0, 255).astype(np.uint8)


def shot(name, cx, cy, Z, **kw):
    kw.setdefault('dof_k', 0.0)                                      # no background blur unless it means something (owner 22.11.2026)
    return K.shot(WN(name), cx, cy, Z, **kw)


def V(name, cx, cy, Z): return K.V(WN(name), cx, cy, Z)


def plate(big, text, y, fg=(255, 232, 110), size=44):
    img = O.sticker(text, fg=fg, size=size)
    O.overlay(big, img, (OUT_W - img.shape[1]) // 2, y, 1.0)


# ================================================================== 0/14/15: HOOK and LOOP — the boss at his door, Эдик up front
def r_hook(t, u, name='office', clock='17:59', loop=False, awake=True):
    Z = 1.0
    cx, cy = 220.0, 250.0
    v = V(name, cx, cy, Z)
    sh = at(C.shef, v, 250, 1760, 11.0, **skw(t, (0.9, 0.1), coat=not loop or True, prop_f=lambda sp, h: C.briefcase(sp, h)))
    if not loop:
        ed = at(C.edik, v, 790, 1190, 24.0, flip=True, pin='head', near=0.99,
                **ekw(t, (-0.9, 0.0), coat=True, hat=True, hand_n=(16.0, 70.0) if t < 1.2 else None))
    else:
        if awake:
            jump = sm(u / 0.25)
            ed = at(C.edik, v, 790, 1190 - 40 * jump, 24.0, flip=True, pin='head', near=0.99,
                    **ekw(t, (-0.9, 0.0), coat=True, stubble_=1.0, hand_n=(16.0, 52.0), prop_n=lambda sp, h: C.keyring(sp, h, tag=True),
                          key_swing=0.6 * math.sin(t * 9) * math.exp(-u * 2)))
        else:
            ed = at(C.edik, v, 790, 1240, 24.0, flip=True, pin='head', near=0.99, lean=-2.0,
                    **ekw(t, (0.0, -1.0), coat=True, stubble_=1.0, hand_n=(12.0, 36.0), prop_n=lambda sp, h: C.keyring(sp, h, tag=True)))
    def pre(big, v_): door_open(big, v_, 1.0)
    def f(big, v_):
        if loop and not awake:
            hx, hy = 860, 980
            for i in range(3):
                k = ((t * 0.7 + i / 3) % 1.0)
                plate(big, 'Z', int(hy - 160 * k - 60 * i), fg=(200, 220, 255), size=40 + 12 * i) if False else None
                img = O.sticker('z', fg=(200, 220, 255), size=40 + 14 * i)
                O.overlay(big, img, int(hx + 50 * i + 30 * k), int(hy - 200 * k - 50 * i), 1.0 - k * 0.5)
    return shot(name, cx, cy, Z, acts=[sh, ed], par=(-4 + 6 * u, 0), t=t, clock=clock, pre=pre, fx_=f)


def r_loop(t, u): return r_hook(t, u, 'office_morning', '08:00', loop=True, awake=False)
def r_jump(t, u): return r_hook(t, u, 'office_morning', '08:01', loop=True, awake=True)


# ================================================================== 1: «Аркадий, слышал?» — two-shot with the ficus on the windowsill
def r_aside(t, u):
    Z = 1.3
    cx, cy = 960.0, 330.0
    v = V('office', cx, cy, Z)
    fk = K.A(C.fikus, SILL[0], SILL[1], WS_SILL * 3 * Z, **fkw(t, (-0.8, 0.0)))
    ed = at(C.edik, v, 330, 1020, 22.0, pin='head', near=0.99, **ekw(t, (0.9, 0.1), coat=True,
                                                                          hand_n=(18.0, 58.0 + 2 * math.sin(t * 7)), hand_f=(10.0, 56.0)))
    return shot('office', cx, cy, Z, acts=[fk, ed], par=(-6 + 8 * u, 0), t=t)


# ================================================================== 2/5/13: FIKUS
def r_fik(t, u, name='office', Z0=1.35, dark=False):
    Z = Z0 + 0.04 * u
    cx, cy = 1020.0, 250.0
    v = V(name, cx, cy, Z)
    fk = at(C.fikus, v, 540, 900, 22.0, pin='head', near=0.99, **fkw(t))
    big = shot(name, cx, cy, Z, acts=[fk], par=(-4 + 8 * u, 0), t=t, clock='18:00')
    if dark:
        big[:] = (big * 0.55).astype(np.uint8)
        yy, xx = np.mgrid[0:OUT_H, 0:OUT_W]
        m = np.clip(1 - np.hypot(xx - 620, yy - 700) / 700, 0, 1)[..., None]
        big[:] = np.clip(big * (1 + 0.9 * m) + m * np.array((10, 20, 50)), 0, 255).astype(np.uint8)
    return big


def r_fik1(t, u): return r_fik(t, u)
def r_fkey(t, u): return r_fik(t, u, Z0=1.25)
def r_f3(t, u): return r_fik(t, u, 'office_night', dark=True)


# ================================================================== 3: FLASHBACK — 17 years ago, young Эдик pushes a wardrobe at night
def r_flash(t, u):
    Z = 1.0
    x = lerp(330.0, 420.0, u / 2.05)
    cx, cy = x + 60.0, 380.0
    v = V('office', cx, cy, Z)
    S = K.ws_at(560.0) * 3 * Z
    wr = K.A(lambda sp, **kw: C.wardrobe(sp), x + 118.0, 560.0, S * 1.05, rim=None)
    wr.near = 0.99
    ed = floor_actor(C.edik, x, 566.0, Z, young=True, lean=6.0, walk=t * 5.0, sweat=2.0, hand_n=(26.0, 48.0), hand_f=(22.0, 46.0),
                     **{k_: v_ for k_, v_ in ekw(t, (0.9, 0.0)).items() if k_ not in ('expr',)}, expr='panic')
    ed.near = 0.99
    big = shot('office', cx, cy, Z, acts=[wr, ed], par=(-6 + 8 * u, 0), t=t, clock='23:40', motes=False)
    g = big.astype(np.float32).mean(axis=2, keepdims=True)                             # sepia memory
    big[:] = np.clip(g * np.array((1.12, 0.94, 0.72)) + 10, 0, 255).astype(np.uint8)
    rng = np.random.default_rng(int(t * 30))
    big[:] = np.clip(big.astype(np.int16) + rng.integers(-10, 10, (OUT_H, OUT_W, 1)), 0, 255).astype(np.uint8)
    fx.vignette(big, 0.55)
    plate(big, '17 ЛЕТ НАЗАД', 330, fg=(255, 232, 160), size=56)
    return big


# ================================================================== 4: «Тогда я был стажёр. А сейчас я — ключевой!»
def r_proud(t, u):
    Z = 1.3
    cx, cy = 560.0, 360.0
    v = V('office', cx, cy, Z)
    chest = sm((t - 12.6) / 0.4)
    ed = at(C.edik, v, 540, 860 - 30 * chest, 32.0, pin='head', near=0.99,
            **ekw(t, (0.0, 0.0), coat=True, hand_n=(12.0 - 4 * chest, 48.0 + 10 * chest), hand_f=(-2.0, 46.0)))
    return shot('office', cx, cy, Z, acts=[ed], par=(-6 + 10 * u, 0), t=t)


# ================================================================== 6: INSERT — the toilet key (the only shot with a soft background)
def r_key(t, u):
    Z = 1.3
    cx, cy = 430.0, 380.0
    v = V('office', cx, cy, Z)
    ed = at(C.edik, v, 540, 1000, 44.0, pin='wc', near=0.99,
            **ekw(t, coat=True, key_swing=0.55 * math.sin((t - 15.35) * 5.5) * math.exp(-(t - 15.35) * 0.6)))
    return shot('office', cx, cy, Z, acts=[ed], par=(4 * u, 0), t=t, dof_k=10)


# ================================================================== 7: CLOCK — 18:00 -> 21:00
def r_clock(t, u):
    k = glide(u / 1.1)
    mins = int(lerp(18 * 60, 21 * 60, k))
    hhmm = f'{mins // 60:02d}:{mins % 60:02d}'
    big = K.clock_insert(t, hhmm)
    plate(big, hhmm, 1470, size=88)
    return big


# ================================================================== 8: 21:00 — on a chair at the boss's door, stubborn
def r_chair(t, u):
    Z = 1.25
    cx, cy = 230.0, 360.0
    v = V('office_night', cx, cy, Z)
    ed = floor_actor(C.edik, 258.0, 530.0, Z, flip=True, lean=-3.0,
                     **ekw(t, (-0.9, -0.2), coat=True, hand_n=(10.0, 34.0), hand_f=(4.0, 34.0)))
    return shot('office_night', cx, cy, Z, acts=[ed], par=(-4 + 6 * u, 0), t=t, clock='21:00')


# ================================================================== 9: TWIST — the door, the boss in his coat, the keyring flies
def keys_actor(wx, wy, s, swing=0.0):
    return K.A(lambda sp, **kw: C.keyring(sp, (0.0, 12.0), swing=swing, tag=True), wx, wy, s)


def r_twist(t, u):
    Z = 1.05
    cx, cy = 260.0, 330.0
    v = V('office_night', cx, cy, Z)
    w = glide(u / 1.2)
    t_hit = 22.75
    caught = t >= t_hit
    throw = t >= 22.2
    sh = floor_actor(C.shef, lerp(132.0, 215.0, w), 508.0 + 12 * w, Z,
                     **skw(t, (0.9, 0.1), coat=True, walk=t * 7.0 if u < 1.2 else None,
                           hand_n=(26.0, 66.0) if 21.6 < t < 22.4 else None, prop_f=lambda sp, h: C.briefcase(sp, h)))
    S = K.ws_at(540.0) * 3 * Z
    sag = (5.0 * math.exp(-(t - t_hit) * 3.0) * math.cos((t - t_hit) * 14) + 3.0) if caught else 0.0
    ed = floor_actor(C.edik, 340.0, 548.0, Z, flip=True, oy=-sag, lean=-3.0 * (1 - sm((t - 20.3) / 0.3)),
                     **ekw(t, (-0.9, 0.2), coat=True, hand_n=(18.0, 46.0) if not caught else (16.0, 30.0 - sag),
                           prop_n=(lambda sp, h: C.keyring(sp, h, tag=True)) if caught else None))
    acts = [sh, ed]
    if throw and not caught:
        kk = (t - 22.2) / (t_hit - 22.2)
        x = lerp(230.0, 325.0, kk); y = lerp(330.0, 400.0, kk) - 80 * math.sin(math.pi * kk)
        acts.append(keys_actor(x, y, S * 1.2, swing=t * 9))
    def pre(big, v_): door_open(big, v_, sm(u / 0.15))
    return shot('office_night', cx, cy, Z, acts=acts, par=(-3 + 5 * u, 0), t=t, clock='21:30', pre=pre,
                kick=kick(t, [(TWIST, 0.8), (t_hit, 0.7)]))


# ================================================================== 10: «А… разговор?»
def r_e4(t, u):
    Z = 1.3
    cx, cy = 420.0, 380.0
    v = V('office_night', cx, cy, Z)
    ed = at(C.edik, v, 540, 720, 28.0, pin='head', near=0.99,
            **ekw(t, (-0.4, 0.0), coat=True, hand_n=(15.0, 50.0), prop_n=lambda sp, h: C.keyring(sp, h, tag=True, swing=0.1 * math.sin(t * 2))))
    return shot('office_night', cx, cy, Z, acts=[ed], par=(4 - 6 * u, 0), t=t, clock='21:31')


# ================================================================== 11: «Так это и был разговор! Свет не забудь.» — he flicks it off himself
def r_exit(t, u):
    Z = 1.1
    cx, cy = 300.0, 330.0
    v = V('office_night', cx, cy, Z)
    w = glide(u / 2.2)
    sh = floor_actor(C.shef, lerp(330.0, 268.0, w), 520.0, Z, flip=True, **skw(t, (-0.9, 0.0), coat=True, walk=t * 7.0 if u < 2.2 else None,
                     hand_n=(24.0, 62.0) if t > 27.4 else None, prop_f=lambda sp, h: C.briefcase(sp, h)))
    ed = at(C.edik, v, 860, 900, 20.0, flip=True, pin='head', near=0.99,
            **ekw(t, (-0.9, 0.0), coat=True, hand_n=(16.0, 40.0), prop_n=lambda sp, h: C.keyring(sp, h, tag=True)))
    big = shot('office_night', cx, cy, Z, acts=[sh, ed], par=(-3 + 4 * u, 0), t=t, clock='21:32')
    if t >= 27.72:
        big[:] = (big * 0.18).astype(np.uint8)                                           # the light goes off
    return big


# ================================================================== 12: in the dark — «Аркадий… меня повысили.»
def r_dark(t, u):
    Z = 1.3
    cx, cy = 560.0, 360.0
    v = V('office_night', cx, cy, Z)
    ed = at(C.edik, v, 540, 820, 32.0, pin='head', near=0.99,
            **ekw(t, (0.0, -0.2), coat=True, hand_n=(15.0, 48.0), prop_n=lambda sp, h: C.keyring(sp, h, tag=True)))
    big = shot('office_night', cx, cy, Z, acts=[ed], par=(2 * u, 0), t=t, clock='21:33', motes=False)
    big[:] = (big * 0.35).astype(np.uint8)
    yy, xx = np.mgrid[0:OUT_H, 0:OUT_W]
    m = np.clip(1 - np.hypot(xx - 560, (yy - 980) * 0.8) / 620, 0, 1)[..., None] ** 1.4      # the phone torch from below
    big[:] = np.clip(big * (1 + 2.2 * m) + m * np.array((30, 34, 40)), 0, 255).astype(np.uint8)
    return big


ST_ZAV = K.st('ЗАВХОЗ?!', fg=(255, 232, 110), size=84)
R = [r_hook, r_aside, r_fik1, r_flash, r_proud, r_fkey, r_key, r_clock, r_chair, r_twist, r_e4, r_exit, r_dark, r_f3, r_loop, r_jump]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, ['ЗАДЕРЖИСЬ', 'НА 5 МИНУТ!'], hook_t=(0.10, 2.6), hook_y=210, hook_size=72,
              stickers=[(ST_ZAV, 22.85, 23.6, 540, 520)],
              flashes=[TWIST], mosaics=[8.85, 10.90],
              cap_y={0: 1560, 1: 1560, 2: 1580, 3: 1560, 4: 1560, 5: 1580, 6: 1560, 7: 1700, 8: 1500, 9: 1560, 10: 1560, 11: 1300,
                     12: 1560, 13: 1580, 14: 1560, 15: 1560})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
