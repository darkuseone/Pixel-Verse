"""S02E03 «Сорок банок» — баба Зина leaves 40 jars of pickles at Valera's door («Банки — вернёшь»). «Операция «Раздача»»: Тамара has her own
thirty, УК «Уют» takes jars «по графику»; at home the pantry buries him. TWIST: the label reads «ВАЛЕРА 2025» — his own jars, given to
Зина a year ago (sepia flashback). «Круговорот банок в природе.» Cat: «Записал.»; loop — баба Люба with forty more: «Вареньице.»
  python3 s2e03.py test 1 5 20 | frames t… | all [4] | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import stage as ST
from stage import view_at, View, Chars, Light, shadow
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import jars as J
from props import bytfx as B
from props import panelka as PK
from props import vikit as K
from props import decals as D
from props import rusigns as R
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG,
              endcard=dict(style='winter', lang='ru', promise='ЗАВТРА: ПОВЕРКА СЧЁТЧИКОВ'))
talk = EPI.talk
CUTS, NAMES = TL.CUTS + [TL.DUR], TL.NAMES                  # per-shot render: python3 s2e03.py shots <i|name>
INK, RED, BLUE, PAPER, GREEN = (34, 30, 30), (176, 30, 34), (40, 60, 150), (240, 234, 214), (40, 110, 50)
W = PK.build()
SHOP, CNT, CNTXY = W['shop'], W['counter'], W['counter_xy']


def world(name):
    return PK.q(Image.open(PK.BG / f'{name}.png').convert('RGB'))


LAND = world('landing')
PANT = world('pantry')
ZHEK = world('zhek')

D.attach(LAND, [
    (R.plate(44, 20, ['КВ. 43'], bg=(230, 220, 190), colors=[INK], border=INK, pad=2), 313, 170),
    (R.plate(44, 20, ['КВ. 44'], bg=(230, 220, 190), colors=[INK], border=INK, pad=2), 668, 170),
    (R.plate(60, 40, ['БАНКИ', 'ВЕРНУТЬ!', '— ЗИНА'], bg=PAPER, colors=[RED, RED, BLUE], border=(120, 100, 70), pad=2, tilt=-4), 492, 250),
    (R.plate(84, 26, ['ОГУРЦЫ НЕ', 'ВЫБРАСЫВАТЬ'], bg=(250, 230, 120), colors=[INK, RED], border=INK, pad=2, tilt=3), 1060, 470),
])
D.attach(PANT, [
    (R.plate(64, 22, ['ОГУРЦЫ 2019'], bg=PAPER, colors=[GREEN], border=(120, 100, 70), pad=2, tilt=-3), 860, 238),
    (R.plate(70, 22, ['НЕ ОТКРЫВАТЬ!'], bg=PAPER, colors=[RED], border=RED, pad=2, tilt=2), 400, 300),
    (R.plate(52, 22, ['ДЛЯ ГОСТЕЙ'], bg=(236, 236, 230), colors=[BLUE], border=BLUE, pad=2), 1110, 330),
])
D.attach(ZHEK, [
    (R.plate(150, 40, ['УК «УЮТ»', 'ДИСПЕТЧЕРСКАЯ'], bg=(236, 240, 246), colors=[BLUE, INK], border=(60, 70, 120), weights=[1, 0.55],
             pad=3), 470, 70),
    (R.plate(96, 50, ['ПРИЁМ БАНОК', 'ПО ГРАФИКУ'], bg=(250, 230, 120), colors=[INK, RED], border=INK, pad=2.5, tilt=-3), 980, 150),
])
D.attach(SHOP, [
    (R.plate(80, 26, ['БАНКИ', 'НЕ ПРИНИМАЕМ'], bg=PAPER, colors=[RED, INK], border=RED, pad=2, tilt=-3), 1010, 300),
])
NOTEBOOK = R.plate(46, 20, ['ЖУРНАЛ', 'ЖАЛОБ'], bg=(70, 110, 170), colors=[(250, 240, 200), (250, 240, 200)], border=INK, pad=1.5)
LBL19 = R.plate(30, 13, ['ОГУРЦЫ', '2019'], bg=(240, 232, 210), colors=[GREEN, INK], border=None, pad=1)
LBL25 = R.plate(40, 18, ['ВАЛЕРА', '2025'], bg=(240, 232, 210), colors=[RED, INK], border=None, pad=1)

# ---------------------------------------------------------------- positions
V_DOOR = (565.0, 640.0, 13.5)            # Valera on the landing, facing left (his leatherette door with the jar mountain)
PILE_D = (335.0, 606.0, 7, 58.0)         # jar mountain in front of his door: cx, floor, rows, jar height
Z_WALK = (680.0, 640.0, 13.5)            # баба Зина walking off to the stairs (facing right)
NX, NY, NU = 680.0, 412.0, 17.0          # Нина Петровна in the office bathtub (S01 callback), facing left
V_PANT = (640.0, 700.0, 15.0)
PILE_P = (640.0, 716.0, 4, 68.0)
V_HOLD = (600.0, 770.0, 17.0)
JAR_H = 92.0
L_DOOR = (620.0, 640.0, 13.5)            # баба Люба with more jars (facing left)


def mouth(who, t, k=1.6):
    return min(1.0, talk(who, t) * k)


def begin(Z):
    ST.set_px(ST.px_for_zoom(Z))
    return Chars(), Chars()


def light(v, lamp, col=(255, 214, 150), amb=(1.0, 0.98, 0.96), a=0.55, r=900):
    lx, ly = v.opt(*lamp)
    return Light(amb=amb, keys=[(lx, ly, r, col, a)], rim=(-1, -0.4, (200, 216, 255), 0.3), grad=(1.04, 0.92))


def valera(CH, v, t, pos, pose='stand', expr='angry', flip=False, **kw):
    x, y, un = pos
    return F.valera(CH, v.cam(x, y, un, flip=flip), F.VPOSE[pose] if isinstance(pose, str) else pose, t, mouth('valera', t), expr,
                    'home', stubble=1.0, **kw)


def to_world(pos, pt, flip=False):
    x, y, un = pos
    return x + (pt[0] - 1000) * un * (-1 if flip else 1), y + (pt[1] - 1000) * un


def sepia(big):
    g = big.astype(np.float32).mean(2)
    big[:] = np.clip(np.stack([g * 1.08 + 10, g * 0.94 + 4, g * 0.74], 2), 0, 255).astype(np.uint8)


# ---------------------------------------------------------------- landing (hook, Зина, flashback, Люба, loop)
def landing(v, t, draw=None, pile=True, label=False, fall=None):
    CH, FX = begin(v.Z)
    big = v.bg()
    top = None
    if pile:
        cx, base, rows, h = PILE_D
        top = J.pile(CH, v, cx, base, rows, h)
    if draw: draw(CH, v, top)
    if fall is not None: J.avalanche(CH, v, t, 230, 120, 640, 640, fall, n=26, h=58)
    CH.comp(big, light(v, (552.0, 60.0), a=0.6))
    if label and top:
        D.blit(big, v, LBL19, top[0] - 15, top[1] + 58 * 0.58 + 2, ws=4)
    fx.vignette(big, 0.3)
    return big, top


def r_hook(t, u):
    """«Сорок банок?! Мне одному?!» — a mountain of jars to the ceiling in front of his door; he panics"""
    x, y, un = V_DOOR
    v = view_at(LAND, 440, 380, 1.2 + 0.05 * u, 180, 330)

    def draw(CH, v_, top):
        valera(CH, v_, t, V_DOOR, 'shrug', 'shout', flip=True)
    big, _ = landing(v, t, draw, label=True)
    if u < 0.3: B.shake(big, t, 6, 36)
    return big


def r_zina(t, u):
    """«Огурчики. А банки — вернёшь.» — Зина trots off to the stairs without looking back"""
    x, y, un = Z_WALK
    xx = x + 70 * u
    v = view_at(LAND, 610 + 50 * u, 380, 1.0, 180, 330)

    def draw(CH, v_, top):
        F.babushka(CH, v_.cam(xx, y - 3 * abs(math.sin(t * 7)), un), t, 'zina', 'stand', mouth('zina', t), 'smug', prop_n=F.string_bag)
        valera(CH, v_, t, V_DOOR, 'shrug', 'shock')
    big, _ = landing(v, t, draw)
    return big


def r_cat_top(t, u):
    """«Огурцы. Урожай девятнадцатого.» — the cat on the top jar like on a throne"""
    cx, base, rows, h = PILE_D
    tx, ty = cx, base - rows * h * 0.98                                      # top jar lid (pile is symmetric)
    un = 5.5
    v = view_at(LAND, tx + 18, ty - 20, 2.4 + 0.06 * u, 180, 330)

    def draw(CH, v_, top):
        F.cat(CH, v_.cam(top[0] - 22, top[1] + 4, un), t=t, pose='loaf', mouth=mouth('cat', t, 2.0), lid=0.6, tail=0.2, expr='smug')
    big, _ = landing(v, t, draw, label=True)
    return big


def r_shop(t, u):
    """«У меня своих тридцать. Пакет — девяносто.» — Тамара behind the till with her own wall of jars; Valera offers one"""
    v = view_at(SHOP, 985, 330, 0.8 + 0.03 * u, 180, 330)
    CH, FX = begin(v.Z)
    big = v.bg()
    J.pile(CH, v, 1000, 470, 5, 50.0, seed=2)
    J.pile(CH, v, 1235, 470, 5, 50.0, seed=5)
    TX, TY, TU = PK.SH_TAMARA
    F.tamara(CH, v.cam(TX, TY, TU, flip=True), t, mouth('tamara', t), 'bored', gum=0.5 + 0.5 * math.sin(t * 9))
    CH.comp(big, K.light_shop(v))
    K.occlude(big, v, CNT, CNTXY)
    CH2 = Chars()
    VX, VY, VU = PK.SH_VALERA
    shadow(big, v, VX + 12, VY, 6 * VU, 0.9 * VU)
    F.valera(CH2, v.cam(VX, VY, VU), F.VPOSE['hold'], t, mouth('valera', t), 'proud', 'street', stubble=1.0,
             prop_n=lambda L, h: J.jar(L, h[0] + 0.6, h[1] + 1.8, 4.4, 'cuke'))
    CH2.comp(big, K.light_shop(v))
    fx.vignette(big, 0.3)
    return big


def r_nina(t, u):
    """«Банки принимаем по графику.» — in the УК office, behind Нина's bathtub, a whole wall of jars"""
    x, y = NX - 1.9 * NU, NY - 10.2 * NU
    v = view_at(ZHEK, x - 30, y + 60, 1.45 + 0.05 * u, 180, 330)
    CH, FX = begin(v.Z)
    big = v.bg()
    J.pile(CH, v, 470, 450, 6, 56.0, seed=1)
    J.pile(CH, v, 900, 450, 6, 56.0, seed=4)
    F.nina(CH, v.cam(NX, NY, NU, flip=True), t, mouth('nina', t), 'smug', True)
    lx, ly = v.opt(632.0, 30.0)
    CH.comp(big, Light(amb=(0.98, 1.02, 0.98), keys=[(lx, ly, 1400, (230, 255, 236), 0.4)], rim=(1, -0.3, (196, 220, 255), 0.3),
                       grad=(1.05, 0.92)))
    B.steam(big, v, t, 830, 395, -99, n=8, rise=190, size=40, a=0.45)
    fx.vignette(big, 0.3)
    return big


