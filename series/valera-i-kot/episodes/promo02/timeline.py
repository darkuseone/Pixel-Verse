"""PROMO 02 «Курс» v2 — dynamic ad (stories / reels): a montage of real episode clips (RU + US series), then the cat, the phone demo,
Valera as a drill sergeant listing the benefits and the CTA. ('C', name) clip from a ready final.mp4 (its own picture + sound),
('L', key, shot) a new line (voice/promo02_t/<key>.mp3) + PAD, ('P', sec, shot) a silent beat."""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SLUG = 'valera-i-kot'
EP = 'promo02'
FPS = 30
MASTER = 0.68
LUFS = -14.0
VEP = 'promo02_t'
S = 'library/sfx/'
MUS = f'series/{SLUG}/music/'
VFX = {}

#        name      source final.mp4 (from ROOT)                         start  dur   label
CLIPS = {'cv_v':  ('series/valera-i-kot/episodes/ep02/final.mp4',        0.17, 1.00, 'ВАЛЕРА И КОТ · РУ'),
         'cv_m':  ('series/mazutych/episodes/ep01/final.mp4',            0.10, 1.55, 'МАЗУТЫЧ · РУ'),
         'cv_b':  ('series/valera-i-kot/episodes/ep03/final.mp4',        6.40, 1.70, 'БАБКИ НА ЛАВКЕ · РУ'),
         'cv_g':  ('series/grim-ride/episodes/ep01/final.mp4',           9.28, 2.10, 'GRIM RIDE · США')}

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / EP / 'lines.json'))
EMPH = dict(c1='телефон.', c2='серия.', v1='можно?!', c3='тебе.', v2='вечер!', v3='марш!', c4='лёжа.')


def _cap(k):
    c = ' '.join(LINES[k][1].split(']')[-1].replace('́', '').split())
    e = EMPH.get(k)
    return c.replace(e, e.upper()) if e and e in c else c


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}
V2_SPLIT = (1.31, 2.40)                               # «Без рисования! | С телефона! | Шесть серий за вечер!» (silencedetect)

BEATS = [('C', 'cv_v'), ('C', 'cv_m'), ('C', 'cv_b'), ('C', 'cv_g'),
         ('L', 'c1', 'cat1'), ('L', 'c2', 'phone'), ('P', 1.1, 'expand'),
         ('L', 'v2', 'drill'), ('L', 'v3', 'cta'), ('L', 'c4', 'button'), ('P', 0.25, 'button2')]
PAD = 0.08
SHOTS, VOICE, CLIP_SFX = [], [], []
t = 0.0
for b in BEATS:
    if b[0] == 'C':
        src, a, d, lab = CLIPS[b[1]]
        SHOTS.append(dict(name=b[1], t0=t, t1=t + d, src=src, a=a, label=lab))
        CLIP_SFX.append((f'series/{SLUG}/episodes/{EP}/clips/{b[1]}.wav', t, 1.0))
    elif b[0] == 'L':
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
TWIST = T0['expand']

SFX = CLIP_SFX + [
    (S + 'whoosh.mp3', T0['cv_m'] - 0.05, 0.35), (S + 'whoosh.mp3', T0['cv_b'] - 0.05, 0.35), (S + 'whoosh.mp3', T0['cv_g'] - 0.05, 0.35),
    (S + 'record_scratch.mp3', T0['cat1'], 0.4),
    (S + 'register_keys.mp3', T0['phone'] + 0.1, 0.35), (S + 'app_notify_ping.mp3', T0['phone'] + 2.2, 0.5),
    (S + 'slowmo_whoosh.mp3', TWIST, 0.55), (S + 'crowd_cheer_short.mp3', TWIST + 0.3, 0.3),
    (S + 'boots_stomp.mp3', T0['drill'], 0.5), (S + 'boots_stomp.mp3', T0['drill'] + V2_SPLIT[0], 0.5),
    (S + 'boots_stomp.mp3', T0['drill'] + V2_SPLIT[1], 0.5), (S + 'brass_fanfare_short.mp3', T0['drill'] + 3.2, 0.3),
    (S + 'police_whistle.mp3', T0['cta'] + 0.1, 0.3), (S + 'stairs_run.mp3', T0['cta'] + 1.8, 0.35), (S + 'snore.mp3', T0['button'] + 1.2, 0.25),
]
BEDS = [
    (MUS + 'operation_sneaky_15s.mp3', 14.6, T0['cat1'], TWIST, 0.2, True),
    (MUS + 'theme_panelka_15s.mp3', 14.6, TWIST + 0.2, DUR, 0.22, True),
    (S + 'amb_flat_winter.mp3', 7.8, T0['cat1'], DUR, 0.25, False),
]
VGAIN = {'valera': 1.5, 'cat': 1.55}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}')
