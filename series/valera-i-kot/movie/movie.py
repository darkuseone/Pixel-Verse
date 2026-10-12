"""«Валера и кот: ПРОПУСКНОЙ РЕЖИМ» — new-year mini-movie, 16:9 1920x1080, rendered by shots (timeline.py).
  python3 movie.py sheet <shot|index> ...   12-up mini sheet of shot middles (build/valera-i-kot-movie/msheet.png)
  python3 movie.py test|frames t ...  |  all  |  shots <i|name> ...      (engine/episode.py CLI)
  python3 mix.py                      -> final.mp4"""
import os
os.environ['PV_WIDE'] = '1'
import sys, pathlib, math
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine')); sys.path.insert(0, str(HERE))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import stage as ST
from stage import View, view_at, Chars, Light, OUT_W, OUT_H
from scene import Layer, sm, lerp
import overlays as O
import fx
import paths as P
from episode import Episode
from props import folk as F
from props import folkmates as M
from props import bytfx as B
from props import panelka as PK
from props import vikit as K
from props import newyear as NY
from props import decals as D
from props import rusigns as R
import timeline as TL

assert (OUT_W, OUT_H) == (1920, 1080)
SX, SY = 320, 180
COL = dict(K.COL, kolyan=(150, 220, 120), semenych=(240, 196, 120))
EPI = Episode('movie', TL.VOICE, TL.DUR, TL.FPS, colors=COL, slug=TL.SLUG,
              endcard=dict(style='default', lang='ru', sec=3.0, cy=900))
talk = EPI.talk
BK = f'{TL.SLUG}-movie'


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def begin():
    ST.set_px(1)                                     # heroes at full logical resolution: 1 hero px = 3 output px
    return Chars(), Chars()


# ======================================================================================= worlds + decor
def load(name): return PK.q(Image.open(PK.BG / name).convert('RGB'))


W = PK.build()
PARTY = load('kitchen_party.png')
GARAGE = load('garage.png')
SROOM = load('semenych_room.png')
SHOP = W['shop']
CNT, CNTXY = W['counter'], W['counter_xy']
YARD = W['yard']
HALL = load('hallway.png')
TABLE = load('table_top.png')
SUMMER = load('yard_summer.png')
BENCH = PK.bench_world([('ОБЪЯВЛЕНИЕ', 8, (40, 36, 40)), ('31.12', 16, (170, 30, 30)), ('ПЕТАРДЫ —', 8, (40, 36, 40)),
                        ('ТОЛЬКО ДЕТЯМ', 8, (40, 36, 40)), ('ЖЭК №3', 8, (60, 60, 120))])

INK, RED, BLUE, PAPER = (34, 30, 30), (176, 30, 34), (40, 60, 150), (240, 234, 214)
D.attach(PARTY, [
    (R.plate(46, 44, ['ДЕКАБРЬ', '31'], bg=(244, 242, 232), colors=[RED, INK], weights=[0.5, 1.0], border=None, pad=2), 666, 192),
    (R.plate(60, 30, ['ВОДУ', 'БЕРЕГИ!'], bg=(250, 220, 90), fg=INK, border=(60, 50, 20), weights=[1, 1], pad=1.5), 832, 262),
    (R.plate(26, 18, ['СОЧИ', '89'], bg=(90, 170, 220), fg=(255, 255, 255), border=(255, 255, 255), pad=1.2, round_=3), 1050, 250),
    (R.plate(24, 50, ['СОВЕЦКОЕ', 'ИГРИСТОЕ'], bg=(236, 212, 140), colors=[RED, INK], border=(150, 110, 40), pad=1.2, weights=[1, 0.8]), 946, 420),
    (R.plate(48, 46, ['ПШЕ-', 'НИЧКА'], bg=(244, 236, 214), fg=BLUE, border=(120, 110, 90), pad=1.5), 1040, 398),
    (R.plate(48, 44, ['ВОДКА', '«ЛЁД»'], bg=(214, 230, 244), colors=[INK, BLUE], border=(120, 130, 150), pad=1.5), 1124, 418),
    (R.plate(60, 40, ['ГРАМОТА', 'ЗА 20 ЛЕТ', 'НА СКЛАДЕ'], bg=(250, 238, 200), colors=[RED, INK, INK], border=(170, 130, 50),
             weights=[1.0, 0.6, 0.6], pad=2), 1110, 120),
])
D.attach(GARAGE, [
    (R.plate(82, 76, ['ЖИГУ', 'НЕ', 'ТРОГАТЬ!'], bg=(236, 226, 196), colors=[RED, INK, RED], border=(90, 70, 40), pad=3, wear=0.3, tilt=-2), 456, 92),
    (R.plate(46, 54, ['ЯНВАРЬ', '1987'], bg=(244, 242, 232), colors=[RED, INK], border=None, pad=2), 557, 152),
    (R.plate(60, 30, ['ГАРАЖ №14', 'КОЛЯН'], bg=(70, 110, 70), fg=(240, 240, 220), border=(30, 40, 30), pad=2, wear=0.4), 1040, 250),
    (R.plate(46, 14, ['НУ 777'], bg=(240, 240, 240), fg=INK, border=INK, pad=1.2), 304, 492),
])
D.attach(SROOM, [
    (R.plate(130, 46, ['ТИШЕ!', 'ИДЁТ ЧТЕНИЕ'], bg=PAPER, colors=[RED, INK], border=(120, 100, 70), pad=3, tilt=3), 392, 238),
    (R.plate(30, 30, ['КЕ-', 'ФИР'], bg=(240, 240, 236), fg=BLUE, border=None, pad=1.5), 148, 222),
])
D.attach(SHOP, [
    (R.plate(200, 58, ['АЛКОГОЛЬ', 'ПОСЛЕ 21:00', 'НЕ ПРОДАЁМ'], bg=(250, 246, 230), colors=[RED, INK, RED], border=(150, 30, 30),
             bw=2, pad=3), 515, 66),
    (R.plate(112, 50, ['КРЕДИТ', 'НЕ ДАЁМ.', 'И НЕ ПРОСИТЕ'], bg=(250, 230, 120), fg=INK, border=INK, pad=3, tilt=-3), 1112, 64),
    (R.plate(160, 44, ['ВАС ОБСЛУЖИВАЕТ', 'ТАМАРА'], bg=(240, 240, 236), colors=[INK, RED], border=(60, 60, 70), pad=3, weights=[0.6, 1]), 1010, 575),
    (R.plate(86, 22, ['ПАКЕТ — 90 Р.'], bg=(255, 226, 60), fg=INK, border=INK, pad=1.5), 930, 438),
])
D.attach(BENCH, [
    (R.plate(64, 32, ['КПП'], bg=(214, 196, 150), fg=RED, border=(120, 90, 50), pad=2, hand=True, tilt=-4, wear=0.3), 752, 462),
    (R.plate(120, 58, ['ПОСТОРОННИМ', 'ВХОД', 'ВОСПРЕЩЁН', '— ЗИНА'], bg=PAPER, colors=[INK, INK, INK, BLUE], border=(90, 80, 70),
             pad=3, weights=[1, 1, 1, 0.8]), 336, 452),
])
D.attach(HALL, [(R.plate(80, 34, ['ДЕМБЕЛЬ', 'НА ПОСТУ'], bg=PAPER, colors=[INK, RED], border=(90, 70, 40), pad=2, tilt=4), 760, 210)])

# party table occluder (everything ON the table is in front of the people sitting behind it)
PMASK = np.zeros(PARTY.shape[:2], bool)
_m = Image.new('L', (PARTY.shape[1], PARTY.shape[0]), 0); _d = ImageDraw.Draw(_m)
_d.rectangle([0, 446, 1280, 720], fill=1)
_d.ellipse([28, 398, 352, 572], fill=1); _d.polygon([(50, 335), (62, 328), (168, 470), (150, 478)], fill=1)          # basin + ladle
_d.ellipse([455, 452, 680, 548], fill=1)
for (cx, cy, r) in ((493, 438, 26), (535, 425, 28), (590, 425, 28), (632, 452, 26), (512, 470, 26), (562, 462, 28), (605, 475, 26)):
    _d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=1)                                                            # tangerines
_d.rounded_rectangle([718, 356, 842, 524], 18, fill=1)                                                              # jar
_d.rectangle([962, 262, 1002, 350], fill=1); _d.rounded_rectangle([934, 330, 1022, 528], 14, fill=1)               # champagne
_d.rectangle([1056, 268, 1090, 335], fill=1); _d.rounded_rectangle([1030, 320, 1112, 534], 14, fill=1)             # vodka 1
_d.rectangle([1132, 292, 1168, 352], fill=1); _d.rounded_rectangle([1104, 340, 1196, 562], 14, fill=1)             # vodka 2
_d.rectangle([800, 462, 944, 545], fill=1); _d.rectangle([1000, 462, 1060, 590], fill=1)                            # glasses, candle
PMASK = np.array(_m).astype(bool)


def occlude(big, v, bg0, mask):
    xs, ys = v.grid()
    m = mask[ys[:, None], xs[None, :]]
    big[m] = bg0[m]


# ======================================================================================= lights
def light_party(v):
    cx, cy = v.opt(1030, 470); tx, ty = v.opt(930, 160)
    return Light(amb=(0.98, 0.92, 0.88), keys=[(cx, cy, 1300 * v.Z, (255, 196, 120), 0.6), (tx, ty, 900 * v.Z, (180, 210, 255), 0.25)],
                 rim=(-1, -0.4, (170, 196, 255), 0.4), grad=(1.04, 0.9))


def light_garage(v):
    lx, ly = v.opt(650, 110)
    return Light(amb=(0.86, 0.84, 0.82), keys=[(lx, ly, 1500 * v.Z, (255, 206, 140), 0.75)], rim=(1, -0.4, (170, 200, 255), 0.35), grad=(1.04, 0.86))


def light_sroom(v):
    lx, ly = v.opt(810, 290)
    return Light(amb=(0.86, 0.84, 0.84), keys=[(lx, ly, 1400 * v.Z, (220, 255, 190), 0.6)], rim=(1, -0.5, (180, 206, 255), 0.35), grad=(1.02, 0.86))


def light_shop(v): return K.light_shop(v)


def light_bench(v):
    lx, ly = v.opt(410.0, 180.0)
    return Light(amb=(0.8, 0.88, 1.08), keys=[(lx, ly, 1500 * v.Z, (255, 206, 140), 0.75)], rim=(-1, -0.5, (190, 214, 255), 0.35), grad=(1.0, 0.92))


def light_yard(v):
    lx, ly = v.opt(412.0, 380.0)
    return Light(amb=(0.8, 0.88, 1.1), keys=[(lx, ly, 700 * v.Z, (255, 206, 140), 0.7)], rim=(1, -0.5, (190, 214, 255), 0.3))


def light_hall(v):
    lx, ly = v.opt(650, 60)
    return Light(amb=(1.0, 0.95, 0.88), keys=[(lx, ly, 1500 * v.Z, (255, 206, 140), 0.7)], rim=(1, -0.3, (255, 236, 200), 0.3))


def light_summer(v):
    sx, sy = v.opt(1100, -100)
    return Light(amb=(1.04, 1.0, 0.92), keys=[(sx, sy, 2400, (255, 236, 180), 0.5)], rim=(1, -0.6, (255, 240, 190), 0.5), grad=(1.04, 0.94))


# ======================================================================================= camera
_BG = {}


def blurred(world, v, r):
    key = (id(world), round(v.X0, 1), round(v.Y0, 1), round(v.Z, 3), r)
    if key not in _BG:
        if len(_BG) > 8: _BG.clear()
        big = v.bg()
        if r: big = np.array(Image.fromarray(big).filter(ImageFilter.GaussianBlur(r)))
        _BG[key] = big
    return _BG[key].copy()


def hview(world, wx, wy, Z, sx, sy):
    v = View(world, 0, 0, Z)
    v.X0, v.Y0 = wx - sx / Z, wy - sy / Z
    return v


