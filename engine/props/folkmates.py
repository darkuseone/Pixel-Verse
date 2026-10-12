"""Valera's drinking buddies for «Валера и кот: ПРОПУСКНОЙ РЕЖИМ»: Колян (huge, silent, tracksuit «АБИБАС», flat cap, broken nose,
gold tooth, only says «Ну.») and Семёныч (ex-literature teacher: beret, round glasses, grey spade beard, tweed jacket with elbow
patches, long red scarf, red nose). Costumes: Колян -> «snegurochka» (blue fur-trimmed coat, kokoshnik, yellow sponge braids,
stubble), Семёныч -> «ded_moroz» (red coat + hat, his own beard). Same conventions as folk.py: anchor = floor point,
H(x, h) unit coords, +x = facing; pose dicts like folk.VPOSE (IK hand targets)."""
import math
from scene import Layer
from props.folk import H, cap, ell, ellt, dot, poly, outline, _limb, _merge, band_mask, recolor, VPOSE, OL

KP = dict(skin=(232, 178, 140), skin_hi=(248, 204, 170), skin_sh=(196, 138, 106), stub=(204, 160, 136),
          suit=(40, 52, 96), suit_hi=(62, 76, 130), suit_sh=(26, 34, 66), stripe=(236, 238, 244),
          cap=(104, 96, 86), cap_hi=(134, 126, 114), cap_sh=(76, 70, 62), brow=(60, 46, 36), eye=(26, 20, 18),
          white=(240, 238, 232), gold=(250, 206, 70), shoe=(230, 232, 236), shoe_sh=(170, 176, 190), sole=(70, 70, 76),
          sneg=(120, 176, 236), sneg_hi=(160, 206, 250), sneg_sh=(84, 132, 196), fur=(246, 248, 252), fur_sh=(200, 210, 226),
          braid=(250, 214, 80), braid_sh=(214, 170, 50), koko=(70, 110, 220), koko_hi=(130, 170, 250), pearl=(255, 255, 255))
SP = dict(skin=(236, 190, 160), skin_hi=(250, 214, 188), skin_sh=(200, 150, 124), nose=(222, 104, 96), nose_hi=(246, 150, 136),
          beard=(214, 214, 210), beard_hi=(240, 240, 236), beard_sh=(170, 170, 168), brow=(200, 200, 196),
          tweed=(132, 104, 72), tweed_hi=(160, 130, 94), tweed_sh=(98, 76, 52), patch=(90, 70, 50), shirt=(226, 222, 206),
          scarf=(70, 100, 130), scarf_hi=(100, 132, 164), scarf_sh=(46, 70, 96), beret=(44, 44, 52), beret_hi=(70, 70, 80),
          pants=(70, 66, 62), pants_hi=(92, 88, 82), pants_sh=(52, 48, 46), shoe=(60, 40, 30), frame=(40, 34, 30),
          glass=(210, 230, 240), eye=(30, 24, 22), white=(244, 242, 236), book=(150, 40, 40), book_pg=(240, 232, 210),
          dm=(204, 36, 40), dm_hi=(236, 70, 70), dm_sh=(150, 20, 26), fur=(246, 248, 252), fur_sh=(200, 210, 226))


STAND = dict(VPOSE['stand'], n=(5.0, 9.6), f=(-3.6, 9.8), bn=1, bf=-1)


def _expr_eyes(Hd, eyes, expr, P, look, t, blink=True, small=False):
    ex = 0.12 * look
    bl = blink and (t % 4.1) < 0.12
    for e_, r in eyes:
        if expr == 'blissful' or bl:
            cap(Hd, (e_[0] - r, e_[1] + 0.05), (e_[0] + r, e_[1] - 0.02), 0.12, 0.12, P['eye']); continue
        if expr in ('squint', 'sly', 'smug'):
            ell(Hd, e_, r * 1.1, r * 0.5, P['white']); dot(Hd, (e_[0] + 0.1 + ex, e_[1] + 0.02), P['eye'], r * 0.45)
            cap(Hd, (e_[0] - r * 1.1, e_[1] - r * 0.45), (e_[0] + r * 1.1, e_[1] - r * 0.5), 0.12, 0.12, P['skin_sh']); continue
        big = expr in ('shock', 'shout')
        rr = r * (1.3 if big else 1.0)
        ell(Hd, e_, rr, rr * (0.8 if small and not big else 1.05), P['white'])
        dot(Hd, (e_[0] + 0.08 + ex, e_[1] + 0.03), P['eye'], rr * (0.42 if big else 0.55))
        dot(Hd, (e_[0] + 0.02 + ex, e_[1] - 0.1), (255, 255, 255), rr * 0.17)


