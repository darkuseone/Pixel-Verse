"""Chapter 3 «Suspicious Man (Walking)» (E03)."""
from shots import *
from props import folk as F

MB = (345.0, 478.0)
WU = 6.4

def ph(screen): return lambda L, h: UP.phone(L, h, 0.0, screen=screen)
def cal(L, h): UP.clipboard(L, h, -0.15, w=4.4, hh=6.0, title='CALENDAR')
def tape(L, h): UP.tape_hold(L, h)


def b_estab(ctx, t, u, dur):
    x = lerp(250.0, 470.0, u / dur)
    cast = [dict(who='dale', x=x, y=606, u=8.6, pose=U.dwalk(t, 9.0, 0.4), prop_n=UP.trash_bag, expr='normal', mute=True)]
    return scene(ctx, t, u, dur, 'yard', cast, (360, 470, 1.25, 460, 470, 1.25))


def feed_draw(big, t, u, dur): UP.neighbornet_feed(big, t, u)


def ring(ctx, t, u, dur):
    Z = 1.15
    ST.set_px(ST.px_for_zoom(Z))
    v = view_at(world('yard'), 430, 490, Z, 320, 190)
    big = v.bg(); CH, _ = K.begin(Z)
    mbx = MB[0] - 26.0 * sm((u - 1.55) / 0.45)
    UP.mailbox_world(CH, v, mbx, MB[1], 0.0, t, s=0.75)
    if u > 1.0:
        L = Layer(v.wcam()); UP.ell(L, (338 + 6 * u, 560), 16, 5, (96, 66, 46), 0, (130, 92, 62), (60, 40, 28)); CH.add(L)
    CH.comp(big, K.light_yard(v))
    C2 = Chars(); bx = 395.0
    if u < 0.9:
        x = lerp(700.0, bx, u / 0.9)
        U.brenda(C2, v.cam(x, 592.0, 8.4, flip=True), U.bwalk(t, 9.0, 0.5, 'shoulder'), t, 0.0, 'sweet', 0.0, hand_n=U.H(2.2, 19.6), prop_n=lambda L, h: UP.shovel(L, h, -2.4), outfit='robe', blink=False)
    elif u < 1.55:
        dig = 0.9 * math.sin((u - 0.9) * 12)
        U.brenda(C2, v.cam(bx, 592.0, 8.4, flip=True), U.BPOSE['shovel'], t, 0.0, 'evil', 0.0, hand_n=U.H(6.8, 12.0 + dig), prop_n=lambda L, h: UP.shovel(L, h, 1.0), outfit='robe')
    elif u < 2.4:
        U.brenda(C2, v.cam(bx, 592.0, 8.4, flip=True), U.BPOSE['point'], t, 0.0, 'evil', 0.0, hand_n=U.H(6.6 + 1.2 * math.sin(u * 10), 16.2), outfit='robe')
    elif u < 3.1:
        U.brenda(C2, v.cam(bx, 592.0, 8.4, flip=True), U.BPOSE['measure'], t, 0.0, 'sweet', 0.0, hand_n=U.H(6.8, 11.6), prop_n=UP.tape_hold, outfit='robe')
    else:
        U.brenda(C2, v.cam(bx, 592.0, 8.4, flip=True), dict(U.BPOSE['wave'], n=(5.4, 22.6 + 1.6 * math.sin(t * 14))), t, 0.0, 'sweet', 0.0, outfit='robe', blink=False)
    C2.comp(big, K.light_yard(v))
    if 2.4 <= u < 3.1:
        L = Layer(v.wcam()); k = sm((u - 2.4) / 0.25); x0 = 372.0; x1 = x0 - 74 * k
        UP.cap(L, (x0, 510), (x1, 510), 2.6, 2.6, (255, 214, 50)); UP.cap(L, (x0, 510), (x1, 510), 0.5, 0.5, (30, 30, 34))
        FX = Chars(); FX.add(L); FX.comp(big)
    if u < 0.15:
        r = np.random.default_rng(int(t * 60))
        for i in range(10):
            y0 = int(r.integers(0, 1000)); big[y0:y0 + 18] = np.roll(big[y0:y0 + 18], int(r.integers(-160, 160)), 1)
    UP.ring_look(big, t)
    return big


