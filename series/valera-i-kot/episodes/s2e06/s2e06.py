"""S02E06 «Плюс тридцать» — season finale: now the radiators roast, +32 at home, no regulator (the valve is sawn off). УК: «Меньше — не по
графику.» The whole block bakes: Гена in his window «Жарко?!», the grannies on the bench «Курорт!». «Двадцать лет в армии! Выход один!»
TWIST (season loop): he throws open THE ventilation pane from E01 — «По уставу.» The thermometer dives to +14, the cat «Батарея. Предатель.»,
УК: «Мужчина. У вас окно открыто.» Cat: «Записал.» Loop = the first frame of E01 «Плюс четырнадцать?! Дома?!» + «СЕЗОН 3: ДАЧА».
  python3 s2e06.py test 1 5 20 | frames t… | all [4] | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import View, view_at, Chars, Light, shadow, OUT_W, OUT_H
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as B
from props import panelka as PK
from props import vikit as K
from props import decals as D
from props import rusigns as R
from props import folkgena as G
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG,
              endcard=dict(style='winter', lang='ru', promise='СЕЗОН 3: ДАЧА — СКОРО'))
talk = EPI.talk
CUTS, NAMES = TL.CUTS + [TL.DUR], TL.NAMES                  # per-shot render: python3 s2e06.py shots <i|name>
W = PK.build()
KIT = W['kitchen']
ZHEK = PK.q(Image.open(PK.BG / 'zhek.png').convert('RGB'))
NX, NY, NU = 680.0, 412.0, 17.0                       # Nina in the office bathtub (S01 callback), facing left
DESK_PHONE = (70.0, 400.0)
LAMP_Z = (632.0, 30.0)
STAND = (905.0, 660.0, 16.5)                          # Valera standing by the table, facing left (window side)
VALVE_V = (868.0, 660.0, 16.5)                        # Valera bent over the radiator valve
SIT = (985.0, 722.0, 16.5)                            # Valera on the stool with the phone, facing right
PHONE_BASE = (1118.0, 512.0)
PANE = PK.WINDOW_OPEN                                 # (660, 80, 780, 160) open ventilation pane
THERMO = (446.0, 176.0)                               # room thermometer taped to the left window frame (world top-left)

# ---------------------------------------------------------------- local signs (S02: УК «Уют» instead of the ЖЭК)
INK, RED, BLUE, PAPER = (34, 30, 30), (176, 30, 34), (40, 60, 150), (240, 234, 214)
D.attach(ZHEK, [
    (R.plate(150, 40, ['УК «УЮТ»', 'ДИСПЕТЧЕРСКАЯ'], bg=(236, 240, 246), colors=[BLUE, INK], border=(60, 70, 120), weights=[1, 0.55],
             pad=3), 470, 70),
    (R.plate(96, 50, ['ОТОПЛЕНИЕ', 'ПО ГРАФИКУ'], bg=(250, 230, 120), colors=[INK, RED], border=INK, pad=2.5, tilt=-3), 980, 150),
])
D.attach(KIT, [
    (R.plate(64, 30, ['ЖЭК → УК', '«УЮТ»'], bg=PAPER, colors=[INK, BLUE], border=(120, 100, 70), pad=2, tilt=4), 1180, 300),
])
NOTEBOOK = R.plate(46, 20, ['ЖУРНАЛ', 'ЖАЛОБ'], bg=(70, 110, 170), colors=[(250, 240, 200), (250, 240, 200)], border=INK, pad=1.5)


def mouth(who, t, k=1.6):
    return min(1.0, talk(who, t) * k)


def begin(Z):
    ST.set_px(ST.px_for_zoom(Z))
    return Chars(), Chars()


def light_kit(v, warm=0.0):
    lx, ly = v.opt(*PK.LAMP_K)
    a = (lerp(0.9, 1.02, warm), lerp(0.97, 0.96, warm), lerp(1.12, 0.92, warm))
    return Light(amb=a, keys=[(lx, ly, 1100, (255, 196, 130), 0.75)], rim=(-1, -0.4, (186, 212, 255), 0.4), grad=(1.04, 0.9))


def light_zhek(v):
    lx, ly = v.opt(*LAMP_Z)
    tx, ty = v.opt(800.0, 380.0)
    return Light(amb=(0.98, 1.02, 0.98), keys=[(lx, ly, 1400, (230, 255, 236), 0.4), (tx, ty, 700, (255, 214, 160), 0.5)],
                 rim=(1, -0.3, (196, 220, 255), 0.3), grad=(1.05, 0.92))


# ---------------------------------------------------------------- props in the world
def thermo_img(val):
    """the room thermometer: white board, red column, big «+NN»"""
    sc = 4
    w, h = 28 * sc, 110 * sc
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, w - 1, h - 1], 8, fill=(244, 242, 232, 255), outline=INK + (255,), width=6)
    d.rectangle([w // 2 - 7, 10 * sc, w // 2 + 7, 86 * sc], fill=(210, 220, 230, 255), outline=INK + (255,), width=3)
    lvl = int(lerp(84, 14, min(1.0, max(0.0, (val - 0) / 40.0))) * sc)
    d.rectangle([w // 2 - 4, lvl, w // 2 + 4, 86 * sc], fill=(214, 30, 36, 255))
    d.ellipse([w // 2 - 14, 84 * sc, w // 2 + 14, 84 * sc + 28], fill=(214, 30, 36, 255), outline=INK + (255,), width=3)
    for k in range(0, 9):
        y = (14 + k * 8.5) * sc
        d.line([(w // 2 + 10, y), (w // 2 + 22, y)], fill=INK + (255,), width=3)
    txt = f'+{int(round(val))}'
    f = O.pfont(34)
    bb = f.getbbox(txt)
    d.rectangle([4, 96 * sc - 2, w - 5, h - 8], fill=(250, 250, 244, 255))
    d.text(((w - (bb[2] - bb[0])) // 2 - bb[0], 96 * sc + 4), txt, font=f, fill=(200, 20, 30, 255))
    return np.array(im)


_T = {}


def thermo(big, v, val):
    key = int(round(val))
    if key not in _T: _T[key] = thermo_img(key)
    D.blit(big, v, _T[key], THERMO[0], THERMO[1], ws=4)


def pane(big, v, k_open=1.0):
    """the ventilation pane: the background shows it open; k_open < 1 draws the sash swinging shut over the gap"""
    if k_open >= 0.999: return
    x0, y0, x1, y1 = PANE
    w = (x1 - x0) * (1 - k_open)
    if w * 4 < 60: return                                                    # sash still edge-on: nothing to draw
    im = Image.new('RGBA', (int((x1 - x0) * 4), int((y1 - y0) * 4)), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    W_, H_ = im.size
    xr = W_ - int(w * 4)
    d.rectangle([xr, 0, W_ - 1, H_ - 1], fill=(104, 88, 72, 255), outline=(40, 32, 28, 255), width=8)       # wooden sash
    d.rectangle([xr + 22, 22, W_ - 23, H_ - 23], fill=(30, 46, 78, 255), outline=(40, 32, 28, 255), width=4)  # dark glass
    gw = W_ - 23 - (xr + 22)
    for i in range(6):                                                                                # frost streaks on the glass
        y = 40 + i * 52
        d.line([(xr + 26, y), (xr + 26 + gw * 0.6, y - 30)], fill=(150, 180, 220, 255), width=5)
    for i in range(10):
        px = xr + 30 + (i * 37) % max(1, gw - 20); py = 30 + (i * 53) % (H_ - 70)
        d.rectangle([px, py, px + 6, py + 6], fill=(220, 236, 255, 255))
    d.rectangle([xr, 0, W_ - 1, 14], fill=(236, 232, 220, 255))                                        # peeling white paint
    D.blit(big, v, np.array(im), x0, y0, ws=4)


def drift(CH, v, k=1.0):
    """snowdrift on the sill under the open pane + icicles on the sash"""
    L = Layer(v.wcam())
    F.ell(L, (720, 377), 64 * k, 13 * k, (236, 244, 255), 0, (255, 255, 255), (190, 206, 230))
    F.ell(L, (690, 372), 34 * k, 12 * k, (236, 244, 255), 0, (255, 255, 255), (190, 206, 230))
    for i, x in enumerate((672, 694, 716, 742, 766)):
        F.cap(L, (x, 160), (x, 160 + (14 + (i % 2) * 12) * k), 2.4, 0.4, (210, 236, 255), (250, 255, 255), (160, 196, 230))
    F.outline(L); CH.add(L)


def handset_cord(CH, v, hand_world):
    L = Layer(v.wcam())
    x, y = PHONE_BASE
    F.ell(L, (x, y), 34, 16, (214, 200, 170), 0, (236, 226, 200), (176, 160, 130))
    F.ell(L, (x, y - 6), 14, 9, (80, 74, 70)); F.ell(L, (x, y - 6), 8, 5, (214, 200, 170))
    pts = [(x - 28, y + 4)]
    for i in range(1, 13):
        k = i / 12
        px = lerp(x - 28, hand_world[0], k); py = lerp(y + 4, hand_world[1], k) + 40 * math.sin(math.pi * k)
        pts.append((px + 3 * math.sin(i * 2.4), py + 3 * math.cos(i * 2.4)))
    for a, b in zip(pts, pts[1:]): F.cap(L, a, b, 1.4, 1.4, (190, 176, 146))
    F.outline(L); CH.add(L)


def breath(big, v, t, hx, hy, k=1.0):
    for i in range(3):
        ph = (t * 0.9 + i / 3) % 1.0
        ox, oy = v.opt(hx + 10 + 30 * ph, hy + 6 - 24 * ph)
        B.puff(big, ox, oy, (14 + 40 * ph) * 3 * v.Z * 0.5, 0.45 * (1 - ph) * k)


def kitchen(v, t, draw=None, warm=0.0, k_open=1.0, snow=46, cat_kw=None, therm=14.0, drift_k=1.0):
    CH, FX = begin(v.Z)
    big = v.bg()
    thermo(big, v, therm)
    pane(big, v, k_open)
    if drift_k > 0: drift(CH, v, drift_k)
    if cat_kw is not None:
        x, y = PK.CAT_K
        F.cat(CH, v.cam(x, y, PK.CAT_K_UNIT), t=t, pose='loaf', **cat_kw)
    if draw: draw(CH, v)
    CH.comp(big, light_kit(v, warm))
    if k_open > 0.5: B.snow_in(FX, v, t, PANE, n=snow, drift=(-90, 220))
    FX.comp(big)
    if warm > 0.2: B.haze(big, v, t, (PK.RAD[0], PK.RAD[1] - 80, PK.RAD[2], PK.RAD[1] + 10), amp=10 * warm)
    fx.vignette(big, 0.28)
    return big


def face_w(x, y, un, flip=False, fwd=1.4, h=21.0):
    return (x - fwd * un) if flip else (x + fwd * un), y - h * un


def v_cold(CH, v, t, pos, pose='stand', expr='angry', flip=True, hand_n=None, prop_n=None, hand_f=None, prop_f=None, **kw):
    x, y, un = pos
    kw.setdefault('cold', 0.55); kw.setdefault('hat', 'ushanka')
    F.valera(CH, v.cam(x, y, un, flip=flip), F.VPOSE[pose] if isinstance(pose, str) else pose, t, mouth('valera', t), expr, 'home',
             hand_n=hand_n, prop_n=prop_n, hand_f=hand_f, prop_f=prop_f, **kw)


# ---------------------------------------------------------------- shots
def r_hook(t, u, loop=False):
    """«Плюс четырнадцать?! Дома?!» — close-up: ushanka, icicles on the moustache, breath, the thermometer in his fist"""
    x, y, un = STAND
    fx_, fy_ = face_w(x, y, un, flip=True, h=20.6)
    v = view_at(KIT, fx_ - 6, fy_ + 60, 1.45 + 0.06 * u, 180, 330)
    shiver = 1.2 * math.sin(t * 40)

    def draw(CH, v_):
        v_cold(CH, v_, t, (x + shiver * 0.3, y, un), 'shiver', 'shout', cold=0.7)
    big = kitchen(v, t, draw)
    breath(big, v, t, fx_ - 30, fy_ + 10)
    img = img_thermo_big()
    O.overlay(big, img, 700 + int(6 * math.sin(t * 35)), 900 + int(5 * math.cos(t * 31)), 1.0)
    return big


_BIG = {}


def img_thermo_big():
    if 'th' not in _BIG:
        a = thermo_img(14)
        _BIG['th'] = np.array(Image.fromarray(a).resize((a.shape[1] * 3 // 2, a.shape[0] * 3 // 2), Image.NEAREST).rotate(-12, expand=True,
                                                                                                                    resample=Image.NEAREST))
    return _BIG['th']


def r_cat_cold(t, u):
    x, y = PK.CAT_K
    hx, hy = x + 4.4 * PK.CAT_K_UNIT, y - 6.9 * PK.CAT_K_UNIT
    v = view_at(KIT, hx, hy, 2.7 + 0.06 * u, 180, 300)
    big = kitchen(v, t, cat_kw=dict(mouth=mouth('cat', t, 2.0), lid=0.6, tail=0.2, tint=(0.86, 0.95, 1.18)))
    breath(big, v, t, hx - 24, hy + 6, 0.6)
    return big


def r_valve(t, u, puff=False):
    v = view_at(KIT, 790, 450, 1.05 + 0.04 * u, 180, 330)
    x, y, un = VALVE_V

    def draw(CH, v_):
        v_cold(CH, v_, t, VALVE_V, 'stand', 'sad' if puff else 'squint', lean=1.6,
               hand_n=(1000 + (x - 736) / un, 1000 - (y - 432) / un), prop_n=lambda L, h: B.screwdriver(L, h, ang=math.pi + 0.5))
    big = kitchen(v, t, draw, cat_kw=dict(lid=0.9, tail=0.1, tint=(0.86, 0.95, 1.18)))
    if puff:
        ox, oy = v.opt(*PK.VALVE)
        k = sm(u / 0.2) * (1 - sm((u - 0.25) / 0.2))
        B.puff(big, ox - 40, oy - 10, 90 * k + 10, 0.8 * k)
    return big


def r_puff(t, u): return r_valve(t, u + 3.0, puff=True)


def zhek_frame(v, t, expr='bored'):
    CH, FX = begin(v.Z)
    big = v.bg()
    hand = F.H(-0.1, 7.3)
    L = Layer(v.wcam())
    hw = (NX + 0.1 * NU, NY - 7.1 * NU)
    pts = [hw]
    for i in range(1, 25):
        k = i / 24
        px = lerp(hw[0], DESK_PHONE[0], k)
        py = lerp(hw[1], DESK_PHONE[1], k) + 190 * math.sin(math.pi * k) * (1 if k > 0.1 else k * 10)
        pts.append((px + 4 * math.sin(i * 2.2), py + 4 * math.cos(i * 2.2)))
    for a, b in zip(pts, pts[1:]): F.cap(L, a, b, 1.6, 1.6, (170, 36, 36))
    CH.add(L)
    F.nina(CH, v.cam(NX, NY, NU, flip=True), t, mouth('nina', t), expr, True, hand_n=hand, prop_n=lambda L_, h: F.handset(L_, h, -2.0))
    CH.comp(big, light_zhek(v))
    B.steam(big, v, t, 830, 395, -99, n=8, rise=190, size=40, a=0.45)
    fx.vignette(big, 0.3)
    return big


def r_nina(t, u, expr='bored', Z=2.6):
    x, y = NX - 1.9 * NU, NY - 10.2 * NU
    v = view_at(ZHEK, x - 10, y + 40, Z + 0.05 * u, 180, 300)
    return zhek_frame(v, t, expr)


def r_v_phone(t, u, expr='shout', Z=2.1, **kw):
    x, y, un = SIT
    fx_, fy_ = face_w(x, y, un, h=20.6)
    v = view_at(KIT, fx_ - 10, fy_ + 20, Z + 0.06 * u, 180, 320)

    def draw(CH, v_):
        handset_cord(CH, v_, (x + 0.2 * un, y - 18.0 * un))
        v_cold(CH, v_, t, SIT, dict(F.VPOSE['sit'], bn=-1), expr, flip=False, hand_n=F.H(0.2, 18.3),
               prop_n=lambda L, h: F.handset(L, h, -2.05, (214, 200, 170)), **kw)
    big = kitchen(v, t, draw)
    breath(big, v, t, fx_ + 20, fy_ + 10, 0.7)
    return big


def r_v_shout(t, u):
    """«Двадцать лет в армии!» — he jumps up, fist in the air; behind him the open pane keeps blowing snow (the clue)"""
    x, y, un = STAND
    v = view_at(KIT, 790, 420, 0.95 + 0.04 * u, 180, 330)

    def draw(CH, v_):
        v_cold(CH, v_, t, STAND, 'fist', 'shout', hand_f=F.H(0.2, 18.3), prop_f=lambda L, h: F.handset(L, h, -2.05, (214, 200, 170)))
    big = kitchen(v, t, draw, snow=80, cat_kw=dict(lid=0.9, tail=0.1, tint=(0.86, 0.95, 1.18)))
    if u < 0.3: B.shake(big, t, 8, 30)
    return big


def r_reveal(t, u):
    """TWIST: «Мужчина. У вас окно открыто.» — pull back and tilt up from Valera to the wide-open pane, a drift on the sill"""
    x, y, un = STAND
    fx_, fy_ = face_w(x, y, un, flip=True, h=20.6)
    k = sm(u / 1.4)
    cx, cy = lerp(fx_, 700, k), lerp(fy_, 230, k)
    Z = lerp(1.5, 1.0, k)
    v = view_at(KIT, cx, cy, Z, 180, lerp(320, 360, k))

    def draw(CH, v_):
        v_cold(CH, v_, t, STAND, 'phone', 'shock', hand_n=F.H(2.2, 20.6), prop_n=lambda L, h: F.handset(L, h, -2.05, (214, 200, 170)))
    big = kitchen(v, t, draw, snow=110, drift_k=1.2)
    if 0.05 < u < 0.7: fx.speed_lines(big, t, 0.45)
    return big


def r_v_proud(t, u):
    x, y, un = STAND
    fx_, fy_ = face_w(x, y, un, flip=True, h=20.6)
    v = view_at(KIT, fx_ - 10, fy_ + 70, 1.4 + 0.05 * u, 180, 330)

    def draw(CH, v_):
        v_cold(CH, v_, t, STAND, 'salute', 'proud')
    big = kitchen(v, t, draw)
    breath(big, v, t, fx_ - 30, fy_ + 10, 0.8)
    return big


def r_cat_dry(t, u):
    x, y = PK.CAT_K
    hx, hy = x + 4.4 * PK.CAT_K_UNIT, y - 6.9 * PK.CAT_K_UNIT
    v = view_at(KIT, hx, hy, 3.0 + 0.08 * u, 180, 300)
    return kitchen(v, t, cat_kw=dict(mouth=mouth('cat', t, 2.0), lid=0.62, tail=0.0, tint=(0.86, 0.95, 1.18)))


def r_slam(t, u):
    """the pane slams shut (Valera's arm), snow stops; the radiator gurgles"""
    v = view_at(KIT, 720, 200, 1.6, 180, 300)
    k = 1 - sm(u / 0.18)
    big = kitchen(v, t, k_open=k, drift_k=1.2)
    if u > 0.16: B.shake(big, t, 10, 40)
    return big


def r_cat_warm(t, u):
    """the radiator is hot: the cat melts on it, writes the complaint log; the two-choice question pops up"""
    x, y = PK.CAT_K
    hx, hy = x + 4.4 * PK.CAT_K_UNIT, y - 6.9 * PK.CAT_K_UNIT
    v = view_at(KIT, hx - 30, hy + 10, 2.3 + 0.05 * u, 180, 320)
    big = kitchen(v, t, warm=1.0, k_open=0.0, therm=lerp(14, 22, sm(u / 2.0)), drift_k=0.6,
                  cat_kw=dict(mouth=mouth('cat', t, 2.0), lid=0.9 if talk('cat', t) < 0.02 else 0.6, tail=1.0, expr='smug'))
    D.blit(big, v, NOTEBOOK, 552, 398, ws=4)
    return big


def r_reopen(t, u):
    """«Для здоровья!» — he throws the pane open again; the thermometer drops back"""
    v = view_at(KIT, 790, 420, 0.95, 180, 330)
    k = sm((u - 0.2) / 0.25)

    def draw(CH, v_):
        v_cold(CH, v_, t, STAND, 'overhead', 'proud', cold=0.2, hat=None)
    return kitchen(v, t, draw, k_open=k, therm=lerp(22, 14, sm((u - 0.6) / 1.2)), warm=1 - k,
                   cat_kw=dict(lid=0.3, tail=0.0, expr='shock'))


YARD = PK.q(Image.open(PK.BG / 'yard.png').convert('RGB'))
BENCH = PK.q(Image.open(PK.BG / 'bench.png').convert('RGB'))
NOREG = R.plate(60, 22, ['РЕГУЛИРОВКИ', 'НЕТ'], bg=(250, 230, 120), colors=[RED, INK], border=INK, pad=2)
D.attach(KIT, [(NOREG, 690, 446)])
G_WIN = (410.0, 136.0, 3.1)                           # Гена leaning out of the window above Valera's (yard facade)


def sweat(big, v, t, x, y, n=5):
    L = Layer(v.wcam())
    for i in range(n):
        ph = (t * 1.4 + i / n) % 1.0
        F.ell(L, (x + (i - n / 2) * 9, y + 40 * ph), 2.6, 3.6, (160, 210, 255), 0, (230, 246, 255), None)
    CH = Chars(); CH.add(L); CH.comp(big)


def fan(CH, v, t, x, y):
    """desk fan on the kitchen table, spinning"""
    L = Layer(v.wcam())
    F.cap(L, (x, y), (x, y - 40), 4, 4, (90, 96, 104))
    F.ell(L, (x, y + 2), 20, 6, (90, 96, 104))
    F.ell(L, (x, y - 62), 30, 30, (200, 206, 214), 0, (236, 240, 246), (150, 156, 166))
    for k in range(3):
        a = t * 30 + k * 2.094
        F.ell(L, (x + 14 * math.cos(a), y - 62 + 14 * math.sin(a)), 14, 6, (120, 170, 220), a)
    F.dot(L, (x, y - 62), (60, 64, 70), 4)
    F.outline(L); CH.add(L)


def r_hot(t, u):
    """«Плюс тридцать два?! Дома?!» — sweat streams, a fan in his face, the thermometer at +32, the pane shut tight"""
    x, y, un = STAND
    fx_, fy_ = face_w(x, y, un, flip=True, h=20.6)
    v = view_at(KIT, fx_ - 6, fy_ + 60, 1.45 + 0.06 * u, 180, 330)

    def draw(CH, v_):
        v_cold(CH, v_, t, STAND, 'shout', 'shout', cold=0.0, hat=None, tint=(1.12, 0.94, 0.9))
        fan(CH, v_, t, fx_ - 70, fy_ + 150)
    big = kitchen(v, t, draw, warm=1.0, k_open=0.0, therm=32, drift_k=0.0)
    sweat(big, v, t, fx_ - 6, fy_ - 30)
    O.overlay(big, img_thermo(32), 700 + int(6 * math.sin(t * 35)), 900, 1.0)
    return big


_TH = {}


def img_thermo(val):
    if val not in _TH:
        a = thermo_img(val)
        _TH[val] = np.array(Image.fromarray(a).resize((a.shape[1] * 3 // 2, a.shape[0] * 3 // 2), Image.NEAREST).rotate(-12, expand=True,
                                                                                                                 resample=Image.NEAREST))
    return _TH[val]


def r_cat_melt(t, u):
    """«Мечта. Сбылась. Слишком.» — the cat spread on the radiator like a pancake, slowly dripping off; РЕГУЛИРОВКИ НЕТ"""
    x, y = PK.CAT_K
    hx, hy = x + 4.4 * PK.CAT_K_UNIT, y - 6.9 * PK.CAT_K_UNIT
    v = view_at(KIT, hx + 20, hy + 20, 2.2 + 0.06 * u, 180, 300)
    big = kitchen(v, t, warm=1.0, k_open=0.0, therm=32, drift_k=0.0,
                  cat_kw=dict(mouth=mouth('cat', t, 2.0), lid=0.85, tail=1.0, expr='blissful'))
    return big


def r_gena(t, u):
    """«Жарко?!» — upstairs, Гена leans out of his open window in the hard hat, bare belly steaming"""
    x, y, un = G_WIN
    v = view_at(YARD, x + 10, y - 30, 3.2, 180, 330)
    CH, FX = begin(v.Z)
    big = v.bg()
    G.gena(CH, v.cam(x, y + 9.5 * un, un), G.GUITAR, t, mouth('gena', t), 'shout', hand_n=F.H(6.0, 20.0), hand_f=F.H(5.0, 18.0))
    PK.clip_below(CH, v, y + 2)
    CH.comp(big, Light(amb=(1.0, 0.95, 0.9), keys=[], rim=(-1, -0.4, (186, 212, 255), 0.4), grad=(1.0, 0.95)))
    B.steam(big, v, t, x + 6, y - 10, -99, n=8, rise=60, size=18, a=0.5)
    fx.vignette(big, 0.3)
    return big


def r_resort(t, u):
    """«Курорт!» — the grannies sunbathe on the bench in winter, the snow on the roof melting into drops"""
    v = view_at(BENCH, 800, 430, 1.35, 180, 330)
    CH, FX = begin(v.Z)
    big = v.bg()
    for who, (x, y, un) in (('zina', PK.B_ZINA), ('lyuba', PK.B_LYUBA)):
        F.babushka(CH, v.cam(x, y, un), t, who, 'sit', mouth(who, t), 'blissful', tint=(1.15, 1.0, 0.92))
    lx, ly = v.opt(845.0, 160.0)
    CH.comp(big, Light(amb=(1.05, 1.0, 0.95), keys=[(lx, ly, 1200, (255, 210, 140), 0.7)], rim=(-1, -0.4, (186, 212, 255), 0.3),
                       grad=(1.04, 0.92)))
    B.haze(big, v, t, (600, 300, 1100, 640), amp=8)
    fx.vignette(big, 0.28)
    return big


def r_exit(t, u):
    """«Двадцать лет в армии! Выход один!» — he marches to the window like to an assault"""
    v = view_at(KIT, 790, 420, 0.95 + 0.04 * u, 180, 330)

    def draw(CH, v_):
        v_cold(CH, v_, t, STAND, 'fist', 'proud', cold=0.0, hat=None, tint=(1.1, 0.95, 0.9))
    big = kitchen(v, t, draw, warm=1.0, k_open=0.0, therm=32, drift_k=0.0, cat_kw=dict(lid=0.9, tail=1.0, expr='blissful'))
    sweat(big, v, t, 870, 300)
    return big


def r_window(t, u):
    """TWIST: he throws open THE pane from E01 — icy wind, snow bursts in; «По уставу.» blissful; flash + «ВЕНТИЛЯЦИЯ!»"""
    v = view_at(KIT, 820, 320, 1.05 + 0.05 * u, 180, 330)
    k = sm(u / 0.3)

    def draw(CH, v_):
        v_cold(CH, v_, t, STAND, 'overhead', 'blissful' if u > 0.4 else 'proud', cold=0.0, hat=None)
    big = kitchen(v, t, draw, warm=1 - k, k_open=k, therm=32, snow=120, drift_k=0.0)
    if u < 0.5: fx.speed_lines(big, t, 0.5)
    return big


def r_cat_cold2(t, u):
    """«Батарея. Предатель.» — the thermometer dives 32 → 14, the cat goes blue again on the cooling radiator"""
    x, y = PK.CAT_K
    hx, hy = x + 4.4 * PK.CAT_K_UNIT, y - 6.9 * PK.CAT_K_UNIT
    v = view_at(KIT, hx - 40, hy - 30, 1.9 + 0.05 * u, 180, 300)
    th = lerp(32, 14, sm(u / 1.2))
    big = kitchen(v, t, therm=th, cat_kw=dict(mouth=mouth('cat', t, 2.0), lid=0.6, tail=0.2, tint=(0.86, 0.95, 1.18)))
    return big


def r_cat_log(t, u):
    x, y = PK.CAT_K
    hx, hy = x + 4.4 * PK.CAT_K_UNIT, y - 6.9 * PK.CAT_K_UNIT
    v = view_at(KIT, hx - 30, hy + 10, 2.3 + 0.05 * u, 180, 320)
    big = kitchen(v, t, therm=14, cat_kw=dict(mouth=mouth('cat', t, 2.0), lid=0.6, tail=0.2, tint=(0.86, 0.95, 1.18)))
    D.blit(big, v, NOTEBOOK, 552, 398, ws=4)
    return big


SHOT = dict(hook=r_hot, cat_melt=r_cat_melt, nina1=lambda t, u: r_nina(t, u, 'bored', 1.7),
            v_phone=lambda t, u: r_v_phone(t, u, 'shout', 1.5, cold=0.0, hat=None, tint=(1.12, 0.94, 0.9)), nina2=lambda t, u: r_nina(t, u, 'smug', 1.95), gena=r_gena,
            resort=r_resort, v_exit=r_exit, window=r_window, cat_cold=r_cat_cold2, v_cold=lambda t, u: r_v_phone(t, u, 'shiver', 1.6),
            nina3=lambda t, u: r_nina(t, u, 'smug', 1.8), cat_log=r_cat_log, loop=lambda t, u: r_hook(t, u, True))


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


F0 = TL.T0
SHOW = K.Show(EPI, 6, ['+32 ДОМА?!'], hook_t=(0.06, 2.5), hook_y=150,
              stickers=[(O.sticker('РЕГУЛИРОВКИ НЕТ', fg=(255, 120, 110), size=58), F0['cat_melt'] + 0.3, F0['nina1'], 540, 330),
                        (O.sticker('ВЕНТИЛЯЦИЯ!', fg=(150, 220, 255), size=80), TL.TWIST + 0.3, F0['cat_cold'], 540, 1180),
                        (O.sticker('+14', fg=(150, 220, 255), size=80), F0['cat_cold'] + 1.2, F0['v_cold'], 860, 420),
                        (O.sticker('СЕЗОН 3: ДАЧА', fg=(255, 236, 120), size=70), F0['loop'] + 0.6, TL.DUR + 1, 540, 1280)],
              flashes=[TL.TWIST + 0.25, F0['loop']], mosaics=[F0['nina1'], F0['gena'], F0['nina3']],
              cap_y={'hook': 1500, 'window': 1500, 'v_exit': 1500, 'loop': 1500, 'cat_log': 1240}, cap_default=1330)
SHOW.badge = O.make_badge('СЕЗОН 2 • СЕРИЯ 6/6')


def question():
    if 'q' not in _BIG:
        a = O.sticker('ДОМА СЕЙЧАС:', fg=(255, 236, 120), size=58)
        b = O.sticker('+14 / +32', fg=(255, 255, 255), size=64)
        w = max(a.shape[1], b.shape[1])
        out = np.zeros((a.shape[0] + b.shape[0] + 8, w, 4), np.uint8)
        out[:a.shape[0], (w - a.shape[1]) // 2:(w - a.shape[1]) // 2 + a.shape[1]] = a
        out[a.shape[0] + 8:, (w - b.shape[1]) // 2:(w - b.shape[1]) // 2 + b.shape[1]] = b
        _BIG['q'] = out
    return _BIG['q']


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    q0 = F0['cat_log'] + 1.6
    if q0 <= t < F0['loop'] + 0.2:
        O.draw_sticker(big, question(), t, q0, F0['loop'] + 0.2, 540, 1600)
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
