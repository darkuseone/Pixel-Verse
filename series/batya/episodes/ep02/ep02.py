"""E02 «-20 — НЕ ЗАВОДИТСЯ?!» — minus twenty, the old red Lada won't start. «Не трогай! Я сам!» — Batya carries the battery home and
tucks it into bed under the tiger plaid with a hot-water bottle, measures it: «Тридцать семь и два. Пойдёт.» (callback to E01).
Morning: the car starts! — TWIST (success is worse than failure): a queue of neighbours, each with a battery: «Саныч! И мой погрей, а?»
Batya opens a «hotel», the bed is full of batteries; Ira: «Я с аккумуляторами в одной кровати не сплю.» — «Они же тёплые!»
  python3 ep02.py test … | frames … | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import stage as ST
from stage import view_at, Light
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as BF
from props import decals as D
from props import rusigns as R
from props import batyacast as B
from props import batyakit as K
from props import batyashots as S
from props.batyashots import mouth, u2w, face, BED, BED_TOP, UN, BX, FLOOR, P
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=dict(K.COL, sosed=(150, 210, 255)), slug=TL.SLUG, promo='ru',
              endcard=dict(style='batya', lang='ru', promise='ЗАВТРА: КОВЁР НА СНЕГ!'))
S.init(EPI)
YARD = S.extra_world('yard')
F0 = TL.T0
OL = B.OL
YF, YU = 610.0, 8.6            # yard: floor line in front of the car, hero unit (car ≈ 1.4 m ≈ 165 px)

D.attach(YARD, [
    (P(30, 30, ['-20'], (236, 244, 250), [(40, 70, 160)], (60, 70, 90), pad=0.8, round_=1.0), 1051, 347),
    (P(36, 36, ['-20'], (236, 244, 250), [(40, 70, 160)], (60, 70, 90), pad=0.8, round_=1.0), 462, 318),
    (P(30, 12, ['ПОДЪЕЗД 3'], (60, 110, 70), [(244, 240, 220)], (30, 50, 34), pad=0.6), 978, 296),
    (P(44, 24, ['НЕ ПАРКОВАТЬСЯ!', 'ЗДЕСЬ БАБУШКИ'], (255, 252, 236), [(184, 30, 40), (34, 28, 30)], (150, 140, 120), pad=0.7,
       tilt=-2, weights=[1, 0.8]), 1110, 300),
    (P(40, 14, ['ОКРАШЕНО'], (255, 244, 170), [(184, 30, 40)], (150, 130, 70), pad=0.6, tilt=3), 1100, 452),
    (P(34, 26, ['ПРОДАМ', 'ГАРАЖ'], (250, 250, 240), [(34, 28, 30), (40, 60, 150)], (150, 140, 120), pad=0.7, tilt=4), 820, 410),
    (P(34, 20, ['МЕСТО', 'САНЫЧА'], (255, 252, 236), [(34, 28, 30), (184, 30, 40)], (150, 140, 120), pad=0.6, hand=True), 222, 540),
])
HOTEL = P(66, 30, ['ГОСТИНИЦА «У БАТИ»', 'МЕСТ НЕТ'], (255, 252, 236), [(184, 30, 40), (34, 28, 30)], (150, 140, 120), pad=0.8,
          hand=True, tilt=-2, weights=[1, 0.8])


def light_yard(v):
    lx, ly = v.opt(180.0, 130.0); dx, dy = v.opt(990.0, 300.0)
    return Light(amb=(0.98, 0.97, 1.06), keys=[(dx, dy, 900, (255, 200, 130), 0.4), (lx, ly, 800, (255, 210, 150), 0.3)],
                 rim=(-1, -0.3, (255, 190, 200), 0.35), grad=(1.04, 0.9))


def yard(v, t, draw=None, after=None, exhaust=None):
    def aft(big, v_):
        if exhaust is not None:
            for i in range(6):
                k = ((t - exhaust) * 1.3 + i / 6) % 1.0
                ox, oy = v_.opt(800 + 70 * k, 548 - 30 * k)
                BF.puff(big, ox, oy, 30 * v_.Z * 3 * (0.4 + k), 0.55 * (1 - k), (200, 200, 206))
        if after: after(big, v_)
    def draw2(CH, v_):
        L = Layer(v_.wcam())                                                                  # the «МЕСТО САНЫЧА» stool in the snow
        F.ell(L, (240, 566), 24, 6, (150, 96, 60), 0, (180, 120, 80), (110, 70, 44))
        for sx in (-16, 14): F.cap(L, (240 + sx, 570), (240 + sx * 1.2, 600), 3, 2.6, (110, 70, 44))
        F.outline(L, OL); CH.add(L)
        if draw: draw(CH, v_)
    big = S.world(YARD, v, t, draw2, light_yard(v), snow=(0, 0, 1280, 700), after=aft, vign=0.24)
    return big


def breath(big, v, cam, r, t, k=1.0):
    mx, my = u2w(v, cam, r['mouth'])
    ph = (t * 0.9) % 1.0
    ox, oy = v.opt(mx + 14 * ph, my - 10 * ph)
    BF.puff(big, ox, oy, 26 * v.Z * 3 * (0.5 + ph), 0.45 * k * (1 - ph), (236, 240, 250))


def keys(L, h):
    F.cap(L, (h[0] + 0.2, h[1] - 0.3), (h[0] + 0.9, h[1] - 1.1), 0.2, 0.2, (200, 200, 210))
    F.ell(L, (h[0] + 1.1, h[1] - 1.4), 0.5, 0.35, (60, 60, 70))


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Минус двадцать?! Не заводится!» — Batya in a knitted hat, frost on the brows, keys in hand, shouting at the red Lada; «-20»"""
    z = 1.32 + 0.08 * sm(min(1.0, u / 2.4))
    v = view_at(YARD, 590, 410, z, 180, 330)
    st = {}

    def draw(CH, v_):
        cam = v_.cam(575, YF + 70, YU * 1.55)
        r = B.batya(CH, cam, B.BPOSE['point'], t=t, mouth_=mouth('batya', t), expr='shout', hat=True, frost=1.0, prop_n=keys,
                    shake=0.05)
        face(v_, cam, r, 3.2); st.update(cam=cam, r=r)
    big = yard(v, t, draw, after=lambda b, v_: breath(b, v_, st['cam'], st['r'], t))
    return big


