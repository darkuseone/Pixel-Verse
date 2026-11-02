"""«ТЁЩА НА НЕДЕЛЬКУ: ЗАГОВОР» — mini-movie (16:9). One timeline built from BEATS:
  ('L', key, shot)              a new line (voice/movie_t/<key>.mp3); the shot holds for the line + PAD
  ('R', 'epNN_t:key', shot)     a season line reused from that episode (same voices, 0 credits)
  ('F', 'epNN', a, b, shot)     a flashback: a piece of the season episode (picture + its own sound) in a «memory» frame
  ('P', seconds, shot)          a silent beat
Scenes ('S', name) switch the music bed. movie.py renders by shots, mix.py mixes VOICE / SFX / BEDS."""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = 'teshcha'
FPS = 30
LUFS = -14.0
VEP = 'movie_t'
C = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
S = f'series/{SLUG}/sfx/'
SER = ROOT / 'series' / SLUG
VFX = {}


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


def _cap(text):
    c = ' '.join(text.split(']')[-1].replace('́', '').replace('[pause]', '').split())
    words = c.split()
    best = max(range(len(words)), key=lambda i: (len(words[i].strip('.,!?…—«»')) >= 4, i))      # the punch word: the last long one
    words[best] = words[best].upper()
    return ' '.join(words)


LINES = json.load(open(SER / 'voice' / 'movie' / 'lines.json'))
OLD = {}
for ep in ('ep03', 'ep04', 'ep06'):
    for k, v in json.load(open(SER / 'voice' / ep / 'lines.json')).items(): OLD[f'{ep}_t:{k}'] = v


def line(key):
    """(vep, file key, speaker, caption, clip seconds)"""
    if ':' in key:
        vep, k = key.split(':'); who, txt = OLD[key]
    else:
        vep, k = VEP, key; who, txt = LINES[key]
    return vep, k, who, _cap(txt), _dur(SER / 'voice' / vep / f'{k}.mp3')


