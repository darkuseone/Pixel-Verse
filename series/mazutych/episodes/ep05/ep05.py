"""S01E05 v2 «Биотопливо» (08.10.2026: after the twist the boss cuts the queue — «Начальству — без очереди!»). BOOM: the garage doors fly off, sooty Мазутыч in the smoke: «Почти получилось.» VHS rewind «2 часа
назад»: a rig from a samovar and a pressure cooker, sunflower husks. «Лузга. Давление. Наука.» Толик: «Одну тебе, одну мне.»
A golden drop — «Капает!» — the old «six» over the pit starts: «Завелась, родимая!» Twist: the doors open — the whole district
queues to his garage, Зоя on the roof with a megaphone: «Бензина нет! Ждём семечки!» «Кто крайний?» — «Это мой гараж!»
Дин-Дон: «Давление много, друга.» BOOM — back to the first frame (loop).
  python3 ep05.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import fx
import overlays as O
from stage import view_at, OUT_W, OUT_H, Light
from scene import sm, lerp
from episode import Episode
from props import mazcast as MC
from props import mazkit as K
from props import bytfx as B
from props import mazshots as M
from props.mazshots import A, wpt, aout, SP, CAR
from timeline import DUR, FPS, VOICE, SLUG, CUTS

EPI = Episode('ep05', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
KIT = M.Kit(EPI)
mouth = KIT.mouth
GAR = K.world('garages')
GI = K.world('garage_inside')
DOOR1 = (35, 270, 295, 560)                      # Мазутыч's garage in the cooperative
RIG = (440.0, 660.0)                             # the still on the garage floor, left of the pit
CAR_X, CAR_Y = 673.0, 545.0                      # the «six» seen from behind, wheels on the far edges of the inspection pit
CAR_R = 15.9                                     # rear-view car scale (output px per sprite px at Z = 1): track = the pit width
PS = 1.9                                         # people / rig scale in the garage (so they match the real-size car)


def car_rear(t, Z, shake=0.0, lights=0.0):
    return A(MC.lada_rear, CAR_X, CAR_Y, CAR_R * Z, t=t, shake=shake, lights=lights)


def light_gi(v):
    return Light(amb=(1.0, 0.92, 0.82), keys=K._keys(v, ((440, 170, 700, (255, 210, 120), 0.6),)), rim=(-1, -0.4, (255, 200, 120), 0.4),
                 grad=(1.04, 0.86))


def light_gar(v):
    return Light(amb=(0.86, 0.84, 1.02), keys=K._keys(v, ((1120, 190, 700, (255, 200, 120), 0.55),)), rim=(1, -0.4, (255, 190, 120), 0.45),
                 grad=(1.02, 0.88))


def blown_world(open_=1.0, light=False):
    """the cooperative with Мазутыч's garage doors blown off (dark smoky hole) or swung open with warm light inside"""
    W = GAR.copy()
    x0, y0, x1, y1 = DOOR1
    if light:
        yy = np.linspace(0, 1, y1 - y0)[:, None, None]
        W[y0:y1, x0:x1] = (np.array([200, 150, 80]) * (1 - yy) + np.array([110, 80, 50]) * yy).astype(np.uint8)
    else:
        W[y0:y1, x0:x1] = (24, 20, 22)
        W[y1 - 6:y1 + 8, x0 - 30:x1 + 40] = (70, 66, 70)                         # the door leaves on the ground
    return W


def smoke(big, v, t, x, y, n=7, a=0.6, col=(90, 86, 92), rise=180):
    for i in range(n):
        ph = (t * 0.6 + i / n) % 1.0
        ox, oy = v.opt(x + math.sin(i * 2.3 + t) * 40, y - ph * rise)
        B.puff(big, ox, oy, (40 + 80 * ph) * 3 * v.Z, a * (1 - ph), col)


def r_boom(t, u, again=False):
    """sooty Мазутыч in the blown-open doorway, smoke, the mustache smoking"""
    W = blown_world()
    t0 = CUTS[12] if again else 0.0
    Z = 2.6 + 0.08 * u
    soot_maz = KIT.maz_act(t, 170.0, 600.0, Z, expr='deadpan', soot=0.78, mouth_=mouth('maz', t), look=(0.0, -0.3), beacon=False, ride=False,
                           hold=False, wheel=False, blink=False)
    tol = A(MC.tolik, 255.0, 596.0, SP * Z, t=t, expr='stunned', mouth_=0.0, look=(-1.0, 0.0), post=lambda sp: sp.soot(0.7))
    def f(big, v):
        smoke(big, v, t, 165, 420, a=0.32)
        smoke(big, v, t * 1.3, 175, 330, n=4, a=0.25, col=(60, 58, 62), rise=120)
        if u < 0.25:
            ox, oy = v.opt(165, 420)
            fx.glow(big, ox, oy, 900, (255, 200, 120), 0.5 * (1 - u / 0.25))
    big = K.shot(W, light_gar, 205.0, 560.0, Z, acts=[tol, soot_maz], fx_=f, sx=180, sy=440)
    if u < 0.5: B.shake(big, t, 14 * (1 - u / 0.5), 30)
    return big


