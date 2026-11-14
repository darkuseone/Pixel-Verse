"""S01E06 «РАСТАЯЛО!» — the season finale (42.0 s, twist at 21.35 s / 51 %, type: «успех хуже провала» — the snow melted, now the yard is a
lake). Main question: will Жора finally walk to work through the door like a human being?
HOOK: the seagull CU on the dripping sill: «Дальний Восток. Весна. Снег, который копили полгода, растаял за одну ночь.» — the cutaway: the
snow mass sinks floor by floor in one night. Жора at the kitchen window, spring outside: «Ира! Растаяло! Всё, теперь на работу — как
человек, через дверь!» — «Жора, лифт не работает. Девятый этаж.» — «Да хоть двадцатый! Я полгода в окно лазил — уж по лестнице-то
сбегаю!» The stairs: «Девятый, пятый, первый! Ну, здравствуй, свобода!» TWIST: he steps out of the door — splash, the whole yard is a lake,
he stands waist-deep: «Это что такое?» Витёк in a rubber boat: «Такси «Лодка», тариф «Эконом»! Город маленький!» — «Ну и сколько до
работы?» — «Три тысячи. Но гребёшь — сам.» Ира with the phone: «Жора! УК пишет: лужу уберут зимой. Замёрзнет — сама.» — «Ничего! Мы,
дальневосточники, — непотопляемые!» The pilot's parcel floats by with the gull on it: «Плаваем.» The sign: «ДО ЗИМЫ: 183 ДНЯ».
  python3 ep06.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import fx
import overlays as O
import stage as ST
import paths as P
from scene import lerp
from cam25 import glide, kick
from episode import Episode
from props import zamcast as C
from props import zamkit as K
from props import zampix as ZX
from props import mimic as M
from props import rusigns as R
from props import decals as D
from props.dibspix import blit
from props.zamkit import A
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

K.DAY = 0
EPI = Episode('ep06', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='zamelo', lang='ru'), promo='ru')
TAB = (C.XTRA, C.EXPR)
FZ = M.Face([(0.0, 'cheerful'), (12.2, 'cocky'), (16.3, 'exhausted'), (18.85, 'proud'), (21.35, 'shock'), (24.1, 'stunned'),
             (27.85, 'nervous'), (31.7, 'gloomy'), (36.15, 'proud')], TAB, seed=3)
FC = M.Face([(0.0, 'dry')], TAB, seed=8)
FV = M.Face([(0.0, 'cheerful')], TAB, seed=11)
FI = M.Face([(0.0, 'dry')], TAB, seed=13)
WH = (255, 255, 255)
KWIN = (892.0, 40.0, 1215.0, 395.0)                # the kitchen window glass (world px)
LWIN = (55.0, 55.0, 300.0, 375.0)                  # the landing window (world px)
DOOR = (140.0, 200.0, 295.0, 530.0)                # the entrance door opening in the flood world
WL = 612.0                                         # the near water surface in the flood world (world y)
_SPR = {}


def mouth(who, t):
    return M.mouth(EPI.talk, who, t)


def face(F, who, t, base=(0.7, 0.0), **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), **kw), M.bob(t, m)


def hat_post(sp):
    if 'head' in sp.anchors: C.ushanka_vitek(sp, sp.anchors['head'])


def glow(big, cx, cy, r, col, a):
    H_, W_ = big.shape[:2]
    y0, y1, x0, x1 = max(0, int(cy - 2 * r)), min(H_, int(cy + 2 * r)), max(0, int(cx - 2 * r)), min(W_, int(cx + 2 * r))
    if y0 >= y1 or x0 >= x1: return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * (r * 0.6) ** 2))[..., None]
    reg = big[y0:y1, x0:x1].astype(np.float32)
    big[y0:y1, x0:x1] = np.clip(reg * (1 + a * 1.6 * g) + np.array(col, np.float32) * a * 0.5 * g, 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- spring outside the windows (paste the flood world into the glass)
def _flood_png():
    if 'f' not in _SPR: _SPR['f'] = np.array(Image.open(P.series(SLUG) / 'bg' / 'flood.png').convert('RGB'))
    return _SPR['f']


def spring_glass(big, v, rect, src=(420, 120, 1250, 620)):
    """replace the snowy view in a window (bluish / bright pixels inside the world rect) with the spring flood view"""
    x0, y0, x1, y1 = rect
    ax, ay = v.opt(x0, y0); bx, by = v.opt(x1, y1)
    cx0, cy0 = int(max(0, ax)), int(max(0, ay)); cx1, cy1 = int(min(big.shape[1], bx)), int(min(big.shape[0], by))
    if cx0 >= cx1 or cy0 >= cy1: return
    fw = _flood_png()[src[1]:src[3], src[0]:src[2]]
    full = np.array(Image.fromarray(fw).resize((max(1, int(bx - ax)), max(1, int(by - ay))), Image.NEAREST))
    sub = full[cy0 - int(ay):cy1 - int(ay), cx0 - int(ax):cx1 - int(ax)]
    reg = big[cy0:cy1, cx0:cx1]
    hh, ww = min(sub.shape[0], reg.shape[0]), min(sub.shape[1], reg.shape[1])
    reg, sub = reg[:hh, :ww], sub[:hh, :ww]
    r = reg.astype(np.int32)
    m = (r[..., 2] > r[..., 0] + 8) | (r.sum(-1) > 560)
    reg[m] = sub[m]


# ---------------------------------------------------------------- water in front of the heroes (the flood world)
def water_front(big, v, t, wl=WL, a=0.55):
    """a semi-transparent near water layer below the water line + moving ripple highlights: heroes stand in the water"""
    H_, W_ = big.shape[:2]
    y0 = int(v.opt(0, wl)[1])
    if y0 >= H_: return
    y0 = max(0, y0)
    reg = big[y0:].astype(np.float32)
    reg = reg * (1 - a) + np.array((40, 128, 178), np.float32) * a
    big[y0:] = np.clip(reg, 0, 255).astype(np.uint8)
    px = max(4, int(2 * v.Z))
    for q in range(14):
        yy = y0 + 10 + int(q * q * 9 * v.Z * 0.18 + (t * 18 * v.Z) % 14)
        if yy >= H_ - px: break
        for k in range(6):
            xx = int((q * 197 + k * 263 + t * 40 * (1 + q % 3)) % (W_ + 200)) - 100
            big[yy:yy + px, max(0, xx):max(0, xx + int(60 * v.Z))] = (190, 232, 250)
    big[y0:y0 + px] = (210, 240, 255)                                          # the surface line


def ripple(big, v, x, y, t, t0=None):
    """rings on the water around a hero at (world) x, y"""
    ox, oy = v.opt(x, y)
    for q in range(3):
        u = ((t * 0.9 + q / 3.0) % 1.0)
        rx, ry = (40 + 160 * u) * v.Z, (8 + 30 * u) * v.Z
        a = 1 - u
        th = np.linspace(0, 2 * np.pi, 120)
        for th_ in th:
            px_, py_ = int(ox + math.cos(th_) * rx), int(oy + math.sin(th_) * ry)
            if 0 <= py_ < big.shape[0] - 3 and 0 <= px_ < big.shape[1] - 3 and math.sin(th_) > -0.2:
                big[py_:py_ + 3, px_:px_ + 4] = np.clip(big[py_:py_ + 3, px_:px_ + 4] * (1 - a * 0.6) + np.array((230, 248, 255)) * a * 0.6, 0, 255)


def splash(big, v, x, y, t, t0, n=30, seed=4):
    ox, oy = v.opt(x, y)
    K.puff(big, ox, oy, t, t0, n=n, col=(170, 220, 250), seed=seed, life=0.7, speed=700, px=int(6 * v.Z) + 4)
    K.puff(big, ox, oy, t, t0 + 0.05, n=n // 2, col=(240, 250, 255), seed=seed + 1, life=0.6, speed=520, px=int(4 * v.Z) + 4)


# ---------------------------------------------------------------- props: the rubber boat, the pilot's parcel
def boat(sp, t=0.0, oars=True, row=0.0):
    """an old olive rubber boat «Уфимка» side view facing +x, ~2.6 m (draw at ~1.0 hero scale): two fat tubes, an upturned bow,
    a plywood seat, rowlocks with two oars (row = phase), the cardboard «ТАКСИ «ЛОДКА»» sign taped to the side"""
    OL = (96, 112, 66)
    sp.sup(0.0, 2.0, 46.0, 4.0, C.tones((60, 70, 44)), n=4.0)                                 # the floor (under)
    sp.sup(-2.0, 9.0, 46.0, 7.0, C.tones(OL), n=6.0)                                         # the tube
    sp.ell(44.0, 13.0, 8.0, 7.6, C.tones(OL))                                                # the upturned bow
    sp.ell(-46.0, 10.0, 6.4, 7.0, C.tones(OL))
    for x in (-30.0, -10.0, 10.0, 30.0): C.thin(sp, (x, 3.0), (x, 15.0), C.dark(OL, 0.7), 0.4)  # the seams
    C.thin(sp, (-44.0, 14.2), (44.0, 15.6), C.mix(OL, (255, 255, 255), 0.35), 0.5)            # the shine
    for q in range(5): sp.blob(-36.0 + q * 18.0, 12.0, 0.7, (40, 40, 40))                    # the rope loops
    sp.txt_box(['ТАКСИ «ЛОДКА»'], (-30.0, 4.0, 18.0, 13.0), (250, 244, 220), pad=0.4)
    if oars:
        a = 0.5 * math.sin(row)
        for dx in (0.0, 5.0):
            x0, y0 = -6.0 + dx, 15.0
            x1, y1 = x0 + 36.0 * math.cos(-0.6 + a), y0 + 36.0 * math.sin(-0.6 + a)
            C.thin(sp, (x0 - 10 * math.cos(-0.6 + a), y0 - 10 * math.sin(-0.6 + a)), (x1, y1), (170, 120, 70), 0.9)
            sp.sup(x1 + 3.0 * math.cos(-0.6 + a), y1 + 3.0 * math.sin(-0.6 + a), 4.0, 1.6, C.tones((200, 60, 50)), n=3.0)
    sp.anchors.update(seat=(-6.0, 14.0))


def parcel_box(sp, t=0.0):
    """the pilot's parcel: a wet cardboard box with the courier tape and «ЖОРА» in marker"""
    sp.sup(0.0, 8.0, 14.0, 8.0, C.tones((176, 128, 80)), n=6.0)
    C.thin(sp, (-14.0, 10.0), (14.0, 10.0), (130, 80, 200), 1.2)
    sp.txt_box(['ЖОРА'], (-11.0, 1.4, 11.0, 7.0), (176, 128, 80), pad=0.2)


