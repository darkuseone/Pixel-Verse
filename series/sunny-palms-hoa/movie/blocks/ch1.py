"""Chapter 1 «Ecru Whisper» (E01): $250 for a mailbox that is the same colour as the approved one."""
from shots import *
from props.folk import H

MB = (345.0, 478.0); MBS = 0.75
POST = (338.0, 552.0)
STREET_Y = 668.0


def notice(L, h): UP.notice(L, h, -0.2, w=5.2, hh=6.8)
def clip(L, h): UP.clipboard(L, h, -0.15, w=4.4, hh=6.0)
def chipfan(L, h): UP.chip_fan(L, h, -1.6, 0.3, 1.2)
def form27(L, h): UP.clipboard(L, h, -0.12, w=4.6, hh=6.2)


def mb_before(painted=1.0, x=None, y=None, attached=True):
    def f(C, v, t, u):
        if attached: UP.mailbox_world(C, v, MB[0] if x is None else x, MB[1] if y is None else y, painted, t, s=MBS)
    return f


# ------------------------------------------------------------------ establishing + cart
def b_estab(ctx, t, u, dur):
    return scene(ctx, t, u, dur, 'yard', [], (350, 470, 1.7, 350, 470, 1.5), before=mb_before(0.0))


def b_d1(ctx, t, u, dur):
    red = 0.55 + 0.35 * hit(u, 0.85) + 0.25 * hit(u, 1.55)
    return cu('dale', 'yard', 1.32, 0.06, dx=10, expr='shout', hand_n=U.H(5.6, 12.6), prop_n=notice, red=red, sweat=0.5,
              before=mb_before(0.0, 345, 478), shake=12 * (hit(u, 0.85, 0.15) + hit(u, 1.55, 0.15)))(ctx, t, u, dur)


def b_cart(ctx, t, u, dur):
    Z = 1.15
    ST.set_px(ST.px_for_zoom(Z))
    v = view_at(world('yard'), 575, 560, Z, 320, 200)
    big = v.bg()
    CB, CF, CM = Chars(), Chars(), Chars()
    x = 700 - 60 * u
    seat = UP.golf_cart(CB, CF, v, x, STREET_Y, u=6.0, flip=True, t=t, brake=0.0 if u < 0.05 else 0.6)
    L_ = K.light_yard(v)
    CB.comp(big, L_)
    U.brenda(CM, v.cam(seat[0], seat[1], 6.0, flip=True), U.BPOSE['sit'], t, 0.0, 'sweet', 0.0, hand_n=U.H(3.2, 13.6), prop_n=UP.clipboard)
    CM.comp(big, L_); CF.comp(big, L_)
    if u > 0.03:
        for i in range(8):
            ph = u - 0.03 - i * 0.05
            if ph < 0: continue
            ox, oy = v.opt(x + 90 + 22 * i * 0.6 + 40 * ph, STREET_Y - 6 - 30 * ph)
            B.puff(big, ox, oy, (30 + 70 * ph) * 3, 0.6 * max(0, 1 - ph / 0.9), (230, 230, 236))
    if u < 0.35: B.shake(big, t, 10 * (1 - u / 0.35), 33)
    fx.vignette(big, 0.22)
    return big


def b_b1(ctx, t, u, dur):
    Z = 1.35
    ST.set_px(ST.px_for_zoom(Z))
    v = view_at(world('yard'), 560, 560, Z, 320, 200)
    big = v.bg()
    CB, CF, CM, CD = Chars(), Chars(), Chars(), Chars()
    L_ = K.light_yard(v)
    seat = UP.golf_cart(CB, CF, v, 640.0, STREET_Y, u=9.0, flip=True, t=t, brake=1.0)
    U.dale(CD, v.cam(450.0, 610.0, 9.4), U.DPOSE['hold'], t, ctx.mouth('dale', t), 'incredulous', 0.3, False, hand_n=U.H(6.4, 14.6), prop_n=notice, red=0.3)
    CB.comp(big, L_); CD.comp(big, L_)
    U.brenda(CM, v.cam(seat[0], seat[1], 9.0, flip=True), U.BPOSE['sit'], t, ctx.mouth('brenda', t), 'sweet', 0.0, hand_n=U.H(3.4, 10.2), prop_n=clip)
    CM.comp(big, L_); CF.comp(big, L_)
    fx.vignette(big, 0.22)
    return big


