"""«ЗАМЕЛО! СОБРАНИЕ ЖИЛЬЦОВ» — the season's sitcom movie, 16:9 1920x1080, rendered by shots (timeline.py).
One stage = one cast: on the 9th-floor landing everyone stands at their own place for the whole meeting, the camera only reframes
(continuity like a real sitcom set); listeners look at whoever is talking.
  python3 movie.py prep                       flashback frames from the season finals -> build/zamelo-movie/fb/<ep>/
  python3 movie.py sheet <shot|index> ...     mini sheet of shot middles (build/zamelo-movie/msheet.png)
  python3 movie.py test|frames t ...  |  all [N]      (engine/episode.py CLI)
  python3 mix.py                              -> final_h264.mp4"""
import os
os.environ['PV_WIDE'] = '1'
import sys, pathlib, math, subprocess
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine')); sys.path.insert(0, str(HERE))
import numpy as np
from PIL import Image, ImageDraw
import stage as ST
from stage import OUT_W, OUT_H
from scene import sm, lerp
from cam25 import glide, kick
import overlays as O
import fx
import paths as P
from episode import Episode
from props import zamcast as C
from props import zamkit as K
from props import zampix as ZX
from props import mimic as M
from props import decals as D
from props import rusigns as R
from props.dibspix import blit
from props.zamkit import A
import timeline as TL

assert (OUT_W, OUT_H) == (1920, 1080)
K.DAY = 97
EPI = Episode('movie', TL.VOICE, TL.DUR, TL.FPS, colors=dict(K.COL, disp=(255, 150, 200), nina=(255, 190, 120), tyoma=(150, 230, 255),
                                                             valya=(220, 200, 255), gosha=(200, 255, 140)),
              slug=TL.SLUG, endcard=dict(style='zamelo', lang='ru', sec=3.0, cy=880))
BK = f'{TL.SLUG}-movie'
TAB = (C.XTRA, C.EXPR)
WH = (255, 255, 255)
PAPER, RED, BLUE, INKC = (246, 242, 226), (200, 40, 40), (32, 84, 176), (30, 30, 40)
LS = 0.86                                   # the landing hero scale vs K.WS['landing'] (real size: the door is 2 m)

# ======================================================================================= faces: the speaker's tag -> expression
TAGMAP = [('furious', 'outraged'), ('outraged', 'outraged'), ('exasperated', 'outraged'), ('shouting', 'yelling'), ('hurt', 'offended'),
          ('offended', 'offended'), ('stubborn', 'offended'), ('confused', 'stunned'), ('surprised', 'stunned'), ('stunned', 'stunned'),
          ('stressed', 'nervous'), ('defensive', 'nervous'), ('apologetic', 'nervous'), ('instantly', 'nervous'), ('suspicious', 'squint'),
          ('triumphant', 'proud'), ('proud', 'proud'), ('booming', 'proud'), ('confident', 'proud'), ('narrowing', 'glare'),
          ('smug', 'smug'), ('businesslike', 'smug'), ('calm', 'smug'), ('politician', 'smug'), ('sly', 'sly'), ('whisper', 'sly'),
          ('moved', 'kind'), ('warm', 'kind'), ('touched', 'kind'), ('sweet', 'kind'), ('excited', 'cheerful'), ('eager', 'cheerful'),
          ('cheerful', 'cheerful'), ('carnival', 'cheerful'), ('bored', 'dry'), ('sarcastic', 'dry'), ('deadpan', 'dry'), ('dry', 'dry'),
          ('flat', 'deadpan'), ('strict', 'deadpan'), ('grumbling', 'dry'), ('slowly', 'gloomy'), ('fast', 'proud')]
BASE = dict(zhora='proud', ira='dry', gosha='sly', nina='kind', tyoma='cheerful', valya='deadpan', vitek='cheerful', chayka='dry', disp='dry')


def tag_expr(who, txt):
    tag = txt.split(']')[0].lower()
    for w, e in TAGMAP:
        if w in tag:
            if who == 'gosha' and e == 'kind': return 'sly'
            return e
    return BASE[who]


def _faces():
    keys = {w: [(0.0, BASE[w])] for w in BASE}
    for v in TL.VOICE:
        who = v[6]; txt = TL.LINES[v[2]][1]
        keys[who].append((v[3], tag_expr(who, txt)))
    tw = TL.TWIST
    for w, e in (('zhora', 'shock'), ('gosha', 'shock'), ('nina', 'stunned'), ('vitek', 'stunned'), ('valya', 'stunned'), ('ira', 'dry'),
                 ('tyoma', 'stunned')):
        keys[w].append((tw, e)); keys[w].sort()
    return {w: M.Face(sorted(k), TAB, seed=i * 7 + 3) for i, (w, k) in enumerate(keys.items())}


FACE = _faces()


def mouth(who, t):
    return M.mouth(EPI.talk, who, t)


def speaker(t):
    for v in TL.VOICE:
        if v[3] <= t < v[3] + v[5]: return v[6]
    return None


def face(who, t, base=(0.7, 0.0), **kw):
    m = mouth(who, t)
    F = FACE[who]
    return dict(expr=F.speak(t, m), mouth_=m, blink=F.blink(t), look=F.look(t, base), **kw), M.bob(t, m)


def hat_post(sp):
    if 'head' in sp.anchors: C.ushanka_vitek(sp, sp.anchors['head'])


# ======================================================================================= props
def stool(sp, t=0.0):
    """a kitchen stool (табуретка), ~0.45 m"""
    W = (176, 120, 70)
    sp.sup(0.0, 24.0, 11.0, 2.0, C.tones(W), n=4.0)
    for x in (-8.0, 8.0): C.thin(sp, (x, 22.0), (x * 1.08, 0.0), C.dark(W, 0.8), 1.3)
    C.thin(sp, (-8.4, 8.0), (8.4, 8.0), C.dark(W, 0.8), 0.8)


def jar(sp, h):
    C.caviar(sp, h, empty=False, ladle=False)