BEATS = [
    # 0. ХОЛОДНОЕ ОТКРЫТИЕ: ночь, шкаф, фонарик
    ('S', 'night'),
    ('L', 'o1', 'hook'), ('P', 3.0, 'evidence'), ('L', 'o2', 'closet'), ('L', 'o3', 'pusya_closet'), ('P', 3.2, 'title'),
    # 1. 07:00 кухня: «Вторник, Толечка»
    ('S', 'kitchen'),
    ('P', 1.7, 'card_0700'), ('P', 2.2, 'kitchen_wide'), ('L', 'k1', 'raisa_kasha'), ('L', 'k2', 'tolik_shirt'),
    ('L', 'k3', 'raisa_kasha2'), ('P', 2.0, 'sveta_wink'), ('L', 'k4', 'tolik_sulk'), ('L', 'k5', 'pusya_k'),
    # 2. 08:30 прихожая: «Балкон замуруем»
    ('S', 'hall'),
    ('P', 1.7, 'card_0830'), ('P', 2.2, 'hall_sneak'), ('L', 'h1', 'raisa_phone'), ('P', 1.2, 'zamuruem'), ('L', 'h2', 'raisa_phone2'),
    ('P', 1.4, 'suitcase_cu'), ('L', 'h3', 'tolik_coats'),
    ('F', 'ep01', 0.15, 5.4, 'fb_ep01'), ('F', 'ep02', 4.25, 9.5, 'fb_ep02'), ('F', 'ep03', 3.35, 9.3, 'fb_ep03'),
    ('L', 'h4', 'tolik_coats2'), ('L', 'h5', 'pusya_h'),
    # 3. 10:00 побег: бабки, маршрутка
    ('S', 'yard'),
    ('P', 1.7, 'card_1000'), ('L', 'e1', 'tolik_rod'), ('P', 2.0, 'sneak_yard'), ('L', 'e2', 'granny1'), ('L', 'e3', 'granny2'),
    ('P', 1.3, 'tolik_run'), ('P', 1.4, 'bus_arrive'), ('L', 'e4', 'lyusya'), ('L', 'e5', 'tolik_betray'), ('L', 'e6', 'lyusya2'),
    ('R', 'ep04_t:b1', 'babki'), ('P', 2.0, 'bus_ride'), ('L', 'e7', 'tolik_hat'),
    # 4. 12:00 разведка у балконной двери
    ('S', 'spy'),
    ('P', 1.7, 'card_1200'), ('P', 3.2, 'spy_glass'), ('L', 's1', 'tolik_spy'), ('P', 1.6, 'colander'), ('L', 's2', 'pusya_col'),
    ('L', 's3', 'tolik_farewell'), ('L', 's4', 'pusya_s4'),
    # 5. 13:00 штурм — ПОВОРОТ 1: кабинет мужика
    ('S', 'storm'),
    ('P', 1.7, 'card_1300'), ('L', 'm1', 'storm'), ('P', 4.0, 'reveal'), ('L', 'm2', 'raisa_gift'), ('L', 'm3', 'sveta_surp'),
    ('L', 'm4', 'tolik_stun'), ('L', 'm5', 'lyusya_cement'), ('L', 'm6', 'pusya_awk'),
    # 6. 15:00 «как мужик»
    ('S', 'cabinet'),
    ('P', 1.7, 'card_1500'), ('L', 'f1', 'tolik_drill'), ('P', 2.4, 'sparks'), ('L', 'f2', 'dark'),
    ('F', 'ep05', 26.15, 30.85, 'fb_ep05'), ('L', 'f3', 'tolik_touched'),
    # 7. 19:00 праздник и тост — ПОВОРОТ 2
    ('S', 'party'),
    ('P', 1.7, 'card_1900'), ('P', 3.0, 'party_wide'), ('P', 2.0, 'cake'), ('R', 'ep03_t:r1', 'raisa_plate'), ('L', 'g1', 'karaoke'),
    ('L', 'p1', 'toast'), ('L', 'p2', 'toast2'), ('P', 1.4, 'freeze'),
    ('S', 'twist2'),
    ('L', 'p3', 'raisa_leaving'), ('P', 1.6, 'suitcase_reveal'), ('L', 'p4', 'sveta_said'), ('L', 'p5', 'raisa_stay'),
    ('L', 'p6', 'lyusya_too'), ('L', 'p7', 'tolik_weak'),
    # 8. 21:00 кнопка
    ('S', 'night_cab'),
    ('P', 1.7, 'card_2100'), ('P', 2.2, 'cab_pan'), ('L', 'b1', 'cab_alone'), ('R', 'ep04_t:r1', 'door_raisa'), ('R', 'ep06_t:p1', 'pusya_chair'),
    ('P', 3.6, 'end'),
]

PAD = 0.45
SHOTS, VOICE, SFX, CLIPS = [], [], [], []
SCENE_SPANS = []
t = 0.0
scene = None
for b in BEATS:
    k = b[0]
    if k == 'S':
        scene = b[1]; SCENE_SPANS.append([scene, t, None]); continue
    if k in ('L', 'R'):
        vep, key, who, cap, clip = line(b[1])
        dur = clip + PAD
        VOICE.append((f'{key}@{len(VOICE)}', vep, key, round(t + 0.06, 3), 0.0, clip, who, cap))
        SHOTS.append(dict(name=b[2], t0=t, t1=t + dur, kind='line', key=b[1], who=who, scene=scene))
    elif k == 'F':
        ep, a, bb, name = b[1], b[2], b[3], b[4]
        dur = bb - a + 0.5
        CLIPS.append(dict(ep=ep, a=a, b=bb, t0=t + 0.25))
        SHOTS.append(dict(name=name, t0=t, t1=t + dur, kind='flash', ep=ep, a=a, b=bb, scene=scene))
    else:
        dur = b[1]
        SHOTS.append(dict(name=b[2], t0=t, t1=t + dur, kind='pause', scene=scene))
    t += dur
