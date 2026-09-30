"""Shared kit for the feature cut «Sunny Palms HOA: The Complete Season» (16:9, 1920x1080, 30 fps).
Importing this module switches the engine to wide mode (PV_WIDE=1) — import it FIRST.
  Block(id, beats, ...)  -> sequenced block: voice/SFX timeline built from beats, lip-flap + karaoke captions, render(t)
  scene(...)             -> generic wide shot (bg world + heroes + props), camera lerp
  earl_cu / pip          -> Earl close-up in the pond / picture-in-picture reaction cam
  hud / card / vhs ...   -> overlays"""
import os
os.environ['PV_WIDE'] = '1'
import sys, pathlib, math, json, subprocess, functools
HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / 'engine')); sys.path.insert(0, str(HERE))
import numpy as np
from PIL import Image, ImageDraw
import paths as P
import stage as ST
from stage import Chars, Light, view_at
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import us_cast as U
from props import us_props as UP
from props import uskit as K
from props import bytfx as B

SLUG = 'sunny-palms-hoa'
FPS = 30
W_, H_ = 1920, 1080
COL = dict(K.COL, kevin=(255, 150, 200))
assert (ST.OUT_W, ST.OUT_H) == (W_, H_) and (O.OUT_W, O.OUT_H) == (W_, H_)


# ------------------------------------------------------------------ worlds & light
_WORLD = {}
WFILE = dict(yard='yard', interior='interior', storm='yard_storm', clubhouse='clubhouse', board='board_room', beach='beach')


def world(name):
    if name not in _WORLD:
        _WORLD[name] = ST.ai_world(P.series(SLUG) / 'bg' / f'{WFILE[name]}.png')
    return _WORLD[name]


def light_beach(v):
    return Light(amb=(1.05, 0.98, 0.94), rim=(-1, -0.4, (255, 206, 180), 0.4), grad=(1.05, 0.92))


LIGHT = dict(yard=K.light_yard, interior=K.light_int, storm=K.light_storm, clubhouse=K.light_yard, board=K.light_int, beach=light_beach)
POND = dict(yard=(640.0, 492.0, 11.0), clubhouse=(1040.0, 585.0, 11.0), beach=(760.0, 425.0, 10.0))


# ------------------------------------------------------------------ audio-clip lengths
_LEN = {}


def clip_len(vep, key):
    k = (vep, key)
    if k not in _LEN:
        f = P.series(SLUG) / 'voice' / vep / f'{key}.mp3'
        _LEN[k] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                       capture_output=True, text=True).stdout)
    return _LEN[k]


# ------------------------------------------------------------------ beats -> block
class Ctx:
    """handed to every shot function: lip-flap amplitude per speaker at block time t"""
    def __init__(s, epi): s.epi = epi
    def mouth(s, who, t, k=1.7): return min(1.0, s.epi.talk(who, t) * k)


