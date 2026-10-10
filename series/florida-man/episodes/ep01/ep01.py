"""S01E01 «Frozen Foods» (09.10.2026) — the A/C dies at 104°F: «NINE GRAND?! For the A/C?!» Tanner (job #1, Cool-Rite): «Compressor's
DEAD! Three-week WAIT!» — «I'll be dead in three WEEKS.» — «No worries! Want the extended WARRANTY?» Zen returns: «Mort. Hold my sub.»
The pelican lawyer swallows it: «What sub?» Florida Man pushes his recliner into Pubbix: «Ohhh. Sixty-EIGHT.» TWIST (54 %): in the
next freezer sits the A/C guy himself: «Mine broke TOO! Three WEEKS!» — the whole aisle is living there. Deputy Darlene: «Sir. You can't
LIVE in Frozen Foods.» — «I'm not living, ma'am. I'm BROWSING.» Mugshot, BREAKING chyron, FREQUENT GUEST 5/10. In the cell the vent
dies with the same rattle: «Broke. Nine GRAND.» Loop: the first frame «NINE GRAND?!».
Heroes: props/fmcast.py in the «Tabloid Sun» manner (props/fmpix.py); kit: props/fmkit.py.
  python3 ep01.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import stage as ST
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
from timeline import DUR, FPS, VOICE, SLUG, CUTS

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
YARD = K.world_baked('yard')
STORE = K.world_baked('store')
AISLE = K.world_baked('aisle')
CELL = K.world('cell')
A, wpt, aout, put = K.A, K.wpt, K.aout, K.put
SAND = 626.0                       # yard: feet on the sand
CHAIR = (806.0, 476.0)             # top of the plastic lawn chair's backrest (Mort's perch)
AC = (520.0, 612.0)                # the dead condenser
WALK = 560.0                       # store sidewalk
FLOOR = 650.0                      # aisle floor (feet)
DOOR_X = (640.0, 777.0)            # the freezer door to Florida Man's right (world x range)
# people scale per world (output px per sprite px = k * Z): matched to the props of each background (rule 09.10.2026)
S_YARD, S_STORE, S_AISLE, S_CELL = 10.0, 5.6, 11.6, 15.0
S_AC, S_MORT = 13.8, 7.0           # the condenser (0.9 m) and the perched pelican (0.65 m) in the yard


def mouth(who, t, k=1.8):
    return min(1.0, talk(who, t) * k)


def cu(world, light, fn, t, cx, cy, sc, head, Z=1.4, flip=False, blur=0, pre_=None, fx_=None, pin='head', extra=(), **kw):
    """close-up: the sprite anchor `pin` sits at output point `head`; the background is zoomed only Z (<= ~1.45), optionally soft"""
    kw.setdefault('t', t)
    v0 = view_at(world, cx, cy, Z, 180, 320)
    hx, hy = wpt(v0, *head)
    a = A(fn, hx, hy, sc, flip=flip, pin=pin, **kw)
    def pre(big, v):
        if pre_: pre_(big, v)
        if blur: big[:] = K.dof(big, blur)
    big = K.shot(world, light, cx, cy, Z, acts=list(extra) + [a], pre=pre, fx_=(lambda b, v: fx_(b, v, a)) if fx_ else None, sx=180, sy=320)
    return big, a


def ac_actor(v, t, dead=True):
    return A(C.ac_unit, AC[0], AC[1], S_AC * v.Z, t=t, dead=dead, fan=0.0 if dead else t * 20, shadow=0.35)


def ac_smoke(big, v, t, k=1.0):
    x, y = v.opt(AC[0] + 10.0, AC[1] - 24.0 * S_AC / 3.0)
    K.smoke(big, x, y, t, n=6, rise=380 * k, size=56 * k, a=0.5)


# ================================================================== shots
def r_hook(t, u):
    """XCU: sweat pours, the shield glasses slide down, «NINE GRAND?!»; the dead condenser smokes behind; the invoice up front"""
    def pre(big, v):
        ac_actor(v, t)(big, v, K.light_sun(v))
        ac_smoke(big, v, t)
        K.heat_haze(big, t, 0, OUT_H, 5)
    big, a = cu(YARD, K.light_sun, C.fm, t, 600.0, 450.0, 30.0, (540, 820), Z=1.35, blur=6, pre_=pre, expr='shriek',
                mouth_=mouth('fm', t), sweat=1.0, glasses_drop=min(1.0, 0.3 + u / 0.8), look=(0.0, 0.2))
    K.invoice_card(big, 450, 1290, 580, ang=7.0)
    if u < 0.5: B.shake(big, t, 9, 33)
    return big


def r_tanner_ac(t, u):
    """MS: Tanner (job #1, Cool-Rite) beside the smoking condenser, tablet up, beaming — and sweating himself (clue)"""
    Z = 1.45
    v = view_at(YARD, 560.0, 470.0, Z, 180, 320)
    acts = [ac_actor(v, t),
            A(C.tanner, 618.0, SAND, S_YARD * Z, t=t, expr='chipper', mouth_=mouth('tanner', t, 2.0), look=(0.0, 0.0), jobs=1, sweat=1.0,
              prop_n=lambda sp, h: C.tablet(sp, (h[0] + 0.5, h[1] - 0.5)), hand_n=(10.0, 40.0), shadow=0.35)]
    def f(big, v_):
        ac_smoke(big, v_, t)
        K.heat_haze(big, t, 1150, OUT_H, 3)
    return K.shot(YARD, K.light_sun, 560.0, 470.0, Z, acts=acts, fx_=f, sx=180, sy=320)


def r_melt(t, u):
    """CU: Florida Man wilting in the heat, slowly sinking, sweat dripping"""
    sink = 70.0 * sm(min(1.0, u / 2.6))
    def pre(big, v):
        K.heat_haze(big, t, 0, OUT_H, 8, speed=4.0)
    big, a = cu(YARD, K.light_sun, C.fm, t, 380.0, 440.0, 25.0, (540, 760 + sink), Z=1.35, blur=5, pre_=pre, expr='weak',
                mouth_=mouth('fm', t), sweat=1.0, glasses_drop=0.6, look=(0.2, -0.4), sway=-0.3)
    return big


def r_tanner_cu(t, u):
    """CU: Tanner, thumbs up, megawatt grin: «No worries! Want the extended WARRANTY?»"""
    def pre(big, v):
        ac_actor(v, t)(big, v, K.light_sun(v)); ac_smoke(big, v, t, 0.8)
    big, a = cu(YARD, K.light_sun, C.tanner, t, 560.0, 460.0, 23.0, (540, 700), Z=1.35, blur=6, pre_=pre, expr='chipper',
                mouth_=mouth('tanner', t, 2.0), look=(0.0, 0.0), jobs=1, sweat=1.0, thumbs=u > 0.35, hand_n=(11.0, 50.0) if u > 0.35 else None,
                prop_f=lambda sp, h: C.tablet(sp, (h[0] - 4.0, h[1])))
    return big


def r_porch(t, u):
    """MS: zen again — Florida Man holds the sub up to Mort perched on the lawn-chair back; the billboard behind; GULP at 12.95"""
    Z = 1.4
    v = view_at(YARD, 770.0, 420.0, Z, 180, 320)
    gone = t >= 12.95
    gul = min(1.0, max(0.0, (t - 12.95) / 0.3))
    fm_ = A(C.fm, 742.0, SAND, S_YARD * Z, t=t, expr='zen', mouth_=mouth('fm', t), look=(0.8, 0.5),
            hand_n=(15.0, 48.0), prop_n=None if gone else (lambda sp, h: C.sub(sp, (h[0] + 1.0, h[1] + 1.0), ang=0.2)), shadow=0.35)
    mort = A(C.mort, CHAIR[0], CHAIR[1], S_MORT * Z, flip=True, t=t, expr='deadpan' if not gone else 'smug', mouth_=mouth('mort', t),
             look=(1.0, -0.4), lump='sub' if gone else None, gulp=gul if gone else 0.0, lift=0.5 * (1 - gul) if t > 12.5 else 0.0)
    def f(big, v_):
        K.heat_haze(big, t, 1300, OUT_H, 3)
    return K.shot(YARD, K.light_sun, 770.0, 420.0, Z, acts=[mort, fm_], fx_=f, sx=180, sy=320)


def r_mort_cu(t, u):
    """CU: Mort to camera, the sub shape bulging in his pouch: «What sub?»"""
    big, a = cu(YARD, K.light_sun, C.mort, t, 900.0, 300.0, 26.0, (560, 760), Z=1.4, blur=7, flip=True, expr='deadpan',
                mouth_=mouth('mort', t), look=(-0.2, -0.1), lump='sub', lift=0.25)
    return big


def r_doors(t, u):
    """the Pubbix entrance: he pushes the recliner on a hand truck through the sliding doors — a blast of cold air, the braid flies back"""
    Z = 1.75
    x = lerp(470.0, 600.0, min(1.0, u / 1.7))
    cx = x + 60.0
    v = view_at(STORE, cx, 446.0, Z, 180, 320)                  # sign band fully out of frame (no cut-off letters on top)
    s_ = S_STORE * Z
    un = s_ / (3 * Z)                                            # world px per sprite px
    dolly = A(C.hand_truck, x + 14.0 * un, WALK, s_, t=t, spin=-t * 8)
    chair = A(C.recliner, x + 18.0 * un, WALK - 5.0 * un, s_, t=t, foot=0.0, rot=-14.0, pivot=(0.0, 0.0))
    fm_ = A(C.fm, x - 6.0 * un, WALK, s_, t=t, expr='bliss', mouth_=mouth('fm', t), walk=t * 9, hand_n=(18.0, 41.0),
            hand_f=(16.0, 42.0), sway=-1.0, rot=-6.0, pivot=(0.0, 0.0), shadow=0.3)
    def f(big, v_):
        K.heat_haze(big, t, 1450, OUT_H, 4)
        if t >= 14.4: K.cold_blast(big, t, min(1.0, (t - 14.4) / 0.3), dirn=-1)
    return K.shot(STORE, K.light_store, cx, 446.0, Z, acts=[dolly, chair, fm_], fx_=f, sx=180, sy=320)


def freezer_door(big, v, x0, x1, y0, y1, ang, frost=0.6):
    """an opened glass freezer door hinged at x1 (world), swung towards the viewer: a narrowing frosty glass panel + chrome frame"""
    ax0, ay0 = v.opt(x0, y0); ax1, ay1 = v.opt(x1, y1)
    w = (ax1 - ax0) * math.cos(ang)
    X0 = int(ax1 - w); X1 = int(ax1)
    Y0, Y1 = int(ay0), int(ay1)
    if X1 - X0 < 4: return
    reg = big[max(0, Y0 - 20):min(OUT_H, Y1 + 20), max(0, X0):min(OUT_W, X1)]
    reg[:] = (reg * 0.45 + np.array((220, 240, 255)) * 0.55).astype(np.uint8)
    big[max(0, Y0 - 20):min(OUT_H, Y1 + 20), max(0, X0):max(0, X0) + 14] = (200, 210, 220)
    big[max(0, Y0 - 20):min(OUT_H, Y1 + 20), max(0, X1 - 14):X1] = (200, 210, 220)
    big[max(0, Y0 - 20):max(0, Y0 - 6), max(0, X0):X1] = (200, 210, 220)
    big[min(OUT_H - 1, Y1 + 6):min(OUT_H, Y1 + 20), max(0, X0):X1] = (200, 210, 220)


def cold_mist(big, v, x, y, t, n=6):
    ox, oy = v.opt(x, y)
    for i in range(n):
        ph = (t * 0.7 + i / n) % 1.0
        B.puff(big, ox - 40 + 160 * ph * math.sin(i * 1.7), oy + 140 * ph, 40 + 60 * ph, 0.35 * (1 - ph), (236, 248, 255))


def r_aisle_set(t, u):
    """the freezer aisle: recliner parked at the open freezers, feet up, TV on, frost creeping; an iguana on top of the freezers goes
    rigid from the cold and drops — THUD"""
    Z = 1.45
    v = view_at(AISLE, 560.0, 470.0, Z, 180, 320)
    s_ = S_AISLE * Z
    un = s_ / (3 * Z)
    fr = 0.25 + 0.35 * u / 1.7
    acts = [A(C.tv_cart, 446.0, FLOOR, s_, t=t),
            A(C.recliner, 548.0, FLOOR, s_, t=t, foot=1.0),
            A(C.fm, 549.0, FLOOR, s_, t=t, pose='sit', expr='bliss', mouth_=mouth('fm', t), frost=fr, hand_n=(14.0, 32.0),
              hand_f=(-8.0, 36.0), look=(0.6, 0.6))]
    fall = (t - 16.9) / 0.3
    if t < 16.9: acts.append(A(C.iguana, 650.0, 206.0, s_ * 0.8, t=t, stiff=t > 16.7))
    else:
        yy = lerp(206.0, FLOOR - 3.0, min(1.0, fall))
        acts.append(A(C.iguana, 650.0 + 20 * min(1.0, fall), yy, s_ * 0.8, t=t, stiff=True, rot=-90.0 * min(1.0, fall)))
    def pre(big, v_):
        freezer_door(big, v_, 502.0, 640.0, 230.0, 500.0, 1.15)
    def f(big, v_):
        cold_mist(big, v_, 560.0, 420.0, t)
        if 16.9 <= t < 17.25:
            x, y = v_.opt(670.0, FLOOR)
            for i in range(6): B.puff(big, x + (i - 3) * 30, y - 10, 30, 0.4, (240, 240, 244))
    big = K.shot(AISLE, K.light_aisle, 560.0, 470.0, Z, acts=acts, pre=pre, fx_=f, sx=180, sy=320)
    if 16.9 <= t < 17.1: B.shake(big, t, 8, 30)
    return big


def freezer_insert(t, u, sc, head, expr, open_k=1.0, shiver=1.0, zoom=1.0):
    """the next freezer, wide open: Tanner (A/C uniform, frost on his frosted tips) huddled among frozen pizzas, shivering, still grinning"""
    v = view_at(AISLE, 700.0, 380.0, 2.2 * zoom, 180, 320)
    big = K.dof(v.bg(), 7)
    x0, y0, x1, y1 = 110, 260, 970, 1700                       # the freezer interior on screen
    big[y0 - 30:y1 + 30, x0 - 30:x1 + 30] = (190, 200, 214)    # chrome frame
    big[y0:y1, x0:x1] = (150, 196, 230)
    g = np.linspace(0, 1, y1 - y0)[:, None, None]
    big[y0:y1, x0:x1] = (big[y0:y1, x0:x1] * (0.75 + 0.25 * g)).astype(np.uint8)
    rng = np.random.default_rng(3)
    for row, yy in enumerate((520, 980, 1440)):                # shelves of pizza boxes
        big[yy:yy + 22, x0:x1] = (210, 220, 232)
        for q in range(7):
            bx = x0 + 10 + q * 122; c = [(226, 60, 50), (255, 190, 60), (60, 160, 90), (230, 120, 40)][(q + row) % 4]
            big[yy - 150:yy - 6, bx:bx + 112] = c
            big[yy - 140:yy - 100, bx + 10:bx + 102] = (255, 250, 236)
            big[yy - 90:yy - 40, bx + 30:bx + 82] = (250, 210, 120)
    v2 = view_at(AISLE, 700.0, 380.0, 2.2, 180, 320)
    sp = FX.draw(C.tanner, sc, t=t, expr=expr, mouth_=mouth('tanner', t, 2.0), look=(0.0, 0.0), jobs=1, frost=1.0, shiver=shiver,
                 hand_n=(9.0, 46.0), hand_f=(-4.0, 46.0))
    px, py = sp.anchors['head']
    blit(big, sp, head[0] - px * sc, head[1] + py * sc, sc, K.light_aisle(v2))
    big[y1 - 40:y1 + 30, x0 - 30:x1 + 30] = (190, 200, 214)    # front lip hides his legs
    big[y1 + 30:] = (big[y1 + 30:] * 0.6).astype(np.uint8)
    if open_k < 1.0:                                           # the glass door still swinging open
        w = int((x1 - x0) * (1 - open_k))
        reg = big[y0 - 30:y1 + 30, x0 - 30:x0 - 30 + w]
        reg[:] = (reg * 0.4 + np.array((224, 240, 255)) * 0.6).astype(np.uint8)
    K.frost_edges(big, 0.8)
    for i in range(10):                                        # cold vapour pouring out
        ph = (t * 0.8 + i / 10) % 1.0
        B.puff(big, 120 + i * 90, 1750 + 120 * ph, 50 + 40 * ph, 0.35 * (1 - ph), (240, 250, 255))
    return big


def r_twist(t, u):
    big = freezer_insert(t, u, 20.0, (560, 860), 'shiver', open_k=min(1.0, u / 0.25))
    if u < 0.4: B.shake(big, t, 10, 35)
    return big


def r_shiver(t, u):
    big = freezer_insert(t, u, 27.0, (540, 900), 'shiver', zoom=1.1)
    return big


LOC = [('retiree', 'sit', 448.0), ('tank', 'stand', 690.0), ('grandpa', 'pool', 720.0), ('curlers', 'sit', 395.0)]


def r_reveal(t, u):
    """pull back: the whole freezer aisle is a campsite — lawn chairs, a kiddie pool of ice, folks in curlers; Tanner in his freezer"""
    k_ = sm(min(1.0, u / 0.5))
    Z = lerp(2.2, 1.05, k_)
    CX = lerp(560.0, 575.0, k_)
    CY = lerp(450.0, 420.0, k_)                                  # end framing: the hanging sign just above the frame (no cut letters)
    v = view_at(AISLE, CX, CY, Z, 180, 320)
    s_ = S_AISLE * Z
    acts = []
    for kind, pose, x in LOC:
        if pose != 'pool': acts.append(A(C.local, x, FLOOR - 6.0, s_, t=t, kind=kind, pose=pose, frost=0.5, flip=x > 560,
                                         expr='content' if pose != 'stand' else 'normal'))
    acts += [A(C.recliner, 548.0, FLOOR, s_, t=t, foot=1.0),
             A(C.fm, 549.0, FLOOR, s_, t=t, pose='sit', expr='content', frost=0.6, hand_n=(14.0, 32.0), hand_f=(-8.0, 36.0))]
    for kind, pose, x in LOC:
        if pose == 'pool': acts.append(A(C.local, x, FLOOR + 10.0, s_, t=t, kind=kind, pose=pose, frost=0.5, flip=True, expr='content'))
    def pre(big, v_):
        freezer_door(big, v_, 502.0, 640.0, 230.0, 500.0, 1.15)
        freezer_door(big, v_, *DOOR_X, 230.0, 500.0, 1.25)
        x, y = v_.opt(708.0, 470.0)                              # Tanner huddled in his freezer
        sp = FX.draw(C.tanner, s_ * 0.9, t=t, expr='shiver', jobs=1, frost=1.0, shiver=1.0)
        blit(big, sp, x, y, s_ * 0.9, K.light_aisle(v_))
    def f(big, v_):
        cold_mist(big, v_, 560.0, 440.0, t)
    return K.shot(AISLE, K.light_aisle, CX, CY, Z, acts=acts, pre=pre, fx_=f, sx=180, sy=320)


def r_darlene_in(t, u):
    """MS: Deputy Darlene walks in from the right with a basket (ice cream), stops by the recliner"""
    Z = 1.45
    v = view_at(AISLE, 590.0, 470.0, Z, 180, 320)
    s_ = S_AISLE * Z
    dx = lerp(800.0, 690.0, sm(min(1.0, u / 0.8)))
    acts = [A(C.recliner, 548.0, FLOOR, s_, t=t, foot=1.0),
            A(C.fm, 549.0, FLOOR, s_, t=t, pose='sit', expr='zen', frost=0.75, look=(0.8, 0.4), hand_n=(14.0, 32.0), hand_f=(-8.0, 36.0)),
            A(C.darlene, dx, FLOOR + 4, s_, flip=True, t=t, expr='bored', mouth_=mouth('darlene', t), walk=t * 8 if u < 0.8 else None,
              prop_n=lambda sp, h: C.basket(sp, h), look=(1.0, -0.3), shadow=0.3, gum=max(0.0, min(1.0, (t - 23.6) / 0.8)) if t < 24.42 else 0.0)]
    def pre(big, v_):
        freezer_door(big, v_, 502.0, 640.0, 230.0, 500.0, 1.15)
    def f(big, v_):
        cold_mist(big, v_, 560.0, 440.0, t)
    return K.shot(AISLE, K.light_aisle, 590.0, 470.0, Z, acts=acts, pre=pre, fx_=f, sx=180, sy=320)


def r_darlene_cu(t, u):
    """CU: Darlene, deadpan, chewing; the gum bubble from the previous shot just popped"""
    big, a = cu(AISLE, K.light_aisle, C.darlene, t, 820.0, 400.0, 22.0, (560, 860), Z=1.4, blur=7, flip=True, expr='bored',
                mouth_=mouth('darlene', t), look=(1.0, -0.2))
    return big


def r_browse(t, u):
    """CU: Florida Man frosted solid in the recliner, icicles on the braid, perfectly zen: «I'm BROWSING.»"""
    def pre(big, v):
        freezer_door(big, v, 502.0, 640.0, 230.0, 500.0, 1.15)
    big, a = cu(AISLE, K.light_aisle, C.fm, t, 560.0, 420.0, 25.0, (520, 760), Z=1.4, blur=6, pre_=pre, expr='zen', mouth_=mouth('fm', t),
                frost=1.0, look=(0.5, 0.0), pose='sit')
    K.frost_edges(big, 0.7)
    return big


def r_mugshot(t, u):
    """FLASH: booking photo against the height chart — serene, shaka, icicles; the BREAKING chyron + FREQUENT GUEST 5/10 (overlays)"""
    big = K.mug_wall()
    sc = 15.0
    sp = FX.draw(C.fm, sc, t=t, expr='proud', frost=0.5, look=(0.0, 0.0), shaka=True)
    px, py = sp.anchors['head']
    blit(big, sp, 540 - px * sc, 720 + py * sc, sc, None)
    K.booking_board(big, 540, 1330, ['MAN, FLORIDA J.', 'DOB: YES', 'LIVING IN FROZEN FOODS'], w=800)
    fx.vignette(big, 0.25)
    return big


BUNK = (430.0, 470.0)              # feet end of the lower bunk mattress (world)


def bunk_fm(t, Z, expr='bliss'):
    s_ = S_CELL * Z
    un = s_ / (3 * Z)
    return A(C.fm, BUNK[0], BUNK[1] - 9.0 * un, s_, t=t, expr=expr, rot=90.0, pivot=(0.0, 0.0), look=(-0.6, 0.6), frost=0.2, shadow=0.0)


def r_cell(t, u):
    """the cell door clangs; he flops onto the bunk, blissful — jail has A/C"""
    Z = 1.0
    v = view_at(CELL, 250.0, 360.0, Z, 180, 320)
    big = K.shot(CELL, K.light_cell, 250.0, 360.0, Z, acts=[bunk_fm(t, Z)], sx=180, sy=320)
    if u < 0.2: B.shake(big, t, 6, 30)
    return big


def r_vent(t, u):
    """insert: the A/C vent with ribbons streaming… it rattles and dies (30.42): ribbons drop, a puff of smoke"""
    Z = 2.0
    v = view_at(CELL, 1025.0, 150.0, Z, 180, 320)
    big = v.bg()
    dead = t >= 30.45
    x0, y0 = v.opt(965.0, 170.0)
    for i in range(6):
        L = 420 if not dead else 120
        for q in range(14):
            yy = int(y0 + q * L / 14); xx = int(x0 + 20 + i * 60 + (0 if dead else 34 * math.sin(t * 22 + q * 0.6 + i)))
            if 0 <= xx < OUT_W - 18 and 0 <= yy < OUT_H - 30: big[yy:yy + 30, xx:xx + 18] = [(255, 86, 160), (40, 196, 196)][i % 2]
    if dead: K.smoke(big, x0 + 220, y0 - 40, t, n=5, rise=300, size=60, a=0.55, seed=2)
    if 30.42 <= t < 30.7: B.shake(big, t, 10, 30)
    fx.vignette(big, 0.3)
    return big


def r_button(t, u):
    """button: Darlene through the bars, flat, to camera: «Broke. Nine GRAND.»; Florida Man on the bunk behind her"""
    def pre(big, v):
        bunk_fm(t, v.Z, 'shock')(big, v, K.light_cell(v))
    big, a = cu(CELL, K.light_cell, C.darlene, t, 330.0, 330.0, 22.0, (560, 880), Z=1.0, blur=4, pre_=pre, expr='bored',
                mouth_=mouth('darlene', t), look=(0.0, 0.0))
    for x in (60, 300, 840, 1060):                              # cell bars in the foreground
        big[:, max(0, x - 34):x + 34] = (60, 70, 76); big[:, max(0, x - 34):max(0, x - 22)] = (120, 134, 140)
        big[:, x + 22:x + 34] = (30, 36, 40)
    big[1560:1620] = (60, 70, 76); big[1560:1572] = (120, 134, 140)
    return big


SHOTS = [r_hook, r_tanner_ac, r_melt, r_tanner_cu, r_porch, r_mort_cu, r_doors, r_aisle_set, r_twist, r_shiver, r_reveal, r_darlene_in,
         r_darlene_cu, r_browse, r_mugshot, r_cell, r_vent, r_button]
NAMES = ['hook', 'tanner_ac', 'melt', 'tanner_cu', 'porch', 'mort_cu', 'doors', 'aisle_set', 'twist', 'shiver', 'reveal', 'darlene_in',
         'darlene_cu', 'browse', 'mugshot', 'cell', 'vent', 'button']
CAP = dict(hook=1800, melt=1640, tanner_cu=1640, mort_cu=1640, twist=1820, shiver=1820, darlene_cu=1640, browse=1640, button=1720,
           porch=1780, tanner_ac=1820, darlene_in=1800, aisle_set=1820, doors=1820)


def extra(big, t, shot_):
    if shot_ == 'darlene_in' and 23.7 <= t < 24.45:                # gum bubble grows over her lines… pops at the cut
        pass


SHOW = K.Show(EPI, 1, ['NINE GRAND?!'], hook_t=(0.10, 2.55), hook_y=150, cap_default=1640, cap_y=CAP, hook_size=84,
              stickers=[(K.st('104°F', (255, 120, 90), 70), 0.35, 2.55, 840, 560),
                        (K.st('JOB #1', (170, 255, 110), 52), 2.75, 4.9, 300, 420),
                        (K.st('68°F', (120, 230, 255), 70), 16.3, 17.75, 760, 420),
                        (K.st('HIS TOO?!', (255, 236, 96), 70), 17.95, 19.7, 540, 380),
                        (K.st('AISLE 9: FULL', (120, 230, 255), 52), 21.95, 22.65, 540, 330)],
              chyrons=[(28.85, 31.0, 'FLORIDA MAN MOVES INTO', 'FREEZER AISLE', 1500)],
              cards=[(28.95, 29.85, 5, 29.25, 540, 370)],
              flashes=[17.82, 28.80], mosaics=[29.85], extra=extra)


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
