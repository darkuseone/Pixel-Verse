"""S01E01 «Ecru Whisper» — timing for video (ep01.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep01_t)."""
DUR = 46.2
FPS = 30
SLUG = 'sunny-palms-hoa'
MASTER = 0.78

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('d1', 'ep01_t', 'd1', 0.00, 0.00, 2.77, 'dale', 'Two hundred FIFTY?! For a MAILBOX?!'),
    ('b1', 'ep01_t', 'b1', 3.95, 0.00, 2.90, 'brenda', 'Morning, Dale! Your mailbox is BONE.'),
    ('d2', 'ep01_t', 'd2', 6.95, 0.00, 1.33, 'dale', "It's BEIGE!"),
    ('b2', 'ep01_t', 'b2', 8.38, 0.00, 2.80, 'brenda', 'The approved color is Ecru Whisper.'),
    ('d3', 'ep01_t', 'd3', 11.28, 0.00, 1.59, 'dale', "That's the SAME color!"),
    ('b3', 'ep01_t', 'b3', 12.95, 0.00, 1.57, 'brenda', 'Bless your heart.'),
    ('d4', 'ep01_t', 'd4', 14.62, 0.00, 3.24, 'dale', "Relax. I'll repaint it myself. I watched a VIDEO."),
    ('e1', 'ep01_t', 'e1', 17.96, 0.00, 3.42, 'earl', "Nothing good starts with 'I watched a video.'"),
    ('d5', 'ep01_t', 'd5', 25.00, 0.00, 0.94, 'dale', 'YES!'),
    ('b5', 'ep01_t', 'b5', 26.04, 0.00, 2.95, 'brenda', 'Painting without a permit? Five hundred DOLLARS.'),
    ('d6', 'ep01_t', 'd6', 29.09, 0.00, 1.15, 'dale', 'WHAT permit?!'),
    ('b6', 'ep01_t', 'b6', 30.34, 0.00, 3.40, 'brenda', 'Form twenty-seven B. Thirty days BEFORE painting.'),
    ('d7', 'ep01_t', 'd7', 33.84, 0.00, 2.17, 'dale', 'FINE! NOT on MY property!'),
    ('d8', 'ep01_t', 'd8', 36.11, 0.00, 1.52, 'dale', 'Enjoy the FINE.'),
    ('b7', 'ep01_t', 'b7', 37.73, 0.00, 2.06, 'brenda', "That's... on MY lawn."),
    ('b8', 'ep01_t', 'b8', 39.89, 0.00, 1.85, 'brenda', 'Into the Beautification FUND!'),
    ('e2', 'ep01_t', 'e2', 41.90, 0.00, 3.50, 'earl', 'Never paid a fine. GRANDFATHERED in.'),
]

# (path, t0, gain[, clip_in, clip_out])
SFX = [
    ('library/sfx/paper_crumple_slap.mp3', 0.00, 0.9),
    ('library/sfx/golf_cart_screech.mp3', 2.80, 0.8, 0.0, 1.3),
    ('library/sfx/paper_unroll.mp3', 8.55, 0.45, 0.0, 0.9),
    ('library/sfx/whoosh.mp3', 9.80, 0.30, 0.0, 0.6),
    ('library/sfx/sax_sting_swell.mp3', 15.00, 0.40),
    ('library/sfx/pond_bloop.mp3', 17.90, 0.55),
    ('library/sfx/spray_can_shake.mp3', 21.38, 0.75, 0.0, 0.9),
    ('library/sfx/spray_paint_hiss.mp3', 21.90, 0.65, 0.0, 1.5),
    ('library/sfx/pond_bloop.mp3', 22.55, 0.45),
    ('library/sfx/coin_clink.mp3', 23.50, 0.30, 0.0, 0.5),
    ('library/sfx/stamp.mp3', 24.62, 1.0),
    ('library/sfx/coin_clink.mp3', 25.10, 0.45, 0.0, 0.6),
    ('library/sfx/record_scratch.mp3', 25.97, 0.8),
    ('library/sfx/sad_trombone.mp3', 28.95, 0.40, 0.0, 1.6),
    ('library/sfx/paper_unroll.mp3', 30.30, 0.4, 0.0, 0.8),
    ('library/sfx/sax_sting_swell.mp3', 33.30, 0.50, 0.0, 1.9),
    ('library/sfx/mailbox_rip.mp3', 34.70, 0.90),
    ('library/sfx/flipflop_stomp.mp3', 35.05, 0.55, 0.0, 1.2),
    ('library/sfx/fist_slam_counter.mp3', 36.00, 0.70),
    ('library/sfx/sax_sting_swell.mp3', 37.00, 0.45, 0.0, 2.2),
    ('library/sfx/stamp.mp3', 40.60, 0.90),
    ('library/sfx/cash_register.mp3', 40.95, 0.80),
    ('library/sfx/coin_clink.mp3', 41.35, 0.40, 0.0, 0.6),
    ('library/sfx/pond_bloop.mp3', 41.82, 0.40),
    ('library/sfx/paper_crumple_slap.mp3', 45.55, 0.6),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, 46.2, 0.24, True),
    ('library/sfx/amb_florida_yard.mp3', 7.8, 0.0, 46.2, 0.32, False),
]
