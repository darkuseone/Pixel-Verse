"""S01E02 «Free Trial» — timing for video (ep02.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep02_t)."""
DUR = 38.0
FPS = 30
SLUG = 'agent-dibs'
MASTER = 0.80
DING_T = 11.80                               # the trial ends

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('d1', 'ep02_t', 'd1', 0.00, 0.00, 1.39, 'dibs', "I'm invisible."),
    ('deb1', 'ep02_t', 'deb1', 2.60, 0.00, 1.60, 'deb', "How long's the trial, hon?"),
    ('d2', 'ep02_t', 'd2', 4.30, 0.00, 1.31, 'dibs', 'Seven days.'),
    ('deb2', 'ep02_t', 'deb2', 6.00, 0.00, 1.60, 'deb', 'And which day is it?'),
    ('d3', 'ep02_t', 'd3', 7.80, 0.00, 0.97, 'dibs', 'Seven.'),
    ('g1', 'ep02_t', 'g1', 12.10, 0.00, 1.91, 'gary', "Ope. Sir? You've got a pop-up."),
    ('g2', 'ep02_t', 'g2', 14.60, 0.00, 0.74, 'gary', 'Top right.'),
    ('d4', 'ep02_t', 'd4', 15.50, 0.00, 1.23, 'dibs', "That's a BIRD."),
    ('g3', 'ep02_t', 'g3', 20.40, 0.00, 2.54, 'gary', "That's actually a good mattress."),
    ('t1', 'ep02_t', 't1', 23.00, 0.00, 2.12, 'terry', "My back's been killing me."),
    ('d5', 'ep02_t', 'd5', 25.20, 0.00, 1.86, 'dibs', 'A hundred-night trial.'),
    ('t2', 'ep02_t', 't2', 28.60, 0.00, 0.92, 'terry', 'Guys?'),
    ('t3', 'ep02_t', 't3', 30.00, 0.00, 1.96, 'terry', 'You know what? Take the disk.'),
    ('d6', 'ep02_t', 'd6', 32.20, 0.00, 1.08, 'dibs', "That's it?"),
    ('t4', 'ep02_t', 't4', 33.50, 0.00, 1.76, 'terry', "I've got a mattress to look at."),
    ('g4', 'ep02_t', 'g4', 35.40, 0.00, 1.49, 'gary', 'Can you send me the link?'),
]

S = 'library/sfx/'
SFX = [
    (S + 'cloak_shimmer.mp3', 0.00, 0.80),
    (S + 'big_bite_chew.mp3', 0.10, 0.40), (S + 'big_bite_chew.mp3', 9.05, 0.30), (S + 'big_bite_chew.mp3', 12.00, 0.35),
    (S + 'tiptoe_marble.mp3', 1.60, 0.60, 0.0, 2.7),
] + [(S + 'counter_blip.mp3', DING_T - n, 0.32 if n > 3 else 0.5) for n in range(9, 0, -1)] + [
    (S + 'tiptoe_marble.mp3', 8.2, 0.35, 0.0, 0.7),
    (S + 'app_notify_ping.mp3', DING_T, 0.95),
    (S + 'cloak_shimmer.mp3', DING_T + 0.02, 0.6, 0.0, 0.5),
    (S + 'whoosh.mp3', 14.50, 0.40, 0.0, 0.6), (S + 'whoosh.mp3', 14.90, 0.35, 0.0, 0.5),
    (S + 'ui_tap_chirp.mp3', 17.20, 0.45), (S + 'ui_tap_chirp.mp3', 17.65, 0.45), (S + 'slowmo_whoosh.mp3', 18.15, 0.40, 0.0, 1.0),
    (S + 'ad_jingle.mp3', 19.20, 0.75),
    (S + 'ui_tap_chirp.mp3', 20.40, 0.30), (S + 'ui_tap_chirp.mp3', 21.40, 0.30), (S + 'ui_tap_chirp.mp3', 22.40, 0.30),
    (S + 'cat_meow.mp3', 23.15, 0.55),
    (S + 'ui_tap_chirp.mp3', 23.40, 0.30), (S + 'ui_tap_chirp.mp3', 24.40, 0.30), (S + 'ui_tap_chirp.mp3', 25.40, 0.30),
    (S + 'app_notify_ping.mp3', 27.10, 0.85),
    (S + 'slowmo_whoosh.mp3', 27.90, 0.65, 0.0, 1.7), (S + 'cloth_flap.mp3', 28.30, 0.40), (S + 'cloth_flap.mp3', 28.90, 0.40),
    (S + 'paper_crumple_slap.mp3', 28.55, 0.45),
    (S + 'ui_tap_chirp.mp3', 29.62, 0.9), (S + 'tv_static_blip.mp3', 29.66, 0.55, 0.0, 0.5),
    (S + 'whoosh.mp3', 31.35, 0.45, 0.0, 0.8),
    (S + 'book_thud.mp3', 32.20, 0.55),
    (S + 'receipt_printer.mp3', 34.45, 0.7), (S + 'stamp.mp3', 35.02, 0.8),
    (S + 'cloak_shimmer.mp3', 37.00, 0.75), (S + 'app_notify_ping.mp3', 37.45, 0.6),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('series/agent-dibs/music/agent_dibs_theme_15s.mp3', 14.6, 0.0, 19.2, 0.22, True),
    ('series/agent-dibs/music/agent_dibs_theme_15s.mp3', 14.6, 29.7, 38.0, 0.22, True),
    ('library/sfx/amb_office_night.mp3', 7.8, 0.0, 38.0, 0.30, False),
]
