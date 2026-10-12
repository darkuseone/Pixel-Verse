"""S01E01 v2 «9 000 ЗА ТЕПЛО?!» — timing for video (ep01.py) and audio (mix.py). Voice: tightened takes voice/ep01b_t (new rough voice).
Sound design: ONLY this series' own sounds (series/prokhor/sfx, owner rule 12.10.2026) + the balalaika theme."""
DUR = 32.0
FPS = 30
SLUG = 'prokhor'
MASTER = 0.90

VOICE = [
    ('p1', 'ep01b_t', 'p1', 0.00, 0.00, 2.23, 'prokhor', 'Девять тыщ за ОТОПЛЕНИЕ?!'),
    ('p2', 'ep01b_t', 'p2', 2.32, 0.00, 3.84, 'prokhor', 'А я в тайгу переехал. Тут тепло — БЕСПЛАТНО!'),
    ('p3', 'ep01b_t', 'p3', 6.35, 0.00, 3.72, 'prokhor', 'Лайфхак: зимой медведь — это БАТАРЕЯ.'),
    ('p3b', 'ep01b_t', 'p3b', 10.30, 0.00, 1.26, 'prokhor', 'Тихо. СПИТ.'),
    ('p4', 'ep01b_t', 'p4', 13.10, 0.00, 2.91, 'prokhor', 'Тридцать восемь градусов. Без СЧЁТЧИКА.'),
    ('p5', 'ep01b_t', 'p5', 16.08, 0.00, 1.84, 'prokhor', 'Городские, УЧИТЕСЬ.'),
    ('b1', 'ep01b_t', 'b1', 18.15, 0.00, 3.00, 'bear', 'Отопление. Девять ТЫСЯЧ.'),
    ('p6', 'ep01b_t', 'p6', 21.30, 0.00, 0.95, 'prokhor', 'НЕТУ...'),
    ('b2', 'ep01b_t', 'b2', 22.35, 0.00, 1.49, 'bear', 'ОТКЛЮЧАЮ.'),
    ('p7', 'ep01b_t', 'p7', 25.95, 0.00, 4.15, 'prokhor', 'Го-городские... НЕ учитесь.'),
    ('b3', 'ep01b_t', 'b3', 30.30, 0.00, 1.36, 'bear', 'Плюс ПЕНИ.'),
]

#       selfie walk   crawl  den    EYE    term   plead  shove  fly    ice
CUTS = [0.0, 6.20, 10.20, 12.95, 17.95, 19.30, 21.30, 22.30, 23.90, 25.90, DUR]
NAMES = ['selfie', 'walk', 'crawl', 'den', 'eye', 'terminal', 'plead', 'shove', 'fly', 'ice']
TWIST = CUTS[4]

X = 'series/prokhor/sfx/'
SFX = [
    (X + 'bill_rustle.mp3', 0.00, 0.80),
    (X + 'breath_frost.mp3', 0.55, 0.55),
    (X + 'crow_caw.mp3', 1.40, 0.28),
    (X + 'bill_rustle.mp3', 1.10, 0.45),
    (X + 'breath_frost.mp3', 4.40, 0.40),
    (X + 'phone_rec_start.mp3', 6.22, 0.55),
    (X + 'tripod_snow.mp3', 6.30, 0.55),
    (X + 'snow_steps_valenki.mp3', 6.40, 0.75),
    (X + 'snow_steps_valenki.mp3', 8.70, 0.70),
    (X + 'crow_caw.mp3', 9.40, 0.22),
    (X + 'bear_snore.mp3', 10.25, 0.35),
    (X + 'snow_crawl_in.mp3', 11.50, 0.85),
    (X + 'bear_snore.mp3', 12.95, 0.75),
    (X + 'snow_crawl_in.mp3', 13.00, 0.45, 0.0, 0.8),
    (X + 'cozy_creak.mp3', 13.70, 0.70),
    (X + 'hat_off_sigh.mp3', 15.95, 0.35, 0.6, 1.48),
    (X + 'bear_snore.mp3', 16.10, 0.45, 0.0, 1.8),
    (X + 'snot_bubble_pop.mp3', 17.85, 1.00),
    (X + 'twist_hit.mp3', 17.95, 0.75),
    (X + 'bear_wake_growl.mp3', 18.00, 0.45),
    (X + 'pos_terminal.mp3', 19.55, 0.80),
    (X + 'bear_wake_growl.mp3', 22.25, 0.55),
    (X + 'paw_shove_whoosh.mp3', 23.25, 1.00),
    (X + 'snowdrift_landing.mp3', 24.62, 1.00),
    (X + 'freeze_crackle.mp3', 24.85, 0.95),
    (X + 'ice_crack_small.mp3', 25.75, 0.60),
    (X + 'teeth_chatter_cold.mp3', 26.00, 0.55),
    (X + 'teeth_chatter_cold.mp3', 28.10, 0.45),
    (X + 'paper_slap_ice.mp3', 29.88, 1.00),
    (X + 'ice_crack_small.mp3', 31.00, 0.45),
]

BEDS = [
    ('series/prokhor/sfx/taiga_wind_loop.mp3', 8.0, 0.0, 12.95, 0.40, True),
    ('series/prokhor/sfx/den_ambience_loop.mp3', 8.0, 12.95, 23.90, 0.55, True),
    ('series/prokhor/sfx/taiga_wind_loop.mp3', 8.0, 23.90, DUR, 0.45, True),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 2.25, 17.90, 0.20, True),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 23.90, DUR, 0.18, True),
]

VFX = {'bear': 'aecho=0.6:0.4:35:0.12'}
VGAIN = {'prokhor': 1.55, 'bear': 1.75}
