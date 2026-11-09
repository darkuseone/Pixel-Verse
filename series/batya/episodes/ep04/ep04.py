"""E04 «412 КВТ?! КТО НЕ ВЫКЛЮЧИЛ СВЕТ?!» — dark at 16:30, the electricity bill: Batya declares war on bulbs and chargers, the family
lives by candle and phone light, but the meter still spins. TWIST (the villain is one of us): on the balcony hums Batya's own chest
freezer «ОКА-1987» next to a heater — inside, a frozen bream «ЛЕЩ 2005». «Не трогай! Это стратегический запас!» —
Ira: «Витя. Этот лещ старше Тёмы.»   Clue: the humming and a pink glow from the balcony room in the first half.
  python3 ep04.py test … | frames … | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from stage import view_at, Light
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as BF
from props import decals as D
from props import batyacast as B
from props import batyakit as K
from props import batyashots as S
from props.batyashots import mouth, u2w, face, P, BED, KIT, BX, UN, BED_TOP, FLOOR
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG, promo='ru',
              endcard=dict(style='batya', lang='ru', promise='ЗАВТРА: 7 ЛИШНИХ БОЛТОВ?!'))
S.init(EPI)
HALL = S.extra_world('hall')
BAL = S.extra_world('balcony')
F0 = TL.T0
OL = B.OL
INK, RED, CREAM = (34, 28, 30), (184, 30, 40), (255, 252, 236)

D.attach(HALL, [
    (P(70, 104, ['ЭКОНОМЬ', 'СВЕТ!', 'ЖЭК № 3'], (250, 246, 226), [RED, INK, INK], (150, 140, 120), pad=0.8,
       weights=[1, 1, 0.6]), 60, 246),
    (P(40, 14, ['412'], (20, 22, 20), [(250, 120, 60)], (90, 96, 90), pad=0.4), 106, 92),
    (P(44, 18, ['БАТИН', 'ГАРАЖ'], (255, 244, 170), [INK, INK], (150, 130, 70), pad=0.5, tilt=-3), 300, 150),
])
D.attach(BAL, [
    (P(60, 30, ['ОКА-1987'], (210, 214, 220), [INK], (120, 124, 130), pad=0.5), 605, 503),
    (P(66, 24, ['НЕ ТРОГАТЬ!', 'ВИТЯ'], (255, 252, 236), [RED, INK], (150, 140, 120), pad=0.6, tilt=-4, hand=True), 470, 344),
    (P(40, 18, ['МАЛИНА', '2025'], (255, 252, 236), [RED, INK], None, pad=0.4), 762, 112),
    (P(46, 18, ['ПОМИДОРЫ', 'ИРЫ'], (255, 244, 170), [(40, 110, 60), INK], (150, 130, 70), pad=0.4), 760, 312),
])
BILL = P(84, 60, ['КВИТАНЦИЯ', '412 кВт'], (250, 250, 240), [(40, 70, 160), RED], (120, 120, 130), pad=0.6, weights=[0.6, 1])
TAG = P(46, 18, ['ЛЕЩ 2005'], (255, 244, 170), [INK], (150, 130, 70), pad=0.4)
DARK = ((0.42, 0.46, 0.7), (0, 0, 8))


def dark(big, mult=DARK[0]):
    fx.grade(big, mult, DARK[1])


# ---------------------------------------------------------------- props (unit coords at hand h)
def bulb(L, h):
    F.ell(L, (h[0], h[1] - 1.6), 1.1, 1.3, (250, 246, 220), 0, (255, 255, 250), (214, 210, 190))
    F.cap(L, (h[0] - 0.5, h[1] - 0.2), (h[0] + 0.5, h[1] - 0.2), 0.35, 0.35, (170, 170, 176), (210, 210, 216), (120, 120, 126))


def plug(L, h):
    F.poly(L, [(h[0] - 0.5, h[1] - 0.9), (h[0] + 0.5, h[1] - 0.9), (h[0] + 0.5, h[1] + 0.3), (h[0] - 0.5, h[1] + 0.3)], (240, 240, 244))
    for dx in (-0.25, 0.25): F.cap(L, (h[0] + dx, h[1] - 0.9), (h[0] + dx, h[1] - 1.6), 0.09, 0.09, (200, 200, 210))
    F.cap(L, (h[0], h[1] + 0.3), (h[0] + 1.5, h[1] + 3.0), 0.14, 0.14, (240, 240, 244))


def candle(L, h, t=0.0):
    F.cap(L, (h[0], h[1] - 0.2), (h[0], h[1] - 2.4), 0.45, 0.45, (250, 244, 220), (255, 255, 240), (210, 200, 170))
    f = 0.15 * math.sin(t * 17)
    F.ell(L, (h[0] + f, h[1] - 3.0), 0.35, 0.7, (255, 200, 70)); F.ell(L, (h[0] + f, h[1] - 2.9), 0.18, 0.35, (255, 250, 210))


def book(L, h):
    F.poly(L, [(h[0] - 2.2, h[1] - 1.6), (h[0] + 2.2, h[1] - 1.6), (h[0] + 2.0, h[1] + 0.8), (h[0] - 2.0, h[1] + 0.8)], (60, 90, 150))
    F.poly(L, [(h[0] - 1.9, h[1] - 1.4), (h[0] + 1.9, h[1] - 1.4), (h[0] + 1.8, h[1] + 0.5), (h[0] - 1.8, h[1] + 0.5)], (246, 240, 220))


def bream(L, h, s=1.0, tilt=0.0):
    """frozen bream held like a plank: silver body, frost, tail, glassy eye"""
    T = lambda x, y: (h[0] + (x * math.cos(tilt) - y * math.sin(tilt)) * s, h[1] + (x * math.sin(tilt) + y * math.cos(tilt)) * s)
    F.poly(L, [T(-5.0, 0), T(-3.0, -2.2), T(1.5, -2.4), T(4.6, -0.6), T(4.6, 0.6), T(1.5, 2.2), T(-3.0, 2.0)],
           (176, 186, 196))
    F.poly(L, [T(-3.0, -2.0), T(1.5, -2.2), T(4.0, -0.6), T(-4.0, -0.4)], (214, 222, 230))
    F.poly(L, [T(4.4, 0), T(6.6, -2.2), T(6.0, 0), T(6.6, 2.2)], (150, 160, 172))
    F.poly(L, [T(-1.0, -2.3), T(1.0, -3.6), T(2.0, -2.3)], (150, 160, 172))
    F.ell(L, T(-3.6, -0.5), 0.6 * s, 0.6 * s, (250, 250, 255)); F.dot(L, T(-3.6, -0.5), (30, 30, 40), 0.35 * s)
    F.cap(L, T(-4.9, 0.5), T(-4.0, 0.9), 0.12 * s, 0.12 * s, (90, 70, 80))
    for k in range(9):
        F.dot(L, T(-3.0 + k * 0.85, -1.4 + 2.6 * ((k * 37) % 10) / 10), (236, 246, 255), 0.22 * s)


# ---------------------------------------------------------------- worlds
def light_hall(v):
    dx, dy = v.opt(820.0, 220.0); px, py = v.opt(1130.0, 300.0)
    return Light(amb=(0.6, 0.66, 0.9), keys=[(dx, dy, 900, (150, 180, 255), 0.5), (px, py, 700, (255, 120, 220), 0.4)],
                 rim=(1, -0.3, (150, 180, 255), 0.4), grad=(1.0, 0.85))


def light_bal(v):
    hx, hy = v.opt(810.0, 460.0); bx, by = v.opt(635.0, 130.0); px, py = v.opt(860.0, 200.0)
    return Light(amb=(0.8, 0.8, 0.95), keys=[(hx, hy, 900, (255, 150, 70), 0.6), (bx, by, 900, (255, 210, 140), 0.5),
                                             (px, py, 700, (255, 120, 220), 0.35)], rim=(-1, -0.3, (150, 180, 255), 0.45), grad=(1.02, 0.88))


def hall(v, t, draw=None, after=None):
    def aft(big, v_):
        k = 0.5 + 0.5 * math.sin(t * 7)                                       # the clue: pink balcony glow pulsing in the far door
        x, y = v_.opt(1130.0, 330.0); fx.glow(big, x, y, 260 * v_.Z, (255, 110, 220), 0.18 + 0.12 * k)
        if after: after(big, v_)
    return S.world(HALL, v, t, draw, light_hall(v), motes=(500, 200, 900, 500), after=aft, vign=0.34)


def balcony(v, t, draw=None, after=None, hum=1.0):
    def aft(big, v_):
        x, y = v_.opt(810.0, 460.0); fx.glow(big, x, y, 300 * v_.Z, (255, 140, 60), 0.22 + 0.05 * math.sin(t * 5))
        x, y = v_.opt(860.0, 200.0); fx.glow(big, x, y, 260 * v_.Z, (255, 100, 220), 0.2)
        if hum:                                                               # vibration marks off the freezer
            for k, (wx, wy) in enumerate(((396, 360), (704, 360), (396, 470), (704, 470))):
                ox, oy = v_.opt(wx, wy); sgn = -1 if wx < 550 else 1
                ph = (t * 6 + k * 0.3) % 1.0
                for j in range(3):
                    a = int(255 * hum * (1 - ph))
                    x0 = int(ox + sgn * (14 + j * 14 + ph * 20) * v_.Z)
                    big[max(0, int(oy - 18 * v_.Z)):max(0, int(oy + 18 * v_.Z)), max(0, x0):max(0, x0 + int(5 * v_.Z))] = \
                        (np.array([236, 246, 255]) * (a / 255) + big[max(0, int(oy - 18 * v_.Z)):max(0, int(oy + 18 * v_.Z)),
                                                                     max(0, x0):max(0, x0 + int(5 * v_.Z))] * (1 - a / 255)).astype(np.uint8)
        if after: after(big, v_)
    return S.world(BAL, v, t, draw, light_bal(v), snow=(0, 0, 380, 420), after=aft, vign=0.3)


def dark_bed(v, t, draw, glows, after=None):
    def aft(big, v_):
        dark(big)
        for (wx, wy, r, col, a) in glows():
            x, y = v_.opt(wx, wy); fx.glow(big, x, y, r * v_.Z, col, a)
        if after: after(big, v_)
    return S.world(BED, v, t, draw, S.light_bed(v), after=aft, vign=0.4)


def dark_kit(v, t, draw, glows, after=None):
    def aft(big, v_):
        dark(big)
        for (wx, wy, r, col, a) in glows():
            x, y = v_.opt(wx, wy); fx.glow(big, x, y, r * v_.Z, col, a)
        if after: after(big, v_)
    return S.world(KIT, v, t, draw, S.light_kit(v), after=aft, vign=0.4)


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Четыреста двенадцать?! Кто не выключил свет?!» — kitchen, Batya in shock with the bill «412 кВт» held up to the camera"""
    z = 1.2 + 0.08 * sm(min(1.0, u / 3.0))
    v = view_at(KIT, 600, 330, z, 180, 330)
    st = {}

    def draw(CH, v_):
        cam = v_.cam(590, 720, UN * 1.08)
        r = B.batya(CH, cam, B.BPOSE['point'], t=t, mouth_=mouth('batya', t), expr='shock', hand_n=F.H(4.8, 17.0))
        face(v_, cam, r, 3.2); st['h'] = u2w(v_, cam, F.H(4.8, 17.0))
    big = S.kitchen(v, t, draw)
    D.blit(big, v, BILL, st['h'][0] - 60, st['h'][1] - 56)
    return big