def pit_lamp(big, v, t):
    """a work lamp glowing down in the inspection pit: the car clearly stands OVER the pit"""
    x, y = v.opt(CAR_X + 20, 600)
    fx.glow(big, x, y, 260 * v.Z, (255, 214, 130), 0.35 + 0.05 * math.sin(t * 7))


def interior(t, Z, cx, cy, acts, fx_=None):
    def f(big, v):
        pit_lamp(big, v, t)
        if fx_: fx_(big, v)
    return K.shot(GI, light_gi, cx, cy, Z, acts=acts, fx_=f, sx=180, sy=380)


def rig_act(t, sz, shake=0.0, gauge=0.2, level=0.0, drop=-1.0):
    return A(MC.still, RIG[0], RIG[1], sz, t=t, shake=shake, gauge=gauge, level=level, drop=drop)


def r_rewind(t, u):
    big = r_lab(t, 0.0)
    fx.vhs(big, t, 1.0)
    return big


def r_lab(t, u):
    """the garage lab: the rig, the «six» standing over the pit, Мазутыч presenting like a professor"""
    Z = 0.8
    acts = [car_rear(t, Z), rig_act(t, SP * Z * 1.1 * PS),
            A(MC.tolik, 315.0, 720.0, SP * Z * PS, t=t, expr='grin', mouth_=0.0, look=(1.0, 0.0)),
            KIT.maz_act(t, 575.0, 722.0, Z, sz=SP * Z * PS, flip=True, expr='proud', ride=False, hold=False, wheel=False,
                        blinker=1.0 if u > 1.2 else 0.0, look=(1.0, 0.0))]
    return interior(t, Z + 0.04 * u, 505.0, 430.0, acts)


def r_seeds(t, u):
    """Толик throws one seed in the rig and one in his mouth"""
    big = KIT.cu(MC.tolik, 'tolik', t, u, GI, 300.0, 420.0, sz=16.0, head=(540, 940), light=light_gi, flare=None, expr='grin',
                 look=(-1.0, 0.0), flip=True)
    r = np.random.default_rng(int(t * 10))
    for i in range(8):
        ph = (t * 1.6 + i / 8) % 1.0
        x, y = int(260 + i * 20 + ph * 30), int(1100 + ph * 600)
        big[y:y + 18, x:x + 12] = (230, 228, 210) if i % 2 else (40, 36, 30)
    return big


def r_drip(t, u):
    """insert: one golden drop falls into the jar — the choir"""
    d = (t - 9.55) / 0.35
    lvl = 0.06 if t > 9.9 else 0.0
    sz = 24.0
    v0 = view_at(GI, RIG[0] + 30, 420.0, 1.45, 180, 320)
    jx, jy = wpt(v0, 600, 1150)
    a = A(MC.still, jx, jy, sz, pin='jar', t=t, level=lvl, drop=d if 0 <= d <= 1 else -1.0, gauge=0.5)
    def pre(big, v): big[:] = M.dof(big, 8)
    big = K.shot(GI, light_gi, RIG[0] + 30, 420.0, 1.45, acts=[a], pre=pre, sx=180, sy=320)
    if t > 9.9:
        fx.glow(big, 600, 1150, 320, (255, 220, 110), 0.5)
    return big


def r_pour(t, u):
    return KIT.cu(MC.maz, 'maz', t, u, GI, 520.0, 420.0, sz=16.0, head=(540, 960), light=light_gi, flare=None, expr='joy', ride=False,
                  wheel=False, hold=False, look=(-1.0, 0.0), beacon=True)


def r_start(t, u):
    """the «six» over the pit coughs, shakes and roars to life: smoke from the exhaust straight at us, tail lights flare"""
    Z = 1.0 + 0.12 * u
    on = t > 12.9
    car = car_rear(t, Z, shake=1.0 if on else 0.35, lights=1.0 if on else 0.0)
    def f(big, v):
        ex, ey = M.aout(car, v, 'exhaust')
        for i in range(7):
            ph = (t * 2.2 + i / 7) % 1.0
            B.puff(big, ex - ph * 120 + 40 * math.sin(i), ey + ph * 160, (24 + 70 * ph) * 3, 0.65 * (1 - ph), (80, 76, 80))
    return interior(t, Z, CAR_X, 400.0, [car], f)


def r_dance(t, u):
    """Толик dances by the running car"""
    Z = 2.2
    rot = 12.0 * math.sin(t * 9)
    hop = abs(math.sin(t * 9)) * 6
    Z = 1.15
    car = car_rear(t, Z, shake=1.0, lights=1.0)
    tol = A(MC.tolik, 900.0, 730.0 - hop, SP * Z * PS, t=t, expr='cheer', mouth_=mouth('tolik', t), rot=rot, look=(-1.0, 0.0), flip=True)
    big = interior(t, Z, 790.0, 460.0, [car, tol])
    K.confetti(big, t, 13.75, n=60, seed=2)
    return big


