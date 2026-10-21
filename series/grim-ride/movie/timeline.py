"""«Grim Ride: ONE MORE HOUR» — Halloween time-loop mini-movie (16:9). One timeline built from BEATS:
  ('L', key, shot)              a new line (voice/movie_t/<key>.mp3); the shot holds for the line + PAD
  ('R', 'epNN_t:key', shot)     a season line reused from that episode (same voices, 0 credits)
  ('P', seconds, shot)          a silent beat
  ('S', scene)                  switches ambience / music bed;  ('O', loop_no) sets the loop counter shown in the HUD
movie.py renders by shots, mix.py mixes VOICE / SFX / BEDS."""
import json, subprocess, pathlib

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SLUG = 'grim-ride'
FPS = 30
MASTER = 0.9
VEP = 'movie_t'
S = 'library/sfx/'
G = f'series/{SLUG}/sfx/'
MUS = f'series/{SLUG}/music/'
SER = ROOT / 'series' / SLUG


def _dur(f):
    return float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', str(f)],
                                capture_output=True, text=True).stdout)


def _cap(text):
    return ' '.join(text.split(']')[-1].split())


LINES = json.load(open(SER / 'voice' / 'movie' / 'lines.json'))
OLD = {}
for ep in ('ep01', 'ep02', 'ep03', 'ep04', 'ep05', 'ep06'):
    for k, v in json.load(open(SER / 'episodes' / ep / 'lines.json')).items(): OLD[f'{ep}_t:{k}'] = v


def line(key):
    """(vep, file key, speaker, caption, clip seconds)"""
    if ':' in key:
        vep, k = key.split(':'); who, txt = OLD[key]
    else:
        vep, k = VEP, key; who, txt = LINES[key]
    return vep, k, who, _cap(txt), _dur(SER / 'voice' / vep / f'{k}.mp3')


