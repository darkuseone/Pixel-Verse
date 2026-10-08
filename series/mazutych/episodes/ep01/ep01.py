"""S01E01 «Кто крайний?» (v3, 09.10.2026: hook outcry «Где бензин?!» = text hook, twist 17.4 s / 58 %, 30.2 s; the wheel visibly talks) — there is no gasoline anywhere. Мазутыч tows his dead «six» to the АЗС «ГАЗПРОПАЛ»
with his monowheel. «Бензина нет.» — «Я — нефтяник!» — «А я — балерина.» Then the tanker truck arrives... and joins the queue:
«Мужики, кто крайний?» It is empty, its driver has not filled up since spring. Finale: the monowheel dies, Мазутыч and the driver
haul the tanker like the Volga barge haulers. «А я его вожу.» — «А я — балерина!»
Heroes: props/mazcast.py in the «Мазутная гравюра» manner (props/mazpix.py); kit: props/mazkit.py.
  python3 ep01.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paths as P
import stage as ST
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
from episode import Episode
from props import mazpix as MX
from props import mazcast as MC
from props import mazkit as K
from props import bytfx as B
from props import mazshots as M
from timeline import DUR, FPS, VOICE, SLUG, CUTS

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
HW = K.world('highway_azs')
WIN = K.world('azs_window')


def mouth(who, t, k=1.8):
    return min(1.0, talk(who, t) * k)


def A(fn, wx, wy, s, flip=False, pin=None, **kw):
    return MX.Act(fn, wx, wy, s_=s, flip=flip, pin=pin, **kw)


def wpt(v, ox, oy):
    """output px -> world px"""
    return v.X0 + ox / (3 * v.Z), v.Y0 + (oy / 3 - v.oy) / v.Z


def aout(act, v, name):
    """output px of a named sprite anchor of an actor that has been drawn"""
    sp = act.last
    px, py = sp.anchors[name]
    ox, oy = v.opt(act.wx, act.wy)
    sc = act.scale(v)
    if act.pin:
        qx, qy = sp.anchors[act.pin]
        ox -= (-qx if act.flip else qx) * sc; oy += qy * sc
    return ox + (-px if act.flip else px) * sc, oy - py * sc


def rope(big, a, b, sag=40, w=10, col=(206, 172, 110)):
    """a thick rope with a little sag between two output points"""
    (x0, y0), (x1, y1) = a, b
    n = int(max(abs(x1 - x0), abs(y1 - y0)) / 4) + 2
    pts = []
    for i in range(n + 1):
        q = i / n
        pts.append((x0 + (x1 - x0) * q, y0 + (y1 - y0) * q + sag * 4 * q * (1 - q)))
    for pad, colf in ((3, lambda i: MX.INK), (0, lambda i: col if (i // 3) % 2 else (176, 140, 84))):
        for i, (x, y) in enumerate(pts):
            xa, ya = int(x - w / 2) - pad, int(y - w / 2) - pad
            xb, yb = xa + w + 2 * pad, ya + w + 2 * pad
            if xb > 0 and yb > 0 and xa < OUT_W and ya < OUT_H:
                big[max(0, ya):min(OUT_H, yb), max(0, xa):min(OUT_W, xb)] = colf(i)


# highway lanes (the road slopes down to the right)
def y_far(x): return 548.0 + 0.0625 * x
def y_near(x): return 590.0 + 0.0625 * x
def y_sh(x): return 618.0 + 0.0625 * x            # the shoulder where Мазутыч rides


SP = 4.2                                           # Мазутыч: output px per sprite px at Z = 1
CAR = 6.0
TRK = 7.0
QUEUE = [(450, 'lada', 0), (570, 'buh', 1), (690, 'lada', 2), (800, 'lada', 3), (905, 'lada', 5)]
TK_X = 92.0                                        # where the tanker stops: right behind the last car (the one «since May»)
JOY = (16.1, 17.4)


def queue_acts(t, Z, honk=0.0):
    acts = []
    for i, (x, kind, c) in enumerate(QUEUE):
        b = (abs(math.sin(t * 30 + i)) * 1.5 if honk > 0 else 0.0)
        y = y_far(x) - b
        if kind == 'lada':
            last = i == 0
            acts.append(A(MC.lada, x, y, CAR * Z, col=MC.CAR_COLS[c], rust=i + 1, web=last, sign='С МАЯ' if last else None))
        else:
            acts.append(A(MC.buhanka, x, y, CAR * Z))
    return acts


def honk_k(t):
    return 1.0 if any(a <= t < a + 1.2 for a in (3.6, 16.3)) else 0.0


def wheel_k(t):
    """how hard the wheel «talks»: voice envelope, never below 0.5 while its line plays (waves: mazkit.shot)"""
    on = any(spk == 'wheel' and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in VOICE)
    return max(mouth('wheel', t, 1.6), 0.5 if on else 0.0)


def maz_act(t, x, y, Z, s=None, **kw):
    kw.setdefault('t', t)
    kw.setdefault('mouth_', mouth('maz', t))
    kw.setdefault('wheel_talk', wheel_k(t))
    return A(MC.maz, x, y, s or SP * Z, **kw)


def dof(big, r=6):
    return np.array(Image.fromarray(big).filter(ImageFilter.GaussianBlur(r)))


def sparks(big, ox, oy, t, n=18, spread=220):
    r = np.random.default_rng(int(t * 30))
    for i in range(n):
        d = r.random() * spread; a = r.random()
        px, py = int(ox - 20 - d), int(oy - 6 - a * 60 + d * 0.15)
        if 0 <= px < OUT_W - 12 and 0 <= py < OUT_H - 12: big[py:py + 12, px:px + 12] = (255, 220, 120) if i % 3 else (255, 140, 60)


# ================================================================== shots
def cu_maz(t, u, world=None, cx=420.0, cy=330.0, Z=1.45, s=17.0, head=(560, 980), wind=1.0, pan=40.0, bob=6.0, light=K.light_hw,
           blur=0, flare=(664, 205), extra_fx=None, **kw):
    """close-up of Мазутыч: the head pinned at an output point; background zoomed less (CU_BG rule) and optionally soft"""
    world = HW if world is None else world
    v0 = view_at(world, cx + pan * u, cy, Z, 180, 320)
    hx, hy = wpt(v0, head[0], head[1] + bob * math.sin(t * 8.0))
    kw.setdefault('mouth_', mouth('maz', t, 1.6))
    kw.setdefault('wheel_talk', wheel_k(t))
    a = A(MC.maz, hx, hy, s, pin='head', t=t, wind=wind, **kw)
    def pre(big, v):
        if flare: K.flare(big, v, t, flare[0], flare[1], 1.0, 0.6)
        if blur: big[:] = dof(big, blur)
    def f(big, v):
        if extra_fx: extra_fx(big, v, a)
    big = K.shot(world, light, cx + pan * u, cy, Z, acts=[a], pre=pre, fx_=f, sx=180, sy=320)
    if wind: K.wind_lines(big, t, 0.4 * wind)
    return big


def r_hook(t, u):
    """0.0: his face straining, sweat flying, a rope over the shoulder pulled taut out of frame"""
    def f(big, v, a):
        bx, by = aout(a, v, 'belt')
        rope(big, (bx, by), (-60, by + 260), sag=-20, w=16)
    big = cu_maz(t, u, expr='strain', sweat=1.0, wind=0.8, pan=12.0, bob=10.0, rot=-6.0, extra_fx=f, beacon=True)
    B.shake(big, t, 5, 26)
    return big


def tow_group(t, x, Z, expr='strain', lean=-12.0):
    """Мазутыч on the monowheel towing the dead «six» on a rope; returns (acts, fx) for a highway shot"""
    car_x = x - 150.0
    car = A(MC.lada, car_x, y_sh(car_x) - 2 + 0.6 * abs(math.sin(t * 7)), CAR * Z, col=(232, 228, 214), driver=False, spin=-t * 4)
    m = maz_act(t, x, y_sh(x), Z, expr=expr, wind=0.5, spin=t * 22, rot=lean, sweat=1.0, beacon=True, shadow=0.3)
    def f(big, v):
        rope(big, aout(m, v, 'belt'), aout(car, v, 'front'), sag=18, w=10)
        ox, oy = v.opt(x, y_sh(x))
        sparks(big, ox, oy, t, 14, 160)
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
    return [car, m], f


def r_reveal(t, u):
    """fast pull-back: the monowheel is towing a whole car"""
    k = sm(min(1.0, u / 0.7))
    Z = lerp(2.4, 1.1, k)
    x = 330.0 + 26.0 * u
    acts, f = tow_group(t, x, Z)
    return K.shot(HW, K.light_hw, x - lerp(10.0, 50.0, k), lerp(470.0, 520.0, k), Z, acts=acts, fx_=f, sx=180, sy=380)


def r_queue(t, u):
    """crossing along the queue: the last car is covered in cobwebs, «С МАЯ»"""
    Z = 1.15
    x = 250.0 + 40.0 * u
    acts, f = tow_group(t, x, Z)
    acts = queue_acts(t, Z, honk_k(t)) + acts
    return K.shot(HW, K.light_hw, lerp(330.0, 420.0, u / 1.5), 470.0, Z, acts=acts, fx_=f, sx=180, sy=330)


def r_sign(t, u):
    def f(big, v): K.flare(big, v, t, 664, 205, 1.0, 0.6)
    return K.shot(HW, K.light_hw, 1098.0, 230.0, 1.5 + 0.08 * u, fx_=f, sx=180, sy=330)


def zoya_shot(t, u, who='zoya', mega=False, Z0=1.45, push=0.05, gum=0.0, expr='bored', look=(0.3, 0.0), pose='desk'):
    Z = Z0 + push * u
    s = 4.0 * 3 * Z
    a = A(MC.zoya, 600.0, 470.0, s, t=t, mega=mega, mouth_=mouth(who, t, 1.7), gum=gum, expr=expr, look=look, pose=pose)
    big = K.shot(WIN, K.light_win, 618.0, 300.0, Z, acts=[a], sx=180, sy=300)
    v = view_at(WIN, 618.0, 300.0, Z, 180, 300)
    xs, ys = v.grid()
    orig = v.bg()
    m = ((ys[:, None] >= 450) & (ys[:, None] <= 510)) & ((xs[None, :] >= 556) & (xs[None, :] <= 708))
    big[m] = orig[m]
    gl = ((ys[:, None] >= 92) & (ys[:, None] <= 520)) & ((xs[None, :] >= 226) & (xs[None, :] <= 1012))
    yy, xx = np.mgrid[0:OUT_H, 0:OUT_W]
    streak = (((xx + yy * 0.8 + 140) % 620) < 46) & gl
    big[streak] = (big[streak] * 0.72 + np.array([255, 236, 210]) * 0.28).astype(np.uint8)
    return big


def r_nogas(t, u):
    return zoya_shot(t, u, gum=sm((t - 7.35) / 0.2) * 0.8)


def r_badge(t, u):
    big = cu_maz(t, u, cx=900.0, cy=330.0, Z=1.45, s=15.5, head=(470, 900), wind=0.2, pan=0.0, bob=0.0, expr='proud', card=True,
                 look=(1.0, 0.0), beacon=True)
    if 0.05 < u < 0.3: B.shake(big, t, 9, 30)
    return big


def r_ballet(t, u):
    return zoya_shot(t, u, Z0=1.35, push=0.08, pose='ballet', expr='bored', look=(1.0, 0.0))


def r_point(t, u):
    return zoya_shot(t, u, Z0=1.4, push=0.03, pose='point', expr='bored', look=(1.0, 0.0))


def r_flare(t, u):
    """«там»: the refinery flare roars on the horizon"""
    def f(big, v):
        K.flare(big, v, t, 664, 205, 2.2, 1.0)
    return K.shot(HW, K.light_hw, 664.0, 260.0, 2.4 + 0.2 * u, fx_=f, sx=180, sy=360)


def r_awe(t, u):
    """the horn: he turns, tears of joy, the choir"""
    big = cu_maz(t, u, cx=900.0, cy=330.0, Z=1.45, s=16.0 + 1.5 * u, head=(560, 960), wind=0.3, pan=0.0, bob=0.0,
                 expr='joy', look=(-1.0, 0.2), beacon=True)
    k = 0.6 + 0.4 * math.sin(t * 20)
    fx.glow(big, 300, 600, 420 * k, (255, 230, 160), 0.25)
    for (cx, cy, r) in ((760, 860, 40), (300, 700, 30), (860, 600, 24)):
        r = int(r * k)
        big[cy - 5:cy + 5, cx - r:cx + r] = (255, 250, 220); big[cy - r:cy + r, cx - 5:cx + 5] = (255, 250, 220)
    return big


def tanker_x(t):
    return lerp(-260.0, TK_X, sm(min(1.0, (t - JOY[0]) / 1.2)))


def r_arrive(t, u):
    """the tanker rolls in — the whole queue honks with joy... and it stops at the END of the queue"""
    Z = 0.95
    tx = tanker_x(t)
    acts = [A(MC.tanker, tx, y_far(tx + 140), TRK * Z, t=t, spin=-t * 14 * (1 - sm(u / 1.2)), bounce=0.4 * abs(math.sin(t * 9)))]
    acts = acts + queue_acts(t, Z, 1.0)
    def f(big, v):
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
        K.exhaust(big, v, t, tx + 155, y_far(tx) - 120)
    big = K.shot(HW, K.light_hw, 285.0, 440.0, Z, acts=acts, fx_=f, sx=180, sy=330)
    K.confetti(big, t, JOY[0] + 0.25, n=70, seed=3)
    return big


def cab_pos():
    """world point of the tanker's cab window (the tanker parked at TK_X)"""
    return TK_X + 86 * TRK / 3, y_far(TK_X + 140) - 35 * TRK / 3


