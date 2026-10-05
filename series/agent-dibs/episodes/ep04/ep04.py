"""S01E04 «Hostage» (v2 cast) — a standoff at Sal's: Terry holds a ketchup bottle over a Chicago dog («seven toppings, son»). The whole block holds its breath.
He only wanted ketchup for his fries. Dibs eats the hostage as evidence. Marty: «I had dibs.»
  python3 ep04.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import paths as P
import stage as ST
from stage import Chars, view_at, OUT_W, OUT_H
from scene import sm, lerp, Layer
import overlays as O
import fx
from episode import Episode
from props import dibspix as DX
from props import dibscast as DC
from props import dibskit as DK
from props import chi_props as PR
from props import chikit as K
from props import bytfx as B
from props.folk import H, cap, ell, dot, poly, outline, OL
from props.us_props import rect, ltext
from timeline import DUR, FPS, VOICE, SLUG, TURN_T, BITE_T

EPI = Episode('ep04', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
WORLD = K.world('sals_stand')
GY = 556.0                                  # sidewalk line in front of the stand
LEDGE_Y = 455.0                             # the service window ledge (the hot dog sits here)
DOG_X, FRY_X = 548.0, 600.0
TERRY_X = 470.0
PU = 8.6                                    # person unit at the stand front


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def chew(t):
    return 0.12 + 0.34 * (0.5 + 0.5 * math.sin(t * 16))


# ================================================================== world text + stand dressing
def world_text(big, v, text, cx, cy, h, col, glow=0.0, outline_=None):
    """pixel-font text at world coordinates (cx, cy centre, h = text height in world px)"""
    s_ = v.Z * 3.0
    size = max(8, int(h * s_))
    ox, oy = v.opt(cx, cy)
    x0 = max(0, int(ox - len(text) * size * 0.62)); x1 = min(OUT_W, int(ox + len(text) * size * 0.62))
    y0 = max(0, int(oy) - size); y1 = min(OUT_H, int(oy) + size)
    if x1 - x0 < 4 or y1 - y0 < 4: return
    img = Image.fromarray(big[y0:y1, x0:x1])
    d = ImageDraw.Draw(img); d.fontmode = '1'
    f = O.pfont(size)
    xy = (ox - x0, oy - y0)
    if glow > 0:
        for dx in (-3, 0, 3):
            for dy in (-3, 0, 3):
                d.text((xy[0] + dx, xy[1] + dy), text, font=f, fill=tuple(int(c * glow) for c in col), anchor='mm')
    if outline_:
        for dx in (-2, 0, 2):
            for dy in (-2, 0, 2): d.text((xy[0] + dx, xy[1] + dy), text, font=f, fill=outline_, anchor='mm')
    d.text(xy, text, font=f, fill=col, anchor='mm')
    big[y0:y1, x0:x1] = np.array(img)


def stand_pre(t, extra=None):
    def pre(big, v):
        world_text(big, v, "SAL'S", 570, 193, 34, (255, 168, 70), glow=0.45)
        ox, oy = v.opt(265, 360); s = v.Z * 3.0                                        # cardboard sign on the wall
        x0, y0, x1, y1 = int(ox - 55 * s), int(oy - 42 * s), int(ox + 55 * s), int(oy + 42 * s)
        if x1 > 0 and x0 < OUT_W and y1 > 0 and y0 < OUT_H:
            big[max(0, y0 - 4):y1 + 4, max(0, x0 - 4):x1 + 4] = (40, 30, 24)
            big[max(0, y0):y1, max(0, x0):x1] = (240, 232, 210)
            world_text(big, v, 'NO', 265, 335, 15, (200, 30, 40))
            world_text(big, v, 'KETCHUP.', 265, 357, 11, (200, 30, 40))
            world_text(big, v, "WE'RE NOT", 265, 378, 7, (60, 40, 30))
            world_text(big, v, 'SORRY.', 265, 390, 7, (60, 40, 30))
        if extra: extra(big, v)
    return pre


def stand_shot(t, cx, acts=(), back=(), front=(), pre_extra=None, emit=None, fx_=None, Z=1.0, cy=400.0, sy=320, snow=True, dof=0):
    """dof = blur radius (output px) of the background only: inserts where the stand cannot be pushed back (hero / food at the same depth)
    get a soft out-of-focus backdrop instead of zoomed pixel mush; heroes and props stay sharp"""
    pre0 = stand_pre(t, pre_extra)
    def pre(big, v):
        pre0(big, v)
        if dof: big[:] = np.array(Image.fromarray(big).filter(ImageFilter.GaussianBlur(dof)))
    def fx2(big, v):
        if snow: K.snow(big, v, t, 80)
        if fx_: fx_(big, v)
    return K.shot(WORLD, K.light_stand, cx, cy, Z, acts=acts, back=back, front=front, pre=pre, emit=emit, fx_=fx2, sx=180, sy=sy)


# ================================================================== the standoff pieces
CROWD = [(250, 570, 8.2, False, (52, 60, 120), (220, 70, 70)), (320, 584, 8.8, False, (120, 40, 40), (70, 160, 90)),
         (385, 598, 9.4, False, (40, 90, 80), (250, 200, 60)), (645, 572, 8.4, True, (40, 40, 70), (240, 120, 60)),
         (710, 586, 9.0, True, (90, 60, 30), (120, 190, 240)), (775, 600, 9.4, True, (60, 60, 60), (220, 90, 150)),
         (860, 578, 8.4, True, (110, 50, 90), (240, 220, 110))]


CU_S = 12.5


def A(fn, wx, wy, un=None, s=None, flip=False, pin=None, **P):
    return DX.Act(fn, wx, wy, s_=s, un=un, flip=flip, pin=pin, **P)


def crowd(t, look=None, skip=(), fall=None, hat_look=None, expr='shock'):
    """the block holding its breath: townies with mittens at their mouths"""
    out = []
    for i, (x, y, un, flip, col, hat) in enumerate(CROWD):
        if i in skip: continue
        lk = 0.6 if look is None else look
        out.append(A(DC.townie, x, y, un=un, flip=flip, variant=i, pose='cover', t=t, expr=expr, look=lk, shadow=0.25))
    return out


def sal(t, peek=True):
    """Sal hides behind the counter: only the chef hat and two worried eyes peek over the Chicago dog"""
    return A(DC.sal, 545.0, LEDGE_Y + 12.0, un=8.0, t=t, look=-0.5 * math.sin(t * 3), clip_h=18.0)


def food(t, bite=0.0, dog=True, fries=True):
    out = []
    if dog: out.append(lambda CH, v: PR.chicago_dog(CH, v.cam(DOG_X, LEDGE_Y, 3.3), t, 1.0, bite=bite))
    if fries: out.append(lambda CH, v: PR.fries(CH, v.cam(FRY_X, LEDGE_Y, 3.3), 1.0))
    return out


TERRY_POSE = dict(n=(5.0, 19.6), f=(-3.0, 10.4), bn=1, bf=-1, nleg=(0.18, 0.0), fleg=(-0.18, 0.0))


def terry_standoff(t, mouth_=0.0, expr='panic', squeeze=0.0, reach=0.0, sweat=1.0, look=0.0, rec=None):
    """Terry holds the ketchup bottle high over the Chicago dog on the ledge; rec (dict) gets the bottle's hand point 'h' in sprite px"""
    hand = (lerp(31.0, 46.0, reach), lerp(93.0, 74.0, reach))
    def prop(sp, h, a, tt):
        DC.p_ketchup(sp, h, a, tt, squeeze=squeeze)
        if rec is not None: rec['h'] = h
    return A(DC.terry, TERRY_X, GY, un=PU, pose='stand', t=t, mouth_=mouth_, expr=expr, look=look, sweat=sweat, hands={'R': hand}, props={'R': prop},
             shadow=0.3)


