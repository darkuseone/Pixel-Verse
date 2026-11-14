"""«Замело» set dressing (rule 10.10.2026: dense local atmosphere): hand-painted plywood boards stuck in the snow, the «СНЕГОМЕР»
ruler on the facade, the countdown «ДО ВЕСНЫ», notices on the buried entrance door, courier arrows, parody brands (ОЗНОБ, САНОКАТ,
КРАБ-МАРКЕТ, УК «СУГРОБ-СЕРВИС»), all fitted inside their plates (props/rusigns.py, Press Start 2P Cyrillic), plus animated
ambience: seagulls over the plain, a smoking chimney, drifting snow. dress(name, world) is called once by zamkit.world()."""
import math
import numpy as np
from props import decals as D
from props import rusigns as R

PLY, PLY_D = (214, 168, 108), (120, 80, 44)
RED, BLUE, INKC, WH = (200, 40, 40), (40, 80, 170), (30, 30, 40), (250, 248, 240)
VIOL = (120, 60, 200)
PAPER = (246, 242, 226)


def board(w, h, lines, pole_h=16, colors=None, hand=True, tilt=0.0, bg=PLY, fg=(40, 30, 30), border=PLY_D, seed=0):
    """a hand-painted plywood board on a stick pushed into the snow (one RGBA decal, the stick goes down)"""
    pl = R.plate(w, h, lines, bg=bg, fg=fg, border=border, colors=colors, hand=hand, seed=seed, wear=0.15)
    ws = D.WS
    H_ = pl.shape[0] + int(pole_h * ws)
    img = np.zeros((H_, pl.shape[1], 4), np.uint8)
    c0 = pl.shape[1] // 2 - ws
    img[pl.shape[0] - ws:, c0:c0 + 2 * ws, :3] = (120, 84, 50); img[pl.shape[0] - ws:, c0:c0 + 2 * ws, 3] = 255
    img[:pl.shape[0]] = np.where(pl[..., 3:4] > 0, pl, img[:pl.shape[0]])
    if tilt: img = D.rotate(img, tilt)
    return img


