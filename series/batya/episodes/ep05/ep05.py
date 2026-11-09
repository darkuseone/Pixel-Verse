"""E05 «7 ЛИШНИХ БОЛТОВ?!» — Black Friday, a «ИКЕЕВНА» wardrobe at −50 %: Batya tears up the manual («Инструкция — для слабых!»),
assembles it crooked in six hours, seven bolts left over. TWIST (the reward is the same problem): the courier rings — «Акция один плюс
один — ваш второй шкаф!» (clue: «1+1» on the boxes from the first second). The manual was in that box. «Ничего! Делов — пять минут!» —
Ira opens the first wardrobe, the door stays in her hand: «Витя. Восьмой болт.»
  python3 ep05.py test … | frames … | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from stage import view_at, Light
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import decals as D
from props import batyacast as B
from props import batyakit as K
from props import batyashots as S
from props.batyashots import mouth, u2w, face, P
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=dict(K.COL, kurier=(255, 190, 80)), slug=TL.SLUG, promo='ru',
              endcard=dict(style='batya', lang='ru', promise='ЗАВТРА: ДЕНЬ МАТЕРИ — ПОДАРОК САМИ!'))
S.init(EPI)
ROOM = S.extra_world('room')
F0 = TL.T0
OL = B.OL
INK, RED, CREAM = (34, 28, 30), (184, 30, 40), (255, 252, 236)
WALL = 456.0                     # wall base line
WX0, WX1, WTOP = 520.0, 740.0, 70.0
CB, CB_HI, CB_SH = (196, 150, 96), (222, 180, 126), (150, 108, 64)
WD, WD_HI, WD_SH = (226, 200, 160), (244, 224, 190), (184, 156, 116)

D.attach(ROOM, [
    (P(70, 30, ['НЕ ВКЛЮЧАТЬ', 'ДО 1 ЯНВАРЯ'], CREAM, [RED, INK], (150, 140, 120), pad=0.6, tilt=-3, hand=True), 330, 268),
    (P(54, 22, ['ПУЛЬТ — У ПАПЫ'], (255, 244, 170), [INK], (150, 130, 70), pad=0.5, tilt=2), 360, 420),
    (P(60, 28, ['КАЛЕНДАРЬ', 'НОЯБРЬ 2026'], CREAM, [INK, RED], (150, 140, 120), pad=0.6), 860, 420),
])
LBL = dict(
    brand=P(80, 22, ['ИКЕЕВНА'], (250, 214, 40), [(30, 60, 150)], (30, 60, 150), pad=0.4),
    sale=P(70, 30, ['ЧЁРНАЯ ПЯТНИЦА', '−50 %'], (30, 28, 30), [(255, 255, 255), (250, 214, 40)], None, pad=0.5, weights=[0.7, 1]),
    one=P(44, 30, ['1+1'], (255, 252, 236), [RED], RED, pad=0.4),
    two=P(70, 30, ['ШКАФ «ВИТЯ»', '2 ИЗ 2'], (250, 214, 40), [(30, 60, 150), INK], (30, 60, 150), pad=0.5),
    man=P(76, 24, ['ИНСТРУКЦИЯ', 'ВНУТРИ'], CREAM, [RED, INK], RED, pad=0.5, weights=[1, 0.8]),
)


# ---------------------------------------------------------------- props (world px, layer L)
def box(L, x, y, w, h):
    """cardboard box with its bottom-left at (x, y)"""
    F.poly(L, [(x, y), (x + w, y), (x + w, y - h), (x, y - h)], CB)
    F.poly(L, [(x, y - h), (x + w, y - h), (x + w - 8, y - h - 7), (x + 8, y - h - 7)], CB_HI)
    F.cap(L, (x + w * 0.45, y - h - 6), (x + w * 0.55, y), 2.2, 2.2, (214, 200, 160))


def wardrobe(CH, v, tilt=0.06, door=True, flip_door=True):
    """the crooked wardrobe against the back wall; tilt (rad) leans it to the right; flip_door: left door upside down"""
    L = Layer(v.wcam())
    bx, by = (WX0 + WX1) / 2, WALL
    def T(x, y):
        dx, dy = x - bx, y - by
        return (bx + dx * math.cos(tilt) - dy * math.sin(tilt), by + dx * math.sin(tilt) + dy * math.cos(tilt))
    F.ell(L, (bx, WALL + 4), 120, 8, (60, 40, 30))
    F.poly(L, [T(WX0, WALL), T(WX1, WALL), T(WX1, WTOP), T(WX0, WTOP)], WD)
    F.poly(L, [T(WX0 - 6, WTOP + 2), T(WX1 + 6, WTOP + 2), T(WX1 + 6, WTOP - 14), T(WX0 - 6, WTOP - 14)], WD_SH)
    mid = (WX0 + WX1) / 2
    for (x0, x1, upside) in ((WX0 + 8, mid - 2, flip_door), (mid + 2, WX1 - 8, False)):
        if not door and x0 > mid: continue
        F.poly(L, [T(x0, WALL - 30), T(x1, WALL - 30), T(x1, WTOP + 10), T(x0, WTOP + 10)], WD_HI)
        my0, my1 = (WTOP + 40, WTOP + 230) if not upside else (WALL - 230, WALL - 40)
        F.poly(L, [T(x0 + 14, my1), T(x1 - 14, my1), T(x1 - 14, my0), T(x0 + 14, my0)], (170, 196, 214))
        hy = WTOP + 200 if not upside else WALL - 90
        hx = x1 - 10 if x0 < mid else x0 + 10
        F.cap(L, T(hx, hy - 14), T(hx, hy + 14), 2.6, 2.6, (200, 170, 60))
    if not door:                                             # the empty right door hole: shelves inside
        F.poly(L, [T(mid + 2, WALL - 30), T(WX1 - 8, WALL - 30), T(WX1 - 8, WTOP + 10), T(mid + 2, WTOP + 10)], (90, 70, 50))
        for k in range(4):
            yy = WTOP + 60 + k * 80
            F.cap(L, T(mid + 4, yy), T(WX1 - 10, yy), 3, 3, WD_SH)
    F.cap(L, T(WX0 + 10, WALL - 14), T(WX1 - 10, WALL - 14), 5, 5, WD_SH)
    F.outline(L, OL); CH.add(L)


def boxes(CH, v, x, y, n=3, big=1.0):
    L = Layer(v.wcam())
    yy = y
    for k in range(n):
        w = (150 - 14 * k) * big; h = (60 - 4 * k) * big
        box(L, x + 8 * k * big - w / 2, yy, w, h); yy -= h + 7 * big
    F.outline(L, OL); CH.add(L)


def bolts(L, h):
    """seven bolts on the open palm"""
    for k, (dx, dy) in enumerate(((-1.4, -0.4), (-0.4, -0.7), (0.6, -0.5), (1.5, -0.3), (-0.9, -1.4), (0.2, -1.5), (1.1, -1.3))):
        x, y = h[0] + dx * 1.6, h[1] + dy * 1.6 - 0.6
        F.cap(L, (x - 0.7, y), (x + 0.7, y), 0.3, 0.3, (170, 172, 180), (220, 222, 230), (110, 112, 120))
        F.ell(L, (x - 0.8, y), 0.36, 0.5, (210, 212, 220))


def paper(L, h, k=0.0):
    F.poly(L, [(h[0] - 1.4, h[1] - 2.6), (h[0] + 1.2 + k, h[1] - 2.4), (h[0] + 1.0, h[1] + 0.4), (h[0] - 1.2, h[1] + 0.2)], (250, 250, 244))
    for j in range(4): F.cap(L, (h[0] - 0.9, h[1] - 2.0 + j * 0.55), (h[0] + 0.7, h[1] - 2.0 + j * 0.55), 0.08, 0.08, (120, 120, 130))


def door_panel(L, h):
    F.poly(L, [(h[0] - 1.0, h[1] - 9.0), (h[0] + 5.6, h[1] - 9.0), (h[0] + 5.6, h[1] + 8.0), (h[0] - 1.0, h[1] + 8.0)], WD_HI)
    F.poly(L, [(h[0] + 0.2, h[1] - 7.5), (h[0] + 4.4, h[1] - 7.5), (h[0] + 4.4, h[1] + 1.0), (h[0] + 0.2, h[1] + 1.0)], (170, 196, 214))
    F.ell(L, (h[0] + 5.0, h[1] + 7.0), 0.5, 0.5, (150, 152, 160))


# ---------------------------------------------------------------- world
def light_room(v):
    lx, ly = v.opt(625.0, 110.0)
    return Light(amb=(1.0, 0.95, 0.88), keys=[(lx, ly, 1400, (255, 210, 140), 0.6)], rim=(1, -0.4, (170, 196, 255), 0.35), grad=(1.03, 0.9))


def room(v, t, draw=None, after=None, plates=()):
    def aft(big, v_):
        for img, x, y in plates: D.blit(big, v_, img, x, y)
        if after: after(big, v_)
    return S.world(ROOM, v, t, draw, light_room(v), snow=(880, 100, 1000, 320), motes=(520, 120, 760, 400), after=aft)


def first_boxes(CH, v_):
    boxes(CH, v_, 330, 600, 3, 1.1)
FB_PLATES = [(LBL['brand'], 262, 580 - 40), (LBL['one'], 380, 560 - 40)]


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Семь лишних болтов?! А шкаф — стоит!» — Batya holds seven bolts on his palm to the camera, the crooked wardrobe behind"""
    z = 1.3 + 0.08 * sm(min(1.0, u / 3.0))
    v = view_at(ROOM, 600, 300, z, 180, 330)

    def draw(CH, v_):
        wardrobe(CH, v_, 0.07)
        cam = v_.cam(640, 720, 17.0)
        r = B.batya(CH, cam, B.BPOSE['stand'], t=t, mouth_=mouth('batya', t), expr='shock', hand_n=F.H(-5.0, 17.5),
                    prop_n=bolts)
        face(v_, cam, r, 3.2)
    return room(v, t, draw)


