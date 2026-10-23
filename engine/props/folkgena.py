"""Гена, Valera's upstairs neighbour (season 2): endless DIY renovation «since 2019». Short, round, bare hairy belly over grey sweatpants
held by a belt with a yellow tape measure, an orange hard hat, eyebrows and cheeks white with plaster dust, red cheeks, a wide grin
with one missing tooth, double chin, worn brown slippers. Unlike Valera (telnyashka, ushanka, walrus moustache) and Колян (tracksuit,
flat cap, unibrow) — no moustache, no clothes on top, a helmet. Prop: `perforator` (red rotary hammer held like a guitar), `shelf`.
Same conventions as folk.py / folkmates.py: anchor = floor point, H(x, h) unit coords, +x = facing."""
import math
from props.folk import H, cap, ell, ellt, dot, poly, VPOSE
from props.folkmates import _rig, _expr_eyes, _mouth

GP = dict(skin=(238, 184, 150), skin_hi=(252, 210, 180), skin_sh=(200, 140, 112), cheek=(236, 120, 110), hair=(70, 52, 40),
          dust=(236, 232, 222), pants=(128, 130, 136), pants_hi=(156, 158, 164), pants_sh=(96, 98, 104), belt=(60, 44, 34),
          tape=(250, 204, 40), tape_sh=(200, 150, 20), hat=(250, 128, 30), hat_hi=(255, 170, 70), hat_sh=(200, 90, 20),
          slip=(120, 74, 44), slip_hi=(150, 100, 64), slip_sh=(84, 50, 30), brow=(230, 226, 214), eye=(30, 22, 20), white=(244, 240, 232),
          drill=(206, 40, 36), drill_hi=(240, 80, 70), drill_sh=(150, 24, 22), metal=(170, 176, 186), metal_sh=(110, 114, 124),
          grip=(40, 40, 46), wood=(176, 130, 80), wood_hi=(206, 160, 104), wood_sh=(136, 96, 56))

# perforator held across the belly like a guitar: near hand on the grip, far hand on the side handle
GUITAR = dict(VPOSE['stand'], n=(4.6, 12.6), f=(3.2, 15.2), bn=1, bf=1)
DRILL = dict(VPOSE['stand'], n=(5.8, 17.0), f=(7.6, 18.2), bn=1, bf=1, nleg=(0.3, 0.0), fleg=(-0.3, 0.0))   # drilling the wall ahead


def gena(CH, cam, pose=None, t=0.0, mouth=0.0, expr='happy', look=0.0, hand_n=None, hand_f=None, prop_n=None, prop_f=None,
         lean=0.0, dust=1.0, hat=True):
    """expr: happy | normal | shout | shock | squint | sad"""
    P = dict(GP)
    top = [P['skin'], P['skin_hi'], P['skin_sh']]
    legc = [P['pants'], P['pants_hi'], P['pants_sh']]
    footc = (P['slip'], P['slip_hi'], P['slip_sh'])

    def head(Hd, br, ln):
        hx = 1.0 + ln * 1.2
        def F(x, h): return H(hx + x - 1.0, h + br + 1.3)
        cap(Hd, F(0.8, 18.8), F(1.0, 20.8), 2.1, 2.0, P['skin'], P['skin_hi'], P['skin_sh'])          # thick neck
        ell(Hd, F(1.6, 20.2), 2.4, 1.3, P['skin'], 0, P['skin_hi'], P['skin_sh'])                      # double chin
        ell(Hd, F(1.2, 23.0), 3.4, 3.3, P['skin'], 0.0, P['skin_hi'], P['skin_sh'])                    # round head
        ell(Hd, F(-1.4, 23.0), 0.7, 1.0, P['skin'], 0, None, P['skin_sh'])                             # ear
        ell(Hd, F(3.0, 22.3), 0.9, 0.6, P['cheek'])                                                    # red cheeks
        ell(Hd, F(0.9, 22.4), 0.8, 0.55, P['cheek'])
        eyes = [(F(1.5 + 0.1 * look, 23.2), 0.46), (F(2.85 + 0.1 * look, 23.15), 0.5)]
        _expr_eyes(Hd, eyes, 'normal' if expr == 'happy' else expr, P, look, t)
        bt = {'sad': -0.4, 'shock': -0.6, 'shout': -0.3, 'angry': 0.5}.get(expr, -0.1)
        for bx in (1.6, 2.9):                                                                           # bushy brows white with plaster
            cap(Hd, F(bx - 0.6, 24.0 - bt * 0.2), F(bx + 0.6, 24.05 + bt * 0.2), 0.3, 0.28, P['hair'])
            if dust > 0.3:
                for q in (-0.35, 0.1, 0.45): dot(Hd, F(bx + q, 24.1), P['brow'], 0.14)
        ell(Hd, F(3.7, 22.4), 0.62, 0.5, P['skin'], 0, P['skin_hi'], P['skin_sh'])                     # potato nose
        mc = F(2.6, 21.5)
        m = max(mouth, 0.35 if expr == 'happy' else 0.0)
        _mouth(Hd, mc, m, 'shout' if expr == 'shout' else expr)
        if m > 0.08:                                                                                    # the missing tooth
            dot(Hd, (mc[0] + 0.15, mc[1] - 0.2 - 0.25 * m), (90, 28, 28), 0.18)
        for k in range(5):                                                                              # stubble dots
            dot(Hd, F(1.7 + 0.5 * k, 20.6 + 0.25 * (k % 2)), P['skin_sh'], 0.13)
        if dust > 0:
            for (dx, dh) in ((3.4, 21.9), (0.2, 21.6), (1.9, 21.4)):
                dot(Hd, F(dx, dh), P['dust'], 0.2 * dust)
        if hat:                                                                                         # orange hard hat with a ridge
            ell(Hd, F(1.1, 26.1), 3.7, 2.2, P['hat'], 0, P['hat_hi'], P['hat_sh'])
            cap(Hd, F(-2.7, 25.0), F(5.2, 24.9), 0.5, 0.45, P['hat_sh'])
            cap(Hd, F(1.1, 28.0), F(1.1, 25.3), 0.35, 0.35, P['hat_hi'])
        return dict(head=F(1.6, 23.2), mouth=mc)

    def skirt(T, bc):                                                                                   # the belly
        ell(T, H(2.4, 13.6), 5.4, 4.6, P['skin'], 0, P['skin_hi'], P['skin_sh'])
        dot(T, H(4.0, 12.8), P['skin_sh'], 0.28)                                                        # navel
        for k in range(7):                                                                              # chest / belly hair
            dot(T, H(1.6 + 0.7 * (k % 3), 18.0 - 1.1 * k), P['hair'], 0.14)
        ell(T, H(1.8, 17.6), 1.2, 0.8, P['dust'])                                                       # plaster dust patch
        cap(T, H(-3.8, 9.6), H(6.8, 9.6), 0.75, 0.75, P['belt'])                                       # belt under the belly
        ell(T, H(-1.2, 9.4), 1.1, 1.1, P['tape'], 0, None, P['tape_sh'])                               # tape measure
        dot(T, H(-1.2, 9.4), P['tape_sh'], 0.35)

    dims = (3.9, 18.4, 9.4, 4.4, 1.7, 2.0, 6.0, 5.2)
    return _rig(CH, cam, pose, t, P, dims, top, legc, footc, head, hand_n, hand_f, prop_n, prop_f, skirt=skirt, lean=lean)