# ---------------------------------------------------------------- pantry
def pantry(v, t, draw=None, pile=False, fall=None):
    CH, FX = begin(v.Z)
    big = v.bg()
    if draw: draw(CH, v)
    top = None
    if pile:
        cx, base, rows, h = PILE_P
        top = J.pile(CH, v, cx, base, rows, h, seed=7)
    if fall is not None: J.avalanche(CH, v, t, 480, 120, 820, 716, fall, n=28, h=68)
    CH.comp(big, light(v, (960.0, 70.0), (255, 210, 140), amb=(0.98, 0.95, 0.9), a=0.7))
    fx.motes(FX, v, t, 700, 100, 1200, 600, n=40, col=(255, 230, 180))
    FX.comp(big)
    fx.vignette(big, 0.3)
    return big, top


def r_buried(t, u):
    """«Двадцать лет в армии… склад так не забивал!» — the pantry door opens, an avalanche of jars buries him to the chin"""
    v = view_at(PANT, 640, 400, 1.0 + 0.04 * u, 180, 330)
    k = u / 0.7

    def draw(CH, v_):
        valera(CH, v_, t, V_PANT, 'shout' if k < 1 else 'strain', 'shock', hat=None)
    big, _ = pantry(v, t, draw, pile=k >= 1, fall=min(1.0, k) if k < 1.2 else None)
    if k < 1.2: B.shake(big, t, 10, 40)
    return big


