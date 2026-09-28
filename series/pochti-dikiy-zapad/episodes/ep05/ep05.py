"""S01E05 «Почти поймал». xAI backgrounds (engine/props/frontier.py) + code heroes integrated with scene light
(stage.Light: ambient/fire/sun + rim + contact shadows + hero pixel size matched to zoom) and particles (engine/fx.py).
  python3 ep05.py test 1 5 20   -> build/ep05/sheet.png
  python3 ep05.py all [4]       -> build/ep05/noaudio.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import math, subprocess, os
import numpy as np
from PIL import Image
import stage as ST
from stage import View, view_at, Chars, Light, shadow, ell, wrect, px_text, OUT_W, OUT_H, UP
import scene as S
from scene import Layer, cap, dot, outline, sm, lerp
import overlays as O
import fx
from props import chars as C
from props import frontier as F
from timeline import DUR, FPS, VOICE

EP = 'ep05'
D = F.build()
CAMP, CANYON, TOWN = D['camp'], D['canyon'], D['town']

# ---------------------------------------------------------------- voice envelopes, captions
ENV = {}
for vid, ep, key, t0, a, b, who, txt in VOICE:
    if (ep, key) not in ENV: ENV[(ep, key)] = S.load_env(P.voice_wav(ep, key))

def talk(who, t):
    v = 0.0
    for vid, ep, key, t0, a, b, spk, txt in VOICE:
        if spk == who and t0 <= t < t0 + (b - a):
            e = ENV[(ep, key)]; i = int((a + t - t0) * 100)
            if 0 <= i < len(e): v = max(v, float(e[i]))
    return v

COL = dict(billy=(255, 222, 96), molniya=(255, 255, 255), sam=(214, 170, 255))
_items = []
for vid, ep, key, t0, a, b, who, txt in VOICE:
    ch = O.chunk_words(O.word_times(ENV[(ep, key)], t0, a, b, txt.split()))
    for i, c in enumerate(ch):
        s0 = c[0][1]; e0 = ch[i + 1][0][1] if i + 1 < len(ch) else max(c[-1][2] + 0.35, t0 + (b - a))
        _items.append((s0, e0, [w[0] for w in c], COL[who]))
CAPTIONS = O.Captions(_items)
CAP_Y = 780

# ---------------------------------------------------------------- helpers
def horse_anchor(x, feet, u): return x, feet - 19 * u

def head_of_horse(x, feet, u, Pz, flip=False):
    ax, ay = horse_anchor(x, feet, u)
    hs = S.horse_frames(1000.0, 1000.0, Pz)[3]
    dx = (hs[0] - 1000.0) * u
    return (ax - dx if flip else ax + dx), ay + (hs[1] - 1000.0) * u

def rider_hip_world(x, feet, u, Pz, flip=False):
    ax, ay = horse_anchor(x, feet, u)
    T = S.horse_frames(1000.0, 1000.0, Pz)[0]; h = T(-1.0, -9.4)
    dx = (h[0] - 1000.0) * u
    return (ax - dx if flip else ax + dx), ay + (h[1] - 1000.0) * u

def light_for(scene, v, t):
    if scene == 'camp':
        fx_, fy = v.opt(*F.FIRE)
        fl = 1.0 + 0.12 * math.sin(t * 13) + 0.08 * math.sin(t * 29 + 1)
        near = fx_ > -500
        return Light(amb=(0.56, 0.62, 0.95) if near else (0.66, 0.72, 1.0),
                     keys=[(fx_, fy - 60, 1150 * max(1.0, v.Z * 0.8), (255, 150, 60), 1.0)],
                     rim=(-1, 0, (255, 170, 80), 0.6) if near else (1, -1, (170, 196, 255), 0.55), grad=(1.0, 0.85), flick=fl)
    if scene == 'canyon':
        return Light(amb=(1.06, 0.95, 0.83), rim=(1, -1, (255, 232, 170), 0.5), grad=(1.08, 0.86))
    return Light(amb=(1.06, 0.92, 0.80), rim=(-1, -1, (255, 196, 120), 0.5), grad=(1.06, 0.86))

def frame_fx(scene, big, v, t, FX):
    if scene == 'camp':
        fx_, fy = v.opt(*F.FIRE)
        fx.glow(big, fx_, fy - 40, 520 * v.Z, (255, 140, 50), 0.35 + 0.08 * math.sin(t * 13))
        FX.comp(big)
        fx.vignette(big, 0.45); fx.grade(big, (0.98, 0.98, 1.04), (0, 0, 6))
    elif scene == 'canyon':
        FX.comp(big)
        fx.shafts(big, t, angle=2.3, a=0.05, col=(255, 226, 160), x_off=-v.X0 * v.Z * UP * 0.3)
        fx.vignette(big, 0.3)
    else:
        sx, sy = v.opt(*F.SUN_TOWN)
        fx.glow(big, sx, sy, 700 * v.Z, (255, 180, 90), 0.25)
        FX.comp(big)
        fx.vignette(big, 0.32); fx.grade(big, (1.02, 0.99, 0.95))

def begin(Z):
    ST.set_px(ST.px_for_zoom(Z))
    return Chars(), Chars()

# ---------------------------------------------------------------- CAMP (0 .. 9.6)
U_CAMP = 6.5
BILLY_LIE = (612.0, 594.0)          # hip while lying

def molniya_camp_x(t):
    if t < 2.5: return 905.0
    return lerp(905.0, 772.0, sm((t - 2.5) / 0.6))

def camp_scene(CH, FX, big, v, t):
    fx.flames(FX, v, F.FIRE[0], F.FIRE[1] - 4, t)
    fx.embers(FX, v, F.FIRE[0], F.FIRE[1] - 20, t)
    fx.fireflies(FX, v, t, 150, 330, 1200, 520)
    # Molniya
    mx = molniya_camp_x(t)
    walking = 2.5 <= t < 3.1
    if walking:
        Pz = C.walk_pose(t) if False else S.stand_pose(t)
    Pz = C.molniya_pose(t, False, talk('molniya', t))
    if 4.25 <= t < 4.7: Pz['neck'] = lerp(-0.95, 0.2, math.sin(math.pi * (t - 4.25) / 0.45)); Pz['head'] = 1.2
    shadow(big, v, mx - 10, F.CAMP_FEET, 16 * U_CAMP, 2.2 * U_CAMP)
    ax, ay = horse_anchor(mx, F.CAMP_FEET, U_CAMP)
    C.molniya(CH, v.cam(ax, ay, U_CAMP, True), t, Pz)
    # tin bucket knocked over at 0
    L = Layer(v.wcam())
    u = min(1.0, t / 0.5); bx = 830 + 40 * u; by = F.CAMP_FEET - 12
    ang = u * 1.5
    cap(L, (bx - 9 * math.cos(ang), by - 9 * math.sin(ang) * 0.4), (bx + 9 * math.cos(ang), by + 9 * math.sin(ang) * 0.4), 8, 7, (150, 156, 166), hi=(200, 206, 214))
    outline(L, (40, 34, 40)); CH.add(L)
    # Billy lying / waking
    k = sm((t - 4.4) / 0.25)
    rot = lerp(1.57, 0.12, k)
    hip = (BILLY_LIE[0] - 6 * k, BILLY_LIE[1] - 4 * k)
    pose = C.POSES['stand'] if k < 0.5 else C.POSES['sit']
    shadow(big, v, hip[0] + 30, F.CAMP_FEET, 11 * U_CAMP, 1.8 * U_CAMP)
    expr = 'normal' if t < 4.4 else 'amazed'
    C.billy(CH, v.cam(hip[0], hip[1], U_CAMP), pose, rot, talk('billy', t), expr)
    if 2.5 <= t < 4.4:                                                                          # snore Z's
        for i in range(3):
            u2 = ((t - 2.5) * 0.8 + i / 3) % 1.0
            sx, sy = v.pt(hip[0] + 60 + 30 * u2, hip[1] - 20 - 80 * u2)
            px_text(FX, 'Z', sx, sy, 16 if ST.PX[0] == 1 else 8, (220, 230, 255))
    if 4.4 <= t < 5.0:
        sx, sy = v.pt(hip[0] + 10, hip[1] - 150)
        px_text(FX, '!', sx, sy, 16, (255, 230, 90))
    fx.dust_puffs(FX, v, t, [(4.4, hip[0] + 20, F.CAMP_FEET, 16)])

def render_camp(name, t, u):
    if name == 'cu_mol_trough':
        hx, hy = head_of_horse(molniya_camp_x(t), F.CAMP_FEET, U_CAMP, C.molniya_pose(t), True)
        v = view_at(CAMP, hx - 40, hy + 40, 2.6 - 0.1 * u, 180, 330)
    elif name == 'wide_camp':
        v = View(CAMP, 400 + 20 * u, 260, 1.0 + 0.04 * u)
    elif name == 'cu_billy_camp':
        v = view_at(CAMP, BILLY_LIE[0] + 6, BILLY_LIE[1] - 9.7 * U_CAMP, 3.0 + 0.08 * u, 180, 430)
    else:  # cu_mol_camp
        hx, hy = head_of_horse(molniya_camp_x(t), F.CAMP_FEET, U_CAMP, C.molniya_pose(t), True)
        v = view_at(CAMP, hx - 12, hy + 10, 2.9 + 0.1 * u, 180, 430)
    CH, FX = begin(v.Z)
    big = v.bg()
    camp_scene(CH, FX, big, v, t)
    CH.comp(big, light_for('camp', v, t))
    frame_fx('camp', big, v, t, FX)
    return big

# ---------------------------------------------------------------- CANYON (9.6 .. 21.5)
U_C = 5.0
T_CATCH = 14.95

def sam_x(t): return 380 + 120 * (t - 9.6)
def mol_x(t):
    if t < T_CATCH: return 60 + 170 * (t - 9.6)
    x0 = 60 + 170 * (T_CATCH - 9.6)
    return x0 + 60 * sm((t - T_CATCH) / 0.6)
def sam_ground(t):
    """Sam after the lasso yank: flies back and lands"""
    x0 = sam_x(T_CATCH); x1 = mol_x(T_CATCH) + 150
    k = min(1.0, (t - T_CATCH) / 0.4)
    return lerp(x0, x1, k), F.CANYON_FEET - 2.5 * U_C - 60 * math.sin(math.pi * k) * (1 - k * 0.3)

def canyon_scene(CH, FX, big, v, t, only=None):
    # dust
    fx.dust_puffs(FX, v, t, fx.gallop_dust(t, mol_x, F.CANYON_FEET, max(9.6, t - 0.8), min(t, T_CATCH + 0.3), 8, 10) +
                  fx.gallop_dust(t, sam_x, F.CANYON_FEET, max(9.6, t - 0.8), t, 5, 7) +
                  [(T_CATCH + 0.4, sam_ground(T_CATCH + 0.4)[0], F.CANYON_FEET, 20)])
    fx.motes(FX, v, t, 500, 120, 1100, 560, n=50, seed=3)
    # Sam + donkey
    if only in (None, 'sam'):
        dx = sam_x(t)
        shadow(big, v, dx, F.CANYON_FEET, 13 * U_C * 0.8, 1.6 * U_C)
        du = U_C * 0.85
        rider = C.rider_sam(dict(C.POSES['ride'], _t=t), talk('sam', t)) if t < T_CATCH else None
        C.donkey(CH, v.cam(dx, F.CANYON_FEET - 19 * du, du), t, moving=True, rider=rider, speed=2.4)
        if t >= T_CATCH:
            sx, sy = sam_ground(t)
            L = Layer(v.cam(sx, sy, U_C, True))
            pose = C.POSES['sit']
            with_bandit = lambda: S.cowboy(L, (1000.0, 1000.0), -0.2 + 0.2 * min(1, (t - T_CATCH) / 0.4), pose, hat_on=True,
                                           mouth=talk('sam', t))
            C.with_pal(S.CC, C.CC_BANDIT, with_bandit)
            HP = C.HPf(-0.2)
            cap(L, HP(-1.2, 10.3), HP(2.7, 10.3), 0.78, 0.78, (24, 20, 24)); dot(L, HP(1.9, 10.3), (240, 240, 240), 0.32)
            cap(L, HP(1.3, 8.45), HP(3.4, 7.25), 0.6, 0.4, (34, 26, 24))
            for yy in (3.0, 4.6):                                                                     # lasso around him
                cap(L, HP(-2.6, yy), HP(2.8, yy + 0.2), 0.35, 0.35, (196, 150, 90))
            outline(L, (20, 14, 14)); CH.add(L)
    # Molniya + Billy (lasso)
    if only in (None, 'mol'):
        mx = mol_x(t)
        running = t < T_CATCH + 0.5
        Pz, ph = C.gallop(t) if running else (C.molniya_pose(t, False, talk('molniya', t)), 0.0)
        shadow(big, v, mx, F.CANYON_FEET, 16 * U_C, 1.8 * U_C)
        swing = 12.2 <= t < T_CATCH
        pose = C.POSES['heroic'] if swing else C.POSES['ride']
        ax, ay = horse_anchor(mx, F.CANYON_FEET, U_C)
        def rider(L, T):
            C.rider_billy(pose, talk('billy', t))(L, T)
            if swing and t < 14.6:
                h = T(-1.0, -9.4)
                C.lasso_loop(L, (h[0] + 1.0, h[1] - 16.5), 3.2, t)
        C.molniya(CH, v.cam(ax, ay, U_C), t, Pz, rider=rider, p=ph)
        if 14.6 <= t < 16.2:                                                                           # rope to Sam
            hx, hy = rider_hip_world(mx, F.CANYON_FEET, U_C, Pz)
            hand = (hx + 1.5 * U_C, hy - 14 * U_C)
            if t < T_CATCH:
                k = (t - 14.6) / (T_CATCH - 14.6); tgt = (lerp(hand[0], sam_x(t), k), lerp(hand[1], F.CANYON_FEET - 16 * U_C, k))
            else:
                sx, sy = sam_ground(t); tgt = (sx, sy - 4 * U_C)
            L = Layer(v.wcam())
            n = 8
            for i in range(n):
                a0, a1 = i / n, (i + 1) / n
                sag = 14 if t >= T_CATCH else -20
                p0 = (lerp(hand[0], tgt[0], a0), lerp(hand[1], tgt[1], a0) + sag * math.sin(math.pi * a0))
                p1 = (lerp(hand[0], tgt[0], a1), lerp(hand[1], tgt[1], a1) + sag * math.sin(math.pi * a1))
                cap(L, p0, p1, 1.4, 1.4, (196, 150, 90))
            outline(L, (70, 46, 24)); CH.add(L)

def render_canyon(name, t, u):
    if name == 'split_chase':
        vt = view_at(CANYON, sam_x(t) + 20, F.CANYON_FEET - 60, 1.7, 180, 200, hlog=320)
        vb = view_at(CANYON, mol_x(t) + 20, F.CANYON_FEET - 70, 1.7, 180, 200, hlog=320)
        out = []
        for v, who in ((vt, 'sam'), (vb, 'mol')):
            CH, FX = begin(v.Z)
            b = v.bg(); canyon_scene(CH, FX, b, v, t, only=who)
            CH.comp(b, light_for('canyon', v, t)); frame_fx('canyon', b, v, t, FX)
            fx.speed_lines(b, t, 0.6)
            out.append(b[:960])
        big = np.concatenate(out, 0); big[954:966] = (30, 18, 12)
        return big
    if name == 'wide_canyon':
        cx = (mol_x(t) + sam_x(t)) / 2
        v = view_at(CANYON, cx + 30, 560, 1.05, 180, 400)
    elif name == 'cu_billy_lasso':
        hx, hy = rider_hip_world(mol_x(t), F.CANYON_FEET, U_C, C.gallop(t)[0])
        v = view_at(CANYON, hx + 12, hy - 10 * U_C, 2.4, 180, 470)
    elif name == 'catch':
        cx = (mol_x(t) + sam_x(min(t, T_CATCH))) / 2
        v = view_at(CANYON, cx + 40, 580, 1.05, 180, 420)
    elif name == 'cu_sam_ground':
        sx, sy = sam_ground(t)
        v = view_at(CANYON, sx - 6, sy - 9.7 * U_C, 2.8 + 0.08 * u, 150, 380)
    else:  # cu_mol_canyon
        hx, hy = head_of_horse(mol_x(t), F.CANYON_FEET, U_C, C.molniya_pose(t))
        v = view_at(CANYON, hx + 14, hy + 8, 2.9 + 0.08 * u, 180, 430)
    CH, FX = begin(v.Z)
    big = v.bg()
    canyon_scene(CH, FX, big, v, t)
    CH.comp(big, light_for('canyon', v, t))
    frame_fx('canyon', big, v, t, FX)
    if name in ('wide_canyon', 'cu_billy_lasso'): fx.speed_lines(big, t, 1.0)
    return big

# ---------------------------------------------------------------- TOWN (21.5 .. 45)
U_T, U_TH = 7.5, 6.3
BILLY_T = 548.0
MOL_T = 815.0
TRIPOD = 468.0
T_FREE = 31.6

def sam_town(t):
    """Sam: tied at the post -> sneaks off -> rides away on the donkey"""
    if t < 32.3: return F.POST_X, 'tied'
    if t < 33.3: return lerp(F.POST_X, 760, (t - 32.3)), 'sneak'
    return 880 + 110 * (t - 33.3), 'ride'

def tripod_camera(CH, v, t, flash_k=0.0):
    L = Layer(v.wcam())
    x, feet = TRIPOD, F.TOWN_FEET
    for dx in (-22, 0, 22): cap(L, (x, feet - 110), (x + dx, feet), 2.2, 2.2, (110, 76, 44))
    wrect(L, x - 26, feet - 150, x + 26, feet - 108, (40, 30, 28)); wrect(L, x + 26, feet - 146, x + 44, feet - 112, (120, 60, 40))
    for i in range(4): wrect(L, x + 28 + i * 4, feet - 146, x + 30 + i * 4, feet - 112, (90, 40, 30))
    ell(L, (x + 50, feet - 129), 9, 9, (70, 60, 60)); ell(L, (x + 50, feet - 129), 5, 5, (170, 200, 220))
    cap(L, (x - 10, feet - 150), (x - 10, feet - 170), 2, 2, (60, 50, 44)); wrect(L, x - 24, feet - 176, x + 4, feet - 168, (200, 190, 170))
    outline(L, (30, 20, 16)); CH.add(L)

def town_scene(CH, FX, big, v, t, parts=('billy', 'sam', 'mol', 'tripod')):
    fx.motes(FX, v, t, 0, 200, 1280, 640, n=40, col=(255, 226, 170), seed=9)
    if 'tripod' in parts: tripod_camera(CH, v, t)
    # Sam
    sx, st = sam_town(t)
    if 'sam' in parts:
        if st == 'ride':
            du = U_TH * 0.62
            C.donkey(CH, v.cam(sx, F.TOWN_FEET - 40 - 19 * du, du), t, moving=True, speed=2.0,
                     rider=C.rider_sam(dict(C.POSES['ride'], _t=t), talk('sam', t), wave=True))
        else:
            feet = F.POST_BASE + 14
            shadow(big, v, sx, feet, 5 * U_T, 1.2 * U_T)
            pose = C.POSES['stand'] if st == 'tied' else C.walk_pose(t * 0.7, 9, 0.3)
            if 29.5 <= t < 30.2: pose = dict(pose, farm=(1.4, 1.6))                             # slips the carrots
            C.sam(CH, v.cam(sx, feet - C.HIP_H * U_T, U_T, st == 'tied' and t < 29.3), pose, mouth=talk('sam', t),
                  look_cam=st == 'sneak')
            if st == 'tied' and t < T_FREE:
                L = Layer(v.cam(sx, feet - C.HIP_H * U_T, U_T))
                for yy in (2.2, 3.8, 5.4): cap(L, (996.4, 1000 - yy), (1003.6, 1000 - yy - 0.3), 0.4, 0.4, (196, 150, 90))
                outline(L, (70, 46, 24)); CH.add(L)
    if t >= T_FREE and 'sam' in parts:                                                                   # bitten rope on the ground
        L = Layer(v.wcam())
        for i in range(4): cap(L, (F.POST_X - 30 + i * 14, F.POST_BASE + 10 + (i % 2) * 3), (F.POST_X - 20 + i * 14, F.POST_BASE + 12), 2.2, 2.2, (196, 150, 90))
        CH.add(L)
    # Molniya
    if 'mol' in parts:
        chew = t >= 30.3
        Pz = C.molniya_pose(t, chew, talk('molniya', t))
        if 31.0 <= t < 31.6: Pz['neck'] = -0.5; Pz['head'] = 1.1                                     # bites the rope
        shadow(big, v, MOL_T - 10, F.TOWN_FEET, 16 * U_TH, 2 * U_TH)
        ax, ay = horse_anchor(MOL_T, F.TOWN_FEET, U_TH)
        C.molniya(CH, v.cam(ax, ay, U_TH, True), t, Pz, carrot=t >= 30.2, carrots=2)
    # Billy
    if 'billy' in parts:
        if t < 24.8: pose, flip, expr, bx = C.POSES['excited'], False, 'excited', BILLY_T
        elif t < 29.3: pose, flip, expr, bx = C.POSES['hips'], True, 'sly', BILLY_T - 10
        elif t < 33.3:
            i = min(2, int((t - 29.3) / 1.2))
            pose = (C.POSES['heroic'], C.POSES['hips'], C.POSES['point'])[i]; flip, expr, bx = True, 'sly', BILLY_T - 10
        else: pose, flip, expr, bx = C.POSES['stand'], False, 'amazed', BILLY_T + 60
        shadow(big, v, bx, F.TOWN_FEET, 5 * U_T, 1.2 * U_T)
        C.billy(CH, v.cam(bx, F.TOWN_FEET - C.HIP_H * U_T, U_T, flip), pose, 0.05, talk('billy', t), expr)

FLASHES = [29.8, 31.0, 32.2, 40.0]

def render_town(name, t, u):
    if name == 'wide_town':
        v = View(TOWN, 450 + 10 * u, 180, 0.95 + 0.03 * u)
    elif name == 'board':
        v = view_at(TOWN, (F.BOARD[0] + F.BOARD[2]) / 2, (F.BOARD[1] + F.BOARD[3]) / 2, 4.0 + 0.2 * u, 180, 360)
    elif name == 'billy_camera':
        v = view_at(TOWN, 520, 520, 1.7, 180, 420)
    elif name == 'cu_billy_town':
        v = view_at(TOWN, BILLY_T - 4, F.TOWN_FEET - (C.HIP_H + 9.7) * U_T, 2.8 + 0.1 * u, 180, 440)
    elif name == 'split_pose':
        vt = view_at(TOWN, BILLY_T - 10, F.TOWN_FEET - (C.HIP_H + 3) * U_T, 1.45, 180, 170, hlog=320)
        vb = view_at(TOWN, 730, 500, 1.6, 180, 190, hlog=320)
        out = []
        for v, parts in ((vt, ('billy', 'tripod')), (vb, ('sam', 'mol'))):
            CH, FX = begin(v.Z); b = v.bg()
            town_scene(CH, FX, b, v, t, parts)
            CH.comp(b, light_for('town', v, t)); frame_fx('town', b, v, t, FX)
            out.append(b[:960])
        big = np.concatenate(out, 0); big[954:966] = (30, 18, 12)
        for fa in FLASHES:
            if fa <= t < fa + 0.25: fx.flash_burst(big[:960], 300, 400, 1 - (t - fa) / 0.25)
        return big
    elif name == 'wide_town_empty':
        v = View(TOWN, 600 + 60 * u, 180, 0.92)
    elif name == 'billy_mol':
        v = view_at(TOWN, 700, 520, 1.45 + 0.03 * u, 180, 420)
    elif name == 'cu_mol_town':
        hx, hy = head_of_horse(MOL_T, F.TOWN_FEET, U_TH, C.molniya_pose(t), True)
        v = view_at(TOWN, hx - 10, hy + 8, 3.0 + 0.1 * u, 180, 430)
    elif name == 'photo':
        return photo(t, u)
    CH, FX = begin(v.Z)
    big = v.bg()
    town_scene(CH, FX, big, v, t)
    CH.comp(big, light_for('town', v, t))
    frame_fx('town', big, v, t, FX)
    return big

_PHOTO = []
def photo(t, u):
    """sepia «ЛУЧШИЙ КОВБОЙ» poster: Billy posing, Sam waving goodbye in the background"""
    if not _PHOTO:
        v = view_at(TOWN, 650, 500, 0.95, 180, 400)
        CH, FX = begin(v.Z); b = v.bg()
        C.donkey(CH, v.cam(596, F.TOWN_FEET - 100 - 19 * 2.6, 2.6), 33.0, moving=True,
                 rider=C.rider_sam(dict(C.POSES['ride'], _t=0.3), 0.0, wave=True))
        tripod = None
        town_scene(CH, FX, b, v, 32.0, ('billy', 'mol'))
        L = Layer(v.wcam())
        for i in range(4): cap(L, (F.POST_X - 30 + i * 14, F.POST_BASE + 10 + (i % 2) * 3), (F.POST_X - 20 + i * 14, F.POST_BASE + 12), 2.2, 2.2, (196, 150, 90))
        CH.add(L)
        CH.comp(b, light_for('town', v, 32.0))
        g = (b[..., 0] * 0.3 + b[..., 1] * 0.59 + b[..., 2] * 0.11)[..., None]
        sep = np.clip(g * np.array([1.08, 0.9, 0.66]) + np.array([24, 12, 0]), 0, 255)
        sep = np.floor(sep / 24) * 24
        img = np.full((OUT_H, OUT_W, 3), (238, 224, 188), np.uint8)
        m = 60
        img[m:OUT_H - m, m:OUT_W - m] = np.array(Image.fromarray(sep.astype(np.uint8)).resize((OUT_W - 2 * m, OUT_H - 2 * m), Image.NEAREST))
        img[m - 8:m, m - 8:OUT_W - m + 8] = (90, 60, 40); img[OUT_H - m:OUT_H - m + 8, m - 8:OUT_W - m + 8] = (90, 60, 40)
        img[m - 8:OUT_H - m + 8, m - 8:m] = (90, 60, 40); img[m - 8:OUT_H - m + 8, OUT_W - m:OUT_W - m + 8] = (90, 60, 40)
        title = O.pixel_title(['ЛУЧШИЙ', 'КОВБОЙ'], 64)
        O.overlay(img, title, 0, 150, 1.0)
        _PHOTO.append(img)
    img = _PHOTO[0]
    s = 1.0 + 0.05 * sm(u / 3.0)
    h, w = int(OUT_H / s), int(OUT_W / s)
    y0, x0 = (OUT_H - h) // 2, (OUT_W - w) // 2
    return np.array(Image.fromarray(img[y0:y0 + h, x0:x0 + w]).resize((OUT_W, OUT_H), Image.NEAREST))

# ---------------------------------------------------------------- shots
SHOTS = [
    (0.00, 2.50, 'camp', 'cu_mol_trough'), (2.50, 4.80, 'camp', 'wide_camp'), (4.80, 7.20, 'camp', 'cu_billy_camp'),
    (7.20, 9.60, 'camp', 'cu_mol_camp'),
    (9.60, 11.40, 'canyon', 'split_chase'), (11.40, 13.00, 'canyon', 'wide_canyon'), (13.00, 14.60, 'canyon', 'cu_billy_lasso'),
    (14.60, 16.20, 'canyon', 'catch'), (16.20, 18.80, 'canyon', 'cu_sam_ground'), (18.80, 21.50, 'canyon', 'cu_mol_canyon'),
    (21.50, 23.40, 'town', 'wide_town'), (23.40, 24.80, 'town', 'board'), (24.80, 26.80, 'town', 'billy_camera'),
    (26.80, 29.30, 'town', 'cu_billy_town'), (29.30, 33.30, 'town', 'split_pose'), (33.30, 35.60, 'town', 'wide_town_empty'),
    (35.60, 38.40, 'town', 'billy_mol'), (38.40, 40.00, 'town', 'cu_mol_town'), (40.00, 43.30, 'town', 'photo'),
    (43.30, DUR + 1, 'town', 'cu_mol_town'),
]
FLASH_AT = [0.0, 9.6, 21.5]

def shot_at(t):
    for a, b, sc, n in SHOTS:
        if a <= t < b: return a, b, sc, n
    return SHOTS[-1]

def render_scene(t):
    a, b, sc, name = shot_at(t); u = t - a
    return {'camp': render_camp, 'canyon': render_canyon, 'town': render_town}[sc](name, t, u)

# ---------------------------------------------------------------- overlays
BADGE = O.make_badge('СЕЗОН 1 • СЕРИЯ 5/6')
HOOK = O.pixel_title(['ПЛАТЁЖ', 'ПРОСРОЧЕН'], 64)
TEASE = O.pixel_title(['СЕРИЯ 6 — ФИНАЛ'], 40)

def carrot_icon(n=2, s=6):
    c = np.zeros((16 * s, (12 * n + 4) * s, 4), np.uint8)
    for k in range(n):
        x0 = k * 12 * s
        for i in range(10):
            w = max(1, 5 - i // 2)
            c[(4 + i) * s:(5 + i) * s, x0 + (6 - w // 2) * s:x0 + (6 + w - w // 2) * s] = (236, 128, 40, 255)
        c[0:4 * s, x0 + 5 * s:x0 + 7 * s] = (84, 160, 60, 255); c[s:3 * s, x0 + 3 * s:x0 + 9 * s] = (84, 160, 60, 255)
    return c

STICKERS = [
    (O.sticker('ПРОСРОЧЕНО', fg=(255, 110, 90), size=56), 2.45, 3.9, 540, 560),
    (O.sticker('$500', size=88), 22.0, 23.35, 540, 560),
    (O.sticker('×2', icon=carrot_icon(2, 6)), 29.9, 31.3, 760, 1250),
]

def render(t):
    big = render_scene(t)
    for img, a, b, cx, cy in STICKERS: O.draw_sticker(big, img, t, a, b, cx, cy)
    O.overlay(big, BADGE, 36, 96, 1.0)
    if 0.2 <= t < 2.3:
        k = min(1.0, (t - 0.2) / 0.1) * (1 - sm((t - 2.1) / 0.2))
        O.overlay(big, HOOK, 0, 220, k)
    CAPTIONS.draw(big, t, CAP_Y if not (29.3 <= t < 33.3) else 900)
    if t >= 44.0: O.overlay(big, TEASE, 0, 1540, min(1.0, (t - 44.0) / 0.15))
    for fa in FLASH_AT:
        if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
    if 40.0 <= t < 40.3: fx.flash_burst(big, 540, 900, 1 - (t - 40.0) / 0.3)
    if 21.5 <= t < 21.8: O.mosaic(big, int(lerp(44, 1, (t - 21.5) / 0.3)))
    return big


def cover_frame():
    p = P.episode(EP) / 'cover.png'
    return np.array(Image.open(p).convert('RGB').resize((OUT_W, OUT_H))) if p.exists() else None


def encode(a0, a1, out):
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{OUT_W}x{OUT_H}', '-r', str(FPS),
                             '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', out], stdin=subprocess.PIPE)
    cov = cover_frame()
    for i in range(a0, a1):
        fr = cov if (i < 6 and cov is not None) else render(i / FPS)
        proc.stdin.write(fr.tobytes())
    proc.stdin.close(); proc.wait()


if __name__ == '__main__':
    n = int(round(DUR * FPS))
    if sys.argv[1] == 'test':
        ts = list(map(float, sys.argv[2:]))
        c = Image.new('RGB', (270 * len(ts), 480))
        for k, tt in enumerate(ts):
            c.paste(Image.fromarray(render(tt)).resize((270, 480), Image.LANCZOS), (k * 270, 0))
        c.save(P.build(EP, 'sheet.png')); print(P.build(EP, 'sheet.png'))
    elif sys.argv[1] == 'frame':
        Image.fromarray(render(float(sys.argv[2]))).save(P.build(EP, 'frame.png')); print(P.build(EP, 'frame.png'))
    elif sys.argv[1] == 'seg':
        a0, a1 = int(sys.argv[2]), min(int(sys.argv[3]), n)
        encode(a0, a1, P.build(EP, f'seg_{a0:04d}.mp4')); print('done', a0, a1)
    elif sys.argv[1] == 'all':
        k = int(sys.argv[2]) if len(sys.argv) > 2 else 4
        cuts = [round(n * i / k) for i in range(k + 1)]
        procs = [subprocess.Popen([sys.executable, __file__, 'seg', str(cuts[i]), str(cuts[i + 1])]) for i in range(k)]
        for p_ in procs: p_.wait()
        lst = P.build(EP, 'segs.txt')
        with open(lst, 'w') as f:
            for i in range(k): f.write(f"file '{P.build(EP, f'seg_{cuts[i]:04d}.mp4')}'\n")
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', P.build(EP, 'noaudio.mp4')], check=True)
        print('ok', P.build(EP, 'noaudio.mp4'))
