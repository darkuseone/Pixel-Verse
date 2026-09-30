"""Chapter 2 intro: Dale's plan (he stopped the video at step two)."""
from shots import *

def phone_prop(L, h): UP.phone(L, h, 0.0, screen='feed')

def dale_phone(ctx, t, u, dur, mute=True):
    return scene(ctx, t, u, dur, 'yard', [dict(who='dale', x=470, y=604, u=10.0, pose=U.DPOSE['paper'], hand_n=U.H(5.6, 19.0), prop_n=phone_prop, expr='smug', mute=mute)],
                 (490, 470, 1.35, 490, 470, 1.5))

def b_estab(ctx, t, u, dur): return dale_phone(ctx, t, u, dur)

def b_earl(ctx, t, u, dur):
    base = dale_phone(ctx, t, u, dur)
    pip(base, earl_cu(ctx, t, u, dur, 'yard', lid=0.5, Z=2.3, zoom=0.03), 'br', 700, 1.0)
    return base

BLOCK = Block('ch2i', [
    dict(dur=2.0, fn=b_estab, cap=None, sfx=[('library/sfx/whoosh.mp3', 0.0, 0.7, 0.0, 0.6), ('library/sfx/stamp.mp3', 0.35, 0.8)]),
    dict(v=('movie_t', 'i1', 'dale', "Step one: get an emotional support animal. Step two: WIN."), fn=cu('dale', 'yard', 1.3, 0.05, expr='smug', pose=U.DPOSE['paper'], hand_n=U.H(5.6, 19.0), prop_n=phone_prop, shades=True),
         st=[('STEP 1: ANIMAL', (255, 236, 120), 44, 500, 330, 0.9, 2.8), ('STEP 2: WIN', (150, 255, 170), 44, 500, 330, 2.9, 4.0)]),
    dict(v=('movie_t', 'i2', 'dale', "Step three? I stopped the video at step TWO."), fn=cu('dale', 'yard', 1.3, 0.05, expr='shock', look=0.3, pose=U.DPOSE['paper'], hand_n=U.H(5.6, 19.0), prop_n=phone_prop),
         st=[('STEP 3: ???', (255, 100, 100), 50, 500, 330, 0.2, 2.4)], sfx=[('library/sfx/record_scratch.mp3', 0.0, 0.5, 0.0, 0.6)]),
    dict(v=('movie_t', 'i3', 'earl', "The video was twelve minutes. He watched forty SECONDS."), fn=b_earl, pad=0.15, st=[('WATCHED 0:40 / 12:00', (255, 236, 120), 32, 620, 300, 1.3, 3.8)]),
], beds=[('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.24, True), ('library/sfx/amb_florida_yard.mp3', 7.8, 0.0, None, 0.32, False)],
    card=(2, 'EMOTIONAL SUPPORT FLAMINGO', 'FINES SO FAR: $750'), chapter='Chapter 2: Emotional Support Flamingo')
