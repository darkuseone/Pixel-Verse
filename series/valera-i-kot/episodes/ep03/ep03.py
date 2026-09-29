"""S01E03 «Разведка» — Valera tries to sneak past the grannies' bench in a bedsheet 'snow camouflage'.
  python3 ep03.py test 1 5 20 | frame 12 | all [4]"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
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

EPI = Episode('ep03', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
W = PK.build()
YARD, KIT = W['yard'], W['kitchen']
BENCH = PK.bench_world([('ОБЪЯВЛЕНИЕ', 8, (40, 36, 40)), ('ГОРЯЧЕЙ ВОДЫ НЕТ', 8, (170, 30, 30)), ('ДО 15.12', 16, (40, 36, 40))],
                       crossed=(2,), hand=[('ДО 20.12', 16, (40, 70, 170), 386)])
DOOR_SPR = np.zeros((365, 200, 4), np.uint8)                   # the door leaf as an occluder for the peek
DOOR_SPR[..., :3] = BENCH[225:590, 297:497]; DOOR_SPR[..., 3] = 255
ZX, ZY, ZU = PK.B_ZINA
LX, LY, LU = PK.B_LYUBA
FLOOR, VU = PK.B_FLOOR, PK.B_UNIT
PEEK = (488.0, 690.0)
STAND = (575.0, 700.0)


def mouth(who, t, k=1.6):
    return min(1.0, talk(who, t) * k)


def light_night(v):
    lx, ly = v.opt(410.0, 160.0)
    return Light(amb=(0.8, 0.88, 1.08), keys=[(lx, ly, 1500, (255, 206, 140), 0.75)], rim=(-1, -0.5, (190, 214, 255), 0.35),
                 grad=(1.0, 0.92))


def light_wide(v):
    lx, ly = v.opt(412.0, 380.0)
    return Light(amb=(0.8, 0.88, 1.1), keys=[(lx, ly, 700, (255, 206, 140), 0.7)], rim=(1, -0.5, (190, 214, 255), 0.3))


def crawl_x(t):
    """prone Valera's x along the steps -> bench (close-up world)"""
    if t < 3.8: return 330.0
    if t < 5.05: return lerp(330, 430, (t - 3.8) / 1.25)
    if t < 12.2: return 470.0
    return lerp(470, 520, min(1.0, (t - 12.2) / 1.2))


# ---------------------------------------------------------------- characters
def grannies(CH, v, t, zina_kw=None, lyuba_kw=None):
    zk = dict(expr='smug', look=0.0); zk.update(zina_kw or {})
    lk = dict(knit=True); lk.update(lyuba_kw or {})
    F.babushka(CH, v.cam(LX, LY, LU, flip=True), t, 'lyuba', 'sit', mouth('lyuba', t), **lk)
    F.babushka(CH, v.cam(ZX, ZY, ZU, flip=True), t, 'zina', 'sit', mouth('zina', t), **zk)


def bench_frame(v, t, parts=('grannies',), valera=None, snow=True, zina_kw=None, lyuba_kw=None, door=False):
    CH, FX = K.begin(v.Z)
    big = v.bg()
    if 'grannies' in parts: grannies(CH, v, t, zina_kw, lyuba_kw)
    CH.comp(big, light_night(v))
    if valera:
        CH2 = Chars(); valera(CH2, v); CH2.comp(big, light_night(v))
    if door: K.occlude(big, v, DOOR_SPR, (297, 225))
    if snow: B.falling_snow(FX, v, t, v.X0 - 20, v.Y0 - 20, v.X0 + 380 / v.Z + 20, v.Y0 + 660 / v.Z, n=70, speed=45)
    FX.comp(big)
    fx.vignette(big, 0.35)
    return big


def v_peek(CH, v, t):
    x, y = PEEK
    F.valera(CH, v.cam(x, y, VU), F.VPOSE['stand'], t, mouth('valera', t), 'whisper', 'street', look=1.0)


# ---------------------------------------------------------------- shots
SHOTS = [
    (0.00, 2.70, 'peek'), (2.70, 3.80, 'yard_wide'), (3.80, 5.05, 'crawl1'), (5.05, 6.40, 'zina_cu'), (6.40, 8.20, 'lyuba_cu'),
    (8.20, 10.00, 'sheet_cu'), (10.00, 11.70, 'sheet_ms'), (11.70, 13.85, 'grannies2'), (13.85, 15.20, 'standup'),
    (15.20, 17.20, 'lyuba_cu2'), (17.20, 18.90, 'busted'), (18.90, 21.95, 'bribe'), (21.95, 24.30, 'take'),
    (24.30, 27.80, 'phone'), (27.80, 28.70, 'freeze'), (28.70, 31.00, 'cat1'), (31.00, 33.60, 'cat2'), (33.60, DUR + 1, 'loop'),
]


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def r_peek(t, u):
    v = view_at(BENCH, 520, 385, 2.0 + 0.06 * u, 180, 300)
    big = bench_frame(v, t, (), valera=lambda CH, v_: v_peek(CH, v_, t), door=True)
    return big


