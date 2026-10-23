"""S02E04 «Поверка» — through the peephole: two «поверщики» in orange vests (Семёныч and Колян) demand a meter check «иначе штраф».
Valera the sentry: «Пароль!» — «Ну.» — «Неправильно!» — they flee, a scanword and a «компот 70°» receipt fly out of their folder.
TWIST: the real УК «Уют» arrives — Нина: «Плановая поверка. Пять тысяч.» — «А те… сколько брали?» — cat: «Две.» Valera shouts down the
stairwell: «Мужики! Вернитесь! У вас дешевле!» — «Ну!». Cat: «Записал.»
  python3 s2e04.py test 1 5 20 | frames t… | all [4] | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import stage as ST
from stage import view_at, Chars, Light
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import folkmates as FM
from props import bytfx as B
from props import panelka as PK
from props import vikit as K
from props import decals as D
from props import rusigns as R
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG,
              endcard=dict(style='winter', lang='ru', promise='ЗАВТРА: ГОЛОЛЁД ВО ДВОРЕ'))
talk = EPI.talk
CUTS, NAMES = TL.CUTS + [TL.DUR], TL.NAMES                  # per-shot render: python3 s2e04.py shots <i|name>
INK, RED, BLUE, PAPER, ORANGE = (34, 30, 30), (176, 30, 34), (40, 60, 150), (240, 234, 214), (250, 122, 30)


def world(name):
    return PK.q(Image.open(PK.BG / f'{name}.png').convert('RGB'))


LAND = world('landing')
HALL = world('hallway')
STAIR = world('stairwell')

D.attach(LAND, [
    (R.plate(44, 20, ['КВ. 43'], bg=(230, 220, 190), colors=[INK], border=INK, pad=2), 313, 170),
    (R.plate(44, 20, ['КВ. 44'], bg=(230, 220, 190), colors=[INK], border=INK, pad=2), 668, 170),
    (R.plate(84, 40, ['ПОВЕРКА', 'СЧЁТЧИКОВ', 'ОБЯЗАТЕЛЬНА!'], bg=(250, 230, 120), colors=[RED, INK, INK], border=INK, pad=2, tilt=-3),
     492, 250),
    (R.plate(90, 26, ['НЕ ОТКРЫВАЙТЕ', 'НЕЗНАКОМЦАМ'], bg=PAPER, colors=[RED, INK], border=(120, 100, 70), pad=2, tilt=3), 900, 300),
])
D.attach(HALL, [
    (R.plate(70, 26, ['ГЛАЗОК', 'НЕ ЗАКЛЕИВАТЬ'], bg=PAPER, colors=[INK, RED], border=(120, 100, 70), pad=2, tilt=-3), 640, 200),
    (R.plate(54, 22, ['ПОСТ №1'], bg=(250, 230, 120), colors=[RED], border=INK, pad=2, tilt=4), 560, 460),
])
D.attach(STAIR, [
    (R.plate(80, 30, ['УК «УЮТ»:', 'ПОВЕРКА 5 000'], bg=(236, 240, 246), colors=[BLUE, RED], border=(60, 70, 120), pad=2), 970, 250),
])
NOTEBOOK = R.plate(46, 20, ['ЖУРНАЛ', 'ЖАЛОБ'], bg=(70, 110, 170), colors=[(250, 240, 200), (250, 240, 200)], border=INK, pad=1.5)
SCAN = R.plate(40, 30, ['СКАНВОРД', '№ 47'], bg=(244, 244, 236), colors=[INK, RED], border=INK, pad=2)
RECEIPT = R.plate(34, 34, ['ЧЕК', 'КОМПОТ 70°', '— 2 шт.'], bg=(250, 250, 244), colors=[INK, RED, INK], border=(150, 150, 150), pad=2)
BADGE = R.plate(28, 12, ['УК «УЮТ»'], bg=(236, 240, 246), colors=[BLUE], border=BLUE, pad=1)
PRICE = R.plate(70, 34, ['ПОВЕРКА', '5 000 ₽'], bg=(250, 230, 120), colors=[INK, RED], border=INK, pad=2)
VEST_TAG = R.plate(22, 9, ['ПОВЕРКА'], bg=(250, 122, 30), colors=[(255, 255, 255)], border=None, pad=0.8)

# ---------------------------------------------------------------- positions
S_PEEP = (600.0, 610.0, 15.0)            # Семёныч outside, facing left (toward Valera's door = camera)
K_PEEP = (780.0, 615.0, 15.5)            # Колян behind him
V_HALL = (470.0, 700.0, 15.0)            # Valera inside at his front door, facing right (eye to the peephole)
PEEPHOLE = (512.0, 382.0)
CAT_BENCH = (300.0, 520.0, 7.0)          # cat on the shoe bench in the hallway
V_DOOR = (440.0, 640.0, 13.5)            # Valera in his doorway on the landing, facing right
N_DOOR = (700.0, 600.0, 16.0)            # Нина Петровна at his door (upper body), facing left
V_RAIL = (860.0, 655.0, 13.5)            # Valera at the top of the stairs, facing right
S_BACK = (640.0, 600.0, 10.0)            # ground floor: the two coming back up (facing right)
K_BACK = (740.0, 604.0, 10.5)


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


def duo(CH, v, t, spos, kpos, flip=True, sexpr='smug', kexpr='normal', walk=0.0, folder=True):
    b = 3 * abs(math.sin(t * 9)) * walk
    x, y, un = kpos
    FM.kolyan(CH, v.cam(x, y - b, un, flip=flip), FM.STAND, t, mouth('kolyan', t), kexpr, vest=True,
              prop_n=(lambda L, h: F.poly(L, [(h[0] - 1.2, h[1] - 3.0), (h[0] + 1.8, h[1] - 3.0), (h[0] + 1.8, h[1] + 0.6),
                                              (h[0] - 1.2, h[1] + 0.6)], (60, 70, 120))) if folder else None)
    x, y, un = spos
    FM.semenych(CH, v.cam(x, y - b, un, flip=flip), FM.STAND, t, mouth('semenych', t), sexpr, vest=True)


def doorway(big, v, box=(222, 112, 448, 508)):
    x0, y0, x1, y1 = box
    a, b = v.opt(x0, y0); c, d = v.opt(x1, y1)
    a, b, c, d = int(max(0, a)), int(max(0, b)), int(min(big.shape[1], c)), int(min(big.shape[0], d))
    if c <= a or d <= b: return
    big[b:d, a:c] = (big[b:d, a:c] * 0.3 + np.array([96, 76, 52]) * 0.7).astype(np.uint8)


def fisheye(big, k=0.55):
    """door peephole: barrel lens in a brass ring, black outside"""
    h, w = big.shape[:2]
    cy, cx, R = h * 0.47, w / 2, w * 0.47
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx, dy = (xx - cx) / R, (yy - cy) / R
    r = np.sqrt(dx * dx + dy * dy)
    s = (1 - k) + k * r                                           # magnify the centre
    sx = np.clip(cx + dx * s * R, 0, w - 1).astype(np.int32)
    sy = np.clip(cy + dy * s * R, 0, h - 1).astype(np.int32)
    out = big[sy, sx]
    out[r > 1.0] = (12, 10, 8)
    ring = (r > 0.97) & (r <= 1.05)
    out[ring] = (150, 120, 60)
    out[(r > 0.8) & (r <= 0.97)] = (out[(r > 0.8) & (r <= 0.97)] * 0.75).astype(np.uint8)
    big[:] = out


# ---------------------------------------------------------------- landing
def landing(v, t, draw=None, door=False):
    CH, FX = begin(v.Z)
    big = v.bg()
    if door: doorway(big, v)
    if draw: draw(CH, v)
    CH.comp(big, light(v, (552.0, 60.0), a=0.6))
    fx.vignette(big, 0.3)
    return big


def r_peep(t, u, loop=False):
    """«Поверка счётчиков! Иначе штраф, сударь!» — fisheye through the peephole: two in orange vests with a huge folder"""
    v = view_at(LAND, 690, 290, 1.05, 180, 300)

    def draw(CH, v_):
        duo(CH, v_, t, S_PEEP, K_PEEP, sexpr='smug', kexpr='normal')
    big = landing(v, t, draw)
    for (x, y) in ((S_PEEP[0] - 1.0 * S_PEEP[2], S_PEEP[1] - 13.4 * S_PEEP[2]), (K_PEEP[0] - 1.0 * K_PEEP[2], K_PEEP[1] - 16.0 * K_PEEP[2])):
        D.blit(big, v, VEST_TAG, x - 11, y, ws=4)
    fisheye(big)
    return big


def hall(v, t, draw=None, cat_kw=None):
    CH, FX = begin(v.Z)
    big = v.bg()
    if cat_kw is not None:
        x, y, un = CAT_BENCH
        F.cat(CH, v.cam(x, y, un), t=t, pose='loaf', **cat_kw)
    if draw: draw(CH, v)
    CH.comp(big, light(v, (640.0, 60.0), (255, 210, 150), amb=(1.0, 0.96, 0.9), a=0.6))
    fx.vignette(big, 0.3)
    return big


def r_v_door(t, u):
    """«Поверка?! Без приказа?!» — Valera's eye pressed to the peephole, a tense whisper"""
    x, y, un = V_HALL
    fx_, fy_ = K.face_w(x, y, un, h=21.0)
    v = view_at(HALL, fx_ + 20, fy_ + 50, 1.9 + 0.05 * u, 180, 300)

    def draw(CH, v_):
        valera(CH, v_, t, (x + 4 * sm(u / 0.4), y, un), dict(F.VPOSE['stand'], n=(4.6, 21.0)), 'normal', look=0.6)
    big = hall(v, t, draw)
    return big


