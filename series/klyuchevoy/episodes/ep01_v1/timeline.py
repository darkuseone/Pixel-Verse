"""S01E01 «ЗАДЕРЖИСЬ НА 5 МИНУТ!» — timing for video (ep01.py) and audio (mix.py). Voice: tightened takes voice/ep01_t
(tempo 1.08 / 1.10 / 1.08). Sound: own sfx (series/klyuchevoy/sfx) + CC0 library + a cheerful CC0 bed with the voice-band dip."""
DUR = 33.6
FPS = 30
SLUG = 'klyuchevoy'
LUFS = -14.0

_D = dict(s1=1.87, e1=2.74, f1=3.46, e2=4.09, f3=5.27, s2=3.56, e4=2.27, f4=2.93, f5=1.46, f6=2.52, s3=1.87)
_T = dict(s1=0.00, e1=1.95, f1=4.78, e2=8.32, f3=12.60, s2=17.95, e4=21.70, f4=24.05, f5=27.10, f6=28.68, s3=31.32)
_W = dict(s='shef', e='edik', f='fikus')
_TX = dict(s1='Эдик, задержись на пять минут!', e1='Конечно! Я же ключевой сотрудник!', f1='Ключевой. От туалета.',
           e2='Пять минут с шефом — это повышение! Кабинет с окном!', f3='Полтора часа. С сентября перерабатывать можно двести сорок часов в год.',
           s2='Эдик, свет выключи и фикус полей. Ты же у нас ключевой!', e4='Повысили… до завхоза.',
           f4='Поздравляю. Теперь ты уходишь последним.', f5='Чаем не поливать!', f6='Пять минут у начальника — это до утра.',
           s3='Эдик! Задержись на пять минут!')
VOICE = [(k, 'ep01_t', k, _T[k], 0.0, _D[k], _W[k[0]], _TX[k]) for k in _T]
T0 = _T

#       hook  hat   fik1  key   whisp board clock sleep 240   twist throw e4    fik4  wide  tea   f6    loop
CUTS = [0.0, 1.95, 4.78, 6.40, 8.32, 10.40, 12.45, 13.60, 16.00, 17.95, 19.80, 21.70, 24.05, 25.60, 27.10, 28.68, 31.32, DUR]
NAMES = ['hook', 'hat', 'fik1', 'key', 'whisper', 'board', 'clock', 'sleep', 'f240', 'twist', 'throw', 'zavhoz', 'fik4', 'wide', 'tea',
         'f6', 'loop']
TWIST = CUTS[9]                  # 17.95 / 33.6 = 53 %

X = 'series/klyuchevoy/sfx/'
L = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'door_apartment_open.mp3', 0.00, 0.55),
    (L + 'cloth_rustle.mp3', 2.20, 0.6),
    (L + 'keys_on_table.mp3', 6.45, 0.35),
    (L + 'boing_cartoon.mp3', 6.55, 0.30),
    (L + 'cloth_rustle.mp3', 8.40, 0.45),
    (L + 'whoosh_1.mp3', 10.35, 0.40),
    (X + 'clock_spin.mp3', 12.45, 0.80),
    (X + 'keyboard_typing.mp3', 13.60, 0.35),
    (X + 'snore_office.mp3', 13.90, 0.45),
    (L + 'vinyl_scratch.mp3', 17.85, 0.50),
    (X + 'door_burst.mp3', 17.95, 0.95),
    (L + 'steps_concrete.mp3', 18.40, 0.35),
    (L + 'whoosh_3.mp3', 20.00, 0.45),
    (X + 'keyring_catch.mp3', 20.55, 0.85),
    (L + 'anvil_clank.mp3', 20.75, 0.30),
    (L + 'door_apartment_close.mp3', 23.60, 0.45),
    (X + 'light_switch.mp3', 25.55, 0.85),
    (X + 'tea_pour.mp3', 27.00, 1.00),
    (L + 'boing_cartoon.mp3', 27.35, 0.30),
    (L + 'rimshot_joke.mp3', 31.00, 0.45),
    (L + 'door_apartment_open.mp3', 31.20, 0.45),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'komiku_shoe_shop.mp3', 59.5, 0.0, TWIST - 0.1, 0.80, True, VOICE_DIP),
    (CM + 'komiku_fetch_contest.mp3', 41.5, TWIST + 0.15, DUR, 0.80, True, VOICE_DIP),
]
VGAIN = {'edik': 2.0, 'fikus': 2.2, 'shef': 1.9}
