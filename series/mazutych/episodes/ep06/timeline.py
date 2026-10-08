"""S01E06 v2 «Почётный нефтяник» (08.10.2026, по статистике TikTok) — timing for video (ep06.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep06_t)."""
DUR = 32.4
FPS = 30
SLUG = 'mazutych'
MASTER = 0.78

VOICE = [
    ('b1', 'ep06_t', 'b1', 0.00, 0.00, 2.90, 'bossh', 'За двадцать пять лет — МАШИНА!'),
    ('m1', 'ep06_t', 'm1', 3.90, 0.00, 2.76, 'maz', 'Двадцать пять лет... СВОЯ!'),
    ('b2', 'ep06_t', 'b2', 6.80, 0.00, 3.58, 'bossh', 'Ключи. А бензин — по талону на ТАЛОН.'),
    ('w1', 'ep06_t', 'w1', 10.55, 0.00, 2.22, 'wheel', 'Опять ТОННА, друга.'),
    ('z1', 'ep06_t', 'z1', 12.95, 0.00, 1.68, 'zoya', 'Бензин ЕСТЬ.'),
    ('m2', 'ep06_t', 'm2', 15.65, 0.00, 1.06, 'maz', 'ЕСТЬ?!'),
    ('m3', 'ep06_t', 'm3', 17.80, 0.00, 1.38, 'maz', 'Это ЧТО?'),
    ('z2', 'ep06_t', 'z2', 19.35, 0.00, 1.36, 'zoya', 'ЭЛЕКТРИЧКА.'),
    ('m4', 'ep06_t', 'm4', 20.85, 0.00, 1.19, 'maz', 'А ЗАРЯДКА есть?'),
    ('z3', 'ep06_t', 'z3', 22.20, 0.00, 1.90, 'zoya', 'Зарядки НЕТ.'),
    ('w2', 'ep06_t', 'w2', 24.30, 0.00, 4.41, 'wheel', 'Я тоже НОЛЬ процент, друга.'),
    ('b3', 'ep06_t', 'b3', 28.90, 0.00, 2.09, 'boss', 'Розетка — по ТАЛОНУ.'),
]

#        hook  curtain cry   keys  bosscu tow    zoya1  sign   awe    flap   SOCKET zoya2  hope   zoya3  lcd    trio   bosswin title
CUTS = [0.0, 2.85, 3.85, 6.70, 8.50, 10.45, 12.85, 14.70, 15.60, 16.75, 17.40, 19.30, 20.80, 22.10, 24.15, 26.50, 28.80, 31.10, DUR]

S = 'library/sfx/'
SFX = [
    (S + 'brass_fanfare_short.mp3', 0.00, 0.55),
    (S + 'crowd_cheer_short.mp3', 0.10, 0.35),
    (S + 'curtain_reveal.mp3', 2.85, 0.5),
    (S + 'choir_hallelujah_short.mp3', 2.95, 0.45),
    (S + 'camera_flash.mp3', 3.20, 0.4),
    (S + 'coin_clink.mp3', 7.40, 0.6),
    (S + 'stamp.mp3', 9.70, 0.5),
    (S + 'rope_strain_creak.mp3', 10.50, 0.5),
    (S + 'monowheel_whine.mp3', 10.45, 0.35),
    (S + 'gum_pop.mp3', 14.55, 0.6),
    (S + 'choir_hallelujah_short.mp3', 14.75, 0.6),
    (S + 'paper_crumple_slap.mp3', 14.80, 0.4),
    (S + 'valve_creak.mp3', 16.95, 0.5),
    (S + 'electric_zap_sparks.mp3', 17.40, 0.8),
    (S + 'record_scratch.mp3', 17.42, 0.45),
    (S + 'gum_pop.mp3', 23.85, 0.6),
    (S + 'battery_die_beeps.mp3', 28.40, 0.5),
    (S + 'sad_trombone.mp3', 26.60, 0.35),
    (S + 'cash_register.mp3', 30.00, 0.5),
    (S + 'title_stinger.mp3', 31.10, 0.6),
]

BEDS = [
    ('library/sfx/amb_refinery.mp3', 8.0, 10.9, DUR, 0.25, False),
    ('series/mazutych/music/mazutych_theme_15s.mp3', 14.6, 0.0, DUR, 0.22, True),
]

VFX = {'wheel': 'highpass=f=240,aecho=0.6:0.5:12:0.25', 'bossh': 'aecho=0.7:0.5:70:0.18'}
VGAIN = {'maz': 1.6, 'zoya': 1.5, 'wheel': 1.45, 'boss': 1.5, 'bossh': 1.5}
