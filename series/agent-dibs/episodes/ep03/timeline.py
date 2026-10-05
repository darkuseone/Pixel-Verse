"""S01E03 «Pothole» — timing for video (ep03.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep03_t)."""
DUR = 41.3
FPS = 30
SLUG = 'agent-dibs'
MASTER = 0.74
HOLD_T0, HOLD_T1 = 25.70, 28.90                  # hold music + time-lapse

# (id, voice_ep, key, t_start, clip_in, clip_out, speaker, caption)
VOICE = [
    ('d1', 'ep03_t', 'd1', 0.00, 0.00, 2.40, 'dibs', "HOLD ON, DEB! I'M IN A PURSUIT!"),
    ('deb1', 'ep03_t', 'deb1', 2.52, 0.00, 1.59, 'deb', 'Seatbelt, hon.'),
    ('d2', 'ep03_t', 'd2', 6.15, 0.00, 2.98, 'dibs', 'Frank. Linda. Big Steve.'),
    ('t1', 'ep03_t', 't1', 10.25, 0.00, 0.96, 'terry', 'Ope?'),
    ('g1', 'ep03_t', 'g1', 11.32, 0.00, 0.96, 'gary', "We're okay!"),
    ('op1', 'ep03_t', 'op1', 13.40, 0.00, 2.85, 'operator', 'Three-one-one. Please state your pothole.'),
    ('d3', 'ep03_t', 'd3', 16.35, 0.00, 1.82, 'dibs', "There's a car in Big Steve."),
    ('op2', 'ep03_t', 'op2', 18.28, 0.00, 2.64, 'operator', "We can't fill a pothole with a car in it."),
    ('d4', 'ep03_t', 'd4', 21.02, 0.00, 1.83, 'dibs', 'So remove the car!'),
    ('op3', 'ep03_t', 'op3', 22.95, 0.00, 2.70, 'operator', "That's Towing. This is Streets. Please hold."),
    ('op4', 'ep03_t', 'op4', 28.95, 0.00, 2.44, 'operator', 'Your request is closed. Duplicate.'),
    ('d5', 'ep03_t', 'd5', 31.49, 0.00, 1.44, 'dibs', 'DUPLICATE OF WHAT?!'),
    ('op5', 'ep03_t', 'op5', 33.03, 0.00, 2.75, 'operator', 'Four-five-one-two-three-three-oh. Pothole.'),
    ('d6', 'ep03_t', 'd6', 37.40, 0.00, 1.10, 'dibs', "That's it?!"),
    ('w1', 'ep03_t', 'w1', 38.60, 0.00, 1.81, 'chief', "It's marked."),
]
PHONE = 'highpass=f=320,lowpass=f=3200,acompressor=threshold=0.2:ratio=4,volume=1.3'
VFX = {'operator': PHONE}                        # the 311 operator is heard through a phone
VGAIN = {'operator': 1.2}

S = 'library/sfx/'
SFX = [
    (S + 'old_sedan_rattle.mp3', 0.00, 0.70), (S + 'old_sedan_rattle.mp3', 3.00, 0.50),
    (S + 'chase_brass.mp3', 0.05, 0.55),
    (S + 'seatbelt_click.mp3', 4.16, 0.95),
    (S + 'old_sedan_rattle.mp3', 4.20, 0.45), (S + 'old_sedan_rattle.mp3', 7.20, 0.40),
    (S + 'blinker_clicks.mp3', 4.20, 0.55), (S + 'blinker_clicks.mp3', 5.70, 0.55), (S + 'blinker_clicks.mp3', 7.20, 0.45),
    (S + 'blinker_clicks.mp3', 8.70, 0.45),
    (S + 'ui_tap_chirp.mp3', 6.25, 0.45), (S + 'ui_tap_chirp.mp3', 7.20, 0.45), (S + 'ui_tap_chirp.mp3', 8.15, 0.55),
    (S + 'brake_skid.mp3', 9.10, 0.7),
    (S + 'car_pothole_drop.mp3', 9.35, 1.0),
    (S + 'pond_bloop.mp3', 10.20, 0.8), (S + 'pond_bloop.mp3', 10.75, 0.6),
    (S + 'flip_phone.mp3', 12.45, 0.85),
    (S + 'ui_tap_chirp.mp3', 12.72, 0.55), (S + 'ui_tap_chirp.mp3', 12.92, 0.55), (S + 'ui_tap_chirp.mp3', 13.12, 0.55),
    (S + 'vhs_rewind.mp3', HOLD_T0, 0.45, 0.0, 1.6),
    (S + 'clock_fast_ticks.mp3', HOLD_T0, 0.55), (S + 'clock_fast_ticks.mp3', HOLD_T0 + 1.5, 0.55),
    (S + 'record_scratch.mp3', 28.90, 0.85),
    (S + 'brake_skid.mp3', 36.00, 0.5), (S + 'book_thud.mp3', 36.45, 0.55),
    (S + 'spray_paint_soft.mp3', 36.70, 0.6, 0.0, 1.2), (S + 'pencil_scribble.mp3', 37.00, 0.5, 0.0, 0.8),
    (S + 'blues_bass_sting.mp3', 40.45, 0.7),
]

# (path, loop_len, t0, t1, gain, duck_under_speech)
BEDS = [
    ('series/agent-dibs/music/agent_dibs_theme_15s.mp3', 14.6, 0.0, 12.4, 0.22, True),
    ('library/sfx/hold_music_elise.mp3', 14.4, 25.7, 28.9, 0.55, False),
    ('series/agent-dibs/music/agent_dibs_theme_15s.mp3', 14.6, 35.8, 41.3, 0.22, True),
    ('library/sfx/amb_flat_winter.mp3', 7.8, 0.0, 41.3, 0.26, False),
]