BEATS = [
    # 1. COLD OPEN: loop two, 1:59:59 -> 2:00 -> 1:00 again
    ('S', 'cold'), ('O', 2),
    ('L', 'g01', 'cold_ride'), ('P', 1.5, 'cold_harold'), ('P', 2.0, 'cold_flip'),
    ('S', 'street'),
    ('L', 'd01', 'cold_app'), ('L', 'g02', 'grim_again_cu'), ('L', 'e01', 'edgar_lamp'), ('L', 'g03', 'grim_shriek'),
    ('L', 'e02', 'edgar_lamp2'),
    ('S', 'title'), ('P', 4.2, 'title'),
    # 2. THE RULES: infinite hours, infinite tries
    ('S', 'hill'), ('O', 3),
    ('L', 'g04', 'hill_plan'), ('P', 2.6, 'plan_sign'), ('L', 'g05', 'hill_grand'), ('L', 'e03', 'edgar_herewego'),
    # 3. LOOP 3 — PLAN A: SPEED
    ('S', 'loop'),
    ('P', 1.5, 'card_a'), ('P', 1.8, 'a_approach'), ('P', 1.3, 'a_tarp'), ('R', 'ep01_t:h2', 'a_catch'), ('P', 1.7, 'a_chase'),
    ('R', 'ep01_t:g6', 'a_slowdown'), ('R', 'ep01_t:e3', 'a_battery'), ('P', 1.6, 'rewind'),
    # 4. LOOP 9 — PLAN B: THE APP
    ('O', 9),
    ('P', 1.5, 'card_b'), ('R', 'ep02_t:g1', 'b_captcha'), ('R', 'ep02_t:d1', 'b_human'), ('R', 'ep02_t:g2', 'b_death'),
    ('R', 'ep02_t:d6', 'b_eternity'), ('R', 'ep02_t:g7', 'b_myline'), ('P', 1.6, 'rewind'),
    # 5. LOOP 17 — PLAN C: CANDY
    ('O', 17),
    ('P', 1.5, 'card_c'), ('R', 'ep03_t:g1', 'c_line'), ('R', 'ep03_t:m1', 'c_mom'), ('R', 'ep03_t:g2', 'c_four'),
    ('R', 'ep03_t:m2', 'c_no'), ('R', 'ep03_t:e2', 'c_carded'), ('P', 1.6, 'rewind'),
    # 6. LOOP 24 — PLAN D: THE PLUG
    ('O', 24),
    ('P', 1.5, 'card_d'), ('R', 'ep04_t:g1', 'd_plug'), ('R', 'ep04_t:e1', 'd_forty'), ('P', 2.4, 'd_rocket'), ('P', 1.4, 'd_crash'),
    ('R', 'ep04_t:e5', 'd_norefunds'), ('P', 1.6, 'rewind'),
    # 7. LOOP 31 — PLAN E: DISGUISE
    ('O', 31),
    ('P', 1.5, 'card_e'), ('R', 'ep05_t:g1', 'e_dontmove'), ('R', 'ep05_t:t2', 'e_fog'), ('R', 'ep05_t:g3', 'e_time'),
    ('R', 'ep05_t:t3', 'e_animatronic'), ('P', 1.6, 'rewind'),
    # 8. LOOP 40 — PLAN F: ASK NICELY
    ('O', 40),
    ('P', 1.5, 'card_f'), ('R', 'ep06_t:g1', 'f_ask'), ('R', 'ep01_t:h1', 'f_body'), ('R', 'ep01_t:g5', 'f_plan'), ('P', 1.2, 'f_slam'),
    ('P', 1.6, 'rewind'),
    # 9. LOOP 45 — PLAN G: HIRE THE GANG
    ('O', 45),
    ('P', 1.5, 'card_g'), ('R', 'ep04_t:k2', 'g_cop'), ('R', 'ep04_t:g3', 'g_costume'), ('R', 'ep04_t:k4', 'g_customer'),
    ('P', 1.6, 'rewind'),
    # 10. MONTAGE — PLANS H to Z
    ('S', 'montage'), ('O', 46),
    ('P', 1.4, 'card_hz'), ('P', 2.0, 'm_pizza'), ('L', 'h01', 'm_pizza_door'), ('O', 49), ('P', 2.2, 'm_ghost'), ('O', 50),
    ('L', 'e04', 'm_loop50'), ('O', 61), ('P', 2.6, 'm_moon'), ('O', 68), ('P', 1.8, 'm_kevin'), ('O', 73), ('L', 'e05', 'm_loop73'),
    ('P', 2.6, 'm_counter'),
    # 11. LOW POINT: loop 96
    ('S', 'low'), ('O', 96),
    ('P', 2.2, 'low_wide'), ('L', 'g06', 'low_cu'), ('L', 'e06', 'low_edgar'), ('L', 'g07', 'low_ready'), ('P', 3.4, 'low_clues'),
    # 12. TWIST: Harold is the one doing it
    ('S', 'twist'),
    ('P', 1.8, 'h_arrive'), ('L', 'h02', 'h_rough'), ('L', 'g08', 'g_remember'), ('L', 'h03', 'h_doing'), ('P', 3.6, 'twist_reveal'),
    ('L', 'h04', 'h_byhand'), ('L', 'g09', 'g_rewinding'), ('L', 'h05', 'h_recycle'), ('L', 'g10', 'g_deactivated'),
    ('L', 'h06', 'h_race'), ('L', 'g11', 'g_ifyou'), ('L', 'h07', 'h_onemore'), ('P', 2.0, 'deal_shake'), ('L', 'e07', 'e_contract'),
    # 13. THE RACE
    ('S', 'race'), ('O', 97),
    ('P', 2.6, 'race_line'), ('R', 'ep06_t:k1', 'race_kayden'), ('R', 'ep06_t:t1', 'race_todd'), ('R', 'ep06_t:d0', 'race_app'),
    ('P', 2.2, 'race_kids'), ('L', 'e08', 'race_count'), ('P', 1.2, 'race_go'), ('P', 2.6, 'race_down'), ('P', 2.4, 'race_gang'),
    ('R', 'ep06_t:g3', 'race_woohoo'), ('P', 2.6, 'race_moon'), ('P', 2.0, 'race_kevin'),
    ('P', 2.4, 'race_fog'), ('P', 2.4, 'race_street'), ('P', 2.2, 'race_lead'), ('P', 2.8, 'race_brake'), ('L', 'e09', 'race_braked'),
    ('P', 1.8, 'race_win'), ('L', 'h08', 'h_letwin'), ('L', 'g12', 'g_battery'), ('L', 'e10', 'e_didnot'),
    # 14. 2:00 AM, STANDARD TIME
    ('S', 'end'),
    ('P', 3.0, 'end_clock'), ('R', 'ep06_t:d1', 'end_app'), ('R', 'ep06_t:g4', 'end_stars'), ('P', 2.4, 'end_town'),
    ('P', 1.8, 'end_porch'), ('L', 'h09', 'end_sametime'), ('L', 'g13', 'end_bike'), ('R', 'ep06_t:e1', 'end_nevermore'),
    # 15. CREDITS + POST-CREDITS: spring forward
    ('S', 'credits'), ('P', 9.0, 'credits'),
    ('S', 'post'),
    ('P', 2.2, 'post_card'), ('P', 1.8, 'post_flip'), ('L', 'g14', 'post_grim'), ('L', 'h10', 'post_harold'), ('P', 4.4, 's2_card'),
]

