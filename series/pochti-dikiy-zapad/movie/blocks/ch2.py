"""Chapter 2 «Засада»: new costume-building montage + S01E02 rebuilt in HD 16:9 (cactus field, barrel-cactus costume)."""
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from kit import *

DUR = 49.0
DAY, INCOME = 118, (1, 8, 33.6)

VOICE = [
    ('n1',  'movie', 'b1', 0.10, 0.00, 4.99, 'billy',   'Ай! Ай... Ай! ГЕНИАЛЬНО!'),
    ('e1',  'ep02',  'b1', 6.60, 0.10, 2.45, 'billy',   'Тс-с. Я — КАКТУС.'),
    ('e2',  'ep02',  'b2', 8.70, 0.20, 6.00, 'billy',   'План гениальный: Сэм подъедет — а я его... ХВАТЬ!'),
    ('m1',  'movie', 'b2', 15.30, 0.10, 3.50, 'molniya', 'Кактус с человеческим ЛИЦОМ. Смело.'),
    ('e3',  'ep02',  'b3', 19.40, 0.10, 1.70, 'billy',   'Молния! ПРЯЧЬСЯ!'),
    ('m2',  'ep02',  'm2', 21.60, 0.10, 1.00, 'molniya', 'Спряталась.'),
    ('s1',  'ep02',  's1', 24.80, 0.05, 3.30, 'sam',     'Какой славный кактус... Присяду.'),
    ('b4',  'ep02',  'b4', 28.70, 0.25, 1.85, 'billy',   'Ммм-мф-ф-ф!'),
    ('s2',  'ep02',  's2', 30.70, 0.20, 1.80, 'sam',     'Хм. Тёплый.'),
    ('s3',  'ep02',  's3', 33.00, 0.10, 3.90, 'sam',     'Как договаривались, мэм. Морковь за неделю.'),
    ('n4',  'ep01',  'n4', 37.10, 0.12, 0.75, 'molniya', 'СПАСИБО.'),
    ('b5',  'ep02',  'b5', 40.40, 0.08, 4.60, 'billy',   'Засада сработала! Он меня даже не ЗАМЕТИЛ!'),
    ('m3',  'ep02',  'm3', 45.20, 0.05, 0.75, 'molniya', 'ВОЗДУХАН.'),
]
SFX = [
    ('library/sfx/film_click.mp3', 0.00, 0.7),
    ('library/sfx/needle_prick.mp3', 0.45, 0.9), ('library/sfx/needle_prick.mp3', 1.40, 0.9), ('library/sfx/needle_prick.mp3', 2.65, 0.9),
    ('library/sfx/whoosh.mp3', 5.60, 0.6),
    ('series/pochti-dikiy-zapad/sfx/costume_pop.mp3', 6.30, 0.8),
    ('library/sfx/wind_gust.mp3', 8.20, 0.5),
    ('library/sfx/horse_snort.mp3', 18.90, 0.5),
    ('library/sfx/vulture.mp3', 22.40, 0.6),
    ('library/sfx/donkey_walk.mp3', 23.20, 0.5),
    ('library/sfx/donkey_bray.mp3', 28.30, 0.6),
    ('library/sfx/boots_stomp.mp3', 33.30, 0.5),
    ('series/pochti-dikiy-zapad/sfx/carrot_spill.mp3', 35.80, 0.9),
    ('library/sfx/counter_blip.mp3', 35.90, 0.6),
    ('library/sfx/carrot_crunch.mp3', 38.30, 0.6),
    ('library/sfx/donkey_walk.mp3', 38.80, 0.5),
    ('series/pochti-dikiy-zapad/sfx/costume_pop.mp3', 40.30, 1.0),
    ('library/sfx/carrot_crunch.mp3', 45.35, 0.6),
]
BEDS = [
    ('series/pochti-dikiy-zapad/music/sneaky_deal_15s.mp3', 14.9, 0.0, 49.0, 0.28, True),
    ('library/sfx/amb_desert_wind.mp3', 7.8, 6.0, 49.0, 0.7, False),
]
EPI = episode('mv_ch2', VOICE, DUR)
talk = EPI.talk

