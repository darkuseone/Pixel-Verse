"""S01E01 «MINUS 400?!» — Kayden's aura app scans Doug: minus four hundred, «the app can't even find your jawline, start mewing».
MIRRA explains mewing (tongue up, all day, no talking); Doug puffs his cheeks and goes silent; Tammy: «He hasn't said one word since
breakfast. It's beautiful.» TWIST (60 %): the aura went UP, plus five hundred — not from mewing, «because you stopped talking». Doug:
«HA! I've still GOT it!» -> the fridge's MIRRA: «Recalculating. Minus four hundred. Welcome back, Doug.» (loop to the opening -400).
  python3 ep01.py test 1 5 20 | frames t… | all | shots <i|name>…      then  python3 mix.py <noaudio.mp4> final.mp4"""
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
              endcard=dict(style='auradad', lang='us', promise='TOMORROW: THE $340 SKINCARE'))
talk = EPI.talk
W = K.build()
K.decorate(W)
KIT, BATH = W['kitchen'], W['bathroom']
CUTS, NAMES = TL.CUTS, TL.NAMES
F0 = TL.T0

DOUG = (740.0, 650.0, 11.0)          # Doug in the kitchen, facing left (towards Kayden)
KAY = (540.0, 652.0, 11.0)           # Kayden, facing right
TAM = (1060.0, 706.0, 11.8)          # Tammy in front of the breakfast table, facing left
BDOUG = (812.0, 666.0, 13.0)         # Doug at the vanity, profile, facing left (the mirror)


def mouth(who, t, k=1.7):
    return min(1.0, talk(who, t) * k)


def face(v, cam, r, ru=3.2):
    K.logface(v, cam, r['head'], ru)


def u2w(v, cam, pt):
    x, y = cam.p(*pt)
    k = ST.PX[0]
    return v.X0 + x * k / v.Z, v.Y0 + (y * k - v.oy) / v.Z


def kitchen(v, t, draw=None, sun=1.0, fx_=None):
    CH, FX = K.begin()
    big = v.bg()
    if draw: draw(CH, v)
    CH.comp(big, K.light_kitchen(v, sun))
    fx.motes(FX, v, t, 480, 120, 840, 380, n=22, col=(255, 244, 210), seed=4)
    if fx_: fx_(FX, v)
    FX.comp(big)
    B.steam(big, v, t, K.K_MUG[0], K.K_MUG[1] - 14, n=4, rise=60, size=18, a=0.35)
    fx.vignette(big, 0.22)
    return big


def bathroom(v, t, draw=None, talk_=0.0, expr='calm', glass=True):
    CH, FX = K.begin()
    big = v.bg()
    if glass:
        L = Layer(v.wcam()); K.mirra_glass(L, t, talk_, expr); CH.add(L)
    if draw: draw(CH, v)
    CH.comp(big, K.light_bath(v))
    if glass: K.glass_glow(big, v, t)
    fx.motes(FX, v, t, 900, 120, 1240, 380, n=16, col=(255, 250, 230), seed=6)
    FX.comp(big)
    fx.vignette(big, 0.22)
    return big


def doug_at(CH, v, t, pos=DOUG, k=1.0, flip=True, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un * k, flip=flip)
    kw.setdefault('expr', 'normal')
    if 'mouth_' not in kw: kw['mouth_'] = mouth('doug', t)
    r = A.doug(CH, cam, t=t, **kw)
    face(v, cam, r, 3.4)
    return cam, r


def kay_at(CH, v, t, pos=KAY, k=1.0, flip=False, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un * k, flip=flip)
    kw.setdefault('expr', 'bored')
    r = A.kayden(CH, cam, t=t, mouth_=mouth('kayden', t), **kw)
    face(v, cam, r, 2.8)
    return cam, r


