"""Dale's campaign: he watched a video about democracy."""
from shots import *


def poster(L, h):
    cx, cy = h[0] + 0.2, h[1] + 3.6
    UP.rect(L, cx + 0.3, cy + 0.3, 8.6, 6.0, -0.06, (20, 20, 50))
    UP.rect(L, cx, cy, 8.6, 6.0, -0.06, (255, 110, 190))
    UP.ltext(L, 'VOTE', (cx, cy - 1.5), 1.5, (255, 255, 255), -0.06)
    UP.ltext(L, 'DALE', (cx, cy + 0.6), 1.9, (255, 236, 90), -0.06)
    UP.ltext(L, 'FINES?', (cx, cy + 2.4), 0.9, (60, 30, 100), -0.06)


def wide_posters(ctx, t, u, dur, mute=True):
    cast = [dict(who='dale', x=760, y=606, u=9.4, expr='cheer', shades=True, pose=U.DPOSE['hips'], mute=mute)]
    def after(big, v, tt, uu):
        C = Chars(); L = Layer(v.wcam())
        for i, x in enumerate((440, 520, 600, 680)):
            if uu < 0.15 + 0.3 * i: continue
            k = sm((uu - 0.15 - 0.3 * i) / 0.12)
            y = 606 - 8 * (1 - k)
            UP.cap(L, (x, y), (x, y - 44), 2.0, 2.0, (150, 110, 70))
            UP.rect(L, x, y - 66, 46, 34, 0.0, (255, 110, 190))
            UP.ltext(L, 'VOTE', (x, y - 74), 9, (255, 255, 255)); UP.ltext(L, 'DALE', (x, y - 60), 11, (255, 236, 90))
        C.add(L); C.comp(big, K.light_yard(v))
    return scene(ctx, t, u, dur, 'yard', cast, (600, 490, 1.2, 620, 490, 1.3), after=after)


def c2_base(ctx, t, u, dur):
    base = wide_posters(ctx, t, u + 1.6, dur)
    pip(base, earl_cu(ctx, t, u, dur, 'yard', lid=0.5, Z=2.3, zoom=0.03), 'br', 700, 1.0)
    return base


BLOCK = Block('campaign', [
    dict(v=('movie_t', 'c1', 'dale', "I'm running for PRESIDENT. I watched a video about DEMOCRACY."), fn=cuts([(0, cu('dale', 'yard', 1.3, 0.06, expr='cheer', shades=True, hand_n=U.H(6.4, 14.4), prop_n=poster, pose=U.DPOSE['hold'])),
                                                                                                             (1.7, lambda c, t, u, d: wide_posters(c, t, u, d, mute=False))]),
         st=[('ELECTION DAY: FRIDAY', (255, 236, 120), 46, 700, 300, 0.2, 1.8)], sfx=[('library/sfx/sax_sting_swell.mp3', 2.4, 0.3, 0.0, 1.0), ('library/sfx/whoosh.mp3', 1.7, 0.4, 0.0, 0.5)], mosaic=[1.7]),
    dict(v=('movie_t', 'c2', 'earl', "It was a cartoon about a beaver running for mayor. The beaver LOST."), fn=c2_base, lead=0.1, pad=0.3, st=[('THE BEAVER LOST', (255, 100, 100), 56, 1200, 300, 2.9, 4.6)],
         sfx=[('library/sfx/sad_trombone.mp3', 3.6, 0.35, 0.0, 1.6)]),
], beds=[('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.22, True), ('library/sfx/amb_florida_yard.mp3', 7.8, 0.0, None, 0.32, False)], hud=True, chapter='Campaign Trail')
