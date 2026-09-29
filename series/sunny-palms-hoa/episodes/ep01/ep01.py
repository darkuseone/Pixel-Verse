"""S01E01 «Ecru Whisper» — HOA fines Dale $250 for a mailbox that is the SAME colour as the approved one.
Dale (Florida Man) repaints it after "watching a video", wins, gets fined $500 for painting without a permit, dumps the mailbox on
the HOA president's lawn -> she fines herself -> the fine goes into her Bahamas fund. Earl the gator is grandfathered in.
  python3 ep01.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import paths as P
import stage as ST
from stage import Chars, view_at, shadow
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import us_cast as U
from props import us_props as UP
from props import uskit as K
from props import bytfx as B
from timeline import DUR, FPS, VOICE, SLUG

EPI = Episode('ep01', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
YARD = ST.ai_world(P.series(SLUG) / 'bg' / 'yard.png')
INTER = ST.ai_world(P.series(SLUG) / 'bg' / 'interior.png')

POST = (338.0, 552.0)                 # bare wooden post in Dale's lawn (base)
MB = (345.0, 478.0)                   # mailbox centre on the post (shoulder height for the wide-shot people)
MBS = 0.75                            # mailbox size factor
WU = 6.4                              # unit of people in wide shots (world px per unit)
CURB_Y = 588.0
STREET_Y = 668.0
BREND_LAWN = (985.0, 548.0)
DX0, DY0, DU = 430.0, 592.0, 16.0     # Dale CU anchor
BX0, BY0, BU = 965.0, 592.0, 16.0     # Brenda CU anchor
EX0, EY0, EU = 640.0, 492.0, 11.0     # Earl CU anchor (waterline)


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def J(u, p=1.7, k=0.38):
    """jump-cut punch-in: every other `p` seconds of a long shot is framed tighter (keeps a new angle every ~1.7 s)"""
    return k if int(u / p) % 2 else 0.0


def hit(t, t0, dur=0.35):
    """0..1 envelope for a reaction that starts at t0"""
    return max(0.0, 1 - (t - t0) / dur) if t >= t0 else 0.0


# ================================================================== close-ups
def cu_dale(t, u, expr, Z=2.0, hand=None, prop=None, shades=False, red=0.0, sweat=0.0, look=0.0, lean=0.0, pose=None, dx=0.0, dy=0.0,
            zoom=0.06, paint=None, kmouth=1.7):
    Zt = Z + zoom * u
    ST.set_px(ST.px_for_zoom(Zt))
    v = view_at(YARD, DX0 + 1.5 * DU + dx, DY0 - 21.0 * DU + dy, Zt, 180, 262)
    CH, FX = K.begin(Zt)
    big = v.bg()
    U.dale(CH, v.cam(DX0, DY0, DU), pose or U.DPOSE['stand'], t, mouth('dale', t, kmouth), expr, look, shades, hand_n=hand,
           prop_n=prop, lean=lean, sweat=sweat, red=red, paint=paint)
    CH.comp(big, K.light_yard(v))
    fx.vignette(big, 0.28)
    return big


def cu_brenda(t, u, expr, Z=2.0, hand=None, prop=None, pose=None, sweat=0.0, look=0.0, lean=0.0, dx=0.0, dy=0.0, zoom=0.06, hand_f=None,
              prop_f=None, in_cart=False, kmouth=1.6):
    Zt = Z + zoom * u
    ST.set_px(ST.px_for_zoom(Zt))
    v = view_at(YARD, BX0 - 1.5 * BU + dx, BY0 - 20.6 * BU + dy, Zt, 180, 262)
    CH, FX = K.begin(Zt)
    big = v.bg()
    if in_cart:
        CB, CF = Chars(), Chars()
        seat = UP.golf_cart(CB, CF, v, BX0 - 5.5 * BU, BY0 + 1.5 * BU, u=BU, flip=True, t=t, brake=1.0)
        CB.comp(big, K.light_yard(v))
        U.brenda(CH, v.cam(seat[0], seat[1], BU, flip=True), U.BPOSE['sit'], t, mouth('brenda', t, kmouth), expr, look, hand_n=hand,
                 prop_n=prop, lean=lean, sweat=sweat, hand_f=hand_f, prop_f=prop_f)
        CH.comp(big, K.light_yard(v))
        CF.comp(big, K.light_yard(v))
    else:
        U.brenda(CH, v.cam(BX0, BY0, BU, flip=True), pose or U.BPOSE['stand'], t, mouth('brenda', t, kmouth), expr, look, hand_n=hand,
                 prop_n=prop, lean=lean, sweat=sweat, hand_f=hand_f, prop_f=prop_f)
        CH.comp(big, K.light_yard(v))
    fx.vignette(big, 0.28)
    return big


def cu_earl(t, u, lid=0.5, Z=2.6, look=(0.0, 0.0), paint=None, grin=0.0, dx=0.0, dy=0.0, zoom=0.05, mist=0.0):
    Zt = Z + zoom * u
    ST.set_px(ST.px_for_zoom(Zt))
    v = view_at(YARD, EX0 + 2.0 * EU + dx, EY0 - 3.0 * EU + dy, Zt, 180, 330)
    CH, FX = K.begin(Zt)
    big = v.bg()
    U.earl(CH, v.cam(EX0, EY0, EU), t, mouth('earl', t, 1.6), lid, look, paint, 0.0, 1.0, True, grin)
    CH.comp(big, K.light_pond(v))
    # waterline glint + ripples
    ox, oy = v.opt(EX0, EY0)
    for k in range(3):
        ph = (t * 0.5 + k / 3) % 1.0
        rw = int((60 + 300 * ph) * v.Z / 2.6); a = 0.5 * (1 - ph)
        y0 = int(oy) + 4 + k * 3
        x0 = int(ox + 60 - rw); x1 = int(ox + 60 + rw)
        if 0 <= y0 < 1914:
            seg = big[y0:y0 + 6, max(0, x0):min(1080, x1)]
            seg[:] = (seg * (1 - a) + np.array((200, 240, 230)) * a).astype(np.uint8)
    if mist > 0:
        for i in range(10):
            r = np.random.default_rng(i)
            cx = ox + 60 + r.uniform(-260, 260); cy = oy - 90 + r.uniform(-170, 120)
            B.puff(big, cx, cy, 90 + 60 * r.random(), 0.55 * mist, UP.BONE)
    fx.vignette(big, 0.28)
    return big


# ================================================================== wide shots
def wide_view(cx, cy, Z=1.0):
    return view_at(YARD, cx, cy, Z, 180, 330)


def r_cart(t, u):
    """Brenda's golf cart arrives at 4 mph with a horror-movie tyre screech"""
    Z = 1.15
    v = wide_view(575, 560, Z)
    CH, FX = K.begin(Z)
    CB, CF, CM = Chars(), Chars(), Chars()
    big = v.bg()
    x = 610 - 26 * u
    cu = 6.0
    seat = UP.golf_cart(CB, CF, v, x, STREET_Y, u=cu, flip=True, t=t, brake=0.0 if u < 0.05 else 0.6)
    CB.comp(big, K.light_yard(v))
    U.brenda(CM, v.cam(seat[0], seat[1], cu, flip=True), U.BPOSE['sit'], t, 0.0, 'sweet', 0.0, hand_n=U.H(3.2, 13.6), prop_n=UP.clipboard)
    CM.comp(big, K.light_yard(v))
    CF.comp(big, K.light_yard(v))
    if u > 0.03:
        for i in range(8):
            ph = u - 0.03 - i * 0.05
            if ph < 0: continue
            ox, oy = v.opt(x + 90 + 22 * i * 0.6 + 40 * ph, STREET_Y - 6 - 30 * ph)
            B.puff(big, ox, oy, (30 + 70 * ph) * 3, 0.6 * max(0, 1 - ph / 0.9), (230, 230, 236))
    if u < 0.35: B.shake(big, t, 10 * (1 - u / 0.35), 33)
    fx.vignette(big, 0.22)
    return big


