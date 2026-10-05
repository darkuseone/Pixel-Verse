"""S01E05 «Don't Let Go» — timing for video (ep05.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep05_t)."""
DUR = 39.8
FPS = 30
SLUG = 'agent-dibs'
MASTER = 0.62
SPLAT_T = 21.95                                  # Dibs hits the Bean
TURN_T = 28.05                                   # the wind snatches the trophy

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('deb1', 'ep05_t', 'deb1', 0.10, 0.00, 3.40, 'deb', "Whatever you do, hon, don't let go of that briefcase."),
    ('d1', 'ep05_t', 'd1', 3.55, 0.00, 2.06, 'dibs', "I'M NOT LETTING GO!"),
    ('deb2', 'ep05_t', 'deb2', 5.70, 0.00, 3.37, 'deb', "Deliver it first, and you're Agent of the Year."),
    ('d2', 'ep05_t', 'd2', 9.10, 0.00, 1.59, 'dibs', 'What do I WIN?'),
    ('deb3', 'ep05_t', 'deb3', 10.75, 0.00, 3.53, 'deb', 'A reserved parking spot. Heated.'),
    ('d3', 'ep05_t', 'd3', 14.35, 0.00, 2.14, 'dibs', 'Heated. DIBS!'),
    ('b1', 'ep05_t', 'b1', 18.20, 0.00, 1.49, 'brad', 'Ope! Hi, Dibs!'),
    ('ch1', 'ep05_t', 'ch1', 23.05, 0.00, 2.56, 'chief', 'Agent Dibs. First to arrive.'),
    ('d4', 'ep05_t', 'd4', 25.70, 0.00, 2.40, 'dibs', 'Twenty-two years on probation.'),
    ('b2', 'ep05_t', 'b2', 29.55, 0.00, 1.46, 'brad', 'Ope! Got it!'),
    ('d5', 'ep05_t', 'd5', 31.05, 0.00, 1.67, 'dibs', 'I called DIBS!'),
    ('ch2', 'ep05_t', 'ch2', 32.75, 0.00, 1.23, 'chief', 'Not in writing.'),
    ('deb4', 'ep05_t', 'deb4', 35.75, 0.00, 2.51, 'deb', 'Proud of you, hon. Truly.'),
]

S = 'library/sfx/'
SFX = [
    (S + 'hurricane_wind_howl.mp3', 0.00, 0.55), (S + 'hurricane_wind_howl.mp3', 7.80, 0.40), (S + 'hurricane_wind_howl.mp3', 15.40, 0.45),
    (S + 'cloth_flap.mp3', 0.30, 0.6), (S + 'cloth_flap.mp3', 0.75, 0.5), (S + 'cloth_flap.mp3', 3.60, 0.5),
    (S + 'whoosh.mp3', 1.75, 0.8), (S + 'whoosh.mp3', 16.30, 0.8),
    (S + 'wind_gust.mp3', 16.35, 0.7), (S + 'pigeons_flap_burst.mp3', 16.90, 0.7),
    (S + 'blinker_clicks.mp3', 18.10, 0.6),
    (S + 'ui_tap_chirp.mp3', 19.75, 0.6), (S + 'ui_tap_chirp.mp3', 20.15, 0.6), (S + 'ui_tap_chirp.mp3', 20.55, 0.6),
    (S + 'bean_splat_slide.mp3', SPLAT_T, 1.0),
    (S + 'crowd_cheer_short.mp3', 23.20, 0.55), (S + 'camera_flash.mp3', 23.30, 0.5), (S + 'camera_flash.mp3', 24.10, 0.4),
    (S + 'wind_gust.mp3', TURN_T, 0.9), (S + 'slowmo_whoosh.mp3', TURN_T + 0.10, 0.7),
    (S + 'record_scratch.mp3', 29.40, 0.6),
    (S + 'crowd_cheer_short.mp3', 33.95, 0.7),
    (S + 'cloth_flap.mp3', 35.15, 0.4), (S + 'bucket_clang.mp3', 35.53, 0.75),
    (S + 'amb_night_crickets.mp3', 36.95, 0.9, 0.4, 1.3),
    (S + 'wind_gust.mp3', 38.25, 0.8), (S + 'whoosh.mp3', 38.90, 0.6),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('series/agent-dibs/music/agent_dibs_theme_15s.mp3', 14.6, 0.0, 39.8, 0.24, True),
    ('library/sfx/hurricane_wind_howl.mp3', 7.8, 0.0, 22.0, 0.18, False),
    ('library/sfx/amb_winter_yard.mp3', 7.8, 22.0, 39.8, 0.26, False),
]
