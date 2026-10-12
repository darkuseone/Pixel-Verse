"""S01E01 «9 000 ЗА ТЕПЛО?!» — timing for video (ep01.py) and audio (mix.py). Voice clips are the tightened takes (voice/ep01_t)."""
DUR = 34.2
FPS = 30
SLUG = 'prokhor'
MASTER = 0.92

VOICE = [
    ('p1', 'ep01_t', 'p1', 0.00, 0.00, 1.91, 'prokhor', 'Девять тыщ за ТЕПЛО?!'),
    ('p2', 'ep01_t', 'p2', 2.05, 0.00, 2.98, 'prokhor', 'Вот. Пять секунд тепла — БЕСПЛАТНО.'),
    ('p3', 'ep01_t', 'p3', 5.12, 0.00, 2.90, 'prokhor', 'Городские! Лайфхак номер ОДИН!'),
    ('p4', 'ep01_t', 'p4', 8.12, 0.00, 3.74, 'prokhor', 'Медведь. Тридцать восемь градусов. Без СЧЁТЧИКА!'),
    ('p5', 'ep01_t', 'p5', 12.02, 0.00, 2.64, 'prokhor', 'Спит до апреля. Тариф — НОЛЬ.'),
    ('p6', 'ep01_t', 'p6', 15.40, 0.00, 1.99, 'prokhor', 'Городские — УЧИТЕСЬ!'),
    ('b1', 'ep01_t', 'b1', 17.60, 0.00, 3.00, 'bear', 'Отопление. Девять ТЫСЯЧ.'),
    ('p7', 'ep01_t', 'p7', 20.72, 0.00, 1.04, 'prokhor', 'Ты ж СПИШЬ!'),
    ('b2', 'ep01_t', 'b2', 21.88, 0.00, 1.72, 'bear', 'Я на УДАЛЁНКЕ.'),
    ('p8', 'ep01_t', 'p8', 23.72, 0.00, 1.67, 'prokhor', 'А если не ЗАПЛАЧУ?'),
    ('b3', 'ep01_t', 'b3', 25.50, 0.00, 2.04, 'bear', 'ОТКЛЮЧУ.'),
    ('p9', 'ep01_t', 'p9', 28.72, 0.00, 3.74, 'prokhor', 'Го-городские... НЕ учитесь.'),
    ('b4', 'ep01_t', 'b4', 32.56, 0.00, 1.46, 'bear', 'Плюс ПЕНИ.'),
]

#        hook stove warm  blog  trek   entr   snug   meter  bliss  EYE    bearcu reveal remote plead  yawn   fly    ice    ice2   button
CUTS = [0.0, 2.00, 3.45, 5.08, 8.08, 10.10, 12.00, 14.66, 15.40, 17.50, 19.20, 20.66, 21.84, 23.66, 25.44, 27.40, 28.68, 30.60, 32.50, DUR]
NAMES = ['hook', 'stove', 'warm', 'blog', 'trek', 'entrance', 'snuggle', 'meter', 'bliss', 'eye', 'bearcu', 'reveal', 'remote', 'plead',
         'yawn', 'fly', 'ice', 'ice2', 'button']
TWIST = CUTS[9]

S = 'library/sfx/'
SFX = [
    (S + 'paper_crumple_slap.mp3', 0.00, 0.45),
    (S + 'wind_gust.mp3', 0.05, 0.35),
    (S + 'paper_crumple_slap.mp3', 2.30, 0.40),
    (S + 'whoosh.mp3', 2.75, 0.45, 0.0, 1.0),
    (S + 'fuse_crackle.mp3', 2.80, 0.40, 0.0, 1.4),
    (S + 'ui_tap_chirp.mp3', 5.10, 0.45),
    (S + 'pushpin_pop.mp3', 6.20, 0.45),
    (S + 'snow_steps.mp3', 8.10, 0.55),
    (S + 'snore.mp3', 10.20, 0.40),
    (S + 'snow_crawl.mp3', 12.00, 0.40),
    (S + 'snore.mp3', 12.40, 0.55),
    (S + 'pushpin_pop.mp3', 13.00, 0.40),
    (S + 'clock_fast_ticks.mp3', 14.66, 0.60, 0.0, 0.8),
    (S + 'counter_blip.mp3', 15.20, 0.40),
    (S + 'snore.mp3', 15.60, 0.30),
    (S + 'gum_pop.mp3', 17.47, 0.75),
    (S + 'record_scratch.mp3', 17.50, 0.50),
    (S + 'scanner_beep.mp3', 19.80, 0.60),
    (S + 'flashlight_click.mp3', 20.66, 0.70),
    (S + 'cash_register.mp3', 23.40, 0.30),
    (S + 'whoosh.mp3', 27.20, 0.60, 0.0, 1.2),
    (S + 'wind_gust.mp3', 27.40, 0.35),
    (S + 'chair_slam_snow.mp3', 28.05, 0.70),
    (S + 'ice_clink.mp3', 28.30, 0.75),
    (S + 'teeth_chatter.mp3', 28.75, 0.45),
    (S + 'teeth_chatter.mp3', 30.40, 0.45),
    (S + 'stamp.mp3', 32.95, 0.55),
    (S + 'pushpin_pop.mp3', 33.20, 0.55),
]

BEDS = [
    ('library/sfx/amb_winter_yard.mp3', 8.0, 0.0, DUR, 0.22, False),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 5.08, 17.50, 0.22, True),
    ('series/prokhor/music/prokhor_theme_15s.mp3', 15.0, 20.66, DUR, 0.20, True),
]

VFX = {'bear': 'aecho=0.6:0.4:35:0.12'}
VGAIN = {'prokhor': 1.5, 'bear': 1.7}
