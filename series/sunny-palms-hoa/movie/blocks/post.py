"""Post-credits scene: Brenda in the Bahamas (Beautification Fund), Dale reads page 400, hurricane season."""
from shots import *
from props.folk import H

BONE_UMB = ((232, 222, 200), (246, 238, 220), (196, 184, 160))
BX = 560.0; FY = 640.0


def drink(L, h):
    UP.rect(L, h[0] + 0.4, h[1] - 0.6, 1.6, 2.6, 0.0, (250, 236, 250)); UP.rect(L, h[0] + 0.4, h[1] - 0.2, 1.3, 1.4, 0.0, (255, 110, 170))
    UP.cap(L, (h[0] + 0.5, h[1] - 1.6), (h[0] + 1.3, h[1] - 3.2), 0.12, 0.12, (255, 236, 90))
def clip(L, h): UP.clipboard(L, h, -0.12, w=4.4, hh=6.0, title='FINES')
def binder(L, h): UP.binder(L, h, -0.1, w=5.6, hh=7.4, title='BYLAWS', pages='400 PG')


def beach_before(x=BX):
    def f(C, v, t, u):
        L = Layer(v.cam(x + 40.0, FY + 6, 9.0)); UP.rect(L, H(0, 3.0), 8.0, 5.0, 0, (20, 130, 150)); UP.ltext(L, 'FUND', H(0, 3.6), 1.4, (255, 236, 120)); C.add(L)
    return f


def umb_front(x=BX):
    def f(C, v, t, u): UP.umbrella(C, v.cam(x, FY, 9.0, flip=True), 4.6, 12.0, 31.0, BONE_UMB)
    return f


def brenda_spec(mute=False, expr='sweet', **kw):
    return dict(who='brenda', x=BX, y=FY, u=9.0, flip=True, expr=expr, pose=U.BPOSE['stand'], hand_n=U.H(4.6, 12.0), prop_n=drink, mute=mute, **kw)