def r_flash(t, u):
    """«Шесть часов назад. Батя купил шкаф в Чёрную пятницу.» — flashback: Tyoma's stream, boxes «ИКЕЕВНА −50 % 1+1» behind"""
    v = view_at(ROOM, 520, 330, 1.0, 180, 320)

    def draw(CH, v_):
        first_boxes(CH, v_)
        cam = v_.cam(628, 1040, 26.0, flip=True)
        r = B.tema(CH, cam, B.TPOSE['selfie'], t=t, mouth_=mouth('tema', t), expr='deadpan', prop_n=None, hand_n=F.H(9.5, 17.0), look=0.6)
        face(v_, cam, r, 2.6)

    def after(big, v_):
        K.phone_ui(big, t, '8 300')
        fx.vhs(big, t, 0.6)
    return room(v, t, draw, after, plates=FB_PLATES + [(LBL['sale'], 300, 486)])


def r_tear(t, u):
    """«Инструкция — для слабых! Делов — пять минут!» — Batya tears the manual in two, boxes «1+1» behind (the clue)"""
    v = view_at(ROOM, 430, 330, 1.15, 180, 320)
    k = sm(min(1.0, max(0.0, (u - 0.5) / 0.5)))

    def draw(CH, v_):
        first_boxes(CH, v_)
        cam = v_.cam(500, 690, 16.0)
        r = B.batya(CH, cam, B.BPOSE['fists'], t=t, mouth_=mouth('batya', t), expr='smug',
                    hand_n=F.H(2.0 + 3.0 * k, 18.0), prop_n=lambda L, h: paper(L, h, 0.4),
                    hand_f=F.H(-2.0 - 3.0 * k, 18.0), prop_f=lambda L, h: paper(L, h, -0.4))
        face(v_, cam, r, 3.2)
    return room(v, t, draw, plates=FB_PLATES)


