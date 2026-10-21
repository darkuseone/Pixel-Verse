"""S01E05 «$30 FOR FOOTBALL?!» (32.25 s, twist at 17.86 s / 55 %, type: bureaucratic recursion — support for the subscription costs
another subscription). Thursday 6 PM, the peak of the season: dinner is on the table at last.
HOOK: Randy at the big TV — «SUBSCRIBE TO WATCH $29.99/MO» — «THIRTY bucks?! For FOOTBALL?!» Pull back: a golden turkey, Nana claps —
«Randy, it's perfect!» — «Twenty years! Never burned a turkey!» — Brayden from the kids' table: «It still has the price tag.»
(SHOP'N'WEEP $139). The TV stacks windows: «Download the app. Verify your email. Reset your password.» — «Security question. Name of
your first pet?» — «…Tom?» — the freezer: Tom: «We never met.» TWIST: «WRONG. ACCOUNT LOCKED. To speak to an agent, subscribe to
SUPPORT PLUS. Twenty-nine ninety-nine.» — on his knees: «I just want to watch the game!» — Nana pulls a 1998 portable TV out of her purse:
«No, it's fine. I have cable.» — «FINAL» — «Spoiler. We lost.» — the family, deadpan: «Thanks, Randy.» (the big TV: SUBSCRIBE again).
Clue: the fine print on the first frame «*requires app, account, email & patience».
  python3 ep05.py test 1 5 20 | frames 1 5 | all      then  python3 mix.py <noaudio.mp4> final.mp4"""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[4] / 'engine'))
import math
import numpy as np
from PIL import Image
import overlays as O
import stage as ST
from stage import view_at, OUT_W, OUT_H, Light
from scene import sm, lerp
from episode import Episode
from props import randycast as C
from props import randykit as K
from props.randykit import A, wpt, aout
from timeline import DUR, FPS, VOICE, SLUG, CUTS, NAMES, TWIST

EPI = Episode('ep05', VOICE, DUR, FPS, colors=K.COL, slug=SLUG, endcard=dict(style='randy', lang='us'))
LIV, LIV_B, KIT_B = K.world('living'), K.world('living_b'), K.world('kitchen_b')
WS = 5.0
FLOOR = 700.0
TV = (138.0, 182.0, 362.0, 333.0)            # TV screen (world, living.png)
TABLE_TOP = 470.0
PLATTER = (675.0, 470.0)
RAN = (430.0, FLOOR)
JOY = (560.0, 520.0)                          # Nana stands on a chair behind the table
BRA = (1170.0, 705.0)                         # Brayden at the kids' table
FREEZER = (34.0, 132.0, 286.0, 300.0)         # kitchen_b fridge top door


def mouth(who, t, k=1.8):
    return min(1.0, EPI.talk(who, t) * k)


def speaking(who, t):
    return any(spk == who and t0 <= t < t0 + (b - a) for _, _, _, t0, a, b, spk, _ in EPI.voice)


def V(world_, cx, cy, Z):
    return view_at(world_, cx, cy, Z, 180, 320)


def W(v, ox, oy):
    return wpt(v, ox, oy)


def light_liv(v, tv=0.0):
    keys = [(1180, 200, 700, (255, 200, 120), 0.40), (700, 340, 500, (255, 190, 110), 0.30)]
    if tv > 0: keys.append((250, 260, 500, (160, 120, 255), 0.35 * tv))
    return Light(amb=(1.0, 0.94, 0.86), keys=[(*v.opt(x, y), r * v.Z, c, a) for (x, y, r, c, a) in keys], rim=(-1, -0.3, (170, 140, 255), 0.25),
                 grad=(1.0, 0.9))


def tv(big, v, mode, t, step=0):
    K.paste_world(big, v, K.tv_ui(mode, t, step=step), TV)


def table_front(big, v, x0=352.0, x1=982.0, y=TABLE_TOP + 4):
    """the tablecloth hides the lower half of whoever stands behind the table"""
    bg = v.bg()
    ox0, oy = v.opt(x0, y); ox1, _ = v.opt(x1, y)
    X0, X1, Y0 = int(max(0, ox0)), int(min(OUT_W, ox1)), int(max(0, oy))
    if X0 < X1 and Y0 < OUT_H: big[Y0:, X0:X1] = bg[Y0:, X0:X1]


