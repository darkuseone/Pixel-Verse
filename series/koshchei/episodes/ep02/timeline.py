"""S01E02 «ЗВОНЯТ ИЗ БАНКА?!» — timing for video (ep02.py) and audio (mix.py). Voice: voice/ep02_t, common_t. Series-own sounds only.
Горыныч: one designed voice, three heads = three pitches (gorynych / gorynych3 via VFX)."""
DUR = 30.4
FPS = 30
SLUG = 'koshchei'
MASTER = 0.66

VOICE = [
    ('r1', 'ep02_t', 'r1', 0.00, 0.00, 4.10, 'gorynych', 'Служба безопасности банка «Сберёг». Ваша СМЕРТЬ — в опасности!'),
    ('k1', 'ep02_t', 'k1', 4.18, 0.00, 2.17, 'koshchei', 'Откуда вы знаете, где ОНА?!'),
    ('k2', 'ep02_t', 'k2', 6.45, 0.00, 4.08, 'koshchei', 'Я — Кощей Бессмертный! Меня не ОБМАНЕШЬ!'),
    ('r4', 'ep02_t', 'r4', 10.60, 0.00, 2.38, 'gorynych', 'Тогда продиктуйте код из СМС.'),
    ('k3', 'ep02_t', 'k3', 13.05, 0.00, 1.65, 'koshchei', 'Семь. ТРИ.'),
    ('r5', 'ep02_t', 'r5', 14.78, 0.00, 1.70, 'gorynych', 'Иглу положите на БАЛКОН.'),
    ('r6', 'ep02_t', 'r6', 16.75, 0.00, 1.96, 'gorynych_live', 'О, сосед! ЗДОРОВО!'),
    ('k4', 'ep02_t', 'k4', 18.80, 0.00, 1.38, 'koshchei', 'ГОРЫНЫЧ?!'),
    ('r7', 'ep02_t', 'r7', 20.30, 0.00, 2.25, 'gorynych_live', 'Это не мы. Это — АЛГОРИТМ.'),
    ('y1', 'ep02_t', 'y1', 22.65, 0.00, 3.21, 'yaga', 'Горыныч! Мне тоже звонили — ВНУКОМ!'),
    ('r8', 'ep02_t', 'r8', 25.95, 0.00, 2.27, 'gorynych3', 'Бабуль, это тоже Я.'),
    ('z1', 'common_t', 'zhut2', 28.35, 0.00, 1.10, 'kuzmich', 'ЖУТЬ.'),
]

#       hook  where  proud  code   needle FACADE algo   yaga   head3  zhut   loop
CUTS = [0.0, 4.15, 6.40, 10.55, 14.72, 16.60, 20.20, 22.55, 25.85, 28.25, 29.55, DUR]
NAMES = ['hook', 'where', 'proud', 'code', 'needle', 'facade', 'algo', 'yaga', 'head3', 'zhut', 'loop']
TWIST = CUTS[5]

X = 'series/koshchei/sfx/'
SFX = [
    (X + 'phone_ring_old.mp3', 0.00, 0.80),
    (X + 'cabinet_crystal.mp3', 4.60, 0.55),
    (X + 'vent_rattle.mp3', 8.20, 0.45),
    (X + 'laptop_typing.mp3', 11.00, 0.35),
    (X + 'vent_rattle.mp3', 13.10, 0.35),
    (X + 'cabinet_crystal.mp3', 14.80, 0.75),
    (X + 'egg_crack_shell.mp3', 15.60, 0.70),
    (X + 'whoosh_fast.mp3', 16.50, 0.70),
    (X + 'twist_choir_hit.mp3', 16.60, 0.80),
    (X + 'fishing_reel.mp3', 17.20, 0.65),
    (X + 'laptop_typing.mp3', 20.40, 0.40),
    (X + 'phone_click.mp3', 27.90, 0.60),
    (X + 'breaker_clunk.mp3', 28.25, 0.50),
    (X + 'phone_ring_old.mp3', 29.55, 0.75),
]

BEDS = [
    ('series/koshchei/sfx/stairwell_amb_loop.mp3', 8.0, 0.0, DUR, 0.30, True),
    ('series/koshchei/music/koshchei_theme_15s.mp3', 15.0, 4.15, 16.50, 0.20, True),
    ('series/koshchei/music/koshchei_theme_15s.mp3', 15.0, 17.20, DUR, 0.18, True),
]

PHONE = 'highpass=f=320,lowpass=f=3400,acompressor=threshold=0.2:ratio=4,volume=1.25'
VFX = {'gorynych': PHONE, 'gorynych3': 'asetrate=44100*1.22,aresample=44100,atempo=0.82', 'kuzmich': 'aecho=0.6:0.4:40:0.15'}
VGAIN = {'koshchei': 1.5, 'gorynych': 1.5, 'gorynych_live': 1.5, 'gorynych3': 1.5, 'yaga': 1.5, 'kuzmich': 1.8}
