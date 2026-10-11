"""«FLORIDA MAN ON TRIAL» — extended cut, 16:9 1920x1080. One timeline (timeline.py), rendered by shots on the engine v2.
  python3 movie.py test t1 t2 ...  |  frames t ...  |  all  |  shots <i|name> ...      (engine/episode.py CLI)
  python3 mix.py build/florida-man-movie/noaudio.mp4 final.mp4
Exhibits (the six episodes) are read from build/florida-man-epNN/final_noend.mp4 (clean masters without the end card)."""
import os
os.environ['PV_WIDE'] = '1'
import sys, pathlib, math, subprocess
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine')); sys.path.insert(0, str(HERE))
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import Light, view_at, OUT_W, OUT_H
from scene import sm, lerp
import overlays as O
import fx
from episode import Episode
from props import fmpix as FX
from props import fmcast as C
from props import fmkit as K
from props import decals as D
from props import bytfx as B
from props.dibspix import blit
import timeline as TL

assert (OUT_W, OUT_H) == (1920, 1080)
SX, SY = 320, 180
EPI = Episode('movie', TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug='florida-man',
              endcard=dict(style='fm', lang='us', sec=3.0, cy=850))
talk = EPI.talk
A = K.A
COURT = K.world('court')
JAIL = K.world('jail_ext')
S_P = 9.0                                 # people in the courtroom (output px per sprite px at Z=1 -> 2.6 world px per sprite px)


def mouth(who, t, k=1.8):
    return min(1.0, talk(who, t) * k)


def light_court(v):
    return Light(amb=(1.04, 0.96, 0.86), keys=[(*v.opt(130.0, 200.0), 900 * v.Z, (255, 226, 160), 0.35)], rim=(-1, -1, (255, 224, 170), 0.35),
                 grad=(1.04, 0.9))


def light_night(v):
    return Light(amb=(0.66, 0.72, 0.96), keys=[(*v.opt(1040.0, 40.0), 1400 * v.Z, (255, 240, 190), 0.55)], rim=(1, -1, (255, 236, 180), 0.5),
                 grad=(1.0, 0.86))


# ---------------------------------------------------------------- cast placement (world px of the court)
JUDGE = (632.0, 468.0)
WIT = (846.0, 470.0)
FMP = (172.0, 604.0)
MORT = (300.0, 521.0)
DAR = (706.0, 666.0)
JURY = [(980.0, 470.0, 'retiree'), (1036.0, 470.0, 'curlers'), (1092.0, 470.0, 'tank'), (1148.0, 470.0, 'grandpa'), (1204.0, 470.0, 'retiree')]
IGU = (515.0, 474.0)
OCC = dict(bench=(462, 338, 798, 484), witness=(802, 362, 890, 478), jury=(884, 406, 1280, 474), defense=(20, 517, 374, 676),
           pros=(872, 515, 1220, 678))


def occlude(big, bg0, v, names):
    for n in names:
        x0, y0, x1, y1 = OCC[n]
        a = v.opt(x0, y0); b = v.opt(x1, y1)
        X0, Y0, X1, Y1 = (int(np.clip(q, 0, m)) for q, m in ((a[0], OUT_W), (a[1], OUT_H), (b[0], OUT_W), (b[1], OUT_H)))
        if X0 < X1 and Y0 < Y1: big[Y0:Y1, X0:X1] = bg0[Y0:Y1, X0:X1]


def judge(v, t, **kw):
    kw.setdefault('expr', 'chipper'); kw.setdefault('look', (-0.2, -0.2))
    return A(C.tanner, *JUDGE, S_P * v.Z, flip=True, t=t, uniform='judge', jobs=8, mouth_=mouth('tanner', t, 2.0), **kw)


def fm_def(v, t, **kw):
    kw.setdefault('expr', 'zen'); kw.setdefault('look', (0.8, 0.3))
    return A(C.fm, *FMP, S_P * v.Z, t=t, jumpsuit=True, mouth_=mouth('fm', t), **kw)


