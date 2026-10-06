"""S01E02 «Талон на талон» — Мазутыч gets his bonus as a fuel coupon («Только не пей сразу»), races to «ГАЗПРОПАЛ»:
«Талоны принимаем. По чётным. — А сегодня? — Нечётное.» He sleeps standing at the window till midnight... and gets
a coupon for a coupon. «А бензин когда? — В четверг. — Какой? — Чётный.» The shutter slams. Дин-Дон: «Такого нет, друга.»
  python3 ep02.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import fx
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
from episode import Episode
from props import mazcast as MC
from props import mazkit as K
from props import bytfx as B
from props import mazshots as M
from props.mazshots import A, wpt, aout, y_far, y_sh, SP
from timeline import DUR, FPS, VOICE, SLUG, CUTS

EPI = Episode('ep02', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
KIT = Kit = M.Kit(EPI)
HW, WIN, GATE = KIT.HW, KIT.WIN, KIT.GATE
mouth = KIT.mouth
NIGHT0, MIDNIGHT = 15.6, 17.2


def night_k(t):
    return sm((t - NIGHT0) / 1.2)


def clock_txt(t):
    if t >= MIDNIGHT: return '00:00'
    k = (t - NIGHT0) / (MIDNIGHT - NIGHT0)
    mins = int(lerp(19 * 60, 23 * 60 + 59, min(1.0, k * 1.15)))
    return f'{mins // 60:02d}:{mins % 60:02d}'


# ================================================================== shots
def r_hook(t, u):
    """the coupon held up against the sunset like a lottery win; tears of joy"""
    def f(big, v, a):
        hx, hy = aout(a, v, 'hand')
        fx.glow(big, hx, hy - 120, 380, (255, 236, 170), 0.35 + 0.1 * math.sin(t * 8))
    return KIT.cu_maz(t, u, world=GATE, cx=1000.0, cy=400.0, sz=15.5 + 1.0 * u, head=(480, 1020), light=K.light_gate, flare=(1105, 60),
                      expr='joy', card='talon', look=(0.8, 0.8), beacon=True, extra_fx=f, wind=0.3)


def r_boss(t, u):
    """the gate: Борис Борисыч slaps his shoulder — «Только не пей сразу»"""
    Z = 2.2
    b = A(MC.boss, 610.0, 640.0, SP * Z, t=t, pose='pat' if 0.2 < u < 2.6 else 'stand', mouth_=mouth('boss', t), expr='grin', look=(1.0, 0.0))
    m = KIT.maz_act(t, 710.0, 640.0, Z, flip=True, expr='proud' if u < 2.2 else 'deadpan', card='talon', look=(1.0, 0.0), beacon=True)
    def pre(big, v): K.flare(big, v, t, 1105, 60, 1.2, 1.0)
    big = K.shot(GATE, K.light_gate, 660.0, 560.0, Z, acts=[b, m], pre=pre, sx=180, sy=400)
    if 0.3 < u < 0.5: B.shake(big, t, 6, 30)
    return big


def r_cross(t, u):
    """crossing past the queue with the coupon raised like a flag"""
    Z = 1.15
    x = 260.0 + 300.0 * u / 2.4
    acts = KIT.queue_acts(t, Z, 1.0 if t > 7.3 else 0.0) + [KIT.maz_act(t, x, y_sh(x), Z, expr='proud', card='talon', wind=1.0, spin=t * 20,
                                                                         rot=-8.0, beacon=True, shadow=0.3)]
    def f(big, v):
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
        K.dust_trail(big, v, t, x - 10, y_sh(x) - 4)
        fx.speed_lines(big, t, 0.5)
    return K.shot(HW, K.light_hw, x + 40.0, 470.0, Z, acts=acts, fx_=f, sx=180, sy=330)


def r_slap(t, u):
    big = KIT.cu_maz(t, u, cx=900.0, cy=330.0, sz=15.5, head=(470, 900), expr='proud', card='talon', look=(1.0, 0.0), beacon=True)
    if 0.05 < u < 0.3: B.shake(big, t, 9, 30)
    return big


def r_zoya1(t, u):
    return KIT.zoya(t, u, gum=0.0, look=(1.0, -0.1))


def r_hope(t, u):
    return KIT.cu_maz(t, u, cx=900.0, cy=330.0, sz=16.0, head=(540, 960), expr='awe', card='talon', look=(1.0, 0.1), mouth_=None or mouth('maz', t, 1.6))


def r_zoya3(t, u):
    return KIT.zoya(t, u, Z0=1.6, push=0.1, gum=sm((t - 15.25) / 0.2) * (1 - sm((t - 15.45) / 0.05)), look=(1.0, 0.0))


def window_with_maz(t, u, expr='sleepy', lights=False, dk=1.0, zz=True, mz=0.0, flip=False):
    """the kiosk at night, Мазутыч standing asleep on his wheel in the foreground left"""
    m = A(MC.maz, 545.0, 556.0, SP * 2.6, t=t, expr=expr, mouth_=mz, blink=False, beacon=False, wheel_face='smile', card='talon')
    def extra(big, v):
        m(big, v, K.light_win(v))
    big = KIT.zoya(t, u, Z0=1.3, push=0.0, lights=lights, dark=0.0, extra=extra)
    M.night(big, 0.7 * dk, moon=(880, 230))
    return big, m


def r_timelapse(t, u):
    big, m = window_with_maz(t, u, dk=night_k(t))
    M.zzz(big, 560, 640, t)
    M.digital_clock(big, clock_txt(t), 540, 330)
    return big


def r_wake(t, u):
    """midnight: the window lights up, he wakes — «Чётное!»"""
    def pre(big, v):
        pass
    big = KIT.cu_maz(t, u, world=WIN, cx=618.0, cy=300.0, sz=15.5, head=(560, 980), light=K.light_win, flare=None, expr='joy',
                     card='talon', look=(1.0, 0.3), beacon=True)
    M.night(big, 0.75)
    fx.glow(big, 960, 700, 700, (255, 220, 150), 0.45)
    M.digital_clock(big, '00:00', 540, 260, 110)
    return big


def r_stamp(t, u):
    """insert: Зоя stamps the coupon «ПОГАШЕН»"""
    big = KIT.zoya(t, u, Z0=1.5, push=0.0, dark=0.45, look=(0.0, -1.0))
    k = sm(min(1.0, (t - 18.52) / 0.08))
    M.paper(big, 540, 1050, ['ТАЛОН', 'НА 10 Л', 'БЕНЗИНА'], w=560, h=360, rot=-4, stamp='ПОГАШЕН' if t >= 18.52 else None, stamp_k=k,
            col=(250, 214, 214), sizes=[56, 40, 40])
    if 18.52 <= t < 18.7: B.shake(big, t, 10, 30)
    return big


def r_talon2(t, u):
    """the twist: a tiny new slip — «ТАЛОН НА ТАЛОН»"""
    big = KIT.zoya(t, u, Z0=1.55, push=0.05, dark=0.45, look=(1.0, 0.0))
    s = 0.6 + 0.4 * sm(u / 0.3)
    M.paper(big, 640, 1180, ['ТАЛОН', 'НА ТАЛОН', 'ЧЕТВЕРГ'], w=int(300 * s), h=int(200 * s), rot=6, col=(214, 236, 250),
            sizes=[int(30 * s), int(24 * s), int(18 * s)])
    return big


def maz_night(t, u, expr, **kw):
    big = KIT.cu_maz(t, u, world=WIN, cx=618.0, cy=300.0, sz=16.0, head=(540, 960), light=K.light_win, flare=None, expr=expr, **kw)
    M.night(big, 0.55)
    fx.glow(big, 1000, 760, 600, (255, 220, 150), 0.3)
    return big


def r_when(t, u):
    return maz_night(t, u, 'stunned', look=(1.0, 0.0), card='talon')


def r_thursday(t, u):
    return KIT.zoya(t, u, Z0=1.6, push=0.05, dark=0.45, look=(1.0, 0.0))


def r_which(t, u):
    return maz_night(t, u, 'squint', look=(1.0, 0.0))


def r_shutter(t, u):
    """«Чётный.» — and the iron shutter slams down"""
    k = sm((t - 26.4) / 0.55)
    big = KIT.zoya(t, u, Z0=1.45, push=0.0, dark=0.0, look=(1.0, 0.0), extra=lambda b, v: KIT.shutter(b, v, k))
    M.night(big, 0.45)
    if 26.95 <= t < 27.2: B.shake(big, t, 12, 30)
    return big


def r_wheel(t, u):
    """Мазутыч in front of the shut kiosk, the wheel's display speaks: «Такого нет, друга.»"""
    def pre(big, v): KIT.shutter(big, v, 1.0)
    big = KIT.cu(MC.maz, 'maz', t, u, WIN, 618.0, 300.0, sz=10.0, head=(560, 820), light=K.light_win, flare=None, pre_fx=pre,
                 expr='deadpan', look=(0.0, -0.4), mouth_=0.0, card='talon', wheel_face='low' if t > 27.5 else 'smile')
    M.night(big, 0.5)
    return big