DUR = round(t, 3)
for i, sp in enumerate(SCENE_SPANS): sp[2] = SCENE_SPANS[i + 1][1] if i + 1 < len(SCENE_SPANS) else DUR
CUTS = [s['t0'] for s in SHOTS] + [DUR]
NAMES = [f"{i:02d}_{s['name']}" for i, s in enumerate(SHOTS)]
T0 = {}
for s in SHOTS: T0.setdefault(s['name'], s['t0'])


def first(name, nth=0):
    return [s for s in SHOTS if s['name'] == name][nth]


def all_(name):
    return [s for s in SHOTS if s['name'] == name]


def shot_at(tt):
    for s in SHOTS:
        if s['t0'] <= tt < s['t1']: return s
    return SHOTS[-1]


TWIST = T0['reveal']
TWIST2 = T0['raisa_leaving']
CHAPTERS = [(0.0, 'Заговор'), (T0['card_0700'], '07:00 Вторник, Толечка'), (T0['card_0830'], '08:30 «Балкон замуруем»'),
            (T0['card_1000'], '10:00 Побег'), (T0['card_1200'], '17:00 Разведка'), (T0['card_1300'], '17:30 Штурм'),
            (T0['card_1500'], '18:30 Как мужик'), (T0['card_1900'], '20:00 Праздник'), (T0['raisa_leaving'], 'Тост'),
            (T0['card_2100'], '23:00 Кабинет')]

for c in CLIPS:                                                  # flashback sound = the episode's own mix (mix.py extracts it)
    SFX.append((f'build/{SLUG}-movie/fb_{c["ep"]}.wav', c['t0'], 1.2, c['a'], c['b']))


def _at(name, dt, path, g, a=None, b=None):
    for s in all_(name):
        SFX.append((path, s['t0'] + dt, g) + ((a, b) if a is not None else ()))


# ---------------------------------------------------------------- point SFX (CC0 library + the series' own)
_at('hook', 0.0, C + 'cloth_rustle.mp3', 0.5)
_at('evidence', 0.0, C + 'whoosh_1.mp3', 0.4); _at('evidence', 0.7, C + 'canvas_bag_drop.mp3', 0.5); _at('evidence', 1.4, C + 'suitcase.mp3', 0.5)
_at('title', 0.05, C + 'gong_strong.mp3', 0.25)
for nm in ('card_0700', 'card_0830', 'card_1000', 'card_1200', 'card_1300', 'card_1500', 'card_1900', 'card_2100'):
    _at(nm, 0.0, C + 'whoosh_3.mp3', 0.45); _at(nm, 0.25, C + 'phone_key_click.mp3', 0.6)
_at('kitchen_wide', 0.2, C + 'bottle_clink.mp3', 0.4)
_at('sveta_wink', 0.4, C + 'boing_cartoon.mp3', 0.25)
_at('pusya_k', 0.1, C + 'rimshot_joke.mp3', 0.35)
_at('hall_sneak', 0.0, C + 'slipper_steps.mp3', 0.5, 0.0, 1.6)
_at('zamuruem', 0.0, C + 'vinyl_scratch.mp3', 0.4); _at('zamuruem', 0.05, S + 'twist_hit.mp3', 0.4)
_at('suitcase_cu', 0.1, C + 'suitcase.mp3', 0.5)
for nm in ('fb_ep01', 'fb_ep02', 'fb_ep03', 'fb_ep05'):
    _at(nm, 0.0, C + 'whoosh_3.mp3', 0.4)