FIELD, RANCH = bgworld('cactus_field'), bgworld('ranch_dawn')
FEET = 600.0
U = 6.0
E0 = 6.2                         # start of the E02 part
MX, PX_POST, CX = 330.0, 352.0, 860.0
T_SIT, T_GIVE, T_POP = 29.4, 33.0, 40.4
T_SPILL = 35.8


def light(scene):
    if scene == 'ranch': return Light(amb=(1.12, 0.92, 0.78), rim=(1, -1, (255, 190, 120), 0.55), grad=(1.08, 0.85))
    return Light(amb=(1.08, 0.98, 0.86), rim=(1, -1, (255, 226, 170), 0.5), grad=(1.08, 0.88))


def wv(world, cx, cy, Z):
    return ST.View(world, cx - ST.W / 2 / Z, cy - ST.H / 2 / Z, Z)


# ---------------------------------------------------------------- props
def costume(CH, v, x, feet, u, wob=0.0, squash=1.0, hand=0.0, spines=1.0):
    """barrel-cactus suit; Billy's eyes look out of a dark hole. anchor (1000,1000) = body centre"""
    L = Layer(v.cam(x + wob, feet - 6 * u * squash, u))
    g, gh, gs = (70, 140, 66), (112, 180, 92), (44, 100, 50)
    ell(L, (1000.0, 1000.0), 7.2, 6.4 * squash, g, hi=gh, sh=gs)
    for k in (-4.5, -2.4, 0.0, 2.4, 4.5):
        cap(L, (1000.0 + k, 995.2 + 0.6), (1000.0 + k * 0.95, 1004.8 * squash + 1000 * (1 - squash) + 0.0), 0.22, 0.22, gs)
    for k in (-4.5, -2.4, 0.0, 2.4, 4.5):
        for yy in (-4.2, -1.6, 1.0, 3.6):
            dot(L, (1000.0 + k * 0.95, 1000.0 + yy * squash), (238, 234, 200), 0.24 * spines)
    ell(L, (1000.0, 993.9 + 6.4 * (1 - squash)), 1.7, 0.9, (240, 110, 160))
    ell(L, (1000.0 + 0.2, 999.4), 3.6, 2.3, (26, 18, 18))
    for ex in (-1.3, 1.5):
        ell(L, (1000.0 + ex, 999.1), 1.0, 1.25, (250, 250, 244)); dot(L, (1000.0 + ex + 0.2, 999.2), (20, 14, 12), 0.45)
    if hand > 0:
        hx = 1007.0 + 5.5 * hand
        cap(L, (1006.0, 1001.0), (hx, 1000.0 - 2.5 * hand), 1.5, 1.2, (170, 60, 50))
        dot(L, (hx + 0.8, 1000.0 - 2.7 * hand), (226, 176, 136), 1.2)
    outline(L, (30, 60, 30)); CH.add(L)


def costume_halves(CH, v, x, feet, u, k):
    """the suit bursts into two halves (k = seconds since the pop)"""
    for side in (-1, 1):
        L = Layer(v.cam(x + side * (3 + 34 * k), feet - 6 * u + (-90 * k + 220 * k * k), u))
        ell(L, (1000.0, 1000.0), 3.6, 6.4, (70, 140, 66), hi=(112, 180, 92), sh=(44, 100, 50), ang=side * k * 2.2)
        for yy in (-3, 0, 3): dot(L, (1000.0 + side * 1.0, 1000.0 + yy), (238, 234, 200), 0.24)
        outline(L, (30, 60, 30)); CH.add(L)