def r_notice(t, u):
    def f(big, v): KIT.shutter(big, v, 1.0)
    big = K.shot(WIN, K.light_win, 618.0, 330.0, 1.6 + 0.08 * u, pre=f, sx=180, sy=320)
    M.night(big, 0.45)
    return big


SHOTS = [r_hook, r_boss, r_cross, r_slap, r_zoya1, r_hope, r_zoya3, r_timelapse, r_wake, r_stamp, r_talon2, r_when, r_thursday, r_which,
         r_shutter, r_wheel, r_notice]
NAMES = ['hook', 'boss', 'cross', 'slap', 'zoya1', 'hope', 'zoya3', 'timelapse', 'wake', 'stamp', 'talon2', 'when', 'thursday', 'which',
         'shutter', 'wheel', 'notice']
CAP = dict(boss=1080, cross=1080, zoya1=1640, zoya3=1640, stamp=1640, talon2=1640, thursday=1640, shutter=1640, timelapse=1500,
           wheel=1600)

SHOW = K.Show(EPI, 2, ['ПРЕМИЯ —', 'ТАЛОНОМ'], hook_t=(0.10, 2.8), hook_y=120, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('ТАЛОН!', (255, 160, 190)), 7.0, 8.9, 760, 1180),
                        (K.st('ТАЛОН НА ТАЛОН', (90, 230, 255), 52), 19.4, 21.6, 540, 420)],
              flashes=[17.2, 18.52], mosaics=[15.6])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
