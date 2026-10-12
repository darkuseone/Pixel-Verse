"""«Валера и кот: ПРОПУСКНОЙ РЕЖИМ» — new-year mini-movie (16:9). One timeline built from BEATS:
  ('L', key, shot)        a line (voice/movie_t/<key>.mp3); the shot holds for the line + PAD
  ('P', seconds, shot)    a silent beat
Scenes ('S', name) switch the ambience / music bed. movie.py renders by shots (CUTS / NAMES), mix.py mixes VOICE / SFX / BEDS."""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = 'valera-i-kot'
FPS = 30
MASTER = 0.9
VEP = 'movie_t'
S = 'library/sfx/'
MUS = f'series/{SLUG}/music/'

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / 'movie' / 'lines.json'))
SPK = {k: v[0] for k, v in LINES.items()}
CAP = {k: v[1].split(']')[-1].replace('[pause]', '').strip() for k, v in LINES.items()}
CAP = {k: ' '.join(v.split()) for k, v in CAP.items()}


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


CLIP = {k: _dur(ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3') for k in LINES}

BEATS = [
    ('S', 'yard'),
    # 1. ХУК: бинокль против бинокля
    ('P', 1.3, 'bino'), ('L', 'v01', 'bino'), ('L', 'z01', 'bino_zina'), ('L', 'c01', 'window_out'), ('P', 2.6, 'title'),
    ('S', 'kitchen'),
    # 2. стол
    ('P', 2.2, 'table_pan'), ('L', 'v02', 'v_table'), ('L', 'v03', 'v_bottle'), ('L', 'c02', 'cat_sill'), ('L', 'v04', 'v_phone'),
    # 3. вербовка
    ('S', 'garage'),
    ('P', 2.2, 'garage_ring'), ('L', 'k01', 'kolyan_phone'), ('L', 'v05', 'v_phone_cu'), ('L', 'k02', 'kolyan_cu'),
    ('S', 'sroom'),
    ('P', 1.6, 'sroom_ring'), ('L', 's01', 'semenych_phone'), ('L', 's02', 'semenych_cu'),
    ('S', 'kitchen'),
    ('L', 'v06', 'split3'), ('L', 'c03', 'cat_cu'),
    # 4. брифинг
    ('L', 'v07', 'map'), ('L', 'v08', 'map'), ('L', 'c04', 'cat_bowl'), ('P', 1.6, 'fortochka'),
    ('S', 'yard'),
    ('P', 2.2, 'meet'), ('L', 's10', 'meet_cu'), ('L', 'k07', 'meet_kolyan'),
    # 5. гастроном
    ('S', 'shop'),
    ('P', 1.8, 'shop_wide'), ('L', 's03', 'shop_two'), ('L', 't01', 'tamara_cu'), ('L', 'k03', 'kolyan_shop'),
    ('P', 1.6, 'tamara_under'), ('L', 't02', 'tamara_jar'), ('L', 's04', 'semenych_sniff'), ('L', 't03', 'tamara_cu'),
    ('L', 't04', 'tamara_cu2'), ('P', 0.8, 'shop_phone'), ('L', 't05', 'tamara_phone'), ('P', 1.2, 'mates_glance'),
    # 6. попытка 1: сугробы
    ('S', 'yard'),
    ('P', 2.0, 'yard_mounds'), ('L', 'v09', 'v_radio'), ('L', 'l01', 'bench_two'), ('L', 'z02', 'zina_cu'), ('P', 0.9, 'mounds_cu'),
    ('L', 'z03', 'zina_shout'), ('P', 1.3, 'mounds_back'), ('L', 'c05', 'fail1'),
    # 7. попытка 2: Дед Мороз и Снегурочка
    ('S', 'garage'),
    ('P', 2.6, 'dress'), ('L', 'k08', 'dress_mirror'),
    ('S', 'yard'),
    ('P', 1.8, 'dm_walk'), ('L', 's05', 'dm_hello'), ('L', 'z04', 'zina_cu'), ('L', 'l02', 'lyuba_cu'), ('L', 'k04', 'sneg_cu'),
    ('L', 'z05', 'zina_cu'), ('L', 's06', 'dm_poem'), ('L', 'z06', 'zina_cu'), ('L', 'c06', 'fail2'),
    # 8. ПОВОРОТ: переговоры, кот — двойной агент
    ('P', 1.8, 'v_flag'), ('L', 'v10', 'v_flag_cu'), ('P', 0.9, 'journal'), ('L', 'z07', 'zina_read'), ('L', 'v11', 'v_shock'),
    ('P', 2.4, 'tilt_up'), ('L', 'c07', 'cat_agent'), ('L', 'v12', 'v_betrayed'), ('L', 'c08', 'cat_agent2'),
    # 9. условия
    ('L', 'z08', 'bench_terms'), ('L', 'l03', 'lyuba_cu'), ('L', 'z09', 'zina_cu'), ('L', 'v13', 'v_defeat'),
    # 10. вечеринка
    ('S', 'party'),
    ('P', 2.0, 'party_wide'), ('L', 't06', 'tamara_enter'), ('L', 'z10', 'party_toast'), ('L', 'l04', 'lyuba_eat'),
    ('P', 2.2, 'party_dance'), ('L', 'l05', 'party_dance'), ('L', 'v17', 'trio_door'), ('L', 'z14', 'party_zina'),
    ('L', 'c10', 'cat_lap'), ('L', 'z11', 'party_zina'), ('L', 'v14', 'trio_door'), ('L', 'z12', 'party_zina'),
    # 11. полночь на лавочке
    ('S', 'midnight'),
    ('P', 3.0, 'yard_midnight'), ('L', 's07', 'trio_bench'), ('L', 'v15', 'trio_v'), ('L', 'k05', 'trio_kolyan'),
    ('L', 's08', 'trio_semenych'), ('L', 'k06', 'trio_kolyan'), ('L', 's09', 'trio_semenych'), ('P', 1.2, 'nina_come'),
    ('L', 'n01', 'nina_cu'), ('L', 'v16', 'v_guard'), ('L', 'z15', 'window_zina'), ('P', 1.6, 'yard_wide_end'), ('L', 'c09', 'cat_final'),
    # 12. титры и после титров
    ('P', 7.5, 'credits'),
    ('S', 'summer'),
    ('L', 'z13', 'summer'), ('P', 3.6, 's2_card'),
]

PAD = 0.38
SHOTS, VOICE, SFX = [], [], []
SCENE_SPANS = []
t = 0.0
scene = None
for b in BEATS:
    k = b[0]
    if k == 'S':
        scene = b[1]; SCENE_SPANS.append([scene, t, None]); continue
    if k == 'L':
        key, shot = b[1], b[2]
        dur = CLIP[key] + PAD
        VOICE.append((f'{key}@{len(VOICE)}', VEP, key, round(t + 0.08, 3), 0.0, CLIP[key], SPK[key], CAP[key]))
        SHOTS.append(dict(name=shot, t0=t, t1=t + dur, kind='line', key=key, scene=scene))
    else:
        dur = b[1]
        SHOTS.append(dict(name=b[2], t0=t, t1=t + dur, kind='pause', scene=scene))
    t += dur
DUR = round(t, 3)
for i, sp in enumerate(SCENE_SPANS): sp[2] = SCENE_SPANS[i + 1][1] if i + 1 < len(SCENE_SPANS) else DUR
CUTS = [s['t0'] for s in SHOTS] + [DUR]
NAMES = [f"{i:02d}_{s['name']}" for i, s in enumerate(SHOTS)]
TWIST = next(s['t0'] for s in SHOTS if s['name'] == 'tilt_up')


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


CHAPTERS = [(0.0, 'Лавочка'), (first('table_pan')['t0'], 'Стол накрыт'), (first('garage_ring')['t0'], 'Вербовка'),
            (first('map')['t0'], 'Операция «Оливье»'), (first('shop_wide')['t0'], 'Компот из-под прилавка'),
            (first('yard_mounds')['t0'], 'Попытка №1: сугробы'), (first('dm_walk')['t0'], 'Попытка №2: Дед Мороз'),
            (first('v_flag')['t0'], 'Переговоры'), (first('party_wide')['t0'], 'Капитуляция'),
            (first('yard_midnight')['t0'], 'Полночь на посту'), (first('credits')['t0'], 'Титры')]


def _at(name, dt, path, g, nth=None, a=None, b=None):
    for i, s in enumerate(all_(name)):
        if nth is not None and i != nth: continue
        SFX.append((S + path, s['t0'] + dt, g) + ((a, b) if a is not None else ()))


_at('bino', 0.0, 'film_click.mp3', 0.5)
_at('bino', 1.0, 'record_scratch.mp3', 0.35, nth=0)
_at('bino_zina', 0.0, 'whoosh.mp3', 0.4)
_at('title', 0.05, 'title_stinger.mp3', 0.6)
_at('table_pan', 0.1, 'ice_clink.mp3', 0.35)
_at('v_bottle', 0.5, 'glass_slide.mp3', 0.4)
_at('v_phone', 0.2, 'phone_pickup.mp3', 0.6)
_at('garage_ring', 0.0, 'doorbell_soviet_trill.mp3', 0.5)
_at('garage_ring', 0.5, 'rocking_creak.mp3', 0.5)
_at('sroom_ring', 0.0, 'doorbell_soviet_trill.mp3', 0.45)
_at('split3', 0.0, 'whoosh.mp3', 0.35)
_at('map', 0.1, 'ketchup_squirt_soft.mp3', 0.6, nth=0)
_at('map', 1.5, 'ketchup_squirt_soft.mp3', 0.5, nth=0)
_at('map', 0.3, 'glass_slide.mp3', 0.35, nth=1)
_at('cat_bowl', 0.2, 'cat_chewing.mp3', 0.6)
_at('fortochka', 0.0, 'wind_gust.mp3', 0.4)
_at('shop_wide', 0.0, 'shop_bell.mp3', 0.6)
_at('shop_two', 0.1, 'gum_pop.mp3', 0.3)
_at('tamara_under', 0.2, 'bucket_clang.mp3', 0.35)
_at('tamara_under', 0.9, 'glass_slide.mp3', 0.5)
_at('tamara_jar', 0.0, 'choir_hallelujah_short.mp3', 0.35)
_at('tamara_cu2', 0.6, 'plastic_bag_rustle.mp3', 0.45)
_at('tamara_cu2', 1.4, 'cash_register.mp3', 0.45)
_at('shop_phone', 0.0, 'doorbell_soviet_trill.mp3', 0.45)
_at('mates_glance', 0.1, 'piano_stop.mp3', 0.35)
_at('yard_mounds', 0.0, 'snow_crawl.mp3', 0.7)
_at('mounds_cu', 0.0, 'snow_crawl.mp3', 0.6)
_at('mounds_cu', 0.3, 'ice_clink.mp3', 0.35)
_at('zina_shout', 0.0, 'police_whistle.mp3', 0.4)
_at('mounds_back', 0.0, 'snow_crawl.mp3', 0.7)
_at('fail1', 0.0, 'camera_flash.mp3', 0.6); _at('fail1', 0.1, 'sad_trombone.mp3', 0.35)
_at('meet', 0.0, 'snow_steps.mp3', 0.6); _at('dress', 0.3, 'cloth_flap.mp3', 0.5); _at('dress', 1.4, 'ribbon_snap.mp3', 0.4)
_at('dm_walk', 0.0, 'snow_steps.mp3', 0.7); _at('dm_walk', 0.4, 'ice_clink.mp3', 0.3)
_at('dm_poem', 0.0, 'brass_fanfare_short.mp3', 0.2)
_at('fail2', 0.0, 'camera_flash.mp3', 0.6); _at('fail2', 0.1, 'sad_trombone.mp3', 0.35)
_at('v_flag', 0.0, 'cloth_flap.mp3', 0.5); _at('v_flag', 0.5, 'snow_steps.mp3', 0.5)
_at('journal', 0.0, 'album_page_flip.mp3', 0.7)
_at('v_shock', 0.0, 'record_scratch.mp3', 0.35, nth=0)
_at('tilt_up', 0.0, 'heartbeat_slow.mp3', 0.5); _at('tilt_up', 1.8, 'tank_knock_hollow.mp3', 0.45)
_at('cat_agent', 0.0, 'neon_buzz_tense.mp3', 0.2)
_at('v_betrayed', 0.0, 'crowd_gasp.mp3', 0.3)
_at('v_defeat', 0.0, 'sad_trombone.mp3', 0.25)
_at('party_wide', 0.0, 'crowd_cheer_short.mp3', 0.3)
_at('tamara_enter', 0.0, 'saloon_doors_bang.mp3', 0.25)
_at('party_toast', 1.4, 'ice_clink.mp3', 0.5)
_at('lyuba_eat', 0.0, 'big_bite_chew.mp3', 0.5)
_at('party_dance', 0.0, 'crowd_cheer_short.mp3', 0.25, nth=0)
_at('cat_lap', 0.2, 'cat_chewing.mp3', 0.5)
_at('yard_wide_end', 0.0, 'fireworks_distant.mp3', 0.6)
_at('yard_midnight', 0.0, 'clock_midnight_chime.mp3', 0.6); _at('yard_midnight', 0.8, 'fireworks_distant.mp3', 0.7)
_at('trio_bench', 0.5, 'fireworks_distant.mp3', 0.35)
_at('trio_v', 0.0, 'teeth_chatter.mp3', 0.4)
_at('nina_come', 0.0, 'snow_steps.mp3', 0.6); _at('nina_come', 0.4, 'basin_clank.mp3', 0.4)
_at('v_guard', 0.0, 'police_whistle.mp3', 0.45)
_at('cat_final', 0.4, 'fireworks_distant.mp3', 0.4)
_at('credits', 0.0, 'title_stinger.mp3', 0.4)
_at('s2_card', 0.05, 'title_stinger.mp3', 0.6)

AMB = dict(yard=('library/sfx/amb_winter_yard.mp3', 7.8, 0.32), kitchen=('library/sfx/amb_flat_winter.mp3', 7.8, 0.3),
           garage=('library/sfx/amb_basement.mp3', 7.8, 0.22), sroom=('library/sfx/amb_flat_winter.mp3', 7.8, 0.25),
           shop=('library/sfx/amb_grocery_store.mp3', 7.8, 0.3), party=('library/sfx/amb_flat_winter.mp3', 7.8, 0.3),
           midnight=('library/sfx/amb_winter_yard.mp3', 7.8, 0.3), summer=('library/sfx/amb_florida_yard_soft.mp3', 7.8, 0.25))
MUSIC = dict(yard=(MUS + 'operation_sneaky_15s.mp3', 0.16), kitchen=(MUS + 'theme_panelka_15s.mp3', 0.14),
             garage=(MUS + 'theme_panelka_15s.mp3', 0.12), sroom=(MUS + 'theme_panelka_15s.mp3', 0.12),
             shop=(MUS + 'theme_panelka_15s.mp3', 0.12), party=(MUS + 'new_year_15s.mp3', 0.2),
             midnight=(MUS + 'new_year_15s.mp3', 0.16), summer=(MUS + 'theme_panelka_15s.mp3', 0.16))
BEDS = []
for sc, a, b in SCENE_SPANS:
    if b - a < 0.4: continue
    p, lp, g = AMB[sc]; BEDS.append((p, lp, a, b, g, False))
    m, g2 = MUSIC[sc]; BEDS.append((m, 14.6, a, b, g2, True))

VGAIN = {'valera': 1.5, 'cat': 1.55, 'nina': 1.5, 'zina': 1.45, 'lyuba': 1.5, 'tamara': 1.45, 'kolyan': 1.55, 'semenych': 1.45}
VFX = {}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:3d} {s['t0']:7.2f} {s['t1'] - s['t0']:5.2f}  {s['name']}  {s.get('key', '')}")
    print('DUR', DUR, f'{int(DUR // 60)}:{DUR % 60:04.1f}', 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}', 'shots', len(SHOTS))
    for c in CHAPTERS: print(f'{int(c[0] // 60)}:{int(c[0] % 60):02d}', c[1])
