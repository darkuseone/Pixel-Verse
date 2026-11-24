"""S01E02 v2 «ГОДОВАЯ ПРЕМИЯ» (standard «голливудский уровень», reference = E01 v2 variant A). Voice: voice/ep02v2_t.
Sound: ONLY real CC0 recordings (BigSoundBank) + FreePD (CC0) live-instrument music. No loop at the end: the last line, then the card."""
DUR = 34.5
FPS = 30
SLUG = 'klyuchevoy'
LUFS = -14.0

_D = dict(l1=3.23, e1=3.13, f1=2.47, l2=1.81, l3=1.98, e3=1.97, l4=1.99, l6=2.54, e5=2.36, l5=2.45, e4=1.85, l7=1.01, s1=3.95, f2=2.45)
_T = dict(l1=0.00, e1=3.29, f1=6.48, l2=9.01, l3=10.88, e3=12.92, l4=14.95, l6=17.00, e5=19.60, l5=22.02, e4=24.53, l7=26.44, s1=27.55,
          f2=31.58)
_W = dict(l='lyuda', e='edik', f='fikus', s='shef')
_TX = dict(l1='Булкин, распишитесь. Годовая премия — сорок тысяч.', e1='Сорок тысяч?! Аркадий, я богат!', f1='Не спеши. У неё калькулятор.',
           l2='Минус налог. Тридцать пять.', l3='Минус опоздания. Двадцать.', e3='Я опоздал один раз!', l4='Двенадцать раз. По пять минут.',
           l6='Итого: вы должны компании триста рублей.', e5='Как… должен?!', l5='Взнос на юбилей шефа. Добровольный.',
           e4='Я не сдавал на юбилей!', l7='Вот и сдали.', s1='Булкин! Спасибо за часы! Мы же одна семья!',
           f2='Поздравляю. Ты премировал начальника.')
VOICE = [(k, 'ep02v2_t', k, _T[k], 0.0, _D[k], _W[k[0]], _TX[k]) for k in _T]
T0 = _T

#       hook  e1    fik   calc  l3    e3    l4    twist e5    board e4    l7    shef  f2
CUTS = [0.0, 3.29, 6.48, 9.01, 10.88, 12.92, 14.95, 17.00, 19.60, 22.02, 24.53, 26.44, 27.55, 31.58, DUR]
NAMES = ['hook', 'e1', 'fik1', 'calc', 'l3', 'e3', 'l4', 'twist', 'e5', 'board', 'e4', 'l7', 'shef', 'f2']
TWIST = CUTS[7]                  # 17.00 / 34.5 = 49 %

L = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'paper_handle.mp3', 0.05, 0.70),
    (L + 'pencil_sign.mp3', 1.20, 0.55),
    (L + 'cloth_rustle.mp3', 3.30, 0.45),
    (L + 'calc_key.mp3', 9.05, 0.9), (L + 'calc_key.mp3', 9.30, 0.9), (L + 'calc_key.mp3', 9.55, 0.9),
    (L + 'calc_printer_2.mp3', 9.80, 0.75),
    (L + 'calc_key.mp3', 10.90, 0.9), (L + 'calc_key.mp3', 11.15, 0.9),
    (L + 'calc_printer_2.mp3', 11.40, 0.75),
    (L + 'calc_printer.mp3', 17.00, 0.85),
    (L + 'calc_ticket_tear.mp3', 19.40, 0.95),
    (L + 'whoosh_1.mp3', 22.00, 0.35),
    (L + 'paper_crumple.mp3', 26.60, 0.70),
    (L + 'steps_wood_floor.mp3', 27.50, 0.65),
    (L + 'keys_jingle.mp3', 28.70, 0.35),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'freepd_baltic_levity.mp3', 48.0, 0.0, 9.0, 0.80, True, VOICE_DIP),
    (CM + 'freepd_busybody.mp3', 86.4, 9.0, TWIST - 0.05, 0.75, True, VOICE_DIP),
    (CM + 'freepd_fensters_explanation.mp3', 168.9, 19.55, 27.50, 0.70, True, VOICE_DIP),
    (CM + 'freepd_silly_boy.mp3', 95.5, 27.50, DUR, 0.80, True, VOICE_DIP),
]
VGAIN = {'edik': 2.0, 'fikus': 2.2, 'shef': 1.9, 'lyuda': 2.1}
