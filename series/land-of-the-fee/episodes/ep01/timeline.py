"""S01E01 «REPRESENTATIVE!» — timing for video (ep01.py) and audio (mix.py). Voice: tightened takes voice/ep01_t.
Sound design: ONLY this series' own sounds (series/land-of-the-fee/sfx, owner rule 12.10.2026) + the code-synth kazoo march."""
DUR = 31.0
FPS = 30
SLUG = 'land-of-the-fee'
MASTER = 0.80
LUFS = -14.0                     # owner's test rule 25.10.2026: -14 LUFS / -1 dBTP

VOICE = [
    ('d1', 'ep01_t', 'd1', 0.00, 0.00, 1.33, 'duke', 'REPRESENTATIVE!!'),
    ('f1', 'ep01_t', 'f1', 1.45, 0.00, 2.41, 'feebee', 'Sounds like you said — UPGRADE! Done!'),
    ('d2', 'ep01_t', 'd2', 3.98, 0.00, 2.55, 'duke', "I'm a BALD EAGLE. I'm on the DOLLAR!"),
    ('s1', 'ep01_t', 's1', 6.65, 0.00, 1.66, 'sal', 'Not on YOURS.'),
    ('d3', 'ep01_t', 'd3', 8.70, 0.00, 2.37, 'duke', "Fine. I'm talking to a HUMAN."),
    ('d4', 'ep01_t', 'd4', 11.20, 0.00, 1.30, 'duke', 'HUMAN! NOW!'),
    ('f2', 'ep01_t', 'f2', 12.62, 0.00, 2.00, 'feebee', 'Sounds like you said — HUMMUS!'),
    ('o1', 'ep01_t', 'o1', 14.80, 0.00, 2.78, 'doris', "Hi, hon! I'm a REAL human!"),
    ('o2', 'ep01_t', 'o2', 17.70, 0.00, 2.34, 'doris', "That's nineteen ninety-nine a MINUTE."),
    ('d5', 'ep01_t', 'd5', 20.16, 0.00, 0.87, 'duke', 'For WHAT?!'),
    ('o3', 'ep01_t', 'o3', 21.15, 0.00, 2.18, 'doris', "Eye contact's EXTRA, hon."),
    ('d6', 'ep01_t', 'd6', 23.45, 0.00, 1.95, 'duke', "Forget it! I'll take the ROBOT!"),
    ('f3', 'ep01_t', 'f3', 25.52, 0.00, 1.98, 'feebee', 'Sounds like you said — HUMAN!'),
    ('s2', 'ep01_t', 's2', 29.40, 0.00, 1.32, 'sal', 'Majestic.'),
]

#       hook  phone proud sal   fly   kiosk  door   twist  what   run    kiosk2 button
CUTS = [0.0, 1.40, 3.92, 6.60, 8.62, 11.15, 14.70, 17.65, 20.10, 23.40, 25.45, 27.55, DUR]
NAMES = ['hook', 'phone', 'proud', 'sal', 'fly', 'kiosk', 'door', 'twist', 'what', 'run', 'kiosk2', 'button']
TWIST = 17.70
CHIRP = (28.05, 29.25)           # Duke's real (wimpy) bald-eagle call