_at('tolik_rod', 0.2, C + 'door_apartment_open.mp3', 0.5)
_at('sneak_yard', 0.0, C + 'snow_steps.mp3', 0.6, 0.0, 2.0)
_at('tolik_run', 0.0, C + 'snow_steps.mp3', 0.7, 1.0, 2.3)
_at('bus_arrive', -0.8, C + 'car_arrive_stop.mp3', 0.8, 4.0, 9.0); _at('bus_arrive', 0.1, C + 'bus_horn.mp3', 0.5)
_at('lyusya', 0.0, C + 'sliding_door_open.mp3', 0.7)
_at('babki', 0.0, C + 'gong_strong.mp3', 0.15)
_at('spy_glass', 0.6, C + 'jackhammer.mp3', 0.25, 0.0, 1.2)
_at('colander', 0.2, C + 'bottle_clink.mp3', 0.5); _at('colander', 0.6, C + 'boing_cartoon.mp3', 0.3)
_at('storm', 0.0, C + 'door_apartment_open.mp3', 0.8)
_at('reveal', 0.0, S + 'twist_hit.mp3', 0.6); _at('reveal', 0.05, C + 'vinyl_scratch.mp3', 0.4)
_at('reveal', 1.3, C + 'anvil_clank.mp3', 0.25)
_at('tolik_stun', 0.3, C + 'bottle_clink.mp3', 0.5)
_at('pusya_awk', 0.1, C + 'rimshot_joke.mp3', 0.3)
_at('tolik_drill', 1.2, C + 'jackhammer.mp3', 0.4, 0.0, 1.0)
_at('sparks', 0.0, C + 'jackhammer.mp3', 0.5, 0.0, 0.8); _at('sparks', 0.9, C + 'anvil_clank.mp3', 0.4)
_at('party_wide', 0.0, C + 'bottle_clink.mp3', 0.5); _at('party_wide', 0.6, C + 'bottle_clink.mp3', 0.4)
_at('freeze', 0.0, C + 'vinyl_scratch.mp3', 0.45)
_at('suitcase_reveal', 0.0, S + 'twist_hit.mp3', 0.5); _at('suitcase_reveal', 0.1, C + 'suitcase.mp3', 0.5)
_at('lyusya_too', 0.0, C + 'suitcase.mp3', 0.5)
_at('door_raisa', 0.0, C + 'door_apartment_open.mp3', 0.6)
_at('pusya_chair', 0.0, C + 'chair_creak.mp3', 0.5)
_at('end', 0.1, C + 'rimshot_joke.mp3', 0.55)

VOICE_DIP = 'equalizer=f=1500:t=q:w=0.7:g=-7,equalizer=f=3200:t=q:w=1:g=-4'
_BED = dict(night=('komiku_shoe_shop', 0.7), kitchen=('komiku_weekly_fair', 0.75), hall=('komiku_fetch_contest', 0.75),
            yard=('komiku_fetch_contest', 0.75), spy=('komiku_shoe_shop', 0.75), storm=None, cabinet=('komiku_mandolin', 0.75),
            party=('komiku_weekly_fair', 0.8), twist2=('komiku_mandolin', 0.75), night_cab=('komiku_shoe_shop', 0.75))
BEDS = []
for name, a, b in SCENE_SPANS:
    bed = _BED.get(name)
    if bed: BEDS.append((CM + bed[0] + '.mp3', 59.5, a, b, bed[1], True, VOICE_DIP))
BEDS.append((CM + 'komiku_mandolin.mp3', 59.5, T0['raisa_gift'], T0['card_1500'], 0.7, True, VOICE_DIP))
BEDS.append((C + 'wind_whistle.mp3', 12.0, T0['card_1000'], T0['card_1200'], 0.35, False))
VGAIN = {'tolik': 1.85, 'raisa': 2.2, 'pusya': 2.3, 'sveta': 2.0, 'lyusya': 2.3, 'babki': 2.2, 'granny': 2.2, 'granny2': 2.2}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:2d} {s['t0']:6.2f} {s['t1'] - s['t0']:5.2f} {s['name']} {s.get('key', '')}")
    print('DUR', DUR, 'twist', round(TWIST, 1), f'{TWIST / DUR:.0%}', 'twist2', round(TWIST2, 1), f'{TWIST2 / DUR:.0%}')
