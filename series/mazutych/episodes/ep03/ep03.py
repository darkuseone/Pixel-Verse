"""S01E03 «Из-под полы» — night, garage cooperative. A tinted «Приора» window rolls down two fingers: «Бензин нужен?»
Вадик sells «Родниковая» bottles: «Пятьсот. — За литр?! — За посмотреть.» Мазутыч sniffs like a sommelier: «Это не девяносто
пятый... Мой. Партия четырнадцать.» Twist: «Так я ж у твоего начальника беру» — Борис Борисыч rolls out of the next garage with
a man-bag of cash: «Тебе — со скидкой! Литр — по цене двух.» Дин-Дон: «Это не скидка, друга.»
  python3 ep03.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
import fx
from stage import view_at, OUT_W, OUT_H, Light
from scene import sm, lerp
from episode import Episode
from props import mazcast as MC
from props import mazkit as K
from props import bytfx as B
from props import mazshots as M
from props.mazshots import A, wpt, aout, SP
from timeline import DUR, FPS, VOICE, SLUG, CUTS

EPI = Episode('ep03', VOICE, DUR, FPS, colors=dict(K.COL, vadik=(200, 160, 255)), slug=SLUG)
KIT = M.Kit(EPI)
mouth = KIT.mouth
GAR = K.world('garages')
GROUND = 640.0
DOOR = (460, 320, 615, 505)                      # the second garage: Борис Борисыч comes out of it


def light_gar(v):
    return Light(amb=(0.86, 0.84, 1.02), keys=K._keys(v, ((1120, 190, 700, (255, 200, 120), 0.55), (640, 520, 420, (255, 214, 140), 0.25))),
                 rim=(1, -0.4, (255, 190, 120), 0.45), grad=(1.02, 0.88))


def cu(fn, who, t, u, cx=600.0, cy=380.0, **kw):
    kw.setdefault('flare', (1170, 170))
    kw.setdefault('light', light_gar)
    return KIT.cu(fn, who, t, u, GAR, cx, cy, **kw)


def maz_cu(t, u, expr, **kw):
    kw.setdefault('look', (1.0, 0.0)); kw.setdefault('sz', 16.0); kw.setdefault('head', (560, 960))
    return cu(MC.maz, 'maz', t, u, expr=expr, **kw)


def vadik_cu(t, u, expr='sly', **kw):
    kw.setdefault('sz', 17.0); kw.setdefault('head', (520, 940))
    return cu(MC.vadik, 'vadik', t, u, cx=700.0, flip=True, expr=expr, **kw)


# ================================================================== shots
def r_hook(t, u):
    """a tinted car window rolls down two fingers: eyes, whisper — «Бензин нужен?»"""
    big = vadik_cu(t, u, 'sly', blur=8, look=(1.0, 0.0), sz=18.0, head=(520, 760))
    k = sm((t - 0.15) / 0.45)
    gx0, gx1, gy0, gy1 = 70, 1010, 560, 1520
    gap = int(gy0 + 210 * k)
    car = np.empty_like(big); car[:] = (34, 34, 44)
    yy = np.arange(OUT_H)[:, None]
    car[((yy // 6) % 9 == 0).repeat(OUT_W, 1)] = (44, 44, 58)                         # metallic flake rows
    car[gy0 - 30:gy0 - 18, :] = (150, 150, 160); car[gy1 + 18:gy1 + 30, :] = (150, 150, 160)   # chrome trims
    car[gy1 + 140:gy1 + 170, 700:900] = (110, 110, 120)                               # door handle
    glass = np.zeros((OUT_H, OUT_W), bool); glass[gy0:gy1, gx0:gx1] = True
    show = glass.copy(); show[gap:, :] = False
    tint = glass & ~show
    out = car.copy()
    out[show] = big[show]
    g = np.empty_like(big); g[:] = (14, 14, 20)
    xx = np.arange(OUT_W)[None, :]
    refl = (((xx + yy * 0.7) % 520) < 70)
    g[refl.repeat(1, 0) if refl.shape[0] == OUT_H else np.broadcast_to(refl, (OUT_H, OUT_W))] = (40, 42, 58)
    out[tint] = g[tint]
    out[gap:gap + 10, gx0:gx1] = (90, 90, 100)                                        # the glass's top edge
    fx.glow(out, 980, 300, 260, (255, 200, 120), 0.4)                                 # street lamp in the paint
    return out


def r_look(t, u):
    """Мазутыч checks left, right — nobody — nods"""
    lk = -1.0 if u < 0.4 else 1.0
    return maz_cu(t, u, 'squint', look=(lk, 0.0))


def r_trunk(t, u):
    """the boot opens: rows of golden «Родниковая» bottles, a heavenly glow"""
    Z = 1.55
    k = sm(u / 0.5)
    car = A(MC.lada, 770.0, GROUND, 5.0 * Z, col=(30, 30, 38), tint=True, trunk=k, rims=True, driver=False)
    v_ = A(MC.vadik, 655.0, GROUND + 4, SP * Z, t=t, pose='offer', bottle=True, mouth_=mouth('vadik', t), expr='sly', look=(1.0, 0.0))
    m = KIT.maz_act(t, 580.0, GROUND + 10, Z, expr='awe', look=(1.0, 0.2), mouth_=0.0, shadow=0.3)
    def f(big, v):
        x, y = v.opt(770 - 38, GROUND - 26)
        fx.glow(big, x, y, 380 * k, (255, 220, 110), 0.55 * k)
        for i in range(8):
            a = -1.2 + i * 0.32
            for r in range(60, 380, 10):
                px, py = int(x + math.cos(a) * r), int(y - abs(math.sin(a)) * r - 40)
                if 0 <= px < OUT_W - 6 and 0 <= py < OUT_H - 6 and (r // 10 + i) % 3 == 0:
                    big[py:py + 6, px:px + 6] = (255, 240, 170)
    return K.shot(GAR, light_gar, 690.0, 500.0, Z, acts=[car, v_, m], fx_=f, sx=180, sy=380)


def r_price(t, u):
    return maz_cu(t, u, 'squint')


def r_v500(t, u):
    return vadik_cu(t, u, 'sly', look=(1.0, 0.0))


def r_shock(t, u):
    big = maz_cu(t, u, 'shock', wind=0.5)
    if u < 0.3: B.shake(big, t, 8, 30)
    return big


def r_look500(t, u):
    return vadik_cu(t, u, 'smug', look=(1.0, -0.2))


def r_sniff(t, u):
    """he pays a coin and sniffs the bottle like a sommelier"""
    return maz_cu(t, u, 'squint' if u < 1.6 else 'deadpan', bottle=True, hold=False, look=(0.4, 0.4))


def r_which(t, u):
    return vadik_cu(t, u, 'nervous', look=(1.0, 0.0))


def r_mine(t, u):
    return maz_cu(t, u, 'proud', bottle=True, hold=False, look=(0.0, -0.2))


def r_boss_line(t, u):
    return vadik_cu(t, u, 'sly', look=(1.0, 0.0))


def door_world(k):
    """the second garage's door swung open: warm light, crates of bottles inside"""
    W = GAR.copy()
    if k <= 0: return W
    x0, y0, x1, y1 = DOOR
    w = int((x1 - x0) * k)
    W[y0:y1, x0:x0 + w] = (60, 40, 28)
    yy = np.linspace(0, 1, y1 - y0)[:, None, None]
    W[y0:y1, x0:x0 + w] = (np.array([120, 80, 40]) * (1 - yy) + np.array([60, 38, 24]) * yy).astype(np.uint8)[:, :1, :].repeat(w, 1) if w > 0 else W[y0:y1, x0:x0]
    for i in range(6):                                                                 # crates of bottles
        cx = x0 + 10 + i * 24
        if cx + 18 < x0 + w:
            W[y1 - 40:y1 - 4, cx:cx + 18] = (110, 80, 50)
            for j in range(3): W[y1 - 50:y1 - 38, cx + 2 + j * 6:cx + 5 + j * 6] = (230, 200, 90)
    return W