def cat_hook(t):
    def f(CH, v):
        EX, EY, EU = POND['yard']
        F.cat(CH, v.cam(EX - 2.6 * EU, EY - 3.7 * EU, EU * 0.42), t, 'loaf', 0.0, 0.55 if (t % 4.5) > 0.2 else 0.95, (0.0, 0.0), 'deadpan', tail=0.5)
    return f


def b_earl(ctx, t, u, dur):
    return earl_cu(ctx, t, u, dur, 'yard', lid=0.5, Z=2.3, front=cat_hook(t), dy=8, dx=14)


V3 = 'ep03_t'
PING = 'library/sfx/app_notify_ping.mp3'
BLOCK = Block('ch3', [
    dict(dur=2.0, fn=b_estab, cap=None, sfx=[('library/sfx/whoosh.mp3', 0.0, 0.7, 0.0, 0.6), ('library/sfx/stamp.mp3', 0.35, 0.8)]),
    dict(v=(V3, 'd1', 'dale', "'Suspicious man. Walking.' Who is WALKING?!"), fn=cuts([(0, cu('dale', 'yard', 1.3, 0.05, expr='incredulous', hand_n=U.H(6.4, 14.6), prop_n=ph('feed'), red=0.3, look=0.2)),
                                                                                    (1.6, cu('dale', 'yard', 1.5, 0.05, expr='shout', hand_n=U.H(6.4, 14.6), prop_n=ph('feed'), red=0.6))]), sfx=[(PING, 0.0, 0.6)]),
    dict(v=(V3, 'b1', 'brenda', "You are, Dale. It's on my RING."), fn=cu('brenda', 'yard', 1.3, 0.05, expr='sweet', hand_n=U.H(6.2, 13.0), prop_n=ph('ring')), sfx=[('library/sfx/whoosh.mp3', 0.0, 0.3, 0.0, 0.5)]),
    dict(v=(V3, 'd2', 'dale', "I was taking out the TRASH!"), fn=cu('dale', 'yard', 1.3, 0.06, expr='shout', red=0.7, sweat=0.5, hand_n=U.H(6.4, 12.4), prop_n=UP.trash_bag), sfx=[('library/sfx/fist_slam_counter.mp3', 0.15, 0.5)], pad=0.1),
    dict(v=(V3, 'b2', 'brenda', "Trash is Tuesday. Today is Wednesday. SUSPICIOUS."), fn=cuts([(0, cu('brenda', 'yard', 1.3, 0.05, expr='bright', hand_n=U.H(3.4, 10.6), prop_n=cal)),
                                                                                                 (2.4, cu('brenda', 'yard', 1.55, 0.05, expr='sweet', hand_n=U.H(3.4, 10.6), prop_n=cal))]),
         st=[('TRASH = TUESDAY', (150, 255, 170), 58, 700, 300, 0.9, 2.2), ('TODAY = WEDNESDAY', (255, 100, 100), 52, 700, 300, 2.3, 4.0)]),
    dict(dur=2.6, fn=portrait_insert(feed_draw, 'yard', 1040), cap=None, sfx=[(PING, 0.3, 0.6), (PING, 0.85, 0.6), (PING, 1.4, 0.6), (PING, 1.95, 0.6)], mosaic=[0.0]),
    dict(v=(V3, 'd3', 'dale', "Fine. I have a Ring too. It's mostly pointed at my TRUCK."), fn=cuts([(0, cu('dale', 'yard', 1.3, 0.05, expr='sly', shades=True, hand_n=U.H(6.8, 14.4), prop_n=ph('truck'), red=0.25)),
                                                                                                     (2.2, cu('dale', 'yard', 1.55, 0.04, expr='sly', shades=True, hand_n=U.H(6.8, 14.4), prop_n=ph('truck'), red=0.25))]),
         st=[('47 CLIPS OF HIS TRUCK', (255, 236, 120), 40, 700, 300, 0.6, 2.9), ('[SAXOPHONE GETS LOUDER]', (255, 255, 255), 30, 960, 1010, 2.4, 3.9)], sfx=[('library/sfx/sax_sting_swell.mp3', 2.2, 0.42, 0.0, 1.6)]),
    dict(dur=3.85, fn=ring, cap=None, mosaic=[0.0], sfx=[('library/sfx/camera_glitch.mp3', 0.0, 0.7), ('library/sfx/doorbell_chime.mp3', 0.25, 0.55), ('library/sfx/shovel_dig_dirt.mp3', 1.15, 0.8),
                                                    ('library/sfx/mailbox_rip.mp3', 1.95, 0.45, 0.0, 1.0), ('library/sfx/tape_measure.mp3', 2.65, 0.8), ('library/sfx/camera_glitch.mp3', 3.75, 0.6)],
         st=[('6 INCHES', (255, 236, 90), 100, 1400, 300, 2.5, 3.6)]),
    dict(v=(V3, 'd4', 'dale', "She moved my mailbox. SIX inches."), fn=cu('dale', 'yard', 1.4, 0.1, expr='shock', shades=None, sweat=0.9, red=0.05, look=0.3, pose=U.DPOSE['stand'])),
    dict(v=(V3, 'b3', 'brenda', "Routine compliance MEASUREMENT."), fn=cu('brenda', 'yard', 1.35, 0.06, expr='sweet', hand_n=U.H(4.4, 11.4), prop_n=tape)),
    dict(v=(V3, 'd5', 'dale', "It's on CAMERA!"), fn=cu('dale', 'yard', 1.3, 0.15, expr='cheer', shades=True, hand_n=U.H(8.6, 26.0)), sfx=[('library/sfx/coin_clink.mp3', 0.05, 0.4, 0.0, 0.6)], st=[('AURA +9999', (255, 236, 96), 60, 1400, 250, 0.05, 1.2)], flash=[0.0], pad=0.08),
    dict(v=(V3, 'b4', 'brenda', "Only approved doorbells are admissible. Yours is BLACK."), fn=cuts([(0, cu('brenda', 'yard', 1.3, 0.05, expr='sweet', pose=U.BPOSE['hands'], lean=0.3)),
                                                                                                     (2.0, cu('brenda', 'yard', 1.55, 0.05, expr='evil', pose=U.BPOSE['hands'], lean=0.3))]),
         sfx=[('library/sfx/record_scratch.mp3', 0.0, 0.6, 0.0, 0.8), ('library/sfx/sad_trombone.mp3', 2.6, 0.4, 0.0, 1.6)], st=[('AURA -9999', (255, 100, 100), 60, 1400, 250, 2.7, 3.9)]),
    dict(v=(V3, 'd6', 'dale', "So the doorbell has to be BEIGE?!"), fn=cu('dale', 'yard', 1.35, 0.08, expr='shout', shades=None, red=0.9, sweat=0.7, pose=U.DPOSE['shout']), sfx=[('library/sfx/fist_slam_counter.mp3', 0.0, 0.5)]),
    dict(v=(V3, 'b5', 'brenda', "Ecru WHISPER."), fn=cu('brenda', 'yard', 1.4, 0.06, expr='bright', pose=U.BPOSE['hands'], lean=0.3), sfx=[('library/sfx/shop_bell.mp3', 0.0, 0.4)], st=[('ECRU WHISPER', (250, 232, 190), 64, 700, 300, 0.05, 1.4)]),
    dict(v=('ep01_t', 'b3', 'brenda', "Bless your heart."), fn=cu('brenda', 'yard', 1.4, 0.06, expr='sweet', lean=0.4, pose=U.BPOSE['hands']), st=[('(TRANSLATION: YOU IDIOT)', (255, 190, 226), 34, 960, 760, 0.1, 1.5)], fines='$1,150', fines_dt=0.2, pad=0.15),
    dict(v=(V3, 'e1', 'earl', "Haven't seen any CAT."), fn=b_earl, sfx=[('library/sfx/pond_bloop.mp3', 0.0, 0.5)], pad=0.3),
], beds=[('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.24, True), ('library/sfx/amb_florida_yard.mp3', 7.8, 0.0, None, 0.32, False)],
    card=(3, 'SUSPICIOUS MAN (WALKING)', 'FINES SO FAR: $1,050'), chapter='Chapter 3: Suspicious Man (Walking)')
