"""«Валера и кот. Дембельский альбом» — extended season cut (16:9). One timeline built from BEATS:
  ('L', key, shot)                       a new line (voice/movie_t/<key>.mp3), the shot is held for the line + PAD
  ('R', vep, key, a, b, who, cap, shot)  a line reused from an episode (voice/<vep>/<key>.mp3, clip a..b)
  ('P', seconds, shot)                   a silent beat
  ('C', n)                               chapter card: page flip + «ГЛАВА N» on the album page
  ('V', n)                               Valera stencils his heroic caption for chapter n (top-down album page)
  ('X', n)                               episode n comes alive inside its photo (two parts joined by a fast-forward)
  ('K', n)                               the cat writes the truth under the caption (clip frozen on its last frame)
Each beat is one shot (CUTS / NAMES) — movie.py renders by shots, mix.py mixes VOICE / SFX / BEDS."""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = 'valera-i-kot'
FPS = 30
MASTER = 0.88
VEP = 'movie_t'
S = 'library/sfx/'

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / 'movie' / 'lines.json'))
SPK = {k: v[0] for k, v in LINES.items()}
CAP = {k: v[1].split(']', 1)[-1].strip() for k, v in LINES.items()}


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


def _clip_lens():
    cache = ROOT / 'build' / f'{SLUG}-movie' / 'clip_lens.json'
    d = json.load(open(cache)) if cache.exists() else {}
    changed = False
    for k in LINES:
        f = ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3'
        key = f'{k}:{int(f.stat().st_mtime)}'
        if key not in d:
            d[key] = _dur(f); changed = True
    if changed:
        cache.parent.mkdir(parents=True, exist_ok=True); json.dump(d, open(cache, 'w'))
    return {k.split(':')[0]: v for k, v in d.items()}


CLIP = _clip_lens()

# ---------------------------------------------------------------- the six episodes: which parts go into the album
PARTS = {1: [(0.0, 9.4), (17.1, 29.6)],          # «ЛЕДЯНАЯ!» … «На складе.» >> батарея … «Копчёный.»
         2: [(0.0, 15.9), (22.6, 27.0)],         # «СКОЛЬКО?!» … «А я тридцать — на кассе.» >> «И пакет.» «Пакет — девяносто.»
         3: [(0.0, 11.6), (19.0, 28.1)],         # бабки на посту … «Я сугроб.» >> «Договоримся?» … «Готовь пакет.»
         4: [(0.0, 6.4), (12.85, 34.1)],         # «Алло! ЖЭК?!» 143-й >> «Где горячая вода?!» … «Вы — сто сорок…» (звонок в дверь)
         5: [(0.0, 8.9), (15.85, 29.0)],         # «Операция «Кипяток»» … кот >> «Пошла, родимая!» … «Всё включено.»
         6: [(0.0, 6.4), (8.3, 24.2)]}           # «Тридцать первое!» >> «ДАЛИ!» … «Теперь — наша.»
FF = 0.45            # fast-forward between the two parts
ZOOM = 0.45          # dive into the photo before the episode starts

TITLES = {1: 'ЗАКАЛКА', 2: 'СКОЛЬКО?!', 3: 'ОНИ ВИДЯТ ВСЁ', 4: 'ВЫ 143-Й', 5: 'КИПЯТОК', 6: 'С ЛЁГКИМ ПАРОМ', 7: 'ЛЕДЯНАЯ'}
STENCIL = {1: ['ДЕНЬ 1.', 'ЗАКАЛЯЛСЯ.', 'НЕ ДРОГНУЛ.'], 2: ['ДЕНЬ 6.', 'ОТСТОЯЛ', 'ЦЕНУ!'], 3: ['ДЕНЬ 11.', 'РАЗВЕДКА.', 'НЕЗАМЕЧЕН.'],
           4: ['ДЕНЬ 16.', 'ПЕРЕГОВОРЫ.', 'НЕ СДАЛСЯ.'], 5: ['ДЕНЬ 24.', 'ОПЕРАЦИЯ', '«КИПЯТОК».', 'УСПЕХ!'],
           6: ['ДЕНЬ 31.', 'НОВЫЙ ГОД.', 'ТРАДИЦИЯ.'], 7: ['ДЕНЬ 32.', 'ЖЭК ПРИНЯЛ', 'ВОДНЫЕ', 'ПРОЦЕДУРЫ.']}