def r_selfie(t, u):
    """«Это мой батя. Мастера он не зовёт.» — Tyoma's selfie stream in the snow, Batya kicks the tyre behind him"""
    v = view_at(YARD, 600, 400, 1.0, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(540, YF + 10, YU * 1.2, flip=True)
        r = B.batya(CH, cam, B.BPOSE['fists'], t=t, mouth_=0.3, expr='angry', hat=True, frost=1.0, shake=0.06)
        face(v_, cam, r, 3.2)
        cam = v_.cam(708, 1010, 25.0, flip=True)
        r = B.tema(CH, cam, B.TPOSE['selfie'], t=t, mouth_=mouth('tema', t), expr='deadpan', prop_n=None, hand_n=F.H(9.5, 17.0), look=0.6)
        face(v_, cam, r, 2.6)
    return yard(v, t, draw, after=lambda b, v_: K.phone_ui(b, t, f'{12 + int(30 * min(1, u / 2))}'))


def r_carry(t, u):
    """«Не трогай! Я сам! Аккумулятор — домой, греть!» — Batya marches to the podyezd with the battery in both hands"""
    x = lerp(760, 880, sm(min(1.0, u / 3.2)))
    v = view_at(YARD, x + 20, 420, 1.15, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(x, YF + 20, YU * 1.4)
        r = B.batya(CH, cam, B.BPOSE['hold'], t=t, mouth_=mouth('batya', t), expr='fists', hat=True, frost=0.6,
                    prop_n=lambda L, h: B.battery(L, (h[0] - 0.6, h[1]), 1.2), lean=0.5)
        face(v_, cam, r, 3.2)
    return yard(v, t, draw)


def bed_with(CH, v, t, xs, top=470.0, tiger=True, bottle=False):
    L = Layer(v.wcam())
    for x in xs: B.battery_world(L, x, top - 8, 1.6)
    F.outline(L, OL); CH.add(L)
    S.blankets(CH, v, top, 330, 650, t, tiger=tiger)
    if bottle:
        L = Layer(v.wcam()); B.hot_water_bottle(L, 600, top + 40, 1.3); F.outline(L, OL); CH.add(L)


def r_tuck(t, u):
    """«Спи, родной. Утром заведёмся.» — the battery lies in bed on the pillow under the tiger plaid, Batya tucks it in"""
    v = view_at(BED, 620, 320, 1.08, 180, 320)

    def draw(CH, v_):
        bed_with(CH, v_, t, [520], bottle=True)
        cam = v_.cam(740, FLOOR + 6, UN, flip=True)
        r = B.batya(CH, cam, B.BPOSE['hold'], t=t, mouth_=mouth('batya', t), expr='happy', hand_n=F.H(7.6, 11.4), hand_f=F.H(6.4, 12.2))
        face(v_, cam, r, 3.2)
    return S.bedroom(v, t, draw)


def r_ira_door(t, u):
    """«Витя. Это что?» — Ira in the doorway, deadpan, looking at the battery in her bed"""
    v = view_at(BED, 900, 320, 1.0, 180, 320)

    def draw(CH, v_):
        bed_with(CH, v_, t, [520])
        cam = v_.cam(1020, FLOOR + 6, UN, flip=True)
        r = B.ira(CH, cam, B.IPOSE['hips'], t=t, mouth_=mouth('ira', t), expr='dry', specs=True)
        face(v_, cam, r, 2.6)
    return S.bedroom(v, t, draw)


def r_measure(t, u):
    """«Тридцать семь и два. Пойдёт.» — close: Batya holds the E01 thermometer to the battery: «37,2»"""
    v = view_at(BED, 600, 350, 1.4, 180, 330)
    st = {}

    def draw(CH, v_):
        bed_with(CH, v_, t, [520], bottle=True)
        cam = v_.cam(700, FLOOR + 6, UN, flip=True)
        r = B.batya(CH, cam, B.BPOSE['hold'], t=t, mouth_=mouth('batya', t), expr='smug', hand_n=F.H(9.0, 12.6),
                    prop_n=S.thermo_prop(st, 1.4, 0.1))
        face(v_, cam, r, 3.2); st['cam'] = cam
    big = S.bedroom(v, t, draw)
    S.lcd(big, v, st['cam'], st, '37,2')
    return big


def r_start(t, u, puff=False):
    """«Завелась! Я сам!» — morning yard: the Lada coughs exhaust, Batya jumps with joy"""
    v = view_at(YARD, 640, 420, 1.0, 180, 330)
    j = abs(math.sin(u * 7)) * 18 if u > 0.3 else 0

    def draw(CH, v_):
        cam = v_.cam(560, YF + 40 - j, YU * 1.35)
        r = B.batya(CH, cam, B.BPOSE['shock'], t=t, mouth_=mouth('batya', t), expr='happy', hat=True, frost=0.4)
        face(v_, cam, r, 3.2)
    big = yard(v, t, draw, exhaust=F0['start'] - 0.2)
    if puff: BF.shake(big, t, 8, 36)
    return big


def r_puff(t, u):
    return r_start(t, u + 2.0, puff=True)


QUEUE = [(870, 0), (950, 1), (1030, 2), (1110, 3)]


def queue(CH, v, t, speak=False, n=4):
    for i, (x, k) in enumerate(QUEUE[:n][::-1]):
        cam = v.cam(x, YF + 18 - i * 4, YU * 1.3, flip=True)
        r = B.neighbour(CH, cam, t, kind=k, mouth_=mouth('sosed', t) if (speak and x == 870) else 0.0, expr='happy')
        if x == 870: face(v, cam, dict(head=r['head']), 2.4)


def r_twist(t, u):
    """TWIST «Саныч! И мой погрей, а?» — the camera pans from the car to the podyezd: a queue of neighbours, each with a battery"""
    x = lerp(640, 960, sm(min(1.0, u / 0.6)))
    v = view_at(YARD, x, 420, 1.0, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(700, YF + 40, YU * 1.35)
        r = B.batya(CH, cam, B.BPOSE['shock'], t=t, mouth_=0.0, expr='shock', hat=True, frost=0.4)
        face(v_, cam, r, 3.2)
        queue(CH, v_, t, speak=True)
    big = yard(v, t, draw)
    if u < 0.35: BF.shake(big, t, 9, 40)
    return big


def r_hotel(t, u):
    """«Ну… по одному! Заселяемся!» — Batya at the podyezd door like a doorman, the neighbours file in"""
    v = view_at(YARD, 930, 400, 1.18, 180, 330)
    k = min(1.0, u / 2.6)

    def draw(CH, v_):
        for i, (x, kind) in enumerate(QUEUE[::-1]):
            xx = x - 70 * k * (1 + 0.2 * i)
            cam = v_.cam(xx, YF + 14 - i * 4, YU * 1.3, flip=True)
            B.neighbour(CH, cam, t, kind=kind, expr='happy')
        cam = v_.cam(860, YF + 34, YU * 1.45)
        r = B.batya(CH, cam, B.BPOSE['point'], t=t, mouth_=mouth('batya', t), expr='proud', hat=True, frost=0.3)
        face(v_, cam, r, 3.2)
    return yard(v, t, draw)


def r_beds(t, u):
    """«Батя открыл гостиницу. Это контент.» — Tyoma's stream: the bed full of batteries, the «ГОСТИНИЦА "У БАТИ"» sign"""
    v = view_at(BED, 560, 330, 1.0, 180, 320)

    def draw(CH, v_):
        bed_with(CH, v_, t, [380, 450, 520, 590], top=468)
        cam = v_.cam(690, 1040, 26.0, flip=True)
        r = B.tema(CH, cam, B.TPOSE['selfie'], t=t, mouth_=mouth('tema', t), expr='deadpan', prop_n=None, hand_n=F.H(9.5, 17.0), look=0.6)
        face(v_, cam, r, 2.6)

    def after(big, v_):
        D.blit(big, v_, HOTEL, 420, 300)
        K.phone_ui(big, t, '96 300')
    return S.bedroom(v, t, draw, after)


def r_ira_no(t, u):
    """«Витя. Я с аккумуляторами в одной кровати не сплю.» — Ira with her pillow under her arm, the battery bed behind"""
    v = view_at(BED, 640, 320, 1.1, 180, 320)

    def draw(CH, v_):
        bed_with(CH, v_, t, [380, 450, 520, 590], top=468)
        cam = v_.cam(760, FLOOR + 6, UN, flip=True)
        r = B.ira(CH, cam, B.IPOSE['tray'], t=t, mouth_=mouth('ira', t), expr='dry', specs=True,
                  prop_n=lambda L, h: F.ell(L, (h[0] - 1.6, h[1] - 0.8), 2.6, 1.5, (246, 246, 250), 0.2, (255, 255, 255), (206, 210, 220)))
        face(v_, cam, r, 2.6)
    return S.bedroom(v, t, draw)


def r_button(t, u):
    """«Они же тёплые!» — Batya hugs a battery to his chest, pleading"""
    v = view_at(BED, 680, 300, 1.4, 180, 300)

    def draw(CH, v_):
        bed_with(CH, v_, t, [380, 450, 520, 590], top=468)
        cam = v_.cam(700, FLOOR + 6, UN)
        r = B.batya(CH, cam, B.BPOSE['hold'], t=t, mouth_=mouth('batya', t), expr='whine', hand_n=F.H(3.2, 16.4), hand_f=F.H(2.6, 15.6),
                    prop_n=lambda L, h: B.battery(L, (h[0] - 0.4, h[1] + 0.4), 1.25))
        face(v_, cam, r, 3.2)
    return S.bedroom(v, t, draw)


def r_loop(t, u):
    return r_hook(t, 0.0)


SHOT = dict(hook=r_hook, selfie=r_selfie, carry=r_carry, tuck=r_tuck, ira_door=r_ira_door, measure=r_measure, start=r_start, puff=r_puff,
            twist=r_twist, hotel=r_hotel, beds=r_beds, ira_no=r_ira_no, button=r_button, loop=r_loop)
CUTS, NAMES = TL.CUTS, TL.NAMES


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


QUESTION = K.question('ВАША НЕ ЗАВОДИТСЯ ПРИ…?', 'ПИШИ ЦИФРУ')


def extra(big, t, shot):
    if TL.DUR - 2.4 <= t < TL.DUR - 1.0:
        O.overlay(big, QUESTION, (big.shape[1] - QUESTION.shape[1]) // 2, 230, min(1.0, (t - (TL.DUR - 2.4)) / 0.12))


SHOW = K.Show(EPI, 1, 2, ['-20', 'НЕ ЗАВОДИТСЯ?!'], hook_t=(0.06, 2.5), hook_y=250,
              stickers=[(O.sticker('ЗАВЕЛАСЬ!', fg=(255, 236, 120), size=96), F0['start'] + 0.3, TL.TWIST, 540, 520),
                        (O.sticker('ОЧЕРЕДЬ: 9', fg=(150, 210, 255), size=96), TL.TWIST + 0.3, F0['beds'], 540, 520),
                        (O.sticker('37,2 — ПОЙДЁТ', fg=(255, 255, 255), size=58), F0['measure'] + 0.4, F0['start'], 540, 470)],
              flashes=[TL.TWIST + 0.02], mosaics=[F0['tuck'], F0['start']], extra=extra,
              cap_y={'selfie': 1460, 'beds': 1480, 'tuck': 1500, 'ira_door': 1500, 'measure': 1500, 'ira_no': 1500, 'button': 1500},
              cap_default=1400)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
