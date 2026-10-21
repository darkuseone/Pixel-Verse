"""«Мазутыч: СЛЕДСТВИЕ ПО БЕНЗИНУ» — detective mini-movie, 16:9 1920x1080, rendered by shots (timeline.py).
  python3 movie.py prep                       flashback frames from the season finals -> build/mazutych-movie/fb/<ep>/
  python3 movie.py sheet <shot|index> ...     12-up mini sheet of shot middles (build/mazutych-movie/msheet.png)
  python3 movie.py test|frames t ...  |  all [N]      (engine/episode.py CLI)
  python3 mix.py                              -> final_h264.mp4"""
import os
os.environ['PV_WIDE'] = '1'
import sys, pathlib, math, subprocess
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine')); sys.path.insert(0, str(HERE))
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import stage as ST
from stage import view_at, Light, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
import paths as P
from episode import Episode
from props import mazcast as MC
from props import mazkit as K
from props import mazpix as MX
from props import mazshots as M
from props import bytfx as B
from props import decals as D
from props import rusigns as R
from props.mazshots import A, aout, wpt, SP, CAR, TRK, y_far, y_near, y_sh
import timeline as TL

assert (OUT_W, OUT_H) == (1920, 1080)
SX, SY = 320, 180
COL = dict(K.COL, vadik=(200, 160, 255), cop=(190, 240, 60), bossh=K.COL['boss'], zoyam=K.COL['zoya'])
EPI = Episode('movie', TL.VOICE, TL.DUR, TL.FPS, colors=COL, slug=TL.SLUG, endcard=dict(style='default', lang='ru', sec=3.0, cy=880))
BK = f'{TL.SLUG}-movie'
INK = MX.INK


def mouth(who, t, k=1.7):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return 1.0 if any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in TL.VOICE) else 0.0


def wheel_k(t):
    return max(mouth('wheel', t, 1.6), 0.5 * speaking('wheel', t))


# ======================================================================================= worlds + signs
HW = K.world('highway_azs')
GATE = K.world('refinery_gate')
WIN = K.world('azs_window')
GAR = K.world('garages')
GI = K.world('garage_inside')
TANK = K.world('tank_farm')
OFF = K.world('boss_office')

RED, BLUE, PAPER, YEL = (176, 30, 34), (40, 60, 150), (240, 234, 214), (250, 214, 60)
D.attach(TANK, [
    (R.plate(186, 140, ['РЕЗЕРВУАР №1', '«ПЛАН»', 'НЕ ВСКРЫВАТЬ!'], bg=(236, 232, 218), colors=[INK, RED, RED], border=(150, 40, 40),
             weights=[0.55, 1.0, 0.45], pad=4, wear=0.25), 740, 228),
    (R.plate(64, 44, ['ЗАДВИЖКА', 'ОТВЕТСТВЕННЫЙ:', 'МАЗУРОВ Г.П.'], bg=(250, 230, 120), colors=[INK, INK, RED], border=INK, pad=2,
             weights=[1, 0.55, 1]), 236, 596),
    (R.plate(84, 26, ['ПОСТОРОННИМ ВХОД ВОСПРЕЩЁН'], bg=PAPER, fg=RED, border=(120, 40, 40), pad=2), 1080, 470),
])
D.attach(OFF, [
    (R.plate(180, 50, ['БОРИС БОРИСЫЧ', 'НАЧАЛЬНИК ЦЕХА'], bg=(214, 176, 90), colors=[INK, INK], border=(90, 60, 20), weights=[1, 0.6], pad=3),
     548, 268),
    (R.plate(66, 20, ['ПЛАН — ЗАКОН!'], bg=(176, 30, 34), fg=(255, 236, 160), border=INK, pad=2), 920, 262),
])
D.attach(GI, [
    (R.plate(60, 30, ['НЕ КУРИТЬ!', 'БЕНЗИН'], bg=PAPER, colors=[RED, INK], border=(90, 70, 40), pad=2, tilt=-3), 1010, 210),
])
D.attach(GATE, [
    (R.plate(120, 22, ['БЕНЗИН — ДЛЯ ПЛАНА!'], bg=(176, 30, 34), fg=(255, 236, 160), border=INK, pad=2), 120, 300),
])


def light_gar(v):
    return Light(amb=(0.86, 0.84, 1.02), keys=K._keys(v, ((1120, 190, 700, (255, 200, 120), 0.55), (640, 520, 420, (255, 214, 140), 0.25))),
                 rim=(1, -0.4, (255, 190, 120), 0.45), grad=(1.02, 0.88))


def light_gi(v):
    return Light(amb=(0.92, 0.86, 0.80), keys=K._keys(v, ((420, 70, 900, (255, 200, 120), 0.6),)), rim=(1, -0.4, (255, 190, 110), 0.4),
                 grad=(1.04, 0.84))


def light_tank(v):
    return Light(amb=(0.72, 0.80, 1.05), keys=K._keys(v, ((330, 230, 700, (200, 230, 255), 0.45), (1010, 300, 600, (200, 230, 255), 0.4),
                                                         (1180, 130, 600, (255, 150, 60), 0.35))),
                 rim=(1, -0.4, (255, 170, 90), 0.5), grad=(1.04, 0.86))


def light_off(v):
    return Light(amb=(0.96, 0.86, 0.78), keys=K._keys(v, ((805, 470, 600, (255, 210, 130), 0.55), (300, 300, 600, (255, 150, 80), 0.3))),
                 rim=(-1, -0.4, (255, 170, 90), 0.4), grad=(1.04, 0.86))


def light_night(v):
    return Light(amb=(0.62, 0.70, 1.0), keys=K._keys(v, ((664, 205, 900, (255, 150, 70), 0.35), (1000, 380, 420, (255, 214, 140), 0.45))),
                 rim=(1, -0.45, (255, 168, 90), 0.5), grad=(1.04, 0.86))


def light_morning(v):
    return Light(amb=(1.04, 1.0, 0.96), keys=K._keys(v, ((1110, 60, 900, (255, 200, 120), 0.35),)), rim=(1, -0.4, (255, 220, 160), 0.35),
                 grad=(1.05, 0.92))


# ======================================================================================= camera helpers
def shot(world, light, cx, cy, Z, acts=(), fx_=None, pre=None, t=0.0, sx=SX, sy=SY, vig=0.28):
    return K.shot(world, light, cx, cy, Z, acts=list(acts), fx_=fx_, pre=pre, sx=sx, sy=sy, t=t, vig=vig)


def cu(world, light, fn, who, t, cx, cy, sz=14.0, head=(1100, 470), Zb=1.3, blur=3, flip=False, pre_fx=None, extra=None, back=(),
       front=(), mk=1.6, **kw):
    """close-up: background at zoom Zb (soft), the hero's head pinned at an output point"""
    v0 = view_at(world, cx, cy, Zb, SX, SY)
    hx, hy = wpt(v0, head[0], head[1])
    if mk is not None: kw.setdefault('mouth_', mouth(who, t, mk))
    if fn is MC.maz: kw.setdefault('wheel_talk', wheel_k(t))
    a = A(fn, hx, hy, sz, pin='head', t=t, flip=flip, **kw)

    def pre(big, v):
        if pre_fx: pre_fx(big, v)
        if blur: big[:] = M.dof(big, blur)

    def f(big, v):
        if extra: extra(big, v, a)
    return shot(world, light, cx, cy, Zb, acts=list(back) + [a] + list(front), pre=pre, fx_=f, t=t)


def maz(t, x, y, Z, **kw):
    kw.setdefault('t', t)
    kw.setdefault('mouth_', mouth('maz', t))
    kw.setdefault('wheel_talk', wheel_k(t))
    return A(MC.maz, x, y, SP * Z, **kw)


def night(big, k=1.0, moon=None):
    M.night(big, k, moon)
    return big


def noir_bars(big, t, k=1.0):
    """film-noir venetian-blind light stripes across the frame"""
    yy = (np.arange(OUT_H) + int(t * 20)) % 120
    m = yy < 44
    big[m] = np.clip(big[m] * (1 + 0.22 * k), 0, 255).astype(np.uint8)
    big[~m] = (big[~m] * (1 - 0.25 * k)).astype(np.uint8)


