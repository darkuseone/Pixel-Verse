"""Press briefing after the hurricane: Kevin is in collections."""
from shots import *
from props.folk import H


def pod(x, y, u):
    def f(C, v, t, uu): UP.podium_front(C, v.cam(x, y, u, flip=True))
    return f


def crowd_front(C, v, t, u): UP.crowd_back(C, v, 12, 730.0, 300.0, 1000.0, 9.5, t, 0.2)


def flashes(big, v, t, u):
    for i, (ft, cx, cy) in enumerate(((0.2, 480, 640), (0.9, 700, 700), (1.5, 1300, 660), (2.3, 1000, 620), (3.0, 800, 690), (3.7, 1500, 650), (4.4, 560, 700))):
        fu = (u - ft)
        if 0 <= fu < 0.12: fx.flash_burst(big, cx, cy, 0.45 * (1 - fu / 0.12))


def wide(ctx, t, u, dur):
    cast = [dict(who='brenda', x=760, y=606, u=8.6, flip=True, pose=U.BPOSE['stand'], expr='sweet')]
    def after(big, v, tt, uu):
        flashes(big, v, tt, uu)
        ptext(big, 'HOA PRESS BRIEFING', W_ // 2, 190, 44, (255, 236, 120), (30, 10, 50))
    return scene(ctx, t, u, dur, 'clubhouse', cast, (700, 470, 1.15, 720, 470, 1.3), front=lambda C, v, tt, uu: (pod(760, 606, 8.6)(C, v, tt, uu), crowd_front(C, v, tt, uu)), after=after)


def cu_p(expr, **kw):
    def fn(ctx, t, u, dur):
        return cu('brenda', 'clubhouse', 1.35, 0.06, expr=expr, front=lambda C, v, tt, uu: UP.podium_front(C, v.cam(760.0, 600.0, 16.0, flip=True)), after=flashes, **kw)(ctx, t, u, dur)
    return fn


def earl_pip(ctx, t, u, dur):
    base = wide(ctx, t, u, dur)
    pip(base, earl_cu(ctx, t, u, dur, 'clubhouse', lid=0.5, Z=2.3, zoom=0.03), 'br', 700, 1.0)
    return base


BLOCK = Block('presser', [
    dict(v=('movie_t', 'p1', 'brenda', "Hurricane Kevin has failed to respond to our NOTICE."), fn=wide, lead=0.1, sfx=[('library/sfx/camera_flash.mp3', 0.2, 0.6), ('library/sfx/camera_flash.mp3', 0.9, 0.5), ('library/sfx/camera_flash.mp3', 1.5, 0.5),
                                                                                                                      ('library/sfx/camera_flash.mp3', 2.3, 0.5), ('library/sfx/whoosh.mp3', 0.0, 0.4, 0.0, 0.5)], mosaic=[0.0]),
    dict(v=('movie_t', 'p2', 'brenda', "Late fee: two hundred fifty dollars. Kevin is now in COLLECTIONS."), fn=cuts([(0, cu_p('sweet', pose=U.BPOSE['hands'])), (2.7, wide)]),
         sfx=[('library/sfx/camera_flash.mp3', 0.6, 0.5), ('library/sfx/cash_register.mp3', 2.0, 0.7), ('library/sfx/stamp.mp3', 3.6, 0.9)], st=[('LATE FEE: $250', (255, 84, 96), 70, 700, 300, 1.3, 3.2), ('KEVIN: IN COLLECTIONS', (255, 236, 120), 44, 960, 260, 3.5, 5.2)]),
    dict(v=('movie_t', 'p3', 'earl', "Kevin is in Georgia. Georgia has been notified."), fn=earl_pip, pad=0.25, lead=0.1, st=[('GEORGIA: NOTIFIED', (255, 236, 120), 44, 700, 300, 1.4, 3.4)]),
], beds=[('library/sfx/amb_bbq_chatter.mp3', 6.5, 0.0, None, 0.3, False), ('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.16, True)], hud=True, chapter='Press Briefing')
