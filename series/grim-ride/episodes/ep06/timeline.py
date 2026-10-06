"""S01E06 «Fall Back» — timing for video (ep06.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep06_t)."""
DUR = 32.4
FPS = 30
SLUG = 'grim-ride'
MASTER = 0.74

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('g1', 'ep06_t', 'g1', 0.00, 0.00, 1.75, 'grim', 'One minute, HAROLD.'),
    ('d0', 'ep06_t', 'd0', 1.85, 0.00, 2.66, 'dashley', 'Reminder! Deactivation in ONE minute!'),
    ('k1', 'ep06_t', 'k1', 4.60, 0.00, 2.69, 'kayden', 'Relax, pal. We GOT you.'),
    ('t1', 'ep06_t', 't1', 7.35, 0.00, 1.83, 'todd', "Go, buddy! FOG'S ON!"),
    ('e0', 'ep06_t', 'e0', 9.25, 0.00, 1.20, 'edgar', 'Tick TOCK.'),
    ('h1', 'ep06_t', 'h1', 10.55, 0.00, 2.04, 'harold', "Alright, Bones. I'm READY."),
    ('g2', 'ep06_t', 'g2', 12.70, 0.00, 1.54, 'grim', 'I am DEATH.'),
    ('h2', 'ep06_t', 'h2', 14.32, 0.00, 2.35, 'harold', 'I know, kid. I KNOW.'),
    ('h3', 'ep06_t', 'h3', 18.10, 0.00, 2.53, 'harold', 'Extra hour, kid. Wanna RIDE?'),
    ('g3', 'ep06_t', 'g3', 20.80, 0.00, 2.59, 'grim', 'Woo-HOO!'),
    ('d1', 'ep06_t', 'd1', 23.50, 0.00, 2.51, 'dashley', 'Pickup rescheduled. Next HALLOWEEN!'),
    ('g4', 'ep06_t', 'g4', 26.10, 0.00, 2.80, 'grim', 'Five. STARS.'),
    ('e1', 'ep06_t', 'e1', 29.00, 0.00, 1.12, 'edgar', 'NEVERMORE.'),
]

CUTS = [0.0, 1.85, 4.55, 7.30, 9.20, 10.50, 12.65, 14.30, 16.70, 17.60, 18.60, 20.70, 23.45, 26.05, 28.95, 30.15, 31.60, DUR]
TWIST = 17.60                                   # 17.60 / 32.4 = 54 %

S = 'library/sfx/'
G = 'series/grim-ride/sfx/'
SFX = [
    (S + 'clock_fast_ticks.mp3', 0.00, 0.5),
    (S + 'app_notify_ping.mp3', 1.85, 0.5),
    (G + 'etrike_zoom.mp3', 4.55, 0.6),
    (S + 'rope_yank.mp3', 4.70, 0.6),
    (S + 'steam_hiss_soft.mp3', 7.30, 0.35),
    (S + 'clock_fast_ticks.mp3', 9.20, 0.5),
    (S + 'wind_gust.mp3', 10.50, 0.4),
    (S + 'heartbeat_slow.mp3', 14.30, 0.45),
    (S + 'clock_midnight_chime.mp3', 16.70, 0.55),
    (S + 'record_scratch.mp3', 17.58, 0.6),
    (S + 'vhs_rewind.mp3', 17.62, 0.5),
    (S + 'choir_hallelujah_short.mp3', 17.90, 0.4),
    (G + 'etrike_rev.mp3', 20.70, 0.7),
    (S + 'fireworks_distant.mp3', 20.90, 0.6),
    (S + 'crowd_cheer_short.mp3', 21.40, 0.35),
    (S + 'app_notify_ping.mp3', 23.45, 0.5),
    (S + 'brass_fanfare_short.mp3', 24.40, 0.35),
    (G + 'raven_caw.mp3', 28.95, 0.3),
    (S + 'thunder_crack.mp3', 31.60, 0.45),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    (S + 'amb_night_crickets.mp3', 6.9, 0.0, DUR, 0.40, False),
    (S + 'monowheel_whine.mp3', 3.8, 4.5, 10.5, 0.18, True),
    ('series/grim-ride/music/grim_theme_15s.mp3', 14.6, 0.0, 10.5, 0.24, True),
    ('series/grim-ride/music/grim_theme_15s.mp3', 14.6, 17.6, DUR, 0.28, True),
]

VFX = {'dashley': 'highpass=f=180,lowpass=f=6500,aecho=0.6:0.4:18:0.15'}
VGAIN = {'grim': 1.6, 'edgar': 1.6, 'todd': 1.5, 'harold': 1.65, 'kayden': 1.55, 'dashley': 1.45}
