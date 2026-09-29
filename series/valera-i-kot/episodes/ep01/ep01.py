"""S01E01 «Закалка» — hot water is off; Valera washes... with radiator water. xAI backgrounds, code heroes and effects.
  python3 ep01.py test 1 5 20 | frame 12 | all [4]"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import stage as ST
from stage import View, view_at, Chars, Light, shadow, OUT_W, OUT_H
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as B
from props import panelka as PK
from timeline import DUR, FPS, VOICE, SLUG

COL = dict(valera=(120, 200, 255), cat=(255, 170, 70))
EPI = Episode('ep01', VOICE, DUR, FPS, colors=COL, slug=SLUG)
talk = EPI.talk
W = PK.build()
KIT, BATH, STAIR = W['kitchen'], W['bath'], W['stair']
TUB, TUBXY = W['tub'], W['tub_xy']

RUST = (1.0, 0.62, 0.40)
SHOWER_V = (468.0, 470.0)                  # Valera in the tub (feet hidden)
FLOOR_V = (850.0, 700.0, 17.0)             # Valera on the bathroom floor
STOVE_V = (960.0, 660.0, 16.5)             # Valera by the stove, facing left
T_JET = 20.75                              # radiator valve opens


def begin(Z):
    ST.set_px(ST.px_for_zoom(Z))
    return Chars(), Chars()


def light_bath(v):
    bx, by = v.opt(*PK.BULB)
    return Light(amb=(0.96, 1.0, 1.07), keys=[(bx, by, 900, (255, 214, 150), 0.7)], rim=(1, -0.3, (196, 222, 255), 0.35), grad=(1.06, 0.9))


def light_cold(v):
    bx, by = v.opt(*PK.BULB)
    return Light(amb=(0.9, 1.0, 1.16), keys=[(bx, by, 700, (220, 230, 255), 0.35)], rim=(1, -0.3, (210, 236, 255), 0.45), grad=(1.08, 0.9))


def light_kit(v):
    lx, ly = v.opt(*PK.LAMP_K)
    return Light(amb=(1.0, 0.96, 0.93), keys=[(lx, ly, 1100, (255, 196, 130), 0.8)], rim=(-1, -0.4, (186, 212, 255), 0.35), grad=(1.04, 0.9))


def mouth(who, t, k=1.6):
    return min(1.0, talk(who, t) * k)


# ---------------------------------------------------------------- characters in places
def valera_shower(CH, v, t, **kw):
    x, y = SHOWER_V
    return F.valera(CH, v.cam(x, y, PK.B_UNIT), t=t, **kw)


def head_shower():
    x, y = SHOWER_V
    return x + 0.9 * PK.B_UNIT, y - 21.2 * PK.B_UNIT


def face_w(x, y, un, flip=False, fwd=1.4, h=21.0):
    """world point of Valera's face (between eyes and nose) for close-up framing"""
    return (x - fwd * un) if flip else (x + fwd * un), y - h * un


def cat_rad(CH, v, t, **kw):
    x, y = PK.CAT_K
    return F.cat(CH, v.cam(x, y, PK.CAT_K_UNIT), t=t, pose='loaf', **kw)


def cat_head_w():
    x, y = PK.CAT_K
    return x + 4.4 * PK.CAT_K_UNIT, y - 6.9 * PK.CAT_K_UNIT


def tub_front(big, v):
    ST.blit_world(big, v, TUB, int(TUBXY[0]), int(TUBXY[1]))


def world_basin(CH, v, x, y, unit, fill=None):
    L = Layer(v.cam(x, y, unit)); B.basin(L, (1000.0, 1000.0), fill); F.outline(L); CH.add(L)