def _mouth(Hd, mc, mouth, expr, gold=None, lips=(150, 70, 60)):
    m = max(mouth, {'shout': 0.8, 'shock': 0.6}.get(expr, 0.0))
    if m > 0.08:
        ell(Hd, mc, 0.6 + 0.3 * m, 0.2 + 0.7 * m, (90, 28, 28))
        ell(Hd, (mc[0] + 0.1, mc[1] + 0.3 * m), 0.4 + 0.2 * m, 0.15 + 0.2 * m, (196, 96, 96))
        cap(Hd, (mc[0] - 0.45, mc[1] - 0.2 - 0.25 * m), (mc[0] + 0.5, mc[1] - 0.2 - 0.25 * m), 0.14, 0.14, (240, 236, 220))
        if gold: dot(Hd, (mc[0] + 0.25, mc[1] - 0.2 - 0.25 * m), gold, 0.2)
    elif expr in ('smug', 'sly', 'blissful', 'happy'):
        cap(Hd, (mc[0] - 0.55, mc[1] - 0.1), (mc[0] + 0.55, mc[1] + 0.12), 0.13, 0.13, lips)
        if gold: dot(Hd, (mc[0] + 0.2, mc[1] + 0.05), gold, 0.18)
    elif expr in ('sad', 'angry'):
        cap(Hd, (mc[0] - 0.55, mc[1] + 0.12), (mc[0] + 0.55, mc[1] - 0.05), 0.13, 0.13, lips)
    else:
        cap(Hd, (mc[0] - 0.5, mc[1]), (mc[0] + 0.5, mc[1]), 0.12, 0.12, lips)


