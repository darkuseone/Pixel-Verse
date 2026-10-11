"""S01E01 «Frozen Foods» — timing for video (ep01.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep01_t)."""
DUR = 33.0
FPS = 30
SLUG = 'florida-man'
MASTER = 0.72

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('f1', 'ep01_t', 'f1', 0.00, 0.00, 2.61, 'fm', 'NINE GRAND?! For the A/C?!'),
    ('t1', 'ep01_t', 't1', 2.66, 0.00, 2.30, 'tanner', "Compressor's DEAD! Three-week WAIT!"),
    ('f2', 'ep01_t', 'f2', 5.02, 0.00, 2.72, 'fm', "I'll be dead in three WEEKS."),
    ('t2', 'ep01_t', 't2', 7.78, 0.00, 2.35, 'tanner', 'No worries! Want the extended WARRANTY?'),
    ('f3', 'ep01_t', 'f3', 10.20, 0.00, 3.03, 'fm', 'Mort. Hold my SUB.'),
    ('m1', 'ep01_t', 'm1', 13.30, 0.00, 1.02, 'mort', 'What SUB?'),
    ('f4', 'ep01_t', 'f4', 14.42, 0.00, 3.40, 'fm', 'Ohhh. Sixty-EIGHT.'),
    ('t3', 'ep01_t', 't3', 17.88, 0.00, 3.76, 'tanner', 'Mine broke TOO! Three WEEKS!'),
    ('d1', 'ep01_t', 'd1', 22.70, 0.00, 3.32, 'darlene', "Sir. You can't LIVE in Frozen Foods."),
    ('f5', 'ep01_t', 'f5', 26.08, 0.00, 2.66, 'fm', "I'm not living, ma'am. I'm BROWSING."),
    ('d2', 'ep01_t', 'd2', 31.08, 0.00, 1.80, 'darlene', 'Broke. Nine GRAND.'),
]

# shot boundaries (ep01.py)
CUTS = [0.0, 2.64, 5.0, 7.76, 10.16, 13.26, 14.36, 16.15, 17.82, 19.75, 21.68, 22.68, 24.45, 26.04, 28.8, 29.85, 30.4, 31.0, DUR]
TWIST = 17.82                                   # 17.82 / 33.0 = 54 %

S = 'library/sfx/'
SFX = [
    (S + 'ac_compressor_die.mp3', 0.00, 0.75),
    (S + 'record_scratch.mp3', 0.02, 0.0),
    (S + 'cash_register.mp3', 0.15, 0.35),
    (S + 'app_notify_ping.mp3', 2.70, 0.30),
    (S + 'sad_trombone.mp3', 5.40, 0.22),
    (S + 'ui_tap_chirp.mp3', 7.80, 0.45),
    (S + 'gator_gulp.mp3', 12.95, 0.85),
    (S + 'store_doors_cold.mp3', 14.30, 0.9),
    (S + 'wind_gust.mp3', 14.40, 0.45),
    (S + 'book_thud.mp3', 16.90, 0.8),
    (S + 'freezer_door_pop.mp3', 17.62, 1.0),
    (S + 'record_scratch.mp3', 17.80, 0.6),
    (S + 'teeth_chatter.mp3', 19.80, 0.55),
    (S + 'crowd_gasp.mp3', 21.70, 0.35),
    (S + 'slowmo_whoosh.mp3', 21.62, 0.35),
    (S + 'gum_pop.mp3', 24.42, 0.7),
    (S + 'camera_flash.mp3', 28.80, 0.8),
    (S + 'news_breaking_sting.mp3', 28.82, 0.55),
    (S + 'hole_punch.mp3', 29.30, 0.9),
    (S + 'cell_door_clang.mp3', 29.85, 0.6),
    (S + 'ac_compressor_die.mp3', 30.42, 0.7),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    (S + 'amb_florida_yard_soft.mp3', 7.9, 0.0, 14.36, 0.3, True),
    (S + 'amb_grocery_store.mp3', 7.9, 14.36, 28.8, 0.9, True),
    ('series/florida-man/music/fm_theme_15s.mp3', 14.9, 0.0, 17.80, 0.24, True),
    ('series/florida-man/music/fm_theme_15s.mp3', 14.9, 19.7, DUR, 0.24, True),
]

VFX = {}
VGAIN = {'fm': 1.9, 'tanner': 1.45, 'mort': 1.7, 'darlene': 1.65}