def tolik_window(t, Z, look=(1.0, 0.0)):
    wxw, wyw = cab_pos()
    return A(MC.tolik, wxw - 4.0, wyw + 10 + 44 * SP / 3, SP * Z, t=t, lean=True, wave=1.0, mouth_=mouth('tolik', t), clip=34.0, expr='grin',
             look=look)


def r_twist(t, u):
    """close on the cab: Толик leans out of the window — «Мужики, кто крайний?»"""
    Z = 2.2 + 0.06 * u
    tank = A(MC.tanker, TK_X, y_far(TK_X + 140), TRK * Z, t=t)
    wxw, wyw = cab_pos()
    return K.shot(HW, K.light_hw, wxw + 20.0, wyw - 10.0, Z, acts=[tank, tolik_window(t, Z)], sx=180, sy=380)


def r_react(t, u):
    return cu_maz(t, u, cx=700.0, cy=330.0, Z=1.45, s=16.0, head=(540, 960), wind=0.0, pan=0.0, bob=0.0, expr='deadpan', look=(0.0, -0.3))


def r_knock(t, u):
    """he knocks on the tank: hollow «БО-ОМ»; Толик from the window: «Пустой.»"""
    Z = 1.75
    knock = 0.1 < u < 0.7
    tank = A(MC.tanker, TK_X, y_far(TK_X + 140), TRK * Z, t=t)
    tol = tolik_window(t, Z, look=(-1.0, 0.0))
    mx = 210.0
    m = maz_act(t, mx, y_sh(mx) + 8, Z, flip=True, expr='deadpan' if u > 0.7 else 'squint', blinker=1.0 if knock else 0.0,
                look=(1.0, 0.0), shadow=0.3)
    def f(big, v):
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
        if 0.12 < u < 1.2:
            hx, hy = aout(m, v, 'hand')
            for i in range(3):
                ph = (u - 0.12) * 1.6 - i * 0.18
                if 0 < ph < 1:
                    r = int(40 + 220 * ph); a = 1 - ph
                    yy, xx = np.ogrid[-r:r + 1, -r:r + 1]
                    ring = (np.abs(np.sqrt(xx * xx + yy * yy) - r) < 6)
                    ys, xs = np.nonzero(ring)
                    ys = ys + int(hy - r); xs = xs + int(hx - 30 - r)
                    ok = (ys >= 0) & (ys < OUT_H) & (xs >= 0) & (xs < OUT_W)
                    big[ys[ok], xs[ok]] = (big[ys[ok], xs[ok]] * (1 - 0.7 * a) + np.array([255, 240, 200]) * 0.7 * a).astype(np.uint8)
    big = K.shot(HW, K.light_hw, 230.0, 470.0, Z, acts=[tank, tol, m], fx_=f, sx=180, sy=360)
    if 0.12 < u < 0.3: B.shake(big, t, 7, 30)
    return big