def r_cat_stool(t, u, two=False):
    x, y, un = CAT_BENCH
    hx, hy = x + 4.4 * un, y - 6.9 * un
    v = view_at(HALL, hx, hy, 2.6 + 0.06 * u, 180, 330)
    return hall(v, t, cat_kw=dict(mouth=mouth('cat', t, 2.0), lid=0.6 if not two else 0.85, tail=0.2, expr='deadpan'))


def r_sentry(t, u):
    """«Стой! Кто идёт?! Пароль!» — at attention by the door like a sentry, ПОСТ №1"""
    v = view_at(HALL, 520, 420, 1.1 + 0.04 * u, 180, 330)

    def draw(CH, v_):
        valera(CH, v_, t, V_HALL, 'salute', 'shout')
    big = hall(v, t, draw, cat_kw=dict(lid=0.8, tail=0.1))
    return big


def falling_paper(big, v, t, t0, items):
    for i, (img, x0, y0) in enumerate(items):
        k = max(0.0, t - t0)
        x = x0 + 40 * math.sin(k * 3 + i) + 60 * k
        y = min(y0 + 160 * k, 640)
        D.blit(big, v, img, x, y, ws=4)


def r_burst(t, u):
    """«Неправильно! Двадцать лет в армии!» — he flings the door open with a whistle; the two flee down the stairs, papers fly"""
    v = view_at(LAND, 600, 380, 1.0, 180, 330)
    run = sm((u - 0.9) / 1.6)

    def draw(CH, v_):
        valera(CH, v_, t, V_DOOR, 'salute' if u < 1.0 else 'fist', 'shout')
        sx = lerp(S_PEEP[0], 1060, run); kx = lerp(K_PEEP[0], 1150, run)
        duo(CH, v_, t, (sx, S_PEEP[1] + 40 * run, 13.5), (kx, K_PEEP[1] + 50 * run, 14.0), flip=False, sexpr='shock', kexpr='shock',
            walk=1.0 if run > 0 else 0.0, folder=run < 0.3)
    big = landing(v, t, draw, door=True)
    if u > 1.0: falling_paper(big, v, t, TL.T0['burst'] + 1.0, [(SCAN, 800, 300), (RECEIPT, 860, 260)])
    if u < 0.3: B.shake(big, t, 8, 36)
    return big