# ---------------------------------------------------------------- shots
SHOTS = [
    (0.00, 2.40, 'hook'), (2.40, 3.70, 'notice'), (3.70, 5.90, 'towel_ms'), (5.90, 8.00, 'towel_cu'),
    (8.00, 9.40, 'cat_cu1'), (9.40, 10.60, 'kitchen_wide'), (10.60, 13.30, 'stove'), (13.30, 15.90, 'cat_cu2'),
    (15.90, 17.20, 'timelapse'), (17.20, 19.10, 'eureka'), (19.10, 20.65, 'eureka2'), (20.65, 22.20, 'valve'),
    (22.20, 23.95, 'lift'), (23.95, 25.30, 'pour'), (25.30, 28.20, 'rust_cu'), (28.20, 30.30, 'cat_cu3'),
    (30.30, 31.80, 'calendar'), (31.80, 33.60, 'cat_end'), (33.60, DUR + 1, 'loop'),
]
FLASH_AT = [2.40, 20.65, 24.35]
MOSAIC_AT = [9.40, 30.30]
CAP_Y = {'kitchen_wide': 1180, 'timelapse': 1380}


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def r_hook(t, u, rust=False):
    hx, hy = head_shower()
    fx_, fy_ = face_w(SHOWER_V[0], SHOWER_V[1], PK.B_UNIT, h=20.6)
    Z = 2.25 + (0.12 * u if rust else 0.0)
    v = view_at(BATH, fx_, fy_, Z, 180, 290)
    CH, FX = begin(Z)
    big = v.bg()
    if rust:
        valera_shower(CH, v, t, pose=F.VPOSE['stand'], expr='blissful', mouth=mouth('valera', t), outfit='towel', tint=RUST, wet=1)
    else:
        valera_shower(CH, v, t, pose=F.VPOSE['shiver'], expr='shout', mouth=max(0.5, mouth('valera', t)), outfit='towel',
                      cold=0.8, wet=1, breath=False)
    CH.comp(big, light_cold(v) if not rust else light_bath(v))
    if not rust:
        B.spray(FX, v, t, PK.SHOWER, spread=60, drop=260, n=90)
    FX.comp(big)
    if rust:
        B.steam(big, v, t, hx - 10, hy - 20, 0.0, n=7, rise=120, size=34, a=0.5)
    fx.vignette(big, 0.3)
    if not rust: B.shake(big, t, 8, 37)
    return big


def r_notice(t, u):
    v = view_at(STAIR, 190, 418, 2.0 + 0.5 * sm(u / 1.3), 180, 300)
    big = v.bg()
    k = 0.85 + 0.15 * math.sin(t * 40) * (1 if (t * 7) % 1 < 0.3 else 0)          # lamp flicker
    fx.grade(big, (k, k, k * 1.03))
    fx.vignette(big, 0.4)
    return big


def r_towel_ms(t, u):
    x, y, un = FLOOR_V
    v = view_at(BATH, 860, 450, 1.05 + 0.03 * u, 180, 330)
    CH, FX = begin(v.Z)
    big = v.bg()
    shadow(big, v, x + 10, y, 6 * un, 1.0 * un)
    shiv = 0.25 * math.sin(t * 60)
    F.valera(CH, v.cam(x + shiv, y, un), F.VPOSE['hips'], t, mouth('valera', t), 'proud', 'towel', cold=0.6, wet=1)
    CH.comp(big, light_cold(v))
    fx.vignette(big, 0.3)
    return big


def r_towel_cu(t, u):
    x, y, un = FLOOR_V
    hx, hy = face_w(x, y, un, h=19.5)
    v = view_at(BATH, hx, hy, 1.9 + 0.08 * u, 180, 290)
    CH, FX = begin(v.Z)
    big = v.bg()
    shiv = 0.12 * math.sin(t * 55)
    F.valera(CH, v.cam(x + shiv, y, un), F.VPOSE['proud'], t, mouth('valera', t), 'proud', 'towel', cold=0.7, wet=1)
    CH.comp(big, light_cold(v))
    fx.vignette(big, 0.3)
    return big


def kitchen_fx(big, v, t, FX, haze=True):
    B.snow_in(FX, v, t, PK.WINDOW_OPEN, n=46, drift=(-90, 220))
    FX.comp(big)
    if haze: B.haze(big, v, t, (PK.RAD[0], PK.RAD[1] - 70, PK.RAD[2], PK.RAD[1] + 10), amp=8)
    fx.vignette(big, 0.28)


