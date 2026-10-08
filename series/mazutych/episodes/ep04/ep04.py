"""S01E04 v2 «Без прав» (08.10.2026, по статистике TikTok): hook text «ШТРАФ ЗА МОНОКОЛЕСО?!» + the fine slip shoved at the
lens; «Знак видим?» became a silent visual gag (the «20» sign right next to «Двадцать пять в час»); twist at 59 % (17.45 s).
v1: a traffic cop stops the monowheel: «Превышаем! — Двадцать пять в час. — Знак видим?» (a «20» sign stuck
right there). «Права категории "Моно"? — Такой нет. — Значит, без прав.» Дин-Дон: «У меня есть права. Китайский.»
«Документики на транспорт! — Вот. От шестёрки.» (the steering wheel). Twist: «Ладно... Дотащишь — отпущу. Третий день без
бензина.» Мазутыч tows the patrol car; Толик passing: «А кто кого остановил?!» Button: the cop does the siren with his mouth.
  python3 ep04.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
import fx
import overlays as O
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
from episode import Episode
from props import mazcast as MC
from props import mazkit as K
from props import bytfx as B
from props import mazshots as M
from props.mazshots import A, wpt, aout, y_far, y_near, y_sh, SP, CAR, TRK
from timeline import DUR, FPS, VOICE, SLUG, CUTS, TWIST

EPI = Episode('ep04', VOICE, DUR, FPS, colors=dict(K.COL, cop=(190, 240, 60)), slug=SLUG)
KIT = M.Kit(EPI)
HW = KIT.HW
mouth = KIT.mouth
PX = 360.0                                     # where the stop happens on the highway (left of the queue)


def lights(big, t, k=0.35):
    """red / blue patrol light wash over the frame"""
    on = int(t * 6) % 2 == 0
    col = np.array((255, 40, 40) if on else (40, 90, 255), np.float32)
    half = slice(0, OUT_W // 2) if on else slice(OUT_W // 2, OUT_W)
    reg = big[:, half].astype(np.float32)
    big[:, half] = np.clip(reg * (1 - k) + col * k, 0, 255).astype(np.uint8)


def cop_cu(t, u, expr='glare', pose='stand', **kw):
    kw.setdefault('sz', 16.0); kw.setdefault('head', (520, 900))
    return KIT.cu(MC.inspector, 'cop', t, u, HW, PX + 120, 380.0, flip=True, expr=expr, pose=pose, **kw)


def maz_cu(t, u, expr, **kw):
    kw.setdefault('sz', 16.0); kw.setdefault('head', (560, 960)); kw.setdefault('look', (1.0, 0.0))
    return KIT.cu(MC.maz, 'maz', t, u, HW, PX - 60, 380.0, expr=expr, **kw)


# ================================================================== shots
def r_hook(t, u):
    big = cop_cu(t, u, 'glare', 'stop', whistle=t < 0.5, sz=17.0 + 1.5 * u)
    lights(big, t, 0.25)
    k = sm((u - 0.25) / 0.2)
    if k > 0:                                                    # the fine slip shoved at the lens
        M.paper(big, 560, int(lerp(1900, 1440, k)), ['ШТРАФ', 'МОНОКОЛЕСО', '№ 000001'], w=440, h=300, rot=-7 + 2 * math.sin(t * 9),
                col=(236, 232, 214), sizes=[70, 34, 26])
    if u < 0.3: B.shake(big, t, 10, 30)
    return big


def r_brake(t, u):
    big = maz_cu(t, u, 'deadpan', rot=-6.0 * (1 - sm(u / 0.5)))
    lights(big, t, 0.2)
    return big


def r_sign(t, u):
    """the «20» sign is stuck in the ground right where they stand"""
    Z = 1.9 + 0.25 * u
    acts = [KIT.maz_act(t, PX - 10, y_sh(PX - 10), Z, expr='deadpan', look=(1.0, 0.0)),
            A(MC.sign20, PX + 62, y_sh(PX + 62) + 4, SP * Z * 1.9),
            A(MC.inspector, PX + 135, y_sh(PX + 135) + 2, SP * Z, flip=True, t=t, pose='point', mouth_=0.0, expr='smug')]
    big = K.shot(HW, K.light_hw, PX + 65, 520.0, Z, acts=acts, sx=180, sy=380)
    lights(big, t, 0.15)
    return big


def r_cat(t, u):
    return cop_cu(t, u, 'squint', 'stand')


def r_none(t, u):
    return maz_cu(t, u, 'deadpan')


def r_fine(t, u):
    return cop_cu(t, u, 'smug', 'stand')


def r_license(t, u):
    """the wheel's display shows its own driving licence: «Китайский.»"""
    big = maz_cu(t, u, 'stunned', head=(560, 1480), sz=15.5, look=(0.0, -1.0), mouth_=0.0)
    big[0:900] = (16, 18, 22)
    big[40:860, 60:OUT_W - 60] = (40, 44, 52)
    big[100:800, 120:OUT_W - 120] = (14, 40, 46)
    im = Image.fromarray(big[100:800, 120:OUT_W - 120]); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([60, 80, 780, 600], fill=(236, 226, 196), outline=(200, 40, 40), width=8)
    d.rectangle([100, 150, 330, 430], fill=(150, 200, 220), outline=(40, 40, 46), width=4)
    d.ellipse([170, 190, 260, 300], fill=(90, 230, 255), outline=(40, 40, 46), width=4)          # the wheel's photo: a smiley wheel
    d.rectangle([205, 225, 215, 240], fill=(40, 40, 46)); d.rectangle([228, 225, 238, 240], fill=(40, 40, 46))
    d.text((370, 140), 'ПРАВА', font=O.pfont(48), fill=(200, 40, 40))
    for i in range(4):                                                                         # «hieroglyphs»
        y = 230 + i * 70
        for j in range(6):
            x = 370 + j * 60
            d.rectangle([x, y, x + 40, y + 6], fill=(60, 60, 70)); d.rectangle([x + 16, y - 12, x + 22, y + 30], fill=(60, 60, 70))
            if (i + j) % 2: d.rectangle([x, y + 18, x + 40, y + 24], fill=(60, 60, 70))
    d.text((120, 520), 'ДИН-ДОН 3000 · КАТ. «МОНО»', font=O.pfont(26), fill=(60, 60, 70))
    big[100:800, 120:OUT_W - 120] = np.array(im)
    big[900:930] = MC.INK
    return big