# ================================================================== 0: «Дальний Восток. Весна.» — the gull on the dripping sill
def r_gull(t, u):
    Z = 2.8 * (1 + 0.025 * u)
    cx, cy = 840.0, 470.0
    v = K.V('facade', cx, cy, Z)
    kw, dy = face(FC, 'chayka', t, (0.0, 0.0))
    g = A(C.chayka, 850.0, 500.0 + dy * 0.3, K.WS['facade'] * 3 * v.Z * 0.6, t=t, flip=True, **kw); g.near = 0.62
    def f(big, _):
        for q in range(7):                                                        # drops from the icicles
            x = 80 + q * 150 + (q % 2) * 40
            ph = (t * 1.3 + q * 0.37) % 1.0
            y = int(-20 + ph * 2000)
            big[max(0, y):y + 22, x:x + 10] = (190, 226, 255)
    return K.shot('facade', K.light_morning, cx, cy, Z, acts=[g], fx_=f, focus=0.62, dof_k=30, t=t, snow=False, kick=kick(t, [(0.12, 0.8)]))


# ================================================================== 1: the cutaway: the snow mass sinks floor by floor in one night
def r_melt(t, u):
    L = CUTS[2] - CUTS[1]
    Z = 0.5
    cx, cy = 360.0, 640.0
    v = K.V('cutaway', cx, cy, Z)
    k = glide(min(1.0, u / (L - 0.3)))
    lev = lerp(K.SNOW_TOP, 1170.0, k)                                           # the snow top (world y)
    def pre(big, _v):
        src = big.copy()
        H_, W_ = big.shape[:2]
        x0 = int(max(0, v.opt(360.0, 0)[0]))
        top_o = v.opt(0, K.SNOW_TOP)[1]; bot_o = v.opt(0, 1280.0)[1]; lev_o = v.opt(0, lev)[1]
        sky = np.array(src[int(max(0, v.opt(0, 40)[1])), x0:], np.float32)
        for y in range(H_):
            if y < top_o: continue
            if y < lev_o:                                                        # spring sky + the city far away
                q = (y - top_o) / max(1.0, lev_o - top_o)
                big[y, x0:] = np.clip(np.array((150, 196, 246)) * (1 - 0.3 * q) + np.array((210, 230, 250)) * 0.3 * q, 0, 255)
            else:                                                                 # the snow mass squashed into [lev, bottom]
                ys = top_o + (y - lev_o) * (bot_o - top_o) / max(1.0, bot_o - lev_o)
                big[y, x0:] = src[int(min(H_ - 1, max(0, ys))), x0:]
        if k > 0.6:                                                              # the meltwater lake at the bottom
            wy = int(v.opt(0, lerp(1280.0, 1185.0, (k - 0.6) / 0.4))[1])
            big[wy:, :] = (np.array(big[wy:, :], np.float32) * 0.35 + np.array((60, 150, 200)) * 0.65).astype(np.uint8)
        ly = int(lev_o)                                                          # the wet crust line
        big[max(0, ly - 3):ly + 3, x0:] = (236, 246, 255)
    def f(big, _):
        O.draw_sticker(big, ST_NIGHT, t, CUTS[1] + 0.2, CUTS[2], 760, 360)
    return K.shot('cutaway', K.light_cut, cx, cy, Z, pre=pre, fx_=f, t=t, focus=0.5, dof_k=0, snow=False, bloom=(240, 14, 0.25))


