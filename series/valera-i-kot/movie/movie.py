"""«Валера и кот. Дембельский альбом» — extended season cut, 16:9 1920x1080, rendered by shots (timeline.py).
  python3 movie.py sheet <shot|index> ...   12-up mini sheet of shot middles (build/valera-i-kot-movie/msheet.png)
  python3 movie.py test|frames t ...  |  all  |  shots <i|name> ...      (engine/episode.py CLI)
  python3 mix.py                      -> final.mp4
Frame: 1 January, 05:40, the flat is freezing; Valera fills his DMB album with the season (stencil captions), the cat pencils in
the truth. The episodes come alive inside the album photos. Twist: the ZhEK rings the doorbell — Nina Petrovna wants a bath."""
import os
os.environ['PV_WIDE'] = '1'
import sys, pathlib, math, subprocess
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
from props import bytfx as B
from props import panelka as PK
from props import vikit as K
from props import newyear as NY
from props import album as AL
import timeline as TL

assert (OUT_W, OUT_H) == (1920, 1080)
SX, SY = 320, 180
EPI = Episode('movie', TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG,
              endcard=dict(style='default', lang='ru', sec=3.0, cy=880))
talk = EPI.talk
BK = f'{TL.SLUG}-movie'


def mouth(who, t, k=1.6):
    return min(1.0, talk(who, t) * k)


def begin():
    ST.set_px(1)                                     # heroes always at full logical resolution (1 px = 3 output px)
    return Chars(), Chars()


# ---------------------------------------------------------------- worlds
W = PK.build()


def kitchen_jan():
    img = Image.fromarray(PK.q(Image.open(PK.BG / 'kitchen.png').convert('RGB')))
    x0, y0, x1, y1 = PK.CALENDAR
    a = np.array(img); a[y0 + 62:y1 - 6, x0 + 6:x1 - 6] = (238, 234, 222); img = Image.fromarray(a)
    img = PK.text(img, 'ЯНВАРЬ', (x0 + x1) / 2, y0 + 72, 8, (170, 40, 36))
    img = PK.text(img, '1', (x0 + x1) / 2, y0 + 104, 32, (40, 36, 40))
    return np.array(img)


def notice_world(lines, stamp=True, warm=False):
    img = Image.fromarray(PK.q(Image.open(PK.BG / 'stairwell.png').convert('RGB')))
    img = PK.notice(img, lines)
    if stamp:
        st = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(st)
        d.ellipse((4, 4, 59, 59), outline=(190, 30, 36, 255), width=3); d.ellipse((11, 11, 52, 52), outline=(190, 30, 36, 255), width=1)
        st = PK.text(st, 'ЖЭК', 32, 27, 8, (190, 30, 36, 255)); st = PK.text(st, '№3', 32, 39, 8, (190, 30, 36, 255))
        st = st.rotate(-18, resample=Image.NEAREST)
        x0, y0, x1, y1 = PK.NOTICE
        img.paste(st, (x1 - 60, y1 - 64), st)
    a = np.array(img)
    if warm: a = np.clip(a * np.array([1.12, 1.04, 0.86]) + 10, 0, 255).astype(np.uint8)
    return a


KIT = kitchen_jan()
BATH, TUB, TUBXY = W['bath'], W['tub'], W['tub_xy']
HALL = PK.q(Image.open(PK.BG / 'hallway.png').convert('RGB'))
STAIR = notice_world([('ОБЪЯВЛЕНИЕ', 8, (40, 36, 40)), ('С 01.01', 16, (170, 30, 30)), ('ПЛАНОВОЕ', 8, (40, 36, 40)),
                      ('ОТКЛЮЧЕНИЕ', 8, (40, 36, 40)), ('ГОРЯЧЕЙ ВОДЫ', 8, (170, 30, 30)), ('ЖЭК №3', 8, (60, 60, 120))])
STAIR_S0 = notice_world([('ОБЪЯВЛЕНИЕ', 8, (40, 36, 40)), ('С 01.06', 16, (170, 30, 30)), ('ПЛАНОВОЕ', 8, (40, 36, 40)),
                         ('ОТКЛЮЧЕНИЕ', 8, (40, 36, 40)), ('ГОРЯЧЕЙ ВОДЫ', 8, (170, 30, 30)), ('НА 14 ДНЕЙ', 8, (40, 36, 40))],
                        stamp=False, warm=True)
STAIR_S1 = notice_world([('ОБЪЯВЛЕНИЕ', 8, (40, 36, 40)), ('С 01.06', 16, (170, 30, 30)), ('ПЛАНОВОЕ', 8, (40, 36, 40)),
                         ('ОТКЛЮЧЕНИЕ', 8, (40, 36, 40)), ('ГОРЯЧЕЙ ВОДЫ', 8, (170, 30, 30)), ('НА 14 ДНЕЙ', 8, (40, 36, 40))],
                        stamp=True, warm=True)
POOL = PK.q(Image.open(PK.BG / 'pool.png').convert('RGB'))
SPRING = PK.q(Image.open(PK.BG / 'yard_spring.png').convert('RGB'))
SUMMER = PK.q(Image.open(PK.BG / 'yard_summer.png').convert('RGB'))
TABLE = PK.q(Image.open(PK.BG / 'table_top.png').convert('RGB'))

KIT_GARLAND = [(10, 34), (420, 22), (840, 26), (1275, 40)]
VK = (985.0, 722.0, 16.5)                    # Valera on the kitchen stool, facing right (towards the table)
NK = (1192.0, 492.0, 15.0)                   # Nina at the far side of the table, facing left (anchor = table line)
VH = (880.0, 716.0, 15.0)                    # Valera in the hallway, facing left (the front door)
NB = (468.0, 436.0, 15.0)                    # Nina in the tub (waterline)
VB = (1010.0, 690.0, 15.5)                   # Valera at the bathroom door with the camera, facing left
CAT_WASH = (1150.0, 424.0, 7.5)
NS = (640.0, 560.0, 17.0)                    # Nina on the landing (waist)
NP = (330.0, 640.0, 21.0)                    # Nina by the yard pool (waist below frame)
VS = (520.0, 600.0, 9.4)                     # Valera in the summer yard
CS = (600.0, 600.0, 4.2)                     # the cat next to him


# ---------------------------------------------------------------- lights
def light_kit(v): return K.light_kit(v)


def light_bath(v): return K.light_bath(v)


def light_hall(v):
    lx, ly = v.opt(650, 60)
    return Light(amb=(1.0, 0.95, 0.88), keys=[(lx, ly, 1500, (255, 206, 140), 0.7)], rim=(1, -0.3, (255, 236, 200), 0.3))


def light_stair(v):
    lx, ly = v.opt(*PK.LAMP_S)
    return Light(amb=(0.9, 0.96, 0.92), keys=[(lx, ly, 1300, (255, 214, 150), 0.6)], rim=(-1, -0.3, (190, 220, 255), 0.35), grad=(1.04, 0.9))


def light_pool(v):
    wx, wy = v.opt(700, 560)
    sx, sy = v.opt(1240, 240)
    return Light(amb=(0.78, 0.88, 1.08), keys=[(wx, wy, 1400, (130, 255, 214), 0.65), (sx, sy, 1300, (255, 206, 140), 0.4)],
                 rim=(0, 1, (150, 255, 220), 0.35), grad=(0.95, 1.05))


def light_frost(v):
    return Light(amb=(0.8, 0.92, 1.18), keys=[], rim=(1, -0.3, (210, 236, 255), 0.5), grad=(1.04, 0.9))


def light_summer(v):
    sx, sy = v.opt(1100, -100)
    return Light(amb=(1.04, 1.0, 0.92), keys=[(sx, sy, 2400, (255, 236, 180), 0.5)], rim=(1, -0.6, (255, 240, 190), 0.5), grad=(1.04, 0.94))


# ---------------------------------------------------------------- camera helpers
_BG = {}


def blurred(world, v, r):
    key = (id(world), round(v.X0, 1), round(v.Y0, 1), round(v.Z, 3), r)
    if key not in _BG:
        if len(_BG) > 6: _BG.clear()
        big = v.bg()
        if r: big = np.array(Image.fromarray(big).filter(ImageFilter.GaussianBlur(r)))
        _BG[key] = big
    return _BG[key].copy()