def scene(world, cx, cy, Z, light, draw=None, pre=None, post=None, mask=None, back=None):
    """medium/wide shot: one camera for background and heroes. back = heroes behind `mask` (occluder), draw = in front"""
    v = view_at(world, cx, cy, Z, SX, SY)
    big = v.bg()
    if pre: pre(big, v)
    bg0 = big.copy() if mask is not None else None
    if back:
        CH, _ = begin(); back(CH, v); CH.comp(big, light(v))
        if mask is not None: occlude(big, v, bg0, mask)
    if draw:
        CH, _ = begin(); draw(CH, v); CH.comp(big, light(v))
    if post: post(big, v)
    fx.vignette(big, 0.3)
    return big


def cu(world, head, at, Zh, light, draw, Zb=1.3, blur=5, pre=None, post=None, bg_center=None):
    """close-up: background soft at zoom Zb (<= 1.45), the hero at zoom Zh with its `head` world point pinned at logical `at`"""
    bx, by = bg_center or head
    vb = view_at(world, bx, by, Zb, at[0], at[1])
    big = blurred(world, vb, blur)
    if pre: pre(big, vb)
    vh = hview(world, head[0], head[1], Zh, at[0], at[1])
    CH, _ = begin(); draw(CH, vh); CH.comp(big, light(vb))
    if post: post(big, vb, vh)
    fx.vignette(big, 0.3)
    return big


def snow(big, v, t, n=70, speed=45):
    FXL = Chars()
    B.falling_snow(FXL, v, t, v.X0 - 20, v.Y0 - 20, v.X0 + 680 / v.Z, v.Y0 + 380 / v.Z, n=n, speed=speed)
    FXL.comp(big)


# ======================================================================================= props
def binoculars(L, h, ang=0.0):
    x, y = h
    for dx in (-0.55, 0.55):
        F.cap(L, (x + dx, y), (x + dx + 1.3, y - 0.15), 0.5, 0.5, (40, 40, 46), None, (24, 24, 28))
        F.ell(L, (x + dx + 1.4, y - 0.15), 0.42, 0.45, (120, 170, 220), 0, (200, 230, 255))
    F.cap(L, (x - 0.55, y), (x + 0.55, y), 0.25, 0.25, (60, 60, 66))


def notebook(L, h, open_=True):
    x, y = h
    if open_:
        F.poly(L, [(x - 2.4, y - 1.2), (x, y - 0.8), (x, y + 0.9), (x - 2.4, y + 0.5)], (240, 234, 214))
        F.poly(L, [(x, y - 0.8), (x + 2.4, y - 1.2), (x + 2.4, y + 0.5), (x, y + 0.9)], (240, 234, 214))
        for k in range(4):
            F.cap(L, (x - 2.0, y - 0.8 + k * 0.38), (x - 0.4, y - 0.5 + k * 0.38), 0.05, 0.05, (60, 60, 120))
            F.cap(L, (x + 0.4, y - 0.5 + k * 0.38), (x + 2.0, y - 0.8 + k * 0.38), 0.05, 0.05, (60, 60, 120))
    else:
        F.poly(L, [(x - 1.2, y - 1.6), (x + 1.2, y - 1.6), (x + 1.2, y + 1.6), (x - 1.2, y + 1.6)], (60, 90, 60))


def walkie(L, h):
    x, y = h
    F.poly(L, [(x - 0.6, y - 1.4), (x + 0.6, y - 1.4), (x + 0.6, y + 1.0), (x - 0.6, y + 1.0)], (40, 44, 40))
    F.cap(L, (x + 0.3, y - 1.4), (x + 0.3, y - 3.2), 0.12, 0.12, (30, 30, 30))
    F.dot(L, (x - 0.2, y - 0.9), (255, 80, 60), 0.18)


def bottle(L, h, empty=True):
    x, y = h
    F.cap(L, (x, y + 1.6), (x, y - 1.8), 0.85, 0.85, (200, 222, 230), (240, 250, 255), (150, 170, 180))
    F.cap(L, (x, y - 1.8), (x, y - 3.2), 0.32, 0.3, (200, 222, 230))
    F.poly(L, [(x - 0.75, y - 0.3), (x + 0.75, y - 0.3), (x + 0.75, y + 0.9), (x - 0.75, y + 0.9)], (244, 236, 214))


def tin_can(L, h, string=False):
    x, y = h
    F.cap(L, (x, y - 0.7), (x, y + 0.7), 0.6, 0.6, (176, 180, 188), (220, 224, 230), (130, 134, 140))
    F.poly(L, [(x - 0.6, y - 0.3), (x + 0.6, y - 0.3), (x + 0.6, y + 0.4), (x - 0.6, y + 0.4)], (200, 40, 40))
    F.ell(L, (x, y - 0.7), 0.6, 0.22, (150, 154, 160))
    if string: F.cap(L, (x, y + 0.7), (x - 6.0, y - 9.0), 0.08, 0.08, (250, 250, 240))


def towel_flag(L, h, t):
    x, y = h
    F.cap(L, (x, y + 2.0), (x, y - 8.0), 0.15, 0.15, (150, 110, 70))
    w = 0.3 * math.sin(t * 7)
    F.poly(L, [(x, y - 8.0), (x + 4.4, y - 7.7 + w), (x + 4.6, y - 5.2 + w), (x, y - 5.4)], (246, 246, 250))
    F.cap(L, (x + 0.2, y - 6.0), (x + 4.4, y - 5.9 + w), 0.12, 0.12, (210, 80, 70))


def shawl(L, head, s=1.0, col=(150, 146, 150)):
    x, y = head
    F.ell(L, (x - 0.2, y - 0.6), 3.3 * s, 3.5 * s, col, 0, tuple(min(255, c + 30) for c in col), tuple(int(c * 0.75) for c in col))
    F.cap(L, (x - 2.0, y + 2.6), (x + 1.8, y + 2.8), 0.7, 0.7, tuple(int(c * 0.75) for c in col))


def ketchup(L, h):
    x, y = h
    F.cap(L, (x, y + 1.0), (x, y - 1.6), 0.7, 0.55, (200, 30, 30), (240, 70, 60), (150, 20, 20))
    F.cap(L, (x, y - 1.6), (x, y - 2.3), 0.25, 0.12, (240, 240, 240))


# ======================================================================================= hero placement
VP = (405.0, 600.0, 11.5)           # Valera at the party table (behind it, facing right)
VW_ = (300.0, 610.0, 11.5)          # Valera at the window with the walkie-talkie
CAT_SILL = (548.0, 338.0, 5.6)      # cat on the windowsill
ZP = (892.0, 482.0, 11.0)           # Zina at the table (seat point)
LP = (408.0, 496.0, 12.0)           # Lyuba at the table
KG = (640.0, 615.0, 15.0)           # Kolyan in the garage, facing left (wall phone)
PHONE_G = (500.0, 262.0)
SR = (790.0, 690.0, 15.5)           # Semenych in his room, facing left (desk phone)
PHONE_S = (716.0, 372.0)
TX, TY, TU = PK.SH_TAMARA
SK = (600.0, 712.0, 21.0)           # Kolyan in the shop
SS = (790.0, 712.0, 20.0)           # Semenych at the counter
ZX, ZY, ZU = PK.B_ZINA
LX, LY, LU = PK.B_LYUBA
BF, BU = PK.B_FLOOR, PK.B_UNIT
EX = dict(v01='whisper', v02='proud', v03='sad', v04='proud', v05='shout', v06='shout', v07='squint', v08='squint', v09='whisper',
          v10='sad', v11='shock', v12='shout', v13='sad', v14='angry', v15='sad', v16='angry', v17='sad')


def vex(t, key=None, default='normal'):
    return EX.get(key, default)


def valera_party(CH, v, t, key=None, pose=None, prop=None, hand=None, expr=None):
    x, y, u = VP
    F.valera(CH, v.cam(x, y, u), pose or dict(F.VPOSE['sit'], n=(6.6, 11.2)), t, mouth('valera', t), expr or vex(t, key), 'home',
             hat='ushanka', hand_n=hand, prop_n=prop)


def cat_sill(CH, v, t, lid=0.55, expr='deadpan', extra=None, look=(0.6, -0.1)):
    x, y, u = CAT_SILL
    cam = v.cam(x, y, u)
    F.cat(CH, cam, t=t, pose='loaf', mouth=mouth('cat', t, 2.0), lid=lid, look=look, expr=expr, tail=0.6)
    if extra:
        L = Layer(cam); extra(L); F.outline(L); CH.add(L)


def can_paw(L):
    F.cap(L, F.H(6.2, 1.4), F.H(7.4, 7.2), 0.9, 0.8, (240, 140, 40), (255, 180, 90), (200, 104, 30))
    tin_can(L, F.H(7.6, 8.2), string=True)
    F.ell(L, F.H(7.2, 7.4), 0.95, 0.85, (248, 244, 236), 0, (255, 255, 255), (214, 206, 196))


def grannies(CH, v, t, zk=None, lk=None):
    zk = dict(dict(expr='smug'), **(zk or {}))
    lk = dict(dict(knit=True), **(lk or {}))
    F.babushka(CH, v.cam(LX, LY, LU, flip=True), t, 'lyuba', 'sit', mouth('lyuba', t), **lk)
    F.babushka(CH, v.cam(ZX, ZY, ZU, flip=True), t, 'zina', 'sit', mouth('zina', t), **zk)


def bench_props(big, v, t, journal=False):
    pass


# ======================================================================================= shots
def binocular_mask(big, k=1.0):
    yy, xx = np.ogrid[0:OUT_H, 0:OUT_W]
    r = 470
    m = ((xx - 700) ** 2 + (yy - 540) ** 2 < r * r) | ((xx - 1220) ** 2 + (yy - 540) ** 2 < r * r)
    big[~m] = (8, 8, 10)
    edge = (((xx - 700) ** 2 + (yy - 540) ** 2 < (r + 14) ** 2) | ((xx - 1220) ** 2 + (yy - 540) ** 2 < (r + 14) ** 2)) & ~m
    big[edge] = (40, 40, 46)


def r_bino(t, s, u):
    b0 = TL.first('bino')
    dur = s['t1'] - s['t0']
    raise_ = 0.0 if s is b0 else sm((u - (dur - 1.1)) / 0.4)
    def draw(CH, v):
        zk = dict(expr='smug', hand_n=F.H(2.8, 12.0) if raise_ > 0.5 else None, prop_n=(lambda L, h: binoculars(L, (h[0] - 0.6, h[1] - 0.2))) if raise_ > 0.5 else None)
        grannies(CH, v, t, zk=zk, lk=dict(knit=True))
    big = scene(BENCH, 790, 440 + 6 * math.sin(t * 1.3), 1.1 + 0.03 * u, light_bench, draw, post=lambda b, v: snow(b, v, t))
    binocular_mask(big)
    return big


def r_bino_zina(t, s, u):
    hx, hy = ZX - 1.0 * ZU, ZY - 11.8 * ZU
    big = cu(BENCH, (hx, hy), (330, 190), 3.0, light_bench,
             lambda CH, vh: F.babushka(CH, vh.cam(ZX, ZY, ZU, flip=True), t, 'zina', 'sit', max(0.4, mouth('zina', t)), 'normal',
                                       hand_n=F.H(4.6, 13.6), prop_n=lambda L, h: binoculars(L, (h[0] - 1.6, h[1]))),
             Zb=1.3, blur=4, post=lambda b, vb, vh: snow(b, vb, t))
    binocular_mask(big)
    return big


def valera_window_tiny(big, v, t, glint=True, cat=False, string=False):
    """a tiny figure INSIDE Valera's lit window (clipped to the window glass)"""
    x0, y0, x1, y1 = PK.Y_WINDOW
    keep = big.copy()
    CH, _ = begin()
    if not cat:
        F.valera(CH, v.cam(x0 + 30, y1 + 22, 1.9), F.VPOSE['phone'], t, 0.0, 'squint', 'home', hat='ushanka',
                 hand_n=F.H(5.0, 21.5), prop_n=lambda L, h: binoculars(L, h))
    else:
        F.cat(CH, v.cam(x0 + 40, y1 - 3, 1.5), t, 'loaf', 0.0, 0.6, (0.6, 0.0), 'deadpan')
    CH.comp(big, light_yard(v))
    ax, ay = v.opt(x0 + 4, y0 + 4); bx, by = v.opt(x1 - 4, y1 - 4)
    m = np.ones(big.shape[:2], bool); m[max(0, int(ay)):max(0, int(by)), max(0, int(ax)):max(0, int(bx))] = False
    big[m] = keep[m]
    if glint and (t * 2) % 1 < 0.5:
        gx, gy = v.opt(x0 + 36, y0 + 30); fx.glow(big, gx, gy, 60 * v.Z, (255, 255, 230), 0.8)


