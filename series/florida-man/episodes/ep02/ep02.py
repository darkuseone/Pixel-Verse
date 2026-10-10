"""S01E02 «Grand Theft Sub» (09.10.2026) — the Pubbix deli: a chicken tender sub is $14.99. «FIFTEEN BUCKS?! For a SUB?!» Tanner (job #2,
deli): «Fourteen ninety-NINE. Totally different!» — «Mort. Hold my—» (no sub: he couldn't afford one) — Mort on the deli scale
(18.2 LB = $72.80): «No sub. This is an EMERGENCY.» — «Nine-one-one? I'd like to report a ROBBERY.» Pull back: Deputy Darlene was in the
line behind him all along, with a coupon from 2019: «Mornin', [DING-DONG]. Prices aren't a CRIME.» She squints at the board… her gum
falls out. TWIST (56 %, the hunter takes the hero's side): «Hands where I can SEE 'em!» — she handcuffs the PRICE TAG. «That's Pubbix
PROPERTY!» — «So's my PAYCHECK.» Mort: «I'm representing the price now. Pays BETTER.» Mugshot of the price tag (front / profile = a thin
line), BREAKING chyron, FREQUENT GUEST 6/10. Tanner: «New price! Covers legal FEES!» ($16.99). Button: «Nine-one-one? Me again.»
  python3 ep02.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
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

EPI = Episode('ep02', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
DELI = K.world_baked('deli')
AISLE = K.world_baked('aisle')
A, wpt, aout = K.A, K.wpt, K.aout
LT = K.light_deli
TOP = 346.0                        # the counter's steel lip (world y): things stand on it, people behind it are hidden below it
FLOOR = 680.0                      # customers' feet in front of the counter
TAN_Y = 530.0                      # Tanner's (hidden) feet behind the counter
SCALE = (962.0, 321.0)             # the deli scale's platform (Mort stands on it)
TAG = (700.0, 347.0)               # the «SUB $14.99» price sign on the counter lip
LCD = (929, 262, 996, 286)         # the scale's display (world box)
# people scale per depth (output px per sprite px at Z=1): the counter is 1.3 m, the eye level ~1.1 m (floor perspective of the bg)
S_FRONT, S_BACK, S_MORT, S_TAG = 20.0, 11.5, 9.1, 7.0


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
    return big, a, v0


def occlude(big, bg0, v):
    """the deli case hides whatever stands behind it: restore the background below the counter lip"""
    oy = int(max(0, v.opt(0, TOP - 1.0)[1]))
    x0 = int(max(0, v.opt(88.0, 0)[0])); x1 = int(min(OUT_W, v.opt(1212.0, 0)[0]))
    if oy < OUT_H and x0 < x1: big[oy:, x0:x1] = bg0[oy:, x0:x1]


def tanner_behind(v, t, x, **kw):
    """Tanner (deli whites, paper hat, apron) behind the counter, facing the customers (left)"""
    kw.setdefault('expr', 'chipper'); kw.setdefault('look', (0.0, 0.0))
    return A(C.tanner, x, TAN_Y, S_BACK * v.Z, flip=True, t=t, uniform='deli', jobs=2, mouth_=mouth('tanner', t, 2.0), **kw)


def tag_act(v, t, x=TAG[0], **kw):
    return A(C.price_tag, x, TAG[1], S_TAG * v.Z, t=t, **kw)


def mort_scale(v, t, **kw):
    kw.setdefault('expr', 'deadpan'); kw.setdefault('look', (0.6, -0.2))
    return A(C.mort, *SCALE, S_MORT * v.Z, flip=True, t=t, mouth_=mouth('mort', t), **kw)


def deli_shot(t, cx, cy, Z, back=(), acts=(), fx_=None):
    """a deli view: `back` actors stand behind the counter (occluded by it), `acts` on / in front of it"""
    def pre(big, v):
        if Z >= 1.2:                                             # depth of field: the huge menu board on the wall goes soft
            yb = int(min(OUT_H, max(0, v.opt(0, TOP - 6.0)[1])))      # (no sharp half-cut prices behind stickers / heads)
            if yb > 0: big[:yb] = K.dof(big[:yb].copy(), min(14, 7 + (Z - 1.2) * 6))
        bg0 = big.copy()
        lt = LT(v)
        for b in back: b(v)(big, v, lt)
        occlude(big, bg0, v)
    v = view_at(DELI, cx, cy, Z, 180, 320)
    return K.shot(DELI, LT, cx, cy, Z, acts=[a(v) for a in acts], pre=pre, fx_=fx_, sx=180, sy=320)


_FG = {}


def counter_fg(big, y0, blur=3):
    """the deli case in the foreground of a close-up behind the counter (Tanner CU): steel lip + glass + trays, soft"""
    if 'c' not in _FG:
        crop = DELI[338:500, 300:760]
        im = Image.fromarray(crop).resize((OUT_W, int(OUT_W * crop.shape[0] / crop.shape[1])), Image.NEAREST)
        _FG['c'] = K.dof(np.array(im), blur)
    a = _FG['c']
    h = min(a.shape[0], OUT_H - y0)
    if h > 0: big[y0:y0 + h] = a[:h]


def trays_fg(big, y0, blur=4):
    """inside the case looking out: meat trays across the bottom of the frame"""
    if 't' not in _FG:
        crop = DELI[392:484, 140:572]
        im = Image.fromarray(crop).resize((OUT_W, int(OUT_W * crop.shape[0] / crop.shape[1])), Image.NEAREST)
        _FG['t'] = K.dof(np.array(im), blur)
    a = _FG['t']
    h = min(a.shape[0], OUT_H - y0)
    if h > 0: big[y0:y0 + h] = a[:h]


def blit_sprite(big, fn, x, y, sc, lt=None, flip=False, **kw):
    sp = FX.draw(fn, sc, flip=flip, **kw)
    blit(big, sp, x, y, sc, lt, flip)
    return sp


def siren(big, t, k=1.0):
    K.siren(big, t, k)


# ================================================================== shots
def r_hook(t, u):
    """from INSIDE the deli case: Florida Man's face against the glass, shrieking at the «SUB $14.99» sign; breath fog, glare, meat
    trays in the foreground"""
    v = view_at(AISLE, 640.0, 400.0, 1.2, 180, 320)
    big = K.dof(v.bg(), 10)
    lt = LT(v)
    sc = 30.0
    push = 1.0 + 0.05 * min(1.0, u / 2.6)
    sp = FX.draw(C.fm, sc * push, t=t, expr='shriek', mouth_=mouth('fm', t), sweat=0.6, glasses_drop=min(1.0, 0.2 + u / 1.2), look=(0.7, -0.6),
                 hand_n=(17.0, 60.0))
    px, py = sp.anchors['head']
    ox, oy = 470 - px * sc * push, 800 + py * sc * push
    blit(big, sp, ox, oy, sc * push, lt)
    mx, my = sp.anchors['mouth']
    fx_, fy_ = ox + mx * sc * push, oy - my * sc * push
    breath = 0.25 + 0.15 * math.sin(t * 6.0)                       # breath fog on the glass, stepped
    yy, xx = np.ogrid[0:OUT_H, 0:OUT_W]
    d = ((xx - fx_ - 40) / 230.0) ** 2 + ((yy - fy_ - 20) / 150.0) ** 2
    a = np.floor(np.clip(1.0 - d, 0, 1) * 3) / 3 * breath
    big[:] = (big * (1 - a[..., None]) + np.array((240, 248, 250)) * a[..., None]).astype(np.uint8)
    big[:] = (big * 0.9 + np.array((200, 236, 240)) * 0.1).astype(np.uint8)  # the glass tint
    for k_, (x0, w) in enumerate(((140, 70), (300, 26), (760, 90))):          # glare streaks
        for y in range(0, OUT_H, 12):
            xa = int(x0 + y * 0.35)
            if xa < OUT_W: big[y:y + 12, xa:min(OUT_W, xa + w)] = (big[y:y + 12, xa:min(OUT_W, xa + w)] * 0.75 + 64).astype(np.uint8)
    trays_fg(big, 1660)
    big[1640:1664] = (200, 210, 220); big[1640:1646] = (240, 244, 250)
    blit_sprite(big, C.price_tag, 790, 1630, 11.0, lt, t=t)
    if u < 0.5: B.shake(big, t, 9, 33)
    return big


def r_tanner(t, u):
    """MS: Tanner behind the counter in deli whites + paper hat, beaming, a wrapped sub held up; the menu board above: $14.99"""
    Z = 1.8
    return deli_shot(t, 830.0, 250.0, Z,
                     back=[lambda v: tanner_behind(v, t, 800.0, hand_n=(10.0, 56.0), prop_n=lambda sp, h: C.sub(sp, (h[0] + 1.0, h[1] + 1.0), ang=0.3))],
                     acts=[lambda v: tag_act(v, t), lambda v: mort_scale(v, t, look=(1.0, -0.3))])


def r_reach(t, u):
    """MS: zen Florida Man at the counter reaches his hand out to Mort standing on the deli scale: «Mort. Hold my—»"""
    Z = 0.98
    k = sm(min(1.0, u / 0.6))
    return deli_shot(t, 850.0, 360.0, Z,
                     back=[lambda v: tanner_behind(v, t, 690.0, look=(-0.6, 0.0))],
                     acts=[lambda v: tag_act(v, t), lambda v: mort_scale(v, t, look=(1.0, -0.5)),
                           lambda v: A(C.fm, 850.0, FLOOR, S_FRONT * v.Z, t=t, expr='zen', mouth_=mouth('fm', t), look=(0.6, 0.6),
                                       hand_n=(lerp(12.0, 15.0, k), lerp(34.0, 60.0, k)), shadow=0.3)])


def r_hand(t, u):
    """CU: he looks down at his open hand — no sub (he couldn't afford one)"""
    sc = lerp(25.0, 28.0, min(1.0, u / 1.3))
    big, a, v = cu(DELI, LT, C.fm, t, 820.0, 260.0, sc, (470, 860), Z=1.35, blur=6, expr='stunned', mouth_=mouth('fm', t),
                   look=(0.7, -0.8), hand_n=(17.0, 46.0))
    return big


def r_mort_scale(t, u):
    """the deli scale insert: Mort standing on it to camera, grave: «No sub. This is an EMERGENCY.»; the LCD reads 18.2 LB  $72.80"""
    Z = 2.0
    def f(big, v):
        x0, y0 = v.opt(LCD[0], LCD[1]); x1, y1 = v.opt(LCD[2], LCD[3])
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        big[y0 - 8:y1 + 8, x0 - 8:x1 + 8] = (150, 156, 166)
        big[y0:y1, x0:x1] = (30, 52, 40)
        lcd_text(big, x0, y0, x1, y1)
    return deli_shot(t, 930.0, 250.0, Z, acts=[lambda v: tag_act(v, t), lambda v: mort_scale(v, t, look=(0.0, 0.0), cam=True)], fx_=f)


_LCD = {}


def lcd_text(big, x0, y0, x1, y1):
    key = (x1 - x0, y1 - y0)
    if key not in _LCD:
        from PIL import ImageDraw
        w, h = key
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
        f1, f2 = O.pfont(max(12, h // 5)), O.pfont(max(16, h // 3))
        d.text((12, 8), '18.2 LB', font=f1, fill=(140, 255, 160, 255))
        bb = f2.getbbox('$72.80')
        d.text((w - 12 - (bb[2] - bb[0]) - bb[0], h - 10 - (bb[3] - bb[1]) - bb[1]), '$72.80', font=f2, fill=(140, 255, 160, 255))
        _LCD[key] = np.array(im)
    O.overlay(big, _LCD[key], x0, y0, 1.0)


def r_phone(t, u):
    """CU: perfectly calm, flip phone to the cheek: «Nine-one-one? I'd like to report a ROBBERY.»"""
    big, a, v = cu(DELI, LT, C.fm, t, 640.0, 260.0, 26.0, (500, 820), Z=1.35, blur=6, expr='zen', mouth_=mouth('fm', t), look=(0.6, 0.2),
                   hand_n=(12.0, 55.0), prop_n=lambda sp, h: C.flip_phone(sp, (h[0] - 0.4, h[1] + 0.6)))
    return big


def r_reveal(t, u):
    """MS on the phone at the counter… pull back + pan: Deputy Darlene has been standing in line right behind him (2019 coupon)"""
    k = sm(min(1.0, max(0.0, (t - 14.5) / 0.7)))
    Z = lerp(1.25, 0.94, k); cx = lerp(860.0, 730.0, k)
    fm_ = lambda v: A(C.fm, 830.0, FLOOR, S_FRONT * v.Z, t=t, expr='zen', mouth_=mouth('fm', t), look=(0.6, 0.2), hand_n=(12.0, 55.0),
                      prop_n=lambda sp, h: C.flip_phone(sp, (h[0] - 0.4, h[1] + 0.6)), shadow=0.3)
    dar = lambda v: A(C.darlene, 590.0, FLOOR, S_FRONT * v.Z, t=t, expr='bored', mouth_=mouth('darlene', t), look=(1.0, 0.1),
                      hand_n=(9.0, 40.0), prop_n=C.coupon, shadow=0.3)
    return deli_shot(t, cx, 340.0, Z, back=[lambda v: tanner_behind(v, t, 700.0, look=(-0.5, 0.0))],
                     acts=[lambda v: tag_act(v, t), lambda v: mort_scale(v, t, look=(1.0, -0.5)), dar, fm_])


def r_darlene_cu(t, u):
    """CU: Darlene, bored, chewing: «Prices aren't a CRIME.»"""
    big, a, v = cu(DELI, LT, C.darlene, t, 600.0, 260.0, 22.0, (560, 860), Z=1.35, blur=7, expr='bored', mouth_=mouth('darlene', t),
                   look=(0.8, 0.2))
    return big


def r_board(t, u):
    """her POV: the board, CHICKEN TENDER SUB $14.99 — the lids narrow into a squint"""
    Z = lerp(2.4, 2.8, min(1.0, u / 0.45))
    v = view_at(DELI, 912.0, 150.0, Z, 180, 320)               # the whole «$14.99» in frame (price column of the menu board)
    big = v.bg()
    x, y = v.opt(944.0, 116.0)
    fx.glow(big, int(x), int(y), 220, (255, 80, 80), 0.35 + 0.25 * math.sin(t * 30))
    lid = int(lerp(0, 640, sm(min(1.0, u / 0.4))))
    big[:lid] = (40, 20, 18); big[OUT_H - lid:] = (40, 20, 18)
    return big


def r_gum(t, u):
    """XCU: her jaw drops — the gum falls out of her mouth"""
    big, a, v = cu(DELI, LT, C.darlene, t, 600.0, 260.0, 30.0, (540, 760), Z=1.4, blur=7, expr='shock', mouth_=0.9, chew=False,
                   look=(0.8, 0.5))
    mx, my = aout(a, v, 'mouth')
    yy = my + 40 + 2600 * u * u
    if yy < OUT_H - 40:
        B.puff(big, mx, yy, 46, 1.0, (255, 120, 190))
        B.puff(big, mx - 12, yy - 14, 16, 1.0, (255, 210, 235))
    return big


def r_twist(t, u):
    """TWIST: Darlene snatches the PRICE TAG off the counter, holds it up and snaps the handcuffs on it; police lights; Tanner frozen"""
    Z = 1.6
    cuffed = t >= 17.95
    up = u >= 0.15
    dar = A(C.darlene, 598.0, FLOOR, S_FRONT * Z, t=t, expr='shout', mouth_=mouth('darlene', t), look=(1.0, 0.2) if up else (1.0, -0.5),
            hand_n=(13.0, 57.0) if up else (15.0, 50.0), chew=False, shadow=0.3)
    def f(big, v):
        if up:
            hx, hy = aout(dar, v, 'hand')
            sc = S_TAG * Z * 1.05
            blit_sprite(big, C.price_tag, hx + 4 * sc, hy + 4 * sc, sc, LT(v), t=t, cuffed=cuffed)
        siren(big, t)
    acts = [] if up else [lambda v: tag_act(v, t)]
    big = deli_shot(t, 690.0, 320.0, Z, back=[lambda v: tanner_behind(v, t, 790.0, expr='shock', look=(-0.6, -0.4), hand_n=(9.0, 60.0), hand_f=(-3.0, 60.0))],
                    acts=acts + [lambda v: dar], fx_=f)
    if u < 0.35: B.shake(big, t, 12, 36)
    return big


def r_tanner_panic(t, u):
    """CU: Tanner behind the counter, hands up, chipper panic: «That's Pubbix PROPERTY!»"""
    def fx_(big, v, a):
        counter_fg(big, 1500)
        siren(big, t, 0.6)
    big, a, v = cu(DELI, LT, C.tanner, t, 760.0, 240.0, 22.0, (540, 760), Z=1.35, blur=6, flip=True, expr='panic', uniform='deli', jobs=2,
                   mouth_=mouth('tanner', t, 2.0), look=(0.0, 0.0), hand_n=(10.0, 64.0), hand_f=(-4.0, 64.0), fx_=fx_)
    return big


def r_darlene_flat(t, u):
    """CU: Darlene guards her prisoner (the cuffed tag on the counter), flat: «So's my PAYCHECK.»"""
    def fx_(big, v, a):
        siren(big, t, 0.35)
    big, a, v = cu(DELI, LT, C.darlene, t, 640.0, 300.0, 22.0, (400, 820), Z=1.35, blur=6, expr='bored', mouth_=mouth('darlene', t),
                   look=(0.0, 0.0), hand_n=(8.0, 40.0), hand_f=(-2.0, 40.0), fx_=fx_,
                   extra=[tag_act(view_at(DELI, 640.0, 300.0, 1.35, 180, 320), t, cuffed=True)])
    return big


def r_mort_rep(t, u):
    """MS on the counter lip: Mort has hopped next to his new client (the cuffed tag), to camera: «I'm representing the price now.
    Pays BETTER.» — cha-ching: cash in the pouch"""
    Z = 1.9
    hop = max(0.0, 1.0 - u / 0.3)
    return deli_shot(t, 750.0, 290.0, Z, back=[lambda v: tanner_behind(v, t, 640.0, expr='nervous', look=(1.0, 0.0))],
                     acts=[lambda v: tag_act(v, t, cuffed=True),
                           lambda v: A(C.mort, 790.0, TOP - 40.0 * hop * (1 - hop) * 4, S_MORT * v.Z, flip=True, t=t, expr='smug',
                                       mouth_=mouth('mort', t), look=(0.0, 0.0), cam=True, lump='cash' if t > 24.45 else None)])


def r_mugshot(t, u):
    """FLASH: the price tag's booking photo — front, then (FLASH) profile: a thin line; chyron + FREQUENT GUEST 6/10 (overlays)"""
    big = K.mug_wall()
    side = t >= 25.8
    sc = 22.0
    blit_sprite(big, C.price_tag, 540, 1080, sc, None, t=t, cuffed=True, side=side)
    K.booking_board(big, 540, 1290, ['PRICE, SUB', 'AKA $14.99', 'GRAND THEFT SUB'], w=800)
    fx.vignette(big, 0.25)
    return big


def r_new_price(t, u):
    """MS: Tanner puts up the new tag — $16.99 — thumbs up: «New price! Covers legal FEES!»"""
    Z = 1.6
    placed = t >= 27.1
    thumbs = t >= 27.6
    def f(big, v):
        if not placed:
            sp = FX.draw(C.price_tag, S_TAG * Z * 1.1, t=t, price='$16.99')
            x, y = v.opt(690.0, lerp(300.0, 340.0, sm(min(1.0, u / 0.45))))
            blit(big, sp, x, y, S_TAG * Z * 1.1, LT(v))
    acts = [lambda v: mort_scale(v, t, look=(-1.0, -0.4), lump='cash')]
    if placed: acts.append(lambda v: tag_act(v, t, price='$16.99'))
    return deli_shot(t, 780.0, 290.0, Z,
                     back=[lambda v: tanner_behind(v, t, 790.0, thumbs=thumbs, hand_n=None if thumbs else (14.0, 46.0))], acts=acts, fx_=f)


def r_button(t, u):
    """button: Florida Man, zen, phone to the cheek again: «Nine-one-one? Me again.»"""
    big, a, v = cu(DELI, LT, C.fm, t, 720.0, 260.0, 27.0, (520, 800), Z=1.35, blur=6, expr='zen', mouth_=mouth('fm', t), look=(0.4, 0.0),
                   hand_n=(12.0, 55.0), prop_n=lambda sp, h: C.flip_phone(sp, (h[0] - 0.4, h[1] + 0.6)))
    return big


SHOTS = [r_hook, r_tanner, r_reach, r_hand, r_mort_scale, r_phone, r_reveal, r_darlene_cu, r_board, r_gum, r_twist, r_tanner_panic,
         r_darlene_flat, r_mort_rep, r_mugshot, r_new_price, r_button]
NAMES = ['hook', 'tanner', 'reach', 'hand', 'mort_scale', 'phone', 'reveal', 'darlene_cu', 'board', 'gum', 'twist', 'tanner_panic',
         'darlene_flat', 'mort_rep', 'mugshot', 'new_price', 'button']
CAP = dict(hook=1800, tanner=1800, reach=1800, hand=1700, mort_scale=1780, phone=1640, reveal=1800, darlene_cu=1640, board=1640,
           gum=1640, twist=1800, tanner_panic=1380, darlene_flat=1700, mort_rep=1800, mugshot=1640, new_price=1800, button=1640)


SHOW = K.Show(EPI, 2, ['$15 FOR', 'A SUB?!'], hook_t=(0.10, 2.55), hook_y=150, cap_default=1640, cap_y=CAP, hook_size=84,
              stickers=[(K.st('JOB #2', (170, 255, 110), 52), 2.75, 4.95, 260, 520),
                        (K.st('NO SUB?!', (255, 236, 96), 70), 7.15, 8.2, 760, 520),
                        (K.st('MORT: $72.80', (120, 230, 255), 52), 8.5, 11.1, 540, 420),
                        (K.st('COUPON: EXP. 2019', (255, 236, 96), 44), 14.85, 15.5, 330, 1290),
                        (K.st('*DING-DONG*', (255, 255, 255), 64), 15.02, 15.55, 540, 330),
                        (K.st('UNDER ARREST', (255, 90, 90), 70), 17.75, 18.9, 540, 380),
                        (K.st('NEW CLIENT', (120, 230, 255), 56), 22.3, 24.9, 330, 470),
                        (K.st('+$2 LEGAL FEES', (170, 255, 110), 56), 27.6, 28.75, 540, 420)],
              chyrons=[(25.0, 26.62, 'SUB PRICE ARRESTED', 'FOR ROBBERY', 1500)],
              cards=[(25.85, 26.62, 6, 26.15, 540, 370)],
              flashes=[17.55, 24.98, 25.8], mosaics=[])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