def r_docs(t, u):
    return cop_cu(t, u, 'glare', 'point')


def r_wheel(t, u):
    """«Вот. От шестёрки.» — he hands over the fur-covered steering wheel as documents"""
    return maz_cu(t, u, 'proud', steer=0.6 * math.sin(t * 3), look=(1.0, 0.0))


def r_whisper(t, u):
    big = cop_cu(t, u, 'nervous', 'stand', look=(-1.0, 0.0) if u < 0.6 else (1.0, 0.0), sz=19.0, head=(500, 980))
    return big


def r_bushes(t, u):
    """reveal: the patrol «six» hiding in the bushes, lights blinking, «Третий день без бензина»"""
    Z = 1.6
    cx = PX + 260
    acts = [A(MC.lada, cx, y_far(cx) - 4, CAR * Z, t=t, col=(240, 240, 236), police=True, driver=False, web=True),
            A(MC.bush, cx - 70, y_far(cx) + 8, SP * Z * 1.3, seed=2), A(MC.bush, cx + 60, y_far(cx) + 10, SP * Z * 1.4, seed=5),
            A(MC.inspector, cx - 105, y_sh(cx - 105), SP * Z, t=t, pose='point', mouth_=mouth('cop', t), expr='sad', look=(1.0, 0.0))]
    big = K.shot(HW, K.light_hw, cx - 30, 520.0, Z + 0.1 * u, acts=acts, sx=180, sy=380)
    lights(big, t, 0.12)
    return big


