"""S01E06 «FINAL ATTEMPT!» (MOTION DETECTED, US; season finale; 33.6 s, twist 16.55 s / 49 %, type: the reward threatens a friend).
STORY (radio play): 6 AM, frost, Glenn slept on the porch in a sleeping bag: «Final attempt. Six A.M. Nobody gets past ME.» — Doris:
«Motion detected. Glenn. Slept on the porch. In the ROBE.» — a van; the PARCELZ courier is… Trent: «Morning, Glenn! New job. Got a minute
to SIGN?» — «Sign here. And here. And HERE. And one for the SOLAR.» — «I SIGNED! Linda! Your gift is HERE!» — he opens it: KNOCKR ULTRA
boots: «ULTRA online. Previous doorbell: obsolete. Deleting DORIS.» — Doris dims: «Oh. That's fine. Motion detected. Glenn. Replacing ME.»
— Glenn sticks the orange tag on ULTRA: «Nah. Trent? Return to SENDER.» — Doris lights up: «Motion detected. Glenn. Being a good GUY. In
the ROBE.» — hook card «SEASON 2: NEW YEAR'S EVE». Callbacks: the tag (E01), «In the ROBE» (E01), Trent's SOLAR (all season).
  python3 ep06.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, VAN, OPEN, S2

EPI = Episode('ep06', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='md', lang='us', promise='SEASON 2: NEW YEAR\'S EVE'))
TAB = (C.XTRA, C.EXPR)
FG = M.Face([(0.0, 'smug'), (3.45, 'sleepy'), (VAN, 'hopeful'), (10.6, 'proud'), (13.6, 'proud'), (TWIST, 'shock'), (21.0, 'crushed'),
             (25.35, 'sweet'), (27.7, 'proud')], TAB, seed=3)
FD = M.Face([(0.0, 'deadpan'), (3.45, 'smirk'), (6.0, 'deadpan'), (TWIST, 'shock'), (21.0, 'crushed'), (27.7, 'sweet')], TAB, seed=8)
FT = M.Face([(0.0, 'sales')], TAB, seed=5)

W = 'porch_dawn'
DORIS = (346.0, 324.0)
DS = 1.55
FEET = 528.0
GX = 470.0


def mouth(who, t): return M.mouth(EPI.talk, who, t)


def kw_(F, who, t, base, **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), t=t, **kw)


def gkw(t, base=(-0.8, 0.0), **kw): return kw_(FG, 'glenn', t, base, **kw)


def doris_act(t, Z, base=(0.6, 0.0)):
    sad = 21.0 <= t < 27.7
    a = K.A(C.doris, DORIS[0], DORIS[1], DS * 3 * Z, rim=None, **kw_(FD, 'doris', t, base, dnd=False, glow=0.2 if sad else 1.0))
    return a


def glenn(t, Z, x=GX, y=FEET, flip=True, base=(-0.8, 0.0), **kw):
    return K.A(C.glenn, x, y, K.ws_at(y) * 3 * Z, flip=flip, **gkw(t, base, **kw))


def trent(t, Z, x, y, flip=True, **kw):
    return K.A(C.trent, x, y, K.ws_at(y) * 1.34 * 3 * Z, flip=flip, **kw_(FT, 'trent', t, (-0.8, 0.0), courier=True, **kw))


def box_act(Z, x, y, open_=0.0, label=True):
    def f(sp, **kw):
        sp.sup(0.0, 6.0, 8.0, 6.0, C.tones((190, 150, 100)), n=6.0)
        C.thin(sp, (-8.0, 10.0), (8.0, 10.0), (230, 200, 120), 0.6)
        sp.txt_box(['PARCELZ', 'FINAL ATTEMPT'], (-7.0, 2.0, 7.0, 8.0), (40, 30, 26), pad=0.2)
        if open_ > 0:
            sp.sup(-8.0 - 4 * open_, 12.0 + 2 * open_, 4.0, 0.8, C.tones((200, 160, 110)), n=6.0)
    return K.A(f, x, y, 3.2 * 3 * Z, rim=None)


def ultra_act(t, Z, x, y, s=3.0, tag=False):
    m = mouth('ultra', t)
    def f(sp, **kw):
        C.ultra(sp, t=t, talk=m)
        if tag:
            C.door_tag(sp, (-2.0, 26.0), 0.8, 0.15)
    return K.A(f, x, y, s * 3 * Z, rim=None)


def shot(cx, cy, Z, t, acts, **kw):
    kw.setdefault('dof_k', 0.0)
    return K.shot(W, cx, cy, Z, acts=acts, t=t, **kw)


def r_hook(t, u):
    Z = 1.8 + 0.1 * glide(u / 3.4)
    cx, cy = GX - 10.0, 390.0
    g = glenn(t, Z, y=FEET + 2, seated=True, oy=-18.0, hand_n=(14.0, 52.0), hand_f=(10.0, 46.0), base=(-0.4, 0.1))
    bag = K.A(C.sleeping_bag, GX - 4.0, FEET + 4, K.ws_at(FEET) * 1.5 * 3 * Z, flip=True, rim=None)
    bag.near = 0.99
    return shot(cx, cy, Z, t, [doris_act(t, Z), g, bag], par=(-4 + 6 * u, 0))


def r_doris(t, u, Z0=2.8):
    Z = Z0 + 0.15 * glide(u / 3.8)
    cx, cy = DORIS[0] + 30.0, DORIS[1] - 30.0
    return shot(cx, cy, Z, t, [doris_act(t, Z)], par=(-2 + 3 * u, 0))


def r_trent(t, u):
    Z = 1.3
    cx, cy = 470.0, 330.0
    w = sm(u / 1.6)
    tr = trent(t, Z, lerp(640.0, 540.0, w), lerp(640.0, FEET + 6, w), walk=t * 8 if w < 1 else None,
               hand_n=(14.0, 34.0), prop_n=lambda sp, h: C.clipboard(sp, h, 'SIGN'))
    g = glenn(t, Z, x=430.0, base=(0.9, 0.0), flip=False, hand_n=(12.0, 50.0))
    return shot(cx, cy, Z, t, [doris_act(t, Z), g, tr])


def r_sign(t, u):
    Z = 2.0
    cx, cy = 480.0, 300.0
    pen = 2.0 * math.sin(t * 18)
    tr = trent(t, Z, 540.0, FEET + 6, hand_n=(12.0, 40.0), prop_n=lambda sp, h: C.clipboard(sp, h, 'SIGN'))
    g = glenn(t, Z, x=440.0, base=(0.9, 0.4), flip=False, hand_n=(20.0 + pen, 52.0))
    return shot(cx, cy, Z, t, [g, tr])


def r_gift(t, u):
    Z = 1.7
    cx, cy = 450.0, 300.0
    ws = K.ws_at(FEET)
    g = glenn(t, Z, x=440.0, flip=False, base=(0.6, 0.3), hand_n=(14.0, 64.0), hand_f=(8.0, 64.0))
    bx = box_act(Z, 440.0 + 11 * ws, FEET - 60 * ws, open_=sm((t - OPEN) / 0.3) if t > OPEN else 0.0)
    bx.near = 0.995
    acts = [g, bx]
    acts.append(trent(t, Z, 560.0, FEET + 6, hand_n=(12.0, 40.0)))
    return shot(cx, cy, Z, t, acts)


def r_twist(t, u):
    Z = 2.8 - 0.2 * glide(u / 0.6)
    cx, cy = 440.0, 215.0
    ws = K.ws_at(FEET)
    rise = sm(u / 0.5)
    by = FEET - 70 * ws
    acts = [ultra_act(t, Z, 440.0, by - 9 * ws * rise - 4 * ws, s=3.6), box_act(Z, 440.0, by)]
    for a in acts: a.near = 0.995
    def f(big, v_):
        ox, oy = v_.opt(440.0, by - 60 * ws)
        yy, xx = np.ogrid[0:OUT_H, 0:OUT_W]
        m = np.clip(1 - np.hypot(xx - ox, yy - oy) / 700, 0, 1)[..., None] ** 2 * rise
        big[:] = np.clip(big + m * np.array((90, 40, 140)), 0, 255).astype(np.uint8)
    return shot(cx, cy, Z, t, acts, fx_=f, kick=kick(t, [(TWIST, 0.9)]))


def r_dsad(t, u):
    Z = 3.0 + 0.3 * glide(u / 4.3)
    cx, cy = DORIS[0] + 10.0, DORIS[1] - 30.0
    return shot(cx, cy, Z, t, [doris_act(t, Z, base=(0.0, 0.8))])


def r_tag(t, u):
    Z = 1.9
    cx, cy = 480.0, 300.0
    ws = K.ws_at(FEET)
    g = glenn(t, Z, x=430.0, flip=False, base=(0.9, 0.2), hand_n=(18.0, 60.0))
    ul = ultra_act(t, Z, 470.0 + 12 * ws * sm(u / 1.2), FEET - 50 * ws, s=3.2, tag=u > 0.5)
    ul.near = 0.995
    tr = trent(t, Z, 560.0, FEET + 6, hand_n=(-6.0, 50.0))
    return shot(cx, cy, Z, t, [g, tr, ul])


def r_bye(t, u):
    Z = 1.05
    cx, cy = lerp(470.0, 560.0, glide(u / 5.0)), 340.0
    w = sm(u / 3.0)
    ws = K.ws_at(FEET)
    tx, ty = lerp(540.0, 760.0, w), lerp(FEET + 6, 640.0, w)
    tr = trent(t, Z, tx, ty, flip=False, walk=t * 8 if w < 1 else None, hand_n=(12.0, 50.0))
    ul = ultra_act(t, Z, tx + 10 * ws, ty - 52 * ws, s=3.0, tag=True)
    g = glenn(t, Z, x=430.0, flip=False, base=(0.9, 0.0), hand_n=(10.0, 96.0 + 6 * math.sin(t * 8)))
    return shot(cx, cy, Z, t, [doris_act(t, Z), g, tr, ul])


ST_DEL = K.st('DELETING DORIS... 12%', fg=(200, 140, 255), size=48)
ST_RET = K.st('RETURN TO SENDER', fg=(255, 140, 60), size=58)
ST_S2 = K.st("SEASON 2: NEW YEAR'S EVE", fg=(110, 230, 255), size=40)
R = [r_hook, r_doris, r_trent, r_sign, r_gift, r_twist, r_dsad, r_tag, r_bye]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, ['FINAL ATTEMPT!'], hook_t=(0.10, 2.7), hook_y=1120, hook_size=74,
              stickers=[(ST_DEL, 19.0, 21.0, 540, 1430), (ST_RET, 26.2, 27.7, 540, 1240), (ST_S2, S2, DUR, 540, 1180)],
              flashes=[TWIST], mosaics=[VAN],
              cap_y={0: 1580, 1: 1580, 2: 1580, 3: 1580, 4: 1580, 5: 1600, 6: 1600, 7: 1580, 8: 1500})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
