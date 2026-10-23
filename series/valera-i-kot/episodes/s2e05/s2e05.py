"""S02E05 «Посыпано» — the yard is a skating rink though the УК sign says «ПОСЫПАНО». Valera flies across it; Зина and Люба score him
like judges («Тройной тулуп.»). «Операция «Песок»»: he sands the whole yard in parade-ground stripes, the grannies follow — «Герой!»,
a medal from a jar lid. TWIST: Нина hangs «ПОСЫПАНО. УК «УЮТ»» and fines him for «самовольное посыпание» — the bucket goes to the УК.
He walks out of the door and slips on the only un-sanded spot: his own step. Cat: «Записал.»; loop — flying across the rink again.
  python3 s2e05.py test 1 5 20 | frames t… | all [4] | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import view_at, Chars, Light, OUT_W, OUT_H
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as B
from props import panelka as PK
from props import vikit as K
from props import decals as D
from props import rusigns as R
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG,
              endcard=dict(style='winter', lang='ru', promise='ЗАВТРА ФИНАЛ: ОТОПЛЕНИЕ ДАЛИ!'))
talk = EPI.talk
CUTS, NAMES = TL.CUTS + [TL.DUR], TL.NAMES                  # per-shot render: python3 s2e05.py shots <i|name>
INK, RED, BLUE, PAPER = (34, 30, 30), (176, 30, 34), (40, 60, 150), (240, 234, 214)
W = PK.build()
KIT = W['kitchen']


def world(name):
    return PK.q(Image.open(PK.BG / f'{name}.png').convert('RGB'))


def ice(a, polys):
    """glossy ice sheets baked into the snow: translucent blue with white streaks"""
    im = Image.fromarray(a).convert('RGBA')
    ov = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for p in polys:
        d.polygon(p, fill=(150, 196, 236, 150))
        x0 = min(q[0] for q in p); x1 = max(q[0] for q in p); y0 = min(q[1] for q in p); y1 = max(q[1] for q in p)
        for k in range(6):
            yy = y0 + (y1 - y0) * (0.2 + 0.12 * k); xx = x0 + (x1 - x0) * (0.1 + 0.13 * k)
            d.line([(xx, yy), (xx + (x1 - x0) * 0.18, yy - 6)], fill=(240, 250, 255, 200), width=3)
    return np.array(Image.alpha_composite(im, ov).convert('RGB'))


YARD = ice(world('yard'), [[(60, 600), (700, 570), (1240, 590), (1260, 700), (40, 712)]])
BENCH = ice(world('bench'), [[(760, 645), (930, 640), (960, 668), (740, 672)]])
SIGN = R.plate(78, 34, ['ПОСЫПАНО.', 'УК «УЮТ»'], bg=(236, 240, 246), colors=[BLUE, RED], border=(60, 70, 120), pad=2)
D.attach(YARD, [(SIGN, 640, 470),
                (R.plate(60, 22, ['КАТОК', '«ДВОР»'], bg=PAPER, colors=[BLUE, INK], border=(120, 100, 70), pad=2, tilt=-4), 160, 470),
                (R.plate(66, 22, ['ОСТОРОЖНО,', 'СОСУЛЬКИ!'], bg=(250, 230, 120), colors=[RED, INK], border=INK, pad=2), 330, 360)])
D.attach(BENCH, [(R.plate(80, 24, ['СКОЛЬЗКО?', 'ЗВОНИТЕ В УК'], bg=PAPER, colors=[RED, INK], border=(120, 100, 70), pad=2, tilt=3), 560, 300),
                 (R.plate(50, 20, ['ПЕСОК — УК'], bg=(236, 240, 246), colors=[BLUE], border=BLUE, pad=2), 1180, 390)])
SCORE = [R.plate(30, 22, [s], bg=(250, 250, 244), colors=[INK], border=INK, pad=2) for s in ('5,8', '5,9')]
FINE = R.plate(48, 30, ['КВИТАНЦИЯ', 'ШТРАФ', '+ ВЕДРО'], bg=(250, 250, 244), colors=[BLUE, RED, INK], border=(150, 150, 150), pad=2)
NOTEBOOK = R.plate(46, 20, ['ЖУРНАЛ', 'ЖАЛОБ'], bg=(70, 110, 170), colors=[(250, 240, 200), (250, 240, 200)], border=INK, pad=1.5)

# ---------------------------------------------------------------- positions
CAT_SILL = (600.0, 386.0, 6.5)           # kitchen sill, tea mug next to him
V_DOOR = (720.0, 668.0, 14.5)            # bench close-up: Valera at the entrance (facing left)
N_POS = (1040.0, 662.0, 14.5)            # Нина by the bench, waist hidden by the snowdrift (facing left)
STEP = (845.0, 652.0, 14.5)              # his own icy step


def mouth(who, t, k=1.6):
    return min(1.0, talk(who, t) * k)


def begin(Z):
    ST.set_px(ST.px_for_zoom(Z))
    return Chars(), Chars()


def light_night(v, lamp=(1160.0, 250.0)):
    lx, ly = v.opt(*lamp)
    return Light(amb=(0.86, 0.92, 1.1), keys=[(lx, ly, 1300, (255, 214, 150), 0.6)], rim=(-1, -0.4, (186, 212, 255), 0.4),
                 grad=(1.04, 0.9))


def light_door(v):
    lx, ly = v.opt(845.0, 160.0)
    return Light(amb=(0.88, 0.92, 1.08), keys=[(lx, ly, 1200, (255, 210, 140), 0.7)], rim=(-1, -0.4, (186, 212, 255), 0.4),
                 grad=(1.04, 0.9))


def valera(CH, v, t, pos, pose='stand', expr='angry', flip=False, outfit='street', **kw):
    x, y, un = pos
    return F.valera(CH, v.cam(x, y, un, flip=flip), F.VPOSE[pose] if isinstance(pose, str) else pose, t, mouth('valera', t), expr,
                    outfit, stubble=1.0, **kw)


def to_world(pos, pt, flip=False):
    x, y, un = pos
    return x + (pt[0] - 1000) * un * (-1 if flip else 1), y + (pt[1] - 1000) * un


def rotated(big, v, draw, lit, ang, pivot):
    """draw characters on a transparent canvas, rotate around the pivot (output px) and composite — for falls and slides"""
    CH = Chars(); draw(CH, v)
    a = np.zeros((OUT_H, OUT_W, 3), np.uint8)
    f = ST.UP * CH.k
    al = np.repeat(np.repeat(CH.m, f, 0), f, 1)[:OUT_H, :OUT_W].astype(np.uint8) * 255   # comp() clears the mask: grab it first
    CH.comp(a, lit)
    img = Image.fromarray(np.dstack([a, al])).rotate(ang, center=pivot, resample=Image.NEAREST)
    O.overlay(big, np.array(img), 0, 0, 1.0)


def bucket(L, h, s=1.0):
    x, y = h
    F.cap(L, (x - 0.2, y), (x - 0.2, y + 1.0), 0.15, 0.15, (90, 90, 96))
    F.poly(L, [(x - 1.5 * s, y + 1.0), (x + 1.3 * s, y + 1.0), (x + 1.0 * s, y + 3.6 * s), (x - 1.2 * s, y + 3.6 * s)], (130, 140, 150))
    F.ell(L, (x - 0.1, y + 1.1), 1.4 * s, 0.4 * s, (200, 160, 100))


def sand_spray(FX, v, t, x, y, n=26):
    L = Layer(v.wcam())
    for i in range(n):
        ph = (t * 2.2 + i / n) % 1.0
        dx = (i % 7 - 3) * 6 + 90 * ph
        F.dot(L, (x + dx, y + 160 * ph * ph - 40 * ph), (214, 176, 110), 1.6)
    FX.add(L)


# ---------------------------------------------------------------- yard
def r_hook(t, u, loop=False, cy=500.0, gy=650.0):
    """«Посыпано?! Где посыпано?!» — he flies across the icy yard on his back past the «ПОСЫПАНО» sign, string bag flying"""
    x = lerp(560, 860, u / 2.6)
    v = view_at(YARD, x - 70, cy, 1.3, 180, 330)                                # the camera tracks the slide
    CH, FX = begin(v.Z)
    big = v.bg()
    CH.comp(big, light_night(v))
    pos = (x, gy + 12 * 11.0, 11.0)                                           # hips on the ice once he lies flat

    def draw(CH_, v_):
        valera(CH_, v_, t, pos, 'shout', 'shout', hat='ushanka', prop_n=F.string_bag)
    px, py = v.opt(x, gy)
    rotated(big, v, draw, light_night(v), 78, (px, py))
    B.falling_snow(FX, v, t, 500, 200, 900, 700, n=50)
    FX.comp(big)
    fx.speed_lines(big, t, 0.55)
    fx.vignette(big, 0.3)
    return big


def bench(v, t, draw=None, drift=False):
    CH, FX = begin(v.Z)
    big = v.bg()
    if draw: draw(CH, v)
    if drift:
        L = Layer(v.wcam())
        F.ell(L, (N_POS[0] + 10, N_POS[1] + 22), 150, 46, (230, 238, 250), 0, (250, 252, 255), (180, 196, 220))
        F.outline(L); CH.add(L)
    CH.comp(big, light_door(v))
    B.falling_snow(FX, v, t, 500, 100, 1280, 720, n=60)
    FX.comp(big)
    fx.vignette(big, 0.3)
    return big


def r_judges(t, u):
    """«Тройной тулуп.» — Зина and Люба on the bench hold up score cards «5,8» and «5,9»"""
    v = view_at(BENCH, 800, 420, 1.35, 180, 330)
    out = []

    def draw(CH, v_):
        up = sm(u / 0.3)
        for who, (x, y, un) in (('zina', PK.B_ZINA), ('lyuba', PK.B_LYUBA)):
            r = F.babushka(CH, v_.cam(x, y, un), t, who, 'sit', mouth(who, t), 'smug', hand_n=F.H(4.0, lerp(8.0, 22.0, up)))
            out.append(to_world((x, y, un), r['hand_n']))
    big = bench(v, t, draw)
    for img, (hx, hy) in zip(SCORE, out):
        D.blit(big, v, img, hx - 15, hy - 26, ws=4)
    return big


def kitchen(v, t, cat_kw):
    CH, FX = begin(v.Z)
    big = v.bg()
    x, y, un = CAT_SILL
    F.cat(CH, v.cam(x, y, un), t=t, pose='loaf', **cat_kw)
    L = Layer(v.wcam())                                                              # tea glass in a metal holder
    F.cap(L, (x + 62, y - 26), (x + 62, y - 2), 7, 6, (190, 120, 60), (230, 170, 100), (140, 80, 40))
    F.cap(L, (x + 69, y - 20), (x + 74, y - 10), 2, 2, (170, 170, 176))
    F.outline(L); CH.add(L)
    lx, ly = v.opt(*PK.LAMP_K)
    CH.comp(big, Light(amb=(0.95, 0.97, 1.08), keys=[(lx, ly, 1100, (255, 196, 130), 0.75)], rim=(-1, -0.4, (186, 212, 255), 0.4),
                       grad=(1.04, 0.9)))
    B.steam(big, v, t, x + 62, y - 30, -99, n=6, rise=90, size=26, a=0.5)
    fx.vignette(big, 0.28)
    return big


def r_cat_tea(t, u):
    x, y, un = CAT_SILL
    v = view_at(KIT, x + 40, y - 40, 2.3 + 0.05 * u, 180, 330)
    return kitchen(v, t, dict(mouth=mouth('cat', t, 2.0), lid=0.7, tail=0.2, expr='deadpan'))


def r_sand(t, u):
    """«Двадцать лет в армии! Плац посыпать — святое!» — out of the door in his camo jacket, bucket of sand, salute"""
    x, y, un = V_DOOR
    v = view_at(BENCH, 760, 430, 1.3 + 0.04 * u, 180, 330)

    def draw(CH, v_):
        valera(CH, v_, t, V_DOOR, 'salute', 'proud', flip=True, hat='ushanka', prop_f=bucket)
    return bench(v, t, draw)


def r_sanding(t, u):
    """«Герой! Валера — герой!» — he sands the rink in parade-ground stripes, the grannies follow in single file"""
    v = view_at(YARD, 640, 470, 1.1, 180, 330)
    CH, FX = begin(v.Z)
    big = v.bg()
    k = u / 3.0
    x = lerp(300, 1000, k)
    L = Layer(v.wcam())
    for yy in (612, 640, 668, 696):
        if x > 260: F.cap(L, (240, yy), (x - 40, yy), 4, 4, (196, 160, 100))
    CH.add(L)
    for i, who in enumerate(('zina', 'lyuba')):
        F.babushka(CH, v.cam(x - 150 - 90 * i, 662 - 3 * abs(math.sin(t * 7 + i)), 8.0), t, who, 'stand', mouth(who, t), 'happy')
    valera(CH, v, t, (x, 668.0, 9.0), F.vwalk(t), 'proud', hat='ushanka', prop_f=bucket)
    CH.comp(big, light_night(v))
    sand_spray(FX, v, t, x + 30, 560)
    B.falling_snow(FX, v, t, 200, 200, 1100, 700, n=50)
    FX.comp(big)
    fx.vignette(big, 0.3)
    return big


def r_medal(t, u):
    """evening: a medal from a jar lid on his chest; the yard is clean"""
    x, y, un = V_DOOR
    fx_, fy_ = K.face_w(x, y, un, flip=True, h=21.0)
    v = view_at(BENCH, fx_ - 10, fy_ + 40, 1.6, 180, 330)
    out = {}

    def draw(CH, v_):
        valera(CH, v_, t, V_DOOR, 'proud', 'proud', flip=True, hat='ushanka')
        L = Layer(v_.cam(x, y, un, flip=True))
        F.cap(L, F.H(1.4, 18.0), F.H(1.6, 16.4), 0.5, 0.5, (200, 40, 40))
        F.ell(L, F.H(1.6, 15.4), 1.2, 1.2, (200, 204, 212), 0, (240, 242, 246), (140, 144, 154))
        F.outline(L); CH.add(L)
    return bench(v, t, draw)


def nina(CH, v, t, expr='bored', pos=N_POS, **kw):
    x, y, un = pos
    return F.nina(CH, v.cam(x, y, un, flip=True), t, mouth('nina', t), expr, False, outfit='coat', **kw)


def r_sign(t, u):
    """«Это я посыпал!» — Нина hangs a new «ПОСЫПАНО. УК «УЮТ»» on the wall; Valera points at himself"""
    v = view_at(BENCH, 850, 400, 0.9, 180, 330)

    def draw(CH, v_):
        valera(CH, v_, t, (740.0, 690.0, 14.5), 'proud', 'shout', hat='ushanka')
        nina(CH, v_, t, 'bored', pos=(990.0, 662.0, 14.5))
        L = Layer(v_.wcam())
        F.ell(L, (1000, 684), 150, 46, (230, 238, 250), 0, (250, 252, 255), (180, 196, 220))
        F.outline(L); CH.add(L)
    big = bench(v, t, draw)
    if u > 0.3: D.blit(big, v, SIGN, 950, 300 + 20 * (1 - sm((u - 0.3) / 0.2)), ws=4)
    return big


def r_fine(t, u):
    """TWIST: «Самовольное посыпание. Штраф. И ведро — УК.» — Нина tears off a receipt; flash, sticker «ШТРАФ ЗА ПЕСОК»"""
    x, y, un = N_POS
    v = view_at(BENCH, x - 60, y - 160, 1.9 + 0.05 * u, 180, 330)
    big = bench(v, t, lambda CH, v_: nina(CH, v_, t, 'smug'), drift=True)
    k = sm((u - 0.5) / 0.3)
    D.blit(big, v, FINE, x - 7.6 * un, y - 10.0 * un + 20 * k, ws=4)
    D.blit(big, v, SIGN, 950, 300, ws=4)
    return big


def r_protest(t, u):
    x, y, un = (660.0, 690.0, 14.5)
    fx_, fy_ = K.face_w(x, y, un, h=21.0)
    v = view_at(BENCH, fx_ + 10, fy_ + 60, 1.8 + 0.05 * u, 180, 300)
    return bench(v, t, lambda CH, v_: valera(CH, v_, t, (x, y, un), 'shrug', 'shout', hat='ushanka'))


def r_nina2(t, u):
    x, y, un = N_POS
    v = view_at(BENCH, x - 40, y - 170, 2.1 + 0.05 * u, 180, 330)
    big = bench(v, t, lambda CH, v_: nina(CH, v_, t, 'bored'), drift=True)
    return big


def r_slip(t, u):
    """he steps out of the door — onto the only un-sanded spot, his own step — and flies"""
    k = sm((u - 0.3) / 0.35)
    v = view_at(BENCH, 845 - 90 * k, 470 + 110 * k, 1.25, 180, 330)
    CH, FX = begin(v.Z)
    big = v.bg()
    CH.comp(big, light_door(v))
    pos = (STEP[0] + 40 * k, STEP[1] + 11 * STEP[2] * k, STEP[2])

    def draw(CH_, v_):
        valera(CH_, v_, t, pos, 'shout' if k > 0 else 'proud', 'shock' if k > 0 else 'proud', hat='ushanka')
    px, py = v.opt(pos[0], pos[1] - 11 * pos[2])
    rotated(big, v, draw, light_door(v), 82 * k, (px, py))
    if k > 0.9:
        for i in range(5):                                                        # cartoon stars
            a = t * 6 + i * 1.25
            sx, sy = v.opt(pos[0] - 40 + 50 * math.cos(a), pos[1] - 120 + 18 * math.sin(a))
            O.overlay(big, O.sticker('★', fg=(255, 230, 90), size=40), int(sx), int(sy), 1.0)
        B.shake(big, t, 4, 30)
    fx.vignette(big, 0.3)
    return big


def r_cat_log(t, u):
    x, y, un = CAT_SILL
    v = view_at(KIT, x + 50, y - 30, 2.2 + 0.05 * u, 180, 320)
    big = kitchen(v, t, dict(mouth=mouth('cat', t, 2.0), lid=0.65, tail=0.3, expr='deadpan'))
    D.blit(big, v, NOTEBOOK, x + 80, y - 22, ws=4)
    return big


SHOT = dict(hook=r_hook, judges=r_judges, cat_tea=r_cat_tea, sand=r_sand, sanding=r_sanding, medal=r_medal, sign=r_sign, fine=r_fine,
            protest=r_protest, nina2=r_nina2, slip=r_slip, cat_log=r_cat_log, loop=lambda t, u: r_hook(t, u, True))


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
        _ST['q'] = stack(O.sticker('КТО ПОСЫПАЕТ:', fg=(255, 236, 120), size=58), O.sticker('УК / САМ', fg=(255, 255, 255), size=60))
    return _ST['q']


F0 = TL.T0
SHOW = K.Show(EPI, 5, ['ПОСЫПАНО?!'], hook_t=(0.06, 2.5), hook_y=150,
              stickers=[(O.sticker('ОПЕРАЦИЯ «ПЕСОК»', fg=(255, 236, 120), size=58), F0['sand'] + 0.1, F0['sanding'] + 1.0, 540, 330),
                        (O.sticker('ГЕРОЙ ДВОРА', fg=(255, 236, 120), size=66), F0['medal'] + 0.1, F0['sign'], 540, 330),
                        (O.sticker('ШТРАФ ЗА ПЕСОК', fg=(255, 120, 110), size=72), TL.TWIST + 0.6, F0['protest'] + 0.6, 540, 380),
                        (O.sticker('БУМ!', fg=(255, 150, 80), size=90), F0['slip'] + 0.7, F0['cat_log'], 760, 520)],
              flashes=[TL.TWIST + 0.5, F0['medal']], mosaics=[F0['sand'], F0['slip']],
              cap_y={'hook': 1500, 'loop': 1500, 'fine': 1640, 'nina2': 1640, 'cat_log': 1240}, cap_default=1460)
SHOW.badge = O.make_badge('СЕЗОН 2 • СЕРИЯ 5/6')


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    q0 = F0['cat_log'] + 1.4
    if q0 <= t < F0['loop'] + 0.1:
        O.draw_sticker(big, question(), t, q0, F0['loop'] + 0.1, 540, 1600)
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
