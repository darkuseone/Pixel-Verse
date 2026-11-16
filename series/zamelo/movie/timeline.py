"""«ЗАМЕЛО! СОБРАНИЕ ЖИЛЬЦОВ» — the season's sitcom movie (16:9). One timeline built from BEATS:
  ('L', key, shot)              a new line (voice/movie_t/<key>.mp3); the shot holds for the line + PAD
  ('F', 'epNN', a, b, shot)     a flashback: a piece of the season episode (picture + its own sound), projected from Тёма's phone
  ('P', seconds, shot)          a silent beat
Scenes ('S', name) switch the ambience / music bed. movie.py renders by shots, mix.py mixes VOICE / SFX / BEDS."""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = 'zamelo'
FPS = 30
LUFS = -14.0
VEP = 'movie_t'
SER = ROOT / 'series' / SLUG
X = 'series/zamelo/sfx/'
L = 'library/cc0/sfx/'
MU = 'library/cc0/music/'


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


def _cap(text):
    c = ' '.join(text.split(']')[-1].replace('́', '').split())
    words = c.split()
    best = max(range(len(words)), key=lambda i: (len(words[i].strip('.,!?…—«»')) >= 4, i))      # the punch word: the last long one
    words[best] = words[best].upper()
    return ' '.join(words)


LINES = json.load(open(SER / 'voice' / 'movie' / 'lines.json'))


def line(key):
    who, txt = LINES[key]
    return VEP, key, who, _cap(txt), _dur(SER / 'voice' / VEP / f'{key}.mp3')


