"""«Мазутыч: СЛЕДСТВИЕ ПО БЕНЗИНУ» — detective mini-movie (16:9). One timeline built from BEATS:
  ('L', key, shot)              a new line (voice/movie_t/<key>.mp3); the shot holds for the line + PAD
  ('R', 'epNN_t:key', shot)     a season line reused from that episode (same voices, 0 credits)
  ('F', 'epNN', a, b, shot)     a flashback: a piece of the season episode (picture + its own sound) in the «case file» frame
  ('P', seconds, shot)          a silent beat
Scenes ('S', name) switch the ambience / music bed. movie.py renders by shots, mix.py mixes VOICE / SFX / BEDS."""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = 'mazutych'
FPS = 30
MASTER = 0.9
VEP = 'movie_t'
S = 'library/sfx/'
MUS = f'series/{SLUG}/music/'
SER = ROOT / 'series' / SLUG


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


def _cap(text):
    c = ' '.join(text.split(']')[-1].replace('[pause]', '').split())
    words = c.split()
    best = max(range(len(words)), key=lambda i: (len(words[i].strip('.,!?…—«»')) >= 4, i))      # the punch word: the last long one
    words[best] = words[best].upper()
    return ' '.join(words)


LINES = json.load(open(SER / 'voice' / 'movie' / 'lines.json'))
OLD = {}
for ep in ('ep01', 'ep02', 'ep03', 'ep04', 'ep06'):
    for k, v in json.load(open(SER / 'episodes' / ep / 'lines.json')).items(): OLD[f'{ep}_t:{k}'] = v


def line(key):
    """(vep, file key, speaker, caption, clip seconds)"""
    if ':' in key:
        vep, k = key.split(':'); who, txt = OLD[key]
    else:
        vep, k = VEP, key; who, txt = LINES[key]
    return vep, k, who, _cap(txt), _dur(SER / 'voice' / vep / f'{k}.mp3')