def r_yard(t, u, walker=None):
    v = View(YARD, 300 + 8 * u, 150, 1.0)
    CH, FX = K.begin(v.Z)
    big = v.bg()
    bx0, bx1, sy = PK.Y_BENCH
    F.babushka(CH, v.cam(505, sy, PK.Y_UNIT, flip=True), t, 'zina', 'sit', 0.0, 'smug')
    F.babushka(CH, v.cam(570, sy, PK.Y_UNIT, flip=True), t, 'lyuba', 'sit', 0.0, knit=True)
    if walker: walker(CH, v)
    CH.comp(big, light_wide(v))
    B.falling_snow(FX, v, t, 280, 140, 700, 800, n=90, speed=40)
    FX.comp(big)
    fx.vignette(big, 0.35)
    return big


def prone(CH, v, t, crawl, expr='whisper'):
    F.valera_prone(CH, v.cam(crawl_x(t), FLOOR, VU), t, crawl, mouth('valera', t), expr, look=1.0)


def r_crawl1(t, u):
    v = view_at(BENCH, 470, 640, 1.35, 180, 360)
    return bench_frame(v, t, (), valera=lambda CH, v_: prone(CH, v_, t, 1.0))


def gz_face(): return ZX - 1.6 * ZU, ZY - 11.8 * ZU


def gl_face(): return LX - 1.4 * LU, LY - 11.8 * LU


def r_granny_cu(t, u, who, Z=2.6, **kw):
    x, y = gz_face() if who == 'zina' else gl_face()
    v = view_at(BENCH, x, y + 20, Z + 0.06 * u, 180, 300)
    return bench_frame(v, t, ('grannies',), **kw)


def r_sheet_cu(t, u):
    x = crawl_x(t)
    v = view_at(BENCH, x + 7.6 * VU, FLOOR - 3.5 * VU, 2.3 + 0.06 * u, 180, 330)
    return bench_frame(v, t, (), valera=lambda CH, v_: prone(CH, v_, t, 0.0))


def r_sheet_ms(t, u):
    v = view_at(BENCH, 700, 560, 1.15 + 0.03 * u, 180, 360)
    return bench_frame(v, t, ('grannies',), valera=lambda CH, v_: prone(CH, v_, t, 0.0 if t < 12.2 else 1.0),
                       zina_kw=dict(look=-1.0))


def r_grannies2(t, u):
    v = view_at(BENCH, 800, 470, 1.7 + 0.04 * u, 180, 330)
    return bench_frame(v, t, ('grannies',), zina_kw=dict(look=-1.0, expr='smug'))


def r_standup(t, u):
    v = view_at(BENCH, 640, 520, 1.25, 180, 360)
    k = sm(u / 0.3)
    def draw(CH, v_):
        x, y = STAND
        F.valera(CH, v_.cam(x, y, VU), F.vblend(F.VPOSE['stand'], F.VPOSE['fist'], k), t, mouth('valera', t), 'shout', 'street')
        F.flying_sheet(CH, v_.cam(x, y, VU), min(1.0, u / 0.9))
    return bench_frame(v, t, ('grannies',), valera=draw, zina_kw=dict(look=-1.0))


def r_busted(t, u):
    x, y = STAND
    fx_, fy_ = K.face_w(x, y, VU, h=20.6)
    v = view_at(BENCH, fx_, fy_, 2.2 + 0.1 * u, 180, 300)
    def draw(CH, v_):
        F.valera(CH, v_.cam(x, y, VU), F.VPOSE['stand'], t, 0.0, 'sad' if u < 0.9 else 'sly', 'street', look=1.0)
        L = Layer(v_.cam(x, y, VU)); F.ell(L, F.H(-0.8, 23.4 - 2.0 * min(1.0, u / 1.2)), 0.35, 0.55, (170, 220, 255)); CH.add(L)
    return bench_frame(v, t, (), valera=draw)


def r_bribe(t, u):
    v = view_at(BENCH, 700, 520, 1.25 + 0.03 * u, 180, 360)
    k = sm((u - 0.3) / 0.4)
    def draw(CH, v_):
        x, y = STAND
        F.valera(CH, v_.cam(x, y, VU), F.VPOSE['stand'], t, mouth('valera', t), 'sly', 'street', look=1.0,
                 hand_n=F.H(lerp(3.9, 8.0, k), lerp(10.4, 14.0, k)), prop_n=(lambda L, h: B.sausage(L, h, 0.3)) if k > 0.2 else None)
    return bench_frame(v, t, ('grannies',), valera=draw, zina_kw=dict(look=-1.0, expr='smug'))