TRUTH = {1: ['Орал.'], 2: ['Пакет — 90.'], 3: ['Спалился', 'за 20 сек.'], 4: [], 5: ['Отопил двор.'], 6: ['Кот помылся', 'первым.'],
         7: ['Отомстил.']}
PHOTO_T = {1: 1.2, 2: 0.6, 3: 6.6, 4: 30.6, 5: 25.0, 6: 19.0}      # still frame of each episode for its album photo
DECALS = {1: ('kettle', 'flake'), 2: ('sausage', 'heart'), 3: ('bench', 'cat'), 4: ('phone', 'drop'), 5: ('drop', 'star'),
          6: ('tree', 'star'), 7: ('ushanka', 'drop')}

BEATS = [
    # ---- ХУК: Нина Петровна под ледяным душем у Валеры, вспышка, фото в альбом
    ('L', 'h_n1', 'nina_ice'), ('P', 0.55, 'photo_fall'), ('L', 'h_v1', 'page_last'), ('L', 'h_c1', 'cat_cu'), ('L', 'h_c2', 'pages_back'),
    ('P', 4.0, 'title'),
    # ---- пролог: кухня, 05:40
    ('L', 'p_v1', 'v_cu'), ('R', 'ep06', 'c4', 0.11, 1.25, 'cat', 'ТРАДИЦИЯ.', 'cat_cu'), ('L', 'p_r1', 'radio'),
    ('L', 'p_v2', 'album_open'), ('L', 'p_v3', 'v_med'), ('L', 'p_c1', 'cat_pencil'),
    # ---- глава 1
    ('C', 1), ('V', 1), ('X', 1), ('K', 1), ('L', 'a_v1', 'v_cu'), ('L', 'a_c1', 'cat_cu'),
    # ---- глава 2
    ('C', 2), ('P', 2.6, 'receipt'), ('V', 2), ('X', 2), ('L', 'b_v1', 'trophy'), ('K', 2), ('L', 'b_c1', 'cat_cu'),
    # ---- глава 3
    ('C', 3), ('L', 'c_v1', 'v_cu_whisper'), ('V', 3), ('P', 0.9, 'spy_flip'), ('L', 'c_v2', 'spy_page'), ('L', 'c_c1', 'cat_cu'),
    ('X', 3), ('K', 3),
    # ---- глава 4 → звонок в дверь
    ('C', 4), ('L', 'd_v1', 'v_cu'), ('V', 4), ('X', 4),
    # ---- ПОВОРОТ: ЖЭК пришёл мыться к Валере
    ('P', 0.8, 'doorbell'), ('L', 't_n1', 'nina_door'), ('P', 1.4, 'v_smile'), ('L', 't_c1', 'cat_cu'), ('L', 't_v1', 'v_hall'),
    ('L', 't_n2', 'nina_door_cu'), ('L', 't_v2', 'v_hall'), ('L', 't_c2', 'cat_cu_whisper'), ('P', 1.2, 'kit_two'),
    ('L', 't_n3', 'page_nina'), ('L', 't_v3', 'v_cu_smug'),
    # ---- глава 5
    ('C', 5), ('L', 'e_v1', 'v_cu_smug'), ('V', 5), ('X', 5), ('L', 'e_n1', 'nina_cu_angry'), ('L', 'e_n2', 'nina_cu'),
    ('P', 1.1, 'yard'), ('R', 'ep05', 'z2', 0.2, 1.08, 'zina', 'Мест НЕТ.', 'pool_zina'),
    ('R', 'ep05', 'l1', 0.0, 2.42, 'lyuba', 'Всё ВКЛЮЧЕНО.', 'pool_lyuba'), ('P', 1.4, 'nina_frost'), ('K', 5),
    # ---- глава 6
    ('C', 6), ('L', 'f_v1', 'v_cu'), ('V', 6), ('X', 6), ('L', 'f_n1', 'nina_cu_soft'),
    ('R', 'ep06', 'c4', 0.11, 1.25, 'cat', 'ТРАДИЦИЯ.', 'cat_cu'), ('L', 'f_n2', 'nina_cu_plead'), ('K', 6),
    # ---- развязка: ванна свободна
    ('L', 'z_v1', 'kit_two_grand'), ('L', 'z_c1', 'cat_cu'), ('P', 1.0, 'bath_wide'), ('L', 'h_n1', 'nina_ice'),
    ('P', 0.55, 'photo_fall'), ('V', 7), ('K', 7),
    # ---- кнопка: кот впервые отдаёт честь
    ('L', 'k_v1', 'salute'), ('P', 1.8, 'cat_salute'),
    # ---- титры и после титров
    ('P', 7.0, 'credits'), ('P', 2.2, 'summer_notice'), ('L', 's_c1', 'summer_valera'), ('P', 3.6, 's2_card'),
]