BEATS = [
    ('S', 'landing'),
    # ХОЛОДНОЕ ОТКРЫТИЕ
    ('L', 'a01', 'gull_cu'), ('P', 1.3, 'notice'), ('L', 'a02', 'door_two'), ('L', 'a03', 'ira_door'), ('L', 'a04', 'zhora_cu'),
    ('L', 'a05', 'gosha_hatch'), ('L', 'a06', 'zhora_cam'),
    ('S', 'roof'),
    ('P', 3.2, 'title'),
    # ГЛАВА 1. ЯВКА
    ('L', 'b01', 'roof'),
    ('S', 'landing'),
    ('L', 'b02', 'nina_ladder'), ('L', 'b03', 'zhora_cu'), ('L', 'b04', 'nina_cu'),
    ('P', 1.4, 'tyoma_slide'), ('L', 'b05', 'tyoma_cu'), ('L', 'b06', 'ira_door'), ('L', 'b07', 'tyoma_cu'),
    ('L', 'b08', 'valya_cu'), ('L', 'b09', 'zhora_cu'), ('L', 'b10', 'valya_cu'), ('L', 'b11', 'gosha_jar'), ('L', 'b12', 'valya_two'),
    ('L', 'b13', 'zhora_cu'), ('L', 'b14', 'valya_cu'),
    ('P', 1.0, 'box_drop'), ('L', 'b15', 'vitek_hatch'), ('L', 'b16', 'zhora_cu'), ('L', 'b17', 'vitek_cu'), ('L', 'b18', 'nina_cu'),
    ('L', 'b19', 'vitek_cu'),
    ('P', 0.9, 'gull_bang'), ('L', 'b20', 'gull_cu'), ('L', 'b21', 'zhora_cu'), ('L', 'b22', 'gull_cu'),
    # ГЛАВА 2. ДЕБАТЫ
    ('L', 'c01', 'hall'), ('L', 'c02', 'zhora_speech'), ('L', 'c03', 'tyoma_phone'),
    ('F', 'ep01', 14.45, 22.6, 'fb'),
    ('L', 'c04', 'ira_door'), ('L', 'c05', 'zhora_cu'), ('L', 'c06', 'nina_cu'),
    ('L', 'c07', 'gull_cu'), ('L', 'c08', 'gosha_cu'), ('L', 'c09', 'duel'),
    ('F', 'ep03', 21.2, 30.85, 'fb'),
    ('L', 'c10', 'gosha_cu'), ('L', 'c11', 'valya_cu'), ('L', 'c12', 'zhora_cu'), ('L', 'c13', 'ira_door'),
    ('F', 'ep05', 22.4, 28.2, 'fb'),
    ('L', 'c14', 'vitek_cu'), ('L', 'c15', 'zhora_cu'), ('L', 'c16', 'vitek_cu'),
    ('L', 'c17', 'gosha_cu'), ('L', 'c18', 'zhora_cu'), ('L', 'c19', 'vitek_cu'),
    ('F', 'ep04', 33.65, 38.9, 'fb'),
    ('L', 'c20', 'nina_cu'), ('L', 'c21', 'duel_nina'), ('L', 'c22', 'nina_cu'),
    ('L', 'c23', 'gull_cu'), ('L', 'c24', 'valya_cu'), ('L', 'c25', 'zhora_cu'),
    ('F', 'ep02', 23.8, 31.6, 'fb'),
    ('L', 'c26', 'valya_cu'), ('L', 'c27', 'gosha_cu'), ('L', 'c28', 'valya_cu'),
    # ГЛАВА 3. ГОЛОСОВАНИЕ
    ('L', 'd01', 'gull_cu'), ('P', 1.3, 'vote_zhora'), ('L', 'd02', 'gull_cu'), ('L', 'd03', 'tyoma_cu'), ('L', 'd04', 'gull_cu'),
    ('P', 1.2, 'vote_gosha'), ('L', 'd05', 'zhora_cu'), ('L', 'd06', 'vitek_cu'), ('L', 'd07', 'gull_cu'), ('L', 'd08', 'valya_cu'),
    ('L', 'd09', 'gosha_win'),
    ('P', 1.0, 'ring'), ('L', 'd10', 'disp'), ('L', 'd11', 'zhora_cu'), ('L', 'd12', 'disp'),
    ('P', 1.6, 'twist'),
    ('L', 'd13', 'gosha_cu'), ('L', 'd14', 'nina_cu'), ('L', 'd15', 'vitek_cu'), ('L', 'd16', 'valya_cu'),
    ('P', 1.1, 'vote_all'), ('L', 'd17', 'gull_cu'), ('L', 'd18', 'zhora_cam'), ('L', 'd19', 'ira_door'),
    # ГЛАВА 4. ПЕРВЫЙ УКАЗ
    ('S', 'kitchen'),
    ('L', 'e01', 'kit_calc'), ('L', 'e02', 'kit_ira'), ('L', 'e03', 'kit_idea'),
    ('S', 'facade'),
    ('P', 1.4, 'sign_nail'), ('L', 'e04', 'win_decree'), ('L', 'e05', 'win_nina'), ('L', 'e06', 'win_zhora'),
    ('L', 'e07', 'win_valya'), ('L', 'e08', 'win_vitek'), ('L', 'e09', 'win_zhora'), ('L', 'e10', 'win_gosha'), ('L', 'e11', 'win_zhora'),
    ('L', 'e12', 'win_tyoma'),
    ('S', 'kitchen'),
    ('L', 'e13', 'kit_valenki'), ('L', 'e14', 'kit_post'),
    ('S', 'night'),
    ('L', 'e15', 'night_count'), ('P', 0.9, 'night_ring'), ('L', 'e16', 'disp'), ('L', 'e17', 'night_cu'), ('L', 'e18', 'disp'),
    ('P', 1.8, 'night_gong'), ('L', 'e19', 'night_gull'),
    ('S', 'morning'),
    ('P', 1.2, 'fox_sign'), ('L', 'e20', 'fox_cu'), ('L', 'e21', 'gosha_phone'), ('L', 'e22', 'fox_cu'),
    ('P', 2.0, 'pull_back'), ('L', 'e23', 'end_gull'), ('P', 3.4, 'end'),
]

PAD = 0.34
SHOTS, VOICE, SFX, CLIPS = [], [], [], []
SCENE_SPANS = []
t = 0.0
scene = None
for b in BEATS:
    k = b[0]
    if k == 'S':
        scene = b[1]; SCENE_SPANS.append([scene, t, None]); continue
    if k == 'L':
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
        SHOTS.append(dict(name=b[2], t0=t, t1=t + b[1], kind='pause', scene=scene))
        dur = b[1]
    t += dur
DUR = round(t, 3)
for i, sp in enumerate(SCENE_SPANS): sp[2] = SCENE_SPANS[i + 1][1] if i + 1 < len(SCENE_SPANS) else DUR
CUTS = [s['t0'] for s in SHOTS] + [DUR]
NAMES = [f"{i:03d}_{s['name']}" for i, s in enumerate(SHOTS)]


def first(name, nth=0):
    return [s for s in SHOTS if s['name'] == name][nth]


def all_(name):
    return [s for s in SHOTS if s['name'] == name]


def shot_at(tt):
    for s in SHOTS:
        if s['t0'] <= tt < s['t1']: return s
    return SHOTS[-1]


def line_t(key):
    return next(v[3] for v in VOICE if v[2] == key)


def line_t1(key):
    return next(v[3] + v[5] for v in VOICE if v[2] == key)


