"""S01E04 «ОТПУСК» (standard «голливудский уровень»). Timing from the tightened takes voice/ep04_t."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import kscommon as KC
SLUG = 'klyuchevoy'
FPS = 30
LUFS = -14.0
ORDER = ['l1', 'e1', 'l2', 'e2', 'l3', 'l4', 'e4', 'f1', 'e5', 'l5', 'f2']
VOICE, T0, END = KC.timing('ep04', ORDER, gaps=dict(f1=0.5, f2=0.2), texts=KC.texts('ep04'))
DUR = round(END + 0.55, 2)
CAL = T0['f1'] + 1.5                       # the calendar insert in the middle of the ficus line
#       hook  e1     chart1   e2     l3      chart2  e4    fik    cal   e5      l5      f2
CUTS = [0.0, T0['e1'], T0['l2'], T0['e2'], T0['l3'], T0['l4'], T0['e4'], T0['f1'] - 0.3, CAL, T0['e5'], T0['l5'], T0['f2'], DUR]
NAMES = ['hook', 'e1', 'chart1', 'e2', 'l3', 'chart2', 'e4', 'fik', 'cal', 'e5', 'l5', 'f2']
TWIST = T0['f1'] - 0.3
L = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'paper_handle.mp3', 0.05, 0.7),
    (L + 'paper_handle.mp3', T0['l2'], 0.5),
    (L + 'pencil_sign.mp3', T0['l4'] + 0.6, 0.5),
    (L + 'pencil_sign.mp3', T0['e4'] + 0.2, 0.7),
    (L + 'anvil_clank.mp3', T0['e4'] + 0.55, 0.35),
    (L + 'vinyl_scratch.mp3', TWIST - 0.05, 0.45),
    (L + 'whoosh_3.mp3', CAL - 0.05, 0.4),
    (L + 'paper_crumple.mp3', T0['l5'] + 0.4, 0.5),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'freepd_fensters_explanation.mp3', 168.9, 0.0, TWIST - 0.1, 0.75, True, VOICE_DIP),
    (CM + 'freepd_silly_boy.mp3', 95.5, T0['e5'], DUR, 0.80, True, VOICE_DIP),
]
VGAIN = {'edik': 2.0, 'fikus': 2.2, 'shef': 1.9, 'lyuda': 2.1}