class Block:
    """beats: list of dicts
         dur   seconds (if omitted: voice length + pad)
         v     (vep, key, speaker, caption)      one voice line, starts at `lead` after the beat start
         lead, pad   seconds (defaults 0.0 / 0.10)
         fn    callable(ctx, t, u, dur) -> frame  (t = block time, u = time in beat)
         sfx   [(path, dt, gain[, in, out])]      dt relative to the beat start
         st    [(text, (fg), size, x, y, dt0, dt1)] stickers
         flash / mosaic  [dt]                     transitions
         cap   caption baseline y (default 960) or None to hide captions in this beat
    beds: [(path, loop_len, t0, t1, gain, duck)] in block time (None t1 = block end)"""
    def __init__(s, bid, beats, beds=(), card=None, hud=True, tail=0.0, chapter=None):
        s.id, s.beats, s.card, s.hud, s.chapter = bid, beats, card, hud, chapter
        t = 0.0
        s.VOICE, s.SFX, s.stickers, s.flashes, s.mosaics, s.FINES = [], [], [], [], [], []
        for b in beats:
            v = b.get('v'); lead = b.get('lead', 0.0)
            d = b.get('dur')
            if d is None: d = lead + clip_len(v[0], v[1]) + b.get('pad', 0.10)
            b['t0'], b['d'] = t, d
            if v: s.VOICE.append((f"{bid}_{len(s.VOICE)}", v[0], v[1], t + lead, 0.0, clip_len(v[0], v[1]), v[2], v[3]))
            for x in b.get('sfx', ()): s.SFX.append((x[0], t + x[1], x[2]) + tuple(x[3:5]))
            for (tx, fg, size, x, y, a, c) in b.get('st', ()): s.stickers.append((O.sticker(tx, fg=fg, size=size), t + a, t + c, x, y))
            if b.get('fines'): s.FINES.append((t + b.get('fines_dt', 0.0), b['fines']))
            for a in b.get('flash', ()): s.flashes.append(t + a)
            for a in b.get('mosaic', ()): s.mosaics.append(t + a)
            t += d
        s.DUR = t + tail
        allb = [(p, ln, a, (s.DUR if c is None else c), g, dk) for (p, ln, a, c, g, dk) in beds]
        s.MUSIC = [b_ for b_ in allb if '/music/' in b_[0]]           # mixed globally (continuous music under the whole film)
        s.BEDS = [b_ for b_ in allb if '/music/' not in b_[0]]        # ambience stays per block
        s.MASTER = 0.78
        s.epi = Episode(f'mv_{bid}', s.VOICE, s.DUR, FPS, colors=COL, slug=SLUG) if s.VOICE else None
        s.ctx = Ctx(s.epi) if s.epi else None
        s.n = int(round(s.DUR * FPS))

    def beat_at(s, t):
        for b in s.beats:
            if b['t0'] <= t < b['t0'] + b['d']: return b
        return s.beats[-1]

    def render(s, t):
        b = s.beat_at(t)
        big = b['fn'](s.ctx, t, t - b['t0'], b['d'])
        for img, a, c, x, y in s.stickers: O.draw_sticker(big, img, t, a, c, x, y)
        cy = b.get('cap', 940)
        if s.epi and cy is not None: s.epi.captions.draw(big, t, cy)
        for fa in s.flashes:
            if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
        for ma in s.mosaics:
            if ma <= t < ma + 0.3: O.mosaic(big, int(lerp(40, 1, (t - ma) / 0.3)))
        return big


# ------------------------------------------------------------------ heroes / scenes
def hero(CH, v, ctx, t, sp):
    """sp: dict(who, x, y=592, u=9.0, flip, pose, expr, look, shades, hand_n, hand_f, prop_n, prop_f, lean, sweat, red, visor, outfit, paint, legs, mute)"""
    who = sp['who']; cam = v.cam(sp['x'], sp.get('y', 592.0), sp.get('u', 9.0), sp.get('flip', False))
    m = 0.0 if sp.get('mute') else (ctx.mouth(who, t) if ctx else 0.0)
    kw = dict(hand_n=sp.get('hand_n'), hand_f=sp.get('hand_f'), prop_n=sp.get('prop_n'), prop_f=sp.get('prop_f'), lean=sp.get('lean', 0.0), sweat=sp.get('sweat', 0.0),
              legs=sp.get('legs', True))
    if who == 'dale':
        U.dale(CH, cam, sp.get('pose') or U.DPOSE['stand'], t, m, sp.get('expr', 'normal'), sp.get('look', 0.0), sp.get('shades', False),
               red=sp.get('red', 0.0), paint=sp.get('paint'), visor=sp.get('visor', False), **kw)
    elif who == 'brenda':
        U.brenda(CH, cam, sp.get('pose') or U.BPOSE['stand'], t, m, sp.get('expr', 'sweet'), sp.get('look', 0.0), outfit=sp.get('outfit', 'polo'),
                 visor=sp.get('visor', True), **kw)
    else:
        raise ValueError(who)


