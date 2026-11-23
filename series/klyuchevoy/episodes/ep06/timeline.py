"""S01E06 «СОТРУДНИК ГОДА» (season finale, standard «голливудский уровень»). Timing from the tightened takes voice/ep06_t."""
import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
import kscommon as KC
SLUG = 'klyuchevoy'
FPS = 30
LUFS = -14.0
ORDER = ['e1', 'f1', 's1', 's2', 's3', 'e2', 's4', 'f2', 'e3']
VOICE, T0, END = KC.timing('ep06', ORDER, gaps=dict(s3=0.9, e2=0.15, f2=0.3, e3=0.7), texts=KC.texts('ep06'))
DUR = round(END + 0.6, 2)
#       hook  fik1      award     walk      drum            e2        hug       carry     alone
CUTS = [0.0, T0['f1'], T0['s1'], T0['s2'], T0['s3'] - 0.9, T0['e2'], T0['s4'], T0['f2'], T0['e3'] - 0.6, DUR]
NAMES = ['hook', 'fik1', 'award', 'walk', 'drum', 'e2', 'hug', 'carry', 'alone']
TWIST = T0['s3'] + 0.9                       # «…фикус Аркадий!» — the name lands after the pause
L = 'library/cc0/sfx/'
CM = 'library/cc0/music/'
SFX = [
    (L + 'paper_handle.mp3', 0.05, 0.6),
    (L + 'steps_wood_floor.mp3', T0['s2'] + 0.3, 0.55),
    (L + 'clock_fast.mp3', T0['s3'] - 0.85, 0.5),
    (L + 'party_horn.mp3', TWIST, 0.7),
    (L + 'vinyl_scratch.mp3', T0['e2'] - 0.05, 0.45),
    (L + 'steps_wood_floor.mp3', T0['f2'] - 0.2, 0.6),
    (L + 'door_slam_office.mp3', T0['e3'] - 0.5, 0.7),
    (L + 'paper_crumple.mp3', DUR - 1.2, 0.5),
]
VOICE_DIP = 'equalizer=f=1800:t=q:w=1.3:g=-9,equalizer=f=500:t=q:w=1.2:g=-4'
BEDS = [
    (CM + 'freepd_baltic_levity.mp3', 48.0, 0.0, T0['s3'] - 0.9, 0.80, True, VOICE_DIP),
    (CM + 'freepd_managing_mischief.mp3', 164.0, TWIST - 0.2, T0['e3'] - 0.6, 0.80, True, VOICE_DIP),
    (CM + 'freepd_silly_boy.mp3', 95.5, T0['e3'] - 0.4, DUR, 0.70, True, VOICE_DIP),
]
VGAIN = {'edik': 2.0, 'fikus': 2.2, 'shef': 1.9, 'lyuda': 2.1}
