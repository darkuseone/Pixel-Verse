"""S01E03 «Good Boy» (09.10.2026) — the hospital billing window: a Florida-shaped bump, a tiny ice pack, a bill to the floor.
«TWO GRAND?! For an ICE PACK?!» Tanner (job #3, billing): «It's ORGANIC ice!» — «It's WATER.» — «Out-of-NETWORK water!» — «Mort. Hold my
sub.» GULP. Mort bills him: «Holding fee. Eighty BUCKS.» Florida Man goes to the vet instead (Dr. Paws, EXAM $40; poster MICROCHIP
SPECIAL = the clue), writes SPECIES: FLORIDA, sits next to an iguana. Tanner (job #4, vet): «Who's a GOOD boy?» — «Me.» TWIST (55 %, the
network sees all): the cone snaps on — «And a little MICROCHIP!» BEEP. Darlene's tablet: MAN, FLORIDA — LIVE. «Gotcha.» He hides in the
mangroves, in the gator-jerky booth, behind his dead A/C: BEEP, BEEP, BEEP. «Mornin', [BEEP].» Mugshot in the cone, BREAKING, 7/10.
Her pet scanner: SHOTS: UP TO DATE + a receipt. Button: «Good boy. Scan's two GRAND.» -> loop «TWO GRAND?!»
  python3 ep03.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
from stage import view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
from episode import Episode
from props import fmpix as FX
from props import fmcast as C
from props import fmkit as K
from props import bytfx as B
from props.dibspix import blit
from timeline import DUR, FPS, VOICE, SLUG, CUTS, BEEPS

EPI = Episode('ep03', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
K.SLOGAN[:] = ['CHIPPED? SCANNED?', 'BILLED? CALL MORT.']
HOSP = K.world_baked('hospital')
VET = K.world_baked('vet')
SWAMP = K.world('swamp')
BOOTH = K.world_baked('booth')
YARD = K.world_baked('yard')
STORE = K.world_baked('store')
A, wpt, aout = K.A, K.wpt, K.aout
LH = lambda v: K.light_store(v)
WIN = (312, 178, 988, 430)          # hospital: the glass billing window (world box); its ledge is at y 430
POST2 = (570.0, 466.0)              # top of the middle rope stanchion (Mort's perch)
H_FLOOR = 700.0                     # customers' feet at the billing window
CHAIRS = [470.0, 570.0, 670.0, 770.0, 870.0]
SEAT, V_FLOOR = 392.0, 505.0        # vet: chair seat top / floor at the wall
SAND, AC = 626.0, (520.0, 612.0)    # yard (E01)
BWIN = (444, 300, 836, 440)         # booth: the service window opening (world box), counter shelf at 440
S_FRONT, S_GLASS, S_POST = 20.0, 15.0, 8.0
S_SIT, S_TV = 22.0, 20.0            # vet: sitting on a chair / Tanner standing in front of the chairs
S_YARD, S_AC = 10.0, 13.8


def mouth(who, t, k=1.8):
    return min(1.0, talk(who, t) * k)


def cu(world, light, fn, t, cx, cy, sc, head, Z=1.4, flip=False, blur=0, pre_=None, fx_=None, pin='head', extra=(), **kw):
    kw.setdefault('t', t)
    v0 = view_at(world, cx, cy, Z, 180, 320)
    hx, hy = wpt(v0, *head)
    a = A(fn, hx, hy, sc, flip=flip, pin=pin, **kw)
    def pre(big, v):
        if pre_: pre_(big, v)
        if blur: big[:] = K.dof(big, blur)
    big = K.shot(world, light, cx, cy, Z, acts=list(extra) + [a], pre=pre, fx_=(lambda b, v: fx_(b, v, a)) if fx_ else None, sx=180, sy=320)
    return big, a, v0


def keep_box(big, bg0, v, box):
    """only the part of the frame inside world box stays (a figure behind a wall seen through an opening)"""
    x0, y0 = v.opt(box[0], box[1]); x1, y1 = v.opt(box[2], box[3])
    x0, y0, x1, y1 = (int(np.clip(q, 0, m)) for q, m in ((x0, OUT_W), (y0, OUT_H), (x1, OUT_W), (y1, OUT_H)))
    m = np.ones(big.shape[:2], bool); m[y0:y1, x0:x1] = False
    big[m] = bg0[m]
    return x0, y0, x1, y1


def glass(big, box_o, t, a=0.16):
    """tinted glass + diagonal glare streaks over an output-px box"""
    x0, y0, x1, y1 = box_o
    if x1 <= x0 or y1 <= y0: return
    reg = big[y0:y1, x0:x1].astype(np.float32)
    big[y0:y1, x0:x1] = (reg * (1 - a) + np.array((200, 236, 236)) * a).astype(np.uint8)
    for k_, (ox, w) in enumerate(((0.12, 60), (0.3, 22), (0.72, 80))):
        for y in range(y0, y1, 12):
            xa = int(x0 + (x1 - x0) * ox + (y - y0) * 0.45)
            if x0 <= xa < x1:
                xb = min(x1, xa + w)
                big[y:y + 12, xa:xb] = (big[y:y + 12, xa:xb] * 0.78 + 56).astype(np.uint8)


def tanner_glass(v, t, x=650.0, **kw):
    kw.setdefault('expr', 'chipper'); kw.setdefault('look', (0.0, 0.0))
    return A(C.tanner, x, 640.0, S_GLASS * v.Z, flip=True, t=t, uniform='billing', jobs=3, mouth_=mouth('tanner', t, 2.0), **kw)


def hosp_shot(t, cx, cy, Z, back=(), acts=(), fx_=None):
    def pre(big, v):
        bg0 = big.copy()
        lt = LH(v)
        for b in back: b(v)(big, v, lt)
        box = keep_box(big, bg0, v, WIN)
        glass(big, box, t)
    v = view_at(HOSP, cx, cy, Z, 180, 320)
    return K.shot(HOSP, LH, cx, cy, Z, acts=[a(v) for a in acts], pre=pre, fx_=fx_, sx=180, sy=320)


def receipt(big, x, y0, y1, t, w=110):
    """the endless itemised hospital bill hanging down to the floor (screen space)"""
    for i, y in enumerate(range(int(y0), int(y1), 14)):
        xx = int(x + 26 * math.sin(y * 0.006 + t * 2.0))
        big[y:y + 14, xx:xx + w] = (250, 250, 244)
        big[y:y + 14, xx:xx + 4] = (200, 200, 196)
        if i % 3 == 1: big[y + 4:y + 8, xx + 12:xx + w - 30] = (150, 150, 160)
        if i % 3 == 1: big[y + 4:y + 8, xx + w - 24:xx + w - 10] = (226, 60, 60)


def bill_overlay(big, t, x=150, y=120, w=300):
    pass


_FG = {}


def wall_fg(big, y0):
    """the billing window's ledge + the tiled wall below it, in the foreground of a close-up behind the glass"""
    if 'w' not in _FG:
        crop = HOSP[426:560, 330:700]
        im = Image.fromarray(crop).resize((OUT_W, int(OUT_W * crop.shape[0] / crop.shape[1])), Image.NEAREST)
        _FG['w'] = K.dof(np.array(im), 3)
    a = _FG['w']
    h = min(a.shape[0], OUT_H - y0)
    if h > 0: big[y0:y0 + h] = a[:h]
    if y0 + h < OUT_H: big[y0 + h:] = a[-1]