def hview(world, wx, wy, Z, sx, sy):
    """unclamped view: world point (wx, wy) lands exactly on logical (sx, sy) — heroes in close-ups"""
    v = View(world, 0, 0, Z)
    v.X0, v.Y0 = wx - sx / Z, wy - sy / Z
    return v


def cu(world, head, at, Zh, Zb=1.3, blur=5, light=light_kit, draw=None, pre=None, post=None, bg_center=None):
    """close-up: background at zoom Zb (soft), the hero drawn at zoom Zh with its `head` world point pinned at logical `at`"""
    bx, by = bg_center or head
    vb = view_at(world, bx, by, Zb, at[0], at[1])
    big = blurred(world, vb, blur)
    if pre: pre(big, vb)
    vh = hview(world, head[0], head[1], Zh, at[0], at[1])
    CH, FXL = begin()
    if draw: draw(CH, vh)
    CH.comp(big, light(vb))
    if post: post(big, vb, vh)
    fx.vignette(big, 0.3)
    return big


def scene(world, cx, cy, Z, light, draw=None, pre=None, post=None, sx=SX, sy=SY):
    v = view_at(world, cx, cy, Z, sx, sy)
    big = v.bg()
    if pre: pre(big, v)
    CH, FXL = begin()
    if draw: draw(CH, v)
    CH.comp(big, light(v))
    if post: post(big, v)
    fx.vignette(big, 0.3)
    return big


# ---------------------------------------------------------------- heroes
EXPR_V = dict(p_v1='sad', p_v2='proud', p_v3='proud', a_v1='angry', b_v1='proud', c_v1='whisper', c_v2='shock', d_v1='proud',
              t_v1='squint', t_v2='smug', t_v3='smug', e_v1='squint', f_v1='sad', z_v1='sly', k_v1='shout', h_v1='proud')
EXPR_N = dict(t_n1='bored', t_n2='angry', t_n3='shock', e_n1='angry', e_n2='smug', f_n1='blissful', f_n2='shock', h_n1='shock')
SIT = dict(F.VPOSE['sit'], n=(6.6, 11.2), bn=1)
SIT_CU = SIT
HIPS = dict(F.VPOSE['hips'], n=(6.0, 11.4), bn=1)


def zenit(L, h):
    """Soviet film camera «Зенит» held at the face"""
    x, y = h
    F.poly(L, [(x - 1.6, y - 1.0), (x + 1.4, y - 1.0), (x + 1.4, y + 1.1), (x - 1.6, y + 1.1)], (38, 38, 44))
    F.poly(L, [(x - 0.6, y - 1.0), (x + 0.6, y - 1.0), (x + 0.3, y - 1.7), (x - 0.3, y - 1.7)], (52, 52, 60))
    F.ell(L, (x + 1.9, y + 0.05), 0.9, 0.95, (90, 92, 104), 0, (150, 154, 170), (50, 50, 58))
    F.ell(L, (x + 2.1, y + 0.05), 0.45, 0.5, (40, 70, 110), 0, (120, 170, 230))
    F.dot(L, (x - 1.1, y - 1.3), (200, 200, 210), 0.3)


def panama(L):
    F.ell(L, F.H(0.7, 24.6), 4.6, 0.9, (246, 240, 220), 0, (255, 252, 240), (210, 200, 176))
    F.ell(L, F.H(0.7, 25.6), 3.0, 1.4, (246, 240, 220), 0, (255, 252, 240), (210, 200, 176))
    F.cap(L, F.H(-2.2, 24.9), F.H(3.6, 24.9), 0.22, 0.22, (90, 150, 220))


def valera_k(CH, v, t, expr='normal', pose=None, key=None, cold=0.0, **kw):
    x, y, un = VK
    F.valera(CH, v.cam(x, y, un), pose or SIT, t, mouth('valera', t), EXPR_V.get(key, expr), 'sheet' if key == 'p_v1' else 'home',
             hat='ushanka',
             cold=cold, **kw)


def nina_k(CH, v, t, expr='bored', cold=0.0, **kw):
    x, y, un = NK
    kw.setdefault('hand_n', F.H(3.4, 2.8))
    F.nina(CH, v.cam(x, y, un, flip=True), t, mouth('nina', t), expr, False, cap_=True, outfit='coat', cold=cold, **kw)


def cat_k(CH, v, t, lid=0.55, expr='deadpan', look=(0.0, 0.0), extra=None):
    x, y = PK.CAT_K
    cam = v.cam(x, y, PK.CAT_K_UNIT)
    F.cat(CH, cam, t=t, pose='loaf', mouth=mouth('cat', t, 2.0), lid=lid, look=look, expr=expr, tail=0.6)
    if extra:
        L = Layer(cam); extra(L); F.outline(L); CH.add(L)


def pencil_ear(L):
    F.cap(L, F.H(5.0, 10.1), F.H(9.2, 8.4), 0.32, 0.32, (242, 196, 50), None, (200, 150, 30))
    F.cap(L, F.H(9.2, 8.4), F.H(10.0, 8.1), 0.22, 0.08, (226, 196, 150))
    F.cap(L, F.H(4.7, 10.2), F.H(5.1, 10.05), 0.3, 0.3, (236, 140, 150))


def paw_pencil(k):
    def draw(L):
        F.cap(L, F.H(6.4, 1.2), F.H(7.2, lerp(2.0, 5.2, k)), 0.9, 0.85, (240, 140, 40), (255, 180, 90), (200, 104, 30))
        px, ph = 7.2, lerp(2.0, 5.2, k)
        F.cap(L, F.H(px - 1.6, ph - 1.8), F.H(px + 1.6, ph + 3.8), 0.3, 0.3, (242, 196, 50), None, (200, 150, 30))
        F.cap(L, F.H(px + 1.6, ph + 3.8), F.H(px + 1.9, ph + 4.5), 0.2, 0.06, (70, 70, 78))
        F.ell(L, F.H(px, ph), 1.0, 0.9, (248, 244, 236), 0, (255, 255, 255), (214, 206, 196))
    return draw


def paw_salute(k):
    def draw(L):
        hx, hh = lerp(6.6, 9.4, k), lerp(1.6, 9.4, k)
        F.cap(L, F.H(6.0, 1.6), F.H(hx, hh), 0.95, 0.85, (240, 140, 40), (255, 180, 90), (200, 104, 30))
        F.ell(L, F.H(hx, hh + 0.4), 1.05, 0.9, (248, 244, 236), 0.6, (255, 255, 255), (214, 206, 196))
        pencil_ear(L)
    return draw


# ---------------------------------------------------------------- kitchen
def kit_fx(big, v, t, bulbs=True):
    if bulbs:
        FXL = Chars()
        b = NY.garland(FXL, v, t, KIT_GARLAND, n=26, sag=24)
        B.snow_in(FXL, v, t, PK.WINDOW_OPEN, n=30, drift=(-90, 220))
        FXL.comp(big)
        NY.garland_glow(big, v, t, b)
    B.steam(big, v, t, 1110, 350, -99, n=3, rise=120, size=26, a=0.25)              # the kettle is cold... almost


def v_cu(t, s, u, expr=None, Zh=1.55, at=(250, 158), shake=0.0, **kw):
    key = s.get('key', '')
    fx_, fy_ = K.face_w(*VK, h=20.6)
    cold = 0.55 if key == 'p_v1' else 0.0
    pose = dict(SIT, n=(-0.2, 14.4), f=(2.3, 14.0)) if key == 'p_v1' else (kw.pop('pose', None) or SIT_CU)
    def draw(CH, vh): valera_k(CH, vh, t, expr or 'normal', pose, key, cold=cold, **kw)
    big = cu(KIT, (fx_, fy_), at, Zh + 0.04 * u, Zb=1.25, blur=5, light=light_kit, draw=draw,
             pre=lambda b, vb: kit_fx(b, vb, t), bg_center=(fx_ + 30, fy_ + 40))
    if key == 'p_v1': B.shake(big, t, 3, 45)
    if shake: B.shake(big, t, shake, 40)
    return big


