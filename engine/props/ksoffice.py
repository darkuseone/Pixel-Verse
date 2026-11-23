"""«Ключевой сотрудник», variant B (owner test 22.11.2026): the office drawn ENTIRELY in code as a pixel-game backdrop, same layout as the
xAI office (door 40–225, window 815–1185, honor board 318–545, desks in the middle, cooler + printer on the right), so the episode code
works on both. Painted at half resolution (640x360 «game pixels», then x2 nearest), hand-placed shading: 3–4 tone ramps, ordered dither
on big gradients, 1-px dark outlines on furniture, a glowing fluorescent ceiling, a dusk/night/morning city in the window.
The depth map comes from the geometry itself (floor rows, wall plane, furniture fronts), saved as <name>.depth.png for depth25.
  python3 engine/props/ksoffice.py      -> series/klyuchevoy/bg/code_office{,_night,_morning}.png + .depth.png"""
import math, sys, pathlib
import numpy as np
from PIL import Image, ImageDraw

W, H = 640, 360
B4 = np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]], np.float32) / 16.0
OUT = pathlib.Path(__file__).resolve().parents[2] / 'series' / 'klyuchevoy' / 'bg'


def C(*c): return np.array(c, np.float32)


def shade(c, k): return np.clip(np.array(c, np.float32) * k, 0, 255)