def blit_sprite(big, fn, x, y, sc, lt=None, flip=False, **kw):
    sp = FX.draw(fn, sc, flip=flip, **kw)
    blit(big, sp, x, y, sc, lt, flip)
    return sp


def beep_ring(big, x, y, t, t0):
    """the chip pinging: expanding red rings + a red glow at (x, y)"""
    if not (t0 <= t < t0 + 0.5): return
    u = (t - t0) / 0.5
    fx.glow(big, int(x), int(y), int(60 + 120 * u), (255, 40, 40), 0.7 * (1 - u))
    yy, xx = np.ogrid[0:OUT_H, 0:OUT_W]
    for k in range(2):
        r = 40 + 360 * ((u + k * 0.4) % 1.0)
        ring = np.abs(np.sqrt((xx - x) ** 2 + (yy - y) ** 2) - r) < 9
        big[ring] = (255, 60, 60)


def cone_out(act, v):
    """output position of the cone rim (in front of the face)"""
    hx, hy = aout(act, v, 'head')
    return hx, hy


# ================================================================== shots
def r_hook(t, u):
    """XCU at the billing window: a Florida-shaped bump, a tiny ice pack balanced on it, the bill unrolling to the floor"""
    def pre(big, v):
        big[:] = K.dof(big, 6)
    big, a, v = cu(HOSP, LH, C.fm, t, 640.0, 300.0, 30.0, (500, 900), Z=1.35, pre_=pre, expr='shriek', mouth_=mouth('fm', t),
                   sweat=0.5, glasses_drop=min(1.0, 0.2 + u / 1.2), look=(0.6, 0.3), bump=True, ice=True)
    receipt(big, 800, 380, min(OUT_H, 380 + 2600 * min(1.0, u / 0.7)), t)
    if u < 0.5: B.shake(big, t, 9, 33)
    return big