BEATS = [
    ('S', 'azs'),
    # 1. ХУК: ночь, пустая колонка, последняя капля
    ('L', 'ma01', 'hook'), ('L', 'wa01', 'drop_cu'), ('L', 'ma02', 'maz_pump'), ('P', 1.1, 'drop_fall'),
    ('L', 'ma03', 'maz_noir'), ('P', 3.2, 'title'),
    # 2. завод: план 147 %, а бензина нет
    ('S', 'gate'),
    ('P', 2.0, 'gate_wide'), ('L', 'ma04', 'banner_cu'), ('L', 'ma05', 'maz_gate'), ('L', 'bb01', 'loudspeaker'),
    # 3. гараж: доска улик со шлангом вместо красной нитки
    ('S', 'garage'),
    ('P', 2.4, 'board_wide'), ('L', 'ma07', 'board_cu'), ('L', 'wa03', 'wheel_board'), ('L', 'ma08', 'maz_board'),
    # 4. подозреваемая №1: Зоя
    ('S', 'kiosk'),
    ('P', 1.25, 'card_zoya'), ('L', 'ma09', 'zoya_two'), ('L', 'zo01', 'zoya_cu'), ('L', 'ma10', 'maz_badge'),
    ('R', 'ep01_t:z2', 'zoya_ballet'), ('L', 'ma12', 'maz_noir_kiosk'), ('F', 'ep02', 9.0, 14.45, 'fb_zoya'),
    ('L', 'zo03', 'zoya_lean'), ('L', 'zo04', 'zoya_cu'),
    # 5. подозреваемый №2: Вадик
    ('S', 'garages'),
    ('P', 1.25, 'card_vadik'), ('R', 'ep03_t:v1', 'vadik_cu'), ('L', 'ma13', 'maz_garages'),
    ('R', 'ep03_t:v6', 'vadik_cu2'), ('L', 'ma14', 'maz_noir_gar'), ('F', 'ep03', 15.75, 21.15, 'fb_boss'),
    # 6. подозреваемый №3: инспектор
    ('S', 'highway'),
    ('P', 1.25, 'card_cop'), ('R', 'ep04_t:c1', 'cop_stop'), ('L', 'ma15', 'maz_cop'), ('R', 'ep04_t:c3', 'cop_cu'),
    ('L', 'ma17', 'maz_noir_hw'), ('F', 'ep04', 17.4, 22.1, 'fb_cop'),
    ('R', 'ep06_t:w1', 'tow_cop'), ('R', 'ep04_t:c8', 'tow_cop2'),
    # 7. подозреваемый №4: Борис Борисыч
    ('S', 'office'),
    ('P', 1.25, 'card_boss'), ('L', 'ma18', 'office_two'), ('L', 'bb02', 'boss_cu'), ('L', 'ma19', 'maz_office'),
    ('L', 'bb03', 'boss_cu2'), ('L', 'bb04', 'boss_talon'), ('R', 'ep02_t:w0', 'wheel_office'),
    # 8. подозреваемый №5: Толик — слежка
    ('S', 'night'),
    ('P', 1.25, 'card_tolik'), ('P', 1.8, 'stakeout'), ('L', 'wa09', 'stake_cu'),
    ('P', 1.4, 'truck_pass'), ('L', 'tl01', 'tolik_sing'),
    ('S', 'chase'),
    ('P', 2.4, 'chase'), ('L', 'wa10', 'chase_cu'), ('P', 1.6, 'gate_night'),
    # 9. ПОВОРОТ: резервуар «ПЛАН», задвижка — его
    ('S', 'tank'),
    ('P', 2.2, 'tank_wide'), ('L', 'ma21', 'maz_tank'), ('L', 'tl02', 'tolik_tank'), ('L', 'tl03', 'tolik_tank2'),
    ('P', 1.4, 'tank_flip'), ('L', 'ma22', 'maz_tank2'), ('P', 1.7, 'valve_tilt'), ('L', 'ma23', 'valve_plate'),
    ('L', 'ma24', 'maz_shock'), ('L', 'wa11', 'wheel_tank'), ('L', 'tl04', 'tolik_tank3'), ('L', 'ma25', 'maz_valve'),
    # 10. дилемма
    ('P', 1.2, 'boss_run'), ('L', 'bb05', 'boss_run2'), ('L', 'bb06', 'boss_beg'), ('L', 'ma26', 'maz_valve_cu'),
    ('L', 'bb07', 'boss_beg2'), ('L', 'ma27', 'maz_hero'),
    ('S', 'hero'),
    ('P', 3.0, 'valve_turn'),
    # 11. утро: раздача
    ('S', 'crowd'),
    ('P', 2.4, 'crowd_gate'), ('R', 'ep01_t:d1', 'tolik_crowd'), ('L', 'zo05', 'zoya_mega'), ('P', 2.0, 'banner_fall'),
    ('L', 'bb08', 'boss_cry'), ('L', 'ma28', 'maz_smile'), ('R', 'ep04_t:c8', 'cop_drive'), ('R', 'ep01_t:z2', 'zoya_dance'),
    # 12. кнопка и петля
    ('S', 'end'),
    ('P', 1.4, 'maz_canister'), ('L', 'ma29', 'maz_vesta'), ('P', 1.3, 'hatch'), ('R', 'ep06_t:z2', 'zoya_pass'),
    ('L', 'wa12', 'wheel_end'), ('L', 'bb09', 'loud_end'),
    ('S', 'azs'),
    ('P', 1.3, 'sign_back'), ('R', 'ep01_t:m25', 'loop_pump'),
    ('S', 'credits'),
    ('P', 7.0, 'credits'), ('P', 3.6, 's2_card'),
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
        SHOTS.append(dict(name=b[2], t0=t, t1=t + b[1], kind='pause', scene=scene))
        dur = b[1]
    t += dur
DUR = round(t, 3)
for i, sp in enumerate(SCENE_SPANS): sp[2] = SCENE_SPANS[i + 1][1] if i + 1 < len(SCENE_SPANS) else DUR
CUTS = [s['t0'] for s in SHOTS] + [DUR]
NAMES = [f"{i:02d}_{s['name']}" for i, s in enumerate(SHOTS)]


def first(name, nth=0):
    return [s for s in SHOTS if s['name'] == name][nth]


def all_(name):
    return [s for s in SHOTS if s['name'] == name]


def shot_at(tt):
    for s in SHOTS:
        if s['t0'] <= tt < s['t1']: return s
    return SHOTS[-1]


def line_t(key):
    return next(v[3] for v in VOICE if v[2] == key.split(':')[-1])


TWIST = first('tank_wide')['t0']
CHAPTERS = [(0.0, 'Последняя капля'), (first('gate_wide')['t0'], 'План 147 %'), (first('board_wide')['t0'], 'Доска улик'),
            (first('card_zoya')['t0'], 'Подозреваемая №1: Зоя'), (first('card_vadik')['t0'], 'Подозреваемый №2: Вадик'),
            (first('card_cop')['t0'], 'Подозреваемый №3: инспектор'), (first('card_boss')['t0'], 'Подозреваемый №4: начальник'),
            (first('card_tolik')['t0'], 'Подозреваемый №5: Толик'), (first('tank_wide')['t0'], 'Резервуар «ПЛАН»'),
            (first('boss_run')['t0'], 'Задвижка'), (first('crowd_gate')['t0'], 'Бензин есть!'), (first('maz_canister')['t0'], 'Ласточка'),
            (first('credits')['t0'], 'Титры')]

# flashback sound: the episode's own mix, cut out of its final.mp4 (build/mazutych-movie/fb_<ep>.wav, see mix.py)
for c in CLIPS:
    SFX.append((f'build/{SLUG}-movie/fb_{c["ep"]}.wav', c['t0'], 1.4, c['a'], c['b']))


def _at(name, dt, path, g, nth=None, a=None, b=None):
    for i, s in enumerate(all_(name)):
        if nth is not None and i != nth: continue
        SFX.append((S + path, s['t0'] + dt, g) + ((a, b) if a is not None else ()))


# ---------------------------------------------------------------- point SFX (library of the season + generic library)
_at('hook', 0.0, 'record_scratch.mp3', 0.25)
_at('hook', 0.15, 'water_drip_single.mp3', 0.0)
_at('drop_cu', 0.6, 'water_drip_single.mp3', 0.7)
_at('drop_fall', 0.55, 'water_drip_single.mp3', 0.9)
_at('drop_fall', 0.6, 'tank_knock_hollow.mp3', 0.25)
_at('maz_noir', 0.0, 'sax_sting_swell.mp3', 0.25)
_at('title', 0.05, 'title_stinger.mp3', 0.6)
_at('gate_wide', 0.0, 'monowheel_whine.mp3', 0.45)
_at('gate_wide', 0.2, 'gate_rolling.mp3', 0.3)
_at('loudspeaker', 0.0, 'pa_chime_feedback.mp3', 0.45)
_at('board_wide', 0.3, 'pushpin_pop.mp3', 0.6); _at('board_wide', 0.9, 'pushpin_pop.mp3', 0.55); _at('board_wide', 1.5, 'pushpin_pop.mp3', 0.6)
_at('board_cu', 0.2, 'rope_yank.mp3', 0.35)
_at('maz_board', 0.0, 'camera_flash.mp3', 0.0)
for nm in ('card_zoya', 'card_vadik', 'card_cop', 'card_boss', 'card_tolik'):
    _at(nm, 0.0, 'camera_flash.mp3', 0.55); _at(nm, 0.45, 'stamp.mp3', 0.75); _at(nm, 0.05, 'blues_bass_sting.mp3', 0.35)
for nm in ('fb_zoya', 'fb_boss', 'fb_cop', 'fb_tolik'):
    _at(nm, 0.0, 'vhs_rewind.mp3', 0.35); _at(nm, 0.0, 'film_click.mp3', 0.5)
_at('zoya_cu', 0.2, 'gum_pop.mp3', 0.4, nth=0)
_at('maz_badge', 0.0, 'fist_slam_counter.mp3', 0.45, nth=0)
_at('zoya_ballet', 0.1, 'gum_pop.mp3', 0.45)
_at('garages_wide', 0.0, 'old_sedan_rattle.mp3', 0.3)
_at('vadik_cu', 0.0, 'glass_slide.mp3', 0.35)
_at('cop_stop', 0.0, 'police_whistle.mp3', 0.5)
_at('cop_stop', 0.15, 'brake_skid.mp3', 0.35)
_at('tow_cop', 0.0, 'rope_strain_creak.mp3', 0.5); _at('tow_cop', 0.2, 'monowheel_whine.mp3', 0.4)
_at('office_wide', 0.0, 'clock_fast_ticks.mp3', 0.25)
_at('boss_cu', 0.1, 'fist_slam_counter.mp3', 0.45)
_at('boss_talon', 0.4, 'stamp.mp3', 0.7)
_at('boss_talon', 0.9, 'paper_crumple_slap.mp3', 0.35)
_at('stakeout', 0.0, 'amb_night_crickets.mp3', 0.25, a=0.0, b=3.0)
_at('stake_cu', 0.2, 'battery_die_beeps.mp3', 0.25)
_at('truck_pass', 0.0, 'truck_horn_old.mp3', 0.45)
_at('truck_pass', 0.1, 'whoosh.mp3', 0.45)
_at('chase', 0.0, 'monowheel_whine.mp3', 0.6); _at('chase', 1.1, 'whoosh.mp3', 0.5)
_at('gate_night', 0.0, 'gate_rolling.mp3', 0.5)
_at('tank_wide', 0.3, 'radiator_valve_gush.mp3', 0.4)
_at('tank_wide', 0.0, 'pipes_rumble.mp3', 0.35)
_at('tank_flip', 0.0, 'counter_blip.mp3', 0.6); _at('tank_flip', 0.5, 'brass_fanfare_short.mp3', 0.18)
_at('valve_tilt', 0.0, 'heartbeat_slow.mp3', 0.5)
_at('valve_plate', 0.0, 'record_scratch.mp3', 0.4)
_at('maz_shock', 0.0, 'crowd_gasp.mp3', 0.3)
_at('maz_shock', 0.0, 'thunder_crack.mp3', 0.3)
_at('boss_run', 0.0, 'flashlight_click.mp3', 0.6); _at('boss_run', 0.2, 'stairs_run.mp3', 0.45)
_at('valve_turn', 0.2, 'valve_creak.mp3', 0.8); _at('valve_turn', 1.4, 'radiator_valve_gush.mp3', 0.7)
_at('valve_turn', 1.6, 'slowmo_whoosh.mp3', 0.4)
_at('crowd_gate', 0.0, 'car_honks_chorus.mp3', 0.45); _at('crowd_gate', 0.4, 'crowd_cheer_short.mp3', 0.45)
_at('banner_fall', 0.0, 'counter_blip.mp3', 0.5); _at('banner_fall', 0.5, 'counter_blip.mp3', 0.5)
_at('banner_fall', 1.0, 'counter_blip.mp3', 0.5); _at('banner_fall', 1.4, 'sad_trombone.mp3', 0.3)
_at('boss_cry', 0.0, 'crowd_sigh.mp3', 0.25)
_at('cop_drive', 0.0, 'old_car_start_roar.mp3', 0.45)
_at('zoya_dance', 0.0, 'crowd_cheer_short.mp3', 0.3)
_at('maz_canister', 0.0, 'water_pour_head.mp3', 0.4)
_at('hatch', 0.3, 'electric_zap_sparks.mp3', 0.55)
_at('wheel_end', 0.0, 'battery_die_beeps.mp3', 0.25)
_at('loud_end', 0.0, 'pa_chime_feedback.mp3', 0.45)
_at('loud_end', 3.2, 'gate_rolling.mp3', 0.45)
_at('sign_back', 0.2, 'paper_crumple_slap.mp3', 0.45)
_at('loop_pump', 1.6, 'water_drip_single.mp3', 0.8)
_at('credits', 0.0, 'title_stinger.mp3', 0.45)
_at('s2_card', 0.05, 'electric_zap_sparks.mp3', 0.4)
_at('s2_card', 0.4, 'title_stinger.mp3', 0.55)

AMB = dict(azs=('library/sfx/amb_night_crickets.mp3', 7.8, 0.22), gate=('library/sfx/amb_refinery.mp3', 7.8, 0.28),
           garage=('library/sfx/amb_basement.mp3', 7.8, 0.2), kiosk=('library/sfx/amb_refinery.mp3', 7.8, 0.12),
           garages=('library/sfx/amb_night_crickets.mp3', 7.8, 0.25), highway=('library/sfx/wind_gust.mp3', 3.5, 0.12),
           office=('library/sfx/amb_office_night.mp3', 7.8, 0.22), night=('library/sfx/amb_night_crickets.mp3', 7.8, 0.3),
           chase=('library/sfx/wind_gust.mp3', 3.5, 0.25), tank=('library/sfx/amb_refinery.mp3', 7.8, 0.3),
           hero=('library/sfx/amb_refinery.mp3', 7.8, 0.3), crowd=('library/sfx/amb_refinery.mp3', 7.8, 0.22),
           end=('library/sfx/amb_refinery.mp3', 7.8, 0.18), credits=('library/sfx/amb_night_crickets.mp3', 7.8, 0.12))
NOIR, CHASE, HERO, THEME = MUS + 'noir_detective_16s.mp3', MUS + 'chase_surf_12s.mp3', MUS + 'valve_hero_16s.mp3', MUS + 'mazutych_theme_15s.mp3'
MLOOP = {NOIR: 16.0, CHASE: 12.0, HERO: 16.0, THEME: 14.6}
MUSIC = dict(azs=(NOIR, 0.20), gate=(THEME, 0.14), garage=(NOIR, 0.2), kiosk=(NOIR, 0.18), garages=(NOIR, 0.18), highway=(THEME, 0.14),
             office=(NOIR, 0.18), night=(NOIR, 0.16), chase=(CHASE, 0.28), tank=(NOIR, 0.14), hero=(HERO, 0.4), crowd=(THEME, 0.24),
             end=(THEME, 0.16), credits=(NOIR, 0.3))


def _minus(a, b):
    """[a, b) without the flashback spans (the flashback brings its own music and ambience)"""
    out = [(a, b)]
    for c in CLIPS:
        c0, c1 = c['t0'] - 0.25, c['t0'] + (c['b'] - c['a']) + 0.25
        out = [p for x0, x1 in out for p in ((x0, min(x1, c0)), (max(x0, c1), x1)) if p[1] - p[0] > 0.4]
    return out


BEDS = []
for sc, a, b in SCENE_SPANS:
    if b - a < 0.4: continue
    p, lp, g = AMB[sc]
    m, g2 = MUSIC[sc]
    for x0, x1 in _minus(a, b):
        BEDS.append((p, lp, x0, x1, g, False))
        BEDS.append((m, MLOOP[m], x0, x1, g2, True))

VGAIN = {'maz': 1.55, 'wheel': 1.4, 'zoya': 1.45, 'zoyam': 1.45, 'boss': 1.4, 'bossh': 1.4, 'tolik': 1.45, 'vadik': 1.55, 'cop': 1.45}
VFX = {}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:3d} {s['t0']:7.2f} {s['t1'] - s['t0']:5.2f}  {s['name']}  {s.get('key', '')}")
    print('DUR', DUR, f'{int(DUR // 60)}:{DUR % 60:04.1f}', 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}', 'shots', len(SHOTS),
          'flash', round(sum(c['b'] - c['a'] for c in CLIPS), 1))
    for c in CHAPTERS: print(f'{int(c[0] // 60)}:{int(c[0] % 60):02d}', c[1])