QUEUE5 = [(420, 0), (545, 2), (670, 3), (795, 1), (920, 4), (1045, 5), (1170, 2)]


def r_queue(t, u):
    """twist: the doors swing open — a queue of cars down the alley; Зоя on the garage roof with a megaphone"""
    W = blown_world(light=True)
    Z = 1.05
    acts = [A(MC.lada, x, 655.0, CAR * Z * 0.95, col=MC.CAR_COLS[c], rust=i + 1, honk=1.0) for i, (x, c) in enumerate(QUEUE5)]
    acts.append(A(MC.lada, 250.0, 652.0, CAR * Z, col=(232, 228, 214), driver=False))
    acts.append(A(MC.zoya, 215.0, 268.0, SP * Z * 0.95, t=t, mega=True, mouth_=mouth('zoyam', t), expr='bored', look=(1.0, 0.0)))
    def f(big, v):
        ox, oy = v.opt(165, 420)
        fx.glow(big, ox, oy, 520, (255, 200, 120), 0.4)
    return K.shot(W, light_gar, 330.0 + 40 * u, 470.0, Z, acts=acts, fx_=f, sx=180, sy=360)


def r_last(t, u):
    """the boss shoulders through the queue with an empty red canister: «Начальству — без очереди!»"""
    big = KIT.cu(MC.boss, 'boss', t, u, blown_world(light=True), 600.0, 400.0, sz=16.5, head=(520, 900), light=light_gar,
                 flare=(1170, 170), expr='smug', pose='stand', look=(1.0, 0.0), pan=-30.0)
    cx, cy = 780, 1420 + int(8 * math.sin(t * 10))                      # the empty canister under his arm
    big[cy - 170:cy + 170, cx - 130:cx + 130] = (30, 20, 16)
    big[cy - 160:cy + 160, cx - 120:cx + 120] = (196, 36, 40)
    big[cy - 120:cy + 120, cx - 80:cx + 80] = (170, 28, 34)
    big[cy - 230:cy - 160, cx - 60:cx + 60] = (30, 20, 16); big[cy - 220:cy - 170, cx - 40:cx + 40] = (196, 36, 40)
    big[cy - 230:cy - 200, cx + 70:cx + 120] = (230, 200, 60)
    return big


def r_mine(t, u):
    big = KIT.cu(MC.maz, 'maz', t, u, blown_world(light=True), 520.0, 400.0, sz=16.0, head=(560, 960), light=light_gar, flare=(1170, 170),
                 expr='angry', ride=False, wheel=False, hold=False, look=(1.0, 0.0), blinker=1.0, wind=0.2)
    return big


def r_pressure(t, u):
    """the rig shakes, the needle in the red, steam — the wheel parked next to it: «Давление много, друга.»"""
    Z = 2.3
    k = sm(u / 2.0)
    acts = [rig_act(t, SP * Z * 1.4, shake=k, gauge=0.5 + 0.5 * k, level=0.1),
            A(MC.monowheel_solo, RIG[0] + 62, RIG[1] + 6, SP * Z * 1.4, t=t, face='low', talk=KIT.wheel_k(t))]
    def f(big, v):
        sx, sy = v.opt(RIG[0], RIG[1] - 52 * SP * Z * 1.4 / 3 / Z)
        for i in range(5):
            ph = (t * 3 + i / 5) % 1.0
            B.puff(big, sx + (i - 2) * 30, sy - ph * 300, (20 + 60 * ph) * 3, 0.7 * (1 - ph), (236, 236, 240))
    big = interior(t, Z + 0.2 * u, RIG[0] + 30, 600.0, acts, f)
    B.shake(big, t, 3 + 9 * k, 30)
    if t > 25.9: O.flash(big, (t - 25.9) / 0.2)
    return big


def r_end(t, u):
    return r_boom(t, u, again=True)


SHOTS = [r_boom, r_rewind, r_lab, r_seeds, r_drip, r_pour, r_start, r_dance, r_queue, r_last, r_mine, r_pressure, r_end]
NAMES = ['boom', 'rewind', 'lab', 'seeds', 'drip', 'pour', 'start', 'dance', 'queue', 'last', 'mine', 'pressure', 'end']
CAP = dict(pressure=640, last=1760, lab=1780, boom=1640, end=1640, rewind=1780, queue=1120, dance=1780, start=1640)

SHOW = K.Show(EPI, 5, ['БЕНЗИН', 'ИЗ СЕМЕЧЕК'], hook_t=(0.10, 2.8), hook_y=120, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('2 ЧАСА НАЗАД', (90, 230, 255), 56), 2.9, 3.9, 540, 420),
                        (K.st('КАП!', (255, 214, 90), 90), 9.8, 11.0, 760, 700),
                        (K.st('ВР-Р-РУМ!', (255, 140, 60), 72), 12.9, 14.0, 540, 420)],
              flashes=[0.0, 16.3, 26.1], mosaics=[2.9])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