def r_take(t, u):
    v = view_at(BENCH, 760, 500, 1.45, 180, 350)
    got = u > 0.4
    walk = max(0.0, t - 22.4)
    def draw(CH, v_):
        x, y = STAND
        xx = x - 120 * walk
        pose = F.vwalk(t, 8.0) if walk > 0 else F.VPOSE['stand']
        F.valera(CH, v_.cam(xx, y, VU, flip=walk > 0), pose, t, mouth('valera', t), 'smug', 'street',
                 hand_n=None if got else F.H(8.0, 14.0), prop_n=None if got else (lambda L, h: B.sausage(L, h, 0.3)))
    zk = dict(look=-1.0, expr='smug', hand_n=F.H(lerp(3.8, 5.5, min(1.0, u / 0.4)), lerp(4.6, 8.0, min(1.0, u / 0.4))))
    if got: zk['prop_n'] = lambda L, h: B.sausage(L, h, -0.4)
    return bench_frame(v, t, ('grannies',), valera=draw, zina_kw=zk)


def r_phone(t, u):
    x, y = gz_face()
    v = view_at(BENCH, x + 10, y + 30, 2.4 + 0.08 * u, 180, 310)
    zk = dict(look=0.0, expr='smug', hand_n=F.H(3.4, 9.2), prop_n=F.flip_phone)
    return bench_frame(v, t, ('grannies',), zina_kw=zk)


def r_freeze(t, u):
    def walker(CH, v):
        x = 470 + 60 * min(u, 0.3)
        pose = F.vwalk(t, 8.0) if u < 0.3 else F.VPOSE['shout']
        F.valera(CH, v.cam(x, 612, 5.4), pose, t, 0.0, 'shock', 'street')
    return r_yard(t, u, walker)


def r_cat(t, u, Z, sx=180):
    x, y = PK.CAT_K
    hx, hy = x + 4.4 * PK.CAT_K_UNIT, y - 6.9 * PK.CAT_K_UNIT
    v = view_at(KIT, hx, hy, Z + 0.06 * u, sx, 290)
    CH, FX = K.begin(v.Z)
    big = v.bg()
    F.cat(CH, v.cam(x, y, PK.CAT_K_UNIT), t, 'loaf', mouth('cat', t, 2.0), 0.55, look=(0.0, -0.3), tail=0.4)
    CH.comp(big, K.light_kit(v))
    B.snow_in(FX, v, t, PK.WINDOW_OPEN, n=40, drift=(-90, 220))
    FX.comp(big)
    fx.vignette(big, 0.3)
    return big


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    if name in ('peek', 'loop'): return r_peek(t, u)
    if name == 'yard_wide': return r_yard(t, u)
    if name == 'crawl1': return r_crawl1(t, u)
    if name == 'zina_cu': return r_granny_cu(t, u, 'zina', 2.6, zina_kw=dict(look=0.0, expr='smug'))
    if name == 'lyuba_cu': return r_granny_cu(t, u, 'lyuba', 2.6)
    if name == 'sheet_cu': return r_sheet_cu(t, u)
    if name == 'sheet_ms': return r_sheet_ms(t, u)
    if name == 'grannies2': return r_grannies2(t, u)
    if name == 'standup': return r_standup(t, u)
    if name == 'lyuba_cu2': return r_granny_cu(t, u, 'lyuba', 2.9)
    if name == 'busted': return r_busted(t, u)
    if name == 'bribe': return r_bribe(t, u)
    if name == 'take': return r_take(t, u)
    if name == 'phone': return r_phone(t, u)
    if name == 'freeze': return r_freeze(t, u)
    if name == 'cat1': return r_cat(t, u, 3.0)
    return r_cat(t, u, 3.6, 200)


SHOW = K.Show(EPI, 3, ['ОНИ ВИДЯТ', 'ВСЁ'], hook_t=(0.15, 2.5),
              stickers=[(O.sticker('МАСКИРОВКА 100%', fg=(236, 244, 255), size=48), 10.1, 11.6, 540, 520),
                        (O.sticker('СПАЛИЛСЯ', fg=(255, 120, 100), size=64), 27.85, 28.7, 540, 600),
                        (O.sticker('20 СЕК', fg=(255, 236, 120), size=72), 31.6, 33.5, 540, 1560)],
              flashes=[13.85, 24.30], mosaics=[28.70], cap_y={'yard_wide': 1300, 'freeze': 1300}, teaser='ДАЛЬШЕ: ЖЭК')


def render(t):
    big = render_scene(t)
    return SHOW.apply(big, t, shot_at(t)[2])


if __name__ == '__main__':
    EPI.main(render, __file__)
