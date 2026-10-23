"""S02E02 «Восемь утра» — Saturday 08:00, the upstairs neighbour Гена drills. Valera answers with a mop in «morse», the drill answers back;
«Операция «Тишина»» upstairs… Гена (deaf: «Чего?!») — then TWIST: «Николаич! Подержите полку! Вы же армия — ровно держите!»
Valera drills himself in Гена's hard hat, beaming; баба Зина knocks from below; Valera: «Чего?!» — deaf too. Cat in earplugs: «Записал.»
  python3 s2e02.py test 1 5 20 | frames t… | all [4] | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from props import folkgena as G
from props import bytfx as B
from props import panelka as PK
from props import vikit as K
from props import decals as D
from props import rusigns as R
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG,
              endcard=dict(style='winter', lang='ru', promise='ЗАВТРА: 40 БАНОК'))
talk = EPI.talk
CUTS, NAMES = TL.CUTS + [TL.DUR], TL.NAMES                  # per-shot render: python3 s2e02.py shots <i|name>
INK, RED, BLUE, PAPER = (34, 30, 30), (176, 30, 34), (40, 60, 150), (240, 234, 214)


def world(name):
    return PK.q(Image.open(PK.BG / f'{name}.png').convert('RGB'))


BED = world('bedroom')
GFL = world('gena_flat')
LAND = world('landing')
HALL = world('hallway')
NOTE = PK.bench_world([('УК «УЮТ»', 8, BLUE), ('РЕМОНТНЫЕ', 13, RED), ('РАБОТЫ', 13, RED), ('С 9:00 ДО 19:00', 9, INK)],
                      hand=[('ГЕНА — С 8:00', 10, (30, 60, 170), 398)])

# ---------------------------------------------------------------- local signs
D.attach(BED, [
    (R.plate(70, 26, ['НЕ БУДИТЬ!', 'ПРАПОРЩИК'], bg=PAPER, colors=[RED, INK], border=(120, 100, 70), pad=2, tilt=-3), 1010, 250),
    (R.plate(54, 40, ['ОКТЯБРЬ', '2026'], bg=(236, 236, 230), colors=[RED, INK], border=INK, pad=2), 1130, 130),
    (R.plate(60, 22, ['ПОДЪЁМ', 'В 6:00'], bg=(250, 230, 120), colors=[INK, INK], border=INK, pad=2, tilt=4), 300, 330),
])
D.attach(LAND, [
    (R.plate(44, 20, ['КВ. 47'], bg=(230, 220, 190), colors=[INK], border=INK, pad=2), 690, 180),
    (R.plate(88, 34, ['ЗВОНОК НЕ', 'РАБОТАЕТ.', 'СТУЧИТЕ ГРОМКО'], bg=PAPER, colors=[INK, INK, RED], border=(120, 100, 70), pad=2,
             tilt=3), 845, 300),
    (R.plate(70, 24, ['НЕ КУРИТЬ!'], bg=(236, 240, 246), colors=[RED], border=RED, pad=2), 520, 160),
    (R.plate(60, 22, ['КВ. 46', 'ВЕЖЛИВЫЕ'], bg=(230, 220, 190), colors=[INK, BLUE], border=INK, pad=2), 335, 180),
])
D.attach(GFL, [
    (R.plate(110, 40, ['РЕМОНТ', 'С 2019 г.'], bg=(250, 230, 120), colors=[INK, RED], border=INK, pad=3, tilt=-2), 1120, 120),
    (R.plate(70, 30, ['НЕ ВЛЕЗАЙ', '— УБЬЁТ'], bg=(236, 236, 230), colors=[RED, INK], border=RED, pad=2), 470, 270),
    (R.plate(64, 26, ['ГЕНА', 'МАСТЕР №1'], bg=(200, 220, 250), colors=[BLUE, INK], border=BLUE, pad=2, tilt=5), 1210, 300),
])
D.attach(HALL, [
    (R.plate(70, 26, ['ТИШИНА', 'С 23 ДО 7'], bg=PAPER, colors=[RED, INK], border=(120, 100, 70), pad=2, tilt=-4), 640, 260),
])
NOTEBOOK = R.plate(46, 20, ['ЖУРНАЛ', 'ЖАЛОБ'], bg=(70, 110, 170), colors=[(250, 240, 200), (250, 240, 200)], border=INK, pad=1.5)

# ---------------------------------------------------------------- positions (world px of each background)
V_BED = (655.0, 600.0, 12.0)            # Valera sitting up in bed (hips under the blanket), facing right
BLANKET_Y = 466.0                       # everything of Valera below this line is under the blanket
CAT_BED = (880.0, 452.0, 6.5)           # cat on the pillow
CAT_SILL = (150.0, 398.0, 6.5)          # cat on the bedroom window sill
V_MOP = (975.0, 690.0, 13.0)           # Valera on the floor with the mop, facing left
V_LAND = (505.0, 600.0, 13.5)           # Valera on the landing, facing right (to Гена's steel door)
G_DOOR = (690.0, 545.0, 13.0)           # Гена in his doorway, facing left
DOORWAY = (598, 122, 782, 508)
V_WALL = (905.0, 700.0, 15.0)           # Gena's flat: Valera drilling, facing right
G_WALL = (1135.0, 700.0, 15.0)          # Гена holding the shelf, facing left
Z_HALL = (640.0, 690.0, 15.0)           # баба Зина downstairs in her hallway


def mouth(who, t, k=1.6):
    return min(1.0, talk(who, t) * k)


def begin(Z):
    ST.set_px(ST.px_for_zoom(Z))
    return Chars(), Chars()


def light(v, lamp, col=(255, 210, 160), amb=(1.0, 0.98, 0.96), a=0.55, r=900):
    lx, ly = v.opt(*lamp)
    return Light(amb=amb, keys=[(lx, ly, r, col, a)], rim=(-1, -0.4, (200, 216, 255), 0.3), grad=(1.04, 0.92))


def plaster(FX, v, t, x0, x1, y0=0.0, y1=700.0, n=46, k=1.0):
    if k > 0: B.falling_snow(FX, v, t, x0, y0, x1, y1, n=int(n * k), col=(232, 228, 216), speed=380)


def doorway(big, v):
    """Гена's steel door is open: a dark renovation hall with a bare bulb behind him"""
    x0, y0, x1, y1 = DOORWAY
    a, b = v.opt(x0, y0); c, d = v.opt(x1, y1)
    a, b, c, d = int(max(0, a)), int(max(0, b)), int(min(big.shape[1], c)), int(min(big.shape[0], d))
    if c <= a or d <= b: return
    big[b:d, a:c] = (big[b:d, a:c] * 0.25 + np.array([52, 46, 40]) * 0.75).astype(np.uint8)
    fx.glow(big, (a + c) // 2, b + (d - b) // 5, max(40, (c - a) // 2), (255, 220, 150), 0.35)


def valera(CH, v, t, pos, pose='stand', expr='angry', flip=False, hat=None, hard=False, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un, flip=flip)
    r = F.valera(CH, cam, F.VPOSE[pose] if isinstance(pose, str) else pose, t, mouth('valera', t), expr, 'home', hat=hat, **kw)
    if hard:
        L = Layer(cam); G.hardhat(L, r['top']); F.outline(L); CH.add(L)
    return r


def gena(CH, v, t, pos, pose=None, expr='happy', flip=True, **kw):
    x, y, un = pos
    return G.gena(CH, v.cam(x, y, un, flip=flip), pose or G.GUITAR, t, mouth('gena', t), expr, **kw)


def mop(CH, v, hand_world, top_y, col=(150, 110, 70)):
    L = Layer(v.wcam())
    hx, hy = hand_world
    F.cap(L, (hx, hy + 30), (hx + 6, top_y + 10), 3.0, 3.0, col, (180, 140, 96), (110, 80, 50))
    F.ell(L, (hx + 6, top_y + 6), 22, 7, (200, 200, 190), 0, (230, 230, 220), (150, 150, 140))
    F.outline(L); CH.add(L)


def drill_in_hand(spin, k=1.0):
    return lambda L, h: G.perforator(L, h, -0.08, spin, k=k)


# ---------------------------------------------------------------- frames
def bedroom(v, t, draw=None, dust=1.0, cat_kw=None, cat_pos=CAT_BED, earplugs=False, pot=False):
    CH, FX = begin(v.Z)
    big = v.bg()
    if cat_kw is not None:
        x, y, un = cat_pos
        cam = v.cam(x, y, un)
        F.cat(CH, cam, t=t, pose='loaf', **cat_kw)
        if pot or earplugs:
            L = Layer(cam)
            if pot:                                                                  # a saucepan as a helmet
                F.ell(L, F.H(4.4, 10.2), 3.1, 1.6, (186, 190, 198), 0, (226, 230, 236), (130, 134, 144))
                F.cap(L, F.H(1.0, 9.4), F.H(7.8, 9.4), 0.45, 0.45, (130, 134, 144))
                F.cap(L, F.H(7.6, 10.0), F.H(9.6, 10.6), 0.35, 0.35, (60, 56, 56))
            if earplugs:
                for ex in (2.6, 6.2): F.dot(L, F.H(ex, 9.0), (255, 214, 60), 0.55)
            F.outline(L); CH.add(L)
    if draw: draw(CH, v)
    CH.comp(big, light(v, (560.0, 30.0), (226, 232, 255), amb=(0.96, 0.98, 1.06), a=0.35))
    plaster(FX, v, t, 380, 1000, 0, 700, k=dust)
    FX.comp(big)
    fx.vignette(big, 0.28)
    return big


def r_hook(t, u, loop=False):
    """«Восемь утра! Суббота!» — he jolts up in bed, plaster rains from the ceiling crack, the bed shakes"""
    x, y, un = V_BED
    hx, hy = x + 1.5 * un, y - 22.0 * un
    v = view_at(BED, hx, hy + 40, 1.5 + 0.06 * u, 180, 300)
    jump = 6 * abs(math.sin(min(u, 0.5) * 6.3)) if u < 0.5 else 0.0

    def draw(CH, v_):
        valera(CH, v_, t, (x, y - jump, un), 'shout', 'shout', stubble=1.0)
        PK.clip_below(CH, v_, BLANKET_Y)
    big = bedroom(v, t, draw, dust=1.4)
    B.shake(big, t, 9 if u < 1.2 or loop else 3, 33)
    return big


def r_cat_pot(t, u):
    x, y, un = CAT_BED
    hx, hy = x + 4.4 * un, y - 6.9 * un
    v = view_at(BED, hx - 10, hy, 2.6 + 0.06 * u, 180, 330)
    big = bedroom(v, t, cat_kw=dict(mouth=mouth('cat', t, 2.0), lid=0.7, tail=0.0), pot=True, dust=1.2)
    B.shake(big, t, 3, 33)
    return big


def r_morse(t, u):
    """mop knocks the ceiling three times — the drill answers three bursts from above (wide)"""
    x, y, un = V_MOP
    v = view_at(BED, 890, 360, 0.95, 180, 330)
    knock = (u < 0.9) and (u * 3.3) % 1 < 0.35
    hand = (x - 3.0 * un, y - (27.0 + (1.5 if knock else 0)) * un)

    def draw(CH, v_):
        valera(CH, v_, t, V_MOP, dict(F.VPOSE['overhead'], n=(3.0, 27.0 + (1.5 if knock else 0)), f=(1.6, 25.4)), 'angry', flip=True,
               stubble=1.0)
        mop(CH, v_, hand, 18.0)
    drilling = u > 0.95 and ((u - 0.95) * 3.0) % 1 < 0.55
    big = bedroom(v, t, draw, dust=1.6 if drilling else 0.3, cat_kw=dict(lid=0.9, tail=0.0), pot=True)
    if drilling: B.shake(big, t, 7, 40)
    return big


def r_notice(t, u):
    cx, cy = (PK.B_NOTICE[0] + PK.B_NOTICE[2]) / 2, (PK.B_NOTICE[1] + PK.B_NOTICE[3]) / 2
    v = view_at(NOTE, cx, cy, 1.75 + 0.1 * u, 180, 330)
    big = v.bg()
    fx.vignette(big, 0.3)
    return big


def landing(v, t, draw=None, door=True, dust=0.0):
    CH, FX = begin(v.Z)
    big = v.bg()
    if door: doorway(big, v)
    if draw: draw(CH, v)
    CH.comp(big, light(v, (552.0, 60.0), (255, 214, 150), amb=(0.98, 0.98, 0.96), a=0.6))
    if dust: plaster(FX, v, t, 560, 820, 100, 620, n=30, k=dust)
    FX.comp(big)
    fx.vignette(big, 0.3)
    return big


def r_march(t, u):
    """«Операция «Тишина». Двадцать лет в армии!» — he marches up onto the landing, whistle in his fist"""
    x, y, un = V_LAND
    k = sm(u / 1.2)
    xx = lerp(900, x, k)
    yy = lerp(700, y, k)
    v = view_at(LAND, lerp(760, 590, k), 360, 1.0, 180, 330)

    def draw(CH, v_):
        pose = F.vwalk(t) if u < 1.2 else 'salute'
        valera(CH, v_, t, (xx, yy, un), pose, 'proud' if u > 1.2 else 'angry', stubble=1.0)
    return landing(v, t, draw, door=False)


def r_door(t, u, again=False):
    """«Чего?!» — the steel door swings open: Гена in the hard hat, bare belly, perforator like a guitar"""
    x, y, un = G_DOOR
    fx_, fy_ = x - 2.4 * un, y - 23.5 * un
    v = view_at(LAND, fx_ - (70 if again else 0), fy_ + 60, (1.55 if not again else 1.25) + 0.05 * u, 180, 300)

    def draw(CH, v_):
        gena(CH, v_, t, G_DOOR, G.GUITAR, 'shout' if talk('gena', t) > 0.05 else 'happy',
             prop_n=drill_in_hand(t if not again or u < 0.3 else 0))
        if again: valera(CH, v_, t, V_LAND, 'hips', 'angry', stubble=1.0)
    big = landing(v, t, draw, dust=0.6)
    if u < 0.25: B.shake(big, t, 6, 40)
    return big


def r_v_shout(t, u):
    x, y, un = V_LAND
    hx, hy = x + 1.6 * un, y - 22.0 * un
    v = view_at(LAND, hx + 20, hy + 40, 1.5 + 0.05 * u, 180, 300)

    def draw(CH, v_):
        valera(CH, v_, t, V_LAND, 'point', 'shout', stubble=1.0)
    return landing(v, t, draw)


def r_shelf(t, u):
    """TWIST: «Николаич! Подержите полку!» — Гена beams and hands him a plank; a two-shot, flash, sticker"""
    v = view_at(LAND, 590, 380, 1.15 + 0.04 * u, 180, 330)

    def draw(CH, v_):
        x, y, un = G_DOOR
        k = sm((u - 0.6) / 0.6)
        a = (lerp(-1.0, -4.6, k), 18.0); b = (lerp(4.6, 1.2, k), 18.4)
        gena(CH, v_, t, G_DOOR, dict(G.GUITAR, n=(lerp(4.6, 6.4, k), lerp(12.6, 11.0, k)), f=(lerp(3.2, 7.4, k), lerp(15.2, 11.4, k))),
             'happy', prop_n=lambda L, h: G.shelf(L, (h[0] - 2.0, h[1] + 0.3), (h[0] + 2.6, h[1] + 0.3)))
        valera(CH, v_, t, V_LAND, 'hips' if u < 1.6 else 'proud', 'shock' if u < 1.6 else 'proud', stubble=1.0)
    return landing(v, t, draw)


def gena_flat(v, t, draw=None, dust=1.0):
    CH, FX = begin(v.Z)
    big = v.bg()
    if draw: draw(CH, v)
    CH.comp(big, light(v, (980.0, 130.0), (255, 214, 140), amb=(1.0, 0.97, 0.92), a=0.65))
    plaster(FX, v, t, 900, 1280, 120, 700, n=40, k=dust)
    fx.motes(FX, v, t, 700, 100, 1280, 600, n=50, col=(240, 230, 200))
    FX.comp(big)
    fx.vignette(big, 0.28)
    return big


def r_drill(t, u, deaf=False):
    """«По уровню! Как на плацу!» — Valera in Гена's hard hat drills the wall, Гена holds the shelf, dust everywhere"""
    v = view_at(GFL, 1015, 380, (0.98 if deaf else 1.08) + 0.04 * u, 180, 330)
    drilling = not deaf or u > 0.7

    def draw(CH, v_):
        gena(CH, v_, t, G_WALL, dict(G.GUITAR, n=(4.6, 20.6), f=(6.6, 20.8), bn=1, bf=1), 'shout' if deaf else 'happy', hat=False,
             prop_n=lambda L, h: G.shelf(L, (h[0] + 3.4, h[1] + 0.1), (h[0] - 0.6, h[1])))
        valera(CH, v_, t, V_WALL, dict(F.VPOSE['hold'], n=(6.0, 19.6), f=(7.6, 20.6)), 'shout' if deaf else 'proud', hard=True,
               hand_n=None, prop_n=drill_in_hand(t if drilling else 0, 0.62), stubble=1.0)
    big = gena_flat(v, t, draw, dust=1.4 if drilling else 0.5)
    if drilling: B.shake(big, t, 5, 44)
    return big


def r_zina(t, u):
    """«Валера! Восемь утра!» — downstairs, баба Зина in her hallway knocks the ceiling with a mop"""
    x, y, un = Z_HALL
    knock = (u * 3.0) % 1 < 0.3
    v = view_at(HALL, x + 2.0 * un, y - 20 * un, 1.2, 180, 300)
    CH, FX = begin(v.Z)
    big = v.bg()
    hand = (x + 6.0 * un, y - (25.0 + (1.2 if knock else 0)) * un)
    r = F.babushka(CH, v.cam(x, y, un), t, 'zina', 'stand', mouth('zina', t), 'angry', hand_n=F.H(6.0, 25.0 + (1.2 if knock else 0)))
    hand = (x + (r['hand_n'][0] - 1000) * un, y + (r['hand_n'][1] - 1000) * un)
    mop(CH, v, (hand[0] - 6, hand[1] - 30), 8.0)
    CH.comp(big, light(v, (640.0, 40.0), (255, 214, 150), a=0.5))
    plaster(FX, v, t, 500, 800, 0, 700, n=30, k=1.0 if knock else 0.4)
    FX.comp(big)
    fx.vignette(big, 0.3)
    if knock: B.shake(big, t, 4, 40)
    return big


def r_cat_sill(t, u):
    """«Записал.» — the cat on the bedroom sill in yellow earplugs, the complaint log; the two-choice question"""
    x, y, un = CAT_SILL
    hx, hy = x + 4.4 * un, y - 6.9 * un
    v = view_at(BED, hx + 10, hy + 10, 2.4 + 0.05 * u, 180, 320)
    big = bedroom(v, t, cat_kw=dict(mouth=mouth('cat', t, 2.0), lid=0.7, tail=0.3, expr='deadpan'), cat_pos=CAT_SILL, earplugs=True,
                  dust=0.0)
    D.blit(big, v, NOTEBOOK, 214, 386, ws=4)
    return big


SHOT = dict(hook=r_hook, cat_pot=r_cat_pot, morse=r_morse, notice=r_notice, march=r_march, door=r_door, v_shout=r_v_shout,
            door2=lambda t, u: r_door(t, u, True), shelf=r_shelf, drill=r_drill, zina=r_zina, deaf=lambda t, u: r_drill(t, u, True),
            cat_sill=r_cat_sill, loop=lambda t, u: r_hook(t, u, True))


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
        _ST['q'] = stack(O.sticker('РЕМОНТ У СОСЕДА:', fg=(255, 236, 120), size=54), O.sticker('ГОД / ВЕЧНО', fg=(255, 255, 255), size=58))
    return _ST['q']


F0 = TL.T0
SHOW = K.Show(EPI, 2, ['ПЕРФОРАТОР', 'В 8:00?!'], hook_t=(0.06, 2.5), hook_y=150,
              stickers=[(K.lcd_sticker('СБ 08:00', size=64), 0.15, F0['cat_pot'], 790, 1180),
                        (O.sticker('ТУК-ТУК…', fg=(236, 220, 190), size=60), F0['morse'] + 0.1, F0['morse'] + 0.95, 330, 700),
                        (O.sticker('ДРРР-ДРРР!', fg=(255, 150, 80), size=64), F0['morse'] + 1.0, F0['notice'], 700, 520),
                        (O.sticker('ПОДЕРЖИ ПОЛКУ', fg=(255, 236, 120), size=68), TL.TWIST + 1.0, F0['drill'], 540, 1160),
                        (O.sticker('ЧЕГО?!', fg=(255, 120, 110), size=80), F0['deaf'] + 0.1, F0['cat_sill'], 540, 560)],
              flashes=[TL.TWIST + 0.9, F0['drill']], mosaics=[F0['notice'], F0['zina']],
              cap_y={'hook': 1500, 'loop': 1500, 'notice': 1500, 'shelf': 1520, 'drill': 1520, 'deaf': 1520, 'cat_sill': 1240},
              cap_default=1420)
SHOW.badge = O.make_badge('СЕЗОН 2 • СЕРИЯ 2/6')


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    q0 = F0['cat_sill'] + 1.2
    if q0 <= t < TL.DUR:
        O.draw_sticker(big, question(), t, q0, TL.DUR + 0.5, 540, 1600)
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
