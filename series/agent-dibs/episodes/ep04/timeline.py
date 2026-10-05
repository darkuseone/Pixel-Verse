"""S01E04 «Hostage» — timing for video (ep04.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep04_t)."""
DUR = 39.8
FPS = 30
SLUG = 'agent-dibs'
MASTER = 0.80
TURN_T = 24.30                                   # the squeeze
BITE_T = 33.95

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('d1', 'ep04_t', 'd1', 0.00, 0.00, 1.70, 'dibs', 'Put the ketchup down, son.'),
    ('t1', 'ep04_t', 't1', 1.85, 0.00, 1.50, 'terry', "Stay back! I'll do it!"),
    ('deb1', 'ep04_t', 'deb1', 5.05, 0.00, 2.23, 'deb', 'Agent, is that ketchup?'),
    ('d2', 'ep04_t', 'd2', 7.40, 0.00, 1.26, 'dibs', 'Think about your mother.'),
    ('t2', 'ep04_t', 't2', 8.80, 0.00, 2.20, 'terry', 'She puts ketchup on EVERYTHING!'),
    ('mw1', 'ep04_t', 'mw1', 11.12, 0.00, 1.39, 'mrs_w', 'Naperville.'),
    ('d3', 'ep04_t', 'd3', 12.65, 0.00, 3.17, 'dibs', "Seven toppings, son. Don't ruin the garden."),
    ('t3', 'ep04_t', 't3', 15.95, 0.00, 2.07, 'terry', "It's just a HOT DOG!"),
    ('t4', 'ep04_t', 't4', 25.60, 0.00, 2.17, 'terry', 'I just wanted ketchup for my fries.'),
    ('mw2', 'ep04_t', 'mw2', 27.90, 0.00, 1.86, 'mrs_w', 'Fries are fine.'),
    ('t5', 'ep04_t', 't5', 29.90, 0.00, 2.07, 'terry', 'Then why did everybody FREAK OUT?'),
    ('d4', 'ep04_t', 'd4', 32.10, 0.00, 1.73, 'dibs', 'Tension.'),
    ('d5', 'ep04_t', 'd5', 35.00, 0.00, 1.02, 'dibs', 'Evidence.'),
    ('m1', 'ep04_t', 'm1', 36.15, 0.00, 1.39, 'marty', 'I had dibs.'),
    ('d6', 'ep04_t', 'd6', 37.70, 0.00, 1.23, 'dibs', "Where's your chair?"),
]

S = 'library/sfx/'
SFX = [
    (S + 'heartbeat_slow.mp3', 19.80, 0.7), (S + 'heartbeat_slow.mp3', 21.70, 0.8), (S + 'heartbeat_slow.mp3', 23.50, 0.9),
    (S + 'water_drip_single.mp3', 20.00, 0.6), (S + 'water_drip_single.mp3', 22.40, 0.7),
    (S + 'crowd_gasp.mp3', 10.95, 0.8),
    (S + 'record_scratch.mp3', 18.00, 0.85),
    (S + 'wind_gust.mp3', 18.00, 0.45),
    (S + 'slowmo_whoosh.mp3', TURN_T, 0.6, 0.0, 1.5),
    (S + 'ketchup_squirt.mp3', TURN_T + 0.15, 1.0),
    (S + 'crowd_sigh.mp3', 27.85, 0.8),
    (S + 'big_bite_chew.mp3', BITE_T, 0.9),
    (S + 'plastic_crunch.mp3', 16.55, 0.4),
    (S + 'tap_squeak.mp3', 18.4, 0.5),
    (S + 'stamp.mp3', 14.2, 0.4),
    (S + 'knitting.mp3', 5.0, 0.5, 0.0, 1.2),
    (S + 'blues_bass_sting.mp3', 36.1, 0.45),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('library/sfx/neon_buzz_tense.mp3', 4.0, 0.0, 24.3, 0.34, False),
    ('series/agent-dibs/music/agent_dibs_theme_15s.mp3', 14.6, 0.0, 19.6, 0.18, True),
    ('series/agent-dibs/music/agent_dibs_theme_15s.mp3', 14.6, 25.5, 39.8, 0.22, True),
    ('library/sfx/amb_flat_winter.mp3', 7.8, 0.0, 39.8, 0.36, False),
]
