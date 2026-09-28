"""Double-resolution patch: logical canvas 216x384 (x5 -> 1080x1920).
World units stay in the old 108x192 space; cameras use scale 2."""
import numpy as np, math
import scene as S

K = 2
SUN = (92, 70)
S.W, S.H = 108 * K, 192 * K
S.S = 10 // K
S.YY, S.XX = [a.astype(np.float32) + 0.5 for a in np.mgrid[0:S.H, 0:S.W]]
W, H, XX, YY = S.W, S.H, S.XX, S.YY
Cam0 = S.Cam


def background_hd(camx, t):
    F = np.empty((H, W, 3), np.uint8)
    edges = [e * K for e in S.SKY_E]
    for i, e in enumerate(edges):
        e1 = edges[i + 1] if i + 1 < len(edges) else H
        F[e:e1] = S.SKY[i]
        if i + 1 < len(S.SKY):  # 3-row checker dither toward next band
            for y in range(e1 - 3, e1):
                F[y, (np.arange(W) + y) % 2 == 0] = S.SKY[i + 1]
    # sun + dithered glow
    d2 = (XX - SUN[0] * K) ** 2 + (YY - SUN[1] * K) ** 2
    glow = (d2 < (14 * K) ** 2) & (d2 >= (11 * K) ** 2) & (((XX + YY).astype(int) % 2) == 0)
    F[glow] = (250, 226, 170)
    F[d2 < (10.5 * K) ** 2] = (255, 226, 150)
    F[d2 < (9 * K) ** 2] = (255, 240, 196)
    ring = (d2 < (7.5 * K) ** 2) & (d2 > (6.8 * K) ** 2) & (YY < SUN[1] * K)
    F[ring] = (255, 250, 226)
    # clouds
    for bx, by, sz, par in ((20, 22, 1.0, 0.03), (95, 60, 0.8, 0.05), (160, 34, 1.2, 0.02)):
        x = (bx - camx * par - t * 1.2) % (108 + 60) - 30
        L = S.Layer(Cam0(0, 0, K))
        S.ell(L, (x, by), 9 * sz, 2.6 * sz, (246, 244, 236))
        S.ell(L, (x - 4 * sz, by - 1.8 * sz), 4.5 * sz, 2.6 * sz, (246, 244, 236))
        S.ell(L, (x + 3 * sz, by - 2.4 * sz), 5 * sz, 3 * sz, (250, 250, 244))
        L.col[L.m & (YY > (by + 1.2 * sz) * K)] = (212, 214, 224)
        L.col[L.m & (YY > (by + 1.9 * sz) * K)] = (196, 200, 214)
        S.comp(F, L)
    # far mesas
    cols = (np.arange(W) + 0.5) / K
    wx = cols + camx * 0.08
    h = np.zeros(W)
    for c, hw, ht in S.MESAS:
        for rep in (-340, 0, 340, 680):
            h = np.maximum(h, np.clip(ht - np.maximum(0, np.abs(wx - c - rep) - hw) * 1.8, 0, None))
    base = 132 * K
    for x in range(W):
        if h[x] <= 0: continue
        top = int(base - h[x] * K)
        F[top:base, x] = (204, 126, 94)
        F[top:top + 2, x] = (232, 160, 120)
        F[top + 2:top + 4, x] = (222, 146, 108)
        for yy in range(top + 8, base, 10):
            F[yy:yy + 2, x] = (182, 108, 82)
        if (x // 3) % 7 == 0: F[top + 5:base:3, x] = (192, 116, 88)  # vertical erosion streaks
    # mid hills
    wx2 = cols + camx * 0.25
    hh = 5 + 2.5 * np.sin(wx2 * 0.07) + 2 * np.sin(wx2 * 0.023 + 1.3)
    for x in range(W):
        top = int((139 - hh[x]) * K)
        F[top:141 * K, x] = (190, 144, 98)
        F[top:top + 2, x] = (210, 166, 116)
    # mid-ground props (parallax 0.55)
    L = S.Layer(Cam0(0, 0, K))
    off = camx * 0.55
    for k in range(int(off // 26) - 1, int((off + 108) // 26) + 2):
        hv = int(S.hsh(k))
        x = k * 26 + (hv % 17) - off
        if hv % 3 == 0:
            ht = 5 + hv % 4
            S.cap(L, (x, 140), (x, 140 - ht), 1.1, 1.1, (96, 132, 76), hi=(120, 158, 96))
            S.cap(L, (x - 2.2, 137 - ht * 0.3), (x - 2.2, 134 - ht * 0.5), 0.7, 0.7, (96, 132, 76))
        elif hv % 3 == 1:
            S.ell(L, (x, 140), 2.2, 1.3, (150, 120, 96), hi=(176, 148, 120))
    S.outline(L, (120, 96, 70))
    S.comp(F, L)
    # ground bands
    F[141 * K:] = (216, 176, 122)
    F[143 * K:161 * K] = (230, 198, 148)
    F[143 * K:143 * K + 2] = (204, 164, 112)
    F[161 * K:170 * K] = (210, 168, 112)
    F[170 * K:] = (182, 150, 96)
    # ruts & pebbles (fine grid, parallax 1)
    wxi = (np.arange(W) + int(camx * K)).astype(np.int64)
    hv = S.hsh(wxi)
    for y, sal in ((148 * K, 7), (156 * K, 11)):
        m = (S.hsh(wxi // 2 + sal) // sal) % 5 < 3
        F[y, m] = (214, 180, 132)
        F[y + 1, m] = (222, 188, 140)
    peb = hv % 31 == 0
    py = 145 * K + (hv // 31) % (14 * K)
    for x in np.where(peb)[0]:
        if x + 2 < W:
            F[py[x], x:x + 2] = (186, 150, 108)
            F[py[x] - 1, x:x + 2] = (244, 220, 176)
    # grass tufts on near sand
    for x in np.where(hv % 13 == 0)[0]:
        y0 = 162 * K + (hv[x] // 13) % (6 * K)
        F[y0:y0 + 4, x] = (150, 150, 80)
        F[y0 + 1:y0 + 4, max(x - 1, 0)] = (136, 138, 72)
    # foreground scrub (parallax 1.3)
    wxf = (np.arange(W) + int(camx * 1.3 * K)).astype(np.int64)
    hf = S.hsh(wxf // 2 + 9999)
    hf2 = S.hsh(wxf + 777)
    fy = H - 14 * K
    for x in range(W):
        hgt = (3 + int(hf[x] % 6)) * K if hf[x] % 3 == 0 else int(hf[x] % 2) * K
        hgt += int(hf2[x] % 2)
        F[fy - hgt:fy, x] = (120, 124, 60) if hf[x] % 2 else (146, 146, 72)
        F[fy:, x] = (110, 104, 58)
    F[fy + 6, (hf % 11 == 0)] = (170, 164, 90)
    F[fy + 8, (hf2 % 17 == 0)] = (128, 118, 66)
    return F


def draw_particles_hd(F, t, cam_sx):
    L = S.Layer(Cam0(0, 0, K))
    thin1 = ((XX.astype(int) + YY.astype(int)) % 2 == 0)
    thin2 = thin1 | ((XX.astype(int) % 2) == 0)
    for p in S.PART:
        a = t - p['b']
        if a < 0 or a > p['life']: continue
        k = a / p['life']
        x0 = S.HORSE_SX + p['x'] if p['rel'] else p['x']
        x = x0 + p['vx'] * a + cam_sx
        y = p['y'] + p['vy'] * a + 12 * a * a
        r = S.lerp(p['r0'], p['r1'], k)
        S.ell(L, (x, y), r, r * 0.8, (238, 218, 180), hi=(250, 238, 212))
        if k > 0.55:
            L.m &= ~(thin2 if k > 0.8 else thin1) | ~L.m
    S.comp(F, L)


def bubble_hd(F, x, y):
    x, y = int(x), int(y)
    w, h = 10, 16
    x0, y0 = x - w // 2, y - h
    if x0 < 3 or y0 < 3 or x0 + w + 3 >= W: return
    ol = (40, 24, 18)
    F[y0 - 2:y0 + h + 2, x0:x0 + w] = ol
    F[y0:y0 + h, x0 - 2:x0 + w + 2] = ol
    F[y0:y0 + h, x0:x0 + w] = (250, 248, 240)
    F[y0 + 2:y0 + 10, x0 + 4:x0 + 6] = (214, 40, 40)
    F[y0 + 12:y0 + 14, x0 + 4:x0 + 6] = (214, 40, 40)
    F[y0 + h:y0 + h + 4, x0 + 2:x0 + 4] = ol


S.background = background_hd
S.draw_particles = draw_particles_hd