def perforator(L, hand, ang=0.0, spin=0.0, P=GP, k=1.0):
    """red rotary hammer: pistol grip in the hand, motor body forward along ang (rad, 0 = +x), a long bit; k = scale"""
    c, s = math.cos(ang), math.sin(ang)
    def A(f, u): return (hand[0] + (c * f - s * u) * k, hand[1] + (s * f + c * u) * k)   # f = along the tool, u = down (screen)
    def cp(a, b, r0, r1, *col): cap(L, a, b, r0 * k, r1 * k, *col)
    cp(A(0.0, 0.0), A(0.4, -1.8), 0.55, 0.6, P['grip'])                                                  # grip
    cp(A(-1.0, -2.3), A(3.4, -2.3), 1.15, 1.0, P['drill'], P['drill_hi'], P['drill_sh'])              # body
    cp(A(3.4, -2.3), A(4.4, -2.3), 0.6, 0.5, P['metal'], None, P['metal_sh'])                         # chuck
    j = 0.08 * math.sin(spin * 60)
    cp(A(4.4, -2.3 + j), A(8.6, -2.3 + j), 0.22, 0.16, P['metal'], None, P['metal_sh'])               # bit
    for q in range(3): dot(L, A(5.0 + 1.2 * q, -2.3 + j + 0.12 * ((q + int(spin * 30)) % 2)), P['metal_sh'], 0.12 * k)
    cp(A(0.6, -3.6), A(1.8, -3.6), 0.25, 0.25, P['grip'])                                                # top vent
    cp(A(2.4, -1.4), A(2.6, 0.6), 0.32, 0.32, P['grip'])                                                 # side handle


def shelf(L, a, b, P=GP):
    """a raw wooden shelf plank between two points (unit coords)"""
    cap(L, a, b, 0.45, 0.45, P['wood'], P['wood_hi'], P['wood_sh'])


def hardhat(L, top, P=GP):
    """Gena's orange hard hat put on someone else's head; top = the rig's 'top' point (unit coords of the same cam)"""
    x, y = top
    ell(L, (x + 0.2, y + 1.0), 3.7, 2.1, P['hat'], 0, P['hat_hi'], P['hat_sh'])
    cap(L, (x - 3.3, y + 2.5), (x + 4.4, y + 2.4), 0.5, 0.5, P['hat_sh'])
    cap(L, (x + 0.2, y - 1.0), (x + 0.2, y + 1.9), 0.35, 0.35, P['hat_hi'])