def r_victory(t, u):
    """«Мошенники! Разбиты по уставу!» — proud, the scanword and the «компот 70°» receipt on the floor"""
    x, y, un = V_DOOR
    v = view_at(LAND, 480, 430, 1.3 + 0.04 * u, 180, 330)

    def draw(CH, v_):
        valera(CH, v_, t, V_DOOR, 'fist', 'proud')
    big = landing(v, t, draw, door=True)
    D.blit(big, v, SCAN, 610, 610, ws=4)
    D.blit(big, v, RECEIPT, 680, 600, ws=4)
    return big


def r_nina(t, u, price=False):
    """«Плановая поверка. УК «Уют».» — the real УК at the door: Нина with a badge; TWIST: «Пять тысяч.» + the price plate"""
    x, y, un = N_DOOR
    v = view_at(LAND, 650 if not price else 670, 480 if not price else 470, (1.75 if not price else 2.1) + 0.05 * u, 180, 330)

    def draw(CH, v_):
        F.nina(CH, v_.cam(x, y, un, flip=True), t, mouth('nina', t), 'smug' if price else 'bored', False)
    big = landing(v, t, draw)
    D.blit(big, v, BADGE, x - 3.4 * un, y - 3.2 * un, ws=4)
    if price:
        k = sm(u / 0.25)
        D.blit(big, v, PRICE, x - 1.0 * un, y - 6.4 * un + 30 * (1 - k), ws=4)
    return big


