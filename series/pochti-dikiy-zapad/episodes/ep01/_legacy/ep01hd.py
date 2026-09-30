import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import numpy as np, math, sys, subprocess
from PIL import Image, ImageDraw, ImageFont
import scene as S
import hd as HDP
from scene import (Layer, cap, dot, outline, comp, hsh, sm, lerp, clamp01, GROUND)
W, H, XX, YY = S.W, S.H, S.XX, S.YY

DUR = 40.0
FPS = 30
OFF = 8.5  # old gag sequence shifted by 8s

# ---- retime the gag (functions in scene read these globals at call time)
S.T_BRAKE, S.T_STOP = 6.1 + OFF, 6.8 + OFF
S.T_LAUNCH, S.T_LAND = 6.35 + OFF, 7.45 + OFF
S.T_HAT = 8.1 + OFF
S.T_EAT0, S.T_EAT1 = 8.4 + OFF, 10.3 + OFF
S.T_CLOSE = 10.4 + OFF
T_CLOSE_END = 23.85
S.CAMX_STOP = S.cam_x(S.T_STOP)
S.HORSE_WX = S.CAMX_STOP + S.HORSE_SX
S.CARROT_WX = S.HORSE_WX + 21
S.CACTUS_WX = S.CAMX_STOP + 88

# ---- flip-capable camera
class Cam(S.Cam):
    def __init__(s, x0, y0, sc=1.0, flip=False):
        super().__init__(x0, y0, sc); s.flip = flip
    def p(s, x, y):
        X = (x - s.x0) * s.sc
        return (-X if s.flip else X, (y - s.y0) * s.sc)

_ell = S.ell
def ell_flip(L, cxy, rx, ry, c, ang=0.0, **kw):
    if getattr(L.cam, 'flip', False): ang = -ang
    return _ell(L, cxy, rx, ry, c, ang, **kw)
S.ell = ell_flip
ell = ell_flip

# ---- audio envelopes for lip flap
for k in ('n1', 'n2', 'n3', 'n4', 'n5', 'n6'):
    S.ENV[k] = S.load_env(P.voice_wav('ep01', k))

LINES = {}  # filled from timing file: name -> start time
exec(open(pathlib.Path(__file__).with_name('timing.py')).read())

def spk_amp(names, t):
    best = 0.0
    for nm, (st, a, b) in names.items():
        if st <= t < st + (b - a):
            best = max(best, S.amp(nm, a + t - st))
    return best

HORSE_SPEECH = {'h1a': None}
def horse_amp(t):
    d = {'n2': (LINES['n2'], 0, 99), 'n4': (LINES['n4'], 0, 99), 'n6': (LINES['n6'], 0, 99)}
    v = spk_amp(d, t)
    if S.HA_T <= t < S.HA_T + S.HA_OUT - S.HA_IN: v = max(v, S.amp('h1', S.HA_IN + t - S.HA_T))
    if S.HB_T <= t < S.HB_T + S.HB_OUT - S.HB_IN: v = max(v, S.amp('h1', S.HB_IN + t - S.HB_T))
    return v
S.HA_T, S.HB_T = 10.9 + OFF, 13.05 + OFF
S.horse_amp = horse_amp

# ---- particles regenerate with new times
rng = np.random.default_rng(7)
S.PART.clear()
t_ = 0.0
while t_ < S.T_BRAKE:
    S.PART.append(dict(b=t_, x=-9 + rng.uniform(-3, 3), y=GROUND - 1, vx=-S.V + rng.uniform(4, 10), vy=rng.uniform(-8, -3), life=0.45, r0=0.8, r1=2.6, rel=True)); t_ += 0.11
t_ = S.T_BRAKE
while t_ < S.T_STOP:
    S.PART.append(dict(b=t_, x=13 + rng.uniform(-2, 3), y=GROUND - 1, vx=rng.uniform(8, 34), vy=rng.uniform(-20, -6), life=0.8, r0=1.2, r1=4.0, rel=True)); t_ += 0.025