def mort_tab(v, t, **kw):
    kw.setdefault('expr', 'deadpan'); kw.setdefault('look', (0.8, 0.0))
    return A(C.mort, *MORT, S_P * 0.72 * v.Z, t=t, mouth_=mouth('mort', t), **kw)


def darlene_ais(v, t, x=None, **kw):
    kw.setdefault('expr', 'bored'); kw.setdefault('look', (0.7, -0.2))
    return A(C.darlene, x if x is not None else DAR[0], DAR[1], S_P * 0.95 * v.Z, flip=True, t=t, mouth_=mouth('darlene', t), shadow=0.3, **kw)


def jurors(v, t, expr='content', python=False, look=(0.8, 0.0)):
    out = [A(C.local, x, y + 8, S_P * 1.05 * v.Z, flip=True, t=t + i * 0.37, kind=k, pose='sit', expr=expr, look=look) for i, (x, y, k) in enumerate(JURY)]
    if python:
        out.append(A(C.python, 1250.0, 476.0, S_P * 0.6 * v.Z, flip=True, t=t, pose='coil', tongue=True))
    return out


def court(t, cx, cy, Z, back=(), occ=(), acts=(), fx_=None, blur=0, pre2=None, lt=light_court):
    """a court shot: `back` actors stand behind furniture (`occ` restores it over them), `acts` in front"""
    def pre(big, v):
        if blur: big[:] = K.dof(big, blur)
        bg0 = big.copy()
        L_ = lt(v)
        for b in back: b(big, v, L_)
        occlude(big, bg0, v, occ)
        if pre2: pre2(big, v)
    v = view_at(COURT, cx, cy, Z, SX, SY)
    return K.shot(COURT, lt, cx, cy, Z, acts=list(acts), pre=pre, fx_=fx_, sx=SX, sy=SY), v


def cu(world, fn, t, cx, cy, sc, head, Z=1.35, flip=False, blur=7, extra=(), lt=light_court, fx_=None, **kw):
    """close-up: the sprite head pinned at output point `head`, the background zoomed only Z (<= 1.45) and soft"""
    kw.setdefault('t', t)
    v0 = view_at(world, cx, cy, Z, SX, SY)
    hx, hy = K.wpt(v0, *head)
    a = A(fn, hx, hy, sc, flip=flip, pin='head', **kw)
    def pre(big, v):
        if blur: big[:] = K.dof(big, blur)
    big = K.shot(world, lt, cx, cy, Z, acts=list(extra) + [a], pre=pre, fx_=(lambda b, v: fx_(b, v, a)) if fx_ else None, sx=SX, sy=SY)
    return big, a


# ---------------------------------------------------------------- overlays
_IMG = {}


def img(key, make):
    if key not in _IMG: _IMG[key] = make()
    return _IMG[key]


def hud(big, s):
    O.overlay(big, img('badge', lambda: O.make_badge('FLORIDA MAN: ON TRIAL (ALLEGEDLY)', 26)), 34, 30, 1.0)
    if s['count']:
        p = img(('count', s['count']), lambda: D.plate(64, 16, [f"COUNT {s['count']} OF 6"], bg=(20, 20, 24), fg=(255, 214, 80),
                                                       border=(255, 214, 80), bw=0.6, pad=1.0))
        O.overlay(big, p, OUT_W - p.shape[1] - 34, 34, 1.0)


