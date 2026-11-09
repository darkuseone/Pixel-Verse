"""E06 «ДЕНЬ МАТЕРИ — ПОДАРОК САМИ!» — timing for video (ep01.py) and audio (mix.py). Built from BEATS:
  ('L', key, shot)   a line (voice/ep01_t/<key>.mp3) + PAD;   ('P', sec, shot)   a silent beat"""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'batya'
EP = 'ep06'
FPS = 30
LUFS = -14.0
VEP = 'ep06_t'
S = f'series/{SLUG}/sfx/'
C = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
VFX = {}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(b1='матери!', t1='слабых.', b2='алмаз!', t2='Три', b3='штатив!', g1='мне?!', b4='Иры…', i1='сама.', g2='горячий!',
            b5='два…')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').replace('[pause]', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper(), 1) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('L', 'b1', 'hook'), ('L', 't1', 'selfie'), ('L', 'b2', 'measure'), ('L', 't2', 'stool'), ('L', 'b3', 'tripod'),
    ('L', 'g1', 'twist'), ('L', 'b4', 'mama'), ('L', 'i1', 'table'), ('L', 'g2', 'forehead'), ('L', 'b5', 'button'),
    ('P', 0.3, 'loop'),
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
    (C + 'canvas_bag_drop.mp3', 0.0, 0.25), (C + 'cloth_rustle.mp3', 0.2, 0.3), (C + 'cloth_rustle.mp3', 0.9, 0.3),
    (C + 'whoosh_1.mp3', T0['selfie'], 0.25),
    (C + 'suitcase.mp3', T0['measure'] + 0.4, 0.2),
    (C + 'chair_creak.mp3', T0['stool'] + 0.3, 0.4), (C + 'chair_creak.mp3', T0['stool'] + 1.2, 0.4), (C + 'boing_cartoon.mp3', T0['stool'] + 1.8, 0.12),
    (C + 'chair_creak.mp3', T0['tripod'] + 0.5, 0.3),
    (C + 'door_apartment_open.mp3', TWIST - 0.15, 0.3), (C + 'vinyl_scratch.mp3', TWIST + 0.05, 0.35), (C + 'snow_steps.mp3', TWIST + 0.3, 0.2),
    (S + 'handbell_ring.mp3', T0['table'] + 0.2, 0.08), (C + 'bottle_clink.mp3', T0['table'] + 1.0, 0.2),
    (C + 'cloth_rustle.mp3', T0['forehead'] + 0.3, 0.3),
    (S + 'thermo_beep.mp3', T0['button'] + 0.1, 0.06), (C + 'rimshot_joke.mp3', T0['button'] + 1.4, 0.2),
]

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.7:g=-7,equalizer=f=3200:t=q:w=1:g=-4'   # carve the voice band out of the music
BEDS = [
    (CM + 'komiku_weekly_fair.mp3', 59.5, 0.0, TWIST, 0.5, True, VOICE_DIP),
    (CM + 'happy_lullaby.mp3', 39.0, TWIST + 0.25, DUR, 0.5, True, VOICE_DIP),
]
VGAIN = {'batya': 2.0, 'tema': 2.1, 'ira': 2.1, 'sosed': 2.0, 'kurier': 2.0, 'babushka': 2.1}
VNORM = -16.0        # every line levelled to -16 LUFS before the mix (owner 09.11: voices were quiet under music and SFX)

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