def r_door(t, u):
    """«Витя. Дверца вверх ногами.» — Ira, arms folded, by the wardrobe with its left door upside down"""
    v = view_at(ROOM, 690, 320, 0.88, 180, 330)

    def draw(CH, v_):
        wardrobe(CH, v_, 0.06)
        cam = v_.cam(830, 690, 15.5, flip=True)
        r = B.ira(CH, cam, B.IPOSE['hips'], t=t, mouth_=mouth('ira', t), expr='dry')
        face(v_, cam, r, 2.6)
    return room(v, t, draw)


def r_design(t, u):
    """«Так задумано! Это дизайн!» — Batya proudly presents the wardrobe"""
    v = view_at(ROOM, 560, 320, 0.9, 180, 330)

    def draw(CH, v_):
        wardrobe(CH, v_, 0.06)
        cam = v_.cam(430, 690, 15.5)
        r = B.batya(CH, cam, B.BPOSE['point'], t=t, mouth_=mouth('batya', t), expr='proud')
        face(v_, cam, r, 3.2)
    return room(v, t, draw)


def r_slap(t, u):
    """«Стоит как влитой!» — Batya slaps the wardrobe, it sways"""
    v = view_at(ROOM, 560, 320, 0.9, 180, 330)
    w = 0.06 + (0.05 * math.sin((u - 0.3) * 11) * math.exp(-1.2 * (u - 0.3)) if u > 0.3 else 0.0)

    def draw(CH, v_):
        wardrobe(CH, v_, w)
        cam = v_.cam(430, 690, 15.5)
        r = B.batya(CH, cam, B.BPOSE['stand'], t=t, mouth_=mouth('batya', t), expr='proud', hand_n=F.H(7.5, 17.0 + (1.0 if u < 0.3 else 0.0)))
        face(v_, cam, r, 3.2)
    return room(v, t, draw)


