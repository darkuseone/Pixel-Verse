"""S01E06 «Naperville» — timing for video (ep06.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep06_t)."""
DUR = 42.0
FPS = 30
SLUG = 'agent-dibs'
MASTER = 0.69
TURN_T = 30.00                                   # the ladies roll Brad into a snow burrito

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('d1', 'ep06_t', 'd1', 0.10, 0.00, 1.65, 'dibs', 'CUL-DE-SAC PLAYERS?!'),
    ('b1', 'ep06_t', 'b1', 1.85, 0.00, 1.36, 'brad', 'Ope.'),
    ('m1', 'ep06_t', 'm1', 3.30, 0.00, 4.41, 'marty', 'Quick recap. Every villain this season? Community theater.'),
    ('d2', 'ep06_t', 'd2', 7.85, 0.00, 2.12, 'dibs', 'You paid them four hundred a WEEK!'),
    ('b2', 'ep06_t', 'b2', 10.05, 0.00, 2.01, 'brad', 'Plus snacks.'),
    ('b3', 'ep06_t', 'b3', 12.20, 0.00, 2.46, 'brad', "I'd love to discuss, but I have a thing."),
    ('b4', 'ep06_t', 'b4', 17.30, 0.00, 1.49, 'brad', 'Where do I PARK?!'),
    ('d3', 'ep06_t', 'd3', 19.05, 0.00, 1.85, 'dibs', "Spot's open right there, Brad."),
    ('d4', 'ep06_t', 'd4', 23.25, 0.00, 2.22, 'dibs', "That's Mrs. Wozniak's chair."),
    ('b5', 'ep06_t', 'b5', 26.45, 0.00, 2.22, 'brad', 'Ope. Ope. OPE.'),
    ('mw1', 'ep06_t', 'mw1', 28.75, 0.00, 1.23, 'mrs_w', 'Naperville.'),
    ('ch1', 'ep06_t', 'ch1', 31.95, 0.00, 2.32, 'chief', "Agent Dibs. You're permanent."),
    ('d5', 'ep06_t', 'd5', 34.85, 0.00, 1.75, 'dibs', 'Dibs.'),
    ('cab1', 'ep06_t', 'cab1', 36.75, 0.00, 2.40, 'cabbie', 'Yo. This spot open?'),
    ('m2', 'ep06_t', 'm2', 39.95, 0.00, 1.38, 'marty', "He's from New York."),
]

S = 'library/sfx/'
SFX = [
    (S + 'ribbon_snap.mp3', 0.02, 0.5), (S + 'paper_crumple_slap.mp3', 0.30, 0.9),
    (S + 'record_scratch.mp3', 1.80, 0.5),
    (S + 'camera_flash.mp3', 4.58, 0.6), (S + 'stamp.mp3', 4.78, 0.8),
    (S + 'camera_flash.mp3', 5.23, 0.6), (S + 'stamp.mp3', 5.43, 0.8),
    (S + 'camera_flash.mp3', 5.88, 0.6), (S + 'stamp.mp3', 6.08, 0.8),
    (S + 'pushpin_pop.mp3', 6.52, 0.8),
    (S + 'paper_crumple_slap.mp3', 7.90, 0.6),
    (S + 'big_bite_chew.mp3', 11.05, 0.6),
    (S + 'minivan_door_slide.mp3', 14.70, 0.7), (S + 'boots_stomp.mp3', 15.00, 0.5),
    (S + 'whoosh.mp3', 16.50, 0.7), (S + 'whoosh.mp3', 18.45, 0.7),
    (S + 'blinker_clicks.mp3', 17.30, 0.5),
    (S + 'brake_skid.mp3', 20.80, 0.6), (S + 'slowmo_whoosh.mp3', 21.00, 0.6), (S + 'chair_scoot.mp3', 21.75, 0.7),
    (S + 'record_scratch.mp3', 22.38, 0.7), (S + 'curtain_reveal.mp3', 22.45, 0.8),
    (S + 'many_doors_open.mp3', 25.50, 0.8), (S + 'blues_bass_sting.mp3', 25.55, 0.8),
    (S + 'snow_crawl.mp3', TURN_T, 0.8), (S + 'whoosh.mp3', TURN_T + 0.05, 0.6),
    (S + 'crowd_cheer_short.mp3', 32.10, 0.35), (S + 'stamp.mp3', 33.85, 0.9),
    (S + 'steam_hiss_soft.mp3', 34.40, 0.5),
    (S + 'taxi_honk.mp3', 36.72, 0.6),
    (S + 'curtain_reveal.mp3', 39.20, 0.8),
    (S + 'title_stinger.mp3', 41.35, 0.6),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('series/agent-dibs/music/agent_dibs_theme_15s.mp3', 14.6, 0.0, 42.0, 0.24, True),
    ('library/sfx/amb_winter_yard.mp3', 7.8, 0.0, 42.0, 0.26, False),
]
