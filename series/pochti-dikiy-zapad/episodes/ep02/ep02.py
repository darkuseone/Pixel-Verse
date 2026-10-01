"""S01E02 «Засада» — HD-пересборка на общем движке (xAI-задник cactus_field + код-герои, свет, частицы), 9:16.
  python3 ep02.py test 1 5 20 | frame 12 | all [4]"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import paths as P
import math
import numpy as np
import stage as ST
from stage import View, view_at, Chars, Light, shadow, ell, OUT_W, OUT_H, UP
import scene as S
from scene import Layer, cap, dot, outline, sm, lerp
import overlays as O
import fx
from episode import Episode
from props import chars as C
from props import pilot as PL
from timeline import DUR, FPS, VOICE

EPI = Episode('ep02', VOICE, DUR, FPS)
talk = EPI.talk
FIELD = ST.ai_world(P.series() / 'bg' / 'cactus_field.png')

FEET = 600.0
U = 6.0
MX, PX_POST, CX = 440.0, 392.0, 690.0
DONKEY_X = 830.0
T_SIT, T_GIVE, T_SPILL, T_POP = 19.3, 25.2, 25.7, 30.3


def light():
    return Light(amb=(1.08, 0.98, 0.86), rim=(1, -1, (255, 226, 170), 0.5), grad=(1.08, 0.88))


def begin(Z):
    ST.set_px(ST.px_for_zoom(Z)); return Chars(), Chars()


def sam_state(t):
    """(x, mode)  mode: none | ride | walk_l | sit | give | walk_r"""
    if t < 14.2: return None, 'none'
    if t < 17.6: return lerp(1150, 850, sm((t - 14.2) / 3.4)), 'ride'
    if t < T_SIT: return lerp(830, CX + 30, sm((t - 17.6) / 1.7)), 'walk_l'
    if t < 23.0: return CX, 'sit'
    if t < T_GIVE: return lerp(CX, MX + 210, sm((t - 23.0) / 2.2)), 'walk_l'
    if t < 28.2: return MX + 210, 'give'
    if t < 29.6: return lerp(MX + 210, 830, sm((t - 28.2) / 1.4)), 'walk_r'
    if t < 32.4: return lerp(830, 1500, sm((t - 29.6) / 2.8)), 'ride'
    return None, 'none'


def scene(CH, FX, big, v, t):
    fx.motes(FX, v, t, 0, 300, 1280, 700, n=30, seed=6)
    mx = MX if t < 12.6 else lerp(MX, MX + 10, sm((t - 12.6) / 0.6))
    ph = C.molniya_pose(t, chew=t >= 34.6 or 26.6 <= t < 29.5, jaw_talk=talk('molniya', t))
    ax, ay = C.horse_anchor(mx, FEET, U)
    shadow(big, v, mx, FEET, 16 * U, 1.8 * U)
    C.molniya(CH, v.cam(ax, ay, U), t, ph, hat=True, carrot=t >= 34.6 or 26.6 <= t < 29.5, carrots=1)
    PL.signpost(CH, v, PX_POST, FEET)
    if t >= 15.0: PL.vulture(CH, v, PX_POST - 20, FEET - 205, t)
    if t >= T_SPILL: PL.carrots_ground(CH, v, MX + 40, FEET, t, 0 if t < 26.6 else 2)
    # costume / Billy
    if t < T_POP:
        squash, wob = 1.0, 0.0
        if T_SIT <= t < 23.0:
            squash = 0.93 + 0.02 * math.sin(t * 30); wob = 1.5 * math.sin(t * 24) * (1 if t < 20.6 else 0.4)
        hand = 0.0
        if 7.3 <= t < 8.8: hand = min(1.0, (t - 7.3) / 0.2) * (1 - sm((t - 8.4) / 0.3))
        shadow(big, v, CX, FEET + 6, 8 * U, 1.4 * U)
        PL.costume(CH, v, CX, FEET + 6, U, wob, squash, hand)
    else:
        k = t - T_POP
        PL.costume_halves(CH, v, CX, FEET + 6, U, min(k, 1.6))
        bx = CX + 20
        shadow(big, v, bx, FEET + 6, 5 * U, 1.2 * U)
        C.billy(CH, v.cam(bx, FEET + 6 - C.HIP_H * U, U), C.POSES['heroic'] if k < 3.0 else C.POSES['hips'], 0.05, talk('billy', t),
                'shout' if k < 3.5 else 'sly', hat=False)
        if k < 0.5: fx.dust_puffs(FX, v, t, [(T_POP, CX, FEET + 6, 26)])
    # donkey + Sam
    x, mode = sam_state(t)
    du = U * 0.85
    if mode == 'ride':
        shadow(big, v, x, FEET - 4, 13 * du, 1.6 * du)
        C.donkey(CH, v.cam(x, FEET - 4 - 19 * du, du), t, moving=True, rider=C.rider_sam(dict(C.POSES['ride'], _t=t), talk('sam', t)))
    elif mode != 'none':
        shadow(big, v, DONKEY_X, FEET - 4, 13 * du, 1.6 * du)
        C.donkey(CH, v.cam(DONKEY_X, FEET - 4 - 19 * du, du), t, moving=False, bray=1.0 if 17.6 <= t < 18.2 else 0.0)
        if mode == 'sit':
            C.sam(CH, v.cam(CX + 2, FEET + 6 - 12.9 * U, U, True), C.POSES['sit'], 0.03, talk('sam', t))
        elif mode in ('walk_l', 'walk_r'):
            shadow(big, v, x, FEET + 4, 5 * U, 1.2 * U)
            C.sam(CH, v.cam(x, FEET + 4 - C.HIP_H * U, U, mode == 'walk_l'), C.walk_pose(t * 0.75, 9, 0.3), 0.03, talk('sam', t))
        elif mode == 'give':
            shadow(big, v, x, FEET + 4, 5 * U, 1.2 * U)
            C.sam(CH, v.cam(x, FEET + 4 - C.HIP_H * U, U, True), C.POSES['present'] if t < 26.4 else C.POSES['stand'], 0.03, talk('sam', t))


SHOTS = [
    (0.0, 2.5, 'cu_costume'), (2.5, 8.5, 'cu_costume2'), (8.5, 12.0, 'cu_mol'), (12.0, 13.7, 'wide'), (13.7, 15.8, 'cu_mol_post'),
    (15.8, T_SIT, 'sam_arrives'), (T_SIT, 23.2, 'sit'), (23.2, 27.3, 'give'), (27.3, 28.2, 'cu_mol_sp'), (28.2, T_POP, 'wide_leave'),
    (T_POP, 34.8, 'cu_billy_pop'), (34.8, DUR + 1, 'cu_mol_end'),
]
FLASH_AT = [T_POP, 12.0]


def shot_at(t):
    for a, b, n in SHOTS:
        if a <= t < b: return a, b, n
    return SHOTS[-1]


def render_scene(t):
    a, b, name = shot_at(t); u = t - a
    def head(): return C.head_of_horse(MX, FEET, U, C.molniya_pose(t))
    if name == 'cu_costume': v = view_at(FIELD, CX, FEET - 50, 3.0 - 0.1 * u, 180, 430)
    elif name == 'cu_costume2': v = view_at(FIELD, CX + 20, FEET - 50, 2.5 + 0.04 * u, 180, 430)
    elif name in ('cu_mol', 'cu_mol_sp'):
        hx, hy = head(); v = view_at(FIELD, hx + 20, hy + 20, 2.9 + 0.04 * u, 180, 430)
    elif name == 'wide': v = view_at(FIELD, 560, FEET - 130, 0.9, 180, 400)
    elif name == 'cu_mol_post':
        hx, hy = head(); v = view_at(FIELD, hx - 20, hy - 30, 2.2, 180, 420)
    elif name == 'sam_arrives':
        sx, _ = sam_state(t); v = view_at(FIELD, (sx or 800) - 20, FEET - 90, 1.3, 180, 420)
    elif name == 'sit': v = view_at(FIELD, CX + 20, FEET - 80, 2.0 + 0.03 * u, 180, 420)
    elif name == 'give':
        sx, _ = sam_state(t); v = view_at(FIELD, (sx or 640) - 70, FEET - 90, 1.4, 180, 420)
    elif name == 'wide_leave': v = view_at(FIELD, 760, FEET - 130, 0.9, 180, 400)
    elif name == 'cu_billy_pop': v = view_at(FIELD, CX + 20, FEET - 100, 1.9 + 0.03 * u, 180, 430)
    else:
        hx, hy = head(); v = view_at(FIELD, hx + 10, hy + 20, 2.6 - 0.03 * u, 180, 440)
    CH, FX = begin(v.Z)
    big = v.bg()
    scene(CH, FX, big, v, t)
    CH.comp(big, light()); FX.comp(big)
    fx.vignette(big, 0.3)
    return big


BADGE = O.make_badge('СЕЗОН 1 • СЕРИЯ 2/6')
HOOK = O.pixel_title(['ИДЕАЛЬНАЯ', 'МАСКИРОВКА'], 64)
TEASE = O.pixel_title(['СЕРИЯ 3 СКОРО'], 40)
STICKERS = [
    (O.sticker('ХВАТЬ!', fg=(255, 120, 90), size=80), 7.4, 8.5, 540, 560),
    (O.sticker('ВОЗДУХАН?', fg=(255, 236, 120), size=64), 9.0, 10.4, 540, 560),
    (O.sticker('+7', icon=C.carrot_icon(1, 7)), 25.8, 27.2, 540, 560),
]


def render(t):
    big = render_scene(t)
    for img, a, b, cx, cy in STICKERS: O.draw_sticker(big, img, t, a, b, cx, cy)
    O.overlay(big, BADGE, 36, 96, 1.0)
    if 0.2 <= t < 2.3:
        k = min(1.0, (t - 0.2) / 0.1) * (1 - sm((t - 2.1) / 0.2))
        O.overlay(big, HOOK, 0, 220, k)
    if t < 35.8: EPI.captions.draw(big, t, 780 if t >= 2.5 else 1000)
    if t >= 35.8: O.overlay(big, TEASE, 0, 1540, min(1.0, (t - 35.8) / 0.15))
    for fa in FLASH_AT:
        if fa <= t < fa + 0.15: O.flash(big, 0.7 * (1 - (t - fa) / 0.15))
    for m0 in (8.5, 15.8, 23.2, T_POP):
        if m0 <= t < m0 + 0.25: O.mosaic(big, int(lerp(40, 1, (t - m0) / 0.25)))
    return big


if __name__ == '__main__':
    EPI.main(render, __file__)