PAD = 0.36
SHOTS, VOICE, SFX = [], [], []
SCENE_SPANS = []
t = 0.0
scene = None
loop_no = 1
for b in BEATS:
    k = b[0]
    if k == 'S':
        scene = b[1]; SCENE_SPANS.append([scene, t, None]); continue
    if k == 'O':
        loop_no = b[1]; continue
    if k in ('L', 'R'):
        vep, key, who, cap, clip = line(b[1])
        dur = clip + PAD
        VOICE.append((f'{key}@{len(VOICE)}', vep, key, round(t + 0.06, 3), 0.0, clip, who, cap))
        SHOTS.append(dict(name=b[2], t0=t, t1=t + dur, kind='line', key=b[1], who=who, scene=scene, loop=loop_no))
    else:
        dur = b[1]
        SHOTS.append(dict(name=b[2], t0=t, t1=t + dur, kind='pause', scene=scene, loop=loop_no))
    t += dur
DUR = round(t, 3)
for i, sp in enumerate(SCENE_SPANS): sp[2] = SCENE_SPANS[i + 1][1] if i + 1 < len(SCENE_SPANS) else DUR
CUTS = [s['t0'] for s in SHOTS] + [DUR]
NAMES = [f"{i:03d}_{s['name']}" for i, s in enumerate(SHOTS)]
for i, s in enumerate(SHOTS): s['i'] = i


def first(name, nth=0):
    return [s for s in SHOTS if s['name'] == name][nth]


def all_(name):
    return [s for s in SHOTS if s['name'] == name]


def shot_at(tt):
    for s in SHOTS:
        if s['t0'] <= tt < s['t1']: return s
    return SHOTS[-1]


TWIST = first('h_doing')['t0']
CHAPTERS = [(0.0, 'Loop two'), (first('hill_plan')['t0'], 'Infinite tries'), (first('card_a')['t0'], 'Plan A: Speed'),
            (first('card_b')['t0'], 'Plan B: The App'), (first('card_c')['t0'], 'Plan C: Candy'), (first('card_d')['t0'], 'Plan D: The Plug'),
            (first('card_e')['t0'], 'Plan E: Disguise'), (first('card_f')['t0'], 'Plan F: Ask Nicely'),
            (first('card_g')['t0'], 'Plan G: Hire the Gang'), (first('card_hz')['t0'], 'Plans H to Z'), (first('low_wide')['t0'], 'Loop 96'),
            (first('h_arrive')['t0'], 'Rough loop, kid?'), (first('race_line')['t0'], 'The Race'), (first('end_clock')['t0'], 'Standard Time'),
            (first('credits')['t0'], 'Credits')]