def count_card(big, s, u):
    a = min(1.0, u / 0.18) * (1 - min(1.0, max(0.0, (u - 1.55) / 0.35)))
    if a <= 0: return
    sh = int((1 - min(1.0, u / 0.3)) ** 2 * 600)
    y0, y1 = 300, 780
    reg = big[y0:y1].astype(np.float32)
    band = np.zeros_like(reg); band[:] = (16, 30, 40)
    tmp = (reg * 0.2 + band * 0.8).astype(np.uint8)
    lab = img(('cl', s['n']), lambda: D.plate(90, 18, [f"COUNT {s['n']}"], bg=(226, 34, 52), fg=(255, 255, 255), border=(255, 255, 255), bw=0.8, pad=1.0))
    O.overlay(tmp, lab, (OUT_W - lab.shape[1]) // 2 - sh, 30, 1.0)
    words = s['title'].split(' ')
    lines, cur = [], ''
    for w in words:
        if len(cur) + len(w) + 1 > 18 and cur: lines.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    lines.append(cur)
    ti = img(('ct', s['n']), lambda: K.hook_title(lines, 78, width=OUT_W, depth=14))
    O.overlay(tmp, ti, sh, 120, 1.0)
    big[y0:y1] = (reg * (1 - a) + tmp.astype(np.float32) * a).astype(np.uint8)


# ---------------------------------------------------------------- exhibits: the episodes on the courtroom screen
class Clip:
    """sequential frame reader of a video segment, scaled; restarts the decoder on a jump"""
    def __init__(s, path, w, h):
        s.path, s.w, s.h, s.p, s.next, s.last = str(ROOT / path), w, h, None, None, None

    def get(s, t):
        fi = int(round(t * TL.FPS))
        if s.p is None or fi != s.next:
            if fi == (s.next or -9) - 1 and s.last is not None: return s.last
            if s.p: s.p.kill()
            s.p = subprocess.Popen(['ffmpeg', '-v', 'error', '-ss', f'{fi / TL.FPS:.4f}', '-i', s.path, '-vf', f'scale={s.w}:{s.h}:flags=area',
                                    '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
            s.next = fi
        buf = s.p.stdout.read(s.w * s.h * 3)
        if len(buf) < s.w * s.h * 3: return s.last if s.last is not None else np.zeros((s.h, s.w, 3), np.uint8)
        s.last = np.frombuffer(buf, np.uint8).reshape(s.h, s.w, 3)
        s.next = fi + 1
        return s.last


_CLIPS = {}
TVW, TVH = 512, 910


def exhibit(t, s):
    e = TL.EXHIBIT[s['n']]
    if s['n'] not in _CLIPS: _CLIPS[s['n']] = Clip(e['src'], TVW, TVH)
    clip = _CLIPS[s['n']]
    u = t - s['t0']
    # courtroom behind, soft and dim; slow push-in
    Z = 0.56 + 0.04 * (u / (s['t1'] - s['t0']))
    v = view_at(COURT, 640, 380, Z, SX, SY)
    big = K.dof(v.bg(), 9)
    big[:] = (big * 0.55).astype(np.uint8)
    # what's on the screen
    if t < s['a1']:
        fr = None
    elif t < s['f0']:
        fr = clip.get(e['p1'][0] + (t - s['a1']))
    elif t < s['a2']:                                              # VHS fast-forward through the middle
        k = (t - s['f0']) / TL.FF
        fr = clip.get(e['p1'][1] + k * (e['p2'][0] - e['p1'][1])).copy()
        fr[::4] = (fr[::4] * 0.5).astype(np.uint8)
        off = int(40 * math.sin(t * 90)); fr[:] = np.roll(fr, off, 1)
    else:
        fr = clip.get(e['p2'][0] + (t - s['a2']))
    # the phone-on-a-cart: black rounded bezel, the vertical video inside
    cx, cy = OUT_W // 2, OUT_H // 2 + 6
    bw, bh = TVW + 36, TVH + 60
    x0, y0 = cx - bw // 2, cy - bh // 2
    big[y0:y0 + bh, x0:x0 + bw] = (20, 20, 26)
    big[y0 + 6:y0 + bh - 6, x0 + 6:x0 + bw - 6] = (36, 36, 44)
    vx, vy = cx - TVW // 2, cy - TVH // 2
    if fr is None:
        noise = np.random.default_rng(int(t * 100)).integers(30, 200, (TVH // 6 + 1, TVW // 6 + 1, 1), dtype=np.uint8)
        big[vy:vy + TVH, vx:vx + TVW] = np.repeat(np.repeat(noise, 6, 0), 6, 1)[:TVH, :TVW]
    else:
        big[vy:vy + TVH, vx:vx + TVW] = fr
    if s['a1'] <= t < s['a1'] + 0.12: O.flash(big, 0.5)
    # left: exhibit plate + count; right: the live court cam (jury reactions, refreshed at 10 fps)
    lab = img(('ex', s['n']), lambda: D.plate(110, 92, [f"EXHIBIT {e['letter']}", '', f"COUNT {s['n']}:"] + _wrap(TL.COUNTS[s['n']], 14),
                                              bg=(246, 240, 220), colors=[(226, 34, 52), (0, 0, 0), (14, 44, 54)] + [(14, 44, 54)] * 4,
                                              border=(90, 60, 20), bw=1.6, pad=3, weights=[1.6, 0.4, 0.9] + [0.9] * 4, wear=0.25, tilt=-3))
    O.overlay(big, lab, 150, 300, 1.0)
    tag = img(('tag', s['n']), lambda: D.sticker('', bg=(255, 214, 40), fg=(20, 20, 24), w=60, h=14, lines=[f"EXHIBIT {e['letter']}"], tilt=-8))
    O.overlay(big, tag, x0 - 40, y0 - 20, 1.0)
    cam = live_cam(t, s)
    cxr, cyr = 1360, 300
    big[cyr - 8:cyr + cam.shape[0] + 8, cxr - 8:cxr + cam.shape[1] + 8] = (20, 20, 26)
    big[cyr:cyr + cam.shape[0], cxr:cxr + cam.shape[1]] = cam
    rec = img('rec', lambda: D.plate(70, 12, ['● LIVE COURT CAM'.replace('●', '*')], bg=(20, 20, 26), fg=(255, 80, 80), border=None, pad=0.5))
    O.overlay(big, rec, cxr, cyr + cam.shape[0] + 14, 1.0)
    return big


def _wrap(txt, n):
    out, cur = [], ''
    for w in txt.split(' '):
        if len(cur) + len(w) + 1 > n and cur: out.append(cur); cur = w
        else: cur = (cur + ' ' + w).strip()
    return out + [cur]


_CAM = {}


def live_cam(t, s):
    """a 420x420 crop of the jury box: watching the exhibit, reacting at the episode's twist"""
    key = (s['n'], int(t * 10))
    if key in _CAM: return _CAM[key]
    tw_glob = s['a2'] + 0.6                                       # the episode's twist plays right after the fast-forward
    expr = 'shock' if tw_glob <= t < tw_glob + 2.0 else 'content'
    big, v = court(t, 1100, 410, 1.6, back=jurors(view_at(COURT, 1100, 410, 1.6, SX, SY), t, expr=expr, python=s['n'] >= 4, look=(-0.8, 0.0)),
                   occ=('jury',))
    cam = big[230:650, 750:1170].copy()
    _CAM.clear(); _CAM[key] = cam
    return cam


# ---------------------------------------------------------------- shots
def shot_render(s, t):
    n = s['name']; u = t - s['t0']; dur = s['t1'] - s['t0']
    if n == 'gavel':
        big, a = cu(COURT, C.tanner, t, 640, 300, 24.0, (1020, 470), expr='angry', uniform='judge', jobs=8, gavel=True,
                    hand_n=(12.0, 64.0 if u < 0.22 else 50.0), look=(0.0, -0.3), flip=True)
        if 0.22 <= u < 0.4: B.shake(big, t, 10, 30)
        return big
    if n in ('bench_cu',):
        return cu(COURT, C.tanner, t, 640, 300, 22.0, (1040, 470), expr='chipper' if u > 0.3 else 'normal', uniform='judge', jobs=8,
                  mouth_=mouth('tanner', t, 2.0), look=(-0.2, -0.1), flip=True)[0]
    if n in ('bench', 'bench_gavel'):
        Z = 1.9
        v = view_at(COURT, 632, 300, Z, SX, SY)
        g = n == 'bench_gavel'
        big, _ = court(t, 632, 300, Z, back=[judge(v, t, gavel=g, hand_n=(12.0, 62.0 if (g and u < 0.15) else 50.0) if g else None),
                                             A(C.iguana, *IGU, S_P * 0.55 * Z, t=t)], occ=('bench', 'witness'))
        if g and 0.15 <= u < 0.32: B.shake(big, t, 8, 30)
        return big
    if n == 'fm_cu':
        return cu(COURT, C.fm, t, 230, 420, 24.0, (820, 470), expr='zen' if s.get('key') != 'e_f1' else 'proud', jumpsuit=True,
                  mouth_=mouth('fm', t), look=(0.6, 0.2))[0]
    if n == 'fm_shriek':
        big = cu(COURT, C.fm, t, 230, 420, 27.0, (820, 520), expr='shriek', jumpsuit=True, mouth_=max(0.6, mouth('fm', t)), sweat=1.0,
                 glasses_drop=min(1.0, u / 0.4), look=(0.0, 0.2))[0]
        if u < 0.5: B.shake(big, t, 10, 33)
        return big
    if n in ('mort_cu', 'mort_gulp', 'mort_stand'):
        kw = dict(expr='smug' if n == 'mort_gulp' else 'deadpan', look=(-0.1, -0.1), cam=True)
        if n == 'mort_gulp': kw.update(lump='sub', gulp=min(1.0, max(0.0, (u - 0.5) / 0.3)))
        if n == 'mort_stand': kw.update(lift=0.6)
        sc = 24.0 if n != 'mort_stand' else lerp(22.0, 27.0, min(1.0, u / max(0.1, dur)))
        return cu(COURT, C.mort, t, 300, 470, sc, (960, 470), mouth_=mouth('mort', t), **kw)[0]
    if n == 'darlene_med':
        Z = 1.9
        v = view_at(COURT, 712, 520, Z, SX, SY)
        return court(t, 712, 520, Z, back=[judge(v, t, expr='normal')], occ=('bench', 'witness'), acts=[darlene_ais(v, t)])[0]
    if n == 'darlene_cu':
        return cu(COURT, C.darlene, t, 760, 430, 21.0, (900, 470), flip=True, expr='bored', mouth_=mouth('darlene', t), look=(0.6, 0.0))[0]
    if n == 'def_two':
        Z = 1.7
        v = view_at(COURT, 240, 455, Z, SX, SY)
        return court(t, 240, 455, Z, back=[fm_def(v, t)], occ=('defense',), acts=[mort_tab(v, t)])[0]
    if n in ('jury', 'jury_python', 'jury_gasp', 'foreman'):
        Z = 1.8
        v = view_at(COURT, 1095, 410, Z, SX, SY)
        expr = 'shock' if n == 'jury_gasp' else 'content'
        big, v = court(t, 1095, 410, Z, back=jurors(v, t, expr=expr, python=(n == 'jury_python' or TL.shot_at(t)['count'] >= 4)), occ=('jury',))
        if n == 'jury_python':
            st = img('j13', lambda: K.st('JUROR #13', (170, 255, 110), 56))
            O.draw_sticker(big, st, u, 0.3, 9.0, 1500, 300)
        if n == 'foreman':
            note = img('note', lambda: D.plate(60, 40, ['WE, THE', 'JURY...'], bg=(250, 248, 238), fg=(20, 20, 24), border=(150, 150, 150), tilt=6))
            O.overlay(big, note, 1080, 420 - int(40 * sm(min(1.0, u / 0.6))), 1.0)
        return big
    if n == 'tv_in':
        Z = 1.5
        v = view_at(COURT, 690, 520, Z, SX, SY)
        x = lerp(980.0, 760.0, sm(min(1.0, u / 1.2)))
        return court(t, 690, 520, Z, back=[judge(v, t, expr='normal')], occ=('bench', 'witness'),
                     acts=[A(C.tv_cart, x - 80, 664, S_P * 1.6 * Z, t=t), darlene_ais(v, t, x=x, walk=t * 8 if u < 1.2 else None)])[0]
    if n == 'witness_tag':
        Z = 2.0
        return court(t, 846, 380, Z, back=[A(C.price_tag, 846, 364, S_P * 0.8 * Z, t=t, cuffed=True)], occ=())[0]
    if n == 'scan':
        Z = 1.5
        v = view_at(COURT, 250, 480, Z, SX, SY)
        big, v = court(t, 250, 480, Z, back=[fm_def(v, t, expr='stunned', look=(0.6, 0.6))], occ=('defense',),
                       acts=[A(C.darlene, 372, 660, S_P * 0.95 * Z, flip=True, t=t, expr='bored', mouth_=mouth('darlene', t),
                               hand_n=(10.0, 48.0), prop_n=lambda sp, h: C.pet_scanner(sp, h))])
        if u < 0.5:
            stb = img('beep', lambda: K.st('BEEP!', (255, 90, 90), 64))
            O.draw_sticker(big, stb, u, 0.0, 0.5, 700, 360)
        return big
    if n == 'witness':
        Z = 1.8
        v = view_at(COURT, 800, 330, Z, SX, SY)
        x = lerp(700.0, WIT[0], sm(min(1.0, u / 0.9)))
        return court(t, 800, 330, Z, back=[A(C.tanner, x, WIT[1], S_P * Z, flip=True, t=t, uniform='judge', jobs=8, expr='nervous',
                                              mouth_=mouth('tanner', t, 2.0), walk=t * 8 if u < 0.9 else None, look=(-0.6, 0.0))],
                     occ=('bench', 'witness'))[0]
    if n == 'witness_cu':
        return cu(COURT, C.tanner, t, 846, 330, 22.0, (1000, 450), flip=True, expr='chipper', uniform='judge', jobs=8, robe_open=1.0,
                  thumbs=True, mouth_=mouth('tanner', t, 2.0), look=(0.0, 0.0))[0]
    if n in ('badges', 'badges2'):
        return badges(t, s, u, n == 'badges2')
    if n == 'iguana':
        Z = 2.2
        stiff = u > 0.6
        fall = max(0.0, (u - 0.9) / 0.3)
        y = IGU[1] + 150 * min(1.0, fall)
        big, v = court(t, 540, 430, Z, back=[A(C.iguana, IGU[0] + 20 * min(1.0, fall), y, S_P * 0.9 * Z, t=t, stiff=stiff,
                                               rot=-90.0 * min(1.0, fall))], occ=())
        if stiff: K.frost_edges(big, 0.6)
        if u > 0.3:
            st = img('brr', lambda: K.st('NOW WITH A/C', (120, 230, 255), 56))
            O.draw_sticker(big, st, u, 0.3, 9.0, 1350, 300)
        return big
    if n == 'cheer':
        big = court(t, 640, 360, 0.5, back=[judge(view_at(COURT, 640, 360, 0.5, SX, SY), t, expr='chipper')] +
                    jurors(view_at(COURT, 640, 360, 0.5, SX, SY), t, expr='cheer' if False else 'content'), occ=('bench', 'jury'),
                    acts=[fm_def(view_at(COURT, 640, 360, 0.5, SX, SY), t, expr='bliss', shaka=True)])[0]
        confetti(big, t, u)
        return big
    if n == 'cuffs':
        big = cu(COURT, C.fm, t, 230, 420, 24.0, (760, 470), expr='zen', jumpsuit=True, look=(0.6, 0.2))[0]
        if u > 0.5: K.punch_card(big, t, s['t0'] + 0.5, 10, cx=1380, cy=560, w=700, punch_t=s['t0'] + 0.8)
        return big
    if n == 'hook':
        big = court(t, 640, 360, 0.5, back=[judge(view_at(COURT, 640, 360, 0.5, SX, SY), t, expr='normal', gavel=True)], occ=('bench',),
                    acts=[fm_def(view_at(COURT, 640, 360, 0.5, SX, SY), t), mort_tab(view_at(COURT, 640, 360, 0.5, SX, SY), t)])[0]
        ti = img('hook', lambda: K.hook_title(['GUILTY OF', 'FLORIDA?!'], 110, width=OUT_W, depth=18))
        O.overlay(big, ti, 0, 230, min(1.0, u / 0.12))
        return big
    if n == 'title':
        v = view_at(COURT, 640, 360, 0.5, SX, SY)
        big = K.dof(v.bg(), 8); big[:] = (big * 0.45).astype(np.uint8)
        ti = img('title', lambda: K.hook_title(['THE STATE OF FLORIDA', 'v. FLORIDA MAN'], 84, width=OUT_W, depth=16))
        k = min(1.0, u / 0.25)
        O.overlay(big, ti, 0, 260, k)
        st = K.allegedly_stamp(56)
        if u > 0.7: O.overlay(big, st, 1180, 600, 1.0)
        tick = img('tick', lambda: D.plate(170, 16, ['6 COUNTS * 1 CROC * 0 SHAME'], bg=(226, 34, 52), fg=(255, 255, 255), border=None, pad=1.0))
        x = int(OUT_W - (u / dur) * (OUT_W + tick.shape[1]))
        O.overlay(big, tick, x, 900, 1.0)
        return big
    if n == 'wide':
        v = view_at(COURT, 640, 360, 0.5, SX, SY)
        return court(t, 640, 360, 0.5, back=[judge(v, t, expr='normal')] + jurors(v, t), occ=('bench', 'jury'),
                     acts=[fm_def(v, t), mort_tab(v, t), darlene_ais(v, t)])[0]
    if n == 'credits':
        return credits(t, u, dur)
    if n in ('snow', 'snow_mort', 'snow_s2'):
        return snow(t, s, u)
    return court(t, 640, 360, 0.5)[0]


def badges(t, s, u, second):
    """insert: Mort lifts the judge's robe — the lanyard with ALL the badges of the season, named one by one"""
    v = view_at(COURT, 846, 330, 1.35, SX, SY)
    big = K.dof(v.bg(), 10); big[:] = (big * 0.5).astype(np.uint8)
    big[60:1020, 560:1360] = (26, 24, 32)                                  # the robe, held open
    big[60:1020, 760:1160] = (34, 56, 112)                                 # the polo underneath
    for x in (930, 990): big[60:300, x - 6:x + 6] = (40, 176, 150)         # lanyard straps
    names = [('COOL-RITE A/C', (40, 120, 200)), ('PUBBIX DELI', (40, 176, 150)), ('SUNSHINE GEN. BILLING', (150, 196, 230)),
             ('DR. PAWS', (255, 140, 60)), ('SUNSURE MUTUAL', (255, 206, 70)), ('SAWGRASS ACRES MGMT', (150, 110, 200)),
             ('FWC PYTHON DESK', (90, 160, 80)), ('JAIL & RESORT', (200, 60, 60)), ('HON. TANNER', (214, 180, 96))]
    dur = s['t1'] - s['t0']
    n_show = (min(4, 1 + int(u / (dur / 4.2))) if not second else min(9, 5 + int(u / (dur / 4.6))))
    for i, (nm, c) in enumerate(names[:n_show]):
        pl = img(('bd', i), lambda nm=nm, c=c, i=i: D.plate(96, 26, [f'JOB #{i + 1}', nm], bg=c, colors=[(20, 20, 24), (255, 255, 255) if sum(c) < 400 else (20, 20, 24)],
                                                        border=(255, 255, 255), bw=0.8, pad=1.2, weights=[0.7, 1.0], tilt=(-3 if i % 2 else 3)))
        col, row = i % 2, i // 2
        x = 520 + col * 460
        y = 90 + row * 190 if i < 8 else 770
        if i == 8: x = 740
        O.overlay(big, pl, x, y, 1.0)
    return big


def confetti(big, t, u):
    r = np.random.default_rng(7)
    for i in range(120):
        x = int(r.uniform(0, OUT_W) + 40 * math.sin(t * 3 + i)); y = int(-60 + (r.uniform(0, 1) * 300 + u * r.uniform(500, 900)) % (OUT_H + 60))
        c = [(255, 86, 160), (40, 196, 196), (255, 214, 40), (120, 230, 120)][i % 4]
        if 0 <= x < OUT_W - 14 and 0 <= y < OUT_H - 8: big[y:y + 8, x:x + 14] = c


def credits(t, u, dur):
    v = view_at(COURT, 640, 360, 0.5, SX, SY)
    big = K.dof(v.bg(), 10); big[:] = (big * 0.25).astype(np.uint8)
    rows = ['FLORIDA MAN: ALLEGEDLY', '', 'FLORIDA MAN .... HIMSELF (ALLEGEDLY)', 'MORT POUCH, ESQ. .... HIS LAWYER', 'DEPUTY DARLENE .... BAILIFF, ALSO DA',
            'TANNER .... JUDGE (JOB #9)', 'THE PYTHON .... JUROR #13', 'THE IGUANA .... STENOGRAPHER (FROZEN)', '', 'NO SUBS WERE HARMED*', '*ONE WAS EATEN']
    pl = img('credits', lambda: D.plate(300, 150, rows, bg=(0, 0, 0), colors=[(255, 214, 80)] + [(240, 240, 240)] * 8 + [(255, 120, 120)] * 2,
                                        border=None, pad=2, weights=[1.4] + [1.0] * 10))
    pl = D.knockout(pl)
    y = int(OUT_H - (u / dur) * (OUT_H + pl.shape[0] * 0.55))
    O.overlay(big, pl, (OUT_W - pl.shape[1]) // 2, y, 1.0)
    return big


def snow(t, s, u):
    Z = 0.8
    v = view_at(JAIL, 640, 360, Z, SX, SY)
    if s['name'] == 'snow_mort':
        big, a = cu(JAIL, C.mort, t, 640, 360, 24.0, (1400, 520), Z=Z, blur=4, lt=light_night, expr='deadpan', mouth_=mouth('mort', t),
                    look=(-0.4, 0.0), cam=True, flip=True)
    else:
        big = K.shot(JAIL, light_night, 640, 360, Z, acts=[], sx=SX, sy=SY)
    tt = t - TL.shot_at(t)['t0'] + (0 if s['name'] == 'snow' else 1.0)
    kinds = ['retiree', 'curlers', 'grandpa', 'retiree', 'curlers']
    for i, k in enumerate(kinds):
        off = abs(i - 2)
        x = -400 + 2400 * ((t - TL.SHOTS[-3]['t0']) / 8.0) - off * 220
        y = 260 + off * 110 + 20 * math.sin(t * 6 + i)
        sp = FX.draw(C.flyer, 12.0, t=t + i * 0.3, kind=k)
        blit(big, sp, x, y, 12.0, None)
    if s['name'] == 'snow_s2':
        ti = img('s2', lambda: K.hook_title(['SEASON 2:', 'SNOWBIRDS'], 96, width=OUT_W, depth=16))
        O.overlay(big, ti, 0, 120, min(1.0, u / 0.15))
    return big


def render(t):
    s = TL.shot_at(t)
    u = t - s['t0']
    if s['kind'] == 'exhibit':
        big = exhibit(t, s)
    elif s['kind'] == 'card':
        v = view_at(COURT, 640, 360, 0.5, SX, SY)
        big = court(t, 640, 360, 0.5, back=[judge(v, t, expr='normal', gavel=True)] + jurors(v, t), occ=('bench', 'jury'),
                    acts=[fm_def(v, t), mort_tab(v, t)])[0]
        count_card(big, s, u)
    else:
        big = shot_render(s, t)
    if s['name'] not in ('title', 'credits') and s['kind'] != 'exhibit':
        EPI.captions.draw(big, t, 960)
    if s['name'] not in ('title', 'credits', 'snow', 'snow_mort', 'snow_s2'):
        hud(big, s)
    if u < 0.1 and s['kind'] != 'exhibit' and s['name'] in ('witness', 'hook', 'cheer'): O.flash(big, 0.6 * (1 - u / 0.1))
    return big


CUTS, NAMES = TL.CUTS, TL.NAMES

if __name__ == '__main__':
    EPI.main(render, __file__)
