"""Chapter 2 «Emotional Support Flamingo» (E02)."""
from shots import *

WU = 9.4

def cert_small(L, h, ang=-0.15, w=5.6, hh=7.2):
    cx, cy = h[0] + 0.3, h[1] - 0.4
    UP.rect(L, cx + 0.3, cy + 0.3, w, hh, ang, (150, 110, 40))
    UP.rect(L, cx, cy, w, hh, ang, (250, 244, 222))
    UP.rect(L, cx, cy - hh * 0.30, w - 1.2, 1.1, ang, (230, 60, 130))
    UP.ltext(L, 'OFFICIAL', (cx, cy - hh * 0.05), min(1.2, w * 0.8 / 8), (60, 50, 110), ang)
    UP.ltext(L, '$19.99', (cx, cy + hh * 0.26), min(1.2, w * 0.7 / 6), (214, 150, 20), ang)
    for k in range(3): UP.dot(L, (cx - 1.3 + 1.3 * k, cy + hh * 0.42), (255, 196, 40), 0.42)

def form300(L, h): UP.notice(L, h, -0.15, 5.4, 7.0, '$300')
def clip(L, h): UP.clipboard(L, h, -0.15, w=4.4, hh=6.0)
def bind(L, h): UP.binder(L, h, -0.1, 5.4, 7.2)


def kev(x, y, u, flip=False, wob=0.0): return kev_hook(x, y, u, flip, wob)


def b_d1(ctx, t, u, dur):
    cast = [dict(who='dale', x=430, y=604, u=WU, pose=U.DPOSE['hips'], expr='smug', shades=True, red=0.25)]
    return scene(ctx, t, u, dur, 'yard', cast, (520, 470, 1.25, 500, 470, 1.4), before=kev(545, 606, WU * 0.95, wob=0.5 * hit(u, 0.05, 0.3)))


def cert_draw(hl):
    def d(big, t, u, dur): UP.cert_insert(big, t, hl=sm((u - 0.4) / 0.35))
    return d


def parade(ctx, t, u, dur):
    Z = 1.05
    ST.set_px(ST.px_for_zoom(Z))
    v = view_at(world('yard'), 1000, 470, Z, 320, 200)
    big = v.bg(); CH, _ = K.begin(Z)
    rng = np.random.default_rng(94)
    pts = sorted(((float(rng.uniform(800, 1180)), float(rng.uniform(432, 590))) for _ in range(40)), key=lambda p: p[1])
    shown = int(min(len(pts), 4 + u * 12))
    for i, (x, y) in enumerate(pts[:shown]):
        us = lerp(2.4, 4.8, (y - 432) / 158)
        UP.flamingo(CH, v.cam(x, y, us), t + i, True, i % 3 == 0, 0.25 * math.sin(t * 3 + i), 0.0)
    CH.comp(big, K.light_yard(v))
    C2 = Chars()
    hero(C2, v, ctx, t, dict(who='brenda', x=1090, y=608, u=8.6, flip=True, pose=U.BPOSE['stand'], expr='sweet', hand_n=U.H(3.4, 13.6), prop_n=UP.clipboard))
    C2.comp(big, K.light_yard(v))
    fx.vignette(big, 0.22)
    return big


def fund(ctx, t, u, dur):
    k = sm((u - 0.15) / 0.45)
    Z = lerp(1.5, 0.9, k)
    ST.set_px(ST.px_for_zoom(Z))
    v = view_at(world('interior'), lerp(318.0, 452.0, k), lerp(370.0, 262.0, k), Z, 320, 190)
    big = v.bg(); CH, _ = K.begin(Z)
    UP.fund_jar(CH, v, t, 1.0)
    CH.comp(big, K.light_int(v))
    UP.fund_insert(big, v, t, 0.04 + 0.08 * sm((u - 0.45) / 0.35), pop=(u - 0.8) / 0.6 if u > 0.8 else 0.0, title=('MALDIVES', '2028'))
    fx.shafts(big, t, 0.6, 0.05); fx.vignette(big, 0.25)
    return big