def dale_wide(CH, v, x, y, pose, t, expr='smug', flip=False, **kw):
    U.dale(CH, v.cam(x, y, WU, flip), pose, t, mouth('dale', t), expr, **kw)


def mailbox_at(CH, v, painted=0.0, t=0.0, attached=True):
    if attached: UP.mailbox_world(CH, v, MB[0], MB[1], painted, t, s=MBS)


def r_spray(t, u):
    """M1: Dale sprays the mailbox, overspray drifts on the wind"""
    Z = 1.55
    v = view_at(YARD, 335, 500, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    painted = sm((u - 0.3) / 0.7)
    mailbox_at(CH, v, painted, t)
    CH.comp(big, K.light_yard(v))
    C2 = Chars()
    shake_ = math.sin(t * 40) * 0.25 if u < 0.32 else 0.0
    can = lambda L, h: UP.spray_can(L, h, -0.35 - 0.25 * math.sin(t * 30) * (1 if u < 0.3 else 0))
    pose = U.DPOSE['spray'] if u >= 0.3 else U.DPOSE['hold']
    U.dale(C2, v.cam(250.0, 590.0, WU), pose, t, 0.0, 'smug' if u > 0.3 else 'normal', 0.0, hand_n=U.H(9.6, 17.6 + shake_) if u >= 0.3 else U.H(5.8, 14.6 + shake_),
           prop_n=can)
    C2.comp(big, K.light_yard(v))
    if u >= 0.3:
        nx, ny = v.opt(250 + 9.6 * WU + 12, 590 - 17.6 * WU - 4)
        for i in range(10):
            ph = ((t - 0.3) * 3 + i * 0.13) % 1.0
            B.puff(big, nx + 200 * ph * 0.9 + 40 * i * 0.15, ny + 16 * math.sin(i) + 34 * ph - 30, 34 + 100 * ph, 0.9 * (1 - ph), (255, 250, 232))
    fx.vignette(big, 0.22)
    return big


def r_earl_sprayed(t, u):
    k = sm(u / 0.5)
    lid = 0.5 if u < 0.55 else 0.9 - 0.4 * (1 if u > 0.75 else 0)
    return cu_earl(t, u, lid=lid, Z=2.4, paint=(226, 206, 156) if u > 0.25 else None, mist=0.6 * max(0.0, 1 - u / 0.8), look=(0.4, 0.2), dx=-10)


def r_thumbs(t, u):
    """M3: Dale steps back and admires the same-looking mailbox"""
    Z = 1.5
    v = view_at(YARD, 300, 500, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    mailbox_at(CH, v, 1.0, t)
    CH.comp(big, K.light_yard(v))
    C2 = Chars()
    U.dale(C2, v.cam(215.0, 592.0, WU), dict(U.DPOSE['cheer'], n=(6.4, 15.5)), t, 0.0, 'smug', 0.0, shades=(u > 0.3), hand_n=U.H(6.4, 15.5 + 0.5 * math.sin(t * 12)))
    C2.comp(big, K.light_yard(v))
    for i in range(4):                                                                     # sparkle
        ph = (u * 2.2 + i * 0.25) % 1.0
        sx, sy = v.opt(MB[0] - 40 + i * 30, MB[1] - 24 - 10 * i + 6 * math.sin(i))
        s = int(18 * math.sin(ph * math.pi))
        if s > 1:
            big[int(sy) - s:int(sy) + s, int(sx) - 2:int(sx) + 2] = (255, 255, 230)
            big[int(sy) - 2:int(sy) + 2, int(sx) - s:int(sx) + s] = (255, 255, 230)
    fx.vignette(big, 0.22)
    return big


def r_compare(t, u):
    """M4: Brenda checks the chip against the mailbox, one eye squinting -> stamps APPROVED"""
    Z = 1.35
    v = view_at(YARD, 320, 500, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    mailbox_at(CH, v, 1.0, t)
    CH.comp(big, K.light_yard(v))
    C2 = Chars()
    U.dale(C2, v.cam(240.0, 592.0, WU), U.DPOSE['hips'], t, 0.0, 'smug', 0.0, shades=True)
    C2.comp(big, K.light_yard(v))
    C3 = Chars()
    press = sm((t - 24.5) / 0.1) if t < 24.7 else max(0.0, 1 - (t - 24.7) / 0.3)
    pr = t >= 24.45
    U.brenda(C3, v.cam(415.0, 592.0, WU, flip=True), dict(U.BPOSE['show'], n=(-2.4, 16.5)) if not pr else dict(U.BPOSE['write']), t, 0.0,
             'evil' if pr else 'sweet', 0.0, hand_n=(U.H(-2.4, 17.6)),
             prop_n=(lambda L, h: UP.chip_fan(L, h, -2.3 + 0.0, 0.28, 1.0)) if not pr else (lambda L, h: UP.stamp_tool(L, h, press)))
    C3.comp(big, K.light_yard(v))
    fx.vignette(big, 0.22)
    return big


def r_yank(t, u):
    """rip the mailbox off the post"""
    Z = 1.6
    v = view_at(YARD, 340, 500, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    k = sm(u / 0.32)
    if u < 0.32: mailbox_at(CH, v, 1.0, t)
    CH.comp(big, K.light_yard(v))
    C2 = Chars()
    pose = U.DPOSE['hold'] if u < 0.32 else U.DPOSE['hold']
    U.dale(C2, v.cam(270.0, 592.0, WU), dict(pose, n=(6.4, 13.6), f=(5.4, 13.9)), t, mouth('dale', t), 'manic', 0.0, red=0.6,
           prop_n=lambda L, h: UP.mailbox_held(L, h, s=1.0) if u >= 0.32 else None, hand_n=U.H(6.4, 13.6 + 2.0 * (1 - k)))
    C2.comp(big, K.light_yard(v))
    if 0.3 < u < 0.6:
        B.puff(big, *v.opt(POST[0], POST[1] - 90), 160 * v.Z / 1.6, 0.5 * (1 - (u - 0.3) / 0.3), (196, 170, 130))
    if u < 0.5: B.shake(big, t, 12 * max(0.0, 1 - u / 0.5), 35)
    fx.vignette(big, 0.22)
    return big


def r_march(t, u):
    """Dale marches past the pond with the mailbox; Earl's eyes follow"""
    Z = 1.05
    x = lerp(400.0, 900.0, u / 0.7 if u < 0.7 else 1.0)
    v = view_at(YARD, lerp(420, 800, min(1.0, u / 0.7)), 480, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    U.earl(CH, v.cam(640.0, 500.0, 4.4), t, 0.0, 0.55, (1.0 if x > 640 else -0.3, 0.0), None, 0.0, 1.0, True)
    CH.comp(big, K.light_pond(v))
    C2 = Chars()
    U.dale(C2, v.cam(x, 596.0, WU), U.dwalk(t, 12.0, 0.5, carry=True), t, mouth('dale', t), 'manic', 0.0, red=0.6,
           prop_n=lambda L, h: UP.mailbox_held(L, h, s=1.0))
    C2.comp(big, K.light_yard(v))
    fx.vignette(big, 0.22)
    return big


def r_plant(t, u):
    """Dale plants the mailbox on Brenda's immaculate lawn"""
    Z = 1.25
    v = view_at(YARD, 995, 500, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    UP.mailbox_world(CH, v, 1005.0, 528.0 + 6 * max(0.0, 1 - u / 0.15), 0.0, t, s=MBS)
    CH.comp(big, K.light_yard(v))
    C2 = Chars()
    U.dale(C2, v.cam(915.0, 592.0, WU), U.DPOSE['hips'], t, mouth('dale', t), 'smug', 0.0, shades=(u > 0.2))
    C2.comp(big, K.light_yard(v))
    C3 = Chars()
    U.brenda(C3, v.cam(1095.0, 592.0, WU, flip=True), U.BPOSE['stand'], t, 0.0, 'sweet', 0.0, hand_n=U.H(3.4, 13.6), prop_n=UP.clipboard)
    C3.comp(big, K.light_yard(v))
    if u < 0.3: B.shake(big, t, 10 * (1 - u / 0.3), 33)
    fx.vignette(big, 0.22)
    return big


def r_fund(t, u):
    """the Beautification Fund: jar of cash, then pull out to the BAHAMAS 2027 chart, which jumps to 100%"""
    k = sm((u - 0.35) / 0.4)
    Z = lerp(2.1, 1.0, k)
    cx, cy = lerp(318.0, 452.0, k), lerp(370.0, 262.0, k)
    v = view_at(INTER, cx, cy, Z, 180, 330)
    CH, FX = K.begin(Z)
    big = v.bg()
    UP.fund_jar(CH, v, t, 1.0 if u > 0.6 else 0.94)
    CH.comp(big, K.light_int(v))
    lvl = 0.94 if u < 0.6 else min(1.0, 0.94 + 0.06 * sm((u - 0.6) / 0.25))
    UP.fund_insert(big, v, t, lvl, pop=(u - 0.85) / 0.3 if u > 0.85 else 0.0)
    fx.shafts(big, t, 0.6, 0.05)
    fx.vignette(big, 0.25)
    return big


def r_chips(t, u):
    """insert: the two 'different' colours"""
    v = view_at(YARD, 465, 250, 2.0, 180, 330)
    big = v.bg()
    big[:] = (big * 0.35).astype(np.uint8)
    im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0))
    from PIL import ImageDraw
    d = ImageDraw.Draw(im); d.fontmode = '1'
    def card(x0, y0, name, tilt):
        d.rectangle([x0 - 10, y0 - 10, x0 + 430, y0 + 690], fill=(20, 12, 30, 255))
        d.rectangle([x0, y0, x0 + 420, y0 + 680], fill=(252, 250, 244, 255))
        d.rectangle([x0 + 24, y0 + 24, x0 + 396, y0 + 470], fill=UP.BONE + (255,))
        f = O.pfont(34)
        bb = f.getbbox(name)
        d.text((x0 + 210 - (bb[2] - bb[0]) / 2 - bb[0], y0 + 540), name, font=f, fill=(40, 30, 60, 255))
    y_off = int(24 * math.sin(t * 6)) if u < 0.2 else 0
    card(60, 470 + y_off, 'BONE', 0); card(590, 470 - y_off, 'ECRU', 0)
    if u > 0.45:
        f2 = O.pfont(int(96 + 14 * math.sin(u * 14))); bb2 = f2.getbbox('='); d.text((540 - (bb2[2] - bb2[0]) / 2 - bb2[0], 760), '=', font=f2, fill=(255, 92, 96, 255), stroke_width=8, stroke_fill=(30, 12, 30, 255))
    f = O.pfont(34); bb = f.getbbox('WHISPER'); d.text((590 + 210 - (bb[2] - bb[0]) / 2 - bb[0], 470 - y_off + 592), 'WHISPER', font=f, fill=(40, 30, 60, 255))
    O.overlay(big, np.array(im), 0, 0, 1.0)
    return big


# ================================================================== shot table
SHOTS = [
    (0.00, 2.77, 'hook'), (2.77, 3.95, 'cart'), (3.95, 6.95, 'b1'), (6.95, 8.38, 'd2'), (8.38, 9.85, 'b2'), (9.85, 11.28, 'chips'),
    (11.28, 12.95, 'd3'), (12.95, 14.62, 'b3'), (14.62, 17.96, 'd4'), (17.96, 21.38, 'e1'),
    (21.38, 22.50, 'spray'), (22.50, 23.35, 'earl_paint'), (23.35, 24.25, 'thumbs'), (24.25, 25.00, 'compare'),
    (25.00, 26.04, 'd5'), (26.04, 29.09, 'b5'), (29.09, 30.34, 'd6'), (30.34, 33.84, 'b6'),
    (33.84, 34.85, 'd7'), (34.85, 35.35, 'yank'), (35.35, 36.11, 'march'), (36.11, 37.73, 'plant'), (37.73, 39.89, 'b7'),
    (39.89, 40.75, 'b8'), (40.75, 41.90, 'fund'), (41.90, 45.40, 'e2'), (45.40, DUR + 1, 'tail'),
]


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    if name == 'hook':
        big = cu_dale(t, u, 'shout', 1.75, dx=34, hand=U.H(5.6, 12.6), prop=lambda L, h: UP.notice(L, h, -0.2, w=5.2, hh=6.8),
                      red=0.55 + 0.35 * hit(t, 0.85) + 0.25 * hit(t, 1.55), sweat=0.5)
        if 0.85 < t < 1.0 or 1.55 < t < 1.7: B.shake(big, t, 12, 37)
        return big
    if name == 'cart': return r_cart(t, u)
    if name == 'b1':
        return cu_brenda(t, u, 'sweet', 2.0 + J(u, 1.5), hand=U.H(3.4, 10.2), prop=lambda L, h: UP.clipboard(L, h, -0.15, w=4.4, hh=6.0), in_cart=True)
    if name == 'd2': return cu_dale(t, u, 'incredulous' if u < 0.3 else 'shout', 2.2, hand=U.H(6.0, 17.6), red=0.6, sweat=0.5, look=0.3)
    if name == 'b2': return cu_brenda(t, u, 'sweet', 2.1, hand=U.H(7.6, 11.6), prop=lambda L, h: UP.chip_fan(L, h, -1.6, 0.3, 1.2))
    if name == 'chips': return r_chips(t, u)
    if name == 'd3': return cu_dale(t, u, 'angry', 2.2, hand=U.H(6.0, 17.2), red=0.85, sweat=0.7)
    if name == 'b3':
        return cu_brenda(t, u, 'sweet', 2.3, lean=0.4, hand=U.H(3.2, 12.4), pose=U.BPOSE['hands'])
    if name == 'd4':
        return cu_dale(t, u, 'smug', 2.0 + J(u), shades=(t > 16.75), pose=U.DPOSE['hips'], look=0.2, zoom=0.1, dx=-6 * u)
    if name == 'e1': return cu_earl(t, u, 0.5, 2.6 + J(u, 1.7, 0.45))
    if name == 'spray': return r_spray(t, u)
    if name == 'earl_paint': return r_earl_sprayed(t, u)
    if name == 'thumbs': return r_thumbs(t, u)
    if name == 'compare': return r_compare(t, u)
    if name == 'd5': return cu_dale(t, u, 'cheer', 2.1, shades=(u > 0.12), hand=U.H(8.6, 26.0 - 1.4 * math.sin(u * 20)), zoom=0.15)
    if name == 'b5':
        return cu_brenda(t, u, 'sweet' if u < 1.95 else 'evil', 2.2 + J(u, 1.5), pose=U.BPOSE['hands'], lean=0.3)
    if name == 'd6': return cu_dale(t, u, 'shock', 2.3, shades=None if u > 0.05 else True, sweat=0.9, red=0.15, pose=U.DPOSE['shout'], zoom=0.2)
    if name == 'b6':
        return cu_brenda(t, u, 'sweet' if u < 1.6 else 'evil', 2.2 + J(u, 1.75), hand=U.H(3.2, 11.0), prop=lambda L, h: UP.clipboard(L, h, -0.12, w=4.6, hh=6.2))
    if name == 'd7': return cu_dale(t, u, 'manic', 2.4, red=0.95, sweat=0.9, zoom=0.25, pose=U.DPOSE['shout'])
    if name == 'yank': return r_yank(t, u)
    if name == 'march': return r_march(t, u)
    if name == 'plant': return r_plant(t, u)
    if name == 'b7': return cu_brenda(t, u, 'dread', 2.4, sweat=1.0, zoom=0.2, pose=U.BPOSE['hands'])
    if name == 'b8':
        return cu_brenda(t, u, 'hollow' if u < 0.4 else 'cheer', 2.3, hand=U.H(3.4, 14.4), prop=(lambda L, h: UP.ticket_pad(L, h)) if u > 0.15 else None)
    if name == 'fund': return r_fund(t, u)
    if name == 'e2': return cu_earl(t, u, 0.5 if u < 3.0 else 0.75, 2.5 + J(u, 1.75, 0.45), grin=0.0)
    slide = 1 - sm(u / 0.25)
    return cu_dale(t, u, 'shout' if u < 0.4 else 'incredulous', 1.75, dx=34, hand=U.H(5.6 + 6 * slide, 12.6 - 6 * slide),
                   prop=lambda L, h: UP.notice(L, h, -0.2 - 1.2 * slide, w=5.2, hh=6.8, txt='$100'), red=0.5, sweat=0.4)


def _shake(big, t, amp):
    B.shake(big, t, amp, 37)
    return big


def st(text, fg=(255, 236, 120), size=56):
    return O.sticker(text, fg=fg, size=size)


SHOW = K.Show(EPI, 1, ['$250 FOR', 'A MAILBOX?!'], hook_t=(0.15, 2.4),
              stickers=[
                  (st('(TRANSLATION: YOU IDIOT)', (255, 190, 226), 28), 13.55, 14.55, 540, 1130),
                  (st('APPROVED', (255, 92, 96), 96), 24.62, 26.0, 540, 470),
                  (st('AURA +9999', (255, 236, 96), 60), 25.18, 26.0, 540, 320),
                  (st('$500', (255, 84, 96), 170), 27.85, 29.05, 540, 470),
                  (st('AURA -9999', (255, 100, 100), 60), 29.30, 30.3, 540, 340),
                  (st('SINCE 1987', (255, 226, 110), 72), 44.0, 45.4, 540, 470),
                  (st('4 MPH', (255, 236, 96), 96), 2.9, 3.95, 700, 640),
                  (st('[SAXOPHONE GETS LOUDER]', (255, 255, 255), 30), 16.3, 17.9, 540, 1480),
                  (st('[SAXOPHONE GETS LOUDER]', (255, 255, 255), 30), 33.4, 34.7, 540, 1480),
                  (st('[SAXOPHONE GETS LOUDEST]', (255, 255, 255), 30), 37.1, 38.9, 540, 1480),
                  (st('TOTAL FINES: $750', (255, 236, 120), 40), 45.85, 47.0, 540, 1450),
              ],
              flashes=[25.00, 33.84], mosaics=[21.38, 39.89], cap_y={'chips': 1500, 'fund': 1560, 'spray': 1420, 'thumbs': 1420, 'march': 1420,
                                                                          'plant': 1420, 'cart': 1420, 'yank': 1420, 'compare': 1420},
              teaser='NEXT: THE FLAMINGO')


def render(t):
    big = render_scene(t)
    SHOW.apply(big, t, shot_at(t)[2])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
