"""E03 «КОВЁР — НА СНЕГ!» — first snow: Batya drags out the 40-year-old carpet to beat it on the snow. Neighbour Gosha offers a
dry-cleaning card for 1 500 — «Деньги на ветер! Снег — бесплатный!» (he pockets the card: the clue). He beats it, leaves it out for the
night «чтоб промёрз» — TWIST (the hunter asks for help): in the morning the carpet is a frozen board that won't fit through the door;
Batya quietly dials «Алло… Химчистка?» — Gosha: «Замороженный — по двойному тарифу.» — «А на снегу бесплатно было!»
  python3 ep03.py test … | frames … | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from props.batyashots import mouth, u2w, face, P
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=dict(K.COL, sosed=(150, 210, 255)), slug=TL.SLUG, promo='ru',
              endcard=dict(style='batya', lang='ru', promise='ЗАВТРА: 412 КВТ?! КТО НЕ ВЫКЛЮЧИЛ СВЕТ?!'))
S.init(EPI)
YARD = S.extra_world('yard')
F0 = TL.T0
OL = B.OL
YF, YU = 610.0, 8.6

D.attach(YARD, [
    (P(30, 12, ['ПОДЪЕЗД 3'], (60, 110, 70), [(244, 240, 220)], (30, 50, 34), pad=0.6), 978, 296),
    (P(44, 24, ['НЕ ПАРКОВАТЬСЯ!', 'ЗДЕСЬ БАБУШКИ'], (255, 252, 236), [(184, 30, 40), (34, 28, 30)], (150, 140, 120), pad=0.7,
       tilt=-2, weights=[1, 0.8]), 1110, 300),
    (P(40, 14, ['ОКРАШЕНО'], (255, 244, 170), [(184, 30, 40)], (150, 130, 70), pad=0.6, tilt=3), 1100, 452),
    (P(46, 26, ['КОВРЫ НЕ ВЫБИВАТЬ!', 'С 23:00 ДО 7:00'], (250, 250, 240), [(184, 30, 40), (34, 28, 30)], (150, 140, 120), pad=0.7,
       tilt=2, weights=[1, 0.8]), 812, 404),
    (P(34, 20, ['МЕСТО', 'САНЫЧА'], (255, 252, 236), [(34, 28, 30), (184, 30, 40)], (150, 140, 120), pad=0.6, hand=True), 222, 540),
])
CARD = P(40, 26, ['ХИМЧИСТКА', 'КОВРОВ', '1 500 ₽'], (250, 250, 255), [(40, 70, 160), (40, 70, 160), (184, 30, 40)], (60, 70, 90),
         pad=0.6, weights=[0.8, 0.8, 1])
TAG = P(24, 12, ['40 ЛЕТ'], (255, 244, 170), [(184, 30, 40)], (150, 130, 70), pad=0.5)
CR, CR_HI, CR_SH, CR_PAT = (176, 36, 44), (206, 70, 72), (126, 20, 30), (232, 196, 120)


def light_yard(v, night=False):
    lx, ly = v.opt(180.0, 130.0); dx, dy = v.opt(990.0, 300.0)
    if night:
        return Light(amb=(0.62, 0.68, 0.98), keys=[(dx, dy, 900, (255, 200, 130), 0.6), (lx, ly, 900, (255, 210, 150), 0.5)],
                     rim=(-1, -0.3, (170, 196, 255), 0.4), grad=(1.0, 0.85))
    return Light(amb=(0.98, 0.97, 1.06), keys=[(dx, dy, 900, (255, 200, 130), 0.4), (lx, ly, 800, (255, 210, 150), 0.3)],
                 rim=(-1, -0.3, (255, 190, 200), 0.35), grad=(1.04, 0.9))


def yard(v, t, draw=None, after=None, night=False):
    def draw2(CH, v_):
        L = Layer(v_.wcam())
        F.ell(L, (240, 566), 24, 6, (150, 96, 60), 0, (180, 120, 80), (110, 70, 44))
        for sx in (-16, 14): F.cap(L, (240 + sx, 570), (240 + sx * 1.2, 600), 3, 2.6, (110, 70, 44))
        F.outline(L, OL); CH.add(L)
        if draw: draw(CH, v_)
    def aft(big, v_):
        if night: fx.grade(big, (0.55, 0.6, 0.85), (0, 0, 10))
        if after: after(big, v_)
    return S.world(YARD, v, t, draw2, light_yard(v, night), snow=(0, 0, 1280, 700), after=aft, vign=0.3 if night else 0.24)


def carpet_flat(CH, v, x0, y0, w, h, frost=0.0, print_=False):
    """the carpet laid on the snow (slight perspective), oriental pattern; print_: the dirty «imprint» next to it"""
    L = Layer(v.wcam())
    if print_:
        F.poly(L, [(x0 + w + 20, y0), (x0 + 2 * w + 10, y0), (x0 + 2 * w + 34, y0 + h), (x0 + w + 40, y0 + h)], (160, 150, 150))
    F.poly(L, [(x0, y0), (x0 + w, y0), (x0 + w + 24, y0 + h), (x0 - 24, y0 + h)], CR)
    F.poly(L, [(x0 + 12, y0 + 6), (x0 + w - 12, y0 + 6), (x0 + w + 8, y0 + h - 8), (x0 - 8, y0 + h - 8)], CR_SH)
    cx, cy = x0 + w / 2, y0 + h / 2
    F.poly(L, [(cx, cy - h * 0.32), (cx + w * 0.28, cy), (cx, cy + h * 0.32), (cx - w * 0.28, cy)], CR_PAT)
    F.poly(L, [(cx, cy - h * 0.18), (cx + w * 0.15, cy), (cx, cy + h * 0.18), (cx - w * 0.15, cy)], CR)
    for k in range(6):
        F.dot(L, (x0 + 18 + k * (w - 36) / 5, y0 + 12), CR_PAT, 3); F.dot(L, (x0 + 4 + k * (w - 8) / 5, y0 + h - 12), CR_PAT, 3)
    if frost:
        for k in range(30):
            a, b, c, d, e = BF.SEED[k]
            F.dot(L, (x0 - 20 + a * (w + 40), y0 + b * h), (236, 246, 255), 1.5 + 2 * c * frost)
    F.outline(L, OL); CH.add(L)


def carpet_board(CH, v, x, y, w=150, h=250, tilt=0.0):
    """the frozen carpet standing upright like a board (bottom-centre x, y), icicles on the top edge"""
    L = Layer(v.wcam())
    c, s_ = math.cos(tilt), math.sin(tilt)
    def T(px, py): return (x + px * c - py * s_, y + px * s_ + py * c)
    F.poly(L, [T(-w / 2, -h), T(w / 2, -h), T(w / 2, 0), T(-w / 2, 0)], CR)
    F.poly(L, [T(-w / 2 + 10, -h + 10), T(w / 2 - 10, -h + 10), T(w / 2 - 10, -10), T(-w / 2 + 10, -10)], CR_SH)
    F.poly(L, [T(0, -h * 0.82), T(w * 0.3, -h * 0.5), T(0, -h * 0.18), T(-w * 0.3, -h * 0.5)], CR_PAT)
    F.poly(L, [T(0, -h * 0.68), T(w * 0.15, -h * 0.5), T(0, -h * 0.32), T(-w * 0.15, -h * 0.5)], CR)
    for k in range(7):
        xa = -w / 2 + 8 + k * (w - 16) / 6
        F.poly(L, [T(xa - 4, -h), T(xa + 4, -h), T(xa, -h + 16 + 8 * (k % 3))], (220, 236, 255))
    for k in range(40):
        a, b, cc, d, e = BF.SEED[60 + k]
        F.dot(L, T(-w / 2 + a * w, -h + b * h), (236, 246, 255), 1.4 + 1.6 * cc)
    F.outline(L, OL); CH.add(L)


def roll_on_shoulder(L, h):
    """carpet roll held over the shoulder (unit coords, hand h)"""
    F.cap(L, (h[0] - 9.0, h[1] - 2.4), (h[0] + 4.0, h[1] + 0.2), 1.5, 1.5, CR, CR_HI, CR_SH)
    for k in range(5): F.cap(L, (h[0] - 8.0 + k * 2.5, h[1] - 2.9 + k * 0.5), (h[0] - 7.6 + k * 2.5, h[1] - 1.5 + k * 0.5), 0.18, 0.18, CR_PAT)
    F.ell(L, (h[0] + 4.0, h[1] + 0.2), 0.8, 1.5, CR_SH); F.ell(L, (h[0] + 4.0, h[1] + 0.2), 0.4, 0.9, CR_PAT)


def beater(L, h, t=0.0):
    """wicker carpet beater (выбивалка)"""
    a = -1.2 + 0.9 * math.sin(t * 9)
    d = (math.cos(a), math.sin(a))
    tip = (h[0] + d[0] * 3.4, h[1] + d[1] * 3.4)
    F.cap(L, h, tip, 0.16, 0.16, (190, 150, 90))
    F.ell(L, (tip[0] + d[0] * 1.0, tip[1] + d[1] * 1.0), 1.1, 0.9, (196, 156, 96))
    F.ell(L, (tip[0] + d[0] * 1.0, tip[1] + d[1] * 1.0), 0.6, 0.45, (120, 90, 50))


def phone(L, h):
    F.poly(L, [(h[0] - 0.3, h[1] - 1.9), (h[0] + 0.5, h[1] - 1.9), (h[0] + 0.5, h[1] + 0.1), (h[0] - 0.3, h[1] + 0.1)], (30, 30, 36))


def gosha(CH, v, t, x, flip=True, card=True, talk=True, un=None):
    cam = v.cam(x, YF + 20, (un or YU * 1.4), flip=flip)
    r = B.neighbour(CH, cam, t, kind=1, mouth_=mouth('sosed', t) if talk else 0.0, expr='happy', held=False)
    face(v, cam, dict(head=r['head']), 2.4)
    return cam, r


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Сорок лет ковру! Первый снег — на снег его!» — Batya marches out with a huge carpet roll on his shoulder, first snow"""
    z = 1.3 + 0.08 * sm(min(1.0, u / 3.0))
    v = view_at(YARD, 640, 410, z, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(lerp(600, 640, u / 3.5), YF + 70, YU * 1.55)
        r = B.batya(CH, cam, dict(B.BPOSE['stand'], bn=-1), t=t, mouth_=mouth('batya', t), expr='proud', hat=True, frost=0.3,
                    hand_n=F.H(3.0, 15.0), prop_n=roll_on_shoulder)
        face(v_, cam, r, 3.2)
    big = yard(v, t, draw)
    D.blit(big, v, TAG, 470, 300)
    return big


def r_offer(t, u):
    """«Саныч, химчистка — полторы тысячи. Вот визитка.» — neighbour Gosha holds out a dry-cleaning card"""
    v = view_at(YARD, 820, 420, 1.2, 180, 330)
    st = {}

    def draw(CH, v_):
        cam = v_.cam(730, YF + 30, YU * 1.45)
        r = B.batya(CH, cam, B.BPOSE['stand'], t=t, mouth_=0.0, expr='smug', hat=True, frost=0.3)
        face(v_, cam, r, 3.2)
        cam2, r2 = gosha(CH, v_, t, 900)
        st['h'] = u2w(v_, cam2, F.H(3.2, 15.0))
    big = yard(v, t, draw)
    D.blit(big, v, CARD, st['h'][0] - 30, st['h'][1] - 26)
    return big


def r_scorn(t, u):
    """«Деньги на ветер! Снег — бесплатный!» — close on Batya, he stuffs the card into his vest pocket anyway (the clue)"""
    v = view_at(YARD, 700, 380, 1.4, 180, 300)

    def draw(CH, v_):
        cam = v_.cam(700, YF + 40, YU * 1.6)
        hand = F.H(-1.0 + 1.4 * sm(min(1.0, u / 1.4)), 16.0)
        r = B.batya(CH, cam, B.BPOSE['stand'], t=t, mouth_=mouth('batya', t), expr='smug', hat=True, frost=0.3, hand_f=hand,
                    prop_f=lambda L, h: F.poly(L, [(h[0] - 0.6, h[1] - 0.6), (h[0] + 0.7, h[1] - 0.6), (h[0] + 0.7, h[1] + 0.2), (h[0] - 0.6, h[1] + 0.2)],
                                               (250, 250, 255)))
        face(v_, cam, r, 3.2)
    return yard(v, t, draw)


def r_beat(t, u):
    """«Раз! Два! Вот так чистят!» — the carpet on the snow, Batya whacks it with the beater, dust clouds and a dirty imprint"""
    v = view_at(YARD, 600, 470, 1.05, 180, 330)
    hit = (u * 2.2) % 1.0 < 0.25

    def draw(CH, v_):
        carpet_flat(CH, v_, 430, 600, 220, 70, print_=True)
        cam = v_.cam(720, YF + 60, YU * 1.45, flip=True)
        r = B.batya(CH, cam, B.BPOSE['point'], t=t, mouth_=mouth('batya', t), expr='fists', hat=True, frost=0.2,
                    prop_n=lambda L, h: beater(L, h, t))
        face(v_, cam, r, 3.2)

    def after(big, v_):
        for i in range(5):
            k = ((u * 2.2) + i / 5) % 1.0
            ox, oy = v_.opt(470 + 160 * ((i * 0.37) % 1.0), 620 - 80 * k)
            BF.puff(big, ox, oy, 40 * v_.Z * 3 * (0.5 + k), 0.5 * (1 - k), (150, 130, 110))
        if hit: BF.shake(big, t, 6, 40)
    return yard(v, t, draw, after)


def r_frost(t, u):
    """«Батя оставил его на ночь. Чтоб промёрз.» — night stream: Tyoma in the frost, the carpet glitters on the snow behind"""
    v = view_at(YARD, 600, 440, 1.0, 180, 330)

    def draw(CH, v_):
        carpet_flat(CH, v_, 430, 600, 220, 70, frost=1.0, print_=True)
        cam = v_.cam(708, 1010, 25.0, flip=True)
        r = B.tema(CH, cam, B.TPOSE['selfie'], t=t, mouth_=mouth('tema', t), expr='deadpan', prop_n=None, hand_n=F.H(9.5, 17.0), look=0.6)
        face(v_, cam, r, 2.6)
    return yard(v, t, draw, after=lambda b, v_: K.phone_ui(b, t, '2 140'), night=True)


def r_twist(t, u):
    """TWIST «Не гнётся… Не лезет!» — morning: the carpet is a frozen board; Batya rams it into the podyezd door, it won't go"""
    v = view_at(YARD, 930, 400, 1.12, 180, 330)
    push = 6 * math.sin(u * 14) if u > 0.3 else 0

    def draw(CH, v_):
        carpet_board(CH, v_, 900 + push, 560, 150, 250, tilt=0.12)
        cam = v_.cam(800 + push, YF + 30, YU * 1.45)
        r = B.batya(CH, cam, B.BPOSE['hold'], t=t, mouth_=mouth('batya', t), expr='shout', hat=True, frost=1.0, hand_n=F.H(6.4, 14.0),
                    hand_f=F.H(5.6, 16.0), shake=0.08)
        face(v_, cam, r, 3.2)
    big = yard(v, t, draw)
    if u < 0.4: BF.shake(big, t, 9, 40)
    return big


def r_window(t, u):
    """«Витя. Он в дверь не пройдёт.» — Ira on the porch in her coat, deadpan"""
    v = view_at(YARD, 980, 400, 1.3, 180, 330)

    def draw(CH, v_):
        cam = v_.cam(1010, 520, YU * 1.25, flip=True)
        r = B.ira(CH, cam, B.IPOSE['hips'], t=t, mouth_=mouth('ira', t), expr='dry', coat=True, scarf=True, specs=True)
        face(v_, cam, r, 2.6)
        carpet_board(CH, v_, 900, 600, 150, 250, tilt=0.12)
    return yard(v, t, draw)


def r_call(t, u):
    """«Алло… Химчистка?» — Batya, eyes down, phone at his ear, the card in his hand"""
    v = view_at(YARD, 760, 380, 1.4, 180, 300)
    st = {}

    def draw(CH, v_):
        cam = v_.cam(760, YF + 40, YU * 1.6)
        r = B.batya(CH, cam, dict(B.BPOSE['stand'], n=(3.2, 23.0)), t=t, mouth_=mouth('batya', t), expr='sad', hat=True, frost=0.6,
                    prop_n=phone, hand_f=F.H(3.0, 15.6))
        face(v_, cam, r, 3.2); st['h'] = u2w(v_, cam, F.H(3.0, 15.6))
    big = yard(v, t, draw)
    D.blit(big, v, CARD, st['h'][0] - 30, st['h'][1] - 20)
    return big


def r_tariff(t, u):
    """«Замороженный — по двойному тарифу.» — Gosha, smug, the card in hand, next to the frozen carpet"""
    v = view_at(YARD, 880, 400, 1.3, 180, 330)
    st = {}

    def draw(CH, v_):
        carpet_board(CH, v_, 800, 600, 150, 250, tilt=0.12)
        cam2, r2 = gosha(CH, v_, t, 930, un=YU * 1.55)
        st['h'] = u2w(v_, cam2, F.H(3.2, 15.0))
    big = yard(v, t, draw)
    D.blit(big, v, P(40, 26, ['ХИМЧИСТКА', 'КОВРОВ', '3 000 ₽'], (250, 250, 255), [(40, 70, 160), (40, 70, 160), (184, 30, 40)],
                     (60, 70, 90), pad=0.6, weights=[0.8, 0.8, 1]), st['h'][0] - 30, st['h'][1] - 26)
    return big


def r_content(t, u):
    """«Это контент.» — Tyoma's stream, the frozen carpet board and Batya behind"""
    v = view_at(YARD, 860, 420, 1.0, 180, 330)

    def draw(CH, v_):
        carpet_board(CH, v_, 820, 600, 150, 250, tilt=0.12)
        cam = v_.cam(708 + 220, 1010, 25.0, flip=True)
        r = B.tema(CH, cam, B.TPOSE['selfie'], t=t, mouth_=mouth('tema', t), expr='deadpan', prop_n=None, hand_n=F.H(9.5, 17.0), look=0.6)
        face(v_, cam, r, 2.6)
    return yard(v, t, draw, after=lambda b, v_: K.phone_ui(b, t, '211 000'))


def r_button(t, u):
    """«А на снегу бесплатно было!» — Batya hugs the frozen carpet, whining"""
    v = view_at(YARD, 860, 380, 1.35, 180, 300)

    def draw(CH, v_):
        carpet_board(CH, v_, 900, 600, 150, 250, tilt=0.12)
        cam = v_.cam(820, YF + 40, YU * 1.6)
        r = B.batya(CH, cam, B.BPOSE['hold'], t=t, mouth_=mouth('batya', t), expr='whine', hat=True, frost=1.0, hand_n=F.H(5.6, 17.0),
                    hand_f=F.H(5.0, 18.0))
        face(v_, cam, r, 3.2)
    return yard(v, t, draw)


def r_loop(t, u):
    return r_hook(t, 0.0)


SHOT = dict(hook=r_hook, offer=r_offer, scorn=r_scorn, beat=r_beat, frost=r_frost, twist=r_twist, window=r_window, call=r_call,
            tariff=r_tariff, content=r_content, button=r_button, loop=r_loop)
CUTS, NAMES = TL.CUTS, TL.NAMES


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


QUESTION = K.question('СКОЛЬКО ЛЕТ КОВРУ?', 'ПИШИ ЦИФРУ')


def extra(big, t, shot):
    if TL.DUR - 2.4 <= t < TL.DUR - 1.0:
        O.overlay(big, QUESTION, (big.shape[1] - QUESTION.shape[1]) // 2, 230, min(1.0, (t - (TL.DUR - 2.4)) / 0.12))


SHOW = K.Show(EPI, 1, 3, ['КОВЁР —', 'НА СНЕГ!'], hook_t=(0.06, 2.6), hook_y=250,
              stickers=[(O.sticker('ДОСКА!', fg=(170, 214, 255), size=110), TL.TWIST + 0.3, F0['window'], 540, 520),
                        (O.sticker('ВЖУХ!', fg=(255, 236, 120), size=80), F0['beat'] + 0.2, F0['frost'], 540, 470),
                        (O.sticker('НОЧЬ', fg=(200, 220, 255), size=70), F0['frost'] + 0.1, F0['frost'] + 1.4, 540, 560)],
              flashes=[TL.TWIST + 0.02], mosaics=[F0['frost'], F0['twist']], extra=extra,
              cap_y={'frost': 1460, 'content': 1460}, cap_default=1400)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