def calc(sp, h):
    x, y = h
    sp.sup(x + 1.0, y + 4.0, 3.2, 4.4, C.tones((70, 74, 84)), n=4.0, frost=False)
    sp.sup(x + 1.0, y + 6.6, 2.4, 1.0, C.tones((170, 210, 150)), n=3.0, frost=False)
    for q in range(6): sp.blob(x - 0.4 + (q % 3) * 1.4, y + 3.8 - (q // 3) * 1.6, 0.35, (220, 220, 230))
    sp.ell(x, y, 1.8, 1.7, C.tones(C.MITT), frost=False)


def money(sp, h):
    x, y = h
    for q in range(3): sp.sup(x + 2.0 + q * 0.6, y + 2.0 + q * 0.8, 4.0, 1.6, C.tones((190, 120, 200) if q % 2 else (240, 120, 60)), n=3.0, frost=False)
    sp.ell(x, y, 1.8, 1.7, C.tones(C.MITT), frost=False)


def sandwich(sp, h):
    x, y = h
    sp.sup(x + 2.6, y + 1.6, 3.4, 1.4, C.tones((230, 190, 120)), n=3.0, frost=False)
    sp.sup(x + 2.6, y + 2.4, 3.0, 0.5, C.tones((230, 90, 90)), n=3.0, frost=False, ol=False)
    sp.ell(x, y, 1.8, 1.7, C.tones(C.MITT), frost=False)


def valenok(sp, t=0.0, col=(120, 120, 130)):
    sp.sup(0.0, 8.0, 3.0, 8.0, C.tones(col), n=4.0)
    sp.sup(3.0, 1.6, 5.0, 1.8, C.tones(col), n=3.0)


def courier_box(sp, t=0.0):
    sp.sup(0.0, 9.0, 11.0, 9.0, C.tones((130, 60, 200)), n=6.0)
    sp.txt_box(['ОЗНОБ'], (-9.0, 6.0, 9.0, 12.0), (130, 60, 200), pad=0.3)


def pin_head(fn, kw, S):
    """sprite px of the head anchor (to frame CUs)"""
    with ZX.res(1):
        sp = ZX.Spr(); fn(sp, **kw)
    return sp.anchors.get('head', (0.0, 60.0))


# ======================================================================================= the landing cast (one set, the camera reframes)
POS = dict(zhora=(655.0, 655.0), ira=(560.0, 610.0), gosha=(870.0, 660.0), nina=(320.0, 690.0), tyoma=(445.0, 705.0),
           valya=(985.0, 645.0), vitek=(1175.0, 695.0))
GULL_POS = (190.0, 414.0)
FNS = dict(zhora=C.zhora, ira=C.ira, gosha=C.gosha, nina=C.nina, tyoma=C.tyoma, valya=C.valya, vitek=C.vitek)
HEIGHT = dict(zhora=1.0, ira=0.93, gosha=0.97, nina=0.82, tyoma=0.72, valya=0.9, vitek=0.98)
MEET_END = TL.first('kit_calc')['t0']


def present(who, t):
    f = TL.first
    if who == 'gosha': return t >= f('gosha_jar')['t0']
    if who == 'nina': return t >= f('nina_ladder')['t1']
    if who == 'tyoma': return t >= f('tyoma_slide')['t1']
    if who == 'valya': return t >= TL.line_t('b08') - 0.06
    if who == 'vitek': return t >= f('vitek_hatch')['t0']
    return True


def pose(who, t):
    """per-character hand / prop poses by story beats"""
    f = TL.first
    kw = {}
    vz, vg, va = f('vote_zhora'), f('vote_gosha'), f('vote_all')
    up_z = vz['t0'] + 0.2 <= t < TL.line_t('d04')
    up_g = vg['t0'] + 0.2 <= t < TL.line_t('d07')
    up_all = va['t0'] + 0.1 <= t < TL.line_t('d18')
    if who == 'zhora':
        kw = dict(hand_n=(20.0, 52.0))
        if up_z: kw['hand_n'] = (16.0, 88.0)
        if TL.line_t('c02') <= t < TL.line_t('c03'): kw['hand_n'] = (24.0, 70.0 + 6 * math.sin(t * 6))
    elif who == 'ira':
        kw = dict(hand_n=(16.0, 46.0))
        if up_z: kw['hand_n'] = (14.0, 82.0)
        if f('ring')['t0'] <= t < f('twist')['t1']: kw.update(hand_n=(16.0, 58.0), prop_n=C.phone)
    elif who == 'gosha':
        kw = dict(hand_n=(14.0, 40.0), prop_n=jar)
        if up_g: kw['hand_f'] = (-12.0, 84.0)
        if f('gosha_win')['t0'] <= t < f('twist')['t0']: kw.update(hand_n=(26.0, 66.0), hand_f=(-24.0, 66.0))
        if f('twist')['t0'] + 0.9 <= t: kw.update(hand_n=(-6.0, 36.0))                  # the jar goes behind the back
        if up_all: kw['hand_f'] = (-12.0, 84.0)
    elif who == 'nina':
        if up_g or up_all: kw = dict(hand_n=(10.0, 70.0))
    elif who == 'tyoma':
        kw = dict(sit=1.0)
        if up_z or TL.line_t('d02') <= t < TL.line_t('d04'): kw.update(hand_n=(8.0, 50.0), prop_n=lambda sp, h: C.ledyanka(sp, t))
        if TL.line_t('c03') <= t < TL.line_t('c04'): kw.update(hand_n=(10.0, 40.0), prop_n=C.phone)
        if up_all: kw.update(hand_n=(8.0, 48.0))
    elif who == 'valya':
        kw = dict(hand_n=(14.0, 40.0))
        if up_all: kw['hand_n'] = (12.0, 78.0)
    elif who == 'vitek':
        kw = dict(hand_n=(12.0, 44.0))
        if up_g or up_all: kw['hand_n'] = (10.0, 80.0)
    return kw


def cast(t, v, skip=()):
    """all the meeting's actors on the landing at time t (painter's order: back to front)"""
    S0 = K.S_of(v, 'landing') * LS
    spk = speaker(t)
    acts = []
    for who in ('ira', 'valya', 'gosha', 'zhora', 'vitek', 'nina', 'tyoma'):
        if who in skip or not present(who, t) or t >= MEET_END: continue
        x, y = POS[who]
        if spk and spk in POS and spk != who: base = (0.8 if POS[spk][0] > x else -0.8, 0.0)
        elif spk == 'chayka': base = (-0.8, -0.1)
        else: base = (0.0, -0.1)
        kw, dy = face(who, t, base, **pose(who, t))
        if who == 'vitek': kw['post'] = hat_post
        flip = base[0] < 0 and who not in ('tyoma',)
        yy = y - 24 * 1.1 * S0 / (3 * v.Z) + 2 if who == 'valya' else y
        if who == 'valya' and 'hand_n' in kw and kw['hand_n'][1] < 60: kw.pop('hand_n'); kw['knit'] = 1.0
        a = A(FNS[who], x, yy + dy, S0, t=t, flip=flip, **kw); a.near = 0.99
        acts.append(a)
        if who == 'nina':
            st = A(stool, x + 40, y + 6, S0 * 0.9, t=t); st.near = 0.99; acts.insert(len(acts) - 1, st)
        if who == 'tyoma':
            sl = A(C.ledyanka, x, y + 2, S0 * 0.9, t=t); sl.near = 0.99; acts.insert(len(acts) - 1, sl)
        if who == 'valya':                                                      # the watchwoman sits on her own chair, knitting
            st = A(stool, x, y + 4, S0 * 1.1, t=t); st.near = 0.99; acts.insert(len(acts) - 1, st)
        if who == 'vitek':
            bx = A(courier_box, x + 60, y + 4, S0 * 0.9, t=t); bx.near = 0.99; acts.insert(len(acts) - 1, bx)
    return acts


def gull_act(t, v, peck=0.0, scale=1.0):
    kw, dy = face('chayka', t, (0.6, 0.0))
    g = A(C.chayka, GULL_POS[0], GULL_POS[1] + dy * 0.3 + peck * 6, K.S_of(v, 'landing') * LS * K.GULL * scale, t=t, **kw); g.near = 0.99
    return g


def peck_k(t):
    """the gull bangs the radiator with its beak (its «gavel») at these moments"""
    for tt in [TL.first('gull_bang')['t0'] + 0.1, TL.first('gull_bang')['t0'] + 0.45, TL.line_t('d01'), TL.line_t('d17'),
               TL.first('hall')['t0'], TL.line_t('b20') + 1.0]:
        if 0 <= t - tt < 0.18: return 1.0 - (t - tt) / 0.18
    return 0.0


NOTICE = None


def landing_pre(v, t):
    def pre(big, _v):
        global NOTICE
        if NOTICE is None:
            NOTICE = R.plate(120, 92, ['СОБРАНИЕ ЖИЛЬЦОВ', '19:00', '1. ВЫБОРЫ СТАРШЕГО', 'ПО ДОМУ', '2. РАЗНОЕ (СНЕГ)'],
                             bg=PAPER, fg=INKC, border=(150, 150, 150), colors=[RED, INKC, INKC, INKC, BLUE], weights=[1.2, 1, 0.8, 0.8, 0.8],
                             wear=0.2, tilt=2)
        s = 3 * v.Z / D.WS
        im = np.array(Image.fromarray(NOTICE).resize((max(1, int(NOTICE.shape[1] * s)), max(1, int(NOTICE.shape[0] * s))), Image.LANCZOS))
        ox, oy = v.opt(590.0, 112.0)
        O.overlay(big, im, int(ox), int(oy), 1.0)
    return pre


def landing(t, cx, cy, Z, extra=(), skip=(), fx_=None, focus=0.9, dof_k=8, kick_=(0, 0), gull=True, dark=0.0):
    v = K.V('landing', cx, cy, Z)
    acts = cast(t, v, skip) + list(extra)
    if gull: acts.insert(0, gull_act(t, v, peck_k(t)))
    pre0 = landing_pre(v, t)
    def pre(big, _v):
        pre0(big, _v)
        if dark: big[:] = (big.astype(np.float32) * (1 - dark)).astype(np.uint8)
    return K.shot('landing', K.light_landing, cx, cy, Z, acts=acts, pre=pre, fx_=fx_, t=t, focus=focus, dof_k=dof_k, snow=False,
                  kick=kick_)


def cu_of(who, t, u, Z=1.55, dx=0.0, dy=-0.0, push=0.06, **kw):
    """a medium close-up of a cast member at their place (the head in the upper third), slow push-in"""
    x, y = POS[who] if who != 'chayka' else (GULL_POS[0] + 40, GULL_POS[1] + 120)
    h = 380.0 * LS * HEIGHT.get(who, 1.0)
    Zk = Z * (1 + push * min(1.0, u / 3.0))
    cy = y - h * 0.62 if who != 'chayka' else GULL_POS[1] - 30
    return landing(t, x + dx, cy + dy, Zk, focus=0.95, dof_k=10, **kw)


# ======================================================================================= landing shots
def r_gull_cu(t, s, u):
    n = TL.all_('gull_cu').index(s)
    if n % 2 == 1:                                                              # a wider angle: the chair-gull over the voters' heads
        return landing(t, GULL_POS[0] + 230, GULL_POS[1] + 40, 1.25 * (1 + 0.03 * min(1.0, u / 3)), focus=0.95, dof_k=6,
                       kick_=(0, 4 * peck_k(t)))
    return landing(t, GULL_POS[0] + 70, GULL_POS[1] - 20, 2.3 * (1 + 0.03 * min(1.0, u / 3)), focus=0.95, dof_k=16,
                   kick_=(0, 4 * peck_k(t)), skip=('nina', 'tyoma'))


def r_notice(t, s, u):
    Z = lerp(1.2, 2.2, glide(min(1.0, u / 1.0)))
    return landing(t, 650.0, 170.0, Z, focus=0.9, dof_k=6, skip=('zhora', 'ira'))


def r_door_two(t, s, u):
    return landing(t, 610.0, 420.0, 1.25, focus=0.9, dof_k=8)


def r_ira_door(t, s, u): return cu_of('ira', t, u, 1.6, dx=30)
def r_zhora_cu(t, s, u): return cu_of('zhora', t, u, 1.6)
def r_gosha_cu(t, s, u): return cu_of('gosha', t, u, 1.6)
def r_nina_cu(t, s, u): return cu_of('nina', t, u, 1.6, dx=20)
def r_tyoma_cu(t, s, u): return cu_of('tyoma', t, u, 1.6, dy=30)
def r_valya_cu(t, s, u): return cu_of('valya', t, u, 1.6)
def r_vitek_cu(t, s, u): return cu_of('vitek', t, u, 1.6, dx=-40)


def r_zhora_cam(t, s, u):
    return cu_of('zhora', t, u, 2.2, dy=-30, push=0.12, kick_=kick(t, [(s['t0'] + 0.1, 0.8)]))


def r_zhora_speech(t, s, u):
    return landing(t, 690.0, 400.0, lerp(1.1, 1.35, glide(min(1.0, u / 4.0))), focus=0.9, dof_k=6)


def hatch_figure(fn, t, v, x, y, scale=1.0, flip=False, **kw):
    a = A(fn, x, y, K.S_of(v, 'landing') * LS * scale, t=t, flip=flip, **kw); a.near = 0.99
    return a


def r_gosha_hatch(t, s, u):
    """Гоша climbs half-way down the ladder from the roof hatch, with a thermos"""
    v = K.V('landing', 980.0, 250.0, 1.15)
    kw, dy = face('gosha', t, (-0.8, -0.1), hand_n=(14.0, 44.0), prop_n=C.thermos)
    g = hatch_figure(C.gosha, t, v, 1095.0, 420.0 + dy, flip=True, **kw)
    return landing(t, 980.0, 250.0, 1.15, extra=[g], skip=('gosha',), focus=0.9, dof_k=6)


def r_nina_ladder(t, s, u):
    L = s['t1'] - s['t0']
    k = glide(min(1.0, u / (L * 0.8)))
    v = K.V('landing', 980.0, 420.0, 1.0)
    kw, dy = face('nina', t, (-0.6, 0.0), hand_n=(10.0, 58.0))
    n = hatch_figure(C.nina, t, v, lerp(1110.0, 1010.0, k), lerp(330.0, 640.0, k), 0.82 / 0.82 * 1.0 * HEIGHT['nina'] / 1.0, True, **kw)
    st = hatch_figure(stool, t, v, lerp(1135.0, 1035.0, k), lerp(240.0, 545.0, k), 0.9)
    return landing(t, 980.0, 420.0, 1.0, extra=[n, st], skip=('nina',), focus=0.9, dof_k=6)


def r_tyoma_slide(t, s, u):
    k = min(1.0, u / 0.8)
    v = K.V('landing', 760.0, 400.0, 0.75)
    x = lerp(1150.0, POS['tyoma'][0], k); y = lerp(160.0, POS['tyoma'][1], k) - 260 * math.sin(math.pi * k)
    kw, _ = face('tyoma', t, (-0.9, 0.0), sit=1.0)
    ty = hatch_figure(C.tyoma, t, v, x, y, 1.0, True, **kw)
    sl = hatch_figure(C.ledyanka, t, v, x, y + 2, 0.9, True)
    def f(big, _):
        if k < 1.0: fx.speed_lines(big, t, 0.25)
        ox, oy = v.opt(POS['tyoma'][0], POS['tyoma'][1])
        K.puff(big, ox, oy, t, s['t0'] + 0.8, n=16, seed=5, life=0.5, speed=380, px=10)
    return landing(t, 760.0, 400.0, 0.75, extra=[sl, ty], skip=('tyoma',), fx_=f, focus=0.9, dof_k=4,
                   kick_=kick(t, [(s['t0'] + 0.8, 1.0)]))


def r_gosha_jar(t, s, u):
    return landing(t, 925.0, 420.0, 1.35, focus=0.9, dof_k=8)


def r_valya_two(t, s, u):
    return landing(t, 930.0, 420.0, 1.35, focus=0.9, dof_k=8)


def r_box_drop(t, s, u):
    k = min(1.0, u / 0.35)
    v = K.V('landing', 1060.0, 420.0, 1.0)
    bx = hatch_figure(courier_box, t, v, POS['vitek'][0] + 60, lerp(150.0, POS['vitek'][1] + 4, k * k), 0.9)
    def f(big, _):
        ox, oy = v.opt(POS['vitek'][0] + 60, POS['vitek'][1])
        K.puff(big, ox, oy, t, s['t0'] + 0.35, n=14, col=(200, 200, 210), seed=7, life=0.5, speed=300, px=8)
    return landing(t, 1060.0, 420.0, 1.0, extra=[bx], skip=('vitek',), fx_=f, focus=0.9, dof_k=4,
                   kick_=kick(t, [(s['t0'] + 0.35, 0.8)]))


def r_vitek_hatch(t, s, u):
    return landing(t, 1080.0, 420.0, 1.25, focus=0.9, dof_k=8)


def r_gull_bang(t, s, u):
    return landing(t, GULL_POS[0] + 60, GULL_POS[1] - 10, 2.6, focus=0.95, dof_k=18, kick_=(0, 5 * peck_k(t)))


def r_hall(t, s, u):
    return landing(t, 640.0, 380.0, lerp(0.5, 0.56, u / (s['t1'] - s['t0'])), focus=0.9, dof_k=2)


def r_tyoma_phone(t, s, u):
    return cu_of('tyoma', t, u, 1.8, dy=20)


def r_duel(t, s, u):
    return landing(t, 765.0, 400.0, 1.3, focus=0.9, dof_k=6)


def r_duel_nina(t, s, u):
    return landing(t, 490.0, 420.0, 1.1, focus=0.9, dof_k=6)


def r_vote(t, s, u):
    return landing(t, 640.0, 380.0, 0.52, focus=0.9, dof_k=2)


def r_gosha_win(t, s, u):
    return cu_of('gosha', t, u, 1.5, dy=20)


def r_ring(t, s, u):
    return landing(t, 600.0, 400.0, 1.2, focus=0.9, dof_k=6, kick_=(3 * math.sin(t * 50), 0))


ST_50 = None


def r_twist(t, s, u):
    global ST_50
    Z = lerp(0.62, 0.7, min(1.0, u / 1.6))
    def f(big, _):
        global ST_50
        if ST_50 is None: ST_50 = O.sticker('50 400 ₽', fg=(255, 80, 80), size=110)
        O.draw_sticker(big, ST_50, t, s['t0'] + 0.1, s['t1'] + 3.0, 960, 300)
    return landing(t, 660.0, 400.0, Z, fx_=f, focus=0.9, dof_k=2, kick_=kick(t, [(s['t0'] + 0.05, 1.3)]))


# ======================================================================================= flashbacks: Тёма's phone projects the episode on the wall
FBW, FBH = 486, 864
FB_LABEL = dict(ep01='СЕРИЯ 1 • 27 МЕТРОВ', ep02='СЕРИЯ 2 • СМЕНКА', ep03='СЕРИЯ 3 • ФЛАЖКИ', ep04='СЕРИЯ 4 • ТАКСИ', ep05='СЕРИЯ 5 • ГРЕЙДЕР')


def prep():
    for c in TL.CLIPS:
        dd = pathlib.Path(P.build(BK, f'fb/{c["ep"]}')); dd.mkdir(parents=True, exist_ok=True)
        if len(list(dd.glob('*.png'))) > 10: continue
        src = ROOT / 'series' / TL.SLUG / 'episodes' / c['ep'] / 'final.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-ss', str(c['a']), '-i', str(src), '-t', str(c['b'] - c['a'] + 0.1),
                        '-vf', f'fps=30,scale={FBW}:{FBH}:flags=area', str(dd / '%04d.png')], check=True)
        print(dd)