def signpost(CH, v, x, feet):
    L = Layer(v.wcam())
    wrect(L, x - 5, feet - 205, x + 5, feet, (112, 74, 42)); wrect(L, x - 5, feet - 205, x - 2, feet, (146, 100, 60))
    for i, (y0, wx0, wx1) in enumerate(((feet - 195, x - 74, x + 8), (feet - 172, x - 60, x + 8))):
        wrect(L, wx0, y0, wx1, y0 + 18, (150, 104, 60)); wrect(L, wx0, y0 + 16, wx1, y0 + 18, (96, 62, 36))
    wrect(L, x + 8, feet - 168, x + 78, feet - 96, (232, 218, 176)); wrect(L, x + 8, feet - 168, x + 78, feet - 165, (196, 172, 124))
    wrect(L, x + 34, feet - 146, x + 52, feet - 138, (46, 40, 48)); wrect(L, x + 36, feet - 138, x + 50, feet - 128, (226, 176, 136))
    wrect(L, x + 36, feet - 135, x + 50, feet - 132, (24, 20, 24)); wrect(L, x + 38, feet - 134, x + 40, feet - 133, (240, 240, 240))
    outline(L, (50, 30, 18)); CH.add(L)
    if v.Z >= 0.7:
        for txt, wx, wy, col in (('САЛУН', x - 33, feet - 186, (60, 34, 20)), ('ТЮРЬМА', x - 26, feet - 163, (60, 34, 20)),
                                 ('РОЗЫСК', x + 43, feet - 158, (140, 36, 26)), ('$500', x + 43, feet - 112, (90, 50, 30))):
            sx, sy = v.pt(wx, wy); px_text(CH, txt, sx, sy, 8 if ST.PX[0] == 1 else 8, col)


def vulture(CH, v, x, y, t):
    L = Layer(v.cam(x, y, 4.0))
    ell(L, (1000.0, 1000.0), 3.6, 2.6, (44, 36, 36), hi=(70, 60, 58))
    cap(L, (1002.0, 998.5), (1004.0, 995.5), 0.9, 0.9, (44, 36, 36))
    dot(L, (1004.5, 995.0), (200, 90, 80), 1.0); cap(L, (1005.2, 995.2), (1007.0, 996.0), 0.4, 0.15, (230, 190, 70))
    bob = 0.6 * math.sin(t * 3)
    cap(L, (998.0, 1000.0), (995.0, 1001.5 + bob), 1.3, 0.6, (34, 28, 28))
    outline(L, (20, 14, 14)); CH.add(L)


def carrots_ground(CH, v, x, feet, t, eaten):
    L = Layer(v.wcam())
    for i, dx in enumerate((-36, -18, 4, 22, 40, 12, -8)):
        if i < 7 - eaten:
            y = feet + 8 + (i % 3) * 5; x0 = x + dx
            cap(L, (x0, y), (x0 + 20, y - 4), 4.0, 1.4, (236, 128, 40), hi=(255, 176, 90))
            for a in (-0.5, 0.0, 0.5): cap(L, (x0, y), (x0 - 8 * math.cos(a), y - 8 * math.sin(a) - 3), 1.6, 0.9, (84, 160, 60))
    outline(L, (70, 40, 20)); CH.add(L)


# ---------------------------------------------------------------- choreography (Sam enters from the RIGHT)
def sam_state(t):
    """(x, mode) mode: ride | sit | walk_l | give | walk_r | ride_away | none"""
    if t < 22.0: return None, 'none'
    if t < 26.4: return lerp(1500, 900, sm((t - 22.0) / 4.4)), 'ride'
    if t < T_SIT: return lerp(900, CX + 30, sm((t - 26.4) / 2.9)), 'walk_l'
    if t < 32.7: return CX, 'sit'
    if t < T_GIVE + 2.4: return lerp(CX, MX + 200, sm((t - 32.7) / 2.4)), 'walk_l'
    if t < 38.6: return MX + 200, 'give'
    if t < 40.4: return lerp(MX + 200, 900, sm((t - 38.6) / 1.8)), 'walk_r'
    return lerp(900, 1500, sm((t - 40.4) / 2.6)), 'ride'


def sam_hip_on_costume():
    return CX + 2, FEET + 6 - 12.9 * U


