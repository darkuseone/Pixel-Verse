"""S01E03 «BOAT DAY» (≈37 s, twist at 60 %: the hunter asks for help — the marine patrol runs out of gas and asks Vince's pedal
flamingo for a tow). Main question: can Vince get his 1986 speedboat chase? Souvenir number: «speedboat $900/day — pedal flamingo $25».
  python3 ep03.py test 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, T, E, PASS

EPI = Episode('ep03', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='v86', lang='us', promise='TOMORROW: DROP DAY'))
FACE = CM.Faces(EPI, dict(
    vince=[(0.0, 'smooth'), (T['f1'], 'cool'), (T['v2'], 'outraged'), (T['f2'], 'defeated'), (T['v3'], 'scheming'), (T['v4'], 'nervous'),
           (PASS, 'shock'), (T['v5'], 'outraged'), (T['d1'], 'shock'), (T['v6'], 'smooth'), (CUTS[10], 'ecstatic'), (T['d2'], 'shock'),
           (T['v7'], 'outraged'), (T['f4'], 'defeated')],
    diaz=[(0.0, 'nervous'), (T['d2'], 'deadpan')]))
WSM, WSB = K.WS['marina'], K.WS['bay']
FRAN_W, FRAN_H = (130.0, 300.0), 110.0
DOCK_Y = 600.0


def fran_shack(big, v, t, on=1.0):
    x, y = v.opt(*FRAN_W)
    K.fran(big, x, y, FRAN_H * 3 * v.Z, t, talk=CM.M.mouth(EPI.talk, 'fran', t), on=on, look=0.6)


def vince_cu(t, head, s, base=(0.8, 0.0), name='marina', light=K.light_marina, cx=640.0, cy=360.0, Z=1.3, kick_=(0, 0), **kw):
    k, dy = FACE('vince', t, base, **kw)
    big, a, v = CM.cu(name, light, C.vince, t, cx, cy, Z, (head[0], head[1] + dy * 10), s, k, kick=kick_)
    return big


def pedal(v, x, y, t, kw, z=1.0, ws=WSB, speed=1.0, rock=1.5):
    return K.pedal_group(v, x, y, t, vince_kw=kw, ws=ws, z=z, pedal=t * 4 * speed, water_y=y - 6 * ws * z, rock=rock)


def wake(big, v, x, y, t, k=1.0):
    """white foam trailing behind a boat (output px)"""
    ox, oy = v.opt(x, y)
    for i in range(10):
        px = ox - 40 - i * 46 + math.sin(t * 9 + i) * 8; py = oy - 6 + (i % 3) * 8
        AT.screen(big, _dot_layer(big.shape, px, py, 18 - i, 0.7 * k * (1 - i / 10)))


def _dot_layer(shape, x, y, r, a):
    lay = np.zeros(shape, np.float32)
    r = max(3, int(r)); x, y = int(x), int(y)
    y0, y1, x0, x1 = max(0, y - r), min(shape[0], y + r), max(0, x - r), min(shape[1], x + r)
    if y0 < y1 and x0 < x1: lay[y0:y1, x0:x1] = 255 * a
    return lay


# ================================================================== shots
def r_hook(t, u):
    return vince_cu(t, (420, 900), 15.5 * (1 + 0.01 * u), (0.9, -0.2), cx=620.0, cy=330.0, hand_n=(24.0, 76.0), sparkle=1.0 if u > 2.2 else 0.0)


def r_fran(t, u):
    Z = 1.15
    v = K.V('marina', 330.0, 380.0, Z)
    k, dy = FACE('vince', t, (-0.8, -0.4))
    a = K.A(C.vince, 420.0, DOCK_Y + dy * 2, K.S_of(v, 'marina'), t=t, flip=True, **k)
    on = 0.0 if u < 0.1 else (1.0 if u > 0.6 else (1.0 if int(u * 20) % 3 else 0.2))
    def f(big, _): fran_shack(big, v, t, on)
    return K.shot('marina', K.light_marina, 330.0, 380.0, Z, acts=[a], fx_=f, t=t, dof_k=12, par=(-6 + 4 * u, 0))


def r_board(t, u):
    Z = 3.0 * (1 + 0.02 * u)
    big = K.shot('marina', K.light_marina, 170.0, 497.0, Z, t=t, dof_k=0, motes=False, kick=kick(t, [(T['v2'] + 0.3, 0.8)]))
    O.draw_sticker(big, ST_900, t, T['v2'] + 0.2, CUTS[3], 540, 1450)
    return big


def r_rent(t, u):
    Z = 1.45
    v = K.V('marina', 140.0, 260.0, Z)
    def pre(big, _): big[:] = K.blur(big, 7)
    def f(big, _): K.fran(big, 560, 1400, 1040, t, talk=CM.M.mouth(EPI.talk, 'fran', t), lid=0.6, look=0.5)
    return K.shot('marina', K.light_marina, 140.0, 260.0, Z * (1 + 0.012 * u), pre=pre, dof_k=0, fx_=f, t=t, bloom=(200, 30, 0.7))


def r_special(t, u):
    Z = 1.25
    cx = lerp(520.0, 400.0, glide((u - 1.2) / 1.0))
    v = K.V('marina', cx, 485.0, Z)
    k, dy = FACE('vince', t, (-0.8, 0.0), hand_n=(-6.0, 70.0) if u > 1.0 else None)
    a = K.A(C.vince, 470.0, DOCK_Y + dy * 2, K.S_of(v, 'marina'), t=t, flip=True, **k)
    boat = [K.WaterClip(K.A(C.pedal_flamingo, 390.0, 712.0, K.S_of(v, 'marina') * C.CAR_K, t=t, rot=1.5 * math.sin(t * 2)), 704.0)]
    def f(big, _): O.draw_sticker(big, ST_25, t, T['v3'] + 1.3, CUTS[5], 540, 420)
    return K.shot('marina', K.light_marina, cx, 485.0, Z, acts=boat + [a], fx_=f, t=t, dof_k=12)


def r_pedal(t, u):
    Z = 1.1
    x = 420.0 + 30.0 * u
    v = K.V('bay', x + 60.0, 400.0, Z)
    k, dy = FACE('vince', t, (0.9, 0.0), hair_wind=0.3, sweat=1.0)
    acts = pedal(v, x, 640.0, t, k, speed=1.6)
    def f(big, _): wake(big, v, x - 60, 640, t, 0.6)
    return K.shot('bay', K.light_marina, x + 60.0, 400.0, Z, acts=acts, fx_=f, t=t, dof_k=10, par=(-8 + 4 * u, 0),
                  rays=dict(src=(560, 760), a=0.22))


def r_pass(t, u):
    Z = 1.1
    x = 520.0
    v = K.V('bay', 560.0, 400.0, Z)
    wet = 1.0 if u > 0.2 else 0.0
    k, dy = FACE('vince', t, (0.9, -0.3), wet=wet, hair_wind=0.4)
    xb = lerp(-300.0, 1500.0, (u + 0.6) / 1.4)
    patrol = [K.WaterClip(K.A(C.patrol_boat, xb, 600.0, K.S_of(v, 'bay', 0.85) * C.TOW_K, t=t, rot=-3.0), 592.0)] if u < 0.9 else []
    acts = patrol + pedal(v, x, 650.0, t, k, speed=1.0, rock=4.0 if u > 0.15 else 1.0)
    def f(big, _):
        if 0.1 < u < 0.9:
            AT.sparks(big, 560, 1400, t, PASS + 0.12, n=30, col=(220, 240, 255), seed=4, life=0.7, speed=900, px=10)
        if u < 0.9: wake(big, v, xb - 80, 600, t, 1.0)
    big = K.shot('bay', K.light_marina, 560.0, 400.0, Z, acts=acts, fx_=f, t=t, dof_k=10, kick=kick(t, [(PASS + 0.15, 1.2)]))
    if u < 0.5: fx.speed_lines(big, t, 0.4)
    return big


def r_chase(t, u):
    Z = 1.15
    x = 440.0 + 60.0 * u
    v = K.V('bay', x + 80.0, 400.0, Z)
    k, dy = FACE('vince', t, (0.9, 0.0), wet=1.0, hair_wind=0.6, sweat=1.0)
    acts = pedal(v, x, 650.0, t, k, speed=2.4, rock=2.5)
    mx, my = x + 190.0, 575.0
    def f(big, _):
        wake(big, v, x - 60, 650, t, 0.8)
        ox, oy = v.opt(mx, my)                                         # a channel marker post with Fran on top
        big[int(oy - 30):int(oy + 400), int(ox - 10):int(ox + 10)] = (60, 50, 70)
        K.fran(big, int(ox), int(oy - 20), 300, t, talk=CM.M.mouth(EPI.talk, 'fran', t), lid=0.6, look=-0.6)
    big = K.shot('bay', K.light_marina, x + 80.0, 400.0, Z, acts=acts, fx_=f, t=t, dof_k=10, par=(-10 + 6 * u, 0))
    fx.speed_lines(big, t, 0.2)
    return big


def r_twist(t, u):
    Z = 1.25
    v = K.V('bay', 640.0, 420.0, Z)
    S = K.S_of(v, 'bay', 0.95)
    bx, by = 780.0, 600.0
    dk = K.WaterClip(K.A(C.patrol_boat, bx, by, S * C.TOW_K, t=t, smoke=1.0, lights=False), 592.0)
    dx, dyy = bx - 125.0, by - 34.0 * C.TOW_K * WSB * 0.95
    kd, dy = FACE('diaz', t, (-0.8, 0.0))
    diaz = K.A(C.diaz, dx, dyy + 30.0 + dy * 2, S, t=t, flip=True, legs=False, hand_n=(-8.0, 60.0), **kd)
    k, _ = FACE('vince', t, (0.9, -0.2), wet=1.0)
    acts = [dk, diaz] + pedal(v, 575.0, 668.0, t, k, speed=0.2, rock=1.0)
    big = K.shot('bay', K.light_marina, 640.0, 420.0, Z, acts=acts, t=t, dof_k=10)
    O.draw_sticker(big, ST_TOW, t, T['d1'] + 1.6, CUTS[9], 540, 380)
    return big


def r_hopon(t, u):
    return vince_cu(t, (470, 960), 18.0, (0.8, -0.2), name='bay', cx=640.0, cy=360.0, wet=1.0, sparkle=1.0, glint=1.0 if u > 0.8 else 0.0)


def r_towing(t, u):
    Z = 0.9
    x = 300.0 + 90.0 * u
    v = K.V('bay', x - 150.0, 400.0, Z)
    k, dy = FACE('vince', t, (0.9, 0.0), wet=1.0, hair_wind=0.5)
    S = K.S_of(v, 'bay', 0.9)
    bx = x - 470.0
    patrol = K.WaterClip(K.A(C.patrol_boat, bx + 30.0, 640.0, S * C.TOW_K, t=t, lights=False), 632.0)
    acts = [patrol] + pedal(v, x, 650.0, t, k, speed=2.2, z=0.95)
    def f(big, _):
        a0 = v.opt(x - 70.0, 620.0); b0 = v.opt(bx + 30.0 + 88.0 * C.TOW_K * WSB * 0.9 * 0.95, 610.0)    # the tow rope
        for i in range(40):
            q = i / 39; xx = int(a0[0] + (b0[0] - a0[0]) * q); yy = int(a0[1] + (b0[1] - a0[1]) * q + 30 * math.sin(math.pi * q))
            if 0 <= xx < OUT_W - 6 and 0 <= yy < OUT_H - 6: big[yy:yy + 6, xx:xx + 6] = (240, 220, 170)
        AT.flare(big, 540, 720, 0.6)
    return K.shot('bay', K.light_marina, x - 150.0, 400.0, Z, acts=acts, fx_=f, t=t, dof_k=8, rays=dict(src=(540, 760), a=0.3))


def r_ticket(t, u):
    Z = 1.4
    v = K.V('marina', 600.0, 470.0, Z)
    S = K.S_of(v, 'marina')
    kd, dy = FACE('diaz', t, (0.8, -0.3))
    diaz = K.A(C.diaz, 540.0, DOCK_Y + dy * 2, S, t=t, ticket=True, **kd)
    k, dy2 = FACE('vince', t, (-0.8, 0.0), wet=1.0, hand_n=(-8.0, 70.0) if t > T['v7'] else None)
    vin = K.A(C.vince, 668.0, DOCK_Y + 4 + dy2 * 2, S, t=t, flip=True, **k)
    big = K.shot('marina', K.light_marina, 600.0, 470.0, Z, acts=[diaz, vin], t=t, dof_k=12, bokeh_=True)
    O.draw_sticker(big, ST_250, t, T['d2'] + 1.6, CUTS[12], 540, 380)
    return big


def r_button(t, u):
    Z = 1.45
    v = K.V('marina', 140.0, 260.0, Z)
    def pre(big, _): big[:] = K.blur(big, 7)
    def f(big, _): K.fran(big, 560, 1400, 1040, t, talk=CM.M.mouth(EPI.talk, 'fran', t), lid=0.6, look=0.3)
    return K.shot('marina', K.light_marina, 140.0, 260.0, Z * (1 + 0.015 * u), pre=pre, dof_k=0, fx_=f, t=t, bloom=(200, 30, 0.7))


ST_900 = K.st('$900 A DAY', fg=(255, 110, 140), size=66)
ST_25 = K.st('PEDAL FLAMINGO $25/HR', fg=(255, 150, 200), size=44)
ST_TOW = K.st('TOW US?!', fg=(255, 214, 80), size=80)
ST_250 = K.st('TICKET: $250', fg=(255, 110, 140), size=60)
R = [r_hook, r_fran, r_board, r_rent, r_special, r_pedal, r_pass, r_chase, r_twist, r_hopon, r_towing, r_ticket, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 3, ['BOAT', 'DAY?'], hook_t=(0.10, 2.6), hook_y=250, hook_size=100,
              stickers=[(K.st('GAME FUND: -$346', fg=(90, 236, 255), size=46), CUTS[10] + 0.3, CUTS[11], 540, 330)],
              flashes=[TWIST, PASS + 0.15, CUTS[10]], mosaics=[CUTS[5]],
              cap_y={0: 1500, 1: 1480, 2: 1640, 3: 1520, 4: 1480, 5: 1200, 6: 1200, 7: 1200, 8: 1240, 9: 1500, 10: 1200, 11: 1500, 12: 1520})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
