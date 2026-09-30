"""Chapter 6 «Vote Earl» (E06): the election; Dale becomes president and fines Brenda."""
from shots import *

CB = 'clubhouse'
PD = (330.0, 600.0, 16.0); PB = (760.0, 600.0, 16.0)


def pod_d(C, v, t, u): UP.podium_front(C, v.cam(PD[0], PD[1], PD[2]))
def pod_b(C, v, t, u): UP.podium_front(C, v.cam(PB[0], PB[1], PB[2], flip=True))
def fines_board(L, h): UP.clipboard(L, h, -0.12, w=4.6, hh=6.2, title='FINES')
def notice250(L, h): UP.notice(L, h, -0.2, 5.4, 6.8, '$250')


def dcu(expr, **kw): return cu('dale', CB, 1.3, 0.06, expr=expr, front=pod_d, **kw)
def bcu(expr, **kw): return cu('brenda', CB, 1.3, 0.06, expr=expr, front=pod_b, **kw)


def confetti(big, t, k=1.0, n=90):
    rng = np.random.default_rng(3)
    cols = ((255, 90, 150), (90, 210, 240), (255, 220, 70), (120, 220, 120), (255, 255, 255))
    for i in range(int(n * k)):
        x = int(rng.uniform(0, W_)); ph = (t * 0.7 + rng.uniform(0, 1)) % 1.0
        y = int(ph * (H_ + 200) - 100); w = int(rng.integers(10, 24))
        x = int(x + 40 * math.sin(t * 5 + i))
        if 0 <= y < H_ - w and 0 <= x < W_ - w: big[y:y + w, x:x + w * 2 // 3] = cols[i % 5]


def estab(ctx, t, u, dur):
    cast = [dict(who='dale', x=430, y=602, u=8.6, expr='smug', shades=True, mute=True), dict(who='brenda', x=850, y=602, u=8.6, flip=True, expr='sweet', mute=True)]
    def front(C, v, tt, uu):
        UP.podium_front(C, v.cam(430.0, 602.0, 8.6)); UP.podium_front(C, v.cam(850.0, 602.0, 8.6, flip=True))
        UP.crowd_back(C, v, 14, 720.0, 200.0, 1100.0, 9.0, tt, 0.4)
    def after(big, v, tt, uu):
        ptext(big, 'HOA ELECTION', W_ // 2, 190, 52, (255, 236, 120), (30, 10, 50))
    return scene(ctx, t, u, dur, CB, cast, (640, 470, 1.05, 640, 470, 1.2), front=front, after=after)


def cheer(ctx, t, u, dur):
    cast = [dict(who='dale', x=430, y=602, u=8.6, expr='cheer', pose=U.DPOSE['cheer'], hand_n=U.H(8.6, 26.0 - 1.4 * math.sin(u * 20)), mute=True, legs=False),
            dict(who='brenda', x=850, y=602, u=8.6, flip=True, expr='hollow', mute=True, legs=False)]
    def front(C, v, tt, uu):
        UP.podium_front(C, v.cam(430.0, 602.0, 8.6)); UP.podium_front(C, v.cam(850.0, 602.0, 8.6, flip=True))
        UP.crowd_back(C, v, 14, 720.0, 200.0, 1100.0, 9.0, tt, 1.0)
    big = scene(ctx, t, u, dur, CB, cast, (640, 470, 1.05), front=front, shake=5 * max(0.0, 1 - u / 0.8))
    confetti(big, t)
    return big


def vote(ctx, t, u, dur):
    Z = 1.6
    ST.set_px(ST.px_for_zoom(Z))
    v = view_at(world(CB), 330, 505, Z, 320, 190)
    big = v.bg(); CH, _ = K.begin(Z)
    for k, t0 in enumerate((0.0, 0.85)):
        p = (u - t0) / 0.45
        if 0 <= p < 1.0: UP.ballot_paper(CH, v, 415.0 + 3 * k, lerp(455.0, 520.0, p * p), 1.0, 0.3 * math.sin(p * 6))
    UP.ballot_box(CH, v, 415.0, 590.0, 0.9)
    CH.comp(big, K.light_yard(v))
    UP.tally_overlay(big, v, 1 if u > 0.4 else 0, 1 if u > 1.25 else 0, 250.0, 470.0)
    fx.vignette(big, 0.25)
    return big


def ballot_front(t):
    def f(CH, v):
        EX, EY, EU = POND[CB]
        UP.ballot_in_mouth(CH, v.cam(EX, EY, EU), 0.0, 'DALE')
    return f


def earl_b(ctx, t, u, dur): return earl_cu(ctx, t, u, dur, CB, lid=0.5, Z=2.4, front=ballot_front(t))
def earl_plain(ctx, t, u, dur): return earl_cu(ctx, t, u, dur, CB, lid=0.5, Z=2.4 + J(u, 1.6, 0.4))


def visor(ctx, t, u, dur):
    on = u > 0.3
    big = cu('dale', CB, 1.35, 0.1, expr='smug' if on else 'cheer', shades=False, visor=on, front=pod_d, red=0.1)(ctx, t, u, dur)
    if 0.3 <= u < 0.45: O.flash(big, 0.5 * (1 - (u - 0.3) / 0.15))
    if 0.3 <= u < 0.6: B.shake(big, t, 8 * (1 - (u - 0.3) / 0.3), 33)
    return big


def tail(ctx, t, u, dur):
    z = lerp(1.38, 1.24, sm(u / dur))
    cast = [dict(who='dale', x=600, y=602, u=10.0, pose=U.DPOSE['hold'], hand_n=U.H(6.4, 12.4), prop_n=fines_board, expr='smug', visor=True),
            dict(who='brenda', x=850, y=602, u=10.0, flip=True, pose=U.BPOSE['stand'], hand_n=U.H(3.4, 12.4), prop_n=notice250, expr='shock', sweat=1.0)]
    return scene(ctx, t, u, dur, CB, cast, (720, 400, z), vig=0.28)


V6 = 'ep06_t'
BLOCK = Block('ch6', [
    dict(dur=2.0, fn=estab, cap=None, sfx=[('library/sfx/whoosh.mp3', 0.0, 0.7, 0.0, 0.6), ('library/sfx/stamp.mp3', 0.35, 0.8), ('library/sfx/crowd_cheer_short.mp3', 0.2, 0.4, 0.0, 1.5)]),
    dict(v=(V6, 'd1', 'dale', "Vote Dale! I promise FEWER fines!"), fn=dcu('shout', red=0.35), st=[('VOTE DALE', (255, 110, 190), 70, 1400, 250, 0.1, 2.4)], sfx=[('library/sfx/crowd_cheer_short.mp3', 2.4, 0.3, 0.0, 1.0)]),
    dict(v=(V6, 'b1', 'brenda', "Dale, you owe almost six thousand dollars in FINES."), fn=cuts([(0, bcu('sweet')), (2.4, bcu('sweet', zoom=0))]), pad=0.1),
    dict(v=(V6, 'd2', 'dale', "Exactly. Nobody knows the fines BETTER."), fn=dcu('smug', shades=True), pad=0.1),
    dict(v=(V6, 'b2', 'brenda', "Any resident may run. Rules are RULES."), fn=cuts([(0, bcu('hollow')), (1.3, bcu('evil'))])),
    dict(v=(V6, 'd3', 'dale', "My platform is simple. I will fine NOBODY. Except Brenda."), fn=cuts([(0, dcu('smug')), (2.2, dcu('smug', shades=True, red=0.3)), (3.0, dcu('cheer'))]), pad=0.1),
    dict(dur=1.7, fn=cheer, cap=None, sfx=[('library/sfx/crowd_cheer_short.mp3', 0.0, 0.9)], st=[('[CROWD GOES WILD]', (255, 255, 255), 30, 960, 1010, 0.1, 1.6)], mosaic=[0.0]),
    dict(dur=2.1, fn=vote, cap=None, sfx=[('library/sfx/ballot_drop.mp3', 0.0, 0.9), ('library/sfx/ballot_drop.mp3', 0.85, 0.9)], mosaic=[0.0]),
    dict(v=(V6, 'e1', 'earl', "I vote DALE. He's the main character."), fn=earl_b, sfx=[('library/sfx/pond_bloop.mp3', 0.0, 0.5)], lead=0.05),
    dict(v=(V6, 'b3', 'brenda', "That's an ALLIGATOR."), fn=bcu('shock', sweat=1.0, zoom=0.14), sfx=[('library/sfx/crowd_gasp.mp3', 0.0, 0.9)]),
    dict(v=(V6, 'e2', 'earl', "Resident since nineteen eighty-SEVEN."), fn=earl_plain, st=[('RESIDENT SINCE 1987', (255, 226, 110), 46, 960, 250, 0.4, 2.6)]),
    dict(v=(V6, 'b4', 'brenda', "Two to one. Dale WINS."), fn=bcu('hollow', sweat=0.6, lean=0.3), sfx=[('library/sfx/gavel_bang.mp3', 2.4, 0.9)], st=[('DALE 2 - BRENDA 1', (255, 236, 120), 52, 960, 250, 0.4, 2.9)], pad=0.1),
    dict(v=('ep01_t', 'd5', 'dale', "YES!"), fn=dcu('cheer', shades=True, hand_n=U.H(8.6, 26.0), zoom=0.15), sfx=[('library/sfx/coin_clink.mp3', 0.0, 0.4, 0.0, 0.5), ('library/sfx/crowd_cheer_short.mp3', 0.1, 0.6), ('library/sfx/sax_sting_swell.mp3', 0.8, 0.5)],
         st=[('AURA +9999', (255, 236, 96), 60, 1400, 250, 0.05, 1.2)], flash=[0.0], pad=0.05),
    dict(dur=1.4, fn=visor, sfx=[('library/sfx/stamp.mp3', 0.3, 0.8), ('library/sfx/sax_sting_swell.mp3', 0.0, 0.5, 0.0, 1.4)], st=[('[SAXOPHONE GETS LOUDER]', (255, 255, 255), 30, 960, 1010, 0.0, 1.4), ('PRESIDENT DALE', (255, 226, 110), 66, 960, 250, 0.4, 1.4)], cap=None),
    dict(v=(V6, 'd4', 'dale', "Morning, Brenda. Your mailbox is BONE."), fn=cuts([(0, dcu('smug', visor=True, hand_n=U.H(5.6, 12.6), prop_n=fines_board)), (1.7, dcu('smug', visor=True, hand_n=U.H(5.6, 12.6), prop_n=fines_board, zoom=0.14))]), fines='$250 (BRENDA)', fines_dt=2.4),
    dict(v=(V6, 'b5', 'brenda', "It's BEIGE!"), fn=cu('brenda', CB, 1.35, 0.1, expr='shock', hand_n=U.H(5.6, 13.2), prop_n=notice250, sweat=0.8), sfx=[('library/sfx/paper_unroll.mp3', 0.0, 0.4, 0.0, 0.8), ('library/sfx/crowd_gasp.mp3', 0.5, 0.4, 0.0, 1.0)],
         st=[('FINE: $250', (255, 84, 96), 90, 960, 250, 0.2, 1.4)], pad=0.08),
    dict(v=(V6, 'd5', 'dale', "The approved color is Ecru Whisper."), fn=dcu('smug', visor=True, hand_n=U.H(5.6, 12.6), prop_n=fines_board, zoom=0.1)),
    dict(v=(V6, 'b6', 'brenda', "That's the SAME color!"), fn=cu('brenda', CB, 1.35, 0.14, expr='evil', hand_n=U.H(5.6, 13.2), prop_n=notice250, sweat=0.6), sfx=[('library/sfx/record_scratch.mp3', 0.0, 0.5, 0.0, 0.8)]),
    dict(v=(V6, 'd6', 'dale', "Bless your HEART."), fn=cu('dale', CB, 1.4, 0.14, expr='smug', visor=True, shades=None, lean=0.3, front=pod_d), sfx=[('library/sfx/sax_sting_swell.mp3', 0.0, 0.5, 0.0, 2.6)],
         st=[('(TRANSLATION: YOU IDIOT)', (255, 190, 226), 34, 960, 760, 0.1, 1.5), ('[SAXOPHONE GETS LOUDEST]', (255, 255, 255), 30, 960, 1010, 0.0, 1.5)]),
    dict(v=(V6, 'e3', 'earl', "Well. That's FLORIDA."), fn=earl_plain, sfx=[('library/sfx/pond_bloop.mp3', 0.0, 0.5)], pad=0.3),
    dict(dur=1.6, fn=tail, cap=None, sfx=[('library/sfx/paper_crumple_slap.mp3', 0.0, 0.6)]),
], beds=[('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.22, True), ('library/sfx/amb_bbq_chatter.mp3', 6.5, 0.0, None, 0.28, False), ('library/sfx/grill_sizzle.mp3', 6.5, 0.0, 19.0, 0.25, False)],
    card=(6, 'VOTE EARL', 'FINES SO FAR: $5,947.63'), chapter='Chapter 6: Vote Earl')
