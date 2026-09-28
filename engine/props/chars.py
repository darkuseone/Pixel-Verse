"""Reusable heroes of «Почти Дикий Запад» on the stage (engine/stage.py). All draw functions take a Chars canvas and
an ACam (stage.View.cam(...)) and add an outlined layer. Mouth/jaw values come from the episode's talk()."""
import math
import scene as S
from scene import Layer, cap, dot, outline, lerp, sm
from stage import ell, wrect

CC_BANDIT = dict(hat=(46, 40, 48), hat_h=(76, 68, 80), band=(190, 50, 50), shirt=(96, 70, 128), shirt_h=(124, 96, 158),
                 shirt_sh=(70, 50, 96), vest=(40, 34, 36), jeans=(90, 80, 70), jeans_sh=(66, 58, 50), bandana=(196, 52, 52),
                 mst=(34, 26, 24), skin=(226, 176, 136))
DONKEY = dict(body=(150, 144, 140), hi=(182, 176, 170), sh=(114, 108, 106), far=(118, 112, 110), farsh=(92, 88, 86),
              mane=(70, 64, 64), maneh=(100, 94, 92), muz=(214, 208, 198), white=(236, 232, 224),
              blanket=(176, 128, 60), blanket_h=(206, 160, 84))
HIP_H = 8.9          # standing hip height above the feet, in units


def with_pal(d, pal, fn):
    old = {k: d[k] for k in pal}; d.update(pal)
    try: return fn()
    finally: d.update(old)


def HPf(rot, hip=(1000.0, 1000.0)):
    u = (math.sin(rot), -math.cos(rot)); f = (math.cos(rot), math.sin(rot))
    return lambda a, b: (hip[0] + f[0] * a + u[0] * b, hip[1] + f[1] * a + u[1] * b)


POSES = dict(
    stand=dict(nleg=(0.08, 0.0), fleg=(-0.08, 0.0), narm=(0.15, 0.1), farm=(-0.1, 0.0)),
    shout=dict(nleg=(0.3, 0.0), fleg=(-0.3, 0.0), narm=(2.1, 2.6), farm=(-1.9, -2.4)),
    angry=dict(nleg=(0.3, 0.0), fleg=(-0.3, 0.0), narm=(1.55, 1.7), farm=(0.9, -0.6)),
    hips=dict(nleg=(0.25, 0.0), fleg=(-0.25, 0.0), narm=(0.9, -0.6), farm=(-0.6, 0.6)),
    lean=dict(nleg=(0.1, 0.0), fleg=(-0.2, 0.0), narm=(1.0, 1.5), farm=(0.4, 0.4)),
    point=dict(nleg=(0.1, 0.0), fleg=(-0.2, 0.0), narm=(1.55, 1.55), farm=(-0.1, 0.0)),
    heroic=dict(nleg=(0.35, 0.0), fleg=(-0.35, 0.0), narm=(2.7, 2.9), farm=(0.2, -0.3)),
    excited=dict(nleg=(0.1, 0.0), fleg=(-0.1, 0.0), narm=(1.9, 2.6), farm=(1.8, 2.5)),
    counter=dict(nleg=(0.05, 0.0), fleg=(-0.05, 0.0), narm=(1.2, 1.6), farm=(1.0, 1.5)),     # hands on a counter
    present=dict(nleg=(0.05, 0.0), fleg=(-0.05, 0.0), narm=(1.9, 1.9), farm=(1.0, 1.5)),     # «прошу!» gesture
    sit=dict(nleg=(1.45, 0.25), fleg=(1.35, 0.3), narm=(0.9, 1.9), farm=(0.6, 1.2)),
    ride=dict(nleg=(1.35, 0.15), fleg=(1.3, 0.2), narm=(0.9, 1.7), farm=(0.8, 1.6)),
    ride_whip=dict(nleg=(1.35, 0.15), fleg=(1.3, 0.2), narm=(2.6, 2.9), farm=(0.8, 1.6)),
)


def walk_pose(t, speed=9.0, amp=0.45):
    s = math.sin(t * speed)
    return dict(nleg=(amp * s, 0.2 * max(0, -s)), fleg=(-amp * s, 0.2 * max(0, s)), narm=(-amp * 0.9 * s, -0.2), farm=(amp * 0.9 * s, -0.2))


def stomp_pose(t):
    p = walk_pose(t, 11, 0.55); p['narm'] = (1.2 + 0.2 * math.sin(t * 11), 1.6); p['farm'] = (1.0, 1.4); return p