def scene(ctx, t, u, dur, wname, cast, cam, before=None, after=None, vig=0.25, shake=0.0, sx=320, sy=190, post=None, front=None):
    """generic wide shot. cam = (cx, cy, Z) or (cx0, cy0, Z0, cx1, cy1, Z1) (eased over the beat).
    cast: list of hero specs (drawn back to front by feet y); before/after: hooks(CH|big, v, t, u)"""
    if len(cam) == 3: cam = cam + cam
    k = sm(u / max(dur, 1e-3))
    cx, cy, Z = lerp(cam[0], cam[3], k), lerp(cam[1], cam[4], k), lerp(cam[2], cam[5], k)
    ST.set_px(ST.px_for_zoom(Z))
    v = view_at(world(wname), cx, cy, Z, sx, sy)
    big = v.bg()
    light = LIGHT[wname](v)
    if before:
        C0 = Chars(); before(C0, v, t, u); C0.comp(big, light)
    for sp in sorted(cast, key=lambda q: q.get('y', 592.0)):
        C = Chars(); hero(C, v, ctx, t, sp); C.comp(big, light)
    if front:
        C1 = Chars(); front(C1, v, t, u); C1.comp(big, light)
    if after: after(big, v, t, u)
    if post: post(big, t, u)
    if shake: B.shake(big, t, shake, 33)
    fx.vignette(big, vig)
    return big


def earl_cu(ctx, t, u, dur, wname='yard', lid=0.5, Z=2.4, look=(0.0, 0.0), dx=0.0, dy=0.0, zoom=0.05, grin=0.0, stuff=None, chew=0.0, paint=None,
            front=None, mist=0.0, vig=0.25):
    EX, EY, EU = POND[wname]
    Zt = Z + zoom * u
    ST.set_px(ST.px_for_zoom(Zt))
    v = view_at(world(wname), EX + 2.0 * EU + dx, EY - 3.0 * EU + dy, Zt, 320, 200)
    CH, _ = K.begin(Zt)
    big = v.bg()
    m = ctx.mouth('earl', t, 1.6) if ctx else 0.0
    U.earl(CH, v.cam(EX, EY, EU), t, m, lid, look, paint, 0.0, 1.0, True, grin, stuff=stuff, chew=chew)
    if front: front(CH, v)
    CH.comp(big, K.light_pond(v))
    ox, oy = v.opt(EX, EY)
    for k in range(3):                                                        # ripples on the waterline
        ph = (t * 0.5 + k / 3) % 1.0
        rw = int((60 + 300 * ph) * v.Z / 2.6); a = 0.5 * (1 - ph)
        y0 = int(oy) + 4 + k * 3
        x0 = int(ox + 60 - rw); x1 = int(ox + 60 + rw)
        if 0 <= y0 < H_ - 8:
            seg = big[y0:y0 + 6, max(0, x0):min(W_, x1)]
            seg[:] = (seg * (1 - a) + np.array((200, 240, 230)) * a).astype(np.uint8)
    if mist > 0:
        for i in range(10):
            r = np.random.default_rng(i)
            cx = ox + 60 + r.uniform(-260, 260); cy = oy - 90 + r.uniform(-170, 120)
            B.puff(big, cx, cy, 90 + 60 * r.random(), 0.55 * mist, UP.BONE)
    fx.vignette(big, vig)
    return big


def pip(big, frame, corner='br', w=620, k=1.0, label='EARL (grandfathered in)'):
    """picture-in-picture reaction cam: `frame` (1080p) scaled to w px wide with a neon frame in a corner"""
    h = int(w * 9 / 16)
    small = np.array(Image.fromarray(frame).resize((w, h), Image.BOX))
    m = 22
    x0 = W_ - w - 40 if 'r' in corner else 40
    y0 = H_ - h - 150 if 'b' in corner else 130
    box = np.zeros((h + 2 * 10, w + 2 * 10, 4), np.uint8); box[..., :3] = (40, 10, 88); box[..., 3] = 255
    box[4:-4, 4:-4, :3] = (0, 214, 232)
    box[10:-10, 10:-10, :3] = small
    O.overlay(big, box, x0 - 10, y0 - 10, k)
    if label:
        f = O.pfont(20); tag = Image.new('RGBA', (w + 20, 34), (40, 10, 88, 230)); d = ImageDraw.Draw(tag)
        d.text((10, 6), label, font=f, fill=(255, 230, 250))
        O.overlay(big, np.array(tag), x0 - 10, y0 - 10 - 34, k)


