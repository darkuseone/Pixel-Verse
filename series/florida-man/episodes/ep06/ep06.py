"""S01E06 «Jail & Resort» (season finale, 09.10.2026). Night, a searchlight: Florida Man climbs the county-jail fence INTO the jail with a
suitcase and a pool noodle: «Jail's CHEAPER than RENT!» Darlene, megaphone: «You're breaking IN?!» — «Checkin' in.» (BREAKING: FLORIDA MAN
BREAKS INTO JAIL). The booking desk: card 9/10, she punches the tenth — jackpot, confetti, FREE NIGHT (*fees may apply — the clue): «Ten.
Free night. Whoopee.» Bliss: «Free A/C. Free food. NO premium.» The VIP cell: a mint on the pillow, a towel swan, a tiny window A/C. He offers
Mort a sub: «I'm FULL.» — Mort spits out the season's five subs and the $14.99 tag. Tanner (job #8, concierge vest, eight badges): «Welcome to
Sunshine County JAIL! Under new management!» TWIST (51 %, the reward is the same problem): «Night's free! Plus a forty-nine dollar RESORT
fee!» — the wall sign flips to JAIL & RESORT. «It's a JAIL.» — «Jail-and-RESORT!» — «Towel's ten. Mint's five. Pillow's a SUBSCRIPTION.»
The tiny A/C rattles and dies (the E01 sound): «Oh! A/C's extra. Nine GRAND.» SEASON LOOP: the E01 first frame — «NINE GRAND?! For the
A/C?!» Button: Mort, «My client pleads. FLORIDA.» (gavel). Tag: retirees fly over the jail in a V, honking — SEASON 2: SNOWBIRDS.
  python3 ep06.py test 1 5 20 | frame 12 | all [4]      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image, ImageDraw
from stage import view_at, OUT_W, OUT_H, Light
from scene import sm, lerp
import overlays as O
import fx
from episode import Episode
from props import fmpix as FX
from props import fmcast as C
from props import fmkit as K
from props import decals as D
from props import bytfx as B
from props.dibspix import blit
from timeline import DUR, FPS, VOICE, SLUG, CUTS

EPI = Episode('ep06', VOICE, DUR, FPS, colors=K.COL, slug=SLUG)
talk = EPI.talk
A, wpt, aout = K.A, K.wpt, K.aout
LC = K.light_cell

JAIL = K.wcopy(K.world('jail_ext'))                  # its sign «SUNSHINE COUNTY / JAIL & RESORT» is a decal (props/fmdecor.py)
BOOK = K.world('booking')


def _cell(resort):
    """the cell with a banner over the bunk: «SUNSHINE COUNTY / JAIL» -> «JAIL & RESORT» + five gold stars (hi-res decal, text fitted)"""
    W = K.wcopy(K.world('cell'))
    lines = ['SUNSHINE COUNTY', 'JAIL & RESORT' if resort else 'JAIL']
    img = D.plate(372, 74, lines, bg=(246, 240, 220), colors=[(14, 44, 54), (226, 34, 52) if resort else (14, 44, 54)],
                  border=(14, 44, 54), bw=4, weights=[1.0, 1.3], pad=3, wear=0.3)
    D.attach(W, [(img, 104, 30)])
    if resort: D.attach(W, [(D.knockout(D.plate(180, 16, ['★ ★ ★ ★ ★'], bg=(0, 0, 0), fg=(255, 206, 70), border=None, pad=0.5)), 200, 106)])
    return W


CELL_A, CELL_B = _cell(False), _cell(True)
FENCE = (400.0, 350.0)               # where he straddles the top of the jail fence (world)
LOT = 650.0                          # parking lot, feet
COUNTER, BEHIND = 368.0, 520.0       # booking: counter top / feet behind the counter
BUNK = (430.0, 470.0)                # feet end of the lower bunk mattress (E01)
AC = (640.0, 238.0)                  # the tiny A/C wedged into the barred window (world, bottom centre)
S_FENCE, S_LOT, S_DESK, S_FRONT, S_CELL = 5.0, 12.0, 13.0, 20.0, 15.0


def light_night(v):
    """night: cold blue ambient, the searchlight as a warm key from the upper right"""
    return Light(amb=(0.66, 0.72, 0.96), keys=[(*v.opt(1040.0, 40.0), 1400 * v.Z, (255, 240, 190), 0.55)], rim=(1, -1, (255, 236, 180), 0.5),
                 grad=(1.0, 0.86))


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


def siren(big, t, k=1.0):
    K.siren(big, t, k)


def spotlight(big, x, y, r, a=0.35):
    fx.glow(big, int(x), int(y), int(r), (255, 244, 200), a)


def sub_spr(sp, t=0.0, ang=0.0):
    C.sub(sp, (0.0, 4.0), ang=ang)


def blit_sprite(big, fn, x, y, sc, lt=None, flip=False, **kw):
    sp = FX.draw(fn, sc, flip=flip, **kw)
    blit(big, sp, x, y, sc, lt, flip)
    return sp


def fence_fm(v, t, expr='cheer', **kw):
    """straddling the top of the fence: suitcase in one hand, pool noodle under the other arm"""
    s = S_FENCE * v.Z
    un = s / (3 * v.Z)
    return A(C.fm, FENCE[0], FENCE[1] + 15.0 * un, s, t=t, pose='sit', expr=expr, look=(0.6, 0.4), hand_n=(14.0, 40.0), hand_f=(-6.0, 34.0),
             prop_n=lambda sp, h: C.suitcase(sp, h), prop_f=lambda sp, h: C.noodle(sp, h), **kw)


# ================================================================== shots
def r_hook(t, u, siren_k=0.5):
    """night, searchlight, siren: on top of the jail fence — climbing IN, suitcase in hand, pool noodle: «Jail's CHEAPER than RENT!»"""
    def pre(big, v):
        spotlight(big, 560, 760, 700, 0.35)
    def fx_(big, v, a):
        for k in range(-6, 14):                                         # the chain-link fence in the foreground (he is on top of it)
            x0 = k * 120
            for y in range(1320, OUT_H, 12):
                xa = int(x0 + (y - 1320) * 0.6) % (OUT_W + 240) - 120
                xb = int(x0 + 120 - (y - 1320) * 0.6) % (OUT_W + 240) - 120
                for xx in (xa, xb):
                    if 0 <= xx < OUT_W - 10: big[y:y + 12, xx:xx + 10] = (150, 156, 170)
        big[1300:1330] = (110, 116, 130)
        if siren_k: siren(big, t, siren_k)
    big, a, v = cu(JAIL, light_night, C.fm, t, 420.0, 300.0, 27.0, (520, 760), Z=1.35, blur=5, pre_=pre, fx_=fx_, expr='cheer',
                   mouth_=mouth('fm', t), look=(0.6, 0.3), hand_n=(17.0, 44.0), hand_f=(-6.0, 34.0),
                   prop_n=lambda sp, h: C.suitcase(sp, h), prop_f=lambda sp, h: C.noodle(sp, h))
    if u < 0.4: B.shake(big, t, 8, 30)
    return big