def r_choke(t, u):
    """«А те… сколько брали?» — Valera in his doorway, choking"""
    x, y, un = V_DOOR
    fx_, fy_ = K.face_w(x, y, un, h=21.0)
    v = view_at(LAND, fx_ + 10, fy_ + 60, 1.8 + 0.05 * u, 180, 300)

    def draw(CH, v_):
        valera(CH, v_, t, V_DOOR, 'shiver', 'shock')
    return landing(v, t, draw, door=True)


def r_stairs(t, u):
    """«Мужики! Вернитесь! У вас дешевле!» — he hangs over the stair rail and shouts down"""
    v = view_at(LAND, 820, 400, 1.2 + 0.04 * u, 180, 330)

    def draw(CH, v_):
        valera(CH, v_, t, V_RAIL, dict(F.VPOSE['shout'], n=(6.2, 18.0), f=(4.0, 25.0)), 'shout', lean=0.8)
    big = landing(v, t, draw)
    return big


def r_back(t, u):
    """«Ну!» — ground floor: the two stop, turn round and trot back up, folder under the arm"""
    v = view_at(STAIR, 720, 380, 1.15, 180, 330)
    CH, FX = begin(v.Z)
    big = v.bg()
    turn = u > 0.35
    duo(CH, v, t, (S_BACK[0] + 40 * max(0, u - 0.4), S_BACK[1], S_BACK[2]), (K_BACK[0] + 40 * max(0, u - 0.4), K_BACK[1], K_BACK[2]),
        flip=not turn, sexpr='happy', kexpr='happy', walk=1.0 if turn else 0.0)
    CH.comp(big, light(v, (616.0, 92.0), a=0.55))
    fx.vignette(big, 0.3)
    return big


def r_cat_log(t, u):
    x, y, un = CAT_BENCH
    hx, hy = x + 4.4 * un, y - 6.9 * un
    v = view_at(HALL, hx + 10, hy + 10, 2.3 + 0.05 * u, 180, 320)
    big = hall(v, t, cat_kw=dict(mouth=mouth('cat', t, 2.0), lid=0.65, tail=0.3, expr='deadpan'))
    D.blit(big, v, NOTEBOOK, x + 58, y - 20, ws=4)
    return big


SHOT = dict(peep=r_peep, v_door=r_v_door, cat_stool=r_cat_stool, sentry=r_sentry, peep2=r_peep, burst=r_burst, victory=r_victory,
            nina=r_nina, price=lambda t, u: r_nina(t, u, True), choke=r_choke, cat_two=lambda t, u: r_cat_stool(t, u, True),
            stairs=r_stairs, back=r_back, cat_log=r_cat_log, loop=lambda t, u: r_peep(t, u, True))


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
        _ST['q'] = stack(O.sticker('КТО ЧЕСТНЕЕ:', fg=(255, 236, 120), size=58), O.sticker('МОШЕННИКИ / УК', fg=(255, 255, 255), size=56))
    return _ST['q']


F0 = TL.T0
SHOW = K.Show(EPI, 4, ['ШТРАФ ЗА', 'СЧЁТЧИК?!'], hook_t=(0.06, 2.5), hook_y=150,
              stickers=[(O.sticker('ПАРОЛЬ?', fg=(255, 236, 120), size=64), F0['sentry'] + 0.5, F0['peep2'] + 0.9, 540, 420),
                        (O.sticker('МОШЕННИКИ!', fg=(255, 120, 110), size=70), F0['victory'] + 0.1, F0['nina'], 540, 330),
                        (O.sticker('5 000?!', fg=(255, 120, 110), size=96), TL.TWIST + 0.4, F0['choke'] + 1.2, 540, 380),
                        (O.sticker('ДВЕ', fg=(255, 236, 120), size=80), F0['cat_two'] + 0.2, F0['stairs'], 820, 520)],
              flashes=[TL.TWIST + 0.3, F0['burst']], mosaics=[F0['nina'], F0['back']],
              cap_y={'peep': 1640, 'peep2': 1640, 'loop': 1640, 'nina': 1640, 'price': 1640, 'cat_log': 1240}, cap_default=1460)
SHOW.badge = O.make_badge('СЕЗОН 2 • СЕРИЯ 4/6')


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    q0 = F0['cat_log'] + 1.4
    if q0 <= t < TL.DUR:
        O.draw_sticker(big, question(), t, q0, TL.DUR + 0.5, 540, 1600)
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
