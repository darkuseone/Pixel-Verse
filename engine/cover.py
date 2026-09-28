"""Series cover style «Почти Дикий Запад»:
- pixel canvas 540x960 (2.5x the episode canvas), upscaled x2 -> 1080x1920
- font Press Start 2P (8px grid, full Cyrillic), sizes multiple of 8, warm yellow->orange stepped gradient,
  4px dark-brown outline + 5px drop shadow; plank badge on top with series + episode
- text kept inside the centre 3:4 safe zone (TikTok/Instagram grid crop)."""
import numpy as np, math, sys
from PIL import Image, ImageDraw, ImageFont
import paths as P
import scene as S
import hd

K = 5
W, H = 108 * K, 192 * K
S.W, S.H = W, H
S.YY, S.XX = [a.astype(np.float32) + 0.5 for a in np.mgrid[0:H, 0:W]]
hd.K, hd.W, hd.H, hd.XX, hd.YY = K, W, H, S.XX, S.YY

FONT_PATH = P.FONT_PX
TEXT_TOP = (255, 236, 120); TEXT_MID = (255, 200, 70); TEXT_BOT = (255, 150, 50)
OUTLINE = (42, 22, 12); SHADOW = (20, 10, 6)
PLANK = (132, 84, 48); PLANK_H = (164, 110, 66); PLANK_D = (92, 56, 32)


