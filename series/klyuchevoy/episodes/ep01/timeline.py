"""S01E01 v2 «ЗАДЕРЖИСЬ НА 5 МИНУТ!» (standard «голливудский уровень», 22.11.2026) — timing for video (ep01.py / ep01b) and audio.
Voice: voice/ep01v2_t (tempo 1.10). Sound: ONLY real CC0 recordings (BigSoundBank) + FreePD (CC0) live-instrument music — no MIDI/chiptune."""
DUR = 33.9
FPS = 30
SLUG = 'klyuchevoy'
LUFS = -14.0

_D = dict(s1=3.31, e1=3.37, f1=4.29, e2=3.37, f2=1.99, e3=3.35, s2=4.02, e4=1.65, s3=2.96, e5=1.88, f3=2.07)
_T = dict(s1=0.00, e1=3.37, f1=6.80, e2=11.15, f2=14.58, e3=16.65, s2=20.08, e4=24.16, s3=25.87, e5=28.93, f3=30.87)
_W = dict(s='shef', e='edik', f='fikus')
_TX = dict(s1='Булкин! Задержись на пять минут. Разговор есть.', e1='Аркадий, слышал? Разговор! Меня повышают!',
           f1='Семнадцать лет назад он так же сказал. Ты потом до ночи шкаф двигал.', e2='Тогда я был стажёр. А сейчас я — ключевой!',
           f2='У тебя ключ от туалета.', e3='Девять вечера… Он проверяет мою преданность.',
           s2='О, Булкин, ты ещё тут? Отлично! Закроешь офис.', e4='А… разговор?', s3='Так это и был разговор! Свет не забудь.',
           e5='Аркадий… меня повысили.', f3='До сторожа. Зарплата та же.',)
VOICE = [(k, 'ep01v2_t', k, _T[k], 0.0, _D[k], _W[k[0]], _TX[k]) for k in _T]
T0 = _T

#       hook  aside fik   flash proud fkey  key   clock chair twist e4    exit  dark  f3
CUTS = [0.0, 3.37, 6.80, 9.10, 11.15, 14.58, 15.60, 16.65, 17.85, 20.08, 24.16, 25.87, 28.93, 30.87, DUR]
NAMES = ['hook', 'aside', 'fik1', 'flash', 'proud', 'fkey', 'key', 'clock', 'chair', 'twist', 'e4', 'exit', 'dark', 'f3']
TWIST = CUTS[9]                  # 20.08 / 33.9 = 59 %  (no loop at the end — owner 22.11.2026: last line, then the subscribe card)

L = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'clock_tick.mp3', 0.00, 0.55),
    (L + 'coat_rustle.mp3', 0.10, 0.60),
    (L + 'coat_rustle.mp3', 3.30, 0.45),
    (L + 'whoosh_1.mp3', 8.95, 0.35),
    (L + 'chair_creak.mp3', 9.15, 0.85),
    (L + 'steps_wood_floor.mp3', 9.45, 0.55),
    (L + 'whoosh_3.mp3', 11.05, 0.35),
    (L + 'cloth_rustle.mp3', 11.45, 0.45),
    (L + 'keys_jingle.mp3', 15.60, 0.55),
    (L + 'clock_fast.mp3', 16.65, 0.70),
    (L + 'chair_creak.mp3', 17.95, 0.35),
    (L + 'door_unlock_open.mp3', 19.80, 0.85),
    (L + 'steps_wood_floor.mp3', 20.55, 0.60),
    (L + 'keys_jingle.mp3', 23.10, 1.00),
    (L + 'keys_on_table.mp3', 23.30, 0.70),
    (L + 'steps_wood_floor.mp3', 25.95, 0.55),
    (L + 'light_switch_click.mp3', 28.58, 1.00),
    (L + 'door_slam_office.mp3', 28.78, 0.90),
    (L + 'clock_tick.mp3', 28.93, 0.45),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'freepd_baltic_levity.mp3', 48.0, 0.0, 16.65, 0.80, True, VOICE_DIP),
    (CM + 'freepd_lurking_sloth.mp3', 157.8, 16.65, TWIST - 0.05, 0.85, True, VOICE_DIP),
    (CM + 'freepd_fensters_explanation.mp3', 168.9, 24.10, 28.58, 0.70, True, VOICE_DIP),
    (CM + 'freepd_silly_boy.mp3', 95.5, 30.80, DUR, 0.80, True, VOICE_DIP),
]
VGAIN = {'edik': 2.0, 'fikus': 2.2, 'shef': 1.9}
