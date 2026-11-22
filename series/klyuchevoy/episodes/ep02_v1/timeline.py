"""S01E02 «ПРЕМИИ НЕ БУДЕТ?!» — timing for video (ep02.py) and audio (mix.py). Voice: voice/ep02_t (tempo 1.08 / 1.10)."""
DUR = 34.6
FPS = 30
SLUG = 'klyuchevoy'
LUFS = -14.0

_D = dict(l1=2.64, e1=3.69, f1=3.45, l2=2.96, e3=2.65, f3=0.76, f4=1.75, e4=2.85, s1=2.75, f5=1.91, s2=3.32, e5=1.53, f6=3.05)
_T = dict(l1=0.00, e1=2.70, f1=6.45, l2=9.98, e3=13.02, f3=15.80, f4=16.70, e4=18.55, s1=21.50, f5=24.35, s2=26.36, e5=29.78, f6=31.40)
_W = dict(l='lyuda', e='edik', f='fikus', s='shef')
_TX = dict(l1='Эдуард, премии в этом году не будет.', e1='Как не будет?! Я уже посчитал: сорок тысяч!', f1='Шуба за двадцать — это шапка.',
           l2='Не положено. Треть компаний премию не платит.', e3='Тогда я найду, кто украл мою премию!', f3='Теплее.', f4='Горячо.',
           e4='Это я в январе… для галочки!', s1='А мы приняли! Мы же одна семья!', f5='В семье тоже не платят.',
           s2='Зато вот тебе грамота! За экономию!', e5='На обороте счёта?!', f6='У каждого в офисе есть такой экономист. Отправь ему.')
VOICE = [(k, 'ep02_t', k, _T[k], 0.0, _D[k], _W[k[0]], _TX[k]) for k in _T]
T0 = _T

#       hook  e1cu  calc  fik1  l2cu  cooler door  board twist e4    hug   f5    gram  back  f6
CUTS = [0.0, 2.70, 4.60, 6.45, 9.98, 13.02, 15.70, 16.60, 17.60, 19.20, 21.45, 24.30, 26.30, 29.70, 31.40, DUR]
NAMES = ['hook', 'e1cu', 'calc', 'fik1', 'l2cu', 'cooler', 'door', 'board', 'twist', 'e4', 'hug', 'f5', 'gram', 'back', 'f6']
TWIST = CUTS[8]                  # 17.60 / 34.6 = 51 %

X = 'series/klyuchevoy/sfx/'
L = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'anvil_clank.mp3', 0.05, 0.40),
    (X + 'keyboard_typing.mp3', 3.00, 0.30),
    (L + 'phone_key_click.mp3', 4.70, 0.6),
    (L + 'phone_key_click.mp3', 5.20, 0.6),
    (L + 'phone_key_click.mp3', 5.70, 0.6),
    (L + 'rimshot_joke.mp3', 9.40, 0.40),
    (L + 'anvil_clank.mp3', 12.20, 0.30),
    (L + 'whoosh_1.mp3', 13.00, 0.45),
    (L + 'chair_creak.mp3', 13.60, 0.45),
    (L + 'slipper_steps.mp3', 15.60, 0.45),
    (L + 'whoosh_3.mp3', 16.55, 0.40),
    (L + 'vinyl_scratch.mp3', 17.50, 0.55),
    (L + 'gong_strong.mp3', 17.62, 0.35),
    (L + 'door_apartment_open.mp3', 21.30, 0.45),
    (L + 'cloth_rustle.mp3', 21.70, 0.55),
    (L + 'whoosh_1.mp3', 26.30, 0.40),
    (L + 'cloth_rustle.mp3', 29.70, 0.55),
    (L + 'boing_cartoon.mp3', 29.85, 0.30),
    (L + 'rimshot_joke.mp3', 33.30, 0.40),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'komiku_weekly_fair.mp3', 59.5, 0.0, TWIST - 0.1, 0.80, True, VOICE_DIP),
    (CM + 'komiku_mandolin.mp3', 59.5, TWIST + 0.15, DUR, 0.80, True, VOICE_DIP),
]
VGAIN = {'edik': 2.0, 'fikus': 2.2, 'shef': 1.9, 'lyuda': 2.1}
