"""Chapter 5 «Suggested Tip» (E05): a free hot dog costs $47.63."""
from shots import *

CB = 'clubhouse'


def plate(L, h):
    UP.ell(L, h, 3.4, 1.0, (250, 250, 246), 0, (255, 255, 255), (196, 200, 208))
    UP.ell(L, h, 2.3, 0.6, (232, 236, 240))

def dog_tongs(L, h):
    UP.tongs(L, h, -0.2); UP.hot_dog(L, (h[0] + 2.9, h[1] + 0.6))

def naked(L, h): UP.hot_dog(L, h, bun=False, mustard=False)


def tab(state):
    def draw(big, t, u, dur, ctx): UP.tablet_ui(big, t, state, u, ctx.epi.talk('tablet', t))
    return portrait_insert(draw, CB, 1040, ctx_arg=True)


def video_draw(big, t, u, dur, ctx):
    UP.tablet_ui(big, t, 'video', u, ctx.epi.talk('tablet', t))
    if u > 3.0:
        k = sm((u - 3.0) / 0.5)
        im = Image.new('RGBA', (1080, 1920), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
        r = int(30 + 70 * k)
        d.ellipse([540 - r - 30, 1590 - r // 2 - 10, 540 + r + 30, 1590 + r // 2 + 10], outline=(230, 40, 60, 255), width=8)
        O.overlay(big, np.array(im), 0, 0, 1.0)


def b_estab(ctx, t, u, dur):
    cast = [dict(who='dale', x=430, y=606, u=8.6, expr='shout', pose=U.DPOSE['hold'], hand_n=U.H(6.6, 13.4), prop_n=plate, red=0.5, mute=True),
            dict(who='brenda', x=720, y=606, u=8.6, flip=True, expr='sweet', pose=U.BPOSE['show'], hand_n=U.H(4.8, 14.6), prop_n=dog_tongs, mute=True)]
    return scene(ctx, t, u, dur, CB, cast, (580, 470, 1.15, 580, 470, 1.3))


def two_shot(ctx, t, u, dur):
    cast = [dict(who='dale', x=430, y=606, u=9.0, expr='sad', shades=None, pose=U.DPOSE['hold'], hand_n=U.H(6.6, 13.4), prop_n=plate, sweat=0.6),
            dict(who='brenda', x=720, y=606, u=9.0, flip=True, expr='bright', pose=U.BPOSE['show'], hand_n=U.H(4.8, 14.6), prop_n=naked)]
    return scene(ctx, t, u, dur, CB, cast, (580, 470, 1.2, 580, 470, 1.3))


def earl_dont(ctx, t, u, dur):
    return earl_cu(ctx, t, u, dur, 'clubhouse', lid=0.5, Z=2.4)


V5 = 'ep05_t'
CH = 'library/sfx/ui_tap_chirp.mp3'
BLOCK = Block('ch5', [
    dict(dur=2.0, fn=b_estab, cap=None, sfx=[('library/sfx/whoosh.mp3', 0.0, 0.7, 0.0, 0.6), ('library/sfx/stamp.mp3', 0.35, 0.8), ('library/sfx/grill_sizzle.mp3', 0.0, 0.4, 0.0, 2.0)]),
    dict(v=(V5, 'd1', 'dale', "It's a FREE hot dog!"), fn=cu('dale', CB, 1.3, 0.06, expr='shout', hand_n=U.H(6.6, 13.4), prop_n=plate, red=0.6, sweat=0.4, look=0.2), sfx=[('library/sfx/fist_slam_counter.mp3', 0.05, 0.6)], pad=0.1),
    dict(v=(V5, 't1', 'tablet', "Would you like to add a tip? Twenty. Twenty-five. Thirty PERCENT."), fn=tab('tip'), sfx=[(CH, 0.05, 0.5), (CH, 0.3, 0.4), (CH, 0.52, 0.4), (CH, 0.74, 0.4), (CH, 2.95, 0.6)], mosaic=[0.0]),
    dict(v=(V5, 'b1', 'brenda', "Service is not FREE, Dale."), fn=cu('brenda', CB, 1.3, 0.05, expr='sweet', hand_n=U.H(4.8, 14.6), prop_n=dog_tongs)),
    dict(v=(V5, 'd2', 'dale', "Twenty percent of free is ZERO. I did the math."), fn=cuts([(0, cu('dale', CB, 1.3, 0.05, expr='sly', shades=True, hand_n=U.H(6.6, 13.4), prop_n=plate, red=0.2)),
                                                                                       (1.6, cu('dale', CB, 1.55, 0.05, expr='sly', shades=True, hand_n=U.H(6.6, 13.4), prop_n=plate, red=0.2))]),
         st=[('20% x $0 = $0', (255, 236, 120), 56, 700, 300, 0.6, 2.9)]),
    dict(v=(V5, 't2', 'tablet', "Total: forty-seven sixty-three. Includes CONVENIENCE fee."), fn=tab('receipt'), fines='$5,947.63', fines_dt=3.4,
         sfx=[('library/sfx/receipt_printer.mp3', 0.05, 0.45)] + [(CH, 0.25 + 0.34 * i, 0.35) for i in range(8)] + [('library/sfx/cash_register.mp3', 2.95, 0.8)], mosaic=[0.0]),
    dict(v=(V5, 'd3', 'dale', "What's so CONVENIENT?!"), fn=cu('dale', CB, 1.3, 0.1, expr='shout', red=0.9, sweat=0.7, pose=U.DPOSE['shout']), sfx=[('library/sfx/fist_slam_counter.mp3', 0.0, 0.5)], pad=0.08),
    dict(v=(V5, 'b2', 'brenda', "Cash has a fifteen percent SURCHARGE."), fn=cu('brenda', CB, 1.35, 0.06, expr='evil', pose=U.BPOSE['hands'], lean=0.3), st=[('CASH: +15%', (255, 100, 110), 76, 700, 300, 0.9, 2.6)]),
    dict(v=(V5, 'd4', 'dale', "Then how do I say NO?!"), fn=cu('dale', CB, 1.35, 0.08, expr='shock', sweat=0.9, look=0.5, red=0.5), pad=0.1),
    dict(v=(V5, 't3', 'tablet', "Are you sure? Brenda worked really HARD."), fn=tab('guilt'), sfx=[(CH, 0.2, 0.4), (CH, 0.6, 0.4), (CH, 1.0, 0.4)] + [('library/sfx/sad_trombone.mp3', 0.4, 0.4, 0.0, 1.6)],
         st=[('[TABLET WHIMPERS]', (255, 255, 255), 30, 960, 1010, 0.3, 2.4)], mosaic=[0.0]),
    dict(v=(V5, 'd5', 'dale', "YES."), fn=cu('dale', CB, 1.3, 0.12, expr='sad', shades=None, sweat=0.6), st=[('AURA -9999', (255, 100, 100), 60, 1400, 250, 0.05, 1.2)], pad=0.08),
    dict(v=(V5, 'b3', 'brenda', "Enjoy! Bun is EXTRA."), fn=two_shot, sfx=[('library/sfx/coin_clink.mp3', 0.6, 0.4, 0.0, 0.5)], st=[('BUN: +$1.50', (255, 236, 120), 76, 700, 300, 0.8, 2.3)]),
    dict(v=(V5, 't5', 'tablet', "Would you like to tip this VIDEO? Twenty. Twenty-five. Thirty percent."), fn=portrait_insert(video_draw, CB, 1040, ctx_arg=True),
         sfx=[('library/sfx/record_scratch.mp3', 0.0, 0.7, 0.0, 0.9), (CH, 0.8, 0.4), (CH, 1.02, 0.4), (CH, 1.24, 0.4), (CH, 3.85, 0.5)],
         st=[('[TABLET TURNS TO YOU]', (255, 255, 255), 30, 960, 1010, 0.1, 2.1), ('[NO TIP BUTTON: 4 PIXELS]', (255, 255, 255), 30, 960, 1010, 2.4, 4.3)], mosaic=[0.0]),
    dict(v=(V5, 'e1', 'earl', "DON'T."), fn=earl_dont, sfx=[('library/sfx/pond_bloop.mp3', 0.0, 0.5)], pad=0.4),
], beds=[('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.22, True), ('library/sfx/grill_sizzle.mp3', 6.5, 0.0, None, 0.3, False), ('library/sfx/amb_bbq_chatter.mp3', 6.5, 0.0, None, 0.28, False)],
    card=(5, 'SUGGESTED TIP', 'FINES SO FAR: $5,900'), chapter='Chapter 5: Suggested Tip')
