"""S01E04 «Wind or Flood» (09.10.2026) — the Sunsure Mutual letter: PREMIUM $8,000/YR. «EIGHT GRAND?! For a TRAILER?!» Tanner (job #5,
insurance) loads a «BYE, FLORIDA!» truck: «Actually, we're leaving Florida! No worries!» — «Fine. I'll insure MYSELF.» — «Mort. Hold my
sub.» GULP. «Sub's not COVERED.» A card table: FLORIDA MAN MUTUAL $40/YR (*WIND ONLY — the clue), a queue of dropped neighbours, a tiny
cloud in the corner of the sky (the clue). Mort stamps APPROVED with his bill: «Is it legal? It's CHEAPER.» +$400. The tiny cloud floats
over HIS trailer only: rain, knee-deep water, the recliner floats away with an iguana surfing it. TWIST (53 %, bureaucratic recursion —
the hero becomes the system): split screen, Florida Man on both sides of the table — the insurer, with Tanner's grin: «Was it WIND, or
FLOOD?» — the soaked client: «Flood.» — «DENIED!» The neighbours: DENIED, DENIED. Darlene in a robe and curlers: «Flood.» DENIED. She
punches his card anyway: 8/10, «Noted.» Mort: «Congrats. You're the bad guy NOW.» He rewrites the banner $40 -> $8,000 (BREAKING).
Darlene reads it: «EIGHT GRAND?! For a TRAILER?!» Button, the perfect Tanner grin: «No worries!»  -> loop to the hook.
  python3 ep04.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
from timeline import DUR, FPS, VOICE, SLUG, CUTS, STAMPS

EPI = Episode('ep04', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
K.SLOGAN[:] = ['DENIED?', 'WE DENY BACK.']
YARD = K.world_baked('yard')
A, wpt, aout = K.A, K.wpt, K.aout
LT = K.light_sun
SAND = 626.0
CHAIR = (806.0, 476.0)
TABLE = 512.0                      # the card table (world x) in front of the trailer
CLOUD = (470.0, 300.0)             # where the tiny cloud parks: right over Florida Man (world)
S_YARD, S_TBL, S_MORT = 10.0, 10.5, 7.0
QUEUE = [('retiree', 655.0), ('tank', 705.0)]
DAR_X = 760.0


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


# ------------------------------------------------------------------ weather (only over him)
def tiny_cloud(big, v, wx, wy, t, k=1.0, dark=0.0):
    """a tiny grumpy rain cloud (world position), stepped puffs, darker underside"""
    z = v.Z * 3 * k
    x, y = v.opt(wx, wy)
    top = np.array((236, 238, 244)) * (1 - dark) + np.array((120, 126, 140)) * dark
    for dx, dy, r in ((-22, 4, 16), (0, -6, 20), (22, 2, 15), (-8, 8, 14), (12, 9, 14)):
        B.puff(big, x + dx * z, y + dy * z, r * z, 1.0, tuple(int(c) for c in top))
    for dx in (-18, -4, 10, 22):
        B.puff(big, x + dx * z, y + 14 * z, 10 * z, 1.0, (110, 116, 130))
    if dark > 0.5:                                                    # an angry little face
        big[int(y + 2 * z):int(y + 5 * z), int(x - 9 * z):int(x - 5 * z)] = (40, 44, 56)
        big[int(y + 2 * z):int(y + 5 * z), int(x + 5 * z):int(x + 9 * z)] = (40, 44, 56)


def rain(big, v, wx, wy0, wy1, t, w=60.0):
    """rain streaks from the cloud down to the ground, only in a narrow column (world)"""
    x0, y0 = v.opt(wx - w, wy0); x1, y1 = v.opt(wx + w, wy1)
    r = np.random.default_rng(5)
    n = int(60 * (x1 - x0) / 400)
    for i in range(max(1, n)):
        xx = int(x0 + r.random() * (x1 - x0))
        yy = int(y0 + ((t * 2600 + r.random() * 3000) % max(1, (y1 - y0))))
        big[yy:min(int(y1), yy + 48), xx:xx + 6] = (170, 210, 255)


def flood(big, v, wx, level, t, w=110.0):
    """knee-deep water in a puddle only around him: blue with stepped white wave crests (world level = water surface y)"""
    x0, y0 = v.opt(wx - w, level); x1, y1 = v.opt(wx + w, SAND + 18)
    x0, x1 = int(max(0, x0)), int(min(OUT_W, x1)); y0, y1 = int(max(0, y0)), int(min(OUT_H, y1))
    if x0 >= x1 or y0 >= y1: return
    reg = big[y0:y1, x0:x1].astype(np.float32)
    big[y0:y1, x0:x1] = (reg * 0.4 + np.array((60, 140, 200)) * 0.6).astype(np.uint8)
    for xx in range(x0, x1, 24):
        dy = int(8 * math.sin(xx * 0.03 + t * 6))
        big[max(0, y0 + dy):max(0, y0 + dy + 10), xx:xx + 18] = (236, 248, 255)


_STAMP = {}


def stamp_img(word, col=(226, 34, 52), size=64):
    key = (word, size)
    if key not in _STAMP:
        f = O.pfont(size); bb = f.getbbox(word); tw, th = bb[2] - bb[0], bb[3] - bb[1]
        im = Image.new('RGBA', (tw + 70, th + 60), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
        d.rectangle([5, 5, tw + 64, th + 54], outline=col + (255,), width=10)
        d.text((35 - bb[0], 30 - bb[1]), word, font=f, fill=col + (255,))
        im = im.rotate(-9, resample=Image.NEAREST, expand=True)
        _STAMP[key] = np.array(im)
    return _STAMP[key]


def stamp(big, word, cx, cy, t, t0, col=(226, 34, 52), size=64):
    """a rubber stamp slammed onto the screen at t0 (big -> normal)"""
    if t < t0: return
    a = stamp_img(word, col, size)
    k = min(1.0, (t - t0) / 0.08)
    sc = 1.6 - 0.6 * k
    im = Image.fromarray(a).resize((int(a.shape[1] * sc), int(a.shape[0] * sc)), Image.NEAREST)
    a2 = np.array(im)
    O.overlay(big, a2, int(cx - a2.shape[1] / 2), int(cy - a2.shape[0] / 2), min(1.0, 0.3 + k))


def letter(big, x, y, w=560, ang=6.0):
    K.invoice_card(big, x, y, w, ang=ang, amount='$8,000', head='SUNSURE MUTUAL', lines=('YOUR NEW PREMIUM:', 'PER YEAR. ENJOY!'),
                   hc=(226, 140, 20))


def table_act(v, t, price='$40/YR'):
    return A(C.card_table, TABLE, SAND, S_TBL * v.Z, t=t, price=price)


# ================================================================== shots
def r_hook(t, u):
    """XCU: the Sunsure letter in his hands, the trailer behind: «EIGHT GRAND?! For a TRAILER?!»"""
    def pre(big, v):
        K.heat_haze(big, t, 0, OUT_H, 4)
    big, a, v = cu(YARD, LT, C.fm, t, 330.0, 360.0, 30.0, (540, 820), Z=1.35, blur=6, pre_=pre, expr='shriek', mouth_=mouth('fm', t),
                   sweat=0.8, glasses_drop=min(1.0, 0.3 + u / 0.8), look=(0.0, -0.4))
    letter(big, 230, 1250)
    if u < 0.5: B.shake(big, t, 9, 33)
    return big


def r_truck(t, u):
    """MS: Tanner (job #5, Sunsure yellow polo) loads the «BYE, FLORIDA!» truck and waves: «Actually, we're leaving Florida!»"""
    Z = 0.9                                                      # the whole «BYE, FLORIDA!» banner in frame
    wave = (11.0 + 2.0 * math.sin(t * 12), 64.0) if u > 1.1 else (12.0, 40.0)
    acts = [A(C.truck, 940.0, SAND, 26.0 * Z, t=0.0, shadow=0.3),
            A(C.tanner, 700.0, SAND + 4, S_YARD * 1.15 * Z, flip=True, t=t, uniform='insurance', jobs=5, expr='chipper',
              mouth_=mouth('tanner', t, 2.0), look=(-0.2, 0.0), hand_n=wave, shadow=0.35,
              prop_f=lambda sp, h: sp.rect(h[0] - 4.0, h[1] - 2.0, h[0] + 3.0, h[1] + 4.0, (196, 150, 96)))]
    def f(big, v):
        K.heat_haze(big, t, 1300, OUT_H, 3)
    return K.shot(YARD, LT, 866.0, 430.0, Z, acts=acts, fx_=f, sx=180, sy=320)


def r_dust(t, u):
    """the truck roars off (horn), dust swallows him; zen from inside the cloud: «Fine. I'll insure MYSELF.»"""
    Z = 1.35
    tx = 900.0 + 900.0 * min(1.0, u / 1.6) ** 1.6
    acts = [A(C.truck, tx, SAND, 26.0 * Z, t=t, shadow=0.3),
            A(C.fm, 600.0, SAND, S_YARD * 1.15 * Z, t=t, expr='zen', mouth_=mouth('fm', t), look=(0.6, 0.0), shadow=0.35)]
    def f(big, v):
        dust = max(0.0, 1.0 - u / 2.6)
        x, y = v.opt(640.0, SAND - 30)
        for i in range(9):
            ph = (t * 0.5 + i / 9) % 1.0
            B.puff(big, x - 420 + i * 110 + 60 * ph, y - 80 * ph, 120 + 80 * ph, 0.55 * dust, (226, 206, 160))
    return K.shot(YARD, LT, 640.0, 430.0, Z, acts=acts, fx_=f, sx=180, sy=320)


def r_mort_hold(t, u):
    """MS: «Mort. Hold my sub.» — Mort on the lawn-chair back swallows it whole (9.80)"""
    Z = 1.1                                                      # Mort's whole billboard behind them
    gone = t >= 9.8
    gul = min(1.0, max(0.0, (t - 9.8) / 0.3))
    fm_ = A(C.fm, 742.0, SAND, S_YARD * Z, t=t, expr='zen', mouth_=mouth('fm', t), look=(0.8, 0.5),
            hand_n=(15.0, 48.0), prop_n=None if gone else (lambda sp, h: C.sub(sp, (h[0] + 1.0, h[1] + 1.0), ang=0.2)), shadow=0.35)
    mort = A(C.mort, CHAIR[0], CHAIR[1], S_MORT * Z, flip=True, t=t, expr='deadpan' if not gone else 'smug', mouth_=mouth('mort', t),
             look=(1.0, -0.4), lump='sub' if gone else None, gulp=gul if gone else 0.0, lift=0.5 * (1 - gul) if t > 9.4 else 0.0)
    return K.shot(YARD, LT, 852.0, 420.0, Z, acts=[mort, fm_], sx=180, sy=320)


def r_mort_cu(t, u):
    big, a, v = cu(YARD, LT, C.mort, t, 900.0, 300.0, 26.0, (560, 760), Z=1.4, blur=7, flip=True, expr='deadpan',
                   mouth_=mouth('mort', t), look=(-0.2, -0.1), lump='sub', lift=0.25)
    return big


def queue_acts(v, t, wet=0.0, dar_expr='bored'):
    acts = [A(C.local, x, SAND - 4.0, S_YARD * v.Z, t=t, kind=k, pose='stand', expr='content', flip=True, shadow=0.3) for k, x in QUEUE]
    acts.append(A(C.darlene, DAR_X, SAND, S_YARD * v.Z, flip=True, t=t, robe=True, wet=wet, expr=dar_expr, mouth_=mouth('darlene', t),
                  look=(-1.0, 0.0), shadow=0.3))
    return acts


def r_setup(t, u):
    """WIDE: FLORIDA MAN MUTUAL — a card table, a queue of dropped neighbours (Darlene in a robe), a tiny cloud in the corner (clue)"""
    Z = 1.25
    v = view_at(YARD, 566.0, 470.0, Z, 180, 320)               # the whole «FLORIDA MAN MUTUAL» banner in frame
    acts = [A(C.fm, TABLE + 14.0, SAND - 10.0, S_YARD * Z, t=t, expr='proud', tie=True, look=(1.0, 0.0), hand_n=(12.0, 36.0)), table_act(v, t)]
    acts += queue_acts(v, t)
    def f(big, v_):
        tiny_cloud(big, v_, 520.0, 250.0, t, 0.7)
    return K.shot(YARD, LT, 566.0, 470.0, Z, acts=acts, fx_=f, sx=180, sy=320)


def r_stamp(t, u):
    """MS: Mort on the table stamps the forms with his bill — APPROVED, APPROVED; the cash pile grows: «Is it legal? It's CHEAPER.»"""
    Z = 1.6
    peck = any(s - 0.12 <= t < s + 0.05 for s in STAMPS[:3])
    acts = [A(C.fm, TABLE + 14.0, SAND - 10.0, S_YARD * Z, t=t, expr='proud', tie=True, look=(1.0, -0.4), hand_n=(12.0, 36.0)), table_act(v=view_at(YARD, 540.0, 450.0, Z, 180, 320), t=t),
            A(C.mort, TABLE - 10.0, SAND - 16.0 * S_TBL / 3.0, S_MORT * Z * 1.3, t=t, expr='smug', mouth_=mouth('mort', t), look=(0.0, 0.0),
              cam=not peck, lift=0.0, rot=25.0 if peck else 0.0, pivot=(0.0, 0.0))]
    def f(big, v_):
        for i, s in enumerate(STAMPS[:3]):
            stamp(big, 'APPROVED', 270 + i * 260, 560 + (i % 2) * 110, t, s, (40, 160, 80), 44)
        n = sum(1 for s in STAMPS[:3] if t >= s)
        x, y = v_.opt(TABLE + 60.0, SAND - 16.0 * S_TBL / 3.0)
        for q in range(n * 3):                                          # the cash pile
            big[int(y) - 30 - q * 16:int(y) - 14 - q * 16, int(x) - 60:int(x) + 60] = (90, 170, 90) if q % 2 else (60, 140, 70)
    return K.shot(YARD, LT, 540.0, 450.0, Z, acts=acts, fx_=f, sx=180, sy=320)


def r_cloud(t, u):
    """the tiny cloud drifts over HIS trailer only, darkens — thunder (15.10), a bolt"""
    Z = 1.1
    k = sm(min(1.0, u / 0.5))
    cx_, cy_ = lerp(330.0, CLOUD[0], k), lerp(140.0, CLOUD[1] - 120.0, k)
    acts = [A(C.fm, TABLE + 14.0, SAND - 10.0, S_YARD * Z, t=t, expr='stunned', tie=True, look=(0.2, 1.0)), table_act(view_at(YARD, 480.0, 400.0, Z, 180, 320), t)]
    def f(big, v):
        tiny_cloud(big, v, cx_, cy_, t, 1.1, dark=min(1.0, u / 0.4))
        if 0.05 <= u < 0.22:
            x, y = v.opt(cx_, cy_ + 20)
            for q in range(6):
                big[int(y + q * 60):int(y + q * 60 + 60), int(x + (q % 2) * 26 - 12):int(x + (q % 2) * 26 + 6)] = (255, 250, 160)
            O.flash(big, 0.35)
        if u > 0.35: rain(big, v, cx_, cy_ + 20, SAND, t, 70.0)
    return K.shot(YARD, LT, 480.0, 400.0, Z, acts=acts, fx_=f, sx=180, sy=320)


def r_flood(t, u):
    """rain only on him: the water rises knee-deep; the recliner floats past with an iguana surfing it"""
    Z = 1.25
    v = view_at(YARD, 520.0, 430.0, Z, 180, 320)
    lvl = SAND - 30.0 * min(1.0, 0.4 + u / 1.0)
    rx = lerp(380.0, 650.0, u / 1.05)
    acts = [A(C.fm, TABLE + 14.0, SAND - 10.0, S_YARD * Z, t=t, expr='sad', tie=True, wet=1.0, look=(0.6, -0.4)),
            table_act(v, t),
            A(C.recliner, rx, lvl + 6.0, S_YARD * Z, t=t, foot=0.5, rot=6.0 * math.sin(t * 4), pivot=(0.0, 0.0)),
            A(C.iguana, rx + 4.0, lvl + 6.0 - 15.0 * S_YARD / 3.0, S_YARD * 0.9 * Z, t=t, look=(1.0, 0.0), rot=-8.0 * math.sin(t * 4), pivot=(0.0, 0.0))]
    def f(big, v_):
        tiny_cloud(big, v_, CLOUD[0], CLOUD[1] - 120.0, t, 1.1, dark=1.0)
        rain(big, v_, CLOUD[0], CLOUD[1] - 100.0, SAND, t, 110.0)
        flood(big, v_, CLOUD[0], lvl, t, 170.0)
    return K.shot(YARD, LT, 520.0, 430.0, Z, acts=acts, fx_=f, sx=180, sy=320)


def half(frame, side):
    return frame[:, 270:810] if side == 0 else frame[:, 270:810]


def split_insurer(t, speaking=True, stamp_down=False):
    Z = 1.45
    v = view_at(YARD, 540.0, 440.0, Z, 180, 320)
    acts = [A(C.fm, TABLE + 14.0, SAND - 10.0, S_YARD * Z, t=t, expr='chipper', tie=True, mouth_=mouth('fm', t) if speaking else 0.0,
              look=(1.0, 0.0), hand_n=(12.0, 46.0 if not stamp_down else 34.0), shadow=0.3), table_act(v, t)]
    return K.shot(YARD, LT, 540.0, 440.0, Z, acts=acts, sx=180, sy=320)


def split_client(t, speaking=False):
    Z = 1.45
    lvl = SAND - 30.0
    acts = [A(C.fm, 600.0, SAND, S_YARD * Z, flip=True, t=t, expr='sad', wet=1.0, mouth_=mouth('fm', t) if speaking else 0.0, look=(-1.0, -0.2),
              sweat=0.0, shadow=0.0)]
    def f(big, v):
        tiny_cloud(big, v, 600.0, 300.0, t, 1.0, dark=1.0)
        rain(big, v, 600.0, 330.0, SAND, t, 90.0)
        flood(big, v, 600.0, lvl, t, 150.0)
    return K.shot(YARD, LT, 600.0, 440.0, Z, acts=acts, fx_=f, sx=180, sy=320)


def split(big_l, big_r):
    out = np.empty_like(big_l)
    out[:, :540] = big_l[:, 270:810]
    out[:, 540:] = big_r[:, 270:810]
    out[:, 532:548] = (250, 250, 244)
    return out


def r_twist(t, u):
    """TWIST: split screen — the same man on both sides of the table: the insurer (tie, Tanner's grin) vs the soaked client"""
    big = split(split_insurer(t), split_client(t))
    if u < 0.3: B.shake(big, t, 8, 30)
    return big


def r_client(t, u):
    """CU: the soaked client, tiny voice: «Flood.»"""
    def fx_(big, v, a):
        rain(big, v, 600.0, 200.0, 700.0, t, 200.0)
    big, a, v = cu(YARD, LT, C.fm, t, 600.0, 380.0, 26.0, (540, 820), Z=1.35, blur=6, flip=True, expr='sad', wet=1.0, mouth_=mouth('fm', t),
                   look=(-0.8, -0.2), fx_=fx_)
    return big


def r_denied(t, u):
    """split again: the insurer slams the stamp — DENIED over the client"""
    big = split(split_insurer(t, stamp_down=t >= STAMPS[3]), split_client(t))
    stamp(big, 'DENIED', 810, 900, t, STAMPS[3], size=56)
    return big


def r_queue(t, u):
    """MS: the neighbours in line, dripping — DENIED, DENIED"""
    Z = 1.25
    v = view_at(YARD, 660.0, 430.0, Z, 180, 320)
    acts = queue_acts(v, t, wet=1.0)
    def f(big, v_):
        for (k_, x), s in zip(QUEUE, STAMPS[4:6]):
            ox, oy = v_.opt(x, SAND - 120.0)
            stamp(big, 'DENIED', ox, oy, t, s, size=44)
    return K.shot(YARD, LT, 660.0, 430.0, Z, acts=acts, fx_=f, sx=180, sy=320)


def r_darlene(t, u):
    """CU: Darlene in a pink robe and curlers, dripping: «Flood.» — DENIED; she punches his card anyway: 8/10, «Noted.»"""
    big, a, v = cu(YARD, LT, C.darlene, t, 700.0, 400.0, 22.0, (560, 860), Z=1.35, blur=6, flip=True, robe=True, wet=1.0,
                   expr='bored', mouth_=mouth('darlene', t), look=(-0.8, -0.2))
    stamp(big, 'DENIED', 540, 600, t, STAMPS[6], size=56)
    return big


def r_mort_bad(t, u):
    """CU: Mort perched on the card table, to camera: «Congrats. You're the bad guy NOW.»"""
    big, a, v = cu(YARD, LT, C.mort, t, 520.0, 380.0, 26.0, (540, 780), Z=1.35, blur=6, expr='deadpan', mouth_=mouth('mort', t),
                   look=(0.0, 0.0), cam=True, lump='sub')
    return big


_BAN = {}


def r_banner(t, u):
    """insert: he crosses out $40/YR on the banner and paints $8,000/YR"""
    if 'b' not in _BAN:
        im = Image.new('RGB', (OUT_W, OUT_H), (120, 200, 210)); d = ImageDraw.Draw(im); d.fontmode = '1'
        d.rectangle([40, 300, 1040, 1300], fill=(236, 226, 196)); d.rectangle([40, 300, 1040, 316], fill=(200, 186, 150))
        d.text((90, 380), 'FLORIDA MAN', font=O.pfont(76), fill=(226, 34, 52))
        d.text((90, 520), 'MUTUAL', font=O.pfont(76), fill=(20, 120, 130))
        d.text((90, 700), 'NO QUESTIONS', font=O.pfont(44), fill=(14, 44, 54))
        d.text((90, 1220), '*WIND ONLY', font=O.pfont(30), fill=(226, 34, 52))
        _BAN['b'] = np.array(im)
    big = _BAN['b'].copy()
    im = Image.fromarray(big); d = ImageDraw.Draw(im); d.fontmode = '1'
    d.text((90, 880), '$40/YR', font=O.pfont(84), fill=(14, 44, 54))
    k = min(1.0, u / 0.35)
    if k > 0: d.rectangle([80, 920, 80 + int(560 * k), 948], fill=(226, 34, 52))
    if u > 0.4:
        s = '$8,000/YR'
        n = int(min(len(s), (u - 0.4) / 0.5 * len(s)))
        d.text((90, 1020), s[:n], font=O.pfont(84), fill=(226, 34, 52))
    big = np.array(im)
    return big


def r_d3(t, u):
    """CU: Darlene reads the new price — shrieks the hook word for word: «EIGHT GRAND?! For a TRAILER?!»"""
    big, a, v = cu(YARD, LT, C.darlene, t, 640.0, 400.0, 24.0, (540, 820), Z=1.35, blur=6, flip=True, robe=True, wet=0.6,
                   expr='shock', mouth_=mouth('darlene', t), look=(-0.8, 0.0), chew=False)
    if u < 0.4: B.shake(big, t, 8, 30)
    return big


def r_button(t, u):
    """button: the perfect Tanner grin on Florida Man, tie on, shaka: «No worries!»"""
    big, a, v = cu(YARD, LT, C.fm, t, 520.0, 380.0, 27.0, (540, 800), Z=1.35, blur=6, expr='chipper', tie=True, mouth_=mouth('fm', t) * 0.6,
                   look=(0.0, 0.0), shaka=u > 0.3)
    K.sparkle(big, 640, 1020, t, (255, 255, 255), n=4, r=50)
    return big


SHOTS = [r_hook, r_truck, r_dust, r_mort_hold, r_mort_cu, r_setup, r_stamp, r_cloud, r_flood, r_twist, r_client, r_denied, r_queue, r_darlene,
         r_mort_bad, r_banner, r_d3, r_button]
NAMES = ['hook', 'truck', 'dust', 'mort_hold', 'mort_cu', 'setup', 'stamp', 'cloud', 'flood', 'twist', 'client', 'denied', 'queue', 'darlene',
         'mort_bad', 'banner', 'd3', 'button']
CAP = dict(hook=1800, truck=1800, dust=1800, mort_hold=1780, mort_cu=1640, setup=1800, stamp=1780, twist=1780, client=1640, denied=1780,
           darlene=1640, mort_bad=1640, banner=1700, d3=1640, button=1640)


SHOW = K.Show(EPI, 4, ['$8,000', 'INSURANCE?!'], hook_t=(0.10, 2.38), hook_y=150, cap_default=1640, cap_y=CAP, hook_size=80,
              stickers=[(K.st('JOB #5', (170, 255, 110), 52), 2.6, 5.0, 300, 420),
                        (K.st('*WIND ONLY', (255, 120, 120), 48), 12.0, 12.9, 560, 1300),
                        (K.st('+$400', (170, 255, 110), 70), 14.3, 15.0, 760, 420),
                        (K.st('WIND OR FLOOD?', (255, 236, 96), 52), 17.1, 18.9, 540, 380),
                        ],
              chyrons=[(26.62, 27.6, 'FLORIDA MAN DENIES', 'OWN CLAIM', 1500)],
              cards=[(22.3, 23.72, 8, 22.5, 540, 1380)],
              flashes=[16.95, STAMPS[3]], mosaics=[26.28])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
