"""Cold open: the last frame of the season (President Dale fines Brenda) -> pause -> Earl explains -> VHS rewind to the start."""
from kit import *

HOOK = O.neon_title(['HOW DID THIS MAN', 'BECOME PRESIDENT?'], 60, width=W_)
_F = {}


def fines_board(L, h): UP.clipboard(L, h, -0.12, w=4.6, hh=6.2, title='FINES')
def notice250(L, h): UP.notice(L, h, -0.2, 5.4, 6.8, '$250')


def finale(ctx, t, u, dur, mute=False):
    z = lerp(1.24, 1.38, sm(t / 2.35))
    cast = [dict(who='dale', x=600, y=602, u=10.0, pose=U.DPOSE['hold'], hand_n=U.H(6.4, 12.4), prop_n=fines_board, expr='smug', visor=True, mute=mute),
            dict(who='brenda', x=850, y=602, u=10.0, flip=True, pose=U.BPOSE['stand'], hand_n=U.H(3.4, 12.4), prop_n=notice250, expr='shock', sweat=1.0, mute=mute)]
    return scene(None if mute else ctx, min(t, 2.35), u, dur, 'clubhouse', cast, (720, 400, z), shake=(9 * hit(t, 0.0, 0.5)), vig=0.28)


def frozen(ctx):
    if 'f' not in _F:
        big = finale(None, 2.3, 2.3, 2.35, mute=True)
        g = big.astype(np.float32).mean(2, keepdims=True)
        _F['f'] = (big * 0.55 + g * 0.45).astype(np.uint8)          # slightly desaturated: PAUSE
    return _F['f'].copy()


def hook_txt(big, t):
    k = min(1.0, t / 0.1)
    O.overlay(big, HOOK, 0, 26, k)


def pause_icon(big, t):
    if int(t * 2) % 2 == 0:
        ptext(big, '|| PAUSE', 170, 118, 26, (255, 255, 255), (20, 6, 40))


def b_hook(ctx, t, u, dur):
    big = finale(ctx, t, u, dur)
    hook_txt(big, t)
    return big


def b_talk(ctx, t, u, dur):
    big = frozen(ctx)
    hook_txt(big, 9)
    pause_icon(big, t)
    pip(big, earl_cu(ctx, t, u, dur, 'clubhouse', lid=0.5, Z=2.3, zoom=0.03), 'br', 700)
    return big


def b_rewind(ctx, t, u, dur):
    big = frozen(ctx)
    k = sm(u / dur)
    day = int(lerp(42, 1, k ** 1.5))
    vhs(big, t, 1.0)
    ptext(big, '<< REW', 190, 118, 30, (255, 255, 255), (20, 6, 40))
    ptext(big, f'DAY {day}', W_ // 2, 540, 96, (255, 236, 120), (40, 10, 88))
    ptext(big, '6 WEEKS EARLIER', W_ // 2, 660, 34, (0, 214, 232), (20, 6, 40))
    if u > dur - 0.25: O.flash(big, (u - (dur - 0.25)) / 0.25)
    return big


BLOCK = Block('cold', [
    dict(v=('ep06_t', 'b5', 'brenda', "It's BEIGE!"), dur=2.35, fn=b_hook, sfx=[('library/sfx/paper_crumple_slap.mp3', 0.0, 0.9), ('library/sfx/crowd_gasp.mp3', 0.15, 0.5)], cap=None),
    dict(v=('movie_t', 'x1', 'earl', "That's Dale. He owes five thousand nine hundred dollars in FINES."), lead=0.25, fn=b_talk, sfx=[('library/sfx/record_scratch.mp3', 0.0, 0.9)], pad=0.12,
         cap=None),
    dict(v=('movie_t', 'x2', 'earl', "He is also the PRESIDENT now. Let me explain."), lead=0.1, fn=b_talk, pad=0.15, cap=None),
    dict(v=('movie_t', 'x3', 'earl', "Rewinding. Please keep your PERMIT visible."), lead=0.1, fn=b_talk, pad=0.3, cap=None),
    dict(dur=1.9, fn=b_rewind, sfx=[('library/sfx/vhs_rewind.mp3', 0.0, 0.9), ('library/sfx/tv_static_blip.mp3', 1.6, 0.6)], cap=None),
], beds=[('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, 2.45, 0.3, False),
         ('library/sfx/amb_florida_yard.mp3', 7.8, 2.3, None, 0.2, False)], hud=False)
