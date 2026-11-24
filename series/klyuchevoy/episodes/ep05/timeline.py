"""S01E05 «НЕ ТОТ ЧАТ» (standard «голливудский уровень»). Timing from the tightened takes voice/ep05_t."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import kscommon as KC
SLUG = 'klyuchevoy'
FPS = 30
LUFS = -14.0
ORDER = ['e1', 'f1', 'e2', 'f2', 'l1', 'e3', 'f3', 's1', 'e4', 's2', 'f4']
VOICE, T0, END = KC.timing('ep05', ORDER, gaps=dict(f2=0.9, s1=0.5, f4=0.2), texts=KC.texts('ep05'))
DUR = round(END + 0.55, 2)
PH1 = T0['e1'] + 2.0                          # the phone insert during «…в общий чат»
DEL = T0['e2'] + 1.6                          # «Удалить у всех…»
#       hook  phone fik1     e2      deleted printer  lyuda   e3      printer2 shef   e4      shef2   f4
CUTS = [0.0, PH1, T0['f1'], T0['e2'], DEL, T0['f2'] - 0.9, T0['l1'], T0['e3'], T0['f3'], T0['s1'] - 0.5, T0['e4'], T0['s2'], T0['f4'], DUR]
NAMES = ['hook', 'phone', 'fik1', 'e2', 'deleted', 'printer', 'lyuda', 'e3', 'printer2', 'shef', 'e4', 'shef2', 'f4']
TWIST = T0['l1']
L = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'message_sent.mp3', 0.05, 0.9),
    (L + 'phone_key_click.mp3', DEL - 0.6, 0.7), (L + 'phone_key_click.mp3', DEL - 0.3, 0.7),
    (L + 'message_sent.mp3', DEL + 0.3, 0.6),
    (L + 'printer_start.mp3', T0['f2'] - 0.85, 0.9),
    (L + 'printer_print.mp3', T0['l1'] - 0.3, 0.75),
    (L + 'printer_print.mp3', T0['f3'] - 0.2, 0.85),
    (L + 'paper_handle.mp3', T0['s1'] - 0.45, 0.8),
    (L + 'steps_wood_floor.mp3', T0['s1'] - 0.5, 0.5),
    (L + 'paper_crumple.mp3', T0['f4'] + 0.2, 0.5),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'freepd_busybody.mp3', 86.4, 0.0, T0['f2'] - 0.9, 0.80, True, VOICE_DIP),
    (CM + 'freepd_lurking_sloth.mp3', 157.8, T0['f2'] - 0.6, T0['s1'] - 0.5, 0.80, True, VOICE_DIP),
    (CM + 'freepd_fensters_explanation.mp3', 168.9, T0['s1'] - 0.3, DUR, 0.70, True, VOICE_DIP),
]
VGAIN = {'edik': 2.0, 'fikus': 2.2, 'shef': 1.9, 'lyuda': 2.1}