def r_bulbs(t, u):
    """«Лампочку — выкрутить! Зарядку — выдернуть! Я сам!» — dark bedroom, a torch beam, Batya holds up a bulb and a yanked plug"""
    v = view_at(BED, 820, 330, 1.15, 180, 320)
    st = {}

    def draw(CH, v_):
        cam = v_.cam(820, FLOOR + 40, UN * 1.1)
        r = B.batya(CH, cam, B.BPOSE['fists'], t=t, mouth_=mouth('batya', t), expr='fists', hand_n=F.H(4.6, 21.0), prop_n=bulb,
                    hand_f=F.H(-4.2, 19.0), prop_f=plug)
        face(v_, cam, r, 3.2); st['b'] = u2w(v_, cam, F.H(4.6, 22.6))
    return dark_bed(v, t, draw, lambda: [(st['b'][0], st['b'][1], 120, (255, 240, 190), 0.35),
                                         (820, 330, 420, (255, 230, 170), 0.12)])


def r_dark(t, u):
    """«Мы теперь живём как в тысяча восемьсот двенадцатом.» — Tyoma's stream in the dark kitchen, lit by his phone"""
    v = view_at(KIT, 560, 330, 1.0, 180, 320)

    def draw(CH, v_):
        cam = v_.cam(668, 1040, 26.0, flip=True)
        r = B.tema(CH, cam, B.TPOSE['selfie'], t=t, mouth_=mouth('tema', t), expr='deadpan', prop_n=None, hand_n=F.H(9.5, 17.0),
                   look=0.6)
        face(v_, cam, r, 2.6)
    return dark_kit(v, t, draw, lambda: [(640, 520, 380, (190, 220, 255), 0.35)],
                    after=lambda b, v_: K.phone_ui(b, t, f'{3100 + int(2500 * min(1.0, u / 2.0)):,}'.replace(',', ' ')))