TWIST = first('twist')['t0']
CHAPTERS = [(0.0, 'Собрание'), (first('roof')['t0'], 'Явка'), (first('hall')['t0'], 'Дебаты'), (line_t('d01') - 0.06, 'Голосование'),
            (first('kit_calc')['t0'], 'Первый указ')]

# flashback sound: the episode's own mix, cut out of its final.mp4 (build/zamelo-movie/fb_<ep>.wav, see mix.py)
for c in CLIPS:
    SFX.append((f'build/{SLUG}-movie/fb_{c["ep"]}.wav', c['t0'], 1.2, c['a'], c['b']))


def _at(name, dt, path, g, nth=None):
    for i, s in enumerate(all_(name)):
        if nth is not None and i != nth: continue
        SFX.append((path, s['t0'] + dt, g))


def _ln(key, dt, path, g):
    SFX.append((path, line_t(key) + dt, g))


# ---------------------------------------------------------------- point SFX (dense: every action has a sound)
_at('gull_cu', 0.0, X + 'seagull_cry.mp3', 0.35, nth=0)
_at('notice', 0.0, L + 'whoosh_3.mp3', 0.4)
_at('door_two', 0.0, L + 'door_apartment_open.mp3', 0.6)
_ln('a03', 0.0, L + 'cloth_rustle.mp3', 0.3)
_at('gosha_hatch', 0.0, L + 'sliding_door_open.mp3', 0.5)
_at('gosha_hatch', 0.2, L + 'wind_whistle.mp3', 0.3)
_at('zhora_cam', 0.0, L + 'vinyl_scratch.mp3', 0.35, nth=0)
_at('title', 0.0, L + 'boing_cartoon.mp3', 0.45)
_at('title', 0.05, X + 'snow_dive.mp3', 0.6)
_at('roof', 0.0, L + 'snow_steps.mp3', 0.7)
_at('roof', 2.0, L + 'snow_steps.mp3', 0.6)
_at('nina_ladder', 0.0, L + 'chair_creak.mp3', 0.6)
_at('nina_ladder', 1.2, L + 'chair_creak.mp3', 0.5)
_at('nina_ladder', 2.6, L + 'steps_concrete.mp3', 0.5)
_at('tyoma_slide', 0.0, L + 'whoosh_1.mp3', 0.7)
_at('tyoma_slide', 0.75, L + 'chair_creak.mp3', 0.6)
_at('tyoma_slide', 0.8, L + 'boing_cartoon.mp3', 0.45)
_at('tyoma_slide', 0.85, X + 'snow_plop.mp3', 0.5)
_at('gosha_jar', 0.3, L + 'bottle_clink.mp3', 0.6)
_at('valya_two', 0.2, L + 'zipper.mp3', 0.4)
_ln('b13', 0.0, L + 'vinyl_scratch.mp3', 0.3)
_at('box_drop', 0.3, L + 'canvas_bag_drop.mp3', 0.8)
_at('box_drop', 0.0, L + 'whoosh_3.mp3', 0.4)
_at('vitek_hatch', 0.0, L + 'steps_concrete.mp3', 0.5)
_at('gull_bang', 0.1, L + 'anvil_clank.mp3', 0.35)
_at('gull_bang', 0.45, L + 'anvil_clank.mp3', 0.35)
_ln('b22', 2.0, L + 'anvil_clank.mp3', 0.3)
_ln('b22', 2.3, L + 'rimshot_joke.mp3', 0.4)
_at('hall', 0.0, L + 'anvil_clank.mp3', 0.3)
_at('tyoma_phone', 0.6, L + 'phone_key_click.mp3', 0.6)
for s in all_('fb'):
    SFX.append((L + 'whoosh_3.mp3', s['t0'], 0.5)); SFX.append((L + 'whoosh_1.mp3', s['t1'] - 0.2, 0.4))
