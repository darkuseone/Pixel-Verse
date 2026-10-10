"""«Florida Man: Allegedly» set dressing (rule 10.10.2026: lots of local US / Florida atmosphere): parody signs, stickers, flyers,
plaques, lawn ornaments and animated ambience (lovebugs, dust motes, freezer mist) laid over the xAI worlds as hi-res decals
(props/decals.py). Every inscription is auto-fitted inside its plate. dress(name, world) is called once by fmkit.world_baked().
Parody brands of the series: PUBBIX (supermarket), COOL-RITE A/C, SUNSURE MUTUAL, DR. PAWS, SAWGRASS ACRES MGMT."""
import math
import numpy as np
from props import decals as D
from props import fmpix as FX
from props import fmcast as C

RED, NAVY, TEAL, YEL, WH, BLK = (214, 40, 46), (20, 40, 70), (20, 140, 150), (255, 214, 40), (250, 248, 238), (24, 24, 28)
SLOGAN = ["ARRESTED?", "GATOR'D? MELTED?"]           # Mort's billboard slogan: a new one every episode (fmkit.SLOGAN is the source)


def _spr(fn, s, **kw):
    img, (ax, ay) = D.sprite(fn, s, FX.draw, **kw)
    return img, ax, ay


def place_sprite(world, fn, wx, wy, s, **kw):
    """a code-drawn ornament standing on the ground: feet anchor at world (wx, wy); s = world px per sprite px"""
    img, ax, ay = _spr(fn, s * D.WS, **kw)
    D.attach(world, [(img, wx - ax / D.WS, wy - ay / D.WS)])