ST_NIGHT = K.st('ЗА 1 НОЧЬ', fg=(120, 230, 255), size=64)


# ================================================================== 2: Жора at the kitchen window, spring outside: «Ира! Растаяло!»
def kitchen_pre(v):
    def pre(big, _v): spring_glass(big, v, KWIN)
    return pre


def light_spring(v):
    return ST.Light(amb=(1.02, 1.02, 1.04), keys=[(*v.opt(1050, 220), 700 * v.Z, (255, 250, 230), 0.30)], grad=(1.02, 0.98))


def r_joy(t, u):
    L = CUTS[3] - CUTS[2]
    Z = lerp(1.15, 1.3, glide(u / L))
    cx, cy = 900.0, 420.0
    v = K.V('kitchen', cx, cy, Z)
    S = K.S_of(v, 'kitchen')
    kz, dz = face(FZ, 'zhora', t, (-0.9, -0.2) if u > 0.8 else (0.9, -0.3), hand_n=(22.0, 70.0 + 4 * math.sin(t * 8)),
                  hand_f=(-20.0, 68.0 + 4 * math.cos(t * 8)))
    z = A(C.zhora, 960.0, 712.0 + dz, S, t=t, flip=u > 0.8, **kz); z.near = 0.99
    return K.shot('kitchen', lambda _v: light_spring(v), cx, cy, Z, acts=[z], pre=kitchen_pre(v), focus=0.9, dof_k=8, t=t, snow=False,
                  rays=None, kick=kick(t, [(CUTS[2] + 1.1, 0.7)]))