def fb_frame(ep, i):
    d = pathlib.Path(P.build(BK, f'fb/{ep}'))
    fs = sorted(d.glob('*.png'))
    if not fs: prep(); fs = sorted(d.glob('*.png'))
    return np.array(Image.open(fs[max(0, min(len(fs) - 1, i))]).convert('RGB'))


_LAB = {}


def r_fb(t, s, u):
    lt = u - 0.25
    fr = fb_frame(s['ep'], int(max(0.0, lt) * 30))
    big = landing(t, 640.0, 380.0, 0.52, focus=0.9, dof_k=6, dark=0.0)
    big[:] = (big.astype(np.float32) * 0.38).astype(np.uint8)
    k = sm(u / 0.3)
    x0, y0 = 300, 100
    w = int(FBW * (0.6 + 0.4 * k)); h = int(FBH * (0.6 + 0.4 * k))
    im = np.array(Image.fromarray(fr).resize((w, h), Image.NEAREST))
    xx, yy = x0 + (FBW - w) // 2, y0 + (FBH - h) // 2
    big[yy - 8:yy + h + 8, xx - 8:xx + w + 8] = (250, 250, 240)
    big[yy:yy + h, xx:xx + w] = (im.astype(np.float32) * 0.92 + 14).clip(0, 255).astype(np.uint8)
    # the light cone from Тёма's phone (bottom right) to the picture
    px, py = 1180, 900
    cone = Image.new('L', (OUT_W, OUT_H), 0)
    ImageDraw.Draw(cone).polygon([(px, py), (xx + w, yy), (xx + w, yy + h)], fill=60)
    c = np.array(cone, np.float32)[..., None] / 255.0
    big[:] = np.clip(big.astype(np.float32) * (1 - c * 0.2) + np.array((255, 250, 220), np.float32) * c * 0.6, 0, 255).astype(np.uint8)
    if s['ep'] not in _LAB: _LAB[s['ep']] = O.make_badge(FB_LABEL[s['ep']], 30)
    O.overlay(big, _LAB[s['ep']], 860, 130, 1.0)
    if u < 0.12: O.flash(big, 0.5 * (1 - u / 0.12))
    return big


