"""S01E03 «AURA FARMING?!» — Kayden: «aura farming means acting cool without trying; my friends are coming, PLEASE don't». Doug: «I
INVENTED acting cool». Shades on, «Sup, boys. Just grilling. Like a LEGEND», flips a burger — it never comes back; he backs away for a
cool exit — straight into the pool. «Nobody saw that. We're FINE.» TWIST (55 %, «the network sees everything»): the neighbour's camera
(blinking since the first shot, «SMILE! YOU'RE ON CAMERA») posted it — two million views, «Grill Dad Falls In is TRENDING». MIRRA from
the patio speaker: «Plus nine hundred. The internet LOVES a fall.» Button: «HA! I've still GOT it!» — and he sinks.
  python3 ep03.py test 1 5 20 | frames t… | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
import stage as ST
from stage import view_at
from scene import Layer, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import folk as F
from props import bytfx as B
from props import decals as D
from props import auracast as A
from props import aurakit as K
import timeline as TL

EPI = Episode(TL.EP, TL.VOICE, TL.DUR, TL.FPS, colors=K.COL, slug=TL.SLUG,
              endcard=dict(style='auradad', lang='us', promise='TOMORROW: THE NEIGHBOR'))
talk = EPI.talk
W = K.build(names=['kitchen', 'bathroom', 'backyard'])
K.decorate(W)
K.decorate_yard(W['backyard'])
YARD = W['backyard']
CUTS, NAMES = TL.CUTS, TL.NAMES
F0 = TL.T0

DOUG = (400.0, 610.0, 11.0)          # Doug on the patio, facing left (towards the boys), the pool behind him
KAY = (250.0, 640.0, 11.4)           # Kayden, facing right
BOYS = [(150.0, 652.0, 11.2), (80.0, 668.0, 11.6)]
POOL_W = 476.0                       # waterline (world y) where Doug floats
PDOUG_X = 600.0


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def face(v, cam, r, ru=3.2):
    K.logface(v, cam, r['head'], ru)


def u2w(v, cam, pt):
    x, y = cam.p(*pt)
    k = ST.PX[0]
    return v.X0 + x * k / v.Z, v.Y0 + (y * k - v.oy) / v.Z


def spatula(L, h):
    F.cap(L, h, (h[0] + 2.4, h[1] - 1.6), 0.18, 0.18, (40, 40, 46))
    F.poly(L, [(h[0] + 2.2, h[1] - 1.2), (h[0] + 3.6, h[1] - 2.0), (h[0] + 3.2, h[1] - 2.8), (h[0] + 1.8, h[1] - 2.0)], (200, 204, 214))


def yard(v, t, draw=None, after=None, water=None, cam_k=1.0):
    CH, FX = K.begin()
    big = v.bg()
    B.steam(big, v, t, 110, 300, n=4, rise=80, size=24, a=0.35)                                        # grill smoke
    if draw: draw(CH, v)
    L = Layer(K.fgcam(v, 0.45)); K.fg_plant(L, 1240, 800, 1.2, pot=(200, 96, 60)); F.outline(L, A.OL); CH.add(L)
    CH.comp(big, K.light_yard(v))
    if water: water(big, v)
    K.cam_blink(big, v, t, cam_k)
    fx.motes(FX, v, t, 300, 120, 1200, 420, n=20, col=(255, 236, 190), seed=11)
    if after: after(FX, v)
    FX.comp(big)
    fx.vignette(big, 0.2)
    return big


def doug_at(CH, v, t, pos, k=1.0, flip=True, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un * k, flip=flip)
    kw.setdefault('expr', 'normal')
    if 'mouth_' not in kw: kw['mouth_'] = mouth('doug', t)
    r = A.doug(CH, cam, t=t, **kw)
    face(v, cam, r, 3.4)
    return cam, r


def kid(CH, v, t, pos, who='kayden', pal=None, k=1.0, flip=False, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un * k, flip=flip)
    kw.setdefault('expr', 'bored')
    r = A.kayden(CH, cam, t=t, mouth_=mouth(who, t), pal=pal, **kw)
    face(v, cam, r, 2.8)
    return cam, r


def boys(CH, v, t, expr='bored', phones=False):
    for i, pos in enumerate(BOYS):
        kid(CH, v, t + i * 0.7, pos, 'jaxon' if i == 0 else 'none', A.FRIEND_PALS[i], expr=expr,
            pose=A.KPOSE['look'] if phones else A.KPOSE['stand'], prop_n=A.phone if phones else None)


def pool_doug(x, wl, un):
    """occluder hiding Doug's body below the waterline: the pool water of the background itself, drawn over him"""
    return K.occluder(YARD, [(x - 90, wl), (x + 90, wl), (x + 90, wl + 260), (x - 90, wl + 260)], ('pool', int(x), int(wl)))