PAD = 0.26
CARD = 1.7
VDUR = 2.3
KDUR = 2.3

SHOTS, VOICE, SFX = [], [], []
t = 0.0
chap = 0
for b in BEATS:
    k = b[0]
    if k == 'L':
        key, shot = b[1], b[2]
        dur = CLIP[key] + PAD
        VOICE.append((f'{key}@{len(VOICE)}', VEP, key, round(t + 0.05, 3), 0.0, CLIP[key], SPK[key], CAP[key]))
        SHOTS.append(dict(name=shot, t0=t, t1=t + dur, kind='line', key=key, chap=chap))
    elif k == 'R':
        _, vep, key, a, bb, who, cap, shot = b
        dur = (bb - a) + PAD
        VOICE.append((f'{vep}{key}@{len(VOICE)}', vep, key, round(t + 0.05, 3), a, bb, who, cap))
        SHOTS.append(dict(name=shot, t0=t, t1=t + dur, kind='line', key=f'{vep}/{key}', chap=chap))
    elif k == 'P':
        dur = b[1]
        SHOTS.append(dict(name=b[2], t0=t, t1=t + dur, kind='pause', chap=chap))
    elif k == 'C':
        chap = b[1]; dur = CARD
        SHOTS.append(dict(name='card', t0=t, t1=t + dur, kind='card', n=chap, chap=chap))
        SFX.append((S + 'album_page_flip.mp3', t + 0.05, 1.0)); SFX.append((S + 'title_stinger.mp3', t + 0.5, 0.3))
    elif k == 'V':
        dur = VDUR
        SHOTS.append(dict(name='stencil', t0=t, t1=t + dur, kind='stencil', n=b[1], chap=chap))
        SFX.append((S + 'spray_paint_soft.mp3', t + 0.25, 0.45, 0.0, 1.3))
    elif k == 'K':
        dur = KDUR if TRUTH[b[1]] else 0.0
        if dur:
            SHOTS.append(dict(name='truth', t0=t, t1=t + dur, kind='truth', n=b[1], chap=chap))
            SFX.append((S + 'pencil_scribble.mp3', t + 0.3, 0.8))
    elif k == 'X':
        n = b[1]
        (a1, b1), (a2, b2) = PARTS[n]
        l1, l2 = b1 - a1, b2 - a2
        dur = ZOOM + l1 + FF + l2
        src = f'series/{SLUG}/episodes/ep0{n}/final.mp4'
        SHOTS.append(dict(name='clip', t0=t, t1=t + dur, kind='clip', n=n, chap=chap, s1=t + ZOOM, f0=t + ZOOM + l1, s2=t + ZOOM + l1 + FF))
        SFX.append((S + 'whoosh.mp3', t, 0.4))
        SFX.append((src, t + ZOOM, 0.95, a1, b1))
        SFX.append((S + 'vhs_rewind.mp3', t + ZOOM + l1, 0.4, 0.0, FF))
        SFX.append((src, t + ZOOM + l1 + FF, 0.95, a2, b2))
    t += dur
DUR = round(t, 3)
CUTS = [s['t0'] for s in SHOTS] + [DUR]
NAMES = [f"{i:02d}_{s['name']}" for i, s in enumerate(SHOTS)]
TWIST = next(s['t0'] for s in SHOTS if s['name'] == 'doorbell')


def first(name, nth=0):
    return [s for s in SHOTS if s['name'] == name][nth]


CHAPTERS = [(0.0, 'Альбом готов'), (first('v_cu')['t0'], 'Пролог')] + \
           [(s['t0'], f"Глава {s['n']}. {TITLES[s['n']].capitalize()}") for s in SHOTS if s['kind'] == 'card'] + \
           [(TWIST, 'Звонок в дверь'), (first('bath_wide')['t0'], 'Ледяная'), (first('summer_notice')['t0'], 'Сезон 2')]