def b_chips(ctx, t, u, dur):
    def draw(big, t, u, dur):
        y_off = int(24 * math.sin(t * 6)) if u < 0.3 else 0
        def card(x0, name, sub=None):
            box = np.zeros((520, 400, 4), np.uint8); box[..., :3] = (20, 12, 30); box[..., 3] = 255
            box[10:510, 10:390, :3] = (252, 250, 244); box[34:340, 34:366, :3] = UP.BONE
            O.overlay(big, box, x0, 250 + (y_off if x0 < 900 else -y_off), 1.0)
            ptext(big, name, x0 + 200, 250 + 400 + (y_off if x0 < 900 else -y_off), 34, (40, 30, 60), (252, 250, 244))
            if sub: ptext(big, sub, x0 + 200, 250 + 450 + (y_off if x0 < 900 else -y_off), 34, (40, 30, 60), (252, 250, 244))
        card(430, 'BONE'); card(1090, 'ECRU', 'WHISPER')
        if u > 0.35:
            ptext(big, '=', W_ // 2 + 30, 500, int(120 + 16 * math.sin(u * 14)), (255, 92, 96), (30, 12, 30))
    return insert_dim('yard', draw, 1.7, 420, 470)(ctx, t, u, dur)


# ------------------------------------------------------------------ the painting plan
def b_spray(ctx, t, u, dur):
    """Dale sprays the mailbox; Earl comments from the corner"""
    Z = 1.5
    k = sm((u - 0.5) / 1.6)
    def before(C, v, tt, uu): UP.mailbox_world(C, v, MB[0], MB[1], k, tt, s=MBS)
    can = lambda L, h: UP.spray_can(L, h, -0.35 - 0.25 * math.sin(t * 30))
    def after(big, v, tt, uu):
        if uu > 0.5:
            nx, ny = v.opt(250 + 9.6 * 6.4 + 12, 590 - 17.6 * 6.4 - 4)
            for i in range(10):
                ph = ((tt - 0.5) * 3 + i * 0.13) % 1.0
                B.puff(big, nx + 200 * ph * 0.9 + 40 * i * 0.15, ny + 16 * math.sin(i) + 34 * ph - 30, 34 + 100 * ph, 0.9 * (1 - ph), (255, 250, 232))
    cast = [dict(who='dale', x=250, y=596, u=8.0, pose=U.DPOSE['spray'], hand_n=U.H(9.6, 17.6), prop_n=can, expr='smug', mute=True)]
    base = scene(ctx, t, u, dur, 'yard', cast, (340, 480, Z), before=before, after=after)
    pip(base, earl_cu(ctx, t, u, dur, 'yard', lid=0.5, Z=2.3, zoom=0.03, look=(0.4, 0.2)), 'br', 700, 1.0)
    return base


def b_admire(ctx, t, u, dur):
    if u < 0.55:
        cast = [dict(who='dale', x=225, y=596, u=8.0, pose=dict(U.DPOSE['cheer'], n=(6.4, 15.5)), hand_n=U.H(6.4, 15.5 + 0.5 * math.sin(t * 12)), expr='smug', shades=(u > 0.3), mute=True)]
        big = scene(ctx, t, u, dur, 'yard', cast, (310, 490, 1.5), before=mb_before(1.0))
        for i in range(4):                                                    # sparkle
            ph = (u * 2.2 + i * 0.25) % 1.0
            sx, sy = ST.view_at(world('yard'), 310, 490, 1.5, 320, 190).opt(MB[0] - 40 + i * 30, MB[1] - 24 - 10 * i)
            s_ = int(18 * math.sin(ph * math.pi))
            if s_ > 1:
                big[int(sy) - s_:int(sy) + s_, int(sx) - 3:int(sx) + 3] = (255, 255, 230); big[int(sy) - 3:int(sy) + 3, int(sx) - s_:int(sx) + s_] = (255, 255, 230)
        return big
    press = sm((u - 0.7) / 0.1) if u < 0.8 else max(0.0, 1 - (u - 0.8) / 0.3)
    cast = [dict(who='dale', x=240, y=596, u=8.0, pose=U.DPOSE['hips'], expr='smug', shades=True, mute=True),
            dict(who='brenda', x=430, y=596, u=8.0, flip=True, pose=U.BPOSE['write'], hand_n=U.H(-2.4, 17.6) if u < 0.6 else None, expr='evil', mute=True,
                 prop_n=(lambda L, h: UP.stamp_tool(L, h, press)) if u >= 0.6 else (lambda L, h: UP.chip_fan(L, h, -2.3, 0.28, 1.0)))]
    return scene(ctx, t, u, dur, 'yard', cast, (330, 490, 1.4), before=mb_before(1.0))


# ------------------------------------------------------------------ the permit
def b_yank(ctx, t, u, dur):
    """FINE! NOT on MY property! — Dale rips the mailbox off the post"""
    ripped = u > 1.3
    Z = 1.45
    def before(C, v, tt, uu):
        if not ripped: UP.mailbox_world(C, v, MB[0], MB[1], 1.0, tt, wob=0.0, s=MBS)
    prop = (lambda L, h: UP.mailbox_held(L, h, s=1.0)) if ripped else None
    cast = [dict(who='dale', x=270, y=596, u=8.4, pose=dict(U.DPOSE['hold'], n=(6.4, 13.6), f=(5.4, 13.9)), hand_n=U.H(6.4, 13.6 + (0 if ripped else 2.0 * (1 - sm((u - 1.0) / 0.3)))),
                 prop_n=prop, expr='manic', red=0.95, sweat=0.9)]
    return scene(ctx, t, u, dur, 'yard', cast, (345, 480, Z, 345, 480, Z + 0.15), before=before, shake=(10 * hit(u, 1.3, 0.5)))


def b_march(ctx, t, u, dur):
    x = lerp(400.0, 900.0, min(1.0, u / 0.7))
    look = 1.0 if x > 640 else -0.3
    cast = [dict(who='dale', x=x, y=596, u=6.8, pose=U.dwalk(t, 12.0, 0.5, carry=True), prop_n=lambda L, h: UP.mailbox_held(L, h, s=1.0), expr='manic', red=0.6, mute=True)]
    def before(C, v, tt, uu): U.earl(C, v.cam(640.0, 500.0, 4.4), tt, 0.0, 0.55, (look, 0.0), None, 0.0, 1.0, True)
    return scene(ctx, t, u, dur, 'yard', cast, (lerp(420, 800, min(1.0, u / 0.7)), 480, 1.1), before=before)


def b_plant(ctx, t, u, dur):
    def before(C, v, tt, uu): UP.mailbox_world(C, v, 1005.0, 528.0 + 6 * max(0.0, 1 - uu / 0.15), 0.0, tt, s=MBS)
    cast = [dict(who='dale', x=915, y=596, u=8.6, pose=U.DPOSE['hips'], expr='smug', shades=(u > 0.2)),
            dict(who='brenda', x=1095, y=596, u=8.6, flip=True, pose=U.BPOSE['stand'], expr='sweet', hand_n=U.H(3.4, 13.6), prop_n=UP.clipboard, mute=True)]
    return scene(ctx, t, u, dur, 'yard', cast, (995, 490, 1.3), before=before, shake=(10 * hit(u, 0.0, 0.3)))


def b_fund(ctx, t, u, dur):
    k = sm((u - 0.35) / 0.4)
    Z = lerp(1.5, 0.9, k)
    ST.set_px(ST.px_for_zoom(Z))
    v = view_at(world('interior'), lerp(318.0, 452.0, k), lerp(370.0, 262.0, k), Z, 320, 190)
    big = v.bg(); CH, _ = K.begin(Z)
    UP.fund_jar(CH, v, t, 1.0 if u > 0.6 else 0.94)
    CH.comp(big, K.light_int(v))
    lvl = 0.94 if u < 0.6 else min(1.0, 0.94 + 0.06 * sm((u - 0.6) / 0.25))
    UP.fund_insert(big, v, t, lvl, pop=(u - 0.85) / 0.3 if u > 0.85 else 0.0)
    fx.shafts(big, t, 0.6, 0.05)
    fx.vignette(big, 0.25)
    return big


TR = ('(TRANSLATION: YOU IDIOT)', (255, 190, 226), 34, 960, 760, 0.1, 1.4)
V = 'ep01_t'
BLOCK = Block('ch1', [
    dict(dur=2.0, fn=b_estab, cap=None, sfx=[('library/sfx/whoosh.mp3', 0.0, 0.7, 0.0, 0.6), ('library/sfx/stamp.mp3', 0.35, 0.8)]),
    dict(v=(V, 'd1', 'dale', "Two hundred FIFTY?! For a MAILBOX?!"), fn=b_d1, fines='$250', fines_dt=0.1, sfx=[('library/sfx/paper_crumple_slap.mp3', 0.0, 0.8)], flash=[0.85, 1.55]),
    dict(dur=1.1, fn=b_cart, sfx=[('library/sfx/golf_cart_screech.mp3', 0.0, 0.8, 0.0, 1.1)], st=[('4 MPH', (255, 236, 96), 90, 1250, 380, 0.1, 1.0)], cap=None),
    dict(v=(V, 'b1', 'brenda', "Morning, Dale! Your mailbox is BONE."), fn=b_b1, pad=0.12),
    dict(v=(V, 'd2', 'dale', "It's BEIGE!"), fn=cu('dale', 'yard', 1.3, 0.05, expr='shout', hand_n=U.H(6.0, 17.6), red=0.6, sweat=0.5, look=0.3, before=mb_before(0.0)), pad=0.12),
    dict(v=(V, 'b2', 'brenda', "The approved color is Ecru Whisper."), fn=cu('brenda', 'yard', 1.3, 0.05, expr='sweet', hand_n=U.H(7.6, 11.6), prop_n=chipfan), sfx=[('library/sfx/paper_unroll.mp3', 0.2, 0.4, 0.0, 0.9)]),
    dict(dur=1.15, fn=b_chips, sfx=[('library/sfx/whoosh.mp3', 0.0, 0.3, 0.0, 0.6)], cap=None),
    dict(v=(V, 'd3', 'dale', "That's the SAME color!"), fn=cu('dale', 'yard', 1.3, 0.05, expr='angry', hand_n=U.H(6.0, 17.2), red=0.85, sweat=0.7)),
    dict(v=(V, 'b3', 'brenda', "Bless your heart."), fn=cu('brenda', 'yard', 1.4, 0.06, expr='sweet', lean=0.4, pose=U.BPOSE['hands']), st=[TR], pad=0.15),
    dict(v=(V, 'd4', 'dale', "Relax. I'll repaint it myself. I watched a VIDEO."), fn=two('yard', [dict(who='dale', x=430, y=604, u=10.0, pose=U.DPOSE['hips'], expr='smug', look=0.2, shades=True)], (440, 470, 1.35, 440, 470, 1.5),
         before=mb_before(0.0)), sfx=[('library/sfx/sax_sting_swell.mp3', 1.9, 0.4, 0.0, 1.6)], st=[('[SAXOPHONE GETS LOUDER]', (255, 255, 255), 30, 960, 1010, 1.6, 3.2)]),
    dict(v=(V, 'e1', 'earl', "Nothing good starts with 'I watched a video.'"), fn=b_spray, pad=0.1, lead=0.0,
         sfx=[('library/sfx/pond_bloop.mp3', 0.0, 0.5), ('library/sfx/spray_can_shake.mp3', 0.3, 0.7, 0.0, 0.9), ('library/sfx/spray_paint_hiss.mp3', 1.0, 0.65, 0.0, 2.4)]),
    dict(dur=1.0, fn=b_admire, sfx=[('library/sfx/coin_clink.mp3', 0.15, 0.3, 0.0, 0.5), ('library/sfx/stamp.mp3', 0.7, 1.0)], flash=[0.7],
         st=[('APPROVED', (255, 92, 96), 96, 700, 250, 0.7, 1.9)], cap=None),
    dict(v=(V, 'd5', 'dale', "YES!"), fn=cu('dale', 'yard', 1.25, 0.12, expr='cheer', shades=True, hand_n=U.H(8.6, 26.0), before=mb_before(1.0)), sfx=[('library/sfx/coin_clink.mp3', 0.1, 0.45, 0.0, 0.6)],
         st=[('AURA +9999', (255, 236, 96), 60, 1400, 250, 0.05, 1.3)], pad=0.08),
    dict(v=(V, 'b5', 'brenda', "Painting without a permit? Five hundred DOLLARS."), fn=cu('brenda', 'yard', 1.3, 0.05, expr='evil', pose=U.BPOSE['hands'], lean=0.3),
         sfx=[('library/sfx/record_scratch.mp3', 0.0, 0.8), ('library/sfx/sad_trombone.mp3', 2.9, 0.4, 0.0, 1.6)], st=[('$500', (255, 84, 96), 170, 500, 330, 1.9, 3.1), ('AURA -9999', (255, 100, 100), 60, 1400, 250, 3.3, 4.6)],
         fines='$750', fines_dt=1.9),
    dict(v=(V, 'd6', 'dale', "WHAT permit?!"), fn=cu('dale', 'yard', 1.3, 0.1, expr='shock', shades=None, sweat=0.9, red=0.15, pose=U.DPOSE['shout'])),
    dict(v=(V, 'b6', 'brenda', "Form twenty-seven B. Thirty days BEFORE painting."), fn=cu('brenda', 'yard', 1.3, 0.05, expr='evil', hand_n=U.H(3.2, 11.0), prop_n=form27), sfx=[('library/sfx/paper_unroll.mp3', 0.0, 0.4, 0.0, 0.8)]),
    dict(v=(V, 'd7', 'dale', "FINE! NOT on MY property!"), fn=b_yank, sfx=[('library/sfx/sax_sting_swell.mp3', 0.0, 0.5, 0.0, 1.9), ('library/sfx/mailbox_rip.mp3', 1.25, 0.9), ('library/sfx/flipflop_stomp.mp3', 1.6, 0.55, 0.0, 0.8)],
         st=[('[SAXOPHONE GETS LOUDER]', (255, 255, 255), 30, 960, 1010, 0.1, 1.8)], pad=0.05),
    dict(dur=0.8, fn=b_march, sfx=[('library/sfx/flipflop_stomp.mp3', 0.0, 0.5, 0.0, 1.0), ('library/sfx/fist_slam_counter.mp3', 0.75, 0.5)], cap=None, mosaic=[0.0]),
    dict(v=(V, 'd8', 'dale', "Enjoy the FINE."), fn=b_plant, sfx=[('library/sfx/sax_sting_swell.mp3', 0.0, 0.45, 0.0, 1.6)], st=[('[SAXOPHONE GETS LOUDEST]', (255, 255, 255), 30, 960, 1010, 0.05, 1.5)]),
    dict(v=(V, 'b7', 'brenda', "That's... on MY lawn."), fn=cu('brenda', 'yard', 1.45, 0.1, expr='dread', sweat=1.0, pose=U.BPOSE['hands'])),
    dict(v=(V, 'b8', 'brenda', "Into the Beautification FUND!"), fn=cu('brenda', 'yard', 1.4, 0.08, expr='cheer', hand_n=U.H(3.4, 14.4), prop_n=lambda L, h: UP.ticket_pad(L, h)),
         sfx=[('library/sfx/stamp.mp3', 0.0, 0.9), ('library/sfx/cash_register.mp3', 0.35, 0.8)], mosaic=[1.8]),
    dict(dur=0.95, fn=b_fund, sfx=[('library/sfx/coin_clink.mp3', 0.3, 0.4, 0.0, 0.6), ('library/sfx/pond_bloop.mp3', 0.85, 0.4)], cap=None),
    dict(v=(V, 'e2', 'earl', "Never paid a fine. GRANDFATHERED in."), fn=earl('yard', 0.5, 2.4, zoom=0.05), st=[('SINCE 1987', (255, 226, 110), 72, 960, 250, 1.6, 3.4)], pad=0.25),
], beds=[('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, None, 0.24, True), ('library/sfx/amb_florida_yard.mp3', 7.8, 0.0, None, 0.32, False)],
    card=(1, 'ECRU WHISPER', 'FINES SO FAR: $0'), chapter='Chapter 1: Ecru Whisper')
