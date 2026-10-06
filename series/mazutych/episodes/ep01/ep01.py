"""S01E01 «Круговорот» — Мазутыч 25 years makes gasoline but cannot fill up anywhere. He rides his monowheel (holding a Lada steering
wheel) past the queue at АЗС «ЛУК-ОЙ», chases the tanker truck that leaves the refinery... and the truck drives back into the same
gate: the plan grows to 141 %. «Двадцать пять лет делаю бензин... Один и тот же.»
Heroes: props/mazcast.py in the «Мазутная гравюра» manner (props/mazpix.py); kit: props/mazkit.py.
  python3 ep01.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageFilter
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
from timeline import DUR, FPS, VOICE, SLUG, CUTS

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
HW = K.world('highway_azs')
GATE = K.world('refinery_gate')
WIN = K.world('azs_window')
TRUCK_GO = 0
PCT = 140


def mouth(who, t, k=1.8):
    return min(1.0, talk(who, t) * k)


def A(fn, wx, wy, s, flip=False, pin=None, **kw):
    return MX.Act(fn, wx, wy, s_=s, flip=flip, pin=pin, **kw)


def wpt(v, ox, oy):
    """output px -> world px"""
    return v.X0 + ox / (3 * v.Z), v.Y0 + (oy / 3 - v.oy) / v.Z


# highway lanes (the road slopes down to the right)
def y_far(x): return 548.0 + 0.0625 * x
def y_near(x): return 590.0 + 0.0625 * x
def y_sh(x): return 618.0 + 0.0625 * x            # the shoulder where Мазутыч rides


SP = 4.2                                           # Мазутыч: output px per sprite px at Z = 1 (= one background px per sprite px)
CAR = 6.0                                          # cars / truck are drawn bigger than the (big-headed) hero
TRK = 7.0
QUEUE = [(40, 'lada', 0), (175, 'buh', 1), (300, 'lada', 2), (430, 'lada', 3), (560, 'buh', 4), (690, 'lada', 5), (815, 'lada', 1)]


def queue_acts(t, Z, honk=0.0):
    acts = []
    for i, (x, kind, c) in enumerate(QUEUE):
        b = (abs(math.sin(t * 30 + i)) * 1.2 if honk > 0 else 0.0)
        y = y_far(x) - b
        if kind == 'lada':
            acts.append(A(MC.lada, x, y, CAR * Z * 0.92, col=MC.CAR_COLS[c], rust=i + 1))
        else:
            acts.append(A(MC.buhanka, x, y, CAR * Z * 0.92))
    return acts


def honk_k(t):
    return 1.0 if any(a <= t < a + 1.2 for a in (3.7, 14.2, 18.15)) else 0.0


def maz_act(t, x, y, Z, s=None, **kw):
    kw.setdefault('t', t)
    kw.setdefault('mouth_', mouth('maz', t))
    return A(MC.maz, x, y, s or SP * Z, **kw)


def hw_fx(t, k_wind=0.0, flare_k=1.0):
    def f(big, v):
        K.flare(big, v, t, 664, 205, flare_k, 0.6)
        if k_wind: K.wind_lines(big, t, k_wind)
    return f


def dof(big, r=6):
    return np.array(Image.fromarray(big).filter(ImageFilter.GaussianBlur(r)))


# ================================================================== shots
def cu_maz(t, u, world=None, cx=420.0, cy=330.0, Z=1.45, s=17.0, head=(560, 980), wind=1.0, pan=40.0, bob=6.0, light=K.light_hw,
           blur=0, conf=0, flare=(664, 205), **kw):
    """close-up of Мазутыч: the head pinned at an output point; background zoomed less (CU_BG rule) and optionally soft"""
    world = HW if world is None else world
    v0 = view_at(world, cx + pan * u, cy, Z, 180, 320)
    hx, hy = wpt(v0, head[0], head[1] + bob * math.sin(t * 8.0))
    kw.setdefault('mouth_', mouth('maz', t, 1.6))
    a = A(MC.maz, hx, hy, s, pin='head', t=t, wind=wind, confetti=conf, **kw)
    def pre(big, v):
        if flare: K.flare(big, v, t, flare[0], flare[1], 1.0, 0.6)
        if blur: big[:] = dof(big, blur)
    big = K.shot(world, light, cx + pan * u, cy, Z, acts=[a], pre=pre, sx=180, sy=320)
    if wind: K.wind_lines(big, t, 0.5 * wind)
    return big


def r_hook(t, u):
    big = cu_maz(t, u, expr='deadpan', wind=1.0)
    if t < 0.25: B.shake(big, t, 10 * (1 - t / 0.25), 30)
    return big


def r_cross(t, u):
    """wide crossing: he rolls in from the left past the queue, the camera ends on «БЕНЗИНА НЕТ»"""
    Z = 1.15
    k = u / (CUTS[2] - CUTS[1])
    cx = lerp(420.0, 1075.0, sm(k))
    x = lerp(300.0, 930.0, k)
    acts = queue_acts(t, Z, honk_k(t)) + [maz_act(t, x, y_sh(x), Z, expr='deadpan', wind=0.6, spin=t * 12, shadow=0.3)]
    def f(big, v):
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
        K.dust_trail(big, v, t, x - 10, y_sh(x) - 4)
    cy = lerp(455.0, 392.0, sm((k - 0.62) / 0.38))                 # tilt up to the sign at the end
    return K.shot(HW, K.light_hw, cx, cy, Z, acts=acts, fx_=f, sx=180, sy=330)


def zoya_shot(t, u, mega=True, Z0=1.45, push=0.05, gum=0.0, expr='bored', look=(0.3, 0.0)):
    Z = Z0 + push * u
    s = 4.0 * 3 * Z
    a = A(MC.zoya, 600.0, 470.0, s, t=t, mega=mega, mouth_=mouth('zoya', t, 1.7), gum=gum, expr=expr, look=look)
    big = K.shot(WIN, K.light_win, 618.0, 300.0, Z, acts=[a], sx=180, sy=300)
    # put the glass back in front of her: speaking grille + tray restored from the background, light reflections
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


def r_zoya(t, u):
    return zoya_shot(t, u, mega=True)


def gate_world(open_k=0.0):
    """refinery gate with the two leaves slid apart by open_k (0 shut .. 1 open), dark yard behind"""
    W = GATE.copy()
    if open_k <= 0: return W
    x0, x1, y0, y1, mid = 462, 838, 392, 556, 650
    left = GATE[y0:y1, x0:mid].copy(); right = GATE[y0:y1, mid:x1].copy()
    yy = np.linspace(0, 1, y1 - y0)[:, None, None]
    inside = (np.array([22, 16, 30]) * (1 - yy) + np.array([60, 44, 50]) * yy).astype(np.uint8)
    W[y0:y1, x0:x1] = inside
    for px in range(x0 + 20, x1, 46):                                                   # lit pipes and columns in the yard
        W[y0:y1 - 50, px:px + 10] = (96, 60, 50); W[y0:y1 - 50, px + 7:px + 10] = (230, 140, 70)
    W[y0 + 26:y0 + 34, x0:x1] = (110, 70, 56); W[y0 + 26:y0 + 28, x0:x1] = (240, 160, 90)
    W[y1 - 50:y1, x0:x1] = (74, 62, 66)                                                 # yard asphalt
    for px in range(x0 + 10, x1, 40): W[y1 - 22:y1 - 18, px:px + 20] = (200, 180, 120)
    for lx in (x0 + 60, x0 + 200, x0 + 320): W[y0 + 6:y0 + 12, lx:lx + 14] = (255, 220, 140)   # yard lamps
    d = int((mid - x0) * open_k)
    lx0 = x0 - d
    W[y0:y1, max(380, lx0):max(380, lx0) + (mid - x0) - max(0, 380 - lx0)] = left[:, max(0, 380 - lx0):]
    rx0 = mid + d
    wr = min(x1 + 90, rx0 + (x1 - mid)) - rx0
    W[y0:y1, rx0:rx0 + wr] = right[:, :wr]
    return W


def r_gate_out(t, u):
    """the gate rolls open, the tanker truck drives out to the right"""
    ok = sm(min(1.0, u / 0.6))
    W = gate_world(ok)
    Z = 1.05
    tx = lerp(380.0, 980.0, sm(max(0.0, (u - 0.35) / 1.3)))
    acts = [A(MC.tanker, tx, 606.0, TRK * Z, t=t, spin=-t * 14, bounce=0.6 * abs(math.sin(t * 9)))]
    def pre(big, v):
        K.flare(big, v, t, 1105, 60, 1.2, 1.0)
        K.plan_banner(big, v, PCT)
    def f(big, v):
        K.exhaust(big, v, t, tx + 150, 470)
    big = K.shot(W, K.light_gate, 640.0, 400.0, Z, acts=acts, pre=pre, fx_=f, sx=180, sy=330)
    v = view_at(W, 640.0, 400.0, Z, 180, 330)
    xs, ys = v.grid()
    wall = v.bg()
    m = (xs[None, :] < 462) & (ys[:, None] > 300) & (ys[:, None] < 620)
    big[m] = wall[m]
    if u > 0.45 and u < 0.9: B.shake(big, t, 5, 30)
    return big


def r_eyes(t, u):
    """extreme close-up: his eyes widen, the tanker glints in them"""
    big = cu_maz(t, u, cx=520.0, cy=420.0, Z=1.45, s=26.0 + 2.0 * u, head=(470, 1220), wind=0.3, pan=10.0, bob=2.0, blur=7,
                 expr='stunned', look=(1.0, 0.1), blink=False, beacon=True)
    sp_x, sp_y = 640 + 2.0 * u * 10, 860
    k = 0.6 + 0.4 * math.sin(t * 20)
    for (dx, dy, r) in ((0, 0, 46), (-140, 18, 30)):
        cx, cy = int(sp_x + dx), int(sp_y + dy)
        big[cy - 6:cy + 6, cx - r:cx + r] = (255, 250, 220); big[cy - r:cy + r, cx - 6:cx + 6] = (255, 250, 220)
    fx.glow(big, sp_x, sp_y, 200 * k, (255, 170, 60), 0.35)
    return big


def r_turn(t, u):
    """medium: the tanker zooms past behind him; he cranks the steering wheel and clicks the «turn signal»"""
    Z = 1.6
    cx = 500.0 + 60 * u
    x = cx - 10
    tk = (u - 0.0) / 0.6
    acts = []
    if 0 <= tk <= 1.2:
        tx = lerp(cx - 420, cx + 420, tk)
        acts.append(A(MC.tanker, tx, y_near(tx), TRK * Z, t=t, spin=-t * 30))
    st_ = 0.55 * sm((u - 0.7) / 0.3)
    bl = 1.0 if 0.75 < u < 1.75 else 0.0
    acts.append(maz_act(t, x, y_sh(x) + 10, Z, expr='glare' if u > 0.6 else 'shock', wind=0.8, steer=st_, blinker=bl, beacon=u > 0.7,
                        spin=t * 14, look=(1.0, 0.0)))
    big = K.shot(HW, K.light_hw, cx, 560.0, Z, acts=acts, fx_=hw_fx(t, 0.5), sx=180, sy=300)
    if 0 <= tk <= 1: big[:] = np.clip(big * 0.92 + np.roll(big, 40, 1) * 0.08, 0, 255).astype(np.uint8)
    return big


def r_chase(t, u):
    """crossing chase: the truck ahead, Мазутыч behind, the queue flies by"""
    Z = 1.1
    cx = lerp(180.0, 700.0, u / 1.6)
    tx = cx + 110; x = cx - 60 + 8 * math.sin(t * 3)
    acts = queue_acts(t, Z, honk_k(t)) + [A(MC.tanker, tx, y_near(tx), TRK * Z, t=t, spin=-t * 30, bounce=0.5 * abs(math.sin(t * 13))),
                                          maz_act(t, x, y_sh(x) + 6, Z, expr='glare', wind=1.0, spin=t * 30, rot=-10.0, beacon=True)]
    def f(big, v):
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
        K.dust_trail(big, v, t, x - 8, y_sh(x) + 2)
        K.exhaust(big, v, t, tx + 2, y_near(tx) - 120)
        fx.speed_lines(big, t, 0.8)
    big = K.shot(HW, K.light_hw, cx, 470.0, Z, acts=acts, fx_=f, sx=180, sy=330)
    return big


def r_pothole(t, u):
    """low and close: the wheel drops into a pothole puddle and he flies over it"""
    Z = 1.7
    x = lerp(420.0, 700.0, u / 1.4)
    cx = x + 20
    j = max(0.0, min(1.0, (u - 0.35) / 0.7))
    hop = math.sin(j * math.pi) * 60 if 0 < j < 1 else 0.0
    rot = -18 * math.sin(j * math.pi) if 0 < j < 1 else 0.0
    acts = [maz_act(t, x, y_sh(x) + 8 - hop, Z, expr='shock' if 0 < j < 1 else 'glare', wind=1.0, spin=t * 30, rot=rot, beacon=True)]
    def f(big, v):
        if 0.30 < u < 1.2:
            for i in range(10):
                ph = (u - 0.30) * 1.4 + i * 0.03
                a = i * 0.6
                ox, oy = v.opt(500 + math.cos(a) * 60 * ph, y_sh(500) + 6 - math.sin(a * 0.7) * 120 * ph + 140 * ph * ph)
                B.puff(big, ox, oy, 20 * v.Z, max(0.0, 0.8 - ph), (170, 120, 200) if i % 2 else (120, 200, 230))
        fx.speed_lines(big, t, 0.6)
    big = K.shot(HW, K.light_hw, cx, 560.0, Z, acts=acts, fx_=f, sx=180, sy=330)
    if 0.55 < u < 0.8: B.shake(big, t, 10, 30)
    return big


def r_past_azs(t, u):
    """static wide on the station: the tanker shoots past without stopping"""
    Z = 1.1
    tx = lerp(600.0, 1500.0, u / 0.6)
    acts = queue_acts(t, Z, 1.0) + [A(MC.tanker, tx, y_near(tx), TRK * Z, t=t, spin=-t * 30)]
    def f(big, v):
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
        K.exhaust(big, v, t, tx, y_near(tx) - 120)
    return K.shot(HW, K.light_hw, 1010.0, 430.0, Z, acts=acts, fx_=f, sx=180, sy=330)


def r_mimo(t, u):
    return zoya_shot(t, u, mega=False, Z0=1.7, push=0.06, gum=sm((u - 0.6) / 0.35) * 0.9, look=(1.0, -0.1))


def lcd(big, t, y0=0, y1=OUT_H // 2):
    """the wheel display insert: battery 3 %, worried face"""
    h = y1 - y0
    big[y0:y1] = (16, 18, 22)
    big[y0 + 40:y1 - 40, 60:OUT_W - 60] = (40, 44, 52)
    sx0, sy0, sx1, sy1 = 120, y0 + 100, OUT_W - 120, y1 - 100
    big[sy0:sy1, sx0:sx1] = (14, 40, 46)
    yy = np.arange(sy0, sy1)[:, None]
    big[sy0:sy1, sx0:sx1][((yy - sy0) % 9 < 2).repeat(sx1 - sx0, 1)] = (10, 30, 34)       # scanlines
    on = int(t * 4) % 2 == 0
    red = (255, 70, 60) if on else (150, 40, 40)
    bx0, by0 = 200, sy0 + 90
    big[by0:by0 + 200, bx0:bx0 + 420] = red; big[by0 + 16:by0 + 184, bx0 + 16:bx0 + 404] = (14, 40, 46)
    big[by0 + 60:by0 + 140, bx0 + 420:bx0 + 460] = red
    big[by0 + 30:by0 + 170, bx0 + 30:bx0 + 52] = red                                         # 3 % sliver
    img = Image.fromarray(big[sy0:sy1, sx0:sx1]); from PIL import ImageDraw
    d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text((560, 120), '3%', font=O.pfont(120), fill=red)
    d.text((120, 340), 'ДИН-ДОН 3000', font=O.pfont(40), fill=(90, 230, 255))
    big[sy0:sy1, sx0:sx1] = np.array(img)
    # worried pixel face
    fxo, fyo = 820, sy0 + 330
    for dx in (-40, 40): big[fyo:fyo + 30, fxo + dx:fxo + dx + 22] = (90, 230, 255)
    big[fyo + 60:fyo + 72, fxo - 30:fxo + 52] = (90, 230, 255)
    big[fyo + 50:fyo + 62, fxo - 42:fxo - 30] = (90, 230, 255); big[fyo + 50:fyo + 62, fxo + 52:fxo + 64] = (90, 230, 255)
    big[fyo - 30:fyo - 6, fxo + 90:fxo + 102] = (120, 200, 255)                              # sweat drop
    return big


def r_battery(t, u):
    big = cu_maz(t, u, cx=640.0, cy=360.0, Z=1.45, s=15.5, head=(560, 1480), wind=1.0, pan=60.0, expr='glare', beacon=True)
    lcd(big, t, 0, 900)
    big[900:930] = MX.INK
    return big


def r_low(t, u):
    """low angle: wheel big in the foreground, sparks, he leans into it"""
    Z = 2.0
    x = lerp(600.0, 820.0, u)
    acts = [maz_act(t, x, y_sh(x) + 4, Z, expr='glare', wind=1.0, spin=t * 40, rot=-14.0, beacon=True, look=(1.0, 0.2))]
    def f(big, v):
        ox, oy = v.opt(x, y_sh(x) + 4)
        r = np.random.default_rng(int(t * 30))
        for i in range(26):
            a = r.random(); d = r.random() * 260
            px, py = int(ox - 30 - d), int(oy - 10 - a * 80 + d * 0.2)
            if 0 <= px < OUT_W - 12 and 0 <= py < OUT_H - 12: big[py:py + 12, px:px + 12] = (255, 220, 120) if i % 3 else (255, 140, 60)
        fx.speed_lines(big, t, 1.0)
        K.wind_lines(big, t, 1.0)
    return K.shot(HW, K.light_hw, x + 30, 560.0, Z, acts=acts, fx_=f, sx=180, sy=420)


def r_twist(t, u):
    """the tanker comes back from the right and drives into the same gate; the leaves close; Мазутыч rolls in and stops"""
    ck = 1.0 - sm(max(0.0, (u - 1.45) / 0.5))
    W = gate_world(ck)
    Z = 1.05
    tx = lerp(1350.0, 160.0, min(1.0, u / 1.5) ** 1.3)
    mx = lerp(1150.0, 770.0, sm(min(1.0, max(0.0, (u - 0.9) / 0.9))))
    ccx = lerp(980.0, 650.0, sm(min(1.0, u / 1.3)))
    acts = [A(MC.tanker, tx, 606.0, TRK * Z, flip=True, t=t, spin=t * 14)]
    if u > 0.9: acts.append(maz_act(t, mx, 640.0, Z * 1.05, flip=True, expr='stunned', wind=0.3, spin=-t * 10, look=(1.0, 0.0), shadow=0.3))
    def pre(big, v):
        K.flare(big, v, t, 1105, 60, 1.2, 1.0)
        K.plan_banner(big, v, PCT)
    big = K.shot(W, K.light_gate, ccx, 400.0, Z, pre=pre, acts=acts, sx=180, sy=330)
    v = view_at(W, ccx, 400.0, Z, 180, 330)
    xs, ys = v.grid()
    wall = v.bg()
    m = (xs[None, :] < 462) & (ys[:, None] > 300) & (ys[:, None] < 640)
    big[m] = wall[m]
    if ck < 1:                                                    # the leaves slide shut over the truck
        lv = (xs[None, :] >= 462) & (xs[None, :] <= 838) & (ys[:, None] >= 392) & (ys[:, None] < 556)
        cl = view_at(gate_world(ck), ccx, 400.0, Z, 180, 330).bg()
        gm = lv & (np.abs(cl.astype(int) - wall.astype(int)).sum(2) < 1)
        big[lv & ~gm] = cl[lv & ~gm]
    if 0.75 < u < 1.0: B.shake(big, t, 4, 30)
    return big


def r_banner(t, u):
    """close on the plan banner: 140 % flips to 141 %, confetti, the flare roars"""
    Z = 0.95 + 0.10 * u
    fk = sm((t - 25.45) / 0.35)
    def pre(big, v):
        K.flare(big, v, t, 1105, 60, 1.0 + 1.2 * sm((t - 25.8) / 0.6), 1.0)
        K.plan_banner(big, v, 141, fk if fk < 1 else 1.0)
    big = K.shot(GATE, K.light_gate, 650.0, 260.0, Z, pre=pre, sx=180, sy=360, vig=0.3)
    K.confetti(big, t, 25.8)
    if 25.4 < t < 25.9: B.shake(big, t, 6, 30)
    return big


def r_lookup(t, u):
    big = cu_maz(t, u, world=GATE, cx=720.0, cy=260.0, Z=1.45, s=17.0, head=(560, 1060), wind=0.0, pan=0.0, bob=0.0, light=K.light_gate,
                 flare=(1105, 60), expr='stunned', look=(0.3, 1.0), mouth_=0.0, conf=int(u * 6) + 1, beacon=True)
    K.confetti(big, t, 25.8, seed=9)
    return big


def r_dead(t, u):
    """medium at the gate: the wheel goes to sleep, he stays standing like a monument"""
    Z = 2.0
    dead = t > 30.3
    face = 'low' if not dead else 'smile'
    acts = [maz_act(t, 830.0, 640.0, Z * 1.05, flip=True, expr='deadpan', wind=0.0, dead=dead, wheel_face=face, confetti=7, look=(1.0, 0.0),
                    mouth_=0.0, shadow=0.3)]
    def pre(big, v):
        K.flare(big, v, t, 1105, 60, 1.5, 1.0)
        K.plan_banner(big, v, 141)
    big = K.shot(GATE, K.light_gate, 830.0, 520.0, Z, pre=pre, acts=acts, sx=180, sy=380)
    K.confetti(big, t, 25.8, n=60, seed=11)
    return big


def r_end(t, u):
    """the same close-up as the hook (loop), confetti on the hard hat, no wind: «Один и тот же.»"""
    big = cu_maz(t, u, world=GATE, cx=760.0, cy=300.0, Z=1.45, s=17.0 + 0.6 * u, head=(560, 980), wind=0.15, pan=4.0, bob=0.0,
                 light=K.light_gate, flare=(1105, 60), expr='deadpan' if t < 33.9 else 'sad', conf=5, look=(0.6, -0.2))
    return big


SHOTS = [r_hook, r_cross, r_zoya, r_gate_out, r_eyes, r_turn, r_chase, r_pothole, r_past_azs, r_mimo, r_battery, r_low, r_twist,
         r_banner, r_lookup, r_dead, r_end]
NAMES = ['hook', 'cross', 'zoya', 'gate', 'eyes', 'turn', 'chase', 'pothole', 'past', 'mimo', 'battery', 'low', 'twist', 'banner', 'lookup',
         'dead', 'end']
CAP = dict(zoya=1640, mimo=1640, battery=1720, cross=1560, banner=1560)

SHOW = K.Show(EPI, 1, ['НЕФТЯНИК', 'БЕЗ БЕНЗИНА'], hook_t=(0.10, 2.9), hook_y=130, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('БИИП!', (255, 236, 120)), 3.75, 5.3, 760, 1180),
                        (K.st('КРУГОВОРОТ', (90, 230, 255), 60), 23.5, 24.9, 540, 1150),
                        (K.st('+1%', (255, 90, 90), 80), 25.6, 27.1, 840, 560)],
              flashes=[8.85, 22.80], mosaics=[24.9])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