def tam_at(CH, v, t, pos=TAM, k=1.0, flip=True, **kw):
    x, y, un = pos
    cam = v.cam(x, y, un * k, flip=flip)
    kw.setdefault('expr', 'tired')
    r = A.tammy(CH, cam, t=t, mouth_=mouth('tammy', t), **kw)
    face(v, cam, r, 2.6)
    return cam, r


def phone_big(big, value, t, x, y, scale=0.72, mode='score', label=None):
    ui = K.phone_ui(value, t, mode, label=label)
    ui = O._scale(ui, scale)
    O.overlay(big, ui, int(x), int(y), 1.0)
    ST.log('sticker', bbox=(int(x), int(y), int(x + ui.shape[1]), int(y + ui.shape[0])))


# ---------------------------------------------------------------- shots
def r_hook(t, u):
    """«Dad, my aura app just scanned you. Minus four hundred.» — Doug's shocked face (mouth open) + Kayden's phone «-400» in the
    foreground (readable without sound), slow push-in"""
    Z = 1.3 + 0.05 * sm(u / 3.5)
    v = view_at(KIT, 760, 650, Z, 236, 600)

    def draw(CH, v_):
        doug_at(CH, v_, t, expr='shock', pose=A.DPOSE['mug'], prop_n=A.mug, mouth_=0.55 + 0.1 * math.sin(t * 9))
        kay_at(CH, v_, t, (600.0, 712.0, 13.2), pose=A.KPOSE['phone'])
    big = kitchen(v, t, draw)
    phone_big(big, -400 if u > 0.9 else 0, t, 40, 1090, 0.7, 'score' if u > 0.9 else 'scan')
    return big


def r_doug_cu(t, u):
    """«Minus four HUNDRED?! I own a BOAT and a Cost-Go card!» — close-up, coffee spat out, cheeks red, shake"""
    x, y, un = DOUG
    k = 1.3
    hy = y - 25.4 * un * k
    v = view_at(KIT, x - 1.0 * un * k, hy, 1.4, 180, 330)

    def draw(CH, v_):
        doug_at(CH, v_, t, (x, y, un), k, expr='shout', pose=A.DPOSE['shout'], shake=0.03 if u < 1.2 else 0.0)

    def spit(FX, v_):
        if u < 0.9:
            sx = x - 4.4 * un * k; sy = hy - 22.9 * un * k + 25.4 * un * k - 0
            B.spray(FX, v_, t, (sx, y - 23.0 * un * k), spread=60, drop=140, n=26, col=(130, 80, 44), col2=(170, 110, 60), speed=3.0)
    big = kitchen(v, t, draw, fx_=spit)
    if u < 0.4: B.shake(big, t, 10, 33)
    return big


def r_jaw(t, u):
    """«It can't even FIND your jawline. Start mewing.» — two-shot; AR scan brackets over Doug's (missing) chin + red label"""
    v = view_at(KIT, 640, 650, 1.0, 180, 560)
    box = {}

    def draw(CH, v_):
        kay_at(CH, v_, t, pose=A.KPOSE['phone'], prop_n=A.phone)
        cam, r = doug_at(CH, v_, t, expr='sad', pose=A.DPOSE['mug'], prop_n=A.mug, look=-0.2)
        box['c'] = cam.p(*r['chin'])
    big = kitchen(v, t, draw)
    if u > 0.25:
        cx, cy = box['c'][0] * 3, box['c'][1] * 3
        K.ar_scan(big, min(cx, 900), cy + 10, 78, t, 'NO JAWLINE')
    return big


def r_mirra(t, u):
    """«Mewing means: tongue on the roof of your mouth. All day. No talking.» — MIRRA's face on the bathroom mirror, Doug in
    profile at the vanity listening; slow push-in on the glass"""
    Z = 1.12 + 0.12 * sm(u / 4.0)
    v = view_at(BATH, 690, 300, Z, 180, 270)

    def draw(CH, v_):
        doug_at(CH, v_, t, BDOUG, 1.0, flip=True, expr='normal', look=0.0, mouth_=0.0)
    return bathroom(v, t, draw, talk_=mouth('mirra', t, 2.0), expr='calm')


