"""«FLORIDA MAN ON TRIAL» — extended season cut (16:9). The whole film is one timeline built from BEATS:
  ('L', key, shot)        a court line (voice/movie_t/<key>.mp3), the shot is held for the line + pad
  ('P', seconds, shot)    a silent beat (reaction, insert, title)
  ('X', n)                Exhibit n: episode n played on the courtroom screen (two parts joined by a VHS fast-forward)
  ('C', n, title)         count card n
Each beat is one shot (CUTS / NAMES) — movie.py renders by shots (engine/episode.py `all` / `shots`), mix.py mixes VOICE/SFX/BEDS."""
import json, subprocess, pathlib, importlib.util

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = 'florida-man'
FPS = 30
MASTER = 0.86
VEP = 'movie_t'
S = 'library/sfx/'

LINES = json.load(open(ROOT / 'series' / SLUG / 'voice' / 'movie' / 'lines.json'))
SPK = {k: v[0] for k, v in LINES.items()}
CAP = {k: v[1].split(']', 1)[-1].strip() for k, v in LINES.items()}


def _clip_lens():
    cache = ROOT / 'build' / f'{SLUG}-movie' / 'clip_lens.json'
    d = json.load(open(cache)) if cache.exists() else {}
    changed = False
    for k in LINES:
        f = ROOT / 'series' / SLUG / 'voice' / VEP / f'{k}.mp3'
        key = f'{k}:{int(f.stat().st_mtime)}'
        if key not in d:
            d[key] = float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                          capture_output=True, text=True).stdout)
            changed = True
    if changed:
        cache.parent.mkdir(parents=True, exist_ok=True); json.dump(d, open(cache, 'w'))
    return {k.split(':')[0]: v for k, v in d.items()}


CLIP = _clip_lens()


def _ep_timing(n):
    spec = importlib.util.spec_from_file_location(f'tl{n}', ROOT / 'series' / SLUG / 'episodes' / f'ep0{n}' / 'timeline.py')
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m.DUR, m.TWIST


EX_LEN = 26.0          # target length of one exhibit (s)
FF = 0.5               # VHS fast-forward between the two parts
EXHIBIT = {}
for n in range(1, 7):
    d, tw = _ep_timing(n)
    p2 = (max(0.1, tw - 0.6), d - 0.05)                     # twist -> button
    p1_len = max(4.0, EX_LEN - FF - (p2[1] - p2[0]))
    EXHIBIT[n] = dict(src=f'build/{SLUG}-ep0{n}/final_noend.mp4', p1=(0.1, 0.1 + p1_len), p2=p2, letter='ABCDEF'[n - 1])

COUNTS = {1: 'TRESPASSING IN FROZEN FOODS', 2: 'FALSE REPORT OF A ROBBERY', 3: 'PRACTICING DOG WITHOUT A LICENSE',
          4: 'INSURANCE FRAUD (AGAINST HIMSELF)', 5: 'UNPAID RENT (PYTHON)', 6: 'BREAKING INTO JAIL'}