# ======================================================================================= the УК dispatcher (port booth, the speakerphone)
BOOTH_WIN = (272.0, 360.0, 322.0, 430.0)


def in_rect(big, v, t, win, fn, S, kw, head, anchor, rect_a):
    x0, y0, x1, y1 = win
    a0, b0, a1, b1 = rect_a
    tmp = big.copy()
    with ZX.res(ZX.res_for(S)), ZX.sky_light():
        sp = ZX.Spr(); fn(sp, t=t, **kw); sp.rim(); sp.outline(ZX.INK)
    ox, oy = v.opt(a0 + (a1 - a0) * anchor[0], b0 + (b1 - b0) * anchor[1])
    blit(tmp, sp, ox - head[0] * S, oy + head[1] * S, S, None, False)
    ax, ay = v.opt(x0, y0); bx, by = v.opt(x1, y1)
    ax, ay, bx, by = int(max(0, ax)), int(max(0, ay)), int(min(big.shape[1], bx)), int(min(big.shape[0], by))
    if ax < bx and ay < by: big[ay:by, ax:bx] = tmp[ay:by, ax:bx]


def r_disp(t, s, u):
    Z = lerp(2.4, 2.6, glide(min(1.0, u / 3)))
    cx, cy = 280.0, 398.0
    v = K.V('port', cx, cy, Z)
    S_d = K.WS['port'] * 3 * v.Z * 1.7
    def pre(big, _v):
        kw, _ = face('disp', t, (0.8, 0.0), chew=0.0 if mouth('disp', t) > 0.05 else 1.0)
        x0, y0, x1, y1 = BOOTH_WIN
        in_rect(big, v, t, (x0 - 40, y0 - 50, x1 + 40, y1 + 2), C.disp, S_d, kw, (1.4, 40.0), (0.45, 0.62), BOOTH_WIN)
        ax, ay = v.opt(x0 - 14, y1 - 3); bx, by = v.opt(x1 + 14, y1 + 6)
        big[int(ay):int(by), int(ax):int(bx)] = (96, 70, 56)
        big[int(ay):int(ay) + int(2 * v.Z), int(ax):int(bx)] = (150, 116, 90)
        for q in range(int(ax), int(bx), int(3 * v.Z)):
            h_ = int((2 + 2 * math.sin(q * 0.05)) * v.Z)
            big[max(0, int(ay) - h_):int(ay), q:q + int(3 * v.Z)] = (240, 246, 255)
    def f(big, _):
        if 'p' not in _LAB: _LAB['p'] = O.make_badge('УК «СУГРОБ-СЕРВИС» • ГРОМКАЯ СВЯЗЬ', 26)
        O.overlay(big, _LAB['p'], 1920 - _LAB['p'].shape[1] - 40, 140, 1.0)
    return K.shot('port', K.light_morning, cx, cy, Z, pre=pre, fx_=f, t=t, focus=0.5, dof_k=0, snow_n=50)


