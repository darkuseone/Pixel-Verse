"""S02E06 «Плюс тридцать» — timing for video (s2e06.py) and audio (mix.py). Built from BEATS like the movies:
  ('L', key, shot)   a line (voice/s2e06_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'valera-i-kot'
EP = 's2e06'
FPS = 30
MASTER = 0.68
VEP = 's2e06_t'
S = 'library/sfx/'
MUS = f'series/{SLUG}/music/'
MUFFLE = 'lowpass=f=1500,volume=1.3'
SEPIA = 'aecho=0.8:0.6:60:0.25,highpass=f=200'
PHONE = 'highpass=f=320,lowpass=f=3200,acompressor=threshold=0.2:ratio=4,volume=1.25'
VFX = {'nina': PHONE}
X = f'series/{SLUG}/sfx/'

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(v1='Дома?!', c1='Слишком.', n1='графику.', v3='меньше!', n2='графику.', g1='Жарко?!', z1='Курорт!', v4='один!',
            v5='уставу.', c2='Предатель.', v6='Холодно!', n3='открыто.', c3='цифру.', v7='Дома?!')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper()) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'v1', 'hook'), ('L', 'c1', 'cat_melt'), ('L', 'n1', 'nina1'), ('L', 'v3', 'v_phone'), ('L', 'n2', 'nina2'),
    ('L', 'g1', 'gena'), ('L', 'z1', 'resort'), ('L', 'v4', 'v_exit'), ('L', 'v5', 'window'), ('L', 'c2', 'cat_cold'),
    ('L', 'v6', 'v_cold'), ('L', 'n3', 'nina3'), ('L', 'c3', 'cat_log'), ('L', 'v7', 'loop'),
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


def first(name):
    return next(s for s in SHOTS if s['name'] == name)


TWIST = first('window')['t0']
T0 = {s['name']: s['t0'] for s in SHOTS}

SFX = [
    (S + 'pipes_rumble.mp3', 0.0, 0.5), (S + 'steam_hiss_soft.mp3', 0.2, 0.4),
    (S + 'water_drip_single.mp3', T0['cat_melt'] + 1.2, 0.6),
    (S + 'phone_pickup.mp3', T0['nina1'], 0.6), (S + 'bath_splash.mp3', T0['nina1'] + 0.6, 0.3),
    (S + 'phone_slam.mp3', T0['nina2'] + 1.9, 0.35),
    (X + 'hammer_drill_wall.mp3', T0['gena'], 0.25), (S + 'seagull.mp3', T0['resort'], 0.25),
    (S + 'boots_stomp.mp3', T0['v_exit'] + 0.3, 0.5),
    (S + 'valve_creak.mp3', TWIST, 0.6), (S + 'hurricane_wind_howl.mp3', TWIST + 0.1, 0.45), (S + 'choir_hallelujah_short.mp3', TWIST + 0.3, 0.3),
    (S + 'wind_gust.mp3', T0['cat_cold'], 0.6), (S + 'teeth_chatter.mp3', T0['v_cold'], 0.5),
    (S + 'phone_pickup.mp3', T0['nina3'], 0.5), (S + 'record_scratch.mp3', T0['nina3'] + 0.2, 0.3),
    (S + 'pencil_scribble.mp3', T0['cat_log'] + 0.4, 0.6), (S + 'book_thud.mp3', T0['cat_log'] + 4.2, 0.5),
    (S + 'wind_gust.mp3', T0['loop'], 0.5), (S + 'teeth_chatter.mp3', T0['loop'] + 0.15, 0.5),
]

BEDS = [
    (S + 'amb_flat_winter.mp3', 7.8, 0.0, T0['nina1'], 0.3, False),
    (MUS + 'theme_panelka_15s.mp3', 14.6, 0.0, TWIST, 0.2, True),
    (S + 'amb_office_night.mp3', 7.8, T0['nina1'], T0['gena'], 0.22, False),
    (S + 'amb_winter_yard.mp3', 7.8, T0['gena'], T0['v_exit'], 0.3, False),
    (S + 'amb_flat_winter.mp3', 7.8, T0['v_exit'], DUR, 0.45, False),
    (MUS + 'new_year_15s.mp3', 14.6, TWIST + 0.2, DUR, 0.18, True),
]
VGAIN = {'valera': 1.5, 'cat': 1.55, 'nina': 1.45, 'gena': 1.45, 'zina': 1.45}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
