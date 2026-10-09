"""S01E05 «Python Money» (09.10.2026) — the season's peak (almost a win). A notice slapped on the trailer: RENT $3,400/MO.
«THIRTY-FOUR HUNDRED?! For a SHED?!» Tanner (job #6, Sawgrass Acres MGMT): «It's a TINY HOME! Very trendy!» A poster on the fence: PYTHON
BOUNTY $50/FT. «Mort. Hold my sub.» — «My fee is a THIRD.» The airboat tears through the sawgrass; a 20-ft python rises and wraps him
like a scarf: «Easy, buddy.» It steals the sub out of Mort's pouch: «Not the SUB.» A dust-cloud brawl -> the python tied in a bow, alive and
offended. The FWC bounty window: Tanner again (job #7, an MGMT badge on his lanyard — the clue): «Twenty feet! A THOUSAND bucks!» — «RENT
money!» TWIST (55 %, success worse than failure): the ranger shirt comes off, MGMT underneath: «You make python money now? Rent's UP!» —
$4,400 slapped on his chest. «That's MORE than I made.» Mort plucks a third: «And my THIRD.» In the trailer window the python on HIS couch
(the sub bulging): «Rented it! He's got better CREDIT.» He holds his wrists out to Darlene: «Officer. Take me HOME.» Mugshot, BREAKING,
9/10: «One more. Then it's FREE.» Button: $4,400 slapped on the trailer — the python hisses. -> loop.
  python3 ep05.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from timeline import DUR, FPS, VOICE, SLUG, CUTS

EPI = Episode('ep05', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
K.SLOGAN[:] = ['SNAKE IN', 'YOUR SHED?']
K.BOOTH_SIGN[:] = ['FISH - WILDLIFE', 'PYTHON BOUNTY', '$50 PER FOOT']
YARD = K.world_baked('yard').copy()
SWAMP = K.world('swamp')
BOOTH = K.world_baked('booth')
A, wpt, aout = K.A, K.wpt, K.aout
LT = K.light_sun
SAND = 626.0
CHAIR = (806.0, 476.0)
WINDOW = (218, 254, 328, 340)       # the trailer window (world box)
BWIN = (444, 300, 836, 440)         # the booth's service window
WATER = 694.0                       # swamp: the airboat's waterline
S_YARD, S_MORT, S_SW = 10.0, 7.0, 12.0


def _poster():
    """PYTHON BOUNTY poster zip-tied to the fence by the lawn chair"""
    x0, y0, x1, y1 = 632, 404, 730, 474
    YARD[y0:y1, x0:x1] = (250, 248, 236)
    YARD[y0:y0 + 14, x0:x1] = (40, 120, 70)
    K.wtext(YARD, 'PYTHON', x0 + 25, y0 + 2, (255, 255, 255), 2)
    K.wtext(YARD, 'BOUNTY', x0 + 25, y0 + 18, (226, 34, 52), 2)
    K.wtext(YARD, '$50/FT', x0 + 25, y0 + 32, (14, 44, 54), 2)
    for q in range(8): YARD[y0 + 52 + (q % 2) * 3:y0 + 56 + (q % 2) * 3, x0 + 10 + q * 10:x0 + 20 + q * 10] = (150, 130, 70)
    K.wtext(YARD, '- FWC', x0 + 32, y0 + 61, (14, 44, 54), 1)


_poster()


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
    x0, y0 = v.opt(box[0], box[1]); x1, y1 = v.opt(box[2], box[3])
    x0, y0, x1, y1 = (int(np.clip(q, 0, m)) for q, m in ((x0, OUT_W), (y0, OUT_H), (x1, OUT_W), (y1, OUT_H)))
    m = np.ones(big.shape[:2], bool); m[y0:y1, x0:x1] = False
    big[m] = bg0[m]


_NOTE = {}


def notice(big, cx, cy, w, t, t0, amount='$3,400/MO', ang=-5.0):
    """the rent-hike notice slapped on (screen space): drops in big at t0, wobbles"""
    if t < t0: return
    key = (amount, w)
    if key not in _NOTE:
        h = int(w * 1.15)
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
        d.rectangle([0, 0, w - 1, h - 1], fill=(14, 44, 54, 255)); d.rectangle([6, 6, w - 7, h - 7], fill=(252, 250, 236, 255))
        d.rectangle([6, 6, w - 7, int(h * 0.2)], fill=(150, 110, 200, 255))
        f1, f2, f3 = O.pfont(int(w * 0.1)), O.pfont(int(w * 0.07)), O.pfont(int(w * 0.088))
        d.text((int(w * 0.08), int(h * 0.06)), 'NOTICE', font=f1, fill=(255, 255, 255, 255))
        d.text((int(w * 0.08), int(h * 0.3)), 'NEW RENT:', font=f2, fill=(14, 44, 54, 255))
        d.text((int(w * 0.08), int(h * 0.45)), amount, font=f3, fill=(226, 34, 52, 255))
        d.text((int(w * 0.08), int(h * 0.7)), 'SAWGRASS ACRES', font=O.pfont(int(w * 0.055)), fill=(14, 44, 54, 255))
        d.text((int(w * 0.08), int(h * 0.8)), 'MGMT. NO WORRIES!', font=O.pfont(int(w * 0.05)), fill=(150, 110, 200, 255))
        _NOTE[key] = im
    k = min(1.0, (t - t0) / 0.08)
    sc = 1.5 - 0.5 * k
    im = _NOTE[key].rotate(ang + 3.0 * math.sin((t - t0) * 20) * max(0.0, 1 - (t - t0) * 3), resample=Image.NEAREST, expand=True)
    im = im.resize((int(im.width * sc), int(im.height * sc)), Image.NEAREST)
    O.overlay(big, np.array(im), int(cx - im.width / 2), int(cy - im.height / 2), 1.0)


def cash(big, x, y, n=7, spread=1.0, sc=1.0):
    """a fan of green bills (screen space)"""
    for i in range(n):
        a = math.radians(-50 + i * 100 / max(1, n - 1)) * spread
        w, h = int(70 * sc), int(150 * sc)
        cx, cy = x + math.sin(a) * h * 0.5, y - math.cos(a) * h * 0.5
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        d.rectangle([0, 0, w - 1, h - 1], fill=(14, 60, 30, 255)); d.rectangle([5, 5, w - 6, h - 6], fill=(120, 200, 110, 255))
        d.ellipse([w // 2 - 16, h // 2 - 16, w // 2 + 16, h // 2 + 16], outline=(14, 90, 40, 255), width=5)
        im = im.rotate(-math.degrees(a), resample=Image.NEAREST, expand=True)
        O.overlay(big, np.array(im), int(cx - im.width / 2), int(cy - im.height / 2), 1.0)


SCARF = [(28.0, -6.0), (24.0, 10.0), (18.0, 26.0), (12.0, 37.0), (2.0, 41.0), (-7.0, 45.0), (-8.0, 51.0), (-1.0, 55.0), (9.0, 53.0),
         (14.0, 50.0), (18.0, 55.0), (19.0, 60.0)]


def python_scarf(x, y, s, t, lump=0.0, pts=None, **kw):
    return A(C.python, x, y, s, t=t, pts=pts or SCARF, lump=lump, thick=0.75, **kw)


# ================================================================== shots
def r_hook(t, u):
    """XCU in front of the trailer: the notice slaps onto the wall beside his head — RENT $3,400/MO"""
    big, a, v = cu(YARD, LT, C.fm, t, 300.0, 330.0, 30.0, (480, 900), Z=1.35, blur=6, expr='shriek', mouth_=mouth('fm', t), sweat=0.8,
                   glasses_drop=min(1.0, 0.3 + u / 0.8), look=(0.8, 0.5))
    notice(big, 770, 640, 330, t, 0.0)
    if u < 0.5: B.shake(big, t, 9, 33)
    return big


def r_tanner(t, u):
    """MS: Tanner (job #6, purple SAWGRASS ACRES MGMT polo) by the trailer, tablet up: «It's a TINY HOME! Very trendy!»"""
    Z = 1.35
    acts = [A(C.fm, 360.0, SAND, S_YARD * Z, t=t, expr='angry', look=(1.0, 0.2), shadow=0.35),
            A(C.tanner, 470.0, SAND, S_YARD * 1.05 * Z, flip=True, t=t, uniform='mgmt', jobs=6, expr='chipper', mouth_=mouth('tanner', t, 2.0),
              look=(-0.2, 0.0), hand_n=(10.0, 42.0), prop_n=lambda sp, h: C.tablet(sp, (h[0] + 0.5, h[1] - 0.5)), thumbs=u > 1.4, shadow=0.35)]
    def f(big, v):
        x, y = v.opt(300.0, 300.0)
        notice(big, x, y, 150, t, 0.0, ang=-3.0)
    return K.shot(YARD, LT, 420.0, 440.0, Z, acts=acts, fx_=f, sx=180, sy=320)


def r_hold(t, u):
    """MS: he points at the PYTHON BOUNTY poster on the fence and hands Mort the sub — into the pouch (7.10)"""
    Z = 1.4
    gone = t >= 7.1
    gul = min(1.0, max(0.0, (t - 7.1) / 0.3))
    fm_ = A(C.fm, 742.0, SAND, S_YARD * Z, t=t, expr='zen', mouth_=mouth('fm', t), look=(0.8, 0.5),
            hand_n=(15.0, 48.0), prop_n=None if gone else (lambda sp, h: C.sub(sp, (h[0] + 1.0, h[1] + 1.0), ang=0.2)), shadow=0.35)
    mort = A(C.mort, CHAIR[0], CHAIR[1], S_MORT * Z, flip=True, t=t, expr='deadpan' if not gone else 'smug', mouth_=mouth('mort', t),
             look=(1.0, -0.4), lump='sub' if gone else None, gulp=gul if gone else 0.0, lift=0.5 * (1 - gul) if t > 6.7 else 0.0)
    return K.shot(YARD, LT, 740.0, 420.0, Z, acts=[mort, fm_], sx=180, sy=320)


def r_mort_fee(t, u):
    big, a, v = cu(YARD, LT, C.mort, t, 900.0, 300.0, 26.0, (560, 760), Z=1.4, blur=7, flip=True, expr='smug',
                   mouth_=mouth('mort', t), look=(-0.2, -0.1), lump='sub', lift=0.25)
    return big


def r_airboat(t, u):
    """the airboat tears across the sawgrass: prop roar, the braid streams back, Mort clings to the prop cage"""
    Z = 1.15
    bx = lerp(760.0, 300.0, u / 1.07)
    s = S_SW * Z * 0.8
    un = s / (3 * Z)
    acts = [A(C.airboat, bx, WATER, s, flip=True, t=t, spin=t * 50),
            A(C.fm, bx + 10.0 * un, WATER - 7.0 * un, s, flip=True, t=t, pose='sit', expr='cheer', look=(1.0, 0.0), sway=-1.0, hand_n=(12.0, 30.0)),
            A(C.mort, bx + 22.0 * un, WATER - 26.0 * un, S_MORT * Z * 0.8, flip=True, t=t, expr='shock', rot=30.0, pivot=(0.0, 10.0), lump='sub')]
    def f(big, v):
        x, y = v.opt(bx + 30.0, WATER)
        for i in range(10):                                         # spray + speed lines
            B.puff(big, x + i * 40, y - 20 + 20 * math.sin(i + t * 20), 40, 0.5, (236, 248, 255))
        for i in range(12):
            yy = 300 + i * 120
            xx = int((t * 3000 + i * 377) % (OUT_W + 600)) - 300
            big[yy:yy + 8, max(0, xx):max(0, min(OUT_W, xx + 260))] = (250, 250, 250)
    return K.shot(SWAMP, LT, 520.0, 520.0, Z, acts=acts, fx_=f, sx=180, sy=320)


def boat_scene(t, Z, cx, cy, py_pts=None, py_lump=0.0, mort_lump='sub', fm_expr='zen', hand_n=None, mort_kw=None, py=True, fm_mouth=None):
    bx = 520.0
    s = S_SW * Z
    un = s / (3 * Z)
    deck = WATER - 7.0 * un
    acts = [A(C.airboat, bx, WATER, s, t=t, spin=0.0),
            A(C.mort, bx - 22.0 * un, WATER - 29.0 * un, S_MORT * Z * 1.2, t=t, lump=mort_lump, **(mort_kw or {})),
            A(C.fm, bx + 6.0 * un, deck, s, t=t, expr=fm_expr, mouth_=mouth('fm', t) if fm_mouth is None else fm_mouth, look=(0.8, 0.4),
              hand_n=hand_n)]
    if py: acts.append(python_scarf(bx + 6.0 * un, deck, s, t, lump=py_lump, pts=py_pts))
    def f(big, v):
        x, y = v.opt(bx + 30.0 * un, WATER)
        for i in range(5): B.puff(big, x - 60 + i * 30, y + 6, 26, 0.35, (236, 248, 255))
    return K.shot(SWAMP, LT, cx, cy, Z, acts=acts, fx_=f, sx=180, sy=320)


def r_scarf(t, u):
    """a 20-ft python rises out of the water and wraps him like a scarf; he pets it, zen: «Easy, buddy.»"""
    k = sm(min(1.0, u / 0.6))
    n = max(3, int(len(SCARF) * k))
    pts = SCARF[:n]
    return boat_scene(t, 1.45, 540.0, 560.0, py_pts=pts, hand_n=(12.0, 56.0) if u > 0.7 else None)


def r_theft(t, u):
    """the python's head dives into Mort's pouch and swallows the sub (12.75): a sub-shaped bulge slides down the snake"""
    reach = sm(min(1.0, u / 0.5))
    gone = t >= 12.75
    head_end = [(lerp(19.0, -14.0, reach), lerp(60.0, 36.0, reach))]
    pts = SCARF[:-1] + head_end
    return boat_scene(t, 1.45, 520.0, 560.0, py_pts=pts, py_lump=0.95 if gone else 0.0, mort_lump=None if gone else 'sub', fm_expr='stunned',
                      mort_kw=dict(expr='shock' if gone else 'deadpan'))


def r_angry(t, u):
    """CU: for the first time ever — rage, low: «Not the SUB.»"""
    big, a, v = cu(SWAMP, LT, C.fm, t, 520.0, 520.0, 27.0, (540, 820), Z=1.35, blur=6, expr='angry', mouth_=mouth('fm', t), look=(-0.6, 0.0),
                   glasses_drop=0.6)
    fx.vignette(big, 0.45)
    return big


def r_brawl(t, u):
    """a cartoon dust-cloud brawl (limbs, a croc, stars) -> the python tied in a neat bow, alive and offended"""
    Z = 1.3
    if u < 0.42:
        v = view_at(SWAMP, 360.0, 520.0, Z, 180, 320)
        big = v.bg()
        for i in range(10):
            ph = i * 0.63 + t * 9
            B.puff(big, 540 + 220 * math.cos(ph), 1100 + 160 * math.sin(ph * 1.3), 170, 0.95, (226, 214, 180))
        for i in range(5):
            x, y = 540 + 300 * math.cos(t * 13 + i * 1.3), 1000 + 260 * math.sin(t * 11 + i)
            big[int(y) - 10:int(y) + 10, int(x) - 40:int(x) + 40] = [(200, 126, 74), (150, 130, 70), (255, 122, 34)][i % 3]
        K.sparkle(big, 540, 760, t, (255, 236, 96), n=5, r=120)
        B.shake(big, t, 12, 34)
        return big
    s = S_SW * Z
    acts = [A(C.python, 360.0, 620.0, s, t=t, pose='bow', lump=0.4, hiss=0.6 if u > 0.5 else 0.0),
            A(C.fm, 300.0, 615.0, s, t=t, expr='proud', look=(1.0, 0.0), sweat=0.6, shaka=True)]
    return K.shot(SWAMP, LT, 360.0, 520.0, Z, acts=acts, sx=180, sy=320)


def r_fwc(t, u):
    """the FWC python-bounty window: Tanner again (job #7, ranger khaki — an MGMT badge on his lanyard), the cash fan: «A THOUSAND bucks!»"""
    Z = 1.2
    def pre(big, v):
        bg0 = big.copy()
        A(C.tanner, 690.0, 560.0, 13.0 * v.Z, flip=True, t=t, uniform='fwc', jobs=7, expr='chipper', mouth_=mouth('tanner', t, 2.0),
          look=(-0.4, -0.2), hand_n=(12.0, 40.0) if t < 15.4 else (14.0, 50.0))(big, v, LT(v))
        keep_box(big, bg0, v, BWIN)
    acts = [A(C.fm, 500.0, 650.0, S_SW * 1.15 * Z, t=t, expr='content', look=(1.0, 0.3), hand_n=(13.0, 40.0), shadow=0.3),
            A(C.python, 470.0, 650.0, S_SW * 0.8 * Z, t=t, pose='bow', lump=0.4)]
    def f(big, v):
        if t >= 15.4:
            x, y = v.opt(600.0, 430.0)
            cash(big, x, y, 7, min(1.0, (t - 15.4) / 0.2), 1.0)
    return K.shot(BOOTH, LT, 620.0, 430.0, Z, acts=acts, pre=pre, fx_=f, sx=180, sy=320)


def r_rent_money(t, u):
    """CU: happy for the first time all season, the cash fanned out: «RENT money!»"""
    def fx_(big, v, a):
        hx, hy = aout(a, v, 'hand')
        cash(big, hx + 40, hy - 40, 7, 1.0, 1.2)
        K.sparkle(big, 540, 600, t, (255, 236, 96), n=4, r=260)
    big, a, v = cu(BOOTH, LT, C.fm, t, 560.0, 380.0, 26.0, (520, 800), Z=1.35, blur=6, expr='cheer', mouth_=mouth('fm', t), look=(0.6, 0.3),
                   hand_n=(14.0, 56.0), fx_=fx_)
    return big


def r_twist(t, u):
    """TWIST: Tanner rips the ranger shirt off — MGMT polo underneath: «You make python money now? Rent's UP!» — $4,400 on his chest"""
    Z = 1.35
    mgmt = t >= 17.95
    fm_ = A(C.fm, 560.0, 650.0, S_SW * Z, t=t, expr='stunned' if t < 19.4 else 'shock', look=(1.0, 0.0), hand_n=(13.0, 40.0), shadow=0.3)
    tan = A(C.tanner, 700.0, 650.0, S_SW * 1.05 * Z, flip=True, t=t, uniform='mgmt' if mgmt else 'fwc', jobs=7, expr='chipper',
            mouth_=mouth('tanner', t, 2.0), look=(-0.3, -0.1), hand_n=(16.0, 50.0) if t >= 19.3 else (11.0, 62.0), shadow=0.3)
    def f(big, v):
        if 17.82 <= t < 18.2:                                          # the shirt flying off
            x, y = v.opt(700.0, 520.0)
            k_ = (t - 17.82) / 0.38
            big[int(y - 500 * k_) - 60:int(y - 500 * k_) + 60, int(x + 300 * k_) - 90:int(x + 300 * k_) + 90] = (190, 170, 110)
        if t >= 19.4:
            hx, hy = aout(fm_, v, 'head')
            notice(big, hx - 20, hy + 420, 300, t, 19.4, '$4,400/MO', ang=4.0)
        if 17.82 <= t < 19.0: K.sparkle(big, 700, 700, t, (200, 160, 255), n=4, r=200)
    big = K.shot(BOOTH, LT, 630.0, 440.0, Z, acts=[fm_, tan], fx_=f, sx=180, sy=320)
    if u < 0.3 or 19.4 <= t < 19.55: B.shake(big, t, 10, 34)
    return big


def r_whimper(t, u):
    """CU: tiny voice, the notice stuck to his belly: «That's MORE than I made.»"""
    def fx_(big, v, a):
        hx, hy = aout(a, v, 'head')
        notice(big, hx + 40, hy + 760, 420, t, 19.4, '$4,400/MO', ang=4.0)
    big, a, v = cu(BOOTH, LT, C.fm, t, 560.0, 380.0, 26.0, (520, 760), Z=1.35, blur=6, expr='teary', mouth_=mouth('fm', t), look=(0.3, -0.5),
                   fx_=fx_)
    return big


def r_third(t, u):
    """CU: Mort plucks a third of the stack with his bill: «And my THIRD.»"""
    def fx_(big, v, a):
        mx, my = aout(a, v, 'tip')
        cash(big, mx, my + 80, 3, 0.5, 0.8)
    big, a, v = cu(BOOTH, LT, C.mort, t, 700.0, 380.0, 26.0, (540, 760), Z=1.35, blur=6, flip=True, expr='smug', mouth_=mouth('mort', t),
                   look=(-0.2, -0.1), lump='cash', fx_=fx_)
    return big


def r_credit(t, u):
    """the trailer window: the python lounges on HIS couch (the sub bulging), Tanner with the tablet: «Rented it! He's got better CREDIT.»"""
    Z = 1.6
    def pre(big, v):
        bg0 = big.copy()
        x0, y0 = v.opt(WINDOW[0], WINDOW[1]); x1, y1 = v.opt(WINDOW[2], WINDOW[3])
        big[int(y0):int(y1), int(x0):int(x1)] = (60, 50, 70)                            # the dim room inside
        big[int(y1) - 120:int(y1), int(x0):int(x1)] = (170, 80, 90)                     # the couch
        A(C.python, 262.0, 334.0, 6.0 * v.Z, t=t, pose='couch', lump=0.5)(big, v, LT(v))
        A(C.tv_cart, 316.0, 340.0, 4.0 * v.Z, t=t)(big, v, LT(v))
        keep_box(big, bg0, v, WINDOW)
    acts = [A(C.tanner, 400.0, SAND, S_YARD * Z, flip=True, t=t, uniform='mgmt', jobs=7, expr='chipper', mouth_=mouth('tanner', t, 2.0),
              look=(-0.6, 0.3), hand_n=(10.0, 42.0), prop_n=lambda sp, h: C.tablet(sp, (h[0] + 0.5, h[1] - 0.5)), shadow=0.35)]
    return K.shot(YARD, LT, 330.0, 400.0, Z, pre=pre, acts=acts, sx=180, sy=320)


def r_wrists(t, u):
    """MS: zen, he holds both wrists out to Darlene — click (26.60): «Officer. Take me HOME.»"""
    Z = 1.5
    cuffed = t >= 26.6
    acts = [A(C.fm, 600.0, SAND, S_YARD * Z, t=t, expr='zen', mouth_=mouth('fm', t), look=(1.0, 0.2), hand_n=(15.0, 38.0), hand_f=(12.0, 37.0),
              prop_n=(lambda sp, h: C.cuffs(sp, (h[0] - 1.0, h[1] + 4.0))) if cuffed else None, shadow=0.35),
            A(C.darlene, 722.0, SAND, S_YARD * Z, flip=True, t=t, expr='bored', look=(-1.0, -0.3), hand_n=(10.0, 40.0),
              prop_n=lambda sp, h: sp.rect(h[0] - 1.0, h[1] - 1.0, h[0] + 3.0, h[1] + 4.0, (252, 250, 236)), shadow=0.35)]
    return K.shot(YARD, LT, 640.0, 440.0, Z, acts=acts, sx=180, sy=320)


def r_mugshot(t, u):
    big = K.mug_wall()
    sc = 15.0
    sp = FX.draw(C.fm, sc, t=t, expr='cheer', look=(0.0, 0.0), shaka=True)
    px, py = sp.anchors['head']
    blit(big, sp, 540 - px * sc, 720 + py * sc, sc, None)
    K.booking_board(big, 540, 1330, ['MAN, FLORIDA J.', 'PYTHON: CAUGHT', 'SHED: LOST'], w=800)
    fx.vignette(big, 0.25)
    return big


def r_darlene(t, u):
    """CU: Darlene punches the 9th hole: «One more. Then it's FREE.»"""
    big, a, v = cu(YARD, LT, C.darlene, t, 700.0, 400.0, 22.0, (560, 860), Z=1.35, blur=6, flip=True, expr='bored', mouth_=mouth('darlene', t),
                   look=(-0.4, -0.2))
    return big


def r_button(t, u):
    """button: Tanner slaps $4,400 onto the trailer; in the window the python rears up — HSSS?!"""
    Z = 1.7
    rear = t >= 30.95
    def pre(big, v):
        bg0 = big.copy()
        x0, y0 = v.opt(WINDOW[0], WINDOW[1]); x1, y1 = v.opt(WINDOW[2], WINDOW[3])
        big[int(y0):int(y1), int(x0):int(x1)] = (60, 50, 70)
        big[int(y1) - 130:int(y1), int(x0):int(x1)] = (170, 80, 90)
        pts = [(-30.0, 16.0), (-16.0, 14.0), (-2.0, 15.0), (6.0, 20.0), (8.0, 30.0), (10.0, 40.0)] if rear else None
        A(C.python, 262.0, 334.0, 6.0 * v.Z, t=t, pose='couch', pts=pts, lump=0.5, hiss=1.0 if rear else 0.0)(big, v, LT(v))
        keep_box(big, bg0, v, WINDOW)
        if rear:                                                       # the head bursts out through the window at Tanner
            k_ = min(1.0, (t - 30.95) / 0.12)
            A(C.python, 300.0, 330.0, 9.0 * v.Z, t=t, pts=[(-8.0, 0.0), (0.0, 3.0), (8.0 + 6.0 * k_, 5.0), (14.0 + 10.0 * k_, 3.0)], hiss=1.0,
              thick=1.2)(big, v, LT(v))
    acts = [A(C.tanner, 400.0, SAND, S_YARD * Z, flip=True, t=t, uniform='mgmt', jobs=7, expr='chipper', look=(-0.6, 0.0),
              hand_n=(14.0, 58.0) if t >= 30.4 else (10.0, 44.0), shadow=0.35)]
    def f(big, v):
        x, y = v.opt(360.0, 300.0)
        notice(big, x, y, 260, t, 30.45, '$4,400/MO', ang=-3.0)
    big = K.shot(YARD, LT, 320.0, 380.0, Z, pre=pre, acts=acts, fx_=f, sx=180, sy=320)
    if rear and t < 31.15: B.shake(big, t, 10, 34)
    return big


SHOTS = [r_hook, r_tanner, r_hold, r_mort_fee, r_airboat, r_scarf, r_theft, r_angry, r_brawl, r_fwc, r_rent_money, r_twist, r_whimper, r_third,
         r_credit, r_wrists, r_mugshot, r_darlene, r_button]
NAMES = ['hook', 'tanner', 'hold', 'mort_fee', 'airboat', 'scarf', 'theft', 'angry', 'brawl', 'fwc', 'rent_money', 'twist', 'whimper', 'third',
         'credit', 'wrists', 'mugshot', 'darlene', 'button']
CAP = dict(hook=1800, tanner=1800, hold=1780, mort_fee=1640, scarf=1800, theft=1800, angry=1640, fwc=1800, rent_money=1640, twist=1800,
           whimper=1640, third=1640, credit=1800, wrists=1800, darlene=1640, button=1800)


SHOW = K.Show(EPI, 5, ['$3,400 FOR', 'A SHED?!'], hook_t=(0.10, 2.7), hook_y=150, cap_default=1640, cap_y=CAP, hook_size=80,
              stickers=[(K.st('JOB #6', (170, 255, 110), 52), 2.9, 5.2, 300, 420),
                        (K.st('FEE: 1/3', (120, 230, 255), 60), 8.4, 9.4, 760, 520),
                        (K.st('20 FT!', (255, 236, 96), 76), 13.9, 14.2, 540, 420),
                        (K.st('JOB #7', (170, 255, 110), 52), 14.4, 16.4, 300, 420),
                        (K.st('+$1,000', (170, 255, 110), 70), 15.45, 16.4, 760, 560),
                        (K.st('+$1,000/MO', (255, 90, 90), 66), 19.45, 20.18, 540, 380),
                        (K.st('CREDIT: 812', (120, 230, 255), 56), 23.6, 25.15, 700, 420),
                        (K.st('HSSS?!', (255, 90, 90), 76), 31.0, 32.6, 540, 420)],
              chyrons=[(27.1, 28.18, 'FLORIDA MAN CATCHES PYTHON,', 'LOSES SHED TO PYTHON', 1500)],
              cards=[(28.25, 30.3, 9, 28.45, 540, 1180)],
              flashes=[17.82, 27.05, 30.95], mosaics=[9.45])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
