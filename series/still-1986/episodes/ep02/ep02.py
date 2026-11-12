"""S01E02 «$40 + FEES» (≈39 s, twist at 57 %: bureaucratic recursion — disputing the fees costs a fee).
Main question: what does a $40 ticket really cost? (closed at the TOTAL screen, 77 %). Souvenir number: «$40 ticket = $86».
  python3 ep02.py test 1 5 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST, T, E

EPI = Episode('ep02', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='v86', lang='us', promise='TOMORROW: BOAT DAY'))
FACE = CM.Faces(EPI, dict(
    vince=[(0.0, 'smooth'), (T['t1'], 'shock'), (T['v2'], 'outraged'), (T['f1'], 'cool'), (T['t2'], 'nervous'), (T['v4_ep01'], 'outraged'),
           (T['v3'], 'shock'), (T['v5'], 'scheming'), (T['t5'], 'shock'), (T['v6'], 'defeated'), (T['v7'], 'proudsad'), (T['f3'], 'smooth')],
    tiffany=[(0.0, 'deadpan'), (T['t5'], 'smug'), (T['t6'], 'deadpan')]))
WS = K.WS['club']
WIN = (806.0, 316.0, 914.0, 398.0)               # booth window (world px)
TIF = (860.0, 482.0)                              # Tiffany's feet anchor behind the counter
VIN = (735.0, 600.0)                              # Vince at the booth
FRAN_W, FRAN_H = (842.0, 226.0), 112.0

ROWS = [(0.0, 'TICKET', '$40.00'), (T['t1'] + 0.5, 'CASH HANDLING FEE', '$4.00'), (T['t2'] + 0.1, 'SERVICE FEE', '$12.50'),
        (T['t2'] + 1.2, 'FACILITY FEE', '$8.00'), (T['t2'] + 2.3, 'CONVENIENCE FEE', '$3.50'), (T['t3'] + 0.5, 'FEE FEE', '$2.00'),
        (T['t5'] + 2.2, 'DISPUTE FEE', '$5.00'), (T['t6'] + 0.6, 'TAX', '$11.00')]


def tiff_act(v, t, s=None, **kw):
    k, dy = FACE('tiffany', t, (-0.6, 0.0))
    k.update(kw)
    a = K.A(C.tiffany, TIF[0], TIF[1] + dy * 2, s or K.S_of(v, 'club'), t=t, flip=True, rim=(K.VX.SUN, K.PINK), **k)
    return CM.Clip(a, WIN)


def glass(big, v, t):
    x0, y0 = v.opt(WIN[0], WIN[1]); x1, y1 = v.opt(WIN[2], WIN[3])
    w = x1 - x0
    for i, off in enumerate((0.2, 0.55)):                              # two diagonal reflections on the glass
        for j in range(0, int(w * 0.18), 6):
            xa = int(x0 + w * off + j); ya, yb = int(y0), int(y1)
            for yy in range(ya, yb, 6):
                xx = xa + int((yy - ya) * 0.5)
                if x0 <= xx < x1 - 6 and 0 <= yy < OUT_H - 6:
                    reg = big[yy:yy + 6, xx:xx + 6].astype(np.float32)
                    big[yy:yy + 6, xx:xx + 6] = np.clip(reg * 0.86 + 255 * 0.14, 0, 255).astype(np.uint8)


def fran_booth(big, v, t, on=1.0):
    x, y = v.opt(*FRAN_W)
    K.fran(big, x, y, FRAN_H * 3 * v.Z, t, talk=CM.M.mouth(EPI.talk, 'fran', t), on=on, look=-0.5)


def vince_cu(t, head, s, base=(0.8, 0.0), Z=1.3, cx=760.0, cy=380.0, kick_=(0, 0), **kw):
    k, dy = FACE('vince', t, base, **kw)
    big, a, v = CM.cu('club', K.light_club, C.vince, t, cx, cy, Z, (head[0], head[1] + dy * 10), s, k, kick=kick_)
    return big


# ================================================================== shots
def r_hook(t, u):
    return vince_cu(t, (420, 900), 15.5 * (1 + 0.01 * u), (0.9, -0.2), hand_n=(26.0, 62.0 + 2 * math.sin(t * 6)), prop_n=C.cash,
                    sparkle=1.0 if u > 2.0 else 0.0)


def r_tiff(t, u):
    Z = 2.2
    v = K.V('club', 860.0, 360.0, Z)
    gum = sm((u - 0.6) / 0.8) if u < 1.45 else 0.0
    acts = [tiff_act(v, t, gum=gum)]
    def f(big, _):
        glass(big, v, t)
    big = K.shot('club', K.light_club, 860.0, 360.0, Z, acts=acts, fx_=f, t=t, dof_k=10)
    O.draw_sticker(big, ST_CASH, t, T['t1'] + 0.4, CUTS[2], 540, 300)
    return big


def r_two(t, u):
    Z = 1.15
    cx = lerp(770.0, 800.0, u / 5.0)
    v = K.V('club', cx, 380.0, Z)
    k, dy = FACE('vince', t, (0.9, -0.5), hand_n=(26.0, 62.0), prop_n=C.cash)
    acts = [tiff_act(v, t), K.A(C.vince, VIN[0], VIN[1] + dy * 2, K.S_of(v, 'club'), t=t, **k)]
    on = 0.0 if t < T['f1'] - 1.1 else (1.0 if t > T['f1'] - 0.5 else (1.0 if int(t * 20) % 3 else 0.2))
    def f(big, _):
        fran_booth(big, v, t, on)
    return K.shot('club', K.light_club, cx, 380.0, Z, acts=acts, fx_=f, t=t, dof_k=12, bokeh_=True, par=(-6 + 3 * u, 0))


def fee_insert(t, u, stamp=None, t_stamp=None, total=None, zoom=1.0):
    Z = 1.6
    v = K.V('club', 860.0, 360.0, Z)
    def pre(big, _): big[:] = K.blur(big, 12)
    big = K.shot('club', K.light_club, 860.0, 360.0, Z, pre=pre, dof_k=0, t=t, motes=False)
    sc = K.fee_screen(t, ROWS, total=total, t_total=T['t6'] + 1.0, stamp=stamp, t_stamp=t_stamp)
    k = 0.92 * zoom
    h, w = CM.overlay_scaled(big, sc, (OUT_W - sc.shape[1] * k) / 2, 380 + 8 * math.sin(t * 2), k)[:2]
    if ST.LOG[0] is not None: ST.log('card', bbox=((OUT_W - w) / 2, 380, (OUT_W + w) / 2, 380 + h))
    return big


def r_fees(t, u):
    return fee_insert(t, u)


def r_who(t, u):
    return vince_cu(t, (520, 960), 22.0, (0.9, 0.0), kick_=kick(t, [(T['v4_ep01'] + 0.5, 1.0)]))


def tiff_cu(t, u, gum=0.0):
    Z = 2.4
    v = K.V('club', 860.0, 352.0, Z)
    acts = [tiff_act(v, t, gum=gum)]
    def f(big, _): glass(big, v, t)
    return K.shot('club', K.light_club, 860.0, 352.0, Z * (1 + 0.01 * u), acts=acts, fx_=f, t=t, dof_k=10)


def r_tiff2(t, u):
    return tiff_cu(t, u)


def r_whatfee(t, u):
    return vince_cu(t, (470, 940), 18.0, (0.9, 0.2), look_up=True) if False else vince_cu(t, (470, 940), 18.0, (0.9, 0.3))


def r_tiff3(t, u):
    big = tiff_cu(t, u, gum=sm((u - 1.2) / 1.0))
    O.draw_sticker(big, ST_FEEFEE, t, T['t4'] + 0.6, CUTS[8], 540, 300)
    return big


def r_hero(t, u):
    Z = 1.55
    v = K.V('club', 730.0, 470.0, Z)
    k, dy = FACE('vince', t, (0.7, 0.4), hand_n=(22.0, 96.0), glint=1.0 if u > 0.4 else 0.0)
    a = K.A(C.vince, VIN[0], VIN[1] + dy * 2, K.S_of(v, 'club') * 1.15, t=t, **k)
    def f(big, _): AT.flare(big, 640, 380, 0.6, col=(255, 120, 200))
    return K.shot('club', K.light_club, 730.0, 470.0, Z, acts=[tiff_act(v, t), a], fx_=f, t=t, dof_k=14, bokeh_=True, par=(4 * u, 0))


def r_twist(t, u):
    big = fee_insert(t, u, stamp='FEE FEE FEE', t_stamp=T['t5'] + 2.25)
    O.draw_sticker(big, ST_DISPUTE, t, T['t5'] + 0.3, T['t5'] + 2.1, 540, 300)
    return big


def r_fran(t, u):
    Z = 1.45
    v = K.V('club', 842.0, 210.0, Z)
    def pre(big, _): big[:] = K.blur(big, 7)
    def f(big, _): K.fran(big, 560, 1400, 1040, t, talk=CM.M.mouth(EPI.talk, 'fran', t), lid=0.6, look=0.5)
    return K.shot('club', K.light_club, 842.0, 210.0, Z * (1 + 0.012 * u), pre=pre, dof_k=0, fx_=f, t=t, bloom=(200, 30, 0.7))


def r_total(t, u):
    return vince_cu(t, (520, 1000), 17.0, (0.9, 0.6))


def r_screen(t, u):
    return fee_insert(t, u, total='$86.00', zoom=1.0 + 0.04 * u)


def r_moved(t, u):
    return vince_cu(t, (480, 960), 19.0 * (1 + 0.025 * u), (0.9, -0.3), tears=1.0, sparkle=1.0)


def r_disco(t, u):
    Z = 1.0
    v = K.V('disco', 640.0, 400.0, Z)
    k, dy = FACE('vince', t, (0.8, 0.0), headphones=True, hand_n=(22.0, 86.0 + 6 * math.sin(t * 7)), hand_f=(-20.0, 84.0 + 6 * math.cos(t * 7)))
    bob = abs(math.sin(t * 7)) * 3
    a = K.A(C.vince, 600.0, 712.0 + dy * 2 - bob, K.S_of(v, 'disco') * 1.25, t=t, **k)
    def back(big, _):
        K.crowd(big, t, 1180, 1330, n=11, seed=3, headphones=True, h=(170, 240))
    def f(big, _):
        O.draw_sticker(big, ST_PHONES, t, CUTS[14] + 0.3, DUR, 540, 330)
        K.fran(big, 230, 900, 380, t, talk=CM.M.mouth(EPI.talk, 'fran', t), lid=0.6, look=0.6)
    return K.shot('disco', lambda v_: K.light_disco(v_, t), 640.0, 400.0, Z, acts=[a], pre=back, fx_=f, t=t, dof_k=10, bokeh_=True,
                  par=(-6 + 4 * u, 0))


ST_PHONES = K.st('HEADPHONES $15', fg=(90, 236, 255), size=54)
ST_CASH = K.st('+$4 CASH FEE', fg=(255, 110, 140), size=54)
ST_FEEFEE = K.st('FEE FOR THE FEES', fg=(255, 214, 80), size=50)
ST_DISPUTE = K.st('DISPUTE FEE?!', fg=(255, 110, 200), size=72)
R = [r_hook, r_tiff, r_two, r_fees, r_who, r_tiff2, r_whatfee, r_tiff3, r_hero, r_twist, r_fran, r_total, r_screen, r_moved, r_disco]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 2, ['$40...', 'RIGHT?'], hook_t=(0.10, 2.6), hook_y=250, hook_size=92,
              stickers=[(K.st('$40 -> $86', fg=(90, 236, 255), size=70), T['t6'] + 1.1, CUTS[13], 540, 330)],
              flashes=[TWIST, T['t5'] + 2.25, CUTS[14]], mosaics=[CUTS[14]],
              cap_y={0: 1500, 1: 1560, 2: 1480, 3: 1640, 4: 1500, 5: 1560, 6: 1500, 7: 1560, 8: 1500, 9: 1640, 10: 1520, 11: 1500, 12: 1640,
                     13: 1500, 14: 1560})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
