"""S02E01 «Плюс четырнадцать» — timing for video (s2e01.py) and audio (mix.py). Built from BEATS like the movies:
  ('L', key, shot)   a line (voice/s2e01_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'valera-i-kot'
EP = 's2e01'
FPS = 30
MASTER = 0.8
VEP = 's2e01_t'
S = 'library/sfx/'
MUS = f'series/{SLUG}/music/'
PHONE = 'highpass=f=320,lowpass=f=3200,acompressor=threshold=0.2:ratio=4,volume=1.25'
VFX = {'nina': PHONE}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(v1='ДОМА?!', c1='Предатель.', v2='уставу!', n1='графику.', v3='графику?!', n2='отопительному.', v4='ответите!',
            n3='открыто.', v5='вентиляция.', c3='Сквозняк.', c4='Пишите.', v6='здоровья!')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper()) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'v1', 'hook'), ('L', 'c1', 'cat_cold'), ('L', 'v2', 'valve'), ('P', 0.35, 'puff'),
    ('L', 'n1', 'nina1'), ('L', 'v3', 'v_phone'), ('L', 'n2', 'nina2'), ('L', 'v4', 'v_shout'),
    ('L', 'n3', 'reveal'), ('L', 'v5', 'v_proud'), ('L', 'c3', 'cat_dry'), ('P', 0.45, 'slam'),
    ('L', 'c4', 'cat_warm'), ('L', 'v6', 'reopen'), ('P', 0.6, 'loop'),
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


TWIST = first('reveal')['t0']
T0 = {s['name']: s['t0'] for s in SHOTS}

SFX = [
    (S + 'wind_gust.mp3', 0.0, 0.5), (S + 'teeth_chatter.mp3', 0.15, 0.55),
    (S + 'wind_gust.mp3', T0['cat_cold'] + 0.3, 0.3),
    (S + 'valve_creak.mp3', T0['valve'] + 0.4, 0.5), (S + 'steam_hiss_soft.mp3', T0['puff'] - 0.1, 0.7),
    (S + 'sad_trombone.mp3', T0['puff'] + 0.25, 0.25),
    (S + 'phone_pickup.mp3', T0['nina1'], 0.7), (S + 'bath_splash.mp3', T0['nina1'] + 0.6, 0.35),
    (S + 'fist_slam_counter.mp3', T0['v_shout'] + 0.3, 0.6),
    (S + 'record_scratch.mp3', TWIST, 0.45), (S + 'hurricane_wind_howl.mp3', TWIST + 0.2, 0.35),
    (S + 'chair_slam_snow.mp3', T0['slam'] + 0.05, 0.9), (S + 'pipes_rumble.mp3', T0['slam'] + 0.35, 0.45),
    (S + 'pencil_scribble.mp3', T0['cat_warm'] + 0.3, 0.6),
    (S + 'wind_gust.mp3', T0['reopen'] + 0.2, 0.6), (S + 'teeth_chatter.mp3', T0['loop'], 0.5),
]

BEDS = [
    (S + 'amb_flat_winter.mp3', 7.8, 0.0, T0['nina1'], 0.45, False),
    (MUS + 'theme_panelka_15s.mp3', 14.6, 0.0, TWIST, 0.2, True),
    (S + 'amb_office_night.mp3', 7.8, T0['nina1'], T0['v_shout'], 0.25, False),
    (S + 'amb_flat_winter.mp3', 7.8, T0['v_shout'], DUR, 0.5, False),
    (MUS + 'operation_sneaky_15s.mp3', 14.6, TWIST + 0.4, DUR, 0.2, True),
]
VGAIN = {'valera': 1.5, 'cat': 1.55, 'nina': 1.45}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
