"""S01E05 «1400 ЗА СНЕГ?!» (43.5 s, twist at 24.85 s / 57 %, type: «награда — та же проблема» — the grader he demanded buries him).
Main question: will Жора beat the УК and get a grader for his 1 400?
HOOK: the seagull CU: «Дальний Восток. Снег тут убирает управляющая компания. А платит за это — Жора.» — the УК booth with a bored
dispatcher eating a sandwich; Жора in the window with the receipt. The receipt insert: УБОРКА СНЕГА 1 400 ₽: «Тысяча четыреста за уборку
снега?! Да я ж сам всё чищу!» — the dispatcher in the booth: «Мужчина, ну это вам не материк. У нас снег убирается весной. Сам.» —
«Сам?! Я тут старший по окну! Требую грейдер! Сегодня же!» — «Ладно, ладно. Заявку приняли. Ждите.» — «Вот! Мы, дальневосточники, своего
добиваемся!» — the grader roars by with a beacon; TWIST: its snow wave buries Жора's window. Витёк on the grader step: «Грейдер вызывали?
Город маленький!» The cutaway: the road is clean, the shaft is full: «Дорогу почистил! А снег — к вам. Распишитесь!» The dark kitchen,
the SMS +600 ₽: «Ещё шестьсот?! За то, что меня закопали?!» Ира lights a candle: «Поздравляю, старший по окну. Окна-то у нас больше нет.»
— «Мы, дальневосточники, — привычные.» The gull's head pokes through the snow in the window: «Привыкай. Ты теперь — подвал.»
  python3 ep05.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import fx
import overlays as O
import stage as ST
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

K.DAY = 31
EPI = Episode('ep05', VOICE, DUR, FPS, colors=dict(K.COL, disp=(255, 150, 200)), slug=SLUG, endcard=dict(style='zamelo', lang='ru'),
              promo='ru')
TAB = (C.XTRA, C.EXPR)
FZ = M.Face([(0.0, 'gloomy'), (4.9, 'outraged'), (12.9, 'yelling'), (20.3, 'proud'), (24.6, 'shock'), (31.1, 'outraged'),
             (34.1, 'gloomy'), (38.1, 'exhausted')], TAB, seed=3)
FC = M.Face([(0.0, 'dry')], TAB, seed=8)
FD = M.Face([(0.0, 'dry'), (16.8, 'gloomy')], TAB, seed=5)
FV = M.Face([(0.0, 'cheerful')], TAB, seed=11)
FI = M.Face([(0.0, 'dry')], TAB, seed=13)
NEAR_ROOM = 0.40
WH = (255, 255, 255)
BOOTH_WIN = (272.0, 360.0, 322.0, 430.0)          # the right window of the port booth (world px)
KWIN = (892.0, 40.0, 1215.0, 395.0)                # the kitchen window glass (world px)
CANDLE = (700.0, 382.0)                            # the candle on the kitchen table (world px)


def mouth(who, t):
    return M.mouth(EPI.talk, who, t)


def face(F, who, t, base=(0.7, 0.0), **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), **kw), M.bob(t, m)


def hat_post(sp):
    if 'head' in sp.anchors: C.ushanka_vitek(sp, sp.anchors['head'])


# ---------------------------------------------------------------- small props
def paper(sp, h):
    """the УК receipt held in the hand: a long white slip with lines and a red total"""
    x, y = h
    sp.sup(x + 1.0, y + 6.0, 3.6, 6.4, C.tones((250, 248, 236)), n=4.0, frost=False)
    for q in range(4): C.thin(sp, (x - 1.6, y + 9.6 - q * 1.8), (x + 3.6, y + 9.6 - q * 1.8), (120, 120, 130), 0.3)
    C.thin(sp, (x - 1.0, y + 1.6), (x + 3.4, y + 1.6), (210, 40, 40), 0.6)
    sp.ell(x, y, 1.8, 1.7, C.tones(C.MITT), frost=False)


def candle(sp, h, t=0.0):
    """a white household candle in a saucer with a living flame"""
    x, y = h
    sp.sup(x, y + 0.6, 3.6, 0.8, C.tones((200, 120, 80)), n=3.0, frost=False)
    sp.sup(x, y + 4.6, 1.2, 3.8, C.tones((246, 240, 226)), n=4.0, frost=False)
    fl = 1.0 + 0.15 * math.sin(t * 23) + 0.1 * math.sin(t * 37)
    sp.ell(x + 0.2 * math.sin(t * 9), y + 10.2, 1.0, 1.8 * fl, C.tones((255, 170, 60)), frost=False, ol=False)
    sp.ell(x + 0.2 * math.sin(t * 9), y + 9.9, 0.5, 0.9 * fl, C.tones((255, 250, 210)), frost=False, ol=False)


def ira_candle(t):
    def p(sp, h): candle(sp, h, t)
    return p


def sms_screen(t, t_up=0.0, w=520, h=860):
    S = 4
    im, d, wl, hl = K._phone(w, h, S)
    k = min(1.0, max(0.0, (t - t_up) / 0.2))
    d.rectangle([6, 14, wl - 7, 40], fill=(40, 90, 200, 255))
    K._fit_text(d, 6, wl - 7, 21, 'УК СУГРОБ-СЕРВИС', 9, WH)
    if k > 0:
        d.rounded_rectangle([12, 56, wl - 13, 186], 6, fill=(236, 236, 244, 255))
        K._fit_text(d, 16, wl - 17, 64, 'ДОП. УСЛУГА:', 7, (90, 90, 110))
        K._fit_text(d, 16, wl - 17, 82, 'СНЕГ', 10, (30, 30, 40))
        K._fit_text(d, 16, wl - 17, 100, 'К ВАШЕМУ ОКНУ', 8, (30, 30, 40))
        K._fit_text(d, 16, wl - 17, 130, '+600 ₽', 20, (220, 40, 40))
    return np.array(im.resize((wl * S, hl * S), Image.NEAREST))


def plate_out(v, w, h, lines, x0, y0, **kw):
    """a rusigns plate (world w x h at the world top-left x0, y0) scaled to the output -> (rgba, ox, oy)"""
    p = R.plate(w, h, lines, **kw)
    s = 3 * v.Z / D.WS
    im = Image.fromarray(p).resize((max(1, int(p.shape[1] * s)), max(1, int(p.shape[0] * s))), Image.LANCZOS)
    ox, oy = v.opt(x0, y0)
    return np.array(im), int(ox), int(oy)


def in_rect(big, v, t, win, fn, S, kw, head, anchor=(0.5, 0.45), rect_a=None):
    """draw a hero clipped to a world rect (a window): `head` = the head point in sprite px goes to the anchor of the rect
    (rect_a: another rect for the anchor)"""
    x0, y0, x1, y1 = win
    a0, b0, a1, b1 = rect_a or win
    tmp = big.copy()
    with ZX.res(ZX.res_for(S)), ZX.sky_light():
        sp = ZX.Spr(); fn(sp, t=t, **kw); sp.rim(); sp.outline(ZX.INK)
    ox, oy = v.opt(a0 + (a1 - a0) * anchor[0], b0 + (b1 - b0) * anchor[1])
    blit(tmp, sp, ox - head[0] * S, oy + head[1] * S, S, None, False)
    ax, ay = v.opt(x0, y0); bx, by = v.opt(x1, y1)
    ax, ay, bx, by = int(max(0, ax)), int(max(0, ay)), int(min(big.shape[1], bx)), int(min(big.shape[0], by))
    if ax < bx and ay < by: big[ay:by, ax:bx] = tmp[ay:by, ax:bx]


# ---------------------------------------------------------------- the УК booth (port world) with the dispatcher in the window
def booth_pre(t, v, S_d, cu=False):
    def pre(big, _v):
        kw, _ = face(FD, 'disp', t, (0.8, 0.0), chew=0.0 if mouth('disp', t) > 0.05 else 1.0)
        x0, y0, x1, y1 = BOOTH_WIN
        win = (x0 - 40, y0 - 50, x1 + 40, y1 + 2) if cu else BOOTH_WIN            # CU: she leans out over the sill
        in_rect(big, v, t, win, C.disp, S_d, kw, head=(1.4, 40.0), anchor=(0.45, 0.62 if cu else 0.42), rect_a=BOOTH_WIN if cu else None)
        if cu:                                                                     # the sill board with snow over the cut
            ax, ay = v.opt(x0 - 14, y1 - 3); bx, by = v.opt(x1 + 14, y1 + 6)
            big[int(ay):int(by), int(ax):int(bx)] = (96, 70, 56)
            big[int(ay):int(ay) + int(2 * v.Z), int(ax):int(bx)] = (150, 116, 90)
            for q in range(int(ax), int(bx), int(3 * v.Z)):
                h_ = int((2 + 2 * math.sin(q * 0.05)) * v.Z)
                big[max(0, int(ay) - h_):int(ay), q:q + int(3 * v.Z)] = (240, 246, 255)
        if cu: return                                                   # CU: the plate is read in the wide shot
        p, ox, oy = plate_out(v, 94, 22, ['УК «СУГРОБ-СЕРВИС»'], 236.0, 446.0, bg=(30, 70, 150), fg=WH, border=WH, round_=3)
        O.overlay(big, p, ox, oy, 1.0)
        p, ox, oy = plate_out(v, 70, 30, ['ПРИЁМ', 'ДО ВЕСНЫ'], 100.0, 440.0, bg=(250, 246, 230), fg=(200, 40, 40),
                              border=(200, 40, 40), tilt=-4)
        O.overlay(big, p, ox, oy, 1.0)
    return pre


def zhora_window(t, v, base=(0.5, -0.3), x=680.0, **extra):
    S = K.S_of(v, 'facade')
    kw, dy = face(FZ, 'zhora', t, base, **extra)
    z = A(C.zhora, x, 640.0 + dy, S, t=t, **kw); z.near = NEAR_ROOM
    return z


# ---------------------------------------------------------------- the dark kitchen (the window is buried)
def snow_wall(big, v, t, rect=KWIN, lit=0.0, seed=4):
    """packed snow pressed against the glass: replaces the bluish/bright pixels inside the window rect (keeps the brown frame)"""
    x0, y0, x1, y1 = rect
    ax, ay = v.opt(x0, y0); bx, by = v.opt(x1, y1)
    ax, ay, bx, by = int(max(0, ax)), int(max(0, ay)), int(min(big.shape[1], bx)), int(min(big.shape[0], by))
    if ax >= bx or ay >= by: return
    reg = big[ay:by, ax:bx].astype(np.int32)
    m = (reg[..., 2] > reg[..., 0] + 8) | (reg.sum(-1) > 560)
    px = max(3, int(2 * v.Z))
    hh, ww = reg.shape[:2]
    g = np.random.default_rng(seed)
    n = g.random(((hh + px - 1) // px, (ww + px - 1) // px))
    n = np.kron(n, np.ones((px, px)))[:hh, :ww]
    yy = (np.arange(hh)[:, None] + ay - v.opt(0, 0)[1]) / (3 * v.Z)
    strata = 0.5 + 0.5 * np.sin(yy / 7.0 + np.arange(ww)[None, :] / (3 * v.Z) / 40.0)
    base = np.array((150, 170, 214), np.float32) * (1 + lit)
    col = base[None, None, :] * (0.78 + 0.14 * n[..., None] + 0.08 * strata[..., None])
    reg[m] = np.clip(col[m], 0, 255).astype(np.int32)
    big[ay:by, ax:bx] = reg.astype(np.uint8)


def glow(big, cx, cy, r, col, a):
    H_, W_ = big.shape[:2]
    y0, y1, x0, x1 = max(0, int(cy - 2 * r)), min(H_, int(cy + 2 * r)), max(0, int(cx - 2 * r)), min(W_, int(cx + 2 * r))
    if y0 >= y1 or x0 >= x1: return
    yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
    g = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * (r * 0.6) ** 2))[..., None]
    reg = big[y0:y1, x0:x1].astype(np.float32)
    reg = reg * (1 + a * 1.6 * g) + np.array(col, np.float32) * a * 0.5 * g
    big[y0:y1, x0:x1] = np.clip(reg, 0, 255).astype(np.uint8)


def dark_pre(t, v, candle_on=True, phone_at=None, t_light=None):
    def pre(big, _v):
        snow_wall(big, v, t)
        big[:] = np.clip(big.astype(np.float32) * np.array((0.40, 0.40, 0.50)), 0, 255).astype(np.uint8)
        k = 1.0 if t_light is None else min(1.0, max(0.0, (t - t_light) / 0.4))
        if candle_on and k > 0:
            cx, cy = v.opt(*CANDLE)
            fl = 1 + 0.06 * math.sin(t * 17)
            glow(big, cx, cy - 30 * v.Z, 330 * v.Z * fl * (0.4 + 0.6 * k), (255, 150, 60), 0.9 * k)
        if phone_at is not None:
            glow(big, phone_at[0], phone_at[1], 260, (120, 170, 255), 0.7)
    return pre


def light_dark(v, candle_on=True, phone_at=None, k=1.0):
    keys = []
    if candle_on and k > 0:
        cx, cy = v.opt(*CANDLE)
        keys.append((cx, cy - 30 * v.Z, 420 * v.Z, (255, 160, 80), 0.95 * k))
    if phone_at is not None:
        keys.append((phone_at[0], phone_at[1], 360, (140, 190, 255), 0.8))
    return ST.Light(amb=(0.55, 0.52, 0.64), keys=keys, grad=(1.0, 0.9))


def candle_act(t, v, S):
    def fn(sp, t=0.0): candle(sp, (0.0, 0.0), t)
    c = A(fn, CANDLE[0], CANDLE[1], S * 1.0, t=t); c.near = 0.99
    return c


# ================================================================== 0: «Дальний Восток.» — CU the gull on the snow at Жора's window
def r_gull(t, u):
    Z = 2.8 * (1 + 0.025 * u)
    cx, cy = 840.0, 470.0
    v = K.V('facade', cx, cy, Z)
    kw, dy = face(FC, 'chayka', t, (0.0, 0.0))
    g = A(C.chayka, 850.0, 500.0 + dy * 0.3, K.WS['facade'] * 3 * v.Z * 0.6, t=t, flip=True, **kw); g.near = 0.62
    return K.shot('facade', K.light_morning, cx, cy, Z, acts=[g], focus=0.62, dof_k=30, t=t, snow_n=60, kick=kick(t, [(0.12, 0.8)]))


# ================================================================== 1: «Снег тут убирает управляющая компания.» — the УК booth
def r_uk(t, u):
    L = CUTS[2] - CUTS[1]
    Z = lerp(2.2, 2.5, glide(u / L))
    cx, cy = 282.0, 410.0
    v = K.V('port', cx, cy, Z)
    S_d = K.WS['port'] * 3 * v.Z * 0.9
    return K.shot('port', K.light_morning, cx, cy, Z, pre=booth_pre(t, v, S_d), t=t, focus=0.5, dof_k=10, snow_n=70,
                  glints=(0, 1400, 1080, 1900))


# ================================================================== 2: «А платит за это — Жора.» — Жора in the window with the receipt
def r_pays(t, u):
    Z = 1.6
    v = K.V('facade', 700.0, 390.0, Z)
    z = zhora_window(t, v, (0.0, -0.6), hand_n=(19.0, 54.0), prop_n=paper, frost=0.3)
    return K.shot('facade', K.light_window, 700.0, 390.0, Z, acts=[z], focus=0.42, dof_k=18, t=t, snow_n=45)


# ================================================================== 3: the receipt insert -> «Тысяча четыреста за уборку снега?!»
def r_rcpt(t, u):
    if u < 1.3:
        Z = 1.6
        cx, cy = 715.0, 330.0
        def pre(big, _v): big[:] = K.blur(big, 12)
        def f(big, _):
            rc = C.receipt_img(w=560, h=880, total=1400)
            x0, y0 = 260, 470 + int(10 * math.sin(t * 4))
            O.overlay(big, rc, x0, y0, 1.0)
        return K.shot('facade', K.light_window, cx, cy, Z, pre=pre, fx_=f, t=t, dof_k=0, snow_n=50, kick=kick(t, [(CUTS[3] + 0.4, 0.9)]))
    Z = 2.0
    v = K.V('facade', 700.0, 380.0, Z)
    z = zhora_window(t, v, (0.5, -0.3), hand_n=(21.0, 60.0 + 4 * math.sin(t * 9)), prop_n=paper, frost=0.3)
    return K.shot('facade', K.light_window, 700.0, 380.0, Z, acts=[z], focus=0.42, dof_k=22, t=t, snow_n=45)


# ================================================================== 4: the dispatcher: «Мужчина, ну это вам не материк…»
def r_disp(t, u):
    L = CUTS[5] - CUTS[4]
    Z = lerp(2.6, 2.8, glide(u / L))
    cx, cy = 297.0, 400.0
    v = K.V('port', cx, cy, Z)
    S_d = K.WS['port'] * 3 * v.Z * 1.6
    return K.shot('port', K.light_morning, cx, cy, Z, pre=booth_pre(t, v, S_d, cu=True), t=t, focus=0.5, dof_k=0, snow_n=40)


# ================================================================== 5: CU Жора shouting into the phone: «Сам?! Я тут старший по окну!…»
def r_shout(t, u):
    Z = 2.1
    v = K.V('facade', 700.0, 380.0, Z)
    z = zhora_window(t, v, (0.6, -0.2), hand_n=(19.0, 54.0), prop_n=C.phone, frost=0.3)
    return K.shot('facade', K.light_window, 700.0, 380.0, Z, acts=[z], focus=0.42, dof_k=22, t=t, snow_n=45,
                  kick=kick(t, [(CUTS[5] + 2.7, 0.9)]))


# ================================================================== 6: the dispatcher: «Ладно, ладно. Заявку приняли. Ждите.»
def r_disp2(t, u):
    Z = 2.7
    cx, cy = 297.0, 404.0
    v = K.V('port', cx, cy, Z)
    S_d = K.WS['port'] * 3 * v.Z * 1.75
    def f(big, _):
        if u > 2.6:
            O.draw_sticker(big, ST_ACC, t, CUTS[6] + 2.6, CUTS[7], 540, 1240)
    return K.shot('port', K.light_morning, cx, cy, Z, pre=booth_pre(t, v, S_d, cu=True), fx_=f, t=t, focus=0.5, dof_k=0, snow_n=40)


ST_ACC = K.st('ЗАЯВКА ПРИНЯТА', fg=(120, 230, 120), size=56)


# ================================================================== 7: «Вот! Мы, дальневосточники, своего добиваемся!» — the beacon flickers on him
def r_proud(t, u):
    L = CUTS[8] - CUTS[7]
    Z = lerp(1.5, 1.7, glide(u / L))
    v = K.V('facade', 700.0, 390.0, Z)
    z = zhora_window(t, v, (0.0, -0.4) if u < 2.6 else (0.9, -0.3), hand_n=(18.0, 58.0), frost=0.2)
    def f(big, _):
        if u > 2.0 and int(t * 5) % 2 == 0:
            k = min(1.0, (u - 2.0) / 1.0)
            big[:] = np.clip(big.astype(np.float32) * (1 + 0.16 * k * np.array((1.0, 0.55, 0.0))), 0, 255).astype(np.uint8)
    return K.shot('facade', K.light_window, 700.0, 390.0, Z, acts=[z], fx_=f, focus=0.42, dof_k=16, t=t, snow_n=45,
                  kick=(0, 3 * math.sin(t * 40)) if u > 2.6 else (0, 0))


# ================================================================== 8: the grader roars along the snow road, the blade throws a wave
def r_grader(t, u):
    L = CUTS[9] - CUTS[8]
    Z = 1.1
    cx, cy = 1110.0, 500.0
    v = K.V('yard', cx, cy, Z)
    S = K.WS['yard'] * 3 * v.Z * 1.5
    x = lerp(1250.0, 1080.0, u / L)
    g = A(C.grader, x, 572.0, S, t=t, flip=True, vitek_kw={}, blade=1.0, spin=-8.0); g.near = 0.99
    def f(big, _):
        ox, oy = v.opt(x - 70, 560.0)
        K.puff(big, ox, oy, t, t - (t * 8 % 0.12), n=16, seed=int(t * 8), life=0.45, speed=520, px=14)
        fx.speed_lines(big, t, 0.2)
    return K.shot('yard', K.light_morning, cx, cy, Z, acts=[g], fx_=f, t=t, focus=0.8, dof_k=6, snow_n=80,
                  kick=(2 * math.sin(t * 37), 3 * math.sin(t * 41)))


# ================================================================== 9: TWIST — Жора turns; the snow wave slams into the window
def r_slam(t, u):
    Z = 1.45
    v = K.V('facade', 700.0, 400.0, Z)
    z = zhora_window(t, v, (1.0, 0.0), hand_n=(20.0, 64.0) if t > TWIST - 0.15 else (18.0, 56.0), frost=0.2)
    def f(big, _):
        k = (t - (TWIST - 0.25)) / 0.25                                       # the wave front from the right edge
        if k > 0:
            H_, W_ = big.shape[:2]
            xf = int(W_ * (1.05 - min(1.2, k) * 1.1))
            yy = np.arange(H_)[:, None]
            edge = xf + (np.sin(yy / 37.0 + t * 9) * 40 + np.sin(yy / 11.0) * 14).astype(int)
            xx = np.arange(W_)[None, :]
            m = xx >= edge
            g = np.random.default_rng(int(t * 30))
            tex = np.array((228, 238, 255), np.float32) * (0.86 + 0.14 * g.random((H_ // 12 + 1, W_ // 12 + 1)))[..., None]
            tex = np.kron(tex, np.ones((12, 12, 1)))[:H_, :W_]
            big[m] = tex[m].astype(np.uint8)
            if k < 1.4:
                for q in range(30):
                    gx = int(xf - g.random() * 260); gy = int(g.random() * H_)
                    s_ = int(10 + g.random() * 22)
                    big[max(0, gy):gy + s_, max(0, gx):gx + s_] = (240, 246, 255)
    return K.shot('facade', K.light_window, 700.0, 400.0, Z, acts=[z], fx_=f, focus=0.42, dof_k=16, t=t, snow_n=60,
                  kick=kick(t, [(TWIST, 1.4)]))


# ================================================================== 10: Витёк on the grader step: «Грейдер вызывали? Город маленький!»
def buried_window(big, v, t, k=1.0):
    """the snow wave piled up over Жора's window on the facade (world polygon, bg level)"""
    H_, W_ = big.shape[:2]
    pts = [(360, 760), (420, 480), (520, 260), (640, 160), (780, 150), (900, 175), (950, 290), (985, 470), (1010, 760)]
    from PIL import ImageDraw
    m = Image.new('L', (W_, H_), 0)
    ImageDraw.Draw(m).polygon([v.opt(x, y) for x, y in pts], fill=255)
    m = np.array(m) > 0
    yy, xx = np.mgrid[0:H_, 0:W_]
    px = max(4, int(2 * v.Z))
    g = np.random.default_rng(7).random((H_ // px + 1, W_ // px + 1))
    n = np.kron(g, np.ones((px, px)))[:H_, :W_]
    sh = 0.84 + 0.10 * n + 0.08 * np.clip((xx - W_ * 0.3) / W_, 0, 1) - 0.10 * np.clip((yy - H_ * 0.5) / H_, 0, 1)
    col = (np.array((232, 240, 255), np.float32)[None, None, :] * sh[..., None])
    big[m] = np.clip(col[m], 0, 255).astype(np.uint8)


def r_cab(t, u):
    Z = 0.95
    cx, cy = 925.0, 400.0
    v = K.V('facade', cx, cy, Z)
    S = K.S_of(v, 'facade') * 1.0
    def pre(big, _v): buried_window(big, v, t)
    g = A(C.grader, 1240.0, 720.0, S * 2.2, t=t, flip=True, blade=1.0, beacon=True, snow=True); g.near = 0.97
    kv, dv = face(FV, 'vitek', t, (-0.6, 0.0), hand_n=(-16.0, 62.0) if u < 1.3 else (14.0, 60.0))
    vk = A(C.vitek, 840.0, 760.0 + dv, S, t=t, post=hat_post, **kv); vk.near = 0.99
    return K.shot('facade', K.light_morning, cx, cy, Z, acts=[g, vk], pre=pre, t=t, focus=0.9, dof_k=10, snow_n=55)


# ================================================================== 11: the cutaway: the road is clean, the shaft is full: «А снег — к вам.»
def r_road(t, u):
    L = CUTS[12] - CUTS[11]
    Z = 0.62
    cx, cy = 400.0, 516.0
    v = K.V('cutaway', cx, cy, Z)
    S = K.WS['cutaway'] * 3 * v.Z
    k = glide(min(1.0, u / 1.6))
    x = lerp(700.0, 560.0, k)
    def pre(big, _v):
        top = K.SNOW_TOP
        pts = [(330, top + 2), (350, top - 30 - 30 * k), (395, top - 60 - 40 * k), (440, top - 40 - 20 * k), (x - 70, top - 4), (x - 70, top + 2)]
        from PIL import ImageDraw
        m = Image.new('L', (big.shape[1], big.shape[0]), 0)
        ImageDraw.Draw(m).polygon([v.opt(a, b) for a, b in pts], fill=255)
        mm = np.array(m) > 0
        big[mm] = (236, 242, 255)
        ax, ay = v.opt(x + 40, top - 3); bx, by = v.opt(720, top + 5)                  # the clean road behind the grader
        big[int(ay):int(by), int(ax):int(bx)] = (120, 130, 150)
        for q in range(int(ax), int(bx), 60): big[int(ay) + 8:int(ay) + 12, q:q + 30] = (240, 220, 120)
    g = A(C.grader, x, K.SNOW_TOP, S * 1.3, t=t, flip=True, vitek_kw={}, blade=1.0, spin=-6.0 * (1 - k)); g.near = 0.99
    def f(big, _):
        if u < 1.7:
            ox, oy = v.opt(x - 64, K.SNOW_TOP - 10)
            K.puff(big, ox, oy, t, t - (t * 8 % 0.12), n=12, seed=int(t * 8), life=0.4, speed=380, px=10)
        sx, sy = v.opt(392.0, 220.0)
        if u > 1.4: O.draw_sticker(big, ST_SHAFT, t, CUTS[11] + 1.4, CUTS[12], int(sx), int(sy))
    return K.shot('cutaway', K.light_cut, cx, cy, Z, acts=[g], pre=pre, fx_=f, t=t, focus=0.5, dof_k=0, snow_n=50, bloom=(240, 14, 0.25))


ST_SHAFT = K.st('ВАШ СНЕГ', fg=(255, 214, 80), size=58)


# ================================================================== 12: the dark kitchen: the SMS +600 -> «Ещё шестьсот?!»
def r_dark(t, u):
    if u < 1.0:
        Z = 2.0
        cx, cy = 760.0, 360.0
        v = K.V('kitchen', cx, cy, Z)
        def pre(big, _v):
            dark_pre(t, v, candle_on=False)(big, _v)
            big[:] = K.blur(big, 10)
        def f(big, _):
            ph = sms_screen(t, t_up=CUTS[12] + 0.1)
            x0, y0 = 280, 520 + int(8 * math.sin(t * 4))
            O.overlay(big, ph, x0, y0, 1.0)
            glow(big, x0 + ph.shape[1] // 2, y0 + ph.shape[0] // 2, 500, (120, 170, 255), 0.5)
        return K.shot('kitchen', lambda _v: light_dark(v, False), cx, cy, Z, pre=pre, fx_=f, t=t, dof_k=0, snow=False, kick=kick(t, [(CUTS[12] + 0.3, 0.9)]))
    Z = 1.7
    cx, cy = 760.0, 440.0
    v = K.V('kitchen', cx, cy, Z)
    S = K.S_of(v, 'kitchen')
    kw, dy = face(FZ, 'zhora', t, (0.0, -0.5), hand_n=(18.0, 50.0), prop_n=C.phone)
    z = A(C.zhora, 760.0, 720.0 + dy, S, t=t, **kw); z.near = 0.99
    ph = (640, 900)
    return K.shot('kitchen', lambda _v: light_dark(v, False, ph), cx, cy, Z, acts=[z], pre=dark_pre(t, v, False, ph), focus=0.9, dof_k=14, t=t,
                  snow=False, kick=kick(t, [(CUTS[12] + 2.0, 0.7)]))


# ================================================================== 13: Ира lights a candle: «Поздравляю, старший по окну…»
def r_candle(t, u):
    L = CUTS[14] - CUTS[13]
    Z = lerp(0.92, 1.0, glide(u / L))
    cx, cy = 760.0, 400.0
    v = K.V('kitchen', cx, cy, Z)
    S = K.S_of(v, 'kitchen')
    tl = CUTS[13] + 0.5
    kl = min(1.0, max(0.0, (t - tl) / 0.4))
    ki, di = face(FI, 'ira', t, (0.9, 0.0) if u < 2.2 else (-0.9, -0.2), hand_n=(18.0, 46.0) if u < 0.9 else (14.0, 40.0))
    ira = A(C.ira, 640.0, 712.0 + di, S, t=t, **ki); ira.near = 0.99
    kz, dz = face(FZ, 'zhora', t, (-0.9, 0.0), sit=1.0, hand_n=(-10.0, 46.0), hand_f=(-16.0, 44.0))
    z = A(C.zhora, 880.0, 712.0 + dz, S, t=t, flip=True, **kz); z.near = 0.99
    acts = [z, ira]
    if kl > 0: acts.append(candle_act(t, v, S))
    def f(big, _):
        if 0 < t - tl < 0.25:                                                    # the match flare
            ox, oy = v.opt(CANDLE[0], CANDLE[1] - 30)
            glow(big, ox, oy, 160, (255, 220, 120), 1.2)
    return K.shot('kitchen', lambda _v: light_dark(v, True, k=kl), cx, cy, Z, acts=acts, pre=dark_pre(t, v, True, t_light=tl), fx_=f, focus=0.9,
                  dof_k=8, t=t, snow=False)


# ================================================================== 14: CU Жора by the candle: «Мы, дальневосточники, — привычные.»
def r_used(t, u):
    Z = 1.7
    cx, cy = 850.0, 470.0
    v = K.V('kitchen', cx, cy, Z)
    S = K.S_of(v, 'kitchen')
    kz, dz = face(FZ, 'zhora', t, (-0.4, -0.4), sit=1.0, hand_n=(-10.0, 46.0), hand_f=(-16.0, 44.0))
    z = A(C.zhora, 900.0, 712.0 + dz, S, t=t, flip=True, **kz); z.near = 0.99
    return K.shot('kitchen', lambda _v: light_dark(v, True), cx, cy, Z, acts=[z, candle_act(t, v, S)], pre=dark_pre(t, v, True), focus=0.9,
                  dof_k=16, t=t, snow=False)


# ================================================================== 15: the gull pokes its head through the snow: «Привыкай. Ты теперь — подвал.»
def r_beak(t, u):
    Z = 2.6
    cx, cy = 1135.0, 250.0
    v = K.V('kitchen', cx, cy, Z)
    S = K.WS['kitchen'] * 3 * v.Z * 0.62
    hx, hy = 1135.0, 225.0
    k = glide(min(1.0, u / 0.35))
    def pre(big, _v):
        dark_pre(t, v, True)(big, _v)
        tmp = big.copy()
        kw, _ = face(FC, 'chayka', t, (-0.2, 0.0))
        with ZX.res(ZX.res_for(S)), ZX.sky_light():
            sp = ZX.Spr(); C.chayka(sp, t=t, **kw); sp.rim(); sp.outline(ZX.INK)
        hd = sp.anchors.get('head', (14.0, 26.0))
        ox, oy = v.opt(hx, hy)
        blit(tmp, sp, ox - hd[0] * S + (1 - k) * 60, oy + hd[1] * S + (1 - k) * 160, S, None, False)
        H_, W_ = big.shape[:2]
        yy, xx = np.mgrid[0:H_, 0:W_]
        r = 11 * S * (0.4 + 0.6 * k)
        d2 = (xx - ox) ** 2 + (yy - oy - 4 * S) ** 2
        hole = d2 < r * r
        ring = (d2 < (r * 1.18) ** 2) & ~hole
        big[ring] = (120, 136, 176)
        big[hole] = (40, 46, 70)
        mm = hole & (np.abs(tmp.astype(np.int32) - big.astype(np.int32)).sum(-1) > 0)
        big[hole] = tmp[hole]
    def f(big, _):
        ox, oy = v.opt(hx, hy + 40)
        K.puff(big, ox, oy, t, CUTS[15] + 0.05, n=24, seed=5, col=(200, 214, 240), life=0.8, speed=300, px=12)
    return K.shot('kitchen', lambda _v: light_dark(v, True), cx, cy, Z, pre=pre, fx_=f, focus=0.5, dof_k=0, t=t, snow=False, kick=kick(t, [(CUTS[15] + 0.1, 0.8)]))


R_ = [r_gull, r_uk, r_pays, r_rcpt, r_disp, r_shout, r_disp2, r_proud, r_grader, r_slam, r_cab, r_road, r_dark, r_candle, r_used, r_beak]
assert len(R_) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 5, ['1400', 'ЗА СНЕГ?!'], hook_t=(0.10, 2.4), hook_y=230, hook_size=84,
              stickers=[(K.st('ЗАКОПАЛИ!', fg=(255, 110, 150), size=72), TWIST + 0.1, TWIST + 0.7, 540, 420),
                        (K.st('ПОДВАЛ', fg=(255, 214, 80), size=72), CUTS[15] + 1.2, DUR - 1.0, 540, 1330)],
              flashes=[TWIST, CUTS[1], CUTS[12]], mosaics=[CUTS[8]],
              cap_y={0: 1510, 1: 1480, 2: 1500, 3: 440, 4: 1480, 5: 1500, 6: 1480, 7: 1500, 8: 1480, 9: 1500, 10: 1020, 11: 1480,
                     12: 440, 13: 1480, 14: 1480, 15: 1480})


def render(t):
    i = max(0, min(len(R_) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R_[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