def lcd(big, t, y0=0, y1=OUT_H // 2, pct='0%', dead=False):
    """the wheel display insert: battery, sad face; goes black when dead"""
    big[y0:y1] = (16, 18, 22)
    big[y0 + 40:y1 - 40, 60:OUT_W - 60] = (40, 44, 52)
    sx0, sy0, sx1, sy1 = 120, y0 + 100, OUT_W - 120, y1 - 100
    big[sy0:sy1, sx0:sx1] = (14, 40, 46) if not dead else (6, 8, 10)
    if dead:
        big[(sy0 + sy1) // 2 - 3:(sy0 + sy1) // 2 + 3, OUT_W // 2 - 40:OUT_W // 2 + 40] = (200, 220, 230)
        return big
    yy = np.arange(sy0, sy1)[:, None]
    big[sy0:sy1, sx0:sx1][((yy - sy0) % 9 < 2).repeat(sx1 - sx0, 1)] = (10, 30, 34)
    on = int(t * 4) % 2 == 0
    red = (255, 70, 60) if on else (150, 40, 40)
    bx0, by0 = 200, sy0 + 90
    big[by0:by0 + 200, bx0:bx0 + 420] = red; big[by0 + 16:by0 + 184, bx0 + 16:bx0 + 404] = (14, 40, 46)
    big[by0 + 60:by0 + 140, bx0 + 420:bx0 + 460] = red
    img = Image.fromarray(big[sy0:sy1, sx0:sx1]); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text((560, 120), pct, font=O.pfont(120), fill=red)
    d.text((120, 340), 'ДИН-ДОН 3000', font=O.pfont(40), fill=(90, 230, 255))
    big[sy0:sy1, sx0:sx1] = np.array(img)
    fxo, fyo = 820, sy0 + 330                                                           # sad pixel face
    for dx in (-40, 40): big[fyo:fyo + 30, fxo + dx:fxo + dx + 22] = (90, 230, 255)
    big[fyo + 50:fyo + 62, fxo - 30:fxo + 52] = (90, 230, 255)
    big[fyo + 62:fyo + 74, fxo - 42:fxo - 30] = (90, 230, 255); big[fyo + 62:fyo + 74, fxo + 52:fxo + 64] = (90, 230, 255)
    return big


def r_battery(t, u):
    dead = t > 25.6
    big = cu_maz(t, u, cx=640.0, cy=360.0, Z=1.45, s=15.5, head=(560, 1480 + 40 * sm((t - 25.3) / 0.4)), wind=0.0, pan=0.0, bob=0.0,
                 expr='sad', dead=dead, wheel_face='low')
    lcd(big, t, 0, 900, '0%', dead)
    if not dead: M.lcd_talk(big, 170, 600, 910, 770, t, wheel_k(t))      # the display «speaks»
    big[900:930] = MX.INK
    return big


def r_haul(t, u):
    """finale: Мазутыч and Толик haul the tanker by ropes like the Volga barge haulers, into the sunset"""
    Z = 1.3
    w = u * 5.0
    tx = 60.0 + 34.0 * u
    tank = A(MC.tanker, tx, y_near(tx + 140), TRK * Z, t=t, spin=-t * 2)
    xm = tx + 385.0; xt = tx + 325.0
    m = maz_act(t, xm, y_sh(xm), Z, pull=True, walk=w, expr='strain', sweat=1.0, rot=-24.0, mouth_=0.0, wind=0.2, shadow=0.3)
    tl = A(MC.tolik, xt, y_sh(xt) - 6, SP * Z, t=t, pull=True, walk=w + 1.6, expr='grin', mouth_=mouth('tolik', t), rot=-20.0, look=(1.0, 0.0))
    def f(big, v):
        front = aout(tank, v, 'front')
        rope(big, aout(m, v, 'shoulder'), front, sag=30, w=10)
        rope(big, aout(tl, v, 'shoulder'), (front[0], front[1] - 10), sag=24, w=10)
        K.flare(big, v, t, 664, 205, 1.3, 0.6)
        K.dust_trail(big, v, t, xm - 10, y_sh(xm) - 4)
    return K.shot(HW, K.light_hw, tx + 362.0, 520.0, Z, acts=[tank, tl, m], fx_=f, sx=180, sy=380)


def r_callback(t, u):
    return zoya_shot(t, u, who='zoyam', mega=True, Z0=1.45, push=0.06, expr='bored', look=(1.0, 0.0))


SHOTS = [r_hook, r_reveal, r_queue, r_sign, r_nogas, r_badge, r_ballet, r_point, r_flare, r_awe, r_arrive, r_twist, r_react, r_knock,
         r_battery, r_haul, r_callback]
NAMES = ['hook', 'reveal', 'queue', 'sign', 'nogas', 'badge', 'ballet', 'point', 'flare', 'awe', 'arrive', 'twist', 'react', 'knock',
         'battery', 'haul', 'callback']
CAP = dict(reveal=1080, haul=1080, nogas=1640, ballet=1640, point=1640, callback=1640, battery=1720, queue=1600, twist=1560)

SHOW = K.Show(EPI, 1, ['ГДЕ', 'БЕНЗИН?!'], hook_t=(0.10, 2.4), hook_y=120, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('БИИП!', (255, 236, 120)), 3.65, 4.7, 760, 1150),
                        (K.st('ПУСТОЙ', (255, 90, 90), 70), 20.6, 22.9, 700, 420)],
              flashes=[16.1, 25.85], mosaics=[19.35])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