def _at(name, dt, path, g, nth=None, a=None, b=None):
    for i, s in enumerate(all_(name)):
        if nth is not None and i != nth: continue
        SFX.append((path, s['t0'] + dt, g) + ((a, b) if a is not None else ()))


# ---------------------------------------------------------------- point SFX (the season's own set + the library it used)
_at('cold_ride', 0.0, S + 'thunder_crack.mp3', 0.45); _at('cold_ride', 0.0, G + 'etrike_zoom.mp3', 0.55)
_at('cold_harold', 0.1, S + 'rocking_creak.mp3', 0.5); _at('cold_harold', 0.3, S + 'clock_fast_ticks.mp3', 0.35)
for nm in ('cold_flip', 'rewind'):
    _at(nm, 0.0, S + 'clock_midnight_chime.mp3', 0.45); _at(nm, 0.45, S + 'record_scratch.mp3', 0.5)
    _at(nm, 0.55, S + 'vhs_rewind.mp3', 0.55)
_at('cold_app', 0.05, S + 'app_notify_ping.mp3', 0.55)
_at('edgar_lamp', 0.0, G + 'raven_caw.mp3', 0.25)
_at('title', 0.05, S + 'title_stinger.mp3', 0.6); _at('title', 0.0, S + 'thunder_crack.mp3', 0.35)
_at('plan_sign', 0.2, S + 'pencil_scribble.mp3', 0.6); _at('plan_sign', 1.3, S + 'pencil_scribble.mp3', 0.5)
_at('hill_grand', 0.3, S + 'thunder_crack.mp3', 0.5); _at('hill_grand', 0.2, S + 'cloak_shimmer.mp3', 0.5)
for nm in ('card_a', 'card_b', 'card_c', 'card_d', 'card_e', 'card_f', 'card_g', 'card_hz'):
    _at(nm, 0.0, S + 'counter_blip.mp3', 0.6); _at(nm, 0.15, S + 'film_click.mp3', 0.5)