# ================================================================== 3: Ира, dry: «Жора, лифт не работает. Девятый этаж.»
def r_ira(t, u):
    Z = 1.9
    cx, cy = 640.0, 520.0
    v = K.V('kitchen', cx, cy, Z)
    S = K.S_of(v, 'kitchen')
    ki, di = face(FI, 'ira', t, (0.6, 0.0), hand_n=(16.0, 48.0))
    ira = A(C.ira, 640.0, 712.0 + di, S, t=t, **ki); ira.near = 0.99
    return K.shot('kitchen', lambda _v: light_spring(v), cx, cy, Z, acts=[ira], pre=kitchen_pre(v), focus=0.9, dof_k=16, t=t, snow=False)


# ================================================================== 4: the landing: Жора bursts out of the flat: «Да хоть двадцатый!…»
def landing_pre(v, floor=None):
    def pre(big, _v):
        spring_glass(big, v, LWIN, src=(450, 60, 1200, 520))
        if floor:
            p = R.plate(70, 80, [str(floor), 'ЭТАЖ'], bg=(40, 90, 170), fg=WH, border=WH, weights=[3, 1], round_=4)
            s = 3 * v.Z / D.WS
            im = np.array(Image.fromarray(p).resize((max(1, int(p.shape[1] * s)), max(1, int(p.shape[0] * s))), Image.LANCZOS))
            ox, oy = v.opt(395.0, 215.0)
            O.overlay(big, im, int(ox), int(oy), 1.0)
    return pre