def field_scene(CH, FX, big, v, t):
    ep = t - E0
    fx.motes(FX, v, t, 0, 300, 1280, 700, n=30, seed=6)
    # Molniya behind (in front of) the thin post, hat on
    if t >= 6.0:
        mx = MX if t < 19.6 else lerp(MX, MX + 8, sm((t - 19.6) / 0.6))
        ph = C.molniya_pose(t, chew=t >= 38.2, jaw_talk=talk('molniya', t))
        ax, ay = C.horse_anchor(mx, FEET, U)
        shadow(big, v, mx, FEET, 16 * U, 1.8 * U)
        C.molniya(CH, v.cam(ax, ay, U), t, ph, hat=True, carrot=t >= 38.4, carrots=1)
        signpost(CH, v, PX_POST, FEET)
        if t >= 22.0: vulture(CH, v, PX_POST - 20, FEET - 205, t)
        if T_SPILL <= t: carrots_ground(CH, v, MX + 30, FEET, t, 0 if t < 38.4 else 2)
    # costume / Billy
    if t < T_POP:
        squash = 1.0
        wob = 0.0
        if T_SIT <= t < 32.7:
            squash = 0.93 + 0.02 * math.sin(t * 30); wob = 1.5 * math.sin(t * 24) * (1 if t < 30.6 else 0.4)
        hand = 0.0
        if 13.0 <= t < 14.6: hand = min(1.0, (t - 13.0) / 0.2) * (1 - sm((t - 14.2) / 0.3))
        shadow(big, v, CX, FEET + 6, 8 * U, 1.4 * U)
        costume(CH, v, CX, FEET + 6, U, wob, squash, hand)
    else:
        k = t - T_POP
        costume_halves(CH, v, CX, FEET + 6, U, min(k, 1.6))
        bx = CX + 20
        shadow(big, v, bx, FEET + 6, 5 * U, 1.2 * U)
        pose = C.POSES['heroic'] if k < 3.0 else C.POSES['hips']
        C.billy(CH, v.cam(bx, FEET + 6 - C.HIP_H * U, U), pose, 0.05, talk('billy', t), 'shout' if k < 3.5 else 'sly', hat=False)
        if k < 0.5: fx.dust_puffs(FX, v, t, [(T_POP, CX, FEET + 6, 26)])
    # donkey + Sam
    x, mode = sam_state(t)
    if mode != 'none':
        du = U * 0.85
        if mode in ('ride',):
            shadow(big, v, x, FEET - 4, 13 * du, 1.6 * du)
            C.donkey(CH, v.cam(x, FEET - 4 - 19 * du, du), t, moving=True,
                     rider=C.rider_sam(dict(C.POSES['ride'], _t=t), talk('sam', t)))
        else:
            dx_ = 980.0 if mode != 'ride_away' else x
            shadow(big, v, 990, FEET - 4, 13 * du, 1.6 * du)
            C.donkey(CH, v.cam(990, FEET - 4 - 19 * du, du), t, moving=False, bray=1.0 if 28.2 <= t < 28.8 else 0.0)
            if mode == 'sit':
                hx, hy = sam_hip_on_costume()
                C.sam(CH, v.cam(hx, hy, U, True), C.POSES['sit'], 0.03, talk('sam', t))
            elif mode in ('walk_l', 'walk_r'):
                fl = mode == 'walk_l'
                shadow(big, v, x, FEET + 4, 5 * U, 1.2 * U)
                C.sam(CH, v.cam(x, FEET + 4 - C.HIP_H * U, U, fl), C.walk_pose(t * 0.75, 9, 0.3), 0.03, talk('sam', t))
            elif mode == 'give':
                shadow(big, v, x, FEET + 4, 5 * U, 1.2 * U)
                pose = C.POSES['present'] if t < 37.0 else C.POSES['stand']
                C.sam(CH, v.cam(x, FEET + 4 - C.HIP_H * U, U, True), pose, 0.03, talk('sam', t))
    if t < 6.2: pass


# ---------------------------------------------------------------- montage at the ranch (0 .. 6.2)
UR = 8.0
RBX = 640.0