def held_jar(CH, v, t, pos, expr='shock', label=True):
    """Valera holds one jar up to the bulb; returns the jar's (x, bottom) in world px"""
    r = valera(CH, v, t, pos, dict(F.VPOSE['hold'], n=(6.0, 19.5), f=(5.2, 20.2)), expr, hat=None)
    hx, hy = to_world(pos, r['hand_n'])
    L = Layer(v.wcam())
    J.jar(L, hx + 6, hy + JAR_H * 0.45, JAR_H, 'cuke')
    F.outline(L); CH.add(L)
    return hx + 6, hy + JAR_H * 0.45


def r_label(t, u):
    """TWIST: he lifts a jar to the light — the label reads «ВАЛЕРА 2025». Push-in, flash, sticker «ЭТО МОИ?!»"""
    x, y, un = V_HOLD
    k = sm(u / 0.35)
    v = view_at(PANT, lerp(650, 690, k), lerp(430, 470, k), lerp(1.6, 2.5, k), 180, 330)
    out = {}

    def draw(CH, v_):
        out['j'] = held_jar(CH, v_, t, V_HOLD, 'shock')
    big, _ = pantry(v, t, draw)
    jx, jb = out['j']
    D.blit(big, v, LBL25, jx - 20, jb - JAR_H * 0.41, ws=4)
    return big


