"""Saloon «Пыльный кактус» as one wide world (800x640 logical px, x3 -> 1080-high frames):
  x   0..140  entrance (batwing doorway, desert outside)
  x 140..500  bar (the approved keyframe from engine/saloon_keyframe.py, without heroes/bartender)
  x 500..800  corner (staircase, «ДЕЛОВАЯ ВСТРЕЧА» table spot)
Bartender is a separate sprite (poses) so he can move. Everything is cached in build/props/."""
import os
import numpy as np
import paths as PATHS
from props.canvas import Canvas, C, quantize, MAT_CHAR

WORLD_W, WORLD_H = 800, 640
BAR_X = 140          # offset of the bar section
CORNER_X = 500
FLOOR_Y = 505
WALL_TOP = 62
WOOD_BASE = C(118, 76, 46)
BOTTLE_COLS = [C(70, 120, 60), C(120, 70, 40), C(160, 90, 40), C(200, 190, 170), C(90, 60, 110), C(150, 40, 40), C(60, 100, 120)]


def _wall(c, seed):
    c.planks_v(0, c.W, WALL_TOP, FLOOR_Y, 15, WOOD_BASE, seed=seed)
    c.rect(0, FLOOR_Y - 10, c.W, FLOOR_Y, C(70, 42, 26)); c.rect(0, FLOOR_Y - 10, c.W, FLOOR_Y - 9, C(140, 94, 56))
    c.rect(0, 0, c.W, WALL_TOP, C(46, 28, 20))
    for bx in range(0, c.W, 60):
        c.rect(bx, 0, bx + 20, WALL_TOP, C(70, 42, 26)); c.rect(bx, 0, bx + 3, WALL_TOP, C(92, 58, 36))
    c.rect(0, WALL_TOP - 8, c.W, WALL_TOP, C(78, 48, 30)); c.rect(0, WALL_TOP - 1, c.W, WALL_TOP + 1, C(40, 24, 16))
    c.rect(0, 300, c.W, 305, C(88, 54, 32)); c.rect(0, 300, c.W, 301, C(150, 102, 62))


def _lamp(c, lx):
    c.rect(lx - 1, 318, lx + 2, 326, C(40, 30, 26)); c.rect(lx - 5, 326, lx + 6, 342, C(60, 50, 40))
    c.put(c.ellm(lx + 0.5, 334, 3.5, 5.5), C(255, 214, 110), emit=1)


def _vig(c):
    return np.clip(((c.YY - 330) / 420) ** 2 - 0.45, 0, 1) * 0.45