def r_cat(t, u, Z, sx=180, sy=280, lid=None):
    hx, hy = cat_head_w()
    v = view_at(KIT, hx, hy, Z + 0.06 * u, sx, sy)
    CH, FX = begin(v.Z)
    big = v.bg()
    m = mouth('cat', t, 2.0)
    if lid is None:
        lid = 0.55 if talk('cat', t) > 0.02 or t > 8.3 else 0.95
    cat_rad(CH, v, t, mouth=m, lid=lid, tail=0.5)
    CH.comp(big, light_kit(v))
    kitchen_fx(big, v, t, FX)
    return big


def r_kitchen_wide(t, u):
    v = View(KIT, 420 - 6 * u, 80, 1.0 + 0.04 * u)
    CH, FX = begin(v.Z)
    big = v.bg()
    cat_rad(CH, v, t, lid=0.8, tail=0.8)
    CH.comp(big, light_kit(v))
    kitchen_fx(big, v, t, FX)
    return big


def r_stove(t, u):
    x, y, un = STOVE_V
    v = view_at(KIT, 985, 360, 1.18 + 0.04 * u, 180, 330)
    CH, FX = begin(v.Z)
    big = v.bg()
    shadow(big, v, x - 8, y, 6 * un, 1.0 * un)
    up = sm((t - 11.3) / 0.35)
    F.valera(CH, v.cam(x, y, un, flip=True), F.VPOSE['point'], t, mouth('valera', t), 'shout' if t > 11.4 else 'proud', 'towel',
             wet=1, hand_n=(1000 + lerp(4.5, 5.8, up), 1000 - lerp(13.0, 25.0, up)),
             prop_n=lambda L, h: B.basin(L, (h[0] + 0.4, h[1] - 1.2), scale=0.9, tilt=-0.25))
    CH.comp(big, light_kit(v))
    FX.comp(big)
    fx.vignette(big, 0.28)
    return big


def draw_clock(FX, v, t, speed=40.0):
    cx, cy, r = PK.CLOCK
    L = Layer(v.wcam())
    a_m = t * speed; a_h = a_m / 12
    F.cap(L, (cx, cy), (cx + math.sin(a_m) * r * 0.8, cy - math.cos(a_m) * r * 0.8), 1.6, 1.2, (30, 24, 20))
    F.cap(L, (cx, cy), (cx + math.sin(a_h) * r * 0.5, cy - math.cos(a_h) * r * 0.5), 2.2, 1.8, (30, 24, 20))
    FX.add(L)


def r_timelapse(t, u):
    v = view_at(KIT, 1128, 240, 1.45, 180, 300)
    CH, FX = begin(v.Z)
    big = v.bg()
    draw_clock(FX, v, t)
    FX.comp(big)
    if t > 16.3: B.steam(big, v, t, PK.KETTLE[0], PK.KETTLE[1], 16.3, n=5, rise=110, size=18, a=0.6)
    fx.vignette(big, 0.3)
    return big


def r_eureka(t, u, push=False):
    x, y, un = STOVE_V
    hx, hy = face_w(x, y, un, flip=True, h=20.3)
    Z = (2.0 + 0.1 * u) if not push else (2.2 + 0.45 * sm(u / 0.6))
    v = view_at(KIT, hx, hy, Z, 180, 300)
    CH, FX = begin(v.Z)
    big = v.bg()
    look = -1.0 if t > 17.9 else 0.0
    expr = 'whisper' if not push else ('shout' if t > 19.3 else 'sly')
    F.valera(CH, v.cam(x, y, un, flip=True), F.VPOSE['stand'], t, mouth('valera', t), expr, 'towel', look=-look, wet=1)
    CH.comp(big, light_kit(v))
    fx.vignette(big, 0.3)
    if push and t > 19.3: fx.speed_lines(big, t, 0.5)
    return big