for i in range(12):
    a = rng.uniform(0, math.pi)
    S.PART.append(dict(b=S.T_LAND, x=S.CACTUS_WX - S.CAMX_STOP, y=GROUND - 22, vx=26 * math.cos(a) * rng.uniform(.4, 1), vy=-26 * math.sin(a) * rng.uniform(.4, 1), life=0.5, r0=1.4, r1=2.8, rel=False))

# ---- donkey + bandit
DONKEY = dict(body=(150, 144, 140), hi=(182, 176, 170), sh=(114, 108, 106), far=(118, 112, 110), farsh=(92, 88, 86),
              mane=(70, 64, 64), maneh=(100, 94, 92), muz=(214, 208, 198), white=(236, 232, 224), blanket=(176, 128, 60), blanket_h=(206, 160, 84))
BANDIT = dict(hat=(46, 40, 48), hat_h=(76, 68, 80), band=(190, 50, 50), shirt=(96, 70, 128), shirt_h=(124, 96, 158), shirt_sh=(70, 50, 96),
              vest=(40, 34, 36), jeans=(90, 80, 70), jeans_sh=(66, 58, 50), bandana=(196, 52, 52), mst=(34, 26, 24), skin=(226, 176, 136))

def with_pal(d, pal, fn):
    old = {k: d[k] for k in pal}
    d.update(pal)
    try: return fn()
    finally: d.update(old)

def walk_pose(p):
    legs = []
    for kind, off in (('h', 0.0), ('f', 0.25), ('h', 0.5), ('f', 0.75)):
        ph = 2 * math.pi * (p + off)
        if kind == 'f':
            a1 = 0.02 + 0.28 * math.sin(ph); a2 = a1 - 0.7 * max(0.0, math.cos(ph)) ** 2
        else:
            a1 = -0.33 + 0.26 * math.sin(ph); a2 = a1 + 0.5 + 0.5 * max(0.0, math.cos(ph)) ** 2
        legs.append((a1, a2))
    return dict(legs=legs, bob=-0.5 * abs(math.sin(2 * math.pi * p)), pitch=0.0, neck=-0.55, head=0.95, jaw=0.0, wind=0.0, ear=0.75, lid=0.3)

def stand_d():
    P = S.stand_pose(0); P.update(neck=-0.55, head=0.95, ear=0.75); return P

BX = [(24.0, 118.0), (26.5, 74.0), (30.6, 74.0), (37.3, -34.0)]  # keyframes of donkey screen x
def donkey_x(t):
    if t <= BX[0][0]: return BX[0][1]
    for (t0, x0), (t1, x1) in zip(BX, BX[1:]):
        if t <= t1:
            return lerp(x0, x1, (t - t0) / (t1 - t0))
    return BX[-1][1]

def donkey_moving(t): return (BX[0][0] < t < BX[1][0]) or (BX[2][0] < t < BX[3][0])