def r_run(t, u):
    L = CUTS[5] - CUTS[4]
    Z = 0.95
    cx, cy = 600.0, 400.0
    v = K.V('landing', cx, cy, Z)
    S = K.S_of(v, 'landing') * 0.85
    x = 650.0 if u < 0.9 else lerp(650.0, 330.0, glide(min(1.0, (u - 0.9) / (L - 1.2))))
    kz, dz = face(FZ, 'zhora', t, (-0.9, 0.0), walk=(t * 10.0 if u > 0.9 else None), lean=0.6 if u > 0.9 else 0.0,
                  hand_n=(20.0, 50.0), hand_f=(-14.0, 46.0))
    z = A(C.zhora, x, 640.0 + dz, S, t=t, flip=True, **kz); z.near = 0.99
    return K.shot('landing', K.light_landing, cx, cy, Z, acts=[z], pre=landing_pre(v), focus=0.9, dof_k=6, t=t, snow=False)


# ================================================================== 5-7: the stairs montage: 9 -> 5 -> 1 (each a new angle)
def stairs(t, u, floor, Z, cx, x0, x1, sweat):
    L = 0.85
    v = K.V('landing', cx, 400.0, Z)
    S = K.S_of(v, 'landing') * 0.85
    x = lerp(x0, x1, min(1.0, u / L))
    kz, dz = face(FZ, 'zhora', t, (-0.9 if x1 < x0 else 0.9, 0.0), walk=t * 13.0, lean=1.0, sweat=sweat, hand_n=(20.0, 52.0),
                  hand_f=(-14.0, 48.0))
    z = A(C.zhora, x, 640.0 + dz, S, t=t, flip=x1 < x0, **kz); z.near = 0.99
    def f(big, _): fx.speed_lines(big, t, 0.25)
    return K.shot('landing', K.light_landing, cx, 400.0, Z, acts=[z], pre=landing_pre(v, floor), fx_=f, focus=0.9, dof_k=6, t=t, snow=False,
                  kick=kick(t, [(t - u + 0.02, 0.8)]))


def r_f9(t, u): return stairs(t, u, 9, 1.05, 520.0, 780.0, 300.0, 0.3)
def r_f5(t, u): return stairs(t, u, 5, 1.25, 520.0, 300.0, 760.0, 0.8)
def r_f1(t, u): return stairs(t, u, 1, 1.05, 520.0, 780.0, 300.0, 1.0)


# ================================================================== 8: CU Жора in the doorway, arms up: «Ну, здравствуй, свобода!» (no water seen)
def r_door(t, u):
    Z = 2.3
    cx, cy = 222.0, 352.0
    v = K.V('flood', cx, cy, Z)
    S = K.S_of(v, 'flood')
    kz, dz = face(FZ, 'zhora', t, (0.0, -0.3), hand_n=(22.0, 84.0), hand_f=(-20.0, 84.0), sweat=0.6)
    z = A(C.zhora, 220.0, 530.0 + dz, S, t=t, **kz); z.near = 0.99
    return K.shot('flood', K.light_morning, cx, cy, Z, acts=[z], focus=0.9, dof_k=10, t=t, snow=False)


# ================================================================== 9: TWIST — the step down: splash, the yard is a lake; «Это что такое?»
def r_twist(t, u):
    L = CUTS[10] - CUTS[9]
    Z = lerp(0.95, 1.15, glide(min(1.0, u / L)))
    cx, cy = lerp(480.0, 450.0, glide(min(1.0, u / L))), 420.0
    v = K.V('flood', cx, cy, Z)
    S = K.S_of(v, 'flood')
    dropk = glide(min(1.0, u / 0.25))
    kz, dz = face(FZ, 'zhora', t, (0.9, -0.2), hand_n=(26.0, 56.0), hand_f=(-22.0, 56.0))
    z = A(C.zhora, lerp(230.0, 440.0, dropk), lerp(530.0, 735.0, dropk) + dz, S, t=t, **kz); z.near = 0.99
    def f(big, _):
        water_front(big, v, t)
        ripple(big, v, 440.0, WL, t)
        splash(big, v, 440.0, WL, t, TWIST + 0.15)
    return K.shot('flood', K.light_morning, cx, cy, Z, acts=[z], fx_=f, focus=0.8, dof_k=6, t=t, snow=False, kick=kick(t, [(TWIST + 0.15, 1.4)]))