def r_candle(t, u):
    """«Витя. Я при свечке ничего не вижу.» — Ira in bed with a candle and a book; a pink glow + hum from the door (the clue)"""
    v = view_at(BED, 600, 300, 1.12, 180, 320)
    st = {}

    def draw(CH, v_):
        cam, r = S.ira_bed(CH, v_, t, 'dry', x=BX, pose=B.IPOSE['tray'], hand_n=F.H(4.6, 12.6),
                           prop_n=lambda L, h: candle(L, h, t), hand_f=F.H(-1.6, 13.2), prop_f=book)
        S.blankets(CH, v_, BED_TOP + 9.6 * UN - 9.8 * UN, BX - 6 * UN, BX + 6.4 * UN, t, tiger=False)
        st['c'] = u2w(v_, cam, F.H(4.6, 15.6))
    k = 0.5 + 0.5 * math.sin(t * 7)
    return dark_bed(v, t, draw, lambda: [(st['c'][0], st['c'][1], 260, (255, 190, 90), 0.5),
                                         (1120, 330, 260, (255, 110, 220), 0.2 + 0.15 * k)])


def r_meter(t, u):
    """«Всё выключено — а он крутится! Кто?!» — hallway: Batya points the tape measure at the spinning meter"""
    v = view_at(HALL, 222, 320, 1.05, 180, 300)
    st = {}

    def draw(CH, v_):
        cam = v_.cam(330, 770, 17.5, flip=True)
        r = B.batya(CH, cam, B.BPOSE['point'], t=t, mouth_=mouth('batya', t), expr='angry', hand_n=F.H(7.0, 24.0))
        face(v_, cam, r, 3.2)

    def after(big, v_):                                                         # the red mark on the meter disc spins
        a = t * 9.0
        x, y = v_.opt(132 + 26 * math.cos(a), 128 + 4 * math.sin(a))
        big[int(y - 6 * v_.Z):int(y + 6 * v_.Z), int(x - 8 * v_.Z):int(x + 8 * v_.Z)] = (220, 40, 40)
    return hall(v, t, draw, after)