def throw(ctx, t, u, dur):
    Z = 1.1
    ST.set_px(ST.px_for_zoom(Z))
    v = view_at(world('yard'), 560, 470, Z, 320, 190)
    big = v.bg(); CH, _ = K.begin(Z)
    k = min(1.0, u / 0.5)
    x = lerp(300.0, 610.0, k); y = lerp(560.0, 500.0, k) - 170 * math.sin(k * math.pi)
    if u < 0.5: UP.flamingo(CH, v.cam(x, y, 4.6, flip=int(t * 14) % 2 == 0), t, True, True, 0.0, 0.0)
    CH.comp(big, K.light_yard(v))
    if u >= 0.45:
        sx, sy = v.opt(610, 505); ph = (u - 0.45) / 0.4
        for i in range(8):
            B.puff(big, sx + 60 * math.sin(i * 1.3) * (0.3 + ph), sy - 120 * ph * (0.4 + 0.15 * i % 0.5), 50 + 60 * ph, 0.7 * max(0.0, 1 - ph), (220, 240, 250))
    if u < 0.3: B.shake(big, t, 8 * (1 - u / 0.3), 33)
    fx.vignette(big, 0.22)
    return big


def earl_chew(ctx, t, u, dur):
    chewing = u < 0.85
    return earl_cu(ctx, t, u, dur, 'yard', lid=0.85 if 0.85 <= u < 1.05 else 0.5, Z=2.4, stuff='flamingo' if chewing else None, chew=1.0 if chewing else 0.0)


def dale_kev(ex, **kw):
    return cu('dale', 'yard', 1.3, 0.05, before=kev(430 + 6.4 * 16 * 0.95, 606, 16 * 0.95 * 0.8), **kw)