_at('a_approach', 0.0, G + 'etrike_rev.mp3', 0.5)
_at('a_tarp', 0.1, S + 'cloth_flap.mp3', 0.6); _at('a_tarp', 0.4, G + 'etrike_rev.mp3', 0.55)
_at('a_catch', 0.6, G + 'etrike_zoom.mp3', 0.6)
_at('a_chase', 0.0, S + 'whoosh.mp3', 0.55); _at('a_chase', 0.6, G + 'etrike_zoom.mp3', 0.5)
_at('a_battery', 0.0, S + 'battery_die_beeps.mp3', 0.5)
_at('b_captcha', 0.4, S + 'ui_tap_chirp.mp3', 0.5); _at('b_captcha', 0.9, G + 'flatline_beep.mp3', 0.35)
_at('b_human', 0.0, S + 'app_notify_ping.mp3', 0.4)
_at('b_eternity', 0.0, S + 'hold_music_elise.mp3', 0.3)
_at('c_line', 0.0, S + 'doorbell_chime.mp3', 0.45)
_at('c_carded', 0.0, S + 'stamp.mp3', 0.5)
_at('d_plug', 0.0, S + 'neon_buzz_tense.mp3', 0.3)
_at('d_forty', 0.4, S + 'cash_register.mp3', 0.45)
_at('d_rocket', 0.0, G + 'etrike_zoom.mp3', 0.7); _at('d_rocket', 0.2, S + 'slowmo_whoosh.mp3', 0.5)
_at('d_crash', 0.05, S + 'debris_crash.mp3', 0.7); _at('d_crash', 0.1, S + 'junk_avalanche.mp3', 0.35)
_at('e_dontmove', 0.3, S + 'needle_prick.mp3', 0.5)
_at('e_fog', 0.6, S + 'pencil_scribble.mp3', 0.5)
_at('e_animatronic', 0.0, S + 'crowd_gasp.mp3', 0.5); _at('e_animatronic', 0.3, S + 'camera_flash.mp3', 0.6)
_at('e_animatronic', 0.9, S + 'camera_flash.mp3', 0.5)
_at('f_ask', 0.0, S + 'doorbell_chime.mp3', 0.5)
_at('f_slam', 0.0, S + 'fist_slam_counter.mp3', 0.6)
_at('g_cop', 0.0, S + 'neon_buzz_tense.mp3', 0.25)
_at('m_pizza', 0.2, S + 'doorbell_chime.mp3', 0.5)
_at('m_ghost', 0.3, G + 'raisin_bonk.mp3', 0.6)
_at('m_moon', 0.0, S + 'slowmo_whoosh.mp3', 0.5); _at('m_moon', 1.6, S + 'debris_crash.mp3', 0.45)
_at('m_kevin', 0.3, S + 'tape_measure.mp3', 0.45)
_at('m_counter', 0.0, S + 'clock_fast_ticks.mp3', 0.5); _at('m_counter', 0.3, S + 'vhs_rewind.mp3', 0.4)
_at('m_counter', 1.3, S + 'vhs_rewind.mp3', 0.4)
_at('low_wide', 0.2, S + 'crowd_sigh.mp3', 0.25)
_at('low_clues', 0.0, S + 'vhs_rewind.mp3', 0.3); _at('low_clues', 0.1, S + 'clock_fast_ticks.mp3', 0.4)
_at('h_arrive', 0.0, G + 'etrike_rev.mp3', 0.45)
_at('h_doing', 0.0, S + 'heartbeat_slow.mp3', 0.45)
_at('twist_reveal', 0.0, S + 'record_scratch.mp3', 0.55); _at('twist_reveal', 0.05, S + 'thunder_crack.mp3', 0.5)
_at('twist_reveal', 0.6, S + 'valve_creak.mp3', 0.6); _at('twist_reveal', 1.2, S + 'clock_midnight_chime.mp3', 0.5)
_at('twist_reveal', 1.4, S + 'vhs_rewind.mp3', 0.45)
_at('h_race', 0.2, S + 'starter_pistol.mp3', 0.0)
_at('e_contract', 0.0, G + 'raven_caw.mp3', 0.2)
_at('race_line', 0.0, S + 'crowd_cheer_short.mp3', 0.4); _at('race_line', 0.3, S + 'fireworks_distant.mp3', 0.3)
_at('race_todd', 0.3, S + 'steam_hiss_soft.mp3', 0.45)
_at('race_app', 0.0, S + 'app_notify_ping.mp3', 0.5)
_at('deal_shake', 0.3, S + 'electric_zap_sparks.mp3', 0.45); _at('deal_shake', 0.2, S + 'thunder_crack.mp3', 0.3)
_at('race_kids', 0.0, S + 'crowd_cheer_short.mp3', 0.35)
_at('race_gang', 0.0, G + 'etrike_rev.mp3', 0.4); _at('race_gang', 0.4, S + 'car_honks_chorus.mp3', 0.25)
_at('race_moon', 0.0, S + 'slowmo_whoosh.mp3', 0.5); _at('race_moon', 0.3, S + 'choir_hallelujah_short.mp3', 0.2)
_at('race_kevin', 0.2, S + 'tape_measure.mp3', 0.4)
_at('race_go', 0.0, S + 'starter_pistol.mp3', 0.6); _at('race_go', 0.1, G + 'etrike_zoom.mp3', 0.7)
_at('race_down', 0.0, S + 'whoosh.mp3', 0.6); _at('race_down', 1.2, G + 'etrike_zoom.mp3', 0.5)
_at('race_fog', 0.0, S + 'steam_hiss_soft.mp3', 0.45); _at('race_fog', 0.4, S + 'whoosh.mp3', 0.45)
_at('race_street', 0.0, S + 'fireworks_distant.mp3', 0.5); _at('race_street', 0.5, G + 'etrike_zoom.mp3', 0.5)
_at('race_lead', 0.0, S + 'clock_fast_ticks.mp3', 0.45)
_at('race_brake', 0.9, S + 'brake_skid.mp3', 0.7); _at('race_brake', 0.0, S + 'heartbeat_slow.mp3', 0.45)
_at('race_win', 0.0, S + 'crowd_cheer_short.mp3', 0.55); _at('race_win', 0.1, S + 'brass_fanfare_short.mp3', 0.4)
_at('e_didnot', 0.0, G + 'raven_caw.mp3', 0.2)
_at('end_clock', 0.0, S + 'clock_fast_ticks.mp3', 0.5); _at('end_clock', 1.5, S + 'clock_midnight_chime.mp3', 0.55)
_at('end_app', 0.0, S + 'app_notify_ping.mp3', 0.5)
_at('end_stars', 0.0, S + 'choir_hallelujah_short.mp3', 0.25)
_at('end_town', 0.2, S + 'flashlight_click.mp3', 0.4); _at('end_town', 0.9, S + 'flashlight_click.mp3', 0.35)
_at('end_porch', 0.0, S + 'rocking_creak.mp3', 0.5)
_at('end_nevermore', 0.0, G + 'raven_caw.mp3', 0.3)
_at('credits', 0.0, S + 'title_stinger.mp3', 0.45)
_at('post_card', 0.0, S + 'film_click.mp3', 0.5)
_at('post_flip', 0.0, S + 'clock_midnight_chime.mp3', 0.45); _at('post_flip', 0.5, S + 'record_scratch.mp3', 0.5)
_at('s2_card', 0.0, S + 'thunder_crack.mp3', 0.45); _at('s2_card', 0.3, S + 'title_stinger.mp3', 0.55)

