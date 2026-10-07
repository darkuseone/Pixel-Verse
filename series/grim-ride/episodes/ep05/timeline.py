"""S01E05 «Best Yard» — timing for video (ep05.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep05_t)."""
DUR = 30.4
FPS = 30
SLUG = 'grim-ride'
MASTER = 0.74

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('g1', 'ep05_t', 'g1', 0.00, 0.00, 1.99, 'grim', "Don't. MOVE."),
    ('t1', 'ep05_t', 't1', 2.10, 0.00, 2.66, 'todd', 'Best Yard judging! Ooh, a REAPER!'),
    ('m1', 'ep05_t', 'm1', 4.85, 0.00, 2.43, 'mom', 'Ugh. TACKY.'),
    ('g2', 'ep05_t', 'g2', 7.35, 0.00, 1.65, 'grim', 'I am DEATH.'),
    ('t2', 'ep05_t', 't2', 9.08, 0.00, 2.27, 'todd', 'Seven out of ten. Needs FOG.'),
    ('e1', 'ep05_t', 'e1', 11.45, 0.00, 1.28, 'edgar', 'Method ACTING.'),
    ('e2', 'ep05_t', 'e2', 14.45, 0.00, 0.97, 'edgar', 'FINALLY.'),
    ('g3', 'ep05_t', 'g3', 15.50, 0.00, 1.91, 'grim', "Harold. It's TIME."),
    ('t3', 'ep05_t', 't3', 17.60, 0.00, 2.74, 'todd', "It MOVES! It's ANIMATRONIC!"),
    ('t4', 'ep05_t', 't4', 20.45, 0.00, 1.85, 'todd', 'Harold wins BEST YARD!'),
    ('h1', 'ep05_t', 'h1', 22.40, 0.00, 1.83, 'harold', 'Wanna buy him? Forty BUCKS.'),
    ('t5', 'ep05_t', 't5', 24.30, 0.00, 0.94, 'todd', 'SOLD!'),
    ('g4', 'ep05_t', 'g4', 26.90, 0.00, 1.31, 'grim', 'HELP.'),
    ('e3', 'ep05_t', 'e3', 28.30, 0.00, 1.25, 'edgar', 'Kinda CHIC.'),
]

CUTS = [0.0, 2.05, 4.80, 7.30, 9.05, 11.40, 12.75, 14.40, 15.45, 17.50, 20.40, 22.35, 24.25, 25.28, 26.85, 28.25, 29.55, DUR]
TWIST = 17.50                                   # 17.50 / 30.4 = 58 %

S = 'library/sfx/'
G = 'series/grim-ride/sfx/'
SFX = [
    (S + 'needle_prick.mp3', 0.30, 0.6), (S + 'needle_prick.mp3', 1.10, 0.6),
    (S + 'pencil_scribble.mp3', 2.30, 0.5),
    (S + 'pencil_scribble.mp3', 9.80, 0.6),
    (S + 'stamp.mp3', 10.90, 0.5),
    (G + 'raven_caw.mp3', 11.40, 0.2),
    (S + 'many_doors_open.mp3', 12.75, 0.4),
    (S + 'heartbeat_slow.mp3', 12.90, 0.55),
    (S + 'slowmo_whoosh.mp3', 15.45, 0.5),
    (S + 'record_scratch.mp3', 17.48, 0.6),
    (S + 'crowd_gasp.mp3', 17.55, 0.5),
    (S + 'camera_flash.mp3', 17.70, 0.6), (S + 'camera_flash.mp3', 18.30, 0.5), (S + 'camera_flash.mp3', 19.10, 0.5),
    (S + 'brass_fanfare_short.mp3', 20.40, 0.45),
    (S + 'crowd_cheer_short.mp3', 20.55, 0.45),
    (S + 'cash_register.mp3', 24.30, 0.6),
    (S + 'tape_measure.mp3', 25.30, 0.6),
    (S + 'rocking_creak.mp3', 25.60, 0.5),
    (S + 'sad_trombone.mp3', 27.20, 0.3),
    (S + 'needle_prick.mp3', 29.80, 0.6),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    (S + 'amb_night_crickets.mp3', 6.9, 0.0, DUR, 0.42, False),
    (S + 'amb_bbq_chatter.mp3', 6.9, 2.0, 25.3, 0.16, True),
    ('series/grim-ride/music/grim_theme_15s.mp3', 14.6, 0.0, 12.7, 0.26, True),
    ('series/grim-ride/music/grim_theme_15s.mp3', 14.6, 20.4, DUR, 0.26, True),
]

VFX = {}
VGAIN = {'grim': 1.6, 'edgar': 1.6, 'todd': 1.5, 'harold': 1.6, 'mom': 1.5}