def r_valve(t, u):
    v = view_at(KIT, 790, 470, 1.75 + 0.08 * u, 180, 350)
    CH, FX = begin(v.Z)
    big = v.bg()
    world_basin(CH, v, 752, 552, 11.0, fill=(140, 72, 34) if t > T_JET + 0.3 else None)
    x, y, un = 868.0, 660.0, 16.5
    F.valera(CH, v.cam(x, y, un, flip=True), F.VPOSE['stand'], t, mouth('valera', t), 'shock' if t > T_JET else 'sly', 'towel',
             wet=1, lean=1.6, hand_n=(1000 + (868 - 736) / un, 1000 - (660 - 432) / un),
             prop_n=lambda L, h: B.screwdriver(L, h, ang=math.pi + 0.5))
    CH.comp(big, light_kit(v))
    B.jet(FX, v, t, T_JET, (730, 432), (752, 540), arc=22, width=4.0)
    FX.comp(big)
    B.steam(big, v, t, 748, 530, T_JET + 0.1, n=6, rise=140, size=26, a=0.6)
    fx.vignette(big, 0.3)
    return big


def r_lift(t, u):
    x, y, un = 640.0, 670.0, 16.5
    v = view_at(KIT, 650, 400, 1.15 + 0.05 * u, 180, 330)
    CH, FX = begin(v.Z)
    big = v.bg()
    shadow(big, v, x + 10, y, 6 * un, 1.0 * un)
    lift = sm(u / 0.5)
    bh = lerp(14.0, 27.5, lift)
    tgt_n = (1000 + 5.6, 1000 - bh); tgt_f = (1000 - 3.6, 1000 - bh)
    info = F.valera(CH, v.cam(x, y, un), F.VPOSE['overhead'], t, mouth('valera', t), 'shout', 'towel', wet=1,
                    hand_n=tgt_n, hand_f=tgt_f)
    L = Layer(v.cam(x, y, un)); B.basin(L, (1000 + 1.0, 1000 - bh - 0.9), (140, 72, 34), scale=1.15); F.outline(L); CH.add(L)
    CH.comp(big, light_kit(v))
    FX.comp(big)
    B.steam(big, v, t, x + 0.8 * un, y - (bh + 1.5) * un, 22.2, n=7, rise=170, size=30, a=0.55)
    kitchen_fx(big, v, t, Chars(), haze=True)
    return big


def r_pour(t, u):
    hx, hy = head_shower()
    v = view_at(BATH, hx + 10, hy + 40, 1.8, 180, 300)
    CH, FX = begin(v.Z)
    big = v.bg()
    k = sm(u / 0.4)
    rust = sm((u - 0.5) / 0.5)
    tint = tuple(lerp(1.0, c, rust) for c in RUST)
    valera_shower(CH, v, t, pose=F.VPOSE['stand'], expr='shock' if u < 0.6 else 'blissful', outfit='towel', wet=1, tint=tint,
                  hand_n=(1000 + 3.0, 1000 - lerp(18, 27.5, k)), prop_n=lambda L, h: B.ladle(L, h, (140, 72, 34)))
    CH.comp(big, light_bath(v))
    tub_front(big, v)
    if u > 0.35:
        x0 = SHOWER_V[0] + 6.5 * PK.B_UNIT; y0 = SHOWER_V[1] - 27.0 * PK.B_UNIT
        B.jet(FX, v, t, 23.95 + 0.35, (x0, y0), (hx + 6, hy - 30), arc=10, width=5.0, grow=0.15)
    FX.comp(big)
    B.steam(big, v, t, hx, hy - 20, 24.3, n=9, rise=150, size=44, a=0.7)
    fx.vignette(big, 0.3)
    return big


def r_calendar(t, u):
    x0, y0, x1, y1 = PK.CALENDAR
    v = view_at(KIT, (x0 + x1) / 2, y0 + 96, 3.0 + 0.3 * sm(u / 1.5), 180, 300)
    big = v.bg()
    fx.vignette(big, 0.35)
    return big