# ---------------------------------------------------------------- animated ambience (background layer)
def lovebugs(box, n=7, seed=3):
    """Florida lovebugs: little black pairs stuck together, wandering in lazy loops inside world box (x0, y0, x1, y1)"""
    r = np.random.default_rng(seed)
    P_ = [(r.uniform(0, 1), r.uniform(0, 1), r.uniform(0.6, 1.4), r.uniform(0, 6.28)) for _ in range(n)]

    def fn(big, v, t):
        x0, y0, x1, y1 = box
        sz = max(2, int(v.Z * 3 * 1.2))
        for (u, w, sp_, ph) in P_:
            x = x0 + (x1 - x0) * (u + 0.08 * math.sin(t * sp_ + ph) + 0.05 * math.sin(t * 2.3 * sp_))
            y = y0 + (y1 - y0) * (w + 0.10 * math.cos(t * 0.8 * sp_ + ph))
            ox, oy = v.opt(x, y)
            a = t * 3 * sp_ + ph
            for k_, col in ((0, (30, 26, 30)), (1, (200, 60, 50))):            # black body + the red-orange thorax of the partner
                px, py = int(ox + math.cos(a) * sz * 1.3 * k_), int(oy + math.sin(a) * sz * 0.6 * k_)
                if 0 <= px < big.shape[1] - sz and 0 <= py < big.shape[0] - sz:
                    big[py:py + sz, px:px + sz] = (30, 26, 30)
                    if k_: big[py:py + max(1, sz // 2), px:px + sz] = col
            if int(t * 20 + ph * 5) % 2 == 0:                                  # wing flicker
                px, py = int(ox), int(oy - sz)
                if 0 <= px < big.shape[1] - 2 * sz and 0 <= py < big.shape[0] - sz:
                    big[py:py + max(1, sz // 2), px:px + 2 * sz] = (200, 210, 220)
    return fn


def motes(box, n=26, col=(255, 240, 200), seed=5, speed=4.0, big_=False):
    """dust motes drifting and twinkling (sunbeams, dusty yards); box in world px"""
    r = np.random.default_rng(seed)
    P_ = [(r.uniform(0, 1), r.uniform(0, 1), r.uniform(0.5, 1.5), r.uniform(0, 6.28)) for _ in range(n)]

    def fn(big, v, t):
        x0, y0, x1, y1 = box
        for (u, w, sp_, ph) in P_:
            x = x0 + (x1 - x0) * ((u + 0.01 * t * sp_ + 0.02 * math.sin(t * 0.7 + ph)) % 1.0)
            y = y0 + (y1 - y0) * ((w - 0.015 * t * sp_ * speed / 4) % 1.0)
            ox, oy = v.opt(x, y)
            tw = 0.5 + 0.5 * math.sin(t * 3 * sp_ + ph)
            sz = max(2, int(v.Z * 3 * (1.0 if big_ else 0.6)))
            px, py = int(ox), int(oy)
            if 0 <= px < big.shape[1] - sz and 0 <= py < big.shape[0] - sz:
                reg = big[py:py + sz, px:px + sz]
                reg[:] = (reg * (1 - 0.75 * tw) + np.array(col) * 0.75 * tw).astype(np.uint8)
    return fn


def mist(box, n=18, seed=9):
    """freezer-door cold mist: pale sparkles sinking and fading"""
    r = np.random.default_rng(seed)
    P_ = [(r.uniform(0, 1), r.uniform(0, 1), r.uniform(0.6, 1.4)) for _ in range(n)]

    def fn(big, v, t):
        x0, y0, x1, y1 = box
        for (u, w, sp_) in P_:
            ph = (w + t * 0.12 * sp_) % 1.0
            x = x0 + (x1 - x0) * (u + 0.02 * math.sin(t * sp_ * 2 + u * 9))
            y = y0 + (y1 - y0) * ph
            ox, oy = v.opt(x, y)
            a = 0.8 * math.sin(math.pi * ph)
            sz = max(2, int(v.Z * 3 * 0.7))
            px, py = int(ox), int(oy)
            if 0 <= px < big.shape[1] - sz and 0 <= py < big.shape[0] - sz:
                reg = big[py:py + sz, px:px + sz]
                reg[:] = (reg * (1 - a) + np.array((236, 248, 255)) * a).astype(np.uint8)
    return fn


# ---------------------------------------------------------------- locations
def billboard(slogan):
    """Mort's billboard across the canal: his face + «MORT POUCH, ESQ. / <slogan> / 1-800-POUCH-ME», text fitted in its column"""
    w, h, ws = 206, 106, D.WS                                      # covers the AI billboard incl. its frame (802..1008 x 213..319)
    img = np.zeros((h * ws, w * ws, 4), np.uint8)
    img[..., :3] = (120, 124, 128); img[..., 3] = 255                # galvanised frame
    f = 4 * ws
    img[f:-f, f:-f, :3] = (250, 248, 238)
    img[f:f + 6 * ws, f:-f, :3] = (40, 196, 196); img[-f - 6 * ws:-f, f:-f, :3] = (255, 150, 90)
    m, ax, ay = _spr(C.mort, 1.9 * ws, t=0.0, expr='smug', look=(0.6, 0.0), lift=0.6, blink=False)
    hx, hy = 0, 0
    cut = m[: min(m.shape[0], (h - 2 * 4 - 12) * ws)]                 # head-and-shoulders portrait, cropped at the orange band
    mh, mw = cut.shape[:2]
    y0 = h * ws - f - 6 * ws - mh; x0 = f + 2 * ws
    reg = img[y0:y0 + mh, x0:x0 + mw]
    al = cut[..., 3:4] / 255.0
    reg[..., :3] = (reg[..., :3] * (1 - al) + cut[..., :3] * al).astype(np.uint8)
    tx0 = x0 + mw + 3 * ws; tx1 = w * ws - f - 3 * ws
    D.text_box(img, ['MORT POUCH,', 'ESQ.'], (tx0, f + 8 * ws, tx1, f + 32 * ws), (14, 44, 54))
    D.text_box(img, list(slogan), (tx0, f + 35 * ws, tx1, f + 62 * ws), RED)
    D.text_box(img, ['1-800-POUCH-ME'], (tx0, f + 65 * ws, tx1, f + 80 * ws), TEAL)
    D.weather(img, 0.4, 2)
    return img


def dress_yard(W, slogan=None):
    D.attach(W, [(billboard(slogan or SLOGAN), 802, 213)])
    D.attach(W, [
        (D.plate(44, 15, ['LOT 13'], bg=(236, 230, 210), fg=NAVY, border=NAVY, wear=0.5, seed=1, rivets=True), 352, 226),
        (D.plate(84, 40, ['NO TRESPASSING', 'VIOLATORS WILL BE', 'TALKED AT'], bg=WH, colors=[RED, BLK, BLK], border=RED,
                 weights=[1.3, 1.0, 1.0], wear=0.6, seed=3, tilt=-2), 344, 360),
        (D.sticker('', bg=NAVY, fg=WH, w=86, h=16, lines=['MY OTHER HOUSE', 'IS ALSO A TRAILER'], tilt=3), 34, 384),
        (D.sticker('HONK IF YOU\'RE SWEATING', bg=YEL, fg=BLK, w=70, h=11, tilt=-4), 228, 352),
        (D.plate(40, 40, ['GATOR', 'XING'], bg=YEL, fg=BLK, border=BLK, bw=1.4, wear=0.4, seed=4, round_=3), 523, 424),
        (D.plate(70, 44, ['DO NOT FEED', 'THE GATORS', '(THEY HAVE', 'A LAWYER)'], bg=(236, 244, 236), colors=[(30, 110, 60)] * 2 + [RED] * 2,
                 border=(30, 110, 60), wear=0.5, seed=5), 868, 426),
        (D.plate(40, 36, ['LOST:', '1 CROC', '(LEFT)', 'REWARD $2'], bg=(255, 250, 200), colors=[RED, BLK, BLK, (30, 110, 60)],
                 border=None, pad=1.2, tilt=5), 668, 432),
    ])
    place_sprite(W, C.flamingo, 1000, 548, 3.0)
    place_sprite(W, C.flamingo, 1052, 556, 2.8, flip=True, faded=0.6)
    place_sprite(W, C.gnome, 300, 600, 3.2)
    D.anim(W, lovebugs((460, 300, 1260, 520), n=8))
    D.anim(W, motes((0, 520, 1280, 700), n=22, col=(250, 236, 200), speed=1.5))


def dress_store(W):
    img = D.plate(400, 76, ['PUBBIX', 'WHERE SHOPPING IS A PLEASURE*', '*PRICES MAY VARY'], bg=(246, 246, 236), border=None,
                  colors=[(34, 150, 110), (14, 44, 54), RED], weights=[3.0, 0.9, 0.9], pad=2.5)
    D.attach(W, [(img, 446, 176)])
    D.attach(W, [
        (D.plate(52, 44, ['BOGO!', 'BUY ONE', 'GET ONE', '(MAYBE)'], bg=YEL, colors=[RED, BLK, BLK, RED], border=RED, weights=[1.5, 1, 1, 1]), 56, 360),
        (D.plate(52, 40, ['ICE', '$9.99', 'LIMIT 1'], bg=(200, 236, 255), colors=[NAVY, RED, NAVY], border=NAVY, weights=[1.4, 1.4, 1]), 120, 354),
        (D.plate(70, 34, ['NO SHIRT, NO SHOES', 'STILL SERVICE', "(IT'S FLORIDA)"], bg=WH, colors=[BLK, (34, 150, 110), RED], border=BLK), 520, 392),
        (D.plate(44, 26, ['OPEN 24/7', 'EXCEPT 3PM', '(TOO HOT)'], bg=WH, colors=[BLK, RED, RED], border=None, pad=1.0), 688, 396),
        (D.plate(70, 20, ['RETURN CARTS', 'HERE (PLEASE)'], bg=(34, 150, 110), fg=WH, border=WH), 1012, 436),
        (D.plate(66, 38, ['CAUTION', 'ASPHALT', 'IS 160°F'.replace('°', '*')], bg=(255, 140, 40), fg=BLK, border=BLK, weights=[1.3, 1, 1], round_=2, wear=0.3), 1140, 500),
        (D.plate(58, 46, ['SUB SALE', '$14.99', '(WAS', '$14.99)'], bg=WH, colors=[(34, 150, 110), RED, BLK, BLK], border=(34, 150, 110), weights=[1, 1.5, 1, 1]), 1110, 350),
    ])
    D.anim(W, motes((0, 560, 1280, 720), n=20, col=(255, 236, 200), speed=1.0))


def dress_aisle(W):
    D.attach(W, [(D.plate(252, 54, ['AISLE 9', 'FROZEN FOODS'], bg=(40, 150, 160), colors=[(255, 255, 250), (255, 236, 96)], border=None,
                          weights=[1.5, 1.0], pad=2.0), 520, 54)])
    tags = [('$8.99', 0), ('$11.49', 1), ('MGR SPECIAL', 2), ('$6.66', 3), ('ICE CREAM', 4), ('$13.99', 5), ('NEW!', 6), ('$9.49', 7)]
    items = []
    for lbl, i in tags:
        x = 120 + i * 137
        items.append((D.plate(34, 9, [lbl], bg=(255, 236, 96) if 'SPECIAL' in lbl or 'NEW' in lbl else WH, fg=RED, border=None, pad=0.6), x, 452))
    items += [
        (D.plate(48, 30, ['PLEASE', 'DO NOT', 'LIVE HERE'], bg=WH, colors=[BLK, RED, RED], border=RED, tilt=-3), 404, 226),
        (D.plate(56, 26, ['KEEP DOORS', 'CLOSED', '(WE SEE YOU)'], bg=(200, 236, 255), fg=NAVY, border=NAVY), 816, 230),
        (D.plate(40, 22, ['NOW 68*F', 'INSIDE'], bg=(40, 150, 160), fg=WH, border=WH), 1180, 260),
    ]
    D.attach(W, items)
    D.anim(W, mist((100, 220, 1190, 470), n=24))


def dress_cell(W):
    D.attach(W, [
        (D.plate(84, 56, ['INMATE RULES', '1. NO', '2. ALSO NO', '3. A/C IS', 'A PRIVILEGE'], bg=(236, 232, 210), colors=[RED] + [BLK] * 4,
                 border=BLK, weights=[1.2, 1, 1, 1, 1], wear=0.7, seed=8, tilt=1.5), 880, 240),
        (D.plate(70, 22, ['FLORIDA MAN', 'WAS HERE'], bg=(0, 0, 0), fg=(40, 40, 46), border=None, pad=0.5, tilt=-6), 560, 300),
        (D.plate(52, 28, ['★★★★★', 'GREAT A/C'], bg=YEL, colors=[RED, BLK], border=None, round_=2, tilt=-4), 990, 192),
        (D.plate(40, 22, ['IIII IIII', 'IIII II'], bg=(0, 0, 0), fg=(60, 60, 62), border=None, pad=0.3), 470, 420),
    ])
    for img, *_ in ST_scrub(W): pass
    D.anim(W, motes((560, 200, 1100, 620), n=34, col=(255, 236, 170), speed=2.0, big_=True))


def ST_scrub(W):
    """drop the black placeholder bg of «scratched-in» plates: only the letters stay (graffiti / tally marks)"""
    import stage as ST
    e = ST.DECALS.get(id(W))
    out = []
    if not e: return out
    for k_, (img, x, y, ws) in enumerate(e[1]):
        bgm = (img[..., :3] == 0).all(-1) & (img[..., 3] == 255)
        if bgm.mean() > 0.4:
            img = img.copy(); img[bgm, 3] = 0; e[1][k_] = (img, x, y, ws)
        out.append(e[1][k_])
    return out


def fly(box, seed=11):
    """one lazy housefly buzzing over the deli trays (a dark dot + flickering wings)"""
    def fn(big, v, t):
        x0, y0, x1, y1 = box
        x = x0 + (x1 - x0) * (0.5 + 0.45 * math.sin(t * 1.3 + seed) * math.cos(t * 0.37))
        y = y0 + (y1 - y0) * (0.5 + 0.45 * math.sin(t * 2.1 + seed * 0.3))
        ox, oy = v.opt(x, y)
        sz = max(3, int(v.Z * 3 * 1.4))
        px, py = int(ox), int(oy)
        if 0 <= px < big.shape[1] - 2 * sz and sz <= py < big.shape[0] - sz:
            big[py:py + sz, px:px + sz] = (24, 24, 30)
            if int(t * 24) % 2: big[py - sz // 2:py, px - sz // 2:px + sz + sz // 2] = (210, 220, 230)
    return fn


def menu_board(rows, title='PUBBIX DELI', foot='*PRICES MAY VARY. UP.', w=624, h=150):
    """the deli menu board: title, rows «ITEM ....... $PRICE» (each row fitted, dot leaders between), red footnote"""
    ws = D.WS
    img = np.zeros((h * ws, w * ws, 4), np.uint8)
    img[..., :3] = (250, 244, 222); img[..., 3] = 255
    b = 5 * ws
    img[:b, :, :3] = img[-b:, :, :3] = img[:, :b, :3] = img[:, -b:, :3] = (40, 150, 160)
    D.text_box(img, [title], (b + 8 * ws, b + 3 * ws, w * ws - b - 8 * ws, b + 26 * ws), (34, 150, 110))
    rh = (h - 10 - 26 - 18) * ws // len(rows)
    y = b + 28 * ws
    for (a, p_, c) in rows:
        # left item + right price in one fitted row; dot leaders fill the gap
        n, _ = D.fit([a + '  ' + p_], int(w * ws * 0.78), rh - 2 * ws)
        n = min(n, 3 * ws)
        D.draw_text(img, a, b + 14 * ws, y + (rh - 5 * n) // 2, n, c)
        pw = D.text_w(p_) * n
        D.draw_text(img, p_, w * ws - b - 14 * ws - pw, y + (rh - 5 * n) // 2, n, c)
        xa = b + 14 * ws + D.text_w(a) * n + 3 * n
        for xx in range(xa, w * ws - b - 18 * ws - pw, 3 * n): img[y + (rh + 3 * n) // 2: y + (rh + 3 * n) // 2 + n, xx:xx + n, :3] = (150, 150, 140)
        y += rh
    D.text_box(img, [foot], (b + 8 * ws, h * ws - b - 15 * ws, w * ws - b - 8 * ws, h * ws - b - 2 * ws), RED)
    return img


def dress_deli(W):
    rows = [('CHICKEN TENDER SUB', '$14.99', RED), ('ITALIAN SUB', '$15.49', (14, 44, 54)),
            ('HALF A SUB', '$11.99', (14, 44, 54)), ('SUB-SIZED SUB', '$13.99', (14, 44, 54))]
    D.attach(W, [(menu_board(rows), 352, 72)])
    lcd = D.plate(68, 25, ['18.2LB', '$72.80'], bg=(30, 52, 40), fg=(140, 255, 160), border=(20, 30, 24), bw=0.8, pad=1.0, weights=[0.8, 1.2])
    D.attach(W, [(lcd, 929, 262)])
    tags = [('TURKEY', '$16.99'), ('SALAMI', '$14.99'), ('PASTRAMI', '$19.99'), ('HAM', '$12.99'), ('SWISS', '$11.99'), ('CHEDDAR', '$9.99'),
            ('PEAS?', '$8.99'), ('MYSTERY', 'SALAD'), ('TATER', 'SALAD')]
    xs = [182, 284, 380, 488, 590, 700, 812, 928, 1040]
    D.attach(W, [(D.plate(52, 14, [a, b_], bg=WH, colors=[NAVY, RED], border=None, pad=0.6), x, 470) for (a, b_), x in zip(tags, xs)])
    D.attach(W, [
        (D.plate(58, 30, ['NOW SERVING', '001'], bg=(20, 20, 24), colors=[(255, 236, 96), (255, 60, 50)], border=(80, 80, 86), weights=[1, 2.2]), 14, 268),
        (D.plate(52, 26, ['TAKE A', 'NUMBER', 'U R #847'], bg=(226, 40, 52), colors=[WH, WH, YEL], border=WH), 1196, 296),
        (D.plate(110, 16, ["PLEASE DON'T TAP GLASS", '(THE HAM IS SLEEPING)'], bg=WH, colors=[BLK, RED], border=RED, pad=0.8), 486, 378),
        (D.plate(84, 30, ['SUB OF THE WEEK:', 'SAME SUB', 'NEW PRICE'], bg=YEL, colors=[BLK, (34, 150, 110), RED], border=BLK, weights=[1, 1.2, 1.2]), 1030, 62),
        (D.plate(40, 13, ['ROLLS $6/EA'], bg=WH, fg=RED, border=None, pad=0.6), 140, 244),
    ])
    D.anim(W, fly((180, 330, 1100, 450)))


def post_sign(w, h, lines, post_h, post_col=(120, 84, 50), **kw):
    """a plate nailed on a wooden stake (stuck in the ground / on a dock post): returns (img, height of the plate in world px)"""
    ws = D.WS
    pl = D.plate(w, h, lines, **kw)
    ph = int(post_h * ws); pw = max(ws * 3, int(w * ws * 0.08))
    img = np.zeros((pl.shape[0] + ph, pl.shape[1], 4), np.uint8)
    x0 = (pl.shape[1] - pw) // 2
    img[pl.shape[0] - ws:, x0:x0 + pw, :3] = post_col; img[pl.shape[0] - ws:, x0:x0 + pw, 3] = 255
    img[pl.shape[0] - ws:, x0:x0 + max(1, pw // 4), :3] = (80, 56, 34)
    al = pl[..., 3:4] / 255.0
    img[:pl.shape[0], :, :3] = (img[:pl.shape[0], :, :3] * (1 - al) + pl[..., :3] * al).astype(np.uint8)
    img[:pl.shape[0], :, 3] = np.maximum(img[:pl.shape[0], :, 3], pl[..., 3])
    return img


def moths(centres, n=5, seed=13):
    """moths circling the night lamps"""
    r = np.random.default_rng(seed)
    P_ = [(c, r.uniform(8, 26), r.uniform(1.5, 3.5), r.uniform(0, 6.28)) for c in centres for _ in range(n)]

    def fn(big, v, t):
        for (cx, cy), rad, sp_, ph in P_:
            x = cx + rad * math.cos(t * sp_ + ph); y = cy + rad * 0.6 * math.sin(t * sp_ * 1.3 + ph)
            ox, oy = v.opt(x, y)
            sz = max(2, int(v.Z * 3 * 0.8))
            px, py = int(ox), int(oy)
            if 0 <= px < big.shape[1] - sz and 0 <= py < big.shape[0] - sz:
                big[py:py + sz, px:px + sz] = (236, 226, 190) if int(t * 16 + ph * 3) % 2 else (120, 110, 90)
    return fn


def dress_hospital(W):
    D.attach(W, [(D.plate(400, 78, ['BILLING - CASHIER', 'SUNSHINE GENERAL - PAY HERE'], bg=(246, 246, 238), colors=[(14, 44, 54), RED],
                          border=(120, 124, 128), bw=3, weights=[1.4, 1.0], pad=3), 448, 84)])
    D.attach(W, [
        (D.plate(112, 36, ['ER WAIT TIME:', '9 HRS'], bg=(20, 20, 24), colors=[(255, 236, 96), (255, 60, 50)], border=(80, 80, 86), weights=[1, 1.8]), 40, 150),
        (D.plate(70, 42, ['WE ACCEPT:', 'CASH', 'CARD', 'KIDNEY'], bg=WH, colors=[NAVY, BLK, BLK, RED], border=NAVY), 860, 214),
        (D.plate(70, 18, ['TALKING: $5/MIN'], bg=YEL, fg=BLK, border=BLK, bw=0.6), 694, 268),
        (D.plate(64, 20, ['WATER', '$12 / CUP'], bg=WH, colors=[NAVY, RED], border=None, pad=0.8), 66, 462),
        (D.plate(76, 14, ['FAKE PLANT ($300)'], bg=WH, fg=RED, border=None, pad=0.6), 1152, 506),
        (D.plate(98, 22, ['LINE STARTS HERE', '(BRING SNACKS)'], bg=RED, colors=[WH, YEL], border=WH, bw=0.6), 340, 520),
        (D.plate(118, 52, ["FLORIDA'S #1", 'HOSPITAL', 'FOR BILLING*', '*SURVEY OF 1'], bg=(236, 244, 236), colors=[(34, 150, 110), (34, 150, 110), BLK, RED],
                 border=(34, 150, 110), weights=[1, 1.3, 1, 0.8], wear=0.3), 1032, 132),
    ])
    D.anim(W, motes((900, 150, 1280, 620), n=26, col=(255, 240, 200), speed=1.5))


def dress_vet(W):
    ws = D.WS
    img = np.zeros((198 * ws, 290 * ws, 4), np.uint8); img[..., 3] = 255
    img[..., :3] = (226, 96, 96); f = 6 * ws
    img[f:-f, f:-f, :3] = (255, 250, 236); img[f:f + 34 * ws, f:-f, :3] = (255, 140, 60)
    D.text_box(img, ['MICROCHIP'], (f + 8 * ws, f + 3 * ws, 290 * ws - f - 8 * ws, f + 31 * ws), (255, 255, 255))
    D.text_box(img, ['SPECIAL!'], (f + 8 * ws, f + 38 * ws, 290 * ws - f - 8 * ws, f + 70 * ws), RED)
    D.text_box(img, ['NEVER LOSE', 'YOUR BEST', 'FRIEND!'], (f + 30 * ws, f + 76 * ws, 290 * ws - f - 30 * ws, f + 132 * ws), (14, 44, 54))
    D.text_box(img, ['$0 TODAY*'], (f + 20 * ws, f + 136 * ws, 290 * ws - f - 20 * ws, f + 162 * ws), (40, 150, 90))
    D.text_box(img, ['*SCAN EXTRA'], (290 * ws - f - 70 * ws, 198 * ws - f - 12 * ws, 290 * ws - f - 4 * ws, 198 * ws - f - 2 * ws), RED)
    D.attach(W, [(img, 612, 80)])
    D.attach(W, [
        (D.plate(196, 46, ['DR. PAWS', 'ANIMAL CLINIC - WALK-INS WELCOME'], bg=WH, colors=[RED, NAVY], border=RED, bw=1.4, weights=[2.0, 0.8], round_=4), 1000, 18),
        (D.plate(150, 32, ['PLEASE KEEP YOUR', 'HUMAN ON A LEASH'], bg=YEL, fg=BLK, border=BLK), 990, 470),
        (D.plate(88, 56, ['BITE RISK:', 'LOW', 'MEDIUM', 'FLORIDA'], bg=WH, colors=[BLK, (40, 150, 90), (255, 140, 40), RED], border=BLK, weights=[1, 1, 1, 1.3]), 382, 246),
        (D.plate(70, 12, ['NOT FOR HUMANS'], bg=WH, fg=RED, border=None, pad=0.5), 386, 620),
        (D.plate(52, 13, ['OCCUPIED'], bg=RED, fg=WH, border=WH, bw=0.5, tilt=-5), 262, 414),
        (D.plate(120, 26, ['NO ALLIGATORS', '(WE CHECKED)'], bg=WH, colors=[RED, BLK], border=RED, wear=0.2), 40, 300),
    ])


def dress_booth(W, lines):
    D.attach(W, [(D.plate(416, 98, list(lines), bg=(240, 226, 190), colors=[RED, (14, 44, 54), (255, 120, 40)], border=(110, 76, 40),
                          bw=5, pad=3, wear=0.7, seed=6), 432, 186)])
    D.attach(W, [
        (D.plate(70, 30, ['CASH ONLY', '(NO GATORS)'], bg=WH, colors=[BLK, RED], border=BLK, wear=0.4, tilt=-3), 358, 318),
        (D.plate(110, 44, ['AIRBOAT TOURS', '$40', '(SURVIVAL', 'EXTRA)'], bg=YEL, colors=[BLK, RED, BLK, BLK], border=BLK, weights=[1, 1.6, 0.9, 0.9], wear=0.3), 872, 316),
        (D.plate(70, 22, ['BAIT &', 'LUNCH'], bg=WH, fg=(20, 120, 150), border=None, pad=0.8), 912, 534),
        (post_sign(62, 30, ['NO SWIM', 'GATORS!'], 30, bg=WH, colors=[BLK, RED], border=RED, wear=0.5), 1030, 404),
        (post_sign(82, 18, ['BOILED PEANUTS ->'.replace('->', '→')], 34, bg=(240, 226, 190), fg=(110, 60, 20), border=(110, 76, 40)), 24, 430),
    ])
    D.anim(W, lovebugs((300, 280, 1000, 520), n=6, seed=8))


def dress_swamp(W):
    D.attach(W, [
        (post_sign(96, 40, ['PRIVATE DOCK', 'TRESPASSERS', 'WILL BE EATEN'], 18, bg=(240, 226, 190), colors=[BLK, BLK, RED], border=(110, 76, 40), wear=0.6), 334, 400),
        (post_sign(96, 32, ['PYTHON CHALLENGE', 'CHECK-IN 2 MI →'], 46, bg=(40, 120, 70), fg=WH, border=WH), 700, 382),
    ])
    D.anim(W, lovebugs((250, 300, 1200, 520), n=9, seed=21))
    D.anim(W, motes((300, 480, 1280, 720), n=18, col=(255, 255, 230), speed=0.8))


def dress_jail_ext(W):
    D.attach(W, [(D.tint(D.plate(142, 38, ['SUNSHINE COUNTY', 'JAIL & RESORT'], bg=(236, 230, 210), colors=[(14, 44, 54), RED], border=(90, 86, 76),
                          bw=2, weights=[1.0, 1.15], pad=1.5), 0.72), 573, 286)])
    D.attach(W, [
        (D.tint(D.plate(110, 40, ['NO TRESPASSING', '(THIS MEANS YOU,', 'FLORIDA MAN)'], bg=WH, colors=[RED, BLK, BLK], border=RED, wear=0.4), 0.55), 518, 436),
        (D.plate(64, 16, ['CHECK-IN →'], bg=(20, 20, 24), fg=(255, 120, 200), border=(255, 120, 200), bw=0.6), 612, 350),
        (D.tint(D.plate(104, 34, ['NOW HIRING GUARDS', '(MUST LIKE', 'FLORIDA MAN)'], bg=YEL, colors=[BLK, BLK, BLK], border=BLK, weights=[1.1, 1, 1], wear=0.3), 0.55), 860, 432),
    ])
    D.anim(W, moths([(302, 358), (940, 358), (1012, 52)], n=4))


def dress_booking(W):
    D.attach(W, [
        (D.plate(66, 84, ['WANTED', 'FLORIDA', 'MAN', '(AGAIN)'], bg=(250, 170, 150), colors=[RED, BLK, BLK, BLK], border=None, pad=1.5, weights=[1.3, 1, 1, 1], tilt=-4), 514, 146),
        (D.plate(60, 66, ['LOST GATOR', 'ANSWERS TO', '"KEVIN"'], bg=(246, 226, 140), colors=[BLK, BLK, RED], border=None, pad=1.2, tilt=2), 616, 132),
        (D.plate(48, 50, ['BAKE', 'SALE', 'FRI'], bg=(240, 236, 226), colors=[NAVY, NAVY, RED], border=None, pad=1.0, tilt=-3), 674, 214),
        (D.plate(66, 84, ['EMPLOYEE', 'OF THE', 'MONTH:', 'FLORIDA', 'MAN'], bg=(170, 214, 226), colors=[NAVY, NAVY, NAVY, RED, RED], border=None, pad=1.3, tilt=-5), 746, 140),
        (D.plate(150, 40, ['FREQUENT GUESTS', '→ EXPRESS LANE'], bg=(34, 150, 110), colors=[WH, YEL], border=WH, wear=0.2), 480, 446),
        (D.plate(44, 14, ['SMILE!'], bg=RED, fg=WH, border=WH, bw=0.5), 1080, 360),
    ])
    D.anim(W, motes((220, 100, 760, 560), n=24, col=(255, 240, 200), speed=1.6))


DRESS = dict(yard=dress_yard, store=dress_store, aisle=dress_aisle, cell=dress_cell, deli=dress_deli, hospital=dress_hospital,
             vet=dress_vet, swamp=dress_swamp, jail_ext=dress_jail_ext, booking=dress_booking)


def dress(name, W, **kw):
    if name in DRESS: DRESS[name](W, **kw); return True
    return False
