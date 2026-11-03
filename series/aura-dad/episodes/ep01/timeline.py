"""S01E01 «MINUS 400?!» — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot, pad)   a line (voice/ep01_t/<key>.mp3) followed by pad seconds (negative = the next line overlaps)"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'aura-dad'
EP = 'ep01'
FPS = 30
LUFS = -14.0
VEP = 'ep01_t'
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
    ('L', 'k1', 'hook', 0.05), ('L', 'd1', 'doug_cu', 0.05), ('L', 'k2', 'jaw', 0.08), ('L', 'm1', 'mirra', -0.1),
    ('L', 'd3', 'mew', 0.1), ('L', 't1', 'tammy', 0.04), ('L', 'k3', 'twist', 0.0), ('L', 'd4', 'cheer', 0.05),
    ('L', 'k4', 'flat', 0.06), ('L', 'd5', 'proud', 0.0), ('L', 'm2', 'button', 0.15),
]
SHOTS, VOICE = [], []
t = 0.0
for kind, k, name, pad in BEATS:
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
    (S + 'phone_scan.mp3', 0.0, 0.7), (C + 'sms_message.mp3', 1.2, 0.5),
    (S + 'coffee_spit.mp3', T0['doug_cu'] + 0.15, 0.9), (S + 'aura_down.mp3', T0['doug_cu'] + 0.05, 0.25),
    (C + 'whoosh_1.mp3', T0['jaw'] - 0.1, 0.4), (S + 'phone_scan.mp3', T0['jaw'] + 0.3, 0.5),
    (C + 'phone_key_click.mp3', T0['jaw'] + 1.6, 0.6),
    (C + 'whoosh_3.mp3', T0['mirra'] - 0.1, 0.45), (S + 'aura_up.mp3', T0['mirra'] + 0.1, 0.35),
    (S + 'cheeks_puff.mp3', T0['mew'] + 0.0, 0.9), (C + 'boing_cartoon.mp3', T0['mew'] + 0.45, 0.35),
    (C + 'chair_creak.mp3', T0['tammy'] + 0.2, 0.5), (S + 'aura_up.mp3', T0['tammy'] + 2.0, 0.18),
    (S + 'twist_sting.mp3', TWIST, 1.6), (S + 'aura_up.mp3', TWIST + 0.05, 0.8), (C + 'vinyl_scratch.mp3', TWIST - 0.05, 0.35),
    (S + 'cheeks_puff.mp3', T0['cheer'] + 0.1, 0.6), (C + 'cloth_rustle.mp3', T0['cheer'] + 0.2, 0.6),
    (C + 'whoosh_1.mp3', T0['flat'] - 0.05, 0.35),
    (S + 'dome_twinkle.mp3', T0['proud'] + 0.9, 1.1), (C + 'cloth_rustle.mp3', T0['proud'] + 0.1, 0.6),
    (C + 'sms_message.mp3', T0['button'] - 0.1, 0.5), (S + 'aura_down.mp3', T0['button'] + 0.15, 0.75),
    (C + 'rimshot_joke.mp3', DUR - 1.05, 0.45),
]

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.7:g=-7,equalizer=f=3200:t=q:w=1:g=-4'
BEDS = [
    (CM + 'komiku_fetch_contest.mp3', 59.5, 0.0, TWIST, 0.8, True, VOICE_DIP),
    (CM + 'komiku_mandolin.mp3', 59.5, TWIST + 0.5, DUR, 0.85, True, VOICE_DIP),
    (S + 'amb_birds_desert.mp3', 8.0, 0.0, T0['mirra'], 3.5, True),
    (S + 'amb_birds_desert.mp3', 8.0, T0['tammy'], DUR, 4.5, True),
]
VGAIN = {'doug': 1.7, 'kayden': 1.9, 'tammy': 2.0, 'mirra': 1.8}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