def ripples(big, v, t, x, wl, w=70):
    for i in range(3):
        k = ((t * 0.8 + i / 3) % 1.0)
        cx, cy = v.opt(x, wl)
        rx, ry = (w * 0.6 + w * 0.9 * k) * v.Z * 3, (8 + 10 * k) * v.Z * 3
        yy, xx = np.ogrid[int(max(0, cy - ry - 4)):int(min(big.shape[0], cy + ry + 4)), int(max(0, cx - rx - 4)):int(min(big.shape[1], cx + rx + 4))]
        if yy.size == 0 or xx.size == 0: continue
        d = np.sqrt(((xx - cx) / rx) ** 2 + ((yy - cy) / ry) ** 2)
        m = np.abs(d - 1) < 0.08
        reg = big[yy.min():yy.max() + 1, xx.min():xx.max() + 1]
        reg[m] = (reg[m] * 0.4 + np.array((255, 255, 255)) * 0.6 * (1 - k)).astype(np.uint8) + (reg[m] * 0.6 * k).astype(np.uint8)


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Dad, aura farming means acting cool without trying. My friends are coming. PLEASE don't do it.» — Doug in a slow-motion «cool»
    pose with the spatula and the shades, Kayden pleading in front of him; the neighbour's camera blinks red on the eave (clue)"""
    v = view_at(YARD, 430, 600, 1.0 + 0.05 * sm(u / 5.5), 180, 560)

    def draw(CH, v_):
        doug_at(CH, v_, t, (480.0, 610.0, 11.6), expr='smug', pose=A.DPOSE['hips'] if u > 1.5 else A.DPOSE['point'], mouth_=0.0,
                shine=0.6 * sm((u - 0.4) / 0.3) * (1 - sm((u - 1.2) / 0.3)), prop_n=spatula)
        kid(CH, v_, t, (350.0, 650.0, 11.8), expr='flat', pose=A.KPOSE['stand'], look=0.3)
    return yard(v, t, draw)


def r_smug(t, u):
    """«Son, I INVENTED acting cool. Watch and learn.» — close on Doug, smug, he slides the shades down onto his eyes"""
    x, y, un = 480.0, 610.0, 11.6
    k = 1.3
    hy = y - 25.4 * un * k
    v = view_at(YARD, x - 2.0 * un * k, hy, 1.4, 180, 330)

    def draw(CH, v_):
        doug_at(CH, v_, t, (x, y, un), k, expr='smug', pose=A.DPOSE['point'], prop_n=spatula)
    big = yard(v, t, draw)
    if u > 2.2:                                                                                         # shades slide onto the eyes
        kk = sm((u - 2.2) / 0.4)
        cx, cy = v.opt(x - 2.3 * un * k, y - (28.7 - 3.2 * kk) * un * k)
        O.overlay(big, _shades(int(5.2 * un * k * v.Z * 3)), int(cx - 2.6 * un * k * v.Z * 3), int(cy), 1.0)
    return big


_SH = {}