X = 'series/land-of-the-fee/sfx/'
E = X + 'es/'                    # sounds rendered from the earshot bank (engine/earshot_sfx.py), audited, code-made
# sound design v2 (30.10.2026, earshot pass): hits with a sub layer on the reveals, swishes/whooshes placed so the peak lands just
# after the cut, the music never stops (ducked under speech, stepped down 0.4 s before the door and the twist), effects panned to
# where they are on screen, Fee-Bee's chimes from the mallet family. Earlier mix: sound/timeline_v1.py.
SFX = [
    (X + 'phone_grip.mp3', 0.00, 1.2),
    (X + 'table_slam.mp3', 0.04, 3.0),
    (E + 'hit_punch.wav', 0.04, 0.55),
    (E + 'hit_sub.wav', 0.04, 0.50),
    (X + 'feather_burst.mp3', 0.10, 6.0, None, None, -0.3),
    (E + 'swish_flick.wav', 1.29, 0.32, None, None, 0.3),
    (E + 'chime_up4.wav', 1.42, 0.24),
    (E + 'pop_step.wav', 3.22, 0.30),
    (X + 'ka_ching.mp3', 3.24, 0.45),
    (E + 'swell_short.wav', 3.69, 0.30),
    (X + 'feather_burst.mp3', 3.95, 4.0, None, None, -0.2),
    (X + 'pigeon_coo.mp3', 6.45, 0.35, None, None, 0.5),
    (X + 'fry_munch.mp3', 6.55, 6.0, None, None, 0.5),
    (X + 'fry_munch.mp3', 8.05, 5.0, None, None, 0.5),
    (E + 'knock_wood.wav', 8.15, 0.30, None, None, -0.5),
    (X + 'wallet_moth.mp3', 8.15, 9.0, None, None, -0.4),
    (E + 'whoosh_cape.wav', 8.06, 0.45),
    (X + 'wing_flap.mp3', 8.62, 0.9, None, None, -0.5),
    (X + 'whoosh_fly.mp3', 9.20, 0.6),
    (X + 'wing_flap.mp3', 10.10, 0.7, None, None, 0.4),
    (E + 'whoosh_whip.wav', 11.04, 0.35),
    (X + 'glass_doors.mp3', 11.10, 1.2),
    (X + 'talons_tile.mp3', 11.18, 1.6, None, None, 0.4),
    (E + 'celesta_bb.wav', 12.55, 0.22, None, None, -0.4),
    (X + 'hummus_plop.mp3', 14.30, 1.3, None, None, -0.4),
    (E + 'drip_bloop.wav', 14.32, 0.22, None, None, -0.4),
    (E + 'popin_round.wav', 14.40, 0.22),
    (E + 'impact_short.wav', 14.70, 0.55, None, None, 0.4),
    (E + 'hit_sub.wav', 14.70, 0.45),
    (X + 'door_burst.mp3', 14.70, 1.0, None, None, 0.4),
    (X + 'holy_choir.mp3', 14.74, 0.6, None, None, 0.3),
    (E + 'riser_snatch.wav', 17.31, 0.35),
    (E + 'sub_drop_twist.wav', 17.70, 0.70),
    (X + 'twist_sting.mp3', 17.66, 0.60),
    (X + 'ka_ching.mp3', 17.72, 0.60),
    (E + 'pop_soft.wav', 17.72, 0.22),
    (X + 'meter_tick.mp3', 18.00, 1.6, None, None, 0.2),
    (E + 'hit_punch.wav', 20.16, 0.30, None, None, -0.3),
    (E + 'shutter_snap.wav', 22.93, 0.30, None, None, 0.4),
    (X + 'meter_tick.mp3', 22.70, 1.4, None, None, 0.4),
    (X + 'ka_ching.mp3', 22.95, 0.60, None, None, 0.4),
    (E + 'pop_step.wav', 22.95, 0.20, None, None, 0.3),
    (E + 'whoosh_sleeve.wav', 23.28, 0.40, None, None, 0.3),
    (X + 'talons_tile.mp3', 23.42, 1.8, None, None, 0.2),
    (E + 'pop_soft.wav', 23.50, 0.22),
    (X + 'talons_tile.mp3', 24.30, 1.6, None, None, -0.2),
    (E + 'swish_flick.wav', 25.33, 0.25, None, None, -0.3),
    (E + 'celesta_bb.wav', 25.47, 0.20, None, None, -0.3),
    (X + 'ka_ching.mp3', 27.40, 0.70, None, None, -0.3),
    (E + 'hit_sub.wav', 27.40, 0.40),
    (E + 'pop_wide.wav', 27.42, 0.25),
    (X + 'meter_tick.mp3', 27.50, 1.4),
    (X + 'big_inhale.mp3', 27.58, 0.9),
    (X + 'eagle_chirp.mp3', CHIRP[0], 1.15),
    (E + 'pop_soft.wav', 28.95, 0.20),
    (X + 'pigeon_coo.mp3', 29.30, 0.25, None, None, -0.2),
    (E + 'pop_wide.wav', 30.00, 0.30),               # end card «SUBSCRIBE!» pops in
    (E + 'glock_d6.wav', 30.02, 0.22),
]

M = 'series/land-of-the-fee/music/freedom_kazoo_v2_16s.mp3'
HAAS = 'adelay=0|14'                                  # 14 ms on the right channel: width for the room tone and the music
STOP = "volume='if(between(t,14.32,14.72)+between(t,17.30,17.70),0.30,1)':eval=frame"   # step down before the hits, back on them
BEDS = [
    (X + 'apt_amb_loop.mp3', 8.0, 0.0, 8.62, 0.8, True, HAAS),
    (X + 'mall_amb_loop.mp3', 8.0, 8.62, 11.15, 0.9, True, HAAS),
    (X + 'store_amb_loop.mp3', 8.0, 11.15, DUR, 0.8, True, HAAS),
    (M, 16.0, 0.30, DUR, 0.50, 0.55, 'equalizer=f=2000:t=q:w=1.4:g=-5,bass=g=4:f=70,' + STOP + ',' + HAAS),   # ducked 5 dB under speech
]

VOICE_LUFS = -14.5               # every line measured and brought to one loudness (o2 was 6 dB under the rest)
VFX = {'feebee': 'highpass=f=150,lowpass=f=8000,aecho=1.0:0.85:14:0.10'}   # the old aecho=0.5 in-gain cut her by 6 dB
VGAIN = {'duke': 1.0, 'sal': 1.0, 'feebee': 1.0, 'doris': 1.0}
MASTER_EQ = 'equalizer=f=50:t=q:w=1.0:g=4.5,equalizer=f=90:t=q:w=1.0:g=2,equalizer=f=2400:t=q:w=1.2:g=-1.5'   # earshot: thin bottom, honky 1-4 kHz