def _rig(CH, cam, pose, t, P, dims, top, legc, footc, head, hand_n=None, hand_f=None, prop_n=None, prop_f=None, skirt=None,
         over=None, lean=0.0, stripes=None):
    """shared body: legs -> far arm -> torso (+skirt) -> head -> overlay (beard/scarf) -> near arm"""
    pose = pose or STAND
    br = 0.16 * math.sin(t * 2.0)
    sw, shh, hip, al, ar, lr, tw, th = dims          # shoulder half-width, shoulder height, hip height, arm len, arm radius, leg radius,
    ln = lean                                        # torso half-width, torso half-height
    sh_n, sh_f = H(sw * 0.8 + ln, shh + br), H(-sw * 0.9 + ln, shh + 0.2 + br)
    hp_n, hp_f = H(1.4, hip), H(-1.3, hip)
    L = Layer(cam)
    A = Layer(cam)
    fl = VPOSE['stand']['fleg'] if pose.get('fleg') is None else pose['fleg']
    kf, ef = _limb(A, hp_f, *fl, hip * 0.5, hip * 0.48, lr, lr * 0.78, *legc)
    ellt(A, (ef[0] + 0.9, ef[1] + 0.35), 1.9, 0.85, footc)
    _merge(L, A)
    A = Layer(cam)
    tf = hand_f if hand_f is not None else H(pose['f'][0], pose['f'][1])
    ka, ea = _limb(A, sh_f, 0, 0, al, al * 0.93, ar, ar * 0.8, *top, target=tf, bend=pose.get('bf', -1))
    ell(A, ea, 1.15, 1.08, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_f: prop_f(A, ea)
    _merge(L, A)
    A = Layer(cam)
    ellt(A, H(0.2, hip + 0.6), tw * 0.72, 2.3, legc)
    kn, en = _limb(A, hp_n, *pose['nleg'], hip * 0.5, hip * 0.48, lr * 1.05, lr * 0.8, *legc)
    ellt(A, (en[0] + 0.9, en[1] + 0.35), 2.0, 0.9, footc)
    if stripes:
        for kk, (o, e) in enumerate(((hp_n, kn), (kn, en))):
            cap(A, (o[0] + 0.15, o[1]), (e[0] + 0.15, e[1]), 0.18, 0.18, stripes)
    _merge(L, A)
    T = Layer(cam)
    bc = H(0.9 + ln * 0.3, (hip + shh) / 2 + 0.6 + br * 0.5)
    ellt(T, bc, tw, th, top)
    ellt(T, H(0.2 + ln, shh - 0.8 + br), sw + 0.6, 2.6, top)
    if skirt: skirt(T, bc)
    _merge(L, T)
    Hd = Layer(cam)
    res = head(Hd, br, ln)
    _merge(L, Hd)
    if over:
        O = Layer(cam); over(O, br, ln); _merge(L, O)
    A = Layer(cam)
    tn = hand_n if hand_n is not None else H(pose['n'][0], pose['n'][1])
    kna, ena = _limb(A, sh_n, 0, 0, al, al * 0.93, ar * 1.03, ar * 0.82, *top, target=tn, bend=pose.get('bn', 1))
    if stripes:
        cap(A, (sh_n[0] + 0.2, sh_n[1]), (kna[0] + 0.2, kna[1]), 0.2, 0.2, stripes)
        cap(A, (kna[0] + 0.2, kna[1]), (ena[0] + 0.2, ena[1]), 0.2, 0.2, stripes)
    ell(A, ena, 1.2, 1.12, P['skin'], 0, P['skin_hi'], P['skin_sh'])
    if prop_n: prop_n(A, ena)
    _merge(L, A)
    outline(L, OL)
    CH.add(L)
    res = dict(res or {}); res.update(hand_n=ena, hand_f=ea)
    return res


# ======================================================================================= КОЛЯН
def kolyan(CH, cam, pose=None, t=0.0, mouth=0.0, expr='normal', costume=None, look=0.0, hand_n=None, hand_f=None, prop_n=None,
           prop_f=None, lean=0.0, cold=0.0):
    """expr: normal | happy | sad | shock | sly | blissful | squint; costume: None (tracksuit) | snegurochka"""
    P = dict(KP)
    if cold > 0:
        for k in ('skin', 'skin_hi', 'skin_sh'):
            P[k] = tuple(int(c * (1 - 0.4 * cold) + b * 0.4 * cold) for c, b in zip(P[k], (176, 206, 255)))
    sneg = costume == 'snegurochka'
    top = [P['sneg'], P['sneg_hi'], P['sneg_sh']] if sneg else [P['suit'], P['suit_hi'], P['suit_sh']]
    legc = [P['suit'], P['suit_hi'], P['suit_sh']]
    footc = (P['shoe'], P['shoe'], P['shoe_sh'])

    def head(Hd, br, ln):
        hx = 1.0 + ln * 1.2
        def F(x, h): return H(hx + x - 1.0, h + br)
        if sneg:                                                                                # sponge braids BEHIND the head
            for bx in (-1.9, 3.3):
                for k in range(6):
                    ell(Hd, F(bx + 0.12 * k * (1 if bx < 0 else 0.4), 24.4 - k * 1.25), 0.72, 0.62, P['braid'], 0, None, P['braid_sh'])
                cap(Hd, F(bx + 0.3, 17.0), F(bx + 0.3, 16.2), 0.5, 0.2, (226, 60, 70))
        cap(Hd, F(0.6, 20.0), F(0.8, 22.0), 2.4, 2.3, P['skin'], P['skin_hi'], P['skin_sh'])          # bull neck
        ell(Hd, F(1.1, 23.6), 2.75, 3.0, P['skin'], 0.05, P['skin_hi'], P['skin_sh'])                # small head
        ell(Hd, F(1.9, 21.6), 2.2, 1.25, P['skin'], 0, None, P['skin_sh'])                           # square jaw
        ell(Hd, F(2.0, 21.5), 2.0, 1.0, P['stub'], 0.05)                                             # stubble
        ell(Hd, F(-1.0, 23.4), 0.65, 0.95, P['skin'], 0, None, P['skin_sh'])                         # ear
        eyes = [(F(1.6 + 0.1 * look, 24.0), 0.3), (F(2.75 + 0.1 * look, 23.95), 0.36)]
        _expr_eyes(Hd, eyes, expr, P, look, t, small=True)
        bt = {'sad': -0.4, 'shock': -0.5, 'happy': 0.0, 'angry': 0.5}.get(expr, 0.15)
        cap(Hd, F(1.0, 24.65 - bt * 0.2), F(3.4, 24.6 + bt * 0.2), 0.32, 0.3, P['brow'])            # unibrow
        poly(Hd, [F(3.2, 24.1), F(4.15, 23.0), F(3.7, 22.6), F(3.05, 22.9)], P['skin_sh'])            # broken nose
        ell(Hd, F(3.7, 22.85), 0.55, 0.4, P['skin'], 0, P['skin_hi'], P['skin_sh'])
        mc = F(3.0, 21.75)
        _mouth(Hd, mc, mouth, expr, gold=P['gold'], lips=(140, 80, 64))
        if sneg:                                                                                # kokoshnik + sponge braids
            poly(Hd, [F(-1.6, 25.6), F(-0.6, 28.6), F(1.2, 29.6), F(3.0, 28.6), F(3.8, 25.6)], P['koko'])
            cap(Hd, F(-1.6, 25.6), F(3.8, 25.6), 0.35, 0.35, P['fur'])
            for k in range(7): dot(Hd, F(-0.6 + k * 0.62, 27.0 + 0.9 * math.sin(k / 6 * math.pi)), P['pearl'], 0.22)
        else:                                                                                   # flat cap (кепка)
            ell(Hd, F(0.9, 25.7), 3.2, 1.25, P['cap'], -0.06, P['cap_hi'], P['cap_sh'])
            cap(Hd, F(2.0, 25.0), F(4.7, 24.6), 0.55, 0.3, P['cap_sh'])
            dot(Hd, F(0.6, 26.6), P['cap_sh'], 0.25)
        return dict(head=F(1.6, 23.4), mouth=mc)

    def skirt(T, bc):
        if sneg:                                                                                # long fur-trimmed coat
            poly(T, [H(-3.4, 15.0), H(4.4, 15.0), H(5.4, 4.2), H(-4.0, 4.2)], P['sneg'])
            cap(T, H(-4.0, 4.4), H(5.4, 4.4), 0.7, 0.7, P['fur'])
            cap(T, H(1.2, 19.6), H(1.4, 4.6), 0.55, 0.55, P['fur'])
        else:                                                                                   # chest logo + zip
            cap(T, H(1.6, 19.6), H(1.6, 10.6), 0.1, 0.1, P['stripe'])
            for k in range(3): cap(T, H(2.9 + k * 0.35, 18.0), H(3.1 + k * 0.35, 17.0 + 0.2 * k), 0.12, 0.12, P['stripe'])

    dims = (4.4, 19.4, 10.2, 4.5, 1.75, 2.05, 6.0, 5.2)
    return _rig(CH, cam, pose, t, P, dims, top, legc, footc, head, hand_n, hand_f, prop_n, prop_f, skirt=skirt, lean=lean,
                stripes=None if sneg else P['stripe'])


# ======================================================================================= СЕМЁНЫЧ
def semenych(CH, cam, pose=None, t=0.0, mouth=0.0, expr='normal', costume=None, look=0.0, hand_n=None, hand_f=None, prop_n=None,
             prop_f=None, lean=0.0, cold=0.0):
    """expr: normal | smug | sad | shock | blissful | squint | shout; costume: None | ded_moroz"""
    P = dict(SP)
    if cold > 0:
        for k in ('skin', 'skin_hi', 'skin_sh'):
            P[k] = tuple(int(c * (1 - 0.4 * cold) + b * 0.4 * cold) for c, b in zip(P[k], (176, 206, 255)))
    dm = costume == 'ded_moroz'
    top = [P['dm'], P['dm_hi'], P['dm_sh']] if dm else [P['tweed'], P['tweed_hi'], P['tweed_sh']]
    legc = [P['dm'], P['dm_hi'], P['dm_sh']] if dm else [P['pants'], P['pants_hi'], P['pants_sh']]
    footc = (P['shoe'], P['shoe'], P['shoe'])

    def head(Hd, br, ln):
        hx = 0.9 + ln * 1.2
        def F(x, h): return H(hx + x - 0.9, h + br)
        cap(Hd, F(0.4, 16.8), F(0.6, 18.6), 1.3, 1.3, P['skin'], P['skin_hi'], P['skin_sh'])
        ell(Hd, F(0.8, 20.6), 2.55, 3.1, P['skin'], -0.05, P['skin_hi'], P['skin_sh'])               # long head
        ell(Hd, F(-1.1, 20.4), 0.6, 0.9, P['skin'], 0, None, P['skin_sh'])
        eyes = [(F(1.45 + 0.1 * look, 21.2), 0.3), (F(2.6 + 0.1 * look, 21.15), 0.36)]
        for (e_, r) in eyes:                                                                    # round glasses
            ell(Hd, e_, 0.66, 0.66, P['frame']); ell(Hd, e_, 0.54, 0.54, P['glass'])
        _expr_eyes(Hd, eyes, expr, P, look, t)
        cap(Hd, (eyes[0][0][0] + 0.6, eyes[0][0][1]), (eyes[1][0][0] - 0.6, eyes[1][0][1]), 0.08, 0.08, P['frame'])
        bt = {'sad': -0.45, 'shock': -0.55, 'smug': 0.3, 'squint': 0.3}.get(expr, 0.0)
        for k2, (e_, r) in enumerate(eyes):                                                       # bushy grey brows
            b = e_[1] - 0.95 - (0.3 if expr in ('shock', 'shout') else 0)
            s_ = 1 if k2 == 0 else -1
            cap(Hd, (e_[0] - 0.6, b - s_ * bt * 0.3), (e_[0] + 0.65, b + s_ * bt * 0.3), 0.3, 0.24, P['brow'])
        ell(Hd, F(3.5, 20.15), 0.85, 0.75, P['nose'], 0, P['nose_hi'], None)                       # red nose
        ell(Hd, F(2.0, 19.9), 0.55, 0.35, (230, 150, 140))
        mc = F(2.7, 18.95)
        if dm:                                                                                   # Ded Moroz hat
            ell(Hd, F(0.8, 23.3), 3.0, 1.9, P['dm'], 0, P['dm_hi'], P['dm_sh'])
            cap(Hd, F(-2.1, 22.4), F(3.6, 22.4), 0.75, 0.75, P['fur'], None, P['fur_sh'])
        else:                                                                                    # beret
            ell(Hd, F(0.6, 23.3), 3.0, 1.05, P['beret'], -0.15, P['beret_hi'], None)
            dot(Hd, F(0.5, 24.35), P['beret'], 0.3)
            cap(Hd, F(-1.6, 22.6), F(-1.9, 21.4), 0.35, 0.25, P['beard_sh'])                       # grey tuft
        return dict(head=F(1.2, 20.6), mouth=mc)

    def over(O, br, ln):
        hx = 0.9 + ln * 1.2
        def F(x, h): return H(hx + x - 0.9, h + br)
        if not dm:                                                                               # scarf under the beard
            cap(O, F(-0.6, 17.4), F(2.4, 17.2), 1.0, 1.0, P['scarf'], P['scarf_hi'], P['scarf_sh'])
            cap(O, F(2.0, 17.0), F(2.8, 11.2 + 0.3 * math.sin(t * 2)), 0.75, 0.6, P['scarf'], P['scarf_hi'], P['scarf_sh'])
            for k in range(3): cap(O, F(2.4 + 0.25 * k, 11.3), F(2.5 + 0.25 * k, 10.6), 0.08, 0.08, P['scarf_sh'])
        m = max(mouth, {'shout': 0.8, 'shock': 0.6}.get(expr, 0.0))
        ell(O, F(2.3, 18.2), 2.1, 1.9, P['beard'], 0, P['beard_hi'], P['beard_sh'])                   # bushy grey spade beard
        ell(O, F(2.5, 16.4), 1.7, 1.6, P['beard'], 0.1, P['beard_hi'], P['beard_sh'])
        ell(O, F(2.7, 14.9 - 0.4 * m), 1.0, 1.1, P['beard'], 0.15, P['beard_hi'], P['beard_sh'])
        for k in range(5): cap(O, F(1.2 + 0.6 * k, 18.6 - 0.2 * k), F(1.6 + 0.45 * k, 15.6 - 0.3 * k), 0.06, 0.06, P['beard_sh'])
        cap(O, F(1.9, 19.6), F(3.7, 19.6), 0.4, 0.3, P['beard_hi'])                                  # moustache
        mc = F(2.7, 18.95)
        if m > 0.08: ell(O, (mc[0], mc[1] + 0.1), 0.5 + 0.2 * m, 0.15 + 0.5 * m, (90, 28, 28))
        elif expr in ('smug', 'blissful'): cap(O, (mc[0] - 0.4, mc[1]), (mc[0] + 0.45, mc[1] - 0.15), 0.1, 0.1, (110, 60, 50))

    def skirt(T, bc):
        if dm:
            poly(T, [H(-3.0, 13.0), H(3.8, 13.0), H(4.4, 3.0), H(-3.4, 3.0)], P['dm'])
            cap(T, H(-3.4, 3.2), H(4.4, 3.2), 0.65, 0.65, P['fur'])
            cap(T, H(1.0, 16.6), H(1.2, 3.4), 0.5, 0.5, P['fur'])
        else:
            poly(T, [H(0.6, 16.8), H(2.4, 16.6), H(1.7, 11.0)], P['shirt'])                       # shirt V
            for (x, h) in ((-0.8, 12.8), (2.6, 12.0)): dot(T, H(x, h), P['tweed_sh'], 0.18)        # tweed flecks
            dot(T, H(1.9, 9.8), P['tweed_sh'], 0.15)

    def arm_patch(A, e):
        pass

    dims = (3.3, 16.8, 8.4, 3.8, 1.2, 1.45, 4.2, 4.5)
    return _rig(CH, cam, pose, t, P, dims, top, legc, footc, head, hand_n, hand_f, prop_n, prop_f, skirt=skirt, over=over,
                lean=lean)


def book(L, h, open_=False):
    x, y = h
    if open_:
        poly(L, [(x - 2.0, y - 1.0), (x, y - 0.6), (x, y + 1.0), (x - 2.0, y + 0.6)], SP['book_pg'])
        poly(L, [(x, y - 0.6), (x + 2.0, y - 1.0), (x + 2.0, y + 0.6), (x, y + 1.0)], SP['book_pg'])
        for k in range(3): cap(L, (x - 1.7, y - 0.5 + k * 0.4), (x - 0.3, y - 0.3 + k * 0.4), 0.05, 0.05, (120, 110, 100))
    else:
        poly(L, [(x - 0.4, y - 2.0), (x + 1.4, y - 2.0), (x + 1.4, y + 0.8), (x - 0.4, y + 0.8)], SP['book'])
        cap(L, (x + 1.3, y - 1.9), (x + 1.3, y + 0.7), 0.12, 0.12, SP['book_pg'])


def jar(L, h, s=1.0, label=True):
    """3-litre jar of «компот» (cherry red) with a plastic lid"""
    x, y = h[0], h[1] - 1.6 * s
    ell(L, (x, y), 1.6 * s, 2.2 * s, (150, 30, 50), 0, (200, 70, 90), (110, 20, 36))
    cap(L, (x - 1.0 * s, y - 2.3 * s), (x + 1.0 * s, y - 2.3 * s), 0.45 * s, 0.45 * s, (236, 236, 240))
    ell(L, (x - 0.7 * s, y - 0.6 * s), 0.35 * s, 1.1 * s, (236, 150, 170))
    if label: poly(L, [(x - 1.1 * s, y - 0.3 * s), (x + 1.1 * s, y - 0.3 * s), (x + 1.1 * s, y + 0.8 * s), (x - 1.1 * s, y + 0.8 * s)], (240, 232, 210))


def sheet_mound(L, c, s=1.0, t=0.0, sneakers=True):
    """a «сугроб»: a man crawling under a white bedsheet, «АБИБАС» sneakers sticking out at the back"""
    x, y = c
    wob = 0.2 * math.sin(t * 6)
    ell(L, (x, y - 1.6 * s + wob * s), 4.6 * s, 2.3 * s, (240, 244, 252), 0, (255, 255, 255), (200, 210, 228))
    ell(L, (x + 3.2 * s, y - 2.2 * s + wob * s), 1.7 * s, 1.6 * s, (240, 244, 252), 0, (255, 255, 255), (200, 210, 228))
    cap(L, (x - 4.0 * s, y - 0.6 * s), (x + 4.4 * s, y - 0.4 * s), 0.6 * s, 0.6 * s, (206, 216, 232))
    if sneakers:
        for k in (0, 1):
            ell(L, (x - 5.0 * s - k * 0.4 * s, y - 0.5 * s - k * 0.9 * s), 1.0 * s, 0.55 * s, (236, 238, 244), 0, None, (170, 176, 190))
            for j in range(3): cap(L, (x - 5.5 * s + j * 0.3 * s - k * 0.4 * s, y - 0.8 * s - k * 0.9 * s),
                                   (x - 5.3 * s + j * 0.3 * s - k * 0.4 * s, y - 0.3 * s - k * 0.9 * s), 0.06 * s, 0.06 * s, (40, 52, 96))
