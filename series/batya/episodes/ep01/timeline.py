"""E01 «37,2 — ПОМИРАЮ!» — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot)   a line (voice/ep01_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'batya'
EP = 'ep01'
FPS = 30
LUFS = -14.0
VEP = 'ep01_t'
S = f'series/{SLUG}/sfx/'
C = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
VFX = {}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(b1='помираю!', t1='третий', b2='не', b3='пульт!', i1='помирай.', b4='болею!', i2='работу.', b5='сам!', b6='пять',
            t3='второй', i3='Спасибо.', b7='тридцать')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').replace('[pause]', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper(), 1) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'b1', 'hook'), ('L', 't1', 'selfie'), ('L', 'b2', 'will'), ('L', 'b3', 'bell'), ('L', 'i1', 'ira_in'), ('P', 0.45, 'sneeze'),
    ('L', 'b4', 'cover'), ('L', 'i2', 'twist'), ('L', 'b5', 'jump'), ('L', 'b6', 'kitchen'), ('L', 't3', 'smoke'), ('L', 'i3', 'taste'),
    ('L', 'b7', 'button'), ('P', 0.3, 'loop'),
]
PAD = 0.07
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
CUTS = [s['t0'] for s in SHOTS] + [DUR]
NAMES = [s['name'] for s in SHOTS]
T0 = {s['name']: s['t0'] for s in SHOTS}
T1 = {s['name']: s['t1'] for s in SHOTS}
TWIST = T0['twist']

SFX = [
    (S + 'thermo_beep.mp3', 0.0, 0.45), (C + 'cloth_rustle.mp3', 0.3, 0.35),
    (C + 'phone_key_click.mp3', T0['selfie'] + 0.05, 0.5),
    (S + 'handbell_ring.mp3', T0['will'] + 0.25, 0.4), (C + 'cloth_rustle.mp3', T0['will'] + 1.6, 0.35),
    (S + 'handbell_ring.mp3', T0['bell'], 0.55), (S + 'handbell_ring.mp3', T0['bell'] + 1.3, 0.5),
    (C + 'door_apartment_open.mp3', T0['ira_in'] - 0.1, 0.45), (C + 'slipper_steps.mp3', T0['ira_in'] + 0.3, 0.45),
    (C + 'bottle_clink.mp3', T0['ira_in'] + 1.7, 0.35),
    (S + 'sneeze_woman.mp3', T0['sneeze'] - 0.05, 0.85),
    (C + 'cloth_rustle.mp3', T0['cover'] + 0.05, 0.55),
    (S + 'thermo_beep.mp3', TWIST - 0.02, 0.75), (C + 'vinyl_scratch.mp3', TWIST + 0.3, 0.4),
    (C + 'whoosh_1.mp3', T0['jump'], 0.7), (C + 'boing_cartoon.mp3', T0['jump'] + 0.15, 0.4), (C + 'gong_strong.mp3', T0['jump'] + 0.3, 0.3),
    (S + 'pot_boil.mp3', T0['kitchen'], 0.4), (C + 'bottle_clink.mp3', T0['kitchen'] + 0.5, 0.35),
    (S + 'pot_boil.mp3', T0['smoke'], 0.45), (C + 'whoosh_3.mp3', T0['smoke'] + 0.7, 0.3), (C + 'whoosh_3.mp3', T0['smoke'] + 1.4, 0.3),
    (C + 'bottle_clink.mp3', T0['taste'] + 0.5, 0.3),
    (C + 'chair_creak.mp3', T0['button'] + 0.5, 0.5),
    (S + 'thermo_beep.mp3', T0['loop'], 0.35),
]

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.7:g=-7,equalizer=f=3200:t=q:w=1:g=-4'   # carve the voice band out of the music
BEDS = [
    (CM + 'komiku_mandolin.mp3', 59.5, 0.0, TWIST, 0.8, True, VOICE_DIP),
    (CM + 'komiku_fetch_contest.mp3', 41.5, TWIST + 0.25, DUR, 0.8, True, VOICE_DIP),
]
VGAIN = {'batya': 2.0, 'tema': 2.1, 'ira': 2.1}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