def ruler(h, floors=9, w=22, top_floor=9):
    """the «СНЕГОМЕР»: a painted red-white measuring strip with floor numbers (top = the highest floor shown)"""
    ws = D.WS
    W_, H_ = int(w * ws), int(h * ws)
    img = np.zeros((H_, W_, 4), np.uint8)
    seg = H_ / floors
    for i in range(floors):
        y0, y1 = int(i * seg), int((i + 1) * seg)
        img[y0:y1, :W_ // 2, :3] = RED if i % 2 == 0 else WH; img[y0:y1, :W_ // 2, 3] = 255
        img[y0:y0 + ws, :, :3] = INKC; img[y0:y0 + ws, :, 3] = 255
        n = R.plate(w * 0.5, seg / ws * 0.6, [str(top_floor - i)], bg=WH, fg=INKC, border=None, pad=0.3)
        yy = y0 + int((y1 - y0 - n.shape[0]) / 2)
        sub = img[yy:yy + n.shape[0], W_ // 2:W_ // 2 + n.shape[1]]
        sub[:] = np.where(n[:sub.shape[0], :sub.shape[1], 3:4] > 0, n[:sub.shape[0], :sub.shape[1]], sub)
    return img


def gulls(n=4, seed=2, box=(0, 40, 1280, 260), col=(60, 60, 80)):
    r = np.random.default_rng(seed)
    P_ = [(r.random(), r.random(), 0.6 + r.random() * 0.5) for _ in range(n)]
    def f(big, v, t):
        x0, y0, x1, y1 = box
        for u, w, sp in P_:
            x = x0 + ((u + t * 0.02 * sp) % 1.0) * (x1 - x0); y = y0 + w * (y1 - y0) + math.sin(t * 1.5 + u * 9) * 6
            ox, oy = v.opt(x, y); q = max(3, int(round(v.Z * 3 * 0.9)))
            flap = 1 if (int(t * 6 + u * 10) % 2) else -1
            for k in range(-3, 4):
                yy = int(oy + abs(k) * q * 0.6 * flap * (-1)); xx = int(ox + k * q)
                if 0 <= xx < big.shape[1] - q and 0 <= yy < big.shape[0] - q: big[yy:yy + q, xx:xx + q] = col
    return f


def smoke(x, y, seed=3, col=(236, 236, 244)):
    """a lazy chimney / vent plume (world px origin)"""
    def f(big, v, t):
        for i in range(7):
            ph = ((t * 0.35 + i / 7) % 1.0)
            wx, wy = x + math.sin(ph * 5 + seed) * 6 + ph * 18, y - ph * 70
            ox, oy = v.opt(wx, wy); r = int((5 + ph * 12) * v.Z)
            if r < 2: continue
            x0, y0 = int(ox - r), int(oy - r)
            if x0 < 0 or y0 < 0 or x0 + 2 * r >= big.shape[1] or y0 + 2 * r >= big.shape[0]: continue
            yy, xx = np.mgrid[-r:r, -r:r]
            m = (xx * xx + yy * yy) <= r * r
            reg = big[y0:y0 + 2 * r, x0:x0 + 2 * r].astype(np.float32)
            a = 0.35 * (1 - ph)
            reg[m] = reg[m] * (1 - a) + np.array(col, np.float32) * a
            big[y0:y0 + 2 * r, x0:x0 + 2 * r] = reg.astype(np.uint8)
    return f


def dress(name, W, day=150):
    if name == 'facade':
        D.attach(W, [
            (board(150, 62, ['ВХОД В ПОДЪЕЗД', '— ЧЕРЕЗ ЖОРУ'], pole_h=26, colors=[(40, 30, 30), RED], seed=2, tilt=-3), 300, 470),
            (board(108, 50, ['ДО ВЕСНЫ:', f'{day} ДНЕЙ'], pole_h=22, colors=[(40, 30, 30), BLUE], seed=5, tilt=4), 1000, 490),
            (R.plate(64, 76, ['СНЕГОМЕР', 'СНЕГ ПО', '9 ЭТАЖ', '↓'], bg=PAPER, fg=INKC, border=RED, colors=[RED, INKC, BLUE, BLUE]), 930, 300),
            (R.plate(150, 26, ['СНЕГ С КРЫШИ НЕ КИДАТЬ!'], bg=PAPER, fg=RED, border=RED), 500, 152),
            (R.plate(86, 40, ['ПРОДАМ', 'ЛЫЖИ. ВЕСНОЙ'], bg=PAPER, fg=INKC, border=(150, 150, 150)), 190, 300),
            (R.plate(54, 22, ['КВ. 36'], bg=BLUE, fg=WH, border=WH), 1100, 150),
        ])
        D.anim(W, gulls(n=3, seed=4, box=(0, 20, 1280, 120)))
    elif name == 'yard':
        D.attach(W, [
            (board(70, 50, ['ПОДЪЕЗД 2', '↓ 27 М'], pole_h=14, bg=(40, 90, 180), fg=WH, border=WH, hand=False, seed=9), 880, 520),
            (board(150, 52, ['НЕ ПРЫГАТЬ!', 'ПОД ВАМИ ДЕТСКАЯ ПЛОЩАДКА'], pole_h=20, colors=[RED, (40, 30, 30)], seed=1, tilt=-2), 30, 470),
            (board(110, 44, ['АВТОБУС —', 'В АПРЕЛЕ'], pole_h=18, seed=3, tilt=3), 470, 520),
            (R.plate(150, 30, ['КРАБ-МАРКЕТ'], bg=(220, 60, 50), fg=WH, border=WH, round_=4), 800, 330),
            (board(120, 40, ['ОЗНОБ ПВЗ →', 'ПО КРЫШАМ'], pole_h=22, bg=VIOL, fg=WH, border=(70, 30, 130), hand=False, seed=6), 660, 560),
        ])
        D.anim(W, gulls(n=5, seed=8, box=(0, 40, 1280, 200)))
        D.anim(W, smoke(420, 260, seed=2)); D.anim(W, smoke(1040, 305, seed=5))
    elif name == 'door':
        D.attach(W, [
            (R.plate(70, 44, ['ОТКЛЮЧЕНИЕ', 'ВОДЫ 01.11'], bg=PAPER, fg=INKC, border=(170, 170, 170), wear=0.3, tilt=-4), 600, 300),
            (R.plate(80, 22, ['ПОДЪЕЗД 2'], bg=BLUE, fg=WH, border=WH), 595, 192),
            (R.plate(44, 26, ['КОД:', 'ЛЕТОМ'], bg=PAPER, fg=INKC, border=(170, 170, 170)), 795, 380),
        ])
    elif name == 'landing':
        D.attach(W, [
            (R.plate(36, 22, ['36'], bg=(220, 190, 90), fg=INKC, border=(120, 90, 40)), 622, 210),
            (R.plate(120, 46, ['КУРЬЕРЫ —', 'ЧЕРЕЗ КРЫШУ ↑'], bg=PAPER, fg=INKC, border=RED, colors=[INKC, RED], wear=0.2, tilt=3), 860, 330),
            (R.plate(110, 40, ['ЛИФТ НЕ', 'РАБОТАЕТ С 2019'], bg=PAPER, fg=INKC, border=(170, 170, 170), wear=0.3, tilt=-3), 360, 300),
            (R.plate(70, 18, ['ВЫТИРАЙ НОГИ'], bg=(150, 60, 50), fg=(230, 200, 140), border=None), 615, 566),
        ])