class Canvas:
    def __init__(s, tod):
        s.tod = tod
        s.img = np.zeros((H, W, 3), np.float32)
        s.near = np.zeros((H, W), np.float32)
        s.yy, s.xx = np.mgrid[0:H, 0:W]
        s.bay = np.tile(B4, (H // 4 + 1, W // 4 + 1))[:H, :W]

    def rect(s, x0, y0, x1, y1, col, near=None, grad=None, dither=True):
        x0, y0, x1, y1 = int(x0), int(y0), int(max(x0 + 1, x1)), int(max(y0 + 1, y1))
        reg = s.img[y0:y1, x0:x1]
        if grad is None: reg[:] = col
        else:                                                           # vertical gradient col -> grad, ordered dither in 4 steps
            k = (s.yy[y0:y1, x0:x1] - y0) / max(1, (y1 - y0 - 1))
            if dither: k = np.floor(k * 4 + s.bay[y0:y1, x0:x1]) / 4
            reg[:] = np.array(col, np.float32) * (1 - k[..., None]) + np.array(grad, np.float32) * k[..., None]
        if near is not None: s.near[y0:y1, x0:x1] = near

    def poly(s, pts, col, near=None):
        m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).polygon(pts, fill=255)
        m = np.array(m) > 0
        s.img[m] = col
        if near is not None: s.near[m] = near if np.isscalar(near) else near[m]
        return m

    def outline(s, x0, y0, x1, y1, col):
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        s.img[y0, x0:x1] = col; s.img[y1 - 1, x0:x1] = col; s.img[y0:y1, x0] = col; s.img[y0:y1, x1 - 1] = col

    def px(s, x, y, col):
        if 0 <= x < W and 0 <= y < H: s.img[int(y), int(x)] = col


def floor_near(y):
    return 0.16 + 0.84 * np.clip((y - 255) / (H - 255), 0, 1) ** 0.9


def paint(tod='evening'):
    c = Canvas(tod)
    night, morning = tod == 'night', tod == 'morning'
    L = 0.42 if night else (1.04 if morning else 1.0)                                     # room light level
    wall, wall_d = C(214, 198, 140) * L, C(176, 160, 108) * L
    if night: wall, wall_d = C(70, 76, 104), C(52, 56, 82)
    # ---------------------------------------------------------------- ceiling
    c.rect(0, 0, W, 22, shade((150, 160, 120), L * (0.6 if night else 1)), near=0.10, grad=shade((120, 128, 96), L * (0.6 if night else 1)))
    for x in range(0, W, 40): c.rect(x, 0, x + 1, 22, shade((110, 116, 88), L))
    c.rect(0, 22, W, 25, shade((90, 92, 70), L), near=0.12)
    for x in range(-200, 900, 48):                                                        # ceiling grid in perspective
        for y in range(0, 22):
            xx = int(320 + (x - 320) * (1.0 + (22 - y) / 22 * 0.35))
            if 0 <= xx < W: c.img[y, xx] = c.img[y, xx] * 0.82
    for (x0, x1, y) in ((150, 260, 6), (300, 380, 26 - 18), (355, 452, 10)):          # fluorescent tubes
        c.rect(x0, y, x1, y + 6, (70, 74, 62))
        c.rect(x0 + 3, y + 2, x1 - 3, y + 4, (120, 130, 110) if night else (236, 255, 214))
    # ---------------------------------------------------------------- walls
    c.rect(0, 25, 352, 258, wall, near=0.16, grad=wall_d)
    c.rect(352, 25, W, 258, shade(wall, 0.92), near=0.18, grad=shade(wall_d, 0.92))
    c.rect(351, 25, 353, 258, shade(wall_d, 0.7))                                          # the corner
    low = C(120, 138, 96) * L if not night else C(44, 56, 70)                              # soviet olive lower half of the walls
    c.rect(0, 172, 352, 250, low, grad=shade(low, 0.86)); c.rect(352, 172, W, 250, shade(low, 0.92), grad=shade(low, 0.80))
    c.rect(0, 171, W, 173, shade(low, 0.6))
    if not night:                                                                          # light pools from the tubes on the wall
        for x0 in (205, 404):
            m = ((c.xx - x0) / 120.0) ** 2 + ((c.yy - 25) / 60.0) ** 2 < 1
            m &= (c.yy < 171) & (((c.xx + c.yy) % 2) == 0)
            c.img[m] = np.clip(c.img[m] * 1.07, 0, 255)
    rng = np.random.default_rng(4)
    for _ in range(60):                                                                    # old paint stains
        x, y, r = rng.integers(0, W), rng.integers(30, 250), rng.integers(2, 7)
        m = (c.xx - x) ** 2 + ((c.yy - y) * 1.6) ** 2 < r * r
        m &= c.yy < 256
        c.img[m] = c.img[m] * 0.93
    c.rect(0, 250, W, 258, shade((96, 70, 44), L * (0.6 if night else 1)), near=0.17)    # skirting board
    # ---------------------------------------------------------------- floor: brown linoleum tiles in perspective
    fl = C(150, 104, 58) * (0.5 if night else L)
    c.rect(0, 258, W, H, fl, near=None, grad=shade(fl, 0.78))
    c.near[258:, :] = floor_near(c.yy[258:, :])
    vx, vy = 320, 150
    for x in range(-640, 1300, 56):                                                        # tile seams to the vanishing point
        for y in range(258, H):
            t = (y - vy) / (H - vy); xx = int(vx + (x - vx) * t)
            if 0 <= xx < W: c.img[y, xx] = c.img[y, xx] * 0.78
    y = 258.0; k = 8.0
    while y < H:
        c.img[int(y), :] *= 0.80; y += k; k *= 1.28
    for _ in range(26):                                                                    # worn spots
        x, y = rng.integers(0, W), rng.integers(262, H)
        m = ((c.xx - x) / 18.0) ** 2 + ((c.yy - y) / 5.0) ** 2 < 1
        c.img[m] = c.img[m] * 1.08
    if not night:                                                                          # tube reflections on the floor
        for x0 in (205, 340, 400):
            m = (np.abs(c.xx - x0) < 26) & (c.yy > 262) & ((c.yy + c.xx // 3) % 3 == 0)
            c.img[m] = np.clip(c.img[m] * 1.10, 0, 255)
    # ---------------------------------------------------------------- the boss's door
    c.rect(19, 77, 113, 258, shade((120, 116, 104), L * (0.7 if night else 1)), near=0.17)
    c.rect(30, 86, 103, 254, shade((92, 50, 30), L * (0.65 if night else 1)), near=0.17, grad=shade((70, 36, 22), L * (0.65 if night else 1)))
    for (y0, y1) in ((96, 160), (172, 244)):                                               # panels
        c.outline(37, y0, 96, y1, shade((60, 30, 18), L)); c.rect(38, y0 + 1, 95, y0 + 3, shade((120, 70, 40), L))
    c.rect(36, 172, 44, 182, (210, 176, 80)); c.rect(36, 174, 48, 176, (230, 200, 100))   # brass handle
    c.outline(19, 77, 113, 258, shade((60, 56, 50), L))
    # clock base (hands are animated by ksdecor.clock)
    m = (c.xx - 68) ** 2 + (c.yy - 53) ** 2 < 17 ** 2; c.img[m] = (40, 36, 34)
    m = (c.xx - 68) ** 2 + (c.yy - 53) ** 2 < 15 ** 2; c.img[m] = shade((236, 232, 218), 0.5 if night else 1)
    # light switch
    c.rect(125, 156, 133, 168, shade((236, 232, 220), L)); c.outline(125, 156, 133, 168, shade((90, 90, 90), L)); c.rect(128, 159, 130, 164, (60, 60, 60))
    # ---------------------------------------------------------------- honor board + the empty frame
    c.rect(159, 75, 273, 150, shade((96, 62, 34), L), near=0.17)
    c.rect(163, 79, 269, 146, shade((176, 130, 80), L))
    for (x0, y0, x1, y1) in ((168, 92, 202, 131), (208, 92, 232, 120), (238, 92, 264, 112), (238, 116, 264, 140)):
        c.rect(x0, y0, x1, y1, shade((236, 226, 196), L)); c.outline(x0, y0, x1, y1, shade((120, 90, 50), L))
    c.rect(291, 91, 326, 145, shade((140, 100, 56), L), near=0.17); c.rect(294, 94, 323, 142, shade((236, 228, 206), L))
    # shelf with binders between the empty frame and the corner
    c.rect(282, 168, 348, 171, shade((110, 76, 44), L), near=0.17)
    bcol = [(170, 50, 50), (50, 80, 150), (60, 120, 70), (200, 170, 60), (90, 60, 120), (50, 80, 150), (170, 50, 50), (120, 120, 120)]
    for i, col in enumerate(bcol):
        x = 284 + i * 8
        c.rect(x, 149 + (i % 3), x + 7, 168, shade(col, L * (0.6 if night else 1)), near=0.17)
        c.rect(x + 2, 155, x + 5, 159, shade((240, 236, 220), L * (0.6 if night else 1)))
    # coat rack by the door: Эдик's grey coat is NOT here (he wears it); someone's umbrella is
    c.rect(122, 120, 125, 252, shade((70, 46, 30), L), near=0.18)
    for dx in (-7, 7): c.rect(123 + dx - 1, 120, 123 + dx + 2, 123, shade((70, 46, 30), L))
    c.rect(116, 180, 121, 230, shade((40, 60, 120), L)); c.rect(114, 228, 123, 232, shade((40, 60, 120), L))
    # ---------------------------------------------------------------- window with the city
    wx0, wy0, wx1, wy1 = 407, 22, 593, 180
    c.rect(wx0, wy0, wx1, wy1, shade((200, 200, 190), L * (0.6 if night else 1)), near=0.18)
    sky = ((40, 30, 80), (230, 120, 90)) if tod == 'evening' else (((10, 14, 34), (30, 34, 70)) if night else ((150, 166, 190), (206, 214, 224)))
    for (x0, x1) in ((413, 488), (494, 587)):
        c.rect(x0, wy0 + 6, x1, wy1 - 6, sky[0], near=0.0, grad=sky[1])
        # panel buildings, lit windows
        for b in range(5):
            bx = x0 + b * (x1 - x0) // 5 + rng.integers(-3, 3); bw = rng.integers(10, 18); bh = rng.integers(40, 90)
            top = wy1 - 6 - bh
            col = (40, 44, 70) if not morning else (120, 128, 150)
            c.rect(bx, top, min(x1, bx + bw), wy1 - 6, col, near=0.02)
            for yy in range(top + 3, wy1 - 8, 5):
                for xx in range(bx + 2, min(x1 - 1, bx + bw - 1), 4):
                    on = rng.random() < (0.55 if not morning else 0.2)
                    c.px(xx, yy, (255, 214, 120) if on else (30, 34, 50)); c.px(xx + 1, yy, (255, 214, 120) if on else (30, 34, 50))
    c.rect(488, wy0 + 6, 494, wy1 - 6, shade((200, 200, 190), L * (0.6 if night else 1)))     # mullion
    for i in range(10):                                                                     # half-down blinds
        y = wy0 + 6 + i * 6
        c.rect(413, y, 587, y + 4, shade((214, 210, 196), L * (0.55 if night else 1)), near=0.18)
        c.rect(413, y + 4, 587, y + 5, shade((140, 136, 120), L * (0.55 if night else 1)))
    c.outline(wx0, wy0, wx1, wy1, shade((90, 90, 84), L))
    # windowsill (the ficus stands on it) + radiator
    c.rect(400, 176, 600, 190, shade((240, 240, 232), L * (0.6 if night else 1)), near=0.2)
    c.rect(400, 189, 600, 191, shade((150, 150, 140), L))
    c.rect(460, 202, 526, 248, shade((210, 212, 206), L * (0.6 if night else 1)), near=0.2)
    for x in range(462, 526, 5): c.rect(x, 202, x + 1, 248, shade((150, 152, 146), L))
    # ---------------------------------------------------------------- water cooler + printer table
    c.rect(586, 196, 636, 300, shade((90, 120, 170), L * (0.6 if night else 1)), near=0.42, grad=shade((60, 84, 130), L))
    m = ((c.xx - 611) / 22.0) ** 2 + ((c.yy - 168) / 28.0) ** 2 < 1                         # the big blue bottle
    c.img[m] = shade((120, 180, 230), 0.7 if night else 1); c.near[m] = 0.40
    c.rect(600, 140, 622, 146, shade((90, 140, 200), L))
    for (x, col) in ((600, (220, 60, 60)), (614, (60, 120, 220))): c.rect(x, 216, x + 6, 224, col)
    c.rect(517, 210, 585, 290, shade((150, 140, 120), L * (0.6 if night else 1)), near=0.35)   # printer table
    c.rect(522, 186, 580, 212, shade((216, 214, 204), L * (0.6 if night else 1)), near=0.35)   # the printer
    c.rect(528, 190, 574, 194, shade((80, 80, 80), L)); c.rect(534, 206, 568, 210, (250, 250, 250) if not night else (110, 110, 120))
    # ---------------------------------------------------------------- desks with partitions, CRT monitors, chairs, the lamp
    def desk(x0, x1, ytop, depth):
        fab = shade((112, 124, 140), L * (0.6 if night else 1))                             # fabric cubicle panel
        c.rect(x0, ytop - 40, x1, ytop, fab, near=depth - 0.03)
        m = (c.yy[ytop - 40:ytop, x0:x1] + c.xx[ytop - 40:ytop, x0:x1]) % 4 == 0
        c.img[ytop - 40:ytop, x0:x1][m] *= 0.9
        c.rect(x0, ytop - 42, x1, ytop - 39, shade((170, 176, 184), L * (0.6 if night else 1)), near=depth - 0.03)
        c.rect(x0 - 2, ytop - 42, x0 + 2, ytop, shade((170, 176, 184), L * (0.6 if night else 1)), near=depth - 0.02)
        c.rect(x0, ytop, x1, ytop + 6, shade((200, 170, 110), L * (0.6 if night else 1)), near=depth)                 # desk top
        c.rect(x0 + 2, ytop + 6, x1 - 2, ytop + 52, shade((150, 136, 104), L * (0.6 if night else 1)), near=depth + 0.02,
               grad=shade((110, 98, 74), L * (0.6 if night else 1)))
        c.rect(x1 - 26, ytop + 10, x1 - 6, ytop + 48, shade((170, 156, 120), L * (0.6 if night else 1)), near=depth + 0.03)   # drawers
        for q in range(3): c.rect(x1 - 20, ytop + 18 + q * 11, x1 - 12, ytop + 19 + q * 11, (60, 50, 40))
    def crt(x, y, depth, on=True):
        c.rect(x - 16, y - 26, x + 16, y + 2, shade((226, 216, 180), L * (0.6 if night else 1)), near=depth)
        scr = (60, 90, 80) if not on else ((80, 150, 140) if not night else (70, 110, 200))
        c.rect(x - 12, y - 22, x + 12, y - 4, scr, near=depth)
        c.rect(x - 8, y + 2, x + 8, y + 6, shade((200, 190, 160), L), near=depth)
        c.rect(x - 14, y + 8, x + 14, y + 12, shade((220, 214, 190), L), near=depth)       # keyboard
    desk(140, 350, 210, 0.32); desk(358, 455, 206, 0.30)
    crt(190, 202, 0.31); crt(252, 200, 0.31, on=False); crt(390, 198, 0.29)
    # the desk lamp (warm pool of light)
    c.rect(300, 180, 304, 210, (40, 90, 50)); c.poly([(292, 178), (316, 178), (308, 168)], (50, 120, 60), near=0.31)
    m = ((c.xx - 302) / 46.0) ** 2 + ((c.yy - 214) / 14.0) ** 2 < 1
    c.img[m] = np.clip(c.img[m] * (1.35 if night else 1.12) + np.array((30, 18, 0)), 0, 255)
    for (x, y, d) in ((222, 262, 0.42), (414, 256, 0.40)):                                # chairs
        c.rect(x - 12, y - 30, x + 12, y - 4, (46, 46, 54), near=d); c.rect(x - 14, y - 4, x + 14, y + 2, (36, 36, 42), near=d)
        c.rect(x - 1, y + 2, x + 1, y + 14, (30, 30, 34), near=d)
        for dx in (-10, 0, 10): c.rect(x + dx - 2, y + 14, x + dx + 2, y + 16, (24, 24, 28), near=d)
    # contact shadows on the floor (furniture stands on it)
    for (x0, x1, y) in ((140, 350, 262), (358, 455, 258), (517, 585, 290), (586, 636, 300), (19, 113, 258)):
        for q in range(5):
            yy = y + q
            if yy < H: c.img[yy, x0 - 4 + q:x1 + 4 - q] *= (0.62 + q * 0.07)
    # wall-floor ambient occlusion
    for q in range(4): c.img[258 + q, :] *= 0.8 + q * 0.05
    # desk props: a phone, paper stacks, a trash bin, cables
    c.rect(318, 202, 330, 209, (40, 40, 44)); c.rect(319, 200, 329, 203, (60, 60, 66))
    for k in range(4): c.rect(166, 206 - k * 2, 180, 208 - k * 2, (246, 244, 236) if k % 2 else (226, 224, 214))
    c.rect(326, 238, 342, 258, shade((90, 96, 100), L * (0.6 if night else 1)), near=0.36); c.rect(325, 236, 343, 239, shade((120, 126, 130), L))
    c.rect(328, 232, 334, 237, (246, 244, 236)); c.rect(335, 233, 340, 237, (236, 230, 200))
    for (x0, x1) in ((200, 206), (396, 402)):
        for y in range(216, 258): c.px(x0 + int(2 * math.sin(y * 0.3)), y, (30, 30, 34))
    # papers + mugs on the desks
    for (x, y) in ((160, 206), (330, 205), (430, 202)):
        c.rect(x, y, x + 12, y + 3, (246, 244, 236))
    c.rect(345, 200, 351, 208, (240, 240, 236)); c.rect(346, 199, 350, 201, (120, 70, 40))
    for (x0, y0, x1, y1) in ((586, 196, 636, 300), (517, 210, 585, 290), (522, 186, 580, 212), (140, 210, 350, 262), (358, 206, 455, 258)):
        c.outline(x0, y0, x1, y1, shade((40, 34, 30), 1.0))
    # night: dark blue cast + monitor glows
    img = c.img
    if night:
        for (x, y) in ((190, 190), (390, 186)):
            m = ((c.xx - x) / 40.0) ** 2 + ((c.yy - y) / 26.0) ** 2 < 1
            img[m] = np.clip(img[m] + np.array((10, 24, 40)), 0, 255)
    near = c.near.copy()
    big = np.repeat(np.repeat(np.clip(img, 0, 255).astype(np.uint8), 2, 0), 2, 1)
    nb = np.repeat(np.repeat(near, 2, 0), 2, 1)
    return big, nb


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    for tod, name in (('evening', 'code_office'), ('night', 'code_office_night'), ('morning', 'code_office_morning')):
        img, near = paint(tod)
        Image.fromarray(img).save(OUT / f'{name}.png')
        Image.fromarray((np.clip(near, 0, 1) * 65535).astype(np.uint16)).save(OUT / f'{name}.depth.png')
        print(OUT / f'{name}.png')


if __name__ == '__main__':
    build()