# ======================================================================================= the roof (arrivals) + the title
ROOF_PATH = [(470.0, 640.0), (560.0, 540.0), (650.0, 440.0)]


def r_roof(t, s, u):
    L = s['t1'] - s['t0']
    Z = lerp(0.62, 0.72, u / L)
    cx, cy = 640.0, 420.0
    v = K.V('roof', cx, cy, Z)
    S = 2.0 * 3 * v.Z
    acts = []
    for i, (who, fn) in enumerate((('nina', C.nina), ('valya', C.valya), ('vitek', C.vitek), ('tyoma', C.tyoma))):
        k = min(1.0, max(0.0, (u - i * 0.7) / (L - 1.0)))
        x = lerp(ROOF_PATH[0][0] - i * 60, ROOF_PATH[2][0], k); y = lerp(ROOF_PATH[0][1] + i * 20, ROOF_PATH[2][1], k)
        kw = dict(expr=BASE[who], mouth_=0.0, look=(0.6, -0.1))
        if who == 'vitek': kw['post'] = hat_post
        a = A(fn, x, y + 3 * math.sin(t * 9 + i), S * (0.7 + 0.3 * (y - 440) / 260) * HEIGHT[who], t=t, **kw); a.near = 0.99
        acts.append(a)
    def f(big, _): fx.vignette(big, 0.1)
    return K.shot('roof', K.light_morning, cx, cy, Z, acts=acts[::-1], fx_=f, t=t, focus=0.7, dof_k=2, snow_n=70)


TITLE = None


def r_title(t, s, u):
    global TITLE
    v = K.V('roof', 640.0, 360.0, 0.5)
    big = K.shot('roof', K.light_morning, 640.0, 360.0, lerp(0.5, 0.56, u / 3.2), t=t, focus=0.5, dof_k=0, snow_n=90)
    if TITLE is None: TITLE = K.hook_title(['ЗАМЕЛО!', 'СОБРАНИЕ ЖИЛЬЦОВ'], 96)
    k = sm(u / 0.3) * (1 - sm((u - 2.9) / 0.3))
    O.overlay(big, TITLE, 0, 260 + int(30 * (1 - sm(u / 0.4))), k)
    return big


# ======================================================================================= the kitchen (ch. 4)
def kitchen(t, cx, cy, Z, acts, fx_=None, light=None, pre=None, focus=0.9, dof_k=8, kick_=(0, 0)):
    return K.shot('kitchen', light or (lambda v: ST.Light(amb=(1.0, 0.98, 0.96), keys=K._keys(v, [(620, 130, 600, (255, 190, 110), 0.35)]),
                                                         grad=(1.02, 0.96))),
                  cx, cy, Z, acts=acts, pre=pre, fx_=fx_, t=t, focus=focus, dof_k=dof_k, snow=False, kick=kick_)


def zhora_table(t, v, stand=False, **kw):
    S = K.S_of(v, 'kitchen') * 0.95
    k2, dz = face('zhora', t, (-0.8, 0.0), **kw)
    z = A(C.zhora, 760.0, 712.0 + dz, S, t=t, sit=0.0 if stand else 1.0, flip=True, **k2); z.near = 0.99
    return z


def ira_stove(t, v, **kw):
    S = K.S_of(v, 'kitchen') * 0.95
    k2, di = face('ira', t, (0.8, 0.0), **kw)
    a = A(C.ira, 230.0, 712.0 + di, S, t=t, **k2); a.near = 0.99
    return a


def r_kit_calc(t, s, u):
    v = K.V('kitchen', 740.0, 440.0, 1.5)
    return kitchen(t, 740.0, 440.0, 1.5 * (1 + 0.05 * min(1, u / 3)), [zhora_table(t, v, hand_n=(18.0, 50.0), prop_n=calc)])


def r_kit_ira(t, s, u):
    v = K.V('kitchen', 300.0, 440.0, 1.45)
    return kitchen(t, 300.0, 440.0, 1.45, [ira_stove(t, v, hand_n=(18.0, 52.0 + 3 * math.sin(t * 5)))])