def grain(big, t, a=10):
    r = np.random.default_rng(int(t * 30))
    n = r.integers(-a, a + 1, (OUT_H // 6, OUT_W // 6, 1), dtype=np.int16).repeat(6, 0).repeat(6, 1)
    big[:] = np.clip(big.astype(np.int16) + n, 0, 255).astype(np.uint8)


def sepia(big, k=0.5):
    g = big.mean(axis=2, keepdims=True)
    sp = np.concatenate([g * 1.07, g * 0.92, g * 0.72], 2)
    big[:] = np.clip(big * (1 - k) + sp * k, 0, 255).astype(np.uint8)


def nozzle(big, hx, hy, s=1.0, hose_from=None, up=False):
    if hose_from is not None:
        M.rope(big, hose_from, (hx, hy), sag=60 * s, w=int(12 * s), col=(34, 34, 38))
    g = (60, 62, 70)
    x, y = int(hx), int(hy)
    q = int(10 * s)
    if up:
        big[y - 3 * q:y + q, x - q:x + q] = g
        big[y - 7 * q:y - 3 * q, x - q // 2:x + q // 2] = (150, 150, 156)
        return x, y - 7 * q
    big[y - q:y + q, x - 3 * q:x + q] = g
    big[y - q // 2:y + q // 2, x + q:x + 5 * q] = (150, 150, 156)
    big[y + q:y + 3 * q, x - 2 * q:x - q] = g
    return x + 5 * q, y


def drop(big, x, y, r=14, col=(255, 214, 90)):
    """a fat pixel drop of gasoline with an oil-slick glint"""
    x, y, r = int(x), int(y), int(r)
    yy, xx = np.ogrid[-2 * r:r + 1, -r:r + 1]
    m = (xx * xx + yy * yy <= r * r) | ((np.abs(xx) <= r * (yy + 2 * r) / (2 * r)) & (yy < 0) & (yy > -2 * r))
    reg = big[y - 2 * r:y + r + 1, x - r:x + r + 1]
    if reg.shape[:2] != m.shape: return
    e = m & ~np.roll(m, 3, 0) | m & ~np.roll(m, -3, 1)
    reg[m] = col; reg[e] = INK
    big[y - r // 2:y - r // 2 + r // 3 + 1, x - r // 2:x - r // 2 + r // 3 + 1] = (255, 255, 240)
    big[y + r // 3:y + r // 3 + 4, x - r // 2:x + r // 3] = (150, 80, 230)


def caption_box(big, lines, x, y, size=34, fg=(255, 236, 160), bg=(16, 12, 14)):
    f = O.pfont(size)
    w = max(f.getbbox(l)[2] for l in lines) + 40
    h = len(lines) * (size + 16) + 24
    im = Image.new('RGBA', (w, h), bg + (230,)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, h - 1], outline=fg + (255,), width=4)
    for i, l in enumerate(lines): d.text((20, 14 + i * (size + 16)), l, font=f, fill=fg)
    O.overlay(big, np.array(im), int(x), int(y), 1.0)


_IMG = {}


def img(key, fn):
    if key not in _IMG: _IMG[key] = fn()
    return _IMG[key]


def portrait(fn, s, size, at=None, bg=(60, 50, 70), flip=False, head=(0.5, 0.42), **kw):
    """sprite render with its 'head' anchor placed at the relative point `head` of the canvas"""
    sp = MX.draw(fn, s, flip=flip, **kw)
    hx, hy = sp.anchors['head']
    ox = size[0] * head[0] - (-hx if flip else hx) * s
    oy = size[1] * head[1] + hy * s
    return MX.render(fn, s=s, bg=bg, size=size, at=(int(ox), int(oy)), flip=flip, **kw)


# ======================================================================================= 1. АЗС ночью: последняя капля
MP = (842.0, 524.0)                                  # Мазутыч at the pump
HOSE = (935, 440)


def azs_night(big, k=0.85, moon=None):
    return night(big, k, moon=moon)


def r_hook(t, s, u):
    Z = 1.75 + 0.1 * u
    m = maz(t, MP[0], MP[1], Z, expr='shout', look=(0.6, -0.6), beacon=True)

    def f(big, v):
        hx, hy = aout(m, v, 'hand')
        tx, ty = nozzle(big, hx + 10, hy - 10, 2.0, hose_from=v.opt(*HOSE), up=True)
        if int(u * 12) % 2: B.shake(big, t, 4, 30)
    big = shot(HW, light_night, 900.0, 405.0, Z, acts=[m], fx_=f, t=t)
    return azs_night(big, 0.7)


def r_drop_cu(t, s, u):
    """insert: the nozzle tip against the night sky; ONE drop swells; the wheel speaks below (waves)"""
    Z = 2.4
    wh = A(MC.monowheel_solo, 800.0, 505.0, SP * Z * 1.15, t=t, talk=wheel_k(t))

    def pre(big, v): big[:] = M.dof(big, 6)

    def f(big, v):
        tx, ty = nozzle(big, 1340, 560, 4.0, hose_from=(1900, 1100), up=True)
        drop(big, tx, ty + 40 + 50 * sm(u / 1.5), 16 + 18 * sm(u / 1.5))
    big = shot(HW, light_night, 900.0, 470.0, Z, acts=[wh], pre=pre, fx_=f, t=t)
    return azs_night(big, 0.6)


def r_maz_pump(t, s, u):
    def pre(big, v): K.flare(big, v, t, 664, 205, 1.0, 0.6)
    big = cu(HW, light_night, MC.maz, 'maz', t, 900.0, 380.0, sz=13.0 + 0.6 * u, head=(1080, 430), expr='sad', look=(-0.6, -0.8),
             beacon=True, pre_fx=pre)
    return azs_night(big, 0.6)


def r_drop_fall(t, s, u):
    """slow motion: the drop falls... and lands on his boot. «КАП.»"""
    Z = 1.9
    m = maz(t, MP[0], MP[1], Z, expr='stunned', look=(0.6, 1.0), beacon=True, mouth_=0.0)

    def f(big, v):
        hx, hy = aout(m, v, 'hand')
        tx, ty = nozzle(big, hx + 10, hy - 10, 2.0, hose_from=v.opt(*HOSE), up=True)
        fx_, fy_ = v.opt(MP[0] + 6, MP[1] - 12)
        k = sm(u / 0.6)
        if u < 0.62: drop(big, tx, lerp(ty + 20, fy_, k), 18)
        else:
            for i in range(8):                                               # splash
                a = i * math.pi / 7
                d = 30 + 90 * sm((u - 0.6) / 0.3)
                px, py = int(fx_ + math.cos(a) * d), int(fy_ - math.sin(a) * d * 0.6)
                big[py:py + 12, px:px + 12] = (255, 214, 90)
    big = shot(HW, light_night, 880.0, 450.0, Z, acts=[m], fx_=f, t=t)
    return azs_night(big, 0.6)


def r_maz_noir(t, s, u):
    """noir close-up: lamp light through the blinds of the kiosk, the flare behind; «Двадцать пять лет делаю бензин...»"""
    def pre(big, v): K.flare(big, v, t, 664, 205, 1.2, 0.7)
    big = cu(HW, light_night, MC.maz, 'maz', t, 700.0, 330.0, sz=15.0 + 0.5 * u, head=(1180, 480), expr='squint', look=(-1.0, 0.0),
             beacon=False, pre_fx=pre, blur=4, flip=True)
    azs_night(big, 0.55)
    noir_bars(big, t, 0.8)
    return big


TITLE = None


def r_title(t, s, u):
    global TITLE
    big = shot(HW, light_night, 760.0, 330.0, 0.62, acts=[maz(t, MP[0], MP[1], 0.62, expr='deadpan', beacon=True, mouth_=0.0)],
               fx_=lambda b, v: K.flare(b, v, t, 664, 205, 1.3, 1.0), t=t)
    azs_night(big, 0.75, moon=(1640, 160))
    big[:] = (big * 0.55).astype(np.uint8)
    if TITLE is None:
        TITLE = (K.hook_title(['МАЗУТЫЧ'], 120), K.hook_title(['СЛЕДСТВИЕ ПО БЕНЗИНУ'], 56, drips=False))
    k = sm(u / 0.25)
    O.overlay(big, TITLE[0], 0, 300, k)
    O.overlay(big, TITLE[1], 0, 560, sm((u - 0.4) / 0.25))
    return big


# ======================================================================================= 2. завод: план 147 %
def gate_fx(t, pct=147, flip=None):
    def f(big, v):
        K.flare(big, v, t, 1180, 140, 1.2, 1.0)
        K.plan_banner(big, v, pct, flip)
    return f


def r_gate_wide(t, s, u):
    Z = 0.62 + 0.03 * u
    x = lerp(300.0, 560.0, sm(u / 2.0))
    m = maz(t, x, 650.0, Z, expr='deadpan', look=(0.8, -0.6), beacon=True, spin=t * 20, mouth_=0.0)
    return shot(GATE, K.light_gate, 640.0, 380.0, Z, acts=[m], fx_=gate_fx(t), t=t)


def r_banner_cu(t, s, u):
    return shot(GATE, K.light_gate, 650.0, 175.0, 1.8 + 0.06 * u, fx_=gate_fx(t), t=t)


def r_maz_gate(t, s, u):
    def pre(big, v):
        K.flare(big, v, t, 1180, 140, 1.0, 0.6); K.plan_banner(big, v, 147)
    return cu(GATE, K.light_gate, MC.maz, 'maz', t, 640.0, 300.0, sz=13.5, head=(1150, 470), expr='deadpan', look=(-0.4, -0.8),
              beacon=True, pre_fx=pre, flip=True)


def r_loudspeaker(t, s, u):
    """the horn on the banner frame shakes; sound rings; Борис Борисыч's voice"""
    Z = 2.4
    def f(big, v):
        K.plan_banner(big, v, 147)
        ox, oy = v.opt(880, 95)
        for i in range(3):
            ph = (t * 2.2 + i / 3) % 1.0
            r = 60 + 260 * ph
            for a in np.linspace(-0.6, 0.6, 14):
                px, py = int(ox + 40 + math.cos(a) * r), int(oy + math.sin(a) * r)
                if 0 <= px < OUT_W - 14 and 0 <= py < OUT_H - 14: big[py:py + 14, px:px + 14] = (255, 230, 80)
        if speaking('boss', t): B.shake(big, t, 3, 40)
    big = shot(GATE, K.light_gate, 800.0, 140.0, Z, fx_=f, t=t)
    caption_box(big, ['ГРОМКОГОВОРИТЕЛЬ', 'ЗАВОДА «ФАКЕЛ ТРУДА»'], 80, 80, 26)
    return big


# ======================================================================================= 3. гараж: доска улик
BOARD = (512, 128, 868, 420)                       # corkboard on the garage doors (world)
PHOTOS = [('zoya', 560, 150), ('vadik', 700, 150), ('cop', 800, 236), ('boss', 700, 316), ('tolik', 560, 300)]
PFN = dict(zoya=(MC.zoya, dict(expr='bored', pose='desk')), vadik=(MC.vadik, dict(expr='sly')), cop=(MC.inspector, dict(expr='glare')),
           boss=(MC.boss, dict(expr='smug')), tolik=(MC.tolik, dict(expr='grin')), maz=(MC.maz, dict(expr='deadpan', ride=False)))
PHEAD = dict(zoya=(40, 230), vadik=(40, 260), cop=(40, 270), boss=(40, 240), tolik=(40, 230), maz=(40, 330))


def mugshot(who, w=60, h=70, s=1.5):
    fn, kw = PFN[who]
    a = portrait(fn, s * 4, (w * 4, h * 4), bg=(200, 196, 186), head=(0.5, 0.48), **kw)
    return np.array(Image.fromarray(a).resize((w, h), Image.NEAREST))


def board_world():
    def mk():
        W = GI.copy()
        im = Image.fromarray(W); d = ImageDraw.Draw(im)
        x0, y0, x1, y1 = BOARD
        d.rectangle([x0, y0, x1, y1], fill=(176, 130, 82), outline=(90, 60, 30), width=5)
        rng = np.random.default_rng(3)
        for _ in range(900):
            x, y = rng.integers(x0 + 6, x1 - 6), rng.integers(y0 + 6, y1 - 6)
            d.point((int(x), int(y)), fill=(150, 108, 66))
        # центр: канистра «КУДА?»
        d.rectangle([668, 236, 724, 296], fill=(200, 40, 40), outline=INK, width=3)
        d.rectangle([700, 226, 716, 238], fill=(200, 40, 40), outline=INK, width=2)
        d.line([(672, 240), (720, 292)], fill=INK, width=2); d.line([(720, 240), (672, 292)], fill=INK, width=2)
        d.rectangle([640, 300, 760, 326], fill=PAPER, outline=INK)
        K._text(d, (700, 313), 'КУДА?!', 14, RED)
        for who, x, y in PHOTOS:
            a = mugshot(who)
            im.paste(Image.fromarray(np.full((76, 66, 3), 236, np.uint8)), (x - 3, y - 3))
            im.paste(Image.fromarray(a), (x, y))
            d.ellipse([x + 26, y - 6, x + 34, y + 2], fill=(220, 40, 40), outline=INK)
        # the empty sixth slot (a clue): a pin and «?»
        d.rectangle([800, 330, 860, 400], fill=(196, 190, 176), outline=INK); K._text(d, (830, 366), '?', 26, INK)
        d.ellipse([826, 324, 834, 332], fill=(220, 40, 40), outline=INK)
        return np.array(im)
    return img('board_world', mk)


def board_hose(big, v, k=1.0):
    pts = [(x + 30, y + 35) for _, x, y in PHOTOS] + [(PHOTOS[0][1] + 30, PHOTOS[0][2] + 35)]
    centre = (696, 266)
    n = int(len(pts) * k)
    for a, b in zip(pts[:n], pts[1:n + 1]): M.rope(big, v.opt(*a), v.opt(*b), sag=30 * v.Z, w=max(6, int(4 * v.Z)), col=(36, 36, 40))
    for p in pts[:min(5, n)]: M.rope(big, v.opt(*p), v.opt(*centre), sag=10 * v.Z, w=max(4, int(3 * v.Z)), col=(36, 36, 40))


def r_board_wide(t, s, u):
    W = board_world()
    Z = 0.72 + 0.03 * u
    m = maz(t, 380.0, 610.0, Z, expr='squint', look=(1.0, -0.4), ride=False, mouth_=0.0, beacon=False)
    wh = A(MC.monowheel_solo, 450.0, 618.0, SP * Z, t=t, talk=wheel_k(t))
    return shot(W, light_gi, 640.0, 370.0, Z, acts=[m, wh], fx_=lambda b, v: board_hose(b, v, sm(u / 2.0)), t=t)


def r_board_cu(t, s, u):
    W = board_world()
    big = shot(W, light_gi, 690.0 + 20 * u, 275.0, 2.2 + 0.08 * u, fx_=lambda b, v: board_hose(b, v), t=t)
    return big


def r_wheel_board(t, s, u):
    W = board_world()
    Z = 1.6
    wh = A(MC.monowheel_solo, 430.0, 650.0, SP * Z * 1.1, t=t, talk=wheel_k(t))
    m = maz(t, 330.0, 640.0, Z, expr='deadpan', look=(1.0, 0.4), ride=False, mouth_=0.0)
    return shot(W, light_gi, 420.0, 560.0, Z, acts=[m, wh], fx_=lambda b, v: board_hose(b, v), t=t)


def r_maz_board(t, s, u):
    W = board_world()
    return cu(W, light_gi, MC.maz, 'maz', t, 640.0, 330.0, sz=14.0, head=(820, 470), expr='proud', look=(1.0, 0.0), ride=False,
              extra=lambda b, v, a: None, blur=3)


# ======================================================================================= suspect cards
CARD = dict(zoya=('ПОДОЗРЕВАЕМАЯ №1', 'ЗОЯ', 'КАССИР АЗС «ГАЗПРОПАЛ»', 'zoya'), vadik=('ПОДОЗРЕВАЕМЫЙ №2', 'ВАДИК', 'ГАРАЖНЫЙ КООПЕРАТИВ', 'vadik'),
            cop=('ПОДОЗРЕВАЕМЫЙ №3', 'ИНСПЕКТОР СТОЛБОВ', 'ДПС, ПОСТ НА ТРАССЕ', 'cop'),
            boss=('ПОДОЗРЕВАЕМЫЙ №4', 'БОРИС БОРИСЫЧ', 'НАЧАЛЬНИК ЦЕХА', 'boss'), tolik=('ПОДОЗРЕВАЕМЫЙ №5', 'ТОЛИК', 'ВОДИТЕЛЬ БЕНЗОВОЗА', 'tolik'))


def card_img(key):
    def mk():
        n, name, role, who = CARD[key]
        W_, H_ = 1500, 860
        im = Image.new('RGB', (W_, H_), (226, 200, 140)); d = ImageDraw.Draw(im); d.fontmode = '1'
        d.rectangle([0, 0, W_ - 1, H_ - 1], outline=(120, 90, 40), width=10)
        d.rectangle([40, 40, 560, 820], fill=(250, 248, 240), outline=INK, width=4)
        fn, kw = PFN[who]
        pa = portrait(fn, 11.0, (500, 760), bg=(186, 190, 196), head=(0.5, 0.36), **kw)
        im.paste(Image.fromarray(pa), (50, 50))
        for y in range(120, 760, 60): d.line([(50, y), (70, y)], fill=INK, width=3)
        d.text((620, 90), n, font=O.pfont(44), fill=(120, 30, 30))
        d.text((620, 200), name, font=O.pfont(56 if len(name) < 12 else 44), fill=INK)
        d.text((620, 300), role, font=O.pfont(28), fill=(70, 60, 50))
        for i, ln in enumerate(['ДЕЛО: ПРОПАЖА БЕНЗИНА', 'СЛЕДОВАТЕЛЬ: МАЗУРОВ Г.П.']):
            d.text((620, 420 + i * 60), ln, font=O.pfont(26), fill=(70, 60, 50))
        return np.array(im)
    return img('card_' + key, mk)


def stamp_img(txt='ПОД ПОДОЗРЕНИЕМ'):
    def mk():
        f = O.pfont(52); bb = f.getbbox(txt)
        st = Image.new('RGBA', (bb[2] - bb[0] + 60, bb[3] - bb[1] + 60), (0, 0, 0, 0)); sd = ImageDraw.Draw(st); sd.fontmode = '1'
        sd.rectangle([3, 3, st.size[0] - 4, st.size[1] - 4], outline=(200, 30, 40, 240), width=8)
        sd.text((30 - bb[0], 30 - bb[1]), txt, font=f, fill=(200, 30, 40, 240))
        return np.array(st.rotate(12, resample=Image.NEAREST, expand=True))
    return img('stamp_' + txt, mk)


def r_card(key):
    def r(t, s, u):
        prev = s.get('bg')
        big = np.zeros((OUT_H, OUT_W, 3), np.uint8); big[:] = (40, 30, 26)
        for y in range(0, OUT_H, 8): big[y:y + 3] = (46, 36, 30)
        c = card_img(key)
        k = sm(u / 0.18)
        x0 = int(210 + (1 - k) * 900); y0 = 110
        O.overlay(big, np.dstack([c, np.full(c.shape[:2], 255, np.uint8)]), x0, y0, 1.0)
        if u > 0.45:
            st = stamp_img(); ks = sm((u - 0.45) / 0.08)
            sc = 1.6 - 0.6 * ks
            st2 = np.array(Image.fromarray(st).resize((int(st.shape[1] * sc), int(st.shape[0] * sc)), Image.NEAREST))
            O.overlay(big, st2, int(1180 - st2.shape[1] / 2), int(640 - st2.shape[0] / 2), 1.0)
            if u < 0.55: B.shake(big, t, 8, 30)
        if u < 0.1: O.flash(big, 0.7 * (1 - u / 0.1))
        grain(big, t, 8)
        return big
    return r


# ======================================================================================= flashback frame (season episode clip)
FBW, FBH = 486, 864


def prep():
    for c in TL.CLIPS:
        d = P.build(BK, f'fb/{c["ep"]}')
        dd = pathlib.Path(d); dd.mkdir(parents=True, exist_ok=True)
        if len(list(dd.glob('*.png'))) > 10: continue
        src = ROOT / 'series' / TL.SLUG / 'episodes' / c['ep'] / 'final.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(c['a']), '-i', str(src), '-t', str(c['b'] - c['a'] + 0.1),
                        '-vf', f'fps=30,scale={FBW}:{FBH}:flags=area', str(dd / '%04d.png')], check=True)
        print(dd)


def fb_frame(ep, i):
    d = pathlib.Path(P.build(BK, f'fb/{ep}'))
    fs = sorted(d.glob('*.png'))
    if not fs: prep(); fs = sorted(d.glob('*.png'))
    return np.array(Image.open(fs[max(0, min(len(fs) - 1, i))]).convert('RGB'))


FB_LABEL = dict(ep01='СЕРИЯ 1', ep02='СЕРИЯ 2', ep03='СЕРИЯ 3', ep04='СЕРИЯ 4')


def r_fb(t, s, u):
    lt = u - 0.25
    fr = fb_frame(s['ep'], int(max(0.0, lt) * 30))
    bgi = np.array(Image.fromarray(fr).resize((OUT_W, int(OUT_W * FBH / FBW)), Image.NEAREST))
    y0 = (bgi.shape[0] - OUT_H) // 2
    big = bgi[y0:y0 + OUT_H].copy()
    big[:] = M.dof(big, 14)
    big[:] = (big * 0.35).astype(np.uint8)
    sepia(big, 0.7)
    k = sm(u / 0.25)
    w, h = int(FBW * (0.8 + 0.2 * k)) + 30, int(FBH * (0.8 + 0.2 * k)) + 30
    ph = np.full((FBH + 60, FBW + 60, 3), 244, np.uint8)
    ph[30:30 + FBH, 30:30 + FBW] = fr
    sepia(ph, 0.25)
    ph = np.array(Image.fromarray(ph).rotate(-2.5, resample=Image.NEAREST, expand=True, fillcolor=(0, 0, 0)))
    m = ph.sum(2) > 0
    x0, yy0 = (OUT_W - ph.shape[1]) // 2, (OUT_H - ph.shape[0]) // 2 + 10
    reg = big[yy0:yy0 + ph.shape[0], x0:x0 + ph.shape[1]]
    reg[m] = ph[m]
    caption_box(big, ['АРХИВ', FB_LABEL[s['ep']]], 120, 120, 36)
    caption_box(big, ['ВОСПОМИНАНИЕ'], 1380, 900, 30, fg=(255, 150, 120))
    grain(big, t, 12)
    if u < 0.12: O.flash(big, 0.6 * (1 - u / 0.12))
    if u > s['t1'] - s['t0'] - 0.2: O.mosaic(big, int(lerp(1, 30, (u - (s['t1'] - s['t0'] - 0.2)) / 0.2)))
    return big


# ======================================================================================= 4. Зоя
def zoya_win(t, Z=1.0, cx=618.0, cy=300.0, who='zoya', gum=0.0, expr='bored', look=(0.3, 0.0), pose='desk', front=None, push=0.0, u=0.0):
    Z = Z + push * u
    acts = [A(MC.zoya, 600.0, 470.0, 4.0 * 3 * Z, t=t, mouth_=mouth(who, t, 1.7), gum=gum, expr=expr, look=look, pose=pose)]
    if front: acts += front(Z)
    big = shot(WIN, K.light_win, cx, cy, Z, acts=acts, t=t)
    v = view_at(WIN, cx, cy, Z, SX, SY)
    xs, ys = v.grid()
    orig = v.bg()
    msk = ((ys[:, None] >= 450) & (ys[:, None] <= 510)) & ((xs[None, :] >= 556) & (xs[None, :] <= 708))
    if not front: big[msk] = orig[msk]
    gl = ((ys[:, None] >= 92) & (ys[:, None] <= 520)) & ((xs[None, :] >= 226) & (xs[None, :] <= 1012))
    yy, xx = np.mgrid[0:OUT_H, 0:OUT_W]
    streak = (((xx + yy * 0.8 + 140) % 620) < 46) & gl
    big[streak] = (big[streak] * 0.72 + np.array([255, 236, 210]) * 0.28).astype(np.uint8)
    return big


def gum_k(t, s): return 0.0


def r_zoya_two(t, s, u):
    """over-the-shoulder: Мазутыч's back-ish profile in the foreground left, Зоя in the window"""
    def front(Z):
        return [maz(t, 330.0, 760.0, Z * 2.0, expr='squint', look=(1.0, -0.3), beacon=True)]
    return zoya_win(t, 0.62, 560.0, 330.0, front=front, look=(-0.6, 0.0), push=0.02, u=u)


def r_zoya_cu(t, s, u):
    return zoya_win(t, 1.35, 618.0, 300.0, look=(-0.7, 0.0), push=0.04, u=u, gum=sm((u - 0.6) / 0.3) * (1 - sm((u - 1.0) / 0.1)))


def r_maz_badge(t, s, u):
    """he slaps a home-made badge «СЛЕДОВАТЕЛЬ» on the counter"""
    def extra(big, v, a):
        k = sm(u / 0.2)
        im = img('badge_sl', lambda: badge_img())
        O.overlay(big, im, int(lerp(1300, 1240, k)), int(lerp(1100, 640, k)), 1.0)
    return cu(WIN, K.light_win, MC.maz, 'maz', t, 600.0, 360.0, sz=14.5, head=(700, 430), expr='proud', look=(1.0, 0.0), beacon=True,
              extra=extra)


def badge_img():
    im = Image.new('RGBA', (440, 260), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.rounded_rectangle([0, 0, 439, 259], 20, fill=(240, 236, 220, 255), outline=(30, 20, 16, 255), width=8)
    d.text((40, 40), 'СЛЕДОВАТЕЛЬ', font=O.pfont(34), fill=(30, 60, 150))
    d.text((40, 110), 'МАЗУРОВ Г.П.', font=O.pfont(26), fill=(30, 20, 16))
    d.text((40, 170), 'ВЫРЕЗАНО ИЗ', font=O.pfont(18), fill=(120, 110, 100))
    d.text((40, 200), 'КОРОБКИ «ДОШИРАК»', font=O.pfont(18), fill=(120, 110, 100))
    return np.array(im)


def r_zoya_ballet(t, s, u):
    return zoya_win(t, 1.25, 618.0, 280.0, pose='ballet', expr='deadpan', look=(-0.4, 0.0))


def r_maz_noir_kiosk(t, s, u):
    big = cu(WIN, K.light_win, MC.maz, 'maz', t, 900.0, 300.0, sz=15.0, head=(1250, 470), expr='squint', look=(-1.0, 0.0), flip=True,
             blur=5, beacon=False)
    noir_bars(big, t, 0.8)
    sepia(big, 0.25)
    return big


def r_zoya_lean(t, s, u):
    return zoya_win(t, 1.55, 618.0, 330.0, look=(-0.8, 0.2), expr='sly', push=0.06, u=u)


# ======================================================================================= 5. Вадик (гаражи)
GROUND = 640.0


def r_vadik_cu(t, s, u, expr='sly'):
    def pre(big, v): K.flare(big, v, t, 1170, 170, 1.0, 0.6)
    car = A(MC.lada, 1020.0, GROUND, 5.0 * 1.3, col=(30, 30, 38), tint=True, trunk=1.0, rims=True, driver=False)
    return cu(GAR, light_gar, MC.vadik, 'vadik', t, 760.0, 420.0, sz=14.0, head=(700, 470), expr=expr, look=(1.0, 0.0), back=[car],
              pre_fx=pre, bottle=True)


def r_vadik_cu2(t, s, u): return r_vadik_cu(t, s, u, 'smug')


def r_maz_garages(t, s, u):
    def pre(big, v): K.flare(big, v, t, 1170, 170, 1.0, 0.6)
    return cu(GAR, light_gar, MC.maz, 'maz', t, 600.0, 400.0, sz=14.0, head=(1180, 470), expr='squint', look=(-1.0, 0.0), flip=True,
              beacon=True, pre_fx=pre)


def r_maz_noir_gar(t, s, u):
    big = r_maz_garages(t, s, u)
    noir_bars(big, t, 0.7); sepia(big, 0.25)
    return big


# ======================================================================================= 6. инспектор (трасса)
PX = 600.0


def cop_scene(t, u, Z, cx, cy, pose='stop', cexpr='glare', mexpr='deadpan', mx=None):
    car = A(MC.lada, PX + 230, y_far(PX + 230) - 4, CAR * Z, t=t, col=(240, 240, 236), police=True, driver=False, web=True)
    bushes = [A(MC.bush, PX + 150, y_far(PX + 150) + 8, SP * Z * 1.3, seed=2), A(MC.bush, PX + 330, y_far(PX + 330) + 10, SP * Z * 1.4, seed=5)]
    cop = A(MC.inspector, PX + 110, y_sh(PX + 110), SP * Z, flip=True, t=t, pose=pose, mouth_=mouth('cop', t), expr=cexpr, whistle=pose == 'stop',
            look=(1.0, 0.0))
    x = mx if mx is not None else PX - 20
    m = maz(t, x, y_sh(x) - 4, Z, expr=mexpr, look=(1.0, -0.2), beacon=True)
    return shot(HW, K.light_hw, cx, cy, Z, acts=bushes + [car, cop, m], fx_=lambda b, v: K.flare(b, v, t, 664, 205, 1.0, 0.6), t=t)


def r_cop_stop(t, s, u):
    return cop_scene(t, u, 1.4, 660.0, 540.0, mx=lerp(380.0, PX - 20, sm(u / 0.5)))


def r_maz_cop(t, s, u):
    return cu(HW, K.light_hw, MC.maz, 'maz', t, 560.0, 420.0, sz=14.0, head=(820, 470), expr='deadpan', look=(1.0, 0.0), beacon=True,
              pre_fx=lambda b, v: K.flare(b, v, t, 664, 205, 1.0, 0.6))


def r_cop_cu(t, s, u):
    return cu(HW, K.light_hw, MC.inspector, 'cop', t, 760.0, 420.0, sz=14.0, head=(1120, 470), expr='smug', pose='point', look=(-1.0, 0.0),
              flip=True, pre_fx=lambda b, v: K.flare(b, v, t, 664, 205, 1.0, 0.6))


def r_maz_noir_hw(t, s, u):
    big = r_maz_cop(t, s, u)
    noir_bars(big, t, 0.7); sepia(big, 0.25)
    return big


def r_tow_cop(t, s, u):
    """déjà vu: the monowheel tows the patrol car again; the inspector rides inside and does the siren"""
    Z = 1.0
    x = 520.0 + 160.0 * u / 3.0
    car_x = x - 170.0
    car = A(MC.lada, car_x, y_sh(car_x) - 2 + 0.6 * abs(math.sin(t * 7)), CAR * Z, t=t, col=(240, 240, 236), police=True, driver=True,
            spin=-t * 4)
    m = maz(t, x, y_sh(x), Z, expr='strain', wind=0.5, spin=t * 22, rot=-12.0, sweat=1.0, beacon=True, mouth_=0.0)

    def f(big, v):
        M.rope(big, aout(m, v, 'belt'), aout(car, v, 'front'), sag=18, w=10)
        ox, oy = v.opt(x, y_sh(x))
        M.sparks(big, ox, oy, t, 14, 160)
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
        K.dust_trail(big, v, t, x - 10, y_sh(x) - 4)
        if speaking('cop', t):                                    # the siren-by-mouth: blue/red blink over the car roof
            cx_, cy_ = aout(car, v, 'front')
            col = (60, 120, 255) if int(t * 8) % 2 else (255, 60, 60)
            fx.glow(big, int(cx_ - 140), int(cy_ - 170), 220, col, 0.6)
    return shot(HW, K.light_hw, x - 70.0, 545.0, Z, acts=[car, m], fx_=f, t=t)


# ======================================================================================= 7. кабинет начальника
DESK = [(250, 395), (978, 395), (978, 615), (250, 615)]
_DMASK = {}


def desk_mask():
    if 'm' not in _DMASK:
        m = Image.new('L', (OFF.shape[1], OFF.shape[0]), 0)
        ImageDraw.Draw(m).polygon(DESK, fill=1)
        ImageDraw.Draw(m).rectangle([300, 330, 420, 400], fill=1)            # phone + abacus on the desk
        ImageDraw.Draw(m).rectangle([740, 330, 830, 400], fill=1)            # the lamp
        _DMASK['m'] = np.array(m).astype(bool)
    return _DMASK['m']


def office(t, Z, cx, cy, boss_kw=None, maz_kw=None, fx_=None):
    bk = dict(t=t, expr='smug', mouth_=mouth('boss', t), look=(-0.8, 0.0), pose='stand')
    bk.update(boss_kw or {})
    b = A(MC.boss, 640.0, 470.0, SP * Z * 1.5, flip=True, **bk)
    acts = [b]
    mz = None
    if maz_kw is not None:
        mk = dict(expr='deadpan', look=(1.0, -0.2), beacon=True, ride=False)
        mk.update(maz_kw)
        mz = maz(t, mk.pop('x', 300.0), 700.0, Z * 1.6, **mk)

    def f(big, v):
        xs, ys = v.grid()
        m = desk_mask()[ys[:, None], xs[None, :]]
        big[m] = v.bg()[m]
        if mz is not None: mz(big, v, light_off(v))
        if fx_: fx_(big, v)
        fx.glow(big, *v.opt(805, 380), 300 * v.Z, (255, 210, 120), 0.25)
    return shot(OFF, light_off, cx, cy, Z, acts=acts, fx_=f, t=t)


def r_office_two(t, s, u):
    return office(t, 0.7 + 0.03 * u, 640.0, 380.0, maz_kw=dict(x=260.0))


def r_boss_cu(t, s, u, expr='shout'):
    return cu(OFF, light_off, MC.boss, 'boss', t, 640.0, 330.0, sz=14.5, head=(1000, 480), expr=expr, look=(-1.0, 0.0), flip=True, blur=3)


def r_boss_cu2(t, s, u): return r_boss_cu(t, s, u, 'smug')


def r_maz_office(t, s, u):
    return cu(OFF, light_off, MC.maz, 'maz', t, 500.0, 360.0, sz=14.0, head=(700, 470), expr='squint', look=(1.0, 0.0), ride=False, blur=4)


def r_boss_talon(t, s, u):
    big = r_boss_cu(t, s, u, 'grin')
    big[:] = (big * 0.7).astype(np.uint8)
    k = sm(u / 0.3)
    M.paper(big, 980, int(lerp(1300, 560, k)), ['ТАЛОН', 'НА ОТВЕТ', 'ВЫДАЧА —', 'ЧЕРЕЗ МЕСЯЦ'], w=620, h=430, rot=-4,
            stamp='ЗАВОД' if u > 0.4 else None, stamp_k=sm((u - 0.4) / 0.1), sizes=[52, 40, 30, 30])
    return big


def r_wheel_office(t, s, u):
    Z = 2.0
    wh = A(MC.monowheel_solo, 470.0, 690.0, SP * Z * 1.1, t=t, talk=wheel_k(t))
    return shot(OFF, light_off, 520.0, 600.0, Z, acts=[wh], t=t)


# ======================================================================================= 8. ночь: слежка и погоня
def r_stakeout(t, s, u):
    Z = 1.4
    bush = A(MC.bush, 440.0, 584.0, SP * Z * 4.0, seed=4)
    m = maz(t, 420.0, 560.0, Z, expr='squint', look=(1.0, -0.1), beacon=False, mouth_=0.0)

    def f(big, v):
        K.flare(big, v, t, 664, 205, 0.8, 0.6)
        hx, hy = aout(m, v, 'eyes')
        for dx in (-26, 26):
            big[int(hy) - 20:int(hy) + 20, int(hx + dx) - 18:int(hx + dx) + 18] = (40, 44, 52)
            big[int(hy) - 12:int(hy) + 12, int(hx + dx) - 10:int(hx + dx) + 10] = (140, 190, 255)
    big = shot(HW, light_night, 560.0, 480.0, Z, acts=[m, bush], fx_=f, t=t)
    return night(big, 0.75, moon=(1500, 150))


def r_stake_cu(t, s, u):
    bush = A(MC.bush, 470.0, 600.0, SP * 2.6 * 2.2, seed=4)
    big = cu(HW, light_night, MC.maz, 'maz', t, 560.0, 420.0, sz=14.0, head=(820, 520), expr='squint', look=(1.0, 0.0), beacon=False,
             front=[bush], wheel_face='low')
    night(big, 0.7)
    caption_box(big, ['ЗАРЯД: 3%'], 1500, 120, 30, fg=(255, 90, 90))
    return big


def r_truck_pass(t, s, u):
    Z = 1.2
    tx = lerp(-200.0, 1200.0, u / 1.4)
    tank = A(MC.tanker, tx, y_near(tx + 140), TRK * Z, t=t, spin=-t * 16, lights=True)
    bush = A(MC.bush, 600.0, 660.0, SP * Z * 2.4, seed=4)

    def f(big, v):
        ox, oy = aout(tank, v, 'front')
        fx.glow(big, int(ox + 60), int(oy - 40), 500, (255, 240, 180), 0.5)
    big = shot(HW, light_night, 560.0, 470.0, Z, acts=[tank, bush], fx_=f, t=t)
    night(big, 0.7)
    K.wind_lines(big, t, 0.5)
    return big


def r_tolik_sing(t, s, u):
    Z = 2.6
    tx = 600.0 + 30 * u
    tank = A(MC.tanker, tx, y_near(tx + 140), TRK * Z, t=t, spin=-t * 16)

    def f(big, v):
        wx, wy = aout(tank, v, 'window')
        wxw, wyw = wpt(v, wx, wy)
        tl = A(MC.tolik, wxw - 4.0, wyw + 10 + 44 * SP / 3, SP * Z, t=t, lean=True, wave=1.0, mouth_=mouth('tolik', t), clip=34.0, expr='grin',
               look=(1.0, -0.3))
        tl(big, v, light_night(v))
        for i in range(3):                                              # music notes
            ph = (t * 0.9 + i / 3) % 1.0
            nx, ny = int(wx + 120 + 200 * ph), int(wy - 120 - 260 * ph)
            if 0 < nx < OUT_W - 40 and 40 < ny < OUT_H:
                big[ny - 30:ny, nx + 18:nx + 24] = (255, 236, 120); big[ny - 8:ny + 8, nx:nx + 24] = (255, 236, 120)
    big = shot(HW, light_night, tx + 190, 525.0, Z, acts=[tank], fx_=f, t=t)
    night(big, 0.6)
    K.wind_lines(big, t, 0.6)
    return big


def r_chase(t, s, u):
    Z = 1.0
    x = 300.0 + 380.0 * u / 2.4
    tank = A(MC.tanker, x + 360, y_far(x + 500), TRK * Z, t=t, spin=-t * 16)
    m = maz(t, x, y_sh(x), Z, expr='strain', wind=1.0, spin=t * 30, rot=-14.0, beacon=True, mouth_=0.0)

    def f(big, v):
        ox, oy = v.opt(x, y_sh(x))
        M.sparks(big, ox, oy, t, 16, 200)
        bx, by = aout(m, v, 'beacon')
        fx.glow(big, int(bx), int(by), 200, (80, 140, 255) if int(t * 8) % 2 else (255, 80, 80), 0.6)
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
    big = shot(HW, light_night, x + 180.0, 480.0, Z, acts=[tank, m], fx_=f, t=t)
    night(big, 0.7, moon=(1600, 140))
    K.wind_lines(big, t, 1.0)
    return big


def r_chase_cu(t, s, u):
    big = cu(HW, light_night, MC.maz, 'maz', t, 600.0 + 400 * u, 420.0, sz=13.0, head=(900, 430), expr='panic', wind=1.0, spin=t * 30,
             beacon=True, rot=-10.0, blur=6)
    night(big, 0.5)
    K.wind_lines(big, t, 1.0)
    B.shake(big, t, 5, 25)
    return big


def r_gate_night(t, s, u):
    Z = 0.62
    tx = lerp(-80.0, 520.0, sm(u / 1.6))
    tank = A(MC.tanker, tx, 660.0, TRK * Z, t=t, spin=-t * 12)
    big = shot(GATE, light_night, 640.0, 380.0, Z, acts=[tank], fx_=gate_fx(t), t=t)
    return night(big, 0.7, moon=(300, 120))


# ======================================================================================= 9. резервуар «ПЛАН» (поворот)
TK = (760.0, 655.0)                                 # the tanker parked at the tank
VALVE = (193.0, 570.0)


def tank_fx(t, pct=147, flip=None, hose=True, gush=0.0):
    def f(big, v):
        K.flare(big, v, t, 1180, 130, 1.1, 0.8)
        im = Image.new('RGBA', (180, 44), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
        k = 1.0 if flip is None else flip
        txt = f'{pct if k >= 0.5 else pct - 1}%'
        K._text(d, (90, 22), txt, 30, (200, 30, 36))
        a = np.array(im); a[..., 3] = (a[..., 3] > 127) * 255
        if flip is not None and 0 < flip < 1:
            sq = max(2, int(44 * abs(math.cos(flip * math.pi))))
            a2 = np.array(Image.fromarray(a).resize((180, sq), Image.NEAREST)); full = np.zeros_like(a); p = (44 - sq) // 2
            full[p:p + sq] = a2; a = full
        ST.blit_world(big, v, a, 742, 374)
        if hose:                                                          # hose from the tanker into the tank pipe
            M.rope(big, v.opt(TK[0] - 40, TK[1] - 40), v.opt(560, 560), sag=30 * v.Z, w=max(8, int(6 * v.Z)), col=(30, 30, 34))
            for i in range(4):                                            # flowing «gasoline» blobs along the hose
                ph = (t * 1.2 + i / 4) % 1.0
                px, py = v.opt(lerp(TK[0] - 40, 560, ph), lerp(TK[1] - 40, 560, ph) + 20 * math.sin(ph * math.pi))
                big[int(py) - 6:int(py) + 6, int(px) - 6:int(px) + 6] = (255, 214, 90)
        if gush > 0:
            ox, oy = v.opt(*VALVE)
            for i in range(30):
                ph = (t * 2 + i / 30) % 1.0
                px, py = int(ox + 60 + ph * 900 * gush), int(oy - 40 - math.sin(ph * math.pi) * 260 * gush)
                if 0 <= px < OUT_W - 16 and 0 <= py < OUT_H - 16: big[py:py + 16, px:px + 16] = (255, 214, 90) if i % 3 else (190, 120, 255)
    return f


def tank_acts(t, Z, tolik_kw=None):
    tank = A(MC.tanker, TK[0], TK[1], TRK * Z, flip=True, t=t)
    acts = [tank]
    if tolik_kw is not None:
        k = dict(t=t, expr='grin', mouth_=mouth('tolik', t), look=(-1.0, 0.0))
        k.update(tolik_kw)
        acts.append(A(MC.tolik, k.pop('x', 520.0), 668.0, SP * Z, flip=True, **k))
    return acts


def r_tank_wide(t, s, u):
    Z = 0.6 + 0.05 * u
    m = maz(t, lerp(80.0, 230.0, sm(u / 1.6)), 676.0, Z, expr='awe', look=(1.0, -0.6), beacon=False, mouth_=0.0)
    return shot(TANK, light_tank, 640.0, 380.0, Z, acts=tank_acts(t, Z, dict(expr='content')) + [m], fx_=tank_fx(t), t=t)


def r_maz_tank(t, s, u):
    return cu(TANK, light_tank, MC.maz, 'maz', t, 600.0, 360.0, sz=14.0, head=(820, 470), expr='stunned', look=(1.0, -0.3), beacon=False,
              pre_fx=tank_fx(t), blur=4)


def r_tolik_tank(t, s, u, Zh=14.0):
    return cu(TANK, light_tank, MC.tolik, 'tolik', t, 700.0, 380.0, sz=Zh, head=(1150, 470), expr='grin', look=(-1.0, 0.0), flip=True,
              pre_fx=tank_fx(t), blur=4)


def r_tolik_tank2(t, s, u): return r_tolik_tank(t, s, u, 15.0)


def r_tank_flip(t, s, u):
    return shot(TANK, light_tank, 832.0, 330.0, 1.9, fx_=tank_fx(t, 148, flip=sm((u - 0.2) / 0.5)), t=t)


def r_maz_tank2(t, s, u):
    big = r_maz_tank(t, s, u)
    return big


def r_valve_tilt(t, s, u):
    """camera tilts down the pipe to the valve with the plate"""
    cy = lerp(380.0, 590.0, sm(u / 1.4))
    cx = lerp(560.0, 260.0, sm(u / 1.4))
    return shot(TANK, light_tank, cx, cy, 1.4 + 0.6 * sm(u / 1.4), fx_=tank_fx(t, 148), t=t)


def r_valve_plate(t, s, u):
    big = shot(TANK, light_tank, 268.0, 618.0, 2.5 + 0.2 * u, fx_=tank_fx(t, 148, hose=False), t=t)
    return big


def r_maz_shock(t, s, u):
    big = cu(TANK, light_tank, MC.maz, 'maz', t, 300.0, 520.0, sz=16.0 + 2 * u, head=(960, 470), expr='shock', look=(0.0, 0.0),
             beacon=False, blur=6)
    if u < 0.3: B.shake(big, t, 10, 30)
    return big


def r_wheel_tank(t, s, u):
    Z = 2.4
    m = maz(t, 300.0, 676.0, Z, expr='stunned', look=(0.0, 0.6), beacon=False, mouth_=0.0)
    return shot(TANK, light_tank, 330.0, 600.0, Z, acts=[m], fx_=tank_fx(t, 148, hose=False), t=t)


def r_tolik_tank3(t, s, u):
    Z = 1.2
    m = maz(t, 300.0, 676.0, Z, expr='sad', look=(1.0, 0.0), beacon=False, mouth_=0.0)
    return shot(TANK, light_tank, 420.0, 520.0, Z, acts=tank_acts(t, Z, dict(x=440.0)) + [m], fx_=tank_fx(t, 148), t=t)


def r_maz_valve(t, s, u):
    Z = 2.0
    m = maz(t, 255.0, 676.0, Z, expr='sad', look=(-1.0, 0.3), beacon=False, flip=True)
    return shot(TANK, light_tank, 260.0, 560.0, Z, acts=[m], fx_=tank_fx(t, 148, hose=False), t=t)


# ======================================================================================= 10. дилемма
def flash_beam(big, v, x, y, t):
    ox, oy = v.opt(x, y)
    fx.glow(big, int(ox), int(oy), 520, (255, 250, 220), 0.55)


def r_boss_run(t, s, u):
    Z = 0.75
    bx = lerp(1250.0, 900.0, sm(u / 1.2))
    b = A(MC.boss, bx, 668.0, SP * Z, flip=True, t=t, expr='panic', mouth_=mouth('boss', t), look=(-1.0, 0.0))
    m = maz(t, 255.0, 676.0, Z, expr='deadpan', look=(1.0, 0.0), beacon=False, mouth_=0.0)

    def f(big, v):
        tank_fx(t, 148)(big, v)
        hx, hy = aout(b, v, 'hand')
        fx.glow(big, int(hx - 300), int(hy), 600, (255, 250, 220), 0.45)
    return shot(TANK, light_tank, 760.0, 470.0, Z, acts=tank_acts(t, Z) + [b, m], fx_=f, t=t)


def r_boss_run2(t, s, u, expr='panic'):
    big = cu(TANK, light_tank, MC.boss, 'boss', t, 900.0, 420.0, sz=14.5, head=(1150, 470), expr=expr, look=(-1.0, 0.0), flip=True, blur=4)
    return big


def r_boss_beg(t, s, u): return r_boss_run2(t, s, u, 'cry')


def r_boss_beg2(t, s, u): return r_boss_run2(t, s, u, 'angry')


def r_maz_valve_cu(t, s, u):
    return cu(TANK, light_tank, MC.maz, 'maz', t, 300.0, 520.0, sz=14.0, head=(760, 470), expr='deadpan', look=(1.0, 0.0), beacon=False,
              blur=5)


def r_maz_hero(t, s, u):
    def pre(big, v): K.flare(big, v, t, 1180, 130, 1.6, 1.0)
    big = cu(TANK, light_tank, MC.maz, 'maz', t, 300.0, 460.0, sz=14.5 + 1.2 * u, head=(900, 500), expr='proud', look=(0.3, -0.3),
             beacon=True, blur=5, pre_fx=pre, wind=0.4)
    return big


def valve_wheel(big, cx, cy, r, ang):
    """the big red hand-wheel in screen space"""
    im = Image.new('RGBA', (2 * r + 40, 2 * r + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    c = r + 20
    d.ellipse([20, 20, 2 * r + 20, 2 * r + 20], outline=INK + (255,), width=int(r * 0.22) + 8)
    d.ellipse([26, 26, 2 * r + 14, 2 * r + 14], outline=(200, 40, 36, 255), width=int(r * 0.2))
    for i in range(5):
        a = ang + i * 2 * math.pi / 5
        d.line([(c, c), (c + math.cos(a) * r * 0.9, c + math.sin(a) * r * 0.9)], fill=INK + (255,), width=int(r * 0.14) + 6)
        d.line([(c, c), (c + math.cos(a) * r * 0.88, c + math.sin(a) * r * 0.88)], fill=(180, 34, 30, 255), width=int(r * 0.12))
    d.ellipse([c - r * 0.2, c - r * 0.2, c + r * 0.2, c + r * 0.2], fill=(120, 120, 126, 255), outline=INK + (255,), width=6)
    O.overlay(big, np.array(im), int(cx - c), int(cy - c), 1.0)


def r_valve_turn(t, s, u):
    """slow motion: both gloves on the wheel; it turns; gasoline bursts out; the flare roars"""
    big = shot(TANK, light_tank, 300.0, 540.0, 1.3, fx_=tank_fx(t, 148, hose=False, gush=sm((u - 1.2) / 0.8)), t=t)
    big[:] = M.dof(big, 5)
    ang = -1.6 * sm((u - 0.3) / 1.4)
    valve_wheel(big, 860, 560, 330, ang)
    if u > 1.2:
        fx.glow(big, 960, 300, 900, (255, 214, 90), 0.4 * sm((u - 1.2) / 0.5))
        B.shake(big, t, 8 * sm((u - 1.2) / 0.3), 30)
    return big


# ======================================================================================= 11. утро: раздача у ворот
def crowd_acts(t, Z, honk=True):
    acts = []
    q = [(220, 'lada', 0), (420, 'buh', 1), (620, 'police', 2), (820, 'priora', 3), (1020, 'lada', 5)]
    for i, (x, kind, c) in enumerate(q):
        b = abs(math.sin(t * 30 + i)) * 1.5 if honk else 0.0
        y = 668.0 - b
        if kind == 'lada': acts.append(A(MC.lada, x, y, CAR * Z, col=MC.CAR_COLS[c], rust=i + 1))
        elif kind == 'buh': acts.append(A(MC.buhanka, x, y, CAR * Z))
        elif kind == 'police': acts.append(A(MC.lada, x, y, CAR * Z, col=(240, 240, 236), police=True))
        else: acts.append(A(MC.lada, x, y, CAR * Z, col=(30, 30, 38), tint=True, rims=True, driver=False))
    return acts


def canisters(big, v, t):
    for i, x in enumerate((300, 520, 700, 900, 1100)):
        ox, oy = v.opt(x, 690)
        s_ = int(26 * v.Z)
        big[int(oy) - 2 * s_:int(oy), int(ox) - s_:int(ox) + s_] = INK
        big[int(oy) - 2 * s_ + 4:int(oy) - 4, int(ox) - s_ + 4:int(ox) + s_ - 4] = (200, 40, 40)


def r_crowd_gate(t, s, u):
    Z = 0.95 + 0.03 * u
    m = maz(t, 600.0, 690.0, Z, expr='smile', look=(-1.0, 0.0), flip=True, beacon=True, mouth_=0.0)
    def f(big, v):
        gate_fx(t, 147)(big, v); canisters(big, v, t)
    big = shot(GATE, light_morning, 640.0, 540.0, Z, acts=crowd_acts(t, Z) + [m], fx_=f, t=t)
    K.confetti(big, t, s['t0'] + 0.3, n=90, seed=3)
    return big


def r_tolik_crowd(t, s, u):
    return cu(GATE, light_morning, MC.tolik, 'tolik', t, 700.0, 420.0, sz=14.0, head=(1100, 470), expr='grin', look=(-1.0, 0.0),
              flip=True, wave=1.0, back=crowd_acts(t, 1.3), blur=3)


def r_zoya_mega(t, s, u):
    Z = 1.6
    z = A(MC.zoya, 560.0, 640.0, 4.0 * 3 * Z * 0.62, t=t, mega=True, mouth_=mouth('zoya', t), expr='bored', look=(1.0, 0.0))
    car = A(MC.lada, 600.0, 652.0, CAR * Z, col=MC.CAR_COLS[0], rust=1)
    return shot(GATE, light_morning, 600.0, 520.0, Z, acts=[z, car], fx_=gate_fx(t), t=t)


def r_banner_fall(t, s, u):
    vals = [147, 120, 90, 60, 30, 12, 0]
    i = min(len(vals) - 1, int(u / 0.28))
    big = shot(GATE, light_morning, 650.0, 175.0, 1.8, fx_=lambda b, v: (K.flare(b, v, t, 1180, 140, 1.2, 1.0), plan_set(b, v, vals[i])),
               t=t)
    if u % 0.28 < 0.06: B.shake(big, t, 6, 30)
    return big


def plan_set(big, v, pct):
    im = Image.new('RGBA', (240, 70), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
    K._text(d, (120, 36), f'{pct}%', 44, (200, 30, 36))
    a = np.array(im); a[..., 3] = (a[..., 3] > 127) * 255
    ST.blit_world(big, v, a, 530, 152)


def r_boss_cry(t, s, u):
    def pre(big, v):
        K.flare(big, v, t, 1180, 140, 1.0, 0.6); plan_set(big, v, 0)
    return cu(GATE, light_morning, MC.boss, 'boss', t, 640.0, 260.0, sz=14.5, head=(900, 520), expr='cry', look=(0.0, -0.8), pre_fx=pre,
              blur=2)


def r_maz_smile(t, s, u):
    def pre(big, v): K.flare(big, v, t, 1180, 140, 1.0, 0.6)
    return cu(GATE, light_morning, MC.maz, 'maz', t, 500.0, 360.0, sz=14.0, head=(820, 480), expr='smile', look=(1.0, -0.2), beacon=True,
              pre_fx=pre, back=crowd_acts(t, 1.0, honk=False), blur=3)


def r_cop_drive(t, s, u):
    Z = 1.8
    x = 560.0 + 200.0 * sm(u / 2.0)
    car = A(MC.lada, x, 668.0, CAR * Z, t=t, col=(240, 240, 236), police=True, driver=True, spin=-t * 8)

    def f(big, v):
        gate_fx(t, 0)(big, v)
        cx_, cy_ = aout(car, v, 'front')
        col = (60, 120, 255) if int(t * 8) % 2 else (255, 60, 60)
        fx.glow(big, int(cx_ - 160), int(cy_ - 180), 240, col, 0.6)
        K.exhaust(big, v, t, x - 70, 655)
    return shot(GATE, light_morning, 680.0, 600.0, Z, acts=[car], fx_=f, t=t)


def r_zoya_dance(t, s, u):
    Z = 1.4
    z = A(MC.zoya, 640.0, 620.0, 4.0 * 3 * Z * 0.62, t=t, pose='ballet', mouth_=mouth('zoya', t), expr='deadpan', look=(1.0, 0.0),
          rot=8 * math.sin(t * 4))
    car = A(MC.lada, 600.0, 690.0, CAR * Z, col=MC.CAR_COLS[2], rust=2)
    big = shot(GATE, light_morning, 640.0, 500.0, Z, acts=[z, car], fx_=gate_fx(t, 0), t=t)
    K.confetti(big, t, s['t0'], n=80, seed=9)
    return big


# ======================================================================================= 12. кнопка и петля
VX = 1040.0


def r_maz_canister(t, s, u):
    Z = 1.2
    x = lerp(700.0, 900.0, sm(u / 1.2))
    car = A(MC.vesta, VX, 520.0, CAR * Z, t=t, bow=0.0)
    m = maz(t, x, 524.0, Z, expr='joy', look=(1.0, -0.2), beacon=True, mouth_=0.0)

    def f(big, v):
        hx, hy = aout(m, v, 'hand')
        c = int(24 * Z * 1.5)
        big[int(hy) - c:int(hy) + c, int(hx) - c:int(hx) + c] = INK
        big[int(hy) - c + 5:int(hy) + c - 5, int(hx) - c + 5:int(hx) + c - 5] = (200, 40, 40)
        K.flare(big, v, t, 664, 205, 1.0, 0.6)
    return shot(HW, K.light_hw, 920.0, 440.0, Z, acts=[car, m], fx_=f, t=t)


def r_maz_vesta(t, s, u):
    car = A(MC.vesta, VX + 60, 520.0, CAR * 2.0, t=t, bow=0.0)
    return cu(HW, K.light_hw, MC.maz, 'maz', t, 960.0, 380.0, sz=14.0, head=(640, 470), expr='joy', look=(1.0, 0.2), beacon=True,
              back=[car], blur=3)


def r_hatch(t, s, u):
    Z = 2.6
    car = A(MC.vesta, VX, 520.0, CAR * Z, t=t, bow=0.0, flap=sm((u - 0.2) / 0.3), plug=False)

    def f(big, v):
        if u > 0.3:
            fx_, fy_ = aout(car, v, 'flap')
            M.sparks(big, fx_, fy_, t, 30, 300)
            fx.glow(big, int(fx_), int(fy_), 300, (120, 220, 255), 0.5)
    big = shot(HW, K.light_hw, VX - 40, 480.0, Z, acts=[car], fx_=f, t=t)
    if u > 0.3 and u < 0.6: B.shake(big, t, 8, 30)
    return big


def r_zoya_pass(t, s, u):
    return zoya_win(t, 1.35, 618.0, 300.0, look=(-0.7, 0.0))


def r_wheel_end(t, s, u):
    Z = 2.4
    m = maz(t, 900.0, 524.0, Z, expr='sad', look=(0.0, 0.6), beacon=False, mouth_=0.0, dead=u > s['t1'] - s['t0'] - 1.2, wheel_face='low')
    big = shot(HW, K.light_hw, 900.0, 470.0, Z, acts=[m], t=t)
    if u > s['t1'] - s['t0'] - 1.4: M.zzz(big, 1100, 700, t)
    return big


def r_loud_end(t, s, u):
    big = r_loudspeaker(t, s, u)
    if u > 3.0:
        big[:] = (big * (1 - 0.5 * sm((u - 3.0) / 1.0))).astype(np.uint8)
    return big


def r_sign_back(t, s, u):
    def f(big, v):
        K.flare(big, v, t, 664, 205, 0.6, 0.6)
    big = shot(HW, light_night, 1150.0, 230.0, 1.5 + 0.1 * u, fx_=f, t=t)
    return night(big, 0.7)


def r_loop_pump(t, s, u):
    big = r_hook(t, s, 0.6)
    return big


def r_credits(t, s, u):
    big = np.zeros((OUT_H, OUT_W, 3), np.uint8); big[:] = (14, 10, 12)
    rows = [('В РОЛЯХ', None), ('МАЗУТЫЧ', 'СЛЕДОВАТЕЛЬ'), ('ДИН-ДОН 3000', 'НАПАРНИК, 3%'), ('ЗОЯ', 'БАЛЕРИНА'),
            ('ВАДИК', 'СВЕЖАК'), ('ИНСПЕКТОР СТОЛБОВ', 'УИ-У'), ('БОРИС БОРИСЫЧ', 'ПЛАН'), ('ТОЛИК', 'ТУДА-ОБРАТНО'),
            ('ЗАДВИЖКА', 'САМА СЕБЯ'), ('БЕНЗИН', 'НЕ НАЙДЕН')]
    y = int(OUT_H - u * 230)
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    for a, b in rows:
        if b is None:
            d.text((960, y), a, font=O.pfont(56), fill=(255, 214, 90), anchor='mm')
        else:
            d.text((900, y), a, font=O.pfont(40), fill=(240, 236, 220), anchor='rm')
            d.text((1020, y), b, font=O.pfont(40), fill=(255, 156, 40), anchor='lm')
        y += 110
    big = np.array(im)
    grain(big, t, 6)
    return big


S2 = None


def r_s2_card(t, s, u):
    global S2
    big = r_sign_back(t, s, 1.0)
    big[:] = (big * 0.35).astype(np.uint8)
    if S2 is None: S2 = K.hook_title(['СЕЗОН 2:', 'ЗАРЯДКИ НЕТ'], 90)
    O.overlay(big, S2, 0, 240, sm(u / 0.25))
    return big


# ======================================================================================= dispatcher + overlays
SHOT = dict(hook=r_hook, drop_cu=r_drop_cu, maz_pump=r_maz_pump, drop_fall=r_drop_fall, maz_noir=r_maz_noir, title=r_title,
            gate_wide=r_gate_wide, banner_cu=r_banner_cu, maz_gate=r_maz_gate, loudspeaker=r_loudspeaker,
            board_wide=r_board_wide, board_cu=r_board_cu, wheel_board=r_wheel_board, maz_board=r_maz_board,
            card_zoya=r_card('zoya'), card_vadik=r_card('vadik'), card_cop=r_card('cop'), card_boss=r_card('boss'), card_tolik=r_card('tolik'),
            zoya_two=r_zoya_two, zoya_cu=r_zoya_cu, maz_badge=r_maz_badge, zoya_ballet=r_zoya_ballet, maz_noir_kiosk=r_maz_noir_kiosk,
            fb_zoya=r_fb, fb_boss=r_fb, fb_cop=r_fb, fb_tolik=r_fb, zoya_lean=r_zoya_lean,
            vadik_cu=r_vadik_cu, maz_garages=r_maz_garages, vadik_cu2=r_vadik_cu2, maz_noir_gar=r_maz_noir_gar,
            cop_stop=r_cop_stop, maz_cop=r_maz_cop, cop_cu=r_cop_cu, maz_noir_hw=r_maz_noir_hw, tow_cop=r_tow_cop, tow_cop2=r_tow_cop,
            office_two=r_office_two, boss_cu=r_boss_cu, maz_office=r_maz_office, boss_cu2=r_boss_cu2, boss_talon=r_boss_talon,
            wheel_office=r_wheel_office,
            stakeout=r_stakeout, stake_cu=r_stake_cu, truck_pass=r_truck_pass, tolik_sing=r_tolik_sing, chase=r_chase, chase_cu=r_chase_cu,
            gate_night=r_gate_night,
            tank_wide=r_tank_wide, maz_tank=r_maz_tank, tolik_tank=r_tolik_tank, tolik_tank2=r_tolik_tank2, tank_flip=r_tank_flip,
            maz_tank2=r_maz_tank2, valve_tilt=r_valve_tilt, valve_plate=r_valve_plate, maz_shock=r_maz_shock, wheel_tank=r_wheel_tank,
            tolik_tank3=r_tolik_tank3, maz_valve=r_maz_valve,
            boss_run=r_boss_run, boss_run2=r_boss_run2, boss_beg=r_boss_beg, maz_valve_cu=r_maz_valve_cu, boss_beg2=r_boss_beg2,
            maz_hero=r_maz_hero, valve_turn=r_valve_turn,
            crowd_gate=r_crowd_gate, tolik_crowd=r_tolik_crowd, zoya_mega=r_zoya_mega, banner_fall=r_banner_fall, boss_cry=r_boss_cry,
            maz_smile=r_maz_smile, cop_drive=r_cop_drive, zoya_dance=r_zoya_dance,
            maz_canister=r_maz_canister, maz_vesta=r_maz_vesta, hatch=r_hatch, zoya_pass=r_zoya_pass, wheel_end=r_wheel_end,
            loud_end=r_loud_end, sign_back=r_sign_back, loop_pump=r_loop_pump, credits=r_credits, s2_card=r_s2_card)
NOHUD = ('title', 'credits', 's2_card', 'card_zoya', 'card_vadik', 'card_cop', 'card_boss', 'card_tolik', 'fb_zoya', 'fb_boss', 'fb_cop',
         'fb_tolik')
NOCAP = ('title', 'credits', 's2_card', 'fb_zoya', 'fb_boss', 'fb_cop', 'fb_tolik')
HOOK = None


def stickers():
    if 'st' in _IMG: return _IMG['st']
    f = TL.first
    out = [(O.sticker('КАП.', fg=(255, 214, 90), size=70), f('drop_fall')['t0'] + 0.6, f('drop_fall')['t1'], 1200, 760),
           (O.sticker('147%?!', fg=(255, 90, 90), size=64), f('banner_cu')['t0'] + 0.3, f('banner_cu')['t1'], 1500, 760),
           (O.sticker('СОХРАНЁН?', fg=(255, 236, 120), size=56), f('loudspeaker')['t1'] - 1.4, f('loudspeaker')['t1'], 1450, 820),
           (O.sticker('ШЕСТЬ?!', fg=(90, 230, 255), size=64), f('wheel_board')['t0'] + 1.0, f('wheel_board')['t1'], 1450, 260),
           (O.sticker('ДЕЖАВЮ', fg=(255, 236, 120), size=60), f('tow_cop')['t0'] + 0.4, f('tow_cop')['t1'], 1450, 220),
           (O.sticker('ТУДА-ОБРАТНО', fg=(120, 255, 140), size=56), f('tolik_tank')['t0'] + 1.2, f('tolik_tank')['t1'], 600, 220),
           (O.sticker('ЭТО Я?!', fg=(255, 90, 90), size=80), f('maz_shock')['t0'], f('maz_shock')['t1'], 1500, 260),
           (O.sticker('БЕЗ ТАЛОНОВ!', fg=(120, 255, 140), size=60), f('zoya_mega')['t0'] + 0.6, f('zoya_mega')['t1'], 1450, 240),
           (O.sticker('0%', fg=(255, 90, 90), size=90), f('banner_fall')['t1'] - 0.5, f('boss_cry')['t1'], 1600, 240),
           (O.sticker('ЭЛЕКТРО?!', fg=(255, 236, 90), size=64), f('hatch')['t0'] + 0.4, f('zoya_pass')['t1'], 1450, 220)]
    _IMG['st'] = out
    return out


def hud(big):
    O.overlay(big, img('badge', lambda: O.make_badge('МАЗУТЫЧ • СЛЕДСТВИЕ ПО БЕНЗИНУ', 26)), 34, 30, 1.0)


FLASH_AT = ('valve_plate', 'maz_shock', 'tank_wide', 'valve_turn', 'crowd_gate', 'hatch')
MOSAIC_AT = ('gate_wide', 'board_wide', 'tank_wide', 'crowd_gate', 'credits', 'maz_canister', 'office_two', 'zoya_two', 'cop_stop')


def render_scene(t):
    s = TL.shot_at(t)
    return SHOT[s['name']](t, s, t - s['t0'])


def render(t):
    global HOOK
    s = TL.shot_at(t)
    u = t - s['t0']
    big = render_scene(t)
    if s is TL.SHOTS[0] or s is TL.SHOTS[1]:
        if HOOK is None: HOOK = K.hook_title(['КУДА ДЕЛИ', 'БЕНЗИН?!'], 84, width=OUT_W)
        if 0.06 <= t < 2.6:
            k = min(1.0, (t - 0.06) / 0.1) * (1 - sm((t - 2.45) / 0.15))
            O.overlay(big, HOOK, 0, 40, k)
    for im, t0, t1, cx, cy in stickers(): O.draw_sticker(big, im, t, t0, t1, cx, cy)
    if s['name'] not in NOCAP: EPI.captions.draw(big, t, 960)
    if s['name'] not in NOHUD: hud(big)
    if s['name'] in FLASH_AT and u < 0.15: O.flash(big, 0.6 * (1 - u / 0.15))
    if s['name'] in MOSAIC_AT and u < 0.3: O.mosaic(big, int(lerp(40, 1, u / 0.3)))
    return big


CUTS, NAMES = TL.CUTS, TL.NAMES


def sheet(ids):
    tiles = []
    for x in ids:
        i = int(x) if x.isdigit() else NAMES.index(next(nm for nm in NAMES if nm == x or nm[3:] == x))
        s = TL.SHOTS[i]; tm = (s['t0'] + s['t1']) / 2
        im = Image.fromarray(render(tm)).resize((480, 270), Image.LANCZOS)
        ImageDraw.Draw(im).text((6, 4), f'{NAMES[i]} {tm:.1f}', fill=(255, 255, 0))
        tiles.append(im)
    cols = 3; rows = (len(tiles) + cols - 1) // cols
    sh = Image.new('RGB', (480 * cols, 270 * rows))
    for k, im in enumerate(tiles): sh.paste(im, ((k % cols) * 480, (k // cols) * 270))
    out = P.build(BK, 'msheet.png'); sh.save(out); print(out)


if __name__ == '__main__':
    if sys.argv[1] == 'prep': prep()
    elif sys.argv[1] == 'sheet': sheet(sys.argv[2:])
    else: EPI.main(render, __file__)