def estab(ctx, t, u, dur):
    big = scene(ctx, t, u, dur, 'beach', [brenda_spec(True)], (700, 470, 1.0, 640, 470, 1.15), before=beach_before(), front=umb_front())
    ptext(big, 'THE BAHAMAS', W_ // 2, 200, 60, (255, 236, 120), (30, 10, 50))
    ptext(big, 'SIX MONTHS LATER', W_ // 2, 280, 28, (255, 200, 236), (30, 10, 50))
    return big


def relax(ctx, t, u, dur):
    return scene(ctx, t, u, dur, 'beach', [brenda_spec(expr='sweet', lean=0.2)], (BX + 30, 520, 1.5, BX + 30, 520, 1.6), before=beach_before(), front=umb_front())


def walk_in(ctx, t, u, dur):
    x = lerp(180.0, 380.0, min(1.0, u / 1.4))
    cast = [brenda_spec(True), dict(who='dale', x=x, y=FY + 8, u=9.4, pose=U.dwalk(t, 9.0, 0.4) if u < 1.4 else U.DPOSE['hold'], hand_n=None if u < 1.4 else U.H(5.6, 12.6), prop_n=None if u < 1.4 else clip, expr='smug', visor=True)]
    return scene(ctx, t, u, dur, 'beach', cast, (420, 500, 1.2, 440, 500, 1.25), before=beach_before(), front=umb_front())


def dale_cu(expr='smug', **kw):
    def f(ctx, t, u, dur):
        return cu('dale', 'beach', 1.35, 0.06, anchor=(440.0, FY, 16.0), expr=expr, visor=True, **kw)(ctx, t, u, dur)
    return f


def brenda_cu(expr, **kw):
    def f(ctx, t, u, dur):
        return cu('brenda', 'beach', 1.35, 0.06, anchor=(BX, FY, 16.0), expr=expr, before=lambda C, v, t, u: None, **kw)(ctx, t, u, dur)
    return f


def earl_surf(ctx, t, u, dur, dark=0.0):
    big = earl_cu(ctx, t, u, dur, 'beach', lid=0.5, Z=2.4, look=(0.4, 0.0))
    if dark > 0: dim(big, dark * 0.5)
    return big


def wide_all(ctx, t, u, dur):
    cast = [brenda_spec(True, sweat=1.0), dict(who='dale', x=380, y=FY + 8, u=9.4, pose=U.DPOSE['hold'], hand_n=U.H(5.6, 12.6), prop_n=binder, expr='smug', visor=True)]
    def before(C, v, tt, uu):
        beach_before()(C, v, tt, uu)
        U.earl(C, v.cam(860.0, 400.0, 6.0), tt, 0.0, 0.5, (-0.5, 0.0), None, 0.0, 1.0, True)
    return scene(ctx, t, u, dur, 'beach', cast, (560, 500, 1.15, 560, 500, 1.3), before=before, front=umb_front())


def storm_end(ctx, t, u, dur):
    k = sm(u / 1.0)
    big = earl_cu(ctx, t, u, dur, 'beach', lid=0.5, Z=2.4, look=(0.4, 0.0))
    dim(big, 0.5 * k)
    if u > 0.8:
        UP.rain(big, t, min(1.0, (u - 0.8) / 1.0), 0.35, 150)
    return big


def endcard(ctx, t, u, dur):
    big = np.zeros((H_, W_, 3), np.uint8); big[:] = (18, 8, 36)
    ti = O.neon_title(['SEASON 2', 'HURRICANE SEASON'], 92, width=W_)
    k = sm(u / 0.4)
    O.overlay(big, ti, 0, 300, k)
    ptext(big, 'COMING SOON', W_ // 2, 720, 40, (0, 214, 232), (10, 2, 20))
    if u > 0.9: ptext(big, 'FINES MAY APPLY', W_ // 2, 820, 26, (255, 236, 120), (10, 2, 20))
    return big


V = 'movie_t'
BLOCK = Block('post', [
    dict(dur=1.7, fn=estab, cap=None, sfx=[('library/sfx/seagull.mp3', 0.2, 0.6), ('library/sfx/whoosh.mp3', 0.0, 0.5, 0.0, 0.5)], mosaic=[0.0]),
    dict(v=(V, 'a1', 'brenda', "Finally. Peace and quiet. Nobody knows I'm HERE."), fn=relax, sfx=[('library/sfx/ice_clink.mp3', 3.0, 0.7)], lead=0.05, pad=0.15),
    dict(v=(V, 'a2', 'dale', "Morning, Brenda. Your umbrella is BONE."), fn=cuts([(0, walk_in), (1.5, dale_cu('smug', hand_n=U.H(5.6, 12.6), prop_n=clip))]), sfx=[('library/sfx/flipflop_stomp.mp3', 0.0, 0.5, 0.0, 1.2), ('library/sfx/sax_sting_swell.mp3', 2.2, 0.4, 0.0, 1.2)], pad=0.1),
    dict(v=(V, 'a3', 'brenda', "HOW did you find me?!"), fn=brenda_cu('shock', sweat=1.0, hand_n=U.H(4.6, 12.0), prop_n=drink), sfx=[('library/sfx/record_scratch.mp3', 0.0, 0.7, 0.0, 0.8), ('library/sfx/crowd_gasp.mp3', 0.0, 0.4, 0.0, 1.0)], pad=0.08),
    dict(v=(V, 'a4', 'dale', "Page four hundred. The president may fine anyone. ANYWHERE."), fn=cuts([(0, dale_cu('smug', hand_n=U.H(5.6, 12.6), prop_n=binder)), (2.6, wide_all)]), st=[('PAGE 400', (255, 236, 120), 80, 1300, 260, 0.3, 2.6)],
         sfx=[('library/sfx/paper_unroll.mp3', 0.2, 0.4, 0.0, 0.8)], pad=0.1),
    dict(v=(V, 'a5', 'brenda', "You READ the packet?"), fn=brenda_cu('shock', sweat=1.0), sfx=[('library/sfx/crowd_gasp.mp3', 0.0, 0.5)], pad=0.1),
    dict(v=(V, 'a6', 'earl', "Nobody was more surprised than me."), fn=earl_surf, sfx=[('library/sfx/pond_bloop.mp3', 0.0, 0.5)], pad=0.15),
    dict(v=(V, 'a7', 'earl', "Hurricane season starts June FIRST."), fn=storm_end, sfx=[('library/sfx/sax_sting_swell.mp3', 0.3, 0.5, 0.0, 3.0), ('library/sfx/thunder_crack.mp3', 2.0, 0.6, 0.0, 1.6)], pad=0.2, flash=[2.2]),
    dict(dur=2.6, fn=endcard, cap=None, sfx=[('library/sfx/hurricane_wind_howl.mp3', 0.0, 0.6, 0.0, 2.6)]),
], beds=[('library/sfx/amb_beach.mp3', 8.0, 0.0, None, 0.6, False), ('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, 14.0, 0.2, True)], hud=False, chapter='Post-Credits Scene')