def r_kit_idea(t, s, u):
    v = K.V('kitchen', 560.0, 420.0, 0.8)
    up = u > 1.0
    def f(big, _):
        if up:
            if 'idea' not in _LAB: _LAB['idea'] = O.sticker('!', fg=(255, 230, 60), size=120)
            ox, oy = v.opt(770.0, 260.0)
            O.draw_sticker(big, _LAB['idea'], t, s['t0'] + 1.0, s['t1'], int(ox), int(oy))
    return kitchen(t, 560.0, 420.0, 0.8, [ira_stove(t, v), zhora_table(t, v, stand=up, hand_n=(20.0, 80.0) if up else (18.0, 50.0),
                                                                      prop_n=None if up else calc)], fx_=f,
                   kick_=kick(t, [(s['t0'] + 1.0, 0.9)]))


def valenki_acts(t, v, n=8):
    acts = []
    for i in range(n):
        a = A(valenok, 330.0 + i * 70.0 + (i % 2) * 12, 700.0 + (i % 3) * 6, K.S_of(v, 'kitchen') * 1.5, t=t,
              col=[(120, 120, 130), (60, 60, 70), (150, 110, 80), (200, 200, 205)][i % 4]); a.near = 0.99
        acts.append(a)
    return acts


def r_kit_valenki(t, s, u):
    v = K.V('kitchen', 640.0, 400.0, 0.62)
    L = s['t1'] - s['t0']
    walkers = []
    for i, (who, fn) in enumerate((('nina', C.nina), ('valya', C.valya))):
        x = lerp(1180.0, 300.0, min(1.0, max(0.0, (u - i * 0.6) / L)))
        kw = dict(expr=BASE[who], mouth_=mouth(who, t), look=(-0.8, 0.0))
        a = A(fn, x, 690.0 + 3 * math.sin(t * 8 + i), K.S_of(v, 'kitchen') * 0.95 * HEIGHT[who], t=t, flip=True, **kw); a.near = 0.99
        walkers.append(a)
    return kitchen(t, 640.0, 400.0, 0.62, valenki_acts(t, v) + walkers + [ira_stove(t, v, hand_n=(20.0, 76.0))], dof_k=2)


def r_kit_post(t, s, u):
    v = K.V('kitchen', 980.0, 420.0, 1.25)
    S = K.S_of(v, 'kitchen') * 0.95
    k2, dz = face('zhora', t, (-0.8, 0.0), hand_n=(18.0, 52.0), prop_n=money)
    z = A(C.zhora, 1000.0, 712.0 + dz, S, t=t, flip=True, **k2); z.near = 0.99
    return kitchen(t, 980.0, 420.0, 1.25, valenki_acts(t, v, 4) + [z])


# ======================================================================================= the facade (paid window, ch. 4) + night + finale
SIGN = {}


def sign_img(kind):
    if kind not in SIGN:
        if kind == 'pay':
            SIGN[kind] = R.plate(150, 70, ['ВХОД — 100 ₽', 'ПЕНСИОНЕРАМ', 'ТОЖЕ 100'], bg=PAPER, fg=INKC, border=RED,
                                 colors=[RED, INKC, INKC], weights=[1.4, 0.7, 0.7], wear=0.15, tilt=-3)
        else:
            SIGN[kind] = R.plate(170, 70, ['УК', '«ЖОРА-СЕРВИС»'], bg=(30, 70, 150), fg=WH, border=WH, weights=[0.8, 1.2], round_=4)
    return SIGN[kind]


def facade_pre(v, sign=None, sign_k=1.0, night=0.0):
    def pre(big, _v):
        if sign:
            p = sign_img(sign)
            s = 3 * v.Z / D.WS
            im = np.array(Image.fromarray(p).resize((max(1, int(p.shape[1] * s)), max(1, int(p.shape[0] * s))), Image.LANCZOS))
            ox, oy = v.opt(492.0, 112.0)
            O.overlay(big, im, int(ox), int(oy - (1 - sign_k) * 300), 1.0)
        if night:
            f_ = np.array((0.34, 0.38, 0.62), np.float32)
            big[:] = (big.astype(np.float32) * (1 - night + night * f_)).clip(0, 255).astype(np.uint8)
            ax, ay = v.opt(486.0, 160.0); bx, by = v.opt(845.0, 480.0)                         # the lit kitchen window
            reg = big[max(0, int(ay)):int(by), max(0, int(ax)):int(bx)].astype(np.float32)
            big[max(0, int(ay)):int(by), max(0, int(ax)):int(bx)] = np.clip(reg * (1 + 1.4 * night) + np.array((40, 24, 0)) * night, 0, 255
                                                                             ).astype(np.uint8)
    return pre


def zhora_win(t, v, base=(0.8, -0.2), scale=1.0, **kw):
    S = K.S_of(v, 'facade') * scale
    k2, dz = face('zhora', t, base, **kw)
    z = A(C.zhora, 680.0, 640.0 + dz, S, t=t, **k2); z.near = 0.40
    return z


def outside(who, t, v, x, y=650.0, scale=0.62, flip=True, **kw):
    k2, dy = face(who, t, (-0.8, 0.0), **kw)
    if who == 'vitek': k2['post'] = hat_post
    a = A(FNS[who], x, y + dy, K.S_of(v, 'facade') * scale * HEIGHT[who], t=t, flip=flip, **k2); a.near = 0.99
    return a


def facade(t, cx, cy, Z, acts, fx_=None, sign='pay', sign_k=1.0, night=0.0, light=None, snow_n=50, kick_=(0, 0)):
    if night:
        f0 = fx_
        def fx_(big, v_):
            if f0: f0(big, v_)
            big[:] = (big.astype(np.float32) * np.array((0.70, 0.76, 1.0))).clip(0, 255).astype(np.uint8)
            fx.vignette(big, 0.35)
    return K.shot('facade', light or K.light_window, cx, cy, Z, acts=acts, pre=facade_pre(K.V('facade', cx, cy, Z), sign, sign_k, night),
                  fx_=fx_, t=t, focus=0.42, dof_k=10, snow_n=snow_n, kick=kick_)


def r_sign_nail(t, s, u):
    v = K.V('facade', 560.0, 330.0, 1.0)
    k = min(1.0, u / 0.4)
    return facade(t, 560.0, 330.0, 1.0, [zhora_win(t, v, (-0.8, -0.3), hand_f=(-22.0, 70.0 + 8 * abs(math.sin(t * 9))))], sign_k=k,
                  kick_=kick(t, [(s['t0'] + 0.2, 0.6), (s['t0'] + 0.65, 0.6), (s['t0'] + 1.05, 0.6)]))


def r_win_decree(t, s, u):
    v = K.V('facade', 600.0, 360.0, lerp(0.75, 0.9, min(1.0, u / 4)))
    return facade(t, 600.0, 360.0, lerp(0.75, 0.9, min(1.0, u / 4)), [zhora_win(t, v, (0.0, -0.3), hand_n=(24.0, 80.0))])