CU_BG = 1.45                                 # background zoom behind close-ups (rule 05.10.2026); extreme close-ups capped at 1.7


def cu(fn, head, t, u, spk, expr, Z=2.3, zoom=0.05, pose='stand', flip=False, k=1.7, sy=262, extra=(), front=(), emit=None, look=0.0,
       pre_extra=None, fx_=None, s=CU_S, **kw):
    """close-up: the hero at 2x sprite resolution pinned by the head; the stand behind is zoomed less than the hero"""
    Zt = Z + zoom * u
    m_ = kw.pop('mouth_', mouth(spk, t, k) if spk else 0.0)
    a = A(fn, head[0], head[1], s=s * Zt / Z, flip=flip, pin='head', pose=pose, t=t, mouth_=m_, expr=expr, look=look, hires=True, **kw)
    zb = min(1.7, CU_BG * Zt / 2.3)
    return stand_shot(t, head[0], acts=list(extra) + [a], front=front, emit=emit, pre_extra=pre_extra, fx_=fx_, Z=zb, cy=head[1], sy=sy)


# ================================================================== shots
def r_hook(t, u):
    acts = food(t) + [terry_standoff(t, mouth('terry', t, 1.2), 'panic', sweat=1.0, look=0.5 * math.sin(t * 9))]
    big = stand_shot(t, 520.0, acts=acts, Z=1.62 + 0.04 * u, cy=410.0, sy=300)
    B.shake(big, t, 3.0, 47)
    return big


