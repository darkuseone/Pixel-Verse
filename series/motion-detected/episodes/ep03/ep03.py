"""S01E03 «$25 LIMIT?!» (MOTION DETECTED, US; 36.1 s, twist 19.15 s / 53 %, type: the reward is the same problem).
STORY (radio play): the office White Elephant, Glenn waves a scratch-off: «Twenty-five dollar LIMIT! And Kyle brought a SCRATCH-OFF?!» —
Marcy from HR: «White Elephant rules, Glenn! Any gift can be STOLEN. Three times, max!» — Glenn whispers to his phone: «I have a SYSTEM.
Let them fight. I steal LAST.» — Doris from the phone app: «Motion detected. Glenn. Staring at the GOLD box. Like a hawk.» — montage:
STEAL 1, STEAL 2 — «Sorry, Marcy. It's MINE!» — TWIST: he rips the gold paper: a KNOCKR Pro box, the second doorbell boots up: «Motion
detected. Glenn. Opening ME.» — Doris on the phone: «Oh no. There's TWO of us now.» — Marcy: «Who brings a DOORBELL to a gift exchange?»
— Trent over the cubicle (TEMP badge): «That's me! Got a minute to talk about SOLAR?» — Glenn quietly slides the box back on the pile:
«Motion detected. Glenn. Regifting ME.»
  python3 ep03.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import overlays as O
from stage import OUT_W, OUT_H
from scene import sm, lerp
from cam25 import glide, kick
from episode import Episode
from props import mdcast as C
from props import mdkit as K
from props import mimic as M
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, MONT, RIP

EPI = Episode('ep03', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='md', lang='us', promise='TOMORROW: $38 TO SHIP A MUG'))
TAB = (C.XTRA, C.EXPR)
FG = M.Face([(0.0, 'furious'), (3.24, 'crushed'), (7.64, 'smug'), (11.14, 'stare'), (15.55, 'stare'), (17.15, 'proud'), (RIP, 'shock'),
             (20.4, 'dead'), (25.55, 'crushed'), (28.3, 'dead'), (30.88, 'smug')], TAB, seed=3)
FD = M.Face([(0.0, 'deadpan'), (11.14, 'smirk'), (14.0, 'deadpan'), (22.7, 'shock'), (24.0, 'crushed')], TAB, seed=8)
FE = M.Face([(0.0, 'deadpan')], TAB, seed=9)
FM = M.Face([(0.0, 'sweet'), (3.24, 'sales'), (15.55, 'proud'), (17.15, 'shock'), (25.55, 'crushed'), (27.0, 'deadpan')], TAB, seed=4)
FT = M.Face([(0.0, 'sales')], TAB, seed=5)

W = 'breakroom'
GX, GY = 800.0, 690.0                   # Glenn on the carpet, facing the table (flip)
MX, MY = 650.0, 705.0                   # Marcy in front of the table's corner, facing Glenn
MARCY_K, TRENT_K = 1.35, 1.34
PHONE = (590.0, 588.0)                  # Glenn's phone on its stand on the table
PS = 2.1
GOLD = (548.0, 560.0)


def mouth(who, t): return M.mouth(EPI.talk, who, t)


def kw_(F, who, t, base, **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), t=t, **kw)


def gkw(t, base=(-0.8, 0.0), **kw): return kw_(FG, 'glenn', t, base, **kw)
def mkw(t, base=(0.8, 0.0), **kw): return kw_(FM, 'marcy', t, base, **kw)
def tkw(t, base=(-0.8, 0.0), **kw): return kw_(FT, 'trent', t, base, **kw)


def doris_talk(t, box=False):
    """mouth of the phone-Doris (d1/d2) vs the boxed one (e1/e2): both speak with the doris voice"""
    lines = ('e1', 'e2') if box else ('d1', 'd2')
    for k in lines:
        a = dict(VOICE_T)[k]
        if a[0] <= t < a[1]: return mouth('doris', t)
    return 0.0


VOICE_T = [(k, (t0, t0 + d)) for (k, _, _, t0, _, d, _, _) in VOICE]


def phone_act(t, Z):
    F_ = FD
    m = doris_talk(t)
    return K.A(lambda sp, **kw: C.phone_stand(sp, t=t, talk=m, expr=F_.speak(t, m), look=F_.look(t, (0.6, 0.0)), blink=F_.blink(t)),
               PHONE[0], PHONE[1], PS * 3 * Z, rim=None)


def gold_act(Z, x=None, y=None, open_=0.0, s=5.4):
    return K.A(lambda sp, **kw: C.gift(sp, gold=True, open_=open_), x or GOLD[0], y or GOLD[1], s * 3 * Z, rim=None)


def pile(Z):
    out = []
    for i, (x, y, c, w, h) in enumerate(((150, 520, (220, 40, 60), 6, 5), (250, 532, (40, 90, 200), 5, 4), (90, 540, (130, 50, 160), 5, 6),
                                          (330, 548, (40, 140, 70), 6, 4))):
        out.append(K.A(lambda sp, c=c, w=w, h=h, **kw: C.gift(sp, col=c, w=w, h=h), x, y, 5.0 * 3 * Z, rim=None))
    return out


def glenn(t, Z, x=GX, y=GY, flip=True, base=(-0.8, 0.0), **kw):
    return K.A(C.glenn, x, y, K.ws_at(y, W) * 3 * Z, flip=flip, **gkw(t, base, robe=False, **kw))


def marcy(t, Z, x=MX, y=MY, flip=False, **kw):
    return K.A(C.marcy, x, y, K.ws_at(y, W) * MARCY_K * 3 * Z, flip=flip, **mkw(t, **kw))


def shot(cx, cy, Z, t, acts, **kw):
    kw.setdefault('dof_k', 0.0)
    return K.shot(W, cx, cy, Z, acts=acts, t=t, **kw)


# ================================================================== 0: HOOK — Glenn with the scratch-off
def r_hook(t, u):
    Z = 2.0 + 0.1 * glide(u / 3.2)
    cx, cy = GX - 10.0, 430.0
    shake = 4 * math.sin(t * 30) * math.exp(-t * 1.5)
    g = glenn(t, Z, hand_n=(14.0, 92.0 + 3 * math.sin(t * 12)), prop_n=C.scratch_off, lean=-2.0)
    return shot(cx, cy, Z, t, [g], par=(-4 + 6 * u, 0), kick=(shake, 0))


# ================================================================== 1: Marcy explains the rules
def r_marcy(t, u):
    Z = 1.55
    cx, cy = 700.0, 520.0
    m = marcy(t, Z, hand_n=(13.0, 44.0 + 4 * math.sin(t * 6)))
    g = glenn(t, Z, base=(-0.9, -0.2))
    return shot(cx, cy, Z, t, pile(Z) + [gold_act(Z), phone_act(t, Z), m, g], par=(-4 + 6 * u, 0))


# ================================================================== 2: «I have a SYSTEM» — whispering to the phone
def r_whisper(t, u):
    Z = 1.9
    cx, cy = 612.0, 440.0
    g = glenn(t, Z, x=650.0, y=700.0, base=(-0.9, 0.5), lean=-2.5, hand_n=(12.0, 60.0))
    return shot(cx, cy, Z, t, [gold_act(Z), phone_act(t, Z), g], par=(-2 + 3 * u, 0))


# ================================================================== 3: the phone CU — Doris + the gold box behind
def r_phone(t, u):
    Z = 3.4 + 0.2 * glide(u / 4.4)
    cx, cy = PHONE[0] - 8.0, PHONE[1] - 26.0
    return shot(cx, cy, Z, t, [gold_act(Z), phone_act(t, Z)], par=(-2 + 3 * u, 0))


# ================================================================== 4: the steals montage — the gold box above Marcy's head
def r_mont(t, u):
    Z = 1.8
    cx, cy = MX + 30.0, 500.0 + 30 * math.sin(u * 9)
    m = marcy(t, Z, hand_n=(4.0, 62.0), hand_f=(-2.0, 62.0), base=(0.0, 1.0))
    v = K.V(W, cx, cy, Z)
    s_ = K.ws_at(MY, W) * MARCY_K
    gb = gold_act(Z, x=MX - 2.0 * s_, y=MY - 64.0 * s_, s=5.4)
    return shot(cx, cy, Z, t, [m, gb], kick=kick(t, [(MONT, 0.6), (16.3, 0.6)]))


# ================================================================== 5: «Sorry, Marcy. It's MINE!» — the grab
def r_grab(t, u):
    Z = 1.6
    cx, cy = 720.0, 520.0
    w = sm(u / 0.5)
    s_ = K.ws_at(MY, W) * MARCY_K
    bx = lerp(MX + 4.0 * s_, GX - 18.0 * K.ws_at(GY, W), w); by = lerp(MY - 40.0 * s_, GY - 56.0 * K.ws_at(GY, W), w)
    m = marcy(t, Z, hand_n=(12.0, 40.0) if w < 0.5 else (10.0, 30.0))
    g = glenn(t, Z, hand_n=(18.0, 56.0), hand_f=(16.0, 52.0))
    return shot(cx, cy, Z, t, [m, g, gold_act(Z, x=bx, y=by)])


# ================================================================== 6: TWIST — the rip: a KNOCKR Pro box; the second doorbell boots
def r_twist(t, u):
    Z = 2.6 - 0.2 * glide(u / 0.6)
    cx, cy = GX - 40.0, 470.0
    ws = K.ws_at(GY, W)
    bx, by = GX - 18.0 * ws, GY - 36.0 * ws
    g = glenn(t, Z, hand_n=(16.0, 54.0), hand_f=(14.0, 52.0), base=(-0.7, -0.6))
    acts = [g]
    if u < 0.35:
        acts.append(gold_act(Z, x=bx, y=by, open_=u / 0.35))
    m = mouth('doris', t) if 'e1' and _T_in(t, 'e1') else 0.0
    acts.append(K.A(lambda sp, **kw: C.doorbell_box(sp, t=t, talk=m, expr=FE.speak(t, m), look=FE.look(t, (0.6, 0.2)), boot=1.0 if t > 19.6 else 0.0),
                    bx, by, 5.0 * 3 * Z, rim=None))
    return shot(cx, cy, Z, t, acts[::-1] if u >= 0.35 else acts, kick=kick(t, [(RIP, 0.9)]))


def _T_in(t, k):
    a, b = dict(VOICE_T)[k]
    return a <= t < b


# ================================================================== 7: «Oh no. There's TWO of us now.»
def r_dcu(t, u):
    Z = 3.8
    cx, cy = PHONE[0] - 4.0, PHONE[1] - 24.0
    return shot(cx, cy, Z, t, [phone_act(t, Z)])


# ================================================================== 8: Marcy — «Who brings a DOORBELL…»
def r_m3(t, u):
    Z = 1.7
    cx, cy = 720.0, 520.0
    ws = K.ws_at(GY, W)
    m = marcy(t, Z, hand_n=(12.0, 44.0))
    g = glenn(t, Z, hand_n=(16.0, 54.0), hand_f=(14.0, 52.0))
    bx = K.A(lambda sp, **kw: C.doorbell_box(sp, t=t, boot=1.0), GX - 18.0 * ws, GY - 36.0 * ws, 5.0 * 3 * Z, rim=None)
    return shot(cx, cy, Z, t, [m, g, bx])


# ================================================================== 9: Trent over the cubicle partition
def r_trent(t, u):
    Z = 2.0
    cx, cy = 1010.0, 380.0
    rise = sm(u / 0.35)
    tr = K.A(C.trent, 1010.0, 640.0 + 60 * (1 - rise), K.ws_at(640.0, W) * TRENT_K * 3 * Z, flip=True,
             **tkw(t, hand_n=(12.0, 40.0), prop_n=lambda sp, h: C.clipboard(sp, h, 'TEMP')))
    return shot(cx, cy, Z, t, [tr])


# ================================================================== 10: button — Glenn slides the box back on the pile
def r_slide(t, u):
    Z = 1.45
    cx, cy = 425.0, 470.0
    w = sm(u / 1.2)
    ws = K.ws_at(600.0, W)
    g = glenn(t, Z, x=lerp(580.0, 500.0, w), y=716.0, base=(-0.9, 0.2), flip=True, hand_n=(18.0, 50.0), lean=-1.0,
              walk=t * 5 if w < 1 else None)
    bx = K.A(lambda sp, **kw: C.doorbell_box(sp, t=t, talk=mouth('doris', t) if _T_in(t, 'e2') else 0.0, boot=1.0),
             lerp(400.0, 330.0, w), 560.0, 5.0 * 3 * Z, rim=None)
    g.near = 0.99; bx.near = 0.98
    return shot(cx, cy, Z, t, pile(Z) + [bx, g])


ST_S1 = K.st('STEAL 1!', fg=(255, 214, 90), size=66)
ST_S2 = K.st('STEAL 2!', fg=(255, 150, 90), size=66)
ST_D2 = K.st('DORIS 2.0', fg=(110, 230, 255), size=70)
R = [r_hook, r_marcy, r_whisper, r_phone, r_mont, r_grab, r_twist, r_dcu, r_m3, r_trent, r_slide]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, ['$25 LIMIT?!'], hook_t=(0.10, 2.7), hook_y=1180, hook_size=84,
              stickers=[(ST_S1, MONT + 0.05, 16.3, 540, 520), (ST_S2, 16.3, 17.15, 540, 640), (ST_D2, 19.7, 22.6, 540, 560)],
              flashes=[TWIST], mosaics=[MONT],
              cap_y={0: 1560, 1: 1580, 2: 1580, 3: 1580, 4: 1580, 5: 1580, 6: 1600, 7: 1600, 8: 1580, 9: 1580, 10: 1500})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
