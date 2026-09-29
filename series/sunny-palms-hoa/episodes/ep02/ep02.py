"""S01E02 «Emotional Support Flamingo» — Dale brings a plastic flamingo with a $19.99 «certificate»; HOA law makes it valid,
so Brenda charges a $300/year registration (the whole street already pays); Dale throws Kevin into the pond, Earl feels supported.
  python3 ep02.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import paths as P
import stage as ST
from stage import Chars, view_at
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import us_cast as U
from props import us_props as UP
from props import uskit as K
from props import bytfx as B
from props.usshots import Shots, J, hit
from timeline import DUR, FPS, VOICE, SLUG

EPI = Episode('ep02', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
YARD = ST.ai_world(P.series(SLUG) / 'bg' / 'yard.png')
INTER = ST.ai_world(P.series(SLUG) / 'bg' / 'interior.png')
S = Shots(talk, YARD)
WU = 6.4


def kevin(t, x_off=8.6, y_off=-4.2, s=0.95, flip=False, wob=0.0, shades=True, anchor='D', tilt=0.0):
    """hook: draw Kevin next to a hero (anchor D = Dale, B = Brenda); lit like the hero"""
    def f(CH, v):
        ax, ay, au = S.D if anchor == 'D' else S.B
        UP.flamingo(CH, v.cam(ax + x_off * au, ay + y_off * au, au * s, flip), t, True, shades, wob, tilt)
    return f


def cert_small(L, h, ang=-0.15, w=5.6, hh=7.2):
    cx, cy = h[0] + 0.3, h[1] - 0.4
    UP.rect(L, cx + 0.3, cy + 0.3, w, hh, ang, (150, 110, 40))
    UP.rect(L, cx, cy, w, hh, ang, (250, 244, 222))
    UP.rect(L, cx, cy, w - 0.8, hh - 0.8, ang, (250, 244, 222))
    UP.rect(L, cx, cy - hh * 0.30, w - 1.2, 1.1, ang, (230, 60, 130))
    UP.ltext(L, 'OFFICIAL', (cx, cy - hh * 0.05), min(1.2, w * 0.8 / 8), (60, 50, 110), ang)
    UP.ltext(L, '$19.99', (cx, cy + hh * 0.26), min(1.2, w * 0.7 / 6), (214, 150, 20), ang)
    for k in range(3): UP.dot(L, (cx - 1.3 + 1.3 * k, cy + hh * 0.42), (255, 196, 40), 0.42)


def form_small(L, h, ang=-0.15, w=5.4, hh=7.0, txt='$300'):
    UP.notice(L, h, ang, w, hh, txt)


# ================================================================== shots
def r_hook(t, u):
    return S.cu_dale(t, u, 'smug', 1.35, dx=48, dy=-4, shades=True, pose=U.DPOSE['hips'], red=0.25, zoom=0.05, front=kevin(t, 5.4, -4.4, 0.95, wob=0.5 * hit(t, 0.05, 0.3)))


def r_b1(t, u):
    return S.cu_brenda(t, u, 'hollow', 2.0, hand=U.H(3.4, 10.4), prop=lambda L, h: UP.clipboard(L, h, -0.15, w=4.4, hh=6.0), front=kevin(t, -9.6, -4.2, 0.95, anchor='B'))


def r_d2(t, u):
    return S.cu_dale(t, u, 'smug', 2.0 + J(u, 1.6), shades=True, hand=U.H(8.0, 14.0), prop=cert_small, red=0.25)


def r_b2a(t, u):
    return S.cu_brenda(t, u, 'evil', 2.2, hand=U.H(7.4, 15.4), prop=lambda L, h: cert_small(L, h, 0.1))


def r_cert(t, u):
    v = view_at(YARD, 465, 300, 2.0, 180, 330)
    big = v.bg()
    UP.cert_insert(big, t, hl=sm((t - 9.75) / 0.35))
    return big


def r_d3(t, u):
    return S.cu_dale(t, u, 'smug', 2.1, shades=True, pose=U.DPOSE['hips'], red=0.2, zoom=0.1)


def r_b3(t, u):
    return S.cu_brenda(t, u, 'shock' if u < 1.3 else 'dread', 2.1 + J(u, 1.4), hand=U.H(3.6, 12.0), prop=lambda L, h: UP.binder(L, h, -0.1, 5.4, 7.2), sweat=0.9)


def r_yes(t, u):
    return S.cu_dale(t, u, 'cheer', 2.1, shades=(u > 0.1), hand=U.H(8.6, 26.0 - 1.4 * math.sin(u * 20)), zoom=0.15)


def r_b4(t, u):
    return S.cu_brenda(t, u, 'evil' if u < 1.2 else 'sweet', 2.1 + J(u, 1.9), hand=U.H(7.8, 14.6), prop=lambda L, h: UP.clipboard(L, h, -0.12, w=4.4, hh=6.0),
                       front=kevin(t, -10.2, -4.2, 0.95, anchor='B'))


def r_b5(t, u):
    return S.cu_brenda(t, u, 'bright' if u < 2.7 else 'sweet', 2.2 + J(u, 1.9), pose=U.BPOSE['hands'], lean=0.3)


def r_d4(t, u):
    return S.cu_dale(t, u, 'shock', 2.3, shades=None, sweat=0.9, pose=U.DPOSE['shout'], zoom=0.2, red=0.15)


def r_bless(t, u):
    return S.cu_brenda(t, u, 'sweet', 2.3, lean=0.4, pose=U.BPOSE['hands'])


def r_parade(t, u):
    """the whole street is registered: rows of identical vested flamingos, Brenda proud in front"""
    Z = 1.2
    v = view_at(YARD, 1005, 470, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    rng = np.random.default_rng(94)
    pts = sorted(((float(rng.uniform(872, 1140)), float(rng.uniform(432, 590))) for _ in range(36)), key=lambda p: p[1])
    shown = int(min(len(pts), 4 + (t - 28.79) * 16))
    for i, (x, y) in enumerate(pts[:shown]):
        us = lerp(2.4, 4.6, (y - 432) / 158)
        UP.flamingo(CH, v.cam(x, y, us), t + i, True, i % 3 == 0, 0.25 * math.sin(t * 3 + i), 0.0)
    CH.comp(big, K.light_yard(v))
    C2 = Chars()
    U.brenda(C2, v.cam(1100.0, 606.0, WU, flip=True), U.BPOSE['stand'], t, mouth_('brenda', t), 'sweet', 0.0, hand_n=U.H(3.4, 13.6), prop_n=UP.clipboard)
    C2.comp(big, K.light_yard(v))
    fx.vignette(big, 0.22)
    return big


def mouth_(who, t, k=1.6):
    return min(1.0, talk(who, t) * k)


def r_fund(t, u):
    k = sm((u - 0.15) / 0.45)
    Z = lerp(2.1, 1.0, k)
    v = view_at(INTER, lerp(318.0, 452.0, k), lerp(370.0, 262.0, k), Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    UP.fund_jar(CH, v, t, 1.0)
    CH.comp(big, K.light_int(v))
    lvl = 0.04 + 0.08 * sm((u - 0.45) / 0.35)
    UP.fund_insert(big, v, t, lvl, pop=(u - 0.8) / 0.6 if u > 0.8 else 0.0, title=('MALDIVES', '2028'))
    fx.shafts(big, t, 0.6, 0.05)
    fx.vignette(big, 0.25)
    return big


def r_d5(t, u):
    return S.cu_dale(t, u, 'sad', 2.0 + 0.0, shades=None, sweat=1.0, pose=U.DPOSE['hold'], zoom=0.14, hand=U.H(5.2, 12.0), red=0.1,
                     front=kevin(t, 6.6, -7.2, 0.95))


def r_throw(t, u):
    """Kevin flies into the pond"""
    Z = 1.1
    v = view_at(YARD, 560, 470, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    k = min(1.0, u / 0.5)
    x = lerp(300.0, 610.0, k); y = lerp(560.0, 500.0, k) - 170 * math.sin(k * math.pi)
    if u < 0.5:
        UP.flamingo(CH, v.cam(x, y, 4.6, flip=int(t * 14) % 2 == 0), t, True, True, 0.0, 0.0)
    CH.comp(big, K.light_yard(v))
    if u >= 0.45:
        sx, sy = v.opt(610, 505)
        ph = (u - 0.45) / 0.4
        for i in range(8):
            B.puff(big, sx + 60 * math.sin(i * 1.3) * (0.3 + ph), sy - 120 * ph * (0.4 + 0.15 * i % 0.5), 50 + 60 * ph, 0.7 * max(0.0, 1 - ph), (220, 240, 250))
    if u < 0.3: B.shake(big, t, 8 * (1 - u / 0.3), 33)
    fx.vignette(big, 0.22)
    return big


def r_earl(t, u):
    chewing = t < 36.45
    lid = 0.85 if 36.45 <= t < 36.7 else 0.5
    return S.cu_earl(t, u, lid, 2.5, stuff='flamingo' if chewing else None, chew=1.0 if chewing else 0.0, dy=0.0 if chewing else -4 * hit(t, 36.45, 0.3))


def r_tail(t, u):
    slide = 1 - sm(u / 0.25)
    return S.cu_dale(t, u, 'sad' if u < 0.5 else 'incredulous', 1.75, dx=34, shades=None, hand=U.H(5.6 + 6 * slide, 12.6 - 6 * slide),
                     prop=lambda L, h: UP.notice(L, h, -0.2 - 1.2 * slide, w=5.2, hh=6.8, txt='$300'), red=0.4, sweat=0.4)


SHOTS = [
    (0.00, 2.95, 'hook'), (2.95, 4.83, 'b1'), (4.83, 8.09, 'd2'), (8.09, 9.25, 'b2a'), (9.25, 11.87, 'cert'), (11.87, 13.90, 'd3'),
    (13.90, 16.64, 'b3'), (16.64, 17.68, 'yes'), (17.68, 21.44, 'b4'), (21.44, 25.90, 'b5'), (25.90, 27.12, 'd4'), (27.12, 28.79, 'bless'),
    (28.79, 31.50, 'parade'), (31.50, 32.86, 'fund'), (32.86, 34.85, 'd5'), (34.85, 35.70, 'throw'), (35.70, 38.37, 'earl'), (38.37, DUR + 1, 'tail'),
]
FN = dict(hook=r_hook, b1=r_b1, d2=r_d2, b2a=r_b2a, cert=r_cert, d3=r_d3, b3=r_b3, yes=r_yes, b4=r_b4, b5=r_b5, d4=r_d4, bless=r_bless,
          parade=r_parade, fund=r_fund, d5=r_d5, throw=r_throw, earl=r_earl, tail=r_tail)


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


SHOW = K.Show(EPI, 2, ['MY EMOTIONAL', 'SUPPORT FLAMINGO'], hook_t=(0.15, 2.4),
              stickers=[
                  (st('AURA +9999', (255, 236, 96), 60), 16.68, 17.6, 540, 320),
                  (st('[SAXOPHONE GETS LOUDER]', (255, 255, 255), 30), 17.1, 18.5, 540, 1480),
                  (st('CORAL WHISPER', (255, 150, 190), 64), 19.2, 21.2, 540, 420),
                  (st('$300 / YEAR', (255, 84, 96), 78), 23.2, 25.9, 540, 440),
                  (st('AURA -9999', (255, 100, 100), 60), 25.95, 26.95, 540, 320),
                  (st('(TRANSLATION: YOU IDIOT)', (255, 190, 226), 28), 27.15, 28.7, 540, 1130),
                  (st('94 FLAMINGOS', (255, 236, 120), 84), 29.2, 31.4, 540, 470),
                  (st('TOTAL FINES: $1,050', (255, 236, 120), 40), 38.9, 40.4, 540, 1450),
              ],
              flashes=[16.64], mosaics=[28.79, 35.70], cap_y={'cert': 1560, 'parade': 1420, 'fund': 1560, 'throw': 1420},
              teaser='NEXT: SUSPICIOUS MAN')


def render(t):
    a, b, name = shot_at(t)
    big = FN[name](t, t - a)
    SHOW.apply(big, t, name)
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