def r_wide(t, u):
    acts = crowd(t) + [sal(t)] + food(t) + [terry_standoff(t, mouth('terry', t, 1.5), 'panic', sweat=0.8)]
    return stand_shot(t, 560.0, acts=acts, Z=1.0 + 0.03 * u, cy=410.0, sy=330)


def r_walkin(t, u):
    k = sm(u / 1.65)
    x = lerp(170.0, 392.0, k)
    acts = crowd(t, skip=(2,)) + [sal(t)] + food(t) + [terry_standoff(t, 0.0, 'panic', sweat=0.8),
                                                    A(DC.dibs, x, GY + 12, un=PU, pose=DC.walk('arms_up', t, 5.0, 0.4, 0.3) if k < 0.98 else 'arms_up', t=t,
                                                      expr='normal', look=0.3, shades=True, shadow=0.3,
                                                      props={'R': lambda sp, h, a, tt: DC.p_shovel(sp, h, a, tt, a=1.45)})]
    return stand_shot(t, lerp(380.0, 460.0, k), acts=acts, Z=1.15, cy=420.0, sy=330)


def r_deb(t, u):
    def needles(big, v):
        for i, (x0, ph) in enumerate(((430, 0.0), (610, 0.12))):
            y = 520 + 1500 * max(0.0, (t - 5.35 - ph)) ** 2
            if y < OUT_H + 100:
                a = (t - 5.35) * (3 + i)
                for k in range(-90, 91, 3):
                    xx = int(x0 + math.sin(a) * k); yy = int(y + math.cos(a) * k)
                    if 0 <= xx < OUT_W - 6 and 0 <= yy < OUT_H - 6: big[yy:yy + 6, xx:xx + 6] = (216, 220, 232)
    return DK.deb_frame(t, 'panic', mouth('deb', t, 1.2), Z=2.0, u=u, pose='cover', props={}, fx_=needles, sweat=0.6)


def r_dibs_soft(t, u):
    return cu(DC.dibs, (610.0, 410.0), t, u, 'dibs', 'sad', pose='arms_up', k=1.5, shades=True)


def r_terry_mom(t, u):
    return cu(DC.terry, (520.0, 410.0), t, u, 'terry', 'cry', k=1.6, sweat=1.0, hands={'R': (27.0, 101.0)},
              props={'R': lambda sp, h, a, tt: DC.p_ketchup(sp, h, a, tt)})


def r_gasp(t, u):
    ang = min(1.35, 1.6 * u * u / 0.3)
    fall = A(DC.townie, 330.0, 584.0, un=8.8, variant=1, pose='cover', t=t, expr='stunned', rot=math.degrees(ang))
    acts = crowd(t, skip=(1,), look=0) + food(t) + [terry_standoff(t, 0.0, 'panic', sweat=0.8)]
    def fx_(big, v):
        K.snow(big, v, t, 40)
        ox, oy = v.opt(300, 600)
        for i in range(12):
            ph = (u * 2.0 + i * 0.09)
            big[int(oy - 160 * ph + 20 * math.sin(i)):int(oy - 160 * ph + 20 * math.sin(i)) + 12, int(ox + (i - 6) * 26):int(ox + (i - 6) * 26) + 12] = (236, 244, 255)
    return stand_shot(t, 465.0, acts=acts + [fall], fx_=fx_, Z=1.1, cy=420.0, sy=330)