def blend_pose(a, b, k):
    return {kk: (lerp(a[kk][0], b[kk][0], k), lerp(a[kk][1], b[kk][1], k)) for kk in a}


# ---------------------------------------------------------------- Billy (hatless: the hat is on Molniya since the pilot)
def billy(CH, cam, pose, rot=0.05, mouth=0.0, expr='normal', red=0.0):
    L = Layer(cam)
    S.CC['mst'] = (96, 60, 36)
    skin0 = S.CC['skin']
    if red > 0: S.CC['skin'] = tuple(int(lerp(a, b, red)) for a, b in zip(skin0, (232, 96, 80)))
    S.cowboy(L, (1000.0, 1000.0), rot, pose, hat_on=False, mouth=mouth)
    S.CC['skin'] = skin0
    HP = HPf(rot)
    ell(L, HP(0.4, 11.4), 2.9, 1.5, (104, 66, 40), rot, hi=(136, 90, 56))
    for dx in (-1.5, -0.3, 0.9):
        cap(L, HP(dx, 11.9), HP(dx + 0.9, 12.9), 0.55, 0.2, (104, 66, 40))
    if cam.sc > 9:
        ew = 0.78 if expr in ('excited', 'shout', 'amazed') else 0.6
        ell(L, HP(1.75, 10.35), ew * 0.85, ew, (250, 250, 244), rot)
        dot(L, HP(1.95, 10.3), (30, 20, 16), 0.32 if expr not in ('excited', 'amazed') else 0.26)
        dot(L, HP(2.05, 10.5), (255, 255, 255), 0.1)
        by = {'excited': 11.55, 'amazed': 11.7, 'shout': 11.3, 'angry': 10.95, 'sly': 11.0, 'normal': 11.2}.get(expr, 11.2)
        tilt = {'sly': -0.35, 'angry': -0.6}.get(expr, 0.15)
        cap(L, HP(1.1, by - tilt * 0.3), HP(2.5, by + tilt * 0.3), 0.2, 0.18, (96, 60, 36))
        ell(L, HP(1.2, 9.05), 0.55, 0.4, (236, 150, 130), rot)
    if mouth > 0.25 or expr in ('shout', 'angry'):
        m = max(mouth, 0.5 if expr in ('shout', 'angry') else 0)
        ell(L, HP(2.2, 7.9), 0.45 + 0.35 * m, 0.25 + 0.55 * m, (90, 24, 24), rot)
    cap(L, HP(1.4, 8.55), HP(3.1, 8.45), 0.55, 0.45, (96, 60, 36))
    if red > 0.6:                                                                             # steam puffs
        for k, dx in enumerate((-1.8, 1.2)):
            ell(L, HP(dx, 13.2 + 0.6 * k), 0.9, 0.7, (240, 240, 236))
    outline(L, (26, 16, 12)); CH.add(L)


# ---------------------------------------------------------------- Sam (bandit mask; optional clerk disguise = big glasses)
def sam(CH, cam, pose, rot=0.03, mouth=0.0, glasses=False, look_cam=False, sweat=False):
    L = Layer(cam)
    with_pal(S.CC, CC_BANDIT, lambda: S.cowboy(L, (1000.0, 1000.0), rot, pose, hat_on=True, mouth=mouth))
    HP = HPf(rot)
    cap(L, HP(-1.2, 10.3), HP(2.7, 10.3), 0.78, 0.78, (24, 20, 24))
    ex = 1.9 if not look_cam else 1.6
    dot(L, HP(ex, 10.3), (240, 240, 240), 0.32)
    if cam.sc > 9: dot(L, HP(ex + (0.12 if not look_cam else -0.05), 10.3), (20, 14, 14), 0.14)
    if glasses:                                                                              # «я не Сэм» glasses over the mask
        for gx in (1.1, 2.6):
            ell(L, HP(gx, 10.3), 0.8, 0.8, (60, 44, 30)); ell(L, HP(gx, 10.3), 0.6, 0.6, (200, 230, 240))
            dot(L, HP(gx + 0.15, 10.5), (255, 255, 255), 0.12)
        dot(L, HP(ex, 10.3), (20, 14, 14), 0.2)
        cap(L, HP(1.8, 10.35), HP(1.9, 10.35), 0.12, 0.12, (60, 44, 30))
    cap(L, HP(1.3, 8.45), HP(3.4, 7.25), 0.6, 0.4, (34, 26, 24))
    if mouth > 0.25: ell(L, HP(2.1, 7.7), 0.35 + 0.3 * mouth, 0.2 + 0.45 * mouth, (90, 24, 24), rot)
    if sweat: ell(L, HP(-0.6, 11.3), 0.35, 0.55, (170, 220, 255))
    outline(L, (20, 14, 14)); CH.add(L)
    return HP