def r_twist(t, u):
    """«Доставка! Акция один плюс один — ваш второй шкаф!» — the courier in the doorway behind a tower of boxes «2 ИЗ 2»"""
    z = 1.0 + 0.1 * sm(min(1.0, u / 3.0))
    v = view_at(ROOM, 1000, 330, z, 180, 320)

    def draw(CH, v_):
        cam = v_.cam(1090, 640, 15.0, flip=True)
        r = B.neighbour(CH, cam, t, kind=4, mouth_=mouth('kurier', t), expr='happy', held=False)
        face(v_, cam, dict(head=r['head']), 2.4)
        boxes(CH, v_, 980, 650, 5, 1.0)
    return room(v, t, draw, plates=[(LBL['two'], 920, 600), (LBL['one'], 958, 470)])


def r_second(t, u):
    """«Второй?! Я этот шесть часов собирал!» — Batya, horrified close-up, the crooked wardrobe behind"""
    v = view_at(ROOM, 560, 280, 1.35, 180, 300)

    def draw(CH, v_):
        wardrobe(CH, v_, 0.07)
        cam = v_.cam(560, 720, 17.5)
        r = B.batya(CH, cam, B.BPOSE['shock'], t=t, mouth_=mouth('batya', t), expr='whine')
        face(v_, cam, r, 3.2)
    big = room(v, t, draw)
    if u < 0.4: fx.speed_lines(big, t, 1.0)
    return big


def r_manual(t, u):
    """«Бать. Инструкция была в этой коробке.» — Tyoma by the courier's boxes, «ИНСТРУКЦИЯ ВНУТРИ»"""
    v = view_at(ROOM, 880, 320, 1.15, 180, 320)

    def draw(CH, v_):
        boxes(CH, v_, 820, 640, 4, 1.0)
        cam = v_.cam(980, 700, 15.5, flip=True)
        r = B.tema(CH, cam, B.TPOSE['shrug'], t=t, mouth_=mouth('tema', t), expr='deadpan')
        face(v_, cam, r, 2.6)
    return room(v, t, draw, plates=[(LBL['man'], 760, 596), (LBL['one'], 800, 480)])


def r_again(t, u):
    """«Ничего! Делов — пять минут!» — Batya rolls up his sleeves in front of the new tower of boxes"""
    v = view_at(ROOM, 820, 320, 1.15, 180, 320)

    def draw(CH, v_):
        boxes(CH, v_, 900, 640, 5, 1.0)
        cam = v_.cam(740, 700, 16.5)
        r = B.batya(CH, cam, B.BPOSE['fists'], t=t, mouth_=mouth('batya', t), expr='fists')
        face(v_, cam, r, 3.2)
    return room(v, t, draw, plates=[(LBL['two'], 840, 590)])


def r_button(t, u):
    """«Витя. Восьмой болт.» — Ira holds the wardrobe door that came off in her hand"""
    v = view_at(ROOM, 700, 320, 0.95, 180, 330)

    def draw(CH, v_):
        wardrobe(CH, v_, 0.06, door=False)
        cam = v_.cam(840, 690, 15.5, flip=True)
        r = B.ira(CH, cam, B.IPOSE['stand'], t=t, mouth_=mouth('ira', t), expr='dry', hand_n=F.H(6.5, 13.0), prop_n=door_panel)
        face(v_, cam, r, 2.6)
    return room(v, t, draw)


def r_loop(t, u):
    return r_hook(t, 0.0)


SHOT = dict(hook=r_hook, flash=r_flash, tear=r_tear, door=r_door, design=r_design, slap=r_slap, twist=r_twist, second=r_second,
            manual=r_manual, again=r_again, button=r_button, loop=r_loop)
CUTS, NAMES = TL.CUTS, TL.NAMES


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


QUESTION = K.question('СКОЛЬКО БОЛТОВ ОСТАЛОСЬ?', 'ПИШИ ЦИФРУ')


def extra(big, t, shot):
    if TL.DUR - 2.4 <= t < TL.DUR - 1.0:
        q = QUESTION
        O.overlay(big, q, (big.shape[1] - q.shape[1]) // 2, 230, min(1.0, (t - (TL.DUR - 2.4)) / 0.12))


SHOW = K.Show(EPI, 1, 5, ['7 ЛИШНИХ', 'БОЛТОВ?!'], hook_t=(0.06, 2.6), hook_y=250,
              stickers=[(O.sticker('6 ЧАСОВ НАЗАД', fg=(255, 236, 120), size=70), F0['flash'] + 0.1, F0['tear'], 540, 440),
                        (O.sticker('ПРОШЛО: 6 ЧАСОВ', fg=(255, 236, 200), size=64), F0['slap'] + 0.2, TL.TWIST, 540, 420),
                        (O.sticker('1+1 = 2 ШКАФА', fg=(255, 120, 120), size=80), TL.TWIST + 0.4, F0['second'] + 1.2, 540, 430)],
              flashes=[TL.TWIST + 0.02], mosaics=[F0['flash'], F0['twist']], extra=extra,
              cap_y={'flash': 1460}, cap_default=1400)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
