"""S01E05 «ROOF: $9.99/MO» (≈36 s, twist at 57 %: success worse than failure — Vince subscribes, the roof closes, the rain stops,
and opening it again needs ULTRA $19.99). Main question: will the game get home dry? Souvenir: «roof $9.99/mo, opening $19.99».
  python3 ep05.py test 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import common as CM
import math
import numpy as np
from PIL import Image
import fx
import atmos as AT
import overlays as O
import stage as ST
from stage import OUT_W, OUT_H
from scene import sm, lerp
from cam25 import glide, kick
from episode import Episode
from props import v86cast as C, v86kit as K
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, T, E, CLOSE, SUN

EPI = Episode('ep05', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='v86', lang='us', promise='TOMORROW: SEASON FINALE'))
FACE = CM.Faces(EPI, dict(vince=[(0.0, 'outraged'), (T['r1'], 'shock'), (T['v2'], 'outraged'), (T['f1'], 'defeated'), (T['v3'], 'outraged'),
                                 (T['r2'], 'shock'), (CLOSE, 'smooth'), (SUN, 'cool'), (T['r3'], 'shock'), (T['f2'], 'tired'),
                                 (T['v6'], 'defeated')]))
WS = K.WS['ocean']
OCEAN_Y = 616.0
FRAN_W, FRAN_H = (505.0, 233.0), 104.0


def raining(t):
    return t < SUN


def level(t):
    """flood level 0..1 inside the car"""
    return sm((t - CUTS[1]) / (CUTS[5] - CUTS[1])) * (1 - sm((t - CLOSE - 0.6) / 0.8))


def car_at_head(v, hx, hy, z):
    S = WS * 3 * v.Z * z
    return K.wpt(v, hx + 3.08 * S, hy + 63.2 * S)


def roof_k(t):
    return sm((t - CLOSE) / 1.0)


def wx_(name):
    return 'ocean_night' if name == 'night' else 'ocean'


def car_cu(t, head, z, base=(0.8, 0.0), Z=1.35, cx=600.0, cy=380.0, kick_=(0, 0), fx_=None, **kw):
    name = 'ocean_night' if raining(t) else 'ocean'
    light = K.light_rain if raining(t) else K.light_sunset
    v = K.V(name, cx, cy, Z)
    d = dict(wet=1.0 if t < CLOSE + 2 else 0.0, sweat=1.0 if t > SUN + 1.5 else 0.0); d.update(kw)
    k, dy = FACE('vince', t, base, **d)
    wx, wy = car_at_head(v, head[0], head[1] + dy * 10, z)
    acts = CM_fg(K.car_group(v, wx, wy, t, vince_kw=k, z=z))
    acts[-1].P['roof'] = roof_k(t); acts[-1].P['fog'] = 1.0 if t > SUN + 3 else 0.0
    def f(big, _):
        if level(t) > 0.01: water(big, t, 1920 - level(t) * 900)
        if raining(t): K.rain(big, t, 1.0)
        if fx_: fx_(big, v)
    return K.shot(name, light, cx, cy, Z, acts=acts, focus=0.95, dof_k=26, fx_=f, t=t, kick=kick_, bokeh_=True)


def CM_fg(acts):
    for a in acts: a.near = 0.99
    return acts


def water(big, t, y):
    """the flooded car: translucent blue water with a wavy pixel surface and a floating rubber duck"""
    y = int(y)
    yy = np.arange(OUT_H)[:, None]; xx = np.arange(OUT_W)[None, :]
    surf = y + 10 * np.sin(xx / 60.0 + t * 4)
    m = (yy >= surf)
    lay = big.astype(np.float32)
    lay[m] = lay[m] * 0.55 + np.array((60, 150, 220), np.float32) * 0.45
    edge = (np.abs(yy - surf) < 6)
    lay[edge] = 235
    big[:] = lay.astype(np.uint8)
    sp = K.VX.draw(C.duck, 14.0)
    K.VX.blit(big, sp, 780 + 40 * math.sin(t * 1.3), y + 10 + 8 * math.sin(t * 4 + 1.3), 14.0, None)


def screen(t, lines, shake=0.0):
    name = 'ocean_night' if raining(t) else 'ocean'
    Z = 1.6
    def pre(big, _): big[:] = K.blur(big, 12)
    big = K.shot(name, K.light_rain if raining(t) else K.light_sunset, 640.0, 420.0, Z, pre=pre, dof_k=0, t=t, motes=False)
    if raining(t): K.rain(big, t, 0.8)
    sc = K.car_screen(t, lines)
    CM.overlay_scaled(big, sc, (OUT_W - sc.shape[1] * 1.15) / 2 + shake * math.sin(t * 40), 560, 1.15)
    if ST.LOG[0] is not None: ST.log('card', bbox=(60, 560, 1020, 560 + sc.shape[0] * 1.15))
    return big


# ================================================================== shots
def r_hook(t, u):
    return car_cu(t, (420, 980), 3.0, (0.9, -0.5), hand_n=(14.0, 96.0), hand_f=(-4.0, 96.0), prop_n=C.game_box, kick_=kick(t, [(0.3, 0.5)]))


def r_screen(t, u):
    return screen(t, [(CUTS[1], 'ROOF CONTROL', (255, 255, 255)), (CUTS[1] + 1.2, 'REQUIRES PREMIUM', (255, 214, 80)),
                      (CUTS[1] + 2.1, '$9.99 / MONTH', (255, 110, 200))])


def r_mine(t, u):
    return car_cu(t, (470, 980), 3.6, (0.9, 0.0), kick_=kick(t, [(T['v2'] + 0.4, 0.8)]))


def r_fran(t, u):
    Z = 1.0
    v = K.V('ocean_night', 560.0, 380.0, Z)
    k, dy = FACE('vince', t, (-0.2, -0.6), wet=1.0, hand_n=(14.0, 96.0), hand_f=(-4.0, 96.0), prop_n=C.game_box)
    acts = K.car_group(v, 600.0, OCEAN_Y, t, vince_kw=k)
    def f(big, _):
        x, y = v.opt(*FRAN_W)
        K.fran(big, x, y, FRAN_H * 3 * v.Z, t, talk=CM.M.mouth(EPI.talk, 'fran', t), look=0.4)
        K.rain(big, t, 1.0)
    return K.shot('ocean_night', K.light_rain, 560.0, 380.0, Z, acts=acts, fx_=f, t=t, dof_k=12, bokeh_=True)


def r_flood(t, u):
    return car_cu(t, (450, 900), 3.2, (0.9, 0.3), hand_n=(14.0, 96.0), hand_f=(-4.0, 96.0), prop_n=C.game_box)


def r_fee(t, u):
    if t >= T['v4_ep01'] - 0.05:
        return car_cu(t, (500, 960), 3.9, (0.9, 0.0), kick_=kick(t, [(T['v4_ep01'] + 0.4, 1.0)]))
    big = screen(t, [(CUTS[5], 'PREMIUM: ACTIVE', (90, 236, 255)), (CUTS[5] + 0.9, '+ $3.50', (255, 110, 140)),
                     (CUTS[5] + 1.3, 'CONVENIENCE FEE', (255, 110, 140))])
    return big


def r_close(t, u):
    Z = 1.05
    v = K.V('ocean_night', 600.0, 400.0, Z)
    k, dy = FACE('vince', t, (0.6, -0.5), wet=1.0)
    acts = K.car_group(v, 600.0, OCEAN_Y, t, vince_kw=k)
    acts[-1].P['roof'] = roof_k(t)
    def f(big, _): K.rain(big, t, 1.0 - 0.7 * sm(u / 1.0))
    return K.shot('ocean_night', K.light_rain, 600.0, 400.0, Z, acts=acts, fx_=f, t=t, dof_k=12)


def r_sun(t, u):
    Z = 1.05
    v = K.V('ocean', 600.0, 400.0, Z)
    k, dy = FACE('vince', t, (0.6, -0.5))
    acts = K.car_group(v, 600.0, OCEAN_Y, t, vince_kw=k)
    acts[-1].P['roof'] = 1.0
    def f(big, _): AT.flare(big, 640, 360, 1.0)
    big = K.shot('ocean', K.light_sunset, 600.0, 400.0, Z, acts=acts, fx_=f, t=t, dof_k=12, rays=dict(src=(620, 330), a=0.4))
    O.draw_sticker(big, ST_SUN, t, SUN + 0.2, CUTS[8], 540, 360)
    return big


def r_ultra(t, u):
    return screen(t, [(CUTS[8], 'OPEN ROOF', (255, 255, 255)), (CUTS[8] + 1.0, 'REQUIRES ULTRA', (255, 214, 80)),
                      (CUTS[8] + 1.9, '$19.99 / MONTH', (255, 110, 200))], shake=6.0 if u > 2.0 else 0.0)


def r_sweat(t, u):
    Z = 1.0
    v = K.V('ocean', 560.0, 380.0, Z)
    k, dy = FACE('vince', t, (0.6, 0.0), sweat=2.0)
    acts = K.car_group(v, 600.0, OCEAN_Y, t, vince_kw=k)
    acts[-1].P['roof'] = 1.0; acts[-1].P['fog'] = 1.0
    def f(big, _):
        x, y = v.opt(*FRAN_W)
        K.fran(big, x, y, FRAN_H * 3 * v.Z, t, talk=CM.M.mouth(EPI.talk, 'fran', t), look=0.4)
        AT.motes(big, t, box=(0, 900, OUT_W, 1700), n=20, col=(255, 240, 200), seed=4, drift=(0, -40))   # heat shimmer specks
    return K.shot('ocean', K.light_sunset, 560.0, 380.0, Z, acts=acts, fx_=f, t=t, dof_k=12, rays=dict(src=(620, 330), a=0.35))


def r_convert(t, u):
    return car_cu(t, (470, 960), 3.6 * (1 + 0.03 * u), (0.9, -0.2), sweat=2.0)


def r_button(t, u):
    Z = 1.45
    v = K.V('ocean', 505.0, 220.0, Z)
    def pre(big, _): big[:] = K.blur(big, 7)
    def f(big, _): K.fran(big, 560, 1430, 1080, t, talk=CM.M.mouth(EPI.talk, 'fran', t), lid=0.6, look=0.4)
    return K.shot('ocean', K.light_sunset, 505.0, 220.0, Z * (1 + 0.012 * u), pre=pre, dof_k=0, fx_=f, t=t, bloom=(200, 30, 0.7))


ST_SUN = K.st('...THE SUN CAME OUT', fg=(255, 214, 80), size=50)
R = [r_hook, r_screen, r_mine, r_fran, r_flood, r_fee, r_close, r_sun, r_ultra, r_sweat, r_convert, r_button]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 5, ['ROOF', 'LOCKED?'], hook_t=(0.10, 2.4), hook_y=250, hook_size=100,
              stickers=[(K.st('GAME FUND: -$441', fg=(90, 236, 255), size=46), T['v6'], CUTS[11], 540, 330)],
              flashes=[TWIST, CLOSE], mosaics=[CUTS[8]],
              cap_y={0: 1500, 1: 1640, 2: 1500, 3: 1200, 4: 1200, 5: 1640, 6: 1200, 7: 1200, 8: 1640, 9: 1200, 10: 1500, 11: 1520})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
