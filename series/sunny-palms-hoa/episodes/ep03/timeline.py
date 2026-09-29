"""S01E03 «Suspicious Man (Walking)» — timing for video (ep03.py) and audio (mix.py). Voice clips: voice/ep03_t (+ 'Bless your heart.' from ep01_t)."""
DUR = 43.2
FPS = 30
SLUG = 'sunny-palms-hoa'
MASTER = 0.78

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('d1', 'ep03_t', 'd1', 0.00, 0.00, 2.90, 'dale', "'Suspicious man. Walking.' Who is WALKING?!"),
    ('b1', 'ep03_t', 'b1', 3.00, 0.00, 2.56, 'brenda', "You are, Dale. It's on my RING."),
    ('d2', 'ep03_t', 'd2', 5.66, 0.00, 2.04, 'dale', 'I was taking out the TRASH!'),
    ('b2', 'ep03_t', 'b2', 7.80, 0.00, 4.05, 'brenda', 'Trash is Tuesday. Today is Wednesday. SUSPICIOUS.'),
    ('d3', 'ep03_t', 'd3', 15.30, 0.00, 3.76, 'dale', "Fine. I have a Ring too. It's mostly pointed at my TRUCK."),
    ('d4', 'ep03_t', 'd4', 23.00, 0.00, 3.21, 'dale', 'She moved my mailbox. SIX inches.'),
    ('b3', 'ep03_t', 'b3', 26.31, 0.00, 2.90, 'brenda', 'Routine compliance MEASUREMENT.'),
    ('d5', 'ep03_t', 'd5', 29.31, 0.00, 1.28, 'dale', "It's on CAMERA!"),
    ('b4', 'ep03_t', 'b4', 30.69, 0.00, 3.71, 'brenda', 'Only approved doorbells are admissible. Yours is BLACK.'),
    ('d6', 'ep03_t', 'd6', 34.50, 0.00, 2.53, 'dale', 'So the doorbell has to be BEIGE?!'),
    ('b5', 'ep03_t', 'b5', 37.13, 0.00, 1.46, 'brenda', 'Ecru WHISPER.'),
    ('b3y', 'ep01_t', 'b3', 38.69, 0.00, 1.57, 'brenda', 'Bless your heart.'),
    ('e1', 'ep03_t', 'e1', 40.40, 0.00, 1.70, 'earl', "Haven't seen any CAT."),
]

SFX = [
    ('library/sfx/app_notify_ping.mp3', 0.00, 0.6),
    ('library/sfx/whoosh.mp3', 2.95, 0.3, 0.0, 0.5),
    ('library/sfx/fist_slam_counter.mp3', 5.80, 0.5),
    ('library/sfx/app_notify_ping.mp3', 12.25, 0.6), ('library/sfx/app_notify_ping.mp3', 12.85, 0.6),
    ('library/sfx/app_notify_ping.mp3', 13.45, 0.6), ('library/sfx/app_notify_ping.mp3', 14.05, 0.6),
    ('library/sfx/sax_sting_swell.mp3', 17.60, 0.42, 0.0, 1.6),
    ('library/sfx/camera_glitch.mp3', 19.10, 0.7),
    ('library/sfx/doorbell_chime.mp3', 19.35, 0.55),
    ('library/sfx/shovel_dig_dirt.mp3', 20.25, 0.8),
    ('library/sfx/mailbox_rip.mp3', 21.05, 0.45, 0.0, 1.0),
    ('library/sfx/tape_measure.mp3', 21.75, 0.8),
    ('library/sfx/camera_glitch.mp3', 22.90, 0.6),
    ('library/sfx/coin_clink.mp3', 29.35, 0.4, 0.0, 0.6),
    ('library/sfx/record_scratch.mp3', 30.62, 0.6, 0.0, 0.8),
    ('library/sfx/sad_trombone.mp3', 32.40, 0.4, 0.0, 1.6),
    ('library/sfx/fist_slam_counter.mp3', 34.55, 0.5),
    ('library/sfx/shop_bell.mp3', 37.25, 0.4),
    ('library/sfx/pond_bloop.mp3', 40.35, 0.5),
    ('library/sfx/paper_crumple_slap.mp3', 42.55, 0.6),
]

BEDS = [
    ('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, 19.1, 0.24, True),
    ('series/valera-i-kot/music/operation_sneaky_15s.mp3', 14.6, 19.1, 23.0, 0.26, True),
    ('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 22.9, 43.2, 0.24, True),
    ('library/sfx/amb_florida_yard.mp3', 7.8, 0.0, 19.1, 0.32, False),
    ('library/sfx/amb_night_crickets.mp3', 6.6, 19.1, 23.0, 0.45, False),
    ('library/sfx/amb_florida_yard.mp3', 7.8, 22.9, 43.2, 0.32, False),
]
