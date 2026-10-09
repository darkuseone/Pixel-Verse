"""S01E03 «Good Boy» — timing for video (ep03.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep03_t).
Darlene's «Mornin', Travis.» is cut after «Mornin'»: the microchip BEEP covers the name (running gag: his name is never heard)."""
DUR = 30.4
FPS = 30
SLUG = 'florida-man'
MASTER = 0.72

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('f1', 'ep03_t', 'f1', 0.00, 0.00, 2.64, 'fm', 'TWO GRAND?! For an ICE PACK?!'),
    ('t1', 'ep03_t', 't1', 2.70, 0.00, 1.46, 'tanner', "It's ORGANIC ice!"),
    ('f2', 'ep03_t', 'f2', 4.22, 0.00, 1.20, 'fm', "It's WATER."),
    ('t2', 'ep03_t', 't2', 5.48, 0.00, 1.33, 'tanner', 'Out-of-NETWORK water!'),
    ('f3', 'ep03_t', 'f3', 6.88, 0.00, 2.19, 'fm', 'Mort. Hold my sub.'),
    ('m1', 'ep03_t', 'm1', 9.14, 0.00, 2.35, 'mort', 'Holding fee. Eighty BUCKS.'),
    ('t3', 'ep03_t', 't3', 13.72, 0.00, 1.80, 'tanner', "Who's a GOOD boy?"),
    ('f4', 'ep03_t', 'f4', 15.58, 0.00, 1.12, 'fm', 'Me.'),
    ('t4', 'ep03_t', 't4', 16.80, 0.00, 1.44, 'tanner', 'And a little MICROCHIP!'),
    ('d1', 'ep03_t', 'd1', 18.42, 0.00, 1.04, 'darlene', 'Gotcha.'),
    ('d2', 'ep03_t', 'd2', 22.60, 0.00, 0.58, 'darlene', "Mornin'—"),
    ('d3', 'ep03_t', 'd3', 27.42, 0.00, 2.43, 'darlene', "Good boy. Scan's two GRAND."),
]

# shot boundaries (ep03.py)
CUTS = [0.0, 2.66, 4.18, 5.44, 6.85, 9.10, 11.5, 12.6, 13.6, 15.5, 16.75, 18.3, 19.5, 20.5, 21.5, 22.5, 23.5, 25.5, 27.3, DUR]
TWIST = 16.75                                   # 16.75 / 30.4 = 55 %
BEEPS = [17.95, 19.85, 20.85, 21.85, 23.18, 25.75]

S = 'library/sfx/'
SFX = [
    (S + 'receipt_printer.mp3', 0.00, 0.7),
    (S + 'record_scratch.mp3', 0.02, 0.0),
    (S + 'cash_register.mp3', 0.15, 0.35),
    (S + 'ui_tap_chirp.mp3', 2.72, 0.4),
    (S + 'water_drip_single.mp3', 4.25, 0.8),
    (S + 'counter_blip.mp3', 5.50, 0.4),
    (S + 'gator_gulp.mp3', 8.70, 0.8),
    (S + 'pencil_scribble.mp3', 9.40, 0.5),
    (S + 'paper_crumple_slap.mp3', 10.90, 0.5),
    (S + 'whoosh.mp3', 11.45, 0.3, 0.0, 0.8),
    (S + 'shop_bell.mp3', 11.55, 0.45),
    (S + 'pencil_scribble.mp3', 12.70, 0.6),
    (S + 'cat_meow.mp3', 13.62, 0.25),
    (S + 'plastic_crunch.mp3', 16.75, 0.8),
    (S + 'record_scratch.mp3', 16.76, 0.5),
    (S + 'needle_prick.mp3', 17.85, 0.8),
    (S + 'crowd_gasp.mp3', 18.30, 0.25),
    (S + 'airboat_roar.mp3', 19.50, 0.35),
    (S + 'brake_skid.mp3', 20.80, 0.35),
    (S + 'siren_whoop.mp3', 21.55, 0.35),
    (S + 'camera_flash.mp3', 23.50, 0.8),
    (S + 'news_breaking_sting.mp3', 23.52, 0.55),
    (S + 'hole_punch.mp3', 24.70, 0.9),
    (S + 'receipt_printer.mp3', 25.95, 0.6),
    (S + 'pushpin_pop.mp3', 28.6, 0.4),
] + [(S + 'scanner_beep.mp3', b, 0.8) for b in BEEPS]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    (S + 'amb_office_night.mp3', 7.9, 0.0, 11.5, 0.5, True),
    (S + 'amb_florida_yard_soft.mp3', 7.9, 11.5, DUR, 0.3, True),
    ('series/florida-man/music/fm_theme_15s.mp3', 14.9, 0.0, 16.75, 0.24, True),
    ('series/florida-man/music/fm_theme_15s.mp3', 14.9, 18.3, DUR, 0.24, True),
]

VFX = {}
VGAIN = {'fm': 1.9, 'tanner': 1.45, 'mort': 1.7, 'darlene': 1.65}