# ---------------------------------------------------------------- Molniya (Billy's hat; optional disguise)
def molniya_pose(t, chew=False, jaw_talk=0.0, moving=False):
    Pz = S.stand_pose(t)
    Pz.update(lid=0.55, ear=0.3 + 0.08 * math.sin(t * 1.1), neck=-0.95, head=0.78)
    c = 0.2 * (1 + math.sin(2 * math.pi * 2.3 * t)) if chew else 0.0
    Pz['jaw'] = max(c, min(jaw_talk * 1.6, 1.0) * 0.8)
    return Pz


def molniya(CH, cam, t, Pz=None, carrot=False, disguise=0.0, stache_drop=None, rider=None):
    """disguise: 0 none, 1 = sunglasses + fake mustache. stache_drop: seconds since the mustache fell (None = on face).
    rider: callable(L, T) drawing a rider on the saddle (same layer, same units)."""
    L = Layer(cam)
    Pz = Pz or molniya_pose(t)
    T, hs, hd_, up = S.draw_horse(L, 1000.0, 1000.0, Pz, t, 0.0, saddle=True)
    pos, rot = S.head_hat_anchor(1000.0, 1000.0, Pz); S.hat(L, pos, rot)
    he = (hs[0] + hd_[0] * 8.5, hs[1] + hd_[1] * 8.5); dn = (-hd_[1], hd_[0])
    if carrot:
        c0 = (he[0] + dn[0] * 1.4 - hd_[0] * 0.6, he[1] + dn[1] * 1.4 - hd_[1] * 0.6)
        cap(L, c0, (c0[0] + 4.2, c0[1] + 0.9), 1.1, 0.4, (236, 128, 40), hi=(255, 176, 90))
        for a in (-0.5, 0.0, 0.5): cap(L, c0, (c0[0] - 1.8, c0[1] - 1.1 - a), 0.4, 0.22, (84, 160, 60))
    S.draw_ears(L, hs, hd_, up, Pz['ear'])
    ec = (hs[0] + hd_[0] * 2.0 + up[0] * 1.0, hs[1] + hd_[1] * 2.0 + up[1] * 1.0)
    if cam.sc > 9 and disguise < 0.5:
        ell(L, ec, 0.95, 0.95, (30, 18, 14)); ell(L, (ec[0] - 0.15, ec[1] + 0.2), 0.55, 0.55, (70, 44, 30))
        dot(L, (ec[0] - 0.35, ec[1] + 0.3), (255, 255, 255), 0.15)
        ell(L, (ec[0], ec[1] - 0.35), 1.15, 0.75, S.HC['body'])
        cap(L, (ec[0] - 1.05, ec[1] - 0.1), (ec[0] + 1.05, ec[1] - 0.1), 0.12, 0.12, (40, 22, 14))
    if disguise >= 0.5:
        ell(L, ec, 1.5, 1.05, (20, 20, 26)); dot(L, (ec[0] + 0.5, ec[1] - 0.35), (150, 170, 200), 0.25)
        cap(L, (ec[0] - 1.4, ec[1] - 0.6), (ec[0] - 3.2, ec[1] - 0.9), 0.18, 0.18, (20, 20, 26))
        m0 = (he[0] - hd_[0] * 1.6 + dn[0] * 0.2, he[1] - hd_[1] * 1.6 + dn[1] * 0.2)
        if stache_drop is None:
            smask(L, m0, 0.0)
        else:
            k = min(1.0, stache_drop / 0.7)
            smask(L, (m0[0] - 1.5 * k, m0[1] + 18.0 * k * k), stache_drop * 7)
    if rider: rider(L, T)
    outline(L, S.HC['ol']); CH.add(L)
    return hs, hd_, he


def smask(L, c, ang):
    """big fake mustache (curly ends)"""
    ca, sa = math.cos(ang), math.sin(ang)
    def R(a, b): return (c[0] + a * ca - b * sa, c[1] + a * sa + b * ca)
    cap(L, R(-1.9, 0.0), R(1.9, 0.0), 0.75, 0.75, (28, 22, 20))
    cap(L, R(-1.9, 0.0), R(-2.7, -0.9), 0.5, 0.3, (28, 22, 20)); cap(L, R(1.9, 0.0), R(2.7, -0.9), 0.5, 0.3, (28, 22, 20))


