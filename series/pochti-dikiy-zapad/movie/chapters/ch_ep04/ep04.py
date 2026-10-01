"""S01E04 «Прокат». First hybrid episode: xAI backgrounds (engine/props/rental.py) + code heroes, light, particles, text.
  python3 ep04.py test 1 5 20   -> build/ep04/sheet.png
  python3 ep04.py all [4]       -> build/ep04/noaudio.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[5] / 'engine'))
import paths as P
import math, subprocess
import numpy as np
from PIL import Image
import stage as ST
from widecam import View, view_at, halves
from stage import Chars, wrect, ell, OUT_W, OUT_H, W, H, UP
import scene as S
from scene import Layer, cap, dot, outline, sm, lerp
import overlays as O
from props import chars as CH_
from props import rental as R
from timeline import DUR, FPS, VOICE

EP = 'ep04'
D = R.build()
EXT, INT = D['ext'], D['int']

# ---------------------------------------------------------------- audio envelopes, captions
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

# ---------------------------------------------------------------- layout (world px of the AI backgrounds)
U_EXT = 6.0
MOL_X = 330.0; BILLY_X0 = 505.0
RIDE_X = 610.0
SAM_X, SAM_HIP, U_SAM = 395.0, 395.0, 8.0
U_BILLY_IN = 11.0
PREM_X, PREM_FEET, U_PREM = 1192.0, 498.0, 4.6

def horse_anchor(x, feet, u): return x, feet - 19 * u

def head_of_horse(x, feet, u, Pz, flip=False):
    ax, ay = horse_anchor(x, feet, u)
    hs = S.horse_frames(1000.0, 1000.0, Pz)[3]
    dx = (hs[0] - 1000.0) * u
    return (ax - dx if flip else ax + dx), ay + (hs[1] - 1000.0) * u

def billy_head(x, feet, u, facing=1):
    return x + 1.0 * u * facing, feet - (CH_.HIP_H + 9.7) * u

# ---------------------------------------------------------------- props drawn by code
MOTES = np.random.default_rng(4).random((70, 3))
def motes(CH, v, t, x0, y0, x1, y1, col=(255, 236, 170)):
    L = Layer(v.wcam())
    for i, (a, b, c) in enumerate(MOTES):
        x = x0 + ((a * (x1 - x0) + t * (6 + 10 * c)) % (x1 - x0))
        y = y0 + ((b * (y1 - y0) + 4 * math.sin(t * 0.8 + i)) % (y1 - y0))
        if (i + int(t * 3)) % 5: dot(L, (x, y), col, 0.6 + 0.6 * c)
    CH.add(L)

def flicker(t): return 0.10 + 0.05 * math.sin(t * 13.0) + 0.04 * math.sin(t * 29.0 + 1.3)

def lantern_light(big, v, t):
    g = ST.sample(v, D['glow_int'])
    big[:] = np.clip(big * (1.0 + flicker(t) * g[..., None]), 0, 255).astype(np.uint8)

def tumbleweed(CH, v, x, y, u, ang):
    L = Layer(v.cam(x, y, u)); S.tumbleweed(L, (1000.0, 1000.0), ang); outline(L, (70, 50, 30)); CH.add(L)

def premium_stage(CH, v, t, k):
    """curtain opens (k 0..1): dark stall + spotlight inside, drapes pulled to the sides"""
    x0, y0, x1, y1 = R.CURTAIN
    L = Layer(v.wcam())
    wrect(L, x0 + 4, y0 + 58, x1 - 4, y1, (58, 36, 22))
    for yy in range(int(y0 + 70), int(y1), 22): wrect(L, x0 + 4, yy, x1 - 4, yy + 2, (44, 26, 16))
    wrect(L, x0 + 4, y1 - 30, x1 - 4, y1, (200, 170, 90))                                      # hay
    ell(L, ((x0 + x1) / 2, y1 - 6), 80, 10, (250, 226, 150))                                   # spotlight pool
    CH.add(L)
    return x0, y0, x1, y1

def drapes(CH, v, k, t):
    x0, y0, x1, y1 = R.CURTAIN
    L = Layer(v.wcam())
    wd = lerp((x1 - x0) / 2, 26, sm(k))
    for side in (0, 1):
        a = x0 if side == 0 else x1 - wd
        wrect(L, a, y0 + 50, a + wd, y1, (150, 28, 34))
        n = max(2, int(wd / 12))
        for i in range(n): wrect(L, a + i * wd / n, y0 + 50, a + i * wd / n + 3, y1, (110, 18, 24))
    wrect(L, x0, y0 + 40, x1, y0 + 60, (120, 20, 26))
    for i in range(10): wrect(L, x0 + i * (x1 - x0) / 10, y0 + 60, x0 + i * (x1 - x0) / 10 + 8, y0 + 68, (230, 190, 80))
    outline(L, (40, 10, 10)); CH.add(L)
    if k > 0.3:                                                                                 # sparkles
        L = Layer(v.wcam())
        for i in range(9):
            a = i * 0.7 + t * 2
            x = (x0 + x1) / 2 + 80 * math.cos(a); y = (y0 + y1) / 2 + 120 * math.sin(a * 1.3)
            s = 2 + 2 * abs(math.sin(t * 6 + i))
            cap(L, (x - s, y), (x + s, y), 0.8, 0.8, (255, 250, 200)); cap(L, (x, y - s), (x, y + s), 0.8, 0.8, (255, 250, 200))
        CH.add(L)

def contract(CH, v, t, t0, length):
    """fine-print contract unrolling from the counter"""
    L = Layer(v.wcam())
    x = 300.0; y = R.COUNTER_TOP - 4
    ln = length * sm((t - t0) / 1.5)
    wrect(L, x - 22, y, x + 22, y + ln, (240, 228, 196))
    for k in range(int(ln / 5)):
        wrect(L, x - 17, y + 4 + k * 5, x + 17 - (k * 7) % 12, y + 5 + k * 5, (120, 100, 80))
    outline(L, (60, 44, 30)); CH.add(L)

def stamp_mark(CH, v, t):
    if t < 37.2: return
    L = Layer(v.wcam())
    k = min(1.0, (t - 37.2) / 0.08)
    wrect(L, 280, 388, 320 + 0 * k, 408, (190, 30, 30)); wrect(L, 284, 392, 316, 404, (240, 228, 196))
    wrect(L, 288, 396, 312, 400, (190, 30, 30))
    CH.add(L)

def name_tag(CH, cam, rot=0.03):
    HP = CH_.HPf(rot)
    L = Layer(cam)
    a = HP(0.9, 5.4); b = HP(2.6, 4.4)
    wrect(L, a[0], a[1], b[0], b[1], (240, 232, 210)); CH.add(L)
    if cam.sc > 16:
        (sx, sy) = cam.p(*HP(1.75, 4.9))
        px_small(CH, 'СЭМЮЭЛЬ', sx, sy, 8, (60, 30, 30))

def px_small(CH, txt, cx, cy, size, col):
    from PIL import ImageDraw
    f = O.pfont(size); bb = f.getbbox(txt); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    img = Image.new('L', (tw + 4, th + 4), 0); d = ImageDraw.Draw(img); d.fontmode = '1'
    d.text((2 - bb[0], 2 - bb[1]), txt, font=f, fill=255)
    m = np.array(img) > 127; ys, xs = np.nonzero(m)
    yy = ys + int(cy - th / 2) - 2; xx = xs + int(cx - tw / 2) - 2
    ok = (yy >= 0) & (yy < H) & (xx >= 0) & (xx < W)
    CH.col[yy[ok], xx[ok]] = col; CH.m[yy[ok], xx[ok]] = True

# ---------------------------------------------------------------- scene builders
def mol_pose(t, chew=False):
    return CH_.molniya_pose(t, chew, talk('molniya', t))

def ext_scene(CH, v, t, name):
    """exterior: Molniya + Billy (standing / stomping / riding)"""
    if t < 37.2:
        Pz = mol_pose(t, chew=True)
        ax, ay = horse_anchor(MOL_X, R.EXT_FEET, U_EXT)
        CH_.molniya(CH, v.cam(ax, ay, U_EXT), t, Pz, carrot=True)
        if t < 7.05:
            bx, feet, u = BILLY_X0, R.EXT_FEET + 6, U_EXT
            CH_.billy(CH, v.cam(bx, feet - CH_.HIP_H * u, u, True), CH_.POSES['angry'], 0.05, talk('billy', t), 'angry', red=0.5)
        elif t < 8.3:
            k = (t - 7.05) / 1.25
            bx = lerp(BILLY_X0, 585, k); feet = lerp(R.EXT_FEET + 6, 500, k); u = lerp(U_EXT, 4.6, k)
            CH_.billy(CH, v.cam(bx, feet - CH_.HIP_H * u, u), CH_.stomp_pose(t), 0.12, 0.0, 'angry', red=0.4)
    else:
        Pz = mol_pose(t, chew=t > 43.3)
        ax, ay = horse_anchor(RIDE_X, R.EXT_FEET, U_EXT)
        drop = (t - 40.0) if t >= 40.0 else None
        pose = CH_.POSES['ride_whip'] if 38.0 <= t < 39.6 else CH_.POSES['ride']
        CH_.molniya(CH, v.cam(ax, ay, U_EXT), t, Pz, carrot=t > 43.3, disguise=1.0, stache_drop=drop,
                    rider=CH_.rider_billy(pose, talk('billy', t)))
        if 39.6 <= t < 41.6:
            u = t - 39.6
            tumbleweed(CH, v, 380 + 260 * u, R.EXT_FEET - 10 - 8 * abs(math.sin(u * 7)), 5.0, u * 8)

def int_scene(CH, big, v, t, billy=None, sam_kw=None, stalls=True, prem_k=0.0):
    # Sam behind the counter (glasses), then counter occluder
    kw = dict(pose=CH_.POSES['counter'], mouth=talk('sam', t), glasses=True)
    if sam_kw: kw.update(sam_kw)
    CH_.sam(CH, v.cam(SAM_X, SAM_HIP, U_SAM, True), **kw)
    if stalls:
        CH_.donkey(CH, v.cam(612, 500 - 19 * 7.5, 7.5), t, bray=0.0)
        CH_.rocking_horse(CH, v.cam(905, 548, 8.0, True), 0.18 * math.sin(t * 3))
    CH.comp(big)
    ST.blit_world(big, v, D['counter'], 0, 334)
    ST.blit_world(big, v, D['gate_eco'], R.STALL_ECO[0], R.GATE_Y[0])
    if prem_k > 0:
        premium_stage(CH, v, t, prem_k)
        Pz = CH_.molniya_pose(t, False, talk('molniya', t))
        ax, ay = horse_anchor(PREM_X, PREM_FEET, U_PREM)
        CH_.molniya(CH, v.cam(ax, ay, U_PREM, True), t, Pz, disguise=1.0)
        drapes(CH, v, prem_k, t)
    motes(CH, v, t, 60, 160, 340, 430)
    if billy: billy(CH)
    CH.comp(big)
    lantern_light(big, v, t)


def billy_in(x, feet, u, facing, pose, expr, t):
    return lambda CH: CH_.billy(CH, ST_view[0].cam(x, feet - CH_.HIP_H * u, u, facing < 0), pose, 0.05, talk('billy', t), expr)

ST_view = [None]

SHOTS = [
    (0.00, 2.00, 'cu_billy_ext'), (2.00, 3.90, 'two_ext'), (3.90, 5.60, 'cu_mol_ext'), (5.60, 7.05, 'two_ext'), (7.05, 8.40, 'wide_ext'),
    (8.40, 11.15, 'wide_int'), (11.15, 13.30, 'board'), (13.30, 16.00, 'cu_sam'), (16.00, 17.80, 'cu_billy_int'),
    (17.80, 19.60, 'cu_sam_sweat'), (19.60, 21.30, 'two_int'), (21.30, 23.30, 'cu_sam_tag'), (23.30, 26.35, 'split_stalls'),
    (26.35, 27.40, 'premium'), (27.40, 29.60, 'cu_billy_amazed'), (29.60, 31.80, 'cu_prem'), (31.80, 34.50, 'cu_sam_fine'),
    (34.50, 37.20, 'contract'), (37.20, 39.60, 'ride'), (39.60, 41.60, 'cu_mol_ride'), (41.60, 43.30, 'cu_mol_cam'),
    (43.30, DUR + 1, 'cu_billy_red'),
]
FLASH_AT = [0.0, 8.4, 26.35, 37.2]

def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def render_scene(t):
    a, b, name = shot_at(t); u = t - a; CH = Chars()
    if name.endswith('_ext') or name in ('ride', 'cu_mol_ride', 'cu_mol_cam', 'cu_billy_red'):
        if name == 'cu_billy_ext':
            hx, hy = billy_head(BILLY_X0, R.EXT_FEET + 6, U_EXT, -1)
            sh = 3 * math.exp(-u * 6) * math.sin(u * 60)
            v = view_at(EXT, hx + sh, hy, 4.4 - 0.2 * u, 180, 420)
        elif name == 'two_ext':
            v = view_at(EXT, 392, 520, 1.9 + 0.05 * u, 180, 420)
        elif name == 'cu_mol_ext':
            hx, hy = head_of_horse(MOL_X, R.EXT_FEET, U_EXT, mol_pose(t))
            v = view_at(EXT, hx + 4 * U_EXT, hy + 2 * U_EXT, 3.0 + 0.08 * u, 180, 430)
        elif name == 'wide_ext':
            v = View(EXT, 330 + 90 * sm(u / 1.3), 80, 1.0 + 0.04 * u)
        elif name == 'ride':
            v = view_at(EXT, RIDE_X + 10, 470, 1.55 + 0.05 * u, 180, 420)
        elif name in ('cu_mol_ride', 'cu_mol_cam'):
            hx, hy = head_of_horse(RIDE_X, R.EXT_FEET, U_EXT, mol_pose(t))
            v = view_at(EXT, hx + 3 * U_EXT, hy + 3 * U_EXT, 2.7 + 0.1 * u, 180, 440)
        else:  # cu_billy_red: rider close-up
            ax, ay = horse_anchor(RIDE_X, R.EXT_FEET, U_EXT)
            v = view_at(EXT, ax - 1 * U_EXT, ay - 17.5 * U_EXT, 3.2 + 0.15 * u, 180, 440)
        big = v.bg()
        ext_scene(CH, v, t, name)
        if name == 'cu_billy_red':
            CH.col[:] = 0; CH.m[:] = False
            ax, ay = horse_anchor(RIDE_X, R.EXT_FEET, U_EXT)
            Pz = mol_pose(t)
            CH_.molniya(CH, v.cam(ax, ay, U_EXT), t, Pz, carrot=True, disguise=1.0, stache_drop=3.0,
                        rider=lambda L, T: None)
            T = S.horse_frames(1000.0, 1000.0, Pz)[0]; hip = T(-1.0, -9.4)
            CH_.billy(CH, v.cam(ax + (hip[0] - 1000) * U_EXT, ay + (hip[1] - 1000) * U_EXT, U_EXT), CH_.POSES['ride'], 0.05,
                      0.0, 'angry', red=min(1.0, u / 0.8))
        motes(CH, v, t, 0, 420, 1280, 700, (236, 200, 150))
        CH.comp(big)
    elif name == 'split_stalls':
        v1 = view_at(INT, 660, 300, 2.3, 180, 190, hlog=320)
        v2 = view_at(INT, 905, 470, 2.6, 180, 190, hlog=320)
        top = v1.bg(); bot = v2.bg()
        # top: economy donkey braying
        CH_.donkey(CH, v1.cam(612, 500 - 19 * 7.5, 7.5), t, bray=sm(u / 0.2) * (1 - sm((u - 1.3) / 0.3)))
        CH.comp(top); ST.blit_world(top, v1, D['gate_eco'], R.STALL_ECO[0], R.GATE_Y[0])
        CH_.rocking_horse(CH, v2.cam(905, 548, 8.0, True), 0.35 * math.sin(u * 5))
        CH.comp(bot)
        big = halves([top, bot])
        lantern_light(big, v1, t)
        big[:, 954:966] = (30, 18, 12)
    else:
        if name == 'wide_int':
            v = View(INT, 196 + 8 * u, 80, 1.0 + 0.03 * u)
        elif name == 'board':
            v = view_at(INT, 250 + 14 * u, 232, 2.5, 180, 330)
        elif name in ('cu_sam', 'cu_sam_sweat', 'cu_sam_tag', 'cu_sam_fine'):
            hx, hy = SAM_X - 1.2 * U_SAM, SAM_HIP - 9.7 * U_SAM
            Z = 3.1 + 0.08 * u if name != 'cu_sam_fine' else 2.4
            v = view_at(INT, hx, hy, Z, 180, 420 if name != 'cu_sam_fine' else 300)
        elif name in ('cu_billy_int', 'cu_billy_amazed'):
            fx = 505.0 if name == 'cu_billy_int' else 860.0
            hx, hy = billy_head(fx, R.INT_FEET, U_BILLY_IN, -1 if name == 'cu_billy_int' else 1)
            v = view_at(INT, hx, hy, 2.9 + 0.08 * u, 180, 430)
        elif name == 'two_int':
            v = view_at(INT, 470, 420, 1.55, 180, 400)
        elif name == 'premium':
            v = view_at(INT, 1160, 330, 1.75, 180, 360)
        elif name == 'cu_prem':
            hx, hy = head_of_horse(PREM_X, PREM_FEET, U_PREM, CH_.molniya_pose(t), flip=True)
            v = view_at(INT, hx - 3 * U_PREM, hy + 2 * U_PREM, 3.0, 180, 430)
        else:  # contract insert
            v = view_at(INT, 300, 392, 4.2, 180, 380)
        ST_view[0] = v
        billy_fn = None
        if name in ('wide_int', 'two_int', 'cu_billy_int'):
            billy_fn = billy_in(505, R.INT_FEET, U_BILLY_IN, -1, CH_.POSES['hips'] if name != 'cu_billy_int' else CH_.POSES['lean'],
                                'sly' if name != 'wide_int' else 'normal', t)
        elif name in ('cu_billy_amazed', 'premium', 'cu_prem'):
            billy_fn = billy_in(860, R.INT_FEET, U_BILLY_IN, 1, CH_.POSES['excited'], 'amazed', t) if name == 'cu_billy_amazed' else None
        sam_kw = dict(sweat=name in ('cu_sam_sweat', 'cu_sam_tag'),
                      pose=CH_.POSES['present'] if name in ('cu_sam', 'premium') else CH_.POSES['counter'])
        prem_k = 0.0
        if t >= 26.35: prem_k = min(1.0, (t - 26.35) / 0.5)
        big = v.bg()
        int_scene(CH, big, v, t, billy_fn, sam_kw, prem_k=prem_k)
        if name == 'cu_sam_tag':
            name_tag(CH, v.cam(SAM_X, SAM_HIP, U_SAM, True)); CH.comp(big)
        if name in ('cu_sam_fine', 'contract'):
            contract(CH, v, t, 31.9, 120 if name == 'cu_sam_fine' else 160)
            stamp_mark(CH, v, t); CH.comp(big)
        if name == 'contract' and t >= 37.1:
            sh = int(10 * math.exp(-(t - 37.2) * 12) * math.sin((t - 37.2) * 70)); big[:] = np.roll(big, sh, 0)
    return big


# ---------------------------------------------------------------- overlays
BADGE = O.make_badge('СЕЗОН 1 • СЕРИЯ 4/6')
HOOK = O.pixel_title(['ЛОШАДЬ', 'УВОЛЕНА'], 64)
TEASE = O.pixel_title(['СЕРИЯ 5 СКОРО'], 40)
import wideov as WO
DAY, INCOME = 620, (22, 30, 7.0)                        # HUD of the feature cut: (before, after, bump time)
STICKERS = [
    (O.sticker('1$', size=80), 23.45, 24.9, 480, 280),
    (O.sticker('3$', size=80), 24.85, 26.3, 1440, 280),
    (O.sticker('5$', size=96), 26.6, 27.4, 960, 300),
    (O.sticker('АВТОПРОДЛЕНИЕ', fg=(255, 120, 90), size=48), 37.2, 38.9, 960, 300),
]


def render(t):
    big = render_scene(t)
    WO.stickers(big, STICKERS, t)
    WO.hud(big, t, DAY, INCOME[1] if t >= INCOME[2] else INCOME[0])
    CAPTIONS.draw(big, t, WO.CAP_Y)
    for fa in FLASH_AT:
        if fa <= t < fa + 0.15: O.flash(big, 0.75 * (1 - (t - fa) / 0.15))
    if 23.30 <= t < 23.55: O.mosaic(big, int(lerp(40, 1, (t - 23.30) / 0.25)))
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
