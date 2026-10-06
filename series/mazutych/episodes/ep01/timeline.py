"""S01E01 «Круговорот» — timing for video (ep01.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep01_t)."""
DUR = 36.5
FPS = 30
SLUG = 'mazutych'
MASTER = 0.68

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('m1', 'ep01_t', 'm1', 0.00, 0.00, 3.19, 'maz', 'Двадцать пять лет делаю БЕНЗИН.'),
    ('m2', 'ep01_t', 'm2', 3.30, 0.00, 2.51, 'maz', 'А заправиться — НЕГДЕ.'),
    ('z1', 'ep01_t', 'z1', 5.90, 0.00, 2.94, 'zoya', 'Бензина НЕТ! Ждём бензовоз!'),
    ('m3', 'ep01_t', 'm3', 10.65, 0.00, 1.30, 'maz', 'БЕНЗОВОЗ...'),
    ('m4', 'ep01_t', 'm4', 12.85, 0.00, 0.96, 'maz', 'Щёлк-щёлк.'),
    ('z2', 'ep01_t', 'z2', 17.75, 0.00, 0.71, 'zoya', 'МИМО.'),
    ('w1', 'ep01_t', 'w1', 18.70, 0.00, 3.03, 'wheel', 'Заряд ТРИ процент. Ты ехать тише, друга.'),
    ('b1', 'ep01_t', 'b1', 25.00, 0.00, 3.86, 'boss', 'Ура, товарищи! План — СТО СОРОК ОДИН процент!'),
    ('w2', 'ep01_t', 'w2', 29.10, 0.00, 1.24, 'wheel', 'Всё. Я спать.'),
    ('m1b', 'ep01_t', 'm1', 30.60, 0.00, 3.19, 'maz', 'Двадцать пять лет делаю бензин...'),
    ('m5', 'ep01_t', 'm5', 34.05, 0.00, 1.93, 'maz', 'Один и тот ЖЕ.'),
]

# shot boundaries (ep01.py)
CUTS = [0.0, 3.10, 5.75, 8.85, 10.50, 12.10, 14.00, 15.60, 17.00, 17.60, 18.60, 21.80, 22.80, 24.90, 27.20, 29.00, 30.40, DUR]

S = 'library/sfx/'
SFX = [
    (S + 'wind_gust.mp3', 0.00, 0.55),
    (S + 'car_honks_chorus.mp3', 3.70, 0.55),
    (S + 'whoosh.mp3', 5.70, 0.35),
    (S + 'gate_rolling.mp3', 8.85, 0.8),
    (S + 'truck_horn_old.mp3', 9.40, 0.75),
    (S + 'slowmo_whoosh.mp3', 10.45, 0.5),
    (S + 'whoosh.mp3', 12.10, 0.7),
    (S + 'truck_horn_old.mp3', 12.15, 0.55, 0.0, 0.9),
    (S + 'blinker_clicks.mp3', 13.10, 0.45, 0.0, 0.8),
    (S + 'car_honks_chorus.mp3', 14.20, 0.45),
    (S + 'car_pothole_drop.mp3', 15.95, 0.8),
    (S + 'bath_splash.mp3', 16.45, 0.4, 0.0, 0.6),
    (S + 'whoosh.mp3', 17.00, 0.6),
    (S + 'car_honks_chorus.mp3', 18.15, 0.55),
    (S + 'battery_die_beeps.mp3', 18.60, 0.45, 0.0, 0.9),
    (S + 'whoosh.mp3', 21.80, 0.5),
    (S + 'record_scratch.mp3', 23.55, 0.7),
    (S + 'gate_rolling.mp3', 24.20, 0.6),
    (S + 'pa_chime_feedback.mp3', 24.70, 0.55),
    (S + 'counter_blip.mp3', 25.55, 0.7),
    (S + 'crowd_cheer_short.mp3', 25.80, 0.45),
    (S + 'fireworks_distant.mp3', 26.00, 0.35),
    (S + 'battery_die_beeps.mp3', 30.20, 0.75),
    (S + 'wind_gust.mp3', 33.80, 0.35),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('library/sfx/amb_refinery.mp3', 7.8, 0.0, DUR, 0.55, False),
    ('library/sfx/monowheel_whine.mp3', 3.8, 0.0, 30.3, 0.32, True),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 0.0, 29.2, 0.26, True),
]

MEGA = 'highpass=f=420,lowpass=f=3600,acompressor=threshold=0.25:ratio=4,volume=1.25'
VFX = {'zoya': MEGA, 'boss': 'highpass=f=320,lowpass=f=3400,aecho=0.8:0.6:140:0.35,volume=1.3',
       'wheel': 'highpass=f=240,aecho=0.6:0.5:12:0.25'}
VGAIN = {'maz': 1.6, 'zoya': 1.5, 'wheel': 1.45, 'boss': 1.45}
