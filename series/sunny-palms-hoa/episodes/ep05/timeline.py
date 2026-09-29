"""S01E05 «Suggested Tip» — timing for video (ep05.py) and audio (mix.py). Voice clips: voice/ep05_t."""
DUR = 40.2
FPS = 30
SLUG = 'sunny-palms-hoa'
MASTER = 0.78

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('d1', 'ep05_t', 'd1', 0.00, 0.00, 1.72, 'dale', "It's a FREE hot dog!"),
    ('t1', 'ep05_t', 't1', 1.82, 0.00, 3.97, 'tablet', 'Would you like to add a tip? Twenty. Twenty-five. Thirty PERCENT.'),
    ('b1', 'ep05_t', 'b1', 5.89, 0.00, 2.27, 'brenda', 'Service is not FREE, Dale.'),
    ('d2', 'ep05_t', 'd2', 8.26, 0.00, 3.03, 'dale', 'Twenty percent of free is ZERO. I did the math.'),
    ('t2', 'ep05_t', 't2', 11.39, 0.00, 3.66, 'tablet', 'Total: forty-seven sixty-three. Includes CONVENIENCE fee.'),
    ('d3', 'ep05_t', 'd3', 15.15, 0.00, 1.67, 'dale', "What's so CONVENIENT?!"),
    ('b2', 'ep05_t', 'b2', 16.92, 0.00, 2.64, 'brenda', 'Cash has a fifteen percent SURCHARGE.'),
    ('d4', 'ep05_t', 'd4', 19.66, 0.00, 1.99, 'dale', 'Then how do I say NO?!'),
    ('t3', 'ep05_t', 't3', 21.75, 0.00, 3.87, 'tablet', 'Are you sure? Brenda worked really HARD.'),
    ('d5', 'ep05_t', 'd5', 25.72, 0.00, 1.28, 'dale', 'YES.'),
    ('t4', 'ep05_t', 't4', 27.10, 0.00, 2.40, 'tablet', 'Great! Would you like to leave a REVIEW?'),
    ('d6', 'ep05_t', 'd6', 29.60, 0.00, 1.04, 'dale', 'NO!'),
    ('b3', 'ep05_t', 'b3', 30.74, 0.00, 2.27, 'brenda', 'Enjoy! Bun is EXTRA.'),
    ('t5', 'ep05_t', 't5', 33.11, 0.00, 4.23, 'tablet', 'Would you like to tip this VIDEO? Twenty. Twenty-five. Thirty percent.'),
    ('e1', 'ep05_t', 'e1', 37.44, 0.00, 0.91, 'earl', "DON'T."),
]

_CH = 'library/sfx/ui_tap_chirp.mp3'
SFX = [
    ('library/sfx/fist_slam_counter.mp3', 0.05, 0.6),
    (_CH, 1.85, 0.5), (_CH, 2.10, 0.4), (_CH, 2.32, 0.4), (_CH, 2.54, 0.4), (_CH, 4.75, 0.6),
    ('library/sfx/receipt_printer.mp3', 11.45, 0.45),
    (_CH, 11.64, 0.35), (_CH, 11.98, 0.35), (_CH, 12.32, 0.35), (_CH, 12.66, 0.35), (_CH, 13.00, 0.35), (_CH, 13.34, 0.35), (_CH, 13.68, 0.35), (_CH, 14.02, 0.35),
    ('library/sfx/cash_register.mp3', 14.36, 0.8),
    ('library/sfx/fist_slam_counter.mp3', 15.20, 0.5),
    (_CH, 20.20, 0.4), (_CH, 20.60, 0.4), (_CH, 21.00, 0.4),
    ('library/sfx/sad_trombone.mp3', 22.00, 0.4, 0.0, 1.6),
    (_CH, 26.70, 0.5),
    ('library/sfx/shop_bell.mp3', 27.15, 0.5),
    ('library/sfx/fist_slam_counter.mp3', 29.65, 0.7),
    ('library/sfx/coin_clink.mp3', 31.40, 0.4, 0.0, 0.5),
    ('library/sfx/record_scratch.mp3', 33.05, 0.7, 0.0, 0.9),
    (_CH, 33.85, 0.4), (_CH, 34.07, 0.4), (_CH, 34.29, 0.4), (_CH, 36.90, 0.5),
    ('library/sfx/pond_bloop.mp3', 37.40, 0.5),
    ('library/sfx/paper_crumple_slap.mp3', 39.50, 0.6),
]

BEDS = [
    ('series/sunny-palms-hoa/music/sunny_palms_theme_15s.mp3', 14.6, 0.0, 40.2, 0.22, True),
    ('library/sfx/grill_sizzle.mp3', 6.5, 0.0, 33.1, 0.30, False),
    ('library/sfx/amb_bbq_chatter.mp3', 6.5, 0.0, 40.2, 0.28, False),
]