def screen_card(big, mode, t, y=300, step=0, w=980, h=560):
    img = K.tv_ui(mode, t, w, h, step)
    out = np.zeros((h + 40, w + 40, 4), np.uint8); out[..., :3] = (30, 30, 34); out[..., 3] = 255
    out[20:20 + h, 20:20 + w, :3] = img
    x0 = (OUT_W - out.shape[1]) // 2
    O.overlay(big, out, x0, y, 1.0)
    if ST.LOG[0] is not None: ST.log('card', bbox=(x0, y, x0 + out.shape[1], y + out.shape[0]))


# ================================================================== 0: HOOK — the paywall
def r_hook(t, u):
    Z = 1.3
    v = V(LIV, 330.0, 300.0, Z)
    big, a = K.cu(C.randy, t, LIV, 330.0, 300.0, Z, 21.0, head=(760, 1000), light=lambda v_: light_liv(v_, 1.0), flip=True,
                  pre_fx=lambda b, v_: tv(b, v_, 'paywall', t), expr='shout', mouth_=max(0.5, mouth('randy', t)), tremble=1.0, look=(1.0, 0.0),
                  stache='up', hand_n=(18.0, 60.0), prop_n=lambda sp, h: C.remote(sp, h), mitt=False)
    if u < 0.3: K.CK.shake(big, t, 12, 33)
    return big


# ================================================================== 1: TABLE — the golden turkey, applause: «It's perfect!» — «Never burned a turkey!»
def r_table(t, u):
    k = sm(u / 1.2)
    Z = lerp(1.15, 0.95, k)
    cx = lerp(420.0, 700.0, k)
    v = V(LIV, cx, 420.0, Z)
    s = WS * Z * 3
    roast = A(C.roast, *PLATTER, s * 0.9, t=t)
    j = A(C.joyce, *JOY, s, t=t, expr='cheer' if speaking('joyce', t) else 'smile', mouth_=mouth('joyce', t), look=(0.8, 0.0), purse=None,
          hand_n=(8.0, 26.0 + 4 * abs(math.sin(t * 9))), hand_f=(4.0, 26.0 + 4 * abs(math.sin(t * 9 + 1))))
    r = A(C.randy, 575.0, FLOOR, s, t=t, expr='proud', mouth_=mouth('randy', t), look=(1.0, 0.0), stache='up', mitt=True, hand_n=(17.0, 66.0))
    b = A(C.brayden, *BRA, s * 0.95, t=t, flip=True, expr='lazy', look=(-0.8, 0.0), stick=False)
    def f(big, v_):
        tv(big, v_, 'paywall', t)
        roast(big, v_, light_liv(v_)); j(big, v_, light_liv(v_))
        table_front(big, v_)
        r(big, v_, light_liv(v_)); b(big, v_, light_liv(v_))
        ox, oy = v_.opt(PLATTER[0], PLATTER[1] - 70)
        K.cold_vapor(big, ox, oy, t, 0.5, 1.0)
    return K.shot(LIV, light_liv, cx, 420.0, Z, fx_=f)


# ================================================================== 2: TAG — the price sticker + Brayden at the kids' table
def r_tag(t, u):
    Z = 1.35
    v = V(LIV_B, 900.0, 420.0, Z)
    def pre(big, v_): big[:] = K.dof(big, 6)
    b = A(C.brayden, *W(v, 760.0, 1960.0), 19.0, t=t, flip=True, expr='lazy', mouth_=mouth('brayden', t), look=(-0.6, 0.4), stick=False,
          hand_n=(8.0, 40.0))
    ro = A(C.roast, *W(v, 360.0, 1700.0), 34.0, t=t)
    return K.shot(LIV_B, light_liv, 900.0, 420.0, Z, acts=[b, ro], pre=pre)


# ================================================================== 3: WINDOWS — the TV stacks windows
def r_windows(t, u):
    def pre(big, v_): big[:] = K.dof(big, 9)
    big = K.shot(LIV, lambda v_: light_liv(v_, 1.0), 640.0, 420.0, 1.0, pre=pre)
    step = 1 + min(3, int((t - 9.34) / 0.8))
    screen_card(big, 'windows', t, y=360, step=step)
    jx = 1.0
    hand = A(C.randy, *W(V(LIV, 640.0, 420.0, 1.0), 300.0, 2500.0), 22.0, t=t, expr='losing', mouth_=0.0, look=(0.0, -0.8), mitt=False,
             hand_n=(14.0, 62.0), prop_n=lambda sp, h: C.cell(sp, h), sweat=1.0)
    hand(big, V(LIV, 640.0, 420.0, 1.0), None)
    return big


