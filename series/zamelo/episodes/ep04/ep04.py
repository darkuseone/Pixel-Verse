"""S01E04 «ТАКСИ — 3000?!» (43.9 s, twist at 23.6 s / 54 %, type: «охотник просит помощи» — the taxi makes the passenger pull).
Main question: will Жора get to work by taxi for three thousand?
HOOK: the seagull close up: «Дальний Восток. Автобус тут ходит — в апреле. Поэтому все ездят на такси. А такси — на собаках.» — a dog
sled taxi zooms past the buried bus stop. The phone: ЯМЩИК Go ×7 — 3000 ₽: «Сколько?! Три тысячи до работы?!…» — «Ну и ладно. Пешком —
это на материке. Заказываю!» The sled with six huskies at the window, Витёк in a checker ushanka: «Такси «Ямщик», тариф «Эконом»!…» —
«Витёк?! Ты ж вчера курьером был!» — «Ну. Город-то маленький.» — the ride: «Вот это сервис! За три тыщи — с ветерком!» TWIST: the dogs
lie down: «Всё, братан, приехали. У собак обед. А на «Экономе» дальше тянет пассажир.» — «В смысле?! Я ж три тысячи заплатил!» — «Так три
тысячи — это собакам. А ты — бесплатно.» Жора in the harness pulls the sled with Витёк and six dogs: «Баклан, ну хоть ты помоги!» — «Я —
чайка. А ты теперь — ездовой.» The port gate: six huskies stare: «Оценочку, братан. Собаки смотрят.» — «Пять звёзд.»
  python3 ep04.py test 1 5 20 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import fx
import overlays as O
from scene import lerp
from cam25 import glide, kick
from episode import Episode
from props import zamcast as C
from props import zamkit as K
from props import zampix as ZX
from props import mimic as M
from props.dibspix import blit
from props.zamkit import A
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

K.DAY = 64
EPI = Episode('ep04', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='zamelo', lang='ru'), promo='ru')
TAB = (C.XTRA, C.EXPR)
FZ = M.Face([(0.0, 'outraged'), (9.4, 'cocky'), (15.4, 'stunned'), (19.3, 'cheerful'), (23.6, 'shock'), (27.4, 'outraged'),
             (33.6, 'exhausted'), (38.9, 'nervous'), (41.9, 'gloomy')], TAB, seed=3)
FC = M.Face([(0.0, 'dry')], TAB, seed=8)
FV = M.Face([(0.0, 'cheerful'), (23.6, 'smug'), (30.1, 'cheerful')], TAB, seed=11)
NEAR_ROOM = 0.40


def mouth(who, t):
    return M.mouth(EPI.talk, who, t)


def face(F, who, t, base=(0.7, 0.0), **kw):
    m = mouth(who, t)
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), **kw), M.bob(t, m)


def vitek_hat(sp, h): pass


def team(t, v, x, y, S, run=True, lie=False, stare=False, rider=True, musher=True, dogs_in=False, look_z=(0.9, 0.0), puller=False):
    """the dog sled taxi at real scale: the sled (2.5 m = 2.2 x hero scale), 6 huskies (pairs, ~1.4 x hero scale) on a gang line in
    front (+x), Витёк standing on the runners at the back, Жора sitting in the bed. (x, y) = ground under the sled centre (world)."""
    k = S / (3 * v.Z)                                                          # world px per hero sprite px
    acts = []
    Ss = S * 2.2
    sl = A(C.sled, x, y, Ss, t=t); sl.near = 0.99
    acts.append(sl)
    if dogs_in:                                                                 # the dogs ride in the sled (after the twist)
        for i in range(6):
            d = A(C.husky, x + (-30 + i * 9) * k, y - 10 * k - (i % 2) * 4 * k, S * 1.1, t=t, run=False, stare=True, ph=i)
            d.near = 0.99; acts.append(d)
    elif not puller:
        for i in range(3):
            for j in range(2):
                xx = x + (64 + i * 34) * k + j * 6 * k
                yy = y + (j * 6 - 3) * k
                d = A(C.husky, xx, yy, S * 1.35, t=t, run=run, lie=lie, stare=stare, ph=i * 1.7 + j)
                d.near = 0.99; acts.append(d)
    if rider:
        kw, dy = face(FZ, 'zhora', t, look_z, sit=1.0, hand_n=(22.0, 50.0), hand_f=(-12.0, 44.0))
        z = A(C.zhora, x - 4 * k, y - 8 * k + dy, S, t=t, **kw); z.near = 0.99
        acts.insert(1, z)
    if musher:
        kv, dv = face(FV, 'vitek', t, (0.9, 0.0), hand_n=(10.0, 40.0), post_hat=True)
        kv.pop('post_hat')
        vk = A(C.vitek, x - 48 * k, y - 2 * k + dv, S * 0.95, t=t, post=hat_post, **kv); vk.near = 0.99
        acts.insert(0, vk)
    return acts


def hat_post(sp):
    if 'head' in sp.anchors: C.ushanka_vitek(sp, sp.anchors['head'])


def taxi_screen(t, t_up=0.0, w=600, h=980):
    S = 4
    im, d, wl, hl = K._phone(w, h, S)
    d.rectangle([6, 14, wl - 7, 42], fill=(250, 214, 40, 255))
    K._fit_text(d, 6, wl - 7, 22, 'ЯМЩИК Go', 10, (30, 30, 40))
    K._fit_text(d, 14, wl - 15, 60, 'ДОМ → РЫБПОРТ', 8, (30, 30, 40))
    K._fit_text(d, 14, wl - 15, 80, '3 КМ • ЭКОНОМ', 7, (90, 90, 110))
    k = min(1.0, max(0.0, (t - t_up) / 0.2))
    d.rounded_rectangle([14, 104, wl - 15, 136], 6, fill=(255, 60, 60, 255))
    K._fit_text(d, 14, wl - 15, 112, 'СПРОС ×7', 12, (255, 255, 255))
    K._fit_text(d, 14, wl - 15, 152, f'{int(430 + 2570 * k)} ₽', 22, (30, 30, 40))
    d.rounded_rectangle([14, hl - 60, wl - 15, hl - 30], 6, fill=(250, 214, 40, 255))
    K._fit_text(d, 14, wl - 15, hl - 52, 'ЗАКАЗАТЬ', 10, (30, 30, 40))
    return np.array(im.resize((wl * S, hl * S), Image.NEAREST))


# ================================================================== 0: «Дальний Восток.» — CU the gull on the buried bus stop board
def r_gull(t, u):
    Z = 2.8 * (1 + 0.025 * u)
    cx, cy = 520.0, 470.0
    v = K.V('yard', cx, cy, Z)
    kw, dy = face(FC, 'chayka', t, (0.0, 0.0))
    g = A(C.chayka, 530.0, 520.0 + dy * 0.3, K.WS['yard'] * 3 * v.Z * 1.6, t=t, flip=True, **kw); g.near = 0.99
    return K.shot('yard', K.light_morning, cx, cy, Z, acts=[g], focus=0.6, dof_k=26, t=t, snow_n=60, kick=kick(t, [(0.12, 0.8)]))


# ================================================================== 1: a sled taxi zooms past the buried bus stop «АВТОБУС — В АПРЕЛЕ»
def r_reveal(t, u):
    L = CUTS[2] - CUTS[1]
    Z = 1.25
    cx, cy = 560.0, 470.0
    v = K.V('yard', cx, cy, Z)
    S = K.WS['yard'] * 3 * v.Z * 1.25
    x = lerp(260.0, 980.0, u / L)
    acts = team(t, v, x, 640.0, S, rider=True, look_z=(0.9, 0.0))
    def f(big, _):
        ox, oy = v.opt(x - 60, 640.0)
        K.puff(big, ox, oy, t, t - (t * 6 % 0.17), n=8, seed=int(t * 6), life=0.35, speed=320, px=12)
        fx.speed_lines(big, t, 0.15)
    return K.shot('yard', K.light_morning, cx, cy, Z, acts=acts, fx_=f, t=t, focus=0.8, dof_k=6, snow_n=60, glints=(0, 1400, 1080, 1900))


# ================================================================== 2: the phone: ЯМЩИК Go ×7 — 3000 ₽; then Жора: «Сколько?!»
def mitten(sp, t=0.0):
    sp.ell(0.0, 7.0, 9.0, 8.0, C.tones(C.MITT), frost=False)
    sp.ell(-7.4, 11.0, 3.2, 4.4, C.tones(C.MITT), frost=False)
    for q in range(9):
        x0 = -8.0 + q * 2.0
        C.thin(sp, (x0, 1.6 + (q % 2) * 1.2), (x0 + 2.0, 1.6 + ((q + 1) % 2) * 1.2), C.WHITE, 0.45)
    sp.sup(0.0, -2.0, 8.6, 2.6, C.tones(C.ALASKA), n=3.0)


def zhora_window(t, v, base=(0.5, -0.3), **extra):
    S = K.S_of(v, 'facade')
    kw, dy = face(FZ, 'zhora', t, base, **extra)
    z = A(C.zhora, 680.0, 640.0 + dy, S, t=t, **kw); z.near = NEAR_ROOM
    return z


def r_phone(t, u):
    Z = 1.6
    cx, cy = 715.0, 330.0
    if u < 1.6:
        def pre(big, _v): big[:] = K.blur(big, 12)
        def f(big, _):
            ph = taxi_screen(t, t_up=CUTS[2] + 0.25, w=520, h=860)
            x0, y0 = 280, 520 + int(10 * math.sin(t * 4))
            O.overlay(big, ph, x0, y0, 1.0)
            sp = ZX.draw(mitten, 22.0, t=t)
            blit(big, sp, x0 + ph.shape[1] // 2 + 40, y0 + ph.shape[0] + 60, 22.0, None, False)
        return K.shot('facade', K.light_window, cx, cy, Z, pre=pre, fx_=f, t=t, dof_k=0, snow_n=50, kick=kick(t, [(CUTS[2] + 0.45, 0.9)]))
    Z = 2.0
    v = K.V('facade', 700.0, 380.0, Z)
    z = zhora_window(t, v, hand_n=(19.0, 52.0), prop_n=C.phone, frost=0.3)
    return K.shot('facade', K.light_window, 700.0, 380.0, Z, acts=[z], focus=0.42, dof_k=22, t=t, snow_n=45)


# ================================================================== 3: «Ну и ладно. Пешком — это на материке. Заказываю!»
def r_order(t, u):
    Z = 1.7
    v = K.V('facade', 710.0, 390.0, Z)
    z = zhora_window(t, v, (0.8, -0.4), hand_n=(20.0, 58.0 + (4.0 if u > 2.3 else 0.0)), prop_n=C.phone)
    return K.shot('facade', K.light_window, 710.0, 390.0, Z, acts=[z], focus=0.42, dof_k=16, t=t, snow_n=45,
                  kick=kick(t, [(CUTS[3] + 2.5, 0.6)]))


# ================================================================== 4: the sled arrives at the window: «Такси «Ямщик»…» — «Витёк?!»
def r_arrive(t, u):
    Z = 1.05
    cx, cy = 760.0, 450.0
    v = K.V('facade', cx, cy, Z)
    S = K.S_of(v, 'facade') * 0.85
    x = lerp(300.0, 560.0, glide(min(1.0, u / 1.2)))
    acts = team(t, v, x, 690.0, S, run=u < 1.2, rider=False)
    z = zhora_window(t, v, (-0.8, 0.0) if u > 1.0 else (0.9, -0.2), hand_n=(20.0, 50.0))
    def f(big, _):
        if u < 1.4:
            ox, oy = v.opt(x + 40, 690.0)
            K.puff(big, ox, oy, t, CUTS[4] + 1.1, n=20, seed=3, life=0.5, speed=420, px=12)
    return K.shot('facade', K.light_morning, cx, cy, Z, acts=[z] + acts, fx_=f, t=t, focus=0.7, dof_k=8, snow_n=55)


# ================================================================== 5: CU Витёк: «Ну. Город-то маленький.»
def r_small(t, u):
    Z = 2.6
    cx, cy = 540.0, 470.0
    v = K.V('facade', cx, cy, Z)
    kv, dv = face(FV, 'vitek', t, (0.0, 0.0), hand_n=(12.0, 50.0 + 2 * math.sin(t * 6)))
    vk = A(C.vitek, 530.0, 640.0 + dv, K.S_of(v, 'facade') * 0.85, t=t, post=hat_post, **kv); vk.near = 0.99
    return K.shot('facade', K.light_morning, cx, cy, Z, acts=[vk], focus=0.95, dof_k=28, t=t, snow_n=45)


# ================================================================== 6: the ride: «Вот это сервис! За три тыщи — с ветерком!»
def r_ride(t, u):
    L = CUTS[7] - CUTS[6]
    Z = 1.9
    x = lerp(300.0, 760.0, u / L)
    cx, cy = x + 40, 560.0
    v = K.V('yard', cx, cy, Z)
    S = K.WS['yard'] * 3 * v.Z * 1.25
    acts = team(t, v, x, 640.0, S, look_z=(0.9, -0.3))
    def f(big, _):
        ox, oy = v.opt(x - 60, 640.0)
        K.puff(big, ox, oy, t, t - (t * 6 % 0.17), n=10, seed=int(t * 6), life=0.35, speed=320, px=12)
        fx.speed_lines(big, t, 0.28)
    return K.shot('yard', K.light_morning, cx, cy, Z, acts=acts, fx_=f, t=t, focus=0.8, dof_k=6, snow_n=90, par=(-12 + 24 * u / L, 0))


# ================================================================== 7: TWIST — the dogs lie down: «Всё, братан, приехали. У собак обед…»
def r_twist(t, u):
    Z = 1.6
    x = 780.0
    cx, cy = x + 60, 560.0
    v = K.V('yard', cx, cy, Z)
    S = K.WS['yard'] * 3 * v.Z * 1.25
    acts = team(t, v, x, 640.0, S, run=False, lie=True, look_z=(-0.8, 0.0))
    return K.shot('yard', K.light_morning, cx, cy, Z, acts=acts, t=t, focus=0.8, dof_k=6, snow_n=60, kick=kick(t, [(TWIST, 1.1)]))


# ================================================================== 8: CU Жора in the sled: «В смысле?! Я ж три тысячи заплатил!»
def r_what(t, u):
    Z = 3.0
    x = 780.0
    v = K.V('yard', x - 4, 560.0, Z)
    S = K.WS['yard'] * 3 * v.Z * 1.25
    kw, dy = face(FZ, 'zhora', t, (-0.6, 0.0), sit=1.0, hand_n=(24.0, 62.0), hand_f=(-14.0, 60.0))
    k = S / (3 * v.Z)
    z = A(C.zhora, x - 4 * k, 640.0 - 8 * k + dy, S, t=t, **kw); z.near = 0.99
    sl = A(C.sled, x, 640.0, S * 2.2, t=t); sl.near = 0.99
    return K.shot('yard', K.light_morning, x - 4, 560.0, Z, acts=[sl, z], t=t, focus=0.9, dof_k=20, snow_n=50, kick=kick(t, [(27.6, 0.6)]))


# ================================================================== 9: Витёк sits in the sled, the dogs jump in: «Так три тысячи — это собакам…»
def r_sitin(t, u):
    Z = 1.6
    x = 780.0
    cx, cy = x, 560.0
    v = K.V('yard', cx, cy, Z)
    S = K.WS['yard'] * 3 * v.Z * 1.25
    k = S / (3 * v.Z)
    acts = team(t, v, x, 640.0, S, rider=False, musher=False, dogs_in=u > 1.0)
    kv, dv = face(FV, 'vitek', t, (0.9, 0.0), hand_n=(10.0, 44.0))
    vk = A(C.vitek, x - 6 * k, 640.0 - 8 * k + dv, S * 0.95, t=t, post=hat_post, **kv); vk.near = 0.99
    kz, _ = face(FZ, 'zhora', t, (-0.8, 0.0), hand_n=(22.0, 40.0))
    z = A(C.zhora, x + 46 * k, 644.0, S, t=t, flip=True, **kz); z.near = 0.99
    if u <= 1.0:                                                              # the dogs still lie in front
        for i in range(6):
            d = A(C.husky, x + (60 + (i // 2) * 30) * k, 640.0 + (i % 2) * 5 * k, S * 1.35, t=t, lie=True, run=False); d.near = 0.99
            acts.append(d)
    return K.shot('yard', K.light_morning, cx, cy, Z, acts=acts + [vk, z], t=t, focus=0.8, dof_k=6, snow_n=55)


# ================================================================== 10: Жора in the harness pulls everyone; the gull: «Я — чайка. А ты теперь — ездовой.»
def r_pull(t, u):
    L = CUTS[11] - CUTS[10]
    Z = 1.55
    x = lerp(700.0, 860.0, u / L)
    cx, cy = x + 50, 560.0
    v = K.V('yard', cx, cy, Z)
    S = K.WS['yard'] * 3 * v.Z * 1.25
    k = S / (3 * v.Z)
    acts = team(t, v, x, 640.0, S, rider=False, musher=False, dogs_in=True, puller=True)
    kv, dv = face(FV, 'vitek', t, (0.9, 0.0), hand_n=(12.0, 56.0 + 6 * math.sin(t * 8)))
    vk = A(C.vitek, x - 6 * k, 640.0 - 8 * k + dv, S * 0.95, t=t, post=hat_post, **kv); vk.near = 0.99
    kz, dz = face(FZ, 'zhora', t, (0.9, 0.0), walk=t * 9.0, lean=1.2, sweat=1.0, hand_n=(20.0, 40.0), hand_f=(-14.0, 42.0))
    z = A(C.zhora, x + 74 * k, 644.0 + dz, S, t=t, **kz); z.near = 0.99
    kc, _ = face(FC, 'chayka', t, (-0.4, 0.0))
    g = A(C.chayka, x + 110 * k, 520.0 + 10 * math.sin(t * 3), S * K.GULL * 1.2, t=t, flip=True, fly=True, **kc); g.near = 0.99
    def f(big, _):
        ax, ay = v.opt(x + 26 * k, 640.0 - 10 * k); bx, by = v.opt(x + 70 * k, 640.0 - 40 * k)
        for i in range(40):                                                    # the gang line from the sled to Жора's waist
            q = i / 39
            px, py = int(ax + (bx - ax) * q), int(ay + (by - ay) * q)
            big[py - 3:py + 3, px - 3:px + 3] = (200, 50, 60)
        ox, oy = v.opt(x + 74 * k, 646.0)
        K.puff(big, ox - 40, oy, t, t - (t * 4 % 0.25), n=6, seed=int(t * 4), life=0.3, speed=200, px=10)
    return K.shot('yard', K.light_morning, cx, cy, Z, acts=acts + [vk, z, g], fx_=f, t=t, focus=0.8, dof_k=6, snow_n=70)


# ================================================================== 11: the port gate: six huskies stare: «Оценочку, братан. Собаки смотрят.» — «Пять звёзд.»
def r_port(t, u):
    Z = 1.45
    cx, cy = 820.0, 470.0
    v = K.V('port', cx, cy, Z)
    S = K.WS['port'] * 3 * v.Z
    k = S / (3 * v.Z)
    acts = []
    for i in range(6):
        d = A(C.husky, 700.0 + i * 26 * k * 0.9, 640.0 + (i % 2) * 8, S * 1.35, t=t, stare=True, run=False, ph=i); d.near = 0.99
        acts.append(d)
    kv, dv = face(FV, 'vitek', t, (0.9, 0.0), hand_n=(12.0, 48.0))
    vk = A(C.vitek, 690.0, 640.0 + dv, S * 0.95, t=t, post=hat_post, **kv); vk.near = 0.99
    kz, dz = face(FZ, 'zhora', t, (-0.5, 0.4), hand_n=(18.0, 50.0), prop_n=C.phone, sweat=1.0, frost=0.6)
    z = A(C.zhora, 960.0, 650.0 + dz, S, t=t, flip=True, **kz); z.near = 0.99
    def f(big, _):
        if u > 0.4:
            sc = K.rating_screen(t, stars=5 if t > 42.0 else 0, t_star=42.0, w=420, h=560)
            O.overlay(big, sc, 600, 980 + int(5 * math.sin(t * 3)), 1.0)
    return K.shot('port', K.light_morning, cx, cy, Z, acts=[vk] + acts + [z], fx_=f, t=t, focus=0.8, dof_k=8, snow_n=55)


R = [r_gull, r_reveal, r_phone, r_order, r_arrive, r_small, r_ride, r_twist, r_what, r_sitin, r_pull, r_port]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 4, ['ТАКСИ —', '3000?!'], hook_t=(0.10, 2.4), hook_y=230, hook_size=84,
              stickers=[(K.st('АВТОБУС — В АПРЕЛЕ', fg=(255, 255, 255), size=44), 2.0, 4.0, 540, 1250),
                        (K.st('ОБЕД!', fg=(255, 110, 150), size=72), TWIST + 0.1, TWIST + 2.4, 540, 380),
                        (K.st('×7', fg=(255, 80, 80), size=80), CUTS[2] + 0.5, CUTS[2] + 1.6, 820, 420)],
              flashes=[TWIST, CUTS[1]], mosaics=[CUTS[6]],
              cap_y={0: 1480, 1: 1460, 2: 1700, 3: 1500, 4: 1460, 5: 1500, 6: 1460, 7: 1460, 8: 1480, 9: 1460, 10: 1460, 11: 820})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