# ==================================================================== bar (from the keyframe)
def bar_section():
    c = Canvas(360, WORLD_H, seed=11); rng = c.rng
    W, H, F, XX, YY = c.W, c.H, c.F, c.XX, c.YY
    c.planks_v(0, W, WALL_TOP, 430, 15, WOOD_BASE, seed=1)
    c.rect(0, 0, W, WALL_TOP, C(46, 28, 20))
    for bx in range(0, W, 60):
        c.rect(bx, 0, bx + 20, WALL_TOP, C(70, 42, 26)); c.rect(bx, 0, bx + 3, WALL_TOP, C(92, 58, 36))
    c.rect(0, WALL_TOP - 8, W, WALL_TOP, C(78, 48, 30)); c.rect(0, WALL_TOP - 1, W, WALL_TOP + 1, C(40, 24, 16))
    c.rect(0, 300, W, 305, C(88, 54, 32)); c.rect(0, 300, W, 301, C(150, 102, 62))
    # window
    wx0, wy0, wx1, wy1 = 292, 118, 352, 238
    c.rect(wx0 - 5, wy0 - 5, wx1 + 5, wy1 + 7, C(70, 42, 26))
    for y in range(wy0, wy1):
        k = (y - wy0) / (wy1 - wy0); F[y, wx0:wx1] = C(255, 232, 178) * (1 - k) + C(240, 176, 112) * k
    c.EMIT[wy0:wy1, wx0:wx1] = 1
    c.put(c.poly([(wx0, 210), (wx0 + 12, 196), (wx0 + 30, 196), (wx0 + 38, 206), (wx1, 204), (wx1, wy1), (wx0, wy1)]), C(214, 132, 92), emit=1)
    c.put(c.ellm(wx0 + 46, 214, 2.5, 12) | c.ellm(wx0 + 41, 212, 1.6, 4) | c.ellm(wx0 + 51, 209, 1.6, 4), C(120, 120, 70), emit=1)
    c.rect(wx0, (wy0 + wy1) // 2 - 1, wx1, (wy0 + wy1) // 2 + 2, C(70, 42, 26))
    c.rect((wx0 + wx1) // 2 - 1, wy0, (wx0 + wx1) // 2 + 2, wy1, C(70, 42, 26))
    c.rect(wx0 - 8, wy1 + 4, wx1 + 8, wy1 + 9, C(96, 60, 36)); c.rect(wx0 - 8, wy1 + 4, wx1 + 8, wy1 + 5, C(150, 100, 60))
    for x in (wx0 - 3, wx1 - 9):
        for i in range(12):
            c.rect(x + (i % 3), wy0 - 4 + i * 10, x + 12 - (i % 2), wy0 + 6 + i * 10, C(150, 50, 44) if i % 2 else C(132, 42, 38))
    # sign + skull
    c.rect(96, 72, 264, 106, C(60, 34, 20)); c.rect(99, 75, 261, 103, C(174, 118, 66)); c.rect(99, 75, 261, 78, C(206, 150, 88))
    for nx in (103, 255): c.rect(nx, 87, nx + 2, 89, C(220, 210, 190))
    c.text('ПЫЛЬНЫЙ', 180, 84, 8, C(250, 226, 150), C(70, 34, 18))
    c.text('КАКТУС', 180, 96, 8, C(250, 226, 150), C(70, 34, 18))
    c.put(c.ellm(180, 62, 9, 6), C(232, 222, 200))
    for s in (-1, 1):
        c.put(c.poly([(180 + s * 7, 60), (180 + s * 24, 50), (180 + s * 28, 44), (180 + s * 22, 55), (180 + s * 8, 64)]), C(236, 226, 206))
    c.rect(176, 61, 178, 63, C(40, 26, 20)); c.rect(182, 61, 184, 63, C(40, 26, 20))
    # mirror + shelves + bottles
    c.rect(118, 122, 242, 214, C(64, 38, 22)); c.rect(122, 126, 238, 210, C(92, 112, 118))
    for i in range(0, 90, 3): c.line(126 + i, 206, 150 + i, 130, C(118, 140, 146))
    c.rect(122, 126, 238, 130, C(140, 164, 168))
    for i in range(7): F[c.ellm(150 + i * 10, 150, 1.2, 2)] = C(255, 230, 150)
    c.rect(122, 180, 238, 210, C(78, 90, 92))
    for x in range(126, 236, 7): c.rect(x, 186 + (x % 3), x + 3, 198, C(96, 120, 100) if x % 2 else C(120, 96, 80))
    for sy in (236, 270, 304):
        c.rect(84, sy, 276, sy + 5, C(96, 60, 34)); c.rect(84, sy, 276, sy + 1, C(160, 108, 64)); c.rect(84, sy + 5, 276, sy + 7, C(40, 24, 16))
    def bottle(x, base, col, h, kind):
        if kind == 0: c.rect(x, base - h, x + 6, base, col); c.rect(x + 2, base - h - 6, x + 4, base - h, col)
        elif kind == 1:
            F[c.ellm(x + 4, base - h * 0.4, 4.5, h * 0.4)] = col; c.rect(x + 3, base - h, x + 5, base - h * 0.7, col)
        else: c.rect(x, base - h, x + 8, base, col); c.rect(x + 8, base - h + 3, x + 10, base - 4, col * 0.8)
        c.rect(x + 1, base - h + 2, x + 2, base - 3, np.minimum(col * 1.5 + 30, 255))
        c.rect(x + 1, base - h // 2 - 2, x + 5, base - h // 2 + 2, C(230, 214, 170))
    for sy in (236, 270, 304):
        x = 88
        while x < 268:
            if 120 < x < 240 and sy == 236: x += 1; continue
            k = int(rng.integers(0, 3)); h = int(rng.integers(14, 22)); col = BOTTLE_COLS[int(rng.integers(0, len(BOTTLE_COLS)))]
            bottle(x, sy, col, h, k); x += int(rng.integers(9, 13))
    for gx in range(126, 236, 9):
        c.rect(gx, 226, gx + 6, 236, C(190, 210, 214)); c.rect(gx + 1, 227, gx + 2, 235, C(240, 250, 250))
    # poster, menu, rifle, clock, horseshoe, lamps
    c.rect(10, 118, 72, 196, C(236, 218, 170)); c.rect(10, 194, 72, 196, C(200, 176, 124)); c.rect(70, 118, 72, 196, C(200, 176, 124))
    c.put(c.poly([(64, 118), (72, 118), (72, 128)]), WOOD_BASE)
    c.text('РОЗЫСК', 41, 128, 8, C(130, 34, 26))
    F[c.ellm(41, 157, 10, 12)] = C(226, 176, 136)
    c.rect(27, 142, 55, 146, C(46, 40, 48)); F[c.ellm(41, 138, 9, 6)] = C(46, 40, 48)
    c.rect(30, 152, 52, 157, C(24, 20, 24)); c.rect(34, 153, 36, 155, C(250, 250, 250)); c.rect(46, 153, 48, 155, C(250, 250, 250))
    c.rect(31, 163, 51, 166, C(34, 26, 24))
    c.text('$500', 41, 184, 8, C(70, 50, 30))
    c.rect(8, 214, 76, 292, C(70, 42, 26)); c.rect(11, 217, 73, 289, C(38, 50, 42))
    c.text('МЕНЮ', 42, 226, 8, C(236, 236, 220))
    for i, s in enumerate(('ВИСКИ 5¢', 'ВОДА 9¢', 'МОРКОВЬ', '   50¢')):
        c.text(s, 42, 241 + i * 12, 8, C(214, 214, 196) if i != 3 else C(250, 190, 90))
    c.line(20, 104, 80, 110, C(60, 40, 30), 3); c.line(28, 105, 50, 107, C(140, 140, 150), 2)
    F[c.ellm(270, 90, 11, 11)] = C(96, 60, 34); F[c.ellm(270, 90, 8, 8)] = C(236, 226, 196)
    c.line(270, 90, 270, 84, C(30, 20, 16)); c.line(270, 90, 274, 92, C(30, 20, 16))
    F[c.ellm(270, 106, 2, 5)] = C(200, 160, 70)
    F[c.ellm(92, 136, 8, 9) & ~c.ellm(92, 136, 5, 6) & (YY > 131)] = C(150, 150, 160)
    for lx_ in (8, 346): _lamp(c, lx_)
    # chandelier
    c.rect(178, 0, 181, 30, C(40, 30, 26))
    F[c.ellm(180, 36, 34, 6) & ~c.ellm(180, 36, 30, 3.5)] = C(90, 70, 50)
    for i in range(7):
        x = 150 + i * 10
        c.rect(x - 1, 26, x + 2, 34, C(236, 226, 200))
        c.put(c.ellm(x + 0.5, 23, 1.6, 3.2), C(255, 214, 110), emit=1)
        F[c.ellm(x + 0.5, 23.5, 0.8, 1.6)] = C(255, 250, 220)
    # counter
    BT, BB = 430, 505
    c.rect(0, BT, W, BT + 10, C(150, 96, 56)); c.rect(0, BT, W, BT + 2, C(196, 138, 84)); c.rect(0, BT + 10, W, BT + 12, C(40, 24, 16))
    c.planks_v(0, W, BT + 12, BB, 30, C(112, 70, 40), seed=4, seam=C(56, 32, 20))
    for px0 in range(4, W, 30):
        c.rect(px0 + 4, BT + 20, px0 + 24, BB - 12, C(100, 62, 36)); c.rect(px0 + 4, BT + 20, px0 + 24, BT + 21, C(150, 100, 60))
    c.rect(0, BB - 8, W, BB - 5, C(200, 160, 70)); c.rect(0, BB - 8, W, BB - 7, C(250, 220, 130))
    c.rect(240, 404, 246, 430, C(200, 160, 70)); c.rect(236, 402, 250, 407, C(220, 186, 96)); c.rect(242, 396, 244, 404, C(60, 30, 20))
    for mx in (60, 256):
        c.rect(mx, 414, mx + 12, 430, C(214, 190, 120)); c.rect(mx + 12, 417, mx + 16, 427, C(170, 150, 96))
        c.rect(mx, 412, mx + 12, 417, C(250, 248, 236)); c.rect(mx + 2, 418, mx + 4, 428, C(240, 220, 150))
    lx = 94
    F[c.ellm(lx, 422, 8, 7)] = C(180, 130, 60); c.rect(lx - 4, 398, lx + 5, 416, C(210, 226, 220))
    c.put(c.ellm(lx + 0.5, 408, 2.5, 5), C(255, 214, 110), emit=1)
    F[c.ellm(lx + 0.5, 409, 1.2, 2.5)] = C(255, 250, 220)
    F[c.ellm(140, 427, 11, 4) & (YY < 430)] = C(160, 110, 60)
    for i in range(9): c.rect(132 + (i * 5) % 17, 422 + (i % 2), 135 + (i * 5) % 17, 424 + (i % 2), C(214, 170, 110))
    c.floor(FLOOR_Y, 180, 260)
    # piano + pianist
    c.rect(0, 432, 58, 520, C(52, 30, 22)); c.rect(0, 432, 58, 436, C(90, 58, 36))
    c.rect(0, 470, 64, 478, C(40, 24, 16)); c.rect(2, 464, 60, 470, C(240, 236, 224))
    for kx in range(4, 60, 5): c.rect(kx, 464, kx + 2, 468, C(24, 20, 20))
    c.rect(20, 440, 40, 458, C(236, 226, 196)); c.line(22, 446, 38, 446, C(90, 80, 70)); c.line(22, 451, 38, 451, C(90, 80, 70))
    F[c.ellm(66, 452, 9, 16)] = C(70, 90, 110)
    F[c.ellm(68, 428, 7, 7)] = C(214, 164, 124)
    F[c.ellm(68, 423, 11, 3)] = C(50, 40, 34); F[c.ellm(68, 419, 6, 5)] = C(50, 40, 34)
    c.rect(58, 466, 62, 474, C(214, 164, 124))
    # foreground poker table: cards 6 and 7 (meme easter egg)
    F[c.ellm(58, 612, 86, 26)] = C(40, 90, 54); F[c.ellm(58, 612, 86, 26) & (YY > 622)] = C(30, 70, 42)
    F[c.ellm(58, 606, 84, 22) & ~c.ellm(58, 606, 78, 18)] = C(90, 56, 34)
    for i, (cx, cy) in enumerate(((36, 598), (47, 602), (70, 596), (84, 604))):
        c.rect(cx, cy, cx + 10, cy + 13, C(246, 244, 236))
        if i < 2: c.text('67'[i], cx + 5, cy + 7, 8, C(190, 30, 30) if i else C(20, 20, 20))
        else: c.rect(cx + 2, cy + 2, cx + 4, cy + 4, C(190, 30, 30) if i % 2 else C(20, 20, 20))
    for i in range(6): F[c.ellm(100 + i * 2, 606 - i * 2, 5, 2)] = C(200, 40, 40) if i % 2 else C(240, 240, 240)
    F[c.ellm(18, 600, 6, 3)] = C(214, 190, 120); c.rect(12, 588, 24, 600, C(214, 190, 120)); c.rect(12, 586, 24, 590, C(250, 248, 236))
    F[c.ellm(128, 598, 14, 6)] = C(110, 70, 40); F[c.ellm(130, 590, 11, 4)] = C(90, 60, 40)
    F[c.ellm(330, 616, 14, 9)] = C(180, 140, 60); F[c.ellm(330, 610, 10, 3)] = C(60, 40, 20); F[c.ellm(328, 614, 2, 5)] = C(240, 210, 130)
    # light
    Lm = np.full((H, W), 0.62, np.float32)
    Lm += c.glow(180, 30, 330, 0.75) + c.glow(95, 408, 110, 0.55) + c.glow(322, 180, 150, 0.45)
    Lm += c.glow(8, 334, 70, 0.35) + c.glow(346, 334, 70, 0.35)
    bm, ba = c.beam(322, 180, -0.62, 1.0); Lm += ba
    Lm -= _vig(c)
    return c.lit(Lm, [bm])


# ==================================================================== entrance
def entrance_section():
    c = Canvas(BAR_X, WORLD_H, seed=21); F = c.F
    _wall(c, seed=7)
    # doorway with bright desert outside
    dx0, dx1, dy0, dy1 = 28, 112, 262, FLOOR_Y
    c.rect(dx0 - 8, dy0 - 10, dx1 + 8, dy1, C(70, 42, 26)); c.rect(dx0 - 8, dy0 - 10, dx1 + 8, dy0 - 7, C(150, 100, 60))
    for y in range(dy0, dy1):
        k = (y - dy0) / (dy1 - dy0)
        F[y, dx0:dx1] = C(250, 226, 170) * (1 - k) + C(236, 170, 110) * k
    c.EMIT[dy0:dy1, dx0:dx1] = 1
    c.put(c.poly([(dx0, 380), (dx0 + 20, 362), (dx0 + 40, 364), (dx0 + 50, 376), (dx1, 372), (dx1, 420), (dx0, 420)]) &
          (c.XX >= dx0) & (c.XX < dx1), C(216, 134, 92), emit=1)
    c.put((c.YY >= 420) & (c.YY < dy1) & (c.XX >= dx0) & (c.XX < dx1), C(230, 190, 130), emit=1)
    for (cx, cy, h) in ((dx0 + 16, 420, 22), (dx1 - 18, 424, 30)):
        c.put(c.ellm(cx, cy - h / 2, 3, h / 2) | c.ellm(cx - 6, cy - h * 0.6, 2, 5) | c.ellm(cx + 6, cy - h * 0.7, 2, 6), C(110, 140, 80), emit=1)
    c.put(c.ellm(dx1 - 22, dy0 + 24, 9, 9), C(255, 248, 214), emit=1)                        # sun
    # sign over the door
    c.rect(18, 212, 122, 246, C(60, 34, 20)); c.rect(21, 215, 119, 243, C(174, 118, 66))
    c.text('НЕ СТРЕЛЯТЬ', 70, 224, 8, C(250, 226, 150), C(70, 34, 18))
    c.text('В ПИАНИСТА', 70, 236, 8, C(250, 226, 150), C(70, 34, 18))
    # coat rack with hats, antlers
    c.rect(122, 170, 128, 176, C(60, 40, 28))
    for i, hx in enumerate((10, 124)):
        c.line(hx, 150, hx + 6, 144, C(200, 190, 170), 2)
    c.put(c.ellm(125, 180, 10, 3), C(80, 60, 44)); c.put(c.ellm(125, 175, 6, 5), C(80, 60, 44))
    c.put(c.ellm(14, 132, 12, 12), C(96, 60, 34)); c.text('$', 14, 132, 8, C(240, 210, 120))  # «касса» medallion
    c.floor(FLOOR_Y, 70, 260, dust=60)
    # spittoon near door
    F[c.ellm(124, 560, 10, 7)] = C(180, 140, 60); F[c.ellm(124, 555, 7, 2)] = C(60, 40, 20)
    Lm = np.full((c.H, c.W), 0.6, np.float32)
    Lm += c.glow(70, 380, 150, 0.6)
    bm, ba = c.beam(70, 380, 0.5, 1.0, w0=36, amp=0.3, reach=300); Lm += ba
    Lm -= _vig(c)
    return c.lit(Lm, [bm], dust_seed=6)


# ==================================================================== corner
def corner_section():
    c = Canvas(WORLD_W - CORNER_X, WORLD_H, seed=31); F = c.F
    W = c.W
    _wall(c, seed=9)
    # staircase to the rooms (right)
    for i in range(12):
        x0 = 200 + i * 9; y0 = 505 - i * 22
        c.rect(x0, y0 - 22, W, y0, C(104, 66, 38)); c.rect(x0, y0 - 22, W, y0 - 19, C(160, 108, 64)); c.rect(x0, y0 - 1, W, y0, C(50, 30, 18))
    for i in range(0, 12, 2):
        x = 204 + i * 9; y = 505 - i * 22
        c.rect(x, y - 60, x + 3, y - 22, C(80, 50, 30))
    c.line(200, 445, 300, 180, C(90, 56, 32), 4); c.line(200, 444, 300, 179, C(150, 100, 60), 1)
    c.rect(214, 110, 282, 132, C(60, 34, 20)); c.rect(216, 112, 280, 130, C(236, 218, 170))
    c.text('НОМЕРА', 248, 121, 8, C(90, 50, 30))
    # «business meeting» sign on a nail + framed portrait «лучший клиент месяца»
    c.rect(96, 250, 196, 290, C(236, 222, 180)); c.rect(96, 288, 196, 290, C(196, 176, 130))
    c.line(146, 238, 104, 252, C(60, 40, 30)); c.line(146, 238, 188, 252, C(60, 40, 30)); c.rect(145, 236, 148, 239, C(160, 160, 170))
    c.text('ДЕЛОВАЯ', 146, 262, 8, C(130, 34, 26)); c.text('ВСТРЕЧА', 146, 276, 8, C(130, 34, 26))
    c.rect(20, 120, 80, 196, C(150, 110, 50)); c.rect(24, 124, 76, 184, C(96, 124, 140))
    F[c.ellm(50, 170, 14, 16)] = C(190, 140, 90); F[c.ellm(50, 150, 12, 13)] = C(190, 140, 90)     # horse portrait
    F[c.ellm(58, 156, 8, 6)] = C(150, 100, 64); F[c.ellm(44, 140, 3, 5)] = C(190, 140, 90)
    c.put(c.ellm(50, 138, 12, 3), C(196, 154, 96)); c.put(c.ellm(50, 134, 6, 4), C(196, 154, 96))  # ...in a hat
    c.rect(24, 186, 76, 196, C(236, 218, 170)); c.text('ЛУЧШАЯ', 50, 191, 8, C(90, 50, 30))
    _lamp(c, 116)
    c.floor(FLOOR_Y, 110, 260, dust=90)
    # back chair (behind the table spot)
    c.rect(56, 440, 62, 540, C(80, 50, 30)); c.rect(96, 440, 102, 540, C(80, 50, 30))
    for y in (448, 468, 488): c.rect(56, y, 102, y + 5, C(110, 70, 40))
    # crates + barrel of carrots (lore!)
    c.rect(150, 470, 196, 520, C(140, 96, 52)); c.rect(150, 470, 196, 474, C(180, 130, 76))
    c.line(150, 470, 196, 520, C(100, 66, 36), 2); c.text('ОВЁС', 173, 500, 8, C(60, 36, 20))
    F[c.ellm(236, 590, 20, 6)] = C(150, 98, 54); c.rect(216, 540, 256, 590, C(162, 108, 60))
    for y in (552, 576): c.rect(216, y, 256, y + 3, C(80, 80, 88))
    F[c.ellm(236, 538, 17, 6)] = C(70, 44, 24)
    for i in range(7):
        a = i * 0.9
        c.put(c.linem(226 + i * 3, 536, 222 + i * 3 + 3 * np.sin(a), 520, 3), C(236, 128, 40))
        c.put(c.linem(222 + i * 3 + 3 * np.sin(a), 520, 220 + i * 3, 512, 2), C(84, 160, 60))
    Lm = np.full((c.H, c.W), 0.6, np.float32)
    Lm += c.glow(116, 334, 120, 0.45) + c.glow(140, 470, 170, 0.35)
    Lm -= _vig(c)
    return c.lit(Lm)


def post(img, x):
    """support post hiding section seams (drawn on the lit image)"""
    img[:, x - 5:x + 5] = (70, 44, 28); img[:, x - 5:x - 3] = (100, 66, 40); img[:, x + 3:x + 5] = (44, 28, 18)
    for y in range(40, WORLD_H, 90): img[y:y + 3, x - 5:x + 5] = (54, 34, 22)
    img[FLOOR_Y - 12:FLOOR_Y, x - 7:x + 7] = (60, 38, 24)


# ==================================================================== bartender sprite
BT_X, BT_Y = BAR_X + 196, 0      # sprite drawn in bar-section coordinates

def bartender(pose='polish', k=0):
    """RGBA sprite (world px, full world height, 120 px wide centred on bartender). pose: polish|point"""
    c = Canvas(120, WORLD_H); c.A[:] = False
    F = c.F; XX, YY = c.XX, c.YY
    bx = 60
    SHIRT, VEST, SK, SKD = C(238, 236, 228), C(56, 60, 78), C(232, 180, 136), C(214, 160, 118)
    c.put(c.ellm(bx, 398, 27, 36) & (YY < 430), SHIRT)
    c.put(c.ellm(bx, 404, 20, 34) & (np.abs(XX - bx) > 6) & (YY < 430), VEST)
    c.rect(bx - 1, 372, bx + 1, 430, C(200, 196, 186))
    for by in (380, 390, 400, 410): c.rect(bx - 1, by, bx + 1, by + 2, C(90, 80, 70))
    # left arm (glass/towel side) always polishing
    ax = bx - 26
    c.put(c.ellm(ax, 392, 8, 16), SHIRT); c.rect(ax - 7, 386, ax + 7, 390, C(190, 40, 40))
    gy = 404 + (2 if k % 2 else 0)
    if pose == 'point':
        c.put(c.ellm(bx - 14, 414, 9, 7), SK)
        c.rect(bx - 6, 402, bx + 6, 420, C(196, 214, 218)); c.rect(bx - 5, 404, bx - 3, 418, C(250, 255, 255))
        # right arm straight out to the right (towards the corner)
        c.put(c.linem(bx + 18, 378, bx + 52, 372, 12), SHIRT); c.rect(bx + 34, 366, bx + 38, 379, C(190, 40, 40))
        c.put(c.ellm(bx + 55, 372, 5, 4), SK); c.put(c.linem(bx + 56, 370, bx + 64, 369, 3), SK)
    else:
        c.put(c.ellm(bx + 26, 392, 8, 16), SHIRT); c.rect(bx + 19, 386, bx + 33, 390, C(190, 40, 40))
        c.put(c.ellm(bx - 14, 414 + (k % 2), 9, 7), SK); c.put(c.ellm(bx + 12, 416 - (k % 2), 9, 7), SK)
        c.rect(bx - 6, gy - 2, bx + 6, gy + 16, C(196, 214, 218)); c.rect(bx - 5, gy, bx - 3, gy + 14, C(250, 255, 255))
        c.put(c.poly([(bx - 22, 408 + k % 2 * 2), (bx - 4, 404), (bx + 2, 424), (bx - 18, 426)]), C(236, 230, 212))
        c.line(bx - 18, 414, bx - 4, 412, C(200, 60, 50))
    c.put(c.ellm(bx, 366, 5, 3), C(190, 40, 40)); c.put(c.ellm(bx - 6, 366, 4, 3), C(170, 30, 30)); c.put(c.ellm(bx + 6, 366, 4, 3), C(170, 30, 30))
    c.put(c.ellm(bx, 340, 15, 17), SK)
    F[c.ellm(bx, 346, 15, 11) & (YY > 346)] = SKD
    F[c.ellm(bx, 327, 13, 7) & (YY < 330)] = C(246, 200, 160)
    c.put(c.ellm(bx - 14, 338, 4, 7), C(60, 44, 36)); c.put(c.ellm(bx + 14, 338, 4, 7), C(60, 44, 36))
    c.put(c.ellm(bx - 16, 342, 3, 4), SKD); c.put(c.ellm(bx + 16, 342, 3, 4), SKD)
    look = 2 if pose == 'point' else 0
    for ex in (-6, 6):
        F[c.ellm(bx + ex, 338, 3, 2.5)] = C(250, 250, 244); c.rect(bx + ex - 1 + look, 337, bx + ex + 1 + look, 340, C(30, 20, 18))
        c.rect(bx + ex - 4, 333, bx + ex + 4, 335, C(60, 44, 36))
    F[c.ellm(bx, 344, 3.5, 3)] = C(220, 140, 110)
    F[c.ellm(bx - 9, 346, 3, 2)] = C(236, 150, 130); F[c.ellm(bx + 9, 346, 3, 2)] = C(236, 150, 130)
    c.put(c.poly([(bx - 17, 351), (bx - 3, 347), (bx, 350), (bx + 3, 347), (bx + 17, 351), (bx + 19, 346), (bx + 14, 355), (bx, 352), (bx - 14, 355), (bx - 19, 346)]), C(60, 36, 24))
    img = np.clip(c.F * 1.05, 0, 255).astype(np.uint8)
    return np.dstack([img, (c.A * 255).astype(np.uint8)])


# ==================================================================== outside (split-screen chase strip)
OUT_W, OUT_H = 1440, 320

def outside_strip():
    c = Canvas(OUT_W, OUT_H, seed=41); F = c.F
    SKY = [C(84, 128, 188), C(118, 160, 204), C(164, 192, 212), C(220, 204, 172), C(242, 194, 140)]
    for y in range(OUT_H):
        k = min(0.999, y / 190) * (len(SKY) - 1); i = int(k); f = k - i
        F[y, :] = SKY[i] * (1 - f) + SKY[min(i + 1, len(SKY) - 1)] * f
    c.EMIT[:] = 1
    r = c.rng
    for m in range(14):
        x0 = m * 110 + r.integers(-20, 20); w = r.integers(60, 120); top = r.integers(120, 160)
        c.put(c.poly([(x0, 200), (x0 + 14, top), (x0 + w - 14, top), (x0 + w, 200)]), C(206, 124, 88), emit=1)
        c.put(c.poly([(x0 + 14, top), (x0 + w - 14, top), (x0 + w - 18, top + 6), (x0 + 18, top + 6)]), C(232, 150, 104), emit=1)
    c.put(c.YY >= 200, C(226, 184, 124), emit=1)
    for y in range(200, OUT_H, 9): c.rect(0, y, OUT_W, y + 1, C(206, 164, 108), emit=1)
    for i in range(40):
        x, y = int(r.integers(0, OUT_W)), int(r.integers(206, OUT_H))
        c.put(c.ellm(x, y, 3, 2), C(170, 130, 90), emit=1)
    for i in range(10):
        x = 60 + i * 140 + int(r.integers(-30, 30)); h = int(r.integers(24, 44)); y = 250
        c.put(c.ellm(x, y - h / 2, 4, h / 2) | c.ellm(x - 8, y - h * 0.6, 3, 7) | c.ellm(x + 8, y - h * 0.7, 3, 8), C(90, 150, 72), emit=1)
    c.put(c.ellm(1100, 60, 16, 16), C(255, 244, 200), emit=1)
    return np.clip(c.F, 0, 255).astype(np.uint8)


# ==================================================================== build + cache
def build(force=False):
    cache = PATHS.build('props', 'saloon_world.npz')
    if os.path.exists(cache) and not force:
        d = np.load(cache)
        return d['world'], {k[3:]: d[k] for k in d.files if k.startswith('bt_')}, d['outside']
    world = np.concatenate([entrance_section(), bar_section(), corner_section()], 1).astype(np.uint8)
    world = quantize(world, 110)
    post(world, BAR_X); post(world, CORNER_X)
    bts = {f'{p}{k}': bartender(p, k) for p in ('polish', 'point') for k in (0, 1)}
    outside = quantize(outside_strip(), 48)
    np.savez_compressed(cache, world=world, outside=outside, **{f'bt_{k}': v for k, v in bts.items()})
    return world, bts, outside


if __name__ == '__main__':
    from PIL import Image
    world, bts, outside = build(force=True)
    Image.fromarray(world).save(PATHS.build('props', 'saloon_world.png'))
    Image.fromarray(outside).save(PATHS.build('props', 'outside.png'))
    print('ok', world.shape, outside.shape)