def r_megaphone(t, u):
    """the parking lot: Darlene with a megaphone under the searchlight, baffled: «You're breaking IN?!»"""
    Z = 1.35
    v = view_at(JAIL, 520.0, 420.0, Z, 180, 320)
    acts = [fence_fm(v, t, expr='cheer'),
            A(C.cruiser, 760.0, LOT + 30.0, S_LOT * 1.15 * Z, flip=True, t=t, lights=True, shadow=0.3),
            A(C.darlene, 600.0, LOT + 40.0, S_LOT * Z, t=t, expr='shout', mouth_=mouth('darlene', t), look=(-0.6, 0.8), flip=True, megaphone=True,
              hand_n=(11.0, 54.0), chew=False, shadow=0.3)]
    def f(big, v_):
        siren(big, t, 0.6)
    return K.shot(JAIL, light_night, 520.0, 420.0, Z, acts=acts, fx_=f, sx=180, sy=320)


def r_checkin(t, u):
    """CU: perched on the fence, cheerful drawl: «Checkin' in.»"""
    def fx_(big, v, a):
        spotlight(big, 540, 820, 500, 0.25)
    big, a, v = cu(JAIL, light_night, C.fm, t, 420.0, 300.0, 26.0, (540, 800), Z=1.35, blur=6, expr='content', mouth_=mouth('fm', t),
                   look=(-0.4, -0.5), hand_n=(14.0, 40.0), prop_n=lambda sp, h: C.suitcase(sp, h), fx_=fx_)
    return big