def r_tanner_glass(t, u):
    """MS: Tanner behind the billing glass in pale-blue scrubs, holding up the tiny ice pack: «It's ORGANIC ice!»"""
    Z = 1.3
    return hosp_shot(t, 650.0, 320.0, Z, back=[lambda v: tanner_glass(v, t, hand_n=(11.0, 58.0), prop_n=lambda sp, h: C.icepack(sp, (h[0] + 0.6, h[1] - 0.4)))],
                     acts=[lambda v: A(C.fm, 470.0, H_FLOOR, S_FRONT * v.Z, t=t, expr='stunned', look=(0.8, 0.4), bump=True, ice=True, shadow=0.3)])


def r_fm_water(t, u):
    """CU: deadpan, the ice pack melting on the bump, one drip: «It's WATER.»"""
    def fx_(big, v, a):
        hx, hy = aout(a, v, 'head')
        yy = hy - 380 + 1800 * max(0.0, u - 0.1) ** 2
        if yy < OUT_H: B.puff(big, hx - 10, yy, 16, 1.0, (150, 214, 255))
    big, a, v = cu(HOSP, LH, C.fm, t, 520.0, 300.0, 27.0, (540, 860), Z=1.35, blur=6, expr='deadpan', mouth_=mouth('fm', t), look=(0.5, 0.0),
                   bump=True, ice=True, fx_=fx_)
    return big