def device(portrait, bg, ph=940, tilt=0.0):
    """put a 1080x1920 portrait UI frame on a phone/tablet in front of `bg` (1080p frame, dimmed)"""
    out = (bg.astype(np.float32) * 0.45).astype(np.uint8)
    sh = int(ph); sw = int(sh * 1080 / 1920)
    scr = np.array(Image.fromarray(portrait).resize((sw, sh), Image.BOX))
    fr = np.zeros((sh + 44, sw + 44, 4), np.uint8); fr[..., :3] = (22, 16, 30); fr[..., 3] = 255
    fr[22:-22, 22:-22, :3] = scr
    x0 = (W_ - sw) // 2 - 22; y0 = (H_ - sh) // 2 - 22
    O.overlay(out, fr, x0, y0, 1.0)
    return out


# ------------------------------------------------------------------ text helpers
def ptext(big, text, cx, cy, size, col=(255, 255, 255), outline=(30, 10, 60), anchor='c'):
    f = O.pfont(size); bb = f.getbbox(text); tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = 12
    img = Image.new('RGBA', (tw + 2 * pad, th + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(img); d.fontmode = '1'
    for dx in (-3, 0, 3):
        for dy in (-3, 0, 3):
            if dx or dy: d.text((pad - bb[0] + dx, pad - bb[1] + dy), text, font=f, fill=outline + (255,))
    d.text((pad - bb[0], pad - bb[1]), text, font=f, fill=col + (255,))
    x0 = int(cx - tw / 2 - pad) if anchor == 'c' else int(cx - pad)
    O.overlay(big, np.array(img), x0, int(cy - th / 2 - pad), 1.0)


def dim(big, k):
    big[:] = (big * (1 - k)).astype(np.uint8)


def vhs(big, t, k=1.0):
    """tape look: scanline roll, colour bleed, tracking glitch bars"""
    r = np.random.default_rng(int(t * 30))
    big[::4] = (big[::4] * (1 - 0.25 * k)).astype(np.uint8)
    for _ in range(int(3 + 5 * k)):
        y0 = int(r.integers(0, H_ - 40)); h = int(r.integers(6, 34)); sh = int(r.integers(-160, 160) * k)
        big[y0:y0 + h] = np.roll(big[y0:y0 + h], sh, 1)
    big[:, 6:, 0] = big[:, :-6, 0]
    if k > 0.6:
        y = int((t * 400) % H_); big[y:y + 10] = (big[y:y + 10] * 0.5 + 120).astype(np.uint8)


def crt(big, k=1.0):
    """TV-commercial look: dark rounded corners, scanlines"""
    h, w = big.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = ((xx - w / 2) / (w / 2)) ** 4 + ((yy - h / 2) / (h / 2)) ** 4
    f = big.astype(np.float32) * (1 - 0.55 * k * np.clip(d - 0.55, 0, 1))[..., None]
    f[::4] *= 1 - 0.18 * k
    big[:] = np.clip(f, 0, 255).astype(np.uint8)


def zoom_crop(img, z, cx=0.5, cy=0.5):
    """digital push-in on a finished frame"""
    if z <= 1.0001: return img
    h, w = img.shape[:2]
    ww, hh = int(w / z), int(h / z)
    x0 = int((w - ww) * cx); y0 = int((h - hh) * cy)
    return np.array(Image.fromarray(img[y0:y0 + hh, x0:x0 + ww]).resize((w, h), Image.BOX))


def hit(t, t0, dur=0.35):
    return max(0.0, 1 - (t - t0) / dur) if t >= t0 else 0.0


def J(u, p=1.7, k=0.38):
    """jump-cut punch-in on long shots"""
    return k if int(u / p) % 2 else 0.0