def montage_scene(CH, FX, big, v, t):
    fx.motes(FX, v, t, 0, 200, 1280, 650, n=30, col=(255, 210, 150), seed=3)
    feet = 620.0
    # the empty barrel suit on a stand, Billy around it
    k = min(1.0, t / 5.0)
    shadow(big, v, RBX + 150, feet, 8 * UR * 0.9, 1.4 * UR * 0.9)
    costume(CH, v, RBX + 150, feet, UR * 0.9, 0.0, 1.0, 0.0, spines=min(1.0, 0.2 + t / 4.0))
    pose = C.POSES['excited'] if t >= 3.6 else C.POSES['lean'] if int(t * 2) % 2 else C.POSES['hips']
    ouch = [0.45, 1.40, 2.65]
    bump = max((math.exp(-(t - o) * 9) for o in ouch if 0 <= t - o < 0.7), default=0.0)
    shadow(big, v, RBX, feet, 5 * UR, 1.2 * UR)
    C.billy(CH, v.cam(RBX + 4 * bump, feet - C.HIP_H * UR - 3 * bump, UR), pose, 0.05 + 0.2 * bump, talk('billy', t),
            'shout' if (bump > 0.3 or t >= 3.6) else 'sly', hat=True)
    for o in ouch:
        if 0 <= t - o < 0.5:
            L = Layer(v.cam(RBX, feet - C.HIP_H * UR, UR))
            for i in range(4):
                a = i * 1.57 + 0.6 + (t - o) * 3; S.star(L, (1000.0 + 6 * math.cos(a), 1000 - 15 + 4 * math.sin(a)))
            CH.add(L)


def montage_shot(t):
    if t < 1.5: v = wv(RANCH, RBX + 20, 520, 1.6)
    elif t < 2.8: v = wv(RANCH, RBX + 60, 500, 2.0)
    elif t < 4.4: v = wv(RANCH, RBX + 40, 490, 1.7 + 0.05 * (t - 2.8))
    else: v = wv(RANCH, RBX + 60, 500, 1.35)
    return shot(v, t, lambda CH, FX, big, vv: montage_scene(CH, FX, big, vv, t), light('ranch'))


# ---------------------------------------------------------------- shots
def field_shot(t):
    def head(x=MX): return C.head_of_horse(x, FEET, U, C.molniya_pose(t))
    if t < 8.7:
        v = wv(FIELD, CX, FEET - 60, 2.6 - 0.05 * (t - 6.2))                       # costume close-up (hook)
    elif t < 13.0: v = wv(FIELD, CX - 10, FEET - 50, 2.2 + 0.06 * (t - 8.7))
    elif t < 15.2: v = wv(FIELD, CX + 20, FEET - 70, 2.4)
    elif t < 19.0:
        hx, hy = head(); v = wv(FIELD, hx + 10, hy + 20, 2.8 - 0.02 * (t - 15.2))
    elif t < 21.6: v = wv(FIELD, 590, FEET - 110, 0.9)
    elif t < 24.4:
        hx, hy = head(MX); v = wv(FIELD, hx + 50, hy + 10, 2.5)
    elif t < 28.4: v = wv(FIELD, 780, FEET - 90, 1.1)
    elif t < 32.8: v = wv(FIELD, CX - 30, FEET - 90, 1.75)
    elif t < 36.0: v = wv(FIELD, 560, FEET - 90, 1.35)
    elif t < 38.9: v = wv(FIELD, MX + 120, FEET - 70, 1.9)
    elif t < 40.4: v = wv(FIELD, 600, FEET - 80, 1.0)
    elif t < 45.0: v = wv(FIELD, CX + 10, FEET - 80, 1.7)
    else:
        hx, hy = head(); v = wv(FIELD, hx + 20, hy + 10, 2.6)
    return shot(v, t, lambda CH, FX, big, vv: field_scene(CH, FX, big, vv, t), light('field'))


STICKERS = [
    (O.sticker('+7', icon=C.carrot_icon(1, 7)), 36.0, 37.4, 1450, 300),
    (O.sticker('ХВАТЬ!', fg=(255, 120, 90), size=80), 13.2, 14.3, 960, 300),
]


def render_scene(t):
    return montage_shot(t) if t < E0 else field_shot(t)


def render(t):
    big = render_scene(t)
    WO.stickers(big, STICKERS, t)
    WO.hud(big, t, DAY, INCOME[1] if t >= INCOME[2] else INCOME[0])
    EPI.captions.draw(big, t, WO.CAP_Y)
    flash_at(big, t, [E0, T_POP], 0.15, 0.6)
    if E0 <= t < E0 + 0.25: O.mosaic(big, int(lerp(44, 1, (t - E0) / 0.25)))
    return big