def r_whisper(t, u):
    """«Круговорот банок… в природе.» — he stares at the jar, the pantry full of the same jars behind him"""
    x, y, un = V_HOLD
    fx_, fy_ = K.face_w(x, y, un, h=20.8)
    v = view_at(PANT, fx_ + 40, fy_ + 50, 1.7 + 0.05 * u, 180, 330)
    out = {}

    def draw(CH, v_):
        out['j'] = held_jar(CH, v_, t, V_HOLD, 'normal')
    big, _ = pantry(v, t, draw)
    jx, jb = out['j']
    D.blit(big, v, LBL25, jx - 20, jb - JAR_H * 0.41, ws=4)
    return big


def r_flashback(t, u):
    """«Берите, Зинаида Петровна! Банки — вернёте!» — a year ago, sepia: Valera hands Зина forty jars himself"""
    v = view_at(LAND, 575, 380, 1.05, 180, 330)

    def draw(CH, v_, top):
        valera(CH, v_, t, (460.0, 640.0, 13.5), 'hold', 'proud', prop_n=lambda L, h: J.jar(L, h[0] + 0.6, h[1] + 1.8, 4.6, 'cuke'))
        F.babushka(CH, v_.cam(690.0, 640.0, 13.5, flip=True), t, 'zina', 'stand', 0.0, 'smug', prop_n=F.string_bag)
    big, _ = landing(v, t, draw)
    sepia(big)
    if int(t * 24) % 7 == 0: big[::6] = (big[::6] * 0.8).astype(np.uint8)            # old-film flicker lines
    return big


def r_cat_log(t, u):
    """«Записал.» — the cat on top of the pantry pile crunches a pickle, writes the complaint log; the two-choice question"""
    cx, base, rows, h = PILE_P
    tx, ty = cx, base - rows * h * 0.98
    v = view_at(PANT, tx + 30, ty - 30, 2.2 + 0.05 * u, 180, 320)

    def draw(CH, v_):
        pass
    CH, FX = begin(v.Z)
    big = v.bg()
    top = J.pile(CH, v, cx, base, rows, h, seed=7)
    cam = v.cam(top[0] - 24, top[1] + 4, 6.0)
    F.cat(CH, cam, t=t, pose='loaf', mouth=max(mouth('cat', t, 2.0), 0.3 if u < 1.3 else 0.0), lid=0.65, tail=0.3)
    if u < 1.4:                                                                       # the pickle he crunches
        L = Layer(cam); F.cap(L, F.H(6.4, 6.0), F.H(9.0, 6.6), 0.6, 0.5, (90, 130, 50), (130, 170, 80), (60, 90, 30)); F.outline(L)
        CH.add(L)
    CH.comp(big, light(v, (960.0, 70.0), (255, 210, 140), amb=(0.98, 0.95, 0.9), a=0.7))
    D.blit(big, v, NOTEBOOK, top[0] + 30, top[1] - 6, ws=4)
    fx.vignette(big, 0.3)
    return big


