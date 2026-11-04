"""S01E05 «$200 HAIR?!» — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot, pad)   a line (voice/ep01_t/<key>.mp3) followed by pad seconds (negative = the next line overlaps)"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'aura-dad'
EP = 'ep05'
FPS = 30
LUFS = -14.0
VEP = 'ep05_t'
S = f'series/{SLUG}/sfx/'
C = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
VFX = {'mirra': 'highpass=f=140,aecho=0.6:0.35:22:0.12'}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = {}


def _cap(k):
    return ' '.join(LINES[k][1].split(']')[-1].replace('[pause]', '').split())


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'l1', 'hook', 0.05), ('L', 'd1', 'dream', 0.05), ('L', 'm1', 'label', 0.05), ('L', 'd2', 'pour', 0.5),
    ('P', 2.0, 'night', 0), ('L', 'd3', 'reveal', 0.5), ('P', 1.9, 'twist', 0), ('L', 'k1', 'kayden', 0.05),
    ('L', 't1', 'tammy', 0.05), ('L', 'd4', 'hair', 0.3), ('L', 'm2', 'button', 0.3),
]
SHOTS, VOICE = [], []
t = 0.0
for kind, k, name, pad in BEATS:
    if kind == 'P':
        SHOTS.append(dict(name=name, t0=t, t1=t + k)); t += k; continue
    d = CLIP[k] + pad
    VOICE.append((k, VEP, k, round(t + 0.02, 3), 0.0, CLIP[k], LINES[k][0], _cap(k)))
    SHOTS.append(dict(name=name, t0=t, t1=t + d, key=k))
    t += d
DUR = round(t, 3)
CUTS = [s['t0'] for s in SHOTS] + [DUR]
NAMES = [s['name'] for s in SHOTS]
T0 = {s['name']: s['t0'] for s in SHOTS}
T1 = {s['name']: s['t1'] for s in SHOTS}
TWIST = T0['twist']

SFX = [
    (S + 'dome_twinkle.mp3', 0.3, 0.5), (C + 'boing_cartoon.mp3', 2.2, 0.2),
    (S + 'aura_up.mp3', T0['dream'] + 0.2, 0.4),
    (C + 'whoosh_1.mp3', T0['label'] - 0.05, 0.35),
    (S + 'serum_glug.mp3', T0['pour'] + 0.4, 1.0), (C + 'boing_cartoon.mp3', T0['pour'] + 1.7, 0.3),
    (S + 'snore_dad.mp3', T0['night'] - 0.1, 0.8), (S + 'dog_nails.mp3', T0['night'] + 0.2, 0.5), (S + 'dog_lick.mp3', T0['night'] + 0.9, 1.0),
    (C + 'whoosh_3.mp3', T0['reveal'] - 0.1, 0.4), (C + 'cloth_rustle.mp3', T0['reveal'] + 2.4, 0.7), (S + 'aura_down.mp3', T0['reveal'] + 2.9, 0.4),
    (C + 'door_apartment_open.mp3', TWIST - 0.15, 0.5), (S + 'twist_sting.mp3', TWIST + 0.05, 1.4), (S + 'guitar_riff.mp3', TWIST + 0.3, 1.0),
    (S + 'dog_nails.mp3', TWIST + 0.4, 0.6),
    (S + 'hair_fall.mp3', T0['hair'] + 1.0, 1.0),
    (C + 'sms_message.mp3', T0['button'] - 0.05, 0.45), (S + 'aura_down.mp3', T0['button'] + 3.2, 0.6),
    (C + 'rimshot_joke.mp3', DUR - 1.05, 0.45),
]

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.8:g=-10,equalizer=f=3200:t=q:w=1:g=-7,equalizer=f=500:t=q:w=1:g=-4'
BEDS = [
    (CM + 'komiku_weekly_fair.mp3', 59.5, 0.0, T0['night'], 0.45, True, VOICE_DIP),
    (CM + 'happy_lullaby.mp3', 59.5, T0['night'], T0['reveal'], 0.35, True, VOICE_DIP),
    (CM + 'komiku_shoe_shop.mp3', 59.5, TWIST + 1.2, DUR, 0.5, True, VOICE_DIP),
]
VGAIN = {'doug': 1.7, 'kayden': 1.9, 'tammy': 2.0, 'mirra': 1.8, 'lily': 1.8, 'skylar': 2.0, 'jaxon': 1.9, 'brett': 1.8}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
