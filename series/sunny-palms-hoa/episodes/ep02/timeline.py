"""S01E02 «Emotional Support Flamingo» — timing for video (ep02.py) and audio (mix.py). Voice clips: voice/ep02_t (+ two reused from ep01_t)."""
DUR = 39.4
FPS = 30
SLUG = 'sunny-palms-hoa'
MASTER = 0.78

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('d1', 'ep02_t', 'd1', 0.00, 0.00, 2.85, 'dale', "This is Kevin. He's my emotional support FLAMINGO."),
    ('b1', 'ep02_t', 'b1', 2.95, 0.00, 1.78, 'brenda', 'Kevin is PLASTIC.'),
    ('d2', 'ep02_t', 'd2', 4.83, 0.00, 3.16, 'dale', 'Emotionally? So am I. I have PAPERS.'),
    ('b2', 'ep02_t', 'b2', 8.09, 0.00, 3.68, 'brenda', "This says, 'Novelty.'"),
    ('d3', 'ep02_t', 'd3', 11.87, 0.00, 1.93, 'dale', 'Novelty is a LEGAL term.'),
    ('b3', 'ep02_t', 'b3', 13.90, 0.00, 2.64, 'brenda', "Federal law. It's VALID."),
    ('d4y', 'ep01_t', 'd5', 16.64, 0.00, 0.94, 'dale', 'YES!'),
    ('b4', 'ep02_t', 'b4', 17.68, 0.00, 3.66, 'brenda', "Kevin is pink. Approved pink is 'Coral Whisper.'"),
    ('b5', 'ep02_t', 'b5', 21.44, 0.00, 4.36, 'brenda', 'Wonderful! Registration is three hundred dollars. Per YEAR.'),
    ('d4', 'ep02_t', 'd4', 25.90, 0.00, 1.12, 'dale', 'PER YEAR?!'),
    ('b3y', 'ep01_t', 'b3', 27.12, 0.00, 1.57, 'brenda', 'Bless your heart.'),
    ('b6', 'ep02_t', 'b6', 28.79, 0.00, 3.97, 'brenda', 'The whole street is registered. Ninety-four FLAMINGOS.'),
    ('d5', 'ep02_t', 'd5', 32.86, 0.00, 1.99, 'dale', "I'm sorry, Kevin. FLY."),
    ('e1', 'ep02_t', 'e1', 36.70, 0.00, 1.67, 'earl', 'I feel SUPPORTED.'),
]

SFX = [
    ('library/sfx/rubber_duck.mp3', 0.05, 0.6),
    ('library/sfx/rubber_duck.mp3', 1.90, 0.45),
    ('library/sfx/whoosh.mp3', 2.90, 0.3, 0.0, 0.5),
    ('library/sfx/paper_unroll.mp3', 9.20, 0.4, 0.0, 0.8),
    ('library/sfx/record_scratch.mp3', 9.95, 0.6, 0.0, 0.7),
    ('library/sfx/shop_bell.mp3', 15.90, 0.5),
    ('library/sfx/coin_clink.mp3', 16.70, 0.45, 0.0, 0.6),
    ('library/sfx/sax_sting_swell.mp3', 17.00, 0.45, 0.0, 2.6),
    ('library/sfx/paper_unroll.mp3', 18.60, 0.3, 0.0, 0.6),
    ('library/sfx/cash_register.mp3', 25.30, 0.7),
    ('library/sfx/sad_trombone.mp3', 25.90, 0.4, 0.0, 1.6),
    ('library/sfx/rubber_duck.mp3', 28.85, 0.45), ('library/sfx/rubber_duck.mp3', 29.15, 0.40),
    ('library/sfx/rubber_duck.mp3', 29.50, 0.50), ('library/sfx/rubber_duck.mp3', 29.75, 0.35),
    ('library/sfx/rubber_duck.mp3', 30.10, 0.45), ('library/sfx/rubber_duck.mp3', 30.45, 0.40),
    ('library/sfx/cash_register.mp3', 31.55, 0.8),
    ('library/sfx/coin_clink.mp3', 32.10, 0.4, 0.0, 0.6),
    ('library/sfx/whoosh.mp3', 34.60, 0.6),
    ('library/sfx/bath_splash.mp3', 35.30, 0.8),
    ('library/sfx/plastic_crunch.mp3', 35.85, 0.8),
    ('library/sfx/plastic_crunch.mp3', 36.25, 0.6, 0.0, 0.7),
    ('library/sfx/gator_gulp.mp3', 36.45, 0.9),
    ('library/sfx/paper_crumple_slap.mp3', 38.80, 0.6),
]

BEDS = [
    ('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, 39.4, 0.24, True),
    ('library/sfx/amb_florida_yard.mp3', 7.8, 0.0, 39.4, 0.32, False),
]
