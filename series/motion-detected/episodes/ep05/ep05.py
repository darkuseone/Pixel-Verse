"""S01E05 «IN-LAWS IN 1 HOUR?!» (MOTION DETECTED, US; 36.3 s, twist 20.5 s / 56 %, type: the opponent is just like you).
STORY (radio play): a messy living room, Glenn with the phone: «Linda's parents in ONE hour?! This house needs a WEEK!» — the laundry pile on
the couch moves; Doris from the wall monitor: «Motion detected. Laundry pile. Moving. Oh, that's GLENN.» — «I have a SYSTEM. Everything
goes in ONE closet.» — montage: everything flies into the closet: «Closet capacity: four hundred PERCENT. Door holding. For NOW.» —
the room is spotless: «Fifty-nine minutes. Spotless. I'm a GENIUS.» — TWIST, the monitor shows the driveway: «Motion detected. Ron. He's
been in your driveway for FORTY minutes.» — Ron at the door, whispering: «Glenn. Pat's still in the car. Can I hide in your CLOSET?» —
«Ron, NOT the clos-» — the avalanche — under the pile three heads: Glenn, Ron… and Trent: «Hi, guys! Got a minute to talk about SOLAR?» —
«Motion detected. Two men. One salesman. Under a LAUNDRY pile.»
  python3 ep05.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, MONT, AVAL

EPI = Episode('ep05', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='md', lang='us', promise='TOMORROW: FINAL ATTEMPT'))
TAB = (C.XTRA, C.EXPR)
FG = M.Face([(0.0, 'panic'), (3.45, 'crushed'), (5.6, 'dead'), (7.58, 'smug'), (MONT, 'panic'), (14.65, 'proud'), (17.72, 'proud'),
             (TWIST, 'shock'), (22.45, 'stare'), (25.74, 'panic'), (AVAL + 0.3, 'dead'), (30.45, 'dead')], TAB, seed=3)
FD = M.Face([(0.0, 'deadpan'), (3.45, 'smirk'), (6.0, 'deadpan'), (17.72, 'deadpan'), (30.45, 'deadpan')], TAB, seed=8)
FR = M.Face([(0.0, 'pleading'), (25.74, 'stare'), (AVAL + 0.3, 'dead')], TAB, seed=6)
FT = M.Face([(0.0, 'sales')], TAB, seed=5)

W = 'living'
MON = (1046.0, 172.0)                    # the KNOCKR wall monitor next to the front door
MS = 3.0
CLO = (80.0, 480.0)                      # the closet door (bottom centre)


def mouth(who, t): return M.mouth(EPI.talk, who, t)


def kw_(F, who, t, base, **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), t=t, **kw)


def gkw(t, base=(-0.8, 0.0), **kw): return kw_(FG, 'glenn', t, base, **kw)


def glenn(t, Z, x, y, flip=True, base=(-0.8, 0.0), **kw):
    return K.A(C.glenn, x, y, K.ws_at(y, W) * 3 * Z, flip=flip, **gkw(t, base, **kw))


def ron(t, Z, x, y, flip=True, **kw):
    return K.A(C.ron, x, y, K.ws_at(y, W) * 1.25 * 3 * Z, flip=flip, **kw_(FR, 'ron', t, (-0.8, 0.0), **kw))


def monitor(t, Z, inset=None):
    m = mouth('doris', t)
    return K.A(lambda sp, **kw: C.wall_monitor(sp, t=t, talk=m, expr=FD.speak(t, m), look=FD.look(t, (0.6, 0.0)), inset=inset),
               MON[0], MON[1], MS * 3 * Z, rim=None)


def mess(t, Z, k=1.0, wob=0.0):
    """the mess: laundry heaps on the couch and the floor, pizza boxes; k = how much is left (1 → 0 as it flies into the closet)"""
    out = []
    for i, (x, y, w, h, s) in enumerate(((390.0, 430.0, 18.0, 9.0, 1), (640.0, 640.0, 14.0, 7.0, 2), (250.0, 600.0, 12.0, 6.0, 3),
                                          (900.0, 600.0, 10.0, 5.0, 4))):
        if k > i / 4.0:
            out.append(K.A(lambda sp, w=w, h=h, s=s, **kw: C.laundry(sp, t=t, w=w, h=h, seed=s, wobble=wob if s == 1 else 0.0),
                           x, y, 6.5 * 3 * Z, rim=None))
    return out


def shot(cx, cy, Z, t, acts, **kw):
    kw.setdefault('dof_k', 0.0)
    return K.shot(W, cx, cy, Z, acts=acts, t=t, **kw)


def plate(big, text, y, fg=(255, 255, 255), size=44, x=None):
    img = O.sticker(text, fg=fg, size=size)
    O.overlay(big, img, (OUT_W - img.shape[1]) // 2 if x is None else x, y, 1.0)


def r_hook(t, u):
    Z = 1.9 + 0.1 * glide(u / 3.4)
    cx, cy = 600.0, 330.0
    shake = 4 * math.sin(t * 30) * math.exp(-t * 1.5)
    g = glenn(t, Z, 620.0, 620.0, hand_n=(14.0, 92.0 + 3 * math.sin(t * 12)), prop_n=C.phone, lean=-2.0)
    big = shot(cx, cy, Z, t, mess(t, Z) + [g], par=(-4 + 6 * u, 0), kick=(shake, 0))
    plate(big, 'LINDA: MOM & DAD 1 HR AWAY :)', 1380, fg=(255, 214, 120), size=40)
    return big


def r_laundry(t, u):
    Z = 2.0
    cx, cy = 400.0, 330.0
    pop = sm((t - 5.4) / 0.3)
    g = K.A(C.glenn, 400.0, lerp(860.0, 700.0, pop), 3.9 * 3 * Z, flip=False, **gkw(t, (0.9, 0.2), hand_n=(10.0, 70.0)))
    g.near = 0.9
    pile = K.A(lambda sp, **kw: C.laundry(sp, t=t, w=22.0, h=14.0, seed=1, wobble=0.4 if t < 5.4 else 0.0), 400.0, 500.0, 7.0 * 3 * Z, rim=None)
    pile.near = 0.95
    acts = ([g] if pop > 0.05 else []) + [pile]
    return shot(cx, cy, Z, t, acts, par=(-3 + 4 * u, 0))


def r_sys(t, u):
    Z = 1.7
    cx, cy = 200.0, 300.0
    g = glenn(t, Z, 230.0, 600.0, base=(-0.9, 0.0), hand_n=(18.0, 56.0))
    return shot(cx, cy, Z, t, mess(t, Z) + [g], par=(-3 + 4 * u, 0))


def r_mont(t, u):
    Z = 1.0
    cx, cy = 480.0, 380.0
    k = min(1.0, u / 3.9)
    x = 300.0 + 250.0 * abs(math.sin(u * 2.4))
    g = glenn(t, Z, x, 640.0, flip=math.cos(u * 2.4) > 0, walk=t * 14, sweat=2.0)
    acts = mess(t, Z, 1.0 - k) + [g]
    for i in range(6):
        p = ((u * 1.6 + i / 6.0) % 1.0)
        jx = lerp(600.0 - i * 60, 90.0, p); jy = lerp(560.0, 380.0, p) - 160 * math.sin(math.pi * p)
        acts.append(K.A(lambda sp, i=i, **kw: C.junk(sp, kind=i), jx, jy, 7.0 * 3 * Z, rim=None))
    big = shot(cx, cy, Z, t, acts)
    plate(big, f'CLOSET: {int(lerp(60, 400, k))}%', 1350, fg=(255, 120, 90), size=64)
    return big


def strain(k):
    """the closet door bulges: dark gap lines around it and a bowed panel"""
    def f(big, v_):
        x0, y0 = v_.opt(10.0, 60.0); x1, y1 = v_.opt(158.0, 478.0)
        xa, xb, ya, yb = int(max(0, x0)), int(min(OUT_W, x1)), int(max(0, y0)), int(min(OUT_H, y1))
        if xa >= xb or ya >= yb: return
        w = max(3, int(4 * k * v_.Z))
        big[ya:yb, max(0, xb - w):xb] = (30, 20, 16)
        big[ya:ya + w, xa:xb] = (30, 20, 16)
    return f


def r_clean(t, u):
    Z = 1.15
    cx, cy = 380.0, 360.0
    g = glenn(t, Z, 470.0, 620.0, flip=False, base=(0.6, -0.2), hand_n=(14.0, 96.0), hand_f=(-10.0, 96.0))
    wob = 3 * math.sin(t * 24) * (math.sin(t * 3) > 0.3)
    return shot(cx, cy, Z, t, [g], fx_=strain(1.0), kick=(wob, 0))


def car_inset(t):
    def f(sp):
        sp.fill(sp.m_super(0.0, 9.0, 5.8, 5.6, 6.0)[0], (150, 170, 200), keep=True)                     # sky / windshield
        sp.fill(sp.m_super(0.0, 5.0, 5.8, 1.6, 6.0)[0], (60, 64, 80), keep=True)                         # dash
        sp.ell(0.0, 9.6, 2.2, 2.4, C.tones(C.SKIN_R))                                                    # Ron at the wheel
        sp.fill(sp.m_super(0.0, 11.8, 2.6, 0.9, 3.0)[0], (90, 110, 80), keep=True)
        sp.blob(1.4, 9.2, 0.5, (220, 90, 90), keep=True)
        sp.fill(sp.m_super(0.0, 14.4, 6.0, 0.5, 8.0)[0], (60, 64, 80), keep=True)
        thin(sp, (-5.6, 13.6), (-3.0, 4.4), (60, 64, 80), 0.4); thin(sp, (5.6, 13.6), (3.0, 4.4), (60, 64, 80), 0.4)
        sp.txt_box(['DRIVEWAY', '40:00'], (-5.4, 12.8, 0.0, 14.6), (250, 80, 80), pad=0.05)
    return f


from props.kspix import thin


def r_monitor(t, u):
    Z = 3.2 + 0.2 * glide(u / 4.6)
    cx, cy = MON[0] + 2.0, MON[1] - 30.0
    return shot(cx, cy, Z, t, [monitor(t, Z, inset=car_inset(t) if t > 19.6 else None)], kick=kick(t, [(TWIST, 0.8)]))


def r_ron(t, u):
    Z = 1.6
    cx, cy = 1100.0, 330.0
    def door(big, v_):
        x0, y0 = v_.opt(1112.0, 85.0); x1, y1 = v_.opt(1268.0, 520.0)
        xa, xb, ya, yb = int(max(0, x0)), int(min(OUT_W, x1)), int(max(0, y0)), int(min(OUT_H, y1))
        if xa < xb and ya < yb:
            big[ya:yb, xa:xb] = np.clip(big[ya:yb, xa:xb] * 0.2 + np.array((220, 226, 240)) * 0.8, 0, 255).astype(np.uint8)
    r = ron(t, Z, 1180.0, 545.0, hand_n=(12.0, 50.0))
    g = glenn(t, Z, 960.0, 600.0, flip=False, base=(0.9, 0.0))
    return shot(cx, cy, Z, t, [r, g], pre=door)


def r_aval(t, u):
    Z = 1.25
    cx, cy = 250.0, 360.0
    out = t >= AVAL
    r = ron(t, Z, 230.0 if not out else 300.0, 560.0, hand_n=(-6.0, 34.0))
    g = glenn(t, Z, 420.0, 620.0, base=(-0.9, 0.0), hand_n=(22.0, 70.0))
    acts = [r, g]
    if out:
        p = t - AVAL
        for i in range(14):
            ang = -0.9 + i * 0.12
            sp_ = 260.0 + (i % 4) * 60
            jx = 100.0 + math.cos(ang) * sp_ * p + i * 8
            jy = 380.0 - math.sin(-ang) * sp_ * p + 300 * p * p
            acts.append(K.A(lambda sp, i=i, **kw: C.junk(sp, kind=i), jx, min(jy, 650.0), 7.0 * 3 * Z, rim=None))
        acts.append(K.A(lambda sp, **kw: C.laundry(sp, t=t, w=12.0 + 30 * min(1.0, p * 2), h=6 + 14 * min(1.0, p * 2), seed=7),
                        260.0, 660.0, 6.0 * 3 * Z, rim=None))
    def f(big, v_):
        if not out:
            strain(1.0)(big, v_)
    return shot(cx, cy, Z, t, acts, fx_=f, kick=kick(t, [(AVAL, 1.2)]))


def heads(t, Z, trent_up=True):
    """three heads out of one laundry pile (fixed scale: the pile hides the bodies)"""
    WS = 4.2
    acts = [K.A(C.glenn, 300.0, 520.0 + 91 * WS, WS * 3 * Z, flip=False, **kw_(FG, 'glenn', t, (0.3, 0.3))),
            K.A(C.ron, 520.0, 535.0 + 56 * WS * 1.25, WS * 1.25 * 3 * Z, flip=True, **kw_(FR, 'ron', t, (-0.3, 0.3)))]
    if trent_up:
        rise = sm((t - 27.95) / 0.3)
        acts.append(K.A(C.trent, 410.0, 600.0 + 64 * WS * 1.34 - 90 * rise, WS * 1.34 * 3 * Z, flip=False, **kw_(FT, 'trent', t, (0.0, 0.2))))
    pile = K.A(lambda sp, **kw: C.laundry(sp, t=t, w=52.0, h=24.0, seed=7), 410.0, 720.0, 5.4 * 3 * Z, rim=None)
    pile.near = 0.999
    acts.append(pile)
    return acts


def r_heads(t, u):
    Z = 1.7
    cx, cy = 410.0, 470.0
    return shot(cx, cy, Z, t, heads(t, Z))


def r_pile(t, u):
    Z = 1.15 - 0.1 * glide(u / 4.0)
    cx, cy = 560.0, 400.0
    return shot(cx, cy, Z, t, heads(t, Z) + [monitor(t, Z)])


ST_400 = K.st('400%', fg=(255, 120, 90), size=80)
ST_40 = K.st('40 MIN IN THE DRIVEWAY', fg=(255, 214, 90), size=46)
R = [r_hook, r_laundry, r_sys, r_mont, r_clean, r_monitor, r_ron, r_aval, r_heads, r_pile]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, ['IN-LAWS IN', '1 HOUR?!'], hook_t=(0.10, 2.7), hook_y=1080, hook_size=80,
              stickers=[(ST_40, TWIST + 0.1, 22.4, 540, 1250)],
              flashes=[TWIST, AVAL], mosaics=[MONT],
              cap_y={0: 1580, 1: 1580, 2: 1580, 3: 1580, 4: 1580, 5: 1580, 6: 1600, 7: 1600, 8: 1600, 9: 1600})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
