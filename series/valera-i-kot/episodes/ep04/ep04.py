"""S01E04 «Сто сорок третий» — Valera calls the ZhEK: 3 hours on hold, bureaucratic ping-pong, and the clerk turns out
to be lying in a hot bathtub right in the office. «Это вода. Служебная.»
  python3 ep04.py test 1 5 20 | frame 12 | all [4]"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import stage as ST
from stage import View, view_at, Chars, Light, shadow
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as B
from props import panelka as PK
from props import vikit as K
from timeline import DUR, FPS, VOICE, SLUG

COL = dict(K.COL, nina_clear=K.COL['nina'])
EPI = Episode('ep04', VOICE, DUR, FPS, colors=COL, slug=SLUG)
talk = EPI.talk
KIT = np.array(PK.kitchen(16))
ZHEK = PK.q(Image.open(PK.BG / 'zhek.png').convert('RGB'))
VX, VY, VU = 985.0, 722.0, 16.5                       # Valera on the kitchen stool, facing right
NX, NY, NU = 680.0, 412.0, 17.0                       # Nina's waterline in the office bathtub, facing left
PHONE_BASE = (1118.0, 512.0)
DESK_PHONE = (70.0, 400.0)
LAMP_Z = (632.0, 30.0)


def mouth(who, t, k=1.6):
    v = talk(who, t)
    if who == 'nina': v = max(v, talk('nina_clear', t))
    return min(1.0, v * k)


def light_zhek(v):
    lx, ly = v.opt(*LAMP_Z)
    tx, ty = v.opt(800.0, 380.0)
    return Light(amb=(0.98, 1.02, 0.98), keys=[(lx, ly, 1400, (230, 255, 236), 0.4), (tx, ty, 700, (255, 214, 160), 0.5)],
                 rim=(1, -0.3, (196, 220, 255), 0.3), grad=(1.05, 0.92))


# ---------------------------------------------------------------- Valera side (kitchen)
def v_face():
    return K.face_w(VX, VY, VU, h=20.6)


def valera(CH, v, t, expr='angry', stubble=0.0, tint=None, look=0.0):
    hand = F.H(0.2, 18.3)                              # handset along the back of the jaw up to the ear: face stays visible
    F.valera(CH, v.cam(VX, VY, VU), dict(F.VPOSE['sit'], bn=-1), t, mouth('valera', t), expr, 'home', hand_n=hand,
             prop_n=lambda L, h: F.handset(L, h, -2.05, (214, 200, 170)), stubble=stubble, tint=tint, look=look)


def phone_base(CH, v, hand_world):
    L = Layer(v.wcam())
    x, y = PHONE_BASE
    F.ell(L, (x, y), 34, 16, (214, 200, 170), 0, (236, 226, 200), (176, 160, 130))
    F.ell(L, (x, y - 6), 14, 9, (80, 74, 70)); F.ell(L, (x, y - 6), 8, 5, (214, 200, 170))
    pts = [(x - 28, y + 4)]
    for i in range(1, 13):                                                                # curly cord to the handset
        k = i / 12
        px = lerp(x - 28, hand_world[0], k); py = lerp(y + 4, hand_world[1], k) + 40 * math.sin(math.pi * k)
        pts.append((px + 3 * math.sin(i * 2.4), py + 3 * math.cos(i * 2.4)))
    for a, b in zip(pts, pts[1:]): F.cap(L, a, b, 1.4, 1.4, (190, 176, 146))
    F.outline(L); CH.add(L)


def kitchen_frame(v, t, expr='angry', stubble=0.0, tint=None, grade=None, clock=None, look=0.0):
    CH, FX = K.begin(v.Z)
    big = v.bg()
    hw = (VX + 0.2 * VU, VY - 18.0 * VU)
    phone_base(CH, v, hw)
    CH.comp(big, K.light_kit(v))
    CH2 = Chars(); valera(CH2, v, t, expr, stubble, tint, look); CH2.comp(big, K.light_kit(v))
    if clock is not None:
        L = Layer(v.wcam()); cx, cy, r = PK.CLOCK
        a_m = clock; a_h = a_m / 12
        F.cap(L, (cx, cy), (cx + math.sin(a_m) * r * 0.8, cy - math.cos(a_m) * r * 0.8), 1.6, 1.2, (30, 24, 20))
        F.cap(L, (cx, cy), (cx + math.sin(a_h) * r * 0.5, cy - math.cos(a_h) * r * 0.5), 2.2, 1.8, (30, 24, 20))
        FX.add(L)
    B.snow_in(FX, v, t, PK.WINDOW_OPEN, n=30, drift=(-90, 220))
    FX.comp(big)
    if grade: fx.grade(big, grade)
    fx.vignette(big, 0.3)
    return big


def r_v_cu(t, u, expr='angry', Z=2.0, **kw):
    fx_, fy_ = v_face()
    v = view_at(KIT, fx_ - 10, fy_ + 10, Z + 0.06 * u, 180, 300)
    return kitchen_frame(v, t, expr, **kw)


def r_timelapse(t, u):
    v = view_at(KIT, 1040, 380, 1.2, 180, 360)
    k = u / 2.2
    day = 0.5 - 0.5 * math.cos(k * 4 * math.pi)                                          # night -> day -> night -> day -> night
    grade = (lerp(1.0, 1.18, day), lerp(1.0, 1.12, day), lerp(1.0, 0.98, day))
    return kitchen_frame(v, t, 'sad' if k > 0.4 else 'normal', stubble=min(1.0, k * 1.4), grade=grade, clock=t * 35)


def r_cat_sing(t, u):
    x, y = PK.CAT_K
    hx, hy = x + 4.4 * PK.CAT_K_UNIT, y - 6.9 * PK.CAT_K_UNIT
    v = view_at(KIT, hx, hy + 5, 2.8 + 0.06 * u, 180, 300)
    CH, FX = K.begin(v.Z)
    big = v.bg()
    sing = 0.5 * (1 + math.sin(t * 2 * math.pi * 1.65)) if talk('cat', t) < 0.02 else 0.0
    F.cat(CH, v.cam(x, y, PK.CAT_K_UNIT), t, 'loaf', max(mouth('cat', t, 2.0), sing * 0.8), 1.0 if sing else 0.55, tail=1.0)
    CH.comp(big, K.light_kit(v))
    L = Layer(v.wcam())                                                                  # music notes rising
    for i in range(4):
        ph = ((t * 0.9 + i * 0.25) % 1.0)
        nx, ny = hx + 20 + 18 * i - 6 * ph, hy - 30 - 70 * ph
        F.ell(L, (nx, ny), 3.2, 2.4, (40, 36, 40), -0.4); F.cap(L, (nx + 2.6, ny - 1), (nx + 2.6, ny - 12), 0.8, 0.8, (40, 36, 40))
        F.cap(L, (nx + 2.6, ny - 12), (nx + 7, ny - 8), 0.8, 0.8, (40, 36, 40))
    FX.add(L)
    B.snow_in(FX, v, t, PK.WINDOW_OPEN, n=30, drift=(-90, 220))
    FX.comp(big)
    fx.vignette(big, 0.3)
    return big


# ---------------------------------------------------------------- Nina side (ZhEK office)
def n_face():
    return NX - 1.9 * NU, NY - 10.2 * NU


def cord(CH, v, hand_world):
    L = Layer(v.wcam())
    pts = [hand_world]
    for i in range(1, 25):
        k = i / 24
        px = lerp(hand_world[0], DESK_PHONE[0], k)
        py = lerp(hand_world[1], DESK_PHONE[1], k) + 190 * math.sin(math.pi * k) * (1 if k > 0.1 else k * 10)
        pts.append((px + 4 * math.sin(i * 2.2), py + 4 * math.cos(i * 2.2)))
    for a, b in zip(pts, pts[1:]): F.cap(L, a, b, 1.6, 1.6, (170, 36, 36))
    CH.add(L)


def zhek_frame(v, t, expr='bored', slam=None):
    CH, FX = K.begin(v.Z)
    big = v.bg()
    if slam is None:
        hand = F.H(-0.1, 7.3)
        hw = (NX + 0.1 * NU, NY - 7.1 * NU)
        cord(CH, v, hw)
        F.nina(CH, v.cam(NX, NY, NU, flip=True), t, mouth('nina', t), expr, True, hand_n=hand,
               prop_n=lambda L, h: F.handset(L, h, -2.0))
    else:                                                                                # arm swings the handset down to hang up
        k = sm(slam)
        hand = F.H(lerp(-0.1, 5.0, k), lerp(7.3, 2.5, k))
        F.nina(CH, v.cam(NX, NY, NU, flip=True), t, 0.0, 'smug', True, hand_n=hand, prop_n=lambda L, h: F.handset(L, h, lerp(-2.0, -0.4, k)))
    CH.comp(big, light_zhek(v))
    B.steam(big, v, t, 830, 395, -99, n=8, rise=190, size=40, a=0.45)
    FX.comp(big)
    fx.vignette(big, 0.3)
    return big


def r_n_cu(t, u, expr='bored', Z=3.0):
    x, y = n_face()
    v = view_at(ZHEK, x, y, Z + 0.06 * u, 180, 290)
    return zhek_frame(v, t, expr)


def r_reveal(t, u):
    x, y = n_face()
    k = sm((u - 0.1) / 1.3)
    cx, cy = lerp(x, 770, k), lerp(y, 385, k)
    Z = lerp(3.0, 0.92, k)
    sy = lerp(290, 330, k)
    v = view_at(ZHEK, cx, cy, Z, 180, sy)
    big = zhek_frame(v, t, 'smug' if u > 1.0 else 'bored')
    if 0.05 < u < 0.6: fx.speed_lines(big, t, 0.4)
    return big


def r_n_bath(t, u):
    v = view_at(ZHEK, 700, 320, 1.7 + 0.05 * u, 180, 320)
    return zhek_frame(v, t, 'blissful' if talk('nina_clear', t) < 0.02 else 'smug')


def r_hangup(t, u):
    if t < 32.9:
        v = view_at(ZHEK, 700, 320, 1.8, 180, 320)
        big = zhek_frame(v, t, slam=min(1.0, u / 0.3))
        if u > 0.28: B.shake(big, t, 10, 40)
        return big
    return r_v_cu(t, u, 'shock' if int(t * 10) % 4 else 'angry', Z=2.3, stubble=1.0)


# ---------------------------------------------------------------- shots
SHOTS = [
    (0.00, 1.75, 'hook'), (1.75, 4.20, 'robot1'), (4.20, 6.40, 'robot2'), (6.40, 8.60, 'timelapse'), (8.60, 10.30, 'cat_sing'),
    (10.30, 12.90, 'n_cu1'), (12.90, 14.85, 'v_cu2'), (14.85, 17.60, 'n_cu2'), (17.60, 19.75, 'v_cu3'), (19.75, 21.35, 'n_cu3'),
    (21.35, 23.90, 'v_cu4'), (23.90, 27.10, 'reveal'), (27.10, 29.80, 'v_sus'), (29.80, 32.50, 'n_bath'), (32.50, 35.03, 'hangup'),
    (35.03, DUR + 1, 'loop'),
]


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    if name in ('hook', 'loop'): return r_v_cu(t, u, 'shout' if name == 'hook' else 'angry', 2.0, stubble=0.0 if name == 'hook' else 1.0)
    if name == 'robot1': return r_v_cu(t, u, 'squint', 2.2)
    if name == 'robot2': return r_v_cu(t, u, 'shock', 2.5)
    if name == 'timelapse': return r_timelapse(t, u)
    if name == 'cat_sing': return r_cat_sing(t, u)
    if name == 'n_cu1': return r_n_cu(t, u, 'bored', 3.0)
    if name == 'v_cu2': return r_v_cu(t, u, 'angry', 2.1, stubble=1.0)
    if name == 'n_cu2': return r_n_cu(t, u, 'smug', 3.3)
    if name == 'v_cu3': return r_v_cu(t, u, 'shout', 2.3, stubble=1.0)
    if name == 'n_cu3': return r_n_cu(t, u, 'bored', 3.0)
    if name == 'v_cu4': return r_v_cu(t, u, 'shout', 2.6, stubble=1.0, tint=(1.12, 0.84, 0.82))
    if name == 'reveal': return r_reveal(t, u)
    if name == 'v_sus': return r_v_cu(t, u, 'squint', 2.2, stubble=1.0, look=-0.5)
    if name == 'n_bath': return r_n_bath(t, u)
    return r_hangup(t, u)


LCD = {n: K.lcd_sticker(n) for n in ('143', '97', '51', '12', '2', '144')}


def lcd_count(t):
    if 4.6 <= t < 6.4: return '143'
    if 6.4 <= t < 8.5:
        return ('143', '97', '51', '12', '2')[min(4, int((t - 6.4) / 2.1 * 5))]
    if 33.4 <= t < 35.0: return '144'
    return None


SHOW = K.Show(EPI, 4, ['ДОЗВОНИТЬСЯ', 'В ЖЭК'], hook_t=(0.15, 2.4),
              stickers=[(O.sticker('3 ЧАСА СПУСТЯ', fg=(255, 236, 120), size=56), 6.5, 8.5, 540, 330)],
              flashes=[23.90, 29.80], mosaics=[6.40, 10.30], cap_y={'timelapse': 1360, 'reveal': 1420}, teaser='ДАЛЬШЕ: ПОДВАЛ')


def render(t):
    big = render_scene(t)
    SHOW.apply(big, t, shot_at(t)[2])
    n = lcd_count(t)
    if n:
        img = LCD[n]
        O.overlay(big, img, 540 - img.shape[1] // 2, 1560, 1.0)
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