def draw_donkey_bandit(F, t):
    if not (BX[0][0] <= t <= BX[3][0]): return
    sx = donkey_x(t) * 2; sy = (GROUND + 7) * 2
    sc = 0.78 * 2
    wx, wy = 1000.0, 1000.0
    cam = Cam(sx / -sc * -1 + wx, wy - sy / sc, sc, flip=True)
    # flip: screen = -(x - x0)*sc  -> x0 = wx + sx/sc
    cam.x0 = wx + sx / sc
    moving = donkey_moving(t)
    p = (t * 1.6) % 1.0
    P = walk_pose(p) if moving else stand_d()
    hy = wy - 19
    L = Layer(cam)
    old_ear = S.draw_ears
    def long_ears(L_, hs, hd, up, ear):
        for side, off in ((0, -0.7), (1, 0.5)):
            base = (hs[0] + up[0] * 2.3 - hd[0] * (0.2 - off), hs[1] + up[1] * 2.3 - hd[1] * (0.2 - off))
            e = ear + side * 0.25 + (0.15 * math.sin(t * 6) if moving else 0)
            tip = (base[0] + 6.2 * (up[0] * math.cos(e) - hd[0] * math.sin(e)), base[1] + 6.2 * (up[1] * math.cos(e) - hd[1] * math.sin(e)))
            cap(L_, base, tip, 1.4, 0.7, S.HC['body'] if side else S.HC['far'])
            if side: cap(L_, base, tip, 0.5, 0.3, (90, 84, 82))
    res = with_pal(S.HC, DONKEY, lambda: S.draw_horse(L, wx, hy, P, t, p, saddle=True))
    T, hs, hd, up = res
    with_pal(S.HC, DONKEY, lambda: long_ears(L, hs, hd, up, P['ear']))
    # money sack on the rump
    ell(L, T(-9.5, -9.8), 3.8, 3.4, (238, 226, 198), hi=(252, 246, 230), sh=(206, 190, 158))
    cap(L, T(-9.5, -12.8), T(-9.5, -14.4), 1.0, 1.4, (238, 226, 198))
    cap(L, T(-10.7, -12.6), T(-8.3, -12.6), 0.5, 0.5, (150, 110, 60))
    outline(L, (38, 30, 30)); comp(F, L)
    # $ sign on sack (screen space)
    sxy = cam.p(*T(-9.5, -9.8))
    x0, y0 = int(sxy[0]) - 3, int(sxy[1]) - 5
    for dx, dy in ((1, 0), (0, 1), (1, 2), (2, 3), (1, 4), (1, -1), (1, 5), (2, 0), (0, 4)):
        X_, Y_ = x0 + dx * 2, y0 + dy * 2
        if 0 <= Y_ < H - 1 and 0 <= X_ < W - 1: F[Y_:Y_ + 2, X_:X_ + 2] = (40, 96, 40)
    # bandit
    L = Layer(cam)
    hip = T(-1, -8.4)
    tip_k = 0.0
    tip0 = LINES['n3'] - 0.2
    if tip0 < t < tip0 + 1.4: tip_k = sm((t - tip0) / 0.25) * (1 - sm((t - tip0 - 1.1) / 0.3))
    pose = dict(nleg=(1.3, 0.15), fleg=(1.25, 0.2), narm=(lerp(0.9, 2.9, tip_k), lerp(1.6, 3.6, tip_k)), farm=(0.8, 1.5))
    bob = 0.4 * math.sin(t * 10) if moving else 0
    hatpos = with_pal(S.CC, BANDIT, lambda: S.cowboy(L, (hip[0], hip[1] + bob), 0.05, pose, hat_on=tip_k < 0.05,
                                                     mouth=S.amp('n3', t - LINES['n3']) if LINES['n3'] <= t else 0))
    if tip_k >= 0.05:
        with_pal(S.CC, BANDIT, lambda: S.hat(L, (hatpos[0] + 0.8 * tip_k, hatpos[1] - 2.2 * tip_k), -0.3 * tip_k))
    # eye mask
    u = (0, -1)
    cap(L, (hip[0] - 1.2, hip[1] + bob - 10.3), (hip[0] + 2.6, hip[1] + bob - 10.3), 0.75, 0.75, (24, 20, 24))
    dot(L, (hip[0] + 1.8, hip[1] + bob - 10.3), (240, 240, 240), 0.3)
    # big droopy mustache
    cap(L, (hip[0] + 1.3, hip[1] + bob - 8.4), (hip[0] + 3.4, hip[1] + bob - 7.2), 0.6, 0.4, (34, 26, 24))
    outline(L, (20, 14, 14)); comp(F, L)

# ---- captions
FONT = ImageFont.truetype(P.FONT_BOLD, 64)
FONT_T = ImageFont.truetype(P.FONT_BOLD, 96)
FONT_S = ImageFont.truetype(P.FONT_BOLD, 54)
YEL, WHT, PUR = (255, 222, 96), (255, 255, 255), (214, 170, 255)