BEATS = [
    # ---- cold open (hook)
    ('P', 0.9, 'gavel'), ('L', 'c_t1', 'bench_cu'), ('L', 'c_f1', 'fm_cu'), ('L', 'c_m1', 'mort_cu'), ('P', 1.7, 'hook'),
    ('P', 4.6, 'title'),
    # ---- opening statements
    ('L', 'o_t0', 'bench_gavel'), ('P', 1.0, 'wide'), ('L', 'o_d1', 'darlene_med'), ('L', 'o_t1', 'bench'), ('L', 'o_d2', 'darlene_cu'), ('L', 'o_m1', 'mort_cu'),
    ('L', 'o_t2', 'bench'), ('L', 'o_m2', 'def_two'), ('P', 1.1, 'jury'),
    # ---- count 1
    ('C', 1), ('L', 'a_d1', 'tv_in'), ('L', 'a_m1', 'mort_cu'), ('L', 'a_t1', 'bench_gavel'), ('X', 1),
    ('L', 'a_t2', 'bench_cu'), ('L', 'a_m2', 'mort_cu'), ('L', 'a_t3', 'bench_cu'), ('P', 0.9, 'jury'),
    # ---- count 2
    ('C', 2), ('P', 1.3, 'witness_tag'), ('L', 'b_d1', 'darlene_med'), ('L', 'b_m1', 'mort_cu'), ('L', 'b_t1', 'bench'), ('X', 2), ('L', 'b_m2', 'mort_cu'), ('L', 'b_d2', 'darlene_cu'), ('L', 'b_m3', 'mort_gulp'),
    # ---- count 3
    ('C', 3), ('X', 3), ('L', 'e_d1', 'scan'), ('L', 'e_t1', 'bench_cu'), ('L', 'e_f1', 'fm_cu'), ('P', 1.8, 'jury_python'),
    # ---- twist: the judge takes the stand
    ('L', 'w_m1', 'mort_stand'), ('L', 'w_t1', 'witness'), ('L', 'w_m2', 'badges'), ('L', 'w_t2', 'badges2'), ('P', 1.0, 'jury_gasp'),
    ('L', 'w_t3', 'witness_cu'), ('L', 'w_m3', 'mort_cu'),
    # ---- count 4
    ('C', 4), ('X', 4), ('L', 'g_f1', 'fm_cu'), ('L', 'g_t1', 'bench_gavel'),
    # ---- count 5
    ('C', 5), ('X', 5), ('L', 'h_d1', 'darlene_med'), ('L', 'h_m1', 'mort_cu'), ('P', 1.0, 'jury_python'),
    # ---- count 6
    ('C', 6), ('X', 6), ('P', 1.6, 'iguana'), ('L', 'i_d1', 'darlene_med'), ('L', 'i_t1', 'bench_cu'),
    # ---- verdict
    ('L', 'v_t0', 'bench'), ('P', 1.6, 'foreman'), ('L', 'v_t1', 'bench_cu'), ('P', 1.5, 'cheer'), ('L', 'v_f1', 'fm_cu'), ('L', 'v_t2', 'bench_gavel'),
    ('L', 'v_f2', 'fm_shriek'), ('L', 'v_d1', 'cuffs'), ('P', 3.4, 'credits'),
    # ---- after the credits
    ('P', 0.9, 'snow'), ('L', 'p_m1', 'snow_mort'), ('P', 3.4, 'snow_s2'),
]

PAD = 0.28
CARD_DUR = 1.9

# ---------------------------------------------------------------- build the timeline
SHOTS = []          # dict(name, t0, t1, kind, ...)
VOICE, SFX = [], []
t = 0.0
count = 0
for i, b in enumerate(BEATS):
    if b[0] == 'L':
        key, shot = b[1], b[2]
        dur = CLIP[key] + PAD
        VOICE.append((key, VEP, key, round(t + 0.06, 3), 0.0, CLIP[key], SPK[key], CAP[key]))
        SHOTS.append(dict(name=shot, t0=t, t1=t + dur, kind='line', key=key, count=count))
    elif b[0] == 'P':
        dur = b[1]
        SHOTS.append(dict(name=b[2], t0=t, t1=t + dur, kind='pause', count=count))
    elif b[0] == 'C':
        count = b[1]
        dur = CARD_DUR
        SHOTS.append(dict(name='card', t0=t, t1=t + dur, kind='card', n=b[1], title=COUNTS[b[1]], count=count))
        SFX.append((S + 'gavel_bang.mp3', t + 0.15, 0.9)); SFX.append((S + 'title_stinger.mp3', t + 0.1, 0.35))
    elif b[0] == 'X':
        e = EXHIBIT[b[1]]
        l1 = e['p1'][1] - e['p1'][0]; l2 = e['p2'][1] - e['p2'][0]
        dur = 0.35 + l1 + FF + l2
        SHOTS.append(dict(name='exhibit', t0=t, t1=t + dur, kind='exhibit', n=b[1], count=count, a1=t + 0.35, f0=t + 0.35 + l1,
                          a2=t + 0.35 + l1 + FF))
        SFX.append((S + 'tv_static_blip.mp3', t, 0.6))
        SFX.append((e['src'], t + 0.35, 1.0, e['p1'][0], e['p1'][1]))
        SFX.append((S + 'vhs_rewind.mp3', t + 0.35 + l1, 0.5, 0.0, FF))
        SFX.append((e['src'], t + 0.35 + l1 + FF, 1.0, e['p2'][0], e['p2'][1]))
    t += dur
