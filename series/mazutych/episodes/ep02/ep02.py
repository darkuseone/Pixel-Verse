"""S01E02 v2 «Талон на талон» (08.10.2026, по статистике TikTok): hook = outcry of a pain everyone knows — «Премия — талоном?!»
(the coupon right in the frame). «Только не пей сразу.» He races past the queue: «У меня талон!» — every car window pops up the
same coupon: «У всех талон, друга.» «Талоны — по чётным. — А сегодня? — Нечётное.» He sleeps standing till midnight — «Чётное!» —
twist (59 %): stamp «ПОГАШЕН», a coupon for a coupon. «А бензин когда? — В четверг. — Какой? — Чётный.» Shutter. Дин-Дон:
«Такого нет, друга.» Loop: next morning the boss hands him a new coupon → back to the first outcry.
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
from timeline import DUR, FPS, VOICE, SLUG, CUTS, TWIST, NIGHT0, MIDNIGHT, STAMP_T, SHUT_T

EPI = Episode('ep02', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
KIT = Kit = M.Kit(EPI)
HW, WIN, GATE = KIT.HW, KIT.WIN, KIT.GATE
mouth = KIT.mouth


def night_k(t):
    return sm((t - NIGHT0) / 0.6)


def clock_txt(t):
    if t >= MIDNIGHT: return '00:00'
    k = (t - NIGHT0) / (MIDNIGHT - NIGHT0)
    mins = int(lerp(19 * 60, 23 * 60 + 59, min(1.0, k * 1.15)))
    return f'{mins // 60:02d}:{mins % 60:02d}'


# ================================================================== shots
def coupon(big, t, x, y, k=1.0, rot=-8.0):
    """the bonus itself, readable in 1 s: a pink coupon «ТАЛОН · 10 Л»"""
    M.paper(big, int(x), int(y), ['ТАЛОН', '10 Л', 'ПРЕМИЯ'], w=int(400 * k), h=int(270 * k), rot=rot + 2 * math.sin(t * 9),
            col=(250, 200, 210), sizes=[int(64 * k), int(48 * k), int(30 * k)])


def r_hook(t, u):
    """0.0: outcry — the bonus is a coupon; the coupon itself shoved at the lens"""
    big = KIT.cu_maz(t, u, world=GATE, cx=1000.0, cy=400.0, sz=16.5 + 0.8 * u, head=(640, 880), light=K.light_gate, flare=(1105, 60),
                     expr='shock', look=(0.6, 0.8), beacon=True, wind=0.6)
    coupon(big, t, 520, 1420, 1.0 + 0.06 * u)
    if u < 0.35: B.shake(big, t, 10, 30)
    return big


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


def r_coupons(t, u):
    """visual punch: from every car window in the queue the same pink coupon pops up and waves"""
    Z = 1.55
    q = [(600, 'lada', 0), (700, 'lada', 2), (800, 'lada', 3)]
    acts = KIT.queue_acts(t, Z, 1.0 if u > 0.3 else 0.0, xs=q)
    def f(big, v):
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
        for i, (x, _, _) in enumerate(q):
            k = sm((u - 0.12 - 0.28 * i) / 0.12)
            if k <= 0: continue
            wx, wy = v.opt(x + 8, y_far(x) - 44)
            hy = wy - 130 * k
            big[int(hy):int(wy), int(wx) - 16:int(wx) + 16] = (214, 160, 120)              # the arm out of the window
            M.paper(big, int(wx), int(hy - 90), ['ТАЛОН', '10 Л'], w=230, h=160, rot=8 * math.sin(t * 10 + i), col=(250, 200, 210),
                    sizes=[44, 34])
    return K.shot(HW, K.light_hw, 700.0, 520.0, Z, acts=acts, fx_=f, sx=180, sy=360)


def r_zoya1(t, u):
    return KIT.zoya(t, u, gum=0.0, look=(1.0, -0.1))


def r_hope(t, u):
    return KIT.cu_maz(t, u, cx=900.0, cy=330.0, sz=16.0, head=(540, 960), expr='awe', card='talon', look=(1.0, 0.1), mouth_=None or mouth('maz', t, 1.6))


def r_zoya3(t, u):
    return KIT.zoya(t, u, Z0=1.6, push=0.1, gum=sm((t - 14.15) / 0.2) * (1 - sm((t - 14.35) / 0.05)), look=(1.0, 0.0))


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
    k = sm(min(1.0, (t - STAMP_T) / 0.08))
    M.paper(big, 540, 1050, ['ТАЛОН', 'НА 10 Л', 'БЕНЗИНА'], w=560, h=360, rot=-4, stamp='ПОГАШЕН' if t >= STAMP_T else None, stamp_k=k,
            col=(250, 214, 214), sizes=[56, 40, 40])
    if STAMP_T <= t < STAMP_T + 0.18: B.shake(big, t, 10, 30)
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
    k = sm((t - SHUT_T) / 0.5)
    big = KIT.zoya(t, u, Z0=1.45, push=0.0, dark=0.0, look=(1.0, 0.0), extra=lambda b, v: KIT.shutter(b, v, k))
    M.night(big, 0.45)
    if SHUT_T + 0.5 <= t < SHUT_T + 0.75: B.shake(big, t, 12, 30)
    return big


def r_wheel(t, u):
    """Мазутыч in front of the shut kiosk, the wheel's display speaks: «Такого нет, друга.»"""
    def pre(big, v): KIT.shutter(big, v, 1.0)
    big = KIT.cu(MC.maz, 'maz', t, u, WIN, 618.0, 300.0, sz=10.0, head=(560, 820), light=K.light_win, flare=None, pre_fx=pre,
                 expr='deadpan', look=(0.0, -0.4), mouth_=0.0, card='talon', wheel_face='low' if t > 25.9 else 'smile')
    M.night(big, 0.5)
    return big


