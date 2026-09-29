"""S01E04 «Category 5 (Permit)» — timing for video (ep04.py) and audio (mix.py). Voice clips: voice/ep04_t."""
DUR = 41.5
FPS = 30
SLUG = 'sunny-palms-hoa'
MASTER = 0.78

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('d1', 'ep04_t', 'd1', 0.00, 0.00, 2.30, 'dale', 'Category five? Is that the GOOD one?'),
    ('b1', 'ep04_t', 'b1', 2.40, 0.00, 1.62, 'brenda', "It's the WORST one."),
    ('d2', 'ep04_t', 'd2', 4.12, 0.00, 1.75, 'dale', "So it's the BEST one!"),
    ('d0', 'ep04_t', 'd0', 5.97, 0.00, 3.63, 'dale', 'I have a cooler, a lawn chair, and zero PLANS.'),
    ('b3', 'ep04_t', 'b3', 12.70, 0.00, 4.26, 'brenda', 'Hurricane Kevin. No permit. Wind is over the LIMIT.'),
    ('d3', 'ep04_t', 'd3', 18.96, 0.00, 2.27, 'dale', 'She fined the HURRICANE.'),
    ('b4', 'ep04_t', 'b4', 21.33, 0.00, 1.44, 'brenda', 'Rules are RULES.'),
    ('d4', 'ep04_t', 'd4', 22.87, 0.00, 2.61, 'dale', 'Ha. What are you gonna do, make it PAY?'),
    ('b5', 'ep04_t', 'b5', 25.58, 0.00, 1.80, 'brenda', 'No. You WILL.'),
    ('d5', 'ep04_t', 'd5', 27.48, 0.00, 0.78, 'dale', 'WHAT?!'),
    ('b6', 'ep04_t', 'b6', 28.36, 0.00, 4.49, 'brenda', 'It landed on your lawn. Four thousand seven hundred fifty DOLLARS.'),
    ('d6', 'ep04_t', 'd6', 32.95, 0.00, 2.12, 'dale', 'I only wanted a PARTY.'),
    ('e1', 'ep04_t', 'e1', 35.17, 0.00, 5.12, 'earl', 'She fined a hurricane. Never once fined ME. Think about that.'),
]

SFX = [
    ('library/sfx/thunder_crack.mp3', 0.95, 0.6, 0.0, 1.6),
    ('library/sfx/whoosh.mp3', 2.35, 0.3, 0.0, 0.5),
    ('library/sfx/sax_sting_swell.mp3', 9.40, 0.5, 0.0, 3.0),
    ('library/sfx/debris_crash.mp3', 10.00, 0.6),
    ('library/sfx/thunder_crack.mp3', 10.25, 0.9),
    ('library/sfx/debris_crash.mp3', 10.90, 0.55),
    ('library/sfx/thunder_crack.mp3', 11.60, 0.7, 0.0, 2.0),
    ('library/sfx/debris_crash.mp3', 11.85, 0.5),
    ('library/sfx/paper_unroll.mp3', 17.10, 0.4, 0.0, 0.8),
    ('library/sfx/whoosh.mp3', 17.55, 0.5),
    ('library/sfx/record_scratch.mp3', 17.90, 0.7, 0.0, 0.9),
    ('library/sfx/shop_bell.mp3', 18.05, 0.35),
    ('library/sfx/sax_sting_swell.mp3', 25.55, 0.5, 0.0, 1.8),
    ('library/sfx/coin_clink.mp3', 27.55, 0.4, 0.0, 0.5),
    ('library/sfx/paper_crumple_slap.mp3', 30.60, 0.6),
    ('library/sfx/cash_register.mp3', 31.60, 0.8),
    ('library/sfx/sad_trombone.mp3', 32.10, 0.4, 0.0, 1.6),
    ('library/sfx/pond_bloop.mp3', 35.10, 0.5),
    ('library/sfx/paper_crumple_slap.mp3', 41.00, 0.6),
]

BEDS = [
    ('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, 41.5, 0.22, True),
    ('library/sfx/hurricane_wind_howl.mp3', 7.5, 0.0, 17.95, 0.55, True),
    ('library/sfx/rain_heavy.mp3', 6.6, 0.0, 17.95, 0.45, True),
    ('library/sfx/amb_florida_yard.mp3', 7.8, 17.95, 41.5, 0.32, False),
]
