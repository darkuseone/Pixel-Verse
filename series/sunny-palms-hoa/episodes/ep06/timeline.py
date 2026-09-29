"""S01E06 «Vote Earl» (season finale) — timing for video (ep06.py) and audio (mix.py). Voice clips: voice/ep06_t (+ 'YES!' from ep01_t)."""
DUR = 49.4
FPS = 30
SLUG = 'sunny-palms-hoa'
MASTER = 0.78

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('d1', 'ep06_t', 'd1', 0.00, 0.00, 3.00, 'dale', 'Vote Dale! I promise FEWER fines!'),
    ('b1', 'ep06_t', 'b1', 3.10, 0.00, 4.26, 'brenda', 'Dale, you owe almost six thousand dollars in FINES.'),
    ('d2', 'ep06_t', 'd2', 7.46, 0.00, 3.06, 'dale', 'Exactly. Nobody knows the fines BETTER.'),
    ('b2', 'ep06_t', 'b2', 10.62, 0.00, 2.74, 'brenda', 'Any resident may run. Rules are RULES.'),
    ('d3', 'ep06_t', 'd3', 13.46, 0.00, 3.94, 'dale', 'My platform is simple. I will fine NOBODY. Except Brenda.'),
    ('e1', 'ep06_t', 'e1', 21.10, 0.00, 2.74, 'earl', "I vote DALE. He's the main character."),
    ('b3', 'ep06_t', 'b3', 23.94, 0.00, 1.88, 'brenda', "That's an ALLIGATOR."),
    ('e2', 'ep06_t', 'e2', 25.92, 0.00, 2.38, 'earl', 'Resident since nineteen eighty-SEVEN.'),
    ('b4', 'ep06_t', 'b4', 28.40, 0.00, 2.98, 'brenda', 'Two to one. Dale WINS.'),
    ('dy', 'ep01_t', 'd5', 31.48, 0.00, 0.94, 'dale', 'YES!'),
    ('d4', 'ep06_t', 'd4', 33.85, 0.00, 3.13, 'dale', 'Morning, Brenda. Your mailbox is BONE.'),
    ('b5', 'ep06_t', 'b5', 37.08, 0.00, 1.33, 'brenda', "It's BEIGE!"),
    ('d5', 'ep06_t', 'd5', 38.51, 0.00, 2.72, 'dale', 'The approved color is Ecru Whisper.'),
    ('b6', 'ep06_t', 'b6', 41.33, 0.00, 1.62, 'brenda', "That's the SAME color!"),
    ('d6', 'ep06_t', 'd6', 43.05, 0.00, 1.38, 'dale', 'Bless your HEART.'),
    ('e3', 'ep06_t', 'e3', 44.53, 0.00, 2.95, 'earl', "Well. That's FLORIDA."),
]

SFX = [
    ('library/sfx/whoosh.mp3', 3.05, 0.3, 0.0, 0.5),
    ('library/sfx/crowd_cheer_short.mp3', 17.35, 0.9),
    ('library/sfx/ballot_drop.mp3', 19.10, 0.9), ('library/sfx/ballot_drop.mp3', 19.95, 0.9),
    ('library/sfx/pond_bloop.mp3', 20.95, 0.5),
    ('library/sfx/crowd_gasp.mp3', 23.90, 0.9),
    ('library/sfx/gavel_bang.mp3', 28.35, 0.9),
    ('library/sfx/coin_clink.mp3', 31.50, 0.4, 0.0, 0.5),
    ('library/sfx/crowd_cheer_short.mp3', 31.60, 0.6),
    ('library/sfx/sax_sting_swell.mp3', 32.30, 0.5),
    ('library/sfx/stamp.mp3', 33.10, 0.8),
    ('library/sfx/paper_unroll.mp3', 36.60, 0.4, 0.0, 0.8),
    ('library/sfx/crowd_gasp.mp3', 37.10, 0.4, 0.0, 1.0),
    ('library/sfx/record_scratch.mp3', 41.30, 0.5, 0.0, 0.8),
    ('library/sfx/sax_sting_swell.mp3', 44.00, 0.5, 0.0, 2.6),
    ('library/sfx/pond_bloop.mp3', 44.45, 0.5),
    ('library/sfx/paper_crumple_slap.mp3', 47.70, 0.6),
]

BEDS = [
    ('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, 33.6, 0.22, True),
    ('series/valera-i-kot/music/operation_sneaky_15s.mp3', 14.6, 33.6, 44.4, 0.26, True),
    ('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 44.3, 49.4, 0.22, True),
    ('library/sfx/grill_sizzle.mp3', 6.5, 0.0, 19.0, 0.25, False),
    ('library/sfx/amb_bbq_chatter.mp3', 6.5, 0.0, 49.4, 0.28, False),
]
