"""Title sequence: fake studio card, then the neon title read by Earl."""
from shots import *

def studio(ctx, t, u, dur):
    big = np.zeros((H_, W_, 3), np.uint8); big[:] = (24, 8, 44)
    k = sm(u / 0.3)
    ptext(big, 'A BEIGE PICTURES PRODUCTION', W_ // 2, 480, 44, (255, 200, 236), (10, 2, 20))
    if u > 0.6:
        ptext(big, 'APPROVED BY THE BOARD (BRENDA)', W_ // 2, 600, 30, (0, 214, 232), (10, 2, 20))
    return big


_T = title_card(['SUNNY PALMS', 'HOA'], 'THE COMPLETE SEASON', 110, bg='yard', dimk=0.55, pan=12)


def main_title(ctx, t, u, dur):
    big = _T(ctx, t, u, dur)
    if int(u * 2.5) % 2 == 0: ptext(big, "EARL'S CUT  •  FINES MAY APPLY", W_ // 2, 985, 26, (255, 236, 120), (20, 6, 40))
    return big


BLOCK = Block('title', [
    dict(dur=1.5, fn=studio, sfx=[('library/sfx/stamp.mp3', 0.9, 0.9), ('library/sfx/shop_bell.mp3', 0.2, 0.3)], cap=None),
    dict(v=('movie_t', 't1', 'earl', "Sunny Palms HOA. The complete season. Fines may apply."), lead=0.3, fn=main_title, pad=0.5,
         sfx=[('library/sfx/whoosh.mp3', 0.0, 0.7, 0.0, 0.7), ('library/sfx/sax_sting_swell.mp3', 0.15, 0.25, 0.0, 1.2)], cap=None),
], beds=[('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 1.4, None, 0.3, True)], hud=False)
