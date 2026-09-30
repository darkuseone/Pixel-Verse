"""Board meeting minutes: the board has one member."""
from shots import *

SEATS = [(410, 'PRESIDENT'), (565, 'VICE PRES.'), (730, 'TREASURER'), (880, 'SECRETARY')]
TABLE_Y = 393.0


def table_after(big, v, t, u):
    bg = v.bg()
    ys = int(v.opt(0, TABLE_Y)[1])
    if 0 <= ys < H_: big[ys:] = bg[ys:]
    for x, label in SEATS:
        cx, cy = v.opt(x + 1, 403)
        s1 = max(8, int(9 * v.Z)); s2 = max(10, int(12 * v.Z))
        ptext(big, label, int(cx), int(cy - 6 * v.Z), s1, (60, 50, 90), (250, 250, 250))
        ptext(big, 'BRENDA', int(cx), int(cy + 6 * v.Z), s2, (200, 40, 90), (250, 250, 250))


def seat(i, expr='sweet', mute=False, **kw):
    return dict(who='brenda', x=SEATS[i][0] + 6, y=528.0, u=9.0, flip=(i % 2 == 0), expr=expr, mute=mute, pose=U.BPOSE['hands'], **kw)


def at_seat(i, Z=1.65, expr='sweet', shake=0.0):
    def fn(ctx, t, u, dur):
        return scene(ctx, t, u, dur, 'board', [seat(i, expr)], (SEATS[i][0], 352, Z, SEATS[i][0], 352, Z + 0.1), after=table_after, shake=shake)
    return fn


def establishing(ctx, t, u, dur):
    big = scene(ctx, t, u, dur, 'board', [], (640, 400, 1.0, 640, 400, 1.12), after=table_after)
    ptext(big, 'HOA BOARD MEETING  •  MINUTES', W_ // 2, 190, 34, (255, 236, 120), (30, 10, 50))
    ptext(big, 'MEMBERS PRESENT: 1', W_ // 2, 250, 24, (255, 200, 236), (30, 10, 50))
    return big


def all_four(ctx, t, u, dur):
    cast = [seat(i, 'sweet', mute=True) for i in range(4)]
    base = scene(ctx, t, u, dur, 'board', cast, (640, 405, 1.0, 640, 405, 1.08), after=table_after)
    pip(base, earl_cu(ctx, t, u, dur, 'yard', lid=0.5, Z=2.3, zoom=0.03), 'bl', 520, 1.0)
    return base


BLOCK = Block('minutes', [
    dict(dur=1.4, fn=establishing, cap=None, sfx=[('library/sfx/whoosh.mp3', 0.0, 0.5, 0.0, 0.5)], mosaic=[0.0]),
    dict(v=('movie_t', 'm1', 'brenda', "The board will now vote on fining DALE."), fn=at_seat(0), lead=0.05),
    dict(v=('movie_t', 'm2', 'brenda', "Motion to fine Dale."), fn=at_seat(1), sfx=[('library/sfx/chair_scoot.mp3', 0.0, 0.7)], st=[('MOTION', (255, 236, 120), 60, 960, 250, 0.1, 1.4)], pad=0.05),
    dict(v=('movie_t', 'm3', 'brenda', "Seconded."), fn=at_seat(2), sfx=[('library/sfx/chair_scoot.mp3', 0.0, 0.7)], st=[('SECONDED', (150, 255, 170), 60, 960, 250, 0.05, 0.9)], pad=0.05),
    dict(v=('movie_t', 'm4', 'brenda', "Approved. Unanimously."), fn=at_seat(3, 1.65, 'evil', shake=0.0), sfx=[('library/sfx/chair_scoot.mp3', 0.0, 0.7), ('library/sfx/gavel_bang.mp3', 1.55, 0.9)],
         st=[('CARRIED 1 - 0', (255, 84, 96), 70, 960, 250, 1.5, 2.6)]),
    dict(v=('movie_t', 'm5', 'earl', "The board has one member. Brenda is the entire BOARD."), fn=all_four, pad=0.2, lead=0.1),
], beds=[('library/sfx/amb_boardroom.mp3', 8.0, 0.0, None, 0.5, False), ('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.16, True)], hud=True, chapter='Board Meeting Minutes')