def r_win_with(who, x=930.0):
    def r(t, s, u):
        v = K.V('facade', 740.0, 330.0, 1.0)
        kw = {}
        if who == 'gosha': kw = dict(hand_n=(16.0, 50.0), prop_n=jar)
        if who == 'vitek': kw = dict(hand_n=(12.0, 50.0))
        if who == 'nina': kw = dict(hand_n=(10.0, 56.0))
        return facade(t, 740.0, 330.0, 1.0, [zhora_win(t, v, (0.8, -0.1), hand_n=(22.0, 56.0), prop_n=money),
                                               outside(who, t, v, x, 528.0, 0.9, **kw)])
    return r


def r_win_zhora(t, s, u):
    v = K.V('facade', 690.0, 360.0, 1.6)
    return facade(t, 690.0, 360.0, 1.6 * (1 + 0.04 * min(1, u / 3)), [zhora_win(t, v, (0.9, -0.1), hand_n=(22.0, 56.0), prop_n=money)])


def r_win_tyoma(t, s, u):
    v = K.V('facade', 330.0, 420.0, 1.2)
    k2, dy = face('tyoma', t, (0.8, 0.0), hand_n=(10.0, 44.0))
    ty = A(C.tyoma, 330.0, 560.0 + dy, K.S_of(v, 'facade') * 0.85, t=t, **k2); ty.near = 0.99
    def f(big, _):
        if 'att' not in _LAB:
            _LAB['att'] = R.plate(110, 50, ['АТТРАКЦИОН', '«ПАПИНО ОКНО»', '30 ₽'], bg=(250, 214, 60), fg=INKC, border=RED,
                                  colors=[RED, INKC, INKC], wear=0.1)
        p = _LAB['att']; s_ = 3 * v.Z / D.WS
        im = np.array(Image.fromarray(p).resize((int(p.shape[1] * s_), int(p.shape[0] * s_)), Image.LANCZOS))
        ox, oy = v.opt(380.0, 430.0)
        O.overlay(big, im, int(ox), int(oy), 1.0)
    return facade(t, 330.0, 420.0, 1.2, [ty], fx_=f)


def night_light(v):
    return ST.Light(amb=(0.55, 0.58, 0.8), keys=K._keys(v, [(680, 380, 380, (255, 190, 110), 0.7)]), grad=(1.0, 0.9))


def r_night_count(t, s, u):
    v = K.V('facade', 680.0, 380.0, 1.6)
    z = zhora_win(t, v, (0.0, -0.4), hand_n=(22.0, 60.0 + 4 * math.sin(t * 6)), prop_n=money)
    return facade(t, 680.0, 380.0, 1.6, [z], night=0.85, light=night_light, snow_n=40)


def r_night_ring(t, s, u):
    v = K.V('facade', 680.0, 380.0, 1.45)
    z = zhora_win(t, v, (0.6, -0.2), hand_n=(18.0, 54.0), prop_n=C.phone)
    return facade(t, 680.0, 380.0, 1.45, [z], night=0.85, light=night_light, snow_n=40, kick_=(3 * math.sin(t * 50), 0))


def r_night_cu(t, s, u):
    v = K.V('facade', 690.0, 360.0, 1.9)
    z = zhora_win(t, v, (0.4, -0.2), hand_n=(18.0, 56.0), prop_n=C.phone)
    return facade(t, 690.0, 360.0, 1.9, [z], night=0.85, light=night_light, snow_n=40)


def r_night_gong(t, s, u):
    v = K.V('facade', 690.0, 360.0, 1.9)
    sc = min(1.0, max(0.0, (u - 0.9) / 0.4))
    z = zhora_win(t, v, (0.0, 0.2), hand_n=(18.0, 40.0), snowcap=sc)
    def f(big, _):
        if 0.9 < u < 1.4:
            ox, oy = v.opt(690.0, 200.0)
            K.puff(big, ox, oy - 120, t, s['t0'] + 0.9, n=26, seed=9, life=0.5, speed=200, px=12)
    return facade(t, 690.0, 360.0, 1.9, [z], fx_=f, night=0.85, light=night_light, snow_n=40, kick_=kick(t, [(s['t0'], 1.0)]))


def r_night_gull(t, s, u):
    v = K.V('facade', 820.0, 430.0, 2.2)
    kw, dy = face('chayka', t, (-0.2, 0.0))
    g = A(C.chayka, 840.0, 486.0 + dy * 0.3, K.WS['facade'] * 3 * v.Z * 0.5, t=t, flip=True, **kw); g.near = 0.62
    return facade(t, 820.0, 430.0, 2.2, [g], night=0.85, light=night_light, snow_n=40)


def fox_acts(t, v, scale=1.0):
    return [zhora_win(t, v, (0.0, -0.3), scale=scale, hat='fox', hand_n=(18.0, 58.0), prop_n=C.phone, hand_f=(-14.0, 50.0), prop_f=sandwich)]


def r_fox_sign(t, s, u):
    v = K.V('facade', 560.0, 330.0, 1.0)
    return facade(t, 560.0, 330.0, 1.0, fox_acts(t, v), sign='uk', sign_k=min(1.0, u / 0.4), light=K.light_morning)


def r_fox_cu(t, s, u):
    v = K.V('facade', 690.0, 360.0, 1.75)
    return facade(t, 690.0, 360.0, 1.75 * (1 + 0.04 * min(1, u / 3)), fox_acts(t, v), sign='uk', light=K.light_morning)


def r_gosha_phone(t, s, u):
    cx, cy, Z = 290.0, 600.0, 2.6
    v = K.V('carfield', cx, cy, Z)
    kw, dy = face('gosha', t, (0.6, 0.0), sit=True, hand_n=(14.0, 58.0), prop_n=C.phone)
    g = A(C.gosha, 262.0, 652.0 + dy * 0.3, K.S_of(v, 'carfield'), t=t, **kw); g.near = 0.99
    return K.shot('carfield', K.light_morning, cx, cy, Z, acts=[g], t=t, focus=0.9, dof_k=18, snow_n=50)


def r_pull_back(t, s, u):
    L = s['t1'] - s['t0'] + 6.0
    Z = lerp(1.3, 0.5, glide(min(1.0, u / 2.0)))
    cx = lerp(690.0, 640.0, glide(min(1.0, u / 2.0)))
    v = K.V('facade', cx, 360.0, Z)
    acts = fox_acts(t, v)
    kw, dy = face('ira', t, (0.8, 0.0), hand_n=(16.0, 50.0))
    ira = A(C.ira, 590.0, 650.0 + dy, K.S_of(v, 'facade') * 0.95, t=t, **kw); ira.near = 0.40
    kc, _ = face('chayka', t, (-0.4, 0.0))
    g = A(C.chayka, 860.0, 488.0, K.WS['facade'] * 3 * v.Z * 0.45, t=t, flip=True, **kc); g.near = 0.62
    return facade(t, cx, 360.0, Z, [ira] + acts + [g], sign='uk', light=K.light_morning, snow_n=80)