def r_tow(t, u):
    """Мазутыч on the monowheel tows the patrol car; the cop waves his baton out of the window"""
    Z = 1.2
    x = 420.0 + 60.0 * u
    car_x = x - 170.0
    car = A(MC.lada, car_x, y_sh(car_x) - 2, CAR * Z, t=t, col=(240, 240, 236), police=True, driver=False, spin=-t * 4)
    wx, wy = car_x + 4.5 * CAR / 3, y_sh(car_x) - 2 - 19 * CAR / 3
    cop = A(MC.inspector, wx, wy + 58 * SP / 3 * 0.9, SP * Z * 0.9, t=t, pose='wave', mouth_=0.0, expr='glare', clip=56.0, look=(1.0, 0.0))
    m = KIT.maz_act(t, x, y_sh(x), Z, expr='strain', wind=0.5, spin=t * 22, rot=-12.0, sweat=1.0, beacon=True, shadow=0.3, mouth_=0.0)
    def f(big, v):
        M.rope(big, aout(m, v, 'belt'), aout(car, v, 'front'), sag=18, w=10)
        ox, oy = v.opt(x, y_sh(x))
        M.sparks(big, ox, oy, t, 14, 160)
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
    big = K.shot(HW, K.light_hw, x - 50.0, 520.0, Z, acts=[car, cop, m], fx_=f, sx=180, sy=380)
    lights(big, t, 0.12)
    return big


def r_tolik(t, u):
    """Толик's tanker rolls past the other way; he leans out laughing"""
    Z = 2.0
    tx = lerp(900.0, 520.0, sm(u / 1.0))
    tank = A(MC.tanker, tx, y_far(tx), TRK * Z, flip=True, t=t, spin=t * 10)
    wx, wy = tx - 86 * TRK / 3, y_far(tx) - 35 * TRK / 3
    tol = A(MC.tolik, wx + 4.0, wy + 10 + 44 * SP / 3, SP * Z, flip=True, t=t, lean=True, wave=1.0, mouth_=mouth('tolik', t), clip=34.0,
            expr='cheer', look=(1.0, 0.0))
    return K.shot(HW, K.light_hw, wx - 10.0, wy - 10.0, Z, acts=[tank, tol], sx=180, sy=380)


def r_siren(t, u):
    """button: the cop in the towed car's window does the siren with his mouth"""
    Z = 2.6
    car_x = 560.0
    car = A(MC.lada, car_x, y_sh(car_x) - 2, CAR * Z, t=t, col=(240, 240, 236), police=True, driver=False)
    wx, wy = car_x + 4.5 * CAR / 3, y_sh(car_x) - 2 - 19 * CAR / 3
    cop = A(MC.inspector, wx, wy + 58 * SP / 3 * 0.9, SP * Z * 0.9, t=t, pose='wave', mouth_=mouth('cop', t), expr='deadpan', clip=56.0,
            look=(1.0, 0.0))
    big = K.shot(HW, K.light_hw, wx + 10.0, wy - 20.0, Z, acts=[car, cop], sx=180, sy=420)
    lights(big, t, 0.18)
    return big


SHOTS = [r_hook, r_sign, r_cat, r_none, r_fine, r_license, r_docs, r_wheel, r_whisper, r_bushes, r_tow, r_tolik, r_siren]
NAMES = ['hook', 'sign', 'cat', 'none', 'fine', 'license', 'docs', 'wheel', 'whisper', 'bushes', 'tow', 'tolik', 'siren']
CAP = dict(hook=1180, sign=1640, license=1720, bushes=1100, tow=1100, tolik=1560, siren=1640)

SHOW = K.Show(EPI, 4, ['ШТРАФ ЗА', 'МОНОКОЛЕСО?!'], hook_t=(0.10, 2.3), hook_y=120, cap_default=1600, cap_y=CAP,
              stickers=[(K.st('25 КМ/Ч', (255, 236, 120), 64), 2.5, 4.0, 760, 520),
                        (K.st('БЕЗ ПРАВ', (255, 90, 90), 70), 8.9, 10.7, 540, 420),
                        (K.st('ДОТАЩИШЬ?', (190, 240, 60), 60), 17.8, 20.0, 540, 420)],
              flashes=[TWIST, 22.1], mosaics=[20.1])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