def dur(k): return DUR_OF[k]
CAPS = [
    (LINES['c1'] + 0.05, LINES['c1'] + 5.7, 'Н-но, родная! Я\u00a0— самый быстрый ковбой на всём Диком Западе!', YEL),
    (LINES['n1'], LINES['n1'] + dur('n1') + 0.2, 'Сегодня я наконец поймаю Кривого Сэма!', YEL),
    (LINES['n2'], LINES['n2'] + dur('n2') + 0.3, 'Он ловит его третий год.', WHT),
    (6.3 + OFF, 7.5 + OFF, 'А-А-А-А-А!', YEL),
    (7.9 + OFF, 9.95 + OFF, 'Ой-й... кактус...', YEL),
    (10.9 + OFF, 12.5 + OFF, 'Самый быстрый тут\u00a0—\u00a0я.', WHT),
    (13.05 + OFF, T_CLOSE_END, 'А ты просто сверху сидел.', WHT),
    (LINES['n3'], LINES['n3'] + dur('n3') + 0.3, 'Приятного аппетита, мэм.', PUR),
    (LINES['n4'], LINES['n4'] + dur('n4') + 0.4, 'Спасибо.', WHT),
    (LINES['n5'], LINES['n5'] + dur('n5') + 0.2, 'Молния... Ты не видела Кривого Сэма?', YEL),
    (LINES['n6'], LINES['n6'] + 1.4, 'Не-а.', WHT),
]