def r_desk(t, u):
    """the booking desk: he slaps the FREQUENT GUEST card down; Darlene behind the counter, hole punch up"""
    Z = 1.2
    def pre(big, v):
        bg0 = big.copy()
        A(C.darlene, 640.0, BEHIND, S_DESK * v.Z, flip=True, t=t, expr='bored', mouth_=mouth('darlene', t), look=(-0.8, -0.4),
          hand_n=(12.0, 56.0))(big, v, LC(v))
        oy = int(v.opt(0, COUNTER)[1]); x0 = int(max(0, v.opt(190.0, 0)[0])); x1 = int(min(OUT_W, v.opt(1062.0, 0)[0]))
        big[oy:, x0:x1] = bg0[oy:, x0:x1]
    slap = t >= 4.95
    acts = [A(C.fm, 470.0, 700.0, S_FRONT * Z, t=t, expr='proud', look=(1.0, -0.2), hand_n=(17.0, 46.0) if slap else (12.0, 52.0),
              prop_n=lambda sp, h: sp.rect(h[0] - 1.0, h[1] - 0.5, h[0] + 5.0, h[1] + 2.5, (255, 244, 214)), shadow=0.3)]
    return K.shot(BOOK, LC, 600.0, 400.0, Z, acts=acts, pre=pre, sx=180, sy=320)


