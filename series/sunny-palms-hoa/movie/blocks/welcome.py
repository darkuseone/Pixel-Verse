"""Move-in day: Brenda hands Dale the 400-page welcome packet (pays off in the post-credits scene)."""
from shots import *
from props.folk import H


def binder_p(L, h): UP.binder(L, h, -0.1, w=6.0, hh=8.0, title='WELCOME', pages='400 PG')
def binder_big(L, h): UP.binder(L, h, 0.1, w=6.6, hh=8.8, title='WELCOME', pages='400 PG')


def cooler_bh(x, y, u):
    def f(CH, v, t, uu):
        UP.cooler(CH, v.cam(x, y, u))
    return f


def w_hand(ctx, t, u, dur):
    cast = [dict(who='dale', x=470, y=604, u=9.4, expr='cheer', pose=U.DPOSE['stand'], shades=False),
            dict(who='brenda', x=760, y=604, u=9.4, flip=True, expr='bright', pose=U.BPOSE['show'], hand_n=U.H(8.2, 17.6), prop_n=binder_p)]
    return scene(ctx, t, u, dur, 'yard', cast, (610, 470, 1.12, 620, 470, 1.25), before=cooler_bh(340, 612, 6.0))


def w_thud(ctx, t, u, dur):
    sag = sm(u / 0.15)
    cast = [dict(who='dale', x=470, y=604 + 6 * sag, u=9.4, expr='shock', pose=dict(U.DPOSE['hold'], n=(6.0, 11.0), f=(5.0, 11.4)), hand_n=U.H(6.0, 11.0 - 1.2 * sag), prop_n=binder_big, lean=0.3 * sag),
            dict(who='brenda', x=760, y=604, u=9.4, flip=True, expr='bright', pose=U.BPOSE['hands'])]
    return scene(ctx, t, u, dur, 'yard', cast, (610, 470, 1.25, 610, 480, 1.35), before=cooler_bh(340, 612, 6.0), shake=14 * hit(u, 0.0, 0.4))


def w_pages(ctx, t, u, dur):
    return cu('brenda', 'yard', 1.3, 0.05, expr='sweet', pose=U.BPOSE['hands'], lean=0.3)(ctx, t, u, dur)


def w_never(ctx, t, u, dur):
    return cu('dale', 'yard', 1.3, 0.05, expr='cheer', pose=dict(U.DPOSE['hold'], n=(6.0, 12.0), f=(5.0, 12.4)), hand_n=U.H(6.0, 12.0), prop_n=binder_big)(ctx, t, u, dur)


def w_toss(ctx, t, u, dur):
    k = min(1.0, u / 0.55)
    def after(big, v, t, uu):
        if k < 1.0:
            C = Chars(); L = Layer(v.wcam())
            x = lerp(520.0, 640.0, k); y = lerp(500.0, 470.0, k) - 190 * math.sin(k * math.pi)
            UP.binder(L, (x, y), 0.4 + 9 * k, w=34, hh=46, title='WELCOME', pages='400 PG'); C.add(L); C.comp(big, K.light_yard(v))
        else:
            sx, sy = v.opt(640, 500); ph = (u - 0.55) / 0.35
            for i in range(8):
                B.puff(big, sx + 60 * math.sin(i * 1.3) * (0.3 + ph), sy - 100 * ph * (0.4 + 0.1 * i % 0.5), 50 + 60 * ph, 0.7 * max(0.0, 1 - ph), (220, 240, 250))
    arm = U.H(8.0, 20.0) if u < 0.4 else U.H(3.6, 10.2)
    cast = [dict(who='dale', x=470, y=604, u=9.4, expr='cheer', pose=dict(U.DPOSE['shout'], n=(8.0, 20.0)) if u < 0.4 else U.DPOSE['stand'], mute=True),
            dict(who='brenda', x=790, y=604, u=9.4, flip=True, expr='shock', pose=U.BPOSE['hands'], mute=True)]
    return scene(ctx, t, u, dur, 'yard', cast, (610, 470, 1.15), after=after, before=lambda C, v, t, uu: U.earl(C, v.cam(640.0, 500.0, 4.4), t, 0.0, 0.55, (-0.6, 0.0), None, 0.0, 1.0, True))


def binder_head(CH, v):
    EX, EY, EU = POND['yard']
    L = Layer(v.cam(EX, EY, EU)); UP.binder(L, H(0.6, 3.4), 0.35, w=3.0, hh=4.0, title='WELCOME', pages='400 PG'); CH.add(L)


def skip(ctx, t, u, dur):
    big = np.zeros((H_, W_, 3), np.uint8); big[:] = (24, 8, 44)
    ptext(big, 'TWO DAYS LATER', W_ // 2, 540, 60, (255, 236, 120), (10, 2, 20))
    return big


BLOCK = Block('welcome', [
    dict(v=('movie_t', 'w1', 'brenda', "Welcome to Sunny Palms! Here is your welcome PACKET."), fn=w_hand, cap=940,
         sfx=[('library/sfx/golf_cart_screech.mp3', 0.0, 0.0, 0.0, 0.1)]),
    dict(v=('movie_t', 'w2', 'dale', "Sweet! How LONG is it?"), fn=w_thud, sfx=[('library/sfx/book_thud.mp3', 0.0, 1.0)]),
    dict(v=('movie_t', 'w3', 'brenda', "Four hundred pages. Page one is the FINES."), fn=w_pages, st=[('400 PAGES', (255, 236, 120), 70, 480, 300, 0.2, 2.2)]),
    dict(v=('movie_t', 'w4', 'dale', "Nice. I'll read it NEVER."), fn=w_never, sfx=[('library/sfx/sax_sting_swell.mp3', 0.5, 0.3, 0.0, 1.2)]),
    dict(dur=1.0, fn=w_toss, sfx=[('library/sfx/whoosh.mp3', 0.05, 0.6, 0.0, 0.5), ('library/sfx/pond_bloop.mp3', 0.6, 0.7)], cap=None),
    dict(v=('movie_t', 'w5', 'earl', "He never read it. Nobody does. That's how they get you."), fn=earl('yard', 0.5, 2.2, front=binder_head), lead=0.1, pad=0.2),
    dict(dur=1.1, fn=skip, sfx=[('library/sfx/whoosh.mp3', 0.0, 0.6, 0.0, 0.6)], cap=None),
], beds=[('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.24, True), ('library/sfx/amb_florida_yard.mp3', 7.8, 0.0, None, 0.32, False)], hud=False)