NIGHT = S + 'amb_night_crickets.mp3'
AMB = dict(cold=(NIGHT, 6.9, 0.25), street=(NIGHT, 6.9, 0.3), title=(NIGHT, 6.9, 0.15), hill=(S + 'wind_gust.mp3', 3.5, 0.15),
           loop=(NIGHT, 6.9, 0.25), montage=(NIGHT, 6.9, 0.18), low=(S + 'wind_gust.mp3', 3.5, 0.18), twist=(NIGHT, 6.9, 0.28),
           race=(S + 'wind_gust.mp3', 3.5, 0.25), end=(NIGHT, 6.9, 0.3), credits=(NIGHT, 6.9, 0.12), post=(NIGHT, 6.9, 0.25))
THEME, WALTZ, RACE, PORCH = MUS + 'grim_theme_15s.mp3', MUS + 'loop_waltz_12s.mp3', MUS + 'race_12s.mp3', MUS + 'porch_12s.mp3'
MLOOP = {THEME: 14.6, WALTZ: 12.0, RACE: 11.43, PORCH: 12.0}
MUSIC = dict(cold=(RACE, 0.22), street=(WALTZ, 0.16), title=(THEME, 0.4), hill=(THEME, 0.18), loop=(WALTZ, 0.2), montage=(WALTZ, 0.32),
             low=(PORCH, 0.12), twist=(PORCH, 0.16), race=(RACE, 0.3), end=(PORCH, 0.2), credits=(THEME, 0.4), post=(WALTZ, 0.16))

BEDS = []
for sc, a, b in SCENE_SPANS:
    if b - a < 0.4: continue
    p, lp, g = AMB[sc]
    m, g2 = MUSIC[sc]
    BEDS.append((p, lp, a, b, g, False))
    BEDS.append((m, MLOOP[m], a, b, g2, True))

VGAIN = {'grim': 1.6, 'edgar': 1.6, 'todd': 1.5, 'harold': 1.6, 'kayden': 1.5, 'dashley': 1.5, 'mom': 1.5}
VFX = {}

if __name__ == '__main__':
    for i, s in enumerate(SHOTS): print(f"{i:3d} {s['t0']:7.2f} {s['t1'] - s['t0']:5.2f}  L{s['loop']:<3d} {s['name']}  {s.get('key', '')}")
    print('DUR', DUR, f'{int(DUR // 60)}:{DUR % 60:04.1f}', 'twist', round(TWIST, 2), f'{TWIST / DUR:.0%}', 'shots', len(SHOTS))
    for c in CHAPTERS: print(f'{int(c[0] // 60)}:{int(c[0] % 60):02d}', c[1])