def r_cat_end(t, u):
    hx, hy = cat_head_w()
    v = view_at(KIT, hx - 20, hy + 10, 2.1 + 0.08 * u, 180, 320)
    CH, FX = begin(v.Z)
    big = v.bg()
    cat_rad(CH, v, t, mouth=mouth('cat', t, 2.0), lid=0.7 + 0.25 * sm((t - 33.0) / 0.5), tail=0.3)
    CH.comp(big, light_kit(v))
    kitchen_fx(big, v, t, FX)
    return big


def r_loop(t, u):
    hx, hy = head_shower()
    v = view_at(BATH, hx + 40, hy + 60, 1.6, 180, 300)
    CH, FX = begin(v.Z)
    big = v.bg()
    reach = sm(u / 0.4)
    valera_shower(CH, v, t, pose=F.VPOSE['stand'], expr='smug', outfit='towel', wet=1, tint=RUST,
                  hand_n=(1000 + lerp(4.0, 9.6, reach), 1000 - lerp(12, 3.6, reach)))
    CH.comp(big, light_bath(v))
    tub_front(big, v)
    fx.vignette(big, 0.3)
    return big


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    if name == 'hook': return r_hook(t, u)
    if name == 'notice': return r_notice(t, u)
    if name == 'towel_ms': return r_towel_ms(t, u)
    if name == 'towel_cu': return r_towel_cu(t, u)
    if name == 'cat_cu1': return r_cat(t, u, 3.0)
    if name == 'kitchen_wide': return r_kitchen_wide(t, u)
    if name == 'stove': return r_stove(t, u)
    if name == 'cat_cu2': return r_cat(t, u, 3.6, 200, 300)
    if name == 'timelapse': return r_timelapse(t, u)
    if name == 'eureka': return r_eureka(t, u)
    if name == 'eureka2': return r_eureka(t, u, push=True)
    if name == 'valve': return r_valve(t, u)
    if name == 'lift': return r_lift(t, u)
    if name == 'pour': return r_pour(t, u)
    if name == 'rust_cu': return r_hook(t, u, rust=True)
    if name == 'cat_cu3': return r_cat(t, u, 3.3, 170, 290, lid=0.35)
    if name == 'calendar': return r_calendar(t, u)
    if name == 'cat_end': return r_cat_end(t, u)
    return r_loop(t, u)


# ---------------------------------------------------------------- overlays
BADGE = O.make_badge('СЕЗОН 1 • СЕРИЯ 1/6')
HOOK = O.winter_title(['ГОРЯЧУЮ', 'ОТКЛЮЧИЛИ'], 64)
TEASE = O.winter_title(['ДАЛЬШЕ: КАССА'], 40)
STICKERS = [
    (O.sticker('-20°', fg=(150, 210, 255), size=72), 9.55, 10.6, 330, 470),
    (O.sticker('+28°', fg=(255, 120, 90), size=72), 9.85, 10.6, 760, 1250),
    (O.sticker('100°', fg=(255, 150, 80), size=64), 21.0, 22.2, 780, 560),
    (O.sticker('14 ДНЕЙ', fg=(255, 236, 120), size=64), 31.0, 33.5, 540, 1520),
]


def render(t):
    big = render_scene(t)
    a, b, name = shot_at(t)
    for img, t0, t1, cx, cy in STICKERS: O.draw_sticker(big, img, t, t0, t1, cx, cy)
    O.overlay(big, BADGE, 36, 96, 1.0)
    if 0.2 <= t < 2.3:
        k = min(1.0, (t - 0.2) / 0.1) * (1 - sm((t - 2.1) / 0.2))
        O.overlay(big, HOOK, 0, 170, k)
    EPI.captions.draw(big, t, CAP_Y.get(name, 1330))
    if t >= DUR - 0.8:
        O.overlay(big, TEASE, 0, 1560, min(1.0, (t - (DUR - 0.8)) / 0.15))
    for fa in FLASH_AT:
        if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
    for ma in MOSAIC_AT:
        if ma <= t < ma + 0.3: O.mosaic(big, int(lerp(40, 1, (t - ma) / 0.3)))
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