def r_mrsw(t, u):
    return cu(DC.lady, (700.0, 425.0), t, u, 'mrs_w', 'deadpan', pose='hips', k=1.4, who='mrs_w', legs=True, clip_h=None)


def garden(big, t, t0, t1):
    if not (t0 <= t < t1): return
    k = min(1.0, (t - t0) / 0.12)
    items = ['MUSTARD', 'RELISH', 'ONION', 'TOMATO', 'PICKLE', 'SPORT PEPPERS', 'CELERY SALT']
    w, h = 640, 70 + 52 * len(items) + 40
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.rectangle([0, 0, w - 1, h - 1], fill=(14, 40, 20, 225), outline=(120, 240, 90, 255), width=7)
    d.text((w // 2, 44), 'THE GARDEN', font=O.pfont(46), fill=(150, 255, 110, 255), anchor='mm')
    for i, it in enumerate(items):
        yy = 100 + i * 52
        if t > t0 + 0.12 + i * 0.1:
            d.text((54, yy), '*', font=O.pfont(34), fill=(120, 240, 90, 255), anchor='mm')
            d.text((88, yy), it, font=O.pfont(34), fill=(250, 250, 240, 255), anchor='lm')
    O.overlay(big, np.array(img), 40, 990, k)


def r_dibs_garden(t, u):
    big = cu(DC.dibs, (700.0, 410.0), t, u, 'dibs', 'angry', pose='point', k=1.5, shades=True, sy=250)
    garden(big, t, 12.95, 15.9)
    return big


def r_terry_crack(t, u):
    return cu(DC.terry, (520.0, 410.0), t, u, 'terry', 'cry' if u < 1.2 else 'shock', k=1.7, sweat=1.0, hands={'R': (27.0, 101.0)},
              props={'R': lambda sp, h, a, tt: DC.p_ketchup(sp, h, a, tt)})


def r_turn_heads(t, u):
    acts = crowd(t, look=0) + food(t) + [terry_standoff(t, 0.0, 'shock', sweat=0.8)]
    big = stand_shot(t, 620.0, acts=acts, Z=1.2, cy=430.0, sy=330)
    if u < 0.12: O.flash(big, 0.5 * (1 - u / 0.12))
    return big


def crosshair(big, cx, cy, t, r=170):
    yy, xx = np.ogrid[:OUT_H, :OUT_W]
    d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    c = (255, 60, 60)
    big[(d > r - 8) & (d < r)] = c
    big[cy - 5:cy + 5, cx - r - 50:cx + r + 50] = c
    big[cy - r - 50:cy + r + 50, cx - 5:cx + 5] = c
    big[cy - 40:cy + 40, cx - 40:cx + 40] = (big[cy - 40:cy + 40, cx - 40:cx + 40] * 0.5).astype(np.uint8)


def r_roof(t, u):
    if u < 0.55:                                                                                # Gary lies behind the roof snow with a mustard rifle
        big = cu(DC.gary, (440.0, 150.0), t, u, 'gary', 'sly', pose='gun', k=1.2, props={'R': 'mustard_rifle'}, look=0.5)
        yy, xx = np.mgrid[1260:OUT_H, 0:OUT_W]
        big[1260:] = (226, 236, 250)
        big[1260:1290] = (250, 252, 255)
        big[1290:][((xx[30:] // 18 + yy[30:] // 18) % 4) == 0] = (196, 214, 240)
        return big
    big = stand_shot(t, 545.0, acts=food(t) + [terry_standoff(t, 0.0, 'panic', sweat=1.0)], Z=1.62, cy=428.0, sy=330)
    yy, xx = np.ogrid[:OUT_H, :OUT_W]
    d = np.sqrt((xx - 540) ** 2 + (yy - 960) ** 2)
    big[d > 520] = 0
    big[(d > 505) & (d <= 520)] = (40, 40, 44)
    big[956:964, 20:1060] = (20, 20, 24); big[:, 536:544] = np.where((d > 520)[:, 536:544, None], 0, 20).astype(np.uint8)
    for k in range(-4, 5):
        big[952:968, 540 + k * 90 - 5:540 + k * 90 + 5] = (20, 20, 24)
    return big


def r_drip(t, u):
    """insert: a drop swells on the bottle nozzle right above the Chicago dog (nozzle = p_ketchup tip h + (0.5, -12) of the drawn sprite)"""
    k = sm(u / 0.75)
    rec = {}
    terry = terry_standoff(t, 0.0, 'shock', sweat=1.0, rec=rec)
    def emit(big, v):
        sc = terry.scale(v); fx0, fy0 = v.opt(terry.wx, terry.wy); hx, hy = rec['h']
        ox, oy = fx0 + (hx + 0.5) * sc, fy0 - (hy - 12.0) * sc
        r = int(12 + 34 * k)
        yy, xx = np.ogrid[:OUT_H, :OUT_W]
        dr = ox, oy + r * (0.6 + 0.5 * k)
        dd = np.sqrt((xx - dr[0]) ** 2 / (0.8 * r) ** 2 + (yy - dr[1]) ** 2 / (1.05 * r) ** 2)
        big[dd < 1.12] = (120, 10, 22)                                                 # dark rim, like the sprite outlines
        big[int(oy) - 4:int(dr[1]), int(ox - r * 0.32) - 4:int(ox + r * 0.32) + 4] = (120, 10, 22)
        big[dd < 1.0] = (214, 28, 36)
        big[int(oy) - 4:int(dr[1]), int(ox - r * 0.32):int(ox + r * 0.32)] = (214, 28, 36)
        hl = np.sqrt((xx - (dr[0] - 0.32 * r)) ** 2 + (yy - (dr[1] - 0.3 * r)) ** 2) < 0.2 * r
        big[hl] = (255, 150, 140)
    return stand_shot(t, 556.0, acts=food(t) + [terry], emit=emit, Z=3.5, cy=410.0, sy=300, dof=9)


def r_dog(t, u):
    def fx_(big, v): B.steam(big, v, t, 548.0, 428.0, n=5, rise=110, size=40, a=0.45)
    return stand_shot(t, 548.0, acts=food(t, fries=False), fx_=fx_, Z=3.3 + 0.15 * u, cy=438.0, sy=330, dof=9)


def r_dibs_eye(t, u):
    return cu(DC.dibs, (620.0, 410.0), t, u, 'dibs', 'normal', Z=3.3, zoom=0.1, k=0.0, shades=False, sweat=1.0, sy=300, s=22.0)


def r_marty_eyes(t, u):
    un = 10.0
    ax, ay = 985.0, 380.0
    look = (math.sin(t * 5.0) * 0.9, 0.2)
    acts = [A(DC.marty, ax, ay, s=22.0, t=t, expr='glare', look=look[0], hires=True)]
    zb = 1.7; f = 2.6 / zb
    return stand_shot(t, ax + 0.5 * un * f, acts=acts, Z=zb, cy=ay - 9.0 * un * f, sy=300)


def r_terry_hand(t, u):
    acts = food(t) + [terry_standoff(t, 0.0, 'cry', squeeze=0.0, sweat=1.0)]
    big = stand_shot(t, 515.0, acts=acts, Z=3.0, cy=400.0, sy=330, dof=8)
    B.shake(big, t, 4, 53)
    return big


def r_freeze(t, u):
    acts = crowd(t, look=0) + [sal(t)] + food(t) + [terry_standoff(t, 0.0, 'panic', sweat=1.0)]
    big = stand_shot(t, 545.0, acts=acts, Z=1.0 + 0.5 * sm(u / 1.3), cy=420.0, sy=330)
    pulse = max(0.0, math.sin(u * 6.5)) ** 3
    fx.vignette(big, 0.25 + 0.4 * pulse)
    return big


def r_squirt(t, u):
    k = sm(min(1.0, u / 0.55))
    sq = 1.0 if u > 0.3 else 0.0
    nz = (lerp(521.0, 581.0, k), lerp(424.0, 446.0, k))
    def fx_(big, v): pass
    acts = food(t) + [terry_standoff(t, 0.0, 'content' if u > 0.3 else 'shock', squeeze=sq, reach=k, sweat=0.6)]
    def stream(CH, v):
        FX = Chars()
        B.jet(FX, v, t, TURN_T + 0.35, (nz[0] + 2, nz[1] + 3), (FRY_X - 2, LEDGE_Y - 24), arc=30, col=(214, 28, 36), col2=(255, 96, 96), width=3.0, grow=0.7)
        CH.col[FX.m] = FX.col[FX.m]; CH.m |= FX.m
    big = stand_shot(t, 540.0, acts=acts, front=[stream], Z=1.7, cy=425.0, sy=330, snow=False)
    # slow-motion feel: desaturate a bit and add speed-line shimmer
    g = big.mean(axis=2, keepdims=True)
    big[:] = (big * 0.7 + g * 0.3).astype(np.uint8)
    return big


def r_terry_fries(t, u):
    return cu(DC.terry, (520.0, 410.0), t, u, 'terry', 'stunned', pose='shrug', k=1.6, sweat=0.0)


def r_mrsw_shrug(t, u):
    big = cu(DC.lady, (700.0, 425.0), t, u, 'mrs_w', 'deadpan', pose='shrug', k=1.4, who='mrs_w', legs=True, clip_h=None)
    return big


def r_terry_freak(t, u):
    return cu(DC.terry, (520.0, 410.0), t, u, 'terry', 'nervous', pose='shrug', k=1.6, sweat=0.0)


def r_dibs_tension(t, u):
    return cu(DC.dibs, (620.0, 410.0), t, u, 'dibs', 'deadpan', k=1.4, shades=True, hands={'R': (18.0, 48.0)}, props={'R': 'coffee'})


def r_bite(t, u):
    head = (620.0, 410.0)
    bites = 0 if u < 0.15 else (1 if u < 0.35 else 2)
    dog = lambda sp, h, a, tt: DC.p_dog(sp, h, a, tt, bites=bites)
    a = A(DC.dibs, head[0], head[1], s=CU_S, pin='head', pose='stand', t=t, mouth_=chew(t) if u > 0.3 else 0.9, expr='content', shades=True,
          hands={'R': (12.0, 64.0)}, props={'R': dog}, hires=True)
    return stand_shot(t, head[0], acts=[a], Z=CU_BG, cy=head[1], sy=262)


def r_dibs_evidence(t, u):
    return cu(DC.dibs, (620.0, 410.0), t, u, 'dibs', 'smug', k=0.0, shades=True, mouth_=chew(t) * 0.6)


def r_marty(t, u):
    un = 10.0
    ax, ay = 985.0, 380.0
    q = 1.0 + 0.025 * u
    acts = [A(DC.marty, ax, ay, s=18.0 * q, t=t, mouth_=mouth('marty', t, 1.7), expr='deadpan', look=0.8, hires=True)]
    def fx_(big, v): B.steam(big, v, t, 960.0, 372.0, n=4, rise=90, size=34, a=0.35)
    f = 2.0 / CU_BG
    return stand_shot(t, ax + 3.0 * un * f, acts=acts, Z=CU_BG * q, cy=ay - 9.0 * un * f, sy=330, fx_=fx_)


def r_dibs_chair(t, u):
    return cu(DC.dibs, (620.0, 410.0), t, u, 'dibs', 'smug', k=1.6, shades=True)


def sal_arm(big, x, y, px=7):
    """Sal's arm reaching in from the right edge: pixel-art white chef sleeve + fist; (x, y) = screen point of the knuckles (left end, middle)"""
    x, y = int(x), int(y)
    w, h = (OUT_W - x) // px + 3, 18
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ol, skin, skin_d = (60, 48, 46, 255), (236, 190, 150, 255), (190, 136, 104, 255)
    d.rectangle([9, 3, w + 2, 14], fill=(236, 234, 228, 255), outline=ol)                  # sleeve
    d.line([10, 13, w, 13], fill=(196, 192, 186, 255)); d.line([10, 4, w, 4], fill=(252, 252, 248, 255))
    d.rectangle([10, 2, 13, 15], fill=(250, 250, 246, 255), outline=ol)                     # cuff
    d.ellipse([0, 2, 12, 15], fill=skin, outline=ol)                                        # fist round the bun end
    d.ellipse([1, 0, 8, 6], fill=skin, outline=ol)                                          # thumb on top of the bun
    for yy in (8, 11): d.line([2, yy, 8, yy], fill=skin_d)                                  # finger creases
    a = np.array(im.resize((w * px, h * px), Image.NEAREST))
    y0 = int(y) - h * px // 2; x0 = int(x)
    ys, xs = slice(max(0, y0), min(OUT_H, y0 + h * px)), slice(max(0, x0), min(OUT_W, x0 + w * px))
    sub = a[ys.start - y0:ys.stop - y0, xs.start - x0:xs.stop - x0]
    m = sub[..., 3] > 0
    big[ys, xs][m] = sub[..., :3][m]


def r_tail(t, u):
    """loop: Sal's arm slides a fresh Chicago dog back onto the ledge (the dog from the hook)"""
    k = sm(min(1.0, u / 0.35))
    dy = 40 * (1 - k)
    acts = [lambda CH, v: PR.chicago_dog(CH, v.cam(DOG_X, LEDGE_Y + dy, 3.3), t, 1.0)]
    def arm(big, v):
        ox, oy = v.opt(DOG_X + 30, LEDGE_Y - 6 + dy)
        sal_arm(big, ox, oy)
    return stand_shot(t, 548.0, acts=acts, Z=2.3, cy=420.0, sy=330, emit=arm, dof=6)


# ================================================================== shot table
SHOTS = [
    (0.00, 1.85, 'hook'), (1.85, 3.40, 'wide'), (3.40, 5.05, 'walkin'), (5.05, 7.35, 'deb'), (7.35, 8.78, 'dibs_soft'), (8.78, 10.55, 'terry_mom'),
    (10.55, 11.10, 'gasp'), (11.10, 12.60, 'mrsw'), (12.60, 15.90, 'dibs_garden'), (15.90, 18.00, 'terry_crack'), (18.00, 18.70, 'turn_heads'),
    (18.70, 19.70, 'roof'), (19.70, 20.45, 'drip'), (20.45, 21.05, 'dog'), (21.05, 21.75, 'dibs_eye'), (21.75, 22.35, 'marty_eyes'),
    (22.35, 23.00, 'terry_hand'), (23.00, TURN_T, 'freeze'), (TURN_T, 25.55, 'squirt'), (25.55, 27.85, 'terry_fries'), (27.85, 29.85, 'mrsw_shrug'),
    (29.85, 32.05, 'terry_freak'), (32.05, BITE_T, 'dibs_tension'), (BITE_T, 34.95, 'bite'), (34.95, 36.10, 'dibs_evidence'), (36.10, 37.65, 'marty'),
    (37.65, 38.95, 'dibs_chair'), (38.95, DUR + 1, 'tail'),
]
FUNCS = {'hook': r_hook, 'wide': r_wide, 'walkin': r_walkin, 'deb': r_deb, 'dibs_soft': r_dibs_soft, 'terry_mom': r_terry_mom, 'gasp': r_gasp,
         'mrsw': r_mrsw, 'dibs_garden': r_dibs_garden, 'terry_crack': r_terry_crack, 'turn_heads': r_turn_heads, 'roof': r_roof, 'drip': r_drip,
         'dog': r_dog, 'dibs_eye': r_dibs_eye, 'marty_eyes': r_marty_eyes, 'terry_hand': r_terry_hand, 'freeze': r_freeze, 'squirt': r_squirt,
         'terry_fries': r_terry_fries, 'mrsw_shrug': r_mrsw_shrug, 'terry_freak': r_terry_freak, 'dibs_tension': r_dibs_tension, 'bite': r_bite,
         'dibs_evidence': r_dibs_evidence, 'marty': r_marty, 'dibs_chair': r_dibs_chair, 'tail': r_tail}


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    return FUNCS[name](t, u)


# ================================================================== overlays
def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


SHOW = K.Show(EPI, 4, ['NO', 'KETCHUP'], hook_t=(0.15, 1.85),
              stickers=[
                  (st('CLEAR SHOT', (255, 90, 90), 56), 18.85, 19.70, 540, 330),
                  (st('TENSION', (255, 255, 255), 56), 32.15, 33.30, 540, 330),
              ],
              flashes=[], mosaics=[], cap_default=1400,
              cap_y={'wide': 1450, 'walkin': 1450, 'gasp': 1450, 'turn_heads': 1450, 'freeze': 1500, 'squirt': 1500, 'dibs_garden': 1560,
                     'tail': 1660})


def render(t):
    big = render_scene(t)
    SHOW.apply(big, t, shot_at(t)[2])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