def head_world(v_cam_fn, wx, wy, unit, Pz, flip=False):
    """world position of the horse head start (for close-up framing)"""
    hs = S.horse_frames(1000.0, 1000.0, Pz)[3]
    dx = (hs[0] - 1000.0) * unit
    return (wx - dx if flip else wx + dx), wy + (hs[1] - 1000.0) * unit


def rider_billy(pose, mouth=0.0, rot=0.05):
    """returns a rider callable for molniya(): Billy sitting in the saddle"""
    def f(L, T):
        hip = T(-1.0, -9.4)
        S.CC['mst'] = (96, 60, 36)
        S.cowboy(L, hip, rot, pose, hat_on=False, mouth=mouth)
        HP = HPf(rot, hip)
        ell(L, HP(0.4, 11.4), 2.9, 1.5, (104, 66, 40), rot, hi=(136, 90, 56))
        cap(L, HP(1.4, 8.55), HP(3.1, 8.45), 0.55, 0.45, (96, 60, 36))
    return f


# ---------------------------------------------------------------- donkey (Sam's), rocking horse
def long_ears(L, hs, hd_, up, ear, t):
    for side, off in ((0, -0.7), (1, 0.5)):
        base = (hs[0] + up[0] * 2.3 - hd_[0] * (0.2 - off), hs[1] + up[1] * 2.3 - hd_[1] * (0.2 - off))
        e = ear + side * 0.25 + 0.05 * math.sin(t * 1.3)
        tip = (base[0] + 6.2 * (up[0] * math.cos(e) - hd_[0] * math.sin(e)), base[1] + 6.2 * (up[1] * math.cos(e) - hd_[1] * math.sin(e)))
        cap(L, base, tip, 1.4, 0.7, S.HC['body'] if side else S.HC['far'])
        if side: cap(L, base, tip, 0.5, 0.3, (90, 84, 82))


def donkey(CH, cam, t, bray=0.0):
    L = Layer(cam)
    Pz = S.stand_pose(t)
    Pz.update(neck=-0.55 - 0.5 * bray, head=0.95 - 0.8 * bray, ear=0.75, lid=0.3 - 0.3 * bray, jaw=0.9 * bray)
    T, hs, hd_, up = with_pal(S.HC, DONKEY, lambda: S.draw_horse(L, 1000.0, 1000.0, Pz, t, 0.0, saddle=True))
    with_pal(S.HC, DONKEY, lambda: long_ears(L, hs, hd_, up, Pz['ear'], t))
    outline(L, (38, 30, 30)); CH.add(L)


def rocking_horse(CH, cam, ang):
    """toy rocking horse, anchor (1000,1000) = floor contact centre; ang = rock angle"""
    L = Layer(cam)
    ca, sa = math.cos(ang), math.sin(ang)
    def R(a, b): return (1000.0 + a * ca - b * sa, 1000.0 + a * sa + b * ca)
    for i in range(10):                                                                      # rocker arc
        a0 = -8 + i * 1.6; a1 = a0 + 1.6
        cap(L, R(a0, -0.02 * a0 * a0), R(a1, -0.02 * a1 * a1), 0.55, 0.55, (150, 40, 36))
    for lx in (-4.5, 4.5): cap(L, R(lx, -0.4), R(lx * 0.7, -5.0), 0.5, 0.5, (236, 226, 200))
    cap(L, R(-4.0, -6.0), R(4.0, -6.0), 2.0, 2.0, (236, 226, 200), hi=(250, 244, 230))
    for k in range(3): dot(L, R(-2 + k * 2, -6.4), (70, 110, 180), 0.5)                       # painted dots
    cap(L, R(3.2, -7.0), R(5.2, -11.0), 1.2, 1.0, (236, 226, 200))
    cap(L, R(5.2, -11.0), R(8.0, -10.4), 1.2, 0.9, (236, 226, 200))
    for k in range(4): cap(L, R(4.2 - k * 0.5, -9.5 + k * 1.1), R(2.8 - k * 0.5, -9.0 + k * 1.1), 0.5, 0.3, (190, 60, 44))
    cap(L, R(-4.2, -6.4), R(-6.4, -4.6), 0.5, 0.3, (190, 60, 44))
    dot(L, R(6.4, -11.2), (30, 20, 16), 0.3)
    cap(L, R(4.8, -12.0), R(5.2, -13.2), 0.4, 0.2, (236, 226, 200))
    outline(L, (40, 24, 14)); CH.add(L)