def r_lyuba(t, u, loop=False):
    """«Вареньице.» — doorbell: баба Люба with another forty jars; loop -> the avalanche again"""
    v = view_at(LAND, 540, 380, 1.1, 180, 330)

    def draw(CH, v_, top):
        J.pile(CH, v_, 820, 640, 5, 56.0, seed=9)
        F.babushka(CH, v_.cam(*L_DOOR, flip=True), t, 'lyuba', 'stand', mouth('lyuba', t), 'smug',
                   prop_n=lambda L, h: J.jar(L, h[0] + 0.4, h[1] + 1.8, 4.2, 'jam'))
        valera(CH, v_, t, (420.0, 640.0, 13.5), 'shrug', 'shock')
    big, _ = landing(v, t, draw, pile=False, fall=min(1.0, u / 0.4) if loop else None)
    if loop: B.shake(big, t, 10, 40)
    return big


SHOT = dict(hook=r_hook, zina=r_zina, cat_top=r_cat_top, shop=r_shop, nina=r_nina, buried=r_buried, label=r_label,
            flashback=r_flashback, whisper=r_whisper, cat_log=r_cat_log, lyuba=r_lyuba, loop=lambda t, u: r_lyuba(t, u, True))


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


_ST = {}


def stack(*rows):
    w = max(r.shape[1] for r in rows)
    out = np.zeros((sum(r.shape[0] for r in rows) + 8 * (len(rows) - 1), w, 4), np.uint8)
    y = 0
    for r in rows:
        out[y:y + r.shape[0], (w - r.shape[1]) // 2:(w - r.shape[1]) // 2 + r.shape[1]] = r
        y += r.shape[0] + 8
    return out


def question():
    if 'q' not in _ST:
        _ST['q'] = stack(O.sticker('БАНКИ:', fg=(255, 236, 120), size=58), O.sticker('ВЕРНУТЬ / ОСТАВИТЬ', fg=(255, 255, 255), size=52))
    return _ST['q']


F0 = TL.T0
SHOW = K.Show(EPI, 3, ['40 БАНОК?!'], hook_t=(0.06, 2.5), hook_y=150,
              stickers=[(O.sticker('ОПЕРАЦИЯ «РАЗДАЧА»', fg=(255, 236, 120), size=56), F0['shop'] + 0.05, F0['shop'] + 1.6, 540, 330),
                        (O.sticker('ЭТО МОИ?!', fg=(255, 120, 110), size=84), TL.TWIST + 0.5, F0['flashback'], 540, 1250),
                        (O.sticker('ГОД НАЗАД', fg=(236, 220, 190), size=64), F0['flashback'] + 0.05, F0['whisper'], 540, 330),
                        (O.sticker('+40', fg=(255, 150, 80), size=80), F0['lyuba'] + 0.4, TL.DUR, 820, 520)],
              flashes=[TL.TWIST + 0.35, F0['flashback'], F0['whisper']], mosaics=[F0['shop'], F0['nina']],
              cap_y={'hook': 1500, 'cat_top': 1540, 'buried': 1500, 'label': 1560, 'cat_log': 1240, 'lyuba': 1500}, cap_default=1460)
SHOW.badge = O.make_badge('СЕЗОН 2 • СЕРИЯ 3/6')


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    q0 = F0['cat_log'] + 1.6
    if q0 <= t < F0['lyuba'] + 0.2:
        O.draw_sticker(big, question(), t, q0, F0['lyuba'] + 0.2, 540, 1600)
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