def r_end_gull(t, s, u):
    return r_pull_back(t, s, u + 3.0)


def r_end(t, s, u):
    return r_pull_back(t, s, u + 6.0)


# ======================================================================================= dispatcher + overlays
SHOT = dict(gull_cu=r_gull_cu, notice=r_notice, door_two=r_door_two, ira_door=r_ira_door, zhora_cu=r_zhora_cu, gosha_hatch=r_gosha_hatch,
            zhora_cam=r_zhora_cam, title=r_title, roof=r_roof, nina_ladder=r_nina_ladder, nina_cu=r_nina_cu, tyoma_slide=r_tyoma_slide,
            tyoma_cu=r_tyoma_cu, valya_cu=r_valya_cu, gosha_jar=r_gosha_jar, valya_two=r_valya_two, box_drop=r_box_drop,
            vitek_hatch=r_vitek_hatch, vitek_cu=r_vitek_cu, gull_bang=r_gull_bang, hall=r_hall, zhora_speech=r_zhora_speech,
            tyoma_phone=r_tyoma_phone, fb=r_fb, gosha_cu=r_gosha_cu, duel=r_duel, duel_nina=r_duel_nina, vote_zhora=r_vote,
            vote_gosha=r_vote, vote_all=r_vote, gosha_win=r_gosha_win, ring=r_ring, disp=r_disp, twist=r_twist,
            kit_calc=r_kit_calc, kit_ira=r_kit_ira, kit_idea=r_kit_idea, sign_nail=r_sign_nail, win_decree=r_win_decree,
            win_nina=r_win_with('nina', 960.0), win_zhora=r_win_zhora, win_valya=r_win_with('valya', 960.0),
            win_vitek=r_win_with('vitek', 960.0), win_gosha=r_win_with('gosha', 960.0), win_tyoma=r_win_tyoma,
            kit_valenki=r_kit_valenki, kit_post=r_kit_post, night_count=r_night_count, night_ring=r_night_ring, night_cu=r_night_cu,
            night_gong=r_night_gong, night_gull=r_night_gull, fox_sign=r_fox_sign, fox_cu=r_fox_cu, gosha_phone=r_gosha_phone,
            pull_back=r_pull_back, end_gull=r_end_gull, end=r_end)
NOHUD = ('title', 'end', 'fb')
NOCAP = ('title', 'fb')
_HUD = {}


def stickers():
    if 'st' in _LAB: return _LAB['st']
    f = TL.first
    out = [(O.sticker('ВЗЯТКА?!', fg=(255, 90, 90), size=64), TL.line_t('b13'), TL.line_t1('b13') + 0.3, 1560, 150),
           (O.sticker('9 000 ₽ / МЕС', fg=(255, 214, 80), size=58), TL.line_t('b18') + 0.3, TL.line_t1('b18') + 0.3, 1560, 150),
           (O.sticker('ЛОГИСТИКА', fg=(120, 255, 140), size=60), TL.line_t('c11') + 0.2, TL.line_t1('c11') + 0.3, 1560, 150),
           (O.sticker('ЗА ЖОРУ: 2', fg=(255, 214, 80), size=64), f('vote_zhora')['t0'] + 0.3, TL.line_t('d04'), 1560, 150),
           (O.sticker('ЗА ГОШУ: 3', fg=(200, 255, 140), size=64), f('vote_gosha')['t0'] + 0.3, TL.line_t('d09'), 1560, 150),
           (O.sticker('ЕДИНОГЛАСНО', fg=(255, 214, 80), size=70), f('vote_all')['t0'] + 0.2, TL.line_t1('d17'), 1540, 150),
           (O.sticker('50 400 ₽ = ?', fg=(255, 214, 80), size=60), TL.line_t('e01'), TL.line_t1('e01'), 1560, 150),
           (O.sticker('50 400 ₽ ✓', fg=(120, 255, 140), size=70), TL.line_t('e15') + 1.2, TL.line_t1('e15') + 0.3, 1560, 150),
           (O.sticker('ВЫ — УК', fg=(255, 90, 90), size=80), TL.line_t('e18') + 1.2, f('night_gong')['t1'], 1560, 150),
           (O.sticker('ВЕСНОЙ. САМ.', fg=(255, 214, 80), size=64), TL.line_t('e22'), f('pull_back')['t0'] + 0.8, 1560, 150)]
    _LAB['st'] = out
    return out


def hud(big):
    if 'b' not in _HUD:
        im = Image.new('RGBA', (560, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im); d.fontmode = '1'
        d.rounded_rectangle([0, 0, 559, 63], 12, fill=(250, 250, 250, 235)); d.rounded_rectangle([5, 5, 554, 58], 9, fill=(32, 84, 176, 235))
        d.text((22, 21), 'ЗАМЕЛО! • СОБРАНИЕ ЖИЛЬЦОВ', font=O.pfont(20), fill=(255, 255, 255))
        _HUD['b'] = np.array(im)
    O.overlay(big, _HUD['b'], 34, 30, 1.0)


FLASH_AT = ('twist', 'title', 'tyoma_slide', 'fox_sign', 'night_gong')
MOSAIC_AT = ('roof', 'hall', 'kit_calc', 'sign_nail', 'night_count', 'fox_sign')


def render_scene(t):
    s = TL.shot_at(t)
    return SHOT[s['name']](t, s, t - s['t0'])


def render(t):
    s = TL.shot_at(t)
    u = t - s['t0']
    big = render_scene(t)
    for im, t0, t1, cx, cy in stickers(): O.draw_sticker(big, im, t, t0, t1, cx, cy)
    if s['name'] not in NOCAP: EPI.captions.draw(big, t, 930)
    if s['name'] not in NOHUD: hud(big)
    if s['name'] in FLASH_AT and u < 0.15: O.flash(big, 0.6 * (1 - u / 0.15))
    if s['name'] in MOSAIC_AT and u < 0.3: O.mosaic(big, int(lerp(40, 1, u / 0.3)))
    return big


CUTS, NAMES = TL.CUTS, TL.NAMES


def sheet(ids):
    tiles = []
    for x in ids:
        i = int(x) if x.isdigit() else NAMES.index(next(nm for nm in NAMES if nm == x or nm[4:] == x))
        s = TL.SHOTS[i]; tm = (s['t0'] + s['t1']) / 2
        im = Image.fromarray(render(tm)).resize((480, 270), Image.LANCZOS)
        ImageDraw.Draw(im).text((6, 4), f'{NAMES[i]} {tm:.1f}', fill=(255, 255, 0))
        tiles.append(im)
    cols = 3; rows = (len(tiles) + cols - 1) // cols
    sh = Image.new('RGB', (480 * cols, 270 * rows))
    for k, im in enumerate(tiles): sh.paste(im, ((k % cols) * 480, (k // cols) * 270))
    out = P.build(BK, 'msheet.png'); sh.save(out); print(out)


if __name__ == '__main__':
    if sys.argv[1] == 'prep': prep()
    elif sys.argv[1] == 'sheet': sheet(sys.argv[2:])
    else: EPI.main(render, __file__)