def r_reveal(t, u):
    """twist: the next garage swings open — Борис Борисыч with a man-bag of cash"""
    Z = 1.35
    k = sm(u / 0.4)
    W = door_world(k)
    bx = lerp(520.0, 560.0, sm((u - 0.2) / 0.6))
    acts = [A(MC.lada, 860.0, GROUND, 6.0 * Z, col=(30, 30, 38), tint=True, trunk=1.0, rims=True, driver=False),
            A(MC.boss, bx, GROUND - 40 + 0 * u, SP * Z, t=t, pose='stand', money=True, mouth_=mouth('boss', t), expr='grin', look=(1.0, 0.0)),
            A(MC.vadik, 730.0, GROUND + 4, SP * Z, t=t, mouth_=0.0, expr='sly', look=(-1.0, 0.0), flip=True),
            KIT.maz_act(t, 660.0, GROUND + 12, Z, flip=True, expr='stunned', look=(1.0, 0.0), mouth_=0.0, shadow=0.3)]
    def f(big, v):
        x, y = v.opt((DOOR[0] + DOOR[2]) / 2, (DOOR[1] + DOOR[3]) / 2)
        fx.glow(big, x, y, 420 * k, (255, 200, 120), 0.4 * k)
    big = K.shot(W, light_gar, 640.0, 470.0, Z, acts=acts, fx_=f, sx=180, sy=380)
    return big