# ================================================================== 10: Витёк rows in: «Такси «Лодка», тариф «Эконом»! Город маленький!»
def boat_acts(t, v, x, y, S, talk=True, base=(-0.8, 0.0)):
    k = S / (3 * v.Z)
    kv, dv = face(FV, 'vitek', t, base, hand_n=(18.0, 46.0 + 4 * math.sin(t * 5)))
    vk = A(C.vitek, x - 4 * k, y + 2 * k + dv, S, t=t, post=hat_post, **kv); vk.near = 0.99
    def bt(sp, t=0.0): boat(sp, t, row=t * 5)
    b = A(bt, x, y + 2 * k * math.sin(t * 2.2), S * 1.0, t=t, flip=True); b.near = 0.99
    return [vk, b]


def r_boat(t, u):
    L = CUTS[11] - CUTS[10]
    Z = 1.0
    cx, cy = 565.0, 420.0
    v = K.V('flood', cx, cy, Z)
    S = K.S_of(v, 'flood')
    x = lerp(940.0, 655.0, glide(min(1.0, u / 1.8)))
    kz, dz = face(FZ, 'zhora', t, (0.9, 0.0), hand_n=(24.0, 56.0), hand_f=(-22.0, 54.0))
    z = A(C.zhora, 470.0, 735.0 + dz, S, t=t, **kz); z.near = 0.99
    def f(big, _):
        water_front(big, v, t)
        ripple(big, v, 470.0, WL, t)
        ripple(big, v, x, WL + 4, t * 1.3)
    return K.shot('flood', K.light_morning, cx, cy, Z, acts=[z] + boat_acts(t, v, x, WL - 6, S), fx_=f, focus=0.8, dof_k=6, t=t,
                  snow=False)


# ================================================================== 11: CU Жора waist-deep: «Ну и сколько до работы?»
def r_much(t, u):
    Z = 2.0
    cx, cy = 360.0, 470.0
    v = K.V('flood', cx, cy, Z)
    S = K.S_of(v, 'flood')
    kz, dz = face(FZ, 'zhora', t, (0.9, 0.0), hand_n=(24.0, 56.0), hand_f=(-22.0, 54.0))
    z = A(C.zhora, 360.0, 735.0 + dz, S, t=t, **kz); z.near = 0.99
    def f(big, _):
        water_front(big, v, t)
        ripple(big, v, 360.0, WL, t)
    return K.shot('flood', K.light_morning, cx, cy, Z, acts=[z], fx_=f, focus=0.8, dof_k=14, t=t, snow=False)


# ================================================================== 12: CU Витёк in the boat holds out the oars: «Три тысячи. Но гребёшь — сам.»
def r_row(t, u):
    Z = 1.9
    cx, cy = 640.0, 480.0
    v = K.V('flood', cx, cy, Z)
    S = K.S_of(v, 'flood')
    def f(big, _):
        water_front(big, v, t, a=0.35)
        if u > 1.0: O.draw_sticker(big, ST_3000, t, CUTS[12] + 1.0, CUTS[13], 760, 520)
    return K.shot('flood', K.light_morning, cx, cy, Z, acts=boat_acts(t, v, 640.0, WL - 6, S, base=(-0.9, 0.0)), fx_=f, focus=0.8,
                  dof_k=14, t=t, snow=False)


ST_3000 = K.st('3000 ₽', fg=(255, 214, 80), size=70)


# ================================================================== 13: Ира with the phone: «Жора! УК пишет: лужу уберут зимой. Замёрзнет — сама.»
def sms_screen(t, t_up=0.0, w=520, h=860):
    S = 4
    im, d, wl, hl = K._phone(w, h, S)
    k = min(1.0, max(0.0, (t - t_up) / 0.2))
    d.rectangle([6, 14, wl - 7, 40], fill=(40, 90, 200, 255))
    K._fit_text(d, 6, wl - 7, 21, 'УК СУГРОБ-СЕРВИС', 9, WH)
    if k > 0:
        d.rounded_rectangle([12, 56, wl - 13, 170], 6, fill=(236, 236, 244, 255))
        K._fit_text(d, 16, wl - 17, 66, 'ЛУЖУ УБЕРЁМ', 10, (30, 30, 40))
        K._fit_text(d, 16, wl - 17, 88, 'ЗИМОЙ.', 10, (30, 30, 40))
        K._fit_text(d, 16, wl - 17, 116, 'ЗАМЁРЗНЕТ —', 8, (220, 40, 40))
        K._fit_text(d, 16, wl - 17, 136, 'САМА.', 10, (220, 40, 40))
    return np.array(im.resize((wl * S, hl * S), Image.NEAREST))


