"""S01E06 «AURA BATTLE?!» — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot, pad)   a line (voice/ep01_t/<key>.mp3) followed by pad seconds (negative = the next line overlaps)"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'aura-dad'
EP = 'ep06'
FPS = 30
LUFS = -14.0
VEP = 'ep06_t'
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
    ('L', 'k1', 'hook', 0.05), ('L', 'd1', 'vow', 0.05), ('L', 'j1', 'score', 0.05),
    ('P', 1.5, 'mew', 0), ('L', 'k2', 'win', 0.1), ('L', 'b2', 'prize', 0.15), ('L', 't1', 'tammy', 0.05),
    ('L', 'd2', 'proud', 0.05), ('L', 'k3', 'loop', 0.35),
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
TWIST = T0['prize']
REVEAL = TWIST + 2.4

SFX = [
    (S + 'notif_burst.mp3', 0.3, 0.5), (C + 'whoosh_1.mp3', T0['vow'] - 0.05, 0.35), (S + 'dome_twinkle.mp3', T0['vow'] + 1.5, 0.5),
    (C + 'gong_strong.mp3', T0['score'] + 0.05, 0.3),
    (S + 'aura_up.mp3', T0['score'] + 0.5, 0.6), (S + 'aura_down.mp3', T0['score'] + 2.2, 0.5),
    (S + 'cheeks_puff.mp3', T0['mew'] + 0.1, 0.9), (S + 'notif_burst.mp3', T0['mew'] + 1.0, 0.8), (S + 'aura_up.mp3', T0['mew'] + 1.2, 0.8),
    (C + 'boing_cartoon.mp3', T0['win'] + 0.2, 0.3),
    (S + 'twist_sting.mp3', TWIST + 2.4, 1.5), (C + 'vinyl_scratch.mp3', TWIST + 2.35, 0.35),
    (S + 'register_beep.mp3', T0['tammy'] + 0.3, 0.6), (S + 'register_beep.mp3', T0['tammy'] + 0.7, 0.6),
    (S + 'dome_twinkle.mp3', T0['proud'] + 0.8, 0.7),
    (S + 'phone_scan.mp3', T0['loop'], 0.7), (S + 'aura_down.mp3', T0['loop'] + 2.6, 0.6), (C + 'car_arrive_stop.mp3', T0['loop'] + 0.3, 0.5),
    (C + 'rimshot_joke.mp3', DUR - 1.05, 0.45),
]

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.8:g=-10,equalizer=f=3200:t=q:w=1:g=-7,equalizer=f=500:t=q:w=1:g=-4'
BEDS = [
    (CM + 'komiku_weekly_fair.mp3', 59.5, 0.0, TWIST, 0.45, True, VOICE_DIP),
    (CM + 'komiku_fetch_contest.mp3', 59.5, TWIST + 0.5, DUR, 0.5, True, VOICE_DIP),
    (S + 'amb_mall_store.mp3', 8.0, 0.0, DUR, 0.35, True),
    (S + 'amb_birds_desert.mp3', 8.0, 0.0, DUR, 3.0, True),
]
VGAIN = {'doug': 1.7, 'kayden': 1.9, 'tammy': 2.0, 'mirra': 1.8, 'lily': 1.8, 'skylar': 2.0, 'jaxon': 1.9, 'brett': 1.8}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}', 'reveal', f'{REVEAL / DUR:.0%}')