def cat_cu(t, s, u, Zh=2.9, at=(330, 176), extra=None, lid=None):
    x, y = PK.CAT_K
    hx, hy = x + 4.4 * PK.CAT_K_UNIT, y - 6.9 * PK.CAT_K_UNIT
    key = s.get('key', '')
    expr = 'smug' if key in ('t_c1', 'c_c1', 'z_c1') else 'deadpan'
    if extra is None and s['t0'] > TL.first('cat_pencil')['t0']: extra = pencil_ear
    lid = lid if lid is not None else (0.72 if key in ('t_c1', 't_c2') else 0.55)
    big = cu(KIT, (hx, hy), at, Zh + 0.05 * u, Zb=1.3, blur=5, light=light_kit, draw=lambda CH, vh: cat_k(CH, vh, t, lid, expr, (0.6, -0.2), extra),
             pre=lambda b, vb: kit_fx(b, vb, t), bg_center=(hx + 40, hy - 10))
    return big


def nina_cu(t, s, u, expr=None, cold=0.0, Zh=1.35, at=(390, 196), shake=0.0, hand=None):
    x, y, un = NK
    hx, hy = x - 0.95 * un, y - 9.5 * un
    e = expr or EXPR_N.get(s.get('key', ''), 'bored')
    kw = {}
    if hand is not None: kw['hand_n'] = hand
    big = cu(KIT, (hx, hy), at, Zh + 0.04 * u, Zb=1.25, blur=5, light=light_kit,
             draw=lambda CH, vh: nina_k(CH, vh, t, e, cold=cold, **kw), pre=lambda b, vb: kit_fx(b, vb, t, bulbs=False),
             bg_center=(hx - 40, hy + 30))
    if shake: B.shake(big, t, shake, 40)
    return big


def kit_two(t, s, u, grand=False, salute=False):
    Z = 0.92 + 0.03 * u
    def draw(CH, v):
        if not salute:
            nina_k(CH, v, t, 'blissful' if grand else ('bored' if u > 0.6 else 'smug'), cold=0.5 if grand else 0.0,
                   prop_n=None)
            L = Layer(v.cam(*NK)); B.basin(L, F.H(-4.0, 0.8), scale=0.9); F.outline(L); CH.add(L)
        if salute:
            F.valera(CH, v.cam(*VK), F.VPOSE['salute'], t, mouth('valera', t), 'shout', 'home', hat='ushanka')
        elif grand:
            valera_k(CH, v, t, 'sly', dict(SIT, n=(9.6, 17.0)), 'z_v1')
        else:
            valera_k(CH, v, t, 'smug')
    def post(big, v):
        if not salute:
            cx, cy = PK.CAT_K
        kit_fx(big, v, t)
    cx = 1110 if not salute else 900
    big = scene(KIT, cx, 440, Z, light_kit, draw, post=post)
    return big


