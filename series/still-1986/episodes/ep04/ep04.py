"""S01E04 «DROP DAY» (≈36 s, twist at 60 %: the villain is your own — the disguised guy in front of Vince in the midnight launch line is
his boss Gary, who also called in sick). Main question: can Vince skip work for the drop without getting caught?
Clue in the first half: the man in the fedora is on the phone exactly when «Gary» answers Vince's sick call.
  python3 ep04.py test 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common as CM
import math
import numpy as np
import fx
import atmos as AT
import overlays as O
import stage as ST
from stage import OUT_W, OUT_H
from scene import sm, lerp
from cam25 import glide, kick
from episode import Episode
from props import v86cast as C, v86kit as K
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, T, E, RING, GATE

EPI = Episode('ep04', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='v86', lang='us', promise='TOMORROW: THE ROOF'))
FACE = CM.Faces(EPI, dict(
    vince=[(0.0, 'nervous'), (T['g1'], 'smooth'), (T['v2'], 'scheming'), (T['v3'], 'smooth'), (RING, 'cool'), (TWIST, 'shock'),
           (CUTS[8], 'nervous'), (T['v5'], 'smooth')],
    gary=[(0.0, 'smug'), (T['g3'], 'nervous'), (TWIST, 'shock'), (T['g5'], 'nervous')]))
WS = K.WS['mall']
GY, VY = (700.0, 622.0), (548.0, 628.0)
FRAN_W, FRAN_H = (712.0, 150.0), 140.0


def gary_act(v, t, s=None, flip=False, **kw):
    k, dy = FACE('gary', t, (-0.8 if flip else 0.8, 0.0))
    k.update(kw)
    so = sm((t - TWIST - 0.1) / 0.5) if t > TWIST else 0.0
    return K.A(C.gary, GY[0], GY[1] + dy * 2, s or K.S_of(v, 'mall'), t=t, flip=flip, stache_off=so, **k)


def vince_act(v, t, s=None, flip=False, **kw):
    k, dy = FACE('vince', t, (-0.8 if flip else 0.8, 0.0), **kw)
    return K.A(C.vince, VY[0], VY[1] + dy * 2, s or K.S_of(v, 'mall'), t=t, flip=flip, **k)


def line_crowd(big, t, y0=1350, y1=1520):
    K.crowd(big, t, y0, y1, n=7, seed=11, sunglasses=True, dance=0.1, h=(380, 460), x0=-60, x1=420)


def vince_cu(t, head, s, base=(0.8, 0.0), kick_=(0, 0), cx=560.0, cy=420.0, **kw):
    k, dy = FACE('vince', t, base, **kw)
    big, a, v = CM.cu('mall', K.light_mall, C.vince, t, cx, cy, 1.3, (head[0], head[1] + dy * 10), s, k, kick=kick_)
    return big


# ================================================================== shots
def r_hook(t, u):
    return vince_cu(t, (430, 930), 16.0, (0.9, 0.2), hand_n=(10.0, 70.0), prop_n=lambda sp, h: C.phone(sp, h),
                    sweat=1.0, kick_=kick(t, [(1.2, 0.4), (2.4, 0.4)]))


def r_line(t, u):
    Z = 1.12
    cx = lerp(560.0, 600.0, u / 2.5)
    v = K.V('mall', cx, 420.0, Z)
    acts = [vince_act(v, t, hand_n=(10.0, 70.0), prop_n=lambda sp, h: C.phone(sp, h)), gary_act(v, t, phone_ear=True)]
    def pre(big, _): line_crowd(big, t)
    big = K.shot('mall', K.light_mall, cx, 420.0, Z, acts=acts, pre=pre, t=t, dof_k=12, bokeh_=True)
    O.draw_sticker(big, ST_CLUE, t, T['g1'] + 0.6, CUTS[2], 540, 360)
    return big


def r_fran(t, u):
    Z = 1.45
    v = K.V('mall', 640.0, 200.0, Z)
    def pre(big, _): big[:] = K.blur(big, 7)
    def f(big, _): K.fran(big, 560, 1400, 1040, t, talk=CM.M.mouth(EPI.talk, 'fran', t), lid=0.6, look=-0.4)
    return K.shot('mall', K.light_mall, 640.0, 200.0, Z * (1 + 0.012 * u), pre=pre, dof_k=0, fx_=f, t=t, bloom=(200, 30, 0.7))


def two(t, u, Z=1.55, cx=630.0, cy=500.0, gkw=None, vkw=None, fx_=None):
    v = K.V('mall', cx, cy, Z)
    acts = [vince_act(v, t, **(vkw or {})), gary_act(v, t, **(gkw or {}))]
    def pre(big, _): line_crowd(big, t, 1500, 1700)
    return K.shot('mall', K.light_mall, cx, cy, Z, acts=acts, pre=pre, fx_=fx_, t=t, dof_k=14, bokeh_=True)


def r_whisper(t, u):
    return two(t, u, vkw=dict(lean=0.8, hand_f=(-6.0, 60.0)))


def r_call(t, u):
    return vince_cu(t, (470, 960), 18.0, (0.9, 0.2), hand_n=(12.0, 68.0), prop_n=lambda sp, h: C.phone(sp, h), glint=1.0 if u > 1.5 else 0.0)


def r_ring(t, u):
    ring = u < 1.2
    def f(big, v):
        if ring:
            for i in range(3):                                               # ringing waves from Gary's pocket
                r = 40 + ((t * 3 + i / 3) % 1.0) * 140
                fx.glow(big, 760, 1300, int(r), (255, 214, 80), 0.25 * (1 - ((t * 3 + i / 3) % 1.0)))
    return two(t, u, Z=1.7, cx=640.0, cy=520.0, gkw=dict(phone_ear=u > 1.0), vkw=dict(hand_n=(12.0, 68.0), prop_n=lambda sp, h: C.phone(sp, h)),
               fx_=f)


def r_twist(t, u):
    Z = 2.3
    v = K.V('mall', 700.0, 470.0, Z)
    g = gary_act(v, t, flip=True, phone_ear=False)
    g.near = 0.99
    big = K.shot('mall', K.light_mall, 700.0, 470.0, Z, acts=[g], t=t, dof_k=20, bokeh_=True, kick=kick(t, [(TWIST + 0.1, 1.2)]))
    O.draw_sticker(big, ST_GARY, t, TWIST + 0.1, CUTS[7], 540, 360)
    return big


def r_gary(t, u):
    Z = 2.6
    v = K.V('mall', 700.0, 450.0, Z)
    g = gary_act(v, t, flip=True)
    g.near = 0.99
    def f(big, _): AT.sparks(big, 640, 600, t, T['g4'] + 0.1, n=12, col=(255, 230, 120), seed=2, life=0.5, speed=500, px=8)
    return K.shot('mall', K.light_mall, 700.0, 450.0, Z, acts=[g], fx_=f, t=t, dof_k=20, kick=kick(t, [(T['g4'] + 0.05, 1.0)]))


def r_office(t, u):
    Z = 1.0
    cx = lerp(620.0, 520.0, glide(u / 1.4))
    v = K.V('mall', cx, 420.0, Z)
    acts = [vince_act(v, t, flip=True), gary_act(v, t, flip=True)]
    def pre(big, _):
        K.crowd(big, t, 1280, 1500, n=12, seed=5, sunglasses=True, dance=0.05, h=(330, 420), x0=-40, x1=700,
                cols=((255, 214, 80), (255, 140, 60)))
    def f(big, _): K.fran(big, 880, 640, 360, t, talk=CM.M.mouth(EPI.talk, 'fran', t), lid=0.6, look=-0.6)
    big = K.shot('mall', K.light_mall, cx, 420.0, Z, acts=acts, pre=pre, fx_=f, t=t, dof_k=12)
    O.draw_sticker(big, ST_OFFICE, t, T['f2'] - 0.4, CUTS[9], 540, 360)
    return big


def r_gate(t, u):
    Z = 1.15
    v = K.V('mall', 560.0, 420.0, Z)
    acts = [vince_act(v, t, lean=-0.4), gary_act(v, t, flip=True, hand_n=(-4.0, 48.0))]
    def pre(big, _):
        k = sm(u / 0.6)
        fx.glow(big, 600, 1250, int(300 + 300 * k), (255, 255, 230), 0.5 * k)
        K.crowd(big, t, 1300, 1560, n=10, seed=9, sunglasses=True, dance=1.6, h=(300, 380), x0=-100, x1=1180)
    big = K.shot('mall', K.light_mall, 560.0, 420.0, Z, acts=acts, pre=pre, t=t, dof_k=12, kick=kick(t, [(GATE + 0.2, 0.8)]))
    O.draw_sticker(big, ST_0000, t, GATE + 0.1, CUTS[10], 540, 360)
    return big


def r_deal(t, u):
    return vince_cu(t, (470, 960), 18.0, (0.8, -0.2), sparkle=1.0, glint=1.0 if u > 1.0 else 0.0, prop_n=lambda sp, h: C.cash(sp, h),
                    hand_n=(24.0, 70.0))


def r_button(t, u):
    return r_fran(t, u)


ST_CLUE = K.st('ON THE PHONE TOO...', fg=(255, 214, 80), size=46)
ST_GARY = K.st('BOSS?!', fg=(255, 110, 200), size=96)
ST_OFFICE = K.st('THE WHOLE OFFICE', fg=(255, 214, 80), size=50)
ST_0000 = K.st('00:00 — THE DROP', fg=(90, 236, 255), size=58)
R = [r_hook, r_line, r_fran, r_whisper, r_call, r_ring, r_twist, r_gary, r_office, r_gate, r_deal, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 4, ['SICK', 'DAY?'], hook_t=(0.10, 2.6), hook_y=250, hook_size=110,
              stickers=[(K.st('GAME FUND: -$416', fg=(90, 236, 255), size=46), T['v5'], CUTS[11], 540, 330)],
              flashes=[TWIST, T['g4'], GATE + 0.1], mosaics=[CUTS[8]],
              cap_y={0: 1500, 1: 1180, 2: 1520, 3: 1180, 4: 1500, 5: 1180, 6: 1560, 7: 1560, 8: 1600, 9: 1640, 10: 1500, 11: 1520})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