# ================================================================== 4: QUESTION — «Name of your first pet?»
def r_question(t, u):
    def pre(big, v_): big[:] = K.dof(big, 9)
    big = K.shot(LIV, lambda v_: light_liv(v_, 1.0), 640.0, 420.0, 1.0, pre=pre)
    screen_card(big, 'question', t, y=300)
    a = A(C.randy, *W(V(LIV, 640.0, 420.0, 1.0), 640.0, 2620.0), 22.0, t=t, expr='nervous', mouth_=0.0, look=(0.2, -0.9), mitt=False,
          hand_n=(14.0, 62.0), prop_n=lambda sp, h: C.cell(sp, h), sweat=1.0)
    a(big, V(LIV, 640.0, 420.0, 1.0), None)
    return big


# ================================================================== 5: TOM? — CU, unsure
def r_tom(t, u):
    big, a = K.cu(C.randy, t, LIV, 330.0, 300.0, 1.3, 24.0 + 1.0 * u, head=(560, 980), light=lambda v_: light_liv(v_, 1.0), blur=5, flip=True,
                  pre_fx=lambda b, v_: tv(b, v_, 'question', t), expr='nervous', mouth_=mouth('randy', t), look=(0.6, 0.4), mitt=False,
                  hand_n=(14.0, 60.0), prop_n=lambda sp, h: C.cell(sp, h), sweat=1.0)
    return big


# ================================================================== 6: FREEZER — Tom: «We never met.»
def r_freezer(t, u):
    Z = 1.4
    v = V(KIT_B, 160.0, 230.0, Z)
    s = 22.0
    def pre(big, v_):
        ox0, oy0 = v_.opt(FREEZER[0] + 10, FREEZER[1] + 10); ox1, oy1 = v_.opt(FREEZER[2] - 10, FREEZER[3] - 6)
        X0, X1, Y0, Y1 = int(max(0, ox0)), int(min(OUT_W, ox1)), int(max(0, oy0)), int(min(OUT_H, oy1))
        big[Y0:Y1, X0:X1] = (150, 190, 220)
        big[Y0 + 20:Y1 - 20, X0 + 20:X1 - 20] = (120, 160, 200)
        for q in range(0, X1 - X0, 60): big[Y0:Y0 + 30, X0 + q:X0 + q + 20] = (236, 246, 255)
    tom = A(C.tom, *W(v, 560.0, 1240.0), s, t=t, expr='dead', mouth_=mouth('tom', t, 1.6), look=(-0.2, -0.2))
    def f(big, v_):
        K.cold_vapor(big, 600, 860, t, 1.0, 1.6)
        K.thaw_meter(big, t, 16.6, 17.85, 'ROCK', x=900, y=1400)
    return K.shot(KIT_B, None, 160.0, 230.0, Z, acts=[tom], pre=pre, fx_=f)


# ================================================================== 7: TWIST — SUPPORT PLUS
def r_twist(t, u):
    def pre(big, v_): big[:] = K.dof(big, 9)
    big = K.shot(LIV, lambda v_: light_liv(v_, 1.0), 640.0, 420.0, 1.0, pre=pre)
    K.alarm_tint(big, t, 0.35)
    screen_card(big, 'locked', t, y=420)
    if u < 0.3: K.CK.shake(big, t, 14, 40)
    return big


# ================================================================== 8: KNEES — «I just want to watch the GAME!»
def r_knees(t, u):
    Z = 1.05
    cx = 470.0
    v = V(LIV, cx, 420.0, Z)
    s = WS * Z * 3
    r = A(C.randy, 400.0, FLOOR + 40.0, s, t=t, flip=True, expr='cry', mouth_=mouth('randy', t), legs=False, look=(1.0, -0.4), mitt=False,
          hand_n=(16.0, 70.0), hand_f=(10.0, 70.0), tremble=0.6)
    j = A(C.joyce, *JOY, s, t=t, expr='dead', look=(-0.8, 0.4), purse=None)
    def f(big, v_):
        tv(big, v_, 'locked', t)
        j(big, v_, light_liv(v_))
        table_front(big, v_)
        r(big, v_, light_liv(v_, 1.0))
    return K.shot(LIV, lambda v_: light_liv(v_, 1.0), cx, 420.0, Z, fx_=f)