_ln('c06', 2.0, L + 'rimshot_joke.mp3', 0.35)
_ln('c10', 0.0, L + 'bottle_clink.mp3', 0.4)
_ln('c11', 0.3, L + 'cloth_rustle.mp3', 0.3)
_ln('c16', 0.0, L + 'boing_cartoon.mp3', 0.3)
_ln('c22', 1.6, L + 'rimshot_joke.mp3', 0.35)
_ln('c26', 0.0, L + 'gong_strong.mp3', 0.12)
_ln('c27', 0.0, L + 'bottle_clink.mp3', 0.45)
_ln('d01', 0.0, L + 'anvil_clank.mp3', 0.3)
_at('vote_zhora', 0.1, L + 'cloth_rustle.mp3', 0.5)
_at('vote_gosha', 0.1, L + 'cloth_rustle.mp3', 0.5)
_ln('d05', 0.0, L + 'vinyl_scratch.mp3', 0.3)
_at('ring', 0.0, L + 'intercom_ring.mp3', 0.6)
_at('twist', 0.0, L + 'gong_strong.mp3', 0.45)
_at('twist', 0.05, L + 'vinyl_scratch.mp3', 0.4)
_at('twist', 0.9, L + 'bottle_clink.mp3', 0.4)
_at('vote_all', 0.05, L + 'cloth_rustle.mp3', 0.6)
_ln('d17', 0.0, L + 'anvil_clank.mp3', 0.35)
_ln('d19', 2.8, L + 'rimshot_joke.mp3', 0.35)
_at('kit_calc', 0.2, L + 'phone_key_click.mp3', 0.5)
_at('kit_calc', 1.2, L + 'phone_key_click.mp3', 0.45)
_at('kit_ira', 0.0, L + 'fridge_door.mp3', 0.35)
_at('kit_idea', 1.0, L + 'boing_cartoon.mp3', 0.4)
_at('sign_nail', 0.2, L + 'anvil_clank.mp3', 0.35)
_at('sign_nail', 0.65, L + 'anvil_clank.mp3', 0.35)
_at('sign_nail', 1.05, L + 'anvil_clank.mp3', 0.35)
for nm in ('win_nina', 'win_valya', 'win_vitek', 'win_gosha'):
    _at(nm, 0.0, L + 'snow_steps.mp3', 0.5); _at(nm, 0.5, L + 'cloth_rustle.mp3', 0.4)
for nm in ('win_zhora',):
    _at(nm, 0.2, L + 'keys_on_table.mp3', 0.45)
_at('win_tyoma', 0.0, L + 'whoosh_1.mp3', 0.4)
_at('kit_valenki', 0.0, L + 'slipper_steps.mp3', 0.6)
_at('kit_valenki', 0.0, L + 'snow_steps.mp3', 0.4)
_at('night_count', 0.0, L + 'keys_on_table.mp3', 0.4)
_at('night_count', 1.0, L + 'cloth_rustle.mp3', 0.3)
_at('night_ring', 0.0, L + 'intercom_ring.mp3', 0.6)
_at('night_gong', 0.0, L + 'gong_strong.mp3', 0.4)
_at('night_gong', 1.0, X + 'snow_plop.mp3', 0.7)
_at('fox_sign', 0.0, L + 'whoosh_3.mp3', 0.4)
_at('fox_sign', 0.3, L + 'anvil_clank.mp3', 0.3)
_ln('e20', 0.0, L + 'intercom_ring.mp3', 0.0)
_at('pull_back', 0.0, L + 'whoosh_1.mp3', 0.4)
_ln('e23', 1.2, L + 'anvil_clank.mp3', 0.35)
_at('end', 0.1, L + 'rimshot_joke.mp3', 0.45)
SFX = [s for s in SFX if s[2] > 0]

V_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9'
BED_OF = dict(landing=[(MU + 'komiku_weekly_fair.mp3', 30.0, 0.70, V_DIP), (X + 'frost_wind_loop.mp3', 8.0, 0.18, '')],
              roof=[(MU + 'komiku_weekly_fair.mp3', 30.0, 0.80, V_DIP), (X + 'frost_wind_loop.mp3', 8.0, 0.45, '')],
              kitchen=[(MU + 'komiku_mandolin.mp3', 30.0, 0.75, V_DIP)],
              facade=[(MU + 'komiku_fetch_contest.mp3', 30.0, 0.75, V_DIP), (X + 'frost_wind_loop.mp3', 8.0, 0.30, '')],
              night=[(MU + 'komiku_shoe_shop.mp3', 30.0, 0.55, V_DIP), (X + 'frost_wind_loop.mp3', 8.0, 0.25, '')],
              morning=[(MU + 'town_cheerful.mp3', 30.0, 0.80, V_DIP), (X + 'frost_wind_loop.mp3', 8.0, 0.30, '')])
BEDS = []
for name, a, b in SCENE_SPANS:
    for path, loop, g, eq in BED_OF[name]:
        BEDS.append((path, loop, round(a, 2), round(b, 2), g, True, eq))

VFX = {'disp': 'highpass=f=300,lowpass=f=3400'}
VGAIN = {'zhora': 2.0, 'chayka': 2.2, 'vitek': 2.0, 'ira': 2.0, 'disp': 2.0, 'nina': 2.0, 'tyoma': 2.0, 'valya': 2.0, 'gosha': 2.0}
