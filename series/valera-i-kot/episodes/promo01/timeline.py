"""PROMO 01 «Курс» — ad for the course (stories / reels), ~24 s. Timing for video (promo01.py) and audio (mix.py).
  ('L', key, shot)   a line (voice/promo01_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'valera-i-kot'
EP = 'promo01'
FPS = 30
MASTER = 0.68
LUFS = -14.0
VEP = 'promo01_t'
S = 'library/sfx/'
MUS = f'series/{SLUG}/music/'
X = f'series/{SLUG}/sfx/'
VFX = {}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(v1='не умею!', c1='художник.', v2='кто?!', v3='телефона?!', c3='любой.', v4='продюсер!', c4='справился.')
CAPS = dict(c2='Claude. С ТЕЛЕФОНА.')                 # the TTS reads «Кло́д», the subtitle shows the product name


def _cap(k):
    if k in CAPS: return CAPS[k]
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper()) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'v1', 'hook'), ('L', 'c1', 'cat1'), ('L', 'v2', 'v_q'), ('L', 'c2', 'phone'), ('P', 2.0, 'phone2'),
    ('L', 'v3', 'reveal'), ('L', 'c3', 'cat_ad'), ('L', 'v4', 'v_proud'), ('L', 'c4', 'button'), ('P', 0.3, 'button2'),
]
PAD = 0.1
SHOTS, VOICE = [], []
t = 0.0
for b in BEATS:
    if b[0] == 'L':
        k = b[1]; d = CLIP[k] + PAD
        VOICE.append((k, VEP, k, round(t + 0.02, 3), 0.0, CLIP[k], LINES[k][0], _cap(k)))
        SHOTS.append(dict(name=b[2], t0=t, t1=t + d, key=k))
    else:
        d = b[1]; SHOTS.append(dict(name=b[2], t0=t, t1=t + d))
    t += d
DUR = round(t, 3)
CUTS = [s['t0'] for s in SHOTS]
NAMES = [s['name'] for s in SHOTS]
T0 = {s['name']: s['t0'] for s in SHOTS}
TWIST = T0['reveal']

SFX = [
    (S + 'paper_crumple_slap.mp3', 0.0, 0.55), (S + 'pencil_scribble.mp3', 0.15, 0.35),
    (S + 'cat_meow.mp3', T0['cat1'] + 0.05, 0.25),
    (S + 'record_scratch.mp3', T0['v_q'], 0.35),
    (S + 'app_notify_ping.mp3', T0['phone'] + 0.3, 0.5), (S + 'ui_tap_chirp.mp3', T0['phone'] + 1.1, 0.25),
    (S + 'app_notify_ping.mp3', T0['phone2'] + 0.2, 0.45),
    (S + 'camera_glitch.mp3', TWIST, 0.6), (S + 'slowmo_whoosh.mp3', TWIST + 0.05, 0.55), (S + 'choir_hallelujah_short.mp3', TWIST + 0.4, 0.3),
    (S + 'title_stinger.mp3', T0['cat_ad'] + 0.2, 0.4),
    (S + 'boots_stomp.mp3', T0['v_proud'] + 0.1, 0.5), (S + 'brass_fanfare_short.mp3', T0['v_proud'] + 1.2, 0.3),
    (S + 'sad_trombone.mp3', T0['button'] + 1.0, 0.3),
]
BEDS = [
    (S + 'amb_flat_winter.mp3', 7.8, 0.0, TWIST, 0.3, False),
    (MUS + 'operation_sneaky_15s.mp3', 14.6, 0.0, TWIST, 0.22, True),
    (MUS + 'theme_panelka_15s.mp3', 14.6, TWIST + 0.3, DUR, 0.22, True),
    (S + 'amb_flat_winter.mp3', 7.8, T0['cat_ad'], DUR, 0.3, False),
]
VGAIN = {'valera': 1.5, 'cat': 1.55}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