def r_ira2(t, u):
    Z = 1.7
    cx, cy = 700.0, 420.0
    v = K.V('kitchen', cx, cy, Z)
    S = K.S_of(v, 'kitchen')
    ki, di = face(FI, 'ira', t, (-0.6, 0.0), hand_n=(16.0, 56.0), prop_n=C.phone)
    ira = A(C.ira, 600.0, 712.0 + di, S, t=t, **ki); ira.near = 0.99
    def f(big, _):
        if u > 0.6:
            ph = sms_screen(t, t_up=CUTS[13] + 0.7, w=430, h=700)
            O.overlay(big, ph, 600, 560 + int(6 * math.sin(t * 3)), 1.0)
    return K.shot('kitchen', lambda _v: light_spring(v), cx, cy, Z, acts=[ira], pre=kitchen_pre(v), fx_=f, focus=0.9, dof_k=16, t=t,
                  snow=False)


# ================================================================== 14: Жора waist-deep, chin up: «Ничего! Мы, дальневосточники, — непотопляемые!»
def r_defy(t, u):
    L = CUTS[15] - CUTS[14]
    Z = lerp(1.45, 1.3, glide(u / L))
    cx, cy = 525.0, 470.0
    v = K.V('flood', cx, cy, Z)
    S = K.S_of(v, 'flood')
    kz, dz = face(FZ, 'zhora', t, (0.0, -0.3), hand_n=(24.0, 84.0) if u > 1.2 else (24.0, 60.0), hand_f=(-22.0, 54.0), frost=0.3)
    z = A(C.zhora, 440.0, 735.0 + dz, S, t=t, **kz); z.near = 0.99
    bx = lerp(720.0, 580.0, u / L)
    pb = A(parcel_box, bx, WL + 6 + 3 * math.sin(t * 2), S * 1.1, t=t); pb.near = 0.99
    def f(big, _):
        water_front(big, v, t, a=0.45)
        ripple(big, v, 440.0, WL, t)
        ox, oy = v.opt(bx, WL - 40)
        if u > 1.0: O.draw_sticker(big, ST_DOOR, t, CUTS[14] + 1.0, CUTS[15], 540, 700)
    return K.shot('flood', K.light_morning, cx, cy, Z, acts=[z, pb], fx_=f, focus=0.8, dof_k=10, t=t, snow=False)


ST_DOOR = K.st('ОСТАВЛЕН У ДВЕРИ', fg=(255, 214, 80), size=48)


# ================================================================== 15: the gull floats on the parcel: «Плаваем.» — the sign «ДО ЗИМЫ: 183 ДНЯ»
def r_gull2(t, u):
    L = CUTS[16] - CUTS[15]
    Z = lerp(2.0, 1.6, glide(u / L))
    bx = lerp(560.0, 640.0, u / L)
    cx, cy = bx + 10.0, 470.0
    v = K.V('flood', cx, cy, Z)
    S = K.S_of(v, 'flood')
    by = WL + 6 + 3 * math.sin(t * 2)
    pb = A(parcel_box, bx, by, S * 1.1, t=t); pb.near = 0.99
    k = S / (3 * v.Z) * 1.1
    kw, dy = face(FC, 'chayka', t, (-0.3, 0.0))
    g = A(C.chayka, bx, by - 16 * k, S * K.GULL * 1.3, t=t, flip=True, **kw); g.near = 0.99
    def f(big, _): water_front(big, v, t, a=0.3)
    return K.shot('flood', K.light_morning, cx, cy, Z, acts=[pb, g], fx_=f, focus=0.8, dof_k=12, t=t, snow=False)


R_ = [r_gull, r_melt, r_joy, r_ira, r_run, r_f9, r_f5, r_f1, r_door, r_twist, r_boat, r_much, r_row, r_ira2, r_defy, r_gull2]
assert len(R_) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 6, ['РАСТАЯЛО!'], hook_t=(0.10, 2.4), hook_y=230, hook_size=90,
              stickers=[(K.st('ПЛЮХ!', fg=(120, 230, 255), size=80), TWIST + 0.15, TWIST + 1.2, 540, 420)],
              flashes=[TWIST, CUTS[1], CUTS[9]], mosaics=[CUTS[4]],
              cap_y={**{i: 1480 for i in range(16)}, 9: 1020, 10: 1020, 11: 1020, 12: 1060, 14: 1020, 15: 1060})


def render(t):
    i = max(0, min(len(R_) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R_[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
