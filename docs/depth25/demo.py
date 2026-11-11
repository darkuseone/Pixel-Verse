"""Демо 2.5D-стиля на готовых задниках и герое Florida Man (правило владельца 11.11.2026):
    python3 docs/depth25/demo.py compare   -> docs/depth25/compare.png (по два кадра: как в сериях сейчас | 2.5D)
    python3 docs/depth25/demo.py clip      -> docs/depth25/demo.mp4 (5 с, два плана)
План 1 (0–2,6 с), крупный план в отделе деликатесов: голова приколота к точке кадра, как в ep02.cu, но фон с параллаксом и
размытием ПО ГЛУБИНЕ, прилавок сам закрывает героя ниже пояса (a.near — герой за прилавком), испуг: плавный переход,
моргание на смене эмоции, пот и линии шока, кик камеры. План 2 (2,6–5 с), вход в магазин: проезд с параллаксом
(парковка движется быстрее здания), ноги героя прячутся за кадкой с пальмой сами (глубина пола), радость с искоркой."""
import sys, pathlib, math, subprocess
ROOT = pathlib.Path(__file__).resolve().parents[2]; sys.path.insert(0, str(ROOT / 'engine'))
import numpy as np
from PIL import Image
import paths as P, stage as ST, depth25 as D25
from cam25 import Cam, kick
from props import fmkit as K, fmcast as C, chikit as CK, mimic as M

BG = P.series('florida-man') / 'bg'
DELI, STORE = K.world('deli'), K.world_baked('store')
D_DELI, D_STORE = D25.of(DELI, BG / 'deli.png'), D25.of(STORE, BG / 'store.png')
T2 = 2.6
CAM1 = Cam([(0.0, 640.0, 260.0, 1.35, -16.0, 0.0), (T2, 640.0, 262.0, 1.35, 16.0, 2.0)], creep=0.0, breathe=0.0)
CAM2 = Cam([(T2, 830.0, 452.0, 1.6, -26.0, 0.0), (4.4, 905.0, 452.0, 2.0, 20.0, 0.0), (5.0, 910.0, 452.0, 2.05, 22.0, 0.0)], creep=0.0012, breathe=3.0)
FACE = M.Face([(0.0, 'zen'), (1.25, 'shock'), (T2, 'nervous'), (3.7, 'cheer')], (C.XTRA, C.EXPR), seed=3)
HIT = [(1.25, 1.0)]


def talk(who, t):                                              # демо без голоса: «реплики» 0,2–1,1 и 3,8–4,8 с
    on = 0.2 < t < 1.1 or 3.8 < t < 4.8
    return (0.55 + 0.45 * math.sin(t * 23) * math.sin(t * 7.3)) if on else 0.0


def face_kw(t, smooth):
    if smooth:
        m = M.mouth(talk, 'fm', t)
        return dict(expr=FACE.speak(t, m), mouth_=m, blink=FACE.blink(t), look=FACE.look(t, (-0.5, 0.1))), M.bob(t, m)
    e = 'zen' if t < 1.25 else 'shock' if t < T2 else 'nervous' if t < 3.7 else 'cheer'   # как в сериях: скачок, моргание раз в 4,1 с
    return dict(expr=e, mouth_=min(1.0, talk('fm', t) * 1.8), look=(-0.5, 0.1)), 0.0


def manpu(t, a):
    def fx_(big, v):
        hx, hy = K.aout(a, v, 'head'); r = 7.5 * a.s_
        if 1.25 < t < T2: M.sweat(big, hx, hy, r, t, side=-1, t0=1.25, px=6); M.shock(big, hx, hy, r, px=6, k=min(1.0, (t - 1.25) * 5))
        if t > 3.75: M.sparkle(big, hx + r * 0.95, hy - r * 0.95, t, px=5)
    return fx_


def frame(t, new=True):
    if t < T2:                                                 # план 1: крупный план за прилавком
        cx, cy, Z, par = CAM1.at(t)
        v0 = ST.view_at(DELI, cx, cy, Z, 180, 320); hx, hy = K.wpt(v0, 540, 760)
        kw, dy = face_kw(t, new)
        a = K.A(C.fm, hx, hy + dy, 22.0, pin='head', t=t, **kw); a.s_ = 22.0
        if not new:
            return CK.shot(DELI, K.light_deli, cx, cy, Z, acts=[a], pre=lambda big, v: big.__setitem__(slice(None), K.dof(big, 6)), sx=180, sy=320)
        a.near = 0.12                                          # герой стоит за прилавком: всё, что ближе (прилавок, витрина), его закрывает
        return D25.shot25(DELI, K.light_deli, cx, cy, Z, D_DELI, acts=[a], par=par, focus=0.12, dof_k=42, haze_=None,
                          fx_=manpu(t, a), sx=180, sy=320, t=t, kick=kick(t, HIT))
    cx, cy, Z, par = CAM2.at(t)                                # план 2: вход в магазин, проезд
    kw, dy = face_kw(t, new)
    s_ = 5.6 * Z
    a = K.A(C.fm, 925.0, 506.0 + dy, s_, t=t, shadow=0.3, **kw); a.s_ = s_
    if not new:
        return CK.shot(STORE, K.light_store, cx, cy, Z, acts=[a], sx=180, sy=320)
    return D25.shot25(STORE, K.light_store, cx, cy, Z, D_STORE, acts=[a], par=par, haze_=((176, 214, 240), 0.35), eps=0.03,
                      fx_=manpu(t, a), sx=180, sy=320, t=t)


def compare(out=ROOT / 'docs' / 'depth25' / 'compare.png', ts=(1.6, 4.0)):
    tiles = [np.asarray(Image.fromarray(frame(t, new)).resize((540, 960), Image.LANCZOS)) for t in ts for new in (False, True)]
    Image.fromarray(np.concatenate(tiles, 1)).save(out); print(out)


def clip(out=ROOT / 'docs' / 'depth25' / 'demo.mp4', dur=5.0, fps=30):
    p = subprocess.Popen(['ffmpeg', '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{ST.OUT_W}x{ST.OUT_H}', '-r', str(fps), '-i', '-',
                          '-c:v', 'libx264', '-crf', '20', '-pix_fmt', 'yuv420p', str(out)], stdin=subprocess.PIPE)
    for f in range(int(dur * fps)):
        ST.T_NOW[0] = f / fps
        p.stdin.write(frame(f / fps).tobytes())
    p.stdin.close(); p.wait(); print(out)


if __name__ == '__main__':
    {'compare': compare, 'clip': clip}[sys.argv[1] if len(sys.argv) > 1 else 'compare']()