def _shades(w):
    if w in _SH: return _SH[w]
    from PIL import Image, ImageDraw
    h = int(w * 0.32)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w // 2 - 4, h - 1], h // 3, fill=(60, 30, 100, 235), outline=(30, 16, 50, 255), width=6)
    d.rounded_rectangle([w // 2 + 4, 0, w - 1, h - 1], h // 3, fill=(60, 30, 100, 235), outline=(30, 16, 50, 255), width=6)
    d.line([(w // 2 - 6, h // 3), (w // 2 + 6, h // 3)], fill=(30, 16, 50, 255), width=8)
    d.line([(10, 8), (w // 4, 8)], fill=(160, 230, 240, 255), width=6)
    _SH[w] = np.array(im)
    return _SH[w]


def r_grill(t, u):
    """«Sup, boys. Just grilling. Like a LEGEND.» — the boys arrive on the left; Doug, shades on, poses with the spatula"""
    v = view_at(YARD, 260, 610, 0.95, 180, 560)

    def draw(CH, v_):
        boys(CH, v_, t)
        doug_at(CH, v_, t, DOUG, expr='smug', pose=A.DPOSE['point'], prop_n=spatula)
        kid(CH, v_, t, KAY, expr='flat', pose=A.KPOSE['stand'], look=0.2)
    return yard(v, t, draw)


def r_burger(t, u):
    """the burger flip: it flies up out of frame — and never comes back (Doug and the boys look up, waiting)"""
    v = view_at(YARD, 260, 560, 0.95, 180, 520)

    def draw(CH, v_):
        boys(CH, v_, t, expr='shock')
        doug_at(CH, v_, t, DOUG, expr='smug' if u < 0.5 else 'shock', pose=A.DPOSE['cheer'] if u < 0.4 else A.DPOSE['point'],
                prop_n=spatula, look=0.0)
        bx = DOUG[0] - 40; by = DOUG[1] - 230 - 900 * sm(u / 0.5)
        L = Layer(v_.wcam()); A.burger(L, bx, by, 1.2, t * 9); F.outline(L, A.OL); CH.add(L)
    return yard(v, t, draw)


def r_fall(t, u):
    """the cool exit: Doug backs away — one step too far — and drops backwards into the pool (splash)"""
    v = view_at(YARD, 520, 560, 1.0, 180, 520)
    x = lerp(DOUG[0], 560, sm(u / 0.7))
    drop = 340 * sm((u - 0.65) / 0.25)

    def draw(CH, v_):
        boys(CH, v_, t, expr='shock')
        if u < 0.9:
            doug_at(CH, v_, t, (x, DOUG[1] + drop, DOUG[2]), expr='smug' if u < 0.6 else 'shock', pose=A.DPOSE['shout'] if u > 0.6 else
                    A.DPOSE['stand'], lean=-1.4 * sm((u - 0.5) / 0.2), prop_n=spatula)

    def splash(FX, v_):
        if u > 0.85:
            B.spray(FX, v_, t, (570, 300), spread=120, drop=200, n=60, col=(220, 245, 255), col2=(150, 220, 240), speed=2.6)
    big = yard(v, t, draw, after=splash)
    if u > 0.85: B.shake(big, t, 10, 33); ripples(big, v, t, 570, POOL_W, 90)
    return big


def r_wet(t, u):
    """«Nobody saw that. We're FINE.» — Doug's head and shoulders above the water, spitting, fake calm; ripples"""
    un = 11.0
    k = 1.25
    wl = POOL_W
    y = wl + 17.0 * un * k
    v = view_at(YARD, PDOUG_X - 1.0 * un * k, wl - 6.0 * un * k, 1.35, 180, 360)

    def draw(CH, v_):
        doug_at(CH, v_, t, (PDOUG_X, y, un), k, expr='sad' if u < 1.0 else 'smug', pose=A.DPOSE['stand'])

    def water(big, v_):
        K.draw_occluder(big, v_, pool_doug(PDOUG_X, wl, un)); ripples(big, v_, t, PDOUG_X, wl, 60)
    big = yard(v, t, draw, water=water)
    if u < 0.8:
        B.puff(big, *v.opt(PDOUG_X - 3.5 * un * k, wl - 6 * un * k), 30, 0.4, col=(220, 245, 255))
    return big


def r_twist(t, u):
    """TWIST «Dad. The neighbor's camera posted it. Two million VIEWS.» — Kayden flat; whip-pan to the blinking camera on the eave
    («SMILE! YOU'RE ON CAMERA»); the phone with the viral clip fills the screen"""
    if u < 1.1:
        v = view_at(YARD, 300, 620, 1.3, 180, 560)
        def draw(CH, v_):
            kid(CH, v_, t, KAY, expr='flat', pose=A.KPOSE['phone'], prop_n=A.phone, look=0.2)
        return yard(v, t, draw)
    k = sm((u - 1.1) / 0.35)
    v = view_at(YARD, lerp(400, K.Y_CAM[0], k), lerp(500, K.Y_CAM[1] + 40, k), lerp(1.1, 1.45, k), 180, 300)
    big = yard(v, t, cam_k=2.0)
    if u < 1.45: fx.speed_lines(big, t, 1.0)
    if u > 2.1:
        kk = sm((u - 2.1) / 0.15)
        ui = O._scale(K.phone_ui(2100000, t, 'video'), 0.4 + 0.65 * kk)
        O.overlay(big, ui, int((1080 - ui.shape[1]) / 2), int(lerp(900, 380, kk)), 1.0)
        ST.log('sticker', bbox=(int((1080 - ui.shape[1]) / 2), int(lerp(900, 380, kk)), int((1080 + ui.shape[1]) / 2), int(lerp(900, 380, kk) + ui.shape[0])))
    return big


def r_viral(t, u):
    """«Bro! Grill Dad Falls In is TRENDING!» — the boys and Kayden glued to their phones, Jaxon laughing; Doug floats behind them"""
    v = view_at(YARD, 330, 600, 1.12, 180, 560)
    un = 11.0

    def draw(CH, v_):
        doug_at(CH, v_, t, (PDOUG_X, POOL_W + 17.0 * un, un), expr='sad', pose=A.DPOSE['stand'], mouth_=0.0)
        kid(CH, v_, t, (300.0, 646.0, 11.6), 'jaxon', A.FRIEND_PALS[0], expr='smirk', pose=A.KPOSE['phone'], prop_n=A.phone)
        kid(CH, v_, t + 0.5, (180.0, 660.0, 11.8), 'none', A.FRIEND_PALS[1], expr='smirk', pose=A.KPOSE['look'], prop_n=A.phone)
        kid(CH, v_, t + 1.0, (90.0, 650.0, 11.4), expr='bored', pose=A.KPOSE['look'], prop_n=A.phone)

    def water(big, v_):
        K.draw_occluder(big, v_, pool_doug(PDOUG_X, POOL_W, un)); ripples(big, v_, t, PDOUG_X, POOL_W, 50)
    return yard(v, t, draw, water=water)


def r_mirra(t, u):
    """«Recalculating aura. Plus nine hundred. The internet LOVES a fall.» — MIRRA on the patio speaker, close; Doug floats behind"""
    sx, sy = K.Y_SPEAKER
    v = view_at(YARD, sx + 20, sy - 40, 1.42, 150, 340)

    def draw(CH, v_):
        L = Layer(v_.wcam()); box = A.speaker(L, sx, sy, 1.6); F.outline(L, A.OL); CH.add(L)
        L = Layer(v_.wcam()); K.mirra_panel(L, box, t, mouth('mirra', t, 2.0), 'smug'); CH.add(L)
    big = yard(v, t, draw)
    D.blit(big, v, K.score_plate(900, 50, 14), sx - 25, sy - 96)
    return big


def r_button(t, u):
    """«HA! I've still GOT it!» — Doug in the pool throws his fists up, the dome twinkles — and he sinks; bubbles"""
    un = 11.0
    k = 1.2
    wl = POOL_W
    sink = 260 * sm((u - 1.75) / 0.5)
    y = wl + 17.0 * un * k + sink
    v = view_at(YARD, PDOUG_X - 0.5 * un * k, wl - 8.0 * un * k, 1.3, 180, 360)

    def draw(CH, v_):
        doug_at(CH, v_, t, (PDOUG_X, y, un), k, expr='proud' if u < 1.8 else 'shock', pose=A.DPOSE['cheer'],
                shine=sm((u - 0.85) / 0.3) * (1 - sm((u - 1.6) / 0.2)))

    def water(big, v_):
        K.draw_occluder(big, v_, pool_doug(PDOUG_X, wl, un)); ripples(big, v_, t, PDOUG_X, wl, 70)
        if u > 1.9:
            for i in range(5):
                bx, by = v_.opt(PDOUG_X - 20 + i * 10, wl - ((t * 60 + i * 13) % 30))
                fx.glow(big, bx, by, 14, (255, 255, 255), 0.7)
    big = yard(v, t, draw, water=water)
    return big


SHOT = dict(hook=r_hook, smug=r_smug, grill=r_grill, burger=r_burger, fall=r_fall, wet=r_wet, twist=r_twist, viral=r_viral,
            mirra=r_mirra, button=r_button)


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


SHOW = K.Show(EPI, 1, 3, ['AURA FARMING?!'], hook_t=(0.06, 2.6), hook_y=250,
              stickers=[(O.sticker('SPLASH!', fg=(120, 230, 240), size=96), F0['fall'] + 0.9, F0['wet'] + 0.5, 540, 600),
                        (O.sticker('2.1M VIEWS', fg=(255, 90, 110), size=80), F0['viral'] + 0.3, F0['mirra'], 540, 520),
                        (O.sticker('+900', fg=(150, 250, 190), size=96), F0['mirra'] + 1.5, F0['button'], 760, 560)],
              flashes=[TL.TWIST + 1.1], mosaics=[F0['grill'], F0['mirra']],
              cap_y={'hook': 1400, 'smug': 1420, 'grill': 1420, 'wet': 1440, 'twist': 1420, 'viral': 1420, 'mirra': 1440,
                     'button': 1440}, cap_default=1420)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