def pixel_text(F, lines, top, size, max_w=500, gap=6):
    font = ImageFont.truetype(FONT_PATH, size)
    try: font.set_variation_by_axes([700])
    except Exception: pass
    y = top
    for line in lines:
        fsz = size
        while True:
            f = ImageFont.truetype(FONT_PATH, fsz)
            try: f.set_variation_by_axes([700])
            except Exception: pass
            bb = f.getbbox(line)
            if bb[2] - bb[0] <= max_w or fsz <= 16: break
            fsz -= 8
        img = Image.new('L', (W, fsz * 2), 0)
        d = ImageDraw.Draw(img); d.fontmode = '1'
        tw = bb[2] - bb[0]
        d.text(((W - tw) // 2 - bb[0], -bb[1] + 8), line, font=f, fill=255)
        m = np.array(img) > 127
        rows = np.where(m.any(1))[0]
        if len(rows) == 0: continue
        m = m[:rows[-1] + 14]
        hh = m.shape[0]
        # outline (square dilation 4px) + shadow
        dil = m.copy()
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                dil |= np.roll(np.roll(m, dy, 0), dx, 1)
        sh = np.roll(np.roll(dil, 5, 0), 3, 1)
        reg = F[y:y + hh]
        hh = reg.shape[0]; m, dil, sh = m[:hh], dil[:hh], sh[:hh]
        reg[sh] = SHADOW
        reg[dil] = OUTLINE
        r0, r1 = rows[0], rows[-1]
        for yy in range(hh):
            k = (yy - r0) / max(1, r1 - r0)
            col = TEXT_TOP if k < 0.34 else TEXT_MID if k < 0.67 else TEXT_BOT
            reg[yy][m[yy]] = col
        # 2px highlight line on top edge of glyphs
        top_edge = m & ~np.roll(m, 2, 0)
        reg[top_edge] = (255, 250, 214)
        y += (r1 - r0) + gap + 14
    return y


def plank(F, text, y, size=16, gap=10):
    """wooden plank with pixel text; '\n' in text = several rows (bigger, readable in the phone grid). Returns bottom y."""
    f = ImageFont.truetype(FONT_PATH, size)
    try: f.set_variation_by_axes([700])
    except Exception: pass
    rows = text.split('\n')
    bbs = [f.getbbox(r) for r in rows]
    tw = max(b[2] - b[0] for b in bbs); th = max(b[3] - b[1] for b in bbs)
    pw, ph = tw + 40, th * len(rows) + gap * (len(rows) - 1) + 22
    x0 = (W - pw) // 2
    F[y - 3:y + ph + 3, x0 - 3:x0 + pw + 3] = OUTLINE
    F[y:y + ph, x0:x0 + pw] = PLANK
    F[y:y + 4, x0:x0 + pw] = PLANK_H
    F[y + ph - 4:y + ph, x0:x0 + pw] = PLANK_D
    for gx in range(x0 + 14, x0 + pw - 10, 37):  # wood grain
        F[y + 8:y + ph - 8:3, gx] = PLANK_D
    for nx in (x0 + 7, x0 + pw - 9):  # nails
        F[y + ph // 2 - 2:y + ph // 2 + 2, nx:nx + 3] = (210, 200, 180)
    img = Image.new('L', (W, ph), 0)
    d = ImageDraw.Draw(img); d.fontmode = '1'
    for i, (r, bb) in enumerate(zip(rows, bbs)):
        rw = bb[2] - bb[0]
        d.text(((W - rw) // 2 - bb[0], 11 + i * (th + gap) - bb[1]), r, font=f, fill=255)
    m = np.array(img) > 127
    reg = F[y:y + ph]
    reg[np.roll(np.roll(m, 3, 0), 2, 1) & ~m] = PLANK_D
    reg[m] = (255, 236, 170)
    return y + ph


def render_cover(title_lines, badge, out_png, out_frame=None):
    hd.SUN = (93, 104)
    camx = 258.0
    F = hd.background_hd(camx, 0.0)
    sc = 6.0
    cam = S.Cam(8.3, 25.0, sc)
    # cactus + dazed cowboy (right)
    cx = 8.3 + 462 / sc
    L = S.Layer(cam); S.cactus(L, cx, S.GROUND + 2, 0.0); S.outline(L, (40, 72, 36)); S.comp(F, L)
    L = S.Layer(cam)
    hip = (cx + 0.3, S.GROUND + 2 - 25.2)
    S.cowboy(L, hip, -0.12, S.pose_sit(0.5, 1.0), False, 1.0)
    for dx, dy in ((-1.2, 0.2), (1.0, -0.4), (0.2, 0.6), (-0.6, -0.8)):
        S.dot(L, (hip[0] + dx, hip[1] + dy + 1.5), (250, 246, 220), 0.3)
    S.outline(L, S.CC['ol']); S.comp(F, L)
    L = S.Layer(cam)
    for i, a in enumerate((0.3, 2.4, 4.4)):
        S.star(L, (hip[0] + 0.6 + 5.5 * math.cos(a), hip[1] - 13 + 1.8 * math.sin(a)))
    S.comp(F, L)
    # horse (foreground, big): deadpan, wearing Billy's hat, carrot in mouth
    P = S.stand_pose(0); P.update(lid=0.6, ear=0.25, jaw=0.3, neck=-1.02, head=0.5)
    hx, hy = 40.0, S.GROUND - 19
    hs0 = S.horse_frames(hx, hy, P)[3]
    sc2 = 15.0
    cam = S.Cam(hs0[0] - 200 / sc2, hs0[1] - 640 / sc2, sc2)
    L = S.Layer(cam)
    T, hs, hdir, up = S.draw_horse(L, hx, hy, P, 0.0, 0.0, saddle=True)
    he = (hs[0] + hdir[0] * 8.5, hs[1] + hdir[1] * 8.5)
    dn = (-hdir[1], hdir[0])
    c0 = (he[0] + dn[0] * 1.6 - hdir[0] * 0.8, he[1] + dn[1] * 1.6 - hdir[1] * 0.8)
    c1 = (c0[0] + 5.2, c0[1] + 1.0)
    S.cap(L, c0, c1, 1.7, 0.55, (236, 128, 40), hi=(255, 176, 90))
    for a in (-0.5, 0.0, 0.5):
        S.cap(L, (c0[0] - 0.4, c0[1]), (c0[0] - 2.4, c0[1] - 1.6 - 1.2 * a), 0.55, 0.3, (84, 160, 60))
    pos, rot = S.head_hat_anchor(hx, hy, P); S.hat(L, pos, rot)
    S.draw_ears(L, hs, hdir, up, P['ear'])
    S.outline(L, S.HC['ol']); S.comp(F, L)
    # vignette-ish darkening of the top band for text contrast (stepped, pixel style)
    for i, yy in enumerate(range(0, 110, 22)):
        F[yy:yy + 22] = (F[yy:yy + 22].astype(np.float32) * (0.62 + 0.07 * i)).astype(np.uint8)
    plank(F, badge, 134, 16)
    pixel_text(F, title_lines, 196, 64, max_w=512, gap=10)
    img = Image.fromarray(F).resize((1080, 1920), Image.NEAREST)
    img.save(out_png)
    return np.array(img)


if __name__ == '__main__':
    render_cover(['САМЫЙ', 'БЫСТРЫЙ?'], 'ПОЧТИ ДИКИЙ ЗАПАД • 1/6', str(P.episode('ep01') / 'cover.png'))