def r_boss_cu(t, u):
    def pre(big, v): pass
    return KIT.cu(MC.boss, 'boss', t, u, door_world(1.0), 560.0, 420.0, sz=17.0, head=(560, 940), light=light_gar, flare=(1170, 170),
                  expr='grin', money=True, pose='key', look=(1.0, 0.0))


def r_nod(t, u):
    """Борис Борисыч and Вадик nod together: «Скидка.»"""
    Z = 2.7
    nod = 1.5 * abs(math.sin(t * 7))
    W = door_world(1.0)
    acts = [A(MC.boss, 560.0, GROUND - 40 + nod, SP * Z, t=t, money=True, mouth_=0.0, expr='smug', look=(1.0, 0.0)),
            A(MC.vadik, 650.0, GROUND + 4 + nod, SP * Z, t=t, mouth_=mouth('vadik', t), expr='sly', look=(-1.0, 0.0), flip=True)]
    return K.shot(W, light_gar, 605.0, 560.0, Z, acts=acts, sx=180, sy=440)


def r_button(t, u):
    """Мазутыч turns to camera; the wheel's display: «Это не скидка, друга.»"""
    return maz_cu(t, u, 'deadpan', look=(0.0, -0.3), mouth_=0.0, bottle=True, hold=False, sz=13.0, head=(540, 820))


SHOTS = [r_hook, r_look, r_trunk, r_price, r_v500, r_shock, r_look500, r_sniff, r_which, r_mine, r_boss_line, r_reveal, r_boss_cu, r_nod,
         r_button]
NAMES = ['hook', 'look', 'trunk', 'price', 'v500', 'shock', 'look500', 'sniff', 'which', 'mine', 'bossline', 'reveal', 'bosscu', 'nod',
         'button']
CAP = dict(hook=1700, trunk=1080, reveal=1080, nod=1640, button=1640)

SHOW = K.Show(EPI, 3, ['БЕНЗИН', 'ИЗ-ПОД ПОЛЫ'], hook_t=(0.10, 2.8), hook_y=120, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('500!', (255, 236, 120), 80), 7.6, 8.5, 780, 520),
                        (K.st('ПАРТИЯ №14', (255, 160, 60), 56), 16.7, 19.0, 540, 420),
                        (K.st('СКИДКА?', (255, 90, 90), 64), 25.2, 27.1, 540, 420)],
              flashes=[3.25, 21.6], mosaics=[11.7])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