def make_text(lines, fonts, colors, gap=20, width=1000):
    img = Image.new('RGBA', (1080, 560), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    y = 20
    for text, font, col in zip(lines, fonts, colors):
        words = text.split(); rows = []; cur = ''
        for w in words:
            tst = (cur + ' ' + w).strip()
            if d.textlength(tst, font=font) > width and cur: rows.append(cur); cur = w
            else: cur = tst
        rows.append(cur)
        for r in rows:
            tw = d.textlength(r, font=font)
            d.text(((1080 - tw) / 2, y), r, font=font, fill=col + (255,), stroke_width=8, stroke_fill=(20, 12, 10, 255))
            y += int(font.size * 1.3)
        y += gap
    return np.array(img)

CAP_IMG = [make_text([c[2]], [FONT], [c[3]]) for c in CAPS]
TITLE = make_text(['ПОЧТИ', 'ДИКИЙ ЗАПАД', 'Серия 1 · «Самый быстрый»'], [FONT_T, FONT_T, FONT_S], [YEL, YEL, WHT], gap=0)
END = make_text(['Продолжение следует…', 'Серия 2 — скоро'], [FONT, FONT_S], [YEL, WHT], gap=10)
CAP_Y = 250

def overlay(big, img, y0, k):
    region = big[y0:y0 + img.shape[0]]
    al = img[..., 3:4].astype(np.float32) / 255 * k
    region[:] = (region * (1 - al) + img[..., :3] * al).astype(np.uint8)

# ---- frame
def horse_pose(t):
    P, p = S.horse_pose_at(min(t, T_CLOSE_END - 0.01) if t < T_CLOSE_END else 18.0)
    if t >= T_CLOSE_END:
        P = S.stand_pose(t)
        P['ear'] = 0.3
        # idle chewing + looks
        P['jaw'] = 0.18 * (1 + math.sin(2 * math.pi * 2.2 * t))
        ha = horse_amp(t)
        if ha > 0.02: P['jaw'] = max(P['jaw'], min(ha * 1.6, 1.0) * 0.8)
        if BX[1][0] < t < BX[2][0] + 0.5:  # glance down at the bandit
            P['head'] = 0.95; P['neck'] = -0.85
        P['lid'] = 0.55
    else:
        # lip flap for the galloping aside
        if t < S.T_BRAKE:
            ha = horse_amp(t)
            if ha > 0.02: P['jaw'] = min(ha * 1.6, 1.0) * 0.7
    return P, p

def render(t):
    close = S.T_CLOSE <= t < T_CLOSE_END
    camx = S.cam_x(t)
    shake = (int(hsh(int(t * 60)) % 5) - 2, int(hsh(int(t * 60) + 7) % 3) - 1) if S.T_LAND <= t < S.T_LAND + 0.3 else (0, 0)
    bg = S.background(camx, t)
    if close:
        ox, oy = 20, 62
        F = np.repeat(np.repeat(bg[2 * oy:2 * oy + 192, 2 * ox:2 * ox + 108], 2, 0), 2, 1)
        cam = Cam(S.CAMX_STOP + ox, oy, 4.0)
    else:
        F = bg
        cam = Cam(camx - shake[0] * 0.5, -shake[1] * 0.5, 2.0)
    hx = camx + S.HORSE_SX; hy = GROUND - 19
    P, p = horse_pose(t)

    L = Layer(cam)
    wob = 3.0 * math.exp(-(t - S.T_LAND) * 3) * math.sin((t - S.T_LAND) * 18) if t >= S.T_LAND else 0.0
    S.cactus(L, S.CACTUS_WX, GROUND + 2, wob); outline(L, (40, 72, 36)); comp(F, L)
    L = Layer(cam)
    frac = 1 - sm((t - (8.75 + OFF)) / 1.25) if t > 8.75 + OFF else 1.0
    S.carrot(L, S.CARROT_WX, GROUND - 0.5, frac); outline(L, (70, 40, 20)); comp(F, L)

    if not close:
        for t0 in (0.6, 7.4):
            if t0 < t < t0 + 3.6:
                L = Layer(Cam(0, 0, 2.0))
                S.tumbleweed(L, (122 - (t - t0) * 48, GROUND - 3.5 - abs(math.sin((t - t0) * 5)) * 7), -(t * 9)); comp(F, L)

    # horse
    L = Layer(cam)
    T, hs, hd, up = S.draw_horse(L, hx, hy, P, t, p, saddle=True)
    if t >= S.T_HAT:
        pos, rot = S.head_hat_anchor(hx, hy, P); S.hat(L, pos, rot)
    S.draw_ears(L, hs, hd, up, P['ear'])
    outline(L, S.HC['ol']); comp(F, L)

    # cowboy
    L = Layer(cam)
    if t < LINES['c1'] + 6: mouth = S.amp('c1', t - LINES['c1'])
    else: mouth = spk_amp({'n1': (LINES['n1'], 0, 99), 'n5': (LINES['n5'], 0, 99)}, t)
    if 6.3 + OFF < t < 7.5 + OFF: mouth = 1.0
    hatL = None
    if t < S.T_LAUNCH:
        hip = T(-1, -8.4)
        lean = 0.12 + 0.05 * math.sin(2 * math.pi * p + 1)
        if t > S.T_BRAKE: lean = lerp(lean, 0.6, sm((t - S.T_BRAKE) / 0.25))
        S.cowboy(L, hip, P['pitch'] + lean, S.pose_ride(t), True, mouth)
    else:
        P0, _ = S.horse_pose_at(S.T_LAUNCH - 1e-3)
        T0 = S.horse_frames(S.cam_x(S.T_LAUNCH) + S.HORSE_SX, hy, P0)[0]
        L0 = T0(-1, -8.4)
        target = (S.CACTUS_WX + 0.3, GROUND + 2 - 25.2)
        if t < S.T_LAND:
            s = (t - S.T_LAUNCH) / (S.T_LAND - S.T_LAUNCH)
            hip = (lerp(L0[0], target[0], s), lerp(L0[1], target[1], s) - 44 * 4 * s * (1 - s))
            S.cowboy(L, hip, lerp(0.6, 2 * math.pi, s), S.pose_fly(t), False, mouth)
        else:
            a = t - S.T_LAND
            hip = (target[0] + wob * 0.9, target[1] - 3.5 * math.exp(-a * 5) * abs(math.sin(a * 14)))
            shock = 1 - sm((a - 0.6) / 0.8)
            pose = S.pose_sit(t, shock)
            if LINES['n5'] - 0.3 < t < LINES['n5'] + dur('n5') + 0.3:
                pose['narm'] = (1.2, 2.2)  # raises hand weakly while asking
            S.cowboy(L, hip, 0.0, pose, False, mouth)
            for dx, dy in ((-1.2, 0.2), (1.0, -0.4), (0.2, 0.6)):
                dot(L, (hip[0] + dx, hip[1] + dy + 1.5), (250, 246, 220), 0.3)
        if t < S.T_HAT:
            Pl, _ = S.horse_pose_at(S.T_HAT)
            tgt, trot = S.head_hat_anchor(S.HORSE_WX, hy, Pl)
            h0 = (L0[0] + 1, L0[1] - 12)
            s = (t - S.T_LAUNCH) / (S.T_HAT - S.T_LAUNCH)
            hatL = ((lerp(h0[0], tgt[0], s), lerp(h0[1], tgt[1], s) - 58 * 4 * s * (1 - s)), lerp(0.0, trot + 4 * math.pi, s))
    outline(L, S.CC['ol']); comp(F, L)
    if hatL:
        L = Layer(cam); S.hat(L, *hatL); outline(L, S.CC['ol']); comp(F, L)

    if S.T_LAND + 0.1 < t < 9.9 + OFF and not close:
        L = Layer(cam)
        cx_, cy_ = S.CACTUS_WX + 0.9, GROUND + 2 - 25.2 - 13
        for i in range(3):
            a = t * 5 + i * 2 * math.pi / 3
            S.star(L, (cx_ + 5 * math.cos(a), cy_ + 1.6 * math.sin(a)))
        comp(F, L)

    if not close:
        draw_donkey_bandit(F, t)
        S.draw_particles(F, t, 0)
        if 5.8 + OFF <= t < 6.35 + OFF:
            hx_s, hy_s = cam.p(*hs); HDP.bubble_hd(F, hx_s + 6, hy_s - 10)

    big = np.repeat(np.repeat(F, 5, 0), 5, 1)
    if t < 2.6:
        overlay(big, TITLE, 230, 1 - sm((t - 2.1) / 0.5))
    for (a, b, _, _), img in zip(CAPS, CAP_IMG):
        if a <= t < b: overlay(big, img, CAP_Y, min(1.0, (t - a) / 0.08))
    if t >= 37.4:
        k = sm((t - 37.4) / 0.5)
        big[:] = (big.astype(np.float32) * (1 - 0.45 * k)).astype(np.uint8)
        overlay(big, END, 760, k)
    return big

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        ts = list(map(float, sys.argv[2:]))
        c = Image.new('RGB', (270 * len(ts), 480))
        for k, tt in enumerate(ts):
            c.paste(Image.fromarray(render(tt)).resize((270, 480), Image.NEAREST), (k * 270, 0))
        c.save(P.build('ep01', 'sheet.png')); sys.exit()
    n = int(DUR * FPS)
    a0, a1 = (int(sys.argv[2]), int(sys.argv[3])) if len(sys.argv) > 3 and sys.argv[1] == 'seg' else (0, n)
    out = P.build('ep01', f'seg_{a0:04d}.mp4') if a0 or a1 != n else P.build('ep01', 'noaudio.mp4')
    proc = subprocess.Popen(['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '1080x1920', '-r', str(FPS),
                             '-i', '-', '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p',
                             out], stdin=subprocess.PIPE)
    COVER = np.array(Image.open(str(P.episode('ep01') / 'cover.png')).convert('RGB'))
    for i in range(a0, a1):
        if i < 6:  # cover for first 0.2 s
            proc.stdin.write(COVER.tobytes()); continue
        proc.stdin.write(render(i / FPS).tobytes())
        if i % 150 == 0: print(i, flush=True)
    proc.stdin.close(); proc.wait(); print('done')