def r_card(t, u):
    """insert: the tenth hole — jackpot: lights, confetti, FREE NIGHT!; fine print *FEES MAY APPLY (the clue)"""
    v = view_at(BOOK, 640.0, 330.0, 1.5, 180, 320)
    big = K.dof(v.bg(), 9)
    if t >= 6.55:
        on = int(t * 8) % 2
        for i in range(10):
            x = 60 + i * 108
            big[120:150, x:x + 60] = (255, 206, 70) if (i + on) % 2 else (226, 34, 52)
            big[1770:1800, x:x + 60] = (255, 206, 70) if (i + on + 1) % 2 else (40, 196, 196)
    K.punch_card(big, t, 6.40, 10, 540, 900, w=900, punch_t=6.55)
    if t >= 6.55:
        im = Image.new('RGBA', (600, 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
        d.text((0, 6), '*FEES MAY APPLY', font=O.pfont(22), fill=(226, 34, 52, 255))
        O.overlay(big, np.array(im), 600, 1180, 1.0)
        r = np.random.default_rng(1)
        for i in range(70):
            x = int(r.random() * OUT_W); sp_ = 600 + r.random() * 900
            y = int(-60 + (t - 6.55) * sp_ + r.random() * 300) % (OUT_H + 100) - 50
            c = [(255, 86, 160), (40, 196, 196), (255, 236, 96), (170, 255, 110)][i % 4]
            big[max(0, y):max(0, y + 22), x:x + 14] = c
    return big


def r_bliss(t, u):
    """CU: pure bliss — the tiny A/C humming behind him: «Free A/C. Free food. NO premium.»"""
    big, a, v = cu(CELL_A, LC, C.fm, t, 800.0, 260.0, 26.0, (520, 820), Z=1.35, blur=6, expr='bliss', mouth_=mouth('fm', t) * 0.6,
                   look=(0.0, 0.5))
    return big


def ac_act(v, t, dead=False, rattle=0.0):
    return A(C.ac_unit, AC[0] + rattle * math.sin(t * 60), AC[1], 4.6 * v.Z, t=t, dead=dead, fan=0.0 if dead else t * 20)


def vip_props(big, v, t):
    """a mint on the pillow and a towel swan on the bunk (world-anchored, screen-space shapes)"""
    x, y = v.opt(120.0, 440.0)
    z = v.Z * 3
    big[int(y - 6 * z):int(y), int(x):int(x + 16 * z)] = (60, 170, 120)
    big[int(y - 6 * z):int(y - 4 * z), int(x):int(x + 16 * z)] = (236, 248, 240)
    sx, sy = v.opt(320.0, 440.0)
    B.puff(big, sx, sy - 10 * z, 16 * z, 1.0, (250, 250, 246))
    big[int(sy - 34 * z):int(sy - 10 * z), int(sx + 8 * z):int(sx + 12 * z)] = (250, 250, 246)
    big[int(sy - 36 * z):int(sy - 32 * z), int(sx + 8 * z):int(sx + 18 * z)] = (250, 250, 246)


def bunk_fm(t, Z, expr='bliss', **kw):
    s_ = S_CELL * Z
    un = s_ / (3 * Z)
    return A(C.fm, BUNK[0], BUNK[1] - 9.0 * un, s_, t=t, expr=expr, rot=90.0, pivot=(0.0, 0.0), look=(-0.6, 0.6), shadow=0.0, **kw)


def r_vip(t, u):
    """the VIP cell: mint on the pillow, a towel swan, the tiny window A/C — he flops onto the bunk"""
    Z = 0.92
    v = view_at(CELL_A, 400.0, 360.0, Z, 180, 320)
    def f(big, v_):
        vip_props(big, v_, t)
        x, y = v_.opt(AC[0], AC[1])
        for i in range(4):
            for q in range(10):
                yy = int(y + q * 22); xx = int(x - 90 + i * 60 + 22 * math.sin(t * 20 + q * 0.6 + i))
                if 0 <= xx < OUT_W - 14 and 0 <= yy < OUT_H: big[yy:yy + 20, xx:xx + 12] = [(255, 86, 160), (40, 196, 196)][i % 2]
    big = K.shot(CELL_A, LC, 400.0, 360.0, Z, acts=[ac_act(v, t), bunk_fm(t, Z) if t >= 10.75 else
                                                   A(C.fm, 470.0, 560.0, S_CELL * Z, t=t, expr='bliss', look=(-1.0, 0.3), rot=-20.0 * min(1.0, u / 0.2),
                                                     pivot=(0.0, 0.0))], fx_=f, sx=180, sy=320)
    if 10.75 <= t < 10.9: B.shake(big, t, 8, 30)
    return big


def r_mort_full(t, u):
    """CU: Mort on the bunk post, green around the bill: «I'm FULL.» — out fly the season's five subs and the $14.99 tag"""
    spit = t >= 13.65
    big, a, v = cu(CELL_A, LC, C.mort, t, 500.0, 300.0, 24.0, (600, 800), Z=1.35, blur=6, expr='nervous' if not spit else 'shock',
                   mouth_=mouth('mort', t), look=(-0.3, 0.0), lump='sub' if not spit else None, gulp=0.6 if 13.3 <= t < 13.65 else 0.0)
    tx, ty = aout(a, v, 'tip')
    if not spit:                                                          # his hand offering yet another sub from the left
        blit_sprite(big, sub_spr, 120, 1250, 20.0, None, ang=0.1)
    else:
        k = t - 13.65
        for i in range(6):
            tt = k - i * 0.06
            if tt <= 0: continue
            x = tx - 900 * tt * (0.6 + 0.15 * i) ; y = ty + 300 * tt - 50 + 2600 * tt * tt
            if y > OUT_H + 100: y = OUT_H - 120 - (i % 3) * 40; x = 160 + i * 140
            if i < 5: blit_sprite(big, sub_spr, x, y, 14.0, None, ang=0.4 * i)
            else: blit_sprite(big, C.price_tag, x, y, 8.0, None, t=t, cuffed=True)
    return big


def tanner_cell(v, t, x=700.0, **kw):
    kw.setdefault('expr', 'chipper'); kw.setdefault('look', (-0.4, 0.0))
    return A(C.tanner, x, 560.0, S_CELL * v.Z, flip=True, t=t, uniform='warden', jobs=8, mouth_=mouth('tanner', t, 2.0), shadow=0.35, **kw)


def r_bars(t, u):
    """the cell door clangs open: Tanner (job #8, black concierge vest, eight badges) sweeps in: «Welcome to Sunshine County JAIL!»"""
    Z = 1.0
    v = view_at(CELL_A, 470.0, 360.0, Z, 180, 320)
    x = lerp(860.0, 640.0, sm(min(1.0, u / 0.6)))
    def f(big, v_):
        vip_props(big, v_, t)
    return K.shot(CELL_A, LC, 470.0, 360.0, Z, acts=[bunk_fm(t, Z, expr='content'),
                                                    tanner_cell(v, t, x, walk=t * 8 if u < 0.6 else None, hand_n=(11.0, 62.0) if u > 0.6 else None)],
                  fx_=f, sx=180, sy=320)


def r_welcome_cu(t, u):
    big, a, v = cu(CELL_A, LC, C.tanner, t, 640.0, 260.0, 22.0, (560, 760), Z=1.35, blur=6, flip=True, expr='chipper', uniform='warden', jobs=8,
                   mouth_=mouth('tanner', t, 2.0), look=(0.0, 0.0), thumbs=u > 0.4, hand_n=(11.0, 50.0) if u > 0.4 else None)
    return big


def r_twist(t, u):
    """TWIST: «Night's free! Plus a forty-nine dollar RESORT fee!» — KA-CHING, the wall sign flips: JAIL & RESORT"""
    Z = 1.0
    world = CELL_B if t >= 18.7 else CELL_A
    v = view_at(world, 300.0, 330.0, Z, 180, 320)
    acts = [bunk_fm(t, Z, expr='shock' if t >= 18.65 else 'content'),
            tanner_cell(v, t, 430.0, hand_n=(12.0, 44.0), prop_n=lambda sp, h: C.tablet(sp, (h[0] + 0.5, h[1] - 0.5)))]
    def f(big, v_):
        vip_props(big, v_, t)
        if 18.65 <= t < 19.4: K.sparkle(big, 330, 260, t, (255, 236, 96), n=4, r=200)
    big = K.shot(world, LC, 300.0, 330.0, Z, acts=acts, fx_=f, sx=180, sy=320)
    if u < 0.3 or 18.65 <= t < 18.85: B.shake(big, t, 9, 32)
    return big


def r_flat(t, u):
    big, a, v = cu(CELL_B, LC, C.fm, t, 300.0, 300.0, 26.0, (540, 820), Z=1.35, blur=6, expr='deadpan', mouth_=mouth('fm', t), look=(0.6, 0.0))
    return big


def r_resort(t, u):
    big, a, v = cu(CELL_B, LC, C.tanner, t, 640.0, 260.0, 22.0, (560, 760), Z=1.35, blur=6, flip=True, expr='chipper', uniform='warden', jobs=8,
                   mouth_=mouth('tanner', t, 2.0), look=(0.0, 0.0), thumbs=True, hand_n=(11.0, 50.0))
    K.sparkle(big, 760, 600, t, (255, 236, 96), n=4, r=80)
    return big


def r_tablet(t, u):
    """MS: Tanner reads the price list off the tablet — each item pops: TOWEL $10, MINT $5, PILLOW $9.99/MO"""
    Z = 1.3
    v = view_at(CELL_B, 380.0, 330.0, Z, 180, 320)
    acts = [bunk_fm(t, Z, expr='stunned'), tanner_cell(v, t, 560.0, hand_n=(12.0, 50.0), prop_n=lambda sp, h: C.tablet(sp, (h[0] + 0.5, h[1] - 0.5)),
                                                     look=(-0.2, -0.6))]
    def f(big, v_):
        vip_props(big, v_, t)
    return K.shot(CELL_B, LC, 380.0, 330.0, Z, acts=acts, fx_=f, sx=180, sy=320)


def r_ac_dies(t, u):
    """insert: the tiny window A/C — rattles, coughs smoke and dies (the E01 sound); the ribbons drop"""
    Z = 2.2
    dead = t >= 25.75
    v = view_at(CELL_B, AC[0], 120.0, Z, 180, 320)
    def f(big, v_):
        x, y = v_.opt(AC[0], AC[1])
        for i in range(4):
            L = 10 if not dead else 3
            for q in range(L):
                yy = int(y + q * 26); xx = int(x - 110 + i * 70 + (0 if dead else 26 * math.sin(t * 22 + q * 0.6 + i)))
                if 0 <= xx < OUT_W - 16 and 0 <= yy < OUT_H: big[yy:yy + 24, xx:xx + 14] = [(255, 86, 160), (40, 196, 196)][i % 2]
        if t >= 25.4: K.smoke(big, x + 60, y - 200, t, n=6, rise=400, size=70, a=0.55)
    big = K.shot(CELL_B, LC, AC[0], 120.0, Z, acts=[ac_act(v, t, dead=dead, rattle=0.0 if dead else 1.2)], fx_=f, sx=180, sy=320)
    if 25.48 <= t < 25.8: B.shake(big, t, 10, 30)
    return big


def r_tanner_9k(t, u):
    """CU: Tanner, casual: «...A/C's extra. Nine GRAND.» — the tablet reads $9,000"""
    big, a, v = cu(CELL_B, LC, C.tanner, t, 640.0, 260.0, 22.0, (600, 760), Z=1.35, blur=6, flip=True, expr='chipper', uniform='warden', jobs=8,
                   mouth_=mouth('tanner', t, 2.0), look=(-0.2, 0.0), hand_n=(12.0, 50.0), prop_n=lambda sp, h: C.tablet(sp, (h[0] + 0.5, h[1] - 0.5)))
    return big


def r_loop(t, u):
    """SEASON LOOP: exactly the E01 first frame — sweat, the glasses slide: «NINE GRAND?! For the A/C?!»"""
    def pre(big, v):
        ac_act(v, t, dead=True)(big, v, LC(v))
        x, y = v.opt(AC[0], AC[1] - 30)
        K.smoke(big, x, y, t, n=5, rise=300, size=50, a=0.45)
        K.heat_haze(big, t, 0, OUT_H, 5)
    big, a, v = cu(CELL_B, LC, C.fm, t, 900.0, 280.0, 30.0, (540, 820), Z=1.35, blur=6, pre_=pre, expr='shriek', mouth_=mouth('fm', t),
                   sweat=1.0, glasses_drop=min(1.0, 0.3 + u / 0.8), look=(0.0, 0.2))
    K.invoice_card(big, 450, 1290, 580, ang=7.0, amount='$9,000', head='JAIL & RESORT', lines=('A/C (OPTIONAL)', 'RESORT FEE: $49'), hc=(150, 110, 200))
    if u < 0.5: B.shake(big, t, 9, 33)
    return big


def r_button(t, u):
    """button: Mort to camera, the defence rests — «My client pleads. FLORIDA.» — gavel"""
    big, a, v = cu(CELL_B, LC, C.mort, t, 300.0, 300.0, 26.0, (560, 760), Z=1.35, blur=7, expr='deadpan', mouth_=mouth('mort', t),
                   look=(0.0, 0.0), cam=True)
    if 32.15 <= t < 32.3: B.shake(big, t, 8, 30)
    return big


_S2 = {}


def r_snowbirds(t, u):
    """tag: night over the jail — retirees in visors fly south in a V, honking like geese: SEASON 2: SNOWBIRDS"""
    Z = 1.0
    v = view_at(JAIL, 640.0, 360.0, Z, 180, 320)
    big = K.shot(JAIL, light_night, 640.0, 360.0, Z, acts=[], sx=180, sy=320)
    kinds = ['retiree', 'curlers', 'grandpa', 'retiree', 'curlers']
    for i, k in enumerate(kinds):
        off = abs(i - 2)
        x = -300 + 1700 * (u / 1.44) - off * 200
        y = 470 + off * 150 + 20 * math.sin(t * 6 + i)
        blit_sprite(big, C.flyer, x, y, 13.0, None, t=t + i * 0.3, kind=k)
    if 'h' not in _S2:
        _S2['h'] = K.hook_title(['SEASON 2:', 'SNOWBIRDS'], 84, depth=16)
    k = min(1.0, max(0.0, (t - 32.9) / 0.15))
    if k > 0: O.overlay(big, _S2['h'], 0, 1150, k)
    return big


SHOTS = [r_hook, r_megaphone, r_checkin, r_desk, r_card, r_bliss, r_vip, r_mort_full, r_bars, r_welcome_cu, r_twist, r_flat, r_resort, r_tablet,
         r_ac_dies, r_tanner_9k, r_loop, r_button, r_snowbirds]
NAMES = ['hook', 'megaphone', 'checkin', 'desk', 'card', 'bliss', 'vip', 'mort_full', 'bars', 'welcome_cu', 'twist', 'flat', 'resort', 'tablet',
         'ac_dies', 'tanner_9k', 'loop', 'button', 'snowbirds']
CAP = dict(hook=1780, megaphone=1380, checkin=1640, desk=1800, card=1500, bliss=1640, vip=1800, mort_full=1640, bars=1800, welcome_cu=1640,
           twist=1800, flat=1640, resort=1640, tablet=1800, ac_dies=1640, tanner_9k=1640, loop=1800, button=1640)


SHOW = K.Show(EPI, 6, ["JAIL'S", 'CHEAPER?!'], hook_t=(0.10, 1.86), hook_y=150, cap_default=1640, cap_y=CAP, hook_size=88,
              stickers=[(K.st('FREE NIGHT!', (255, 236, 96), 76), 6.6, 8.5, 540, 380),
                        (K.st('SUBS RETURNED: 5', (120, 230, 255), 52), 13.75, 14.25, 540, 380),
                        (K.st('JOB #8', (170, 255, 110), 56), 14.5, 17.4, 300, 420),
                        (K.st('RESORT FEE?!', (255, 90, 90), 70), 18.7, 20.3, 540, 1200),
                        (K.st('TOWEL $10', (170, 255, 110), 52), 23.05, 25.45, 300, 520),
                        (K.st('MINT $5', (170, 255, 110), 52), 23.75, 25.45, 780, 640),
                        (K.st('PILLOW $9.99/MO', (255, 236, 96), 52), 24.45, 25.45, 540, 780),
                        (K.st('104°F', (255, 120, 90), 70), 25.9, 26.5, 540, 1200),
                        (K.st('$9,000', (255, 90, 90), 70), 26.9, 27.6, 760, 1240)],
              chyrons=[(2.0, 3.55, 'FLORIDA MAN BREAKS', 'INTO JAIL', 1500)],
              flashes=[17.45, 18.65, 27.65], mosaics=[18.7, 32.66])


def render(t):
    i = max(k for k in range(len(SHOTS)) if CUTS[k] <= t) if t < DUR else len(SHOTS) - 1
    u = t - CUTS[i]
    big = SHOTS[i](t, u)
    return SHOW.apply(big, t, NAMES[i])


if __name__ == '__main__':
    EPI.main(render, __file__)