DUR = round(t, 3)
CUTS = [s['t0'] for s in SHOTS] + [DUR]
NAMES = [f"{i:02d}_{s['name']}" for i, s in enumerate(SHOTS)]
TWIST = next(s['t0'] for s in SHOTS if s.get('key') == 'w_m1')
CHAPTERS = [(0.0, 'Hook')] + [(s['t0'], 'Opening Statements') for s in SHOTS if s['name'] == 'wide'][:1] + \
           [(s['t0'], f"Count {s['n']}: {COUNTS[s['n']].title()}") for s in SHOTS if s['kind'] == 'card'] + \
           [(TWIST, 'The Judge Takes the Stand')] + [(s['t0'], 'Verdict') for s in SHOTS if s['name'] == 'foreman'] + \
           [(s['t0'], 'Season 2') for s in SHOTS if s['name'] == 'snow']
CHAPTERS.sort()


def shot_at(tt):
    for s in SHOTS:
        if s['t0'] <= tt < s['t1']: return s
    return SHOTS[-1]


# ---------------------------------------------------------------- point SFX (court) + beds
def _at(name, dt, path, g):
    for s in SHOTS:
        if s['name'] == name: SFX.append((S + path, s['t0'] + dt, g))


_at('gavel', 0.25, 'gavel_bang.mp3', 1.0)
_at('hook', 0.0, 'record_scratch.mp3', 0.5)
_at('hook', 0.05, 'gavel_bang.mp3', 0.8)
_at('title', 0.0, 'title_stinger.mp3', 0.6)
_at('bench_gavel', 0.15, 'gavel_bang.mp3', 0.8)
_at('mort_gulp', 0.5, 'gator_gulp.mp3', 0.6)
_at('witness_tag', 0.2, 'handcuffs_click.mp3', 0.6)
_at('scan', 0.0, 'scanner_beep.mp3', 0.8)
_at('jury_python', 0.3, 'python_hiss.mp3', 0.5)
_at('mort_stand', 0.0, 'slowmo_whoosh.mp3', 0.4)
_at('witness', 0.0, 'camera_flash.mp3', 0.6)
_at('witness', 0.02, 'news_breaking_sting.mp3', 0.45)
_at('jury_gasp', 0.05, 'crowd_gasp.mp3', 0.8)
_at('iguana', 0.9, 'gator_gulp.mp3', 0.0)
_at('iguana', 0.95, 'debris_crash.mp3', 0.25)
_at('foreman', 0.3, 'paper_unroll.mp3', 0.5)
_at('cheer', 0.0, 'crowd_cheer_short.mp3', 0.8)
_at('cheer', 0.05, 'brass_fanfare_short.mp3', 0.45)
_at('fm_shriek', 0.0, 'record_scratch.mp3', 0.45)
_at('cuffs', 0.4, 'handcuffs_click.mp3', 0.9)
_at('cuffs', 0.8, 'hole_punch.mp3', 0.8)
_at('credits', 0.0, 'tv_static_soft.mp3', 0.3)
_at('snow_s2', 0.1, 'title_stinger.mp3', 0.5)
SFX[:] = [s for s in SFX if s[2] > 0]

# beds: courtroom room tone + the theme under court talk, both muted during exhibits (the episode brings its own mix)
BEDS = []
seg0 = 0.0
for s in SHOTS:
    if s['kind'] == 'exhibit':
        if s['t0'] - seg0 > 0.5:
            BEDS.append((S + 'amb_boardroom.mp3', 7.9, seg0, s['t0'], 0.22, True))
            BEDS.append(('series/florida-man/music/fm_theme_15s.mp3', 14.9, seg0, s['t0'], 0.16, True))
        seg0 = s['t1']
BEDS.append((S + 'amb_boardroom.mp3', 7.9, seg0, DUR, 0.22, True))
BEDS.append(('series/florida-man/music/fm_theme_15s.mp3', 14.9, seg0, DUR, 0.2, True))

VGAIN = {'fm': 1.9, 'tanner': 1.45, 'mort': 1.7, 'darlene': 1.65}
VFX = {}

if __name__ == '__main__':
    for s in SHOTS: print(f"{s['t0']:7.2f} {s['t1'] - s['t0']:5.2f}  {s['name']}")
    print('DUR', DUR, f'{int(DUR // 60)}:{DUR % 60:04.1f}', 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}', 'shots', len(SHOTS))
    for c in CHAPTERS: print(f'{int(c[0] // 60)}:{int(c[0] % 60):02d}', c[1])