def r_twist(t, u):
    """«Бать… а что у нас на балконе гудит?» — the balcony door opens: the chest freezer «ОКА-1987» hums and shakes next to the heater"""
    z = 0.92 + 0.1 * sm(min(1.0, u / 2.5))
    v = view_at(BAL, 640, 360, z, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(745, 760, 15.5, flip=True)
        r = B.tema(CH, cam, B.TPOSE['film'], t=t, mouth_=mouth('tema', t), expr='deadpan', look=-0.6)
        face(v_, cam, r, 2.6)
    big = balcony(v, t, draw)
    if u < 0.5: fx.speed_lines(big, t, 0.8)
    return big


def r_hug(t, u):
    """«Не трогай! Это стратегический запас!» — Batya throws himself onto the freezer lid, arms wide"""
    v = view_at(BAL, 540, 340, 1.15, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(540, 660, 16.0)
        r = B.batya(CH, cam, B.BPOSE['hold'], t=t, mouth_=mouth('batya', t), expr='shout', hand_n=F.H(8.0, 14.0), hand_f=F.H(-7.0, 14.0))
        face(v_, cam, r, 3.2)
    return balcony(v, t, draw)


def r_bream(t, u):
    """«Лещ. Две тысячи пятого года.» — Tyoma holds the frozen bream stiff as a plank, tag «ЛЕЩ 2005»"""
    v = view_at(BAL, 720, 300, 1.3, 180, 330)
    st = {}

    def draw(CH, v_):
        cam = v_.cam(730, 700, 18.0, flip=True)
        r = B.tema(CH, cam, B.TPOSE['stand'], t=t, mouth_=mouth('tema', t), expr='deadpan', prop_n=lambda L, h: bream(L, h, 1.1),
                   hand_n=F.H(2.0, 19.0), hand_f=F.H(-3.0, 19.0))
        face(v_, cam, r, 2.6); st['h'] = u2w(v_, cam, F.H(2.0, 22.0))
    big = balcony(v, t, draw, hum=0.4)
    D.blit(big, v, TAG, st['h'][0] - 20, st['h'][1] - 34)
    BF.steam(big, v, t, st['h'][0], st['h'][1], n=5, rise=60, size=30, a=0.35)
    return big


def r_fresh(t, u):
    """«Он ещё свежий! Я его сам поймал!» — Batya, proud, cradles the frozen bream"""
    v = view_at(BAL, 520, 340, 1.45, 180, 300)
    st = {}

    def draw(CH, v_):
        cam = v_.cam(520, 700, 18.5)
        r = B.batya(CH, cam, B.BPOSE['hold'], t=t, mouth_=mouth('batya', t), expr='proud', hand_n=F.H(4.0, 15.0),
                    prop_n=lambda L, h: bream(L, (h[0] - 3.0, h[1] - 1.0), 1.0, -0.15), hand_f=F.H(-2.0, 15.0))
        face(v_, cam, r, 3.2); st['h'] = u2w(v_, cam, F.H(0.0, 18.0))
    big = balcony(v, t, draw, hum=0.4)
    D.blit(big, v, TAG, st['h'][0] - 20, st['h'][1] - 30)
    return big


def r_button(t, u):
    """«Витя. Этот лещ старше Тёмы.» — Ira at the balcony door, dry; Batya by the freezer hugging the bream"""
    v = view_at(BAL, 690, 350, 0.95, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(590, 690, 15.5)
        r = B.batya(CH, cam, B.BPOSE['hold'], t=t, mouth_=0.0, expr='whine', hand_n=F.H(4.0, 15.0),
                    prop_n=lambda L, h: bream(L, (h[0] - 3.0, h[1] - 1.0), 1.0, -0.15), hand_f=F.H(-2.0, 15.0))
        face(v_, cam, r, 3.2)
        cam2 = v_.cam(790, 720, 16.0, flip=True)
        r2 = B.ira(CH, cam2, B.IPOSE['hips'], t=t, mouth_=mouth('ira', t), expr='dry')
        face(v_, cam2, r2, 2.6)
    return balcony(v, t, draw, hum=0.4)


def r_loop(t, u):
    return r_hook(t, 0.0)


SHOT = dict(hook=r_hook, bulbs=r_bulbs, dark=r_dark, candle=r_candle, meter=r_meter, twist=r_twist, hug=r_hug, bream=r_bream,
            fresh=r_fresh, button=r_button, loop=r_loop)
CUTS, NAMES = TL.CUTS, TL.NAMES


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


QUESTION = K.question('СКОЛЬКО КВТ У ВАС?', 'ПИШИ ЦИФРУ')


def extra(big, t, shot):
    if TL.DUR - 2.4 <= t < TL.DUR - 1.0:
        O.overlay(big, QUESTION, (big.shape[1] - QUESTION.shape[1]) // 2, 230, min(1.0, (t - (TL.DUR - 2.4)) / 0.12))


SHOW = K.Show(EPI, 1, 4, ['412 КВТ?!', 'КТО?!'], hook_t=(0.06, 2.6), hook_y=250,
              stickers=[(O.sticker('ЭТО ТВОЁ?!', fg=(255, 150, 220), size=100), TL.TWIST + 0.3, F0['hug'], 540, 470),
                        (O.sticker('ЭКОНОМИЯ!', fg=(255, 236, 120), size=80), F0['bulbs'] + 0.3, F0['dark'], 540, 400),
                        (O.sticker('ГУ-У-У…', fg=(255, 150, 220), size=60), F0['meter'] + 0.8, TL.TWIST, 820, 560)],
              flashes=[TL.TWIST + 0.02], mosaics=[F0['twist']], extra=extra,
              cap_y={'dark': 1460}, cap_default=1400)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