def r_mew(t, u):
    """«Mm-HMM!» — close-up: Doug presses his tongue up, cheeks inflate, fists clenched; MIRRA smug in the glass behind"""
    x, y, un = BDOUG
    k = 1.55
    hy = y - 25.4 * un * k
    v = view_at(BATH, x - 1.4 * un * k - 30, hy, 1.42, 200, 300)
    puff = sm(u / 0.35)

    def draw(CH, v_):
        doug_at(CH, v_, t, (x, y, un), k, flip=True, expr='mew' if puff > 0.4 else 'normal', pose=A.DPOSE['fists'],
                shake=0.02 * puff, mouth_=0.0)
    return bathroom(v, t, draw, talk_=0.0, expr='smug')


def r_tammy(t, u):
    """«He hasn't said ONE word since breakfast. It's beautiful.» — wide kitchen: Doug silent with puffed cheeks, Tammy blissful with
    her mug, Kayden reading his phone — the clue: his aura counter quietly climbs while Doug is silent"""
    v = view_at(KIT, 800, 650, 0.9 + 0.02 * sm(u / 3.8), 180, 560)
    pos = {}

    def draw(CH, v_):
        cam, r = kay_at(CH, v_, t, (630.0, 652.0, 11.0), pose=A.KPOSE['look'], prop_n=A.phone, look=0.2)
        pos['k'] = u2w(v_, cam, r['hand_n'])
        doug_at(CH, v_, t, (800.0, 650.0, 11.0), expr='mew', pose=A.DPOSE['fists'], mouth_=0.0, bob=0.03)
        tam_at(CH, v_, t, (930.0, 700.0, 11.4), expr='bliss', pose=A.TPOSE['hug'], prop_n=A.mug)
    big = kitchen(v, t, draw)
    val = int(lerp(-400, -40, sm(u / 3.6)) // 10 * 10)
    hx, hy = pos['k']
    D.blit(big, v, K.score_plate(val), hx - 32, hy - 64)
    return big


def r_twist(t, u):
    """TWIST «Yo, Dad! Your aura went UP! Plus five hundred!» — the phone fills the screen: «+500» (flash + sting), then Kayden in shock"""
    v = view_at(KIT, 640, 650, 1.12 + 0.04 * sm(u / 4.0), 180, 580)

    def draw(CH, v_):
        kay_at(CH, v_, t, (590.0, 652.0, 11.0), pose=A.KPOSE['shock'], expr='shock', prop_n=A.phone)
        doug_at(CH, v_, t, (780.0, 650.0, 11.0), expr='mew', pose=A.DPOSE['fists'], mouth_=0.0)
    big = kitchen(v, t, draw)
    if u < 1.25:
        k = sm(u / 0.15)
        phone_big(big, 500, t, 540 - 280 * k, 980 - 520 * k, 0.4 + 0.68 * k, 'score')
    return big


def r_cheer(t, u):
    """«Mm-MM!» — Doug throws both fists up, cheeks still puffed, victory bob"""
    x, y, un = 770.0, 650.0, 11.0
    k = 1.1
    v = view_at(KIT, x - 10, y, 1.2, 180, 615)

    def draw(CH, v_):
        doug_at(CH, v_, t, (x, y, un), k, expr='mew', pose=A.DPOSE['cheer'], mouth_=0.0, bob=0.18)
    big = kitchen(v, t, draw)
    return big


def r_flat(t, u):
    """«It's not the mewing, Dad. It's because you stopped TALKING.» — Kayden close, deadpan, half-turned to camera"""
    x, y, un = 540.0, 652.0, 11.0
    k = 1.4
    hy = y - 25.8 * un * k
    v = view_at(KIT, x + 1.0 * un * k, hy, 1.4 + 0.03 * sm(u / 3.0), 180, 320)

    def draw(CH, v_):
        kay_at(CH, v_, t, (x, y, un), k, pose=A.KPOSE['look'], expr='flat', prop_n=A.phone, look=0.3)
    return kitchen(v, t, draw)


def r_proud(t, u):
    """«HA! See? I've still GOT it!» — Doug opens his mouth, arms up, the dome twinkles"""
    x, y, un = 770.0, 650.0, 11.0
    k = 1.15
    hy = y - 25.4 * un * k
    v = view_at(KIT, x - 0.8 * un * k, hy + 40, 1.3, 180, 300)

    def draw(CH, v_):
        doug_at(CH, v_, t, (x, y, un), k, expr='proud', pose=A.DPOSE['cheer'], shine=sm((u - 0.85) / 0.3) * (1 - sm((u - 2.0) / 0.3)))
    return kitchen(v, t, draw)


def r_button(t, u):
    """«Recalculating. Minus four hundred. Welcome BACK, Doug.» — ding: whip-pan to the smart fridge: MIRRA on its screen with
    «AURA -400»; Doug in the foreground deflates"""
    pan = sm(u / 0.4)
    cx = lerp(640, 190, pan)
    v = view_at(KIT, cx, lerp(420, 300, pan), lerp(1.2, 1.25, pan), 180, lerp(300, 330, pan))

    def draw(CH, v_):
        L = Layer(v_.wcam()); K.mirra_panel(L, K.K_FRIDGE_SCREEN[:2] + (K.K_FRIDGE_SCREEN[0] + 64, K.K_FRIDGE_SCREEN[1] + 64), t,
                                             mouth('mirra', t, 2.0), 'smug'); CH.add(L)
        doug_at(CH, v_, t, (300.0, 740.0, 12.0), flip=True, expr='sad' if u > 0.7 else 'proud', pose=A.DPOSE['stand'], mouth_=0.0)
    big = kitchen(v, t, draw)
    D.blit(big, v, K.score_plate(-400, 64, 16), K.K_FRIDGE_SCREEN[0], K.K_FRIDGE_SCREEN[1] + 70)
    if u < 0.4: fx.speed_lines(big, t, 0.9)
    return big


SHOT = dict(hook=r_hook, doug_cu=r_doug_cu, jaw=r_jaw, mirra=r_mirra, mew=r_mew, tammy=r_tammy, twist=r_twist, cheer=r_cheer,
            flat=r_flat, proud=r_proud, button=r_button)


def shot_at(t):
    for s in TL.SHOTS:
        if s['t0'] <= t < s['t1']: return s
    return TL.SHOTS[-1]


SHOW = K.Show(EPI, 1, 1, ['MINUS 400?!'], hook_t=(0.06, 2.6), hook_y=250,
              stickers=[(O.sticker('MEWING...', fg=(150, 250, 190), size=64), F0['mew'] + 0.35, F0['tammy'], 540, 1480),
                        (O.sticker('+500?!', fg=(150, 250, 190), size=96), TL.TWIST + 1.3, F0['cheer'], 760, 520),
                        (O.sticker('-400', fg=(255, 90, 110), size=96), F0['button'] + 1.4, TL.DUR - 1.0, 760, 520)],
              flashes=[TL.TWIST + 0.02, F0['button'] + 0.05], mosaics=[F0['mirra'], F0['tammy']],
              cap_y={'hook': 990, 'doug_cu': 1400, 'jaw': 1340, 'mirra': 1440, 'mew': 1300, 'tammy': 1380, 'twist': 1420,
                     'cheer': 1400, 'flat': 1420, 'proud': 1420, 'button': 1230}, cap_default=1380)


def render(t):
    s = shot_at(t)
    big = SHOT[s['name']](t, t - s['t0'])
    SHOW.apply(big, t, s['name'])
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