def radio(t, s, u):
    v = view_at(KIT, 520, 300, 1.3, SX, SY)
    big = blurred(KIT, v, 6)
    FXL = Chars(); B.snow_in(FXL, v, t, PK.WINDOW_OPEN, n=40, drift=(-90, 220)); FXL.comp(big)
    k = mouth('robot', t, 2.0)
    im = Image.new('RGBA', (900, 520), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 60, 899, 519], 40, fill=(120, 70, 40, 255), outline=(40, 22, 14, 255), width=10)       # case
    d.rounded_rectangle([40, 110, 520, 480], 24, fill=(196, 196, 186, 255), outline=(60, 50, 40, 255), width=6)     # grille
    for i in range(14):
        yy = 130 + i * 25
        d.line([(60, yy), (500, yy)], fill=(110, 110, 104, 255), width=8)
    d.rounded_rectangle([560, 110, 860, 260], 14, fill=(30, 22, 16, 255))                                     # dial window
    glow = int(160 + 90 * k)
    d.rounded_rectangle([572, 122, 848, 248], 10, fill=(glow, int(glow * 0.62), 40, 255))
    for i in range(9): d.line([(590 + i * 30, 140), (590 + i * 30, 160 + (i % 2) * 12)], fill=(60, 30, 10, 255), width=3)
    nx = 600 + int(200 * (0.5 + 0.5 * math.sin(t * 0.7)))
    d.line([(nx, 130), (nx, 240)], fill=(200, 30, 20, 255), width=5)
    for cx_ in (630, 790):
        d.ellipse([cx_ - 48, 320, cx_ + 48, 416], fill=(60, 36, 22, 255), outline=(220, 200, 160, 255), width=5)
        d.line([(cx_, 330), (cx_, 360)], fill=(220, 200, 160, 255), width=6)
    d.line([(820, 64), (900, -60)], fill=(170, 170, 176, 255), width=8)                                       # antenna
    lab = AL.text_img(['ВЭФИК'], 32, (236, 206, 120), shadow=(60, 34, 14))
    im.alpha_composite(lab, (710 - lab.width // 2, 432))
    a = np.array(im)
    grille = a[110:480, 40:520]
    if k > 0.05:                                                                                            # the grille breathes
        grille[..., :3] = np.clip(grille[..., :3] * (1 + 0.25 * k), 0, 255).astype(np.uint8)
    AL.paste(big, a, 510, 470 + int(4 * math.sin(t * 40) * k))
    if k > 0.05:
        for r_ in (1, 2, 3):
            rr = int(80 + r_ * 60 + (t * 300) % 60)
            ImageDraw.Draw(im2 := Image.fromarray(big)).arc([790 - rr, 760 - rr, 790 + rr, 760 + rr], 200, 250, fill=(255, 240, 200), width=6)
            big[:] = np.array(im2)
    fx.vignette(big, 0.35)
    return big


# ---------------------------------------------------------------- bathroom
def nina_bath(CH, v, t, cold, expr, cap_=True):
    F.nina(CH, v.cam(*NB, flip=True), t, max(0.55, mouth('nina', t)) if cold else mouth('nina', t), expr, True, cap_=cap_,
           cold=cold, foam=not cold)


def r_nina_ice(t, u, shake=True):
    hx, hy = NB[0] - 0.95 * NB[2], NB[1] - 9.5 * NB[2]
    v = view_at(BATH, hx - 70, hy + 10, 1.45, SX, SY)
    big = v.bg()
    CH, FXL = begin()
    nina_bath(CH, v, t, 0.85, 'shock')
    CH.comp(big, K.light_cold(v))
    K.occlude(big, v, TUB, TUBXY)
    B.spray(FXL, v, t, PK.SHOWER, spread=70, drop=300, n=110)
    FXL.comp(big)
    fx.grade(big, (0.92, 1.0, 1.12))
    fx.vignette(big, 0.3)
    if shake: B.shake(big, t, 8, 37)
    return big


def r_bath_wide(t, u):
    v = view_at(BATH, 640, 360, 0.52, SX, SY)
    big = v.bg()
    CH, FXL = begin()
    nina_bath(CH, v, t, 0.0, 'blissful')
    F.cat(CH, v.cam(*CAT_WASH), t, 'sit', 0.0, 0.7, (-0.6, 0.0), 'smug', tail=0.5)
    F.valera(CH, v.cam(*VB, flip=True), dict(F.VPOSE['phone'], n=(2.6, 21.2), f=(3.6, 20.4)), t, 0.0, 'sly', 'home',
             hat='ushanka', prop_n=lambda L, h: zenit(L, (h[0] - 0.4, h[1])))
    CH.comp(big, light_bath(v))
    K.occlude(big, v, TUB, TUBXY)
    FXL2 = Chars()
    if u > 0.55: B.spray(FXL2, v, t, PK.SHOWER, spread=60, drop=260, n=60)
    FXL2.comp(big)
    for i in range(6): B.steam(big, v, t, 160 + 90 * i, 420, -99, n=3, rise=240, size=50, a=0.4 * (1 - sm((u - 0.55) / 0.3)), seed=i * 5)
    fx.vignette(big, 0.3)
    return big


# ---------------------------------------------------------------- hallway / landing
def r_doorbell(t, u):
    v = view_at(HALL, 600, 230, 1.35, SX, SY)
    big = v.bg()
    B.steam(big, v, t, 1030, 330, -99, n=4, rise=180, size=36, a=0.3)
    for r_ in range(3):                                                                             # ring waves from the bell
        rr = int(((u * 2.2 + r_ / 3) % 1) * 420)
        im = Image.fromarray(big); ImageDraw.Draw(im).ellipse([1460 - rr, 380 - rr, 1460 + rr, 380 + rr], outline=(255, 236, 150), width=8)
        big[:] = np.array(im)
    fx.vignette(big, 0.35)
    B.shake(big, t, 9 if u < 0.5 else 3, 45)
    return big


def r_v_hall(t, u, s):
    key = s.get('key', '')
    x, y, un = VH
    fx_, fy_ = K.face_w(x, y, un, flip=True, h=20.6)
    pose = HIPS
    return scene(HALL, fx_ - 40, fy_ + 70, 1.35 + 0.03 * u, light_hall,
                 lambda CH, v: F.valera(CH, v.cam(x, y, un, flip=True), pose, t, mouth('valera', t), EXPR_V.get(key, 'smug'), 'home',
                                        hat='ushanka', look=-0.4),
                 post=lambda big, v: B.steam(big, v, t, 1030, 330, -99, n=4, rise=180, size=36, a=0.3))


_FISH = {}


def fisheye(big, cx=960, cy=540, R=520):
    if 'map' not in _FISH:
        yy, xx = np.mgrid[0:OUT_H, 0:OUT_W].astype(np.float32)
        dx, dy = xx - cx, yy - cy
        r = np.sqrt(dx * dx + dy * dy) / R
        k = 0.5 + 0.5 * np.clip(r, 0, 1) ** 1.6
        sx = np.clip(cx + dx * k, 0, OUT_W - 1).astype(np.int32); sy = np.clip(cy + dy * k, 0, OUT_H - 1).astype(np.int32)
        _FISH['map'] = (sy, sx, r)
    sy, sx, r = _FISH['map']
    out = big[sy, sx]
    out[r > 1.0] = (14, 10, 8)
    ring = (r > 0.96) & (r <= 1.0); out[ring] = (90, 84, 70)
    shade = np.clip(1.15 - 0.55 * r, 0.5, 1.0)[..., None]
    big[:] = (out * shade).astype(np.uint8)


def nina_land(CH, v, t, expr, cold=0.0, basin=True):
    x, y, un = NS
    F.nina(CH, v.cam(x, y, un, flip=True), t, mouth('nina', t), expr, False, cap_=True, outfit='coat', cold=cold,
           hand_n=F.H(2.6, 1.2) if basin else None)
    if basin:
        L = Layer(v.cam(x, y, un, flip=True)); B.basin(L, F.H(2.2, 0.2), scale=0.95, tilt=0.15); F.outline(L); CH.add(L)


def r_nina_door(t, u, s):
    x, y, un = NS
    hx, hy = x - 0.95 * un, y - 9.5 * un
    big = scene(STAIR, hx, hy + 30, 1.2, light_stair, lambda CH, v: nina_land(CH, v, t, EXPR_N.get(s.get('key', ''), 'bored')))
    fisheye(big)
    return big


def r_nina_door_cu(t, u, s):
    x, y, un = NS
    hx, hy = x - 0.95 * un, y - 9.5 * un
    def post(big, vb, vh):
        big[:, :560] = (big[:, :560] * 0.12).astype(np.uint8); big[:, 1460:] = (big[:, 1460:] * 0.12).astype(np.uint8)
        big[:, 540:580] = (88, 52, 30); big[:, 1440:1480] = (88, 52, 30)                                  # door + frame edges
        im = Image.fromarray(big); d = ImageDraw.Draw(im)
        for i in range(9):                                                                                   # the door chain
            xx = 580 + i * 98; yy = 520 + int(70 * math.sin(math.pi * i / 8))
            d.ellipse([xx - 30, yy - 16, xx + 30, yy + 16], outline=(196, 200, 206), width=9)
        big[:] = np.array(im)
    return cu(STAIR, (hx, hy), (330, 165), 1.55 + 0.03 * u, Zb=1.3, blur=5, light=light_stair,
              draw=lambda CH, vh: nina_land(CH, vh, t, EXPR_N.get(s.get('key', ''), 'angry'), basin=False), post=post,
              bg_center=(hx, hy + 40))


# ---------------------------------------------------------------- yard
def grannies_pool(CH, v, t, zk=None, lk=None):
    zk = dict(dict(expr='smug', look=0.6), **(zk or {}))
    lk = dict(dict(expr='smug', hand_n=F.H(3.4, 10.4), prop_n=B.cocktail), **(lk or {}))
    F.babushka(CH, v.cam(*PK.PL_ZINA), t, 'zina', 'sit', mouth('zina', t), **zk)
    F.babushka(CH, v.cam(*PK.PL_LYUBA, flip=True), t, 'lyuba', 'sit', mouth('lyuba', t), **lk)
    PK.clip_below(CH, v, PK.PL_WATER, *PK.PL_X)


def pool_fx(big, v, t):
    FXL = Chars()
    L = Layer(v.wcam()); B.duck(L, 690, PK.PL_WATER + 12, 5.0, t); F.outline(L); FXL.add(L)
    B.falling_snow(FXL, v, t, v.X0 - 20, v.Y0 - 20, v.X0 + 660 / v.Z, v.Y0 + 380 / v.Z, n=70, speed=40)
    FXL.comp(big)
    for i, x in enumerate((300, 520, 700, 900, 1060)):
        B.steam(big, v, t, x, PK.PL_WATER + 10, -99, n=3, rise=220, size=50, a=0.3, seed=i * 11)


def r_pool(t, u, who=None, wide=False):
    if wide:
        Z, cx, cy = 0.62 + 0.05 * u, 680, 400
    else:
        if who == 'zina': cx, cy = PK.PL_ZINA[0] + 1.6 * PK.PL_ZINA[2] + 60, PK.PL_ZINA[1] - 11.8 * PK.PL_ZINA[2] + 40
        else: cx, cy = PK.PL_LYUBA[0] - 1.4 * PK.PL_LYUBA[2] - 60, PK.PL_LYUBA[1] - 11.8 * PK.PL_LYUBA[2] + 40
        Z = 0.95 + 0.04 * u
    return scene(POOL, cx, cy, Z, light_pool, lambda CH, v: grannies_pool(CH, v, t), post=lambda big, v: pool_fx(big, v, t))


def r_yard(t, u):
    k = sm(u / 1.1)
    def draw(CH, v):
        F.babushka(CH, v.cam(*PK.SP_ZINA), t, 'zina', 'sit', 0.0, 'smug', 0.6)
        F.babushka(CH, v.cam(*PK.SP_LYUBA, flip=True), t, 'lyuba', 'sit', 0.0, 'smug', hand_n=F.H(3.4, 10.4), prop_n=B.cocktail)
        PK.clip_below(CH, v, PK.SP_WATER, 640, 1200)
    def post(big, v):
        FXL = Chars(); B.falling_snow(FXL, v, t, v.X0 - 20, v.Y0 - 20, v.X0 + 660 / v.Z, v.Y0 + 380 / v.Z, n=80, speed=40); FXL.comp(big)
        B.steam(big, v, t, 840, 600, -99, n=10, rise=380, size=60, a=0.45)
        for i, x in enumerate((680, 760, 940, 1010)): B.steam(big, v, t, x, 605, -99, n=3, rise=160, size=30, a=0.3, seed=i * 5)
    return scene(SPRING, lerp(700, 840, k), lerp(380, 520, k), lerp(0.62, 1.35, k), light_pool, draw, post=post)


def r_nina_frost(t, u):
    x, y, un = NP
    hx, hy = x - 0.95 * un, y - 9.5 * un
    def draw(CH, vh):
        F.nina(CH, vh.cam(x, y, un, flip=True), t, 0.5 + 0.3 * math.sin(t * 40), 'shock', False, cap_=True, outfit='coat', cold=1.0,
               hand_n=F.H(2.6, 1.6))
        L = Layer(vh.cam(x, y, un, flip=True)); B.basin(L, F.H(2.2, 0.6), scale=0.95, tilt=0.15); F.outline(L); CH.add(L)
    def post(big, vb, vh):
        FXL = Chars(); B.falling_snow(FXL, vb, t, vb.X0 - 20, vb.Y0 - 20, vb.X0 + 660 / vb.Z, vb.Y0 + 380 / vb.Z, n=140, speed=60)
        FXL.comp(big)
        fx.grade(big, (0.86, 0.96, 1.16))
        B.shake(big, t, 4, 50)
    return cu(POOL, (hx, hy), (300, 160), 1.25 + 0.04 * u, Zb=1.2, blur=6, light=light_frost, draw=draw, post=post, bg_center=(560, 420))


# ---------------------------------------------------------------- summer
def r_summer_notice(t, u):
    x0, y0, x1, y1 = PK.NOTICE
    w = STAIR_S1 if u >= 0.05 else STAIR_S0
    v = view_at(w, (x0 + x1) / 2 + 40, (y0 + y1) / 2 + 6, 1.9 + 0.1 * u, SX, SY)
    big = v.bg()
    FXL = Chars(); B.falling_snow(FXL, v, t, v.X0, v.Y0 - 20, v.X0 + 660 / v.Z, v.Y0 + 380 / v.Z, n=24, col=(255, 252, 240), speed=10)
    FXL.comp(big)
    fx.grade(big, (1.06, 1.02, 0.94), (8, 6, 0))
    fx.vignette(big, 0.3)
    if 0.05 <= u < 0.3: B.shake(big, t, 10, 50)
    return big


def r_summer(t, u, card=False):
    def draw(CH, v):
        F.valera(CH, v.cam(*VS), F.VPOSE['hold'], t, mouth('valera', t), 'shock' if u > 0.4 else 'blissful', 'towel', hat='ushanka',
                 prop_n=lambda L, h: B.basin(L, (h[0] + 0.4, h[1] - 1.2), scale=0.9, tilt=-0.2))
        L = Layer(v.cam(*VS)); panama(L); F.outline(L); CH.add(L)
        F.cat(CH, v.cam(*CS), t, 'sit', mouth('cat', t, 2.0), 0.6, (-0.5, 0.0), 'deadpan', tail=0.4)
    def post(big, v):
        FXL = Chars()
        B.falling_snow(FXL, v, t, v.X0 - 40, v.Y0 - 20, v.X0 + 680 / v.Z, v.Y0 + 380 / v.Z, n=90, col=(255, 252, 240), speed=12)
        FXL.comp(big)
    if card:
        v = view_at(SUMMER, 640, 360, 0.55, SX, SY)
        big = blurred(SUMMER, v, 4)
        post(big, v)
        fx.vignette(big, 0.3)
        return big
    return scene(SUMMER, 560, 470, 1.35 + 0.05 * u, light_summer, draw, post=post)


# ---------------------------------------------------------------- the album (top-down table)
def _still(n, tt):
    f = pathlib.Path(P.build(BK, f'still_{n}_{tt:05.2f}.png'))
    if not f.exists():
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', f'{tt:.2f}', '-i', str(ROOT / f'series/{TL.SLUG}/episodes/ep0{n}/final.mp4'),
                        '-frames:v', '1', str(f)], check=True)
    return Image.open(f).convert('RGB')