CHAPTERS.sort()


def shot_at(tt):
    for s in SHOTS:
        if s['t0'] <= tt < s['t1']: return s
    return SHOTS[-1]


def _at(name, dt, path, g, nth=None, a=None, b=None):
    for i, s in enumerate([s for s in SHOTS if s['name'] == name]):
        if nth is not None and i != nth: continue
        SFX.append((S + path, s['t0'] + dt, g) + ((a, b) if a is not None else ()))


_at('nina_ice', 0.0, 'shower_cold_spray.mp3', 0.8)
_at('photo_fall', 0.0, 'camera_flash.mp3', 0.9)
_at('photo_fall', 0.35, 'book_thud.mp3', 0.35)
_at('pages_back', 0.0, 'album_page_flip.mp3', 0.8); _at('pages_back', 0.45, 'album_page_flip.mp3', 0.7)
_at('pages_back', 0.9, 'album_page_flip.mp3', 0.7); _at('pages_back', 1.35, 'album_page_flip.mp3', 0.6)
_at('title', 0.05, 'book_thud.mp3', 0.6); _at('title', 0.2, 'title_stinger.mp3', 0.5)
_at('v_cu', 0.1, 'teeth_chatter.mp3', 0.5, nth=0)
_at('radio', 0.0, 'tv_static_soft.mp3', 0.35)
_at('album_open', 0.0, 'book_thud.mp3', 0.5); _at('album_open', 0.4, 'album_page_flip.mp3', 0.7)
_at('receipt', 0.0, 'receipt_printer.mp3', 0.6); _at('receipt', 0.5, 'paper_unroll.mp3', 0.6)
_at('trophy', 0.1, 'plastic_bag_rustle.mp3', 0.5)
_at('spy_flip', 0.0, 'album_page_flip.mp3', 0.8)
_at('spy_page', 0.0, 'record_scratch.mp3', 0.35)
_at('doorbell', 0.0, 'doorbell_soviet_trill.mp3', 1.0)
_at('nina_door', 0.0, 'crowd_gasp.mp3', 0.5)
_at('nina_door', 0.0, 'camera_flash.mp3', 0.3)
_at('v_smile', 0.3, 'sax_sting_swell.mp3', 0.25)
_at('kit_two', 0.1, 'chair_scoot.mp3', 0.6)
_at('yard', 0.0, 'geyser_steam.mp3', 0.4)
_at('nina_frost', 0.1, 'teeth_chatter.mp3', 0.8)
_at('bath_wide', 0.55, 'tap_squeak.mp3', 0.8)
_at('salute', 0.0, 'boots_stomp.mp3', 0.5)
_at('cat_salute', 0.35, 'brass_fanfare_short.mp3', 0.55)
_at('credits', 0.0, 'album_page_flip.mp3', 0.7)
_at('summer_notice', 0.0, 'stamp.mp3', 0.8)
_at('s2_card', 0.05, 'title_stinger.mp3', 0.6)

# beds: kitchen dawn + the series theme between the episodes (the episodes bring their own mix)
BEDS = []
seg0 = 0.0
for s in SHOTS + [dict(kind='end', t0=DUR, t1=DUR)]:
    if s['kind'] in ('clip', 'end'):
        if s['t0'] - seg0 > 0.5:
            BEDS.append(('library/sfx/amb_flat_winter.mp3', 7.8, seg0, s['t0'], 0.3, False))
            BEDS.append((f'series/{SLUG}/music/theme_panelka_15s.mp3', 14.6, seg0, s['t0'], 0.16, True))
        seg0 = s['t1']

VGAIN = {'valera': 1.5, 'cat': 1.5, 'nina': 1.55, 'robot': 1.4, 'zina': 1.45, 'lyuba': 1.45}
VFX = {'robot': 'highpass=f=280,lowpass=f=3400,acompressor=threshold=0.2:ratio=4,volume=1.2'}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:3d} {s['t0']:7.2f} {s['t1'] - s['t0']:5.2f}  {s['name']}")
    print('DUR', DUR, f'{int(DUR // 60)}:{DUR % 60:04.1f}', 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}', 'shots', len(SHOTS))
    for c in CHAPTERS: print(f'{int(c[0] // 60)}:{int(c[0] % 60):02d}', c[1])