def r_tanner_cu(t, u):
    """CU: Tanner behind the glass at the speaking hole, beaming: «Out-of-NETWORK water!»"""
    def pre(big, v):
        pass
    def fx_(big, v, a):
        glass(big, (0, 0, OUT_W, 1300), t, 0.12)
        wall_fg(big, 1300)
        cx, cy = 560, 1150                                         # the round speaking grille in the glass
        yy, xx = np.ogrid[0:OUT_H, 0:OUT_W]
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        ring = (d < 120) & (d > 104)
        big[ring] = (190, 196, 204)
        holes = (d < 100) & ((xx // 24 + yy // 24) % 2 == 0) & ((xx % 24) < 8) & ((yy % 24) < 8)
        big[holes] = (60, 70, 80)
    big, a, v = cu(HOSP, LH, C.tanner, t, 650.0, 260.0, 22.0, (540, 760), Z=1.35, blur=7, flip=True, expr='chipper', uniform='billing', jobs=3,
                   mouth_=mouth('tanner', t, 2.0), look=(0.0, 0.0), thumbs=u > 0.5, hand_n=(11.0, 50.0) if u > 0.5 else None, fx_=fx_)
    return big


def r_mort_hold(t, u):
    """MS: Florida Man hands the sub to Mort perched on the rope stanchion — GULP (8.70); the sub shows in the pouch"""
    Z = 1.6
    gone = t >= 8.7
    gul = min(1.0, max(0.0, (t - 8.7) / 0.3))
    fm_ = lambda v: A(C.fm, 700.0, 620.0, 14.0 * v.Z, flip=True, t=t, expr='zen', mouth_=mouth('fm', t), look=(0.8, 0.5), bump=True,
                      hand_n=(15.0, 39.0), prop_n=None if gone else (lambda sp, h: C.sub(sp, (h[0] + 1.0, h[1] + 1.0), ang=0.2)), shadow=0.3)
    mort = lambda v: A(C.mort, *POST2, S_POST * v.Z, t=t, expr='deadpan' if not gone else 'smug', mouth_=mouth('mort', t), look=(1.0, -0.4),
                       lump='sub' if gone else None, gulp=gul if gone else 0.0, lift=0.5 * (1 - gul) if t > 8.3 else 0.0)
    return hosp_shot(t, 640.0, 440.0, Z, back=[lambda v: tanner_glass(v, t, x=760.0, look=(-0.6, -0.2))], acts=[mort, fm_])


def r_mort_bill(t, u):
    """CU: Mort on the stanchion to camera, the sub in his pouch, an invoice slides into frame: «Holding fee. Eighty BUCKS.»"""
    big, a, v = cu(HOSP, LH, C.mort, t, 560.0, 330.0, 24.0, (560, 760), Z=1.35, blur=7, expr='smug', mouth_=mouth('mort', t),
                   look=(-0.1, -0.1), lump='sub', lift=0.2)
    k = sm(min(1.0, u / 0.35))
    K.invoice_card(big, lerp(-560, 70, k), 1140, 520, ang=-7.0, amount='$80', head='MORT POUCH ESQ.',
                   lines=('HOLDING: 1 SUB', 'IN POUCH. SAFE.'), hc=(20, 140, 150))
    return big


def r_vet_in(t, u):
    """wide: Dr. Paws — the MICROCHIP SPECIAL poster on the wall (the clue); he walks in, the door bell jingles"""
    Z = 1.0
    x = lerp(440.0, 540.0, min(1.0, u / 1.1))
    return K.shot(VET, LH, 620.0, 330.0, Z, acts=[A(C.fm, x, 560.0, S_TV * Z, t=t, expr='zen', walk=t * 9, look=(1.0, 0.2), bump=True, shadow=0.3)],
                  sx=180, sy=320)


_CLIP = {}


def r_form(t, u):
    """insert: the new-patient form — he writes SPECIES: FLORIDA"""
    if 'b' not in _CLIP:
        im = Image.new('RGB', (OUT_W, OUT_H), (40, 150, 160)); d = ImageDraw.Draw(im); d.fontmode = '1'
        d.rectangle([110, 230, 970, 1760], fill=(150, 100, 56)); d.rectangle([110, 230, 970, 250], fill=(120, 80, 44))
        d.rectangle([170, 330, 910, 1700], fill=(252, 250, 240))
        d.rectangle([380, 190, 700, 330], fill=(190, 196, 206)); d.rectangle([420, 230, 660, 290], fill=(150, 156, 166))
        d.text((210, 380), 'DR. PAWS', font=O.pfont(60), fill=(226, 34, 52))
        d.text((210, 470), 'NEW PATIENT FORM', font=O.pfont(34), fill=(14, 44, 54))
        for i, lab in enumerate(['NAME:', 'SPECIES:', 'BREED:', 'GOOD BOY?']):
            y = 640 + i * 230
            d.text((210, y), lab, font=O.pfont(38), fill=(14, 44, 54))
            d.rectangle([210, y + 120, 870, y + 126], fill=(150, 150, 160))
        _CLIP['b'] = np.array(im)
        _CLIP['f'] = O.pfont(56)
    big = _CLIP['b'].copy()
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.text((230, 700), 'MAN', font=_CLIP['f'], fill=(40, 70, 200))
    word = 'FLORIDA'
    n = int(min(len(word), u / 0.55 * len(word)))
    d.text((230, 930), word[:n], font=_CLIP['f'], fill=(40, 70, 200))
    if u > 0.65: d.text((230, 1160), '?', font=_CLIP['f'], fill=(40, 70, 200))
    if u > 0.8: d.text((230, 1390), 'YES!!', font=_CLIP['f'], fill=(40, 70, 200))
    big = np.array(im)
    px = 230 + 62 * n
    big[880 + 40:880 + 60, px:px + 160] = (255, 206, 70); big[880 + 40:880 + 60, px:px + 14] = (40, 40, 40)   # the pen
    return big


def vet_sitters(v, t, expr='content', cone=False, mouth_=0.0, look=(0.6, 0.2), **kw):
    """Florida Man on a waiting chair and an iguana on the next one, both sitting proud in the same pose"""
    return [A(C.iguana, CHAIRS[1] + 10.0, SEAT + 2.0, S_SIT * 1.0 * v.Z, flip=True, t=t, look=(-1.0, 0.0)),
            A(C.fm, CHAIRS[0], V_FLOOR, S_SIT * v.Z, t=t, pose='sit', expr=expr, mouth_=mouth_, look=look, bump=True, cone=cone,
              hand_n=(13.0, 30.0), hand_f=(-6.0, 32.0), **kw)]


def r_waiting(t, u):
    """MS: the waiting room — FM and an iguana side by side; Tanner (job #4, vet teal scrubs) leans in, baby talk: «Who's a GOOD boy?»"""
    Z = 1.0
    v = view_at(VET, 560.0, 340.0, Z, 180, 320)
    acts = vet_sitters(v, t, look=(1.0, 0.3)) + [A(C.tanner, 690.0, 560.0, S_TV * Z, flip=True, t=t, uniform='vet', jobs=4, expr='cheer',
                                                    mouth_=mouth('tanner', t, 2.0), look=(-0.4, -0.6), hand_n=(12.0, 40.0), shadow=0.3)]
    return K.shot(VET, LH, 560.0, 340.0, Z, acts=acts, sx=180, sy=320)


def r_me(t, u):
    """CU: chest out, proud: «Me.»"""
    big, a, v = cu(VET, LH, C.fm, t, 480.0, 260.0, 26.0, (520, 820), Z=1.35, blur=6, expr='proud', mouth_=mouth('fm', t), look=(0.6, 0.3),
                   bump=True, pose='sit', hand_n=(13.0, 30.0), hand_f=(-6.0, 32.0))
    return big


def r_twist(t, u):
    """TWIST: click — the cone snaps on; Tanner, sweetly: «And a little MICROCHIP!» — the injector to the neck — BEEP"""
    Z = 1.15
    v = view_at(VET, 540.0, 330.0, Z, 180, 320)
    jab = t >= 17.75
    fm_ = vet_sitters(v, t, expr='shock' if jab else 'stunned', cone=True, look=(1.0, 0.0))
    tan = A(C.tanner, 600.0, 545.0, S_TV * Z, flip=True, t=t, uniform='vet', jobs=4, expr='cheer', mouth_=mouth('tanner', t, 2.0), look=(-0.2, -0.4),
            hand_n=(16.0, 52.0) if jab else (12.0, 44.0), prop_n=lambda sp, h: C.syringe(sp, h), shadow=0.3)
    def f(big, v_):
        if jab:
            hx, hy = aout(tan, v_, 'hand')
            beep_ring(big, hx - 30, hy, t, BEEPS[0])
    big = K.shot(VET, LH, 540.0, 330.0, Z, acts=fm_ + [tan], fx_=f, sx=180, sy=320)
    if u < 0.3 or 17.75 <= t < 17.95: B.shake(big, t, 10, 34)
    return big


_MAP = {}


def tablet_map(big, x0, y0, w, t, dot=True):
    """Darlene's patrol tablet: a green Florida on blue water, a blinking red dot + MAN, FLORIDA - LIVE"""
    h = int(w * 1.15)
    big[y0 - 24:y0 + h + 24, x0 - 24:x0 + w + 24] = (30, 32, 40)
    big[y0:y0 + h, x0:x0 + w] = (40, 110, 190)
    cell = w // 11
    ox, oy = x0 + cell, y0 + cell * 2
    for r, row in enumerate(C.FLORIDA):
        for q, ch in enumerate(row):
            if ch == 'X': big[oy + r * cell:oy + (r + 1) * cell, ox + q * cell:ox + (q + 1) * cell] = (90, 190, 90)
    if dot and int(t * 5) % 2 == 0:
        dx, dy = ox + int(6.4 * cell), oy + int(6.2 * cell)
        fx.glow(big, dx, dy, int(cell * 1.6), (255, 40, 40), 0.9)
        big[dy - cell // 3:dy + cell // 3, dx - cell // 3:dx + cell // 3] = (255, 60, 60)
    key = w
    if key not in _MAP:
        im = Image.new('RGBA', (w, cell * 2), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
        d.text((14, 14), 'MAN, FLORIDA - LIVE', font=O.pfont(max(14, w // 22)), fill=(255, 255, 255, 255))
        _MAP[key] = np.array(im)
    O.overlay(big, _MAP[key], x0, y0, 1.0)


def r_dar_map(t, u):
    """CU: Darlene in her cruiser, the patrol tablet: the dot blinks — a slow smile: «Gotcha.»"""
    big, a, v = cu(STORE, K.light_store, C.darlene, t, 640.0, 420.0, 21.0, (720, 760), Z=1.35, blur=8, flip=True, expr='sly',
                   mouth_=mouth('darlene', t), look=(-0.8, -0.6))
    big[:, :70] = (34, 36, 44); big[:110] = (34, 36, 44)          # the car window frame
    big[1640:] = (34, 36, 44)
    tablet_map(big, 80, 1000, 520, t)
    return big


def r_swamp(t, u):
    """montage 1: the mangroves — a cone sticks out of the leaves; BEEP; Darlene's airboat glides in"""
    Z = 1.25
    v = view_at(SWAMP, 330.0, 420.0, Z, 180, 320)
    fm_ = A(C.fm, 230.0, 590.0, 9.0 * Z, t=t, expr='nervous', cone=True, look=(1.0, 0.0), bump=True)
    bx = lerp(620.0, 410.0, sm(min(1.0, u / 0.8)))
    boat = A(C.airboat, bx, 676.0, 7.0 * Z, flip=True, t=t, spin=t * 40)
    dar = A(C.darlene, bx + 30.0, 676.0 - 7.0 * 7.0 / 3.0, 7.0 * Z, flip=True, t=t, expr='sly', look=(-1.0, 0.0))
    def f(big, v_):
        hx, hy = aout(fm_, v_, 'head')
        for i, (dx, dy, r) in enumerate(((-90, 150, 120), (60, 170, 130), (0, 290, 160), (-140, 300, 120), (120, 300, 110), (-30, 80, 70))):
            B.puff(big, hx + dx, hy + dy, r, 1.0, [(46, 110, 50), (70, 140, 60), (34, 90, 44)][i % 3])
        beep_ring(big, hx, hy + 60, t, BEEPS[1])
    return K.shot(SWAMP, K.light_sun, 330.0, 420.0, Z, acts=[fm_, dar, boat], fx_=f, sx=180, sy=320)


def r_booth(t, u):
    """montage 2: GATOR JERKY booth — he sells jerky in a cone and a fake moustache; BEEP; the cruiser skids in"""
    Z = 1.2
    def pre(big, v):
        bg0 = big.copy()
        A(C.fm, 640.0, 560.0, 13.0 * v.Z, t=t, expr='nervous', cone=True, stache=True, look=(0.2, 0.0), bump=True,
          hand_n=(12.0, 36.0))(big, v, K.light_sun(v))
        keep_box(big, bg0, v, BWIN)
    cx_ = lerp(1100.0, 760.0, sm(min(1.0, u / 0.45)))
    car = A(C.cruiser, cx_, 640.0, 9.0 * Z, flip=True, t=t, lights=True, shadow=0.3)
    def f(big, v_):
        x, y = v_.opt(650.0, 330.0)
        beep_ring(big, x, y, t, BEEPS[2])
    return K.shot(BOOTH, K.light_sun, 640.0, 380.0, Z, acts=[car], pre=pre, fx_=f, sx=180, sy=320)


def r_yard(t, u):
    """montage 3: home — crouched behind the dead A/C, the cone sticks up over it; BEEP; siren; Darlene walks in"""
    Z = 1.4
    v = view_at(YARD, 560.0, 470.0, Z, 180, 320)
    fm_ = A(C.fm, 560.0, SAND + 40.0, S_YARD * Z, t=t, expr='nervous', cone=True, look=(1.0, 0.0), bump=True)
    ac = A(C.ac_unit, AC[0] + 30.0, AC[1], S_AC * Z, t=t, dead=True, shadow=0.35)
    dx = lerp(760.0, 680.0, sm(min(1.0, u / 0.7)))
    dar = A(C.darlene, dx, SAND, S_YARD * Z, flip=True, t=t, expr='sly', walk=t * 8 if u < 0.7 else None, look=(-1.0, -0.3), shadow=0.3)
    def f(big, v_):
        hx, hy = aout(fm_, v_, 'head')
        beep_ring(big, hx, hy, t, BEEPS[3])
        K.heat_haze(big, t, 1300, OUT_H, 3)
    return K.shot(YARD, K.light_sun, 560.0, 470.0, Z, acts=[fm_, ac, dar], fx_=f, sx=180, sy=320)


def r_mornin(t, u):
    """CU: Darlene leans over the A/C: «Mornin'—» BEEP (the name)"""
    def fx_(big, v, a):
        beep_ring(big, 300, 1500, t, BEEPS[4])
    big, a, v = cu(YARD, K.light_sun, C.darlene, t, 640.0, 440.0, 22.0, (600, 820), Z=1.35, blur=6, flip=True, expr='bored',
                   mouth_=mouth('darlene', t), look=(-0.6, -0.4), fx_=fx_)
    return big


def r_mugshot(t, u):
    big = K.mug_wall()
    sc = 15.0
    sp = FX.draw(C.fm, sc, t=t, expr='proud', look=(0.0, 0.0), shaka=True, cone=True, bump=True)
    px, py = sp.anchors['head']
    blit(big, sp, 540 - px * sc, 720 + py * sc, sc, None)
    K.booking_board(big, 540, 1330, ['MAN, FLORIDA J.', 'SPECIES: FLORIDA', 'CHIPPED. GOOD BOY.'], w=800)
    fx.vignette(big, 0.25)
    return big


_SCR = {}


def r_scan(t, u):
    """MS yard: Darlene waves the pet scanner over his neck — BEEP — SHOTS: UP TO DATE, a receipt crawls out"""
    Z = 1.55
    fm_ = A(C.fm, 640.0, SAND, S_YARD * Z, t=t, expr='content', cone=True, bump=True, look=(1.0, 0.2), shadow=0.3)
    dar = A(C.darlene, 705.0, SAND, S_YARD * Z, flip=True, t=t, expr='bored', look=(-1.0, -0.2), hand_n=(12.0, 50.0),
            prop_n=lambda sp, h: C.pet_scanner(sp, h), shadow=0.3)
    def f(big, v_):
        hx, hy = aout(dar, v_, 'hand')
        beep_ring(big, hx - 40, hy, t, BEEPS[5])
        if t >= BEEPS[5]:
            if 'o' not in _SCR:
                im = Image.new('RGBA', (560, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
                d.rectangle([0, 0, 559, 149], fill=(30, 52, 40, 255), outline=(150, 156, 166, 255), width=8)
                d.text((24, 26), 'CHIP: MAN, FLORIDA', font=O.pfont(26), fill=(140, 255, 160, 255))
                d.text((24, 84), 'SHOTS: UP TO DATE', font=O.pfont(26), fill=(140, 255, 160, 255))
                _SCR['o'] = np.array(im)
            O.overlay(big, _SCR['o'], 260, 300, 1.0)
            L = int(min(1.0, (t - BEEPS[5] - 0.15) / 1.2) * 700) if t > BEEPS[5] + 0.15 else 0
            receipt(big, int(hx) - 50, int(hy) + 40, int(hy) + 40 + L, t, w=90)
    return K.shot(YARD, K.light_sun, 680.0, 470.0, Z, acts=[fm_, dar], fx_=f, sx=180, sy=320)


def r_button(t, u):
    """button: two-shot CU — Darlene pats the coned head, flat: «Good boy. Scan's two GRAND.»"""
    Z = 1.6
    pat = 0.6 * math.sin(t * 9.0) if t > 28.2 else 0.0
    fm_ = A(C.fm, 640.0, SAND, S_YARD * 1.4 * Z, t=t, expr='bliss', cone=True, bump=True, look=(1.0, 0.4), shadow=0.3)
    dar = A(C.darlene, 712.0, SAND, S_YARD * 1.4 * Z, flip=True, t=t, expr='bored', mouth_=mouth('darlene', t), look=(-0.6, -0.5),
            hand_n=(16.5, 54.0 + pat), shadow=0.3)
    return K.shot(YARD, K.light_sun, 645.0, 420.0, Z, acts=[fm_, dar], sx=180, sy=320)


SHOTS = [r_hook, r_tanner_glass, r_fm_water, r_tanner_cu, r_mort_hold, r_mort_bill, r_vet_in, r_form, r_waiting, r_me, r_twist, r_dar_map,
         r_swamp, r_booth, r_yard, r_mornin, r_mugshot, r_scan, r_button]
NAMES = ['hook', 'tanner_glass', 'fm_water', 'tanner_cu', 'mort_hold', 'mort_bill', 'vet_in', 'form', 'waiting', 'me', 'twist', 'dar_map',
         'swamp', 'booth', 'yard', 'mornin', 'mugshot', 'scan', 'button']
CAP = dict(hook=1780, tanner_glass=1800, fm_water=1640, tanner_cu=1640, mort_hold=1800, mort_bill=1700, waiting=1800, me=1640, twist=1800,
           dar_map=1780, mornin=1640, scan=1800, button=1800)


SHOW = K.Show(EPI, 3, ['$2,000', 'ICE PACK?!'], hook_t=(0.10, 2.6), hook_y=150, cap_default=1640, cap_y=CAP, hook_size=84,
              stickers=[(K.st('JOB #3', (170, 255, 110), 52), 2.8, 4.15, 260, 420),
                        (K.st('ICE: $2,000', (120, 230, 255), 52), 3.1, 4.15, 760, 540),
                        (K.st('$80', (120, 230, 255), 70), 10.5, 11.45, 780, 520),
                        (K.st('JOB #4', (170, 255, 110), 52), 13.75, 15.45, 820, 420),
                        (K.st('CHIPPED', (255, 90, 90), 70), 17.95, 18.28, 760, 300),
                        (K.st('BEEP!', (255, 90, 90), 64), 19.85, 20.45, 760, 420),
                        (K.st('BEEP!', (255, 90, 90), 64), 20.85, 21.45, 300, 420),
                        (K.st('BEEP!', (255, 90, 90), 64), 21.85, 22.45, 760, 420),
                        (K.st('*BEEP*', (255, 255, 255), 64), 23.18, 23.5, 540, 330)],
              chyrons=[(23.55, 25.5, 'FLORIDA MAN SEES VET,', 'NOW ON A LEASH', 1500)],
              cards=[(24.4, 25.5, 7, 24.7, 540, 370)],
              flashes=[16.75, 17.95, 23.5], mosaics=[11.5])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