# ================================================================== 9: CABLE — Nana pulls a 1998 TV out of her purse
def r_cable(t, u):
    Z = 1.3
    cx = 560.0
    v = V(LIV, cx, 395.0, Z)
    s = WS * Z * 3
    out = sm((t - 25.2) / 0.6)
    j = A(C.joyce, *JOY, s, t=t, expr='fine' if speaking('joyce', t) else 'smug', mouth_=mouth('joyce', t), look=(-0.6, 0.0), purse='side',
          hand_n=(8.0, 20.0 + 10 * out), prop_n=(lambda sp, h: C.tiny_tv(sp, h, t)) if out > 0.05 else None)
    r = A(C.randy, 470.0, FLOOR + 40.0, s, t=t, expr='stunned', mouth_=0.2, legs=False, look=(1.0, -0.6), mitt=False)
    def f(big, v_):
        j(big, v_, light_liv(v_))
        table_front(big, v_)
        r(big, v_, light_liv(v_))
    return K.shot(LIV, light_liv, cx, 395.0, Z, fx_=f)


# ================================================================== 10: FINAL — the tiny screen: «Spoiler. We lost.»
def r_final(t, u):
    Z = 1.35
    v = V(LIV_B, 600.0, 400.0, Z)
    def pre(big, v_): big[:] = K.dof(big, 6)
    big = K.shot(LIV_B, light_liv, 600.0, 400.0, Z, pre=pre)
    sp_s = 70.0
    tt = A(C.tiny_tv, *W(v, 300.0, 1500.0), sp_s, t=t, h=(0.0, 0.0))
    tt(big, v, None)
    sx, sy = aout(tt, v, 'tiny_screen')
    f = O.pfont(56)
    im = Image.fromarray(big); from PIL import ImageDraw; d = ImageDraw.Draw(im); d.fontmode = '1'
    d.text((sx - f.getlength('FINAL') / 2, sy - 40), 'FINAL', font=f, fill=(255, 255, 255), stroke_width=4, stroke_fill=(0, 0, 0))
    d.text((sx - O.pfont(30).getlength('MF 0 : EVERYBODY 63') / 2, sy + 40), 'MF 0 : EVERYBODY 63', font=O.pfont(30), fill=(255, 214, 60),
           stroke_width=3, stroke_fill=(0, 0, 0))
    big[:] = np.array(im)
    b = A(C.brayden, *W(v, 880.0, 1960.0), 18.0, t=t, flip=True, expr='dead', mouth_=mouth('brayden', t), look=(-0.6, 0.6), stick=False)
    b(big, v, light_liv(v))
    return big


# ================================================================== 11: THANKS — the family, deadpan: «Thanks, Randy.»
def r_thanks(t, u):
    Z = 1.3
    v = V(LIV_B, 640.0, 380.0, Z)
    def pre(big, v_): big[:] = K.dof(big, 6)
    m = mouth('family', t)
    acts = [A(C.joyce, *W(v, 330.0, 1500.0), 22.0, t=t, expr='dead', mouth_=m, look=(0.0, 0.0), purse=None,
              hand_n=(8.0, 20.0), prop_n=lambda sp, h: C.tiny_tv(sp, h, t)),
            A(C.brayden, *W(v, 760.0, 2140.0), 19.0, t=t, flip=True, expr='dead', mouth_=m, look=(0.0, 0.0), stick=False)]
    big = K.shot(LIV_B, light_liv, 640.0, 380.0, Z, acts=acts, pre=pre)
    if t > 31.85: screen_card(big, 'paywall', t, y=300)
    return big


R = [r_hook, r_table, r_tag, r_windows, r_question, r_tom, r_freezer, r_twist, r_knees, r_cable, r_final, r_thanks]
assert len(R) == len(CUTS) - 1 == len(NAMES)

SHOW = K.Show(EPI, 5, ['$30 FOR', 'FOOTBALL?!'], hook_t=(0.10, 1.95), hook_y=300, hook_size=84,
              day=(2.10, 5.10, 'THURSDAY 6:00 PM', 'TURKEY DAY', 1650),
              stickers=[(K.st("KIDS' TABLE (HE'S 24)", fg=(255, 214, 80), size=50), 7.40, 9.25, 600, 1240),
                        (K.st('STEP 4 OF 47', fg=(255, 120, 120), size=56), 11.80, 12.60, 540, 1380),
                        (K.st('SUPPORT+ $29.99', fg=(200, 150, 255), size=62), 18.20, 22.10, 540, 1260)],
              flashes=[TWIST], mosaics=[],
              cap_y={0: 1600, 1: 1650, 2: 1000, 3: 1250, 4: 1640, 5: 1600, 6: 560, 7: 1500, 8: 1600, 9: 1620, 10: 560, 11: 1680})


def render(t):
    i = max(0, min(len(R) - 1, int(np.searchsorted(CUTS, t, side='right')) - 1))
    big = R[i](t, t - CUTS[i])
    return SHOW.apply(big, t, i)


if __name__ == '__main__':
    EPI.main(render, __file__)