_PHOTO = {}
PH_C = (430, 360)                                # photo centre on the left page
PH_W = 240


def photo(n):
    if n not in _PHOTO:
        if n == 7: fr = Image.fromarray(r_nina_ice(TL.first('nina_ice')['t0'] + 0.6, 0.6, shake=False)).crop((960, 0, 1568, 1080))
        else: fr = _still(n, TL.PHOTO_T[n])
        _PHOTO[n] = AL.photo(fr, PH_W, border=10, tilt=(-2.5 if n % 2 else 2.0))
    return _PHOTO[n]


def photo_rect(n):
    p = photo(n)
    return (PH_C[0] - p.width // 2, PH_C[1] - p.height // 2, PH_C[0] + p.width // 2, PH_C[1] + p.height // 2)


_BASE = {}
STEN = {n: [AL.stencil([l], 16, seed=n * 7 + i) for i, l in enumerate(ls)] for n, ls in TL.STENCIL.items()}
TRUTH = {n: [AL.pencil([l], 16, seed=n * 5 + i) for i, l in enumerate(ls)] for n, ls in TL.TRUTH.items()}
STEN_Y, TRUTH_Y = 236, 472


def base_page(n, ph=True):
    key = (n, ph)
    if key in _BASE: return _BASE[key]
    if 'spread' not in _BASE: _BASE['spread'] = AL.spread(TABLE)
    a = _BASE['spread'].copy()
    if n == 0:                                                                                  # title page
        for img, cx, cy in ((AL.text_img(['ДЕМБЕЛЬСКИЙ', 'АЛЬБОМ'], 24, AL.INK_RED, shadow=(110, 20, 24)), 430, 250),
                            (AL.text_img(['ПРАПОРЩИК', 'ЗАПАСА', 'ВАЛЕРА'], 16, AL.INK_BLUE), 430, 470),
                            (AL.text_img(['ЗИМА', '2026'], 24, AL.INK_BLUE), 850, 250),
                            (AL.text_img(['ДМБ'], 32, AL.INK_RED, shadow=(110, 20, 24)), 850, 450)):
            AL.paste(a, img, cx - img.width // 2, cy - img.height // 2)
        AL.paste(a, AL.decal('ushanka', 8), 806, 520); AL.paste(a, AL.decal('star', 6), 300, 560); AL.paste(a, AL.decal('star', 6), 520, 560)
    elif n == 'spy':
        stills = [(3, 1.0), (3, 4.4), (3, 8.6), (3, 16.4)]
        for i, (e, tt) in enumerate(stills):
            fr = _still(e, tt).crop((0, 300, 1080, 1380))
            p = AL.photo(fr, 160, border=8, tilt=(-4, 3, 2, -3)[i])
            x = (330, 530, 750, 950)[i]; y = (220, 230, 220, 236)[i]
            AL.paste(a, p, x - p.width // 2, y - p.height // 2)
            im = Image.fromarray(a); ImageDraw.Draw(im).ellipse([x - 60, y - 70, x + 60, y + 50], outline=AL.INK_RED, width=5); a = np.array(im)
        for img, cx, cy in ((AL.text_img(['НАБЛЮДЕНИЕ', 'ОБЪЕКТ: ВАЛЕРА'], 16, AL.INK_RED, shadow=(110, 20, 24)), 430, 470),
                            (AL.text_img(['С НОВЫМ ГОДОМ!', 'ЗИНА И ЛЮБА'], 16, AL.INK_BLUE, tilt=4), 850, 480)):
            AL.paste(a, img, cx - img.width // 2, cy - img.height // 2)
        AL.paste(a, AL.decal('heart', 6), 950, 560); AL.paste(a, AL.decal('bench', 6), 700, 570)
    elif n == 'credits':
        for i in range(6):
            p = AL.photo(_still(i + 1, TL.PHOTO_T[i + 1]), 100, border=6, tilt=(-3, 2, -2, 3, -1, 2)[i])
            x = 330 + (i % 2) * 200; y = 160 + (i // 2) * 200
            AL.paste(a, p, x - p.width // 2, y - p.height // 2)
    else:
        if ph:
            p = photo(n); AL.paste(a, p, PH_C[0] - p.width // 2, PH_C[1] - p.height // 2)
        hd = AL.text_img([f'ГЛАВА {n}' if n <= 6 else 'ЭПИЛОГ'], 16, AL.INK_BLUE)
        AL.paste(a, hd, 850 - hd.width // 2, 88)
        title = TL.TITLES[n]
        ti = AL.text_img([title], 24 if len(title) <= 11 else 16, AL.INK_RED, shadow=(110, 20, 24))
        AL.paste(a, ti, 850 - ti.width // 2, 136)
        d1, d2 = TL.DECALS[n]
        AL.paste(a, AL.decal(d1, 7), 290, 92); AL.paste(a, AL.decal(d2, 7), 970, 580)
        AL.paste(a, AL.decal('star', 5), 690, 600)
    _BASE[key] = a
    return a


def lines_reveal(a, imgs, y0, r, x_c=850, left=None, step=None):
    """paste lines one after another; r 0..1 over all of them; returns the world point of the pen (x, y) or None"""
    if not imgs or r <= 0: return None
    n = len(imgs); pen = None
    y = y0
    for i, im in enumerate(imgs):
        k = max(0.0, min(1.0, r * n - i))
        x = (left if left is not None else x_c - im.width // 2)
        if k > 0:
            AL.paste(a, im, x, y, reveal=k)
            if k < 1: pen = (x + im.width * k, y + im.height * 0.55)
        y += step or int(im.height * 0.72)
    return pen


def page(n, st=1.0, tr=1.0, ph=True):
    a = base_page(n, ph).copy()
    pen_s = lines_reveal(a, STEN.get(n), STEN_Y, st) if isinstance(n, int) and n > 0 else None
    pen_t = lines_reveal(a, TRUTH.get(n), TRUTH_Y + (34 if n == 7 else 0), tr, left=690) if isinstance(n, int) and n > 0 else None
    return a, pen_s, pen_t


def table_fx(big, v, t):
    B.steam(big, v, t, 70, 120, -99, n=4, rise=160, size=40, a=0.35)                          # tea glass
    ox, oy = v.opt(1012, 620); fx.glow(big, ox, oy, 260 * v.Z, (255, 200, 120), 0.25 + 0.06 * math.sin(t * 13))
    ox, oy = v.opt(1230, 40); fx.glow(big, ox, oy, 500 * v.Z, (255, 214, 150), 0.18)


def table_view(a, cx, cy, Z, t):
    v = view_at(a, cx, cy, Z, SX, SY)
    big = v.bg()
    table_fx(big, v, t)
    return big, v


def spray_hand(big, x, y, t, on=True):
    """Valera's arm (telnyashka sleeve) from the bottom-right, a red spray can; nozzle at output (x, y)"""
    im = Image.fromarray(big); d = ImageDraw.Draw(im)
    hx, hy = x + 70, y + 120
    for i in range(14):                                                                         # striped sleeve towards the corner
        k0, k1 = i / 14, (i + 1) / 14
        p0 = (hx + 90 + (OUT_W + 300 - hx) * k0, hy + 80 + (OUT_H + 200 - hy) * k0)
        p1 = (hx + 90 + (OUT_W + 300 - hx) * k1, hy + 80 + (OUT_H + 200 - hy) * k1)
        d.line([p0, p1], fill=(240, 244, 250) if i % 2 else (40, 60, 130), width=150)
    d.ellipse([hx - 40, hy - 10, hx + 120, hy + 130], fill=(232, 176, 140), outline=(60, 30, 20), width=5)   # fist
    d.rounded_rectangle([x - 26, y + 10, x + 46, y + 170], 14, fill=(200, 30, 36), outline=(60, 10, 10), width=5)
    d.rectangle([x - 18, y - 12, x + 38, y + 12], fill=(236, 236, 240), outline=(60, 60, 70), width=4)
    d.rectangle([x - 6, y - 26, x + 14, y - 10], fill=(60, 60, 70))
    big[:] = np.array(im)
    if on:
        rng = np.random.default_rng(int(t * 60))
        for _ in range(70):
            dx, dy = rng.normal(0, 26), rng.normal(-50, 22)
            px, py = int(x + dx - 30), int(y + dy)
            if 0 <= px < OUT_W - 6 and 0 <= py < OUT_H - 6: big[py:py + 6, px:px + 6] = (220, 60, 60)


def r_album(t, s, u):
    """album shots on the table"""
    n_ = s['name']; dur = s['t1'] - s['t0']; ch = s.get('n') or s['chap']
    if n_ == 'title':
        a = AL.closed(TABLE) if 'closed' not in _BASE else _BASE['closed']
        _BASE['closed'] = a
        big, v = table_view(a, 640, 360, 0.62 + 0.06 * sm(u / dur), t)
        sub = img('sub', lambda: badge('РАСШИРЕННАЯ ВЕРСИЯ • СЕЗОН 1', 30))
        if u > 0.6: O.overlay(big, sub, (OUT_W - sub.shape[1]) // 2, 980, min(1.0, (u - 0.6) / 0.3))
        sparkle(big, t)
        return big
    if n_ == 'album_open':
        if u < 1.6:
            a = AL.closed(TABLE) if 'closed' not in _BASE else _BASE['closed']
            _BASE['closed'] = a
            big, v = table_view(a, 640, 360, 0.6, t)
            if u > 1.3: O.mosaic(big, int(lerp(2, 30, (u - 1.3) / 0.3)))
            return big
        a, _, _ = page(0)
        big, v = table_view(a, 640, 360, 0.6 + 0.04 * (u - 1.6), t)
        if u < 1.9: O.mosaic(big, int(lerp(30, 1, (u - 1.6) / 0.3)))
        return big
    if n_ == 'card':
        a, _, _ = page(ch, 0.0, 0.0)
        a = a.copy(); AL.page_flip(a, min(1.0, u / 0.55))
        big, v = table_view(a, 640, 360, 0.6, t)
        ti = img(('ct', ch), lambda: O.winter_title([f'ГЛАВА {ch}', TL.TITLES[ch]], 80))
        k = sm((u - 0.45) / 0.2) * (1 - sm((u - (dur - 0.25)) / 0.25))
        if k > 0:
            big[:] = (big * (1 - 0.45 * k)).astype(np.uint8)
            O.overlay(big, ti, 0, (OUT_H - ti.shape[0]) // 2, k)
        return big
    if n_ == 'stencil':
        r = sm(max(0.0, (u - 0.2)) / (dur - 0.5))
        a, pen, _ = page(ch, r, 0.0)
        big, v = table_view(a, 820, 330, 1.05, t)
        if pen is not None or u < 0.3:
            px, py = v.opt(*(pen or (850 - STEN[ch][0].width // 2, STEN_Y)))
            spray_hand(big, px, py, t, on=pen is not None)
        return big
    if n_ == 'truth':
        r = sm(max(0.0, (u - 0.15)) / (dur - 0.45))
        a, _, pen = page(ch, 1.0, r)
        big, v = table_view(a, 820, 400, 1.05, t)
        if pen is not None:
            px, py = v.opt(*pen)
            AL.paw_pencil(big, (px, py + 8), 1.3, 6 * math.sin(t * 40))
        elif u < 0.2 or r >= 1:
            px, py = v.opt(1000, 560)
            AL.paw_pencil(big, (px, py), 1.3, 0)
        return big
    if n_ == 'receipt':
        a, _, _ = page(2, 0.0, 0.0)
        big, v = table_view(a, 760, 330, 1.0, t)
        rc = img('receipt', lambda: np.array(AL.receipt(['ГАСТРОНОМ', '«ДЕШЕВЛЕ НЕТ»', '', 'КОЛБ. ДОКТОРСК.', 'ЦЕНА ...... 289',
                                                           '*ПО КАРТЕ 199', 'КАРТЫ НЕТ', '', 'ПАКЕТ ....... 90', 'СКИДКА ...... 0',
                                                           '', 'ИТОГО: 379', '', 'СПАСИБО', 'ЗА ПОКУПКУ!'], 200, 24).resize((600, 1110), Image.NEAREST)))
        h = int(rc.shape[0] * sm(min(1.0, u / 1.6)))
        if h > 0:
            AL.paste(big, rc[-h:], 1050, 0)
        return big
    if n_ == 'trophy':
        a, _, _ = page(2, 1.0, 0.0)
        big, v = table_view(a, 820, 360, 1.1, t)
        tb = img('trophy', lambda: np.array(AL.trophy_bag(180).resize((450, 562), Image.NEAREST)))
        k = sm(min(1.0, u / 0.35))
        sc = lerp(1.25, 1.0, k)
        im = tb if sc == 1.0 else np.array(Image.fromarray(tb).resize((int(450 * sc), int(562 * sc)), Image.NEAREST))
        AL.paste(big, im, 1180 - im.shape[1] // 2, 520 - im.shape[0] // 2)
        if u > 0.3: sparkle(big, t, (1180, 520), 300)
        return big
    if n_ in ('spy_flip', 'spy_page'):
        a, _, _ = page('spy')
        if n_ == 'spy_flip':
            a = a.copy(); AL.page_flip(a, min(1.0, u / 0.6))
            big, v = table_view(a, 640, 360, 0.6, t)
        else:
            big, v = table_view(a, lerp(560, 660, sm(u / dur)), 300, 1.0 + 0.08 * u, t)
            if u < 0.25: B.shake(big, t, 8, 40)
        return big
    if n_ == 'page_nina':
        a, _, _ = page(4, 1.0, 0.0)
        x0, y0, x1, y1 = photo_rect(4)
        big, v = table_view(a, (x0 + x1) / 2 + 40, (y0 + y1) / 2 - 40, 1.45 + 0.1 * u, t)
        return big
    if n_ in ('page_last', 'photo_fall', 'pages_back'):
        if n_ == 'pages_back':
            k = u / dur * 4
            i = min(3, int(k))
            pg = 7 - i
            a, _, _ = page(pg, 1.0, 1.0)
            a = a.copy(); AL.page_flip(a, 1 - (k - i))
            big, v = table_view(a, 640, 360, 0.6, t)
            return big
        st_ = 1.0 if s['t0'] < TL.first('salute')['t0'] and s['t0'] > TL.first('pages_back')['t0'] + 99 else 0.0
        a, _, _ = page(7, st_, 0.0, ph=(n_ == 'page_last'))
        Z = 0.75 + 0.05 * u if n_ == 'page_last' else 0.75
        big, v = table_view(a, 600, 360, Z, t)
        if n_ == 'photo_fall':
            p = img('ph7', lambda: np.array(photo(7)))
            k = sm(min(1.0, u / 0.45))
            sc = lerp(1.6, 1.0, k)
            im = np.array(Image.fromarray(p).resize((int(p.shape[1] * sc * v.Z * 3), int(p.shape[0] * sc * v.Z * 3)), Image.NEAREST))
            cx, cy = v.opt(*PH_C)
            sh = im.copy(); sh[..., :3] = 0; sh[..., 3] = (sh[..., 3] * 0.4).astype(np.uint8)
            AL.paste(big, sh, cx - im.shape[1] // 2 + int(40 * (1 - k)), cy - im.shape[0] // 2 + int(60 * (1 - k)))
            AL.paste(big, im, cx - im.shape[1] // 2, cy - im.shape[0] // 2)
            if u < 0.12: O.flash(big, 1 - u / 0.12)
        return big
    if n_ == 'credits':
        a, _, _ = page('credits')
        big, v = table_view(a, 640, 360, 0.6, t)
        cr = img('credits', lambda: np.array(AL.text_img(CREDITS, 16, (40, 36, 40), lead=1.7)))
        crs = np.array(Image.fromarray(cr).resize((cr.shape[1] * 2, cr.shape[0] * 2), Image.NEAREST))
        x0, y0 = v.opt(660, 80); x1, y1 = v.opt(1040, 640)
        y = int(y1 - (u / dur) * (y1 - y0 + crs.shape[0] * 0.8))
        reg = big[int(y0):int(y1), int(x0):int(x1)]
        AL.paste(reg, crs, (reg.shape[1] - crs.shape[1]) // 2, y - int(y0))
        return big
    a, _, _ = page(ch or 1)
    return table_view(a, 640, 360, 0.6, t)[0]


CREDITS = ['ВАЛЕРА И КОТ', 'ДЕМБЕЛЬСКИЙ АЛЬБОМ', '', 'В РОЛЯХ:', '', 'ВАЛЕРА', 'ПРАПОРЩИК ЗАПАСА', '', 'ДЕМБЕЛЬ', 'КОТ. ПРАВДА', '',
           'НИНА ПЕТРОВНА', 'ЖЭК №3', '', 'ЗИНА И ЛЮБА', 'РАЗВЕДКА', '', 'ТАМАРА', 'КАССА', '', 'ГОРЯЧАЯ ВОДА', 'НЕ ЯВИЛАСЬ', '',
           'ПАКЕТ — 90 РУБ.', '', 'НИ ОДИН КОТ', 'НЕ ПОСТРАДАЛ.', 'КОТ ПОМЫЛСЯ', 'ПЕРВЫМ.']


def sparkle(big, t, c=(960, 420), R=560):
    rng = np.random.default_rng(5)
    for i in range(26):
        a = rng.uniform(0, 2 * math.pi); r = rng.uniform(0.2, 1.0) * R
        k = max(0.0, math.sin(t * 5 + i * 1.7))
        if k < 0.3: continue
        x, y = int(c[0] + r * math.cos(a)), int(c[1] + r * math.sin(a) * 0.6)
        s_ = int(6 + 12 * k)
        if 20 < x < OUT_W - 20 and 20 < y < OUT_H - 20:
            big[y - 2:y + 2, x - s_:x + s_] = (255, 248, 210); big[y - s_:y + s_, x - 2:x + 2] = (255, 248, 210)


# ---------------------------------------------------------------- the episodes inside the photos
class Clip:
    """sequential frame reader of a video segment, scaled; restarts the decoder on a jump"""
    def __init__(s, path, w, h):
        s.path, s.w, s.h, s.p, s.next, s.last = str(ROOT / path), w, h, None, None, None

    def get(s, t):
        fi = int(round(t * TL.FPS))
        if s.p is None or fi != s.next:
            if fi == (s.next or -9) - 1 and s.last is not None: return s.last
            if s.p: s.p.kill()
            s.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{fi / TL.FPS:.4f}', '-i', s.path, '-vf', f'scale={s.w}:{s.h}:flags=area',
                                    '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
            s.next = fi
        buf = s.p.stdout.read(s.w * s.h * 3)
        if len(buf) < s.w * s.h * 3: return s.last if s.last is not None else np.zeros((s.h, s.w, 3), np.uint8)
        s.last = np.frombuffer(buf, np.uint8).reshape(s.h, s.w, 3)
        s.next = fi + 1
        return s.last


_CLIPS = {}
VW, VHH = 558, 992
_IMG = {}


def img(key, make):
    if key not in _IMG: _IMG[key] = make()
    return _IMG[key]


def r_clip(t, s, u):
    n = s['n']
    if n not in _CLIPS: _CLIPS[n] = Clip(f'series/{TL.SLUG}/episodes/ep0{n}/final.mp4', VW, VHH)
    clip = _CLIPS[n]
    (a1, b1), (a2, b2) = TL.PARTS[n]
    a, _, _ = page(n, 1.0, 0.0, ph=False)
    v = view_at(a, 640, 360, 0.6, SX, SY)
    big = blurred(a, v, 12)
    big[:] = (big * 0.42).astype(np.uint8)
    # left: the chapter plate; right: Valera's stencil version, «ВЕРСИЯ ВАЛЕРЫ»
    pl = img(('cl', n), lambda: np.array(AL.text_img([f'ГЛАВА {n}', TL.TITLES[n]], 24, (250, 240, 214), shadow=(40, 20, 10))))
    O.overlay(big, pl, 340 - pl.shape[1] // 2, 160, 1.0)
    d1, d2 = TL.DECALS[n]
    O.overlay(big, img(('dl', d1), lambda: np.array(AL.decal(d1, 22))), 200, 520, 1.0)
    O.overlay(big, img(('dl2', d2), lambda: np.array(AL.decal(d2, 22))), 1560, 640, 1.0)
    vv = img(('vv', n), lambda: np.array(AL.text_img(['ВЕРСИЯ', 'ВАЛЕРЫ:', ''] + TL.STENCIL[n], 24, (255, 120, 110), shadow=(60, 10, 10))))
    O.overlay(big, vv, 1600 - vv.shape[1] // 2, 140, 1.0)
    # the photo grows from its place on the page into the frame
    x0, y0, x1, y1 = photo_rect(n)
    p0 = v.opt(x0, y0); p1 = v.opt(x1, y1)
    k = sm(min(1.0, u / TL.ZOOM))
    fx0, fy0, fx1, fy1 = (960 - VW // 2 - 14, 540 - VHH // 2 - 14, 960 + VW // 2 + 14, 540 + VHH // 2 + 14)
    rx0, ry0, rx1, ry1 = (int(lerp(p0[0], fx0, k)), int(lerp(p0[1], fy0, k)), int(lerp(p1[0], fx1, k)), int(lerp(p1[1], fy1, k)))
    if t < s['s1']:
        ph = np.array(photo(n).convert('RGBA').resize((rx1 - rx0, ry1 - ry0), Image.LANCZOS))
        AL.paste(big, ph, rx0, ry0)
        if u > TL.ZOOM - 0.1: O.flash(big, 0.3)
        return big
    if t < s['f0']:
        fr = clip.get(a1 + (t - s['s1']))
        ff = False
    elif t < s['s2']:
        kk = (t - s['f0']) / TL.FF
        fr = clip.get(b1 + kk * (a2 - b1)).copy(); ff = True
        fr[::4] = (fr[::4] * 0.5).astype(np.uint8)
        off = int(30 * math.sin(t * 90)); fr[:] = np.roll(fr, off, 1)
    else:
        fr = clip.get(a2 + (t - s['s2'])); ff = False
    big[fy0 + 4:fy1 + 10, fx0 + 10:fx1 + 10] = (big[fy0 + 4:fy1 + 10, fx0 + 10:fx1 + 10] * 0.5).astype(np.uint8)
    big[fy0:fy1, fx0:fx1] = (250, 248, 240)
    big[fy0 + 14:fy0 + 14 + VHH, fx0 + 14:fx0 + 14 + VW] = fr
    tabs = Image.fromarray(big); d = ImageDraw.Draw(tabs)
    for (x, y, sx, sy) in ((fx0, fy0, 1, 1), (fx1, fy0, -1, 1), (fx0, fy1, 1, -1), (fx1, fy1, -1, -1)):
        d.polygon([(x - sx * 6, y - sy * 6), (x + sx * 70, y - sy * 6), (x - sx * 6, y + sy * 70)], fill=(30, 30, 34))
    big[:] = np.array(tabs)
    if ff:
        lab = img('ff', lambda: badge('>> x16', 44))
        O.overlay(big, lab, fx1 + 40, 470, 1.0)
        fx.vhs(big, t, 0.6) if hasattr(fx, 'vhs') else None
    return big


# ---------------------------------------------------------------- dispatch
def shot_render(s, t):
    n = s['name']; u = t - s['t0']; key = s.get('key', '')
    if s['kind'] == 'clip': return r_clip(t, s, u)
    if s['kind'] in ('card', 'stencil', 'truth') or n in ('title', 'album_open', 'receipt', 'trophy', 'spy_flip', 'spy_page', 'page_nina',
                                                          'page_last', 'photo_fall', 'pages_back', 'credits'):
        return r_album(t, s, u)
    if n == 'nina_ice': return r_nina_ice(t, u)
    if n == 'bath_wide': return r_bath_wide(t, u)
    if n == 'cat_cu': return cat_cu(t, s, u)
    if n == 'cat_cu_whisper': return cat_cu(t, s, u, Zh=3.4, at=(300, 170), lid=0.75)
    if n == 'cat_pencil': return cat_cu(t, s, u, extra=paw_pencil(sm(u / 0.6)))
    if n == 'cat_salute': return cat_cu(t, s, u, Zh=3.1, extra=paw_salute(sm(u / 0.35)))
    if n == 'v_cu': return v_cu(t, s, u)
    if n == 'v_cu_whisper': return v_cu(t, s, u, Zh=1.75, at=(280, 170))
    if n == 'v_cu_smug': return v_cu(t, s, u, Zh=1.65, pose=None)
    if n == 'v_smile': return v_cu(t, s, u, expr='sly', Zh=lerp(1.5, 1.9, sm(u / 1.4)))
    if n == 'v_med':
        return scene(KIT, 900, 430, 1.05 + 0.03 * u, light_kit,
                     lambda CH, v: valera_k(CH, v, t, 'proud', dict(SIT, n=(6.4, 24.0)), key), post=lambda big, v: kit_fx(big, v, t))
    if n == 'radio': return radio(t, s, u)
    if n == 'salute':
        return scene(KIT, 930, 400, 1.0 + 0.04 * u, light_kit,
                     lambda CH, v: F.valera(CH, v.cam(*VK), dict(F.VPOSE['salute'], bn=1), t, mouth('valera', t), 'shout', 'home', hat='ushanka',
                                            hand_n=F.H(5.4, 24.2)),
                     post=lambda big, v: kit_fx(big, v, t))
    if n == 'kit_two': return kit_two(t, s, u)
    if n == 'kit_two_grand': return kit_two(t, s, u, grand=True)
    if n == 'doorbell': return r_doorbell(t, u)
    if n == 'nina_door': return r_nina_door(t, u, s)
    if n == 'nina_door_cu': return r_nina_door_cu(t, u, s)
    if n == 'v_hall': return r_v_hall(t, u, s)
    if n == 'nina_cu': return nina_cu(t, s, u)
    if n == 'nina_cu_angry': return nina_cu(t, s, u, shake=4)
    if n == 'nina_cu_soft': return nina_cu(t, s, u, cold=0.5, hand=F.H(3.0, 6.6))
    if n == 'nina_cu_plead': return nina_cu(t, s, u, cold=0.6, Zh=1.6, hand=F.H(3.4, 7.2))
    if n == 'yard': return r_yard(t, u)
    if n == 'pool_zina': return r_pool(t, u, 'zina')
    if n == 'pool_lyuba': return r_pool(t, u, 'lyuba')
    if n == 'nina_frost': return r_nina_frost(t, u)
    if n == 'summer_notice': return r_summer_notice(t, u)
    if n == 'summer_valera': return r_summer(t, u)
    if n == 's2_card':
        big = r_summer(t, u, card=True)
        ti = img('s2', lambda: O.winter_title(['СЕЗОН 2:', 'ЛЕТО'], 110, outline=(120, 40, 10), shadow=(60, 20, 6)))
        O.overlay(big, ti, 0, 250, min(1.0, u / 0.15))
        return big
    return scene(KIT, 640, 360, 0.6, light_kit)


HOOK = None
NOHUD = ('title', 'credits', 's2_card', 'summer_notice', 'summer_valera')
STICKERS = []


def stickers():
    if STICKERS: return STICKERS
    d = TL.first('doorbell'); nd = TL.first('nina_door'); y = TL.first('yard'); nf = TL.first('nina_frost'); vc = TL.first('v_cu')
    STICKERS.extend([(O.sticker('ДЗЫНЬ!', fg=(255, 236, 120), size=64), d['t0'] + 0.05, d['t1'], 1380, 300),
                     (O.sticker('ЖЭК?!', fg=(255, 130, 110), size=72), nd['t0'] + 0.2, nd['t1'], 1520, 220),
                     (O.sticker('-30°', fg=(170, 220, 255), size=64), nf['t0'] + 0.1, nf['t1'], 1500, 260),
                     (K.lcd_sticker('05:40', (255, 120, 90)), vc['t0'] + 0.2, vc['t1'], 1600, 230),
                     (O.sticker('ВСЁ ВКЛЮЧЕНО', fg=(150, 255, 214), size=56), y['t0'] + 0.5, y['t1'] + 0.01, 960, 200)])
    return STICKERS


def badge(text, size=34):
    from PIL import ImageFont
    font = ImageFont.truetype(P.FONT_BOLD, size)
    tw = int(ImageDraw.Draw(Image.new('L', (8, 8))).textlength(text, font=font))
    im = Image.new('RGBA', (tw + 40, int(size * 1.8)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, 0, tw + 36, int(size * 1.7)), 14, fill=(20, 12, 10, 130))
    d.text((18, int(size * 0.26)), text, font=font, fill=(255, 244, 214, 220))
    return np.array(im)


def hud(big, s):
    O.overlay(big, img('badge', lambda: badge('ВАЛЕРА И КОТ • ДЕМБЕЛЬСКИЙ АЛЬБОМ', 26)), 34, 30, 1.0)
    c = s['chap']
    if 1 <= c <= 6 and s['kind'] != 'card':
        p = img(('chap', c), lambda: badge(f'ГЛАВА {c}/6', 26))
        O.overlay(big, p, OUT_W - p.shape[1] - 34, 30, 1.0)


def render(t):
    global HOOK
    s = TL.shot_at(t)
    u = t - s['t0']
    big = shot_render(s, t)
    if s is TL.SHOTS[0]:
        HOOK = HOOK if HOOK is not None else O.winter_title(['ЖЭК В НАШЕЙ', 'ВАННОЙ?!'], 88, width=1180)
        if 0.08 <= t < s['t1']:
            k = min(1.0, (t - 0.08) / 0.1) * (1 - sm((t - (s['t1'] - 0.15)) / 0.15))
            O.overlay(big, HOOK, 0, 120, k)
    for im, t0, t1, cx, cy in stickers(): O.draw_sticker(big, im, t, t0, t1, cx, cy)
    if s['kind'] != 'clip' and s['name'] not in ('title', 'credits', 's2_card'):
        EPI.captions.draw(big, t, 940)
    if s['name'] not in NOHUD: hud(big, s)
    if s['name'] in ('doorbell',) and u < 0.15: O.flash(big, 0.8 * (1 - u / 0.15))
    if s['name'] in ('yard', 'summer_notice', 'title') and u < 0.3: O.mosaic(big, int(lerp(40, 1, u / 0.3)))
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