def r_loop(t, u):
    """loop: next morning at the gate the boss slaps a NEW coupon into his hand → back to the first outcry"""
    Z = 2.2
    b = A(MC.boss, 610.0, 640.0, SP * Z, t=t, pose='pat' if u < 0.9 else 'stand', mouth_=0.0, expr='grin', look=(1.0, 0.0))
    m = KIT.maz_act(t, 710.0, 640.0, Z, flip=True, expr='deadpan', look=(1.0, 0.0), beacon=True, mouth_=0.0)
    def pre(big, v): K.flare(big, v, t, 1105, 60, 1.2, 1.0)
    big = K.shot(GATE, K.light_gate, 660.0, 560.0, Z + 0.15 * u, acts=[b, m], pre=pre, sx=180, sy=400)
    coupon(big, t, lerp(300, 640, sm(u / 0.4)), lerp(700, 1080, sm(u / 0.4)), 0.8)
    return big


SHOTS = [r_hook, r_boss, r_cross, r_coupons, r_zoya1, r_hope, r_zoya3, r_timelapse, r_wake, r_stamp, r_talon2, r_when, r_thursday,
         r_which, r_shutter, r_wheel, r_loop]
NAMES = ['hook', 'boss', 'cross', 'coupons', 'zoya1', 'hope', 'zoya3', 'timelapse', 'wake', 'stamp', 'talon2', 'when', 'thursday',
         'which', 'shutter', 'wheel', 'loop']
CAP = dict(hook=1760, boss=1640, cross=1080, coupons=1640, zoya1=1640, zoya3=1640, stamp=1640, talon2=1640, thursday=1640,
           shutter=1640, timelapse=1500, wheel=1600, loop=1640)

SHOW = K.Show(EPI, 2, ['ПРЕМИЮ ДАЛИ', 'ТАЛОНОМ?!'], hook_t=(0.10, 2.4), hook_y=120, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('ТАЛОН!', (255, 160, 190)), 5.6, 7.2, 760, 520),
                        (K.st('ТАЛОН НА ТАЛОН', (90, 230, 255), 52), 17.7, 19.9, 540, 420)],
              flashes=[TWIST, CUTS[-2]], mosaics=[NIGHT0])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
