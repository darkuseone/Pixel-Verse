"""S01E01 «Dibs» — timing for video (ep01.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep01_t)."""
DUR = 37.8
FPS = 30
SLUG = 'agent-dibs'
MASTER = 0.80

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('d1', 'ep01_t', 'd1', 0.00, 0.00, 0.80, 'dibs', 'DIBS!'),
    ('deb1', 'ep01_t', 'deb1', 1.40, 0.00, 2.98, 'deb', 'Agent, why is something sizzling, hon?'),
    ('d2', 'ep01_t', 'd2', 4.50, 0.00, 2.27, 'dibs', 'Found the bomb. Called dibs.'),
    ('deb2', 'ep01_t', 'deb2', 6.90, 0.00, 1.72, 'deb', "Oh. That's different."),
    ('t1', 'ep01_t', 't1', 10.20, 0.00, 1.63, 'terry', "That's our bomb."),
    ('d3', 'ep01_t', 'd3', 11.90, 0.00, 1.44, 'dibs', 'Does it have a CHAIR on it?'),
    ('g1', 'ep01_t', 'g1', 13.40, 0.00, 1.52, 'gary', 'Yeah.'),
    ('t2', 'ep01_t', 't2', 15.00, 0.00, 1.88, 'terry', 'Ope. Sorry.'),
    ('deb3', 'ep01_t', 'deb3', 19.60, 0.00, 3.60, 'deb', 'Agent! Ten seconds! Please do something, hon!'),
    ('d4', 'ep01_t', 'd4', 23.30, 0.00, 2.02, 'dibs', "I am. I'm SITTING on it."),
    ('d5', 'ep01_t', 'd5', 29.00, 0.00, 1.58, 'dibs', "Spot's still mine."),
    ('b1', 'ep01_t', 'b1', 30.90, 0.00, 1.49, 'brad', 'Ope! Is this spot open?'),
    ('b2', 'ep01_t', 'b2', 32.70, 0.00, 1.06, 'brad', 'Is that a chair?'),
    ('m1', 'ep01_t', 'm1', 34.40, 0.00, 1.48, 'marty', "He's from NAPERVILLE."),
]

S = 'library/sfx/'
SFX = [
    (S + 'chair_slam_snow.mp3', 0.05, 1.0),
    (S + 'fuse_hiss.mp3', 0.00, 0.50), (S + 'fuse_hiss.mp3', 2.00, 0.45),
] + [(S + 'fuse_hiss.mp3', 4.0 + 2.0 * k, 0.26) for k in range(0, 11)] + [
    (S + 'golf_cart_screech.mp3', 8.55, 0.8, 0.0, 1.3),
    (S + 'book_thud.mp3', 9.95, 0.5),
    (S + 'ui_tap_chirp.mp3', 16.30, 0.8), (S + 'ui_tap_chirp.mp3', 18.00, 0.8), (S + 'ui_tap_chirp.mp3', 20.20, 0.8),
    (S + 'brake_skid.mp3', 16.95, 0.7),
    (S + 'scanner_beep.mp3', 18.40, 0.5), (S + 'scanner_beep.mp3', 18.75, 0.4),
    (S + 'tank_reverse_beeps.mp3', 19.00, 0.8),
    (S + 'water_pour_head.mp3', 22.00, 0.4, 0.0, 1.2),
    (S + 'clock_fast_ticks.mp3', 25.30, 0.7), (S + 'clock_fast_ticks.mp3', 26.80, 0.5, 0.0, 0.5),
    (S + 'cartoon_boom_big.mp3', 27.30, 1.0),
    (S + 'wind_gust.mp3', 28.40, 0.35),
    (S + 'minivan_door_slide.mp3', 30.60, 0.7),
    (S + 'record_scratch.mp3', 31.55, 0.8),
    (S + 'cloth_flap.mp3', 31.62, 0.5), (S + 'cloth_flap.mp3', 31.99, 0.5), (S + 'cloth_flap.mp3', 32.36, 0.5),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('series/agent-dibs/music/agent_dibs_theme_15s.mp3', 14.6, 0.0, 27.3, 0.24, True),
    ('series/agent-dibs/music/agent_dibs_theme_15s.mp3', 14.6, 30.6, 37.8, 0.24, True),
    ('library/sfx/amb_winter_yard.mp3', 7.8, 0.0, 37.8, 0.30, False),
]