V2 = 'ep02_t'
BLOCK = Block('ch2', [
    dict(v=(V2, 'd1', 'dale', "This is Kevin. He's my emotional support FLAMINGO."), fn=b_d1, sfx=[('library/sfx/rubber_duck.mp3', 0.05, 0.6), ('library/sfx/rubber_duck.mp3', 1.9, 0.45)]),
    dict(v=(V2, 'b1', 'brenda', "Kevin is PLASTIC."), fn=cu('brenda', 'yard', 1.25, 0.05, expr='hollow', hand_n=U.H(3.4, 10.4), prop_n=clip, before=kev(790, 606, 14.0, True))),
    dict(v=(V2, 'd2', 'dale', "Emotionally? So am I. I have PAPERS."), fn=cuts([(0, cu('dale', 'yard', 1.3, 0.05, expr='smug', shades=True, hand_n=U.H(8.0, 14.0), prop_n=cert_small, red=0.25)),
                                                                        (1.7, cu('dale', 'yard', 1.55, 0.04, expr='smug', shades=True, hand_n=U.H(8.0, 14.0), prop_n=cert_small, red=0.25))]), pad=0.12),
    dict(v=(V2, 'b2', 'brenda', "This says, 'Novelty.'"), fn=cuts([(0, cu('brenda', 'yard', 1.35, 0.05, expr='evil', hand_n=U.H(7.4, 15.4), prop_n=lambda L, h: cert_small(L, h, 0.1))),
                                                                (1.2, portrait_insert(cert_draw(1.0), 'yard'))]), sfx=[('library/sfx/paper_unroll.mp3', 0.0, 0.4, 0.0, 0.8), ('library/sfx/record_scratch.mp3', 1.4, 0.6, 0.0, 0.7)]),
    dict(v=(V2, 'd3', 'dale', "Novelty is a LEGAL term."), fn=cu('dale', 'yard', 1.3, 0.1, expr='smug', shades=True, pose=U.DPOSE['hips'], red=0.2)),
    dict(v=(V2, 'b3', 'brenda', "Federal law. It's VALID."), fn=cu('brenda', 'yard', 1.35, 0.06, expr='shock', sweat=0.9, hand_n=U.H(3.6, 12.0), prop_n=bind), sfx=[('library/sfx/shop_bell.mp3', 0.0, 0.5)]),
    dict(v=('ep01_t', 'd5', 'dale', "YES!"), fn=cu('dale', 'yard', 1.25, 0.12, expr='cheer', shades=True, hand_n=U.H(8.6, 26.0), before=kev(560, 606, 14.0)), sfx=[('library/sfx/coin_clink.mp3', 0.05, 0.45, 0.0, 0.6), ('library/sfx/sax_sting_swell.mp3', 0.3, 0.45, 0.0, 2.6)],
         st=[('AURA +9999', (255, 236, 96), 60, 1400, 250, 0.05, 1.3)], flash=[0.0], pad=0.08),
    dict(v=(V2, 'b4', 'brenda', "Kevin is pink. Approved pink is 'Coral Whisper.'"), fn=cuts([(0, cu('brenda', 'yard', 1.3, 0.05, expr='evil', hand_n=U.H(7.8, 14.6), prop_n=clip, before=kev(790, 606, 14.0, True))),
                                                                                       (2.0, two('yard', [dict(who='brenda', x=900, y=606, u=9.4, flip=True, expr='sweet', pose=U.BPOSE['board'], hand_n=U.H(3.4, 13.6), prop_n=UP.clipboard)],
                                                                                                 (800, 470, 1.35), before=kev(690, 608, 8.9, True)))]),
         st=[('CORAL WHISPER', (255, 150, 190), 64, 700, 300, 2.0, 3.6)], sfx=[('library/sfx/paper_unroll.mp3', 0.1, 0.3, 0.0, 0.6)]),
    dict(v=(V2, 'b5', 'brenda', "Wonderful! Registration is three hundred dollars. Per YEAR."), fn=cuts([(0, cu('brenda', 'yard', 1.3, 0.05, expr='bright', pose=U.BPOSE['hands'], lean=0.3)),
                                                                                                  (2.4, cu('brenda', 'yard', 1.55, 0.05, expr='sweet', hand_n=U.H(7.6, 15.0), prop_n=form300))]),
         sfx=[('library/sfx/cash_register.mp3', 3.0, 0.7), ('library/sfx/sad_trombone.mp3', 4.2, 0.4, 0.0, 1.6)], st=[('$300 / YEAR', (255, 84, 96), 78, 700, 300, 2.9, 4.5)], fines='$1,050', fines_dt=3.2),
    dict(v=(V2, 'd4', 'dale', "PER YEAR?!"), fn=cu('dale', 'yard', 1.35, 0.15, expr='shock', shades=None, sweat=0.9, pose=U.DPOSE['shout'], red=0.15), st=[('AURA -9999', (255, 100, 100), 60, 1400, 250, 0.1, 1.2)]),
    dict(v=('ep01_t', 'b3', 'brenda', "Bless your heart."), fn=cu('brenda', 'yard', 1.4, 0.06, expr='sweet', lean=0.4, pose=U.BPOSE['hands']), st=[('(TRANSLATION: YOU IDIOT)', (255, 190, 226), 34, 960, 760, 0.1, 1.5)], pad=0.15),
    dict(v=(V2, 'b6', 'brenda', "The whole street is registered. Ninety-four FLAMINGOS."), fn=parade, sfx=[('library/sfx/rubber_duck.mp3', 0.9 + 0.35 * i, 0.4) for i in range(6)] + [('library/sfx/cash_register.mp3', 2.6, 0.8)],
         st=[('94 FLAMINGOS', (255, 236, 120), 84, 620, 300, 1.6, 3.9)], mosaic=[0.0]),
    dict(dur=0.8, fn=fund, sfx=[('library/sfx/coin_clink.mp3', 0.2, 0.4, 0.0, 0.6)], cap=None),
    dict(v=(V2, 'd5', 'dale', "I'm sorry, Kevin. FLY."), fn=cu('dale', 'yard', 1.3, 0.14, expr='sad', shades=None, sweat=1.0, pose=U.DPOSE['hold'], hand_n=U.H(5.2, 12.0), before=kev(560, 606, 12.0), red=0.1)),
    dict(dur=0.9, fn=throw, sfx=[('library/sfx/whoosh.mp3', 0.0, 0.6), ('library/sfx/bath_splash.mp3', 0.45, 0.8)], cap=None, mosaic=[0.0]),
    dict(v=(V2, 'e1', 'earl', "I feel SUPPORTED."), fn=earl_chew, sfx=[('library/sfx/plastic_crunch.mp3', 0.1, 0.8), ('library/sfx/plastic_crunch.mp3', 0.5, 0.6, 0.0, 0.7), ('library/sfx/gator_gulp.mp3', 0.7, 0.9)], pad=0.3),
], beds=[('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.24, True), ('library/sfx/amb_florida_yard.mp3', 7.8, 0.0, None, 0.32, False)])
