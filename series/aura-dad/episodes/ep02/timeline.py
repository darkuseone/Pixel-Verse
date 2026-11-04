"""S01E02 «$340 SKINCARE?!» — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot, pad)   a line (voice/ep01_t/<key>.mp3) followed by pad seconds (negative = the next line overlaps)"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'aura-dad'
EP = 'ep02'
FPS = 30
LUFS = -14.0
VEP = 'ep02_t'
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
    ('L', 'l1', 'hook', 0.05), ('L', 'd1', 'doug_cu', 0.05), ('L', 'd2', 'march', 0.05), ('L', 's1', 'counter', 0.05),
    ('L', 'd3', 'twist', 0.55), ('L', 't1', 'tammy', 0.08), ('L', 'd4', 'spray', 0.0), ('L', 's2', 'price', 0.15),
    ('L', 'd5', 'masks', 0.05), ('L', 'm1', 'button', 0.25),
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
    (S + 'receipt_unroll.mp3', 0.25, 0.9), (C + 'boing_cartoon.mp3', 1.4, 0.25),
    (S + 'aura_down.mp3', T0['doug_cu'] + 0.05, 0.3), (C + 'cloth_rustle.mp3', T0['doug_cu'] + 0.1, 0.6),
    (C + 'whoosh_1.mp3', T0['march'] - 0.1, 0.45), (S + 'bag_crinkle.mp3', T0['march'] + 0.2, 0.8), (S + 'bag_crinkle.mp3', T0['march'] + 1.5, 0.7),
    (C + 'slipper_steps.mp3', T0['march'] + 0.1, 0.5, 0.0, 2.5),
    (S + 'register_beep.mp3', T0['counter'] + 0.3, 0.7), (S + 'register_beep.mp3', T0['counter'] + 2.6, 0.6),
    (S + 'twist_sting.mp3', TWIST + 0.9, 1.6), (C + 'vinyl_scratch.mp3', TWIST + 0.85, 0.35), (C + 'whoosh_3.mp3', TWIST + 0.95, 0.5),
    (C + 'canvas_bag_drop.mp3', T0['tammy'] + 0.3, 0.4),
    (S + 'spray_mist.mp3', T0['spray'] + 0.15, 0.9), (S + 'dome_twinkle.mp3', T0['spray'] + 0.9, 0.6),
    (S + 'register_beep.mp3', T0['price'] + 0.1, 0.7), (S + 'aura_down.mp3', T0['price'] + 0.6, 0.45),
    (S + 'sheet_mask.mp3', T0['masks'] - 0.1, 1.2), (S + 'sheet_mask.mp3', T0['masks'] + 0.25, 1.0),
    (C + 'sms_message.mp3', T0['button'] - 0.05, 0.45), (S + 'aura_down.mp3', T0['button'] + 2.1, 0.6),
    (C + 'rimshot_joke.mp3', DUR - 1.05, 0.45),
]

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.8:g=-10,equalizer=f=3200:t=q:w=1:g=-7,equalizer=f=500:t=q:w=1:g=-4'
BEDS = [
    (CM + 'komiku_shoe_shop.mp3', 59.5, 0.0, TWIST + 0.8, 0.45, True, VOICE_DIP),
    (CM + 'komiku_fetch_contest.mp3', 59.5, TWIST + 1.2, DUR, 0.5, True, VOICE_DIP),
    (S + 'amb_birds_desert.mp3', 8.0, 0.0, T0['march'], 3.5, True),
    (S + 'amb_mall_store.mp3', 8.0, T0['march'], T0['masks'], 0.5, True),
]
VGAIN = {'doug': 1.7, 'kayden': 1.9, 'tammy': 2.0, 'mirra': 1.8, 'lily': 1.8, 'skylar': 2.0}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