def r_window_out(t, s, u):
    def post(big, v):
        snow(big, v, t, 80, 40)
        valera_window_tiny(big, v, t)
    def draw(CH, v):
        x0, x1, sy = PK.Y_BENCH
        F.babushka(CH, v.cam(x0 + 35, sy, PK.Y_UNIT), t, 'zina', 'sit', 0.0, 'smug')
        F.babushka(CH, v.cam(x0 + 70, sy, PK.Y_UNIT), t, 'lyuba', 'sit', 0.0, 'normal')
    return scene(YARD, 470, lerp(330, 300, sm(u / 6)), 1.25 + 0.04 * u, light_yard, draw, post=post)


def r_title(t, s, u):
    v = view_at(YARD, 640, 360, 0.55, SX, SY)
    big = blurred(YARD, v, 5)
    big[:] = (big * 0.6).astype(np.uint8)
    snow(big, v, t, 90, 40)
    a = img('title', lambda: O.winter_title(['ПРОПУСКНОЙ', 'РЕЖИМ'], 120))
    b_ = img('title_sub', lambda: badge('ВАЛЕРА И КОТ • НОВОГОДНИЙ ФИЛЬМ', 34))
    k = min(1.0, u / 0.2)
    O.overlay(big, a, 0, 260, k)
    if u > 0.5: O.overlay(big, b_, (OUT_W - b_.shape[1]) // 2, 720, min(1.0, (u - 0.5) / 0.3))
    return big


# ---------------------------------------------------------------- kitchen / party
def party_fx(big, v, t, cat_extra=None, cat=True):
    bx, by = v.opt(930, 160)                                                 # TV flicker
    fx.glow(big, bx, by, 300 * v.Z, (180, 210, 255), 0.12 + 0.08 * math.sin(t * 23) * math.sin(t * 7))
    cx, cy = v.opt(1030, 478)                                                # candle
    fx.glow(big, cx, cy, 240 * v.Z, (255, 196, 110), 0.28 + 0.08 * math.sin(t * 11))
    for j, (x, y) in enumerate(((35, 68), (95, 60), (168, 22), (215, 32), (270, 44), (320, 46), (405, 44), (445, 36), (505, 28),
                                (560, 44), (622, 42), (688, 18), (728, 24), (772, 40), (812, 48), (852, 56), (888, 58), (928, 50),
                                (965, 44), (1005, 36), (1040, 22))):
        if math.sin(t * 3.1 + j * 1.7) > -0.2:
            gx, gy = v.opt(x, y); fx.glow(big, gx, gy, 46 * v.Z, NY.BULBS[j % 5], 0.35)
    FXL = Chars()
    B.snow_in(FXL, v, t, (230, 60, 560, 300), n=26, drift=(-40, 120))
    FXL.comp(big)
    B.steam(big, v, t, 190, 420, -99, n=4, rise=110, size=30, a=0.2)          # olivier is still... warm-ish


def party_bowl(CH, v):
    L = Layer(v.wcam())
    F.ell(L, (598, 340), 16, 6, (236, 236, 240), 0, (255, 255, 255), (190, 196, 206))
    F.ell(L, (598, 337), 13, 3, (250, 248, 236))
    F.outline(L); CH.add(L)


def r_party(t, s, u, cx=640, cy=360, Z=0.55, back=None, front=None, cat=True, cat_extra=None, cat_kw=None):
    def b(CH, v):
        if cat:
            party_bowl(CH, v)
            cat_sill(CH, v, t, extra=cat_extra, **(cat_kw or {}))
        if back: back(CH, v)
    return scene(PARTY, cx, cy, Z, light_party, front, pre=None, post=lambda big, v: party_fx(big, v, t), mask=PMASK, back=b)


def r_table_pan(t, s, u):
    k = sm(u / (s['t1'] - s['t0']))
    return r_party(t, s, u, lerp(260, 1000, k), lerp(470, 430, k), 1.35)


def r_v_table(t, s, u):
    return r_party(t, s, u, 520, 360, 0.95 + 0.03 * u,
                   back=lambda CH, v: valera_party(CH, v, t, s.get('key'), pose=dict(F.VPOSE['sit'], n=(7.5, 16.5), bn=1)))


def r_v_bottle(t, s, u):
    x, y, un = VP
    fx_, fy_ = K.face_w(x, y, un, h=20.6)
    def draw(CH, vh):
        F.valera(CH, vh.cam(x, y, un), F.VPOSE['sit'], t, mouth('valera', t), 'sad', 'home', hat='ushanka', hand_n=F.H(4.6, 21.6),
                 prop_n=lambda L, h: bottle(L, (h[0] + 0.6, h[1])), look=0.6)
    return cu(PARTY, (fx_, fy_), (300, 176), 1.5 + 0.04 * u, light_party, draw, Zb=1.25, blur=5,
              pre=lambda b, vb: party_fx(b, vb, t), bg_center=(fx_ + 40, fy_ + 30))


def r_cat_sill(t, s, u, Zh=4.2, lid=0.55, extra=None, expr=None):
    x, y, un = CAT_SILL
    hx, hy = x + 4.4 * un, y - 6.9 * un
    key = s.get('key', '')
    e = expr or ('smug' if key in ('c08', 'c10') else 'deadpan')
    return cu(PARTY, (hx, hy), (330, 180), Zh + 0.05 * u, light_party,
              lambda CH, vh: (party_bowl(CH, vh), cat_sill(CH, vh, t, lid=lid, expr=e, extra=extra)), Zb=1.35, blur=5,
              pre=lambda b, vb: party_fx(b, vb, t), bg_center=(hx + 20, hy))


def r_v_phone(t, s, u, cu_=False):
    x, y, un = VP
    def draw(CH, v):
        F.valera(CH, v.cam(x, y, un), dict(F.VPOSE['sit'], bn=-1), t, mouth('valera', t), vex(t, s.get('key'), 'proud'), 'home',
                 hat='ushanka', hand_n=F.H(0.2, 18.3), prop_n=lambda L, h: F.handset(L, h, -2.05, (196, 40, 40)))
    if cu_:
        fx_, fy_ = K.face_w(x, y, un, h=20.6)
        return cu(PARTY, (fx_, fy_), (290, 176), 1.6 + 0.04 * u, light_party, draw, pre=lambda b, vb: party_fx(b, vb, t),
                  bg_center=(fx_ + 40, fy_ + 30))
    return r_party(t, s, u, 470, 380, 1.1 + 0.03 * u, back=draw)


# ---------------------------------------------------------------- garage / Semenych's room
def kolyan_g(CH, v, t, expr='normal', phone=True, legs_only=False):
    x, y, un = KG
    if phone:
        hand = F.H(-0.5, 22.8)
        res = M.kolyan(CH, v.cam(x, y, un, flip=True), dict(M.STAND, bn=-1), t, mouth('kolyan', t, 2.2), expr, hand_n=hand,
                       prop_n=lambda L, h: F.handset(L, h, -2.0, (60, 60, 64)))
        L = Layer(v.wcam())                                                    # the curly cord to the wall phone
        hw = (x + 0.5 * un, y - 22.8 * un)
        pts = [hw] + [(lerp(hw[0], PHONE_G[0], k / 20) + 5 * math.sin(k * 2.4), lerp(hw[1], PHONE_G[1], k / 20) + 60 * math.sin(math.pi * k / 20)) for k in range(1, 21)]
        for a, b in zip(pts, pts[1:]): F.cap(L, a, b, 1.5, 1.5, (50, 50, 54))
        CH.add(L)


def garage_fx(big, v, t):
    bx, by = v.opt(650, 110); fx.glow(big, bx, by, 500 * v.Z, (255, 214, 140), 0.18 + 0.03 * math.sin(t * 9))
    FXL = Chars(); B.snow_in(FXL, v, t, (1160, 60, 1240, 560), n=26, drift=(-30, 30)); FXL.comp(big)


def sneakers_under(CH, v, t):
    L = Layer(v.wcam())
    for k, x in enumerate((262, 302)):
        F.ell(L, (x, 566 + 3 * math.sin(t * 9 + k)), 20, 11, (236, 238, 244), 0, (255, 255, 255), (170, 176, 190))
        for j in range(3): F.cap(L, (x - 10 + j * 6, 560), (x - 6 + j * 6, 572), 1.2, 1.2, (40, 52, 96))
    F.outline(L); CH.add(L)


def r_garage_ring(t, s, u):
    def post(big, v):
        garage_fx(big, v, t)
        px, py = v.opt(*PHONE_G)
        for r_ in range(3):
            rr = int(((u * 2.4 + r_ / 3) % 1) * 160)
            im = Image.fromarray(big); ImageDraw.Draw(im).ellipse([px - rr, py - rr, px + rr, py + rr], outline=(255, 236, 150), width=5)
            big[:] = np.array(im)
        if (t * 14) % 2 < 1: B.shake(big, t, 2, 60)
    return scene(GARAGE, 560, 380, 0.62, light_garage, lambda CH, v: sneakers_under(CH, v, t), post=post)


def r_kolyan_phone(t, s, u):
    return scene(GARAGE, 600, 255, 1.05 + 0.03 * u, light_garage, lambda CH, v: kolyan_g(CH, v, t, 'normal'),
                 post=lambda b, v: garage_fx(b, v, t))


def r_kolyan_cu(t, s, u):
    x, y, un = KG
    hx, hy = x - 1.6 * un, y - 23.4 * un
    return cu(GARAGE, (hx, hy), (330, 175), 1.35 + 0.05 * u, light_garage,
              lambda CH, vh: kolyan_g(CH, vh, t, 'happy'), Zb=1.25, blur=5, pre=lambda b, vb: garage_fx(b, vb, t), bg_center=(hx - 60, hy + 30))


def semenych_s(CH, v, t, expr='normal'):
    x, y, un = SR
    M.semenych(CH, v.cam(x, y, un, flip=True), dict(M.STAND, bn=-1), t, mouth('semenych', t, 2.0), expr,
               hand_n=F.H(-0.4, 19.8), prop_n=lambda L, h: F.handset(L, h, -2.0, (40, 40, 44)), hand_f=F.H(-2.0, 12.0),
               prop_f=lambda L, h: M.book(L, h))
    L = Layer(v.wcam())
    hw = (x + 0.4 * un, y - 19.8 * un)
    pts = [hw] + [(lerp(hw[0], PHONE_S[0], k / 16), lerp(hw[1], PHONE_S[1], k / 16) + 30 * math.sin(math.pi * k / 16)) for k in range(1, 17)]
    for a, b in zip(pts, pts[1:]): F.cap(L, a, b, 1.3, 1.3, (40, 40, 44))
    CH.add(L)


def bust_hat(CH, v):
    L = Layer(v.wcam())
    F.ell(L, (55, 222), 34, 16, (98, 92, 88), 0, (130, 124, 118), (70, 66, 64))
    F.cap(L, (22, 230), (88, 230), 8, 8, (130, 124, 118))
    F.outline(L); CH.add(L)


def sroom_fx(big, v, t):
    lx, ly = v.opt(810, 290); fx.glow(big, lx, ly, 380 * v.Z, (200, 255, 170), 0.2)
    sx, sy = v.opt(1075, 140); fx.glow(big, sx, sy, 200 * v.Z, (230, 240, 255), 0.25)
    FXL = Chars(); B.snow_in(FXL, v, t, (920, 60, 1110, 330), n=30, drift=(-30, 40)); FXL.comp(big)


def r_sroom_ring(t, s, u):
    def post(big, v):
        sroom_fx(big, v, t)
        px, py = v.opt(*PHONE_S)
        for r_ in range(3):
            rr = int(((u * 2.4 + r_ / 3) % 1) * 160)
            im = Image.fromarray(big); ImageDraw.Draw(im).ellipse([px - rr, py - rr, px + rr, py + rr], outline=(255, 236, 150), width=5)
            big[:] = np.array(im)
    return scene(SROOM, 640, 380, 0.6 + 0.03 * u, light_sroom, lambda CH, v: bust_hat(CH, v), post=post)


def r_semenych_phone(t, s, u):
    return scene(SROOM, 700, 400, 1.0 + 0.03 * u, light_sroom, lambda CH, v: (bust_hat(CH, v), semenych_s(CH, v, t, 'smug')),
                 post=lambda b, v: sroom_fx(b, v, t))


def r_semenych_cu(t, s, u):
    x, y, un = SR
    hx, hy = x - 1.2 * un, y - 20.6 * un
    return cu(SROOM, (hx, hy), (330, 175), 1.4 + 0.05 * u, light_sroom, lambda CH, vh: semenych_s(CH, vh, t, 'sad'), Zb=1.25, blur=5,
              pre=lambda b, vb: sroom_fx(b, vb, t), bg_center=(hx - 80, hy + 20))


def r_split3(t, s, u):
    """three-way split: Valera (kitchen) | Kolyan (garage) | Semenych (room)"""
    a = r_v_phone(t, s, u, cu_=True)
    b = r_kolyan_cu(t, s, u)
    c = r_semenych_cu(t, s, u)
    out = np.zeros_like(a)
    w = OUT_W // 3
    out[:, :w] = a[:, 380:380 + w]
    out[:, w:2 * w] = b[:, 420:420 + w]
    out[:, 2 * w:] = c[:, 420:420 + OUT_W - 2 * w]
    out[:, w - 4:w + 4] = (250, 240, 220); out[:, 2 * w - 4:2 * w + 4] = (250, 240, 220)
    return out


# ---------------------------------------------------------------- briefing map (top-down table)
_MAP = {}


def map_world(k1, k2):
    key = (round(k1, 2), round(k2, 2))
    if key in _MAP: return _MAP[key]
    if len(_MAP) > 40: _MAP.clear()
    im = Image.fromarray(TABLE.copy()); d = ImageDraw.Draw(im)
    # props: matchbox = entrance, loaf = bench, two tangerines with glasses = grannies
    d.rectangle([560, 230, 680, 300], fill=(200, 160, 60), outline=(60, 40, 20), width=3)
    d.rectangle([575, 245, 665, 285], fill=(230, 60, 40))
    d.rounded_rectangle([480, 360, 760, 420], 24, fill=(200, 140, 70), outline=(110, 70, 30), width=3)
    for i in range(6): d.line([(520 + i * 40, 368), (540 + i * 40, 410)], fill=(160, 100, 50), width=4)
    for cx in (560, 680):
        d.ellipse([cx - 34, 300, cx + 34, 368], fill=(250, 140, 30), outline=(150, 70, 10), width=3)
        for ex in (-12, 12): d.ellipse([cx + ex - 9, 322, cx + ex + 9, 340], outline=(30, 30, 30), width=3)
        d.line([(cx - 3, 331), (cx + 3, 331)], fill=(30, 30, 30), width=3)
    # forks = the fighters, moving along the ketchup route
    route = [(1020, 640), (980, 520), (860, 470), (760, 330), (640, 300)]
    def along(k):
        n = len(route) - 1; i = min(n - 1, int(k * n)); f = k * n - i
        return (route[i][0] + (route[i + 1][0] - route[i][0]) * f, route[i][1] + (route[i + 1][1] - route[i][1]) * f)
    pts = [along(j / 40 * k1) for j in range(41)] if k1 > 0 else []
    for a_, b_ in zip(pts, pts[1:]): d.line([a_, b_], fill=(200, 24, 24), width=14)
    if k1 > 0.95:
        for (x, y) in ((560, 230), (700, 230)):
            d.line([(x, y), (x + 40, y - 40)], fill=(200, 24, 24), width=10); d.line([(x + 40, y), (x, y - 40)], fill=(200, 24, 24), width=10)
    a = np.array(im)
    lab = [('ПОДЪЕЗД', (620, 196), 180), ('КПП', (620, 452), 90)]
    for txt, (cx, cy), w in lab:
        p = R.plate(w, 34, [txt], bg=(250, 250, 240), fg=(250, 250, 236), border=None, pad=1, transparent=True)
        sp = Image.fromarray(p).resize((p.shape[1] // 4, p.shape[0] // 4), Image.LANCZOS)
        im2 = Image.fromarray(a); im2.paste(sp, (int(cx - sp.width / 2), int(cy - sp.height / 2)), sp); a = np.array(im2)
    fk = along(min(1.0, k2)) if k2 > 0 else route[0]
    im2 = Image.fromarray(a); d2 = ImageDraw.Draw(im2)
    for dx in (-26, 26):
        x, y = fk[0] + dx, fk[1]
        d2.line([(x, y), (x, y + 90)], fill=(200, 204, 212), width=8)
        for j in range(4): d2.line([(x - 12 + j * 8, y - 40), (x - 12 + j * 8, y)], fill=(200, 204, 212), width=4)
    _MAP[key] = np.array(im2)
    return _MAP[key]


def r_map(t, s, u):
    first = s is TL.first('map')
    dur = s['t1'] - s['t0']
    k1 = sm(u / dur) if first else 1.0
    k2 = 0.0 if first else sm(u / dur)
    a = map_world(k1, k2)
    v = view_at(a, 760, 400, 0.85 + 0.03 * u, SX, SY)
    big = v.bg()
    if first:                                                                       # ketchup bottle in Valera's fist (from below)
        route = [(1020, 640), (980, 520), (860, 470), (760, 330), (640, 300)]
        n = len(route) - 1; kk = min(0.999, k1); i = int(kk * n); f = kk * n - i
        p = (route[i][0] + (route[i + 1][0] - route[i][0]) * f, route[i][1] + (route[i + 1][1] - route[i][1]) * f)
        x, y = v.opt(*p)
        im = Image.fromarray(big); d = ImageDraw.Draw(im)
        for j in range(12):
            k0, k1_ = j / 12, (j + 1) / 12
            d.line([(x + 60 + 900 * k0, y + 200 + 500 * k0), (x + 60 + 900 * k1_, y + 200 + 500 * k1_)],
                   fill=(240, 244, 250) if j % 2 else (40, 60, 130), width=170)
        d.ellipse([x + 10, y + 120, x + 170, y + 270], fill=(232, 176, 140), outline=(60, 30, 20), width=5)
        d.rounded_rectangle([x - 34, y - 10, x + 40, y + 200], 22, fill=(200, 30, 30), outline=(90, 10, 10), width=5)
        d.polygon([(x - 10, y - 10), (x + 16, y - 10), (x + 3, y - 46)], fill=(240, 240, 240))
        big[:] = np.array(im)
    fx.vignette(big, 0.35)
    return big


def r_fortochka(t, s, u):
    v = view_at(PARTY, 300, 180, 1.45 + 0.05 * u, SX, SY)
    big = v.bg()
    CH, _ = begin(); party_bowl(CH, v); CH.comp(big, light_party(v))
    L = Layer(v.wcam())                                                       # the thread: from the bowl up and out of the fortochka
    pts = [(560, 332), (470, 250), (330, 150), (300, 100)]
    for a_, b_ in zip(pts, pts[1:]): F.cap(L, a_, b_, 0.8, 0.8, (240, 240, 236))
    FXL = Chars(); FXL.add(L); B.snow_in(FXL, v, t, (230, 60, 560, 300), n=40, drift=(-40, 120)); FXL.comp(big)
    lab = img('bowl', lambda: R.plate(70, 26, ['СМЕТАНА', 'ОТ З. И Л.'], bg=PAPER, colors=[INK, RED], border=(120, 100, 70), pad=1.5))
    D.blit(big, v, lab, 565, 345)
    fx.vignette(big, 0.35)
    return big


# ---------------------------------------------------------------- yard meeting
def r_meet(t, s, u, cu_=None):
    """Kolyan's garage: Semenych arrives through the snowy gate, they set off"""
    def draw(CH, v):
        M.kolyan(CH, v.cam(640, 640, 15.0), M.STAND, t, mouth('kolyan', t, 2.2), 'normal', look=0.6,
                 prop_n=lambda L, h: F.string_bag(L, h))
        M.semenych(CH, v.cam(860, 640, 14.5, flip=True), dict(F.VPOSE['proud'], n=(4.4, 18.0)), t, mouth('semenych', t, 2.0), 'smug',
                   prop_f=lambda L, h: M.book(L, h))
    if cu_ == 's':
        return cu(GARAGE, (860 - 1.2 * 14.5, 640 - 20.6 * 14.5), (360, 175), 1.4 + 0.04 * u, light_garage, draw, blur=5,
                  pre=lambda b, vb: garage_fx(b, vb, t), bg_center=(800, 420))
    if cu_ == 'k':
        return cu(GARAGE, (640 + 1.6 * 15, 640 - 23.4 * 15), (300, 175), 1.35 + 0.04 * u, light_garage, draw, blur=5,
                  pre=lambda b, vb: garage_fx(b, vb, t), bg_center=(700, 420))
    return scene(GARAGE, 760, 380, 0.95 + 0.03 * u, light_garage, draw, post=lambda b, v: garage_fx(b, v, t))


# ---------------------------------------------------------------- shop
def shop_scene(t, cx, cy, Z, who=('tamara', 'kolyan', 'semenych'), texpr='bored', tkw=None, kexpr='normal', sexpr='smug', skw=None,
               kkw=None, post=None):
    def back(CH, v):
        if 'tamara' in who:
            F.tamara(CH, v.cam(TX, TY, TU, flip=True), t, mouth('tamara', t), texpr, **(tkw or {}))
    def front(CH, v):
        if 'kolyan' in who: M.kolyan(CH, v.cam(*SK), M.STAND, t, mouth('kolyan', t, 2.2), kexpr, look=0.8, **(kkw or {}))
        if 'semenych' in who: M.semenych(CH, v.cam(*SS), M.STAND, t, mouth('semenych', t, 2.0), sexpr, look=0.8, **(skw or {}))
    v = view_at(SHOP, cx, cy, Z, SX, SY)
    big = v.bg()
    CH, _ = begin(); back(CH, v); CH.comp(big, light_shop(v))
    K.occlude(big, v, CNT, CNTXY)
    PK.lcd_digits(big, v, '90')
    CH, _ = begin(); front(CH, v); CH.comp(big, light_shop(v))
    if post: post(big, v)
    fx.vignette(big, 0.3)
    return big


def t_face(): return TX - 2.0 * TU, TY - 20.5 * TU


def r_tamara_cu(t, s, u, expr=None, tkw=None, Zh=1.25):
    hx, hy = t_face()
    key = s.get('key', '')
    e = expr or {'t03': 'smug', 't04': 'bored', 't01': 'bored'}.get(key, 'bored')
    return cu(SHOP, (hx, hy), (300, 170), Zh + 0.04 * u, light_shop,
              lambda CH, vh: F.tamara(CH, vh.cam(TX, TY, TU, flip=True), t, mouth('tamara', t), e, **(tkw or {})), Zb=1.25, blur=5,
              bg_center=(hx - 60, hy + 30))


def jar_prop(L, h): M.jar(L, (h[0] - 0.4, h[1] + 0.6), 1.3)


def r_tamara_under(t, s, u):
    dur = s['t1'] - s['t0']
    k = sm(u / (dur * 0.45)) * (1 - sm((u - dur * 0.55) / (dur * 0.4)))     # ducks under the counter and comes back
    def back(CH, v):
        F.tamara(CH, v.cam(TX, TY + 140 * k, TU, flip=True), t, 0.0, 'bored', hand_n=F.H(4.8, 12.6) if u > dur * 0.6 else None,
                 prop_n=jar_prop if u > dur * 0.6 else None)
    v = view_at(SHOP, 1110, 400, 1.15, SX, SY)
    big = v.bg()
    CH, _ = begin(); back(CH, v); CH.comp(big, light_shop(v))
    K.occlude(big, v, CNT, CNTXY)
    PK.lcd_digits(big, v, '90')
    fx.vignette(big, 0.3)
    return big


def r_tamara_jar(t, s, u):
    hx, hy = t_face()
    def draw(CH, vh):
        F.tamara(CH, vh.cam(TX, TY, TU, flip=True), t, mouth('tamara', t), 'smug', hand_n=F.H(4.8, 12.6), prop_n=jar_prop)
    def post(big, vb, vh):
        jx, jy = vh.opt(TX - 4.4 * TU, TY - 11.5 * TU)
        fx.glow(big, jx, jy, 420, (255, 120, 140), 0.3 + 0.1 * math.sin(t * 6))
    return cu(SHOP, (hx, hy), (300, 170), 1.2 + 0.03 * u, light_shop, draw, Zb=1.25, blur=5, post=post, bg_center=(hx - 60, hy + 30))


def r_shop_two(t, s, u):
    return shop_scene(t, 940, 380, 0.92 + 0.03 * u, sexpr='smug')


def r_kolyan_shop(t, s, u):
    x, y, un = SK
    hx, hy = x + 1.6 * un, y - 23.4 * un
    return cu(SHOP, (hx, hy), (330, 175), 1.15 + 0.04 * u, light_shop,
              lambda CH, vh: M.kolyan(CH, vh.cam(x, y, un), F.VPOSE['shrug'], t, mouth('kolyan', t, 2.2), 'sad', look=0.8),
              Zb=1.2, blur=5, bg_center=(hx + 80, hy + 20))


def r_semenych_sniff(t, s, u):
    x, y, un = SS
    hx, hy = x + 1.2 * un, y - 20.6 * un
    return cu(SHOP, (hx, hy), (300, 175), 1.25 + 0.04 * u, light_shop,
              lambda CH, vh: M.semenych(CH, vh.cam(x, y, un), M.STAND, t, mouth('semenych', t, 2.0), 'squint', look=0.8,
                                        lean=0.6 + 0.2 * math.sin(t * 5)), Zb=1.2, blur=5, bg_center=(hx + 80, hy + 20))


def r_tamara_phone(t, s, u):
    return r_tamara_cu(t, s, u, expr='bored', tkw=dict(hand_n=F.H(1.0, 21.0), prop_n=lambda L, h: F.handset(L, h, -2.0, (40, 40, 44))))


def r_mates_glance(t, s, u):
    return shop_scene(t, 700, 330, 1.2, who=('kolyan', 'semenych'), kexpr='shock', sexpr='shock')


# ---------------------------------------------------------------- yard: attempts
def mounds(CH, v, t, x, crawl=True, s_=1.0, y=600.0, unit=PK.Y_UNIT * 1.2):
    L = Layer(v.wcam())
    for k, dx in enumerate((0, 70)):
        xx = x + dx + (6 * math.sin(t * 5 + k) if crawl else 0)
        cam = v.cam(xx, y + 12 * k, unit * s_)
        Lk = Layer(cam); M.sheet_mound(Lk, (1000.0, 1000.0), 1.0, t + k, sneakers=True); F.outline(Lk); CH.add(Lk)


def r_yard_mounds(t, s, u, back=False):
    dur = s['t1'] - s['t0']
    x = lerp(980, 820, u / dur) if not back else lerp(760, 1000, sm(u / dur))
    def draw(CH, v):
        x0, x1, sy = PK.Y_BENCH
        F.babushka(CH, v.cam(x0 + 35, sy, PK.Y_UNIT), t, 'zina', 'sit', 0.0, 'smug')
        F.babushka(CH, v.cam(x0 + 70, sy, PK.Y_UNIT), t, 'lyuba', 'sit', 0.0, 'normal')
        mounds(CH, v, t, x, unit=PK.Y_UNIT * 1.3)
    def post(big, v):
        snow(big, v, t, 80, 40); valera_window_tiny(big, v, t, glint=False)
    return scene(YARD, 700, 450, 1.05, light_yard, draw, post=post)


def r_v_radio(t, s, u):
    x, y, un = VW_
    fx_, fy_ = K.face_w(x, y, un, h=20.6)
    def draw(CH, vh):
        F.valera(CH, vh.cam(x, y, un), dict(F.VPOSE['phone'], bn=-1), t, mouth('valera', t), 'whisper', 'home', hat='ushanka',
                 hand_n=F.H(6.2, 16.6), prop_n=lambda L, h: walkie(L, h))
    return cu(PARTY, (fx_, fy_), (300, 176), 1.55 + 0.04 * u, light_party, draw, Zb=1.3, blur=4,
              pre=lambda b, vb: party_fx(b, vb, t), bg_center=(fx_ - 20, fy_ + 10))


def r_bench(t, s, u, cx=800, cy=470, Z=1.2, zk=None, lk=None, visitors=None, journal=False):
    def draw(CH, v):
        grannies(CH, v, t, zk, lk)
        if visitors: visitors(CH, v)
    return scene(BENCH, cx, cy, Z + 0.03 * u, light_bench, draw, post=lambda b, v: snow(b, v, t))


def granny_cu(t, s, u, who='zina', **kw):
    if who == 'zina': hx, hy = ZX - 1.0 * ZU, ZY - 11.8 * ZU
    else: hx, hy = LX - 0.9 * LU, LY - 11.8 * LU
    kk = dict(expr='smug' if who == 'zina' else 'normal'); kk.update(kw)
    def draw(CH, vh):
        if who == 'zina': F.babushka(CH, vh.cam(ZX, ZY, ZU, flip=True), t, 'zina', 'sit', mouth('zina', t), **kk)
        else: F.babushka(CH, vh.cam(LX, LY, LU, flip=True), t, 'lyuba', 'sit', mouth('lyuba', t), **kk)
    return cu(BENCH, (hx, hy), (360, 196), 1.9 + 0.05 * u, light_bench, draw, Zb=1.3, blur=5, post=lambda b, vb, vh: snow(b, vb, t),
              bg_center=(hx - 40, hy + 20))


def r_mounds_cu(t, s, u):
    def draw(CH, v):
        mounds(CH, v, t, 560, unit=BU * 1.25, y=BF - 6)
    return r_bench(t, s, u, 770, 560, 1.1, visitors=draw)


def stamp_fail(big, t, s, u, n):
    gray = big.mean(2, keepdims=True)
    big[:] = (big * 0.35 + gray * 0.65).astype(np.uint8)
    st = img(('fail', n), lambda: stamp_img(f'ПОПЫТКА №{n}', 'ПРОВАЛ'))
    k = min(1.0, u / 0.12)
    sc = lerp(1.6, 1.0, k)
    im = st if sc == 1.0 else np.array(Image.fromarray(st).resize((int(st.shape[1] * sc), int(st.shape[0] * sc)), Image.NEAREST))
    O.overlay(big, im, (OUT_W - im.shape[1]) // 2, 230 - (im.shape[0] - st.shape[0]) // 2, 1.0)
    if u < 0.1: O.flash(big, 0.7 * (1 - u / 0.1))


def stamp_img(l1, l2):
    W_, H_ = 900, 300
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([10, 10, W_ - 10, H_ - 10], 30, outline=(214, 30, 36, 255), width=16)
    f1 = R._font(48); f2 = R._font(104)
    d.text(((W_ - f1.getlength(l1)) / 2, 40), l1, font=f1, fill=(214, 30, 36, 255))
    d.text(((W_ - f2.getlength(l2)) / 2, 120), l2, font=f2, fill=(214, 30, 36, 255))
    return np.array(im.rotate(-6, resample=Image.NEAREST, expand=True))


_FREEZE = {}


def r_fail(t, s, u, n):
    src = TL.first('mounds_back') if n == 1 else TL.first('dm_poem')
    if n not in _FREEZE:
        _FREEZE[n] = render_scene(src['t1'] - 0.05).copy()
    big = _FREEZE[n].copy()
    stamp_fail(big, t, s, u, n)
    return big


# Ded Moroz + Snegurochka in front of the bench (bench world)
DMX, KSX = 470.0, 330.0


def visitors_dm(CH, v, t, walk=None):
    kx = KSX if walk is None else lerp(-80, KSX, walk)
    sx = DMX if walk is None else lerp(40, DMX, walk)
    wk = walk is not None and walk < 1
    M.kolyan(CH, v.cam(kx, BF, BU), F.vwalk(t, 9, 0.5) if wk else M.STAND, t, mouth('kolyan', t, 2.2), 'sad',
             costume='snegurochka', look=0.6)
    M.semenych(CH, v.cam(sx, BF, BU * 0.95), F.vwalk(t, 9, 0.5) if wk else dict(F.VPOSE['shout'], n=(6.0, 23.0)), t,
               mouth('semenych', t, 2.0), 'smug' if not wk else 'normal', costume='ded_moroz', look=0.6,
               prop_f=lambda L, h: sack(L, h, t))


def sack(L, h, t):
    x, y = h
    F.ell(L, (x - 1.0, y + 2.6), 2.6, 3.0, (150, 30, 40), 0.2, (190, 60, 70), (110, 20, 28))
    F.cap(L, (x - 1.4, y + 0.2), (x + 0.2, y - 0.2), 0.3, 0.3, (236, 200, 90))


def r_dress(t, s, u):
    """garage mirror: Kolyan puts on the kokoshnik; Semenych holds the braids"""
    dur = s['t1'] - s['t0']
    k = sm(u / (dur * 0.6))
    def draw(CH, v):
        M.semenych(CH, v.cam(780, 640, 14.5, flip=True), F.VPOSE['proud'], t, mouth('semenych', t, 2.0), 'blissful', costume='ded_moroz')
        M.kolyan(CH, v.cam(620, 640, 15.0), dict(F.VPOSE['overhead'], bn=1) if k < 0.9 else M.STAND, t, mouth('kolyan', t, 2.2),
                 'sad', costume='snegurochka' if k > 0.5 else None)
    def post(big, v):
        garage_fx(big, v, t)
        if 0.48 < k < 0.56: O.flash(big, 0.5)
    return scene(GARAGE, 700, 380, 1.0 + 0.04 * u, light_garage, draw, post=post)


def r_dress_mirror(t, s, u):
    x, y, un = 620.0, 640.0, 15.0
    hx, hy = x + 1.6 * un, y - 23.4 * un
    return cu(GARAGE, (hx, hy), (330, 190), 1.4 + 0.04 * u, light_garage,
              lambda CH, vh: M.kolyan(CH, vh.cam(x, y, un), M.STAND, t, mouth('kolyan', t, 2.2), 'sad', costume='snegurochka'),
              Zb=1.25, blur=5, pre=lambda b, vb: garage_fx(b, vb, t), bg_center=(hx + 40, hy + 20))


def r_dm_walk(t, s, u):
    dur = s['t1'] - s['t0']
    return r_bench(t, s, u, 640, 470, 0.95, visitors=lambda CH, v: visitors_dm(CH, v, t, walk=min(1.0, u / dur * 1.15)),
                   zk=dict(expr='normal', look=-1.0), lk=dict(knit=False, look=-1.0))


def r_dm_hello(t, s, u):
    return r_bench(t, s, u, 560, 470, 1.05, visitors=lambda CH, v: visitors_dm(CH, v, t), zk=dict(look=-1.0), lk=dict(look=-1.0))


def r_sneg_cu(t, s, u):
    hx, hy = KSX + 1.6 * BU, BF - 23.4 * BU
    return cu(BENCH, (hx, hy), (330, 180), 1.3 + 0.05 * u, light_bench,
              lambda CH, vh: M.kolyan(CH, vh.cam(KSX, BF, BU), M.STAND, t, max(0.3, mouth('kolyan', t, 2.2)), 'sad',
                                      costume='snegurochka', look=0.6), Zb=1.25, blur=5,
              post=lambda b, vb, vh: snow(b, vb, t), bg_center=(hx + 60, hy + 40))


def r_dm_poem(t, s, u):
    hx, hy = DMX + 1.2 * BU * 0.95, BF - 20.6 * BU * 0.95
    return cu(BENCH, (hx, hy), (300, 180), 1.3 + 0.05 * u, light_bench,
              lambda CH, vh: M.semenych(CH, vh.cam(DMX, BF, BU * 0.95), dict(F.VPOSE['shout'], n=(6.0, 23.0)), t,
                                        mouth('semenych', t, 2.0), 'blissful', costume='ded_moroz', look=0.6), Zb=1.25, blur=5,
              post=lambda b, vb, vh: snow(b, vb, t), bg_center=(hx + 60, hy + 40))


# ---------------------------------------------------------------- the twist
VX_B = 520.0


def valera_b(CH, v, t, key=None, flag=True, x=VX_B, walk=False, expr=None):
    pose = F.vwalk(t, 8, 0.5) if walk else F.VPOSE['stand']
    F.valera(CH, v.cam(x, BF, BU), pose, t, mouth('valera', t), expr or vex(t, key, 'sad'), 'street', look=0.8,
             hand_n=F.H(4.4, 13.0) if flag else None, prop_n=(lambda L, h: towel_flag(L, h, t)) if flag else None,
             hand_f=F.H(3.6, 11.0), prop_f=lambda L, h: B.basin(L, (h[0] + 0.4, h[1] - 1.0), fill=(236, 220, 160), scale=0.8))


def r_v_flag(t, s, u):
    dur = s['t1'] - s['t0']
    x = lerp(380, VX_B, sm(u / dur))
    return r_bench(t, s, u, 640, 470, 0.95, visitors=lambda CH, v: valera_b(CH, v, t, flag=True, x=x, walk=u < dur), zk=dict(look=-1.0))


def r_v_flag_cu(t, s, u, expr=None):
    hx, hy = VX_B + 1.4 * BU, BF - 21.0 * BU
    return cu(BENCH, (hx, hy), (300, 176), 1.3 + 0.05 * u, light_bench,
              lambda CH, vh: valera_b(CH, vh, t, s.get('key'), expr=expr), Zb=1.25, blur=5,
              post=lambda b, vb, vh: snow(b, vb, t), bg_center=(hx + 60, hy + 40))


def r_journal(t, s, u):
    v = view_at(BENCH, ZX, ZY - 60, 1.4, SX, SY)
    big = blurred(BENCH, v, 6)
    k = sm(u / 0.5)
    im = img('journal', journal_img)
    w = int(lerp(300, im.shape[1], k)); h = int(im.shape[0] * w / im.shape[1])
    p = np.array(Image.fromarray(im).resize((w, h), Image.LANCZOS))
    O.overlay(big, p, (OUT_W - p.shape[1]) // 2, max(20, (OUT_H - p.shape[0]) // 2 - 60), 1.0)
    fx.vignette(big, 0.4)
    return big


def journal_img():
    W_, H_ = 1300, 760
    im = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, W_ - 1, H_ - 1], 24, fill=(60, 90, 60, 255))
    d.rectangle([30, 30, W_ // 2 - 6, H_ - 30], fill=(246, 240, 222, 255)); d.rectangle([W_ // 2 + 6, 30, W_ - 30, H_ - 30], fill=(246, 240, 222, 255))
    for y in range(110, H_ - 40, 48):
        d.line([(50, y), (W_ // 2 - 26, y)], fill=(170, 190, 220, 255), width=2); d.line([(W_ // 2 + 26, y), (W_ - 50, y)], fill=(170, 190, 220, 255), width=2)
    hd = R._font(40); f = R._font(24)
    d.text((60, 46), 'ЖУРНАЛ', font=hd, fill=(176, 30, 34, 255)); d.text((60, 92 - 6), '', font=f)
    rows = [('31.12', 'ОПЕРАЦИЯ «ОЛИВЬЕ»'), ('20:00', 'ВАЛЕРА — БИНОКЛЬ'), ('21:40', 'ТАМАРА: КОМПОТ'), ('22:30', 'СУГРОБЫ (2 ШТ)'),
            ('23:10', 'КОЛЯН = СНЕГУРКА')]
    y = 122
    for tm, tx in rows:
        d.text((60, y), tm, font=f, fill=(40, 60, 150, 255)); d.text((200, y), tx, font=f, fill=(30, 30, 34, 255)); y += 96
    d.text((W_ // 2 + 40, 46), 'ПОСЕЩЕНИЙ', font=hd, fill=(176, 30, 34, 255))
    y = 122
    for tx in ('ИСТОЧНИК:', '«КОТ»', 'ОПЛАТА:', 'СМЕТАНА 20%', 'ВЫВОД: НЕ ПУСКАТЬ'):
        d.text((W_ // 2 + 40, y), tx, font=f, fill=(30, 30, 34, 255) if 'ВЫВОД' not in tx else (176, 30, 34, 255)); y += 96
    return np.array(im)


def r_zina_read(t, s, u):
    return granny_cu(t, s, u, 'zina', expr='smug', hand_n=F.H(4.0, 8.4), prop_n=lambda L, h: notebook(L, (h[0] + 0.4, h[1] - 0.6)))


def r_tilt_up(t, s, u):
    dur = s['t1'] - s['t0']
    k = sm(u / dur)
    cy = lerp(480, 230, k)
    def draw(CH, v):
        x0, x1, sy = PK.Y_BENCH
        F.babushka(CH, v.cam(x0 + 35, sy, PK.Y_UNIT), t, 'zina', 'sit', 0.0, 'smug', hand_n=F.H(3.8, 4.6),
                   prop_n=lambda L, h: notebook(L, h, False))
        F.babushka(CH, v.cam(x0 + 70, sy, PK.Y_UNIT), t, 'lyuba', 'sit', 0.0, 'normal', hand_n=F.H(3.0, 4.4), prop_n=tin_can)
        F.valera(CH, v.cam(x0 - 20, sy + 40, PK.Y_UNIT), F.VPOSE['stand'], t, 0.0, 'shock', 'street', look=1.0)
        L = Layer(v.wcam())                                                    # the string: Lyuba's can -> the kitchen fortochka
        a = (x0 + 70 + 3.0 * PK.Y_UNIT, sy - 4.4 * PK.Y_UNIT); b = (PK.Y_WINDOW[0] + 14, PK.Y_WINDOW[1] + 8)
        n = 24
        for i in range(n):
            p0 = (lerp(a[0], b[0], i / n), lerp(a[1], b[1], i / n) + 18 * math.sin(math.pi * i / n))
            p1 = (lerp(a[0], b[0], (i + 1) / n), lerp(a[1], b[1], (i + 1) / n) + 18 * math.sin(math.pi * (i + 1) / n))
            F.cap(L, p0, p1, 0.6, 0.6, (250, 250, 240))
        CH.add(L)
    def post(big, v):
        snow(big, v, t, 80, 40)
        valera_window_tiny(big, v, t, glint=False, cat=True)
    return scene(YARD, 450, cy, 2.0 - 0.3 * k, light_yard, draw, post=post)


def r_cat_agent(t, s, u):
    return r_cat_sill(t, s, u, Zh=4.4, lid=0.6, extra=can_paw)


def r_v_shock(t, s, u):
    return r_v_flag_cu(t, s, u, expr='shock')


def r_bench_terms(t, s, u):
    return r_bench(t, s, u, 700, 470, 1.15, visitors=lambda CH, v: valera_b(CH, v, t, flag=False, expr='sad'),
                   zk=dict(hand_n=F.H(4.0, 8.4), prop_n=lambda L, h: notebook(L, (h[0] + 0.4, h[1] - 0.6))))


def r_v_defeat(t, s, u):
    hx, hy = VX_B + 1.4 * BU, BF - 21.0 * BU
    def draw(CH, vh):
        F.valera(CH, vh.cam(VX_B, BF, BU), F.VPOSE['shrug'], t, mouth('valera', t), 'sad', 'street', look=0.8)
    return cu(BENCH, (hx, hy), (300, 176), 1.3 + 0.05 * u, light_bench, draw, Zb=1.25, blur=5,
              post=lambda b, vb, vh: snow(b, vb, t), bg_center=(hx + 60, hy + 40))


# ---------------------------------------------------------------- the party
def party_cast(CH, v, t, toast=False, dance=False):
    zx, zy, zu = ZP
    lx, ly, lu = LP
    lk = dict(hand_n=F.H(3.4, 10.0 + 1.5 * math.sin(t * 8)) if not dance else F.H(2.6, 16.0 + 1.5 * math.sin(t * 6)),
              prop_n=(lambda L, h: B.ladle(L, h, fill=(236, 220, 160))) if not dance else None)
    F.babushka(CH, v.cam(lx + (14 * math.sin(t * 4) if dance else 0), ly, lu), t, 'lyuba', 'sit', mouth('lyuba', t), 'normal', **lk)
    F.babushka(CH, v.cam(zx, zy, zu, flip=True), t, 'zina', 'sit', mouth('zina', t), 'smug',
               hand_n=F.H(3.4, 14.5) if toast else None, prop_n=(lambda L, h: glass(L, h)) if toast else None)
    paper_crown(CH, v, zx - 0.4 * zu, zy - 15.6 * zu, zu)


def glass(L, h):
    x, y = h
    F.poly(L, [(x - 0.55, y - 1.6), (x + 0.55, y - 1.6), (x + 0.45, y + 0.2), (x - 0.45, y + 0.2)], (210, 230, 240))
    F.poly(L, [(x - 0.5, y - 0.9), (x + 0.5, y - 0.9), (x + 0.45, y + 0.2), (x - 0.45, y + 0.2)], (190, 40, 60))


def paper_crown(CH, v, x, y, u):
    L = Layer(v.wcam())
    pts = [(x - 2.0 * u, y), (x - 1.6 * u, y - 1.6 * u), (x - 0.8 * u, y - 0.6 * u), (x, y - 1.8 * u), (x + 0.8 * u, y - 0.6 * u),
           (x + 1.6 * u, y - 1.6 * u), (x + 2.0 * u, y)]
    F.poly(L, pts, (250, 210, 60)); F.outline(L); CH.add(L)


def r_party_wide(t, s, u, toast=False, dance=False, cx=640, cy=360, Z=0.6):
    return r_party(t, s, u, cx, cy, Z + 0.03 * u, back=lambda CH, v: party_cast(CH, v, t, toast, dance),
                   cat_kw=dict(expr='smug', lid=0.7))


def r_tamara_enter(t, s, u):
    dur = s['t1'] - s['t0']
    x = lerp(600, 760, sm(u / dur))
    def draw(CH, v):
        F.tamara(CH, v.cam(x, 700, 15.0), t, mouth('tamara', t), 'bored', hand_n=F.H(4.4, 14.0), prop_n=jar_prop)
    return scene(HALL, 700, 360, 1.0 + 0.03 * u, light_hall, draw)


def r_lyuba_eat(t, s, u):
    lx, ly, lu = LP
    hx, hy = lx + 0.9 * lu, ly - 11.8 * lu
    return cu(PARTY, (hx, hy), (330, 176), 2.2 + 0.05 * u, light_party,
              lambda CH, vh: F.babushka(CH, vh.cam(lx, ly, lu), t, 'lyuba', 'sit', max(mouth('lyuba', t), 0.3 * abs(math.sin(t * 9))),
                                        'normal', hand_n=F.H(3.0, 12.4), prop_n=lambda L, h: B.ladle(L, h, fill=(236, 220, 160))),
              Zb=1.3, blur=5, pre=lambda b, vb: party_fx(b, vb, t), bg_center=(hx + 60, hy + 20))


def r_party_zina(t, s, u):
    zx, zy, zu = ZP
    hx, hy = zx - 1.0 * zu, zy - 11.8 * zu
    def draw(CH, vh):
        F.babushka(CH, vh.cam(zx, zy, zu, flip=True), t, 'zina', 'sit', mouth('zina', t), 'smug', hand_n=F.H(4.2, 12.8))
        paper_crown(CH, vh, zx - 0.4 * zu, zy - 15.6 * zu, zu)
    return cu(PARTY, (hx, hy), (330, 176), 2.2 + 0.05 * u, light_party, draw, Zb=1.3, blur=5, pre=lambda b, vb: party_fx(b, vb, t),
              bg_center=(hx - 60, hy + 20))


def shawl_back(CH, v, cx, y, uu, head_h, col):
    L = Layer(v.cam(cx, y, uu))
    F.ell(L, F.H(1.0, head_h + 0.3), 3.9, 4.3, col, 0, tuple(min(255, c + 30) for c in col), tuple(int(c * 0.72) for c in col))
    F.outline(L); CH.add(L)


def shawl_knot(CH, v, cx, y, uu, head_h, col):
    L = Layer(v.cam(cx, y, uu))
    F.ell(L, F.H(1.6, head_h - 3.6), 1.4, 0.9, tuple(int(c * 0.8) for c in col))
    F.cap(L, F.H(1.2, head_h - 3.9), F.H(0.6, head_h - 6.0), 0.5, 0.35, tuple(int(c * 0.8) for c in col))
    F.outline(L); CH.add(L)


def trio(CH, v, t, x0, y, un, shawls=False, sit=False, k_expr='sad', s_expr='sad', v_expr=None, key=None, cold=0.0):
    pose = dict(F.VPOSE['sit'], n=(4.4, 10.6)) if sit else M.STAND
    vpose = dict(F.VPOSE['sit'], n=(4.4, 10.6)) if sit else F.VPOSE['stand']
    people = ((x0, un * 0.95, 20.6, (150, 146, 150)), (x0 + 9 * un, un, 21.4, (176, 120, 130)), (x0 + 18.5 * un, un, 23.6, (140, 150, 140)))
    if shawls:
        for cx, uu, hh, col in people: shawl_back(CH, v, cx, y, uu, hh, col)
    M.semenych(CH, v.cam(x0, y, un * 0.95), pose, t, mouth('semenych', t, 2.0), s_expr, look=0.4, cold=cold)
    F.valera(CH, v.cam(x0 + 9 * un, y, un), vpose, t, mouth('valera', t), v_expr or vex(t, key, 'sad'), 'street', look=0.4, cold=cold)
    M.kolyan(CH, v.cam(x0 + 18.5 * un, y, un), pose, t, mouth('kolyan', t, 2.2), k_expr, look=-0.4, cold=cold)


def r_trio_door(t, s, u):
    return scene(HALL, 560, 360, 1.0 + 0.03 * u, light_hall, lambda CH, v: trio(CH, v, t, 420, 716, 14.0, key=s.get('key')))


def r_cat_lap(t, s, u):
    """the cat on Zina's lap at the party, eating sour cream from a bowl — the contract"""
    zx, zy, zu = ZP
    cx_, cy_ = zx - 0.5 * zu, zy - 2.0 * zu
    def draw(CH, vh):
        F.babushka(CH, vh.cam(zx, zy, zu, flip=True), t, 'zina', 'sit', mouth('zina', t), 'blissful', hand_n=F.H(2.4, 4.6))
        F.cat(CH, vh.cam(cx_, cy_, 4.4), t, 'loaf', mouth('cat', t, 2.0), 0.8, (0.6, 0.0), 'smug', tail=0.6)
    return cu(PARTY, (cx_ + 4.4 * 4.4, cy_ - 6.9 * 4.4), (330, 190), 3.2 + 0.05 * u, light_party, draw, Zb=1.3, blur=5,
              pre=lambda b, vb: party_fx(b, vb, t), bg_center=(cx_ - 40, cy_ - 20))


# ---------------------------------------------------------------- midnight
BURSTS = [(0.0, 300, 330, 120, 0), (0.4, 560, 520, 90, 2), (0.9, 900, 880, 140, 3), (1.3, 700, 720, 60, 4), (1.8, 1100, 1060, 110, 1),
          (2.3, 450, 420, 80, 0), (2.8, 820, 800, 70, 2), (3.3, 1000, 980, 130, 3)]


def bursts_at(t0):
    return [(t0 + a, b, c, d, e) for (a, b, c, d, e) in BURSTS]


def r_yard_midnight(t, s, u, end=False):
    t0 = s['t0']
    def draw(CH, v):
        x0, x1, sy = PK.Y_BENCH
        for k, (fn, dx) in enumerate(((M.semenych, 30), (None, 70), (M.kolyan, 110))):
            un = PK.Y_UNIT
            if fn is None: F.valera(CH, v.cam(x0 + dx, sy + 4, un), dict(F.VPOSE['sit'], n=(4.4, 10.6)), t, 0.0, 'sad', 'street')
            else: fn(CH, v.cam(x0 + dx, sy + 4, un), dict(F.VPOSE['sit'], n=(4.4, 10.6)), t, 0.0, 'sad')
    def post(big, v):
        FXL = Chars()
        lit = NY.fireworks(FXL, v, t, bursts_at(t0) + bursts_at(t0 + 3.6), 1.0)
        B.falling_snow(FXL, v, t, v.X0 - 20, v.Y0 - 20, v.X0 + 680 / v.Z, v.Y0 + 380 / v.Z, n=70, speed=40)
        FXL.comp(big)
        for (bx, by, c, f_) in lit:
            ox, oy = v.opt(bx, by); fx.glow(big, ox, oy, 520 * v.Z, c, 0.5 * f_)
        x0, y0, x1, y1 = PK.Y_WINDOW                                                   # the party in the window
        k = 0.5 + 0.5 * math.sin(t * 8)
        wx, wy = v.opt((x0 + x1) / 2, (y0 + y1) / 2); fx.glow(big, wx, wy, 240 * v.Z, (255, 200, 120), 0.35 + 0.15 * k)
        L = Layer(v.wcam())
        for j in range(3):
            sx_ = x0 + 16 + j * 22 + 4 * math.sin(t * 7 + j)
            F.ell(L, (sx_, y1 - 16 + 3 * abs(math.sin(t * 8 + j))), 7, 12, (60, 36, 30))
            F.ell(L, (sx_, y1 - 32 + 3 * abs(math.sin(t * 8 + j))), 5, 5, (60, 36, 30))
        FXL2 = Chars(); FXL2.add(L); FXL2.comp(big)
    if end:
        return scene(YARD, 640, 330, 0.62 + 0.03 * u, light_yard, draw, post=post)
    return scene(YARD, 520, lerp(300, 380, sm(u / 3)), lerp(0.9, 1.5, sm(u / 3)), light_yard, draw, post=post)


TB = (560.0, BF, BU)                     # the trio on the bench (Semenych at x, Valera +9u, Kolyan +18.5u)


def bench_trio(CH, v, t, key=None, k_expr='sad', s_expr='sad'):
    trio(CH, v, t, 650, BF, BU, shawls=True, sit=True, k_expr=k_expr, s_expr=s_expr, key=key, cold=0.25)


def midnight_fx(big, v, t):
    FXL = Chars()
    lit = NY.fireworks(FXL, v, t, bursts_at(TL.first('yard_midnight')['t0']) + bursts_at(TL.first('trio_bench')['t0'] + 1.0), 0.8)
    FXL.comp(big)
    for (bx, by, c, f_) in lit:
        ox, oy = v.opt(bx, by); fx.glow(big, ox, oy, 420 * v.Z, c, 0.35 * f_)
    snow(big, v, t, 70, 40)


def r_trio_bench(t, s, u):
    return scene(BENCH, 820, 450, 1.05 + 0.03 * u, light_bench, lambda CH, v: bench_trio(CH, v, t, s.get('key')),
                 post=lambda b, v: midnight_fx(b, v, t))


def trio_cu(t, s, u, who):
    off = {'s': 0.0, 'v': 9.0, 'k': 18.5}[who]
    x = 650 + off * BU
    h = {'s': 20.6 * 0.95, 'v': 21.0, 'k': 23.4}[who]
    hx, hy = x + 1.2 * BU, BF - h * BU
    key = s.get('key', '')
    kx = {'k05': 'blissful', 'k06': 'normal'}.get(key, 'sad')
    sx = {'s08': 'shock', 's09': 'squint'}.get(key, 'sad')
    return cu(BENCH, (hx, hy), (320, 170), 1.35 + 0.05 * u, light_bench,
              lambda CH, vh: bench_trio(CH, vh, t, key, k_expr=kx, s_expr=sx), Zb=1.25, blur=5,
              post=lambda b, vb, vh: midnight_fx(b, vb, t), bg_center=(hx + 30, hy + 40))


NN = (450.0, 640.0, 17.0)                # Nina (waist below the frame bottom) at the left of the bench


def r_nina(t, s, u, come=False):
    dur = s['t1'] - s['t0']
    x = lerp(250, NN[0], sm(u / dur)) if come else NN[0]
    def draw(CH, v):
        bench_trio(CH, v, t)
        F.nina(CH, v.cam(x, NN[1], NN[2], flip=False), t, mouth('nina', t), 'bored', False, cap_=True, outfit='coat', cold=0.4,
               hand_n=F.H(3.0, 1.8))
        L = Layer(v.cam(x, NN[1], NN[2])); B.basin(L, F.H(3.2, 0.9), scale=0.95, tilt=0.15); F.outline(L); CH.add(L)
    return scene(BENCH, 600, 420, 1.15 + 0.03 * u, light_bench, draw, post=lambda b, v: midnight_fx(b, v, t))


def r_v_guard(t, s, u):
    off = 9.0
    x = 650 + off * BU
    def draw(CH, vh):
        trio(CH, vh, t, 650, BF, BU, shawls=True, sit=True, key='v16', cold=0.25)
    hx, hy = x + 1.2 * BU, BF - 21.0 * BU
    big = cu(BENCH, (hx, hy), (320, 176), 1.35 + 0.05 * u, light_bench,
             lambda CH, vh: F.valera(CH, vh.cam(x, BF, BU), F.VPOSE['point'], t, mouth('valera', t), 'angry',
                                     'street', look=-0.6, cold=0.25),
             Zb=1.25, blur=5, post=lambda b, vb, vh: midnight_fx(b, vb, t), bg_center=(hx - 60, hy + 40))
    return big


def r_window_zina(t, s, u):
    v = view_at(YARD, 440, 210, 1.35, SX, SY)
    big = blurred(YARD, v, 4)
    midnight_fx(big, v, t)
    # the lit window frame + Zina leaning out
    x0, y0 = 600, 120
    big[y0:y0 + 760, x0:x0 + 720] = (40, 34, 30)
    big[y0 + 20:y0 + 740, x0 + 20:x0 + 700] = (236, 186, 110)
    fx.glow(big, x0 + 360, y0 + 380, 600, (255, 210, 140), 0.4)
    vh = hview(YARD, 1000, 1000 - 18.8 * 16, 1.0, 330, 170)
    keep = big.copy()
    CH, _ = begin()
    F.babushka(CH, vh.cam(1000, 1000, 16.0, flip=True), t, 'zina', 'stand', mouth('zina', t), 'smug', hand_n=F.H(4.6, 18.0))
    paper_crown(CH, vh, 1000 - 0.4 * 16, 1000 - 22.6 * 16, 16)
    CH.comp(big, light_party(view_at(PARTY, 640, 360, 0.6, SX, SY)))
    big[y0 + 600:] = keep[y0 + 600:]
    big[y0 + 600:y0 + 660, x0 - 40:x0 + 760] = (90, 84, 80)                          # window sill (hides the body)
    big[y0 + 600:y0 + 610, x0 - 40:x0 + 760] = (236, 240, 250)
    fx.vignette(big, 0.35)
    return big


def r_cat_final(t, s, u):
    return r_cat_sill(t, s, u, Zh=4.0, lid=0.6, expr='smug')


# ---------------------------------------------------------------- credits / summer
CREDITS = ['ВАЛЕРА И КОТ', 'ПРОПУСКНОЙ РЕЖИМ', '', 'В РОЛЯХ:', '', 'ВАЛЕРА — ПРАПОРЩИК ЗАПАСА', 'КОТ ДЕМБЕЛЬ — ДВОЙНОЙ АГЕНТ',
           'КОЛЯН — «НУ»', 'СЕМЁНЫЧ — ЛИТЕРАТУРА', 'БАБА ЗИНА — КПП', 'БАБА ЛЮБА — ОЛИВЬЕ', 'ТАМАРА — КОМПОТ 70°', 'НИНА ПЕТРОВНА — ЖЭК',
           '', 'ВО ВРЕМЯ СЪЁМОК', 'НИ ОДНА БАБУШКА', 'НЕ ЗАМЁРЗЛА.', 'ТРОЕ МУЖИКОВ —', 'ДА.']


def r_credits(t, s, u):
    v = view_at(YARD, 640, 360, 0.55, SX, SY)
    big = blurred(YARD, v, 5)
    big[:] = (big * 0.4).astype(np.uint8)
    snow(big, v, t, 90, 40)
    cr = img('credits', lambda: credits_img())
    dur = s['t1'] - s['t0']
    y = int(OUT_H - (u / dur) * (OUT_H + cr.shape[0] * 0.8))
    O.overlay(big, cr, (OUT_W - cr.shape[1]) // 2, y, 1.0)
    return big


def credits_img():
    f1, f2 = R._font(48), R._font(32)
    H_ = 0
    rows = []
    for i, l in enumerate(CREDITS):
        f = f1 if i < 2 else f2
        rows.append((l, f, (255, 214, 90) if i < 2 else (240, 240, 236))); H_ += (72 if i < 2 else 58)
    im = Image.new('RGBA', (1600, H_ + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    y = 20
    for l, f, c in rows:
        d.text(((1600 - f.getlength(l)) / 2, y), l, font=f, fill=c + (255,)); y += 72 if f is f1 else 58
    return np.array(im)


def r_summer(t, s, u):
    def draw(CH, v):
        un = 5.6
        for k, (fn, dx, hh) in enumerate(((M.semenych, 0, 20.6), (None, 26, 21.4), (M.kolyan, 52, 23.6))):
            x = 498 + dx
            shawl_back(CH, v, x, 528, un, hh, ((150, 146, 150), (176, 120, 130), (140, 150, 140))[k])
            if fn is None: r = F.valera(CH, v.cam(x, 528, un), dict(F.VPOSE['sit'], n=(4.4, 10.6)), t, 0.0, 'sad', 'street')
            else: r = fn(CH, v.cam(x, 528, un), dict(F.VPOSE['sit'], n=(4.4, 10.6)), t, 0.0, 'sad')
            pass
    def post(big, v):
        FXL = Chars()
        B.falling_snow(FXL, v, t, v.X0 - 40, v.Y0 - 20, v.X0 + 680 / v.Z, v.Y0 + 380 / v.Z, n=90, col=(255, 252, 240), speed=12)
        FXL.comp(big)
    return scene(SUMMER, 540, 440, 1.4 + 0.04 * u, light_summer, draw, post=post)


def r_s2(t, s, u):
    v = view_at(SUMMER, 640, 360, 0.55, SX, SY)
    big = blurred(SUMMER, v, 4)
    FXL = Chars(); B.falling_snow(FXL, v, t, -40, -20, 1320, 740, n=90, col=(255, 252, 240), speed=12); FXL.comp(big)
    ti = img('s2', lambda: O.winter_title(['СЕЗОН 2:', 'ЛЕТО'], 110, outline=(120, 40, 10), shadow=(60, 20, 6)))
    O.overlay(big, ti, 0, 220, min(1.0, u / 0.15))
    return big


# ======================================================================================= dispatch
_IMG = {}


def img(key, make):
    if key not in _IMG: _IMG[key] = make()
    return _IMG[key]


def badge(text, size=34):
    from PIL import ImageFont
    font = ImageFont.truetype(P.FONT_BOLD, size)
    tw = int(ImageDraw.Draw(Image.new('L', (8, 8))).textlength(text, font=font))
    im = Image.new('RGBA', (tw + 40, int(size * 1.8)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, tw + 36, int(size * 1.7)), 14, fill=(20, 12, 10, 130))
    d.text((18, int(size * 0.26)), text, font=font, fill=(255, 244, 214, 220))
    return np.array(im)


SHOT = {
    'bino': r_bino, 'bino_zina': r_bino_zina, 'window_out': r_window_out, 'title': r_title,
    'table_pan': r_table_pan, 'v_table': r_v_table, 'v_bottle': r_v_bottle, 'cat_sill': lambda t, s, u: r_cat_sill(t, s, u),
    'v_phone': r_v_phone, 'v_phone_cu': lambda t, s, u: r_v_phone(t, s, u, True),
    'garage_ring': r_garage_ring, 'kolyan_phone': r_kolyan_phone, 'kolyan_cu': r_kolyan_cu,
    'sroom_ring': r_sroom_ring, 'semenych_phone': r_semenych_phone, 'semenych_cu': r_semenych_cu, 'split3': r_split3,
    'cat_cu': lambda t, s, u: r_cat_sill(t, s, u, Zh=4.6),
    'map': r_map, 'cat_bowl': lambda t, s, u: r_cat_sill(t, s, u, Zh=4.0, lid=0.85, expr='smug'), 'fortochka': r_fortochka,
    'meet': lambda t, s, u: r_meet(t, s, u), 'meet_cu': lambda t, s, u: r_meet(t, s, u, 's'), 'meet_kolyan': lambda t, s, u: r_meet(t, s, u, 'k'),
    'shop_wide': lambda t, s, u: shop_scene(t, 760, 330, 0.6 + 0.03 * u, sexpr='normal'),
    'shop_two': r_shop_two, 'tamara_cu': r_tamara_cu, 'tamara_cu2': lambda t, s, u: r_tamara_cu(t, s, u, Zh=1.4),
    'kolyan_shop': r_kolyan_shop, 'tamara_under': r_tamara_under, 'tamara_jar': r_tamara_jar, 'semenych_sniff': r_semenych_sniff,
    'shop_phone': lambda t, s, u: r_tamara_cu(t, s, u, expr='annoyed'), 'tamara_phone': r_tamara_phone, 'mates_glance': r_mates_glance,
    'yard_mounds': r_yard_mounds, 'v_radio': r_v_radio, 'bench_two': lambda t, s, u: r_bench(t, s, u, 800, 470, 1.25),
    'zina_cu': lambda t, s, u: granny_cu(t, s, u, 'zina'), 'lyuba_cu': lambda t, s, u: granny_cu(t, s, u, 'lyuba'),
    'zina_shout': lambda t, s, u: granny_cu(t, s, u, 'zina', expr='normal', hand_n=F.H(5.4, 12.6)),
    'mounds_cu': r_mounds_cu, 'mounds_back': lambda t, s, u: r_yard_mounds(t, s, u, back=True),
    'fail1': lambda t, s, u: r_fail(t, s, u, 1), 'fail2': lambda t, s, u: r_fail(t, s, u, 2),
    'dress': r_dress, 'dress_mirror': r_dress_mirror, 'dm_walk': r_dm_walk, 'dm_hello': r_dm_hello, 'sneg_cu': r_sneg_cu,
    'dm_poem': r_dm_poem,
    'v_flag': r_v_flag, 'v_flag_cu': lambda t, s, u: r_v_flag_cu(t, s, u), 'journal': r_journal, 'zina_read': r_zina_read,
    'v_shock': r_v_shock, 'tilt_up': r_tilt_up, 'cat_agent': r_cat_agent, 'v_betrayed': lambda t, s, u: r_v_flag_cu(t, s, u, 'shout'),
    'cat_agent2': lambda t, s, u: r_cat_sill(t, s, u, Zh=4.0, lid=0.7, extra=can_paw, expr='smug'),
    'bench_terms': r_bench_terms, 'v_defeat': r_v_defeat,
    'party_wide': lambda t, s, u: r_party_wide(t, s, u), 'tamara_enter': r_tamara_enter,
    'party_toast': lambda t, s, u: r_party_wide(t, s, u, toast=True, cx=700, cy=330, Z=0.85), 'lyuba_eat': r_lyuba_eat,
    'party_dance': lambda t, s, u: r_party_wide(t, s, u, dance=True, cx=660, cy=320, Z=0.75), 'party_zina': r_party_zina,
    'trio_door': r_trio_door, 'cat_lap': r_cat_lap,
    'yard_midnight': r_yard_midnight, 'trio_bench': r_trio_bench, 'trio_v': lambda t, s, u: trio_cu(t, s, u, 'v'),
    'trio_kolyan': lambda t, s, u: trio_cu(t, s, u, 'k'), 'trio_semenych': lambda t, s, u: trio_cu(t, s, u, 's'),
    'nina_come': lambda t, s, u: r_nina(t, s, u, True), 'nina_cu': lambda t, s, u: r_nina(t, s, u), 'v_guard': r_v_guard,
    'window_zina': r_window_zina, 'yard_wide_end': lambda t, s, u: r_yard_midnight(t, s, u, end=True), 'cat_final': r_cat_final,
    'credits': r_credits, 'summer': r_summer, 's2_card': r_s2,
}
NOHUD = ('title', 'credits', 's2_card', 'summer', 'fail1', 'fail2', 'split3')
NOCAP = ('title', 'credits', 's2_card')


def render_scene(t):
    s = TL.shot_at(t)
    return SHOT[s['name']](t, s, t - s['t0'])


def stickers():
    if 'st' in _IMG: return _IMG['st']
    out = [(O.sticker('ДЗЫНЬ!', fg=(255, 236, 120), size=60), TL.first('garage_ring')['t0'] + 0.1, TL.first('garage_ring')['t1'], 1500, 220),
           (O.sticker('ДЗЫНЬ!', fg=(255, 236, 120), size=60), TL.first('sroom_ring')['t0'] + 0.1, TL.first('sroom_ring')['t1'], 1500, 220),
           (K.lcd_sticker('20:00', (255, 120, 90)), TL.first('table_pan')['t0'] + 0.2, TL.first('table_pan')['t1'], 1640, 230),
           (K.lcd_sticker('21:40', (255, 120, 90)), TL.first('shop_wide')['t0'] + 0.2, TL.first('shop_wide')['t1'], 1640, 230),
           (K.lcd_sticker('22:30', (255, 120, 90)), TL.first('yard_mounds')['t0'] + 0.2, TL.first('yard_mounds')['t1'], 1640, 230),
           (K.lcd_sticker('23:10', (255, 120, 90)), TL.first('dm_walk')['t0'] + 0.2, TL.first('dm_walk')['t1'], 1640, 230),
           (K.lcd_sticker('23:50', (255, 120, 90)), TL.first('party_wide')['t0'] + 0.2, TL.first('party_wide')['t1'], 1640, 230),
           (K.lcd_sticker('00:00', (255, 120, 90)), TL.first('yard_midnight')['t0'] + 0.2, TL.first('yard_midnight')['t1'], 1640, 230),
           (O.sticker('ДВОЙНОЙ АГЕНТ', fg=(255, 130, 110), size=56), TL.first('cat_agent')['t0'] + 0.3, TL.first('cat_agent')['t1'], 1380, 260),
           (O.sticker('КОМПОТ 70°', fg=(255, 150, 170), size=56), TL.first('tamara_jar')['t0'] + 0.4, TL.first('tamara_jar')['t1'], 1450, 250),
           (O.sticker('АБИБАС', fg=(255, 255, 255), size=56), TL.first('zina_shout')['t0'] + 0.6, TL.first('zina_shout')['t1'], 1450, 760)]
    _IMG['st'] = out
    return out


def hud(big, s):
    O.overlay(big, img('badge', lambda: badge('ВАЛЕРА И КОТ • ПРОПУСКНОЙ РЕЖИМ', 26)), 34, 30, 1.0)


def render(t):
    s = TL.shot_at(t)
    u = t - s['t0']
    big = render_scene(t)
    if s is TL.SHOTS[0] or s is TL.SHOTS[1]:
        hk = img('hook', lambda: O.winter_title(['ГОСТИ', 'НЕ ПРОЙДУТ?!'], 84, width=1900))
        if 0.08 <= t < 2.6:
            k = min(1.0, (t - 0.08) / 0.1) * (1 - sm((t - 2.45) / 0.15))
            O.overlay(big, hk, 10, 470, k)
    for im, t0, t1, cx, cy in stickers(): O.draw_sticker(big, im, t, t0, t1, cx, cy)
    if s['name'] not in NOCAP: EPI.captions.draw(big, t, 950)
    if s['name'] not in NOHUD: hud(big, s)
    if s['name'] in ('tilt_up',) and u < 0.15: O.flash(big, 0.6 * (1 - u / 0.15))
    if s['name'] in ('title', 'party_wide', 'yard_midnight', 'shop_wide', 'garage_ring', 'credits') and u < 0.3:
        O.mosaic(big, int(lerp(40, 1, u / 0.3)))
    return big


CUTS, NAMES = TL.CUTS, TL.NAMES


def sheet(ids):
    tiles = []
    for x in ids:
        i = int(x) if x.isdigit() else NAMES.index(next(nm for nm in NAMES if nm == x or nm[3:] == x))
        s = TL.SHOTS[i]; tm = (s['t0'] + s['t1']) / 2
        im = Image.fromarray(render(tm)).resize((480, 270), Image.LANCZOS)
        ImageDraw.Draw(im).text((6, 4), f'{NAMES[i]} {tm:.1f}', fill=(255, 255, 0))
        tiles.append(im)
    cols = 3; rows = (len(tiles) + cols - 1) // cols
    sh = Image.new('RGB', (480 * cols, 270 * rows))
    for k, im in enumerate(tiles): sh.paste(im, ((k % cols) * 480, (k // cols) * 270))
    out = P.build(BK, 'msheet.png'); sh.save(out); print(out)


if __name__ == '__main__':
    if sys.argv[1] == 'sheet': sheet(sys.argv[2:])
    else: EPI.main(render, __file__)
