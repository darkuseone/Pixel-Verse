"""S01E06 «Почётный нефтяник» — season finale. Factory hall, fanfare: «За двадцать пять лет — машина!» The cover slides off a red
«Веста-Шместа» with a gift bow; Мазутыч sobs «Своя!». Борис Борисыч: «Ключи. А бензин — по талону на талон.» The monowheel tows the
new car to «ГАЗПРОПАЛ» («Опять тонна, друга»). Зоя: «Бензин есть.» — the cardboard flips to «ЕСТЬ!», the choir. Twist: under the fuel
flap — a socket, sparks: «Это что? — Электричка. — А зарядка есть? — Зарядки нет.» Дин-Дон: «Я тоже ноль процент.» Button: Борис
Борисыч pops up in the kiosk: «Розетка — по талону.» Title: «СЕЗОН 2: ЗАРЯДКИ НЕТ». Loops into his first shout.
  python3 ep06.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
import fx
import overlays as O
import stage as ST
from stage import view_at, OUT_W, OUT_H, Light
from scene import sm, lerp
from episode import Episode
from props import mazcast as MC
from props import mazkit as K
from props import bytfx as B
from props import mazshots as M
from props.mazshots import A, wpt, aout, y_far, y_sh, SP, CAR
from timeline import DUR, FPS, VOICE, SLUG, CUTS

EPI = Episode('ep06', VOICE, DUR, FPS, colors=dict(K.COL, bossh=K.COL['boss']), slug=SLUG)
KIT = M.Kit(EPI)
HW, WIN = KIT.HW, KIT.WIN
mouth = KIT.mouth
HALL = K.world('assembly_hall')
PODIUM = (483, 386, 569, 488)                     # world rect of the podium (occludes Борис Борисыч)
STAGE_Y = 482.0                                   # stage floor (feet)
CAR_HX = 760.0                                    # the award car on the stage
PX_, PY_ = 1040.0, 520.0                          # the award car parked at the pumps
TWIST = CUTS[10]


def light_hall(v):
    spots = ((572, 210, 360, (255, 214, 140), 0.45), (696, 210, 360, (255, 214, 140), 0.45), (826, 210, 360, (255, 214, 140), 0.45))
    return Light(amb=(0.92, 0.84, 0.80), keys=K._keys(v, spots), rim=(1, -0.4, (255, 190, 110), 0.45), grad=(1.04, 0.86))


def occlude(big, v, rect):
    """restore the background inside a world rect (a foreground prop drawn in the bg covers the actors)"""
    xs, ys = v.grid()
    x0, y0, x1, y1 = rect
    m = ((ys[:, None] >= y0) & (ys[:, None] < y1)) & ((xs[None, :] >= x0) & (xs[None, :] < x1))
    big[m] = v.bg()[m]


def spots(big, v, t, k=1.0):
    for i, x in enumerate((572, 696, 826)):
        ox, oy = v.opt(x, 330)
        fx.glow(big, ox, oy, 300 * v.Z, (255, 220, 150), 0.18 * k * (0.85 + 0.15 * math.sin(t * 7 + i)))


def flashes(big, t, seed=1, n=3):
    """press camera flashes from the hall"""
    rng = np.random.default_rng(int(t * 6) + seed)
    if (int(t * 6) + seed) % 3: return
    for _ in range(n):
        x, y = rng.integers(80, OUT_W - 80), rng.integers(500, OUT_H - 300)
        fx.glow(big, int(x), int(y), 160, (255, 255, 240), 0.6)
        big[y - 4:y + 4, x - 40:x + 40] = (255, 255, 250); big[y - 40:y + 40, x - 4:x + 4] = (255, 255, 250)


def sign_board(big, v, state, k=1.0):
    """the cardboard over the price board (world 1156..1240 x 114..207): 'есть' / 'зарядки'; k 0..1 flips from the old text"""
    if state is None: return
    W_, H_ = 90, 96
    img = Image.new('RGBA', (W_, H_), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.polygon([(2, 6), (86, 2), (84, 92), (4, 95)], fill=(196, 160, 112), outline=(120, 90, 60))
    for x in (6, 76): d.rectangle([x, 0, x + 10, 4], fill=(220, 220, 200))
    if k < 0.5:
        K._text(d, (44, 34), 'БЕНЗИНА', 11, (196, 30, 36)); K._text(d, (44, 64), 'НЕТ', 22, (196, 30, 36))
    elif state == 'есть':
        K._text(d, (44, 30), 'БЕНЗИН', 12, (30, 140, 40)); K._text(d, (44, 62), 'ЕСТЬ!', 20, (30, 140, 40))
    else:
        K._text(d, (44, 30), 'ЗАРЯДКИ', 11, (196, 30, 36)); K._text(d, (44, 62), 'НЕТ', 22, (196, 30, 36))
    a = np.array(img)
    if 0 < k < 1:
        s = abs(math.cos(k * math.pi)); h = max(2, int(H_ * s))
        a2 = np.array(Image.fromarray(a).resize((W_, h), Image.NEAREST)); full = np.zeros_like(a); p = (H_ - h) // 2
        full[p:p + h] = a2; a = full
    a[..., 3] = (a[..., 3] > 127) * 255
    ST.blit_world(big, v, a, 1153, 112)


def nozzle(big, hx, hy, s=1.0, hose_from=None):
    """the fuel gun in his glove (output px) + the hose back to the pump"""
    if hose_from is not None:
        M.rope(big, hose_from, (hx, hy), sag=60, w=int(12 * s), col=(34, 34, 38))
    g = (60, 62, 70)
    x, y = int(hx), int(hy)
    q = int(10 * s)
    big[y - q:y + q, x - 3 * q:x + q] = g
    big[y - q // 2:y + q // 2, x + q:x + 5 * q] = (150, 150, 156)
    big[y + q:y + 3 * q, x - 2 * q:x - q] = g


# ================================================================== the hall
def car_hall(t, Z, cover=0.0, bow=1.0):
    return A(MC.vesta, CAR_HX, STAGE_Y - 6, CAR * Z, t=t, bow=bow)


def r_hook(t, u):
    """0.0: Борис Борисыч bellows into the microphone, confetti, flashes — «За двадцать пять лет — машина!»"""
    def f(big, v, a):
        hx, hy = aout(a, v, 'head')
        M.rope(big, (hx + 340, OUT_H + 40), (hx + 230, hy + 130), sag=-30, w=16, col=(40, 40, 46))   # gooseneck mic
        cx, cy = int(hx + 225), int(hy + 110)
        big[cy - 46:cy + 46, cx - 30:cx + 30] = (70, 70, 78)
        big[cy - 40:cy + 40, cx - 24:cx + 24] = (120, 120, 130)
        big[cy - 40:cy + 40:12, cx - 24:cx + 24] = (60, 60, 66)
    big = KIT.cu(MC.boss, 'bossh', t, u, HALL, 620.0, 360.0, sz=16.5 + 1.2 * u, head=(520, 1000), light=light_hall, flare=None,
                 expr='shout' if u < 2.2 else 'grin', pose='podium', look=(1.0, -0.1), extra_fx=f, blur=4)
    K.confetti(big, t, 0.0, n=170, seed=6)
    flashes(big, t, 2)
    if u < 0.25: B.shake(big, t, 8, 30)
    return big


def r_curtain(t, u):
    """the grey cover flies off: a red «Веста-Шместа» with a giant bow under three spotlights"""
    Z = 1.2
    k = sm(u / 0.45)
    car = car_hall(t, Z)
    m = KIT.maz_act(t, 905.0, STAGE_Y + 2, Z, flip=True, expr='awe', look=(1.0, 0.0), mouth_=0.0, beacon=True, shadow=0.3)
    def f(big, v):
        if k < 1:                                                   # the cover sheet rising off the car and flying away
            x0, y0 = v.opt(CAR_HX - 80, STAGE_Y - 96 - 420 * k)
            x1, y1 = v.opt(CAR_HX + 82 + 300 * k, STAGE_Y + 4 - 420 * k)
            im = Image.new('RGBA', (OUT_W, OUT_H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
            d.polygon([(x0, y1), (x0 + 30, y0 + 20), ((x0 + x1) / 2, y0), (x1 - 20, y0 + 30), (x1, y1),
                       ((x0 + x1) / 2, y1 - 20 * math.sin(t * 20))], fill=(120, 126, 140, 255), outline=(30, 20, 16, 255))
            a = np.array(im); msk = a[..., 3] > 0
            big[msk] = a[..., :3][msk]
        spots(big, v, t, 1.0 + 1.5 * k)
        cx, cy = v.opt(CAR_HX, STAGE_Y - 40)
        fx.glow(big, cx, cy, 420 * k, (255, 230, 160), 0.35 * k)
    big = K.shot(HALL, light_hall, 800.0, 420.0, Z, acts=[car, m], fx_=f, sx=180, sy=420)
    K.confetti(big, t, 2.9, n=120, seed=2)
    flashes(big, t, 4)
    return big


def r_cry(t, u):
    """Мазутыч, tears of joy streaming: «Двадцать пять лет... Своя!»"""
    def pre(big, v): spots(big, v, t, 1.4)
    big = KIT.cu(MC.maz, 'maz', t, u, HALL, 860.0, 360.0, sz=16.0 + 0.8 * u, head=(560, 940), light=light_hall, flare=None, pre_fx=pre,
                 expr='joy', look=(-1.0, 0.2), flip=True, beacon=True, blur=4)
    K.confetti(big, t, 2.9, n=90, seed=8)
    return big


def r_keys(t, u):
    """two-shot on the stage: the keys handed over, the car behind"""
    Z = 2.0
    car = car_hall(t, Z)
    boss = A(MC.boss, 700.0, STAGE_Y, SP * Z, t=t, pose='key', mouth_=mouth('bossh', t), expr='grin', look=(1.0, 0.0))
    m = KIT.maz_act(t, 815.0, STAGE_Y + 3, Z, flip=True, expr='joy', look=(1.0, -0.1), mouth_=0.0, beacon=True, shadow=0.3)
    def f(big, v):
        hx, hy = aout(boss, v, 'hand')
        x, y = int(hx + 18), int(hy + 10)
        big[y:y + 70, x:x + 14] = (240, 200, 70); big[y + 46:y + 52, x + 14:x + 30] = (240, 200, 70)   # the key
        big[y - 30:y + 6, x - 6:x + 20] = (240, 200, 70)
        tg = Image.new('RGBA', (120, 60), (0, 0, 0, 0)); d = ImageDraw.Draw(tg); d.fontmode = '1'
        d.rectangle([0, 0, 119, 59], fill=(255, 190, 210), outline=(30, 20, 16), width=4)
        d.text((12, 14), 'ТАЛОН', font=O.pfont(24), fill=(150, 30, 60))
        O.overlay(big, np.array(tg), x - 120, y - 20, 1.0)
        spots(big, v, t, 1.0)
    return K.shot(HALL, light_hall, 760.0, 410.0, Z, acts=[car, boss, m], fx_=f, sx=180, sy=440)


def r_bosscu(t, u):
    return KIT.cu(MC.boss, 'bossh', t, u, HALL, 620.0, 360.0, sz=17.0, head=(560, 940), light=light_hall, flare=None,
                  expr='smug', pose='stand', look=(1.0, 0.0), blur=4)


# ================================================================== the highway
def r_tow(t, u):
    """the monowheel tows the brand-new car to «ГАЗПРОПАЛ», the bow flapping"""
    Z = 1.2
    x = 330.0 + 130.0 * u / 2.65
    car_x = x - 160.0
    car = A(MC.vesta, car_x, y_sh(car_x) - 2 + 0.6 * abs(math.sin(t * 7)), CAR * Z, t=t, spin=-t * 4, bow=1.0)
    m = KIT.maz_act(t, x, y_sh(x), Z, expr='strain', wind=0.5, spin=t * 22, rot=-12.0, sweat=1.0, beacon=True, shadow=0.3, mouth_=0.0)
    def f(big, v):
        M.rope(big, aout(m, v, 'belt'), aout(car, v, 'front'), sag=18, w=10)
        ox, oy = v.opt(x, y_sh(x))
        M.sparks(big, ox, oy, t, 14, 160)
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
        K.dust_trail(big, v, t, x - 10, y_sh(x) - 4)
    return K.shot(HW, K.light_hw, x - 60.0, 520.0, Z, acts=KIT.queue_acts(t, Z) + [car, m], fx_=f, sx=180, sy=380)


def gum_pop(t, t0):
    return sm((t - t0 + 0.25) / 0.2) * (1 - sm((t - t0) / 0.05))


def r_zoya1(t, u):
    return KIT.zoya(t, u, gum=gum_pop(t, 15.25), look=(1.0, -0.1))


def r_sign(t, u):
    """the cardboard flips: «БЕНЗИН ЕСТЬ!», heavenly rays, the choir"""
    k = sm((u - 0.15) / 0.35)
    def f(big, v):
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
        sign_board(big, v, 'есть', k)
        if k > 0.5:
            x, y = v.opt(1198, 160)
            fx.glow(big, x, y, 520, (255, 240, 170), 0.45)
            for i in range(10):
                a = i * math.pi / 5 + t * 0.6
                for r in range(160, 900, 14):
                    px, py = int(x + math.cos(a) * r), int(y + math.sin(a) * r)
                    if 0 <= px < OUT_W - 6 and 0 <= py < OUT_H - 6 and (r // 14) % 3 == 0:
                        big[py:py + 6, px:px + 6] = (255, 240, 170)
    big = K.shot(HW, K.light_hw, 1150.0, 230.0, 1.5 + 0.1 * u, fx_=f, sx=180, sy=330)
    if 0.3 < u < 0.5: B.shake(big, t, 6, 30)
    return big


def r_awe(t, u):
    def f(big, v, a):
        fx.glow(big, 900, 300, 500, (255, 240, 170), 0.3 + 0.1 * math.sin(t * 12))
    return KIT.cu_maz(t, u, cx=900.0, cy=330.0, sz=16.0 + 1.5 * u, head=(540, 960), expr='awe', look=(1.0, -0.4), beacon=True, extra_fx=f)


def car_pumps(t, Z, flap=0.0, plug=False):
    return A(MC.vesta, PX_, PY_, CAR * Z, t=t, bow=0.0, flap=flap, plug=plug)


def r_flap(t, u):
    """he marches up with the fuel gun, pops the flap..."""
    Z = 2.0
    fl = sm((u - 0.55) / 0.3)
    car = A(MC.vesta, PX_ + 25.0, PY_, CAR * Z, t=t, bow=0.0, flap=fl)
    mx = lerp(890.0, 928.0, sm(u / 0.5))
    m = KIT.maz_act(t, mx, PY_ + 4, Z, expr='proud', look=(1.0, -0.2), mouth_=0.0, beacon=True, shadow=0.3)
    def f(big, v):
        hx, hy = aout(m, v, 'hand')
        nozzle(big, hx, hy, 1.0, hose_from=v.opt(1000, 450))
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
    return K.shot(HW, K.light_hw, 995.0, 450.0, Z, acts=[car, m], fx_=f, sx=180, sy=320)


def r_socket(t, u):
    """TWIST insert: under the flap — a socket. Sparks. The gun stops an inch away."""
    W_, H_ = OUT_W // 3, OUT_H // 3
    im = Image.new('RGB', (W_, H_), (196, 40, 44)); d = ImageDraw.Draw(im)
    for y in range(0, H_, 9): d.line([(0, y), (W_, y + 40)], fill=(176, 34, 40))      # engraving hatch on the paint
    d.rectangle([0, 0, W_, 60], fill=(150, 196, 220)); d.line([(0, 60), (W_, 60)], fill=MC.INK, width=3)   # the rear window strip
    d.line([(0, 470), (W_, 480)], fill=(120, 22, 30), width=3)                           # character line
    cx, cy = 170, 300
    d.rectangle([cx - 90, cy - 90, cx + 90, cy + 90], fill=(24, 24, 28), outline=MC.INK, width=4)   # the open flap hole
    d.polygon([(cx - 90, cy - 90), (cx - 170, cy - 70), (cx - 170, cy + 70), (cx - 90, cy + 90)], fill=(170, 32, 38), outline=MC.INK)
    d.ellipse([cx - 66, cy - 66, cx + 66, cy + 66], fill=(60, 60, 68), outline=MC.INK, width=4)    # Type-2 socket
    d.ellipse([cx - 58, cy - 58, cx + 58, cy + 58], fill=(44, 44, 50))
    glow = (90, 230, 255) if int(t * 10) % 2 else (40, 140, 200)
    for ax, ay in ((-30, -24), (0, -36), (30, -24), (-34, 8), (34, 8), (-14, 34), (14, 34)):
        d.ellipse([cx + ax - 9, cy + ay - 9, cx + ax + 9, cy + ay + 9], fill=(12, 12, 14), outline=glow, width=2)
    d.text((cx - 80, cy + 110), 'ЭЛЕКТРО', font=O.pfont(26), fill=(255, 236, 90))
    ex = d.textbbox((cx - 80, cy + 110), 'ЭЛЕКТРО', font=O.pfont(26))[2] - (cx + 96) + 8
    d.polygon([(cx + 110 + ex, cy + 104), (cx + 96 + ex, cy + 128), (cx + 106 + ex, cy + 128), (cx + 98 + ex, cy + 150), (cx + 120 + ex, cy + 120),
               (cx + 110 + ex, cy + 120), (cx + 118 + ex, cy + 104)], fill=(255, 236, 90))
    gx = int(lerp(W_ + 40, cx + 84, sm(u / 0.25)))                                      # the fuel gun freezes an inch away
    d.rectangle([gx, cy - 18, gx + 160, cy + 18], fill=(150, 150, 156), outline=MC.INK, width=3)
    d.rectangle([gx + 60, cy - 40, gx + 200, cy + 30], fill=(60, 62, 70), outline=MC.INK, width=3)
    d.rectangle([gx + 120, cy + 30, gx + 150, cy + 110], fill=(60, 62, 70), outline=MC.INK, width=3)
    big = np.array(im.resize((OUT_W, OUT_H), Image.NEAREST))
    if u < 0.9:
        M.sparks(big, cx * 3, cy * 3, t, 40, 520)
        fx.glow(big, cx * 3, cy * 3, 420, (120, 220, 255), 0.5 * (1 - u / 0.9))
    if u < 0.3: B.shake(big, t, 12, 30)
    return big


def r_zoya2(t, u):
    return KIT.zoya(t, u, Z0=1.6, push=0.08, gum=0.0, look=(1.0, 0.0))


def r_hope(t, u):
    return KIT.cu_maz(t, u, cx=900.0, cy=330.0, sz=16.0, head=(540, 960), expr='teary', look=(1.0, 0.1), beacon=True)


def r_zoya3(t, u):
    return KIT.zoya(t, u, Z0=1.45, push=0.04, gum=gum_pop(t, 25.3), look=(1.0, -0.1))


def lcd(big, t, y0, y1, pct, dead):
    """the wheel display insert (as in E01): blinking empty battery, sad face; goes black when dead"""
    big[y0:y1] = (16, 18, 22)
    big[y0 + 40:y1 - 40, 60:OUT_W - 60] = (40, 44, 52)
    sx0, sy0, sx1, sy1 = 120, y0 + 100, OUT_W - 120, y1 - 100
    big[sy0:sy1, sx0:sx1] = (14, 40, 46) if not dead else (6, 8, 10)
    if dead:
        big[(sy0 + sy1) // 2 - 3:(sy0 + sy1) // 2 + 3, OUT_W // 2 - 40:OUT_W // 2 + 40] = (200, 220, 230)
        return big
    on = int(t * 4) % 2 == 0
    red = (255, 70, 60) if on else (150, 40, 40)
    bx0, by0 = 200, sy0 + 90
    big[by0:by0 + 200, bx0:bx0 + 420] = red; big[by0 + 16:by0 + 184, bx0 + 16:bx0 + 404] = (14, 40, 46)
    big[by0 + 60:by0 + 140, bx0 + 420:bx0 + 460] = red
    img = Image.fromarray(big[sy0:sy1, sx0:sx1]); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text((560, 120), pct, font=O.pfont(120), fill=red)
    d.text((120, 340), 'ДИН-ДОН 3000', font=O.pfont(40), fill=(90, 230, 255))
    big[sy0:sy1, sx0:sx1] = np.array(img)
    fxo, fyo = 820, sy0 + 330
    for dx in (-40, 40): big[fyo:fyo + 30, fxo + dx:fxo + dx + 22] = (90, 230, 255)
    big[fyo + 50:fyo + 62, fxo - 30:fxo + 52] = (90, 230, 255)
    big[fyo + 62:fyo + 74, fxo - 42:fxo - 30] = (90, 230, 255); big[fyo + 62:fyo + 74, fxo + 52:fxo + 64] = (90, 230, 255)
    return big


def r_lcd(t, u):
    dead = t > 27.45
    big = KIT.cu_maz(t, u, cx=900.0, cy=330.0, sz=15.5, head=(560, 1480 + 40 * sm((t - 27.2) / 0.4)), expr='sad', dead=dead,
                     wheel_face='low', look=(0.0, 0.4), mouth_=0.0)
    lcd(big, t, 0, 900, '0%', dead)
    big[900:930] = MC.INK
    return big


def r_trio(t, u):
    """all three stare into the lens: the car plugged into nothing, the dead wheel, Мазутыч; the sign now says «ЗАРЯДКИ НЕТ»"""
    Z = 1.3 + 0.05 * u
    car = car_pumps(t, Z, flap=1.0)
    m = KIT.maz_act(t, PX_ + 105.0, PY_ + 6, Z, flip=True, expr='deadpan', look=(0.0, -0.5), mouth_=0.0, dead=True, beacon=False, shadow=0.3)
    def f(big, v):
        sign_board(big, v, 'зарядки', 1.0)
        hx, hy = aout(m, v, 'hand')
        nozzle(big, hx, hy, 0.8, hose_from=v.opt(1000, 450))
    return K.shot(HW, K.light_hw, 1098.0, 356.0, Z, acts=[car, m], fx_=f, sx=180, sy=330)


def r_bosswin(t, u):
    """button: Борис Борисыч squeezes into the kiosk window next to Зоя — «Розетка — по талону.»"""
    Zw = 1.45
    bx = lerp(820.0, 705.0, sm(u / 0.3))
    def extra(big, v):
        b = A(MC.boss, bx, 560.0, 11.0 * Zw, t=t, pose='key', mouth_=mouth('boss', t), expr='smug', look=(-1.0, 0.0), flip=True, clip=30.0)
        b(big, v, K.light_win(v))
    big = KIT.zoya(t, u, Z0=Zw, push=0.0, look=(1.0, 0.0), extra=extra)
    return big


def r_title(t, u):
    big = r_trio(t, u + 2.35)
    big[:] = (big * 0.35).astype(np.uint8)
    k = sm(u / 0.2)
    O.overlay(big, TITLE, 0, 700, k)
    return big


TITLE = K.hook_title(['СЕЗОН 2:', 'ЗАРЯДКИ НЕТ'], 80)

SHOTS = [r_hook, r_curtain, r_cry, r_keys, r_bosscu, r_tow, r_zoya1, r_sign, r_awe, r_flap, r_socket, r_zoya2, r_hope, r_zoya3, r_lcd,
         r_trio, r_bosswin, r_title]
NAMES = ['hook', 'curtain', 'cry', 'keys', 'bosscu', 'tow', 'zoya1', 'sign', 'awe', 'flap', 'socket', 'zoya2', 'hope', 'zoya3', 'lcd',
         'trio', 'bosswin', 'title']
CAP = dict(curtain=1100, keys=1080, tow=1080, zoya1=1640, zoya2=1640, zoya3=1640, bosswin=1640, lcd=1720, trio=1680, socket=1640,
           title=1500)

SHOW = K.Show(EPI, 6, ['ЕМУ ПОДАРИЛИ', 'МАШИНУ'], hook_t=(0.10, 2.8), hook_y=120, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('ТАЛОН НА ТАЛОН', (90, 230, 255), 52), 9.4, 10.9, 540, 420),
                        (K.st('ЕСТЬ!', (120, 255, 140), 90), 15.9, 16.45, 540, 1480),
                        (K.st('ЭЛЕКТРО?!', (255, 236, 90), 70), 19.0, 20.5, 540, 420),
                        (K.st('0%', (255, 90, 90), 90), 28.2, 30.2, 860, 1300)],
              flashes=[2.9, TWIST, 32.6], mosaics=[10.9])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
