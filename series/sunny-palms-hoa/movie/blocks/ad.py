"""Commercial break: Sunny Palms Realty (Brenda as the announcer)."""
from shots import *


def crt_post(big, t, u=0): crt(big, 1.0)


def ad_bug(big, u, label='SPONSORED BY BRENDA'):
    ptext(big, 'COMMERCIAL BREAK', 260, 118, 26, (255, 255, 255), (20, 6, 40))


def a_open(ctx, t, u, dur):
    base = cu('brenda', 'clubhouse', 1.25, 0.05, expr='bright', pose=U.BPOSE['wave'], hand_n=U.H(5.6, 22.6))(ctx, t, u, dur)
    ptext(base, 'SUNNY PALMS REALTY', W_ // 2, 200, 52, (255, 236, 120), (60, 20, 10))
    ptext(base, 'LIVE WHERE EVERY HOUSE IS THE SAME COLOR', W_ // 2, 880, 26, (255, 255, 255), (60, 20, 10))
    ad_bug(base, u); crt(base, 1.0)
    return base


def a_swatches(ctx, t, u, dur):
    names = ['BONE', 'BEIGE', 'IVORY', 'ECRU WHISPER']
    def draw(big, tt, uu, d):
        for i, nm in enumerate(names):
            if uu < 0.25 + i * 0.95: continue
            k = sm((uu - 0.25 - i * 0.95) / 0.15)
            x0 = 200 + i * 400; y0 = int(300 + (1 - k) * 80)
            box = np.zeros((360, 340, 4), np.uint8); box[..., :3] = (20, 12, 30); box[..., 3] = 255
            box[10:350, 10:330, :3] = (252, 250, 244); box[26:250, 26:314, :3] = UP.BONE
            O.overlay(big, box, x0, y0, k)
            ptext(big, nm, x0 + 170, y0 + 300, 22 if len(nm) > 5 else 26, (40, 30, 60), (252, 250, 244))
        if uu > 4.1:
            ptext(big, '4 COLORS = 1 COLOR', W_ // 2, 790, 60, (255, 92, 96), (30, 12, 30))
    base = insert_dim('clubhouse', draw, 1.0, 640, 360, 0.55)(ctx, t, u, dur)
    ptext(base, 'SUNNY PALMS REALTY', W_ // 2, 200, 44, (255, 236, 120), (60, 20, 10))
    ad_bug(base, u); crt(base, 1.0)
    return base


def a_legal(ctx, t, u, dur):
    base = cu('brenda', 'clubhouse', 1.4, 0.04, expr='sweet', pose=U.BPOSE['hands'], lean=0.3)(ctx, t, u, dur)
    txt = 'FINES MAY APPLY.  FINES DO APPLY.  VOID WHERE PROHIBITED.  VOID WHERE PERMITTED.  ' * 2
    ptext(base, txt, int(2600 - u * 900), 1020, 18, (255, 255, 255), (10, 4, 20), anchor='l')
    ptext(base, 'CALL 1-800-555-BEIGE', W_ // 2, 190, 48, (255, 236, 120), (60, 20, 10))
    ad_bug(base, u); crt(base, 1.0)
    return base


BLOCK = Block('ad', [
    dict(v=('movie_t', 'r1', 'brenda', "Sunny Palms. Live where every house is the same COLOR."), fn=a_open, lead=0.2, cap=None,
         sfx=[('library/sfx/tv_static_blip.mp3', 0.0, 0.7), ('library/sfx/ad_jingle.mp3', 0.0, 0.7)]),
    dict(v=('movie_t', 'r2', 'brenda', "Bone. Beige. Ivory. Ecru Whisper. Four colors. Same COLOR."), fn=a_swatches, cap=None, pad=0.15),
    dict(v=('movie_t', 'r3', 'brenda', "Fines may apply. Fines do APPLY."), fn=a_legal, cap=None, sfx=[('library/sfx/tv_static_blip.mp3', 2.3, 0.7), ('library/sfx/record_scratch.mp3', 1.9, 0.35, 0.0, 0.6)], pad=0.3),
], beds=[('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.0, True)], hud=True, chapter='Commercial Break')
