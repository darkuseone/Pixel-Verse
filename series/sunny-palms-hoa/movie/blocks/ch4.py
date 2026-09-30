"""Chapter 4 «Category 5 (Permit)» (E04): the HOA fines a hurricane."""
from shots import *

WU = 8.4

def rain_post(flashes=()):
    def f(big, t, u):
        UP.rain(big, t, 1.0, 0.35, 150)
        B.shake(big, t, 3, 29)
        for a, b in flashes:
            if a <= u < b: O.flash(big, 0.55 * (1 - (u - a) / (b - a)))
    return f

def calm(big, t, u): UP.rainbow(big, 0.28, W_ // 2, 1500, 1350, 40)

STORM_P = rain_post([])
def chair_b(C, v, t, u): UP.lawn_chair(C, v.cam(430.0, 592.0, 16.0), t)
def cooler_f(C, v, t, u): UP.cooler(C, v.cam(430.0 + 9.0 * 16.0, 592.0, 12.8))
def umb_f(C, v, t, u): UP.umbrella(C, v.cam(965.0, 592.0, 16.0, flip=True), 3.4, 13.0)
def weeds_f(C, v, t, u): UP.weeds(C, v.cam(430.0, 592.0, 16.0))
def clip(L, h): UP.clipboard(L, h, -0.15, w=4.4, hh=6.0)
def note(txt, w=5.6, hh=7.0, ang=-0.2): return lambda L, h: UP.notice(L, h, ang, w, hh, txt)


def dale_st(expr='cheer', **kw):
    return cu('dale', 'storm', 1.3, 0.06, expr=expr, shades=True, before=chair_b, front=cooler_f, post=STORM_P, **kw)


def brenda_st(expr='sweet', **kw):
    return cu('brenda', 'storm', 1.3, 0.05, expr=expr, front=umb_f, post=STORM_P, **kw)


def dale_calm(expr, **kw): return cu('dale', 'yard', 1.3, 0.08, expr=expr, shades=None, front=weeds_f, post=calm, **kw)
def brenda_calm(expr, **kw): return cu('brenda', 'yard', 1.3, 0.06, expr=expr, post=calm, **kw)


def b_estab(ctx, t, u, dur):
    cast = [dict(who='dale', x=520, y=606, u=8.6, expr='cheer', shades=True, pose=U.DPOSE['hold'], hand_n=U.H(6.6, 12.4), prop_n=UP.koozie_can, mute=True)]
    return scene(ctx, t, u, dur, 'storm', cast, (560, 470, 1.15, 560, 470, 1.3), before=lambda C, v, tt, uu: UP.lawn_chair(C, v.cam(520.0, 606.0, 8.6), tt),
                 front=lambda C, v, tt, uu: UP.cooler(C, v.cam(600.0, 606.0, 7.0)), post=rain_post([(0.95, 1.08)]))


def d0_wide(ctx, t, u, dur):
    cast = [dict(who='dale', x=500, y=606, u=9.6, expr='smug', shades=True, pose=U.DPOSE['hold'], hand_n=U.H(6.6, 12.4), prop_n=UP.koozie_can, red=0.2)]
    return scene(ctx, t, u, dur, 'storm', cast, (560, 470, 1.2, 560, 470, 1.35), before=lambda C, v, tt, uu: UP.lawn_chair(C, v.cam(500.0, 606.0, 9.6), tt),
                 front=lambda C, v, tt, uu: UP.cooler(C, v.cam(500.0 + 9.0 * 9.6, 606.0, 7.6)), post=STORM_P)


def storm_arrive(ctx, t, u, dur):
    Z = 1.0
    ST.set_px(ST.px_for_zoom(Z))
    v = view_at(world('storm'), 600, 470, Z, 320, 200)
    big = v.bg(); CH, _ = K.begin(Z)
    for i in range(8):
        ph = (u * 0.85 + i * 0.13) % 1.0
        x = lerp(1000.0, 120.0, ph); y = 280 + 34 * i + 50 * math.sin(ph * 9 + i)
        UP.flamingo(CH, v.cam(x, y, 3.6 + 0.3 * (i % 3), flip=int(t * 12 + i) % 2 == 0), t + i, True, i % 2 == 0, 0.0, 0.0)
    ph = (u * 0.7 + 0.1) % 1.0
    UP.mailbox_world(CH, v, lerp(980.0, 110.0, ph), 330 + 60 * math.sin(ph * 12), 0.0, t, s=0.9)
    CH.comp(big, K.light_storm(v))
    C2 = Chars()
    px = lerp(1000.0, -20.0, min(1.0, u / 3.0)); py = 545 - 50 * abs(math.sin(u * 5))
    UP.lawn_chair(C2, v.cam(px, py, 5.0))
    U.dale(C2, v.cam(px, py - 4 * 5.0, 5.0), U.DPOSE['cheer'], t, 0.8, 'cheer', 0.0, True, legs=False, hand_n=U.H(7.4, 24.0 + 2 * math.sin(t * 20)), prop_n=UP.koozie_can)
    C2.comp(big, K.light_storm(v))
    rain_post([(0.0, 0.14), (0.65, 0.8), (2.0, 2.15)])(big, t, u)
    UP.rain(big, t + 0.5, 0.6, 0.6, 120)
    fx.vignette(big, 0.3)
    return big


def ticket(ctx, t, u, dur):
    storm = u < 0.9
    wname = 'storm' if storm else 'yard'
    hand = U.H(6.0 + 2.0 * sm(u / 0.4), 22.0 - 2.0 * sm(u / 0.4)) if storm else U.H(3.4, 13.6)
    cast = [dict(who='brenda', x=760, y=606, u=8.6, flip=True, pose=U.BPOSE['point'] if storm else U.BPOSE['wave'], hand_n=hand, expr='sweet', mute=True)]
    def front(C, v, tt, uu):
        if storm: UP.umbrella(C, v.cam(760.0, 606.0, 8.6, flip=True), 3.4, 12.0)
    def after(big, v, tt, uu):
        if storm:
            C3 = Chars(); L = Layer(v.cam(600.0 - 260 * max(0.0, uu - 0.3), 330.0 - 60 * max(0.0, uu - 0.3), 6.0))
            UP.notice(L, U.H(0, 0), 0.3 + 9 * uu, 5.4, 7.0, '$500'); C3.add(L); C3.comp(big, K.light_storm(v))
            rain_post([])(big, tt, uu)
        else:
            UP.rainbow(big, 0.34, W_ // 2, 1500, 1350, 40)
    return scene(ctx, t, u, dur, wname, cast, (640, 470, 1.15), front=front, after=after)


def earl_debris(ctx, t, u, dur):
    def front(CH, v):
        EX, EY, EU = POND['yard']
        UP.flamingo(CH, v.cam(EX + 9.5 * EU, EY + 0.2 * EU, EU * 0.42, flip=True), t, True, True, 0.0, 0.0)
    return earl_cu(ctx, t, u, dur, 'yard', lid=0.5, Z=2.3, front=front)


V4 = 'ep04_t'
BLOCK = Block('ch4', [
    dict(dur=2.0, fn=b_estab, cap=None, sfx=[('library/sfx/thunder_crack.mp3', 0.0, 0.6, 0.0, 1.6), ('library/sfx/whoosh.mp3', 0.0, 0.5, 0.0, 0.5), ('library/sfx/stamp.mp3', 0.35, 0.8)]),
    dict(v=(V4, 'd1', 'dale', "Category five? Is that the GOOD one?"), fn=dale_st('cheer', hand_n=U.H(6.6, 12.4), prop_n=UP.koozie_can, red=0.15, look=0.2)),
    dict(v=(V4, 'b1', 'brenda', "It's the WORST one."), fn=brenda_st('sweet', hand_n=U.H(3.4, 12.0), prop_n=clip)),
    dict(v=(V4, 'd2', 'dale', "So it's the BEST one!"), fn=dale_st('cheer', hand_n=U.H(8.6, 25.0), red=0.2), pad=0.1),
    dict(v=(V4, 'd0', 'dale', "I have a cooler, a lawn chair, and zero PLANS."), fn=cuts([(0, dale_st('smug', hand_n=U.H(6.6, 12.4), prop_n=UP.koozie_can, red=0.2)), (1.9, d0_wide)]),
         st=[('HURRICANE PARTY', (255, 236, 120), 60, 700, 300, 0.2, 1.9)]),
    dict(dur=3.0, fn=storm_arrive, cap=None, mosaic=[0.0], sfx=[('library/sfx/sax_sting_swell.mp3', 0.0, 0.5, 0.0, 3.0), ('library/sfx/debris_crash.mp3', 0.6, 0.6), ('library/sfx/thunder_crack.mp3', 0.65, 0.9),
                                                             ('library/sfx/debris_crash.mp3', 1.3, 0.55), ('library/sfx/thunder_crack.mp3', 2.0, 0.7, 0.0, 2.0), ('library/sfx/debris_crash.mp3', 2.25, 0.5)],
         st=[('[SAXOPHONE GETS LOUDER]', (255, 255, 255), 30, 960, 1010, 0.0, 1.7), ('WIND: 156 MPH', (255, 120, 110), 64, 700, 300, 0.3, 2.9)]),
    dict(v=(V4, 'b3', 'brenda', "Hurricane Kevin. No permit. Wind is over the LIMIT."), fn=cuts([(0, brenda_st('sweet', pose=U.BPOSE['hands'], lean=0.2)),
                                                                                                  (2.2, brenda_st('sweet', hand_n=U.H(3.4, 12.0), prop_n=clip))]), pad=0.1,
         sfx=[('library/sfx/paper_unroll.mp3', 2.2, 0.4, 0.0, 0.8)]),
    dict(dur=1.9, fn=ticket, cap=None, sfx=[('library/sfx/paper_unroll.mp3', 0.0, 0.4, 0.0, 0.8), ('library/sfx/whoosh.mp3', 0.45, 0.5), ('library/sfx/record_scratch.mp3', 0.9, 0.7, 0.0, 0.9), ('library/sfx/shop_bell.mp3', 1.05, 0.35)],
         st=[('FINE: $500 (WIND)', (255, 236, 120), 46, 700, 300, 0.1, 1.8)], flash=[0.9]),
    dict(v=(V4, 'd3', 'dale', "She fined the HURRICANE."), fn=dale_calm('shock', sweat=1.0, look=0.3)),
    dict(v=(V4, 'b4', 'brenda', "Rules are RULES."), fn=brenda_calm('sweet', pose=U.BPOSE['hands'], lean=0.3)),
    dict(v=(V4, 'd4', 'dale', "Ha. What are you gonna do, make it PAY?"), fn=cuts([(0, dale_calm('smug', sweat=0.7, red=0.1)), (1.5, cu('dale', 'yard', 1.6, 0.05, expr='smug', shades=None, front=weeds_f, post=calm))])),
    dict(v=(V4, 'b5', 'brenda', "No. You WILL."), fn=brenda_calm('evil', pose=U.BPOSE['hands'], lean=0.4), sfx=[('library/sfx/sax_sting_swell.mp3', 0.0, 0.5, 0.0, 1.8)],
         st=[('[SAXOPHONE GETS LOUDER]', (255, 255, 255), 30, 960, 1010, 0.0, 1.8)]),
    dict(v=(V4, 'd5', 'dale', "WHAT?!"), fn=dale_calm('shock', sweat=1.0, pose=U.DPOSE['shout']), st=[('AURA -9999', (255, 100, 100), 60, 1400, 250, 0.05, 1.2)], sfx=[('library/sfx/coin_clink.mp3', 0.0, 0.4, 0.0, 0.5)], pad=0.08),
    dict(v=(V4, 'b6', 'brenda', "It landed on your lawn. Four thousand seven hundred fifty DOLLARS."), fn=cuts([(0, brenda_calm('bright', hand_n=U.H(7.4, 13.6), prop_n=note('$4750'))), (2.4, brenda_calm('sweet', hand_n=U.H(7.4, 13.6), prop_n=note('$4750')))]),
         sfx=[('library/sfx/paper_crumple_slap.mp3', 0.2, 0.6), ('library/sfx/cash_register.mp3', 3.0, 0.8), ('library/sfx/sad_trombone.mp3', 3.4, 0.4, 0.0, 1.6)], st=[('$4,750', (255, 84, 96), 130, 700, 300, 1.8, 3.9)],
         fines='$5,900', fines_dt=3.1),
    dict(v=(V4, 'd6', 'dale', "I only wanted a PARTY."), fn=dale_calm('sad', sweat=1.0, hand_n=U.H(6.2, 12.8), prop_n=note('$4750', 5.0, 6.4))),
    dict(v=(V4, 'e1', 'earl', "She fined a hurricane. Never once fined ME. Think about that."), fn=cuts([(0, earl_debris), (2.9, lambda c, t, u, d: earl_cu(c, t, u, d, 'yard', lid=0.5, Z=2.8, zoom=0.05))]),
         sfx=[('library/sfx/pond_bloop.mp3', 0.0, 0.5)], pad=0.3),
], beds=[('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.22, True), ('library/sfx/hurricane_wind_howl.mp3', 7.5, 0.0, 17.0, 0.5, True), ('library/sfx/rain_heavy.mp3', 6.6, 0.0, 17.0, 0.4, True),
         ('library/sfx/amb_florida_yard.mp3', 7.8, 17.0, None, 0.32, False)],
    card=(4, 'CATEGORY 5 (PERMIT)', 'FINES SO FAR: $1,150'), chapter='Chapter 4: Category 5 (Permit)')
